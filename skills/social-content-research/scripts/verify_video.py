#!/usr/bin/env python3
"""Verify a local video without downloading, authenticating, or claiming research coverage."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone


def verify(path, expected_duration=None, require_audio=False, timeout=300):
    path = Path(path).resolve()
    if not path.is_file() or not path.stat().st_size:
        raise ValueError("Missing or empty media file")
    for tool in ("ffprobe", "ffmpeg"):
        if not shutil.which(tool):
            raise ValueError("Missing dependency: " + tool)
    if expected_duration is not None and (
        not math.isfinite(expected_duration) or expected_duration <= 0
    ):
        raise ValueError("Expected duration must be positive and finite")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,codec_name,width,height",
         "-of", "json", str(path)],
        capture_output=True, text=True, timeout=min(timeout, 30), check=True,
    )
    info = json.loads(result.stdout)
    streams = info.get("streams", [])
    videos = [s for s in streams if s.get("codec_type") == "video"]
    audios = [s for s in streams if s.get("codec_type") == "audio"]
    duration = float(info.get("format", {}).get("duration", 0))
    if not videos or not math.isfinite(duration) or duration <= 0:
        raise ValueError("No video stream or no positive finite duration")
    if videos[0].get("width", 0) <= 0 or videos[0].get("height", 0) <= 0:
        raise ValueError("Invalid video dimensions")
    if require_audio and not audios:
        raise ValueError("Expected audio stream is missing")
    tolerance = max(1.0, expected_duration * 0.01) if expected_duration else None
    if expected_duration and abs(duration - expected_duration) > tolerance:
        raise ValueError("Duration mismatch: expected %.3fs, got %.3fs" % (expected_duration, duration))
    subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-xerror", "-i", str(path),
         "-map", "0:v:0", "-map", "0:a?", "-f", "null", "-"],
        capture_output=True, text=True, timeout=timeout, check=True,
    )
    digest = hashlib.sha256()
    with path.open("rb") as media:
        for chunk in iter(lambda: media.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "acquisition_status": "VERIFIED_LOCAL",
        "local_file": str(path),
        "bytes": path.stat().st_size,
        "sha256": digest.hexdigest(),
        "duration_seconds": duration,
        "expected_duration_seconds": expected_duration,
        "duration_tolerance_seconds": tolerance,
        "streams": streams,
        "has_audio": bool(audios),
        "full_decode": "passed",
        "source_identity_check": "not_performed_by_verifier",
        "content_review": "not_performed_by_verifier",
        "reuse_clearance": "not_confirmed",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--source-url", required=True, help="Public permalink, never a signed media URL")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--method", required=True)
    parser.add_argument("--tool-version", default="not_recorded")
    parser.add_argument("--expected-duration", type=float)
    parser.add_argument("--require-audio", action="store_true")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    if args.receipt.resolve() == args.video.resolve():
        parser.error("Receipt must not overwrite the video")
    receipt = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "source_url": args.source_url,
        "source_id": args.source_id,
        "method": args.method,
        "tool_version": args.tool_version,
        "acquisition_status": "FAILED",
        "local_file": str(args.video.resolve()),
    }
    exit_code = 1
    try:
        receipt.update(verify(args.video, args.expected_duration, args.require_audio, args.timeout))
        exit_code = 0
    except subprocess.CalledProcessError as exc:
        receipt["verification_error"] = "%s exited %s: %s" % (
            Path(exc.cmd[0]).name, exc.returncode, (exc.stderr or "")[-800:]
        )
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        receipt["verification_error"] = str(exc)[:800]
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["acquisition_status"], "receipt": str(args.receipt.resolve())}))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
