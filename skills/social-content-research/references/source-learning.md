# Source Learning contract

只在 Deep SL mode 閱讀本檔。

SL 唔係將 Source 縮短。目標係保留完整方法、證據邊界及可用觀點，令另一個 Agent 無需重讀原 Source 都可理解內容。

## File pair

每個來源建立一對檔案：

- 01-Sources/SRC-YYYYMMDD-topic.md
- 02-SL/SL-YYYYMMDD-topic.md

topic 使用短小 kebab-case。Source ID 及 SL source_id 必須一致。

## Source Receipt schema

~~~yaml
---
type: social_source_record
status: captured
source_id: SRC-YYYYMMDD-topic
source_ref: https://example.com/or-local-reference
source_type: post
captured: YYYY-MM-DD
access_state: FULL
retrieval_method: original-page
content_scope: social-post-research-only
origin_id: creator-or-publication-plus-item-id
---
~~~

必須包含：

1. Access receipt：讀到、讀唔到及擷取方法；
2. Evidence inventory：Observed 嘅主張、例子、數字、畫面或 CTA；
3. Limitations：過時風險、缺少內容、未能核實事項；
4. SL route：對應 SL 檔案。

只保存研究需要嘅短引文或準確 paraphrase。不要複製完整文章或逐字稿。

## SL schema

~~~yaml
---
type: social_source_learning
status: queued-for-insight-review
source_id: SRC-YYYYMMDD-topic
source_ref: https://example.com/or-local-reference
created: YYYY-MM-DD
access_state: FULL
knowledge_status: source-learning-not-approved-insight
content_scope: social-post-research-only
candidate_count: 0
review_status: queued
---
~~~

## Required SL sections

### 30 秒理解

用 3–5 點講清楚主題、核心結論、適用對象、來源證據強度及限制。

### Coverage

列出 Source 主要章節／論點，並標示 covered、partial 或 missing。完整 SL 要覆蓋所有重要主張，而唔只係最吸引嘅一段。

### 完整攻略

按來源本身邏輯重組：

- 問題或背景；
- 方法、模型或逐步做法；
- 例子、數字及反例；
- 來源提出嘅條件與限制；
- 實際可採取嘅動作。

Observed 與 Inferred 要清楚分開。無法證實嘅內容標 Not proven。

### Candidate Insight cards

每個真正獨立嘅觀點一張卡：

~~~markdown
#### Candidate 01

- candidate_key: stable-kebab-case-pattern
- 一句見解：
- 點解值得記住：
- 來源證據：
- 邊界／反例：
- Post relevance：
~~~

Candidate Card 只代表一個來源嘅可測試理解，唔係 durable Insight。

### Evidence boundary

列出可安全使用嘅 claims、必須 attribution 嘅 claims、不可使用嘅 claims，以及時間敏感資料。

### Source-bounded Post Brief

只有用戶要求出 Post 時才加入：

- Target platform / audience；
- Problem or tension；
- Source-backed takeaway；
- Evidence available；
- Claims to avoid；
- Suggested hook；
- Suggested structure；
- CTA intent。

呢份 Brief 可以支援今次 Post draft，但唔可以當成跨任務 evergreen Insight。

## Completeness test

SL 合格條件：

- 未睇原 Source 嘅人都理解完整方法；
- 重要步驟、論據、例子及限制都有覆蓋；
- Candidate 互相有明確差異；
- 每張 Candidate 都可追溯到 Source Receipt；
- 冇將作者聲稱誤寫成已證實結果；
- 冇加入公司未提供嘅立場或商業資料。
