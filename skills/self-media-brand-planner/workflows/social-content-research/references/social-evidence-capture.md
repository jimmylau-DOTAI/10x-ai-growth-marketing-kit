# Social Evidence Capture

Instagram、Carousel、Reel、Screenshot、Image 或 Video source 先讀本檔，再做任何內容分析。目標係保存原始來源中實際可見／可聽證據，唔係從 preview 推測內容。

## 1. Classify and plan

先分類：

- Instagram carousel / photo post；
- Instagram Reel / video post；
- social post with image(s)；
- social post with video；
- user-supplied screenshot(s)；
- user-supplied local video；
- text-only post。

記錄來源、預計要取得嘅 Caption／正文、媒體數量或影片範圍，以及可用 browser、vision、OCR、audio／video 工具。工具不可用時直接標示限制，唔好模擬擷取。

## 2. Retrieve the source and caption

1. 用 browser 開原始 URL；只可使用用戶有權使用、已存在嘅 authenticated local session。
2. 如有 `more`／展開 Caption，先展開再記錄實際讀到嘅全文範圍。
3. 記錄 URL、platform、可見 creator／account、可見日期、實際讀到嘅文字及缺少元素。
4. Search snippet、preview card、OpenGraph 圖、metadata 或 thumbnail 只可作定位，不可代替原始內容。
5. 不繞過 login、private account、paywall、region block、rate limit、CAPTCHA、DRM 或平台限制。

## 3. Capture a carousel

1. 擷取 slide 1，記錄可見 `1/N` 或其他位置提示。
2. 每次只前進一張，擷取每個 unique slide，直到實際最後一張或平台阻止繼續。
3. Content asset 盡量避開 avatar、comments、browser chrome 及重複 UI；保留足以審核來源嘅必要 context。
4. 每張記錄 index、file、capture method、可見 position／count、OCR、visual description、legibility／crop limitation。
5. 未能證實已到最後一張、已知 count 但缺任何 slide，或部分 slide 無法清楚檢查，標 `PARTIAL` 並列出 captured range 同 missing range。

## 4. Capture a Reel or video

1. 先確認真實影片可以播放。Cover image 唔等於影片 evidence。
2. 擷取 cover，以及開頭、主要轉折、關鍵 proof／示範、結尾嘅 representative frames。
3. 如合法取得 local media file／audio stream，先驗證檔案可播放，再做 frame extraction 或 transcription。
4. 只有 browser playback 時，只記錄實際可見 frames／subtitles；除非真實音訊已轉錄，否則要寫 `audio transcript unavailable`。
5. 記錄 duration（如可見）、frames captured、Caption／subtitle／audio states 及 missing evidence。
6. 影片不能播放時只可用 `PARTIAL` 或 `BLOCKED`；不要以 cover 推斷完整內容。

## 5. OCR and visual inventory

每個 content asset：

1. 用 OCR／vision 讀可見文字，盡量保留 line breaks 同 slide／frame attribution；
2. 記錄 layout hierarchy、visual hook、proof device、diagram、CTA、image role 同關鍵 visual motif；
3. 文字太細、模糊、遮擋或裁切時標示 uncertainty，唔可以當成可靠 quote；
4. 分開 `Observed`、`Inferred`、`Not proven`，唔好補寫 Caption、skip 咗嘅 slide、統計、結果、反應或 conversion impact。

## 6. Make a contact sheet

有兩個或以上 captured assets 時：

1. 只由實際 captures 建立 contact sheet；保留原始 pixels，不重畫、不 restyle、不生成替代內容；
2. 每格只用 source media index，例如 `Slide 01`、`Frame 03`；
3. 保留個別 assets 供 audit；contact sheet 唔代替 per-asset OCR／analysis；
4. Channel 支援時將 contact sheet 當 native media 交回用戶，否則回報實際檔案路徑及限制。

## 7. Decide the access state

- `FULL`：Caption／主要文字及所有重要 media 都已實際檢查；Carousel 到最後一張；Reel／Video 已播放並記錄可取得嘅 frames、subtitles／audio boundary。
- `PARTIAL`：Caption、slides、frames、playback、subtitle 或 audio 有任何重要缺口。
- `IMAGE_ONLY`：只有 visual evidence，冇可靠 Caption／完整 post text。
- `BLOCKED`：原始來源因權限、登入、地區、付費牆、平台或技術限制不可檢查。

如不完整，具體寫出 missing／blocked 原因，以及用戶可補交嘅 exported images、screen recording、screenshots、local media 或 copied Caption。

## 8. Store only what is needed

Quick Research 將 evidence 交回用戶但預設唔寫 Vault。Deep SL 獲授權後，保存 Source Receipt、短 excerpt／OCR、structured manifest、analysis 及 retention policy 容許嘅必要 captures。唔好保存完整而不必要嘅受版權保護內容或逐字稿；唔好硬編任何 home／Vault absolute path。
