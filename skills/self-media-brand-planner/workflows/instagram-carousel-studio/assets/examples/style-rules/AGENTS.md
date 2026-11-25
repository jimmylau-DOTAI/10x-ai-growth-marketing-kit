# Visual rules teaching example

## Carousel Contract

- Use `instagram-carousel-studio` for content strategy and `ai-social-image-maker` for final images.
- Default to 10 cards at exactly 1080×1350px; use 2–9 only after an explicit request.
- Lock audience, one message, creator judgment, and title before the complete plan.
- Reuse `PREFERENCES.md` and the resolved reviewed Style automatically. If a new candidate is needed, route through package-local `image-style-lab`; keep content and Style choices inside the same conversation.
- This planning Skill does not render. The downstream image Skill generates complete native AI images.
- Require exact `CAROUSEL_PLAN_APPROVED` before image handoff and exact `C01_APPROVED` before generating the remaining cards.
- Never publish, send, deploy, schedule, or configure live automation without valid approval covering the current action and version.

## Learning Contract

- Learning stays in this project.
- Record reviewed runs as `KEEP / CHANGE / BAN / WHY`.
- The same run ID cannot increment one candidate twice.
- Three comparable independent carousels may generate a preference proposal; they do not auto-apply it.
- A directly confirmed user rule may generate a proposal immediately, but Human approval is still required before applying it.
- Do not update shared memory, an external Vault, or the reusable public Skill automatically.
