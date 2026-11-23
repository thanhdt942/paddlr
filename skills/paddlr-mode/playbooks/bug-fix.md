### Bug fix

**You own this task. Plan, diagnose, verify.** Single-Agent execution baseline. Stay in the lead.

Be scientific. Every shipped line traces to runtime evidence (**principle-prove-it-works**). Belt-and-suspenders that "might help" is a hypothesis, not a fix; it does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more (**principle-laziness-protocol**).

1. **Reproduce on the Matching Surface:** Reproduce the defect yourself with standard project test runners or command execution (`shell.exec`). Do not guess or rely on user reports alone. If it will not reproduce directly, synthesize the trigger, tighten preconditions, or add diagnostic logging until it reproduces consistently.
2. **Scientific Root Cause Investigation:** Invoke the **sre-debugging** skill. Formulate explicit, testable hypotheses. Binary-search the cause by ruling out candidates with runtime instrumentation and logging. Seed hypotheses by tracing the affected subsystem and querying regression history via the **why** skill. Confirm the surviving mechanism with runtime evidence before planning the fix (**principle-fix-root-causes**).
3. **Plan the Fix:** If the fix crosses module boundaries or reshapes state, invoke the **architect** skill first to ensure proper domain modeling. Keep the plan recorded in `docs/paddlr/plans/YYYY-MM-DD-<slug>.md` if non-trivial.
4. **Test-Driven Fix Execution:** Invoke the **test-driven-development** skill:
   - Write the smallest reproduction test that fails against the current head.
   - Stage and commit the failing repro test *before* applying the code fix (**principle-sequence-verifiable-units**).
   - Implement the minimal fix that turns the test green.
   - Refactor if necessary, keeping all tests passing.
5. **Verify on the Real Surface:** Prove that the original repro now passes and no regressions exist. "Inconclusive" or wrong-surface is not a pass (**principle-prove-it-works**). Unit tests prove branch behavior, not bug absence.
6. **Open PR:** Invoke **Opening a PR** (`playbooks/opening-a-pr.md`).

**Reply:** what was broken, confirmed root cause, minimal fix, verification evidence, and verbatim failing-then-passing test output.
