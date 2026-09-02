#!/usr/bin/env python3
"""Validate Image Style Lab pilot routing and completion receipts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


VISUAL_INTENTS = {"image-led", "layout-led", "hybrid"}
PILOT_MEDIA = {"image-generation", "deterministic-layout", "hybrid"}
HTML_ROLES = {"none", "layout-reference-only", "final-render"}
FALLBACK_POLICIES = {"stop", "user-approved-layout-fallback"}
PROOF_MODALITIES = {
    "authentic-ui-screenshot",
    "authentic-dashboard-screenshot",
    "authentic-document-capture",
    "authentic-object-photo",
    "faithful-data-render",
    "generated-metaphor",
    "decorative-scene",
    "mixed",
}
PROOF_AUTHENTICITIES = {"authentic-required", "authentic-preferred", "generated-allowed", "not-proof"}
VISIBLE_ATTRIBUTION = {"required", "optional", "forbidden"}
PLACEHOLDERS = {"", "TBC", "TODO", "none"}


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


def placeholder(value: str | None) -> bool:
    return value is None or value.strip() in PLACEHOLDERS


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content_job", type=Path)
    args = parser.parse_args()

    path = args.content_job.expanduser().resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not path.is_file():
        errors.append(f"CONTENT-JOB.md not found: {path}")
        meta: dict[str, str] = {}
    else:
        meta = frontmatter(path.read_text(encoding="utf-8"))
        if not meta:
            errors.append("CONTENT-JOB.md: missing or invalid frontmatter")

    visual_intent = meta.get("visual_intent", "")
    pilot_medium = meta.get("pilot_medium", "")
    html_role = meta.get("html_role", "")
    fallback = meta.get("fallback_policy", "")
    status = meta.get("status", "")
    production_skill = meta.get("production_skill", "")
    proof_modality = meta.get("proof_modality", "")
    proof_authenticity = meta.get("proof_authenticity", "")
    visible_attribution = meta.get("visible_attribution", "")

    if visual_intent not in VISUAL_INTENTS:
        errors.append(f"visual_intent must be one of {sorted(VISUAL_INTENTS)}")
    if pilot_medium not in PILOT_MEDIA:
        errors.append(f"pilot_medium must be one of {sorted(PILOT_MEDIA)}")
    if html_role not in HTML_ROLES:
        errors.append(f"html_role must be one of {sorted(HTML_ROLES)}")
    if fallback not in FALLBACK_POLICIES:
        errors.append(f"fallback_policy must be one of {sorted(FALLBACK_POLICIES)}")
    if placeholder(production_skill):
        errors.append("production_skill must name the actual selected runtime capability")
    if proof_modality not in PROOF_MODALITIES:
        errors.append(f"proof_modality must be one of {sorted(PROOF_MODALITIES)}")
    if proof_authenticity not in PROOF_AUTHENTICITIES:
        errors.append(f"proof_authenticity must be one of {sorted(PROOF_AUTHENTICITIES)}")
    if visible_attribution not in VISIBLE_ATTRIBUTION:
        errors.append(f"visible_attribution must be one of {sorted(VISIBLE_ATTRIBUTION)}")
    if meta.get("internal_provenance") != "required":
        errors.append("internal_provenance must remain required")
    if visible_attribution == "forbidden" and meta.get("visible_source_text", "").strip().lower() not in {"", "none"}:
        errors.append("visible_attribution forbidden requires visible_source_text: none")

    asset_path = meta.get("proof_asset_path", "")
    asset_sha = meta.get("proof_asset_sha256", "")
    proof_asset_ready = not placeholder(asset_path) and bool(re.fullmatch(r"[0-9a-fA-F]{64}", asset_sha))
    if proof_authenticity == "authentic-required":
        if proof_modality in {"generated-metaphor", "decorative-scene"}:
            errors.append("authentic-required proof cannot use generated-metaphor or decorative-scene")
        if status in {"PRODUCTION_HANDOFF_READY", "PILOT_REVIEW_STOP"} and not proof_asset_ready:
            errors.append(f"{status} with authentic-required proof needs proof_asset_path and 64-character proof_asset_sha256")

    try:
        image_model_calls = int(meta.get("image_model_calls", ""))
        if image_model_calls < 0:
            raise ValueError
    except ValueError:
        image_model_calls = -1
        errors.append("image_model_calls must be a non-negative integer")

    if visual_intent in {"image-led", "hybrid"}:
        if pilot_medium not in {"image-generation", "hybrid"}:
            errors.append("image-led/hybrid job requires image-generation or hybrid pilot_medium")
        if html_role == "final-render":
            errors.append("image-led/hybrid job cannot use HTML as final-render")

    if visual_intent == "layout-led" and html_role == "final-render" and pilot_medium != "deterministic-layout":
        errors.append("layout-led HTML final-render requires deterministic-layout pilot_medium")

    if status == "PILOT_REVIEW_STOP":
        if visual_intent in {"image-led", "hybrid"} and image_model_calls < 1:
            errors.append("image-led/hybrid PILOT_REVIEW_STOP requires at least one image-model call")
        if html_role == "layout-reference-only" and pilot_medium == "deterministic-layout":
            errors.append("layout-reference-only HTML cannot be the deterministic pilot output")
        if placeholder(meta.get("output_path")):
            errors.append("PILOT_REVIEW_STOP requires output_path")
        if not re.fullmatch(r"[0-9a-fA-F]{64}", meta.get("output_sha256", "")):
            errors.append("PILOT_REVIEW_STOP requires a 64-character output_sha256")
        for field in ("native_dimensions", "final_dimensions"):
            if not re.fullmatch(r"\d+[x×]\d+", meta.get(field, "")):
                errors.append(f"PILOT_REVIEW_STOP requires {field} as WIDTHxHEIGHT")
        if placeholder(meta.get("postprocess")):
            errors.append("PILOT_REVIEW_STOP requires postprocess receipt")
    elif status not in {"draft", "PRODUCTION_HANDOFF_READY", "BLOCKED_PROOF_ASSET", "BLOCKED_RENDER_CONTRACT"}:
        warnings.append("status is not a standard pilot routing state")

    payload = {
        "ok": not errors,
        "content_job": str(path),
        "status": status or None,
        "visual_intent": visual_intent or None,
        "pilot_medium": pilot_medium or None,
        "production_skill": production_skill or None,
        "html_role": html_role or None,
        "proof_modality": proof_modality or None,
        "proof_authenticity": proof_authenticity or None,
        "proof_asset_ready": proof_asset_ready,
        "visible_attribution": visible_attribution or None,
        "image_model_calls": image_model_calls,
        "errors": errors,
        "warnings": warnings,
        "note": "Routing validation does not replace visual QA or Human Review.",
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
