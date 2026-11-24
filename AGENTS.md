# AGENTS.md — Contributing to Paddlr

This file is for agents and people **developing Paddlr itself**. It is never released.

**First read and follow [rules/AGENTS.md](rules/AGENTS.md).** Those rules ship to users and bind work in this repository too.

## Repository Layout Boundary
- `rules/AGENTS.md`, `rules/CLAUDE.md`: Paddlr rules distributed to users. Never put repo-specific contributor conventions in `rules/`.
- Root `AGENTS.md`, `CLAUDE.md`: contributor rules for this repository only.
- `docs/paddlr/`: dev-only specs and plans for this repository (not released).
- `docs/guide/`: user-facing handbook (released).

## Branches & Release
- Work on `dev` (or a branch from `dev`); open pull requests against `dev`.
- Never edit `release` directly; release via `dev` and GitHub Actions (`.github/workflows/release-please.yml` / `.github/workflows/release.yml`).

## Verification Before Reporting Done
Run what CI runs (`.github/workflows/ci.yml`):

```bash
python scripts/validate_skills.py --verbose
python -m unittest discover -s tests -v
python scripts/check_markdown_links.py
```

## Commit Messages
Use [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/): `<type>[(scope)][!]: <description>` (see [CONTRIBUTING.md](CONTRIBUTING.md#commit-message-convention)). Commit only when requested.
