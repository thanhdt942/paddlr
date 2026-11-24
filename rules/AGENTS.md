# AGENTS.md — Paddlr Operating Rules

> **Framework:** Paddlr — Simple on the Surface. Sophisticated Underneath.
> **Entry points:** `/paddlr-mode` (execution), `/setup-paddlr` (repo onboarding), `/paddlr-help` (read-only advisor).

## 1. Reversibility-First Autonomy
- **Level 1 (Small fix / localized refactor):** No Spec or Plan. Execute directly and verify.
- **Level 2 (Standard feature, reversible on a feature branch/worktree):** Author Spec + Plan in project memory, implement in verifiable slices, commit on the feature branch, verify on the real surface, and open a ready-for-review PR without blocking for pre-code approval (unless product/UX ambiguity remains or the user asks to review/hold commits first).
- **Level 3 (Architectural, schema/public API breaking, or multi-PR):** Prototype unknowns if present, author Spec + ADR + Plan, and **pause for explicit user approval** before modifying production code.
- **Session overrides:** Directives such as "don't stop" or "run until done" continue reversible branch work while recording decisions in Plan/ADR; hard stops still apply.

## 2. Hard Stops (Always Pause)
- Destructive Git on shared state (`git reset --hard`, `git clean -fd`, `git push --force` to shared branches, pushing directly to protected trunk branches without authorization).
- Production deploys, package publishing, deleting persistent data, or sending messages to external channels.
- Exposing secrets, tokens, or credentials in code, logs, or docs.

## 3. Evidence-Based Verification
- Never claim success without running real verification commands and reporting concrete status (`PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, `NOT APPLICABLE`) with captured output.
- Compilation or type checks alone do not prove behavioral correctness.

## 4. Project Memory & Prose
- Default root is `docs/paddlr/` (`specs/`, `plans/`, `decisions/`, `DECISIONS.md`, `PROJECT.md`); honor any custom overrides in `.paddlr.json` at the repo root.
- Always create a fresh plan file per Level 2/3 request; never overwrite past plans or rewrite accepted ADRs (supersede via `/adr`).
- Keep prose, docs, and PR descriptions concise, plain English, and aligned with Conventional Commits.
