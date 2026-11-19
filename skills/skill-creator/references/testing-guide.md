# Skill Verification & Testing Guide

Test skills in a **fresh context** so prior conversation history does not mask ambiguous instructions.

## 1. No-Guidance Control (Baseline)

Before adding a rule, check whether the agent already handles the scenario correctly *without* the skill:
- If the baseline run succeeds consistently → **do not add the rule**.
- If the baseline run skips steps, guesses policy, or formats inconsistently → **add a targeted rule** addressing that exact failure.

## 2. Trigger Testing

Verify that the frontmatter `description` routes accurately:
1. **Positive prompts (3–5):** Direct and paraphrased requests that *must* trigger the skill.
2. **Negative / Near-miss prompts (2–3):** Related topics that *must not* trigger the skill.
3. Refine trigger keywords and exclusions in `description` until routing is unambiguous.

## 3. Execution Testing by Risk Tier

### Standard Skills (Workflows, Formatting, Analysis)
1. Run 1–2 realistic tasks in a clean session with the skill loaded.
2. Inspect the raw output manually (do not rely solely on self-reported checklists).
3. Check for: skipped steps, invented assumptions, broken references, or bloated output.
4. Tighten wording where the agent interpreted instructions inconsistently.

### High-Risk / Discipline Skills (Releases, Security, Migrations, Compliance)
Apply lightweight pressure testing:
1. **Design a pressure scenario** combining 2–3 realistic stressors (e.g., urgent deadline, incomplete config, user asking to "just ship it quickly").
2. **Run with the skill** and observe whether the agent cuts corners or skips authorization/validation gates.
3. **Log rationalizations:** Record exact excuses the agent uses to bypass a rule (e.g., *"Tests probably pass since the change is small"*).
4. **Close loopholes:** Add concise counter-rules or a **Red Flags** list directly addressing the observed failure modes.
5. **Re-verify** in a fresh context until the agent holds the boundary reliably.

## 4. Packaging & Portability Audit

- [ ] No hardcoded OS paths, usernames, or private URLs.
- [ ] No links escaping the skill directory (`../`).
- [ ] All files in `references/`, `scripts/`, and `assets/` are referenced from `SKILL.md`.
- [ ] Instructions work without requiring a specific agent vendor or subagent framework.
