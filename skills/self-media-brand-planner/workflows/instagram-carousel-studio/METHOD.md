---
name: instagram-carousel-studio
description: Turn a source or brief into an approved 2–10 card Instagram carousel, including story directions, automatic routing to an existing or candidate Style, direct AI-image handoff, QA, and project-local learning. Use for a one-request content-to-carousel workflow. Default to 10 cards at exactly 1080×1350px. Does not build HTML, publish, or update shared knowledge automatically.
---

# Instagram Carousel Studio

Create one coherent story, not several posts forced into one carousel. Own the content strategy and review surface; hand approved cards to `ai-social-image-maker` for rendering.

## Non-Negotiable Contract

- Default to 10 cards. Use 2–9 only when the user explicitly requests another count.
- Target every final card at exactly `1080×1350px`.
- Lock objective, audience, one message, source boundary, creator judgment, and title before writing the full carousel.
- Give every card one job. Attractive filler does not count as teaching.
- Use one project-local `PREFERENCES.md` automatically when present. Do not repeat a brand interview; the user may choose content directions and Style directions separately within one Carousel conversation.
- Read an active approved `STYLE.md`／`DESIGN.md` when available. If none fits, or the user asks to explore／learn a supplied visual reference, automatically route that stage to package-local `image-style-lab`, receive a project-local candidate, then continue here. The user does not need to invoke another Skill.
- `image-style-lab` reference rules are mechanisms, not the brand identity. Active Vault brand DESIGN、TONE and genuine Logo assets take precedence over reference colours, subject appearance and copy style. A candidate remains project-local and review-required; do not save it as a shared Style automatically.
- Normal production stops at `CAROUSEL_PLAN_REVIEW_REQUIRED` before image handoff. An explicit request to see a first-image draft may use the preview-first route below; it does not approve the unseen plan or remaining images.
- Do not build HTML or generate final images in this Skill.
- Never publish, deploy, schedule, send, install, or update shared knowledge without valid approval for the action, content version and destination.
- Keep learning inside the consuming project. Never auto-modify this reusable `METHOD.md`.

## Start Here

When the user asks for a carousel with few prompts, directions to choose from, or a first image before reviewing all copy, read [references/preview-first.md](references/preview-first.md). This route owns the whole content-to-image handoff: do not make the user invoke a separate Caption Skill or copy files between Skills. Final images are still produced by `ai-social-image-maker`.

## Style route inside the same request

The Carousel main task owns the learner experience while each stage uses one production Skill:

1. Read the active Vault brand DESIGN／TONE、genuine Logo and any project `PREFERENCES.md`. At a new run or after a style correction, check the format Style Router and actual selected examples before trusting cached run preferences. A previously saved Style is not automatically selected for every job.
2. If a reviewed Style already fits this format and task, use it and show only useful story／composition choices.
3. If no suitable Style exists, or the user asks for more Style choices, check for supplied reference images. When references exist, announce and execute package-local `image-style-lab`; inspect the images and return a project-local `STYLE.md`／`DESIGN.md` candidate with evidence and limitations.
4. Present content directions as A／B／C and Style directions as 1／2／3 only when the user asked for both. These are independently selectable. Each Style direction names subject relationship、reading order、material／light、type treatment and brand adaptation; a colour label alone is not a Style.
5. After selection, return to this Skill for the ordered content plan. Pass the selected Style／DESIGN and exact brand adaptation to `ai-social-image-maker` for C01 and the remaining cards.

If no usable reference exists, create clearly labelled own-brand visual directions from the approved brand DESIGN. Call them `visual directions`, not a reference-derived or reusable Style. Ask for a reference only when the user specifically wants reference learning or a portable Style pack.

For a new consuming project, run:

```bash
python3 scripts/create_project.py --project-dir "/absolute/path/to/project" --project-name "Project name"
```

Read only the files required for the current phase.

## Phase 1 — Lock The Brief And Point Of View

Read `project.yaml`, `brief.md`, and `PREFERENCES.md`; route through the active Vault to the relevant TONE and brand assets. Follow confirmed brand language/voice and avoid importing the source creator's voice, identity or claims. Missing brand input is a gap to ask about, not permission to copy reference colours or skip Logo. Confirm or infer only:

1. objective
2. audience
3. audience's current tension or misconception
4. one message
5. source and claim boundary
6. creator judgment: what this carousel adds beyond repeating the source
7. CTA, language, and card count

Mark unstable or unsupported claims `TBC`. Separate source facts from creator interpretation. Do not invent customer results, research findings, product limits, or delivery routes.

If the angle or title is not approved, offer up to five audience-specific directions. Each direction must say who should care and why now. Stop for Human Review before completing every card.

Then read [references/workflow.md](references/workflow.md) and write `content-plan.md`.

## Authorized local batch preview

一般production仍先review角度、完整plan及C01。若用戶明確要求指定數量的整套本地試作／用戶模擬並授權AI完成，記其原話、數量與preview範圍；可先寫完整DRAFT plan，檢查C01後完成該批授權draft，最後一起review。這不是內容／Style的Human Approval，不自填CAROUSEL_PLAN_APPROVED。只有「幫我做Carousel」或--draft flag本身不算批次授權。`--draft` 匯出只供交接，真正生成授權須另外從當次用戶要求核對。

## Phase 2 — Build One Carousel Story

Use this default rhythm, adapting it to the idea rather than filling a template mechanically:

1. Cover: name the audience tension and promised payoff.
2. Recognition: show the audience's current situation.
3. Misdiagnosis: expose the common but incomplete interpretation.
4. Reframe: state the creator's core judgment.
5–8. Reasoning, layers, evidence, examples, or practical steps.
9. Application: what the audience should do differently.
10. Summary and one CTA.

When the user requests four cards, compress the story into hook → observation/reframe → practical action → summary/CTA; do not require absent cards 5–9 or add filler to reach ten.

Every row in `content-plan.md` needs `job`, `lead`, `support_or_proof`, `visual_role`, and `handoff`. Cards 1–10 must read as a single argument even without images. Remove any card that merely repeats the previous one.

For comment-to-get CTAs, use one short uppercase ASCII keyword. The cover, final card, caption, asset, and real delivery route must use the identical keyword. If the asset or route is unverified, set `NEEDS_LIVE_AUTOMATION`; do not imply delivery is live.

## Phase 3 — Content Review

Run the checks in [references/qa-contract.md](references/qa-contract.md), then validate the project:

```bash
python3 scripts/validate_project.py --project-dir "/absolute/path/to/project"
```

Show the complete ordered plan together. Set `CAROUSEL_PLAN_REVIEW_REQUIRED` and stop, except for an explicitly requested C01 draft under preview-first. A title approval alone is not approval of the complete plan.

A clear natural-language approval of this complete plan permits the next phase. Record the approved version and user decision; sync `Status: CAROUSEL_PLAN_APPROVED` in the plan and `status: CAROUSEL_PLAN_APPROVED` in project.yaml. These labels are records, not proof of approval by themselves.

## Phase 4 — Direct Image Handoff

After `CAROUSEL_PLAN_APPROVED`, call the installed `ai-social-image-maker` Skill with:

- absolute project path
- approved `content-plan.md`
- current `PREFERENCES.md`
- relevant approved assets from `references/ASSET-MANIFEST.md`, including genuine Logo path/rights and brand/format DESIGN and TONE sources; mark unresolved brand fields explicitly
- concrete reference-to-brand changes, including subject/scene and layout differences; image maker must complete its brand preflight before generation
- card count, language, and exact dimensions
- CTA delivery status

Write an actual file handoff before the image stage:

```sh
python3 PATH_TO_SKILL/scripts/export_image_jobs.py --project-dir PROJECT --output PROJECT/jobs-v1
```

This writes ordered `jobs-v1/C01/CONTENT-JOB.md` + `job.json` and a manifest. `--draft` is only for local review/demo export, never approval or generation permission. Include relative STYLE/DESIGN pointers in PREFERENCES.md and resolve them from the consuming project.

The image Skill owns generation, the C01 pilot, visual continuity, final image QA, and output receipts. It generates a complete native AI visual per card. Do not insert HTML, CSS cards, or background-plus-text composition. Visible copy is generated natively as part of the complete composition. The image Skill records a clean Logo corner, places the supplied original Logo when requested, and verifies the final canvas. Built-in generation is the default; an explicitly requested external runtime does not replace the image Skill's brand and completion requirements. users do not choose this mode or need Canva. If unavailable, deliver the self-contained job files and name the missing capability; do not route to a private Skill.

## Phase 5 — Learning Log And Three-Use Loop

Read [references/project-learning-loop.md](references/project-learning-loop.md). After each Human Review, record one bounded signal:

```bash
python3 scripts/record_learning.py \
  --project-dir "/absolute/path/to/project" \
  --run-id "carousel-2026-01" \
  --candidate-key "cover-audience-tension" \
  --decision KEEP \
  --rule "Open with the audience's misconception before the product detail" \
  --why "The intended reader understood immediately why the post mattered" \
  --evidence-type human_review \
  --receipt "reviews/carousel-2026-01.md"
```

The script automatically appends the learning log, updates the candidate count, and creates `learning/proposals/<candidate-key>.md` when the same candidate reaches three comparable independent carousel uses. It never applies the proposal.

A directly stated user preference may use `--direct-confirmed`; this creates a ready-for-review proposal without pretending it has three performance observations. Human approval is still required before editing `PREFERENCES.md`.

## Output Contract

Return:

- project path
- approved audience, one message, and creator judgment
- card count and dimensions
- content-plan path and approval status
- image-Skill handoff status and output path, if produced
- content and image QA status
- learning receipt and candidate count
- explicit statement that nothing was published unless destination read-back proves otherwise

Use [references/output-contract.md](references/output-contract.md) for the exact handoff format.

完整 10-card worked example：`assets/examples/style-rules/`，有 source、brief、content plan 同每卡實際 handoff。全部係 DRAFT，唔代表已獲准生成全套。
