"""Phase 8 Steps 3 and 5: turn the tune run's pre-registered choice into the final-run and app configs.

Run:  python -m src.final_config gen_llama            show the selected decline setting and what would change
      python -m src.final_config gen_llama --write    write configs/gen_final.yaml and update configs/app.yaml

The decline setting is the one run_generation selected by the pre-registered run-10 rule (decline.csv,
column `selected`). The threshold is recomputed unrounded from per_question.csv (the same percentile of the
answerable tune questions' top-1 scores), so the final run uses exactly the value that was evaluated.
Reads saved files only: no model is loaded.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from src.config import load_config, resolve_path
from src.generate import percentile_thresholds

FINAL_RUN = "gen_final"
APP_CONFIG = "configs/app.yaml"


def selected_setting(folder: Path) -> tuple[str, float | None]:
    """(setting name, unrounded threshold or None for 'no threshold') from a graded tune run."""
    decline = pd.read_csv(folder / "decline.csv")
    chosen = decline[decline["selected"].astype(str).str.lower() == "true"]
    if chosen.empty:
        raise ValueError("no decline setting was selected (none meets the wrong-decline guardrail)")
    row = chosen.iloc[0]
    if pd.isna(row["threshold"]):
        return str(row["setting"]), None
    match = re.match(r"p([\d.]+) ", str(row["setting"]))
    if not match:
        raise ValueError(f"unexpected setting name: {row['setting']!r}")
    p = float(match.group(1))
    pq = pd.read_csv(folder / "per_question.csv")
    scores = pq.loc[pq["question_type"] != "no_answer", "decline_score"].astype(float).tolist()
    threshold = percentile_thresholds(scores, [p])[p]
    if abs(threshold - float(row["threshold"])) > 1e-3:          # decline.csv stores it rounded to 4 places
        raise ValueError(f"recomputed threshold {threshold} does not match decline.csv ({row['threshold']})")
    return str(row["setting"]), threshold


def final_config_text(reference: dict[str, Any], run: str, setting: str, threshold: float | None) -> str:
    """configs/gen_final.yaml: the tune run's own config file, on the test split, with the chosen threshold."""
    cfg = {**reference, "run_name": FINAL_RUN}
    cfg["eval"] = {**reference.get("eval", {}), "split": "test"}
    cfg["generation"] = {**reference.get("generation", {}), "decline_threshold": threshold}
    header = (f"# Phase 8 FINAL test run (Step 5): run ONCE with --final. Nothing is tuned on its results.\n"
              f"# Same system as the tune run `{run}`; decline setting chosen on tune by the pre-registered\n"
              f"# run-10 rule: {setting}.\n")
    return header + yaml.safe_dump(cfg, sort_keys=False)


def set_generation_keys(text: str, values: dict[str, Any]) -> str:
    """Set keys inside the top-level `generation:` block of a YAML file, keeping every other line and comment.
    Keys that are missing from the block are added at its end."""
    lines = text.splitlines(keepends=True)
    start = next((i for i, l in enumerate(lines) if l.startswith("generation:")), None)
    if start is None:
        return text.rstrip("\n") + "\ngeneration:\n" + "".join(f"  {k}: {fmt(v)}\n" for k, v in values.items())
    end = start + 1
    while end < len(lines) and (not lines[end].strip() or lines[end].startswith((" ", "\t", "#"))):
        end += 1
    remaining = dict(values)
    for i in range(start + 1, end):
        m = re.match(r"^(\s+)(\w+):(\s*)([^#\n]*?)(\s*#.*)?$", lines[i].rstrip("\n"))
        if m and m.group(2) in remaining:
            lines[i] = f"{m.group(1)}{m.group(2)}: {fmt(remaining.pop(m.group(2)))}{m.group(5) or ''}\n"
    insert = [f"  {k}: {fmt(v)}\n" for k, v in remaining.items()]
    return "".join(lines[:end] + insert + lines[end:])


def fmt(value: Any) -> str:
    return "null" if value is None else (repr(float(value)) if isinstance(value, float) else str(value))


def app_text(text: str, generation: dict[str, Any], setting: str, run: str) -> str:
    """configs/app.yaml with the chosen generator, prompt version and decline threshold."""
    text = set_generation_keys(text, {"model": generation["model"],
                                      "prompt_version": generation.get("prompt_version", 1),
                                      "decline_threshold": generation["decline_threshold"]})
    return re.sub(r"^# decline_threshold stays null.*$",
                  f"# decline_threshold: chosen on tune by the pre-registered run-10 rule ({setting}; run {run}).",
                  text, flags=re.M)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run", help="the graded tune run, e.g. gen_llama")
    parser.add_argument("--write", action="store_true", help="write configs/gen_final.yaml and update configs/app.yaml")
    parser.add_argument("--force", action="store_true", help="overwrite an existing configs/gen_final.yaml")
    args = parser.parse_args()

    ref_path = resolve_path(f"configs/{args.run}.yaml")
    reference = yaml.safe_load(open(ref_path, encoding="utf-8"))
    folder = resolve_path(load_config(ref_path)["paths"]["results_dir"]) / args.run
    saved = yaml.safe_load(open(folder / "config.yaml", encoding="utf-8"))
    if saved["eval"]["split"] != "tune":
        sys.exit(f"{args.run} was run on the {saved['eval']['split']} split: choices are made on tune only.")
    try:
        setting, threshold = selected_setting(folder)
    except ValueError as err:
        sys.exit(f"Cannot choose a decline setting: {err}")

    final_text = final_config_text(reference, args.run, setting, threshold)
    generation = {**reference.get("generation", {}), "decline_threshold": threshold}
    app_path = resolve_path(APP_CONFIG)
    new_app = app_text(app_path.read_text(encoding="utf-8"), generation, setting, args.run)
    print(f"Selected decline setting: {setting}" + ("" if threshold is None else f" -> threshold {threshold!r}"))
    print(f"Generator: {generation['model']}, prompt v{generation.get('prompt_version', 1)}\n")
    print(f"--- configs/{FINAL_RUN}.yaml ---\n{final_text}")
    if not args.write:
        print("Dry run: nothing written. Add --write to write both files.")
        return
    final_path = resolve_path(f"configs/{FINAL_RUN}.yaml")
    if final_path.exists() and not args.force:
        sys.exit(f"{final_path.name} already exists: not overwriting (add --force if this is intended).")
    final_path.write_text(final_text, encoding="utf-8")
    load_config(final_path)                                   # must pass the usual validation
    app_path.write_text(new_app, encoding="utf-8")
    load_config(app_path)
    print(f"Wrote configs/{FINAL_RUN}.yaml and updated {APP_CONFIG}.")


if __name__ == "__main__":
    main()
