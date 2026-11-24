"""
Tests for HolyShitItWorks — Engineering Workflow & Scenarios (Phase 2)

Validates workflow classification rules, approval gate logic, skill contracts,
and the 10 required scenario simulations using Python standard library.
"""

import os
import sys
import unittest
from pathlib import Path

# Add project root to sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


class WorkflowClassificationEngine:
    """Deterministic simulation engine modeling the HolyShitItWorks classification rules."""

    @staticmethod
    def classify_task(
        title: str,
        files_affected: int,
        is_typo_or_doc: bool = False,
        touches_db_schema: bool = False,
        touches_auth_or_security: bool = False,
        crosses_multiple_modules: bool = False,
        has_breaking_changes: bool = False,
        has_external_integration: bool = False,
        is_ambiguous: bool = False,
        multiple_approaches_exist: bool = False,
    ) -> dict:
        """Evaluate task risk and return workflow level, required steps, and gates."""
        # Baseline classification
        if touches_db_schema or touches_auth_or_security or has_breaking_changes:
            level = 3
            workflow = "workflows/architectural-change.md"
            requires_brainstorming = True
            requires_spec = True
            requires_design = True
            requires_plan = True
            requires_approval_before_code = True
        elif crosses_multiple_modules or has_external_integration:
            level = 2
            workflow = "workflows/feature-development.md"
            requires_brainstorming = multiple_approaches_exist
            requires_spec = True
            requires_design = True
            requires_plan = True
            requires_approval_before_code = is_ambiguous
        elif is_typo_or_doc or files_affected <= 1:
            level = 1
            workflow = "workflows/small-change.md"
            requires_brainstorming = False
            requires_spec = False
            requires_design = False
            requires_plan = False
            requires_approval_before_code = False  # Approved on diff review
        else:
            level = 2
            workflow = "workflows/feature-development.md"
            requires_brainstorming = multiple_approaches_exist
            requires_spec = True
            requires_design = True
            requires_plan = True
            requires_approval_before_code = is_ambiguous

        return {
            "title": title,
            "level": level,
            "workflow": workflow,
            "requires_clarification": is_ambiguous,
            "requires_brainstorming": requires_brainstorming,
            "requires_formal_spec": requires_spec,
            "requires_technical_design": requires_design,
            "requires_implementation_plan": requires_plan,
            "requires_approval_before_code": requires_approval_before_code,
        }

    @staticmethod
    def escalate_task(initial_result: dict, discovered_factor: str) -> dict:
        """Simulate dynamic escalation when new risk factors are discovered."""
        updated = dict(initial_result)
        if discovered_factor in ("db_migration", "breaking_change", "security_redesign"):
            updated["level"] = 3
            updated["workflow"] = "workflows/architectural-change.md"
            updated["requires_formal_spec"] = True
            updated["requires_technical_design"] = True
            updated["requires_implementation_plan"] = True
            updated["requires_approval_before_code"] = True
            updated["escalated"] = True
            updated["escalation_reason"] = discovered_factor
        return updated


class TestEngineeringWorkflowScenarios(unittest.TestCase):
    """Scenario simulation tests for the 10 required cases."""

    def test_scenario_01_simple_text_or_config_change(self):
        """Scenario 1: Simple text or config change (Level 1, lightweight, no spec)."""
        res = WorkflowClassificationEngine.classify_task(
            title="Fix typo in README",
            files_affected=1,
            is_typo_or_doc=True,
        )
        self.assertEqual(res["level"], 1)
        self.assertEqual(res["workflow"], "workflows/small-change.md")
        self.assertFalse(res["requires_formal_spec"])
        self.assertFalse(res["requires_brainstorming"])
        self.assertFalse(res["requires_implementation_plan"])

    def test_scenario_02_localized_bug_fix(self):
        """Scenario 2: Localized bug fix with clear root cause (Level 1 / bug-fix)."""
        res = WorkflowClassificationEngine.classify_task(
            title="Fix off-by-one error in calculate_total",
            files_affected=1,
            crosses_multiple_modules=False,
        )
        self.assertEqual(res["level"], 1)
        self.assertEqual(res["workflow"], "workflows/small-change.md")
        self.assertFalse(res["requires_brainstorming"])

    def test_scenario_03_multi_module_feature(self):
        """Scenario 3: Clear reversible Level 2 feature proceeds without blocking for pre-code approval."""
        res = WorkflowClassificationEngine.classify_task(
            title="Implement User Notification Service",
            files_affected=5,
            crosses_multiple_modules=True,
        )
        self.assertEqual(res["level"], 2)
        self.assertEqual(res["workflow"], "workflows/feature-development.md")
        self.assertTrue(res["requires_formal_spec"])
        self.assertTrue(res["requires_technical_design"])
        self.assertTrue(res["requires_implementation_plan"])
        self.assertFalse(res["requires_approval_before_code"])

    def test_scenario_04_new_external_integration(self):
        """Scenario 4: New external integration (Level 2 reversible with multiple approaches, no ambiguity)."""
        res = WorkflowClassificationEngine.classify_task(
            title="Integrate Stripe Payment Gateway",
            files_affected=4,
            has_external_integration=True,
            multiple_approaches_exist=True,
        )
        self.assertEqual(res["level"], 2)
        self.assertTrue(res["requires_brainstorming"])
        self.assertTrue(res["requires_technical_design"])
        self.assertFalse(res["requires_approval_before_code"])

    def test_scenario_05_database_schema_change(self):
        """Scenario 5: Database schema change (Level 3 Architectural Change)."""
        res = WorkflowClassificationEngine.classify_task(
            title="Migrate Users Table to Multi-Tenant Partitioning",
            files_affected=3,
            touches_db_schema=True,
        )
        self.assertEqual(res["level"], 3)
        self.assertEqual(res["workflow"], "workflows/architectural-change.md")
        self.assertTrue(res["requires_brainstorming"])
        self.assertTrue(res["requires_approval_before_code"])

    def test_scenario_06_backward_compatibility_risk(self):
        """Scenario 6: Change with backward-compatibility concerns (Level 3)."""
        res = WorkflowClassificationEngine.classify_task(
            title="Refactor Public REST API Endpoint Signatures",
            files_affected=6,
            has_breaking_changes=True,
        )
        self.assertEqual(res["level"], 3)
        self.assertEqual(res["workflow"], "workflows/architectural-change.md")
        self.assertTrue(res["requires_technical_design"])

    def test_scenario_07_ambiguous_request_missing_requirements(self):
        """Scenario 7: Ambiguous request requiring clarification before planning."""
        res = WorkflowClassificationEngine.classify_task(
            title="Make dashboard faster",
            files_affected=3,
            crosses_multiple_modules=True,
            is_ambiguous=True,
        )
        self.assertTrue(res["requires_clarification"])
        # Must clarify before approving code implementation
        self.assertTrue(res["requires_approval_before_code"])

    def test_scenario_08_multiple_solution_approaches(self):
        """Scenario 8: Task with multiple solution approaches (triggers brainstorming)."""
        res = WorkflowClassificationEngine.classify_task(
            title="Implement Client-Side Caching Layer",
            files_affected=3,
            crosses_multiple_modules=True,
            multiple_approaches_exist=True,
        )
        self.assertTrue(res["requires_brainstorming"])

    def test_scenario_09_straightforward_task_skips_brainstorming(self):
        """Scenario 9: Straightforward task that does not need brainstorming."""
        res = WorkflowClassificationEngine.classify_task(
            title="Add 'middle_name' field to User profile following existing pattern",
            files_affected=2,
            crosses_multiple_modules=True,
            multiple_approaches_exist=False,
        )
        self.assertEqual(res["level"], 2)
        self.assertFalse(res["requires_brainstorming"])
        self.assertTrue(res["requires_implementation_plan"])

    def test_scenario_10_risk_elevation_during_investigation(self):
        """Scenario 10: Task whose risk increases during investigation (Level 1 -> Level 3)."""
        # Starts as localized fix
        initial = WorkflowClassificationEngine.classify_task(
            title="Fix status code for expired sessions",
            files_affected=1,
            is_typo_or_doc=False,
        )
        self.assertEqual(initial["level"], 1)

        # Investigation reveals it requires database schema migration for session table
        escalated = WorkflowClassificationEngine.escalate_task(initial, "db_migration")
        self.assertEqual(escalated["level"], 3)
        self.assertEqual(escalated["workflow"], "workflows/architectural-change.md")
        self.assertTrue(escalated["requires_approval_before_code"])
        self.assertTrue(escalated["escalated"])


class TestActiveSkillsIntegrity(unittest.TestCase):
    """Validates structural integrity, Agent Skills format, and markdown files for active skills."""

    REQUIRED_SKILLS = [
        "code-review",
        "feature-development",
        "release-management",
        "skill-creator",
        "sre-debugging",
        "test-driven-development",
        "writing-plans",
        "writing-specs",
    ]

    def test_all_five_skills_exist_and_conform_to_format(self):
        """Verify Active Skills have valid frontmatter and mandatory sections."""
        for skill in self.REQUIRED_SKILLS:
            skill_path = REPO_ROOT / "skills" / skill / "SKILL.md"
            self.assertTrue(skill_path.is_file(), f"Missing skill file: {skill_path}")
            content = skill_path.read_text(encoding="utf-8")
            self.assertTrue(content.startswith("---"), f"{skill} missing YAML frontmatter")
            self.assertIn(f"name: {skill}", content)
            self.assertIn("description:", content)
            self.assertTrue(
                any(line.startswith("# ") for line in content.splitlines()),
                f"{skill} missing Level 1 heading",
            )

    def test_skill_supporting_files_exist(self):
        """Verify supporting guides and reference files for active skills exist and are non-empty."""
        supporting_files = [
            "skills/code-review/code-reviewer.md",
            "skills/feature-development/references/completion-checklist.md",
            "skills/feature-development/references/implementation-guidelines.md",
            "skills/feature-development/references/workflow-decisions.md",
            "skills/test-driven-development/writing_good_tests.md",
            "skills/sre-debugging/references/hypothesis-log-template.md",
            "skills/sre-debugging/references/performance-methods.md",
            "skills/sre-debugging/references/zeller-techniques.md",
            "skills/writing-specs/references/adr-guide.md",
        ]
        for rel_path in supporting_files:
            file_path = REPO_ROOT / rel_path
            self.assertTrue(file_path.is_file(), f"Missing supporting file: {file_path}")
            self.assertGreater(file_path.stat().st_size, 100, f"File {rel_path} is too small or empty")


if __name__ == "__main__":
    unittest.main()
