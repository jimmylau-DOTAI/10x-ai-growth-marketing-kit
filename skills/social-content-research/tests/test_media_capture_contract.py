#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_sl_packet.py"
SOURCE_ID = "SRC-20260831-media-example"
SOURCE_REF = "https://example.com/social-post"


def source_text(
    access_state: str,
    media_kind: str,
    caption_state: str,
    limitations: str = "No performance data is proven by the post.",
    source_ref: str = SOURCE_REF,
) -> str:
    return f"""---
type: social_source_record
status: captured
source_id: {SOURCE_ID}
source_ref: {source_ref}
source_type: post
captured: 2026-08-31
access_state: {access_state}
media_kind: {media_kind}
caption_state: {caption_state}
retrieval_method: original-page
content_scope: social-post-research-only
origin_id: example-media-post
---

## Access receipt

The original source was inspected within the stated access boundary.

## Evidence inventory

Observed evidence is recorded in the paired manifest when available.

## Limitations

{limitations}

## SL route

SL-20260831-media-example.md
"""


def sl_text(
    access_state: str,
    media_kind: str,
    caption_state: str,
    source_ref: str = SOURCE_REF,
    extra: str = "",
) -> str:
    return f"""---
type: social_source_learning
status: queued-for-insight-review
source_id: {SOURCE_ID}
source_ref: {source_ref}
created: 2026-08-31
access_state: {access_state}
media_kind: {media_kind}
caption_state: {caption_state}
knowledge_status: source-learning-not-approved-insight
content_scope: social-post-research-only
candidate_count: 0
review_status: queued
---

## 30 秒理解

Summary bounded by captured evidence.

## Coverage

Coverage and missing media are stated.

## 完整攻略

Observed evidence remains separate from interpretation.

## Candidate Insight cards

No independent candidate in this fixture.

## Evidence boundary

Do not claim performance results.

{extra}
"""


def manifest_text(
    access_state: str,
    media_kind: str,
    caption_state: str,
    expected_count: int | str,
    asset_types: list[str],
    missing: str = "none",
    source_ref: str = SOURCE_REF,
    contact_file: str = "contact-sheet.png",
) -> str:
    rows = "\n".join(
        f"| {index:02d} | {asset_type} | `asset-{index:02d}.png` | browser screenshot | "
        f"Observed text {index} | Visual evidence {index} | none |"
        for index, asset_type in enumerate(asset_types, start=1)
    )
    assets = rows or "not applicable"
    return f"""---
type: social_media_evidence_manifest
source_id: {SOURCE_ID}
source_ref: {source_ref}
captured: 2026-08-31
access_state: {access_state}
media_kind: {media_kind}
caption_state: {caption_state}
expected_media_count: {expected_count}
captured_media_count: {len(asset_types)}
content_scope: social-post-research-only
---

## Capture receipt

- Retrieval environment: authenticated local browser where permitted
- Source observed directly: yes
- Caption read: {caption_state}
- Media completion: captured {len(asset_types)} of {expected_count}
- Actual video played: yes
- Missing / blocked: {missing}
- Why this access_state is accurate: based on actual inspected media

## Assets

| Index | Type | File | Capture method | OCR / visible text | Visual evidence | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
{assets}

## Contact sheet

- File: {contact_file}
- Included assets: all captured assets

## Evidence boundary

- Safe observed claims: visible content only
- Claims requiring attribution: creator claims
- Claims that must not be made: performance impact
- Time-sensitive information: none
"""


def run_validator(source: str, sl: str, manifest: str | None) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        source_path = root / "source.md"
        sl_path = root / "sl.md"
        source_path.write_text(source, encoding="utf-8")
        sl_path.write_text(sl, encoding="utf-8")
        command = [
            sys.executable,
            str(VALIDATOR),
            "--source",
            str(source_path),
            "--sl",
            str(sl_path),
        ]
        if manifest is not None:
            manifest_path = root / "manifest.md"
            manifest_path.write_text(manifest, encoding="utf-8")
            command.extend(["--media-manifest", str(manifest_path)])
        return subprocess.run(command, capture_output=True, text=True, check=False)


class MediaCaptureContractTests(unittest.TestCase):
    def test_valid_full_carousel_passes(self) -> None:
        result = run_validator(
            source_text("FULL", "carousel", "full"),
            sl_text("FULL", "carousel", "full"),
            manifest_text("FULL", "carousel", "full", 4, ["slide"] * 4),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_full_carousel_with_missing_slide_fails(self) -> None:
        result = run_validator(
            source_text("FULL", "carousel", "full"),
            sl_text("FULL", "carousel", "full"),
            manifest_text("FULL", "carousel", "full", 4, ["slide"] * 3),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FULL carousel captured fewer assets", result.stderr)

    def test_full_social_post_with_unavailable_caption_fails(self) -> None:
        result = run_validator(
            source_text("FULL", "carousel", "unavailable"),
            sl_text("FULL", "carousel", "unavailable"),
            manifest_text(
                "FULL",
                "carousel",
                "unavailable",
                1,
                ["slide"],
                contact_file="not applicable",
            ),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot have an unavailable caption", result.stderr)

    def test_partial_carousel_with_specific_limitation_passes(self) -> None:
        result = run_validator(
            source_text("PARTIAL", "carousel", "partial", "Slide 4 was blocked by a platform error."),
            sl_text("PARTIAL", "carousel", "partial"),
            manifest_text(
                "PARTIAL",
                "carousel",
                "partial",
                4,
                ["slide"] * 3,
                "Slide 4 was blocked by a platform error.",
            ),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_full_reel_without_frame_or_video_evidence_fails(self) -> None:
        result = run_validator(
            source_text("FULL", "reel", "full"),
            sl_text("FULL", "reel", "full"),
            manifest_text("FULL", "reel", "full", 1, ["cover"], contact_file="not applicable"),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires actual frame or video evidence", result.stderr)

    def test_valid_image_only_source_passes_without_caption_analysis(self) -> None:
        limitation = "Caption was unavailable; only the supplied image could be inspected."
        result = run_validator(
            source_text("IMAGE_ONLY", "image-post", "unavailable", limitation),
            sl_text("IMAGE_ONLY", "image-post", "unavailable"),
            manifest_text(
                "IMAGE_ONLY",
                "image-post",
                "unavailable",
                1,
                ["image"],
                limitation,
                contact_file="not applicable",
            ),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_manifest_source_url_mismatch_fails(self) -> None:
        result = run_validator(
            source_text("FULL", "carousel", "full"),
            sl_text("FULL", "carousel", "full"),
            manifest_text(
                "FULL",
                "carousel",
                "full",
                2,
                ["slide"] * 2,
                source_ref="https://example.com/different-post",
            ),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("source_ref does not match", result.stderr)

    def test_blocked_source_without_manifest_needs_and_accepts_specific_reason(self) -> None:
        reason = "Instagram login wall blocked the original post and all media."
        result = run_validator(
            source_text("BLOCKED", "carousel", "unavailable", reason),
            sl_text("BLOCKED", "carousel", "unavailable"),
            None,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_blocked_source_without_specific_reason_fails(self) -> None:
        result = run_validator(
            source_text("BLOCKED", "carousel", "unavailable", "Unknown."),
            sl_text("BLOCKED", "carousel", "unavailable"),
            None,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("requires a specific block reason", result.stderr)

    def test_visual_source_without_manifest_fails(self) -> None:
        result = run_validator(
            source_text("FULL", "carousel", "full"),
            sl_text("FULL", "carousel", "full"),
            None,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("media manifest is required", result.stderr)

    def test_unavailable_caption_cannot_claim_caption_analysis(self) -> None:
        limitation = "Caption was unavailable; only the supplied image could be inspected."
        result = run_validator(
            source_text("IMAGE_ONLY", "image-post", "unavailable", limitation),
            sl_text("IMAGE_ONLY", "image-post", "unavailable", extra="## Caption analysis\n\nComplete."),
            manifest_text(
                "IMAGE_ONLY",
                "image-post",
                "unavailable",
                1,
                ["image"],
                limitation,
                contact_file="not applicable",
            ),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot claim caption analysis", result.stderr)


if __name__ == "__main__":
    unittest.main()
