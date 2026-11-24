# Paddlr Core Contracts Reference Guide

**Status:** Normative Core Specification  
**Framework:** Paddlr — Agent-Agnostic Software Engineering  
**Authority:** [docs/paddlr/plans/2026-11-23-paddlr-mode-evolution.md](../../../docs/paddlr/plans/2026-11-23-paddlr-mode-evolution.md)  
**Location:** `skills/paddlr-mode/references/core-contracts.md`

---

## 1. Overview

Paddlr establishes a runtime-independent orchestration core. The core defines engineering behavior, task lifecycles, and execution contracts that remain consistent across diverse AI coding agents (Claude Code, Cursor, Antigravity, OpenCode, Codex).

This document establishes the 8 foundational execution contracts that govern all Paddlr Mode playbooks, companion skills, and agent interactions.

---

## Contract 1: Intent Contract (AR-03)

Governs how Paddlr understands and validates incoming user requests before executing actions.

### 1. Separation of Intent Resolution from Action Authorization
Paddlr strictly separates two distinct engineering questions:
1. **Intent Resolution (Contract 1):** Does the agent understand the user's goal, problem, and done predicate with sufficient clarity to continue to planning and playbook selection?
2. **Action Authorization (Contract 6 - Autonomy Policy):** Is the agent authorized to execute a specific operational action (file edit, test execution, dependency change, branch modification)?

Passing the Intent Contract with a `PROCEED` verdict means the request is sufficiently understood to continue. **It does NOT grant unrestricted autonomous execution.** All subsequent operational actions remain strictly governed by the Autonomy Policy (Contract 6).

### 2. Intent Model

```typescript
interface TaskIntent {
  raw_request: string;
  user_goal: string;               // Concrete outcome the user desires
  root_problem: string;            // Underlying technical or functional problem
  constraints: string[];           // Stated boundaries (architectural, tech stack, backwards-compat)
  done_predicate: string;          // Falsifiable, empirical completion condition
  assumptions: string[];           // Inferred premises (strictly separated from confirmed facts)
  identified_ambiguities: string[]; // Unresolved questions requiring clarification
  resolution_verdict: "PROCEED" | "CLARIFY" | "STOP";
}
```

### 3. Resolution Verdicts

1. **`PROCEED` (Sufficiently Understood to Continue):**
   - The user's goal, root problem, and done predicate are understood with sufficient clarity to select a playbook and formulate a plan.
   - Any remaining unstated details are non-material (resolvable from codebase conventions).
   - *Verdict Effect:* Restate the goal and the smallest change that meets it in a single declarative sentence, select the matching playbook, and proceed to the next phase.
   - *Constraint:* `PROCEED` does *not* authorize unilateral code modification on non-trivial tasks; actions must obey the Autonomy Policy.

2. **`CLARIFY` (Material Ambiguity Requires User Input):**
   - A critical goal, requirement, or constraint contains material ambiguity that cannot be resolved from codebase inspection.
   - Multiple valid architectural choices exist that fundamentally alter data structures, public interfaces, or system boundaries.
   - *Verdict Effect:* Halt before drafting code or plans. Present at most 2–3 concrete, well-bounded alternatives with trade-offs. Proceed once the human selects an option.

3. **`STOP` (Execution Cannot Safely or Legitimately Continue):**
   - Execution cannot safely or legitimately continue because the request contradicts established repository invariants, violates safety guardrails, requests impossible/incoherent behavior, or would result in unrecoverable system damage.
   - *Verdict Effect:* Halt execution immediately. State the contradiction, safety rule, or impossibility condition, and do not proceed.

---

## Contract 2: Canonical Task State Contract (AR-04)

Governs the storage, lifecycle, and consistency of active engineering tasks.

### 1. Single Canonical State Principle
- The Git-tracked Markdown plan located at `docs/paddlr/plans/YYYY-MM-DD-<slug>.md` (or the `plans` path configured in an optional `.paddlr.json` at the repository root) is the **single canonical Task State**.
- Target repositories may customize `root`, `specs`, `plans`, `decisions`, `decisionsIndex`, or `project` via `.paddlr.json` (all relative paths contained within the repository root; unspecified keys inherit from `root`, default `docs/paddlr`).
- No secondary file, internal transcript log, or hidden database (e.g. `.paddlr/state.json`) may act as a parallel state store.
- **Operational Scratchpads:** Local files such as `decision.tsv` in `hillclimb.md` are strictly ephemeral trial logs for raw numerical metric iterations. They are not canonical state stores. Canonical summaries and decisions are committed to the task plan.
- **Trivial Task Exemption:** Small Level 1 tasks (typo fixes, localized one-file edits) execute in-turn without creating a plan file unless escalated or requested.

### 2. Distinction from Project Memory
- **Task State (`docs/paddlr/plans/`):** Ephemeral to the task lifecycle. Tracks active steps, execution checkboxes, and verification evidence.
- **Project Memory (`docs/paddlr/PROJECT.md` & `docs/paddlr/DECISIONS.md`):** Durable repository context, but not strictly immutable.
  - `PROJECT.md` represents the living current project snapshot (architecture, tech stack, conventions).
  - `DECISIONS.md` and `docs/paddlr/decisions/XXXX-<slug>.md` record architectural decisions and their historical evolution. Decisions are superseded rather than overwritten, preserving historical auditability.

---

## Contract 3: Task Lifecycle Contract (AR-05)

Defines the formal 7-state lifecycle machine governing task transitions.

```text
Active States:
  ┌──────────────┐      Classify & Select Playbook
  │   pending    ├──────────────────────────────────┐
  └──────────────┘                                  │
                                                    ▼
  ┌──────────────┐      Unblock / Re-plan    ┌──────────────┐      pause-safely (Checkpoint)
  │   blocked    ├──────────────────────────►│ in_progress  ├───────────────────────────────►┌──────────────┐
  └──────┬───────┘                           └──┬───▲───┬───┘                                │    paused    │
         │                                      │   │   │                                    └──────┬───────┘
         │ Unrecoverable                        │   │   │ session-pickup (Verify Baseline)          │
         ▼                                      │   │   └───────────────────────────────────────────┘
  ┌──────────────┐  Unrecoverable Failure       │   │
  │    failed    │◄─────────────────────────────┤   │ All Done Predicates PASS
  └──────────────┘                              │   ▼
                                                │ ┌──────────────┐
  ┌──────────────┐  Intentional Abandonment     │ │  completed   │
  │  cancelled   │◄─────────────────────────────┘ └──────────────┘
  └──────────────┘
```

### 1. State Definitions

#### Active States
- **`pending`:** Task plan initialized; classification complete; work has not yet started.
- **`in_progress`:** Actively executing a playbook. The active workflow phase is recorded in plan metadata. Baseline verification during session pickup is an operation performed within this state.
- **`paused`:** Execution voluntarily halted at an atomic boundary. Durable work is preserved; resume note identifies current state and next action.
- **`blocked`:** Execution involuntarily stopped due to an external impediment, missing prerequisite, environment failure, or contradictory requirement. Requires intervention.

#### Terminal States
- **`completed`:** Done predicate empirically satisfied. Evidence captured in task plan.
- **`failed`:** Task cannot be completed because execution encountered an unrecoverable failure within the permitted scope (e.g. proof of impossible requirement, persistent external blocker).
- **`cancelled`:** An authorized human actor intentionally abandons or supersedes the task.

### 2. Complete State Transition Matrix

| Current State | Allowed Next States | Trigger Event & Invariant Gate |
|---|---|---|
| `pending` | `in_progress` | Kickoff authorized; execution begins. |
| `pending` | `cancelled` | Human directive to abandon task before execution starts. |
| `in_progress` | `paused` | Voluntary stop via `pause-safely` on clean boundary; durable work preserved. |
| `in_progress` | `blocked` | Involuntary impediment hit (missing dependency, environmental issue). |
| `in_progress` | `completed` | Falsifiable done predicate passes with captured empirical evidence. |
| `in_progress` | `failed` | Unrecoverable failure or contradiction proven within task scope. |
| `in_progress` | `cancelled` | Human directive to abandon task during execution. |
| `paused` | `in_progress` | Resumed via `session-pickup` after baseline re-verification passes. |
| `paused` | `cancelled` | Human directive to abandon task while paused. |
| `blocked` | `in_progress` | Prerequisite satisfied or task replanned with human guidance. |
| `blocked` | `failed` | Blocker determined to be permanently unresolvable. |
| `blocked` | `cancelled` | Human directive to abandon blocked task. |
| `completed` | *None (Terminal)* | Immutable. New requirements require a fresh task plan. |
| `failed` | *None (Terminal)* | Immutable. Re-attempting work requires a new task plan referencing the failure. |
| `cancelled` | *None (Terminal)* | Immutable. Re-attempting work requires a new task plan. |

### 3. Terminal State Reopening Rule
Terminal states (`completed`, `failed`, `cancelled`) are **immutable**. Reopening terminal tasks is forbidden. If new work, bug fixes, or retries are needed, author a fresh task plan in `docs/paddlr/plans/` that links back to the prior plan's findings.

---

## Contract 4: Delegation & Concurrency Contract (AR-07)

Governs delegating work to subagents and integrating concurrent worker results.

### 1. Skill Invocation vs. Agent Delegation
Paddlr establishes strict terminology to distinguish between execution models:
- **Invoke a Skill:** The Main Agent applies a specialized capability, checklist, or engineering standard within its own active execution context (in-thread). No second agent is launched.
- **Delegate to a Worker:** The Main Agent assigns an explicit slice of work to another Agent (subagent, background worker, or isolated process) with an explicit brief, scope boundaries, and return deliverables.

**Single-Agent Invariant:** Phase 3 workflows and playbooks may **invoke Skills** within the single-agent execution thread, but must **not implement or activate Worker delegation**. Worker delegation remains deferred to Phase 4.

### 2. Delegation Brief Model (Phase 4+)

```typescript
interface DelegationBrief {
  worker_id: string;
  role: string;                   // e.g., "Refactoring Specialist", "Security Auditor"
  model_profile?: "deep-reasoning" | "standard-code" | "fast-mechanical"; // OPTIONAL
  goal: string;                   // Concise statement of objective
  scope_boundaries: string[];     // Explicit paths allowed to inspect or modify
  readonly: boolean;              // Restrict to read-only tools
  context_references: string[];   // Paths to relevant files (no inlined context dumps)
  deliverables: string[];         // Expected patch or report files
  verification_command: string;   // Command worker must execute to verify its slice
  failure_protocol: string;       // Action on failure (revert and report vs retry)
}
```

### 3. Canonical State Ownership & Concurrency Rules
1. **Main Agent Ownership:** The **Main Agent exclusively owns, updates, and writes canonical Task State** in `docs/paddlr/plans/`.
2. **No Direct Writes:** Subagents/workers must *never* edit the canonical plan file and must *never* merge branches directly into the main trunk.
3. **Bounded Return:** Workers return bounded deliverables (patch/diff files or text summaries), execution status (`PASS`/`FAIL`), and command output evidence.
4. **Concurrency Isolation:**
   - Concurrent workers operate in separate Git worktrees, isolated workspaces, or dedicated scratch directories (`principle-separate-before-serializing-shared-state`).
   - The Main Agent drains worker results **sequentially**, inspects diffs, runs verification on the integrated artifact, merges the patch into the working tree, and updates the canonical Task State.
5. **Initial Single-Agent Baseline:** In Single-Agent mode (Phases 1–3), delegation metadata (`assigned_workers`) is omitted from the plan frontmatter to avoid speculative schema bloat. Delegation tracking is introduced in Phase 4.

---

## Contract 5: Runtime Adapter Contract (AR-08)

Isolates core engineering behavior from runtime-specific tooling using semantic capability primitives.

### 1. Semantic Capability Primitives Matrix

Core v1 establishes a strict Single-Agent baseline. `agent.delegate` and `scheduler.loop` are kept out of the required Core v1 runtime capability set. A Single-Agent runtime does not need to implement them; an environment providing only the 5 mandatory primitives (`fs.read`, `fs.write`, `fs.patch`, `shell.exec`, `search.find`) is 100% fully compliant with Paddlr Core v1.

| Semantic Primitive | Capability Category | Core v1 Requirement | Description | Runtime Mappings (Claude Code / Antigravity / Cursor / OpenCode) | Fallback Strategy if Unsupported |
|---|---|---|---|---|---|
| `fs.read` | Filesystem | **Required (Mandatory)** | Read file contents by path. | `View`, `read_file`, Composer file read | Mandatory. No fallback. |
| `fs.write` | Filesystem | **Required (Mandatory)** | Create or overwrite whole file. | `Edit` (new), `write_file`, File write | Mandatory. No fallback. |
| `fs.patch` | Filesystem | **Required (Mandatory)** | Apply contiguous replacement. | `Edit`, `edit_file`, Composer edit | Mandatory. Fall back to `fs.write`. |
| `shell.exec` | Shell | **Required (Mandatory)** | Execute command in workspace. | `Bash`, `run_command`, Terminal command | Mandatory. No fallback. |
| `search.find` | Discovery | **Required (Mandatory)** | Find paths and search regex. | `GlobTool`/`GrepTool`, `glob`/`grep`, find | Fall back to `shell.exec` (`git ls-files`, `findstr`). |
| `model.steer` | Reasoning Tier | **Optional Enhancement** | Select model reasoning tier. | Model flags, `Model: "..."`, pstack | Fall back to runtime's default active model. |
| `ui.prompt` | User Interface | **Optional Enhancement** | Multiple-choice interactive prompt. | `AskQuestion`, `ask_question`, UI prompt | Fall back to plain-text turn prompt. |
| `ui.todo` | User Interface | **Optional Enhancement** | Live session checklist mirror. | Cursor/Claude Code `TodoWrite`, Antigravity `update_steps`, Codex CLI `update_plan`, OpenCode `todowrite` | Fall back to a compact progress list in chat replies at phase boundaries. |
| `agent.delegate`| Multi-Agent | **Deferred (Phase 4)** | Spawn isolated worker agent. | `Task`, `invoke_subagent`, subagent | Not required for Core v1. Single-agent runtimes do not implement. |
| `scheduler.loop`| Automation | **Deferred (Phase 6)** | Automated background loops. | `/loop`, `schedule`, cron | Not required for Core v1. Single-agent runtimes do not implement. |

---

## Contract 6: Autonomy Policy (AR-09)

Applies **Reversibility-First Autonomy**, separating decision-making autonomy from operational authorization:

- **Level 1 (Small Bug / Localized Refactor — Execute Directly):**
  - No Spec or Plan required. Execute the matching playbook directly, verify on the real surface, and report evidence.
- **Level 2 (Standard Feature, Reversible on Branch/Worktree — Proceed Without Blocking):**
  - Author Spec + Plan in project memory (`docs/paddlr/` or `.paddlr.json` overrides) and proceed directly through implementation, real-surface verification, and PR creation so the human reviews the complete result.
  - Pause only when product/UX ambiguity cannot be settled by code or prototyping, or when the user explicitly requests plan review first.
- **Level 3 (Architectural, Hard to Reverse, Schema/Public API Breaking, or Multi-PR — Mandatory Pre-Code Approval):**
  - Prototype or red-team unknowns if present, author Spec + ADR + Plan, and **pause for explicit human approval** before modifying production code.
- **Hard Stops (Always Pause — Never Execute Autonomously):**
  - Force-pushing to shared Git branches (`git push --force`).
  - Deleting persistent data, production databases, or cloud resources.
  - Triggering production deployments or publishing packages.
  - Sending messages to external systems or external human channels.
- **Session Overrides:**
  - Explicit user directives ("don't stop", "run until done") allow continuing reversible branch work while recording decisions in Plan/ADR. Hard stops remain enforced unless explicitly authorized.

---

## Contract 7: Evidence Contract (AR-10)

Defines what constitutes acceptable verification evidence.

### 1. Verification Dimensions
- `PASS`: Verbatim terminal output showing exit code 0 and passing test counts.
- `FAIL`: Verbatim terminal output showing stack trace, assertion failure, or exit code != 0.
- `BLOCKED`: Verbatim output showing environment or external blocker.
- `NOT RUN`: Explicitly documented deferred verification.
- `NOT APPLICABLE`: Explicitly justified exemption.

### 2. Forbidden Proxies
- Never accept: "It compiles", file modification timestamps, agent self-reports ("I verified..."), or cached test runs without live execution proof.
- Verification must link to the current Git commit SHA (`git rev-parse HEAD`).

---

## Contract 8: Recovery & Checkpoint Protocol (AR-11)

Governs session resumption, crash recovery, and idempotent execution.

### 1. Durable Recoverable Work Invariant
On pause or interruption, the system guarantees:
- **No work is lost:** Working state is safely preserved.
- **Durable resume note:** The task plan in `docs/paddlr/plans/` records current status (`paused`), the last green verified step, and the next required action.
- **Flexible preservation mechanism:** A `wip:` Git commit on the active branch is one supported mechanism; saving dirty edits to an isolated stash, branch, or patch file is also permitted. The invariant is durable recoverability, not a mandatory commit.
- **Baseline re-verification:** Before execution resumes, `session-pickup.md` verifies the last known good baseline against the real artifact.

### 2. In-Turn Retries vs. Deferred Loops
- **Bounded In-Turn Retries (Core):** Retrying a command 1–2 times within an active turn to isolate a transient flake, environmental jitter, or syntax error is permitted core behavior.
- **Autonomous Unattended Loops (Deferred):** Multi-hour autonomous background scheduling without human turn oversight is deferred to Phase 6.
