# Implementation Plan: Paddlr Landing Page & Documentation

- **Date:** 2026-11-19
- **Spec:** [2026-11-19-paddlr-landing-page.md](../specs/2026-11-19-paddlr-landing-page.md)
- **Branch:** `dev`

---

## Task 1 — Brand Assets & Favicon Setup
- **Consumes:** `assets/logo.svg`
- **Produces:** `website/assets/images/logo.svg`, `website/favicon.svg`
- [x] Copy existing `assets/logo.svg` into `website/assets/images/logo.svg`.
- [x] Create clean, crisp `website/favicon.svg` derived from the Paddlr logo mark for crisp rendering at 16px–32px.

## Task 2 — Design Tokens & Responsive Stylesheet
- **Consumes:** Spec Section 3 & 4
- **Produces:** `website/assets/css/styles.css`
- [x] Define CSS custom properties for light and dark themes (surface, text, border, subtle slate/cyan-teal accents, code block tokens, typography scale, spacing scale).
- [x] Style layout primitives, responsive header & mobile drawer, hero + terminal preview, comparison table, feature grid, workflow stepper, platform tabs, documentation sidebar/sections, code blocks with copy button, FAQ accordion, and footer.
- [x] Ensure `prefers-reduced-motion`, focus-visible outlines, and responsive breakpoints (mobile, tablet, desktop).

## Task 3 — Semantic HTML5 Page & Verified Documentation Content
- **Consumes:** Spec Sections 2 & 3, repository source files (`README.md`, `skills/`, `commands/`, `index.js`, `hooks/session-start.py`, `rules/AGENTS.md`, `scripts/`, `.opencode/INSTALL.md`, `LICENSE`)
- **Produces:** `website/index.html`
- [x] Add complete SEO, Open Graph, Twitter card, canonical URL, favicon, and anti-FOUC inline theme initialization script.
- [x] Author all 9 sections (Navigation, Hero, Introduction, Features, How It Works, Quick Start, Documentation / Usage Guide, FAQ, Footer) using strictly verified repository facts and relative asset paths.

## Task 4 — Lightweight Vanilla JavaScript Interactions
- **Consumes:** `website/index.html` DOM contracts
- **Produces:** `website/assets/js/main.js`
- [x] Implement light/dark theme toggle with `localStorage` persistence and system preference fallback.
- [x] Implement accessible mobile navigation menu toggle (`aria-expanded`, `Escape` key, outside-click/link-click close).
- [x] Implement accessible platform install tabs (`role="tablist"`, arrow-key & click navigation) for Quick Start.
- [x] Implement copy-to-clipboard buttons for all code blocks with visual confirmation (`Copied`) and fallback support.
- [x] Implement active-section scroll highlighting for navigation/docs links.

## Task 5 — GitHub Actions Pages Workflow
- **Consumes:** Spec Section 5
- **Produces:** `.github/workflows/deploy-pages.yml`
- [x] Author GitHub Actions workflow using `actions/checkout@v4`, `actions/configure-pages@v5`, `actions/upload-pages-artifact@v3` (`path: website`), and `actions/deploy-pages@v4`.
- [x] Configure minimal permissions (`contents: read`, `pages: write`, `id-token: write`), `pages` concurrency group, `github-pages` environment, and triggers (`push` on `dev` and `release` + `workflow_dispatch`).

## Task 6 — Local Verification & Repo CI Gates
- **Consumes:** `website/`, `.github/workflows/deploy-pages.yml`, existing test suite
- **Produces:** Verified local test & browser QA evidence
- [x] Run existing CI gates: `python scripts/validate_skills.py --verbose`, `python -m unittest discover -s tests -v`, `python scripts/check_markdown_links.py`.
- [x] Serve `website/` locally under a `/paddlr/` subpath check and verify HTML/CSS/JS, console errors, responsive layout, theme toggle, tabs, copy buttons, mobile menu, and all internal anchors.

## Task 7 — GitHub Pages Configuration, Commit, Push & Live Deployment Verification
- **Consumes:** Verified local files, `gh` CLI credentials
- **Produces:** Live website at `https://thanhdt942.github.io/paddlr/`
- [x] Configure GitHub Pages (`build_type: workflow`) via `gh api` and ensure `dev` branch is permitted in the `github-pages` environment.
- [x] Stage and commit changes on `dev` using Conventional Commits (`feat(website): ...`) and push to `origin/dev`.
- [x] Monitor the `Deploy Pages` workflow run via `gh run list` / `gh run watch` until completion.
- [x] Verify the live URL `https://thanhdt942.github.io/paddlr/` in a real browser and confirm assets, interactivity, and zero console errors.
