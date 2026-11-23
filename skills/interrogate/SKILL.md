---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Adversaries try to break a change or design, and only findings proven by a run survive."
disable-model-invocation: true
---

# Interrogate

Adversarial review to find blind spots and break a proposed design or change. A finding survives only when an empirical execution proves it.

## Frame

The scope is what the user names. Otherwise it is the branch diff from merge base through the working tree. Restate intent using the **in-your-own-words** skill.

## Fan Out or Adversarial Mode

1. **Multi-Agent Delegation (when supported):**
   - Allocate each adversary its own isolated working directory or worktree.
   - Dispatch adversaries across model profiles with the brief:
     > Break this change. Prove each finding with an empirical run against the real code: a failing test, a repro script, or command output demonstrating the failure. Keep repros isolated. Report each finding with a title, exact reproduction command, verbatim error output, and required behavior. Ignore non-functional preferences or hypothetical risks requiring unrelated changes. No findings is a valid result.
2. **Single-Agent Fallback:**
   - The Main Agent switches to an explicit red-teaming stance: actively write targeted boundary tests and fuzzing scripts to challenge the premises and edge cases of the implementation.

## Verify

Verify each candidate finding by running its reproduction command against the code. Retain a finding only when:
- The command executes and reproduces the failure.
- The failure breaks a genuine functional invariant or safety requirement.

Merge findings that share a root cause. Drop unproven or stylistic assertions.

## Output

- **Intent:** concise restatement of user and architectural intent.
- **Verified Findings:** for each proven finding: title, reproduction command, verbatim output, and impact.
- **Dropped Claims:** count of unverified assertions discarded.
