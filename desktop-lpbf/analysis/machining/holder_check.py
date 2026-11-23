"""Tool-holder, spindle, fixture and travel check of the chamber frame and floor plate G-code (issue #260, PR #266).

CAMotics models the cutter only, and camotics_sim.py's rapid check treats the tool as a cylinder going up forever. This
script sweeps the whole tool assembly along every move of each setup's posted program (freecad_cam.py's .ngc files):
  * the cutter's flutes and shank (flute length and overall length of the end mills in tooling-bom.csv), the CT40 holder
    (Haas Tooling part numbers, dimensions read off haastooling.com's product pages, HOLDERS below), the CAT40 flange and
    the spindle nose;
  * against the in-process stock at that point in the program: the blank (minus the frame's waterjet core) less every
    earlier setup's cuts, less what this setup has cut so far. The flutes cut; anything above them (shank, holder,
    flange, spindle) that meets stock is a collision, and so is a rapid whose flutes go more than 0.5 mm into stock;
  * against that setup's fixtures (FIXTURES below, from setup_plan.json's fixture notes: end tabs and toe clamps, risers,
    parallels, the dummy-floor plate, the floor plate's stud and clamp washer, the HRT210 rotary with its riser), which
    nothing may touch, flutes included;
  * against the Haas VF-4's travels (X 1270, Y 508 mm; spindle nose 107-742 mm above the table), with the part centred in
    X and Y travel and the table height set by the fixture stack.

Method. The tool is vertical in every setup, and the assembly's radius grows upward (each part is taken as at least as
wide as the parts below it). So a column of material at horizontal distance rho from the tool axis is hit iff its top is
above tip + h(rho), where h is the height of the lowest part of the assembly at least rho wide. Stock and fixtures are
therefore held as top-surface height maps on a --res grid (0.5 mm), in the setup frame, and each straight piece of each
move (arcs split to 0.25 mm chord) is tested exactly against the columns within reach. The in-process stock is a voxel
grid at --res in the part frame: each setup starts from the top surface of the stock its predecessors left (seen from
that setup's side) and lowers it column by column as the flutes pass (the lowest tip over each column); at the end of a
setup every voxel above that z-map is removed. Clearance is the largest c for which the assembly, grown by c in radius
and lowered by c, still misses: c = min over columns of max(distance - radius, tip + height - top). It is reported per
tool per setup against stock and against fixtures, with the G-code line of the tightest move; it is exact to the grid
(0.5 mm in x and y; z is exact for flat tops, +-0.5 mm on the voxel stock's curved tops).
If $CAMOTICS_WORK holds camotics_sim.py's final voxels, the chained stock at the end is compared with CAMotics' own
(stock_vs_camotics in the JSON).

Run (after freecad_cam.py has written $CHAMBER_CAM_IN/gcode/*.ngc):
    OMP_NUM_THREADS=1 /tmp/capmem 2 env CHAMBER_CAM_IN=/tmp/chamber-cam CAMOTICS_WORK=/tmp/cam-sim /tmp/venv/bin/python \
        desktop-lpbf/analysis/machining/holder_check.py [--res 0.5]
Writes desktop-lpbf/analysis/out/machining/holder_check.json.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import pathlib
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import camotics_sim as CS  # noqa: E402
import freecad_cam as FC  # noqa: E402

IN_DIR = pathlib.Path(os.environ.get("CHAMBER_CAM_IN", "/tmp/chamber-cam"))
OUT = HERE.parent / "out" / "machining" / "holder_check.json"
IN = 25.4
DMAX = 10.0          # mm: clearances above this are reported as ">= 10"
RAPID_TOL = 0.5      # mm: a rapid's flutes may graze stock by this much (voxel noise), as in camotics_sim.py
TIGHT = 2.0          # mm: clearances under this are flagged as tight (tool-length setting, thermal growth, chips)

# --- VF-4 (setup_plan.json "machines", haascnc.com VF-4 page fetched 2026-11-23 22:35 UTC through the lab tunnel) --------
VF4 = dict(x_travel=1270.0, y_travel=508.0, nose_to_table=(107.0, 742.0))
# The CAT40 V-flange (ASME B5.50): 2.50 in. diameter; taken as 5/8 in. thick, ending at the gauge line.
FLANGE = (15.875, 31.75)
# Spindle nose and head of the VF-4's inline 40-taper spindle: no Haas drawing found, so ASSUMED: a 150 mm nose for 100 mm
# above the gauge line, then the head as a 300 mm cylinder going up forever.
SPINDLE = [(0.0, 100.0, 75.0), (100.0, 1e6, 150.0)]

# --- holders: Haas Tooling CT40, TSC; "Technical specifications" read from https://www.haastooling.com/p/<part number>
# (fetched 2026-11-23 22:30 UTC through the lab tunnel). profile = (from, to, radius) in mm measured up from the holder's
# nose face, ending at the flange's front face (gauge length - flange thickness); where a page gives only the nose
# (body diameter x body length), the rest up to the flange is ASSUMED as wide as the body or the shoulder.
HOLDERS = {
    "04-0004": dict(title='CT40 3/4" End Mill Holder x 1-3/4" Gage Length, TSC (side lock)', bore=0.75 * IN,
                    gage=1.75 * IN, spec="body dia. 1.75 in. x body length 1.0 in.; min. body dia. 1.25 in.; 5/8-18 set screw",
                    profile=[(0.0, 1.75 * IN - 15.875, 1.75 * IN / 2)]),
    "04-0001": dict(title='CT40 1/2" End Mill Holder x 1-3/4" Gage Length, TSC (side lock)', bore=0.5 * IN,
                    gage=1.75 * IN, spec="body dia. 1.25 in. x 1.0 in.; shoulder dia. 1.75 in. x 0.63 in.",
                    profile=[(0.0, 1.0 * IN, 1.25 * IN / 2), (1.0 * IN, 1.75 * IN - 15.875, 1.75 * IN / 2)]),
    "04-0006": dict(title="CT40 ER16 Collet Chuck x 2-1/2\" Gage Length, TSC", bore=None, gage=2.5 * IN,
                    spec="body (nut) dia. 1.1 in. x body length 1.12 in.; ER16 holds 1-10 mm",
                    profile=[(0.0, 1.12 * IN, 1.1 * IN / 2), (1.12 * IN, 2.5 * IN - 15.875, 1.75 * IN / 2)]),
    "04-0010": dict(title="CT40 ER32 Collet Chuck x 2-1/2\" Gage Length, TSC", bore=None, gage=2.5 * IN,
                    spec="body (nut) dia. 1.97 in. x body length 1.75 in.; ER32 holds 2-20 mm",
                    profile=[(0.0, 2.5 * IN - 15.875, 1.97 * IN / 2)]),
    "04-0011": dict(title="CT40 ER32 Collet Chuck x 4\" Gage Length, TSC", bore=None, gage=4.0 * IN,
                    spec="body (nut) dia. 1.97 in. x body length 3.25 in.",
                    profile=[(0.0, 4.0 * IN - 15.875, 1.97 * IN / 2)]),
    "04-0048": dict(title='CT40 3/4" Shrink Fit Holder x 3.15" Gage Length, TSC', bore=0.75 * IN, gage=3.15 * IN,
                    spec="nose dia. 1.299 in. rising at 4.5 deg to 1.654 in.; clamping length 1.654-2.126 in.",
                    profile=[(0.0, 57.2, 1.654 * IN / 2), (57.2, 3.15 * IN - 15.875, 1.654 * IN / 2)]),
    "04-0015": dict(title='CT40 Shell Mill Holder, 3/4" Pilot Diameter x 2" Gage Length, TSC', bore=None,
                    gage=2.0 * IN, spec="body dia. 1.69 in. x body length 1.25 in.; pilot 0.687 in. long",
                    profile=[(0.0, 2.0 * IN - 15.875, 1.69 * IN / 2)]),
}

# --- cutters: the real tools behind freecad_cam.TOOLS (tooling-bom.csv lines). loc = flute length, oal = overall length,
# stick = stick-out from the holder's nose (freecad_cam's "length"). The face mill's body height is ASSUMED (40 mm, a
# typical 2.5 in. shell-type face mill); its inserts cut the bottom 8 mm.
CUTTERS = {
    1: dict(holder="04-0015", loc=8.0, stick=40.0, shank_r=31.75, bom="face mill (shop's, 3/4 in. arbor)"),
    2: dict(holder="04-0004", loc=1.5 * IN, oal=4.0 * IN, bom="A5 Lakeshore 1600034, 3/4 x 1-1/2 LOC x 4 OAL"),
    3: dict(holder="04-0001", loc=1.0 * IN, oal=3.0 * IN, bom="A4 Lakeshore LC205012, 1/2 x 1 LOC x 3 OAL"),
    4: dict(holder="04-0006", loc=0.5 * IN, oal=1.5 * IN, bom="A1 Lakeshore LC205018, 1/8 x 1/2 LOC x 1-1/2 OAL"),
    5: dict(holder="04-0006", loc=None, bom="5.0 mm carbide drill (stub length)"),
    6: dict(holder="04-0006", loc=None, bom="3.3 mm carbide drill (stub length)"),
    7: dict(holder="04-0006", loc=None, bom="4.2 mm carbide drill (stub length)"),
    8: dict(holder="04-0006", loc=None, bom="6.0 mm carbide drill (stub length)"),
    9: dict(holder="04-0006", loc=0.75 * IN, oal=2.5 * IN, bom="A2 Lakeshore LC205014, 1/4 x 3/4 LOC x 2-1/2 OAL"),
}
for _t, _spec in FC.TOOLS.items():  # freecad_cam.py's own holder choice wins
    if "holder" in _spec:
        CUTTERS[_t] = dict(CUTTERS[_t], holder=_spec["holder"])


def assembly(t):
    """[(z_lo, z_hi, r, part, cutting)] from the tip up, radii made non-decreasing upward; and the gauge length"""
    spec, c = FC.TOOLS[t], CUTTERS[t]
    r = spec["d"] / 2
    stick = c.get("stick", spec["length"])
    loc = c["loc"] if c.get("loc") else stick  # drills: fluted to the holder
    loc = min(loc, stick)
    h = HOLDERS[c["holder"]]
    segs = [(0.0, loc, r, "flutes", True)]
    if loc < stick:
        segs.append((loc, stick, c.get("shank_r", r), "shank", False))
    for a, b, rr in h["profile"]:
        segs.append((stick + a, stick + b, rr, "holder " + c["holder"], False))
    gl = stick + h["gage"]
    segs.append((gl - FLANGE[0], gl, FLANGE[1], "CAT40 flange", False))
    for a, b, rr in SPINDLE:
        segs.append((gl + a, gl + b, rr, "spindle nose" if a == 0 else "spindle head", False))
    out, rmax = [], 0.0
    for z0, z1, rr, name, cut in segs:
        rmax = max(rmax, rr)
        out.append((z0, z1, rmax, name, cut))
    return out, gl


# --- fixtures (setup frame, mm) ----------------------------------------------------------------------------------
TAB = float(os.environ.get("HOLDER_TAB", 0)) or None


def fixtures(su):
    """(table z in the setup frame, [(name, kind, params)], end tabs as extra stock [(x0, x1, y0, y1, z0, z1)])"""
    name = su["name"]
    fx = getattr(FC, "FIXTURES", {}).get(name)
    if fx is not None:
        return fx
    raise KeyError(name)


def top_of(kind, p, X, Y):
    """top z of a fixture primitive over the grid columns (X, Y), -inf where absent"""
    if kind == "box":
        x0, x1, y0, y1, z0, z1 = p
        m = (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)
        return np.where(m, z1, -np.inf)
    if kind == "vcyl":
        cx, cy, r, z0, z1 = p
        return np.where((X - cx) ** 2 + (Y - cy) ** 2 <= r * r, z1, -np.inf)
    if kind == "ycyl":  # cylinder with its axis along y: (cx, cz, r, y0, y1)
        cx, cz, r, y0, y1 = p
        dx2 = r * r - (X - cx) ** 2
        m = (dx2 >= 0) & (Y >= y0) & (Y <= y1)
        return np.where(m, cz + np.sqrt(np.maximum(dx2, 0)), -np.inf)
    raise ValueError(kind)


# --- the sweep --------------------------------------------------------------------------------------------------
class Field:
    """a top-surface height map with a block-max pyramid for quick rejection"""
    B = 16

    def __init__(self, top, x0, y0, h):
        self.top, self.x0, self.y0, self.h = top, x0, y0, h
        nx, ny = top.shape
        self.nbx, self.nby = -(-nx // self.B), -(-ny // self.B)
        pad = np.full((self.nbx * self.B, self.nby * self.B), -np.inf, np.float32)
        pad[:nx, :ny] = top
        self.blk = pad.reshape(self.nbx, self.B, self.nby, self.B).max(axis=(1, 3))

    def window(self, xlo, xhi, ylo, yhi):
        nx, ny = self.top.shape
        i0 = max(int(math.floor((xlo - self.x0) / self.h)), 0)
        i1 = min(int(math.ceil((xhi - self.x0) / self.h)) + 1, nx)
        j0 = max(int(math.floor((ylo - self.y0) / self.h)), 0)
        j1 = min(int(math.ceil((yhi - self.y0) / self.h)) + 1, ny)
        return i0, i1, j0, j1

    def blockmax(self, i0, i1, j0, j1):
        if i0 >= i1 or j0 >= j1:
            return -np.inf
        return float(self.blk[i0 // self.B:(i1 - 1) // self.B + 1, j0 // self.B:(j1 - 1) // self.B + 1].max())

    def refresh(self, i0, i1, j0, j1):
        b0, b1 = i0 // self.B, (i1 - 1) // self.B + 1
        c0, c1 = j0 // self.B, (j1 - 1) // self.B + 1
        sub = self.top[b0 * self.B:b1 * self.B, c0 * self.B:c1 * self.B]
        nx, ny = sub.shape
        pad = np.full(((b1 - b0) * self.B, (c1 - c0) * self.B), -np.inf, np.float32)
        pad[:nx, :ny] = sub
        self.blk[b0:b1, c0:c1] = pad.reshape(b1 - b0, self.B, c1 - c0, self.B).max(axis=(1, 3))


def reach(p0, p1, X, Y, rr):
    """columns within rr of the tool axis on the piece p0 -> p1: (mask, distance, lowest tip z while within rr)"""
    d = p1 - p0
    a = d[0] ** 2 + d[1] ** 2
    fx, fy = p0[0] - X, p0[1] - Y
    if a < 1e-12:
        dist = np.sqrt(fx ** 2 + fy ** 2)
        return dist <= rr, dist, np.full(X.shape, min(p0[2], p1[2]))
    t = np.clip(-(d[0] * fx + d[1] * fy) / a, 0, 1)
    dist = np.sqrt((fx + t * d[0]) ** 2 + (fy + t * d[1]) ** 2)
    c0 = fx ** 2 + fy ** 2 - rr ** 2
    bq = 2 * (d[0] * fx + d[1] * fy)
    disc = bq ** 2 - 4 * a * c0
    sq = np.sqrt(np.maximum(disc, 0))
    ta = np.clip((-bq - sq) / (2 * a), 0, 1)
    tb = np.clip((-bq + sq) / (2 * a), 0, 1)
    zt = np.minimum(p0[2] + ta * d[2], p0[2] + tb * d[2])
    return (disc >= 0) & (dist <= rr), dist, zt


def sweep(su, moves, stock_top, fix_top, fix_lab, fix_names, x0, y0, h, zc, lower=None):
    """runs the setup's moves; lowers stock_top and the cut z-map zc in place; returns per-tool and collision records"""
    S = Field(stock_top, x0, y0, h)
    F = Field(fix_top, x0, y0, h)
    asm = {t: assembly(t) for t in {m["tool"] for m in moves}}
    per_tool, hits = {}, []
    for mi, mv in enumerate(moves):
        t = mv["tool"]
        segs, gl = asm[t]
        rec = per_tool.setdefault(t, dict(stock=dict(c=DMAX, line=None, op=None, part=None),
                                          fixture=dict(c=DMAX, line=None, op=None, part=None, what=None),
                                          by_part={}))
        pts = CS.segments(mv)
        for p0, p1 in zip(pts[:-1], pts[1:]):
            zlo_piece = min(p0[2], p1[2])
            for z0, z1, r, part, cut in segs:
                if cut and mv["rapid"]:
                    r = r - RAPID_TOL  # as camotics_sim.py's rapid check: grazing a wall by the voxel size is not a hit
                rr = r + DMAX
                i0, i1, j0, j1 = S.window(min(p0[0], p1[0]) - rr, max(p0[0], p1[0]) + rr,
                                          min(p0[1], p1[1]) - rr, max(p0[1], p1[1]) + rr)
                if i0 >= i1 or j0 >= j1:
                    continue
                need_s = (not cut or mv["rapid"]) and S.blockmax(i0, i1, j0, j1) > zlo_piece + z0 - DMAX
                need_f = F.blockmax(i0, i1, j0, j1) > zlo_piece + z0 - DMAX
                need_cut = cut and not mv["rapid"]
                if not (need_s or need_f or need_cut):
                    continue
                Xs = x0 + h * np.arange(i0, i1)
                Ys = y0 + h * np.arange(j0, j1)
                X, Y = np.meshgrid(Xs, Ys, indexing="ij")
                m, dist, zt = reach(p0, p1, X, Y, rr)
                if not m.any():
                    continue
                for what, fld, need in (("stock", S, need_s), ("fixture", F, need_f)):
                    if not need:
                        continue
                    top = fld.top[i0:i1, j0:j1]
                    allow = RAPID_TOL if (what == "stock" and cut) else 0.0
                    c = np.where(m & np.isfinite(top), np.maximum(dist - r, zt + z0 + allow - top), np.inf)
                    k = np.unravel_index(np.argmin(c), c.shape)
                    cmin = float(c[k])
                    bp = rec["by_part"].setdefault(part, {})
                    if cmin < bp.get(what, (DMAX, None))[0]:
                        bp[what] = (round(cmin, 2), mv["src_line"])
                    if cmin < rec[what]["c"]:
                        rec[what].update(c=round(cmin, 2), line=mv["src_line"], op=mv["op"], part=part,
                                         at=[round(float(X[k]), 1), round(float(Y[k]), 1)],
                                         tip=[round(float(v), 2) for v in p0])
                        if what == "fixture":
                            rec[what]["what"] = fix_names[int(fix_lab[i0 + k[0], j0 + k[1]])]
                    if cmin < 0:
                        inside = m & (dist <= r)
                        depth = np.where(inside & np.isfinite(top), top - (zt + z0 + allow), -np.inf)
                        hits.append(dict(move=mi, line=mv["src_line"], op=mv["op"], tool=t, rapid=mv["rapid"],
                                         part=part, against=what if what == "stock" else
                                         fix_names[int(fix_lab[i0 + k[0], j0 + k[1]])],
                                         depth_mm=round(float(depth.max()), 2) if inside.any() else 0.0,
                                         p0=[round(float(v), 3) for v in p0], p1=[round(float(v), 3) for v in p1]))
                if need_cut:
                    inside = m & (dist <= r)
                    if inside.any():
                        sub = S.top[i0:i1, j0:j1]
                        np.minimum(sub, np.where(inside, zt, np.inf).astype(np.float32), out=sub)
                        if lower is not None:  # cut through the topmost run: the column's top is the next run's
                            bsub, t2sub = lower[0][i0:i1, j0:j1], lower[1][i0:i1, j0:j1]
                            through = inside & (sub <= bsub)
                            if through.any():
                                sub[through] = np.minimum(t2sub[through], sub[through])
                                bsub[through] = -np.inf
                                t2sub[through] = -np.inf
                        zsub = zc[i0:i1, j0:j1]
                        np.minimum(zsub, np.where(inside, zt, np.inf).astype(np.float32), out=zsub)
                        S.refresh(i0, i1, j0, j1)
    return per_tool, hits


def merge_hits(hits):
    """one record per (move, part of the assembly, object): the deepest"""
    best = {}
    for hh in hits:
        k = (hh["move"], hh["part"], hh["against"])
        if k not in best or hh["depth_mm"] > best[k]["depth_mm"]:
            best[k] = hh
    return sorted(best.values(), key=lambda v: (v["line"], v["part"]))


# --- stock in the part frame (voxels) and its top surface seen from each setup ------------------------------------
def setup_grid(part, res, pad):
    lo = np.array(CS.GRID_LO[part]) - pad
    hi = np.array(CS.GRID_HI[part]) + pad
    return lo, hi


def top_in_setup(stock, grid, rot):
    """top of the voxel stock per setup column: arrays over setup (x', y') and the setup coordinates of the columns"""
    cz = grid.c[2]
    if rot == 0:
        S, cx, cy, cz_s = stock, grid.c[0], grid.c[1], cz
    elif rot == 180:  # (x, -y, -z)
        S, cx, cy, cz_s = stock[:, ::-1, ::-1], grid.c[0], -grid.c[1][::-1], -cz[::-1]
    else:  # -90: (x, z, -y)
        S = np.transpose(stock, (0, 2, 1))[:, :, ::-1]
        cx, cy, cz_s = grid.c[0], grid.c[2], -grid.c[1][::-1]
    any_ = S.any(axis=2)
    nz = S.shape[2]
    k = nz - 1 - np.argmax(S[:, :, ::-1], axis=2)
    top = np.where(any_, cz_s[k] + grid.h / 2, -np.inf).astype(np.float32)
    # the topmost run of material: its bottom, and the top of the next run below it (a web over air, as the floor
    # plate's 2.2 mm ring over the outside A cut through, must empty its column when it is faced off)
    idx = np.arange(nz)[None, None, :]
    gap = (~S) & (idx < k[:, :, None])
    kb = np.where(gap.any(axis=2), nz - 1 - np.argmax(gap[:, :, ::-1], axis=2), -1)  # last air voxel below the top
    bot = np.where(any_, np.where(kb >= 0, cz_s[np.clip(kb + 1, 0, nz - 1)] - grid.h / 2, -np.inf), -np.inf)
    below = S & (idx <= kb[:, :, None])
    k2 = nz - 1 - np.argmax(below[:, :, ::-1], axis=2)
    top2 = np.where(below.any(axis=2), cz_s[k2] + grid.h / 2, -np.inf)
    top_in_setup.lower = (bot.astype(np.float32), top2.astype(np.float32))
    return top, cx, cy, cz_s


def cut_stock(stock, grid, rot, zc_cols):
    """remove every voxel above the setup's cut z-map (zc over the stock's own columns, setup frame)"""
    if rot == 0:
        zs = grid.c[2][None, None, :]
        stock &= ~(zs - grid.h / 2 >= zc_cols[:, :, None] - 1e-6)
    elif rot == 180:
        zc_p = zc_cols[:, ::-1]  # setup y' = -y
        zs = -grid.c[2][None, None, :]
        stock &= ~(zs - grid.h / 2 >= zc_p[:, :, None] - 1e-6)
    else:  # setup (x', y', z') = (x, z, -y); zc over (x', y'=z)
        zs = -grid.c[1][None, :, None]
        stock &= ~(zs - grid.h / 2 >= zc_cols[:, None, :] - 1e-6)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--res", type=float, default=0.5)
    ap.add_argument("--parts", default="frame,floor")
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    h = a.res
    report = dict(method=__doc__.split("Run (")[0].strip(), resolution_mm=h, clearance_cap_mm=DMAX, tight_below_mm=TIGHT,
                  machine=VF4, flange=dict(dia_mm=2 * FLANGE[1], thickness_mm=FLANGE[0]),
                  spindle_assumed=[dict(z_from_gauge_line=list(s[:2]), dia_mm=2 * s[2]) for s in SPINDLE],
                  holders=HOLDERS, cutters={str(t): dict(CUTTERS[t], d=FC.TOOLS[t]["d"],
                                                         stick=CUTTERS[t].get("stick", FC.TOOLS[t]["length"]))
                                            for t in FC.TOOLS},
                  setups={})
    for part in a.parts.split(","):
        grid = CS.Grid(part, h)
        z0, z1 = CS.BLANK_Z[part]
        # the blank less its outermost voxel in x and y: the CAM's edge passes stop within that, and a skin thinner than
        # a voxel standing at the blank's edge would read as a wall
        stock = grid.box(-CS.L / 2 + h, CS.L / 2 - h, -CS.W / 2 + h, CS.W / 2 - h, z0, z1)
        if part == "frame":
            stock &= ~CS.core_mask(grid)
        for su in [s for s in FC.SETUPS if s["part"] == part]:
            t0 = time.time()
            name, rot = su["name"], CS.rot_of(su)
            text = open(IN_DIR / "gcode" / f"{name}.ngc").read()
            _, moves = CS.expand(text)
            table_z, fx, tabs = fixtures(su)
            top_cols, cx, cy, _ = top_in_setup(stock, grid, rot)
            # padded setup grid: the stock's columns plus PAD mm all round (fixtures and the spindle reach)
            pad = int(round(160.0 / h))
            nx, ny = top_cols.shape
            X0, Y0 = cx[0] - pad * h, cy[0] - pad * h
            stock_top = np.full((nx + 2 * pad, ny + 2 * pad), -np.inf, np.float32)
            stock_top[pad:pad + nx, pad:pad + ny] = top_cols
            lower = [np.full(stock_top.shape, -np.inf, np.float32) for _ in range(2)]
            for arr, src in zip(lower, top_in_setup.lower):
                arr[pad:pad + nx, pad:pad + ny] = src
            Xg = X0 + h * np.arange(nx + 2 * pad)
            Yg = Y0 + h * np.arange(ny + 2 * pad)
            XX, YY = np.meshgrid(Xg, Yg, indexing="ij")
            for (bx0, bx1, by0, by1, bz0, bz1) in tabs:  # end tabs: stock the CAM blank does not have
                m = (XX >= bx0) & (XX <= bx1) & (YY >= by0) & (YY <= by1)
                stock_top = np.where(m, np.maximum(stock_top, bz1), stock_top).astype(np.float32)
            fix_top = np.full(XX.shape, -np.inf, np.float32)
            fix_lab = np.zeros(XX.shape, np.int16)
            names = ["-"]
            for nm, kind, p in fx:
                tp = top_of(kind, p, XX, YY)
                names.append(nm)
                upd = tp > fix_top
                fix_lab[upd] = len(names) - 1
                fix_top = np.maximum(fix_top, tp).astype(np.float32)
            zc = np.full(XX.shape, np.inf, np.float32)
            per_tool, hits = sweep(su, moves, stock_top, fix_top, fix_lab, names, X0, Y0, h, zc, lower)
            hits = merge_hits(hits)
            cut_stock(stock, grid, rot, zc[pad:pad + nx, pad:pad + ny])
            # travels: tool-centre span in X and Y, and gauge line above the table
            xs = np.array([[m["p0"][0], m["p1"][0]] for m in moves]).ravel()
            ys = np.array([[m["p0"][1], m["p1"][1]] for m in moves]).ravel()
            travel = dict(table_z_setup=table_z)
            if rot == -90:  # A along machine X: machine X = setup y', machine Y = setup x'
                xs, ys = ys, xs
            travel.update(x_span_mm=round(float(xs.max() - xs.min()), 1), y_span_mm=round(float(ys.max() - ys.min()), 1),
                          x_ok=bool(xs.max() - xs.min() <= VF4["x_travel"]),
                          y_ok=bool(ys.max() - ys.min() <= VF4["y_travel"]))
            zrows = []
            hi_part = float(np.nanmax(np.where(np.isfinite(fix_top), fix_top, -1e9)))
            hi_stock = float(np.nanmax(np.where(np.isfinite(stock_top), stock_top, -1e9)))
            for t in sorted({m["tool"] for m in moves}):
                segs, gl = assembly(t)
                zt = [z for m in moves if m["tool"] == t and not (m is moves[0]) for z in (m["p0"][2], m["p1"][2])]
                lo_, hi_ = min(zt) + gl - table_z, max(zt) + gl - table_z
                home_tip = table_z + VF4["nose_to_table"][1] - gl
                zrows.append(dict(tool=t, gauge_length_mm=round(gl, 2), nose_above_table_min=round(lo_, 1),
                                  nose_above_table_max=round(hi_, 1),
                                  ok=bool(lo_ >= VF4["nose_to_table"][0] and hi_ <= VF4["nose_to_table"][1]),
                                  tip_at_z_home_clears_by_mm=round(home_tip - max(hi_part, hi_stock), 1)))
            travel["z"] = zrows
            tools = {}
            for t, rec in sorted(per_tool.items()):
                c = CUTTERS[t]
                segs, gl = assembly(t)
                tools["T%d" % t] = dict(cutter=FC.TOOLS[t]["name"], bom=c["bom"], holder=c["holder"],
                                        holder_title=HOLDERS[c["holder"]]["title"],
                                        stick_out_mm=round(c.get("stick", FC.TOOLS[t]["length"]), 2),
                                        gauge_length_mm=round(gl, 2),
                                        min_clearance_to_stock_mm=rec["stock"], min_clearance_to_fixtures_mm=rec["fixture"],
                                        by_part={p_: {w: dict(c=v[0], line=v[1]) for w, v in d_.items()}
                                                 for p_, d_ in rec["by_part"].items()},
                                        collisions=sum(1 for hh in hits if hh["tool"] == t),
                                        tight=bool(min(rec["stock"]["c"], rec["fixture"]["c"]) < TIGHT))
            report["setups"][name] = dict(part=part, rot_about_x_deg=rot, moves=len(moves),
                                          fixtures=[dict(name=n, kind=k, params=[round(float(v), 2) for v in p])
                                                    for n, k, p in fx],
                                          end_tabs=tabs, tools=tools, n_collisions=len(hits), collisions=hits[:60],
                                          travel=travel, seconds=round(time.time() - t0, 1))
            print(f"{name}: {len(moves)} moves, {len(hits)} collisions, {time.time() - t0:.0f} s", flush=True)
            for tn, tv in tools.items():
                print("   ", tn, {p_: {w: v["c"] for w, v in d_.items()} for p_, d_ in tv["by_part"].items()}, flush=True)
                print(f"   {tn} {tv['holder']} stick {tv['stick_out_mm']}: stock {tv['min_clearance_to_stock_mm']['c']} "
                      f"(line {tv['min_clearance_to_stock_mm']['line']}, {tv['min_clearance_to_stock_mm']['part']}), "
                      f"fixtures {tv['min_clearance_to_fixtures_mm']['c']} ({tv['min_clearance_to_fixtures_mm']['what']}, "
                      f"line {tv['min_clearance_to_fixtures_mm']['line']}), collisions {tv['collisions']}", flush=True)
            for hh in hits[:8]:
                print("   HIT", hh, flush=True)
            print("   travel", json.dumps(travel), flush=True)
        # cross-check of the stock model: this script's chained stock at the end against CAMotics' (camotics_sim.py's
        # final voxels, same grid), both without the pieces cut free (slugs)
        npz = pathlib.Path(os.environ.get("CAMOTICS_WORK", "/tmp/cam-sim")) / f"{part}_voxels.npz"
        if npz.exists():
            from scipy import ndimage
            z = np.load(npz)
            shape = tuple(z["shape"])
            cam = np.unpackbits(z["final"])[:int(np.prod(shape))].reshape(shape).astype(bool)
            lab, _ = ndimage.label(stock)
            sizes = np.bincount(lab.ravel())
            sizes[0] = 0
            mine = lab == int(np.argmax(sizes))
            del lab
            if cam.shape == mine.shape:
                v = h ** 3 / 1000
                report.setdefault("stock_vs_camotics", {})[part] = dict(
                    camotics_final="$CAMOTICS_WORK/" + npz.name, this_cm3=round(float(mine.sum()) * v, 2),
                    camotics_cm3=round(float(cam.sum()) * v, 2),
                    only_here_cm3=round(float((mine & ~cam).sum()) * v, 2),
                    only_in_camotics_cm3=round(float((cam & ~mine).sum()) * v, 2))
                print(part, "stock vs CAMotics", report["stock_vs_camotics"][part], flush=True)
    pathlib.Path(a.out).write_text(json.dumps(report, indent=1))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
