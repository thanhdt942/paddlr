# Paddlr

<p align="center">
  <img src="assets/logo.svg" alt="Paddlr Logo" width="140" height="140" />
</p>

<p align="center">
  <strong>Simple on the Surface. Sophisticated Underneath.</strong><br>
  <em>An agent-agnostic software engineering framework turning spec-driven design, TDD, scientific debugging, and persistent project memory into reusable AI Agent Skills.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License"></a>
  <a href="tests"><img src="https://img.shields.io/badge/Tests-PASS-brightgreen.svg" alt="Tests"></a>
  <a href="plugin.json"><img src="https://img.shields.io/badge/Antigravity-Plugin-blue.svg" alt="Antigravity Plugin"></a>
  <a href=".claude-plugin/plugin.json"><img src="https://img.shields.io/badge/Claude%20Code-Plugin-purple.svg" alt="Claude Code Plugin"></a>
  <a href=".opencode/INSTALL.md"><img src="https://img.shields.io/badge/OpenCode-Plugin-green.svg" alt="OpenCode Plugin"></a>
  <a href=".codex-plugin/plugin.json"><img src="https://img.shields.io/badge/Codex-Plugin-black.svg" alt="Codex Plugin"></a>
</p>

---

## Philosophy

Like a duck gliding across water, Paddlr keeps the developer experience calm and frictionless on the surface while paddling with engineering discipline underneath:

- **Spec-Driven Design & Memory:** Durable specs, contract-first plans, and immutable ADRs in `docs/paddlr/` (customizable via `.paddlr.json`).
- **Reversibility-First Autonomy:** Level 1 runs directly; Level 2 reversible branch work proceeds without pre-code blocking; Level 3 architectural changes and hard stops always pause for approval.
- **Agent-Agnostic by Design:** Zero vendor lock-in. Runs natively on Google Antigravity, Claude Code, Cursor, OpenAI Codex, and OpenCode.

Read the full handbook in the **[User Guide](docs/guide/README.md)**.

---

## Quick Start & Installation

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

See [.opencode/INSTALL.md](.opencode/INSTALL.md) for local linking and configuration details.

### OpenAI Codex (`codex`)

```bash
codex plugin marketplace add thanhdt942/paddlr
codex plugin add paddlr@paddlr
```

### Cursor

Add Paddlr as a plugin or rules/skills source and load `rules/AGENTS.md` plus `skills/`.

After installing, run `/setup-paddlr` (or ask your agent to *"setup paddlr"*) to initialize `docs/paddlr/` or generate a `.paddlr.json` override. Type `/paddlr-help <question>` for read-only routing without executing tasks.

---

## Core Skills

Paddlr ships **57 Agent Skills** (all lazy-loaded with `disable-model-invocation: true` except `setup-paddlr`), including 22 playbooks under `paddlr-mode` and 26 engineering principles:

| Skill | Purpose |
|---|---|
| `paddlr-mode` | Single-door orchestration mode with 22 playbooks and 26 principles |
| `setup-paddlr` | Initialize `docs/paddlr/` or `.paddlr.json` and optional model profiles |
| `paddlr-help` | Read-only advisor routing questions to skills, playbooks, principles, and prompts |
| `feature-development` | 5-phase SDD feature delivery lifecycle |
| `writing-specs` / `writing-plans` | Feature specifications and bite-sized contract-first plans |
| `writing-decisions` / `sync-docs` | Immutable ADRs (`/adr`) and mandatory pre-PR doc-drift checks |
| `test-driven-development` | Strict RED -> GREEN -> REFACTOR execution |
| `sre-debugging` | Evidence-based root-cause investigation before fixing |
| `code-review` / `interrogate` | Spec-alignment review and adversarial red-teaming |
| `no-comments` / `unslop` / `correct` | Comment/workaround audit, prose cleanup, and structural mistake prevention |
| `why` / `how` / `architect` | Historical rationale, runtime tracing, and boundary/type modeling |
| `release-management` / `skill-creator` | Governed releases (`RELEASE.md`) and authoring new Agent Skills |

---

## Project Memory Layout

Paddlr stores project memory under `docs/paddlr/` by default (customizable via `.paddlr.json` — see [Customization](docs/guide/06-customization.md)):

```text
docs/paddlr/
├── specs/          # Reviewable feature specifications
├── plans/          # Contract-first implementation plans (canonical Task State)
├── decisions/      # Granular, immutable Architecture Decision Records (ADRs)
├── DECISIONS.md    # Compact single-line-per-decision ADR index
└── PROJECT.md      # Living snapshot of architecture, stack, and conventions
```

---

## Verification

Run the same checks CI runs:

```bash
python scripts/validate_skills.py --verbose
python -m unittest discover -s tests -v
python scripts/check_markdown_links.py
```

---

## Acknowledgements

Paddlr is inspired by and builds upon the work of **[Lauren Tan](https://github.com/poteto)** ([@poteto](https://github.com/poteto)) and **pstack** ([cursor/plugins](https://github.com/cursor/plugins)). Several skills, workflows, and engineering principles in Paddlr adapt concepts originating from pstack.

## License

Apache 2.0. See [LICENSE](LICENSE).
