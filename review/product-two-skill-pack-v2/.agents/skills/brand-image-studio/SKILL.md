---
name: brand-image-studio
description: Turn product, service or hybrid-offer facts, reviewed references and customer voices into customer insights, detail-page blueprints, evidence-led images, posters and ad creatives with matching sales copy. Supports blueprint-only work and complete AI image production; does not rebuild understanding packs or operate ad accounts.
---

# 品牌詳情頁與廣告工作室
以已知產品、服務或混合方案的真相、客戶問題、品牌與參考的設計邏輯做可 review 的銷售素材。学生不用填 MD、貼檔名或知道內部模式。預設以快速批次完成草稿；正式交付才啟用完整驗收。

## 強制客戶對話關卡：逐步確認，不可跳過

每一個新詳情頁／廣告／活動視覺工作，**先問客戶，再做下一步。** 此規則優先於 Quick Batch、「直接完成」、「一次過」及任何預設張數；它不影響客戶已明確授權的 Send／Publish 等外部安全關卡。

**關卡 A｜銷售選擇。** 先讀交接包與已答資料，然後以一句已知內容加 1–4 條簡短問題，等候客戶答覆／確認。只問未答而會改變成品的項目：受眾／市場、第一個平台或交付物、最想賣的 offer／買家問題／CTA、指定或禁用的 Logo／品牌素材／視覺 reference／claim。若全部已答，仍要問「我理解為……，可否按此方向做文案與視覺？」。客戶可用自然短答，不需要填表。

**關卡 B｜文案與方向。** 只在關卡 A 確認後，才交候選 Direction 及完整對外文案／版式表。然後必須問客戶「方向同文案可以嗎？要改甚麼？」並等候答覆。未收到確認時，不能生圖、不能建立批次，也不能用 `draft_inferred` 代替確認。

**關卡 C｜成品 review。** 客戶確認關卡 B 後才可生成指定圖數；交圖後問客戶揀／修改／確認。除非客戶另行明確要求 Final QA，這個關卡只處理候選稿，絕不等同發布授權。

## 課堂引導模式：文案鎖定後才快速出整套圖

當學生說「上堂、先有文案、重新開始」時，讀 [classroom-dialogue.md](references/classroom-dialogue.md)。這個模式的目的不是多做文件，而是先讓學生看見 AI 理解的產品、買家和文字，再讓 AI 一夜批量出圖。所有缺口集中在一張開場選項卡；不逐題追問。

順序是：

1. **接 Offer 交接包**：只核對已知事實、用途、語言、Logo 和 reference，不能再問第一個 Skill 已答的題；先辨認 `product`、`service` 或 `hybrid`。
2. **選工作目標**：學生用一句說清楚要「詳情頁、廣告或兩樣」，平台／市場和最想賣的重點；缺項才一次問最多三題。
3. **先交方向**：有 Primary reference 時拆成一套可執行的 Design System；沒有時從產品包裝與品牌資料提出一套候選。學生只確認「似唔似我想要的視覺家族」，不做五格拼圖或五頁文字分析，除非明確要求比較。
4. **方向後必交完整文案與版式表**：在任何生圖前，先按已選方向寫 5 頁 Core Detail Pages（產品是 PDP；服務是服務介紹頁；用戶指定長詳情才寫 10 頁）及實際要求的廣告角度。每頁必須給學生看見：購買問題、headline、subheadline／body copy、3–4 個能被證據支持的資訊模組、閱讀順序、主畫面、產品位置或服務接觸點、CTA／買前提示及禁止 claim。這是可直接讀、改、排版的對外內容，不可只交 headline、chips 或藏在內部製作卡。
5. **一次合併確認**：學生只需要一次過指出方向或文案的錯誤、刪除項和主打重點；不用逐頁填內容。
6. **整圖模式**：文案和 Design System 已鎖後，逐圖用獨立製作卡生成已選數量；全套詳情未指定張數時預設 `5 張 Core Detail Pages`，不是 10 張。每張是一張獨立完整圖，絕不可生成多格總覽來交差。保留同一設計系統，但每頁按購買問題改構圖、場景和資訊密度。

「快速」是縮短已確認批次的人手等待，不是跳過客戶對話、產品真實性、文案和視覺方向。Quick Batch 只可在關卡 A 與關卡 B 均獲客戶確認後整批出圖；「直接完成」不構成豁免。

## 三種執行模式

- **Quick Batch（確認後預設）**：客戶在關卡 B 確認文案與視覺後，當他說「下一步／做晒／一次過／今晚做／大量出圖」或沒有要求逐張審批時使用。研究、藍圖和 Style Recipe 只準備一次；之後內部先看一張代表圖，沒有產品跑樣、錯 Logo、假 claim 或明顯不可讀文字便直接生成整批。獨立圖片可以並行，毋須每張停下等確認，也不為每張建立 request／hash／delivery JSON。
- **Review First**：只有用戶明確說「先試一張／每張俾我揀／A–E 比較」，或風格參考互相矛盾時使用。先交代表圖，再等方向。
- **Final QA**：只有用戶要求 final、正式上架、指定平台精確尺寸、交客或發布前驗收時使用。此時才讀 [output-contract.md](references/output-contract.md) 並跑完整尺寸、文字、Logo、hash 和 delivery checker。

Quick Batch 仍保留四個硬性檢查：同一 SKU、產品形狀、真 Logo、claim boundary。其餘品味、像素和細節問題集中在成套 review 或用戶指出時修正，不能把內部文件工作放在出圖前阻塞整批。

## Reference Match 優先

用戶只要提供一張或多張「想似呢種」的參考圖，本 Skill 預設進入 **Reference Match Mode**，優先級高過自由創作與三方向探索。用戶指明「呢張」時，那張就是唯一 Primary；其他圖只可補一項細節，不能混成新風格。

AI 先把長圖切成可讀 section、把 mood board 裁出指定格，再鎖定版面骨架、明暗、色彩比例、產品大小／位置、圖文密度、字級層次、分隔形狀、攝影光線及裝飾語法。每次生成都重新附 Primary reference 或相應 section crop；成品縮小看時要與 reference 屬同一視覺家族。產品原圖只替換 reference 內的商品，真 Logo 只替換原品牌識別，不能順手把亮色詳情頁改成黑藍專櫃、把高資訊頁改成極簡海報，或加入 reference 沒有的玻璃展台、霓虹、電影場景。Reference Match Mode 將明顯 `REFERENCE_DRIFT` 視為硬錯誤，代表圖未修正前不能開批次。

Reference Match 是學習視覺語言，不複製對方 Logo、商品、文案、價格、認證或專有插畫。若 reference 與產品真實性衝突，保留 reference 的構圖與節奏，改用受來源支持的產品角度，而不是另創一套美術方向。

### 預設批次大小

- 詳情頁未指定張數：5 張 Core Detail Pages。產品做產品認知、成分／材質、細節／質地、使用、規格／買前確認；服務做服務定位、客戶情境、方法／流程、交付／證據、方案／FAQ／CTA；每張要有完整可閱讀的內容層次。
- 廣告未指定張數：3 張不同動機廣告；用戶明確說「全套詳情＋廣告」時預設 5 張 Core PDP＋3 張廣告。
- 「10 張詳情／長 Shopify 頁／今晚大量出圖」才目標 10 張 PDP＋6 張廣告候選；6 張廣告至少分 3 個購買動機，每個動機 2 種不同構圖或場景。
- 只要詳情或只要廣告，就只生成該類；用戶已有指定數量永遠優先。
- 證據不足以支持目標張數時，先用不同購買問題、生活情境、特寫、用法、FAQ 及尺寸核對擴展；仍不足便減少張數並列明原因，不能重複同一句賣點或製造假資料湊數。

## Step 0：承接 Offer，而不是重新猜
先讀當前工作區與來源，按 [product-intake.md](references/product-intake.md) 接受 product-understanding-studio 的實際資料包，或用戶已有的等效原圖／服務資料／確認用途。此 Skill 不產出新的理解包；缺的產品或服務事實先列清，非依賴工作可繼續。
沿用已確認市場、語言、數量、比例及 reference。預設通用版，不把香港產品自動改成英文 Shopify。品牌／圖片資料只在實際出圖依賴時必需，Customer Insight 和文字藍圖可先做。

## 新手入口：AI 準備，用戶只需隨時糾正
最低輸入是產品原圖、服務 URL／一句用途，以及想要廣告／詳情圖。先讀交接內已答問題、特點轉譯表、Logo 與 reference；依關卡 A 僅追問會改變成品的缺口，最多四個簡短問題合併一輪。給出具體建議讓學生選，不問設計術語或要求他們建 MD。
- Offer 理解已有：沿用。缺資料先問並等待，再做可用文案和候選方向；不能把新手描述少等同已授權自行決定。
- 沒有風格參考：在關卡 A 清楚問客戶是否提供／指定參考；客戶確認可由 AI 自行設計後，才可提出 candidate Direction。白底產品相只作身份來源。
- 要公司風格但找不到真 Logo：指出缺的是哪個公司素材，先完成藍圖；不能偷偷省 Logo。用戶選只做產品品牌草稿時，可依產品包裝設計，不稱公司風格完成。
- 沒指定張數：按上面的預設批次大小直接執行；僅廣告或僅詳情就只做該項。十頁不能靠重複賣點或假資料填滿。
Review First 才要求逐張核對產品與代表圖；所有模式均須完成關卡 A 及關卡 B。內部研究、文案、頁序、工具記錄不逐份要求批准。「只要藍圖」及用戶指定其他停止點仍優先。

## 按用戶要求選出口
| 要求 | 行動與停止位置 |
| --- | --- |
| 分析 reviews／Q&A／客服問題 | 讀 customer-insights；交完整分析，停，不自動生圖 |
| 規劃 Shopify 10 頁／只要藍圖 | 讀 customer-insights（已有則核對）及 pdp-blueprint；交十頁完整藍圖，停，不調生圖工具 |
| 詳情圖／全套 | 藍圖 → Quick Batch 完成所要求批次；Review First 才出代表頁後停 |
| 做 Page 01／指定單張 | 只製作指定頁，不因預設批次大小擴成全套 |
| 單張產品海報／廣告 | 讀 creative-packs，選一個有證據的主張與場景，不強迫十頁 |
| 產品 gallery／listing／Meta／Google 素材 | 讀 creative-packs，只完成所要求的 pack |
| 既有內容的品牌圖、活動／服務海報、加 Logo／換尺寸 | 讀 source-and-style、[image-plan](references/image-plan.md)、native-images，沿現有素材做相應圖片；非實物不要求 Sheet |

所有 reference 連結見以下流程。不得把「只規劃」解讀成準備後自動出圖。

## 由客戶問題到圖像
1. 讀 [customer-insights.md](references/customer-insights.md)：客戶最在意 10 問、5 痛點、5 阻力、section 對應、禁止內容、1–10 優先級。每項保留來源與事實界線，不足就標候選，不編 reviews。
2. 讀 [reference-deconstruction.md](references/reference-deconstruction.md) 及 [source-and-style.md](references/source-and-style.md)：用戶提供 reference 要真看並進入 Reference Match Mode；長頁先裁成可讀 section，mood board 先選定單一格。品牌與 SKU 包裝配色只作身份適配，不能蓋過 Primary reference 的版式、亮度與資訊密度。沒有參考才使用 candidate 設計。
3. **先判斷交付類型並建立逐圖分鏡。** 讀 [image-storyboard.md](references/image-storyboard.md)，承接產品知識的七類資料覆蓋表，決定採用／合併／省略，再為實際要做的每張寫製作卡。七類是內容檢查，不是固定七張。沒有覆蓋表就從現有來源補最短對應，不重跑第一個 Skill。詳情頁（PDP）再讀 [pdp-blueprint.md](references/pdp-blueprint.md) 和 [product-detail.md](references/product-detail.md)，先寫每頁購買問題、完整對外內容和版式閱讀順序；只有這套內容完整才可生圖。不可把廣告 campaign 的 Style Proof 當成詳情頁第一頁。若產品 Form Lock 未被交接提供，由真原圖記錄已知形態；不能核實立體外形時只做 front-on 構圖。
4. **再讀 [creative-direction.md](references/creative-direction.md)**：已有 Primary reference 時只建立一個 Reference Match Direction，不另寫三個 style；沒有參考時先建立一個最合適 candidate，只有用戶要求比較才寫三個方向。Quick Batch 以一張內部代表圖校準後繼續；Review First 才停下讓用戶揀。PDP 代表圖必須有真正頁面資訊結構，而不是無字 mood image。
5. 圖像或配套文案讀 [creative-packs.md](references/creative-packs.md) 及 [design-brief.md](references/design-brief.md)。由已選 Direction 衍生三個角度／文案，不容許把所有 constraint 和所有資訊塞進第一張。若指定藍圖，只交藍圖。
6. 真正生圖讀 [native-images.md](references/native-images.md)，按 image-storyboard 的單圖任務規格，每次帶**原產品圖**、真 Logo 處理要求、Form Lock、相關已核對 Sheet／參考、當頁文案和已選 Direction。不得把整套分鏡或其他頁文案一起送進當次生圖指令。十頁是十張獨立圖，不拼成十格；Quick Batch 可按工具能力並行或連續生成，不能只交 prompt 冒充成品。
7. 按 [continuation-and-review.md](references/continuation-and-review.md) 處理「下一步」、「先試一張」、「A–E 五版本」、「直接完成」或 overnight batch。Quick Batch 只做硬性檢查和成套抽查；Final QA 才逐張完整驗收。當用戶說「唔靚／太普通／冇創意」，停止未開始的批次，回到 Creative Direction 修正。

## 誠實交付
輸出只寫實際已完成項。原圖不夠核實材質、規格或背面時換成受支持構圖，不能用生成圖補證據。廣告 creative 是待測試假設，不代表有效投放。
此 Skill 可寫配套 listing／ad copy，但不接管獨立 SEO Blog、廣告受眾／預算策略、數據／CRM、發送、網站組裝或投放。原有獨立數據 Skill 可讀 content_id／campaign_id 對回素材；沒有真 ad_id 就不虛構。
