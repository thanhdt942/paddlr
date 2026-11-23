### Eval

**You own the experiment design. Plan, blind, run, synthesize.**

**Non-negotiables for blinding:**
- No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, or `arena` in any directory, file, or prompt the candidate sees.
- The candidate prompt looks like an organic user request. State the goal, not the meta.
- No chain-eliciting cues. Do not ask candidates to list which skills, principles, or files they applied; evaluate chain-following from code shape, not self-report.
- Sanitize directory and slug names; use project-shaped paths.
- Do not disclose to candidates that other candidates exist.
- The judge can know it is evaluating, but sees outputs by sanitized label only, never by author or model name.
- When comparing two variants: one judge scores both sets in a single pass on one scale, blind to which set each came from.

**Steps:**
1. **Frame:** State what variant is under test and what behavior counts as success. Write the rubric (3–6 concrete criteria) for the judge only.
2. **Set Up Sanitized Environments:** Establish per-candidate working directories with the variant in place. Include organic context (a project skeleton, relevant skills).
3. **Author Organic Prompt:** Craft a clean prompt representing an authentic developer request.
4. **Execute Candidates:** Run candidates across distinct models or prompt variants. Each executes in its own isolated directory (**principle-separate-before-serializing-shared-state**). Model profiles are steered via the Runtime Adapter Contract (`skills/paddlr-mode/references/runtime-adapters.md`).
5. **Blinded Evaluation:** Evaluate outputs using a blinded judge or independent reviewer against the rubric.
6. **Verify from Real Artifacts, Not Self-Reports:** Inspect candidate git diffs, executed commands, test logs, and touched files directly (**principle-prove-it-works**).
7. **Synthesize:** Read every candidate output end-to-end. Compare with the judge's scoring. Formulate a final recommendation.

**Reply:** variant under test, rubric, per-candidate notes, judge's verdict, synthesis, and recommendation on whether to promote the variant.
