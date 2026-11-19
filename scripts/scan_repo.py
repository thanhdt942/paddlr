#!/usr/bin/env python3
"""
HolyShitItWorks — Deterministic Repository Scanner (scan_repo.py)

Lightweight, dependency-free utility to inspect repository structure,
identify technology indicators, and discover development commands
without executing arbitrary code or exposing sensitive values.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

# Directories to always ignore during structure and file exploration
DEFAULT_IGNORED_DIRS: Set[str] = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "bower_components",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    "dist",
    "build",
    "out",
    "target",
    "bin",
    "obj",
    ".idea",
    ".vscode",
    ".vs",
    ".next",
    ".nuxt",
    ".turbo",
    ".cache",
    ".gradle",
    ".terraform",
}

# Patterns for sensitive/secret files whose contents must NEVER be read or printed
SENSITIVE_FILE_PATTERNS = [
    re.compile(r"^\.env(\..+)?$", re.IGNORECASE),
    re.compile(r".*credential.*", re.IGNORECASE),
    re.compile(r".*secret.*", re.IGNORECASE),
    re.compile(r".*token.*", re.IGNORECASE),
    re.compile(r".*\.pem$", re.IGNORECASE),
    re.compile(r".*\.key$", re.IGNORECASE),
    re.compile(r".*\.pfx$", re.IGNORECASE),
    re.compile(r"^id_rsa.*", re.IGNORECASE),
    re.compile(r"^id_ed25519.*", re.IGNORECASE),
]

# Indicator files mapping to technology stacks
TECH_INDICATORS = {
    "Python": [
        "pyproject.toml",
        "setup.py",
        "setup.cfg",
        "requirements.txt",
        "Pipfile",
        "poetry.lock",
        "uv.lock",
    ],
    "JavaScript / TypeScript": [
        "package.json",
        "tsconfig.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "package-lock.json",
        "bun.lockb",
        "deno.json",
    ],
    "Go": ["go.mod", "go.sum", "Gopkg.toml"],
    "Rust": ["Cargo.toml", "Cargo.lock"],
    "Java / JVM": [
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "gradlew",
        "mvnw",
    ],
    "C# / .NET": ["*.sln", "*.csproj", "global.json", "Directory.Build.props"],
    "PHP": ["composer.json", "composer.lock"],
    "Ruby": ["Gemfile", "Gemfile.lock"],
    "Docker / Containers": [
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        "Containerfile",
    ],
    "CI/CD": [
        ".github/workflows",
        ".gitlab-ci.yml",
        ".circleci/config.yml",
        "Jenkinsfile",
        "azure-pipelines.yml",
    ],
    "Build & Task Automation": ["Makefile", "Taskfile.yml", "Justfile"],
}


def is_sensitive_filename(name: str) -> bool:
    """Return True if filename matches sensitive/secret patterns."""
    return any(pattern.match(name) for pattern in SENSITIVE_FILE_PATTERNS)


def scan_tree(
    root: Path, current_depth: int, max_depth: int, ignored_dirs: Set[str]
) -> Dict[str, Any]:
    """Recursively collect directory structure up to max_depth."""
    tree: Dict[str, Any] = {"name": root.name or str(root), "type": "directory", "children": []}

    if current_depth >= max_depth:
        return tree

    try:
        entries = sorted(os.scandir(root), key=lambda e: (not e.is_dir(), e.name.lower()))
    except (PermissionError, OSError) as err:
        tree["error"] = f"Unreadable directory: {err}"
        return tree

    for entry in entries:
        try:
            if entry.is_dir(follow_symlinks=False) and entry.name in ignored_dirs:
                continue
            if entry.is_dir(follow_symlinks=False):
                child_tree = scan_tree(
                    Path(entry.path), current_depth + 1, max_depth, ignored_dirs
                )
                tree["children"].append(child_tree)
            elif entry.is_file(follow_symlinks=False):
                is_sensitive = is_sensitive_filename(entry.name)
                tree["children"].append(
                    {
                        "name": entry.name,
                        "type": "file",
                        "is_sensitive": is_sensitive,
                    }
                )
        except (PermissionError, OSError):
            continue

    return tree


def extract_potential_commands(root: Path) -> Dict[str, List[str]]:
    """Inspect safe configuration files to extract common commands."""
    commands: Dict[str, List[str]] = {}

    # Inspect package.json for npm scripts
    pkg_json = root / "package.json"
    if pkg_json.is_file():
        try:
            with open(pkg_json, "r", encoding="utf-8") as f:
                data = json.load(f)
                scripts = data.get("scripts", {})
                if scripts:
                    commands["npm / pnpm / yarn scripts"] = [
                        f"{name}: {cmd}" for name, cmd in list(scripts.items())[:15]
                    ]
        except Exception:
            pass

    # Inspect Makefile for targets
    makefile = root / "Makefile"
    if makefile.is_file():
        try:
            targets: List[str] = []
            with open(makefile, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    m = re.match(r"^([a-zA-Z0-9_\-\.]+):", line)
                    if m and not line.startswith("."):
                        target = m.group(1)
                        if target not in targets:
                            targets.append(target)
            if targets:
                commands["make targets"] = targets[:15]
        except Exception:
            pass

    # Inspect pyproject.toml for scripts / test config
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        try:
            indicators: List[str] = []
            with open(pyproject, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if "pytest" in content:
                    indicators.append("pytest (test framework detected)")
                if "ruff" in content:
                    indicators.append("ruff (linter/formatter detected)")
                if "black" in content:
                    indicators.append("black (formatter detected)")
                if "mypy" in content:
                    indicators.append("mypy (type checker detected)")
                if "flit" in content or "poetry" in content or "hatch" in content or "setuptools" in content:
                    indicators.append("standard python build backend configured")
            if indicators:
                commands["python tooling indicators"] = indicators
        except Exception:
            pass

    return commands


def scan_repository(root_path: str, max_depth: int = 3) -> Dict[str, Any]:
    """Execute complete deterministic repository scan."""
    root = Path(root_path).resolve()

    if not root.exists():
        return {
            "error": f"Repository path does not exist: {root_path}",
            "path": str(root),
            "status": "NOT_FOUND",
        }

    if not root.is_dir():
        return {
            "error": f"Repository path is not a directory: {root_path}",
            "path": str(root),
            "status": "NOT_A_DIRECTORY",
        }

    # Discover top-level files and directories
    top_level_files: List[str] = []
    top_level_dirs: List[str] = []
    sensitive_files_found: List[str] = []

    try:
        for entry in os.scandir(root):
            if entry.is_dir(follow_symlinks=False) and entry.name in DEFAULT_IGNORED_DIRS:
                continue
            if is_sensitive_filename(entry.name):
                sensitive_files_found.append(entry.name)
            if entry.is_dir(follow_symlinks=False):
                top_level_dirs.append(entry.name)
            elif entry.is_file(follow_symlinks=False):
                top_level_files.append(entry.name)
    except (PermissionError, OSError) as err:
        return {
            "error": f"Failed to read root directory: {err}",
            "path": str(root),
            "status": "PERMISSION_DENIED",
        }

    top_level_files.sort()
    top_level_dirs.sort()
    sensitive_files_found.sort()

    # Detect technology stacks based on indicator files
    detected_tech: Dict[str, List[str]] = {}
    for tech, indicators in TECH_INDICATORS.items():
        matched: List[str] = []
        for ind in indicators:
            if "*" in ind:
                pattern = ind.replace(".", r"\.").replace("*", ".*")
                rgx = re.compile(f"^{pattern}$", re.IGNORECASE)
                if any(rgx.match(f) for f in top_level_files):
                    matched.append(ind)
            elif "/" in ind:
                if (root / ind).exists():
                    matched.append(ind)
            else:
                if ind in top_level_files:
                    matched.append(ind)
        if matched:
            detected_tech[tech] = matched

    # Scan directory tree
    tree = scan_tree(root, 0, max_depth, DEFAULT_IGNORED_DIRS)

    # Extract safe command indicators
    commands = extract_potential_commands(root)

    # Detect existing agent instructions or project context
    project_context_indicators = {
        "has_agents_md": (root / "AGENTS.md").is_file(),
        "has_readme": any(f.lower().startswith("readme") for f in top_level_files),
        "has_contributing": any(f.lower().startswith("contributing") for f in top_level_files),
        "has_license": any(f.lower().startswith("license") for f in top_level_files),
        "has_project_context_dir": (root / "project-context").is_dir(),
        "has_project_context_doc": (root / "docs" / "PROJECT_CONTEXT.md").is_file(),
        "has_docs_dir": (root / "docs").is_dir(),
        "has_tests_dir": any(d in {"tests", "test", "__tests__", "spec"} for d in top_level_dirs),
    }

    return {
        "repository_root": str(root),
        "status": "OK",
        "scan_depth": max_depth,
        "summary": {
            "top_level_directory_count": len(top_level_dirs),
            "top_level_file_count": len(top_level_files),
            "sensitive_files_flagged": len(sensitive_files_found),
        },
        "project_context_indicators": project_context_indicators,
        "detected_technologies": detected_tech,
        "discovered_commands": commands,
        "sensitive_files_detected": sensitive_files_found,
        "tree": tree,
        "security_note": (
            "Sensitive files detected by filename only. Contents were NOT read or exposed."
        ),
    }


def format_tree_text(node: Dict[str, Any], prefix: str = "") -> List[str]:
    """Render the scanned directory tree into clean ASCII tree lines."""
    lines: List[str] = []
    children = node.get("children", [])
    total = len(children)
    for i, child in enumerate(children):
        is_last = i == (total - 1)
        connector = "└── " if is_last else "├── "
        child_name = child["name"]
        if child.get("type") == "directory":
            child_name += "/"
        if child.get("is_sensitive"):
            child_name += " [SENSITIVE - CONTENT PROTECTED]"
        lines.append(f"{prefix}{connector}{child_name}")
        if child.get("type") == "directory" and "children" in child:
            extension = "    " if is_last else "│   "
            lines.extend(format_tree_text(child, prefix + extension))
    return lines


def format_human_readable(data: Dict[str, Any]) -> str:
    """Format scan results for clear human/agent inspection."""
    if data.get("status") != "OK":
        return f"SCAN ERROR: {data.get('error')} (Path: {data.get('path')})\n"

    lines: List[str] = [
        "=" * 70,
        "HOLYSHITITWORKS — DETERMINISTIC REPOSITORY SCAN REPORT",
        "=" * 70,
        f"Repository Root: {data['repository_root']}",
        f"Scan Depth:      {data['scan_depth']}",
        "",
        "--- PROJECT CONTEXT & AGENT ENVIRONMENT ---",
    ]

    pci = data.get("project_context_indicators", {})
    for key, val in pci.items():
        status_str = "[FOUND]" if val else "[NOT FOUND]"
        lines.append(f"  {status_str:<12} {key}")

    lines.append("")
    lines.append("--- DETECTED TECHNOLOGIES & FRAMEWORKS ---")
    techs = data.get("detected_technologies", {})
    if techs:
        for tech, indicators in techs.items():
            lines.append(f"  • {tech}: {', '.join(indicators)}")
    else:
        lines.append("  (No standard framework configuration files detected at root)")

    commands = data.get("discovered_commands", {})
    if commands:
        lines.append("")
        lines.append("--- DISCOVERED COMMAND INDICATORS ---")
        for category, cmd_list in commands.items():
            lines.append(f"  [{category}]")
            for c in cmd_list:
                lines.append(f"    - {c}")

    sensitive = data.get("sensitive_files_detected", [])
    if sensitive:
        lines.append("")
        lines.append("--- SECURITY NOTICE ---")
        lines.append(f"  {data.get('security_note')}")
        lines.append(f"  Detected sensitive files: {', '.join(sensitive)}")

    lines.append("")
    lines.append("--- REPOSITORY DIRECTORY TREE ---")
    tree = data.get("tree", {})
    tree_lines = format_tree_text(tree)
    if tree_lines:
        lines.extend(tree_lines[:100])
        if len(tree_lines) > 100:
            lines.append(f"  ... ({len(tree_lines) - 100} more items truncated)")
    else:
        lines.append("  (Directory is empty)")

    lines.append("=" * 70)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lightweight deterministic repository scanner for HolyShitItWorks."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Path to repository root (defaults to current working directory).",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Maximum depth to inspect directory tree (default: 3).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw JSON instead of human-readable text.",
    )

    args = parser.parse_args()

    data = scan_repository(args.root, max_depth=args.depth)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_human_readable(data))

    if data.get("status") != "OK":
        sys.exit(1)


if __name__ == "__main__":
    main()
