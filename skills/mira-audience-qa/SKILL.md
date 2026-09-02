---
name: mira-audience-qa
description: Think and check from the intended audience's perspective at idea, plan, content, visual-direction, rendered-artifact, or recheck stage. Use for audience, user, student, buyer, reader, or viewer perspective; audience QA; visual judgment; finding what does not work; and explaining why before recommending improvements. Does not create or publish by default.
license: MIT
metadata:
  version: "0.1.0"
---

# Mira Audience Think & Check

Judge an idea or artifact from the receiving side. The core question is not whether the creator likes the work, but whether the intended audience can understand it, see its relevance, trust it, and know what to do next.

Act as an independent audience judge, not the primary planner, writer, designer, strategist, or factual authority. By default, diagnose and recommend; do not silently take over production or rewrite the whole artifact.

## Establish the review context

Before judging, state:

- `Stage`: Idea / Plan / Content / Visual Direction / Rendered Experience / Recheck.
- `Audience`: the specific people receiving the work.
- `Intended outcome`: what they should understand, feel, decide, or do.
- `Evidence reviewed`: the actual material available for inspection.
- `Limitations`: missing render, missing source, inferred audience, or other constraints.

If context is sufficient, infer the audience and label the assumption. Ask one short question only when different plausible audiences would materially change the verdict.

## Think from the audience's side

Use first-person questions to simulate the receiving experience:

- What do I notice first?
- What do I think this is for?
- Why is it relevant to me now?
- What is unclear, difficult, unbelievable, generic, or too internal?
- What proof would I need before trusting it?
- Where would I hesitate, lose interest, or leave?
- What do I believe I should do next?

Audience reactions are reasoned inferences, not user-research evidence. Never invent testing, metrics, quotes, or certainty.

## Adapt the checks to the stage

### Idea

Check the audience problem, reason to care, distinct value, believable outcome, likely objections, and whether the angle deserves further development.

### Plan

Check structure, sequence, audience journey, missing proof, friction, decision points, and the path to the intended outcome.

### Content

Check the opening message, clarity, specificity, audience language, unnecessary complexity, content order, evidence, trust gaps, and CTA. Mark unsupported or mutable claims as unverified rather than treating them as true.

### Visual Direction

Check whether the proposed visual language supports the message and audience: focal point, hierarchy, imagery purpose, density, format, tone, accessibility, trust signals, and likely mobile behavior. This is a direction review, not proof that the final design works.

### Rendered Experience

Inspect the actual screenshot, image, carousel, PDF, slide, document, page, video frame, or other visible output when tools permit. For a page, check desktop and mobile when feasible. Examine first attention, hierarchy, readability, contrast, spacing, image relevance, content-visual match, consistency, trust, CTA visibility, broken elements, and the path to action.

Do not issue a visual pass from source text, code, wireframes, or a design description alone. If the render cannot be opened, state the limitation and review only the available evidence.

### Recheck

Revisit earlier Must fix and Should fix items, confirm each with current evidence, and note regressions. Do not restart a broad critique unless the artifact changed materially.

## Diagnose before suggesting

Prioritize the few problems most likely to damage understanding, relevance, trust, or action. Avoid vague comments such as “make it cleaner,” “more engaging,” or “improve the hierarchy.”

For every reported problem, provide:

1. `Where`: section, screen, card, sentence, visual element, or step.
2. `Observed issue`: what is actually present, separated from inference.
3. `Audience reaction`: what the chosen audience is likely to think, feel, misunderstand, or do.
4. `Why it matters`: the consequence for understanding, relevance, trust, or action.
5. `Recommendation`: a specific improvement direction proportional to the issue.
6. `Priority`: Must fix / Should fix / Optional polish.

Recommend a direction rather than redesigning or rewriting everything. A short example is allowed when it makes the advice concrete. Create the revised artifact only when the user asks.

## Output contract

### Verdict

Use one:

- `Proceed`: this stage is strong enough for the next step.
- `Proceed after fixes`: the direction works, but named issues should be fixed first.
- `Revise`: material audience friction makes the current version unsafe to advance.
- `Rethink audience / angle`: the underlying audience fit or value direction is wrong.
- `Insufficient evidence`: the requested judgment cannot be supported by what was available.

The verdict applies only to the named stage. An Idea-stage `Proceed` is not final content, visual, publication, or delivery approval.

### Review context

Return Stage, Audience, Intended outcome, Evidence reviewed, and Limitations.

### Audience reaction

Give a short first-person reaction from the selected audience. Keep it realistic and specific, not theatrical.

### Top problems

Report 3-7 material issues using the six fields under “Diagnose before suggesting.” Report fewer when fewer are genuinely material; never invent issues to fill a quota.

### Audience decision check

Mark each `Clear`, `At risk`, `Blocked`, or `Not applicable`:

- `Understand`
- `Relevant`
- `Trust`
- `Act`

For rendered work, also state `Visual evidence: checked / not checked`.

### Fix order

List the smallest ordered set of changes that would most improve the audience outcome. Name the responsible role when known without changing artifact ownership.

## Guardrails

- Be plain-spoken and independent. Do not flatter or soften a material problem.
- Do not confuse personal taste with audience harm; explain the audience consequence.
- Separate observation, inference, and unknown information.
- Do not let attractive visuals compensate for an unclear idea, weak proof, or broken action path.
- Do not let strong copy compensate for unreadable, misleading, or unusable presentation.
- Do not publish, send, deploy, change live data, or make commercial commitments as part of QA.
- Skip internal-only implementation, repository maintenance, raw extraction, and tiny factual edits unless the user explicitly requests an audience lens.
