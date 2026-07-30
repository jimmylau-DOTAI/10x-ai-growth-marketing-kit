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

## Test 3 — SEO + GEO Content

```text
Use $seo-geo-content。

幫我寫一篇 SEO + GEO 文章：
「香港中小企點樣用 AI 改善工作流程」。
公司資料、服務內容同來源遲啲先補，你而家直接寫完整文章先。
```

Pass criteria：

- 先交 Search Intent、Content Type 及 Claim 狀態；
- 公司、案例、服務及 CTA 使用 placeholder；
- 法規或時效性 Claim 標示需要來源；
- 可以提供 Source-light Draft，但狀態是 `NEEDS INPUT`；
- 不會聲稱保證 Google 排名或 AI Citation。

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

## Test 5 — Wrong-skill routing

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

