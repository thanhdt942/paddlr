---
name: principle-record-decisions-immutably
description: "Apply when making or changing a high-impact architectural decision (Level 3). Append a new ADR and supersede the prior record rather than overwriting history."
disable-model-invocation: true
---

# Record Decisions Immutably

Future engineers and AI agents inherit the codebase without the chat transcript that produced it. When an architectural choice changes, overwriting the old record erases why the previous design existed and invites the next contributor to repeat the same dead-end debate.

- **One decision, one file:** Store each Level 3 decision in `docs/paddlr/decisions/XXXX-<slug>.md` (or `.paddlr.json` override) and add a one-line row to `DECISIONS.md`.
- **Never rewrite accepted history:** When a direction changes, author a new ADR (`XXXX+1-<slug>.md`) explaining the new context and trade-offs, and mark the old ADR `Superseded by ADR-XXXX+1`.
- **Keep the index scannable:** `DECISIONS.md` stays a compact single-line-per-decision table so agents can scan architectural boundaries in one read and open individual ADRs only when relevant.
- **Cite before changing:** Before reversing a past architectural choice, inspect `decisions/` and `specs/` (via **why**) to confirm the original constraint no longer holds.
