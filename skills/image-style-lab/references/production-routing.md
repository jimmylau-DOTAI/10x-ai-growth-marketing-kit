# Pilot production routing

## Aim

Style Lab 負責定義同驗證 Style；真正輸出必須由符合視覺機制嘅 production capability 執行。Runtime 要自己 route，唔可以要求用戶先識得叫 image Skill。

Production medium 之前先過 Evidence Modality Gate。Renderer 唔可以改寫 Style：真 UI proof 唔會因為 image model available 就變 generated metaphor。

## Pilot Fit Gate

1. 從 `STYLE.md` 讀 `proof_modality`、`proof_authenticity`、recognition test 同 break rules。
2. 從 Content Job 讀 `proof_asset_path／hash`、rights、claim-critical crop、visible attribution。
3. `authentic-required` 而 asset 缺失／未核實：停止 `BLOCKED_PROOF_ASSET`。
4. Authentic screenshot／Dashboard 可由 deterministic layout framed，或作為 complete-image composition 的不可重畫 proof layer；不可叫 model 模仿、生成或改寫 claim-critical UI。
5. Job proof modality 同 Style 不符：return to Style／Job review；唔可以將 output 當 pilot evidence。

## Decide the visual intent

從 approved `STYLE.md` recognition test、fixed rules、treatment 同今次 Content Job 判斷：

| Visual intent | Recognition depends on | Required pilot medium |
|---|---|---|
| `image-led` | generated scene、illustration、photographic material、native image composition、人物或環境語意；Style 容許 generated modality | `image-generation` or `hybrid` |
| `layout-led` | typography、grid、vector geometry、real supplied UI／Dashboard／artifact、deterministic chart／diagram | `deterministic-layout`; image generation remains optional |
| `hybrid` | authentic proof asset plus generated surrounding scene，或 generated visual plus exact copy／Logo／export | `hybrid`，但 claim-critical authentic proof 不可重畫 |

如果 reference 明顯係 image-led，而 output 只保留 headline hierarchy／box layout，代表只測試到 layout，未測試到 Style。

## Creative Envelope handoff

每個 pilot 只傳一份精簡合約：

- `LOCK`：card／image job、第一眼訊息、required copy、approved identity／Logo／proof、Style recognition test、format 同 claim boundary；
- `FLEX`：構圖、主體位置、比例、字體關係、留白、視覺比喻、景深、illustrative UI、palette treatment；
- `BAN`：假／近似官方 Logo、錯字或未批准文字、無意義典型 AI 味、重複模板、畸形手部／人體，加上用戶明確確認嘅 project-specific 禁項。

Illustrative UI 可以係 generated-allowed。只有 Content Job 將 UI 定義成 authentic／claim-critical proof 時，先禁止生成或改寫。

## Capability handoff

1. 先 audit runtime 已有 image-production Skill／tool；選最窄、能產生完整圖像而非背景 asset 嘅 capability。
2. 在 `CONTENT-JOB.md` 記錄實際 `production_skill`，並傳入 Creative Envelope、獲准嘅 1–3 張最相關 visual anchors／assets 同 render contract。唔好每張圖載入全部歷史 references。
3. Image-led／hybrid 而有可用 capability：必須 handoff，status 可設 `PRODUCTION_HANDOFF_READY`。
4. Image-led／hybrid 但冇可用 capability：`BLOCKED_RENDER_CONTRACT`；回報缺咩能力。唔好改用 HTML 冒充完成。
5. 不在 public Skill 寫死某個私人 Skill 名；由 runtime 按當前可用 capability 選擇並留 receipt。

## HTML roles

- `none`：冇 HTML。
- `layout-reference-only`：鎖定 copy、ratio、safe areas、proof map 或畀 downstream image Skill 做 complete-image pass。只係 handoff artifact，唔係 pilot output。
- `final-render`：只可用於 `layout-led + deterministic-layout`，或用戶明確改變 output medium。不可用於 image-led／hybrid pilot。

HTML reference 可有內部 QA，但唔可以：

- 寫入 `tested_jobs`；
- 提高 cross-job evidence score；
- 用 `PILOT_REVIEW_STOP` 表示 image-led Style 已證明；
- 被描述成 image-generation output。

## Render contracts

### Native one-pass

- 一個 image-model call 產生完整圖；
- 禁止後期修補；
- 接受 renderer 原生尺寸；
- 一次 targeted retry 上限，只處理 hard blocker。

### Exact-size production

- 若 image renderer 支援 exact target，直接生成並 read back。
- 若只支援同 aspect ratio 的其他尺寸，可生成完整圖後 deterministic resize；記錄 native、final dimensions 同 transformation。
- Aspect ratio 不同時禁止 crop 隱藏失敗；最多一次 targeted retry，仍不合就 `BLOCKED_RENDER_CONTRACT`。
- Official Logo／brand asset 可按 Content Job deterministic lock；不可由模型重畫。
- Authentic UI／Dashboard proof 可作 supplied asset composited／framed；唔屬禁止嘅文字修補，但必須保持 claim-critical pixels、記錄 asset hash，並且不可被模型重畫。
- Deterministic wrapper 只做已聲明嘅 size／brand lock，唔可以把 image-led output 改造成另一個 HTML layout。

## Pilot receipt

到 `PILOT_REVIEW_STOP` 前必須記錄：

- `visual_intent`；
- `pilot_medium`；
- `production_skill`；
- `html_role`；
- `fallback_policy`；
- image-model call count；
- output path、SHA-256；
- native dimensions、final dimensions；
- deterministic transformation；
- failed attempts and retry count；
- proof modality、authenticity、asset path／hash、fidelity and substitution decision；
- internal provenance and visible attribution decision；
- Visual Style mechanism QA；
- current approval／publish state。

Image-led／hybrid job 若 image-model call count 係 `0`，一定唔可以成為 passing pilot。
