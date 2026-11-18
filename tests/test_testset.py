"""Tests for src/testset.py using a tiny fake corpus."""

from collections import Counter

import pytest

import src.testset as testset
from src.testset import assign_splits, build, normalize, old_quote, stratified_split


def make_doc(doc_id, text, group=None, current=True, status=None):
    return {"doc_id": doc_id, "doc_title": doc_id, "version_group": group or doc_id, "is_current": current,
            "version_status": status or ("current" if current else "superseded"),
            "pages": [{"page": None, "text": text}]}


def make_chunk(doc_id, i, text):
    return {"chunk_id": f"{doc_id}::fixed-500-50::{i}", "doc_id": doc_id, "doc_title": doc_id,
            "section_path": "", "text": text}


# A current page, its full-copy old version (hotel fact changed, meals fact unchanged) and an unrelated PDF.
DOCS = [
    make_doc("hb:expenses", "Hotel stays are capped at **$300** per night.\nMeals up to $120 per day."),
    make_doc("syn:expenses-old", "Hotel stays are capped at $250 per night.\nMeals up to $120 per day.",
             group="hb:expenses", current=False),
    make_doc("pdf:leave", "Staff get 30 days\nof leave per year. Meals up to $90 per day."),
    make_doc("pdf:other", "Annual leave rules: staff get 30 days of leave per year."),
]
CHUNKS = [
    make_chunk("hb:expenses", 0, "Hotel stays are capped at **$300** per night."),
    make_chunk("hb:expenses", 1, "Meals up to $120 per day."),
    make_chunk("syn:expenses-old", 0, "Hotel stays are capped at $250 per night. Meals up to $120 per day."),
    make_chunk("pdf:leave", 0, "Staff get 30 days\nof leave per year. Meals up to $90 per day."),
    make_chunk("pdf:other", 0, "Annual leave rules: staff get 30 days of leave per year."),
]


@pytest.fixture(autouse=True)
def small_counts(monkeypatch):
    """The real builder expects 106 questions; these tests use a handful."""
    monkeypatch.setattr(testset, "EXPECTED_COUNTS", None)


def source(*questions):
    return {"no_answer_text": "I couldn't find this in the documents.", "questions": list(questions)}


def q(qid, qtype, doc, quote, split="tune"):
    return {"id": qid, "type": qtype, "split": split, "question": "?", "answer": "x",
            "evidence": [{"doc": doc, "quote": quote}]}


# --- normalize and splits ------------------------------------------------------------------

def test_normalize_ignores_formatting():
    assert normalize("Hotel  stays\nare **capped** at ‘$300’") == "hotel stays are capped at '$300'"


def test_stratified_split_counts_and_determinism():
    questions = [{"id": f"{t}-{i}", "type": t} for t, n in
                 {"lookup": 20, "paraphrase": 15, "exact_term": 10, "multi_doc": 10,
                  "outdated_version": 15, "no_answer": 10}.items() for i in range(n)]
    split = stratified_split(questions, test_size=25, seed=42)
    test_by_type = Counter(qq["type"] for qq in questions if split[qq["id"]] == "test")
    assert test_by_type == {"lookup": 6, "paraphrase": 5, "exact_term": 3, "multi_doc": 3,
                            "outdated_version": 5, "no_answer": 3}
    assert split == stratified_split(questions, test_size=25, seed=42)


def test_frozen_splits_are_kept_and_new_ones_assigned():
    old = [{"id": f"old-{i}", "type": "lookup", "split": "test" if i < 3 else "tune"} for i in range(10)]
    new = [{"id": f"new-{i}", "type": "outdated_version"} for i in range(16)]
    split = assign_splits(old + new)
    assert all(split[f"old-{i}"] == ("test" if i < 3 else "tune") for i in range(10))  # untouched
    assert sum(split[f"new-{i}"] == "test" for i in range(16)) == round(16 * testset.TEST_SHARE)


# --- evidence rules -------------------------------------------------------------------------

def test_valid_lookup_gets_gold_chunk():
    built, _, errors = build(source(q("a", "lookup", "pdf:leave", "Staff get 30 days of leave per year.")),
                             DOCS[:3], CHUNKS[:4])
    assert errors == []
    assert built[0]["gold_chunk_ids"] == ["pdf:leave::fixed-500-50::0"]  # matched across the line break


def test_missing_quote_is_an_error():
    _, _, errors = build(source(q("a", "lookup", "pdf:leave", "Staff get 40 days")), DOCS, CHUNKS)
    assert any("quote not found" in e for e in errors)


def test_quote_in_unrelated_doc_is_ambiguous():
    _, _, errors = build(source(q("a", "lookup", "pdf:leave", "staff get 30 days of leave per year")), DOCS, CHUNKS)
    assert any("unrelated docs ['pdf:other']" in e for e in errors)


def test_quote_in_other_version_becomes_acceptable():
    built, _, errors = build(source(q("a", "lookup", "hb:expenses", "Meals up to $120 per day.")), DOCS, CHUNKS)
    assert errors == []
    assert built[0]["acceptable_doc_ids"] == ["syn:expenses-old"]
    assert built[0]["gold_evidence"][0]["acceptable_doc_ids"] == ["syn:expenses-old"]


def test_quote_split_across_chunks_is_an_error():
    quote = "Hotel stays are capped at $300 per night. Meals up to $120"
    _, _, errors = build(source(q("a", "lookup", "hb:expenses", quote)), DOCS, CHUNKS)
    assert any("split across chunks" in e for e in errors)


def test_outdated_quote_must_contain_the_changed_fact():
    changes = {"syn:expenses-old": [["capped at **$300**", "capped at $250"]]}
    good, _, errors = build(source(q("a", "outdated_version", "hb:expenses", "Hotel stays are capped at $300 per night.")),
                            DOCS, CHUNKS, changes)
    assert errors == []
    assert good[0]["outdated_doc_ids"] == ["syn:expenses-old"] and good[0]["acceptable_doc_ids"] == []
    assert good[0]["outdated_evidence"] == [{"doc_id": "syn:expenses-old",
                                             "quote": "hotel stays are capped at $250 per night."}]
    _, _, errors = build(source(q("b", "outdated_version", "hb:expenses", "Meals up to $120 per day.")), DOCS, CHUNKS)
    assert any("must contain the changed fact" in e for e in errors)


def test_outdated_question_needs_a_superseded_version():
    _, _, errors = build(source(q("a", "outdated_version", "pdf:leave", "Staff get 30 days")), DOCS[:3], CHUNKS[:4])
    assert any("no superseded version" in e for e in errors)


def test_history_question_points_at_old_version():
    built, review, errors = build(source(q("h", "history", "syn:expenses-old", "capped at $250 per night")), DOCS, CHUNKS)
    assert errors == []
    assert built[0]["gold_doc_ids"] == ["syn:expenses-old"]
    _, _, errors = build(source(q("h", "history", "hb:expenses", "capped at $300 per night")), DOCS, CHUNKS)
    assert any("must point at an OLD version" in e for e in errors)


def test_no_answer_absent_check():
    covered = {"id": "n1", "type": "no_answer", "split": "tune", "question": "parking?",
               "absent": [{"pattern": "hotel", "scope": ""}]}
    absent = {"id": "n2", "type": "no_answer", "split": "tune", "question": "parking?",
              "absent": [{"pattern": "parking", "scope": ""}]}
    built, _, errors = build(source(covered, absent), DOCS, CHUNKS)
    assert any("n1" in e and "topic is covered" in e for e in errors)
    assert not any("n2" in e for e in errors)
    assert built[1]["expected_answer"] == "I couldn't find this in the documents."



def test_old_quote_applies_changes_ignoring_table_pipes():
    assert old_quote("Parental Leave | 16 weeks", [["| Parental Leave | 16 weeks |", "| Parental Leave | 12 weeks |"]]) \
        == "parental leave | 12 weeks"
    assert old_quote("Something unrelated", [["16 weeks", "12 weeks"]]) is None


def test_normal_question_altered_by_synthetic_change_is_an_error():
    docs = DOCS + [make_doc("syn:leave-old", "Staff get 25 days\nof leave per year.", group="pdf:leave", current=False)]
    chunks = CHUNKS + [make_chunk("syn:leave-old", 0, "Staff get 25 days of leave per year.")]
    _, _, errors = build(source(q("a", "lookup", "pdf:leave", "Staff get 30 days of leave per year.")), docs[:3] + docs[4:], chunks[:4] + chunks[5:])
    assert any("synthetic change alters this quote" in e for e in errors)


def test_real_pair_uses_old_evidence_and_acceptable_versions():
    docs = [make_doc("hb:ta", "Customer may provide feedback on features."),
            make_doc("hb:ta-v1", "Customer will provide feedback on features.", group="hb:ta", current=False),
            make_doc("hb:ta-v5", "Customer may provide feedback on features.", group="hb:ta", current=False)]
    chunks = [make_chunk(d["doc_id"], 0, d["pages"][0]["text"]) for d in docs]
    rp = {**q("r", "real_pair", "hb:ta", "Customer may provide feedback"),
          "old_evidence": [{"quote": "Customer will provide feedback"}]}
    built, _, errors = build(source(rp), docs, chunks)
    assert errors == []
    assert built[0]["outdated_doc_ids"] == ["hb:ta-v1"]           # states a different rule
    assert built[0]["acceptable_doc_ids"] == ["hb:ta-v5"]         # same rule as current
    assert built[0]["outdated_evidence"] == [{"doc_id": "hb:ta-v1", "quote": "customer will provide feedback"}]


def test_same_fact_rule():
    from src.testset import same_fact
    d = "hb:logging"
    assert same_fact(d, "Security logs for production systems | 1 year minimum", d, "production systems | 1 year")  # contained
    assert not same_fact(d, "Security logs for production systems | 1 year minimum",
                         d, "Security logs for critical systems that are not production | 90 days minimum")    # values differ
    assert not same_fact(d, "Tips up to 20%", "hb:other", "Tips up to 20%")                                       # other document
    assert same_fact(d, "Set up a session with your buddy 1-2 days before you plan",
                     d, "Set up a catch-up session with your buddy 1-2 days after your return")                   # mostly same words
