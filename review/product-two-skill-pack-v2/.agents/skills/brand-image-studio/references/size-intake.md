# 尺寸需求：沿用已知用途，分清預覽與正式規格

已指定用途及比例、但沒有精確像素時，可按下列課堂預覽基準選尺寸並告知，不為像素再問一次：16:9 用 1600×900，4:5 用 1200×1500，1:1 用 1200×1200，3:4 用 1200×1600。這些是本候選的 preview targets，不是平台官方規格或工具保證；request 的 basis 記 project_brief，evidence 指向本條及實際用戶比例要求。工具不支援精確尺寸時如實交比例／尺寸未達標的 preview，不倒改要求以取得 PASS。
用戶有 exact pixels、既有網站欄位或平台正式交付規格時，該要求優先；不套上述預覽值。未知用途真的影響構圖才集中問一次。

## 判斷與一句話問法

- 「做張 IG 圖」→ 問 Feed／Carousel／Story／Cover 及尺寸，未回答不出圖。
- 「4:5」且用途清楚 → 按上方預覽基準準備；若要指定平台正式交付，才核對該版位精確要求。
- 「1080×1920 Story」→ 沿用明確 width／height，直接檢查出圖模式，不再問相同問題。
- 「1200×630 圖」→ 可按 custom／user-specified image 執行；未知網站規格就不聲稱網站規格已驗。
- 「幫我揀尺寸」但用途未知 → 先問用途；用途清楚後建議一個尺寸，等用戶確認。若用戶已明確授權 AI 直接選尺寸，記 `delegated_choice`、其原話及選擇理由，說明採用值後繼續。
- 「已批准的圖片計劃」→ 沿用該 brief 的實際尺寸，不重問。
- 「SEO banner」→ 問網站位置／所需尺寸；未有 CMS 規格只能提出候選，不能把任意橫圖稱為合規 banner。
- 「IG 同另一個平台都要」→ 每個 placement 分開確認 target；可一次問齊，分 job 製作／驗收。
- 「將 1080×1350 改 1080×1920」→ 係改構圖比例，選 native-recompose 並確認要保留的文案／主體；不以拉伸冒充。只加 Logo 沿用現有 job target。

同時收到互相矛盾的 pixel size／ratio／brief，而未清楚係新指令取代舊版，要先澄清。不將輸出錯尺寸倒寫成用戶要求。

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
