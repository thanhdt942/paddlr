# Scientific Debugging Techniques (Andreas Zeller)

Apply these techniques when a bug is difficult to reproduce, inputs or codebases are large, or the defect location is not obvious from the initial stack trace.

## 1. Reliable Reproduction

A bug you cannot reliably reproduce is difficult to prove fixed.

- **Lock down inputs and environment**: Capture exact payloads, CLI flags, config files, database state, timezone, locale, and dependency versions.
- **Control nondeterminism**: For flaky or timing-dependent bugs, fix random seeds, mock clocks, increase concurrency, or add controlled delays to surface race conditions consistently.
- **Automate early**: Turn manual steps into a single runnable command or failing test case so every experiment takes seconds.

## 2. Simplification (Delta Debugging)

Reduce the failing case to the smallest possible input, configuration, or change set that still triggers the failure.

- **Input reduction**: Split the failing input in half. If either half still fails, discard the other half and repeat. Continue until removing any remaining element makes the failure disappear.
- **Configuration reduction**: Disable unrelated middleware, plugins, or feature flags to isolate the minimal active subsystem.
- **Change reduction (`git bisect`)**: When a bug is a regression between a known-good commit and a failing commit, use binary search over commit history to pinpoint the exact introducing commit.

A minimal failing case often exposes the root cause immediately by stripping away distracting context.

## 3. Hypothesis Formation and Discriminating Experiments

Treat debugging like controlled experimentation:

- **Formulate competing hypotheses**: Avoid tunnel vision on a single explanation. Ask "What else could produce these exact observations?"
- **Design discriminating tests**: Prefer an experiment whose outcome distinguishes H1 from H2 over one that only checks H1 weakly.
- **Predict before observing**: Write down what you expect to see *before* running the test or adding instrumentation. Unexpected results are the highest-value clues.
- **Inspect state, not just outputs**: Use targeted logging, assertions, or debugger breakpoints to inspect intermediate variable values along the execution path.

## 4. Fault Localization

Narrow the search space systematically instead of reading the entire codebase linearly:

- **Binary search the execution path**: Pick the midpoint between input entry and failure site. Check whether program state is already corrupted there.
  - If state is valid at the midpoint, the defect lies in the **second half**.
  - If state is already invalid at the midpoint, the defect lies in the **first half**.
- **Differential analysis (passing vs. failing runs)**: Compare a minimal passing run against a minimal failing run. Focus on the earliest point where control flow, data values, or external responses diverge.
- **Check boundary invariants**: Verify preconditions and postconditions at module, API, serialization, and database boundaries.

## 5. Causal Analysis (The Infection Chain)

Zeller models every failure as a three-step causal chain:

1. **Defect**: The static error in code, config, or data.
2. **Infection**: Execution of the defect creates an invalid internal program state.
3. **Failure**: The invalid state propagates until it produces an externally visible error.

Keep two rules in mind:

- **Failure site != defect site**: The line where an exception is thrown is often only where the infection finally became visible. Trace backward from the failure to the earliest infected state, then to the defect that created it.
- **Fix the defect, not the propagation**: Suppressing an exception or patching a downstream variable leaves the infection intact and often causes subtler bugs elsewhere.
