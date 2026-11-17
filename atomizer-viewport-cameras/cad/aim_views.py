#!/usr/bin/env python3
"""What the front unit's HQ Camera (16 mm M12 lens) would see through the port, as designed (looking along the port's
axis) and tilted at the point where the stream lands, in one stack set-up (VIZ3D_STACK: training, oct6, measured).

The camera sits where the Onshape model puts the HQ's lens, 15 mm left of the port's axis, its front 11 mm outside the
glass. The port is drawn as its Ø63 glass only (a dark ring 33-41 mm out from the chamber face); the bore behind the
glass isn't known. The dashed box is the 1332 x 990 mode's crop (126 fps on the current driver, about 200 fps at a
750 MHz link). Depth of field isn't drawn: at F1.9 and 240 mm only about 3-5 mm of depth is sharp.

    for s in training oct6 measured; do VIZ3D_STACK=$s xvfb-run -a -s "-screen 0 1920x1080x24" python aim_views.py; done
    python aim_views.py --sheet          # the six tiles -> ../renders/front_hq_aim.png
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

import units as U
import model as M

OUT = U.HERE.parent / "renders"
TMP = OUT / "aim"
SIZE = (640, 480)                    # 4:3, the HQ sensor's shape
HQ_VFOV = 2 * math.degrees(math.atan(4.712 / 2 / 16.0))       # 16 mm lens on the full 6.287 x 4.712 mm sensor
CROP = (2664 / 4056, 1980 / 3040)    # the 1332 x 990 mode's share of the sensor, centred
N = U.unit(M.VIEWPORT_N)             # out along the port's axis
O = M.VIEWPORT + N * (M.CH_Y[0] - M.VIEWPORT[1]) / N[1]      # the axis at the chamber face
X = U.unit(np.cross([0, 0, 1], N))   # the operator's right
Y = np.cross(N, X)                   # up, square to the axis


def world(x, y, z):
    return O + X * x + Y * y + N * z


HQ = world(-15.0, 0.0, 52.0)         # the HQ lens's front, from the Onshape export (lens_start 4 + lens 20, cam_gap 1)


def ring(r_in, r_out, z0, z1):
    import pyvista as pv
    t = pv.CylinderStructured(radius=np.linspace(r_in, r_out, 2), height=z1 - z0, center=world(0, 0, (z0 + z1) / 2),
                              direction=N, theta_resolution=96, z_resolution=2)
    return t.extract_surface(algorithm="dataset_surface")


def views() -> None:
    import pyvista as pv
    import scene as S
    from PIL import Image, ImageDraw

    name = os.environ.get("VIZ3D_STACK", "").strip() or "measured"
    target = M.IMPACT
    fwd_t = U.unit(target - HQ)
    tilt = math.degrees(math.atan2(fwd_t @ Y, -(fwd_t @ N)))
    pan = math.degrees(math.atan2(fwd_t @ X, -(fwd_t @ N)))
    dist = float(np.linalg.norm(target - HQ))
    TMP.mkdir(parents=True, exist_ok=True)
    info = {"setup": name, "lands_on": M.IMPACT_ON, "landing_z": round(float(target[2]), 1),
            "tilt_deg": round(tilt, 1), "pan_deg": round(pan, 1), "distance_mm": round(dist)}
    for view, fwd in (("axis", -N), ("tilted", fwd_t)):
        sc = S.Scene(f"aim_{name}_{view}", "", size=SIZE, gif=False, mp4=False)
        S.load_machine(sc, hide=U.HIDE_IN_MODEL)
        sc.add("port_glass_edge", ring(31.5, 70.0, 33.0, 41.0), (0.12, 0.12, 0.13), "port")
        sc.add("stream", pv.Line((0, 0, M.NOZZLE_EXIT_Z), target).tube(radius=1.4, n_sides=16), S.MELT, "stream",
               ambient=0.9, diffuse=0.2, specular=0.0)
        up = U.unit(Y - fwd * (Y @ fwd))
        sc.cam = [tuple(HQ), tuple(HQ + fwd * 200.0), tuple(up)]
        sc.view_angle = HQ_VFOV
        img = sc.snap().convert("RGB")
        sc.pl.close()
        d = ImageDraw.Draw(img)
        W, H = img.size
        cw, ch = W * CROP[0], H * CROP[1]
        x0, y0, x1, y1 = (W - cw) / 2, (H - ch) / 2, (W + cw) / 2, (H + ch) / 2
        for a, b in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
            n = 24
            for k in range(0, n, 2):
                p = [a[i] + (b[i] - a[i]) * k / n for i in (0, 1)]
                q = [a[i] + (b[i] - a[i]) * (k + 1) / n for i in (0, 1)]
                d.line([tuple(p), tuple(q)], fill=(220, 40, 40), width=2)
        img.save(TMP / f"{name}_{view}.png")
        print("wrote", TMP / f"{name}_{view}.png")
    (TMP / f"{name}.json").write_text(json.dumps(info, indent=1) + "\n")
    print(json.dumps(info))


def sheet() -> None:
    from PIL import Image, ImageDraw, ImageFont
    rows = ("training", "oct6", "measured")
    what = {"training": "training set-up (inferred, 7 Oct)", "oct6": "6 Oct failure",
            "measured": "measured, 8 Oct: as the lab runs it now"}
    surface = {"plate": "the plate", "upper": "the upper sonotrode"}
    W, H = SIZE
    top, left, gap = 46, 0, 6
    cap = 30
    sheet = Image.new("RGB", (2 * W + gap, top + len(rows) * (H + cap + gap)), "white")
    d = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype("DejaVuSans.ttf", 17)
        fb = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
    except OSError:
        f = fb = ImageFont.load_default()
    d.text((10, 12), "HQ Camera + 16 mm lens, as designed (along the port axis)", font=fb, fill=(15, 15, 20))
    d.text((W + gap + 10, 12), "the same camera, tilted at where the stream lands", font=fb, fill=(15, 15, 20))
    for i, s in enumerate(rows):
        info = json.loads((TMP / f"{s}.json").read_text())
        y = top + i * (H + cap + gap)
        for j, v in enumerate(("axis", "tilted")):
            sheet.paste(Image.open(TMP / f"{s}_{v}.png"), (j * (W + gap), y))
        t = info["tilt_deg"]
        d.text((10, y + H + 4), f"{what[s]}: lands on {surface[info['lands_on']]}", font=f, fill=(15, 15, 20))
        aim = "on the axis" if abs(t) < 1 else f"tilted {abs(t):.0f}° {'down' if t < 0 else 'up'}"
        d.text((W + gap + 10, y + H + 4), f"{aim}, {abs(info['pan_deg']):.0f}° left; "
               f"{info['distance_mm']} mm to the landing point", font=f, fill=(15, 15, 20))
    sheet.save(OUT / "front_hq_aim.png", optimize=True)
    print("wrote", OUT / "front_hq_aim.png")


if __name__ == "__main__":
    sheet() if "--sheet" in sys.argv else views()
