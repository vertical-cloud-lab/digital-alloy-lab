"""Check every posted program by cutting it on a voxel model of the blank (#260, PR 294 round 2).

The same idea as PR 266's gcode_sim.py, in a simpler form: each setup's tool axis is one of the piece's axes, so a
setup's cut is a height field over the setup's XY (the lowest point the tool reaches over each column, for a flat end
mill swept exactly along each linear move, drills and the spot drill with their cone). Everything above that field is
removed (tool and holder come from above). Setups run in order on one voxel grid in the part frame.

Inputs: /tmp/ft-fab/pieces/<pid>_start.stl (the blank, or the turned piece / bought plate the mill starts from),
<pid>.stl (the finished piece) or <pid>_target.stl (the piece plus what the lathe removes later), fab/out/cam.json and
fab/gcode/*.ngc. Parsing reuses camotics_sim.expand() (G0/G1/G2/G3, G81/G83 expanded the way LinuxCNC runs them).

Reported per piece: volume removed against blank - target, gouges (target voxels removed, and how deep), material
left (stock voxels left that are not the target, and how thick), and rapid moves that pass through the target.

    /tmp/tools/capmem 3 /tmp/venv/bin/python desktop-lpbf/fast-track/fab/sim.py [pid ...]  -> fab/out/sim.json, img
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time

import numpy as np
from scipy import ndimage

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "analysis" / "machining"))
import camotics_sim as CS  # noqa: E402
import tools as T  # noqa: E402

SCR = pathlib.Path("/tmp/ft-fab")
OUT = HERE / "out"
ROT = {"+Z": ((1, 0, 0), (0, 1, 0), (0, 0, 1)), "-Z": ((1, 0, 0), (0, -1, 0), (0, 0, -1)),
       "+X": ((0, 1, 0), (0, 0, 1), (1, 0, 0)), "-X": ((0, -1, 0), (0, 0, 1), (-1, 0, 0)),
       "+Y": ((1, 0, 0), (0, 0, -1), (0, 1, 0)), "-Y": ((-1, 0, 0), (0, 0, -1), (0, -1, 0))}
MAX_VOX = 12e6


class Grid:
    def __init__(self, lo, hi, res):
        self.lo = np.array(lo, float)
        self.h = res
        self.n = np.maximum(1, np.round((np.array(hi, float) - self.lo) / res).astype(int))
        self.hi = self.lo + self.n * res
        self.c = [self.lo[a] + (np.arange(self.n[a]) + 0.5) * res for a in range(3)]


def tool_k(t):
    v = T.TOOLS[t]
    if v["shape"] == "drill":
        return 1.0 / math.tan(math.radians(59.0))
    if v["shape"] == "chamfer":
        return 1.0 / math.tan(math.radians(v.get("angle", 90.0) / 2))
    return 0.0


def stamp_segment(H, cx, cy, a, b, r, k):
    """lower envelope of a tool of radius r (cone slope k: z = tip + k * rho) moving linearly from a to b"""
    xlo, xhi = min(a[0], b[0]) - r, max(a[0], b[0]) + r
    ylo, yhi = min(a[1], b[1]) - r, max(a[1], b[1]) + r
    i0, i1 = np.searchsorted(cx, xlo), np.searchsorted(cx, xhi, side="right")
    j0, j1 = np.searchsorted(cy, ylo), np.searchsorted(cy, yhi, side="right")
    if i0 >= i1 or j0 >= j1:
        return
    X = cx[i0:i1][:, None]
    Y = cy[j0:j1][None, :]
    dx, dy, dz = b[0] - a[0], b[1] - a[1], b[2] - a[2]
    L2 = dx * dx + dy * dy
    if k > 0 or L2 < 1e-12:
        # plunge (drills, spot drill, vertical end-mill moves): the lowest tip
        if L2 > 1e-12:          # a coned tool moving sideways: sample it
            n = int(math.ceil(math.sqrt(L2) / 0.1)) + 1
            for s in np.linspace(0, 1, n):
                stamp_segment(H, cx, cy, (a[0] + s * dx, a[1] + s * dy, a[2] + s * dz),
                              (a[0] + s * dx, a[1] + s * dy, a[2] + s * dz), r, k)
            return
        rho = np.sqrt((X - a[0]) ** 2 + (Y - a[1]) ** 2)
        z = np.where(rho <= r, min(a[2], b[2]) + k * rho, np.inf)
    else:
        # flat tool: cells within r of the axis for t in [t1, t2] (quadratic in t); z linear in t -> min at an end
        px, py = X - a[0], Y - a[1]
        tc = (px * dx + py * dy) / L2
        d2 = px * px + py * py - tc * tc * L2               # squared distance to the infinite line
        inside = d2 <= r * r
        half = np.sqrt(np.maximum(r * r - d2, 0.0) / L2)
        t1 = np.clip(tc - half, 0.0, 1.0)
        t2 = np.clip(tc + half, 0.0, 1.0)
        ok = inside & (t1 <= t2) & (tc + half >= 0.0) & (tc - half <= 1.0)
        z = np.where(ok, np.minimum(a[2] + t1 * dz, a[2] + t2 * dz), np.inf)
    sub = H[i0:i1, j0:j1]
    np.minimum(sub, z, out=sub)


def program_moves(path):
    text = pathlib.Path(path).read_text()
    _, moves = CS.expand(text)
    return moves


def piece_grid(start_tris, res=None):
    lo = start_tris.reshape(-1, 3).min(0) - 1.5
    hi = start_tris.reshape(-1, 3).max(0) + 1.5
    vol = float(np.prod(hi - lo))
    if res is None:
        res = float(np.clip((vol / MAX_VOX) ** (1 / 3), 0.12, 1.0))
    return Grid(lo, hi, res)


def run_piece(pc, setups, gdir):
    pid = pc["pid"]
    st = CS.read_stl(str(SCR / "pieces" / (pid + "_start.stl")))
    tgt_p = SCR / "pieces" / (pid + "_target.stl")
    tg = CS.read_stl(str(tgt_p if tgt_p.exists() else SCR / "pieces" / (pid + ".stl")))
    g = piece_grid(st)
    occ = CS.voxelize(st, g)
    target = CS.voxelize(tg, g)
    start = occ.copy()
    target_core = ndimage.binary_erosion(target, iterations=2)    # rapids: hits deeper than 2 voxels only
    vox = g.h ** 3 / 1000.0
    out = dict(pid=pid, res_mm=round(g.h, 3), grid=[int(v) for v in g.n], setups=[])
    rapid_hits = []
    for su in setups:
        if not su.get("gcode"):
            continue
        rot = np.array(ROT[su["up"]], float)
        view = CS.setup_view(occ, rot)
        cx, cy, cz = CS.setup_coords(g, rot)
        H = np.full((len(cx), len(cy)), np.inf)
        moves = program_moves(HERE / su["gcode"])
        t0 = time.time()
        n_seg = 0
        Htgt_rapid = []
        for mv in moves:
            t = mv["tool"]
            if t is None:
                continue
            r = T.TOOLS[t]["d"] / 2
            k = tool_k(t)
            pts = CS.segments(mv, chord=0.05)
            if mv["rapid"]:
                Htgt_rapid.append((pts, r, k, mv))
                continue
            for a, b in zip(pts[:-1], pts[1:]):
                stamp_segment(H, cx, cy, a, b, r, k)
                n_seg += 1
        tm = CS.camotics_times(moves)
        t_min = sum(o["feed_s"] + o["vf4_rapid_s"] for o in tm.values()) / 60.0
        before = int(view.sum())
        mask = cz[None, None, :] > H[:, :, None]
        view[mask] = False
        removed = before - int(view.sum())
        # rapids: lowest envelope of the rapid moves against the target (a rapid through the finished piece is a crash)
        tview = CS.setup_view(target_core, rot)
        hits = 0
        ops_hit = {}
        for pts, r, k, mv in Htgt_rapid:
            Hr = np.full((len(cx), len(cy)), np.inf)
            for a, b in zip(pts[:-1], pts[1:]):
                stamp_segment(Hr, cx, cy, a, b, r, k)
            if np.isfinite(Hr).any():
                m = cz[None, None, :] > Hr[:, :, None] + g.h
                if (m & tview).any():
                    hits += 1
                    ops_hit[mv["op"]] = ops_hit.get(mv["op"], 0) + 1
        if hits:
            rapid_hits.append(dict(setup=su["setup"], rapids_through_target=hits, ops=ops_hit))
        out["setups"].append(dict(setup=su["setup"], up=su["up"], segments=n_seg, removed_cm3=round(removed * vox, 2),
                                  minutes_from_moves=round(t_min, 2), minutes_recount=su["total_min"],
                                  minutes_freecad=su["freecad_cycle_min"],
                                  stamp_s=round(time.time() - t0, 1), rapid_moves_through_target=hits))
    # free slugs (stock cut loose by a through profile, e.g. an opening's core) drop out of the vise: keep only the
    # material still joined to the piece
    lab, nlab = ndimage.label(occ)
    keep = np.unique(lab[target & occ])
    slugs = occ & ~np.isin(lab, keep[keep > 0])
    slug_cm3 = float(slugs.sum()) * g.h ** 3 / 1000.0
    occ &= ~slugs
    removed = start & ~occ
    expect = start & ~target
    gouge = removed & target
    left = occ & ~target
    # depth of gouges into the target, thickness of what is left (distance transforms, mm)
    dt_in = ndimage.distance_transform_edt(target) * g.h if gouge.any() else None
    deep_gouge = float(dt_in[gouge].max()) if gouge.any() else 0.0
    dt_left = ndimage.distance_transform_edt(left) * g.h if left.any() else None
    thick_left = float(dt_left[left].max()) * 2 if left.any() else 0.0
    # gouges deeper than 1.5 voxels are real; shallower ones are voxel noise on surfaces
    real_g = gouge & (dt_in > 1.5 * g.h) if gouge.any() else gouge
    real_l = left & (dt_left > 1.5 * g.h) if left.any() else left
    out.update(start_cm3=round(start.sum() * vox, 2), target_cm3=round(target.sum() * vox, 2),
               expected_removal_cm3=round(expect.sum() * vox, 2), removed_cm3=round(removed.sum() * vox, 2),
               removed_pct_of_expected=round(100.0 * removed.sum() / max(1, expect.sum()), 1),
               gouge_cm3=round(gouge.sum() * vox, 3), gouge_deep_cm3=round(real_g.sum() * vox, 3),
               gouge_max_depth_mm=round(deep_gouge, 2), left_cm3=round(left.sum() * vox, 3),
               left_thick_cm3=round(real_l.sum() * vox, 3), left_max_thickness_mm=round(thick_left, 2),
               rapid_hits=rapid_hits, slugs_dropped_cm3=round(slug_cm3, 2))
    (SCR / "simmask").mkdir(exist_ok=True)
    np.savez_compressed(SCR / "simmask" / (pid + ".npz"), target=target, left=real_l, gouge=real_g, lo=g.lo, h=g.h)
    # keep only the top views for the contact sheet: holding every piece's 3D arrays until the end took the full run
    # past its 2 GB cap after about 20 pieces (the cgroup was killed without a message)
    out["_arrays"] = (g, target.any(2), real_g.any(2), real_l.any(2))
    return out


def render(results, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = len(results)
    cols = 6
    rows = int(math.ceil(n / cols))
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 2.6, rows * 2.8))
    for ax in axs.ravel():
        ax.axis("off")
    for ax, r in zip(axs.ravel(), results):
        g, t2, gg2, ll2 = r["_arrays"]
        img = np.zeros(t2.shape + (3,))
        img[:] = (1, 1, 1)
        img[t2] = (0.78, 0.80, 0.83)
        img[ll2] = (0.85, 0.33, 0.10)
        img[gg2] = (0.13, 0.35, 0.80)
        ax.imshow(np.transpose(img, (1, 0, 2)), origin="lower", extent=(g.lo[0], g.hi[0], g.lo[1], g.hi[1]))
        ax.set_title("%s  %.0f%% of blank-part\ngouge %.2f / left %.2f cm3" % (
            r["pid"], r["removed_pct_of_expected"], r["gouge_deep_cm3"], r["left_thick_cm3"]), fontsize=7)
    fig.suptitle("Posted programs cut on voxel blanks (top view): grey = piece, orange = stock left > 1.5 voxels "
                 "thick, blue = gouge > 1.5 voxels deep", fontsize=9)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def main():
    spec = json.loads((SCR / "pieces.json").read_text())
    cam = json.loads((OUT / "cam.json").read_text())
    by_pid = {}
    for su in cam["setups"]:
        by_pid.setdefault(su["pid"], []).append(su)
    only = sys.argv[1:]
    res = []
    for pc in spec["pieces"]:
        if pc["pid"] not in by_pid or (only and pc["pid"] not in only):
            continue
        sus = sorted(by_pid[pc["pid"]], key=lambda s: s["setup"])
        t0 = time.time()
        r = run_piece(pc, sus, HERE)
        r["seconds"] = round(time.time() - t0, 1)
        print("%-7s res %.2f  removed %6.1f of %6.1f cm3 (%5.1f%%)  gouge %.3f cm3 (max %.2f mm)  left %.3f cm3 (max "
              "%.2f mm)  rapids-through-part %s  %.0f s" % (
                  r["pid"], r["res_mm"], r["removed_cm3"], r["expected_removal_cm3"], r["removed_pct_of_expected"],
                  r["gouge_deep_cm3"], r["gouge_max_depth_mm"], r["left_thick_cm3"], r["left_max_thickness_mm"],
                  sum(h["rapids_through_target"] for h in r["rapid_hits"]), r["seconds"]), flush=True)
        res.append(r)
    if res and not only:
        render(res, HERE / "img" / "sim-check.png")
    keep = [{k: v for k, v in r.items() if k != "_arrays"} for r in res]
    old = {}
    if only and (OUT / "sim.json").exists():
        old = {r["pid"]: r for r in json.loads((OUT / "sim.json").read_text())["pieces"]}
    for r in keep:
        old[r["pid"]] = r
    (OUT / "sim.json").write_text(json.dumps(dict(method=__doc__.split("\n\n")[1], pieces=list(old.values())),
                                             indent=1))
    if only and res:
        render(res, SCR / ("sim-%s.png" % "_".join(only)))


if __name__ == "__main__":
    main()
