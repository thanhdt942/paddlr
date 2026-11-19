---
description: "Perform independent, read-only code review against specifications and quality standards"
argument-hint: "[commit range, task, or files to review]"
---

# /pdl:code-review — Code Review

**Task:** $ARGUMENTS

Apply the **Code Review** skill to evaluate changes against specs, plans, and code quality standards.

1. Read the skill entrypoint ([code-review/SKILL.md](../skills/code-review/SKILL.md)).
2. Gather minimal review context and dispatch a read-only reviewer subagent using `code-reviewer.md`.
3. Act on feedback before merging or completing the milestone.
