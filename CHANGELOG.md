# Changelog

All notable changes to the Paddlr project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0](https://github.com/thanhdt942/paddlr/compare/v1.2.1...v1.3.0) (2026-11-24)


### Features

* **autonomy:** pause only on irreversible actions by default and load .paddlr.json autonomy settings ([1e2ddfb](https://github.com/thanhdt942/paddlr/commit/1e2ddfb854aaa42cedf91de629b6e844c3f88fdb))

## [1.2.1] - 2026-11-24

### Removed
- Removed obsolete legacy `commands/` directory and `tests/test_commands.py` (Claude Code and other supported agents auto-expose skills directly from `skills/*/SKILL.md`).

### Changed
- Streamlined and aligned top-level documentation (`README.md`, `CONTRIBUTING.md`, `SUPPORT.md`, `SECURITY.md`, `AGENTS.md`) with Paddlr v1.2 (57 skills, Cursor support, `docs/guide/`, `.paddlr.json`, and accurate `1.2.x` version support tables).

## [1.2.0] - 2026-11-24

### Added
- **Project Memory Path Overrides (`.paddlr.json`):** Optional root configuration file and pure-stdlib resolver (`scripts/paddlr_config.py`) allowing target repositories to map `root`, `specs`, `plans`, `decisions`, `decisionsIndex`, and `project` without colliding with existing docs.
- **Two-Tier Checklist Synchronization (`ui.todo`):** Added `ui.todo` optional semantic primitive to `runtime-adapters.md` and `core-contracts.md`, mapping active steps to Cursor/Claude Code (`TodoWrite`), Antigravity (`update_steps`), Codex CLI (`update_plan`), OpenCode (`todowrite`), and a chat progress fallback.
- **ADR & Doc-Sync Closure:**
  - `skills/writing-decisions` + `/adr` command (`commands/adr.md`) for authoring and superseding immutable ADRs in `decisions/` and `DECISIONS.md`.
  - `skills/sync-docs` wired as a mandatory pre-PR gate in `playbooks/opening-a-pr.md`.
- **Two New SDD Principles (26 Principles Total):** `skills/principle-spec-before-code` and `skills/principle-record-decisions-immutably` (both lazy-loaded).
- **Agent-Agnostic Craft & Onboarding Skills:**
  - `skills/no-comments` (+ `comment-sicko.md`), `skills/unslop`, `skills/correct`.
  - `skills/setup-paddlr` (+ `commands/setup-paddlr.md`) for repository onboarding, `.paddlr.json` detection, optional model profile steering, and verification skill offer.
  - `skills/paddlr-help` (+ `commands/paddlr-help.md`) as a strictly read-only advisor routing questions to skills, playbooks, principles, and copy-paste prompts.
- **User-Facing Handbook (`docs/guide/`):** Six-chapter onboarding and reference guide linked from `README.md`.

### Changed
- **Reversibility-First Autonomy Policy:** Unified Level 1 (direct), Level 2 reversible branch work (write Spec + Plan and proceed without pre-code blocking), Level 3 architectural/breaking (mandatory pre-code approval on Spec + ADR + Plan), and Hard Stops across `rules/AGENTS.md`, `core-contracts.md`, `paddlr-mode`, and `tests/test_workflow_scenarios.py`.
- **Streamlined Always-On Rules:** Trimmed `rules/AGENTS.md` (90 -> 24 lines) and `rules/CLAUDE.md` (21 -> 9 lines) to remove legacy v1.0 contradictions and reduce baseline token overhead.
- **Lazy-Loading Discipline:** Set `disable-model-invocation: true` across all skills except `setup-paddlr` (enforced by unit test).
- **`paddlr-mode` & `why` Alignment:** Replaced legacy `poteto-agent` reference with `paddlr-worker`, aligned Level 1 plan exemption, added Playbook vs. Skill boundary matrix, and updated `why` to inspect `specs/` and `.paddlr.json`.

## [1.1.0] - 2026-11-23

### Added
- **Paddlr Official Documentation & Landing Page:**
  - Modern, minimalist single-column landing page with dark mode support (`website/`).
  - Interactive Agent Installation Hub for Antigravity, Claude Code, Codex, and OpenCode.
  - Automated deployment workflow via GitHub Pages (`.github/workflows/deploy-pages.yml`).
- **40 Additional Agent Skills & Engineering Principles:**
  - Playbook skills: `skills/paddlr-mode`, `skills/architect`, `skills/arena`, `skills/teach`, `skills/interrogate`, `skills/how`, `skills/why`, `skills/recall`, `skills/reflect`, `skills/swarm`, `skills/blast-radius`, `skills/figure-it-out`, `skills/in-your-own-words`, `skills/benchmark-checklist`, `skills/create-verification-skill`, `skills/maintain-verification-skill`.
  - 24 Core Engineering Principles: `skills/principle-attack-the-premise`, `skills/principle-boundary-discipline`, `skills/principle-build-the-lever`, `skills/principle-encode-lessons-in-structure`, `skills/principle-exhaust-the-design-space`, `skills/principle-experience-first`, `skills/principle-explain-the-number`, `skills/principle-fix-root-causes`, `skills/principle-foundational-thinking`, `skills/principle-guard-the-context-window`, `skills/principle-laziness-protocol`, `skills/principle-make-operations-idempotent`, `skills/principle-migrate-callers-then-delete-legacy-apis`, `skills/principle-minimize-reader-load`, `skills/principle-model-the-domain`, `skills/principle-never-block-on-the-human`, `skills/principle-outcome-oriented-execution`, `skills/principle-prove-it-works`, `skills/principle-redesign-from-first-principles`, `skills/principle-separate-before-serializing-shared-state`, `skills/principle-sequence-verifiable-units`, `skills/principle-subtract-before-you-add`, `skills/principle-test-behavior-not-implementation`, `skills/principle-type-system-discipline`.
  - Automated pull request and CI watching tool (`skills/paddlr-mode/scripts/watch-pr`).
- **Acknowledgements:**
  - Added acknowledgements in `README.md` for Lauren Tan (@poteto) and pstack.

## [1.0.0] - 2026-11-19

### Added
- **Initial Release of Paddlr:** "Simple on the Surface. Sophisticated Underneath."
- **8 Core Agent Skills:**
  - `skills/feature-development`: Lightweight, end-to-end workflow orchestrator for feature intake, specs, plans, TDD, and verification gates.
  - `skills/writing-specs`: Turn requirements into reviewable specifications with ADR decisions.
  - `skills/writing-plans`: Decompose approved specifications into bite-sized, contract-first implementation plans.
  - `skills/test-driven-development`: Implement code strictly test-first (RED -> GREEN -> REFACTOR).
  - `skills/sre-debugging`: Scientific debugging and evidence-based root cause analysis.
  - `skills/code-review`: Independent, read-only reviewer subagent evaluating code quality against specs and standards.
  - `skills/release-management`: Manage software releases and conventions in `RELEASE.md`.
  - `skills/skill-creator`: Design, draft, verify, and package reusable AI agent skills.
- **Universal Multi-Agent Platform Support:**
  - Google Antigravity (`plugin.json`, `hooks.json`, `hooks/session-start.py`)
  - Anthropic Claude Code (`.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `commands/`)
  - OpenCode Plugin (`index.js`, `index.d.ts`, `.opencode/plugins/paddlr.js`) with tools `pdl_bootstrap`, `pdl_status`, and `pdl_scan`
  - OpenAI Codex (`.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`)
- **Slash Commands (`/pdl:*`):** Streamlined CLI and agent commands (`/pdl:feature-development`, `/pdl:writing-specs`, `/pdl:writing-plans`, `/pdl:test-driven-development`, `/pdl:sre-debugging`, `/pdl:code-review`, `/pdl:release-management`, `/pdl:skill-creator`).
- **Persistent Project Memory:** Standardized project memory root under `docs/paddlr/` (`docs/paddlr/specs/`, `docs/paddlr/plans/`).
- **Brand Identity & Assets:** Calm, minimalist geometric duck mascot floating on water ripples in `assets/logo.svg`.
