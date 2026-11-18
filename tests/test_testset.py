"""Tests for src/testset.py using a tiny fake corpus."""

from collections import Counter

import pytest

import src.testset as testset
from src.testset import build, normalize, stratified_split


def make_doc(doc_id, text, group=None, current=True):
    return {"doc_id": doc_id, "doc_title": doc_id, "version_group": group or doc_id, "is_current": current,
            "pages": [{"page": None, "text": text}]}


def make_chunk(doc_id, i, text):
    return {"chunk_id": f"{doc_id}::fixed-500-50::{i}", "doc_id": doc_id, "doc_title": doc_id,
            "section_path": "", "text": text}


DOCS = [
    make_doc("hb:expenses", "Hotel stays are capped at **$300** per night.\nMeals up to $120 per day."),
    make_doc("syn:expenses-old", "Hotel stays are capped at $250 per night.\nMeals up to $120 per day.",
             group="hb:expenses", current=False),
    make_doc("pdf:leave", "Staff get 30 days\nof leave per year."),
]
CHUNKS = [
    make_chunk("hb:expenses", 0, "Hotel stays are capped at **$300** per night."),
    make_chunk("hb:expenses", 1, "Meals up to $120 per day."),
    make_chunk("syn:expenses-old", 0, "Hotel stays are capped at $250 per night. Meals up to $120 per day."),
    make_chunk("pdf:leave", 0, "Staff get 30 days\nof leave per year."),
]


@pytest.fixture(autouse=True)
def small_counts(monkeypatch):
    """The real builder expects 80 questions; these tests use a handful."""
    monkeypatch.setattr(testset, "EXPECTED_COUNTS", None)
    monkeypatch.setattr(testset, "check_structure", lambda source: [])
    monkeypatch.setattr(testset, "TEST_SIZE", 1)


def source(*questions):
    return {"no_answer_text": "I couldn't find this in the documents.", "questions": list(questions)}


def q(qid, qtype, doc, quote, answer="x"):
    return {"id": qid, "type": qtype, "question": "?", "answer": answer, "evidence": [{"doc": doc, "quote": quote}]}


# --- normalize ---------------------------------------------------------------------

def test_normalize_ignores_formatting():
    assert normalize("Hotel  stays\nare **capped** at ‘$300’") == "hotel stays are capped at '$300'"


# --- split ---------------------------------------------------------------------------

def test_stratified_split_counts_and_determinism():
    questions = [{"id": f"{t}-{i}", "type": t} for t, n in
                 {"lookup": 20, "paraphrase": 15, "exact_term": 10, "multi_doc": 10,
                  "outdated_version": 15, "no_answer": 10}.items() for i in range(n)]
    split = stratified_split(questions, test_size=25, seed=42)
    test_by_type = Counter(qq["type"] for qq in questions if split[qq["id"]] == "test")
    assert sum(test_by_type.values()) == 25
    assert test_by_type == {"lookup": 6, "paraphrase": 5, "exact_term": 3, "multi_doc": 3,
                            "outdated_version": 5, "no_answer": 3}
    assert split == stratified_split(questions, test_size=25, seed=42)  # same seed -> same split


# --- build / validation --------------------------------------------------------------

def test_valid_lookup_gets_gold_chunk():
    built, _, errors = build(source(q("a", "lookup", "pdf:leave", "Staff get 30 days of leave per year.")), DOCS, CHUNKS)
    assert errors == []
    assert built[0]["gold_doc_ids"] == ["pdf:leave"]
    assert built[0]["gold_chunk_ids"] == ["pdf:leave::fixed-500-50::0"]  # matched across the line break


def test_missing_quote_is_an_error():
    _, _, errors = build(source(q("a", "lookup", "pdf:leave", "Staff get 40 days")), DOCS, CHUNKS)
    assert any("quote not found" in e for e in errors)


def test_quote_also_in_other_doc_is_ambiguous_for_normal_questions():
    _, _, errors = build(source(q("a", "lookup", "hb:expenses", "Meals up to $120 per day.")), DOCS, CHUNKS)
    assert any("ambiguous" in e for e in errors)


def test_quote_split_across_chunks_is_an_error():
    quote = "Hotel stays are capped at $300 per night. Meals up to $120"
    _, _, errors = build(source(q("a", "lookup", "hb:expenses", quote)), DOCS, CHUNKS)
    assert any("split across chunks" in e for e in errors)


def test_outdated_question_records_old_versions():
    built, review, errors = build(source(q("a", "outdated_version", "hb:expenses",
                                           "Hotel stays are capped at $300 per night.")), DOCS, CHUNKS)
    assert errors == []
    assert built[0]["outdated_doc_ids"] == ["syn:expenses-old"]
    assert any("fact differs" in note for note in review[0]["notes"])


def test_outdated_question_needs_an_old_version():
    _, _, errors = build(source(q("a", "outdated_version", "pdf:leave", "Staff get 30 days")), DOCS, CHUNKS)
    assert any("no outdated version" in e for e in errors)


def test_no_answer_absent_check():
    covered = {"id": "n1", "type": "no_answer", "question": "parking?", "absent": [{"pattern": "hotel", "scope": ""}]}
    absent = {"id": "n2", "type": "no_answer", "question": "parking?", "absent": [{"pattern": "parking", "scope": ""}]}
    built, _, errors = build(source(covered, absent), DOCS, CHUNKS)
    assert any("n1" in e and "topic is covered" in e for e in errors)
    assert not any("n2" in e for e in errors)
    assert built[1]["expected_answer"] == "I couldn't find this in the documents."
    assert built[1]["gold_doc_ids"] == []
