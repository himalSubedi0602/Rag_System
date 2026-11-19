"""Indexing: embed chunks into Chroma (vector search) and build a BM25 index (keyword search).

Run:  python -m src.index configs/baseline.yaml                    build or reuse the index
      python -m src.index configs/baseline.yaml --query "..."      compare both searches
      python -m src.index configs/baseline.yaml --force            re-embed even if unchanged
"""

from __future__ import annotations

import argparse
import hashlib
import re
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

import chromadb
import numpy as np
from rank_bm25 import BM25Okapi

from src.chunking import (EMBEDDING_MAX_TOKENS, chunk_all, chunk_source_key, chunks_are_current, chunks_path,
                          get_tokenizer, index_text, load_chunks, strategy_key, token_offsets, window_spans,
                          write_chunks_with_meta)
from src.config import load_config, resolve_path
from src.ingest import load_documents

EmbedFn = Callable[[list[str]], list[list[float]]]  # texts -> one vector per text

MODEL_SHORT_NAMES = {
    "sentence-transformers/all-MiniLM-L6-v2": "minilm",
    "BAAI/bge-small-en-v1.5": "bge-small",
}
ADD_BATCH = 500  # chunks per Chroma insert (Chroma caps the size of a single add)

# Metadata fields copied from each chunk into Chroma ("text" is stored as the document instead).
META_FIELDS = ("doc_id", "doc_title", "version_group", "is_current", "version_status", "source_type", "source_path",
               "section_path", "page", "updated_date", "department", "access_roles", "content_hash",
               "chunk_strategy", "chunk_index", "token_count", "char_start", "char_end")


# ---------------------------------------------------------------------------
# Embedding model
# ---------------------------------------------------------------------------

def check_max_tokens(model_name: str, actual: int) -> None:
    """Make sure the truncation limit Phase 3 reported matches what the loaded model really reads."""
    expected = EMBEDDING_MAX_TOKENS.get(model_name)
    if expected != actual:
        raise ValueError(f"{model_name} reads {actual} tokens but EMBEDDING_MAX_TOKENS says {expected}; "
                         "fix the table in src/chunking.py so truncation stats are correct")


@lru_cache(maxsize=2)
def load_embedder(model_name: str, device: str = "auto") -> EmbedFn:
    """Load a sentence-transformers model once and return a function that embeds a list of texts.
    device "auto" picks Apple GPU (mps), CUDA or CPU automatically; "cpu" forces the CPU."""
    from sentence_transformers import SentenceTransformer  # slow import; only when really needed

    model = SentenceTransformer(model_name, device=None if device == "auto" else device)
    check_max_tokens(model_name, model.max_seq_length)

    def embed(texts: list[str]) -> list[list[float]]:
        # normalize -> every vector has length 1, so cosine similarity is just the dot product
        vectors = model.encode(texts, batch_size=64, normalize_embeddings=True,
                               show_progress_bar=len(texts) > 200, convert_to_numpy=True)
        return vectors.tolist()

    return embed


# ---------------------------------------------------------------------------
# Chroma
# ---------------------------------------------------------------------------

def model_short_name(model_name: str) -> str:
    """'BAAI/bge-small-en-v1.5' -> 'bge-small' (unknown models: last part of the name, cleaned)."""
    return MODEL_SHORT_NAMES.get(model_name) or re.sub(r"[^a-zA-Z0-9.-]", "-", model_name.split("/")[-1])


def collection_name(cfg: dict[str, Any]) -> str:
    """One collection per index setup: chunking + embedding model + prefix."""
    prefix = "prefix" if cfg["chunking"]["add_prefix"] else "noprefix"
    return f"{strategy_key(cfg['chunking'])}__{model_short_name(cfg['embedding']['model'])}__{prefix}"


# Metadata that filters and reranking depend on. If it changes (e.g. a page becomes superseded),
# the stored metadata is stale even though the text is identical, so it must change the fingerprint.
FINGERPRINT_META = ("is_current", "version_status", "version_group", "updated_date", "access_roles")


def fingerprint(chunks: list[dict[str, Any]]) -> str:
    """Hash of every chunk's id, content hash and filterable metadata: changes if any of them change."""
    digest = hashlib.sha256()
    for chunk in chunks:
        meta = "|".join(str(chunk.get(field)) for field in FINGERPRINT_META)
        digest.update(f"{chunk['chunk_id']}|{chunk['content_hash']}|{meta}\n".encode())
    return digest.hexdigest()


def to_chroma_metadata(chunk: dict[str, Any]) -> dict[str, Any]:
    """Chroma metadata can't hold None: markdown chunks have page=None -> -1, missing strings -> ''."""
    meta = {}
    for field in META_FIELDS:
        value = chunk[field]
        if value is None:
            value = -1 if field == "page" else ""
        meta[field] = value
    return meta


def from_chroma_metadata(meta: dict[str, Any]) -> dict[str, Any]:
    """Undo to_chroma_metadata's placeholders."""
    restored = dict(meta)
    if restored.get("page") == -1:
        restored["page"] = None
    if restored.get("updated_date") == "":
        restored["updated_date"] = None
    return restored


def get_client(cfg: dict[str, Any]) -> chromadb.ClientAPI:
    """Chroma client that stores its files in paths.chroma_dir (git-ignored)."""
    return chromadb.PersistentClient(path=str(resolve_path(cfg["paths"]["chroma_dir"])))


def build_vector_index(chunks: list[dict[str, Any]], cfg: dict[str, Any], client: chromadb.ClientAPI,
                       embed_fn: EmbedFn, force: bool = False) -> tuple[Any, bool]:
    """Create (or reuse) the Chroma collection for this config. Returns (collection, was_built).

    A collection is reused only if its stored fingerprint matches the current chunks,
    so stale vectors can't silently be used after re-chunking.
    """
    name, fp = collection_name(cfg), fingerprint(chunks)
    existing = {c.name for c in client.list_collections()}
    if name in existing:
        collection = client.get_collection(name, embedding_function=None)
        if not force and collection.metadata.get("fingerprint") == fp and collection.count() == len(chunks):
            return collection, False
        client.delete_collection(name)  # chunks changed (or --force): rebuild from scratch

    collection = client.create_collection(
        name,
        configuration={"hnsw": {"space": "cosine"}},  # distance = 1 - cosine similarity
        metadata={"fingerprint": fp, "embedding_model": cfg["embedding"]["model"],
                  "add_prefix": cfg["chunking"]["add_prefix"], "chunk_strategy": strategy_key(cfg["chunking"])},
        embedding_function=None,  # we always pass our own vectors; never let Chroma embed
    )
    add_prefix = cfg["chunking"]["add_prefix"]
    for i in range(0, len(chunks), ADD_BATCH):
        batch = chunks[i:i + ADD_BATCH]
        collection.add(
            ids=[c["chunk_id"] for c in batch],
            embeddings=embed_fn([index_text(c, add_prefix) for c in batch]),  # prefix only affects search
            documents=[c["text"] for c in batch],                              # clean text is stored
            metadatas=[to_chroma_metadata(c) for c in batch],
        )
    return collection, True


def tie_break_key(chunk_id: str) -> str:
    """Deterministic order for equal scores that ignores names and version status.

    Sorting ties by chunk_id would favour "hb:..." over "syn:..." (alphabetical), and Chroma's own
    order is insertion order (current docs were inserted first). A hash is stable but arbitrary.
    """
    return hashlib.sha256(chunk_id.encode()).hexdigest()


def rank_results(pairs: list[tuple[str, float]]) -> list[tuple[str, float]]:
    """Sort by score (rounded, so float noise can't decide) and break exact ties by tie_break_key."""
    return sorted(pairs, key=lambda p: (-round(p[1], 6), tie_break_key(p[0])))


def vector_search(collection: Any, embed_fn: EmbedFn, query: str, k: int,
                  where: dict[str, Any] | None = None) -> list[tuple[str, float]]:
    """Top-k chunks by cosine similarity to the query: [(chunk_id, similarity), ...], best first.

    `where` is a Chroma metadata filter, e.g. {"is_current": True}.
    """
    result = collection.query(query_embeddings=embed_fn([query]), n_results=k, where=where,
                              include=["distances"])
    return rank_results([(cid, 1.0 - dist) for cid, dist in zip(result["ids"][0], result["distances"][0])])


# ---------------------------------------------------------------------------
# Small-to-big (run 2b): search small pieces, return their parent chunk
# ---------------------------------------------------------------------------

PIECE_META = ("doc_id", "version_group", "is_current", "version_status", "updated_date", "access_roles")


def make_pieces(chunks: list[dict[str, Any]], cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Split every chunk into overlapping pieces of `piece_size` tokens. Each piece remembers its parent.

    The prefix option (if on) is added to every piece, so each small piece still says which document
    and section it comes from.
    """
    tokenizer = get_tokenizer(cfg["chunking"]["tokenizer"])
    size, overlap = cfg["retrieval"]["piece_size"], cfg["retrieval"]["piece_overlap"]
    pieces = []
    for chunk in chunks:
        text = chunk["text"]
        offsets = token_offsets(text, tokenizer)
        for j, (a, b) in enumerate(window_spans(offsets, 0, len(offsets), size, overlap)):
            piece_text = text[offsets[a][0]:offsets[b - 1][1]]
            pieces.append({
                "piece_id": f"{chunk['chunk_id']}::p{j}",
                "parent_chunk_id": chunk["chunk_id"],
                "text": index_text({**chunk, "text": piece_text}, cfg["chunking"]["add_prefix"]),
                **{field: chunk[field] for field in PIECE_META},
            })
    return pieces


def piece_collection_name(cfg: dict[str, Any]) -> str:
    r = cfg["retrieval"]
    return f"{collection_name(cfg)}__pieces{r['piece_size']}-{r['piece_overlap']}"


def build_piece_index(chunks: list[dict[str, Any]], cfg: dict[str, Any], client: chromadb.ClientAPI,
                      embed_fn: EmbedFn, force: bool = False) -> tuple[Any, bool]:
    """Create (or reuse) the collection of pieces. Reused only if the parent chunks are unchanged."""
    name = piece_collection_name(cfg)
    fp = fingerprint(chunks) + f"|pieces{cfg['retrieval']['piece_size']}-{cfg['retrieval']['piece_overlap']}"
    if name in {c.name for c in client.list_collections()}:
        collection = client.get_collection(name, embedding_function=None)
        if not force and collection.metadata.get("fingerprint") == fp:
            return collection, False
        client.delete_collection(name)
    collection = client.create_collection(name, configuration={"hnsw": {"space": "cosine"}},
                                          metadata={"fingerprint": fp}, embedding_function=None)
    pieces = make_pieces(chunks, cfg)
    for i in range(0, len(pieces), ADD_BATCH):
        batch = pieces[i:i + ADD_BATCH]
        collection.add(ids=[p["piece_id"] for p in batch], embeddings=embed_fn([p["text"] for p in batch]),
                       documents=[p["text"] for p in batch],
                       metadatas=[{"parent_chunk_id": p["parent_chunk_id"],
                                   **{f: ("" if p[f] is None else p[f]) for f in PIECE_META}} for p in batch])
    return collection, True


def small_to_big_search(piece_collection: Any, embed_fn: EmbedFn, query: str, k: int,
                        where: dict[str, Any] | None = None) -> list[tuple[str, float]]:
    """Rank pieces, then return each parent chunk once, scored by its best piece: [(chunk_id, score), ...]."""
    n_pieces = min(piece_collection.count(), k * 6)  # enough pieces to usually yield k distinct parents
    result = piece_collection.query(query_embeddings=embed_fn([query]), n_results=n_pieces, where=where,
                                    include=["distances", "metadatas"])
    pieces = rank_results([(pid, 1.0 - dist) for pid, dist in zip(result["ids"][0], result["distances"][0])])
    parent_of = {pid: meta["parent_chunk_id"] for pid, meta in zip(result["ids"][0], result["metadatas"][0])}
    parents: dict[str, float] = {}
    for pid, score in pieces:                      # best piece first, so the first score seen is the best
        parents.setdefault(parent_of[pid], score)
        if len(parents) == k:
            break
    return list(parents.items())


# ---------------------------------------------------------------------------
# BM25
# ---------------------------------------------------------------------------

def bm25_tokenize(text: str) -> list[str]:
    """Lower-case words and numbers: 'Max $200/night!' -> ['max', '200', 'night']."""
    return re.findall(r"\w+", text.lower())


class BM25Index:
    """Keyword index over chunks. Rebuilt in memory on load: under a second for a few thousand chunks."""

    def __init__(self, chunks: list[dict[str, Any]], add_prefix: bool):
        self.chunk_ids = [c["chunk_id"] for c in chunks]
        self.bm25 = BM25Okapi([bm25_tokenize(index_text(c, add_prefix)) for c in chunks])

    def search(self, query: str, k: int, allowed_ids: set[str] | None = None) -> list[tuple[str, float]]:
        """Top-k chunks by BM25 score: [(chunk_id, score), ...], best first.

        Chunks sharing no word with the query (score 0) are left out. `allowed_ids`
        restricts results, e.g. to current versions only.
        """
        scores = self.bm25.get_scores(bm25_tokenize(query))
        results = []
        # highest score first; exact ties broken by the same version-blind rule as vector search
        order = sorted(range(len(scores)), key=lambda i: (-round(float(scores[i]), 6), tie_break_key(self.chunk_ids[i])))
        for i in order:
            if scores[i] <= 0 or len(results) == k:
                break
            if allowed_ids is None or self.chunk_ids[i] in allowed_ids:
                results.append((self.chunk_ids[i], float(scores[i])))
        return results


# ---------------------------------------------------------------------------
# Everything retrieval needs, loaded together
# ---------------------------------------------------------------------------

@dataclass
class IndexBundle:
    """The built indexes plus a chunk lookup; what retrieval (Phase 6+) works with."""
    collection: Any
    bm25: BM25Index
    chunks_by_id: dict[str, dict[str, Any]]
    embed_fn: EmbedFn
    piece_collection: Any = None   # only for small_to_big


def load_or_create_chunks(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    """Read this config's chunk file, (re)building it if it is missing or was built from other inputs
    (changed documents, settings or chunker code), so a stale chunk file is never reused."""
    path = chunks_path(cfg)
    processed = resolve_path(cfg["paths"]["processed_dir"])
    key = chunk_source_key(cfg, processed / "documents.jsonl")
    if not chunks_are_current(path, key):
        print(f"{path.name} missing or out of date; chunking documents ...")
        write_chunks_with_meta(chunk_all(load_documents(processed), cfg["chunking"]), path, key)
    return load_chunks(path)


def build_indexes(cfg: dict[str, Any], force: bool = False, verbose: bool = True) -> IndexBundle:
    """Build (or reuse) the vector index and build the BM25 index for one config."""
    chunks = load_or_create_chunks(cfg)
    embed_fn = load_embedder(cfg["embedding"]["model"], cfg["device"])
    start = time.perf_counter()
    collection, built = build_vector_index(chunks, cfg, get_client(cfg), embed_fn, force)
    if verbose:
        action = "Built" if built else "Reused (chunks unchanged)"
        print(f"{action} Chroma collection '{collection.name}': {collection.count()} chunks "
              f"in {time.perf_counter() - start:.1f}s")
    pieces = None
    if cfg["retrieval"]["small_to_big"]:
        start = time.perf_counter()
        pieces, built = build_piece_index(chunks, cfg, get_client(cfg), embed_fn, force)
        if verbose:
            print(f"{'Built' if built else 'Reused'} piece collection '{pieces.name}': {pieces.count()} pieces "
                  f"in {time.perf_counter() - start:.1f}s")
    bm25 = BM25Index(chunks, cfg["chunking"]["add_prefix"])
    return IndexBundle(collection, bm25, {c["chunk_id"]: c for c in chunks}, embed_fn, pieces)


def print_results(title: str, results: list[tuple[str, float]], chunks_by_id: dict[str, dict[str, Any]]) -> None:
    """Show ranked results with a short snippet."""
    print(f"\n{title}")
    for rank, (cid, score) in enumerate(results, start=1):
        c = chunks_by_id[cid]
        where = c["section_path"] or (f"page {c['page']}" if c["page"] else "")
        old = "" if c["is_current"] else "  [OUTDATED]"
        snippet = " ".join(c["text"].split())[:110]
        print(f"  {rank}. {score:6.3f}  {c['doc_id']}  {where}{old}\n       {snippet}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("config", nargs="?", default="configs/baseline.yaml")
    parser.add_argument("--query", help="run a test query against both indexes")
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--force", action="store_true", help="re-embed even if the chunks are unchanged")
    args = parser.parse_args()

    cfg = load_config(args.config)
    bundle = build_indexes(cfg, force=args.force)
    model = cfg["embedding"]["model"]
    print(f"Embedding model {model} reads {EMBEDDING_MAX_TOKENS[model]} tokens (checked against the loaded model)")
    print(f"BM25 index: {len(bundle.bm25.chunk_ids)} chunks")

    if args.query:
        print_results(f"VECTOR search (cosine similarity) for: {args.query!r}",
                      vector_search(bundle.collection, bundle.embed_fn, args.query, args.k), bundle.chunks_by_id)
        print_results(f"BM25 search (keyword score) for: {args.query!r}",
                      bundle.bm25.search(args.query, args.k), bundle.chunks_by_id)


if __name__ == "__main__":
    main()
