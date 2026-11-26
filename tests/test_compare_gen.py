"""Paired comparison of two generation runs (src/compare_gen.py), on hand-made per_question tables."""

import pandas as pd

from src.compare_gen import GROUPS, paired_rows, verdict


def run(correct, qtype="lookup", **extra):
    n = len(correct)
    df = pd.DataFrame({"id": [f"q{i}" for i in range(n)], "question_type": [qtype] * n,
                       "cluster": [f"c{i}" for i in range(n)], "correct": correct})
    for col, values in extra.items():
        df[col] = values
    return df


def test_groups_match_run_generation():
    import run_generation
    types = pd.Series(["lookup", "outdated_version", "history", "real_pair", "no_answer", "compound"])
    for name, select in run_generation.GROUPS.items():
        assert list(select(types)) == list(GROUPS[name](types)), name


def test_clear_improvement_is_detected():
    a = run([False] * 30 + [True] * 10)
    b = run([True] * 40)
    table = paired_rows(a, b)
    row = table.loc["correct (overall)"]
    assert (row["better"], row["worse"], row["same"]) == (30, 0, 10)
    assert row["A"] == 0.25 and row["B"] == 1.0 and row["ci_lo"] > 0
    assert verdict(table, "gen_llama", "gen_qwen").startswith("gen_qwen is better")


def test_small_mixed_difference_keeps_a():
    a = run([True, False] * 20)
    b = run([False, True] * 20)         # 20 better, 20 worse
    assert "no detectable difference" in verdict(paired_rows(a, b), "gen_llama", "gen_qwen")


def test_blank_values_and_lower_is_better():
    a = run([True] * 4, "outdated_version", stale_answer=[1.0, 1.0, 0.0, None])
    b = run([True] * 4, "outdated_version", stale_answer=[0.0, 0.0, 0.0, 0.0])
    row = paired_rows(a, b).loc["stale_answer (outdated_version)"]
    assert row["questions"] == 3                       # the blank in A drops that question
    assert (row["better"], row["worse"]) == (2, 0)     # stale going DOWN counts as better


def test_wrong_declines_count_as_worse_but_no_answer_declines_as_better():
    a = pd.concat([run([True] * 2, declined=[False] * 2),
                   run([False] * 2, "no_answer", declined=[False] * 2).assign(id=["n0", "n1"], cluster=["d0", "d1"])])
    b = a.copy()
    b["declined"] = True
    table = paired_rows(a, b)
    assert table.loc["declined (overall)", "worse"] == 2
    assert table.loc["declined (no_answer)", "better"] == 2


def test_no_shared_questions():
    a, b = run([True]), run([True]).assign(id=["other"])
    table = paired_rows(a, b)
    assert table.empty and "stays" in verdict(table, "A", "B")
