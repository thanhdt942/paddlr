### Session pickup

**You own the resume point. Read the prior trail, don't redo completed work.** Single-Agent execution baseline.

1. **Locate Canonical Task State:** Locate the active task plan under `docs/paddlr/plans/YYYY-MM-DD-<slug>.md`. Read the YAML frontmatter (`status`, `playbook`, `active_phase`), the resume note, and the last verified step.
2. **Reconstruct Operational State:** Inspect Git state (`git status`, `git branch --show-current`, `git log -n 5`, `git diff`). Identify what already landed, what is uncommitted, and the decisions recorded in `docs/paddlr/decisions/` or the plan. The prior plan is authoritative input; resist the bias to re-derive it from scratch.
3. **Diff Done vs. Pending:** Compare what is completed against what remains in the plan checklist. Identify the exact next action. Do not redo completed work or re-run passing tests unless needed for baseline re-verification.
4. **Baseline Re-Verification:** Execute the baseline verification command (e.g. test suite or build) to prove that the inherited working state compiles and passes its baseline tests before applying new changes (**principle-prove-it-works**).
5. **Route Remaining Work:** Update the task plan status from `paused` to `in_progress`, route to the matching playbook (Feature, Bug fix, Refactoring, etc.), and continue execution.

**Reply:** where the prior session stopped, what you inherited vs redid (nothing redone beyond baseline verification), baseline verification results, the resume point, and the immediate next step.
