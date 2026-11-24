# Contributing to Paddlr

Thank you for contributing to Paddlr. Please read our [Code of Conduct](CODE_OF_CONDUCT.md) and [Operating Rules](rules/AGENTS.md) before opening a pull request.

## 1. Contribution Principles

1. **Agent-Agnostic:** Keep skills, playbooks, and contracts portable across Antigravity, Claude Code, Cursor, OpenCode, and Codex. Never require vendor-only tools outside `runtime-adapters.md`.
2. **Portable-First:** Follow the Agent Skills open standard (`skills/<name>/SKILL.md`) with zero-dependency Python 3.10+ stdlib utilities.
3. **Minimal Overhead:** Avoid unnecessary abstractions, dependencies, databases, or background daemons. Keep non-setup skills lazy-loaded (`disable-model-invocation: true`).
4. **Evidence-Based:** Verify every change with real command output before reporting done.

## 2. Repository Areas

- **Skills (`skills/`):** Agent Skills, `paddlr-mode` playbooks/references, and the 26 `principle-*` skills.
- **User Guide (`docs/guide/`):** End-user onboarding and reference chapters.
- **Contributor Memory (`docs/paddlr/`):** Dev-only specs and plans for Paddlr itself.
- **Plugin Adapters:** `plugin.json`, `.claude-plugin/`, `.codex-plugin/`, `.agents/`, `index.js`, `.opencode/`, and `hooks/`.

## 3. Skill Authoring Layout

```text
skills/<skill-name>/
├── SKILL.md          # Concise entrypoint with YAML frontmatter (name, description)
├── references/       # Progressive disclosure guides (optional)
└── scripts/          # Deterministic helper scripts (optional)
```

## 4. Local Validation

Run the full CI suite before submitting a PR:

```bash
python scripts/validate_skills.py --verbose
python -m unittest discover -s tests -v
python scripts/check_markdown_links.py
```

## 5. Pull Request Process

1. Branch from `dev` (e.g., `feat/add-skill`, `fix/link-check`) and open pull requests against `dev`. Never edit `release` directly.
2. Keep each PR focused on one logical change.
3. Format commits using [Commit Message Convention](#commit-message-convention).
4. Use the [Pull Request Template](.github/pull_request_template.md) and include passing verification output.

### Commit Message Convention

Commits follow [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

```text
<type>[(scope)][!]: <description>

[optional body]

[optional footer(s)]
```

| Type | Use for | SemVer |
|---|---|---|
| `feat` | New capability | MINOR |
| `fix` | Bug fix | PATCH |
| `docs`, `test`, `refactor`, `perf`, `style`, `build`, `ci`, `chore` | Other changes | none |

- **Breaking change:** append `!` after the type/scope, or add a `BREAKING CHANGE: <description>` footer (MAJOR).
- **Scope** (optional): affected area in parentheses, e.g. `skills`, `paddlr`, `core`, `plugins`, `release`.
- **Footers:** git trailer format, e.g. `Refs: #12`.
