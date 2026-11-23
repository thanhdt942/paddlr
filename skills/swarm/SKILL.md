---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
disable-model-invocation: true
---

# Swarm

Coordinated parallel worker execution across independent slices or competitive race arms.

## Phase A: Frame

1. **Done Predicate:** State the empirical done predicate and the expected output artifact or report.
2. **Execution Shape:** Choose the coordination pattern:
   - *Slice Partitioning:* Disjoint modules, services, or test suites.
   - *Competitive Race:* N workers on identical briefs (`first pass`, `rank all`, or `best-of`).
3. **Model Profiles & Worker Allocation:**
   - Map worker tiers using the Runtime Adapter Contract (`skills/paddlr-mode/references/runtime-adapters.md`) via optional model profile hints (`fast-mechanical`, `standard-code`).
   - Give each worker its own isolated working directory, Git worktree, or branch (**principle-separate-before-serializing-shared-state**).
4. **Single-Agent Fallback:** If the host runtime does not support parallel subagent dispatch (`agent.delegate`), execute the slices sequentially in the main thread with state bracketing.

## Phase B: Execution / Fan Out

When subagents are supported, dispatch workers in isolated environments with explicit `DelegationBrief`s.

Every brief stands alone: goal, exact scope boundaries, verification command, and expected return status (`PASS`, `ISSUES`, or `BLOCKED` with evidence).

Workers return patches or reports; workers must *never* modify canonical Task State or merge directly to the main trunk.

## Phase C: Sequential Integration & Aggregation

The Main Agent drains worker results sequentially:
- Drop or re-run workers with malformed outputs or unverified assertions.
- Merge patches into the working tree one by one, executing the verification suite after each integration (**principle-sequence-verifiable-units**).
- For competitive races, apply the selection rule declared up front.

## Phase D: Report

Deliver a consolidated summary:
- Status table across slices or race arms.
- Issue details with verbatim verification proofs.
- Any gaps, drops, or unverified regions.
