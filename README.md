<p align="center">
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
- Exact format selection — no forced audio downloads
- SABR-compatible format handling
- Clean output organized under `~/Videos/`
- Cross-platform: **Windows, Linux, macOS**

---

## 📦 Prerequisites

All of the following must be installed and available on your system `PATH` before running `srv3`.

### Python 3.8+
Required to run `srv3.py`.
- **Windows:** https://www.python.org/downloads/
- **Linux:** `sudo apt install python3` or `sudo dnf install python3`
- **macOS:** `brew install python`

### yt-dlp
Used to download videos and subtitle tracks.
- **All platforms:** `pip install yt-dlp` or download the binary from https://github.com/yt-dlp/yt-dlp/releases
- **Update anytime:** `yt-dlp -U`

### ffmpeg + ffprobe
Required for burning or muxing subtitles.
- **Windows:** Download from https://www.gyan.dev/ffmpeg/builds/ — add the `bin/` folder to your PATH
- **Linux:** `sudo apt install ffmpeg` or `sudo dnf install ffmpeg`
- **macOS:** `brew install ffmpeg`

### .NET 8 Runtime
Required by YTSubConverter.
- **All platforms:** https://dotnet.microsoft.com/en-us/download/dotnet/8.0
- Download the **Runtime** (not SDK) for your OS and architecture
- Verify install: `dotnet --version`

### YTSubConverter (`ytsubconverter`)
Converts `.srv3` subtitle files to `.ass`.
- Download from https://github.com/arcusmaximus/YTSubConverter/releases
- Extract and place `ytsubconverter` (or `ytsubconverter.exe` on Windows) somewhere on your PATH
- Linux/macOS users: `chmod +x ytsubconverter`

### micro (optional — default subtitle editor)
Used when editing subtitles with `-se` / `--soft-edit` or `-be` / `--burn-edit`.
- **All platforms:** https://micro-editor.github.io / `brew install micro`
- **Linux:** `sudo apt install micro` or `sudo snap install micro`
- You can use any editor by setting the `EDITOR` environment variable:
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
├── srv3.py       ← main script (Windows / Linux / macOS)
├── LICENSE
└── README.md
```

---

## 🚀 Installation

1. Install all prerequisites listed above
2. Clone or download this repo:
   ```
   git clone https://github.com/Copilot443/srv3-karaoke-extractor
   cd srv3-karaoke-extractor
   ```
3. Run directly with Python:
   ```
   python srv3.py "<URL>"
   ```
4. **Optional — run from anywhere:** add `srv3.py` to a folder on your PATH, or create a short wrapper:
   - **Linux / macOS:** create `/usr/local/bin/srv3` containing `python /path/to/srv3.py "$@"` and `chmod +x` it
   - **Windows:** create `srv3.bat` containing `@python C:\path\to\srv3.py %*` and place it on your PATH

---

## 🎬 Usage

```
python srv3.py "<VIDEO_URL>" [MODE]
python srv3.py "<VIDEO_URL>" -S "<SUBS_URL>" [PROCESS_MODE]
```

### Modes

| Short | Long | Output | Description |
|-------|------|--------|-------------|
| *(none)* | | Folder `~/Videos/<title>_F<fmt>/` | Download video + `.ass`, keep both |
| `-b` | `--burn` | MP4 in `~/Videos/` | Burn subtitles into video |
| `-be` | `--burn-edit` | MP4 in `~/Videos/` | Edit `.ass` first, then burn |
| `-s` | `--soft` | MKV in `~/Videos/` | Mux `.ass` as soft subtitle track |
| `-se` | `--soft-edit` | MKV in `~/Videos/` | Edit `.ass` first, then mux |
| `-So` | `--subtitles-only` | `.ass` file only | Download and convert subtitles only |
| `-S <URL>` | `--subtitles <URL>` | Depends on PROCESS_MODE | Use subtitles from a different URL |

### Using a separate subtitle URL (`-S`)

When subtitles exist on a different video than the one you're downloading, pass both URLs:

```
python srv3.py "<VIDEO_URL>" -S "<SUBS_URL>" [PROCESS_MODE]
```

`PROCESS_MODE` is optional and accepts the same flags as above (`-b`, `-be`, `-s`, `-se`).

---

## 💡 Examples

Download video and subtitles, keep both in a folder:
```
python srv3.py "https://www.youtube.com/watch?v=XXXX"
```

Burn subtitles into an MP4:
```
python srv3.py "https://www.youtube.com/watch?v=XXXX" --burn
```

Mux as a soft subtitle track (MKV):
```
python srv3.py "https://www.youtube.com/watch?v=XXXX" --soft
```

Edit subtitles before burning:
```
python srv3.py "https://www.youtube.com/watch?v=XXXX" --burn-edit
```

Download subtitles only:
```
python srv3.py "https://www.youtube.com/watch?v=XXXX" --subtitles-only
```

Download video from one URL, subtitles from another, and burn:
```
python srv3.py "https://www.youtube.com/watch?v=XXXX" --subtitles "https://www.youtube.com/watch?v=YYYY" --burn
```

---

## 🎚 Format Selection & SABR Notes

When you run `srv3`, it will:

1. Fetch and display all available formats for the video
2. Prompt you to enter a format code
3. Download exactly that format

If the selected format is video-only (no audio), yt-dlp will automatically fetch and merge the best available audio. No extra configuration needed.

---

## 🧹 Uninstalling

Simply delete `srv3.py` and remove any PATH entries or wrapper scripts you created.

---

## 🙏 Credits

- **YTSubConverter** — https://github.com/arcusmaximus/YTSubConverter
- **yt-dlp** — https://github.com/yt-dlp/yt-dlp
- **ffmpeg** — https://ffmpeg.org

---

## 📄 License

MIT License
