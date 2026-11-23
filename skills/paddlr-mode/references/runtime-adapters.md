# Runtime Adapter Contract Specification

**Status:** Normative Adapter Specification  
**Framework:** Paddlr — Agent-Agnostic Software Engineering  
**Authority:** [docs/paddlr/plans/2026-11-23-paddlr-mode-evolution.md](../../../docs/paddlr/plans/2026-11-23-paddlr-mode-evolution.md)  
**Location:** `skills/paddlr-mode/references/runtime-adapters.md`

---

## 1. Overview

Paddlr is an **agent-agnostic framework**. Its orchestration core (Paddlr Mode, Playbooks, Principles, and Companion Skills) must never depend directly on vendor-specific tool names, proprietary SDK APIs, or runtime-exclusive extensions.

This document defines the **Runtime Adapter Contract**: the boundary isolating runtime-independent engineering logic from runtime-specific execution capabilities across Claude Code, Cursor, Antigravity, OpenCode, Codex, and other agents using semantic capability primitives.

---

## 2. Capability Negotiation Matrix

Every host runtime provides a distinct subset of tools. Paddlr maps all runtime interactions to semantic operational primitives.

Core v1 establishes a strict Single-Agent baseline. `agent.delegate` and `scheduler.loop` are kept out of the required Core v1 runtime capability set. A Single-Agent runtime providing only the 5 mandatory primitives (`fs.read`, `fs.write`, `fs.patch`, `shell.exec`, `search.find`) is fully compliant with Paddlr Core v1; it does not need to implement `agent.delegate` or `scheduler.loop`.

| Semantic Primitive | Capability Category | Core v1 Requirement | Description | Runtime Mappings (Claude Code / Antigravity / Cursor / OpenCode) | Fallback Strategy if Unsupported |
|---|---|---|---|---|---|
| `fs.read` | Filesystem | **Required (Mandatory)** | Read file contents by path. | `View`, `read_file`, Composer file read | Mandatory. Runtime without file I/O cannot execute Paddlr. |
| `fs.write` | Filesystem | **Required (Mandatory)** | Create or overwrite whole file. | `Edit` (new), `write_file`, File write | Mandatory. Runtime without file I/O cannot execute Paddlr. |
| `fs.patch` | Filesystem | **Required (Mandatory)** | Apply contiguous replacement. | `Edit`, `edit_file`, Composer edit | Mandatory. Fall back to `fs.write`. |
| `shell.exec` | Shell | **Required (Mandatory)** | Run shell commands in workspace. | `Bash`, `run_command`, Terminal command | Mandatory. Runtime without command execution cannot verify work. |
| `search.find` | Discovery | **Required (Mandatory)** | Search paths and content regexes. | `GlobTool`/`GrepTool`, `glob`/`grep`, find | Fall back to `shell.exec` (`git ls-files`, `findstr`, Python). |
| `model.steer` | Reasoning Tier | **Optional Enhancement** | Select model reasoning tier. | Model flags, `Model: "..."`, pstack | Fall back to runtime's default active model. |
| `ui.prompt` | User Interface | **Optional Enhancement** | Multiple-choice interactive prompt. | `AskQuestion`, `ask_question`, UI prompt | Fall back to plain-text turn prompt. |
| `agent.delegate`| Multi-Agent | **Deferred (Phase 4)** | Spawn isolated worker agent. | `Task`, `invoke_subagent`, subagent | Not required for Core v1. Single-agent runtimes do not implement. |
| `scheduler.loop`| Automation | **Deferred (Phase 6)** | Automated background loops. | `/loop`, `schedule`, cron | Not required for Core v1. Single-agent runtimes do not implement. |

---

## 3. Capability Abstraction Definitions

### 1. File Operations & Search (`fs.read`, `fs.write`, `fs.patch`, `search.find`)
Playbooks assume standard POSIX/Windows filesystem operations. Tool invocations must never hardcode proprietary arguments (e.g. Cursor-specific worktree flags).

### 2. Subagent Delegation (`agent.delegate`) - Deferred (Phase 4)
In Core v1, the Main Agent executes all workflows in its own context by invoking Skills directly. A Single-Agent runtime does not need to implement `agent.delegate`. When worker delegation is introduced in Phase 4:
1. **If Subagent Dispatch is Supported:**
   - The Main Agent constructs a `DelegationBrief`.
   - The runtime adapter spawns the worker in an isolated directory or worktree.
   - The worker returns its patch and verification log to the Main Agent.
2. **If Subagent Dispatch is Unsupported (Fallback):**
   - The Main Agent executes the delegation brief sequentially in-thread.
   - The Main Agent brackets the step: inspect baseline -> apply patch -> verify -> proceed.

### 3. Model Profile Steering (`model.steer`) - Optional
In Paddlr, playbooks specify abstract model profiles:
- `deep-reasoning`: Complex architecture design, contested red-teaming, root cause diagnosis.
- `standard-code`: Feature implementation, test-driven development, standard refactoring.
- `fast-mechanical`: Bulk linting, formatting passes, typo corrections.

**Core Invariant:** Model profiles are **strictly optional**. If the host runtime does not support steering models per turn or subagent, the adapter ignores the profile hint and executes on the runtime's default model without failure.

### 4. Background Scheduling & Looping (`scheduler.loop`) - Deferred
Unattended execution loops (such as Cursor's `/loop` command) are deferred beyond the initial Paddlr Core.
- Paddlr Core introduces no background daemon or external process supervisor.
- In-turn bounded retries (1–2 attempts) for transient flakes are standard core debugging.
- When an operation requires multi-turn execution without an automated loop tool, the agent executes bounded atomic slices, commits state to `docs/paddlr/plans/`, and returns control to the user.

---

## 4. Target Runtime Adapter Profiles

### Profile 1: Claude Code
- **Capabilities:** Full file I/O (`View`, `Edit`), bash execution (`Bash`), glob/grep search (`GlobTool`, `GrepTool`), subagent dispatch (`Task`).
- **Adapter Mapping:** Native command execution; optional subagents; model steering unsupported (runs on active Claude model).

### Profile 2: Cursor
- **Capabilities:** Full file I/O, terminal execution, subagent dispatch, workspace worktrees.
- **Adapter Mapping:** Decoupled from `cursor-team-kit` and `/loop`. Operates using standard tools and Git worktrees.

### Profile 3: Antigravity
- **Capabilities:** Full file I/O (`read_file`, `write_file`, `edit_file`), PowerShell/Bash command execution (`run_command`), subagent delegation (`invoke_subagent`), background scheduling (`schedule`).
- **Adapter Mapping:** Native subagent delegation; model profile steering via `Model: "inherit"|"pro"|"flash"`.

### Profile 4: OpenCode / Codex
- **Capabilities:** File I/O, CLI execution, standard shell search.
- **Adapter Mapping:** Operates in single-agent sequential fallback mode; full core contracts preserved.
