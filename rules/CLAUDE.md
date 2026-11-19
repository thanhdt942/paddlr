---
trigger: manual
---

# Claude Code Instruction Router

> **Framework:** Paddlr  
> **Source of Truth:** [AGENTS.md](AGENTS.md)  
> **Project Context:** [docs/paddlr/PROJECT.md](docs/paddlr/PROJECT.md)  

This repository uses the **Paddlr** engineering framework. Paddlr rules (imported into context):

@AGENTS.md

To prevent conflicting guidelines and maintain a single source of truth:
1. **Operating Principles & Guardrails:** Adhere strictly to [AGENTS.md](AGENTS.md).
2. **Engineering Workflow Cycle:** Execute tasks using the standard cycle: `Understand ──► Analyze & Plan ──► Incremental Implement ──► Evidence Verify ──► Finalize`.
3. **Git & Safety Rules:** Never run destructive git commands (`git reset --hard`, `git clean -fd`) or make unapproved commits.
4. **Skills Location:** Discover and execute skills located under `.claude/skills/` or `skills/`.
5. **Project Knowledge:** Check [docs/paddlr/DECISIONS.md](docs/paddlr/DECISIONS.md) (or [DECISIONS.md](DECISIONS.md)) before making architectural changes; update [docs/paddlr/PROGRESS.md](docs/paddlr/PROGRESS.md) (or [PROGRESS.md](PROGRESS.md)) when completing verifiable slices.
6. **Skills & Commands:** Use `/pdl:feature-development` to orchestrate end-to-end feature delivery, `/pdl:writing-specs` to draft specifications, `/pdl:writing-plans` to create implementation plans, `/pdl:test-driven-development` for test-driven execution, `/pdl:sre-debugging` for root-cause troubleshooting, `/pdl:code-review` for pre-merge review, `/pdl:release-management` for managing releases, and `/pdl:skill-creator` for authoring reusable agent skills.
