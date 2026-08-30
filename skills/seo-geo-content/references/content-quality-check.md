# Content Quality Check

## Phase and approval

- [ ] 只完成目前獲批准嘅階段
- [ ] 上一個 Review Stop 有清楚批准
- [ ] 輸出列出 Current phase、Status、TBC 同下一個批准
- [ ] 沒有將「OK」推斷為發布、上載或外部交付批准

## Intent

- [ ] Primary Query 清楚
- [ ] 開首直接回答查詢
- [ ] Content Type 符合搜尋者工作
- [ ] 每一段都幫助理解、判斷或行動

## Evidence

- [ ] 時效性資料已核實擷取日期
- [ ] 數字、法規、功能及引用可追溯
- [ ] 用戶提供資料與獨立核實資料已區分
- [ ] Inference 明確寫成判斷，而非來源事實
- [ ] 沒有虛構公司、案例、合作、價格或成果
- [ ] 公開正文沒有來源名稱、URL、引用清單或研究過程
- [ ] 內部 Claim Notes 保留必要 provenance 及讀取限制

## Company Brain and CTA

- [ ] 有公司內容時已讀 Company profile 及 Current Offer
- [ ] 公司名沒有被當成完整 Company Brain
- [ ] 角色扮演品牌在內部標示 `SYNTHETIC_BRAND`
- [ ] CTA 對應已確認 Offer 及真實目的地；否則標示 `CTA_TBC`

## SEO

- [ ] Title、H1 及開首自然包含搜尋概念
- [ ] 小標題描述實際問題或結果
- [ ] Meta Title / Description 與正文一致
- [ ] URL slug 清楚簡短
- [ ] 內部連結及 CTA 連結有真實目的地
- [ ] 每條 reader link 有描述性 anchor、用途及狀態
- [ ] 未確認 URL 使用 `LINK_TBC`，沒有虛構 `href`
- [ ] Source provenance link 沒有混入公開文章
- [ ] 沒有 Keyword Stuffing 或重複空話

## GEO / answer quality

- [ ] 重要問題有簡短直接答案
- [ ] 段落包含足夠上下文，抽出後不會誤導
- [ ] 內部 Claim Notes 可將重要 Claim 追溯到來源
- [ ] Named entities、日期及適用範圍清楚
- [ ] 沒有聲稱保證排名或 AI Citation

## Reader value

- [ ] 有具體步驟、例子、比較或決策準則
- [ ] 有限制、取捨或不適用情況
- [ ] CTA 符合文章目的
- [ ] 香港語境並非硬加地名

## Local HTML and images

- [ ] HTML 使用 UTF-8、`zh-Hant`、單一 H1 及合理 Heading 順序
- [ ] 手機及桌面可讀，中文字型有可靠 fallback
- [ ] 圖片位於相關段落附近並有合適 `alt`
- [ ] 未確認授權圖片有 `INTERNAL_REVIEW_ONLY`、rights status 及 image manifest
- [ ] Copy／export 區域不包含 provenance、內部備註或 Review-only 圖片

## Status

選一個：

- `NEEDS INPUT`
- `DRAFT`
- `READY FOR REVIEW`
- `SOURCE_GUIDE_REVIEW_STOP`
- `SEO_TITLE_REVIEW_STOP`
- `BLOG_REVIEW_STOP`
- `HTML_REVIEW_STOP`
- `APPROVED`
- `PUBLISHED`（需要 URL 或發佈證據）
