# 4. Autonomy and Verification

## Reversibility-First Autonomy Policy

Paddlr matches approval gates to reversibility rather than blocking on routine branch work:

| Tier | Scope | Spec & Plan | Approval Gate |
|---|---|---|---|
| **Level 1** | Typos, localized bugs, single-file refactors | Exempt (no Spec or Plan) | Execute directly; review via diff. |
| **Level 2** | Standard features, reversible on a branch/worktree | Write Spec + Plan in project memory | **Proceed without blocking** through implementation, verification, and PR creation. Pause only on unresolved product/UX ambiguity or explicit user request. |
| **Level 3** | Architectural changes, DB schemas, public API breaks, multi-PR | Prototype unknowns, then Spec + ADR + Plan | **Mandatory pause** for explicit human approval before modifying code. |
| **Hard Stops** | Production deploys, persistent data deletion, force-push to shared branches, external messages | N/A | **Always pause.** Never execute autonomously. |

Explicit session directives ("don't stop", "run until done") keep reversible branch work moving while still recording decisions in Plan/ADR; hard stops remain enforced.

## Two-Tier Checklist Synchronization (`ui.todo`)

- **Canonical source of truth:** `docs/paddlr/plans/YYYY-MM-DD-<slug>.md` (durable across sessions).
- **Live session mirror:** The optional `ui.todo` primitive in [runtime-adapters.md](../../skills/paddlr-mode/references/runtime-adapters.md) maps active steps to each host's native todo tool:
  - Cursor / Claude Code: `TodoWrite`
  - Antigravity: `update_steps`
  - OpenAI Codex CLI: `update_plan`
  - OpenCode: `todowrite`
  - Fallback: compact progress list in chat replies at phase boundaries
- **Sync invariant:** Mark `- [x]` in the plan file and `done` in `ui.todo` only after real verification passes.

## Evidence-Based Verification

Every verification claim carries an explicit status (`PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, `NOT APPLICABLE`) backed by verbatim terminal output. Compilation alone or agent self-reports never satisfy `principle-prove-it-works`.

Next: [Principles and craft skills](05-principles-and-skills.md).
