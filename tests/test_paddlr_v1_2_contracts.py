#!/usr/bin/env python3
"""Contract and regression tests for Paddlr v1.2.0 upgrade."""

from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
PADDLR_MODE_DIR = SKILLS_DIR / "paddlr-mode"


class TestPaddlrV12Contracts(unittest.TestCase):
    """Verify v1.2.0 contracts, skills, principles, and hygiene invariants."""

    def test_ui_todo_primitive_documented(self):
        """ui.todo primitive is mapped across all supported runtimes and sync rule is defined."""
        adapters = (PADDLR_MODE_DIR / "references" / "runtime-adapters.md").read_text(encoding="utf-8")
        contracts = (PADDLR_MODE_DIR / "references" / "core-contracts.md").read_text(encoding="utf-8")
        schema = (PADDLR_MODE_DIR / "references" / "task-state-schema.md").read_text(encoding="utf-8")
        mode = (PADDLR_MODE_DIR / "SKILL.md").read_text(encoding="utf-8")

        for token in ("ui.todo", "TodoWrite", "update_steps", "update_plan", "todowrite"):
            self.assertIn(token, adapters, f"Missing '{token}' in runtime-adapters.md")
        self.assertIn("ui.todo", contracts)
        self.assertIn("ui.todo", schema)
        self.assertIn("ui.todo", mode)

    def test_no_legacy_upstream_agent_references(self):
        """Zero legacy upstream worker names remain in skills, rules, commands, hooks, tests, or scripts."""
        forbidden = "pot" + "eto"
        scan_roots = ("skills", "rules", "commands", "hooks", "tests", "scripts")
        hits = []
        for root_name in scan_roots:
            base = REPO_ROOT / root_name
            if not base.exists():
                continue
            for path in base.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.suffix not in (".md", ".py", ".ts", ".js", ".json", ".sh"):
                    continue
                text = path.read_text(encoding="utf-8", errors="ignore").lower()
                if forbidden in text:
                    hits.append(str(path.relative_to(REPO_ROOT)))
        self.assertEqual(hits, [], f"Found legacy upstream references in: {hits}")

    def test_paddlr_mode_boundaries_and_level1_exemption(self):
        """paddlr-mode uses paddlr-worker, exempts Level 1 from plans, and states skill vs playbook boundaries."""
        mode = (PADDLR_MODE_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("paddlr-worker", mode)
        self.assertIn("Level 1", mode)
        for token in ("feature-development", "sre-debugging", "code-review", "interrogate"):
            self.assertIn(token, mode, f"Missing boundary reference '{token}' in paddlr-mode/SKILL.md")

    def test_adr_and_sync_docs_closure(self):
        """writing-decisions, sync-docs, opening-a-pr gate, and spec-aware why are wired."""
        adr_skill = SKILLS_DIR / "writing-decisions" / "SKILL.md"
        sync_skill = SKILLS_DIR / "sync-docs" / "SKILL.md"
        self.assertTrue(adr_skill.is_file(), "Missing skills/writing-decisions/SKILL.md")
        self.assertTrue(sync_skill.is_file(), "Missing skills/sync-docs/SKILL.md")

        adr_text = adr_skill.read_text(encoding="utf-8")
        sync_text = sync_skill.read_text(encoding="utf-8")
        self.assertIn("disable-model-invocation: true", adr_text)
        self.assertIn("disable-model-invocation: true", sync_text)
        self.assertIn(".paddlr.json", adr_text)
        self.assertIn(".paddlr.json", sync_text)

        opening_pr = (PADDLR_MODE_DIR / "playbooks" / "opening-a-pr.md").read_text(encoding="utf-8")
        self.assertIn("sync-docs", opening_pr)

        why_text = (SKILLS_DIR / "why" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("specs/", why_text)
        self.assertIn(".paddlr.json", why_text)

    def test_26_principles_exist_and_indexed(self):
        """All 26 lazy-loaded principle skills exist and the 2 new SDD principles are indexed."""
        principle_dirs = sorted(p for p in SKILLS_DIR.glob("principle-*") if p.is_dir())
        self.assertEqual(len(principle_dirs), 26, f"Expected 26 principles, found {len(principle_dirs)}")
        for pdir in principle_dirs:
            text = (pdir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("disable-model-invocation: true", text, f"{pdir.name} must be lazy-loaded")

        mode = (PADDLR_MODE_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("**Spec Before Code.**", mode)
        self.assertIn("**Record Decisions Immutably.**", mode)

    def test_craft_skills_exist_and_agent_agnostic(self):
        """no-comments, unslop, and correct exist, are lazy-loaded, and stay agent-agnostic."""
        for skill_name in ("no-comments", "unslop", "correct"):
            skill_path = SKILLS_DIR / skill_name / "SKILL.md"
            self.assertTrue(skill_path.is_file(), f"Missing skills/{skill_name}/SKILL.md")
            text = skill_path.read_text(encoding="utf-8")
            self.assertIn("disable-model-invocation: true", text, f"{skill_name} must be lazy-loaded")
            self.assertNotIn("cursor-team-kit", text)

        sicko = SKILLS_DIR / "no-comments" / "comment-sicko.md"
        self.assertTrue(sicko.is_file(), "Missing skills/no-comments/comment-sicko.md")
        no_comments_text = (SKILLS_DIR / "no-comments" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("agent.delegate", no_comments_text)
        self.assertIn("Single-Agent", no_comments_text)
        self.assertNotIn("Spawn `Task`", no_comments_text)

    def test_user_guide_exists_and_linked_from_readme(self):
        """User-facing docs/guide/ handbook exists with all 6 chapters and is linked from README.md."""
        guide_dir = REPO_ROOT / "docs" / "guide"
        expected_files = (
            "README.md",
            "01-setup.md",
            "02-paddlr-mode.md",
            "03-specs-plans-adrs.md",
            "04-autonomy-and-verification.md",
            "05-principles-and-skills.md",
            "06-customization.md",
        )
        for filename in expected_files:
            path = guide_dir / filename
            self.assertTrue(path.is_file(), f"Missing docs/guide/{filename}")
            self.assertGreater(path.stat().st_size, 150, f"docs/guide/{filename} is too short")

        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/guide/README.md", readme)


if __name__ == "__main__":
    unittest.main()
