---
name: sales-funnel-landing-page-builder
description: Use when a user wants to plan, write, build, revise or verify a conversion-focused single-offer Landing Page with one lead form, UTM tracking, design review and optional CRM or email follow-up. Not for multi-page websites, quizzes, scorecards or advanced assessment funnels.
---

# Sales Funnel Landing Page Builder

## Outcome

將一個已確認嘅 Offer 變成簡單、直接、可驗收嘅 Sales Funnel Landing Page：一個主要受眾、一個訊息、一個 CTA、一個短表格、一個清楚下一步。

預設流程：`Brief → Style → Copy → Build → Tracking → Lead Operations → QA → Human Review`。

## Standard V1 scope lock

Standard V1 只處理 single-offer direct lead capture。Quiz、scorecard、多步 Assessment、branching questionnaire、動態 Results Page 及複雜會員流程不在本 Skill 範圍；需要時另開獨立 Advanced Skill，不要令第一版一路變重。

## Start here

先判斷目前階段，只讀及完成該階段需要嘅內容。

| Current state | Read now | Deliver | Stop status |
| --- | --- | --- | --- |
| New idea／raw Offer | [workflow-and-review-gates.md](references/workflow-and-review-gates.md) + [landing-page-brief.md](assets/landing-page-brief.md) | Source／Offer brief | `BRIEF_REVIEW_STOP` |
| Approved brief, style undecided | 上述 workflow + [design-and-interaction.md](references/design-and-interaction.md) | 2–3 style directions／reference mapping | `STYLE_REVIEW_STOP` |
| Approved brief and style, copy missing | [copy-and-page-structure.md](references/copy-and-page-structure.md) | Section-by-section copy | `COPY_REVIEW_STOP` |
| Approved brief, style and copy | Workflow + design reference + [landing-page-output.md](assets/landing-page-output.md) | Local／staging page and design receipt | `PROTOTYPE_REVIEW_REQUIRED` or `DESIGN_QA_PASSED` |
| Existing page needs revision | Workflow + requested reference only | Scoped revision and regression QA | 保持原有 release status |
| Form／CRM／email／reminder work | [funnel-operations.md](references/funnel-operations.md) | Operations contract and receipt | `OPS_QA_PASSED` |
| Completed page needs final QA | [quality-check.md](references/quality-check.md) | QA result and open items | `QA_REVIEW_STOP` |
| Approved production release | Workflow release section + relevant QA reference | Destination read-back | `PUBLIC_RELEASE_READY` only when proven |

不要因為用戶提供咗 reference 或 Design MD，就跳過 Offer、copy、CTA、資料用途及 destination 確認。

## Intake

用自然語言取得：

- Objective、funnel stage、主要 Audience 及一個核心訊息；
- Offer、價格／日期／名額／地點／交付方式及可用 Proof；
- Primary CTA、成功後下一步及 CTA destination；
- Brand assets、Design MD、reference sites 及現有技術 stack；
- 表格欄位、consent／privacy wording、CRM destination 及 follow-up 規則；
- UTM 命名、environment 及目前批准階段。

可變資料未有 current source 時使用 `TBC`。缺少會改變 Offer、CTA、資料處理或 release 決定嘅資料時，先交目前可確認部分同 blocker，不要用舊 Campaign 或假資料補位。

## Core working rules

- 一頁只服務一個主要轉化目的；不要用第二個同等 CTA 分散決定。
- 用最少 section 回答訪客真正會問嘅問題；不要用 cards、badges、假 dashboard 或重複 CTA 令頁面扮完整。
- 不可虛構 Logo、客戶、testimonial、數字、資格、scarcity、deadline、price、法律文字或結果保證。
- Current brief、用戶提供嘅 Design MD 同 approved reference mapping 優先於預設 aesthetic。
- Draft／local preview／HTTP 200 都不等於已 deploy、已收 Lead、已寫入 CRM 或已發 email。
- 「OK」、「繼續」或修改意見只批准目前可見階段，不代表 publish、deploy、analytics、CRM write、email send 或 customer-data action 已批准。

## Phase 1: Brief lock

使用 [landing-page-brief.md](assets/landing-page-brief.md) 鎖定：

- one Audience、one Message、one Offer、one CTA；
- visitor problem、desired outcome、mechanism 及 objections；
- `VERIFIED`／`PROVIDED`／`INFERENCE`／`SOURCE_NEEDED` Claim status；
- form fields、data use、success action 及 operations scope；
- mutable commercial facts、environment 及 external-action boundaries。

Standard mode 停在 `BRIEF_REVIEW_STOP`。只有用戶明確要求 quick mock／trial／rapid prototype，先可以將 Brief、Style、Copy stops 合併；成品必須標示 `PROTOTYPE_REVIEW_REQUIRED`。

## Phase 2: Style and design dependencies

凡係會改變 layout、visual style、responsive behaviour、motion 或 interaction，必須讀完整已安裝嘅：

1. `design-taste-frontend`：Design Read、design dials、anti-slop、responsive composition、asset plan 及 pre-flight；
2. `emil-design-eng`：interaction purpose、motion timing／easing、hover／active／focus、reduced motion、performance 及 engineering review。

如果任何一個 Skill 不可用或未讀完整，使用 `DEPENDENCY_BLOCKED`，不可假稱已完成設計。詳細執行及 receipt 見 [design-and-interaction.md](references/design-and-interaction.md) 與 [mandatory-design-dependencies.md](references/mandatory-design-dependencies.md)。

Operations-only／tracking-only 修改如果不改 rendered page，記錄 `design_change: false`，保留最近一次有效 design receipt，毋須重跑設計判斷。

用戶有 reference 時，交付 `reference → adapt／reject → reason` mapping。未有 reference 時，提供 2–3 個真正不同方向、推薦一個並停在 `STYLE_REVIEW_STOP`；不要叫用戶由零發明設計術語。

## Phase 3: Copy and page structure

Copy 要將訪客由 `呢個係乜` 帶到 `我知道下一步會發生乜`。預設香港受眾使用自然繁體中文及廣東話節奏，保留熟悉嘅 English product／technical terms。

使用最少內容回答：

1. **What is this?** 一個 promise、一句 supporting explanation、一個 CTA；
2. **Is it for me?** 可辨認嘅處境或阻力；
3. **What will I get?** 三至五個具體 outcome、deliverable 或 learning step；
4. **Why should I trust it?** 只有已核實嘅 proof、method、instructor context 或 delivery fact；
5. **What happens next?** Short form、data／follow-up microcopy 及同一 CTA intent。

FAQ 只處理真正阻力。完整 writing rules 見 [copy-and-page-structure.md](references/copy-and-page-structure.md)。Standard mode 停在 `COPY_REVIEW_STOP`。

## Phase 4: Build and tracking

只有 Brief、Style 同 Copy 已批准先正式 Build；Rapid prototype 除外。

- 保留現有 stack，除非轉換有明確理由同批准；
- 使用 semantic HTML、清楚 heading hierarchy、labelled form、visible focus 及 explicit mobile rules；
- 實作 approved Taste／Emil decisions，不把 interaction 同 responsive QA 留到「之後 polish」；
- 使用真實 assets；未知圖片、route 或 destination 保持 `TBC`；
- Analytics、endpoint、CRM、payment 或 external automation 未獲批准時保持 disconnected。

Tracking in scope 時建立 project-local `utm-registry.csv`：

```text
status,channel,utm_source,utm_medium,utm_campaign,utm_content,utm_term,destination,short_url,owner,checked_at,notes
```

保留五個 UTM fields，包括空白 `utm_term`。未知值標示 `TBC` 並停止生成 production link；不要自行猜 campaign naming 或 short URL。

## Phase 5: Lead operations

表格 endpoint、Google Sheet／CRM、Lead scoring、confirmation email、conditional Sales alert、scheduled reminder 或 manual Sales action 在範圍內時，先讀 [funnel-operations.md](references/funnel-operations.md)。

明確分開：

1. `dry-run-no-write`：驗 schema、UI、validation 同 decision logic；不寫 CRM、不發送；
2. `test-connected`：優先使用 dedicated test destination；否則清楚標記 test rows 同 KPI exclusion；
3. `production-smoke`：只有當前明確批准，使用 owned contact 做一次，之後按 submission ID／unique marker 讀返 CRM row 同 sender Sent mailbox。

Google Apps Script 可以使用 `scripts/apps_script_endpoint.py` 做 health check 同受控提交。回應含糊時回傳 `AMBIGUOUS_SUBMISSION`，先查 CRM，禁止盲目 retry。

## Phase 6: QA and controlled release

完成前讀 [quality-check.md](references/quality-check.md)，在 Desktop 及 Mobile 驗證 source、copy、visual、interaction、accessibility、form、tracking 同 operations。

Build／Revision 建立 `design-skill-receipt.json`，再執行：

```bash
python3 scripts/validate_design_skill_receipt.py /absolute/path/to/design-skill-receipt.json
```

Lead operations 在範圍內時另建 `funnel-ops-receipt.json`：

```bash
python3 scripts/validate_funnel_ops_receipt.py /absolute/path/to/funnel-ops-receipt.json
```

Validator exit code `0` 只證明 receipt 結構同指定 evidence 完整，不代表 browser QA、deployment 或真實 customer journey 已完成。

Deploy page、deploy endpoint、install trigger、write CRM、send email、connect analytics 及 publish tracking link 都係獨立 external mutation。逐項取得 current-turn approval；完成後由真實 destination read back。不得用本機畫面、success message 或單一 HTTP response 代替 destination proof。

## Status contract

- `BRIEF_REVIEW_STOP`：Brief 待確認；
- `DEPENDENCY_BLOCKED`：mandatory design Skill 不可用或未讀完整；
- `STYLE_REVIEW_STOP`：視覺方向待選；
- `COPY_REVIEW_STOP`：完整文案待批；
- `PROTOTYPE_REVIEW_REQUIRED`：implementation 存在，但未完成全部 approval／QA；
- `DESIGN_QA_PASSED`：design receipts 及 rendered design checks 通過；
- `OPS_QA_PASSED`：endpoint、schema、scoring、automation logic 通過，不代表 production journey；
- `PRODUCTION_SMOKE_VERIFIED`：一次獲批准 owned-contact flow 已有 CRM／Sent-mail read-back；
- `QA_REVIEW_STOP`：已完成所述 QA，仍待 Human Review；
- `PUBLIC_RELEASE_READY`：current claims、CTA、destination、consent、data behaviour、tracking 及 public read-back 全部通過。

不可由意圖、畫面外觀、named Skill、preview URL 或 receipt 自動升級狀態。

## Completion receipt

每個階段最後列出：

- `Current phase`；
- `Status`；
- `Confirmed`；
- `TBC / blocked items`；
- `Artifacts / evidence`；
- `External actions performed`；
- `Next approval needed`。

任何 Review Stop、local build 或 staging preview 都不等於已公開或已接通 Lead journey。
