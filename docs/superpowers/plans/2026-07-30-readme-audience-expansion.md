# README Audience Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Broaden the README positioning from a Hong Kong team-test audience to anyone who wants to grow with AI, while keeping Jimmy's Hong Kong practitioner perspective and the honest four-Skill release state.

**Architecture:** Change only three reader-facing areas in `README.md`: the hero promise, the audience line, and the roadmap introduction. Keep the four existing Skill descriptions and all safety boundaries unchanged.

**Tech Stack:** GitHub-flavored Markdown and shell-based content validation.

## Global Constraints

- Say that the kit will continue to add useful, tested Skills over time.
- State that four implemented Skills are the starting point.
- Explain that `10x` is a growth direction, not a limit of exactly ten Skills.
- Keep the current ten-Skill roadmap as the first development stage.
- Keep Hong Kong and Jimmy's real marketing practice as the distinctive perspective.
- Do not claim universal outcomes, unlimited growth, or a fixed delivery schedule.

---

### Task 1: Expand the README audience and future direction

**Files:**
- Modify: `README.md`
- Modify: `docs/superpowers/specs/2026-07-30-readme-productization-design.md`

**Interfaces:**
- Consumes: the approved positioning copy and the existing four-Skill README.
- Produces: a broader public-facing promise without changing implemented feature claims.

- [x] **Step 1: Update the hero**

Add the line:

```markdown
**A growing AI Marketing Skill Kit for everyone who wants to grow with AI.**
```

Explain in Chinese that four Skills are the starting point and that the kit will continue to test, improve, and add Skills based on real marketing work.

- [x] **Step 2: Update the audience line**

Replace the narrow audience definition with people who want to use AI to grow content, brand, campaigns, teams, or a business. Retain a short note that the methods come from Jimmy and Hong Kong practice.

- [x] **Step 3: Clarify the roadmap**

Before the roadmap table, state that `10x` is the direction of growth rather than a ten-Skill limit, and that the current roadmap is the first development stage.

- [x] **Step 4: Validate**

Run:

```bash
git diff --check
rg -n "everyone who wants to grow with AI|四個 Skills 只係起點|10x.*唔係限制|第一個發展階段" README.md
```

Expected: `git diff --check` exits `0`; all four positioning ideas are found.

- [x] **Step 5: Commit**

Run:

```bash
git add README.md docs/superpowers/specs/2026-07-30-readme-productization-design.md docs/superpowers/plans/2026-07-30-readme-audience-expansion.md
git commit -m "docs: broaden AI growth kit positioning"
```
