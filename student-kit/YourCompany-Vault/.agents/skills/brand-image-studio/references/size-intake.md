# 尺寸：沿用已知需求

已指定像素／比例就沿用，不因換工具重問。只有比例及用途時，可按工具能力選合適預覽尺寸並說明；不要把預覽值當平台官方規格。用途／版位不清或要求互相矛盾且影響構圖，才把問題合併到當輪確認。

正式平台交付須核對實際版位要求；自訂尺寸可記 user-specified，不聲稱平台合規。改比例須重構圖而非拉伸；明確修改指令可沿用授權。只加 Logo 沿用原尺寸。

## Final QA 的 request

在生成或改圖前建立 request.json。若草稿已存在，記錄新的定稿操作及其原圖，不回填虛假的出圖前證據。

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

這是格式示例，不是固定要求。platform／placement 可用其他平台或 custom；aspect_ratio 可省略，有填須與像素一致。

basis 用 user_explicit／project_brief／user_confirmed_recommendation／delegated_choice。evidence 保存相關用戶原話或 brief 位置；未確認建議仍 pending，不可標批准。尺寸改變保留舊版本，另建新 request。

Preflight 驗需求一致性與來源檔存在，不驗記錄真實或代客戶批准。delivery 綁定實際 request 及 hash；不能為迎合錯圖倒改需求。
