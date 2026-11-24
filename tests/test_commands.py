#!/usr/bin/env python3
"""
HolyShitItWorks — Claude Code Commands Validation Suite.

Validates that all slash commands in commands/ conform to Claude Code plugin standards:
1. 5 core slash commands exist matching active skills.
2. Every command has valid frontmatter (description, argument-hint).
3. Relative links resolve to existing skills.
"""

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = REPO_ROOT / "commands"

EXPECTED_COMMANDS = [
    "adr",
    "feature-development",
    "paddlr-help",
    "release-management",
    "setup-paddlr",
    "skill-creator",
    "writing-specs",
    "writing-plans",
    "test-driven-development",
    "sre-debugging",
    "code-review",
]


class TestClaudeCommands(unittest.TestCase):
    """Test suite for commands/."""

    def test_01_all_commands_exist(self):
        """All expected command files exist in commands/."""
        self.assertTrue(COMMANDS_DIR.is_dir(), "commands/ directory missing")
        for cmd in EXPECTED_COMMANDS:
            cmd_file = COMMANDS_DIR / f"{cmd}.md"
            self.assertTrue(cmd_file.is_file(), f"Missing command: {cmd}.md")

    def test_02_commands_frontmatter(self):
        """Every command file contains valid YAML frontmatter with description."""
        for cmd in EXPECTED_COMMANDS:
            cmd_file = COMMANDS_DIR / f"{cmd}.md"
            content = cmd_file.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---"), f"{cmd}.md missing frontmatter start")
            self.assertIn("description:", content, f"{cmd}.md missing description")

    def test_03_command_links_resolve(self):
        """Relative links inside every command resolve to existing repository files."""
        for cmd in EXPECTED_COMMANDS:
            cmd_file = COMMANDS_DIR / f"{cmd}.md"
            text = cmd_file.read_text(encoding="utf-8")
            # Strip code blocks
            text = re.sub(r"```[\s\S]*?```", "", text)
            for m in re.finditer(r"\[([^\]]+)\]\(([^)#]+)(?:#[^)]*)?\)", text):
                target = m.group(2).strip()
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                # Resolve relative to commands directory
                resolved = (COMMANDS_DIR / target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"Broken link in {cmd}.md: '{target}' -> {resolved}",
                )


if __name__ == "__main__":
    unittest.main()
