# Implementation Plan: Website Layout Redesign & Interactive Agent Installation Hub

- **Date:** 2026-11-19
- **Spec:** [2026-11-19-website-layout-and-agent-hub.md](../specs/2026-11-19-website-layout-and-agent-hub.md)
- **Branch:** `dev`

---

## Task 1 — Stylesheet Upgrade for 9-Section Architecture & Agent Hub
- **Consumes:** Spec Sections 2 & 3
- **Produces:** `website/assets/css/styles.css`
- [x] Refine compact sticky header (`56px`), prominent `Agents` nav link, and active link indicators.
- [x] Style the Agent Compatibility & Installation Hub (`.agent-grid`, `.agent-card`, `.status-badge`, `.install-workbench`, `.method-tabs`, `.cmd-step`, syntax-highlighted terminal tokens, and mobile inline card-expansion layout).
- [x] Style the varied Core Features layout (`.feature-showcase` split hero block + asymmetric supporting blocks with embedded terminal/code snippets).
- [x] Style the 5-step How It Works sequence with code examples and concise Quick Start layout.

## Task 2 — Semantic HTML5 Structure for All 9 Sections
- **Consumes:** Spec Section 2, verified repository manifests & docs
- **Produces:** `website/index.html`
- [x] Update Navigation (`Features`, `Agents`, `How It Works`, `Documentation`, `GitHub`, theme toggle) and Hero section (`Get Started` + `Explore on GitHub` CTAs + verified terminal visual).
- [x] Author `Why Paddlr` (`#why-paddlr`), `Agent Compatibility & Installation Hub` (`#agents`), varied `Core Features` (`#features`), 5-step `How It Works` (`#how-it-works`), concise `Quick Start` (`#quick-start`), comprehensive `Documentation & FAQ` (`#docs`, `#faq`), and minimal `Footer`.

## Task 3 — Data-Driven Vanilla JS Agent Installation Hub & Controls
- **Consumes:** `website/index.html` DOM hooks
- **Produces:** `website/assets/js/main.js`
- [x] Define maintainable `AGENTS_CATALOG` structure for Claude Code, Google Antigravity, OpenCode, and OpenAI Codex (statuses, descriptions, prerequisites, multi-method command steps, verification commands, minimal usage examples, doc links).
- [x] Implement interactive agent card selection (click + keyboard arrows/Enter/Space + URL hash support), secondary installation method switching, dynamic command block rendering with syntax highlighting, and mobile DOM placement directly beneath the active agent card.
- [x] Implement delegated copy-to-clipboard handler with `Copied!` visual feedback, theme toggle, mobile navigation drawer, and scroll-spy active nav highlighting.

## Task 4 — Verification & Live GitHub Pages Deployment
- **Consumes:** `website/`, `.github/workflows/deploy-pages.yml`
- **Produces:** Live deployment at `https://thanhdt942.github.io/paddlr/`
- [x] Run repository CI checks (`validate_skills.py`, `unittest`, `check_markdown_links.py`) and static HTML anchor/asset verification.
- [x] Commit and push to `origin/dev`, monitor `Deploy Pages` workflow completion, and verify live HTTP responses at `https://thanhdt942.github.io/paddlr/`.
