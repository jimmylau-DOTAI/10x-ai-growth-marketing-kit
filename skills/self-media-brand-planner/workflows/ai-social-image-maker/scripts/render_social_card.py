#!/usr/bin/env python3
"""Build a final PNG from an AI visual, exact text, and an approved transparent Logo.

This is a deterministic finishing tool, not an image generator.  It never redraws a
Logo or invents text: it only places the supplied files and literal strings from a
reviewed layout specification.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont


FONT_CANDIDATES = (
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    r"C:\\Windows\\Fonts\\msjh.ttc",
)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def positive_int(value, label):
    if type(value) is not int or value <= 0:
        raise ValueError(f"{label} must be a positive integer")
    return value


def rect(value, canvas_size, label):
    if not isinstance(value, list) or len(value) != 4 or not all(type(n) is int for n in value):
        raise ValueError(f"{label} must be [left, top, width, height]")
    left, top, width, height = value
    if width <= 0 or height <= 0 or left < 0 or top < 0:
        raise ValueError(f"{label} must stay inside the canvas")
    if left + width > canvas_size[0] or top + height > canvas_size[1]:
        raise ValueError(f"{label} extends outside the canvas")
    return left, top, width, height


def color(value, label):
    try:
        return ImageColor.getrgb(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} is not a valid colour") from exc


def source_path(value, spec_path, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} path is required")
    path = Path(value)
    if not path.is_absolute():
        path = spec_path.parent / path
    if not path.is_file():
        raise ValueError(f"{label} file is missing: {path}")
    return path.resolve()


def font_path(value=None):
    if value:
        path = Path(value)
        if path.is_file():
            return path
        raise ValueError(f"font file is missing: {path}")
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.is_file():
            return path
    raise ValueError("no CJK-capable font found; set font_path in the layout spec")


def open_font(path, size, index=0):
    try:
        return ImageFont.truetype(str(path), size, index=index)
    except OSError as exc:
        raise ValueError(f"cannot load font: {path}") from exc


def fit_image(source, width, height, fit, allow_crop):
    image = Image.open(source).convert("RGBA")
    source_width, source_height = image.size
    if fit not in {"contain", "cover"}:
        raise ValueError("image fit must be contain or cover")
    if fit == "contain":
        scale = min(width / source_width, height / source_height)
    else:
        scale = max(width / source_width, height / source_height)
        if source_width * height != source_height * width and allow_crop is not True:
            raise ValueError("cover crop needs crop_ok: true in the layout spec")
    resized = image.resize((round(source_width * scale), round(source_height * scale)), Image.Resampling.LANCZOS)
    if fit == "cover":
        left = max(0, (resized.width - width) // 2)
        top = max(0, (resized.height - height) // 2)
        return resized.crop((left, top, left + width, top + height)), bool(left or top)
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    layer.alpha_composite(resized, ((width - resized.width) // 2, (height - resized.height) // 2))
    return layer, False


def draw_text(canvas, item, selected_font, canvas_size):
    text = item.get("text")
    if not isinstance(text, str) or not text:
        raise ValueError("each text item needs a non-empty literal text value")
    left, top, width, height = rect(item.get("box"), canvas_size, "text box")
    size = positive_int(item.get("font_size"), "font_size")
    font = open_font(selected_font, size, item.get("font_index", 0))
    alignment = item.get("align", "left")
    if alignment not in {"left", "center", "right"}:
        raise ValueError("text align must be left, center or right")
    spacing = item.get("line_spacing", round(size * 0.18))
    if type(spacing) is not int or spacing < 0:
        raise ValueError("line_spacing must be a non-negative integer")
    draw = ImageDraw.Draw(canvas)
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align=alignment, stroke_width=item.get("stroke_width", 0))
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if text_width > width or text_height > height:
        raise ValueError(f"text does not fit its declared box: {text!r}")
    x = left if alignment == "left" else left + (width - text_width if alignment == "right" else (width - text_width) // 2)
    draw.multiline_text(
        (x - bbox[0], top - bbox[1]), text, font=font, fill=color(item.get("fill", "#000000"), "text fill"),
        spacing=spacing, align=alignment, stroke_width=item.get("stroke_width", 0),
        stroke_fill=color(item.get("stroke_fill", item.get("fill", "#000000")), "stroke fill"),
    )


def render(spec_path, output_path):
    spec_path = Path(spec_path).resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    canvas_spec = spec.get("canvas", {})
    width = positive_int(canvas_spec.get("width"), "canvas width")
    height = positive_int(canvas_spec.get("height"), "canvas height")
    canvas = Image.new("RGBA", (width, height), color(canvas_spec.get("background", "#FFFFFF"), "canvas background"))
    canvas_size = (width, height)
    receipt = {"schema_version": 1, "canvas": [width, height], "images": [], "texts": [], "logo": None}

    for item in spec.get("images", []):
        source = source_path(item.get("path"), spec_path, "image")
        left, top, item_width, item_height = rect(item.get("box"), canvas_size, "image box")
        layer, cropped = fit_image(source, item_width, item_height, item.get("fit", "contain"), item.get("crop_ok", False))
        canvas.alpha_composite(layer, (left, top))
        receipt["images"].append({"path": str(source), "sha256": sha256(source), "box": [left, top, item_width, item_height], "fit": item.get("fit", "contain"), "cropped": cropped})

    logo = spec.get("logo")
    if logo:
        source = source_path(logo.get("path"), spec_path, "logo")
        left, top, logo_width, logo_height = rect(logo.get("box"), canvas_size, "logo box")
        logo_image = Image.open(source).convert("RGBA")
        scale = min(logo_width / logo_image.width, logo_height / logo_image.height)
        resized = logo_image.resize((round(logo_image.width * scale), round(logo_image.height * scale)), Image.Resampling.LANCZOS)
        canvas.alpha_composite(resized, (left + (logo_width - resized.width) // 2, top + (logo_height - resized.height) // 2))
        receipt["logo"] = {"path": str(source), "sha256": sha256(source), "box": [left, top, logo_width, logo_height], "alpha_preserved": True}

    selected_font = font_path(spec.get("font_path")) if spec.get("texts") else None
    for item in spec.get("texts", []):
        draw_text(canvas, item, selected_font, canvas_size)
        receipt["texts"].append({"text": item["text"], "box": item["box"]})

    output_path = Path(output_path)
    if output_path.exists():
        raise ValueError("output already exists; choose a new versioned filename")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, "PNG")
    receipt["output"] = {"path": str(output_path.resolve()), "sha256": sha256(output_path)}
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    try:
        receipt = render(args.spec, args.output)
        rendered = json.dumps(receipt, ensure_ascii=False, indent=2) + "\n"
        if args.receipt:
            if args.receipt.exists():
                raise ValueError("receipt already exists; choose a new versioned filename")
            args.receipt.parent.mkdir(parents=True, exist_ok=True)
            args.receipt.write_text(rendered, encoding="utf-8")
        print(rendered)
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
