# Style extraction method

## Aim

拆嘅唔係「張圖有咩」，而係「轉 topic、人物、顏色之後，邊個視覺機制仍然令人認得係同一個 Style」。

## Evidence order

1. 用戶親口講鍾意乜；
2. 大部分 reference 都出現嘅機制；
3. 少數但符合用戶描述嘅強機制；
4. 只出現一次嘅顏色、texture、object 或 effect。

第 4 層唔可以自動升級成固定規則。

## Mechanism matrix

每張 reference 建一欄，逐行比較：

| Axis | Questions | Decision types |
|---|---|---|
| Canvas | aspect、border、corner、crop 是否一致？ | core／parameterized／treatment |
| Reading path | 第一、第二、第三焦點係乜？ | core／conflicting |
| Headline | 位置、行數、shape、weight、contrast？ | core／range |
| Subject | hero、guide、scene anchor、decoration？ | core／parameterized |
| Proof meaning | 今次證明產品、流程、比較、數字定結果？ | job-specific／content-dependent |
| Evidence modality | proof 係真 UI／Dashboard／文件／實物、faithful data render、generated metaphor 定 decoration？ | core／parameterized／treatment |
| Proof authenticity | 一定要 real、prefer real、定可以 generated？claim-critical 位要幾忠實？ | authentic-required／authentic-preferred／generated-allowed |
| Palette | 固定 hue 定只係明暗／accent 角色？ | source-locked／swappable／adaptive |
| Material | paper、HUD、glass、editor、photo depth？ | treatment／core |
| Density | thumbnail 下仲睇到幾多層？ | range |
| Semantic link | 人物／場景點樣幫 headline 同 proof？ | core／fail |

每個決定使用：

```text
實際觀察 → 機制／用途 → 可保留的關係 → 可變範圍 → 信心
```

例子：

```text
R01、R03、R04 headline 佔上方約三分一
→ 標題先被讀到，主體承接解釋
→ 保留標題主導、主體協助閱讀的層級
→ 上方三分一只是來源觀察；新圖按內容／尺寸安排
→ OBSERVED；跨用途位置未驗證
```

避免只寫 `高級、科技感、吸睛、專業`。必須翻譯成可見規則。

## One Style or several?

先移除顏色、人物身份、產品名、Logo、精確 source 文案同 proprietary chrome；唔好移除 proof modality。再問：

- headline hierarchy 是否仍相同？
- subject role 是否相容？
- proof 是否同樣必要？
- proof 是否一直由同一種真實／生成 evidence modality 承載？
- 不同 reading path 是否仍共享相容的層級、材質及字圖關係？不要因封面與內頁排版不同就拆成兩款。

答案大致相同：保留一個 Style，差異寫成 treatments。人物一張係 hero、另一張係純裝飾而且兩者不能共存；一組要求 authentic UI、另一組只接受生成 metaphor；或一組需要 proof、另一組完全禁止 proof，先提議 split。

「真 UI screenshot」唔等於「某產品 UI」，而「illustrative UI」亦唔等於假冒產品證據。前者係 authentic evidence modality；第二種可以係 generated-allowed 視覺語言；某個 source 嘅 proprietary chrome 先係要排除嘅 source identity。抽象後仍需保留已確認嘅真實性要求、framing、crop、inspectability 同 proof-to-headline 關係。

## Preference review language

用普通人聽得明嘅方式交付：

```text
你已確認鍾意：...
我喺多張圖都見到：...
我推測你可能鍾意：...
只係其中一張出現，暫時唔當核心：...
呢個 Style 一定唔包括：...
```

已有明確拆解／建立候選要求就先交 candidate，唔強制另等一次確認；用戶要先試感覺則按短 brief 先做已授權試版。正式品牌確認與保存另按主指引的範圍處理。

## 一份 STYLE.md 是否足夠供下次使用

在同一份的「風格核心／使用界線」回答：

- 點解呢幾張屬於同一個 Style？
- 改走人物、topic 同顏色後，乜嘢仍然要保持？
- 換另一個獲准使用的真 UI／Dashboard／實物後，proof modality 是否仍然成立？
- 改邊一點會令佢唔再係同一 Style？

在「設計方法與變奏／品牌適配」回答：

- 怎樣按下一張的資訊任務／畫幅選擇 reading order、比例和 safe area，而非預先指定位置？
- typography、palette roles、materials、subject／proof 關係怎樣執行？
- proof asset 要真實到咩程度、冇 asset 時可否 substitute、visible attribution 是否顯示？
- 有咩 content fields、prompt rules、negative rules 同 QA？
- LOCK 咗邊啲結果、FLEX 留咗邊啲創作空間、BAN 是否只包含用戶確認或基礎輸出 QA？

「參考圖片與觀察」保留完整 current examples、原圖實際擺位、來源及權利；「確認與測試」只記真實用戶決定與已做測試。不要求重讀全部歷史；少量最新 anchors 與文字一起使用。今次產品事實／copy 留 job；品牌 binding 記自己的來源與 palette。以上係六節同一份資料，不是六份檔案；舊 STYLE／DESIGN／REFERENCE 僅作舊包相容讀取。
