#!/usr/bin/env python3
"""Validate endpoint, CRM, automation and live-read-back evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


STATUS_ORDER = {
    "OPS_CONFIGURED": 0,
    "OPS_QA_PASSED": 1,
    "PRODUCTION_SMOKE_VERIFIED": 2,
    "PUBLIC_RELEASE_READY": 3,
}
CHECK_STATUS = {"pass", "not-run", "not-in-scope"}
TEST_MODES = {"dry-run-no-write", "dedicated-test-destination", "tagged-production-fixture"}


def required_text(container: dict, key: str, errors: list[str], prefix: str) -> str:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip() or value.strip().upper() == "TBC":
        errors.append(f"{prefix}.{key} must be a non-TBC string")
        return ""
    return value.strip()


def required_object(container: dict, key: str, errors: list[str], prefix: str) -> dict:
    value = container.get(key)
    if not isinstance(value, dict):
        errors.append(f"{prefix}.{key} must be an object")
        return {}
    return value


def check_status(container: dict, key: str, errors: list[str], prefix: str) -> str:
    value = container.get(key)
    if value not in CHECK_STATUS:
        errors.append(f"{prefix}.{key} must be pass, not-run or not-in-scope")
        return ""
    return value


def require_bool(container: dict, key: str, errors: list[str], prefix: str) -> bool | None:
    value = container.get(key)
    if not isinstance(value, bool):
        errors.append(f"{prefix}.{key} must be boolean")
        return None
    return value


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_funnel_ops_receipt.py /absolute/path/to/funnel-ops-receipt.json")
        return 2

    receipt_path = Path(sys.argv[1]).expanduser().resolve()
    if not receipt_path.is_file():
        print(f"FAIL: receipt not found: {receipt_path}")
        return 1
    try:
        data = json.loads(receipt_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read valid JSON: {exc}")
        return 1

    errors: list[str] = []
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if data.get("primary_skill") != "sales-funnel-landing-page-builder":
        errors.append("primary_skill must be sales-funnel-landing-page-builder")

    artifact_status = data.get("artifact_status")
    if artifact_status not in STATUS_ORDER:
        errors.append("artifact_status is invalid")
        status_level = -1
    else:
        status_level = STATUS_ORDER[artifact_status]

    require_bool(data, "design_change", errors, "receipt")
    environment = data.get("environment")
    if environment not in {"local", "staging", "production"}:
        errors.append("environment must be local, staging or production")

    endpoint = required_object(data, "endpoint", errors, "receipt")
    required_text(endpoint, "provider", errors, "endpoint")
    endpoint_url = required_text(endpoint, "url", errors, "endpoint")
    parsed = urlparse(endpoint_url)
    if endpoint_url and (parsed.scheme != "https" or not parsed.netloc):
        errors.append("endpoint.url must be an HTTPS URL")
    required_text(endpoint, "expected_version", errors, "endpoint")
    health = check_status(endpoint, "health_readback", errors, "endpoint")
    if status_level >= STATUS_ORDER["OPS_QA_PASSED"] and health != "pass":
        errors.append("endpoint.health_readback must be pass for OPS_QA_PASSED or higher")

    crm = required_object(data, "crm", errors, "receipt")
    crm_in_scope = require_bool(crm, "in_scope", errors, "crm")
    schema = check_status(crm, "schema_readback", errors, "crm")
    if crm_in_scope:
        required_text(crm, "destination_id", errors, "crm")
        required_text(crm, "sheet", errors, "crm")
        require_bool(crm, "test_rows_excluded_from_kpis", errors, "crm")
        if status_level >= STATUS_ORDER["OPS_QA_PASSED"] and schema != "pass":
            errors.append("crm.schema_readback must be pass when CRM is in scope")
    elif crm_in_scope is False and schema != "not-in-scope":
        errors.append("crm.schema_readback must be not-in-scope when CRM is out of scope")

    automations = required_object(data, "automations", errors, "receipt")
    automation_statuses = {
        key: check_status(automations, key, errors, "automations")
        for key in ("lead_ack_email", "conditional_sales_alert", "scheduled_reminder", "manual_sales_action")
    }
    if status_level >= STATUS_ORDER["OPS_QA_PASSED"]:
        for key, value in automation_statuses.items():
            if value == "not-run":
                errors.append(f"automations.{key} cannot be not-run for OPS_QA_PASSED or higher")

    test_contract = required_object(data, "test_contract", errors, "receipt")
    test_mode = test_contract.get("mode")
    if test_mode not in TEST_MODES:
        errors.append("test_contract.mode is invalid")
    writes_production = require_bool(test_contract, "writes_production", errors, "test_contract")
    sends_external = require_bool(test_contract, "sends_external_email", errors, "test_contract")
    owned_contacts = require_bool(test_contract, "owned_contacts_only", errors, "test_contract")
    if writes_production:
        if test_mode != "tagged-production-fixture" or environment != "production":
            errors.append("production writes require tagged-production-fixture in production")
        if owned_contacts is not True:
            errors.append("production writes require owned_contacts_only true")
    if sends_external and owned_contacts is not True:
        errors.append("external test email requires owned_contacts_only true")

    live = required_object(data, "live_verification", errors, "receipt")
    production_smoke = require_bool(live, "production_smoke_performed", errors, "live_verification")
    submission_id = required_text(live, "submission_id", errors, "live_verification")
    crm_row = check_status(live, "crm_row_readback", errors, "live_verification")
    lead_email = check_status(live, "lead_email_sent_readback", errors, "live_verification")
    sales_email = check_status(live, "sales_email_sent_readback", errors, "live_verification")
    trigger = check_status(live, "trigger_readback", errors, "live_verification")
    retention = required_text(live, "retention_decision", errors, "live_verification")
    unproven = live.get("unproven")
    if not isinstance(unproven, list) or not all(isinstance(item, str) and item.strip() for item in unproven):
        errors.append("live_verification.unproven must be an array of non-empty strings")

    if production_smoke:
        if environment != "production" or owned_contacts is not True:
            errors.append("production smoke requires production and owned_contacts_only true")
        if submission_id.lower() in {"not-applicable", "not-run"}:
            errors.append("production smoke requires a real submission_id")
        if retention not in {"keep", "remove-approved"}:
            errors.append("production smoke retention_decision must be keep or remove-approved")
        if crm_in_scope and crm_row != "pass":
            errors.append("production smoke requires crm_row_readback pass")
        if automation_statuses.get("lead_ack_email") == "pass" and lead_email != "pass":
            errors.append("production smoke requires lead_email_sent_readback pass")
        if automation_statuses.get("conditional_sales_alert") == "pass" and sales_email != "pass":
            errors.append("production smoke requires sales_email_sent_readback pass")
        if any(automation_statuses.get(key) == "pass" for key in ("scheduled_reminder", "manual_sales_action")) and trigger != "pass":
            errors.append("production smoke requires trigger_readback pass")
    elif retention != "not-applicable":
        errors.append("retention_decision must be not-applicable when no production smoke was performed")

    if status_level >= STATUS_ORDER["PRODUCTION_SMOKE_VERIFIED"] and production_smoke is not True:
        errors.append("PRODUCTION_SMOKE_VERIFIED or higher requires production smoke")

    safety = required_object(data, "safety", errors, "receipt")
    for key in ("consent_enforced", "server_validation", "dedupe_or_idempotency", "formula_injection_protection", "secrets_out_of_source"):
        value = require_bool(safety, key, errors, "safety")
        if status_level >= STATUS_ORDER["OPS_QA_PASSED"] and value is not True:
            errors.append(f"safety.{key} must be true for OPS_QA_PASSED or higher")

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: funnel operations evidence and release boundaries are complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
