# 口播剪輯同特效方法

## 用 FFmpeg 剪 First Cut

1. **先找候選。** 用 FFprobe 讀每個原片嘅片長、時間基準同音軌。用 FFmpeg 查較長靜音、近黑畫格；有多段視覺突變可加 scene detection 找候選，按時間碼抽查畫格。背景嘈雜時，調整靜音閾值及最短時間，用片段實聽確認。
2. **逐段判斷。** 將逐字稿對原聲，逐段決定「保留／縮短／移除」。失敗起句、重錄、重複內容及打斷意思嘅停頓通常可剪；呼吸、語氣或必要交代要留。每個刪剪位置聽前後，避免截斷字頭或字尾。稿有而原片冇講嘅內容，標明補錄或刪稿。
3. **做可播粗剪。** 用確認要保留嘅原片範圍同步裁畫同聲，串成 A-Roll First Cut MP4，另存 **來源檔｜原片時間｜剪後時間｜重要刪剪原因**。從實際輸出聽接位，睇有冇突然跳動、黑格或聲畫走位。交予用戶確認節奏、次序同切點。
4. **確認後逐鏡設計。** 用 First Cut 時間做基準，每鏡定主體同重點。需要補鏡（B-Roll）就配到具體一句，負責顯示實物、操作、比較前後或交代情景。用 punch-in 時先試細幅度，檢查眼睛、頭頂同視線，再按主 Skill 交三款靜態效果及 SFX。

### 本機命令起點

先替換 `source` 做當次影片路徑。以下偵測只攞候選時間；閾值按原聲、光線與剪輯內容調整。

```bash
source='source.mp4'
ffprobe -v error -show_entries stream=index,codec_type,time_base,start_time,duration:format=start_time,duration -of json "$source"
ffmpeg -hide_banner -i "$source" -map 0:a:0 -af 'silencedetect=n=-35dB:d=0.40' -f null -
ffmpeg -hide_banner -i "$source" -an -vf 'blackdetect=d=0.08:pix_th=0.10' -f null -
ffmpeg -hide_banner -i "$source" -an -vf "select='gt(scene,0.32)',showinfo" -f null -
```

單檔且畫聲原本對時，可以用 `trim`／`atrim` 裁同一組保留區間，用 `setpts`／`asetpts` 重置每段時鐘，再用 `concat`。例如保留 0–1 秒同 2–3 秒：

```bash
ffmpeg -hide_banner -i "$source" -filter_complex \
  '[0:v:0]trim=start=0:end=1,setpts=PTS-STARTPTS[v0];[0:a:0]atrim=start=0:end=1,asetpts=PTS-STARTPTS[a0];[0:v:0]trim=start=2:end=3,setpts=PTS-STARTPTS[v1];[0:a:0]atrim=start=2:end=3,asetpts=PTS-STARTPTS[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]' \
  -map '[v]' -map '[a]' -c:v libx264 -pix_fmt yuv420p -c:a aac -movflags +faststart first-cut.mp4
ffmpeg -v error -xerror -i first-cut.mp4 -map 0:v:0 -map 0:a:0 -f null -
```

原片內畫聲起點不同、跨機位或跨檔時，先對齊時間及格式，再串接。命令例子只適用於上面嘅單檔條件。

## 用動作揀效果

先寫「主體做咩」同「觀眾因此睇得明乜」，再決定用咩效果。保持起點、觸發、落位同閱讀時間清楚。

| 觀眾要睇清乜 | 做法 | 音效／驗收 |
| --- | --- | --- |
| 產品上面某個細節 | 細幅推近，或者跟住實物畫圈、底線及箭嘴 | 視乎轉折加短 whoosh；檢查標註有冇偏離主體、有冇遮住文字 |
| 一句裡面嘅兩個選項 | 兩個詞或物件先後出現，必要時微斜或短彈一次 | 按口播 cue 用 pop；停格時仍然讀得清 |
| 一個動作點樣造成變化 | 用開／合、插入、疊層、連線或逐筆畫出嘅動畫顯示先後 | 聲音跟真正落點；檢查中間幀能否認到關係 |
| 實物或成果值得揭曉 | 遮罩揭露、物件入位或者直接切近鏡 | 用一粒短 hit 或保留自然動作聲；畫面落定俾人睇清 |
| 轉鏡要保持順滑 | 按動作接切、硬切或局部遮罩 | 檢查切點前後，尤其全畫面淡入淡出造成嘅短暫變暗 |

先用最新版原稿同可用素材實作；程式特效同 SFX 參數放入可調整嘅鏡頭元件或時間線。從一個有代表性嘅效果試畫面＋聲音，合片時重用同一參數。審片逐條記時間點及具體改法，重大修訂保留上一版方便對照。

## 研究依據

- 用戶提供嘅 ChatCut 截圖記錄到真人 A-Roll 先獨立預覽，保留自然語氣，按重點句做 punch-in，檢查切點同人面構圖；當中 1.1×、107%–110% 係該片嘅設定。
- DeaglePC 原文同開源 `topic-video` 用分鏡動詞解釋畫面，再在最終輸出檢查開頭、小屏可讀同音軌。本 Skill 取用動作用途同時間碼返工方法。 [X 原文](https://x.com/DeaglePc/status/2124494529860710696) · [topic-video](https://github.com/DeaglePC/ai-video-workflow-skills/blob/main/skills/topic-video/SKILL.md)
- 逐筆畫出同筆觸音效係一種顯示過程嘅做法，適用於觀眾需要睇清次序嘅段落。 [ArtInMotion](https://github.com/DeaglePC/ArtInMotion)
