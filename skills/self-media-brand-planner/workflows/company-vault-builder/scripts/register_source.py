#!/usr/bin/env python3
"""Register one owner-provided source file in a Student Company Vault."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import unicodedata
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import quote

from validate_vault import is_within, validate_vault


ALLOWED_SUFFIXES = {
    ".csv",
    ".docx",
    ".htm",
    ".html",
    ".jpeg",
    ".jpg",
    ".md",
    ".pdf",
    ".png",
    ".pptx",
    ".tsv",
    ".txt",
    ".webp",
    ".xlsx",
}
SOURCE_ROWS_END = "<!-- SOURCE_ROWS_END -->"
WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


class SourceRegisterError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def table_text(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def single_line(value: str, field: str, max_length: int = 240) -> str:
    cleaned = re.sub(r"\s+", " ", value).strip()
    if not cleaned:
        raise SourceRegisterError(f"empty_{field}")
    return cleaned[:max_length]


def safe_filename(name: str) -> str:
    normalized = unicodedata.normalize("NFKC", name)
    normalized = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", normalized)
    normalized = re.sub(r"\s+", "-", normalized).strip(" .-")
    if not normalized:
        normalized = "source-file"
    stem = Path(normalized).stem
    suffix = Path(normalized).suffix
    if stem.upper() in WINDOWS_RESERVED:
        stem = f"_{stem}"
    max_stem = max(1, 120 - len(suffix))
    return f"{stem[:max_stem]}{suffix}"


def find_duplicate(record_dir: Path, file_hash: str) -> Optional[Path]:
    pattern = re.compile(rf'^sha256:\s*["\']?{re.escape(file_hash)}["\']?\s*$', re.MULTILINE)
    for note in sorted(record_dir.glob("SRC-*.md")):
        try:
            text = note.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if pattern.search(text):
            return note
    return None


def frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    if not match:
        return "TBC"
    value = match.group(1).strip()
    if value.startswith('"') and value.endswith('"'):
        try:
            return str(json.loads(value))
        except json.JSONDecodeError:
            pass
    return value


def choose_source_id(record_dir: Path, file_hash: str, captured: datetime) -> str:
    date_key = captured.strftime("%Y%m%d")
    for length in (8, 12, 16, 64):
        source_id = f"SRC-{date_key}-{file_hash[:length]}"
        if not (record_dir / f"{source_id}.md").exists():
            return source_id
    raise SourceRegisterError("unable_to_allocate_source_id")


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
        delete=False,
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    try:
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def note_content(
    source_id: str,
    title: str,
    source_name: str,
    stored_path: str,
    original_link: str,
    file_hash: str,
    size_bytes: int,
    document_type: str,
    owner: str,
    privacy: str,
    rights: str,
    source_date: str,
    captured_at: str,
    target: str,
) -> str:
    return f"""---
title: {yaml_string(title)}
type: source_note
source_id: {source_id}
status: unverified
owner: {yaml_string(owner)}
source_date: {yaml_string(source_date)}
captured_at: {yaml_string(captured_at)}
source_ref: {yaml_string('owner_provided:' + source_name)}
stored_path: {yaml_string(stored_path)}
sha256: {file_hash}
size_bytes: {size_bytes}
document_type: {document_type}
privacy: {privacy}
rights: {rights}
---

# {source_id}｜{title}

[打開原始文件]({original_link})

## Read receipt

- Registration：完成；原始內容未讀
- 實際讀到的頁面／章節／工作表：未開始
- 未讀範圍：全部
- 讀取限制：TBC

## 來源內容地圖

| 頁面／章節／工作表 | 內容 | 可能相關 target | 是否需要深入讀 |
| --- | --- | --- | --- |

## 可確認資料

| Fact／claim | Locator | Freshness | 建議 target | Status |
| --- | --- | --- | --- | --- |

## 可變資料／仍需核實

- TBC

## 衝突／Owner decision

- TBC

## 建議去向及下一題

- 目標檔案：{target}
- 原因：TBC
- 下一條只問的問題：TBC

## 私隱／使用權界線

- Privacy：`{privacy}`
- Rights：`{rights}`
- 未經 Human Review，不可因為已登記就用於公開內容。
"""


def register_source(args: argparse.Namespace) -> int:
    vault = Path(args.vault).expanduser().resolve()
    source_input = Path(args.source).expanduser()
    if source_input.is_symlink():
        raise SourceRegisterError("source_symlink_not_allowed")
    source = source_input.resolve()
    validation = validate_vault(vault, strict_template=False)
    if not validation["ok"]:
        raise SourceRegisterError(
            "vault_validation_failed:" + ",".join(validation["errors"][:5])
        )

    if not source.exists():
        raise SourceRegisterError("source_file_not_found")
    if not source.is_file():
        raise SourceRegisterError("source_is_not_a_file")
    suffix = source.suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise SourceRegisterError(f"unsupported_source_type:{suffix or 'none'}")
    size_bytes = source.stat().st_size
    if args.max_megabytes <= 0:
        raise SourceRegisterError("max_megabytes_must_be_positive")
    max_bytes = int(args.max_megabytes * 1024 * 1024)
    if size_bytes <= 0:
        raise SourceRegisterError("empty_source_file")
    if size_bytes > max_bytes:
        raise SourceRegisterError(
            f"source_too_large:max_bytes={max_bytes},actual_bytes={size_bytes}"
        )

    raw_dir = vault / "00-收件箱" / "原始文件"
    record_dir = vault / "00-收件箱" / "來源記錄"
    index_path = record_dir / "INDEX.md"
    if not raw_dir.is_dir() or not index_path.is_file():
        raise SourceRegisterError("source_intake_structure_missing")

    if is_within(source, vault) and not is_within(source, raw_dir):
        raise SourceRegisterError("source_inside_vault_but_outside_raw_folder")

    file_hash = sha256_file(source)
    duplicate_note = find_duplicate(record_dir, file_hash)
    if duplicate_note is not None:
        existing_text = duplicate_note.read_text(encoding="utf-8")
        print("SOURCE_ALREADY_REGISTERED")
        print(f"source_id={frontmatter_value(existing_text, 'source_id')}")
        print(f"source_note={duplicate_note}")
        print(f"sha256={file_hash}")
        print("action=no_duplicate_created")
        return 0

    captured = datetime.now().astimezone()
    captured_at = captured.isoformat(timespec="seconds")
    source_id = choose_source_id(record_dir, file_hash, captured)
    title = single_line(args.title if args.title else source.stem, "title")
    owner = single_line(args.owner, "owner")
    source_date = single_line(args.source_date, "source_date")
    target = single_line(args.target, "target")
    document_type = suffix.lstrip(".")
    created_copy = False

    if is_within(source, raw_dir):
        stored_file = source
    else:
        stored_file = raw_dir / f"{source_id}--{safe_filename(source.name)}"
        if stored_file.exists():
            raise SourceRegisterError(f"stored_file_collision:{stored_file.name}")
        with tempfile.NamedTemporaryFile(
            prefix=f".{source_id}.", suffix=".tmp", dir=str(raw_dir), delete=False
        ) as handle:
            temporary_copy = Path(handle.name)
        try:
            shutil.copyfile(source, temporary_copy)
            if sha256_file(temporary_copy) != file_hash:
                raise SourceRegisterError("copied_source_hash_mismatch")
            os.replace(temporary_copy, stored_file)
            created_copy = True
        finally:
            if temporary_copy.exists():
                temporary_copy.unlink()

    note_path = record_dir / f"{source_id}.md"
    index_original = index_path.read_text(encoding="utf-8")
    if SOURCE_ROWS_END not in index_original:
        if created_copy:
            stored_file.unlink()
        raise SourceRegisterError("source_registry_marker_missing")

    stored_path = stored_file.relative_to(vault).as_posix()
    link_from_note = Path(os.path.relpath(stored_file, start=record_dir)).as_posix()
    encoded_link = quote(link_from_note, safe="/-._~")
    note = note_content(
        source_id=source_id,
        title=title,
        source_name=source.name,
        stored_path=stored_path,
        original_link=encoded_link,
        file_hash=file_hash,
        size_bytes=size_bytes,
        document_type=document_type,
        owner=owner,
        privacy=args.privacy,
        rights=args.rights,
        source_date=source_date,
        captured_at=captured_at,
        target=target,
    )
    row = (
        f"| [{source_id}]({source_id}.md) | {table_text(title)} | {document_type} | "
        f"{table_text(source_date)} | {table_text(owner)} | {args.privacy} | "
        f"{args.rights} | unverified | {table_text(target)} |\n"
    )
    index_updated = index_original.replace(SOURCE_ROWS_END, row + SOURCE_ROWS_END, 1)

    created_note = False
    try:
        with note_path.open("x", encoding="utf-8") as handle:
            handle.write(note)
        created_note = True
        atomic_write(index_path, index_updated)
        final_validation = validate_vault(vault, strict_template=False)
        if not final_validation["ok"]:
            raise SourceRegisterError(
                "post_register_validation_failed:"
                + ",".join(final_validation["errors"][:5])
            )
    except Exception:
        atomic_write(index_path, index_original)
        if created_note and note_path.exists():
            note_path.unlink()
        if created_copy and stored_file.exists():
            stored_file.unlink()
        raise

    print("SOURCE_REGISTER_PASS")
    print(f"source_id={source_id}")
    print(f"stored_path={stored_file}")
    print(f"source_note={note_path}")
    print(f"sha256={file_hash}")
    print(f"size_bytes={size_bytes}")
    print(f"privacy={args.privacy}")
    print("status=unverified")
    print("original_source_preserved=PASS")
    print("next_action=process_one_source_then_stop_at_SOURCE_INTAKE_REVIEW")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Register one file in a Student Company Vault.")
    parser.add_argument("--vault", required=True, help="Exact Student Company Vault path")
    parser.add_argument("--source", required=True, help="Exact source file path")
    parser.add_argument("--owner", required=True, help="Owner responsible for this source")
    parser.add_argument(
        "--privacy", required=True, choices=("public", "internal", "private")
    )
    parser.add_argument(
        "--rights",
        required=True,
        choices=("owner_provided", "public_reference", "licensed", "unknown"),
    )
    parser.add_argument("--source-date", default="TBC", help="Document date/version or TBC")
    parser.add_argument("--title", help="Optional human-readable source title")
    parser.add_argument("--target", default="TBC", help="One suggested canonical target or TBC")
    parser.add_argument("--max-megabytes", type=float, default=50.0)
    args = parser.parse_args()
    try:
        return register_source(args)
    except (SourceRegisterError, OSError, ValueError) as error:
        print("SOURCE_REGISTER_FAIL")
        print(f"source={Path(args.source).expanduser()}")
        print(f"issue={error}")
        print("action=no_canonical_knowledge_changed")
        return 2


if __name__ == "__main__":
    sys.exit(main())
