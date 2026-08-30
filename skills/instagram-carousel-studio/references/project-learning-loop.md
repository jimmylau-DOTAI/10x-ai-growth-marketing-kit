# Project-Local Learning Loop

## Purpose

Improve one project's Style without turning every preference into a global rule. The reusable Skill owns the method; the consuming project owns its identity and learning.

## Default Mode

`learning_mode: local_review_only`

Alternative: `off`. Never default to shared, global, Company Vault, or automatic Skill learning.

## Per-Run Receipt

After Human Review, record:

- run ID and date
- source and approved title
- selected Style ID and version
- output path and status
- `KEEP`: specific mechanisms to retain
- `CHANGE`: specific mechanisms to test next time
- `BAN`: repeated failures to avoid
- `WHY`: audience, clarity, brand, production, or performance reason
- evidence type: `human_review` or `published_result`
- candidate key, if any

Human preference and published performance are different evidence types. Do not combine them as if they prove the same thing.

## Candidate Rule

A candidate must be bounded and testable, for example:

`cover.focal_object_scale: increase from about 35% to 50–60%`

Avoid vague candidates such as “make it more creative.”

One carousel is one independent use. Ten cards from the same carousel do not count as ten uses. A revision of the same carousel is not a fresh independent use unless the audience, content job, or test condition materially changes.

## Three-Use Gate

When the same candidate key appears in three comparable independent uses:

1. create `learning/proposed-style-update.md`
2. list all three receipts
3. distinguish observation, insight, hypothesis, and proposed decision
4. show the exact Style Capsule lines or fields to change
5. request Human approval

Only after approval may the project-local Style Capsule version change. Do not update the reusable Skill unless the user separately requests a Skill revision and the rule is genuinely cross-project.

## Destination Map

| Information | Destination |
|---|---|
| one run's feedback | `reviews/<run-id>.md` |
| bounded repeated candidate | `learning/candidates.md` |
| three-use proposal | `learning/proposed-style-update.md` |
| approved project identity | `styles/<style-id>/STYLE-CAPSULE.md` |
| universal method change | separate Skill revision with approval |

No step writes to an external Vault, shared memory, dashboard, or public repository by default.
