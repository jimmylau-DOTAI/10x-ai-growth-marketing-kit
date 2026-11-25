---
name: toapis-minimax-h3-video
description: Create or compare named ToAPIs image-to-video animated social posters from a supplied first-frame image. Use only when the user explicitly names MiniMax-H3, seedance-2-mini, or gemini_omni_flash; not for publishing or a multi-scene video edit.
---

# ToAPIs animated-poster models

Use this package-local Skill for an explicitly named animated-poster generation or a user-approved model comparison. The source image is the first frame; do not redesign its copy, branding, or claims. A named model authorizes **one** paid generation for that model, not a retry, variation, or publication. A comparison only authorizes the named models and one like-for-like result per model.

## Before the call

1. Inspect the supplied image and record its actual dimensions. Do not claim that a model preserves its ratio unless its current API contract supports it.
2. Make one concise motion prompt that specifies what stays locked, what moves, camera movement, duration, and sound intent. Keep text, logos, product claims, and UI-like graphics stable unless the user explicitly asks to animate them.
3. Run `scripts/toapis_minimax_h3.sh --dry-run` with the exact input and target settings. Live execution reads `TOAPIS_API_KEY` only from the execution environment without outputting it; dry-run needs no key and makes no API call. Never ask the user to paste a key into chat or store it in the Skill package. The shell helper requires Bash, curl and jq; check these locally before live execution. On Windows use an available compatible shell or stop with the missing dependency; do not silently install one.
4. Check the live model contract before submission:
   - `MiniMax-H3`: 4–15 seconds; `2K` or `768p`; a first frame adapts to the source ratio.
   - `seedance-2-mini`: 4–15 seconds; use the user-selected resolution and `generate_audio:false` for a silent poster.
   - `gemini_omni_flash` / `gemini-omni-flash`: 4, 6, or 10 seconds; `720p`; only `16:9` or `9:16`. A 4:5 source therefore needs an explicit vertical or landscape comparison target.
5. Do not replace a failed model or submit a second request without fresh approval. For a price comparison, take sequential read-only balance snapshots before and after each approved model. Report them as account-level deltas and label attribution `TBC` if other account use could overlap.

## Generate and inspect

Run `scripts/toapis_minimax_h3.sh` once. It uploads the local first frame, submits the asynchronous task, polls the same task, downloads the output, and writes a redacted manifest. If the command times out, retain its task ID and rerun only with `--resume-task`; never resubmit.

After download, inspect the actual video and the first/middle/last frames. Check that it opens, the source composition and required text remain legible, requested subject motion appears, and no clear anatomy or severe text-warping defect dominates. This is local QA only: a downloaded video is not approved for publishing.

## Deliver

Return the output path, actual duration/dimensions, model, task ID, manifest path, and a concise visual limitation. State `LOCAL_QA_PASSED_REVIEW_REQUIRED` only after the inspection passes; otherwise return `LOCAL_QA_REVIEW_REQUIRED` and do not spend a retry.
