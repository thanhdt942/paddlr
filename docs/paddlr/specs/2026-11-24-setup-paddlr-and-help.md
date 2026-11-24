# `setup-paddlr` and `paddlr-help` Specification

**Status:** Approved (Level 2 reversible — proceeding directly per Reversibility-First Autonomy)
**Owner:** thanhdt942
**Last updated:** 2026-11-24
**Related:**
- v1.2.0 Spec: [2026-11-24-paddlr-v1-2-sdd-and-autonomy.md](2026-11-24-paddlr-v1-2-sdd-and-autonomy.md)
- Runtime Adapters: [runtime-adapters.md](../../../skills/paddlr-mode/references/runtime-adapters.md)
- Config Resolver: [paddlr_config.py](../../../scripts/paddlr_config.py)

---

## 1. Overview

Add two user-facing onboarding and navigation skills to Paddlr:

1. **`setup-paddlr`** (`skills/setup-paddlr/SKILL.md`): Interactive, idempotent onboarding skill that initializes project memory (`docs/paddlr/` or `.paddlr.json` overrides compatible with `scripts/paddlr_config.py`), configures optional model profile steering (`deep-reasoning`, `standard-code`, `fast-mechanical`), and offers `/create-verification-skill` once if the repo lacks a verification harness.
2. **`paddlr-help`** (`skills/paddlr-help/SKILL.md`): Read-only, lazy-loaded advisor (`disable-model-invocation: true`) that answers questions about Paddlr's skills, playbooks, 26 principles, and `docs/guide/`, returning the best match, a direct link, and a copy-paste prompt — without ever executing the task on the user's behalf.

---

## 2. Problem & Context

- New users installing Paddlr have no guided command to scaffold `docs/paddlr/` or detect existing `docs/adr/` / `docs/specs/` directories and generate a valid `.paddlr.json`.
- Users browsing 55+ skills, 22 playbooks, and 26 principles need a low-token, read-only advisor (`/paddlr-help`) that routes questions accurately without accidentally triggering expensive multi-step execution.

---

## 3. Scope

### In Scope
- `skills/setup-paddlr/SKILL.md` (omits `disable-model-invocation: true` so natural-language setup requests can invoke it) + `commands/setup-paddlr.md`.
- `skills/paddlr-help/SKILL.md` (sets `disable-model-invocation: true`) + `commands/paddlr-help.md`.
- Updates to `docs/guide/01-setup.md`, `docs/guide/05-principles-and-skills.md`, `docs/guide/06-customization.md`, `docs/guide/README.md`, `README.md`, and `hooks/session-start.py`.
- Unit tests in `tests/test_setup_and_help_skills.py` and `tests/test_commands.py`.

### Non-goals
- No vendor-specific config files (e.g., `~/.cursor/rules/*.mdc`) or vendor-locked tool names (`Task`, `cursor-team-kit`, `poteto-*`).
- No modifications to the completed v1.2.0 plan file (`docs/paddlr/plans/2026-11-24-paddlr-v1-2-sdd-and-autonomy.md`).
- No `git commit` or version bump.

---

## 4. Requirements

- **FR-001 (`setup-paddlr` Auto-Invocable Flag):** `skills/setup-paddlr/SKILL.md` **must** NOT set `disable-model-invocation: true`.
- **FR-002 (`setup-paddlr` Project Memory Initialization & `.paddlr.json` Detection):** `setup-paddlr` **must** scan the target repo for existing `docs/adr/`, `docs/specs/`, or `.paddlr.json`; propose a valid `.paddlr.json` compatible with `scripts/paddlr_config.py` (`root`, `specs`, `plans`, `decisions`, `decisionsIndex`, `project`) when collisions exist, or initialize `docs/paddlr/` (`specs/`, `plans/`, `decisions/`, `DECISIONS.md`, `PROJECT.md`) idempotently.
- **FR-003 (`setup-paddlr` Optional Model Profile Steering):** `setup-paddlr` **must** support optional configuration of the 3 abstract model profiles (`deep-reasoning`, `standard-code`, `fast-mechanical`) per `skills/paddlr-mode/references/runtime-adapters.md` and skip gracefully without error when the host runtime does not support model steering.
- **FR-004 (`setup-paddlr` Optional Verification Skill Offer):** If the target repo has no verification skill (`verify-*`) or harness, `setup-paddlr` **must** offer `/create-verification-skill` once without pushing.
- **FR-005 (`paddlr-help` Lazy-Loaded & Read-Only):** `skills/paddlr-help/SKILL.md` **must** set `disable-model-invocation: true` and **must** strictly prohibit executing the user's engineering task (read-only advisory to avoid burning tokens).
- **FR-006 (`paddlr-help` Structured Output):** `paddlr-help` **must** map the user's question against Paddlr's skills, playbooks, 26 principles, and `docs/guide/`, replying concisely with:
  1. The best-matching skill, playbook, or principle and a short reason.
  2. A direct link to the corresponding skill file or `docs/guide/` chapter.
  3. One ready-to-copy example prompt the user can send to start the work.
- **CON-001 (Agent-Agnostic & CI Clean):** Zero vendor-locked tool names or `poteto` references; `validate_skills.py`, `unittest discover -s tests`, and `check_markdown_links.py` must all pass with exit code 0.

---

## 5. Acceptance Criteria

- **AC-001:** `skills/setup-paddlr/SKILL.md` exists, passes `validate_skills.py`, omits `disable-model-invocation: true`, documents `.paddlr.json` + `docs/paddlr/` initialization, all 3 model profiles (`deep-reasoning`, `standard-code`, `fast-mechanical`), graceful skip on unsupported runtimes, and the optional `/create-verification-skill` offer.
- **AC-002:** `skills/paddlr-help/SKILL.md` exists, passes `validate_skills.py`, includes `disable-model-invocation: true`, enforces read-only non-execution, covers skills/playbooks/26 principles/`docs/guide/`, and specifies the 3-part output format (match + reason, link, copy-paste prompt).
- **AC-003:** `commands/setup-paddlr.md` and `commands/paddlr-help.md` exist with valid frontmatter and resolving links; `docs/guide/` and `README.md` document both skills; all CI checks pass.
