"""Retrieval metrics: recall@k and MRR (document + chunk level), stale rate, per-type table, 95% CIs.

Conventions (all positions are CHUNK ranks in the retrieved list, 1 = best):
  gold item   one evidence entry of a question: a gold doc + a supporting quote. Other versions of
              that doc which state the SAME answer are "acceptable" for that item (never for
              outdated_version questions, whose quote contains the changed fact)
  doc hit     a retrieved chunk from the item's gold doc or one of its acceptable docs
  chunk hit   a doc hit whose text contains the quote. Quotes of 8+ words also match if the chunk
              holds a continuous start or end of the quote with >= 80% of its words (a quote cut by a
              chunk boundary); shorter quotes need an exact (normalized) match
  recall@k    share of the question's gold items hit within the top k (multi_doc can score 0.5)
  MRR         1 / rank of the first hit (0 if none), averaged over questions
  stale       outdated_version only: an outdated version's first chunk ranks above the current
              gold doc's first chunk (or appears while the current one doesn't); stale@5 = top 5 only
  fact_stale  stricter: the chunk stating the OLD fact ranks above the chunk stating the CURRENT
              fact (what the LLM would see first). For both, an exact score TIE counts 0.5: identical
              text gets identical vectors, so the order is arbitrary (index insertion order).
              If NEITHER version was retrieved the question can't show staleness: stale = blank (not 0),
              and fact_found (share of questions where a fact chunk was retrieved) reports that miss
Groups: "overall" = all answerable questions except the sanity checks (history, real_pair); "non_outdated"
= overall minus outdated_version (shows effects on general recall separately); history and real_pair get
their own rows. real_pair is scored like outdated_version but with REAL old documents.
no_answer questions have no gold, so they're excluded here (Phase 8 scores them).
"""

from __future__ import annotations

import math
import re
from typing import Any

import numpy as np
import pandas as pd

from src.testset import normalize

TYPE_ORDER = ["lookup", "paraphrase", "exact_term", "multi_doc", "outdated_version", "real_pair", "history"]
SEPARATE_TYPES = {"history", "real_pair"}   # sanity checks: own rows, not part of "overall"
# Headline metrics get 95% CIs. The version metric is fact_stale (on questions where a fact chunk was
# found), always reported with fact_found; doc-level stale is secondary.
HEADLINE = ["chunk_recall@5", "chunk_mrr", "doc_recall@5", "fact_stale", "fact_found", "stale"]
STALE_COLS = ["stale", "stale@5", "fact_stale", "fact_stale@5", "fact_found"]
DIAGNOSTIC_COLS = ["chunk_recall@30", "chunk_recall@100"]
TIE_TOLERANCE = 1e-6
LOOSE_MIN_WORDS = 8       # quotes this long use loose matching
LOOSE_SHARE = 0.8         # share of the quote's words that must appear in the chunk
BOOTSTRAP_SAMPLES = 2000


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def words(text: str) -> list[str]:
    """Word tokens of normalized text: letters, digits and the symbols that matter in policies."""
    return re.findall(r"[a-z0-9$£€%]+", normalize(text))


def quote_matches(quote: str, chunk_text: str) -> bool:
    """Does the chunk contain the quote?

    Short quotes (< 8 words): exact normalized substring.
    Long quotes: the chunk must contain a CONTINUOUS start or end of the quote covering >= 80% of its
    words. That is what a chunk boundary does to a quote (cuts off its end or its beginning). Scattered
    words don't count: a bag-of-words test matched unrelated chunks full of common words.
    """
    quote_words = words(quote)
    if len(quote_words) < LOOSE_MIN_WORDS:
        return normalize(quote) in normalize(chunk_text)
    chunk_string = " " + " ".join(words(chunk_text)) + " "
    min_len = math.ceil(LOOSE_SHARE * len(quote_words))
    for length in range(len(quote_words), min_len - 1, -1):
        head, tail = quote_words[:length], quote_words[-length:]
        if f" {' '.join(head)} " in chunk_string or f" {' '.join(tail)} " in chunk_string:
            return True
    return False


# ---------------------------------------------------------------------------
# Per question
# ---------------------------------------------------------------------------

def first_rank(flags: list[bool]) -> int | None:
    """1-based position of the first True, or None."""
    return next((i + 1 for i, flag in enumerate(flags) if flag), None)


def recall_at_k(found_ranks: list[int | None], k: int) -> float:
    """Share of gold items whose first hit is within the top k. One entry per gold item."""
    return sum(1 for r in found_ranks if r is not None and r <= k) / len(found_ranks)


def reciprocal_rank(rank: int | None) -> float:
    """1/rank, or 0 if never found."""
    return 1.0 / rank if rank else 0.0


def stale_score(current_flags: list[bool], old_flags: list[bool], scores: list[float] | None,
                within: int | None = None) -> float:
    """1.0 if the first 'old' position beats the first 'current' one, 0.0 if not, 0.5 for an exact
    score tie, NaN if neither appears. Positions beyond `within` are ignored. No scores -> rank decides."""
    if within:
        current_flags, old_flags = current_flags[:within], old_flags[:within]
    cur, old = first_rank(current_flags), first_rank(old_flags)
    if old is None and cur is None:
        return float("nan")
    if old is None:
        return 0.0
    if cur is None:
        return 1.0
    if scores is not None and abs(scores[cur - 1] - scores[old - 1]) <= TIE_TOLERANCE:
        return 0.5
    return 1.0 if old < cur else 0.0


def is_stale(ranked_docs: list[str], gold_docs: list[str], outdated_docs: list[str],
             within: int | None = None) -> bool:
    """True if an outdated version outranks the current gold document (rank order only)."""
    return stale_score([d in gold_docs for d in ranked_docs], [d in outdated_docs for d in ranked_docs],
                       None, within) == 1.0


def deep_chunk_recall(question: dict[str, Any], deep_ids: list[str],
                      chunks_by_id: dict[str, dict[str, Any]], depths: list[int]) -> dict[str, float]:
    """Diagnostic: chunk recall at large depths (e.g. 30, 100) over a longer candidate list. It shows
    whether the answer chunk is in the pool at all, i.e. whether a reranker could still rescue it."""
    ranked = [chunks_by_id[cid] for cid in deep_ids]
    ranks = []
    for item in question["gold_evidence"]:
        allowed = {item["doc_id"], *item.get("acceptable_doc_ids", [])}
        ranks.append(first_rank([c["doc_id"] in allowed and quote_matches(item["quote"], c["text"]) for c in ranked]))
    return {f"chunk_recall@{d}": recall_at_k(ranks, d) for d in depths}


def evaluate_question(question: dict[str, Any], ranked_ids: list[str],
                      chunks_by_id: dict[str, dict[str, Any]], ks: list[int],
                      scores: list[float] | None = None) -> dict[str, Any]:
    """All metrics for one question, given the ranked chunk ids (and their scores) retrieval returned."""
    row: dict[str, Any] = {"id": question["id"], "question_type": question["question_type"]}
    if question["question_type"] == "no_answer":
        return row
    ranked = [chunks_by_id[cid] for cid in ranked_ids]

    doc_ranks, chunk_ranks = [], []
    for item in question["gold_evidence"]:
        allowed = {item["doc_id"], *item.get("acceptable_doc_ids", [])}   # same rule at both levels
        in_allowed = [c["doc_id"] in allowed for c in ranked]
        doc_ranks.append(first_rank(in_allowed))
        chunk_ranks.append(first_rank([ok and quote_matches(item["quote"], c["text"])
                                       for ok, c in zip(in_allowed, ranked)]))

    for k in ks:
        row[f"doc_recall@{k}"] = recall_at_k(doc_ranks, k)
        row[f"chunk_recall@{k}"] = recall_at_k(chunk_ranks, k)
    best_doc = min((r for r in doc_ranks if r), default=None)
    best_chunk = min((r for r in chunk_ranks if r), default=None)
    row["doc_mrr"], row["chunk_mrr"] = reciprocal_rank(best_doc), reciprocal_rank(best_chunk)
    row["gold_doc_rank"], row["gold_chunk_rank"] = best_doc, best_chunk

    if question["question_type"] in ("outdated_version", "real_pair"):
        current_doc = [c["doc_id"] in question["gold_doc_ids"] for c in ranked]
        old_doc = [c["doc_id"] in question["outdated_doc_ids"] for c in ranked]
        current_fact = [ok and any(quote_matches(e["quote"], c["text"]) for e in question["gold_evidence"])
                        for ok, c in zip(current_doc, ranked)]
        old_fact = [any(c["doc_id"] == e["doc_id"] and quote_matches(e["quote"], c["text"])
                        for e in question.get("outdated_evidence", [])) for c in ranked]
        row["stale"] = stale_score(current_doc, old_doc, scores)
        row["stale@5"] = stale_score(current_doc, old_doc, scores, within=5)
        if question.get("stale_level", "fact") == "fact":
            row["fact_stale"] = stale_score(current_fact, old_fact, scores)
            row["fact_stale@5"] = stale_score(current_fact, old_fact, scores, within=5)
            row["fact_found"] = float(any(current_fact) or any(old_fact))
        # stale_level "doc" (e.g. rp-02: the old version has no competing fact): only doc-level stale
    return row


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def metric_columns(ks: list[int]) -> list[str]:
    """Metric column names in display order."""
    return ([f"doc_recall@{k}" for k in ks] + ["doc_mrr"] +
            [f"chunk_recall@{k}" for k in ks] + ["chunk_mrr"] + STALE_COLS + DIAGNOSTIC_COLS)


def bootstrap_ci(values: np.ndarray, seed: int = 0) -> tuple[float, float]:
    """95% interval for a mean: resample the questions with replacement many times and take the
    2.5th and 97.5th percentiles of the resampled means. Wide interval = few or noisy questions."""
    values = values[~np.isnan(values)]
    if len(values) == 0:
        return float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    means = rng.choice(values, size=(BOOTSTRAP_SAMPLES, len(values)), replace=True).mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def to_frame(rows: list[dict[str, Any]], ks: list[int]) -> pd.DataFrame:
    """Per-question metrics as a DataFrame (answerable questions only), stale as 1/0/NaN."""
    df = pd.DataFrame([r for r in rows if r["question_type"] != "no_answer"])
    for col in metric_columns(ks):
        if col not in df:
            df[col] = np.nan
    df[STALE_COLS] = df[STALE_COLS].astype(float)
    return df


def aggregate(rows: list[dict[str, Any]], ks: list[int]) -> pd.DataFrame:
    """Mean of every metric per group, plus 95% bootstrap CIs (`<metric>_lo` / `_hi`) for HEADLINE metrics."""
    df = to_frame(rows, ks)
    cols = metric_columns(ks)
    main = df[~df["question_type"].isin(SEPARATE_TYPES)]
    groups = [("overall", main), ("non_outdated", main[main["question_type"] != "outdated_version"])]
    groups += [(t, df[df["question_type"] == t]) for t in TYPE_ORDER]

    table = []
    for name, part in groups:
        if part.empty:
            continue
        entry: dict[str, Any] = {"group": name, "n": len(part)}
        entry.update(part[cols].mean(numeric_only=True).to_dict())   # mean skips NaN
        for metric in HEADLINE:
            entry[f"{metric}_lo"], entry[f"{metric}_hi"] = bootstrap_ci(part[metric].to_numpy(float))
        table.append(entry)
    ci_cols = [f"{m}_{side}" for m in HEADLINE for side in ("lo", "hi")]
    return pd.DataFrame(table).set_index("group")[["n"] + cols + ci_cols]
