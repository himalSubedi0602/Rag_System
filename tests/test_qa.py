"""Tests for src/qa.py (the Phase 9 app's question pipeline) with a fake LLM and fake retrieval."""

import json
from types import SimpleNamespace

import src.qa as qa


def chunk(i, status="current"):
    return {"chunk_id": f"c{i}", "doc_title": f"Doc {i}", "section_path": "Expenses", "page": None,
            "updated_date": "2026-01-01T00:00:00", "version_status": status, "source_path": f"d{i}.md",
            "text": f"text {i}"}


BUNDLE = SimpleNamespace(chunks_by_id={f"c{i}": chunk(i) for i in range(1, 8)})
CFG = {"run_name": "app", "generation": {"context_chunks": 5, "decline_threshold": None, "prompt_version": 1,
                                         "model": "fake"}}


def setup(monkeypatch, seen=None):
    def fake_retrieve(question, bundle, cfg, role=None):
        if seen is not None:
            seen.append(role)
        return [(f"c{i}", 1.0 / i) for i in range(1, 8)]
    monkeypatch.setattr(qa, "retrieve", fake_retrieve)
    monkeypatch.setattr(qa, "decline_score", lambda q, c, cfg: 3.21)


def test_ask_marks_cited_sources_and_passes_role(monkeypatch):
    roles = []
    setup(monkeypatch, roles)
    out = qa.ask("How long?", "legal", BUNDLE, CFG, llm=lambda m, c, model: "90 days [2][4].")
    assert roles == ["legal"]
    assert [s["n"] for s in out["sources"]] == [1, 2, 3, 4, 5]            # only the 5 chunks the LLM saw
    assert [s["cited"] for s in out["sources"]] == [False, True, False, True, False]
    assert out["sources"][0]["updated"] == "2026-01-01" and not out["declined"]
    assert out["invalid_citations"] == []


def test_ask_flags_invalid_citations_and_declines(monkeypatch):
    setup(monkeypatch)
    bad = qa.ask("q", "all_employees", BUNDLE, CFG, llm=lambda m, c, model: "Yes [7].")
    assert bad["invalid_citations"] == [7]
    declined = qa.ask("q", "all_employees", BUNDLE, CFG,
                      llm=lambda m, c, model: "I couldn't find this in the documents.")
    assert declined["declined"] and declined["declined_by"] == "llm"
    assert not any(s["cited"] for s in declined["sources"])


def test_threshold_declines_without_calling_llm(monkeypatch):
    setup(monkeypatch)
    cfg = {**CFG, "generation": {**CFG["generation"], "decline_threshold": 5.0}}   # score 3.21 < 5.0
    out = qa.ask("q", "all_employees", BUNDLE, cfg, llm=lambda *a: (_ for _ in ()).throw(AssertionError))
    assert out["declined"] and out["declined_by"] == "threshold"


def test_log_query_appends_without_chunk_text(monkeypatch, tmp_path):
    setup(monkeypatch)
    out = qa.ask("q", "finance", BUNDLE, CFG, llm=lambda m, c, model: "A [1].")
    log = tmp_path / "logs" / "queries.jsonl"
    qa.log_query(log, out, CFG)
    qa.log_query(log, out, CFG)
    lines = [json.loads(line) for line in log.read_text().splitlines()]
    assert len(lines) == 2 and lines[0]["role"] == "finance" and lines[0]["model"] == "fake"
    assert "text" not in lines[0]["sources"][0] and lines[0]["sources"][0]["cited"] is True
