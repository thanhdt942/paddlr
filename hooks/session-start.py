#!/usr/bin/env python3
"""
Paddlr — Session Start Lifecycle Hook.

Executes during session startup, resume, or context compaction (SessionStart event).
Injects the Paddlr engineering methodology bootstrap into the agent's context.

Supports both:
1. Google Antigravity (`agy`) SessionStart contract (when stdin contains `conversationId` or `--antigravity` is passed):
   {
     "injectSteps": [
       {
         "systemMessage": {
           "systemMessage": "..."
         }
       }
     ]
   }
2. Claude Code / Cursor / Gemini CLI SessionStart contract:
   {
     "hookSpecificOutput": {
       "hookEventName": "SessionStart",
       "additionalContext": "..."
     }
   }
"""

import json
import os
from pathlib import Path
import sys

claude_plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
if claude_plugin_root and Path(claude_plugin_root).is_dir():
    PLUGIN_ROOT = Path(claude_plugin_root).resolve()
else:
    PLUGIN_ROOT = Path(__file__).resolve().parent.parent

if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))

from scripts.paddlr_config import CONFIG_FILENAME, resolve_autonomy_config, resolve_memory_paths

BOOTSTRAP_CONTEXT = """=== Paddlr Engineering Discipline Active ===
You are operating with the Paddlr software engineering framework.
Tagline: Simple on the Surface. Sophisticated Underneath.
Philosophy: Handle the complexity. Simplify the experience.
Authority / Source of Truth: rules/AGENTS.md

Core Operating Principles:
1. UNDERSTAND BEFORE MODIFYING: Discover repository conventions, architecture, and dependencies.
2. CLARIFY OR RECORD ASSUMPTIONS: Honor .paddlr.json autonomy.pauseOnAmbiguity (ask on ambiguity when true; record assumptions in Spec/Plan and report them when false).
3. INCREMENTAL IMPLEMENTATION: Work in small, self-contained, verifiable slices (Red-Green-Refactor).
4. EVIDENCE-BASED VERIFICATION: Never report success without capturing concrete command output (PASS/FAIL).
5. PERSISTENT CONTEXT & PLANS: Maintain project context, ADRs (docs/paddlr/DECISIONS.md), feature specs (docs/paddlr/specs/), and plans (docs/paddlr/plans/) in docs/paddlr/ (or .paddlr.json overrides). Always create a new plan file for each Level 2/3 request. Never store plans solely in ephemeral IDE chat artifacts.

Available Skills:
- skills/feature-development: Orchestrate end-to-end feature delivery coordinating all companion skills
- skills/writing-specs: Clarify requirements and draft reviewable feature specifications in docs/paddlr/specs/
- skills/writing-plans: Decompose approved specifications into verifiable, contract-first implementation plans in docs/paddlr/plans/
- skills/writing-decisions: Record and supersede immutable ADRs in docs/paddlr/decisions/ and DECISIONS.md (/adr)
- skills/sync-docs: Pre-PR check verifying specs, ADRs, and PROJECT.md stay aligned with code diffs
- skills/test-driven-development: Implement code strictly test-first (RED -> GREEN -> REFACTOR)
- skills/sre-debugging: Systematic root cause analysis and scientific troubleshooting for bugs and failures
- skills/code-review: Independent, read-only code review before merging or completing tasks
- skills/release-management: Manage software release lifecycle and persist release conventions in RELEASE.md
- skills/skill-creator: Design, draft, verify, and package reusable AI agent skills
- skills/setup-paddlr: Initialize docs/paddlr/ or .paddlr.json and optional model profiles
- skills/paddlr-help: Read-only advisor routing questions to skills, playbooks, principles, and prompts (/paddlr-help)

{config_section}
CRITICAL: Before writing or modifying application code, check which Paddlr skill applies to your task.
==========================================================="""


def _read_stdin_payload() -> dict:
    if not sys.stdin.isatty():
        try:
            raw = sys.stdin.read().strip()
            if raw:
                data = json.loads(raw)
                if isinstance(data, dict):
                    return data
        except Exception:
            pass
    return {}


def _is_antigravity_invocation(stdin_data: dict) -> bool:
    if "--antigravity" in sys.argv[1:]:
        return True
    return "conversationId" in stdin_data or "workspacePaths" in stdin_data


def _resolve_workspace_root(stdin_data: dict) -> Path:
    workspace_paths = stdin_data.get("workspacePaths")
    if isinstance(workspace_paths, list) and workspace_paths and isinstance(workspace_paths[0], str):
        return Path(workspace_paths[0]).resolve()
    cwd = stdin_data.get("cwd")
    if isinstance(cwd, str) and cwd.strip():
        return Path(cwd).resolve()
    return Path.cwd().resolve()


def _build_config_section(workspace_root: Path) -> str:
    config_file = workspace_root / CONFIG_FILENAME
    source = str(config_file) if config_file.is_file() else "defaults (no .paddlr.json found)"
    try:
        paths = resolve_memory_paths(workspace_root)
        autonomy = resolve_autonomy_config(workspace_root)
        rel_root = paths["root"].relative_to(workspace_root)
        return (
            f"Active Configuration ({source}):\n"
            f"- Memory root: {rel_root.as_posix()}\n"
            f"- Autonomy: pauseOnAmbiguity={json.dumps(autonomy['pauseOnAmbiguity'])}, "
            f"pauseBeforeCode={json.dumps(autonomy['pauseBeforeCode'])}\n"
        )
    except ValueError as exc:
        return f"Active Configuration WARNING ({config_file}): {exc}\n"


def main():
    stdin_data = _read_stdin_payload()
    workspace_root = _resolve_workspace_root(stdin_data)
    context = BOOTSTRAP_CONTEXT.format(config_section=_build_config_section(workspace_root))

    if _is_antigravity_invocation(stdin_data):
        payload = {
            "injectSteps": [
                {
                    "systemMessage": {
                        "systemMessage": context,
                    }
                }
            ]
        }
    else:
        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context,
            }
        }
    print(json.dumps(payload, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
