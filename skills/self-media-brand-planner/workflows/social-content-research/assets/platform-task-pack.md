# Platform Task Pack｜[Campaign／主題]

## 全部 Task 共用根據

- Source Guide：`SOURCE-GUIDE.md`
- Content Brief：`post-brief.md`
- Audience：
- One point：
- CTA：
- 方向預覽：以輪播為主時，由 IG 主 Task 先交 A／B／C；兩個延伸 Task 各交 Banner、Threads A／B／C，選定後才製作
- 進度回報：而家做到邊／用緊邊個 Skill／已交乜／下一步等你乜
- 可講／不可講：沿用 Content Brief；唔可自行補充公司成果、數字或 Offer。

沿用已確認且無實質改動嘅共同根據；新建或實質修改先 Review。用戶要求建立 Tasks 時，由系統按 `references/task-dispatch.md` 真正派工，本檔由 AI 管理，唔要求用戶逐張貼卡。每個 Task 只寫自己 output folder；需要改共同內容時，返回 Brief 由人確認。

## 任務清單（由實際工具結果更新）

- 共用輸入版本／hash：
- 最近核對時間：
- 建立授權：用戶原意／範圍

| 工作 | Owner／實際 Task ID | sidebar | 實讀 Skill 路徑 | 狀態及成果／QA | 待用戶決定 |
| --- | --- | --- | --- | --- | --- |
| IG Carousel | 主 Task | 當前主對話 | 未核對 | 準備中／未產生 | — |
| SEO Banner | 分支 Task／未建立 | 未核對 | 未核對 | 準備中／未產生 | — |
| Threads | 分支 Task／未建立 | 未核對 | 未核對 | 準備中／未產生 | — |

下列係主 Task 同兩個分支嘅製作要求。每個 owner 先驗證能讀共同輸入、相同版本及實際 package-local Skill 正文；讀不到就回報交接缺口，不能靠 Task 名稱或 prompt 入面嘅 Skill 名開工。

## 主 Task｜IG Carousel

- Primary Skill：`instagram-carousel-studio`，出圖時接 `ai-social-image-maker`
- 讀取：共用 Source Guide、Content Brief、現有 Style／brand 資料
- Deliverable：指定卡數 Carousel、Caption、第一張圖 Review，再完成其餘圖片
- Output：`outputs/ig-carousel/`
- Review：先交故事角度與畫面方向，等 IG 選擇；再睇首圖同完整內容，確認後做其餘卡；唔發布

## 分支 Task 1｜SEO Banner

- Primary Skill：`ai-social-image-maker`
- 讀取：共用 Source Guide、Content Brief、Blog 標題、網站 target size、現有 Style／brand 資料
- Deliverable：一張完整 AI SEO Banner，文字、品牌、尺寸 QA
- Output：`outputs/seo-banner/`
- Review：先交標題／構圖／風格方向，等 Banner 選擇才生成；再打開實圖，唔假稱已 upload 到網站

## 分支 Task 2｜Threads Post

- Primary Skill：`hk-threads-writer`
- 讀取：共用 Source Guide、Content Brief、香港語氣／品牌資料
- Deliverable：一篇自然廣東話 Threads Draft，連同 source boundary 同字數 receipt
- Output：`outputs/threads/`
- Review：先交切入／語氣方向及一句開頭，等 Threads 選擇才寫全文；唔發布，link／CTA 未確認時保留 TBC
