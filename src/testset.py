"""Build and validate the test set from eval/questions_source.yaml.

Run:  python -m src.testset
  - checks every evidence quote really appears in its gold document (and in one baseline chunk)
  - a quote may also appear in OTHER VERSIONS of the same page (they become acceptable_doc_ids,
    since retrieving them still gives the right answer); anywhere else it would make gold ambiguous
  - outdated_version: the quote must contain the changed fact, i.e. appear in NO old version
  - history: the gold doc is an old version and the quote must not appear in the current one
  - real_pair: like outdated_version, but the old versions are REAL documents; `old_evidence` gives the
    old wording, which must appear in every real old version that lacks the current quote
  - a normal question's quote must not be altered in a synthetic old copy (that would silently turn it
    into an outdated-version test)
  - checks no_answer topics are truly absent and records the closest BM25 hits as proof
  - keeps every frozen split; new questions get a stratified split (fixed seed)
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
CHANGES_PATH = "data/synthetic/changes.yaml"
EXPECTED_COUNTS = {"lookup": 50, "paraphrase": 35, "exact_term": 10, "multi_doc": 18, "compound": 7,
                   "outdated_version": 39, "real_pair": 2, "history": 12, "no_answer": 25}
TEST_SHARE = 25 / 80          # share of NEW questions that go to test (same as the original split)
MIN_OUTDATED_TUNE = 20        # enough outdated questions to measure stale rate while tuning
MIN_OUTDATED_TEST = 12        # ... and for the one final test run
SPLIT_SEED = 42


# ---------------------------------------------------------------------------
# Matching quotes
# ---------------------------------------------------------------------------

def normalize(text: str) -> str:
    """Make quote matching robust to formatting: case, whitespace, curly quotes, markdown marks."""
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    text = re.sub(r"[*_`]", "", text)          # markdown bold/italic/code marks
    return re.sub(r"\s+", " ", text).strip().lower()


STOPWORDS = set("""a an the and or but if then than of to in on at by for from with without into onto over under
about as is are was were be been being am do does did done have has had having i me my mine we us our you your he
she it its they them their this that these those there here what which who whom whose when where why how can could
may might must shall should will would not no yes any all each every some such more most much many few other own
same so too very just also only per get got go going want need make made let lets im ive id dont isnt arent cant
""".split())
MAX_PARAPHRASE_OVERLAP = 0.40


def content_words(text: str, ignore: set[str] = frozenset()) -> list[str]:
    """Lower-case words that carry meaning: no stopwords, no words from `ignore`, crude plural stripping."""
    out = []
    for w in re.findall(r"[a-z0-9$£%]+", normalize(text)):
        w = w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w
        if w not in STOPWORDS and w not in ignore and len(w) > 1:
            out.append(w)
    return out


def word_overlap(question: str, quote: str, title: str) -> float:
    """Share of the question's content words that also appear in the gold quote. Words from the document
    title (e.g. the organisation name, which PDF questions must include) are not counted."""
    ignore = set(content_words(title)) | {"gitlab"}
    q_words = content_words(question, ignore)
    quote_words = set(content_words(quote))
    return sum(w in quote_words for w in q_words) / len(q_words) if q_words else 0.0


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

def assign_splits(questions: list[dict[str, Any]]) -> dict[str, str]:
    """Keep every frozen split; give questions without one a stratified split of their own."""
    split = {q["id"]: q["split"] for q in questions if q.get("split")}
    new = [q for q in questions if not q.get("split")]
    if new:
        split.update(stratified_split(new, round(len(new) * TEST_SHARE), SPLIT_SEED))
    return split


def old_quote(quote: str, replacements: list[list[str]]) -> str | None:
    """Apply a synthetic file's [current, old] replacements to a (current) quote, on normalized text.
    Returns the outdated wording of the quote, or None if none of the changes touch it."""
    text = normalize(quote)
    for current, old in replacements:
        cur, new = normalize(current).strip("| "), normalize(old).strip("| ")  # table pipes vary
        if cur in text:
            text = text.replace(cur, new)
    return None if text == normalize(quote) else text


def check_structure(source: dict[str, Any]) -> list[str]:
    """Ids unique, required fields present, counts per type as specified."""
    errors = []
    questions = source["questions"]
    dupes = [qid for qid, n in Counter(q["id"] for q in questions).items() if n > 1]
    if dupes:
        errors.append(f"duplicate ids: {dupes}")
    counts = Counter(q["type"] for q in questions)
    if EXPECTED_COUNTS and dict(counts) != EXPECTED_COUNTS:
        errors.append(f"type counts {dict(counts)} != expected {EXPECTED_COUNTS}")
    bad = [q["id"] for q in questions if q.get("split") not in (None, "tune", "test")]
    if bad:
        errors.append(f"invalid split values: {bad}")
    for q in questions:
        if q["type"] == "no_answer":
            if not q.get("absent"):
                errors.append(f"{q['id']}: no_answer question needs 'absent' checks")
        elif not q.get("evidence") or not q.get("answer"):
            errors.append(f"{q['id']}: needs 'evidence' and 'answer'")
        if q["type"] in ("multi_doc", "compound") and len({e["doc"] for e in q.get("evidence", [])}) < 2:
            errors.append(f"{q['id']}: {q['type']} needs evidence from at least 2 documents")
    return errors


def build(source: dict[str, Any], docs: list[dict[str, Any]], chunks: list[dict[str, Any]],
          changes: dict[str, list[list[str]]] | None = None
          ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    """Validate every question against the corpus. Returns (questions, review_rows, errors).

    `changes` maps a synthetic doc_id to its [current, old] replacements (from changes.yaml); it is
    used to work out what each outdated_version quote says in the old version (outdated_evidence).
    """
    changes = changes or {}
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

    split = assign_splits(source["questions"])
    outdated_tune = sum(1 for q in source["questions"]
                        if q["type"] == "outdated_version" and split[q["id"]] == "tune")
    outdated_test = sum(1 for q in source["questions"]
                        if q["type"] == "outdated_version" and split[q["id"]] == "test")
    if EXPECTED_COUNTS and outdated_tune < MIN_OUTDATED_TUNE:
        errors.append(f"only {outdated_tune} outdated_version questions in tune (need {MIN_OUTDATED_TUNE})")
    if EXPECTED_COUNTS and outdated_test < MIN_OUTDATED_TEST:
        errors.append(f"only {outdated_test} outdated_version questions in test (need {MIN_OUTDATED_TEST})")
    built, review = [], []
    for q in source["questions"]:
        qid, qtype = q["id"], q["type"]
        row = {"id": qid, "type": qtype, "split": split[qid], "question": q["question"],
               "answer": q.get("answer", source["no_answer_text"]), "evidence": [], "notes": [],
               "style": q.get("style", "direct"), "overlap": None}
        gold_docs, gold_chunks, outdated_docs, acceptable, outdated_evidence = [], [], [], [], []

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
            is_current = docs_by_id[doc_id]["is_current"]
            if qtype == "history" and is_current:
                errors.append(f"{qid}: history question must point at an OLD version, not {doc_id}")
            if qtype != "history" and not is_current:
                errors.append(f"{qid}: gold doc {doc_id} is not the current version")

            elsewhere = [d for d, text in norm_docs.items() if d != doc_id and quote in text]
            siblings = [d for d in groups[docs_by_id[doc_id]["version_group"]] if d != doc_id]
            unrelated = [d for d in elsewhere if d not in siblings]
            if unrelated:
                errors.append(f"{qid}: quote also appears in unrelated docs {unrelated}; gold would be ambiguous")
            if qtype == "outdated_version":
                old_versions = [d for d in siblings if docs_by_id[d]["version_status"] == "superseded"]
                if not old_versions:
                    errors.append(f"{qid}: gold doc {doc_id} has no superseded version in its version group")
                same = [d for d in old_versions if d in elsewhere]
                if same:
                    errors.append(f"{qid}: quote also appears in old version(s) {same}; it must contain the changed fact")
                outdated_docs += old_versions
                for old_doc in old_versions:
                    old = old_quote(ev["quote"], changes.get(old_doc, []))
                    if old is None or old not in norm_docs[old_doc]:
                        errors.append(f"{qid}: can't find the outdated wording of the quote in {old_doc}")
                        continue
                    outdated_evidence.append({"doc_id": old_doc, "quote": old})
                    row["notes"].append(f"old version {old_doc} says: \"{old}\"")
            elif qtype == "real_pair":
                old_versions = [d for d in siblings if docs_by_id[d]["version_status"] == "superseded"
                                and d not in elsewhere]          # real old versions WITHOUT the current wording
                acceptable += [d for d in siblings if d in elsewhere]
                if not old_versions:
                    errors.append(f"{qid}: no real old version states a different fact")
                for old_doc in (old_versions if q.get("stale_level", "fact") == "fact" else []):
                    olds = [normalize(o["quote"]) for o in q.get("old_evidence", []) if normalize(o["quote"]) in norm_docs[old_doc]]
                    if not olds:
                        errors.append(f"{qid}: old_evidence not found in old version {old_doc}")
                        continue
                    outdated_evidence.append({"doc_id": old_doc, "quote": olds[0]})
                outdated_docs += old_versions
                row["notes"].append(f"real old version(s) with the old rule: {', '.join(old_versions)}")
            elif qtype == "history":
                current = [d for d in siblings if docs_by_id[d]["is_current"]]
                if any(d in elsewhere for d in current):
                    errors.append(f"{qid}: history quote also appears in the current version {current}")
                row["notes"].append(f"current version (should NOT be preferred here): {', '.join(current)}")
            else:
                same = [d for d in elsewhere if d in siblings]
                acceptable += same
                altered = [d for d in siblings if d.startswith("syn:") and d not in elsewhere]
                if altered:
                    errors.append(f"{qid}: a synthetic change alters this quote in {altered}; "
                                  "make it an outdated_version question or pick another quote")
                if same:
                    row["notes"].append(f"same answer in other version(s), acceptable: {', '.join(same)}")

            overlap = word_overlap(q["question"], ev["quote"], docs_by_id[doc_id]["doc_title"])
            row["overlap"] = overlap if row["overlap"] is None else max(row["overlap"], overlap)
            if qtype == "paraphrase" and overlap > MAX_PARAPHRASE_OVERLAP:
                errors.append(f"{qid}: paraphrase shares {overlap:.0%} of its content words with the quote "
                              f"(max {MAX_PARAPHRASE_OVERLAP:.0%}); reword it")
            gold_docs.append(doc_id)
            gold_chunks += hits
            item_acceptable = ([d for d in elsewhere if d in siblings]
                               if qtype not in ("outdated_version", "history") else [])
            row["evidence"].append({"doc": doc_id, "quote": ev["quote"], "chunks": hits,
                                    "acceptable": item_acceptable})

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
            "gold_evidence": [{"doc_id": e["doc"], "quote": e["quote"], "acceptable_doc_ids": e["acceptable"]}
                              for e in row["evidence"]],
            "outdated_doc_ids": sorted(set(outdated_docs)),
            "acceptable_doc_ids": sorted(set(acceptable) - set(gold_docs)),
            "outdated_evidence": outdated_evidence,
            "stale_level": q.get("stale_level", "fact") if qtype in ("outdated_version", "real_pair") else None,
            "style": row["style"],
            "word_overlap": None if row["overlap"] is None else round(row["overlap"], 3),
            "doc_group": doc_group(gold_docs),
        })
        review.append(row)
    errors += quote_reuse_errors(source["questions"])
    assign_clusters(built, fact_reuse_pairs(source["questions"]))
    return built, review, errors


def same_chunk_pairs(built: list[dict[str, Any]]) -> list[tuple[str, str]]:
    """Pairs of questions whose gold quotes fall in the same baseline chunk (so their retrieval outcomes
    are tied: whatever ranks that chunk well helps both)."""
    by_chunk: dict[str, list[str]] = defaultdict(list)
    for q in built:
        for cid in set(q["gold_chunk_ids"]):
            by_chunk[cid].append(q["id"])
    return sorted({(a, b) for ids in by_chunk.values() for i, a in enumerate(sorted(ids)) for b in sorted(ids)[i + 1:]})


def assign_clusters(built: list[dict[str, Any]], fact_pairs: list[tuple[str, str, str]]) -> dict[str, int]:
    """Group linked questions (same fact, or gold in the same baseline chunk) into clusters with a small
    union-find; writes q["cluster"] on every question. The bootstrap resamples whole clusters, so linked
    questions can't make the intervals look tighter than the evidence justifies."""
    parent = {q["id"]: q["id"] for q in built}

    def root(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving keeps the trees shallow
            x = parent[x]
        return x

    chunk_pairs = same_chunk_pairs(built)
    for a, b in [(a, b) for a, b, _ in fact_pairs] + chunk_pairs:
        parent[root(a)] = root(b)
    roots = sorted({root(q["id"]) for q in built})
    number = {r: i for i, r in enumerate(roots)}
    for q in built:
        q["cluster"] = f"c{number[root(q['id'])]:03d}"
    sizes = Counter(q["cluster"] for q in built)
    return {"fact_pairs": len(fact_pairs), "same_chunk_pairs": len(chunk_pairs), "clusters": len(roots),
            "multi_question_clusters": sum(1 for n in sizes.values() if n > 1), "largest_cluster": max(sizes.values())}


def doc_group(gold_docs: list[str]) -> str:
    """Coarse document group for reporting: 'pdf', or the handbook section (e.g. 'finance', 'security');
    'mixed' if a question's gold docs come from different groups; 'none' for no_answer."""
    groups = {"pdf" if d.startswith("pdf:") else d.split(":", 1)[1].split("/")[0] for d in gold_docs}
    return "none" if not groups else groups.pop() if len(groups) == 1 else "mixed"


FACT_WORD_SHARE = 0.6   # two quotes from one document sharing >= 60% of their content words = same fact


def same_fact(doc_a: str, quote_a: str, doc_b: str, quote_b: str) -> bool:
    """Same document AND the same stated value: one quote contains the other, or (when their numbers
    don't differ) they share most of their content words."""
    if doc_a != doc_b:
        return False
    a, b = normalize(quote_a), normalize(quote_b)
    if a in b or b in a:
        return True
    nums_a, nums_b = set(re.findall(r"\d+(?:[.,]\d+)*", a)), set(re.findall(r"\d+(?:[.,]\d+)*", b))
    if nums_a and nums_b and nums_a != nums_b:
        return False          # different stated values (e.g. "1 year" vs "90 days") = different facts
    wa, wb = set(content_words(a)), set(content_words(b))
    return bool(wa and wb) and len(wa & wb) / min(len(wa), len(wb)) >= FACT_WORD_SHARE


def fact_reuse_pairs(questions: list[dict[str, Any]]) -> list[tuple[str, str, str]]:
    """Every pair of DIFFERENT questions whose evidence states the same fact: (id_a, id_b, doc)."""
    items = [(q["id"], ev["doc"], ev["quote"]) for q in questions for ev in q.get("evidence", [])]
    pairs = set()
    for i, (qa, da, xa) in enumerate(items):
        for qb, db, xb in items[i + 1:]:
            if qa != qb and same_fact(da, xa, db, xb):
                pairs.add((min(qa, qb), max(qa, qb), da))
    return sorted(pairs)


def quote_reuse_errors(questions: list[dict[str, Any]]) -> list[str]:
    """Questions sharing a fact aren't independent samples, whatever their type. A pair is an error if
    either question is NOT in the frozen pre-expansion set (eval/replication_groups.json lists the new
    ones); pairs among the original questions are only reported, because the test split can't change."""
    groups_path = resolve_path("eval/replication_groups.json")
    new_ids = set(json.loads(groups_path.read_text())["new_60"]) if groups_path.exists() else None
    errors = []
    for qa, qb, doc in fact_reuse_pairs(questions):
        if new_ids is None or qa in new_ids or qb in new_ids:
            errors.append(f"{qa} and {qb} use the same fact from {doc}")
    return errors


# ---------------------------------------------------------------------------
# Output files
# ---------------------------------------------------------------------------

def md_cell(text: str) -> str:
    """Make text safe inside a markdown table cell."""
    return str(text).replace("|", "\\|").replace("\n", " ")


def write_questions_review(review: list[dict[str, Any]], path: Path) -> None:
    """One readable table with every question, for approval."""
    lines = ["# Test set for review", "",
             '> **Synthetic versions:** the "old" values in outdated_version and history questions (and in `data/synthetic/`) are **invented for this evaluation**. They are deliberately changed copies of current GitLab handbook pages, **not real GitLab history**. Only the two real_pair questions use real old versions (GitLab Testing Agreement v1-v4, University of Cambridge 2022 draft policy).', "",
             f"{len(review)} questions: " + ", ".join(f"{t} {n}" for t, n in Counter(r['type'] for r in review).items()),
             f"Split: tune {sum(r['split'] == 'tune' for r in review)}, test {sum(r['split'] == 'test' for r in review)}", "",
             "| ID | Type | Split | Style | Word overlap | Question | Expected answer | Gold document(s) |",
             "|---|---|---|---|---|---|---|---|"]
    for r in review:
        docs = "<br>".join(e["doc"] for e in r["evidence"]) or "(none: should decline)"
        overlap = "" if r["overlap"] is None else f"{r['overlap']:.0%}"
        lines.append(f"| {r['id']} | {r['type']} | {r['split']} | {r['style']} | {overlap} | "
                     f"{md_cell(r['question'])} | {md_cell(r['answer'])} | {md_cell(docs)} |")
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
    specs = yaml.safe_load(open(resolve_path(CHANGES_PATH), encoding="utf-8"))
    changes = {f"syn:{s['file']}": s["replace"] for s in specs}
    questions, review, errors = build(source, docs, chunks, changes)

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
    pairs = same_chunk_pairs(questions)
    sizes = Counter(q["cluster"] for q in questions)
    tune_clusters = {q["cluster"] for q in questions if q["split"] == "tune"
                     and q["question_type"] not in ("no_answer", "history", "real_pair")}
    print(f"Links: {len(fact_reuse_pairs(source['questions']))} same-fact pairs, {len(pairs)} same-chunk pairs -> "
          f"{len(sizes)} clusters ({sum(n > 1 for n in sizes.values())} with >1 question, largest {max(sizes.values())}); "
          f"tune `overall`: {len(tune_clusters)} clusters")
    print("Same-chunk pairs:", ", ".join(f"{a}+{b}" for a, b in pairs) or "none")
    print("By type:  ", dict(Counter(q["question_type"] for q in questions)))
    print("By split: ", dict(Counter(q["split"] for q in questions)))
    for split_name in ("tune", "test"):
        by_type = Counter(q["question_type"] for q in questions if q["split"] == split_name)
        print(f"{split_name.capitalize()} split by type:", dict(by_type))
    print("Wrote eval/questions.jsonl, eval/questions_review.md, eval/gold_review.md")


if __name__ == "__main__":
    main()
