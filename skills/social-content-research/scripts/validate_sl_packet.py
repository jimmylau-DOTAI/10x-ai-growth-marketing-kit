#!/usr/bin/env python3
"""Validate one social Source Receipt and its matching SL note."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ACCESS_STATES = {"FULL", "PARTIAL", "IMAGE_ONLY", "BLOCKED"}


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


def require_keys(meta: dict[str, str], keys: list[str], label: str, errors: list[str]) -> None:
    for key in keys:
        if not meta.get(key):
            errors.append(f"{label}: missing frontmatter key '{key}'")


def require_headings(text: str, headings: list[str], label: str, errors: list[str]) -> None:
    for heading in headings:
        if not re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE):
            errors.append(f"{label}: missing section '## {heading}'")


def validate(source_path: Path, sl_path: Path) -> list[str]:
    errors: list[str] = []
    try:
        source_text = source_path.read_text(encoding="utf-8")
        sl_text = sl_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"read error: {exc}"]

    source_meta = frontmatter(source_text)
    sl_meta = frontmatter(sl_text)

    require_keys(
        source_meta,
        [
            "type",
            "status",
            "source_id",
            "source_ref",
            "source_type",
            "captured",
            "access_state",
            "retrieval_method",
            "content_scope",
            "origin_id",
        ],
        "source",
        errors,
    )
    require_keys(
        sl_meta,
        [
            "type",
            "status",
            "source_id",
            "source_ref",
            "created",
            "access_state",
            "knowledge_status",
            "content_scope",
            "candidate_count",
            "review_status",
        ],
        "sl",
        errors,
    )

    if source_meta.get("type") != "social_source_record":
        errors.append("source: type must be social_source_record")
    if sl_meta.get("type") != "social_source_learning":
        errors.append("sl: type must be social_source_learning")
    if source_meta.get("source_id") != sl_meta.get("source_id"):
        errors.append("source_id does not match")
    if source_meta.get("source_ref") != sl_meta.get("source_ref"):
        errors.append("source_ref does not match")
    if source_meta.get("content_scope") != "social-post-research-only":
        errors.append("source: content_scope must be social-post-research-only")
    if sl_meta.get("content_scope") != "social-post-research-only":
        errors.append("sl: content_scope must be social-post-research-only")
    if sl_meta.get("knowledge_status") != "source-learning-not-approved-insight":
        errors.append("sl: knowledge_status must remain source-learning-not-approved-insight")
    if sl_meta.get("status") != "queued-for-insight-review":
        errors.append("sl: status must be queued-for-insight-review")
    if source_meta.get("access_state") not in ACCESS_STATES:
        errors.append("source: invalid access_state")
    if sl_meta.get("access_state") not in ACCESS_STATES:
        errors.append("sl: invalid access_state")

    require_headings(
        source_text,
        ["Access receipt", "Evidence inventory", "Limitations", "SL route"],
        "source",
        errors,
    )
    require_headings(
        sl_text,
        ["30 秒理解", "Coverage", "完整攻略", "Candidate Insight cards", "Evidence boundary"],
        "sl",
        errors,
    )

    candidates = re.findall(r"^####\s+Candidate\s+\d+\s*$", sl_text, re.MULTILINE)
    try:
        declared_count = int(sl_meta.get("candidate_count", ""))
    except ValueError:
        declared_count = -1
        errors.append("sl: candidate_count must be an integer")
    if declared_count != len(candidates):
        errors.append(
            f"sl: candidate_count says {declared_count}, found {len(candidates)} Candidate headings"
        )

    blocks = re.split(r"^####\s+Candidate\s+\d+\s*$", sl_text, flags=re.MULTILINE)[1:]
    required_card_fields = [
        "candidate_key:",
        "一句見解",
        "來源證據",
        "邊界",
        "Post relevance",
    ]
    for index, block in enumerate(blocks, start=1):
        for field in required_card_fields:
            if field not in block:
                errors.append(f"sl: Candidate {index} missing '{field}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--sl", required=True, type=Path)
    args = parser.parse_args()

    errors = validate(args.source, args.sl)
    if errors:
        print("SL_PACKET_FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "status": "SL_PACKET_PASS",
                "source": str(args.source),
                "sl": str(args.sl),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
