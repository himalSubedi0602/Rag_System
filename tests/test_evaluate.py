"""Tests for src/evaluate.py and src/retrieve.py with hand-checked rankings."""

import math

import pytest

from src.evaluate import aggregate, evaluate_question, is_stale, recall_at_k, reciprocal_rank
from src.retrieve import unsupported_settings

KS = [1, 3, 5]


def chunk(cid, doc, text="filler text", current=True):
    return {"chunk_id": cid, "doc_id": doc, "text": text, "is_current": current}


CHUNKS = {c["chunk_id"]: c for c in [
    chunk("a1", "doc:a", "Unrelated policy text."),
    chunk("b1", "doc:b", "Hotels are capped at $300 per night."),
    chunk("b2", "doc:b", "Other content in the gold document."),
    chunk("c1", "doc:c", "Meals up to $120 per day."),
    chunk("old1", "doc:old", "Hotels are capped at $250 per night.", current=False),
    chunk("d1", "doc:d", "More filler."),
]}


def question(qtype="lookup", gold=("doc:b",), quotes=(("doc:b", "Hotels are capped at $300 per night."),),
             outdated=()):
    return {"id": "q", "question_type": qtype, "gold_doc_ids": list(gold),
            "gold_evidence": [{"doc_id": d, "quote": q} for d, q in quotes], "outdated_doc_ids": list(outdated)}


# --- building blocks -----------------------------------------------------------------

def test_recall_and_reciprocal_rank():
    assert recall_at_k([2], 1) == 0 and recall_at_k([2], 3) == 1
    assert recall_at_k([1, None], 5) == 0.5          # one of two gold items found
    assert reciprocal_rank(4) == 0.25 and reciprocal_rank(None) == 0


def test_is_stale():
    assert is_stale(["doc:old", "doc:b"], ["doc:b"], ["doc:old"])           # old above current
    assert not is_stale(["doc:b", "doc:old"], ["doc:b"], ["doc:old"])       # current first
    assert is_stale(["doc:a", "doc:old"], ["doc:b"], ["doc:old"])           # current missing, old present
    assert not is_stale(["doc:a"], ["doc:b"], ["doc:old"])                  # neither present
    ranking = ["doc:b"] * 5 + ["doc:old"]
    assert not is_stale(ranking, ["doc:b"], ["doc:old"])
    assert not is_stale(["doc:a"] * 5 + ["doc:old"], ["doc:b"], ["doc:old"], within=5)  # old only at rank 6


# --- one question ----------------------------------------------------------------------

def test_gold_at_rank_two():
    row = evaluate_question(question(), ["a1", "b1", "c1"], CHUNKS, KS)
    assert (row["doc_recall@1"], row["doc_recall@3"], row["doc_recall@5"]) == (0, 1, 1)
    assert row["doc_mrr"] == 0.5 and row["chunk_mrr"] == 0.5
    assert row["gold_doc_rank"] == 2


def test_doc_hit_without_chunk_hit():
    # Right document, wrong chunk: document-level hit, chunk-level miss.
    row = evaluate_question(question(), ["b2", "a1"], CHUNKS, KS)
    assert row["doc_recall@1"] == 1 and row["chunk_recall@5"] == 0 and row["chunk_mrr"] == 0


def test_chunk_hit_matches_quote_not_chunk_id():
    # Formatting differences don't matter: the quote is normalized before matching.
    q = question(quotes=(("doc:b", "hotels are CAPPED at $300   per night."),))
    assert evaluate_question(q, ["b1"], CHUNKS, KS)["chunk_recall@1"] == 1


def test_multi_doc_partial_recall():
    q = question("multi_doc", gold=("doc:b", "doc:c"),
                 quotes=(("doc:b", "Hotels are capped at $300 per night."), ("doc:c", "Meals up to $120 per day.")))
    row = evaluate_question(q, ["b1", "a1", "d1", "a1", "a1", "c1"], CHUNKS, KS)
    assert row["doc_recall@5"] == 0.5               # only doc:b in the top 5
    assert row["doc_mrr"] == 1.0                    # first gold hit at rank 1


def test_outdated_question_gets_stale_flags():
    q = question("outdated_version", outdated=("doc:old",))
    row = evaluate_question(q, ["old1", "b1"], CHUNKS, KS)
    assert row["stale"] == 1.0 and row["stale@5"] == 1.0
    assert row["chunk_recall@1"] == 0               # the $250 chunk doesn't contain the $300 quote


def test_no_answer_has_no_metrics():
    row = evaluate_question(question("no_answer", gold=(), quotes=()), ["a1"], CHUNKS, KS)
    assert set(row) == {"id", "question_type"}


# --- aggregation ---------------------------------------------------------------------------

def test_aggregate_overall_and_by_type():
    rows = [
        evaluate_question(question(), ["b1"], CHUNKS, KS),                                       # perfect
        evaluate_question(question(), ["a1", "d1", "c1", "a1", "d1", "b1"], CHUNKS, KS),        # rank 6
        evaluate_question(question("outdated_version", outdated=("doc:old",)), ["old1", "b1"], CHUNKS, KS),
        evaluate_question(question("no_answer", gold=(), quotes=()), ["a1"], CHUNKS, KS),
    ]
    table = aggregate(rows, KS)
    assert table.loc["overall", "n"] == 3                                   # no_answer excluded
    assert table.loc["lookup", "doc_recall@5"] == pytest.approx(0.5)
    assert table.loc["lookup", "doc_mrr"] == pytest.approx((1 + 1 / 6) / 2)
    assert table.loc["outdated_version", "stale"] == 1.0
    assert table.loc["overall", "stale"] == 1.0                             # share of OUTDATED questions
    assert math.isnan(table.loc["lookup", "stale"])


# --- retrieve guard -------------------------------------------------------------------------

def test_unsupported_settings_are_reported():
    cfg = {"retrieval": {"mode": "hybrid", "version_filter": "bogus", "date_aware_rerank": True,
                         "version_swap": False, "two_stage": True},
           "reranker": {"enabled": True}}
    assert unsupported_settings(cfg) == ["retrieval.version_filter=bogus",
                                         "two_stage combined with version handling"]
    cfg["retrieval"].update(version_filter="exclude_superseded", two_stage=False)
    assert unsupported_settings(cfg) == []


# --- matching rule: exact for short quotes, 80% of words for long ones ------------------------

from src.evaluate import bootstrap_ci, quote_matches  # noqa: E402
import numpy as np  # noqa: E402


def test_short_quote_needs_exact_match():
    assert quote_matches("each fiscal quarter", "a campaign takes place each fiscal quarter.")
    # all three words present, but not as the phrase -> no match for a short quote
    assert not quote_matches("each fiscal quarter", "each team reports per quarter in the fiscal year")


def test_long_quote_matches_when_cut_by_a_chunk_boundary():
    quote = "Hotel stays are reimbursable up to $300 USD per night for standard rooms"   # 13 words
    cut_off = "Hotel stays are reimbursable up to $300 USD per night for"                  # 11/13 = 85%
    assert quote_matches(quote, cut_off)
    assert not quote_matches(quote, "Hotel stays are reimbursable up to")                # 6/13 = 46%
    assert quote_matches(quote, "...are reimbursable up to $300 USD per night for standard rooms")  # end kept


def test_scattered_words_do_not_match():
    # 8 of 10 words present but scattered across a list: the sentence is NOT in the chunk (real case md-02).
    quote = "This policy is issued by the Director of Legal Services"
    chunk_text = "Related policies: anti-bribery policy. This is the role of the Director of Legal Services."
    assert not quote_matches(quote, chunk_text)


def test_changed_fact_in_long_quote_is_blocked_by_document_rule():
    # The old copy shares 12 of 13 words (only $250 differs) -> the WORDS would match loosely,
    # but for outdated questions the old doc is not allowed, so it is still not a hit.
    chunks = {"old": chunk("old", "doc:old", "Hotel stays are reimbursable up to $250 USD per night for standard rooms", False)}
    q = question("outdated_version", quotes=(("doc:b", "Hotel stays are reimbursable up to $300 USD per night for standard rooms"),),
                 outdated=("doc:old",))
    row = evaluate_question(q, ["old"], chunks, KS)
    assert row["doc_recall@5"] == 0 and row["chunk_recall@5"] == 0 and row["stale"] == 1.0


# --- acceptable versions: same rule at both levels ------------------------------------------

def test_acceptable_version_counts_at_doc_and_chunk_level():
    chunks = {"copy": chunk("copy", "doc:b-old", "Hotels are capped at $300 per night.", False),
              "noise": chunk("noise", "doc:z", "Hotels are capped at $300 per night.")}
    q = question()
    q["gold_evidence"][0]["acceptable_doc_ids"] = ["doc:b-old"]
    row = evaluate_question(q, ["copy"], chunks, KS)
    assert row["doc_recall@1"] == 1 and row["chunk_recall@1"] == 1      # old copy states the same answer
    row = evaluate_question(q, ["noise"], chunks, KS)
    assert row["doc_recall@5"] == 0 and row["chunk_recall@5"] == 0      # same words, unrelated doc: no hit


# --- groups and intervals ----------------------------------------------------------------------

def test_history_excluded_from_overall_and_non_outdated_row():
    rows = [evaluate_question(question(), ["b1"], CHUNKS, KS),
            evaluate_question(question("outdated_version", outdated=("doc:old",)), ["old1"], CHUNKS, KS),
            evaluate_question(question("history", gold=("doc:old",),
                                       quotes=(("doc:old", "Hotels are capped at $250 per night."),)), ["a1"], CHUNKS, KS)]
    table = aggregate(rows, KS)
    assert table.loc["overall", "n"] == 2                     # history not in overall
    assert table.loc["non_outdated", "n"] == 1
    assert table.loc["non_outdated", "doc_recall@5"] == 1.0
    assert table.loc["history", "n"] == 1
    assert {"chunk_recall@5_lo", "chunk_recall@5_hi"} <= set(table.columns)


def test_bootstrap_ci_brackets_the_mean():
    values = np.array([1.0] * 30 + [0.0] * 20)
    lo, hi = bootstrap_ci(values)
    assert lo < 0.6 < hi and 0 <= lo and hi <= 1
    assert bootstrap_ci(np.array([1.0, 1.0, 1.0])) == (1.0, 1.0)       # no variation -> zero width



# --- ties and fact-level stale ------------------------------------------------------------------

from src.evaluate import stale_score  # noqa: E402


def test_stale_is_blank_when_neither_version_retrieved():
    assert math.isnan(stale_score([False, False], [False, False], scores=[0.5, 0.4]))
    assert stale_score([True, False], [False, False], scores=[0.5, 0.4]) == 0.0


def test_exact_score_tie_counts_half():
    assert stale_score([False, True], [True, False], scores=[0.70, 0.70]) == 0.5   # identical vectors
    assert stale_score([False, True], [True, False], scores=[0.71, 0.70]) == 1.0   # old genuinely higher
    assert stale_score([True, False], [False, True], scores=[0.70, 0.70]) == 0.5   # order alone doesn't decide


def test_fact_stale_compares_the_fact_chunks_not_the_documents():
    chunks = {
        "cur_intro": chunk("cur_intro", "doc:b", "Intro text shared by both versions."),
        "old_intro": chunk("old_intro", "doc:old", "Intro text shared by both versions.", False),
        "old_fact": chunk("old_fact", "doc:old", "Hotels are capped at $250 per night.", False),
        "cur_fact": chunk("cur_fact", "doc:b", "Hotels are capped at $300 per night."),
    }
    q = question("outdated_version", outdated=("doc:old",))
    q["outdated_evidence"] = [{"doc_id": "doc:old", "quote": "hotels are capped at $250 per night."}]
    row = evaluate_question(q, ["cur_intro", "old_intro", "old_fact", "cur_fact"], chunks, KS,
                            scores=[0.9, 0.9, 0.8, 0.7])
    assert row["stale"] == 0.0          # rank: the current doc's intro chunk comes first
    assert row["stale_t005"] == 0.5     # secondary (cosine): the documents tie on their shared intro chunk
    assert row["fact_stale"] == 1.0     # but the OLD fact is shown before the current fact
    assert row["fact_stale_t005"] == 1.0
    assert row["fact_found"] == 1.0


# --- doc-order scoring and depth diagnostics ---------------------------------------------------

from src.evaluate import deep_chunk_recall  # noqa: E402


def test_stale_level_doc_scores_only_document_order():
    q = question("real_pair", outdated=("doc:old",))
    q["stale_level"] = "doc"
    row = evaluate_question(q, ["b1", "old1"], CHUNKS, KS)
    assert row["stale"] == 0.0                      # current version ranked above the old one
    assert "fact_stale" not in row and "fact_found" not in row


def test_deep_chunk_recall_finds_answers_beyond_the_top_30():
    deep = ["a1"] * 40 + ["b1"]                     # answer chunk at rank 41
    chunks = {**CHUNKS}
    result = deep_chunk_recall(question(), deep, chunks, [30, 100])
    assert result == {"chunk_recall@30": 0.0, "chunk_recall@100": 1.0}


def test_tie_tolerance_treats_tiny_gaps_as_ties():
    assert stale_score([False, True], [True, False], scores=[0.803, 0.800]) == 0.5            # gap 0.003 < 0.005
    assert stale_score([False, True], [True, False], scores=None) == 1.0                      # rank decides
    assert stale_score([False, True], [True, False], scores=[0.810, 0.800]) == 1.0            # gap 0.010: real


def test_primary_stale_is_rank_only_and_tolerance_needs_scores():
    q = question("outdated_version", outdated=("doc:old",))
    no_scores = evaluate_question(q, ["old1", "b1"], CHUNKS, KS)                 # e.g. a reranker run
    assert no_scores["stale"] == 1.0 and "stale_t005" not in no_scores
    tied = evaluate_question(q, ["old1", "b1"], CHUNKS, KS, scores=[0.801, 0.800])  # cosine run
    assert tied["stale"] == 1.0                     # primary: same rank scale as every other run
    assert tied["stale_t005"] == 0.5                # secondary: a cosine near-tie


def test_cluster_bootstrap_is_wider_when_questions_are_linked():
    values = np.array([1.0] * 10 + [0.0] * 10)
    independent = bootstrap_ci(values)
    linked = bootstrap_ci(values, clusters=np.array([0] * 10 + [1] * 10))   # two big clusters
    assert (linked[1] - linked[0]) > (independent[1] - independent[0])
    assert bootstrap_ci(values, clusters=np.arange(20)) == independent    # singletons = plain bootstrap
