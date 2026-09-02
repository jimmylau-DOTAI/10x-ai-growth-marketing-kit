# Creator-led and background-scene modes

## Purpose

提供一個可移植嘅「有人像教學圖」起點，同時保持 Style、人物身份同今次內容獨立。

## Mode A — creator-led-cover

適合封面、教學 promise、比較、產品示範。

閱讀順序：

```text
dominant headline → recognisable creator → one semantic proof system
```

- Creator 係第二焦點，通常 28–55% canvas width。
- Proof 必須將 headline 變成具體方法、流程、比較或結果；唔可以只放 random icon。
- Publisher Logo 固定 quiet zone；content-brand Logos 屬 proof，角色分開。
- 人物可用 gaze、body direction、overlap 或一個簡單 contact point 連結 proof。

## Mode B — background-scene-information-front

適合 carousel 內頁或資訊較多嘅 social post。

```text
message → information geometry → reading path
        + low-salience creator scene → identity、depth、atmosphere
```

- Foreground information：65–80% visual attention。
- Creator／scene：20–35%，但面、眼鏡、髮型等 anchors 仍可辨識。
- Scene 至少提供兩項：direction、depth、metaphor、negative space、semantic light。
- 人物唔需要指住文字或拎 Logo；背景 mode 預設零手部接觸。
- 唔好十張都放右上角；改變 crop、anchor、gaze、scene geometry 同 information archetype。

## Character file

只記錄肉眼可見身份 anchors：髮型、眼鏡、輪廓、服裝 anchor、允許表情／crop、禁止改動。避免敏感特徵推論。

至少兩個 materially different accepted views／actions，先可以由 `draft` 升為 `locked`。

## Hand-complexity budget

- Background mode：`0` contacts。
- Cover／active mode：預設 `1` active hand + `1` contact point。
- Inactive hand：自然放鬆、清楚可見，或完全離場。
- Prompt 前寫明 active hand、wrist entry、object、contact point、inactive hand、no-cross zone。
- Extra fingers、broken wrist、impossible reach、floating press、穿過物件或爭議手勢都係 hard FAIL。
- 失敗手部圖不可做下一張 pose／composition reference。

## Logo and brand proof

- 使用獲批准 asset；唔靠模型記憶重畫 Logo。
- Publisher mark 只負責署名；content brand 只負責解釋今次主題。
- 每個 Logo 有一個 semantic owner、anchor、contrast variant、quiet zone 同 failure rule。
- 一次生成模式下，Logo 遺漏／變形／串字要求完整重生；唔可以後加再聲稱 one-pass。

## Failure tests

- 移除人物後完全冇影響，而且人物只係裝飾：creator relationship fail。
- 背景人物變第一焦點：foreground-dominance fail。
- 只換人像同顏色就聲稱係學生個人 Style：extraction fail。
- 封面同所有內頁都複製同一 hero pose：system reuse fail。
