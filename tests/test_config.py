"""Tests for src/config.py."""

from pathlib import Path

import pytest

from src.config import PROJECT_ROOT, ConfigError, deep_merge, load_config


def write_yaml(tmp_path: Path, text: str) -> Path:
    """Write YAML text to a temporary file and return its path."""
    path = tmp_path / "exp.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def test_baseline_config_loads():
    cfg = load_config(PROJECT_ROOT / "configs" / "baseline.yaml")
    assert cfg["run_name"] == "baseline"
    assert cfg["chunking"]["chunk_size"] == 500
    assert cfg["retrieval"]["mode"] == "vector"


def test_override_keeps_other_keys_in_same_section(tmp_path):
    path = write_yaml(tmp_path, "run_name: small\nchunking:\n  chunk_size: 250\n")
    cfg = load_config(path)
    assert cfg["chunking"]["chunk_size"] == 250
    assert cfg["chunking"]["strategy"] == "fixed"  # untouched default survives the merge


def test_deep_merge_does_not_mutate_base():
    base = {"a": {"b": 1}}
    deep_merge(base, {"a": {"b": 2}})
    assert base == {"a": {"b": 1}}


def test_unknown_key_is_rejected(tmp_path):
    path = write_yaml(tmp_path, "run_name: typo\nchunking:\n  chunk_sise: 250\n")
    with pytest.raises(ConfigError, match="chunking.chunk_sise"):
        load_config(path)


def test_invalid_choice_is_rejected(tmp_path):
    path = write_yaml(tmp_path, "run_name: bad\nretrieval:\n  mode: magic\n")
    with pytest.raises(ConfigError, match="retrieval.mode"):
        load_config(path)


def test_overlap_must_be_smaller_than_chunk_size(tmp_path):
    path = write_yaml(tmp_path, "run_name: bad\nchunking:\n  chunk_size: 100\n  chunk_overlap: 100\n")
    with pytest.raises(ConfigError, match="chunk_overlap"):
        load_config(path)


def test_section_replaced_by_scalar_is_rejected(tmp_path):
    path = write_yaml(tmp_path, "run_name: bad\nchunking: 500\n")
    with pytest.raises(ConfigError, match="must be a section"):
        load_config(path)


def test_min_section_tokens_must_be_smaller_than_chunk_size(tmp_path):
    path = write_yaml(tmp_path, "run_name: bad\nchunking:\n  chunk_size: 100\n  min_section_tokens: 100\n")
    with pytest.raises(ConfigError, match="min_section_tokens"):
        load_config(path)
