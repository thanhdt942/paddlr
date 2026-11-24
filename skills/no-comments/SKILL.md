---
name: no-comments
description: "Audit a diff for unnecessary comments, suppressions, and workaround justifications using the Comment Sicko checklist, then fix accepted findings and offer structural encodings for claimed constraints."
disable-model-invocation: true
---

# No comments

Run a strict comment and workaround audit over the scoped diff, act on accepted findings, and replace prose constraints with structural checks where possible.

## Scope

Use the caller's specified files or diff. Otherwise use the current diff against the repository's default base branch (e.g., `dev` or `main`), including working-tree changes.

## Execution Mode (Agent-Agnostic)

1. **Multi-Agent Delegation (`agent.delegate` when supported):**
   - Delegate the comment-audit pass to a fresh worker loaded with [comment-sicko.md](comment-sicko.md) and the scoped file list or diff. Do not restate its rules in the brief.
2. **Single-Agent Fallback:**
   - Read [comment-sicko.md](comment-sicko.md) and execute its audit checklist directly in-thread before applying any code reshapes.

## Steps

1. **Run the Audit Pass:** Execute [comment-sicko.md](comment-sicko.md) over the scope to delete unjustified comments and flag workarounds/suppressions (`MUST KILL`).
2. **Verify Audit Output:** Inspect the resulting report and diff. Reject application-code edits made during the comment pass, scope escapes, exception-protected deletions, misstated `MUST KILL` reasons, and flags that treat intentional code as guilty. Reshape flags on surprises in our own code stay actionable; do not restore those comments. A keep survives only with proof it describes an external constraint we cannot reshape. Audit missed lint/type suppressions in scope: correctness or safety suppressions remain actionable `MUST KILL`s. Before accepting thin `IMPORTANT` or `do not remove` kills or keeps, trace the symbol or invoke **why**. If a kill is ambiguous, do not restore. If a keep is refuted or still ambiguous, delete it. Revert and rerun once if the audit violated its fence; reject a second violation and report `/no-comments` failed.
3. **Shape Non-Trivial Fixes:** Fix trivial accepted flags directly (delete a dead path, drop an unused parameter, call the real API). If any fix requires a structural redesign, invoke **architect** once for the accepted set and surrounding code. Stop at the sketch; Step 4 implements.
4. **Implement Minimal Root-Cause Fixes:** Remove every named workaround in scope. If the root cause lies outside scope, land the smallest in-scope fix and report the remainder open. Follow **principle-fix-root-causes** and **principle-redesign-from-first-principles** without widening the fence or bolting on symptom guards.
5. **Encode Claimed Constraints:** Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave verified keeps about external constraints we cannot change. For internal constraints, offer the cheapest in-scope type, runtime check, test, or CI lint (**principle-encode-lessons-in-structure**). Wait for user approval when interactive (or require pre-approval in unattended runs). If approved, encode then delete the comment; otherwise delete, report the constraint open, and sketch follow-up work.
6. **Report:** Deletion count, restored comments, reruns, architect sketch (if any), fixes landed, encoding offers, encodings landed, unenforced constraints, and open follow-ups.
