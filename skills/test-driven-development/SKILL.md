---
name: test-driven-development
description: Use when implementing any feature, bugfix, or behavior change — before writing production code
disable-model-invocation: true
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write the minimal code to make it pass. Refactor.

**Announce at start:** "I'm using the test-driven-development skill to implement this."

**Reference:** Load and follow `writing-good-tests.md` whenever writing or modifying tests, adding test doubles, or creating test helpers.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.
```

If you wrote production code before the test, delete the production code and start over from the failing test. Do not keep it as "reference" or "just adapt it."

**Exceptions (require explicit confirmation from your human partner):**
- Throwaway spikes / prototypes (must be deleted before real implementation)
- Pure configuration, static assets, or generated code
- Trivial wiring with zero logic (e.g., re-exporting symbols)

---

## The Red – Green – Refactor Cycle

Work in tight, single-behavior iterations. Complete one full cycle before starting the next.

### 1. RED — Write One Failing Test

- Pick **one** concrete behavior from the spec or plan (e.g., one happy path, one boundary case, or one error condition).
- Write a single test following `writing-good-tests.md`:
  - Target the **public API**, not internal implementation.
  - Name the test after the **behavior**, not the method.
  - Use **hand-derived literal expectations** (no logic in tests).
  - Follow **Arrange – Act – Assert**.

### 2. VERIFY RED — Watch It Fail for the Right Reason

**Mandatory.** Run the test command and inspect the output.

- Confirm the test **fails**.
- Confirm it fails for the **expected reason** (missing function, wrong return value, unthrown error) — **not** a syntax error, typo, or broken import.
- If the test passes immediately, you are testing existing behavior or a tautology. Fix the test before continuing.

### 3. GREEN — Write Minimal Production Code

- Write the **simplest, smallest** production code needed to make the failing test pass.
- Do **not** add features, flags, error handling, or abstractions not required by the current failing test (YAGNI).
- Do **not** modify the test to make it pass unless the test itself had a genuine spec mistake.

### 4. VERIFY GREEN — Watch All Tests Pass

**Mandatory.** Run the new test **and** the relevant existing test suite.

- Confirm the new test passes.
- Confirm all existing tests still pass (zero regressions).
- Confirm output is clean (no unexpected warnings or errors).

### 5. REFACTOR — Clean Up Without Changing Behavior

Only after GREEN:
- Remove duplication in production code, improve naming, extract focused helpers.
- Clean up test readability if needed (keep tests DAMP, not over-abstracted).
- **Do not** add new behavior during refactor.
- Re-run tests after every refactor step to confirm everything stays GREEN.

### 6. COMMIT

Commit small, working increments once a task or logical behavior is green and clean.

---

## Bugfix Workflow

When fixing a bug, never jump straight to patching the code:

1. Write a failing test that **reproduces the exact bug**.
2. Run it and confirm it fails with the bug's symptom (**VERIFY RED**).
3. Fix the root cause in production code (**GREEN**).
4. Run the full suite to confirm the bug is fixed and nothing else broke (**VERIFY GREEN**).
5. Commit the regression test together with the fix.

---

## Verification Checklist

Before declaring any task complete, verify every item:

- [ ] Every new behavior or bugfix has a corresponding test written **before** the implementation
- [ ] Every new test was observed **failing** for the expected reason before implementation
- [ ] Only minimal production code was written to pass the tests
- [ ] All tests (new and existing) pass with clean output
- [ ] Tests follow `writing-good-tests.md` (behavior-focused, DAMP, Real → Fake → Stub → Mock, hermetic & deterministic)
- [ ] Edge cases and error paths from the spec/plan are covered

---

## Common Rationalizations (Stop and Reject These)

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks too. A simple test takes 30 seconds. |
| "I'll write tests after I get it working" | Tests written after code pass immediately — you never proved they can catch a failure, and they tend to test implementation instead of behavior. |
| "I already tested it manually" | Manual checks are ad-hoc, unrepeatable, and won't catch future regressions. |
| "Deleting my pre-written code is wasteful" | Keeping untested code is sunk-cost fallacy. Rewriting from a failing test takes minutes and produces cleaner design. |
| "It's hard to test without mocking everything" | Hard-to-test code is a design signal. Simplify the interface or use a Fake instead of fighting mocks. |