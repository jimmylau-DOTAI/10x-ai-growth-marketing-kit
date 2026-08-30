#!/usr/bin/env python3
"""Count every publishable Threads segment with Python len(text)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


LIMIT = 500


def count_segment(text: str) -> dict[str, int | str]:
    """Return the count receipt for one segment without changing its text."""
    if not isinstance(text, str):
        raise TypeError("segment text must be a string")
    count = len(text)
    return {
        "count": count,
        "remaining": LIMIT - count,
        "status": "PASS" if count <= LIMIT else "FAIL",
    }


def validate_payload(payload: dict) -> tuple[list[dict], bool]:
    """Validate and count a payload of independently publishable segments."""
    if not isinstance(payload, dict):
        raise TypeError("payload must be an object")
    segments = payload.get("segments")
    if not isinstance(segments, list) or not segments:
        raise ValueError("segments must be a non-empty list")

    seen_ids: set[str] = set()
    results: list[dict] = []
    for segment in segments:
        if not isinstance(segment, dict):
            raise TypeError("each segment must be an object")
        segment_id = segment.get("id")
        if not isinstance(segment_id, str) or not segment_id.strip():
            raise ValueError("segment id must be a non-empty string")
        if segment_id in seen_ids:
            raise ValueError(f"duplicate segment id: {segment_id}")
        seen_ids.add(segment_id)
        counted = count_segment(segment.get("text"))
        results.append({"id": segment_id, **counted})

    return results, all(item["status"] == "PASS" for item in results)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Count Threads segments using Python len(text)."
    )
    parser.add_argument("input", type=Path, help="JSON payload file")
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        results, passed = validate_payload(payload)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {"limit": LIMIT, "passed": passed, "segments": results},
            ensure_ascii=False,
            indent=2,
        )
    )
    if not passed:
        print("ERROR: one or more segments exceed 500 characters", file=sys.stderr)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
