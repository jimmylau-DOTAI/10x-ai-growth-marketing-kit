#!/usr/bin/env python3
"""Cheap due check for the three-day SL insight review."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if item:
            values[item.group(1)] = item.group(2).strip("'\"")
    return values


def parse_day(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def optional_day(value: str | None) -> date | None:
    if not value or value.upper() in {"TBC", "NONE", "NULL"}:
        return None
    try:
        return parse_day(value)
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", required=True, type=Path)
    parser.add_argument("--today", default=date.today().isoformat())
    args = parser.parse_args()

    today = parse_day(args.today)
    if not args.state.exists():
        result = {
            "status": "INSIGHT_REVIEW_NOT_SCHEDULED",
            "reason": "state-file-missing",
            "today": today.isoformat(),
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0

    meta = frontmatter(args.state.read_text(encoding="utf-8"))
    try:
        cadence = int(meta.get("review_cadence_days", "3"))
    except ValueError:
        cadence = 3
    next_due = optional_day(meta.get("next_review_due"))
    last_review = optional_day(meta.get("last_review_at"))
    if next_due:
        due = next_due
    elif last_review:
        due = last_review + timedelta(days=cadence)
    else:
        result = {
            "status": "INSIGHT_REVIEW_NOT_SCHEDULED",
            "reason": "no-successful-review",
            "today": today.isoformat(),
        }
        print(json.dumps(result, ensure_ascii=False))
        return 0

    status = "INSIGHT_REVIEW_DUE" if today >= due else "INSIGHT_REVIEW_NOT_DUE"
    print(
        json.dumps(
            {
                "status": status,
                "today": today.isoformat(),
                "next_review_due": due.isoformat(),
                "days_until_due": (due - today).days,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
