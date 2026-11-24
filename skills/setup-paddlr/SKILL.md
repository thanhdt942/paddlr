---
name: setup-paddlr
description: "Initialize Paddlr project memory (docs/paddlr/ or .paddlr.json), configure optional model profiles (deep-reasoning, standard-code, fast-mechanical), and optionally offer /create-verification-skill. Use for /setup-paddlr, 'setup paddlr', or 'configure paddlr'."
---

# Setup Paddlr

Interactive, idempotent setup for adopting Paddlr in a repository. Re-running this skill safely updates configuration without overwriting existing specs, plans, or ADRs.

## Step 1: Scan Target Repository Layout

Inspect the repository root before creating any files:

1. Check whether `.paddlr.json` already exists. If so, read it and preserve existing valid overrides.
2. Check whether `docs/paddlr/` already exists.
3. Check for existing documentation conventions that should not be collided with, such as `docs/adr/`, `docs/adrs/`, or `docs/specs/`.

## Step 2: Initialize Project Memory (`docs/paddlr/` or `.paddlr.json`)

- **If existing `docs/adr/` or `docs/specs/` are detected** (and no `.paddlr.json` maps them yet):
  - Propose generating `.paddlr.json` at the repository root so Paddlr reuses the repository's conventions instead of creating duplicate folders.
  - Use the exact schema validated by [paddlr_config.py](../../scripts/paddlr_config.py) (all fields optional, relative paths strictly contained inside the repository root):
    ```json
    {
      "root": "docs/paddlr",
      "specs": "docs/specs",
      "plans": "docs/paddlr/plans",
      "decisions": "docs/adr",
      "decisionsIndex": "docs/adr/DECISIONS.md",
      "project": "docs/paddlr/PROJECT.md",
      "autonomy": {
        "pauseOnAmbiguity": false,
        "pauseBeforeCode": "never"
      }
    }
    ```
  - Optionally confirm whether the user wants the default autonomy settings (`pauseOnAmbiguity: false`, `pauseBeforeCode: "never"`) or a different preference (`pauseOnAmbiguity: true` to ask on ambiguous requirements, or `pauseBeforeCode: "level3"` / `"always"`).
  - Write `.paddlr.json` only after the user confirms the proposed mapping (or accept the default `docs/paddlr/` layout if they prefer isolation).
- **Initialize missing directories and index files idempotently:**
  - Ensure `specs/`, `plans/`, and `decisions/` directories exist at the resolved paths (default `docs/paddlr/`).
  - Create `DECISIONS.md` with the compact ADR table header if missing (never overwrite an existing `DECISIONS.md`).
  - Create `PROJECT.md` with a concise snapshot of the repository's detected stack, directory structure, and test commands if missing (never overwrite an existing `PROJECT.md`).

## Step 3: Optional Model Profile Steering (`model.steer`)

Paddlr defines three abstract model profiles in [runtime-adapters.md](../paddlr-mode/references/runtime-adapters.md):

- `deep-reasoning` — architecture design, contested red-teaming (`interrogate`, `arena`), root-cause diagnosis.
- `standard-code` — feature implementation, TDD, refactoring.
- `fast-mechanical` — bulk linting, formatting, typo fixes, routine verification.

1. Check whether the active host runtime supports `model.steer` (per-turn or per-subagent model selection).
2. **If unsupported:** Skip this step gracefully with a one-line note that all workflows will run on the host's active default model. Do not create vendor-specific rule files or fail.
3. **If supported:** Ask the user (via `ui.prompt` or plain text) whether they want to map models to the three profiles or keep the runtime default. Record any agreed mapping in the runtime's standard configuration or session notes without hardcoding proprietary tool paths.

## Step 4: Optional Verification Skill Offer

Check whether the repository already has a project-local verification skill (`verify-*`) or an automated end-to-end test harness that drives the real app.

- If absent, offer **once** without pushing:
  > "Your repo does not have a project-local verification skill yet. Want me to generate one with `/create-verification-skill` so agents can prove changes against the real app?"
- On yes, invoke [create-verification-skill](../create-verification-skill/SKILL.md). On no, finish cleanly.

## Step 5: Confirm Setup

Report concisely:
- Resolved project memory paths (and whether `.paddlr.json` was created/updated)
- Files created vs. preserved untouched
- Model profile steering status (configured or skipped on default model)
- Next step: start a task with `/paddlr-mode` or ask `/paddlr-help` for guidance
