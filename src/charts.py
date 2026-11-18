"""Phase 7 summary charts (tune split). Writes PNGs to eval/results/charts/.

Run:  python -m src.charts

1. phase7_main_metric.png  paired Δ chunk R@5 (overall) vs the original baseline, with cluster 95% intervals
2. phase7_versions.png     version strategies on the final base (hybrid): fact_stale (lower is better) next
                           to the history pass rate (guardrail), as two panels sharing the run axis
Blue, filled = interval excludes zero (significant); grey, hollow = no detectable difference.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from src.compare import load_run, paired  # noqa: E402
from src.config import load_config, resolve_path  # noqa: E402

BLUE, GREY, INK, MUTED, SURFACE = "#2a78d6", "#898781", "#0b0b0b", "#52514e", "#fcfcfb"

MAIN_RUNS = [("bge", "bge-small (5)"), ("small2big", "small-to-big (2b)"), ("bge_prefix", "bge + prefix (6p)"),
             ("cap2", "cap 2 per group (6b)"), ("twostage", "two-stage (12)"), ("rerank30", "reranker top 30 (7)"),
             ("rerank100", "reranker top 100 (7b)"), ("hybrid", "hybrid RRF k=60 (6)"),
             ("hybrid_rerank30", "hybrid + reranker 30 (4b)"), ("hybrid_v9w10", "FINAL: hybrid + date w=0.1")]
VERSION_RUNS = [("hybrid", "base: hybrid"), ("hybrid_v8", "8 exclude superseded"),
                ("hybrid_v8b", "8b exclude legacy"), ("hybrid_v9w10", "9 date w=0.1 (chosen)"),
                ("hybrid_v9w25", "9 date w=0.25"), ("hybrid_v9w50", "9 date w=0.5"), ("hybrid_v9b", "9b version swap")]


def style(ax) -> None:
    ax.set_facecolor(SURFACE)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelcolor=INK, length=0)
    ax.grid(axis="x", color="#e6e5e0", linewidth=0.8)
    ax.set_axisbelow(True)


def interval_row(ax, y: float, mid: float, lo: float, hi: float, significant: bool, label: str) -> None:
    color = BLUE if significant else GREY
    ax.plot([lo, hi], [y, y], color=color, linewidth=2, solid_capstyle="round")
    ax.plot(mid, y, "o", markersize=8, color=color, markerfacecolor=color if significant else SURFACE,
            markeredgewidth=2)
    ax.text(hi, y, f"  {label}", va="center", fontsize=9, color=INK)


def main_metric_chart(results: Path, out: Path) -> None:
    _, ref = load_run(results, "baseline")
    fig, ax = plt.subplots(figsize=(8.5, 5.2), facecolor=SURFACE)
    style(ax)
    for y, (run, name) in enumerate(MAIN_RUNS):
        _, pq = load_run(results, run)
        d = paired(ref, pq, "overall").loc["chunk_recall@5"]
        lo, hi = (float(x) for x in d["95% CI of diff"].strip("[]").split(","))
        interval_row(ax, y, d["mean_diff (B-A)"], lo, hi, lo > 0, f"{d['mean_diff (B-A)']:+.3f}")
    ax.axvline(0, color=MUTED, linewidth=1)
    ax.set_yticks(range(len(MAIN_RUNS)), [n for _, n in MAIN_RUNS])
    ax.set_xlabel("Δ chunk recall@5 vs original baseline (overall, n=126; cluster 95% interval)", color=MUTED)
    ax.set_title("Phase 7: retrieval changes vs the baseline (tune split)", loc="left", color=INK, fontsize=12)
    ax.text(0, -0.13, "Filled blue = interval excludes zero; hollow grey = no detectable difference.",
            transform=ax.transAxes, fontsize=8.5, color=MUTED)
    ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(out / "phase7_main_metric.png", dpi=160)
    plt.close(fig)


def version_chart(results: Path, out: Path) -> None:
    _, base = load_run(results, "hybrid")
    fig, (left, right) = plt.subplots(1, 2, figsize=(10, 4.4), sharey=True, facecolor=SURFACE)
    for ax in (left, right):
        style(ax)
    for y, (run, _) in enumerate(VERSION_RUNS):
        m = pd.read_csv(results / run / "metrics.csv", index_col=0)
        _, pq = load_run(results, run)
        o, h = m.loc["outdated_version"], m.loc["history"]
        sig_stale = sig_hist = False
        if run != "hybrid":
            ds = paired(base, pq, "outdated_version").loc["fact_stale"]
            dh = paired(base, pq, "history").loc["chunk_recall@5"]
            sig_stale = float(ds["95% CI of diff"].strip("[]").split(",")[1]) < 0      # significantly lower
            sig_hist = float(dh["95% CI of diff"].strip("[]").split(",")[1]) < 0       # significantly lower
        interval_row(left, y, o["fact_stale"], o["fact_stale_lo"], o["fact_stale_hi"], sig_stale,
                     f"{o['fact_stale']:.2f}")
        interval_row(right, y, h["chunk_recall@5"], h["chunk_recall@5_lo"], h["chunk_recall@5_hi"], sig_hist,
                     f"{h['chunk_recall@5']:.2f}")
    left.set_yticks(range(len(VERSION_RUNS)), [n for _, n in VERSION_RUNS])
    left.invert_yaxis()
    left.set_xlim(-0.05, 1.15)
    right.set_xlim(-0.05, 1.15)
    left.set_title("fact_stale by rank (lower is better)\nblue = significantly lower than base", loc="left",
                   color=INK, fontsize=10)
    right.set_title("History pass rate, chunk R@5 (guardrail)\nblue = significantly lower than base (fails)",
                    loc="left", color=INK, fontsize=10)
    fig.suptitle("Version strategies on the final base (hybrid), tune split", x=0.01, ha="left", color=INK,
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(out / "phase7_versions.png", dpi=160)
    plt.close(fig)


def main() -> None:
    results = resolve_path(load_config("configs/default.yaml")["paths"]["results_dir"])
    out = results / "charts"
    out.mkdir(exist_ok=True)
    main_metric_chart(results, out)
    version_chart(results, out)
    print(f"Wrote {out.relative_to(resolve_path('.'))}/phase7_main_metric.png and phase7_versions.png")


if __name__ == "__main__":
    main()
