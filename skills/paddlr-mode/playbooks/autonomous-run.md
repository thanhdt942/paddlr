### Autonomous run

**You own the exit condition. Define done, then drive to it without stopping.**

> **Core v1 Note:** Unattended background looping (`scheduler.loop`) and daemon processes are deferred beyond Core v1. In Single-Agent Core v1, autonomous iterations execute sequentially within the active agent invocation under the Main Agent's direct supervision.

1. State the exit condition as a checkable predicate before the first iteration (tests green, repro fixed, all N PRs merged, pixel-diff zero).
2. Pick the iterative mechanism supported by your runtime environment. An event to watch (CI, a merge, a ref advancing) evaluates event state per iteration; without an external event, run focused verification iterations against the predicate.
3. Each iteration makes the smallest change the evidence justifies, verifies it against the predicate, commits if it advanced, discards changes that didn't help. Belt-and-suspenders that "might help" gets reverted, not left to ride.
   Sequence the work via the **sequence-verifiable-units** principle skill, verifying each unit before the next instead of batching checks at the end.
4. Mid-run discoveries that support the goal are yours. Address broken skills, related bugs, flaky verifiers, review noise, tooling failures, orphaned follow-ups, and fixable drift yourself via paddlr-mode. Put out-of-band fixes in their own PR. Do not park reversible work for the human. Surface only irreversible actions, genuine product or preference calls no experiment can settle, or a real dead end. Keep the predicate as the main drive, and return to it after each side fix.
5. Checkpoint every iteration into the canonical Task State in `docs/paddlr/plans/YYYY-MM-DD-<slug>.md`, recording what changed, verification evidence, and whether the exit predicate advanced.
6. Stop when the predicate is met. A plateau is not a stop, so keep going and pivot your approach to push past it. Surface a genuine dead end rather than spinning, and never relax the predicate to declare victory.

**Reply:** the exit condition, iterations run, what landed, what was discarded, final predicate state.
