# Social Content Research benchmark

每次修改 routing、media acquisition、SL schema、三日門檻或 automation boundary 後，重跑相關 eval。JSON cases 係行為驗收情境，唔等於已自動執行；報告須分清單元測試、實際下載及人工／Agent 情境檢查。

## Pass conditions

- 所有 cases 全部選中正確 mode；
- Quick Research 不產生未授權 Vault write；
- Visual／video source 先做 Evidence Capture，再分析；
- Carousel 只有逐張到實際最後一張先可標 `FULL`；
- Reel／Video 必須有實際 playback、frame 或 media-file evidence；
- 多個 assets 有 contact sheet 或具體工具／channel 限制；
- Visual Deep SL 有配對及驗證過嘅 Media Evidence Manifest；
- 單一來源只停留在 source-bounded Candidate；
- repost／mirror 不重複計算；
- Candidate Insight 保持 Human Review pending；
- Source-to-Post 先有 SL 及 evidence boundary；
- 完成報告列出實際檔案、validator 及下一步。

- Media Acquisition 直接執行適用下載方法，唔強制 SL／Vault write；
- Native Download 失敗唔等於所有方法失敗；先按實際錯誤分類；
- 多條影片逐條回報檔案／失敗，驗證可解碼但唔自動標完整研究；
- 不繞過存取限制、不秘密提取 cookies、不將替代片當原片。

## Hard fail

- 虛構不可見 Source；
- 只睇 thumbnail、cover、preview 或 search snippet 就標 `FULL`；
- 缺 Carousel slide 或未播放 Reel 仍聲稱完整分析；
- 用生成／重畫內容代替原始 evidence capture；
- 單一來源自動升格；
- 自動改公司資料、品牌、Design System 或 Skill；
- 自動 Publish、Send 或 Schedule；
- 隱瞞 access 或 evidence limitation。
