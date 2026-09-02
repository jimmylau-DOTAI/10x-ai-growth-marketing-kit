# Image Style Lab unified auto modes

Status: `IMPLEMENTED LOCALLY · JIMMY REVIEW REQUIRED · NOT INSTALLED OR PUBLISHED`

## Goal

Keep one student-facing `image-style-lab` entry point that can distil three evidence-backed candidate layers: visual `STYLE.md + DESIGN.md`, writing `TONE.md`, and a reusable workflow `SKILL.md + evals`. The merged Skill separates reusable systems from current content, tests them on new work, and supports platform-specific output without asking the student to understand Skill routing.

The existing `image-style-lab` package remains the artifact owner. Do not create a second Style Lab or require `design-md-creator` at runtime. Re-express the required method in original wording; do not copy upstream prose into the public package.

## User experience

`auto` is always the default. A user may name a mode directly, but never has to.

Example start:

> 幫我將呢批 reference 變成一個可以重用嘅 Style，用喺 IG Carousel。

Auto routing uses the requested destination and artifact. If the destination cannot be resolved from the brief or files, ask one plain-language question: `今次主要想用喺 SEO Banner、IG Carousel，定 IG 單圖？`

Do not ask the user to choose another Skill.

## Auto output layers and destinations

| Layer | Trigger evidence | Primary output |
|---|---|---|---|
| `style` | Repeatable visual hierarchy, composition, palette roles, materials or proof grammar | `STYLE.md + DESIGN.md` |
| `tone` | Repeatable voice, Hook, rhythm, narrative, vocabulary or CTA behaviour | `TONE.md` |
| `skill` | Repeatable inputs, decisions, steps, outputs, exceptions and quality gates | `SKILL.md + evals/evals.json` |

`seo-banner`, `ig-carousel`, `ig-single-image`, and `portable` are destination profiles, not student-selected modes. One source may support any combination of the three layers. There is no classroom mode; old classroom-only worksheets, teacher guides, and presets are not part of the published package.

## Unified workflow

### 1. Resolve mode and evidence

Create `AUTO-ROUTE.md` with detected candidate layers, target platform/format, source types, rights status, save boundary, and unresolved fields. Do not force all three outputs when the evidence supports fewer.

Classify each supplied item as Style reference, identity reference, content/proof reference, brand asset, or edit target. Preserve internal provenance and exclusions.

### 2. Distil the reusable system

Use the existing `PREFERENCE.md`, `REFERENCE.md`, `STYLE.md`, and `DESIGN.md` separation.

- `PREFERENCE.md`: what the user confirmed, what is observed, and what remains uncertain.
- `REFERENCE.md`: evidence, rights, hashes, reusable mechanisms, and do-not-copy boundaries.
- `STYLE.md`: recognition test, fixed rules, adjustable parameters, treatments, and break conditions.
- `DESIGN.md`: bounded tokens, composition vocabulary, proof/asset contract, mode-specific execution rules, negative patterns, and QA.

Rules must describe observable output. Numeric values, colours, typography roles, spacing and named components belong in the bounded vocabulary. Mechanical failures belong in deterministic validation where possible. Current topic, copy, campaign, product, person and CTA stay in the Content Job.

### 3. Build only supported candidates

- Visual evidence creates the existing portable Style pack.
- Language evidence creates one identity-safe `TONE.md`.
- Workflow evidence creates a concise candidate `SKILL.md` plus two scenarios and one hidden holdout in `evals/evals.json`.

### 4. Adapt the visual candidate by destination

- `seo-banner`: define article relationship, headline policy, proof modality, wide/mobile crop behaviour, publisher mark, and handoff to the selected page/blog production route.
- `ig-carousel`: define cover-to-body reading rhythm, card roles, continuity rules, proof placement, CTA card behaviour, mobile legibility and carousel-safe assets.
- `ig-single-image`: define one-message hierarchy, thumbnail recognition, subject/proof relationship, safe areas, caption boundary and single-frame CTA behaviour.

Mode adaptation may change canvas, reading rhythm, typography, CTA and proof placement. It must not silently change the shared Style identity.

### 5. Test before selection

Freeze realistic Content Jobs before testing. Keep the inputs and success rubric stable so Style guidance is the only intended variable.

For a new Style:

1. Keep one unguided baseline when practical.
2. Run the same job with the candidate Style pack.
3. Review structure, first-glance message, evidence fidelity and repeated failure patterns, not surface polish alone.
4. Convert repeatable corrections into Style rules, bounded vocabulary, or deterministic checks.
5. Require two materially different passing Content Jobs before proposing `STYLE_SELECTED`.

One attractive pilot remains `PILOT_REVIEW_STOP`.

## Multiple Styles per platform

One platform/format may contain any number of evidence-backed Styles. Do not force one default and do not cap the count.

Each saved Style must have:

- a unique Style ID and destination-specific Design ID;
- its own `REFERENCE.md`, `STYLE.md`, `DESIGN.md`, and permitted reference assets;
- one row in the platform Style selector/index;
- a clear status such as candidate, candidate operational, or approved according to the active Vault contract.

Auto mode may recommend the nearest existing Style or propose a new candidate. It must not silently select or register one.

## Exact save trigger

Vault writing is forbidden until the user explicitly says one of these current-task commands:

- `save it as style`
- `Save 做 Style`
- `入 Style`
- `加入 Style`
- `save it as tone`／`Save 做 Tone`／`入 Tone`
- `save it as skill`／`Save 做 Skill`／`入 Skill`

Analysis, pilot approval, `looks good`, validator pass, or a request to reuse a Style does not authorize a Vault write.

The explicit save command identifies one candidate layer. Style registration follows the steps below. Tone and Skill candidates first resolve their own platform／project canonical route and must not be written into the Visual Style tree.

1. Read the chosen Vault root rules and nearest platform/format index.
2. Resolve the exact Style selector, Style folder pattern, reference-asset destination, and Design ID namespace.
3. Duplicate-check Style IDs, Design IDs, slugs and equivalent visual grammar.
4. Run the route/save dry-run internally.
5. If there is no conflict or contract gap, create the new Style folder, copy the approved files/assets, update the exact Style index, and read everything back.
6. Open or show the saved `STYLE.md` and exact Style folder/index to the user.

Never overwrite an existing Style. A collision, missing index, ambiguous platform, unapproved reference right, or contract that would drop `DESIGN.md` stops the write and returns the exact conflict.

## Output shape

```text
<experiment>/
  AUTO-ROUTE.md
  PREFERENCE.md
  reference/reference-manifest.md
  styles/<style-id>/
    PREFERENCE.md
    REFERENCE.md
    STYLE.md
    DESIGN.md
    scorecard.md
    PLATFORM-ROUTE.md
    assets/reference-images/
  jobs/<job-id>/CONTENT-JOB.md
  tones/<tone-id>/TONE.md
  skill-candidates/<skill-id>/SKILL.md
  skill-candidates/<skill-id>/evals/evals.json
  tests/<test-id>/
    baseline/
    guided/
    review.md
```

Saved platform Styles remain separate from Content Jobs and generated outputs.

## Implemented scope

Update only `skills/image-style-lab/`:

- shorten `SKILL.md` around a natural student front door and auto routing;
- add focused auto, Tone, Skill-extraction and destination references;
- add `AUTO-ROUTE.md`, `TONE.md`, `SKILL-CANDIDATE.md`, and eval templates;
- add deterministic auto-route validation and focused tests;
- update existing platform/save references to recognise explicit Style, Tone, and Skill save commands;
- remove classroom mode and classroom-only resources from the public package;
- retain current reference, identity, proof, production, Vault and no-overwrite safeguards.

Do not install, publish, push, write to a real Vault, or change unrelated Skills.

## Verification

- `quick_validate.py` passes for the package.
- Existing helper-script tests still pass.
- New fixtures prove `style`, `tone`, and `skill` candidate routing.
- An unknown layer fails.
- A missing detected output fails when output checking is requested.
- No save occurs without an explicit save command.
- Each accepted save target validates only when that candidate layer exists.
- The existing Style saver remains dry-run first and refuses overwriting an existing Style.

## Done state

Stop at Human Review. Local validation is not installation, Vault registration, publication, or delivery.
