"""Tests for src/index.py. A fake embedding function keeps them fast and offline."""

import math

import chromadb
import pytest

from src.index import (
    BM25Index,
    bm25_tokenize,
    build_vector_index,
    check_max_tokens,
    collection_name,
    fingerprint,
    from_chroma_metadata,
    to_chroma_metadata,
    vector_search,
)


def fake_embed(texts: list[str]) -> list[list[float]]:
    """Letter-count vectors: texts sharing letters point in similar directions. Normalized like the real one."""
    vectors = []
    for text in texts:
        v = [float(text.lower().count(ch)) for ch in "abcdefghijklmnopqrstuvwxyz"]
        norm = math.sqrt(sum(x * x for x in v)) or 1.0
        vectors.append([x / norm for x in v])
    return vectors


def make_chunk(i: int, text: str, is_current: bool = True, roles=("all_employees",), page=None) -> dict:
    return {
        "chunk_id": f"hb:doc{i}::fixed-500-50::0", "doc_id": f"hb:doc{i}", "doc_title": f"Doc {i}",
        "version_group": f"hb:doc{i}", "is_current": is_current, "source_type": "markdown",
        "source_path": f"handbook/doc{i}.md", "section_path": "", "page": page, "updated_date": "2025-01-01",
        "department": "finance", "access_roles": list(roles), "content_hash": f"h{i}-{hash(text)}",
        "chunk_strategy": "fixed-500-50", "text": text, "chunk_index": 0, "token_count": 5,
        "char_start": 0, "char_end": len(text),
    }


CFG = {"chunking": {"strategy": "fixed", "chunk_size": 500, "chunk_overlap": 50, "min_section_tokens": 50,
                    "add_prefix": False},
       "embedding": {"model": "sentence-transformers/all-MiniLM-L6-v2"}}

CHUNKS = [
    make_chunk(0, "zzzz zzzz zzzz"),
    make_chunk(1, "aaaa aaaa bbbb", is_current=False, roles=("legal",)),
    make_chunk(2, "aaaa aaaa aaaa"),
]


@pytest.fixture
def client(tmp_path):
    return chromadb.PersistentClient(path=str(tmp_path / "chroma"))  # fresh database per test


# --- naming, fingerprint, metadata ------------------------------------------------

def test_collection_name():
    assert collection_name(CFG) == "fixed-500-50__minilm__noprefix"
    cfg = {**CFG, "chunking": {**CFG["chunking"], "add_prefix": True},
           "embedding": {"model": "BAAI/bge-small-en-v1.5"}}
    assert collection_name(cfg) == "fixed-500-50__bge-small__prefix"


def test_fingerprint_changes_when_a_chunk_changes():
    edited = [CHUNKS[0], CHUNKS[1], {**CHUNKS[2], "content_hash": "different"}]
    assert fingerprint(CHUNKS) == fingerprint(list(CHUNKS))
    assert fingerprint(CHUNKS) != fingerprint(edited)
    assert fingerprint(CHUNKS) != fingerprint(CHUNKS[:2])


def test_metadata_roundtrip_handles_none():
    chunk = make_chunk(0, "text", page=None)
    chunk["updated_date"] = None
    meta = to_chroma_metadata(chunk)
    assert meta["page"] == -1 and meta["updated_date"] == ""      # Chroma can't store None
    assert "text" not in meta                                      # stored as the document instead
    restored = from_chroma_metadata(meta)
    assert restored["page"] is None and restored["updated_date"] is None
    assert restored["access_roles"] == ["all_employees"]           # lists are kept


def test_check_max_tokens():
    check_max_tokens("sentence-transformers/all-MiniLM-L6-v2", 256)
    with pytest.raises(ValueError, match="EMBEDDING_MAX_TOKENS"):
        check_max_tokens("sentence-transformers/all-MiniLM-L6-v2", 512)


# --- Chroma ----------------------------------------------------------------------

def test_build_then_reuse_then_rebuild(client):
    collection, built = build_vector_index(CHUNKS, CFG, client, fake_embed)
    assert built and collection.count() == 3

    _, built_again = build_vector_index(CHUNKS, CFG, client, fake_embed)
    assert not built_again                                         # same chunks -> reused

    changed = CHUNKS[:2] + [make_chunk(2, "bbbb bbbb bbbb")]
    collection, rebuilt = build_vector_index(changed, CFG, client, fake_embed)
    assert rebuilt and collection.count() == 3                     # chunks changed -> rebuilt
    assert collection.get(ids=[CHUNKS[2]["chunk_id"]])["documents"] == ["bbbb bbbb bbbb"]


def test_vector_search_ranks_and_filters(client):
    collection, _ = build_vector_index(CHUNKS, CFG, client, fake_embed)

    results = vector_search(collection, fake_embed, "aaaa", k=3)
    assert results[0][0] == CHUNKS[2]["chunk_id"]                  # all a's: most similar
    assert results[0][1] == pytest.approx(1.0, abs=1e-5)           # similarity = 1 - distance
    assert results[-1][0] == CHUNKS[0]["chunk_id"]                 # no shared letters: least similar

    current = vector_search(collection, fake_embed, "aaaa bbbb", k=3, where={"is_current": True})
    assert CHUNKS[1]["chunk_id"] not in [cid for cid, _ in current]  # outdated chunk filtered out

    legal = vector_search(collection, fake_embed, "aaaa", k=3, where={"access_roles": {"$contains": "legal"}})
    assert [cid for cid, _ in legal] == [CHUNKS[1]["chunk_id"]]


# --- BM25 ----------------------------------------------------------------------

def test_bm25_tokenize():
    assert bm25_tokenize("Max $200/night, per PTO-policy!") == ["max", "200", "night", "per", "pto", "policy"]


BM25_CHUNKS = [
    make_chunk(0, "Expense claims must be submitted within 90 days of purchase."),
    make_chunk(1, "Book travel through Navan, the company travel tool."),
    make_chunk(2, "Annual leave requests need manager approval in Workday."),
    make_chunk(3, "Hotel stays are capped per night in most cities."),
    make_chunk(4, "Old rule: book travel through Navan or by phone.", is_current=False),
]


def test_bm25_finds_exact_rare_term():
    index = BM25Index(BM25_CHUNKS, add_prefix=False)
    top_ids = [cid for cid, _ in index.search("Navan", k=5)]
    assert set(top_ids) == {BM25_CHUNKS[1]["chunk_id"], BM25_CHUNKS[4]["chunk_id"]}  # only chunks with the word


def test_bm25_skips_chunks_without_shared_words():
    index = BM25Index(BM25_CHUNKS, add_prefix=False)
    assert index.search("quantum entanglement", k=5) == []


def test_bm25_allowed_ids_filter():
    index = BM25Index(BM25_CHUNKS, add_prefix=False)
    current = {c["chunk_id"] for c in BM25_CHUNKS if c["is_current"]}
    assert [cid for cid, _ in index.search("Navan", k=5, allowed_ids=current)] == [BM25_CHUNKS[1]["chunk_id"]]


def test_bm25_prefix_makes_title_searchable():
    chunks = [{**make_chunk(i, f"Rule number {i} applies."), "doc_title": title}
              for i, title in enumerate(["Expenses", "Leave", "Security", "Travel"])]
    assert BM25Index(chunks, add_prefix=False).search("Security", k=5) == []
    assert BM25Index(chunks, add_prefix=True).search("Security", k=5)[0][0] == chunks[2]["chunk_id"]
