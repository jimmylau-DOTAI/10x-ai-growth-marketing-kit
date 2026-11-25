# 只在映射報表／計指標時讀

保留原始匯出；正規化必須記raw field→normalized field、單位與選取條件。Excel／JSON用當前可用讀取工具；不能讀取就請用戶提供CSV或可讀範圍，唔估。

| 輸入／指標 | 意義／做法 |
| --- | --- |
| spend／currency | 同幣別才可合計；原始單位與小數保留 |
| impressions | 曝光，可按不重疊明細求和；reach是去重人數，不能如此相加 |
| link_clicks | 明確link clicks；all clicks、outbound clicks各自不同，不能偷換 |
| meta_leads／lead_event | 指定一個轉化事件的計數；不可把results自動當Lead |
| link CTR | sum(link_clicks) / sum(impressions) × 100 |
| link CPC | sum(spend) / sum(link_clicks) |
| Meta CPL | sum(spend) / sum(meta_leads)，列明lead_event |
| CRM CPL | 需明確同期間ad／UTM對照與去重的有效Lead分母；本腳本不代作CRM歸因 |
| ROAS | 可對應且同幣別／同歸因的收入 / spend；本腳本不算未知收入 |

## 核數CSV只處理一個比較組

欄位：

`ad_id,date_start,date_stop,currency,timezone,objective,attribution_setting,lead_event,spend,impressions,link_clicks,meta_leads`

- 一行是一個ad在**整個指定期間**嘅總數，沒有placement／age等breakdown。日期為YYYY-MM-DD。
- 同個CSV每個ad_id唯一；日期、幣別、時區、目標、歸因與Lead事件一致。原表按日／breakdown先驗證互斥再正規化；重疊分組唔合計。
- 四個數字欄位可空白（未知），不可負／NaN／Infinity；零係真0。計數欄位允許來源歸因計數的小數，勿擅自四捨五入。
- 缺任何一行的某個數字，該欄位合計及依賴比率回null；不默默只算有數據的部分。
- timezone／objective／attribution_setting／lead_event未知填TBC；腳本會標`needs_review`，不代表可作決策。raw檔存在不等於這些資訊已知。
- 空表回`no_data`，不產生0績效。

原表若只給率而無分母，就保留原率但不合計。計算輸出僅核數，文案仍須解釋其限制。

## 自然內容與廣告並看

自然貼文以platform＋account＋post_id去重；boost不新增一篇Post，ad數不等於Post數。保留發布日期與擷取日期。原Post被多個ad引用時，用明確ID對照保存關係；沒有映射就標缺口，不靠文案相似配對。

本腳本只核算上述廣告CSV，不接受organic rows。自然貼文另列來源及其原始指標；沒有spend就不計CPC／CPL，沒有organic分拆就標「貼文總數據，付費影響未知」。累積貼文數據不能直接和30日Ads結果作效率排名；新舊貼文曝光時間不同亦要註明。

同時列每條來源的完整／部分／不可用狀態。原始API空data、missing欄位與已核實零結果分開；不可用的資料流不計入合計或產生贏家。
