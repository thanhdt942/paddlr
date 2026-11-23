### Opening a PR

Invoked at the conclusion of every code-modifying playbook.

1. **Clean Worktree & Rebase:** Work from a clean branch based on current `origin/dev`. Rebase into small, landable commits using Conventional Commits (`type(scope): subject`).
2. **Quality Pass:** Run standard project linters, formatters, and the **code-review** skill over the diff before opening the PR.
3. **PR Format:**
   - **Title:** `type(scope): subject`, naming a real symbol or module that carries the change.
   - **Body:** Under 40 lines with these `##` headings in order, dropping empty ones:
     - `## Why`: Underlying problem and business/technical motivation.
     - `## What changed`: Concise bulleted summary of structural and functional modifications.
     - `## Scope`: Explicit boundaries of what was touched versus what was left out.
     - `## Tradeoffs`: Key alternatives evaluated and rejected.
     - `## Blast Radius`: Runtime risks, dependency impact, and failure modes.
     - `## Verification`: Verbatim command outputs, test results, and passing metrics.
4. **Open Ready for Review:** Open PRs ready for review (never draft) via GitHub CLI (`gh pr create`), git push, or the repository host forge. Opening a PR does not conclude the task until verified by CI.
