"""Chunking: split documents into token-limited chunks that carry full metadata.

Strategies (config: chunking.strategy)
  fixed    sliding window of chunk_size tokens, moving forward by chunk_size - chunk_overlap
  heading  one chunk per markdown section; long sections are split with the fixed window,
           tiny ones merged into the next section. PDFs have no reliable headings, so they
           fall back to the fixed window.

Run:  python -m src.chunking configs/baseline.yaml
Writes data/processed/chunks/<strategy_key>.jsonl and prints size + truncation stats.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import re
import statistics
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from src.config import load_config, resolve_path
from src.ingest import load_documents

PAGE_SEPARATOR = "\n\n"  # PDF pages are joined with this into one document string
# Bump when chunk_document's output changes (new field, new rule): existing chunk files are then rebuilt.
CHUNKER_VERSION = 2

# How many tokens each embedding model actually reads; everything after is silently dropped.
# (Values from each model's sentence-transformers config; Phase 4 checks them against the loaded model.)
EMBEDDING_MAX_TOKENS = {
    "sentence-transformers/all-MiniLM-L6-v2": 256,
    "BAAI/bge-small-en-v1.5": 512,
}
SPECIAL_TOKENS = 2  # the model adds [CLS] at the start and [SEP] at the end of every input

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


# ---------------------------------------------------------------------------
# Tokens
# ---------------------------------------------------------------------------

@lru_cache(maxsize=4)
def get_tokenizer(name: str):
    """Load a Hugging Face tokenizer once (transformers comes with sentence-transformers)."""
    from transformers import AutoTokenizer  # imported here so tests of pure functions stay fast

    tokenizer = AutoTokenizer.from_pretrained(name)
    tokenizer.model_max_length = 10**9  # we tokenize whole documents; silence the "too long" warning
    return tokenizer


def token_offsets(text: str, tokenizer) -> list[tuple[int, int]]:
    """Character span (start, end) of every token in `text`, without [CLS]/[SEP]."""
    encoded = tokenizer(text, add_special_tokens=False, return_offsets_mapping=True)
    return [tuple(span) for span in encoded["offset_mapping"]]


def count_tokens(text: str, tokenizer) -> int:
    """Number of tokens in `text` (without special tokens)."""
    return len(tokenizer(text, add_special_tokens=False)["input_ids"])


# ---------------------------------------------------------------------------
# Sliding window
# ---------------------------------------------------------------------------

def is_word_start(offsets: list[tuple[int, int]], i: int) -> bool:
    """True if token i begins a new word, i.e. there is whitespace before it.

    Tokenizers split rare words into pieces ("reimbursement" -> "rei", "##mb", ...);
    we never want a chunk to start or end in the middle of such a word.
    """
    return i == 0 or i >= len(offsets) or offsets[i][0] > offsets[i - 1][1]


def window_spans(offsets: list[tuple[int, int]], t_start: int, t_end: int,
                 size: int, overlap: int) -> list[tuple[int, int]]:
    """Token ranges [a, b) covering tokens t_start..t_end with windows of <= size tokens.

    Each window starts `size - overlap` tokens after the previous one, so neighbours share
    about `overlap` tokens. Edges are nudged to word boundaries.
    """
    step = size - overlap
    spans: list[tuple[int, int]] = []
    a = t_start
    while a < t_end:
        b = min(a + size, t_end)
        while b < t_end and b > a + 1 and not is_word_start(offsets, b):
            b -= 1  # don't cut a word in half at the end
        spans.append((a, b))
        if b >= t_end:
            break
        next_a = max(a + step, a + 1) if b - a >= step else b  # if b was pulled back a lot, continue from b
        while next_a < b and not is_word_start(offsets, next_a):
            next_a += 1  # don't start in the middle of a word
        a = next_a
    return spans


# ---------------------------------------------------------------------------
# Document structure: full text, pages, headings
# ---------------------------------------------------------------------------

@dataclass
class Heading:
    char_pos: int   # where the heading line starts in the document text
    level: int      # 1 for "#", 2 for "##", ...
    path: str       # full trail, e.g. "Expenses > Travel > Hotels"


def document_text(doc: dict[str, Any]) -> tuple[str, list[int]]:
    """Join a document's pages into one string. Returns (text, start offset of each page)."""
    starts, parts, pos = [], [], 0
    for page in doc["pages"]:
        starts.append(pos)
        parts.append(page["text"])
        pos += len(page["text"]) + len(PAGE_SEPARATOR)
    return PAGE_SEPARATOR.join(parts), starts


def clean_heading(text: str) -> str:
    """Strip markdown emphasis from a heading: '**Travel**' -> 'Travel'."""
    return re.sub(r"[*_`]+", "", text).strip()


def find_headings(text: str) -> list[Heading]:
    """Find markdown headings (ignoring '#' lines inside ``` code blocks) and their full paths."""
    headings: list[Heading] = []
    stack: list[tuple[int, str]] = []  # (level, title) of the current heading trail
    in_code, pos = False, 0
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            in_code = not in_code
        elif not in_code and (match := HEADING_RE.match(line)):
            level, title = len(match.group(1)), clean_heading(match.group(2))
            while stack and stack[-1][0] >= level:
                stack.pop()  # a "##" closes any open "##", "###", ... before it
            stack.append((level, title))
            headings.append(Heading(pos, level, " > ".join(t for _, t in stack)))
        pos += len(line) + 1  # +1 for the "\n" removed by split
    return headings


def section_path_at(headings: list[Heading], char_pos: int) -> str:
    """Heading trail in force at a character position ('' before the first heading)."""
    i = bisect.bisect_right([h.char_pos for h in headings], char_pos) - 1
    return headings[i].path if i >= 0 else ""


def page_at(page_starts: list[int], char_pos: int, source_type: str) -> int | None:
    """PDF page number (1-based) containing a character position; None for markdown."""
    if source_type != "pdf":
        return None
    return bisect.bisect_right(page_starts, char_pos)


# ---------------------------------------------------------------------------
# Strategies -> token spans
# ---------------------------------------------------------------------------

def fixed_spans(offsets: list[tuple[int, int]], size: int, overlap: int) -> list[tuple[int, int, int]]:
    """Fixed strategy: one sliding window over the whole document. Each chunk is named by its start."""
    return [(a, b, a) for a, b in window_spans(offsets, 0, len(offsets), size, overlap)]


def heading_spans(offsets: list[tuple[int, int]], headings: list[Heading],
                  size: int, overlap: int, min_tokens: int) -> list[tuple[int, int, int]]:
    """Heading strategy: one span per section, merging tiny sections, splitting big ones.

    Returns (start_token, end_token, label_token); the section path at label_token names the chunk.
    """
    token_starts = [s for s, _ in offsets]
    # Section boundaries as token indices: document start + each heading.
    bounds = sorted({0, *(bisect.bisect_left(token_starts, h.char_pos) for h in headings)})
    bounds.append(len(offsets))
    sections = [(a, b) for a, b in zip(bounds, bounds[1:]) if b > a]

    # (start, end, label): label = first token of the section that gives the chunk its name.
    merged: list[tuple[int, int, int]] = []
    pending_start: int | None = None  # start of tiny sections waiting to be merged forward
    for i, (a, b) in enumerate(sections):
        start = a if pending_start is None else pending_start
        is_last = i == len(sections) - 1
        if b - start < min_tokens:
            if not is_last:
                pending_start = start  # too small: carry it into the next section
                continue
            if merged:
                prev_start, _, prev_label = merged[-1]
                merged[-1] = (prev_start, b, prev_label)  # tiny last section: attach to previous
                break
        merged.append((start, b, a))  # named after the section it was merged INTO (starts at a)
        pending_start = None

    spans: list[tuple[int, int, int]] = []
    for start, end, label in merged:
        if end - start <= size:
            spans.append((start, end, label))
        else:  # long section: windows; the first keeps the label, the rest are named by position
            windows = window_spans(offsets, start, end, size, overlap)
            spans.extend((a, b, label if j == 0 else a) for j, (a, b) in enumerate(windows))
    return spans


# ---------------------------------------------------------------------------
# Chunk records
# ---------------------------------------------------------------------------

def strategy_key(chunking_cfg: dict[str, Any]) -> str:
    """Short name for a chunking setup, used in chunk ids and file names: 'fixed-500-50'."""
    c = chunking_cfg
    key = f"{c['strategy']}-{c['chunk_size']}-{c['chunk_overlap']}"
    return key + (f"-min{c['min_section_tokens']}" if c["strategy"] == "heading" else "")


def chunk_document(doc: dict[str, Any], chunking_cfg: dict[str, Any], tokenizer) -> list[dict[str, Any]]:
    """Split one document into chunk records with the full metadata."""
    text, page_starts = document_text(doc)
    offsets = token_offsets(text, tokenizer)
    if not offsets:
        return []
    headings = find_headings(text) if doc["source_type"] == "markdown" else []
    size, overlap = chunking_cfg["chunk_size"], chunking_cfg["chunk_overlap"]

    if chunking_cfg["strategy"] == "heading" and headings:
        spans = heading_spans(offsets, headings, size, overlap, chunking_cfg["min_section_tokens"])
    else:  # fixed strategy, or a heading-less doc (all PDFs) under the heading strategy
        spans = fixed_spans(offsets, size, overlap)

    key = strategy_key(chunking_cfg)
    chunks = []
    for a, b, label in spans:
        char_start, char_end = offsets[a][0], offsets[b - 1][1]
        chunk_text = text[char_start:char_end].strip()
        if not re.search(r"\w", chunk_text):
            continue  # nothing but punctuation / whitespace
        chunks.append({
            "chunk_id": f"{doc['doc_id']}::{key}::{len(chunks)}",
            "doc_id": doc["doc_id"],
            "doc_title": doc["doc_title"],
            "version_group": doc["version_group"],
            "is_current": doc["is_current"],
            "version_status": doc["version_status"],
            "source_type": doc["source_type"],
            "source_path": doc["source_path"],
            "section_path": section_path_at(headings, offsets[label][0]),
            "page": page_at(page_starts, char_start, doc["source_type"]),
            "updated_date": doc["updated_date"],
            "department": doc["department"],
            "access_roles": doc["access_roles"],
            "content_hash": hashlib.sha256(chunk_text.encode("utf-8")).hexdigest(),
            "chunk_strategy": key,
            "text": chunk_text,
            # Extra fields beyond the spec:
            "chunk_index": len(chunks),
            "token_count": b - a,
            "char_start": char_start,  # position in the joined document text, so evaluation can
            "char_end": char_end,      # match chunks to gold evidence under ANY chunking strategy
        })
    return chunks


def index_text(chunk: dict[str, Any], add_prefix: bool) -> str:
    """The text that gets embedded and BM25-indexed.

    With add_prefix, "Doc title > Section > Subsection" goes in front, so a chunk that just says
    "The limit is $75" also carries *what* the limit is about. The chunk's own `text` stays
    clean for display and for the LLM.
    """
    if not add_prefix:
        return chunk["text"]
    trail = " > ".join(part for part in (chunk["doc_title"], chunk["section_path"]) if part)
    return f"{trail}\n\n{chunk['text']}"


# ---------------------------------------------------------------------------
# Truncation
# ---------------------------------------------------------------------------

def truncation_stats(token_counts: list[int], max_tokens: int) -> dict[str, float]:
    """How much chunk text an embedding model with a `max_tokens` input limit never sees.

    token_counts are per-chunk counts WITHOUT special tokens; the model spends SPECIAL_TOKENS
    of its limit on [CLS] and [SEP].
    """
    usable = max_tokens - SPECIAL_TOKENS
    over = [n for n in token_counts if n > usable]
    total = sum(token_counts)
    return {
        "usable_tokens": usable,
        "chunks_truncated_pct": 100 * len(over) / len(token_counts) if token_counts else 0.0,
        "tokens_unseen_pct": 100 * sum(n - usable for n in over) / total if total else 0.0,
    }


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def chunk_all(docs: list[dict[str, Any]], chunking_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Chunk every document."""
    tokenizer = get_tokenizer(chunking_cfg["tokenizer"])
    return [chunk for doc in docs for chunk in chunk_document(doc, chunking_cfg, tokenizer)]


def write_chunks(chunks: list[dict[str, Any]], path: Path) -> None:
    """Write chunks as JSON lines."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def load_chunks(path: Path) -> list[dict[str, Any]]:
    """Read a chunks .jsonl file."""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def chunk_source_key(cfg: dict[str, Any], documents_path: Path) -> dict[str, Any]:
    """What a chunk file was built from: the documents file's hash, the chunking settings, the code version."""
    digest = hashlib.sha256(documents_path.read_bytes()).hexdigest()
    # Only settings that change chunk CONTENT (the prefix is applied later, at embedding time).
    content_settings = {k: cfg["chunking"][k] for k in
                        ("strategy", "chunk_size", "chunk_overlap", "min_section_tokens", "tokenizer")}
    return {"documents_sha256": digest, "chunking": content_settings, "chunker_version": CHUNKER_VERSION}


def chunks_are_current(path: Path, key: dict[str, Any]) -> bool:
    """True if the chunk file exists and was built from exactly these inputs (its .meta.json matches)."""
    meta = path.with_suffix(".meta.json")
    return path.exists() and meta.exists() and json.loads(meta.read_text()) == key


def write_chunks_with_meta(chunks: list[dict[str, Any]], path: Path, key: dict[str, Any]) -> None:
    write_chunks(chunks, path)
    path.with_suffix(".meta.json").write_text(json.dumps(key, indent=1, sort_keys=True))


def chunks_path(cfg: dict[str, Any]) -> Path:
    """Where the chunks for this config live: data/processed/chunks/<strategy_key>.jsonl."""
    return resolve_path(cfg["paths"]["processed_dir"]) / "chunks" / f"{strategy_key(cfg['chunking'])}.jsonl"


def print_stats(chunks: list[dict[str, Any]], cfg: dict[str, Any]) -> None:
    """Chunk counts, size distribution and how much text the embedding model would miss."""
    tokenizer = get_tokenizer(cfg["chunking"]["tokenizer"])
    add_prefix = cfg["chunking"]["add_prefix"]
    counts = sorted(count_tokens(index_text(c, add_prefix), tokenizer) for c in chunks)
    by_type: dict[str, int] = {}
    for c in chunks:
        by_type[c["source_type"]] = by_type.get(c["source_type"], 0) + 1

    print(f"Chunks: {len(chunks)} from {len({c['doc_id'] for c in chunks})} documents  {by_type}")
    print(f"Tokens per chunk{' (incl. prefix)' if add_prefix else ''}: min {counts[0]}, "
          f"median {statistics.median(counts):.0f}, p95 {counts[int(0.95 * (len(counts) - 1))]}, max {counts[-1]}")

    model = cfg["embedding"]["model"]
    limit = EMBEDDING_MAX_TOKENS.get(model)
    if limit is None:
        print(f"Truncation: unknown input limit for {model}; add it to EMBEDDING_MAX_TOKENS")
        return
    t = truncation_stats(counts, limit)
    print(f"Truncation for {model} (reads {limit} tokens = {t['usable_tokens']} text + 2 special):")
    print(f"  {t['chunks_truncated_pct']:.1f}% of chunks are cut off; "
          f"{t['tokens_unseen_pct']:.1f}% of all chunk tokens are never embedded")


def main() -> None:
    parser = argparse.ArgumentParser(description="Chunk data/processed/documents.jsonl")
    parser.add_argument("config", nargs="?", default="configs/baseline.yaml")
    args = parser.parse_args()

    cfg = load_config(args.config)
    processed = resolve_path(cfg["paths"]["processed_dir"])
    docs = load_documents(processed)
    chunks = chunk_all(docs, cfg["chunking"])
    out = chunks_path(cfg)
    write_chunks_with_meta(chunks, out, chunk_source_key(cfg, processed / "documents.jsonl"))
    print(f"Wrote {out.relative_to(resolve_path('.'))}")
    print_stats(chunks, cfg)


if __name__ == "__main__":
    main()
