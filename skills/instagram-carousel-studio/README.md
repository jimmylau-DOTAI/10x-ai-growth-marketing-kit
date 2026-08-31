# Instagram Carousel Studio

將一個 Source、Brief 或你自己嘅見解，重新編排成一個完整 Instagram Carousel：

`Brief → Audience → One Message → Creator Judgment → Carousel Story → Human Review → AI Image Handoff → QA → Learning Log`

呢個 Skill 專心處理內容策略同故事順序。佢唔需要揀 Style，亦唔會先砌 HTML；完整內容批准後，直接交俾 [`ai-social-image-maker`](../ai-social-image-maker/) 逐張製作成品圖。

## 你會得到甚麼

- 預設 10 張、每張 `1080×1350px`；
- 明確目標受眾、One Message 同 Creator Judgment；
- 最多五個有受眾指向嘅標題／角度；
- 一個由頭到尾成立、每張只有一個工作嘅 Carousel Story；
- 完整 Content Plan Human Review；
- 可直接交俾 AI 圖像 Skill 嘅 Handoff；
- Project-local `PREFERENCES.md`；
- 自動 Learning Log 同三次可比較使用嘅成長循環。

## 安裝

### Codex

```bash
npx --yes skills add jimmylau-DOTAI/10x-ai-growth-marketing-kit \
  --skill instagram-carousel-studio -g -a codex -y
```

圖像製作需要同時安裝：

```bash
npx --yes skills add jimmylau-DOTAI/10x-ai-growth-marketing-kit \
  --skill ai-social-image-maker -g -a codex -y
```

### Claude Code

```bash
npx --yes skills add jimmylau-DOTAI/10x-ai-growth-marketing-kit \
  --skill instagram-carousel-studio -g -a claude-code -y
```

安裝後開新 Session：

```text
Use $instagram-carousel-studio。

我想將以下 Source 做成 Instagram Carousel：
[貼上文章、對話、截圖、筆記或 URL]

Audience：
我自己嘅見解：
CTA：
參考圖：[可選]
```

## 工作方法

### 1. 先講清楚係寫俾邊個

AI 會先鎖定 Objective、Audience、受眾而家嘅誤解、One Message、Source boundary、Creator Judgment 同 CTA。未清楚「邊個點解要理」之前，唔會急住寫十張。

### 2. Source 唔等於成品觀點

Skill 會分開：

- Source 已確認講過乜；
- 你對件事嘅判斷；
- 為目標受眾重新編排後，最值得帶走嘅一個 Message。

所以輸出唔係將原文拆十段，而係一個有開場、推進、Reframe、應用同 CTA 嘅故事。

### 3. 唔使揀 Style

Project 只會維護一份 `PREFERENCES.md`。有就自動沿用；冇就先用中性、清晰、內容優先嘅預設開始。你提供五張鍾意嘅圖時，AI 可以拆解共同偏好，但唔會叫你喺 A／B／C／D 中揀一款。

### 4. 完整內容批准後直接做圖

Skill 會一次過展示完整 Content Plan，停在 `CAROUSEL_PLAN_REVIEW_REQUIRED`。你明確批准後，先交俾 `ai-social-image-maker`：

```text
C01 pilot → Human Review → remaining cards → contact-sheet QA
```

每張係一個完整、扁平化嘅成品圖；冇 HTML 排版中間層。AI 生成文字同 Logo 仍可能出錯，重要字句同品牌資產一定要人手檢查。

## Learning Log 同三次成長 Loop

每次 Human Review 後，Project 會記錄：

```text
KEEP / CHANGE / BAN / WHY
→ bounded candidate
→ 1/3 → 2/3 → 3/3 comparable carousel uses
→ exact proposed PREFERENCES.md update
→ Human Review
→ approved writeback
```

一個十張 Carousel 只計一次，修改同一個 Carousel 唔會扮成新證據。三次只會自動產生建議，唔會自動改 `PREFERENCES.md`，更加唔會自動改公開 Skill。

如果你直接講明「以後唔好再用某種做法」，可以記作 `direct-confirmed`，無需假裝等三次先承認你嘅明確偏好；正式寫入仍要 Human Review。

## 手動建立同驗證 Project

```bash
python3 scripts/create_project.py \
  --project-dir "/absolute/path/to/my-carousel-project" \
  --project-name "My Carousel Project"

python3 scripts/validate_project.py \
  --project-dir "/absolute/path/to/my-carousel-project"
```

加 `--strict` 會在 Brief、偏好或 Content Plan 仍有 `TBC` 時停止。

## 重要邊界

- `CAROUSEL_PLAN_APPROVED` 唔等於圖像已生成；
- Local PNG 或 `FINAL_DRAFT_READY` 唔等於已發布；
- Skill 唔會自動發 Instagram、設定自動回覆、上載 CRM 或修改外部 Vault；
- Publish、Send、Deploy、Schedule 或 Live Automation 需要另行批准同目的地 read-back；
- 參考圖只用嚟學習可描述嘅偏好，唔複製另一位創作者嘅品牌身份、文案或 Claims。
