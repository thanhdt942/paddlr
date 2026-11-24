---
name: feature-development
description: Orchestrate end-to-end software feature development from requirement intake to verified completion. Coordinates existing engineering skills (writing-specs, writing-plans, test-driven-development, code-review, sre-debugging) without duplicating their internals. Use when the user asks to build a new feature, implement a user story, add new functionality, extend an existing module, or run a structured feature development workflow.
disable-model-invocation: true
---

# Feature Development

Coordinate the end-to-end lifecycle of building a software feature by sequencing discovery, scoping, implementation, verification, and handoff while delegating specialized work to existing engineering skills.

## Purpose and Scope

This skill acts as a lightweight workflow orchestrator. It defines the phases, decision gates, and completion standards for delivering a feature safely and predictably, while keeping detailed procedures in dedicated reference files and companion skills.

## When to Use and When Not to Use

Use this skill when:

- Building a new user-facing or internal feature from requirements or a user story.
- Extending an existing module with new behavior, endpoints, UI flows, or configuration.
- Coordinating multi-step changes that may require specs, plans, tests, debugging, or review.

Do not use this skill when:

- The task is purely an incident investigation or bug fix with no new feature work (use `sre-debugging` directly).
- The user only wants a standalone code review, spec, or architecture discussion without implementation.
- The change is a trivial one-line edit such as a typo fix or comment update.

## Workflow Overview

Execute feature development in six sequential phases. Read the designated reference file before acting in each phase.

1. **Intake and Codebase Discovery**
   - Clarify the goal, target behavior, constraints, and acceptance criteria.
   - Explore the relevant codebase area before proposing changes.
   - Read `references/implementation-guidelines.md` for discovery and convention rules.

2. **Workflow Triage**
   - Assess complexity, risk, and ambiguity to select which activities and companion skills are required.
   - Read `references/workflow-decisions.md` to decide whether to invoke `writing-specs`, `writing-plans`, `test-driven-development`, or `code-review`, or when a step can be skipped.

3. **Specification and Planning (Conditional)**
   - If the feature has multiple behaviors, edge cases, or unclear acceptance criteria, delegate to `writing-specs`.
   - If the change spans multiple components or requires ordered steps, delegate to `writing-plans`.
   - If the feature involves major architectural choices or technology trade-offs, formulate an ADR in `docs/paddlr/decisions/` and register it in `docs/paddlr/DECISIONS.md` (see `skills/writing-specs/references/adr-guide.md`).
   - Confirm major assumptions and architectural decisions with the user before writing production code.

4. **Implementation**
   - Follow `references/implementation-guidelines.md` to make small, focused, convention-aligned changes.
   - If automated testing fits the logic, delegate test-first execution to `test-driven-development`.
   - If unexpected failures or unclear root causes arise during implementation, delegate diagnosis to `sre-debugging` instead of guessing fixes.

5. **Verification and Review**
   - Run relevant test suites, type checks, linters, and builds to gather concrete evidence.
   - If the change has meaningful blast radius or complexity, delegate review to `code-review` and address findings.

6. **Completion Gate**
   - Verify all items in `references/completion-checklist.md`.
   - Report what was implemented, the exact verification evidence run, and any remaining limitations or follow-up items.

## Reusing Companion Skills

Delegate specialized work instead of re-inventing it inline:

- **`writing-specs`**: Clarify behavioral requirements, edge cases, and acceptance criteria.
- **`writing-plans`**: Break multi-component features into an ordered execution plan.
- **`test-driven-development`**: Drive deterministic logic implementation through red-green-refactor cycles.
- **`sre-debugging`**: Perform hypothesis-driven root cause analysis when tests or runtime behavior fail unexpectedly.
- **`code-review`**: Audit diffs for correctness, maintainability, security, and edge cases before finalizing.

## Decision Points and Escalation Criteria

Pause and consult the user whenever any of the following occur:

- Requirements or acceptance criteria have multiple plausible interpretations that affect external behavior.
- Codebase discovery reveals that the initial plan conflicts with existing architecture or constraints.
- Implementation requires a breaking API, schema, or contract change not mentioned in the request.
- Scope expands significantly beyond the original feature request.
- Verification cannot be completed (for example, missing test environment, credentials, or external services).

## Reference Reading Map

Load reference files only at the phase where they are needed:

- **Phase 2 (Triage) and any scope change**: Read `references/workflow-decisions.md`.
- **Phase 1 (Discovery) and Phase 4 (Implementation)**: Read `references/implementation-guidelines.md`.
- **Phase 6 (Completion Gate)**: Read `references/completion-checklist.md`.

## Completion Criteria

Do not declare a feature complete until every applicable gate in `references/completion-checklist.md` is satisfied with direct verification evidence. If any check could not be run or failed, state it explicitly rather than claiming success.

## Gotchas

- **Over-processing simple features**: Do not force full specs and multi-step plans for small, unambiguous changes. Use `references/workflow-decisions.md` to take the fast path when appropriate.
- **Opportunistic refactoring**: Avoid cleaning up unrelated legacy code inside a feature diff; log tech debt separately.
- **Unverified claims**: Never state that tests pass or a feature works without actually running the checks and observing the output.
- **Duplicating companion skills**: Keep TDD loops, spec templates, and debugging procedures inside their respective skills rather than rewriting them here.
