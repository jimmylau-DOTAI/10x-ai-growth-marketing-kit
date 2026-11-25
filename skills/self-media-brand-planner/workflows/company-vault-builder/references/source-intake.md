# Source Intake

只在用戶提供新公司文件、要求匯入 source，或者要由文件補 Company Vault 時讀本頁。

## Outcome

每份文件只產生：一份保留原貌的 raw file、一個 Source ID、一份精簡 source note，以及最多一個建議 canonical target。文件本身唔會直接變成 verified company knowledge。

## Intake gate

1. 目前 workspace root 必須係已通過驗證的 user Company Vault；本 Skill 已經內置，唔需要另行安裝。
2. 取得 exact file list、owner、privacy、rights 同 source date；同一批設定相同時只問一次。
3. 拒絕 credentials、登入資料、未遮蓋客戶 PII、無權保存文件、空檔及超過 50 MB 的單一檔案。
4. 舊 `.doc／.ppt／.xls` 或未支援格式請用戶先匯出成 PDF、Markdown、文字或新版 Office 格式；唔好自行安裝不明 converter。

## Register first

以 Vault root 作 workdir，每份檔案執行一次；將所有 placeholder 換成實際值：

```bash
python3 .agents/skills/company-vault-builder/scripts/register_source.py \
  --vault "ACTUAL_VAULT_PATH" \
  --source "ACTUAL_SOURCE_FILE" \
  --owner "ACTUAL_OWNER" \
  --privacy "public_or_internal_or_private" \
  --rights "owner_provided_or_public_reference_or_licensed_or_unknown" \
  --source-date "ACTUAL_DATE_OR_TBC"
```

Windows 可以用 `py -3`。只有 `SOURCE_REGISTER_PASS` 或 `SOURCE_ALREADY_REGISTERED` 先可繼續；後者唔建立副本。

## Read light

- 多份文件可以先全部登記，但預設每輪只分析一份；唔掃描 `00-收件箱/原始文件/`。
- 長 PDF／DOCX／PPTX 先讀目錄、標題及頁面／章節結構，寫「來源內容地圖」，再深入真正相關部分。
- 試算表先列 sheet、欄名、日期範圍同資料量，再揀相關 sheet；圖片只分析可見內容，唔估被裁走或模糊文字。
- 如目前環境冇可靠 reader，只保留 registration receipt，回報 `CONTENT_READER_NEEDED`，請用戶提供 PDF／Markdown／text export。

## Extract and map

更新同一份 `00-收件箱/來源記錄/<Source ID>.md`：

1. Read receipt：實際讀過與未讀範圍；
2. 來源內容地圖；
3. 有 locator 的 observed fact／claim；
4. 日期、價格、名額、連結、結果等可變資料；
5. 與現有 Vault 的衝突；
6. 最多一個建議 canonical target。

唔複製全文、唔將 inference 寫成 fact、唔因為文件係公司提供就假設仍然 current。

## Grill Me only for decisions

Source 已回答的資料唔重問。只有缺口或衝突會改變 canonical target 時，先一次問一題：問題、重要性、二至三個選項、建議答案及 exact target。

有今次明確寫入授權，而且 source／owner 足夠時，先將一個 exact target 更新為 `needs_review`，再 read back；否則只展示 proposed diff。`verified／approved` 仍需 Human Review。

## Stop

完成一份 source 後回報 `SOURCE_INTAKE_REVIEW`，包括 Source ID、hash、讀取範圍、建議 target、已寫檔案、TBC／conflict、未處理 queue 同下一題。日常任務只讀 canonical 公司檔；除非要查證，唔讀 raw files 或全部 source notes。
