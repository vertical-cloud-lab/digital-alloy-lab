"""A few stills of the rendered assembly chapters for the write-up (issue #260, round 7): picks frames by step id and
sub-caption from /tmp/robotbuild/frames/<chapter>/meta.jsonl, adds the caption and the status as a strip under the frame
(the video's compositor draws the real panels), and saves PNGs under 400 kB to analysis/out/assembly/.

    /tmp/venv/bin/python desktop-lpbf/analysis/assembly/stills.py
"""
from __future__ import annotations

import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

FR = pathlib.Path("/tmp/robotbuild/frames")
OUT = pathlib.Path(__file__).resolve().parent.parent / "out" / "assembly"
# (chapter, step, a word the frame's sub must contain or "", which matching frame: 0.0 first .. 1.0 last, output name)
WANT = [
    ("40-assembly-module", "M03", "pick at the parts table", 0.6, "r7_pick_table"),
    ("40-assembly-module", "M12", "", 0.55, "r7_ring_loader"),
    ("40-assembly-module", "M17", "", 0.6, "r7_spigot_mandrel"),
    ("40-assembly-module", "M20", "runs down", 0.5, "r7_screw_gland"),
    ("40-assembly-module", "M05", "drives", 0.5, "r7_mir_drive"),
    ("41-assembly-chamber", "F10b", "", 0.6, "r7_liner_wand"),
    ("41-assembly-chamber", "F29", "", 0.5, "r7_lid_cord_roller"),
    ("41-assembly-chamber", "F05b", "hoist", 0.5, "r7_hoist_carry"),
    ("41-assembly-chamber", "F48b", "", 0.6, "r7_ring_pad"),
]
COL = {"pass": (42, 157, 143), "fail": (209, 73, 91), "redesign": (233, 162, 59), "person": (230, 126, 34)}


def pick(chapter, step, word, at):
    d = FR / chapter
    if not (d / "meta.jsonl").exists():
        return None, None
    rows = [json.loads(x) for x in (d / "meta.jsonl").read_text().splitlines() if x.strip()]
    hits = [k for k, r in enumerate(rows) if r.get("step") == step and (not word or word in (r.get("sub") or ""))]
    if not hits:
        return None, None
    k = hits[min(len(hits) - 1, int(at * len(hits)))]
    return d / f"{k:05d}.png", rows[k]


def main():
    font = None
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf"):
        if pathlib.Path(f).exists():
            font = ImageFont.truetype(f, 15)
    font = font or ImageFont.load_default()
    made = []
    for ch, step, word, at, name in WANT:
        f, meta = pick(ch, step, word, at)
        if f is None or not f.exists():
            print("no frame for", ch, step, word)
            continue
        im = Image.open(f).convert("RGB").resize((960, 540))
        strip = Image.new("RGB", (960, 58), (246, 247, 249))
        dr = ImageDraw.Draw(strip)
        st = meta.get("status") or ""
        dr.rectangle((8, 10, 92, 32), fill=COL.get(st, (120, 120, 120)))
        dr.text((14, 13), f"{step} {st}"[:13], fill=(255, 255, 255), font=font)
        dr.text((102, 6), (meta.get("caption") or "")[:105], fill=(29, 39, 51), font=font)
        dr.text((102, 30), (meta.get("sub") or "")[:115], fill=(70, 83, 95), font=font)
        out = Image.new("RGB", (960, 598))
        out.paste(im, (0, 0))
        out.paste(strip, (0, 540))
        p = OUT / f"{name}.png"
        out.quantize(colors=200, method=Image.Quantize.MEDIANCUT).save(p, optimize=True)
        made.append((p.name, round(p.stat().st_size / 1000)))
    print(made)


if __name__ == "__main__":
    main()
