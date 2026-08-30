---
name: seo-geo-content
description: Use when a user wants to turn supplied source material into a high-quality SEO/GEO blog, improve an article for search and AI answer engines, or create a local HTML review with Company Brain, CTA, link, claim, image, and Human Review controls.
---

# SEO + GEO Blog Writing

## Outcome

將用戶提供嘅 Source 轉成有搜尋價值、容易理解同引用嘅 SEO／GEO Blog，同時保留原創、公司資料、CTA、連結、圖片及 Human Review 邊界。

預設流程：`Source Guide → Title → Article → Local HTML → Human Review`。

## Phase router

先讀 [workflow-and-review-gates.md](references/workflow-and-review-gates.md)，每次只完成目前獲批准嘅階段：

| Current state | Current job | Stop status |
| --- | --- | --- |
| New raw Source | Source Guide only | `SOURCE_GUIDE_REVIEW_STOP` |
| Approved Source Guide | Title and search angle only | `SEO_TITLE_REVIEW_STOP` |
| Approved Guide and title | Article、Meta、CTA、Links and QA | `BLOG_REVIEW_STOP` |
| Approved article with an HTML request | Local generic HTML only | `HTML_REVIEW_STOP` |

「OK」、「繼續」或修改意見只批准當前可見階段。文章或 HTML approval 不授權 Google Doc、CMS、publish、deploy 或 send。

## Intake

用自然語言取得：

- Source：URL、文字、筆記、PDF 或圖片；
- Audience、地區、語言及主要搜尋問題；
- 公司／品牌、Offer、CTA 及可用連結；
- 文章用途及期望格式。

資料不足時使用 `TBC`、`LINK_TBC`、`CTA_TBC` 或 `SOURCE_NEEDED`，不要用假資料填空。

## Non-negotiable boundaries

- Public copy 必須係原創 synthesis；不可貼上、翻譯、輕度改寫或模仿 Source 結構，亦不可公開 Source 名稱、URL、citation 或研究過程，除非有強制披露要求。
- Provenance 只留在內部 Source Guide、Claim Notes、Link Ledger 或 Review Receipt。
- 公司名不等於 Company Brain。使用品牌身份、Offer、proof 或 CTA 前，先讀 Project 提供嘅 Company profile 及 Offer；角色扮演品牌標示 `SYNTHETIC_BRAND`。
- Public link 只限已確認第一方權威／行動頁、站內延伸內容或 CTA direct destination；欠缺或過期目標使用 `LINK_TBC`，不可製造 `href`。
- Local HTML 不包含 Framer、CMS 或發布行為。未確認授權嘅 Source 圖片只可作 `INTERNAL_REVIEW_ONLY`，不可進入公開 copy／export。
- 不可虛構公司能力、案例、價格、結果、第一手經歷、圖片授權或連結；不可保證排名、AI citation、traffic 或 conversion。

## Reference map

| Need | Read |
| --- | --- |
| Phase、Company Brain、link、image and approval gates | [workflow-and-review-gates.md](references/workflow-and-review-gates.md) |
| Search Intent、Content Type and answer structure | [seo-geo-framework.md](references/seo-geo-framework.md) |
| Article voice、Owned Answer Units、SEO／GEO and HTML rules | [writing-style-and-platform-rules.md](references/writing-style-and-platform-rules.md) |
| Final QA | [content-quality-check.md](references/content-quality-check.md) |
| Brief and production output | [article-brief.md](assets/article-brief.md) and [article-output.md](assets/article-output.md) |

Read only the references needed for the current phase. Article drafting requires the writing-style reference; HTML review reuses its Local HTML section.

## Completion receipt

End every phase with：

- `Current phase`；
- `Status`；
- `Confirmed`；
- `TBC / blocked items`；
- `Next approval needed`。

任何 Review Stop、`READY_FOR_REVIEW` 或本機 HTML 都不等於已發布。
