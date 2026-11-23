### Refactoring

**You own the contract. The structure changes. The behavior does not.** Distinct from Feature, which adds behavior, and Bug fix, which corrects it.

If the cleanup reveals a missing feature or a real bug, split it out and ship the structural change first against the pinned contract. A redesign is allowed, but name it and route to Feature. Large or cross-cutting structural work routes to a dedicated multi-phase plan (`docs/paddlr/plans/`). This playbook is for focused-to-medium changes in a single-agent execution context.

1. **Pin the Behavior Contract First:** Trace the affected subsystem to learn the contract, then write a characterization test, snapshot, or equivalence harness that captures current behavior before any structure moves. If the area has no coverage, write the pin before touching structure. Type checks and linters are not a behavioral pin.
2. **Model Missing Structure:** Name the structure the code is missing per **principle-model-the-domain**. Existing code stays when the shape is already clear and local. The reshape must delete branches or invalid states, not add indirection.
3. **Target Architecture:** State what the module layout, types, and call graph should be if built today (**principle-foundational-thinking**, **principle-redesign-from-first-principles**). If the target crosses a function or module boundary, invoke the **architect** skill for the shape before making the move.
4. **Subtract Before Adding:** Delete dead code, collapse one-caller wrappers, drop redundant validators, and remove orphan references before introducing the new shape (**principle-subtract-before-you-add**). The smallest change that reaches the target shape ships (**principle-laziness-protocol**). A speculative cleanup that "might help" gets reverted.
5. **Integrate with TDD Refactor Phase:** Execute mechanical edits directly in-thread keeping the pinned tests green (**test-driven-development**). For API reshapes, migrate every caller and delete the old API in the same wave (**principle-migrate-callers-then-delete-legacy-apis**). No compatibility shims, no parallel old-and-new paths. Spot-check every rename across all references.
6. **Prove Invariant Behavior:** Prove behavior is unchanged on the real artifact, not "it compiles" (**principle-prove-it-works**). Run equivalence checks: diff old-vs-new outputs, replay recorded baselines against new code, or run existing integration tests.
7. **Verify Reduced Reader Load:** The true success measure is reduced cognitive load (**principle-minimize-reader-load**). If the diff does not lower reader load somewhere, revert it.
8. **Sequence Verifiable Slices:** Rebase into small ordered commits: a subtraction commit, then the reshape, then follow-on cleanup (**principle-sequence-verifiable-units**).
9. **Open PR:** Invoke **Opening a PR** (`playbooks/opening-a-pr.md`).

**Reply:** the structure that changed, the pin you held it against, equivalence proof, reader-load delta, what shipped and what was reverted. No new behavior.
