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
from src.evaluate import BOOTSTRAP_SAMPLES, bootstrap_ci
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

def generate_all(cfg: dict[str, Any], questions: list[dict[str, Any]], llm=call_llm,
                 log_path: Path | None = None) -> list[dict[str, Any]]:
    """Retrieve, score and generate for each question. The decline threshold is NOT applied here (it is
    applied afterwards for every candidate value), unless the config fixes one.

    With log_path, each entry is appended to it as soon as it is generated, and entries already in the file
    are reused, so a crashed or disconnected run resumes where it stopped (temperature 0, fixed seed)."""
    done: dict[str, dict[str, Any]] = {}
    if log_path is not None and log_path.exists():
        broken = 0
        for line in open(log_path, encoding="utf-8"):
            if line.strip():
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:      # a line cut short by a disconnect: regenerate that answer
                    broken += 1
                    continue
                done[entry["id"]] = entry
        if broken:                                # rewrite without the broken line, so appends start clean
            log_path.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in done.values()),
                                encoding="utf-8")
            print(f"Dropped {broken} incomplete line(s) from {log_path.name}", flush=True)
        if done:
            print(f"Resuming: {len(done)} answers already in {log_path.name}", flush=True)
    bundle = build_indexes(cfg)
    n_ctx = cfg["generation"]["context_chunks"]
    log = []
    sink = open(log_path, "a", encoding="utf-8") if log_path is not None else None
    for i, q in enumerate(questions, start=1):
        if q["id"] in done:
            log.append(done[q["id"]])
            continue
        start = time.perf_counter()
        ids = [cid for cid, _ in retrieve(q["question"], bundle, cfg)][:n_ctx]
        chunks = [bundle.chunks_by_id[cid] for cid in ids]
        score = decline_score(q["question"], chunks[0] if chunks else None, cfg)
        result = generate(q["question"], chunks, cfg, llm=llm, score=score)
        log.append({"id": q["id"], "chunk_ids": ids, "decline_score": score, **result,
                    "latency_s": round(time.perf_counter() - start, 2)})
        print(f"  [{i}/{len(questions)}] {q['id']}: {'DECLINED' if result['declined'] else 'answered'} "
              f"({log[-1]['latency_s']} s)", flush=True)
        if sink is not None:
            sink.write(json.dumps(log[-1], ensure_ascii=False) + "\n")
            sink.flush()
    if sink is not None:
        sink.close()
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


WRONG_DECLINE_MAX = 0.10   # pre-registered guardrail: wrong declines on answerable questions


def balanced_accuracy_ci(df: pd.DataFrame, seed: int = 0) -> tuple[float, float]:
    """95% cluster-bootstrap interval for decline balanced accuracy: whole clusters are resampled and
    both halves (no_answer declined, answerable not declined) recomputed on each resample."""
    if df.empty or not (df["question_type"] == "no_answer").any() or not (df["question_type"] != "no_answer").any():
        return float("nan"), float("nan")
    _, idx = np.unique(df["cluster"].to_numpy(), return_inverse=True)
    na = (df["question_type"] == "no_answer").to_numpy()
    dec = df["declined"].astype(bool).to_numpy()
    n = idx.max() + 1
    na_n, na_dec = np.bincount(idx, weights=na, minlength=n), np.bincount(idx, weights=na & dec, minlength=n)
    an_n, an_ok = np.bincount(idx, weights=~na, minlength=n), np.bincount(idx, weights=~na & ~dec, minlength=n)
    draw = np.random.default_rng(seed).integers(0, n, size=(BOOTSTRAP_SAMPLES, n))
    with np.errstate(invalid="ignore", divide="ignore"):
        ba = (na_dec[draw].sum(1) / na_n[draw].sum(1) + an_ok[draw].sum(1) / an_n[draw].sum(1)) / 2
    ba = ba[~np.isnan(ba)]
    return float(np.percentile(ba, 2.5)), float(np.percentile(ba, 97.5))


def decline_table(df: pd.DataFrame, percentiles: list[float]) -> tuple[pd.DataFrame, dict[float, float]]:
    """Run 10: the LLM-only reference plus each pre-registered percentile threshold, on the same answers."""
    answerable_scores = df.loc[df["question_type"] != "no_answer", "decline_score"].tolist()
    thresholds = percentile_thresholds(answerable_scores, percentiles)
    rows = [{"setting": "no threshold (LLM decides)", "threshold": None, **decline_stats(df),
             **dict(zip(("ba_lo", "ba_hi"), balanced_accuracy_ci(df)))}]
    for p, t in thresholds.items():
        applied = pd.DataFrame([apply_threshold(r, s, t) for r, s in zip(df.to_dict("records"), df["decline_score"])])
        rows.append({"setting": f"p{p:g} of answerable top-1 scores", "threshold": round(t, 4),
                     **decline_stats(applied), **dict(zip(("ba_lo", "ba_hi"), balanced_accuracy_ci(applied)))})
    table = pd.DataFrame(rows)
    table["selected"] = table.index == select_setting(table)
    return table, thresholds


def select_setting(table: pd.DataFrame) -> int | None:
    """Pre-registered rule (Phase 8): among settings with wrong declines <= 10%, take the highest balanced
    accuracy; settings whose interval overlaps the best one's count as tied, and ties go to the lowest
    threshold (it declines least). 'No threshold' is the lowest of all. Returns the row index, or None."""
    ok = table[(table["answerable_wrong_decline"] <= WRONG_DECLINE_MAX) & table["balanced_accuracy"].notna()]
    if ok.empty:
        return None
    best = ok.loc[ok["balanced_accuracy"].idxmax()]
    tied = ok[(ok["ba_hi"] >= best["ba_lo"]) & (ok["ba_lo"] <= best["ba_hi"])] if not np.isnan(best["ba_lo"]) else ok.loc[[best.name]]
    order = tied["threshold"].fillna(-np.inf)
    return int(order.idxmin())


def selected_text(decline: pd.DataFrame) -> str:
    chosen = decline[decline["selected"]]
    if chosen.empty:
        return "none (no setting meets the wrong-decline guardrail, or no no_answer questions in this run)"
    row = chosen.iloc[0]
    return row["setting"] + ("" if pd.isna(row["threshold"]) else f" (threshold {row['threshold']})")


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
            f"Selected by the pre-registered rule: {selected_text(decline)}", "",
            "## Judge validity", "", f"Judge vs code on numeric answers: {agreement}", "",
            "## Citation-following (pre-registered fallback trigger: format < 0.90 or support < 0.70)", "",
            f"Below threshold: {poor or 'none'}", "",
            "## Failure labels", "", str(failures), "",
            "## Answer accuracy by gold position (Limitation 9)", "", md_table(rank_vs_correct.round(3)), ""]
    (out / "summary.md").write_text("\n".join(text), encoding="utf-8")
    print("\n".join(text[4:12]))
    print(f"Decline setting selected: {selected_text(decline)}")
    print(f"Judge agreement: {agreement}\nCitation below threshold: {poor or 'none'}\nFailures: {failures}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("config")
    parser.add_argument("--final", action="store_true", help="allow the one-time test-split run")
    parser.add_argument("--limit", type=int, help="smoke test on the first N questions (written to <run>_smoke)")
    parser.add_argument("--regrade", action="store_true", help="re-grade saved generations.jsonl")
    parser.add_argument("--fresh", action="store_true", help="discard saved generations and start over")
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

    config_text = yaml.safe_dump(cfg, sort_keys=False)
    config_path = out / "config.yaml"
    if args.regrade:
        log = [json.loads(line) for line in open(log_path, encoding="utf-8")]
    else:
        if args.fresh and log_path.exists():
            log_path.unlink()
        if log_path.exists() and config_path.exists() and config_path.read_text(encoding="utf-8") != config_text:
            sys.exit(f"{log_path} was made with a different config; rerun with --fresh to start over.")
        config_path.write_text(config_text, encoding="utf-8")
        log = generate_all(cfg, questions, log_path=log_path)
    config_path.write_text(config_text, encoding="utf-8")
    print("Grading ...", flush=True)
    df = grade_all(cfg, questions, log)
    write_outputs(out, cfg, split, df, questions)
    print(f"Saved to {out.relative_to(resolve_path('.'))}/")


if __name__ == "__main__":
    main()
