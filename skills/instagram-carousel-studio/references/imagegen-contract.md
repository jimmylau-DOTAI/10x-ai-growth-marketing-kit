# AI-Image Rendering Contract

## One-Pass Default

Generate once per card from the approved content and Style Capsule. Do not generate a rough image and then regenerate the whole card as routine post-production.

Each card prompt should contain:

1. exact 4:5 vertical composition and 1080×1350 delivery target
2. the card's single communication job
3. focal subject or visual metaphor
4. hierarchy and reserved text zones
5. selected Style mechanisms
6. continuity rules shared across the series
7. local logo safe zone
8. negative constraints

Use the smallest continuity input that represents the selected Style. Do not feed all historical references into every card.

## Text And Logo

- Chinese is the visible default for Hong Kong-facing content.
- Keep product names in their official form.
- Use supplied official logo files for the deterministic overlay when exact identity matters.
- Choose black or white logo from contrast at the reserved local zone.
- Never replace an official logo with generated approximate lettering.
- Put claim-critical wording, CTA keywords, and dense teaching text in deterministic HTML or post-production.

## Retry Boundary

One retry is allowed only for a hard blocker such as wrong composition, unusable artifact, missing required identity subject, or impossible text zone. Log the blocker and the retry. Taste-only variations return to Human Review instead of starting an unbounded generation loop.
