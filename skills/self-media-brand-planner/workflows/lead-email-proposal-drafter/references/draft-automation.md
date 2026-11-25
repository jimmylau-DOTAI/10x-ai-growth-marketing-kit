# Daily Gmail lead draft automation

只在用戶明確要求設定／執行每日Gmail automation時讀。

## 一句指令要包含的資料

- exact approved Gmail account；
- daily run time及timezone；
- search window，預設最近24小時；
- current Codex Task；
- 已驗證的 `lead-email-proposal-drafter`；
- draft-only／never-send boundary；
- 建立後 read-back Automation name、status、schedule、next run 同 report location。

用戶完成手動 synthetic workflow 同 Skill validation 後，可以用一句自然語言交代以上資料，並明確講「請而家建立 Automation」。缺 exact account、時間、時區、current Task 或 draft-only boundary 就停低追問；資料齊及有明確批准就建立，而唔係先做 Paused 設定表。

示範預設指令見 Project root 的 `daily-gmail-lead-draft-blueprint.md`。建立後必須見到 `ACTIVE` 同 `next_run`；只寫好 Prompt 不算有排程。

## Daily run

1. 讀Gmail profile，確認係exact approved account；唔符合就停止。
2. 搜尋`newer_than:1d -in:spam -in:trash`，加Lead意圖詞，例如quotation、proposal、enquiry、training、workshop、合作、報價、查詢。
3. 排除OTP、安全通知、system receipt、newsletter、活動報名及供應商promotion，除非明確係商業機會。
4. 每輪最多處理10封候選；逐封讀thread，唔批量生成同一內容。
5. 先列現有Draft，確認同一thread未有automation建立或人手正在寫的Draft；有就`SKIP_EXISTING_DRAFT`。
6. 用主Skill判斷`INFO_REPLY／PROPOSAL_DRAFT／NEEDS_MORE_INFO／HOLD_FOR_HUMAN／NO_REPLY`。
7. 建立localProposal／reply artifacts；只有exact account／thread授權成立先建立一份Gmail Draft。
8. Gmail Draft必須reply原thread；未有批准嘅價錢、日期、條款、成果或附件保持TBC／唔提及。
9. 建立後read back draft ID、masked recipient、subject、thread及status；不可Send。
10. 在同一個 Codex Task 留 Run Report，列 scanned、candidate、drafted、skipped、held、errors 及 next action；未到第一次執行就如實顯示 `no run yet`。

## Hard stops

- 永不自動Send、forward、schedule-send；
- 永不自動批准／附上final quotation或contract；
- 永不刪除、archive或改CRM；
- 投訴、付款、退款、法律、安全、敏感資料、重大承諾一律`HOLD_FOR_HUMAN`；
- 連續兩次connector／authentication失敗就停止當日run，唔重試fan-out。
