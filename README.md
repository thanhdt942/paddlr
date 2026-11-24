# Paddlr

<p align="center">
  <img src="assets/logo.svg" alt="Paddlr Logo" width="160" height="160" />
</p>

<p align="center">
  <strong>Simple on the Surface. Sophisticated Underneath.</strong><br>
  <em>An Agent-Agnostic Software Engineering Framework turning proven engineering practices into practical, reusable AI Agent Skills.</em>
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

## 1. Brand Story: The Duck Philosophy

**Paddlr** is inspired by the serene image of a duck gliding gracefully across the water.

From above the surface, the duck moves calmly, smoothly, and effortlessly. But beneath the surface, its legs paddle continuously and purposefully to maintain balance, navigate currents, and propel forward.

This is the foundational metaphor for how Paddlr approaches Software Engineering:

- **Above the Surface:** A clean, frictionless developer experience with intuitive workflows and clear guidance.
- **Below the Surface:** Disciplined engineering practices, structured specifications, contract-first implementation planning, rigorous Test-Driven Development (TDD), scientific debugging, and persistent project memory.

> **"Great engineering doesn't have to feel complicated."**  
> *Handle the complexity. Simplify the experience.*

Developers should not have to manually coordinate every quality gate or memorize sprawling procedural checklists. Paddlr orchestrates and standardizes professional software engineering through dedicated, reusable **AI Agent Skills**.

---

## 2. Core Principles

Paddlr is built upon four foundational pillars:

1. **Simplicity by Design:** Every skill has a single, unmistakable purpose, an intuitive interface, and an actionable workflow requiring zero memorization.
2. **Engineering Discipline:** Simplicity of experience never compromises engineering rigor. Paddlr embeds proven methodologies:
   - Specification-driven development (`docs/paddlr/specs/`)
   - Structured contract-first planning (`docs/paddlr/plans/`)
   - Test-Driven Development (TDD: RED → GREEN → REFACTOR)
   - Scientific SRE debugging and root cause analysis
   - Independent, read-only code review
   - Governed release management
3. **Practical over Theoretical:** Engineering principles are translated into deterministic, verifiable procedures that generate real, checkable artifacts.
4. **Agent-Agnostic by Design:** Zero proprietary vendor lock-in. Built natively for Google Antigravity, Claude Code, OpenCode, and OpenAI Codex.

---

## 3. Positioning: What Paddlr Is and Is Not

| What Paddlr Is | What Paddlr Is Not |
|---|---|
| A collection of reusable AI Agent Skills | Not an AI coding agent itself |
| A practical Software Engineering Framework | Not an IDE or closed development environment |
| A system for applying proven engineering practices | Not an arbitrary collection of ad-hoc prompts |
| An agent-agnostic approach to AI software engineering | Not tied to a single AI vendor or platform |

---

## 4. Quick Start & Installation

### Google Antigravity (`agy`)

Install directly via git in one command:

```bash
agy plugin install https://github.com/thanhdt942/paddlr
```

### Claude Code

Install inside your Claude Code session (one step):

```text
/plugin install paddlr --marketplace thanhdt942/paddlr
```

*Or in two steps (for versions without `--marketplace`):*

```text
/plugin marketplace add thanhdt942/paddlr
/plugin install paddlr@paddlr
```

### OpenCode

Install via the OpenCode CLI (adds Paddlr to `.opencode/opencode.json`; pass `-g` to install globally):

```bash
opencode plugin paddlr@git+https://github.com/thanhdt942/paddlr.git
```

Or configure inside your project's `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "paddlr@git+https://github.com/thanhdt942/paddlr.git"
  ]
}
```

See [.opencode/INSTALL.md](.opencode/INSTALL.md) for local linking and full documentation.

### OpenAI Codex (`codex`)

Add the Paddlr marketplace, then install the plugin from it:

```bash
codex plugin marketplace add thanhdt942/paddlr
codex plugin add paddlr@paddlr
```

---

## 5. Agent Skills & Slash Commands

Once installed, describe your task in natural language and your coding agent will load the matching skill. In Claude Code, skills are also exposed as slash commands under the plugin namespace (`/paddlr:<skill>`):

| Skill | Directory | Purpose |
|---|---|---|
| `feature-development` | `skills/feature-development` | Orchestrate end-to-end feature delivery across all phases |
| `writing-specs` | `skills/writing-specs` | Requirements discovery and specification authoring |
| `writing-plans` | `skills/writing-plans` | Bite-sized implementation plans in `docs/paddlr/plans/` |
| `test-driven-development` | `skills/test-driven-development` | Iron-law TDD (no code without a failing test first) |
| `sre-debugging` | `skills/sre-debugging` | Evidence-based root-cause investigation before fixing |
| `code-review` | `skills/code-review` | Read-only code review against specifications |
| `release-management` | `skills/release-management` | Semantic versioning and release lifecycle in `RELEASE.md` |
| `skill-creator` | `skills/skill-creator` | Design, test, and package reusable AI agent skills |
| `setup-paddlr` | `skills/setup-paddlr` | Initialize `docs/paddlr/` or `.paddlr.json` and optional model profiles |
| `paddlr-help` | `skills/paddlr-help` | Read-only advisor routing questions to skills, playbooks, principles, and prompts |

---

## 6. Project Architecture & Memory

Paddlr persists engineering memory canonically under `docs/paddlr/` (customizable via an optional `.paddlr.json` at your repository root — see the [User Guide](docs/guide/README.md)):

```text
docs/paddlr/
├── specs/                 # Reviewable feature specifications
├── plans/                 # Contract-first implementation plans
├── decisions/             # Granular Architecture Decision Records (ADRs)
├── DECISIONS.md           # Lightweight ADR master index
├── PROGRESS.md            # Current operational status and completed slices
└── PLAN.md                # Long-term engineering roadmap
```

---

## 7. Verification & Quality Gates

Run what CI runs:

```bash
# Validate all Agent Skills conform to the Agent Skills open standard
python scripts/validate_skills.py --verbose

# Run the complete automated test suite
python -m unittest discover -s tests -v
```

---

## 8. Acknowledgements

Paddlr is inspired by and builds upon the pioneering work of **[Lauren Tan](https://github.com/poteto)** ([@poteto](https://github.com/poteto)) and her project **pstack** (available in [cursor/plugins](https://github.com/cursor/plugins)). Several engineering skills, workflows, and core principles in Paddlr reference, adapt, and reuse concepts originating from pstack.

Special thanks and sincere gratitude to Lauren for her foundational contributions to rigorous, disciplined AI agent engineering practices.

---

## 9. License

Distributed under the Apache 2.0 License. See [LICENSE](LICENSE) for details.
