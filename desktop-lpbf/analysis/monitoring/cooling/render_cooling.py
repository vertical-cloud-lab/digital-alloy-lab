"""Render the cooling parts as drawn (cad/monitoring_cooling.py; monitoring/cooling.md) -> analysis/out/monitoring/cooling/cooling_parts.png

Uses the mechanics renderer's scene() (analysis/monitoring/mech/render_parts.py): monitoring parts in colour, the rest grey, the
guard's panels and the bridge posts hidden; the cooling parts are drawn in a highlight colour.
Run:  /tmp/heavy 3 xvfb-run -a -s "-screen 0 1920x1080x24" /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/cooling/render_cooling.py
"""
from __future__ import annotations

import pathlib
import sys

from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "mech"))
import render_parts as RP  # noqa: E402

OUT = RP.ROOT / "analysis" / "out" / "monitoring" / "cooling"
COOL = ("light trap", "Guard inlet filter", "Hood duct", "Side camera hood", "Hood fan", "Guard exhaust", "G-10", "PB2 vent fan",
        "LP camera's Pi")


def recolour(p):
    if any(k in p.name for k in COOL):
        if "G-10" in p.name:
            return RP.hex2rgb("#e0a526")
        if "fan" in p.name.lower():
            return RP.hex2rgb("#2b6cd2")
        if "light trap" in p.name:
            return RP.hex2rgb("#3a3f46")
        return RP.hex2rgb("#7fb3d5")
    return None


def main():
    parts = RP.M.build(include_tray=True, module="M50", monitoring=True)
    img = RP.scene(parts, [(-900, 820, 700), (-80, 40, 110), (0, 0, 1)], box=(-430, 330, -300, 270, -175, 380),
                   keep=lambda p: p.module == "process" or any(k in p.name for k in COOL), recolour=recolour,
                   title="Cooling, seen from the back left: inlet trap and filter (left), hood duct over the side camera, "
                         "exhaust trap and fans (right), LP camera's Pi on the bridge. Guard panels hidden.")
    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.fromarray(img).convert("RGB")
    path = OUT / "cooling_parts.png"
    im.quantize(colors=200, method=Image.Quantize.MEDIANCUT).save(path, optimize=True)
    if path.stat().st_size > 400_000:
        im.resize((im.width * 3 // 4, im.height * 3 // 4), Image.LANCZOS).quantize(colors=160).save(path, optimize=True)
    print(path, path.stat().st_size // 1024, "kB")


if __name__ == "__main__":
    main()
