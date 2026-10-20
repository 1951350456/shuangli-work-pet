#!/usr/bin/env python3
"""Export previews from the validated atlas without altering pet artwork."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
from validate import ROOT, validate


def save_gif(frames, durations, path):
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=durations,
                   loop=0, disposal=2, optimize=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "build")
    parser.add_argument("--mp4", action="store_true", help="Require FFmpeg on PATH and encode MP4 too")
    args = parser.parse_args()
    validate()
    out = args.output.resolve()
    if out == ROOT or out.is_relative_to(ROOT / "assets"):
        raise ValueError("Render into a separate directory; source assets are immutable inputs")
    out.mkdir(parents=True, exist_ok=True)
    metadata = json.loads((ROOT / "pet.json").read_text(encoding="utf-8"))
    atlas = Image.open(ROOT / metadata["atlas"]).convert("RGBA")
    states, all_frames, all_durations = {}, [], []
    for row, spec in enumerate(metadata["rows"]):
        frames = [atlas.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))
                  for col in range(spec["frames"])]
        states[spec["name"]] = frames
        save_gif(frames, spec["durations_ms"], out / (spec["name"] + ".gif"))
        if row < 9:
            for frame, duration in zip(frames, spec["durations_ms"], strict=True):
                labeled = Image.new("RGBA", (192, 240), "#f2effb")
                labeled.alpha_composite(frame, (0, 24))
                ImageDraw.Draw(labeled).text((8, 7), spec["name"], fill="#3f315f")
                all_frames.append(labeled)
                all_durations.append(duration)
    save_gif(all_frames, all_durations, out / "preview.gif")
    save_gif(states["look-a"] + states["look-b"], [220] * 16, out / "look-loop.gif")
    transition = states["idle"] + states["jumping"] + states["idle"]
    timing = metadata["rows"][0]["durations_ms"] + metadata["rows"][4]["durations_ms"] + metadata["rows"][0]["durations_ms"]
    save_gif(transition, timing, out / "idle-jump-idle.gif")
    if args.mp4:
        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg is None:
            raise FileNotFoundError("--mp4 requires FFmpeg on PATH")
        subprocess.run([ffmpeg, "-y", "-i", str(out / "preview.gif"), "-c:v", "libx264",
                        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out / "preview.mp4")], check=True)
    print(json.dumps({"ok": True, "output": str(out), "artwork_unchanged": True}))


if __name__ == "__main__":
    main()
