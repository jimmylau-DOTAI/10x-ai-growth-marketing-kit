# AI Social Image Maker

將一份已批准嘅 Content Plan，直接逐張生成完整 Social Image：

`Approved Plan → C01 AI Image → Human Review → Remaining Images → Contact-sheet QA`

冇 HTML，冇「先整背景再疊字」，亦唔會一次生成十格拼圖。每張都係一個完整、扁平化、可直接審閱嘅 `1080×1350px` 圖像。

## 安裝

### Codex

```bash
npx --yes skills add jimmylau-DOTAI/10x-ai-growth-marketing-kit \
  --skill ai-social-image-maker -g -a codex -y
```

### Claude Code

```bash
npx --yes skills add jimmylau-DOTAI/10x-ai-growth-marketing-kit \
  --skill ai-social-image-maker -g -a claude-code -y
```

## 使用方法

做單張圖：

```text
Use $ai-social-image-maker。

Audience：
Message：
Visible copy：
Preferences／參考圖：
```

做 Carousel，建議先用 [`instagram-carousel-studio`](../instagram-carousel-studio/) 完成內容：

```text
Use $ai-social-image-maker，根據已批准 content-plan.md 生成 C01。
```

## 硬性流程

1. 完整 Carousel Plan 要有明確 `CAROUSEL_PLAN_APPROVED`；
2. 只生成 C01；
3. 讀返實際圖片、尺寸、文字同品牌處理；
4. 停在 `C01_REVIEW_REQUIRED`；
5. 只有明確 `C01_APPROVED` 先生成其餘圖片；
6. 每張一個獨立 ImageGen call；
7. 完成後逐張 QA，再睇 Contact Sheet。

每張預設只生成一次。只有清楚命名嘅 Hard Blocker，例如主體錯誤、文字不可讀、出現假 Logo，先可以針對問題再試一次。

## 100% AI 圖像代表甚麼

代表一張完整 Final Image 由圖像模型一次生成，唔經 HTML 排版中間層。但唔代表 AI 對中文字、數字、Logo 或 UI 可以 100% 準確。

- 重要 Claim 一定要 Human Review；
- 冇官方 Logo 檔時，唔會叫 AI 畫一個似樣嘅假 Logo；
- 純 AI 做唔到精準文字時，會標示 `DETERMINISTIC_FINISH_RECOMMENDED`；
- Local PNG 唔等於已發布。

## 邊界

呢個 Skill 唔負責揀題目、寫完整 Carousel Story、改 `PREFERENCES.md`、發布、Schedule 或設定自動回覆。內容策略交俾 `instagram-carousel-studio`；偏好更新必須經 Human Review。
