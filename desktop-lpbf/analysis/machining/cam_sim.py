"""3-axis stock-removal simulation (dexel/voxel) for the machining review of the desktop LPBF (issue #260, PR #266).

What it does, per part (STLs from inventory.py):
  1. Voxelizes the part by ray parity along Z (pitch 0.25-0.5 mm) and builds the stock (a standard block or bbox + 3 mm).
  2. For each setup direction (+-X, +-Y, +-Z) and each flat end mill (diameter D, stick-out L, holder diameter H):
       height map h of the part seen from that direction (top voxel of every column),
       cutter-location surface  z_cl  = grey dilation of h by a disk of radius D/2  (= drop-cutter for a flat end mill),
       holder collision         z_tip = max(z_cl, dilation of h by a disk of radius H/2 - L),
       finished surface         r     = grey erosion of z_tip by a disk of radius D/2 (the swept cutter, i.e. a dexel
                                        stock-removal simulation of a dense raster toolpath),
     and marks every voxel above r as removable from that setup. cam_ocl.py runs OpenCAMLib's BatchDropCutter for the
     same cutters; toolpaths.py compares its z_cl with the dilation here (they agree to within one voxel).
  3. Residual stock = stock - part - union of removable voxels: what 3-axis milling with that tool set cannot reach
     (internal corners sharper than the tool, floors deeper than the stick-out next to a wall, undercuts such as dovetail
     and radial O-ring grooves, cross holes). Connected residual regions are listed with volume and location.
  4. Setup count: every air voxel touching the part ("skin") is tagged with the setups that can reach it with a 1/8 in.
     tool of unlimited reach; a greedy set cover gives the fewest setups, and skin no setup reaches is an undercut.

Run:  OMP_NUM_THREADS=1 /tmp/capmem 3 xvfb-run -a -s "-screen 0 1280x1024x24" /tmp/venv/bin/python \
          desktop-lpbf/analysis/machining/cam_sim.py [--parts DIR] [--only detailed|sweep|all]
Writes desktop-lpbf/analysis/out/machining/cam_sim.json and cam_<part>_<toolset>.png, and the residual voxels to
/tmp/mach-work/cam/res_*.npz for residual_report.py. Needs inventory.py's STLs. ~7 min (detailed) + 2 min (sweep).
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import time

import cv2
import numpy as np
from scipy import ndimage

REPO = pathlib.Path(__file__).resolve().parents[3]
OUT = REPO / "desktop-lpbf" / "analysis" / "out" / "machining"
INCH = 25.4

# Flat end mills: (diameter mm, stick-out from the holder mm, holder diameter mm). Stick-out = overall length minus
# ~1.25-1.5 in. held in the collet / side-lock holder. Holder: CAT40/BT30 ER32 or side-lock nose ~ 50 mm (63 mm for 1 in.
# in ER40), ER20 nose ~ 35 mm for small tools. "std": stocked lengths most shops have; "long": buy for this job.
TOOLS = {
    "1/2 std (3 in. OAL)": (12.7, 38.0, 50.0, "std"),
    "3/8 std (2.5 in. OAL)": (9.525, 32.0, 50.0, "std"),
    "1/4 std (2.5 in. OAL)": (6.35, 32.0, 35.0, "std"),
    "1/8 std (1.5 in. OAL)": (3.175, 19.0, 35.0, "std"),
    "1/16 std (3/16 LOC, 1/8 shank)": (1.5875, 4.8, 3.175, "std"),
    "3/4 std (4 in. OAL)": (19.05, 63.0, 50.0, "std"),
    "1 x 6 in. OAL": (25.4, 108.0, 63.0, "long"),
    "3/4 x 6 in. OAL": (19.05, 112.0, 50.0, "long"),
    "1/2 x 6 in. OAL": (12.7, 114.0, 50.0, "long"),
    "3/8 x 4 in. OAL": (9.525, 64.0, 50.0, "long"),
    "1/4 x 4 in. OAL": (6.35, 70.0, 35.0, "long"),
    "1/8 long reach (1 in.)": (3.175, 25.4, 6.35, "long"),
}
DIRS = ["+z", "-z", "+x", "-x", "+y", "-y"]
# part frame -> setup frame: (axis index of the tool axis, sign); the tool points along -axis*sign
AXIS = {"+x": (0, 1), "-x": (0, -1), "+y": (1, 1), "-y": (1, -1), "+z": (2, 1), "-z": (2, -1)}


def read_stl(path):
    import trimesh
    m = trimesh.load_mesh(path)
    return np.asarray(m.triangles, float)


def voxelize(tris, pitch, lo, shape):
    """Solid voxels by ray parity along +Z through every (x, y) column centre (slightly offset to dodge edges)."""
    nx, ny, nz = shape
    off = np.array([1e-3 * math.sqrt(2), 1e-3 * math.sqrt(3)]) * pitch
    cx0, cy0 = lo[0] + 0.5 * pitch + off[0], lo[1] + 0.5 * pitch + off[1]
    cols, zs = [], []
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    area = (b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (c[:, 0] - a[:, 0]) * (b[:, 1] - a[:, 1])
    keep = np.abs(area) > 1e-12
    for t, ar in zip(tris[keep], area[keep]):
        x, y = t[:, 0], t[:, 1]
        i0 = max(int(math.ceil((x.min() - cx0) / pitch)), 0)
        i1 = min(int(math.floor((x.max() - cx0) / pitch)), nx - 1)
        j0 = max(int(math.ceil((y.min() - cy0) / pitch)), 0)
        j1 = min(int(math.floor((y.max() - cy0) / pitch)), ny - 1)
        if i1 < i0 or j1 < j0:
            continue
        X, Y = np.meshgrid(cx0 + pitch * np.arange(i0, i1 + 1), cy0 + pitch * np.arange(j0, j1 + 1), indexing="ij")
        w0 = ((x[1] - X) * (y[2] - Y) - (x[2] - X) * (y[1] - Y)) / ar
        w1 = ((x[2] - X) * (y[0] - Y) - (x[0] - X) * (y[2] - Y)) / ar
        w2 = 1.0 - w0 - w1
        ins = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not ins.any():
            continue
        z = w0 * t[0, 2] + w1 * t[1, 2] + w2 * t[2, 2]
        I, Jj = np.meshgrid(np.arange(i0, i1 + 1), np.arange(j0, j1 + 1), indexing="ij")
        cols.append((I * ny + Jj)[ins])
        zs.append(z[ins])
    col = np.concatenate(cols)
    z = np.concatenate(zs)
    o = np.lexsort((z, col))
    col, z = col[o], z[o]
    # pair crossings column by column (drop columns with an odd count: an edge hit)
    uc, start, cnt = np.unique(col, return_index=True, return_counts=True)
    good = cnt % 2 == 0
    sel = np.concatenate([np.arange(s, s + n) for s, n, g in zip(start, cnt, good) if g]) if good.any() else np.array([], int)
    col, z = col[sel], z[sel]
    zin, zout, cc = z[0::2], z[1::2], col[0::2]
    kin = np.clip(np.ceil((zin - lo[2]) / pitch - 0.5).astype(int), 0, nz)
    kout = np.clip(np.floor((zout - lo[2]) / pitch - 0.5).astype(int) + 1, 0, nz)
    ok = kout > kin
    diff = np.zeros((nx * ny, nz + 1), np.int16)
    np.add.at(diff, (cc[ok], kin[ok]), 1)
    np.add.at(diff, (cc[ok], kout[ok]), -1)
    vox = np.cumsum(diff[:, :nz], axis=1) > 0
    return vox.reshape(nx, ny, nz), int((~good).sum())


def disk(r_vox):
    r = max(r_vox, 0.5)
    n = int(math.ceil(r - 1e-9))
    yy, xx = np.mgrid[-n:n + 1, -n:n + 1]
    return (xx ** 2 + yy ** 2 <= r * r + 1e-9).astype(np.uint8)


def to_setup(arr, d):
    """View a part-frame voxel array in the setup frame: tool axis last, pointing toward the spindle."""
    ax, s = AXIS[d]
    a = np.moveaxis(arr, ax, -1)
    return a[..., ::-1] if s < 0 else a


def from_setup(arr, d):
    ax, s = AXIS[d]
    a = arr[..., ::-1] if s < 0 else arr
    return np.moveaxis(a, -1, ax)


def removable(vox_setup, pitch, D, L, H):
    """Voxels a flat end mill (D, stick-out L, holder H) can remove in one 3-axis setup (setup frame, axis last)."""
    nz = vox_setup.shape[-1]
    occ = vox_setup.any(axis=-1)
    top = np.where(occ, nz - np.argmax(vox_setup[..., ::-1], axis=-1), -1e6).astype(np.float32)  # voxel units
    k = disk(D / 2 / pitch)
    z_cl = cv2.dilate(top, k, borderType=cv2.BORDER_CONSTANT, borderValue=-1e6)
    if H and L is not None:
        kh = disk(H / 2 / pitch)
        z_h = cv2.dilate(top, kh, borderType=cv2.BORDER_CONSTANT, borderValue=-1e6) - L / pitch
        z_tip = np.maximum(z_cl, z_h)
    else:
        z_tip = z_cl
    r = cv2.erode(z_tip, k, borderType=cv2.BORDER_CONSTANT, borderValue=1e6)
    kk = np.arange(nz, dtype=np.float32) + 0.5
    return kk[None, None, :] > r[..., None], z_cl


def grid_for(tris, pitch, margin, stock=None):
    lo = tris.reshape(-1, 3).min(0) - margin
    hi = tris.reshape(-1, 3).max(0) + margin
    if stock is not None:
        lo = np.minimum(lo, np.array(stock[0::2]) - pitch)
        hi = np.maximum(hi, np.array(stock[1::2]) + pitch)
    shape = tuple(int(math.ceil((h - l) / pitch)) for l, h in zip(lo, hi))
    return lo, shape


def centers(lo, shape, pitch):
    return [lo[i] + pitch * (np.arange(shape[i]) + 0.5) for i in range(3)]


def stock_mask(lo, shape, pitch, box):
    cx, cy, cz = centers(lo, shape, pitch)
    mx = (cx >= box[0]) & (cx <= box[1])
    my = (cy >= box[2]) & (cy <= box[3])
    mz = (cz >= box[4]) & (cz <= box[5])
    return mx[:, None, None] & my[None, :, None] & mz[None, None, :]


def components(res, lo, pitch, min_mm3=1.0, top=12):
    lab, n = ndimage.label(res, structure=np.ones((3, 3, 3)))
    if n == 0:
        return []
    idx = np.arange(1, n + 1)
    cnt = ndimage.sum(res, lab, idx)
    sl = ndimage.find_objects(lab)
    v = pitch ** 3
    rows = []
    for i in np.argsort(-cnt)[:top]:
        if cnt[i] * v < min_mm3:
            continue
        s = sl[i]
        b = [lo[a] + pitch * s[a].start for a in range(3)], [lo[a] + pitch * s[a].stop for a in range(3)]
        rows.append(dict(volume_mm3=round(float(cnt[i] * v), 1),
                         bbox=[round(b[0][0], 1), round(b[1][0], 1), round(b[0][1], 1), round(b[1][1], 1), round(b[0][2], 1), round(b[1][2], 1)]))
    return rows


def simulate(tris, pitch, stock_box, tools, dirs=DIRS):
    lo, shape = grid_for(tris, pitch, 4.0, stock_box)
    t0 = time.time()
    vox, odd = voxelize(tris, pitch, lo, shape)
    t_vox = time.time() - t0
    st = stock_mask(lo, shape, pitch, stock_box) | vox
    rem_all = np.zeros_like(vox)
    for name, (D, L, H, _) in tools.items():
        for d in dirs:
            r, _ = removable(to_setup(vox, d), pitch, D, L, H)
            rem_all |= from_setup(r, d)
    res = st & ~vox & ~rem_all
    return dict(lo=lo, shape=shape, vox=vox, stock=st, rem=rem_all, res=res, odd=odd, t_vox=t_vox)


def setups(tris, pitch, stock_box, D=3.175):
    """Greedy set cover of the skin (air voxels touching the part) by the 6 setups, with a slim tool of unlimited reach."""
    lo, shape = grid_for(tris, pitch, 4.0, stock_box)
    vox, _ = voxelize(tris, pitch, lo, shape)
    st = stock_mask(lo, shape, pitch, stock_box)
    skin = ndimage.binary_dilation(vox, structure=ndimage.generate_binary_structure(3, 1)) & ~vox & st
    reach = {}
    for d in DIRS:
        r, _ = removable(to_setup(vox, d), pitch, D, None, None)
        reach[d] = from_setup(r, d) & skin
    nskin = int(skin.sum())
    covered = np.zeros_like(skin)
    chosen = []
    while True:
        gains = {d: int((reach[d] & ~covered).sum()) for d in DIRS if d not in chosen}
        if not gains:
            break
        d = max(gains, key=gains.get)
        if gains[d] < max(0.002 * nskin, 3):
            break
        chosen.append(d)
        covered |= reach[d]
    unreach = skin & ~np.logical_or.reduce([reach[d] for d in DIRS])
    return dict(setups=chosen, skin_vox=nskin, unreachable_frac=float(unreach.sum()) / max(nskin, 1),
                unreachable=components(unreach, lo, pitch, min_mm3=pitch ** 3 * 4, top=6),
                gain=[int((reach[d]).sum()) for d in chosen], vox=vox, unreach=unreach, lo=lo)


# ------------------------------------------------------------------------------------------------ images
def render(name, sim, path, title, views=((-35, 28), (145, -25)), extra=None):
    import pyvista as pv
    pv.OFF_SCREEN = True
    lo, pitch = sim["lo"], sim["pitch"]
    def grid(mask):
        g = pv.ImageData(dimensions=np.array(mask.shape) + 1, spacing=(pitch,) * 3, origin=tuple(lo))
        g.cell_data["m"] = mask.ravel(order="F").astype(np.uint8)
        return g.threshold(0.5, scalars="m")
    part = pv.read(sim["stl"])
    pl = pv.Plotter(off_screen=True, window_size=(1500, 640), shape=(1, len(views)))
    res = sim["res"]
    rg = grid(res) if res.any() else None
    for k, (az, el) in enumerate(views):
        pl.subplot(0, k)
        pl.add_mesh(part, color="#c9d0d6", opacity=0.35, smooth_shading=False)
        if rg is not None and rg.n_cells:
            pl.add_mesh(rg, color="#d62728", opacity=1.0)
        if extra is not None and extra.any():
            pl.add_mesh(grid(extra), color="#1f77b4", opacity=0.9)
        pl.camera_position = "iso"
        pl.camera.azimuth = az
        pl.camera.elevation = el
        pl.reset_camera()
        pl.camera.zoom(1.25)
        if k == 0:
            pl.add_text(title, font_size=9, color="black")
    pl.set_background("white")
    pl.screenshot(str(path))
    pl.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parts", default="/tmp/mach-work/parts")
    ap.add_argument("--only", default="all")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    meta = json.load(open(pathlib.Path(a.parts) / "parts.json"))
    P = {p["slug"]: p for p in meta["parts"] if p["kind"] == "stock"}
    jpath = OUT / "cam_sim.json"
    result = json.loads(jpath.read_text()) if jpath.exists() else {}
    std = {k: v for k, v in TOOLS.items() if v[3] == "std"}
    if a.only in ("all", "detailed"):
        det = [  # (slug prefix, pitch, stock box or None)
            ("process_chamber_body", 0.5, [-165.1, 165.1, -120.65, 120.65, -26.2, 126.2]),   # 13 x 9.5 x 6 in. block
            ("chamber_lid", 0.4, None),
            ("chamber_door", 0.4, None),
            ("build_module_m50_spigot", 0.4, None),
        ]
        for pre, pitch, sbox in det:
            slug = next(s for s in P if s.startswith(pre))
            p = P[slug]
            tris = read_stl(str(pathlib.Path(a.parts) / f"{slug}.stl"))
            b = p["bbox"]
            sbox = sbox or [b[0] - 3, b[1] + 3, b[2] - 3, b[3] + 3, b[4] - 3, b[5] + 3]
            out = dict(name=p["name"], pitch=pitch, stock_box=sbox)
            for label, tools in (("std", std), ("std+long", TOOLS)):
                t0 = time.time()
                sim = simulate(tris, pitch, sbox, tools)
                v = pitch ** 3
                comp = components(sim["res"], sim["lo"], pitch, min_mm3=2.0)
                out[label] = dict(residual_mm3=round(float(sim["res"].sum() * v), 1), part_mm3=round(float(sim["vox"].sum() * v), 1),
                                  stock_mm3=round(float(sim["stock"].sum() * v), 1), removed_mm3=round(float((sim["stock"] & ~sim["vox"]).sum() * v), 1),
                                  odd_columns=sim["odd"], components=comp, seconds=round(time.time() - t0, 1),
                                  model_volume_mm3=round(p["volume_mm3"], 1))
                print(f"{slug[:40]} {label}: residual {out[label]['residual_mm3']:.0f} mm3, part vox {out[label]['part_mm3']:.0f} vs model "
                      f"{p['volume_mm3']:.0f} mm3, {len(comp)} regions, {time.time() - t0:.0f} s", flush=True)
                sim.update(pitch=pitch, stl=str(pathlib.Path(a.parts) / f"{slug}.stl"))
                render(slug, sim, OUT / f"cam_{pre}_{label.replace('+', '_')}.png",
                       f"{p['name'][:60]}\n3-axis, 6 setups, {label} tools: residual stock {out[label]['residual_mm3'] / 1000:.1f} cm3 (red)")
                np.savez_compressed(f"/tmp/mach-work/cam/res_{pre}_{label.replace('+', '_')}.npz", res=sim["res"], lo=sim["lo"], pitch=pitch)
            result.setdefault("detailed", {})[pre] = out
            jpath.write_text(json.dumps(result, indent=1))
    if a.only in ("all", "sweep"):
        sweep = {}
        for slug, p in P.items():
            tris = read_stl(str(pathlib.Path(a.parts) / f"{slug}.stl"))
            b = p["bbox"]
            big = max(b[1] - b[0], b[3] - b[2], b[5] - b[4])
            pitch = 0.25 if big < 60 else (0.4 if big < 150 else (0.6 if big < 350 else 1.5))
            sbox = [b[0] - 2, b[1] + 2, b[2] - 2, b[3] + 2, b[4] - 2, b[5] + 2]
            t0 = time.time()
            try:
                s = setups(tris, pitch, sbox)
            except Exception as e:  # noqa: BLE001
                print(slug, "failed", e)
                continue
            sweep[slug] = dict(setups=s["setups"], skin_vox=s["skin_vox"], unreachable_frac=round(s["unreachable_frac"], 4),
                               unreachable=s["unreachable"], pitch=pitch)
            print(f"{slug[:50]:50s} setups {s['setups']} unreachable {100 * s['unreachable_frac']:.2f} % ({time.time() - t0:.0f} s)", flush=True)
            result["sweep"] = sweep
            jpath.write_text(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
