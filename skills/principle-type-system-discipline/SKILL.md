---
name: principle-type-system-discipline
description: "Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust variants, derive from authoritative schemas."
disable-model-invocation: true
---

# Type System Discipline

Make the compiler reject impossible states, mismatched primitives, and unhandled variants.

- **Brand semantic primitives.** If two values share a primitive representation (e.g. string or number) but carry distinct domain meanings (e.g. `UserId` vs `OrderId`), give each its own branded or newtype wrapper. Validate invariants once at creation.
- **External data is untyped until parsed.** JSON payloads, network responses, CLI flags, configuration files, environment variables, and database rows are untrusted until parsed at the system boundary into typed domain models. Parse, don't validate.
- **Derive types from authoritative schemas.** When a schema or specification owns a data shape, derive types from it rather than maintaining a parallel handwritten duplicate.
- **Exhaust all variants.** Use discriminated unions, algebraic data types, or enums with exhaustive pattern matching so the compiler flags any unhandled state when new variants are added.
