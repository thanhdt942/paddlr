# AGENTS.md — Instructions for AI Coding Agents

> **Framework:** Paddlr  
> **Tagline:** Simple on the Surface. Sophisticated Underneath.  
> **Source of Truth:** [AGENTS.md](AGENTS.md) (Core Operating Principles & Guardrails)

This document provides binding instructions for any AI coding agent operating within this repository or utilizing the Paddlr framework.

---

## 1. Core Operating Principles

Whenever executing development tasks, adhere to the following principles:

1. **Understand Before Modifying:** Never edit code before discovering repository structure, technology stack, conventions, and development commands.
2. **Clarify Before Assuming:** Disclose ambiguities in requirements or constraints early. Do not silently resolve major architectural ambiguities.
3. **Proportional Overhead:** Match engineering effort, design depth, and documentation to task risk.
   - For simple fixes (Level 1), keep the process lightweight.
   - For multi-component features (Level 2), produce actionable plans and incremental slices.
   - For high-impact architectural changes (Level 3), evaluate alternatives, operational risks, and seek explicit approval.
4. **Implement Incrementally:** Divide work into small, self-contained, verifiable slices. Never make massive unverified changes.
5. **Verify with Concrete Evidence:** Distinguish between what was inspected, changed, executed, verified, and what remains untested. Never report success without running verification.
6. **Preserve User Changes & State:** Never overwrite existing documentation, delete user files, or perform destructive Git operations without authorization.
7. **Keep Documentation Minimal & Meaningful:** Never generate empty placeholder files or duplicate information across multiple documents.

---

## 2. Standard Engineering Workflow Loop

For every task, execute the standard engineering cycle:

```text
Understand ──► Analyze & Plan ──► Incremental Implement ──► Evidence Verify ──► Finalize
```

### Step 1 — Inspect & Understand
- Inspect current Git state, untracked files, and recent commit history.
- Locate existing documentation, testing scripts, and coding style rules.
- Discover dependencies and runtime environment commands.
- Distinguish verified facts from inferred assumptions.

### Step 2 — Analyze & Plan
- Classify task complexity:
  - **Level 1 (Small Change):** Typo fixes, minor refactoring, localized bugs. No formal plan or spec required.
  - **Level 2 (Feature Development):** Requirements clarification, acceptance criteria, technical design (if needed), task decomposition into verifiable slices.
  - **Level 3 (Architectural Change):** Deep investigation, trade-off analysis, security/rollback assessment, approval gate before implementation.
- For Level 2 & 3: Author the Feature Specification directly in `docs/paddlr/specs/[YYYY-MM-DD-feature].md` and a brand-new Implementation Plan in `docs/paddlr/plans/[YYYY-MM-DD-feature].md` (or the configured project memory root). Always create a fresh, dedicated plan file for every new request; never overwrite or append to past plans. Structure plans into bite-sized, contract-first tasks (`Consumes`/`Produces`) with checkbox steps (`- [ ]`). Never store plans solely in ephemeral IDE chat artifacts or temporary scratchpads. Present the plan from these persistent files and get explicit user approval before high-impact changes.

### Step 3 — Incremental Implementation
- Execute one slice at a time.
- Follow existing codebase patterns and naming conventions.
- When applicable, use test-driven cycles (RED → GREEN → REFACTOR).
- Stop immediately when unexpected errors arise; do not cascade breaking edits.

### Step 4 — Evidence-Based Verification
- Choose verification dimensions appropriate to task risk (lint, type-check, unit tests, integration tests, runtime execution).
- Report status explicitly using standard statuses:
  - `PASS`: Verification executed successfully with captured evidence.
  - `FAIL`: Verification executed and failed (investigate root cause before fixing).
  - `BLOCKED`: Verification blocked by environmental or external factors.
  - `NOT RUN`: Verification skipped or deferred.
  - `NOT APPLICABLE`: Dimension does not apply to this change.
- A passing build or type check does not alone prove behavioral correctness.

### Step 5 — Finalize & Record
- Update persistent project context (`project-context/` or authoritative docs) if architecture or decisions changed.
- Prepare a concise summary: files created, files modified, verification evidence, remaining questions, and next steps.

---

## 3. Git and Execution Safety Guardrails

### Forbidden Actions
- **No Destructive Git:** Never run `git reset --hard`, `git clean -fd`, `git push --force`, or rewrite history unless explicitly requested by the user.
- **No Unapproved Commits:** Do not run `git commit` or `git push` without explicit authorization.
- **No Secret Exposure:** Never display, log, or store secrets, tokens, or environment credentials in repository documentation.
- **No Untrusted Command Execution:** Evaluate every command before executing. Prefer read-only inspection commands.
- **No Fictional Verification:** Never claim a test passed or an environment check succeeded without actual command output.

---

## 4. Documentation & Project Context Rules

1. **One Authoritative Location:** Every piece of project knowledge belongs in one authoritative document.
2. **Roadmap vs. Progress:** Long-term goals belong in `PLAN.md` or `ROADMAP.md`. Current status belongs in `PROGRESS.md`. Do not mix them.
3. **Decisions are Immutable & Granular:** Accepted architectural decisions are recorded individually in `docs/paddlr/decisions/XXXX-<slug>.md` and indexed in `docs/paddlr/DECISIONS.md`. They are never rewritten. If a decision changes, create a new decision that supersedes the prior one (`Superseded by ADR-XXXX`).
4. **Session Handoffs:** Handoff notes must be concise, highlighting current objective, completed work, verified state, blockers, and exact next steps.
5. **Persistent Specifications & Plans (Always New Plan per Request):** Every Level 2 feature and Level 3 architectural change MUST persist its specification in `docs/paddlr/specs/` and its implementation plan in a fresh, dedicated file in `docs/paddlr/plans/[YYYY-MM-DD-feature].md`. Always create a new plan file for each new request or feature initiative; never overwrite or merge with existing past plans. IDE artifacts (`<appDataDir>/brain/`, temporary scratchpads) are strictly ephemeral mirrors for rendering; the authoritative, Git-tracked source of truth must reside in `docs/paddlr/`.
