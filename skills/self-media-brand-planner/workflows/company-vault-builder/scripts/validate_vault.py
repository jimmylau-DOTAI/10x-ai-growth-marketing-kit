#!/usr/bin/env python3
"""Validate the ready-to-use Student Company Vault without dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Optional
from urllib.parse import unquote


TEMPLATE_VERSION = "1.6"
REQUIRED_FILES = [
    "AGENTS.md",
    "INDEX.md",
    "START-HERE.md",
    "START-HERE.html",
    "00-收件箱/公司資料建立進度.md",
    "00-收件箱/來源記錄/INDEX.md",
    "10-公司與品牌/INDEX.md",
    "11-內容與平台/INDEX.md",
    "20-Projects/INDEX.md",
    "20-Projects/_Project-Template/AGENTS.md",
    "30-學習與優化/INDEX.md",
    "30-學習與優化/LOOP-STATE.md",
    "40-建庫檢查/完成報告.md",
    ".agents/skills/company-vault-builder/SKILL.md",
    ".agents/skills/company-vault-learning-loop/SKILL.md",
]
FORBIDDEN_TEMPLATE_MARKERS = [
    "/Us" + "ers/",
    "/ho" + "me/",
]
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
TEXT_SUFFIXES = {".css", ".html", ".js", ".json", ".jsonl", ".md", ".py", ".txt", ".yaml", ".yml"}


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def local_link_target(raw_target: str) -> Optional[str]:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", target):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0]).strip()
    return target or None


def read_utf8_files(root: Path) -> tuple[dict[Path, str], list[str]]:
    files: dict[Path, str] = {}
    errors: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            files[path] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"invalid_utf8:{path.relative_to(root)}")
    return files, errors


def validate_vault(vault_path: Path, strict_template: bool = False) -> dict[str, Any]:
    root = vault_path.expanduser().resolve()
    errors: list[str] = []

    if not root.exists():
        return {"ok": False, "root": str(root), "template_version": TEMPLATE_VERSION, "files": 0,
                "local_markdown_links": 0, "agents_md": False, "local_skills": 0,
                "symlinks": 0, "errors": ["vault_not_found"]}
    if not root.is_dir():
        return {"ok": False, "root": str(root), "template_version": TEMPLATE_VERSION, "files": 0,
                "local_markdown_links": 0, "agents_md": False, "local_skills": 0,
                "symlinks": 0, "errors": ["vault_path_is_not_directory"]}

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"missing_required_file:{relative}")

    symlinks = [path for path in root.rglob("*") if path.is_symlink()]
    errors.extend(f"symlink_not_allowed:{path.relative_to(root)}" for path in symlinks)

    regular_files = [path for path in root.rglob("*") if path.is_file() and not path.is_symlink()]
    text_files, utf8_errors = read_utf8_files(root)
    errors.extend(utf8_errors)

    start_here = text_files.get(root / "START-HERE.md", "")
    if f"v{TEMPLATE_VERSION}" not in start_here:
        errors.append(f"template_version_missing:v{TEMPLATE_VERSION}")

    local_skills = list((root / ".agents" / "skills").glob("*/SKILL.md"))
    expected_skills = {"company-vault-builder", "company-vault-learning-loop"}
    manifest = root / "STUDENT-KIT.json"
    if manifest.is_file():
        try:
            declared = json.loads(manifest.read_text(encoding="utf-8"))["skills"]
            if not isinstance(declared, list) or not all(isinstance(name, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) for name in declared):
                raise ValueError("skills must be a list of valid Skill names")
            if len(declared) != len(set(declared)) or not expected_skills.issubset(set(declared)):
                raise ValueError("manifest must include both base Vault Skills without duplicates")
            expected_skills = set(declared)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            errors.append(f"invalid_student_manifest:{exc}")
    actual_skills = {path.parent.name for path in local_skills}
    if actual_skills != expected_skills:
        errors.append(f"local_skill_manifest_mismatch:missing={sorted(expected_skills-actual_skills)},extra={sorted(actual_skills-expected_skills)}")

    local_link_count = 0
    for source, text in text_files.items():
        if source.suffix.lower() != ".md":
            continue
        for match in MARKDOWN_LINK_RE.finditer(text):
            target_text = local_link_target(match.group(1))
            if target_text is None:
                continue
            local_link_count += 1
            resolved = (source.parent / target_text).resolve()
            if not is_within(resolved, root):
                errors.append(f"link_escapes_vault:{source.relative_to(root)}->{target_text}")
            elif not resolved.exists():
                errors.append(f"broken_local_link:{source.relative_to(root)}->{target_text}")

    if strict_template:
        all_text = "\n".join(text_files.values()).lower()
        for marker in FORBIDDEN_TEMPLATE_MARKERS:
            if marker.lower() in all_text:
                errors.append(f"private_marker_found:{marker}")

    return {
        "ok": not errors,
        "root": str(root),
        "template_version": TEMPLATE_VERSION,
        "files": len(regular_files),
        "local_markdown_links": local_link_count,
        "agents_md": (root / "AGENTS.md").is_file(),
        "local_skills": len(local_skills),
        "symlinks": len(symlinks),
        "errors": errors,
    }


def print_receipt(result: dict[str, Any]) -> None:
    print("VAULT_VALIDATION_PASS" if result["ok"] else "VAULT_VALIDATION_FAIL")
    print(f"vault_path={result['root']}")
    print(f"template_version={result['template_version']}")
    print(f"files={result['files']}")
    print(f"local_markdown_links={result['local_markdown_links']}")
    print(f"AGENTS.md={'PASS' if result['agents_md'] else 'FAIL'}")
    print(f"local_skills={result['local_skills']}")
    print(f"symlinks={result['symlinks']}")
    if result["errors"]:
        for error in result["errors"]:
            print(f"issue={error}")
    else:
        print("issues=0")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a ready-to-use Student Company Vault.")
    parser.add_argument("--vault", required=True, help="Exact path of the Company Vault")
    parser.add_argument("--strict-template", action="store_true", help="Also scan the untouched public template")
    args = parser.parse_args()
    result = validate_vault(Path(args.vault), strict_template=args.strict_template)
    print_receipt(result)
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
