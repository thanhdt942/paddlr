### Visual parity

**You own pixel-exact equivalence. The baseline is the spec; you do not touch it.** Equivalence is verified by automated image diff, not by eye (**principle-prove-it-works**).

1. **Establish Baseline First:** Prior to making changes, establish a visual regression harness using standard headless browser tools (Playwright, Puppeteer, pixelmatch). Capture screenshots across all component states. No baseline means no parity claim; this is a blocking prerequisite.
2. **Anti-Shortcut Clauses:** Do not modify the harness, tamper with baselines, or distort component structure to make a diff artificially pass. If a baseline appears genuinely flawed, pause and clarify; never edit it silently.
3. **Migrate Incrementally:** Migrate one component or view at a time. Shared primitives migrate first as a blocking prerequisite.
4. **Automated Visual Verification:** Verify each component against its baseline via headless image diffing. A non-zero diff is an immediate failure. Investigate pixel deltas, adjust styles or layout, and re-run until diff is zero.
5. **Open PR:** Invoke **Opening a PR** (`playbooks/opening-a-pr.md`) per component or per verified batch.

**Reply:** components migrated, diff results for each, baseline harness location, and remaining components.
