"""Read the process worker's scan program (process/scan_program.py save_build format) or make a synthetic one.

NPZ format (process/scan_program.py, save_build): seg_delta_um int32 (n, 4) delta-coded by column (np.cumsum along
axis 0 restores x0 y0 x1 y1 in um); kind 0 hatch / 1 contour; part index into meta["parts"]; layer_ptr (segments of
layer k are rows layer_ptr[k]:layer_ptr[k+1]); meta JSON with parts, parameter sets (P_hatch, v_hatch, P_contour,
v_contour, layer) and the scanner timing used for the time estimate.
"""
from __future__ import annotations

import json
import math
import pathlib
from dataclasses import dataclass
from typing import Optional

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
DEFAULT_TIMING = dict(tick=10e-6, v_jump=5000.0, jump_delay=300e-6, jump_delay_min=100e-6, jump_limit=5.0,
                      mark_delay=150e-6, polygon_delay=50e-6, laser_on_delay=100e-6, laser_off_delay=150e-6,
                      list_overhead=0.05)


@dataclass
class Layer:
    index: int
    z_mm: float               # top of this layer above the substrate
    segs: np.ndarray          # (n, 4) mm: x0 y0 x1 y1 in the machine frame
    power_W: np.ndarray       # (n,)
    speed_mm_s: np.ndarray    # (n,)
    kind: np.ndarray          # (n,) 0 hatch, 1 contour
    part: np.ndarray          # (n,)

    def __len__(self):
        return len(self.segs)


@dataclass
class ScanProgram:
    segs: np.ndarray
    kind: np.ndarray
    part: np.ndarray
    layer_ptr: np.ndarray
    meta: dict
    source: str

    @property
    def n_layers(self) -> int:
        return len(self.layer_ptr) - 1

    @property
    def layer_mm(self) -> float:
        ps = next(iter(self.meta["psets"].values()))
        return float(ps["layer"])

    def timing(self) -> dict:
        t = dict(DEFAULT_TIMING)
        t.update({k: v for k, v in self.meta.get("timing", {}).items() if k in DEFAULT_TIMING})
        return t

    def layer(self, k: int) -> Layer:
        a, b = int(self.layer_ptr[k]), int(self.layer_ptr[k + 1])
        parts = self.meta["parts"]
        psets = self.meta["psets"]
        kind = self.kind[a:b]
        part = self.part[a:b]
        P = np.empty(b - a)
        v = np.empty(b - a)
        for i, (kd, pi) in enumerate(zip(kind, part)):
            ps = psets[parts[int(pi)]["pset"]]
            P[i], v[i] = (ps["P_hatch"], ps["v_hatch"]) if kd == 0 else (ps["P_contour"], ps["v_contour"])
        return Layer(k, (k + 1) * self.layer_mm, self.segs[a:b], P, v, kind, part)


def load_npz(path) -> ScanProgram:
    z = np.load(path, allow_pickle=False)
    meta = json.loads(str(z["meta"]))
    segs = np.cumsum(z["seg_delta_um"].astype(np.int64), axis=0).astype(float) / 1000.0
    return ScanProgram(segs, z["kind"].astype(np.uint8), z["part"].astype(np.uint8), z["layer_ptr"].astype(np.int64),
                       meta, str(path))


def synthetic(n_layers: int = 20, size: float = 10.0, hatch: float = 0.1, P: float = 250.0, v: float = 1200.0,
              layer_mm: float = 0.030, rot_deg: float = 67.0) -> ScanProgram:
    """One size x size mm square at the plate centre: meander hatch rotated rot_deg per layer and one contour."""
    segs, kinds, ptr = [], [], [0]
    for k in range(n_layers):
        th = math.radians((rot_deg * k) % 180.0)
        d = np.array([math.cos(th), math.sin(th)])
        nrm = np.array([-d[1], d[0]])
        h = size / 2 - 0.14
        lay = []
        n = int(2 * h * math.sqrt(2) / hatch) + 1
        for i in range(n):
            o = -h * math.sqrt(2) + i * hatch
            ts = []
            for (p, dd) in ((o * nrm[0], d[0]), (o * nrm[1], d[1])):
                if abs(dd) < 1e-12:
                    ts.append((-1e9, 1e9) if abs(p) <= h else (1, 0))
                else:
                    a_, b_ = (-h - p) / dd, (h - p) / dd
                    ts.append((min(a_, b_), max(a_, b_)))
            t0, t1 = max(ts[0][0], ts[1][0]), min(ts[0][1], ts[1][1])
            if t1 - t0 > 1e-6:
                s = o * nrm + t0 * d
                e = o * nrm + t1 * d
                if len(lay) % 2:
                    s, e = e, s
                lay.append((*s, *e))
        c = size / 2 - 0.08
        pts = [(-c, -c), (c, -c), (c, c), (-c, c), (-c, -c)]
        con = [(*pts[i], *pts[i + 1]) for i in range(4)]
        segs.append(np.array(lay + con))
        kinds.append(np.r_[np.zeros(len(lay)), np.ones(4)].astype(np.uint8))
        ptr.append(ptr[-1] + len(lay) + 4)
    meta = dict(frame="cad/ft_model.py", parts=[dict(name="S", cx=0.0, cy=0.0, sx=size, sy=size,
                                                     height=n_layers * layer_mm, pset="syn")],
                psets=dict(syn=dict(name="syn", P_hatch=P, v_hatch=v, hatch=hatch, P_contour=0.6 * P,
                                    v_contour=0.67 * v, layer=layer_mm)),
                timing=dict(DEFAULT_TIMING), units={}, synthetic=True)
    S = np.vstack(segs)
    return ScanProgram(S, np.concatenate(kinds), np.zeros(len(S), np.uint8), np.array(ptr, np.int64), meta,
                       "synthetic")


def find_program(explicit: Optional[str] = None) -> Optional[pathlib.Path]:
    """The process worker's build file: an explicit path, else ../process/out/build_*.npz next to this package, else
    /tmp/ft-process/**/build_*.npz, else /tmp/ft-control/build_*.npz. None if there is none."""
    if explicit:
        return pathlib.Path(explicit)
    cands = sorted((HERE.parents[1] / "process" / "out").glob("build_*.npz"))
    cands += sorted(pathlib.Path("/tmp/ft-process").glob("**/build_*.npz"))
    cands += sorted(pathlib.Path("/tmp/ft-control").glob("build_*.npz"))
    return cands[0] if cands else None


def polylines(layer: Layer, tol_mm: float = 1e-3):
    """Split a layer into polylines: runs of segments that start where the previous one ended, with one power and
    speed (a change of either starts a new run). Yields (start (2,), list of (end (2,), P, v, kind))."""
    run, start, last = [], None, None
    for s, P, v, kd in zip(layer.segs, layer.power_W, layer.speed_mm_s, layer.kind):
        p0, p1 = s[:2], s[2:]
        cont = (last is not None and np.hypot(*(p0 - last[0])) <= tol_mm and P == last[1] and v == last[2])
        if not cont:
            if run:
                yield start, run
            run, start = [], p0.copy()
        run.append((p1.copy(), float(P), float(v), int(kd)))
        last = (p1, P, v)
    if run:
        yield start, run


def layer_time(layer: Layer, timing: dict, start=(0.0, 0.0), end=(0.0, 0.0)) -> dict:
    """List execution time, laser-on time and delivered energy of one layer by the RTC5's rules (10 us clock; mark,
    polygon and variable jump delays; laser on/off delays). Same rules as process/scan_program.py layer_time."""
    tm = timing
    tick = tm["tick"]

    def ticks(t):
        return math.ceil(t / tick - 1e-9) * tick

    t = t_on = E = 0.0
    pos = np.asarray(start, float)
    n_mark = n_jump = 0
    mark_mm = jump_mm = 0.0
    for p0, run in polylines(layer):
        gap = float(np.hypot(*(p0 - pos)))
        if gap > 1e-3:
            jd = tm["jump_delay"] if gap >= tm["jump_limit"] else (
                tm["jump_delay_min"] + (tm["jump_delay"] - tm["jump_delay_min"]) * gap / tm["jump_limit"])
            t += ticks(gap / tm["v_jump"]) + ticks(jd)
            n_jump += 1
            jump_mm += gap
        seq = 0.0
        cur = p0
        for i, (p1, P, v, kd) in enumerate(run):
            if i:
                t += tm["polygon_delay"]
            L = float(np.hypot(*(p1 - cur)))
            dt = ticks(L / v)
            t += dt
            seq += dt
            mark_mm += L
            n_mark += 1
            cur = p1
        t += tm["mark_delay"]
        on = max(seq - tm["laser_on_delay"] + tm["laser_off_delay"], 0.0)
        t_on += on
        E += run[0][1] * on
        pos = cur
    gap = float(np.hypot(*(np.asarray(end) - pos)))
    t += ticks(gap / tm["v_jump"]) + ticks(tm["jump_delay"]) + tm["list_overhead"]
    return dict(t_list=t, t_laser_on=t_on, energy_J=E, n_mark=n_mark, n_jump=n_jump, mark_mm=mark_mm,
                jump_mm=jump_mm)
