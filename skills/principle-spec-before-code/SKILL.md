---
name: principle-spec-before-code
description: "Apply before implementing any Level 2 or Level 3 feature or architectural change. Define problem, scope, requirements, and acceptance criteria before writing code."
disable-model-invocation: true
---

# Spec Before Code

Ambiguity discovered in code is ten times more expensive than ambiguity resolved in a one-page spec. For any Level 2 feature or Level 3 architectural change, state what the system must do, what is out of scope, and how completion will be verified before writing production code.

- **Level 1 is exempt:** Typos, localized bug fixes, and single-file mechanical edits skip specs and run directly.
- **Level 2 proceeds without blocking:** Write a concise spec in `docs/paddlr/specs/YYYY-MM-DD-<slug>.md` (or `.paddlr.json` override) and a contract-first plan, then implement and verify on a reversible branch.
- **Level 3 pauses for alignment:** High-impact, breaking, or multi-PR changes require human approval on the Spec + ADR + Plan before code changes begin.
- **Specs stay truthful:** If implementation uncovers a better shape, update the spec (via **sync-docs**) before opening the PR so code and spec never diverge.
