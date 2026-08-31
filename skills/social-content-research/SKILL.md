---
name: social-content-research
description: Use when a user provides a social post, screenshot, carousel, video, transcript, or URL and asks to research it, run SL or Save and Learn, turn it into a source-backed social-post brief, save it to a Company Vault, or review several SL notes for recurring content insights.
---

# Social Content Research

## Purpose

將 Social Source 變成可追溯、可寫 Post、又唔會污染公司知識嘅研究。

核心路線：

Source → Source Receipt → SL → Source-bounded Post Brief
                         └→ 3-day cross-source review → Candidate Insight → Human Review

呢個 Skill 只服務 Social Post research。唔可以用佢更新公司事實、產品資料、品牌核心、Design System、Proposal、Skill 規則、CRM，亦唔可以自行 Publish。

所有持久化產物使用 content_scope: social-post-research-only。

## Choose one mode

只選完成今次任務所需嘅最小模式：

1. **Quick Research**：用戶只要 Summary、Hook analysis、content teardown、angles、只貼 bare URL，或只講一般 `sl` 而未要求持久化。先做 actual-media quick triage，預設不寫 Vault。
2. **Deep SL**：用戶明確講 `deep sl`、Save and Learn、完整消化、入／存 Vault，或 Project AGENTS.md 已明確授權建立持久化產物。
3. **Three-day Insight Review**：用戶要求整理 Insights，或已授權排程而 TRIAGE-STATE 顯示到期。
4. **Post Handoff**：用戶要出 Post。先建立或讀取相關 SL，再交一份 content brief 俾平台 Post Skill。

不要一次啟動全部模式。不要因為收到一條 URL 就自動做永久知識寫入。

## Evidence first

先標示 Access state：

- FULL：Caption／正文及所有重要媒體都實際檢查；Carousel 已逐張到最後一張，影片已實際播放並檢查可取得嘅文字／音訊證據；
- PARTIAL：只讀到部分正文、部分 slides／frames，Caption 未展開，或影片／音訊未能完整檢查；
- IMAGE_ONLY：只有圖片、截圖或可見媒體，沒有可靠 Caption／完整貼文文字；
- BLOCKED：因登入、權限、地區、付費牆、平台或技術限制而無法開啟來源。

URL 優先讀原頁。影片先讀官方字幕；無字幕才轉錄實際音訊。Carousel 要逐張讀。URL 成功開啟、標題、縮圖、封面截圖、Metadata、OpenGraph 圖、搜尋摘要或 preview text 都唔足以證明 `FULL`。

每項內容再分：

- Observed：來源直接顯示；
- Inferred：根據證據作出嘅解讀；
- Not proven：來源未能證明。

不可繞過登入、付費牆或權限；不可將完整受版權保護文章或逐字稿複製入 Vault。

## Evidence Capture Before Analysis

社交 URL 或來源包含 Instagram、Carousel、Reel、Screenshot、Image、Video 時，分析前必須讀 [social-evidence-capture.md](references/social-evidence-capture.md) 並完成適用嘅擷取步驟。Evidence Capture 係所有 mode 共用嘅 phase，唔係會自動寫 Vault 嘅第五個 mode。

最少要完成：

1. 分類來源及訂出 capture plan；
2. 用現有 browser／media／vision 工具直接檢查原始內容；
3. 取得實際 Caption／正文，並逐張擷取所有可存取 Carousel slides，或檢查真實影片及代表 frames／字幕／音訊；
4. 對每個 content asset 做 OCR 及 visual inventory，記錄 index、方法、可見文字、畫面角色及限制；
5. 根據真正取得嘅證據決定 Access state；
6. 兩個或以上 assets 時，用原始 captures 建立有 index 標籤嘅 contact sheet，並在 channel 支援時連同個別／總覽 media 交回用戶。

Carousel 未到實際最後一張或有 slide 無法檢查，只可標 `PARTIAL`。Reel／Video 必須實際播放或檢查可播放嘅 media file；單一 cover image 唔可以支援影片內容分析。工具不可用或來源受阻時，誠實報告限制及可由用戶補充嘅 exported images、screen recording、screenshots 或 copied Caption；不可模擬、重畫或用 image model 重建證據。

## Quick Research

1. 如適用，先完成 Evidence Capture；記錄 Source、Access state、實際讀到與缺少部分。
2. 將 captures／contact sheet 及 media completion 交回用戶，但預設不寫 Vault。
3. 分開內容主張、可見證據及 AI Interpretation。
4. 按需要讀 [analysis-checklist.md](references/analysis-checklist.md)。
5. 輸出 Summary、Hook／結構、值得學嘅機制、風險及原創 angles。
6. 若用戶只要 Summary，停止；不要擴張成 SL。

完整輸出可用 [research-output-template.md](assets/research-output-template.md)。

## Deep SL

先讀 [source-learning.md](references/source-learning.md)，再完成：

1. 建立一份 Source Receipt；
2. 將同一來源寫成一份完整 SL；
3. 如來源有實際 visual／video evidence，建立與 Source Receipt 及 SL 配對嘅 Media Evidence Manifest；
4. 每個獨特觀點寫成 source-bounded Candidate Card；
5. 執行 SL packet validator；有 media manifest 時一併驗證；
6. 將 SL 狀態設為 queued-for-insight-review；
7. 跑 due-check；如狀態未排程，將 next_review_due 設為今次日期後三日並停止。

一份 SL 必須令未讀原 Source 嘅人明白：

- 發生咩事；
- 核心方法、論點或步驟；
- 重要例子、數字及限制；
- 對 Social Post 有咩可用價值；
- 邊啲係來源事實，邊啲只係 Interpretation。

一個 Source 可以即時產生一份「只限今次來源」嘅 Post Brief，但唔可以直接變成可重用嘅公司 Insight。

## Vault route

如獲授權寫入 Company Vault，先由最近嘅 AGENTS.md 或 Vault INDEX 找到根目錄，再只寫：

~~~text
11-內容與平台/09-Source與Insight/
├── 01-Sources/
├── 02-SL/
├── 03-Insights/
└── TRIAGE-STATE.md
~~~

- 01-Sources：來源收據、可見證據及限制；
- 02-SL：每個來源一份完整攻略與 Candidate Cards；
- 03-Insights：只放跨來源綜合結果；
- TRIAGE-STATE.md：只記上次成功 review、下次到期及已處理 SL。

不要在 Skill 內硬編絕對路徑。找不到 Vault 或未獲授權時，在工作區輸出 draft 並報告建議目的地。

## Three-day Insight Review

先讀 [three-day-insight-review.md](references/three-day-insight-review.md)。

規則：

- 只讀上次成功 review 後新增或更新嘅 SL；
- 用 candidate_key／共同問題分組；
- 轉載、鏡像及同源內容只計一個 origin；
- 0–1 個獨立來源：保留 queued，不建立 Insight；
- 2 個或以上獨立來源出現同一 pattern：建立 Candidate Insight；
- 相反證據要保留，唔可以為咗合併而抹走；
- Candidate Insight 需要 Human Review 先可變 approved-for-post；
- 三日係 review cadence，唔係證據門檻。

due-check 回傳 INSIGHT_REVIEW_NOT_SCHEDULED 時，只初始化三日日期；不要即日假裝完成跨來源 review。

自動化只可建立或更新 Candidate Insight 及 TRIAGE-STATE。不可自動批准、改公司知識、改 Skill／Design System 或發布。

## Post Handoff

如用戶要由 Source 出 Post：

1. 先完成或讀取該 Source 嘅 SL；
2. 產生 source-bounded content brief；
3. 清楚標示 evidence boundary；
4. 再交俾一個最相關平台 Post Skill。

如使用 03-Insights 嘅可重用見解，只可選 human_review: approved、status: approved-for-post。

Content brief 最少包括：

- Audience / platform；
- Problem or tension；
- Source-backed takeaway；
- Evidence available；
- Claims to avoid；
- Suggested hook；
- Suggested structure；
- CTA intent。

## Quality gate

- Access state 與實際證據一致；
- Caption／preview／thumbnail／cover 沒有被當成完整 media evidence；
- Carousel 每張可存取 slide 都有記錄，否則已標 `PARTIAL`；
- Reel／Video 有實際 playback、frame 或 media-file evidence，否則沒有標 `FULL`；
- 每個 capture 有 slide／frame-level OCR、visual note 及 limitation；多個 assets 有 contact sheet 或清楚解釋 channel／tool 限制；
- Observed、Inferred、Not proven 已分開；
- 沒有補寫睇唔到嘅 Caption、畫面、數字或成效；
- SL 有完整方法／論點，而唔係幾句摘要；
- 每個 Candidate Card 有來源及邊界；
- 單一來源沒有升格成 durable Insight；
- 同源 repost 沒有當成獨立證據；
- 未批准 Insight 沒有當成公司定論或 evergreen rule；
- 沒有自行 Publish 或改動其他知識層。

## Completion report

完成時簡短列出：

- Mode；
- Source 及 Access state；
- Media captured，例如 `slides 1–8 of 8` 或 `6 representative frames`；
- Caption state 及 OCR／visual evidence state；
- Contact sheet／media attachment 或實際路徑；
- 實際產物／路徑；
- Candidate 數量或 review 結果；
- Validator 狀態；
- Human Review 狀態；
- 下一步及負責人。
