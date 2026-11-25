# 明確授權的 API 取數

只在用戶明確要求取其帳戶資料時使用；主堂／離線報表不需要此模式。本reference提供執行契約，並非已安裝connector，也不自動產生權限。

1. 用現有connector／已配置runtime確認平台、帳戶身份、帳戶ID、日期、時區及讀取權限。Token只留既有安全環境，不貼聊天、不寫Skill、設定範本、URL或輸出。不可用一個有發布權限的token就假定有廣告／Insights權限。
2. Ads需可存取指定廣告帳戶及適用Insights讀取權限；organic需對應Page／IG身份及所需指標權限。依當次官方API契約和實際回應核對版本／指標。不同token類型的入口可以不同，不盲目用`me/adaccounts`當唯一方法。
3. GET／明確只讀connector為限，按授權期間和帳戶取數。每個資料流分別記查詢、時間、分頁完整性、來源hash。只使用已核實API host，不跟含token的paging URL到其他域；不得保存paging URL或完整provider headers。
4. Ads保留Campaign／adset／ad ID、目標、花費、曝光、link clicks、原始actions及實際可得歸因資訊。Lead、purchase、訊息等事件分開；不要將重疊action_type加總。跨Campaign可以描述帳戶花費，但需全量完整及同幣別；不能跨目標判一個贏家。
5. Organic分清「本期發出的貼文，截至擷取時的累積數字」與「本期內所有內容產生的活動數字」。可讀文案／日期／permalink不等於取得organic績效；post總數字可能包含付費分發，只有來源明確拆分才稱純organic。
6. 保留API明確回傳0；缺字段、無metric或空data寫未知／未提供，不自動當0。曝光、views、reach不可換名，無可靠分母不算互動率。來源指標不齊時分項返回已知資料，唔令一個comments權限錯誤吞掉整份貼文清單。
7. 過期、權限不足或無帳戶對應時停止該資料流；錯誤只記安全code與不含secrets的摘要。不自動擴權、不反覆試token、不改用公開Ad Library當帳戶績效。可查已配置且用途相符的正確token／入口來診斷；有另一條獨立已授權來源則繼續。用戶指定API時尊重選擇，不能悄悄用網頁抓數冒稱API。
8. 每個資料流標`READY`、`PARTIAL`或`BLOCKED`。有部分資料就先交局部分析及保存位置；任何未取得的廣告成本、曝光、轉換不得補demo。回報精確缺口，如「指定帳戶ID＋有ads_read且可存取該帳戶的連線」，不要只叫用戶重新登入。

來源取得後回主Skill核數、分析、保存；讀取成功不等於dashboard已更新。真公司資料只留授權工作區，公開／用戶去識別副本另按分享批准處理。

## 多平台與可保存的 dashboard

- Facebook Page、Instagram、Threads 分別驗證身份、授權與貼文／Insights。Threads 的 Tester 邀請、接受邀請、可用 token、成功 API 回應是四個不同狀態；Facebook／IG token 不當作 Threads 已接通。
- 分頁清楚分成平台內容、付費廣告、帳戶期間活動及見解。廣告的 publisher_platform 是投放位置，不代表該平台自然內容已取到。廣告帳戶可能服務多個 Page，保留 Page ID，不能把帳戶總花費稱作單一 Page 花費。
- 保存查詢起止、帳戶時區、擷取時間、metric 的 period／total_value／lifetime。API 原生日桶未必在香港午夜結束；不強行重標成香港每日數字，也不將 lifetime 當期間增量。欄位名稱以當次官方契約及回應核對，貼文與帳戶指標可能不同。
- 用 Post ID／Ad ID 精確配對；只在本期廣告找不到配對，不代表貼文從未加強推廣。沒有可信 organic 拆分，就保留「未提供」，不能用總觀看減廣告曝光。
- 每項見解用穩定 Review ID，分開事實、解讀／限制、下一個測試、人的決定、狀態。刷新先讀現有決定並按 ID 合併；不可用新空白欄覆蓋。一次匯入只是快照，除非實際排程與刷新已驗證，不稱自動同步。
- 保存後讀回同一份 Sheet 的分頁、期間、來源、公式合計及人的決定。若雲端同步失敗，保留本地成果並標示未同步；API 取得成功不能代替寫入證據。
