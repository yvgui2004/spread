<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  <img src="https://img.shields.io/badge/platform-Windows%20|%20macOS%20|%20Linux-blue" alt="Platform">
  <img src="https://img.shields.io/badge/GUI-CustomTkinter-3b8ed0" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/FFmpeg-pan%20filter-007808" alt="FFmpeg">
</p>

<h1 align="center">Spread — Stereo Channel Splitter</h1>

<p align="center"><strong>Spread</strong> splits the left and right channels of a stereo audio/video file into two separate stereo files — or swaps them — through a modern dual-theme GUI.<br>
<small>立体声左右声道分离工具：把立体声音频/视频的左右声道拆成两个独立的立体声文件，或反转声道，现代双主题图形界面。</small></p>

<p align="center">
  <a href="#features">Features</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#requirements">Requirements</a> ·
  <a href="#usage">Usage</a>
</p>

---

## Features

- **Channel split** — Extract the left (`_L`) and right (`_R`) channels into two separate stereo files
  <br><small>左右声道分离 — 提取左 / 右声道，各生成一个独立的立体声文件</small>
- **Channel swap** — Swap left and right channels in one click
  <br><small>声道反转 — 一键交换左右声道</small>
- **Batch input** — Add multiple audio/video files at once and process them sequentially
  <br><small>批量添加 — 一次添加多个音视频文件，顺序处理</small>
- **File info** — Preview format, codec, bitrate, sample rate, channels, and duration via ffprobe
  <br><small>文件信息 — 通过 ffprobe 预览格式、编码器、码率、采样率、声道数、时长</small>
- **Real-time progress** — Per-file progress bar with live FFmpeg log and status
  <br><small>实时进度 — 每个文件的进度条，实时 FFmpeg 日志与状态</small>
- **Keep quality** — Preserves sample rate and bitrate; lossless codecs stay lossless
  <br><small>保持音质 — 保留采样率与码率，无损编码器保持无损</small>
- **Theme & i18n** — Dark / Light theme with fade transition, and a bilingual EN/ZH UI
  <br><small>主题与双语 — 明暗主题渐变动画切换，中英文界面一键切换</small>

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/yvgui2004/spread.git
cd spread

# 2. Install dependencies
pip install -r requirements.txt

# 3. Make sure FFmpeg (ffmpeg + ffprobe) is on your PATH (see Requirements)

# 4. Run
python main.py
```

## Requirements

### 1. Python 3.10+

Download from [python.org](https://www.python.org/downloads/) and check **"Add Python to PATH"** during installation.
<br><small>从 [python.org](https://www.python.org/downloads/) 下载，安装时勾选 <strong>"Add Python to PATH"</strong>。</small>

```bash
python --version   # should be ≥ 3.10
```

### 2. CustomTkinter + Pillow

```bash
pip install -r requirements.txt
```

Or with a mirror (e.g. in China) / 国内镜像加速：

```bash
pip install customtkinter Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. FFmpeg (includes ffprobe)

The app uses `ffprobe` to read media metadata and `ffmpeg` to split the channels. Both must be available on your PATH.
<br><small>程序通过 <code>ffprobe</code> 读取媒体信息，用 <code>ffmpeg</code> 分离声道，两者都必须加入系统 PATH。</small>

**Windows:**

1. Download [ffmpeg-master-latest-win64-gpl.zip](https://github.com/BtbN/FFmpeg-Builds/releases/latest)
2. Extract to a directory, e.g. `C:\ffmpeg` / 解压到 `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH / 添加到 PATH：
   - Right-click **This PC** → Properties → Advanced system settings → Environment Variables
     <br><small>右键<strong>"此电脑"</strong> → 属性 → 高级系统设置 → 环境变量</small>
   - Find `Path` in System variables, add `C:\ffmpeg\bin`
     <br><small>在系统变量 <code>Path</code> 中添加 <code>C:\ffmpeg\bin</code></small>
4. Restart the terminal and verify / 重启终端验证：

```bash
ffmpeg -version
ffprobe -version
```

**macOS:**

```bash
brew install ffmpeg
```

**Linux (Debian / Ubuntu):**

```bash
sudo apt install ffmpeg
```

### 4. Verify

```bash
python -c "import customtkinter, PIL; print('OK')"
ffmpeg -version | head -1
```

## Usage

```bash
python main.py
```

| Step | Action |
|------|--------|
| 1 | Click **Select File** or **Batch Add** / 点击"选择文件"或"批量添加" |
| 2 | Check the file info (codec, channels, etc.) / 查看文件信息（编码器、声道数等） |
| 3 | Choose output: same folder or a custom directory / 选择输出：与源文件同目录或自定义目录 |
| 4 | Click **Start Split** to produce `_L` / `_R` files / 点击"开始分离"生成 `_L` / `_R` 文件 |
| 5 | Or click **Swap Channels** to produce a `_swap` file / 或点击"声道反转"生成 `_swap` 文件 |

> **Note**: Only stereo (≥ 2 channels) files can be split. / **注意**：仅立体声（≥ 2 声道）文件可分离。

## Output Naming

| Mode / 模式 | Output / 输出 |
|-------------|---------------|
| Split / 分离 | `name_L.ext`, `name_R.ext` |
| Swap / 反转 | `name_swap.ext` |

## Project Structure

```
spread/
├── main.py            # Main application / 主程序
├── spread.ico         # Application icon / 应用图标
├── 启动.bat           # Windows launcher / Windows 启动脚本
├── requirements.txt   # Python dependencies / Python 依赖
└── README.md          # This file / 本文件
```

## License

MIT — feel free to use, modify, and distribute.
