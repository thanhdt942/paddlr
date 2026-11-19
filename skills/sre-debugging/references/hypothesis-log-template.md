# Hypothesis Log Template

Use this template during non-trivial investigations to keep observations, hypotheses, and experiment results explicit and verifiable.

## Template

```markdown
## Investigation Summary

- **Expected Behavior**: <What should happen>
- **Actual Behavior**: <What actually happens, with exact error or symptom>
- **Scope / Impact**: <Affected users, endpoints, tests, or environments>
- **Mitigation Status**: <Not needed | Applied: details | Pending>

## Confirmed Observations (Facts Only)

- [O1] <Exact log line, stack trace frame, metric value, or code reference>
- [O2] <Exact reproduction condition or recent diff>

## Hypotheses & Experiments

| ID | Hypothesis | Prediction (If True) | Experiment | Actual Result | Verdict |
|----|------------|----------------------|------------|---------------|---------|
| H1 | <Proposed cause> | <Observable outcome> | <Test or inspection> | <Observed output> | Confirmed / Refuted / Inconclusive |
| H2 | <Competing cause> | <Observable outcome> | <Test or inspection> | <Observed output> | Confirmed / Refuted / Inconclusive |

## Causal Chain

1. **Root Defect**: <Exact file, function, config, or interaction>
2. **State Infection**: <How internal state becomes invalid>
3. **Observed Failure**: <How infected state produces the reported symptom>

## Fix & Verification

- **Fix Applied**: <Concise description of change and why it removes the root defect>
- **Reproduction Re-check**: <Command run and confirmed passing result>
- **Regression Coverage**: <Test added or updated, plus test suite result>
```

## Worked Example (Abbreviated)

```markdown
## Investigation Summary

- **Expected Behavior**: `POST /orders` returns 201 and deducts inventory once.
- **Actual Behavior**: Concurrent requests for the last item both return 201, leaving `stock = -1`.
- **Scope / Impact**: High-demand SKU checkout under concurrent load.
- **Mitigation Status**: Not needed (reproduced in staging).

## Confirmed Observations (Facts Only)

- [O1] `inventory.py:42` reads `item.stock`, checks `if item.stock > 0`, then updates `item.stock -= 1` without a row lock.
- [O2] Reproducible 100% of the time when firing 2 parallel requests against a row with `stock = 1`.

## Hypotheses & Experiments

| ID | Hypothesis | Prediction (If True) | Experiment | Actual Result | Verdict |
|----|------------|----------------------|------------|---------------|---------|
| H1 | Retry middleware sends duplicate requests | Request logs show 2 calls with same idempotency key | Inspect access logs for test run | 2 distinct requests with different keys | Refuted |
| H2 | Read-modify-write race condition without row lock | Both transactions read `stock = 1` before either commits | Log transaction ID and read value before update | Tx A and Tx B both logged `stock = 1` | Confirmed |

## Causal Chain

1. **Root Defect**: Non-atomic read-check-update in `inventory.py:42` without `SELECT ... FOR UPDATE` or atomic SQL decrement.
2. **State Infection**: Two concurrent transactions both evaluate `stock > 0` as true using stale reads.
3. **Observed Failure**: Both transactions commit a decrement, resulting in `stock = -1`.

## Fix & Verification

- **Fix Applied**: Replaced read-modify-write with atomic `UPDATE items SET stock = stock - 1 WHERE id = :id AND stock > 0` and checked affected row count.
- **Reproduction Re-check**: Ran 10 parallel checkout requests for `stock = 1`; exactly 1 returned 201, 9 returned 409, final `stock = 0`.
- **Regression Coverage**: Added concurrency test `test_concurrent_checkout_prevents_negative_stock`; full suite passed.
```
