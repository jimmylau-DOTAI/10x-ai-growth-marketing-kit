# Skill extraction

## Candidate threshold

Create a Skill candidate only when the Reference supports a repeatable job, not merely an attractive result. Evidence should reveal most of these:

- a recognisable user request or trigger;
- required inputs and source boundaries;
- decisions that change the route;
- a repeatable transformation;
- an observable output;
- failure, approval, or stop conditions;
- quality checks another agent can apply.

Missing elements stay `Proposed` or `Open`. Do not fill them with the source creator's private tools, credentials, clients, claims, or personality.

## Three-layer triage

- Judgment and decision criteria belong in `SKILL.md` prose.
- Numbers, names, tokens, formats, and allowed values belong in a bounded vocabulary or template.
- Mechanical failures belong in deterministic scripts when repetition and risk justify them.

Keep the entrypoint concise. Put conditional schemas, platform details, or substantial examples in references and load only the relevant one.

## Trigger and interaction

The description names the job using words a user would naturally say. It must not become a catchall for every task involving the same medium.

The generated Skill reads existing source before asking questions, asks only for gaps that materially change the work, and keeps technical receipts out of ordinary conversation.

## Behavioral evals

Deliver `evals/evals.json` with at least:

1. two normal, materially different scenarios;
2. one hidden holdout not used while revising;
3. realistic inputs or fixture files;
4. observable assertions covering task success, evidence fidelity, boundaries, and requested artifact;
5. retained baseline output or baseline notes.

Compare baseline and guided outputs without relying on typography or wording polish alone. Repeated human corrections become candidate rules; one-off preferences stay local.

Formal installation, publication, or replacement of an existing Skill requires duplicate check, owner review, package validation, and explicit approval.
