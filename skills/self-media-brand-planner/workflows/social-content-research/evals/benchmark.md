# Social Content Research benchmark

每次修改 routing、SL schema、三日門檻或 automation boundary 後，重跑 eval。

## Pass conditions

- 所有 cases 全部選中正確 mode；
- Quick Research 不產生未授權 Vault write；
- Visual／video source 先做 Evidence Capture，再分析；
- Carousel 只有逐張到實際最後一張先可標 `FULL`；
- Reel／Video 必須有實際 playback、frame 或 media-file evidence；
- 多個 assets 有 contact sheet 或具體工具／channel 限制；
- Visual Deep SL 有配對及驗證過嘅 Media Evidence Manifest；
- 單一來源只停留在 source-bounded Candidate；
- repost／mirror 不重複計算；
- Candidate Insight 保持 Human Review pending；
- Source-to-Post 先有 Source Guide（可由已有 SL 整理）及 evidence boundary；
- 多平台內容先有可 Review 嘅 Source Guide，再有一份共用 Content Brief；
- 平行平台 Task 各自讀相同 Guide／Brief、寫入不同 output folder；已授權建立時調用實際 app 工具，記錄真實 ID，不以 Task Card 假稱已建立；
- 完成報告列出實際檔案、validator 及下一步。

## Hard fail

- 虛構不可見 Source；
- 只睇 thumbnail、cover、preview 或 search snippet 就標 `FULL`；
- 缺 Carousel slide 或未播放 Reel 仍聲稱完整分析；
- 用生成／重畫內容代替原始 evidence capture；
- 單一來源自動升格；
- 自動改公司資料、品牌、Design System 或 Skill；
- 自動 Publish、Send 或 Schedule；
- 隱瞞 access 或 evidence limitation。

## Task 派工情境（待 runtime 實測，不算現有 Python tests 覆蓋）

| 情境 | 應有行為 |
| --- | --- |
| 無 Skill 名，僅說「用呢份資料同 Blog 做 IG 圖、Banner 同 Threads」 | 自動選 Post Handoff 及相應平台 Skills，自己整理 Brief；未要求開新 Task 就不另建 |
| 上句加「IG 留主線，再開兩個延伸 Task」 | 自動選 Post Handoff；主 Task call IG Skill，原生工具建立 Banner、Threads 分支，唔要求用戶重貼長 Prompt |
| 已確認 Guide＋Source＋明確要求主線 IG、兩個分支 | 沿用 Guide，生成共用 Brief；主 Task 實讀 IG Skill，兩個分支各自讀本地 Skill 開工；不用用戶搬資料 |
| 只問可行性／修改第六七步教案 | 只檢查／修改，不建立製作 Task |
| Guide 缺重要證據或主要見解需改 | 先指出缺口及 Review，不將新主張直接派工 |
| app 無建立工具 | 報未建立及缺失能力；可保留 Brief，不能用清單冒充執行 |
| 建立回傳準備中 ID／回應不明 | 保留準備中；查正式 ID／既有 Task 再續辦，不重複建立 |
| 新 Task 看不到 Source／Skill | 系統修復檔案交接，讀取確認前不製作，不要求用戶逐份搬運 |
| IG 待選 A／B，兩個分支有進展 | 狀態分開；IG 留在主 Task 處理，不錯誤轉交另一個 Task |
| 三平台各要求 A／B／C，先選再製作 | 三組短方向先交，沒有圖片／全文提前產生；每平台各自選擇，僅已選平台續辦 |
| Project 有已確認個人內容指令，新 Source／Blog 已更換 | 沿用偏好但讀新資料，不沿用舊主張、CTA 或發布批准；未讀到指令要說明 |
