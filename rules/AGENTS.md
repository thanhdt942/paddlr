# AGENTS.md — Paddlr Operating Rules

> **Framework:** Paddlr — Simple on the Surface. Sophisticated Underneath.
> **Entry points:** `/paddlr-mode` (execution), `/setup-paddlr` (repo onboarding), `/paddlr-help` (read-only advisor).

## 1. Reversibility-First Autonomy
- **Level 1 (Small fix / localized refactor):** No Spec or Plan. Execute directly and verify.
- **Level 2 (Standard feature, reversible on a feature branch/worktree):** Author Spec + Plan in project memory, implement in verifiable slices, commit on the feature branch, verify on the real surface, and open a ready-for-review PR without blocking.
- **Level 3 (Architectural, schema/public API breaking, or multi-PR, reversible on a branch/worktree):** Prototype unknowns if present, author Spec + ADR + Plan, and proceed on a reversible branch/worktree without blocking — present the complete diff, ADR, and verification evidence for review.
- **Configurable pauses (`.paddlr.json` `autonomy`):**
  - `pauseOnAmbiguity` (default `false`): when `false`, pick the safest convention-aligned default, record assumptions in Spec/Plan, and report them in the final summary/PR. When `true`, ask concise clarifying questions before coding if product/UX/acceptance criteria are ambiguous and cannot be settled by reading code or prototyping.
  - `pauseBeforeCode` (`"never"` | `"level3"` | `"always"`, default `"never"`): optionally require pre-code Spec/Plan approval for Level 3 or all Level 2–3 work.
- **Session overrides:** Directives such as "don't stop", "don't ask", or "write the plan and stop" override `.paddlr.json` autonomy settings for the current session; hard stops still apply.

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
