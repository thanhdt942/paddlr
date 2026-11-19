#!/usr/bin/env python3
"""Check internal Markdown links across the repository."""

import re
import sys
from pathlib import Path


def check_markdown_links() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    broken = []

    for p in repo_root.rglob("*.md"):
        # Ignore dotfiles, virtual environments, cache, build dirs
        if any(
            part.startswith(".")
            or part in ("__pycache__", "dist", "build", "packaging", "node_modules")
            for part in p.parts
        ):
            continue

        # rules/ is installed at the user's project root; its links target that layout
        rel_parts = p.relative_to(repo_root).parts
        if rel_parts and rel_parts[0] == "rules":
            continue

        text = p.read_text(encoding="utf-8")
        clean_text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        clean_text = re.sub(r"`[^`\n]+`", "", clean_text)

        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", clean_text):
            link = m.group(2).strip()
            if link.startswith(("http://", "https://", "mailto:", "#", "file://", "conversation://")):
                continue
            clean = link.split("#")[0]
            if not clean:
                continue
            resolved = (p.parent / clean).resolve()
            if not resolved.exists():
                broken.append((str(p.relative_to(repo_root)), link, str(resolved)))

    if broken:
        print(f"Found {len(broken)} broken Markdown link(s):")
        for src, lk, res in broken:
            print(f"  {src} -> {lk} (resolved: {res})")
        return 1

    print("All Markdown internal links resolve successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(check_markdown_links())
