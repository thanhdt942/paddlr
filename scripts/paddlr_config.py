#!/usr/bin/env python3
"""Paddlr project memory configuration loader (.paddlr.json).

Zero external dependencies (Python 3.10+ standard library only).
Resolves canonical project memory paths under `docs/paddlr/` by default,
with optional overrides from `<repo_root>/.paddlr.json`.
"""

import json
from pathlib import Path
from typing import Dict

CONFIG_FILENAME = ".paddlr.json"
DEFAULT_ROOT = "docs/paddlr"
ALLOWED_KEYS = ("root", "specs", "plans", "decisions", "decisionsIndex", "project")
DEFAULT_RELATIVE_SUBPATHS = {
    "specs": "specs",
    "plans": "plans",
    "decisions": "decisions",
    "decisionsIndex": "DECISIONS.md",
    "project": "PROJECT.md",
}


def _resolve_contained_path(repo_root: Path, raw_value: str, key: str) -> Path:
    if not isinstance(raw_value, str) or not raw_value.strip():
        raise ValueError(f".paddlr.json field '{key}' must be a non-empty string.")

    candidate = Path(raw_value)
    if candidate.is_absolute():
        raise ValueError(f".paddlr.json field '{key}' must be a relative path inside the repository.")

    resolved = (repo_root / candidate).resolve()
    try:
        resolved.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(
            f".paddlr.json field '{key}' escapes the repository root: {raw_value!r}"
        ) from exc

    return resolved


def resolve_memory_paths(repo_root: Path) -> Dict[str, Path]:
    """Resolve project memory paths for a repository root.

    Returns a dictionary containing `root`, `specs`, `plans`, `decisions`,
    `decisionsIndex`, and `project` as resolved `Path` objects inside `repo_root`.
    Raises `ValueError` if `.paddlr.json` is malformed or contains invalid paths.
    """
    base_root = Path(repo_root).resolve()
    config_path = base_root / CONFIG_FILENAME
    overrides: Dict[str, str] = {}

    if config_path.is_file():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {config_path}: {exc}") from exc

        if not isinstance(data, dict):
            raise ValueError(f"{config_path} must contain a JSON object.")

        for key in ALLOWED_KEYS:
            if key in data:
                val = data[key]
                if not isinstance(val, str) or not val.strip():
                    raise ValueError(f".paddlr.json field '{key}' must be a non-empty string.")
                overrides[key] = val

    root_rel = overrides.get("root", DEFAULT_ROOT)
    resolved_root = _resolve_contained_path(base_root, root_rel, "root")

    paths: Dict[str, Path] = {"root": resolved_root}
    for key, rel_subpath in DEFAULT_RELATIVE_SUBPATHS.items():
        if key in overrides:
            paths[key] = _resolve_contained_path(base_root, overrides[key], key)
        else:
            paths[key] = (resolved_root / rel_subpath).resolve()

    return paths
