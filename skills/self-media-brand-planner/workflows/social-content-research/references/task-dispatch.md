# IG 主線＋三個延伸平台 Tasks

本流程供 AI 執行。當交付以 IG Carousel 為主；IG 留在主 Task，Blog Banner、Threads、Reels 才分支。清單係進度總覽，真正建立分支必須調用當前 app 工具。

## 1. 開工範圍

- 「主線做 IG，再同步做 Banner、Threads 同 Reels」授權主 Task 開始 IG Draft，並建立三個延伸 Task。
- 「教我點開／修改教案／做唔做到」只回答或修訂材料，不建立 Task。
- Draft 不包括 Publish、Deploy、Send、Schedule、CRM write 或正式品牌規則更新。

## 2. 共用輸入

先核對 `SOURCE-GUIDE.md`、原始 Source、Blog、`post-brief.md`、品牌 Style 同 CTA，記錄路徑及版本。主 Task 與三個分支共用同一版，任何一邊都不能自行改共同事實、見解、CTA 或 Style。

避免重複建立：先查現有 Task ID；已有就續辦。每個 owner 只寫自己的 output folder。

## 3. 主 Task 先做 IG Carousel

主 Task 必須依次完成以下開工證據，先可標示「IG 進行中」：

1. 讀用戶 Project `AGENTS.md`、Vault `INDEX.md`、`SKILL-ROUTING.md`；
2. 實際打開 package-local `instagram-carousel-studio/METHOD.md` 及該階段必要 references；
3. 用一句人話回報：「今次用 instagram-carousel-studio 做四張 IG Carousel 內容同 Caption」；
4. 交 A／B／C 三個故事與畫面方向，等用戶揀；
5. 揀定後先做完整逐卡內容；出圖前再實際打開 `ai-social-image-maker/METHOD.md`，先交 C01 實圖，確認後完成 C02–C04；
6. 回報實際 Skill 路徑、成果路徑、QA、限制同下一步。

只喺 prompt 寫 Skill 名、只交出圖 prompt、或只建立一行清單，都不算 call 過 Skill。

## 4. 建立三個延伸 Task

先發現當前工具：查 Project、建立 Task、移入 sidebar section、讀狀態、傳續辦指令。以實際 schema 為準。

每個分支 prompt 必須包括：

1. 可讀嘅共用資料路徑及 output folder；
2. 先讀用戶 Project `AGENTS.md`、Vault `INDEX.md`、`SKILL-ROUTING.md`；
3. Banner 實讀 `ai-social-image-maker/METHOD.md`；Threads 實讀 `hk-brand-threads/SKILL.md`；Reels 先實讀 `reels-text-storyboard/METHOD.md`；
4. 先回報已讀 Skill 實際路徑，再交 A／B／C 方向；未讀到就標受阻，不能直接製作；
5. 選定方向後才製作 Draft，完成時回傳成果、QA、限制及下一步。

建立成功後，將三個分支加入今堂 Project 所在 sidebar section，再用 `list_threads` 核對。只有真實 `threadId`／`hostId` 先記「已建立」；projectless、未入 section 或只得準備中狀態都要如實標示。

Banner 尺寸由網站版位決定，不能套用 IG 尺寸。Threads 用香港廣東話。Reels 先產生 60–75 秒文字分鏡；用戶確認文字並要求 HTML 後才交 `reels-html-storyboard`。只有用戶確認 HTML 並要求繼續後，才由 `remotion-reel-scene` 檢查 Node／npm、安裝 Remotion 並做一段 Studio 預覽 Scene。已有 Style 就沿用；只有拆新參考才用 `image-style-lab`。

## 5. 排程與清單

三個分支建立後可同步整理方向；主 Task 繼續 IG，不等待分支完成。示範 Review 次序固定：

`IG 三方向 → 揀 IG → C01 實圖 → C02–C04＋Caption → Banner → Threads → Reels HTML 分鏡 → Remotion Scene 01`

清單每次工具返回後更新：工作、owner、Task ID、sidebar 位置、實讀 Skill 路徑、進度、成果／QA、下一個決定。狀態只用有證據嘅「準備中／進行中／等你確認／完成／受阻」。

對用戶只展示：而家做到邊、用緊邊個 Skill、已交乜、下一步等你乜。主 Task 未完成四張可開啟 IG 圖及 Caption QA，不可因 Banner／Threads／Reels 完成而宣稱主線完成。
