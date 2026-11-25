#!/usr/bin/env python3
"""Dry-run by default; copy one validated Style pack into a user-chosen Vault."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from urllib.parse import quote
from pathlib import Path

from reference_assets import reference_images, pack_version, required_files
from validate_style_pack import find_style_folder, frontmatter


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


def portable_files(source: Path) -> list[Path]:
    files = [Path(name) for name in required_files(source)]
    optional = ("DECONSTRUCTION.md", "TONE.md") if pack_version(source) == 2 else OPTIONAL_FILES
    files.extend(Path(name) for name in optional if (source / name).is_file())
    for relative in files:
        if (source / relative).is_symlink():
            raise ValueError(f"pack document must not be a symlink: {relative}")
    # Current embedded images only; do not export rejected review history or stray files.
    files.extend(reference_images(source))
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", type=Path)
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--style-id")
    parser.add_argument("--style-root", required=True, help="Exact authorized format library, relative to --vault")
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
        source = find_style_folder(experiment, args.style_id)
        style_id = read_style_id(source / "STYLE.md")
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    if source.name != style_id:
        raise SystemExit("style folder name does not match STYLE.md style_id")

    try:
        missing = [name for name in required_files(source) if not (source / name).is_file()]
    except (OSError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    if missing:
        raise SystemExit("missing required files: " + ", ".join(missing))

    validation = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("validate_style_pack.py")), str(source)],
        capture_output=True, text=True, check=False,
    )
    if validation.returncode:
        raise SystemExit("Style pack validation failed:\n" + validation.stdout + validation.stderr)

    try:
        relative_files = portable_files(source)
    except (OSError, ValueError, ImportError) as exc:
        raise SystemExit(str(exc)) from exc

    style_root = (vault / args.style_root).resolve()
    if vault != style_root and vault not in style_root.parents:
        raise SystemExit("resolved style root escapes the supplied Vault")
    destination = style_root / style_id
    if destination.exists() or destination.is_symlink():
        raise SystemExit(f"refusing to overwrite existing destination: {destination}")

    index = style_root / "INDEX.md"
    if index.is_symlink() or (index.exists() and not index.is_file()):
        raise SystemExit("refusing unsafe or non-file index")
    if source.is_symlink():
        raise SystemExit("source Style folder must not be a symlink")
    library_status = frontmatter((source / "STYLE.md").read_text(encoding="utf-8")).get("status", "candidate")
    images = reference_images(source)
    preview = images[0]
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
        "library_status": library_status,
        "reference_image_count": len(images),
        "preview_image": str(destination / preview),
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
        existing = index.read_text(encoding="utf-8") if index.exists() else "# Style candidates\n"
        links = " · ".join(
            f"[{name}]({quote(style_id + '/' + name)})"
            for name in ("STYLE.md", "DESIGN.md", "REFERENCE.md", "TONE.md")
            if Path(name) in relative_files
        )
        entry = (
            f"\n## {style_id}\n\nStatus: {library_status}\n\n{links}\n\n"
            f"![{style_id} — current preview]({quote(style_id + '/' + preview.as_posix())})\n"
        )
        index.write_text(existing.rstrip() + "\n" + entry, encoding="utf-8")
        payload["index"] = str(index)
        payload["read_back"] = [
            {
                "path": item["destination"],
                "sha256": sha256(Path(item["destination"])),
            }
            for item in manifest
        ]
        payload["read_back_verified"] = all(
            original["sha256"] == saved["sha256"]
            for original, saved in zip(manifest, payload["read_back"])
        )
        if not payload["read_back_verified"]:
            payload["status"] = "STYLE_SAVE_READ_BACK_FAILED"

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.apply and not payload["read_back_verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
