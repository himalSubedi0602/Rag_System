"""Phase 9: one question -> answer with sources, for the Streamlit app (app.py).

Uses exactly the evaluated pipeline (retrieve -> decline score -> generate), plus the simulated access role:
a user only gets answers from documents their role may see. Every question is appended to a JSONL log.
UI-free, so it is tested with a fake LLM.
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.generate import LLM, call_llm, decline_score, generate, parse_citations
from src.retrieve import retrieve

ROLES = {"Employee": "all_employees", "Legal": "legal", "Finance": "finance"}   # label -> access role


def source_card(n: int, chunk: dict[str, Any], cited: set[int]) -> dict[str, Any]:
    """What the UI shows for excerpt [n]."""
    return {"n": n, "cited": n in cited, "chunk_id": chunk["chunk_id"], "title": chunk["doc_title"],
            "section": chunk.get("section_path") or "", "page": chunk.get("page"),
            "updated": str(chunk.get("updated_date") or "")[:10], "status": chunk.get("version_status"),
            "source_path": chunk.get("source_path"), "text": chunk["text"]}


def ask(question: str, role: str, bundle: Any, cfg: dict[str, Any], llm: LLM = call_llm) -> dict[str, Any]:
    """Answer one question as the given access role. Returns the answer, decline info and the source cards
    (all excerpts the LLM saw, in the order it saw them, each marked cited or not)."""
    start = time.perf_counter()
    ids = [cid for cid, _ in retrieve(question, bundle, cfg, role=role)][:cfg["generation"]["context_chunks"]]
    chunks = [bundle.chunks_by_id[cid] for cid in ids]
    score = decline_score(question, chunks[0] if chunks else None, cfg)
    result = generate(question, chunks, cfg, llm=llm, score=score)
    cited = set() if result["declined"] else set(parse_citations(result["answer"]))
    return {"question": question, "role": role, "answer": result["answer"], "declined": result["declined"],
            "declined_by": result["declined_by"], "decline_score": round(score, 4),
            "threshold": cfg["generation"]["decline_threshold"],
            "sources": [source_card(i + 1, c, cited) for i, c in enumerate(chunks)],
            "invalid_citations": sorted(n for n in cited if not 1 <= n <= len(chunks)),
            "latency_s": round(time.perf_counter() - start, 2)}


def log_query(path: Path, record: dict[str, Any], cfg: dict[str, Any]) -> None:
    """Append one question to the log (chunk ids, not chunk text, to keep it small)."""
    entry = {"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "run_name": cfg["run_name"],
             "model": cfg["generation"]["model"],
             **{k: v for k, v in record.items() if k != "sources"},
             "sources": [{k: s[k] for k in ("n", "chunk_id", "cited", "status")} for s in record["sources"]]}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
