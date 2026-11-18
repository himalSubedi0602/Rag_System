"""Tests for src/compare.py."""

import pandas as pd

from src.compare import paired


def pq(values: dict[str, tuple[str, float, float]]) -> pd.DataFrame:
    """id -> (question_type, chunk_recall@5, fact_stale)."""
    return pd.DataFrame([{"id": i, "question_type": t, "chunk_recall@5": r, "fact_stale": f}
                         for i, (t, r, f) in values.items()])


A = pq({"l1": ("lookup", 0.0, None), "h1": ("history", 0.0, None),
        "o1": ("outdated_version", 0.0, 1.0), "o2": ("outdated_version", 1.0, None)})
B = pq({"l1": ("lookup", 1.0, None), "h1": ("history", 1.0, None),
        "o1": ("outdated_version", 0.0, 0.0), "o2": ("outdated_version", 1.0, 1.0)})


def test_paired_overall_excludes_sanity_types():
    result = paired(A, B, "overall")
    assert result.loc["chunk_recall@5", "questions"] == 3          # history left out
    assert result.loc["chunk_recall@5", "better"] == 1


def test_paired_non_outdated_group():
    assert paired(A, B, "non_outdated").loc["chunk_recall@5", "questions"] == 1


def test_fact_stale_paired_only_where_both_runs_found_a_fact():
    result = paired(A, B, "outdated_version")
    assert result.loc["fact_stale", "questions"] == 1              # o2 has no value in run A
    assert result.loc["fact_stale", "better"] == 1                 # 1.0 -> 0.0 is an improvement
