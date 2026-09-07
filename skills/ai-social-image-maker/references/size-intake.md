# 尺寸需求

沿用今次明確要求／已批准 brief；用戶授權自選時按用途選並講明理由。用途、像素或互相矛盾資料會影響製作先問，已有完整尺寸不重問。只講 IG 或 4:5 時，先確認 placement 與像素；1080×1350 是第三堂既有 Carousel brief，不是跨平台規則。自訂像素可記 custom，唔為填平台欄追問無關資料。

不同 placement 各自記 target。改比例需重新構圖，加 Logo 沿用 target。網站尺寸不明只提候選，唔聲稱已符合 CMS 規格；最新平台規則有需要才查官方資料。

## request.json（由 AI 寫，在生成之前）

```json
{
  "schema_version": 1,
  "platform": "Instagram",
  "placement": "lesson3-carousel",
  "width": 1080,
  "height": 1350,
  "aspect_ratio": [4, 5],
  "basis": "project_brief",
  "evidence": "size-source.md"
}
```

platform／placement 是開放文字，支援其他平台及 custom image。aspect_ratio 可省略；有填就必須與像素一致。
basis：`user_explicit`／`project_brief`／`user_confirmed_recommendation`／`delegated_choice`。證據檔保留相關用戶原話或精確 brief 位置及尺寸，不能只寫 PASS。建議未獲確認記 `pending`，不可算需求完成。

Preflight 只驗需求是否完整一致及來源檔存在，不會替用戶批准，也不能證明記錄真實。尺寸變更另存 request-v2.json／新 job，保留原版本；delivery 綁定實際使用的 request 及 hash。
