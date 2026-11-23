---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads."
disable-model-invocation: true
---

# Guard the Context Window

Context window saturation degrades reasoning quality, introduces hallucination and compression artifacts, and prematurely halts progress. Protect the main reasoning thread from raw payload bloat.

- **Delegate bulk processing to workers.** Route large file scans, raw test log dumps, compiler telemetry, and wide codebase surveys to bounded subagents or temporary scripts. Subagents extract the essential facts and return distilled summaries to the main conversation thread.
- **Use targeted queries.** Avoid reading entire multi-thousand-line files when an AST lookup, exact regex grep, or line-bounded read suffices. Never ingest bulk raw data just to check a single field.
- **Cap scope per turn.** Size development phases into small, verifiable slices. Bound the number of files inspected or modified in a single turn.
- **Account for mechanism costs.** Context spent on raw dumps is permanently lost for downstream architectural reasoning, planning, and verification.
