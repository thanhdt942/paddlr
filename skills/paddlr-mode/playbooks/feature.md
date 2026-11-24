### Feature

**You own the design. Plan, execute, review, verify.** Single-Agent execution baseline. Stay in the lead.

1. **Intake & Subsystem Trace:** Trace the affected subsystem and establish the task intent, done predicate, and constraints per the Intent Contract.
2. **Domain Architecture:** Name the data shape first. If the change crosses module boundaries or introduces new abstractions, invoke the **architect** skill to model types, state machines, and boundaries before writing logic.
3. **Throughput Checkpoint:** Formulate the checkpoint as four explicit dimensions in the canonical plan (`docs/paddlr/plans/YYYY-MM-DD-<slug>.md`):
   - **Blocking first steps.** Prerequisite schemas, foundational types, or test harnesses required before implementation.
   - **Independent workstreams.** Disjoint files, modules, or layers that can be developed in separate verifiable slices.
   - **Shared mutable state.** Default to splitting the target (**principle-separate-before-serializing-shared-state**). Serialize only for real system invariants.
   - **Smallest safe decomposition.** Break work into bite-sized, verifiable units (**principle-sequence-verifiable-units**).
4. **Lifecycle Coordination:** Invoke the **feature-development** skill for the end-to-end 5-phase delivery flow:
   - *Phase 1 (Intake):* Intent restatement and assumption extraction.
   - *Phase 2 (Spec):* Feature specification in `docs/paddlr/specs/YYYY-MM-DD-<slug>.md` (or `.paddlr.json` override).
   - *Phase 3 (Plan):* Contract-first plan in `docs/paddlr/plans/YYYY-MM-DD-<slug>.md` (or `.paddlr.json` override). For reversible Level 2 branch work with clear requirements, proceed straight to Phase 4 without blocking for approval (**principle-never-block-on-the-human**). For Level 3 architectural/breaking changes, record an ADR via **writing-decisions** and pause for explicit approval before Phase 4.
   - *Phase 4 (Implement):* Test-driven development (**test-driven-development**), maintaining type system discipline (**principle-type-system-discipline**).
   - *Phase 5 (Verify & Review):* Verification on real surface (**principle-prove-it-works**), doc-drift check (**sync-docs**), and diff audit (**code-review**).
5. **Implementation Execution:** Execute slices sequentially within the main agent thread. Model the domain using typed models and state machines rather than scattered booleans (**principle-model-the-domain**). Surgical edits; commit liberally using Conventional Commits.
6. **Verification on Real Surface:** Verify against the real artifact, not proxies or compilation alone (**principle-prove-it-works**). Capture verbatim passing output.
7. **Sequence Verifiable Units:** Rebase into small, ordered commits. Build, verify, and commit each small unit before the next (**principle-sequence-verifiable-units**).
8. **Contested Design Resolution:** If architectural alternatives remain contested, prototype side-by-side per `playbooks/prototype.md` (**principle-exhaust-the-design-space**) or resolve via red-teaming.
9. **Open PR:** Invoke **Opening a PR** (`playbooks/opening-a-pr.md`).

**Reply:** what you built, architectural choices and rationale, the throughput checkpoint, verification evidence, and the canonical plan path.
