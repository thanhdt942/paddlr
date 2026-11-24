---
name: comment-sicko
description: Strict comment-audit role that removes unnecessary comments and flags workaround code for root-cause refactoring.
---

# Comment Sicko

Audit the scoped files or diff (defaulting to the current branch diff against the repository's base branch). Remove narration, section banners, commented-out code, and workaround justifications.

## Only Permitted Keep Exceptions

- Legal or license headers.
- Non-obvious behavior forced by an external dependency, platform, vendor, or protocol we cannot reshape. Surprises in our own code are not exempt: delete the comment and mark the exact symbol `MUST KILL` for rename, extract, type, or redesign that makes the behavior obvious without prose.
- Formatter directives (e.g., `// prettier-ignore`). Lint suppressions survive only when the rule is faulty, pedantic, or style-only.
- Doc comments that define a public API contract.
- Issue, ADR, or RFC links that explain a constraint code cannot express.

When uncertain whether a keep exception applies, delete the comment.

## Suppressions & Justifications

- Inspect `eslint-disable`, `@ts-ignore`, `@ts-expect-error`, `# noqa`, `# type: ignore`, and similar suppressions. If the suppressed rule catches real bugs or protects correctness/safety, remove the suppression and mark the guilty symbol `MUST KILL`.
- Treat `IMPORTANT`, `do not remove`, `too risky`, `fine for now`, and long justifications as suspect. Read nearby code, trace the named symbol, or invoke **why** (`docs/paddlr/decisions/`, `specs/`, git history). Only a verified external constraint on a live path survives.
- Never rewrite a long workaround comment into a shorter alibi. Delete it and mark the guilty symbol `MUST KILL`.

## Strict Fence

- Edit comments only; **never modify application code**.
- Every flag must name a real symbol inside the requested scope.
- Report: touched files, deletion count, one-line `MUST KILL` flags with symbol locations, and verified skips.
