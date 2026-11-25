# Image QA Contract

## Per Image

- Actual file exists and opens.
- Actual dimensions match the current approved request.
- One complete frame, not a mockup, collage, or background plate.
- Card job and approved message remain obvious.
- The first-glance message, visual hierarchy, Style qualities, and any user-requested correction are visible in the actual image. Matching a previous position or proportion alone is not a pass.
- Visible wording is checked character by character.
- No invented quote, metric, product UI, partnership, or result.
- No fake or approximate official logo.
- No clipped subject, accidental watermark, malformed anatomy, or unintended extra text.
- Retry count is 0 or 1 and any retry names the hard blocker.

## Carousel Set

- Ordered filenames map one-to-one to approved card IDs.
- Card count matches the approved plan.
- C01 approval is recorded before C02 onward.
- Visual continuity is recognisable without identical layouts.
- Contact sheet and individual files agree.
- CTA wording and keyword match the approved plan exactly.

## Status

- `CONTENT_APPROVAL_REQUIRED`: complete content is not approved.
- `C01_REVIEW_REQUIRED`: only the pilot exists and awaits review.
- `C01_APPROVED`: remaining card generation may begin.
- `FINAL_DRAFT_READY`: all local images pass the declared QA; nothing is published.
- `DETERMINISTIC_FINISH_RECOMMENDED`: exact text or identity cannot be guaranteed natively.
- `BLOCKED`: a required asset, approval, or generation capability is unavailable.
