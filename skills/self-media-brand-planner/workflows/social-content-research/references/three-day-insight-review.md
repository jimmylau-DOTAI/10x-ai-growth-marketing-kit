# Three-day Insight Review

只在 Three-day Insight Review mode 閱讀本檔。

## Purpose

每三日比較新 SL，找出多個獨立來源重複出現嘅 content pattern。三日係整理節奏，唔係自動認證機制。

## Inputs

1. TRIAGE-STATE.md；
2. 上次 successful review 後新增或更新嘅 02-SL 檔案；
3. 現有 03-Insights 中相同 candidate_key 嘅檔案。

不要重讀全部 Source。只有需要核對衝突或 evidence boundary 時，先精確打開對應 Source Receipt。

如 state 尚未排程，將 next_review_due 設為第一份合格 SL 完成日後三日，然後停止。用戶今次明確要求立即 review 除外。

## Independence rules

- 同一原作者同一內容嘅 repost、mirror、翻譯或摘要只計一個 origin；
- 互相引用同一篇研究嘅多篇內容，不等於多個獨立證據；
- 不確定是否獨立時，保守計一次並標示 uncertainty；
- 相反結果不可被平均或刪除。

## Decision table

| 獨立來源數 | 動作 |
| --- | --- |
| 0–1 | 保留 SL queued；不建立 Insight |
| 2+，pattern 相同 | 建立或更新 Candidate Insight |
| 2+，但互相衝突 | 建立 conflict candidate 或保留 queued，列明差異 |
| Human approved | 改為 approved-for-post |
| Human rejected | 改為 rejected，保留理由 |

## Candidate Insight schema

~~~yaml
---
type: social_content_insight
status: candidate
insight_id: INS-topic
candidate_key: stable-kebab-case-pattern
source_refs:
  - SRC-YYYYMMDD-a
  - SRC-YYYYMMDD-b
sl_refs:
  - SL-YYYYMMDD-a
  - SL-YYYYMMDD-b
independent_source_count: 2
review_window: YYYY-MM-DD_to_YYYY-MM-DD
content_scope: social-post-only
human_review: pending
---
~~~

內容必須包括：

1. Insight；
2. 重複出現嘅 pattern；
3. 來源如何相同／不同；
4. Contradictions；
5. Evidence boundaries；
6. 可用 Post angles；
7. Human Review decision。

## State contract

成功完成 review 後才更新 TRIAGE-STATE：

~~~yaml
---
last_review_at: YYYY-MM-DD
next_review_due: YYYY-MM-DD
review_cadence_days: 3
last_status: success
processed_sl:
  - SL-YYYYMMDD-a
---
~~~

如 review 失敗或資料不完整，不可將檔案標記為 processed。

## Automation boundary

獲用戶啟用嘅排程可以：

- 到期時讀新 SL；
- 建立／更新 Candidate Insight；
- 更新成功狀態；
- 回報待 Human Review 清單。

排程不可：

- 將 candidate 自動批准；
- 寫入公司事實、產品、品牌、Design System 或 Skill；
- 自行建立 Post、Publish、Send 或 Schedule；
- 因為高互動數字就宣稱機制有效。

## Efficient report

只報：

- Review window；
- New SL count；
- New／updated Candidate Insights；
- Queued single-source candidates；
- Conflicts；
- Human Review required；
- Next due date。
