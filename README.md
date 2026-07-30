# 10x AI Growth Marketing Kit

呢個係一個俾香港 Marketer、中小企團隊及 AI 課程學員測試嘅四 Skill Package。

版本：`v0.1-team-test`

## 四個 Skills

| Skill | 用途 | 主要輸出 |
| --- | --- | --- |
| `social-content-research` | 研究 YouTube、IG、Facebook、Threads、LinkedIn、X、截圖或逐字稿 | Access state、內容分析、風險、原創角度 |
| `full-funnel-campaign-planner` | 由 Offer 或 Campaign Idea 建立 Full Funnel | Current state、Grill Me、Funnel、90 日優先次序、Handoffs |
| `seo-geo-content` | 建立 Search-led、SEO 及 GEO 內容 | Intent brief、Claim map、Outline、Article、QA |
| `social-post-writing` | 將可靠觀點改寫成平台原生社交文案 | Threads、LinkedIn、Facebook、Instagram Draft Pack |

## 點樣一齊用

```text
來源或社交內容
    ↓
social-content-research
    ↓
full-funnel-campaign-planner
    ├── seo-geo-content
    └── social-post-writing
    ↓
Human review
```

每個 Skill 亦可以獨立使用。

## 安裝

### 方法一：放入 Project

將 `skills/` 入面四個 Folder 複製到目標 Project：

```bash
mkdir -p .agents/skills
cp -R skills/. .agents/skills/
```

### 方法二：個人安裝

Codex：

```bash
mkdir -p ~/.codex/skills
cp -R skills/. ~/.codex/skills/
```

Claude Code：

```bash
mkdir -p ~/.claude/skills
cp -R skills/. ~/.claude/skills/
```

重新開啟 Agent Session，確保 Skills 被重新載入。

## 最簡單測試方法

先明確叫 Skill 名稱：

```text
Use $social-content-research to analyse this post.
```

```text
Use $full-funnel-campaign-planner to plan this launch.
```

```text
Use $seo-geo-content to create a source-backed article.
```

```text
Use $social-post-writing to adapt this idea for LinkedIn and Threads.
```

完整測試情境及 Pass Criteria 見 [TEAM-TEST-GUIDE.md](TEAM-TEST-GUIDE.md)。

## 共通安全界線

- 不會因為資料不足而虛構公司、客戶、合作、數字或成效；
- Draft 不等於 Approved；
- Approved 不等於 Published；
- 不會自動發佈、發訊息、花廣告預算或處理客戶資料；
- 涉及時效性、法律、產品功能或外部 Claim 時，需要核實當前來源；
- 最終對外內容需要人手 Review。

## Package 原則

- 每個 Skill 只有真正執行工作需要嘅 Files；
- `SKILL.md` 負責 Routing、Workflow 及硬界線；
- `references/` 放需要時先讀嘅詳細框架；
- `assets/` 放可以複製使用嘅 Brief 或 Output Template；
- 第一版不加入自動 Scraping、Database、API Publishing 或多餘 Scripts。

## 授權狀態

呢個版本只供團隊測試，暫未附帶公開分發 License。公開 Repository 前，請先確認 License、品牌名稱、案例、第三方資產及示範內容嘅分發權。

參考來源及原創界線見 [ATTRIBUTIONS.md](ATTRIBUTIONS.md)。

