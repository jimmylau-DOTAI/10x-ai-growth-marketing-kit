# Quality check

## Structure hard gates

- 每張 input 已分 role、rights status 同 exclusions；
- `PREFERENCE.md` 分開 user-confirmed、observed、inferred、treatment、uncertain；
- `STYLE.md` frontmatter 有 `identity_agnostic: true`；
- `STYLE.md` frontmatter 有非 placeholder `proof_modality`、`proof_authenticity`、`visible_attribution_default`；
- `STYLE.md` 有 recognition test、fixed rules、adjustable parameters、break rules；
- `STYLE.md` 有 proof modality／authenticity 同 attribution boundary；
- `DESIGN.md` 有 recognition path、Creative Envelope、palette roles、subject／proof possibilities、proof asset contract、attribution／provenance、content fields、prompt 同 QA；
- 1–6 張 permitted portable visual anchors 已存入 `assets/reference-images/` 並用相對路徑列入 `REFERENCE.md`；冇權利保存圖片時有清楚 external-reference fallback，而且不可聲稱 pack portable；
- campaign／topic／人物／文案／card number／source handle 冇滲入通用 pack；
- Character 同 Style 分開；
- Content Job 同 Style 分開。
- Source identity 已移除，但跨-reference evidence modality 冇被過度刪除；
- internal provenance 同 visible attribution 分開。

任何一項 fail 都不可 save 成 selected Style。

## Evidence score — 100

| Dimension | Points |
|---|---:|
| Reference roles and rights boundary | 10 |
| User preference and evidence separation | 15 |
| Layout／reading path／type system | 15 |
| Subject, proof modality and authenticity | 15 |
| Palette and material role system | 10 |
| Core vs treatment vs content variables | 15 |
| Character／source separation | 10 |
| Cross-job executability and QA | 10 |

- `<70`：`REFERENCE_STUDY`
- `70–84`：`STYLE_PACK_CANDIDATE`
- `85+` + one passing pilot：`PILOT_REVIEW_STOP`
- two materially different passing jobs + explicit selection：`STYLE_SELECTED`

分數唔可以蓋過 hard gate。

## Pilot hard gates

- `visual_intent` 由 approved Style recognition test 判斷，唔係由可用 renderer 倒推；
- Content Job proof modality 符合 Style；`authentic-required` 有真實 asset path、hash 同 rights／claim boundary；
- authentic proof 冇被 generated metaphor、illustrative UI 或重畫 screenshot 代替；generated-allowed job 可以使用 illustrative UI；
- visible attribution 決定已記錄；`forbidden` 成品冇 Source／handle／footnote，但 internal provenance 仍完整；
- image-led／hybrid job 已 route 到可產生完整圖像嘅 production Skill；
- HTML 若存在，已標明 `layout-reference-only` 或符合 layout-led final-render 條件；
- image-led／hybrid passing pilot 至少有一次 image-model call，HTML-only output 不計；
- Render contract 事前鎖定；
- native one-pass route 冇後期修補；
- exact-size route 有實際 dimension read-back；
- required copy、subject、proof、Logo、safe zones、hands、identity 通過；冇假／近似官方 Logo、錯字、無意義典型 AI 味、重複模板或畸形手部；
- output hash、dimensions、path、generation count 已記錄；
- production Skill、HTML role、native／final dimensions 同 deterministic transformation 已記錄；
- failed output 保留證據，但唔做下一張 reference；
- draft／saved／selected／published 狀態誠實。

## Student explanation test

學生應可以用三句說明：

1. 「我鍾意嘅唔係某一隻色，而係……」
2. 「就算轉人物同 topic，仍然要保留……」
3. 「如果改走……，就唔再係同一個 Style。」
4. 「個 proof 一定要真 UI／真物件，定可以係生成 metaphor？」

答唔到代表 Style 仲未真正拆清楚。
