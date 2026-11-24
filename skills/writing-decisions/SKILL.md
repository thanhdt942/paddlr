---
name: writing-decisions
description: "Create or supersede immutable Architectural Decision Records (ADRs) in docs/paddlr/decisions/ (or .paddlr.json overrides) and maintain the DECISIONS.md index. Use for /adr or Level 3 architectural decisions."
disable-model-invocation: true
---

# Writing Decisions (ADRs)

Record high-impact architectural decisions as immutable, granular Markdown files so future engineers and AI agents understand why the system was shaped this way without reading sprawling logs.

Reference template and trigger criteria: [adr-guide.md](../writing-specs/references/adr-guide.md).

## 1. Resolve Target Paths

1. Check for an optional `.paddlr.json` at the repository root.
2. Resolve the decisions directory (`decisions`, default `docs/paddlr/decisions/`) and master index (`decisionsIndex`, default `docs/paddlr/DECISIONS.md`).
3. Never write outside the repository root.

## 2. When to Author an ADR

- **Write an ADR for (Level 3 / high-impact):** core technology or dependency choices, persistence or protocol boundaries, security/identity models, public API/SDK breaking changes, or repository-wide structural conventions.
- **Skip an ADR for:** routine bug fixes, localized refactors, styling changes, or feature-scoped trade-offs that belong inside a feature spec (`specs/YYYY-MM-DD-<slug>.md`).

## 3. Creating a New ADR

1. Inspect the existing `DECISIONS.md` index and `decisions/` directory to determine the next zero-padded sequence number (`0001`, `0002`, ...).
2. Create `decisions/XXXX-<kebab-case-slug>.md` using the structure from [adr-guide.md](../writing-specs/references/adr-guide.md):
   - Metadata header (`Date`, `Status`, `Deciders`, `Tags`)
   - `## 1. Context & Problem Statement`
   - `## 2. Considered Alternatives` (2–3 viable options with concrete trade-offs)
   - `## 3. Decision Outcome` (chosen option, decisive justification, positive & negative consequences)
   - `## 4. Links & References` (related spec, PR, or superseded ADR)
3. Add a single-line entry to `DECISIONS.md` (keep the index compact and scannable).
4. Set `Status` to `Proposed` until explicitly approved by the user, then update to `Accepted`.

## 4. Superseding an Existing ADR (Immutability Rule)

Accepted ADRs are **never rewritten or deleted** (**principle-record-decisions-immutably**):

1. Create a new ADR `XXXX+1-<new-slug>.md` explaining the changed context and new decision, linking `Supersedes: ADR-XXXX`.
2. In the prior ADR `XXXX-*.md`, update **only** its `Status` line to `Superseded by ADR-YYYY` (do not alter its historical rationale).
3. Update the prior row's `Status` in `DECISIONS.md` to `Superseded` and append the new row.

## 5. Verification

- Confirm the new ADR file exists, has a unique zero-padded ID, and links cleanly from `DECISIONS.md`.
- Run the repository's link/validation checks if configured.
