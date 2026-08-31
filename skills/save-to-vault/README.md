# Save to Vault

將一個已經做咗好多決定嘅 chatroom，整理成 Company Vault 入面可追溯、可覆核、唔會污染 canonical knowledge 嘅 business memory。

呢個 Skill 補上 AI Builder 工作流入面一個常見斷層：AI 完成任務之後，唔係靠人手 copy 成段對話，亦唔係乜都當「長期記憶」；而係先判斷邊啲係 source、owner decision、Project record、Learning signal、TBC 或純粹唔應該保存。

## 一句開始

```text
Use $save-to-vault。消化今個 chatroom，只保存對之後工作有用嘅內容去目前 Company Vault；完成後列出實際檔案、排除內容、Human Review 同下一步。
```

## 佢會做乜

```text
Current chatroom
→ 去重及解衝突
→ 分開 Fact／Decision／Observation／TBC
→ Privacy／secret gate
→ Route plan
→ 最小必要寫入
→ Read-back + receipt validation
```

常見 routes 包括：

- 未核實公司 source → Inbox／source receipt；
- 公司 fact → exact company knowledge candidate，等 source／owner gate；
- Project decision／artifact → 該 Project canonical file／output；
- substantial task → task／learning receipt；
- Human feedback／published evidence → 同一 Learning Loop receipt；
- 可重用方法 → candidate／proposed diff，唔會自動改規則；
- brainstorm、閒聊、重複或過期版本 → `NO_SAVE`。

## 最重要邊界

- 必須已有兼容 Company Vault；Skill 唔會自己創建一套新 Vault。
- 唔保存完整 raw transcript、system instructions、hidden reasoning、credentials、cookies 或不必要私人資料。
- 最新明確修正先係 active decision；舊版本標 superseded。
- 一次 feedback／一個結果唔會自動變成長期 rule。
- `saved` 唔等於 approved、Git pushed、synced、published 或 delivered。

## 驗證

Package 附帶零第三方 dependency 嘅 receipt validator：

```bash
python3 scripts/validate_save_receipt.py \
  --vault /path/to/YourCompany-Vault \
  --receipt 30-學習與優化/任務收據/YYYY-MM-DD-topic.md
```

Validator 檢查 receipt contract、安全相對路徑、實際 target 存在、基本 secret patterns 同 Vault root；Human Approval 仍然要由真正 owner 決定。

## AI Builder 對應

- Level 1：完成一條可 review workflow；
- Level 2：將工作方法同決定變成可重用 business memory；
- Level 3：用清楚 owner、source、approval、evidence 同 recovery，令記憶成為公司可管理嘅工作系統。

所以呢個 Skill 目的唔係「記得最多」，而係「只記得正確、可追溯、下一次真係用得返嘅嘢」。
