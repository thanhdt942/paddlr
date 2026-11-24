# Paddlr v1.2.0 — Spec-Driven Autonomy, ADR Closure & Craft Upgrade Specification

**Status:** Approved
**Owner:** thanhdt942
**Last updated:** 2026-11-24
**Related:**
- Handoff: [paddlr-v1.2-handoff.md](file:///home/tanthanh/.gemini/antigravity/brain/b562ba66-1881-4c4f-99ae-4409f81bf46d/paddlr-v1.2-handoff.md)
- Prior Evolution Spec: [2026-11-23-paddlr-mode-evolution.md](2026-11-23-paddlr-mode-evolution.md)
- Repository Rules: [rules/AGENTS.md](../../../rules/AGENTS.md)
- Core Contracts: [skills/paddlr-mode/references/core-contracts.md](../../../skills/paddlr-mode/references/core-contracts.md)

---

## 1. Overview

Paddlr v1.2.0 consolidates Paddlr as a **standalone, agent-agnostic software engineering plugin** (Cursor, Claude Code, OpenAI Codex, Google Antigravity, OpenCode) that unites:

1. **Paddlr's Spec-Driven Design (SDD) & Project Memory:** Durable specs (`specs/`), contract-first plans (`plans/`), immutable architectural decision records (`decisions/`, `DECISIONS.md`), and living project context (`PROJECT.md`), with optional path customization via `.paddlr.json`.
2. **Reversibility-First Autonomy & Live Execution Discipline:** Eliminating unnecessary human approval bottlenecks on reversible Level 2 branch work, synchronizing canonical plans with native IDE/CLI todo trackers (`ui.todo`), closing the ADR and documentation-drift loop (`writing-decisions`, `sync-docs`, `why`), expanding the lazy-loaded principle library to 26 principles, porting high-signal engineering craft skills (`no-comments`, `unslop`, `correct`), and shipping a user-facing `docs/guide/` handbook.

---

## 2. Problem & Context

Inspection of the current `dev` branch (`v1.1.0`, commit `69552c1`, 48 valid skills, 52 passing tests) reveals six concrete gaps that create friction or inconsistency for users and AI agents:

1. **Conflicting Autonomy Rules:** `skills/paddlr-mode/SKILL.md` includes `principle-never-block-on-the-human`, while `rules/AGENTS.md`, `core-contracts.md` (Contract 6), and `tests/test_workflow_scenarios.py` still require pre-code approval on routine Level 2 features. Agents receive contradictory signals about when to proceed vs. pause.
2. **Rigid Project Memory Paths:** All skills and rules hardcode `docs/paddlr/` without a standard mechanism for repositories that already store ADRs or plans elsewhere (e.g., `docs/adr/` or `.local/plans/`).
3. **No Live Checklist Sync Contract:** Plans in `docs/paddlr/plans/` are durable across sessions, but `runtime-adapters.md` lacks a semantic primitive (`ui.todo`) to mirror active steps into each host's native task-progress UI (`TodoWrite`, `update_steps`, `update_plan`, `todowrite`).
4. **Incomplete ADR & Doc-Sync Lifecycle:** `writing-specs` references `adr-guide.md`, and `why` reads `decisions/`, but there is no standalone `writing-decisions` (`/adr`) skill to create/supersede ADRs, no `sync-docs` gate before opening a PR to prevent spec/ADR drift, and `why` does not explicitly read `docs/paddlr/specs/`.
5. **Leftover Drift & Overlapping Skill Boundaries in `paddlr-mode`:**
   - `skills/paddlr-mode/SKILL.md:11` still contains a leftover `poteto-agent` reference instead of `paddlr-worker`.
   - `skills/paddlr-mode/SKILL.md:100` implies mandatory plan creation for all playbooks, contradicting the Level 1 exemption in `task-state-schema.md` and `rules/AGENTS.md`.
   - Boundaries between `feature-development` vs. `playbooks/feature.md`, `sre-debugging` vs. `playbooks/bug-fix.md`, and `code-review` vs. `interrogate` are implicit rather than explicitly stated.
6. **Missing Craft Skills & User Onboarding Handbook:** High-leverage code/writing/self-correction skills (`no-comments`, `unslop`, `correct`) and a structured user-facing handbook (`docs/guide/`) are not yet present in Paddlr.

---

## 3. Goals & Success Metrics

| Goal | Measurable Indicator |
|---|---|
| **G1. Consistent Reversibility-First Autonomy** | `rules/AGENTS.md`, `core-contracts.md`, `paddlr-mode/SKILL.md`, and `tests/test_workflow_scenarios.py` express identical Level 1 / Level 2 / Level 3 / Hard-Stop rules with zero contradictions. |
| **G2. Configurable Project Memory** | Default root remains `docs/paddlr/`; optional `.paddlr.json` override contract is documented and validated by unit tests. |
| **G3. Agent-Agnostic Live Checklist Sync** | `ui.todo` primitive is defined in `runtime-adapters.md` and `core-contracts.md` with mappings for all 5 supported runtimes plus a chat fallback. |
| **G4. Closed SDD & ADR Loop** | `writing-decisions` (`/adr`), `sync-docs` (wired into `opening-a-pr.md`), updated `why`, and 2 new SDD principles (`principle-spec-before-code`, `principle-record-decisions-immutably`, 26 principles total) pass skill validation and tests. |
| **G5. Zero Vendor/Legacy Leaks & Clear Boundaries** | Zero occurrences of `poteto` across `skills/`, `rules/`, `commands/`, `hooks/`, `tests/`, `scripts/`; explicit boundary table in `paddlr-mode/SKILL.md`. |
| **G6. Craft Skills & Handbook** | `no-comments` (with agent-agnostic `comment-sicko` role), `unslop`, `correct`, and `docs/guide/` pass `validate_skills.py`, `unittest`, and `check_markdown_links.py`. |

---

## 4. Scope

### In Scope
1. **Project Memory Path Configuration:** Document default `docs/paddlr/` layout and optional `.paddlr.json` root config schema (`root`, `specs`, `plans`, `decisions`, `decisionsIndex`, `project`) with fallback rules.
2. **Reversibility-First Autonomy Policy:** Update `rules/AGENTS.md`, `rules/CLAUDE.md` (if needed), `core-contracts.md` (Contract 6), `paddlr-mode/SKILL.md`, `playbooks/feature.md`, `playbooks/bug-fix.md`, `worker.md`, and `tests/test_workflow_scenarios.py`.
3. **Two-Tier Checklist Synchronization (`ui.todo`):** Add `ui.todo` to `runtime-adapters.md`, `core-contracts.md`, `task-state-schema.md`, and `paddlr-mode/SKILL.md`.
4. **`paddlr-mode` Cleanup & Disambiguation:**
   - Replace `poteto-agent` with `paddlr-worker` in `skills/paddlr-mode/SKILL.md:11`.
   - Align `skills/paddlr-mode/SKILL.md:100` with Level 1 exemption.
   - Add explicit Skill vs. Playbook boundary guidance (`feature-development` vs. `playbooks/feature.md`; `sre-debugging` vs. `playbooks/bug-fix.md`; `code-review` vs. `interrogate`).
5. **ADR & Doc-Sync Closure:**
   - Add `skills/writing-decisions/SKILL.md` and `commands/adr.md`.
   - Add `skills/sync-docs/SKILL.md` and wire it as a mandatory pre-PR gate in `skills/paddlr-mode/playbooks/opening-a-pr.md`.
   - Update `skills/why/SKILL.md` to inspect `specs/` in addition to `decisions/` and `DECISIONS.md` (respecting `.paddlr.json` overrides) before git history.
6. **Two New SDD Principles (26 total):**
   - Add `skills/principle-spec-before-code/SKILL.md` (`disable-model-invocation: true`).
   - Add `skills/principle-record-decisions-immutably/SKILL.md` (`disable-model-invocation: true`).
   - Index both in `skills/paddlr-mode/SKILL.md`.
7. **Craft Skills Ported & Adapted from `pstack`:**
   - `skills/no-comments/SKILL.md` + `skills/no-comments/comment-sicko.md` (agent-agnostic reviewer prompt supporting both `agent.delegate` and single-agent fallback).
   - `skills/unslop/SKILL.md`.
   - `skills/correct/SKILL.md`.
8. **User-Facing Handbook (`docs/guide/`):**
   - Create concise, agent-agnostic user handbook under `docs/guide/` (`README.md` + focused chapters covering installation/setup, `paddlr-mode`, specs/plans/ADRs, autonomy & verification, principles, playbooks, and `.paddlr.json` customization).
9. **Automated Test Coverage:**
   - Add/update tests in `tests/` covering workflow autonomy rules, `.paddlr.json` contract, 26 principles, new skills/commands, and zero `poteto` leaks.

### Non-goals
- **No runtime CLI daemon or binary:** `.paddlr.json` is a declarative JSON configuration file read by agents/scripts; v1.2.0 does not introduce a compiled CLI or background process.
- **No vendor-locked tool calls:** All new skills (`no-comments`, `writing-decisions`, `sync-docs`, `unslop`, `correct`) must remain agent-agnostic and work in Single-Agent baseline mode without requiring Cursor- or Claude-only tools.
- **No breaking changes to existing plugin manifests:** Claude Code, Antigravity, OpenCode, and Codex plugin structures remain backward-compatible.
- **No release tag / version bump execution in this spec:** Version bumping (`1.1.0` -> `1.2.0`) and release tagging are tracked as an explicit decision/follow-up (see Section 11).

---

## 5. Users & Scenarios

### Primary Users
- **Solo / Team Software Engineers** using Paddlr across Cursor, Claude Code, Codex, Antigravity, or OpenCode.
- **AI Coding Agents** operating under `rules/AGENTS.md` and `skills/paddlr-mode/SKILL.md`.

### Key Scenarios

#### Scenario 1: Reversible Level 2 Feature Without Unnecessary Blocking
- **Actor:** Engineer requesting a standard multi-file feature on a feature branch (e.g., "Add CSV export to the reports module").
- **Precondition:** Requirements are clear; no breaking schema/API changes.
- **Flow:** Agent classifies as Level 2, writes Spec (`docs/paddlr/specs/...`) and Plan (`docs/paddlr/plans/...`), mirrors active steps into `ui.todo`, implements via TDD, verifies on the real surface, runs `sync-docs` and `code-review`, and opens a PR.
- **Expected Outcome:** Agent does **not** stall waiting for pre-code plan approval. The human reviews the complete PR, Spec, and Plan together.

#### Scenario 2: Level 3 Architectural Change With Mandatory Approval Gate
- **Actor:** Engineer requesting a database schema migration or public API breaking change.
- **Flow:** Agent classifies as Level 3, runs `prototype`/`arena` if design unknowns exist, drafts Spec + ADR (`writing-decisions`) + Plan, and **pauses for explicit human approval** before modifying production code.
- **Expected Outcome:** High-impact, hard-to-reverse decisions are reviewed and recorded immutably before code changes occur.

#### Scenario 3: Custom Project Memory Layout via `.paddlr.json`
- **Actor:** Team whose repository already stores ADRs in `docs/adr/` and wants local gitignored plans in `.local/plans/`.
- **Flow:** Team adds `.paddlr.json` at repo root overriding `decisions` and `plans`. Agent reads `.paddlr.json` during Step 1 (Inspect & Understand) and writes ADRs to `docs/adr/` and plans to `.local/plans/`, while `specs` defaults to `docs/paddlr/specs/`.
- **Expected Outcome:** Zero path collisions with existing repo docs; all Paddlr skills (`writing-specs`, `writing-plans`, `writing-decisions`, `why`, `sync-docs`) honor the override.

#### Scenario 4: Pre-PR Doc-Sync Gate Catches Spec/ADR Drift
- **Actor:** Agent finishing implementation and invoking `playbooks/opening-a-pr.md`.
- **Flow:** Before opening the PR, agent runs `sync-docs` against the branch diff. It detects that a public config key changed from what the Spec recorded.
- **Expected Outcome:** Agent updates the Spec (or drafts a superseding ADR if architectural) before opening the PR, keeping code and project memory aligned.

#### Scenario 5: Level 1 Small Bug Fix Without Plan Bloat
- **Actor:** Engineer reporting a localized single-file bug.
- **Flow:** Agent classifies as Level 1, skips Spec and Plan creation, copies playbook steps into `ui.todo`, runs `bug-fix.md` (`sre-debugging` + TDD repro), verifies on the real surface, and reports verbatim evidence.
- **Expected Outcome:** Fast, lightweight execution with no unnecessary files created in `docs/paddlr/plans/`.

---

## 6. Requirements

### Functional Requirements

- **FR-001 (Project Memory Default & Override Schema):** Paddlr **must** default all project memory artifacts to `docs/paddlr/` (`specs/`, `plans/`, `decisions/`, `DECISIONS.md`, `PROJECT.md`) and **must** support an optional `.paddlr.json` file at the target repository root with optional string keys: `root`, `specs`, `plans`, `decisions`, `decisionsIndex`, and `project`. Unspecified keys **must** inherit from `root` (default `docs/paddlr`).
- **FR-002 (Reversibility-First Autonomy Policy):** Paddlr **must** enforce a unified 4-tier autonomy policy across `rules/AGENTS.md`, `core-contracts.md`, and `paddlr-mode/SKILL.md`:
  - **Level 1 (Small / localized):** No Spec, no Plan; execute playbook directly.
  - **Level 2 (Standard feature, reversible on branch/worktree):** Author Spec + Plan in project memory and proceed directly through implementation, verification, and PR creation without blocking for approval, unless product/UX ambiguity cannot be settled by code/prototyping or the user explicitly asks to review the plan first.
  - **Level 3 (Architectural, hard to reverse, schema/public API breaking, or multi-PR):** Prototype/arena unknowns if present, author Spec + ADR + Plan, and **pause for explicit approval** before modifying code.
  - **Hard Stops (Always Pause):** Production deploys, persistent data deletion, force-push to shared branches, and messages to external channels.
  - **Session Overrides:** Explicit user directives ("don't stop", "run until done") allow continuing reversible branch work while still recording decisions in Plan/ADR; hard stops remain in effect unless explicitly authorized.
- **FR-003 (`ui.todo` Semantic Primitive & Sync Rule):** `runtime-adapters.md` and `core-contracts.md` **must** define `ui.todo` as an optional enhancement primitive mapped to: Cursor/Claude Code (`TodoWrite`), Antigravity (`update_steps`), Codex CLI (`update_plan`), OpenCode (`todowrite`), and fallback (compact progress list in chat replies at phase boundaries). `task-state-schema.md` and `paddlr-mode/SKILL.md` **must** specify that canonical plans remain the source of truth, active steps are copied into `ui.todo`, and items are marked `- [x]` / `done` only after verification.
- **FR-004 (`writing-decisions` Skill & `/adr` Command):** Paddlr **must** provide `skills/writing-decisions/SKILL.md` (with `disable-model-invocation: true`) and `commands/adr.md` defining how to create new ADRs (`XXXX-<slug>.md`), maintain the master index (`DECISIONS.md`), and supersede prior ADRs immutably (`Superseded by ADR-YYYY`) while respecting `.paddlr.json`.
- **FR-005 (`sync-docs` Skill & Pre-PR Gate):** Paddlr **must** provide `skills/sync-docs/SKILL.md` (with `disable-model-invocation: true`) that compares the current branch diff against active `specs/`, `decisions/`, and `PROJECT.md` to detect drift, and `playbooks/opening-a-pr.md` **must** invoke `sync-docs` as a mandatory pre-PR quality gate.
- **FR-006 (`why` Skill Alignment):** `skills/why/SKILL.md` **must** inspect `decisions/` + `DECISIONS.md` AND `specs/` (respecting `.paddlr.json` overrides) before falling back to git history (`git log`, `git blame`).
- **FR-007 (Two New SDD Principles):** Paddlr **must** add `skills/principle-spec-before-code/SKILL.md` (Level 2+ spec before implementation) and `skills/principle-record-decisions-immutably/SKILL.md` (append-only ADRs, supersede rather than overwrite), both with `disable-model-invocation: true`, and index them in `skills/paddlr-mode/SKILL.md` for a total of 26 principles.
- **FR-008 (`paddlr-mode` Cleanup & Boundary Disambiguation):** `skills/paddlr-mode/SKILL.md` **must**:
  - Replace `poteto-agent` on line 11 with `paddlr-worker`.
  - Explicitly state the Level 1 exemption from plan creation on line 100.
  - Include a concise boundary table distinguishing `feature-development` vs. `playbooks/feature.md`, `sre-debugging` vs. `playbooks/bug-fix.md`, and `code-review` vs. `interrogate`.
- **FR-009 (Craft Skills — `no-comments`, `unslop`, `correct`):** Paddlr **must** add:
  - `skills/no-comments/SKILL.md` + `skills/no-comments/comment-sicko.md` (agent-agnostic: uses `agent.delegate` when available, otherwise executes the `comment-sicko.md` persona/checklist in-thread; uses repo default base branch instead of hardcoding `main`).
  - `skills/unslop/SKILL.md` (prose de-slopping rules with stable rule IDs).
  - `skills/correct/SKILL.md` (structural mistake-prevention workflow: architecture -> types/lint -> tests -> rules).
- **FR-010 (User-Facing Handbook `docs/guide/`):** Paddlr **must** include a concise, agent-agnostic `docs/guide/` handbook covering installation/setup, `paddlr-mode`, SDD artifacts (specs, plans, ADRs, `.paddlr.json`), autonomy & verification, principles, and playbooks, linked from `README.md`.

### Business Rules & Constraints

- **BR-001 (Immutable ADRs):** Accepted ADRs **must** never be rewritten or deleted; changes require a new ADR that supersedes the prior record.
- **BR-002 (Single Canonical State):** `ui.todo` is strictly an ephemeral session mirror. The Markdown plan file (`docs/paddlr/plans/YYYY-MM-DD-<slug>.md` or `.paddlr.json` override) remains the single canonical Task State.
- **CON-001 (Agent-Agnostic Portability):** No skill in `skills/` may hardcode vendor-specific tool names (e.g., `Task`, `TodoWrite`, `update_steps`) as mandatory requirements outside `runtime-adapters.md`.
- **CON-002 (Zero External Dependencies):** All validation scripts and unit tests **must** remain Python 3.10+ standard-library only.
- **CON-003 (CI & Link Conformance):** All changes **must** pass `python scripts/validate_skills.py --verbose`, `python -m unittest discover -s tests -v`, and `python scripts/check_markdown_links.py`.
- **CON-004 (Lazy-Loading Budget):** All newly added principles and specialized utility skills (`writing-decisions`, `sync-docs`, `no-comments`, `unslop`, `correct`) **must** set `disable-model-invocation: true` in YAML frontmatter to avoid bloating default model context.

---

## 7. UX & Expected Behavior

### `.paddlr.json` Configuration Format
Optional file at the target repository root:

```json
{
  "root": "docs/paddlr",
  "specs": "docs/paddlr/specs",
  "plans": "docs/paddlr/plans",
  "decisions": "docs/paddlr/decisions",
  "decisionsIndex": "docs/paddlr/DECISIONS.md",
  "project": "docs/paddlr/PROJECT.md"
}
```

- All fields are optional.
- If `.paddlr.json` does not exist, all paths default to `docs/paddlr/...`.
- If only `root` is set (e.g., `"root": ".paddlr-docs"`), omitted sub-paths resolve relative to `root`.
- If a specific sub-path is set (e.g., `"decisions": "docs/adr"`), it overrides only that path.

### Skill vs. Playbook Boundary Matrix (to be added in `paddlr-mode/SKILL.md`)

| Concern | Playbook (`paddlr-mode/playbooks/*`) | Standalone Skill (`skills/*`) | When to Use Each |
|---|---|---|---|
| **Feature Delivery** | `playbooks/feature.md` (end-to-end orchestration: throughput checkpoint, autonomy, PR) | `feature-development` (5-phase SDD lifecycle checklist) | `playbooks/feature.md` is the entry point in Paddlr Mode; it invokes `feature-development` for the 5-phase lifecycle. |
| **Debugging** | `playbooks/bug-fix.md` (repro, TDD repro commit, PR) | `sre-debugging` (4-phase scientific root-cause methodology) | `playbooks/bug-fix.md` orchestrates the fix and PR; it invokes `sre-debugging` during diagnosis. |
| **Review** | — | `code-review` (spec alignment, quality, maintainability audit) vs. `interrogate` (adversarial red-teaming; findings survive only with empirical repro) | Run `code-review` on every PR; run `interrogate` on high-risk, security-sensitive, or contested designs. |

---

## 8. Acceptance Criteria

- **AC-001 (Links to FR-001):**
  - *Given* a repository with no `.paddlr.json`, *When* an agent resolves project memory paths, *Then* all paths resolve under `docs/paddlr/`.
  - *Given* a repository with `.paddlr.json` setting `{"decisions": "docs/adr", "plans": ".local/plans"}`, *When* an agent resolves paths, *Then* ADRs resolve to `docs/adr/`, plans to `.local/plans/`, and `specs` defaults to `docs/paddlr/specs/`.
- **AC-002 (Links to FR-002):**
  - *Given* a reversible Level 2 multi-module feature with clear requirements, *When* classified by `WorkflowClassificationEngine` and `rules/AGENTS.md`, *Then* `requires_formal_spec=True`, `requires_implementation_plan=True`, and `requires_approval_before_code=False`.
  - *Given* an ambiguous Level 2 feature OR any Level 3 architectural change, *When* classified, *Then* `requires_approval_before_code=True`.
- **AC-003 (Links to FR-003):**
  - *Given* `skills/paddlr-mode/references/runtime-adapters.md`, *When* inspected, *Then* `ui.todo` is present in the Capability Negotiation Matrix with mappings for Cursor/Claude Code (`TodoWrite`), Antigravity (`update_steps`), Codex (`update_plan`), OpenCode (`todowrite`), and chat fallback.
- **AC-004 (Links to FR-004, FR-005, FR-006):**
  - *Given* the repository skills and commands directories, *When* `python scripts/validate_skills.py` and `python -m unittest discover -s tests` run, *Then* `writing-decisions`, `sync-docs`, `why`, and `commands/adr.md` exist, pass validation, `opening-a-pr.md` references `sync-docs`, and `why/SKILL.md` references `specs/`.
- **AC-005 (Links to FR-007):**
  - *Given* `skills/principle-*`, *When* counted and cross-checked against `skills/paddlr-mode/SKILL.md`, *Then* exactly 26 `principle-*` skills exist, all have `disable-model-invocation: true`, and all 26 are indexed in `paddlr-mode/SKILL.md`.
- **AC-006 (Links to FR-008):**
  - *Given* the entire repository (`skills/`, `rules/`, `commands/`, `hooks/`, `tests/`, `scripts/`), *When* searched for `poteto`, *Then* zero matches are returned; `paddlr-mode/SKILL.md` references `paddlr-worker`, states the Level 1 plan exemption, and includes the Skill vs. Playbook boundary table.
- **AC-007 (Links to FR-009, FR-010, CON-003):**
  - *Given* `no-comments`, `unslop`, `correct`, and `docs/guide/`, *When* `scripts/validate_skills.py`, `unittest`, and `scripts/check_markdown_links.py` run, *Then* all three exit with code `0` and zero errors.

---

## 9. Edge Cases & Error Handling

- **Malformed `.paddlr.json`:** If `.paddlr.json` contains invalid JSON or non-string path values, agents must halt with a clear diagnostic error rather than silently writing to unintended paths.
- **Path traversal in `.paddlr.json`:** Paths escaping the repository root (e.g., `../outside`) must be rejected.
- **Single-Agent fallback for `no-comments`:** If the host runtime does not support `agent.delegate`, `no-comments` must execute the `comment-sicko.md` review pass directly in-thread rather than failing on a missing `Task` tool.
- **Empty `docs/paddlr/specs/` or `decisions/` during `sync-docs`:** On Level 1 changes or repositories that have not yet created specs/ADRs, `sync-docs` reports "No active specs/ADRs affected" cleanly instead of failing.
- **Pre-existing uncommitted changes on `dev`:** Currently `skills/code-review/SKILL.md` and `skills/feature-development/SKILL.md` have uncommitted `disable-model-invocation: true` edits. Implementation must preserve those edits (do not revert or overwrite them).

---

## 10. Confirmed Technical Decisions & Design Choices

All decisions below were confirmed in the handoff ([paddlr-v1.2-handoff.md](file:///home/tanthanh/.gemini/antigravity/brain/b562ba66-1881-4c4f-99ae-4409f81bf46d/paddlr-v1.2-handoff.md)):

1. **Decision:** Keep `docs/paddlr/` as default project memory root, with optional `.paddlr.json` override at target repo root.
   - **Rationale:** Avoids colliding with existing `docs/` folders in user repos, stays `.gitignore`-friendly in 1 line, and preserves backward compatibility with v1.1.0 tests and rules.
   - **Declined Alternatives:** Moving defaults to `docs/specs/` (collision risk) or `.paddlr/` hidden folder (less discoverable for human reviewers).
2. **Decision:** Adopt Reversibility-First Autonomy (Level 1 direct; Level 2 reversible proceeds without blocking; Level 3 and hard stops pause for approval).
   - **Rationale:** Eliminates unnecessary human wait loops on reversible branch work while preserving strict review gates for architectural/irreversible changes.
   - **Declined Alternatives:** Mandatory human approval on every Level 2 task (too slow) or fully autonomous Level 3 execution (too risky).
3. **Decision:** Two-tier checklist synchronization (`docs/paddlr/plans/` canonical + `ui.todo` optional runtime primitive).
   - **Rationale:** Combines git-tracked cross-session durability with live IDE/CLI progress visibility across all 5 supported agents.
   - **Declined Alternatives:** Dropping Markdown plans in favor of IDE todos (loses cross-session durability) or ignoring native todo UIs (poor UX).
4. **Decision:** Keep all 24 existing lazy-loaded principles and add 2 SDD principles (`principle-spec-before-code`, `principle-record-decisions-immutably`) = 26 total.
   - **Rationale:** Minimal context cost thanks to `disable-model-invocation: true`, while encoding Paddlr's core SDD discipline as first-class principles.
   - **Declined Alternatives:** Pruning existing principles (loses proven discipline) or embedding full SDD prose directly in `paddlr-mode/SKILL.md` (bloats prompt).

---

## 11. Assumptions, Dependencies & Open Questions

### Provisional Assumptions (Please Confirm)
1. **Craft Skills Inclusion (`no-comments`, `unslop`, `correct`):** Included in v1.2.0 scope (Task 7). Confirm if you want all three included in this release or deferred.
2. **User-Facing Handbook (`docs/guide/`):** Included in v1.2.0 scope as a concise 6–7 chapter guide modeled on `pstack/docs/guide/` (Task 8). Confirm if you want this in the same PR/batch or as a follow-up PR.
3. **Version Bump (`1.1.0` -> `1.2.0`):** Assumed to be done via `release-management` *after* all v1.2.0 feature tasks are merged/verified, rather than bumping manifests prematurely during feature implementation.
4. **Uncommitted `disable-model-invocation: true` Edits:** `skills/code-review/SKILL.md` and `skills/feature-development/SKILL.md` currently have uncommitted `disable-model-invocation: true` lines on `dev`. Assumed intentional and to be preserved.
