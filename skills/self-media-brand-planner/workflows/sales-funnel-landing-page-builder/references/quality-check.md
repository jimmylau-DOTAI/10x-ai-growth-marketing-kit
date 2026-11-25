# Landing Page Quality Check

完成 Build／Revision 後逐項檢查。Status 要反映實際 evidence，未跑就寫 `NOT_RUN`，不可以當 pass。

## Source and conversion

- [ ] One Audience、one Message、one Offer、one primary CTA；
- [ ] Price、date、capacity、location、terms、eligibility 來自 current source；
- [ ] Hero promise 清楚，support line 增加 context；
- [ ] 每個 section 回答一個 visitor question；
- [ ] feature 已轉成 practical outcome；
- [ ] proof／testimonial／metric／urgency 有 source；
- [ ] CTA label、intent、destination 全頁一致；
- [ ] form microcopy 交代 next step、data use、Sales contact。

## Visual and responsive

- [ ] Taste Design Read、dials、reference mapping、asset plan 已實作；
- [ ] Desktop 同 Mobile Hero 無截斷／不自然 wrap；
- [ ] multi-column sections 有 explicit mobile collapse；
- [ ] 無 horizontal overflow、broken assets、desktop button wrap；
- [ ] type hierarchy、spacing、contrast、visual density 清楚；
- [ ] 無 fake UI、fake dashboard、filler card 或 copied identity。

## Interaction and accessibility

- [ ] Emil motion decision table 同 review 完成；
- [ ] 無 `transition: all`，timing／easing 有目的；
- [ ] hover、active、focus、loading、success、error states 可辨認；
- [ ] keyboard order、labels、alt text、contrast 合理；
- [ ] reduced motion 已測；
- [ ] animation 不拖慢 repeated action。

## Form, data and tracking

- [ ] required／optional fields 清楚；
- [ ] server validation、consent、honeypot／abuse control 已測；
- [ ] duplicate click、dedupe／idempotency 已測；
- [ ] spreadsheet formula injection protection 已測；
- [ ] phone／email normalization 規則清楚；
- [ ] five UTMs、landing URL、referrer preserved；
- [ ] `utm-registry.csv` 無 production `TBC`；
- [ ] test rows／emails 會按 contract 標記及排除 KPI。

## Operations

- [ ] endpoint health／expected version read-back；
- [ ] CRM schema 同 exact row read-back；
- [ ] scoring fixtures 在 threshold 兩邊通過；
- [ ] high-tier alert sent、low-tier suppressed、manual action tested；
- [ ] Lead confirmation／Sales alert 有 plain-text fallback 同 sender identity；
- [ ] reminder filter、time zone、dedupe、sent log、trigger read-back；
- [ ] ambiguous submit 未盲目 retry；
- [ ] unproven inbox／open／membership 項目已列出。

## Release and boundary

- [ ] Design receipt validator exit `0`；
- [ ] Operations receipt validator exit `0` when in scope；
- [ ] Browser console error count、broken assets、overflow 已記錄；
- [ ] Local／staging／production environment 清楚；
- [ ] Publish、deploy、CRM write、trigger、send 各自有 current approval；
- [ ] Public page／endpoint／CRM／Sent mailbox 已由 destination read back；
- [ ] 完成狀態沒有超過 evidence 可以支持嘅範圍。

## QA receipt

```markdown
Current phase:
Status:
Confirmed:
TBC / blocked items:
Artifacts / evidence:
External actions performed:
Unproven:
Next approval needed:
```
