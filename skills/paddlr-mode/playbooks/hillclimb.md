### Hillclimb

**You own the metric and the experiment's integrity. Supervise, iterate, and verify.** For sustained, iterative improvement of one measurable metric against an empirical target. A one-off fix is Bug fix or Perf issue; Hillclimb is the optimization loop.

Core discipline: one change, one measurement, keep or revert. Never stack untested changes, and never claim a win from code inspection alone (**principle-prove-it-works**).

1. **Ground Workload & Metric:** Trace the target code and identify realistic workload dimensions (data size, history, state, concurrency). Select a case that reproduces the bottleneck. Fix one concrete metric, the direction that counts as better, and a falsifiable stop predicate pairing a target with a floor on attempts (e.g. "at least 30% faster than baseline and at least 5 iterations").
2. **Build Frozen Harness:** Build the measurement harness, prove its sensitivity against realistic workloads, then freeze it (**principle-build-the-lever**). Vet the harness with the **benchmark-checklist** skill. The frozen harness must emit the metric sampled enough to clear the noise floor (median of N runs) alongside error and throughput counts. Record baseline metrics and ensure regression tests pass before changing code.
3. **Open Trial Scratchpad:** Record raw iterations in an ephemeral `decision.tsv` scratchpad (gitignored), with columns: `id`, `hypothesis`, `change`, `before`, `after`, `delta`, `tests`, `verdict` (`kept` or `reverted`), `note`. The overall initiative status is tracked in the canonical task plan (`docs/paddlr/plans/YYYY-MM-DD-<slug>.md`).
4. **Formulate Architectural Hypotheses:** Ground each hypothesis in a concrete mechanism ("defer JSON parsing off the critical request path"), ordered by the 7 performance mantras.
5. **Iterate (One Hypothesis per Attempt):**
   - Execute the code change directly in-thread (or via a bounded delegation brief in an isolated worktree if subagent dispatch is enabled).
   - Measure before and after with the frozen harness, and run regression tests.
   - Accept only when the metric moves past the noise floor and all tests stay green. Otherwise revert the change in full (**principle-laziness-protocol**).
   - Record the row in `decision.tsv`. One commit per accepted fix, staging only touched files (`git add <files>`).
   - Each attempt concludes in a check before the next starts (**principle-sequence-verifiable-units**).
6. **Push Past Plateaus:** On consecutive rejections, pivot category, combine near-misses, or re-read source before concluding the hill is climbed. Correctness outranks speed: revert a win that breaks behavior; keep a simplification that holds the number.
7. **Stop Condition:** Stop when the stop predicate is satisfied or remaining ideas are marginal.
8. **Open PR:** Invoke **Opening a PR** (`playbooks/opening-a-pr.md`) with accepted commits stacked in order.

**Reply:** the metric and target, baseline to final with percent delta, iterations run (kept vs reverted), each accepted fix, path to `decision.tsv`, and recommended follow-ups.
