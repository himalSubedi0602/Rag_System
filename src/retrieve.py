"""Retrieval: question -> ranked list of chunks.

Supported: vector search, and small-to-big (search pieces, return parent chunks). Phase 7 adds BM25 hybrid with
reciprocal rank fusion, the cross-encoder reranker, the current-version filter and
date-aware reranking, all inside `retrieve()`, each switched on by one config setting.
"""

from __future__ import annotations

from typing import Any

from src.index import IndexBundle, small_to_big_search, vector_search


def unsupported_settings(cfg: dict[str, Any]) -> list[str]:
    """Config options that are not implemented yet (so they are never silently ignored)."""
    r = cfg["retrieval"]
    problems = []
    if r["mode"] != "vector":
        problems.append(f"retrieval.mode={r['mode']}")
    if r["version_filter"] != "none":
        problems.append(f"retrieval.version_filter={r['version_filter']}")
    if r["date_aware_rerank"]:
        problems.append("retrieval.date_aware_rerank=true")
    if cfg["reranker"]["enabled"]:
        problems.append("reranker.enabled=true")
    return problems


def retrieve(question: str, bundle: IndexBundle, cfg: dict[str, Any]) -> list[tuple[str, float]]:
    """Return the top `retrieval.top_k_each` chunks for a question: [(chunk_id, score), ...], best first."""
    problems = unsupported_settings(cfg)
    if problems:
        raise NotImplementedError(f"Not implemented yet (Phase 7): {', '.join(problems)}")
    k = cfg["retrieval"]["top_k_each"]
    if cfg["retrieval"]["small_to_big"]:
        return small_to_big_search(bundle.piece_collection, bundle.embed_fn, question, k)
    return vector_search(bundle.collection, bundle.embed_fn, question, k)
