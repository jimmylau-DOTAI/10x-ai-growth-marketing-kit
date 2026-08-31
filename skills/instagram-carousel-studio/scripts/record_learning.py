#!/usr/bin/env python3
"""Record one reviewed carousel signal and maintain the three-use preference loop."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--candidate-key", required=True)
    parser.add_argument("--decision", required=True, choices=("KEEP", "CHANGE", "BAN"))
    parser.add_argument("--rule", required=True, help="One bounded, testable preference rule")
    parser.add_argument("--why", required=True)
    parser.add_argument(
        "--evidence-type", required=True, choices=("human_review", "published_result")
    )
    parser.add_argument("--receipt", required=True, help="Receipt path inside the project")
    parser.add_argument("--target-section", help="PREFERENCES.md heading; defaults to the decision")
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--direct-confirmed", action="store_true")
    return parser.parse_args()


def safe_value(value: str, label: str) -> str:
    value = value.strip()
    if not value:
        raise SystemExit(f"ERROR: {label} cannot be empty")
    return value


def safe_key(value: str) -> str:
    value = safe_value(value, "candidate key")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{1,79}", value):
        raise SystemExit(
            "ERROR: candidate key must be 2–80 characters using letters, numbers, dot, underscore, or hyphen"
        )
    return value


def load_records(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    if not path.exists():
        return records
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"ERROR: invalid JSONL at line {line_number}: {exc.msg}") from exc
        if not isinstance(record, dict):
            raise SystemExit(f"ERROR: JSONL line {line_number} must be an object")
        records.append(record)
    return records


def ensure_project_receipt(root: Path, receipt_value: str) -> str:
    receipt = Path(receipt_value)
    receipt = receipt if receipt.is_absolute() else root / receipt
    receipt = receipt.resolve()
    try:
        relative = receipt.relative_to(root)
    except ValueError as exc:
        raise SystemExit("ERROR: receipt must remain inside --project-dir") from exc
    if not receipt.is_file():
        raise SystemExit(f"ERROR: receipt not found: {receipt}")
    return relative.as_posix()


def group_key(record: dict[str, object]) -> tuple[str, str, str, str]:
    return (
        str(record.get("candidate_key", "")),
        str(record.get("decision", "")),
        str(record.get("rule", "")),
        str(record.get("evidence_type", "")),
    )


def render_candidates(records: list[dict[str, object]]) -> str:
    groups: dict[tuple[str, str, str, str], list[dict[str, object]]] = defaultdict(list)
    for record in records:
        groups[group_key(record)].append(record)

    lines = [
        "# Project-Local Learning Candidates",
        "",
        "Generated from `learning/log.jsonl`. Do not edit counts by hand.",
        "",
        "| candidate_key | decision | bounded rule | evidence | progress | receipts | status |",
        "|---|---|---|---|---:|---|---|",
    ]
    for key in sorted(groups):
        entries = groups[key]
        candidate_key, decision, rule, evidence_type = key
        direct = any(bool(entry.get("direct_confirmed")) for entry in entries)
        independent_runs = sorted({str(entry.get("run_id", "")) for entry in entries})
        receipts = sorted({str(entry.get("receipt", "")) for entry in entries})
        progress = "direct" if direct else f"{min(len(independent_runs), 3)}/3"
        status = "HUMAN_REVIEW_REQUIRED" if direct or len(independent_runs) >= 3 else "WATCH"
        escaped_rule = rule.replace("|", "\\|")
        lines.append(
            f"| {candidate_key} | {decision} | {escaped_rule} | {evidence_type} | {progress} | "
            f"{', '.join(receipts)} | {status} |"
        )
    return "\n".join(lines) + "\n"


def write_proposal(
    root: Path, record: dict[str, object], matching: list[dict[str, object]], direct: bool
) -> Path:
    proposal_dir = root / "learning" / "proposals"
    proposal_dir.mkdir(parents=True, exist_ok=True)
    candidate_key = str(record["candidate_key"])
    proposal = proposal_dir / f"{candidate_key}.md"
    unique = []
    seen: set[str] = set()
    for entry in matching:
        run_id = str(entry["run_id"])
        if run_id not in seen:
            unique.append(entry)
            seen.add(run_id)
    evidence = [record] if direct else unique[-3:]
    evidence_lines = "\n".join(
        f"- `{entry['run_id']}` — `{entry['receipt']}` — {entry['why']}" for entry in evidence
    )
    mode = "DIRECT_USER_RULE" if direct else "THREE_COMPARABLE_USES"
    text = f"""# Proposed Preference Update

Status: `HUMAN_REVIEW_REQUIRED`
Mode: `{mode}`
Candidate: `{candidate_key}`

## Evidence

{evidence_lines}

## Exact Proposed Change

- Target: `PREFERENCES.md` → `{record['target_section']}`
- Decision: `{record['decision']}`
- Proposed line: {record['rule']}

## Why

{record['why']}

## Human Decision

- [ ] Approve and apply to `PREFERENCES.md`
- [ ] Revise the proposed line
- [ ] Reject and keep the current preference profile

This proposal has not changed `PREFERENCES.md`, the reusable Skill, shared memory, or any external Vault.
"""
    proposal.write_text(text, encoding="utf-8")
    return proposal


def main() -> int:
    args = parse_args()
    root = Path(args.project_dir).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"ERROR: project directory not found: {root}")
    if not (root / "PREFERENCES.md").is_file():
        raise SystemExit("ERROR: PREFERENCES.md is missing")

    candidate_key = safe_key(args.candidate_key)
    run_id = safe_value(args.run_id, "run ID")
    receipt = ensure_project_receipt(root, args.receipt)
    record: dict[str, object] = {
        "date": safe_value(args.date, "date"),
        "run_id": run_id,
        "candidate_key": candidate_key,
        "decision": args.decision,
        "rule": safe_value(args.rule, "rule"),
        "why": safe_value(args.why, "why"),
        "evidence_type": args.evidence_type,
        "receipt": receipt,
        "target_section": safe_value(args.target_section or args.decision, "target section"),
        "direct_confirmed": bool(args.direct_confirmed),
    }

    learning_dir = root / "learning"
    learning_dir.mkdir(parents=True, exist_ok=True)
    log_path = learning_dir / "log.jsonl"
    records = load_records(log_path)
    if any(
        str(item.get("candidate_key")) == candidate_key and str(item.get("run_id")) == run_id
        for item in records
    ):
        raise SystemExit("ERROR: this candidate already has evidence from the same run ID")

    records.append(record)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    candidates_path = learning_dir / "candidates.md"
    candidates_path.write_text(render_candidates(records), encoding="utf-8")

    matching = [item for item in records if group_key(item) == group_key(record)]
    comparable = [item for item in matching if not bool(item.get("direct_confirmed"))]
    independent_count = len({str(item["run_id"]) for item in comparable})
    proposal: Path | None = None
    if args.direct_confirmed:
        proposal = write_proposal(root, record, [record], True)
    elif independent_count >= 3:
        proposal = write_proposal(root, record, comparable, False)

    print(f"RECORDED: {log_path}")
    print(f"CANDIDATE: {candidate_key}")
    print(f"PROGRESS: {'direct' if args.direct_confirmed else f'{min(independent_count, 3)}/3'}")
    if proposal:
        print(f"PROPOSAL: {proposal}")
        print("STATUS: HUMAN_REVIEW_REQUIRED")
    else:
        print("STATUS: WATCH")
    print("NOTE: PREFERENCES.md and the reusable Skill were not changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
