# Writing Good Tests

**Load this reference when:** writing or modifying tests, introducing test
doubles (fakes, stubs, mocks), or extracting test helpers.

## Overview

A good test catches real bugs while staying silent during refactors. Four
principles from *Software Engineering at Google* govern everything here:

```
1. Test behavior, not implementation
2. Keep tests clear and self-contained (DAMP over DRY)
3. Prefer real implementations over test doubles
4. Keep every test hermetic and deterministic
```

Strict TDD enforces these naturally: a test written before the code can
only target public behavior, and you only reach for a test double when
the real dependency is genuinely slow, nondeterministic, or external.

---

## Principle 1: Test Behavior, Not Implementation

Test **what** the system does through its public API, never **how** it
does it internally. If you refactor the internals without changing
observable behavior, every test should still pass untouched.

**Test via public APIs only.** Never call private helpers, inspect
internal fields, or assert on internal call sequences just to verify
state. If a behavior is hard to test through the public API, that is a
design smell in the production code, not a reason to break encapsulation.

**Test state, not interactions.** Assert on return values and resulting
system state rather than asserting that a specific internal method was
called with specific arguments.

```typescript
// ❌ Interaction test: breaks if we batch writes or rename saveRecord()
expect(repo.saveRecord).toHaveBeenCalledWith(user);

// ✅ State test: survives any internal refactor
await registerUser(repo, user);
expect(await repo.findById(user.id)).toEqual(user);
```

**One behavior per test (not one assertion).** Structure each test around
a single scenario using **Arrange – Act – Assert** (Given – When – Then).
Multiple assertions are fine when they verify different facets of the
same outcome; split the test when you need a second "Act".

**Name the behavior, not the method.** A test name should read like a
specification so a failure tells you what broke without opening the file.

```typescript
// ❌ Method-centric
test('calculateDiscount', ...);

// ✅ Behavior-centric
test('applies 10% discount when order total exceeds $100', ...);
```

### Gate Function

```
BEFORE writing a test:
  Can I refactor the internal implementation without changing this test?
    NO  → You are testing implementation. Rewrite against the public API.

  Does the test name state the scenario and expected outcome?
    NO  → Rename to describe the behavior, not the function name.
```

---

## Principle 2: Keep Tests Clear and Self-Contained (DAMP over DRY)

Production code optimizes for **DRY** (Don't Repeat Yourself). Test code
optimizes for **DAMP** (Descriptive and Meaningful Phrases). A reader
should understand a failing test in seconds without jumping through
layers of abstractions.

**No logic in tests.** Never put `if/else`, loops, string concatenation,
or math formulas in a test to compute the expected value. Logic in tests
can contain the exact same bug as the production code. Use hand-derived
literals.

```typescript
// ❌ Logic in test: mirrors production bug and hides the actual expected value
const expected = baseUrl + '/users/' + id;
expect(buildUserUrl(id)).toBe(expected);

// ✅ Hand-derived literal: instantly verifiable by eye
expect(buildUserUrl(42)).toBe('https://api.example.com/users/42');
```

**Prefer local setup over shared `beforeEach` magic.** Repeating 3–5
lines of setup inside a test is better than hiding state in a distant
`beforeEach` hook. Use small, explicit **factory/builder helpers** (e.g.,
`createUser({ role: 'admin' })`) that highlight only the fields relevant
to the test and default everything else.

**Write clear failure messages.** Use descriptive matchers (`toEqual`,
`toContain`, `toThrow`) rather than bare booleans (`expect(a === b).toBe(true)`).
When a test fails, the diff alone should explain why.

### Gate Function

```
BEFORE finalizing a test:
  Does the test contain loops, conditionals, or computed expected values?
    YES → Replace with hand-derived literals or table-driven cases.

  Must a reader scroll to another file or top-level hook to understand the inputs?
    YES → Inline the relevant setup or use an explicit factory with overrides.
```

---

## Principle 3: Prefer Real Implementations Over Test Doubles

When a dependency is needed, follow Google's strict hierarchy:

```
Real Implementation  >  Fake  >  Stub  >  Mock
```

1. **Real Implementation (Default):** Use the real object whenever it is
   fast, deterministic, and has no external side effects.
2. **Fake (Second Choice):** A lightweight working implementation (e.g.,
   an in-memory database, fake clock, or fake filesystem) when the real
   dependency is slow or external. Fakes preserve real behavior without
   coupling tests to internal calls.
3. **Stub (Third Choice):** Returns canned data to force a specific
   branch (e.g., simulating a 503 network error). Do not assert on how
   the stub was called.
4. **Mock (Last Resort):** Verifies that a specific interaction occurred.
   Reserve mocks strictly for **system boundaries** where the interaction
   itself *is* the observable side effect (e.g., sending an email, charging
   a payment gateway).

**Never mock what you don't own lightly, and never assert on the mock's
existence.** Over-mocking creates brittle tests that pass while
production breaks.

**Keep test-only code out of production.** Never add `resetForTest()`,
`destroy()`, or test-only flags to production classes. Put test cleanup
and builders in test utilities.

### Gate Function

```
BEFORE adding a mock:
  1. Can I use the real implementation?
       YES → Use it.
  2. Is it slow, nondeterministic, or external?
       YES → Can I use or build a simple Fake?
               YES → Use the Fake.
               NO  → Use a Stub (for inputs) or Mock (only for boundary side effects).
```

---

## Principle 4: Keep Every Test Hermetic and Deterministic

A flaky test destroys trust in the entire test suite. Every test must
produce the exact same result whether run alone, in parallel, in random
order, or on a different machine.

- **No shared mutable state:** Each test creates and cleans up its own
  state. Never rely on a previous test having run first.
- **No real clock, randomness, or network:** Inject a fake clock for
  time-dependent logic, seed any randomness, and block real network calls.
- **Keep unit tests fast:** Milliseconds per test. Slow tests don't get
  run during the TDD Red-Green-Refactor loop.

---

## Quick Reference

| When you... | Do |
|-------------|-----|
| Write a new test | Target public API and observable state, not internals |
| Name a test | Describe the scenario and expected behavior |
| Compute an expected value | Hardcode a hand-derived literal; no logic in tests |
| Share setup across tests | Use explicit factory helpers with defaults, not hidden `beforeEach` state |
| Need a dependency | Follow Real → Fake → Stub → Mock |
| Test a boundary side effect | Mock only at the system boundary (email, payment, external API) |
| Need test-only cleanup | Put it in test utilities, never on production classes |
| Deal with time or randomness | Inject a fake clock or fixed seed |

---

## Warning Signs

- A refactor that doesn't change behavior breaks multiple tests
- Tests assert `toHaveBeenCalledWith` on internal collaborators instead of checking resulting state
- Test body contains `if`, `for`, or helper functions that compute `expected`
- You have to read 3 helper files or a 40-line `beforeEach` to understand one test
- Mock setup is longer than the Arrange/Act/Assert logic
- A test passes alone but fails when run in parallel or in a different order
- Production classes contain methods or flags used only by test files