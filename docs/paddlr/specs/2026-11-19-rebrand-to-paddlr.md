# Feature Specification: Brand Rebranding to Paddlr

- **Date:** 2026-11-19
- **Author:** Antigravity / Engineering Discipline
- **Status:** Approved & Implemented
- **Previous Brand:** HolyShitItWorks (HSIW)
- **New Brand:** Paddlr
- **Tagline:** Simple on the Surface. Sophisticated Underneath.
- **CLI Command:** `pdl`

---

## 1. Executive Summary & Brand Foundation

Following the Brand Rebranding Brief, this specification governs the comprehensive transition of the framework from **HolyShitItWorks (HSIW)** to **Paddlr**.

### The Duck Philosophy & Metaphor
Paddlr embodies the metaphor of a duck swimming calmly across water:
- **Above the Surface:** Simple experience, frictionless workflows, natural developer interactions.
- **Below the Surface:** Rigorous engineering discipline, structured workflows (TDD, scientific debugging, spec-driven development), thorough validation, and persistent project memory.

### Core Philosophy
> *Handle the complexity. Simplify the experience.*
> *Great engineering doesn't have to feel complicated.*

### Guiding Principles (Brief Section 8)
1. **Preserve the Engineering Foundation:** Maintain all 8 active Agent Skills, workflows, and quality gates intact.
2. **Improve Brand Consistency:** Standardize naming, CLI commands (`pdl`), slash commands (`/pdl:...`), and documentation.
3. **Maintain Agent Agnosticism:** Keep seamless first-class support for Google Antigravity, Claude Code, OpenCode, and OpenAI Codex.
4. **Avoid Unnecessary Redesign:** Keep technical architecture and schemas stable while updating identity.
5. **Update Identity Everywhere:** Completely update all references across manifests, tools, hooks, rules, documentation, assets, and tests.

---

## 2. Component Naming & Architecture Mapping

| Component | Legacy (HSIW) | New Brand (Paddlr) | Detail / Path |
|---|---|---|---|
| **Framework Name** | HolyShitItWorks (HSIW) | **Paddlr** | Universal Brand Name |
| **CLI Command** | `hsiw` | **`pdl`** | CLI identity (`pdl init`, `pdl spec`, `pdl plan`, etc.) |
| **Slash Command Prefix** | `/hsiw:<command>` | **`/pdl:<command>`** | Claude Code & IDE slash commands (`/pdl:writing-specs`, etc.) |
| **Project Memory Root** | `docs/hsiw/` | **`docs/paddlr/`** | Persistent specs (`docs/paddlr/specs/`), plans (`docs/paddlr/plans/`), ADRs |
| **Antigravity Plugin** | `holy-shit-it-works` / `HolyShitItWorks` | `paddlr` / `Paddlr` | `plugin.json` |
| **Claude Code Plugin** | `hsiw` | `paddlr` | `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json` |
| **OpenCode Plugin** | `holy-shit-it-works` | `paddlr` | `package.json`, `index.js`, `index.d.ts`, `.opencode/` |
| **Codex Plugin** | `holy-shit-it-works` | `paddlr` | `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json` |
| **Lifecycle Hooks** | `hsiw-session-start` | `paddlr-session-start` | `hooks.json`, `hooks/hooks.json`, `hooks/session-start.py` |
| **OpenCode Tools** | `hsiw_bootstrap`, `hsiw_status`, `hsiw_scan` | `pdl_bootstrap`, `pdl_status`, `pdl_scan` | `index.js` (with backwards compatibility aliases) |
| **Visual Identity** | Abstract shield & brackets | **The Duck Mascot** | Minimalist geometric duck silhouette & water ripple aesthetic in `assets/logo.svg` |

---

## 3. Scope of Implementation

### In Scope
1. **Manifests & Metadata:** Update `package.json`, `plugin.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `hooks.json`, `hooks/hooks.json`, `.gitattributes`, `.gitignore`.
2. **Visual Asset (`assets/logo.svg`):** Redesign SVG logo to feature "The Duck" mascot with clean developer-tool geometric lines and water-inspired elements.
3. **Runtime & Hooks:**
   - `hooks/session-start.py`: Updated bootstrap context with Paddlr brand story, tagline, and principles.
   - `index.js` & `index.d.ts`: Export `PaddlrPlugin`, implement `pdl_bootstrap`, `pdl_status`, `pdl_scan` tools (supporting `docs/paddlr/` with legacy fallback).
   - `.opencode/plugins/paddlr.js` and `.opencode/INSTALL.md`.
4. **Slash Commands (`commands/`):** Update 8 command files with `# /pdl:<command>`.
5. **Rules & Contributor Guides:**
   - `rules/AGENTS.md`, `rules/CLAUDE.md`.
   - Root `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`.
6. **Documentation (`README.md`, `RELEASE.md`):** Complete brand rewrite of `README.md` reflecting Sections 1–9 of the Brand Brief.
7. **Skills References:** Update path and framework references across all 8 skills (`skills/*`).
8. **Project Memory Migration:** Rename directory `docs/hsiw/` to `docs/paddlr/`.
9. **Test Suites:** Update all tests in `tests/` (`test_commands.py`, `test_plugins.py`, `test_core_skills_architecture.py`, `test_workflow_scenarios.py`, `test_scan_repo.py`, and fixtures) to validate Paddlr contracts.

### Out of Scope
- Modifying the core logic or methodology of the 8 Agent Skills (feature-development, writing-specs, writing-plans, test-driven-development, sre-debugging, code-review, release-management, skill-creator).
- Destructive git operations.

---

## 4. Acceptance Criteria
- [ ] All platform manifests (`package.json`, `plugin.json`, `.claude-plugin`, `.codex-plugin`, `.agents`) correctly identify as `paddlr` with `Paddlr` display name.
- [ ] `assets/logo.svg` embodies the Paddlr Duck mascot.
- [ ] OpenCode plugin exposes `pdl_bootstrap`, `pdl_status`, and `pdl_scan` with `PaddlrPlugin` exports.
- [ ] Slash commands in `commands/` use `/pdl:` prefix and resolve all internal skill links.
- [ ] Canonical project memory path is updated to `docs/paddlr/`.
- [ ] `README.md` fully presents Paddlr's brand story, Duck philosophy, CLI commands, and multi-agent setup.
- [ ] `python scripts/validate_skills.py --verbose` reports 8/8 PASS.
- [ ] `python -m unittest discover -s tests -v` passes 100% (52+ tests).
- [ ] CI Markdown internal link check reports 0 broken links.
