"""The chamber's posted G-code, parsed, timed and cut, for the robot-build video's machining chapter (round 8, issue
#260, PR #266). Sterling on round 7: "dummy tool paths instead of real ones". Chapter 30 now draws these programs.

Programs (desktop-lpbf/analysis/out/machining/gcode/, regenerated with freecad_cam.py, FreeCAD 1.0.2's linuxcnc post):
frame_B.ngc (F-S1), frame_A.ngc (F-S2), frame_C_haas.nc (F-S3: the four wall indexes joined for a Haas with the A
moves; frame_C0/C90/C180/C270.ngc are the same bodies one index each), floor_A.ngc (P-S1), floor_B.ngc (P-S2).

* Parse: camotics_sim.expand() (G0/G1, G2/G3 helical arcs in G17, G81/G83 expanded into their moves with LinuxCNC's
  0.254 mm peck clearance, T/M6 tool changes, every move tagged with its line in the posted file). The Haas program is
  cut at its "(index A..)" lines and each index parsed on its own (its G53 G00 Z0. / M11 / G00 A / M10 lines are the
  index move: Z to machine home, then A), so no move runs from one index's frame into the next.
* Time: feeds as programmed (length / F), rapids at the VF-4's 25.4 m/min, as freecad_cam.py's recount; arcs split
  so the chord error is under 0.1 mm, each chord carrying its arc's line. Tool changes and A indexes are not timed
  (the recount doesn't either); the chapter shows them with their own stated estimates.
* Cut: in the part frame (mm, model origin), on camotics_sim.Grid's voxel grid. Every setup's tool axis is one of the
  part frame's axes (freecad_cam.json's rotation_model_to_setup: +z for A, -z for B, -y/-x/+y/+x for the wall
  indexes), so within a setup the cut is a height field over the setup's XY: the lowest tool-tip height over each
  column, for a flat-ended cylinder swept along each move (exact for flat end mills and the face mill; drills with
  their 118 deg point). The setup removes every voxel above its field (the tool and its holder come in from above).
  The programs' stock is freecad_cam.py's: the 317.5 x 228.6 x 127 frame blank with the 274 x 184 (R7) core already
  cut out by waterjet, and the 317.5 x 228.6 x 25.4 floor blank.

    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/gcode_sim.py [--res 0.75]
        -> desktop-lpbf/analysis/out/videoqa/gcode_sim.json (minutes per setup against freecad_cam.json, removed
           volume against the CAD, gouge and leftover against the part's own STL voxelised on the same grid)
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import re
import sys
import time

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
LPBF = HERE.parents[1]
MACH = LPBF / "analysis" / "machining"
if str(MACH) not in sys.path:
    sys.path.insert(0, str(MACH))
import camotics_sim as CS  # noqa: E402  (plain Python: the parser, the grid, the voxeliser)
import freecad_cam as FC  # noqa: E402  (plain Python: TOOLS, rot_matrix, the recount gcode_times)

GDIR = LPBF / "analysis" / "out" / "machining" / "gcode"
FCJ = LPBF / "analysis" / "out" / "machining" / "freecad_cam.json"
OUT_JSON = LPBF / "analysis" / "out" / "videoqa" / "gcode_sim.json"
RAPID = FC.RAPID_MM_MIN                       # 25.4 m/min, the VF-4's X/Y/Z rapid
CHORD = 0.1                                   # mm, arc chord error
DRILL_K = 1.0 / math.tan(math.radians(59.0))  # a 118 deg point: the cone rises 0.60 mm per mm of radius
HAAS = "frame_C_haas.nc"
ORDER = {"frame": ["frame_B", "frame_A", "frame_C0", "frame_C90", "frame_C180", "frame_C270"],
         "floor": ["floor_A", "floor_B"]}
PLAN_ID = {"frame_B": "F-S1", "frame_A": "F-S2", "frame_C0": "F-S3", "frame_C90": "F-S3", "frame_C180": "F-S3",
           "frame_C270": "F-S3", "floor_A": "P-S1", "floor_B": "P-S2"}


def fc_json():
    return json.loads(FCJ.read_text())


def setup_meta(name):
    for p in fc_json()["parts"].values():
        for s in p["setups"]:
            if s["setup"] == name:
                return s
    raise KeyError(name)


def rot_of(name):
    """model -> setup rotation (rows: setup x, y, z in model coordinates), freecad_cam.json's"""
    return np.array(setup_meta(name)["rotation_model_to_setup"], float)


def tools():
    """T number -> dict(d, length, shape, name) from freecad_cam.json's "tools" (FC.TOOLS as posted)"""
    out = {}
    for k, v in fc_json()["tools"].items():
        out[int(k.lstrip("T"))] = dict(d=float(v["d"]), length=float(v["length"]), shape=v["shape"], name=v["name"])
    return out


# ------------------------------------------------------------------------------------------------ programs
def haas_chunks(text):
    """The Haas program cut at its "(index A<deg>: ...)" lines: {a_deg: (first line, last line, home line, a line)}
    (1-based line numbers in the file)."""
    lines = text.splitlines()
    starts = [(i + 1, int(m.group(1))) for i, ln in enumerate(lines) for m in [re.match(r"\(index A(\d+):", ln)] if m]
    out = {}
    for k, (l0, a) in enumerate(starts):
        l1 = starts[k + 1][0] - 1 if k + 1 < len(starts) else len(lines)
        home = next(i for i in range(l0, l1 + 1) if lines[i - 1].strip().startswith("G53"))
        aline = next(i for i in range(l0, l1 + 1) if re.match(r"G0?0 A", lines[i - 1].strip()))
        out[a] = (l0, l1, home, aline)
    return out


class Program:
    """One setup's program as timed chords. Arrays (n chords): p0, p1 (work = setup coordinates), dur (s), t0, t1,
    s1 (path length at the chord's end), rapid, tool, line (in `src`), op (index into ops)."""

    def __init__(self, name):
        self.name = name
        self.rot = rot_of(name)
        if name.startswith("frame_C"):
            self.src = HAAS
            full = (GDIR / HAAS).read_text()
            a = int(name[len("frame_C"):])
            l0, l1, home, aline = haas_chunks(full)[a]
            lines = full.splitlines()
            # keep the file's line numbers: blank lines before and after this index's chunk; the index move itself
            # (G53 Z home, M11, G0 A, M10) is not a cutting move and is drawn by the chapter
            keep = [ln if l0 <= i + 1 <= l1 else "" for i, ln in enumerate(lines)]
            keep[home - 1] = "(index move: Z to machine home)"
            keep[aline - 1] = "(index move: A)"
            text = "\n".join(keep)
            self.a_deg, self.index_lines = a, dict(home=home, a=aline, first=l0, last=l1)
        else:
            self.src = f"{name}.ngc"
            text = (GDIR / self.src).read_text()
            self.a_deg, self.index_lines = None, None
        self.text = text
        _, moves = CS.expand(text)
        T = tools()
        p0, p1, dur, rapid, tool, line, op = [], [], [], [], [], [], []
        self.ops = []
        opi = {}
        for mv in moves:
            if mv["tool"] is None:
                continue
            pts = CS.segments(mv, chord=CHORD)
            o = opi.setdefault(mv["op"], len(opi))
            if o == len(self.ops):
                self.ops.append(mv["op"])
            for a_, b_ in zip(pts[:-1], pts[1:]):
                d = float(np.linalg.norm(b_ - a_))
                if d < 1e-9:
                    continue
                v = RAPID if mv["rapid"] else (mv["feed"] or RAPID)
                p0.append(a_)
                p1.append(b_)
                dur.append(d / v * 60.0)
                rapid.append(mv["rapid"])
                tool.append(mv["tool"])
                line.append(mv["src_line"])
                op.append(o)
        self.p0, self.p1 = np.array(p0), np.array(p1)
        self.dur = np.array(dur)
        self.t1 = np.cumsum(self.dur)
        self.t0 = self.t1 - self.dur
        L = np.linalg.norm(self.p1 - self.p0, axis=1)
        self.len = L
        self.s1 = np.cumsum(L)
        self.rapid = np.array(rapid, bool)
        self.tool = np.array(tool, int)
        self.line = np.array(line, int)
        self.op = np.array(op, int)
        self.total_s = float(self.t1[-1])
        self.radius = np.array([T[t]["d"] / 2 for t in self.tool])
        self.cone = np.array([DRILL_K if T[t]["shape"] == "drill" else 0.0 for t in self.tool])
        self.T = T

    def index(self, t):
        return int(min(np.searchsorted(self.t1, t, side="left"), len(self.t1) - 1))

    def at(self, t):
        """(position in work coordinates, chord index) at time t (s from the program's start)"""
        i = self.index(t)
        f = 0.0 if self.dur[i] <= 0 else min(max((t - self.t0[i]) / self.dur[i], 0.0), 1.0)
        return self.p0[i] + (self.p1[i] - self.p0[i]) * f, i

    def trail(self, t, length=220.0, feed_only=True):
        """The path just run (work coordinates), up to `length` mm back from the position at t: (k, 3) points."""
        pos, i = self.at(t)
        s_now = self.s1[i] - self.len[i] + np.linalg.norm(pos - self.p0[i])
        j = int(np.searchsorted(self.s1, s_now - length, side="left"))
        pts = [self.p0[k] for k in range(j, i + 1)] + [pos]
        if feed_only:
            keep = [not self.rapid[k] for k in range(j, i + 1)] + [not self.rapid[i]]
            pts = [p for p, kp in zip(pts, keep) if kp]
        return np.array(pts) if len(pts) >= 2 else None

    def recount(self):
        """freecad_cam.gcode_times on the posted text (the recount freecad_cam.json holds), and this timeline's own sums"""
        if self.src == HAAS:
            text = (GDIR / f"{self.name}.ngc").read_text() if (GDIR / f"{self.name}.ngc").exists() else self.text
        else:
            text = self.text
        ops, n_tc = FC.gcode_times(text)
        feed_mm = sum(v["feed_mm"] for v in ops.values())
        rapid_mm = sum(v["rapid_mm"] for v in ops.values())
        tot_s = sum(v["feed_s"] + v["rapid_s"] for v in ops.values())
        return dict(recount_min=round(tot_s / 60, 2), path_feed_mm=round(feed_mm, 1), path_rapid_mm=round(rapid_mm, 1),
                    timeline_min=round(self.total_s / 60, 2),
                    timeline_feed_mm=round(float(self.len[~self.rapid].sum()), 1),
                    timeline_rapid_mm=round(float(self.len[self.rapid].sum()), 1),
                    chords=int(len(self.dur)), program_lines=int(len(set(self.line.tolist()))))


# ------------------------------------------------------------------------------------------------ the cut
try:
    import numba

    @numba.njit(cache=False)
    def _stamp(H, u0, v0, h, P0, P1, R, K):
        nu, nv = H.shape
        for s in range(P0.shape[0]):
            a0, b0, w0 = P0[s, 0], P0[s, 1], P0[s, 2]
            a1, b1, w1 = P1[s, 0], P1[s, 1], P1[s, 2]
            r = R[s]
            k = K[s]
            i0 = max(int(math.floor((min(a0, a1) - r - u0) / h)), 0)
            i1 = min(int(math.floor((max(a0, a1) + r - u0) / h)) + 1, nu)
            j0 = max(int(math.floor((min(b0, b1) - r - v0) / h)), 0)
            j1 = min(int(math.floor((max(b0, b1) + r - v0) / h)) + 1, nv)
            du, dv = a1 - a0, b1 - b0
            L2 = du * du + dv * dv
            for i in range(i0, i1):
                cu = u0 + (i + 0.5) * h
                for j in range(j0, j1):
                    cv = v0 + (j + 0.5) * h
                    fx, fy = cu - a0, cv - b0
                    c = fx * fx + fy * fy - r * r
                    if L2 < 1e-12:
                        if c <= 0.0:
                            z = min(w0, w1) + k * math.sqrt(fx * fx + fy * fy)
                            if z < H[i, j]:
                                H[i, j] = z
                        continue
                    b = fx * du + fy * dv
                    disc = b * b - L2 * c
                    if disc < 0.0:
                        continue
                    sq = math.sqrt(disc)
                    t1 = max((b - sq) / L2, 0.0)
                    t2 = min((b + sq) / L2, 1.0)
                    if t1 > t2:
                        continue
                    z = min(w0 + t1 * (w1 - w0), w0 + t2 * (w1 - w0))
                    if z < H[i, j]:
                        H[i, j] = z
except ImportError:  # pragma: no cover
    _stamp = None


def make_grid(part, res):
    """camotics_sim.Grid shifted by 0.137 voxel, so that no voxel centre lies on a programmed plane (setups A and B both
    cut the frame's outside to z 58: centres on z 58 would be left as a one-voxel film between them)"""
    g = CS.Grid(part, res)
    g.lo = g.lo + 0.137 * res
    g.c = [g.lo[a] + (np.arange(g.n[a]) + 0.5) * res for a in range(3)]
    return g


def drop_free(occ):
    """Pieces cut free (slugs from through trepans and slots) drop out: keep the largest connected piece. Returns
    (occupancy, [freed cm3 per voxel])."""
    from scipy import ndimage
    lab, n = ndimage.label(occ)
    if n <= 1:
        return occ, []
    sizes = np.bincount(lab.ravel())[1:]
    keep = int(np.argmax(sizes)) + 1
    freed = [int(v) for i, v in enumerate(sizes) if i + 1 != keep]
    return lab == keep, freed


def stock0(part, grid):
    """freecad_cam.py's stock on the grid: the blank box (the frame with the waterjet core out)"""
    z0, z1 = CS.BLANK_Z[part]
    s = grid.box(-CS.L / 2, CS.L / 2, -CS.W / 2, CS.W / 2, z0, z1)
    if part == "frame":
        s &= ~CS.core_mask(grid)
    return s


class Cutter:
    """One setup's cut on a part grid, advanced in time: H is the height field (setup frame) of the lowest tool tip
    so far; occupancy() is the stock at the setup's start less everything above H."""

    def __init__(self, prog, grid, stock):
        self.p, self.g, self.stock = prog, grid, stock
        self.cs = CS.setup_coords(grid, prog.rot)
        h = grid.h
        self.u0 = self.cs[0][0] - h / 2
        self.v0 = self.cs[1][0] - h / 2
        self.H = np.full((len(self.cs[0]), len(self.cs[1])), np.inf)
        self.k = 0                     # chords stamped in full
        self.t = 0.0

    def advance(self, t):
        p = self.p
        i = p.index(t)
        if i > self.k:
            sl = slice(self.k, i)
            _stamp(self.H, self.u0, self.v0, self.g.h, p.p0[sl], p.p1[sl], p.radius[sl], p.cone[sl])
            self.k = i
        pos, _ = p.at(t)
        _stamp(self.H, self.u0, self.v0, self.g.h, p.p0[i:i + 1], pos[None, :], p.radius[i:i + 1], p.cone[i:i + 1])
        if t >= p.t1[i] - 1e-9:
            self.k = max(self.k, i + 1)
        self.t = t

    def finish(self):
        self.advance(self.p.total_s + 1.0)

    def occupancy(self):
        out = self.stock.copy()
        v = CS.setup_view(out, self.p.rot)
        v &= ~(self.cs[2][None, None, :] > self.H[:, :, None])
        return out


def occ_mesh(occ, grid, sigma=0.6):
    """A smooth surface of a voxel occupancy (part frame): lightly blurred, contoured at 0.5."""
    import pyvista as pv
    from scipy import ndimage
    a = np.zeros(tuple(np.array(occ.shape) + 2), np.float32)
    a[1:-1, 1:-1, 1:-1] = occ
    if sigma:
        a = ndimage.gaussian_filter(a, sigma)
    img = pv.ImageData(dimensions=a.shape, spacing=(grid.h,) * 3,
                       origin=tuple(grid.c[k][0] - grid.h for k in range(3)))
    img.point_data["o"] = a.ravel(order="F")
    m = img.contour([0.5], scalars="o", method="flying_edges")
    return m


# ------------------------------------------------------------------------------------------------ the check
def check(res=0.75):
    t0 = time.time()
    fc = fc_json()
    out = dict(what="the chamber's posted programs parsed, timed and cut in the part frame (cad/robotbuild/gcode_sim.py)",
               generated_utc=time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime()), resolution_mm=res,
               rapid_mm_min=RAPID, timing="feeds as programmed, rapids at 25.4 m/min; tool changes and A indexes "
               "not timed (as freecad_cam.py's recount)", cutter="flat-ended cylinders swept along every move "
               "(drills with a 118 deg point), the tool and holder coming in along the setup's tool axis",
               stock="freecad_cam.py's: frame 317.5 x 228.6 x 127 with the 274 x 184 R7 core out (waterjet), floor "
               "317.5 x 228.6 x 25.4", setups={}, parts={})
    inv = json.loads(pathlib.Path(os.environ.get("CHAMBER_CAM_IN", "/tmp/chamber-cam"), "parts.json").read_text()) \
        if pathlib.Path(os.environ.get("CHAMBER_CAM_IN", "/tmp/chamber-cam"), "parts.json").exists() else None
    for part, names in ORDER.items():
        grid = make_grid(part, res)
        stock = stock0(part, grid)
        initial = stock.copy()
        stl = pathlib.Path(os.environ.get("CHAMBER_CAM_IN", "/tmp/chamber-cam")) / f"{part}.stl"
        tgt = CS.voxelize(CS.read_stl(str(stl)), grid) if stl.exists() else None
        for name in names:
            p = Program(name)
            c = Cutter(p, grid, stock)
            c.finish()
            new, freed = drop_free(c.occupancy())
            removed = float((stock & ~new).sum()) * res ** 3 / 1000.0
            rc = p.recount()
            ref = next(s for s in fc["parts"][part]["setups"] if s["setup"] == name)["totals"]
            row = dict(program=f"analysis/out/machining/gcode/{p.src}", plan_setup=PLAN_ID[name], **rc,
                       freecad_cam_json_min=ref["total_min"], freecad_cam_json_feed_mm=ref["path_feed_mm"],
                       freecad_cam_json_rapid_mm=ref["path_rapid_mm"],
                       recount_vs_json_min=round(rc["recount_min"] - ref["total_min"], 2),
                       timeline_vs_json_min=round(rc["timeline_min"] - ref["total_min"], 2),
                       removed_cm3=round(removed, 2), tools=sorted(set(int(t) for t in p.tool)),
                       slugs_dropped_cm3=[round(v * res ** 3 / 1000, 2) for v in sorted(freed, reverse=True)
                                          if v * res ** 3 > 50.0])
            if p.index_lines:
                row["haas_index_lines"] = p.index_lines
            if tgt is not None:
                row["gouge_cm3"] = round(float((stock & ~new & tgt).sum()) * res ** 3 / 1000.0, 3)
            out["setups"][name] = row
            print(name, row, flush=True)
            stock = new
        prt = dict(setups=names, initial_stock_cm3=round(float(initial.sum()) * res ** 3 / 1000, 1),
                   final_cm3=round(float(stock.sum()) * res ** 3 / 1000, 1))
        prt["removed_sim_cm3"] = round(prt["initial_stock_cm3"] - prt["final_cm3"], 1)
        if tgt is not None:
            prt["part_voxels_cm3"] = round(float(tgt.sum()) * res ** 3 / 1000, 1)
            prt["removed_cad_cm3"] = round(float((initial & ~tgt).sum()) * res ** 3 / 1000, 1)
            prt["removed_sim_vs_cad_pct"] = round(100.0 * (prt["removed_sim_cm3"] - prt["removed_cad_cm3"])
                                                  / max(prt["removed_cad_cm3"], 1e-9), 2)
            prt["leftover_cm3"] = round(float((stock & ~tgt).sum()) * res ** 3 / 1000, 2)
            prt["gouge_cm3"] = round(float((~stock & tgt & initial).sum()) * res ** 3 / 1000, 3)
            from scipy import ndimage
            for k in (1, 2):           # more than k voxels from the model's surface (voxel steps left out)
                far_out = stock & ~ndimage.binary_dilation(tgt, iterations=k)
                deep_in = ndimage.binary_erosion(tgt, iterations=k) & ~stock
                prt[f"leftover_beyond_{k * res:g}mm_cm3"] = round(float(far_out.sum()) * res ** 3 / 1000, 3)
                prt[f"gouge_beyond_{k * res:g}mm_cm3"] = round(float(deep_in.sum()) * res ** 3 / 1000, 3)
                if k == 2:
                    lab, n = ndimage.label(far_out)
                    if n:
                        sizes = np.bincount(lab.ravel())[1:]
                        big = np.argsort(sizes)[::-1][:6]
                        sl = ndimage.find_objects(lab)
                        prt["leftover_largest"] = [
                            dict(cm3=round(float(sizes[b]) * res ** 3 / 1000, 3),
                                 bbox_mm=[round(float(grid.c[a][s_.start]), 1) for a, s_ in enumerate(sl[b])]
                                 + [round(float(grid.c[a][s_.stop - 1]), 1) for a, s_ in enumerate(sl[b])])
                            for b in big]
                    del lab
                del far_out, deep_in
            prt["note"] = ("leftover: stock the programs leave that the model doesn't have (taps, STI threads, reamed "
                           "dowel holes, chamfers and other features not programmed, plus voxel steps); gouge: "
                           "model volume the programs cut (voxel steps at walls)")
        if inv:
            key = "process_chamber_body" if part == "frame" else "chamber_floor_plate"
            row = next((r for r in inv["parts"] if r["slug"].startswith(key)), None)
            if row:
                prt["cad_part_cm3"] = round(row["volume_mm3"] / 1000, 1)
                z0, z1 = CS.BLANK_Z[part]
                blank = CS.L * CS.W * (z1 - z0)
                if part == "frame":
                    Lc, Wc, R = CS.CORE
                    blank -= (Lc * Wc - (4 - math.pi) * R * R) * (z1 - z0)
                prt["cad_blank_cm3"] = round(blank / 1000, 1)
                prt["removed_exact_cad_cm3"] = round(prt["cad_blank_cm3"] - prt["cad_part_cm3"], 1)
                prt["blank_kg_6061"] = round(blank / 1000 * 2.70 / 1000, 2)
                prt["part_kg_6061"] = round(prt["cad_part_cm3"] * 2.70 / 1000, 2)
        out["parts"][part] = prt
        print(part, prt, flush=True)
    out["seconds"] = round(time.time() - t0, 1)
    return out


def regen_compare(new_json, out_path):
    """freecad_cam.py re-run (its JSON written elsewhere with $FREECAD_CAM_JSON) against the committed freecad_cam.json:
    per setup and op, the recount's minutes and path lengths, and the posted files' sha256."""
    import hashlib
    old, new = fc_json(), json.loads(pathlib.Path(new_json).read_text())
    rows = {}
    for part, p in old["parts"].items():
        for s in p["setups"]:
            n = next(x for x in new["parts"][part]["setups"] if x["setup"] == s["setup"])
            a, b = s["totals"], n["totals"]
            ops = []
            for o, q in zip(s["ops"], n["ops"]):
                if o.get("label") != q.get("label"):
                    ops.append(dict(label=o.get("label"), new_label=q.get("label")))
                    continue
                d = {k: round((q.get(k) or 0) - (o.get(k) or 0), 3) for k in ("cut_time_min", "rapid_time_min")
                     if k in o}
                if any(abs(v) > 0 for v in d.values()):
                    ops.append(dict(label=o["label"], **d))
            g = GDIR / f"{s['setup']}.ngc"
            rows[s["setup"]] = dict(
                committed_total_min=a["total_min"], regenerated_total_min=b["total_min"],
                d_min=round(b["total_min"] - a["total_min"], 3),
                committed_feed_mm=a["path_feed_mm"], regenerated_feed_mm=b["path_feed_mm"],
                d_feed_mm=round(b["path_feed_mm"] - a["path_feed_mm"], 1),
                committed_rapid_mm=a["path_rapid_mm"], regenerated_rapid_mm=b["path_rapid_mm"],
                d_rapid_mm=round(b["path_rapid_mm"] - a["path_rapid_mm"], 1),
                tool_changes=[a["tool_changes"], b["tool_changes"]], ops_that_differ=ops,
                ngc_sha256=hashlib.sha256(g.read_bytes()).hexdigest() if g.exists() else None)
    h = GDIR / HAAS
    out = dict(what="freecad_cam.py re-run on 2026-11-26 (FreeCAD 1.0.2 conda AppImage, sha256 checked against the "
                    "release's SHA256 file) against the committed analysis/out/machining/freecad_cam.json; the "
                    "re-posted programs are the ones in analysis/out/machining/gcode/",
               freecad=new.get("tool"), inputs="inventory.py's frame and floor BREPs and parts.json, built 2026-11-26",
               setups=rows, haas_program_sha256=hashlib.sha256(h.read_bytes()).hexdigest(),
               note="FreeCAD's Adaptive op is not bit-for-bit repeatable (a re-post moves its paths by ~0.01 mm, "
                    "freecad_cam.py's docstring): frame_B and floor_B changed by a few tenths of a percent in feed "
                    "length; every other setup is identical in minutes and path lengths. freecad_cam.json is left as "
                    "it was.")
    pathlib.Path(out_path).write_text(json.dumps(out, indent=1))
    return out


def verify_frames(frames_json=None):
    """Independent check of a render's cutting frames (shop_chapters.py writes analysis/out/videoqa/gcode_frames.json):
    re-parse each program and confirm that every drawn cutter position lies on the chords of the program line the
    frame names (distance under 0.001 mm), and that its time is in the program's run."""
    fj = pathlib.Path(frames_json or (LPBF / "analysis" / "out" / "videoqa" / "gcode_frames.json"))
    data = json.loads(fj.read_text())
    out = {}
    progs = {}
    for ch, d in data.items():
        worst, bad, n, good = 0.0, [], 0, 0
        for r in d["rows"]:
            p = progs.get(r["setup"]) or progs.setdefault(r["setup"], Program(r["setup"]))
            ks = np.nonzero(p.line == r["line"])[0]
            q = np.array(r["work_xyz"], float)
            best = math.inf
            for k in ks:
                a, b = p.p0[k], p.p1[k]
                ab = b - a
                t = float(np.clip((q - a) @ ab / max(ab @ ab, 1e-12), 0.0, 1.0))
                best = min(best, float(np.linalg.norm(a + t * ab - q)))
            n += 1
            worst = max(worst, best)
            if best < 1e-3 and 0.0 <= r["t_s"] <= p.total_s + 1e-6:
                good += 1
            elif len(bad) < 5:
                bad.append(dict(frame=r["chapter_frame"], program=r["program"], line=r["line"], off_mm=best))
        out[ch] = dict(frames=n, on_their_program_line=good,
                       worst_off_line_mm=round(worst, 6), problems=bad, out_of_travel=d.get("out_of_travel"),
                       programs=d.get("programs"), minutes=d.get("minutes"),
                       statement=("every drawn cutter position is interpolated on a line of a posted program: "
                                  "re-parsed, each frame's position lies on the chords of the line it names")
                       if good == n else "SOME FRAMES ARE OFF THEIR LINE (see problems)")
    res = json.loads(OUT_JSON.read_text()) if OUT_JSON.exists() else {}
    res["drawn_frames"] = dict(source=str(fj.relative_to(LPBF)), chapters=out)
    OUT_JSON.write_text(json.dumps(res, indent=1))
    return out


def main(argv):
    if "--verify-frames" in argv:
        print(json.dumps(verify_frames(), indent=1))
        return
    if "--regen-compare" in argv:
        i = argv.index("--regen-compare")
        out = regen_compare(argv[i + 1], argv[i + 2])
        for k, v in out["setups"].items():
            print(k, v["committed_total_min"], v["regenerated_total_min"], v["d_feed_mm"], v["d_rapid_mm"])
        return
    res = 0.75
    if "--res" in argv:
        res = float(argv[argv.index("--res") + 1])
    out = check(res)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    old = json.loads(OUT_JSON.read_text()) if OUT_JSON.exists() else {}
    old.update(out)
    OUT_JSON.write_text(json.dumps(old, indent=1))
    print("wrote", OUT_JSON)


if __name__ == "__main__":
    main(sys.argv[1:])
