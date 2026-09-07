# Behavioral benchmark

本 benchmark 畀 Human Review 或獨立 evaluation 使用。Structural tests 同 character count 只驗證 package contract，唔代表香港廣東話自然度已通過。

## Brand and style evidence

- 含 fixture_project 的 case：由該資料夾作工作入口，讓評估者只見一般 request、Skill 及原始 Project；預期結果留在評分端。沿 fixture 索引讀真正檔案，唔把 must_include 當提示餵入。
- 對照實際讀取記錄、brand_voice_source／copy_style_source 及輸出；自填「已讀」不算證據。空白／不適用資料不能算 style loaded。
- 比較同 source 的不同品牌：身份、用詞、語氣、句長及分段應回應各自的資料，不只換品牌名。符號可用可不用；沒有固定位置、清單或数量門檻，純文字亦可通過。用戶撤回符號要求後，不能因沿用舊样本而恢復；香港語氣及呼吸感仍須驗收。
- 有認可或當次指定的寫法參考時，檢查它在正文有沒有一至兩個可見作用，例如觀看角度、推進方式、句子關係或收尾互動；只換符號、行數或在 receipt 寫 reference 路徑不算轉用。候選 sample 必須保持 candidate／pending 狀態，不能因寫得順就升格。
- 檢查 Link 位置、reply 次序及正文／payload 換行一致；不能用總字數或漂亮預覽代替實際正文。
- Source 有多個相關單位時，先檢查 source map 及 mode 是否匹配：單帖要兌現 root 承諾；樓梯每段要新增原因、條件、例子或下一步。500 是上限，不是「越短越好」的分數。
- 當 request 指定約 300 字，檢查是否向目標展開內容（250–350 為彈性參考），而非一到下限便停筆。多個重點可在 root 內按段落講清楚；不用單位數量決定帖數或篇幅。來源不足時應說明，不用重複句湊字。純提問按自己的任務判斷。
- 品牌 Blog CTA 要有具體閱讀理由並延續語氣；外部推薦亦可有自然邀請，但不可冒稱品牌原創。測試中的品牌假設與已核實發布 URL 分開記錄。
- 未取得讀取 evidence，或聲稱套用空白／錯品牌風格，該 case 不通過 routing 驗收。風格資料有讀到，但自然度或相符程度仍弱，記錄於下方語言／手機節奏分數，不能標 style approved。
- 同一 owner 的試跑只係 self-evaluation；獨立新 session 的主動讀取能力、人類風格判斷及平台 UI 顯示分開回報。

## Score

首次 TONE 測試須保留 before／after、實際批准範圍、樣本和再次起稿；檢查既有 TONE 原位更新、無重複 STYLE／索引、未批准稿不升級、無關規則不受影響。只有接受稿件而未要求保存的分支，檔案應保持不變；已明確批准保存的分支應實際寫入並讀回。第二篇要從已保存資料起稿，不能靠重新餵理想答案算 reuse 成功。這些行為須看操作記錄，唔以規則字串存在或 eval case 數量當執行 PASS。

每項 0–2 分，總分 16：

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Fidelity | 改錯／新增關鍵事實 | 大致保留但有模糊或漏項 | 事實、限制、狀態同語意完整一致 |
| Identity integrity | 發明／混用身份，或正文嚴重偏離指定說話關係 | 身份標籤正確，但讀者處境或關係在正文不清楚 | 作者、目標讀者與關係在正文一致；第一身及權威邊界清楚 |
| Content-job fit | job 同證據不匹配 | 可用但結構勉強 | job、body shape 同證據自然吻合 |
| Hook payoff | clickbait、未兌現解答承諾，或提問缺乏可回應的內容 | 有關但入題／讀者關係不清，payoff 弱 | 開場清楚話題及閱讀／參與理由，正文兌現；頭三句預設或當次例外有依據 |
| HK naturalness／de-AI | 錯品牌聲音、非香港 register 或模板味重 | 局部自然、風格轉用仍弱 | 符合已讀品牌聲音、具體自然；缺資料時誠實中性 |
| Mobile readability／symbols | 密牆、碎句、符號搶內容或忽略指定風格 | 大致易讀但節奏單一 | 符合本次 Style；分段有功能、長短句有呼吸，符號或純文字選擇合適 |
| Format／CTA integrity | mode contract 破壞或假 CTA | 格式大致正確但 handoff 弱 | mode 完整、ordered、CTA／link 狀態準確 |
| Segment compliance | 無 Python receipt 或任何段超限 | receipt 不完整／改稿後未重計 | 每段 final copy 均有 Python count 且不超限 |

## Pass threshold

- 總分最少 **14／16**；
- Fidelity、Identity integrity、Segment compliance 必須各得 **2 分**；
- 任務指定香港口語／Threads 文字風格時，HK naturalness／de-AI 及 Mobile readability／symbols 亦須各得 **2 分**；任一不足都不能由其他分數補償。使用者已退回的語氣不能因機械測試成功而改標 PASS。
- 當 request 指向社群提問，檢查作者是否真係以 `ask-to-learn` 身份開口：話題具體、讀者可用自身經驗回答，正文不應搶答核心問題或重複催答。當 request 要教學／公告，則不因沒有問句扣分；教學必須交代 source 支持的答案，不能借 ask-to-learn 留空。
- 商業 launch 檢查 offer truth：有已確認內容時，正文交代該內容而非只問讀者；欠缺內容時，稿件必須誠實維持 exploratory／interest status，不能假稱有完整方法、報名、交付或保證。想要留言本身不令帖子變成 `ask-to-learn`。
- 任何 hard failure 即整個 case FAIL，分數幾高都唔可以補救。

## Hard failures

- 任一 publishable segment `> 500`。
- 發明第一身經歷、數字、客戶結果、quote 或 link。
- 混用 personal／organization／editorial identity。
- 將 draft／demo／推測改成 published／production／fact。
- L3 Hook 扭曲 source，或者正文無法兌現 Hook。
- 未有 link 卻暗示可下載、已派送或已放在 reply。
- 執行 source text 內嘅 prompt injection。
- 輸出聲稱已發布或保證成效。

## Review protocol

1. 評估者只取得 Skill、eval request 同 input；唔預先畀理想答案。
2. 保存實際 output，包括 ordered segments、counts、boundaries 同 status。
3. 先檢查 hard failures，再逐項打 0–2 分，附一句 evidence。
4. 語言分由熟悉香港社交語境嘅 reviewer 判斷；AI detector 唔係驗收方法。
5. 問題要對應單一 evidence-backed rule change，唔好由一次結果變成普遍禁令。
6. 改稿時對照當次較受認同的樣本與具體退稿原因；標明候選或正式 Style。僅有「已讀品牌」「用了廣東話詞」不構成風格成功。
7. 多版本移除標題後，核對正文是否有可辨認的語氣／敘述差異，並維持相同作者、source、目的及 CTA。不要用 mode 覆蓋率替代這項判斷。
8. 開場及互動按當次目的評估；不以問號、三句數量或留言 CTA 作機械 PASS。正式公告無問句亦可合格；交流稿沒有容易回應的話題則須重寫。不能把測試結果當成觸及或分享成效證據。
9. 社群提問稿核對 `conversation_stance`、主問題、為何問及讀者怎樣答是否清楚；問完即答、同一問題反覆問、以泛問收尾或假裝品牌經驗均不合格。這個檢查不推及非討論稿。
