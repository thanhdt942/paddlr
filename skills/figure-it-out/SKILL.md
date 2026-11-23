---
name: figure-it-out
description: "Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Scales rigor to the task, runs a hypothesis loop, and logs decisions. Use for /figure-it-out or 'figure it out'."
disable-model-invocation: true
---

# Figure it out

When the task matches no existing playbook, design one. The deliverable before any code is the workflow itself: a sequence of phases that scales rigor to the task, runs the scientific method, and leaves an audit trail in `docs/paddlr/plans/` that a human can verify after stepping away.

## Start

Create a canonical task plan in `docs/paddlr/plans/YYYY-MM-DD-<slug>.md` per the Task State Schema. Record the phases below as checklist items.

## Phase A: Frame

Ground first, then commit. Do not start implementation until you can state:
- The definition of done as a falsifiable predicate (**principle-prove-it-works**).
- Scope, quantified: rough units, affected modules, and known blockers.
- The rigor level, biased high. One-way doors and high blast radius get formal plans and specifications. Reversible low-stakes steps get lightweight slices.

Present framing and trade-offs before committing to an extended run (**principle-never-block-on-the-human**).

## Phase B: Design the Workflow

Decompose into atomic, independently-landable units. Sequence riskiest-unknown-first. Scaffold and verification precede features (**principle-foundational-thinking**).

- Build the verification harness before the work, with the baseline captured from the pre-change state.
- For one-way-door architectural choices, invoke the **architect** skill. Skip it for mechanical work whose shape is already clear (**principle-laziness-protocol**).
- Decide execution seams. In Single-Agent mode, execute slices sequentially; when worker dispatch is active (Phase 4+), give each worker an isolated worktree (**principle-separate-before-serializing-shared-state**).
- Write the designed phase list into the canonical task plan.

## Phase C: Run the Loop

Each unit is an experiment. State the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep it if it advanced, revert it if it did not. Apply the **sequence-verifiable-units** principle skill, verifying each unit before starting the next.

- Verify by inspecting the real artifact, never a self-report.
- A verdict is `PASS`, `FAIL`, or `INCONCLUSIVE`. Inconclusive is not a pass; investigate the gap.

## Phase D: Keep the Audit Trail

Log each completed step in the canonical task plan in `docs/paddlr/plans/YYYY-MM-DD-<slug>.md`. The plan plus the git diff allows engineers to audit and trust the work.

## Phase E: Verify and Hand Back

Check the whole system against the Phase A predicate on the real product, not just isolated harnesses. Encode any recurring lesson as a lint rule, check, or script (**principle-encode-lessons-in-structure**).

**Reply:** the playbook you designed, rigor level and rationale, canonical plan path, what is verified against the predicate, and remaining open threads.
