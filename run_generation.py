"""Phase 8: generate answers for every question of a split and grade them.

Run:
    python run_generation.py configs/gen_llama.yaml             tune split (default)
    python run_generation.py configs/gen_llama.yaml --limit 5   quick smoke test on 5 questions (not a result)
    python run_generation.py configs/gen_llama.yaml --regrade   re-grade saved generations without the generator
    python run_generation.py configs/<final>.yaml --final       the ONE pre-registered test-split run

Writes eval/results/<run_name>/:
  generations.jsonl   question, retrieved chunk ids, decline score, raw LLM output   (git-ignored log)
  per_question.csv    grading per question (answer text included)                     (committed)
  metrics.csv         per group, with cluster 95% intervals                            (committed)
  decline.csv         run 10: every candidate threshold, applied to the same answers  (committed)
  judge_audit.md      30 judge decisions to check by hand                              (committed)
  summary.md          readable report                                                  (committed)
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

from run_experiment import load_questions
from src.config import load_config, resolve_path
from src.evaluate import bootstrap_ci
from src.generate import call_llm, decline_score, generate, percentile_thresholds
from src.grade import apply_threshold, grade
from src.index import build_indexes
from src.retrieve import retrieve, unsupported_settings

SANITY = {"history", "real_pair"}
GROUPS = {
    "overall": lambda t: ~t.isin(SANITY | {"no_answer"}),          # MAIN: answerable except sanity types
    "non_outdated": lambda t: ~t.isin(SANITY | {"no_answer", "outdated_version"}),
    "outdated_version": lambda t: t == "outdated_version",
    "history": lambda t: t == "history",
    "no_answer": lambda t: t == "no_answer",
}
AUDIT_SIZE = 30
CITATION_POOR = {"cit_format": 0.90, "cit_supported": 0.70}   # pre-registered fallback trigger


# ---------------------------------------------------------------------------
# Generation pass
# ---------------------------------------------------------------------------

def generate_all(cfg: dict[str, Any], questions: list[dict[str, Any]], llm=call_llm) -> list[dict[str, Any]]:
    """Retrieve, score and generate for each question. The decline threshold is NOT applied here (it is
    applied afterwards for every candidate value), unless the config fixes one."""
    bundle = build_indexes(cfg)
    n_ctx = cfg["generation"]["context_chunks"]
    log = []
    for i, q in enumerate(questions, start=1):
        start = time.perf_counter()
        ids = [cid for cid, _ in retrieve(q["question"], bundle, cfg)][:n_ctx]
        chunks = [bundle.chunks_by_id[cid] for cid in ids]
        score = decline_score(q["question"], chunks[0] if chunks else None, cfg)
        result = generate(q["question"], chunks, cfg, llm=llm, score=score)
        log.append({"id": q["id"], "chunk_ids": ids, "decline_score": score, **result,
                    "latency_s": round(time.perf_counter() - start, 2)})
        print(f"  [{i}/{len(questions)}] {q['id']}: {'DECLINED' if result['declined'] else 'answered'} "
              f"({log[-1]['latency_s']} s)", flush=True)
    return log


def grade_all(cfg: dict[str, Any], questions: list[dict[str, Any]], log: list[dict[str, Any]],
              judge_llm=call_llm) -> pd.DataFrame:
    bundle_chunks = load_chunk_lookup(cfg)
    by_id = {q["id"]: q for q in questions}
    rows = []
    for entry in log:
        q = by_id[entry["id"]]
        chunks = [bundle_chunks[cid] for cid in entry["chunk_ids"]]
        row = grade(q, entry, chunks, cfg, judge_llm)
        row.update(decline_score=entry["decline_score"], cluster=q.get("cluster", q["id"]),
                   latency_s=entry.get("latency_s"))
        rows.append(row)
    return pd.DataFrame(rows)


def load_chunk_lookup(cfg: dict[str, Any]) -> dict[str, dict[str, Any]]:
    from src.index import load_or_create_chunks
    return {c["chunk_id"]: c for c in load_or_create_chunks(cfg)}


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def mean_ci(values: pd.Series, clusters: pd.Series) -> tuple[float, float, float, int]:
    mask = values.notna()
    v = values[mask].astype(float).to_numpy()
    if len(v) == 0:
        return float("nan"), float("nan"), float("nan"), 0
    lo, hi = bootstrap_ci(v, clusters[mask].to_numpy())
    return float(v.mean()), lo, hi, len(v)


def metrics_table(df: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for name, select in GROUPS.items():
        g = df[select(df["question_type"])]
        if g.empty:
            continue
        entry: dict[str, Any] = {"n": len(g)}
        cols = ["correct", "declined"] + [c for c in ("cit_format", "cit_supported", "stale_answer") if c in g]
        for col in cols:
            m, lo, hi, n = mean_ci(g[col].astype("float"), g["cluster"])
            entry.update({col: m, f"{col}_lo": lo, f"{col}_hi": hi, f"{col}_n": n})
        rows[name] = entry
    return pd.DataFrame(rows).T


def decline_stats(df: pd.DataFrame) -> dict[str, float]:
    answerable = df[df["question_type"] != "no_answer"]
    no_answer = df[df["question_type"] == "no_answer"]
    declined_na = no_answer["declined"].mean() if len(no_answer) else float("nan")
    wrong = answerable["declined"].mean() if len(answerable) else float("nan")
    overall = df[GROUPS["overall"](df["question_type"])]
    return {"no_answer_declined": declined_na, "answerable_wrong_decline": wrong,
            "balanced_accuracy": (declined_na + (1 - wrong)) / 2, "overall_accuracy": overall["correct"].mean()}


def decline_table(df: pd.DataFrame, percentiles: list[float]) -> tuple[pd.DataFrame, dict[float, float]]:
    """Run 10: the LLM-only reference plus each pre-registered percentile threshold, on the same answers."""
    answerable_scores = df.loc[df["question_type"] != "no_answer", "decline_score"].tolist()
    thresholds = percentile_thresholds(answerable_scores, percentiles)
    rows = [{"setting": "no threshold (LLM decides)", "threshold": None, **decline_stats(df)}]
    for p, t in thresholds.items():
        applied = pd.DataFrame([apply_threshold(r, s, t) for r, s in zip(df.to_dict("records"), df["decline_score"])])
        rows.append({"setting": f"p{p:g} of answerable top-1 scores", "threshold": round(t, 4), **decline_stats(applied)})
    return pd.DataFrame(rows), thresholds


def judge_agreement(df: pd.DataFrame) -> dict[str, Any]:
    both = df[(df["method"] == "code") & df["judge_correct"].notna()]
    unparsed = int(((df["method"] == "judge") & df["judge_correct"].isna()).sum())
    if both.empty:
        return {"n": 0, "agreement": float("nan"), "judge_unparsed": unparsed}
    agree = (both["judge_correct"].astype(bool) == both["correct"].astype(bool))
    return {"n": len(both), "agreement": float(agree.mean()),
            "judge_says_correct_code_says_wrong": int((both["judge_correct"].astype(bool) & ~both["correct"].astype(bool)).sum()),
            "judge_says_wrong_code_says_correct": int((~both["judge_correct"].astype(bool) & both["correct"].astype(bool)).sum()),
            "judge_unparsed": unparsed}


def audit_sample(df: pd.DataFrame, questions: dict[str, dict[str, Any]], seed: int) -> str:
    """30 judge decisions for the hand audit: judge-decided (non-numeric) answers first, then numeric ones."""
    judged = df[df["judge_correct"].notna()]
    primary = judged[judged["method"] == "judge"]
    rest = judged[judged["method"] == "code"]
    rng = random.Random(seed)
    ids = rng.sample(list(primary["id"]), min(AUDIT_SIZE, len(primary)))
    if len(ids) < AUDIT_SIZE:
        ids += rng.sample(list(rest["id"]), min(AUDIT_SIZE - len(ids), len(rest)))
    lines = ["# Judge audit sample (hand-check each verdict; fill in 'my reading')", "",
             "| # | id | method | question | expected | answer | judge | my reading |", "|---|---|---|---|---|---|---|---|"]
    for n, qid in enumerate(ids, start=1):
        r = df[df["id"] == qid].iloc[0]
        q = questions[qid]
        clean = lambda s: str(s).replace("|", "/").replace("\n", " ")
        lines.append(f"| {n} | {qid} | {r['method']} | {clean(q['question'])} | {clean(q['expected_answer'])} | "
                     f"{clean(r['answer'])} | {'CORRECT' if r['judge_correct'] else 'INCORRECT'} | |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def md_table(df: pd.DataFrame, index: bool = True) -> str:
    """Plain markdown table (no extra package)."""
    cols = ([df.index.name or ""] if index else []) + [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|---" * len(cols) + "|"]
    for idx, row in df.iterrows():
        cells = ([str(idx)] if index else []) + ["" if pd.isna(v) else str(v) for v in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_outputs(out: Path, cfg: dict[str, Any], split: str, df: pd.DataFrame,
                  questions: list[dict[str, Any]]) -> None:
    metrics = metrics_table(df)
    decline, thresholds = decline_table(df, cfg["generation"]["decline_percentiles"])
    agreement = judge_agreement(df)
    overall = metrics.loc["overall"] if "overall" in metrics.index else None
    poor = {k: float(overall[k]) for k in CITATION_POOR if overall is not None and k in overall
            and not pd.isna(overall[k]) and float(overall[k]) < CITATION_POOR[k]}
    df.to_csv(out / "per_question.csv", index=False)
    metrics.round(4).to_csv(out / "metrics.csv")
    decline.round(4).to_csv(out / "decline.csv", index=False)
    (out / "judge_audit.md").write_text(audit_sample(df, {q["id"]: q for q in questions}, cfg["seed"]),
                                        encoding="utf-8")
    failures = df["failure"].value_counts().to_dict()
    rank_vs_correct = (df[df["gold_rank"].notna() & ~df["declined"] & GROUPS["overall"](df["question_type"])]
                       .assign(rank_bucket=lambda d: np.where(d["gold_rank"] == 1, "gold at rank 1", "gold at rank 2-5"))
                       .groupby("rank_bucket")["correct"].agg(["mean", "size"]))
    text = [f"# Generation run: {cfg['run_name']} ({split} split)", "",
            f"Generator `{cfg['generation']['model']}`, judge `{cfg['generation']['judge_model']}`"
            + (" (SELF-GRADED: judge = generator)" if cfg['generation']['model'] == cfg['generation']['judge_model'] else "")
            + f", prompt v{cfg['generation']['prompt_version']}, {cfg['generation']['context_chunks']} chunks.", "",
            "## Metrics by group (cluster 95% intervals)", "", md_table(metrics.round(3)), "",
            "## Decline (run 10: candidate thresholds applied to the same answers)", "",
            md_table(decline.round(3), index=False), "",
            "## Judge validity", "", f"Judge vs code on numeric answers: {agreement}", "",
            "## Citation-following (pre-registered fallback trigger: format < 0.90 or support < 0.70)", "",
            f"Below threshold: {poor or 'none'}", "",
            "## Failure labels", "", str(failures), "",
            "## Answer accuracy by gold position (Limitation 9)", "", md_table(rank_vs_correct.round(3)), ""]
    (out / "summary.md").write_text("\n".join(text), encoding="utf-8")
    print("\n".join(text[4:12]))
    print(f"Judge agreement: {agreement}\nCitation below threshold: {poor or 'none'}\nFailures: {failures}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("config")
    parser.add_argument("--final", action="store_true", help="allow the one-time test-split run")
    parser.add_argument("--limit", type=int, help="smoke test on the first N questions (written to <run>_smoke)")
    parser.add_argument("--regrade", action="store_true", help="re-grade saved generations.jsonl")
    args = parser.parse_args()

    cfg = load_config(args.config)
    split = cfg["eval"]["split"]
    if split == "test" and not args.final:
        sys.exit("Refusing to run on the TEST split without --final.")
    if problems := unsupported_settings(cfg):
        sys.exit(f"Config uses features not implemented: {', '.join(problems)}")
    questions = load_questions(cfg, split)
    name = cfg["run_name"] + ("_smoke" if args.limit else "")
    if args.limit:
        questions = questions[:args.limit]
    out = resolve_path(cfg["paths"]["results_dir"]) / name
    out.mkdir(parents=True, exist_ok=True)
    log_path = out / "generations.jsonl"

    if args.regrade:
        log = [json.loads(line) for line in open(log_path, encoding="utf-8")]
    else:
        log = generate_all(cfg, questions)
        with open(log_path, "w", encoding="utf-8") as f:
            for entry in log:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    (out / "config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    print("Grading ...", flush=True)
    df = grade_all(cfg, questions, log)
    write_outputs(out, cfg, split, df, questions)
    print(f"Saved to {out.relative_to(resolve_path('.'))}/")


if __name__ == "__main__":
    main()
