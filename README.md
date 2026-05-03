<p align="center">
  <img src="icon.svg" width="75%" height="75%"/>
  &nbsp;&nbsp;&nbsp;
  <img src="banner.svg" width="75%"/>
</p>

# srv3 – YouTube Karaoke Subtitle Extractor (`.srv3 → .ass`)

`srv3` is a cross-platform command-line tool built specifically for YouTube videos that use **karaoke-style, syllable-animated subtitles** (YouTube's `.srv3` subtitle format).

It downloads the video, extracts syllable-accurate karaoke subtitle data, converts it to `.ass` format (preserving all animation and timing), and organizes everything cleanly into your `~/Videos` directory.

Fully compatible with **YouTube's SABR streaming system** — downloads exactly the format you select, no forced merges unless required by the format itself.

---

## 🎤 Why `.srv3` / Karaoke Subtitles?

Many music videos, anime openings/endings, and lyric videos on YouTube use karaoke-style subtitles where words or syllables animate individually with frame-accurate timing. Standard formats like `.srt` and `.vtt` cannot preserve this behavior — YouTube stores it internally as `.srv3`.

`srv3` exists specifically to extract that data, convert it to `.ass`, and keep the karaoke animations intact.

---

## ✨ Features

- Built specifically for karaoke / syllable-animated subtitles
- Extracts YouTube `.srv3` subtitle tracks
- Converts `.srv3 → .ass` with full timing and animation precision
- Supports **burned** subtitles (hardcoded into video)
- Supports **soft** subtitles (muxed as a selectable track in MKV)
- Optional subtitle editing before processing
- Supports **separate subtitle source URLs** (e.g. grab subs from a different video)
- Pass **custom yt-dlp arguments** independently to the video and subtitle downloads
- Fully **order-independent** argument parsing — flags can go in any order
- Exact format selection — no forced audio downloads
- SABR-compatible format handling
- Clean output organized under `~/Videos/`
- Cross-platform: **Windows, Linux, macOS**

---

## 📦 Prerequisites

All of the following must be installed and available on your system `PATH`.

### Python 3.8+ *(only needed if running from source)*
- **Windows:** https://www.python.org/downloads/
- **Linux:** `sudo apt install python3` or `sudo dnf install python3`
- **macOS:** `brew install python`

### yt-dlp
- **All platforms:** `pip install yt-dlp` or https://github.com/yt-dlp/yt-dlp/releases
- **Update anytime:** `yt-dlp -U`

### ffmpeg + ffprobe
Required for burning or muxing subtitles.
- **Windows:** https://www.gyan.dev/ffmpeg/builds/ — add the `bin/` folder to your PATH
- **Linux:** `sudo apt install ffmpeg` or `sudo dnf install ffmpeg`
- **macOS:** `brew install ffmpeg`

### .NET 8 Runtime
Required by YTSubConverter.
- **All platforms:** https://dotnet.microsoft.com/en-us/download/dotnet/8.0
- Download the **Runtime** (not SDK) for your OS and architecture
- Verify: `dotnet --version`

### YTSubConverter (`ytsubconverter`)
Converts `.srv3` subtitle files to `.ass`.
- Download from https://github.com/arcusmaximus/YTSubConverter/releases
- Place `ytsubconverter` (or `ytsubconverter.exe`) somewhere on your PATH
- Linux/macOS: `chmod +x ytsubconverter`

### micro *(optional — default subtitle editor)*
Used when editing subtitles with `-se` or `-be` modes.
- **All platforms:** https://micro-editor.github.io
- **Linux:** `sudo apt install micro`
- **macOS:** `brew install micro`
- Use any editor by setting the `EDITOR` environment variable:
  ```
  # Windows (PowerShell)
  $env:EDITOR = "notepad"

  # Linux / macOS
  export EDITOR=nano
  ```

---

## 📁 Repository Layout

```
.
├── .github/
│   └── workflows/
│       └── build.yml     ← automated cross-platform build pipeline
├── srv3.py               ← main script (Windows / Linux / macOS)
├── icon.svg              ← project icon
├── banner.svg            ← project banner
├── LICENSE
└── README.md
```

---

## 🚀 Installation

### Option 1 — Precompiled Binaries *(recommended)*

Precompiled executables are available for all platforms on the [Releases](https://github.com/Copilot443/srv3-karaoke-extractor/releases) page — **no Python required**.

| File | Platform |
|---|---|
| `srv3-windows.exe` | Windows |
| `srv3-linux` | Linux |
| `srv3-macos` | macOS |

After downloading:
- Rename the file to `srv3` (or `srv3.exe` on Windows)
- Place it somewhere on your PATH so you can run it from anywhere

> **Note:** Python is bundled inside the binary. You do **not** need Python installed. All other dependencies (yt-dlp, ffmpeg, YTSubConverter, etc.) still need to be on your PATH.

### Option 2 — Run from source / compile yourself

1. Install [Python 3.8+](https://www.python.org/downloads/)
2. Clone the repo:
   ```
   git clone https://github.com/Copilot443/srv3-karaoke-extractor
   cd srv3-karaoke-extractor
   ```
3. Run directly:
   ```
   python srv3.py "<URL>"
   ```
4. Or compile to a binary:
   ```
   pip install pyinstaller
   pyinstaller --onefile srv3.py
   ```
   Output will be in `dist/`.

---

## 🎬 Usage

```
srv3 [OPTIONS] <VIDEO_URL> [MODE]
srv3 [OPTIONS] <VIDEO_URL> -S <SUBS_URL> [MODE]
```

Flags and URLs can be passed in **any order**.

### Modes

| Short | Long | Output | Description |
|-------|------|--------|-------------|
| *(none)* | | Folder `~/Videos/<title>_F<fmt>/` | Download video + `.ass`, keep both |
| `-b` | `--burn` | MP4 in `~/Videos/` | Burn subtitles into video |
| `-be` | `--burn-edit` | MP4 in `~/Videos/` | Edit `.ass` first, then burn |
| `-s` | `--soft` | MKV in `~/Videos/` | Mux `.ass` as soft subtitle track |
| `-se` | `--soft-edit` | MKV in `~/Videos/` | Edit `.ass` first, then mux |
| `-So` | `--subtitles-only` | `.ass` file only | Download and convert subtitles only |
| `-S <URL>` | `--subtitles <URL>` | Depends on mode | Use subtitles from a different URL |

### Options

| Short | Long | Description |
|-------|------|-------------|
| `-yv` | `--yt-dlp-video "<ARGS>"` | Extra yt-dlp args for the video download |
| `-ys` | `--yt-dlp-subs "<ARGS>"` | Extra yt-dlp args for the subtitle download |

---

## 💡 Examples

Download video and subtitles, keep both:
```
srv3 "https://www.youtube.com/watch?v=XXXX"
```

Burn subtitles into an MP4:
```
srv3 "https://www.youtube.com/watch?v=XXXX" --burn
```

Mux as a soft subtitle track (MKV):
```
srv3 "https://www.youtube.com/watch?v=XXXX" --soft
```

Edit subtitles before burning:
```
srv3 "https://www.youtube.com/watch?v=XXXX" --burn-edit
```

Download subtitles only:
```
srv3 "https://www.youtube.com/watch?v=XXXX" --subtitles-only
```

Video from one URL, subtitles from another, burn:
```
srv3 "https://www.youtube.com/watch?v=XXXX" -S "https://www.youtube.com/watch?v=YYYY" --burn
```

Remove sponsor segments from video only:
```
srv3 "https://www.youtube.com/watch?v=XXXX" --burn -yv "--sponsorblock-remove outro"
```

Use browser cookies for subtitle download only:
```
srv3 "https://www.youtube.com/watch?v=XXXX" -S "https://www.youtube.com/watch?v=YYYY" -ys "--cookies-from-browser chrome"
```

Full example — flags in any order:
```
srv3 -yv "--sponsorblock-remove outro" --burn-edit -S "https://www.youtube.com/watch?v=YYYY" -ys "--limit-rate 500K" "https://www.youtube.com/watch?v=XXXX"
```

---

## 🎚 Format Selection & SABR Notes

When you run `srv3`, it will:

1. Fetch and display all available formats for the video
2. Prompt you to enter a format code
3. Download exactly that format

If the selected format is video-only (no audio), yt-dlp will automatically fetch and merge the best available audio.

---

## 🧹 Uninstalling

Simply delete the `srv3` binary and remove any PATH entries or wrapper scripts you created.

---

## 🙏 Credits

- **YTSubConverter** — https://github.com/arcusmaximus/YTSubConverter
- **yt-dlp** — https://github.com/yt-dlp/yt-dlp
- **ffmpeg** — https://ffmpeg.org

---

## 📄 License

MIT License
