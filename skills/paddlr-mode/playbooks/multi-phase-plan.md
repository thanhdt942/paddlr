### Multi-phase or multi-PR plan

**You own the plan, not the code. The plan is a verifiable checklist an engineer executes slice by slice and audits from concrete evidence.** The plan is the deliverable; do not implement during planning.

1. **Lightweight Trivial Tasks Exemption:** When the change is localized to one or two files with an obvious, low-risk approach, skip formal plan authoring. State intent and proceed directly.
2. **Prototype Open Forks:** Settle open technical questions by prototyping beforehand per `playbooks/prototype.md`. Clarify with the user only on product direction or subjective preference calls.
3. **Invoke Writing Plans:** Invoke the **writing-plans** skill to structure the plan into `docs/paddlr/plans/YYYY-MM-DD-<slug>.md`. Include YAML frontmatter conforming to the Task State Schema (`task-state-schema.md`).
4. **Structured Slicing:** Structure the plan into bite-sized, contract-first tasks (`Consumes` / `Produces`) with checkbox steps (`- [ ]`). Define a dependency graph showing independent vs. serialized slices (**principle-sequence-verifiable-units**).
5. **Concrete Verification Criteria:** Each phase must define falsifiable exit conditions and verification commands (unit, integration, and performance benchmarks where applicable).
6. **Hand Over Plan Path:** Persist the plan file, verify internal markdown links, and return the canonical plan path to the user. Execution begins only upon explicit authorization.

**Reply:** the plan path, ordered phases/tasks with their dependencies, and any unproven assumptions requiring confirmation.
