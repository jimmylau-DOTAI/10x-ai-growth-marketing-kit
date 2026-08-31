#!/usr/bin/env python3
"""Create a safe, project-local Instagram Carousel planning workspace."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "project-template"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", required=True, help="Absolute destination path")
    parser.add_argument("--project-name", required=True, help="Human-readable project name")
    return parser.parse_args()


def replace_tokens(path: Path, project_name: str) -> None:
    if path.suffix.lower() not in {".md", ".yaml", ".jsonl"}:
        return
    text = path.read_text(encoding="utf-8")
    path.write_text(text.replace("{{PROJECT_NAME}}", project_name), encoding="utf-8")


def main() -> int:
    args = parse_args()
    destination = Path(args.project_dir).expanduser()
    if not destination.is_absolute():
        raise SystemExit("ERROR: --project-dir must be an absolute path")
    if destination.exists() and not destination.is_dir():
        raise SystemExit(f"ERROR: destination exists and is not a directory: {destination}")
    if destination.exists() and any(destination.iterdir()):
        raise SystemExit(f"ERROR: destination is not empty: {destination}")

    destination.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE_ROOT, destination, dirs_exist_ok=True)

    agents_template = destination / "PROJECT-AGENTS.template.md"
    agents_template.rename(destination / "AGENTS.md")

    for path in destination.rglob("*"):
        if path.is_file():
            replace_tokens(path, args.project_name)

    print(f"CREATED: {destination}")
    print("STATUS: BRIEF_REQUIRED")
    print("NEXT: complete brief.md; PREFERENCES.md is reused automatically")
    print("NOTE: no Style selection or HTML stage is created")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
