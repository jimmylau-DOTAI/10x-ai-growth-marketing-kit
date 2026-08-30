#!/usr/bin/env python3
"""Validate the structural and production contract of a Carousel project."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_FILES = (
    "AGENTS.md",
    "project.yaml",
    "brief.md",
    "content-plan.md",
    "carousel.html",
    "style-picker.html",
    "learning/candidates.md",
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
    html_file = root / "carousel.html"

    if project_file.is_file():
        project_text = project_file.read_text(encoding="utf-8")
        dimensions = simple_yaml_value(project_text, "dimensions")
        count_text = simple_yaml_value(project_text, "card_count")
        if dimensions != "1080x1350":
            errors.append(f"dimensions must be 1080x1350, found {dimensions!r}")
        try:
            count = int(count_text or "")
            if not 2 <= count <= 10:
                errors.append(f"card_count must be 2–10, found {count}")
            if count != 10:
                warnings.append("card_count is not the default 10; confirm explicit user request")
        except ValueError:
            errors.append(f"card_count must be an integer, found {count_text!r}")

    if html_file.is_file():
        html = html_file.read_text(encoding="utf-8")
        compact = re.sub(r"\s+", "", html)
        if "width:1080px" not in compact or "height:1350px" not in compact:
            errors.append("carousel.html must declare a 1080px × 1350px card stage")
        card_ids = re.findall(r'id="C(\d{2})"', html)
        if project_file.is_file():
            count_text = simple_yaml_value(project_file.read_text(encoding="utf-8"), "card_count")
            try:
                expected_count = int(count_text or "")
                if len(card_ids) != expected_count:
                    errors.append(f"HTML contains {len(card_ids)} card stages; project.yaml expects {expected_count}")
            except ValueError:
                pass
        if "{{" in html or "}}" in html:
            warnings.append("carousel.html still contains template placeholders")

    tbc_files: list[str] = []
    for relative in ("brief.md", "content-plan.md"):
        path = root / relative
        if path.is_file() and "TBC" in path.read_text(encoding="utf-8"):
            tbc_files.append(relative)
    if tbc_files:
        message = "TBC placeholders remain in " + ", ".join(tbc_files)
        (errors if args.strict else warnings).append(message)

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    print("NOTE: structural QA is not Human Review or publishing proof")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
