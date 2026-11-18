"""Ingestion: load markdown + PDF files, extract clean text and metadata, detect versions.

Run:  python -m src.ingest
Writes:
  data/processed/documents.jsonl  one JSON record per document (input to chunking)
  data/processed/manifest.json    content hash + extracted text per file, so unchanged
                                  files are skipped on the next run
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pymupdf
import yaml

from src.config import load_config, read_yaml, resolve_path

# Bump this whenever extract_markdown/extract_pdf change: cached text made by older code
# is then re-extracted even though the files' hashes are unchanged.
EXTRACTOR_VERSION = 4

MIN_DOC_CHARS = 200   # docs shorter than this after cleaning (e.g. link-only index pages) are dropped
EDGE_LINES = 8         # max lines at the top/bottom of a PDF page that count as header/footer zone
REPEAT_SHARE = 0.5     # a line repeated in the edge zone of >= 50% of pages is a header/footer


@dataclass
class SourceFile:
    """One file to ingest."""
    path: Path                         # absolute path on disk
    rel_path: str                      # path relative to raw_dir, e.g. "handbook/finance/expenses.md"
    source_type: str                   # "markdown" | "pdf"
    pdf_entry: dict[str, Any] | None = None  # the PDF's entry from sources.yaml


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------

def file_hash(path: Path) -> str:
    """SHA-256 of the file's bytes: identical files always give the identical hash."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):  # read in 64 KB blocks, not all at once
            digest.update(block)
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FRONT_MATTER_KEYS = ("title", "version_group", "is_current", "updated_date", "synthetic_old_version")


def split_front_matter(raw: str) -> tuple[dict[str, Any], str]:
    """Split the YAML block between the leading '---' lines from the markdown body."""
    match = FRONT_MATTER_RE.match(raw)
    if not match:
        return {}, raw
    try:
        meta = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        meta = {}
    if not isinstance(meta, dict):
        meta = {}
    meta = {str(k).lower(): v for k, v in meta.items()}  # some pages write "Title:" instead of "title:"
    # Keep only the keys we use; YAML can produce date objects, so turn dates into strings.
    kept = {k: meta[k] for k in FRONT_MATTER_KEYS if k in meta}
    if "updated_date" in kept:
        kept["updated_date"] = str(kept["updated_date"])
    return kept, raw[match.end():]


def clean_markdown(body: str) -> str:
    """Remove site markup (shortcodes, HTML, link URLs) but keep headings, lists and tables."""
    text = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)            # HTML comments
    text = re.sub(r"\{\{[<%].*?[%>]\}\}", "", text, flags=re.DOTALL)  # Hugo shortcodes {{< x >}}
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)                  # images
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)              # [text](url) -> text
    text = re.sub(r"<[^>\n]+>", "", text)                             # HTML tags (inner text kept)
    text = re.sub(r"[ \t]*\{#[\w-]+\}", "", text)                     # heading anchors {#my-id}
    text = re.sub(r"[ \t]+\n", "\n", text)                            # trailing spaces
    text = re.sub(r"\n{3,}", "\n\n", text)                            # max one blank line
    return text.strip()


def first_heading(text: str) -> str | None:
    """Return the text of the first '# ' heading, if any."""
    match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def extract_markdown(path: Path) -> dict[str, Any]:
    """Read a markdown file -> {"title", "front_matter", "pages"} (markdown is one 'page')."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    front_matter, body = split_front_matter(raw)
    text = clean_markdown(body)
    title = front_matter.get("title") or first_heading(text)
    return {"title": title, "front_matter": front_matter, "pages": [{"page": None, "text": text}]}


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

TOC_LINE_RE = re.compile(r"(\.\s?){5,}|…{2,}")  # dot leaders: "Purpose ........ 3"
PAGE_NUMBER_RE = re.compile(r"^[-–\s]*(page\s*)?#(\s*(of|/)\s*#)?[-–\s]*$")  # "3", "page 3 of 9", "- 3 -"


def normalize_line(line: str) -> str:
    """Lower-case, squeeze spaces and replace digits with '#', so 'Page 3' and 'Page 4' compare equal."""
    return re.sub(r"\d+", "#", re.sub(r"\s+", " ", line)).strip().lower()


def edge_size(n_lines: int) -> int:
    """Lines at each end of a page that may be header/footer: at most EDGE_LINES, and at most
    a third of the page, so a short page never has its body treated as header/footer."""
    return min(EDGE_LINES, n_lines // 3)


def edge_lines(lines: list[str]) -> list[str]:
    """The top and bottom zone of one page."""
    k = edge_size(len(lines))
    return lines[:k] + lines[len(lines) - k:] if k else []


def find_repeated_edge_lines(pages: list[list[str]]) -> set[str]:
    """Find normalized lines that appear in the top/bottom zone of most pages."""
    if len(pages) < 3:  # too few pages to tell a header from normal text
        return set()
    counts: Counter[str] = Counter()
    for lines in pages:
        counts.update({normalize_line(line) for line in edge_lines(lines)})  # a set: once per page
    min_pages = max(2, int(len(pages) * REPEAT_SHARE))
    # Require a letter: numbering like "5.3" and "8.1" normalizes to the same "#.#" on every
    # page but is real structure. Bare page numbers are caught by PAGE_NUMBER_RE instead.
    return {line for line, n in counts.items()
            if n >= min_pages and re.search(r"[a-z]", line)}


def strip_headers_footers(pages: list[list[str]]) -> list[list[str]]:
    """Drop repeated header/footer lines and bare page numbers from each page's edge zone.

    Only lines in a page's edge zone can be removed, so body text that happens to repeat
    (e.g. a heading used on several pages) is never touched.
    """
    repeated = find_repeated_edge_lines(pages)
    cleaned = []
    for lines in pages:
        n, k = len(lines), edge_size(len(lines))
        kept = []
        for i, line in enumerate(lines):
            in_edge_zone = i < k or i >= n - k
            norm = normalize_line(line)
            if in_edge_zone and (norm in repeated or PAGE_NUMBER_RE.match(norm)):
                continue
            kept.append(line)
        cleaned.append(kept)
    return cleaned


SECTION_NUMBER_RE = re.compile(r"^\d+(\.\d+)*\.?$")  # "1.", "2.4", "3.6.1"
MIN_NUMBER_RUN = 3


def remove_table_of_contents(lines: list[str]) -> list[str]:
    """Drop table-of-contents residue from one page.

    - Lines with dot leaders ("Purpose ........ 3").
    - Runs of 3+ consecutive lines that are only section numbers ("1.", "1.1", "1.2", ...):
      some PDFs store the ToC numbers as a separate column. A single "5.3" line is a real
      clause heading and is kept.
    """
    lines = [line for line in lines if not TOC_LINE_RE.search(line)]
    kept: list[str] = []
    run: list[str] = []  # current run of number-only lines
    for line in lines + [""]:  # "" sentinel flushes the last run
        if SECTION_NUMBER_RE.match(line):
            run.append(line)
            continue
        if len(run) < MIN_NUMBER_RUN:
            kept.extend(run)
        run = []
        if line:
            kept.append(line)
    return kept


def pdf_date(raw: str | None) -> str | None:
    """Convert a PDF date like "D:20251112153048+00'00'" to "2025-11-12"."""
    match = re.match(r"D:(\d{4})(\d{2})(\d{2})", raw or "")
    return f"{match[1]}-{match[2]}-{match[3]}" if match else None


def extract_pdf(path: Path) -> dict[str, Any]:
    """Read a PDF -> {"title", "file_date", "pages"} with headers/footers stripped."""
    with pymupdf.open(path) as doc:
        raw_pages = [
            [line.strip() for line in page.get_text().splitlines() if line.strip()]
            for page in doc
        ]
        meta = doc.metadata or {}
    pages = strip_headers_footers(raw_pages)
    pages = [remove_table_of_contents(lines) for lines in pages]
    return {
        "title": meta.get("title") or None,
        "file_date": pdf_date(meta.get("modDate")) or pdf_date(meta.get("creationDate")),
        "pages": [{"page": i + 1, "text": "\n".join(lines)} for i, lines in enumerate(pages)],
    }


# ---------------------------------------------------------------------------
# Building document records
# ---------------------------------------------------------------------------

def handbook_doc_id(rel_path: str) -> str:
    """'handbook/legal/testing-agreement-v3.md' -> 'hb:legal/testing-agreement-v3'.

    Hugo stores a folder's own page as _index.md, so 'finance/_index.md' -> 'hb:finance'.
    """
    parts = list(Path(rel_path).with_suffix("").parts[1:])  # drop the leading "handbook"
    if parts[-1] == "_index":
        parts = parts[:-1]
    return "hb:" + "/".join(parts)


def access_roles_for(department: str, sources: dict[str, Any]) -> list[str]:
    """Simulated access roles, looked up by department in sources.yaml."""
    roles_cfg = sources.get("access_roles", {})
    return list(roles_cfg.get("by_department", {}).get(department, roles_cfg.get("default", ["all_employees"])))


def build_record(src: SourceFile, extraction: dict[str, Any], content_hash: str,
                 sources: dict[str, Any], commit_dates: dict[str, str]) -> dict[str, Any]:
    """Combine extracted text with metadata into one document record.

    Metadata is rebuilt on every run (cheap), so editing sources.yaml takes effect
    even when the file itself is unchanged and its text comes from the cache.
    """
    if src.source_type == "markdown":
        front = extraction["front_matter"]
        handbook_rel = src.rel_path.split("/", 1)[1]  # path inside the handbook folder
        doc_id = handbook_doc_id(src.rel_path)
        department = handbook_rel.split("/")[0]
        title = extraction["title"] or doc_id.rsplit("/", 1)[-1]
        updated = front.get("updated_date") or commit_dates.get(handbook_rel)
        explicit_group = front.get("version_group")
        explicit_current = front.get("is_current")
        synthetic = bool(front.get("synthetic_old_version", False))
    else:
        entry = src.pdf_entry or {}
        doc_id = f"pdf:{entry['id']}"
        department = entry.get("department", "general")
        title = entry.get("title") or extraction["title"] or entry["id"]
        updated = entry.get("updated_date") or extraction["file_date"]
        explicit_group = entry.get("version_group")
        explicit_current = entry.get("is_current")
        synthetic = bool(entry.get("synthetic_old_version", False))

    return {
        "doc_id": doc_id,
        "doc_title": str(title).strip(),
        "source_type": src.source_type,
        "source_path": src.rel_path,
        "department": department,
        "access_roles": access_roles_for(department, sources),
        "updated_date": str(updated) if updated else None,
        "version_group": explicit_group,      # filled in by assign_versions()
        "version_number": None,
        "is_current": explicit_current,       # filled in by assign_versions()
        "synthetic_old_version": synthetic,
        "content_hash": content_hash,
        "pages": extraction["pages"],
    }


# ---------------------------------------------------------------------------
# Version detection
# ---------------------------------------------------------------------------

VERSION_SUFFIX_RE = re.compile(r"-v(\d+)$")
LEGACY_RE = re.compile(r"\b(legacy|deprecated|superseded|archived)\b", re.IGNORECASE)


def handbook_version_key(doc_id: str) -> tuple[str, int | None]:
    """'hb:legal/legacy/legacy-psa-v2' -> ('legal/psa', 2). Strips 'legacy-' and '-vN' from the name."""
    parts = doc_id.removeprefix("hb:").split("/")
    stem = parts[-1].removeprefix("legacy-")
    match = VERSION_SUFFIX_RE.search(stem)
    version = int(match.group(1)) if match else None
    return f"{parts[0]}/{VERSION_SUFFIX_RE.sub('', stem)}", version


def looks_legacy(record: dict[str, Any]) -> bool:
    """True if the path, title or a banner on the first line marks the document as old.

    Only the first line is checked: a page that merely *mentions* something deprecated
    ("password login has been deprecated") is not itself an old version.
    """
    if "legacy" in record["source_path"].lower():
        return True
    if LEGACY_RE.search(record["doc_title"]):
        return True
    text = record["pages"][0]["text"].lstrip() if record["pages"] else ""
    first_line = text.split("\n", 1)[0]
    return bool(re.search(r"\bdeprecated\b", first_line, re.IGNORECASE))


def assign_versions(records: list[dict[str, Any]]) -> None:
    """Set version_group, version_number and is_current on every record (in place).

    Grouping: explicit group (front matter / sources.yaml) wins. Otherwise handbook files
    with the same name after removing 'legacy-' / '-vN' are grouped, but only when at least
    one of them shows real evidence of versioning; everything else is its own group.

    Current version per group: explicit is_current wins; legacy/deprecated docs are never
    current; then the unversioned file (the live page), then highest -vN, then newest date.
    """
    legacy = {r["doc_id"]: looks_legacy(r) for r in records}

    # 1. Candidate groups from file names.
    candidates: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        if r["source_type"] == "markdown":
            key, r["version_number"] = handbook_version_key(r["doc_id"])
            candidates["hb:" + key].append(r)

    # 2. Keep a name-based group only if it has versioning evidence.
    for key, members in candidates.items():
        has_evidence = any(m["version_number"] is not None or legacy[m["doc_id"]] for m in members)
        for m in members:
            if m["version_group"] is None:
                m["version_group"] = key if (len(members) > 1 and has_evidence) else m["doc_id"]
    for r in records:
        if r["version_group"] is None:
            r["version_group"] = r["doc_id"]

    # 3. Pick the current version inside each group.
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in records:
        groups[r["version_group"]].append(r)

    for members in groups.values():
        explicit_current = any(m["is_current"] is True for m in members)
        undecided = [m for m in members if m["is_current"] is None]
        for m in undecided:
            m["is_current"] = False
        live = [m for m in undecided if not legacy[m["doc_id"]]]
        if live and not explicit_current:
            newest = max(live, key=lambda m: (m["version_number"] is None,   # unversioned page = live page
                                              m["version_number"] or 0,
                                              m["updated_date"] or ""))
            newest["is_current"] = True


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def discover_files(raw_dir: Path, sources: dict[str, Any]) -> tuple[list[SourceFile], list[str]]:
    """List handbook markdown files and the PDFs named in sources.yaml. Also returns missing PDF ids."""
    files = [
        SourceFile(p, p.relative_to(raw_dir).as_posix(), "markdown")
        for p in sorted((raw_dir / "handbook").rglob("*.md"))
    ]
    missing = []
    for entry in sources.get("pdfs", []):
        path = raw_dir / "pdfs" / f"{entry['id']}.pdf"
        if path.exists():
            files.append(SourceFile(path, path.relative_to(raw_dir).as_posix(), "pdf", entry))
        else:
            missing.append(entry["id"])
    return files, missing


def extract(src: SourceFile) -> dict[str, Any]:
    """Run the right extractor for the file type."""
    return extract_markdown(src.path) if src.source_type == "markdown" else extract_pdf(src.path)


def ingest_all(raw_dir: Path, processed_dir: Path, sources: dict[str, Any]) -> Counter[str]:
    """Ingest every source file, reusing cached text for files whose hash hasn't changed."""
    processed_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = processed_dir / "manifest.json"
    old_manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    dates_path = raw_dir / "handbook" / "_dates.json"
    commit_dates = json.loads(dates_path.read_text()) if dates_path.exists() else {}

    files, missing_pdfs = discover_files(raw_dir, sources)
    stats: Counter[str] = Counter(missing_pdfs=len(missing_pdfs))
    new_manifest: dict[str, Any] = {}
    records = []

    for src in files:
        content_hash = file_hash(src.path)
        cached = old_manifest.get(src.rel_path)
        if (cached and cached["content_hash"] == content_hash
                and cached.get("extractor_version") == EXTRACTOR_VERSION):
            extraction = cached["extraction"]
            stats["skipped_unchanged"] += 1
        else:
            extraction = extract(src)
            stats["extracted"] += 1
        new_manifest[src.rel_path] = {"content_hash": content_hash,
                                      "extractor_version": EXTRACTOR_VERSION,
                                      "extraction": extraction}

        record = build_record(src, extraction, content_hash, sources, commit_dates)
        if sum(len(p["text"]) for p in record["pages"]) < MIN_DOC_CHARS:
            stats["dropped_too_short"] += 1
            continue
        records.append(record)

    stats["removed_since_last_run"] = len(set(old_manifest) - set(new_manifest))
    assign_versions(records)
    stats["documents"] = len(records)

    with open(processed_dir / "documents.jsonl", "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    manifest_path.write_text(json.dumps(new_manifest, ensure_ascii=False))
    return stats


def load_documents(processed_dir: Path) -> list[dict[str, Any]]:
    """Read documents.jsonl back into a list of dicts."""
    with open(processed_dir / "documents.jsonl", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def print_summary(stats: Counter[str], records: list[dict[str, Any]]) -> None:
    """Print run counts plus a breakdown of the corpus."""
    print("Run:", ", ".join(f"{k}={v}" for k, v in sorted(stats.items())))
    print("By source type:", dict(Counter(r["source_type"] for r in records)))
    print("By department: ", dict(Counter(r["department"] for r in records).most_common()))
    multi = defaultdict(list)
    for r in records:
        multi[r["version_group"]].append(r)
    multi = {g: m for g, m in multi.items() if len(m) > 1}
    print(f"Version groups with >1 document: {len(multi)}  "
          f"(non-current docs: {sum(not r['is_current'] for r in records)})")
    no_date = sum(r["updated_date"] is None for r in records)
    print(f"Docs without updated_date: {no_date}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest data/raw into data/processed/documents.jsonl")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()

    paths = load_config(args.config)["paths"]
    sources = read_yaml(resolve_path(paths["sources"]))
    processed_dir = resolve_path(paths["processed_dir"])
    stats = ingest_all(resolve_path(paths["raw_dir"]), processed_dir, sources)
    print_summary(stats, load_documents(processed_dir))


if __name__ == "__main__":
    main()
