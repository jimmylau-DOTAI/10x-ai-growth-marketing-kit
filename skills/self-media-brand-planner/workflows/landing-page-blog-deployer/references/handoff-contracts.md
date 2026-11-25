# Landing and Blog Handoff Contracts

## Shared rules

Handoff 係另一個 Skill 已完成工作嘅可驗證交接，唔係 permission token。每份 JSON 要保留 artifact path、approval status、open items 同 evidence pointers。

Allowed approval values：

- `APPROVED_FOR_ASSEMBLY`
- `REVIEW_REQUIRED`
- `BLOCKED`

只有 `APPROVED_FOR_ASSEMBLY` 可以進 production assembly。其他狀態可以用於 gap analysis 或 local mock，但不可公開。

## `landing-site-handoff.json`

Required top-level fields：

```json
{
  "schema_version": "1.0",
  "handoff_type": "landing-site",
  "approval_status": "APPROVED_FOR_ASSEMBLY",
  "source_artifact": "path/to/landing-page-output.md",
  "route": "/",
  "primary_cta": {
    "label": "TBC",
    "intent": "lead-capture",
    "target": "#lead-form",
    "status": "VERIFIED"
  },
  "form": {
    "anchor": "lead-form",
    "fields": [],
    "consent_status": "VERIFIED",
    "success_action": "TBC",
    "endpoint_status": "DISCONNECTED"
  },
  "tracking": {
    "utm_fields": ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"],
    "first_touch_required": true,
    "registry_path": "path/to/utm-registry.csv"
  },
  "qa": {
    "design_status": "DESIGN_QA_PASSED",
    "operations_status": "NOT_IN_SCOPE",
    "mobile_evidence": "path/or/TBC"
  },
  "open_items": []
}
```

## `blog-publish-handoff.json`

每篇文章一份。Required top-level fields：

```json
{
  "schema_version": "1.0",
  "handoff_type": "blog-publish",
  "approval_status": "APPROVED_FOR_ASSEMBLY",
  "source_artifact": "path/to/article-output.md",
  "slug": "example-slug",
  "title": "Article title",
  "meta_title": "Meta title",
  "meta_description": "Meta description",
  "canonical_path": "/blog/example-slug",
  "content_source": "path/to/article.md",
  "language": "zh-Hant",
  "internal_links": [],
  "cta": {
    "label": "TBC",
    "target": "/#lead-form",
    "status": "VERIFIED"
  },
  "schema": {
    "article": true,
    "faq": false,
    "visible_content_match": "VERIFIED"
  },
  "image_rights_status": "VERIFIED",
  "open_items": []
}
```

## Gate rules

- `source_artifact` 同 `content_source` 必須存在或由 caller 提供可讀 equivalent；
- route／slug 不可同現有 route 衝突；
- `open_items` 非空時，approval status 不可係 `APPROVED_FOR_ASSEMBLY`；
- CTA target 未核實時使用 `TBC` 同 `REVIEW_REQUIRED`，不可生成假 URL；
- image rights 未核實時，public image 要排除或 handoff 保持 review；
- form／CRM endpoint status 不等於 permission。Connected test 同 production write 仍要獨立批准。

## Multiple articles

可以傳入多個 Blog handoff。先按 canonical path 去重，再驗證：

- slug 唯一；
- metadata 非空；
- internal links 指向存在或同批建立嘅 routes；
- CTA intent 同 Landing Page 一致；
- article list 有明確排序規則，而唔係依賴 filesystem 偶然順序。
