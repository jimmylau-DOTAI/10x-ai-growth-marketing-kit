#!/usr/bin/env python3
"""Validate one social Source Receipt, matching SL note, and optional media manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ACCESS_STATES = {"FULL", "PARTIAL", "IMAGE_ONLY", "BLOCKED"}
MEDIA_KINDS = {
    "carousel",
    "reel",
    "image-post",
    "video-post",
    "screenshot-set",
    "local-video",
    "text-only",
}
VISUAL_MEDIA_KINDS = MEDIA_KINDS - {"text-only"}
VIDEO_MEDIA_KINDS = {"reel", "video-post", "local-video"}
CAPTION_STATES = {"full", "partial", "unavailable"}


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"\A---\s*\n(.*?)\n---(?:\n|\Z)", text, re.DOTALL)
    if not match:
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        item = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if item:
            values[item.group(1)] = item.group(2).strip("'\"")
    return values


def require_keys(meta: dict[str, str], keys: list[str], label: str, errors: list[str]) -> None:
    for key in keys:
        if not meta.get(key):
            errors.append(f"{label}: missing frontmatter key '{key}'")


def require_headings(text: str, headings: list[str], label: str, errors: list[str]) -> None:
    for heading in headings:
        if not re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE):
            errors.append(f"{label}: missing section '## {heading}'")


def section_text(text: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def field_value(text: str, label: str) -> str:
    match = re.search(
        rf"^\s*-\s*{re.escape(label)}\s*:\s*(.*?)\s*$",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).strip() if match else ""


def meaningful_note(value: str) -> bool:
    normalized = value.strip().strip("`*_-. ").lower()
    return bool(normalized) and normalized not in {
        "none",
        "no",
        "n/a",
        "na",
        "not applicable",
        "unknown",
        "無",
        "不適用",
    }


def has_specific_block_reason(text: str) -> bool:
    if not meaningful_note(text):
        return False
    return bool(
        re.search(
            r"login|permission|private|paywall|region|platform|technical|captcha|"
            r"rate.?limit|blocked|unavailable|cannot|could not|無法|登入|權限|私密|"
            r"地區|付費|平台|技術|封鎖|未能存取",
            text,
            re.IGNORECASE,
        )
    )


def asset_rows(manifest_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in section_text(manifest_text, "Assets").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0].lower() == "index" or re.fullmatch(r"[-: ]+", cells[0]):
            continue
        rows.append({"index": cells[0], "type": cells[1].lower(), "file": cells[2]})
    return rows


def integer_value(value: str, label: str, errors: list[str]) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        errors.append(f"manifest: {label} must be an integer")
        return None
    if parsed < 0:
        errors.append(f"manifest: {label} must not be negative")
        return None
    return parsed


def validate_media_manifest(
    manifest_text: str,
    source_meta: dict[str, str],
    sl_meta: dict[str, str],
    sl_text: str,
    errors: list[str],
) -> None:
    manifest_meta = frontmatter(manifest_text)
    require_keys(
        manifest_meta,
        [
            "type",
            "source_id",
            "source_ref",
            "captured",
            "access_state",
            "media_kind",
            "caption_state",
            "captured_media_count",
            "content_scope",
        ],
        "manifest",
        errors,
    )
    require_headings(
        manifest_text,
        ["Capture receipt", "Assets", "Contact sheet", "Evidence boundary"],
        "manifest",
        errors,
    )

    if manifest_meta.get("type") != "social_media_evidence_manifest":
        errors.append("manifest: type must be social_media_evidence_manifest")
    for key in ("source_id", "source_ref"):
        if manifest_meta.get(key) != source_meta.get(key) or manifest_meta.get(key) != sl_meta.get(key):
            errors.append(f"manifest: {key} does not match Source Receipt and SL")
    if manifest_meta.get("content_scope") != "social-post-research-only":
        errors.append("manifest: content_scope must be social-post-research-only")

    access_state = manifest_meta.get("access_state")
    media_kind = manifest_meta.get("media_kind")
    caption_state = manifest_meta.get("caption_state")
    if access_state not in ACCESS_STATES:
        errors.append("manifest: invalid access_state")
    if media_kind not in MEDIA_KINDS:
        errors.append("manifest: invalid media_kind")
    if caption_state not in CAPTION_STATES:
        errors.append("manifest: invalid caption_state")
    if access_state != source_meta.get("access_state") or access_state != sl_meta.get("access_state"):
        errors.append("manifest: access_state does not match Source Receipt and SL")
    if media_kind != source_meta.get("media_kind") or media_kind != sl_meta.get("media_kind"):
        errors.append("manifest: media_kind does not match Source Receipt and SL")
    if caption_state != source_meta.get("caption_state") or caption_state != sl_meta.get("caption_state"):
        errors.append("manifest: caption_state does not match Source Receipt and SL")

    captured_count = integer_value(
        manifest_meta.get("captured_media_count", ""),
        "captured_media_count",
        errors,
    )
    expected_raw = manifest_meta.get("expected_media_count", "unknown")
    expected_count: int | None = None
    if expected_raw != "unknown":
        expected_count = integer_value(expected_raw, "expected_media_count", errors)

    rows = asset_rows(manifest_text)
    assets_section = section_text(manifest_text, "Assets").lower()
    explicit_not_applicable = "not applicable" in assets_section or "不適用" in assets_section
    if media_kind in VISUAL_MEDIA_KINDS and access_state != "BLOCKED" and not rows:
        errors.append("manifest: visual/video source requires an assets table with evidence rows")
    if not rows and not explicit_not_applicable and media_kind in {"text-only"} | VISUAL_MEDIA_KINDS:
        errors.append("manifest: Assets must contain evidence rows or explicit not applicable")
    if explicit_not_applicable and media_kind not in {"text-only"} and access_state != "BLOCKED":
        errors.append("manifest: not applicable Assets is allowed only for text-only or BLOCKED sources")
    if captured_count is not None and rows and captured_count != len(rows):
        errors.append(
            f"manifest: captured_media_count says {captured_count}, found {len(rows)} asset rows"
        )

    if access_state == "FULL" and media_kind == "carousel" and expected_count is not None:
        if captured_count is not None and captured_count < expected_count:
            errors.append("manifest: FULL carousel captured fewer assets than expected")
    if (
        access_state == "FULL"
        and media_kind in {"carousel", "reel", "image-post", "video-post"}
        and caption_state == "unavailable"
    ):
        errors.append("manifest: FULL social post cannot have an unavailable caption")
    if access_state == "FULL" and media_kind in VIDEO_MEDIA_KINDS:
        if not any(row["type"] in {"frame", "video"} for row in rows):
            errors.append("manifest: FULL video/reel requires actual frame or video evidence")
        actual_video_played = field_value(
            section_text(manifest_text, "Capture receipt"),
            "Actual video played",
        ).lower()
        if actual_video_played not in {"yes", "true", "verified"}:
            errors.append("manifest: FULL video/reel requires verified actual playback")

    caption_analysis_claimed = bool(
        re.search(r"^##\s+Caption(?:\s+analysis|\s+分析|\s+拆解)?\s*$", sl_text, re.MULTILINE | re.IGNORECASE)
        or sl_meta.get("caption_analysis", "").lower() in {"yes", "true", "performed", "complete"}
    )
    if caption_state == "unavailable" and caption_analysis_claimed:
        errors.append("sl: cannot claim caption analysis when caption_state is unavailable")

    missing_note = field_value(section_text(manifest_text, "Capture receipt"), "Missing / blocked")
    if access_state in {"PARTIAL", "IMAGE_ONLY", "BLOCKED"} and not meaningful_note(missing_note):
        errors.append(f"manifest: {access_state} requires a meaningful Missing / blocked note")

    if captured_count is not None and captured_count >= 2:
        contact_file = field_value(section_text(manifest_text, "Contact sheet"), "File")
        limitation_explains_absence = bool(
            re.search(
                r"contact.?sheet|attachment|channel|tool|接觸表|總覽圖|附件|渠道|工具",
                missing_note,
                re.IGNORECASE,
            )
        )
        if not meaningful_note(contact_file) and not limitation_explains_absence:
            errors.append("manifest: multiple assets require a contact sheet or a specific limitation")


def validate(source_path: Path, sl_path: Path, media_manifest_path: Path | None = None) -> list[str]:
    errors: list[str] = []
    try:
        source_text = source_path.read_text(encoding="utf-8")
        sl_text = sl_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"read error: {exc}"]

    source_meta = frontmatter(source_text)
    sl_meta = frontmatter(sl_text)

    require_keys(
        source_meta,
        [
            "type",
            "status",
            "source_id",
            "source_ref",
            "source_type",
            "captured",
            "access_state",
            "media_kind",
            "caption_state",
            "retrieval_method",
            "content_scope",
            "origin_id",
        ],
        "source",
        errors,
    )
    require_keys(
        sl_meta,
        [
            "type",
            "status",
            "source_id",
            "source_ref",
            "created",
            "access_state",
            "media_kind",
            "caption_state",
            "knowledge_status",
            "content_scope",
            "candidate_count",
            "review_status",
        ],
        "sl",
        errors,
    )

    if source_meta.get("type") != "social_source_record":
        errors.append("source: type must be social_source_record")
    if sl_meta.get("type") != "social_source_learning":
        errors.append("sl: type must be social_source_learning")
    if source_meta.get("source_id") != sl_meta.get("source_id"):
        errors.append("source_id does not match")
    if source_meta.get("source_ref") != sl_meta.get("source_ref"):
        errors.append("source_ref does not match")
    if source_meta.get("content_scope") != "social-post-research-only":
        errors.append("source: content_scope must be social-post-research-only")
    if sl_meta.get("content_scope") != "social-post-research-only":
        errors.append("sl: content_scope must be social-post-research-only")
    if sl_meta.get("knowledge_status") != "source-learning-not-approved-insight":
        errors.append("sl: knowledge_status must remain source-learning-not-approved-insight")
    if sl_meta.get("status") != "queued-for-insight-review":
        errors.append("sl: status must be queued-for-insight-review")
    if source_meta.get("access_state") not in ACCESS_STATES:
        errors.append("source: invalid access_state")
    if sl_meta.get("access_state") not in ACCESS_STATES:
        errors.append("sl: invalid access_state")
    if source_meta.get("access_state") != sl_meta.get("access_state"):
        errors.append("access_state does not match")
    if source_meta.get("media_kind") not in MEDIA_KINDS:
        errors.append("source: invalid media_kind")
    if sl_meta.get("media_kind") not in MEDIA_KINDS:
        errors.append("sl: invalid media_kind")
    if source_meta.get("media_kind") != sl_meta.get("media_kind"):
        errors.append("media_kind does not match")
    if source_meta.get("caption_state") not in CAPTION_STATES:
        errors.append("source: invalid caption_state")
    if sl_meta.get("caption_state") not in CAPTION_STATES:
        errors.append("sl: invalid caption_state")
    if source_meta.get("caption_state") != sl_meta.get("caption_state"):
        errors.append("caption_state does not match")

    require_headings(
        source_text,
        ["Access receipt", "Evidence inventory", "Limitations", "SL route"],
        "source",
        errors,
    )
    require_headings(
        sl_text,
        ["30 秒理解", "Coverage", "完整攻略", "Candidate Insight cards", "Evidence boundary"],
        "sl",
        errors,
    )

    candidates = re.findall(r"^####\s+Candidate\s+\d+\s*$", sl_text, re.MULTILINE)
    try:
        declared_count = int(sl_meta.get("candidate_count", ""))
    except ValueError:
        declared_count = -1
        errors.append("sl: candidate_count must be an integer")
    if declared_count != len(candidates):
        errors.append(
            f"sl: candidate_count says {declared_count}, found {len(candidates)} Candidate headings"
        )

    blocks = re.split(r"^####\s+Candidate\s+\d+\s*$", sl_text, flags=re.MULTILINE)[1:]
    required_card_fields = [
        "candidate_key:",
        "一句見解",
        "來源證據",
        "邊界",
        "Post relevance",
    ]
    for index, block in enumerate(blocks, start=1):
        for field in required_card_fields:
            if field not in block:
                errors.append(f"sl: Candidate {index} missing '{field}'")

    access_state = source_meta.get("access_state")
    media_kind = source_meta.get("media_kind")
    if media_kind in VISUAL_MEDIA_KINDS and access_state != "BLOCKED" and media_manifest_path is None:
        errors.append("media manifest is required for a non-BLOCKED visual/video Deep SL")
    if access_state == "BLOCKED" and media_manifest_path is None:
        if not has_specific_block_reason(section_text(source_text, "Limitations")):
            errors.append("source: BLOCKED without manifest requires a specific block reason")

    if media_manifest_path is not None:
        try:
            manifest_text = media_manifest_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"manifest read error: {exc}")
        else:
            validate_media_manifest(manifest_text, source_meta, sl_meta, sl_text, errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--sl", required=True, type=Path)
    parser.add_argument("--media-manifest", type=Path)
    args = parser.parse_args()

    errors = validate(args.source, args.sl, args.media_manifest)
    if errors:
        print("SL_PACKET_FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "status": "SL_PACKET_PASS",
                "source": str(args.source),
                "sl": str(args.sl),
                "media_manifest": str(args.media_manifest) if args.media_manifest else None,
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
