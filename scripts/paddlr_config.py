#!/usr/bin/env python3
"""Paddlr project memory configuration loader (.paddlr.json).

Zero external dependencies (Python 3.10+ standard library only).
Resolves canonical project memory paths under `docs/paddlr/` by default,
with optional overrides from `<repo_root>/.paddlr.json`.
"""

import json
from pathlib import Path
from typing import Any, Dict

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
ALLOWED_AUTONOMY_KEYS = ("pauseOnAmbiguity", "pauseBeforeCode")
ALLOWED_PAUSE_BEFORE_CODE = ("never", "level3", "always")
DEFAULT_AUTONOMY: Dict[str, Any] = {
    "pauseOnAmbiguity": False,
    "pauseBeforeCode": "never",
}


def _load_config_data(repo_root: Path) -> Dict[str, Any]:
    base_root = Path(repo_root).resolve()
    config_path = base_root / CONFIG_FILENAME
    if not config_path.is_file():
        return {}

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {config_path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError(f"{config_path} must contain a JSON object.")

    return data


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
    data = _load_config_data(base_root)
    overrides: Dict[str, str] = {}

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


def resolve_autonomy_config(repo_root: Path) -> Dict[str, Any]:
    """Resolve autonomy preferences from `.paddlr.json`.

    Returns a dictionary with:
    - `pauseOnAmbiguity` (bool, default False): ask when product/UX/requirements
      are ambiguous and cannot be settled by reading code or prototyping.
    - `pauseBeforeCode` ("never" | "level3" | "always", default "never"):
      whether to pause for Spec/Plan approval before editing production code.
      Irreversible actions (Hard Stops) always pause regardless of this setting.
    """
    data = _load_config_data(repo_root)
    resolved = dict(DEFAULT_AUTONOMY)

    if "autonomy" not in data:
        return resolved

    autonomy = data["autonomy"]
    if not isinstance(autonomy, dict):
        raise ValueError(".paddlr.json field 'autonomy' must be a JSON object.")

    unknown_keys = set(autonomy.keys()) - set(ALLOWED_AUTONOMY_KEYS)
    if unknown_keys:
        raise ValueError(
            f"Unknown key(s) in .paddlr.json 'autonomy': {', '.join(sorted(unknown_keys))}"
        )

    if "pauseOnAmbiguity" in autonomy:
        val = autonomy["pauseOnAmbiguity"]
        if not isinstance(val, bool):
            raise ValueError(".paddlr.json field 'autonomy.pauseOnAmbiguity' must be a boolean.")
        resolved["pauseOnAmbiguity"] = val

    if "pauseBeforeCode" in autonomy:
        val = autonomy["pauseBeforeCode"]
        if not isinstance(val, str) or val not in ALLOWED_PAUSE_BEFORE_CODE:
            allowed = ", ".join(ALLOWED_PAUSE_BEFORE_CODE)
            raise ValueError(
                f".paddlr.json field 'autonomy.pauseBeforeCode' must be one of: {allowed}."
            )
        resolved["pauseBeforeCode"] = val

    return resolved
