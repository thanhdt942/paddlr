# 2. Paddlr Mode and Playbooks

`paddlr-mode` ([skills/paddlr-mode/SKILL.md](../../skills/paddlr-mode/SKILL.md)) is the single orchestration entry point for disciplined engineering work. It stays lazy-loaded (`disable-model-invocation: true`) so it adds zero overhead until invoked.

## How a Session Flows

1. **Restate goal and smallest change:** On the first turn, the agent states your goal and the minimal change that meets it.
2. **Classify complexity:** Level 1 (small/localized), Level 2 (standard reversible feature), or Level 3 (architectural/breaking).
3. **Select a playbook:** Open `skills/paddlr-mode/playbooks/<name>.md` and mirror active steps into `ui.todo`.
4. **Execute in verifiable slices:** Use TDD (`test-driven-development`), verify against the real artifact (`principle-prove-it-works`), run `sync-docs` and `code-review`, and open a ready-for-review PR (`opening-a-pr.md`).

## Playbook vs. Standalone Skill Boundaries

Some capabilities exist as both a playbook and a focused skill. They compose rather than compete:

| Concern | Playbook | Standalone Skill | Relationship |
|---|---|---|---|
| Feature delivery | `playbooks/feature.md` | `feature-development` | The playbook owns throughput checkpoints, autonomy, and PR creation; it invokes `feature-development` for the 5-phase SDD lifecycle. |
| Bug fixing | `playbooks/bug-fix.md` | `sre-debugging` | The playbook owns reproduction, failing-test commits, and PR creation; it invokes `sre-debugging` for 4-phase root-cause analysis. |
| Review | — | `code-review` vs. `interrogate` | Run `code-review` on every PR for spec alignment and maintainability; run `interrogate` on high-risk or contested designs where only empirically reproduced findings survive. |

## Single-Agent Baseline and Optional Delegation

Paddlr Core requires only five primitives (`fs.read`, `fs.write`, `fs.patch`, `shell.exec`, `search.find`). Multi-agent delegation (`agent.delegate` using `paddlr-worker` and [worker.md](../../skills/paddlr-mode/worker.md)) is strictly optional and falls back to sequential in-thread execution when unsupported.

Next: [Specs, plans, and ADRs](03-specs-plans-adrs.md).
