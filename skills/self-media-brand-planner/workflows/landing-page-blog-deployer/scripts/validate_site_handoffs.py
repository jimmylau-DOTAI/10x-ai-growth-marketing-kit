#!/usr/bin/env python3
"""Validate landing and blog handoff structure without performing external actions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ALLOWED_APPROVALS = {"APPROVED_FOR_ASSEMBLY", "REVIEW_REQUIRED", "BLOCKED"}
REQUIRED_UTM_FIELDS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_content",
    "utm_term",
}
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"top-level JSON must be an object: {path}")
    return data


def require(data: dict[str, Any], fields: list[str], label: str) -> list[str]:
    return [f"{label}: missing {field}" for field in fields if data.get(field) in (None, "")]


def validate_common(data: dict[str, Any], label: str, expected_type: str) -> list[str]:
    errors = require(
        data,
        ["schema_version", "handoff_type", "approval_status", "source_artifact", "open_items"],
        label,
    )
    if data.get("handoff_type") != expected_type:
        errors.append(f"{label}: handoff_type must be {expected_type}")
    if data.get("approval_status") not in ALLOWED_APPROVALS:
        errors.append(f"{label}: invalid approval_status")
    open_items = data.get("open_items")
    if not isinstance(open_items, list):
        errors.append(f"{label}: open_items must be a list")
    elif open_items and data.get("approval_status") == "APPROVED_FOR_ASSEMBLY":
        errors.append(f"{label}: approved handoff cannot contain open_items")
    return errors


def validate_landing(path: Path) -> list[str]:
    data = load_json(path)
    errors = validate_common(data, "landing", "landing-site")
    errors.extend(require(data, ["route", "primary_cta", "form", "tracking", "qa"], "landing"))
    if data.get("route") != "/":
        errors.append("landing: route must be /")
    cta = data.get("primary_cta")
    if isinstance(cta, dict):
        errors.extend(require(cta, ["label", "intent", "target", "status"], "landing.primary_cta"))
    form = data.get("form")
    if isinstance(form, dict):
        errors.extend(require(form, ["anchor", "fields", "consent_status", "success_action", "endpoint_status"], "landing.form"))
    tracking = data.get("tracking")
    if isinstance(tracking, dict):
        actual = tracking.get("utm_fields")
        if not isinstance(actual, list) or set(actual) != REQUIRED_UTM_FIELDS:
            errors.append("landing.tracking: utm_fields must contain all five standard UTM fields")
        if tracking.get("first_touch_required") is not True:
            errors.append("landing.tracking: first_touch_required must be true")
    return errors


def validate_blog(path: Path) -> list[str]:
    data = load_json(path)
    errors = validate_common(data, f"blog[{path.name}]", "blog-publish")
    label = f"blog[{path.name}]"
    errors.extend(
        require(
            data,
            ["slug", "title", "meta_title", "meta_description", "canonical_path", "content_source", "language", "internal_links", "cta", "schema", "image_rights_status"],
            label,
        )
    )
    slug = data.get("slug")
    if isinstance(slug, str) and not SLUG_PATTERN.fullmatch(slug):
        errors.append(f"{label}: slug must be lowercase kebab-case")
    if isinstance(slug, str) and data.get("canonical_path") != f"/blog/{slug}":
        errors.append(f"{label}: canonical_path must equal /blog/{slug}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--landing", required=True, type=Path)
    parser.add_argument("--blog", required=True, action="append", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    try:
        errors.extend(validate_landing(args.landing))
        for blog_path in args.blog:
            errors.extend(validate_blog(blog_path))
    except ValueError as exc:
        errors.append(str(exc))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"HANDOFF_VALIDATION_PASSED landing=1 blogs={len(args.blog)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
