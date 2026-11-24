# Task State Schema Specification

**Status:** Normative Schema Specification  
**Framework:** Paddlr — Agent-Agnostic Software Engineering  
**Authority:** [docs/paddlr/plans/2026-11-23-paddlr-mode-evolution.md](../../../docs/paddlr/plans/2026-11-23-paddlr-mode-evolution.md)  
**Location:** `skills/paddlr-mode/references/task-state-schema.md`

---

## 1. Overview

Paddlr requires an explicit, durable, and human-auditable model of task state. The canonical Task State resides in a single Git-tracked Markdown plan file:

```text
docs/paddlr/plans/YYYY-MM-DD-<slug>.md
```

### Optional Path Overrides (`.paddlr.json`)
Target repositories may place an optional `.paddlr.json` file at the repository root to override default project memory paths (`root`, `specs`, `plans`, `decisions`, `decisionsIndex`, `project`). Unspecified keys inherit from `root` (default `docs/paddlr`). All paths must be relative and remain inside the repository root; malformed JSON or escaping paths fail fast with an error.

This document specifies the YAML frontmatter schema, body section requirements, and lifecycle rules governing canonical Task State.

---

## 2. Canonical State vs. Operational Logs

1. **Single Canonical Store:**
   The Markdown plan file in `docs/paddlr/plans/` is the **only canonical Task State**. All phase transitions, task completions, and verification evidence must be recorded here.
2. **Ephemeral Scratchpads:**
   Local files such as `decision.tsv` in `hillclimb.md` are strictly ephemeral trial logs for raw numerical metric iterations during optimization sweeps. They are not canonical state stores. Canonical summaries and decisions are committed to the task plan.
3. **Trivial Task Exemption:**
   Small Level 1 changes (typos, single-file localized fixes) execute in-turn without creating a plan file unless escalated or requested.
4. **Boundary with Project Memory:**
   - Task State is initiative-scoped and ephemeral to task completion.
   - Project Memory (`docs/paddlr/PROJECT.md` and `docs/paddlr/DECISIONS.md`) is durable across tasks. `PROJECT.md` is the living current snapshot; `DECISIONS.md` records architectural decisions and their historical evolution.
5. **Two-Tier Checklist Synchronization (`ui.todo`):**
   - The Markdown plan file (`docs/paddlr/plans/YYYY-MM-DD-<slug>.md` or `.paddlr.json` override) is always the **canonical source of truth**.
   - When executing a Level 2/3 plan or a Level 1 playbook, mirror active steps into the host runtime's live checklist via the optional `ui.todo` primitive (`runtime-adapters.md`).
   - Mark `- [x]` in the canonical plan and `done` in `ui.todo` **only after** concrete verification succeeds. If `ui.todo` is unavailable, emit a compact progress list in chat replies at phase boundaries.

---

## 3. Frontmatter Schema Specification

Every persistent task plan must begin with a YAML frontmatter block adhering to the following schema:

```yaml
---
task_id: "pdl-YYYY-MM-DD-NN"
title: "Human-Readable Title of the Initiative"
classification: 2                 # 1 = Small Change, 2 = Feature Development, 3 = Architectural Change
status: "in_progress"             # pending | in_progress | paused | blocked | completed | failed | cancelled
playbook: "feature"               # Selected playbook archetype (e.g. feature, bug-fix, multi-phase-plan)
active_phase: "phase_1"           # Current phase or workflow step identifier
done_predicate: "Empirically verifiable condition defining successful completion"
created_at: "2026-11-23T14:53:41+07:00"
updated_at: "2026-11-23T15:30:00+07:00"
---
```

*(Note: Delegation tracking metadata such as `assigned_workers` is omitted from the initial Single-Agent baseline schema to eliminate speculative bloat; it will be introduced in Phase 4 when local subagent delegation is implemented).*

### Field Definitions

| Field | Type | Required | Description |
|---|---|---|---|
| `task_id` | String | Yes | Unique identifier formatted as `pdl-YYYY-MM-DD-NN`. |
| `title` | String | Yes | Concise imperative title of the initiative. |
| `classification` | Integer | Yes | Task complexity level: `1` (Small), `2` (Feature), `3` (Architecture). |
| `status` | Enum | Yes | `pending`, `in_progress`, `paused`, `blocked`, `completed`, `failed`, `cancelled`. |
| `playbook` | String | Yes | Name of the active playbook in `skills/paddlr-mode/playbooks/`. |
| `active_phase` | String | Yes | Identifier of the current workflow phase or step. |
| `done_predicate` | String | Yes | Falsifiable, empirical predicate defining completion. |
| `created_at` | ISO-8601 | Yes | Timestamp of task initiation. |
| `updated_at` | ISO-8601 | Yes | Timestamp of most recent state update. |

---

## 4. Markdown Body Section Structure

The body of the canonical task plan follows a contract-first task decomposition:

```markdown
# Implementation Plan: [Title]

- **Date:** YYYY-MM-DD
- **Specification:** [Link to spec in docs/paddlr/specs/ or N/A]
- **Status:** [Matching status from frontmatter]

---

## 1. Objective & Scope
Concise statement of the user's goal, the technical approach, and boundaries.

---

## 2. Tasks

### Task 1: [Task Title]
- **Consumes:** [Input files, specs, or preceding task outputs]
- **Produces:** [Output files, patches, or artifacts]
- [ ] Step 1.1: Concrete verifiable action.
- [ ] Step 1.2: Concrete verifiable action.

### Task 2: [Task Title]
- **Consumes:** ...
- **Produces:** ...
- [ ] Step 2.1: ...

---

## 3. Verification & Evidence
Command outputs, test results, and evidence logs proving completion.

---

## 4. Decisions & Trade-offs
Decisions made during execution, trade-offs evaluated, and rejected alternatives.
```

---

## 5. State Transition and Update Rules

1. **Atomic Phase Updates:** The Main Agent updates `active_phase`, `status`, and `updated_at` whenever advancing past a playbook phase boundary.
2. **Checkbox Invariant:** Step checkboxes `- [ ]` are marked `- [x]` only after concrete command verification confirms the step succeeded.
3. **Durable Recoverable Work:** On pause, working state is safely preserved, and the resume note in the plan specifies the current state and next action. Baseline verification is executed before resuming.
4. **Terminal Immutability:** Terminal tasks (`completed`, `failed`, `cancelled`) cannot be reopened. New requirements or fix attempts require authoring a fresh task plan.
