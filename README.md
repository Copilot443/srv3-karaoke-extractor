# srv3-karaoke-extractor – YouTube Karaoke Subtitle Extractor (`.srv3 → .ass`)

`srv3` is a Linux command-line tool designed specifically for YouTube videos that use **karaoke-style, syllable-animated subtitles** (the `.srv3` subtitle format).

It downloads the video, extracts YouTube’s timing-accurate karaoke subtitle data, converts it to `.ass` format (preserving syllable animation and timing), and organizes everything cleanly into your `~/Videos` directory.

Newer versions of `srv3` are fully compatible with **YouTube’s SABR streaming system** and download **exactly the format the user selects**, without forcing separate audio streams unless required by the chosen format.

---

## 🎤 Why `.srv3` / Karaoke Subtitles?

Many music videos, anime openings/endings, and lyric videos on YouTube use karaoke-style subtitles where:

- Words or syllables animate individually
- Timing exists at the syllable level
- Standard subtitle formats (`.srt`, `.vtt`) cannot preserve this behavior

YouTube stores this data internally as `.srv3`.

`srv3` exists specifically to:

- Extract syllable-accurate subtitle timing
- Convert `.srv3 → .ass`
- Preserve karaoke animations correctly

---

## ✨ Features

- Built specifically for karaoke / syllable-animated subtitles  
- Extracts YouTube `.srv3` subtitle tracks  
- Converts `.srv3 → .ass` with full timing precision  
- Supports **burned** or **soft** subtitles  
- Optional subtitle editing before processing  
- Supports **separate subtitle source URLs**  
- Exact format selection (no forced audio downloads)  
- SABR-compatible format handling  
- Clean output structure in `~/Videos/`  
- Global `srv3` command usable from anywhere  

---

## 📦 Requirements

Installed automatically by the installer:

- `yt-dlp`
- `ffmpeg`
- .NET 8 Runtime
- YTSubConverter
- `micro` (default subtitle editor)

---

## 📁 Repository Layout

```
.
├── install.sh
├── srv3
├── YTSubConverter-Linux.deb
├── YTSubConverter-Linux.tar.xz
└── README.md
```

---

## 🚀 Installation (Debian / Ubuntu / Fedora)

`srv3` uses **one unified installer** for both Debian- and Fedora-based systems. The installer automatically installs all required dependencies for your distro.

### 1️⃣ Download

**GitHub Releases (recommended):**
```
https://github.com/Copilot443/srv3-karaoke-extractor/releases
```

Or clone directly:
```bash
git clone https://github.com/Copilot443/srv3-karaoke-extractor
cd srv3-karaoke-extractor
```

### 2️⃣ Make installer executable
```bash
chmod +x install.sh
```

### 3️⃣ Run installer
```bash
sudo ./install.sh
```

The installer will:
- Detect your distro (Debian/Ubuntu or Fedora)
- Install all required dependencies
- Install yt-dlp (latest upstream binary)
- Install .NET 8 Runtime
- Install YTSubConverter
- Register global commands:
  - `srv3`
  - `ytsubconverter`

Logging out and back in is recommended after installation.

---

## 🎬 Usage

```bash
srv3 "<VIDEO_URL>" [MODE]
```

### Modes

| Mode | Output | Description |
|----|------|------------|
| *(none)* | Folder in `~/Videos/<title>_<format>/` | Downloads video + `.ass`, keeps everything |
| `-burn` | MP4 in `~/Videos/` | Burns subtitles into video |
| `-burn-e` | MP4 in `~/Videos/` | Edit `.ass` before burning |
| `-soft` | MKV in `~/Videos/` | Mux `.ass` as soft subtitle track |
| `-soft-e` | MKV in `~/Videos/` | Edit `.ass` before muxing |
| `-subs-o` | `.ass` only | Download subtitles only |
| `-subs <SUB_URL>` | Video + subs | Use subtitles from a different URL |

---

## 🎚 Format Selection & SABR Notes

When running, `srv3`:

1. Lists all available YouTube formats
2. Prompts you to select a format code
3. Downloads **exactly** the format you selected

If the selected format is video-only, yt-dlp will automatically download and merge the required audio stream. No forced audio downloads are performed.

---

## 🧹 Uninstalling

```bash
sudo rm /usr/local/bin/srv3
sudo rm /usr/local/bin/ytsubconverter
```

---

## 🙏 Credits

- **YTSubConverter** – https://github.com/arcusmaximus/YTSubConverter  
- **yt-dlp** – https://github.com/yt-dlp/yt-dlp  
- **ffmpeg** – https://git.ffmpeg.org/ffmpeg.git  

---

## 📄 License

MIT License

