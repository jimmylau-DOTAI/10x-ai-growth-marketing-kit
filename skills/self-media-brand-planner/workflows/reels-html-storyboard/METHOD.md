---
name: reels-html-storyboard
description: Turn a user-approved short-video script into an editable 9:16 HTML storyboard showing timed screen text, visual emphasis and scene transitions. Use for 口播配畫面 or HTML 分鏡 after text review, before video rendering.
---

# Reels HTML Storyboard

Translate approved words into a visible scene plan. Accept text from `reels-text-storyboard` or any equivalent user-approved script. No private Vault, fixed filename, brand or renderer is required.

## Intake

Read the exact approved text, approval evidence, source/asset notes and current task's visual preferences. Follow [the portable handoff](../reels-text-storyboard/references/handoff.md) when the paired Skill is installed; otherwise apply the same minimum contract: exact text/version, actual user approval, HTML request, timing uncertainty, sources and assets. Missing a sidecar file is not a reason to rewrite an approved script.

If text is unapproved, show what needs text review and return to text drafting. If the user already approved this version and requested HTML, proceed; do not ask them to approve filenames or a second identical handoff. Never mark a draft approved yourself.

## Visual direction

Preserve voiceover, scene order, claims, attribution, CTA and language. Keep the approved duration; flag timing that cannot be read naturally. Estimated timing is allowed for a clearly labelled provisional preview and is not verified audio timing.

Use the user's actual brand rules and relevant short-video style. A Carousel reference may inform colour or texture, not dictate a video layout. If no treatment is selected, offer three concise directions when the user wants to choose; otherwise state a reasonable draft treatment and proceed. Do not silently assign a permanent Style or assume one industry has one look.

Read the selected storyboard's composition and layout mode before building. The HTML must preserve the intended base frame: A-roll position, safe text space, B-roll focal detail and the visual change at the cut. Use the paired Skill's `shoot-ready-output.md` when present. A layout is chosen for the sentence: `speaker-side-caption` for a spoken conclusion, `full-frame-proof` for a real detail, `checklist-rail` for ordered action, `before-to-after-switch` for a corrected assumption, and `quiet-end-frame` for the final CTA. Do not make every scene a title over a generic background.

## Build the preview

- Provide separate labelled sections for **完整口播**, **逐幕分鏡**, and **9:16 畫面預覽**, plus the production asset list. Show the full script by default in its own section, with a copy control and optional reader dialog; never require clicking every scene to read the whole story. Reader-dialog opening pauses preview playback, supports Escape, and restores focus on close. Both script views must come from the same approved scene data.
- Preserve the selected spoken style. The scene panel identifies A-roll (main delivery), B-roll (supporting footage) and HTML overlay (graphics above footage or a dedicated explanatory screen). An A-roll/B-roll switch changes the base footage; an overlay is not itself B-roll. Show where narration continues over an insert, how the image relates to it, and which assets are still only proposed.
- In each scene panel, show the chosen layout mode and its short purpose. The preview keeps a real or clearly labelled placeholder base image visible; it adds one primary text group and, only when needed, one short supporting line or marker. Change hierarchy, placement and focal area across scenes according to the storyboard. Do not simulate evidence with fake UI, a card wall or decorative motion.
- Use the storyboard's spoken-word cue and scene-relative time for each overlay: what enters, where, how, how long it remains readable and how it exits. Until actual audio exists, cue timing is provisional. In the review UI display filming directions and AI-generation alternatives outside the viewer-facing video frame.
- Default to text alongside a 9:16 screen, stacked on narrow displays. Keep full voiceover in the text panel and short conclusions inside the frame. Every scene explains one idea through a focused visual action: highlight a relevant area, reveal ordered checks, transform a relationship, or hold a conclusion. Avoid adding motion to every noun.
- Keep scene content and timings in one editable data structure. Selecting a scene or seeking time must reproduce the same state; manual selection clears playback. Include play/pause, replay and a visible time indicator, with an accurate final hold and total timeline.
- Preserve the approved full story; the local animation preview does not generate voiceover audio. Missing footage/Logo/UI must remain labelled placeholders, and explanatory diagrams must not pretend to be real evidence.
- Keep important content away from likely platform overlays, provide a safe-area review toggle, keyboard controls and readable focus states. Reduced-motion retains all content while removing unnecessary movement. Check the intended export/platform layout separately before release.
- Suggested outputs: `drafts/reels/storyboard.html`, `storyboard-manifest.json`, `review-receipt.md` inside this task's output root. Use relative/local assets or self-contained HTML; report any external dependency.

## Verify and deliver

Read back saved text against the approved version. Check every scene, full playback duration, switching scenes during playback, pause/replay, final state, narrow layout and reduced-motion when a browser is available. Report observed visual checks separately from code inspection; a browser blocker is not a visual pass.

The manifest records the upstream text path/hash, approval evidence, selected treatment, scene times, timing status, source/asset gaps and output paths. Return `REELS_HTML_REVIEW_STOP`. Later text changes require reconciliation before using this HTML as a production plan.

The current course can continue with `remotion-reel-scene` after HTML approval and a request to start that stage. Other environments can choose an available renderer later; this Skill does not require one and does not install, render, export or publish.

## user prompt

「文字 OK，用我嘅風格做 HTML 預覽，畀我睇每幕啲字同重點點樣喺畫面出現。」
