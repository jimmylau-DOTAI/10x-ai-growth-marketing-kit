#!/usr/bin/env python3
"""Report whether a Company Vault learning triage is due."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", text, re.MULTILINE)
    if not match:
        return "TBC"
    return match.group(1).strip().strip('"\'') or "TBC"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Company Vault triage due date.")
    parser.add_argument("--state", required=True, help="Path to LOOP-STATE.md")
    parser.add_argument("--today", help="Optional YYYY-MM-DD override for deterministic tests")
    args = parser.parse_args()

    state = Path(args.state).expanduser().resolve()
    if not state.is_file():
        print("TRIAGE_STATE_INVALID")
        print(f"issue=state_file_not_found:{state}")
        return 2

    text = state.read_text(encoding="utf-8")
    next_due = frontmatter_value(text, "next_triage_due")
    pending = frontmatter_value(text, "pending_signals")
    try:
        today = date.fromisoformat(args.today) if args.today else date.today()
    except ValueError:
        print("TRIAGE_STATE_INVALID")
        print("issue=invalid_today")
        return 2

    print(f"state={state}")
    print(f"today={today.isoformat()}")
    print(f"next_triage_due={next_due}")
    print(f"pending_signals={pending}")

    if next_due in {"", "TBC", "none", "null"}:
        print("TRIAGE_NOT_SCHEDULED")
        return 0

    try:
        due = date.fromisoformat(next_due)
    except ValueError:
        print("TRIAGE_STATE_INVALID")
        print("issue=invalid_next_triage_due")
        return 2

    if due <= today:
        print("TRIAGE_DUE")
    else:
        print("TRIAGE_NOT_DUE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
