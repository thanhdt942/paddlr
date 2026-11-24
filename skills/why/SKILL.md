---
name: why
description: "Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Returns a cited read on decisions and tradeoffs. Use how for runtime behavior."
disable-model-invocation: true
---

# Why

Answer from the historical record, not just the code (respecting any custom paths in `.paddlr.json` at the repo root):
1. **Architectural Decisions:** Inspect `docs/paddlr/decisions/` and `docs/paddlr/DECISIONS.md` (or `.paddlr.json` overrides) for recorded ADRs, trade-offs, and superseded decisions.
2. **Feature Specifications:** Inspect `docs/paddlr/specs/` (or `.paddlr.json` override) for requirements, non-goals, and confirmed technical decisions explaining why a behavior exists.
3. **Git & PR Trail:** Read the commits (`git log -S`, `git log -L`, `git blame`) and PR discussions that introduced the target and subsequent modifications.
4. **Cited Findings:** Cite what authors and engineers explicitly recorded. Mark your own inferences clearly as inferences, and declare what the record does not answer.
