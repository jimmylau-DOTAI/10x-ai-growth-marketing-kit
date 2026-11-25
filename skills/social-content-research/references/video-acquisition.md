# Video acquisition

Use for an explicit video download request or when the requested research needs a local media file. Preserve the exact requested URLs and IDs. Download-only work ends with files and receipts; it does not require a full SL report. This workflow selects methods; it cannot guarantee that every platform or video will work.

## Scope and boundaries

- A request to download a publicly accessible video for local research is sufficient task authorization to try a normal downloader. Do not invent a requirement for the user to own every public source, or categorically ban extractors. Download success does not establish copyright ownership, permission to redistribute, or permission to use clips in a public deck.
- Respect the execution environment's rules. Do not download merely to circumvent a tool's media display restrictions. An explicit local-file research request is a separate purpose.
- Do not bypass private-account access, paywalls, DRM, geographic restrictions, CAPTCHA, rate limits, or other access controls. A public-page extractor is not authorization to bypass those controls. Standard supported player parsing/runtime dependencies are distinct from defeating a CAPTCHA or authentication gate.
- Start without cookies, credentials, proxies or account mutation. If a source needs the user's existing authorized account, use supported first-party browser/export tools within that account's actual rights. Do not silently extract browser cookies, tokens, passwords or keychain data; do not upload credentials to download sites or third-party services.
- Keep downloads in the requested local project. Do not upload media, full transcripts, signed media URLs, credentials, or private project data to Git or a Company Vault. Record public permalink/ID and only necessary metadata. Public reuse permission remains `not confirmed` unless there is evidence.

## Choose a method by platform

First check existing source files and available tools. For public videos, a maintained extractor is often the quickest route; there is no mandatory detour through a Premium/offline button.

| Platform/source | First useful method | Next method when appropriate | Important distinction |
| --- | --- | --- | --- |
| YouTube / Shorts | Current `yt-dlp`, supported JavaScript runtime, `ffmpeg` | Repair a missing runtime or stale extractor once; publisher original; owner download/export if this is the user's channel | Premium/offline playback is not necessarily an exportable MP4. A metadata-only run is not a download. |
| Facebook / Instagram | Canonical public video/post URL with current platform extractor | Native download if offered; Page/account owner export; publisher original | Facebook `Save video` can be a bookmark. Login-required results do not authorize cookie harvesting. |
| TikTok / Douyin | Creator-enabled native Save/download where available, or public extractor | Publisher original or permitted account export | Keep attribution/watermarks; do not claim all posts support downloads. |
| X / Twitter, Bilibili, Xiaohongshu | Check the current extractor for that exact public post | Publisher-provided file or native export where available | Supported-site listing is a candidate method, not proof that this URL works. No membership/private-content bypass. |
| Vimeo | Publisher-enabled download, or public extractor | Publisher original or account-owner export | Password, private or paid access is not bypassed. |
| Publisher website / direct MP4 | Follow the publisher's visible media/download link; use HTTPS file transfer | Normal browser download if supported, or a permitted extractor for a public player | A file extension alone does not prove identity, usable media, or reuse rights. A different video is a labelled alternative. |
| User-provided local file | Verify the file and source identity | Request a replacement only if corrupt/incomplete | Do not download again unnecessarily. |

Firecrawl can find source pages, captions and publisher-provided links. Saving a webpage, screenshot or Markdown with Firecrawl is not the same as retrieving a playable video. Use an actually documented media-download capability if available; do not invent one from the tool name. Other installed APIs/connectors can be candidates only after checking their current schema, access scope and costs; do not subscribe, pay or forward private links without authorization.

## YouTube and other public extractors

Dependencies: a supported Python, current `yt-dlp` (its `default` extra includes EJS dependencies), `ffmpeg`/`ffprobe`, and a supported JavaScript runtime for YouTube. Deno is enabled by default; Node requires `--js-runtimes node`. Check current upstream docs before repairing a version problem.

If `yt-dlp` is not installed but `uv` is available, use an isolated tool environment; do not modify system Python:

```sh
uv run --python 3.12 --with 'yt-dlp[default]' python -m yt_dlp --version
ffmpeg -version
ffprobe -version
node --version
```

Set `SOURCE_URL` to the exact user-provided public URL and `OUTPUT_DIR` to the intended local directory, using normal shell quoting. `--no-playlist` prevents accidentally downloading an entire channel/playlist. `--ignore-config` and `--no-plugin-dirs` avoid inheriting unknown account or plugin behavior.

```sh
uv run --python 3.12 --with 'yt-dlp[default]' python -m yt_dlp \
  --ignore-config --no-plugin-dirs --js-runtimes node --no-playlist \
  --socket-timeout 20 --retries 1 --fragment-retries 1 --no-progress \
  -S 'res:1080,ext:mp4:m4a' --merge-output-format mp4 --remux-video mp4 \
  -P "$OUTPUT_DIR" -o '%(id)s.%(ext)s' \
  --print 'before_dl:%(id)s | %(title)s | %(duration)s seconds' \
  --print 'after_move:filepath' -- "$SOURCE_URL"
```

With an installed `yt-dlp`, use the same options directly. For other platforms omit the YouTube-specific Node option if unnecessary. For several requested URLs, give each a separate result/receipt so a successful clip does not hide another failure. Use a source-specific directory if IDs might collide.

For diagnosis use `--simulate --list-formats` with the same public URL; it does not save a video. An MP4 container can contain AV1/VP9. If the actual destination requires H.264, retain the source and produce a labelled compatible derivative:

```sh
ffmpeg -nostdin -n -i "$LOCAL_VIDEO" -c:v libx264 -crf 20 -preset medium \
  -c:a aac -b:a 160k -movflags +faststart "$COMPATIBLE_MP4"
```

Do not automatically save raw `--dump-json`/`--write-info-json` to shared storage: it can include signed URLs and unnecessary data. Retain only public title/ID/uploader, tool version, result, and verification fields needed for the task.

## Direct publisher files

Only use a URL actually linked/provided by the publisher or user; do not guess file paths or probe private storage. Use normal HTTPS transfer with bounded timeouts, download to a temporary file, then verify before naming it as the final video. Reject HTML/login/error responses masquerading as `.mp4`. Never overwrite a known good file with an error page. A `403` alone does not prove copyright or ownership: record it as a technical/access result, inspect the visible official page, and do not defeat access controls.

## Diagnose once, then change route

| Result | Appropriate next action |
| --- | --- |
| Missing command / JS runtime / EJS dependency | Install or select supported dependencies within task scope; retry once. |
| Extractor/parser failure or outdated version | Check current upstream release/docs, update the isolated environment once, retry. No repeated unsupported client tricks. |
| Requested format unavailable | List actual formats; select a real available format, then merge/remux as needed. Do not infer no video exists. |
| Timeout / transient network failure | One bounded retry or resume the same partial transfer. |
| `401` / login required / private / paywall / DRM / CAPTCHA | Stop anonymous extraction; use legitimate account-owner export, publisher file, or request the actual missing access. |
| `403` | Check the actual error and visible source. For a clearly expired public link, refresh through the normal publisher page once; if access is denied or bot-gated, stop that route. |
| `429` / rate limit | Stop, respect Retry-After, report the limitation; no proxy rotation or account cycling. |
| Downloaded file shorter than expected / wrong ID / silent-only stream | Do not call it complete. Compare source metadata and frames; browser ad/autoplay duration can be wrong. Investigate truncation, format selection, or source mismatch. |
| No supported local-file route | Report exact attempts and blocker; obtain publisher original or user file. Browser playback remains a research fallback, not a claimed MP4 download. |

Do not repeat identical failing attempts indefinitely. Do not replace a requested video with a related official video without labelling the substitution and keeping the requested item unresolved.

## Verify and deliver

1. Confirm source ID/title and actual file path. Inspect representative original frames to detect ads, autoplay and wrong sources.
2. Run the verifier for positive duration, real video stream, dimensions, codec/audio inventory, hash and full local decode. Supply `--expected-duration` when a trustworthy source duration exists, and `--require-audio` when audio is expected. Decode success is not proof of source identity, completeness beyond known metadata, or audio transcription.

```sh
python scripts/verify_video.py "$LOCAL_VIDEO" \
  --source-url "$SOURCE_URL" --source-id "$SOURCE_ID" \
  --method yt-dlp-public --tool-version "$YTDLP_VERSION" \
  --expected-duration "$EXPECTED_SECONDS" --require-audio \
  --receipt "$RECEIPT_JSON"
```

3. The verifier reports `VERIFIED_LOCAL` only after successful checks; an unverified download stays `DOWNLOADED_UNVERIFIED`. Failed checks report `FAILED`. Missing access reports `BLOCKED` in the attempt record. None automatically sets research access to `FULL`.
4. Return playable/local file links, durations, sizes, method and any unresolved item. Keep source files local. Only proceed to transcript/frame analysis when requested; only claim transcription when actual audio was processed.

## Maintained references

- [yt-dlp installation, output and format options](https://github.com/yt-dlp/yt-dlp)
- [YouTube JavaScript runtime and EJS requirements](https://github.com/yt-dlp/yt-dlp/wiki/EJS)
- [Supported extractor list; site support is not a guarantee](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- [FFmpeg / FFprobe documentation](https://ffmpeg.org/documentation.html)

Implementation checked against upstream documentation on 2026-09-24. Recheck for dependency/platform errors rather than assuming this date guarantees current compatibility.
