# 4. Autonomy and Verification

## Reversibility-First Autonomy Policy

Paddlr pauses **only when an action cannot be rolled back** (or when you explicitly ask to review a plan first). Levels 1–3 determine the engineering artifacts you produce, not whether the agent blocks on reversible branch work:

| Tier | Scope | Spec, Plan & ADR | Approval Gate |
|---|---|---|---|
| **Level 1** | Typos, localized bugs, single-file refactors | Exempt (no Spec or Plan) | **Proceed without blocking**; review via diff. |
| **Level 2** | Standard features, reversible on a branch/worktree | Write Spec + Plan in project memory | **Proceed without blocking** through implementation, verification, and PR creation. |
| **Level 3** | Architectural changes, DB schemas, public API breaks, multi-PR (reversible on a branch/worktree) | Prototype unknowns, then Spec + ADR + Plan | **Proceed without blocking** on a reversible branch/worktree; review via PR + ADR (pause only if an action is irreversible or the user explicitly requests plan review first). |
| **Hard Stops** | Production deploys, package publishing, persistent data deletion, destructive Git/force-push on shared branches, external messages | N/A | **Always pause.** Never execute autonomously. |

Explicit session directives ("don't stop", "run until done", "don't ask", or "write the plan and stop") override `.paddlr.json` autonomy settings for the current session while still recording decisions in Spec/Plan/ADR; hard stops remain enforced.

### Configurable Autonomy in `.paddlr.json`

You can tune pause behavior per repository in `.paddlr.json` (defaults shown):

```json
{
  "autonomy": {
    "pauseOnAmbiguity": false,
    "pauseBeforeCode": "never"
  }
}
```

- **`pauseOnAmbiguity`** (default `false`): When `false`, Paddlr proceeds without asking, records assumptions in the Spec/Plan, and reports them in the final summary/PR. Set to `true` to ask concise clarifying questions before coding when product/UX/acceptance criteria are ambiguous and cannot be settled by reading code or prototyping.
- **`pauseBeforeCode`** (`"never"` | `"level3"` | `"always"`, default `"never"`): Choose whether to pause for pre-code Spec/Plan approval on Level 3 tasks or all Level 2–3 tasks. Hard Stops always pause regardless of this setting.

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
