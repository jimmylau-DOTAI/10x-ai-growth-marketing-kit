#!/usr/bin/env python3
"""Append UTM previews and update their lifecycle in a project-local CSV registry."""

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


BASE_FIELDS = [
    "created_at", "destination_url", "utm_url", "source", "medium", "campaign",
    "term", "content", "status", "verified_submission_id", "notes",
]
VALID_STATUSES = {"PREVIEWED", "CREATED_UNPUBLISHED", "LIVE_VERIFIED", "PLANNED"}


def read_rows(path: Path):
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return reader.fieldnames or [], list(reader)


def write_rows(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Register or update a UTM lifecycle row")
    parser.add_argument("--registry", required=True)
    parser.add_argument("--action", choices=["append", "update-status"], required=True)
    parser.add_argument("--utm-url", required=True)
    parser.add_argument("--status", choices=sorted(VALID_STATUSES), required=True)
    parser.add_argument("--destination-url")
    parser.add_argument("--source")
    parser.add_argument("--medium")
    parser.add_argument("--campaign")
    parser.add_argument("--term", default="")
    parser.add_argument("--content")
    parser.add_argument("--submission-id", default="")
    parser.add_argument("--notes", default="")
    args = parser.parse_args()

    path = Path(args.registry)
    old_fields, rows = read_rows(path)
    fields = list(dict.fromkeys(BASE_FIELDS + old_fields))

    if args.action == "append":
        required = [args.destination_url, args.source, args.medium, args.campaign, args.content]
        if not all(required):
            parser.error("append requires destination-url, source, medium, campaign, and content")
        rows.append({
            "created_at": datetime.now(timezone.utc).isoformat(),
            "destination_url": args.destination_url,
            "utm_url": args.utm_url,
            "source": args.source,
            "medium": args.medium,
            "campaign": args.campaign,
            "term": args.term,
            "content": args.content,
            "status": args.status,
            "verified_submission_id": args.submission_id,
            "notes": args.notes,
        })
        write_rows(path, fields, rows)
        print(json.dumps({"action": "appended", "status": args.status, "registry": str(path)}, ensure_ascii=False))
        return

    for row in reversed(rows):
        if row.get("utm_url") == args.utm_url:
            row["status"] = args.status
            if args.submission_id:
                row["verified_submission_id"] = args.submission_id
            if args.notes:
                row["notes"] = args.notes
            write_rows(path, fields, rows)
            print(json.dumps({"action": "updated", "status": args.status, "registry": str(path)}, ensure_ascii=False))
            return
    parser.error("utm-url was not found in the registry")


if __name__ == "__main__":
    main()
