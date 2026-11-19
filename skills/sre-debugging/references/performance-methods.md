# Performance Analysis Methodology (Brendan Gregg)

Use this reference **only** when the investigation involves latency, throughput, timeouts, high resource usage, memory leaks, or scalability bottlenecks. Do not use it as the default workflow for functional logic bugs.

## 1. Baseline First

Before changing any code or configuration:

- Measure the current performance metric quantitatively (for example: p50, p95, p99 latency, requests/sec, memory growth rate).
- Avoid relying on averages alone; tail latency (p95/p99) often hides the real bottleneck.
- Establish a repeatable benchmark or load profile so improvements can be verified objectively.

## 2. RED Method (Service and Request Level)

Start here for microservices, APIs, and request-driven workloads:

- **Rate**: Requests per second. Did traffic spike or change shape?
- **Errors**: Failed requests per second or error rate percentage. Are retries amplifying load?
- **Duration**: Distribution of request latency (p50, p95, p99). Where in the request lifecycle is time spent?

Use distributed traces or stage-level timers to break total duration into components (network, queue wait, application CPU, database queries, external API calls).

## 3. USE Method (Resource Level)

For every relevant hardware or software resource (CPU, memory, disk I/O, network interface, thread pool, DB connection pool, locks), check three metrics:

- **Utilization**: Percentage of time the resource is busy or percentage of capacity in use.
- **Saturation**: Degree to which extra work is queued and waiting for the resource.
- **Errors**: Count of resource-level errors (dropped packets, OOM kills, pool exhaustion timeouts, lock timeouts).

A resource with high saturation (growing queues) is often a stronger indicator of a bottleneck than moderate utilization alone.

## 4. Drill-Down Analysis

Narrow the bottleneck in three progressive layers instead of guessing at micro-optimizations:

1. **Monitoring**: Identify which service, endpoint, or host shows the anomaly (using RED/USE metrics).
2. **Identification**: Narrow down to the responsible subsystem (database query, GC pauses, lock contention, serialization, external call).
3. **Analysis**: Profile or trace only that subsystem (CPU flame graphs, query `EXPLAIN ANALYZE`, heap allocation profiles, lock wait traces) to pinpoint the exact hotspot.

## 5. Process of Elimination and Scientific Verification

- Rule out subsystems systematically using measurements rather than intuition.
- Apply **one optimization at a time** against the baseline.
- Re-measure after each change to confirm actual improvement and check whether the bottleneck simply shifted to a downstream resource.
- If a change does not measurably improve the target metric, revert it to avoid unnecessary complexity.
