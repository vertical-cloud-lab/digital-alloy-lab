"""Scan vectors drawn on the plate: the process worker's scan program when it is there, else a labelled placeholder.

The video draws every vector at the time the laser would mark it: vectors in program order, each marked at its own speed,
with jumps between them at JUMP_MM_S plus a fixed delay. `program()` returns

    dict(source=str, placeholder=bool,
         tracks=[(x0, y0, x1, y1, v_mm_s, p_w), ...],            # FT-0's single-track screening layer
         coupons=dict(layer_um, n_layers, boxes=[(x0, y0, x1, y1), ...], layer(k) -> [(x0, y0, x1, y1, v), ...]))

and `timeline(vectors)` the start and end time (s) of each vector within its layer.
"""
from __future__ import annotations

import glob
import json
import math
import os

import numpy as np

JUMP_MM_S = 2500.0          # galvo jump speed (estimate)
DELAY_S = 0.0003            # laser on/off and jump delays per vector (estimate)
PROCESS = os.environ.get("FT_PROCESS", "/tmp/ft-process")


def timeline(vecs):
    t, out, last = 0.0, [], None
    for (x0, y0, x1, y1, v, *_) in vecs:
        if last is not None:
            t += math.hypot(x0 - last[0], y0 - last[1]) / JUMP_MM_S + DELAY_S
        t1 = t + math.hypot(x1 - x0, y1 - y0) / max(v, 1e-6)
        out.append((t, t1))
        t, last = t1, (x1, y1)
    return out


# ------------------------------------------------------------------------------------------------ placeholder
def _hatch_box(x0, y0, x1, y1, ang_deg, h, v):
    """Hatch lines of a rectangle at angle ang, spacing h, alternating direction (meander), clipped to the rectangle."""
    a = math.radians(ang_deg)
    d = np.array([math.cos(a), math.sin(a)])
    n = np.array([-d[1], d[0]])
    c = np.array([(x0 + x1) / 2, (y0 + y1) / 2])
    R = math.hypot(x1 - x0, y1 - y0) / 2
    out = []
    k = 0
    for s in np.arange(-R, R + 1e-9, h):
        p = c + n * s
        # clip the line p + t d to the box
        t0, t1 = -1e9, 1e9
        ok = True
        for i, (lo, hi) in enumerate(((x0, x1), (y0, y1))):
            if abs(d[i]) < 1e-12:
                if not lo <= p[i] <= hi:
                    ok = False
                continue
            ta, tb = (lo - p[i]) / d[i], (hi - p[i]) / d[i]
            t0, t1 = max(t0, min(ta, tb)), min(t1, max(ta, tb))
        if not ok or t1 - t0 < 1e-6:
            continue
        a_, b_ = p + d * t0, p + d * t1
        if k % 2:
            a_, b_ = b_, a_
        out.append((a_[0], a_[1], b_[0], b_[1], v))
        k += 1
    return out


def placeholder():
    # FT-0: 25 tracks of 9 mm (Bosio et al. 2019's screening: 25 power-speed pairs on one 50 um layer), 1 mm apart, along Y
    speeds = (200.0, 500.0, 800.0, 1100.0, 1400.0)
    powers = (150.0, 200.0, 250.0, 300.0, 350.0)
    tracks = []
    for i in range(25):
        x = -12.0 + i
        tracks.append((x, -4.5, x, 4.5, speeds[i % 5], powers[i // 5]))
    boxes = [(-11.5, -11.5, -1.5, -1.5), (1.5, -11.5, 11.5, -1.5), (-11.5, 1.5, -1.5, 11.5), (1.5, 1.5, 11.5, 11.5)]

    def layer(k, boxes=boxes):
        vecs = []
        ang = (67.0 * k) % 180.0
        for (x0, y0, x1, y1) in boxes:
            vecs += [(x0, y0, x1, y0, 1000.0), (x1, y0, x1, y1, 1000.0), (x1, y1, x0, y1, 1000.0), (x0, y1, x0, y0, 1000.0)]
            vecs += _hatch_box(x0 + 0.05, y0 + 0.05, x1 - 0.05, y1 - 0.05, ang, 0.1, 1000.0)
        return vecs
    return dict(source="placeholder hatch generator in video/scan.py (the process worker's scan program was not merged yet)",
                placeholder=True, tracks=tracks,
                coupons=dict(layer_um=30.0, n_layers=333, boxes=boxes, layer=layer, hatch_mm=0.1, v_mm_s=1000.0,
                             rotate_deg=67.0))


def _find_program():
    for pat in ("scan*/**/*.json", "**/scan_program*.json", "**/scan*.npz"):
        hits = sorted(glob.glob(os.path.join(PROCESS, pat), recursive=True))
        if hits:
            return hits[0]
    return None


def program():
    path = os.environ.get("FT_SCAN_PROGRAM") or None
    if path and os.path.exists(path):
        return load(path)
    return placeholder()


def load(path):
    """The process worker's program (format agreed when it lands); falls back to the placeholder for missing parts."""
    base = placeholder()
    if path.endswith(".json"):
        d = json.load(open(path))
    else:
        d = dict(np.load(path, allow_pickle=True))
    out = dict(base, source=f"{os.path.basename(path)} (process worker's scan program)", placeholder=False)
    if "tracks" in d:
        out["tracks"] = [tuple(map(float, t)) for t in d["tracks"]]
    return out
