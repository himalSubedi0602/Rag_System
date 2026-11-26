"""Check a downloaded generation-results folder before committing it. Read-only and light: it loads no model.

Run:  python -m src.check_generation gen_llama                  (compares with configs/gen_llama.yaml)
      python -m src.check_generation gen_llama --config configs/gen_llama.yaml
Prints one line per check (OK / FAIL / NOTE) and exits with status 1 if any check fails.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.config import load_config, resolve_path

EXPECTED_FILES = ["config.yaml", "generations.jsonl", "per_question.csv", "metrics.csv", "decline.csv",
                  "judge_audit.md", "summary.md"]
IGNORED_KEYS = {"device"}     # cuda on Colab, cpu on the Mac (documented deviation); nothing else may differ
AUDIT_SIZE = 30


def config_differences(saved: dict[str, Any], reference: dict[str, Any], prefix: str = "") -> list[str]:
    """Dotted keys whose values differ between the saved run config and the reference config."""
    diffs = []
    for key in sorted(set(saved) | set(reference)):
        if not prefix and key in IGNORED_KEYS:
            continue
        a, b = saved.get(key), reference.get(key)
        if isinstance(a, dict) and isinstance(b, dict):
            diffs += config_differences(a, b, f"{prefix}{key}.")
        elif a != b:
            diffs.append(f"{prefix}{key}: run={a!r} reference={b!r}")
    return diffs


def split_ids(questions_path: Path, split: str) -> list[str]:
    return [q["id"] for q in map(json.loads, open(questions_path, encoding="utf-8")) if q["split"] == split]


def check_folder(folder: Path, reference: dict[str, Any]) -> list[tuple[str, str, str]]:
    """(status, check, detail) per check; status is OK, FAIL or NOTE."""
    out: list[tuple[str, str, str]] = []
    missing = [f for f in EXPECTED_FILES if not (folder / f).exists()]
    out.append(("FAIL" if missing else "OK", "all output files present", ", ".join(missing) or "7 files"))
    if not (folder / "config.yaml").exists() or not (folder / "generations.jsonl").exists():
        return out

    saved = yaml.safe_load(open(folder / "config.yaml", encoding="utf-8"))
    diffs = config_differences(saved, reference)
    out.append(("FAIL" if diffs else "OK", "config matches the reference (device ignored)",
                "; ".join(diffs) or f"device={saved.get('device')}"))

    lines = [line for line in open(folder / "generations.jsonl", encoding="utf-8") if line.strip()]
    log, broken = [], 0
    for line in lines:
        try:
            log.append(json.loads(line))
        except json.JSONDecodeError:
            broken += 1
    out.append(("FAIL" if broken else "OK", "every generations.jsonl line is complete", f"{broken} broken"))

    split = saved["eval"]["split"]
    expected = split_ids(resolve_path(saved["paths"]["questions"]), split)
    ids = [e["id"] for e in log]
    dupes = len(ids) - len(set(ids))
    out.append(("FAIL" if dupes else "OK", "no duplicate question ids", f"{dupes} duplicates"))
    missing_ids, extra_ids = sorted(set(expected) - set(ids)), sorted(set(ids) - set(expected))
    out.append(("FAIL" if missing_ids or extra_ids else "OK", f"one answer per {split} question",
                f"{len(set(ids))} of {len(expected)}" + (f"; missing {missing_ids[:5]}" if missing_ids else "")
                + (f"; not in split {extra_ids[:5]}" if extra_ids else "")))

    empty = [e["id"] for e in log if not str(e.get("answer", "")).strip()]
    out.append(("FAIL" if empty else "OK", "no empty answers", ", ".join(empty[:5]) or "0 empty"))
    out.append(("NOTE", "declined by the LLM", f"{sum(bool(e.get('declined')) for e in log)} of {len(log)}"))

    if (folder / "per_question.csv").exists():
        pq = pd.read_csv(folder / "per_question.csv")
        out.append(("FAIL" if len(pq) != len(log) else "OK", "per_question.csv has one row per answer",
                    f"{len(pq)} rows"))
        ungraded = pq[pq["question_type"] != "no_answer"]["correct"].isna().sum()
        out.append(("NOTE" if ungraded else "OK", "every answer graded (judge reply parsed)",
                    f"{ungraded} ungraded"))
    if (folder / "judge_audit.md").exists():
        rows = sum(1 for line in open(folder / "judge_audit.md", encoding="utf-8")
                   if line.startswith("| ") and not line.startswith("| #"))
        out.append(("OK" if rows == AUDIT_SIZE else "NOTE", "judge audit sample size", f"{rows} rows"))
    size_kb = (folder / "generations.jsonl").stat().st_size / 1024
    out.append(("NOTE", "generations.jsonl size (git-ignored by default)", f"{size_kb:.0f} KB"))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run", help="results folder name, e.g. gen_llama")
    parser.add_argument("--config", help="reference config (default: configs/<run>.yaml)")
    args = parser.parse_args()

    reference = load_config(args.config or f"configs/{args.run}.yaml")
    folder = resolve_path(reference["paths"]["results_dir"]) / args.run
    if not folder.is_dir():
        sys.exit(f"No results folder: {folder}")
    results = check_folder(folder, reference)
    for status, check, detail in results:
        print(f"{status:<4}  {check}: {detail}")
    failed = sum(status == "FAIL" for status, _, _ in results)
    print(f"\n{'All checks passed.' if not failed else f'{failed} check(s) FAILED: do not commit yet.'}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
