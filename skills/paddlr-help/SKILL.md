---
name: paddlr-help
description: "Read-only advisor for Paddlr: routes questions to the right skill, playbook, principle, or docs/guide/ chapter and returns a ready-to-copy prompt without executing the task. Use for /paddlr-help."
disable-model-invocation: true
---

# Paddlr Help

Read-only advisor for navigating Paddlr. Answer the user's question concisely and hand them a ready-to-copy prompt.

## Non-Negotiable Rule: Read-Only Advisory

- **Do not execute the user's task.** Never edit repository code, run feature/bug playbooks, or spawn implementation workers during `/paddlr-help`. The user asked for guidance, and starting a full workflow spends unnecessary tokens.
- Read only the relevant Paddlr skill, playbook, or `docs/guide/` file needed to verify your recommendation before replying.

## How to Route a Question

Match the user's question against Paddlr's catalog below (check [paddlr-mode/SKILL.md](../paddlr-mode/SKILL.md) for the full 22-playbook and 26-principle index, and [docs/guide/README.md](../../docs/guide/README.md) for handbook chapters):

### Quick Routing Map

| User Goal / Question | Best Match | Reference |
|---|---|---|
| Initialize `docs/paddlr/`, `.paddlr.json`, or model profiles | `/setup-paddlr` | [setup-paddlr/SKILL.md](../setup-paddlr/SKILL.md) & [01-setup.md](../../docs/guide/01-setup.md) |
| Run any non-trivial engineering task end-to-end with rigor | `/paddlr-mode` | [paddlr-mode/SKILL.md](../paddlr-mode/SKILL.md) & [02-paddlr-mode.md](../../docs/guide/02-paddlr-mode.md) |
| Build a feature (Level 2/3) with Spec -> Plan -> TDD -> PR | `playbooks/feature.md` + `feature-development` | [feature.md](../paddlr-mode/playbooks/feature.md) & [feature-development/SKILL.md](../feature-development/SKILL.md) |
| Write a feature spec before coding | `writing-specs` | [writing-specs/SKILL.md](../writing-specs/SKILL.md) & [03-specs-plans-adrs.md](../../docs/guide/03-specs-plans-adrs.md) |
| Break a spec into bite-sized contract-first tasks | `writing-plans` | [writing-plans/SKILL.md](../writing-plans/SKILL.md) |
| Record or supersede an immutable ADR | `writing-decisions` (`/adr`) | [writing-decisions/SKILL.md](../writing-decisions/SKILL.md) & [03-specs-plans-adrs.md](../../docs/guide/03-specs-plans-adrs.md) |
| Check whether code drifted from specs, ADRs, or `PROJECT.md` | `sync-docs` | [sync-docs/SKILL.md](../sync-docs/SKILL.md) |
| Diagnose and fix a bug scientifically with a failing repro test | `playbooks/bug-fix.md` + `sre-debugging` | [bug-fix.md](../paddlr-mode/playbooks/bug-fix.md) & [sre-debugging/SKILL.md](../sre-debugging/SKILL.md) |
| Implement code test-first (RED -> GREEN -> REFACTOR) | `test-driven-development` | [test-driven-development/SKILL.md](../test-driven-development/SKILL.md) |
| Model types, state machines, or module boundaries first | `architect` | [architect/SKILL.md](../architect/SKILL.md) |
| Review a PR for spec alignment and maintainability | `code-review` | [code-review/SKILL.md](../code-review/SKILL.md) |
| Adversarially red-team a risky diff (proven repros only) | `interrogate` | [interrogate/SKILL.md](../interrogate/SKILL.md) |
| Strip unnecessary comments and fix hidden workarounds | `no-comments` | [no-comments/SKILL.md](../no-comments/SKILL.md) |
| Remove AI writing tells from docs, specs, or PR text | `unslop` | [unslop/SKILL.md](../unslop/SKILL.md) |
| Stop agents from repeating the same repo mistake | `correct` | [correct/SKILL.md](../correct/SKILL.md) |
| Ask why a design/decision exists (`decisions/`, `specs/`, git) | `why` | [why/SKILL.md](../why/SKILL.md) |
| Trace how code behaves at runtime | `how` | [how/SKILL.md](../how/SKILL.md) |
| Understand autonomy levels (Level 1–3, hard stops) & `ui.todo` | Autonomy & Verification guide | [04-autonomy-and-verification.md](../../docs/guide/04-autonomy-and-verification.md) |
| Browse the 26 engineering principles | Principles & Craft Skills guide | [05-principles-and-skills.md](../../docs/guide/05-principles-and-skills.md) |
| Customize paths with `.paddlr.json` | Customization guide | [06-customization.md](../../docs/guide/06-customization.md) |
| Build a project-local verification skill or manage releases | `create-verification-skill` / `release-management` | [create-verification-skill/SKILL.md](../create-verification-skill/SKILL.md) & [release-management/SKILL.md](../release-management/SKILL.md) |

If the user's question is ambiguous, ask one short clarifying question (at most 3–4 choices) before recommending.

## Required Reply Format (Always 3 Parts)

Keep every reply short, direct, and structured into exactly three parts:

1. **Best Match & Why:** Name the single best skill, playbook, or principle (from the 26 principles) and explain in 1–2 sentences why it fits.
2. **Reference Link:** Provide the direct link to the matching `SKILL.md`, playbook, or `docs/guide/` chapter.
3. **Copy-Paste Prompt:** Provide one ready-to-send prompt in a fenced code block so the user can start the work themselves when ready.
