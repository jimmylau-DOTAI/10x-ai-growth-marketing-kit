#!/usr/bin/env python3
"""Validate portable design-dependency and rendered-QA evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_SKILLS = ("design-taste-frontend", "emil-design-eng")


def required_text(container: dict, key: str, errors: list[str], prefix: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip() or value.strip().upper() == "TBC":
        errors.append(f"{prefix}.{key} must be a non-TBC string")
        return ""
    return value.strip()


def resolve_existing(receipt_dir: Path, raw_path: str, errors: list[str], label: str) -> None:
    if not raw_path:
        return
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        path = receipt_dir / path
    if not path.exists():
        errors.append(f"{label} does not exist: {path}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_design_skill_receipt.py /absolute/path/to/design-skill-receipt.json")
        return 2

    receipt_path = Path(sys.argv[1]).expanduser().resolve()
    if not receipt_path.is_file():
        print(f"FAIL: receipt not found: {receipt_path}")
        return 1

    try:
        data = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read valid JSON: {exc}")
        return 1

    errors: list[str] = []
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if data.get("primary_skill") != "sales-funnel-landing-page-builder":
        errors.append("primary_skill must be sales-funnel-landing-page-builder")
    if data.get("mode") not in {"standard", "rapid-prototype", "revision"}:
        errors.append("mode must be standard, rapid-prototype or revision")
    required_text(data, "artifact_status", errors, "receipt")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, dict):
        errors.append("dependencies must be an object")
        dependencies = {}

    for name in REQUIRED_SKILLS:
        record = dependencies.get(name)
        if not isinstance(record, dict):
            errors.append(f"missing dependency record: {name}")
            continue
        if record.get("status") != "applied":
            errors.append(f"{name}.status must be applied")
        if record.get("skill_name") != name:
            errors.append(f"{name}.skill_name must be {name}")

    taste = dependencies.get("design-taste-frontend", {})
    if isinstance(taste, dict):
        required_text(taste, "design_read", errors, "design-taste-frontend")
        if taste.get("redesign_mode") not in {"greenfield", "redesign-preserve", "redesign-overhaul"}:
            errors.append("design-taste-frontend.redesign_mode is invalid")
        dials = taste.get("dials")
        if not isinstance(dials, dict):
            errors.append("design-taste-frontend.dials must be an object")
        else:
            for key in ("design_variance", "motion_intensity", "visual_density"):
                value = dials.get(key)
                if not isinstance(value, int) or not 1 <= value <= 10:
                    errors.append(f"design-taste-frontend.dials.{key} must be an integer from 1 to 10")
        if taste.get("preflight_status") != "pass":
            errors.append("design-taste-frontend.preflight_status must be pass")
        evidence = required_text(taste, "evidence_file", errors, "design-taste-frontend")
        resolve_existing(receipt_path.parent, evidence, errors, "design-taste-frontend.evidence_file")

    emil = dependencies.get("emil-design-eng", {})
    if isinstance(emil, dict):
        count = emil.get("motion_decision_count")
        if not isinstance(count, int) or count < 1:
            errors.append("emil-design-eng.motion_decision_count must be at least 1")
        if emil.get("interaction_qa_status") != "pass":
            errors.append("emil-design-eng.interaction_qa_status must be pass")
        review = required_text(emil, "review_file", errors, "emil-design-eng")
        resolve_existing(receipt_path.parent, review, errors, "emil-design-eng.review_file")

    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        errors.append("artifacts must be an object")
    else:
        for key in ("page", "copy", "qa_receipt", "desktop_evidence", "mobile_evidence"):
            raw_path = required_text(artifacts, key, errors, "artifacts")
            resolve_existing(receipt_path.parent, raw_path, errors, f"artifacts.{key}")

    qa = data.get("qa")
    if not isinstance(qa, dict):
        errors.append("qa must be an object")
    else:
        if qa.get("rendered_status") != "pass":
            errors.append("qa.rendered_status must be pass")
        for key in ("horizontal_overflow_desktop", "horizontal_overflow_mobile", "console_errors", "broken_assets"):
            if qa.get(key) != 0:
                errors.append(f"qa.{key} must be 0")
        if qa.get("cta_consistent") is not True:
            errors.append("qa.cta_consistent must be true")
        if qa.get("reduced_motion_checked") is not True:
            errors.append("qa.reduced_motion_checked must be true")

    boundaries = data.get("boundaries")
    if not isinstance(boundaries, dict):
        errors.append("boundaries must be an object")
    else:
        for key in ("deployed", "form_connected", "crm_connected", "payment_connected"):
            if not isinstance(boundaries.get(key), bool):
                errors.append(f"boundaries.{key} must be boolean")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: mandatory design dependencies and QA evidence are complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
