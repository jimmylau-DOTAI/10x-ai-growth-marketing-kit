---
name: social-content-research
description: Download social images and videos, break down posts, prepare and review Source Guides, and adapt supplied sources or an existing Blog into multi-platform content. Trigger on natural requests such as 用呢份資料同 Blog 做 IG 圖、Banner、Threads 同 Reels without requiring a Skill name or a Brief request. Explicit requests to open Tasks also route to native app dispatch. Supports source learning; does not publish or change company facts.
---

# Social Content Research

## Purpose

將 Social Source 變成可追溯、可寫 Post、又唔會污染公司知識嘅研究。

核心路線：

Source → Source Guide → Shared Content Brief → Platform Task Pack → Authorized app Tasks
      └→ Source Receipt／SL → 3-day cross-source review → Candidate Insight → Human Review

呢個方法支援 Social Post research 同按要求取得來源圖片／影片。唔可以用佢更新公司事實、產品資料、品牌核心、Design System、Proposal、Skill 規則、CRM，亦唔可以自行 Publish。

所有持久化產物使用 content_scope: social-post-research-only。

## Choose one mode

用戶唔需要寫 Skill 名、「共用 Brief」或「call Skill」。例如「用已選好資料同 Blog，主線做 IG Carousel，再開兩個 Task 做 Banner、Threads 同 Reels，各畀三個方向，揀好先製作」直接選 Post Handoff，按已有資料核對來源、整理 Brief、由主 Task 做 IG，延伸 Task 交相應平台 Skill；唔要求用戶重貼技術版 Prompt。沿用當前已選定嘅 Source Guide、原始 Source、Blog 及 Style，真係有多份無法判斷先問。

若當前 Project 有用戶已確認嘅 `我的內容指令.md`，先讀其適用範圍及偏好；最新要求優先。沿用嘅係工作方法，每次仍讀今次 Source／Blog，唔沿用舊 Campaign 資料或舊批准。未存在就按當次要求做，唔強迫先建立檔案。

只講「幫我做 IG、Banner、Threads 同 Reels」亦可自動選本 Skill 及平台 Skills；若未明確要求開新 Task，就在當前任務接力處理，不將自動選 Skill 當成另開 Tasks 嘅授權。只問教學／能力仍只回答或修改教案。

用戶只想「每日入靈感袋」或稍後揀帖，就按[每日收集規則](references/content-selection.md)保存候選快照，交一次名單即停。用戶選中先讀原文或媒體做拆解；明確要求寫稿先交平台製作。

只選完成今次任務所需嘅最小模式：

1. **Quick Research**：用戶只要 Summary、Hook analysis、content teardown、angles、只貼 bare URL，或只講一般 `sl` 而未要求持久化。先做 actual-media quick triage，預設不寫 Vault。
2. **Deep SL**：用戶明確講 `deep sl`、Save and Learn、完整消化、入／存 Vault，或 Project AGENTS.md 已明確授權建立持久化產物。
3. **Three-day Insight Review**：用戶要求整理 Insights，或已授權排程而 TRIAGE-STATE 顯示到期。
4. **Post Handoff**：用戶要出一個或多個平台內容。先核對現有 Source Guide，缺少才建立，再整理共用 content brief。用戶明確要求建立／開始多個 Task 時，按 [task-dispatch.md](references/task-dispatch.md) 調用實際 app 工具，建立 Task 並交相應平台 Skill 執行；只要求 Brief／教案／可行性檢查時不建立 Task。

5. **Media Acquisition**：只要求下載原帖媒體時，圖片按 [逐張下載方法](references/image-acquisition.md)，影片按 [影片下載同檔案驗證](references/video-acquisition.md)。交可開檔案、張數及缺項。要研究就由取得嘅實際媒體接 Evidence Capture。

不要一次啟動全部模式。不要因為收到一條 URL 就自動做永久知識寫入。

## Discover and judge content

用戶要求近期／爆款來源或問做乜內容時，先讀 [content-selection.md](references/content-selection.md)。這是本 Skill 的來源選擇工作，不需要另裝私人內容判斷 Skill。之後按 Post Handoff 交平台 Skill；不要把視覺 reference 誤當當前內容來源。

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

社交 URL 或來源包含 Instagram、Carousel、Reel、Screenshot、Image、Video 時，分析前必須讀 [social-evidence-capture.md](references/social-evidence-capture.md) 並完成適用嘅擷取步驟。Evidence Capture 係研究 mode 共用嘅 phase。只要求下載時用 Media Acquisition。

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

## One selected post: Breakdown and Source Guide

用戶揀定一篇要拆，就做一次 Evidence Capture，跟[圖文／影片拆解](references/analysis-checklist.md#selected-post-breakdown)記錄原帖。只要拆解，交原帖做法就可以停。要求拆解同 Source Guide，就沿用同一次擷取分兩節交。一帖一卡保留兩節，有已確認 Guide 就沿用，需要補證據先重開原帖。

- **爆款拆解**保留原帖結構。指出第一眼、內文點推、邊度畀證據或兌現承諾、結尾叫人做乜；影片附時間碼，圖文附頁碼或圖號。互動數字是快照，對吸引或留存嘅解釋列為推斷。
- **Source Guide**係畀下一位寫稿同事嘅[內容底稿](assets/source-guide.md)。用拆解已核嘅位置，只交一個讀者問題、一個可以借用嘅做法、已核或待補嘅自家材料、同今次可講嘅範圍。新增或實質改動先交真人確認；確認後先交寫稿同事。需要存入 Notion 時，按用戶指定嘅原卡更新。

收到小紅書或 YouTube／Shorts 連結，按 [平台取材、字幕同畫面](references/social-evidence-capture.md#xiaohongshu-and-youtube) 自動揀路。現成字幕優先；有實際音軌同可用工具先轉錄。圖上字另用 OCR／視覺讀取。只有封面、畫面或逐字稿，按實際證據拆解並標明缺口。已確認嘅 Guide 可以直接接平台製作，無需重拆原帖。

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

如用戶要由 Source 出 Post，先讀現有 [Source Guide](assets/source-guide.md) 同原始 Source，核對重要論點嘅覆蓋、有冇矛盾及證據邊界；缺少 Guide 才補一份。呢份係 GEO Source Guide 嘅 Social 版本：先將來源事實、觀察、未證明項目同自己見解分開，等所有下游平台用同一個根據。

Source Guide 最少包括：

- Reader problem；
- Source／access boundary；
- Observed、Inferred、Not proven；
- Own insight：只可由已讀 evidence 推導，唔將 Source 作者主張變成公司事實；
- Safe takeaway、claims to avoid、CTA intent；
- 下一步：先 review，先可產生共用 Brief。

新建或實質修改嘅 Source Guide 交畀用戶 review 後停在 `SOURCE_GUIDE_REVIEW_STOP`；已有明確確認版本、來源及主要見解無變就沿用，不重問。來源不可讀或缺口會影響主張時，列出實際缺口；未批准嘅新主張不得傳入下游。Quick Research 可以產生精簡 Guide；Deep SL 可以由完整 SL 填入 Guide。唔要求每次出 Post 都先做 Vault 寫入或三日 Insight review。

確認 Guide 後：

1. 產生 `post-brief.md`：Audience、one point、evidence available、claim boundary、CTA、共用 Style／brand pointers；
2. 如同一見解要去兩個或以上平台，產生 [Platform Task Pack](assets/platform-task-pack.md)。示範預設由主 Task 持續負責 IG Carousel；Banner、Threads、Reels 等延伸格式才各開一張 Task Card，寫清楚共用 Brief、deliverable、output folder、Skill 同 review gate；
3. 主 Task 同所有分支 Task 必須讀同一份 `SOURCE-GUIDE.md` 同 `post-brief.md`。任何一邊都唔可自行改共同事實、見解、CTA 或 Style；要改就回到共用 Brief，再由人確認；
4. 主 Task 先實讀 `instagram-carousel-studio` 做 IG Carousel，出圖階段再實讀 `ai-social-image-maker`。SEO Banner 分支用 `ai-social-image-maker`，廣東話 Threads 分支用 `hk-threads-writer`，Reels 分支先用 `reels-text-storyboard` 交一分鐘文字稿；文字確認並要求 HTML 後用 `reels-html-storyboard`，HTML 分鏡獲確認後才可交 `remotion-reel-scene` 製作一個本機 Studio 預覽 Scene。各 owner 只寫自己的 output folder。

用戶要求「三個平台都先畀方向，揀好先整」時，主 Task 先交 IG 故事／畫面方向；三個分支 Task 分別交 Banner 標題／構圖、Threads 切入／語氣及一句 Hook、Reels 的 Hook／場景／節奏方向。先交短方向，未選定不得生成圖片或完成全文；各平台分別記錄所選方向，不把 IG 批准套用另外兩個。每次進度回報用「而家做到邊／用緊邊個 Skill／已交乜／下一步等你乜」四項。

用戶明確講「主線做 IG，再開清單同步做 Banner、Threads 同 Reels」就係今次三個分支 Task 建立與 Draft 製作嘅授權，唔再逐個確認。按 [task-dispatch.md](references/task-dispatch.md) 由系統整理資料、建立三個真正 Task、交入平台指令及追蹤結果；IG 由主 Task 直接開始。Task Card 係內部交接材料，唔要求用戶逐個複製。沒有工具就標受阻，唔以文字清單冒充已建立。

如使用 03-Insights 嘅可重用見解，只可選 human_review: approved、status: approved-for-post。

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
- 多 Task 請求已有明確授權；IG 主 Task 有實際 Skill 讀取證據，三個分支每個已建立狀態都有真實工具回傳 ID，並能讀共同資料及 package-local Skill；
- 清單區分計劃、排隊、實際執行、待 Review 及完成；每個成品有實際路徑及該平台 QA；
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
- 如有派 Task：實際 Task ID／入口、最新工具讀取狀態、已交成果及待用戶決定；工具不可用就報未建立，未實測就報未實測；
- 下一步及負責人。

## user offline route

無平台登入／capture 能力時，用用戶提供嘅 screenshot、文字、文件或可讀公開來源照做有範圍嘅 packet。分清只見 screenshot／caption／metadata／完整內容，唔由 views 或截圖片段推論爆款原因。Source 不可讀就標缺口；唔需要安裝 TikHub／Meta API 才可上堂。

寫 `SOURCE-GUIDE.md` 再寫 `post-brief.md` 作下游交接：source paths、可支持嘅 facts、observations、own insight、claim boundary、audience、one point。兩個或以上平台時，再寫 `platform-task-pack.md`。讀者可直接交 `social-post-writing`／`instagram-carousel-studio`／`ai-social-image-maker`／`hk-threads-writer`／`reels-text-storyboard`。
