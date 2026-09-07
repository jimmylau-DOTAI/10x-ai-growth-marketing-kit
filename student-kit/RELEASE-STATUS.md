# Release status

LOCAL_CANDIDATE — not released.

2026-09-08 v0.4.4：已同步 `product-understanding-studio` 與 `brand-image-studio` 的 v2.5 產品／服務分支。共用順序為確認任務、理解確認、必要視覺核對、風格與完整文案確認、製作及 review；產品按畫面核對外觀／操作，服務核對範圍／流程／交付。理解預覽不固定數量，單張廣告不展開詳情頁。兩個 Skill 及所有可到達 references 已通過靜態連結和 quick validation；尚未在 clean student environment、真產品或真服務上 runtime 測試，未重打學生 ZIP，亦未正式發放。

學生包結構／回歸測試已通過；完整 AI 試圖已真正生成。
阻礙正式圖像交付：當前工具兩次均未達指定 4:5／1080×1350，一次 targeted retry 已完成。需要可控制比例的真實 image tool／設定再測。
尚待：人類審美 review、4-card continuity／正確 4:5 尺寸、SEO banner、Threads Draft、clean student environment、Windows 驗證。

圖片示例係 preview，唔係合格 export。所有私人 Style 原始 reference 不在此包內；沒有 Publish／Push／正式發放。

2026-09-05 v0.2：加入 mandatory Skill-first routing 及 ai-social-image-maker 修改後驗收。15 個新 gate 測試通過；原 pilot／retry／Logo edit 的真實檔案全部被尺寸 gate 擋住。這是修正驗收，不代表三張圖片已修好。新 task 是否讀取本地 routing 尚待 clean-environment 驗證。

2026-09-05 v0.3：出圖前需求檢查、不清楚先問尺寸；按任務選可用 native 模式並實際 call。移除跨平台固定 1080×1350，保留本課已批准 Carousel 要求。Delivery schema 2 綁定 request。此輪是 Skill／驗證程式修訂，沒有新圖生成或新 provider 能力實測；v0.2 歷史 receipt 保留原版本。

2026-09-05 v0.3.1：修正 `STUDENT-KIT.json` 漏列 `meta-ads-results-review` 同 `utm-link-builder`。Manifest、實際 folders 同 Marketing Skills ZIP 而家同為 12 個，全部 12 個 `SKILL.md` quick validation 通過；未代表 clean student environment 已安裝或自然語言觸發已實測。
