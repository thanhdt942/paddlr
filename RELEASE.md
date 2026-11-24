# Release Configuration

## Release Destinations
- Git Hosting: Confirmed (GitHub: `https://github.com/thanhdt942/paddlr`)
- Release Platform: Confirmed (GitHub Releases via `.github/workflows/release.yml`)
- Package Registry: Not Applicable
- Deployment Targets: Not Applicable

## Versioning
- Strategy: Confirmed (Semantic Versioning 2.0.0 — `MAJOR.MINOR.PATCH`)
- Current Version: Confirmed (`1.2.0`)
- Version Sources: Confirmed (`plugin.json`, `package.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `.release-please-manifest.json`)
- Format: Confirmed (Manifests: `X.Y.Z`; Git tags: `vX.Y.Z`)
- Pre-release: Not Applicable

## Git Conventions
- Source Branch: Confirmed (`dev`)
- Release Branch: Confirmed (`release` — auto-generated from `dev`, never edit directly)
- Tag Format: Confirmed (`vX.Y.Z`, e.g. `v3.3.0`)
- Release Commit Convention: Confirmed (Conventional Commits: `feat(skills): ...` or `chore(release): ...`)
- Tag Push Rules: Confirmed (Requires explicit authorization before push)

## Changelog
- File: Confirmed (`CHANGELOG.md`)
- Format: Confirmed (Keep a Changelog 1.0.0 standard)
- Categories: Confirmed (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`)

## Validation
- Skills Open Standard: `python scripts/validate_skills.py --verbose`
- Unit & Integration Test Suite: `python -m unittest discover -s tests -v`
- Required Gates: All skill validation and unit tests must pass before execution.

## Release Execution
- Automation Workflow: `.github/workflows/release.yml` (triggered via workflow_dispatch with `version`)
- Required Approvals: Explicit user authorization required before creating Git commits, tags, or publishing releases.

## Post-release
- Verification: Confirm Git tag exists, verify GitHub release notes, run automated test suites.
- Rollback: Manual Git tag/release removal upon explicit user authorization; no auto-rollback.
