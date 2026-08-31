---
name: instagram-carousel-studio
description: Turn a source or brief into an approved 2–10 card Instagram carousel story and hand it directly to an AI social-image Skill. Use when the user needs audience-aware angles, creator judgment, one coherent carousel, content review, image-production handoff, QA, and project-local learning. Default to 10 cards at exactly 1080×1350px. This Skill does not choose styles, build HTML, generate final images, publish, or update shared knowledge automatically.
---

# Instagram Carousel Studio

Create one coherent story, not several posts forced into one carousel. Own the content strategy and review surface; hand approved cards to `ai-social-image-maker` for rendering.

## Non-Negotiable Contract

- Default to 10 cards. Use 2–9 only when the user explicitly requests another count.
- Target every final card at exactly `1080×1350px`.
- Lock objective, audience, one message, source boundary, creator judgment, and title before writing the full carousel.
- Give every card one job. Attractive filler does not count as teaching.
- Use one project-local `PREFERENCES.md` automatically when present. Do not ask the user to choose a Style.
- Five liked references may initialize or refine one preference profile; do not turn them into a style menu or average conflicting identities.
- Stop at `CAROUSEL_PLAN_REVIEW_REQUIRED`. Only an explicit approval of the complete plan permits image handoff.
- Do not build HTML or generate final images in this Skill.
- Never publish, deploy, schedule, send, install, or update shared knowledge without current-turn approval.
- Keep learning inside the consuming project. Never auto-modify this reusable `SKILL.md`.

## Start Here

For a new consuming project, run:

```bash
python3 scripts/create_project.py --project-dir "/absolute/path/to/project" --project-name "Project name"
```

Read only the files required for the current phase.

## Phase 1 — Lock The Brief And Point Of View

Read `project.yaml`, `brief.md`, and `PREFERENCES.md`. Confirm or infer only:

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

## Phase 2 — Build One Carousel Story

Use this default rhythm, adapting it to the idea rather than filling a template mechanically:

1. Cover: name the audience tension and promised payoff.
2. Recognition: show the audience's current situation.
3. Misdiagnosis: expose the common but incomplete interpretation.
4. Reframe: state the creator's core judgment.
5–8. Reasoning, layers, evidence, examples, or practical steps.
9. Application: what the audience should do differently.
10. Summary and one CTA.

Every row in `content-plan.md` needs `job`, `lead`, `support_or_proof`, `visual_role`, and `handoff`. Cards 1–10 must read as a single argument even without images. Remove any card that merely repeats the previous one.

For comment-to-get CTAs, use one short uppercase ASCII keyword. The cover, final card, caption, asset, and real delivery route must use the identical keyword. If the asset or route is unverified, set `NEEDS_LIVE_AUTOMATION`; do not imply delivery is live.

## Phase 3 — Content Review

Run the checks in [references/qa-contract.md](references/qa-contract.md), then validate the project:

```bash
python3 scripts/validate_project.py --project-dir "/absolute/path/to/project"
```

Show the complete ordered plan together. Set `CAROUSEL_PLAN_REVIEW_REQUIRED` and stop. A title approval alone is not approval of the complete plan.

Only exact approval such as `CAROUSEL_PLAN_APPROVED` permits the next phase. Record that status in `project.yaml` and the run receipt.

## Phase 4 — Direct Image Handoff

After `CAROUSEL_PLAN_APPROVED`, call the installed `ai-social-image-maker` Skill with:

- absolute project path
- approved `content-plan.md`
- current `PREFERENCES.md`
- relevant approved assets from `references/ASSET-MANIFEST.md`
- card count, language, and exact dimensions
- CTA delivery status

The image Skill owns generation, the C01 pilot, visual continuity, final image QA, and output receipts. Do not insert an HTML step. If the image Skill is unavailable, return `IMAGE_SKILL_REQUIRED` with the exact handoff package; do not silently replace it with improvised rendering.

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
