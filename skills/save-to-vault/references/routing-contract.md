# Routing Contract

只在 chatroom 包含多種資料、destination 唔明顯，或需要處理 Learning Loop 時讀本檔。Vault 自己嘅 `AGENTS.md`／`INDEX.md` 永遠優先；路徑名唔同時按當前 Vault route，唔好硬建呢張表嘅示例資料夾。

| Chatroom item | Default destination | Save state | Gate |
|---|---|---|---|
| Owner 提供嘅公司文件、網站、產品資料、品牌資料 | Inbox raw source + source receipt | `unverified` | duplicate、privacy、rights、source date |
| 公司定位、受眾、Offer、Proof、價格、能力等 fact | Exact company knowledge file；未核實先留 source receipt／candidate | `needs_human_review` 或 Vault 指定狀態 | current source + owner decision；時效資料有 `checked_at` |
| Project scope、decision、acceptance criteria | Project `README／DECISIONS／SOURCES` 或現有 canonical equivalent | active／superseded | 最近 Project rules；latest explicit decision wins |
| Project artifact、QA、result、next action | Project output + `LEARNING.md`／receipt | draft／awaiting feedback | artifact path + actual QA/read-back |
| 非 Project substantial task | Central task receipt | awaiting feedback | 必須係 substantial；普通問答不記 |
| 對 substantial artifact 嘅具體喜惡／原因 | Update same learning receipt | signal recorded | 保留 Human wording；同一 artifact 不重複計數 |
| 已發布 artifact + URL/backend evidence | Update same published review receipt | evidence recorded | live/backend/commercial evidence 分開 |
| 跨任務可重用方法 | Learning candidate／proposed diff | pending | 先 evidence，後 Human Approval；唔直接改 rule |
| 改 Skill 嘅建議 | Skill candidate／Loop Update | pending | 只有 exact approval 才交 `skill-creator` |
| Social post／video/link 嘅內容學習 | Source／SL route；如有對應 research Skill 就 handoff | source-bounded candidate | 單一 source 不升格 durable Insight |
| 一次 wording、過期版本、重複內容、brainstorm、禮貌回覆 | nowhere | `NO_SAVE` | 在 receipt 列 excluded reason 即可 |

## Conflict rules

1. 今次 owner 明確決定 > 已確認 Vault knowledge > Project record > model inference。
2. 同一 chatroom 內，較新嘅明確 correction > 較舊要求；標記 superseded，唔合併成兩套 active rules。
3. Source 只證明 source 有咁講；唔自動證明 claim 係事實。
4. Local artifact、validator PASS 或 draft 唔等於 delivered、published、deployed 或 approved。
5. 一個 item 只去一個 canonical owner。其他位置只放 link／reference，唔複製第二份真相。

## Growth and Learning Loop boundary

「值得成長」唔係一個 destination。先判斷 evidence 類型：

- 完整 deliverable 未有 feedback：closeout receipt，`signal_type: none`；
- 具體 Human feedback：同一 receipt 加一個 bounded signal；
- published result：先 read back evidence，再更新同一 receipt；
- 可重複 pattern：按 Vault threshold 合併 comparable receipts；
- exact approved diff：先至可以改一個 bounded rule。

如果 Vault 內有 `company-vault-learning-loop`，用佢做 closeout／feedback／published review／triage／approved update。Save to Vault 只負責辨認同交接，唔複製或繞過 Loop gate。
