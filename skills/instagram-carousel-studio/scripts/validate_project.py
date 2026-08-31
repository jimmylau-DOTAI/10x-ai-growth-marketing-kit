#!/usr/bin/env python3
"""Validate a Carousel content-plan workspace before image handoff."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_FILES = (
    "AGENTS.md",
    "project.yaml",
    "brief.md",
    "PREFERENCES.md",
    "content-plan.md",
    "learning/candidates.md",
    "learning/log.jsonl",
    "references/ASSET-MANIFEST.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", required=True)
    parser.add_argument("--strict", action="store_true", help="Fail when TBC placeholders remain")
    return parser.parse_args()


def simple_yaml_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*[\"']?([^\n\"']+)", text)
    return match.group(1).strip() if match else None


def main() -> int:
    args = parse_args()
    root = Path(args.project_dir).expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []

    if not root.is_dir():
        raise SystemExit(f"ERROR: project directory not found: {root}")

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing required file: {relative}")

    project_file = root / "project.yaml"
    expected_count: int | None = None
    if project_file.is_file():
        project_text = project_file.read_text(encoding="utf-8")
        dimensions = simple_yaml_value(project_text, "dimensions")
        count_text = simple_yaml_value(project_text, "card_count")
        if dimensions != "1080x1350":
            errors.append(f"dimensions must be 1080x1350, found {dimensions!r}")
        try:
            expected_count = int(count_text or "")
            if not 2 <= expected_count <= 10:
                errors.append(f"card_count must be 2–10, found {expected_count}")
            if expected_count != 10:
                warnings.append("card_count is not the default 10; confirm explicit user request")
        except ValueError:
            errors.append(f"card_count must be an integer, found {count_text!r}")

    plan_file = root / "content-plan.md"
    if plan_file.is_file():
        plan_text = plan_file.read_text(encoding="utf-8")
        card_rows = re.findall(r"(?m)^\|\s*(\d{1,2})\s*\|", plan_text)
        if expected_count is not None and len(card_rows) != expected_count:
            errors.append(
                f"content-plan.md contains {len(card_rows)} card rows; project.yaml expects {expected_count}"
            )
        expected_order = [str(index) for index in range(1, len(card_rows) + 1)]
        if card_rows != expected_order:
            errors.append("content-plan.md card rows must be ordered consecutively from 1")

    log_file = root / "learning" / "log.jsonl"
    if log_file.is_file():
        for line_number, line in enumerate(log_file.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"learning/log.jsonl line {line_number} is invalid JSON: {exc.msg}")

    tbc_files: list[str] = []
    for relative in ("brief.md", "PREFERENCES.md", "content-plan.md"):
        path = root / relative
        if path.is_file() and "TBC" in path.read_text(encoding="utf-8"):
            tbc_files.append(relative)
    if tbc_files:
        message = "TBC placeholders remain in " + ", ".join(tbc_files)
        (errors if args.strict else warnings).append(message)

    if (root / "carousel.html").exists() or (root / "style-picker.html").exists():
        warnings.append("legacy HTML or Style-picker file exists; it is not part of the current workflow")

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    print("NOTE: structural QA is not Human Review, image generation, or publishing proof")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
