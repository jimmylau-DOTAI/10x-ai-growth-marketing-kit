# Native 出圖與分級 QA

先沿 SKILL.md 選 Quick Batch、Review First 或 Final QA。不要將 Final QA 的逐檔驗收套在普通草稿批次。

生成／改圖前確認用途、width × height px、reference、exact copy、輸出位置及有效批准。資料已明確不重問；未有尺寸亦未授權自選就先問，不猜平台唯一尺寸。

先讀當前 image tool 真實 schema。新圖、現有圖編輯、重構比例各選支持該工作的可用工具；遵守 runtime 指定的圖像工具規則。工具無 model／aspect 欄位不捏造參數。尺寸只寫在 prompt 就記 prompt-only，不能宣稱精確尺寸控制。無合用能力只交已獲准 preview 或報缺口。

實際看圖後才生成／修改。工具素材要包括真實產品原圖、Primary reference／相應可讀 crop 與 Logo Safe Area 要求；在 prompt 講清楚：原圖決定商品，reference 決定版面、明暗、色彩比例、圖文密度和攝影語言。不能只帶產品圖再用形容詞代替 reference，也不能只附細長到看不清的完整長頁。不能手打近似商標冒充 Logo。每張獨立檔案。延伸時仍附真產品、Primary reference crop 與同一個 Style Recipe；生成圖只能參考設計，不能代替身份原件。

### Logo two-stage rule

生圖模型不可重畫商標。先生成沒有 Logo、但有乾淨 safe area 的視覺底圖；再用能真正保留原檔 pixels／向量的 compositing 或 design tool，在指定位置加入原 Logo。後製前交付叫 `preview_without_logo`，不能稱為完成圖。若本環境沒有可靠 overlay 能力，要交付合成步驟與保留 safe area，明確標 `logo_overlay_required`；不得用近似文字或失真的 AI logo 取代。

## Quick Batch：快而有底線

批次前打開原產品、Logo、Primary reference 和一張代表圖。代表圖沒有以下硬錯便繼續整批：錯 SKU／容量、產品變成另一種形態、AI 假 Logo、未確認 claim、主要文案完全不可讀。後續圖片以縮圖／聯看抽查產品一致、頁面是否重複及明顯壞圖；只重做出錯檔，不為每張寫長 QA、hash 或 JSON。

Reference Match 批次另做一個快速漂移檢查：把 reference crop 與代表圖縮小並排；若整體明暗、最大色塊分佈、產品大小／位置、圖文密度四項中有兩項明顯不同，代表圖不可作批次 seed。修正 prompt 時直接寫出偏差，例如 `keep the reference's bright sky-blue and white modular PDP layout; no dark showroom, no glass podium, no cinematic curtains`，不要只加「更相似」。

一次過多圖時，先建立簡短 batch manifest：content_id、頁面／角度、文案、輸出檔及狀態。獨立圖可按工具能力並行；Logo overlay、統一尺寸及命名可在生成後批次處理。完成時回報成功數、失敗數和需人睇的例外。

## Review First／Final QA：視覺 review 先於檔案驗收

把輸出、產品原圖、Logo 與已選參考實際打開比較。先檢查：

- 不讀細字，第一眼是否認到主產品與單一重點？包裝清楚，沒有被標題、裝飾或圖示搶焦點？
- 包裝配色、公司識別與參考的攝影／字體是否協調？是否只是拿通用模板換產品？
- 光影、透視、接地陰影、材質是否一致？產品與背景是否有足夠分離？
- 產品是否自然融入海報？有沒有去背白邊、不同光源／色溫、浮起的底部或過度調色？融合不能靠改掉真實包裝及 Logo 來達成。
- 在手機大小下，主標題及賣點能否讀清、留白有節奏？各頁構圖是否服務不同目的？
- Logo 是否是原檔 overlay、可辨認，並符合計劃？如仍是 AI 重畫或尚未 overlay，必須標 preview，不可寫 PASS。

有任一明顯問題就記具體位置與原因，改對應構圖／配色／文字密度再試；不要只把 prompt 改成「更高級、更漂亮」。視覺感受不能用尺寸、hash 或自評總分代替。技術上成功也不能自行替用戶確認新風格。

Final QA 或用戶指定的 Review First 圖，才在生成／加 Logo／改字／改尺寸後逐張重新開啟並記：

- 實際 width／height、檔案 SHA-256 及工具回傳來源；
- 逐字核對 exact copy、CTA、Logo、數字及 claim；
- 對照真實原圖：形狀、比例、顏色、材質、零件、包裝；
- 對照 Style：構圖、光影／材質、閱讀次序、文字整合及可讀性；
- 不合格位置、修正方法及新版結果。

Final QA 的檔案尺寸用可靠 metadata 工具量，不能由 prompt 推斷。Quick Batch 只需保留用戶要求的方向／比例，工具無精確尺寸控制時集中在批次尾處理。尺寸失敗先換控制方法；不要因草稿像素差異阻塞其餘內容生成。

Final QA 紀錄才綁實際 hash；圖改了舊 PASS 無效。Quick Batch 可標 `DRAFT_BATCH_COMPLETE`，不冒稱平台正式檔。只有 Final QA 的檔案／尺寸與視覺檢查完成，才叫 `LOCAL_QA_PASSED_REVIEW_REQUIRED`。

## Final QA 才跑完整本地驗收

用戶要求正式尺寸／final／交付前檢查時，才讀 [size-intake.md](size-intake.md) 寫 request，再讀 [output-contract.md](output-contract.md) 留 evidence，沿以下順序執行。Quick Batch 不跑這三個 checker：

```text
python3 <本Skill>/scripts/verify_delivery.py <job>/request.json --preflight
python3 <本Skill>/scripts/inspect_images.py <job>/output.png --expected <width> <height> --output <job>/image-check-v1.json
python3 <本Skill>/scripts/verify_delivery.py <job>/delivery.json --output <job>/delivery-check-v1.json
```

width／height 来自該 request，不由示例推斷。需要 Python／Pillow；缺 runtime 先回報，不自動安裝。退出碼失敗就不交作合格成品。`tests/test_delivery.py` 只用合成圖驗規則，唔代表真圖好睇或跟足 Style。
