#!/usr/bin/env bash
set -euo pipefail

base_url="${TOAPIS_BASE_URL:-https://toapis.com/v1}"
reference=""; prompt=""; prompt_file=""; output=""; manifest=""; model="MiniMax-H3"; aspect_ratio="adaptive"
duration="5"; resolution="2K"; timeout_seconds="900"; poll_interval="10"; resume_task=""; dry_run=false

usage() { printf '%s\n' 'Usage: toapis_minimax_h3.sh --model MODEL --reference IMAGE --prompt TEXT --output VIDEO.mp4 [options]' '       toapis_minimax_h3.sh --resume-task TASK_ID --output VIDEO.mp4 [options]' 'Models: MiniMax-H3 | seedance-2-mini | gemini_omni_flash | gemini-omni-flash' 'Options: --prompt-file FILE --duration SECONDS --resolution VALUE --aspect-ratio RATIO' '         --manifest FILE --timeout SECONDS --poll-interval SECONDS --dry-run'; }
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model) model="$2"; shift 2 ;; --reference) reference="$2"; shift 2 ;; --prompt) prompt="$2"; shift 2 ;; --prompt-file) prompt_file="$2"; shift 2 ;;
    --output) output="$2"; shift 2 ;; --manifest) manifest="$2"; shift 2 ;; --duration) duration="$2"; shift 2 ;;
    --resolution) resolution="$2"; shift 2 ;; --aspect-ratio) aspect_ratio="$2"; shift 2 ;; --timeout) timeout_seconds="$2"; shift 2 ;; --poll-interval) poll_interval="$2"; shift 2 ;;
    --resume-task) resume_task="$2"; shift 2 ;; --dry-run) dry_run=true; shift ;; --help|-h) usage; exit 0 ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done
[[ -n "$output" ]] || { printf '%s\n' '--output is required.' >&2; exit 2; }
if [[ -z "$resume_task" ]]; then
  [[ -n "$reference" && -f "$reference" ]] || { printf '%s\n' 'A readable --reference is required.' >&2; exit 2; }
  if [[ -n "$prompt_file" ]]; then [[ -r "$prompt_file" ]] || { printf 'Prompt file not readable: %s\n' "$prompt_file" >&2; exit 2; }; prompt="$(<"$prompt_file")"; fi
  [[ -n "$prompt" ]] || { printf '%s\n' 'A prompt is required.' >&2; exit 2; }
  [[ "$duration" =~ ^([4-9]|1[0-5])$ ]] || { printf '%s\n' 'Duration must be an integer from 4 to 15.' >&2; exit 2; }
  case "$model" in
    MiniMax-H3) [[ "$resolution" == '2K' || "$resolution" == '768p' ]] || { printf '%s\n' 'MiniMax-H3 resolution must be 2K or 768p.' >&2; exit 2; } ;;
    seedance-2-mini) [[ "$resolution" == '480p' || "$resolution" == '720p' || "$resolution" == '1080p' ]] || { printf '%s\n' 'seedance-2-mini resolution must be 480p, 720p or 1080p.' >&2; exit 2; } ;;
    gemini_omni_flash|gemini-omni-flash) [[ "$resolution" == '720p' || "$resolution" == '720P' ]] || { printf '%s\n' 'Gemini Omni Flash resolution must be 720p.' >&2; exit 2; }; [[ "$duration" == 4 || "$duration" == 6 || "$duration" == 10 ]] || { printf '%s\n' 'Gemini Omni Flash duration must be 4, 6 or 10.' >&2; exit 2; }; [[ "$aspect_ratio" == '16:9' || "$aspect_ratio" == '9:16' ]] || { printf '%s\n' 'Gemini Omni Flash aspect ratio must be 16:9 or 9:16.' >&2; exit 2; } ;;
    *) printf 'Unsupported model: %s\n' "$model" >&2; exit 2 ;;
  esac
  bytes="$(wc -c < "$reference" | tr -d ' ')"; (( bytes <= 10485760 )) || { printf '%s\n' 'Reference exceeds the ToAPIs upload endpoint 10MB limit.' >&2; exit 2; }
fi
[[ -n "$manifest" ]] || manifest="${output%.*}.manifest.json"
if "$dry_run"; then printf 'dry-run valid model=%s duration=%s resolution=%s aspect_ratio=%s reference=%s output=%s\n' "$model" "$duration" "$resolution" "$aspect_ratio" "${reference:-resume}" "$output"; exit 0; fi
[[ -n "${TOAPIS_API_KEY:-}" ]] || { printf '%s\n' 'TOAPIS_API_KEY is missing. Configure it in your execution environment; do not paste it into chat or package it with this Skill.' >&2; exit 3; }
mkdir -p "$(dirname "$output")" "$(dirname "$manifest")"
api_error() { printf '%s' "$1" | jq -r '.error.message // .error // .message // .fail_reason // "Unknown ToAPIs error"' 2>/dev/null | head -c 1000 >&2 || printf 'Unknown ToAPIs error' >&2; printf '\n' >&2; }
if [[ -n "$resume_task" ]]; then
  task_id="$resume_task"; mode='resume'; printf 'resuming task=%s\n' "$task_id"
else
  upload_response="$(curl --silent --show-error --max-time 90 --request POST "$base_url/uploads/images" --header "Authorization: Bearer $TOAPIS_API_KEY" --form "file=@${reference}")"
  image_url="$(printf '%s' "$upload_response" | jq -r '.data.url // empty')"
  if [[ -z "$image_url" ]]; then printf '%s' 'Reference upload failed: ' >&2; api_error "$upload_response"; exit 4; fi
  case "$model" in
    MiniMax-H3) payload="$(jq -n --arg prompt "$prompt" --arg image_url "$image_url" --argjson duration "$duration" --arg resolution "$resolution" '{model:"MiniMax-H3",prompt:$prompt,duration:$duration,resolution:$resolution,image_with_roles:[{url:$image_url,role:"first_frame"}],watermark:false}')" ;;
    seedance-2-mini) payload="$(jq -n --arg model "$model" --arg prompt "$prompt" --arg image_url "$image_url" --argjson duration "$duration" --arg resolution "$resolution" --arg aspect_ratio "$aspect_ratio" '{model:$model,prompt:$prompt,duration:$duration,resolution:$resolution,aspect_ratio:$aspect_ratio,image_with_roles:[{url:$image_url,role:"first_frame"}],generate_audio:false}')" ;;
    gemini_omni_flash|gemini-omni-flash) payload="$(jq -n --arg model "$model" --arg prompt "$prompt" --arg image_url "$image_url" --argjson duration "$duration" --arg resolution "720p" --arg aspect_ratio "$aspect_ratio" '{model:$model,prompt:$prompt,duration:$duration,resolution:$resolution,aspect_ratio:$aspect_ratio,image_urls:[$image_url]}')" ;;
  esac
  create_response="$(curl --silent --show-error --max-time 90 --request POST "$base_url/videos/generations" --header "Authorization: Bearer $TOAPIS_API_KEY" --header 'Content-Type: application/json' --data "$payload")"
  task_id="$(printf '%s' "$create_response" | jq -r '.id // .task_id // .data.id // empty')"
  if [[ -z "$task_id" ]]; then printf '%s' 'Generation submission failed: ' >&2; api_error "$create_response"; exit 4; fi
  mode='image-to-video'; printf 'submitted task=%s model=%s\n' "$task_id" "$model"
fi
started_at="$(date +%s)"
while :; do
  now="$(date +%s)"; if (( now - started_at >= timeout_seconds )); then printf 'timeout task=%s; use --resume-task before any resubmission\n' "$task_id" >&2; exit 5; fi
  poll_response="$(curl --silent --show-error --max-time 45 --header "Authorization: Bearer $TOAPIS_API_KEY" "$base_url/videos/generations/$task_id")"
  state="$(printf '%s' "$poll_response" | jq -r '.status // .data.status // empty')"; progress="$(printf '%s' "$poll_response" | jq -r '.progress // .data.progress // empty')"
  printf 'poll state=%s progress=%s\n' "${state:-unknown}" "${progress:-unknown}"
  if [[ "$state" == completed || "$state" == succeeded ]]; then break; fi
  if [[ "$state" == failed || "$state" == error || "$state" == cancelled ]]; then printf 'generation failed task=%s: ' "$task_id" >&2; api_error "$poll_response"; exit 4; fi
  sleep "$poll_interval"
done
video_url="$(printf '%s' "$poll_response" | jq -r '.result.data[0].url // .data[0].url // .data.url // .output[0].url // .output.url // .url // empty')"
[[ -n "$video_url" ]] || { printf 'Task completed without a downloadable video URL: %s\n' "$task_id" >&2; exit 4; }
curl --silent --show-error --fail --location --max-time 300 "$video_url" -o "$output"
width=''; height=''; actual_duration=''
if command -v ffprobe >/dev/null 2>&1; then probe="$(ffprobe -v error -show_entries stream=width,height -show_entries format=duration -of json "$output")"; width="$(printf '%s' "$probe" | jq -r '.streams[0].width // empty')"; height="$(printf '%s' "$probe" | jq -r '.streams[0].height // empty')"; actual_duration="$(printf '%s' "$probe" | jq -r '.format.duration // empty')"; fi
sha256="$(shasum -a 256 "$output" | awk '{print $1}')"; actual_model="$(printf '%s' "$poll_response" | jq -r --arg fallback "$model" '.model // .data.model // $fallback')"
jq -n --arg provider 'ToAPIs' --arg model "$actual_model" --arg mode "$mode" --arg task_id "$task_id" --arg input "$(basename "$reference")" --arg prompt "$prompt" --arg resolution "$resolution" --arg aspect_ratio "$aspect_ratio" --argjson duration "$duration" --arg output "$output" --arg width "$width" --arg height "$height" --arg actual_duration "$actual_duration" --arg sha256 "$sha256" '{provider:$provider,model:$model,mode:$mode,task_id:$task_id,status:"completed",settings:{duration_seconds:$duration,resolution:$resolution,aspect_ratio:$aspect_ratio},input:{reference:$input,prompt:$prompt},output:{path:$output,pixel_width:$width,pixel_height:$height,duration_seconds:$actual_duration,sha256:$sha256},contains_secret:false}' > "$manifest"
unset TOAPIS_API_KEY
printf 'completed task=%s output=%s dimensions=%sx%s duration=%ss manifest=%s\n' "$task_id" "$output" "${width:-unknown}" "${height:-unknown}" "${actual_duration:-unknown}" "$manifest"
