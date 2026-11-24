---
name: correct
description: "Find mistakes agents keep repeating in a repository and make each class structurally impossible. Try architecture first, then types, then a lint whose error names the fix, then a test, and write docs last. Prove each check fails on a real past mistake."
disable-model-invocation: true
---

# Correct

When the operator keeps correcting agents in a repository for the same mistake, change the repository so the next agent cannot repeat it (**principle-encode-lessons-in-structure**).

Assume every future contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Shape the repository so a change that looks right locally is right for the whole repo.

## 1. Find the Mistake Classes

Read recent commits, reverts, review comments, agent instruction files (`AGENTS.md`, `CLAUDE.md`), and workaround comments. Group recurring issues into mistake classes. A class qualifies once it has happened at least twice.

## 2. Fix Each Class at the Highest Level That Works

1. **Eliminate it with architecture.** Give each piece of state one owner and each task one supported way. Hide internals so the wrong import fails. Replace hand-synced lists with one source of truth. Delete old patterns and dead code an agent would copy.
2. **Enforce it with types or CI lints.** Make the bad state unrepresentable in types. If bad code still compiles, add a lint or CI check whose error message names the exact file, type, or function to use instead. If the pattern is already widespread, fail only when a diff adds new instances.
3. **Test the behavior.** Fix or delete any test that still passes when the behavior breaks, or that fails when only internals change (**principle-test-behavior-not-implementation**).
4. **Write docs or agent rules last, only for judgment calls.** Nothing fails automatically when an agent skips prose.

## 3. Fix and Prove

Fix the highest-frequency classes first, one verifiable slice each. Prove every new check fails on a real past mistake before turning it green. Run the exact same command locally and in CI. Any exception goes on the offending line with a reason, an expiry date, and human approval.

## 4. Keep the Rule Table Honest

Maintain a concise table in the repository's agent instruction file pairing each rule with what enforces it. When corrected by the operator, fix the mistake and add the rule. If the rule already existed without enforcement, treat it as a repeat and upgrade it to a higher structural level in the same change. Delete a rule once its mistake can no longer happen.

**Reply:** Each mistake class with its evidence, the enforcement level chosen, and why a higher level could not apply.
