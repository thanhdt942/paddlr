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
import sys

BOOTSTRAP_CONTEXT = """=== Paddlr Engineering Discipline Active ===
You are operating with the Paddlr software engineering framework.
Tagline: Simple on the Surface. Sophisticated Underneath.
Philosophy: Handle the complexity. Simplify the experience.
Authority / Source of Truth: rules/AGENTS.md

Core Operating Principles:
1. UNDERSTAND BEFORE MODIFYING: Discover repository conventions, architecture, and dependencies.
2. CLARIFY BEFORE ASSUMING: Disclose ambiguities in requirements early.
3. INCREMENTAL IMPLEMENTATION: Work in small, self-contained, verifiable slices (Red-Green-Refactor).
4. EVIDENCE-BASED VERIFICATION: Never report success without capturing concrete command output (PASS/FAIL).
5. PERSISTENT CONTEXT & PLANS: Maintain project context, ADRs (docs/paddlr/DECISIONS.md), feature specs (docs/paddlr/specs/), and plans (docs/paddlr/plans/) in docs/paddlr/. Always create a new plan file for each new request. Never store plans solely in ephemeral IDE chat artifacts.

Available Skills:
- skills/feature-development: Orchestrate end-to-end feature delivery coordinating all companion skills
- skills/writing-specs: Clarify requirements and draft reviewable feature specifications in docs/paddlr/specs/
- skills/writing-plans: Decompose approved specifications into verifiable, contract-first implementation plans in docs/paddlr/plans/
- skills/test-driven-development: Implement code strictly test-first (RED -> GREEN -> REFACTOR)
- skills/sre-debugging: Systematic root cause analysis and scientific troubleshooting for bugs and failures
- skills/code-review: Independent, read-only code review before merging or completing tasks
- skills/release-management: Manage software release lifecycle and persist release conventions in RELEASE.md
- skills/skill-creator: Design, draft, verify, and package reusable AI agent skills

CRITICAL: Before writing or modifying application code, check which Paddlr skill applies to your task.
==========================================================="""


def _is_antigravity_invocation() -> bool:
    if "--antigravity" in sys.argv[1:]:
        return True
    if not sys.stdin.isatty():
        try:
            raw = sys.stdin.read().strip()
            if raw:
                data = json.loads(raw)
                if isinstance(data, dict) and ("conversationId" in data or "workspacePaths" in data):
                    return True
        except Exception:
            pass
    return False


def main():
    if _is_antigravity_invocation():
        payload = {
            "injectSteps": [
                {
                    "systemMessage": {
                        "systemMessage": BOOTSTRAP_CONTEXT,
                    }
                }
            ]
        }
    else:
        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": BOOTSTRAP_CONTEXT,
            }
        }
    print(json.dumps(payload, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
