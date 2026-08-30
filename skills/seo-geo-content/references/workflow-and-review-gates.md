# Workflow and Review Gates

## 1. Source Guide

目的係理解 Source，而唔係即時寫 Blog。

最少包括：

```markdown
# Source Guide

## Reader problem
## Verified facts and scope
## Useful examples or mechanisms
## Limits, risks, and unknowns
## Search opportunities
## Internal provenance
## Claim status
```

Source Guide 保持中性，不加入 Company judgment、Offer、CTA 或公開文章 polish。

Claim status 使用：

- `VERIFIED`：已由可追溯來源核實；
- `PROVIDED`：由用戶提供但未獨立核實；
- `INFERENCE`：根據資料作出嘅判斷；
- `SOURCE_NEEDED`：未補證據前不可公開使用。

如果 Source 無法完整讀取，要標示 `PARTIAL` 或 `BLOCKED`，列出實際讀到嘅部分。搜尋結果摘要、縮圖或截圖不是完整來源。

結束狀態：`SOURCE_GUIDE_REVIEW_STOP`。

## 2. SEO title and angle

只在 Source Guide 獲批准後進行。輸出：

- Primary Query；
- Search Intent；
- Audience and location；
- Content Type；
- 十個真正不同嘅標題方向：Search-direct、Work friction、Beginner question、Process／outcome、Company point of view 各兩個；
- 每個標題記錄 angle、primary search phrase、reader promise 及 overpromise／jargon risk；
- 推薦 Top 3 及每個推薦原因；
- 核心答案及獨特觀點；
- 暫定 CTA／`CTA_TBC`。

標題要符合讀者工作，不可為追求點擊而超出證據。不要用十個近義改寫充當探索；`最新`、年份、數字、`完整`、`實測` 或結果承諾只有在內容可以完全兌現時先使用。

結束狀態：`SEO_TITLE_REVIEW_STOP`。

## 3. Article production

只在 Guide 及標題獲批准後進行。

### Company Brain read gate

如有公司資料，最少讀：

1. Company profile／定位與受眾；
2. Current Offer／服務或產品；
3. 與文章有關嘅 Claim evidence（如有）；
4. CTA direct destination（如有）。

公司名本身不算 Company Brain。欠缺資料時，不可自動加品牌權威、服務承諾或硬銷 CTA。

### Article output

包括：

- H1 及開首直接答案；
- 由讀者問題推進嘅 H2／H3；
- 具體步驟、準則、例子、限制及適用情況；
- Meta title、Meta description、slug；
- FAQ（只在真實幫助讀者時使用）；
- CTA；
- Internal Link Ledger；
- Claim Notes；
- QA Status and Open Items。

文章階段可使用 `COMPANY_FRAMEWORK` 標示由 Company Brain 支持、確實屬於該公司嘅命名方法或 decision rule。不可將外部方法重新命名成公司原創；未有 ownership evidence 時只可使用 `INFERENCE` 或中性描述。

公開正文保持 source-blind；內部 Claim Notes 保留 provenance。

### Reader link ledger

```markdown
| Anchor | Destination | Link class | Purpose | Status |
| --- | --- | --- | --- | --- |
|  |  | authority / internal / CTA |  | VERIFIED / LINK_TBC |
```

每條連結要幫助理解或完成下一步。不可將 provenance URL 偽裝成 reader link，亦不可加入未核實、轉址不明或虛構連結。

結束狀態：`BLOG_REVIEW_STOP`。

## 4. Local HTML review

只在文章獲批准而用戶明確要求 HTML 後進行。

HTML 最少要求：

- `<html lang="zh-Hant">` 及 UTF-8；
- 單一 `<main id="article">`；
- H1 只有一個，Heading 順序合理；
- 手機及桌面可讀；
- 所有公開連結有清楚 anchor；
- 不含 Framer、CMS、追蹤碼或發布動作；
- Copy／export 區域不含內部 provenance、Review badge 或未批准圖片。

### Source image review rule

只有用戶要求保留 Source 圖片，而且可以合法取得檔案時，先下載到 Project asset folder，再放入相關段落。授權未確認時使用：

```html
<figure data-review-only="true">
  <div class="review-badge">INTERNAL_REVIEW_ONLY</div>
  <img src="assets/example.jpg" alt="描述圖片真正展示嘅內容">
  <figcaption>Review-only image；rights status: TBC</figcaption>
</figure>
```

另建立圖片清單：來源 URL、原始位置、用途、rights status、公開處理決定。不可用 screenshot 偽裝成已授權圖片。

結束狀態：`HTML_REVIEW_STOP`。

## 5. Boundary after HTML

Google Doc、CMS upload、publish、deploy 或 send 屬於另一個交付階段。只有用戶在當前對話明確批准目標及動作後，先可以使用相應工具；完成後要 read back 真實目的地。
