"""Phase 8 report from a graded results folder: the chosen system's metrics, the failure report with
examples, the Limitation 9 check and the hand-audit tally, as markdown ready for NOTES.md and the README.

Run:  python -m src.report_gen gen_llama      (also gen_final, after the test run)
Writes eval/results/<run>/report.md and prints it. Reads saved files only: no model is loaded.

"Chosen system" = the LLM answers with the decline threshold chosen by the pre-registered run-10 rule applied
(for the final run the threshold is already fixed in its config, so nothing changes). The LLM-only accuracy is
shown next to it. Only pre-registered metrics are reported.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.config import load_config, resolve_path
from src.grade import apply_threshold

FAILURE_ORDER = ["answered_no_answer", "wrong_decline", "retrieval_miss", "stale_fact", "hallucination",
                 "ignored_context"]
FAILURE_MEANING = {
    "answered_no_answer": "answered a no_answer question instead of declining",
    "wrong_decline": "declined an answerable question",
    "retrieval_miss": "no gold chunk in the top 5",
    "stale_fact": "stated the old value",
    "hallucination": "no usable citation, or cites no chunk with the gold quote",
    "ignored_context": "gold chunk in the top 5, cited, but the answer is wrong",
}
AGREE = {"agree", "a", "yes", "y", "ok", "✓", "✔", "correct"}
DISAGREE = {"disagree", "d", "no", "n", "✗", "✘", "x", "wrong"}
EXAMPLES_PER_LABEL = 2


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_records(folder: Path) -> list[dict[str, Any]]:
    """per_question.csv as dicts, with blanks as None (grade.failure_label tests `is None`)."""
    df = pd.read_csv(folder / "per_question.csv")
    return df.astype(object).where(df.notna(), None).to_dict("records")


def chosen_threshold(folder: Path, saved_cfg: dict[str, Any]) -> tuple[str, float | None, bool]:
    """(description, threshold, already_applied). A threshold fixed in the run's config (the final run) was
    applied during generation; otherwise the run-10 selection from decline.csv is used."""
    fixed = saved_cfg["generation"].get("decline_threshold")
    if fixed is not None:
        return f"fixed in the run config ({fixed!r})", float(fixed), True
    from src.final_config import selected_setting
    try:
        setting, threshold = selected_setting(folder)
    except ValueError as err:
        return f"none ({err})", None, False
    return setting + ("" if threshold is None else f" (threshold {threshold:.4f})"), threshold, False


def system_records(records: list[dict[str, Any]], threshold: float | None) -> list[dict[str, Any]]:
    """The chosen system's rows: each LLM answer, replaced by a decline if its score is below the threshold."""
    return [apply_threshold(r, r["decline_score"], threshold) for r in records]


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def frame(records: list[dict[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(records)
    df["declined"] = df["declined"].astype(bool)
    return df


def ci(row: pd.Series, col: str) -> str:
    if col not in row or pd.isna(row[col]):
        return ""
    return f"{row[col]:.3f} [{row[col + '_lo']:.2f}, {row[col + '_hi']:.2f}]"


def metrics_section(system: pd.DataFrame, llm_only: pd.DataFrame) -> str:
    from run_generation import metrics_table
    m, base = metrics_table(system), metrics_table(llm_only)
    lines = ["| group | n | answer accuracy | declined | citation format | citation support | stale answer |",
             "|---|---|---|---|---|---|---|"]
    for group in ["overall", "non_outdated", "outdated_version", "history", "no_answer"]:
        if group in m.index:
            r = m.loc[group]
            lines.append(f"| {group} | {int(r['n'])} | {ci(r, 'correct')} | {ci(r, 'declined')} | "
                         f"{ci(r, 'cit_format')} | {ci(r, 'cit_supported')} | {ci(r, 'stale_answer')} |")
    note = ""
    if "overall" in m.index and "overall" in base.index:
        note = (f"\nAnswer accuracy on `overall`: chosen system **{m.loc['overall', 'correct']:.3f}**, "
                f"LLM deciding alone {base.loc['overall', 'correct']:.3f}.\n")
    return "\n".join(lines) + "\n" + note


def decline_section(system: pd.DataFrame) -> str:
    answerable, no_answer = system[system["question_type"] != "no_answer"], system[system["question_type"] == "no_answer"]
    na = no_answer["declined"].mean() if len(no_answer) else float("nan")
    wrong = answerable["declined"].mean() if len(answerable) else float("nan")
    return (f"no_answer declined: {na:.3f} (n = {len(no_answer)}) | answerable wrongly declined: {wrong:.3f} "
            f"(n = {len(answerable)}) | balanced accuracy: {(na + 1 - wrong) / 2:.3f}\n")


def short(text: Any, limit: int = 160) -> str:
    s = " ".join(str(text or "").split()).replace("|", "/")
    return s if len(s) <= limit else s[:limit - 1] + "…"


def failure_section(system: pd.DataFrame, questions: dict[str, dict[str, Any]],
                    n_examples: int = EXAMPLES_PER_LABEL) -> str:
    """Counts per failure label (first matching rule wins, as pre-registered) and examples for each."""
    wrong = system[system["failure"].notna()]
    total = len(wrong)
    lines = [f"{total} wrong answers of {len(system)} questions.", "",
             "| label | meaning | count | share of wrong |", "|---|---|---|---|"]
    for label in FAILURE_ORDER:
        count = int((wrong["failure"] == label).sum())
        share = f"{count / total:.2f}" if total else ""
        lines.append(f"| {label} | {FAILURE_MEANING[label]} | {count} | {share} |")
    for label in FAILURE_ORDER:
        rows = wrong[wrong["failure"] == label].sort_values("id").head(n_examples)
        if rows.empty:
            continue
        lines += ["", f"**{label}** examples:", "", "| id | question | expected | answer | gold rank |",
                  "|---|---|---|---|---|"]
        for _, r in rows.iterrows():
            q = questions.get(r["id"], {})
            rank = "" if pd.isna(r.get("gold_rank")) else int(r["gold_rank"])
            lines.append(f"| {r['id']} | {short(q.get('question'))} | {short(q.get('expected_answer'), 100)} | "
                         f"{short(r['answer'])} | {rank} |")
    return "\n".join(lines) + "\n"


def rank_section(llm_only: pd.DataFrame) -> str:
    """Limitation 9 as pre-registered: answer accuracy when the gold chunk is at rank 1 vs rank 3-5
    (rank 2 shown for completeness). LLM answers that were not declined, `overall` questions."""
    from run_generation import GROUPS, mean_ci
    d = llm_only[GROUPS["overall"](llm_only["question_type"]) & ~llm_only["declined"] & llm_only["gold_rank"].notna()]
    buckets = {"rank 1": d["gold_rank"] == 1, "rank 2": d["gold_rank"] == 2, "rank 3-5": d["gold_rank"] >= 3}
    lines = ["| gold chunk at | n | answer accuracy [95% CI] |", "|---|---|---|"]
    for name, mask in buckets.items():
        sub = d[mask]
        if sub.empty:
            lines.append(f"| {name} | 0 | |")
            continue
        mean, lo, hi, n = mean_ci(sub["correct"].astype(float), sub["cluster"])
        lines.append(f"| {name} | {n} | {mean:.3f} [{lo:.2f}, {hi:.2f}] |")
    return "\n".join(lines) + "\n"


def judge_section(llm_only: pd.DataFrame) -> str:
    from run_generation import judge_agreement
    a = judge_agreement(llm_only)
    if not a["n"]:
        return f"No numeric answers graded by both (judge unparsed: {a['judge_unparsed']}).\n"
    return (f"Judge vs code on {a['n']} numeric answers: agreement **{a['agreement']:.3f}**; judge says correct "
            f"where code says wrong: {a['judge_says_correct_code_says_wrong']}; judge says wrong where code says "
            f"correct: {a['judge_says_wrong_code_says_correct']}; judge replies not parsed: {a['judge_unparsed']}.\n")


def audit_tally(path: Path) -> str:
    """Counts of the hand marks in judge_audit.md (last column: agree / disagree, or a/d, ✓/✗, yes/no)."""
    if not path.exists():
        return "judge_audit.md not found.\n"
    marks = []
    for line in open(path, encoding="utf-8"):
        if not line.startswith("| ") or line.startswith("| #"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8 or not cells[0].isdigit():
            continue
        mark = cells[-1].lower()
        kind = "agree" if mark in AGREE else "disagree" if mark in DISAGREE else "unmarked" if not mark else "unclear"
        marks.append((cells[1], cells[6], kind, cells[-1]))
    if not marks:
        return "No audit rows found.\n"
    count = {k: sum(m[2] == k for m in marks) for k in ("agree", "disagree", "unmarked", "unclear")}
    if count["unmarked"] == len(marks):
        return f"{len(marks)} audit rows, not marked yet (fill the last column with agree / disagree).\n"
    marked = count["agree"] + count["disagree"]
    text = (f"{len(marks)} audit rows: agree {count['agree']}, disagree {count['disagree']}"
            + (f" ({count['disagree'] / marked:.0%} of marked)" if marked else "")
            + f", unmarked {count['unmarked']}, unclear {count['unclear']}.\n")
    dis = [f"{qid} (judge said {verdict})" for qid, verdict, kind, _ in marks if kind == "disagree"]
    odd = [f"{qid}: {raw!r}" for qid, _, kind, raw in marks if kind == "unclear"]
    if dis:
        text += "Disagreements: " + ", ".join(dis) + ".\n"
    if odd:
        text += "Unclear marks (use agree / disagree): " + ", ".join(odd) + ".\n"
    return text


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def build_report(folder: Path, questions_path: Path | None = None) -> str:
    saved = yaml.safe_load(open(folder / "config.yaml", encoding="utf-8"))
    qpath = questions_path or resolve_path(saved["paths"]["questions"])
    questions = {q["id"]: q for q in map(json.loads, open(qpath, encoding="utf-8"))}
    records = load_records(folder)
    description, threshold, applied = chosen_threshold(folder, saved)
    llm_only, system = frame(records), frame(system_records(records, None if applied else threshold))
    g = saved["generation"]
    return "\n".join([
        f"# Phase 8 report: {saved['run_name']} ({saved['eval']['split']} split)", "",
        f"Generator `{g['model']}`, judge `{g['judge_model']}`, prompt v{g['prompt_version']}, "
        f"{g['context_chunks']} chunks. Decline setting: {description}.", "",
        "## Chosen system: metrics by group (cluster 95% intervals)", "", metrics_section(system, llm_only),
        "## Decline (chosen system)", "", decline_section(system),
        "## Judge validity", "", judge_section(llm_only),
        "## Hand audit (judge_audit.md)", "", audit_tally(folder / "judge_audit.md"),
        "## Failure report (chosen system; one label per wrong answer)", "", failure_section(system, questions),
        "## Limitation 9: accuracy by gold-chunk rank (LLM answers, not declined, `overall`)", "",
        rank_section(llm_only),
    ])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run", help="graded results folder, e.g. gen_llama or gen_final")
    args = parser.parse_args()
    folder = resolve_path(load_config("configs/default.yaml")["paths"]["results_dir"]) / args.run
    report = build_report(folder)
    (folder / "report.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"Wrote {(folder / 'report.md').relative_to(resolve_path('.'))}")


if __name__ == "__main__":
    main()
