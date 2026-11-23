### Pause safely

**You own a clean stop. Leave a durable checkpoint a cold-start agent can resume from.**

This action is explicit only. On instructions like "keep going", "run until done", or "don't stop", do not pause.

1. **Stop at a Safe Boundary:** Finish the current atomic step or revert cleanly. Start nothing new.
2. **Reversible Actions Only:** Take no irreversible action to pause. No deployment and no push unless a PR was already out.
3. **Durable Recoverable Work Invariant:** Ensure working state is safely preserved. Committing uncommitted edits as a `wip:` commit on the current branch is one supported mechanism so nothing is lost; working tree state can also be preserved in place if uncommitted. If the tree is broken, state so explicitly.
4. **Persist Resume State to Canonical Plan:** Update the canonical Task State in `docs/paddlr/plans/YYYY-MM-DD-<slug>.md`:
   - Set status to `paused`.
   - Record the last verified step and current checkpoint.
   - Record exact next action on resume.
   - List touched key files and active branch.
   - Note any known gotchas or incomplete thoughts.

**Reply:** where you paused in the loop, what is on disk versus active context (paths, no raw diff dumps), the commits made, whether the tree is clean, and the exact first action to take upon resuming.
