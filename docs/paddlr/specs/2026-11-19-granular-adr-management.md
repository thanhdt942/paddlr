# Feature Specification: Granular ADR Management (Index + Granular Decisions)

- **Date:** 2026-11-19
- **Status:** Reviewable / In Implementation
- **Target Component:** `skills/writing-specs`, `skills/feature-development`, `rules/AGENTS.md`, `README.md`

## 1. Objective & Problem Statement

Currently, HolyShitItWorks mentions `docs/hsiw/DECISIONS.md` in general operating rules, but lacks concrete operational instructions in the active skills for recording architectural decisions. Furthermore, storing all architectural decisions in a single file causes long-term context bloat for AI agents.

This feature establishes the **Granular Architectural Decision Record (ADR)** pattern:
- A compact, one-line-per-decision index file: `docs/hsiw/DECISIONS.md` (< 100 lines).
- Dedicated individual ADR markdown documents: `docs/hsiw/decisions/XXXX-<slug>.md`.
- Explicit triggers in `skills/writing-specs` and `skills/feature-development` to formulate, record, and link ADRs when architectural trade-offs or high-impact technical directions are agreed with the user.

## 2. In Scope & Out of Scope

### In Scope
1. **ADR Reference Guide:** Create `skills/writing-specs/references/adr-guide.md` specifying:
   - When to write an ADR (High impact, cross-cutting, irreversibility, trade-offs) vs when NOT to write an ADR.
   - Index table schema in `docs/hsiw/DECISIONS.md`.
   - Granular ADR file structure (`docs/hsiw/decisions/XXXX-<slug>.md`).
2. **Writing-Specs Skill Integration:**
   - Update `skills/writing-specs/SKILL.md` to trigger ADR formulation during discovery & technical design.
3. **Feature-Development Skill Integration:**
   - Update `skills/feature-development/SKILL.md` and `references/workflow-decisions.md` to require ADR checks and recording for Level 3 (Architectural Changes).
4. **Project Rules & Documentation:**
   - Update `rules/AGENTS.md` and `README.md` project memory layout to include `docs/hsiw/decisions/`.
5. **Testing & Validation:**
   - Add unit test verifying ADR guide and methodology in `tests/test_core_skills_architecture.py`.
   - Verify `scripts/validate_skills.py` (8/8 PASS) and `unittest` (53/53 PASS).

### Out of Scope
- Migrating arbitrary past commit messages into retrospective ADRs.
- Changing SemVer versioning scheme.

## 3. Acceptance Criteria
- [ ] `skills/writing-specs/references/adr-guide.md` exists and contains ADR lifecycle, format, and indexing protocol.
- [ ] `skills/writing-specs/SKILL.md` links and instructs reading `references/adr-guide.md` when architectural decisions are confirmed.
- [ ] `skills/feature-development/SKILL.md` references ADR creation for Level 3 tasks.
- [ ] `rules/AGENTS.md` and `README.md` document `docs/hsiw/decisions/` and `docs/hsiw/DECISIONS.md`.
- [ ] All skills pass validation (`python scripts/validate_skills.py --verbose`).
- [ ] All unit tests pass (`python -m unittest discover -s tests -v`).
