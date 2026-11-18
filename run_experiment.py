"""Run one retrieval experiment and save its results.

Usage:  python run_experiment.py configs/baseline.yaml
        python run_experiment.py configs/<final>.yaml --final    (only for the one-time test-split run)

Saves to eval/results/<run_name>/:
  config.yaml          the exact merged config (so the run can be reproduced)
  metrics.csv          overall + per-type metrics with 95% bootstrap CIs   (committed)
  per_question.csv     every question's metrics, for paired comparisons     (committed)
  run_info.yaml        chunk count, truncation %, latency                    (committed)
  summary.md           readable report incl. misses and stale cases          (committed)
  per_question.jsonl   full ranking, scores and timing per question          (git-ignored log)
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.chunking import EMBEDDING_MAX_TOKENS, count_tokens, get_tokenizer, index_text, truncation_stats
from src.config import load_config, resolve_path
from src.evaluate import HEADLINE, aggregate, deep_chunk_recall, evaluate_question, to_frame
from src.index import IndexBundle, build_indexes
from src.retrieve import retrieve, unsupported_settings


def load_questions(cfg: dict[str, Any], split: str) -> list[dict[str, Any]]:
    """Questions from eval/questions.jsonl belonging to one split."""
    with open(resolve_path(cfg["paths"]["questions"]), encoding="utf-8") as f:
        return [q for q in map(json.loads, f) if q["split"] == split]


def run_info(cfg: dict[str, Any], bundle: IndexBundle, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Run-level facts: how many chunks, how much text the embedding model can't see, speed."""
    tokenizer = get_tokenizer(cfg["chunking"]["tokenizer"])
    counts = [count_tokens(index_text(c, cfg["chunking"]["add_prefix"]), tokenizer)
              for c in bundle.chunks_by_id.values()]
    trunc = truncation_stats(counts, EMBEDDING_MAX_TOKENS[cfg["embedding"]["model"]])
    return {"chunks": len(counts),
            "chunks_truncated_pct": round(trunc["chunks_truncated_pct"], 1),
            "tokens_unseen_pct": round(trunc["tokens_unseen_pct"], 1),
            "mean_latency_ms": round(sum(r["latency_ms"] for r in rows) / len(rows), 1),
            "questions": len(rows)}


def run(cfg: dict[str, Any], split: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], IndexBundle]:
    """Retrieve for every question; return (metric rows, full log rows, the index bundle)."""
    bundle = build_indexes(cfg)
    questions = load_questions(cfg, split)
    ks = cfg["eval"]["ks"]
    rows, log = [], []
    depths = cfg["eval"]["diagnostic_depths"]
    deep_cfg = {**cfg, "retrieval": {**cfg["retrieval"], "top_k_each": max(depths)}}
    for q in questions:
        start = time.perf_counter()
        ranked = retrieve(q["question"], bundle, cfg)
        latency_ms = 1000 * (time.perf_counter() - start)
        ids = [cid for cid, _ in ranked]
        row = evaluate_question(q, ids, bundle.chunks_by_id, ks, scores=[score for _, score in ranked])
        if q["question_type"] != "no_answer":
            # Diagnostic only: a deeper candidate list (top 100). The official metrics above use `ranked`.
            deep_ids = [cid for cid, _ in retrieve(q["question"], bundle, deep_cfg)]
            row.update(deep_chunk_recall(q, deep_ids, bundle.chunks_by_id, depths))
        row["latency_ms"] = latency_ms
        rows.append(row)
        log.append({**row, "question": q["question"], "gold_doc_ids": q["gold_doc_ids"],
                    "outdated_doc_ids": q["outdated_doc_ids"],
                    "retrieved": [{"rank": i + 1, "chunk_id": cid, "doc_id": bundle.chunks_by_id[cid]["doc_id"],
                                   "is_current": bundle.chunks_by_id[cid]["is_current"], "score": round(score, 4)}
                                  for i, (cid, score) in enumerate(ranked)]})
    return rows, log, bundle


def fmt(value: Any) -> str:
    """Format a metric for a markdown table."""
    if isinstance(value, float):
        return "" if pd.isna(value) else f"{value:.3f}"
    return str(value)


def markdown_table(df: pd.DataFrame) -> str:
    """Small markdown table writer (avoids an extra dependency)."""
    header = "| group | " + " | ".join(df.columns) + " |"
    sep = "|---" * (len(df.columns) + 1) + "|"
    body = ["| " + str(idx) + " | " + " | ".join(fmt(v) for v in row) + " |" for idx, row in df.iterrows()]
    return "\n".join([header, sep] + body)


def with_ci(table: pd.DataFrame, metric: str) -> pd.Series:
    """'0.458 [0.323, 0.604]' strings for one headline metric."""
    return table.apply(lambda r: "" if pd.isna(r[metric]) else
                       f"{r[metric]:.3f} [{r[metric + '_lo']:.2f}, {r[metric + '_hi']:.2f}]", axis=1)


def headline_table(table: pd.DataFrame) -> pd.DataFrame:
    """Compact view: n, headline metrics with 95% CIs, plus recall@1 at both levels."""
    view = pd.DataFrame({"n": table["n"].astype(int),
                         "doc_R@1": table["doc_recall@1"], "chunk_R@1": table["chunk_recall@1"],
                         "chunk_R@30": table["chunk_recall@30"], "chunk_R@100": table["chunk_recall@100"]})
    for metric in HEADLINE:
        view[metric] = with_ci(table, metric)
    return view


def write_summary(path: Path, cfg: dict[str, Any], split: str, table: pd.DataFrame, log: list[dict[str, Any]],
                  info: dict[str, Any]) -> None:
    """Readable report: settings, metrics, questions missed in the top 5, stale cases."""
    c, r = cfg["chunking"], cfg["retrieval"]
    lines = [
        f"# Run: {cfg['run_name']}", "",
        f"- split: **{split}** ({sum(1 for x in log)} questions; no_answer excluded from retrieval metrics)",
        f"- chunking: {c['strategy']} size={c['chunk_size']} overlap={c['chunk_overlap']} prefix={c['add_prefix']}",
        f"- embedding: {cfg['embedding']['model']}",
        f"- retrieval: mode={r['mode']} top_k={r['top_k_each']} version_filter={r['version_filter']} "
        f"date_aware={r['date_aware_rerank']} reranker={cfg['reranker']['enabled']}",
        f"- chunks: {info['chunks']}; truncated by the embedding model: {info['chunks_truncated_pct']}% of chunks, "
        f"{info['tokens_unseen_pct']}% of tokens never embedded",
        f"- run at: {datetime.now().strftime('%Y-%m-%d %H:%M')}", "",
        "## Headline metrics (95% bootstrap intervals in brackets)", "",
        "Retrieval: **chunk_recall@5** (main), chunk_mrr; doc_recall@5 is a lenient upper bound. "
        "Versions: **fact_stale** (main; only questions where a fact chunk was retrieved) with **fact_found**; "
        "doc-level stale is secondary.", "",
        "`overall` = answerable questions except history/real_pair; `non_outdated` = overall minus outdated_version.", "",
        markdown_table(headline_table(table)), "",
        "## All metrics", "", markdown_table(table[[c for c in table.columns if not c.endswith(("_lo", "_hi"))]]), "",
        "## Answerable questions with no gold document in the top 5", "",
        "| id | type | gold doc rank (of 30) | top-1 retrieved doc | question |", "|---|---|---|---|---|",
    ]
    for x in log:
        if x["question_type"] not in ("no_answer", "history") and (x.get("gold_doc_rank") or 99) > 5:
            top1 = x["retrieved"][0]["doc_id"] if x["retrieved"] else ""
            lines.append(f"| {x['id']} | {x['question_type']} | {x.get('gold_doc_rank') or 'not found'} | "
                         f"{top1} | {x['question']} |")
    lines += ["", "## Outdated-version questions", "",
              "stale / fact_stale: 1 = old version first, 0.5 = exact score tie, 0 = current first, "
              "blank = neither version retrieved.", "",
              "| id | first current doc rank | first old doc rank | stale | fact_stale |", "|---|---|---|---|---|"]
    for x in log:
        if x["question_type"] != "outdated_version":
            continue
        ranks = x["retrieved"]
        cur = next((d["rank"] for d in ranks if d["doc_id"] in x["gold_doc_ids"]), "-")
        old = next((d["rank"] for d in ranks if d["doc_id"] in x["outdated_doc_ids"]), "-")
        lines.append(f"| {x['id']} | {cur} | {old} | {fmt(x.get('stale'))} | {fmt(x.get('fact_stale'))} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("config")
    parser.add_argument("--final", action="store_true", help="allow running on the held-out test split")
    args = parser.parse_args()

    cfg = load_config(args.config)
    split = cfg["eval"]["split"]
    if split == "test" and not args.final:
        sys.exit("Refusing to run on the TEST split without --final. Tune on 'tune'; use test once, at the end.")
    if problems := unsupported_settings(cfg):
        sys.exit(f"Config uses features not implemented yet: {', '.join(problems)}")

    rows, log, bundle = run(cfg, split)
    table = aggregate(rows, cfg["eval"]["ks"])
    info = run_info(cfg, bundle, rows)

    out = resolve_path(cfg["paths"]["results_dir"]) / cfg["run_name"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    table.round(4).to_csv(out / "metrics.csv")
    to_frame(rows, cfg["eval"]["ks"]).round(4).to_csv(out / "per_question.csv", index=False)
    (out / "run_info.yaml").write_text(yaml.safe_dump(info, sort_keys=False), encoding="utf-8")
    with open(out / "per_question.jsonl", "w", encoding="utf-8") as f:
        for entry in log:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    write_summary(out / "summary.md", cfg, split, table, log, info)

    print(f"\nRun '{cfg['run_name']}' on {split} split: {len(rows)} questions, "
          f"mean retrieval latency {info['mean_latency_ms']:.0f} ms, "
          f"{info['tokens_unseen_pct']}% of chunk tokens never embedded")
    with pd.option_context("display.width", 250, "display.max_columns", 20):
        print(headline_table(table).round(3).to_string())
    print(f"\nSaved to {out.relative_to(resolve_path('.'))}/")


if __name__ == "__main__":
    main()
