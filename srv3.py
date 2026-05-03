#!/usr/bin/env python3
"""
YTSubConverter + yt-dlp SABR downloader
Cross-platform (Windows, Linux, macOS)

Modes:
  (none)      -> video + subs from same URL
  -burn       -> burn subtitles
  -burn-e     -> burn + edit
  -soft       -> soft subtitles (MKV)
  -soft-e     -> soft + edit
  -subs-o     -> subtitles only
  -subs       -> video from URL1 + subtitles from URL2
"""

import sys
import os
import shutil
import subprocess
import glob
import argparse
from pathlib import Path


# -------- HELPERS --------

def which(cmd):
    """Return path to command or None."""
    return shutil.which(cmd)


def require(cmd, label=None):
    label = label or cmd
    if not which(cmd):
        die(f"{label} not found. Please install it and ensure it's on PATH.")


def die(msg, code=1):
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(code)


def quote_for_display(arg):
    """Quote an argument for display purposes if it contains spaces."""
    s = str(arg)
    return f'"{s}"' if " " in s else s


def run(args, check=True, **kwargs):
    """Run a subprocess inheriting the terminal (native color + progress bars)."""
    print("$", " ".join(quote_for_display(a) for a in args), flush=True)
    proc = subprocess.run(args, check=False, **kwargs)
    if check and proc.returncode != 0:
        die(f"Command failed with exit code {proc.returncode}: {args[0]}")
    return proc


def videos_dir():
    """Return ~/Videos, creating it if needed."""
    d = Path.home() / "Videos"
    d.mkdir(parents=True, exist_ok=True)
    return d


def safe_title(raw):
    """Replace characters that are illegal in directory/file names."""
    for ch in r'/:\*?"<>|':
        raw = raw.replace(ch, "_")
    return raw.strip()


def get_video_title(url):
    print(f'$ yt-dlp --get-title "{url}"', flush=True)
    proc = subprocess.Popen(
        ["yt-dlp", "--get-title", url],
        stdout=subprocess.PIPE,
        stderr=None,   # inherit terminal so errors print natively
        text=True,
    )
    stdout, _ = proc.communicate()
    if proc.returncode != 0:
        die("yt-dlp failed to fetch video title. See error above.")
    return stdout.strip()


def show_formats(url):
    run(["yt-dlp", "-F", url])


def pick_format():
    return input("Format code: ").strip()


def get_video_resolution(video_file):
    proc = subprocess.Popen(
        [
            "ffprobe", "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=height",
            "-of", "csv=p=0",
            str(video_file),
        ],
        stdout=subprocess.PIPE,
        stderr=None,   # inherit terminal
        text=True,
    )
    stdout, _ = proc.communicate()
    if proc.returncode != 0:
        die("ffprobe failed to detect resolution.")
    return stdout.strip()


def find_video_file(directory):
    """Find the first video file in a directory."""
    exts = ["mp4", "mkv", "webm", "avi", "flv", "mov"]
    for ext in exts:
        matches = glob.glob(str(directory / f"*.{ext}"))
        if matches:
            return Path(matches[0])
    return None


def find_ass_file(directory):
    matches = glob.glob(str(directory / "*.ass"))
    return Path(matches[0]) if matches else None


def convert_subs(dest_dir):
    """Convert all .srv3 files in dest_dir to .ass."""
    ass_file = None
    for srv3 in dest_dir.glob("*.srv3"):
        ass = srv3.with_suffix(".ass")
        run(["ytsubconverter", str(srv3), str(ass)])
        srv3.unlink()
        ass_file = ass
    return ass_file


def edit_subs(ass_file):
    editor = os.environ.get("EDITOR", "micro")
    run([editor, str(ass_file)])


def escape_ass_path(path):
    """
    Escape a path for use in ffmpeg's -vf ass=<path> filter.
    ffmpeg's lavfi parser requires:
      - backslashes replaced with forward slashes
      - colons escaped as \\: (e.g. drive letter C:)
      - single quotes in the path escaped as \\'
      - entire path wrapped in single quotes so spaces are safe
    """
    p = str(path).replace("\\", "/")
    p = p.replace("'", "\\'")
    p = p.replace(":", "\\:")
    return f"'{p}'"


def burn_subs(video_file, ass_file, out_file):
    run([
        "ffmpeg", "-y",
        "-i", str(video_file),
        "-vf", f"ass={escape_ass_path(ass_file)}",
        "-c:a", "copy",
        str(out_file),
    ])


def mux_soft_subs(video_file, ass_file, out_file):
    run([
        "ffmpeg", "-y",
        "-i", str(video_file),
        "-i", str(ass_file),
        "-c", "copy",
        "-metadata:s:s:0", "language=eng",
        "-disposition:s:0", "default",
        str(out_file),
    ])


# -------- HELP --------

HELP_TEXT = """
Usage:
  srv3.py <VIDEO_URL> [MODE] [OPTIONS]
  srv3.py <VIDEO_URL> -S/--subtitles <SUBS_URL> [PROCESS_MODE] [OPTIONS]

PROCESS_MODE (optional after -S/--subtitles):
  -s,  --soft         soft subtitles (MKV)
  -se, --soft-edit    soft + edit
  -b,  --burn         burn subtitles
  -be, --burn-edit    burn + edit

Modes:
  (none)              video + subs (same URL)
  -So, --subtitles-only     subs only
  -S,  --subtitles <URL>    video from URL1 + subs from URL2
  -b,  --burn               burn subtitles
  -be, --burn-edit          burn + edit
  -s,  --soft               soft subtitles (MKV)
  -se, --soft-edit          soft + edit

Options:
  -yv, --yt-dlp-video "<ARGS>"   extra yt-dlp args for the video download
  -ys, --yt-dlp-subs  "<ARGS>"   extra yt-dlp args for the subtitle download

Examples:
  srv3.py "URL" --burn -yv "--sponsorblock-remove outro"
  srv3.py "URL" -S "URL2" -ys "--cookies-from-browser chrome"
  srv3.py "URL" -yv "--sponsorblock-remove outro" -ys "--cookies-from-browser firefox"
"""


# -------- ARGUMENT PARSING --------

BURN_FLAGS    = {"-b",  "--burn"}
BURN_E_FLAGS  = {"-be", "--burn-edit"}
SOFT_FLAGS    = {"-s",  "--soft"}
SOFT_E_FLAGS  = {"-se", "--soft-edit"}
SUBS_FLAGS    = {"-S",  "--subtitles"}
SUBS_O_FLAGS  = {"-So", "--subtitles-only"}

ALL_PROCESS_FLAGS = BURN_FLAGS | BURN_E_FLAGS | SOFT_FLAGS | SOFT_E_FLAGS


def parse_args():
    import shlex

    raw_args = sys.argv[1:]

    if not raw_args or {"-help", "--help"} & set(raw_args):
        print(HELP_TEXT)
        sys.exit(0)

    video_url = None
    subs_url = None
    mode_flag = None
    process_mode_flag = None
    video_extra = []
    subs_extra = []

    # All known flags that consume no extra value
    MODE_FLAGS = (
        BURN_FLAGS | BURN_E_FLAGS | SOFT_FLAGS | SOFT_E_FLAGS | SUBS_O_FLAGS
    )
    # Flags that consume the next argument as a value
    VALUE_FLAGS = SUBS_FLAGS | {"--yt-dlp-video", "-yv", "--yt-dlp-subs", "-ys"}

    i = 0
    while i < len(raw_args):
        arg = raw_args[i]

        if arg in ("--yt-dlp-video", "-yv"):
            if i + 1 >= len(raw_args):
                die(f"{arg} requires a value")
            video_extra = shlex.split(raw_args[i + 1])
            i += 2

        elif arg in ("--yt-dlp-subs", "-ys"):
            if i + 1 >= len(raw_args):
                die(f"{arg} requires a value")
            subs_extra = shlex.split(raw_args[i + 1])
            i += 2

        elif arg in SUBS_FLAGS:
            if i + 1 >= len(raw_args):
                die(f"{arg} requires a subtitle URL")
            # Mark that -S was used; grab its URL
            mode_flag = arg
            subs_url = raw_args[i + 1]
            i += 2

        elif arg in MODE_FLAGS:
            # Could be a primary mode or a process mode after -S
            if mode_flag in SUBS_FLAGS and process_mode_flag is None:
                process_mode_flag = arg
            else:
                mode_flag = arg
            i += 1

        elif arg.startswith("-"):
            die(f"Unknown flag: {arg}")

        else:
            # Positional: first non-flag = video URL
            if video_url is None:
                video_url = arg
            else:
                die(f"Unexpected argument: {arg}")
            i += 1

    if not video_url:
        die("No video URL provided")

    # ---- Resolve mode ----
    if mode_flag in BURN_FLAGS:
        mode = "burn"
    elif mode_flag in BURN_E_FLAGS:
        mode = "burn-edit"
    elif mode_flag in SOFT_FLAGS:
        mode = "soft"
    elif mode_flag in SOFT_E_FLAGS:
        mode = "soft-edit"
    elif mode_flag in SUBS_O_FLAGS:
        mode = "subs-only"
    elif mode_flag in SUBS_FLAGS:
        mode = "dual-subs"
    else:
        mode = "normal"

    if mode == "dual-subs" and not subs_url:
        die("-S/--subtitles requires a subtitle URL")

    # ---- Resolve process mode after -S ----
    if process_mode_flag:
        if mode not in ("dual-subs",):
            die(f"Process mode {process_mode_flag} is only valid after -S/--subtitles")
        if process_mode_flag in BURN_FLAGS:
            mode = "dual-burn"
        elif process_mode_flag in BURN_E_FLAGS:
            mode = "dual-burn-edit"
        elif process_mode_flag in SOFT_FLAGS:
            mode = "dual-soft"
        elif process_mode_flag in SOFT_E_FLAGS:
            mode = "dual-soft-edit"
        else:
            die(f"Invalid processing mode: {process_mode_flag}")

    return video_url, mode, subs_url or "", video_extra, subs_extra


# -------- MAIN --------

def main():
    video_url, mode, subs_url, video_extra, subs_extra = parse_args()

    # ---- Dependencies ----
    require("yt-dlp")
    require("ytsubconverter")
    if "burn" in mode or "soft" in mode:
        require("ffmpeg")

    vdir = videos_dir()
    temp_dir = vdir / "xx1.temp.1xx"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    # ---- Metadata ----
    print("Fetching video title...")
    raw_title = get_video_title(video_url)
    stitle = safe_title(raw_title)

    # ---- Format Selection ----
    quality_suffix = ""
    format_code = ""
    if not mode.startswith("subs"):
        print("\nFetching available formats...")
        show_formats(video_url)
        print("\nPick the format code you want to download:")
        format_code = pick_format()
        quality_suffix = f"F{format_code}"

    # ---- Destination ----
    if mode == "normal" or mode.startswith("dual"):
        dest_dir = vdir / f"{stitle}_{quality_suffix}"
    elif mode.startswith("subs"):
        dest_dir = vdir
    else:
        dest_dir = temp_dir
    dest_dir.mkdir(parents=True, exist_ok=True)

    # ---- Video Download ----
    if not mode.startswith("subs"):
        run([
            "yt-dlp", video_url,
            "-f", format_code,
            "-o", str(dest_dir / "%(title)s.%(ext)s"),
            *video_extra,
        ])

    # ---- Subtitle Source ----
    sub_src = subs_url if mode.startswith("dual") else video_url

    run([
        "yt-dlp", sub_src,
        "--skip-download",
        "--write-subs",
        "--sub-format", "srv3",
        "-o", str(dest_dir / "%(title)s.%(ext)s"),
        *subs_extra,
    ])

    # ---- Find Video File ----
    video_file = None
    if not mode.startswith("subs"):
        video_file = find_video_file(dest_dir)
        if not video_file:
            die("Downloaded video file not found.")

    # ---- Convert Subs ----
    ass_file = convert_subs(dest_dir)
    if ass_file is None:
        die("No .srv3 subtitle file found after download.")

    # ---- Edit Subs ----
    if mode.endswith("-edit") or mode.endswith("edit"):
        edit_subs(ass_file)

    # ---- Process Video + Subs ----
    if "burn" in mode or "soft" in mode:
        res = get_video_resolution(video_file)
        ext = "mkv" if "soft" in mode else "mp4"
        out_file = vdir / f"{stitle}_{res}p.{ext}"

        if "burn" in mode:
            burn_subs(video_file, ass_file, out_file)
        else:
            mux_soft_subs(video_file, ass_file, out_file)

        shutil.rmtree(dest_dir, ignore_errors=True)

    print("\nAll done.")


if __name__ == "__main__":
    main()
