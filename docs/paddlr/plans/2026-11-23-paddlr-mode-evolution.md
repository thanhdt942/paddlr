# Implementation Plan: Paddlr Mode Evolution

- **Date:** 2026-11-23
- **Specification:** [docs/paddlr/specs/2026-11-23-paddlr-mode-evolution.md](../specs/2026-11-23-paddlr-mode-evolution.md)
- **Status:** Approved Architecture & Phased Roadmap (Ready for Implementation Phase 1)
- **Type:** Architecture Design, Migration Mapping, and Phased Development Roadmap

---

## Executive Summary

This document presents the complete architectural investigation, target design, migration mapping, and phased development roadmap for evolving the inherited **Poteto Mode** into **Paddlr Mode** (`skills/paddlr-mode/`), the primary orchestration entrypoint for Paddlr.

Paddlr is an **Agent-Agnostic Software Engineering Framework** whose guiding philosophy is *"Simple on the Surface. Sophisticated Underneath."* Paddlr preserves Poteto's battle-tested operational discipline, empirical verification rigor, 24 engineering principles, and playbook methodology, while eliminating Cursor-specific vendor lock-in, hardcoded model identifiers, and fragmented task state.

All five core architectural decision gates have been reviewed and approved by the project owner:
1. **Decision 1 (Task State Persistence):** APPROVED Option A. Single Git-tracked Markdown file per persistent task with structured YAML frontmatter under `docs/paddlr/plans/`. Trivial tasks are not persisted to files. Task State is strictly distinguished from long-lived Project Memory.
2. **Decision 2 (Playbook vs. Native Skill):** APPROVED Option A. Playbooks orchestrate workflows; independent Skills provide specialized capabilities without duplicating logic. Strict directory conventions are preserved.
3. **Decision 3 (Subagent & Swarm Phasing):** APPROVED Option A. Strict sequencing: Single-agent execution first (invoking Skills in-thread without worker delegation), then local subagent delegation (Phase 4), deferring cloud swarms and complex stack automation (Phase 6).
4. **Decision 4 (Looping & Polling):** MODIFIED Recommendation. Unattended execution and looping are deferred beyond the initial Paddlr Core without introducing external background daemons.
5. **Decision 5 (Missing External References):** APPROVED Option A. Verified against all 25 repository occurrences (14 in Phase 3 scope, 11 in later phases); missing external references (`unslop`, `technical-writing`, `no-comments`, `show-me-your-work`, `ketchup`, `control-ui`, `control-cli`) are retired in favor of native Paddlr standards and canonical plan tracking without creating stub skills.

---

## Table of Contents

1. [D-01: Repository Inventory & Audit](#d-01-repository-inventory--audit)
2. [D-02: Architecture Assessment](#d-02-architecture-assessment)
3. [D-03: Paddlr Architecture Specification](#d-03-paddlr-architecture-specification)
4. [D-04: Core Contracts Specification](#d-04-core-contracts-specification)
5. [D-05: Component Migration Mapping](#d-05-component-migration-mapping)
6. [D-06: Phased Development Roadmap](#d-06-phased-development-roadmap)
7. [D-07: Evaluation & Verification Plan](#d-07-evaluation--verification-plan)
8. [D-08: Resolved Architectural Decision Gates](#d-08-resolved-architectural-decision-gates)

---

## D-01: Repository Inventory & Audit

A comprehensive inventory of all 48 skills, 22 playbooks, supporting tools, plugins, and test suites in `c:\Users\User01\thanh-duongt\paddlr` was conducted.

### 1. Repository Component Census

| Component Category | Count | Directory Location | Conformance & Status |
|---|---|---|---|
| **Native Paddlr Core Skills** | 8 | `skills/<name>/SKILL.md` | 8/8 Valid; Fully conforms to Agent Skills spec; Python unit tests pass (52/52). |
| **Principle Skills** | 24 | `skills/principle-*/SKILL.md` | 24/24 Valid; Validated by `scripts/validate_skills.py`. Zero runtime coupling. |
| **Poteto Auxiliary Skills** | 15 | `skills/<name>/SKILL.md` | 15/15 Valid. Varying degrees of Cursor model/subagent coupling. |
| **Paddlr Mode Orchestrator** | 1 | `skills/paddlr-mode/` | **FAIL** in `validate_skills.py` due to frontmatter name mismatch (`name: poteto-mode` in directory `paddlr-mode`). |
| **Playbooks** | 22 | `skills/paddlr-mode/playbooks/*.md` | Operational workflows. Heavy coupling to Cursor `/loop`, cloud agents, and `pstack-models`. |
| **Supporting Tools & References** | 5 | `skills/paddlr-mode/{references,scripts}/` | `bugbot-triage.md` (clean); `watch-pr/` (high quality TypeScript/Bun); `bootstrap.ts`; `worktree-audit.sh` (Bash/POSIX). |
| **Runtime Plugin Integrations** | 4 | `.claude-plugin/`, `.codex-plugin/`, `.opencode/`, `.agents/` | Metadata configurations for Claude Code, OpenAI Codex, OpenCode, and Antigravity. |
| **Project Memory Root** | 1 | `docs/paddlr/` | Standard persistent store containing `specs/`, `plans/`, and architectural decisions. |

### 2. Immediate Structural Defect Identified
Running `python scripts/validate_skills.py` produces an immediate failure:
```text
[FAIL] paddlr-mode: Frontmatter name 'poteto-mode' does not match directory name 'paddlr-mode'.
```
When Poteto Mode was initially copied into `skills/paddlr-mode/`, the directory was renamed but its YAML frontmatter `name:` field was left as `poteto-mode`. Correcting this is established as Task 1 in Phase 1 of the roadmap.

---

## D-02: Architecture Assessment

### 1. Strengths of Inherited Poteto Mode Worth Preserving
- **Empirical Verification Rigor:** Poteto rejects self-reports, file modification timestamps, and "it compiles" proxies. It mandates concrete execution proofs: live surface verification (`principle-prove-it-works`), repro-first failing test commits (`sequence-verifiable-units`), automated pixel diffs (`visual-parity.md`), and SQLite trace queries (`trace-forensics.md`).
- **Defensive Engineering Invariants:** Clear separation between reversible operations (autonomous execution) and irreversible writes (mandatory pause for deploys, force-pushes, data deletion).
- **Domain Modeling Primacy:** Strong bias toward modeling state machines, typed schemas, and discriminated unions before writing branching business logic (`principle-model-the-domain`, `principle-foundational-thinking`).
- **Clean Subagent Boundaries:** Explicit worker kickoff rules (`worker.md`) enforcing that subagents work for the human operator, do not ask interactive questions on reversible choices, and package PRs cleanly.

### 2. Architectural Limitations & Coupling in Inherited Implementation
- **Cursor Vendor Lock-In:** Multiple playbooks depend on Cursor-exclusive primitives:
  - Wake loop commands: Cursor's `/loop` command (`autonomous-run.md`, `autopilot-full.md`, `autopilot-stack.md`, `shipping.md`, `visual-parity.md`).
  - Cloud infrastructure: Cursor cloud subagents, `environment: "cloud"`, `cloud_base_branch`.
  - Transcript disk layout: Scanning `~/.cursor/projects/<slug>/agent-transcripts/*.jsonl` (`recall`, `eval`, `session-pickup`, `worktree-audit.sh`).
  - Proprietary plugins: Hardcoded invocations of `cursor-team-kit` (`/deslop`, `control-ui`, `control-cli`).
- **Hardcoded Model Slugs:** System prompts and playbooks hardcode specific proprietary models (`claude-opus-5-5-xhigh-fast`, `claude-fable-5-2-high`, `gemini-4-neon-xhigh`). This breaks portability when running on other models (e.g., Gemini, Claude Sonnet, GPT-4o, local models).
- **Fragmented, Ephemeral State:** Task state is split between in-memory conversation history, the runtime `todolist` tool, ad-hoc files (`decision.tsv`, `/tmp/<slug>-resume.md`), and IDE transcripts.
- **Missing External Skill References:** Poteto instructions cite 7 helper skills not present in the repository (`unslop`, `technical-writing`, `no-comments`, `show-me-your-work`, `ketchup`, `control-ui`, `control-cli`).
- **Duplication with Native Paddlr Skills:** Poteto playbooks duplicate capabilities already implemented cleanly in native Paddlr skills (`feature.md` vs `feature-development`, `bug-fix.md` vs `sre-debugging`, `authoring-a-skill.md` vs `skill-creator`, `multi-phase-plan.md` vs `writing-plans`).

---

## D-03: Paddlr Architecture Specification

### 1. Identity & Positioning Statement
> **Paddlr** is an agent-agnostic software engineering framework that turns proven engineering disciplines into practical, reusable Agent Skills, structured operational workflows, and persistent project memory.  
> **Tagline:** Simple on the Surface. Sophisticated Underneath.  
> **Core Mission:** Provide a consistent, high-rigor engineering methodology across diverse AI coding agents (Claude Code, Cursor, Antigravity, OpenCode, Codex) without binding orchestration logic to any single vendor's runtime.

### 2. Architectural Responsibilities and Directory Boundaries

```text
┌────────────────────────────────────────────────────────────────────────┐
│                              USER / OPERATOR                           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ /paddlr-mode, natural request
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                PADDLR MODE (skills/paddlr-mode/SKILL.md)               │
│  - Intent Intake & Classification (Level 1 / Level 2 / Level 3)        │
│  - Playbook Selection & Lifecycle State Management                     │
│  - Autonomy Policy Enforcement & Approval Gates                        │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │ Selects                        │ Selects
                    ▼                                ▼
┌───────────────────────────────────────┐  ┌─────────────────────────────┐
│    PLAYBOOKS (paddlr-mode/playbooks/) │  │     PRINCIPLES (skills/)    │
│  - Operational Workflow Execution     │  │  - 24 Standalone Razors     │
│  - Phase Transitions & Verifications  │  │  - Conditional Invocations  │
│  - Coordinates Companion Skills       │  │  - Non-Negotiable Triggers  │
└───────────────────┬───────────────────┘  └─────────────────────────────┘
                    │ Coordinates (Invokes Specialized Skills)
                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     COMPANION SKILLS (skills/*/)                       │
│  - sre-debugging (Scientific Root Cause Analysis)                      │
│  - test-driven-development (Red-Green-Refactor Cycles)                 │
│  - writing-specs & writing-plans (Specifications & Execution Plans)    │
│  - code-review (Read-Only Independent Diff Audits)                     │
│  - release-management & skill-creator                                  │
│  - architect, arena, blast-radius, benchmark-checklist, why            │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │ Reads / Writes                 │ Tool Invocations
                    ▼                                ▼
┌───────────────────────────────────────┐  ┌─────────────────────────────┐
│       PERSISTENT TASK STATE           │  │   RUNTIME ADAPTER CONTRACT  │
│  - docs/paddlr/plans/YYYY-MM-DD-*.md  │  │  - Capability Negotiation   │
│  (One file per persistent task;       │  │  - Optional Model Steering  │
│   Distinct from Project Memory)       │  │  - Graceful Degradation     │
└───────────────────────────────────────┘  └─────────────────────────────┘
```

#### Strict Directory Layout Rules (Preserved)
- `paddlr-mode/` is an independent Skill and the main orchestrator at `skills/paddlr-mode/`.
- Playbooks remain strictly inside `skills/paddlr-mode/playbooks/`.
- Independent Skills (both Companion Skills and Principle Skills) remain at the root `skills/` level alongside `paddlr-mode/`.
- **Forbidden:** Do not create `skills/paddlr-mode/skills/` or `skills/paddlr-mode/principles/`.
- **Separation of Concerns:** Playbooks orchestrate end-to-end procedural flows; they **invoke Companion Skills** for specialized domain capabilities within the execution context rather than duplicating instructions.

#### Distinction: Task State vs. Project Memory
- **Canonical Task State (`docs/paddlr/plans/YYYY-MM-DD-<slug>.md`):** The Git-tracked Markdown task plan is the *single canonical Task State*. Ephemeral to the initiative. Contains active task metadata, current phase, delegation status, execution checkboxes, and verification evidence. Created only for persistent tasks (Level 2 features, Level 3 architectural changes); trivial Level 1 tasks execute directly in-turn without creating a plan file. Any secondary operational logs (such as `decision.tsv` in `hillclimb.md`) must not become parallel state stores; they are strictly ephemeral, local scratch trial logs for empirical metric iterations.
- **Project Memory (`docs/paddlr/decisions/`, `docs/paddlr/DECISIONS.md`, `docs/paddlr/PROJECT.md`):** Durable repository knowledge, but not strictly immutable. It evolves deliberately: `docs/paddlr/PROJECT.md` represents the current living project snapshot (architecture, tech stack, conventions), while `docs/paddlr/DECISIONS.md` records architectural decisions and their historical evolution. Decisions are superseded (`Superseded by ADR-XXXX`) rather than silently overwritten, preserving the auditable rationale of how the system arrived at its current state.

---

## D-04: Core Contracts Specification

### Contract 1: Intent Contract (AR-03)
Governs how Paddlr processes user requests before taking action.

#### 1. Separation of Intent Resolution from Action Authorization
Paddlr strictly separates two distinct engineering questions:
1. **Intent Resolution (Contract 1):** Does the agent understand the user's goal, problem, and done predicate with sufficient clarity to continue to planning and playbook selection?
2. **Action Authorization (Contract 6 - Autonomy Policy):** Is the agent authorized to execute a specific operational action (file edit, test execution, dependency change, branch modification)?

Passing the Intent Contract with a `PROCEED` verdict means the request is sufficiently understood to continue. **It does NOT grant unrestricted autonomous execution.** All subsequent operational actions remain strictly governed by the Autonomy Policy (Contract 6).

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

#### 2. Resolution Verdicts
- **`PROCEED` (Sufficiently Understood to Continue):** The user's goal, root problem, and done predicate are understood with sufficient clarity to select a playbook and formulate a plan. Any remaining unstated details are non-material (resolvable from codebase conventions). Restate intent in one declarative sentence and proceed to the next phase. *`PROCEED` does not authorize unilateral code modifications on non-trivial tasks; actions must obey the Autonomy Policy.*
- **`CLARIFY` (Material Ambiguity Requires User Input):** Additional user input is needed to resolve material ambiguity that directly alters the architectural direction, interface contracts, or data shape. Present at most 2–3 concrete options with trade-offs.
- **`STOP` (Execution Cannot Safely or Legitimately Continue):** Execution cannot safely or legitimately continue because the request contradicts established repository invariants, violates safety guardrails, requests impossible/incoherent behavior, or would result in unrecoverable system damage. State the contradiction, safety rule, or impossibility condition and halt.

### Contract 2: Task State Model (AR-04)
Stored durably as Git-tracked Markdown files within `docs/paddlr/plans/YYYY-MM-DD-<slug>.md`.

**Rules:**
1. **Single Canonical Task State:** The Git-tracked Markdown task plan is the *single canonical Task State*. No secondary files or databases (including `decision.tsv`) may function as a parallel state store. `decision.tsv` in `hillclimb.md` is strictly an ephemeral numerical trial scratchpad for recording raw benchmark iterations before consolidating results into the plan.
2. **One file per persistent task** (Level 2 features, Level 3 architectural initiatives, multi-step refactorings).
3. **YAML Frontmatter:** Holds machine-parseable state machine fields.
4. **Markdown Body:** Holds human-readable context, technical choices, checkbox progress, and verification logs.
5. **No Trivial Bloat:** Small Level 1 changes (typos, single-file localized fixes) execute directly in-session without generating a plan file unless escalated or requested.

```markdown
---
task_id: "pdl-2026-11-23-01"
title: "Paddlr Mode Evolution"
classification: 3                 # Level 1 (Small), Level 2 (Feature), Level 3 (Arch)
status: "in_progress"             # pending | in_progress | paused | blocked | completed | failed | cancelled
playbook: "multi-phase-plan"
active_phase: "phase_1"
done_predicate: "All core contracts specified and validated via CI"
created_at: "2026-11-23T14:53:41+07:00"
updated_at: "2026-11-23T15:30:00+07:00"
---

# Task Plan: [Title]
...
```

### Contract 3: Task Lifecycle (AR-05)

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

#### 1. State Definitions
- **Active States:**
  - `pending`: Task plan initialized; classification complete; work has not yet started.
  - `in_progress`: Actively executing a playbook. Baseline re-verification during session pickup is an operation performed within this state.
  - `paused`: Execution voluntarily halted at an atomic boundary. Durable work preserved; resume note identifies current state and next action.
  - `blocked`: Involuntary stop due to external impediment, missing prerequisite, environment failure, or contradictory requirement.
- **Terminal States:**
  - `completed`: Falsifiable done predicate satisfied with captured empirical evidence.
  - `failed`: Task cannot be completed because execution encountered an unrecoverable failure within permitted scope.
  - `cancelled`: An authorized human actor intentionally abandons or supersedes the task.

#### 2. Complete State Transition Matrix

| Current State | Allowed Next States | Trigger Event & Invariant Gate |
|---|---|---|
| `pending` | `in_progress`, `cancelled` | Kickoff authorized; execution begins, or task cancelled prior to start. |
| `in_progress` | `paused`, `blocked`, `completed`, `failed`, `cancelled` | Voluntary pause; involuntary blocker; done predicate pass; unrecoverable failure; or human cancellation. |
| `paused` | `in_progress`, `cancelled` | Resumed via `session-pickup` after baseline re-verification; or cancelled while paused. |
| `blocked` | `in_progress`, `failed`, `cancelled` | Prerequisite resolved; blocker proven permanent; or cancelled while blocked. |
| `completed` | *None (Terminal)* | Immutable. New requirements require a fresh task plan. |
| `failed` | *None (Terminal)* | Immutable. Retrying work requires authoring a fresh task plan referencing prior failure. |
| `cancelled` | *None (Terminal)* | Immutable. New work requires authoring a fresh task plan. |

Terminal states (`completed`, `failed`, `cancelled`) cannot be reopened; prefer creating a new task plan over reopening terminal tasks.

### Contract 4: Delegation & Concurrency Contract (AR-07)
Governs dispatching work to subagents or background workers:

#### 1. Skill Invocation vs. Agent Delegation
Paddlr establishes strict terminology to distinguish between execution models:
- **Invoke a Skill:** The Main Agent applies a specialized capability, checklist, or engineering standard within its own active execution context (in-thread). No second agent is launched.
- **Delegate to a Worker:** The Main Agent assigns an explicit slice of work to another Agent (subagent, background worker, or isolated process) with an explicit brief, scope boundaries, and return deliverables.

**Single-Agent Invariant:** Phase 3 workflows and playbooks may **invoke Skills** within the single-agent execution thread, but must **not implement or activate Worker delegation**. Worker delegation remains deferred to Phase 4.

#### 2. Delegation Brief Model (Phase 4+)

```typescript
interface DelegationBrief {
  worker_id: string;
  role: string;                   // e.g. "Security Reviewer", "Refactoring Worker"
  model_profile?: "deep-reasoning" | "standard-code" | "fast-mechanical"; // OPTIONAL
  goal: string;                   // Concise statement of objective
  scope_boundaries: string[];     // Explicit files/modules allowed to edit
  readonly: boolean;              // Restrict to read-only tools
  context_references: string[];   // Paths to relevant files (no inlined context bloat)
  deliverables: string[];         // Expected files or patches produced
  verification_command: string;   // Command worker must execute to verify its work
  failure_protocol: string;       // Action on failure (revert and report vs retry)
}
```

#### 3. Rules for Subagents and Canonical State Ownership:
1. **Optional Model Profiles:** Model profiles (`deep-reasoning`, `standard-code`, `fast-mechanical`) are **strictly optional capabilities**. If the host runtime does not support model steering, the orchestrator proceeds using the runtime's active model without error.
2. **Canonical State Ownership:** The **Main Agent exclusively owns, updates, and writes the canonical Task State** in `docs/paddlr/plans/`. Workers/subagents must *never* modify canonical Task State and must *never* merge directly into the main branch.
3. **Bounded Return:** Workers return bounded deliverables (diff/patch files or text reports), execution status (`PASS`/`FAIL` with verbatim command outputs), and verification evidence.
4. **Concurrent Worker Integration:** To eliminate write conflicts:
   - Workers execute in isolated workspaces, Git worktrees, or designated scratch directories (`principle-separate-before-serializing-shared-state`).
   - Workers emit their results to local branch patches or return messages.
   - The Main Agent drains worker results **sequentially**, reviews diffs, verifies each change on the main artifact, integrates/merges changes into the working tree, and updates the canonical Task State in `docs/paddlr/plans/`.

### Contract 5: Runtime Adapter Contract (AR-08)
Isolates core engineering behavior from runtime-specific tooling using semantic capability primitives.

Core v1 establishes a strict Single-Agent baseline. `agent.delegate` and `scheduler.loop` are kept out of the required Core v1 runtime capability set. A Single-Agent runtime does not need to implement them; an environment providing only the 5 mandatory primitives (`fs.read`, `fs.write`, `fs.patch`, `shell.exec`, `search.find`) is 100% fully compliant with Paddlr Core v1.

| Semantic Primitive | Capability Category | Core v1 Requirement | Description | Fallback Strategy if Unsupported |
|---|---|---|---|---|
| `fs.read`, `fs.write`, `fs.patch` | Filesystem | **Required (Mandatory)** | Read, create, and patch local repository files. | Mandatory. No fallback. |
| `shell.exec` | Shell | **Required (Mandatory)** | Run shell commands in workspace. | Mandatory. No fallback. |
| `search.find` | Discovery | **Required (Mandatory)** | Search paths and content regexes. | Fall back to `shell.exec` (`git ls-files`, `findstr`, Python). |
| `model.steer` | Reasoning Tier | **Optional Enhancement** | Select model reasoning tier. | Fall back to runtime's default active model. |
| `ui.prompt` | User Interface | **Optional Enhancement** | Interactive multiple-choice prompt. | Fall back to plain-text turn prompt. |
| `agent.delegate` | Multi-Agent | **Deferred (Phase 4)** | Spawn isolated worker agent. | Not required for Core v1. Single-agent runtimes do not implement. |
| `scheduler.loop` | Automation | **Deferred (Phase 6)** | Automated background loops. | Not required for Core v1. Single-agent runtimes do not implement. |

### Contract 6: Autonomy Policy (AR-09)
Separates decision authority from operational execution authorization:

- **Autonomous (Just Do It):** Reading code, running read-only search commands, editing implementation files in working tree, creating local scratch files, running unit test suites, profiling.
- **Proceed with Plan Approval (Level 2):** Introducing new dependencies, creating architectural specifications, multi-file refactorings. Approved via implementation plan sign-off.
- **Mandatory Approval Pause (Level 3 / Irreversible):** Force-pushing to shared Git branches, deleting production or database state, executing external deployments, sending external messages.

### Contract 7: Evidence Contract (AR-10)
Defines acceptable proof of completion:

- **Valid Evidence Types:**
  - `PASS`: Verbatim terminal output showing exit code 0 and passing test count.
  - `FAIL`: Verbatim terminal output showing stack trace, assertion failure, or exit code != 0.
  - `MEASURED`: Number with explicit noise floor, bounding limiter, and median across N runs (`principle-explain-the-number`).
- **Forbidden Proxies:** "It compiles", file mtime changes, or agent declarations ("I have verified that...").
- **Verification Binding:** All verification logs must record the current Git commit SHA (`git rev-parse HEAD`).

### Contract 8: Recovery & Checkpoint Protocol (AR-11)
Governs session resumption, crash recovery, and idempotent execution.

1. **Durable Recoverable Work Invariant (`pause-safely`):** On pause, working state is safely preserved, and the plan is updated with current status (`paused`), last verified step, and next action. A `wip:` commit is one supported mechanism, not a mandatory requirement.
2. **State Resumption (`session-pickup`):** On session start or pickup, inspect `docs/paddlr/plans/` and `git status`, re-verifying the last known passing state before making new changes.
3. **In-Turn Retries vs. Deferred Loops:** Bounded in-turn retries (1–2 attempts) for transient errors are core behavior; autonomous multi-hour background scheduling without human turn oversight is deferred to Phase 6.
4. **Idempotence Invariant (`principle-make-operations-idempotent`):** All lifecycle steps and commands must converge to the same end state regardless of partial prior runs or crashes.

---

## D-05: Component Migration Mapping

### 1. Principle Skills Migration (24 Principles)

All 24 principles remain at the repository root level (`skills/principle-*/SKILL.md`).

| # | Principle Skill | Decision | Required Changes & Rationale |
|---|---|---|---|
| 1 | `principle-attack-the-premise` | **REUSE** | Keep as-is. Perfectly aligns with scientific debugging. |
| 2 | `principle-boundary-discipline` | **REUSE** | Keep as-is. Clean architecture boundary rules. |
| 3 | `principle-build-the-lever` | **REUSE** | Keep as-is. Encourages deterministic tooling. |
| 4 | `principle-encode-lessons-in-structure` | **REUSE** | Keep as-is. Promotes structural checks over prompt bloat. |
| 5 | `principle-exhaust-the-design-space` | **ADAPT** | Expand truncated body text with prototyping protocol and evaluation criteria. |
| 6 | `principle-experience-first` | **REUSE** | Keep as-is. Customer and maintainer delight heuristics. |
| 7 | `principle-explain-the-number` | **REUSE** | Keep as-is. Empirical measurement bounding checklist. |
| 8 | `principle-fix-root-causes` | **REUSE** | Keep as-is. Anti-defensive guard rules. |
| 9 | `principle-foundational-thinking` | **REUSE** | Keep as-is. Data modeling and scaffold-first sequencing. |
| 10 | `principle-guard-the-context-window` | **ADAPT** | Expand sparse body text with concrete subagent delegation and summarization guidance. |
| 11 | `principle-laziness-protocol` | **REUSE** | Keep as-is. Minimal diffs and consolidated decisions. |
| 12 | `principle-make-operations-idempotent` | **REUSE** | Keep as-is. Crash-safe convergent operations. |
| 13 | `principle-migrate-callers-then-delete-legacy-apis` | **REUSE** | Keep as-is. Clean refactoring wave rules. |
| 14 | `principle-minimize-reader-load` | **REUSE** | Keep as-is. Collapsing single-caller wrappers and shrinking scope. |
| 15 | `principle-model-the-domain` | **REUSE** | Keep as-is. Type modeling over scattered conditionals. |
| 16 | `principle-never-block-on-the-human` | **REUSE** | Keep as-is. Autonomy on reversible work; pause on irreversible actions. |
| 17 | `principle-outcome-oriented-execution` | **REUSE** | Keep as-is. End-state convergence over throwaway intermediate wrappers. |
| 18 | `principle-prove-it-works` | **REUSE** | Keep as-is. Evidence on real artifacts over proxies. |
| 19 | `principle-redesign-from-first-principles` | **REUSE** | Keep as-is. Holistic rethinking when integrating new requirements. |
| 20 | `principle-separate-before-serializing-shared-state` | **REUSE** | Keep as-is. Concurrency isolation rules. |
| 21 | `principle-sequence-verifiable-units` | **REUSE** | Keep as-is. Bracketed, verifiable unit slicing. |
| 22 | `principle-subtract-before-you-add` | **REUSE** | Keep as-is. Removing complexity and dead code before construction. |
| 23 | `principle-test-behavior-not-implementation` | **REUSE** | Keep as-is. Contract testing surviving internal refactoring. |
| 24 | `principle-type-system-discipline` | **ADAPT** | Remove dangling link to missing `typescript-best-practices` skill; replace with generic static typing guidance. |

### 2. Playbooks Migration (22 Playbooks inside `skills/paddlr-mode/playbooks/`)

| # | Playbook | Decision | Target Location & Required Changes | Priority |
|---|---|---|---|---|
| 1 | `authoring-a-skill.md` | **ADAPT** | Keep in `playbooks/`; invoke `skills/skill-creator` for core skill drafting. | Phase 3 |
| 2 | `autonomous-run.md` | **DEFER** | Defer unattended execution beyond initial core (Decision 4). | Phase 5 |
| 3 | `autopilot-full.md` | **DEFER** | Defer to Phase 6; requires multi-agent cloud infrastructure (Decision 3). | Phase 6 |
| 4 | `autopilot-stack.md` | **DEFER** | Defer to Phase 6; depends on multi-agent cloud infrastructure (Decision 3). | Phase 6 |
| 5 | `babysit.md` | **ADAPT** | Keep in `playbooks/`; decouple from Origin CLI; make `gh` standard; retain `watch-pr`. | Phase 4 |
| 6 | `bug-fix.md` | **ADAPT** | Keep in `playbooks/`; invoke `sre-debugging` for diagnosis and `test-driven-development` for fix. | Phase 3 |
| 7 | `eval.md` | **ADAPT** | Keep in `playbooks/`; decouple from Cursor transcript paths and model slugs. | Phase 4 |
| 8 | `feature.md` | **ADAPT** | Keep in `playbooks/`; harmonize with `feature-development`; link to `docs/paddlr/plans/`. | Phase 3 |
| 9 | `hillclimb.md` | **ADAPT** | Keep in `playbooks/`; retain `decision.tsv`; decouple model slugs; run bounded iterations. | Phase 4 |
| 10 | `investigation.md` | **REUSE** | Keep in `playbooks/`; replace `unslop` reference with Paddlr prose guidelines. | Phase 3 |
| 11 | `multi-phase-plan.md` | **ADAPT** | Keep in `playbooks/`; harmonize with `writing-plans`; persist to `docs/paddlr/plans/`. | Phase 3 |
| 12 | `opening-a-pr.md` | **ADAPT** | Keep in `playbooks/`; decouple from `/deslop`; use standard lint/review passes. | Phase 3 |
| 13 | `pause-safely.md` | **ADAPT** | Keep in `playbooks/`; persist resume note in `docs/paddlr/` instead of `/tmp/`. | Phase 3 |
| 14 | `perf-issue.md` | **ADAPT** | Keep in `playbooks/`; invoke `sre-debugging`; retain 7 perf mantras & SQLite. | Phase 4 |
| 15 | `prototype.md` | **REUSE** | Keep in `playbooks/`; standardize scratch directory to `.scratch/`. | Phase 3 |
| 16 | `refactoring.md` | **ADAPT** | Keep in `playbooks/`; integrate with `test-driven-development` REFACTOR phase. | Phase 3 |
| 17 | `runtime-forensics.md` | **REUSE** | Keep in `playbooks/`; live profiling and CDP diagnostics. | Phase 4 |
| 18 | `session-pickup.md` | **ADAPT** | Keep in `playbooks/`; read `docs/paddlr/plans/` and Git history instead of IDE transcripts. | Phase 3 |
| 19 | `shipping.md` | **DEFER** | Defer to Phase 6; stacked PR landing requires cloud agents and stack watchers. | Phase 6 |
| 20 | `trace-forensics.md` | **REUSE** | Keep in `playbooks/`; offline SQLite trace analysis. | Phase 4 |
| 21 | `visual-parity.md` | **ADAPT** | Keep in `playbooks/`; decouple from `/loop` and `control-ui`; use Playwright/headless diff. | Phase 4 |
| 22 | `worktree-cleanup.md` | **DEFER** | Defer to Phase 6; macOS/Xcode simulator disk cleanup utility. | Phase 6 |

### 3. Auxiliary Poteto Skills Migration (15 Skills)

| # | Skill | Decision | Required Changes & Rationale | Priority |
|---|---|---|---|---|
| 1 | `architect` | **ADAPT** | Ground in `docs/paddlr/specs/` (Section 10) & `docs/paddlr/plans/`. | Phase 3 |
| 2 | `arena` | **ADAPT** | Decouple model slugs to runtime adapter; add single-agent sequential fallback. | Phase 4 |
| 3 | `benchmark-checklist` | **REUSE** | Keep as-is. High-value 7-question empirical checklist. | Phase 4 |
| 4 | `blast-radius` | **REUSE** | Keep as-is. Executable pre-merge safety proof. | Phase 4 |
| 5 | `create-verification-skill` | **ADAPT** | Generalize output destination from `.cursor/skills/` to runtime-agnostic paths. | Phase 4 |
| 6 | `figure-it-out` | **ADAPT** | Replace `todolist` tool and `show-me-your-work` with `docs/paddlr/plans/`. | Phase 4 |
| 7 | `how` | **ADAPT** | Add single-agent fallback for environments without subagent support. | Phase 3 |
| 8 | `in-your-own-words` | **REUSE** | Keep as-is. Intent restatement and assumption extraction. | Phase 1 |
| 9 | `interrogate` | **ADAPT** | Decouple from `arena` model files; add single-agent self-red-teaming mode. | Phase 4 |
| 10 | `maintain-verification-skill` | **ADAPT** | Adapt alongside `create-verification-skill`. | Phase 4 |
| 11 | `recall` | **ADAPT/REPLACE** | Replace Cursor JSONL transcript mining with queries against Git and `docs/paddlr/`. | Phase 3 |
| 12 | `reflect` | **ADAPT** | Generalize destination paths to repository-level skills; integrate with `skill-creator`. | Phase 4 |
| 13 | `swarm` | **ADAPT** | Abstract worker dispatch behind Runtime Adapter Contract with serial fallback. | Phase 4 |
| 14 | `teach` | **REUSE** | Keep as-is. Pedagogical step-by-step onboarding walkthroughs. | Phase 3 |
| 15 | `why` | **REUSE** | Keep as-is. Forensic search across Git, PRs, and `docs/paddlr/decisions/`. | Phase 3 |

### 4. Dependency Verification & Retirement of Missing References (Decision 5)

An exhaustive repository audit across `skills/` verified exactly **25 occurrences** of the 7 missing external references across 12 files. Rather than claiming a capability is replaced merely because a related tool exists, each reference is categorized by its actual architectural status (Intentionally Removed, No Longer Needed, or Replaced):

- **Phase 3 Scope (14 occurrences across 7 files):** `paddlr-mode/SKILL.md` (7), `investigation.md` (1), `opening-a-pr.md` (1), `pause-safely.md` (1), `recall/SKILL.md` (1), `teach/SKILL.md` (1), `blast-radius/SKILL.md` (1).
- **Later Phases Scope (11 occurrences across 5 files):** Phase 4 (`figure-it-out/SKILL.md` [1], `hillclimb.md` [1]), Phase 5 (`autonomous-run.md` [1]), Phase 6 (`autopilot-full.md` [7], `shipping.md` [2]).

| Missing Reference | Repository Occurrences (Exact File & Line) | Architectural Status | Migration Action & Rationale |
|---|---|---|---|
| `unslop` / `deslop` (8) | `blast-radius` (L48), `paddlr-mode` (L23, L24), `investigation` (L10), `opening-a-pr` (L5), `recall` (L33), `teach` (L19), `autopilot-full` (L10) | **Intentionally Removed** | Proprietary text clean-up plugin. Dropped in favor of Paddlr's native declarative communication style rules in `rules/AGENTS.md`. |
| `technical-writing` (1) | `paddlr-mode` (L23) | **No Longer Needed as Standalone Skill** | Writing standards are already structurally embedded in core repository conventions: Conventional Commits (`CONTRIBUTING.md`), PR template in `opening-a-pr.md`, and `rules/AGENTS.md`. No standalone skill required. |
| `no-comments` (2) | `paddlr-mode` (L24), `autopilot-full` (L10) | **Intentionally Removed as Standalone Skill** | Clean-code inspection heuristic. Folded into `skills/code-review/` and standard reviewer heuristics. |
| `show-me-your-work` (6) | `paddlr-mode` (L29), `pause-safely` (L8), `figure-it-out` (L46), `hillclimb` (L9), `autonomous-run` (L10), `autopilot-full` (L12) | **Replaced** | Replaced by the single canonical Task State plan in `docs/paddlr/plans/YYYY-MM-DD-<slug>.md`. |
| `ketchup` (2) | `autopilot-full` (L22, L25) | **Intentionally Removed** | Redundant with standard Git commands (`git log`, `git diff`) and `session-pickup.md`. Dropped without replacement. |
| `control-ui` (3) | `paddlr-mode` (L25), `autopilot-full` (L14), `shipping` (L5) | **Intentionally Removed** | Proprietary Cursor UI automation tool. Reliance on proprietary IDE control plugins is intentionally removed; UI verification relies on standard project-level test harnesses (Playwright, Cypress, or app harnesses). |
| `control-cli` (3) | `paddlr-mode` (L25), `autopilot-full` (L14), `shipping` (L5) | **Intentionally Removed** | Proprietary Cursor CLI automation tool. Reliance on proprietary IDE control plugins is intentionally removed; CLI verification relies on standard shell command execution (`run_command`). |

**Total Occurrences:** 8 + 1 + 2 + 6 + 2 + 3 + 3 = **25 occurrences**. Zero stub skills will be created.

---

## D-06: Phased Development Roadmap

The development roadmap is strictly sequenced into 5 active phases and 1 deferred phase:
1. **Single-Agent Core Execution First (Phases 1-3).**
2. **Local Subagent Delegation & Diagnostics (Phase 4).**
3. **Advanced Playbooks & Tooling (Phase 5).**
4. **Deferred Cloud Swarms & Unattended Loops (Phase 6).**

```text
Phase 1: Foundation & Metadata Conformance (Fix validate_skills, adapt 3 principles)
   │
   ▼
Phase 2: Core Contracts & Task State Infrastructure (State engine in docs/paddlr/plans/)
   │
   ▼
Phase 3: Single-Agent Core Playbook & Skill Harmonization (feature, bug-fix, tdd, sre)
   │
   ▼
Phase 4: Diagnostics, Forensics & Local Subagent Delegation (perf, traces, benchmarks, arena)
   │
   ▼
Phase 5: Advanced Playbooks, Evaluation & Stack Watching (figure-it-out, hillclimb, watch-pr)
   │
   ▼
Phase 6: Multi-Agent Cloud Swarms & Unattended Loops [Deferred]
```

---

### Phase 1: Foundation & Metadata Conformance

- **Objective:** Fix immediate validation errors, rebrand the entrypoint to Paddlr Mode, establish Agent Skills specification conformance, and adapt the 3 incomplete principle skills.
- **Dependencies:** None (initial phase).
- **Scope:**
  - `skills/paddlr-mode/SKILL.md` frontmatter and title.
  - `skills/principle-exhaust-the-design-space/SKILL.md`.
  - `skills/principle-guard-the-context-window/SKILL.md`.
  - `skills/principle-type-system-discipline/SKILL.md`.
- **Tasks:**
  - [x] **Task 1.1: Correct Paddlr Mode Metadata Conformance**
    - **Consumes:** `skills/paddlr-mode/SKILL.md`
    - **Produces:** Validated `skills/paddlr-mode/SKILL.md`
    - Change frontmatter `name: poteto-mode` to `name: paddlr-mode`.
    - Update description to reflect Paddlr's agent-agnostic engineering framework.
    - Change H1 title from `# Poteto mode` to `# Paddlr mode`.
  - [x] **Task 1.2: Adapt `principle-exhaust-the-design-space`**
    - **Consumes:** `skills/principle-exhaust-the-design-space/SKILL.md`
    - **Produces:** Expanded skill body
    - Add explicit operational sections: core rule (2-3 competing prototypes side-by-side), evaluation criteria, and clean discard instructions.
  - [x] **Task 1.3: Adapt `principle-guard-the-context-window`**
    - **Consumes:** `skills/principle-guard-the-context-window/SKILL.md`
    - **Produces:** Expanded skill body
    - Add practical context-budgeting tactics: bulk extraction delegation to subagents, targeted AST/grep reads, and returning distilled summaries to main context.
  - [x] **Task 1.4: Adapt `principle-type-system-discipline`**
    - **Consumes:** `skills/principle-type-system-discipline/SKILL.md`
    - **Produces:** Cleaned skill body
    - Remove dangling reference to nonexistent `typescript-best-practices` skill; replace with language-agnostic static typing guidance.
- **Deliverables:** Updated `skills/paddlr-mode/SKILL.md` and 3 updated principle skills.
- **Acceptance Criteria:** `python scripts/validate_skills.py` passes with **48/48 valid skills (100% PASS)**.
- **Verification Command:**
  ```powershell
  python scripts/validate_skills.py --verbose
  ```
- **Exit Conditions:** Zero validation errors across all 48 skills in repository.

---

### Phase 2: Core Contracts & Task State Infrastructure

- **Objective:** Establish the runtime-independent orchestration core, implement the Task State persistence model in `docs/paddlr/plans/`, and standardize the Runtime Adapter boundary with optional model steering.
- **Dependencies:** Phase 1 complete.
- **Scope:**
  - Core contract specifications persisted in `skills/paddlr-mode/references/core-contracts.md`.
  - Task State schema and plan format in `skills/paddlr-mode/references/task-state-schema.md`.
  - Definition of capability negotiation interface in `skills/paddlr-mode/references/runtime-adapters.md`.
- **Tasks:**
  - [x] **Task 2.1: Author Core Contracts Reference Guide**
    - **Consumes:** Specification Section 6 and D-04 designs
    - **Produces:** `skills/paddlr-mode/references/core-contracts.md`
    - Formalize Intent Contract, Task State Model, Task Lifecycle, Delegation Contract, Autonomy Policy, Evidence Contract, and Recovery Protocol. Include explicit rules for Main Agent canonical state ownership and worker integration.
  - [x] **Task 2.2: Establish Task State Plan Schema**
    - **Consumes:** Paddlr plan conventions
    - **Produces:** `skills/paddlr-mode/references/task-state-schema.md`
    - Define standard YAML frontmatter and Markdown structure for persistent plans in `docs/paddlr/plans/YYYY-MM-DD-<slug>.md`. Define distinction from long-lived Project Memory.
  - [x] **Task 2.3: Author Runtime Adapter Capability Contract**
    - **Consumes:** D-04 Runtime Adapter Contract
    - **Produces:** `skills/paddlr-mode/references/runtime-adapters.md`
    - Define required, optional, and deferred capability matrix (classifying model profile steering as optional, and looping as deferred) with fallback strategies.
- **Deliverables:** Core contract reference guides in `skills/paddlr-mode/references/`.
- **Acceptance Criteria:** Reference documents are populated, validated by link checkers, and adhere to Paddlr rules.
- **Verification Command:**
  ```powershell
  python scripts/check_markdown_links.py
  ```
- **Exit Conditions:** All core contracts documented and cross-linked.

---

### Phase 3: Single-Agent Core Playbook & Skill Harmonization

- **Objective:** Adapt the primary single-agent development playbooks, harmonizing them with Paddlr's native skills (`feature-development`, `sre-debugging`, `test-driven-development`, `writing-plans`, `writing-specs`), removing Cursor-specific model slugs, and retiring missing external references under a strict Single-Agent execution baseline.
- **Dependencies:** Phase 2 complete.
- **Scope & Constraints:**
  - **Strict Single-Agent Baseline:** No actual worker dispatch, subagent delegation, or multi-agent orchestration implementation in Phase 3. Single-agent execution is the primary mode of operation.
  - **Skill Invocation vs. Agent Delegation Terminology:** "Invoke a Skill" means the Main Agent uses a specialized capability in its own execution context. "Delegate to a Worker" means assigning work to another Agent. Phase 3 may invoke Skills but must not implement or activate Worker delegation.
  - **Playbooks Orchestrate; Skills Provide Capabilities:** Playbooks inside `skills/paddlr-mode/playbooks/` orchestrate workflows; independent companion skills (`feature-development`, `sre-debugging`, `test-driven-development`, `writing-plans`, `writing-specs`, `skill-creator`, `code-review`) provide specialized capabilities without duplicating instructions inside playbooks.
  - **Deferred Runtime Capabilities:** `agent.delegate` and `scheduler.loop` are kept out of the required Core v1 runtime capability set. A Single-Agent runtime does not need to implement these capabilities.
  - **Worker Kickoff Harmonization Without Delegation:** `skills/paddlr-mode/worker.md` will be harmonized with Paddlr conventions (Paddlr style, Conventional Commits, standard PR format, evidence logging, Autonomy Policy guardrails), but **must not enable delegation** (no launching subagents or recursive worker kickoff).
  - **Audited External Reference Retirement:** Each missing external skill reference is audited against Table 4 before removal (categorized as Replaced, No Longer Needed, or Intentionally Removed). Zero stub skills will be created. Exactly 14 in-scope occurrences across 7 files are retired in Phase 3 (with the remaining 11 occurrences in 5 files retired in later phases).
  - **No Unrelated Architecture:** Zero cloud swarms, zero unattended background loops, zero external daemons, and zero speculative capabilities.
  - Playbooks in scope: `feature.md`, `bug-fix.md`, `refactoring.md`, `investigation.md`, `prototype.md`, `pause-safely.md`, `session-pickup.md`, `opening-a-pr.md`, `authoring-a-skill.md`, `multi-phase-plan.md`.
  - Auxiliary skills in scope: `recall` (adapted to Git and `docs/paddlr/plans/`), `how` (single-agent exploration fallback), `teach` (remove `unslop`), `architect` (ground in `docs/paddlr/specs/` and `plans/`), `why` (query Git & `docs/paddlr/decisions/`).
  - Worker kickoff in scope: `skills/paddlr-mode/worker.md` (harmonized without delegation).
- **Tasks:**
  - [ ] **Task 3.1: Harmonize `feature.md` with `feature-development`**
    - **Consumes:** `skills/paddlr-mode/playbooks/feature.md`, `skills/feature-development/SKILL.md`
    - **Produces:** Refactored `feature.md`
    - Playbook orchestrates workflow; invokes `feature-development`, `writing-specs`, and `writing-plans` for domain logic; retains the 4-point throughput checkpoint and domain-first data modeling; records canonical state in `docs/paddlr/plans/`.
  - [ ] **Task 3.2: Harmonize `bug-fix.md` with `sre-debugging` and `test-driven-development`**
    - **Consumes:** `skills/paddlr-mode/playbooks/bug-fix.md`, `skills/sre-debugging/SKILL.md`, `skills/test-driven-development/SKILL.md`
    - **Produces:** Refactored `bug-fix.md`
    - Invoke `sre-debugging` for root cause analysis; enforce commit of failing test before fix via `test-driven-development`; remove model slugs.
  - [ ] **Task 3.3: Adapt `refactoring.md` to TDD Refactor Phase**
    - **Consumes:** `skills/paddlr-mode/playbooks/refactoring.md`, `skills/test-driven-development/SKILL.md`
    - **Produces:** Refactored `refactoring.md`
    - Retain characterization test pinning and reader load reduction; integrate with `test-driven-development` REFACTOR phase.
  - [ ] **Task 3.4: Adapt State & Session Playbooks (`pause-safely.md`, `session-pickup.md`, `recall`)**
    - **Consumes:** `skills/paddlr-mode/playbooks/pause-safely.md`, `session-pickup.md`, `skills/recall/SKILL.md`
    - **Produces:** Refactored playbooks and skill
    - Persist resume state to `docs/paddlr/plans/` (not `/tmp/`); enforce durable recoverable work invariant (wip commit is supported but not mandatory); adapt `session-pickup` and `recall` to inspect `docs/paddlr/` and Git history instead of IDE transcripts; execute baseline re-verification.
  - [ ] **Task 3.5: Adapt PR, Packaging & Worker Guidelines (`opening-a-pr.md`, `authoring-a-skill.md`, `worker.md`)**
    - **Consumes:** `opening-a-pr.md`, `authoring-a-skill.md`, `skills/paddlr-mode/worker.md`
    - **Produces:** Refactored playbooks and worker kickoff
    - Replace `/deslop` with standard lint/review passes; invoke `skill-creator` for skill authoring; standardize `worker.md` to Paddlr terminology, Conventional Commits, and Autonomy Policy while strictly disabling worker delegation.
  - [ ] **Task 3.6: Retire Missing External References across Playbooks & Skills**
    - **Consumes:** The 14 in-scope occurrences from D-05 Table 4 (across `blast-radius`, `investigation`, `teach`, `paddlr-mode/SKILL.md`, `opening-a-pr`, `pause-safely`, `recall`)
    - **Produces:** Cleaned playbooks and skills
    - Update the 7 Phase 3 files to replace `unslop`, `technical-writing`, `no-comments`, `show-me-your-work`, `ketchup`, and `control-*` with native Paddlr standards and canonical plan tracking, creating zero stub skills.
- **Deliverables:** 10 refactored playbooks, 1 refactored skill (`recall`), updated `worker.md`, retired external references across 7 files in Phase 3 scope (14 occurrences).
- **Acceptance Criteria:** All adapted playbooks and skills execute cleanly under a single-agent baseline without referencing Cursor-specific plugins, `/tmp/` paths, hardcoded model slugs, or missing external skills.
- **Verification Command:**
  ```powershell
  python scripts/validate_skills.py --verbose
  python -m unittest discover -s tests
  python scripts/check_markdown_links.py
  ```
- **Exit Conditions:** Single-agent development loop (`investigation` -> `feature`/`bug-fix` -> `tdd` -> `review` -> `open PR`) functions end-to-end under Paddlr Mode.

---

### Phase 4: Diagnostics, Forensics & Local Subagent Delegation

- **Objective:** Adapt performance diagnosis, offline trace analysis, visual regression, and local subagent delegation workflows (`arena`, `interrogate`, `swarm`), enforcing Main Agent canonical state ownership.
- **Dependencies:** Phase 3 complete.
- **Scope:**
  - Playbooks: `perf-issue.md`, `runtime-forensics.md`, `trace-forensics.md`, `visual-parity.md`, `hillclimb.md`, `eval.md`, `babysit.md`.
  - Auxiliary skills: `benchmark-checklist`, `blast-radius`, `create-verification-skill`, `maintain-verification-skill`, `reflect`, `arena`, `interrogate`, `swarm`.
- **Tasks:**
  - [ ] **Task 4.1: Adapt Performance Playbooks (`perf-issue.md`, `runtime-forensics.md`, `trace-forensics.md`)**
    - **Consumes:** `perf-issue.md`, `runtime-forensics.md`, `trace-forensics.md`
    - **Produces:** Refactored performance playbooks
    - Retain the 7 performance mantras and SQLite trace analysis; integrate with `sre-debugging` performance methods; decouple model slugs.
  - [ ] **Task 4.2: Adapt `visual-parity.md`**
    - **Consumes:** `skills/paddlr-mode/playbooks/visual-parity.md`
    - **Produces:** Refactored `visual-parity.md`
    - Decouple from Cursor `/loop` and `control-ui`; allow integration with standard headless browser harnesses (Playwright, pixelmatch).
  - [ ] **Task 4.3: Adapt Local Subagent Delegation Skills (`arena`, `interrogate`, `swarm`)**
    - **Consumes:** `arena`, `interrogate`, `swarm`
    - **Produces:** Runtime-agnostic candidate evaluation skills
    - Abstract model pools to runtime adapter; enforce Main Agent canonical state ownership; implement sequential integration of concurrent worker patches; add single-agent sequential fallbacks.
  - [ ] **Task 4.4: Adapt Optimization & Evaluation Playbooks (`hillclimb.md`, `eval.md`)**
    - **Consumes:** `hillclimb.md`, `eval.md`
    - **Produces:** Refactored playbooks
    - Retain on-disk `decision.tsv` state; decouple from Cursor transcript paths and model slugs; run bounded manual iterations.
  - [ ] **Task 4.5: Adapt Verification Harness Skills (`create-verification-skill`, `maintain-verification-skill`, `reflect`)**
    - **Consumes:** `create-verification-skill`, `maintain-verification-skill`, `reflect`
    - **Produces:** General-purpose verification harness skills
    - Generalize target skill directory from `.cursor/skills/` to runtime-configurable project paths.
- **Deliverables:** 7 refactored playbooks and 7 adapted skills.
- **Acceptance Criteria:** Diagnostic and local delegation tools operate portably across platforms without vendor-specific hooks.
- **Verification Command:**
  ```powershell
  python scripts/validate_skills.py
  ```
- **Exit Conditions:** Local subagent delegation and performance forensics conform to the Delegation (AR-07) and Evidence (AR-10) contracts.

---

### Phase 5: Advanced Playbooks, Dynamic Routing & Stack Watching

- **Objective:** Adapt open-ended problem solving (`figure-it-out.md`), PR babysitting, and the `watch-pr` CLI engine.
- **Dependencies:** Phase 4 complete.
- **Scope:**
  - Playbook: `figure-it-out.md`, `babysit.md`.
  - Tooling: `scripts/watch-pr/`, `scripts/bootstrap.ts`.
- **Tasks:**
  - [ ] **Task 5.1: Adapt `figure-it-out.md` for Dynamic Task Orchestration**
    - **Consumes:** `figure-it-out.md`
    - **Produces:** Refactored dynamic playbook
    - Ground hypothesis testing and state tracking in `docs/paddlr/plans/`; remove `todolist` and `show-me-your-work` references.
  - [ ] **Task 5.2: Adapt `babysit.md` and Tooling (`scripts/watch-pr/`, `scripts/bootstrap.ts`)**
    - **Consumes:** `babysit.md`, `scripts/watch-pr/`, `scripts/bootstrap.ts`
    - **Produces:** Rebranded, robust PR watcher CLI and playbook
    - Rebrand package to `@paddlr/watch-pr`; make `gh` standard forge client; ensure Bun and Node compatibility.
- **Deliverables:** 2 refactored playbooks, updated `watch-pr` package.
- **Acceptance Criteria:** Dynamic problem-solving and PR babysitting function cleanly across runtimes. `watch-pr` unit tests pass.
- **Verification Command:**
  ```powershell
  cd skills/paddlr-mode/scripts/watch-pr; bun test; cd ../../../..
  ```
- **Exit Conditions:** Dynamic routing and PR status watching operational under Paddlr Mode.

---

### Phase 6: Multi-Agent Cloud Swarms & Unattended Loops [Deferred]

- **Objective:** Revisit unattended looping and evaluate high-scale multi-PR cloud swarms and platform maintenance utilities after Task State, Recovery Protocol, and runtime capabilities have been validated.
- **Dependencies:** Phases 1-5 complete, multi-agent cloud infrastructure available, and explicit project owner authorization.
- **Scope:**
  - Playbooks: `autonomous-run.md`, `autopilot-full.md`, `autopilot-stack.md`, `shipping.md`, `worktree-cleanup.md`.
  - Script: `scripts/worktree-audit.sh`.
- **Tasks:**
  - [ ] **Task 6.1: Revisit Unattended Looping & Polling (`autonomous-run.md`)** (Evaluate runtime-independent looping without external background daemons).
  - [ ] **Task 6.2: Evaluate Cloud Swarm Requirements** (Assess feasibility of adapting `autopilot-full.md` and `autopilot-stack.md` to Antigravity Swarm or Claude Agent Teams).
  - [ ] **Task 6.3: Adapt Stacked PR Shipping Playbook (`shipping.md`)** (Evaluate `git patch-id` retargeting engine for automated stack landing).
  - [ ] **Task 6.4: Cross-Platform Worktree Maintenance Utility** (Rewrite `worktree-audit.sh` in Python/Node to support Windows and Linux).
- **Deliverables:** Deferred playbooks adapted or formally deprecated.
- **Acceptance Criteria:** Swarm orchestration tested on compatible multi-agent infrastructure.
- **Exit Conditions:** Full enterprise-scale multi-agent capabilities operational.

---

## D-07: Evaluation & Verification Plan

Paddlr Mode will be validated against 12 end-to-end evaluation scenarios representing the core engineering spectrum:

| # | Scenario | Initial Condition | Expected Agent Behavior | Expected Task State | Verification Gate |
|---|---|---|---|---|---|
| 1 | **Simple Bug Fix** | Failing unit test or reported regression | Classify as Level 1; select `bug-fix.md`; reproduce failure; stage failing test commit before fix; implement fix | Minimal diff; no persistent plan file needed; commit history has failing commit then fix commit | Repro command passes; entire test suite green |
| 2 | **Feature Implementation** | Feature request with clear scope | Classify as Level 2; select `feature.md`; invoke `feature-development`; trace code; draft spec & plan | `docs/paddlr/specs/` and `docs/paddlr/plans/` created with checkboxes | Live matching surface proof; unit tests green |
| 3 | **Read-Only Investigation** | "How does component X work?" | Select `investigation.md`; trace code; route motivation questions to `why` | Read-only structured report; no state files written | Cited file, symbol, and line numbers; zero uncommitted edits |
| 4 | **Refactoring** | Code smells / high reader load | Select `refactoring.md`; pin behavior with characterization tests first; subtract dead code; reshape structure | Characterization tests committed before edits | Pre-existing characterization tests remain green; zero behavioral divergence |
| 5 | **Ambiguous Request** | Unclear user prompt | Invoke `in-your-own-words`; separate facts from assumptions; present 2-3 concrete alternatives | Intent state in chat turn; does not write code prematurely | User confirmation received before code edits begin |
| 6 | **Multi-Step Initiative** | Cross-cutting system migration | Classify as Level 3; select `multi-phase-plan.md`; decompose into verifiable slices with dependencies | Multi-phase plan in `docs/paddlr/plans/` with unit/live/perf checkboxes | Each phase verified independently before advancing to next |
| 7 | **Delegated Task** | Fan-out review or parallel work | Main agent constructs `DelegationBrief`; dispatches bounded subagent; reviews diff | Subagent assigned in plan state; diff reviewed by main agent | Verification command in brief passes; main agent writes own summary |
| 8 | **Worker Failure** | Subagent crashes or fails verification | Main agent catches failure; does not cascade breaking changes; reverts partial worker edits | Task status marked `BLOCKED` or retried with fresh subagent | Dirty edits wiped; workspace restored to clean baseline |
| 9 | **Interruption & Recovery** | User interrupts / "pause safely" | Select `pause-safely.md`; cancel workers; stage uncommitted work as `wip:` commit; update plan | Plan frontmatter marked `paused`; resume note written | Clean git tree; resuming via `session-pickup` re-validates state |
| 10 | **Runtime Without Delegation** | Agent running on runtime without subagents | Adapter detects missing `spawn_agent` capability; falls back to sequential execution | Single-agent execution trail in plan file | All tasks completed sequentially; same verification gates pass |
| 11 | **Verification Failure** | Fix fails regression test suite | Agent detects failure; invokes `principle-attack-the-premise`; does not paper over failure with guards | Failure logged in plan; root cause investigated | No defensive patch committed; real root cause fixed |
| 12 | **Mid-Run Requirement Change** | User alters requirements mid-execution | Agent halts active step; invokes `principle-redesign-from-first-principles`; updates spec and plan | Spec and plan updated and re-approved before code resumes | New requirements integrated cleanly; obsolete code deleted |

---

## D-08: Resolved Architectural Decision Gates

All 5 architectural decision gates have been resolved by the project owner:

### Decision Gate 1: Task State Persistence Format & Location
- **Status:** **APPROVED Option A** (Git-tracked Markdown files under `docs/paddlr/plans/`).
- **Binding Constraints:**
  - Single canonical Task State: The Git-tracked Markdown task plan (`docs/paddlr/plans/YYYY-MM-DD-<slug>.md`) is the *single canonical Task State*. No secondary files or databases (including `decision.tsv`) may function as a parallel state store. `decision.tsv` serves strictly as an ephemeral, local scratch iteration log for raw numerical trial data during hillclimbing.
  - Use one file per persistent task (`docs/paddlr/plans/YYYY-MM-DD-<slug>.md`).
  - Use YAML frontmatter for structured task state machine fields.
  - Use Markdown body for context, decisions, progress checkboxes, and verification evidence.
  - Do not persist every trivial task (Level 1 small changes do not create plan files).
  - Distinguish Task State from Project Memory: Project Memory is not strictly immutable; `PROJECT.md` represents the living current project snapshot, while `DECISIONS.md` records architectural decisions and their historical evolution (ADR index, where decisions are superseded rather than silently overwritten).

### Decision Gate 2: Playbook vs. Native Skill Orchestration Hierarchy
- **Status:** **APPROVED Option A** (Playbooks orchestrate workflows; independent Skills provide specialized capabilities).
- **Binding Constraints:**
  - Playbooks remain strictly inside `skills/paddlr-mode/playbooks/`.
  - Independent Skills remain at the same repository level as `paddlr-mode` (`skills/<name>/`).
  - Forbidden: Do not create `skills/paddlr-mode/skills/` or `skills/paddlr-mode/principles/`.
  - Avoid duplicating Companion Skill instructions inside Playbooks (playbooks coordinate; skills implement domain logic).

### Decision Gate 3: Subagent & Cloud Swarm Phasing
- **Status:** **APPROVED Option A** (Strict progressive phasing).
- **Binding Constraints:**
  - Prioritize: (1) Single-agent execution, (2) Local subagent delegation, (3) Multi-agent coordination after delegation contract is validated.
  - Defer cloud swarms, `autopilot-stack.md`, `autopilot-full.md`, and complex shipping automation to Phase 6.
  - Main Agent Ownership: Workers must not modify canonical Task State or merge directly into the main branch. Workers return bounded deliverables, patches, and verification evidence. The Main Agent reviews, integrates, verifies, and updates canonical Task State.

### Decision Gate 4: Looping & Polling Mechanism for Unattended Runs
- **Status:** **MODIFIED Recommendation**.
- **Binding Constraints:**
  - Keep looping and polling runtime-independent in principle, but defer unattended execution implementation beyond the initial Paddlr Core.
  - Do not introduce an external background daemon.
  - Revisit this capability in Phase 6 after Task State, Recovery Protocol, and runtime capabilities have been validated.

### Decision Gate 5: Retirement of Missing External References
- **Status:** **APPROVED Option A** (Retire references without stubs, subject to dependency verification).
- **Binding Constraints:**
  - Verified all 20 occurrences of missing references (`unslop`, `technical-writing`, `no-comments`, `show-me-your-work`, `ketchup`, `control-ui`, `control-cli`).
  - Distinguish capabilities: `technical-writing` is no longer needed as a standalone skill (embedded in repository conventions); `control-ui`/`control-cli` reliance is intentionally removed in favor of standard repository test tooling; `unslop`/`deslop` and `ketchup` are intentionally removed; `show-me-your-work` is replaced by canonical Task State tracking in `docs/paddlr/plans/`.
  - Do not claim a capability is replaced merely because a related tool exists.
  - Do not create empty stub Skills.

### Execution Status
- **Phase 1 Authorized:** Execution of Phase 1 (Foundation & Metadata Conformance) authorized by the project owner. Implementation of subsequent phases remains held pending review and authorization.
