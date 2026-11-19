# Changelog

All notable changes to the Paddlr project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
