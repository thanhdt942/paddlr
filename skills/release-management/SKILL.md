---
name: release-management
description: Manage the end-to-end software release lifecycle and persist project release conventions in `RELEASE.md`. Use when setting up release configuration, planning, preparing, validating, executing, verifying, or reporting software releases across any Git platform, package registry, or deployment target.
---

# Release Management

Platform-agnostic workflow for managing software releases and persisting confirmed project release policies.

## Core Rules

- **Configuration first:** Check existing release config before acting.
- **Ask when unknown:** Never invent or silently alter release policy.
- **Persist confirmed policy:** Save confirmed settings to `RELEASE.md` (or reuse an equivalent existing config file—never duplicate).
- **Adaptive & minimal:** Run only steps applicable to the project (supports single-package, monorepo, multi-destination, non-SemVer, no-changelog, manual/automated deploy).
- **Safe by default:** Require explicit authorization for mutating/external actions. Preparing a release does not authorize publishing or deploying.
- **Evidence-based:** Never claim success without verification output from the target system.
- **Out of scope:** Designing CI/CD infrastructure, building deployment platforms, unauthorized rollbacks or destructive actions.

## Persistent Configuration (`RELEASE.md`)

Track only applicable categories:
1. **Release Destinations:** Git hosting, release platform, package/container registries, deployment targets, other channels.
2. **Versioning:** Scheme (SemVer/CalVer/custom), version source file(s), format, bump rules, pre-release format, breaking-change rules.
3. **Git Conventions:** Source/release branch, tag format, release commit convention, tag push rules.
4. **Changelog & Release Notes:** Enabled, file path, format, change categories, migration/breaking notes.
5. **Build & Validation:** Build, test, lint/static analysis, artifact commands, required gates.
6. **Release Execution:** Publish/deploy commands or workflows, artifact naming, manual/approval steps.
7. **Post-release:** Smoke tests, health checks, verification commands, rollback procedure, success criteria.

Classify every item as `Confirmed`, `Inferred`, `Unknown`, or `Not Applicable`. Never promote `Inferred` or `Unknown` to policy without user confirmation.

### First-Time Setup
1. **Discover:** Inspect repo docs, existing release config, manifests, branches/tags, changelog, scripts, CI/CD workflows, and release history.
2. **Classify:** Map findings to the categories above (`Confirmed`, `Inferred`, `Unknown`, `Not Applicable`).
3. **Ask:** Group and ask only missing, policy-critical questions. Skip already-confirmed or irrelevant items. Partial setup is allowed.
4. **Save:** Write confirmed settings to `RELEASE.md` (mark `Unknown`/`Not Applicable` explicitly; preserve unrelated config).
5. **Confirm:** Re-read the saved file to verify integrity, then report saved vs. remaining unknown items.

### Subsequent Runs & Updates
- Read `RELEASE.md`, verify it still matches the repo, and reuse confirmed rules without re-asking.
- If config drifted from the repo, alert the user and ask before changing policy.
- On user updates: modify only requested sections, check for rule conflicts, preserve unaffected settings, and append (do not replace) when adding a new destination.

### Minimal `RELEASE.md` Structure
Include only applicable sections:
```markdown
# Release Configuration

## Release Destinations
- Git Hosting: <Confirmed | Unknown>
- Release Platform: <Confirmed | Not Applicable>
- Package Registry: <Confirmed | Not Applicable>
- Deployment Targets: <Confirmed | Not Applicable>

## Versioning
- Strategy / Source / Format / Pre-release: <Confirmed>

## Git Conventions
- Source Branch / Release Branch / Tag Format: <Confirmed>

## Changelog
- File / Format: <Confirmed | Not Applicable>

## Validation
- Build / Tests / Lint: <Commands>

## Release Execution
- Publish / Deploy / Approvals: <Commands & Rules>

## Post-release
- Verification / Rollback: <Checks & Procedure>
```

## Release Workflow

Adapt to the project's config and release type (`Patch`, `Minor`, `Major`, `Pre-release`, `Hotfix`). Skip inapplicable steps.

1. **Configuration Discovery:** Load and verify release config; resolve missing or drifted items; persist any newly confirmed rules.
2. **Release Planning:** Define release type, target version, scope, source branch/commit, destinations, and applicable steps.
3. **Release Preparation:** Check scope, bump version, update changelog/release notes, and verify metadata/dependencies.
4. **Release Validation:** Run required build, test, lint, version consistency, changelog, and artifact checks. **Halt if any required check fails.**
5. **Release Execution:** Execute configured steps (commit, tag, push, package, publish, create release, deploy) only after required authorization.
6. **Post-release Verification:** Verify Git tag/commit, published artifacts/packages, release page, deployment status, and smoke/health checks. Do not auto-rollback without authorization.
7. **Release Reporting:** Report version, type, source commit, tag, destinations, artifacts, validation results, deployment status, post-release checks, and known issues/pending actions. Label each item `Completed`, `Failed`, `Skipped`, or `Pending` with evidence.

## Safety & Authorization

- **Proceed freely (low-risk):** Inspect repo, read config, review Git history, run builds/tests, draft plans/release notes.
- **Require explicit authorization:** Edit release config/metadata, create/push commits or tags, publish packages, create public releases, deploy, run DB migrations, overwrite artifacts, or rollback.
