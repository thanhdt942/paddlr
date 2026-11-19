# Feature Specification: Paddlr Landing Page & Documentation

- **Date:** 2026-11-19
- **Author:** Antigravity / Paddlr Engineering Discipline
- **Status:** Approved
- **Target URL:** `https://thanhdt942.github.io/paddlr/`
- **Repository:** `https://github.com/thanhdt942/paddlr`

---

## 1. Objective

Build a clean, fast, production-ready single-page landing website and user documentation portal for **Paddlr** inside `website/`, using pure HTML5, CSS3, and vanilla JavaScript (zero frameworks, zero build step), and deploy it to GitHub Pages via GitHub Actions.

The website serves two primary goals:
1. **Product Introduction:** Communicate Paddlr's philosophy ("Simple on the Surface. Sophisticated Underneath."), what problem it solves, its core capabilities, and why developers use it.
2. **User Documentation:** Enable developers to install, configure, and use Paddlr across supported AI coding agents (Google Antigravity, Claude Code, OpenCode, OpenAI Codex) without reverse-engineering the repository.

---

## 2. Source-of-Truth Scope Boundaries

All content must strictly reflect verified repository functionality:

- **In Scope (Verified Capabilities):**
  - Brand identity: **Paddlr**, tagline *"Simple on the Surface. Sophisticated Underneath."*, implicit duck/water-surface philosophy (*above the surface* vs. *below the surface*).
  - 4 native AI agent integrations: Google Antigravity (`agy`), Claude Code, OpenCode (`@opencode/plugin` v2 & `@opencode-ai/plugin` v1), OpenAI Codex (`codex`).
  - 8 Agent Skills conforming to the Agent Skills open standard: `feature-development`, `writing-specs`, `writing-plans`, `test-driven-development`, `sre-debugging`, `code-review`, `release-management`, `skill-creator`.
  - 8 Slash Commands in `commands/` (`/pdl:feature-development`, `/pdl:writing-specs`, `/pdl:writing-plans`, `/pdl:test-driven-development`, `/pdl:sre-debugging`, `/pdl:code-review`, `/pdl:release-management`, `/pdl:skill-creator`).
  - Engineering workflow loop (`Understand -> Analyze & Plan -> Incremental Implement -> Evidence Verify -> Finalize`) and complexity levels (Level 1 / 2 / 3).
  - Persistent project memory under `docs/paddlr/` (`specs/`, `plans/`, `decisions/`, `DECISIONS.md`, `PROGRESS.md`, `PLAN.md`).
  - OpenCode plugin tools (`pdl_bootstrap`, `pdl_status`, `pdl_scan`) and lifecycle/safety hooks (`session.created`, `experimental.chat.system.transform`, `tool.execute.before`).
  - SessionStart hook (`hooks/session-start.py`) supporting Antigravity and Claude Code / Cursor / Gemini CLI contracts.
  - Rules & guardrails (`rules/AGENTS.md`, `rules/CLAUDE.md`) and verification scripts (`scripts/scan_repo.py`, `scripts/validate_skills.py`, `scripts/check_markdown_links.py`).
  - Apache 2.0 License.
- **Out of Scope:**
  - Unimplemented `pdl` standalone CLI binary (`pdl init`, `pdl spec`, etc. — omitted per user confirmation).
  - Modifying existing Paddlr plugin, skill, hook, or test behavior.
  - Adding frameworks, bundlers, or npm build dependencies.

---

## 3. Page Architecture & Functional Requirements

1. **Navigation (`<header>` / `<nav>`):**
   - Paddlr wordmark + subtle geometric logo mark (`assets/images/logo.svg`).
   - Section links: Features (`#features`), How It Works (`#how-it-works`), Quick Start (`#quick-start`), Docs (`#docs`), FAQ (`#faq`).
   - External link: GitHub repository (`https://github.com/thanhdt942/paddlr`).
   - Light/Dark theme toggle persisting to `localStorage` and honoring `prefers-color-scheme`.
   - Accessible mobile menu drawer/toggle with keyboard (`Escape`) and focus handling.
2. **Hero Section:**
   - Product name, tagline badge, concise headline, value proposition.
   - Primary CTA (`Get Started` -> `#quick-start`) and Secondary CTA (`View on GitHub`).
   - Realistic interactive terminal/session preview showing actual Paddlr installation and `/pdl:feature-development` + `scripts/validate_skills.py` output.
3. **Introduction (`#introduction`):**
   - What Paddlr is and is not (concise comparison), why it exists, and the Above/Below the Surface philosophy.
4. **Core Features (`#features`):**
   - Focused set of real capabilities: Agent-Agnostic Plugins, 8 Composable Agent Skills, Persistent Project Memory (`docs/paddlr/`), Risk-Proportional Workflows, Evidence-Based Quality Gates, Built-in Safety Guardrails & Hooks.
5. **How It Works (`#how-it-works`):**
   - Visual 5-step engineering workflow flow (`Understand -> Analyze & Plan -> Incremental Implement -> Evidence Verify -> Finalize`) showing how skills, rules, and `docs/paddlr/` interact.
6. **Quick Start (`#quick-start`):**
   - Prerequisites (Python 3.10+, Git, supported AI coding agent).
   - Interactive platform tabs (Google Antigravity, Claude Code, OpenCode, OpenAI Codex) with exact verified install commands and copy-to-clipboard buttons.
   - First usage example (`/pdl:feature-development` / `/pdl:writing-specs`) and expected output (SessionStart bootstrap + `docs/paddlr/` artifacts + `validate_skills.py` check).
7. **Documentation / Usage Guide (`#docs`):**
   - Logical subsections with in-page navigation:
     - Installation & Platform Setup (including OpenCode `opencode.json` and local linking).
     - Project Memory & Configuration (`docs/paddlr/` layout, `rules/AGENTS.md`, `rules/CLAUDE.md`).
     - Slash Commands Reference (all 8 `/pdl:*` commands).
     - Agent Skills Reference (all 8 skills with when-to-use guidance).
     - OpenCode Tools & Lifecycle Hooks (`pdl_bootstrap`, `pdl_status`, `pdl_scan`, `session-start.py`, destructive git guardrail).
     - Utility Scripts & Verification (`scan_repo.py`, `validate_skills.py`, `check_markdown_links.py`).
     - Customization & Authoring Skills (`/pdl:skill-creator`, `rules/AGENTS.md`).
     - Troubleshooting (real issues: Python 3.10+ for hooks/scripts, OpenCode v1 `plugin` vs v2 `plugins`, destructive git command guardrail, verifying plugin load).
8. **FAQ (`#faq`):**
   - Accessible `<details>`/`<summary>` accordion answering real questions grounded in the repository.
9. **Footer:**
   - Paddlr wordmark & tagline, documentation links, GitHub repository & issues/contributing links, Apache 2.0 License link, copyright notice.

---

## 4. Design & Technical Requirements

- **Stack:** Pure HTML5, CSS3 (custom properties / design tokens), Vanilla ES6 JavaScript.
- **Visual Direction:** Minimalist, crisp developer-tool aesthetic inspired by Paddlr's slate/oceanic-teal palette (`#0f172a`, `#0284c7`, `#06b6d4`, `#10b981`) with clean light mode and deep slate dark mode; generous whitespace; zero excessive gradients or stock imagery; duck mascot kept subtle in logo/favicon only.
- **Relative Paths:** All CSS, JS, image, and favicon paths strictly relative (`./assets/...`, `./favicon.svg`) so the site works seamlessly at `/paddlr/` and locally.
- **SEO & Metadata:** `<title>`, `<meta name="description">`, canonical URL, Open Graph (`og:*`), Twitter card metadata, SVG favicon.
- **Accessibility:** Skip-to-content link, semantic landmarks (`header`, `nav`, `main`, `section`, `footer`), proper heading hierarchy (`h1` -> `h2` -> `h3`), ARIA attributes on tabs/menu/theme toggle/copy buttons, keyboard navigation, sufficient contrast in both themes.

---

## 5. GitHub Pages Deployment Specification

- **Workflow:** `.github/workflows/deploy-pages.yml`
- **Triggers:**
  - `push` to `dev` and `release` branches (filtered on `website/**` and `.github/workflows/deploy-pages.yml`).
  - `workflow_dispatch` for manual deployment.
- **Permissions:** `contents: read`, `pages: write`, `id-token: write`.
- **Environment:** `github-pages` with `url: ${{ steps.deployment.outputs.page_url }}`.
- **Steps:** `actions/checkout@v4` -> `actions/configure-pages@v5` -> `actions/upload-pages-artifact@v3` (`path: website`) -> `actions/deploy-pages@v4`.
- **GitHub Repository Settings:** Enable GitHub Pages with `build_type: workflow` and allow `dev` branch in the `github-pages` deployment environment so pushes to `dev` deploy to `https://thanhdt942.github.io/paddlr/`.

---

## 6. Acceptance Criteria

- [ ] `website/` directory contains `index.html`, `favicon.svg`, `assets/css/styles.css`, `assets/js/main.js`, and `assets/images/logo.svg` with zero external runtime dependencies.
- [ ] All documented commands, skills, slash commands, tools, hooks, and paths match the repository source of truth.
- [ ] Light/dark mode toggle, mobile navigation, platform install tabs, copy-to-clipboard buttons, and FAQ accordions work cleanly with zero console errors.
- [ ] Existing CI checks (`python scripts/validate_skills.py`, `python -m unittest discover -s tests`, `python scripts/check_markdown_links.py`) all PASS.
- [ ] `.github/workflows/deploy-pages.yml` deploys `website/` to `https://thanhdt942.github.io/paddlr/` and live verification confirms HTTP 200 and full rendering.
