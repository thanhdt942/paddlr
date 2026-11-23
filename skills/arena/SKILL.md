---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
disable-model-invocation: true
---

# Arena

Compare competing design candidates against a frozen rubric.

## Phase A: Frame

Every candidate receives the identical prompt. The prompt is the contract.

1. **Task Definition:** Explicitly declare the artifact each candidate must produce.
2. **Rubric Derivation:** Derive 3–6 concrete, falsifiable evaluation criteria defining architectural and functional success.
3. **Execution Model & Profiles:**
   - When subagent delegation is supported (`agent.delegate`), spawn independent runners using diverse model reasoning tiers (`deep-reasoning`, `standard-code`) via the Runtime Adapter Contract (`skills/paddlr-mode/references/runtime-adapters.md`).
   - **Single-Agent Fallback:** If subagent dispatch is unsupported, the Main Agent drafts 2–3 competing designs sequentially in-thread.
4. **Concurrency Isolation:** Allocate each candidate its own isolated working directory or Git worktree (`.scratch/arena-<slug>/candidate-<n>/`) per **principle-separate-before-serializing-shared-state**.

## Phase B: Execution

Execute candidates against the shared task specification. Each candidate produces its artifact and a concise design note explaining alternatives considered and rejected.

If a candidate fails or drops out, continue with the remaining candidates.

## Phase C: Cross-Evaluation

Score candidates against the rubric:
- When multi-agent cross-judging is supported, dispatch a blinded evaluator on an alternate model profile.
- In single-agent fallback, the Main Agent scores each candidate against the rubric criterion by criterion before selecting a base.

## Phase D: Pick a Base

Read every candidate thoroughly. Score each against the rubric criteria. Select the base that future maintainers can extend most easily while preserving invariants (**principle-minimize-reader-load**). When tied, choose the smaller API surface and cleaner boundary (**principle-laziness-protocol**).

## Phase E: Graft

Identify high-value elements from losing candidates worth incorporating into the winning base (typically 1–2 focused improvements). Graft them into the base holistically (**principle-redesign-from-first-principles**).

If candidates naturally converge on one shape, adopt the consensus. If they diverge wildly, the task was under-specified: reframe Phase A rather than averaging incompatible designs.

## Phase F: Verify

Verify the synthesized artifact against the real test suite or execution harness (**principle-prove-it-works**).

## Outputs

One synthesized artifact with a synthesis note: winning base, scoring against rubric, grafted components, rejected approaches, and verification evidence.
