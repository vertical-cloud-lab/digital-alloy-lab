"""Post-process the fast-track CFD cases (issue #260, PR 294) into numbers and PNGs.

Cross-flow cases (make_case.py --kind cross), per case:
  - gas speed 1, 3 and 5 mm above the Ø30 build area (mean, min, max, spread, reversed fraction);
  - wall shear on the powder bed (the plate and the strip the blade spreads) against the Shao & Lu (2000) entrainment
    threshold for loose 20-63 um AlSi10Mg spheres in argon (the same threshold as PR 266's gas-flow.md section 3.4);
  - capture: tracers (fume, condensate: they follow the gas) released 0.5-3 mm over the build area, followed along the
    steady velocity field; the fraction that enters the collector on the first pass, and where the rest goes,
    including how close it comes to the cover slide;
  - the jet's flow at the collector face against the collector's intake (the spill), and the pressure drop.
Purge cases (--kind scalar / buoyant): O2 against time at the plate, at the exhaust (flow-weighted, what the analyzer
samples) and in the box, and the times to 1000 and 100 ppm against the well-mixed ideal.

Run (light, ~1-3 min a case, < 1.5 GB):
    /tmp/tools/capmem 2 /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/cfd/post.py cross /tmp/ft-cfd/cross-lam --name laminar
    /tmp/tools/capmem 1 /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/cfd/post.py purge /tmp/ft-cfd/scal-A --name A ...
    /tmp/venv/bin/python desktop-lpbf/fast-track/analysis/cfd/post.py figures
Results go to desktop-lpbf/fast-track/analysis/out/cfd/cfd.json (merged case by case) and the PNGs there.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402
import numpy as np                                  # noqa: E402
import pyvista as pv                                # noqa: E402
from scipy.interpolate import RegularGridInterpolator   # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[0] / "out" / "cfd"
SCR = pathlib.Path("/tmp/ft-cfd/post")               # resampled fields (not committed)
RHO, MU, G = 1.65, 2.26e-5, 9.81
RHO_P = 2670.0                                       # AlSi10Mg, kg/m3
X_O2_AIR = 0.2095
# categorical palette (dataviz reference, light) and text inks
C1, C2, C3, C4, C5, C6, C7, C8 = "#257de0", "#f47230", "#00b894", "#f2a600", "#ee7fac", "#008a17", "#6a4ce2", "#ec4647"
INK, INK2, SURF = "#191919", "#666666", "#ffffff"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False, "text.color": INK,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
                     "axes.titlesize": 9.5, "legend.frameon": False})


def shao_lu(d_m, gamma):
    """Threshold friction velocity (m/s) and wall shear (Pa) for loose spheres, Shao & Lu (2000), A_N = 0.0123:
    u*t = sqrt(A_N (rho_p/rho g d + gamma/(rho d)))."""
    us = math.sqrt(0.0123 * (RHO_P / RHO * G * d_m + gamma / (RHO * d_m)))
    return us, RHO * us * us


THR = {f"{d}um_g{g:g}": shao_lu(d * 1e-6, g)[1] for d in (20, 40, 63) for g in (1.65e-4, 3e-4, 5e-4)}
THR_LO, THR_HI = THR["63um_g0.000165"], THR["63um_g0.0005"]          # 0.053, 0.118 Pa: the coarse fraction's band


# --------------------------------------------------------------------------------------------------
class Case:
    def __init__(self, path, time=None):
        self.path = pathlib.Path(path)
        self.meta = json.loads((self.path / "case_meta.json").read_text())
        self.g = self.meta["geom"]
        r = pv.OpenFOAMReader(str(self.path / "case.foam"))
        self.time = r.time_values[-1] if time is None else time
        r.set_active_time_value(self.time)
        r.cell_to_point_creation = True
        r.enable_all_patch_arrays()
        m = r.read()
        self.mesh = m["internalMesh"]
        self.bnd = m["boundary"]
        self.zb = self.g["zb"]
        mean = "UMean" in self.mesh.point_data          # a transient case: use its time averages
        self.uf, self.pf = ("UMean", "pMean") if mean else ("U", "p")
        self.wf = "wallShearStressMean" if mean else "wallShearStress"

    def sample(self, pts_mm, fields=("U", "p")):
        pd = pv.PolyData(np.asarray(pts_mm, float) / 1000.0)
        s = pd.sample(self.mesh)
        alias = {"U": self.uf, "p": self.pf}
        out = {f: np.asarray(s.point_data[alias.get(f, f)]) for f in fields if alias.get(f, f) in s.point_data}
        out["valid"] = np.asarray(s.point_data["vtkValidPointMask"]).astype(bool)
        return out

    def grid(self, name, xs, ys, zs, fields=("U",)):
        """Resample onto a rectilinear grid (mm axes); cached as .npz under /tmp."""
        SCR.mkdir(parents=True, exist_ok=True)
        f = SCR / f"{self.path.name}_{name}.npz"
        if f.exists():
            d = np.load(f)
            return {k: d[k] for k in d.files}
        rg = pv.RectilinearGrid(np.asarray(xs) / 1000.0, np.asarray(ys) / 1000.0, np.asarray(zs) / 1000.0)
        s = rg.sample(self.mesh)
        out = dict(x=np.asarray(xs), y=np.asarray(ys), z=np.asarray(zs))
        shp = (len(zs), len(ys), len(xs))
        for fl in fields:
            a = np.asarray(s.point_data[{"U": self.uf, "p": self.pf}.get(fl, fl)])
            a = a.reshape(shp + a.shape[1:])
            out[fl] = np.moveaxis(a, (0, 1, 2), (2, 1, 0)).astype(np.float32)
        v = np.asarray(s.point_data["vtkValidPointMask"]).reshape(shp)
        out["valid"] = np.moveaxis(v, (0, 1, 2), (2, 1, 0)).astype(np.int8)
        np.savez_compressed(f, **out)
        return out


def disc(r_mm, z_mm, n=40):
    """Equal-area polar sample points over a disc."""
    pts = []
    for i in range(n):
        rr = r_mm * math.sqrt((i + 0.5) / n)
        m = max(6, int(round(2 * math.pi * (i + 0.5))))
        for j in range(m):
            t = 2 * math.pi * (j + 0.5) / m
            pts.append((rr * math.cos(t), rr * math.sin(t), z_mm))
    return np.array(pts)


def bed_speed(cs):
    out = {}
    for z in (1.0, 3.0, 5.0):
        p = disc(15.0, cs.zb + z)
        s = cs.sample(p)
        u = s["U"][s["valid"]]
        sp = np.linalg.norm(u, axis=1)
        out[f"z{z:g}"] = dict(mean=float(sp.mean()), min=float(sp.min()), max=float(sp.max()), cov=float(sp.std() / sp.mean()),
                             uy_mean=float(u[:, 1].mean()), uz_mean=float(u[:, 2].mean()),
                             frac_reversed=float((u[:, 1] < 0).mean()), n=int(len(sp)))
    return out


def bed_shear(cs):
    b = cs.bnd["bed"]
    c = np.asarray(b.cell_centers().points) * 1000.0
    tau = np.linalg.norm(np.asarray(b.cell_data[cs.wf]), axis=1) * RHO
    area = np.asarray(b.compute_cell_sizes(length=False, volume=False).cell_data["Area"]) * 1e6
    r = np.hypot(c[:, 0], c[:, 1])
    hx = cs.g["hx"]
    # where loose powder lies: the plate, and the strip the blade sweeps between its parks (block top, |y| < 23,
    # from the block's left edge to the overflow slot)
    zones = {"build_area_d30": r < 15.0, "plate_d40": r < cs.g["plate_d"] / 2,
             "strip_outside_plate": (np.abs(c[:, 1]) < 23.0) & (c[:, 0] > -40.0) & (c[:, 0] < cs.g["ovf"][0][0]) & (r >= cs.g["plate_d"] / 2),
             "whole_block_top": np.ones(len(r), bool)}
    out = {}
    for k, msk in zones.items():
        t, a = tau[msk], area[msk]
        if not len(t):
            continue
        out[k] = dict(mean=float((t * a).sum() / a.sum()), max=float(t.max()), p95=float(np.percentile(t, 95)),
                      frac_area_above_63um_low=float(a[t > THR_LO].sum() / a.sum()),
                      frac_area_above_63um_high=float(a[t > THR_HI].sum() / a.sum()),
                      frac_area_above_20um_low=float(a[t > THR["20um_g0.000165"]].sum() / a.sum()))
    if "yPlus" in b.cell_data:
        yp = np.asarray(b.cell_data["yPlus"])
        out["yplus_plate"] = dict(mean=float(yp[zones["plate_d40"]].mean()), max=float(yp[zones["plate_d40"]].max()))
    return out, (c, tau)


T_AVG = [None]          # transient cases: average function-object series from this time on


def last_line(path):
    lines = [ln for ln in pathlib.Path(path).read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    rows = [[float(v.strip("()")) for v in ln.split()] for ln in lines]
    if T_AVG[0] is not None:
        sel = np.array([r for r in rows if r[0] >= T_AVG[0]])
        if len(sel):
            return list(sel.mean(axis=0))
    return rows[-1]


def fo_file(cs, fo, name):
    d = cs.path / "postProcessing" / fo
    if not d.exists():
        return None
    ts = sorted(d.iterdir(), key=lambda p: float(p.name))
    f = ts[-1] / name
    return f if f.exists() else None


def convergence(cs):
    lf = cs.path / ("log.pimpleFoam" if cs.meta.get("transient") else "log.simpleFoam")
    log = lf.read_text(errors="replace")
    its = re.findall(r"^Time = ([0-9.eE+-]+)", log, re.M)
    res = {}
    for v in ("Ux", "Uy", "Uz", "p", "k", "omega"):
        m = re.findall(r"Solving for %s, Initial residual = ([0-9.eE+-]+)" % v, log)
        if m:
            res[v] = float(m[-1])
    out = dict(iterations=float(its[-1]) if its else 0, steps=len(its), final_initial_residuals=res)
    f = fo_file(cs, "probes", "U")
    if f:
        rows = [ln.split() for ln in f.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
        t = np.array([float(r[0]) for r in rows])
        vals = np.array([[float(x.strip("()")) for x in r[1:]] for r in rows]).reshape(len(rows), -1, 3)
        sp = np.linalg.norm(vals, axis=2)
        last = t >= 0.8 * t[-1]
        out["probe_speed_last20pct"] = dict(mean=sp[last].mean(axis=0).round(4).tolist(), std=sp[last].std(axis=0).round(5).tolist(),
                                            labels=["z1", "z3", "z5", "y-15 z3", "y+15 z3", "under slide"])
    return out


def pressure(cs):
    out = {}
    f = fo_file(cs, "pIn", "surfaceFieldValue.dat")
    if f:
        out["inlet_minus_outlet_Pa"] = last_line(f)[1] * RHO
    f = fo_file(cs, "qOut", "surfaceFieldValue.dat")
    if f:
        out["outlet_flow_L_min"] = last_line(f)[1] * 60000.0
    f = fo_file(cs, "probes", "p")
    if f:
        v = last_line(f)
        out["box_under_slide_minus_outlet_Pa"] = v[6] * RHO
        out["over_plate_z3_minus_outlet_Pa"] = v[2] * RHO
    return out


# --------------------------------------------------------------------------------------------------
def near_axes(cs):
    zb = cs.zb
    xs = np.arange(-45.0, 45.01, 0.5)
    ys = np.arange(-45.0, 50.01, 0.5)
    zs = np.concatenate([np.arange(zb, zb + 12.0, 0.25), np.arange(zb + 12.0, zb + 30.01, 1.0)])
    return xs, ys, zs


def box_axes(cs):
    e = cs.g["enclosure"]
    return (np.arange(e[0] + 0.5, e[1], 2.5), np.arange(e[2] + 0.5, e[3], 2.5), np.arange(e[4] + 0.5, e[5], 2.5))


class Field:
    def __init__(self, d):
        self.ax = (d["x"], d["y"], d["z"])
        self.itp = RegularGridInterpolator(self.ax, d["U"], bounds_error=False, fill_value=0.0)
        self.lo = np.array([a[0] for a in self.ax])
        self.hi = np.array([a[-1] for a in self.ax])

    def inside(self, p):
        return np.all((p >= self.lo) & (p <= self.hi), axis=1)


def trace(near, boxf, p0, cs, ds_near=0.15, ds_box=1.0, n_near=4000, n_box=6000):
    """Streamlines (tracers) from p0 (mm). Fates: captured (into the collector's plenum), escaped (left the near
    region), stalled. Escaped ones go on in the box field; their closest approach to the slide is recorded."""
    co, zb = cs.g["collector"], cs.zb
    yin = co["y_face"] + 2.0
    n = len(p0)
    p = p0.astype(float).copy()
    fate = np.zeros(n, int)                     # 0 active, 1 captured, 2 escaped, 3 stalled
    tt = np.zeros(n)
    paths = [[] for _ in range(n)]

    def vel(f, q):
        return f.itp(q / 1000.0 * 1000.0) if False else f.itp(q)

    for step in range(n_near):
        a = fate == 0
        if not a.any():
            break
        q = p[a]
        u1 = near.itp(q)
        s1 = np.linalg.norm(u1, axis=1)
        st = s1 < 1e-4
        d1 = u1 / np.maximum(s1, 1e-12)[:, None]
        qm = q + 0.5 * ds_near * d1
        u2 = near.itp(qm)
        s2 = np.linalg.norm(u2, axis=1)
        d2 = u2 / np.maximum(s2, 1e-12)[:, None]
        q2 = q + ds_near * d2
        idx = np.where(a)[0]
        tt[idx] += ds_near * 1e-3 / np.maximum(s2, 1e-6)
        p[idx] = q2
        if step % 20 == 0:
            for i, qq in zip(idx, q2):
                paths[i].append(qq.copy())
        cap = (q2[:, 1] > yin) & (np.abs(q2[:, 0]) < co["w"] / 2) & (q2[:, 2] > zb + co["z0"] - 0.5) & (q2[:, 2] < zb + co["z1"] + 0.5)
        esc = ~near.inside(q2) | (q2[:, 2] > zb + 29.0)
        fate[idx[cap]] = 1
        fate[idx[esc & ~cap]] = 2
        fate[idx[st & ~cap & ~esc]] = 3
    fate[fate == 0] = 3
    # escaped: on through the box field
    zs, rs = cs.g["z_slide"], 30.0
    esc = np.where(fate == 2)[0]
    dmin = np.full(n, np.nan)
    t_win = np.full(n, np.nan)
    back = np.zeros(n, bool)
    if len(esc):
        q = p[esc].copy()
        live = np.ones(len(esc), bool)
        te = tt[esc].copy()
        dm = np.full(len(esc), np.inf)
        for step in range(n_box):
            if not live.any():
                break
            u1 = boxf.itp(q[live])
            s1 = np.linalg.norm(u1, axis=1)
            d1 = u1 / np.maximum(s1, 1e-12)[:, None]
            u2 = boxf.itp(q[live] + 0.5 * ds_box * d1)
            s2 = np.linalg.norm(u2, axis=1)
            d2 = u2 / np.maximum(s2, 1e-12)[:, None]
            li = np.where(live)[0]
            q[li] = q[li] + ds_box * d2
            te[li] += ds_box * 1e-3 / np.maximum(s2, 1e-6)
            r = np.hypot(q[li, 0], q[li, 1])
            d = np.where(r < rs, zs - q[li, 2], np.hypot(r - rs, zs - q[li, 2]))
            newmin = d < dm[li]
            dm[li[newmin]] = d[newmin]
            hit = d < 10.0
            for k in li[hit]:
                if np.isnan(t_win[esc[k]]):
                    t_win[esc[k]] = te[k]
            if step % 10 == 0:
                for k in li:
                    paths[esc[k]].append(q[k].copy())
            # back over the bed region near the jet: counted as re-entrained
            nb = (np.abs(q[li, 0]) < 30) & (q[li, 1] > -27) & (q[li, 1] < 27) & (q[li, 2] < zb + 8)
            back[esc[li[nb]]] = True
            live[li[(s2 < 1e-5) | nb | (te[li] > 120.0)]] = False
        dmin[esc] = dm
    return fate, tt, dmin, t_win, back, paths


def capture(cs, near, boxf):
    rng = np.random.default_rng(1)
    pts = []
    for z in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        d = disc(15.0, cs.zb + z, n=12)
        pts.append(d)
    p0 = np.concatenate(pts)
    p0[:, :2] += rng.uniform(-0.05, 0.05, size=(len(p0), 2))
    fate, tt, dmin, t_win, back, paths = trace(near, boxf, p0, cs)
    n = len(p0)
    res = dict(n=n, captured=float((fate == 1).mean()), escaped=float((fate == 2).mean()), stalled=float((fate == 3).mean()))
    for z in (0.5, 1.0, 2.0, 3.0):
        m = np.isclose(p0[:, 2], cs.zb + z)
        res[f"captured_from_z{z:g}"] = float((fate[m] == 1).mean())
    cap = fate == 1
    res["transit_s_median_captured"] = float(np.median(tt[cap])) if cap.any() else None
    st = fate == 3
    if st.any():
        pe = np.array([paths[i][-1] if len(paths[i]) else p0[i] for i in np.where(st)[0]])
        lip = (pe[:, 1] > cs.g["collector"]["y_face"] - 8) & (pe[:, 2] < cs.zb + cs.g["collector"]["z0"] + 1.0)
        res["stalled_at_collector_lower_lip"] = float(lip.sum() / n)
    e = fate == 2
    if e.any():
        res["escaped_closest_to_slide_mm_min"] = float(np.nanmin(dmin[e]))
        res["escaped_closest_to_slide_mm_median"] = float(np.nanmedian(dmin[e]))
        res["frac_all_within_10mm_of_slide"] = float((dmin[e] < 10).sum() / n)
        res["frac_all_within_30mm_of_slide"] = float((dmin[e] < 30).sum() / n)
        res["escaped_back_to_jet"] = float(back[e].mean())
        tw = t_win[e]
        res["time_to_within_10mm_of_slide_s_median"] = float(np.nanmedian(tw)) if np.isfinite(tw).any() else None
    # tracers above the jet, where a rising plume would be (no buoyancy of the hot plume: tracers only)
    pts = [disc(15.0, cs.zb + z, n=8) for z in (4.0, 6.0, 8.0, 10.0, 15.0)]
    q0 = np.concatenate(pts)
    f2, t2, d2, w2, b2, paths2 = trace(near, boxf, q0, cs)
    pl = dict(n=len(q0), captured=float((f2 == 1).mean()), escaped=float((f2 == 2).mean()), stalled=float((f2 == 3).mean()))
    for z in (4.0, 6.0, 8.0, 10.0, 15.0):
        m = np.isclose(q0[:, 2], cs.zb + z)
        pl[f"captured_from_z{z:g}"] = float((f2[m] == 1).mean())
    e2 = f2 == 2
    if e2.any():
        pl["frac_all_within_10mm_of_slide"] = float((d2[e2] < 10).sum() / len(q0))
        pl["frac_all_within_30mm_of_slide"] = float((d2[e2] < 30).sum() / len(q0))
        pl["escaped_closest_to_slide_mm_median"] = float(np.nanmedian(d2[e2]))
        pl["escaped_back_to_jet"] = float(b2[e2].mean())
    res["above_jet_4_15mm"] = pl
    return res, (p0, fate, paths)


def spill(cs, near):
    """Flow along +y through planes across the jet, |x| < 40, from the bed to 25 mm up (L/min): the jet plus what it
    entrains, against the collector's intake (the nozzle's flow, since the box has no other outlet)."""
    out = {}
    xs = np.arange(-40.0, 40.01, 0.25)
    zs = np.arange(cs.zb + 0.125, cs.zb + 25.0, 0.25)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    for y in (-20.0, 0.0, 20.0, 25.0):
        pts = np.stack([X.ravel(), np.full(X.size, y), Z.ravel()], axis=1)
        uy = near.itp(pts)[:, 1].reshape(X.shape)
        da = 0.25e-3 * 0.25e-3
        out[f"y{y:g}"] = dict(forward_L_min=float(uy[uy > 0].sum() * da * 60000), backward_L_min=float(-uy[uy < 0].sum() * da * 60000))
    return out


def fig_cross(cases, name):
    """|U| in the x = 0 plane near the jet, one panel per case, shared scale; streamlines of (Uy, Uz)."""
    n = len(cases)
    fig, axs = plt.subplots(n, 1, figsize=(7.2, 2.35 * n), squeeze=False, constrained_layout=True)
    for ax, (label, cs, near) in zip(axs[:, 0], cases):
        xs, ys, zs = near.ax
        i0 = np.argmin(np.abs(xs - 0.0))
        zs2 = np.arange(cs.zb, cs.zb + 25.0, 0.25)
        Y, Z = np.meshgrid(ys, zs2, indexing="ij")
        pts = np.stack([np.zeros(Y.size), Y.ravel(), Z.ravel()], axis=1)
        U = near.itp(pts).reshape(Y.shape + (3,))
        sp = np.linalg.norm(U, axis=2)
        pc = ax.pcolormesh(Y, Z - cs.zb, sp, cmap="Blues", vmin=0, vmax=2.8, shading="auto", rasterized=True)
        ax.streamplot(ys, zs2 - cs.zb, U[:, :, 1].T, U[:, :, 2].T, color=INK2, linewidth=0.5, density=1.6, arrowsize=0.5)
        sl, co = cs.g["slot"], cs.g["collector"]
        ax.add_patch(plt.Rectangle((-46, 0), 46 - 27, 8, color="#bfbfbf", zorder=3))
        ax.add_patch(plt.Rectangle((27, 0), 13, max(10, co["z1"] + 2), color="#bfbfbf", zorder=3))
        ax.add_patch(plt.Rectangle((sl["y_inlet"], sl["z0"]), sl["chan"], sl["h"], color="white", zorder=4))
        ax.add_patch(plt.Rectangle((27, co["z0"]), 11, co["z1"] - co["z0"], color="white", zorder=4))
        if co.get("lip", 0) > 0:
            ax.add_patch(plt.Rectangle((27 - co["lip"], co["z1"]), co["lip"], 2, color="#bfbfbf", zorder=3))
        ax.plot([-20, 20], [0, 0], color=C2, lw=3, solid_capstyle="butt", zorder=5)
        ax.set_xlim(-45, 50)
        ax.set_ylim(0, 25)
        ax.set_aspect("equal")
        ax.set_ylabel("z above bed (mm)")
        ax.set_title(label, loc="left")
    axs[-1, 0].set_xlabel("y (mm): nozzle exit at -27, collector face at +27; orange = Ø40 plate")
    fig.colorbar(pc, ax=axs[:, 0], shrink=0.8, label="|U| (m/s)")
    fig.savefig(OUT / name, dpi=120)
    plt.close(fig)


def fig_shear(c, tau, cs, title, name):
    fig, ax = plt.subplots(figsize=(5.6, 4.6), constrained_layout=True)
    sc = ax.tricontourf(c[:, 0], c[:, 1], tau, levels=np.linspace(0, max(0.3, np.percentile(tau, 99)), 13), cmap="Blues")
    cs_ = ax.tricontour(c[:, 0], c[:, 1], tau, levels=[THR_LO, THR_HI], colors=[C2, C8], linewidths=1.0)
    ax.clabel(cs_, fmt={THR_LO: f"{THR_LO:.3f}", THR_HI: f"{THR_HI:.3f}"}, fontsize=7)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(19.9 * np.cos(t), 19.9 * np.sin(t), color=INK, lw=0.8)
    ax.plot(15 * np.cos(t), 15 * np.sin(t), color=INK, lw=0.6, ls="--")
    ax.set_aspect("equal")
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm), flow along +y")
    ax.set_title(title + f"\ncontours: 63 µm pick-up band {THR_LO:.3f} (orange) to {THR_HI:.3f} Pa (red)", loc="left")
    fig.colorbar(sc, ax=ax, label="wall shear (Pa)")
    fig.savefig(OUT / name, dpi=120)
    plt.close(fig)


def fig_tracers(p0, fate, paths, cs, title, name):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.0, 3.6), constrained_layout=True)
    cols = {1: C1, 2: C2, 3: C7}
    labs = {1: "into the collector", 2: "escaped to the box", 3: "stalled"}
    for k in (1, 3, 2):
        idx = np.where(fate == k)[0][::3]
        for j, i in enumerate(idx):
            pp = np.array(paths[i]) if len(paths[i]) else p0[i:i + 1]
            pp = np.vstack([p0[i:i + 1], pp])
            kw = dict(color=cols[k], lw=0.6, alpha=0.8, label=labs[k] if j == 0 else None)
            a1.plot(pp[:, 1], pp[:, 2] - cs.zb, **kw)
            a2.plot(pp[:, 1], pp[:, 0], **kw)
    a1.set_xlim(-50, 60)
    a1.set_ylim(0, 40)
    a1.set_xlabel("y (mm)")
    a1.set_ylabel("z above bed (mm)")
    a2.set_xlim(-50, 60)
    a2.set_ylim(-50, 50)
    a2.set_xlabel("y (mm)")
    a2.set_ylabel("x (mm)")
    a1.set_title(title, loc="left")
    a2.legend(loc="lower right", fontsize=7)
    fig.savefig(OUT / name, dpi=120)
    plt.close(fig)


def fig_box(cs, boxf, title, name):
    """|U| over the whole box in the x = 0 plane (through the plate and the slide)."""
    xs, ys, zs = boxf.ax
    Y, Z = np.meshgrid(ys, zs, indexing="ij")
    pts = np.stack([np.zeros(Y.size), Y.ravel(), Z.ravel()], axis=1)
    U = boxf.itp(pts).reshape(Y.shape + (3,))
    sp = np.linalg.norm(U, axis=2)
    fig, ax = plt.subplots(figsize=(7.0, 4.4), constrained_layout=True)
    pc = ax.pcolormesh(Y, Z, np.maximum(sp, 1e-4), cmap="Blues", norm=matplotlib.colors.LogNorm(1e-3, 3), shading="auto", rasterized=True)
    ax.streamplot(ys, zs, U[:, :, 1].T, U[:, :, 2].T, color=INK2, linewidth=0.5, density=1.4, arrowsize=0.6)
    zsl = cs.g["z_slide"]
    ax.plot([-20, 20], [zsl, zsl], color=C8, lw=2.5, solid_capstyle="butt")
    ax.plot([-20, 20], [cs.zb, cs.zb], color=C2, lw=2.5, solid_capstyle="butt")
    ax.set_aspect("equal")
    ax.set_xlabel("y (mm)")
    ax.set_ylabel("z (mm)")
    ax.set_title(title + "  (red: cover slide, orange: plate)", loc="left")
    fig.colorbar(pc, ax=ax, label="|U| (m/s), log scale", shrink=0.85)
    fig.savefig(OUT / name, dpi=120)
    plt.close(fig)


def load_json():
    f = OUT / "cfd.json"
    return json.loads(f.read_text()) if f.exists() else {}


def save_json(d):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "cfd.json").write_text(json.dumps(d, indent=1, default=float))


def do_cross(a):
    cs = Case(a.case)
    if cs.meta.get("transient"):
        T_AVG[0] = cs.meta.get("avg_from", 0.1)
    near = Field(cs.grid("near", *near_axes(cs)))
    boxf = Field(cs.grid("box", *box_axes(cs)))
    res = dict(case=str(cs.path), model=cs.meta["model"], nozzle_lpm=cs.meta["nozzle_lpm"], geom={k: cs.g[k] for k in ("slot", "collector")},
               cells=int(cs.mesh.n_cells), time=float(cs.time))
    res["convergence"] = convergence(cs)
    res["speed_over_build_area"] = bed_speed(cs)
    sh, (c, tau) = bed_shear(cs)
    res["bed_shear_Pa"] = sh
    res["pressure"] = pressure(cs)
    res["jet_flow"] = spill(cs, near)
    cap, (p0, fate, paths) = capture(cs, near, boxf)
    res["capture"] = cap
    # gas speed just under the slide
    s = cs.sample(disc(19.0, cs.g["z_slide"] - 2.0, n=10))
    res["speed_2mm_under_slide"] = dict(mean=float(np.linalg.norm(s["U"][s["valid"]], axis=1).mean()),
                                        max=float(np.linalg.norm(s["U"][s["valid"]], axis=1).max()))
    d = load_json()
    d.setdefault("cross", {})[a.name] = res
    d["threshold_shao_lu_Pa"] = THR
    save_json(d)
    off = np.cumsum([0] + [len(p_) for p_ in paths])
    flat = np.concatenate([np.array(p_) for p_ in paths if len(p_)]) if off[-1] else np.zeros((0, 3))
    np.savez_compressed(SCR / f"{cs.path.name}_post.npz", c=c, tau=tau, p0=p0, fate=fate, flat=flat, off=off)
    if a.figs:
        fig_shear(c, tau, cs, f"Bed wall shear, {a.name}", f"bed_shear_{a.name}.png")
        fig_tracers(p0, fate, paths, cs, f"Tracers from 0.5-3 mm over the build area, {a.name}: "
                    f"{cap['captured'] * 100:.0f} % into the collector", f"tracers_{a.name}.png")
        fig_box(cs, boxf, f"Box section x = 0, {a.name}", f"box_section_{a.name}.png")
    print(json.dumps({k: res[k] for k in ("speed_over_build_area", "bed_shear_Pa", "pressure", "jet_flow", "capture",
                                          "convergence", "speed_2mm_under_slide")}, indent=1, default=float))


# --------------------------------------------------------------------------------------------------
def series(path, cols=None):
    rows = [ln.split() for ln in pathlib.Path(path).read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    return np.array([[float(x.strip("()")) for x in r] for r in rows])


def fo_series(case, fo, name):
    d = pathlib.Path(case) / "postProcessing" / fo
    parts = []
    for td in sorted(d.iterdir(), key=lambda p: float(p.name)):
        f = td / name
        if f.exists():
            parts.append(series(f))
    a = np.concatenate(parts)
    _, i = np.unique(a[:, 0], return_index=True)
    return a[i]


def crossing(t, y, level):
    """First time y drops below level (linear interpolation), or None."""
    below = np.where(y <= level)[0]
    if not len(below):
        return None
    i = below[0]
    if i == 0:
        return float(t[0])
    f = (y[i - 1] - level) / (y[i - 1] - y[i])
    return float(t[i - 1] + f * (t[i] - t[i - 1]))


def x_o2(yo2, yar):
    """O2 mole fraction from O2 and Ar mass fractions (N2 the rest)."""
    yn2 = np.clip(1.0 - yo2 - yar, 0, 1)
    n = yo2 / 31.9988 + yn2 / 28.0134 + yar / 39.948
    return yo2 / 31.9988 / n


def do_purge(a):
    case = pathlib.Path(a.case)
    meta = json.loads((case / "case_meta.json").read_text())
    kind = meta["kind"]
    if kind == "scalar":
        box = fo_series(case, "boxAvg", "volFieldValue.dat")
        exh = fo_series(case, "exhaust", "surfaceFieldValue.dat")
        prb = fo_series(case, "probes", "T")
        ppm = lambda c: c * X_O2_AIR * 1e6
        S = dict(t=box[:, 0], box=ppm(box[:, 1]), exhaust=None, plate=None)
        S["exhaust_t"], S["exhaust"] = exh[:, 0], ppm(exh[:, 1])
        S["plate_t"], S["plate"] = prb[:, 0], ppm(prb[:, 1])
        S["slide"] = ppm(prb[:, 3])
    else:
        box = fo_series(case, "boxAvg", "volFieldValue.dat")
        exh = fo_series(case, "exhaust", "surfaceFieldValue.dat")
        po2, par = fo_series(case, "probes", "O2"), fo_series(case, "probes", "Ar")
        n = min(len(po2), len(par))
        S = dict(t=box[:, 0], box=x_o2(box[:, 1], box[:, 3]) * 1e6)
        S["exhaust_t"] = exh[:, 0]
        S["exhaust"] = x_o2(exh[:, 1], exh[:, 3]) * 1e6
        S["plate_t"] = po2[:n, 0]
        S["plate"] = x_o2(po2[:n, 1], par[:n, 1]) * 1e6
        S["slide"] = x_o2(po2[:n, 3], par[:n, 3]) * 1e6
    q_total = sum(meta["inlets"].values())
    V = meta["geom"].get("gas_L", 23.19)
    res = dict(case=str(case), kind=kind, inlets=meta["inlets"], outlet=meta["outlet"], q_total_L_min=q_total, gas_L=V,
               t_end_s=float(S["t"][-1]))
    for lvl in (10000, 1000, 100):
        res[f"t_{lvl}ppm_min"] = {k: (lambda v: None if v is None else v / 60.0)(crossing(S[k + "_t"] if k + "_t" in S else S["t"], S[k], lvl))
                                  for k in ("box", "exhaust", "plate")}
        res[f"t_{lvl}ppm_min"]["well_mixed_ideal"] = math.log(209500 / lvl) * V / q_total
    res["ppm_at_end"] = dict(box=float(S["box"][-1]), exhaust=float(S["exhaust"][-1]), plate=float(S["plate"][-1]), slide=float(S["slide"][-1]))
    # levels not reached by the end of the run: extrapolate the last 20 % of the run's own exponential decay
    # (an estimate, labelled as such in results.md)
    ext = {}
    for k in ("box", "exhaust", "plate"):
        t = S[k + "_t"] if k + "_t" in S else S["t"]
        y = S[k]
        m = t >= 0.8 * t[-1]
        if m.sum() < 5 or np.any(y[m] <= 0):
            continue
        rate = -np.polyfit(t[m] / 60.0, np.log(y[m]), 1)[0]          # 1/min
        ext[k] = dict(decay_per_min_last20pct=float(rate))
        for lvl in (1000, 100):
            if res[f"t_{lvl}ppm_min"][k] is None and rate > 0:
                ext[k][f"t_{lvl}ppm_min_extrapolated"] = float(t[-1] / 60.0 + math.log(y[-1] / lvl) / rate)
    res["tail"] = ext
    # tail decay rate of the box average: effective volume changes per minute vs the ideal q/V
    t, b = S["t"], S["box"]
    m = (b < 3000) & (b > 5) & (t > 0.3 * t[-1])
    if m.sum() > 10:
        k = -np.polyfit(t[m] / 60.0, np.log(b[m]), 1)[0]
        res["tail_decay_per_min"] = float(k)
        res["ideal_decay_per_min"] = q_total / V
    if kind == "scalar":
        # the frozen purge flow (0/U, copied from the steady case): how much of the box is nearly still
        r = pv.OpenFOAMReader(str(case / "case.foam"))
        r.skip_zero_time = False
        r.set_active_time_value(0.0)
        r.cell_to_point_creation = False
        m = r.read()["internalMesh"]
        u = np.linalg.norm(np.asarray(m.cell_data["U"]), axis=1)
        vol = np.asarray(m.compute_cell_sizes(length=False, area=False, volume=True).cell_data["Volume"])
        res["flow"] = dict(mean_speed_mm_s=float(1000 * (u * vol).sum() / vol.sum()),
                           median_speed_mm_s=float(1000 * np.median(u)),
                           **{f"vol_frac_below_{v}mm_s": float(vol[u < v / 1000].sum() / vol.sum()) for v in (1, 3, 10)})
    np.savez_compressed(SCR / f"purge_{a.name}.npz", **{k: v for k, v in S.items() if v is not None})
    d = load_json()
    d.setdefault("purge", {})[a.name] = res
    save_json(d)
    print(json.dumps(res, indent=1, default=float))


class Lite:
    """A solved case's metadata and its cached near-jet grid, for the comparison figures."""

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.meta = json.loads((self.path / "case_meta.json").read_text())
        self.g = self.meta["geom"]
        self.zb = self.g["zb"]


def fig_shear_multi(rows, fname):
    n = len(rows)
    fig, axs = plt.subplots(1, n, figsize=(4.3 * n, 4.2), squeeze=False, constrained_layout=True)
    lv = np.linspace(0, 0.15, 16)
    for ax, (label, cs, P) in zip(axs[0], rows):
        c, tau = P["c"], P["tau"]
        sc = ax.tricontourf(c[:, 0], c[:, 1], np.clip(tau, 0, 0.1499), levels=lv, cmap="Blues")
        ax.tricontour(c[:, 0], c[:, 1], tau, levels=[THR_LO], colors=[C2], linewidths=1.0)
        ax.tricontour(c[:, 0], c[:, 1], tau, levels=[THR_HI], colors=[C8], linewidths=1.0)
        tt = np.linspace(0, 2 * np.pi, 200)
        ax.plot(19.9 * np.cos(tt), 19.9 * np.sin(tt), color=INK, lw=0.8)
        ax.plot(15 * np.cos(tt), 15 * np.sin(tt), color=INK, lw=0.6, ls="--")
        ax.set_aspect("equal")
        ax.set_xlim(-40, 40)
        ax.set_ylim(-40, 40)
        ax.set_xlabel("x (mm)")
        ax.set_title(label, loc="left")
    axs[0, 0].set_ylabel("y (mm); the jet runs along +y")
    fig.colorbar(sc, ax=axs[0], shrink=0.85, label="wall shear on the bed (Pa)")
    fig.suptitle(f"Bed shear. Orange line: {THR_LO:.3f} Pa, red: {THR_HI:.3f} Pa (63 µm pick-up band, Shao & Lu). "
                 "Circles: Ø40 plate, Ø30 build area", x=0.01, ha="left", fontsize=9)
    fig.savefig(OUT / fname, dpi=120)
    plt.close(fig)


def fig_tracers_multi(rows, fname):
    n = len(rows)
    fig, axs = plt.subplots(n, 2, figsize=(9.0, 2.7 * n), squeeze=False, constrained_layout=True)
    cols = {1: C1, 2: C2, 3: C7}
    labs = {1: "into the collector", 2: "escaped to the box", 3: "held (lip vortex) or stalled"}
    for (a1, a2), (label, cs, P) in zip(axs, rows):
        p0, fate, flat, off = P["p0"], P["fate"], P["flat"], P["off"]
        for k in (1, 3, 2):
            idx = np.where(fate == k)[0][::3]
            for j, i in enumerate(idx):
                pp = np.vstack([p0[i:i + 1], flat[off[i]:off[i + 1]]])
                kw = dict(color=cols[k], lw=0.6, alpha=0.8, label=labs[k] if j == 0 else None)
                a1.plot(pp[:, 1], pp[:, 2] - cs.zb, **kw)
                a2.plot(pp[:, 1], pp[:, 0], **kw)
        a1.set_xlim(-50, 60)
        a1.set_ylim(0, 30)
        a1.set_ylabel("z above bed (mm)")
        a2.set_xlim(-50, 60)
        a2.set_ylim(-45, 45)
        a2.set_ylabel("x (mm)")
        a1.set_title(label, loc="left")
        a2.legend(loc="lower right", fontsize=7)
    axs[-1, 0].set_xlabel("y (mm), side view")
    axs[-1, 1].set_xlabel("y (mm), top view")
    fig.savefig(OUT / fname, dpi=120)
    plt.close(fig)


def fig_box_multi(rows, fname):
    n = len(rows)
    fig, axs = plt.subplots(1, n, figsize=(5.2 * n, 4.0), squeeze=False, constrained_layout=True)
    for ax, (label, cs, B) in zip(axs[0], rows):
        xs, ys, zs = B.ax
        Y, Z = np.meshgrid(ys, zs, indexing="ij")
        pts = np.stack([np.zeros(Y.size), Y.ravel(), Z.ravel()], axis=1)
        U = B.itp(pts).reshape(Y.shape + (3,))
        sp = np.linalg.norm(U, axis=2)
        pc = ax.pcolormesh(Y, Z, np.maximum(sp, 1e-4), cmap="Blues", norm=matplotlib.colors.LogNorm(1e-3, 3), shading="auto",
                           rasterized=True)
        ax.streamplot(ys, zs, U[:, :, 1].T, U[:, :, 2].T, color=INK2, linewidth=0.5, density=1.3, arrowsize=0.6)
        zsl = cs.g["z_slide"]
        ax.plot([-20, 20], [zsl, zsl], color=C8, lw=2.5, solid_capstyle="butt")
        ax.plot([-20, 20], [cs.zb, cs.zb], color=C2, lw=2.5, solid_capstyle="butt")
        ax.set_aspect("equal")
        ax.set_xlabel("y (mm)")
        ax.set_title(label, loc="left")
    axs[0, 0].set_ylabel("z (mm)")
    fig.colorbar(pc, ax=axs[0], label="|U| (m/s), log scale", shrink=0.85)
    fig.suptitle("Box section x = 0 (through the plate and the window). Red: cover slide; orange: plate", x=0.01, ha="left",
                 fontsize=9)
    fig.savefig(OUT / fname, dpi=120)
    plt.close(fig)


def do_figures(a):
    """--cases label=path ...: the jet section, bed shear, tracer and box-section figures, one panel per case
    (from the cross step's caches under /tmp/ft-cfd/post)."""
    rows, rows_p, rows_b = [], [], []
    for item in a.cases:
        label, path = item.split("=", 1)
        cs = Lite(path)
        d = np.load(SCR / f"{cs.path.name}_near.npz")
        rows.append((label, cs, Field({k: d[k] for k in d.files})))
        f = SCR / f"{cs.path.name}_post.npz"
        if f.exists():
            rows_p.append((label, cs, dict(np.load(f))))
        f = SCR / f"{cs.path.name}_box.npz"
        if f.exists():
            d = np.load(f)
            rows_b.append((label, cs, Field({k: d[k] for k in d.files})))
    pre = a.name or "cross"
    fig_cross(rows, f"{pre}_jet_section.png")
    if rows_p:
        fig_shear_multi(rows_p, f"{pre}_bed_shear.png")
        fig_tracers_multi(rows_p, f"{pre}_tracers.png")
    if rows_b:
        fig_box_multi(rows_b, f"{pre}_box_section.png")


def fig_purge_curves(names, labels, fname, tmax=None, title=""):
    """O2 against time, one panel per purge configuration: box average, exhaust (flow-weighted), the plate (1 mm
    above it) and 2 mm under the cover slide, with the well-mixed ideal for the same flow and volume."""
    d = load_json()["purge"]
    n = len(names)
    tmax = tmax or max(d[nm]["t_end_s"] for nm in names) / 60
    ncol = 3 if n == 3 else (2 if n > 1 else 1)
    nrow = math.ceil(n / ncol)
    fig, axs = plt.subplots(nrow, ncol, figsize=(4.3 * ncol, 2.9 * nrow + 0.3), squeeze=False, sharex=True, sharey=True,
                            constrained_layout=True)
    for ax, nm, lab in zip(axs.ravel(), names, labels):
        r = d[nm]
        S = np.load(SCR / f"purge_{nm}.npz")
        tm = np.linspace(0, tmax, 200)
        ideal = 209500 * np.exp(-r["q_total_L_min"] * tm / r["gas_L"])
        ax.plot(tm, ideal, color="#9a9a9a", lw=1.2, ls=(0, (4, 2)), label="well mixed, same flow")
        ax.plot(S["t"] / 60, S["box"], color=C1, lw=2, label="box average")
        ax.plot(S["exhaust_t"] / 60, S["exhaust"], color=C2, lw=2, label="exhaust (analyzer)")
        ax.plot(S["plate_t"] / 60, S["plate"], color=C3, lw=2, label="1 mm over the plate")
        if "slide" in S.files:
            ax.plot(S["plate_t"][:len(S["slide"])] / 60, S["slide"], color=C7, lw=1.2, label="2 mm under the cover slide")
        for lvl in (1000, 100):
            ax.axhline(lvl, color=INK2, lw=0.6)
        ax.set_yscale("log")
        ax.set_ylim(10, 3e5)
        ax.set_xlim(0, tmax)
        t1 = r["t_1000ppm_min"]["exhaust"]
        t2 = r["t_100ppm_min"]["exhaust"]
        f = lambda v: "-" if v is None else f"{v:.1f}"
        ax.set_title(f"{lab}\nexhaust to 1000 / 100 ppm: {f(t1)} / {f(t2)} min", loc="left")
        ax.set_ylabel("O2 (ppm)")
    for ax in axs[-1]:
        ax.set_xlabel("time from the start of the purge (min)")
    for ax in axs.ravel()[n:]:
        ax.axis("off")
    axs[0, 0].legend(loc="lower left", fontsize=7)
    if title:
        fig.suptitle(title, x=0.01, ha="left", fontsize=9)
    fig.savefig(OUT / fname, dpi=120)
    plt.close(fig)


def fig_purge_snap(items, t_snaps, fname):
    """O2 (ppm, log) on the y = mid-depth section (through the purge ports): one row per case, one column per time
    in t_snaps (s; the nearest written time is shown)."""
    n, m = len(items), len(t_snaps)
    fig, axs = plt.subplots(n, m, figsize=(3.6 * m + 0.8, 2.0 * n + 0.3), squeeze=False, constrained_layout=True)
    for (i, (lab, path, field)), (j, t_snap) in ((a, b) for a in enumerate(items) for b in enumerate(t_snaps)):
        ax = axs[i, j]
        r = pv.OpenFOAMReader(str(pathlib.Path(path) / "case.foam"))
        tv = r.time_values
        tt = min(tv, key=lambda v: abs(v - t_snap))
        r.set_active_time_value(tt)
        r.cell_to_point_creation = True
        m = r.read()["internalMesh"]
        meta = json.loads((pathlib.Path(path) / "case_meta.json").read_text())
        e = meta["geom"]["enclosure"]
        ym = 0.5 * (e[2] + e[3])
        xs = np.arange(e[0] + 0.5, e[1], 2.0)
        zs = np.arange(e[4] + 0.5, e[5], 2.0)
        X, Z = np.meshgrid(xs, zs, indexing="ij")
        pts = pv.PolyData(np.stack([X.ravel(), np.full(X.size, ym), Z.ravel()], axis=1) / 1000.0)
        s = pts.sample(m)
        if field in ("c", "T"):
            v = np.asarray(s.point_data["T"]) * X_O2_AIR * 1e6
        else:
            v = x_o2(np.asarray(s.point_data["O2"]), np.asarray(s.point_data["Ar"])) * 1e6
        ok = np.asarray(s.point_data["vtkValidPointMask"]).astype(bool)
        v = np.where(ok, v, np.nan).reshape(X.shape)
        pc = ax.pcolormesh(X, Z, np.clip(v, 10, 2.1e5), cmap="Blues", norm=matplotlib.colors.LogNorm(10, 2.1e5),
                           shading="auto", rasterized=True)
        ax.set_aspect("equal")
        ax.set_title(f"{lab}, t = {tt / 60:.0f} min" if j == 0 else f"t = {tt / 60:.0f} min", loc="left", fontsize=8)
        if j == 0:
            ax.set_ylabel("z (mm)")
        if i < n - 1:
            ax.set_xticklabels([])
    for ax in axs[-1]:
        ax.set_xlabel("x (mm)")
    fig.suptitle(f"O2 on the section y = {ym:.0f} mm (mid-depth, through the purge ports on the left wall)", x=0.01,
                 ha="left", fontsize=9)
    fig.colorbar(pc, ax=axs, label="O2 (ppm), log scale", shrink=0.8)
    fig.savefig(OUT / fname, dpi=120)
    plt.close(fig)


def do_purgefigs(a):
    names = [c.split("=", 1)[0] for c in a.cases]
    labels = [c.split("=", 1)[1] for c in a.cases]
    fig_purge_curves(names, labels, a.name, a.tmax, a.title)


def do_snaps(a):
    items = []
    for c in a.cases:
        lab, path, field = c.split("=", 2)
        items.append((lab, path, field))
    fig_purge_snap(items, a.times or [a.t_snap], a.name)


def do_tables(a):
    """Markdown tables of the cross-flow and purge results in cfd.json (printed; results.md quotes them)."""
    d = load_json()
    cr = d.get("cross", {})
    names = [n for n in a.cases if n in cr] or list(cr)
    f2 = lambda v, n=2: "-" if v is None else f"{v:.{n}f}"
    pc = lambda v: "-" if v is None else f"{100 * v:.0f} %"
    L = ["| | " + " | ".join(names) + " |", "|---|" + "---|" * len(names)]

    def row(label, fn):
        vals = []
        for n in names:
            try:
                vals.append(fn(cr[n]))
            except (KeyError, TypeError):
                vals.append("-")
        L.append(f"| {label} | " + " | ".join(vals) + " |")
    sp = lambda r, z: r["speed_over_build_area"]["z" + z]
    for z in ("1", "3", "5"):
        row(f"speed {z} mm over the Ø30 build area: mean (min-max), m/s",
            lambda r: f"{sp(r, z)['mean']:.2f} ({sp(r, z)['min']:.2f}-{sp(r, z)['max']:.2f})")
    for z in ("1", "3", "5"):
        row(f"spread {z} mm (std/mean)", lambda r: pc(sp(r, z)["cov"]))
    for zone, lab in (("build_area_d30", "Ø30 build area"), ("plate_d40", "Ø40 plate"),
                      ("strip_outside_plate", "spread strip beside the plate"), ("whole_block_top", "whole block top")):
        row(f"bed shear, {lab}: mean / max, Pa",
            lambda r: f"{r['bed_shear_Pa'][zone]['mean']:.3f} / {r['bed_shear_Pa'][zone]['max']:.3f}")
        row(f"{lab}: area over 0.053 Pa (63 µm, low cohesion)", lambda r: pc(r["bed_shear_Pa"][zone]["frac_area_above_63um_low"]))
    cp = lambda r: r["capture"]
    ab = lambda r: r["capture"]["above_jet_4_15mm"]
    row("tracers 0.5-3 mm: into the collector", lambda r: pc(cp(r)["captured"]))
    row("tracers 0.5-3 mm: held under the collector's lower lip", lambda r: pc(cp(r).get("stalled_at_collector_lower_lip", 0)))
    row("tracers 0.5-3 mm: escaped to the box", lambda r: pc(cp(r)["escaped"]))
    row("tracers 0.5 mm: into the collector", lambda r: pc(cp(r)["captured_from_z0.5"]))
    row("tracers 4-15 mm (above the jet): into the collector", lambda r: pc(ab(r)["captured"]))
    row("tracers 4-15 mm: escaped to the box", lambda r: pc(ab(r)["escaped"]))
    row("escaped tracers: median closest approach to the slide, mm",
        lambda r: f2(ab(r).get("escaped_closest_to_slide_mm_median"), 0))
    row("tracers within 30 mm of the slide", lambda r: pc(ab(r).get("frac_all_within_30mm_of_slide", 0)))
    row("gas speed 2 mm under the slide: mean, mm/s", lambda r: f"{1000 * r['speed_2mm_under_slide']['mean']:.1f}")
    row("jet flow at y = 25 mm, forward / back, L/min",
        lambda r: f"{r['jet_flow']['y25']['forward_L_min']:.1f} / {r['jet_flow']['y25']['backward_L_min']:.1f}")
    row("outlet flow, L/min", lambda r: f"{r['pressure']['outlet_flow_L_min']:.1f}")
    row("pressure drop, nozzle channel inlet to collector port, Pa", lambda r: f"{r['pressure']['inlet_minus_outlet_Pa']:.0f}")
    row("box (under the slide) above the collector port, Pa", lambda r: f"{r['pressure']['box_under_slide_minus_outlet_Pa']:.0f}")
    row("y+ on the plate, mean / max",
        lambda r: f"{r['bed_shear_Pa']['yplus_plate']['mean']:.2f} / {r['bed_shear_Pa']['yplus_plate']['max']:.2f}")
    row("cells", lambda r: f"{r['cells']:,}")
    fr = lambda r: r["convergence"]["final_initial_residuals"]
    row("iterations or time steps; final initial residual Ux / Uz / p",
        lambda r: f"{r['convergence']['steps']}; {fr(r)['Ux']:.0e} / {fr(r)['Uz']:.0e} / {fr(r)['p']:.0e}")
    print("\n".join(L))
    pu = d.get("purge", {})
    if pu:
        print()
        ex = lambda r, k, lvl: r.get("tail", {}).get(k, {}).get(f"t_{lvl}ppm_min_extrapolated")

        def tt(r, k, lvl):
            v = r[f"t_{lvl}ppm_min"][k]
            if v is not None:
                return f"{v:.1f}"
            e = ex(r, k, lvl)
            return f"(≈ {e:.0f})" if e is not None else f"> {r['t_end_s'] / 60:.0f}"
        P = ["| run | in (L/min) | out | box average: 1000 / 100 ppm (min) | exhaust (analyzer) | 1 mm over the plate | "
             "O₂ at the end: box / exhaust / plate / under the slide (ppm) |", "|---|---|---|---|---|---|---|"]
        for n in [n for n in a.cases if n in pu] or list(pu):
            r = pu[n]
            ins = ", ".join(f"{k} {v:g}" for k, v in r["inlets"].items())
            e = r["ppm_at_end"]
            P.append(f"| {n} | {ins} | {r['outlet']} | " + " | ".join(f"{tt(r, k, 1000)} / {tt(r, k, 100)}" for k in
                     ("box", "exhaust", "plate")) + f" | {e['box']:.0f} / {e['exhaust']:.0f} / {e['plate']:.0f} / "
                     f"{e['slide']:.0f} (at {r['t_end_s'] / 60:.1f} min) |")
        r0 = next(iter(pu.values()))
        P.append(f"| well mixed, same flow and volume | {r0['q_total_L_min']:g} | | "
                 f"{r0['t_1000ppm_min']['well_mixed_ideal']:.1f} / {r0['t_100ppm_min']['well_mixed_ideal']:.1f} | | | |")
        print("\n".join(P))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=("cross", "purge", "figures", "purgefigs", "snaps", "tables"))
    ap.add_argument("--t-snap", type=float, default=600.0)
    ap.add_argument("--times", type=float, nargs="*", default=[], help="snaps: snapshot times, s (one column each)")
    ap.add_argument("--tmax", type=float, default=None, help="purgefigs: x-axis limit, min")
    ap.add_argument("--title", default="", help="purgefigs: figure title")
    ap.add_argument("case", nargs="?")
    ap.add_argument("--name", default="", help="case name in cfd.json (figures: the PNG's file name)")
    ap.add_argument("--figs", action="store_true")
    ap.add_argument("--cases", nargs="*", default=[], help="figures: label=case_path ...")
    a = ap.parse_args()
    SCR.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    {"cross": do_cross, "purge": do_purge, "figures": do_figures, "purgefigs": do_purgefigs, "snaps": do_snaps,
     "tables": do_tables}[a.what](a)


if __name__ == "__main__":
    main()
