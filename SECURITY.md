# Security Policy

## Supported Versions

Paddlr provides security updates and vulnerability patches for the following versions:

| Version | Supported | Status |
|---|---|---|
| `3.x` | Yes | Active (Current Release) |
| `2.x` | Yes | Maintenance |
| `< 2.0.0` | No | End of Life |

## Reporting a Vulnerability

We take the security and safety of software engineering automation seriously. If you discover a security vulnerability or safety risk in Paddlr (including skill instructions, template risks, script vulnerabilities, path traversal risks, or platform adapter behaviors):

1. **Do not disclose the issue publicly.** Do not create a public GitHub issue or discuss it in public chat rooms.
2. Submit a confidential report via GitHub Private Vulnerability Reporting on the repository page.
3. If private vulnerability reporting is unavailable, contact the repository maintainers privately.
4. Include detailed reproduction steps:
   - Affected skill, workflow, script, template, or adapter.
   - Operating system and agent runtime environment.
   - Exact steps or scenario required to reproduce the issue.
   - Potential impact and assessment of risk.

## Response Process

- **Acknowledgment:** Maintainers will acknowledge receipt of the report within 48 hours.
- **Assessment:** Maintainers will verify the vulnerability, evaluate its impact, and determine severity.
- **Remediation:** A fix will be developed, tested, and reviewed in private.
- **Disclosure:** Once a patch is available, a security advisory will be published detailing the vulnerability, remediation, and credits (unless anonymity is requested).

## Agent and Execution Safety Principles

Paddlr skills, scripts, and workflows operate within developer repositories and alongside AI coding agents. The following security principles are strictly enforced:

- **No Secret Leakage:** Framework components, templates, and logging conventions must never log, stage, commit, or serialize credentials, access tokens, API keys, or private environment variables.
- **Untrusted Input Handling:** Repository content, issues, external references, and third-party prompts must be treated as untrusted data.
- **Deterministic Script Safety:** Scripts distributed with the framework (such as `scan_repo.py`, `pdl`, or validators) must be read-only or strictly scoped, avoiding arbitrary command execution.
- **Non-Destructive Defaults:** Agent operations must never default to destructive actions (such as `git reset --hard`, deleting untracked files without confirmation, or rewriting history).
- **Destination Safety:** Installers must validate destination paths against system root traversal (`/`, `C:\`, dangling symlinks).
