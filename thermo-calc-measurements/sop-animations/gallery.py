"""A contact sheet of every instrument model the SOP videos use (#262, PR #263).

    xvfb-run -a python gallery.py            # -> out/gallery.jpg (and out/gallery/<key>.png)

Each tile: the model alone on a bench at a three-quarter view, its maker and model, its published W x D x H, and,
where it was registered to reference frames, the RMS pixel error after the fit (refs/<key>/fit.json).
"""
from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("PREVIEW", "")
import numpy as np
from PIL import Image, ImageDraw

import stage as S

HERE = Path(__file__).resolve().parent
TILE = (640, 400)
REUSED = ["mount_press", "polisher", "fumehood", "vhx", "sem", "furnace", "quench_tank", "hardness"]


def keys() -> list[str]:
    out = []
    for f in sorted(HERE.glob("models_*.py")):
        mod = importlib.import_module(f.stem)
        for k, build in getattr(mod, "REGISTRY", {}).items():
            out.append(k)
    return out + [k for k in REUSED if k not in out]


def still(key: str) -> Image.Image | None:
    try:
        inst, ents = S.get(key)
    except Exception as e:                                  # noqa: BLE001
        print(f"{key}: {type(e).__name__}: {e}", flush=True)
        return None
    sc = S.SOPScene(f"gallery_{key}", "", size=(TILE[0] * 2, TILE[1] * 2), gif=False, mp4=False)
    x0, x1, y0, y1, z0, z1 = inst.bbox()
    w = max(x1 - x0, 300.0)
    floor = getattr(inst, "floor", False) or (z1 - z0) > 1500
    S.room(sc, x0=-w - 400, x1=w + 400, bench=not floor, wall=False)
    z = 0.0 if floor else S.BENCH_H
    S.Rig(sc, inst, ents, f"{key}:", at=S.T((0, 0, z)))
    sc.cam = S.frame_cam((x0, x1, y0, y1, z0 + z, z1 + z), direction=(0.9, -1.5, 0.75), pad=0.82, look_z=0.45)
    img = Image.fromarray(sc.render_base()).resize(TILE, Image.LANCZOS)
    sc.pl.close()
    return img


def main() -> None:
    out = S.OUT / "gallery"
    out.mkdir(parents=True, exist_ok=True)
    tiles = []
    for key in keys():
        im = still(key)
        if im is None:
            continue
        im.save(out / f"{key}.png", optimize=True)
        inst, _ = S.get(key)
        fit = HERE / "refs" / key / "fit.json"
        note = "not registered"
        if fit.exists():
            v = json.loads(fit.read_text()).get("views", {})
            fitted = [x["rms_px"] for x in v.values() if not x.get("holdout")]
            held = [x["rms_px"] for x in v.values() if x.get("holdout")]
            note = f"fit to {len(fitted)} views: {np.mean(fitted):.1f} px RMS" if fitted else "registered"
            if held:
                note += f"; held out {np.mean(held):.1f} px"
        elif key in REUSED:
            note = "byu-vcl model" + (" (fitted there)" if key in ("polisher", "furnace", "vhx", "sem") else "")
        tiles.append((key, inst, im, note))
        print(key, note, flush=True)
    cols = 4
    cap = 64
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (TILE[0] * cols, (TILE[1] + cap) * rows), "white")
    d = ImageDraw.Draw(sheet)
    f1, f2 = S.font(17, bold=True), S.font(14)
    for i, (key, inst, im, note) in enumerate(tiles):
        x, y = (i % cols) * TILE[0], (i // cols) * (TILE[1] + cap)
        sheet.paste(im, (x, y))
        name = inst.model if len(inst.model) < 60 else inst.model[:57] + "..."
        d.text((x + 10, y + TILE[1] + 4), name, font=f1, fill=(20, 20, 24))
        w_, d_, h_ = inst.size
        d.text((x + 10, y + TILE[1] + 26), f"{w_:.0f} x {d_:.0f} x {h_:.0f} mm published", font=f2, fill=(70, 72, 78))
        d.text((x + 10, y + TILE[1] + 44), note, font=f2, fill=(30, 60, 140))
    dst = S.OUT / "gallery.jpg"
    sheet.save(dst, quality=85, optimize=True)
    print(dst)


if __name__ == "__main__":
    sys.exit(main())
