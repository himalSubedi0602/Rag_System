"""One comparison table for several runs against a reference run (normally the baseline).

Run:  python -m src.report --name phase7a baseline chunk250 chunk1000 small2big heading prefix bge
Writes eval/results/report_<name>.md.

Every number says which question group it comes from:
  overall       answerable questions except the sanity checks (history, real_pair)
                -> chunk_recall@5 here is the PRE-REGISTERED MAIN retrieval metric; its verdict is the main one
  non_outdated  overall minus outdated_version (guardrail: side effects on ordinary questions)
  outdated      outdated_version questions; fact_stale is paired ONLY on questions where both runs
                retrieved a fact chunk, with the 0.005 tie tolerance (and without, as *_exact)
Verdicts follow the pre-registered rule: ✅ / ❌ only if the paired 95% interval excludes zero,
otherwise "–" (no detectable difference).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import yaml

from src.compare import LOWER_IS_BETTER, load_run, paired
from src.config import load_config, resolve_path


def first_comment(run: str) -> str:
    """The first comment line of configs/<run>.yaml, used as a one-line description."""
    path = resolve_path("configs") / f"{run}.yaml"
    if not path.exists():
        return ""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            return line.lstrip("# ").strip()
    return ""


def ci(metrics: pd.DataFrame, group: str, metric: str) -> str:
    """'0.455 [0.33, 0.58]' for one group/metric, or '' if not available."""
    if group not in metrics.index or metric not in metrics.columns or pd.isna(metrics.loc[group, metric]):
        return ""
    row = metrics.loc[group]
    if f"{metric}_lo" in row and not pd.isna(row[f"{metric}_lo"]):
        return f"{row[metric]:.3f} [{row[metric + '_lo']:.2f}, {row[metric + '_hi']:.2f}]"
    return f"{row[metric]:.3f}"


def verdict(diff_row: pd.Series, metric: str) -> str:
    """✅ / ❌ if the paired 95% interval excludes zero (in the improving direction), otherwise '–'."""
    lo, hi = (float(x) for x in diff_row["95% CI of diff"].strip("[]").split(","))
    if metric in LOWER_IS_BETTER:
        lo, hi = -hi, -lo
    return "✅" if lo > 0 else "❌" if hi < 0 else "–"


def delta(diffs: pd.DataFrame, metric: str) -> str:
    """'+0.084 [0.013, 0.169] ✅ (9/2, n=66)' for one paired metric."""
    if metric not in diffs.index:
        return "n/a"
    d = diffs.loc[metric]
    return (f"{d['mean_diff (B-A)']:+.3f} {d['95% CI of diff']} {verdict(d, metric)} "
            f"({d['better']}/{d['worse']}, n={d['questions']}, {d['clusters']} clusters)")


def build_table(results_dir: Path, reference: str, runs: list[str]) -> pd.DataFrame:
    ref_metrics, ref_pq = load_run(results_dir, reference)
    rows = []
    for run in runs:
        metrics, pq = load_run(results_dir, run)
        info = yaml.safe_load(open(results_dir / run / "run_info.yaml"))
        entry = {
            "run": run,
            "MAIN chunk R@5 (overall)": ci(metrics, "overall", "chunk_recall@5"),
            "chunk R@5 (non_outdated)": ci(metrics, "non_outdated", "chunk_recall@5"),
            "chunk MRR (overall)": ci(metrics, "overall", "chunk_mrr"),
            "doc R@5 (overall)": ci(metrics, "overall", "doc_recall@5"),
            "chunk R@30 (overall)": f"{metrics.loc['overall', 'chunk_recall@30']:.3f}",
            "chunk R@100 (overall)": f"{metrics.loc['overall', 'chunk_recall@100']:.3f}",
            "fact_stale (outdated, own found set)": ci(metrics, "outdated_version", "fact_stale"),
            "fact_found (outdated)": ci(metrics, "outdated_version", "fact_found"),
            "embedded vectors": info["embedded_units"],
            "vector index MB": info.get("vector_index_mb", ""),
            "mean search ms": info["mean_latency_ms"],
            "tokens unseen %": info["tokens_unseen_pct"],
            "quotes reachable": info["quotes_reachable"],
        }
        if run != reference:
            overall = paired(ref_pq, pq, "overall")
            non_out = paired(ref_pq, pq, "non_outdated")
            outdated = paired(ref_pq, pq, "outdated_version")
            entry.update({
                "Δ MAIN chunk R@5 (overall)": delta(overall, "chunk_recall@5"),
                "Δ chunk R@5 (non_outdated, guardrail)": delta(non_out, "chunk_recall@5"),
                "Δ fact_stale (both found, tol 0.005)": delta(outdated, "fact_stale"),
                "Δ fact_stale (both found, exact ties)": delta(outdated, "fact_stale_exact"),
                "Δ fact_found (outdated, guardrail)": delta(outdated, "fact_found"),
            })
        rows.append(entry)
    return pd.DataFrame(rows).set_index("run").fillna("")


def replication_table(results_dir: Path, reference: str, runs: list[str]) -> pd.DataFrame | None:
    """Main-metric paired Δ on the frozen replication groups (eval/replication_groups.json):
    original questions, new questions only, and combined."""
    path = resolve_path("eval/replication_groups.json")
    if not path.exists():
        return None
    groups = json.loads(path.read_text())
    subsets = {"original": set(groups["original_66"]), "new only": set(groups["new_60"])}
    subsets["combined"] = subsets["original"] | subsets["new only"]
    _, ref_pq = load_run(results_dir, reference)
    rows = []
    for run in runs:
        if run == reference:
            continue
        _, pq = load_run(results_dir, run)
        entry = {"run": run}
        for name, ids in subsets.items():
            diffs = paired(ref_pq[ref_pq["id"].isin(ids)], pq[pq["id"].isin(ids)], "overall")
            entry[f"Δ chunk R@5 ({name}, n={len(ids)})"] = delta(diffs, "chunk_recall@5")
        rows.append(entry)
    return pd.DataFrame(rows).set_index("run")


def breakdown_table(results_dir: Path, runs: list[str], column: str) -> pd.DataFrame:
    """Mean chunk R@5 per run, split by a question attribute (question_type or doc_group), on `overall`."""
    questions = pd.read_json(resolve_path("eval/questions.jsonl"), lines=True)[["id", "doc_group"]]
    table = {}
    for run in runs:
        _, pq = load_run(results_dir, run)
        pq = pq.merge(questions, on="id")
        pq = pq[~pq["question_type"].isin(["history", "real_pair"])]
        means = pq.groupby(column)["chunk_recall@5"].agg(["mean", "size"])
        table[run] = {f"{g} (n={int(r['size'])})": f"{r['mean']:.3f}" for g, r in means.iterrows()}
    return pd.DataFrame(table).T


def to_markdown(df: pd.DataFrame, columns: list[str]) -> str:
    header = "| run | " + " | ".join(columns) + " |"
    sep = "|---" * (len(columns) + 1) + "|"
    body = [f"| {idx} | " + " | ".join(str(row[c]) for c in columns) + " |" for idx, row in df.iterrows()]
    return "\n".join([header, sep] + body)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("runs", nargs="+", help="first run is the reference (normally baseline)")
    parser.add_argument("--name", required=True)
    args = parser.parse_args()

    results_dir = resolve_path(load_config("configs/default.yaml")["paths"]["results_dir"])
    reference, runs = args.runs[0], args.runs
    table = build_table(results_dir, reference, runs)

    delta_cols = [c for c in table.columns if c.startswith("Δ")]
    level_cols = ["MAIN chunk R@5 (overall)", "chunk R@5 (non_outdated)", "chunk MRR (overall)",
                  "doc R@5 (overall)", "chunk R@30 (overall)", "chunk R@100 (overall)"]
    version_cols = ["fact_stale (outdated, own found set)", "fact_found (outdated)"]
    cost_cols = ["embedded vectors", "vector index MB", "mean search ms", "tokens unseen %", "quotes reachable"]
    descriptions = "\n".join(f"- **{r}**: {first_comment(r)}" for r in runs)
    text = (
        f"# Report: {args.name} (reference: {reference}, tune split)\n\n{descriptions}\n\n"
        "**Pre-registered main metric:** chunk_recall@5 on `overall` (answerable questions except history and "
        "real_pair). The verdict in the first Δ column is the main result. ✅ / ❌ = paired 95% interval excludes "
        "zero; – = no detectable difference. (better/worse counts, n = paired questions.)\n\n"
        f"## Paired differences from {reference}\n\n{to_markdown(table, delta_cols)}\n\n"
        "fact_stale is paired only on outdated questions where BOTH runs retrieved a fact chunk; "
        "lower is better.\n\n"
        f"## Retrieval levels (95% bootstrap intervals)\n\n{to_markdown(table, level_cols)}\n\n"
        "## Version metrics (each run on its own found set; see the paired Δ above for comparisons)\n\n"
        f"{to_markdown(table, version_cols)}\n\n## Cost and diagnostics\n\n{to_markdown(table, cost_cols)}\n")
    repl = replication_table(results_dir, reference, runs)
    if repl is not None:
        text += ("\n## Replication (frozen groups in eval/replication_groups.json)\n\n"
                 "An effect replicates if it has the same sign on the new questions; it is confirmed only if the "
                 "combined interval excludes zero.\n\n" + to_markdown(repl, list(repl.columns)) + "\n")
    for column in ("question_type", "doc_group"):
        bd = breakdown_table(results_dir, runs, column)
        text += f"\n## chunk R@5 by {column} (`overall` questions)\n\n" + to_markdown(bd, list(bd.columns)) + "\n"
    out = results_dir / f"report_{args.name}.md"
    out.write_text(text, encoding="utf-8")
    with pd.option_context("display.width", 300, "display.max_columns", 30, "display.max_colwidth", 48):
        for cols in (delta_cols, level_cols, version_cols, cost_cols):
            print(table[cols].to_string(), "\n")
    print(f"Wrote {out.relative_to(resolve_path('.'))}")


if __name__ == "__main__":
    main()
