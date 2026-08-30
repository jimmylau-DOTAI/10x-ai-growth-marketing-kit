# Writing Style and Platform Rules

Read this reference after the Source Guide and title are approved, before drafting the article. Read the HTML section again when creating a local preview.

## Editorial outcome

Move the reader from:

`我聽過呢樣嘢`

to:

`我明白真正改變咩、點樣影響我嘅工作，同下一步應該點做`

The default is a DotAI-derived practical-operator style. If the Project Company Brain contains an approved Brand Voice, use that voice while preserving the evidence、CTA、link and Human Review boundaries.

## Voice

- Use mostly written Traditional Chinese with natural Hong Kong wording. Keep necessary English product and technical terms, then explain them in plain language.
- Lead with a recognizable work friction before terminology. Name real work such as 客戶查詢、報價、帳單、落單、課室、內容審批、公司流程。
- State a mild, reasoned point of view. Useful patterns include `真正分別不是……而是……`、`較準確的說法是……`、`這不等於……`。
- Translate technology into work consequences: input、output、time、cost、risk、approval and next step.
- Show limitations and trade-offs plainly. Avoid hype such as `完全不用擔心`、`絕對`、`完美選擇`、`一步到位` or unsupported superlatives.
- Use the company name only for an owned judgment、method、verified experience、boundary or next step. Repeating the brand in every paragraph does not create authority.
- Use first-person experience such as `我們實測` only when a real setup、artifact or receipt exists.
- End one level above the tool or news item: workflow、decision method、adoption、governance or a concrete current action.

## Structure by reader job

| Reader job | Recommended movement |
| --- | --- |
| `what is／點解` | direct definition → mechanism → scope／limit → work consequence |
| `how to／點做` | promised deliverable → input → steps → output → QA／failure route |
| `compare／點揀` | decision criteria → same-task comparison → trade-off → recommendation by scenario |
| `news／what changed` | verified event → meaningful change → Hong Kong work impact → action／limit |
| `case／proof` | problem → delivery → artifact → exact result and scope → learning |
| `course／service` | audience problem → transformation → scope／deliverables → fit／limits → verified CTA |

Do not force every topic into the same template. Select the movement that matches the reader's actual decision.

## Opening and section grammar

- Put the primary search intent in the H1 and opening without keyword stuffing.
- News and launch articles begin with the verified event and meaningful change before company opinion.
- Evergreen explainers begin with a clear definition and current context, then the reader problem and reasoned recommendation.
- Do not open with a slogan、a blockquote verdict、the research process or an unsupported result.
- Every H2 answers one major reader question. Every H3 handles a function、step、comparison、limitation or scenario.
- Explain the concept and work consequence before using bullets or a table.
- Keep paragraphs self-contained enough to be understood when extracted, but do not turn the whole article into mechanical FAQ blocks.

For practical examples, use:

```text
場景／阻力
→ input／source
→ AI or tool action
→ visible deliverable
→ work value
→ limitation／human approval
```

For comparison evidence, use:

```text
same task／input／acceptance
→ environment differences
→ quality／time／cost／human correction
→ what the result supports
→ what it cannot prove
```

## Owned Answer Units

Create original, useful answer units rather than generic advice:

```text
verified fact／definition
→ company／author judgment with a reason
→ Hong Kong work translation
→ visible deliverable
→ human boundary／limitation
```

An article around 1,500 Chinese characters or more normally needs 3–5 strong units. A practical guide should contain two concrete work translations、one reasoned judgment and one owned next step. Add a named company method only when Company Brain or ownership evidence supports it; otherwise use a clearly reasoned editorial decision rule without presenting it as company IP.

Record each unit internally with its reader question、body location、visible output、boundary and claim label. Do not rename an external mechanism as a company invention; if the draft still contains only generic advice, report an originality gap.

## Public-copy discipline

- Keep Source names、URLs、citations、claim labels and research notes outside the public body unless a mandatory disclosure is approved.
- Do not narrate internal workflow language such as `source-backed`、`claim boundary`、`artifact`、`可驗收` or `review gate` unless it is genuinely useful to the reader.
- Keep a caveat only when it changes permission、safety、rights、availability、cost、confidence or the next decision.
- Separate fact、company judgment and recommendation through clear prose rather than repeating defensive disclaimers.

## SEO output rules

- H1 and Meta title share one search intent but do not need to be identical. H1 may be more human; Meta title may be more search-direct.
- Meta description states the reader problem、useful answer and scope accurately; it does not promise unsupported completeness or results.
- Use a short, descriptive slug.
- Use verb-result headings and descriptive link anchors.
- Add an internal-link plan only where another page advances the same reader job.
- Do not add keyword-stuffed headings、anchors、repetitive summaries or links merely to simulate SEO strength.

## GEO／AEO output rules

- Use a facts-first opening、clear entity names、definitions、dates and applicable scope.
- Give a one-to-three-sentence direct answer before deeper explanation for major questions.
- Make important answer units independently understandable without removing their limits.
- FAQ exists only for supported reader questions. A fixed FAQ count is not a GEO tactic.
- Recommend FAQ or Article Schema only when the visible article actually contains the matching content; do not invent schema-only claims.
- Do not promise recommendation、citation、ranking、traffic or conversion.

## Platform-ready production pack

An approved article pack should include:

- H1、Meta title、Meta description and slug;
- Primary Query、Search Intent and related reader questions;
- Article body and Owned Answer Unit ledger;
- Reader Link／CTA Ledger and internal-link plan;
- supported FAQ and Schema recommendation;
- image manifest and rights status;
- monitoring prompts and baseline fields when GEO monitoring is requested.

Keep measurement layers separate:

| Layer | Question |
| --- | --- |
| Discovery | Can the public page be fetched or indexed where observable? |
| Selection | Is the page listed as an answer source? |
| Absorption | Does the answer use a distinct claim or method from the article? |
| Attribution | Is that claim correctly linked or named? |
| Accuracy | Are entities、numbers、dates and limitations represented correctly? |
| Stability | Does the result persist across repeated runs? |
| Action | Is referral or CTA activity measured through a defined path? |

Publication proves only that the page exists. It does not prove any later layer.

## Local HTML rules

- Use semantic HTML with UTF-8、`<html lang="zh-Hant">`、one H1 and one `<main id="article">`.
- Preserve heading order、paragraph rhythm、tables、link anchors and image proximity on mobile and desktop.
- Use system CJK font fallbacks; do not depend on a font that has not been bundled or verified.
- Use descriptive `alt` for informative images and empty `alt` for decorative images.
- Keep Review-only assets and provenance outside public copy／export controls.
- Do not add Framer、CMS、tracking、publish or deploy behavior to the local review file.

## Final writing gate

Before `BLOG_REVIEW_STOP`, confirm:

- the opening answers the search job before promoting the company;
- every H2／H3 contains explanatory prose, not headings plus lists only;
- examples show input、action、deliverable、value and human boundary;
- company judgments have reasons and are not disguised external claims;
- the article contains enough original answer units to justify publication;
- Metadata、links、CTA、FAQ／Schema and image decisions match the visible article;
- public prose is natural and does not expose internal QA language.
