# Save Receipt Contract

Receipt 係 routing 同 read-back 證據，唔係 raw transcript。

## Required frontmatter

- `type: save_to_vault_receipt`
- `status: saved | needs_human_review | draft`
- `created`、`updated`：`YYYY-MM-DD`
- `owner`：真正決策人；未知用 `TBC`，同時 status 必須係 `needs_human_review` 或 `draft`
- `source_kind: chatroom`
- `source_ref`：穩定 task/thread ID；冇就 `current-chatroom`
- `privacy: internal | confidential | public | mixed`
- `human_review: not_required | pending | required | approved`
- `canonical_changes`：`none` 或列明 exact target

## Active record

每行只記一個 active item：

| Field | Meaning |
|---|---|
| `item_id` | Receipt-local stable ID，例如 `item-001` |
| `class` | `FACT／OWNER_DECISION／OBSERVATION／INTERPRETATION／TBC` |
| `summary` | 不含 secret／私人資料嘅短 paraphrase |
| `source` | current-chatroom、turn ID 或 supplied file |
| `target` | relative canonical target |
| `action` | created／updated／linked／candidate／no-save |
| `review` | approved／pending／not-required |

## Writes

Validator 會讀以下固定格式，每個實際寫入一組：

```markdown
- path: relative/path/from/vault-root.md
  action: created | updated
  read_back: pass
```

只用 relative paths。路徑必須已存在、位於 Vault root 內，唔可以包含 `..`。

## Exclusions

列出「冇保存乜」同原因，例如 duplicate、superseded、transient、secret、private data 或 out-of-scope。只描述類別，唔好在 Exclusions 再貼一次 secret。

## Review

列清 owner、Human Review 狀態、open items 同 next action。`saved` 只代表實際檔案已保存/read back；佢唔代表 canonical approval、sync、Git push 或 publication。
