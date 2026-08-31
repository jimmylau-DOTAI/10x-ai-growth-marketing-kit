---
name: save-to-vault
description: Digest the active chatroom and safely route durable, source-backed information into an existing Company Vault. Use when the user says save to vault, 記低, 存入 Vault, or asks to turn the current conversation into company knowledge, a project record, or a Learning Loop signal. Do not use to dump raw chats, create a new Vault, or auto-approve facts, rules, or Skills.
metadata:
  status: team-test
  scope: existing-company-vault-only
  receipt_version: "1.0"
---

# Save to Vault

將一次對話變成可追溯嘅 business memory，而唔係將成個 chatroom 原封不動塞入 Vault。只保存對未來工作有用、來源同狀態清楚、由正確位置負責嘅內容。

## Start gate

1. 找到包含 `AGENTS.md` 同 `INDEX.md` 嘅現有 Vault root。先讀兩份檔；唔好掃晒成個 Vault。
2. 找唔到 root 就停止並回報 `VAULT_ROOT_REQUIRED`；唔好自行建立資料夾架構。
3. 「save to vault／記低落 Vault」只授權今次在該 Vault 內作最小必要寫入。唔授權 Send、Publish、Deploy、Schedule、Git push、改 CRM，亦唔代表批准公司事實、規則或 Skill。
4. 如路由去一個正式 Project，先讀最近一層 `AGENTS.md` 同 `README.md`。缺檔時按 Vault 規則停止，唔好估。

## Distil the chatroom

以今次 active conversation 做 source。最新明確修正取代舊版本；舊內容只保留為必要 provenance，唔可以同時當 active requirement。

只抽取以下類別：

- owner-provided facts 或 source；
- 已明確作出嘅決定、scope、acceptance criteria；
- Project artifact、進度、結果或 next action；
- 對 substantial artifact 嘅具體 Human feedback；
- 有來源嘅 published／performance evidence；
- 可能可重用、但仍需 Learning Loop 證明嘅方法候選；
- `TBC／OPEN／BLOCKED`；
- 應排除嘅閒聊、重複、過期內容、工具噪音及敏感資料。

唔好保存 system/developer instructions、hidden reasoning、credentials、cookies、tokens、私人識別資料，亦唔好捏造不存在嘅 turn ID。冇穩定 task/thread ID 時寫 `current-chatroom`。

## Route before writing

寫入前先 duplicate-check exact target，然後顯示一個短 route plan：`item → class → target → action → review state`。

詳細分類只在需要時讀 [Routing contract](references/routing-contract.md)。核心界線：

- 原始公司 source／未核實 facts：先入 Inbox／source receipt；如已安裝，交俾 `company-vault-builder` 處理，唔直接改 approved company knowledge。
- Project 決定、artifact 或結果：寫入該 Project 最細嘅 canonical file／output receipt。
- 非 Project substantial 工作：寫中央 task receipt。
- 完成品、具體 feedback 或 published evidence：如已安裝，使用 `company-vault-learning-loop` 嘅對應 mode；一次 signal 唔會自動改規則。
- 可重用方法：先記 receipt／candidate；未有今次 Human Approval，唔改 `AGENTS.md`、`SKILL.md`、TONE、DESIGN、QA 或 approved knowledge。
- 只屬今次 wording、brainstorm 或普通問答：`NO_SAVE`。

如果兩個 canonical destinations 都合理，而選擇會改變公司真相、future rule、privacy 或 owner，問一條問題後停在 `ROUTE_REVIEW_REQUIRED`。否則用最保守 route 寫入，唔為咗問問題而阻塞安全嘅 Inbox／receipt 保存。

## Write the smallest durable record

1. 每個 item 只設一個 artifact owner；更新現有檔優先於建立重複檔。
2. 分開 `FACT／OWNER_DECISION／OBSERVATION／INTERPRETATION／TBC`，並保留 source、date、owner、privacy、review state。
3. 保存 active decisions 同結論；唔複製完整 transcript。需要 audit trail 時只用短 paraphrase 加 source reference。
4. 使用 Vault 現有 template；冇合適 template先複製 [Save receipt template](assets/save-receipt.md)。詳細欄位見 [Receipt contract](references/receipt-contract.md)。
5. Canonical write 缺 current source、owner 或 approval 時，改寫為 candidate／source receipt，狀態設 `needs_human_review`。
6. 不覆蓋 unrelated user changes；如 exact target 有未預期修改，停止並展示衝突。

## Verify and report

完成後逐一 read back 實際檔案。使用 package receipt 時執行：

```bash
python3 PATH_TO_SKILL/scripts/validate_save_receipt.py \
  --vault PATH_TO_VAULT \
  --receipt RELATIVE_RECEIPT_PATH
```

Validator 只證明 receipt 結構、路徑同基本 secret gate；唔證明內容已獲 Human Approval。

最終只可使用以下狀態之一：

- `SAVED_TO_VAULT`：所有寫入已 read back，冇 canonical approval 缺口；
- `SAVED_WITH_REVIEW_REQUIRED`：安全 receipt／candidate 已保存，但有 owner 或 Human Review 待處理；
- `ROUTE_REVIEW_REQUIRED`：未寫入，等一個會實質改變 destination 嘅答案；
- `NO_DURABLE_INFORMATION`：今次對話冇值得保存嘅 durable item；
- `VAULT_ROOT_REQUIRED`：未找到兼容 Vault。

回報順序：Vault root、chat scope、route decisions、實際 files／actions、排除內容、validation/read-back、Human Review、owner、下一步。唔好將 local save 說成 Git push、sync、publish 或 delivery。
