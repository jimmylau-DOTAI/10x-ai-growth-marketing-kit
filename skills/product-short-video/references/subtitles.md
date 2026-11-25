# 抽字幕、轉錄廣東話同輸出 SRT

先定用邊條已確認剪輯時間線。有正式換聲或改切點，按當前剪後版本做。以下命令喺當次影片工作目錄跑；`skill` 改成完整解壓後嘅 Skill 資料夾。

```bash
skill='/absolute/path/product-short-video'
source='source.mp4'
mkdir -p subtitles
ffprobe -v error -select_streams s \
  -show_entries 'stream=index,codec_name:stream_tags=language,title' -of json "$source"
```

## 有可用文字字幕軌

揀返同聲線相符嘅軌。以下 `0:s:0` 係第一條字幕軌；例如要揀第二條可用 `0:s:1`，或者用 FFprobe 回報嘅全域 index，例如 `0:2`。SRT 保留文字同時間，字型及特效交畀 Remotion 或現有剪輯器。 [FFmpeg 串流選擇說明](https://ffmpeg.org/ffmpeg.html#Stream-selection)

```bash
ffmpeg -n -i "$source" -map 0:s:0 -c:s srt 'subtitles/source.srt'
```

如果字幕係由**已剪好嘅檔案**直接抽出，核對首尾時間就可以交付。若由原片抽出，按實際剪接表建立 `subtitles/cuts.csv`。下例保留原片 0–1 秒及 2–3 秒，第二段接喺成片 1 秒；`speed` 省略時用 1。可用多份 SRT，每行 `srt_path` 用相對於 CSV 嘅路徑。

```csv
srt_path,source_in,source_out,cut_in,speed
source.srt,0,1,0,1
source.srt,2,3,1,1
```

```bash
python3 "$skill/scripts/subtitles.py" retime 'subtitles/cuts.csv' 'subtitles/final.srt'
```

所有時間用秒。確認 SRT 同剪接表用同一原片起點；旁白有 L-cut 或交疊時，用實際保留嘅**口播音軌範圍**建立對照。程式會裁走刪剪區間嘅字幕，再換算每段起止。若一句跨切點，聽返剪後原聲，修正拆後仍有多餘原字嘅字幕。

## 冇可用文字軌，轉錄剪後廣東話

字幕燒入畫面、圖片式字幕軌（如 PGS 或 DVD 字幕）或字幕內容已過期時，用可讀到嘅剪後原聲做轉錄。最好從已對時、未混入底樂嘅口播軌抽音，令字幕由剪後第 0 秒起計；片中有片頭留白就保留相同留白。

```bash
ffmpeg -n -i 'first-cut.mp4' -map 0:a:0 -af 'aresample=16000:async=1:first_pts=0' \
  -ac 1 -c:a pcm_s16le 'subtitles/cut-voice.wav'
python3 "$skill/scripts/subtitles.py" transcribe \
  'subtitles/cut-voice.wav' 'subtitles/draft.srt' --model large-v3
```

轉錄命令用 faster-whisper 跑 Whisper `large-v3`，腳本明確指定廣東話 `yue` 同 `transcribe`。執行端有 `faster-whisper` 就直接跑。未裝可在有權限嘅專案環境安裝：

```bash
python3 -m venv .subtitle-env
.subtitle-env/bin/python -m pip install faster-whisper
.subtitle-env/bin/python "$skill/scripts/subtitles.py" transcribe \
  'subtitles/cut-voice.wav' 'subtitles/draft.srt' --model large-v3
```

第一次載入模型可能要下載；已有模型同需要離線時加 `--offline`。品牌名可用 `--initial-prompt '品牌名、產品型號'` 提示。 [faster-whisper 說明](https://github.com/SYSTRAN/faster-whisper) · [Whisper large-v3 語言支援](https://github.com/openai/whisper/discussions/1762)

## 對時、聽校同交付

- 將抽出／轉錄嘅 SRT 疊到同一剪後版本。逐句按原聲斷句，核對粵語字、繁體、品牌名、數字、首尾及每個改過嘅切點。保留原話，按手機畫幅試讀。
- Whisper 時間係草稿。頭尾字幕同聽到嘅說話有落差時，可先用以下命令找留白邊界，再播相應位置校正。

```bash
ffmpeg -hide_banner -i 'subtitles/cut-voice.wav' -af 'silencedetect=n=-35dB:d=0.20' -f null -
```

- 以 UTF-8 保存校對後嘅 `subtitles/final.srt`。轉錄草稿保留 `draft.srt`；如果時間線再改，重跑受影響嘅時間映射或轉錄。檢查字幕時間單調、每條起點早過終點、末條未超出成片。疊字用成片時間，留低獨立 SRT。
- 以下命令可列出 SRT 起點同持續秒數，同成片實際長度比對。

```bash
ffprobe -v error -f srt -show_entries packet=pts_time,duration_time -of csv=p=0 'subtitles/final.srt'
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 'first-cut.mp4'
```
