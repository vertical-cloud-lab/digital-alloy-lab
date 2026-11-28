"""Stills of the scale figure (render_scale.person): its poses, and before against after.

  cad/img/sequence/person-poses.png         front, three-quarter and side views of "stand" and "reach", a bent-over
                                            pose, and the head close up
  cad/img/sequence/person-before-after.png  with --before: the 2026-11-23 lofted figure against this one, same views

Run (headless):
  git show f9ba610:desktop-lpbf/cad/render_scale.py > /tmp/rs_2026_11_23.py      # the lofted figure, for --before
  xvfb-run -a -s "-screen 0 1920x1080x24" python desktop-lpbf/cad/human/render_person.py [--before /tmp/rs_2026_11_23.py]
"""
from __future__ import annotations

import argparse
import importlib.util
import math
import pathlib
import sys

import numpy as np
import pyvista as pv
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import render_scale as RS  # noqa: E402

pv.OFF_SCREEN = True
OUT = HERE.parent / "img" / "sequence"
MAT = dict(smooth_shading=True, specular=0.12, specular_power=10, ambient=0.25, diffuse=0.8)     # render_low.MAT
INK = (29, 39, 51)


def rgb(h):
    return tuple(int(h[k:k + 2], 16) / 255 for k in (1, 3, 5))


def panel(pieces, az, el=6.0, focal=(0.0, 0.0, 900.0), dist=3500.0, size=(420, 560), floor=True):
    """One view of [(mesh, colour)] as an image array, lit and shaded like the build animation (render_low.Scene)."""
    pl = pv.Plotter(off_screen=True, window_size=size, lighting="three lights")
    pl.set_background("#f7f9fb", top="#dfe6ee")
    for m, col in pieces:
        pl.add_mesh(m, color=rgb(col), **MAT)
    if floor:
        pl.add_mesh(pv.Disc(center=(0, 0, 0), inner=0, outer=420, normal=(0, 0, 1), c_res=72), color=rgb("#a9aba6"), **MAT)
    a, e = math.radians(az - 90.0), math.radians(el)
    f = np.asarray(focal, float)
    pl.camera.position = tuple(f + dist * np.array([math.cos(a) * math.cos(e), math.sin(a) * math.cos(e), math.sin(e)]))
    pl.camera.focal_point = tuple(f)
    pl.camera.up = (0, 0, 1)
    pl.camera.view_angle = 30
    pl.enable_anti_aliasing("ssaa")
    img = pl.screenshot(return_img=True)
    pl.close()
    return Image.fromarray(img)


def font(size):
    for name in ("DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def row(images, title, pad=12, title_h=34):
    w = sum(i.width for i in images)
    h = max(i.height for i in images)
    im = Image.new("RGB", (w, h + title_h), "white")
    ImageDraw.Draw(im).text((pad, 8), title, fill=INK, font=font(17))
    x = 0
    for i in images:
        im.paste(i, (x, title_h))
        x += i.width
    return im


def stack(rows, gap=10, vertical=True):
    if vertical:
        w = max(r.width for r in rows)
        im = Image.new("RGB", (w, sum(r.height for r in rows) + gap * (len(rows) - 1)), "white")
        y = 0
        for r in rows:
            im.paste(r, (0, y))
            y += r.height + gap
        return im
    h = max(r.height for r in rows)
    im = Image.new("RGB", (sum(r.width for r in rows) + gap * (len(rows) - 1), h), "white")
    x = 0
    for k, r in enumerate(rows):
        im.paste(r, (x, 0))
        if k:
            ImageDraw.Draw(im).line([(x - gap // 2, 0), (x - gap // 2, h)], fill=(190, 190, 190), width=2)
        x += r.width + gap
    return im


def three(pieces):
    return [panel(pieces, az) for az in (0, 35, 90)]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", help="a copy of render_scale.py whose person() is the earlier figure")
    a = ap.parse_args(argv)
    OUT.mkdir(parents=True, exist_ok=True)
    now = RS.person()
    # poses
    head = [panel(now, az, el=2.0, focal=(0, -20, 1625), dist=820, size=(420, 420), floor=False) for az in (0, 40, 90)]
    rows = [row(three(now), 'pose="stand": arms hanging, elbows and fingers slightly bent, ankles 260 mm apart'),
            row(three(RS.person(pose="reach")), 'pose="reach": both hands forward at about waist height'),
            row(three(RS.person(bend=30, head_down=15, arm_fwd=35, elbow=25)),
                "bend=30, head_down=15, arm_fwd=35, elbow=25: leaning over a bench"),
            row(head, "Head: MakeHuman's base mesh, its short02 hair, low-poly eyes and eyebrow001, in flat colours")]
    out = stack(rows)
    out.save(OUT / "person-poses.png")
    print("wrote", OUT / "person-poses.png", out.size)
    if a.before:
        spec = importlib.util.spec_from_file_location("rs_before", a.before)
        old = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(old)
        before = row(three(old.person()), "Before (2026-11-23): lofted from ellipses and tubes")
        after = row(three(now), "Now (2026-11-25): MakeHuman's CC0 body, clothes and rig, posed")
        out = stack([before, after], gap=14, vertical=False)
        out.save(OUT / "person-before-after.png")
        print("wrote", OUT / "person-before-after.png", out.size)


if __name__ == "__main__":
    main(sys.argv[1:])
