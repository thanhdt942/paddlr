#!/usr/bin/env python3
"""
HolyShitItWorks — Core Skills Architecture Test Suite.

Validates the active 5-Skill architecture:
1. Five skills exist (writing-specs, writing-plans, test-driven-development, sre-debugging, code-review).
2. Each skill has a valid SKILL.md with proper YAML frontmatter (name, description).
3. Core engineering methodologies (TDD, SRE Scientific Debugging, Specs, Plans, Code Review) are fully retained.
4. All associated reference guides, prompt templates, and helper files exist and are populated.
"""

from pathlib import Path
import re
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

EXPECTED_SKILLS = [
    "code-review",
    "feature-development",
    "release-management",
    "skill-creator",
    "sre-debugging",
    "test-driven-development",
    "writing-plans",
    "writing-specs",
]


class TestCoreSkillsArchitecture(unittest.TestCase):
    """Test verification suite for the Five Skills architecture."""

    def test_01_all_five_skills_exist(self):
        """Verify that all five skills exist as directories with SKILL.md files."""
        self.assertTrue(SKILLS_DIR.is_dir(), "skills/ directory missing")
        for skill_name in EXPECTED_SKILLS:
            skill_path = SKILLS_DIR / skill_name
            self.assertTrue(
                skill_path.is_dir(),
                f"Skill directory missing: {skill_path}",
            )
            skill_md = skill_path / "SKILL.md"
            self.assertTrue(
                skill_md.is_file(),
                f"Missing SKILL.md in skill: {skill_name}",
            )

    def test_02_skills_valid_frontmatter(self):
        """Verify each skill has valid YAML frontmatter matching directory name."""
        for skill_name in EXPECTED_SKILLS:
            skill_md = SKILLS_DIR / skill_name / "SKILL.md"
            content = skill_md.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---"), f"{skill_name}/SKILL.md missing frontmatter start")
            self.assertIn(f"name: {skill_name}", content, f"{skill_name} frontmatter name mismatch")
            self.assertIn("description:", content, f"{skill_name} missing description in frontmatter")

    def test_03_skills_entrypoints_substantive(self):
        """Verify that each skill entrypoint SKILL.md is populated and non-empty."""
        for skill_name in EXPECTED_SKILLS:
            skill_md = SKILLS_DIR / skill_name / "SKILL.md"
            lines = skill_md.read_text(encoding="utf-8").splitlines()
            self.assertGreater(
                len(lines),
                50,
                f"Skill {skill_name}/SKILL.md is too short: {len(lines)} lines",
            )

    def test_04_writing_specs_methodology_retained(self):
        """Verify writing-specs retains specification structure, requirements discovery, and ADR guide."""
        skill_dir = SKILLS_DIR / "writing-specs"
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("# Writing Specifications", content)
        self.assertIn("Scope Check", content)
        self.assertIn("Discovery", content)
        self.assertIn("Acceptance Criteria", content)
        self.assertIn("Confirmed Technical Decisions & Design Choices", content)
        self.assertIn("Architectural Decisions (ADR Recording)", content)
        self.assertIn("adr-guide.md", content)
        adr_guide = skill_dir / "references" / "adr-guide.md"
        self.assertTrue(adr_guide.is_file(), "Missing references/adr-guide.md in writing-specs")
        self.assertGreater(adr_guide.stat().st_size, 100)

    def test_05_writing_plans_methodology_retained(self):
        """Verify writing-plans retains task right-sizing and step granularity."""
        skill_md = SKILLS_DIR / "writing-plans" / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("# Writing Plans", content)
        self.assertIn("File Structure", content)
        self.assertIn("Task Right-Sizing", content)
        self.assertIn("Step Granularity", content)
        self.assertIn("Key Decisions", content)
        self.assertIn("Honor Confirmed Decisions", content)

    def test_06_tdd_methodology_retained(self):
        """Verify test-driven-development retains Iron Law, Red-Green-Refactor, and helper guide."""
        skill_dir = SKILLS_DIR / "test-driven-development"
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST", content)
        self.assertIn("RED", content)
        self.assertIn("GREEN", content)
        self.assertIn("REFACTOR", content)

        guide = skill_dir / "writing_good_tests.md"
        self.assertTrue(guide.is_file(), "writing_good_tests.md missing in test-driven-development")
        guide_content = guide.read_text(encoding="utf-8")
        self.assertGreater(len(guide_content.splitlines()), 50)

    def test_07_sre_debugging_methodology_retained(self):
        """Verify sre-debugging retains scientific troubleshooting, 4 phases, and references."""
        skill_dir = SKILLS_DIR / "sre-debugging"
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("NO PERMANENT FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST", content)
        self.assertIn("Phase 1: Root Cause Investigation", content)
        self.assertIn("Phase 2: Pattern & Differential Analysis", content)
        self.assertIn("Phase 3: Hypothesis & Experiments", content)
        self.assertIn("Phase 4: Implementation & Verification", content)

        refs_dir = skill_dir / "references"
        self.assertTrue(refs_dir.is_dir(), "references/ missing in sre-debugging")
        for ref_file in [
            "hypothesis-log-template.md",
            "performance-methods.md",
            "zeller-techniques.md",
        ]:
            ref_path = refs_dir / ref_file
            self.assertTrue(ref_path.is_file(), f"Missing SRE reference: {ref_file}")
            self.assertGreater(ref_path.stat().st_size, 100)

    def test_08_code_review_methodology_retained(self):
        """Verify code-review retains reviewer subagent flow and prompt template."""
        skill_dir = SKILLS_DIR / "code-review"
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("Code Review", content)
        self.assertIn("When to Run Code Review", content)
        self.assertIn("Dispatch the Reviewer Subagent", content)

        reviewer_template = skill_dir / "code-reviewer.md"
        self.assertTrue(reviewer_template.is_file(), "code-reviewer.md template missing")
        self.assertGreater(reviewer_template.stat().st_size, 100)

    def test_09_feature_development_orchestrator_retained(self):
        """Verify feature-development coordinates companion skills and references exist."""
        skill_dir = SKILLS_DIR / "feature-development"
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("Feature Development", content)
        self.assertIn("Workflow Overview", content)
        self.assertIn("writing-specs", content)
        self.assertIn("writing-plans", content)
        self.assertIn("test-driven-development", content)
        self.assertIn("DECISIONS.md", content)

        refs_dir = skill_dir / "references"
        self.assertTrue(refs_dir.is_dir(), "references/ missing in feature-development")
        for ref_file in [
            "completion-checklist.md",
            "implementation-guidelines.md",
            "workflow-decisions.md",
        ]:
            ref_path = refs_dir / ref_file
            self.assertTrue(ref_path.is_file(), f"Missing feature-development reference: {ref_file}")
            self.assertGreater(ref_path.stat().st_size, 100)
        self.assertIn("ADR Gate", (refs_dir / "workflow-decisions.md").read_text(encoding="utf-8"))

    def test_10_release_management_methodology_retained(self):
        """Verify release-management retains release workflow and RELEASE.md config."""
        skill_dir = SKILLS_DIR / "release-management"
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("Release Management", content)
        self.assertIn("RELEASE.md", content)
        self.assertIn("Release Workflow", content)
        self.assertIn("Safety & Authorization", content)

    def test_11_skill_creator_methodology_retained(self):
        """Verify skill-creator retains authoring principles, references, and workflow."""
        skill_dir = SKILLS_DIR / "skill-creator"
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")
        self.assertIn("Skill Creator", content)
        self.assertIn("Progressive disclosure", content)
        self.assertIn("Workflow", content)
        self.assertIn("skill-anatomy.md", content)
        self.assertIn("testing-guide.md", content)
        refs_dir = skill_dir / "references"
        self.assertTrue(refs_dir.is_dir(), "Missing references dir in skill-creator")
        self.assertTrue((refs_dir / "skill-anatomy.md").is_file())
        self.assertTrue((refs_dir / "testing-guide.md").is_file())


if __name__ == "__main__":
    unittest.main()
