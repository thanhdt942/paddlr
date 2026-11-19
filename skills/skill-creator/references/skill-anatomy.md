# Skill Anatomy & Authoring Guide

## 1. Directory Layout

```text
<skill-name>/
├── SKILL.md                  # Required: frontmatter + core workflow
├── references/               # Optional: detailed guides, templates, rubrics
├── scripts/                  # Optional: deterministic helper scripts
└── assets/                   # Optional: static files, schemas, examples
```

Keep all paths relative to the skill root (`references/file.md`). Never point outside the skill folder (`../other-skill/...`).

## 2. YAML Frontmatter

```yaml
---
name: <kebab-case-name>
description: <What the skill does>. Use when <trigger contexts/keywords>. Do not use for <exclusions>.
---
```

**Description Rules:**
- Lead with concrete capability, not vague marketing language.
- Include realistic trigger phrases users actually type.
- Add explicit exclusions if the skill overlaps with adjacent tasks.
- Avoid summarizing internal steps in `description`; keep it focused on routing/discovery.

## 3. Writing Rules for High Compliance

| Pattern | Weak (Avoid) | Strong (Prefer) |
|---|---|---|
| **Conditions** | "Always check config carefully." | "Before planning, read `RELEASE.md`. If missing, run First-Time Setup." |
| **Guardrails** | "Never make mistakes on prod." | "Require explicit user authorization before running `publish`, `deploy`, or `push --tags`." |
| **Formatting** | 3 paragraphs explaining 4 states. | Compact Markdown table mapping State → Behavior. |
| **References** | Mentioning a file without context. | "Read `references/testing-guide.md` before running Phase 4." |

## 4. Minimal `SKILL.md` Starter Template

```markdown
---
name: <skill-name>
description: <Core capability>. Use when <trigger scenarios>. Do not use for <exclusions>.
---

# <Skill Title>

One-line summary of what this skill accomplishes.

## Core Rules

- **Rule 1:** Observable condition → required action.
- **Rule 2:** Boundary or safety constraint.

## Workflow

1. **Step 1 — Intake:** Gather required inputs; ask only what is missing.
2. **Step 2 — Execute:** Perform core transformation or action.
3. **Step 3 — Verify:** Validate output against concrete criteria.
4. **Step 4 — Report:** Deliver structured output with evidence.

## Safety & Edge Cases

- **Low-risk (proceed):** Read-only inspection, drafting.
- **High-risk (ask first):** Mutating files, external side effects, destructive actions.
```
