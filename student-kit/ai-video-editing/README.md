# Grok Bot AI 剪片實習

四段素材可以剪成好多條片。第一次做，最常卡住嘅係觀眾第一眼睇到咩，同下一鏡點解接住出現。先試好鏡頭次序，改一句要求就容易對返原片。

Grok Bot 負責收 Brief、派工同收稿。Cursor Cloud Agent 要實際讀到影片，可以執行剪輯工具同交收檔案。播得到嘅粗剪先畀同學睇到實際節奏。

導師示範《魚定蝦？》用四鏡帶出一個選擇。實習先揀一個內容方向，再剪一版，只試第一鏡嘅三款效果，最後先合片。

| 一步 | 學生要做嘅決定 | 收到嘅成果 |
| --- | --- | --- |
| 開 Bot | 用返已有剪片 Bot 或開新 Bot | 總管設定同 Skill |
| 揀方向 | 從十個方向揀一個 | Hook、主軸、下一步 |
| 睇粗剪 | 揀一個要保留或要改嘅切點 | 分鏡表、First Cut MP4 |
| 試效果 | 同一鏡揀 A、B 或 C | 三款預覽同音效落點／試聽 |
| 收成片 | 開檔睇字、聽聲同核順序 | 9:16 MP4、剪接表、有口播時嘅 SRT |

## 開 AI 剪片總管

1. 開返你已有嘅 Bot。第一次做就喺 Grok 開新 Bot，叫「AI 剪片總管」，貼[角色設定](bot-setup.txt)。
2. 將 [product-short-video Skill](../../skills/product-short-video/) 同 references、scripts 畀 Bot 讀。若 Grok 未能直接載入 GitHub，先打開 [SKILL.md](../../skills/product-short-video/SKILL.md) 同所需配套檔，再交到已授權嘅工作區。
3. 用已連接嘅 Cursor Cloud Agent。唔同裝置嘅本機路徑唔一定互通，先核對四條片讀得開、FFmpeg／FFprobe 可用同能交檔。成功用一次後，可保存為自己可重用嘅 Skill。 [Grok Bot Skills](https://docs.x.ai/grok-bot/skills-routines-and-automations) · [Cursor Cloud Agents](https://cursor.com/docs/cloud-agent)

## 實習｜四段無聲素材剪一條約 13 秒直片

下載四段原鏡。檔名已打亂，打開睇內容再排次序。

| 素材 | MP4 |
| --- | --- |
| A | [clip-a.mp4](media/clip-a.mp4) |
| B | [clip-b.mp4](media/clip-b.mp4) |
| C | [clip-c.mp4](media/clip-c.mp4) |
| D | [clip-d.mp4](media/clip-d.mp4) |

罐身同鏡內原字係教學素材，產品資料以你確認嘅原頁或實物為準。片尾可用一張自家商品圖，或者一張練習用結尾。先決定觀眾依序見到咩，再考慮推近同聲效。

### 逐輪複製畀總管

**揀剪片方向** · [純文字](prompts/01-direction.txt)

```text
我有四段無聲貓片，素材喺呢度：https://github.com/jimmylau-DOTAI/10x-ai-growth-marketing-kit/tree/codex/grok-video-classroom-public/student-kit/ai-video-editing/media。用 product-short-video 幫我諗一條約 13 秒、9:16 嘅短片。觀眾係想了解貓罐頭嘅貓主。先睇素材，交 10 個有實質分別嘅方向，每個寫 Hook、內容主軸同下一步。推薦一個，等我揀。素材罐身同原有字只當畫面示意，商品資料等我另行確認。
```

**揀定先派粗剪** · [純文字](prompts/02-first-cut.txt)

```text
我揀 [方向編號]。請派畀已連接嘅 Cursor Cloud Agent。先查讀唔讀到四段片同 product-short-video Skill，再按原素材排鏡，交有時間嘅分鏡表、一條可播放嘅 First Cut MP4，同取檔入口。講清每鏡用邊段素材同點解咁排。先等我睇節奏。
```

**試三款開場效果** · [純文字](prompts/03-effects.txt)

```text
我確認粗剪順序。只試第一鏡，用同一畫格做 A、B、C 三款「魚」「蝦」出字。每款講清楚字點出、幾時停，同兩次出字嘅音效落點。附並排預覽同簡短試聽，等我揀一款。
```

**揀款、合片同收檔** · [純文字](prompts/04-final.txt)

```text
我揀 [A／B／C] 款。沿用已確認嘅粗剪同順序，第一鏡先出「魚」再出「蝦」，兩次出字各對一粒音效。按需要加輕底樂同繁中畫面字。片尾用我確認嘅商品資料或自家結尾。交可下載嘅 9:16 MP4 同剪接表。若有原聲字幕，另交對齊剪後時間嘅 UTF-8 SRT。檢查手機畫幅、字有冇遮主體、聲畫落點同能否播放。
```

**局部改一句** · [純文字](prompts/05-revision.txt)

```text
用返上個版本同一條時間線。我只想改 [時間碼] 嗰句 [原句] 做 [新句]。先畀我嗰句預覽，再同步改字幕同畫面字。保留其他鏡頭、節奏同底樂，交新版本 MP4，同修正前後可以比較嘅時間點。
```

**進階｜真人口播同字幕** · [純文字](prompts/06-aroll.txt)

```text
呢條有廣東話原聲。先用 FFprobe／FFmpeg 執走重錄同過長停頓，保留自然呼吸，交可播 First Cut 同原片到剪後時間對照。剪接確認後，有文字字幕軌就抽取並重對時間，冇就用 Whisper 轉錄剪後音訊。聽校品牌名、粵語同數字，再交 UTF-8 SRT 同 MP4。
```

## 交功課同兩個小實驗

- 交一段可播放粗剪同一條約 13 秒、9:16 嘅成片，附剪接表，留時間、素材、畫面字同音效。有口播就交對齊剪後時間嘅 SRT。
- **實驗 A｜聲畫對時。** 同一開場播兩次。第一次只出字，第二次兩次出字各加一下 pop。講低邊版更容易睇清「魚」「蝦」，同音效係咪落得準。
- **實驗 B｜局部改稿。** 用秒數指定一個修改，例如「0:03 轉鏡太急，上一鏡留多 0.3 秒」。比較改前改後嗰段，再播成片核對字幕同聲音。
- 用手機直向開片，睇頭三秒主體、畫面字會唔會遮畫面、片尾讀唔讀得完。收到 Cloud Agent 連結後，自己下載並播一次，將交件確認留喺任務卡。

[老師《魚定蝦？》節奏對照](reference-timeline.md) · [字幕處理方法](../../skills/product-short-video/references/subtitles.md) · [Cursor 收檔說明](https://cursor.com/docs/cloud-agent/api/endpoints#artifacts)
