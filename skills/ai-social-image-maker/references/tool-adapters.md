# 工具能力與尺寸控制

實際看 runtime tool schema，分清 generate、edit、reference input 與 size/aspect 控制。這些是能力分類，不能假設 API 有同名 mode 或 model 參數。用戶指定且工具支援先設定 model；否則記 runtime-managed／null。

| size_control | 證據與限制 |
| --- | --- |
| structured | 真實 width／height／aspect 參數或可核對 UI 設定；輸出仍須驗 |
| prompt_only | 尺寸只寫 prompt；不能承諾 exact size |
| unavailable | 沒有必要能力，回報 CAPABILITY_BLOCKED |
| deterministic-finish | 獲允許使用本 Skill renderer，記 layout 與 finish receipt；不是模型尺寸控制 |

job 的 tool-contract.md 記 tool、公開 model、操作、實際非敏感參數、size_control、限制；tool-result.md 記真正回傳檔案或定位。不捏造設定、來源或工具成功。

尺寸與 target 同比例：runtime／用戶容許時可整圖等比例 resize，再驗實際像素。比例不同：不可拉伸、偷偷裁剪或倒改 target；需要獲授權 native recompose。只加 Logo 不代表批准改構圖。

沒有尺寸控制，不反覆用同一句 prompt 盲試。可查看其他已可用而符合用戶／runtime 要求嘅工具；缺可行方法就交代 blocker，唔將 preview 當正式成品。以修尺寸為由 retry，必須有不同而可核對嘅控制方法。
