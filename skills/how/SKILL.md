---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions. Single-Agent execution baseline.

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

## 1. Explore & Analyze

In the main agent context, use read-only search and file tools (`search.find`, `fs.read`) to trace:
- **Entry Points & Interfaces:** Public functions, API endpoints, or CLI commands.
- **Runtime Flow:** Execution path from intake to persistence or output.
- **Ownership & Layering:** Which packages, modules, or services own each piece of state.

## 2. Present

Deliver an architectural explanation structured for an engineer to start working confidently:
- Plain definition of the subsystem.
- High-level architecture and mental model.
- Step-by-step runtime flow.
- Key invariants and edge cases.
- Where things live (exact paths and symbols).
