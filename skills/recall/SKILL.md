---
name: recall
description: "Reconstruct your recent working context from Git history, canonical Task State plans, and repository records, then hand back a tight current-state brief. Use for 'recall my work on X', 'catch me up', 'what have I been working on', 'where did I leave off', before starting or resuming work."
disable-model-invocation: true
---

# Recall

**Before you start or resume work, you rebuild the user's recent working context and hand back a tight capsule of where things stand now and what to do next.**

Single-Agent execution baseline. Keep it tight and on-topic. Read only what the in-scope threads need, then stop.

Your context lives in two authoritative records:
1. **Repository & Task Record:** Git commit logs (`git log -n 20 --oneline`), active diffs (`git status`, `git diff`), and canonical task plans in `docs/paddlr/plans/`.
2. **Project Memory:** Architectural decisions in `docs/paddlr/decisions/`, living architecture in `docs/paddlr/PROJECT.md`, and issue/PR discussions.

1. **Classify, then Route:** Resuming one specific prior task plan is the **session-pickup** playbook (`playbooks/session-pickup.md`), not this. Recall synthesizes broad working context across recent initiatives before you act. If the user already provided a full state capsule, use it directly.
2. **Lock Scope:** Pin the search window (default the last 7 days), the topic or subsystem named, and the workspace. State the scope back cleanly.
3. **Inspect Repository History:** Query `git log --grep="<topic>"`, `git log --author`, and recently modified files in `docs/paddlr/plans/` and `docs/paddlr/specs/`. Extract the user's goals, decisions, completed slices, and open threads directly in the main agent thread.
4. **Inspect Project Memory & Live State:** Check `docs/paddlr/DECISIONS.md` for relevant architectural choices. Verify against live branches and PRs using `git` and `gh`.
5. **Write the Brief:** Group findings by thread following the output contract below.

## Output contract

Lead with the capsule, then thread status, problems, and the next move.

- **Capsule:** At most 5 bullets summarizing what this work is and where it stands overall.
- **Threads:** One line each, prefixed with exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`.
- **Problems:** At most 5 recurring issues, symptoms, or reverted fixes.
- **Next move:** The single most useful next concrete action.

Write the brief in concise, plain English following Paddlr style rules in [rules/AGENTS.md](../../rules/AGENTS.md). Cite findings by commit SHA, PR number, or plan path.

**Reply:** the brief, to the contract above.
