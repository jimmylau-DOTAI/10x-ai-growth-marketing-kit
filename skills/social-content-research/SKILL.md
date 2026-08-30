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

1. **Quick Research**：用戶只要 Summary、Hook analysis、content teardown 或 angles。預設不寫 Vault。
2. **Deep SL**：用戶講 SL、Save and Learn、完整消化、存入 Vault，或 Project AGENTS.md 已明確授權。
3. **Three-day Insight Review**：用戶要求整理 Insights，或已授權排程而 TRIAGE-STATE 顯示到期。
4. **Post Handoff**：用戶要出 Post。先建立或讀取相關 SL，再交一份 content brief 俾平台 Post Skill。

不要一次啟動全部模式。不要因為收到一條 URL 就自動做永久知識寫入。

## Evidence first

先標示 Access state：

- FULL：正文及主要媒體已讀；
- PARTIAL：只讀到部分正文、預覽或部分媒體；
- IMAGE_ONLY：只有圖片或截圖；
- BLOCKED：內容無法存取。

URL 優先讀原頁。影片先讀官方字幕；無字幕才轉錄實際音訊。Carousel 要逐張讀。標題、縮圖、搜尋摘要唔等於完整內容。

每項內容再分：

- Observed：來源直接顯示；
- Inferred：根據證據作出嘅解讀；
- Not proven：來源未能證明。

不可繞過登入、付費牆或權限；不可將完整受版權保護文章或逐字稿複製入 Vault。

## Quick Research

1. 記錄 Source、Access state、實際讀到與缺少部分。
2. 分開內容主張、可見證據及 AI Interpretation。
3. 按需要讀 [analysis-checklist.md](references/analysis-checklist.md)。
4. 輸出 Summary、Hook／結構、值得學嘅機制、風險及原創 angles。
5. 若用戶只要 Summary，停止；不要擴張成 SL。

完整輸出可用 [research-output-template.md](assets/research-output-template.md)。

## Deep SL

先讀 [source-learning.md](references/source-learning.md)，再完成：

1. 建立一份 Source Receipt；
2. 將同一來源寫成一份完整 SL；
3. 每個獨特觀點寫成 source-bounded Candidate Card；
4. 執行 SL validator；
5. 將 SL 狀態設為 queued-for-insight-review；
6. 跑 due-check；如狀態未排程，將 next_review_due 設為今次日期後三日並停止。

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
- 實際產物／路徑；
- Candidate 數量或 review 結果；
- Validator 狀態；
- Human Review 狀態；
- 下一步及負責人。
