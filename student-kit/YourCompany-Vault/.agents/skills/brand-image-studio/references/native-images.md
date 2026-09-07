# 生成、檢查與修正

先按 SKILL.md 完成任務及方向／文案確認。批量與先試一張只改出圖後等待位置；Final QA 是驗收深度，不可取代客戶確認。

## 出圖準備

讀可用工具 schema，依 runtime 規則選支持新圖／編輯／重構的工具。用戶指定 ToAPIs 等工具時沿用有效選擇及付費範圍；缺能力就報缺口，不暗中換付費工具或自行安裝。

先看真原素材、Logo、參考；每次只帶本張文案、畫面要求及適用來源。產品原相決定外觀，服務來源決定內容，參考決定視覺。每次生成一張完整獨立圖，不能以 HTML／CSS、底圖加字或多圖總覽代替。

沿用已確認比例／尺寸，只有用途不明會影響構圖時才補問。預覽可用工具支持的合適尺寸並說明；精確尺寸依 [size-intake.md](size-intake.md)，實際輸出須量度。尺寸只寫 prompt 不代表精確控制，不能拉伸產品或倒改需求。

## 原 Logo

先生成包含完整文案與構圖、預留乾淨 Logo 區域的圖片，再用能保留原檔 pixels／向量的工具放入真 Logo。不得讓模型重畫、手打近似字標或交空框當成品。

尚未加入原 Logo 記 `preview_without_logo`；沒有可靠合成能力記 `logo_overlay_required`，說明缺口。需要品牌識別的圖不能因此稱完成。

## 批量與先試一張

用已要求成品中的第一張校準，計入總張數，不額外加測試圖。對照原資料、已確認文案及參考，檢查：
- 產品身份、外觀與操作，或服務範圍、流程、交付與人物身份。
- 真 Logo、價格／數字、主要文字可讀性及宣稱。
- 視覺是否符合已選風格，構圖能否表達本張問題。

通過後按批量授權完成其餘；先試一張則交圖等待。每張看基本錯誤，最後聯看全套的讀序、內容差異與風格一致。只重做出錯頁；一次針對修正仍失敗則記部分完成，不無限重試。額外付費須在授權範圍內。

在現有計劃的輸出清單記圖號、版本、路徑、狀態與例外；已有 batch manifest 可沿用，不同時維護重複清單。缺實際輸出記 not_generated。改方向按主指引重新確認。

## 正式交付檢查

用戶要求 final、交客或精確尺寸時，逐張打開核對全部文字、CTA、Logo、事實、參考及實際像素，改後重驗；再檢查整套。Hash 只辨認版本，不證明圖片正確。

出圖前按 size-intake 建 request；完成後按 [output-contract.md](output-contract.md) 留實際證據並執行：

```text
python3 <本Skill>/scripts/verify_delivery.py <job>/request.json --preflight
python3 <本Skill>/scripts/inspect_images.py <job>/output.png --expected <width> <height> --output <job>/image-check-v1.json
python3 <本Skill>/scripts/verify_delivery.py <job>/delivery.json --output <job>/delivery-check-v1.json
```

width／height 來自 request。需要 Python／Pillow，缺失就說明。普通草稿與單純先試一張不用逐圖 JSON／hash。已完成批次可記 DRAFT_BATCH_COMPLETE；正式檔案及視覺驗收完成才記 LOCAL_QA_PASSED_REVIEW_REQUIRED。

程式只驗檔案與證據契約；不證明客戶滿意、目標平台實測或廣告成效，亦不授權發布。
