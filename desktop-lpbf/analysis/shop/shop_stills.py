"""Stills for robot-shop.md round 7 from the rendered shop chapters (/tmp/robotbuild/frames): the frame in the middle of
the first run of frames whose caption starts with each key, saved at 960 x 540 under 400 kB.

Run after shop_chapters.py:  /tmp/venv/bin/python desktop-lpbf/analysis/shop/shop_stills.py
"""
from __future__ import annotations

import io
import json
import pathlib

from PIL import Image

FR = pathlib.Path("/tmp/robotbuild/frames")
OUT = pathlib.Path(__file__).resolve().parent.parent / "out" / "shop"
PICKS = [
    ("30-machining-chamber", "A person loads the 30 kg blank", 0.80, "r7_person_loads_blank.png"),
    ("30-machining-chamber", "Arm A drives the four edge clamps", 0.35, "r7_arm_clamps.png"),
    ("30-machining-chamber", "F-S1 on the VF-4", 0.55, "r7_cutting_fs1.png"),
    ("30-machining-chamber", "The person lifts the freed core", 0.55, "r7_person_core.png"),
    ("30-machining-chamber", "F-S3 on the HRT210", 0.6, "r7_fs3_rotary.png"),
    ("30-machining-chamber", "Arm A sets the floor plate", 0.6, "r7_vgp20_floor_plate.png"),
    ("31-machining-parts", "Arm A loads a bar slug", 0.55, "r7_lathe_top_down.png"),
    ("31-machining-parts", "Arm B lays a bar", 0.5, "r7_saw.png"),
    ("32-finishing", "Arm A deburrs", 0.5, "r7_deburr.png"),
    ("32-finishing", "Arm A kits the floor plate", 0.7, "r7_kit_long_table.png"),
    ("20-receiving", "Three crates over two arms", 0.6, "r7_pallet_jack.png"),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for ch, key, frac, name in PICKS:
        d = FR / ch
        if not (d / "meta.jsonl").exists():
            continue
        meta = [json.loads(line) for line in open(d / "meta.jsonl")]
        idx = [i for i, m in enumerate(meta) if m.get("caption", "").startswith(key)]
        if not idx:
            continue
        run = [idx[0]]
        for i in idx[1:]:
            if i != run[-1] + 1:
                break
            run.append(i)
        k = run[min(len(run) - 1, int(frac * len(run)))]
        p = d / f"{k:05d}.png"
        if not p.exists():
            continue
        im = Image.open(p).convert("RGB").resize((960, 540), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, "PNG", optimize=True)
        for colors in (256, 128, 64):
            if buf.tell() < 400_000:
                break
            buf = io.BytesIO()
            im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT).save(buf, "PNG", optimize=True)
        (OUT / name).write_bytes(buf.getvalue())
        print(name, ch, k, f"{buf.tell() / 1000:.0f} kB")


if __name__ == "__main__":
    main()
