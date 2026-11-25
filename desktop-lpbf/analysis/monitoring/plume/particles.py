"""Condensate and spatter in the solved chamber flow: where they go, how much reaches each window, LW purge on and off
(issue #260; monitoring/plume.md §1).

Reads cases written by make_case_plume.py and solved by analysis/cfd/run_case.sh, through analysis/cfd/post.py's Case
(imported, not edited). One-way coupled, frozen steady RANS field, as post.py; new here:
  - Condensate (0.05-1 um aggregates): tracers moved by the mean flow plus a random walk with D = D_Brownian + nu_t / Sc_t
    (Sc_t 0.7; post.py adds the gas's own nu, which suits a gas tracer but overstates a particle's diffusion in still gas).
    Settling (< 0.1 mm/s at 1 um) and inertia (Stokes number ~1e-3) are left out. Released continuously from five plate
    positions (centre, +/-25 mm in x and y) in two height bands: 0.5-5 mm (conduction mode and the keyhole jet's base) and
    5-20 mm (the keyhole jet's top; plume_jet.py). The time each tracer spends in a control volume gives the steady
    concentration there per unit source rate, C/S = E[time in V] / V (s/m3). Deposition on a window is J = v_d C_near, with
    C_near over the 2 mm next to the window and v_d from Lai & Nazaroff (2000, J. Aerosol Sci. 31:463-476; vertical or
    downward-facing smooth surface, friction velocity from the CFD's wall shear on that patch), plus a thermophoretic term
    when the window is colder than the gas (Talbot-type, K_th 0.5, over a 2 mm thermal layer).
  - Spatter (20-200 um Al): Schiller-Naumann drag and gravity in the CFD velocity field, launched from the same five
    positions with the speed and direction distributions of spatter.py; fates counted per patch: each viewport's cover slide
    or window, the laser slide, the plate (bed), the floor, the outlet slot, the walls and lid.
Thermophoresis away from the 200 C plate and the plate's buoyancy are not in the flow field (isothermal CFD); see plume.md.

Run: /tmp/capmem 4 /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/plume/particles.py /tmp/plume/p200 /tmp/plume/p200_lw3 ...
Writes analysis/out/monitoring/plume/particles.json (merged per case) and particles_<case>.png.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE.parents[1] / "out" / "monitoring" / "plume"
_s = importlib.util.spec_from_file_location("cfdpost", ROOT / "analysis" / "cfd" / "post.py")
PO = importlib.util.module_from_spec(_s)
_s.loader.exec_module(PO)
_s2 = importlib.util.spec_from_file_location("spatter", HERE / "spatter.py")
SP = importlib.util.module_from_spec(_s2)
_s2.loader.exec_module(SP)

RHO, MU, G = 1.65, 2.26e-5, 9.81
NU = MU / RHO
KB, T_GAS, LAMBDA_AR = 1.380649e-23, 298.15, 68e-9       # argon mean free path at ~1 atm, 25 C
RELEASES = [(0.0, 0.0), (25.0, 0.0), (-25.0, 0.0), (0.0, 25.0), (0.0, -25.0)]
WINDOWS = ("LW", "BW", "LP", "LC", "laser")


def cunningham(d):
    kn = 2 * LAMBDA_AR / d
    return 1 + kn * (1.257 + 0.4 * math.exp(-1.1 / kn))


def d_brownian(d):
    return KB * T_GAS * cunningham(d) / (3 * math.pi * MU * d)


def v_settle(d, rho_p=2700.0):
    return rho_p * d * d * G * cunningham(d) / (18 * MU)


def lai_nazaroff(d, u_star, orientation="vertical", rho_p=2700.0):
    """Deposition velocity (m/s) onto a smooth surface, Lai & Nazaroff (2000)."""
    D = d_brownian(d)
    sc = NU / D
    rp = d / 2 * u_star / NU
    A = 10.92 * sc ** (-1 / 3)
    a = 0.5 * math.log((A + 4.3) ** 3 / (1 / sc + 0.0609)) + math.sqrt(3) * math.atan((8.6 - A) / (math.sqrt(3) * A))
    b = 0.5 * math.log((A + rp) ** 3 / (1 / sc + 7.669e-4 * rp ** 3)) + math.sqrt(3) * math.atan((2 * rp - A) / (math.sqrt(3) * A))
    I = 3.64 * sc ** (2 / 3) * (a - b) + 39.0
    vs = v_settle(d, rho_p)
    if orientation == "vertical":
        return u_star / I
    if orientation == "up":
        return vs / (1 - math.exp(-vs * I / u_star))
    return vs / (math.exp(vs * I / u_star) - 1)          # downward-facing


def v_thermophoresis(dT, T=320.0, delta=2e-3, K=0.5):
    return K * NU * (dT / delta) / T


def face_cell(meta, ax, fa, low):
    """Size (mm) of the mesh cell that touches a window face at coordinate fa on axis ax, on the fluid side."""
    L, N = meta["lines"]["xyz"[ax]], meta["n"]["xyz"[ax]]
    for i in range(len(L) - 1):
        if low and abs(L[i] - fa) < 1e-6:
            return (L[i + 1] - L[i]) / N[i]
        if not low and abs(L[i + 1] - fa) < 1e-6:
            return (L[i + 1] - L[i]) / N[i]
    return 2.0


def control_volumes(meta):
    """Recess boxes, the layer next to each window face (2 mm, or the cell touching it if thicker), and a column around the
    beam axis (mm)."""
    cv = {}
    vps = dict(meta["viewports"])
    vps["laser"] = dict(box=[-25.0, 25.0, -25.0, 25.0, 120.0, 126.0], face_axis=2, face_at=126.0, patch="slide", area_mm2=1600.0)
    for k, v in vps.items():
        b = list(v["box"])
        cv[f"{k} recess"] = b
        nb = list(b)
        ax, fa = v["face_axis"], v["face_at"]
        low = abs(b[2 * ax] - fa) < 1e-6                  # face at the low end of the box (LW: -x)
        th = max(2.0, face_cell(meta, ax, fa, low) + 0.01)
        if low:
            nb[2 * ax + 1] = fa + th
        else:
            nb[2 * ax] = fa - th
        if k == "laser":
            nb = [-20.0, 20.0, -20.0, 20.0, 124.0, 126.0]
        cv[f"{k} near face"] = nb
    cv["beam column z 20-120 (r < 5 mm)"] = "beam"
    cv["over plate z 0-20"] = [-37.5, 37.5, -37.5, 37.5, 0.0, 20.0]
    return cv, vps


def inside(b, p):
    return (p[:, 0] > b[0]) & (p[:, 0] < b[1]) & (p[:, 1] > b[2]) & (p[:, 1] < b[3]) & (p[:, 2] > b[4]) & (p[:, 2] < b[5])


def track_condensate(cs, zr, n_per=600, t_end=8.0, dt=1e-3, seed=11, sc_t=0.7, d_b=0.05e-6):
    rng = np.random.default_rng(seed)
    meta = cs.meta
    sl = meta["fluid"]["outlet slot"]
    pos = []
    for (x0, y0) in RELEASES:
        r = 3.0 * np.sqrt(rng.random(n_per))
        th = 2 * np.pi * rng.random(n_per)
        pos.append(np.column_stack([x0 + r * np.cos(th), y0 + r * np.sin(th), rng.uniform(zr[0], zr[1], n_per)]))
    pos = np.vstack(pos)
    n = len(pos)
    src = np.repeat(np.arange(len(RELEASES)), n_per)
    alive = np.ones(n, bool)
    fate = np.array(["chamber"] * n, dtype=object)
    t_out = np.full(n, np.nan)
    cv, vps = control_volumes(meta)
    tres = {k: np.zeros(n) for k in cv}
    entered = {k: np.zeros(n, bool) for k in vps}
    near_win_axis = np.zeros(n, bool)
    Db = d_brownian(d_b) * 1e6                                                   # mm2/s
    for step in range(int(t_end / dt)):
        ia = np.where(alive)[0]
        if not len(ia):
            break
        p = pos[ia]
        u = cs.U(p) * 1000.0
        D = Db + np.maximum(cs("nut", p), 0) / sc_t * 1e6
        new = p + u * dt + np.sqrt(2 * D * dt)[:, None] * rng.standard_normal(p.shape)
        ok = cs.is_fluid(new)
        p = np.where(ok[:, None], new, p)
        pos[ia] = p
        for k, b in cv.items():
            if b == "beam":
                m = (p[:, 2] > 20) & (p[:, 2] < 120) & (np.hypot(p[:, 0], p[:, 1]) < 5.0)
            else:
                m = inside(b, p)
            tres[k][ia[m]] += dt
        for k, v in vps.items():
            entered[k][ia[inside(v["box"], p)]] = True
        near_win_axis[ia[(p[:, 2] > 105.0) & (np.hypot(p[:, 0], p[:, 1]) < 30)]] = True
        out = (p[:, 2] < -2.0) & (p[:, 0] > sl[0]) & (p[:, 0] < sl[1]) & (p[:, 1] > sl[2]) & (p[:, 1] < sl[3])
        fate[ia[out]] = "outlet"
        t_out[ia[out]] = (step + 1) * dt
        alive[ia[out]] = False
    res = dict(n=n, release_z_mm=list(zr), t_end_s=t_end, outlet=float((fate == "outlet").mean()),
               still_in_chamber=float((fate == "chamber").mean()),
               median_time_to_outlet_s=float(np.nanmedian(t_out)) if np.isfinite(t_out).any() else None,
               passed_within_30mm_of_window_axis_above_z105=float(near_win_axis.mean()),
               entered_recess={k: float(v.mean()) for k, v in entered.items()},
               entered_recess_by_release={k: [float(v[src == i].mean()) for i in range(len(RELEASES))] for k, v in entered.items()})
    conc = {}
    for k, b in cv.items():
        if b == "beam":
            V = math.pi * 5.0 ** 2 * 100.0
        else:
            V = (b[1] - b[0]) * (b[3] - b[2]) * (b[5] - b[4])
        conc[k] = dict(volume_mm3=V, C_per_S_s_m3=float(tres[k].mean() / (V * 1e-9)),
                       C_per_S_by_release=[float(tres[k][src == i].mean() / (V * 1e-9)) for i in range(len(RELEASES))])
    res["concentration_per_source"] = conc
    return res


def wall_ustar(cs):
    out = {}
    for name in ("slide", "lwSlide", "bwWindow", "lpSlide", "lcWindow", "floor"):
        try:
            blk = cs.bnd[name]
            tau = np.linalg.norm(np.asarray(blk.cell_data["wallShearStress"]), axis=1)       # kinematic, m2/s2
            out[name] = dict(u_star_mean=float(np.sqrt(tau).mean()), u_star_max=float(np.sqrt(tau).max()),
                             tau_Pa_mean=float(tau.mean() * RHO))
        except (KeyError, TypeError):
            out[name] = None
    return out


def window_speeds(cs, vps):
    """Gas speed 1 mm in front of each window face (mean over the face)."""
    out = {}
    for k, v in vps.items():
        b, ax, fa = v["box"], v["face_axis"], v["face_at"]
        g = np.meshgrid(np.linspace(b[0] + 1, b[1] - 1, 7), np.linspace(b[2] + 1, b[3] - 1, 7), np.linspace(b[4] + 0.5, b[5] - 0.5, 4))
        P = np.column_stack([a.ravel() for a in g])
        low = abs(b[2 * ax] - fa) < 1e-6
        sgn = 1.0 if low else -1.0
        P[:, ax] = fa + sgn * max(1.0, 0.5 * face_cell(cs.meta, ax, fa, low))     # the centre of the cell at the face
        P = P[cs.is_fluid(P)]
        if not len(P):
            out[k] = None
            continue
        u = cs.U(P)
        out[k] = dict(mean_speed=float(np.linalg.norm(u, axis=1).mean()), mean_normal_out=float(sgn * u[:, ax].mean()))
    return out


def track_spatter(cs, vps, d_um, n_per=500, slow=False, seed=5, dt=5e-5, t_max=2.5, rho_p=2670.0):
    rng = np.random.default_rng(seed + d_um)
    pos, vel = [], []
    for (x0, y0) in RELEASES:
        p_, v_, _ = SP.sample_launch(n_per, rng, slow)
        p_[:, 0] = (x0 + 3.0 * (rng.random(n_per) - 0.5)) * 1e-3
        p_[:, 1] = (y0 + 3.0 * (rng.random(n_per) - 0.5)) * 1e-3
        pos.append(p_)
        vel.append(v_)
    pos, vel = np.vstack(pos), np.vstack(vel)
    n = len(pos)
    src = np.repeat(np.arange(len(RELEASES)), n_per)
    d = d_um * 1e-6
    tau0 = rho_p * d * d / (18 * MU)
    sl = cs.meta["fluid"]["outlet slot"]
    fate = np.array(["airborne"] * n, dtype=object)
    alive = np.ones(n, bool)
    zmax = pos[:, 2].copy()
    t = 0.0
    while alive.any() and t < t_max:
        ia = np.where(alive)[0]
        pm_old = pos[ia] * 1e3
        ug = cs.U(pm_old)
        rel = ug - vel[ia]
        rep = RHO * np.linalg.norm(rel, axis=1) * d / MU
        acc = rel * ((1 + 0.15 * rep ** 0.687) / tau0)[:, None]
        acc[:, 2] -= G
        vel[ia] += acc * dt
        pos[ia] += vel[ia] * dt
        zmax[ia] = np.maximum(zmax[ia], pos[ia, 2])
        t += dt
        pm = pos[ia] * 1e3
        ok = cs.is_fluid(pm)
        below = pm[:, 2] <= 0.0
        for j in np.where(~ok | below)[0]:
            i = ia[j]
            x, y, z = pm[j]
            xo, yo, zo = pm_old[j]
            if z <= 0.0 and not (sl[0] < x < sl[1] and sl[2] < y < sl[3]):
                fate[i] = "plate" if math.hypot(x, y) < 37.5 else "floor"
            elif z <= 0.0:
                if not ok[j]:
                    fate[i] = "outlet slot"
                else:
                    continue
            else:
                f = "wall or part"
                for k, v in vps.items():
                    b = v["box"]
                    if b[0] - 1 < xo < b[1] + 1 and b[2] - 1 < yo < b[3] + 1 and b[4] - 1 < zo < b[5] + 1:
                        ax, fa = v["face_axis"], v["face_at"]
                        lo = abs(b[2 * ax] - fa) < 1e-6
                        crossed = (pm[j][ax] <= fa + 1.0) if lo else (pm[j][ax] >= fa - 1.0)
                        f = f"{k} window" if crossed else f"{k} recess wall"
                        break
                if f == "wall or part" and z >= 119.0:
                    f = "lid"
                fate[i] = f
            alive[i] = False
        # a particle that fell into the outlet slot and keeps going down is gone
        gone = ia[(pm[:, 2] < -15.0)]
        fate[gone] = "outlet slot"
        alive[gone] = False
    keys = sorted(set(fate))
    return dict(d_um=d_um, n=n, slow=slow, fates={k: float((fate == k).mean()) for k in keys},
                windows={k: float((fate == f"{k} window").mean()) for k in vps},
                windows_by_release={k: [float(((fate == f"{k} window") & (src == i)).sum() / n_per) for i in range(len(RELEASES))] for k in vps},
                median_rise_mm=float(np.median(zmax) * 1e3), p95_rise_mm=float(np.percentile(zmax, 95) * 1e3))


def deposition(conc, ustar, vps):
    """Deposition velocity and flux per unit condensate source (kg/m2/s per kg/s) on each window, by size and window
    temperature offset."""
    orient = {"LW": "vertical", "BW": "vertical", "LP": "down", "LC": "down", "laser": "down"}
    patch = {"LW": "lwSlide", "BW": "bwWindow", "LP": "lpSlide", "LC": "lcWindow", "laser": "slide"}
    out = {}
    for k in vps:
        us = ustar.get(patch[k])
        u_star = max(1e-3, us["u_star_mean"]) if us else 0.01
        c = conc[f"{k} near face"]["C_per_S_s_m3"]
        row = dict(u_star=u_star, C_per_S=c)
        for d_um in (0.05, 0.1, 0.3, 1.0):
            d = d_um * 1e-6
            vd = max(lai_nazaroff(d, u_star, orient[k]), d_brownian(d) / 2e-3)
            for dT in (0.0, 10.0):
                v = vd + (v_thermophoresis(dT) if dT else 0.0)
                row[f"{d_um:g} um, dT {dT:g} K"] = dict(v_d=v, J_per_S=v * c)
        out[k] = row
    return out


def figure(name, res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.2), constrained_layout=True)
    wins = list(res["spatter"]["Ly 2017 speeds"]["100"]["windows"].keys())
    ds = sorted(int(k) for k in res["spatter"]["Ly 2017 speeds"])
    cols = ("#eb6834", "#1baf7a", "#6250d6", "#52514e", "#2a78d6")
    for w, c in zip(wins, cols):
        axs[0].plot(ds, [100 * res["spatter"]["Ly 2017 speeds"][str(d)]["windows"][w] for d in ds], color=c, lw=1.5, marker="o", ms=3, label=w)
        if "slow (speeds / 2)" in res["spatter"]:
            axs[0].plot(ds, [100 * res["spatter"]["slow (speeds / 2)"][str(d)]["windows"][w] for d in ds], color=c, lw=1.0, ls="--")
    axs[0].set_xlabel("Al spatter diameter (um)")
    axs[0].set_ylabel("share of launches hitting the window (%)")
    axs[0].set_title(f"{name}: spatter on each window (solid: Ly 2017 speeds, dashed: halved)", fontsize=9)
    axs[0].legend(fontsize=7, frameon=False)
    bands = list(res["condensate"].keys())
    x = np.arange(len(WINDOWS))
    for i, (bnd, c) in enumerate(zip(bands, ("#2a78d6", "#eb6834"))):
        vals = [res["condensate"][bnd]["concentration_per_source"][f"{w} near face"]["C_per_S_s_m3"] for w in WINDOWS]
        axs[1].bar(x + (i - 0.5) * 0.38, vals, width=0.36, color=c, label=f"released {bnd}")
    axs[1].set_xticks(x, [f"{w}" for w in WINDOWS])
    axs[1].set_yscale("log")
    axs[1].set_ylabel("condensate next to the window per unit source (s/m³)")
    axs[1].set_title("Steady condensate concentration 0-2 mm from each window, per kg/s released", fontsize=9)
    axs[1].legend(fontsize=7, frameon=False)
    fig.savefig(OUT / f"particles_{name}.png", dpi=110)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cases", nargs="+")
    ap.add_argument("--n-per", type=int, default=600)
    ap.add_argument("--no-spatter", action="store_true")
    ap.add_argument("--no-slow", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    jpath = OUT / "particles.json"
    allres = json.loads(jpath.read_text()) if jpath.exists() else {}
    for path in a.cases:
        cs = PO.Case(path)
        name = pathlib.Path(path).name
        cv, vps = control_volumes(cs.meta)
        res = dict(case=path, cells=cs.ncells, iterations=cs.time, q_lpm=cs.meta["q_lpm"], upper_lpm=cs.meta["upper_lpm"],
                   lw_purge_lpm=cs.meta.get("lw_purge_lpm", 0.0), recoater_x=cs.meta.get("x_recoater"))
        res["u_star"] = wall_ustar(cs)
        res["gas_at_windows"] = window_speeds(cs, vps)
        res["bed"] = {k: v for k, v in PO.bed_stats(cs).items() if k in ("z1_d75", "z3_d75", "z10_d75")}
        res["window_z121"] = PO.window_stats(cs)["z121"]
        res["condensate"] = {}
        for zr in ((0.5, 5.0), (5.0, 20.0)):
            key = f"{zr[0]:g}-{zr[1]:g} mm"
            res["condensate"][key] = track_condensate(cs, zr, n_per=a.n_per)
            c = res["condensate"][key]
            print(name, key, "out", round(c["outlet"], 3), "left", round(c["still_in_chamber"], 3), "entered",
                  {k: round(v, 4) for k, v in c["entered_recess"].items()},
                  {k: f"{v['C_per_S_s_m3']:.3g}" for k, v in c["concentration_per_source"].items()}, flush=True)
        res["deposition_per_source"] = {key: deposition(c["concentration_per_source"], res["u_star"], vps)
                                        for key, c in res["condensate"].items()}
        if not a.no_spatter:
            res["spatter"] = {}
            for slow in ((False,) if a.no_slow else (False, True)):
                lab = "slow (speeds / 2)" if slow else "Ly 2017 speeds"
                res["spatter"][lab] = {}
                for d_um in (20, 35, 50, 100, 150, 200):
                    r = track_spatter(cs, vps, d_um, n_per=300 if d_um < 100 else 240, slow=slow)
                    res["spatter"][lab][str(d_um)] = r
                    print(name, lab, d_um, {k: round(v, 4) for k, v in r["fates"].items()}, flush=True)
            figure(name, res)
        allres[name] = res
        jpath.write_text(json.dumps(allres, indent=1, default=float))
    print("wrote", jpath)


if __name__ == "__main__":
    main()
