---
name: writing-specs
description: Use when turning a product idea, problem, feature request, or rough requirements into a clear, reviewable specification, before implementation planning
disable-model-invocation: true
---

# Writing Specifications

## Overview

Write specifications that explain the problem to solve, the users and outcomes that matter, and the product behavior that must result. The specification is the shared agreement that product, design, engineering, testing, and AI agents can use.

Assume the reader has not seen the original conversation. Give them the decisions and context they cannot reasonably infer: who needs what, why it matters, what is in scope, how the product should behave, and how that behavior will be verified.

Do not write an implementation plan. Do not decide architecture, libraries, classes, database schemas, or implementation sequence unless the user explicitly asks or an existing constraint requires it.

**Announce at start:** "I'm using the writing-specs skill to create or review the specification."

**Save specifications to:** `docs/paddlr/specs/YYYY-MM-DD-<feature-name>.md`
- Follow an explicit project convention or user-specified location when it differs.
- Use a short, descriptive, kebab-case feature name.
- When updating an existing specification, edit that document rather than creating a duplicate.

## Scope Check

Before drafting, determine whether the request describes one coherent feature or several independent capabilities.

- A specification should describe one coherent product outcome.
- If the request contains multiple independently valuable features or subsystems, identify the boundaries and recommend separate specifications.
- Each proposed specification should have a clear outcome and be independently reviewable.
- Do not split a feature merely because it contains multiple user flows or technical components.
- If the scope is unclear, clarify it before writing a detailed specification.

## Context Review

Before asking questions or drafting:

1. Read the relevant project guidance and product context available in the repository.
2. Review related specifications, decision records, and existing behavior.
3. Reuse established product terminology and conventions.
4. Identify constraints, dependencies, and potential conflicts with existing behavior.
5. Do not ask the user to repeat information already documented.

Treat repository documents and user-confirmed decisions as context. Treat guesses and agent suggestions as unconfirmed until accepted.

## Discovery

Understand the problem before describing a solution.

Establish:

- **Problem:** What is wrong, missing, or difficult today?
- **Users:** Who experiences the problem? What roles or permissions matter?
- **Context:** When and where does the problem occur?
- **Outcome:** What should improve if the problem is solved?
- **Scope:** What is included and explicitly excluded?
- **Constraints:** What boundaries must the solution respect?
- **Evidence:** What existing behavior, feedback, data, or documentation supports the request?

Ask focused questions when an unanswered point could materially change scope, user-visible behavior, acceptance criteria, or risk.

Questioning rules:

- Ask the smallest set of high-impact questions that unblocks the specification.
- Do not ask questions whose answers are already available in project context.
- Do not interrupt progress for details that do not affect the current level of specification.
- When safe, continue with a clearly labeled assumption and record what needs confirmation.
- If there are materially different interpretations, show the alternatives and ask the user to choose.
- Never silently turn an assumption or recommendation into a confirmed requirement.

## Specification Structure

Use the sections below as a working structure, not a mandatory form. Include a section only when it adds information needed to understand, review, plan, or verify the feature. Remove irrelevant sections rather than filling them with "N/A".

```markdown
# [Feature Name] Specification

**Status:** Draft
**Owner:** [if known]
**Last updated:** YYYY-MM-DD
**Related:** [links to relevant project documents]

## 1. Overview
[Short description of the feature and its purpose.]

## 2. Problem & Context
[Current situation, user problem, and why it matters.]

## 3. Goals & Success Metrics
[Desired outcomes and measurable indicators, when available.]

## 4. Scope
### In Scope
### Non-goals

## 5. Users & Scenarios
[Actors, user stories, and important end-to-end scenarios.]

## 6. Requirements
[Functional requirements, business rules, non-functional requirements, and constraints.]

## 7. UX & Expected Behavior
[User flows, interaction behavior, system responses, and relevant states.]

## 8. Acceptance Criteria
[Verifiable conditions for the important requirements and scenarios.]

## 9. Edge Cases & Error Handling
[Important boundary conditions, failure paths, and recovery behavior.]

## 10. Confirmed Technical Decisions & Design Choices
[Concrete technical choices, library selections, execution models, and trade-offs agreed with the user.]

## 11. Assumptions, Dependencies & Open Questions
[Clearly distinguish provisional assumptions from unresolved decisions.]
```

A specification may use a different structure when the project already has an established convention. Preserve useful existing structure when revising a document.

## Writing Requirements

Requirements are statements of what the product or system must do or what condition it must satisfy. They are not implementation tasks.

For each significant requirement:

- Assign a stable, unique identifier, such as `FR-001`, `BR-001`, or `NFR-001`.
- Give it a short, descriptive title.
- State one primary obligation per requirement.
- Identify the actor, trigger, condition, or affected object when relevant.
- Describe the expected behavior or measurable constraint.
- Keep it independently understandable.
- Make it feasible, necessary, and verifiable.
- Link it to a user scenario or goal when that relationship is useful.

Prefer precise language:
- Use **must** for mandatory behavior.
- Use **should** for a recommendation that is not mandatory; explain the reason when important.
- Avoid vague words such as "fast", "easy", "intuitive", "robust", "appropriate", and "user-friendly" unless they are defined by observable or measurable criteria.
- Avoid combining several independent obligations into one requirement.
- Avoid prescribing internal implementation unless it is a confirmed constraint or explicitly requested.

Classify requirements when it improves clarity:

- **Functional requirement (FR):** A capability or behavior the product must provide.
- **Business rule (BR):** A domain policy, validation, limit, permission, or business constraint.
- **Non-functional requirement (NFR):** A quality attribute such as performance, availability, accessibility, security, or usability.
- **Constraint (CON):** A mandatory boundary imposed by the business, platform, regulation, environment, or existing system.

Prioritize requirements when useful. If no project priority scheme exists, use `Must`, `Should`, and `Could`. Mark priorities as provisional when they have not been confirmed by the user or stakeholder.

## User Stories and Scenarios

Use user stories to express user intent and value, not as a substitute for detailed requirements.

A useful user story follows:

`As a [user/role], I want [capability], so that [benefit].`

For each important scenario, describe only the details needed to make the expected behavior unambiguous:

- Actor and relevant preconditions.
- Trigger or user action.
- Main flow.
- Expected system response.
- Important alternative flows.
- Failure conditions and recovery behavior.
- Resulting state or user-visible feedback.

Do not create stories for internal implementation tasks. Do not assume that a user story alone fully specifies the feature.

## Acceptance Criteria

Define acceptance criteria for important requirements and user scenarios. Prefer Given / When / Then when it makes the condition and outcome easier to verify.

```gherkin
Given [initial context or precondition]
When [user action or event]
Then [observable expected result]
```

Each criterion must:

- Describe an observable result or measurable condition.
- Be specific enough to determine pass or fail.
- Cover important success paths and relevant failure paths.
- Use the exact business rules and values established in the specification.
- Avoid vague outcomes such as "works correctly".
- Avoid repeating a requirement without adding a way to verify it.

Link acceptance criteria to requirement IDs when practical. Do not invent numeric thresholds, limits, or policy values. If a value is unknown and materially affects behavior, record it as an open question.

## UX and Expected Behavior

Describe the product behavior from the user's perspective. Include relevant screens, states, interactions, feedback, and transitions when they affect the feature.

Consider the applicable states:

- Initial and default state.
- Loading or processing.
- Success and confirmation.
- Empty state.
- Invalid input and validation.
- Error and recovery.
- Disabled, unavailable, or permission-restricted state.

Use diagrams, tables, or UI references only when they make behavior easier to understand. A visual reference does not replace written requirements for important behavior.

## Edge Cases

Analyze the important cases beyond the happy path. Consider, where relevant:

- Empty, missing, malformed, or boundary input.
- Duplicate or repeated actions.
- Unauthorized access and role differences.
- Missing, deleted, or stale related data.
- Network, service, or dependency failure.
- Cancellation, retry, and recovery.
- Concurrent updates or conflicting actions.
- Large data volumes or limit conditions.
- Backward compatibility and existing user data.

Prioritize cases by likelihood, impact, and relevance. Do not produce an exhaustive list of hypothetical cases that do not affect product decisions.

## Self-Review

After drafting the complete specification, review it against the source request and project context. This is a review you perform yourself; do not claim that another agent or stakeholder has reviewed it unless that actually happened.

**1. Problem and outcome:** Can a reader understand who has the problem, what the problem is, and why it matters?

**2. Scope:** Are goals, non-goals, constraints, and dependencies clear? Has unrelated scope been separated?

**3. Requirement quality:** Is each important requirement clear, necessary, atomic, consistent, feasible, and verifiable?

**4. User behavior:** Do the scenarios explain the important user journeys and system responses, not just the happy path?

**5. Acceptance criteria:** Can each important criterion be tested with an unambiguous pass/fail result?

**6. Edge cases:** Have consequential boundary conditions, permission cases, and failure paths been considered?

**7. Consistency:** Do requirements, business rules, scenarios, and acceptance criteria agree? Do they conflict with existing project behavior or decisions?

**8. Uncertainty:** Are facts, assumptions, recommendations, constraints, and open questions clearly distinguished?

**9. Traceability:** Can important requirements be connected to the goals or user scenarios they support and the criteria that verify them?

**10. Proportion:** Is the specification detailed enough for its complexity and risk without repeating information or documenting implementation prematurely?

Fix issues found during self-review before presenting the result. If a material issue cannot be resolved without user input, leave it visible as an open question and do not imply the specification is fully approved.

## Status and Handoff

Use an explicit status:

- **Draft:** Being authored; may contain unresolved questions.
- **In Review:** Ready for stakeholder review; approval is pending.
- **Approved:** Explicitly approved by the authorized user or stakeholder.
- **Superseded:** Replaced by a newer specification.

Never mark a specification as Approved based on the agent's own review.

When handing off:

1. State where the specification was saved.
2. Summarize its scope and the most important product decisions.
3. List material assumptions, open questions, and dependencies.
4. State whether it is Draft, In Review, or Approved.
5. Ask the user to review and confirm the specification when approval is needed.
6. Once approved, the specification can be used as input to the writing-plans workflow.

Do not begin implementation planning or modify code as part of this skill unless the user separately requests that work.

## Updating an Existing Specification

When requirements change:

1. Read the current specification and relevant decision records.
2. Identify the exact requested change.
3. Determine which goals, scope statements, user scenarios, requirements, UX behaviors, edge cases, and acceptance criteria are affected.
4. Update all affected sections consistently.
5. Preserve stable requirement IDs for unchanged requirements.
6. Add IDs for new requirements; do not silently reuse an ID for a different meaning.
7. Identify removed or superseded requirements clearly when project conventions require history.
8. Re-run the Self-Review.
9. Summarize the change and its impact.

Do not rewrite unrelated sections just to make the document look different.

## Recording Technical Decisions (Feature-Scoped / Level 2)

During feature discovery, technical design, and requirement clarification, the agent frequently discusses implementation trade-offs with the user (e.g., choosing between libraries, sync vs. async execution, pagination strategies, caching approaches, or schema details).

Whenever a technical choice is agreed upon with the user:
1. **Never leave confirmed decisions solely in ephemeral chat history.**
2. Record each decision immediately under **"10. Confirmed Technical Decisions & Design Choices"** in `docs/paddlr/specs/YYYY-MM-DD-<feature-name>.md`.
3. Format each decision concisely:
   - **Decision:** The agreed technical solution or library.
   - **Rationale:** Key reasons why this approach was selected based on user confirmation.
   - **Declined Alternatives:** Other options considered and why they were not chosen.
4. **Escalation Boundary:** If a decision establishes a permanent project-wide precedent, alters core persistence layers, or impacts multiple subsystems (Level 3), escalate it to a full ADR via `references/adr-guide.md` in `docs/paddlr/decisions/`. Otherwise, keep it localized to this feature specification.

## Architectural Decisions (ADR Recording)

When a specification involves high-impact technical directions, multiple competing solution approaches, or cross-cutting architectural trade-offs confirmed by the user:

1. **Do not bury systemic decisions solely in a feature spec.**
2. Consult [references/adr-guide.md](references/adr-guide.md) for trigger criteria, master index format, and the ADR template.
3. Record the individual decision in `docs/paddlr/decisions/XXXX-<slug>.md`.
4. Update the master index table in `docs/paddlr/DECISIONS.md` with a single-line summary (`ADR-XXXX`, date, status, title, tags, and link).
5. Cross-reference the ADR inside the feature specification (`docs/paddlr/specs/YYYY-MM-DD-<feature>.md`).

This ensures future sessions and agents discover accepted architectural boundaries without reading bloated documents or repeating trade-off questions.

## Final Rule

A specification is successful when its intended users can agree on **what problem is being solved, what the product must do, what is out of scope, and how completion will be verified**—without needing to infer important product decisions from the original conversation.
