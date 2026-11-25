#!/usr/bin/env python3
"""Extract mechanical raster evidence without deciding semantic Style rules."""

from __future__ import annotations

import argparse
import colorsys
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageFilter, ImageStat


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def luminance(rgb: tuple[int, int, int]) -> float:
    channels = []
    for value in rgb:
        channel = value / 255
        channels.append(
            channel / 12.92
            if channel <= 0.04045
            else ((channel + 0.055) / 1.055) ** 2.4
        )
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def dominant_swatches(image: Image.Image, count: int) -> list[dict[str, object]]:
    sample = image.convert("RGB")
    sample.thumbnail((256, 256), Image.Resampling.LANCZOS)
    quantized = sample.quantize(colors=count, method=Image.Quantize.MEDIANCUT).convert("RGB")
    colours = quantized.getcolors(maxcolors=256 * 256) or []
    total = sum(amount for amount, _ in colours) or 1
    result = []
    for amount, rgb in sorted(colours, reverse=True)[:count]:
        hue, saturation, value = colorsys.rgb_to_hsv(*(channel / 255 for channel in rgb))
        result.append(
            {
                "hex": "#{:02X}{:02X}{:02X}".format(*rgb),
                "coverage": round(amount / total, 4),
                "luminance": round(luminance(rgb), 4),
                "saturation": round(saturation, 4),
                "value": round(value, 4),
                "hue_degrees": round(hue * 360, 1),
            }
        )
    return result


def edge_density(image: Image.Image) -> float:
    sample = image.convert("L")
    sample.thumbnail((256, 256), Image.Resampling.LANCZOS)
    edges = sample.filter(ImageFilter.FIND_EDGES)
    values = list(edges.getdata())
    return round(sum(value >= 36 for value in values) / max(len(values), 1), 4)


def analyze(path: Path, colour_count: int) -> dict[str, object]:
    with Image.open(path) as opened:
        image = opened.convert("RGBA")
        width, height = image.size
        alpha = image.getchannel("A")
        alpha_stat = ImageStat.Stat(alpha)
        rgb = image.convert("RGB")
        gray_stat = ImageStat.Stat(rgb.convert("L"))
        return {
            "path": str(path.resolve()),
            "sha256": sha256(path),
            "format": opened.format,
            "dimensions": {"width": width, "height": height},
            "aspect_ratio": round(width / height, 4) if height else None,
            "orientation": "portrait" if height > width else "landscape" if width > height else "square",
            "has_transparency": alpha_stat.extrema[0][0] < 255,
            "mean_luma_8bit": round(gray_stat.mean[0], 2),
            "luma_range_8bit": list(gray_stat.extrema[0]),
            "edge_density": edge_density(rgb),
            "dominant_swatches": dominant_swatches(rgb, colour_count),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--colours", type=int, default=8)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    missing = [str(path) for path in args.images if not path.is_file()]
    if missing:
        parser.error("missing image(s): " + ", ".join(missing))
    if not 2 <= args.colours <= 16:
        parser.error("--colours must be between 2 and 16")
    payload = {
        "schema_version": 1,
        "note": "Mechanical evidence only; semantic Style decisions require visual review.",
        "images": [analyze(path, args.colours) for path in args.images],
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
