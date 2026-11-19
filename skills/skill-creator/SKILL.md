---
name: skill-creator
description: Design, draft, verify, and package reusable AI agent skills following progressive disclosure and platform-agnostic standards. Use when creating a new skill from scratch, turning a repeated workflow or specification into a skill, or auditing and refactoring an existing skill. Do not use for one-off prompts, single-project rules better suited to project config files, or mechanical checks better handled by linters/scripts.
---

# Skill Creator

Platform-agnostic workflow for building concise, reliable, and portable AI agent skills.

## Core Principles

- **No-guidance control:** Only write instructions for behaviors the model does not reliably do on its own. Omit generic advice.
- **Progressive disclosure:** Keep `SKILL.md` focused on orchestration and core rules. Move long templates, checklists, or deep guides into `references/` and link them explicitly with *when* to read them.
- **Observable conditions over blanket prohibitions:** Prefer `"If X exists, do Y"` over `"Never do Z"`.
- **Self-contained & portable:** Keep all referenced files inside the skill directory. Avoid hardcoding a specific agent runtime, Git host, or tool unless the skill explicitly targets one.
- **Minimum sufficient process:** Match structure and testing rigor to the skill's risk and complexity.

## Workflow

### 1. Scope & Trigger Intake
Confirm before drafting (ask only what is missing):
- **Goal & Audience:** What task does the skill automate or standardize?
- **In Scope / Out of Scope:** Clear boundaries to prevent over-triggering.
- **Trigger Examples:** 3–5 concrete user prompts that *should* activate the skill and 2–3 near-miss prompts that *should not*.
- **Risk Level:** Standard (informational/formatting/workflow) vs. High-risk (mutating state, external actions, strict compliance).

### 2. Architecture Selection
Choose the lightest structure that fits:

| Complexity | Structure | Use When |
|---|---|---|
| **Simple** | `SKILL.md` only | Single focused workflow, short rules, no heavy templates. |
| **Standard** | `SKILL.md` + `references/` | Needs reusable templates, schemas, or deep domain guides. |
| **Tool-backed** | `SKILL.md` + `references/` + `scripts/` or `assets/` | Requires deterministic scripts, validation, or static assets. |

Read `references/skill-anatomy.md` for frontmatter conventions, description formulas, and the starter template.

### 3. Drafting
1. Write YAML frontmatter (`name` in `kebab-case` matching the folder name; `description` stating **what it does**, **when to use**, and **when not to use**).
2. Structure `SKILL.md` in order: **Core Rules → Workflow/Steps → Safety/Edge Cases → Output Format**.
3. Use tables or numbered steps instead of long prose paragraphs.
4. Link every file in `references/` from `SKILL.md` with an explicit trigger condition (e.g., *"Read `references/X.md` when doing Y"*). Leave no orphan files.

### 4. Verification
Adapt testing effort to the skill's risk level (read `references/testing-guide.md` for detailed protocols):
- **Trigger check:** Test positive and near-miss prompts against `description` wording.
- **Clean-context execution:** Run 1–2 realistic tasks in a fresh session and check output against acceptance criteria.
- **Pressure check (High-risk skills only):** Test under conflicting constraints (urgency, missing info, shortcut temptation). Capture any rationalizations, then tighten rules or add a Red Flags / Guardrails list.

### 5. Packaging & Delivery
Verify before finalizing:
- [ ] Folder name matches frontmatter `name`.
- [ ] `description` clearly defines triggers and exclusions.
- [ ] Every file in `references/` is linked from `SKILL.md`.
- [ ] No broken links or paths pointing outside the skill folder (`../`).
- [ ] No unnecessary boilerplate or rules the model already follows by default.
- [ ] Package cleanly as a directory or `.zip` archive (`<skill-name>/SKILL.md` at root).

## References

- `references/skill-anatomy.md` — Read during **Phase 2 & 3** for frontmatter rules, description patterns, and `SKILL.md` template.
- `references/testing-guide.md` — Read during **Phase 4** for trigger tests, clean-context verification, and pressure-testing high-risk skills.
