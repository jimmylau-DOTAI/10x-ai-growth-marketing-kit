# Funnel Operations Contract

只在 Landing Page 收集 Lead，或連接 endpoint、CRM、email、scoring、reminder、manual Sales action 時讀取。

## Outcome

分層證明完整 journey：

`form → server validation → CRM row → classification → confirmation → conditional Sales alert → scheduled/manual follow-up → destination read-back`

頁面完成不等於 operations 完成；operations repair 亦不需要重開已批准嘅 design。

## Lock the contract

實作前記錄：

- environment、endpoint provider／deployed URL／expected version；
- required fields、allowed values、consent text／version；
- CRM destination ID、visible table／sheet、immutable submission ID、column map；
- sender mailbox、Lead recipient rule、Sales recipient；
- score inputs、threshold outputs、automatic alert rule；
- reminder time zone、eligibility filter、dedupe key、sent timestamp、failure state；
- five UTM fields、landing URL、referrer；
- test write／send behaviour、KPI exclusion、retention decision。

Receipt、HTML、Sheet 同 source control 不可包含 API key、token、password 或 webhook secret。使用 provider runtime secret store／Apps Script Properties。

## Data invariants

- Browser validation 只改善 usability；server 仍要驗 required fields 同 allowed values；
- 使用 immutable submission ID 做 CRM 及 message read-back；
- 電話以 text 儲存，只按明確 country-code rule normalize；
- 防止 user-controlled value 成為 spreadsheet formula；
- 保留五個 UTM fields，空白 `utm_term` 繼續空白；
- append／send 要 idempotent 或 deduplicated；timeout 不可直接 retry；
- raw Lead rows 儘量 immutable；dashboard／score summary 另行計算；
- Sales view 先顯示 company、role、score reason、decision role、business email、next action；diagnostics 放後；
- 在每個 threshold 兩邊建立 score fixtures；free mailbox、job title 或 student signal 都不可單獨決定質素。

## Test states

### `dry-run-no-write`

使用 mock transport／pure functions 驗 required fields、honeypot、consent、normalization、score、UTM、success／error UI 同 version mismatch。不可寫 CRM、send 或 install trigger。

### `test-connected`

優先 dedicated test Sheet／tab／event 同 owned mailbox alias。如果 backend 只有 `is_test`，要讀 code 證明：

- 是否仍會寫 row；
- 是否會發 Lead／Sales email；
- 是否排除 dashboard KPI／reminder；
- 如何識別、保留或獲批准後移除。

不要假設 `is_test=true` 等於 no-write。不可用 random external email／phone；randomness 只可用於非聯絡 marker，例如 `fixture-7f3a`。

### `production-smoke`

只在 current-turn 明確批准後使用 owned contact 跑一次：

- identity 清楚標示為 internal verification；
- submit 前保存 unique marker；
- ambiguous response 先查 CRM，不 retry；
- 以 submission ID／marker 讀返 exact row；
- 由 sender Sent mailbox 讀返 Lead confirmation 同 conditional Sales alert；
- 記錄 fixture 保留或另行批准移除。

刪除 production fixture 是另一個 CRM mutation，未批准不可做。

## Google Apps Script shortest path

1. 讀 current deployment 同 source version；
2. `doGet` 回傳 service／version；
3. `doPost` 先 server validation，後 write；
4. CRM row 成功後先發 messages，並獨立記錄每個 send result；
5. trigger 按 handler dedupe，install 後 read back；
6. deploy 一次，再確認 live health/version；
7. 使用 `scripts/apps_script_endpoint.py` 做 health／controlled submit。

不要用 `curl -L -X POST` 測 Apps Script Web App。Google redirect 後可能保留 POST，原 request 可能已執行但最後只見 HTML error。任何 non-JSON／timeout／ambiguous response 都先查 CRM。

## Minimum verification matrix

| Layer | Required evidence |
| --- | --- |
| Form | required fields、consent、error state、no duplicate click |
| Endpoint | health／version read-back、structured response |
| CRM | metadata／schema、exact row by submission ID |
| Scoring | threshold fixtures、alert decisions |
| Confirmation | sender Sent-mail；owned inbox when available |
| Sales alert | high-tier sent、low-tier suppressed、manual action |
| Reminder | trigger／filter／dedupe test、trigger read-back |
| Tracking | five UTMs、landing／referrer preserved |
| Success handoff | 只在 contract 定義嘅 registration state 後顯示 |

Sent-mail 證明 provider 接受 outgoing message，不證明 inbox placement／open。WhatsApp redirect 或 click 不證明 group membership。

## Operations receipt

建立 `funnel-ops-receipt.json`：

```json
{
  "schema_version": "1.0",
  "primary_skill": "sales-funnel-landing-page-builder",
  "artifact_status": "OPS_QA_PASSED",
  "design_change": false,
  "environment": "staging",
  "endpoint": {
    "provider": "Google Apps Script Web App",
    "url": "https://script.google.com/macros/s/DEPLOYMENT_ID/exec",
    "expected_version": "campaign-v1",
    "health_readback": "pass"
  },
  "crm": {
    "in_scope": true,
    "destination_id": "SPREADSHEET_ID",
    "sheet": "Leads",
    "schema_readback": "pass",
    "test_rows_excluded_from_kpis": true
  },
  "automations": {
    "lead_ack_email": "pass",
    "conditional_sales_alert": "pass",
    "scheduled_reminder": "pass",
    "manual_sales_action": "pass"
  },
  "test_contract": {
    "mode": "dedicated-test-destination",
    "writes_production": false,
    "sends_external_email": false,
    "owned_contacts_only": true
  },
  "live_verification": {
    "production_smoke_performed": false,
    "submission_id": "not-applicable",
    "crm_row_readback": "not-run",
    "lead_email_sent_readback": "not-run",
    "sales_email_sent_readback": "not-run",
    "trigger_readback": "pass",
    "retention_decision": "not-applicable",
    "unproven": ["recipient inbox placement", "email open", "group membership"]
  },
  "safety": {
    "consent_enforced": true,
    "server_validation": true,
    "dedupe_or_idempotency": true,
    "formula_injection_protection": true,
    "secrets_out_of_source": true
  }
}
```

`PRODUCTION_SMOKE_VERIFIED` 或 `PUBLIC_RELEASE_READY` 需要 production smoke 及相關 CRM／Sent-mail／trigger read-back 通過，但仍不會證明 `unproven` 項目。
