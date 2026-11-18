"""Compare two runs: side-by-side metrics with 95% intervals, plus a paired per-question comparison.

Run:  python -m src.compare baseline chunk250
Writes eval/results/compare_<a>_vs_<b>.md and prints the same tables.

Why paired: both runs answer the SAME questions, so comparing question by question
("12 better, 3 worse") is far more informative than two averages with overlapping intervals.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import load_config, resolve_path
from src.evaluate import BOOTSTRAP_SAMPLES, HEADLINE

PAIRED_METRICS = ["chunk_recall@5", "chunk_mrr", "doc_recall@5", "fact_stale", "fact_found", "stale"]
LOWER_IS_BETTER = {"stale", "fact_stale"}


def load_run(results_dir: Path, run: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(metrics table indexed by group, per-question table)."""
    folder = results_dir / run
    return pd.read_csv(folder / "metrics.csv", index_col="group"), pd.read_csv(folder / "per_question.csv")


def ci_text(row: pd.Series, metric: str) -> str:
    if pd.isna(row.get(metric)):
        return ""
    return f"{row[metric]:.3f} [{row[metric + '_lo']:.2f}, {row[metric + '_hi']:.2f}]"


def side_by_side(a: pd.DataFrame, b: pd.DataFrame, name_a: str, name_b: str) -> pd.DataFrame:
    """For each group present in both runs: n and every headline metric with its interval."""
    rows = []
    for group in [g for g in a.index if g in b.index]:
        entry = {"group": group, f"n {name_a}": int(a.loc[group, "n"]), f"n {name_b}": int(b.loc[group, "n"])}
        for metric in HEADLINE:
            entry[f"{metric} {name_a}"] = ci_text(a.loc[group], metric)
            entry[f"{metric} {name_b}"] = ci_text(b.loc[group], metric)
        rows.append(entry)
    return pd.DataFrame(rows).set_index("group")


def paired_bootstrap(diff: np.ndarray, seed: int = 0) -> tuple[float, float]:
    """95% interval of the mean per-question difference (B - A). If it excludes 0, the change is
    unlikely to be luck."""
    rng = np.random.default_rng(seed)
    means = rng.choice(diff, size=(BOOTSTRAP_SAMPLES, len(diff)), replace=True).mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def paired(pq_a: pd.DataFrame, pq_b: pd.DataFrame) -> pd.DataFrame:
    """Per metric, on questions present in both runs: how many got better / worse / stayed, and the
    mean difference with its paired 95% interval. For stale, LOWER is better."""
    merged = pq_a.merge(pq_b, on="id", suffixes=("_a", "_b"))
    rows = []
    for metric in PAIRED_METRICS:
        if f"{metric}_a" not in merged or f"{metric}_b" not in merged:
            continue  # an older run may not have this metric
        both = merged[[f"{metric}_a", f"{metric}_b"]].dropna()
        if both.empty:
            continue
        diff = (both[f"{metric}_b"] - both[f"{metric}_a"]).to_numpy(float)
        sign = -1 if metric in LOWER_IS_BETTER else 1  # stale going down is an improvement
        lo, hi = paired_bootstrap(diff)
        rows.append({"metric": metric, "questions": len(diff),
                     "better": int((sign * diff > 0).sum()), "worse": int((sign * diff < 0).sum()),
                     "same": int((diff == 0).sum()), "mean_diff (B-A)": round(float(diff.mean()), 3),
                     "95% CI of diff": f"[{lo:.3f}, {hi:.3f}]"})
    return pd.DataFrame(rows).set_index("metric")


def to_markdown(df: pd.DataFrame) -> str:
    header = f"| {df.index.name} | " + " | ".join(df.columns) + " |"
    sep = "|---" * (len(df.columns) + 1) + "|"
    body = [f"| {idx} | " + " | ".join(str(v) for v in row) + " |" for idx, row in df.iterrows()]
    return "\n".join([header, sep] + body)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_a")
    parser.add_argument("run_b")
    args = parser.parse_args()

    results_dir = resolve_path(load_config("configs/default.yaml")["paths"]["results_dir"])
    metrics_a, pq_a = load_run(results_dir, args.run_a)
    metrics_b, pq_b = load_run(results_dir, args.run_b)
    sbs = side_by_side(metrics_a, metrics_b, args.run_a, args.run_b)
    pair = paired(pq_a, pq_b)

    text = (f"# {args.run_a} vs {args.run_b}\n\n## Side by side (95% bootstrap intervals)\n\n{to_markdown(sbs)}\n\n"
            f"## Paired, on the {len(pq_a.merge(pq_b, on='id'))} questions both runs share\n\n{to_markdown(pair)}\n")
    out = results_dir / f"compare_{args.run_a}_vs_{args.run_b}.md"
    out.write_text(text, encoding="utf-8")
    with pd.option_context("display.width", 250, "display.max_columns", 30, "display.max_colwidth", 30):
        print(sbs.to_string(), "\n")
        print(pair.to_string())
    print(f"\nWrote {out.relative_to(resolve_path('.'))}")


if __name__ == "__main__":
    main()
