---
name: meta-ads-results-review
description: Analyse Meta ads and organic content from supplied reports or explicitly authorized read-only APIs, relate results to their campaign and content, and save source-backed insights when requested. Use for 廣告成果分析、自然內容成效、organic與ads、睇報表、分析見解入Vault. No account registration, publishing, ad buying, or budget changes.
metadata:
  status: local-candidate
  scope: supplied-results-or-authorized-read-and-existing-vault
---

# Meta 廣告成果分析與 Vault 回存

用戶交已有CSV／Excel／JSON／可讀報表，講一句想評估甚麼即可。先回答「結果同原目標有冇關係、證據夠唔夠、下一輪試乜」，再按要求記返原本工作。唔先叫人填一大份表。

用戶入口：「睇呢個活動最近一個月嘅報表，畀我有根據嘅見解同下一個測試，再講會存返邊度。」最近一個月先列明起止日期；未指定時採最近30個完整日，以來源帳戶時區為準，不能當自然月或未完今日。缺來源仍可整理讀取缺口，不補造績效。

能力分開回報：本Skill可讀已有報表、核數、分析、按批准保存並讀回；安裝不等於取得Meta帳戶或Google Sheet權限。要求真數據時，先核對現有已授權來源；未有就交代所需匯出與日期。直接API取數由已可用的只讀取數流程處理，不自動安裝或要求用戶貼token。只交數字或一個「高」評級不算完成見解分析。

用戶明確要求API取数時，先讀 [授權API來源](references/api-read.md)，使用當前可用的只讀connector／runtime；不依賴任何私人DotAI設定。用戶主堂仍用報表，沒有明確帳戶讀取授權不啟用API。Facebook Page、Instagram、Threads各自列連接狀態及內容分頁；一個平台成功不代表其他平台已接通。自然內容與廣告一起分析時，分別保留post與ad來源，唔將post總互動當純organic，亦唔將兩份重疊數字相加。

## 1. 先找原任務與資料範圍

讀用戶指定報表及今次brief。要對返Vault時，讀實際Vault的AGENTS／INDEX，揀指定Project或精確Campaign／成果紀錄；只讀該Project規則、brief同創意對照。找不到唯一對象就問一條關鍵問題，分析仍可先做，不猜寫入位置、不自動開新Project。

記清：檔案／後台來源、匯出日期、報告期間、時區、幣別、Campaign目標、報表層級、歸因設定、轉化事件。未知寫TBC；唔將檔案修改時間當匯出日期。資料若係模擬／教學fixture，整份結果保持`demo`，不計公司真實成效或Learning信號。

按Campaign／ad／Post ID及用戶提供的對照，找原內容、Hook、CTA與Landing／Blog。名字相似唔證明同一Post；一個ad亦可能無公開Post URL。無對照仍可分析數字，但標`creative_mapping_missing`，唔對未見過嘅圖作評論。

## 2. 核對數據先計數

讀 [指標與資料契約](references/data-contract.md)。原始檔只讀；另存最小正規化資料及欄位對照，保留來源。不把all clicks當link clicks、不混Campaign合計與ad明細、不跨幣別／歸因／轉化事件硬合計。

- 空白／缺值不等於0；分母0或不明就不計該比率。
- CTR／CPC／CPL由分子分母重算，唔平均行內百分比。
- Meta回報Lead與CRM有效Lead分開；只有明確ad／UTM／提交對照、同期間及去重方法才可計CRM CPL。無法對應嘅CRM總數只作獨立觀察。
- Meta歸因收入不是可直接證明因果的增量收入；冇一致收入與花費資料不計ROAS。
- 圖片報表只涵蓋可見行；OCR含糊先核對該數字，唔扮已讀完整匯出。

有CSV可按契約整理一個比較組，用標準Python腳本核數：

```text
python3 <此Skill>/scripts/summarize_ads.py <normalized.csv>
```

腳本只讀CSV並輸出JSON，不連網、不寫Vault。多個比較組分開跑。它核對已映射資料的數值／粒度，不證明原檔完整、欄位映射正確或歸因真實。無Python時用可用可靠計算工具，記實際方法；不能聲稱跑過腳本。

## 3. 對返內容，提出有限判斷

讀 [見解、決定與下次覆核](references/insight-review.md)。先讀同Campaign上次判斷；沒有就如實開始首次review。每項重要見解要講明數字支持哪個決策、仍有甚麼其他解釋、下次如何驗證，不能只覆述升跌。

輸出應短而具體：

1. **目的與結果：**原本想帶來甚麼？目前能觀察到甚麼？
2. **資料與指標：**來源／比較條件、總數／比率、缺乏甚麼；自然貼文互動另列。
3. **對應作品：**哪個ad對哪份Hook／圖／CTA／目的地，缺對照就標示。
4. **觀察 → 解讀 → 未證實：**只在同目標／可比組內比較。高CTR不自動等於好Lead，少量或短時間資料不急判輸贏；無通用必停／加碼門檻。
5. **下一輪一個測試：**改哪一點、為何、觀察哪個指標與期間，保留其他變數；不執行改廣告／預算。

用戶指定互動／觀看目標時先回答該目標，不強制改成Lead分析。CTR與互動率達標只叫「點擊／互動達標」，不能推成整體廣告質素、盈利或自動加預算。沒有完整影片／社交互動欄仍保留可分析的其他數字。

分析不一定要有贏家。零資料可交準備狀態與缺口，不能產生績效結論或補造示範數字。用戶另要求demo才用清楚標示的例子。

## 4. 記返原本 Vault 工作

只要求分析就交報告，不自行入Vault。要求「分析並保存」則先完成可review結果，展示`分析摘要 → 原Project／receipt精確路徑 → 新增或更新`。按該Vault要求確認；已有涵蓋exact target／內容範圍的批准沿用。

保存讀 [回存契約](references/vault-return.md)。更新同一Campaign／作品對應紀錄，保留不同review window與舊結論；唔開平行真相、唔覆蓋用家Feedback。資料來源、報告路徑、創意對照、觀察／假設／下一個測試要能找回。

已獲准在當前Project保存、但未能唯一對應正式Campaign時，可先存Project內獨立review並標「Campaign未對應」，不冒稱已回存公司Vault。保存紀錄和批准下一輪投放是兩件事。

要求更新dashboard時，先讀指定工作簿／分頁及本次範圍，交同一分析的待寫入摘要；只有現有工具、適用Skill及有效批准齊備才寫。驗證篩選期間、總數與圖表相符，保留其他Campaign和人的舊決定。沒有寫入／讀回證據就標「本地已保存；Sheet未同步」。UTM登記只證明連結已建立／發布，不證明流量、Lead或廣告API接通。

本用戶Vault已有`company-vault-learning-loop`：它只接closeout／published-review，沿用原有保存／receipt驗證機制，不新增第二個分析Skill。先真讀其相應mode，再交接；不能以「已handoff」冒充已寫入。獨立安裝時以目標Vault現有規則／模板為準，沒有相應能力只交報告與保存建議，不自創Vault。

`50-研究與見解`放外部文章學習，唔放自己Campaign績效。此Skill不改STYLE、DESIGN、公司facts、SKILL或AGENTS；數據衍生嘅設計假設記原任務，用家之後明確批准才交原設計流程處理。

## 5. 驗收與人話回報

- 抽查至少一行及合計的分子／分母、來源欄位與幣別；條件不明不給確定排名。
- 核對ad→作品對照是證據，不是猜測；示範示範不混真成效。
- 保存後重讀確切檔案；對照Report期間與原作品。用到既有Loop receipt就執行其validator，未過不說已完整保存。
- 不把token、cookie、客戶名單或完整個人Lead資料抄入報告／Vault。

回覆包括：主要發現、不能判斷、下一個測試、實際報告／Vault路徑、owner。狀態分`ANALYSIS_ONLY`、`AWAITING_SAVE_CONFIRMATION`、`SAVED_AND_READ_BACK`或`INCOMPLETE`；本地保存不等於雲端同步／正式發布。最多問一個具體用家評價問題；未有回答不填「用家同意」。
