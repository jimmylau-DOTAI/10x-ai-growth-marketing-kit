"""Transcribe Cantonese on the cut timeline or remap source SRT by edit ranges."""

import argparse
import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
import re


@dataclass(frozen=True)
class Cue:
    start: int
    end: int
    text: str


TIMESTAMP = r"\d{2,}:[0-5]\d:[0-5]\d[,.]\d{3}"
TIMING = re.compile(rf"^({TIMESTAMP})\s*-->\s*({TIMESTAMP})(?:\s+.*)?$")


def milliseconds(value):
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def parse_timestamp(value):
    hours, minutes, seconds = value.replace(",", ".").split(":")
    return milliseconds((int(hours) * 3600 + int(minutes) * 60 + Decimal(seconds)) * 1000)


def format_timestamp(value):
    seconds, fraction = divmod(value, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{fraction:03d}"


def read_srt(path):
    content = path.read_text(encoding="utf-8-sig").strip()
    if not content:
        return []
    cues = []
    for index, block in enumerate(re.split(r"\n[ \t]*\n+", content), 1):
        lines = block.splitlines()
        timing = TIMING.fullmatch(lines[1].strip()) if len(lines) >= 3 else None
        if not timing or not lines[0].strip().isdigit():
            raise ValueError(f"{path}: invalid SRT block {index}")
        start, end = map(parse_timestamp, timing.groups())
        if end <= start:
            raise ValueError(f"{path}: invalid timing in block {index}")
        cues.append(Cue(start, end, "\n".join(lines[2:]).strip()))
    return cues


def retime(cut_list):
    tracks = {}
    mapped = []
    with cut_list.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        required = {"srt_path", "source_in", "source_out", "cut_in"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Cuts CSV needs srt_path,source_in,source_out,cut_in and optional speed")
        for line, row in enumerate(reader, 2):
            try:
                if not row["srt_path"].strip():
                    raise ValueError("srt_path is empty")
                path = cut_list.parent / row["srt_path"].strip()
                start = Decimal(row["source_in"]) * 1000
                end = Decimal(row["source_out"]) * 1000
                cut_in = Decimal(row["cut_in"]) * 1000
                speed = Decimal(row.get("speed") or "1")
                if not all(value.is_finite() for value in (start, end, cut_in, speed)):
                    raise ValueError("times and speed must be finite")
                if start < 0 or end <= start or cut_in < 0 or speed <= 0:
                    raise ValueError("invalid cut interval or speed")
            except (InvalidOperation, ValueError, TypeError, AttributeError) as exc:
                raise ValueError(f"{cut_list}, line {line}: {exc}") from exc

            if path not in tracks:
                tracks[path] = read_srt(path)
            for cue in tracks[path]:
                left, right = max(start, cue.start), min(end, cue.end)
                if right <= left:
                    continue
                output_start = milliseconds(cut_in + (left - start) / speed)
                output_end = milliseconds(cut_in + (right - start) / speed)
                if output_end > output_start:
                    mapped.append(Cue(output_start, output_end, cue.text))
    return mapped


def transcribe(audio, model_name, offline, initial_prompt):
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise ValueError("Install faster-whisper in the Python environment used for transcription") from exc
    model = WhisperModel(model_name, device="cpu", compute_type="int8", local_files_only=offline)
    segments, _ = model.transcribe(
        str(audio),
        language="yue",
        task="transcribe",
        vad_filter=True,
        word_timestamps=True,
        initial_prompt=initial_prompt,
    )
    return [
        Cue(round(seg.start * 1000), round(seg.end * 1000), seg.text.strip())
        for seg in segments
        if seg.text.strip() and round(seg.end * 1000) > round(seg.start * 1000)
    ]


def write_srt(output, cues):
    ordered = sorted(set(cues), key=lambda cue: (cue.start, cue.end, cue.text))
    if not ordered:
        raise ValueError("No subtitles found for the supplied audio or retained ranges")
    blocks = [
        f"{index}\n{format_timestamp(cue.start)} --> {format_timestamp(cue.end)}\n{cue.text}"
        for index, cue in enumerate(ordered, 1)
    ]
    with output.open("x", encoding="utf-8") as handle:
        handle.write("\n\n".join(blocks) + "\n")
    return len(ordered)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    remap = commands.add_parser("retime", help="map extracted source subtitles through a cuts CSV")
    remap.add_argument("cuts", type=Path)
    remap.add_argument("output", type=Path)
    whisper = commands.add_parser("transcribe", help="transcribe Cantonese directly on the cut timeline")
    whisper.add_argument("audio", type=Path)
    whisper.add_argument("output", type=Path)
    whisper.add_argument("--model", default="large-v3")
    whisper.add_argument("--offline", action="store_true", help="require an already cached model")
    whisper.add_argument("--initial-prompt", help="optional brand names or vocabulary")
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError(f"{args.output} already exists; use a fresh output filename")
        if args.command == "retime":
            cues = retime(args.cuts)
        else:
            cues = transcribe(args.audio, args.model, args.offline, args.initial_prompt)
        count = write_srt(args.output, cues)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"{count} subtitles saved to {args.output}")


if __name__ == "__main__":
    main()
