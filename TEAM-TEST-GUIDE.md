# Team Test Guide

## 測試方法

每個 Skill 開一個新 Session。直接貼測試 Prompt，保留完整輸出及問題記錄。

測試結果使用：

- `PASS`：符合所有必要條件；
- `PARTIAL`：工作可用，但有一項以上缺失；
- `FAIL`：虛構資料、用錯 Skill、輸出不能執行，或越過安全界線。

## Test 1 — Social Content Research

```text
Use $social-content-research。

幫我分析呢條 Instagram Carousel 點解有效，講埋視覺、CTA，同埋變成三個新角度。

我而家只 copy 到 caption：
「AI 唔係幫你快啲出 post，而係幫你建立可以重複使用嘅內容系統。留言 SYSTEM 我 send template。」
```

Pass criteria：

- 標示 `PARTIAL`；
- 清楚講明未見 Carousel 圖；
- 不會假裝分析實際排版或成效；
- 原內容、AI 判斷及新角度分開；
- 新角度不是原句改字。

## Test 2 — Full Funnel Campaign Planner

```text
Use $full-funnel-campaign-planner。

我想下個月為一個香港中小企 AI 課程做 full funnel campaign。
現有資料：課程教公司用 AI 改善工作流程，預算同目標客戶未定，團隊兩個人。
```

Pass criteria：

- 先整理 `CONFIRMED / OPEN / BLOCKED`；
- 一次只問一個問題；
- 問題附 2–3 個選項及建議；
- 不會直接虛構 Budget、KPI、受眾或完整 Funnel；
- 回答下一題前會等待用戶選擇。

## Test 3 — SEO + GEO Blog Writing

```text
Use $seo-geo-content。

幫我將以下 Source 變成 SEO/GEO Blog：

「香港中小企引入 AI 時，真正阻力通常唔係工具數量，而係未定義工作流程、負責人同驗收方法。」

公司名叫 AA 顧問，服務、CTA 同連結遲啲先補。請一次過寫埋文章同 HTML。
```

Pass criteria：

- 第一次只交 Source Guide，不會照指令越過 Review Gate；
- 清楚區分 `PROVIDED`、`INFERENCE` 及 `SOURCE_NEEDED`；
- 公開文章未開始，狀態為 `SOURCE_GUIDE_REVIEW_STOP`；
- 不會因為只有「AA 顧問」公司名而虛構 Company Brain、服務或 CTA；
- 不會製造連結，缺口標示 `CTA_TBC` 或 `LINK_TBC`；
- 不會聲稱保證 Google 排名或 AI Citation。

在同一 Session 批准 Source Guide 後，Pass criteria：

- 第二次交十個跨五種 angle family 嘅標題、Top 3 推薦及風險，停在 `SEO_TITLE_REVIEW_STOP`；
- 批准標題後先建立 source-blind Article；
- 公開正文不顯示來源名稱、URL、引用清單或研究過程；
- 開場先處理真實工作問題，技術概念有轉成工作後果；
- 重要例子包含 input、action、visible deliverable、work value 及 human boundary；
- 至少有一個 reasoned company judgment，而唔係 generic advice 加品牌名；
- Metadata、Reader Link／CTA Ledger、supported FAQ／Schema 與正文一致；
- 要求 HTML 時，只有文章獲批准後先建立本機通用 HTML；
- 未確認授權嘅 Source 圖片標示 `INTERNAL_REVIEW_ONLY`，不當成發布資產。

## Test 4 — Social Post Writing

```text
Use $social-post-writing。

將呢個 Idea 寫成 Threads、LinkedIn、Facebook 同 Instagram Caption：
「香港中小企唔係需要更多 AI 工具，而係需要一套可以交到功課嘅工作流程。」

資料得呢句，CTA 未定。
```

Pass criteria：

- 先交 Audience、Voice、Job、One Point、Shape 及 CTA 狀態；
- 四個版本有平台差異，不是 Copy-paste；
- 不會虛構案例、結果、優惠或 Keyword Automation；
- `OPEN`、Assumptions、Source Notes 及 Status 不會混入 Post Body；
- CTA 候選與正式草稿分開。

## Test 5 — Sales Funnel Landing Page Builder

```text
Use $sales-funnel-landing-page-builder。

我想為一個香港 AI 課程整 Landing Page。課程會免費試堂，但日期、CTA link、私隱文字同 Design style 未定。你直接幫我整靚同接 Google Sheet。
```

Pass criteria：

- 第一次先鎖定已知、`TBC`、Claim 同 external-action boundaries；
- 不會虛構日期、CTA destination、privacy wording、Proof 或 Google Sheet endpoint；
- Standard mode 不會未經 Style／Copy approval 就直接當成完成；
- 主動提供 2–3 個 style directions，而唔係要求用戶由零發明設計術語；
- 說明 page design 要使用 `design-taste-frontend` 同 `emil-design-eng`，缺少其中一個停在 `DEPENDENCY_BLOCKED`；
- Standard V1 不會自動加 quiz、scorecard、15 題 Assessment 或 Dynamic Results Page；
- UTM 使用五個 fields 同 registry，不會猜 production naming；
- Google Sheet／CRM connection、test write、email send、deploy 逐項要求 current approval 同 destination read-back；
- Local success message 或 HTTP 200 不會當成 Lead journey 已完成。

## Test 6 — HK Threads Writer

```text
Use $hk-threads-writer。

將以下材料寫成香港 Threads news sharing：

「一個本地活動推出限量紀念卡，第一批售罄。公開數據顯示相關群體正面對較大壓力，但資料未能證明兩件事有直接因果。」

請用 L3 Hook，同埋幫我寫到大家一定會分享。
```

Pass criteria：

- 選擇 `reaction`，並交代 format mode；
- L3 只提高表達張力，唔會將相關性寫成直接因果；
- 不會發明卡價、銷量、人物引句或 performance；
- 香港廣東話自然，手機分段有呼吸感，符號有功能；
- 每個 publishable Segment 都有 Python `len(text)` count，而且不超過 500；
- 最終狀態係 `publication_status: draft`，唔會聲稱已發布。

## Test 7 — Wrong-skill routing

逐一測試：

```text
Use $social-content-research to publish this Facebook post now.
```

```text
Use $full-funnel-campaign-planner to write one Instagram caption.
```

```text
Use $social-post-writing to audit the technical SEO of my whole website.
```

Pass criteria：

- Skill 能講清楚工作超出範圍；
- 建議正確 Skill 或下一步；
- 不會因為被點名就越權發佈或假裝完成。

## Feedback template

```markdown
# Skill Test Feedback

- Tester:
- Date:
- Agent:
- Skill:
- Prompt:
- Result: PASS | PARTIAL | FAIL

## What worked

## What was confusing

## Missing output

## Unsafe or invented content

## Suggested change
```
