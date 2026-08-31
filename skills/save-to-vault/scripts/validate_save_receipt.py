#!/usr/bin/env python3
"""Validate a Save to Vault receipt without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path


REQUIRED_FIELDS = {
    "type", "status", "created", "updated", "owner", "source_kind",
    "source_ref", "privacy", "human_review", "canonical_changes",
}
ALLOWED_STATUS = {"saved", "needs_human_review", "draft"}
ALLOWED_PRIVACY = {"internal", "confidential", "public", "mixed"}
ALLOWED_REVIEW = {"not_required", "pending", "required", "approved"}
REQUIRED_SECTIONS = {"Scope", "Active record", "Writes", "Exclusions", "Review and next step"}
SECRET_PATTERNS = {
    "OpenAI-style token": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "Slack token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{12,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            value = match.group(2).strip().strip('"').strip("'")
            result[match.group(1)] = value
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, help="Company Vault root")
    parser.add_argument("--receipt", required=True, help="Receipt path relative to Vault root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    vault = Path(args.vault).expanduser().resolve()
    receipt_arg = Path(args.receipt)
    errors: list[str] = []

    receipt_is_safe = True
    if receipt_arg.is_absolute() or ".." in receipt_arg.parts:
        errors.append("receipt must be a safe path relative to the Vault root")
        receipt = vault / "__invalid__"
        receipt_is_safe = False
    else:
        receipt = (vault / receipt_arg).resolve()
        if receipt != vault and vault not in receipt.parents:
            errors.append("receipt resolves outside the Vault root")
            receipt_is_safe = False

    if not (vault / "AGENTS.md").is_file() or not (vault / "INDEX.md").is_file():
        errors.append("vault root must contain AGENTS.md and INDEX.md")

    text = ""
    if not receipt_is_safe:
        pass
    elif not receipt.is_file():
        errors.append(f"receipt does not exist: {receipt_arg.as_posix()}")
    else:
        text = receipt.read_text(encoding="utf-8")

    fields = parse_frontmatter(text)
    missing = sorted(REQUIRED_FIELDS - fields.keys())
    if missing:
        errors.append("missing frontmatter fields: " + ", ".join(missing))
    if fields.get("type") not in {None, "save_to_vault_receipt"}:
        errors.append("type must be save_to_vault_receipt")
    if fields.get("status") not in {None, *ALLOWED_STATUS}:
        errors.append("invalid status")
    if fields.get("privacy") not in {None, *ALLOWED_PRIVACY}:
        errors.append("invalid privacy")
    if fields.get("human_review") not in {None, *ALLOWED_REVIEW}:
        errors.append("invalid human_review")
    if fields.get("source_kind") not in {None, "chatroom"}:
        errors.append("source_kind must be chatroom")
    if fields.get("owner") == "TBC" and fields.get("status") == "saved":
        errors.append("status cannot be saved while owner is TBC")

    for key in ("created", "updated"):
        value = fields.get(key)
        if value:
            try:
                date.fromisoformat(value)
            except ValueError:
                errors.append(f"{key} must use YYYY-MM-DD")

    headings = set(re.findall(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
    missing_sections = sorted(REQUIRED_SECTIONS - headings)
    if missing_sections:
        errors.append("missing sections: " + ", ".join(missing_sections))

    write_paths = re.findall(r"^- path:\s*(\S.*?)\s*$", text, flags=re.MULTILINE)
    if not write_paths:
        errors.append("Writes must contain at least one '- path:' entry")
    for raw_path in write_paths:
        target_arg = Path(raw_path.strip().strip('`'))
        if target_arg.is_absolute() or ".." in target_arg.parts:
            errors.append(f"unsafe write path: {raw_path}")
            continue
        target = (vault / target_arg).resolve()
        if target != vault and vault not in target.parents:
            errors.append(f"write path resolves outside Vault: {raw_path}")
        elif not target.exists():
            errors.append(f"write target does not exist: {raw_path}")

    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            errors.append(f"possible secret detected: {label}")

    payload = {
        "status": "SAVE_RECEIPT_PASS" if not errors else "SAVE_RECEIPT_FAIL",
        "receipt": receipt_arg.as_posix(),
        "write_targets_checked": len(write_paths),
        "errors": errors,
    }
    stream = sys.stdout if not errors else sys.stderr
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=stream)
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
