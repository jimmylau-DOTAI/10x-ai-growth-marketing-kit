# Design and Interaction Dependencies

## Required Skills

任何會改變頁面 presentation 或 frontend behaviour 嘅 Build／Revision，都要讀完整及實際使用：

1. `design-taste-frontend` — source: [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)；
2. `emil-design-eng` — source: [emilkowalski/skills](https://github.com/emilkowalski/skills)。

兩個 Skills 需要另行安裝，本 Repository 不複製其內容。如果執行環境無法找到或完整讀取其中一個，停止在 `DEPENDENCY_BLOCKED`。不要憑記憶、摘要或一般 UI knowledge 偽裝成已使用。

## Design Taste output

Build 前最少記錄：

- one-line Design Read；
- mode: `greenfield / redesign-preserve / redesign-overhaul`；
- `DESIGN_VARIANCE`、`MOTION_INTENSITY`、`VISUAL_DENSITY`（1–10）及原因；
- chosen system／honestly labelled aesthetic family；
- reference mapping：adapt、reject、reason；
- mobile collapse rule for each multi-column section；
- supplied／real asset plan。

Build 後跑完整 pre-flight。Contextual rule 可以標示 not applicable，但要有原因；mandatory failure 要修正。

## Emil Design Engineering output

每個 material interaction 記錄：

| Element | Frequency | Purpose | Decision | Timing／easing | Reduced-motion behaviour |
| --- | --- | --- | --- | --- | --- |
|  |  | hierarchy / explanation / feedback / state change |  |  |  |

`Looks cool` 不是 purpose。Static page 亦要決定哪些內容不應動畫，並 audit：

- exact transition properties；不要 `transition: all`；
- pressable controls 有 active state；
- hover 只在 hover-capable pointer；
- UI entry 不用 `ease-in`；
- UI timing 通常低於 300ms；
- animation 優先使用 transform／opacity；
- visible focus、validation 同 loading／success／error states；
- reduced-motion behaviour；
- repeated action 不被動畫拖慢。

Revision 建立 `DESIGN-ENGINEERING-REVIEW.md`：

| Before | After | Why |
| --- | --- | --- |
|  |  |  |

## When not to rerun

Endpoint、CRM、tracking、email、reminder 或 deployment read-back 如果完全不改 rendered page，記錄 `design_change: false`，保留最近有效 receipt。Design review 不能代替 backend evidence。

## Evidence boundary

Named dependency、written receipt 或 validator pass 只證明已記錄指定 decision／files。仍然要在真實 rendered page 做 Desktop／Mobile visual、interaction、accessibility、console、asset 同 overflow QA。
