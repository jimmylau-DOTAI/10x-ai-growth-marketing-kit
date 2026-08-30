# Instagram Carousel Studio

將一個 Source、教學題目或框架，逐步變成一個可審核嘅 Instagram Carousel：

`Brief → 題目及標題 → 四款 Style → 10 張內容 → Editable HTML → Human Review → HTML／AI 圖像 → QA → Project-local Learning`

呢個 Skill 唔係一次過亂生十張圖。佢會先幫你鎖定內容同 Style，再做可修改 HTML，最後先按需要生成圖像。

## 你會得到甚麼

- 預設 10 張、每張正確 `1080×1350px`；
- 五個標題方向及一個完整故事節奏；
- Existing Style、參考圖拆解或四款 Starter Styles；
- 同一份封面內容嘅 A／B／C／D Style 比較；
- 可直接審閱及修改嘅 HTML Carousel；
- 可選 HTML Final 或一次生成嘅 AI-image Final；
- Logo、中文字、CTA、尺寸及內容密度 QA；
- 只屬於目前 Project 嘅 Learning receipt。

## 安裝

### Codex

```bash
npx --yes skills add jimmylau-DOTAI/10x-ai-growth-marketing-kit \
  --skill instagram-carousel-studio -g -a codex -y
```

### Claude Code

```bash
npx --yes skills add jimmylau-DOTAI/10x-ai-growth-marketing-kit \
  --skill instagram-carousel-studio -g -a claude-code -y
```

安裝後重新開一個 Agent Session，直接講明 Skill 名稱：

```text
Use $instagram-carousel-studio。

我想將以下題目／Source 做成一個 Instagram 教學 Carousel：
[貼上題目、文章、筆記或 URL]

Audience：
CTA：
Brand Logo／參考圖：[如有就提供]
```

如果你唔用 Terminal，可以[下載整個 Repository ZIP](https://github.com/jimmylau-DOTAI/10x-ai-growth-marketing-kit/archive/refs/heads/main.zip)，解壓後取出：

```text
skills/instagram-carousel-studio/
```

## 第一次使用會發生甚麼

### 1. 先鎖定 Brief、題目同標題

AI 會先確認：

- 想達成甚麼目的；
- 邊個會睇；
- 成個 Carousel 只想講清楚邊一個重點；
- 可用 Source 同 Claim 邊界；
- CTA 同語言；
- Card 數量，預設 10 張。

未選定標題之前，唔會急住寫晒十張。

### 2. 再選 Style

Skill 會按照以下次序處理：

1. Project 已有批准 Style：直接使用；
2. 你有參考圖：先拆解 Layout、字體、顏色、質感、焦點、Logo zone 同禁用元素；
3. 兩樣都冇：用同一份封面內容比較四款 Starter Styles。

四款 Starter Styles：

| Style | 適合內容 | 主要感覺 |
|---|---|---|
| A — Editorial Contrast | 觀點、策略、Reframe | 強字體、非對稱、Editorial 對比 |
| B — Dark System | AI、Workflow、技術框架 | 深色 Layer、發光焦點、系統結構 |
| C — Product Visual | 工具、痛點、Before／After | 大型立體主角、產品視覺、清晰焦點 |
| D — Tactile Explainer | 步驟、比較、教學模型 | 立體模組、關係圖、可見流程 |

可以直接打開 [`assets/style-picker.html`](assets/style-picker.html) 查看中性示例。四款比較只會改設計機制，標題、承諾、CTA 同品牌輸入保持一致。

### 3. 建立一個完整 10 張故事

預設節奏：

```text
Cover
→ 讀者現況
→ 常見誤判
→ 核心 Reframe
→ 四個 Layer／步驟／例子
→ 實際應用
→ Summary + CTA
```

每張都要有一個工作、一句 Lead、支持內容同 Visual role。純粹張圖靚、但冇知識點，會被 QA 擋住。

### 4. 先睇 Editable HTML

Skill 會使用 `assets/carousel-card-template.html` 建立十張 `1080×1350px` HTML cards。

HTML 用嚟確認：

- 故事係咪順；
- 中文字眼係咪準；
- 每張資訊夠唔夠；
- 標題、圖像同 CTA 焦點；
- Logo 位置同背景對比。

狀態會停在 `HTML_REVIEW_REQUIRED`。你批准後先進入 Final。

### 5. 選擇 Final 做圖方法

#### HTML Final

適合文字、Diagram、比較表或品牌排版需要完全準確嘅 Carousel。

#### AI-image Final

適合需要大型視覺主角、立體效果、情境或強烈痛點畫面嘅 Carousel。

預設每張只生成一次，唔會先生成一輪再無限重做。重要中文、CTA keyword 同官方 Logo 應使用 deterministic HTML／後期處理；AI 唔應該重新畫一個近似 Logo。

## Logo 同 CTA

- 提供官方 Logo 檔案，唔好只提供品牌名；
- Logo 只需要一個局部乾淨 safe zone，唔代表成個背景要變純色；
- 深色局部背景用白色 Logo，淺色局部背景用黑色／深色 Logo；
- 如果 CTA 係留言攞 Guide，用一個短而清楚嘅英文大寫 Keyword；
- Cover、最後一張、Caption、下載內容同 Automation route 必須完全一致；
- 真實下載內容或 Automation 未確認時，Skill 會標示 `NEEDS_LIVE_AUTOMATION`，唔會當成已交付。

## Learning Loop 點保存

Learning 預設只留喺你目前嘅 Carousel Project：

```text
Human Review
→ KEEP / CHANGE / BAN / WHY
→ Run receipt
→ 明確批准先保存 Candidate
→ 三個獨立 Carousel 出現同一訊號
→ Proposed Style Update
→ Human Review
→ 更新 Project-local Style Capsule
```

一個十張 Carousel 只計一次使用，唔係十次。Skill 唔會自動修改共用 Skill、其他品牌 Style、外部 Vault 或 Shared Memory。

## 手動建立 Project Folder

通常你只需要叫 Agent 使用 Skill。想手動初始化，可以在 Skill folder 執行：

```bash
python3 scripts/create_project.py \
  --project-dir "/absolute/path/to/my-carousel-project" \
  --project-name "My Carousel Project"
```

完成後驗證：

```bash
python3 scripts/validate_project.py \
  --project-dir "/absolute/path/to/my-carousel-project"
```

加上 `--strict` 會在 Brief 或內容仍有 `TBC` 時停止。

## 重要邊界

- Local HTML、PNG 或 `FINAL_DRAFT_READY` 都唔代表已發布；
- Skill 唔會自動發 Instagram、設定 ManyChat、上載 CRM 或修改外部資料；
- Publish、Send、Deploy、Schedule 或 Live Automation 需要你另行批准及驗證真正目的地；
- 參考圖只用嚟拆解設計機制，唔應該複製另一個創作者嘅品牌身份、文案或 Claims。
