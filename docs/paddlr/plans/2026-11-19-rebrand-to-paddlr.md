# Implementation Plan: Brand Rebranding to Paddlr

- **Date:** 2026-11-19
- **Specification:** [docs/paddlr/specs/2026-11-19-rebrand-to-paddlr.md](../specs/2026-11-19-rebrand-to-paddlr.md)
- **Status:** Completed & Verified

---

## Task Decomposition

### Task 1: Manifests & Metadata Updates
- **Consumes:** Existing manifests (`package.json`, `plugin.json`, `.claude-plugin/*`, `.codex-plugin/*`, `.agents/*`, `hooks.json`, `hooks/hooks.json`, `.gitattributes`, `.gitignore`)
- **Produces:** Updated manifests reflecting brand `paddlr`, display name `Paddlr`, description, keywords, and hook name `paddlr-session-start`
- **Steps:**
  - [x] Update `package.json` with name `paddlr`, description, keywords (`paddlr`, `pdl`, `software-engineering`), repository links.
  - [x] Update `plugin.json` with name `paddlr`, displayName `Paddlr`, description, suggestedPrompts.
  - [x] Update `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` with `paddlr`.
  - [x] Update `.codex-plugin/plugin.json` and `.agents/plugins/marketplace.json` with `paddlr`.
  - [x] Update `hooks.json` and `hooks/hooks.json` with hook ID `paddlr-session-start`.
  - [x] Update `.gitattributes` (`pdl text eol=lf`) and `.gitignore` (`.pdl-manifest.json`).

### Task 2: Mascot & Visual Identity (`assets/logo.svg`)
- **Consumes:** Brand brief section 5 (The Duck mascot, minimalist aesthetic, water ripples, calm geometric profile)
- **Produces:** Modern, high-resolution SVG logo in `assets/logo.svg` representing the Paddlr Duck
- **Steps:**
  - [x] Design SVG logo featuring a geometric, calm duck floating on water with gentle ripple waves and developer-tool aesthetic.
  - [x] Verify SVG validity and rendering.

### Task 3: Core Runtime, Hooks & OpenCode Plugin
- **Consumes:** `hooks/session-start.py`, `index.js`, `index.d.ts`, `.opencode/`
- **Produces:** Updated runtime modules with Paddlr bootstrap, `pdl_*` tools, and `PaddlrPlugin` exports
- **Steps:**
  - [x] Update `hooks/session-start.py` bootstrap context: Paddlr discipline, tagline, core principles, and `docs/paddlr/` persistent memory path.
  - [x] Update `index.js`: update `BOOTSTRAP_CONTEXT`, export `PaddlrPlugin` (with backward-compatible `HolyShitItWorksPlugin`), rename tools to `pdl_bootstrap`, `pdl_status`, `pdl_scan` (supporting both `docs/paddlr` and legacy `docs/hsiw` fallback).
  - [x] Update `index.d.ts`: declare `PaddlrPlugin` and `BOOTSTRAP_CONTEXT`.
  - [x] Create `.opencode/plugins/paddlr.js` (and keep `.opencode/plugins/hsiw.js` re-exporting for backward compatibility).
  - [x] Update `.opencode/INSTALL.md` with `paddlr` installation and tool instructions.

### Task 4: Slash Commands (`commands/`)
- **Consumes:** 8 Markdown command files in `commands/`
- **Produces:** Updated commands with `# /pdl:<command>` prefixes
- **Steps:**
  - [x] Update `commands/code-review.md` -> `# /pdl:code-review`
  - [x] Update `commands/feature-development.md` -> `# /pdl:feature-development`
  - [x] Update `commands/release-management.md` -> `# /pdl:release-management`
  - [x] Update `commands/skill-creator.md` -> `# /pdl:skill-creator`
  - [x] Update `commands/sre-debugging.md` -> `# /pdl:sre-debugging`
  - [x] Update `commands/test-driven-development.md` -> `# /pdl:test-driven-development`
  - [x] Update `commands/writing-plans.md` -> `# /pdl:writing-plans`
  - [x] Update `commands/writing-specs.md` -> `# /pdl:writing-specs`

### Task 5: Rules & Contributor Guidelines
- **Consumes:** `rules/AGENTS.md`, `rules/CLAUDE.md`, root `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `RELEASE.md`
- **Produces:** Comprehensive rules and documentation updated for Paddlr
- **Steps:**
  - [x] Update `rules/AGENTS.md` and `rules/CLAUDE.md` to Paddlr, updating memory standard to `docs/paddlr/`.
  - [x] Update root `AGENTS.md` and `CLAUDE.md`.
  - [x] Update `RELEASE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`.

### Task 6: Comprehensive README Rebrand
- **Consumes:** Complete text and sections from Brand Rebranding Brief
- **Produces:** High-impact, beautifully formatted `README.md` for Paddlr
- **Steps:**
  - [x] Present Paddlr brand identity, tagline ("Simple on the Surface. Sophisticated Underneath.").
  - [x] Include The Duck Philosophy (Above the Surface vs. Below the Surface).
  - [x] Include Brand Principles, CLI identity (`pdl init`, `pdl spec`, `pdl plan`, `pdl test`, `pdl debug`, `pdl release`).
  - [x] Provide installation guides for Google Antigravity, Claude Code, OpenCode, and OpenAI Codex.
  - [x] Document product architecture and skill ecosystem.

### Task 7: Skills References & Project Memory Migration
- **Consumes:** `skills/` directory, `docs/hsiw/`
- **Produces:** Skills referencing `docs/paddlr/`, persistent memory migrated to `docs/paddlr/`
- **Steps:**
  - [x] Update references in `skills/feature-development/SKILL.md`, `skills/writing-specs/SKILL.md`, `skills/writing-plans/SKILL.md`, `skills/code-review/SKILL.md`, `skills/writing-specs/references/adr-guide.md`, etc.
  - [x] Rename/move `docs/hsiw` to `docs/paddlr`.
  - [x] Verify skill validity with `python scripts/validate_skills.py --verbose`.

### Task 8: Test Suite Updates & Verification
- **Consumes:** `tests/` directory and fixtures
- **Produces:** Fully updated, passing test suite confirming all Paddlr contracts
- **Steps:**
  - [x] Update `tests/test_plugins.py` to test `paddlr`, `Paddlr`, `pdl_bootstrap`, `pdl_status`, `pdl_scan`.
  - [x] Update `tests/test_commands.py` and other test files.
  - [x] Update fixture files if necessary.
  - [x] Execute `python scripts/validate_skills.py --verbose`.
  - [x] Execute `python -m unittest discover -s tests -v`.
  - [x] Execute CI Markdown internal link check script.
