#!/usr/bin/env python3
"""Health-check or safely submit a Google Apps Script Web App lead endpoint."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ENDPOINT_RE = re.compile(r"^https://script\.google\.com/macros/s/[A-Za-z0-9_-]+/exec$")


class AmbiguousSubmission(RuntimeError):
    """The request may have executed but did not return structured proof."""


def valid_endpoint(raw: str) -> str:
    endpoint = raw.strip()
    if not ENDPOINT_RE.fullmatch(endpoint):
        raise ValueError("endpoint must be an Apps Script /macros/s/.../exec HTTPS URL")
    return endpoint


def load_payload(path_value: str) -> dict[str, Any]:
    try:
        if path_value == "-":
            data = json.load(sys.stdin)
        else:
            data = json.loads(Path(path_value).expanduser().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read valid payload JSON: {exc}") from exc
    if not isinstance(data, dict) or not data:
        raise ValueError("payload must be a non-empty JSON object")
    return data


def bool_value(value: Any) -> bool:
    if value is True or str(value).lower() == "true":
        return True
    if value is False or str(value).lower() == "false":
        return False
    raise ValueError("is_test must be an explicit boolean or true/false string")


def contains_marker(value: Any, marker: str) -> bool:
    if isinstance(value, dict):
        return any(contains_marker(item, marker) for item in value.values())
    if isinstance(value, list):
        return any(contains_marker(item, marker) for item in value)
    return marker in str(value)


def encode_payload(payload: dict[str, Any]) -> bytes:
    encoded: dict[str, str] = {}
    for key, value in payload.items():
        if isinstance(value, bool):
            encoded[key] = "true" if value else "false"
        elif value is None:
            encoded[key] = ""
        elif isinstance(value, (dict, list)):
            encoded[key] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        else:
            encoded[key] = str(value)
    return urllib.parse.urlencode(encoded).encode("utf-8")


def read_json_response(request: urllib.request.Request, timeout: float, submitting: bool) -> dict[str, Any]:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        if submitting:
            raise AmbiguousSubmission(f"network response failed: {exc}") from exc
        raise RuntimeError(f"health request failed: {exc}") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        if submitting:
            raise AmbiguousSubmission("endpoint returned non-JSON content") from exc
        raise RuntimeError("health endpoint returned non-JSON content") from exc
    if not isinstance(data, dict):
        raise RuntimeError("endpoint JSON response must be an object")
    return data


def health(args: argparse.Namespace) -> int:
    endpoint = valid_endpoint(args.endpoint)
    request = urllib.request.Request(endpoint, headers={"User-Agent": "Sales-Funnel-Skill/1.0"})
    data = read_json_response(request, args.timeout, submitting=False)
    passed = data.get("ok") is True and data.get("version") == args.expect_version
    print(json.dumps({
        "status": "pass" if passed else "fail",
        "service": data.get("service"),
        "expected_version": args.expect_version,
        "actual_version": data.get("version"),
    }, ensure_ascii=False))
    return 0 if passed else 1


def submit(args: argparse.Namespace) -> int:
    endpoint = valid_endpoint(args.endpoint)
    payload = load_payload(args.payload)
    expected_test = args.mode == "test"
    if bool_value(payload.get("is_test")) != expected_test:
        raise ValueError(f"payload is_test must be {str(expected_test).lower()} for --mode {args.mode}")
    if not args.allow_submit:
        raise ValueError("submission blocked: add --allow-submit only after the current test/send is authorized")

    if args.mode == "production":
        if not args.allow_production or not args.owned_contact:
            raise ValueError("production submit requires --allow-production and --owned-contact")
        marker = (args.unique_marker or "").strip()
        if len(marker) < 4 or not contains_marker(payload, marker):
            raise ValueError("production submit requires a 4+ character --unique-marker present in the payload")

    request = urllib.request.Request(
        endpoint,
        data=encode_payload(payload),
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "User-Agent": "Sales-Funnel-Skill/1.0",
        },
        method="POST",
    )
    try:
        data = read_json_response(request, args.timeout, submitting=True)
    except AmbiguousSubmission as exc:
        print(json.dumps({
            "submission_state": "AMBIGUOUS_SUBMISSION",
            "reason": str(exc),
            "next_action": "search CRM by the unique marker before any retry",
        }, ensure_ascii=False), file=sys.stderr)
        return 3

    state = "CONFIRMED_RESPONSE" if data.get("ok") is True else "REJECTED_RESPONSE"
    print(json.dumps({
        "submission_state": state,
        "ok": data.get("ok"),
        "duplicate": data.get("duplicate", False),
        "submission_id": data.get("submission_id"),
        "quality_tier": data.get("quality_tier"),
        "email_status": data.get("email_status"),
        "error": data.get("error"),
    }, ensure_ascii=False))
    return 0 if data.get("ok") is True else 1


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    subparsers = root.add_subparsers(dest="command", required=True)

    health_parser = subparsers.add_parser("health", help="read and verify endpoint version")
    health_parser.add_argument("--endpoint", required=True)
    health_parser.add_argument("--expect-version", required=True)
    health_parser.add_argument("--timeout", type=float, default=30.0)
    health_parser.set_defaults(run=health)

    submit_parser = subparsers.add_parser("submit", help="submit one explicitly authorized fixture")
    submit_parser.add_argument("--endpoint", required=True)
    submit_parser.add_argument("--payload", required=True, help="JSON file path, or - for stdin")
    submit_parser.add_argument("--mode", choices=("test", "production"), required=True)
    submit_parser.add_argument("--allow-submit", action="store_true")
    submit_parser.add_argument("--allow-production", action="store_true")
    submit_parser.add_argument("--owned-contact", action="store_true")
    submit_parser.add_argument("--unique-marker")
    submit_parser.add_argument("--timeout", type=float, default=45.0)
    submit_parser.set_defaults(run=submit)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return args.run(args)
    except (ValueError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
