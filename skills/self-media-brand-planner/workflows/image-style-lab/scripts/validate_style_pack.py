#!/usr/bin/env python3
"""Validate a portable Image Style Lab pack before Human Review or Vault save."""

from __future__ import annotations

import argparse
import json
import re
import sys
from PIL import Image, UnidentifiedImageError
from pathlib import Path
from reference_assets import reference_images, pack_version, required_files, reference_document


REQUIRED_FILES = ("PREFERENCE.md", "REFERENCE.md", "STYLE.md", "DESIGN.md", "scorecard.md")
COMPACT_REQUIRED_HEADINGS = {
    "STYLE.md": (
        "風格核心",
        "設計方法與變奏",
        "品牌適配",
        "使用界線",
        "參考圖片與觀察",
        "確認與測試",
    ),
    "DESIGN.md": (
        "Canvas and framing",
        "Recognition path",
        "Reading order",
        "Typography geometry",
        "Subject slot",
        "Palette roles",
        "Material and effects",
        "Density and safe areas",
        "Creative Envelope — LOCK",
        "Creative Envelope — FLEX",
        "Creative Envelope — BAN",
        "Brand asset and Logo lock",
        "Variant matrix",
        "Prompt block",
        "QA targets",
    ),
}
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
    if (experiment / "STYLE.md").is_file():
        if style_id and experiment.name != style_id:
            raise ValueError("requested style_id does not match direct pack")
        return experiment
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
        version = pack_version(style_folder)
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, ensure_ascii=False, indent=2))
        raise SystemExit(1)

    texts: dict[str, str] = {}
    compact = version == 2
    for name in required_files(style_folder):
        path = style_folder / name
        if path.is_symlink():
            errors.append(f"required file must not be a symlink: {path}")
            continue
        if not path.is_file():
            errors.append(f"missing required file: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        for heading in (COMPACT_REQUIRED_HEADINGS[name] if compact else REQUIRED_HEADINGS[name]):
            if not has_heading(text, heading):
                errors.append(f"{name}: missing heading '{heading}'")
        # Reject empty sections; a word-count threshold is not a quality test.
        sections = re.split(r"(?m)^#{2,} +(.+)\n", text)
        for index in range(1, len(sections), 2):
            body = sections[index + 1].strip() if index + 1 < len(sections) else ""
            if not body or body.casefold() in {"tbc", "todo", "—", "-"}:
                errors.append(f"{name}: empty section '{sections[index]}'")

    design_text = texts.get("DESIGN.md", "")
    for alternatives in (() if compact else DESIGN_HEADING_ALTERNATIVES):
        if not any(has_heading(design_text, heading) for heading in alternatives):
            errors.append("DESIGN.md: missing one of headings " + " / ".join(repr(item) for item in alternatives))

    reference_name = reference_document(style_folder)
    reference_text = texts.get(reference_name, "")
    reference_meta = frontmatter(reference_text)
    declared_asset_root = Path(reference_meta.get("reference_asset_root", ""))
    if declared_asset_root != CANONICAL_REFERENCE_ASSET_ROOT:
        errors.append(
            f"{reference_name}: reference_asset_root must be assets/reference-images"
        )
    stored_images = []
    try:
        stored_images = reference_images(style_folder)
    except (OSError, ValueError, ImportError) as exc:
        errors.append(f"{reference_name}: {exc}")

    style_text = texts.get("STYLE.md", "")
    style_meta = frontmatter(style_text)
    design_meta = frontmatter(design_text)
    if compact:
        if style_meta.get("rights_status", "").casefold() in {"", "tbc", "todo"}:
            errors.append("STYLE.md: rights_status must state the permitted scope or explicit uncertainty")
        tone = style_folder / "TONE.md"
        if style_meta.get("tone_requested") == "true" or tone.exists() or tone.is_symlink():
            if style_meta.get("tone_requested") != "true":
                errors.append("TONE.md: optional writing voice requires tone_requested: true")
            if tone.is_symlink() or not tone.is_file():
                errors.append("TONE.md: requested Tone must be a regular local file")
            elif not tone.read_text(encoding="utf-8").strip():
                errors.append("TONE.md: requested Tone must not be empty")
    style_id = style_meta.get("style_id", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", style_id):
        errors.append("STYLE.md: style_id must be a non-placeholder lowercase kebab-case ID")
    if style_id and style_folder.name != style_id:
        errors.append(f"style folder '{style_folder.name}' does not match style_id '{style_id}'")
    identity_contract = style_meta.get("style_identity_contract", "")
    if identity_contract:
        if identity_contract != "immutable-v1":
            errors.append("STYLE.md: unsupported style_identity_contract")
        revision = style_meta.get("style_revision", "")
        if not re.fullmatch(r"[1-9][0-9]*", revision):
            errors.append("STYLE.md: immutable-v1 needs a positive integer style_revision")
        if re.search(r"-v[0-9]+$", style_id):
            errors.append("STYLE.md: immutable-v1 style_id must not carry a revision suffix")
        basis = style_meta.get("identity_basis", "")
        if basis.casefold() in {"", "tbc", "todo", "unknown", "none"}:
            errors.append("STYLE.md: immutable-v1 needs a non-empty identity_basis")
        predecessor = style_meta.get("predecessor_style_id", "")
        if predecessor == style_id:
            errors.append("STYLE.md: predecessor_style_id cannot equal style_id")
        elif predecessor not in {"none", ""} and not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", predecessor):
            errors.append("STYLE.md: predecessor_style_id must be none or a lowercase kebab-case ID")
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

    # Candidate saves stay lightweight; formal brand claims require explicit data.
    brand_state = style_meta.get("brand_state", "reference-only")
    if "brand_state" not in style_meta:
        warnings.append("Legacy pack has no brand_state; treated as reference-only")
    if brand_state not in {"reference-only", "brand-adapted", "brand-approved"}:
        errors.append("STYLE.md: invalid brand_state")
    if brand_state in {"brand-adapted", "brand-approved"}:
        for field in ("brand_id", "brand_source"):
            if design_meta.get(field, "").casefold() in {"", "unassigned", "tbc", "unknown", "none"}:
                errors.append(f"DESIGN.md: {field} required for {brand_state}")
        try:
            palette = json.loads(design_meta.get("brand_palette", "{}"))
            if not isinstance(palette, dict):
                raise ValueError("brand_palette must be an object")
            if not {"primary", "background", "text"}.issubset(palette):
                raise ValueError("brand_palette requires primary, background and text roles")
            if not all(isinstance(v, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", v) for v in palette.values()):
                raise ValueError("brand_palette roles require six-digit HEX values")
        except (ValueError, TypeError) as exc:
            errors.append(f"DESIGN.md: {exc}")
    if brand_state == "brand-approved":
        review = design_meta.get("brand_review", "unreviewed")
        review_path = Path(review.split("#", 1)[0])
        if (review in {"unreviewed", "TBC", ""} or review_path.is_absolute()
                or ".." in review_path.parts or (style_folder / review_path).is_symlink()
                or not (style_folder / review_path).is_file()):
            errors.append("DESIGN.md: brand-approved needs a local brand_review evidence link")
        elif compact:
            if review != "STYLE.md#確認與測試" or not has_heading(style_text, "確認與測試"):
                errors.append("STYLE.md: compact brand_review must point to STYLE.md#確認與測試")
    combined = style_text + "\n" + design_text
    if re.search(r"(?:^|[\s`])(?:/Users/|[A-Za-z]:\\\\)", combined):
        errors.append("STYLE.md/DESIGN.md: private absolute path leakage")
    # Source names can be recorded as evidence, not inherited as design instructions.
    grammar = re.split(r"(?m)^## 參考圖片與觀察\s*$", combined)[0] if compact else combined
    if re.search(r"\bC\d{2}\b|card-c\d+|source\s*:@|@[A-Za-z0-9_]{2,}", grammar, re.IGNORECASE):
        errors.append("STYLE.md/DESIGN.md: campaign card or source-handle leakage")
    if re.search(r"\[TODO|TODO:", combined, re.IGNORECASE):
        errors.append("STYLE.md/DESIGN.md: unresolved placeholder")
    for term in args.forbid_term:
        if term and term.casefold() in grammar.casefold():
            errors.append(f"STYLE.md/DESIGN.md: forbidden Content Job term found: {term}")

    if style_meta.get("status") in {"selected", "user-selected"}:
        tested = style_meta.get("tested_jobs", "")
        if tested in ("", "[]"):
            warnings.append("User selection is not visual QA; no tested_jobs evidence recorded")
    elif style_meta.get("status") not in {"candidate", "starter-template", "draft"}:
        warnings.append("STYLE.md: status should normally be draft, candidate, starter-template or selected")

    payload = {
        "ok": not errors,
        "pack_version": version,
        "experiment": str(experiment),
        "style_folder": str(style_folder),
        "style_id": style_id or None,
        "style_revision": style_meta.get("style_revision") or None,
        "design_id": style_design_id or None,
        "platform_scope": style_platform_scope or None,
        "reference_image_count": len(stored_images),
        "brand_state": brand_state,
        "errors": errors,
        "warnings": warnings,
        "note": "Structure, image and metadata checks only; not proof of brand correctness, user approval or visual quality.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
