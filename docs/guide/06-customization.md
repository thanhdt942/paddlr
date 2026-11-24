# 6. Customization with `.paddlr.json`

By default, Paddlr stores all project memory under `docs/paddlr/` so it does not collide with existing `docs/` directories and can be gitignored in one line if desired.

## Overriding Paths

To map specs, plans, or ADRs to custom locations in your repository, add an optional `.paddlr.json` file at the repository root:

```json
{
  "root": "docs/paddlr",
  "specs": "docs/paddlr/specs",
  "plans": ".local/plans",
  "decisions": "docs/adr",
  "decisionsIndex": "docs/adr/README.md",
  "project": "docs/paddlr/PROJECT.md",
  "autonomy": {
    "pauseOnAmbiguity": false,
    "pauseBeforeCode": "never"
  }
}
```

## Autonomy Settings (`autonomy`)

Both fields under `autonomy` are optional and validated fail-fast:

- **`pauseOnAmbiguity`** (`boolean`, default `false`): When `false`, Paddlr picks the safest convention-aligned default, logs assumptions in Spec/Plan, and reports them in the final reply/PR. When `true`, Paddlr asks concise clarifying questions before coding if product/UX/acceptance criteria are ambiguous and cannot be settled by code inspection or prototyping.
- **`pauseBeforeCode`** (`"never"` | `"level3"` | `"always"`, default `"never"`): Controls whether Paddlr pauses for Spec/Plan approval before editing production code. Irreversible actions (Hard Stops) always pause regardless of this setting.

## Resolution Rules

- **All keys are optional:** Omitted path keys inherit from `root` (default `docs/paddlr`); omitted `autonomy` keys inherit `{ "pauseOnAmbiguity": false, "pauseBeforeCode": "never" }`.
- **Cascading `root`:** Setting only `{"root": ".paddlr-docs"}` moves `specs`, `plans`, `decisions`, `decisionsIndex`, and `project` under `.paddlr-docs/`.
- **Partial overrides:** Setting `{"decisions": "docs/adr"}` moves only ADRs while keeping specs and plans under `docs/paddlr/`.
- **Strict containment & fail-fast validation:** Every path must be a non-empty relative path contained inside the repository root. Malformed JSON, non-string values, absolute paths, path traversal (`../outside`), or invalid `autonomy` keys/values raise a validation error instead of silently falling back.

Paddlr's stdlib resolver lives in [scripts/paddlr_config.py](../../scripts/paddlr_config.py) (`resolve_memory_paths(repo_root)` and `resolve_autonomy_config(repo_root)`).

Back to [User Guide index](README.md).
