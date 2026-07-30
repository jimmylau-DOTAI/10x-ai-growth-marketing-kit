# Routing and Delivery Gates

## Route by job

| Job | Skill | Handoff result |
| --- | --- | --- |
| 研究社交內容、Hook 或競爭內容 | `social-content-research` | Research note and original angles |
| 建立 search-led、SEO 或 GEO 文章 | `seo-geo-content` | Search brief and reviewed draft |
| 寫或改寫平台社交文案 | `social-post-writing` | Platform-ready draft pack |

沒有對應 Skill 時，保留 Handoff，不假裝工作已完成。

## Required handoff fields

```yaml
task:
funnel_stage:
audience:
business_outcome:
core_message:
proof:
cta:
required_output:
source_links:
owner:
reviewer:
status:
```

## Status

- `BRIEFED`：資料足夠，可開始；
- `IN PROGRESS`：正在執行；
- `NEEDS INPUT`：缺資料；
- `READY FOR REVIEW`：完成草稿，未批准；
- `APPROVED`：指定人已批准；
- `PUBLISHED`：有實際發佈證據。

`READY FOR REVIEW` 不等於 `APPROVED`；`APPROVED` 不等於 `PUBLISHED`。

## Human gates

以下行動必須由獲授權嘅人確認：

- 公開發佈；
- 發送 Email、DM 或客戶回覆；
- 改動廣告預算；
- 使用個人或客戶資料；
- 對外作結果、合作或客戶 Claim。

