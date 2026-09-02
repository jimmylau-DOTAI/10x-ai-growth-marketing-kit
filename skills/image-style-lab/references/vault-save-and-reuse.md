# Vault save and reuse

## Portable Vault layout

唔假設任何私人 Vault 名稱或 absolute path。由用戶提供目的地。

```text
<vault>/
  Visual-Styles/
    INDEX.md
    <style-id>/
      PREFERENCE.md
      REFERENCE.md
      STYLE.md
      DESIGN.md
      scorecard.md
      assets/reference-images/
      PLATFORM-ROUTE.md          # only when a managed platform route was requested
  Visual-Characters/
    <character-id>/
      CHARACTER.md
```

Content Jobs 同生成 outputs 留喺 project／workbench；唔好塞入通用 Style folder。

`TONE.md` 同 Skill candidates 使用各自平台／project 嘅 canonical route，唔可以塞入 `Visual-Styles/`。一個平台可以有多個 Style folders 同多個 Tone folders；每個項目要有獨立 ID、evidence 同 approval status。

Portable save 必須複製 `REFERENCE.md` 實際 embed 嘅本地圖片到 `assets/reference-images/`，並 read back hashes。只有 URL 或原始機器 absolute path 唔算已保存 reference。

## Managed platform filing

當用戶指定內容平台、要求 Design ID 或「擺去適當位置」，先讀 [platform-routing-and-design-id.md](platform-routing-and-design-id.md)。Portable `Visual-Styles/` save 唔等於正式平台註冊。

- 建立 `PLATFORM-ROUTE.md`，duplicate-check namespace／ID，先做 dry-run。
- Destination-ready `STYLE.md` 同 `DESIGN.md` 必須有相同 Design ID 及 platform scope。
- Reference 圖像放入已核實嘅 reference／visual-assets destination；平台 `REFERENCE.md` 連回該 evidence。
- 由 active Vault／brand-system owner 執行 approved write，再 read back index、三份 Markdown 同 reference-image hashes。
- 如果現有 platform contract 會遺失 `DESIGN.md`，停止 `PLATFORM_CONTRACT_CONFLICT`，唔好自行改規則。

## Save gate

只接受同一任務內清楚指定類型嘅命令：

- `save it as style`／`Save 做 Style`／`入 Style`／`加入 Style`；
- `save it as tone`／`Save 做 Tone`／`入 Tone`；
- `save it as skill`／`Save 做 Skill`／`入 Skill`。

只講 `save it` 而同時有多種 candidate 時，先問要保存邊一層。下面嘅 script 只負責 Visual Style；Tone／Skill 要跟目的地最近嘅規則、duplicate-check 同獨立 approval，唔好借用 Visual Style folder。

1. Validator pass；
2. 顯示 source、destination、style status、將複製檔案及衝突；
3. 執行 dry-run；
4. 停在 `STYLE_SAVE_REVIEW_STOP`；
5. 用戶今次明確批准後先 `--apply`；
6. read back destination files and hashes；
7. 回報 `STYLE_SAVED`，但唔代表 `STYLE_SELECTED` 或已發布。

命令：

```bash
python3 scripts/save_style_pack.py /path/to/experiment --vault /path/to/my-vault
python3 scripts/save_style_pack.py /path/to/experiment --vault /path/to/my-vault --apply
```

預設拒絕覆蓋同名 Style。要修改自己版本，先喺 project workbench 建新 version，review 後使用新 style ID 或人手處理舊版本；唔好靜默 overwrite。

## Reuse contract

新圖只需要：

```text
Saved STYLE.md + DESIGN.md
+ new CONTENT-JOB.md
+ optional CHARACTER.md
+ approved brand assets
→ pilot
```

唔需要重新讀 reference 圖，除非用戶想重新定義 Style。

## Modify my version

學生應分清：

- 改 topic／copy／Logo／CTA：只改 Content Job；
- 改人物：只改 Character；
- 改顏色但保留角色關係：新增／修改 treatment；
- 改 headline dominance、proof requirement、subject role 或 reading path：可能係 Style version 或新 Style，要重新 Preference Review。

每次更新寫一個簡短 decision receipt：`KEEP／CHANGE／BAN／WHY`、受影響檔案、舊／新 rule、測試 job 同 Human Review。
