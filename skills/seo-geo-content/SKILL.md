---
name: seo-geo-content
description: Use when a user wants to turn supplied source material into an original SEO/GEO blog, improve an article for search and AI answer engines, or create a local HTML review with Company Brain, CTA, link, claim, image, and Human Review controls.
---

# SEO + GEO Blog Writing

## Outcome

將用戶提供嘅 Source 轉成原創、有搜尋價值、容易理解同引用嘅 SEO／GEO Blog。成品要回答真實搜尋問題，加入有理由嘅公司觀點，並保留 Company Brain、CTA、連結、圖片、Claim 及 Human Review 邊界。

預設流程：`Source Guide → Title → Article → Local HTML → Human Review`。

## Start here

先判斷目前階段，只完成該階段。不要因為用戶提供咗 Source，就跳過攻略及標題確認直接寫文章。

| Current state | Read now | Deliver | Stop status |
| --- | --- | --- | --- |
| New raw Source | [workflow-and-review-gates.md](references/workflow-and-review-gates.md) | Source Guide | `SOURCE_GUIDE_REVIEW_STOP` |
| Approved Source Guide | 上述 workflow + [seo-geo-framework.md](references/seo-geo-framework.md) | Search angle and titles | `SEO_TITLE_REVIEW_STOP` |
| Approved Guide and title | 上述兩份 + [writing-style-and-platform-rules.md](references/writing-style-and-platform-rules.md) + output templates | Article production pack | `BLOG_REVIEW_STOP` |
| Completed article draft | [content-quality-check.md](references/content-quality-check.md) | QA result and open items | 保持 `BLOG_REVIEW_STOP` |
| Approved article with HTML request | Workflow + writing-style reference 嘅 Local HTML section | Local generic HTML | `HTML_REVIEW_STOP` |

只讀目前階段需要嘅檔案。[article-brief.md](assets/article-brief.md) 用於整理 approved brief；[article-output.md](assets/article-output.md) 用於組裝文章 production pack。

## Intake

用自然語言取得：

- Source：URL、文字、筆記、PDF 或圖片；
- Audience、地區、語言及主要搜尋問題；
- 公司／品牌、Current Offer、CTA 及可用連結；
- 文章用途、期望格式及目前已批准階段。

資料不足但不影響目前階段時，使用 `TBC`、`LINK_TBC`、`CTA_TBC` 或 `SOURCE_NEEDED`。缺少會改變文章方向、事實邊界或 CTA 嘅資料時，先交目前可以確認嘅部分及列出 blocker，不要用假資料填空。

## Core working rules

- Public copy 必須係原創 synthesis；不可貼上、翻譯、輕度改寫、模仿 Source 結構，或將外部方法重新命名成公司原創。
- 除非法律、合規或用戶明確要求，公開文章不可出現 Source 名稱、URL、citation、研究筆記或「參考咗某篇文章」等來源痕跡。
- Provenance 必須保留在內部 Source Guide、Claim Notes、Link Ledger 或 Review Receipt，不能因公開文章 source-blind 而刪走。
- 不可虛構公司能力、案例、價格、成果、第一手經歷、圖片授權、連結、日期、數字或法規。
- 不可保證排名、AI citation、traffic 或 conversion。
- 「OK」、「繼續」或修改意見只批准當前可見階段，不代表 Google Doc、CMS、publish、deploy、send 或其他外部動作已獲批准。

## Phase 1: Source Guide

先理解資料，暫時不要寫 Blog、品牌觀點或 CTA。Source Guide 最少包括：

- Reader problem；
- Verified facts and scope；
- Useful examples or mechanisms；
- Limits, risks and unknowns；
- Search opportunities；
- Internal provenance and Claim status。

Claim 使用 `VERIFIED`、`PROVIDED`、`INFERENCE` 或 `SOURCE_NEEDED`。如果只讀到摘要、截圖或部分內容，標示 `PARTIAL` 或 `BLOCKED`，不可當成完整 Source。

交付攻略後停在 `SOURCE_GUIDE_REVIEW_STOP`，等用戶修正或批准。

## Phase 2: Search angle and title

只有 approved Source Guide 先可以進入此階段。先確定：

- Primary Query、Search Intent、Audience、Location and Content Type；
- 讀者想理解、完成、比較、評估或購買嘅工作；
- 核心直接答案、文章獨特觀點及暫定 CTA。

產出十個真正不同嘅標題方向，而唔係十個近義改寫；推薦 Top 3，說明 search phrase、reader promise 及 overpromise／jargon risk。年份、數字、`最新`、`完整`、`實測` 或結果承諾，只可在內容能完全兌現時使用。

停在 `SEO_TITLE_REVIEW_STOP`，未選定標題前不要起稿。

## Phase 3: Article production

### Company Brain gate

文章涉及公司、服務或 CTA 時，先讀 Project 提供嘅：

1. Company profile／定位與受眾；
2. Current Offer／產品或服務；
3. 相關 Claim evidence；
4. CTA direct destination。

公司名不等於 Company Brain。資料不足時不可自行加入品牌權威、能力承諾或硬銷 CTA；角色扮演品牌在內部標示 `SYNTHETIC_BRAND`。

### Build the answer

- H1 及開首先直接回答 Primary Query，再補背景；不要先講公司或研究過程。
- 每個 H2 回答一個主要讀者問題；H3 用於步驟、功能、比較、限制或情境。
- 重要問題先用一至三句直接答案，再提供準則、步驟、例子、限制及下一步。
- 清楚寫出 Entity、日期、地區、適用範圍及 Fact／Judgment／Recommendation 邊界。
- FAQ 只回答正文已有足夠支持嘅真實問題；Schema 建議必須對應可見內容。
- 不要為 SEO 堆砌關鍵字、重複摘要、空泛小標題或無用途連結。

### Write with an owned point of view

預設使用實務營運者語氣：書面繁體中文配合自然香港用語，先講讀者熟悉嘅工作阻力，再解釋術語。將技術翻譯成 input、output、time、cost、risk、approval 及 next step。

每個主要段落應推進新資料或判斷。長文建立 3–5 個有用嘅 Owned Answer Units：

`verified fact／definition → company or author judgment with reason → work translation → visible deliverable → limitation or human boundary`

公司名稱只用於真實擁有嘅判斷、方法、證據、限制或下一步。重複品牌名不會增加權威；第一身實測只有在真實 artifact 或 receipt 存在時先可使用。

### Complete the production pack

交付內容包括：

- H1、Meta title、Meta description and slug；
- Primary Query、Search Intent and related questions；
- Article body and Owned Answer Unit ledger；
- supported FAQ and Schema recommendation；
- Internal-link plan、Reader Link／CTA Ledger；
- Claim Notes、image manifest、QA Status and Open Items。

Public links 只限已確認嘅第一方 authority／action page、真正相關站內內容或 CTA direct destination。每條連結要有描述性 anchor 及幫助讀者理解或行動；欠缺真實目標時使用 `LINK_TBC`，不可製造 `href`，亦不可將 provenance URL 偽裝成 reader link。

CTA 必須對應已確認 Offer、適合本文讀者及真實目的地；否則使用 `CTA_TBC`。完成初稿後讀完整 QA checklist，修正後停在 `BLOG_REVIEW_STOP`。

## Phase 4: Local HTML review

只有文章已批准，而且用戶明確要求 HTML，先建立本機 generic HTML：

- 使用 UTF-8、`<html lang="zh-Hant">`、單一 H1 及 `<main id="article">`；
- Heading、段落、表格、連結及圖片在手機與桌面均可讀；
- 使用可靠 CJK font fallbacks；
- 不加入 Framer、CMS、tracking、publish 或 deploy 行為。

如用戶要求使用 Source 圖片，先合法取得檔案、保存到 Project asset folder，並放在真正相關段落。Rights 未確認嘅圖片只可標示 `INTERNAL_REVIEW_ONLY`，另記來源、用途及 rights status，不可進入公開 copy／export。

停在 `HTML_REVIEW_STOP`。Google Doc、CMS upload、publish、deploy 或 send 需要用戶在當前對話另行批准指定目標；完成後必須 read back 真實目的地。

## Completion receipt

每個階段最後列出：

- `Current phase`；
- `Status`；
- `Confirmed`；
- `TBC / blocked items`；
- `Next approval needed`。

任何 Review Stop、`READY_FOR_REVIEW` 或本機 HTML 都不等於已發布。
