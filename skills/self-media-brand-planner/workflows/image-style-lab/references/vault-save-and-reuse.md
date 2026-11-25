# 保存與下次重用

先沿用用戶指定 Vault、已知用途及最近 INDEX／DESIGN；Carousel 歸 Carousel，SEO 歸其格式。Visual-Styles 只係明確通用用途或無對應格式目錄時的備用。格式路由見 [platform-routing-and-design-id.md](platform-routing-and-design-id.md)。

## 保存候選與更新

有效同範圍保存／搬位／更新批准持續有效。修改前交代 exact files、改動、影響；查重後執行，不因 dry-run 完成再問同一批准。普通讚好唔授權未約定的 Vault 寫入。

## 先決定係 revision 定新 Style

`style_id` 是一款 Style 的長期身份，不能用作「今次第幾稿」。新 pack 用沒有 `-v1` 尾綴的穩定 kebab-case ID；`style_revision` 才記同一身份下的修訂次數。

只有以下全部不變，才可留在同一 ID 並將 `style_revision` 加一：格式與比例家族、三個核心辨識規律、active references 所代表的視覺方向、以及 Logo／safe-area 的構圖界線。一次普通調色、修一個字、換同一方向的主體或更新一張同款示例，通常是 revision。

出現任何一項就要 fork 新 ID：由 IG 正方形改為 SEO 橫幅；用戶否決原方向並指定另一個；active reference 改成新的獨立視覺方向；或把「自然角落放 Logo」改為新的構圖規則。新 pack 填 `predecessor_style_id` 指向來源；舊 pack 在確認節寫 `superseded_by`，或清楚寫成仍然並列候選。唔可以覆寫舊 pack 令它靜悄悄變成另一款 Style。

新 pack 的 frontmatter 必須有：

```yaml
style_id: expressive-reaction-blog-banner
style_identity_contract: immutable-v1
style_revision: 1
predecessor_style_id: previous-style-id-or-none
identity_basis: 16:9 banner + oversized capsule headline + expressive real-pet subject
```

`identity_basis` 是人可讀的識別摘要，不是 Content Job 文案。舊 pack 沒有 contract 時維持可讀／可驗，遷移只在用戶要求時進行。

新 pack helper（需 Python／Pillow）：
```bash
python3 scripts/save_style_pack.py <pack-or-experiment> --vault <vault> --style-root <exact/format/Style-Candidates>
python3 scripts/save_style_pack.py <pack-or-experiment> --vault <vault> --style-root <exact/format/Style-Candidates> --apply
```

--style-root 必須明確提供；預設 dry-run。helper 檢查結構／圖片、複製完整 current gallery、寫可點擊連結與首張 preview、比較 read-back hashes，拒絕覆蓋已有目的地。這不禁止按用戶批准更新既有 Style：用 bounded edit 保留先前版本／來源紀錄，更新主檔、preview、hash 和規則，不為每個微調開新 style ID。

新包複製 STYLE＋DESIGN＋current images；存在完整 `DECONSTRUCTION.md` 時一併複製作 evidence。明確另要文案 Tone 且 `tone_requested: true` 才帶 TONE。舊包維持五文件相容。現有格式 INDEX 可以加連結／preview，但不是每款 Style 再生一份 INDEX。確認、測試及來源放 STYLE 對應節，不再另開收據填同一資料。

保存 reference-only 候選不需要有品牌 palette；不能因此宣稱正式品牌 Style。brand-approved 依 own-brand-style.md 記實際品牌與用戶確認。圖片 QA 和跨題材證據另記，不虛填。

本地可保存不等於可公開分發圖片。無權複製則保留外部引用，不能報已完整 portable 保存。

## 示範圖可見

把最新封面、內頁、收結按次序放入 STYLE「參考圖片與觀察」（舊包才用 REFERENCE），以本地相對路徑嵌入；首圖是 catalogue preview。已選新版存在時，原始 inspiration／被替代版本不混進 active gallery；研究候選只有原圖則清楚標 inspiration。移動後核對相對連結、第一張、最後一張、來源與 hash。

## 真正持久的選用

沿用現有格式 INDEX／Router，不新建另一套偏好系統：
- 候選收錄：記 style_id、主檔路徑、current preview、版本及 brand_state；不改 default。
- Project selection：在既有 Project 選擇紀錄記 style_id／path、brand_id、format scope、版本、用戶選擇依據；不影響其他 Project。
- 用戶明確要求品牌／格式 default 時：在該既有 INDEX 記 default_style、brand_id、platform_scope、version 及 approval_evidence。字段可跟既有結構對應，不強改格式。自己的品牌正式預設要 brand-approved；選 reference-only 研究候選不能冒充正式品牌預設。

讀取優先：今次明確指定 → Project selection → 同品牌且同格式的 default。無合適候選才最小選擇；路徑失效或 scope 不符要講清楚，不偷偷選另一款。不要掃全部風格內容。

重用新包讀選中 STYLE＋DESIGN、最新品牌來源、少量 current reference anchors 同新 job；DECONSTRUCTION 只在重新定義、修正或審核 Style 時讀。舊包按原結構讀。唔重讀全部歷史，但唔只靠文字描述。品牌源、Style 或示例有更新，重驗受影響部分；單次調色／文案修改不自動寫成永久規則。

以上是 Lab 的保存／交接契約；下游 maker 是否已實作相同讀取要另外核對。尚未跑新 task 重用，就不能聲稱永久預設已生效。
