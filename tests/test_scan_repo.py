"""
Tests for HolyShitItWorks — Repository Scanner and Skills (Phase 1)

Validates scripts/scan_repo.py and skills contracts across 10+ required scenarios
using isolated temporary fixtures to ensure strictly non-destructive operations.
"""

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

# Add project root to sys.path so scripts can be imported directly
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.scan_repo import scan_repository, format_human_readable, is_sensitive_filename


class TestRepositoryScanner(unittest.TestCase):
    """Scenario tests for scripts/scan_repo.py."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="hsiw_test_repo_")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_01_empty_repository(self):
        """Scenario 1: Empty repository scan."""
        data = scan_repository(self.temp_dir, max_depth=3)
        self.assertEqual(data["status"], "OK")
        self.assertEqual(data["summary"]["top_level_directory_count"], 0)
        self.assertEqual(data["summary"]["top_level_file_count"], 0)
        self.assertEqual(data["detected_technologies"], {})
        self.assertEqual(data["tree"]["children"], [])

    def test_02_typical_python_repository(self):
        """Scenario 2: Typical Python repository with pyproject.toml and tests."""
        pyproject = Path(self.temp_dir) / "pyproject.toml"
        pyproject.write_text(
            "[project]\nname = 'sample-app'\nversion = '0.1.0'\n\n[tool.pytest.ini_options]\nminversion = '7.0'\n",
            encoding="utf-8",
        )
        src_dir = Path(self.temp_dir) / "src" / "sample"
        src_dir.mkdir(parents=True)
        (src_dir / "__init__.py").write_text("", encoding="utf-8")
        (src_dir / "main.py").write_text("print('hello')", encoding="utf-8")

        tests_dir = Path(self.temp_dir) / "tests"
        tests_dir.mkdir()
        (tests_dir / "test_main.py").write_text("def test_ok(): pass", encoding="utf-8")

        data = scan_repository(self.temp_dir, max_depth=3)
        self.assertEqual(data["status"], "OK")
        self.assertIn("Python", data["detected_technologies"])
        self.assertIn("pyproject.toml", data["detected_technologies"]["Python"])
        self.assertTrue(data["project_context_indicators"]["has_tests_dir"])
        self.assertIn("python tooling indicators", data["discovered_commands"])

    def test_03_typical_javascript_typescript_repository(self):
        """Scenario 3: Typical JS/TS repository with package.json and tsconfig.json."""
        pkg = Path(self.temp_dir) / "package.json"
        pkg.write_text(
            json.dumps({"name": "web-app", "scripts": {"build": "tsc", "test": "vitest"}}),
            encoding="utf-8",
        )
        (Path(self.temp_dir) / "tsconfig.json").write_text("{}", encoding="utf-8")
        src_dir = Path(self.temp_dir) / "src"
        src_dir.mkdir()
        (src_dir / "index.ts").write_text("console.log('web')", encoding="utf-8")

        data = scan_repository(self.temp_dir, max_depth=3)
        self.assertEqual(data["status"], "OK")
        self.assertIn("JavaScript / TypeScript", data["detected_technologies"])
        self.assertIn("package.json", data["detected_technologies"]["JavaScript / TypeScript"])
        self.assertIn("npm / pnpm / yarn scripts", data["discovered_commands"])
        scripts = data["discovered_commands"]["npm / pnpm / yarn scripts"]
        self.assertTrue(any("test: vitest" in s for s in scripts))

    def test_04_multi_language_repository(self):
        """Scenario 4: Multi-language repository with Python and Go."""
        (Path(self.temp_dir) / "pyproject.toml").write_text("", encoding="utf-8")
        (Path(self.temp_dir) / "go.mod").write_text("module example.com/service\n", encoding="utf-8")

        data = scan_repository(self.temp_dir, max_depth=3)
        self.assertEqual(data["status"], "OK")
        self.assertIn("Python", data["detected_technologies"])
        self.assertIn("Go", data["detected_technologies"])

    def test_05_ignored_and_generated_directories(self):
        """Scenario 5: Pruning of generated/ignored directories (node_modules, .venv, .git)."""
        node_modules = Path(self.temp_dir) / "node_modules" / "some-lib"
        node_modules.mkdir(parents=True)
        (node_modules / "index.js").write_text("hidden", encoding="utf-8")

        venv_dir = Path(self.temp_dir) / ".venv" / "bin"
        venv_dir.mkdir(parents=True)
        (venv_dir / "python").write_text("bin", encoding="utf-8")

        git_dir = Path(self.temp_dir) / ".git" / "objects"
        git_dir.mkdir(parents=True)
        (git_dir / "abc").write_text("obj", encoding="utf-8")

        src_dir = Path(self.temp_dir) / "src"
        src_dir.mkdir()
        (src_dir / "app.py").write_text("code", encoding="utf-8")

        data = scan_repository(self.temp_dir, max_depth=3)
        self.assertEqual(data["status"], "OK")
        child_names = [c["name"] for c in data["tree"]["children"]]
        self.assertNotIn("node_modules", child_names)
        self.assertNotIn(".venv", child_names)
        self.assertNotIn(".git", child_names)
        self.assertIn("src", child_names)

    def test_06_sensitive_and_secret_files_protection(self):
        """Scenario 6: Sensitive files detected by name only; content NEVER read or leaked."""
        secret_content = "SUPER_SECRET_AWS_KEY_123456789"
        env_file = Path(self.temp_dir) / ".env"
        env_file.write_text(f"API_KEY={secret_content}\n", encoding="utf-8")

        cred_file = Path(self.temp_dir) / "credentials.json"
        cred_file.write_text(json.dumps({"secret": secret_content}), encoding="utf-8")

        rsa_file = Path(self.temp_dir) / "id_rsa"
        rsa_file.write_text(secret_content, encoding="utf-8")

        data = scan_repository(self.temp_dir, max_depth=3)
        self.assertEqual(data["status"], "OK")
        self.assertIn(".env", data["sensitive_files_detected"])
        self.assertIn("credentials.json", data["sensitive_files_detected"])
        self.assertIn("id_rsa", data["sensitive_files_detected"])

        # Serialize complete JSON output and text output and verify secret is nowhere in it
        json_output = json.dumps(data)
        human_output = format_human_readable(data)
        self.assertNotIn(secret_content, json_output)
        self.assertNotIn(secret_content, human_output)

    def test_07_invalid_repository_path(self):
        """Scenario 7: Graceful error handling for missing or invalid path."""
        non_existent = Path(self.temp_dir) / "does_not_exist"
        data = scan_repository(str(non_existent), max_depth=3)
        self.assertEqual(data["status"], "NOT_FOUND")
        self.assertIn("error", data)

        # File instead of directory
        a_file = Path(self.temp_dir) / "a_file.txt"
        a_file.write_text("content", encoding="utf-8")
        data_file = scan_repository(str(a_file), max_depth=3)
        self.assertEqual(data_file["status"], "NOT_A_DIRECTORY")

    def test_08_json_output_validity(self):
        """Scenario 8: JSON serialization and schema structure."""
        (Path(self.temp_dir) / "README.md").write_text("# Test", encoding="utf-8")
        data = scan_repository(self.temp_dir, max_depth=2)
        json_str = json.dumps(data)
        parsed = json.loads(json_str)
        self.assertEqual(parsed["status"], "OK")
        self.assertIn("repository_root", parsed)
        self.assertIn("tree", parsed)
        self.assertIn("summary", parsed)

    def test_09_configurable_directory_depth(self):
        """Scenario 9: Configurable directory depth limits."""
        # Create 4 levels deep: l1/l2/l3/l4/file.txt
        deep = Path(self.temp_dir) / "l1" / "l2" / "l3" / "l4"
        deep.mkdir(parents=True)
        (deep / "deep.txt").write_text("deep", encoding="utf-8")

        # Scan with depth=1: only l1 should have empty or pruned children
        d1 = scan_repository(self.temp_dir, max_depth=1)
        l1_node = next(c for c in d1["tree"]["children"] if c["name"] == "l1")
        self.assertEqual(len(l1_node.get("children", [])), 0)

        # Scan with depth=3: should reach l3
        d3 = scan_repository(self.temp_dir, max_depth=3)
        l1_node3 = next(c for c in d3["tree"]["children"] if c["name"] == "l1")
        l2_node3 = next(c for c in l1_node3["children"] if c["name"] == "l2")
        l3_node3 = next(c for c in l2_node3["children"] if c["name"] == "l3")
        self.assertEqual(len(l3_node3.get("children", [])), 0)

    def test_10_read_only_behavior(self):
        """Scenario 10: Scanner leaves target repository completely unmodified."""
        marker = Path(self.temp_dir) / "sample.py"
        marker.write_text("x = 1", encoding="utf-8")
        mtime_before = marker.stat().st_mtime_ns
        entries_before = sorted(os.listdir(self.temp_dir))

        # Perform scan
        _ = scan_repository(self.temp_dir, max_depth=3)

        entries_after = sorted(os.listdir(self.temp_dir))
        mtime_after = marker.stat().st_mtime_ns

        self.assertEqual(entries_before, entries_after)
        self.assertEqual(mtime_before, mtime_after)


class TestSkillsFrontmatterAndContracts(unittest.TestCase):
    """Validates skills syntax, frontmatter, and structural integrity."""

    def test_skill_writing_specs_format(self):
        skill_path = REPO_ROOT / "skills" / "writing-specs" / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        content = skill_path.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"))
        self.assertIn("name: writing-specs", content)
        self.assertIn("description:", content)
        self.assertIn("# Writing Specifications", content)
        self.assertIn("## Overview", content)

    def test_skill_writing_plans_format(self):
        skill_path = REPO_ROOT / "skills" / "writing-plans" / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        content = skill_path.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"))
        self.assertIn("name: writing-plans", content)
        self.assertIn("description:", content)
        self.assertIn("# Writing Plans", content)
        self.assertIn("## Overview", content)

    def test_skill_tdd_format(self):
        skill_path = REPO_ROOT / "skills" / "test-driven-development" / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        content = skill_path.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---"))
        self.assertIn("name: test-driven-development", content)
        self.assertIn("description:", content)
        self.assertIn("# Test-Driven Development (TDD)", content)
        self.assertIn("## The Iron Law", content)


if __name__ == "__main__":
    unittest.main()
