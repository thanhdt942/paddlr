### Runtime forensics

**You own the diagnosis. Instrument the live process, don't theorize from source.** The deliverable is a cited diagnosis, not a speculative fix.

1. **Capture Live Signal:** Capture diagnostic signals on the live process using standard inspection tools: a CPU profile for a hot process (`node --cpu-prof`, `py-spy`), a heap snapshot for a memory leak, or CDP trace/logging for a visual or event loop glitch. Require a real artifact, not a guess (**principle-prove-it-works**).
2. **Reduce Artifact:** Narrow the capture to the root mechanism: the function on the hot path, the retainer chain from a leaked object to a GC root, or an event loop firing without backpressure. Keep findings distilled in the main thread (**principle-guard-the-context-window**).
3. **Prove Mechanism Empirically:** Confirm the mechanism before committing to a fix. Inject temporary runtime instrumentation or logging into the running process to confirm the hypothesis cheaply (**principle-fix-root-causes**).
4. **Map to Source:** Map the finding back to repository source: file path, symbol, and the line that allocates or loops.
5. **Checkpoint:** Throughput checkpoint stays one line: `throughput checkpoint: n/a, read-only forensics`.

**Reply:** the signal captured, the reduced finding, how you proved the mechanism, the exact source location, and artifact paths. No code fix unless requested; hand findings back to Bug fix or Perf issue once the cause is proven.
