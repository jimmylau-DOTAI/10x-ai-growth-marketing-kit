---
name: instagram-carousel-studio
description: Build a reusable Instagram carousel from a source or brief through topic and title selection, four-style comparison, editable HTML review, optional one-pass AI-image rendering, QA, and project-local learning. Use when creating or revising a 2–10 card educational, guide, framework, or insight carousel. Default to 10 cards at exactly 1080×1350px. Do not use this Skill to publish, automate delivery, or update an external Vault.
---

# Instagram Carousel Studio

Create one coherent story, not several posts forced into one carousel. Keep content, Style, rendering, and learning as separate decisions.

## Non-Negotiable Contract

- Render every card at exactly `1080×1350px`.
- Default to 10 cards. Use 2–9 only when the user explicitly requests another count.
- Decide the topic and title before writing the full carousel.
- Use the same approved cover content when comparing Styles.
- Make HTML the editable Human Review surface before final output.
- Preserve useful teaching substance. Attractive imagery without a clear insight fails.
- Generate each AI-image card once. Permit a second generation only for a hard visual blocker; prefer deterministic post-production for official logos and exact text.
- Never publish, deploy, schedule, send, install, or write to an external knowledge base without current-turn approval.
- Keep learning inside the consuming project unless the user explicitly approves another destination.

## Start Here

For a new consuming project, run:

```bash
python3 scripts/create_project.py --project-dir "/absolute/path/to/project" --project-name "Project name"
```

Read only the files needed for the current phase. Do not load every reference at once.

## Phase 1 — Lock The Brief

Read `project.yaml` and `brief.md`. Confirm or infer only these fields:

1. objective
2. audience
3. one_message
4. source_or_claim_boundary
5. CTA
6. language
7. card_count

Mark unstable or unsupported claims `TBC`. Do not invent scores, research findings, customer results, or automation destinations.

Offer five topic/title directions when the title is not approved. Stop for Human Review of the topic and title before completing all cards.

Then read [references/workflow.md](references/workflow.md) and write `content-plan.md`.

## Phase 2 — Choose The Style Route

Use exactly one route:

1. `existing_style`: load the approved project-local Style Capsule.
2. `reference_deconstruction`: classify supplied images, cluster visually different references, and create up to four bounded Style Capsules.
3. `starter_styles`: show the four bundled Starter Styles when no usable Style or references exist.

Read [references/style-intake.md](references/style-intake.md). Use [assets/style-picker.html](assets/style-picker.html) for the neutral four-style comparison and [references/starter-style-catalog.md](references/starter-style-catalog.md) for the design mechanisms.

Do not blend multiple reference clusters by default. Do not copy another creator's distinctive identity, private brand assets, or visible claims. Mechanism can be referenced; identity cannot.

Record the chosen route and Style ID in `project.yaml`. Copy and complete [assets/project-template/styles/STYLE-CAPSULE.template.md](assets/project-template/styles/STYLE-CAPSULE.template.md) as `styles/<style-id>/STYLE-CAPSULE.md`.

## Phase 3 — Build One 10-Card Story

Use this default rhythm, adapting it without changing the one story:

1. Cover: tension + promised outcome + CTA when applicable.
2. Recognition: the audience sees its current situation.
3. Misdiagnosis: explain why the obvious fix fails.
4. Reframe: introduce the core model.
5. Layer or step 1.
6. Layer or step 2.
7. Layer or step 3.
8. Layer or step 4, example, or diagnostic.
9. Application: what to do next.
10. Summary + one CTA.

Each card needs one job, one lead sentence, and supporting proof or explanation. Use cards 3–9 for knowledge density; do not stretch one sentence across several empty cards.

If using a comment-to-get-notes CTA, choose one short uppercase ASCII keyword. The cover, final card, caption, and real delivery route must use the identical keyword. If the asset or route is unverified, mark `needs_live_automation` and block publishing.

## Phase 4 — Produce Editable HTML

Read [references/html-contract.md](references/html-contract.md). Duplicate [assets/carousel-card-template.html](assets/carousel-card-template.html) for the carousel and replace the sample content.

Requirements:

- Self-contained HTML and CSS.
- One visible 1080×1350 stage per card.
- Actual text remains editable in HTML.
- No visible pagination unless the brief explicitly requests it.
- Respect safe zones and readable mobile hierarchy.
- Reserve only a quiet local logo zone; do not flatten the entire background for logo placement.

Stop at `HTML_REVIEW_REQUIRED`. Continue only after Human Review approves the content and direction.

## Phase 5 — Choose Final Route

### HTML Final

Use when exact wording, editable layout, diagrams, or deterministic typography matter most. Export the reviewed stages without changing the approved content.

### AI-Image Final

Read [references/imagegen-contract.md](references/imagegen-contract.md). Use one approved HTML card as the composition brief and one Style continuity reference when available.

- Keep Chinese as the primary visible language unless the brief says otherwise.
- Use official supplied logos as deterministic overlays after generation when exact identity matters.
- Select black or white logo treatment from the local background contrast.
- Do not rely on generated text for claim-critical wording.
- Generate cards in a controlled batch; review once as a contact sheet.

## Phase 6 — QA And Receipt

Read [references/qa-contract.md](references/qa-contract.md). Validate the project with:

```bash
python3 scripts/validate_project.py --project-dir "/absolute/path/to/project"
```

Write a run receipt under `reviews/`. A local file is not publishing proof. State whether the final status is:

- `HTML_REVIEW_REQUIRED`
- `FINAL_DRAFT_READY`
- `NEEDS_LIVE_AUTOMATION`
- `BLOCKED`

## Phase 7 — Project-Local Learning

Read [references/project-learning-loop.md](references/project-learning-loop.md).

Default `learning_mode` is `local_review_only`:

1. Capture Human Review as `KEEP / CHANGE / BAN / WHY`.
2. Save feedback in the current run receipt.
3. Update neither the Style Capsule nor this Skill automatically.
4. If the user explicitly says to save a rule, append one bounded candidate to `learning/candidates.md`.
5. After three independent, comparable carousel uses of the same candidate, create `learning/proposed-style-update.md`.
6. Apply the proposal to the project-local Style Capsule only after explicit Human approval.

One 10-card carousel counts as one use, not ten. Never transfer one project's learning into another project's identity without approval.

## Output Contract

Return:

- project path
- selected Style and route
- card count and dimensions
- HTML review path
- final output path, if produced
- QA status
- learning receipt path or `learning_mode: off`
- explicit statement that nothing was published unless destination read-back proves otherwise

Use [references/output-contract.md](references/output-contract.md) for the exact handoff format.
