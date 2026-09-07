# Version-bound delivery receipt（只限 Final QA）

只有用戶要求 final、正式上架、客戶交付或精準平台尺寸時，才為每張圖建立以下 `delivery.json` 並跑完整驗收。Quick Batch 不建立逐張 request／delivery／hash；只保留一份 batch manifest、實際輸出路徑、使用來源、成功／失敗狀態及硬錯誤例外清單。

`delivery.json` 由 AI 根據真實工作記錄填寫，唔叫學生填。全部 evidence／image 路徑相對此 JSON 所在 job folder，保留素材在該 folder；不可越界或用 symlink。

```json
{
  "schema_version": 2,
  "skill": {"name": "brand-image-studio", "sha256": "SHA256_OF_ACTUALLY_READ_SKILL_MD"},
  "operation": "create",
  "request_file": "request.json",
  "request_sha256": "SHA256_OF_PRE_GENERATION_REQUEST",
  "target": {"width": 1080, "height": 1350},
  "tool": {"name": "ACTUAL_TOOL_NAME", "mode": "native-generate", "model": null, "parameters": {}, "size_control": "prompt_only", "evidence": "tool-contract.md"},
  "generation_evidence": "tool-result.md",
  "output_image": "output.png",
  "output_sha256": "ACTUAL_OUTPUT_SHA256",
  "reviews": {
    "text": {"status": "pass", "image_sha256": "ACTUAL_OUTPUT_SHA256", "evidence": "text-review.md"},
    "visual": {"status": "pass", "image_sha256": "ACTUAL_OUTPUT_SHA256", "evidence": "visual-review.md"}
  }
}
```

先按 [size-intake.md](size-intake.md) 寫出圖前 request，跑 --preflight。platform／placement 同確認來源在 request 內；target 必須逐項等於其 width／height，request_sha256 必須一致。沒有全平台固定尺寸。需求變更建立新 request 版本，保留原記錄；不能為迎合錯圖改寫已確認要求。

`operation`: create／edit／add-logo／resize／recompose。除 create 外全部另需 `input_image` 同 `input_sha256`，記修改前檔案。沿用已確認 target；若用戶明確要求新尺寸，建立新的 request 版本。不得因輸出不合而倒改數字。

tool.mode 是工作分類（native-generate／native-edit／native-recompose／proportional-resize），不是必然存在的 API 參數。model 沒公開就 null；parameters 記實際呼叫的非敏感參數，不虛構。

Tool evidence 寫真實可用尺寸設定／限制，tool-result 寫該次實際工具回傳定位及操作記錄。review 檔寫逐字核對／具體視覺觀察；不是放「PASS」就算有 evidence。

取 Skill hash／image hash 可用已有 file tools 或 Python hashlib；hash 只是版本識別，唔係模型已遵守嘅證明。

執行 verify_delivery.py，程式自行判斷 `LOCAL_QA_PASSED_REVIEW_REQUIRED` 或 `DELIVERY_BLOCKED`，不能手填 final-ready。檢查存在的 evidence 不代表它是真實；owner 必須核對工具回傳與圖像。結果不授權任何發布或保存品牌規則。
