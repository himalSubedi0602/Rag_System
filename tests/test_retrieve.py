"""Tests for src/retrieve.py (RRF, cap, reranker ordering, two-stage) with fakes instead of models."""

from types import SimpleNamespace

import src.retrieve as retrieve_mod
from src.retrieve import cap_per_version_group, reciprocal_rank_fusion, rerank, scores_are_similarities, two_stage


def test_rrf_rewards_chunks_high_in_either_list():
    dense = [("a", 0.9), ("b", 0.8), ("c", 0.7)]
    keyword = [("c", 12.0), ("d", 9.0)]
    fused = [cid for cid, _ in reciprocal_rank_fusion([dense, keyword], k=60)]
    assert fused[0] == "c"                     # rank 3 + rank 1 beats a single rank 1
    assert set(fused) == {"a", "b", "c", "d"}  # union of both lists


def test_rrf_uses_ranks_not_raw_scores():
    a = reciprocal_rank_fusion([[("x", 0.99)], [("y", 1000.0)]], k=60)
    assert {cid for cid, _ in a} == {"x", "y"} and a[0][1] == a[1][1]   # rank 1 in one list each: equal


def test_cap_per_version_group():
    chunks = {"a1": {"version_group": "A"}, "a2": {"version_group": "A"}, "a3": {"version_group": "A"},
              "b1": {"version_group": "B"}}
    ranked = [("a1", 3), ("a2", 2), ("a3", 1.5), ("b1", 1)]
    assert [cid for cid, _ in cap_per_version_group(ranked, chunks, 2)] == ["a1", "a2", "b1"]


class FakeCrossEncoder:
    """Scores a pair by how many question words appear in the chunk."""
    def predict(self, pairs, **_):
        return [sum(w in text.lower() for w in q.lower().split()) for q, text in pairs]


def fake_bundle():
    chunks = {"d1::0": {"doc_id": "d1", "text": "hotel limit per night", "version_group": "d1"},
              "d1::1": {"doc_id": "d1", "text": "meals", "version_group": "d1"},
              "d2::0": {"doc_id": "d2", "text": "nothing relevant", "version_group": "d2"},
              "d3::0": {"doc_id": "d3", "text": "hotel night limit", "version_group": "d3"}}
    return SimpleNamespace(chunks_by_id=chunks, _chunks_by_doc=None)


CFG = {"reranker": {"model": "fake", "max_length": 512}, "retrieval": {"two_stage_docs": 2}}


def test_rerank_reorders_head_and_keeps_tail_below(monkeypatch):
    monkeypatch.setattr(retrieve_mod, "load_reranker", lambda *a: FakeCrossEncoder())
    candidates = [("d2::0", 0.9), ("d1::0", 0.8), ("d1::1", 0.7)]
    out = rerank("hotel limit night", candidates, fake_bundle(), CFG, n=2)
    assert [cid for cid, _ in out] == ["d1::0", "d2::0", "d1::1"]          # top 2 reordered, tail kept last
    assert out[2][1] < out[1][1]                                            # tail scored below the head


def test_two_stage_reranks_all_chunks_of_top_documents(monkeypatch):
    monkeypatch.setattr(retrieve_mod, "load_reranker", lambda *a: FakeCrossEncoder())
    monkeypatch.setattr(retrieve_mod, "first_stage", lambda q, b, c, depth: [("d2::0", .9), ("d1::1", .8), ("d3::0", .7)])
    out = [cid for cid, _ in two_stage("hotel limit night", fake_bundle(), CFG, k=10)]
    assert "d3::0" not in out                                # d3 is the 3rd document: not in the top 2
    assert out[0] == "d1::0"                                 # d1::0 wasn't in stage 1 but its document was


def test_tie_tolerance_only_for_cosine_scores():
    def cfg(mode="vector", reranker=False, two=False):
        return {"retrieval": {"mode": mode, "two_stage": two}, "reranker": {"enabled": reranker}}
    assert scores_are_similarities(cfg())
    assert not scores_are_similarities(cfg(mode="hybrid"))     # RRF scores: rank only
    assert not scores_are_similarities(cfg(reranker=True))     # cross-encoder logits: rank only
    assert not scores_are_similarities(cfg(two=True))


# --- version handling (Amendment 4) ----------------------------------------------------------

from src.retrieve import allowed_chunk_ids, date_aware_rerank, version_swap  # noqa: E402


def version_bundle():
    def c(doc, idx, text, status, current, day, group="g"):
        return {"doc_id": doc, "chunk_index": idx, "text": text, "version_status": status,
                "is_current": current, "updated_date": day, "version_group": group}
    chunks = {"new::0": c("new", 0, "hotel limit is 300 per night", "current", True, "2026-01-01"),
              "new::1": c("new", 1, "meals are 120 per day", "current", True, "2026-01-01"),
              "old::0": c("old", 0, "hotel limit is 250 per night", "superseded", False, "2022-01-01"),
              "old::1": c("old", 1, "meals are 100 per day", "superseded", False, "2022-01-01"),
              "leg::0": c("leg", 0, "an old agreement", "legacy", False, "2018-01-01", group="L"),
              "oth::0": c("oth", 0, "something else", "current", True, "2018-01-01", group="O")}
    return SimpleNamespace(chunks_by_id=chunks, _chunks_by_doc=None)


def test_version_filter_excludes_only_that_status():
    b = version_bundle()
    assert allowed_chunk_ids(b, "superseded") == {"new::0", "new::1", "leg::0", "oth::0"}
    assert allowed_chunk_ids(b, "legacy") == {"new::0", "new::1", "old::0", "old::1", "oth::0"}


def test_date_aware_rerank_moves_newer_chunks_up_with_weight():
    b = version_bundle()
    ranked = [("old::0", 0.9), ("new::0", 0.8), ("oth::0", 0.7)]
    assert [c for c, _ in date_aware_rerank(ranked, b, 0.0)] == ["old::0", "new::0", "oth::0"]  # w=0: unchanged
    assert [c for c, _ in date_aware_rerank(ranked, b, 0.5)][0] == "new::0"   # newer version overtakes
    assert date_aware_rerank([], b, 0.5) == []


def test_version_swap_replaces_superseded_with_matching_current_chunk():
    b = version_bundle()
    out = version_swap([("old::1", 0.9), ("oth::0", 0.8), ("leg::0", 0.7)], b)
    assert [c for c, _ in out] == ["new::1", "oth::0", "leg::0"]       # meals chunk -> current meals chunk
    dup = version_swap([("old::0", 0.9), ("new::0", 0.8)], b)          # current copy already present lower
    assert [c for c, _ in dup] == ["new::0"]                           # kept once, at the higher position
