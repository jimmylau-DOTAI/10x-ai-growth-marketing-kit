---
name: landing-page-blog-deployer
description: Use when a user wants to combine an approved landing page and approved blog content into one website, resume an unfinished site build, add shared CTA and UTM behaviour, or safely preview and deploy the result to Vercel. Guides beginners one decision at a time and does not replace landing-page or blog writing Skills.
---

# Landing Page Blog Deployer

## Outcome

將已批准嘅 Landing Page 同 Blog handoff 組合成一個可驗收網站，保留共同 CTA、表格、UTM、SEO metadata 同 mobile behaviour，再經 Local QA、Preview、Human Review 同 live read-back 完成 Vercel release。

預設流程：`Resume／Inspect → Repair inputs → Assemble → Local QA → Preview → Human Review → Production deploy → Live read-back`。

本 Skill 係 assembly、guided recovery 同 deployment owner。佢不會重新發明 Offer、重寫未批准文章，亦不會將一句「OK」當成 production approval。

## Start or resume

開始時先讀完整 [guided-workflow.md](references/guided-workflow.md)，然後：

1. 檢查 current project、現有 routes、framework、package scripts、Git state、Vercel linkage、content files、form endpoint 同 `site-deployment-state.json`；
2. 從現有 artifacts 預填已知資料，唔好叫用戶重新回答；
3. 顯示簡短進度：`已完成／而家處理／下一個 gate`；
4. 只有一個未決定事項會實質改變結果時，先問一條問題；
5. 保存答案及 evidence，完成安全嘅本機工作，然後自動進入下一項；
6. 接受「確認」、「揀 A」、「繼續」等短答，但只批准目前顯示嘅 gate。

如果 project 已經完成部分工作，從最早一個未通過 gate 繼續。不可因為 state file 缺失就覆蓋現有網站或由零重建。

## Required handoffs

組合前讀 [handoff-contracts.md](references/handoff-contracts.md)。優先取得：

- `landing-site-handoff.json`：由 `sales-funnel-landing-page-builder` 產生；
- 一份或多份 `blog-publish-handoff.json`：由 `seo-geo-content` 產生；
- current project path 或 approved starter destination；
- intended Vercel project／team、domain 同 environment；
- CTA、form／CRM、consent、tracking 同 mutable facts 嘅 current status。

缺少 handoff 時先搜尋 current project 中可驗證嘅 equivalent artifacts。可以建立 handoff draft，但不可將推測升級為 approved。用以下 command 驗證結構：

```bash
python3 scripts/validate_site_handoffs.py \
  --landing /absolute/path/to/landing-site-handoff.json \
  --blog /absolute/path/to/blog-publish-handoff.json
```

Validator 通過只證明結構同 gate labels 合格，不代表 copy、claims、browser QA 或 deploy 已批准。

## Scope lock

預設 V1 包含：

- `/` Landing Page；
- `/blog` article index；
- `/blog/[slug]` 或 stack 等價嘅 article route；
- 共用 Header、Footer、CTA intent 同 lead form；
- Blog 中段 CTA；
- 只在 Blog article mobile viewport 顯示嘅 fixed bottom CTA；
- UTM first-touch continuity；
- Article metadata、canonical、sitemap、robots 同 supported structured data；
- Vercel Preview／Production release 同 read-back。

CMS 係可選。現有 Markdown、MDX、JSON、Obsidian export 或 code content folder 足夠時，不要為咗「完整」強行加入 Supabase、登入、dashboard 或 editor。只有內容量、多人編輯或 workflow 真正需要時，先提出 CMS decision。

## Assembly rules

- 保留 current stack、routes、brand assets、approved copy、form contract、analytics identifiers 同 working behaviour；除非修復有明確理由。
- 先 map 現有 project，再作最小修改。不得為加入 Blog 重寫整個 Landing Page。
- Landing Page 同 Blog CTA 要指向同一 approved intent。Blog 可以連回 `/#lead-form` 或 approved equivalent，但不可製造 destination。
- Mobile fixed CTA 只在 article pages 顯示；不得遮住 form、cookie control、browser safe area 或重要內容，並要提供足夠 bottom spacing。
- 所有 links 要有真實 destination。`TBC`、`CTA_TBC`、`LINK_TBC`、`SOURCE_NEEDED` 或未批准 image 不可進 production output。
- Article H1、metadata、canonical、FAQ／Article schema 要同可見內容一致。不要生成正文冇出現嘅 schema answers。
- 保留 UTM 五個 fields；first-touch 值寫入同 origin 相同嘅安全 client storage 或 approved server session，之後由同一 form submission 帶出。不要將測試 UTM／test lead 混入 production KPI。
- Form、CRM、email、analytics 同 domain change 各自係 external mutation；未獲批准時可以做 no-write validation，但保持 disconnected。

## Build and local QA

使用現有 package manager 同 scripts。改動前記錄 preserve list，改動後最少驗證：

- clean install／typecheck／lint／build，按 repo 實際可用 commands；
- `/`、`/blog`、每個 article slug 都能 render；
- no broken internal links、duplicate H1、missing canonical 或 invalid structured data；
- Desktop 同 390px mobile 無 horizontal overflow；
- keyboard focus、form labels、error／success states 同 reduced motion；
- Blog 中段 CTA 可達；mobile fixed CTA 只在 article route 出現；
- direct article entry with UTM、article → form navigation、submission payload continuity；
- form dry-run 不寫 CRM；connected tests 使用 dedicated test destination 或清楚 `is_test` marker。

本機完成後狀態係 `LOCAL_QA_PASSED`，不等於 deploy。

## Preview and production release

需要 Vercel 時讀完整 [vercel-release.md](references/vercel-release.md)。

建立 Preview 會改變外部狀態；如果當前請求未明確批准 deploy／preview，先停在 `PREVIEW_APPROVAL_REQUIRED`。Preview 完成後打開真實 Preview URL 做 browser read-back，列出可見結果及未證明項目，然後停在 `HUMAN_REVIEW_STOP`。

Production deploy 必須有當前對話針對 exact project／environment 嘅明確批准。批准前展示：

- target Vercel project／team／domain；
- commit 或 artifact identity；
- environment variable readiness；
- Preview URL 同 QA result；
- external side effects，包括 form、CRM、email、analytics 同 domain。

Deploy 一次後立即 read back deployment metadata、production URL、HTTP response、主要 routes 同 browser behaviour。含糊或 timeout 時先查 deployment list／logs／live destination，禁止盲目 retry。

## Guided recovery

遇到問題唔好只丟 error 畀初學者。先保存 state，再用以下次序處理：

1. 用一句人話講出卡住嘅結果；
2. 分開已保留工作同失敗步驟；
3. 做安全 read-only diagnosis；
4. 有一個合理修復時直接修正並重跑該 gate；
5. 有多個會改變產品／資料／成本嘅選擇時，推薦一個並只問一條問題；
6. 需要新權限、secret、付費、domain、CRM write 或 production action 時停低；
7. 修復後由失敗 gate 繼續，不重做已通過階段。

不得顯示、提交或保存 secret value 到 repo、receipt 或對話。只記錄 variable name 同 `PRESENT／MISSING／UNVERIFIED`。

## Status contract

- `INPUT_REPAIR_REQUIRED`：handoff／project 有實質缺口，仍可逐項補回；
- `ASSEMBLY_IN_PROGRESS`：網站正組合或修復；
- `LOCAL_QA_PASSED`：本機 build、routes、responsive、CTA／form dry-run 已通過；
- `PREVIEW_APPROVAL_REQUIRED`：等待批准建立 Vercel Preview；
- `PREVIEW_QA_FAILED`：Preview 已存在，但有明確失敗項目；
- `HUMAN_REVIEW_STOP`：Preview 同證據已交，等待人手批准 Production；
- `PRODUCTION_APPROVAL_REQUIRED`：目標已列明，等待本次正式發布批准；
- `PRODUCTION_DEPLOYED_UNVERIFIED`：deployment 已回報成功，但 live read-back 未完成；
- `PUBLIC_RELEASE_VERIFIED`：production routes、CTA、tracking contract 及已批准 destinations 完成 read-back；
- `BLOCKED_EXTERNAL`：需要用戶／provider action，並已列明保留內容同下一步。

## Completion receipt

使用 [site-release-receipt.md](assets/site-release-receipt.md)，最少列出：

- Current phase and status；
- completed／preserved work；
- Landing／Blog handoff paths；
- local／Preview／Production evidence；
- exact routes tested；
- form／UTM／CRM／email／analytics status；
- external actions actually performed；
- unproven items；
- owner and next action。

只有 `PUBLIC_RELEASE_VERIFIED` 先可以話網站已正式發布並驗證。Git commit、Vercel build success、Preview URL、HTTP 200 或 form success message 都不能單獨證明完整流程。
