---
task_id: "pdl-2026-11-24-02"
title: "Add setup-paddlr and paddlr-help skills"
classification: 2
status: "completed"
playbook: "feature"
active_phase: "completed"
done_predicate: "setup-paddlr and paddlr-help skills, commands, docs, and unit tests pass validate_skills.py, unittest discover -s tests, and check_markdown_links.py with exit code 0."
created_at: "2026-11-24T20:06:00+07:00"
updated_at: "2026-11-24T20:07:30+07:00"
---

# `setup-paddlr` and `paddlr-help` Implementation Plan

> **Execution:** Level 2 reversible feature; execute task-by-task without blocking for approval.

**Goal:** Add `setup-paddlr` (auto-invocable onboarding/setup skill) and `paddlr-help` (lazy-loaded read-only advisor skill), with matching slash commands, handbook/README updates, and unit tests.

**Architecture:** Both skills follow the Agent Skills open standard under `skills/`, expose slash commands under `commands/`, remain 100% agent-agnostic using Paddlr's semantic primitives (`runtime-adapters.md`) and `.paddlr.json` schema (`scripts/paddlr_config.py`), and are verified by Python stdlib `unittest` tests.

**Tech Stack:** Markdown (Agent Skills), Python 3.10+ stdlib (`unittest`).

**Key Decisions:**
- `setup-paddlr` omits `disable-model-invocation: true`; `paddlr-help` sets `disable-model-invocation: true`.
- Model profile configuration uses Paddlr's 3 abstract profiles (`deep-reasoning`, `standard-code`, `fast-mechanical`) and degrades gracefully when unsupported.
- `paddlr-help` is strictly read-only and never runs the requested task.

**Spec:** [docs/paddlr/specs/2026-11-24-setup-paddlr-and-help.md](../specs/2026-11-24-setup-paddlr-and-help.md)

## Global Constraints

- Agent-agnostic: zero Cursor-only tool requirements, zero `cursor-team-kit`, zero `poteto` references.
- Preserve completed v1.2.0 plan untouched; no `git commit`.
- Full CI checks (`validate_skills.py`, `unittest`, `check_markdown_links.py`) must exit 0.

## Review Focus

- `setup-paddlr` must NOT contain `disable-model-invocation: true`, while `paddlr-help` MUST contain `disable-model-invocation: true` (pinned in Task 1 tests).
- `setup-paddlr` must align with `scripts/paddlr_config.py` keys (`root`, `specs`, `plans`, `decisions`, `decisionsIndex`, `project`) and handle existing `docs/adr/` or `docs/specs/` without overwriting them (pinned in Task 1 tests).
- `paddlr-help` must explicitly forbid executing the user's task and mandate the 3-part reply (match + reason, link, copy-paste prompt) (pinned in Task 1 tests).

---

## Tasks

### Task 1: Write Failing Unit Tests (TDD RED)

**Files:**
- Create: `tests/test_setup_and_help_skills.py`
- Modify: `tests/test_commands.py`

**Interfaces:**
- Consumes: `skills/setup-paddlr/SKILL.md`, `skills/paddlr-help/SKILL.md`, `commands/setup-paddlr.md`, `commands/paddlr-help.md`, `docs/guide/`, `README.md`.
- Produces: Executable unit tests verifying all requirements in the Spec.

- [x] **Step 1:** Create `tests/test_setup_and_help_skills.py` asserting `setup-paddlr` (no `disable-model-invocation: true`, `.paddlr.json` & `docs/paddlr/` init, 3 model profiles, graceful skip, `/create-verification-skill` offer), `paddlr-help` (`disable-model-invocation: true`, read-only rule, 3-part output, links to skills/playbooks/26 principles/`docs/guide/`), and doc references.
- [x] **Step 2:** Add `"setup-paddlr"` and `"paddlr-help"` to `EXPECTED_COMMANDS` in `tests/test_commands.py`.
- [x] **Step 3:** Run `python -m unittest tests/test_setup_and_help_skills.py tests/test_commands.py -v` and confirm RED failure.

### Task 2: Author `setup-paddlr` and `paddlr-help` Skills

**Files:**
- Create: `skills/setup-paddlr/SKILL.md`
- Create: `skills/paddlr-help/SKILL.md`

**Interfaces:**
- Consumes: `scripts/paddlr_config.py`, `skills/paddlr-mode/references/runtime-adapters.md`, `skills/paddlr-mode/SKILL.md`, `docs/guide/`.
- Produces: Two valid, agent-agnostic Agent Skills.

- [x] **Step 1:** Author `skills/setup-paddlr/SKILL.md` (without `disable-model-invocation: true`).
- [x] **Step 2:** Author `skills/paddlr-help/SKILL.md` (with `disable-model-invocation: true`, read-only advisory, concise routing table, 3-part output format).

### Task 3: Sync Commands, Handbook, README, and Session Hook

**Files:**
- Create: `commands/setup-paddlr.md`
- Create: `commands/paddlr-help.md`
- Modify: `docs/guide/01-setup.md`
- Modify: `docs/guide/05-principles-and-skills.md`
- Modify: `README.md`
- Modify: `hooks/session-start.py`

**Interfaces:**
- Consumes: `skills/setup-paddlr/SKILL.md`, `skills/paddlr-help/SKILL.md`.
- Produces: Consistent slash commands, onboarding guide references, and session-start awareness.

- [x] **Step 1:** Create `commands/setup-paddlr.md` and `commands/paddlr-help.md` linking to their respective `SKILL.md` files.
- [x] **Step 2:** Update `docs/guide/01-setup.md`, `docs/guide/05-principles-and-skills.md`, `README.md`, and `hooks/session-start.py`.

### Task 4: Full CI Verification & Plan Finalization

- [x] **Step 1:** Run `python scripts/validate_skills.py --verbose`, `python -m unittest discover -s tests -v`, and `python scripts/check_markdown_links.py`.
- [x] **Step 2:** Mark all plan checkboxes `- [x]`, set `status: "completed"`, and report verbatim verification evidence.

---

## Verification & Evidence

- **`python scripts/validate_skills.py`:** `PASS` — `Total: 57 | Valid: 57 | Invalid: 0`
- **`python -m unittest discover -s tests -v`:** `PASS` — `Ran 67 tests in 1.181s — OK`
- **`python scripts/check_markdown_links.py`:** `PASS` — `All Markdown internal links resolve successfully.`
