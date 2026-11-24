---
name: sync-docs
description: "Pre-PR doc-drift gate: compare the current branch diff against active specs, ADRs, and PROJECT.md (respecting .paddlr.json) so documentation never drifts from code."
disable-model-invocation: true
---

# Sync Docs

Verify that code changes in the current branch have not drifted from project memory (`specs/`, `decisions/`, `DECISIONS.md`, `PROJECT.md`).

## 1. Resolve Project Memory Paths

1. Check for `.paddlr.json` at the repository root.
2. Resolve `specs`, `decisions`, `decisionsIndex`, and `project` (defaulting under `docs/paddlr/`).

## 2. Inspect the Branch Diff

1. Compute the diff from the repository's default base branch (`git diff <base>...HEAD` plus any staged/unstaged working-tree edits).
2. Identify user-visible or structural changes:
   - Public APIs, CLI flags, config schemas, or file layouts
   - Architectural boundaries, data models, or dependencies
   - Behavioral changes tied to an active spec in `specs/`

## 3. Check for Drift

1. **Active Specs (`specs/`):** If the branch implements or modifies a specified feature, compare the diff against the spec's Requirements, UX/Behavior, and Confirmed Technical Decisions. Update the spec if an agreed behavior changed during implementation.
2. **Architectural Decisions (`decisions/` & `DECISIONS.md`):** If the diff contradicts an `Accepted` ADR, do **not** edit the old ADR's rationale. Invoke **writing-decisions** to author a superseding ADR.
3. **Living Project Snapshot (`PROJECT.md`):** If `PROJECT.md` exists and the diff changes tech stack, directory layout, or core commands, update it concisely.
4. **Empty State Handling:** If this is a Level 1 change or the repository has no affected specs/ADRs, report `No active specs or ADRs affected` and exit cleanly without creating placeholder docs.

## 4. Output

Report in 3–5 concise lines:
- Diff scope inspected (base branch and file count)
- Specs/ADRs/PROJECT.md checked
- Drift found and fixed (or `None — docs aligned with diff`)
