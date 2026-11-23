# Changelog

All notable changes to the Paddlr project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
