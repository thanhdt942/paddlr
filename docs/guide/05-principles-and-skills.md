# 5. Principles and Craft Skills

## 26 Lazy-Loaded Principles

Paddlr ships 26 `principle-*` skills grouped into Core, Architecture, Verification, Delegation, and Meta. Every principle sets `disable-model-invocation: true`, so only the one-line index in [skills/paddlr-mode/SKILL.md](../../skills/paddlr-mode/SKILL.md) loads by default. Agents read the full leaf skill only when its trigger applies.

The two SDD principles added in v1.2.0 encode Paddlr's spec and ADR discipline directly into the library:

- **Spec Before Code (`principle-spec-before-code`):** Define scope, requirements, and acceptance criteria before coding Level 2+ work (Level 1 exempt).
- **Record Decisions Immutably (`principle-record-decisions-immutably`):** Append new ADRs and supersede prior ones instead of rewriting accepted history.

## Craft and Review Skills

All specialized craft skills are lazy-loaded (`disable-model-invocation: true`) and agent-agnostic:

- **`no-comments`:** Runs the [comment-sicko.md](../../skills/no-comments/comment-sicko.md) audit (via `agent.delegate` or Single-Agent fallback) to delete narration/workaround comments, refactor root causes behind `MUST KILL` flags, and encode internal constraints in types/lints/tests.
- **`unslop`:** Strips AI writing tells and filler from prose, specs, docs, and PR descriptions using numbered rules.
- **`correct`:** Turns recurring agent mistakes into structural impossibility (architecture -> types/lint -> behavior tests -> docs last).
- **`architect`:** Shapes data models, state machines, and module boundaries before logic is written.
- **`interrogate`:** Adversarial red-teaming where findings survive only with an empirical reproduction command.
- **`why` / `how`:** Cited historical rationale (`decisions/`, `specs/`, git history) vs. live runtime behavior tracing.
- **`setup-paddlr`:** Auto-invocable repository onboarding (`docs/paddlr/` or `.paddlr.json`, optional model profiles, optional verification skill offer).
- **`paddlr-help`:** Lazy-loaded, strictly read-only advisor (`/paddlr-help`) that recommends the right skill, playbook, or principle with a doc link and copy-paste prompt without executing the task.

Next: [Customization with `.paddlr.json`](06-customization.md).
