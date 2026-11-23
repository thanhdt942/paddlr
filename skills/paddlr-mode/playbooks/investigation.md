### Investigation

**You own the answer. Plan, route, write.** Single-Agent execution baseline.

Investigation requests are read-only. They produce a cited explanation, architecture map, or recommendation, not a code change.

1. **Trace Code & Rationale:** Trace the code and subsystems the question touches. For historical motivation or regression origins, also route through the **why** skill to query Git history and `docs/paddlr/decisions/`.
2. **Throughput Checkpoint:** Checkpoint stays one line: `throughput checkpoint: n/a, read-only investigation`.
3. **Structured Findings:** Produce the output using clear structural sections:
   - Overview
   - Key Concepts & Types
   - How It Works (runtime execution flow)
   - Where Things Live (file paths and architectural ownership)
   - Gotchas & Operational Edge Cases
   - If the request is a decision between alternatives, include an explicit tradeoffs table.
4. **Declarative Prose Standards:** Format the response using concise, plain English following Paddlr style rules in [rules/AGENTS.md](../../../rules/AGENTS.md). Cut filler, avoid marketing jargon, and use short declarative sentences.

No PR, no babysit, no `architect` unless the investigation precedes a code change. If it does, record findings in `docs/paddlr/specs/` and route to Bug fix or Feature.

**Reply:** the investigation output. For "are we sure?" questions, provide candid engineering judgment backed by evidence. Push back if the premise is invalid (**principle-attack-the-premise**).
