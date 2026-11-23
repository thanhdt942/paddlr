### Trace forensics

**You own the diagnosis from the artifact.**

Distinct from **Runtime forensics**, which instruments a live process. In trace forensics, the capture already exists. The artifact is a fixed dataset; query it, do not re-run it. Use generic offline analysis tooling: DevTools or trace parsers for cpuprofiles, SQLite for structured event traces, and text/heap dump tools for heap snapshots.

1. **Load Artifact:** Identify the format and parse it. Distill large artifacts into actionable summaries (**principle-guard-the-context-window**).
2. **Transform to Queryable Shape:** Dump raw traces or heap snapshots into SQLite or relational formats where helpful (one row per sample, call frame, or node). Reach a queryable shape before analyzing.
3. **Isolate Root Cause:** Query for frames holding the most execution time, or follow the retainer chain from a leaked object to a GC root. For stuck threads, locate the frame blocked on I/O or lock contention.
4. **Attribute to Source:** Map the critical frame to file path, symbol, and line number via debug symbols. A frame with no source mapping is not yet a completed diagnosis. Resolve the symbols or explicitly state that the artifact lacks them.
5. **Differential Comparison:** If paired before-and-after captures exist, diff the metrics to confirm the diagnosis. Otherwise, mark the finding as the strongest hypothesis supported by the artifact.
6. **Checkpoint & Route:** Hand back a cited diagnosis (no code fix unless requested). Route to Bug fix or Perf issue once the cause is confirmed. Throughput checkpoint stays: `throughput checkpoint: n/a, read-only forensics`.

**Reply:** the artifact and format, the reduced finding, the source location, artifact paths, and whether a paired capture confirmed it.
