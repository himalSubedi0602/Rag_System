"""Phase 8 generation, grading and decline logic, with a fake LLM (no Ollama needed)."""

import math

import pandas as pd

from src.generate import (DECLINE, build_messages, generate, is_decline, mentions_decline, parse_citations,
                          percentile_thresholds)
from src.grade import (apply_threshold, citation_format, citation_supported, failure_label, grade, numbers,
                       numeric_correct, parse_judge, stale_answer)

CFG = {"seed": 0, "generation": {"model": "gen-model", "judge_model": "judge-model", "prompt_version": 1,
                                 "decline_threshold": None, "backend": "ollama"}}


def chunk(doc, text, status="current", date="2026-01-01"):
    return {"doc_id": doc, "doc_title": doc.title(), "section_path": "", "text": text,
            "version_status": status, "updated_date": date}


CHUNKS = [chunk("hotel", "Hotels are capped at $300 per night."),
          chunk("hotel-old", "Hotels are capped at $250 per night.", "superseded", "2022-01-01")]


def question(qtype="lookup", expected="$300 per night.", **extra):
    q = {"id": "q1", "question": "What is the hotel cap?", "question_type": qtype, "expected_answer": expected,
         "gold_evidence": [{"doc_id": "hotel", "quote": "Hotels are capped at $300 per night.", "acceptable_doc_ids": []}],
         "outdated_evidence": []}
    q.update(extra)
    return q


class FakeLLM:
    """Returns canned replies by model name and records every call."""
    def __init__(self, answer="Hotels are capped at $300 per night [1].", verdict="CORRECT"):
        self.answer, self.verdict, self.calls = answer, verdict, []

    def __call__(self, messages, cfg, model):
        self.calls.append(model)
        return self.verdict if model == cfg["generation"]["judge_model"] else self.answer


# --- prompt and generation -----------------------------------------------------------------

def test_prompt_numbers_excerpts_and_shows_date_and_status():
    user = build_messages("Q?", CHUNKS)[1]["content"]
    assert "[1] Hotel | updated 2026-01-01 | current version" in user
    assert "[2] Hotel-Old | updated 2022-01-01 | OLDER version" in user


def test_generate_calls_llm_and_detects_decline():
    llm = FakeLLM(answer=f'  "{DECLINE}"  ')
    out = generate("Q?", CHUNKS, CFG, llm=llm)
    assert out["declined"] and out["declined_by"] == "llm" and out["answer"] == DECLINE
    assert llm.calls == ["gen-model"]


def test_threshold_declines_without_calling_llm():
    llm = FakeLLM()
    cfg = {**CFG, "generation": {**CFG["generation"], "decline_threshold": 0.0}}
    out = generate("Q?", CHUNKS, cfg, llm=llm, score=-3.2)
    assert out["declined_by"] == "threshold" and llm.calls == []
    assert not generate("Q?", CHUNKS, cfg, llm=llm, score=1.5)["declined"]


def test_decline_must_be_exact():
    assert is_decline("I couldn't find this in the documents")
    assert not is_decline(f"{DECLINE} But hotels are $300 [1].")
    assert mentions_decline(f"{DECLINE} But hotels are $300 [1].")


def test_parse_citations():
    assert parse_citations("a [1][3] b [2, 4] c") == [1, 3, 2, 4]


def test_percentile_thresholds_interpolate():
    t = percentile_thresholds([0.0, 1.0, 2.0, 3.0, 4.0], [0, 50, 10])
    assert t[0] == 0.0 and t[50] == 2.0 and math.isclose(t[10], 0.4)


# --- grading ----------------------------------------------------------------------------------

def test_numbers_are_normalised_and_ignore_citations():
    assert numbers("$1,500 USD, 66.70% and 12.0 days [3]") == {"1500", "66.7", "12"}


def test_numeric_correct_needs_every_expected_number():
    assert numeric_correct("Up to $300 a night [1].", "$300 per night.")
    assert not numeric_correct("Up to $250 a night [1].", "$300 per night.")
    assert numeric_correct("Yes.", "Manager approval is needed.") is None      # no number -> judge


def test_stale_answer_uses_old_only_and_current_only_numbers():
    q = question("outdated_version",
                 outdated_evidence=[{"doc_id": "hotel-old", "quote": "Hotels are capped at $250 per night."}])
    assert stale_answer("It is $250 [2].", q) == 1.0
    assert stale_answer("It is $300 [1] (it used to be $250 [2]).", q) == 0.0
    assert math.isnan(stale_answer("anything", question("outdated_version", outdated_evidence=[
        {"doc_id": "x", "quote": "Room service is not reimbursable"}])))


def test_citation_checks():
    q = question()
    assert citation_format([1, 2], 5) and not citation_format([], 5) and not citation_format([6], 5)
    assert citation_supported([1], CHUNKS, q) and not citation_supported([2], CHUNKS, q)


def test_parse_judge():
    assert parse_judge("CORRECT") is True
    assert parse_judge("Incorrect.") is False
    assert parse_judge("The answer is INCORRECT because ...") is False
    assert parse_judge("maybe") is None


def test_grade_numeric_uses_code_and_still_asks_judge_for_agreement():
    llm = FakeLLM(verdict="INCORRECT")
    row = grade(question(), {"answer": "It is $300 [1].", "declined": False}, CHUNKS, CFG, llm)
    assert row["correct"] is True and row["method"] == "code"
    assert row["judge_correct"] is False                    # disagreement is recorded, code decides
    assert llm.calls == ["judge-model"]                     # judge model, never the generator


def test_grade_non_numeric_uses_judge():
    q = question(expected="Manager approval is needed.")
    row = grade(q, {"answer": "Your manager must approve it [1].", "declined": False}, CHUNKS, CFG, FakeLLM())
    assert row["correct"] is True and row["method"] == "judge"


def test_grade_declines():
    na = grade(question("no_answer"), {"answer": DECLINE, "declined": True}, CHUNKS, CFG, FakeLLM())
    assert na["correct"] is True and na["failure"] is None
    wrong = grade(question(), {"answer": DECLINE, "declined": True}, CHUNKS, CFG, FakeLLM())
    assert wrong["correct"] is False and wrong["failure"] == "wrong_decline"
    answered = grade(question("no_answer"), {"answer": "$300 [1]", "declined": False}, CHUNKS, CFG, FakeLLM())
    assert answered["failure"] == "answered_no_answer"


def test_failure_labels_in_order():
    base = {"correct": False, "question_type": "lookup", "declined": False, "gold_rank": 1,
            "cit_format": True, "cit_supported": True}
    assert failure_label({**base, "gold_rank": None}) == "retrieval_miss"
    assert failure_label({**base, "stale_answer": 1.0}) == "stale_fact"
    assert failure_label({**base, "cit_supported": False}) == "hallucination"
    assert failure_label(base) == "ignored_context"
    assert failure_label({**base, "correct": True}) is None


def test_apply_threshold_regrades_without_new_generation():
    right = grade(question(), {"answer": "It is $300 [1].", "declined": False}, CHUNKS, CFG, FakeLLM())
    assert apply_threshold(right, score=-5.0, threshold=-1.0)["failure"] == "wrong_decline"
    assert apply_threshold(right, score=0.5, threshold=-1.0) is right
    na = grade(question("no_answer"), {"answer": "$300 [1]", "declined": False}, CHUNKS, CFG, FakeLLM())
    assert apply_threshold(na, score=-5.0, threshold=-1.0)["correct"] is True


# --- run-level tables ---------------------------------------------------------------------------

def test_decline_table_and_metrics(tmp_path):
    from run_generation import decline_table, judge_agreement, metrics_table, write_outputs
    rows = []
    for i in range(10):     # answerable, all right, scores 1..10
        r = grade({**question(), "id": f"a{i}"}, {"answer": "It is $300 [1].", "declined": False}, CHUNKS, CFG, FakeLLM())
        rows.append({**r, "decline_score": float(i + 1), "cluster": f"c{i}", "latency_s": 1.0})
    for i in range(4):      # no_answer, LLM answered (wrong), low scores
        r = grade({**question("no_answer"), "id": f"n{i}"}, {"answer": "$300 [1]", "declined": False}, CHUNKS, CFG, FakeLLM())
        rows.append({**r, "decline_score": -5.0, "cluster": f"n{i}", "latency_s": 1.0})
    df = pd.DataFrame(rows)
    table, thresholds = decline_table(df, [2.5, 5, 10])
    assert table.loc[0, "no_answer_declined"] == 0.0           # LLM alone declined nothing
    assert table.loc[1, "no_answer_declined"] == 1.0           # every threshold catches the -5 scores
    assert table["answerable_wrong_decline"].iloc[1:].max() <= 0.1
    assert metrics_table(df).loc["overall", "correct"] == 1.0
    assert judge_agreement(df)["agreement"] == 1.0
    write_outputs(tmp_path, {**CFG, "run_name": "t", "generation": {**CFG["generation"], "context_chunks": 5,
                                                                    "decline_percentiles": [2.5, 5, 10]}},
                  "tune", df, [{**question(), "id": r["id"]} for r in rows])
    assert (tmp_path / "summary.md").exists() and (tmp_path / "judge_audit.md").exists()


def test_select_setting_rule():
    """Guardrail first, then best balanced accuracy, then ties (overlapping intervals) -> lowest threshold."""
    from run_generation import select_setting

    def table(rows):
        return pd.DataFrame(rows, columns=["setting", "threshold", "answerable_wrong_decline",
                                           "balanced_accuracy", "ba_lo", "ba_hi"])
    clear = table([["none", None, 0.02, 0.60, 0.55, 0.65], ["p2.5", 1.0, 0.03, 0.80, 0.75, 0.85],
                   ["p5", 2.0, 0.05, 0.82, 0.77, 0.87], ["p10", 3.0, 0.12, 0.95, 0.90, 0.99]])
    assert select_setting(clear) == 1          # p10 breaks the 10% guardrail; p5 best but ties p2.5 -> lower
    separate = table([["none", None, 0.0, 0.50, 0.45, 0.55], ["p2.5", 1.0, 0.05, 0.90, 0.85, 0.95]])
    assert select_setting(separate) == 1       # no overlap: the clearly better threshold wins
    tied_with_none = table([["none", None, 0.0, 0.78, 0.70, 0.86], ["p2.5", 1.0, 0.02, 0.80, 0.72, 0.88]])
    assert select_setting(tied_with_none) == 0  # overlaps 'no threshold', which declines least
    assert select_setting(table([["p10", 3.0, 0.2, 0.9, 0.8, 1.0]])) is None


def test_balanced_accuracy_ci_brackets_the_estimate():
    from run_generation import balanced_accuracy_ci
    df = pd.DataFrame({"question_type": ["no_answer"] * 10 + ["lookup"] * 30,
                       "declined": [True] * 7 + [False] * 3 + [False] * 27 + [True] * 3,
                       "cluster": [f"c{i}" for i in range(40)]})
    lo, hi = balanced_accuracy_ci(df)
    assert lo < (0.7 + 0.9) / 2 < hi and 0 <= lo and hi <= 1


def test_generate_all_resumes_and_drops_a_cut_line(tmp_path, monkeypatch):
    """Saved answers are reused (no new LLM call), a line cut by a disconnect is dropped and regenerated,
    and every new answer is appended as soon as it is made."""
    import json
    from types import SimpleNamespace

    import run_generation as rg

    bundle = SimpleNamespace(chunks_by_id={"c1": CHUNKS[0]})
    monkeypatch.setattr(rg, "build_indexes", lambda cfg: bundle)
    monkeypatch.setattr(rg, "retrieve", lambda q, b, cfg: [("c1", 1.0)])
    monkeypatch.setattr(rg, "decline_score", lambda q, c, cfg: 5.0)
    cfg = {**CFG, "generation": {**CFG["generation"], "context_chunks": 5}}
    qs = [question(id=f"q{i}") for i in (1, 2, 3)]

    log_path = tmp_path / "generations.jsonl"
    saved = {"id": "q1", "chunk_ids": ["c1"], "decline_score": 5.0, "answer": "saved", "declined": False}
    log_path.write_text(json.dumps(saved) + "\n" + '{"id": "q2", "ans', encoding="utf-8")   # q2 cut short

    llm = FakeLLM()
    log = rg.generate_all(cfg, qs, llm=llm, log_path=log_path)
    assert [e["id"] for e in log] == ["q1", "q2", "q3"]
    assert log[0]["answer"] == "saved" and llm.calls == ["gen-model", "gen-model"]   # only q2 and q3 generated
    lines = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
    assert sorted(e["id"] for e in lines) == ["q1", "q2", "q3"]

    llm2 = FakeLLM()
    assert [e["id"] for e in rg.generate_all(cfg, qs, llm=llm2, log_path=log_path)] == ["q1", "q2", "q3"]
    assert llm2.calls == []                                                           # all resumed
