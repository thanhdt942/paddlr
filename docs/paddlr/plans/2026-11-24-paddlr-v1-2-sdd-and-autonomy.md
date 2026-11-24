---
task_id: "pdl-2026-11-24-01"
title: "Paddlr v1.2.0 — Spec-Driven Autonomy, ADR Closure & Craft Upgrade"
classification: 3
status: "completed"
playbook: "multi-phase-plan"
active_phase: "completed"
done_predicate: "All 9 tasks complete; validate_skills.py, unittest discover -s tests, and check_markdown_links.py exit 0 with zero errors."
created_at: "2026-11-24T19:30:00+07:00"
updated_at: "2026-11-24T19:44:00+07:00"
---

# Paddlr v1.2.0 Implementation Plan

> **Execution:** Implement this plan task-by-task after explicit user approval. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade Paddlr to v1.2.0 by unifying reversibility-first autonomy, adding `.paddlr.json` project memory overrides, introducing `ui.todo` checklist sync, closing the ADR/doc-sync loop, adding 2 SDD principles (26 total), cleaning up `paddlr-mode`, porting 3 craft skills, and shipping `docs/guide/`.

**Architecture:** All behavioral upgrades live in declarative Markdown rules, skills, commands, playbooks, and reference contracts under `rules/`, `skills/`, `commands/`, and `docs/guide/`, backed by a zero-dependency Python 3.10+ standard-library helper (`scripts/paddlr_config.py`) and `unittest` test suites under `tests/`. Every new principle and utility skill uses `disable-model-invocation: true` to preserve a minimal default context footprint.

**Tech Stack:** Markdown (Agent Skills open standard), JSON (`.paddlr.json`, plugin manifests), Python 3.10+ stdlib (`unittest`, `pathlib`, `json`, `re`).

**Key Decisions:**
- Default project memory root remains `docs/paddlr/`; optional `.paddlr.json` at target repo root overrides `root`, `specs`, `plans`, `decisions`, `decisionsIndex`, `project`.
- Reversibility-First Autonomy: Level 1 direct (no spec/plan); Level 2 reversible branch work proceeds without pre-code human block; Level 3 architectural/breaking and hard stops always pause for approval.
- Two-tier checklist sync: canonical Markdown plan + optional `ui.todo` runtime primitive.
- 26 lazy-loaded principles (`disable-model-invocation: true`).

**Spec:** [docs/paddlr/specs/2026-11-24-paddlr-v1-2-sdd-and-autonomy.md](../specs/2026-11-24-paddlr-v1-2-sdd-and-autonomy.md)

## Global Constraints

- Agent-agnostic portability: no skill outside `runtime-adapters.md` may require vendor-specific tool names (`Task`, `TodoWrite`, `update_steps`).
- Zero external dependencies: all Python scripts and tests use Python 3.10+ standard library only.
- Lazy-loading budget: all new principles and utility skills (`writing-decisions`, `sync-docs`, `no-comments`, `unslop`, `correct`) set `disable-model-invocation: true`.
- Preserve uncommitted `disable-model-invocation: true` edits in `skills/code-review/SKILL.md` and `skills/feature-development/SKILL.md`.
- Every task must keep `python scripts/validate_skills.py --verbose`, `python -m unittest discover -s tests -v`, and `python scripts/check_markdown_links.py` passing.

## Review Focus

- **Malformed `.paddlr.json` (invalid JSON or non-string field):** Config loader raises `ValueError` with a clear message instead of silently falling back to wrong paths (pinned in Task 1 tests).
- **Path traversal in `.paddlr.json` (e.g. `../outside` or absolute path outside repo):** Config loader rejects paths escaping the repository root with `ValueError` (pinned in Task 1 tests).
- **Ambiguous Level 2 task vs. clear reversible Level 2 task:** `WorkflowClassificationEngine` returns `requires_approval_before_code=False` for clear reversible Level 2, `True` for ambiguous Level 2, and `True` for all Level 3 tasks (pinned in Task 2 tests).
- **Stale `poteto` references or broken principle index links:** Regression test scans `skills/`, `rules/`, `commands/`, `hooks/`, `tests/`, `scripts/` for `poteto` and verifies every `skills/principle-*` directory is indexed in `paddlr-mode/SKILL.md` (pinned in Task 4 & Task 6 tests).
- **Single-agent fallback in `no-comments`:** `skills/no-comments/SKILL.md` explicitly handles runtimes without `agent.delegate` and does not hardcode `Task` or `main` branch (pinned in Task 7 tests).

---

## File Structure Overview

- **Create:**
  - `scripts/paddlr_config.py` — Pure stdlib `.paddlr.json` loader & path resolver with validation.
  - `tests/test_paddlr_config.py` — Unit tests for `.paddlr.json` defaults, partial overrides, malformed JSON, and path traversal rejection.
  - `tests/test_paddlr_v1_2_contracts.py` — Contract tests for `ui.todo`, zero `poteto` leaks, 26 principles index sync, `writing-decisions`, `sync-docs`, `why`, `no-comments`, `unslop`, `correct`, and `docs/guide/`.
  - `skills/writing-decisions/SKILL.md` — Standalone ADR authoring & superseding skill.
  - `commands/adr.md` — `/adr` slash command pointing to `skills/writing-decisions/SKILL.md`.
  - `skills/sync-docs/SKILL.md` — Pre-PR doc-drift check skill.
  - `skills/principle-spec-before-code/SKILL.md` — SDD principle #25.
  - `skills/principle-record-decisions-immutably/SKILL.md` — SDD principle #26.
  - `skills/no-comments/SKILL.md` & `skills/no-comments/comment-sicko.md` — Comment & workaround audit skill.
  - `skills/unslop/SKILL.md` — Prose de-slopping skill.
  - `skills/correct/SKILL.md` — Structural mistake-prevention skill.
  - `docs/guide/README.md` + 6 focused handbook chapters (`01-setup.md` through `06-customization.md`).
- **Modify:**
  - `rules/AGENTS.md` & `rules/CLAUDE.md` — Reversibility-first autonomy + `.paddlr.json` override notice.
  - `skills/paddlr-mode/SKILL.md` — Remove `poteto-agent`, align line 100 Level 1 exemption, add Skill vs. Playbook boundary table, add `ui.todo` sync note, index 2 new SDD principles, align Autonomy section.
  - `skills/paddlr-mode/references/runtime-adapters.md` — Add `ui.todo` primitive & runtime mappings.
  - `skills/paddlr-mode/references/core-contracts.md` — Add `ui.todo` to Contract 5, update Contract 6 (Reversibility-First Autonomy), note `.paddlr.json` in Contract 2.
  - `skills/paddlr-mode/references/task-state-schema.md` — Document `.paddlr.json` override and `ui.todo` two-tier sync rule.
  - `skills/paddlr-mode/playbooks/feature.md`, `playbooks/bug-fix.md`, `playbooks/opening-a-pr.md`, `worker.md` — Align autonomy, `ui.todo`, and mandatory `sync-docs` pre-PR gate.
  - `skills/why/SKILL.md` — Include `specs/` and `.paddlr.json` awareness.
  - `hooks/session-start.py` — Keep skill summary concise and aligned with `writing-decisions` and `sync-docs`.
  - `tests/test_workflow_scenarios.py` & `tests/test_commands.py` — Update Level 2 autonomy assertions and add `adr` command check.
  - `README.md` — Link to `docs/guide/README.md`.

---

## Tasks

### Task 1: Project Memory Configuration (`.paddlr.json`) & Resolver

**Files:**
- Create: `scripts/paddlr_config.py`
- Create: `tests/test_paddlr_config.py`
- Modify: `skills/paddlr-mode/references/task-state-schema.md`
- Modify: `skills/paddlr-mode/references/core-contracts.md` (Contract 2)

**Interfaces:**
- Consumes: Target repository root `Path`.
- Produces: `resolve_memory_paths(repo_root: Path) -> dict[str, Path]` returning keys `root`, `specs`, `plans`, `decisions`, `decisionsIndex`, `project`.

- [x] **Step 1: Write failing tests in `tests/test_paddlr_config.py`**
  - `test_defaults_when_no_config_file`: returns `docs/paddlr` and all 5 sub-paths under it.
  - `test_custom_root_cascades_to_unspecified_subpaths`: `{"root": ".paddlr-docs"}` resolves `specs` to `.paddlr-docs/specs`, etc.
  - `test_partial_subpath_overrides`: `{"decisions": "docs/adr", "plans": ".local/plans"}` overrides only those two keys while keeping `specs` at `docs/paddlr/specs`.
  - `test_malformed_json_raises_value_error`: invalid JSON or non-string value raises `ValueError`.
  - `test_path_traversal_raises_value_error`: `{"plans": "../outside"}` or `{"plans": "/etc/plans"}` raises `ValueError`.
- [x] **Step 2: Run tests to verify failure**
  - Run: `python -m unittest tests/test_paddlr_config.py -v`
  - Expected: FAIL (`ModuleNotFoundError: No module named 'scripts.paddlr_config'`).
- [x] **Step 3: Implement `resolve_memory_paths(repo_root: Path) -> dict[str, Path]` in `scripts/paddlr_config.py`**
  - Read `repo_root / ".paddlr.json"` if present; validate JSON object, string values, and ensure every resolved path stays inside `repo_root.resolve()`.
- [x] **Step 4: Document `.paddlr.json` schema in `task-state-schema.md` and `core-contracts.md` (Contract 2)**
- [x] **Step 5: Run tests to verify pass**
  - Run: `python -m unittest tests/test_paddlr_config.py -v`
  - Expected: PASS (all 5 tests).

---

### Task 2: Reversibility-First Autonomy Policy Alignment

**Files:**
- Modify: `rules/AGENTS.md`
- Modify: `rules/CLAUDE.md`
- Modify: `skills/paddlr-mode/references/core-contracts.md` (Contract 6)
- Modify: `skills/paddlr-mode/SKILL.md` (`## Autonomy`)
- Modify: `skills/paddlr-mode/playbooks/feature.md`
- Modify: `skills/paddlr-mode/worker.md`
- Modify: `tests/test_workflow_scenarios.py`

**Interfaces:**
- Consumes: `WorkflowClassificationEngine.classify_task(...)` in `tests/test_workflow_scenarios.py`.
- Produces: Consistent Level 1 / Level 2 (reversible vs. ambiguous) / Level 3 / Hard-Stop autonomy rules across rules, contracts, playbooks, and tests.

- [x] **Step 1: Update `tests/test_workflow_scenarios.py` assertions first (TDD)**
  - Update `test_scenario_03_multi_module_feature`: clear reversible Level 2 expects `requires_approval_before_code=False`, `requires_formal_spec=True`, `requires_implementation_plan=True`.
  - Update `test_scenario_04_new_external_integration`: reversible Level 2 with `multiple_approaches_exist=True` (no ambiguity) or explicit `is_ambiguous=True` reflects the new rule cleanly.
  - Keep `test_scenario_05`, `test_scenario_06`, `test_scenario_07` (`is_ambiguous=True`), and `test_scenario_10` expecting `requires_approval_before_code=True`.
- [x] **Step 2: Run `tests/test_workflow_scenarios.py` to verify failure**
  - Run: `python -m unittest tests/test_workflow_scenarios.py -v`
  - Expected: FAIL on Level 2 `requires_approval_before_code` assertion.
- [x] **Step 3: Update `WorkflowClassificationEngine.classify_task` in `tests/test_workflow_scenarios.py` and align documentation**
  - Set Level 2 `requires_approval_before_code = is_ambiguous` (default `False` for clear reversible branch work; `True` when ambiguous or escalated to Level 3).
  - Update `rules/AGENTS.md` (Step 2 + `.paddlr.json` mention), `rules/CLAUDE.md` (if it mirrors autonomy), `core-contracts.md` (Contract 6), `paddlr-mode/SKILL.md` (`## Autonomy`), `playbooks/feature.md`, and `worker.md` to state the exact 4-tier Reversibility-First Autonomy Policy.
- [x] **Step 4: Run tests to verify pass**
  - Run: `python -m unittest tests/test_workflow_scenarios.py -v`
  - Expected: PASS.

---

### Task 3: Two-Tier Checklist Synchronization (`ui.todo`)

**Files:**
- Modify: `skills/paddlr-mode/references/runtime-adapters.md`
- Modify: `skills/paddlr-mode/references/core-contracts.md` (Contract 5)
- Modify: `skills/paddlr-mode/references/task-state-schema.md`
- Modify: `skills/paddlr-mode/SKILL.md`
- Create: `tests/test_paddlr_v1_2_contracts.py`

**Interfaces:**
- Consumes: Existing semantic primitive tables in `runtime-adapters.md` and `core-contracts.md`.
- Produces: `ui.todo` optional primitive specification + two-tier sync rule.

- [x] **Step 1: Write failing contract tests in `tests/test_paddlr_v1_2_contracts.py`**
  - `test_ui_todo_primitive_documented`: asserts `ui.todo`, `TodoWrite`, `update_steps`, `update_plan`, `todowrite` appear in `runtime-adapters.md`, and `ui.todo` appears in `core-contracts.md` and `task-state-schema.md`.
- [x] **Step 2: Run test to verify failure**
  - Run: `python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: FAIL.
- [x] **Step 3: Add `ui.todo` primitive and sync rule**
  - Add `ui.todo` row to the Capability Negotiation Matrix in `runtime-adapters.md` and `core-contracts.md` (Optional Enhancement; mappings for Cursor/Claude Code `TodoWrite`, Antigravity `update_steps`, Codex CLI `update_plan`, OpenCode `todowrite`; fallback: compact progress list in chat replies at phase boundaries).
  - Document the two-tier sync rule in `task-state-schema.md` (Section 2) and `paddlr-mode/SKILL.md` (`## Non-negotiables`).
- [x] **Step 4: Run test to verify pass**
  - Run: `python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: PASS.

---

### Task 4: `paddlr-mode` Cleanup & Skill Boundary Disambiguation

**Files:**
- Modify: `skills/paddlr-mode/SKILL.md`
- Modify: `skills/paddlr-mode/playbooks/bug-fix.md`
- Modify: `tests/test_paddlr_v1_2_contracts.py`

**Interfaces:**
- Consumes: `skills/paddlr-mode/SKILL.md`.
- Produces: Zero `poteto` leaks, explicit Level 1 plan exemption, and Skill vs. Playbook boundary table.

- [x] **Step 1: Add failing regression tests in `tests/test_paddlr_v1_2_contracts.py`**
  - `test_no_poteto_references_in_repo`: scans `skills/`, `rules/`, `commands/`, `hooks/`, `tests/`, `scripts/` and asserts zero case-insensitive matches for `poteto` (excluding the test file's own string literal).
  - `test_paddlr_mode_boundaries_and_level1_exemption`: asserts `paddlr-worker`, Level 1 exemption, and boundary comparisons (`feature-development`, `sre-debugging`, `code-review`, `interrogate`) appear in `skills/paddlr-mode/SKILL.md`.
- [x] **Step 2: Run tests to verify failure**
  - Run: `python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: FAIL (`poteto-agent` found at `skills/paddlr-mode/SKILL.md:11`).
- [x] **Step 3: Update `skills/paddlr-mode/SKILL.md` and `playbooks/bug-fix.md`**
  - Replace `poteto-agent` with `paddlr-worker` on line 11.
  - Update line 100 to explicitly exempt Level 1 tasks from mandatory plan creation (referencing `task-state-schema.md`).
  - Add the concise Skill vs. Playbook Boundary Matrix (`feature-development` vs. `playbooks/feature.md`, `sre-debugging` vs. `playbooks/bug-fix.md`, `code-review` vs. `interrogate`).
- [x] **Step 4: Run tests to verify pass**
  - Run: `python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: PASS.

---

### Task 5: ADR & Doc-Sync Closure (`writing-decisions`, `sync-docs`, `why`)

**Files:**
- Create: `skills/writing-decisions/SKILL.md`
- Create: `commands/adr.md`
- Create: `skills/sync-docs/SKILL.md`
- Modify: `skills/paddlr-mode/playbooks/opening-a-pr.md`
- Modify: `skills/why/SKILL.md`
- Modify: `hooks/session-start.py`
- Modify: `tests/test_commands.py`
- Modify: `tests/test_paddlr_v1_2_contracts.py`

**Interfaces:**
- Consumes: `skills/writing-specs/references/adr-guide.md`, `.paddlr.json` contract from Task 1.
- Produces: `writing-decisions` skill, `/adr` command, `sync-docs` skill, mandatory pre-PR doc-sync gate in `opening-a-pr.md`, and spec-aware `why` skill.

- [x] **Step 1: Add failing tests in `tests/test_commands.py` and `tests/test_paddlr_v1_2_contracts.py`**
  - Add `"adr"` to `EXPECTED_COMMANDS` in `tests/test_commands.py`.
  - Add `test_adr_and_sync_docs_closure` asserting `writing-decisions/SKILL.md` and `sync-docs/SKILL.md` exist with `disable-model-invocation: true`, `opening-a-pr.md` invokes `sync-docs`, and `why/SKILL.md` checks `specs/` and `.paddlr.json`.
- [x] **Step 2: Run tests to verify failure**
  - Run: `python -m unittest tests/test_commands.py tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: FAIL.
- [x] **Step 3: Author skills, command, and playbook updates**
  - Create `skills/writing-decisions/SKILL.md` (`disable-model-invocation: true`): create/supersede immutable ADRs in `decisions/XXXX-<slug>.md`, update `DECISIONS.md` index, respect `.paddlr.json`, link to `../writing-specs/references/adr-guide.md`.
  - Create `commands/adr.md` linking to `../skills/writing-decisions/SKILL.md`.
  - Create `skills/sync-docs/SKILL.md` (`disable-model-invocation: true`): diff branch changes against active `specs/`, `decisions/`, and `PROJECT.md` (respecting `.paddlr.json`); report/fix drift or cleanly report no affected docs.
  - Update `skills/paddlr-mode/playbooks/opening-a-pr.md` Step 2 (Quality Pass) to run `sync-docs` before opening the PR.
  - Update `skills/why/SKILL.md` to inspect `decisions/` + `DECISIONS.md` and `specs/` (respecting `.paddlr.json`) before git history.
  - Update `hooks/session-start.py` `BOOTSTRAP_CONTEXT` to mention `writing-decisions` and `sync-docs`.
- [x] **Step 4: Run tests and validator to verify pass**
  - Run: `python scripts/validate_skills.py && python -m unittest tests/test_commands.py tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: PASS.

---

### Task 6: Two New SDD Principles (26 Total)

**Files:**
- Create: `skills/principle-spec-before-code/SKILL.md`
- Create: `skills/principle-record-decisions-immutably/SKILL.md`
- Modify: `skills/paddlr-mode/SKILL.md` (`## Principles`)
- Modify: `tests/test_paddlr_v1_2_contracts.py`

**Interfaces:**
- Consumes: Principle frontmatter pattern (`disable-model-invocation: true`) and `paddlr-mode/SKILL.md` Principles index.
- Produces: 26 lazy-loaded `principle-*` skills fully indexed in `paddlr-mode/SKILL.md`.

- [x] **Step 1: Add failing test in `tests/test_paddlr_v1_2_contracts.py`**
  - `test_26_principles_exist_and_indexed`: asserts `len(list(SKILLS_DIR.glob("principle-*"))) == 26`, every principle has `disable-model-invocation: true`, and `Spec Before Code` and `Record Decisions Immutably` are indexed in `skills/paddlr-mode/SKILL.md`.
- [x] **Step 2: Run test to verify failure**
  - Run: `python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: FAIL (24 != 26).
- [x] **Step 3: Create the 2 SDD principle skills and index them**
  - Create `skills/principle-spec-before-code/SKILL.md` (`disable-model-invocation: true`, Level 2+ spec before implementation, Level 1 exempt).
  - Create `skills/principle-record-decisions-immutably/SKILL.md` (`disable-model-invocation: true`, append-only ADRs, supersede rather than rewrite).
  - Add both entries under `**Architecture**` or `**Core**` in `skills/paddlr-mode/SKILL.md`.
- [x] **Step 4: Run tests and validator to verify pass**
  - Run: `python scripts/validate_skills.py && python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: PASS.

---

### Task 7: Craft Skills from `pstack` (`no-comments`, `unslop`, `correct`)

**Files:**
- Create: `skills/no-comments/SKILL.md`
- Create: `skills/no-comments/comment-sicko.md`
- Create: `skills/unslop/SKILL.md`
- Create: `skills/correct/SKILL.md`
- Modify: `tests/test_paddlr_v1_2_contracts.py`

**Interfaces:**
- Consumes: Paddlr's agent-agnostic `agent.delegate` + Single-Agent fallback contract (`runtime-adapters.md`).
- Produces: 3 lazy-loaded craft skills conforming to the Agent Skills open standard.

- [x] **Step 1: Add failing test in `tests/test_paddlr_v1_2_contracts.py`**
  - `test_craft_skills_exist_and_agent_agnostic`: asserts `no-comments`, `unslop`, `correct` exist with `disable-model-invocation: true`, `skills/no-comments/comment-sicko.md` exists, and `no-comments/SKILL.md` contains no `poteto` or hardcoded `Task` tool requirement.
- [x] **Step 2: Run test to verify failure**
  - Run: `python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: FAIL.
- [x] **Step 3: Create the 3 craft skills**
  - Author `skills/no-comments/SKILL.md` and `skills/no-comments/comment-sicko.md` adapted for Paddlr (uses `agent.delegate` when supported, falls back to in-thread execution of `comment-sicko.md`; diffs against repository base branch instead of hardcoding `main`).
  - Author `skills/unslop/SKILL.md` (`disable-model-invocation: true`, concise prose de-slopping checklist with stable rule IDs).
  - Author `skills/correct/SKILL.md` (`disable-model-invocation: true`, structural mistake prevention hierarchy: architecture -> types/lint -> tests -> rules).
- [x] **Step 4: Run tests and validator to verify pass**
  - Run: `python scripts/validate_skills.py && python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: PASS.

---

### Task 8: User-Facing Handbook (`docs/guide/`)

**Files:**
- Create: `docs/guide/README.md`
- Create: `docs/guide/01-setup.md`
- Create: `docs/guide/02-paddlr-mode.md`
- Create: `docs/guide/03-specs-plans-adrs.md`
- Create: `docs/guide/04-autonomy-and-verification.md`
- Create: `docs/guide/05-principles-and-skills.md`
- Create: `docs/guide/06-customization.md`
- Modify: `README.md`
- Modify: `tests/test_paddlr_v1_2_contracts.py`

**Interfaces:**
- Consumes: Finalized v1.2.0 contracts, `.paddlr.json` schema, 26 principles, and skills catalog.
- Produces: User-facing handbook linked from `README.md` with 100% valid internal links.

- [x] **Step 1: Add failing test in `tests/test_paddlr_v1_2_contracts.py`**
  - `test_user_guide_exists_and_linked_from_readme`: asserts `docs/guide/README.md` and chapters `01`..`06` exist and `README.md` links to `docs/guide/README.md`.
- [x] **Step 2: Run test to verify failure**
  - Run: `python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: FAIL.
- [x] **Step 3: Author `docs/guide/` chapters and link from `README.md`**
  - Keep every chapter concise, plain English, agent-agnostic, and free of unverified claims.
  - Link `docs/guide/README.md` from `README.md`.
- [x] **Step 4: Run tests and Markdown link checker**
  - Run: `python scripts/check_markdown_links.py && python -m unittest tests/test_paddlr_v1_2_contracts.py -v`
  - Expected: PASS.

---

### Task 9: Full CI Verification Suite

**Files:**
- Verify all modified and created files.

**Interfaces:**
- Consumes: Outputs of Tasks 1–8.
- Produces: Captured verbatim CI verification evidence.

- [x] **Step 1: Run full CI validation suite**
  - Run: `python scripts/validate_skills.py --verbose && python -m unittest discover -s tests -v && python scripts/check_markdown_links.py`
  - Expected: Exit code `0`; all skills valid (55 total: 48 existing + `writing-decisions`, `sync-docs`, 2 SDD principles, `no-comments`, `unslop`, `correct`), all unit tests pass, zero broken Markdown links.
- [x] **Step 2: Inspect `git status` and `git diff --stat`**
  - Confirm uncommitted `disable-model-invocation: true` edits in `skills/code-review/SKILL.md` and `skills/feature-development/SKILL.md` are intact and no extraneous/temp files exist.
- [x] **Step 3: Update plan frontmatter (`status: "completed"`) and record verification evidence**

---

## Verification & Evidence

- **Head commit:** `69552c1` (`dev`, working tree uncommitted for user review)
- **`python scripts/validate_skills.py --verbose`:** `PASS` — `Total: 55 | Valid: 55 | Invalid: 0`
- **`python -m unittest discover -s tests -v`:** `PASS` — `Ran 64 tests in 1.189s — OK`
- **`python scripts/check_markdown_links.py`:** `PASS` — `All Markdown internal links resolve successfully.`
- **Preserved pre-existing edits:** Verified via `git diff skills/code-review/SKILL.md skills/feature-development/SKILL.md` (`disable-model-invocation: true` intact in both files).
