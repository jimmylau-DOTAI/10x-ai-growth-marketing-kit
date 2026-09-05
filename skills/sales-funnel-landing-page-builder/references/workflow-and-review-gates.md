# Workflow and Review Gates

## Guided interview loop

Standard student experience係一次啟動後連續完成，唔係一疊 copyable prompts。先從 current artifacts 預填，再顯示進度；只問最早一個會改變結果嘅問題。保存回答、完成安全工作、更新 receipt，然後自動前進到下一個 gate。

短答只批准目前顯示嘅決定。每個 Human Review stop 保持獨立；Resume 時以 artifacts／receipts 證據為準，state 聲稱完成但冇證據就只降級相關 gate，唔推倒其他已通過階段。

## 1. Modes

### Standard

逐步完成 Brief、Style、Copy、Build、Operations 同 Release。每個主要 decision 都有 Human Review stop。

### Rapid prototype

只在用戶明確要求 quick mock、trial、direct build 或 rapid prototype 時使用。可以合併 Brief／Style／Copy stops，但要把假設留在內部 receipt，並標示 `PROTOTYPE_REVIEW_REQUIRED`。

### Revision

先列出 preserve list：approved source、copy、information architecture、brand assets、routes、form fields、analytics identifiers 及 operations contract。只改指定範圍，完成 regression QA；不要用一次細改重做整頁。

### Operations hardening

適用於 rendered page 已存在，而問題係 endpoint、CRM、scoring、email、reminder 或 manual Sales action。記錄 `design_change: false`，不要將 backend repair 變成未要求嘅 redesign。

## 2. Source and Offer brief

使用 `assets/landing-page-brief.md`。分開：

- `VERIFIED`：由 current source 核實；
- `PROVIDED`：由用戶提供但未獨立核實；
- `INFERENCE`：有根據嘅判斷；
- `SOURCE_NEEDED`：未補證據前不可公開。

價格、日期、名額、地點、availability、terms、eligibility 同 CTA route 都係 mutable facts。無 current source 時留 `TBC`。

結束狀態：`BRIEF_REVIEW_STOP`。

## 3. Style review

有 reference／Design MD：

1. 說明 layout、type、colour、imagery、density、motion；
2. 建立 `reference element → adapt／reject → reason` mapping；
3. 保留自己 Brand、Offer、claims、assets 同 identity；
4. 寫清楚 desktop-to-mobile collapse rules。

無 reference：提供 2–3 個在 hierarchy、density、type scale、palette、imagery 或 interaction 上真正不同嘅方向。推薦一個，說明點解適合 Audience、Offer 同 CTA。

結束狀態：`STYLE_REVIEW_STOP`。

## 4. Copy review

先交完整 section-by-section copy，唔好只交 Hero。最少包括 Hero、recognition、outcomes、trust、form／next step；FAQ 只處理真實 objection。

Copy Review 要確認：

- 一個清楚 promise；
- feature 已翻譯成 visitor outcome；
- proof 有 status 同 source；
- CTA verb、intent 同 destination 一致；
- form microcopy 交代資料用途、成功後下一步同可能嘅 Sales follow-up；
- 無 TBC 被包裝成 fact。

結束狀態：`COPY_REVIEW_STOP`。

## 5. Build and QA

Build 後建立：

- page source／CMS handoff；
- `DESIGN-ENGINEERING-REVIEW.md`；
- `design-skill-receipt.json`；
- Desktop／Mobile evidence；
- `utm-registry.csv` when applicable；
- `funnel-ops-receipt.json` when applicable。

Receipt validator 通過後仍要做 rendered browser QA。Visual review、DOM／console check、form behaviour 同 destination proof 係不同 evidence channels。

## 6. Controlled release

下列每項係獨立 mutation：

- publish／deploy page；
- deploy endpoint；
- connect form／CRM／analytics／payment；
- write customer data；
- install trigger；
- send confirmation／Sales email；
- create redirect／short URL。

只有用戶在當前對話明確批准 exact target 同 action 先執行。最短安全順序：

1. local no-write validation；
2. read current destination metadata／endpoint version；
3. test with no-send or dedicated destination；
4. deploy once；
5. read back live version／public page；
6. 如獲批准，用 owned contact 跑一次 production smoke；
7. 以 submission ID／unique marker 讀返 CRM row；
8. 由 sender Sent mailbox 讀返 confirmation／Sales messages；
9. 記錄 recipient inbox placement、open、button click 或 group membership 等未證明項目。

HTTP success、success screen、redirect、同一 request 寫入嘅 timestamp 都唔可以單獨證明完整 journey。

## 7. Landing plus Blog handoff

當要求變成 `/`、`/blog` 同 article routes 嘅同一網站，Landing Skill 完成 `landing-site-handoff.json` 後交返現有網站 Project，由 AI 按自然語言整合要求接手，唔在本 Skill 重建 Blog／site deployment 功能。

Handoff 必須指向已批准 artifacts，列出 CTA、form、UTM、QA evidence 同 open items。`APPROVED_FOR_ASSEMBLY` 只代表可以進入 assembly，唔代表 Preview、Production、CRM、email、analytics 或 domain action 已批准。
