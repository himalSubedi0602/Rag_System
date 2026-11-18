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
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.chunking import EMBEDDING_MAX_TOKENS, count_tokens, get_tokenizer, index_text, truncation_stats
from src.config import load_config, resolve_path
from src.evaluate import HEADLINE, aggregate, deep_chunk_recall, evaluate_question, quote_matches, to_frame
from src.index import IndexBundle, build_indexes, make_pieces
from src.retrieve import retrieve, scores_are_similarities, unsupported_settings


def load_questions(cfg: dict[str, Any], split: str) -> list[dict[str, Any]]:
    """Questions from eval/questions.jsonl belonging to one split."""
    with open(resolve_path(cfg["paths"]["questions"]), encoding="utf-8") as f:
        return [q for q in map(json.loads, f) if q["split"] == split]


def quotes_reachable(questions: list[dict[str, Any]], bundle: IndexBundle) -> str:
    """How many gold quotes are inside at least one chunk of this chunking (the ceiling for chunk recall)."""
    by_doc: dict[str, list[str]] = {}
    for c in bundle.chunks_by_id.values():
        by_doc.setdefault(c["doc_id"], []).append(c["text"])
    items = [e for q in questions for e in q["gold_evidence"]]
    ok = sum(any(quote_matches(e["quote"], t) for d in {e["doc_id"], *e.get("acceptable_doc_ids", [])}
                 for t in by_doc.get(d, [])) for e in items)
    return f"{ok}/{len(items)}"


def vector_index_mb(cfg: dict[str, Any], collection_names: list[str]) -> float:
    """On-disk size of the HNSW vector index folders of these Chroma collections (MB).
    Chroma keeps each collection's vector index in a folder named after its VECTOR segment id."""
    chroma_dir = resolve_path(cfg["paths"]["chroma_dir"])
    con = sqlite3.connect(chroma_dir / "chroma.sqlite3")
    marks = ",".join("?" * len(collection_names))
    ids = [r[0] for r in con.execute(
        f"SELECT s.id FROM segments s JOIN collections c ON s.collection = c.id "
        f"WHERE s.scope = 'VECTOR' AND c.name IN ({marks})", collection_names)]
    con.close()
    size = sum(f.stat().st_size for seg in ids for f in (chroma_dir / seg).rglob("*") if f.is_file())
    return round(size / 1e6, 1)


def rerank_truncation(cfg: dict[str, Any], bundle: IndexBundle, questions: list[dict[str, Any]], tokenizer) -> float | None:
    """For reranker / two-stage runs: % of chunks that, together with a median-length question and the
    3 special tokens, exceed the cross-encoder's input limit (so their end is not read). None otherwise."""
    if not (cfg["reranker"]["enabled"] or cfg["retrieval"]["two_stage"]):
        return None
    q_lens = sorted(count_tokens(q["question"], tokenizer) for q in questions)
    q_len = q_lens[len(q_lens) // 2]
    limit = cfg["reranker"]["max_length"] - 3 - q_len
    chunk_lens = [count_tokens(c["text"], tokenizer) for c in bundle.chunks_by_id.values()]
    return round(100 * sum(n > limit for n in chunk_lens) / len(chunk_lens), 1)


def run_info(cfg: dict[str, Any], bundle: IndexBundle, rows: list[dict[str, Any]],
             questions: list[dict[str, Any]]) -> dict[str, Any]:
    """Run-level facts: chunks, how much text the embedding model can't see, quote reachability, speed."""
    tokenizer = get_tokenizer(cfg["chunking"]["tokenizer"])
    if cfg["retrieval"]["small_to_big"]:   # the model embeds pieces, not whole chunks
        texts = [p["text"] for p in make_pieces(list(bundle.chunks_by_id.values()), cfg)]
    else:
        texts = [index_text(c, cfg["chunking"]["add_prefix"]) for c in bundle.chunks_by_id.values()]
    counts = [count_tokens(t, tokenizer) for t in texts]
    trunc = truncation_stats(counts, EMBEDDING_MAX_TOKENS[cfg["embedding"]["model"]])
    return {"chunks": len(bundle.chunks_by_id), "embedded_units": len(counts),
            "quotes_reachable": quotes_reachable(questions, bundle),
            "rerank_truncated_pct": rerank_truncation(cfg, bundle, questions, tokenizer),
            "vector_index_mb": vector_index_mb(cfg, [bundle.collection.name] +
                                               ([bundle.piece_collection.name] if bundle.piece_collection else [])),
            "chunks_truncated_pct": round(trunc["chunks_truncated_pct"], 1),
            "tokens_unseen_pct": round(trunc["tokens_unseen_pct"], 1),
            "mean_latency_ms": round(sum(r["latency_ms"] for r in rows) / len(rows), 1),
            "tolerance_columns": "yes (cosine scores)" if scores_are_similarities(cfg) else "no (rank-only scores)",
            "questions": len(rows)}


def run(cfg: dict[str, Any], split: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], IndexBundle, list[dict[str, Any]]]:
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
        # Primary staleness is by rank for every run; tolerance columns are added only for cosine scores.
        tie_scores = [score for _, score in ranked] if scores_are_similarities(cfg) else None
        row = evaluate_question(q, ids, bundle.chunks_by_id, ks, scores=tie_scores)
        if q["question_type"] != "no_answer":
            # Diagnostic only: a deeper candidate list (top 100). The official metrics above use `ranked`.
            deep_ids = [cid for cid, _ in retrieve(q["question"], bundle, deep_cfg)]
            row.update(deep_chunk_recall(q, deep_ids, bundle.chunks_by_id, depths))
        row["latency_ms"] = latency_ms
        row["cluster"] = q.get("cluster", q["id"])   # linked questions are resampled together
        rows.append(row)
        log.append({**row, "question": q["question"], "gold_doc_ids": q["gold_doc_ids"],
                    "outdated_doc_ids": q["outdated_doc_ids"],
                    "retrieved": [{"rank": i + 1, "chunk_id": cid, "doc_id": bundle.chunks_by_id[cid]["doc_id"],
                                   "is_current": bundle.chunks_by_id[cid]["is_current"], "score": round(score, 4)}
                                  for i, (cid, score) in enumerate(ranked)]})
    return rows, log, bundle, questions


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
        f"- chunks: {info['chunks']} (embedded units: {info['embedded_units']}); truncated by the embedding model: "
        f"{info['chunks_truncated_pct']}% of units, {info['tokens_unseen_pct']}% of tokens never embedded",
        f"- gold quotes reachable in this chunking: {info['quotes_reachable']}",
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
              "stale / fact_stale (by rank): 1 = old version first, 0 = current first, "
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

    rows, log, bundle, questions = run(cfg, split)
    table = aggregate(rows, cfg["eval"]["ks"])
    info = run_info(cfg, bundle, rows, [q for q in questions if q["question_type"] != "no_answer"])

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
