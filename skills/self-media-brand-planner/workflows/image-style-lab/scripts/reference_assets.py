"""Validate the current embedded gallery; storage count is not a model-input limit."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from urllib.parse import unquote

ASSET_ROOT = Path("assets/reference-images")
IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}

LEGACY_FILES = ("PREFERENCE.md", "REFERENCE.md", "STYLE.md", "DESIGN.md", "scorecard.md")


def frontmatter(text: str) -> dict[str, str]:
    """Read the flat scalar/inline-JSON metadata used by both pack versions."""
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        return {}
    result = {}
    for line in text[4:text.index("\n---\n", 4)].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "-")):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"'")
    return result


def pack_version(source: Path) -> int:
    path = source / "STYLE.md"
    if path.is_symlink():
        raise ValueError("STYLE.md must not be a symlink")
    value = frontmatter(path.read_text(encoding="utf-8")).get("pack_version", "1")
    if value not in {"1", "2"}:
        raise ValueError(f"unsupported pack_version: {value}")
    return int(value)


def required_files(source: Path) -> tuple[str, ...]:
    return ("STYLE.md", "DESIGN.md") if pack_version(source) == 2 else LEGACY_FILES


def reference_document(source: Path) -> str:
    return "STYLE.md" if pack_version(source) == 2 else "REFERENCE.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reference_images(source: Path) -> list[Path]:
    """Return safe, decodable, hash-inventoried images in first-embed order."""
    from PIL import Image

    document = source / reference_document(source)
    if document.is_symlink():
        raise ValueError(f"reference document must not be a symlink: {document.name}")
    text = document.read_text(encoding="utf-8")
    images: list[Path] = []
    matches = re.findall(r"!\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[\"'][^\n]*[\"'])?\s*\)", text)
    for bracketed, plain in matches:
        relative = Path(unquote(bracketed or plain))
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(f"unsafe visual reference path: {relative}")
        if not relative.is_relative_to(ASSET_ROOT):
            raise ValueError(f"image must live under the declared reference asset root: {relative}")
        if relative.suffix.lower() not in IMAGE_SUFFIXES:
            raise ValueError(f"unsupported reference image type: {relative}")
        target = source / relative
        for part in (target, *target.parents):
            if part == source:
                break
            if part.is_symlink():
                raise ValueError(f"reference image must not use a symlink: {relative}")
        if not target.is_file():
            raise ValueError(f"missing visual reference image: {relative}")
        if not target.resolve().is_relative_to(source.resolve()):
            raise ValueError(f"reference image escapes pack: {relative}")
        try:
            with Image.open(target) as picture:
                picture.verify()
            with Image.open(target) as picture:
                picture.load()
        except (OSError, ValueError) as exc:
            raise ValueError(f"invalid reference image: {relative}") from exc
        if sha256(target) not in text:
            raise ValueError(f"reference image hash missing or stale in source inventory: {relative}")
        if document.name == "STYLE.md" and not any(
            relative.as_posix() in unquote(line) and sha256(target) in line
            for line in text.splitlines()
        ):
            raise ValueError(f"reference path and hash must share one inventory row: {relative}")
        if relative not in images:
            images.append(relative)
    if not images:
        raise ValueError("visual reference board must embed at least one local image")
    stored = set()
    asset_root = source / ASSET_ROOT
    for path in asset_root.rglob("*"):
        if path.is_symlink():
            raise ValueError(f"reference asset must not be a symlink: {path.relative_to(source)}")
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            stored.add(path.relative_to(source))
    unembedded = stored - set(images)
    if unembedded:
        raise ValueError("stored reference image is not embedded: " + ", ".join(map(str, sorted(unembedded))))
    return images
