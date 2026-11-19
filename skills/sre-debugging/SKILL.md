---
name: sre-debugging
description: Evidence-based software debugging and troubleshooting using Google SRE Effective Troubleshooting and Andreas Zeller's Scientific Debugging. Use when encountering any bug, test failure, production incident, unexpected runtime behavior, regression, crash, or performance issue, BEFORE proposing or implementing fixes.
---

# sre-debugging

**Core principle:** ALWAYS prove the root cause before implementing a permanent fix. Symptom fixes are failure.

## The Iron Law

```
NO PERMANENT FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

**Google SRE Exception (Active Outages):** If a live service is actively degraded or losing data, mitigate first (rollback, traffic shift, feature flag, restart) to stop the impact. Capture logs, stack traces, or state snapshots before restarting so forensic evidence is not lost. Mitigation restores service; it does NOT replace root cause analysis.

## Methodology

- **Google SRE - Effective Troubleshooting**: Hypothetico-Deductive Method, evidence-based diagnosis, simplification, and separating mitigation from root cause analysis.
- **Andreas Zeller - Scientific Debugging**: Reliable reproduction, Delta Debugging, discriminating experiments, fault localization, and the `Defect -> Infection -> Failure` causal chain.
- **Brendan Gregg - Performance Analysis**: RED, USE, and Drill-Down methods (used only for latency, throughput, or resource bottlenecks).

## The Four Phases

Complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE proposing ANY fix:**

1. **Read Errors Completely**: Inspect exact error messages, full stack traces, line numbers, and expected vs. actual behavior. Separate confirmed facts from assumptions.
2. **Reproduce & Simplify**: Establish a reliable reproduction with exact inputs and environment. Shrink inputs and isolate components (see `references/zeller-techniques.md`).
3. **Check Recent Changes**: Inspect `git diff`, recent commits, config updates, and dependency changes. Treat them as leads, not proof (correlation != causation).
4. **Instrument Multi-Component Boundaries**: Across multi-layer systems (CI -> build -> deploy, API -> service -> DB), log data entering/exiting each boundary and verify config propagation before proposing fixes. Run once to prove *which boundary* fails.
5. **Trace Backward**: Trace from **Observed Failure** -> **State Infection** (earliest invalid state) -> **Root Defect**. Fix at the source, never at the crash site.

### Phase 2: Pattern & Differential Analysis

1. **Find Working Examples**: Locate a similar working implementation or minimal passing run.
2. **List All Differences**: Compare passing vs. failing execution paths (inputs, state, config, timing, dependencies). Do not assume any difference is irrelevant.
3. **Check Invariants**: Verify preconditions, postconditions, and assumptions at module/API boundaries.

### Phase 3: Hypothesis & Experiments

1. **Form Falsifiable Hypotheses**: State clearly: "I think X is the root cause because Y." For non-trivial bugs, log 2 to 3 competing hypotheses in `references/hypothesis-log-template.md`. For performance issues, consult `references/performance-methods.md`.
2. **Predict Before Testing**: Define what observable output confirms or refutes the hypothesis *before* running the experiment.
3. **Test Minimally**: Change **one variable at a time**. Mark each hypothesis as **Confirmed**, **Refuted**, or **Inconclusive**.
4. **Loop on Failure**: If refuted, revert any diagnostic tweaks and return to Phase 1/3 with the new evidence. Do NOT stack speculative changes.

### Phase 4: Implementation & Verification

1. **Use `test-driven-development`**: Invoke the `test-driven-development` skill to write a minimal failing regression test first (red), then implement the fix (green).
2. **Single Focused Fix**: Apply the smallest clean change that eliminates the root defect. No bundled refactoring, no "while I am here" edits, and no broad `try/catch` or arbitrary `sleep` calls that mask corrupted state.
3. **Verify**: Confirm the reproduction test passes and the relevant test suite has no regressions. Summarize: root cause, evidence, fix applied, and verification results.
4. **3-Strike Rule**: If a fix fails, revert it and return to Phase 1. If **3+ fixes fail**, **STOP** — do not attempt Fix #4. Treat it as an architectural flaw and discuss redesign options with the user.

## Red Flags - STOP and Return to Phase 1

- "Quick fix for now, investigate later" (outside a live outage)
- "Just try changing X and see if it works"
- Applying multiple changes at once
- Skipping the failing test to "verify manually"
- Proposing a fix before tracing the causal chain
- Attempting a 4th fix after 3 failed attempts

## When to Stop and Ask

Stop investigating and ask the user instead of guessing when:

- The failure cannot be reproduced and no logs, stack traces, or metrics exist.
- Required telemetry, environment access, or configs are outside your visibility.
- Differentiating remaining hypotheses requires running a command you cannot execute.

Report: (1) confirmed facts, (2) remaining plausible hypotheses, and (3) the exact evidence needed.

## Reference Guides

Load only when needed:

- `references/hypothesis-log-template.md` - Template for observations, ranked hypotheses, predictions, experiments, and causal chains.
- `references/zeller-techniques.md` - Reproduction, Delta Debugging, fault localization, and the `Defect -> Infection -> Failure` chain.
- `references/performance-methods.md` - Brendan Gregg's RED, USE, and Drill-Down methods (performance issues only).
