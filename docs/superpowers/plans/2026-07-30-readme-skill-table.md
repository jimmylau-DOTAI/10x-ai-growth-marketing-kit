# README Skill Table Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a concise Skill summary table near the top of the README so readers can understand the implemented kit in ten seconds.

**Architecture:** Insert one `目前可用 Skills` section after the hero release-state block and before Jimmy's long-form rationale. Keep the existing detailed introductions and ten-Skill roadmap table unchanged.

**Tech Stack:** GitHub-flavored Markdown and repository-relative links.

## Global Constraints

- Include only the selected implemented Skills.
- Link every Skill name to its existing repository folder.
- Use the columns `Skill`, `幫你做乜`, `你需要提供`, and `主要輸出`.
- Keep each cell concise enough to remain readable on GitHub.
- Do not add planned Skills or imply that the roadmap is implemented.

---

### Task 1: Add and validate the implemented Skill table

**Files:**
- Modify: `README.md`
- Modify: `docs/superpowers/specs/2026-07-30-readme-productization-design.md`

**Interfaces:**
- Consumes: the selected existing `skills/*/` folders and their verified purpose, input, and output.
- Produces: one linked summary table that leads readers to the detailed Skill sections.

- [x] **Step 1: Add the table**

Insert this structure after the hero state block:

```markdown
## 目前可用 Skills

| Skill | 幫你做乜 | 你需要提供 | 主要輸出 |
| --- | --- | --- | --- |
| [Social Content Research](skills/social-content-research/) | ... | ... | ... |
| [SEO + GEO Content](skills/seo-geo-content/) | ... | ... | ... |
| [Social Post Writing](skills/social-post-writing/) | ... | ... | ... |
```

Use the approved concise Chinese descriptions rather than copying the longer sections.

- [x] **Step 2: Validate table content and links**

Run:

```bash
git diff --check
rg -n "^## 目前可用 Skills$|^\\| \\[.*\\]\\(skills/.*/\\)" README.md
```

Expected: one section heading and three linked rows.

- [x] **Step 3: Run README integrity checks**

Confirm all repository-relative links resolve, the heading hierarchy has no jumps, and the roadmap matches the current implemented set.

- [x] **Step 4: Commit**

Run:

```bash
git add README.md docs/superpowers/specs/2026-07-30-readme-productization-design.md docs/superpowers/plans/2026-07-30-readme-skill-table.md
git commit -m "docs: add implemented skills overview table"
```
