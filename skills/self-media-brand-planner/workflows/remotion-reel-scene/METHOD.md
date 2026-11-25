---
name: remotion-reel-scene
description: Set up Remotion and build one approved 9:16 Reels scene for local Studio preview. Use only after the HTML storyboard is approved; it does not render, export, publish, or create a full multi-scene video.
---

# Remotion Reels Scene

Use this package-local Skill after a `reels-html-storyboard` has been approved. It sets up a local Remotion project and makes **one 5–8 second 9:16 scene** previewable in Remotion Studio. It is not a video exporter and not a replacement for the approved storyboard.

## Preconditions

Read the approved `drafts/reels/storyboard.html` and `review-receipt.md`. Confirm the selected scene, its visible caption, timing, assets and claim boundary. If these are not approved, return to `reels-html-storyboard`.

## Setup and build

1. Check `node --version` and `npm --version`. If either is missing, report the actual blocker.
2. Explain that the following creates a local project and downloads dependencies. Run it only when the user asks to install or start Remotion:

```bash
npx create-video@latest --yes --blank --no-tailwind reel-remotion
cd reel-remotion
npm install
```

3. In the created `reel-remotion/` folder, implement only the chosen scene as a `9:16` composition. Use the approved captions, timing, Style and real assets; leave a visible placeholder for assets that are still missing.
4. Start local preview with `npx remotion studio --no-open`. If file watching fails, retry once with `--webpack-poll 1000`.
5. Review the scene in Studio: phone safe area, caption readability, first-frame hook, timing, source/claim boundary and missing assets.

## Simple user prompt

```text
我已確認 Reels HTML 分鏡稿的 Scene 01。請先檢查 Node 和 npm；我確認後才安裝 Remotion。
在本 Project 建立 reel-remotion，按已確認的 Scene 01 做一段 5–8 秒、9:16 的本地 Studio 預覽。不要 render、export 或發布。
```

## Boundaries

- “做一段 frame” 在呢個工作流程指一個可預覽的短 Scene，不是完成影片。
- Do not rewrite the hook, captions, claims, CTA or Style decision.
- Do not render a video file unless the user separately asks. Studio preview is evidence of local setup, not delivery or publication.
- Do not install arbitrary packages beyond the standard Remotion starter without user approval.

## Completion report

Return Node/npm status, project path, composition id, chosen scene, target frame size, Studio URL/status, review result, missing assets and `LOCAL_PREVIEW_REVIEW_REQUIRED`.
