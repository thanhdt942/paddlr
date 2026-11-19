# Implementation Plan: Granular ADR Management

- **Date:** 2026-11-19
- **Specification:** [docs/hsiw/specs/2026-11-19-granular-adr-management.md](../specs/2026-11-19-granular-adr-management.md)
- **Status:** Completed

## Tasks

### Task 1: Create ADR Reference Guide
- **Consumes:** Feature spec requirements
- **Produces:** `skills/writing-specs/references/adr-guide.md`
- [x] Create `skills/writing-specs/references/adr-guide.md` detailing ADR anatomy, trigger criteria, index table format in `DECISIONS.md`, and individual ADR file template in `decisions/XXXX-<slug>.md`.

### Task 2: Update writing-specs Skill
- **Consumes:** `skills/writing-specs/references/adr-guide.md`
- **Produces:** Updated `skills/writing-specs/SKILL.md`
- [x] Add Architectural Decisions (ADR) section to `skills/writing-specs/SKILL.md` with trigger condition and explicit reference to `references/adr-guide.md`.

### Task 3: Update feature-development Skill & Workflow Decisions
- **Consumes:** `skills/feature-development/SKILL.md`, `references/workflow-decisions.md`
- **Produces:** Updated orchestrator instructions
- [x] Update `skills/feature-development/SKILL.md` Phase 2 (Triage) and Phase 3 (Spec/Plan) to enforce ADR formulation for Level 3 architectural tasks.
- [x] Update `skills/feature-development/references/workflow-decisions.md` Level 3 requirements to include recording ADR in `docs/hsiw/decisions/` and updating `docs/hsiw/DECISIONS.md`.

### Task 4: Update Rules and Documentation
- **Consumes:** Updated ADR architecture
- **Produces:** Updated `rules/AGENTS.md` and `README.md`
- [x] Update `rules/AGENTS.md` Documentation & Project Context Rules to describe `docs/hsiw/DECISIONS.md` index + `docs/hsiw/decisions/` files.
- [x] Update `README.md` Persistent Project Memory section tree diagram to include `decisions/`.

### Task 5: Add Architecture Verification Tests
- **Consumes:** Modified skills and reference guides
- **Produces:** Updated `tests/test_core_skills_architecture.py`
- [x] Add unit test verifying that `writing-specs` contains `adr-guide.md` and references ADR recording methodology.

### Task 6: Evidence Verification & Quality Gates
- **Consumes:** All repository modifications
- **Produces:** Test run logs and skill validation evidence
- [x] Run `python scripts/validate_skills.py --verbose` (confirm 8/8 PASS).
- [x] Run `python -m unittest discover -s tests -v` (confirm all tests PASS).
