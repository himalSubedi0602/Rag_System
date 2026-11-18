"""Print sample extracted documents so extraction quality can be spot-checked by eye.

Examples:
  python -m src.inspect_docs                       5 random docs (fixed seed)
  python -m src.inspect_docs --n 3 --type pdf      3 random PDFs
  python -m src.inspect_docs --doc-id hb:finance/expenses
  python -m src.inspect_docs --versions            list every multi-version group
"""

from __future__ import annotations

import argparse
import random
from collections import defaultdict
from typing import Any

from src.config import load_config, resolve_path
from src.ingest import load_documents

META_FIELDS = ("doc_id", "doc_title", "source_type", "source_path", "department", "access_roles",
               "updated_date", "version_group", "version_number", "is_current")


def show_document(doc: dict[str, Any], chars: int, max_pages: int) -> None:
    """Print a document's metadata and the start of its first few pages."""
    print("=" * 80)
    for field in META_FIELDS:
        print(f"{field:>15}: {doc[field]}")
    total = sum(len(p["text"]) for p in doc["pages"])
    print(f"{'pages / chars':>15}: {len(doc['pages'])} / {total}")
    for page in doc["pages"][:max_pages]:
        label = f"page {page['page']}" if page["page"] else "text"
        print(f"--- {label} (first {chars} chars) ---")
        print(page["text"][:chars])
    print()


def show_versions(docs: list[dict[str, Any]]) -> None:
    """Print each version group that has more than one document, current version marked."""
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for d in docs:
        groups[d["version_group"]].append(d)
    for group, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        print(group)
        for d in sorted(members, key=lambda d: (d["version_number"] or 999, d["updated_date"] or "")):
            mark = "CURRENT" if d["is_current"] else "old    "
            print(f"   {mark}  {d['updated_date']}  {d['doc_id']}  ({d['doc_title']})")
    solo_old = [d for d in docs if not d["is_current"] and len(groups[d["version_group"]]) == 1]
    print(f"\nSingle documents marked not current (legacy/deprecated, no newer copy): {len(solo_old)}")
    for d in solo_old:
        print(f"   {d['doc_id']}  ({d['doc_title']})")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--n", type=int, default=5, help="number of random documents")
    parser.add_argument("--type", choices=["markdown", "pdf"], help="only this source type")
    parser.add_argument("--doc-id", help="show one specific document")
    parser.add_argument("--chars", type=int, default=700, help="characters to print per page")
    parser.add_argument("--pages", type=int, default=2, help="pages to print per document")
    parser.add_argument("--seed", type=int, default=0, help="change to see different samples")
    parser.add_argument("--versions", action="store_true", help="list version groups instead")
    parser.add_argument("--config", default="configs/default.yaml")
    args = parser.parse_args()

    docs = load_documents(resolve_path(load_config(args.config)["paths"]["processed_dir"]))

    if args.versions:
        show_versions(docs)
        return
    if args.doc_id:
        selected = [d for d in docs if d["doc_id"] == args.doc_id]
        if not selected:
            print(f"No document with doc_id {args.doc_id!r}")
            return
    else:
        pool = [d for d in docs if args.type in (None, d["source_type"])]
        selected = random.Random(args.seed).sample(pool, min(args.n, len(pool)))

    for doc in selected:
        show_document(doc, args.chars, args.pages)


if __name__ == "__main__":
    main()
