#!/usr/bin/env python3
"""Tests for .paddlr.json project memory configuration and path resolution."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.paddlr_config import resolve_autonomy_config, resolve_memory_paths

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestPaddlrConfig(unittest.TestCase):
    """Validate default paths, overrides, and error handling for .paddlr.json."""

    def test_defaults_when_no_config_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            paths = resolve_memory_paths(root)
            self.assertEqual(paths["root"], root / "docs" / "paddlr")
            self.assertEqual(paths["specs"], root / "docs" / "paddlr" / "specs")
            self.assertEqual(paths["plans"], root / "docs" / "paddlr" / "plans")
            self.assertEqual(paths["decisions"], root / "docs" / "paddlr" / "decisions")
            self.assertEqual(paths["decisionsIndex"], root / "docs" / "paddlr" / "DECISIONS.md")
            self.assertEqual(paths["project"], root / "docs" / "paddlr" / "PROJECT.md")

    def test_custom_root_cascades_to_unspecified_subpaths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / ".paddlr.json").write_text(
                json.dumps({"root": ".paddlr-docs"}),
                encoding="utf-8",
            )
            paths = resolve_memory_paths(root)
            self.assertEqual(paths["root"], root / ".paddlr-docs")
            self.assertEqual(paths["specs"], root / ".paddlr-docs" / "specs")
            self.assertEqual(paths["plans"], root / ".paddlr-docs" / "plans")
            self.assertEqual(paths["decisions"], root / ".paddlr-docs" / "decisions")
            self.assertEqual(paths["decisionsIndex"], root / ".paddlr-docs" / "DECISIONS.md")
            self.assertEqual(paths["project"], root / ".paddlr-docs" / "PROJECT.md")

    def test_partial_subpath_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / ".paddlr.json").write_text(
                json.dumps({"decisions": "docs/adr", "plans": ".local/plans"}),
                encoding="utf-8",
            )
            paths = resolve_memory_paths(root)
            self.assertEqual(paths["root"], root / "docs" / "paddlr")
            self.assertEqual(paths["specs"], root / "docs" / "paddlr" / "specs")
            self.assertEqual(paths["plans"], root / ".local" / "plans")
            self.assertEqual(paths["decisions"], root / "docs" / "adr")
            self.assertEqual(paths["decisionsIndex"], root / "docs" / "paddlr" / "DECISIONS.md")
            self.assertEqual(paths["project"], root / "docs" / "paddlr" / "PROJECT.md")

    def test_malformed_json_raises_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / ".paddlr.json").write_text("{not valid json", encoding="utf-8")
            with self.assertRaises(ValueError):
                resolve_memory_paths(root)

            (root / ".paddlr.json").write_text(json.dumps(["not-a-dict"]), encoding="utf-8")
            with self.assertRaises(ValueError):
                resolve_memory_paths(root)

            (root / ".paddlr.json").write_text(json.dumps({"plans": 123}), encoding="utf-8")
            with self.assertRaises(ValueError):
                resolve_memory_paths(root)

    def test_path_traversal_raises_value_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / ".paddlr.json").write_text(
                json.dumps({"plans": "../outside"}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                resolve_memory_paths(root)

            (root / ".paddlr.json").write_text(
                json.dumps({"plans": "/etc/plans"}),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                resolve_memory_paths(root)

    def test_autonomy_defaults_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            self.assertEqual(
                resolve_autonomy_config(root),
                {"pauseOnAmbiguity": False, "pauseBeforeCode": "never"},
            )
            (root / ".paddlr.json").write_text(json.dumps({"root": "docs/paddlr"}), encoding="utf-8")
            self.assertEqual(
                resolve_autonomy_config(root),
                {"pauseOnAmbiguity": False, "pauseBeforeCode": "never"},
            )

    def test_autonomy_partial_and_full_overrides(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / ".paddlr.json").write_text(
                json.dumps({"autonomy": {"pauseOnAmbiguity": True}}),
                encoding="utf-8",
            )
            self.assertEqual(
                resolve_autonomy_config(root),
                {"pauseOnAmbiguity": True, "pauseBeforeCode": "never"},
            )

            (root / ".paddlr.json").write_text(
                json.dumps({"autonomy": {"pauseOnAmbiguity": True, "pauseBeforeCode": "level3"}}),
                encoding="utf-8",
            )
            self.assertEqual(
                resolve_autonomy_config(root),
                {"pauseOnAmbiguity": True, "pauseBeforeCode": "level3"},
            )

            (root / ".paddlr.json").write_text(
                json.dumps({"autonomy": {"pauseBeforeCode": "always"}}),
                encoding="utf-8",
            )
            self.assertEqual(
                resolve_autonomy_config(root),
                {"pauseOnAmbiguity": False, "pauseBeforeCode": "always"},
            )

    def test_session_start_hook_injects_paddlr_json_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / ".paddlr.json").write_text(
                json.dumps({"root": ".custom-paddlr", "autonomy": {"pauseOnAmbiguity": True, "pauseBeforeCode": "level3"}}),
                encoding="utf-8",
            )
            proc = subprocess.run(
                [sys.executable, str(REPO_ROOT / "hooks" / "session-start.py")],
                input=json.dumps({"conversationId": "test-conv", "workspacePaths": [str(root)]}),
                text=True,
                capture_output=True,
                check=True,
            )
            output = json.loads(proc.stdout)
            msg = output["injectSteps"][0]["systemMessage"]["systemMessage"]
            self.assertIn(".custom-paddlr", msg)
            self.assertIn("pauseOnAmbiguity=true", msg)
            self.assertIn('pauseBeforeCode="level3"', msg)

    def test_autonomy_invalid_values_raise_value_error(self):
        invalid_payloads = [
            {"autonomy": "never"},
            {"autonomy": {"unknownKey": True}},
            {"autonomy": {"pauseOnAmbiguity": "true"}},
            {"autonomy": {"pauseOnAmbiguity": 1}},
            {"autonomy": {"pauseBeforeCode": "level2"}},
            {"autonomy": {"pauseBeforeCode": False}},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            for payload in invalid_payloads:
                (root / ".paddlr.json").write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(ValueError, msg=f"Expected ValueError for {payload}"):
                    resolve_autonomy_config(root)


if __name__ == "__main__":
    unittest.main()
