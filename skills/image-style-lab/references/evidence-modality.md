# Evidence modality and attribution boundary

## Why this gate exists

Identity subtraction只係移除 source-owned 身份，唔係將所有 proof 都泛化成「任何能解釋概念嘅物件」。如果多張 reference 都由真實 UI、Dashboard、文件、實物或 screenshot 完成說服，呢種 `how the proof is embodied` 可能就係 Style identity。

## Two questions for every proof region

1. `What does it prove?`：今次內容、產品、結果或 claim，屬於 Content Job。
2. `How is proof embodied?`：真實 UI screenshot、真 dashboard、實物相、faithful data render、generated metaphor 或純裝飾，可能係可重用 Style mechanism。

唔可以用第一題係 job-specific 作理由，連第二題一齊刪走。

## Modality vocabulary

每張 reference 的主 proof 只揀一個 primary modality：

- `authentic-ui-screenshot`：真實產品／網站／App 介面截圖；
- `authentic-dashboard-screenshot`：真實 dashboard 或 analytics UI；
- `authentic-document-capture`：真實文件、post、report 或頁面 capture；
- `authentic-object-photo`：真實產品、實物或成果相；
- `faithful-data-render`：由可驗證數據 deterministic 繪製的 chart／diagram；
- `generated-metaphor`：模型生成、用來解釋概念而非充當真實證據的場景／物件；
- `illustrative-ui`：模型生成、用來解釋流程或概念而唔冒充真實產品畫面嘅 UI；
- `decorative-scene`：只提供氣氛，唔係 proof；
- `mixed`：兩種 modality 都不可移除，必須列明 primary／secondary。

另記：

```yaml
proof_authenticity: authentic-required | authentic-preferred | generated-allowed | not-proof
proof_fidelity: exact | claim-critical-region | structural | atmospheric
proof_legibility: thumbnail | mobile | close-inspection
identity_exclusions: []
visible_attribution: required | optional | forbidden
```

## Cross-reference intersection rule

如果同一 modality：

- 出現在大部分或全部 reference；
- 佔最大或第二大視覺面積；
- 直接完成 headline 的說服；

就先列為 `OBSERVED_ACROSS_SET`，唔准直接降級成 content-dependent。用戶可在 Preference Review 將它確認為 CORE、改為 FLEX 或指出只是巧合。

只出現一次、只作細節或與 headline 無直接關係，先可留作 treatment／content variable。

## Identity-safe subtraction

對 authentic UI／Dashboard：

- 移除或替換產品名、Logo、handle、精確文案、客戶資料、proprietary chrome 同 claim；
- 保留「真 screenshot 作 hero」、framing、crop priority、screen perspective、inspectability、周邊場景關係同閱讀次序；
- 唔好將真 UI 改寫成 fake dashboard、生成 terminal、虛構數字或 generic sci-fi panel。

Recognition test 應問：換另一個獲准使用的真實 UI／Dashboard 之後，仍然認得係同一 Style 嗎？如果答案係係，authentic interface modality 就係 transferable rule，唔係 identity leakage。

## Substitution gate

- `authentic-required`：只接受可驗證 real asset 或 faithful deterministic render；generated metaphor、fake UI、重畫 screenshot、虛構 dashboard 一律 fail。
- `authentic-preferred`：優先真 asset；只有用戶批准，先可用明確標示為 illustration 的替代物。
- `generated-allowed`：reference 或用戶證據支持生成 metaphor；仍不可偽裝成真實產品證據。
- `illustrative-ui` 可用於 `generated-allowed` job；只要唔聲稱係真實 screenshot，就唔屬於 fake-proof failure。
- Job 冇符合要求嘅 proof asset：`BLOCKED_PROOF_ASSET`。唔可以因為 image model available 就改變 Style。

## Attribution is not provenance

永遠分開：

```yaml
internal_provenance: required
visible_attribution: required | optional | forbidden
```

- `internal_provenance` 記 source、rights、hash、checked date 同 claim boundary，永遠保留喺 manifest／receipt。
- `visible_attribution` 控制成品有冇 Source line、handle、footnote 或 source Logo。
- Visible attribution 由用戶決定，或由法律、授權、平台、合約要求決定；唔可以因為內部有 source 就自動顯示。
- `forbidden` 時，prompt／HTML／final image 都不可出現 Source、handle、footnote 或來源 Logo；receipt 仍保留完整 provenance。

## Pilot Fit Gate

Pilot 前逐項比對：

| Style requires | Job supplies | Result |
|---|---|---|
| authentic UI screenshot | approved real UI screenshot | fit |
| authentic dashboard | generated machine／metaphor | fail |
| faithful data render | verified data + deterministic chart | fit |
| generated metaphor | approved generated scene | fit |
| authentic-required | no proof asset | `BLOCKED_PROOF_ASSET` |

Pilot output proof modality 同 Style 唔一致，就算 headline、顏色同構圖靚，都唔可以寫入 `tested_jobs` 或提高 Style score。
