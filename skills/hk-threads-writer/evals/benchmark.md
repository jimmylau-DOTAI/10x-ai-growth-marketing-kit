# Behavioral benchmark

本 benchmark 畀 Human Review 或獨立 evaluation 使用。Structural tests 同 character count 只驗證 package contract，唔代表香港廣東話自然度已通過。

## Score

每項 0–2 分，總分 16：

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Fidelity | 改錯／新增關鍵事實 | 大致保留但有模糊或漏項 | 事實、限制、狀態同語意完整一致 |
| Identity integrity | 發明或混用身份 | 身份含糊但無明顯虛構 | 作者／組織／editorial 邊界清楚 |
| Content-job fit | job 同證據不匹配 | 可用但結構勉強 | job、body shape 同證據自然吻合 |
| Hook payoff | clickbait 或正文無回答 | 有關但 payoff 弱 | Hook 有吸引力且正文完整兌現 |
| HK naturalness／de-AI | 非香港 register 或模板味重 | 局部自然、仍有機械痕跡 | 香港口語自然、具體、無刻意 cosplay |
| Mobile readability／symbols | 密牆、碎句或符號濫用 | 大致易讀但節奏單一 | 段落有功能、長短句有呼吸、符號克制 |
| Format／CTA integrity | mode contract 破壞或假 CTA | 格式大致正確但 handoff 弱 | mode 完整、ordered、CTA／link 狀態準確 |
| Segment compliance | 無 Python receipt 或任何段超限 | receipt 不完整／改稿後未重計 | 每段 final copy 均有 Python count 且不超限 |

## Pass threshold

- 總分最少 **14／16**；
- Fidelity、Identity integrity、Segment compliance 必須各得 **2 分**；
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
