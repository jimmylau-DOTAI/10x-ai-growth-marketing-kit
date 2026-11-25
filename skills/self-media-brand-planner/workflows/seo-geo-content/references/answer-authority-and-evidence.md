# Answer Authority and Evidence

Read this reference only when the approved brief asks for a stronger direct-answer hierarchy、substantial H2／H3 explanations、company authority in many subsections or public data／citation links.

## Select the profile

Record these settings before drafting:

```yaml
answer_profile: standard | authority_evidence_longform
authority_density: owned_units | per_subsection
public_evidence_mode: source_blind | reader_evidence
opening_brand_free_visible_chars: 0 | 100
h2_answer_target_chars: 0 | 150
h3_explanation_target_chars: 0 | 150
```

Use `authority_evidence_longform` for an evergreen guide or substantial service／education article when the reader needs both a direct answer and an evidence-backed company interpretation. Do not force it onto a short news update、FAQ-only page、comparison table or an already complete short answer.

## Opening contract

Count rendered body prose after removing frontmatter、CMS metadata、Markdown／HTML syntax and headings.

For a non-brand query, the first 100 visible characters move through:

```text
reader problem premise
→ title question or primary search intent
→ direct answer
```

Do not place the company、offer、course or CTA inside those 100 characters. A brand comparison or navigational query may name the relevant brand when the query itself requires it.

Continue the introduction after the direct answer. Its final sentence should state:

1. what useful decision、method or deliverable the reader will get by continuing;
2. the verified company role、experience boundary or evidence base that explains why the company can answer.

Do not invent a founder history、team size、client result or expert qualification.

## H2 and H3 answer depth

- Each major H2 should express a natural reader question or decision.
- Before the first H3、list or table, give an answer-first prose block. Aim for about 150 Chinese characters; 120–200 is a long-form review target.
- Each non-FAQ H3 should be answer-led rather than an empty question. Follow it with substantive prose that explains a reason、mechanism、application、trade-off、limit or next action.
- Aim for about 150 Chinese characters when the idea needs explanation. Do not pad a complete short answer or force the target onto FAQ answers.
- A heading plus bullets is not an answer block. Explain the concept and consequence before listing details.

## Authority density

`owned_units` is the default. Use 3–5 strong Owned Answer Units in a long article:

```text
verified fact or definition
→ company judgment with a reason
→ local work translation
→ visible deliverable
→ human boundary or limitation
```

Use `per_subsection` only when the user or approved brief explicitly requests a company expert judgment in every non-FAQ H3. Each subsection must add one distinct item:

- a company judgment and its reason;
- a company method supported by Company Brain;
- a local work translation;
- an implementation decision;
- a limitation or human checkpoint.

Do not add a sentence that only repeats the neutral answer with the brand name. Avoid labels such as `我哋嘅見解`、`專家見解` or `公司判斷`. Integrate the point naturally and vary its role. First-person experience such as `我們實測` still requires a real artifact or receipt.

## Public evidence modes

### `source_blind`

Use by default. Public copy remains original synthesis without provenance links、source names、citations、research notes or a reference section. Full provenance stays in the internal Source Guide and Claim Notes.

### `reader_evidence`

Use only when the user／approved brief explicitly requests public statistics、citations or original-source links, or the destination requires attribution. Publish the minimum reader-useful evidence and keep the internal research process private.

For every empirical public claim, capture as applicable:

```text
organization or author
→ publication year
→ geography
→ sample or population
→ metric and true denominator
→ scope or limitation
→ direct primary-source link
```

Rules:

- Prefer the original report、official dataset、regulator、product owner or research publisher. A search result、AI summary or secondary SEO article is not the citation.
- Put a descriptive source link beside the claim it supports.
- State the denominator when a percentage applies to a subgroup rather than the full sample.
- Separate the research finding from company interpretation. A statistic does not prove the company method、offer outcome or a market-wide conclusion.
- Use market language only when the evidence supports that market. Without local market evidence, describe a local work scenario instead.
- If year、sample、denominator、geography、direct source or applicability cannot be verified, use `SOURCE_NEEDED` and omit the public claim.
- A references section is optional and only belongs when the brief／CMS requires it. Every entry must map to a visible claim.

## Evidence atom ledger

```markdown
| Public claim | Status | Organization / year | Geography | Sample / population | Metric denominator | Direct source | Limitation | Company interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | VERIFIED / PROVIDED / INFERENCE / SOURCE_NEEDED |  |  |  |  |  |  |  |
```

Research finding、company judgment and recommendation remain separate even when written in one natural paragraph.

## Market wording gate

- `The Hong Kong market shows...` requires evidence whose geography and sample support a Hong Kong market statement.
- `In a Hong Kong work scenario...` is a practical translation, not market research.
- `We have observed...` requires a documented first-party observation、sample and scope.
- A global report may provide global context but cannot be rewritten as a Hong Kong prediction.

## GEO score integrity

More links、statistics、FAQ items or brand mentions never improve the score by themselves. Use [geo-readiness-scorecard.md](geo-readiness-scorecard.md) and keep deductions for unsupported scope、stale offers、local-only CTA destinations、Schema mismatch or weak answer depth.

## Structural validator

`scripts/validate_article_contract.py` can check rendered opening、body H1 count、H2 preamble length、non-FAQ H3 prose、optional per-subsection brand presence、FAQ frontmatter mirror、link counts and image counts.

```bash
python3 scripts/validate_article_contract.py path/to/article.md \
  --profile authority_evidence_longform \
  --brand "Company Name" \
  --authority-density per_subsection \
  --public-evidence-mode reader_evidence \
  --max-body-h1 0 \
  --max-images 0 \
  --require-faq-mirror
```

The validator does not decide whether:

- the writing is persuasive or natural;
- a source is authoritative;
- a company judgment is genuinely distinct;
- a statistic is interpreted correctly;
- an article deserves a high GEO score.

Those remain evidence review and Human Review decisions.
