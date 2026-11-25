---
type: social_media_evidence_manifest
source_id: SRC-YYYYMMDD-topic
source_ref: https://example.com/or-local-reference
captured: YYYY-MM-DD
access_state: FULL
media_kind: carousel
caption_state: full
expected_media_count: 10
captured_media_count: 10
content_scope: social-post-research-only
---

# Media Evidence Manifest

`access_state`: `FULL | PARTIAL | IMAGE_ONLY | BLOCKED`
`media_kind`: `carousel | reel | image-post | video-post | screenshot-set | local-video | text-only`
`caption_state`: `full | partial | unavailable`；`full` 包括已直接確認來源沒有 Caption，`unavailable` 代表未能可靠取得
`expected_media_count`: 使用平台顯示嘅數量；無法確定時填 `unknown`。

## Capture receipt

- Retrieval environment:
- Source observed directly:
- Caption read:
- Media completion:
- Actual video played: yes / no / not applicable
- Missing / blocked:
- Why this access_state is accurate:

## Local media receipt (when applicable)

- Requested source URL / ID:
- Actual source URL / ID (flag any substitute):
- Acquisition method / tool version:
- Acquisition status: NOT_ATTEMPTED / DOWNLOADED_UNVERIFIED / VERIFIED_LOCAL / FAILED / BLOCKED
- Attempt results / exact blocker:
- Local file / bytes / SHA-256:
- Duration / resolution / video and audio codecs:
- Full decode verification / receipt file:
- Identity check (title, ID, duration, representative frames):
- Intended use: local research / internal review / other specified use
- Publication or presentation reuse clearance: confirmed / not confirmed / not applicable

For download-only work, use the JSON receipt from `scripts/verify_video.py`; a full research manifest is unnecessary. Successful acquisition does not change `access_state` to FULL automatically.

## Assets

| Index | Type | File | Capture method | OCR / visible text | Visual evidence | Limitation |
| --- | --- | --- | --- | --- | --- | --- |
| 01 | slide | `relative/path` | browser screenshot | `observed text` | layout / proof / CTA | none |

Text-only 或 `BLOCKED` 而沒有可保存 media 時，可用 `not applicable` 代替 asset rows；其他 media kind 必須逐項列出。

## Contact sheet

- File:
- Included assets:

## Evidence boundary

- Safe observed claims:
- Claims requiring attribution:
- Claims that must not be made:
- Time-sensitive information:
