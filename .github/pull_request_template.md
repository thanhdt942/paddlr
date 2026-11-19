## Description

<!-- Brief summary of what this PR introduces, modifies, or fixes. -->

## Category
- [ ] New / Modified Agent Skill (`skills/`)
- [ ] Workflow Enhancement (`workflows/`)
- [ ] Platform Integration / Native Manifest
- [ ] Documentation / Guide (`docs/`)
- [ ] Validator / Tooling (`scripts/`)
- [ ] Test Suite / Fixture (`tests/`)

## Verification Checklist
Please verify the following before requesting review:
- [ ] `python scripts/validate_skills.py` passes with zero errors.
- [ ] `python scripts/validate_context.py` passes with zero errors.
- [ ] `python -m unittest discover -s tests -v` passes completely.
- [ ] No broken Markdown links exist (`file:///` or relative).
- [ ] No unapproved commits or destructive Git commands were run.
- [ ] Portable core (`skills/`, `workflows/`, `templates/`) contains zero platform-specific dependencies.
- [ ] Relevant documentation updated (`README.md`, `CHANGELOG.md`, `PROGRESS.md`).

## Verification Output
<!-- Paste captured test execution or validator command output here. -->
```shell

```
