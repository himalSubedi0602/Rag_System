"""Build and validate the test set from eval/questions_source.yaml.

Run:  python -m src.testset
  - checks every evidence quote really appears in its gold document (and in one baseline chunk)
  - checks non-outdated quotes don't ALSO appear in other documents (that would make gold ambiguous)
  - checks no_answer topics are truly absent and records the closest BM25 hits as proof
  - assigns a stratified tune/test split with a fixed seed
  - writes eval/questions.jsonl, eval/gold_review.md and eval/questions_review.md
Exits with an error listing every problem, and writes nothing, if any check fails.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

from src.chunking import chunks_path, load_chunks
from src.config import load_config, resolve_path
from src.index import BM25Index
from src.ingest import load_documents

SOURCE_PATH = "eval/questions_source.yaml"
EXPECTED_COUNTS = {"lookup": 20, "paraphrase": 15, "exact_term": 10, "multi_doc": 10,
                   "outdated_version": 15, "no_answer": 10}
TEST_SIZE = 25
SPLIT_SEED = 42


# ---------------------------------------------------------------------------
# Matching quotes
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    """Make quote matching robust to formatting: case, whitespace, curly quotes, markdown marks."""
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"[*_`]", "", text)          # markdown bold/italic/code marks
    return re.sub(r"\s+", " ", text).strip().lower()


def doc_text(doc: dict[str, Any]) -> str:
    """All of a document's pages as one string."""
    return "\n".join(page["text"] for page in doc["pages"])


# ---------------------------------------------------------------------------
# Split
# ---------------------------------------------------------------------------

def stratified_split(questions: list[dict[str, Any]], test_size: int, seed: int) -> dict[str, str]:
    """Assign 'tune' / 'test' so each question type is represented proportionally in test.

    Each type gets round(n * test_size / total) test questions; any rounding remainder is
    fixed by adjusting the largest types. Returns {question_id: split}.
    """
    by_type: dict[str, list[str]] = defaultdict(list)
    for q in questions:
        by_type[q["type"]].append(q["id"])
    total = len(questions)
    quota = {t: round(len(ids) * test_size / total) for t, ids in by_type.items()}
    largest_first = sorted(by_type, key=lambda t: -len(by_type[t]))
    i = 0
    while sum(quota.values()) != test_size:  # fix rounding so the total is exact
        t = largest_first[i % len(largest_first)]
        quota[t] += 1 if sum(quota.values()) < test_size else -1
        i += 1

    rng = random.Random(seed)
    split = {}
    for t in sorted(by_type):              # sorted -> same result on every run
        ids = sorted(by_type[t])
        test_ids = set(rng.sample(ids, quota[t]))
        split.update({qid: "test" if qid in test_ids else "tune" for qid in ids})
    return split


# ---------------------------------------------------------------------------
# Validation + building
# ---------------------------------------------------------------------------

def check_structure(source: dict[str, Any]) -> list[str]:
    """Ids unique, required fields present, counts per type as specified."""
    errors = []
    questions = source["questions"]
    dupes = [qid for qid, n in Counter(q["id"] for q in questions).items() if n > 1]
    if dupes:
        errors.append(f"duplicate ids: {dupes}")
    counts = Counter(q["type"] for q in questions)
    if dict(counts) != EXPECTED_COUNTS:
        errors.append(f"type counts {dict(counts)} != expected {EXPECTED_COUNTS}")
    for q in questions:
        if q["type"] == "no_answer":
            if not q.get("absent"):
                errors.append(f"{q['id']}: no_answer question needs 'absent' checks")
        elif not q.get("evidence") or not q.get("answer"):
            errors.append(f"{q['id']}: needs 'evidence' and 'answer'")
        if q["type"] == "multi_doc" and len({e["doc"] for e in q.get("evidence", [])}) < 2:
            errors.append(f"{q['id']}: multi_doc needs evidence from at least 2 documents")
    return errors


def build(source: dict[str, Any], docs: list[dict[str, Any]], chunks: list[dict[str, Any]]
          ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Validate every question against the corpus. Returns (questions, review_rows, errors)."""
    errors = check_structure(source)
    docs_by_id = {d["doc_id"]: d for d in docs}
    norm_docs = {d["doc_id"]: normalize(doc_text(d)) for d in docs}
    raw_docs = {d["doc_id"]: doc_text(d) for d in docs}
    chunks_by_doc: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for c in chunks:
        chunks_by_doc[c["doc_id"]].append(c)
    groups: dict[str, list[str]] = defaultdict(list)
    for d in docs:
        groups[d["version_group"]].append(d["doc_id"])
    bm25 = BM25Index(chunks, add_prefix=True)

    split = stratified_split(source["questions"], TEST_SIZE, SPLIT_SEED)
    built, review = [], []
    for q in source["questions"]:
        qid, qtype = q["id"], q["type"]
        row = {"id": qid, "type": qtype, "split": split[qid], "question": q["question"],
               "answer": q.get("answer", source["no_answer_text"]), "evidence": [], "notes": []}
        gold_docs, gold_chunks, outdated_docs = [], [], []

        for ev in q.get("evidence", []):
            doc_id, quote = ev["doc"], normalize(ev["quote"])
            if doc_id not in docs_by_id:
                errors.append(f"{qid}: unknown doc {doc_id}")
                continue
            if quote not in norm_docs[doc_id]:
                errors.append(f"{qid}: quote not found in {doc_id}: {ev['quote']!r}")
                continue
            hits = [c["chunk_id"] for c in chunks_by_doc[doc_id] if quote in normalize(c["text"])]
            if not hits:
                errors.append(f"{qid}: quote is split across chunks in {doc_id} (shorten it): {ev['quote']!r}")
            if not docs_by_id[doc_id]["is_current"]:
                errors.append(f"{qid}: gold doc {doc_id} is not the current version")

            # Same quote elsewhere? Expected only for outdated_version (real old copies).
            elsewhere = [d for d, text in norm_docs.items() if d != doc_id and quote in text]
            old_versions = [d for d in groups[docs_by_id[doc_id]["version_group"]]
                            if d != doc_id and not docs_by_id[d]["is_current"]]
            if qtype == "outdated_version":
                if not old_versions:
                    errors.append(f"{qid}: gold doc {doc_id} has no outdated version in its version group")
                outdated_docs += old_versions
                same = [d for d in old_versions if d in elsewhere]
                changed = [d for d in old_versions if d not in elsewhere]
                if same:
                    row["notes"].append(f"same text in old version(s): {', '.join(same)}")
                if changed:
                    row["notes"].append(f"fact differs in old version(s): {', '.join(changed)}")
            elif elsewhere:
                errors.append(f"{qid}: quote also appears in {elsewhere}; gold would be ambiguous")

            gold_docs.append(doc_id)
            gold_chunks += hits
            row["evidence"].append({"doc": doc_id, "quote": ev["quote"], "chunks": hits,
                                    "in_text": find_original(raw_docs[doc_id], ev["quote"])})

        for check in q.get("absent", []):
            pattern = re.compile(check["pattern"], re.IGNORECASE)
            found = [d for d, text in raw_docs.items() if d.startswith(check["scope"]) and pattern.search(text)]
            if found:
                errors.append(f"{qid}: '{check['pattern']}' found in {found[:5]} (topic is covered)")
            scope = check["scope"] or "whole corpus"
            row["notes"].append(f"/{check['pattern']}/ in {scope}: 0 matches")
        if qtype == "no_answer":
            top = bm25.search(q["question"], k=3)
            row["notes"].append("closest BM25 hits (not answers): " +
                                "; ".join(f"{cid.split('::')[0]} ({score:.1f})" for cid, score in top))

        built.append({
            "id": qid, "question": q["question"], "question_type": qtype,
            "gold_doc_ids": sorted(set(gold_docs)), "gold_chunk_ids": sorted(set(gold_chunks)),
            "expected_answer": row["answer"], "split": split[qid],
            "gold_evidence": [{"doc_id": e["doc"], "quote": e["quote"]} for e in q.get("evidence", [])],
            "outdated_doc_ids": sorted(set(outdated_docs)),
        })
        review.append(row)
    return built, review, errors


def find_original(text: str, quote: str) -> bool:
    """True if the quote appears verbatim (before normalization). Only informational."""
    return quote in text


# ---------------------------------------------------------------------------
# Output files
# ---------------------------------------------------------------------------

def md_cell(text: str) -> str:
    """Make text safe inside a markdown table cell."""
    return str(text).replace("|", "\\|").replace("\n", " ")


def write_questions_review(review: list[dict[str, Any]], path: Path) -> None:
    """One readable table with every question, for approval."""
    lines = ["# Test set for review", "",
             f"{len(review)} questions: " + ", ".join(f"{t} {n}" for t, n in Counter(r['type'] for r in review).items()),
             f"Split: tune {sum(r['split'] == 'tune' for r in review)}, test {sum(r['split'] == 'test' for r in review)}", "",
             "| ID | Type | Split | Question | Expected answer | Gold document(s) |",
             "|---|---|---|---|---|---|"]
    for r in review:
        docs = "<br>".join(e["doc"] for e in r["evidence"]) or "(none: should decline)"
        lines.append(f"| {r['id']} | {r['type']} | {r['split']} | {md_cell(r['question'])} | "
                     f"{md_cell(r['answer'])} | {md_cell(docs)} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_gold_review(review: list[dict[str, Any]], path: Path) -> None:
    """Supporting quote, gold chunk ids and checks for every question."""
    lines = ["# Gold evidence review", "",
             "Every quote below was checked automatically against the ingested corpus by `python -m src.testset`.", ""]
    for r in review:
        lines += [f"## {r['id']} ({r['type']}, {r['split']})", "", f"**Q:** {r['question']}", "",
                  f"**Expected:** {r['answer']}", ""]
        for e in r["evidence"]:
            lines += [f"- `{e['doc']}`", f"  > {e['quote']}", f"  - gold chunks: {', '.join(e['chunks'])}"]
        for note in r["notes"]:
            lines.append(f"- {note}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", default="configs/baseline.yaml", help="whose chunks define gold_chunk_ids")
    args = parser.parse_args()

    cfg = load_config(args.config)
    source = yaml.safe_load(open(resolve_path(SOURCE_PATH), encoding="utf-8"))
    docs = load_documents(resolve_path(cfg["paths"]["processed_dir"]))
    chunks = load_chunks(chunks_path(cfg))
    questions, review, errors = build(source, docs, chunks)

    if errors:
        print(f"{len(errors)} problem(s); nothing written:")
        for e in errors:
            print("  -", e)
        sys.exit(1)

    eval_dir = resolve_path("eval")
    with open(eval_dir / "questions.jsonl", "w", encoding="utf-8") as f:
        for q in questions:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")
    write_questions_review(review, eval_dir / "questions_review.md")
    write_gold_review(review, eval_dir / "gold_review.md")

    print(f"OK: {len(questions)} questions validated against {len(docs)} documents / {len(chunks)} chunks")
    print("By type:  ", dict(Counter(q["question_type"] for q in questions)))
    print("By split: ", dict(Counter(q["split"] for q in questions)))
    test_by_type = Counter(q["question_type"] for q in questions if q["split"] == "test")
    print("Test split by type:", dict(test_by_type))
    print("Wrote eval/questions.jsonl, eval/questions_review.md, eval/gold_review.md")


if __name__ == "__main__":
    main()
