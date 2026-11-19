# Plan: Minimal Landing Page Redesign

Spec: [2026-11-19-minimal-landing-page-redesign.md](../specs/2026-11-19-minimal-landing-page-redesign.md)

## Task 1 — Verify install facts
- **Consumes:** README, manifests, local agent CLIs
- **Produces:** verified command list (spec §2)
- [x] Read `--help` of `claude`, `codex`, `opencode`, `agy` plugin commands
- [x] Sandboxed installs with temp config dirs

## Task 2 — Markup
- **Consumes:** spec §3
- **Produces:** `website/index.html` (semantic, metadata, OG, relative paths)
- [x] Replace 9-section page with 5 sections + footer

## Task 3 — Styles
- **Produces:** `website/assets/css/styles.css` (tokens, single column, responsive, reduced motion)
- [x] Rewrite stylesheet; remove unused theme code

## Task 4 — Behavior
- **Consumes:** `AGENTS` data
- **Produces:** `website/assets/js/main.js` (tabs, render panel, copy)
- [x] Data-driven agent panel, ARIA tabs, clipboard with fallback

## Task 5 — Assets & docs
- **Produces:** `website/assets/images/favicon.svg`, `website/README.md`
- [x] Move favicon, remove unused `logo.svg`

## Task 6 — Deployment
- **Produces:** `.github/workflows/deploy-pages.yml`
- [x] Confirm official actions, permissions, `website/` artifact

## Task 7 — Verification
- [x] Local static server under `/paddlr/` subpath; check assets 200
- [x] Browser check: tabs, keyboard, copy, mobile width, console errors
- [x] `python scripts/validate_skills.py` and `python -m unittest discover -s tests`
- [ ] Deploy after user authorizes commit/push; verify live URL
