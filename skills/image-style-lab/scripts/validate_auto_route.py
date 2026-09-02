#!/usr/bin/env python3
"""Validate Image Style Lab AUTO-ROUTE.md decisions and optional candidate outputs."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ALLOWED_MODES = {"auto", "reuse-saved-style"}
ALLOWED_TARGETS = {"portable", "seo-banner", "ig-carousel", "ig-single-image"}
ALLOWED_OUTPUTS = {"style", "tone", "skill"}
ALLOWED_SAVE_TARGETS = {"none", "style", "tone", "skill"}


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"'")
    return result


def parse_outputs(raw: str) -> set[str]:
    value = raw.strip().strip("[]")
    return {
        item.strip().strip("\"'")
        for item in value.split(",")
        if item.strip()
    }


def has_candidate(experiment: Path, output: str) -> bool:
    if output == "style":
        return any((path / "STYLE.md").is_file() and (path / "DESIGN.md").is_file()
                   for path in (experiment / "styles").glob("*"))
    if output == "tone":
        return any((path / "TONE.md").is_file() for path in (experiment / "tones").glob("*"))
    return any(
        (path / "SKILL.md").is_file() and (path / "evals" / "evals.json").is_file()
        for path in (experiment / "skill-candidates").glob("*")
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("route", type=Path)
    parser.add_argument("--check-outputs", action="store_true")
    args = parser.parse_args()

    route = args.route.expanduser().resolve()
    errors: list[str] = []
    if not route.is_file():
        errors.append(f"route file not found: {route}")
        metadata: dict[str, str] = {}
        text = ""
    else:
        text = route.read_text(encoding="utf-8")
        metadata = frontmatter(text)

    mode = metadata.get("route_mode", "")
    target = metadata.get("target_use", "")
    outputs = parse_outputs(metadata.get("detected_outputs", ""))
    save_target = metadata.get("save_target", "")
    save_authorized = metadata.get("save_authorized", "").lower()

    if mode not in ALLOWED_MODES:
        errors.append("route_mode must be auto or reuse-saved-style")
    if target not in ALLOWED_TARGETS:
        errors.append("target_use must be portable, seo-banner, ig-carousel or ig-single-image")
    if not outputs:
        errors.append("detected_outputs must contain at least one output")
    unknown = outputs - ALLOWED_OUTPUTS
    if unknown:
        errors.append("unknown detected_outputs: " + ", ".join(sorted(unknown)))
    if save_target not in ALLOWED_SAVE_TARGETS:
        errors.append("save_target must be none, style, tone or skill")
    if save_authorized not in {"true", "false"}:
        errors.append("save_authorized must be true or false")
    if save_authorized == "false" and save_target != "none":
        errors.append("save_target must remain none before an explicit save command")
    if save_authorized == "true" and save_target == "none":
        errors.append("an authorized save requires one explicit save_target")
    if save_target in ALLOWED_OUTPUTS and save_target not in outputs:
        errors.append("save_target must be one of the detected candidate outputs")

    for heading in ("Student request", "Sources received", "Why these outputs", "Save boundary"):
        if not re.search(rf"^#+\s+{re.escape(heading)}\s*$", text, re.MULTILINE):
            errors.append(f"missing heading: {heading}")

    if args.check_outputs and route.is_file():
        experiment = route.parent
        for output in sorted(outputs & ALLOWED_OUTPUTS):
            if not has_candidate(experiment, output):
                errors.append(f"missing candidate output for detected layer: {output}")

    print(json.dumps({
        "ok": not errors,
        "route_mode": mode,
        "target_use": target,
        "detected_outputs": sorted(outputs),
        "save_target": save_target,
        "save_authorized": save_authorized == "true",
        "errors": errors,
    }, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
