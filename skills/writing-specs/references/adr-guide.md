# Architectural Decision Records (ADR) Guide

Platform-agnostic protocol for recording high-impact technical choices without causing context bloat.

## 1. Core Principles

- **One Decision, One File:** Store detailed records individually in `docs/paddlr/decisions/XXXX-<slug>.md`.
- **Lightweight Master Index:** Maintain a compact, single-line-per-decision table in `docs/paddlr/DECISIONS.md` (< 100 lines). AI agents read the index first and load individual ADR files only when relevant to the active task.
- **Immutable History:** Accepted decisions are never rewritten or deleted. When a technical direction shifts, author a new ADR that explicitly supersedes the prior one (`Superseded by ADR-XXXX`).

---

## 2. When to Write an ADR

### Write an ADR For (Level 3 / High-Impact):
- **Core Technology Selection:** Introducing, replacing, or removing major frameworks, databases, or runtime dependencies.
- **Architectural & Persistence Boundaries:** Changing core data models, database engines, caching layers, or RPC/REST protocol paradigms.
- **Security & Identity Models:** Redesigning authentication, authorization, session management, or encryption schemes.
- **Public API & SDK Breaking Changes:** Restructuring core package boundaries, deprecating major interfaces, or altering public SDK contracts.
- **Structural Conventions:** Standardizing project-wide repository conventions (e.g., persistent memory paths, packaging layouts).

### Do NOT Write an ADR For:
- Routine bug fixes or localized refactoring.
- Ephemeral implementation details specific to a single feature (document these in `docs/paddlr/specs/YYYY-MM-DD-<feature>.md` instead).
- Styling, linting, formatting, or minor variable/function renames.

---

## 3. Directory Layout

```text
docs/paddlr/
├── DECISIONS.md              # Compact Master Index Table (< 100 lines)
└── decisions/                # Dedicated ADR files
    ├── 0001-local-storage-sqlite.md
    ├── 0002-standardize-docs-paddlr.md
    └── ...
```

---

## 4. Master Index Table (`docs/paddlr/DECISIONS.md`)

When an ADR is accepted, prepend or append a one-line entry to `docs/paddlr/DECISIONS.md`:

```markdown
# Architectural Decisions (ADRs)

| ID | Date | Status | Title | Scope / Tags | File |
|---|---|---|---|---|---|
| **ADR-0001** | 2026-11-19 | `Accepted` | Use SQLite for Local Caching | Storage, Cache | [0001-local-storage-sqlite.md](decisions/0001-local-storage-sqlite.md) |
| **ADR-0002** | 2026-11-19 | `Accepted` | Standardize Project Memory to docs/paddlr | Architecture, Governance | [0002-standardize-docs-paddlr.md](decisions/0002-standardize-docs-paddlr.md) |
```

### Status Vocabulary:
- `Proposed`: Under active discussion or user review; not yet authorized.
- `Accepted`: Approved by user; active architecture standard.
- `Superseded`: Replaced by a newer decision (link to the replacing ADR).
- `Deprecated`: Retired or removed without direct replacement.

---

## 5. Granular ADR File Template

Save as `docs/paddlr/decisions/XXXX-<kebab-case-title>.md`:

```markdown
# ADR-XXXX: <Short Imperative Title>

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded by ADR-YYYY | Deprecated
- **Deciders:** User & Agent Name
- **Tags:** <comma-separated tags: Architecture, Storage, Security, etc.>

## 1. Context & Problem Statement
What technical problem or architectural crossroads triggered this decision? What constraints (performance, backward-compatibility, operational simplicity) must be satisfied?

## 2. Considered Alternatives
Briefly list 2–3 viable options evaluated:
- **Option A (Chosen):** <Core approach, primary advantages>
- **Option B:** <Alternative approach, trade-offs, reasons for rejection>

## 3. Decision Outcome
Chosen option: **<Option A>**, because <primary decisive justification approved by the user>.

### Positive Consequences
- <Advantage 1: e.g., improved read throughput>
- <Advantage 2: e.g., zero external network dependencies>

### Negative Consequences & Trade-offs
- <Trade-off 1: e.g., requires custom backup routine>
- <Trade-off 2: e.g., slightly higher local disk consumption>

## 4. Links & References
- Feature Spec: `docs/paddlr/specs/YYYY-MM-DD-<feature>.md` (if originated from a spec)
- Supersedes: `docs/paddlr/decisions/XXXX-<prior>.md` (if applicable)
```
