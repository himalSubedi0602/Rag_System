"""Retrieval: question -> ranked list of chunks.

Pipeline, each step switched on by one config setting:
  1. first stage   vector search over chunks (or small-to-big pieces); with retrieval.mode = hybrid,
                   BM25 results are merged in by reciprocal rank fusion (RRF)
  2. reranker      a cross-encoder re-scores the top `reranker.candidates` first-stage results
  3. cap           at most `retrieval.max_per_version_group` chunks per version group (0 = off)
  two_stage        alternative to 1-2: rank documents by their best chunk, keep the top N documents,
                   then rerank ALL chunks of those documents with the cross-encoder
Version handling (Amendment 4, runs 8 / 8b / 9 / 9b):
  version_filter     exclude_superseded | exclude_legacy: those chunks are removed BEFORE search
                     (vector search, BM25 and everything after them)
  date_aware_rerank  score' = (1 - w) * rel + w * recency on the final candidate list (scale-free)
  version_swap       each superseded chunk is replaced by the most similar chunk of the current version
"""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import date
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


VERSION_FILTERS = {"none": None, "exclude_superseded": "superseded", "exclude_legacy": "legacy"}


def unsupported_settings(cfg: dict[str, Any]) -> list[str]:
    """Config values that are not implemented (so they are never silently ignored)."""
    r = cfg["retrieval"]
    problems = []
    if r["version_filter"] not in VERSION_FILTERS:
        problems.append(f"retrieval.version_filter={r['version_filter']}")
    if r["two_stage"] and (r["version_filter"] != "none" or r["date_aware_rerank"] or r["version_swap"]):
        problems.append("two_stage combined with version handling")
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


def allowed_chunk_ids(bundle: IndexBundle, excluded_status: str) -> set[str]:
    """Chunk ids whose version_status is not `excluded_status`, computed once per bundle and status."""
    cache = getattr(bundle, "_allowed", None)
    if cache is None:
        cache = bundle._allowed = {}
    if excluded_status not in cache:
        cache[excluded_status] = {cid for cid, c in bundle.chunks_by_id.items()
                                  if c["version_status"] != excluded_status}
    return cache[excluded_status]


EVERYONE = "all_employees"   # access role every user has (data/sources.yaml)


def role_where(role: str) -> dict[str, Any]:
    """Chroma filter: chunks the role may see (its own role, or open to all employees)."""
    if role == EVERYONE:
        return {"access_roles": {"$contains": EVERYONE}}
    return {"$or": [{"access_roles": {"$contains": role}}, {"access_roles": {"$contains": EVERYONE}}]}


def role_allowed_ids(bundle: IndexBundle, role: str) -> set[str]:
    """Chunk ids the role may see, computed once per bundle and role."""
    cache = getattr(bundle, "_role_allowed", None)
    if cache is None:
        cache = bundle._role_allowed = {}
    if role not in cache:
        cache[role] = {cid for cid, c in bundle.chunks_by_id.items()
                       if role in c["access_roles"] or EVERYONE in c["access_roles"]}
    return cache[role]


def first_stage(question: str, bundle: IndexBundle, cfg: dict[str, Any], depth: int,
                role: str | None = None) -> list[tuple[str, float]]:
    """Top `depth` candidates from vector search (or small-to-big), optionally fused with BM25.
    With a version filter, excluded chunks are never searched (run 8 / 8b). With a role (the Phase 9 app;
    evaluation passes none), chunks that role may not see are never searched either."""
    r = cfg["retrieval"]
    excluded = VERSION_FILTERS[r["version_filter"]]
    filters = ([{"version_status": {"$ne": excluded}}] if excluded else []) + ([role_where(role)] if role else [])
    where = filters[0] if len(filters) == 1 else ({"$and": filters} if filters else None)
    if r["small_to_big"]:
        dense = small_to_big_search(bundle.piece_collection, bundle.embed_fn, question, depth, where=where)
    else:
        dense = vector_search(bundle.collection, bundle.embed_fn, question, depth, where=where)
    if r["mode"] != "hybrid":
        return dense
    allowed = allowed_chunk_ids(bundle, excluded) if excluded else None
    if role:
        visible = role_allowed_ids(bundle, role)
        allowed = visible if allowed is None else allowed & visible
    keyword = bundle.bm25.search(question, depth, allowed_ids=allowed)
    return reciprocal_rank_fusion([dense, keyword], r["rrf_k"])[:depth]


# ---------------------------------------------------------------------------
# Stage 2: cross-encoder reranker
# ---------------------------------------------------------------------------

@lru_cache(maxsize=2)
def load_reranker(model_name: str, max_length: int, device: str = "auto"):
    """Load the cross-encoder once. It reads (question, chunk) together and outputs a relevance score."""
    from sentence_transformers import CrossEncoder  # slow import; only when really needed

    return CrossEncoder(model_name, max_length=max_length, device=None if device == "auto" else device)


def rerank(question: str, candidates: list[tuple[str, float]], bundle: IndexBundle,
           cfg: dict[str, Any], n: int) -> list[tuple[str, float]]:
    """Re-score the top `n` candidates with the cross-encoder; the rest keep their order below them.

    The cross-encoder sees the clean chunk text (what the LLM would receive). Its scores are logits;
    the remaining candidates get scores just below the lowest reranked one so the list stays ordered.
    """
    head, tail = candidates[:n], candidates[n:]
    if not head:
        return []
    model = load_reranker(cfg["reranker"]["model"], cfg["reranker"]["max_length"], cfg.get("device", "auto"))
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
# Version handling: date-aware rerank (run 9) and version swap (run 9b)
# ---------------------------------------------------------------------------

def recency_scores(bundle: IndexBundle) -> dict[str, float]:
    """chunk_id -> (updated_date - oldest) / (newest - oldest) over the whole corpus, in [0, 1]."""
    if getattr(bundle, "_recency", None) is None:
        days = {cid: date.fromisoformat(str(c["updated_date"])[:10]).toordinal()
                for cid, c in bundle.chunks_by_id.items()}
        lo, hi = min(days.values()), max(days.values())
        bundle._recency = {cid: (d - lo) / (hi - lo) for cid, d in days.items()}
    return bundle._recency


def date_aware_rerank(ranked: list[tuple[str, float]], bundle: IndexBundle, w: float) -> list[tuple[str, float]]:
    """Blend rank-based relevance with recency: score' = (1 - w) * rel + w * recency, rel = 1 - (rank-1)/N.

    Uses ranks, not raw scores, so it behaves the same after vector search, RRF or the cross-encoder.
    """
    n = len(ranked)
    if n == 0:
        return []
    recency = recency_scores(bundle)
    blended = [(cid, (1 - w) * (1 - i / n) + w * recency[cid]) for i, (cid, _) in enumerate(ranked)]
    return rank_results(blended)


def word_set(text: str) -> set[str]:
    return set(re.findall(r"\w+", text.lower()))


def current_doc_of_group(bundle: IndexBundle) -> dict[str, str]:
    """version_group -> doc_id of its current version (groups with no current version are absent)."""
    if getattr(bundle, "_current_doc", None) is None:
        bundle._current_doc = {c["version_group"]: c["doc_id"] for c in bundle.chunks_by_id.values()
                               if c["is_current"]}
    return bundle._current_doc


def version_swap(ranked: list[tuple[str, float]], bundle: IndexBundle) -> list[tuple[str, float]]:
    """Replace each superseded chunk by the current version's chunk with the highest word overlap
    (Jaccard over word sets), keeping its position. If that chunk is already higher in the list, the swapped
    copy is dropped; if it is lower, the lower copy is dropped (the higher position is kept)."""
    out, seen = [], set()
    for cid, score in ranked:
        chunk = bundle.chunks_by_id[cid]
        target = cid
        current_doc = current_doc_of_group(bundle).get(chunk["version_group"])
        if chunk["version_status"] == "superseded" and current_doc:
            words = word_set(chunk["text"])

            def similarity(other_id: str) -> tuple[float, int]:   # Jaccard; ties -> earlier chunk
                other = bundle.chunks_by_id[other_id]
                o_words = word_set(other["text"])
                return len(words & o_words) / max(1, len(words | o_words)), -other["chunk_index"]

            target = max(chunks_by_doc(bundle)[current_doc], key=similarity)
        if target not in seen:
            out.append((target, score))
            seen.add(target)
    return out


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

def retrieve(question: str, bundle: IndexBundle, cfg: dict[str, Any],
             role: str | None = None) -> list[tuple[str, float]]:
    """Return the top `retrieval.top_k_each` chunks for a question: [(chunk_id, score), ...], best first.
    `role` (Phase 9 app only) restricts the search to documents that access role may see."""
    problems = unsupported_settings(cfg)
    if problems:
        raise NotImplementedError(f"Not implemented yet: {', '.join(problems)}")
    r, rr = cfg["retrieval"], cfg["reranker"]
    k = r["top_k_each"]
    if r["two_stage"]:
        if role:
            raise NotImplementedError("Not implemented yet: role filter with two_stage")
        return two_stage(question, bundle, cfg, k)

    depth = k
    if rr["enabled"]:
        depth = max(depth, rr["candidates"])
    if r["max_per_version_group"] > 0:
        depth = max(depth, 4 * k)            # extra candidates so the cap can still fill k slots
    ranked = first_stage(question, bundle, cfg, depth, role=role)
    if rr["enabled"]:
        ranked = rerank(question, ranked, bundle, cfg, rr["candidates"])
    if r["max_per_version_group"] > 0:
        ranked = cap_per_version_group(ranked, bundle.chunks_by_id, r["max_per_version_group"])
    ranked = ranked[:k]
    if r["date_aware_rerank"]:
        ranked = date_aware_rerank(ranked, bundle, r["date_weight"])
    if r["version_swap"]:
        ranked = version_swap(ranked, bundle)
    return ranked
