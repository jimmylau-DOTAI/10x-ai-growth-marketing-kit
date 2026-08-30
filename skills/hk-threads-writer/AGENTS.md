# AGENTS.md

## Project purpose

Build a public, portable Agent Skill for natural Hong Kong Threads copy.

## Scope

- Brand-neutral; no private company or personal voice rules.
- Draft only; no publish, schedule, account mutation or performance promise.
- Preserve facts, claims, names, links, quotes and evidence status.
- Every publishable segment must pass Python `len(text) <= 500`.

## Structure

- `SKILL.md` is the concise runtime entrypoint.
- Detailed writing rules live in `references/`.
- Deterministic checks live in `scripts/` and `tests/`.
- Behavioral cases and benchmarks live in `evals/`.

## Quality gates

- Use current `skill-creator` validation.
- Run all unittest files and eval package checks.
- Human Review is required for Hong Kong language quality.
- Do not install, publish, push or create a remote without current approval.
