# Security Policy

## Supported Versions

| Version | Supported | Status |
|---|---|---|
| `1.2.x` | Yes | Active (Current Release) |
| `< 1.2.0` | No | Upgrade to `1.2.x` |

## Reporting a Vulnerability

If you discover a security or safety issue in Paddlr (skill instructions, script vulnerabilities, path traversal in `.paddlr.json` handling, or platform adapters):

1. **Do not disclose publicly.** Do not file a public GitHub issue.
2. Submit a confidential report via **GitHub Private Vulnerability Reporting** on the repository page (or contact the maintainer privately if unavailable).
3. Include affected files/skills, runtime environment, reproduction steps, and potential impact.

Maintainers aim to acknowledge reports within 48 hours, verify impact, prepare a fix privately, and publish an advisory once patched.

## Execution Safety Principles

- **No Secret Leakage:** Never log, stage, commit, or serialize credentials, tokens, or private environment variables.
- **Untrusted Input Handling:** Treat repository contents, issues, and external references as untrusted data.
- **Scoped Scripts:** Standard-library helpers (`scripts/paddlr_config.py`, `scripts/validate_skills.py`, `scripts/scan_repo.py`) enforce strict path containment and avoid arbitrary command execution.
- **Non-Destructive Defaults:** Hard stops block `git reset --hard`, `git clean -fd`, force-pushing shared branches, production deploys, and deleting persistent data without explicit user authorization.
