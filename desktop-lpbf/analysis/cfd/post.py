"""Post-process the chamber cross-flow CFD into numbers, PNGs and particle fates (issue #260, PR #266).

Reads the cases written by make_case.py and solved by run_case.sh (OpenFOAM v2406, simpleFoam, k-omega SST) and
reports, for the fine mesh (and the coarse one as the mesh check):
  - the velocity over the plate at 1, 3 and 10 mm above the powder (mean, min, max, spread over Ø25 / Ø50 / Ø75),
  - the flow through the inlet slot and into the outlet slot along their length,
  - reversed flow over the plate and the flow under the cover slide,
  - wall shear on the powder bed against a Shao & Lu (2000) entrainment threshold for 20-63 um Al in argon,
  - the pressure drop from the inlet KF-25 flange to the outlet KF-25 flange,
  - where spatter (50-150 um, ballistic with drag) and condensate (< 1 um, tracers with turbulent diffusion) go.

Run (light: a few hundred MB, ~3 min):
    /tmp/capmem 3 /tmp/venv/bin/python desktop-lpbf/analysis/cfd/post.py --fine /tmp/cfd/fine --coarse /tmp/cfd/coarse
        [--variant /tmp/cfd/<name> ...]
Writes desktop-lpbf/analysis/out/cfd/cfd.json, cfd_summary.md and the PNGs.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                     # noqa: E402
import numpy as np                                  # noqa: E402
import pyvista as pv                                # noqa: E402
from scipy.interpolate import RegularGridInterpolator   # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[0] / "out" / "cfd"
RHO, MU, G = 1.65, 2.26e-5, 9.81
RHO_P = 2670.0                         # AlSi10Mg, kg/m3
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2 = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "savefig.facecolor": "#fcfcfb"})


class Case:
    """One solved case on its rectilinear grid (mm in the metadata, m in OpenFOAM)."""

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.meta = json.loads((self.path / "case_meta.json").read_text())
        r = pv.OpenFOAMReader(str(self.path / "case.foam"))
        self.time = r.time_values[-1]
        r.set_active_time_value(self.time)
        r.cell_to_point_creation = False
        m = r.read()
        im = m["internalMesh"]
        self.bnd = m["boundary"]
        c = np.asarray(im.cell_centers().points) * 1000.0           # mm
        L, N = self.meta["lines"], self.meta["n"]
        self.ax = []
        for a in "xyz":
            cs = []
            for i in range(len(L[a]) - 1):
                h = (L[a][i + 1] - L[a][i]) / N[a][i]
                cs += [L[a][i] + (m_ + 0.5) * h for m_ in range(N[a][i])]
            self.ax.append(np.array(cs))
        idx = [np.searchsorted(0.5 * (self.ax[a][1:] + self.ax[a][:-1]), c[:, a]) for a in range(3)]   # nearest centre
        shape = tuple(len(a) for a in self.ax)
        self.fluid = np.zeros(shape, bool)
        self.fluid[idx[0], idx[1], idx[2]] = True
        self.f = {}
        for name, comps in (("U", 3), ("p", 1), ("k", 1), ("nut", 1)):
            arr = np.asarray(im.cell_data[name])
            arr = arr.reshape(len(arr), -1)
            for j in range(comps):
                g = np.zeros(shape)
                g[idx[0], idx[1], idx[2]] = arr[:, j]
                key = name + ("xyz"[j] if comps == 3 else "")
                if name == "p":
                    g *= RHO                                         # kinematic -> Pa
                self.f[key] = g
        grid = tuple(a / 1000.0 for a in self.ax)
        self.itp = {k: RegularGridInterpolator(grid, v, bounds_error=False, fill_value=0.0) for k, v in self.f.items()}
        fm = RegularGridInterpolator(grid, self.fluid.astype(float), bounds_error=False, fill_value=0.0, method="nearest")
        self.is_fluid = lambda p_mm: fm(np.asarray(p_mm) / 1000.0) > 0.5
        self.ncells = int(self.fluid.sum())

    def __call__(self, key, pts_mm):
        return self.itp[key](np.asarray(pts_mm) / 1000.0)

    def U(self, pts_mm):
        return np.stack([self("Ux", pts_mm), self("Uy", pts_mm), self("Uz", pts_mm)], axis=-1)


def disc(r_mm, z_mm, n=60):
    """Polar sample points (equal area) over a disc of radius r at height z."""
    pts = []
    for i in range(n):
        rr = r_mm * math.sqrt((i + 0.5) / n)
        m = max(6, int(2 * math.pi * rr / (r_mm / n * 2)))
        for j in range(m):
            t = 2 * math.pi * (j + 0.5) / m
            pts.append((rr * math.cos(t), rr * math.sin(t), z_mm))
    return np.array(pts)


def bed_stats(cs):
    out = {}
    for z in (1.0, 3.0, 10.0):
        for d in (25, 50, 75):
            p = disc(d / 2, z)
            u = cs.U(p)
            sp = np.hypot(u[:, 0], u[:, 1])
            out[f"z{z:g}_d{d}"] = dict(mean=float(sp.mean()), min=float(sp.min()), max=float(sp.max()),
                                      cov=float(sp.std() / sp.mean()), minus_uy_mean=float(-u[:, 1].mean()),
                                      frac_ge_2=float((sp >= 2.0).mean()), frac_ge_2p5=float((sp >= 2.5).mean()),
                                      frac_reversed=float((u[:, 1] > 0).mean()))
    return out


def shao_lu(d_m, gamma):
    """Threshold friction velocity (m/s) and wall shear (Pa) for loose spheres, Shao & Lu (2000), A_N = 0.0123."""
    us = math.sqrt(0.0123 * (RHO_P / RHO * G * d_m + gamma / (RHO * d_m)))
    return us, RHO * us * us


def floor_shear(cs):
    fl = cs.bnd["floor"]
    c = np.asarray(fl.cell_centers().points) * 1000.0
    tau = np.linalg.norm(np.asarray(fl.cell_data["wallShearStress"]), axis=1) * RHO
    r = np.hypot(c[:, 0], c[:, 1])
    res = {}
    for d in (25, 50, 75):
        s = r < d / 2
        res[f"d{d}"] = dict(mean=float(tau[s].mean()), max=float(tau[s].max()))
    chamber = (np.abs(c[:, 1]) < 95) & (np.abs(c[:, 0]) < 140)
    res["floor_max"] = float(tau[chamber].max())
    imax = np.argmax(np.where(chamber, tau, 0))
    res["floor_max_at_mm"] = [float(v) for v in c[imax, :2]]
    return res, c, tau


def pressure(cs):
    pts = {"inlet port": (0, 140.5, 12.5), "plenum": (0, 124, 11), "chamber (mid)": (0, 0, 60), "under slide": (0, 0, 121),
           "outlet channel, x = -50": (-50, -90, -27), "outlet channel, x = +50": (50, -90, -27),
           "boot": (86, -92, -40), "outlet port": (86, -92, -60)}
    return {k: float(cs("p", [v])[0]) for k, v in pts.items()}


def slot_profiles(cs):
    x = np.linspace(-59, 59, 119)
    zin = np.linspace(4.5, 11.5, 8)
    uin = np.array([cs("Uy", np.column_stack([np.full(8, xi), np.full(8, 103.0), zin])).mean() for xi in x])
    xo = np.linspace(-61, 61, 123)
    uo = cs("Uz", np.column_stack([xo, np.full_like(xo, -90.0), np.full_like(xo, -10.0)]))
    return x, -uin, xo, -uo


def plane_xy(cs, z, h=1.0):
    x = np.arange(-139.5, 140, h)
    y = np.arange(-94.5, 95, h)
    X, Y = np.meshgrid(x, y)
    P = np.column_stack([X.ravel(), Y.ravel(), np.full(X.size, z)])
    u = cs.U(P)
    m = cs.is_fluid(P)
    U = [np.where(m, u[:, i], np.nan).reshape(X.shape) for i in range(3)]
    return x, y, U


def plane_yz(cs, x0, h=1.0):
    y = np.arange(-110.5, 143, h)
    z = np.arange(-32.5, 126, h * 0.5)
    Y, Z = np.meshgrid(y, z)
    P = np.column_stack([np.full(Y.size, x0), Y.ravel(), Z.ravel()])
    u = cs.U(P)
    m = cs.is_fluid(P)
    U = [np.where(m, u[:, i], np.nan).reshape(Y.shape) for i in range(3)]
    return y, z, U


def window_stats(cs):
    """Flow just under the cover slide and over the beam path (cylinder r < 25 mm)."""
    res = {}
    for z in (121.0, 117.0, 110.0, 90.0, 60.0):
        p = disc(20.0 if z > 120 else 25.0, z, 20)
        u = cs.U(p)
        sp = np.linalg.norm(u, axis=1)
        res[f"z{z:g}"] = dict(mean_speed=float(sp.mean()), max_speed=float(sp.max()), mean_uz=float(u[:, 2].mean()),
                              mean_uy=float(u[:, 1].mean()))
    return res


def recirculation(cs):
    """Share of the gas over the plate (|x|,|y| < 37.5, z 0-30 mm) that flows back toward the inlet (+y), and of the
    upper chamber (z 30-120) that does; the return flow is what carries plume back over the plate."""
    ax = cs.ax
    X, Y, Z = np.meshgrid(*ax, indexing="ij")
    f = cs.fluid
    uy = cs.f["Uy"]
    res = {}
    for name, sel in {"over plate, z 0-30 mm": (np.abs(X) < 37.5) & (np.abs(Y) < 37.5) & (Z < 30) & (Z > 0),
                      "over plate, z 30-120 mm": (np.abs(X) < 37.5) & (np.abs(Y) < 37.5) & (Z >= 30) & (Z < 120),
                      "whole chamber, z 0-120 mm": (np.abs(Y) < 95) & (Z > 0) & (Z < 120)}.items():
        s = sel & f
        res[name] = dict(frac_reversed=float((uy[s] > 0).mean()), mean_uy=float(uy[s].mean()))
    return res


# ------------------------------------------------------------------ particles
def track_spatter(cs, n=600, seed=1):
    rng = np.random.default_rng(seed)
    res = {}
    lands = {}
    for d_um in (50, 100, 150):
        d = d_um * 1e-6
        tau0 = RHO_P * d * d / (18 * MU)
        r = 25.0 * np.sqrt(rng.random(n))
        th = 2 * np.pi * rng.random(n)
        pos = np.column_stack([r * np.cos(th), r * np.sin(th), np.full(n, 0.3)]) / 1000.0     # m
        spd = rng.uniform(1.0, 6.0, n)
        el = np.radians(rng.uniform(20, 90, n))
        az = 2 * np.pi * rng.random(n)
        vel = np.column_stack([spd * np.cos(el) * np.cos(az), spd * np.cos(el) * np.sin(az), spd * np.sin(el)])
        fate = np.array(["airborne"] * n, dtype=object)
        alive = np.ones(n, bool)
        zmax = pos[:, 2].copy()
        dt = 2e-4
        for _ in range(int(2.0 / dt)):
            if not alive.any():
                break
            a = alive
            ug = cs.U(pos[a] * 1000.0)
            rel = ug - vel[a]
            rep = RHO * np.linalg.norm(rel, axis=1) * d / MU
            fd = 1 + 0.15 * rep ** 0.687
            acc = rel * (fd / tau0)[:, None]
            acc[:, 2] -= G
            vel[a] += acc * dt
            pos[a] += vel[a] * dt
            zmax[a] = np.maximum(zmax[a], pos[a, 2])
            pm = pos * 1000.0
            ia = np.where(a)[0]
            down = ia[pm[ia, 2] <= 0.0]
            for i in down:
                x, y = pm[i, 0], pm[i, 1]
                if -62 < x < 62 and -94 < y < -86:
                    fate[i] = "outlet slot"
                else:
                    fate[i] = "floor"
                alive[i] = False
            ia = np.where(alive)[0]
            if len(ia):
                ok = cs.is_fluid(pm[ia])
                for i in ia[~ok]:
                    z = pm[i, 2]
                    if z >= 119.0 and abs(pm[i, 0]) < 25 and abs(pm[i, 1]) < 25:
                        fate[i] = "slide recess"
                    elif z >= 119.0:
                        fate[i] = "ceiling"
                    else:
                        fate[i] = "wall or part"
                    alive[i] = False
        pm = pos * 1000.0
        rr = np.hypot(pm[:, 0], pm[:, 1])
        fl = fate == "floor"
        res[f"{d_um} um"] = dict(
            n=n, tau_p_s=tau0,
            settling_m_s=float(next_vt(d)),
            floor=float(fl.mean()), back_on_d75_plate=float((fl & (rr < 37.5)).mean()),
            back_on_d50_plate=float((fl & (rr < 25)).mean()),
            outlet_slot=float((fate == "outlet slot").mean()), wall_or_part=float((fate == "wall or part").mean()),
            ceiling=float((fate == "ceiling").mean()), slide_recess=float((fate == "slide recess").mean()),
            airborne_after_2s=float((fate == "airborne").mean()),
            median_rise_mm=float(np.median(zmax) * 1000), p95_rise_mm=float(np.percentile(zmax, 95) * 1000),
            median_landing_y_mm=float(np.median(pm[fl, 1])) if fl.any() else None,
            median_travel_mm=float(np.median(np.hypot(pm[fl, 0], pm[fl, 1]))) if fl.any() else None)
        lands[d_um] = (pm[fl, 0], pm[fl, 1])
    return res, lands


def next_vt(d):
    """Terminal settling speed in still argon with Schiller-Naumann drag."""
    v = RHO_P * d * d * G / (18 * MU)
    for _ in range(50):
        re = RHO * v * d / MU
        v = RHO_P * d * d * G / (18 * MU * (1 + 0.15 * re ** 0.687))
    return v


def track_condensate(cs, n=1500, t_end=12.0, dt=4e-3, seed=2, sc_t=0.7, zr=(1.0, 10.0)):
    """Tracers released over the Ø50 plate at 1-10 mm, moved by the mean flow plus a random walk with the RANS eddy
    diffusivity (nu + nut / Sc_t). Fates are first passages: out through the outlet slot, into the slide recess."""
    rng = np.random.default_rng(seed)
    r = 25.0 * np.sqrt(rng.random(n))
    th = 2 * np.pi * rng.random(n)
    pos = np.column_stack([r * np.cos(th), r * np.sin(th), rng.uniform(zr[0], zr[1], n)])  # mm
    fate = np.array(["chamber"] * n, dtype=object)
    t_out = np.full(n, np.nan)
    near_window = np.zeros(n, bool)
    above_60 = np.zeros(n, bool)
    alive = np.ones(n, bool)
    nu = MU / RHO
    paths = []
    keep = rng.choice(n, 12, replace=False)
    path_buf = {int(i): [pos[i].copy()] for i in keep}
    for step in range(int(t_end / dt)):
        ia = np.where(alive)[0]
        if not len(ia):
            break
        p = pos[ia]
        u = cs.U(p) * 1000.0                                                                  # mm/s
        D = (nu + np.maximum(cs("nut", p), 0) / sc_t) * 1e6                                  # mm2/s
        new = p + u * dt + np.sqrt(2 * D * dt)[:, None] * rng.standard_normal(p.shape)
        ok = cs.is_fluid(new)
        p = np.where(ok[:, None], new, p)
        pos[ia] = p
        x, y, z = p[:, 0], p[:, 1], p[:, 2]
        out = (z < -2.0) & (np.abs(x) < 62) & (y > -94) & (y < -86)
        slide = (z > 120.0) & (np.abs(x) < 25) & (np.abs(y) < 25)
        near = (z > 105.0) & (np.hypot(x, y) < 30)
        near_window[ia[near]] = True
        above_60[ia[z > 60.0]] = True
        fate[ia[out]] = "outlet"
        fate[ia[slide]] = "slide recess"
        t_out[ia[out]] = (step + 1) * dt
        alive[ia[out | slide]] = False
        if step % 10 == 0:
            for i in path_buf:
                if alive[i] or len(path_buf[i]) < 2 or not np.allclose(path_buf[i][-1], pos[i]):
                    path_buf[i].append(pos[i].copy())
    res = dict(n=n, release_z_mm=list(zr), t_end_s=t_end, outlet=float((fate == "outlet").mean()), slide_recess=float((fate == "slide recess").mean()),
               still_in_chamber=float((fate == "chamber").mean()), passed_within_30mm_of_window_axis_above_z105=float(near_window.mean()),
               rose_above_z60=float(above_60.mean()),
               median_time_to_outlet_s=float(np.nanmedian(t_out)) if np.isfinite(t_out).any() else None,
               p90_time_to_outlet_s=float(np.nanpercentile(t_out, 90)) if np.isfinite(t_out).sum() > 10 else None)
    return res, [np.array(v) for v in path_buf.values()]


# ------------------------------------------------------------------ figures
def outline_xy(ax):
    ax.add_patch(plt.Rectangle((-140, -95), 280, 190, fill=False, ec=INK2, lw=0.8))
    for d in (25, 50, 75):
        ax.add_patch(plt.Circle((0, 0), d / 2, fill=False, ec=INK, lw=0.7, ls="--"))
    ax.plot([-60, 60], [95, 95], color=ORANGE, lw=3, solid_capstyle="butt")
    ax.plot([-62, 62], [-90, -90], color=AQUA, lw=3, solid_capstyle="butt")
    ax.set_aspect("equal")
    ax.set_xlabel("x (mm), recoat direction")
    ax.set_ylabel("y (mm), back wall up")


def fig_planes(cs, tag, vmax=3.0):
    fig, axs = plt.subplots(2, 2, figsize=(11, 7.6), constrained_layout=True)
    for ax, z in zip(axs.ravel(), (3.0, 10.0, 60.0, 115.0)):
        x, y, U = plane_xy(cs, z)
        sp = np.hypot(U[0], U[1])
        im = ax.pcolormesh(x, y, sp, cmap="Blues", vmin=0, vmax=vmax, shading="auto")
        ax.streamplot(x, y, np.nan_to_num(U[0]), np.nan_to_num(U[1]), color=INK2, density=1.1, linewidth=0.5, arrowsize=0.6)
        outline_xy(ax)
        if z > 110:
            ax.add_patch(plt.Rectangle((-25, -25), 50, 50, fill=False, ec=ORANGE, lw=1.0))
            ax.add_patch(plt.Rectangle((-32, -42), 64, 6, fc="#bbbbbb", ec=INK2, lw=0.5))
        ax.set_title(f"z = {z:g} mm above the powder: horizontal speed (m/s) and streamlines", fontsize=9, color=INK)
        ax.set_xlim(-141, 141)
        ax.set_ylim(-96, 96)
    fig.colorbar(im, ax=axs, shrink=0.6, label="horizontal speed (m/s)")
    fig.suptitle(f"Argon cross-flow, {tag}: inlet slot (orange) on the back wall, outlet slot (aqua) in the floor; "
                 "dashed circles = Ø25 / Ø50 / Ø75 plates", fontsize=9.5, color=INK)
    return fig


def fig_midplane(cs, tag, vmax=3.0, x0=0.0):
    y, z, U = plane_yz(cs, x0)
    sp = np.sqrt(U[1] ** 2 + U[2] ** 2)
    fig, ax = plt.subplots(figsize=(11, 6.2), constrained_layout=True)
    im = ax.pcolormesh(y, z, sp, cmap="Blues", vmin=0, vmax=vmax, shading="auto")
    ax.streamplot(y, z, np.nan_to_num(U[1]), np.nan_to_num(U[2]), color=INK2, density=1.6, linewidth=0.55, arrowsize=0.6)
    for yy in (-37.5, 37.5):
        ax.plot([yy, yy], [-1.5, 0], color=INK, lw=2)
    ax.plot([-37.5, 37.5], [0, 0], color=INK, lw=2.5)
    ax.text(0, -6, "Ø75 plate", ha="center", va="top", color=INK, fontsize=8)
    ax.text(124, 30, "inlet plenum\n(KF-25 at back)", ha="center", color=INK, fontsize=8)
    ax.text(-90, -40, "outlet slot and\nunder-floor channel", ha="center", color=INK, fontsize=8)
    ax.text(0, 129, "cover slide", ha="center", color=INK, fontsize=8)
    ax.set_aspect("equal")
    ax.set_xlim(-112, 144)
    ax.set_ylim(-34, 132)
    ax.invert_xaxis()
    ax.set_xlabel("y (mm): flow runs left to right, from the back wall (inlet, left) to the door (outlet, right)")
    ax.set_ylabel("z (mm) above the powder")
    fig.colorbar(im, ax=ax, shrink=0.7, label="in-plane speed (m/s)")
    ax.set_title(f"Mid-plane x = {x0:g} mm, {tag}: speed and streamlines", color=INK)
    return fig


def fig_profiles(fine, coarse):
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.8), constrained_layout=True)
    y = np.linspace(-94, 94, 189)
    for z, ls in ((1.0, ":"), (3.0, "-"), (10.0, "--")):
        for cs, col, lab in ((fine, BLUE, "fine"), (coarse, ORANGE, "coarse")):
            if cs is None:
                continue
            u = cs("Uy", np.column_stack([np.zeros_like(y), y, np.full_like(y, z)]))
            axs[0].plot(y, -u, color=col, ls=ls, lw=1.5, label=f"{lab}, z = {z:g} mm")
    axs[0].axvspan(-37.5, 37.5, color="#e8e8e4", zorder=0)
    axs[0].axhline(2.5, color=INK2, lw=0.7, ls="-.")
    axs[0].text(-90, 2.55, "2.5 m/s target", color=INK2, fontsize=7.5)
    axs[0].set_xlim(95, -95)
    axs[0].set_xlabel("y (mm) along the flow, x = 0 (grey = Ø75 plate)")
    axs[0].set_ylabel("cross-flow velocity -Uy (m/s)")
    axs[0].legend(fontsize=7, frameon=False)
    z = np.linspace(0.25, 119, 300)
    for (yy, nm), col in zip(((37.5, "upstream edge y = +37.5"), (0.0, "centre"), (-37.5, "downstream edge y = -37.5")), (BLUE, ORANGE, AQUA)):
        for cs, ls in ((fine, "-"), (coarse, "--")):
            if cs is None:
                continue
            u = cs("Uy", np.column_stack([np.zeros_like(z), np.full_like(z, yy), z]))
            axs[1].plot(-u, z, color=col, ls=ls, lw=1.4, label=f"{nm} ({'fine' if cs is fine else 'coarse'})")
    axs[1].axvline(0, color=INK2, lw=0.6)
    axs[1].set_ylim(0, 120)
    axs[1].set_xlabel("-Uy (m/s); negative = flowing back toward the inlet")
    axs[1].set_ylabel("z (mm)")
    axs[1].legend(fontsize=6.5, frameon=False, loc="upper right")
    for cs, col, lab in ((fine, BLUE, "fine"), (coarse, ORANGE, "coarse")):
        if cs is None:
            continue
        x, uin, xo, uo = slot_profiles(cs)
        axs[2].plot(x, uin, color=col, lw=1.5, label=f"inlet slot, mean over its height ({lab})")
        axs[2].plot(xo, uo, color=col, lw=1.2, ls="--", label=f"outlet slot, 10 mm down ({lab})")
    axs[2].axhline(2.0, color=INK2, lw=0.7, ls="-.")
    axs[2].set_xlabel("x (mm) along the slots")
    axs[2].set_ylabel("velocity through the slot (m/s)")
    axs[2].legend(fontsize=6.5, frameon=False)
    axs[0].set_title("Along the flow over the plate", color=INK, fontsize=9)
    axs[1].set_title("Vertical profiles over the Ø75 plate", color=INK, fontsize=9)
    axs[2].set_title("Flow along the inlet and outlet slots", color=INK, fontsize=9)
    return fig


def fig_compare(items):
    """Baseline against a variant: along the flow at z = 3 and 10 mm, and vertical profiles at the plate centre."""
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.8), constrained_layout=True)
    y = np.linspace(-94, 94, 189)
    z = np.linspace(0.25, 125, 300)
    for cs, lab, col in items:
        if cs is None:
            continue
        for zz, ls in ((3.0, "-"), (10.0, "--")):
            u = cs("Uy", np.column_stack([np.zeros_like(y), y, np.full_like(y, zz)]))
            axs[0].plot(y, -u, color=col, ls=ls, lw=1.5, label=f"{lab}, z = {zz:g} mm")
        u = cs("Uy", np.column_stack([np.zeros_like(z), np.zeros_like(z), z]))
        axs[1].plot(-u, z, color=col, lw=1.5, label=lab)
    axs[0].axvspan(-37.5, 37.5, color="#e8e8e4", zorder=0)
    axs[0].axhline(2.5, color=INK2, lw=0.7, ls="-.")
    axs[0].set_xlim(95, -95)
    axs[0].set_xlabel("y (mm) along the flow at x = 0 (grey = Ø75 plate)")
    axs[0].set_ylabel("-Uy (m/s)")
    axs[0].legend(fontsize=7, frameon=False)
    axs[1].axvline(0, color=INK2, lw=0.6)
    axs[1].set_xlabel("-Uy at the plate centre (m/s); negative = toward the inlet")
    axs[1].set_ylabel("z (mm)")
    axs[1].legend(fontsize=7, frameon=False)
    fig.suptitle("Coarse mesh: the drawn chamber against the 'fix' variants (screens in both slots, wider outlet, "
                 "upper slot under the lid)", fontsize=9, color=INK)
    return fig


def fig_shear(c, tau, thr, tag):
    fig, ax = plt.subplots(figsize=(8.2, 5.6), constrained_layout=True)
    s = (np.abs(c[:, 1]) < 95) & (np.abs(c[:, 0]) < 140)
    t = tau[s] * 1000
    vmax = max(120.0, thr[1] * 1000)
    tp = ax.tripcolor(c[s, 0], c[s, 1], np.clip(t, 0, vmax), cmap="Blues", vmin=0, vmax=vmax, shading="gouraud")
    cs_ = ax.tricontour(c[s, 0], c[s, 1], t, levels=[thr[0] * 1000, thr[1] * 1000], colors=[ORANGE, INK], linewidths=[1.0, 1.0])
    ax.clabel(cs_, fmt="%.0f mPa", fontsize=7)
    outline_xy(ax)
    fig.colorbar(tp, ax=ax, shrink=0.8, label="wall shear on the floor (mPa)")
    ax.set_title(f"Floor shear stress, {tag}\nShao & Lu threshold, loose 63 um Al in argon: {thr[0]*1000:.0f} mPa "
                 f"(orange) to {thr[1]*1000:.0f} mPa (black); 20 um: {thr[2]*1000:.0f}-{thr[3]*1000:.0f} mPa", fontsize=8, color=INK)
    return fig


def fig_particles(lands, paths):
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.6), constrained_layout=True)
    for (d, (x, y)), col in zip(lands.items(), (BLUE, ORANGE, AQUA)):
        axs[0].scatter(x, y, s=4, color=col, alpha=0.6, label=f"{d} um")
    outline_xy(axs[0])
    axs[0].set_xlim(-141, 141)
    axs[0].set_ylim(-96, 96)
    axs[0].legend(fontsize=7, frameon=False, markerscale=2, loc="upper right")
    axs[0].set_title("Where spatter lands (launched from the Ø50 area at 1-6 m/s)", fontsize=9, color=INK)
    for pth in paths:
        if len(pth) > 1:
            axs[1].plot(pth[:, 1], pth[:, 2], color=BLUE, lw=0.6, alpha=0.8)
    axs[1].add_patch(plt.Rectangle((-95, 0), 190, 120, fill=False, ec=INK2, lw=0.8))
    axs[1].add_patch(plt.Rectangle((-25, 120), 50, 6, fill=False, ec=ORANGE, lw=1))
    axs[1].plot([-37.5, 37.5], [0, 0], color=INK, lw=2.5)
    axs[1].set_xlim(100, -100)
    axs[1].set_ylim(-25, 130)
    axs[1].set_aspect("equal")
    axs[1].set_xlabel("y (mm), inlet (back wall) on the left")
    axs[1].set_ylabel("z (mm)")
    axs[1].set_title("Condensate tracers, side view (6 from 1-10 mm, 6 from 10-30 mm)", fontsize=8.5, color=INK, pad=12)
    return fig


def write_summary(res):
    """cfd_summary.md: the key numbers of every case side by side (all from cfd.json)."""
    names = [k for k in ("fine", "coarse") if k in res] + [k for k in res if k not in ("fine", "coarse", "threshold_shao_lu")]
    R = {k: res[k] for k in names}

    def row(label, fn):
        cells = []
        for k in names:
            try:
                cells.append(fn(R[k]))
            except (KeyError, TypeError, ZeroDivisionError):
                cells.append("-")
        return "| " + label + " | " + " | ".join(cells) + " |"

    def bed(z, d, key="mean"):
        return lambda r: f"{r['bed'][f'z{z}_d{d}'][key]:.2f}"

    def rng(z, d):
        return lambda r: (f"{r['bed'][f'z{z}_d{d}']['mean']:.2f} ({r['bed'][f'z{z}_d{d}']['min']:.2f}-"
                          f"{r['bed'][f'z{z}_d{d}']['max']:.2f}), CoV {100 * r['bed'][f'z{z}_d{d}']['cov']:.0f} %")
    lines = ["# Chamber cross-flow CFD: key numbers per case", "",
             "Written by `analysis/cfd/post.py` from `cfd.json`. Speeds in m/s (horizontal speed on discs centred on the plate), "
             "shear in Pa, pressures in Pa above the outlet flange. 'fix' = screens in both slots, 35 mm outlet channel with a "
             "KF-40 boot, 100 x 4 mm upper slot under the lid (see gas-flow.md).", "",
             "| | " + " | ".join(names) + " |", "|---|" + "---|" * len(names),
             row("cells / iterations", lambda r: f"{r['cells']/1000:.0f}k / {r['iterations']:.0f}"),
             row("bed slot + upper slot flow (L/min)", lambda r: f"{r['q_lpm']:g} + {r.get('upper_slot_lpm', 0):g}")]
    for z in (1, 3, 10):
        for d in (25, 50, 75):
            lines.append(row(f"speed at {z} mm over Ø{d}: mean (min-max), CoV", rng(z, d)))
    lines += [row("share of Ø75 >= 2.5 m/s at 3 mm", lambda r: f"{100 * r['bed']['z3_d75']['frac_ge_2p5']:.0f} %"),
              row("inlet slot: min / max / middle-third share", lambda r: f"{r['inlet_slot']['min']:.2f} / {r['inlet_slot']['max']:.2f} / {100 * r['inlet_slot']['centre_third_share']:.0f} %"),
              row("outlet slot: min / max / right-half share", lambda r: f"{r['outlet_slot']['min']:.2f} / {r['outlet_slot']['max']:.2f} / {100 * r['outlet_slot']['right_half_share']:.0f} %"),
              row("pressure drop flange to flange (Pa)", lambda r: f"{r['dp_inlet_to_outlet_Pa']:.0f}"),
              row("bed shear over Ø75: mean / max (Pa)", lambda r: f"{r['floor_shear_Pa']['d75']['mean']:.3f} / {r['floor_shear_Pa']['d75']['max']:.3f}"),
              row("highest shear on the floor (Pa)", lambda r: f"{r['floor_shear_Pa']['floor_max']:.2f}"),
              row("under the slide (z 121): mean speed, mean Uy", lambda r: f"{r['window']['z121']['mean_speed']:.2f}, {r['window']['z121']['mean_uy']:+.2f}"),
              row("gas over the plate at z 30-120 flowing toward the inlet", lambda r: f"{100 * r['recirculation']['over plate, z 30-120 mm']['frac_reversed']:.0f} %")]
    for rel, key in (("1-10 mm", "condensate"), ("10-30 mm", "condensate_released_10_30mm")):
        lines += [row(f"condensate from {rel}: out in 12 s / median time (s)", lambda r, k=key: f"{100 * r[k]['outlet']:.0f} % / {r[k]['median_time_to_outlet_s']:.2f}"),
                  row(f"condensate from {rel}: near the window / into the slide recess", lambda r, k=key: f"{100 * r[k]['passed_within_30mm_of_window_axis_above_z105']:.1f} % / {100 * r[k]['slide_recess']:.1f} %")]
    for d in ("50 um", "100 um", "150 um"):
        lines.append(row(f"spatter {d}: back on Ø75 / lid / slide footprint", lambda r, d=d: f"{100 * r['spatter'][d]['back_on_d75_plate']:.0f} / {100 * (r['spatter'][d]['ceiling'] + r['spatter'][d]['slide_recess']):.0f} / {100 * r['spatter'][d]['slide_recess']:.0f} %"))
    th = res["threshold_shao_lu"]
    lines += ["", "Shao & Lu (2000) entrainment threshold for loose AlSi10Mg spheres in argon (Pa):", "",
              "| d | γ = 1.65e-4 N/m | 3e-4 | 5e-4 |", "|---|---|---|---|"]
    for d in (20, 40, 63):
        lines.append(f"| {d} um | " + " | ".join(f"{th[f'{d} um, gamma {g:g} N/m']['tau_Pa']:.3f}" for g in (1.65e-4, 3e-4, 5e-4)) + " |")
    (OUT / "cfd_summary.md").write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fine", required=True)
    ap.add_argument("--coarse")
    ap.add_argument("--variant", action="append", default=[])
    ap.add_argument("--no-particles", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    fine = Case(a.fine)
    coarse = Case(a.coarse) if a.coarse else None
    thr = {f"{d} um, gamma {g:g} N/m": shao_lu(d * 1e-6, g) for d in (20, 40, 63) for g in (1.65e-4, 3e-4, 5e-4)}
    res = dict(threshold_shao_lu={k: dict(u_star_m_s=v[0], tau_Pa=v[1]) for k, v in thr.items()})
    cases = {"fine": fine, "coarse": coarse}
    cases.update({pathlib.Path(v).name: Case(v) for v in a.variant})
    for name, cs in cases.items():
        if cs is None:
            continue
        sh, c, tau = floor_shear(cs)
        pr = pressure(cs)
        x, uin, xo, uo = slot_profiles(cs)
        res[name] = dict(case=str(cs.path), cells=cs.ncells, iterations=cs.time, q_lpm=cs.meta["q_lpm"],
                         variant=cs.meta.get("variant", "baseline"), upper_slot_lpm=cs.meta.get("upper_lpm", 0.0),
                         bed=bed_stats(cs), floor_shear_Pa=sh, pressure_Pa=pr,
                         dp_inlet_to_outlet_Pa=pr["inlet port"] - pr["outlet port"],
                         inlet_slot=dict(max=float(uin.max()), min=float(uin.min()), mean=float(uin.mean()),
                                         centre_third_share=float(uin[np.abs(x) < 20].sum() / uin.sum())),
                         outlet_slot=dict(max=float(uo.max()), min=float(uo.min()), mean=float(uo.mean()),
                                          right_half_share=float(np.clip(uo[xo > 0], 0, None).sum() / np.clip(uo, 0, None).sum())),
                         window=window_stats(cs), recirculation=recirculation(cs))
        print(name, json.dumps({k: res[name][k] for k in ("cells", "dp_inlet_to_outlet_Pa", "inlet_slot", "outlet_slot")}))
        tag = f"{name} mesh, {cs.ncells/1000:.0f}k cells, {cs.meta['q_lpm']:g} L/min" if name in ("fine", "coarse") else f"{name}, {cs.meta['q_lpm']:g} L/min"
        if name in ("fine",) or name not in ("coarse",):
            fig_planes(cs, tag).savefig(OUT / f"planes_{name}.png", dpi=110)
            fig_midplane(cs, tag).savefig(OUT / f"midplane_{name}.png", dpi=110)
            fig_shear(c, tau, (shao_lu(63e-6, 1.65e-4)[1], shao_lu(63e-6, 5e-4)[1], shao_lu(20e-6, 1.65e-4)[1],
                               shao_lu(20e-6, 5e-4)[1]), tag).savefig(OUT / f"floor_shear_{name}.png", dpi=110)
            plt.close("all")
        (OUT / "cfd.json").write_text(json.dumps(res, indent=1))
    fig_profiles(fine, coarse).savefig(OUT / "profiles_mesh_check.png", dpi=110)
    plt.close("all")
    for name, cs in cases.items():
        if a.no_particles or cs is None:
            continue
        sp, lands = track_spatter(cs)
        cd, paths = track_condensate(cs)
        cd2, paths2 = track_condensate(cs, zr=(10.0, 30.0), seed=3)
        res[name]["spatter"] = sp
        res[name]["condensate"] = cd
        res[name]["condensate_released_10_30mm"] = cd2
        paths = paths[:6] + paths2[:6]
        fig_particles(lands, paths).savefig(OUT / f"particles_{name}.png", dpi=110)
        plt.close("all")
        print(name, json.dumps(sp, indent=1), json.dumps(cd, indent=1), json.dumps(cd2, indent=1))
        (OUT / "cfd.json").write_text(json.dumps(res, indent=1))
    if a.variant:
        cols = (ORANGE, AQUA, "#6250d6")
        items = [(coarse, "baseline, 115 L/min", BLUE)] + [
            (cases[pathlib.Path(v).name], f"fix, {cases[pathlib.Path(v).name].meta['q_lpm']:g} + "
             f"{cases[pathlib.Path(v).name].meta.get('upper_lpm', 0):g} L/min", cols[i % 3]) for i, v in enumerate(a.variant)]
        fig_compare(items).savefig(OUT / "compare_variants.png", dpi=110)
        plt.close("all")
    (OUT / "cfd.json").write_text(json.dumps(res, indent=1))
    write_summary(res)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
