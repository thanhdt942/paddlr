---
name: code-review
description: Use when completing a task, finishing a feature, or before merging to verify code quality and spec alignment via an independent review
---

# Code Review

Dispatch a fresh, read-only reviewer subagent to evaluate completed work against the spec/plan and Google's code review standards — before issues cascade into later tasks.

**Announce at start:** "I'm using the code-review skill to review these changes."

**Core principle:** Review early, review often, and keep the reviewer's context isolated from the implementation session.

---

## When to Run Code Review

**Mandatory:**
- After completing a task or logical milestone in `docs/paddlr/plans/`
- After finishing a feature or bugfix
- Before merging a branch to `main`

**Optional but valuable:**
- Before a major refactor (baseline check)
- When stuck and needing a fresh perspective

---

## Step 1: Gather Minimal Review Context

Collect only what the reviewer needs — **never pass your implementation chat history**:

```bash
BASE_SHA=$(git merge-base origin/main HEAD) # or: git rev-parse HEAD~1
HEAD_SHA=$(git rev-parse HEAD)
```

Prepare these 4 inputs:
1. **`DESCRIPTION`**: 2–4 sentences summarizing what was built or changed.
2. **`SPEC_OR_PLAN`**: Exact path(s) to the relevant spec (`docs/paddlr/specs/...`) and/or plan (`docs/paddlr/plans/...`) and task number.
3. **`BASE_SHA`** and **`HEAD_SHA`**: Exact commit range to review.
4. **`TEST_GUIDE`**: Path to `writing-good-tests.md` (if present in the workspace).

---

## Step 2: Dispatch the Reviewer Subagent

Spawn a **read-only subagent with a fresh context** using the prompt template in `code-reviewer.md`, filling in all placeholders (`[DESCRIPTION]`, `[SPEC_OR_PLAN]`, `[BASE_SHA]`, `[HEAD_SHA]`, `[TEST_GUIDE]`).

**Fallback (single-agent environment without subagents):**
If subagent dispatch is unavailable in the current environment, explicitly switch roles, read `code-reviewer.md`, inspect the actual `git diff [BASE_SHA]..[HEAD_SHA]` and surrounding files (never rely on memory), and produce the exact review report format before making any edits.

---

## Step 3: Act on Feedback

Handle returned findings strictly by severity:

| Severity | Required Action |
|----------|-----------------|
| **Critical** | Must fix immediately. Do not proceed or merge. |
| **Important** | Fix before moving to the next task or merging. |
| **Nit / Optional** | Fix if trivial, or skip — never block progress on personal preference. |
| **Declined to Judge** | Review each line and confirm with your human partner if any item should become a follow-up task. |

**If you disagree with a finding:**
- Do **not** blindly apply a bad suggestion, and do **not** dismiss valid feedback.
- Push back with concrete technical evidence (spec citation, benchmark, or passing test) and explain the tradeoff.

**After fixing Critical or Important issues:**
- Re-run the test suite to verify everything stays green.
- Re-dispatch the reviewer on the updated range if the fixes were non-trivial.

---

## Common Rationalizations (Stop and Reject These)

| Excuse | Reality |
|--------|---------|
| "The change is small, I'll skip review" | Small diffs hide subtle boundary bugs and spec mismatches. Small diffs are also the fastest to review. |
| "I'll just eyeball my own diff inline" | Reviewing in the same session suffers from confirmation bias and burns the context window you need to keep building. |
| "Let me paste our whole chat so the reviewer understands" | Handing over your thought process biases the reviewer. Give them only the diff and the spec/plan so they judge the actual code. |
