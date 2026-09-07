# Creative Direction / 出圖前創意診斷

## 為何需要這一步

產品事實、pack lock、claim boundary 是「不可變」；它們不會自動產生品牌風格。沒有一個可判斷的藝術方向時，模型通常會輸出白底、包裝置中、無記憶點的通用電商圖。先做方向，才讓 AI 有足夠自由把故事、鏡頭、光線與畫面張力做好。

## 先分兩層

| 層 | 內容 | 例子 |
| --- | --- | --- |
| 不可變 Product Truth | 真產品外形、包裝字、logo、已核實特點、不能宣稱的內容 | 同一款藍色軟袋；不可變盒、不可創作新功效 |
| 可變 Creative Field | 情緒、攝影語言、鏡頭、人物、貓、家居、道具、光影、圖文關係 | 午夜藍的 cinematic 家居、雜誌式材質 still life、溫暖紀錄片感 |

不要用「保留產品」當理由，將 Creative Field 一併鎖死。

## 有參考圖：只做一個 Reference Match Direction

把 Primary reference 的八項 Style Lock 直接變成一個可執行方向。方向名稱用 `Reference Match — [可見特徵]`，並寫清：哪個 reference crop、產品替換位置、我方文案位置、Logo safe area、保留的明暗與色塊、不可出現的風格漂移。

不要為展示創意另外提供 Cinematic、Editorial 或 Documentary 三套 style。創意應放在同一視覺家族內的場景、產品角度和內容問題，而不是每頁換品牌。

## 沒有參考圖：先做一個方向

AI 按產品、用途和品牌資料提出一個最合適 candidate。只有用戶明確要求「三個方向／比較風格」才產出三個方向。每個方向包含：

1. 方向名稱與一句情緒描述
2. 客戶當刻想解決的問題
3. 主產品以甚麼角色出現（hero、道具、日常物件、畫面切入點）
4. 鏡頭／構圖（距離、角度、留白、前中後景）
5. 光線、色彩、材質與空間
6. 人／寵物／場景的獨特設定
7. 文字怎樣融入，而非把字貼在空白位置
8. 3 個要避免的 generic cliché

### 要比較時可用的差異範式

- **Cinematic sanctuary**：情緒先行，電影式側光、景深、家居真實紋理；產品是安靜、可信的 hero。
- **Editorial material study**：雜誌攝影與材質特寫，形狀、陰影、顆粒、色帶構成主畫面；不必有人或貓。
- **Real-life documentary**：手持鏡頭般的自然日常，人物正在做合理動作；產品只是生活流程中清楚可見的一部分。

這三項只是起點，不是強制風格；依品類、受眾與 reference 改寫。

## Style Proof 規則

有 Primary reference 時，從相應 crop 生成一張 **Reference Match Proof**；縮圖並排檢查明暗、最大色塊、產品大小／位置和圖文密度。若交付是廣告，再驗產品、logo、標題與畫面融合；若交付是 PDP，Proof 必須是其中一頁真的資料結構。PDP 不可先交無字 mood image 假裝已驗證詳情頁。

Quick Batch／「直接完成」仍先在內部生成 Style Proof。一般模式以產品、Logo、claim 三項硬檢決定量產；Reference Match Mode 另外把明顯 `REFERENCE_DRIFT` 當硬錯。以下其餘品味項目用作快速挑選與批次改良，不逐項阻塞每張圖片。Review First 才把 Style Proof 交用戶確認後再繼續。

## 快速品味檢查

以代表圖和整批總覽檢查；明顯 generic 或成套重複時重做相關方向，其餘輕微問題可先完成批次再集中修正：

- 第一秒可否說出畫面有甚麼情緒或觀點？若只有「一包產品在白底」，失敗。
- 有沒有一個有意義的視覺張力：光／暗、尺度、動靜、材質、前後景或視角？
- 產品是否仍真實、清楚、主角沒有被裝飾搶走？
- 色彩、空間與光線有沒有把包裝變成畫面的一部分，而非硬貼上去？
- 文字有沒有與構圖共用節奏，而不是孤立在左上角？
- 成套圖片是否可由同一品牌拍出，但每張的貓、人、地點、鏡頭和動機不可重複？
- 與 Primary reference 並排縮小時，明暗、色塊、產品比例和資訊密度是否仍屬同一視覺家族？若 reference 明亮而輸出低調深色、reference 是分段詳情而輸出變成單張專櫃海報，直接判 `REFERENCE_DRIFT`。

## 失敗後的回復

用戶說「核突／普通／冇創意」時，不要求他先交設計 brief。先指出失敗屬於以下哪一類：缺乏情緒、構圖太 catalogue、產品與場景分離、文字像貼紙、參考不足、或 constraints 過度壓縮。再重選／重寫 Direction 和 Style Proof。原圖、logo、claim boundary 繼續保留；只放開 Creative Field。
