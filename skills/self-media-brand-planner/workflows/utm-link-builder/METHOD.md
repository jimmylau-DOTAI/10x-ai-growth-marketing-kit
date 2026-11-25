---
name: utm-link-builder
description: Build reviewable UTM links for a website, Blog, social post, or ad campaign and maintain the project UTM registry. Use before promoting a live page; do not deploy, publish, buy ads, or connect accounts.
---

# UTM Link Builder

Use this Skill when a user needs a tracked link for Instagram, Facebook, Threads, 小紅書, WhatsApp, Email, an ad, or another promotion.

## What UTM means

UTM is a few labels added after a URL. It tells the company where a visitor came from.

```text
https://your-site.vercel.app/blog/article
?utm_source=instagram
&utm_medium=organic_social
&utm_campaign=blog-launch-sep
&utm_content=carousel-01
```

- `source`：客人由邊度嚟，例如 `instagram`、`facebook`、`threads`、`xiaohongshu`、`whatsapp`；
- `medium`：呢條連結屬於乜，例如 `organic_social`、`paid_social`、`email`、`creator`；
- `campaign`：今次宣傳活動嘅名字，例如 `blog-launch-sep`；
- `content`：同一 Campaign 入面邊一個版本，例如 `carousel-01`、`story-01`、`ad-a`。

同一個 Campaign 可以有多條 link：平台不同，`source` 要不同；同一平台的不同 Post／ad，`content` 要不同。

## Inputs

Before making a link, read the current Project `funnel/utm-registry.csv` when it exists. Ask only for any missing item:

1. destination page URL;
2. platform;
3. organic or paid;
4. campaign name;
5. Post／ad version when there is more than one.

Do not guess the final destination URL. If the Vercel URL is not ready, create a tracking plan only and mark it `PLANNED`.

## Workflow

1. Explain the four labels in one short Cantonese sentence.
2. Build a preview link with `scripts/build_utm_link.py`.
3. Immediately register every generated link with `scripts/register_utm_link.py` as `PREVIEWED`, then show the full URL and the four labels. Every generation is an audit record; never overwrite an older platform／Campaign／version row.
4. After the user confirms the exact link, update that same row to `CREATED_UNPUBLISHED`. If the existing registry has only the original six columns, the script adds `destination_url`, `utm_url`, `created_at`, `verified_submission_id`, and `notes` while preserving every existing row.
5. When the link is actually used and a TEST Lead proves that the UTM fields reached CRM, update that same row to `LIVE_VERIFIED` and record the `submission_id`.

The Skill never publishes a post, changes Vercel, creates an ad, connects Meta, or claims that an untested link is live.

## user prompt

```text
我想由 [平台] 宣傳呢篇 Blog。Campaign 叫 [名稱]，今次係 [自然 Post／廣告]，版本係 [Carousel 01／Story 01／Ad A]。請用 utm-link-builder 先整一條 UTM 預覽連結，講清楚每個標籤代表乜；未確認前唔好出 Post、投放或改網站。
```

## Acceptance

- destination、source、medium、campaign、content 都清楚；
- URL 可打開，原本 query parameters 沒有丟失；
- 每一條新生成的 link 已即時登記為 `PREVIEWED`，或如實標 `PLANNED`；
- TEST Lead 以同一條 UTM URL 進入，才可聲稱 CRM 收到來源資料。
