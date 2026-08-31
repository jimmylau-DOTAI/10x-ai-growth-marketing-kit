#!/usr/bin/env python3
"""Validate structural invariants for an SEO/GEO Markdown article."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)(?:\s+['\"][^)]*['\"])?\)")
IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
HTML_RE = re.compile(r"<[^>]+>")
FAQ_H2_RE = re.compile(r"^(faq|frequently asked questions|常見問題|常見問題解答)$", re.I)
DEFAULT_EXCLUDED_H2_RE = re.compile(
    r"^(faq|frequently asked questions|常見問題|常見問題解答|"
    r"references|citations|引用|參考資料|額外資源|additional resources)$",
    re.I,
)


@dataclass
class SectionResult:
    heading: str
    visible_chars: int
    brand_present: bool | None = None


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end == -1:
        return "", text
    return text[4:end], text[end + 5 :]


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value.replace(r'\"', '"').replace(r"\'", "'")


def parse_frontmatter_faq(frontmatter: str) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    current_question: str | None = None
    in_faq = False
    faq_indent = 0

    for raw in frontmatter.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        stripped = raw.strip()
        if stripped == "faq:":
            in_faq = True
            faq_indent = indent
            continue
        if in_faq and indent <= faq_indent and not stripped.startswith("-"):
            break
        if not in_faq:
            continue

        question_match = re.match(r"-\s+question:\s*(.+)$", stripped)
        if question_match:
            current_question = unquote(question_match.group(1))
            continue
        answer_match = re.match(r"answer:\s*(.+)$", stripped)
        if answer_match and current_question is not None:
            items.append((current_question, unquote(answer_match.group(1))))
            current_question = None

    return items


def strip_markdown(text: str, *, drop_headings: bool = True) -> str:
    kept: list[str] = []
    in_fence = False
    for raw in text.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if drop_headings and HEADING_RE.match(raw):
            continue
        if re.match(r"^\s*\|?\s*:?-{3,}", raw):
            continue
        line = IMAGE_RE.sub("", raw)
        line = LINK_RE.sub(lambda match: match.group(1), line)
        line = HTML_RE.sub(" ", line)
        line = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+|>\s*)", "", line)
        line = re.sub(r"[*_~]", "", line)
        line = line.replace("`", "")
        if "|" in line:
            line = line.replace("|", " ")
        kept.append(line)
    return re.sub(r"\s+", " ", html.unescape("\n".join(kept))).strip()


def compact_visible(text: str) -> str:
    return re.sub(r"\s+", "", strip_markdown(text))


def normalize_compare(text: str) -> str:
    return re.sub(r"\s+", "", strip_markdown(text)).strip().rstrip("？?")


def collect_sections(body: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str]]]:
    lines = body.splitlines()
    h2_sections: list[tuple[str, str]] = []
    h3_sections: list[tuple[str, str]] = []
    visible_faq: list[tuple[str, str]] = []
    current_h2: str | None = None
    current_h2_preamble: list[str] = []
    current_h3: str | None = None
    current_h3_body: list[str] = []
    in_faq = False

    def flush_h3() -> None:
        nonlocal current_h3, current_h3_body
        if current_h3 is None:
            return
        text = "\n".join(current_h3_body)
        if in_faq:
            visible_faq.append((current_h3, strip_markdown(text)))
        else:
            h3_sections.append((current_h3, text))
        current_h3 = None
        current_h3_body = []

    def flush_h2() -> None:
        nonlocal current_h2, current_h2_preamble
        if current_h2 is not None:
            h2_sections.append((current_h2, "\n".join(current_h2_preamble)))
        current_h2 = None
        current_h2_preamble = []

    for line in lines:
        match = HEADING_RE.match(line)
        if match:
            level = len(match.group(1))
            heading = strip_markdown(match.group(2), drop_headings=False)
            if level == 2:
                flush_h3()
                flush_h2()
                current_h2 = heading
                in_faq = bool(FAQ_H2_RE.match(heading.strip()))
                continue
            if level == 3:
                flush_h3()
                current_h3 = heading
                continue
            if level <= 3:
                flush_h3()
            continue

        if current_h3 is not None:
            current_h3_body.append(line)
        elif current_h2 is not None:
            current_h2_preamble.append(line)

    flush_h3()
    flush_h2()
    return h2_sections, h3_sections, visible_faq


def body_h1_count(body: str) -> int:
    return sum(1 for line in body.splitlines() if re.match(r"^#\s+", line))


def count_links(body: str) -> tuple[int, int]:
    internal = 0
    external = 0
    for match in LINK_RE.finditer(body):
        target = match.group(2)
        if target.startswith(("http://", "https://")):
            external += 1
        elif target.startswith(("/", "#")):
            internal += 1
    return internal, external


def first_visible_body(body: str, count: int) -> str:
    return compact_visible(body)[:count]


def faq_matches(
    frontmatter_items: Iterable[tuple[str, str]],
    visible_items: Iterable[tuple[str, str]],
) -> bool:
    front = [(normalize_compare(q), normalize_compare(a)) for q, a in frontmatter_items]
    visible = [(normalize_compare(q), normalize_compare(a)) for q, a in visible_items]
    return front == visible


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path)
    parser.add_argument(
        "--profile",
        choices=("standard", "authority_evidence_longform"),
        default="standard",
    )
    parser.add_argument("--brand", action="append", default=[])
    parser.add_argument(
        "--authority-density",
        choices=("owned_units", "per_subsection"),
        default="owned_units",
    )
    parser.add_argument(
        "--public-evidence-mode",
        choices=("source_blind", "reader_evidence"),
        default="source_blind",
    )
    parser.add_argument("--opening-brand-free", type=int)
    parser.add_argument("--h2-min", type=int)
    parser.add_argument("--h3-min", type=int)
    parser.add_argument("--max-body-h1", type=int, default=1)
    parser.add_argument("--max-images", type=int)
    parser.add_argument("--require-faq-mirror", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    raw = args.article.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(raw)

    opening_limit = args.opening_brand_free
    h2_min = args.h2_min
    h3_min = args.h3_min
    if args.profile == "authority_evidence_longform":
        opening_limit = 100 if opening_limit is None else opening_limit
        h2_min = 120 if h2_min is None else h2_min
        h3_min = 100 if h3_min is None else h3_min
    opening_limit = 0 if opening_limit is None else opening_limit
    h2_min = 0 if h2_min is None else h2_min
    h3_min = 0 if h3_min is None else h3_min

    failures: list[str] = []
    manual_checks: list[str] = []
    if args.authority_density == "per_subsection" and not args.brand:
        failures.append("per_subsection authority requires at least one --brand value")
    h1_count = body_h1_count(body)
    if h1_count > args.max_body_h1:
        failures.append(f"body H1 count {h1_count} exceeds {args.max_body_h1}")

    opening = first_visible_body(body, opening_limit or 100)
    if opening_limit and args.brand:
        lowered = opening.casefold()
        found = [brand for brand in args.brand if brand.casefold() in lowered]
        if found:
            failures.append(
                f"brand appears inside first {opening_limit} visible characters: {', '.join(found)}"
            )
    if args.profile == "authority_evidence_longform":
        manual_checks.append(
            "Confirm the opening semantics follow problem premise → primary question/search intent → direct answer."
        )
        manual_checks.append(
            "Confirm the introduction ends with reader value and a verified company answer qualification."
        )
    if args.public_evidence_mode == "reader_evidence":
        manual_checks.append(
            "Verify each public data claim has year, geography, sample/denominator, scope, limitation and a direct primary-source link."
        )

    h2_sections, h3_sections, visible_faq = collect_sections(body)
    h2_results: list[SectionResult] = []
    for heading, preamble in h2_sections:
        if DEFAULT_EXCLUDED_H2_RE.match(heading.strip()):
            continue
        length = len(compact_visible(preamble))
        h2_results.append(SectionResult(heading=heading, visible_chars=length))
        if h2_min and length < h2_min:
            failures.append(
                f"H2 preamble is {length} visible characters; minimum is {h2_min}: {heading}"
            )

    h3_results: list[SectionResult] = []
    for heading, section_body in h3_sections:
        compact = compact_visible(section_body)
        brand_present: bool | None = None
        if args.brand:
            lowered = compact.casefold()
            brand_present = any(brand.casefold() in lowered for brand in args.brand)
        h3_results.append(
            SectionResult(
                heading=heading,
                visible_chars=len(compact),
                brand_present=brand_present,
            )
        )
        if h3_min and len(compact) < h3_min:
            failures.append(
                f"H3 prose is {len(compact)} visible characters; minimum is {h3_min}: {heading}"
            )
        if (
            args.authority_density == "per_subsection"
            and args.brand
            and not brand_present
        ):
            failures.append(f"brand is absent from per-subsection authority block: {heading}")

    frontmatter_faq = parse_frontmatter_faq(frontmatter)
    faq_mirror: bool | None = None
    if args.require_faq_mirror:
        faq_mirror = faq_matches(frontmatter_faq, visible_faq)
        if not faq_mirror:
            failures.append(
                f"FAQ frontmatter ({len(frontmatter_faq)}) does not exactly mirror visible FAQ ({len(visible_faq)})"
            )

    internal_links, external_links = count_links(body)
    images = len(IMAGE_RE.findall(body))
    if args.max_images is not None and images > args.max_images:
        failures.append(f"image count {images} exceeds {args.max_images}")

    result = {
        "article": str(args.article),
        "profile": args.profile,
        "authority_density": args.authority_density,
        "public_evidence_mode": args.public_evidence_mode,
        "opening_visible_excerpt": opening,
        "opening_checked_chars": opening_limit,
        "body_h1_count": h1_count,
        "h2_sections": [asdict(item) for item in h2_results],
        "h3_sections": [asdict(item) for item in h3_results],
        "faq_frontmatter_count": len(frontmatter_faq),
        "faq_visible_count": len(visible_faq),
        "faq_mirror": faq_mirror,
        "internal_links": internal_links,
        "external_links": external_links,
        "images": images,
        "manual_checks": manual_checks,
        "failures": failures,
        "status": "PASS" if not failures else "FAIL",
    }

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"status: {result['status']}")
        print(f"opening: {opening}")
        print(f"body_h1_count: {h1_count}")
        print(f"h2_checked: {len(h2_results)}")
        print(f"h3_checked: {len(h3_results)}")
        print(f"faq_mirror: {faq_mirror}")
        print(f"links: internal={internal_links} external={external_links}")
        print(f"images: {images}")
        for item in manual_checks:
            print(f"manual_check: {item}")
        for failure in failures:
            print(f"failure: {failure}")

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
