---
name: principle-exhaust-the-design-space
description: "Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing prototypes and compare side by side before committing."
disable-model-invocation: true
---

# Exhaust the Design Space

When facing a novel interaction, unproven data flow, or unprecedented architectural fork, do not pick a direction by theoretical debate or speculative analysis alone. Build 2-3 minimal competing prototypes side by side and compare them empirically before committing to an approach.

- **Construct minimal variants.** Build each prototype in an isolated scratch workspace or branch with the smallest surface that answers the question. Do not write full production tests or polish edge cases for candidates that may be discarded.
- **Compare along explicit dimensions.** Evaluate prototypes on observable criteria: developer ergonomics, caller cognitive load, runtime performance, maintainability, and boundary cleanliness.
- **Clean teardown.** Once a winning candidate is selected, completely remove or discard the rejected prototype artifacts. Never allow throwaway exploratory code to accidentally slip into production baselines.
- **Product experience.** This applies equally to UX/UI decisions where user experience depends on feel, responsiveness, and direct manipulation rather than abstract logic.
