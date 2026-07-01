"""
Video transcode and info via FFmpeg (subprocess). OpenCV optional for thumbnails.
"""
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Tuple

FFMPEG_CMD = shutil.which("ffmpeg") or "ffmpeg"
FFPROBE_CMD = shutil.which("ffprobe") or "ffprobe"


def get_media_info(video_path: str) -> dict:
    """Return width, height, duration_sec, codec from ffprobe."""
    path = Path(video_path)
    if not path.exists():
        raise FileNotFoundError(video_path)
    out = subprocess.run(
        [
            FFPROBE_CMD,
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            str(path),
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    if out.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {out.stderr}")
    import json

    data = json.loads(out.stdout)
    video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    format_info = data.get("format", {})
    duration = float(format_info.get("duration", 0) or 0)
    width = int(video_stream.get("width", 0) or 0)
    height = int(video_stream.get("height", 0) or 0)
    return {
        "width": width,
        "height": height,
        "duration_sec": duration,
        "codec": video_stream.get("codec_name", ""),
        "size_bytes": int(format_info.get("size", 0) or 0),
    }


def transcode_video(
    input_path: str,
    output_path: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crf: int = 23,
    preset: str = "medium",
    timeout_sec: int = 3600,
) -> str:
    """
    Transcode to H.264. If width/height given, scale to that (keeping aspect if only one set).
    Returns output_path.
    """
    path_in = Path(input_path)
    path_out = Path(output_path)
    if not path_in.exists():
        raise FileNotFoundError(input_path)
    path_out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [FFMPEG_CMD, "-y", "-i", str(path_in), "-c:v", "libx264", "-crf", str(crf), "-preset", preset]
    if width and height:
        cmd += ["-vf", f"scale={width}:{height}"]
    elif width:
        cmd += ["-vf", f"scale={width}:-2"]
    elif height:
        cmd += ["-vf", f"scale=-2:{height}"]
    cmd += ["-c:a", "aac", str(path_out)]
    subprocess.run(cmd, check=True, timeout=timeout_sec)
    return output_path
