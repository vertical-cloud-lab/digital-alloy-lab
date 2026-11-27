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


def timeline(vecs, timing=None, start=(0.0, 0.0)):
    """(start, end) of each vector within its layer, s. With the program's `timing` (scanprog.DEFAULT_TIMING keys) by the
    RTC5 rules of control/ftctl/scanprog.layer_time: 10 us ticks; a jump at v_jump with its variable jump delay before
    every polyline (a run of vectors that start where the last ended, at one speed), a polygon delay between the vectors
    of a run, a mark delay after it. Without it, the old estimate (JUMP_MM_S, DELAY_S)."""
    if timing is not None:
        tm = timing

        def ticks(x):
            return math.ceil(x / tm["tick"] - 1e-9) * tm["tick"]
        t, out, pos, last = 0.0, [], np.asarray(start, float), None
        for (x0, y0, x1, y1, v, *_) in vecs:
            cont = last is not None and math.hypot(x0 - last[0], y0 - last[1]) <= 1e-3 and v == last[2]
            if cont:
                t += tm["polygon_delay"]
            else:
                if last is not None:
                    t += tm["mark_delay"]
                gap = math.hypot(x0 - pos[0], y0 - pos[1])
                if gap > 1e-3:
                    jd = tm["jump_delay"] if gap >= tm["jump_limit"] else (
                        tm["jump_delay_min"] + (tm["jump_delay"] - tm["jump_delay_min"]) * gap / tm["jump_limit"])
                    t += ticks(gap / tm["v_jump"]) + ticks(jd)
            t1 = t + ticks(math.hypot(x1 - x0, y1 - y0) / max(v, 1e-6))
            out.append((t, t1))
            t, last, pos = t1, (x1, y1, v), np.array([x1, y1])
        return out
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


FT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKS_NPZ = os.path.join(FT, "process", "out", "rung2_single_tracks.npz")
BUILD_NPZ = os.path.join(FT, "process", "out", "build_first_coupons_15mm.npz")


def program():
    """The process worker's programs (process/README.md), read with control/ftctl/scanprog.load_npz: chapter 3's tracks
    from rung2_single_tracks.npz (ladder rung 2: 25 tracks of 9 mm, 25 power-speed pairs, on a 50 um layer), chapter 5's
    layers from build_first_coupons_15mm.npz (500 layers of 30 um). Segments are x0 y0 x1 y1 in mm in the plate frame
    (ft_model's: origin at the substrate top centre, +X recoat, +Y back); the lens axis offset does not change it. The
    placeholder hatch generator is used only when the files are missing."""
    if not (os.path.exists(TRACKS_NPZ) and os.path.exists(BUILD_NPZ)):
        return placeholder()
    import sys
    sys.path.insert(0, os.path.join(FT, "control", "ftctl"))
    import scanprog as SP
    tp = SP.load_npz(TRACKS_NPZ)
    L = tp.layer(0)
    tracks = [(float(a), float(b), float(c), float(d), float(v), float(pw))
              for (a, b, c, d), pw, v in zip(L.segs, L.power_W, L.speed_mm_s)]
    bp = SP.load_npz(BUILD_NPZ)
    parts = bp.meta["parts"]
    boxes = [(q["cx"] - q["sx"] / 2, q["cy"] - q["sy"] / 2, q["cx"] + q["sx"] / 2, q["cy"] + q["sy"] / 2) for q in parts]

    def layer(k, bp=bp):
        Lk = bp.layer(k)
        return [(float(a), float(b), float(c), float(d), float(v)) for (a, b, c, d), v in zip(Lk.segs, Lk.speed_mm_s)]
    ps = bp.meta["psets"]
    return dict(source=f"process/out/{os.path.basename(TRACKS_NPZ)} and {os.path.basename(BUILD_NPZ)} (the process "
                       f"worker's scan programs)",
                placeholder=False, tracks=tracks, tracks_timing=tp.timing(),
                tracks_file=os.path.basename(TRACKS_NPZ),
                coupons=dict(layer_um=bp.layer_mm * 1000.0, n_layers=bp.n_layers, boxes=boxes, parts=parts, psets=ps,
                             layer=layer, timing=bp.timing(), file=os.path.basename(BUILD_NPZ),
                             height_mm=bp.n_layers * bp.layer_mm))


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
