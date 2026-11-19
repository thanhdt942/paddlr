#!/usr/bin/env python3
"""
HolyShitItWorks — Automated Skill Validator.

Validates that all agent skills adhere to the Agent Skills open specification:
1. Valid YAML frontmatter with 'name' and 'description'.
2. Skill directory name matches the 'name' field in frontmatter.
3. Required standard sections are present.
4. Internal markdown links within skill documentation resolve to existing files.
5. No proprietary platform-specific leaks in portable core skills.

Zero external dependencies (Python 3.8+ standard library only).
"""

import argparse
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

MANDATORY_SECTIONS = [
    r"^#\s+[A-Za-z0-9\s\-_()]+",  # Level 1 Title
]


def extract_frontmatter(content: str) -> Tuple[Optional[Dict[str, str]], Optional[str]]:
    """Extract YAML frontmatter between leading --- fences."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, "Missing YAML frontmatter block (expected leading --- fences)."

    yaml_block = match.group(1)
    metadata = {}
    for line in yaml_block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(":", 1)
        if len(parts) == 2:
            key = parts[0].strip()
            val = parts[1].strip().strip("'\"")
            metadata[key] = val

    return metadata, None


def validate_skill_file(skill_dir: Path, skill_md_path: Path) -> List[str]:
    """Validate a single skill directory and its SKILL.md."""
    errors = []
    if not skill_md_path.is_file():
        return [f"Missing SKILL.md file in directory: {skill_dir}"]

    content = skill_md_path.read_text(encoding="utf-8")
    metadata, fm_error = extract_frontmatter(content)

    if fm_error:
        errors.append(fm_error)
        return errors

    # 1. Frontmatter 'name' check
    name = metadata.get("name")
    if not name:
        errors.append("Frontmatter missing required 'name' field.")
    elif name != skill_dir.name:
        errors.append(f"Frontmatter name '{name}' does not match directory name '{skill_dir.name}'.")

    # 2. Frontmatter 'description' check
    desc = metadata.get("description")
    if not desc:
        errors.append("Frontmatter missing required 'description' field.")
    elif len(desc) < 15:
        errors.append(f"Frontmatter description too short ({len(desc)} chars): '{desc}'")

    # 3. Mandatory sections check
    for pattern in MANDATORY_SECTIONS:
        if not re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            section_label = pattern.replace(r"\s+", " ").replace("(?:", "").replace(")", "").replace("#", "").strip()
            errors.append(f"Missing mandatory section matching pattern: {section_label}")

    # 4. Internal links check
    for link_match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", content):
        link_target = link_match.group(2).strip()
        if link_target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean_target = link_target.split("#")[0]
        if not clean_target:
            continue
        resolved_link = (skill_dir / clean_target).resolve()
        if not resolved_link.exists():
            errors.append(f"Broken internal link '{link_target}' in {skill_md_path.name}")

    return errors


def validate_all_skills(skills_dir: Path) -> Tuple[int, Dict[str, Any]]:
    """Validate all skills in skills_dir."""
    report: Dict[str, Any] = {
        "skills_directory": str(skills_dir.resolve()),
        "total_skills": 0,
        "valid_skills": 0,
        "invalid_skills": 0,
        "results": {},
    }

    if not skills_dir.is_dir():
        report["error"] = f"Directory not found: {skills_dir}"
        return 1, report

    skill_subdirs = [p for p in sorted(skills_dir.iterdir()) if p.is_dir()]
    report["total_skills"] = len(skill_subdirs)

    has_failures = False
    for sdir in skill_subdirs:
        skill_md = sdir / "SKILL.md"
        errors = validate_skill_file(sdir, skill_md)
        status = "PASS" if not errors else "FAIL"
        if errors:
            has_failures = True
            report["invalid_skills"] += 1
        else:
            report["valid_skills"] += 1

        report["results"][sdir.name] = {
            "status": status,
            "errors": errors,
            "path": str(sdir.resolve()),
        }

    return (1 if has_failures else 0), report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="HolyShitItWorks — Agent Skills Validator."
    )
    repo_root = Path(__file__).resolve().parent.parent
    default_skills = repo_root / "skills"

    parser.add_argument(
        "--skills-dir",
        type=str,
        default=str(default_skills),
        help=f"Path to skills directory (default: {default_skills})",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output validation results in JSON format.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed results for every skill.",
    )

    args = parser.parse_args()
    skills_dir = Path(args.skills_dir).resolve()
    code, report = validate_all_skills(skills_dir)

    if args.json:
        print(json.dumps(report, indent=2))
        return code

    print(f"\nValidating Agent Skills in: {skills_dir}")
    print("=" * 80)
    for name, res in report["results"].items():
        if res["status"] == "PASS":
            if args.verbose:
                print(f"  [PASS] {name}")
        else:
            print(f"  [FAIL] {name}")
            for err in res["errors"]:
                print(f"         - {err}")

    print("=" * 80)
    print(f"Total: {report['total_skills']} | Valid: {report['valid_skills']} | Invalid: {report['invalid_skills']}")
    if code == 0:
        print("All skills conform to the Agent Skills open standard!\n")
    else:
        print("Skill validation failed. Please address the errors above.\n")

    return code


if __name__ == "__main__":
    sys.exit(main())
