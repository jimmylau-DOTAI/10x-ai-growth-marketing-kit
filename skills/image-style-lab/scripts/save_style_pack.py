#!/usr/bin/env python3
"""Dry-run by default; copy one validated Style pack into a user-chosen Vault."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


REQUIRED_FILES = ("PREFERENCE.md", "REFERENCE.md", "STYLE.md", "DESIGN.md", "scorecard.md")
OPTIONAL_FILES = ("PLATFORM-ROUTE.md",)
REFERENCE_ASSET_ROOT = Path("assets/reference-images")
IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_style_id(style_file: Path) -> str:
    text = style_file.read_text(encoding="utf-8")
    match = re.search(r"^style_id:\s*([^\s#]+)", text, re.MULTILINE)
    if not match:
        raise ValueError("STYLE.md has no style_id")
    style_id = match.group(1).strip('"\'')
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", style_id):
        raise ValueError("style_id must be lowercase kebab-case")
    return style_id


def select_style(experiment: Path, requested: str | None) -> Path:
    styles = experiment / "styles"
    if requested:
        folder = styles / requested
        if not folder.is_dir():
            raise ValueError(f"style folder not found: {folder}")
        return folder
    candidates = sorted(path for path in styles.iterdir() if path.is_dir()) if styles.is_dir() else []
    if len(candidates) != 1:
        raise ValueError(f"expected exactly one style folder; found {len(candidates)}")
    return candidates[0]


def portable_files(source: Path) -> list[Path]:
    files = [Path(name) for name in REQUIRED_FILES]
    files.extend(Path(name) for name in OPTIONAL_FILES if (source / name).is_file())
    asset_root = source / REFERENCE_ASSET_ROOT
    reference_images: list[Path] = []
    if asset_root.is_dir():
        for path in sorted(asset_root.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"reference asset must not be a symlink: {path}")
            if path.is_file():
                files.append(path.relative_to(source))
                if path.suffix.lower() in IMAGE_SUFFIXES:
                    reference_images.append(path)
    if not reference_images:
        raise ValueError(
            "portable Style pack must contain at least one local reference image"
        )
    if len(reference_images) > 6:
        raise ValueError("portable Style pack may contain at most 6 reference images")
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--style-id")
    parser.add_argument("--style-root", default="Visual-Styles")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    experiment = args.experiment.expanduser().resolve()
    vault = args.vault.expanduser().resolve()
    if not experiment.is_dir():
        raise SystemExit(f"experiment not found: {experiment}")
    if not vault.is_dir():
        raise SystemExit(f"vault must already exist: {vault}")
    if Path(args.style_root).is_absolute() or ".." in Path(args.style_root).parts:
        raise SystemExit("--style-root must be a safe relative path")

    try:
        source = select_style(experiment, args.style_id)
        style_id = read_style_id(source / "STYLE.md")
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    if source.name != style_id:
        raise SystemExit("style folder name does not match STYLE.md style_id")

    missing = [name for name in REQUIRED_FILES if not (source / name).is_file()]
    if missing:
        raise SystemExit("missing required files: " + ", ".join(missing))

    try:
        relative_files = portable_files(source)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    style_root = (vault / args.style_root).resolve()
    if vault != style_root and vault not in style_root.parents:
        raise SystemExit("resolved style root escapes the supplied Vault")
    destination = style_root / style_id
    if destination.exists():
        raise SystemExit(f"refusing to overwrite existing destination: {destination}")

    manifest = [
        {
            "name": relative.as_posix(),
            "source": str(source / relative),
            "destination": str(destination / relative),
            "sha256": sha256(source / relative),
        }
        for relative in relative_files
    ]
    payload: dict[str, object] = {
        "mode": "apply" if args.apply else "dry-run",
        "style_id": style_id,
        "source": str(source),
        "destination": str(destination),
        "files": manifest,
        "status": "STYLE_SAVED" if args.apply else "STYLE_SAVE_REVIEW_STOP",
    }

    if args.apply:
        destination.mkdir(parents=True, exist_ok=False)
        for item in manifest:
            target = Path(item["destination"])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item["source"], target)
        index = style_root / "INDEX.md"
        if not index.exists():
            index.write_text(
                "# Visual Styles\n\n| Style ID | Status | Path |\n|---|---|---|\n",
                encoding="utf-8",
            )
        row = f"| `{style_id}` | saved | `{style_id}/STYLE.md` |"
        existing = index.read_text(encoding="utf-8")
        if row not in existing:
            with index.open("a", encoding="utf-8") as handle:
                handle.write(row + "\n")
        payload["index"] = str(index)
        payload["read_back"] = [
            {
                "path": item["destination"],
                "sha256": sha256(Path(item["destination"])),
            }
            for item in manifest
        ]

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
