---
name: ai-social-image-maker
description: Generate one complete social image or an ordered set of Instagram carousel images directly from an approved content plan and optional preference profile, without HTML. Use when the user wants native AI-generated 1080×1350 social images, a C01 pilot and review gate, one image-model call per final card, continuity QA, and a local output receipt. Do not use for content strategy, unapproved carousel plans, exact-logo recreation, publishing, or automatic preference updates.
---

# AI Social Image Maker

Turn approved content into complete, flattened social images. Do not add an HTML layout stage or produce separate background plates for later composition.

## Non-Negotiable Contract

- For a carousel, require explicit `CAROUSEL_PLAN_APPROVED` before any image generation.
- Generate C01 first and stop at `C01_REVIEW_REQUIRED`.
- Generate the remaining cards only after explicit `C01_APPROVED`.
- Make one native image-model call per final card. A second call is allowed only for one named hard blocker.
- Target exactly `1080×1350px` for every final image.
- Each output is a complete image: background, subject, hierarchy, visible copy, and visual treatment in one frame.
- Use the supplied `PREFERENCES.md` automatically. Do not present a Style chooser.
- Never invent an official logo, trademark, customer result, quotation, product UI, or claim.
- Never publish, send, deploy, schedule, or modify preferences automatically.

## Required Inputs

For one image:

- approved message and visible copy
- audience and content job
- exact dimensions
- optional `PREFERENCES.md`
- approved reference or identity assets
- output path

For a carousel:

- absolute project path
- `content-plan.md` with exact `CAROUSEL_PLAN_APPROVED`
- card count and ordered card IDs
- `PREFERENCES.md`
- relevant approved assets from `ASSET-MANIFEST.md`
- CTA delivery status

If the plan is incomplete or merely says `CAROUSEL_PLAN_REVIEW_REQUIRED`, return `CONTENT_APPROVAL_REQUIRED`. Do not infer approval from casual phrases such as “looks fine” when the complete plan was not shown.

## Phase 1 — Prepare One Self-Contained Card Brief

Read [references/imagegen-contract.md](references/imagegen-contract.md). Convert the approved card row into a bounded image brief containing:

1. card ID and content job
2. audience response to create
3. exact visible wording
4. visual subject or explanatory structure
5. composition and hierarchy
6. continuity rules from `PREFERENCES.md`
7. approved assets and forbidden inventions
8. exact output size and filename

Use only information needed for that card plus the minimum continuity context. Do not send the entire source archive to every generation call.

## Phase 2 — Generate C01 Only

Make one image-generation call for C01. Ask for a complete final social image at `1080×1350px`, not a mockup, slide canvas, HTML screenshot, or blank background.

Read back the actual file, dimensions, visible text, claims, and identity treatment. Create a C01 receipt and stop at `C01_REVIEW_REQUIRED`.

If a hard blocker exists—such as broken anatomy, unreadable headline, accidental logo imitation, or wrong core subject—name that blocker and permit one targeted retry. Taste-only exploration is a new direction and needs Human Review, not automatic retry loops.

## Phase 3 — Continue After C01 Approval

Only exact `C01_APPROVED` permits the remaining cards. Use approved C01 as the smallest continuity reference where the image tool supports it. Keep hierarchy, palette relationships, texture, focal scale, and recurring graphic language coherent without forcing every card into an identical layout.

Generate each remaining card in one separate call. Never treat ten cards as one multi-panel image.

## Phase 4 — Final QA

Read [references/qa-contract.md](references/qa-contract.md). Verify every file individually, then inspect an ordered contact sheet when available.

Important limitation: native image generation may misspell Chinese or English and cannot guarantee exact official logos. Claim-critical text and brand identity require Human Review. If exact copy or exact logo cannot be achieved inside the allowed calls, return `DETERMINISTIC_FINISH_RECOMMENDED`; do not claim the pure-AI image is exact.

Whole-image resizing to `1080×1350px` is allowed only when the source has the same aspect ratio and no crop or recomposition occurs. Record the resize. Do not crop away content to force compliance.

## Output Contract

Return:

- approval state received
- C01 path, actual dimensions, QA, and retry count
- Human decision on C01
- ordered final paths and actual dimensions
- contact-sheet path, if created
- unresolved text, claim, identity, or continuity issues
- generation receipt path
- explicit `not published` statement

Use [references/output-contract.md](references/output-contract.md) for the exact handoff.
