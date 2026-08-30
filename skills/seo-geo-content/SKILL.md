---
name: seo-geo-content
description: Use when a user wants to turn supplied source material into a high-quality SEO/GEO blog, improve an article for search and AI answer engines, or create a local HTML review with Company Brain, CTA, link, claim, image, and Human Review controls.
---

# SEO + GEO Blog Writing

## Overview

將用戶提供嘅 Source 轉成有搜尋價值、容易理解同引用、但唔會在公開文章暴露研究來源嘅 SEO／GEO Blog。預設流程係：

`Source Guide → Title → Article → Local HTML → Human Review`

每次只完成目前階段。未獲用戶批准，不會自動跳去下一階段；亦不會建立 Google Doc、上載 CMS 或發布。

## Public-output boundary

- 公開文章不得出現來源作者、媒體、網站、URL、引用清單、研究過程或「參考某文章」等字眼，除非法律、合規或用戶明確要求披露。
- 來源名稱及 URL 只可留在內部 Source Guide、Claim Notes、Link Ledger 或 Review Receipt。
- 不可逐句改寫、模仿原文結構或大段搬運；先抽取可驗證事實、讀者問題、限制及判斷，再重新建立文章架構。
- 不可虛構公司能力、客戶案例、價格、合作、結果、專家身份、圖片授權或連結目的地。
- 不可聲稱保證 Google 排名、AI Overview 或 AI Citation。

## Phase router

按 [workflow-and-review-gates.md](references/workflow-and-review-gates.md) 執行：

1. 原始 Source 尚未整理：只建立 Source Guide，結束為 `SOURCE_GUIDE_REVIEW_STOP`。
2. Source Guide 已批准：只提出標題及搜尋角度，結束為 `SEO_TITLE_REVIEW_STOP`。
3. Guide 及標題已批准：建立文章、Meta、CTA、Link Ledger 及 QA，結束為 `BLOG_REVIEW_STOP`。
4. 文章已批准而用戶要求 HTML：建立本機通用 HTML，結束為 `HTML_REVIEW_STOP`。

「OK」、「繼續」或修改意見，只批准當前可見階段；不要視為發布或外部交付批准。

## Intake

用自然語言取得：

- Source：URL、文字、筆記、PDF 或圖片；
- Audience、地區及語言；
- 主要搜尋問題或讀者任務；
- 公司／品牌、Offer、CTA 及可用連結；
- 文章用途及期望格式。

資料不足時，標示 `TBC`、`LINK_TBC`、`CTA_TBC` 或 `SOURCE_NEEDED`，並繼續完成當前可安全完成嘅階段。不要用假資料填空。

## Company Brain and CTA gate

如果 Project 提供 `company-brain`、公司簡介、Offer 或品牌規則，文章階段必須先讀相關檔案；只有公司名並不足夠。CTA 必須對應已確認 Offer 及真實目的地。

沒有 Company Brain 時，使用中性教學語氣及非商業下一步；角色扮演公司必須在內部標示 `SYNTHETIC_BRAND`，不得暗示為真實公司或保險／法律／醫療承諾。

## Link gate

可放入公開文章嘅連結只限：

- 已批准嘅第一方權威／行動頁；
- 站內延伸內容；
- 已確認 CTA 直接目的地。

Source provenance 連結只留在內部記錄。每條公開連結要有清楚 anchor、用途及已核實 URL；缺少目的地時用 `LINK_TBC`，不可製造 `href`。

## HTML and image gate

- HTML 只作本機 Review，使用通用、可讀、支援繁體中文嘅 standalone HTML；不包含 Framer 專用結構。
- 圖片要放在相關段落附近，並提供描述性 `alt`；裝飾圖使用空 `alt`。
- 未確認授權嘅 Source 圖片只可出現在本機 Review HTML，必須用 `figure[data-review-only="true"]`、可見 `INTERNAL_REVIEW_ONLY` 標記及圖片清單；不得當成已批准發布資產。
- Copy／export 區域不得包含 Review-only 圖片、來源 URL 或內部備註。

## References and templates

- 用 [seo-geo-framework.md](references/seo-geo-framework.md) 選 Search Intent、Content Type 及答案結構。
- 用 [workflow-and-review-gates.md](references/workflow-and-review-gates.md) 執行每個 Review Gate。
- 文章階段必須讀 [writing-style-and-platform-rules.md](references/writing-style-and-platform-rules.md)，用嚟校準 DotAI-derived 寫作風格、Owned Answer Units、SEO／GEO 輸出及 HTML 規格；如 Company Brain 有已批准 Brand Voice，以該 Voice 為準。
- 用 [content-quality-check.md](references/content-quality-check.md) 做 QA。
- 用 [article-brief.md](assets/article-brief.md) 及 [article-output.md](assets/article-output.md) 建立可交接產物。

## Output status

每次輸出最後列出：

- `Current phase`；
- `Status`；
- `Confirmed`；
- `TBC / blocked items`；
- `Next approval needed`。

`READY_FOR_REVIEW`、任何 Review Stop 或本機 HTML 都不等於已發布。
