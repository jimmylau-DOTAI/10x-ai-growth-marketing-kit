# Mobile rhythm and delivery modes

Threads 先喺手機被掃到，再決定值唔值得慢慢讀。呼吸感唔等於逐句斬碎；每次換段都應該有功能。

## Delivery modes

### `complete-single-500`

一個 segment 內完成 Hook → 解釋／例子 → 判斷。讀者唔需要撳入 reply 先得到核心價值。適合一個觀點、一段反應、一個短故事或簡短 review。

交付：只輸出 `root`；Python `len(text) <= 500`。

### `notes-link-reply`

Root 本身要有一個完整而值得收藏嘅 insight，唔可以只寫「下面有 link」。第一個 self-reply 放筆記、工具或 source link，再補一句入面有咩。Link 未核實時必須原樣保留 `[LINK TBC]`。

交付：按次序輸出 `root`、`reply-1`；兩段分開計數。`👇` 只可喺 root 作真實 handoff。

### `staircase-thread`

資料多、推理有層次，或者每一步都要獨立消化先用。Root 定義問題同閱讀承諾；其後每個 reply 只推進一層；最後一段先落判斷或 CTA。

交付：`root`、`reply-1`、`reply-2`……有明確次序；每段獨立 `len(text) <= 500`；全條 thread 只設一個主要 CTA，放最尾。

## 手機分段規則

- 預設每段 1–3 句；一個視覺段落只做一件事。
- 新場景、新證據、新轉折、新步驟或結論先換段。
- 連續三行都長，主動拆開；但唔好將主語、動詞、條件拆到唔完整。
- 長句負責必要脈絡，短句負責判斷。兩者交替先有節奏。
- Fragment 只用喺 Hook、pivot 或 punchline；正文仍然要有完整句。
- 白位要幫理解，唔係用十幾個單句製造假深度。
- Link 最好獨立成行；連同 link、emoji、空格同換行一齊計入 500。

## Symbol grammar

- `▍`：小標／視覺轉場；每個 segment 最多 2 次。
- `→`：只表示真實次序、因果或轉換；唔好當普通 bullet 裝飾。
- `👇`：只用於下一個 reply 或 link handoff；無 handoff 就唔用。
- 除同一流程重複使用嘅 `→` 外，每段預設 0–3 個功能性符號。
- Emoji 唔係語氣救命丸。文字本身無判斷，落 emoji 都唔會自然。

## CTA placement

一段 Post 只揀一個主要動作：回覆、收藏、打開 link、試一個步驟或分享經驗。CTA 由內容自然推出；無下一步亦可以用一句判斷完結，唔需要每次都問問題。
