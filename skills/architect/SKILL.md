---
name: architect
description: "Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape."
disable-model-invocation: true
---

# Architect

Before writing code, trace every system the change touches. Ground the design in `docs/paddlr/specs/` and `docs/paddlr/plans/`.

1. **Sketch Competing Shapes:** Sketch two different shapes for the architecture (types, discriminated unions, state machines, module boundaries).
2. **Evaluate Invariants:** Pick the shape where:
   - Each piece of state has exactly one authoritative owner (**principle-model-the-domain**).
   - Each task has one clear way to be performed.
   - Callers need to know the least internal detail (**principle-minimize-reader-load**).
   - Illegal states are unrepresentable (**principle-type-system-discipline**).
3. **Decisions & Specs:** For Level 2 features, persist the chosen design to `docs/paddlr/specs/YYYY-MM-DD-<slug>.md`. For Level 3 architectural decisions, author an ADR in `docs/paddlr/decisions/XXXX-<slug>.md` and index in `docs/paddlr/DECISIONS.md`. Redesign from first principles instead of patching if workarounds repeat (**principle-redesign-from-first-principles**).
