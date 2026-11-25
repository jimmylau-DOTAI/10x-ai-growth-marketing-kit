#!/usr/bin/env python3
"""Validate one Student Company Vault learning receipt without dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


REQUIRED_KEYS = {
    "title",
    "type",
    "status",
    "date",
    "project",
    "task",
    "platform",
    "format",
    "objective",
    "artifact",
    "artifact_status",
    "human_review",
    "signal_type",
    "candidate_key",
    "evidence_count",
    "loop_status",
    "rule_update_status",
    "updated",
}
REQUIRED_HEADINGS = {
    "## Artifact",
    "## Human feedback",
    "## Published evidence",
    "## Learning",
    "## Candidate",
}
ALLOWED_STATUS = {"awaiting_human_feedback", "signal_recorded", "published_review", "closed"}
ALLOWED_ARTIFACT_STATUS = {"draft", "approved", "published"}
ALLOWED_HUMAN_REVIEW = {"pending", "recorded"}
ALLOWED_SIGNAL = {"none", "preference", "quality", "workflow", "performance", "commercial"}
ALLOWED_LOOP_STATUS = {"not-a-signal", "log-only", "watch", "retest", "eligible-for-proposed-diff"}
ALLOWED_RULE_STATUS = {"none", "proposed", "approved_pending_apply", "applied", "rejected"}


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"\'')
    return values


def resolve_receipt(vault: Path, raw: str) -> Path:
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = vault / candidate
    return candidate.resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Company Vault learning receipt.")
    parser.add_argument("--vault", required=True, help="Company Vault root")
    parser.add_argument("--receipt", required=True, help="Receipt path, relative to Vault or absolute")
    args = parser.parse_args()

    vault = Path(args.vault).expanduser().resolve()
    receipt = resolve_receipt(vault, args.receipt)
    errors: list[str] = []

    if not (vault / "AGENTS.md").is_file():
        errors.append("invalid_vault_root")
    if not is_within(receipt, vault):
        errors.append("receipt_outside_vault")
    if receipt.is_symlink():
        errors.append("receipt_symlink_not_allowed")
    if not receipt.is_file():
        errors.append("receipt_not_found")

    allowed_roots = [
        vault / "20-Projects",
        vault / "30-學習與優化" / "任務收據",
    ]
    if is_within(receipt, vault) and not any(is_within(receipt, root.resolve()) for root in allowed_roots):
        errors.append("receipt_wrong_location")

    text = ""
    if receipt.is_file():
        try:
            text = receipt.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append("receipt_not_utf8")

    frontmatter = parse_frontmatter(text)
    missing = sorted(REQUIRED_KEYS - set(frontmatter))
    errors.extend(f"missing_frontmatter:{key}" for key in missing)
    errors.extend(f"missing_heading:{heading}" for heading in sorted(REQUIRED_HEADINGS) if heading not in text)

    if frontmatter:
        if frontmatter.get("type") != "learning_receipt":
            errors.append("invalid_type")
        checks = [
            ("status", ALLOWED_STATUS),
            ("artifact_status", ALLOWED_ARTIFACT_STATUS),
            ("human_review", ALLOWED_HUMAN_REVIEW),
            ("signal_type", ALLOWED_SIGNAL),
            ("loop_status", ALLOWED_LOOP_STATUS),
            ("rule_update_status", ALLOWED_RULE_STATUS),
        ]
        for key, allowed in checks:
            value = frontmatter.get(key)
            if value is not None and value not in allowed:
                errors.append(f"invalid_{key}:{value}")
        for key in ("date", "updated"):
            value = frontmatter.get(key, "")
            try:
                date.fromisoformat(value)
            except ValueError:
                errors.append(f"invalid_{key}")

        try:
            evidence_count = int(frontmatter.get("evidence_count", "-1"))
            if evidence_count < 0:
                raise ValueError
        except ValueError:
            evidence_count = -1
            errors.append("invalid_evidence_count")

        signal = frontmatter.get("signal_type")
        candidate = frontmatter.get("candidate_key", "")
        human_review = frontmatter.get("human_review")
        if signal == "none":
            if candidate not in {"none", "TBC"}:
                errors.append("non_signal_must_not_have_candidate_key")
            if evidence_count not in {-1, 0}:
                errors.append("non_signal_evidence_count_must_be_zero")
        elif signal:
            if human_review != "recorded":
                errors.append("signal_requires_recorded_human_review")
            if candidate in {"", "none", "TBC"}:
                errors.append("signal_requires_candidate_key")
            if evidence_count == 0:
                errors.append("signal_requires_evidence")

        artifact_raw = frontmatter.get("artifact", "")
        if artifact_raw in {"", "TBC", "none"}:
            errors.append("artifact_path_required")
        else:
            artifact = Path(artifact_raw).expanduser()
            if not artifact.is_absolute():
                artifact = vault / artifact
            artifact = artifact.resolve()
            if not is_within(artifact, vault):
                errors.append("artifact_outside_vault")
            elif not artifact.exists():
                errors.append("artifact_not_found")

    status = "LEARNING_RECEIPT_PASS" if not errors else "LEARNING_RECEIPT_FAIL"
    print(status)
    print(f"vault={vault}")
    print(f"receipt={receipt}")
    print(f"issues={len(errors)}")
    for error in errors:
        print(f"issue={error}")
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
