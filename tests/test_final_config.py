"""Final-run and app configs from the tune run's choice (src/final_config.py)."""

import pandas as pd
import pytest
import yaml

from src.config import load_config, resolve_path
from src.final_config import app_text, final_config_text, selected_setting, set_generation_keys


def tune_folder(tmp_path, selected_row, threshold):
    scores = [float(i) for i in range(100)]                       # answerable top-1 scores 0..99
    pq = pd.DataFrame({"question_type": ["lookup"] * 100 + ["no_answer"] * 5,
                       "decline_score": scores + [-50.0] * 5})
    pq.to_csv(tmp_path / "per_question.csv", index=False)
    rows = [["no threshold (LLM decides)", None], ["p2.5 of answerable top-1 scores", 2.475],
            ["p5 of answerable top-1 scores", threshold], ["p10 of answerable top-1 scores", 9.9]]
    decline = pd.DataFrame(rows, columns=["setting", "threshold"])
    decline["selected"] = decline.index == selected_row
    decline.to_csv(tmp_path / "decline.csv", index=False)
    return tmp_path


def test_selected_percentile_is_recomputed_unrounded(tmp_path):
    setting, t = selected_setting(tune_folder(tmp_path, 2, 4.95))
    assert setting.startswith("p5") and t == pytest.approx(4.95)    # 5th percentile of 0..99, no_answer excluded


def test_no_threshold_and_no_selection(tmp_path):
    assert selected_setting(tune_folder(tmp_path, 0, 4.95)) == ("no threshold (LLM decides)", None)
    with pytest.raises(ValueError, match="no decline setting"):
        selected_setting(tune_folder(tmp_path, None, 4.95))


def test_mismatched_threshold_is_refused(tmp_path):
    with pytest.raises(ValueError, match="does not match"):
        selected_setting(tune_folder(tmp_path, 2, 7.0))


def test_final_config_is_valid_and_on_test(tmp_path):
    reference = yaml.safe_load(open(resolve_path("configs/gen_llama.yaml")))
    text = final_config_text(reference, "gen_llama", "p5 of answerable top-1 scores", 4.95)
    path = tmp_path / "gen_final.yaml"
    path.write_text(text)
    cfg = load_config(path)
    assert cfg["run_name"] == "gen_final" and cfg["eval"]["split"] == "test"
    assert cfg["generation"]["decline_threshold"] == 4.95 and cfg["generation"]["model"] == "llama3.1:8b"
    assert cfg["retrieval"] == load_config(resolve_path("configs/gen_llama.yaml"))["retrieval"]
    assert text.startswith("# Phase 8 FINAL test run")


def test_app_config_update_keeps_everything_else(tmp_path):
    original = resolve_path("configs/app.yaml").read_text()
    new = app_text(original, {"model": "qwen2.5:7b", "prompt_version": 2, "decline_threshold": 1.25},
                   "p5 of answerable top-1 scores", "gen_qwen")
    path = tmp_path / "app.yaml"
    path.write_text(new)
    cfg = load_config(path)
    assert cfg["generation"]["model"] == "qwen2.5:7b" and cfg["generation"]["decline_threshold"] == 1.25
    assert cfg["generation"]["prompt_version"] == 2
    assert cfg["embedding"]["model"] == "BAAI/bge-small-en-v1.5"          # the other `model:` is untouched
    assert "stays null" not in new and "run-10 rule (p5" in new
    assert cfg["retrieval"] == load_config(resolve_path("configs/app.yaml"))["retrieval"]


def test_set_generation_keys_keeps_comments():
    text = "run_name: x\ngeneration:\n  model: a   # the generator\n  decline_threshold: null\nother: 1\n"
    out = set_generation_keys(text, {"model": "b", "decline_threshold": None, "prompt_version": 1})
    assert "  model: b   # the generator\n" in out and "  prompt_version: 1\nother: 1\n" in out
