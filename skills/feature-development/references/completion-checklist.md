# Completion Checklist

Verify every applicable item below during Phase 6 (Completion Gate) before declaring the feature complete. Never claim completion without direct verification evidence.

## 1. Requirements and Scope

- [ ] All stated functional requirements are implemented.
- [ ] Every acceptance criterion (from the user prompt or spec) has been explicitly checked.
- [ ] All code changes remain within the agreed feature scope; no unrequested refactors or stray debug artifacts remain in the diff.

## 2. Testing and Regression Checks

- [ ] Relevant unit, integration, or end-to-end tests covering the new feature were executed and passed.
- [ ] Existing tests in affected areas were executed to confirm no unhandled regressions were introduced.
- [ ] Build, type-checking, and linting checks relevant to the modified files were executed and passed.

## 3. Code Quality and Review

- [ ] `code-review` was performed when required by `references/workflow-decisions.md`, and critical findings were resolved.
- [ ] Error handling, edge cases, and boundary conditions align with existing codebase conventions.
- [ ] Documentation, comments, or configuration examples were updated if the feature changes public usage or setup.

## 4. Evidence-Based Handoff

Before writing the final response, confirm that your report includes:

- [ ] **Summary of changes**: What was built and which components/files were updated.
- [ ] **Verification evidence**: The exact commands or checks run and their observed outcomes (do not claim tests pass unless you actually ran them and saw them pass).
- [ ] **Open issues and limitations**: Any skipped checks, unverified environments, known edge cases, or out-of-scope tech debt discovered during implementation, stated clearly and honestly.

If any required check failed or could not be executed, mark the feature as **partially complete** or **blocked**, explain the exact gap, and specify what is needed to close it.
