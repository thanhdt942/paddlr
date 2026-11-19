# Workflow Decisions

Use these rules during Phase 2 (Workflow Triage) and whenever scope or risk changes mid-feature to choose the right activities and companion skills.

## Quick Decision Matrix

| Situation | Decision | Rationale |
| --- | --- | --- |
| Requirement is small, single-behavior, and unambiguous | Skip `writing-specs` | Avoid overhead when acceptance criteria are already clear |
| Feature has multiple behaviors, edge cases, or unclear UX/API contracts | Use `writing-specs` | Align on behavior before investing in implementation |
| Change touches multiple components, layers, or data models | Use `writing-plans` | Prevent missed dependencies and ad-hoc edits |
| Logic is deterministic and testable with automated tests | Use `test-driven-development` | Catch regressions early and keep design modular |
| Unexpected test failure, regression, or unclear runtime error | Use `sre-debugging` | Verify root cause before changing code |
| Change has significant blast radius, complex logic, or sensitive impact | Use `code-review` | Catch subtle defects, security issues, and style drift |

## When to Invoke Each Companion Skill

### `writing-specs`

Invoke when:

- The request describes a high-level goal ("add export support") without concrete acceptance criteria.
- Multiple user flows, permission levels, error states, or edge cases must be defined.
- External contracts (REST/GraphQL APIs, CLI flags, UI states, data schemas) are being introduced or changed.

Skip when:

- The requirement is already fully specified with clear inputs, outputs, and edge cases.

### `writing-plans`

Invoke when:

- Implementation spans more than one component, service, or architectural layer (for example, DB migration + backend service + UI).
- Ordering matters due to dependencies, migrations, or feature flags.
- The user explicitly asks for an implementation plan before coding.

Skip when:

- The change is localized to one module or a few closely related files with an obvious sequence.

### `test-driven-development`

Invoke when:

- Implementing business logic, parsers, validators, state machines, API handlers, or utilities that can be verified via unit or integration tests.
- The repository already has a working test harness for the target layer.

Skip when:

- The change is purely declarative (static copy, styling tweaks, configuration files) where automated unit tests add little value. Still verify via build, lint, or manual check.

### `sre-debugging`

Invoke when:

- A test or build fails for reasons that are not immediately obvious from the diff.
- Existing behavior regresses unexpectedly.
- An environment, dependency, or runtime error blocks progress.

Do not guess and apply repeated trial-and-error edits; switch to `sre-debugging` to isolate the root cause first.

### `code-review`

Invoke when:

- The diff is non-trivial, touches shared abstractions, or modifies critical paths (auth, billing, data persistence, concurrency, security).
- Multiple files or components were modified.

Skip when:

- The change is tiny, isolated, low-risk, and fully covered by straightforward tests.

## When to Increase Process Rigor

Escalate from a lightweight path to the full workflow (spec + plan + TDD + code review) if any of the following emerge during discovery or implementation:

- **Architectural Decisions (ADR Gate)**: If the change introduces new frameworks, alters database schemas, redefines security boundaries, or forces a major architectural trade-off, formulate an ADR in `docs/paddlr/decisions/XXXX-<slug>.md` and register it in `docs/paddlr/DECISIONS.md` before implementation (see `skills/writing-specs/references/adr-guide.md`).
- **Breaking changes**: Public APIs, database schemas, or persisted formats must change.
- **High-risk domains**: Security, authentication, authorization, payments, privacy, or data integrity are affected.
- **Low safety net**: The target area has little or no existing test coverage.
- **Wide blast radius**: Shared libraries, core state management, or cross-cutting middleware are modified.
- **Repeated surprises**: Two or more unexpected blockers appear during implementation, signaling incomplete discovery.
