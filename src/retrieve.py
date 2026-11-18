"""Retrieval: question -> ranked list of chunks.

Pipeline, each step switched on by one config setting:
  1. first stage   vector search over chunks (or small-to-big pieces); with retrieval.mode = hybrid,
                   BM25 results are merged in by reciprocal rank fusion (RRF)
  2. reranker      a cross-encoder re-scores the top `reranker.candidates` first-stage results
  3. cap           at most `retrieval.max_per_version_group` chunks per version group (0 = off)
  two_stage        alternative to 1-2: rank documents by their best chunk, keep the top N documents,
                   then rerank ALL chunks of those documents with the cross-encoder
Version filters / date-aware rerank / version swap (runs 8, 8b, 9, 9b) come in the next branch.
"""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from typing import Any

from src.index import IndexBundle, rank_results, small_to_big_search, vector_search

TWO_STAGE_POOL = 100   # first-stage chunks used to rank documents in two-stage search


def scores_are_similarities(cfg: dict[str, Any]) -> bool:
    """True if the final scores are cosine similarities (0-1 scale), so a fixed tie tolerance means something.

    RRF scores (1/(k+rank): neighbouring ranks differ by ~0.0003) and cross-encoder logits (unbounded) are
    on other scales; for them staleness is decided by rank alone (Phase 7b decision, see NOTES).
    """
    r = cfg["retrieval"]
    return r["mode"] != "hybrid" and not cfg["reranker"]["enabled"] and not r["two_stage"]


def unsupported_settings(cfg: dict[str, Any]) -> list[str]:
    """Config options that are not implemented yet (so they are never silently ignored)."""
    r = cfg["retrieval"]
    problems = []
    if r["version_filter"] != "none":
        problems.append(f"retrieval.version_filter={r['version_filter']}")
    if r["date_aware_rerank"]:
        problems.append("retrieval.date_aware_rerank=true")
    return problems


# ---------------------------------------------------------------------------
# Stage 1: candidates
# ---------------------------------------------------------------------------

def reciprocal_rank_fusion(rankings: list[list[tuple[str, float]]], k: int) -> list[tuple[str, float]]:
    """Merge ranked lists: each chunk scores sum(1 / (k + rank)) over the lists it appears in.

    Only ranks are used, never raw scores, so cosine similarities and BM25 scores (different scales)
    can be combined. A larger k flattens the difference between rank 1 and rank 10.
    """
    fused: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, (cid, _) in enumerate(ranking, start=1):
            fused[cid] += 1.0 / (k + rank)
    return rank_results(list(fused.items()))


def first_stage(question: str, bundle: IndexBundle, cfg: dict[str, Any], depth: int) -> list[tuple[str, float]]:
    """Top `depth` candidates from vector search (or small-to-big), optionally fused with BM25."""
    r = cfg["retrieval"]
    if r["small_to_big"]:
        dense = small_to_big_search(bundle.piece_collection, bundle.embed_fn, question, depth)
    else:
        dense = vector_search(bundle.collection, bundle.embed_fn, question, depth)
    if r["mode"] != "hybrid":
        return dense
    keyword = bundle.bm25.search(question, depth)
    return reciprocal_rank_fusion([dense, keyword], r["rrf_k"])[:depth]


# ---------------------------------------------------------------------------
# Stage 2: cross-encoder reranker
# ---------------------------------------------------------------------------

@lru_cache(maxsize=2)
def load_reranker(model_name: str, max_length: int):
    """Load the cross-encoder once. It reads (question, chunk) together and outputs a relevance score."""
    from sentence_transformers import CrossEncoder  # slow import; only when really needed

    return CrossEncoder(model_name, max_length=max_length)


def rerank(question: str, candidates: list[tuple[str, float]], bundle: IndexBundle,
           cfg: dict[str, Any], n: int) -> list[tuple[str, float]]:
    """Re-score the top `n` candidates with the cross-encoder; the rest keep their order below them.

    The cross-encoder sees the clean chunk text (what the LLM would receive). Its scores are logits;
    the remaining candidates get scores just below the lowest reranked one so the list stays ordered.
    """
    head, tail = candidates[:n], candidates[n:]
    if not head:
        return []
    model = load_reranker(cfg["reranker"]["model"], cfg["reranker"]["max_length"])
    scores = model.predict([(question, bundle.chunks_by_id[cid]["text"]) for cid, _ in head],
                           batch_size=32, show_progress_bar=False)
    reranked = rank_results([(cid, float(s)) for (cid, _), s in zip(head, scores)])
    floor = reranked[-1][1]
    return reranked + [(cid, floor - 1.0 - 0.001 * i) for i, (cid, _) in enumerate(tail)]


# ---------------------------------------------------------------------------
# Stage 3: cap per version group
# ---------------------------------------------------------------------------

def cap_per_version_group(ranked: list[tuple[str, float]], chunks_by_id: dict[str, dict[str, Any]],
                          max_per_group: int) -> list[tuple[str, float]]:
    """Keep at most `max_per_group` chunks from each version group (all versions of one page),
    so one long document - or near-identical old and new versions - can't fill the whole top list."""
    seen: dict[str, int] = defaultdict(int)
    kept = []
    for cid, score in ranked:
        group = chunks_by_id[cid]["version_group"]
        if seen[group] < max_per_group:
            kept.append((cid, score))
            seen[group] += 1
    return kept


# ---------------------------------------------------------------------------
# Two-stage search (run 12)
# ---------------------------------------------------------------------------

def chunks_by_doc(bundle: IndexBundle) -> dict[str, list[str]]:
    """doc_id -> its chunk ids, computed once per bundle."""
    if getattr(bundle, "_chunks_by_doc", None) is None:
        mapping: dict[str, list[str]] = defaultdict(list)
        for cid, chunk in bundle.chunks_by_id.items():
            mapping[chunk["doc_id"]].append(cid)
        bundle._chunks_by_doc = dict(mapping)
    return bundle._chunks_by_doc


def two_stage(question: str, bundle: IndexBundle, cfg: dict[str, Any], k: int) -> list[tuple[str, float]]:
    """Rank documents by their best first-stage chunk, keep the top N, rerank all their chunks."""
    pool = first_stage(question, bundle, cfg, TWO_STAGE_POOL)
    top_docs: list[str] = []
    for cid, _ in pool:                      # pool is best-first, so first appearance = best chunk
        doc = bundle.chunks_by_id[cid]["doc_id"]
        if doc not in top_docs:
            top_docs.append(doc)
        if len(top_docs) == cfg["retrieval"]["two_stage_docs"]:
            break
    candidates = [(cid, 0.0) for doc in top_docs for cid in chunks_by_doc(bundle)[doc]]
    return rerank(question, candidates, bundle, cfg, len(candidates))[:k]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def retrieve(question: str, bundle: IndexBundle, cfg: dict[str, Any]) -> list[tuple[str, float]]:
    """Return the top `retrieval.top_k_each` chunks for a question: [(chunk_id, score), ...], best first."""
    problems = unsupported_settings(cfg)
    if problems:
        raise NotImplementedError(f"Not implemented yet: {', '.join(problems)}")
    r, rr = cfg["retrieval"], cfg["reranker"]
    k = r["top_k_each"]
    if r["two_stage"]:
        return two_stage(question, bundle, cfg, k)

    depth = k
    if rr["enabled"]:
        depth = max(depth, rr["candidates"])
    if r["max_per_version_group"] > 0:
        depth = max(depth, 4 * k)            # extra candidates so the cap can still fill k slots
    ranked = first_stage(question, bundle, cfg, depth)
    if rr["enabled"]:
        ranked = rerank(question, ranked, bundle, cfg, rr["candidates"])
    if r["max_per_version_group"] > 0:
        ranked = cap_per_version_group(ranked, bundle.chunks_by_id, r["max_per_version_group"])
    return ranked[:k]
