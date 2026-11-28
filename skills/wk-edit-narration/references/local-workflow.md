# 本地定位与导出

在临时目录生成分析文件。下面的 `$input` 指本轮输入音频，`$work` 指已经创建的临时目录，`$skill_dir` 指技能所在目录，`$output` 指待导出的成品路径。

## 定位切口

```sh
ffprobe -v error -select_streams a:0 \
  -show_entries stream=codec_name,sample_rate,channels:format=duration -of json "$input"
ffmpeg -nostdin -n -i "$input" -map 0:a:0 -ar 16000 -ac 1 -c:a pcm_s16le "$work/asr.wav"
ffmpeg -nostdin -hide_banner -nostats -i "$input" \
  -map 0:a:0 -af 'silencedetect=noise=-38dB:d=0.22' -f null - 2> "$work/silence.log"
```

将 `asr.wav` 交给现有的本地转写工具，选择对应的录音语言并保留时间戳。若现有工具是 `whisper-cli`，按其帮助指定已可用的模型和 JSON 输出。疑似合并或漏转的重读可在安静点附近截取小段，保留上下文后重新转写。

静音检测只提供候选边界。示例阈值适用于较干净的单人口播，需按素材的底噪和音量调整。寻找很短的剪接点时可降低最短检测时长。缩短长停顿时，可先用较宽松的阈值找整段停顿，再用更严格的阈值标出其中可安全缩短的安静区间。确认有无轻声、尾音和呼吸后再定切口。

## 渲染已确认的区间

`cuts.json` 是按时间升序排列的 `[起始秒, 结束秒]` 数组，单位为秒，起点包含在删除区间内，终点对应恢复保留的位置。例如 `[[12.48, 15.36], [41.20, 43.05]]`。用本轮输入的时间轴，复查短片转写时先加上短片起点。

脚本需要 Python 3 和单声道或双声道的 16 位 PCM WAV。分析用的 16 kHz 单声道文件留给转写。剪接用的工作文件应保留口播的声道和采样率。需要保留更多声道或更高位深时，使用支持该格式的剪辑工具处理同一份区间。

```sh
ffmpeg -nostdin -n -i "$input" -map 0:a:0 -c:a pcm_s16le "$work/edit-input.wav"
python3 "$skill_dir/scripts/render_cuts.py" "$work/edit-input.wav" "$work/cuts.json" "$work/edited.wav"
```

脚本报告删除区间数量和剪前、剪后时长。后续节奏调整可继续用 `edited.wav`，前提是定位和剪辑都使用同一份输入。如果成品用 MP3，再编码一次即可，码率按用户要求选择。下面以 192 kbps 为例。

```sh
ffmpeg -nostdin -n -i "$work/edited.wav" -c:a libmp3lame -b:a 192k "$output"
ffprobe -v error -select_streams a:0 \
  -show_entries stream=codec_name,sample_rate,channels:format=duration -of json "$output"
ffmpeg -nostdin -v error -xerror -i "$output" -map 0:a:0 -f null -
```

用户要求 WAV 时可直接使用剪接脚本输出。核对成品中的切口时，从原时间点减去前面已经删除的时长。MP3 时长可能含少量编码填充，可结合无损中间文件的采样帧数核验。
