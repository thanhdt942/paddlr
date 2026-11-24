# 1. Setup and Installation

Paddlr works natively across five AI coding agents using the Agent Skills open standard.

## Install by Platform

### Google Antigravity (`agy`)

```bash
agy plugin install https://github.com/thanhdt942/paddlr
```

### Claude Code

```text
/plugin install paddlr --marketplace thanhdt942/paddlr
```

Or in two steps on older versions:

```text
/plugin marketplace add thanhdt942/paddlr
/plugin install paddlr@paddlr
```

### OpenCode

```bash
opencode plugin paddlr@git+https://github.com/thanhdt942/paddlr.git
```

See [.opencode/INSTALL.md](../../.opencode/INSTALL.md) for local linking details.

### OpenAI Codex (`codex`)

```bash
codex plugin marketplace add thanhdt942/paddlr
codex plugin add paddlr@paddlr
```

### Cursor

Clone or add Paddlr as a plugin/rules source and load `rules/AGENTS.md` plus `skills/`. Paddlr does not require vendor-specific extensions or background daemons.

## Initialize a Repository

After installing, run `/setup-paddlr` (or ask your agent to "setup paddlr") to:

1. Initialize `docs/paddlr/` (`specs/`, `plans/`, `decisions/`, `DECISIONS.md`, `PROJECT.md`), or detect existing `docs/adr/` / `docs/specs/` directories and generate a `.paddlr.json` override.
2. Optionally map the three abstract model profiles (`deep-reasoning`, `standard-code`, `fast-mechanical`) if your runtime supports model steering.
3. Optionally create a project-local verification skill via `/create-verification-skill`.

Need quick routing without starting a workflow? Type `/paddlr-help <your question>` for a read-only recommendation, doc link, and copy-paste prompt.

## Verify Your Local Clone

If you are contributing to Paddlr itself, run the same checks CI executes:

```bash
python scripts/validate_skills.py --verbose
python -m unittest discover -s tests -v
python scripts/check_markdown_links.py
```

Next: [Paddlr Mode and playbooks](02-paddlr-mode.md).
