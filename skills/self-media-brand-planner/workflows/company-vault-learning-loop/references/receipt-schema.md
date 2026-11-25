# Learning Receipt Schema

只在新增／更新 Learning receipt 時讀。每個 receipt 對應一個實際 artifact；同一 artifact 的 closeout、feedback 及 published review 更新同一檔案。

## Required frontmatter

```yaml
---
title: YYYY-MM-DD｜Topic
type: learning_receipt
status: awaiting_human_feedback
date: YYYY-MM-DD
project: none
task: topic-slug
platform: none
format: none
objective: TBC
artifact: exact/relative/path
artifact_status: draft | approved | published
human_review: pending | recorded
signal_type: none | preference | quality | workflow | performance | commercial
candidate_key: none
evidence_count: 0
loop_status: not-a-signal | log-only | watch | retest | eligible-for-proposed-diff
rule_update_status: none | proposed | approved_pending_apply | applied | rejected
updated: YYYY-MM-DD
---
```

## Required sections

```markdown
# Learning Receipt

## Artifact
- Final artifact：
- Source／brief：
- Production Skill：
- Style／Reference：
- QA receipt／result：

## Human feedback
- 原話／決定：pending
- 喜歡：none
- 不喜歡：none
- 原因：none

## Published evidence
- URL／date／review window：none
- Public evidence：none
- Backend evidence：none
- Commercial evidence：none
- Missing evidence：none

## Learning
- Observation：
- Insight：
- Hypothesis：
- Decision：retain | stop | retest | propose-rule-update | none

## Candidate
- Comparable receipts：
- Proposed exact target：none
- Proposed bounded diff：none
- Human approval：pending
```

`awaiting_human_feedback` 必須保持 `signal_type: none`、`candidate_key: none`、`evidence_count: 0`。只有明確 feedback／published evidence 先可變成 signal；AI 自評、QA PASS 或建立咗 artifact 唔等於 Human approval。
