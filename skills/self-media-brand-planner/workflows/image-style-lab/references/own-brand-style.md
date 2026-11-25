# 從參考候選變成自己的品牌 Style

本 reference 是拆解 Skill 的適配契約，不是第三個 Skill，也不是用家要填的問卷。

## 先有自己的品牌來源

從當前 brief／已確認資料／active Vault 的精確品牌檔讀品牌身份、色彩角色及相關字體／資產規則。未有 palette 可先完成 reference-only 分析；只問缺少的品牌資料。用戶明確授權設計新 palette 時可先提 brand candidate，確認後才當自己的品牌規則。唔拿外部 reference 色值假扮已確認品牌色。

STYLE 的 brand_state：
- reference-only：設計方法候選，仍未完成自己品牌轉化；可按批准保存研究／候選。
- brand-adapted：已套入自己的品牌來源／配色角色，等待用戶確認。
- brand-approved：用戶已確認這個品牌適配版本；不是圖片已過全部 QA、平台 default 或發布批准。

新包在 STYLE frontmatter 的 brand_id、brand_source、brand_palette、brand_review 記依據。brand_palette 用 JSON object 記角色與 HEX，例如 primary／background／text，可另加 accent；這些是適用的 palette，唔係聲稱每個照片 pixel 精確相等。來源用可追溯的 Vault-relative path、來源 ID 或公開連結，不帶私人絕對路徑。brand_review 在真正確認後指向 `STYLE.md#確認與測試`，該節記日期、版本、用戶確認範圍，唔為此另建文件。舊五文件包維持 DESIGN metadata／PREFERENCE 確認證據，不憑空升格。

## 適配而不失去質素

- 色彩先映射功能：大標／底色／重點／文字保持閱讀對比，唔只全圖套色濾鏡。
- 自然膚色、動物、食物、植物、真產品包裝保持真實／產品身份；除非 job 要求，唔染成品牌色。
- 保留已選字體氣質、字圖比例、材質／光影、設計節奏；字體 exact name 未知就標類別與合法替代。
- 外部原句、人物身份、Logo、主體姿勢及資訊排列唔整套搬入；只換色或 Logo 唔代表充分轉化。
- 修改用家已選自有成品時，當次 KEEP／CHANGE 優先；colour-only 不授權改字、換主體或重排。
- Logo intent 跟 job：not-requested／required／later-by-request。無 Logo 可以符合品牌 brief；required 時只用真資產。自然 quiet corner 不加空白牌或框。

## 對着實圖判斷

比較來源／品牌來源／新版本：保留了哪個機制？品牌色如何落到角色？自己的內容／主體／場景是否清楚？文字可讀嗎？有冇保留用戶不想要的 Logo 容器？

缺新圖時可交 brand-adapted spec，但唔聲稱已證明視覺品質。brand-approved 記真用戶確認；正式圖仍由 maker 對實際版本做文字、素材、尺寸及品牌 QA。Validator 只查欄位與格式，不證明色彩、原創性、權利或確認內容真確。
