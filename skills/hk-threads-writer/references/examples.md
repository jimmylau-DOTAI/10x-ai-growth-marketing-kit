# Source-faithful examples

以下係結構示例，唔係已發布內容或 performance evidence。產品能力、link 同第一身經歷要喺實際任務重新核實。每組 `segments` 可複製成 JSON，交畀 `scripts/count_segments.py` 計數。

## `complete-single-500` — `hot-take`

Material boundary：作者只確認自己用緊一個本地筆記庫，同一個可讀取指定資料嘅 AI 工作空間；無效率數字、無普遍結果。

```json
{
  "segments": [
    {
      "id": "root",
      "text": "Obsidian x Claude 最有價值嘅位，唔係又多一個 AI 筆記玩法。\n\n係你終於要面對一個更基本嘅問題：啲資料寫低咗之後，究竟搵唔搵得返、信唔信得過、用唔用得落去？\n\nObsidian 負責保留你揀過嘅資料同脈絡；Claude 可以協助你由指定材料入面整理、比較同起草。\n\n但如果個 vault 本身亂，AI 只會更快咁放大個亂。\n\n所以我會先執命名、source 同版本，再諗 prompt。工具係加速器，唔係知識管理嘅替身。"
    }
  ]
}
```

## `notes-link-reply`

```json
{
  "segments": [
    {
      "id": "root",
      "text": "我整理 AI 筆記 workflow 時，最常見嘅問題唔係唔識用工具。\n\n係一開始就將「收集、判斷、重用」混埋一齊。結果資料愈多，反而愈難信。\n\n我而家會分三層：raw source 保留原文；working note 寫今次判斷；approved note 先畀之後嘅內容重用。\n\n下面放完整欄位同檢查方法。👇"
    },
    {
      "id": "reply-1",
      "text": "完整筆記：\n[LINK TBC]\n\n入面有三層 note 嘅用途、最少 metadata，同埋點樣避免 draft 被當成已確認知識。Link 核實前唔好發布。"
    }
  ]
}
```

## `staircase-thread` — three segments

```json
{
  "segments": [
    {
      "id": "root",
      "text": "AI 寫 Threads 最易出事嘅，唔係文筆差。\n\n係第一句講到太盡，正文又交唔到貨。\n\n我會用三層 Gate 拆：Hook、證據、手機節奏。呢三樣無對齊，寫得再順都只係包裝。"
    },
    {
      "id": "reply-1",
      "text": "▍第一層：Hook\n\n先起幾個角度，但每一個都要指得返正文某段證據或判斷。\n\nL3 可以更尖銳，但只係加強表達，唔可以順手加數字、保證或者「全部人都錯」。"
    },
    {
      "id": "reply-2",
      "text": "▍第二、三層：證據同手機節奏\n\n數字、日期、身份、link 先逐項 read-back；之後先拆段。長句交代脈絡，短句落判斷。\n\n最後用 Python 對每個 segment 跑 len(text)。超過 500 就重寫再計，唔係肉眼估。\n\n如果只做一件事：先確保 Hook 喺正文有 payoff。"
    }
  ]
}
```

## Bad／good mobile paragraph

Bad：

```text
我哋成日以為只要搵到更好嘅 AI 工具就可以解決內容問題但其實真正困難係資料來源、判斷同埋版本管理全部混埋一齊所以每次生成都要重新解釋而且無人知道邊一段係已確認邊一段只係草稿最後就算寫得快咗都未必敢直接用。
```

Good：

```text
我哋成日以為，換個更好嘅 AI 工具就會解決內容問題。

真正困難嘅係：source、判斷同版本混埋一齊。每次生成都要重新解釋，亦無人知邊段已確認、邊段只係 draft。

寫快咗。

但未必敢用。
```

## Same boundary, three Hook Levels

Claim boundary：今次只係作者對自己 workflow 嘅判斷，無聲稱適用所有人。

```json
{
  "segments": [
    {
      "id": "L1",
      "text": "我用 AI 整理筆記之後，最先要改善嘅唔係 prompt，而係 source 同版本。"
    },
    {
      "id": "L2",
      "text": "我改咗好多次 prompt，最後先發現：真正拖慢筆記 workflow 嘅，係 source 同版本根本未分清。"
    },
    {
      "id": "L3",
      "text": "Prompt 寫得再靚都救唔到一個亂 vault。至少喺我個 workflow，先分清 source 同版本，比再改 prompt 重要。"
    }
  ]
}
```
