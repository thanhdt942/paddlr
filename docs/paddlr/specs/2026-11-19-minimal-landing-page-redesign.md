# Spec: Minimal Landing Page Redesign

- **Date:** 2026-11-19
- **Level:** 2 (Feature Development)
- **Supersedes (design only):** `2026-11-19-website-layout-and-agent-hub.md` (9-section layout)

## 1. Goal

Replace the current 9-section website with a small, minimal, developer-focused landing page that:

1. Explains what Paddlr is and why a developer would use it.
2. Lets a visitor pick their coding agent and copy verified install commands.

Design test: if an element does not help visitors understand, install, or use Paddlr, remove it.

## 2. Verified Facts (source of truth)

| Fact | Evidence |
|---|---|
| Paddlr = 8 Agent Skills + rules + SessionStart hook, persists memory in `docs/paddlr/` | `skills/`, `rules/`, `hooks/`, README §6 |
| Antigravity: `agy plugin install https://github.com/thanhdt942/paddlr` | Sandboxed install (temp `HOME`): 8 skills, 2 rules, 1 hook installed |
| Codex: `codex plugin marketplace add thanhdt942/paddlr` then `codex plugin add paddlr@paddlr` | Sandboxed install (temp `CODEX_HOME`); `codex plugin add --help` requires `PLUGIN@MARKETPLACE` or `--marketplace` |
| Claude Code: `/plugin install paddlr --marketplace thanhdt942/paddlr` | Sandboxed install (temp `CLAUDE_CONFIG_DIR`): `paddlr@paddlr` installed; `claude plugin install --help` documents `--marketplace` |
| OpenCode: `opencode plugin paddlr@git+https://github.com/thanhdt942/paddlr.git` | Sandboxed install: writes `"plugin": [...]` to `.opencode/opencode.json`; `-g` for global per `--help` |
| There is no `pdl` CLI binary | `package.json` has no `bin`; no executable in repo |

### Discrepancies found in README (not fixed in this change, reported to user)

- `codex plugin add paddlr` fails without `@paddlr` marketplace suffix.
- `opencode plugin add ...` — the installed OpenCode CLI has no `add` subcommand.
- `pdl init|spec|plan|...` CLI commands do not exist.
- Slash commands are documented as `/pdl:*`; Claude Code namespaces plugin commands by plugin name (`paddlr`).

The website only shows commands verified above.

## 3. Structure

1. **Nav** — wordmark, Docs (README), GitHub.
2. **Hero** — name, tagline, one-sentence description, `Get started` (→ `#installation`), `View on GitHub`.
3. **About** (`#about`) — what it is, the problem, what you get (8 skills list), who it is for.
4. **Install** (`#installation`) — agent tabs (ARIA tablist) + one panel: status, prerequisites, method(s), command blocks with copy, verify step, docs link.
5. **Usage** (`#usage`) — 3 prompt-based examples with expected artifacts.
6. **Footer** — GitHub, Docs, License (Apache-2.0), Contributing.

## 4. Acceptance Criteria

- [x] Agent data lives in a single `AGENTS` array in `main.js`, separate from rendering.
- [x] Tabs: click and Arrow/Home/End keys switch agents; one panel visible; visible focus states.
- [x] Each command in its own block with a working copy button and "Copied" feedback (with `aria-live`).
- [x] No JS console errors; without JS, a `<noscript>` note links to the README install guide.
- [x] All asset paths relative; works under `/paddlr/`.
- [x] No horizontal overflow at 360px; content width ~800px.
- [x] Respects `prefers-reduced-motion`; contrast AA.
- [x] `deploy-pages.yml` deploys `website/` with official Pages actions and minimal permissions.

## 5. Out of Scope

- Fixing README install commands (separate change, needs maintainer decision).
- Dark mode, analytics, custom domain.
