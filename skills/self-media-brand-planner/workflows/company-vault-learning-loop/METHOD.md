---
name: company-vault-learning-loop
description: Close out a substantial Company Vault deliverable, record explicit human feedback or published evidence, triage repeated learning signals when due, and apply one human-approved bounded rule update. Use when a real artifact is ready, the user says 完成 or 搞掂 or 記低, gives concrete likes/dislikes/results, asks to review learning, or LOOP-STATE says triage is due. Do not use for unfinished drafts, tiny edits, general questions, or a standalone OK/try.
metadata:
  status: user-release
  scope: current-company-vault-only
  receipt_version: "1.0"
---

# Company Vault Learning Loop

同一個 Skill 負責 closeout、feedback、published review、三日 triage 及已批准更新。佢唔係 production Skill，亦唔會因一次 feedback 自動改規則。

## 先揀一個 mode

### 1｜delivery-closeout

只在 substantial deliverable 準備交付時使用：完整 Post／Carousel／Deck／Proposal／Blog／Campaign asset，或有明確 done definition 的公司工作。普通問答、未完成 draft、細微改字唔記錄。

1. 確認 final artifact path、source／brief、production Skill、Style／Reference 及精確 QA receipt。
2. Project 任務寫入 `20-Projects/<project>/outputs/<task>/LEARNING.md`；非 Project 任務寫入 `30-學習與優化/任務收據/YYYY-MM-DD-topic.md`。
3. 使用 [Receipt schema](references/receipt-schema.md)。未收到 Human feedback 時：
   - `status: awaiting_human_feedback`
   - `human_review: pending`
   - `signal_type: none`
   - `candidate_key: none`
   - `evidence_count: 0`
4. 有平台時，在該平台 `04-實戰案例與學習/INDEX.md` 只新增或更新一行連結；唔複製 receipt。
5. 驗證 receipt；回報 `LEARNING_CLOSEOUT_RECORDED`。呢個狀態唔代表成功規則。

### 2｜human-feedback

用戶對 substantial artifact 提供具體評價、修改原因、喜惡，或明確要求「記低」時：

1. 找回同一 artifact 的 receipt；先用 artifact path／date／topic duplicate-check。
2. 保存用戶原意，分開 `preference | quality | workflow | performance | commercial`；唔將 AI 推測寫成 Human feedback。
3. 寫 `Observation → Insight → Hypothesis → Decision`；Hypothesis 只改一個 bounded variable。
4. 同一 `platform＋format＋objective＋bounded hypothesis` 使用同一 `candidate_key`。
5. 更新 `LOOP-STATE.md` 的 `last_receipt_at`、`pending_signals`；如 `next_triage_due: TBC`，設為本次日期後三日。
6. 驗證及 read-back；回報 `LEARNING_SIGNAL_RECORDED`。

單獨「OK／try」、禮貌回覆、冇原因的「幾好」、未完成 draft 及微小改字唔建立 signal；有需要只更新 task state。

### 3｜published-review

只有已發布 artifact 到達 review window，而且有 URL／平台後台／商業證據時使用：

1. 先 read-back live URL 或記錄 backend evidence 的 precise source。
2. Public、backend、commercial evidence 分開；留言不可推算 DM、lead 或 sale。
3. 更新同一 receipt；缺失資料寫 `none／無法判斷`。
4. 將 performance／commercial signal 加入候選，但唔自行宣告成功。

### 4｜triage

先執行：

```bash
python3 .agents/skills/company-vault-learning-loop/scripts/check_triage_due.py --state 30-學習與優化/LOOP-STATE.md
```

- `TRIAGE_NOT_DUE`／`TRIAGE_NOT_SCHEDULED`：停止，唔讀 receipts。
- `TRIAGE_DUE`，或用戶今次明確要求 review：只讀 `last_triage_at` 後新增或更新的 receipts。

按 `candidate_key` 合併 comparable signals：

- 1 個：`log-only`；
- 2 個：`watch／retest`；
- 3 個獨立 receipts：`eligible-for-proposed-diff`；
- evidence 不可比、有衝突或同一 artifact 重複計算：`no-change`。

Triage 最多產生一個 target package、三個 atomic edits，寫到 `30-學習與優化/Loop-Updates/YYYY-MM-DD-candidate-key.md`。只提出 exact diff，唔修改 `TONE／DESIGN／QA／Reference／AGENTS／SKILL.md`。完成後先更新 `last_triage_at`；下次 due 設為三日後。

### 5｜apply-approved-update

只在用戶今次明確批准一份 exact Loop Update 時使用：

1. 核對至少三份獨立 comparable receipts、target、atomic diff、衝突及 approval。
2. Vault 規則：只改一個 exact `TONE.md`、`DESIGN.md`、QA、Reference 或 Project rule；重跑相關 QA 並 read-back。
3. Skill：使用環境內 `skill-creator` 先 duplicate-check，再改一個 exact `SKILL.md` contract 及跑其 validator／eval；如 `skill-creator` 不可用，保持 `approved_pending_capability`，不可直接改。
4. `AGENTS.md`：即使有三份 receipts 亦只可提出；必須有針對 `AGENTS.md` 的明確批准先更新。
5. 將 Loop Update 標記 `applied`，記錄 before／after、驗證及 rollback note。

## Validation

每次新增或更新 receipt 後執行：

```bash
python3 .agents/skills/company-vault-learning-loop/scripts/validate_learning_receipt.py \
  --vault . --receipt "ACTUAL_RECEIPT_PATH"
```

只有 `LEARNING_RECEIPT_PASS` 先可回報完成。完成回報包括 artifact、receipt、QA、signal／loop status、今次有冇改 canonical rule、Human Approval 及下一步。
