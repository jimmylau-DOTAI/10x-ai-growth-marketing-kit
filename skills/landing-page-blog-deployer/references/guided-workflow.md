# Guided Student Workflow

## Purpose

學生只需要一次啟動 Skill，之後用自然短答完成工作。Agent 負責讀現況、保存決定、顯示進度、執行安全步驟同帶住修復，唔應該要求學生逐段複製技術 prompts。

## First response contract

第一個回應要：

1. 用一句說明今次結果；
2. read-only 檢查 project 同現有 artifacts；
3. 顯示 `已找到／仍欠／下一步`；
4. 可以安全繼續就直接做；
5. 只有缺少一個會實質改變結果嘅決定時，先問一條問題。

避免先問 framework、package manager、route convention 等可以由 repo 發現嘅技術問題。

## Persistent state

Project root 使用 `site-deployment-state.json`。如果已有 equivalent state file，沿用並 map 欄位，不建立競爭版本。

每次完成 gate 後更新：

- `current_phase`；
- `status`；
- `completed_gates`；
- `approved_decisions`；
- `artifacts`；
- `blocked_items`；
- `external_actions`；
- `next_action`；
- `updated_at`。

Secret 只記 variable name 同 presence status。禁止保存 value。

## One-question loop

問題只可以處理目前最早一個會改變結果嘅缺口。格式保持短：

```text
而家已完成：Landing Page handoff、Blog article handoff
下一步：確認 Blog CTA 去邊度
建議：沿用 Landing Page 嘅 #lead-form，保持同一轉化目的
問題：確認沿用呢個 CTA 嗎？
```

用戶回答後：

1. 保存答案；
2. 回讀你理解嘅決定；
3. 執行因此解鎖嘅安全步驟；
4. 顯示新進度；
5. 如仍有關鍵缺口，先問下一條。

不要每一小步都要求確認。只有產品方向、公開內容、資料處理、成本、外部 mutation 或 Human Review gate 需要停低。

## Resume rules

- State 同 repository evidence 一致：由 `next_action` 繼續。
- State 落後，但 artifacts／tests 證明已完成：更新 state，唔重做。
- State 聲稱完成，但 artifact／destination 無證據：降級相關 gate，保留其他通過項。
- 無 state：建立 inventory，重建最小 state，唔覆蓋 existing files。
- 多個 candidate projects：列出 evidence，同時推薦最可能 target，只問一次選擇。

## Recovery map

| Symptom | First action | Safe recovery | Stop when |
| --- | --- | --- | --- |
| Landing handoff missing | Search approved brief／page／receipt | Build a draft handoff with gaps | Offer、CTA、form use remains ambiguous |
| Blog handoff missing | Search approved article pack／HTML／slug | Build a draft handoff with gaps | Article approval or CTA is unknown |
| Build fails | Read first actionable error and package scripts | Make smallest scoped fix, rerun failed gate | Fix changes stack or public behaviour |
| Route conflicts | Inventory actual routes and redirects | Preserve existing public route, choose non-conflicting map | Redirect/domain decision is needed |
| UTM disappears | Trace entry, storage and form payload | Repair first-touch capture and add regression test | Consent/data policy would change |
| Form returns ambiguous result | Check destination by unique marker | Record result or one controlled retry only when no write occurred | Destination cannot be read |
| Vercel deploy times out | Inspect deployment list and logs | Reuse or diagnose existing deployment | State remains ambiguous after read-back |
| Secret missing | Report variable name only | Give provider-specific placement instruction | User/provider must supply access |

## Progress receipt

每次停低只交最少而足夠嘅狀態：

```text
Current phase:
Status:
Completed:
Preserved:
Blocked item:
Next action:
Approval needed:
```

唔好用大量技術輸出淹沒初學者。完整 logs 留在 artifact，回應只解釋 actionable result。
