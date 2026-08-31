---
name: seo-geo-content
description: Use when a user wants guided creation of an original SEO/GEO blog from supplied source material, stronger answer-first H2/H3 structure, company authority or evidence-backed public data links, a local HTML review, or an approved Blog handoff for a separate website deployment workflow. Does not publish or deploy.
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
| Approved Guide and title | 上述兩份 + [writing-style-and-platform-rules.md](references/writing-style-and-platform-rules.md)；如要求強答案層次／公司權威／公開數據，再讀 [answer-authority-and-evidence.md](references/answer-authority-and-evidence.md) + output templates | Article production pack | `BLOG_REVIEW_STOP` |
| Completed article draft | [content-quality-check.md](references/content-quality-check.md) | QA result and open items | 保持 `BLOG_REVIEW_STOP` |
| Approved article with HTML request | Workflow + writing-style reference 嘅 Local HTML section | Local generic HTML | `HTML_REVIEW_STOP` |
| Approved article needs website assembly | Workflow handoff section + [article-output.md](assets/article-output.md) | `blog-publish-handoff.json` | `BLOG_HANDOFF_READY` |

只讀目前階段需要嘅檔案。[article-brief.md](assets/article-brief.md) 用於整理 approved brief；[article-output.md](assets/article-output.md) 用於組裝文章 production pack。

## Guided student contract

新學生只需要啟動一次 Skill：

1. 先讀 current Source、Company context、已有 Guide／Title／Draft／HTML 同 receipt，預填已知資料；
2. 顯示 `已完成／仍欠／而家處理／下一個 review gate`；
3. 一次只問一條會實質改變 search angle、Claim、公司觀點、CTA、links、圖片權利或 approval 嘅問題；
4. 保存回答，再完成因此解鎖嘅安全工作；
5. 接受「Guide 確認」、「揀標題 2」、「Blog 批准」等短答，只批准目前可見 gate；
6. 中斷後由 artifacts 重建進度，從最早未通過 gate 繼續；
7. 出錯時保留已批准內容，先修復失敗 gate，唔要求學生由頭寫過。

不要要求學生逐段複製 technical prompts。可由 Source 或 project 發現嘅答案直接讀取，只有真正未決定事項先問。

## Intake

用自然語言取得：

- Source：URL、文字、筆記、PDF 或圖片；
- Audience、地區、語言及主要搜尋問題；
- 公司／品牌、Current Offer、CTA 及可用連結；
- 文章用途、期望格式及目前已批准階段。
- 是否要求首 100 個可見字 direct answer、約 150 字 H2／H3 解說、逐小節公司判斷或公開 data／citation links。

資料不足但不影響目前階段時，使用 `TBC`、`LINK_TBC`、`CTA_TBC` 或 `SOURCE_NEEDED`。缺少會改變文章方向、事實邊界或 CTA 嘅資料時，先交目前可以確認嘅部分及列出 blocker，不要用假資料填空。

## Core working rules

- Public copy 必須係原創 synthesis；不可貼上、翻譯、輕度改寫、模仿 Source 結構，或將外部方法重新命名成公司原創。
- Public evidence 預設 `source_blind`。只有用戶／approved brief 明確要求公開數據、citation、原始來源連結或目的地規則要求時，先使用 `reader_evidence`；兩個 mode 都禁止複製 Source 結構或公開內部研究過程。
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
- 如 brief 選擇 `authority_evidence_longform`，按 answer-authority reference 執行 rendered first-100、H2／H3 answer depth、authority density 及 reader-evidence contract；數字 target 唔可硬套到 FAQ、短 news 或完整短答案。
- 清楚寫出 Entity、日期、地區、適用範圍及 Fact／Judgment／Recommendation 邊界。
- FAQ 只回答正文已有足夠支持嘅真實問題；Schema 建議必須對應可見內容。
- 不要為 SEO 堆砌關鍵字、重複摘要、空泛小標題或無用途連結。

### Write with an owned point of view

預設使用實務營運者語氣：書面繁體中文配合自然香港用語，先講讀者熟悉嘅工作阻力，再解釋術語。將技術翻譯成 input、output、time、cost、risk、approval 及 next step。

每個主要段落應推進新資料或判斷。長文建立 3–5 個有用嘅 Owned Answer Units：

`verified fact／definition → company or author judgment with reason → work translation → visible deliverable → limitation or human boundary`

公司名稱只用於真實擁有嘅判斷、方法、證據、限制或下一步。重複品牌名不會增加權威；第一身實測只有在真實 artifact 或 receipt 存在時先可使用。

`owned_units` 係預設 authority density。只有用戶／approved brief 明確要求，先使用 `per_subsection`；每個非 FAQ H3 必須增加一個不同而有理由嘅公司判斷，唔可以只重複品牌名。

### Complete the production pack

交付內容包括：

- H1、Meta title、Meta description and slug；
- Primary Query、Search Intent and related questions；
- Answer profile、authority density and public evidence mode；
- Article body and Owned Answer Unit ledger；
- Evidence atom ledger when public data is requested；
- supported FAQ and Schema recommendation；
- Internal-link plan、Reader Link／CTA Ledger；
- Claim Notes、image manifest、QA Status and Open Items。

Public links 只限已確認嘅第一方 authority／action page、`reader_evidence` 中直接支持相鄰 public claim 嘅 primary evidence、真正相關站內內容或 CTA direct destination。每條連結要有描述性 anchor 及幫助讀者理解或行動；欠缺真實目標時使用 `LINK_TBC`，不可製造 `href`，亦不可將內部 provenance URL 偽裝成 reader link。

CTA 必須對應已確認 Offer、適合本文讀者及真實目的地；否則使用 `CTA_TBC`。完成初稿後讀完整 QA checklist，修正後停在 `BLOG_REVIEW_STOP`。

如有 Python 3，可用 `scripts/validate_article_contract.py` 檢查 rendered opening、body H1、H2／H3 prose、authority density、FAQ mirror、links 同 images。Script 只驗結構，不能代替 evidence review、writing judgment 或 Human Review。

## Phase 4: Local HTML review

只有文章已批准，而且用戶明確要求 HTML，先建立本機 generic HTML：

- 使用 UTF-8、`<html lang="zh-Hant">`、單一 H1 及 `<main id="article">`；
- Heading、段落、表格、連結及圖片在手機與桌面均可讀；
- 使用可靠 CJK font fallbacks；
- 不加入 Framer、CMS、tracking、publish 或 deploy 行為。

如用戶要求使用 Source 圖片，先合法取得檔案、保存到 Project asset folder，並放在真正相關段落。Rights 未確認嘅圖片只可標示 `INTERNAL_REVIEW_ONLY`，另記來源、用途及 rights status，不可進入公開 copy／export。

停在 `HTML_REVIEW_STOP`。Google Doc、CMS upload、publish、deploy 或 send 需要用戶在當前對話另行批准指定目標；完成後必須 read back 真實目的地。

## Phase 5: Blog publish handoff

文章經 Human Review 批准後，可以建立 `blog-publish-handoff.json` 交俾 `landing-page-blog-deployer`。HTML 唔係必要條件；可以交 Markdown、MDX、JSON 或現有 CMS-safe source，但必須指向真實 artifact。

Handoff contract 見 [article-output.md](assets/article-output.md)，最少包括：

- source artifact、content source、approval status；
- slug、title、meta title、meta description、language；
- canonical path；
- verified internal links；
- CTA label、target、status；
- Article／FAQ schema recommendation 同 visible-content match；
- image rights status 同 open items。

只有文章、metadata、CTA、公開 links、rights 同 Schema support 已確認，而且 `open_items` 為空，先使用 `APPROVED_FOR_ASSEMBLY` 同 `BLOG_HANDOFF_READY`。呢份 handoff 不批准 CMS upload、Preview、Production deploy、tracking、CRM、email 或 domain action。

## Completion receipt

每個階段最後列出：

- `Current phase`；
- `Status`；
- `Confirmed`；
- `TBC / blocked items`；
- `Next approval needed`。

Phase receipt status 加入 `BLOG_HANDOFF_READY`。任何 Review Stop、`READY_FOR_REVIEW`、本機 HTML 或 handoff 都不等於已發布。
