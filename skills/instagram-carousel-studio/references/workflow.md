# Workflow

## State Machine

`BRIEF_REQUIRED → ANGLE_REVIEW_REQUIRED → CAROUSEL_PLAN_REVIEW_REQUIRED → CAROUSEL_PLAN_APPROVED → IMAGE_HANDOFF_READY`

The downstream image Skill may then use:

`C01_REVIEW_REQUIRED → C01_APPROVED → FINAL_DRAFT_READY`

Use `IMAGE_SKILL_REQUIRED` when `ai-social-image-maker` is unavailable. Use `NEEDS_LIVE_AUTOMATION` when a CTA promises delivery but its asset or route is unverified. Use `BLOCKED` when a missing source, decision, or approval materially changes the work.

## Brief To Story

1. Extract objective, audience, audience tension, one message, source boundary, creator judgment, CTA, language, and card count.
2. Distinguish `source_fact`, `creator_interpretation`, and `unknown`.
3. Propose up to five audience-specific angles if none is approved.
4. After angle approval, write the complete story in one sentence.
5. Assign exactly one job to each card.
6. Record `job`, `lead`, `support_or_proof`, `visual_role`, and `handoff` for every card.
7. Read all leads without support copy. They must form one coherent short argument.
8. Add definitions, reasoning, examples, diagnostics, proof, or practical steps. Remove filler.
9. Show the whole plan for Human Review before image handoff.

## Density Check

- Cover: one audience tension and one promised payoff.
- Interior lead: one concise claim or instruction.
- Support: enough to teach; never decorative filler.
- A card fails if removing its image leaves no useful idea.
- A card fails if it repeats the previous card without advancing the argument.
- The creator judgment must become visible by card 4 at the latest.

## CTA Check

Use one action only. For keyword CTAs, require short uppercase ASCII and repeat it exactly across cover, final card, caption, delivery asset, and automation route. Unverified delivery is `NEEDS_LIVE_AUTOMATION`, not live.
