#!/usr/bin/env python3
"""Validate a portable Image Style Lab pack before Human Review or Vault save."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FILES = ("PREFERENCE.md", "REFERENCE.md", "STYLE.md", "DESIGN.md", "scorecard.md")
CANONICAL_REFERENCE_ASSET_ROOT = Path("assets/reference-images")
IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}
REQUIRED_HEADINGS = {
    "PREFERENCE.md": (
        "User-stated preference",
        "Plain-language conclusion",
        "CONFIRMED_BY_USER",
        "OBSERVED_ACROSS_SET",
        "INFERRED_LIKING",
        "TREATMENT_VARIATIONS",
        "PROOF_MODALITY_PREFERENCE",
        "VISIBLE_ATTRIBUTION_PREFERENCE",
        "NOT_THE_PREFERENCE",
        "UNCERTAIN",
        "Human Review",
    ),
    "REFERENCE.md": (
        "Source inventory",
        "Visual reference board",
        "User-stated set intent",
        "Mechanism matrix",
        "Evidence modality ledger",
        "Identity subtraction boundary",
        "Visible attribution boundary",
        "OBSERVED",
        "INFERRED",
        "UNCERTAIN",
        "Source exclusions",
    ),
    "STYLE.md": (
        "One-line definition",
        "What the user likes",
        "Recognition test",
        "Core grammar",
        "Subject role",
        "Headline and proof relationship",
        "Proof modality and authenticity",
        "Attribution boundary",
        "Fixed rules",
        "Adjustable parameters",
        "Treatment presets",
        "Breaks the Style",
        "Evidence and confidence",
    ),
    "DESIGN.md": (
        "Canvas and framing",
        "Reading order",
        "Typography geometry",
        "Subject slot",
        "Proof-object slot",
        "Proof asset contract",
        "Attribution and provenance",
        "Palette roles",
        "Treatment preset table",
        "Material and effects",
        "Density and safe areas",
        "Content input fields",
        "Identity substitution rules",
        "Brand asset and Logo lock",
        "Prompt block",
        "QA targets",
    ),
    "scorecard.md": ("Hard gates", "Score", "Verdict", "Required next test"),
}

DESIGN_HEADING_ALTERNATIVES = (
    ("Recognition path", "Normalized layout zones"),
    ("Creative Envelope — LOCK", "Fixed rules"),
    ("Creative Envelope — FLEX", "Adjustable parameters"),
    ("Creative Envelope — BAN", "Negative block"),
    ("Variant opportunities", "Variant matrix"),
)


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


def has_heading(text: str, heading: str) -> bool:
    return bool(re.search(rf"^#+\s+{re.escape(heading)}\s*$", text, re.MULTILINE | re.IGNORECASE))


def find_style_folder(experiment: Path, style_id: str | None) -> Path:
    styles = experiment / "styles"
    if style_id:
        target = styles / style_id
        if not target.is_dir():
            raise ValueError(f"style folder not found: {target}")
        return target
    candidates = sorted(path for path in styles.iterdir() if path.is_dir()) if styles.is_dir() else []
    if len(candidates) != 1:
        raise ValueError(f"expected exactly one style folder; found {len(candidates)}")
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("--style-id")
    parser.add_argument("--forbid-term", action="append", default=[])
    args = parser.parse_args()

    experiment = args.experiment.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    try:
        style_folder = find_style_folder(experiment, args.style_id)
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    texts: dict[str, str] = {}
    for name in REQUIRED_FILES:
        path = style_folder / name
        if not path.is_file():
            errors.append(f"missing required file: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        for heading in REQUIRED_HEADINGS[name]:
            if not has_heading(text, heading):
                errors.append(f"{name}: missing heading '{heading}'")

    design_text = texts.get("DESIGN.md", "")
    for alternatives in DESIGN_HEADING_ALTERNATIVES:
        if not any(has_heading(design_text, heading) for heading in alternatives):
            errors.append("DESIGN.md: missing one of headings " + " / ".join(repr(item) for item in alternatives))

    reference_text = texts.get("REFERENCE.md", "")
    reference_meta = frontmatter(reference_text)
    declared_asset_root = Path(reference_meta.get("reference_asset_root", ""))
    if declared_asset_root != CANONICAL_REFERENCE_ASSET_ROOT:
        errors.append(
            "REFERENCE.md: reference_asset_root must be assets/reference-images"
        )
    asset_root = style_folder / CANONICAL_REFERENCE_ASSET_ROOT
    image_paths = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", reference_text)
    if not image_paths:
        errors.append("REFERENCE.md: visual reference board must embed at least one local image")
    referenced_images: set[Path] = set()
    for raw_path in image_paths:
        relative = Path(raw_path.strip().split()[0].strip("<>"))
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"REFERENCE.md: unsafe visual reference path: {raw_path}")
            continue
        if relative.suffix.lower() not in IMAGE_SUFFIXES:
            errors.append(f"REFERENCE.md: unsupported reference image type: {relative}")
        try:
            relative.relative_to(CANONICAL_REFERENCE_ASSET_ROOT)
        except ValueError:
            errors.append(
                f"REFERENCE.md: image must live under the declared reference asset root: {relative}"
            )
            continue
        target = style_folder / relative
        if not target.is_file():
            errors.append(f"REFERENCE.md: missing visual reference image: {relative}")
        elif target.is_symlink():
            errors.append(f"REFERENCE.md: reference image must not be a symlink: {relative}")
        referenced_images.add(relative)

    stored_images = {
        path.relative_to(style_folder)
        for path in asset_root.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    } if asset_root.is_dir() else set()
    if not stored_images:
        errors.append("REFERENCE.md: reference asset root contains no local images")
    if len(stored_images) > 6:
        errors.append("REFERENCE.md: portable Style pack may contain at most 6 reference images")
    for relative in sorted(stored_images - referenced_images):
        errors.append(f"REFERENCE.md: stored reference image is not embedded: {relative}")

    style_text = texts.get("STYLE.md", "")
    style_meta = frontmatter(style_text)
    design_meta = frontmatter(design_text)
    style_id = style_meta.get("style_id", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", style_id):
        errors.append("STYLE.md: style_id must be a non-placeholder lowercase kebab-case ID")
    if style_id and style_folder.name != style_id:
        errors.append(f"style folder '{style_folder.name}' does not match style_id '{style_id}'")
    if style_meta.get("identity_agnostic", "").lower() != "true":
        errors.append("STYLE.md: identity_agnostic must be true")
    proof_modality = style_meta.get("proof_modality", "")
    if proof_modality in {"", "TBC", "TODO"}:
        errors.append("STYLE.md: proof_modality must be explicit")
    proof_authenticity = style_meta.get("proof_authenticity", "")
    if proof_authenticity not in {
        "authentic-required",
        "authentic-preferred",
        "generated-allowed",
        "adaptive",
    }:
        errors.append("STYLE.md: proof_authenticity must use an allowed evidence policy")
    visible_attribution = style_meta.get("visible_attribution_default", "")
    if visible_attribution not in {"required", "optional", "forbidden", "job-controlled"}:
        errors.append("STYLE.md: visible_attribution_default must be required, optional, forbidden or job-controlled")
    if design_meta.get("style_id") != style_id:
        errors.append("DESIGN.md: style_id must match STYLE.md")
    style_design_id = style_meta.get("design_id", "")
    design_design_id = design_meta.get("design_id", "")
    if style_design_id != design_design_id:
        errors.append("STYLE.md/DESIGN.md: design_id must match")
    if style_design_id != "unassigned" and not re.fullmatch(
        r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*-[0-9]{3}", style_design_id
    ):
        errors.append(
            "STYLE.md/DESIGN.md: design_id must be unassigned or a namespaced ID ending in three digits"
        )
    style_platform_scope = style_meta.get("platform_scope", "")
    design_platform_scope = design_meta.get("platform_scope", "")
    if style_platform_scope != design_platform_scope:
        errors.append("STYLE.md/DESIGN.md: platform_scope must match")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", style_platform_scope):
        errors.append("STYLE.md/DESIGN.md: platform_scope must be lowercase kebab-case")
    if style_design_id != "unassigned" and style_platform_scope == "portable":
        errors.append(
            "STYLE.md/DESIGN.md: an assigned Design ID requires a destination platform_scope"
        )
    if design_meta.get("proof_asset_policy", "") in {"", "TBC", "TODO"}:
        errors.append("DESIGN.md: proof_asset_policy must be explicit")
    if design_meta.get("visible_attribution") != visible_attribution:
        errors.append("DESIGN.md: visible_attribution must match STYLE.md visible_attribution_default")

    combined = style_text + "\n" + design_text
    if re.search(r"(?:^|[\s`])(?:/Users/|[A-Za-z]:\\\\)", combined):
        errors.append("STYLE.md/DESIGN.md: private absolute path leakage")
    if re.search(r"\bC\d{2}\b|card-c\d+|source\s*:@|@[A-Za-z0-9_]{2,}", combined, re.IGNORECASE):
        errors.append("STYLE.md/DESIGN.md: campaign card or source-handle leakage")
    if re.search(r"\bTBC\b|\[TODO|TODO:", combined, re.IGNORECASE):
        errors.append("STYLE.md/DESIGN.md: unresolved placeholder")
    for term in args.forbid_term:
        if term and term.casefold() in combined.casefold():
            errors.append(f"STYLE.md/DESIGN.md: forbidden Content Job term found: {term}")

    if style_meta.get("status") == "selected":
        tested = style_meta.get("tested_jobs", "")
        if tested in ("", "[]"):
            errors.append("STYLE.md: selected status requires recorded tested_jobs")
    elif style_meta.get("status") not in {"candidate", "starter-template", "draft"}:
        warnings.append("STYLE.md: status should normally be draft, candidate, starter-template or selected")

    payload = {
        "ok": not errors,
        "experiment": str(experiment),
        "style_folder": str(style_folder),
        "style_id": style_id or None,
        "design_id": style_design_id or None,
        "platform_scope": style_platform_scope or None,
        "reference_image_count": len(stored_images),
        "errors": errors,
        "warnings": warnings,
        "note": "Structural validation only; Human Review and cross-job visual proof remain required.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
