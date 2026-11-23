### Perf issue

**You own the measurement story. Plan, review, verify the numbers.** Tie every fix to an empirical measurement; never evaluate performance from code inspection alone (**principle-prove-it-works**, **principle-explain-the-number**).

1. **Capture Baseline Measurement:** Capture a baseline trace or metric using standard profiling tools (`py-spy`, `node --cpu-prof`, benchmark scripts, or SQLite trace dumps). Vet the baseline, and each subsequent number, with the **benchmark-checklist** skill.
2. **Trace Code & Hypotheses:** Trace the code to ground hypotheses. Do not claim a performance ceiling without profiling first. Try the 7 performance mantras in order, cheapest first:
   1. *Don't do it.* Eliminate work whose result is unused.
   2. *Do it, but don't do it again.* Cache or memoize across calls.
   3. *Do it less.* Reduce frequency or batch operations.
   4. *Do it later.* Defer off the critical latency path.
   5. *Do it when they're not looking.* Background or idle processing.
   6. *Do it concurrently.* Parallelize independent computation.
   7. *Do it cheaper.* Algorithmic, data structure, or primitive optimization.

   When an earlier mantra achieves the performance target, stop (**principle-laziness-protocol**).
3. **Plan & Implement Fix:** Plan the fix from the profile. If it crosses a module boundary, invoke the **architect** skill first. Execute the fix directly in-thread (or via a bounded delegation brief if worker dispatch is supported). Capture a post-fix trace under identical conditions. Verify each attempt before trying the next (**principle-sequence-verifiable-units**).
4. **Compare Artifacts:** Parse and compare baseline and post-fix measurements (diff SQLite tables, JSON traces, or benchmark logs). "Inconclusive" or unverified numbers are not a pass.
5. **PR Evidence:** Cite the baseline metric, post-fix metric, sample count, noise floor, and limiting resource in the PR body.
6. **Open PR:** Invoke **Opening a PR** (`playbooks/opening-a-pr.md`).

For sustained, iterative optimization against an empirical metric, invoke the **Hillclimb** playbook (`playbooks/hillclimb.md`).

**Reply:** baseline number, post-fix number, delta percentage, limiting resource, and artifact path.
