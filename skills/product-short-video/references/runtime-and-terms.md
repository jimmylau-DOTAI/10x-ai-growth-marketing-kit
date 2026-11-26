# 工具、名詞同執行檢查

## Agent 先做嘅事

1. 檢查 Agent 有冇執行命令嘅工具及實際讀寫權限。附件已上傳到聊天，也要確認執行端可以讀到該檔。
2. 用以下命令讀回工具版本，再對每份原片跑 FFprobe。FFprobe 顯示無音軌時，先找單獨錄音或確認本片為無聲素材。影片、字幕或音效有多個版本時，核對當次要用嗰份。

```bash
command -v ffmpeg
command -v ffprobe
ffmpeg -version
ffprobe -version
```

3. 有真人原聲，照 [FFmpeg 剪輯命令](aroll-and-effects.md#本機命令起點) 分析，再交實際 First Cut MP4 同原片／剪後時間表。偵測時間係候選，切點用原聲及畫格決定。路徑有空格時在 shell 用引號包住，輸出用新檔名。
4. 睇參考片時，有 `rea-video` 可用佢定點拆；同一環境未有此工具時，可用 FFmpeg 按指定時間抽畫格，或用現成已核實截圖對照。字幕用 [字幕指引](subtitles.md) 查文字軌、按已剪版本對時或轉錄廣東話。做正式動態前先核對 Remotion 或原專案引擎是否可用。
5. 驗實際生成檔可解碼，交可以打開嘅路徑、現有版本同最後做完嘅階段。命令回報缺工具或原片未能打開，按具體狀況交代。聊天內嘅剪輯方案同實際 MP4 分開記錄。

按時間抽一張相做檢查時，替換 `source.mp4`、時間同輸出檔名。

```bash
ffmpeg -hide_banner -ss 00:00:01.250 -i 'source.mp4' -map 0:v:0 -frames:v 1 -vf 'scale=640:-2' -update 1 'review-frame.jpg'
```

## 名詞對照

| 名詞 | 白話意思同用途 |
| --- | --- |
| FFprobe | 讀原片資料，例如片長、尺寸、畫面及聲音軌、時間基準。 |
| FFmpeg | 執行抽畫格、分析靜音、裁切、串片、混音及輸出。 |
| `silencedetect`、`blackdetect`、scene detection | 分別找較靜、近黑同畫面突變嘅位置。用來縮窄檢查範圍。 |
| ASR | 將原聲轉成逐字稿；稿件要對返錄到嘅語句。 |
| A-Roll、B-Roll、First Cut | 主口播、用嚟補充某一句嘅畫面、第一條可播放粗剪。 |
| 原片時間／剪後時間 | 同一段說話喺原檔同粗剪嘅各自位置。保留兩邊先方便回頭修改。 |
| `trim`／`atrim`、`setpts`／`asetpts`、`concat` | 分別裁畫／裁聲、重置每小段嘅時鐘、將小段接返成一條片。 |
| Punch-in、cue | 短推近；以及某個字、動畫或音效發生嘅時間點。 |
| SFX、BGM、ducking | 音效、背景音樂、人講嘢時自動或手動壓低底樂。 |
| CTA、fps | 想觀眾做嘅下一步；每秒畫格數。 |
| MP4、H.264、AAC | MP4 係成片容器，H.264 同 AAC 分別係常用畫面同聲音編碼。 |
| Remotion、`Sequence`、`useCurrentFrame()` | 用程式做動畫及出片嘅引擎、時間線上嘅一段、取得目前畫格以計動畫位置。 |
