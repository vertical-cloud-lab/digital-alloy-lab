"""Scan program for FT-1's first coupon build on the Ø40 plate (#260).

  layout     how many 10 x 10 mm (and 5 x 5 mm) coupons fit inside the usable Ø30 (inside the M2 screw heads at r = 17.1)
  vectors    meander (or stripe) hatching at the recommended hatch, rotated 67° a layer, one contour per part, written
             for the whole build to ONE compressed file: out/build_<name>.npz (int32 um, see save_build)
  timing     exact per-layer list time with the RTC5's 10 us clock: marks, jumps, variable jump delay, mark and
             polygon delays; laser-on time from the laser on/off delays
  recoat     hopper-blade return + plate step + spread, for the Zaber X-LSM100B-E03 (lead's candidate) and the
             X-LSQ075B-E01 (the study's stage) as the comparison; build times for 5, 10 and 15 mm
  heat       layer-wise heat input for the FEA: out/heat_input.csv (and /tmp/ft-process/heat_input.csv)

Frame: mm, the CAD frame of cad/ft_model.py: origin at the centre of the substrate's top face, +X the recoat
direction, +Y to the back. The cross-flow runs along +Y (nozzle in front, exhaust behind), so parts are scanned from
+Y to -Y and each part's hatch lines step towards -Y (into the gas flow). The lens axis offset (optics.py) is applied
when the vectors are turned into RTC5 commands (rtc5_list.py), not here.

Run: python desktop-lpbf/fast-track/process/scan_program.py
"""
from __future__ import annotations

import csv
import json
import math
import pathlib
import shutil
from dataclasses import asdict, dataclass, field

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "out"
SCRATCH = pathlib.Path("/tmp/ft-process")

# --------------------------------------------------------------------------------------------------
# The plate (cad/ft_model.py MK-05: Ø39.8 x 6 mm 6061 disc, three countersunk M2 screws at r = 17.1 mm)
# --------------------------------------------------------------------------------------------------
PLATE_R = 19.9
SCREW_R = 17.1
SCREW_ANG = (90.0, 210.0, 330.0)        # ft_model.py: a = 90 + 120 k
SCREW_HEAD_R = 2.0                      # M2 countersunk head Ø3.8 (ISO 10642 dk max 3.8) + 0.1
USABLE_R = 15.0                         # the study's Ø30 build area


# --------------------------------------------------------------------------------------------------
# Parameter sets (meltpool.py chooses them; the cube set is the recommended starting point)
# --------------------------------------------------------------------------------------------------
@dataclass
class ParamSet:
    name: str
    P_hatch: float          # W
    v_hatch: float          # mm/s
    hatch: float            # mm
    P_contour: float        # W
    v_contour: float        # mm/s
    contour_offset: float   # mm, contour centre line inside the part outline (half a track width)
    hatch_offset: float     # mm, hatch region edge inside the contour centre line
    layer: float            # mm
    rot_deg: float = 67.0
    note: str = ""


# Starting sets for AlSi10Mg cubes at 200 C from meltpool.py's recommend() (out/process_window.json): 255 W at
# 1.25 m/s keeps King's number at 22 (keyhole above 30); hatch 0.10 mm keeps Tang's sum at 0.45 (0.73 if the plate
# is cold). The first build brackets it: B at the 200 C hatch limit (Tang 0.60), C 20 % slower (King 24.7).
# Contour 150 W, 0.8 m/s (pool 146 x 66 um at 200 C).
_C = dict(P_contour=150.0, v_contour=800.0, contour_offset=0.08, hatch_offset=0.06, layer=0.030)
PSETS = {
    "nominal": ParamSet("nominal", P_hatch=255.0, v_hatch=1250.0, hatch=0.10, note="recommended starting set", **_C),
    "wide": ParamSet("wide", P_hatch=255.0, v_hatch=1250.0, hatch=0.12, note="hatch at Tang 0.60 (200 C)", **_C),
    "slow": ParamSet("slow", P_hatch=255.0, v_hatch=1000.0, hatch=0.10, note="20 % slower, King 24.7", **_C),
}
CUBE_SET = PSETS["nominal"]


# --------------------------------------------------------------------------------------------------
# Scanner and laser timing (sources in the README; values to be tuned on the burn tests)
# --------------------------------------------------------------------------------------------------
@dataclass
class Timing:
    """SCANLAB hurrySCAN 25 data (scanlab.de/en/print-product/609): tracking error 0.50 ms; step response 0.90 ms
    (1 % of full scale) and 3.20 ms (10 %); marking speed 0.8 m/s and positioning speed 5.0 m/s at f = 160 mm, so
    1.27 and 7.95 m/s at f = 254.4. (The lead's interpolation between the hurrySCAN 20 and 30 gave 0.45 ms and
    7.2 m/s.) Delays from the tracking error by SCANLAB's usual rules: laser off and mark delay ~ the tracking error,
    laser on about half of it, jump delay the tracking error plus settling. Starting values: tune them with a delay
    test pattern burned on anodised Al before any powder. RTC5 units: laser delays 0.5 us a bit, scanner delays
    10 us a bit (rtc5_list.py rounds to them)."""
    tick: float = 10e-6             # s, RTC5 list clock (10 us)
    tracking_error: float = 500e-6  # s, hurrySCAN 25
    v_jump: float = 7000.0          # mm/s, jump speed in the field (below the 7.95 m/s positioning speed at f = 254.4)
    jump_delay: float = 700e-6      # s, after a long jump (>= jump_limit)
    jump_delay_min: float = 300e-6  # s, after a very short jump (RTC5 variable jump delay, set_delay_mode)
    jump_limit: float = 5.0         # mm, jumps shorter than this get a delay scaled between min and full
    mark_delay: float = 550e-6      # s, after the last mark of a polyline, before the jump (>= laser_off_delay)
    polygon_delay: float = 250e-6   # s, at each corner inside a polyline (contours)
    laser_on_delay: float = 250e-6  # s, laser on after the start of the first mark of a polyline
    laser_off_delay: float = 500e-6  # s, laser off after the end of the last mark of a polyline
    list_overhead: float = 0.05     # s, per layer: list load and start (est.)
    source: str = ("SCANLAB hurrySCAN 25 data (tracking error 0.50 ms, 7.95 m/s positioning at f = 254.4); delays "
                   "from the tracking error; tune with a delay test pattern")


@dataclass
class Stage:
    name: str
    v_max: float        # mm/s (zaber.com, read 2026-11-27 by the lead)
    accel: float        # mm/s2 (est.: Zaber default class)
    note: str = ""


X_LSM100B = Stage("Zaber X-LSM100B-E03", 104.0, 1000.0, "101.6 mm travel, 25 N continuous thrust, 250 N centred load")
X_LSQ075B = Stage("Zaber X-LSQ075B-E01", 280.0, 1000.0, "75 mm travel, body 285.9 mm (too long for the 250 mm deck)")
X_VSR20A = Stage("Zaber X-VSR20A-E01", 48.0, 200.0, "20 mm travel, 100 N continuous thrust")


@dataclass
class Recoat:
    stroke: float = 66.4            # mm, park to park (cad/README: -30.9 to +35.5)
    v_spread: float = 40.0          # mm/s, forward stroke that lays the layer (est.; powder-limited, not the stage)
    v_return: float = 1e9           # mm/s, back over the scanned layer: the stage's maximum unless set lower
    step_settle: float = 0.10       # s, after the plate step (est.)
    host_overhead: float = 0.50     # s, per layer: stage commands, list load, logging, a layer photo (est.)
    dose_extra: float = 0.0         # s, the hopper vibrator runs during the spread


def move_time(d, v, a):
    """Trapezoidal (or triangular) move time over d mm."""
    if d <= 0:
        return 0.0
    if d >= v * v / a:
        return d / v + v / a
    return 2 * math.sqrt(d / a)


def recoat_time(rc: Recoat, stage: Stage, layer_mm: float, piston: Stage = X_VSR20A):
    v_ret = min(rc.v_return, stage.v_max)
    v_spr = min(rc.v_spread, stage.v_max)
    t_ret = move_time(rc.stroke, v_ret, stage.accel)
    t_spr = move_time(rc.stroke, v_spr, stage.accel)
    t_step = move_time(layer_mm, min(5.0, piston.v_max), piston.accel) + rc.step_settle
    total = t_ret + t_spr + t_step + rc.host_overhead + rc.dose_extra
    return dict(stage=stage.name, v_return=v_ret, v_spread=v_spr, t_return=t_ret, t_spread=t_spr, t_step=t_step,
                t_overhead=rc.host_overhead, t_recoat=total)


# --------------------------------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------------------------------
def screws():
    return [(SCREW_R * math.cos(math.radians(a)), SCREW_R * math.sin(math.radians(a))) for a in SCREW_ANG]


def rect_ok(x0, x1, y0, y1, R=USABLE_R):
    """Rectangle fully inside the circle of radius R (all four corners)."""
    return max(math.hypot(x, y) for x in (x0, x1) for y in (y0, y1)) <= R + 1e-9


def pack_rows(size, gap, R=USABLE_R, steps=400):
    """Most squares of side `size` with `gap` between them inside radius R, in rows (each row centred on its own).
    Returns (count, list of (cx, cy))."""
    pitch = size + gap
    best = (0, [])
    for oy in np.linspace(-pitch / 2, pitch / 2, steps):
        cs = []
        j0 = -int(R // pitch) - 2
        for j in range(j0, -j0 + 1):
            yc = oy + j * pitch
            y0, y1 = yc - size / 2, yc + size / 2
            if max(abs(y0), abs(y1)) > R:
                continue
            xm = math.sqrt(R * R - max(y0 * y0, y1 * y1))     # half-width available to the whole row
            n = int(math.floor((2 * xm + gap) / pitch + 1e-9))
            for i in range(n):
                cs.append((-(n - 1) * pitch / 2 + i * pitch, yc))
        if len(cs) > best[0]:
            best = (len(cs), cs)
    return best


def layout_table():
    rows = []
    for size, gaps in ((10.0, (1.0, 2.0, 3.0, 4.0)), (5.0, (2.0, 2.5, 3.0, 4.0))):
        for g in gaps:
            n, cs = pack_rows(size, g)
            rows.append(dict(size_mm=size, gap_mm=g, count=n, centres=[(round(x, 2), round(y, 2)) for x, y in cs]))
    return rows


@dataclass
class Part:
    name: str
    cx: float
    cy: float
    sx: float
    sy: float
    height: float
    pset: str


def place_small(parts, size=5.0, height=10.0, pset="cube", step=0.1, R=USABLE_R, min_gap=2.0):
    """Greedily add size x size squares where they fit (inside R, >= min_gap from parts, >= 1 mm from screw heads),
    trying candidate centres from the plate centre outwards. Returns the added parts."""
    added = []
    g = np.arange(-R, R + 1e-9, step)
    cand = sorted(((x, y) for x in g for y in g), key=lambda c: (round(math.hypot(*c), 3), c[1], c[0]))
    names = iter("defghijk")
    for (x, y) in cand:
        q = Part("?", float(x), float(y), size, size, height, pset)
        if not check_layout(parts + added + [q], R, min_gap):
            q.name = next(names)
            added.append(q)
    return added


def first_build(height=10.0, small=True):
    """The recommended first coupon build: three 10 x 10 mm cubes with 2 mm gaps (two side by side, one centred below
    them), all inside r = 15 mm, plus the 5 x 5 mm cubes that still fit (place_small)."""
    parts = [
        Part("A", -6.0, 5.15, 10.0, 10.0, height, "nominal"),
        Part("B", 6.0, 5.15, 10.0, 10.0, height, "wide"),
        Part("C", 0.0, -6.9, 10.0, 10.0, height, "slow"),
    ]
    if small:
        parts += place_small(parts, height=height, pset="nominal")
    return parts


def check_layout(parts, R=USABLE_R, min_gap=2.0):
    issues = []
    for p in parts:
        x0, x1, y0, y1 = p.cx - p.sx / 2, p.cx + p.sx / 2, p.cy - p.sy / 2, p.cy + p.sy / 2
        if not rect_ok(x0, x1, y0, y1, R):
            issues.append(f"{p.name} outside r = {R}")
        for (sx, sy) in screws():
            dx = max(x0 - sx, 0, sx - x1)
            dy = max(y0 - sy, 0, sy - y1)
            if math.hypot(dx, dy) < SCREW_HEAD_R + 1.0:
                issues.append(f"{p.name} within 1 mm of a screw head")
    for i, p in enumerate(parts):
        for q in parts[i + 1:]:
            gx = max(q.cx - q.sx / 2 - (p.cx + p.sx / 2), p.cx - p.sx / 2 - (q.cx + q.sx / 2))
            gy = max(q.cy - q.sy / 2 - (p.cy + p.sy / 2), p.cy - p.sy / 2 - (q.cy + q.sy / 2))
            g = max(gx, gy)
            if g < min_gap - 1e-9:
                issues.append(f"{p.name}-{q.name} gap {g:.2f} mm")
    return issues


# --------------------------------------------------------------------------------------------------
# Vectors
# --------------------------------------------------------------------------------------------------
def hatch_rect(x0, x1, y0, y1, theta_deg, h, step_dir=(0.0, -1.0)):
    """Meander hatch of the rectangle at angle theta (line direction), spacing h. Lines step so that their
    progression has a component along step_dir (into the gas flow). Returns an (n, 4) array of segments."""
    th = math.radians(theta_deg)
    d = np.array([math.cos(th), math.sin(th)])            # line direction
    nrm = np.array([-d[1], d[0]])                          # step direction between lines
    if nrm @ np.asarray(step_dir) < 0 or (abs(nrm @ np.asarray(step_dir)) < 1e-9 and nrm[0] < 0):
        nrm = -nrm
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    corners = np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]) - (cx, cy)
    nn = corners @ nrm
    n_lo, n_hi = nn.min(), nn.max()
    span = n_hi - n_lo
    k = int(math.floor(span / h))
    offs = n_lo + (span - k * h) / 2 + np.arange(k + 1) * h   # centred in the span
    segs = []
    for i, o in enumerate(offs):
        # points p = c + o*nrm + t*d inside the rectangle: solve the t-interval
        px, py = o * nrm[0], o * nrm[1]
        tl, th_ = -1e9, 1e9
        for (p, dd, lo, hi) in ((px, d[0], x0 - cx, x1 - cx), (py, d[1], y0 - cy, y1 - cy)):
            if abs(dd) < 1e-12:
                if p < lo - 1e-12 or p > hi + 1e-12:
                    tl, th_ = 1, 0
                continue
            a, b = (lo - p) / dd, (hi - p) / dd
            tl, th_ = max(tl, min(a, b)), min(th_, max(a, b))
        if th_ - tl <= 1e-6:
            continue
        s = (cx + px + tl * d[0], cy + py + tl * d[1])
        e = (cx + px + th_ * d[0], cy + py + th_ * d[1])
        if i % 2:
            s, e = e, s
        segs.append((*s, *e))
    return np.array(segs, float).reshape(-1, 4)


def contour_rect(x0, x1, y0, y1):
    """One closed contour, counter-clockwise from the corner nearest -X-Y, as 4 chained segments."""
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]
    return np.array([(*pts[i], *pts[i + 1]) for i in range(4)], float)


def layer_vectors(parts, psets, k):
    """Segments of layer k (0-based) in scan order: parts from +Y to -Y; per part hatch then contour.
    Returns segs (n, 4) mm, kind (n,) 0 hatch / 1 contour, part index (n,)."""
    z_top = (k + 1)
    order = sorted(range(len(parts)), key=lambda i: (-parts[i].cy, parts[i].cx))
    S, K, I = [], [], []
    for i in order:
        p = parts[i]
        ps = psets[p.pset]
        if z_top * ps.layer > p.height + 1e-9:
            continue
        theta = (ps.rot_deg * k) % 180.0
        co = ps.contour_offset
        x0, x1, y0, y1 = p.cx - p.sx / 2, p.cx + p.sx / 2, p.cy - p.sy / 2, p.cy + p.sy / 2
        hx = co + ps.hatch_offset
        h = hatch_rect(x0 + hx, x1 - hx, y0 + hx, y1 - hx, theta, ps.hatch)
        c = contour_rect(x0 + co, x1 - co, y0 + co, y1 - co)
        S += [h, c]
        K += [np.zeros(len(h), np.uint8), np.ones(len(c), np.uint8)]
        I += [np.full(len(h), i, np.uint8), np.full(len(c), i, np.uint8)]
    if not S:
        return np.zeros((0, 4)), np.zeros(0, np.uint8), np.zeros(0, np.uint8)
    return np.vstack(S), np.concatenate(K), np.concatenate(I)


def n_layers(parts, psets):
    return max(int(round(p.height / psets[p.pset].layer)) for p in parts)


def build_vectors(parts, psets):
    segs, kinds, pidx, ptr = [], [], [], [0]
    for k in range(n_layers(parts, psets)):
        s, kd, ii = layer_vectors(parts, psets, k)
        segs.append(s)
        kinds.append(kd)
        pidx.append(ii)
        ptr.append(ptr[-1] + len(s))
    return np.vstack(segs), np.concatenate(kinds), np.concatenate(pidx), np.array(ptr, np.int64)


def save_build(path, parts, psets, timing, segs, kinds, pidx, ptr, meta=None):
    """One compressed NPZ for the whole build.
    seg_delta_um: int32 (n, 4), the segments x0 y0 x1 y1 in um, each column stored as differences from the row before
                  (np.cumsum along axis 0 restores them; load_build does it); kind: 0 hatch / 1 contour;
    part: index into meta["parts"]; layer_ptr: segments of layer k are rows layer_ptr[k]:layer_ptr[k+1];
    meta: JSON (frame, parts, parameter sets, scanner timing)."""
    info = dict(frame="cad/ft_model.py: mm, origin at the substrate top centre, +X recoat, +Y back (gas flows +Y)",
                parts=[asdict(p) for p in parts], psets={k: asdict(v) for k, v in psets.items()},
                timing=asdict(timing), units=dict(seg_delta_um="micrometres, delta-coded by column",
                                                  kind="0 hatch, 1 contour"), **(meta or {}))
    um = np.round(segs * 1000).astype(np.int32)
    delta = np.diff(um, axis=0, prepend=np.zeros((1, 4), np.int32)).astype(np.int32)
    np.savez_compressed(path, seg_delta_um=delta, kind=kinds.astype(np.uint8), part=pidx.astype(np.uint8),
                        layer_ptr=ptr.astype(np.int64), meta=np.array(json.dumps(info)))


def load_build(path):
    """(segs mm (n, 4), kind, part, layer_ptr, meta) from a save_build file."""
    z = np.load(path, allow_pickle=False)
    meta = json.loads(str(z["meta"]))
    segs = np.cumsum(z["seg_delta_um"].astype(np.int64), axis=0).astype(float) / 1000.0
    return segs, z["kind"], z["part"], z["layer_ptr"], meta


# --------------------------------------------------------------------------------------------------
# Timing of one layer's list (the RTC5 rules, see rtc5_list.py for the commands)
# --------------------------------------------------------------------------------------------------
def ticks(t, tick):
    return math.ceil(t / tick - 1e-9) * tick


def layer_time(segs, kinds, pidx, parts, psets, tm: Timing, start=(0.0, 0.0), end=(0.0, 0.0)):
    """List execution time, laser-on time and delivered energy of one layer.
    A segment whose start equals the previous end (within 1 um) continues the polyline (polygon delay); otherwise
    the scanner jumps (mark delay before, jump delay after; variable below jump_limit)."""
    t = 0.0
    t_on = 0.0
    E = 0.0
    pos = np.array(start, float)
    in_poly = False
    n_jump = n_poly = n_mark = 0
    seq_mark_t = 0.0
    seq_P = 0.0
    jump_len = 0.0
    mark_len = 0.0

    def close_seq():
        nonlocal t_on, E, seq_mark_t
        if seq_mark_t > 0:
            on = max(seq_mark_t - tm.laser_on_delay + tm.laser_off_delay, 0.0)
            t_on += on
            E += seq_P * on
        seq_mark_t = 0.0

    for s, kd, ii in zip(segs, kinds, pidx):
        p0, p1 = s[:2], s[2:]
        ps = psets[parts[ii].pset]
        P, v = (ps.P_hatch, ps.v_hatch) if kd == 0 else (ps.P_contour, ps.v_contour)
        gap = float(np.hypot(*(p0 - pos)))
        if gap > 1e-3 or not in_poly:
            if in_poly:
                t += tm.mark_delay
                close_seq()
            if gap > 1e-3:
                jd = tm.jump_delay if gap >= tm.jump_limit else tm.jump_delay_min + (tm.jump_delay - tm.jump_delay_min) * gap / tm.jump_limit
                t += ticks(gap / tm.v_jump, tm.tick) + ticks(jd, tm.tick)
                n_jump += 1
                jump_len += gap
            in_poly = True
            seq_P = P
        else:
            t += tm.polygon_delay
            n_poly += 1
        L = float(np.hypot(*(p1 - p0)))
        dt = ticks(L / v, tm.tick)
        t += dt
        seq_mark_t += dt
        n_mark += 1
        mark_len += L
        pos = p1
    if in_poly:
        t += tm.mark_delay
        close_seq()
    gap = float(np.hypot(*(np.asarray(end) - pos)))
    t += ticks(gap / tm.v_jump, tm.tick) + ticks(tm.jump_delay, tm.tick) + tm.list_overhead
    return dict(t_list=t, t_laser_on=t_on, energy_J=E, n_mark=n_mark, n_jump=n_jump, n_corner=n_poly,
                mark_mm=mark_len, jump_mm=jump_len)


def build_schedule(parts, psets, tm, rc, stage, segs, kinds, pidx, ptr, layer_mm):
    rec = recoat_time(rc, stage, layer_mm)
    rows = []
    t = 0.0
    for k in range(len(ptr) - 1):
        a, b = ptr[k], ptr[k + 1]
        lt = layer_time(segs[a:b], kinds[a:b], pidx[a:b], parts, psets, tm)
        period = lt["t_list"] + rec["t_recoat"]
        rows.append(dict(layer=k + 1, t_start_s=t, exposure_s=lt["t_list"], laser_on_s=lt["t_laser_on"],
                         energy_J=lt["energy_J"], period_s=period, mean_W=lt["energy_J"] / period,
                         mark_mm=lt["mark_mm"], jump_mm=lt["jump_mm"], n_vectors=lt["n_mark"]))
        t += period
    return rows, rec


def main():
    OUT.mkdir(exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    tm, rc = Timing(), Recoat()
    psets = PSETS
    lay = layout_table()
    (OUT / "layout.json").write_text(json.dumps(lay, indent=1))
    for r in lay:
        print(f"{r['size_mm']:g} mm squares, gap {r['gap_mm']:g} mm: {r['count']}")
    parts = first_build(height=15.0)
    print("layout issues:", check_layout(parts) or "none")
    segs, kinds, pidx, ptr = build_vectors(parts, psets)
    path = OUT / "build_first_coupons_15mm.npz"
    save_build(path, parts, psets, tm, segs, kinds, pidx, ptr)
    back = load_build(path)
    err = float(np.abs(back[0] - segs).max())
    print(f"{len(ptr) - 1} layers, {len(segs)} vectors, {path.stat().st_size / 1e3:.0f} kB; round trip max error {err * 1e3:.2f} um")
    layer = CUBE_SET.layer
    summary, times = {}, []
    for stage in (X_LSM100B, X_LSQ075B):
        for v_spread in (10.0, 20.0, 40.0, 80.0):
            rcv = Recoat(v_spread=v_spread)
            rows, rec = build_schedule(parts, psets, tm, rcv, stage, segs, kinds, pidx, ptr, layer)
            summary[(stage.name, v_spread)] = dict(recoat=rec, rows=rows)
            for hmm in (5.0, 10.0, 15.0):
                n = int(round(hmm / layer))
                tt = sum(r["period_s"] for r in rows[:n])
                t_scan = sum(r["exposure_s"] for r in rows[:n])
                times.append(dict(stage=stage.name, v_spread_mm_s=v_spread, build_mm=hmm, layers=n, hours=tt / 3600,
                                  scan_h=t_scan / 3600, return_h=n * rec["t_return"] / 3600,
                                  spread_h=n * rec["t_spread"] / 3600, step_h=n * rec["t_step"] / 3600,
                                  overhead_h=n * rec["t_overhead"] / 3600, recoat_s=rec["t_recoat"],
                                  list_s_mean=t_scan / n))
    # tracking error 0.7 ms (worn 2003 galvos): every delay scaled by 0.7 / 0.5
    s = 0.7 / 0.5
    tm_old = Timing(tracking_error=700e-6, jump_delay=tm.jump_delay * s, jump_delay_min=tm.jump_delay_min * s,
                    mark_delay=tm.mark_delay * s, polygon_delay=tm.polygon_delay * s, laser_on_delay=tm.laser_on_delay * s,
                    laser_off_delay=tm.laser_off_delay * s)
    rows_old, _ = build_schedule(parts, psets, tm_old, rc, X_LSM100B, segs, kinds, pidx, ptr, layer)
    sens = dict(list_s_mean_0p5ms=float(np.mean([r["exposure_s"] for r in summary[(X_LSM100B.name, 40.0)]["rows"]])),
                list_s_mean_0p7ms=float(np.mean([r["exposure_s"] for r in rows_old])))
    for t in times:
        if t["build_mm"] == 10.0:
            print(f"{t['stage']}, spread {t['v_spread_mm_s']:.0f} mm/s: 10 mm in {t['hours']:.2f} h "
                  f"(recoat {t['recoat_s']:.2f} s, list {t['list_s_mean']:.2f} s)")
    print("tracking error sensitivity", sens)
    with open(OUT / "build_times.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(times[0]))
        w.writeheader()
        for t in times:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in t.items()})
    rows = summary[(X_LSM100B.name, 40.0)]["rows"]
    cols = ["layer", "t_start_s", "exposure_s", "energy_J", "mean_W", "laser_on_s", "period_s"]
    for dst in (OUT / "heat_input.csv", SCRATCH / "heat_input.csv"):
        with open(dst, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for r in rows:
                w.writerow([r["layer"]] + [f"{r[c]:.4f}" for c in cols[1:]])
    per_part = {}
    a, b = ptr[0], ptr[1]
    for i, p in enumerate(parts):
        sel = pidx[a:b] == i
        lt = layer_time(segs[a:b][sel], kinds[a:b][sel], pidx[a:b][sel], parts, psets, tm)
        per_part[p.name] = dict(pset=p.pset, cx=p.cx, cy=p.cy, sx=p.sx, sy=p.sy, energy_J_layer1=lt["energy_J"],
                                laser_on_s=lt["t_laser_on"], list_s=lt["t_list"], vectors=lt["n_mark"])
    info = dict(parts=per_part, psets={k: asdict(v) for k, v in psets.items()}, timing=asdict(tm),
                recoat={f"{k[0]}, spread {k[1]:.0f} mm/s": v["recoat"] for k, v in summary.items()},
                tracking_error_sensitivity=sens, npz=dict(path=path.name, kB=path.stat().st_size / 1e3,
                                                          vectors=int(len(segs)), layers=int(len(ptr) - 1)),
                energy_J_mean=float(np.mean([r["energy_J"] for r in rows])),
                mean_W_mean=float(np.mean([r["mean_W"] for r in rows])),
                period_s_mean=float(np.mean([r["period_s"] for r in rows])))
    (OUT / "scan_program.json").write_text(json.dumps(info, indent=1))
    print("heat input: mean energy per layer", info["energy_J_mean"], "J; mean W", info["mean_W_mean"])
    figures(parts, psets, segs, kinds, pidx, ptr, times)


def figures(parts, psets, segs, kinds, pidx, ptr, times):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection
    from matplotlib.patches import Circle, Rectangle
    C1, C2, C3, C4, C5 = "#257de0", "#f47230", "#00b894", "#f2a600", "#ee7fac"
    INK, INK2, GRID = "#191919", "#666666", "#e6e6e6"
    plt.rcParams.update({"font.size": 8.5, "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.spines.top": False, "axes.spines.right": False})
    # ---- layout and the vectors of layers 1 and 2 ----
    fig, axs = plt.subplots(1, 2, figsize=(11.5, 5.6))
    for ax, k in zip(axs, (0, 1)):
        ax.set_aspect("equal")
        ax.add_patch(Circle((0, 0), PLATE_R, fc="#f4f4f4", ec=INK2, lw=1.0))
        ax.add_patch(Circle((0, 0), USABLE_R, fc="none", ec=INK2, lw=0.8, ls="--"))
        for (sx, sy) in screws():
            ax.add_patch(Circle((sx, sy), 1.9, fc=INK2, ec="none"))
        a, b = ptr[k], ptr[k + 1]
        s, kd = segs[a:b], kinds[a:b]
        hatch = LineCollection([[(x0, y0), (x1, y1)] for x0, y0, x1, y1 in s[kd == 0]], colors=C1, linewidths=0.35)
        cont = LineCollection([[(x0, y0), (x1, y1)] for x0, y0, x1, y1 in s[kd == 1]], colors=C2, linewidths=1.2)
        ax.add_collection(hatch)
        ax.add_collection(cont)
        # jumps
        ends = np.vstack([np.zeros((1, 2)), s[:, 2:]])[:-1]
        starts = s[:, :2]
        gap = np.hypot(*(starts - ends).T)
        J = [[tuple(e), tuple(st)] for e, st, g in zip(ends, starts, gap) if g > 1.0]
        ax.add_collection(LineCollection(J, colors=INK2, linewidths=0.6, linestyles=":"))
        for p in parts:
            ps = psets[p.pset]
            ax.text(p.cx, p.cy, f"{p.name}\n{ps.P_hatch:.0f} W\n{ps.v_hatch / 1000:.2f} m/s\nh {ps.hatch:.2f}",
                    ha="center", va="center", fontsize=6.5 if p.sx < 8 else 7.5, color=INK,
                    bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.6))
        ax.annotate("", xy=(17, 21.5), xytext=(17, 15.5), arrowprops=dict(arrowstyle="->", color=INK2))
        ax.text(17.6, 18, "gas", fontsize=7.5, color=INK2, rotation=90, va="center")
        ax.annotate("", xy=(-10, -21.5), xytext=(-17, -21.5), arrowprops=dict(arrowstyle="->", color=INK2))
        ax.text(-13.5, -23.6, "recoat", fontsize=7.5, color=INK2, ha="center")
        ax.set_xlim(-22, 22); ax.set_ylim(-24.5, 23)
        ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)")
        ax.grid(color=GRID, lw=0.5)
        th = (CUBE_SET.rot_deg * k) % 180
        ax.set_title(f"Layer {k + 1}: hatch at {th:.0f}°, {b - a} vectors\n(blue hatch, orange contour, dotted jumps)",
                     fontsize=9, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(HERE / "img" / "coupon-layout.png", dpi=150)
    plt.close(fig)
    # ---- build-time breakdown, 10 mm builds ----
    rows = [t for t in times if t["build_mm"] == 10.0]
    labels = [f"{t['stage'].replace('Zaber ', '').replace('-E03', '').replace('-E01', '')}\nspread {t['v_spread_mm_s']:.0f} mm/s"
              for t in rows]
    fig, ax = plt.subplots(figsize=(11.5, 4.2))
    left = np.zeros(len(rows))
    parts_ = (("scan (RTC5 list)", "scan_h", C1), ("spread stroke", "spread_h", C2), ("return stroke", "return_h", C3),
              ("plate step", "step_h", C4), ("host overhead", "overhead_h", C5))
    for name, key, col in parts_:
        vals = np.array([t[key] for t in rows])
        ax.barh(np.arange(len(rows)), vals, left=left, color=col, edgecolor="white", linewidth=2, label=name, height=0.62)
        left += vals
    for i, t in enumerate(rows):
        ax.text(left[i] + 0.01, i, f"{t['hours']:.2f} h", va="center", fontsize=8, color=INK)
    ax.axvspan(1.2, 1.8, color="#efefef", zorder=0)
    ax.text(1.5, 0.0, "study's estimate\n1.2-1.8 h", ha="center", va="center", fontsize=8, color=INK2)
    ax.set_yticks(np.arange(len(rows)), labels, fontsize=7.5)
    ax.invert_yaxis()
    ax.set_xlabel("hours for a 10 mm build (333 layers of 30 um), first coupon layout")
    ax.legend(loc="lower right", fontsize=7.5, frameon=False, ncol=5, bbox_to_anchor=(1.0, -0.22))
    ax.grid(axis="x", color=GRID, lw=0.5)
    ax.set_title("Build time: three 10 x 10 mm and two 5 x 5 mm cubes, by recoater stage and spreading speed",
                 fontsize=9.5, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(HERE / "img" / "build-time.png", dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    main()
