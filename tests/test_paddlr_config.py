#!/usr/bin/env python3
"""Tests for .paddlr.json project memory configuration and path resolution."""

import json
from pathlib import Path
import tempfile
import unittest

from scripts.paddlr_config import resolve_memory_paths


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


if __name__ == "__main__":
    unittest.main()
