# Paddlr User Guide

Paddlr is an agent-agnostic software engineering framework for Google Antigravity, Claude Code, Cursor, OpenAI Codex, and OpenCode. It combines Spec-Driven Design (SDD) and persistent project memory with reversibility-first execution discipline.

## Chapters

1. [Setup and installation](01-setup.md) — Install Paddlr across supported AI coding agents and verify the setup.
2. [Paddlr Mode and playbooks](02-paddlr-mode.md) — Use `paddlr-mode`, choose the right playbook, and understand Playbook vs. Standalone Skill boundaries.
3. [Specs, plans, and ADRs](03-specs-plans-adrs.md) — Persist durable specifications, contract-first plans, immutable ADRs (`/adr`), and prevent drift with `sync-docs` and `why`.
4. [Autonomy and verification](04-autonomy-and-verification.md) — Understand the Reversibility-First Autonomy Policy (Level 1–3, hard stops), two-tier `ui.todo` checklist sync, and evidence-based verification.
5. [Principles and craft skills](05-principles-and-skills.md) — How the 26 lazy-loaded engineering principles and craft skills (`no-comments`, `unslop`, `correct`, `interrogate`, `architect`) work.
6. [Customization with `.paddlr.json`](06-customization.md) — Override project memory paths without colliding with existing repository docs.

## Reference Contracts

- Core rules shipped to repositories: [rules/AGENTS.md](../../rules/AGENTS.md)
- Orchestration mode: [skills/paddlr-mode/SKILL.md](../../skills/paddlr-mode/SKILL.md)
- Runtime Adapter Contract: [runtime-adapters.md](../../skills/paddlr-mode/references/runtime-adapters.md)
- Task State Schema: [task-state-schema.md](../../skills/paddlr-mode/references/task-state-schema.md)
