# Paddlr Mode Evolution Specification

**Status:** Proposed  
**Type:** Architecture & Migration Planning  
**Target:** Transform the inherited Poteto Mode into Paddlr Mode  
**Execution mode:** Research, analysis, architecture design, and planning only  
**Implementation:** Not authorized by this specification

---

## 1. Objective

Evolve the existing `poteto-mode` into `paddlr-mode`, the orchestration entry point of Paddlr, an agent-agnostic engineering system.

Paddlr should preserve the proven engineering philosophy, orchestration patterns, principles, playbooks, and skills inherited from Poteto while improving the system in areas that require stronger architectural definitions.

The goal is not to rewrite Poteto or create a completely new engineering framework.

The goal is to:

1. Understand the existing Poteto architecture and its actual implementation.
2. Identify what should be reused, adapted, removed, or added.
3. Define the architectural identity and boundaries of Paddlr.
4. Design the target architecture for `paddlr-mode`.
5. Produce a detailed, incremental migration and development plan.
6. Establish verifiable acceptance criteria for each development phase.

**The deliverable is an actionable development plan, not an implementation.**

## 2. Project Context

Paddlr is an Agent-Agnostic Engineering System.

It aims to provide a consistent engineering methodology across different AI coding agents, without making the orchestration logic dependent on a particular runtime.

The existing `poteto-mode` has been copied into the Paddlr repository as the starting point.

Poteto provides valuable existing capabilities, including:

- Single entry point for engineering tasks.
- Task classification and Playbook selection.
- Conditional Skill invocation.
- Engineering principles.
- Main Agent ownership.
- Subagent delegation.
- Verification and evidence-oriented execution.
- Session continuity and recovery workflows.
- Specialized engineering Skills and Playbooks.

Paddlr should build on these capabilities rather than replace them without justification.

The actual local repository is the source of truth. Do not assume that its contents match the latest public version of Poteto.

## 3. Confirmed Architectural Decisions

The following decisions have already been made. Treat them as constraints unless repository evidence reveals a fundamental incompatibility. If such a conflict exists, document it and explain the consequences rather than silently changing the decision.

### 3.1 Runtime Architecture: Core-first

Paddlr must have a runtime-independent orchestration core.

The core defines engineering behavior, workflow rules, task management, and execution contracts.

Runtime-specific capabilities must be isolated behind an adapter or an equivalent integration boundary.

Target runtimes may include:

- Claude Code
- Cursor
- Antigravity
- Other compatible coding agents

Do not assume that all runtimes support identical capabilities.

The architecture must distinguish:

- Core requirements.
- Runtime-provided capabilities.
- Optional capabilities.
- Unsupported capabilities.
- Fallback behavior.

Do not introduce an abstraction merely because two tools have different names. Introduce a boundary when their behavior, lifecycle, or guarantees actually differ.

### 3.2 Principles: Adapt

Retain the existing 24 Poteto Principles as the initial foundation.

Do not replace them with an entirely new collection.

Review each principle and determine whether it should be:

- Reused without changes.
- Adapted for agent-agnostic behavior.
- Extended with additional guidance.
- Deprecated, only when there is a demonstrated reason.

Preserve the original intent and attribution of inherited principles.

Do not claim that Paddlr invented principles inherited from Poteto.

If additional principles are proposed, explain the gap they address and why existing principles cannot address it.

Principles remain independent Skills at the repository level. Do not create a `principles/` directory inside `paddlr-mode`.

### 3.3 Task State: Explicit

Paddlr must have an explicit model of task state.

Do not rely exclusively on conversation history, implicit agent context, or a loosely maintained todo list.

The design must investigate and define:

- Task identity.
- User intent.
- Task classification.
- Selected workflow.
- Current phase and step.
- Completed and pending work.
- Decisions and assumptions.
- Dependencies.
- Delegated workers.
- Artifacts.
- Verification status and evidence.
- Pause, interruption, failure, and recovery information.

The design must distinguish task state from runtime execution state and long-lived project knowledge.

Do not assume that these must be implemented as separate files or storage systems. Choose the simplest representation that satisfies the requirements.

### 3.4 Directory Convention

Preserve the existing Skill organization convention.

The expected logical structure is:

```text
paddlr/
└── skills/
    ├── paddlr-mode/
    │   ├── SKILL.md
    │   └── playbooks/
    │
    ├── principle-laziness-protocol/
    │   └── SKILL.md
    │
    ├── principle-foundational-thinking/
    │   └── SKILL.md
    │
    ├── in-your-own-words/
    │   └── SKILL.md
    │
    ├── how/
    │   └── SKILL.md
    │
    └── tdd/
        └── SKILL.md
```

This is a logical convention, not an instruction to force every runtime to use the same packaging format.

Important rules:

- `paddlr-mode` is an independent Skill and the main orchestrator.
- Playbooks remain inside `paddlr-mode`.
- Principle Skills remain independent and at the same directory level as `paddlr-mode`.
- Other reusable Skills also remain independent.
- Do not create `paddlr-mode/principles/`.
- Do not create `paddlr-mode/skills/`.
- Do not move Playbooks into independent top-level Skills unless a demonstrated architectural requirement justifies the change.

The exact placement of internal contracts, runtime documentation, and protocols must be determined during architecture design. Do not create directories solely to make the structure look more layered.

---

## 4. Core Design Goals

The target Paddlr architecture should satisfy the following goals.

### DG-01: Preserve Proven Engineering Practices

Retain effective Poteto behavior.

Do not redesign a working component without identifying a concrete limitation or requirement that justifies the change.

### DG-02: Agent-Agnostic Orchestration

Separate orchestration decisions from runtime-specific tool invocation.

The same engineering intent and workflow should remain valid across supported runtimes, even when the execution mechanisms differ.

### DG-03: Explicit Intent Understanding

The system must distinguish:

- What the user wants to achieve.
- What problem they are trying to solve.
- Constraints and preferences.
- The proposed implementation.
- Conditions that define successful completion.

The system must not blindly interpret a proposed solution as the user's actual goal.

For clear requests, the agent should proceed without unnecessary confirmation.

### DG-04: Explicit Task Lifecycle

A task must have a recognizable lifecycle.

The design must account for normal execution, completion, pause, interruption, blocking, failure, and recovery.

The agent must not report completion merely because it has finished generating a response or stopped executing tools.

### DG-05: Controlled Delegation

Main Agent ownership must remain explicit.

Delegated workers must receive bounded responsibilities and sufficient context.

Delegation must define ownership, expected outputs, dependencies, and verification responsibilities.

The Main Agent remains accountable for the overall result.

### DG-06: Evidence-Based Verification

Important completion claims must be supported by evidence.

The system must distinguish:

- Verified results.
- Unverified results.
- Inferred conclusions.
- Unsupported assumptions.
- Known limitations.

Verification must apply to the actual artifact and relevant final state.

### DG-07: Recoverable Execution

An interrupted task must be recoverable from explicit state.

A new agent should be able to understand what happened, what remains, what decisions have been made, and what must be verified before continuing.

### DG-08: Minimal Architectural Complexity

Do not overengineer the system.

Prefer the smallest architecture that satisfies the requirements.

Do not introduce a workflow engine, database, runtime SDK, configuration framework, or additional abstraction unless repository evidence and actual requirements justify it.

---

## 5. Required Investigation

Before proposing the target architecture, audit the actual repository.

### 5.1 Repository Inventory

Inspect:

- Existing directory structure.
- `poteto-mode/SKILL.md`.
- All Playbooks.
- All 24 Principle Skills.
- Other Skills referenced by Poteto Mode.
- Shared instructions and supporting documents.
- Runtime-specific configuration and integrations.
- References between files.
- External tools, commands, and assumptions.

Produce a complete inventory.

For every component, record:

| Field | Description |
|---|---|
| Name | Component or file name |
| Type | Mode, Playbook, Principle, Skill, contract, or runtime integration |
| Purpose | What it does |
| Dependencies | Other files, tools, or runtime capabilities it requires |
| Runtime coupling | None, partial, or strong |
| Current behavior | What the actual instructions require |
| Migration decision | Reuse, Adapt, Remove, or Defer |
| Rationale | Why this decision was made |

Do not classify a component based only on its name. Read its actual content and relevant dependencies.

### 5.2 Runtime Dependency Audit

Identify every instruction that assumes a specific runtime.

Examples include:

- Tool names.
- Subagent APIs.
- Background execution.
- Worker creation and resumption.
- Todo management.
- File access.
- Command execution.
- Session persistence.
- Approval and authorization behavior.
- Runtime-specific metadata.
- Skill discovery and invocation.

For each dependency, determine:

1. What behavior the instruction requires.
2. Whether the behavior is essential to the core.
3. Whether it is provided by the runtime.
4. Whether it needs an adapter.
5. What fallback is possible if unavailable.

Do not assume that replacing tool names is sufficient to make an instruction agent-agnostic.

### 5.3 Orchestration Flow Audit

Trace the actual task lifecycle in Poteto:

```text
User Request
    |
    v
Poteto Mode
    |
    v
Task Classification
    |
    v
Playbook Selection
    |
    v
Conditional Skill Invocation
    |
    v
Execution and Delegation
    |
    v
Verification
    |
    v
Final Report
```

Determine:

- Where decisions are made.
- Which instructions own each decision.
- How workflow steps are tracked.
- How Skills are selected and invoked.
- How delegation works.
- How failures and retries are handled.
- How session continuity works.
- Which responsibilities are implicit or duplicated.

Document the actual flow rather than assuming the diagram represents every task.

---

## 6. Architecture Design Requirements

After the investigation, design the target architecture.

### AR-01: Define Paddlr Identity

Explain:

- What Paddlr is.
- What problem it solves.
- What it inherits from Poteto.
- What it improves.
- What it intentionally does not attempt to solve.

Provide a concise positioning statement and detailed design goals.

### AR-02: Define Architectural Boundaries

Identify the responsibilities and relationships of:

- Paddlr Mode.
- Orchestration Core.
- Principles.
- Playbooks.
- Independent Skills.
- Main Agent.
- Delegated Workers.
- Runtime Adapters.
- Task State.
- Verification and Recovery.

Do not assume these responsibilities require separate directories or software modules.

Define which component owns each decision.

### AR-03: Define Intent Contract

Specify the minimum information required to understand a task.

Consider:

- Goal.
- Problem.
- Constraints.
- Done criteria.
- Assumptions.
- Ambiguities.
- User authorization boundaries.

Define when the agent should proceed, clarify, or stop.

Do not require a lengthy intent questionnaire for every task.

### AR-04: Define Task State Model

Design an explicit task state schema.

At minimum, investigate:

- Task identity and status.
- Intent.
- Classification.
- Workflow and phase.
- Progress.
- Decisions.
- Dependencies.
- Workers.
- Artifacts.
- Verification.
- Checkpoints.
- Recovery metadata.

Define:

- State ownership.
- Persistence location.
- Update rules.
- State transitions.
- Checkpoint behavior.
- Consistency requirements.
- Concurrent update behavior.
- Recovery after interruption.

The schema must represent meaningful states without introducing unnecessary fields.

### AR-05: Define Task Lifecycle

Design a lifecycle model.

Consider states such as:

- Pending.
- In progress.
- Blocked.
- Paused.
- Interrupted.
- Recovering.
- Completed.
- Failed.
- Cancelled.

These are candidate states, not mandatory final names.

For every accepted state, define:

- Entry conditions.
- Exit conditions.
- Allowed transitions.
- Required state updates.
- Required verification.
- Recovery behavior.

Explicitly distinguish workflow phase from overall task status.

### AR-06: Define Workflow Orchestration

Retain Playbook-driven execution.

Specify:

- Task classification.
- Playbook selection.
- Workflow steps.
- Conditional Skill invocation.
- Phase transitions.
- Verification gates.
- Handling of unmatched tasks.
- Handling of multi-phase work.

Explain the responsibilities of Mode, Playbook, and Skill without duplicating instructions across them.

### AR-07: Define Delegation Contract

Specify the minimum information required when delegating work:

- Goal.
- Scope.
- Constraints.
- Inputs.
- Dependencies.
- Ownership.
- Writable resources.
- Expected outputs.
- Completion criteria.
- Verification requirements.
- Failure and retry handling.

Define:

- When delegation is appropriate.
- When work should remain with Main Agent.
- How worker context is constructed.
- How results are reviewed.
- How conflicting outputs are handled.
- How concurrent changes are isolated.

Do not assume that every runtime supports subagents.

### AR-08: Define Runtime Adapter Contract

Specify a capability-oriented boundary between core instructions and runtime-specific execution.

Investigate capabilities such as:

- Read files.
- Write files.
- Execute commands.
- Search repository.
- Spawn workers.
- Inspect worker status.
- Resume workers.
- Manage task lists.
- Persist state.
- Request authorization.

Classify each capability as:

- Required.
- Optional.
- Runtime-specific.
- Unsupported.

Define graceful degradation and fallback behavior.

Do not require identical runtime implementations.

### AR-09: Define Autonomy Policy

Separate two questions:

1. Can the agent make this decision independently?
2. Is the agent authorized to execute the action?

Consider:

- Reversibility.
- Blast radius.
- External impact.
- Data loss.
- Security implications.
- Cost.
- User authorization.

Define when the agent may proceed autonomously and when it must request authorization.

### AR-10: Define Evidence Contract

Specify what constitutes sufficient evidence for:

- Code changes.
- Tests.
- Builds.
- Runtime behavior.
- Performance claims.
- Delegated work.
- Task completion.

Evidence should identify the relevant artifact, command or observation, outcome, and limitations where applicable.

Where relevant, tie verification to the exact commit or artifact version tested.

### AR-11: Define Recovery Protocol

Specify how to:

- Checkpoint a task.
- Pause safely.
- Resume a task.
- Recover after context loss.
- Detect stale worker state.
- Retry failed operations.
- Avoid duplicate side effects.
- Revalidate state before continuing.

Distinguish recoverable state from runtime-specific process state.

---

## 7. Migration Strategy

Produce a migration mapping for every existing component.

Use exactly four decisions:

### REUSE

Keep the component substantially unchanged.

Explain why its current behavior satisfies Paddlr requirements.

### ADAPT

Preserve its purpose but modify instructions, structure, dependencies, or behavior.

Specify the required changes.

### REMOVE

Remove the component because it is unnecessary, duplicated, obsolete, or incompatible with the target architecture.

Explain the reason and identify affected references.

### DEFER

Keep the component out of the initial development scope.

Explain its future value and why it is not needed yet.

Do not delete or modify anything during this planning task.

### 7.1 Migration Mapping Deliverable

Create a table with:

| Source component | Target location | Decision | Required changes | Dependencies | Priority |
|---|---|---|---|---|---|

Include every relevant Mode, Playbook, Principle, Skill, and runtime-specific component.

### 7.2 Principle Migration

Review all 24 principles individually.

Do not assume that all require changes.

For every principle, document:

- Existing purpose.
- Existing trigger.
- Runtime dependencies, if any.
- Whether its current behavior fits Paddlr.
- Proposed adaptation.
- Reason for the decision.

### 7.3 Playbook Migration

Review every existing Playbook.

Determine whether it:

- Works independently of a particular runtime.
- Depends on runtime-specific tools.
- Needs explicit Task State integration.
- Needs additional verification gates.
- Should be retained, adapted, or deferred.

Keep Playbooks inside `paddlr-mode`.

### 7.4 Independent Skill Migration

Review each independent Skill referenced by Poteto.

Determine:

- Whether it should remain independent.
- Whether it is reusable without Paddlr Mode.
- Whether it has runtime-specific dependencies.
- Whether it needs changes to its interface or invocation instructions.

Keep reusable Skills at the same repository level as `paddlr-mode`.

---

## 8. Development Plan Requirements

Create an incremental development roadmap.

The roadmap must be derived from repository findings and the approved architecture, not copied mechanically from this specification.

At minimum, consider the following development areas:

1. Repository audit and migration inventory.
2. Paddlr identity and architecture.
3. Core contracts and task lifecycle.
4. Paddlr Mode implementation.
5. Playbook and Skill migration.
6. Delegation and runtime independence.
7. Recovery and continuity.
8. Evaluation and hardening.

You may merge, split, reorder, or replace these areas if the investigation justifies a better sequence.

For each phase, define:

| Field | Required information |
|---|---|
| Objective | What the phase achieves |
| Scope | What is included |
| Dependencies | What must exist first |
| Tasks | Concrete implementation tasks |
| Deliverables | Files or artifacts produced |
| Acceptance criteria | Conditions for completion |
| Verification | How the result is proven |
| Risks | Potential problems |
| Exit conditions | When the next phase may begin |

The roadmap must be actionable enough for another coding agent to execute without reconstructing the architecture from scratch.

### Development sequencing rules

- Establish core contracts before depending on them in Playbooks.
- Build the smallest useful Paddlr Mode before migrating every Skill.
- Prioritize behavior and correctness over directory restructuring.
- Avoid migrating runtime-specific workflows before defining capability boundaries.
- Validate each migration unit before proceeding.
- Avoid unnecessary compatibility layers.
- Keep deferred features explicitly out of the initial scope.

---

## 9. Evaluation Strategy

Define how the resulting Paddlr Mode will be evaluated.

At minimum, include these scenarios:

1. Simple bug fix.
2. Feature implementation.
3. Read-only investigation.
4. Refactoring.
5. Ambiguous user request.
6. Multi-step task.
7. Delegated task.
8. Worker failure.
9. Task interruption and recovery.
10. Runtime without delegation support.
11. Verification failure.
12. User changes requirements during execution.

For each scenario, define:

- Initial conditions.
- Expected agent behavior.
- Expected Task State.
- Expected workflow.
- Expected verification.
- Failure conditions.

Include both functional evaluation and orchestration quality.

Do not claim cross-runtime compatibility until the same relevant behavior has been tested on multiple actual runtimes.

---

## 10. Constraints and Non-Goals

### Constraints

- Preserve the agreed directory convention.
- Keep `playbooks/` inside `paddlr-mode`.
- Keep Principle Skills independent and at the same level as `paddlr-mode`.
- Do not create `principles/` inside `paddlr-mode`.
- Do not create `skills/` inside `paddlr-mode`.
- Retain the 24 Poteto Principles as the initial foundation.
- Make explicit Task State part of the target architecture.
- Keep the orchestration core runtime-independent.
- Preserve Main Agent ownership.
- Keep the initial architecture as simple as possible.
- Base migration decisions on actual repository contents.

### Non-Goals for This Task

This task does not authorize:

- Implementing Paddlr Mode.
- Modifying existing Poteto-derived Skills.
- Migrating Playbooks.
- Rewriting Principle Skills.
- Building runtime adapters.
- Building a workflow engine.
- Creating a database or persistent state service.
- Implementing delegation infrastructure.
- Deleting inherited files.
- Changing repository packaging or installation conventions.
- Creating a release or publishing a new version.

These may become future implementation tasks after the plan is reviewed.

---

## 11. Required Deliverables

Produce a coherent planning package.

Use the repository's existing documentation conventions when possible. Do not create duplicate documents if equivalent documentation already exists; update or reference existing artifacts instead.

The planning package must contain the following information, whether as separate files or well-structured sections:

### D-01: Repository Inventory

A complete inventory of the existing Poteto-derived components and their dependencies.

### D-02: Architecture Assessment

A description of the existing architecture, its strengths, limitations, and runtime coupling.

### D-03: Paddlr Architecture Specification

The target architecture, component responsibilities, boundaries, relationships, and design rationale.

### D-04: Core Contracts Specification

Detailed designs for:

- Intent Contract.
- Task State.
- Task Lifecycle.
- Delegation Contract.
- Runtime Adapter Contract.
- Autonomy Policy.
- Evidence Contract.
- Recovery Protocol.

If a contract is unnecessary or should be deferred, explain why.

### D-05: Migration Mapping

A component-by-component mapping from Poteto to Paddlr.

### D-06: Development Roadmap

An ordered, phased implementation plan with dependencies, deliverables, and acceptance criteria.

### D-07: Evaluation Plan

Scenarios and measurable criteria for validating Paddlr.

### D-08: Open Decisions and Risks

A list of unresolved decisions, alternatives, trade-offs, and recommendations.

For every unresolved decision, identify whether it:

- Blocks implementation.
- Can be decided during implementation.
- Can safely be deferred.

---

## 12. Execution Instructions for Poteto Mode

Treat this as a large, cross-cutting architecture and migration planning task.

Use the appropriate Poteto workflow. If no existing Playbook adequately covers the task, use the figure-it-out Skill to design a rigorous investigation and planning workflow. If this is treated as an ongoing multi-phase program, distinguish the planning work from the later implementation program.

### Step 1: Understand

- Restate the objective.
- Identify the smallest useful deliverable.
- Read the relevant Poteto principles before applying them.
- Identify the scope and constraints.
- Do not start modifying implementation files.

### Step 2: Investigate

- Audit the actual repository.
- Read the relevant source files.
- Trace dependencies and runtime assumptions.
- Use bounded parallel investigation where it provides independent coverage.
- Keep Main Agent responsible for consolidating and reviewing findings.

### Step 3: Analyze

- Separate confirmed facts from interpretations.
- Identify architectural strengths worth preserving.
- Identify actual limitations and migration risks.
- Compare alternative designs where a meaningful architectural choice exists.
- Do not add abstractions without a demonstrated need.

### Step 4: Design

- Define the Paddlr target architecture.
- Specify core contracts.
- Define task state and lifecycle.
- Define runtime boundaries.
- Establish migration decisions.
- Resolve dependencies and sequencing.

### Step 5: Plan

- Produce the phased roadmap.
- Define implementation tasks.
- Specify deliverables and acceptance criteria.
- Define verification and evaluation scenarios.
- Identify decisions that require user approval.

### Step 6: Review

Perform an adversarial review of the proposal.

Check for:

- Unnecessary complexity.
- Duplicate responsibilities.
- Hidden runtime dependencies.
- Inconsistent state ownership.
- Missing lifecycle transitions.
- Overly broad delegation.
- Weak verification requirements.
- Migration steps with unresolved dependencies.
- Contradictions with confirmed architectural decisions.
- Scope expansion without justification.

Revise the plan based on findings.

### Step 7: Report

Present:

1. Executive summary.
2. Key findings from the repository audit.
3. What Paddlr should inherit from Poteto.
4. What Paddlr must change and why.
5. Target architecture.
6. Core contract designs.
7. Migration mapping.
8. Phased development roadmap.
9. Evaluation strategy.
10. Open decisions and risks.

Cite concrete file paths and relevant sections as evidence.

Clearly label confirmed facts, recommendations, and unresolved assumptions.

---

## 13. Acceptance Criteria

The planning task is complete only when all of the following are satisfied:

- [ ] The actual repository has been audited.
- [ ] All relevant existing components have been inventoried.
- [ ] Runtime-specific dependencies have been identified.
- [ ] The distinction between Poteto and Paddlr is clearly defined.
- [ ] Confirmed architectural decisions are respected.
- [ ] The target architecture has explicit component responsibilities.
- [ ] Task State and Task Lifecycle have been designed.
- [ ] Core contracts have sufficient detail for implementation.
- [ ] Every inherited component has a migration decision.
- [ ] The 24 Principles have been reviewed individually.
- [ ] Playbook and independent Skill migration has been addressed.
- [ ] The development roadmap has ordered, actionable phases.
- [ ] Each phase has deliverables and acceptance criteria.
- [ ] Evaluation scenarios cover normal and failure paths.
- [ ] Risks and unresolved decisions are documented.
- [ ] The proposal has undergone an adversarial review.
- [ ] No implementation changes have been made.

A polished document without repository evidence does not satisfy these criteria.

A proposed architecture without a migration path does not satisfy these criteria.

A migration plan without verification criteria does not satisfy these criteria.

---

## 14. Final Instruction

Do not implement the proposed architecture yet.

Your responsibility is to produce a technically grounded, internally consistent, and actionable specification and development plan that can be reviewed and approved by the project owner.

Use engineering judgment to determine how Paddlr should evolve from Poteto.

Preserve what works. Change what has a demonstrated reason to change. Add only what the target requirements need.

When finished, provide the planning artifacts, summarize the most important architectural decisions, and identify the decisions that require project-owner approval before implementation begins.