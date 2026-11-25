# 分析結果回到原本工作

分析Skill擁有報告；已存在的Campaign／內容Project擁有工作歷史。一次同源同期間review只更新一個紀錄，唔因重跑新增Learning signal。

見解正文按 `insight-review.md`，保留觀察依據、解讀、替代解釋、測試與人的決定。保存已獲當次明確授權且目標唯一時直接執行；不因跨回合重問。正式Campaign對應不明時，先保存已授權Project的分析並標mapping缺口，不猜canonical路徑。

公司報表留喺指定工作區；對外分享用經批准嘅去識別版本，不能帶入帳戶資料、非公開原素材、credentials或Lead個資。

1. 先讀Vault AGENTS／INDEX與精確Project。用ad_id、Campaign、已給作品路徑、review期間查重；同名但無ID對照就先確認。
2. 選既有review／LEARNING紀錄作入口。Report有獨立長表時存同一Project相鄰輸出；receipt只加summary＋link。既有記錄已足夠就原位更新，不另開新報告。
3. 保存清單包含：來源檔與匯出日期、期間／幣別／時區／歸因／事件、ad到作品對照、可比狀態、觀察、推測、缺口、下一個測試、review日期／owner。
4. 示範demo只放教學Project或demo區，標`demo`；不寫進真Campaign成效receipt、不加LOOP-STATE信號、不當獨立證據。
5. 真實Project績效優先更新原`outputs/<task>/LEARNING.md`。跨多個作品的一份Campaign分析留Campaign原紀錄，引用相關作品，唔為每一行ad重開Project。
6. 無Project的實質分析按Vault規則放`30-學習與優化/任務收據/`。平台實戰索引只加一行link；外部研究區`50-研究與見解`不接績效報表。
7. 本包由既有`company-vault-learning-loop`記closeout／published-review；不捏造原創意圖片或live Post。缺原作品可先保存獨立分析報告，清楚留mapping缺口。
8. 保存需要的確認完成後，最小修改並讀回。兩份期間不同的報告不是兩個獨立創意實驗；重跑、同作品版本都不應自動湊數。

驗證：確切路徑存在、期間／source／數據摘要與分析一致、舊Feedback仍在、無secrets、沒有重複receipt。如果用Loop receipt，按該Skill跑`validate_learning_receipt.py`。找不到既有工具／路由則`INCOMPLETE`並交保存建議，不假稱自動記住。
