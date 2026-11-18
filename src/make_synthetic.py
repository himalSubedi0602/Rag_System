"""Generate minimal-edit outdated versions from data/synthetic/changes.yaml.

Each old version is a FULL copy of the current page's extracted text with only the listed
facts changed and an earlier date, so it looks as relevant to search as the real page;
which version wins then depends only on how versions are handled.

Run:  python -m src.make_synthetic      (after ingestion; then run ingestion again)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.config import load_config, resolve_path
from src.ingest import load_documents


def apply_changes(text: str, replacements: list[list[str]]) -> str:
    """Apply each [current, old] replacement; every current text must be present."""
    for current, old in replacements:
        if current not in text:
            raise ValueError(f"text to change not found: {current!r}")
        text = text.replace(current, old)
    return text


def render(spec: dict[str, Any], source_doc: dict[str, Any], body: str) -> str:
    """Front matter that clearly marks the file as synthetic, followed by the edited page."""
    changes = "".join(f"#   {cur!r} -> {old!r}\n" for cur, old in spec["replace"])
    return (
        "---\n"
        f"title: {yaml.safe_dump(source_doc['doc_title']).strip().removesuffix('...').strip()}\n"
        f"version_group: \"{source_doc['version_group']}\"\n"
        "is_current: false\n"
        "synthetic_old_version: true\n"
        f"updated_date: \"{spec['date']}\"\n"
        f"department: \"{source_doc['department']}\"\n"
        "# SYNTHETIC OLD VERSION for evaluation. Full copy of GitLab handbook page\n"
        f"# {spec['source']} (CC BY-SA 4.0) with ONLY these facts changed:\n"
        f"{changes}"
        "---\n\n" + body.strip() + "\n"
    )


def main() -> None:
    cfg = load_config("configs/default.yaml")
    out_dir = resolve_path(cfg["paths"]["synthetic_dir"])
    specs = yaml.safe_load(open(out_dir / "changes.yaml", encoding="utf-8"))
    docs = {d["doc_id"]: d for d in load_documents(resolve_path(cfg["paths"]["processed_dir"]))}

    expected = {f"{s['file']}.md" for s in specs}
    for old_file in out_dir.glob("*.md"):  # remove files no longer listed (e.g. old excerpt versions)
        if old_file.name not in expected and old_file.name != "README.md":
            old_file.unlink()
            print(f"removed {old_file.name}")

    for spec in specs:
        source_doc = docs[spec["source"]]
        text = "\n".join(page["text"] for page in source_doc["pages"])
        body = apply_changes(text, spec["replace"])
        Path(out_dir / f"{spec['file']}.md").write_text(render(spec, source_doc, body), encoding="utf-8")
        print(f"{spec['file']}.md: full copy of {spec['source']} ({len(body)} chars), "
              f"{len(spec['replace'])} change(s)")


if __name__ == "__main__":
    main()
