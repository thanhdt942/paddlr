#!/usr/bin/env python3
"""Unit tests for setup-paddlr and paddlr-help skills."""

from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"


class TestSetupAndHelpSkills(unittest.TestCase):
    """Validate contracts for setup-paddlr and paddlr-help."""

    def test_setup_paddlr_contract(self):
        skill_path = SKILLS_DIR / "setup-paddlr" / "SKILL.md"
        self.assertTrue(skill_path.is_file(), "Missing skills/setup-paddlr/SKILL.md")
        text = skill_path.read_text(encoding="utf-8")

        # Must NOT disable model invocation so natural-language setup triggers work
        self.assertNotIn("disable-model-invocation: true", text)
        self.assertIn("name: setup-paddlr", text)

        # Must cover docs/paddlr/ init and .paddlr.json detection/compatibility
        for token in (
            "docs/paddlr/",
            "specs/",
            "plans/",
            "decisions/",
            "DECISIONS.md",
            "PROJECT.md",
            "docs/adr/",
            "docs/specs/",
            ".paddlr.json",
            "paddlr_config.py",
        ):
            self.assertIn(token, text, f"Missing '{token}' in setup-paddlr/SKILL.md")

        # Must cover the 3 model profiles and graceful skip
        for profile in ("deep-reasoning", "standard-code", "fast-mechanical", "runtime-adapters.md"):
            self.assertIn(profile, text, f"Missing '{profile}' in setup-paddlr/SKILL.md")

        # Must offer optional /create-verification-skill
        self.assertIn("/create-verification-skill", text)

        # Must remain agent-agnostic
        self.assertNotIn("cursor-team-kit", text)
        self.assertNotIn("pstack-models.mdc", text)

    def test_paddlr_help_contract(self):
        skill_path = SKILLS_DIR / "paddlr-help" / "SKILL.md"
        self.assertTrue(skill_path.is_file(), "Missing skills/paddlr-help/SKILL.md")
        text = skill_path.read_text(encoding="utf-8")

        # Must be lazy-loaded (explicit slash command only)
        self.assertIn("disable-model-invocation: true", text)
        self.assertIn("name: paddlr-help", text)

        # Must enforce read-only advisory (never execute the task)
        self.assertIn("read-only", text.lower())
        self.assertIn("do not execute", text.lower())

        # Must reference skills, playbooks, 26 principles, docs/guide/, and copy-paste prompt
        for token in ("paddlr-mode", "26", "docs/guide/", "prompt"):
            self.assertIn(token, text, f"Missing '{token}' in paddlr-help/SKILL.md")

        # Must remain agent-agnostic
        self.assertNotIn("cursor-team-kit", text)

    def test_docs_reference_setup_and_help(self):
        setup_guide = (REPO_ROOT / "docs" / "guide" / "01-setup.md").read_text(encoding="utf-8")
        skills_guide = (REPO_ROOT / "docs" / "guide" / "05-principles-and-skills.md").read_text(encoding="utf-8")
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("setup-paddlr", setup_guide)
        self.assertIn("paddlr-help", setup_guide)
        self.assertIn("setup-paddlr", skills_guide)
        self.assertIn("paddlr-help", skills_guide)
        self.assertIn("setup-paddlr", readme)
        self.assertIn("paddlr-help", readme)

    def test_only_setup_paddlr_allows_auto_model_invocation(self):
        """Across all skills, setup-paddlr is the only skill omitting disable-model-invocation: true."""
        auto_invocable = []
        for skill_md in sorted(SKILLS_DIR.glob("*/SKILL.md")):
            text = skill_md.read_text(encoding="utf-8")
            if "disable-model-invocation: true" not in text:
                auto_invocable.append(skill_md.parent.name)
        self.assertEqual(auto_invocable, ["setup-paddlr"])


if __name__ == "__main__":
    unittest.main()
