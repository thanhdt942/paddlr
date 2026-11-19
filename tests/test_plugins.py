#!/usr/bin/env python3
"""
Paddlr — Plugin Validation Test Suite (Claude Code, Antigravity, OpenCode, Codex).

Validates that Paddlr adheres to:
1. Claude Code plugin specification (.claude-plugin/plugin.json, hooks/hooks.json).
2. Google Antigravity plugin specification (plugin.json, hooks.json).
3. OpenCode plugin standard (package.json, index.js, .opencode/).
4. OpenAI Codex plugin and marketplace specification (.codex-plugin/plugin.json, .agents/plugins/marketplace.json).
5. Official CLI tools (claude, agy, opencode, codex) validate and register the plugin.
"""

import json
from pathlib import Path
import re
import shutil
import subprocess
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestPlugins(unittest.TestCase):
    """Test suite for Claude Code and Antigravity plugin conformance."""

    def test_01_claude_plugin_manifest_structure(self):
        """Validate .claude-plugin/plugin.json has required fields."""
        manifest_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
        self.assertTrue(manifest_path.is_file(), "Missing .claude-plugin/plugin.json")
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("name"), "paddlr")
        self.assertIn("version", data)
        self.assertIn("description", data)
        self.assertIn("author", data)
        self.assertEqual(data.get("hooks"), "./hooks/hooks.json")

    def test_02_claude_hooks_manifest(self):
        """Validate hooks/hooks.json defines SessionStart hook."""
        hooks_path = REPO_ROOT / "hooks" / "hooks.json"
        self.assertTrue(hooks_path.is_file(), "Missing hooks/hooks.json")
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
        self.assertIn("hooks", data)
        self.assertIn("SessionStart", data["hooks"])

    def test_03_rules_exist(self):
        """Validate rules/AGENTS.md and rules/CLAUDE.md exist."""
        for rule_file in ["AGENTS.md", "CLAUDE.md"]:
            path = REPO_ROOT / "rules" / rule_file
            self.assertTrue(path.is_file(), f"Missing rules/{rule_file}")

    def test_04_claude_plugin_validate_cli(self):
        """Run official claude plugin validate CLI if claude is installed."""
        claude_bin = shutil.which("claude") or shutil.which("claude.cmd") or shutil.which("claude.exe")
        if not claude_bin:
            self.skipTest("claude CLI tool not found in PATH")

        res = subprocess.run(
            [claude_bin, "plugin", "validate", "."],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            res.returncode,
            0,
            f"claude plugin validate returned code {res.returncode}: {res.stderr or res.stdout}",
        )
        self.assertIn("Validation passed", res.stdout)

    def test_05_antigravity_plugin_manifest(self):
        """Validate root plugin.json and hooks.json for Antigravity."""
        manifest_path = REPO_ROOT / "plugin.json"
        self.assertTrue(manifest_path.is_file(), "Missing root plugin.json")
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("name"), "paddlr")
        self.assertEqual(data.get("displayName"), "Paddlr")
        self.assertIn("version", data)
        self.assertEqual(data.get("logo"), "assets/logo.svg")
        self.assertIsInstance(data.get("suggestedPrompts"), list)
        self.assertEqual(len(data.get("suggestedPrompts")), 3)

        hooks_path = REPO_ROOT / "hooks.json"
        self.assertTrue(hooks_path.is_file(), "Missing root hooks.json")
        hooks_data = json.loads(hooks_path.read_text(encoding="utf-8"))
        self.assertIn("paddlr-session-start", hooks_data)
        self.assertIn("SessionStart", hooks_data["paddlr-session-start"])

    def test_06_antigravity_plugin_validate_cli(self):
        """Run official agy plugin validate CLI if agy is installed."""
        agy_bin = shutil.which("agy") or shutil.which("agy.cmd") or shutil.which("agy.exe")
        if not agy_bin:
            self.skipTest("agy CLI tool not found in PATH")

        res = subprocess.run(
            [agy_bin, "plugin", "validate", ".", "--json"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            res.returncode,
            0,
            f"agy plugin validate returned code {res.returncode}: {res.stderr or res.stdout}",
        )
        val_data = json.loads(res.stdout)
        self.assertEqual(val_data.get("name"), "paddlr")
        errors = [f for f in val_data.get("findings", []) if f.get("severity") == "error"]
        self.assertEqual(len(errors), 0, f"agy plugin validate found errors: {errors}")

    def test_07_opencode_package_manifest(self):
        """Validate package.json conforming to OpenCode and NPM standard."""
        pkg_path = REPO_ROOT / "package.json"
        self.assertTrue(pkg_path.is_file(), "Missing root package.json")
        data = json.loads(pkg_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("name"), "paddlr")
        self.assertEqual(data.get("type"), "module")
        self.assertEqual(data.get("main"), "index.js")
        self.assertEqual(data.get("types"), "index.d.ts")
        self.assertEqual(data.get("license"), "Apache-2.0")

        # Ensure version matches root plugin.json
        plugin_path = REPO_ROOT / "plugin.json"
        if plugin_path.is_file():
            plugin_data = json.loads(plugin_path.read_text(encoding="utf-8"))
            self.assertEqual(data.get("version"), plugin_data.get("version"))

    def test_08_opencode_plugin_files_structure(self):
        """Validate OpenCode plugin files and documentation exist."""
        for path in [
            REPO_ROOT / "index.js",
            REPO_ROOT / "index.d.ts",
            REPO_ROOT / ".opencode" / "INSTALL.md",
            REPO_ROOT / ".opencode" / "plugins" / "paddlr.js",
            REPO_ROOT / ".opencode" / "plugins" / "hsiw.js",
        ]:
            self.assertTrue(path.is_file(), f"Missing OpenCode plugin file: {path}")

    def test_09_opencode_plugin_runtime_execution(self):
        """Validate OpenCode plugin loads and executes under Node.js runtime."""
        node_bin = shutil.which("node") or shutil.which("node.exe")
        if not node_bin:
            self.skipTest("node binary not found in PATH")

        script = """
        import('./index.js').then(async (m) => {
            const plugin = m.default;
            if (!plugin || plugin.id !== 'paddlr') {
                console.error('Invalid plugin definition');
                process.exit(1);
            }
            const res = await plugin.setup();
            if (!res.tool || !res.tool.pdl_bootstrap || !res.tool.pdl_status || !res.tool.pdl_scan) {
                console.error('Missing expected tools');
                process.exit(2);
            }
            const boot = await res.tool.pdl_bootstrap.execute();
            if (!boot || !boot.includes('Paddlr')) {
                console.error('Invalid bootstrap output');
                process.exit(3);
            }
            process.exit(0);
        }).catch((err) => {
            console.error(err);
            process.exit(4);
        });
        """
        res = subprocess.run(
            [node_bin, "--input-type=module", "-e", script],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            res.returncode,
            0,
            f"OpenCode plugin runtime verification failed: {res.stderr or res.stdout}",
        )

    def test_10_opencode_cli_support(self):
        """Validate opencode CLI is functional if installed."""
        opencode_bin = shutil.which("opencode") or shutil.which("opencode.cmd") or shutil.which("opencode.exe")
        if not opencode_bin:
            self.skipTest("opencode CLI tool not found in PATH")

        res = subprocess.run(
            [opencode_bin, "--version"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(res.returncode, 0, f"opencode --version failed: {res.stderr}")
        self.assertTrue(bool(re.search(r"\d+\.\d+", res.stdout) or "opencode" in res.stdout.lower()))

    def test_11_codex_plugin_manifest_structure(self):
        """Validate .codex-plugin/plugin.json has required fields and matching version."""
        manifest_path = REPO_ROOT / ".codex-plugin" / "plugin.json"
        self.assertTrue(manifest_path.is_file(), "Missing .codex-plugin/plugin.json")
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("name"), "paddlr")
        self.assertIn("version", data)
        self.assertEqual(data.get("skills"), "./skills")
        self.assertEqual(data.get("license"), "Apache-2.0")

        # Ensure version matches root plugin.json
        plugin_path = REPO_ROOT / "plugin.json"
        if plugin_path.is_file():
            plugin_data = json.loads(plugin_path.read_text(encoding="utf-8"))
            self.assertEqual(data.get("version"), plugin_data.get("version"))

        # Interface validation
        interface = data.get("interface", {})
        self.assertEqual(interface.get("displayName"), "Paddlr")
        self.assertIn("category", interface)
        self.assertIsInstance(interface.get("capabilities"), list)

    def test_12_codex_marketplace_manifest_structure(self):
        """Validate .agents/plugins/marketplace.json catalog schema and plugin source."""
        mp_path = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
        self.assertTrue(mp_path.is_file(), "Missing .agents/plugins/marketplace.json")
        data = json.loads(mp_path.read_text(encoding="utf-8"))
        self.assertEqual(data.get("name"), "paddlr")
        self.assertIn("plugins", data)
        self.assertIsInstance(data["plugins"], list)
        self.assertGreater(len(data["plugins"]), 0)

        entry = next((p for p in data["plugins"] if p.get("name") == "paddlr"), None)
        self.assertIsNotNone(entry, "Missing paddlr entry in marketplace.json")
        self.assertEqual(entry.get("source", {}).get("source"), "local")
        self.assertEqual(entry.get("source", {}).get("path"), "./")
        self.assertEqual(entry.get("policy", {}).get("installation"), "AVAILABLE")

    def test_13_codex_cli_marketplace_integration(self):
        """Validate codex CLI adds marketplace and lists paddlr as available plugin."""
        codex_bin = shutil.which("codex") or shutil.which("codex.cmd") or shutil.which("codex.exe")
        if not codex_bin:
            self.skipTest("codex CLI tool not found in PATH")

        try:
            # 1. Add repository as marketplace
            add_res = subprocess.run(
                [codex_bin, "plugin", "marketplace", "add", str(REPO_ROOT), "--json"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                add_res.returncode,
                0,
                f"codex plugin marketplace add failed: {add_res.stderr or add_res.stdout}",
            )

            # 2. Query available plugins from this marketplace
            list_res = subprocess.run(
                [
                    codex_bin,
                    "plugin",
                    "list",
                    "--marketplace",
                    "paddlr",
                    "--available",
                    "--json",
                ],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(
                list_res.returncode,
                0,
                f"codex plugin list failed: {list_res.stderr or list_res.stdout}",
            )
            list_data = json.loads(list_res.stdout)
            available = list_data.get("available", [])
            plugin_entry = next((p for p in available if p.get("name") == "paddlr"), None)
            self.assertIsNotNone(
                plugin_entry,
                f"paddlr not discovered in codex marketplace. Output: {list_res.stdout}",
            )
            self.assertEqual(plugin_entry.get("marketplaceName"), "paddlr")
        finally:
            # 3. Clean up marketplace
            subprocess.run(
                [codex_bin, "plugin", "marketplace", "remove", "paddlr"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )


if __name__ == "__main__":
    unittest.main()
