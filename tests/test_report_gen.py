"""Phase 8 report (src/report_gen.py) on a small hand-made results folder."""

import json

import pandas as pd
import yaml

from src.report_gen import audit_tally, build_report, load_records, system_records

COLS = ["id", "question_type", "declined", "declined_by", "answer", "correct", "method", "gold_rank", "cit_format",
        "cit_supported", "stale_answer", "judge_correct", "failure", "decline_score", "cluster"]


def row(qid, qtype="lookup", correct=True, declined=False, gold_rank=1.0, score=5.0, failure=None, **kw):
    r = dict(id=qid, question_type=qtype, declined=declined, declined_by="llm" if declined else None,
             answer="I couldn't find this in the documents." if declined else f"Answer {qid} [1].",
             correct=correct, method="declined" if declined else "code", gold_rank=gold_rank,
             cit_format=None if declined else True, cit_supported=None if declined else True, stale_answer=None,
             judge_correct=None if declined else correct, failure=failure, decline_score=score, cluster=qid)
    r.update(kw)
    return r


def make_folder(tmp_path, rows, selected=0, threshold=None, fixed=None):
    folder = tmp_path / "gen_llama"
    folder.mkdir()
    pd.DataFrame(rows, columns=COLS).to_csv(folder / "per_question.csv", index=False)
    decline = pd.DataFrame([["no threshold (LLM decides)", None], ["p5 of answerable top-1 scores", threshold]],
                           columns=["setting", "threshold"])
    decline["selected"] = decline.index == selected
    decline.to_csv(folder / "decline.csv", index=False)
    questions = tmp_path / "questions.jsonl"
    questions.write_text("".join(json.dumps({"id": r["id"], "question": f"Question {r['id']}?",
                                             "expected_answer": f"Expected {r['id']}"}) + "\n" for r in rows))
    cfg = {"run_name": "gen_llama", "eval": {"split": "tune"}, "paths": {"questions": str(questions)},
           "generation": {"model": "llama3.1:8b", "judge_model": "qwen2.5:7b", "prompt_version": 1,
                          "context_chunks": 5, "decline_threshold": fixed}}
    (folder / "config.yaml").write_text(yaml.safe_dump(cfg))
    return folder


ROWS = [row("lk-01"), row("lk-02", correct=False, gold_rank=None, failure="retrieval_miss"),
        row("lk-03", correct=False, gold_rank=4.0, failure="ignored_context"),
        row("lk-04", score=-3.0),                                     # right, but below a threshold of 0
        row("na-01", "no_answer", correct=False, gold_rank=None, failure="answered_no_answer", score=-9.0),
        row("na-02", "no_answer", correct=True, declined=True, gold_rank=None, score=-8.0)]


def test_report_without_threshold(tmp_path):
    folder = make_folder(tmp_path, ROWS)
    assert load_records(folder)[1]["gold_rank"] is None
    report = build_report(folder)
    assert "Decline setting: no threshold (LLM decides)" in report
    assert "| retrieval_miss | no gold chunk in the top 5 | 1 | 0.33 |" in report
    assert "| ignored_context |" in report and "Question lk-03?" in report         # example row shown
    assert "| rank 1 | 2 |" in report and "| rank 3-5 | 1 |" in report             # Limitation 9 buckets
    assert "not marked yet" in report or "judge_audit.md not found" in report


def test_selected_threshold_turns_low_scores_into_declines(tmp_path):
    scores_rows = ROWS + [row(f"lk-{i:02d}", score=float(i)) for i in range(10, 30)]
    folder = make_folder(tmp_path, scores_rows, selected=1, threshold=None)
    answerable = sorted(r["decline_score"] for r in scores_rows if r["question_type"] != "no_answer")
    from src.generate import percentile_thresholds
    t = percentile_thresholds(answerable, [5])[5]
    pd.DataFrame([["no threshold (LLM decides)", None, False], ["p5 of answerable top-1 scores", round(t, 4), True]],
                 columns=["setting", "threshold", "selected"]).to_csv(folder / "decline.csv", index=False)
    report = build_report(folder)
    assert "Decline setting: p5 of answerable top-1 scores" in report
    system = system_records(load_records(folder), t)
    lk04 = next(r for r in system if r["id"] == "lk-04")
    assert lk04["declined"] and lk04["failure"] == "wrong_decline"           # was right, now a wrong decline
    na01 = next(r for r in system if r["id"] == "na-01")
    assert na01["declined"] and na01["correct"]                             # threshold rescues a no_answer
    assert "| wrong_decline | declined an answerable question | 1 |" in report


def test_fixed_threshold_is_not_applied_twice(tmp_path):
    folder = make_folder(tmp_path, ROWS, fixed=0.0)
    report = build_report(folder)
    assert "fixed in the run config (0.0)" in report
    assert "| wrong_decline | declined an answerable question | 0 |" in report   # lk-04 left as generated


def test_audit_tally(tmp_path):
    path = tmp_path / "judge_audit.md"
    header = "| # | id | method | question | expected | answer | judge | my reading |\n|---|---|---|---|---|---|---|---|\n"
    body = ("| 1 | pp-01 | judge | q | e | a | CORRECT | agree |\n| 2 | pp-02 | judge | q | e | a | INCORRECT | d |\n"
            "| 3 | md-01 | judge | q | e | a | CORRECT |  |\n| 4 | md-02 | judge | q | e | a | CORRECT | maybe |\n")
    path.write_text("# Judge audit\n\n" + header + body)
    text = audit_tally(path)
    assert "agree 1, disagree 1 (50% of marked), unmarked 1, unclear 1" in text
    assert "pp-02 (judge said INCORRECT)" in text and "md-02: 'maybe'" in text
    path.write_text(header + "| 1 | pp-01 | judge | q | e | a | CORRECT |  |\n")
    assert "not marked yet" in audit_tally(path)
