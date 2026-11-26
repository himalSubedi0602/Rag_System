"""Phase 8: paired comparison of two generation runs on the same questions.

Run:  python -m src.compare_gen gen_llama gen_qwen
Writes eval/results/compare_gen_<a>_vs_<b>.md and prints the same table. Reads only saved
per_question.csv files: no model is loaded.

Used by the pre-registered choices: the qwen2.5:7b fallback (only if citation-following is poor) and
prompt v2 (only to fix a documented failure category). The main metric is answer accuracy on `overall`;
B replaces A only if the paired cluster 95% interval of (B - A) excludes zero above it. Otherwise A stays.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.compare import paired_bootstrap, to_markdown
from src.config import load_config, resolve_path

SANITY = {"history", "real_pair"}
# Same groups as run_generation.GROUPS (checked by a test)
GROUPS = {
    "overall": lambda t: ~t.isin(SANITY | {"no_answer"}),
    "non_outdated": lambda t: ~t.isin(SANITY | {"no_answer", "outdated_version"}),
    "outdated_version": lambda t: t == "outdated_version",
    "history": lambda t: t == "history",
    "no_answer": lambda t: t == "no_answer",
}
MAIN = ("overall", "correct")
# (group, column): what each row of the table compares. Blank values (e.g. no citation score for a
# declined answer) drop that question from that row only.
ROWS = [MAIN, ("non_outdated", "correct"), ("outdated_version", "correct"), ("outdated_version", "stale_answer"),
        ("history", "correct"), ("overall", "cit_format"), ("overall", "cit_supported"),
        ("no_answer", "declined"), ("overall", "declined")]
LOWER_IS_BETTER = {"stale_answer"}
# Declining is right on no_answer questions and wrong on answerable ones:
LOWER_IS_BETTER_IN = {("overall", "declined")}


def paired_rows(pq_a: pd.DataFrame, pq_b: pd.DataFrame) -> pd.DataFrame:
    """One row per (group, metric): questions compared, better/worse/same counts, levels of A and B, mean
    difference (B - A) and its paired 95% cluster interval. Clusters come from run A (same test set)."""
    merged = pq_a.merge(pq_b, on="id", suffixes=("_a", "_b"))
    rows = []
    for group, col in ROWS:
        if f"{col}_a" not in merged or f"{col}_b" not in merged:
            continue
        sub = merged[GROUPS[group](merged["question_type_a"])]
        sub = sub[sub[f"{col}_a"].notna() & sub[f"{col}_b"].notna()]
        if sub.empty:
            continue
        a, b = sub[f"{col}_a"].astype(float).to_numpy(), sub[f"{col}_b"].astype(float).to_numpy()
        diff = b - a
        lo, hi = paired_bootstrap(diff, sub["cluster_a"].to_numpy())
        sign = -1 if col in LOWER_IS_BETTER or (group, col) in LOWER_IS_BETTER_IN else 1
        rows.append({"metric": f"{col} ({group})", "questions": len(diff), "clusters": sub["cluster_a"].nunique(),
                     "A": round(float(a.mean()), 3), "B": round(float(b.mean()), 3),
                     "better": int((sign * diff > 0).sum()), "worse": int((sign * diff < 0).sum()),
                     "same": int((diff == 0).sum()), "mean_diff (B-A)": round(float(diff.mean()), 3),
                     "ci_lo": lo, "ci_hi": hi})
    if not rows:
        return pd.DataFrame(index=pd.Index([], name="metric"))
    return pd.DataFrame(rows).set_index("metric")


def verdict(table: pd.DataFrame, name_a: str, name_b: str) -> str:
    """The pre-registered decision on the main metric: B wins only if its interval is entirely above zero."""
    key = f"{MAIN[1]} ({MAIN[0]})"
    if key not in table.index:
        return f"no shared `overall` questions: {name_a} stays"
    lo, hi = table.loc[key, "ci_lo"], table.loc[key, "ci_hi"]
    if lo > 0:
        return f"{name_b} is better on answer accuracy (overall): use {name_b}"
    if hi < 0:
        return f"{name_b} is worse on answer accuracy (overall): {name_a} stays"
    return f"no detectable difference on answer accuracy (overall): {name_a} stays"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_a", help="the current choice (e.g. gen_llama)")
    parser.add_argument("run_b", help="the challenger (e.g. gen_qwen or a prompt-v2 run)")
    args = parser.parse_args()

    results_dir = resolve_path(load_config("configs/default.yaml")["paths"]["results_dir"])
    pq_a = pd.read_csv(Path(results_dir) / args.run_a / "per_question.csv")
    pq_b = pd.read_csv(Path(results_dir) / args.run_b / "per_question.csv")
    table = paired_rows(pq_a, pq_b)
    shown = table.copy()
    if not shown.empty:
        shown["95% CI of diff"] = [f"[{lo:.3f}, {hi:.3f}]" for lo, hi in zip(shown.pop("ci_lo"), shown.pop("ci_hi"))]
    decision = verdict(table, args.run_a, args.run_b)
    text = (f"# {args.run_a} (A) vs {args.run_b} (B), paired on shared questions\n\n"
            f"{to_markdown(shown) if not shown.empty else '(no shared questions)'}\n\n"
            f"**Pre-registered decision:** {decision}\n")
    out = Path(results_dir) / f"compare_gen_{args.run_a}_vs_{args.run_b}.md"
    out.write_text(text, encoding="utf-8")
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print(shown.to_string())
    print(f"\nDecision: {decision}\nWrote {out.relative_to(resolve_path('.'))}")


if __name__ == "__main__":
    main()
