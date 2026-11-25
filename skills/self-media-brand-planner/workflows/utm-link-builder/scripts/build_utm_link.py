#!/usr/bin/env python3
"""Create a UTM preview URL. This script never sends, publishes, or deploys."""

import argparse
import json
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


def value(text: str, field: str) -> str:
    clean = re.sub(r"\s+", "-", text.strip().lower())
    if not clean:
        raise ValueError(f"{field} is required")
    return clean


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a review-only UTM URL")
    parser.add_argument("--url", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--medium", required=True)
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--term")
    args = parser.parse_args()

    parts = urlsplit(args.url)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError("url must be an http(s) destination URL")

    labels = {
        "utm_source": value(args.source, "source"),
        "utm_medium": value(args.medium, "medium"),
        "utm_campaign": value(args.campaign, "campaign"),
        "utm_content": value(args.content, "content"),
    }
    if args.term:
        labels["utm_term"] = value(args.term, "term")

    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update(labels)
    preview_url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
    print(json.dumps({"status": "PREVIEWED_NOT_POSTED", "url": preview_url, "labels": labels}, ensure_ascii=False))


if __name__ == "__main__":
    main()
