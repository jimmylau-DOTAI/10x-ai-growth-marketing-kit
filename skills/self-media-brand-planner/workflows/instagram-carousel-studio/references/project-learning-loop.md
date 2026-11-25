# Project-Local Learning Loop

## Purpose

Improve one user's or project's working preferences without turning every reaction into a universal design rule. The reusable Skill owns the method; `PREFERENCES.md` owns local taste.

## Evidence Record

After Human Review, record:

- run ID and date
- candidate key
- `KEEP`, `CHANGE`, or `BAN`
- one bounded proposed rule
- `WHY`
- evidence type: `human_review` or `published_result`
- receipt path
- whether it was a directly confirmed user rule

Human preference and published performance are different evidence types. Do not merge them as if they prove the same claim.

## Comparable Independent Use

One complete carousel is one use. Ten cards are not ten uses. Revisions of the same carousel retain the same run ID and cannot increment the count.

Candidate keys must be bounded and testable, for example:

`cover-audience-tension`

with proposed rule:

`Open with the audience's misconception before introducing the product detail.`

Avoid keys such as `make-it-better` or rules such as “more creative.”

## Automatic Three-Use Loop

Use `scripts/record_learning.py`. It will:

1. reject duplicate run evidence for the same candidate
2. append a JSONL evidence record
3. update `learning/candidates.md` to `1/3`, `2/3`, or `3/3`
4. at `3/3`, generate `learning/proposals/<candidate-key>.md`
5. stop at `HUMAN_REVIEW_REQUIRED`

It never edits `PREFERENCES.md` or this public Skill. At three comparable uses, a Human decides whether the proposed line should be applied, revised, or rejected.

## Direct Confirmed Preference

When the user explicitly states a standing preference, use `--direct-confirmed`. The script creates a proposal marked `DIRECT_USER_RULE`; it does not claim three observations. Human approval is still required before applying the change to `PREFERENCES.md`.

## Destination Map

| Information | Destination |
|---|---|
| one run's feedback | `reviews/<run-id>.md` and `learning/log.jsonl` |
| bounded repeated candidate | `learning/candidates.md` |
| three-use or direct-rule proposal | `learning/proposals/<candidate-key>.md` |
| approved local preference | `PREFERENCES.md` |
| reusable method change | separate Skill revision with explicit approval |

No step writes to an external Vault, shared memory, dashboard, or public repository by default.
