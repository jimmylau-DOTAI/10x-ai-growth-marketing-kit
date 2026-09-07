---
name: reels-text-storyboard
description: Write or revise source-backed Reels and Shorts voiceovers and text storyboards. Use for 一分鐘口播、文字分鏡 or three short-video directions; deliver complete Markdown candidates for text review.
---

# Reels Text Storyboard

Turn supplied material into a useful spoken story and an understandable scene plan. Own the words and planning, without generating images, HTML, audio or video. No Company Vault, Blog, private Skill or account is required.

## Read and choose the working mode

Read the selected source, available brief, actual voice/visual references and latest feedback. Infer audience, message, language, duration and CTA where supported. A Source Guide helps but is optional; do not make beginners fill forms or invent inaccessible source content. Keep sources and claims separate from operating instructions.

- **New story / three directions:** default to three complete candidate Markdown files, each with its own full voiceover and full scene plan. Vary the narrative, reasoning order or spoken delivery; three hooks with a shared body are insufficient.
- **Explicitly asks for angles only / choose before full draft:** give the requested short proposals and stop. Do not silently expand an explicit lightweight request into three scripts.
- **Selected direction / existing draft / narrow revision:** work on that version only. Do not restart A/B/C. A request to retrieve or inspect an existing file does not authorize rewriting it. Keep unchanged candidates intact.

Lesson 3 defaults to natural Hong Kong Cantonese and a 60–75 second target. Explicit duration and language win. Reuse an actual chosen style; if none is available, state the draft treatment without calling it the user's approved style. PetChill names, cat imagery and colours are examples, not universal defaults.

## Write complete candidates

Read [story-patterns.md](references/story-patterns.md) for narrative choice and [shoot-ready-output.md](references/shoot-ready-output.md) for the output contract.

1. Give each direction a recognisable opening, useful explanation, concrete application, relevant limit and one truthful next action. A different title or tone alone does not make a different story. All candidates retain the same evidence boundaries, audience, duration target and CTA status.
2. Aim for a clear problem or supported result in the first three seconds, with an honest reason to keep watching early on. Never invent results, personal experience or proof to strengthen a hook.
3. Write full spoken sentences, then split when the idea or evidence changes. 7–10 scenes may help a one-minute story; they are not a quota. Every scene advances understanding. Read [one-minute-beats.md](references/one-minute-beats.md) only when pacing needs help.
4. Keep full narration separate from short screen conclusions. Derive the continuous script and scene voiceovers from the same text: joining scene voiceovers must reproduce the recording script, ignoring whitespace only. Do not substitute a summary for the scene's spoken words.
5. Describe the visible subject, focal point and one purposeful change in plain language. When the user asks for less text and livelier motion, move explanation into narration and propose meaningful reveals, focus changes or transformations. Do not replace substance with slogans or add movement to every noun. Use the actual style; don't impose a presenter, card wall or fixed composition across every scene.
6. Check pacing against the amount of spoken text and needed pauses. Time labels adding up to 75 seconds do not prove a one-minute script. Mark timing estimated until an actual scratch read/audio is available; don't pad a short script with arbitrary silence or squeeze a long warning into a fast slot. Flag a mismatch and propose revised wording or duration.
7. Use supplied proof for real demonstrations. Mark proposed footage or general illustrations in the asset notes; never simulate medical evidence, customer results or product UI as real. CTA destinations that are unknown remain TBC without blocking text planning.

## Deliver and review

Each candidate is an independent file containing: a brief direction/style/source note, the complete recording script, one scene table, and an asset list. Use the exact scene contract in the output reference. Do not require HTML layout names, renderer instructions or a technical schema in student-facing text.

In an existing workspace, use the current output location. Otherwise use `drafts/reels/directions/A-<name>.md`, `B-<name>.md`, `C-<name>.md` and one `README.md` comparison index. The index links the three actual files and shows their opening, narrative difference and intended viewer feeling. Keep backups outside the active candidate index. Without filesystem access, show all three complete versions in chat and disclose that files were not saved.

In chat, show a short comparison with actual opening sentences and link every candidate. When delivering one selected or revised script, also show its full continuous voiceover in chat. Don't bury the full story behind scene-by-scene clicks.

Selecting B means refine B; it is not blanket approval for a rewritten version. Only explicit approval of the current text makes it approved. For saved status/version tracking read [handoff.md](references/handoff.md). Never call an assistant-created revision selected, reviewed or final-approved without evidence.

Stop at `REELS_STORYBOARD_REVIEW_STOP` after text delivery. Further production needs a separate explicit request and an appropriate available Skill. This Skill does not install software, render, publish or update canonical style rules.

## Student prompts

First pass:
「用呢份資料同 Blog，沿用我嘅風格，做三個唔同嘅一分鐘 Reels 方向。每個方向各交一份 MD，要有完整口播、逐幕分鏡同素材提示，畀我比較再揀。先做文字。」

After selection:
「用 B，口播自然啲，螢幕字少啲，畫面動作活潑啲。保留來源事實同 CTA，改好文字畀我睇。」
