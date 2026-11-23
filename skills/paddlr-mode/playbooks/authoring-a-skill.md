### Authoring or modifying a skill

**You own the skill's voice and structure.**

1. **Invoke Skill Creator:** Invoke the **skill-creator** skill (`skills/skill-creator/SKILL.md`) to design, draft, and package the skill according to the open Agent Skills specification.
2. **Metadata & Standard Validation:** Validate that frontmatter contains required fields (`name`, `description`), `name` matches the directory slug, referenced files exist, and all cross-skill links resolve. Run:
   ```powershell
   python scripts/validate_skills.py --verbose
   python scripts/check_markdown_links.py
   ```
3. **Behavioral Test Verification:** Add structural or regression test cases in `tests/` where applicable. Run `python -m unittest discover -s tests`.
4. **Tone & Density Guidelines:** Keep only prose that changes a decision. Tell the agent what to do directly; omit fluff and redundant rationales. Point at structural sources (types, READMEs, config) per **principle-encode-lessons-in-structure**. Invoke other skills by path without duplicating their text.
5. **Open PR:** Invoke **Opening a PR** (`playbooks/opening-a-pr.md`).

**Reply:** summary of the skill, key architectural decisions, validation results, and test evidence.
