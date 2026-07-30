# README Productization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the team-test README with a Hong Kong Traditional Chinese product page that introduces Jimmy's point of view, teaches how Skills work, and lets readers install and test the four implemented marketing Skills.

**Architecture:** Keep the entire reader journey in the root `README.md`: pain and positioning first, teaching model second, four Skill explanations and handoffs third, then installation, testing, boundaries, repository map, roadmap, author note, and license state. Add the newly supplied presentation reference to `ATTRIBUTIONS.md`; existing Skill files remain unchanged.

**Tech Stack:** GitHub-flavored Markdown, repository-relative links, shell-based link and content validation.

## Global Constraints

- Use natural Hong Kong Traditional Chinese and Jimmy's first-person practitioner voice.
- State that four Skills are implemented and ten Skills are only the roadmap.
- Do not invent business results, client names, testimonials, usage numbers, or benchmarks.
- Do not add unsupported installers, compatibility claims, badges, or a public license.
- Keep `Human Review` before publication.
- Do not expose private absolute paths, credentials, contact PII, or internal client data.
- Do not copy distinctive wording, examples, diagrams, or brand language from the two reference repositories.

---

### Task 1: Rewrite and validate the root README

**Files:**
- Modify: `README.md`
- Modify: `ATTRIBUTIONS.md`
- Reference: `docs/superpowers/specs/2026-07-30-readme-productization-design.md`
- Reference: `TEAM-TEST-GUIDE.md`
- Reference: `10-SKILL-INTRO-AND-FLOW.md`
- Reference: `ATTRIBUTIONS.md`

**Interfaces:**
- Consumes: the four existing folders under `skills/`, current local-copy installation model, and the approved README design.
- Produces: one root README that serves as product introduction, learning entrypoint, installation guide, and navigation page.

- [x] **Step 1: Replace the current README content**

Write the following sections in this order:

1. Hero and release state.
2. The marketing problem Jimmy observed.
3. Prompt versus Skill.
4. Why Skills need rules.
5. Shared operating model.
6. Four Skill introductions, each with problem, Jimmy viewpoint, input, flow, output, and human checkpoint.
7. Four-Skill handoff diagram and one illustrative Hong Kong SME scenario.
8. Thirty-second installation for project, Codex, and Claude Code.
9. One starter test per Skill.
10. Six-step student learning loop.
11. Human approval and safety boundaries.
12. Repository map and ten-Skill roadmap.
13. Short Jimmy author note.
14. Team-test license status and attribution link.

Add a short `Raymond Hou — speak-human-tw` entry to `ATTRIBUTIONS.md` that identifies the MIT-licensed repository as presentation inspiration and states that its brand, writing-pattern rules, cases, eval content, and distinctive copy were not copied.

- [x] **Step 2: Check Markdown formatting**

Run:

```bash
git diff --check -- README.md
```

Expected: exit code `0` and no output.

- [x] **Step 3: Check repository-relative links**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import re

repo = Path.cwd()
text = (repo / "README.md").read_text()
links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
missing = []
for link in links:
    if link.startswith(("http://", "https://", "#")):
        continue
    target = link.split("#", 1)[0]
    if target and not (repo / target).exists():
        missing.append(link)
print({"relative_links": len(links), "missing": missing})
raise SystemExit(1 if missing else 0)
PY
```

Expected: `missing` is an empty list and exit code is `0`.

- [x] **Step 4: Check release honesty and privacy boundaries**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

text = Path("README.md").read_text()
required = [
    "四個",
    "Roadmap",
    "Human Review",
    "TEAM-TEST-GUIDE.md",
    "ATTRIBUTIONS.md",
]
forbidden = [
    "/Users/",
    "API key",
    "已發佈",
    "10 個完整 Skills",
    "MIT License",
]
missing = [item for item in required if item not in text]
found = [item for item in forbidden if item in text]
print({"missing_required": missing, "found_forbidden": found})
raise SystemExit(1 if missing or found else 0)
PY
```

Expected: both lists are empty and exit code is `0`.

- [x] **Step 5: Review the final diff**

Run:

```bash
git diff -- README.md
```

Confirm that the README and its necessary source attribution are the only product files changed, and that all four Skills have a point of view, flow, and output.

- [x] **Step 6: Commit the README**

Run:

```bash
git add README.md ATTRIBUTIONS.md docs/superpowers/specs/2026-07-30-readme-productization-design.md docs/superpowers/plans/2026-07-30-readme-productization.md
git commit -m "docs: productize marketing skills README"
```

Expected: one new commit containing the README and this implementation plan.
