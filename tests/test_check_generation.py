"""Results-folder checker (src/check_generation.py) on a small fake folder."""

import json

import yaml

from src.check_generation import check_folder, config_differences


def make_folder(tmp_path, answers, device="cuda", model="llama3.1:8b"):
    questions = tmp_path / "questions.jsonl"
    questions.write_text("".join(json.dumps({"id": i, "split": s}) + "\n"
                                 for i, s in [("q1", "tune"), ("q2", "tune"), ("t1", "test")]))
    reference = {"device": "cpu", "eval": {"split": "tune"}, "paths": {"questions": str(questions)},
                 "generation": {"model": "llama3.1:8b", "max_tokens": 512}}
    folder = tmp_path / "gen_llama"
    folder.mkdir()
    saved = {**reference, "device": device, "generation": {**reference["generation"], "model": model}}
    (folder / "config.yaml").write_text(yaml.safe_dump(saved))
    (folder / "generations.jsonl").write_text(answers)
    return folder, reference


def statuses(results):
    return {check: status for status, check, _ in results}


def entry(qid, answer="Yes [1].", declined=False):
    return json.dumps({"id": qid, "answer": answer, "declined": declined}) + "\n"


def test_good_folder_passes_except_missing_files(tmp_path):
    folder, ref = make_folder(tmp_path, entry("q1") + entry("q2", declined=True))
    s = statuses(check_folder(folder, ref))
    assert s["config matches the reference (device ignored)"] == "OK"
    assert s["one answer per tune question"] == "OK" and s["no duplicate question ids"] == "OK"
    assert s["no empty answers"] == "OK" and s["every generations.jsonl line is complete"] == "OK"
    assert s["all output files present"] == "FAIL"      # only config + generations were written here


def test_problems_are_caught(tmp_path):
    folder, ref = make_folder(tmp_path, entry("q1") + entry("q1", answer=" ") + '{"id": "q2", "ans',
                              model="qwen2.5:7b")
    s = statuses(check_folder(folder, ref))
    for check in ["config matches the reference (device ignored)", "every generations.jsonl line is complete",
                  "no duplicate question ids", "one answer per tune question", "no empty answers"]:
        assert s[check] == "FAIL", check


def test_config_differences_ignores_only_device():
    assert config_differences({"device": "cuda", "a": {"b": 1}}, {"device": "cpu", "a": {"b": 1}}) == []
    assert config_differences({"a": {"b": 1}}, {"a": {"b": 2}}) == ["a.b: run=1 reference=2"]
