# 3. Specs, Plans, and ADRs

Chat transcripts disappear across sessions. Paddlr keeps engineering decisions durable and git-tracked under `docs/paddlr/` by default (customizable via `.paddlr.json`):

```text
docs/paddlr/
├── specs/          # Reviewable feature specifications (YYYY-MM-DD-<slug>.md)
├── plans/          # Contract-first implementation plans (canonical Task State)
├── decisions/      # Granular, immutable ADRs (XXXX-<slug>.md)
├── DECISIONS.md    # Compact single-line-per-decision ADR index
└── PROJECT.md      # Living snapshot of architecture, stack, and conventions
```

## The SDD Lifecycle

1. **Specifications (`writing-specs`):** Capture problem, scope, requirements (`FR`/`BR`/`NFR`), acceptance criteria, and confirmed technical choices before writing code on Level 2+ tasks (`principle-spec-before-code`).
2. **Implementation Plans (`writing-plans`):** Decompose the spec into bite-sized, contract-first tasks (`Consumes` / `Produces`) with checkbox steps (`- [ ]`). Always create a fresh plan file per request; terminal plans (`completed`, `failed`, `cancelled`) are never reopened.
3. **Architectural Decisions (`writing-decisions` / `/adr`):** Record Level 3 decisions in `decisions/XXXX-<slug>.md` and index them in `DECISIONS.md`. Accepted ADRs are immutable (`principle-record-decisions-immutably`): when a direction changes, author a new ADR and mark the prior record `Superseded by ADR-YYYY`.
4. **Preventing Drift (`sync-docs`):** `playbooks/opening-a-pr.md` runs `sync-docs` as a mandatory pre-PR gate. It compares the branch diff against active specs, ADRs, and `PROJECT.md` so documentation stays aligned with shipped code.
5. **Historical Context (`why`):** When asking why a design or threshold exists, `why` inspects `decisions/`, `DECISIONS.md`, and `specs/` before searching git history (`git log`, `git blame`).

Next: [Autonomy and verification](04-autonomy-and-verification.md).
