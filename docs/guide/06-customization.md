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
  "project": "docs/paddlr/PROJECT.md"
}
```

## Resolution Rules

- **All keys are optional:** Omitted keys inherit from `root` (default `docs/paddlr`).
- **Cascading `root`:** Setting only `{"root": ".paddlr-docs"}` moves `specs`, `plans`, `decisions`, `decisionsIndex`, and `project` under `.paddlr-docs/`.
- **Partial overrides:** Setting `{"decisions": "docs/adr"}` moves only ADRs while keeping specs and plans under `docs/paddlr/`.
- **Strict containment & fail-fast validation:** Every path must be a non-empty relative path contained inside the repository root. Malformed JSON, non-string values, absolute paths, or path traversal (`../outside`) raise a validation error instead of silently writing to the wrong directory.

Paddlr's stdlib resolver lives in [scripts/paddlr_config.py](../../scripts/paddlr_config.py) (`resolve_memory_paths(repo_root)`).

Back to [User Guide index](README.md).
