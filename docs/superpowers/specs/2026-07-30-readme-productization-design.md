# 10x AI Growth Marketing Kit README Productization Design

**Date:** 2026-07-30
**Scope:** Rewrite the repository root `README.md` and add the newly supplied presentation reference to `ATTRIBUTIONS.md`.
**Audience:** Hong Kong marketers, SME teams, AI course students, and non-technical operators trying agent skills for the first time.

## Objective

Turn the current team-test README into a Traditional Chinese, Hong Kong Cantonese product page and teaching entrypoint.

The README must let a new reader answer five questions without opening the skill files:

1. What problem does this kit solve?
2. Why did Jimmy build it this way?
3. What is a Skill, and why does it contain workflows and restrictions?
4. What can the four current Skills do together?
5. How can I install and test one safely?

## Reference Strategy

The README will synthesize, not copy, two public references:

- `coreyhaines31/marketingskills`: multi-skill navigation, shared context, skill handoffs, installation, and category clarity.
- `Raymondhou0917/speak-human-tw`: concrete pain-led introduction, author point of view, explicit boundaries, workflow explanation, quick start, and proof-oriented examples.

Jimmy's original contribution remains the largest layer:

- Hong Kong SME and marketer context;
- first-person practitioner observations;
- research → strategy → production → human review;
- source and claim discipline;
- Full Funnel planning and `Grill Me`;
- platform-native output rather than one post copied everywhere;
- teaching readers how to modify a Skill, not merely use Jimmy's answer.

The README must not reuse the references' distinctive copy, examples, diagrams, performance claims, badges, or brand language.

## Positioning

### Name

`10x AI Growth Marketing Kit`

### Primary line

「唔係再收集 Prompts，而係將你做 Marketing 嘅判斷，寫成 AI 可以重複執行嘅 Skills。」

### Supporting promise

Four installable Skills connect content research, Full Funnel campaign planning, SEO/GEO content, and platform-native social writing into one reviewable workflow.

### Audience and growth direction

- The kit is for anyone who wants to grow content, brand, campaigns, teams, or a business with AI.
- Hong Kong marketer and SME practice remains the distinctive source context, not an audience restriction.
- The four implemented Skills are the starting point.
- The current ten-Skill roadmap is the first development stage, not a permanent limit.
- `10x` describes the direction of capability and growth; it does not mean the repository will contain exactly ten Skills.
- New Skills should be added progressively only after they solve a real workflow and have been tested.

### Honest release state

- The repository currently contains four implemented Skills.
- The ten-skill document is a roadmap, not a claim that ten Skills are production-ready.
- The package is a private team-test release.
- No public distribution license is claimed.

## Voice and Language

- Traditional Chinese with natural Hong Kong Cantonese sentence structure.
- First-person Jimmy voice for practitioner observations.
- Clear enough for a non-technical marketer.
- Direct, specific, and teachable; avoid generic AI transformation claims.
- Use English terms where Hong Kong marketers normally use them: Skill, Prompt, Workflow, Full Funnel, SEO, GEO, Human Review.
- Explain an English term the first time when ambiguity is likely.
- No invented business results, client names, testimonials, usage numbers, or benchmark scores.
- Avoid heavy emoji use, slogan stacking, and repetitive rhetorical questions.

## Page Architecture

### 1. Hero

- Repository name.
- Pain-led headline.
- One concise explanation of the four-Skill kit.
- Current version and release status.
- Compatible agent environments already supported by the package.

### 2. The problem Jimmy observed

First-person explanation:

- marketers already know how to ask AI for output;
- a one-off prompt does not preserve company context, decision order, standards, or handoffs;
- polished output can still be unusable when it starts before research and strategy;
- a Skill captures judgment, workflow, constraints, and acceptance criteria.

### 3. What a Skill is

Explain the difference:

| Prompt | Skill |
| --- | --- |
| A one-time instruction | A reusable way of working |
| Relies on context in the current chat | Checks and gathers required context |
| Output can vary without a standard | Has workflow, format, guardrails, and QA |
| Hard to teach or hand over | Can be installed, inspected, tested, and modified |

### 4. Why there are restrictions

Map each component to its practical purpose:

- Trigger → prevent using the wrong Skill.
- Required context → prevent invention.
- Questions → fill material gaps.
- Workflow → preserve decision sequence.
- Output contract → make handoff possible.
- Guardrails → prevent false claims and unauthorized action.
- QA → define completion.
- Evals → test whether future edits break expected behavior.

Core statement:

「規限唔係為咗限制創意，而係令創意可以被驗收、重複同交接。」

### 5. The shared operating model

Show one compact text diagram:

```text
Company Context
      ↓
Research Evidence
      ↓
Strategic Decision
      ↓
Content Production
      ↓
Human Review
```

Clarify that each Skill can run independently, but the best result comes from handing reliable output to the next stage.

### 6. Four Skill introductions

Each section follows the same five-part pattern:

1. Concrete work problem.
2. Jimmy's reason for writing it.
3. Input.
4. Flow.
5. Output and human checkpoint.

#### `social-content-research`

Point of view: the common mistake is writing too early. Research must separate access state, evidence, interpretation, and original angles.

Flow:

`提供來源 → 確認可讀程度 → 提取證據 → 分開事實與判斷 → 找出內容角度 → 輸出 Research Brief`

Mention browser-visible sources, transcripts, screenshots, YouTube captions, and optional Whisper/FFmpeg workflows without promising universal extraction.

#### `full-funnel-campaign-planner`

Point of view: a campaign is not a list of posts. It connects business goal, audience, offer, funnel stage, message, assets, CTA, and measurement.

Flow:

`確認目標 → 標示已知與假設 → Grill Me → 設計 Funnel → 排內容與渠道 → 定義 CTA → 設定優先次序與交接`

Explain that `Grill Me` challenges weak assumptions one question at a time.

#### `seo-geo-content`

Point of view: SEO/GEO should begin with the user's problem, search intent, and claims the business can support, not with inserting keywords.

Flow:

`理解搜尋問題 → 研究來源 → 建立 Claim Map → 設計內容結構 → 寫 Draft → Citation／Fact QA → Human Review`

#### `social-post-writing`

Point of view: the same insight should not be pasted unchanged across platforms.

Flow:

`選擇可靠觀點 → 定義目標與平台 → 寫 Hook → 重組平台節奏 → 加 CTA → Brand Voice QA → 輸出 Draft Pack`

Mention current output coverage: Threads, LinkedIn, Facebook, and Instagram captions. Do not claim a separate production-ready carousel design Skill.

### 7. How the Skills work together

Show the existing verified sequence:

```text
來源／社交內容
      ↓
social-content-research
      ↓
full-funnel-campaign-planner
      ├── seo-geo-content
      └── social-post-writing
      ↓
Human review
```

Include one compact Hong Kong SME scenario, clearly labeled as an illustrative workflow rather than a client result.

### 8. Thirty-second start

Keep three installation paths:

- project-level `.agents/skills/`;
- personal Codex `~/.codex/skills/`;
- personal Claude Code `~/.claude/skills/`.

Use commands that match the current repository contents. Do not advertise an `npx` package, marketplace plugin, Cursor installer, or remote install command that has not been implemented and verified.

### 9. First test

Provide one starter instruction per implemented Skill. Tell users what a good first output should contain and direct them to `TEAM-TEST-GUIDE.md`.

### 10. How students should learn from the repository

Teaching loop:

1. Run the original Skill on a real task.
2. Identify one output that does not fit the student's company.
3. Locate the corresponding rule, reference, or output requirement.
4. Change one item only.
5. Rerun the same task.
6. Compare before and after.

Core lesson:

「你唔係要複製 Jimmy 嘅答案，而係學識將自己做事嘅判斷寫成 Skill。」

### 11. Boundaries

Retain and simplify the current safety boundaries:

- no invented company, customer, partnership, result, or claim;
- draft is not approval; approval is not publication;
- no automatic publishing, messaging, ad spend, or personal-data handling;
- current external claims require verification;
- humans approve brand position and public output.

### 12. Repository map and roadmap

- Briefly explain the current files.
- Link the four Skill folders.
- Link `TEAM-TEST-GUIDE.md`, `10-SKILL-INTRO-AND-FLOW.md`, and `ATTRIBUTIONS.md`.
- Clearly label the ten-skill plan as a roadmap.

### 13. Author note

Use a short first-person note:

- Jimmy works across design, marketing, growth marketing, and AI Growth Builder practice.
- The kit comes from repeatedly turning real marketing work into source-aware, reviewable agent workflows.
- The goal is to help non-technical marketers become builders of their own operating methods.

Do not add unverified biography, client claims, course outcomes, follower counts, or external promotional links.

### 14. License status

Keep the current team-test wording. Do not add an MIT badge or license until Jimmy explicitly chooses a public release license.

## Link and Content Rules

- All repository-relative links must resolve.
- No private absolute paths may appear in the README.
- No credentials, tokens, contact PII, or internal client data.
- External references belong in `ATTRIBUTIONS.md`; the README may briefly credit inspiration without presenting copied content as original.
- Code blocks must be directly runnable within the stated local-clone context.

## Acceptance Checks

The rewritten README passes when:

1. A new marketer can explain the difference between a Prompt and a Skill.
2. A student can describe why the workflow contains restrictions.
3. All four implemented Skills have an intro, Jimmy point of view, flow, and output.
4. The README never implies all ten roadmap Skills are complete.
5. Installation commands match the repository.
6. Every relative link resolves.
7. The page contains no private local path, placeholder, invented result, or unsupported compatibility claim.
8. The README preserves human approval and verification boundaries.
9. Language reads as natural Hong Kong Traditional Chinese rather than translated documentation.
10. The two references influence structure and presentation without copied wording or examples.

## Out of Scope

- Editing the four `SKILL.md` files.
- Creating per-Skill human-facing README files.
- Adding reference, example, eval, install, image, or automation files.
- Changing repository visibility or license.
- Publishing, pushing, or opening a pull request.

Those remain part of the later v0.2 productized toolkit implementation after the root README is approved. The only adjacent documentation change in this scope is the required `speak-human-tw` credit in `ATTRIBUTIONS.md`.
