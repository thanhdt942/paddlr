# Feature Specification: Website Layout Redesign & Interactive Agent Installation Hub

- **Date:** 2026-11-19
- **Author:** Antigravity / Paddlr Engineering Discipline
- **Status:** Approved
- **Target URL:** `https://thanhdt942.github.io/paddlr/`

---

## 1. Objective

Refine the Paddlr landing page and documentation portal (`website/`) to implement the **Website Layout & Interaction Design Specification**, combining design principles from **Bun** (product-focused hero, sharp terminal visuals, concise copy), **Oh My Zsh** (approachable open-source developer personality), and **Astro** (clear information architecture and structured documentation navigation), centered around an interactive **Agent Compatibility & Installation Hub**.

---

## 2. Information Architecture (9 Sections)

1. **Navigation (`<header>`):**
   - Compact sticky bar (`56px` height) with Paddlr wordmark, `Features` (`#features`), prominent `Agents` (`#agents`), `How It Works` (`#how-it-works`), `Documentation` (`#docs`), `GitHub` link, and Light/Dark theme toggle.
   - Smooth anchor navigation, active section state, and responsive mobile drawer.
2. **Hero / Product Introduction (`#top`):**
   - Desktop two-column layout:
     - Left: Paddlr wordmark + version badge, tagline (*Simple on the Surface. Sophisticated Underneath.*), headline, concise explanation, Primary CTA (`Get Started` -> `#agents`), Secondary CTA (`Explore on GitHub`).
     - Right: Terminal showcase with verified repository commands and session output.
3. **Why Paddlr (`#why-paddlr`):**
   - Problem statement, motivation, *Above the Surface* vs. *Below the Surface* philosophy, What Paddlr Is vs. Is Not comparison, and four core engineering pillars.
4. **Agent Compatibility & Installation Hub (`#agents`):**
   - Heading: **Works With Your Favorite Coding Agents.**
   - Description: *"Use Paddlr with the coding agent you already love. Choose your agent and follow the installation instructions."*
   - **Agent Directory (4 Verified Agents):**
     - **Claude Code** (`Supported` — Marketplace & Direct Git methods)
     - **Google Antigravity** (`Supported` — `agy` CLI method)
     - **OpenCode** (`Supported` — OpenCode CLI, `opencode.json` v2, `opencode.json` v1, and Local Plugin methods)
     - **OpenAI Codex** (`Supported` — Two-step Codex CLI Marketplace & Install commands)
   - **Interactive Selection & Inline Installation Panel:**
     - Selecting a card highlights it and updates the connected installation panel without reloading.
     - Secondary method switcher for agents with multiple installation approaches (preserves active agent).
     - Separate terminal blocks and copy-to-clipboard buttons for commands that must be executed separately.
     - Displays agent name, support status badge, description, prerequisites, step-by-step installation commands, configuration details, verification command, minimal usage example, and link to detailed documentation.
     - Responsive behavior: Horizontal 4-card grid above the connected panel on desktop; stacked cards on mobile where the installation panel dynamically positions directly beneath the selected agent card.
5. **Core Features (`#features`):**
   - Varied editorial layout: one prominent full-width feature showcase (8 Agent Skills + Persistent `docs/paddlr/` Project Memory with live tree/command preview) plus supporting feature blocks with code/terminal examples (SessionStart hook, Destructive Git guardrail, Secret-safe `scan_repo.py`, Risk-proportional levels).
6. **How It Works (`#how-it-works`):**
   - 5-step visual sequence (`Understand -> Analyze & Plan -> Incremental Implement -> Evidence Verify -> Finalize`) with step numbers, headings, explanations, and concrete examples.
7. **Quick Start (`#quick-start`):**
   - Concise 4-stage getting-started guide (Prerequisites, Installation with CTA link to `#agents`, Initial Setup & Session Bootstrap, First Usage & Expected Result) with copy buttons and no redundant wall of agent instructions.
8. **Documentation & FAQ (`#docs`, `#faq`):**
   - Organized documentation covering Installation, Configuration (`docs/paddlr/` & `rules/`), Usage, Slash Commands (`/pdl:*`), Agent Skills & Workflows, Customization, and Troubleshooting, followed by a concise FAQ accordion linking to relevant sections.
9. **Footer:**
   - Minimal footer with Paddlr branding, GitHub repository, documentation links, and Apache-2.0 license notice.

---

## 3. Maintainability & Technical Constraints

- **Pure HTML5, CSS3, Vanilla JS:** Zero frameworks or external runtime dependencies.
- **Data-Driven Agent Hub:** Store all agent metadata, installation methods, separate command steps, verification steps, and usage examples in a single structured `AGENTS_CATALOG` object in `website/assets/js/main.js` decoupled from rendering logic.
- **Relative Paths:** All assets use `./assets/...` and `./favicon.svg` for GitHub Pages `/paddlr/` compatibility.

---

## 4. Acceptance Criteria

- [ ] All 9 sections follow the exact specification order and design principles.
- [ ] `#agents` interactive hub renders all 4 verified agents with accurate `Supported` status, secondary method tabs, separate copyable command steps, verification commands, and mobile inline panel placement directly under the selected card.
- [ ] Core Features uses a varied showcase + supporting blocks layout with real code/terminal examples.
- [ ] All repository CI gates (`validate_skills.py`, `unittest`, `check_markdown_links.py`) and static anchor/asset checks PASS.
- [ ] Changes are deployed to `https://thanhdt942.github.io/paddlr/` via GitHub Actions and verified live.
