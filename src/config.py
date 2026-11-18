"""Load experiment configs: configs/default.yaml merged with one experiment YAML."""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "configs" / "default.yaml"

# Settings that only make sense with a fixed set of values.
ALLOWED_VALUES: dict[tuple[str, str], set[str]] = {
    ("chunking", "strategy"): {"fixed", "heading"},
    ("retrieval", "mode"): {"vector", "hybrid"},
    ("retrieval", "version_filter"): {"none", "current_only"},
    ("eval", "split"): {"tune", "test"},
}


class ConfigError(ValueError):
    """Raised when a config file is missing keys or has invalid values."""


def read_yaml(path: str | Path) -> dict[str, Any]:
    """Read a YAML file and return it as a dict (empty file -> empty dict)."""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)  # safe_load never executes code embedded in YAML
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ConfigError(f"{path} must contain a mapping at the top level")
    return data


def deep_merge(base: dict[str, Any], override: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Return a copy of `base` with values from `override` applied, section by section.

    Nested dicts are merged instead of replaced, so overriding chunking.chunk_size
    keeps chunking.strategy. Keys that don't exist in `base` raise ConfigError (catches typos).
    """
    merged = copy.deepcopy(base)  # never mutate the caller's defaults
    for key, value in override.items():
        full_key = f"{prefix}{key}"
        if key not in base:
            raise ConfigError(f"Unknown config key: '{full_key}'")
        if isinstance(base[key], dict):
            if not isinstance(value, dict):
                raise ConfigError(f"'{full_key}' must be a section (mapping), got {value!r}")
            merged[key] = deep_merge(base[key], value, prefix=f"{full_key}.")
        else:
            merged[key] = value
    return merged


def validate_config(cfg: dict[str, Any]) -> None:
    """Check values that would otherwise cause confusing errors much later in a run."""
    if not isinstance(cfg.get("run_name"), str) or not cfg["run_name"].strip():
        raise ConfigError("run_name must be a non-empty string")

    for (section, key), allowed in ALLOWED_VALUES.items():
        value = cfg[section][key]
        if value not in allowed:
            raise ConfigError(f"{section}.{key} must be one of {sorted(allowed)}, got {value!r}")

    chunking = cfg["chunking"]
    if chunking["chunk_size"] <= 0:
        raise ConfigError("chunking.chunk_size must be positive")
    if not 0 <= chunking["chunk_overlap"] < chunking["chunk_size"]:
        # overlap >= size would make the chunker step forward by 0 tokens and loop forever
        raise ConfigError("chunking.chunk_overlap must be >= 0 and smaller than chunk_size")

    if not 0 <= chunking["min_section_tokens"] < chunking["chunk_size"]:
        raise ConfigError("chunking.min_section_tokens must be >= 0 and smaller than chunk_size")

    retrieval = cfg["retrieval"]
    if retrieval["small_to_big"] and not (0 <= retrieval["piece_overlap"] < retrieval["piece_size"] < chunking["chunk_size"]):
        raise ConfigError("small_to_big needs 0 <= piece_overlap < piece_size < chunking.chunk_size")
    if not 0 < retrieval["final_k"] <= retrieval["top_k_each"]:
        raise ConfigError("retrieval.final_k must be between 1 and retrieval.top_k_each")


def load_config(path: str | Path, default_path: str | Path = DEFAULT_CONFIG_PATH) -> dict[str, Any]:
    """Load one experiment config: defaults + overrides, then validate."""
    cfg = deep_merge(read_yaml(default_path), read_yaml(path))
    validate_config(cfg)
    return cfg


def resolve_path(relative: str | Path) -> Path:
    """Turn a path from the config (relative to the project root) into an absolute Path."""
    return PROJECT_ROOT / relative


if __name__ == "__main__":
    # Usage: python -m src.config configs/baseline.yaml  -> prints the final merged config
    config_path = sys.argv[1] if len(sys.argv) > 1 else "configs/baseline.yaml"
    print(yaml.safe_dump(load_config(config_path), sort_keys=False))
