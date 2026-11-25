---
name: toapis-image-creator
description: Prepare or run one ToAPIs image task after a user selects a model, complete brief and budget. Use for a fast paid image-model route; not for automatic retries, publishing or unapproved paid generation.
---

# ToAPIs Image Creator

ToAPIs is one API gateway for different image models. It is useful when a team wants to compare a named model, generate a complete image quickly, or keep image requests under one API account. It is **not** a Style, and it does not make the source, claim, Logo or CTA correct by itself.

## Start with the right state

Read the current content brief, approved Style, platform size, supplied reference assets and the requested outcome. Check the live official pages before the first task of a session:

- Website and account: https://toapis.com/en
- Model market: https://toapis.com/en/market
- Current price: https://toapis.com/en/pricing
- GPT-Image-2 guide: https://toapis.com/en/model-guide/gpt-image-2

The price and speed figures on those pages are vendor-listed snapshots, not a promise. As checked on 2026-09-07, the GPT-Image-2 guide listed 1K at US$0.015/image and an 8-second average; final price, queue time and supported parameters follow the user's own account and the live model page.

If no account/API key is configured, prepare the brief and point the user to the website. Do not request, store or expose a key. Do not claim that an image was generated.

## One-image workflow

1. Explain the selected model in one sentence: what visual job it suits and why it is being used today.
2. Build one complete brief: purpose, audience, ratio, subject, reading order, scene, materials/light, supplied reference roles, required copy, real Logo asset, KEEP/CHANGE/BAN list and factual limits.
3. State: `今次會用 ToAPIs 做一張完整圖；這是一個付費 API 任務。` A clear request to generate authorizes one image only.
4. Submit one task only when the user has selected the image, model and budget. Keep the task ID, actual model, dimensions and local output path.
5. If queued or timed out, resume/check the same task. Never auto-submit a retry, a different model, a variation, an upscale or a second image.
6. QA the downloaded file: it opens, ratio is right, requested subject and composition are present, and any obvious text/Logo/anatomy issue is reported. A pass is local review, never publication.

## Example request

```text
我想用 ToAPIs 試一張完整圖片。先讀我已確認的內容、Style 和真品牌資產，
建議一個適合今次目的的模型和原因，並核對官方現時價格與尺寸支援。
幫我寫一張 4:5 圖的完整 Brief：保留、嘗試、禁止各是甚麼。
未得到我「開始生成一張」的確認前，不要呼叫 API 或花費。
```

## Boundaries

- 只用原資料支持的產品事實、服務流程、交付證據與客戶聲音；未知寫 TBC。
- 真 Logo、可讀中文、確切 UI 或法規／醫療 claim 要有 supplied asset/evidence；不要讓模型幻想成真。
- ToAPIs image-to-image/editing requires the current model's documented reference support. Verify it before a call.
- This Skill does not create a video, publish a post, buy ads, connect accounts or save credentials.
