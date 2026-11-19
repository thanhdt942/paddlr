# Implementation Guidelines

Follow these rules during Phase 1 (Discovery) and Phase 4 (Implementation). This guide governs how feature work is coordinated in the codebase. It does not redefine TDD or debugging workflows; delegate those to `test-driven-development` and `sre-debugging`.

## 1. Explore the Codebase Before Changing Anything

Before editing files:

- Locate the entrypoints, data flow, and existing tests for the target area.
- Identify related modules that already solve similar problems so you can reuse existing utilities and patterns.
- Check project configuration (lint rules, typecheck commands, test runners, build scripts) so you know how to verify changes.

## 2. Respect Existing Architecture and Conventions

- Match the repository's existing folder structure, naming conventions, error-handling style, and abstraction boundaries.
- Prefer existing internal helpers and approved dependencies over introducing new patterns or third-party packages.
- If an existing convention feels suboptimal, still follow it for the feature unless the user asks for a broader architectural change.

## 3. Prefer Small, Focused Changes

- Keep each edit cohesive and directly tied to an acceptance criterion.
- Implement and verify one vertical slice or logical unit at a time rather than editing dozens of files before running any check.
- Avoid mixing formatting sweeps or unrelated cleanups with functional changes so the diff stays easy to review and revert.

## 4. Maintain Strict Scope Discipline

- Do not refactor unrelated code outside the feature scope.
- If you discover pre-existing bugs, technical debt, or cleanup opportunities in nearby code, note them in your final report instead of silently fixing them inside the feature diff.
- Only touch adjacent code when strictly required to integrate the new feature cleanly.

## 5. Manage Dependencies and Cross-Component Impact

- Trace callers, consumers, type definitions, and serialization boundaries affected by your changes.
- Verify backward compatibility for shared interfaces, database schemas, and configuration files.
- If a new external dependency is genuinely required, justify why existing tools cannot solve the problem and confirm before adding it if the impact is significant.

## 6. Handle Deviations from the Initial Plan

Implementation often reveals constraints that were invisible during planning. When reality diverges from the plan:

1. Stop making further speculative edits.
2. Assess whether the deviation is minor (internal implementation detail, same external behavior and scope) or major (changes behavior, architecture, timeline, or risk).
3. For minor deviations: adjust locally, document the reason, and proceed.
4. For major deviations: update the plan and confirm the new direction with the user before continuing.

## 7. When to Stop and Ask the User

Do not silently guess when a decision carries product or architectural risk. Pause and ask the user if:

- Acceptance criteria are ambiguous and different choices produce noticeably different user or API behavior.
- Two requirements or existing system constraints contradict each other.
- Fulfilling the feature requires a breaking change, destructive migration, or new paid/external service.
- You encounter a blocker that requires credentials, access, or domain decisions outside the codebase.
