---
name: ai-social-image-maker
description: Create or edit complete AI social images, Carousel cards and Blog banners using the selected Style, visible copy and real brand assets. Verify the actual image, text, Logo and requested dimensions before delivery.
---

# AI Social Image Maker

將內容、已選 Style 同品牌素材做成完整 AI 圖像。文字、主體、構圖、材質與光影一齊設計；不用 HTML／CSS 排版替代原生圖像。

## 1. 讀今次資料

沿用已有內容、用途／尺寸、Style、參考圖、品牌同 Logo 要求，只問真正影響下一步嘅缺口。先看實圖；新版 STYLE 已包含設計方法，唔補造 DESIGN。舊 Style 有獨立 DESIGN 才按需補讀；品牌共通 DESIGN 係另一類資料。

按需要讀：品牌圖用 [品牌與真素材](references/brand-adaptation.md)，將來源色彩／字形／圖像方法轉成自己品牌；未確認適配圖只交候選。平台同具體位置跟 Style 界線，未驗格式需重排並驗圖；Banner 用 [橫幅處理](references/banner-production.md)。學生只講想完成乜，AI 管理所需檔案，唔要求填技術表。

## 2. 確認尺寸與工具

按 [尺寸需求](references/size-intake.md) 寫 request，執行 preflight；已確認資料唔重問。再按 [工具能力](references/tool-adapters.md) 核對實際生成／編輯能力、參考圖輸入及尺寸控制。只喺 prompt 寫尺寸不代表工具做到。

預設用環境提供嘅 image tool；用戶指定其他可用工具時跟其要求。遵守 runtime 編輯規則，不自動安裝、付費或連帳戶。工具缺能力如實說明。

## 3. 做完整圖片

先定今次想觀眾注意／理解乜，再把文案、第一眼焦點、Style 的字形／色彩／質感及必要參考寫成簡短生成指令。用主次與視覺關係指導構圖，不主動用百分比、座標或固定格數綁住版面；只有用戶指定精確版面或窄修改才保留相應位置。需要 Logo 時留自然低細節背景，唔畫空白容器；用戶要求真 Logo 就要完成原檔放置，不能只交留位。

依 [生成、修改與 Logo 操作](references/imagegen-contract.md) 實際調用工具。窄修改保持其餘已選內容；Carousel 首圖／方向 review 跟該文件及有效用戶要求，普通單圖不強加多次選擇。每個 job 最多一次有具體方法嘅 targeted retry；仍失敗就列缺口。

## 4. 睇新圖，再驗檔

按 [圖像驗收](references/qa-contract.md) 對照當次 Style 特徵及用戶要求：標題、主角、質感、層次同指定修正有冇落實。逐字核對文案，檢查真 Logo、素材及實際尺寸；改圖後重驗，唔沿用舊 PASS。

按 [交付記錄格式](references/output-contract.md) 留同一版本嘅工具與檢查證據，執行 delivery gate。程式只核對檔案與記錄，不能代替實際看圖或證明用戶批准。

## 5. 交返成果

展示圖片／實際檔案位置、尺寸、完成項目及未解決問題，簡述實際使用嘅 Skill。未通過就標 preview；通過本地驗收仍需用戶 review，唔自動發布、排程或保存成預設 Style。只檢查文件而未出圖時，清楚說明尚未驗證生成效果。
