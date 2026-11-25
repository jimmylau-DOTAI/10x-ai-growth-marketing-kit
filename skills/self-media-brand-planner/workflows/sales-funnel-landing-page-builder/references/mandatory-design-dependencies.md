# Mandatory Design Dependency Receipt

Build／Revision 建立 `design-skill-receipt.json`，放在 landing-page artifact 或 QA folder。

## Required shape

```json
{
  "schema_version": "1.0",
  "primary_skill": "sales-funnel-landing-page-builder",
  "mode": "standard",
  "artifact_status": "DESIGN_QA_PASSED",
  "dependencies": {
    "design-taste-frontend": {
      "status": "applied",
      "skill_name": "design-taste-frontend",
      "design_read": "One-line design interpretation",
      "redesign_mode": "greenfield",
      "dials": {
        "design_variance": 7,
        "motion_intensity": 4,
        "visual_density": 5
      },
      "preflight_status": "pass",
      "evidence_file": "STYLE-DIRECTION.md"
    },
    "emil-design-eng": {
      "status": "applied",
      "skill_name": "emil-design-eng",
      "motion_decision_count": 3,
      "interaction_qa_status": "pass",
      "review_file": "DESIGN-ENGINEERING-REVIEW.md"
    }
  },
  "artifacts": {
    "page": "index.html",
    "copy": "COPY-REVIEW.md",
    "qa_receipt": "qa/QA-RECEIPT.md",
    "desktop_evidence": "qa/desktop.png",
    "mobile_evidence": "qa/mobile.png"
  },
  "qa": {
    "rendered_status": "pass",
    "horizontal_overflow_desktop": 0,
    "horizontal_overflow_mobile": 0,
    "console_errors": 0,
    "broken_assets": 0,
    "cta_consistent": true,
    "reduced_motion_checked": true
  },
  "boundaries": {
    "deployed": false,
    "form_connected": false,
    "crm_connected": false,
    "payment_connected": false
  }
}
```

## Evidence rules

- `status: applied` 代表該 Skill 在今次工作完整讀取，而且 decision 可在 output／evidence 見到；
- `skill_name` 使用 portable identifier，不記錄私人 absolute install path；
- Taste evidence 包含 Design Read、三個 dials 及 final pre-flight；
- Emil evidence 包含 motion decision table 及 `Before | After | Why` review；
- artifact／evidence path 相對於 receipt directory；
- `TBC`、空字串、缺少 file 或 validator failure 都不能使用 `DESIGN_QA_PASSED`；
- `boundaries` 只記錄已發生事項，不授權 external action。
