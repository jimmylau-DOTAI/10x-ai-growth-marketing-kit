#!/usr/bin/env python3
"""Validate a reviewed platform route before any managed-Vault registration."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_FIELDS = (
    "style_id",
    "route_status",
    "platform",
    "format",
    "source_design_id",
    "design_id_namespace",
    "proposed_design_id",
    "style_index",
    "style_destination",
    "reference_destination",
    "registration_authorized",
)
REQUIRED_FILES = ("REFERENCE.md", "STYLE.md", "DESIGN.md")
PLACEHOLDERS = {"", "TBC", "TODO", "unassigned"}


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
            result[key.strip()] = value.strip().strip('"\'')
    return result


def read_style_meta(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    return frontmatter(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("route", type=Path)
    args = parser.parse_args()

    experiment = args.experiment.expanduser().resolve()
    route = args.route.expanduser().resolve()
    errors: list[str] = []

    if not experiment.is_dir():
        errors.append(f"experiment not found: {experiment}")
    if not route.is_file():
        errors.append(f"route receipt not found: {route}")
        text = ""
        meta: dict[str, str] = {}
    else:
        text = route.read_text(encoding="utf-8")
        meta = frontmatter(text)

    for field in REQUIRED_FIELDS:
        if field not in meta or meta.get(field, "") in PLACEHOLDERS:
            errors.append(f"PLATFORM-ROUTE.md: missing resolved field '{field}'")

    style_id = meta.get("style_id", "")
    namespace = meta.get("design_id_namespace", "")
    proposed = meta.get("proposed_design_id", "")
    source_design_id = meta.get("source_design_id", "")
    if style_id and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", style_id):
        errors.append("PLATFORM-ROUTE.md: style_id must be lowercase kebab-case")
    if namespace and not re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*", namespace):
        errors.append("PLATFORM-ROUTE.md: invalid design_id_namespace")
    if namespace and proposed and not re.fullmatch(rf"{re.escape(namespace)}-[0-9]{{3}}", proposed):
        errors.append("PLATFORM-ROUTE.md: proposed_design_id does not match its namespace")
    if source_design_id not in {"", "none"} and source_design_id == proposed:
        errors.append("PLATFORM-ROUTE.md: cross-platform adaptation must not reuse source_design_id")

    route_status = meta.get("route_status", "")
    authorized = meta.get("registration_authorized", "").lower()
    if route_status not in {"PLATFORM_ROUTE_REVIEW_STOP", "PLATFORM_ROUTE_APPROVED"}:
        errors.append("PLATFORM-ROUTE.md: unsupported route_status")
    if route_status == "PLATFORM_ROUTE_REVIEW_STOP" and authorized != "false":
        errors.append("PLATFORM-ROUTE.md: review-stop route cannot authorize registration")
    if route_status == "PLATFORM_ROUTE_APPROVED" and authorized != "true":
        errors.append("PLATFORM-ROUTE.md: approved route must record registration_authorized: true")

    style_index = Path(meta.get("style_index", "")).expanduser()
    style_destination = Path(meta.get("style_destination", "")).expanduser()
    reference_destination = Path(meta.get("reference_destination", "")).expanduser()
    if style_index and not style_index.is_file():
        errors.append("PLATFORM-ROUTE.md: style_index must resolve to an existing selector")
    if style_index.is_file() and style_destination.parent.resolve() != style_index.parent.resolve():
        errors.append(
            "PLATFORM-ROUTE.md: style_destination must be inside the resolved Style index directory"
        )
    if style_destination.exists():
        errors.append("PLATFORM-ROUTE.md: style_destination already exists; duplicate-check failed")
    if reference_destination and not reference_destination.parent.is_dir():
        errors.append(
            "PLATFORM-ROUTE.md: reference_destination parent must already exist"
        )
    if proposed and style_id and style_destination.name != f"{proposed}-{style_id}":
        errors.append(
            "PLATFORM-ROUTE.md: style_destination must end with <Design ID>-<style-id>"
        )
    if style_destination and reference_destination:
        if style_destination == reference_destination:
            errors.append(
                "PLATFORM-ROUTE.md: reference_destination must be a distinct reference image location"
            )
        reference_hint = reference_destination.as_posix().casefold()
        if not any(token in reference_hint for token in ("reference", "visual-assets")):
            errors.append(
                "PLATFORM-ROUTE.md: reference_destination must identify a reference or visual-assets location"
            )

    style_folder = route.parent
    style_meta = read_style_meta(style_folder / "STYLE.md")
    design_meta = read_style_meta(style_folder / "DESIGN.md")
    if style_meta.get("style_id") != style_id or design_meta.get("style_id") != style_id:
        errors.append("PLATFORM-ROUTE.md: style_id must match STYLE.md and DESIGN.md")
    if style_meta.get("design_id") != proposed or design_meta.get("design_id") != proposed:
        errors.append("PLATFORM-ROUTE.md: proposed_design_id must match STYLE.md and DESIGN.md")
    expected_scope = "-".join(
        part for part in (meta.get("platform", ""), meta.get("format", "")) if part
    )
    if (
        style_meta.get("platform_scope") != expected_scope
        or design_meta.get("platform_scope") != expected_scope
    ):
        errors.append(
            "PLATFORM-ROUTE.md: platform and format must match STYLE.md and DESIGN.md platform_scope"
        )

    for name in REQUIRED_FILES:
        if f"`{name}`" not in text:
            errors.append(f"PLATFORM-ROUTE.md: Files to register must include {name}")

    payload = {
        "ok": not errors,
        "experiment": str(experiment),
        "route": str(route),
        "style_id": style_id or None,
        "proposed_design_id": proposed or None,
        "style_destination": meta.get("style_destination") or None,
        "reference_destination": meta.get("reference_destination") or None,
        "errors": errors,
        "note": (
            "Route validation is a dry-run contract check; it does not register, publish, "
            "or write to a Vault."
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
