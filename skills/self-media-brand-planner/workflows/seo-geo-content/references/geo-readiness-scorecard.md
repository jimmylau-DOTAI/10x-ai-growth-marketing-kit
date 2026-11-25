# GEO Readiness Scorecard

Use this scorecard for internal review after the visible draft、metadata、link ledger、evidence ledger and FAQ／Schema decision are available. It measures readiness signals, not ranking、citation or conversion.

| Dimension | Weight | Full-credit evidence |
| --- | ---: | --- |
| Search job and answer architecture | 20 | Primary Query matches title and opening；direct answer arrives before promotion；major sections answer real reader questions with enough context |
| Evidence and claim boundaries | 20 | Important claims are traceable；public data has year、geography、sample／denominator、scope and direct source when `reader_evidence` is selected |
| Owned authority and originality | 20 | Company judgments have reasons；Owned Answer Units add distinct work value；no external method is renamed as company IP |
| Entity、scope and local meaning | 15 | Entities、dates、location and applicability are explicit；market claims and local scenarios are not confused |
| Reader links、CTA and decision support | 10 | Every public link has a reader purpose and verified target；one CTA fits the article and current Offer status |
| Metadata、FAQ／Schema and technical alignment | 15 | H1／Meta／slug agree；visible FAQ matches structured data；heading、image and CMS decisions match the rendered article |
| **Total** | **100** | |

## Scoring rules

- Give points only for visible or internally traceable evidence. Do not award points because the draft is long.
- Link count、statistic count、FAQ count and brand-name count are not scoring inputs.
- A high number of citations cannot compensate for an unclear answer or unsupported interpretation.
- A company mention without an owned reason、method、evidence、boundary or next action earns no authority credit.
- Keep explicit deductions for a stale／unverified Offer、local demo CTA、missing denominator、unsupported market-wide wording、FAQ／Schema mismatch、unresolved image rights or `SOURCE_NEEDED` claims still present in public copy.
- Report the score with evidence pointers and open items. Do not present it as a probability of being cited by an AI system.

## Receipt

```markdown
## GEO readiness

- Score: /100
- Status: DRAFT / GEO_REVIEW_READY / BLOCKED

| Dimension | Weight | Score | Evidence pointer | Open item |
| --- | ---: | ---: | --- | --- |
| Search job and answer architecture | 20 |  |  |  |
| Evidence and claim boundaries | 20 |  |  |  |
| Owned authority and originality | 20 |  |  |  |
| Entity、scope and local meaning | 15 |  |  |  |
| Reader links、CTA and decision support | 10 |  |  |  |
| Metadata、FAQ／Schema and technical alignment | 15 |  |  |  |
| **Total** | **100** |  |  |  |
```

`GEO_REVIEW_READY` means the draft passed this internal readiness review. It does not mean published、indexed、selected、absorbed、attributed、stable or converted.
