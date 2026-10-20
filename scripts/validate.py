#!/usr/bin/env python3
"""Validate this v2 atlas and its preview links; no visual-semantic claims."""
import hashlib
import json
import statistics
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]


def require(condition, message):
    if not condition:
        raise ValueError(message)


class LocalLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"src", "href"} and value and not value.startswith(("https:", "http:", "#", "data:")):
                self.paths.append(value)


def validate():
    metadata = json.loads((ROOT / "pet.json").read_text(encoding="utf-8"))
    require(metadata["schema_version"] == 2, "Only the v2 format is supported")
    require([row["frames"] for row in metadata["rows"]] == COUNTS, "Wrong row/frame contract")
    require([metadata[k] for k in ["width", "height", "cell_width", "cell_height", "columns"]] == [1536, 2288, 192, 208, 8], "Wrong atlas metadata geometry")
    require(metadata["look_degrees"] == [i * 22.5 for i in range(16)], "Wrong clockwise direction order")
    for row in metadata["rows"]:
        require(len(row["durations_ms"]) == row["frames"], "Missing frame duration")
        require(all(isinstance(ms, int) and ms > 0 for ms in row["durations_ms"]), "Invalid duration")
    path = ROOT / metadata["atlas"]
    require(path.resolve().is_relative_to(ROOT), "Atlas must be inside the project")
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    require(digest == metadata["sha256"], "Atlas checksum differs from pet.json")
    with Image.open(path) as image:
        require(image.format == "PNG" and image.mode == "RGBA", "Expected an RGBA PNG")
        require(image.size == (1536, 2288), "Expected a 1536 x 2288 v2 atlas")
        atlas = image.copy()
    require(len(raw) <= 20 * 1024 * 1024, "Atlas exceeds the 20 MiB format limit")
    bounds = {}
    for row, count in enumerate(COUNTS):
        for col in range(8):
            cell = atlas.crop((192 * col, 208 * row, 192 * (col + 1), 208 * (row + 1)))
            alpha = cell.getchannel("A")
            occupied = alpha.getbbox() is not None
            require(occupied == (col < count), f"Wrong occupancy at row {row}, cell {col}")
            if occupied:
                bbox = alpha.point(lambda value: 255 if value > 16 else 0).getbbox()
                require(bbox is not None, f"No visible artwork at row {row}, cell {col}")
                require(bbox[0] > 0 and bbox[1] > 0 and bbox[2] < 192 and bbox[3] < 208,
                        f"Artwork touches the boundary at row {row}, cell {col}")
                bounds[row, col] = bbox
    pixels = atlas.tobytes()
    require(all(pixels[i + 3] != 0 or pixels[i:i + 3] == b'\x00\x00\x00'
                for i in range(0, len(pixels), 4)), "Nonzero hidden RGB under transparency")
    idle_bottom = statistics.median(bounds[0, col][3] for col in range(6))
    jump_bottoms = [bounds[4, col][3] for col in range(5)]
    lift = max(jump_bottoms) - min(jump_bottoms)
    landing_delta = abs(jump_bottoms[-1] - idle_bottom)
    require(lift >= 8, "Jump must visibly lift at least 8 pixels")
    require(landing_delta <= 12, "Jump landing differs from idle baseline by more than 12 pixels")
    links = LocalLinks()
    links.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    links.paths.append("assets/spritesheet.png")
    for link in links.paths:
        require((ROOT / link).is_file(), f"Missing preview resource: {link}")
    return {"ok": True, "sha256": digest, "bytes": len(raw), "required_frames": 73,
            "unused_transparent_cells": 15, "visible_alpha_threshold": 16, "jump_lift_pixels": lift,
            "landing_delta_pixels": landing_delta, "local_preview_links": len(links.paths),
            "scope": "format, checksum, geometry and file links; visual quality needs human review"}


if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
