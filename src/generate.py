"""Answer generation (Phase 8): question + top retrieved chunks -> answer with [n] citations, or a decline.

The LLM is called in ONE place (`call_llm`), through the local Ollama server's HTTP API with the Python
standard library (no extra package). Everything else takes an `llm` function as an argument, so tests use a
fake LLM and a different backend only needs a new `call_llm`.

Decline (pre-registered, run 10): the system declines if
  1. the cross-encoder score on (question, top-1 chunk) is below the threshold (the LLM is then not needed), or
  2. the LLM's answer is exactly DECLINE (ignoring surrounding whitespace, quotes and a final period).
"""

from __future__ import annotations

import json
import re
import urllib.request
from typing import Any, Callable

DECLINE = "I couldn't find this in the documents."

LLM = Callable[[list[dict[str, str]], dict[str, Any], str], str]   # (messages, cfg, model) -> text

STATUS_TEXT = {"current": "current version",
               "superseded": "OLDER version (a newer version of this page exists)",
               "legacy": "old document (no newer version exists)"}

SYSTEM_PROMPT_V1 = f"""You answer questions about company and organisation policies using ONLY the numbered excerpts provided.

Rules:
- Use only facts stated in the excerpts. Do not use outside knowledge.
- After every sentence that states a fact, cite the excerpt(s) it comes from, like [1] or [2][3].
- Each excerpt shows its last-updated date and whether it is the current version or an older version.
  If excerpts disagree, give the answer from the CURRENT version.
  Only if the question asks about a previous or earlier policy, answer from the older version and say it was the previous policy.
- If the excerpts do not contain the answer, reply with exactly this sentence and nothing else:
{DECLINE}
- Be brief: answer in one to three sentences."""


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

def format_excerpt(n: int, chunk: dict[str, Any]) -> str:
    """'[n] Title > section | updated YYYY-MM-DD | current version' followed by the chunk text."""
    where = chunk["doc_title"] + (f" > {chunk['section_path']}" if chunk.get("section_path") else "")
    date = str(chunk.get("updated_date") or "unknown")[:10]
    status = STATUS_TEXT.get(chunk.get("version_status"), "unknown status")
    return f"[{n}] {where} | updated {date} | {status}\n{chunk['text'].strip()}"


def build_messages(question: str, chunks: list[dict[str, Any]], prompt_version: int = 1) -> list[dict[str, str]]:
    """Chat messages for the generator. Excerpts are numbered 1..len(chunks) in retrieval order."""
    if prompt_version != 1:
        raise ValueError(f"prompt_version {prompt_version} is not defined yet (at most 2 are pre-registered)")
    excerpts = "\n\n".join(format_excerpt(i + 1, c) for i, c in enumerate(chunks))
    user = f"Excerpts:\n\n{excerpts}\n\nQuestion: {question}\nAnswer:"
    return [{"role": "system", "content": SYSTEM_PROMPT_V1}, {"role": "user", "content": user}]


# ---------------------------------------------------------------------------
# The one LLM call
# ---------------------------------------------------------------------------

def call_llm(messages: list[dict[str, str]], cfg: dict[str, Any], model: str) -> str:
    """Send chat messages to the local Ollama server and return the reply text (deterministic settings)."""
    g = cfg["generation"]
    if g["backend"] != "ollama":
        raise ValueError(f"unsupported generation.backend: {g['backend']}")
    body = {"model": model, "messages": messages, "stream": False,
            "options": {"temperature": g["temperature"], "seed": g["seed"], "num_ctx": g["num_ctx"],
                        "num_predict": g["max_tokens"]}}
    request = urllib.request.Request(f"{g['ollama_url']}/api/chat", data=json.dumps(body).encode("utf-8"),
                                     headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=600) as response:
        return json.loads(response.read())["message"]["content"].strip()


# ---------------------------------------------------------------------------
# Decline
# ---------------------------------------------------------------------------

def _plain(text: str) -> str:
    return text.strip().strip("\"'“”‘’ ").rstrip(".").strip().lower().replace("’", "'")


def is_decline(answer: str) -> bool:
    """True if the answer is exactly the decline sentence (whitespace, quotes and final period ignored)."""
    return _plain(answer) == _plain(DECLINE)


def mentions_decline(answer: str) -> bool:
    """Diagnostic: the decline sentence appears inside a longer answer ('partial decline')."""
    return _plain(DECLINE) in _plain(answer) and not is_decline(answer)


def decline_score(question: str, top_chunk: dict[str, Any] | None, cfg: dict[str, Any]) -> float:
    """Cross-encoder score on (question, top-1 retrieved chunk): the confidence signal for declining.
    RRF scores are ranks, not confidence, so they are not used (pre-registered)."""
    if top_chunk is None:
        return float("-inf")
    from src.retrieve import load_reranker   # loads the model once (cached)
    model = load_reranker(cfg["reranker"]["model"], cfg["reranker"]["max_length"], cfg.get("device", "auto"))
    return float(model.predict([(question, top_chunk["text"])], show_progress_bar=False)[0])


def percentile_thresholds(scores: list[float], percentiles: list[float]) -> dict[float, float]:
    """Candidate thresholds = percentiles of the answerable questions' top-1 scores (linear interpolation)."""
    ordered = sorted(scores)
    out = {}
    for p in percentiles:
        pos = (len(ordered) - 1) * p / 100
        lo, frac = int(pos), pos - int(pos)
        hi = min(lo + 1, len(ordered) - 1)
        out[p] = ordered[lo] + (ordered[hi] - ordered[lo]) * frac
    return out


# ---------------------------------------------------------------------------
# Generate
# ---------------------------------------------------------------------------

def generate(question: str, chunks: list[dict[str, Any]], cfg: dict[str, Any], llm: LLM = call_llm,
             score: float | None = None) -> dict[str, Any]:
    """Answer one question from its retrieved chunks.

    `score` is the decline score; if generation.decline_threshold is set and score is below it, the system
    declines without calling the LLM. Returns {"answer", "declined", "declined_by", "partial_decline", "raw"}.
    """
    g = cfg["generation"]
    threshold = g["decline_threshold"]
    if threshold is not None and score is not None and score < threshold:
        return {"answer": DECLINE, "declined": True, "declined_by": "threshold", "partial_decline": False, "raw": None}
    if not chunks:
        return {"answer": DECLINE, "declined": True, "declined_by": "no_chunks", "partial_decline": False, "raw": None}
    raw = llm(build_messages(question, chunks, g["prompt_version"]), cfg, g["model"])
    declined = is_decline(raw)
    return {"answer": DECLINE if declined else raw, "declined": declined, "declined_by": "llm" if declined else None,
            "partial_decline": mentions_decline(raw), "raw": raw}


def parse_citations(answer: str) -> list[int]:
    """Citation numbers in order of appearance: 'x [1][3] y [2]' -> [1, 3, 2] (also '[1, 3]')."""
    found = []
    for group in re.findall(r"\[(\d+(?:\s*,\s*\d+)*)\]", answer):
        found.extend(int(n) for n in group.split(","))
    return found
