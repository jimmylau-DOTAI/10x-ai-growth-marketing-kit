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
evidence → mechanism → parameter → allowed range → confidence
```

例子：

```text
R01、R03、R04 headline 佔上方約三分一
→ dominant headline zone
→ headline_height_ratio
→ 0.28–0.38
→ OBSERVED, high confidence
```

避免只寫 `高級、科技感、吸睛、專業`。必須翻譯成可見規則。

## One Style or several?

先移除顏色、人物身份、產品名、Logo、精確 source 文案同 proprietary chrome；唔好移除 proof modality。再問：

- headline hierarchy 是否仍相同？
- subject role 是否相容？
- proof 是否同樣必要？
- proof 是否一直由同一種真實／生成 evidence modality 承載？
- reading path 是否可以用同一 normalized system 表達？

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

先確認理解，再寫 Style pack。

## STYLE.md vs DESIGN.md test

`STYLE.md` 要回答：

- 點解呢幾張屬於同一個 Style？
- 改走人物、topic 同顏色後，乜嘢仍然要保持？
- 換另一個獲准使用的真 UI／Dashboard／實物後，proof modality 是否仍然成立？
- 改邊一點會令佢唔再係同一 Style？

`DESIGN.md` 要回答：

- 下一張圖嘅 zones、比例、reading order 同 safe area？
- typography、palette roles、materials、subject／proof slots 點執行？
- proof asset 要真實到咩程度、冇 asset 時可否 substitute、visible attribution 是否顯示？
- 有咩 content fields、prompt rules、negative rules 同 QA？
- LOCK 咗邊啲結果、FLEX 留咗邊啲創作空間、BAN 是否只包含用戶確認或基礎輸出 QA？

如果檔案要重新打開 reference 先做到下一張，DESIGN.md 未夠 executable。如果出現今次產品名、人物名、文案、card number 或 campaign，代表 job leakage。
