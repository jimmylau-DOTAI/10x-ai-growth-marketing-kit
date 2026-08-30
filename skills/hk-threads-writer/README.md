# HK Threads Writer

一個品牌中立、可攜式 Agent Skill，用自然香港廣東話寫、改寫及 QA Threads 文案。佢會按證據揀內容 job、調節 Hook 強度、處理手機閱讀節奏，並用 Python 對每個可發布 segment 執行 500 字硬性 Gate。

Package 只產生 draft，唔會登入、發布、排程或修改 Threads 帳戶。

## What it handles

八個 content jobs：

- `hot-take`：有立場、有可解釋理由；
- `reaction`：回應目前可核實 source；
- `personal-story`：真實第一身場景同轉折；
- `build-note`：真實 artifact、進度或失敗；
- `review`：實際體驗，或披露 research-only；
- `anti-pattern`：拆失敗機制同替代做法；
- `curated-list`：有多個選項同選擇準則；
- `how-to`：可重做步驟及成功／失敗 check。

三個 delivery modes：

- `complete-single-500`：一段完成 Hook、解釋／例子同判斷；
- `notes-link-reply`：有獨立價值嘅 root，加第一個 self-reply link；
- `staircase-thread`：多段有次序推進，每段一層，最後先放 CTA。

Hook Levels 由克制嘅 L1、預設有反差嘅 L2，到表達更尖銳嘅 L3。L3 只提高 expression strength，唔會提高 claim strength。

## Source and identity safety

Skill 會保護數字、日期、價錢、名稱、URL、引句、術語、承諾、身份同 evidence status。無第一身證據就唔會發明「我試過」；無已核實 link 就使用 `[LINK TBC]`；draft、prototype 同 published 狀態唔會混寫。

## Use

如果已放入 Codex skills directory，可以用：

```text
Use $hk-threads-writer to turn the supplied source into a L2 notes-link-reply draft.
```

亦可以直接要求：

```text
用香港廣東話將呢段材料寫成 Threads hot take。手機分段要清楚，每段用 Python 計 500 字，唔好發布。
```

手動放入 skills directory 嘅例子（只係安裝示例，執行前自行核對目標位置）：

```bash
cp -R hk-threads-writer ~/.codex/skills/
```

本 repository 未因為呢段示例而執行安裝。

## Deterministic count gate

準備 JSON：

```json
{
  "segments": [
    {"id": "root", "text": "第一段文案"},
    {"id": "reply-1", "text": "第一個 self-reply"}
  ]
}
```

執行：

```bash
python3 scripts/count_segments.py segments.json
```

每個 segment 獨立使用 Python `len(text)`；空格、換行、English、符號、emoji 同 link 都會計。任何一段超過 500，command 會以 exit code `1` 結束；script 唔會截斷或改寫文案。

## Package structure

```text
SKILL.md                 Runtime router and hard gates
agents/openai.yaml       UI metadata and invocation policy
references/              Jobs, Hook, mobile rhythm, HK language and safety
scripts/count_segments.py  Deterministic per-segment counter
tests/                   Package and script contract tests
evals/                   Behavioral cases and human-review benchmark
```

## Validate

```bash
python3 -m unittest discover -s tests -v
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

第二條 command 適用於已包含 `skill-creator` 嘅 Codex 環境；其他 Agent 可以用自己嘅 Skill validator。`quick_validate.py` 檢查 Skill 結構同 frontmatter；佢唔證明廣東話自然。公開使用前仍然需要香港讀者 Human Review，同埋用真實 source 做 behavioral eval。

## License and references

Package 以 MIT License 提供。上游機制參考及未直接搬用嘅平台規則見 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
