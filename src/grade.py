"""Grading generated answers (Phase 8 pre-registration). Code first; an LLM judge only where code can't decide.

  correct        numeric expected answers: the answer contains EVERY number in the expected answer (code);
                 other answers: the judge model (qwen2.5:7b, never the generator) says CORRECT.
                 A declined answerable question is wrong; a declined no_answer question is right.
  judge_correct  the judge's verdict, also collected on numeric answers to measure judge-vs-code agreement
  stale_answer   outdated questions: the answer states an OLD-only number and no CURRENT-only number
                 (NaN when the change has no number, so code can't tell)
  cit_format     at least one citation and every citation is a valid [1]..[n_chunks]
  cit_supported  some cited chunk contains a gold quote (only defined when a gold chunk was in the context)
  failure        one label per wrong answer (see failure_label)
"""

from __future__ import annotations

import re
from typing import Any

from src.evaluate import quote_matches
from src.generate import LLM

JUDGE_PROMPT = """You are grading an answer to a question about a policy document.

Question: {question}
Reference answer: {expected}
Candidate answer: {answer}

Is the candidate answer correct? It is correct if it states the same key facts as the reference answer and
does not contradict it. Extra detail is fine if it does not contradict the reference. Reply with one word:
CORRECT or INCORRECT."""


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------

def numbers(text: str) -> set[str]:
    """Normalised numbers in a text: '$1,500 USD and 66.7% or 12.0' -> {'1500', '66.7', '12'}.
    Citation markers like [2] are removed first so they never count as facts."""
    text = re.sub(r"\[\d+(?:\s*,\s*\d+)*\]", " ", text)
    found = set()
    for raw in re.findall(r"\d[\d,]*(?:\.\d+)?", text):
        value = raw.replace(",", "")
        if "." in value:
            value = value.rstrip("0").rstrip(".")
        found.add(value)
    return found


def numeric_correct(answer: str, expected: str) -> bool | None:
    """True if the answer contains every number of the expected answer; None if the expected has none."""
    needed = numbers(expected)
    if not needed:
        return None
    return needed <= numbers(answer)


def stale_answer(answer: str, question: dict[str, Any]) -> float:
    """1.0 if the answer states an old-only number and no current-only number, 0.0 if not, NaN if the
    changed fact has no number (code can't decide). Old/current numbers come from the evidence quotes."""
    old_q = " ".join(e["quote"] for e in question.get("outdated_evidence", []))
    cur_q = " ".join(e["quote"] for e in question.get("gold_evidence", []))
    old_only, cur_only = numbers(old_q) - numbers(cur_q), numbers(cur_q) - numbers(old_q)
    if not old_only:
        return float("nan")
    said = numbers(answer)
    return 1.0 if (said & old_only) and not (said & cur_only) else 0.0


# ---------------------------------------------------------------------------
# Citations
# ---------------------------------------------------------------------------

def citation_format(cited: list[int], n_chunks: int) -> bool:
    return bool(cited) and all(1 <= c <= n_chunks for c in cited)


def citation_supported(cited: list[int], chunks: list[dict[str, Any]], question: dict[str, Any]) -> bool:
    """Some cited chunk (from an allowed document) contains a gold quote."""
    for c in cited:
        if 1 <= c <= len(chunks):
            chunk = chunks[c - 1]
            for e in question["gold_evidence"]:
                allowed = {e["doc_id"], *e.get("acceptable_doc_ids", [])}
                if chunk["doc_id"] in allowed and quote_matches(e["quote"], chunk["text"]):
                    return True
    return False


def gold_rank_in_context(chunks: list[dict[str, Any]], question: dict[str, Any]) -> int | None:
    """1-based position of the first context chunk holding a gold quote, or None."""
    for i, chunk in enumerate(chunks, start=1):
        for e in question["gold_evidence"]:
            allowed = {e["doc_id"], *e.get("acceptable_doc_ids", [])}
            if chunk["doc_id"] in allowed and quote_matches(e["quote"], chunk["text"]):
                return i
    return None


# ---------------------------------------------------------------------------
# Judge
# ---------------------------------------------------------------------------

def parse_judge(text: str) -> bool | None:
    """'CORRECT' -> True, 'INCORRECT' -> False, anything else -> None (counted as unparsed)."""
    words = re.findall(r"[A-Za-z]+", text.upper())
    if not words:
        return None
    if words[0] == "INCORRECT" or ("INCORRECT" in words and "CORRECT" not in words):
        return False
    if words[0] == "CORRECT":
        return True
    return None


def judge(question: str, expected: str, answer: str, cfg: dict[str, Any], llm: LLM) -> bool | None:
    prompt = JUDGE_PROMPT.format(question=question, expected=expected, answer=answer)
    return parse_judge(llm([{"role": "user", "content": prompt}], cfg, cfg["generation"]["judge_model"]))


# ---------------------------------------------------------------------------
# One question
# ---------------------------------------------------------------------------

def failure_label(row: dict[str, Any]) -> str | None:
    """One label per wrong answer, first matching rule wins; None if the answer is right."""
    if row["correct"]:
        return None
    if row["question_type"] == "no_answer":
        return "answered_no_answer"            # should have declined
    if row["declined"]:
        return "wrong_decline"
    if row["gold_rank"] is None:
        return "retrieval_miss"
    if row.get("stale_answer") == 1.0:
        return "stale_fact"
    if not row["cit_format"] or not row["cit_supported"]:
        return "hallucination"                # no usable citation, or cites no gold chunk
    return "ignored_context"


def grade(question: dict[str, Any], result: dict[str, Any], chunks: list[dict[str, Any]], cfg: dict[str, Any],
          judge_llm: LLM | None, judge_numeric: bool = True) -> dict[str, Any]:
    """All grading fields for one generated answer. `judge_llm=None` skips the judge (e.g. in quick tests);
    non-numeric answers then get correct=None (ungraded)."""
    from src.generate import parse_citations
    qtype = question["question_type"]
    row: dict[str, Any] = {"id": question["id"], "question_type": qtype, "declined": result["declined"],
                           "declined_by": result.get("declined_by"), "partial_decline": result.get("partial_decline", False),
                           "answer": result["answer"]}
    if qtype == "no_answer":
        row.update(correct=result["declined"], method="decline", gold_rank=None)
        row["failure"] = failure_label(row)
        return row

    cited = [] if result["declined"] else parse_citations(result["answer"])
    row["gold_rank"] = gold_rank_in_context(chunks, question)
    row["cit_format"] = citation_format(cited, len(chunks)) if not result["declined"] else None
    row["cit_supported"] = (citation_supported(cited, chunks, question)
                            if not result["declined"] and row["gold_rank"] is not None else None)
    if qtype in ("outdated_version", "real_pair") and not result["declined"]:
        row["stale_answer"] = stale_answer(result["answer"], question)

    code = None if result["declined"] else numeric_correct(result["answer"], question["expected_answer"])
    run_judge = judge_llm is not None and not result["declined"] and (code is None or judge_numeric)
    row["judge_correct"] = (judge(question["question"], question["expected_answer"], result["answer"], cfg, judge_llm)
                            if run_judge else None)
    if result["declined"]:
        row.update(correct=False, method="declined")
    elif code is not None:
        row.update(correct=code, method="code")
    else:
        row.update(correct=row["judge_correct"], method="judge")
    row["failure"] = failure_label(row) if row["correct"] is not None else None
    return row


def apply_threshold(row: dict[str, Any], score: float, threshold: float | None) -> dict[str, Any]:
    """Re-grade a row as if the decline threshold had been set: below it, the system declines (run 10).
    The LLM answer was generated anyway, so one generation pass serves every candidate threshold."""
    if threshold is None or score >= threshold or row["declined"]:
        return row
    out = {**row, "declined": True, "declined_by": "threshold", "answer": "I couldn't find this in the documents."}
    if row["question_type"] == "no_answer":
        out.update(correct=True, method="decline")
    else:
        out.update(correct=False, method="declined", cit_format=None, cit_supported=None, judge_correct=None)
        out.pop("stale_answer", None)
    out["failure"] = failure_label(out)
    return out

