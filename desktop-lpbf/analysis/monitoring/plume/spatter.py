"""Spatter ballistics, cooling and what the cameras see of it, without the CFD (issue #260; monitoring/plume.md §2).

1. Flight in still argon and in a 1-D cross-flow profile U(z) (gas-flow.md §0.5, fixed layout at 200 + 40 L/min):
   Schiller-Naumann drag, Cd = 24/Re (1 + 0.15 Re^0.687), gravity, Al (2500 kg/m3 liquid; 2670 solid) against steel (7000).
   Max height, range, flight time per size and launch speed; then a Monte Carlo of launches from the Ø50 area against the
   chamber's walls with the viewport apertures from cad/monitoring_spec.py (as boxes, like make_case_plume.py), counting what
   lands on the LW and LP cover slides, the layer camera's bore and the laser slide.
2. Launch distributions:
   - speeds by mechanism, Ly et al. 2017 (Sci. Rep. 7:4085, doi:10.1038/s41598-017-04237-z; 316L and Ti-6Al-4V at 1 atm Ar,
     as summarised in Li et al. 2022, Micromachines 13:1366, doi:10.3390/mi13081366): hot entrainment 60 % at 6-20 m/s, cold
     entrainment 25 % at 2-4 m/s, recoil droplet break-up 15 % at 3-8 m/s. No Al-specific speed distribution was found; the
     same distribution is used for Al, and a slow variant (all speeds / 2) brackets it.
   - sizes: powder spatter = the feedstock, 15-63 um; droplet spatter >= 63 um (Nagato et al. 2023, Mater. Des. 227:111696,
     doi:10.1016/j.matdes.2023.111696, AlSi10Mg on an SLM280HL at 200 C), up to 200 um here (assumed); about 4 powder spatters
     to 1 droplet spatter by number (their Fig. 4c, 350 W, 1.6 m/s).
   - directions: polar angle from vertical uniform in 0-70 deg, azimuth uniform (the scan direction rotates from layer to
     layer, so the backward bias averages out over a build) - assumed.
3. Cooling: lumped capacitance (Biot << 1) with Ranz-Marshall convection, Nu = 2 + 0.6 Re^0.5 Pr^(1/3), argon properties at
   the film temperature, grey radiation, and latent heat over the freezing range.
4. Visibility: photoelectrons per pixel from a glowing sphere (Planck, grey emissivity) for each camera, against a 100 e-
   threshold; the glow time is how long the particle stays above that temperature. Motion blur = speed x exposure / pixel.

Run: /tmp/capmem 2 /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/plume/spatter.py
Writes analysis/out/monitoring/plume/spatter.json and spatter.png.
"""
from __future__ import annotations

import importlib.util
import json
import math
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE.parents[1] / "out" / "monitoring" / "plume"
G, RHO_G, MU_G = 9.81, 1.65, 2.26e-5
H, C, KB, SIGMA = 6.62607e-34, 2.99792e8, 1.380649e-23, 5.670374e-8

# 1-D cross-flow profile over the plate centre, -Uy (m/s) at z (mm): gas-flow.md §0.5 fix200 (1, 3, 10 mm), jet ~20 mm thick,
# upper chamber ~0.3 m/s toward the door with the upper slot (its z 121 value); replaced by the CFD in particles.py
PROFILE_Z = np.array([0.0, 1.0, 3.0, 10.0, 20.0, 30.0, 60.0, 100.0, 120.0])
PROFILE_U = np.array([0.0, 2.19, 2.94, 2.34, 1.0, 0.3, 0.1, 0.3, 0.29])

MATERIALS = {"Al": dict(rho=2500.0, cp=1180.0, L=397e3, T_liq=870.0, T_sol=830.0, eps=0.15),     # AlSi10Mg-like
             "steel": dict(rho=7000.0, cp=790.0, L=270e3, T_liq=1720.0, T_sol=1670.0, eps=0.35)}  # 316L-like

# launch mechanisms (Ly et al. 2017): share, speed range (m/s)
MECH = [("hot entrainment", 0.60, (6.0, 20.0)), ("cold entrainment", 0.25, (2.0, 4.0)), ("droplet break-up", 0.15, (3.0, 8.0))]

# cameras (monitoring.md §3 and §1): name -> (pixel at the plate um, lens aperture D mm, distance mm, band um (lo, hi), QE)
CAMERAS = {
    "LW Chronos 2.1-HD + 50 mm f/4, 850 +/- 5 nm": dict(px=29.0, D=12.5, R=161.0, band=(0.845, 0.855), qe=0.2),
    "LW Chronos 2.1-HD + 50 mm f/4, 450-950 nm (notch at 1070)": dict(px=29.0, D=12.5, R=161.0, band=(0.45, 0.95), qe=0.3),
    "LW IMX296 + 50 mm f/2.8, 850 +/- 5 nm": dict(px=10.0, D=17.9, R=161.0, band=(0.845, 0.855), qe=0.15),
    "Layer camera Pi HQ + 12 mm f/2.8, 400-650 nm (its IR-cut filter)": dict(px=25.0, D=4.3, R=205.0, band=(0.40, 0.65), qe=0.5),
}
THRESH_E = 100.0                                         # e- per pixel for a clear detection (~5x read noise of ~20 e-)


def drag_acc(rel, d, rho_p):
    vr = np.linalg.norm(rel, axis=-1)
    re = RHO_G * vr * d / MU_G
    tau = rho_p * d * d / (18 * MU_G)
    return rel * ((1 + 0.15 * re ** 0.687) / tau)[..., None]


def u_gas(z_mm, cross=True):
    if not cross:
        return np.zeros(z_mm.shape + (3,))
    u = np.zeros(z_mm.shape + (3,))
    u[..., 1] = -np.interp(z_mm, PROFILE_Z, PROFILE_U)
    return u


def fly_single(d, v0, elev_deg, rho_p, cross=False, dt=5e-5, tmax=3.0):
    """One trajectory launched across the flow (+x) from z = 0.3 mm; max height, range, drift along the flow, flight time."""
    el = math.radians(elev_deg)
    x, y, z = 0.0, 0.0, 0.3e-3
    vx, vy, vz = v0 * math.cos(el), 0.0, v0 * math.sin(el)
    tau = rho_p * d * d / (18 * MU_G)
    zmax, t = z, 0.0
    while t < tmax:
        ug = -float(np.interp(z * 1e3, PROFILE_Z, PROFILE_U)) if cross else 0.0
        rx, ry, rz = -vx, ug - vy, -vz
        vr = math.sqrt(rx * rx + ry * ry + rz * rz)
        f = (1 + 0.15 * (RHO_G * vr * d / MU_G) ** 0.687) / tau
        vx += rx * f * dt
        vy += ry * f * dt
        vz += (rz * f - G) * dt
        x += vx * dt
        y += vy * dt
        z += vz * dt
        t += dt
        zmax = max(zmax, z)
        if z <= 0:
            break
    return dict(z_max_mm=zmax * 1e3, range_mm=math.hypot(x, y) * 1e3, drift_y_mm=y * 1e3, t_s=t)


def spec(cad_dir):
    s = importlib.util.spec_from_file_location("make_case_plume", HERE / "make_case_plume.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    MP, P = m.MC.load_params(pathlib.Path(cad_dir))
    MS = m.load_spec(cad_dir)
    return m.viewport_boxes(MS, P, 4.0, 4.0)


def sample_launch(n, rng, slow=False):
    mech = rng.choice(len(MECH), n, p=[m[1] for m in MECH])
    lo = np.array([MECH[i][2][0] for i in mech])
    hi = np.array([MECH[i][2][1] for i in mech])
    spd = rng.uniform(lo, hi) * (0.5 if slow else 1.0)
    th = np.radians(rng.uniform(0, 70, n))
    az = rng.uniform(0, 2 * np.pi, n)
    vel = np.column_stack([spd * np.sin(th) * np.cos(az), spd * np.sin(th) * np.sin(az), spd * np.cos(th)])
    r = 25.0 * np.sqrt(rng.random(n))
    t2 = rng.uniform(0, 2 * np.pi, n)
    pos = np.column_stack([r * np.cos(t2), r * np.sin(t2), np.full(n, 0.3)]) * 1e-3
    return pos, vel, mech


def monte_carlo(d, rho_p, vp, n=4000, cross=True, slow=False, seed=7, dt=5e-5):
    """Launches from the Ø50 area into a box chamber (x +/-140, y +/-95, z 0-120 mm) with the viewport recesses as apertures."""
    rng = np.random.default_rng(seed)
    pos, vel, mech = sample_launch(n, rng, slow)
    alive = np.ones(n, bool)
    fate = np.array(["airborne"] * n, dtype=object)
    zmax = pos[:, 2].copy()
    lw, lp, lc = vp["LW"]["box"], vp["LP"]["box"], vp["LC"]["box"]
    slide = (-20.0, 20.0, -20.0, 20.0)
    t = 0.0
    while alive.any() and t < 3.0:
        a = alive
        acc = drag_acc(u_gas(pos[a, 2] * 1e3, cross) - vel[a], d, rho_p)
        acc[:, 2] -= G
        vel[a] += acc * dt
        pos[a] += vel[a] * dt
        zmax[a] = np.maximum(zmax[a], pos[a, 2])
        t += dt
        pm = pos * 1e3
        ia = np.where(a)[0]
        x, y, z = pm[ia, 0], pm[ia, 1], pm[ia, 2]
        hit_floor = z <= 0
        hit_x = (x <= -140) | (x >= 140)
        hit_y = (y <= -95) | (y >= 95)
        hit_top = z >= 120
        done = hit_floor | hit_x | hit_y | hit_top
        for i, xi, yi, zi, f_, hx, hy, ht in zip(ia[done], x[done], y[done], z[done], hit_floor[done], hit_x[done], hit_y[done], hit_top[done]):
            if f_:
                fate[i] = "plate" if math.hypot(xi, yi) < 37.5 else "floor"
            elif hx and xi < 0 and lw[2] < yi < lw[3] and lw[4] < zi < lw[5]:
                fate[i] = "LW slide"
            elif ht and lp[0] < xi < lp[1] and lp[2] < yi < lp[3]:
                fate[i] = "LP slide"
            elif ht and lc[0] < xi < lc[1] and lc[2] < yi < lc[3]:
                fate[i] = "LC bore"
            elif ht and slide[0] < xi < slide[1] and slide[2] < yi < slide[3]:
                fate[i] = "laser slide"
            elif ht:
                fate[i] = "lid"
            else:
                fate[i] = "wall"
            alive[i] = False
    keys = ("plate", "floor", "wall", "lid", "LW slide", "LP slide", "LC bore", "laser slide", "airborne")
    return {k: float((fate == k).mean()) for k in keys} | dict(n=n, median_rise_mm=float(np.median(zmax) * 1e3),
                                                               p95_rise_mm=float(np.percentile(zmax, 95) * 1e3))


# ------------------------------------------------------------------ cooling and glow
def k_ar(T):
    return 0.0177 * (T / 300.0) ** 0.72


def mu_ar(T):
    return 2.27e-5 * (T / 300.0) ** 0.70


def cool(d, T0, v0, mat="Al", eps=None, T_end=500.0, dt=2e-6, tmax=2.0):
    """Lumped cooling of a spatter droplet flying through argon at 300 K, slowing by drag (still gas). Returns arrays."""
    m = MATERIALS[mat]
    eps = m["eps"] if eps is None else eps
    rho_p, cp, L = m["rho"], m["cp"], m["L"]
    mass = rho_p * math.pi / 6 * d ** 3
    A = math.pi * d * d
    T, v, t, frac_solid, x = T0, v0, 0.0, 0.0, 0.0
    ts, Ts, xs = [0.0], [T0], [0.0]
    while T > T_end and t < tmax:
        Tf = 0.5 * (T + 300.0)
        re = RHO_G * (300.0 / Tf) * v * d / mu_ar(Tf)
        nu = 2 + 0.6 * math.sqrt(re) * 0.67 ** (1 / 3)
        h = nu * k_ar(Tf) / d
        q = h * A * (T - 300.0) + eps * SIGMA * A * (T ** 4 - 300.0 ** 4)
        if m["T_sol"] <= T <= m["T_liq"] and frac_solid < 1.0:
            # freezing range: release latent heat first, then sensible over the range
            frac_solid = min(1.0, frac_solid + q * dt / (mass * L))
            if frac_solid >= 1.0:
                T = m["T_sol"] - 1e-3
        else:
            T -= q * dt / (mass * cp)
        rep = RHO_G * v * d / MU_G
        v = max(0.0, v - v * (1 + 0.15 * rep ** 0.687) / (rho_p * d * d / (18 * MU_G)) * dt)
        x += v * dt
        t += dt
        if len(ts) < 20000 and (int(t / dt) % 25 == 0):
            ts.append(t)
            Ts.append(T)
            xs.append(x)
    return np.array(ts), np.array(Ts), np.array(xs)


def planck(lam, T):
    return 2 * H * C * C / lam ** 5 / np.expm1(H * C / (lam * KB * T))


def electrons_per_px(cam, d, T, eps, v, t_exp, n_lam=40):
    lam = np.linspace(cam["band"][0], cam["band"][1], n_lam) * 1e-6
    L = np.trapezoid(planck(lam, T) * lam / (H * C), lam)                 # photons /s /m2 /sr
    omega = math.pi * (cam["D"] / 2) ** 2 / cam["R"] ** 2
    n_ph = eps * L * (math.pi * d * d / 4) * omega * t_exp
    d_px = max(1.0, d * 1e6 / cam["px"])
    blur_px = v * t_exp * 1e6 / cam["px"]
    return n_ph * cam["qe"] / (d_px * (d_px + blur_px))


def t_visible(cam, d, eps, v, t_exp):
    lo, hi = 400.0, 3500.0
    if electrons_per_px(cam, d, hi, eps, v, t_exp) < THRESH_E:
        return None
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if electrons_per_px(cam, d, mid, eps, v, t_exp) >= THRESH_E:
            hi = mid
        else:
            lo = mid
    return hi


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    res = dict(notes=["launch speeds: Ly et al. 2017 (316L, Ti-6Al-4V) used for Al too; directions uniform 0-70 deg from vertical"])
    sizes_um = (20, 35, 50, 63, 100, 150, 200)
    # 1. single trajectories
    traj = {}
    for mat in ("Al", "steel"):
        rho = 2670.0 if mat == "Al" else 7900.0
        for d in sizes_um:
            for v0 in (2.0, 5.0, 10.0, 20.0):
                for el in (45.0, 80.0):
                    traj[f"{mat}, {d} um, {v0:g} m/s, {el:g} deg"] = dict(
                        still=fly_single(d * 1e-6, v0, el, rho, cross=False), cross=fly_single(d * 1e-6, v0, el, rho, cross=True))
    res["trajectories"] = traj
    res["relaxation"] = {f"{mat}, {d} um": dict(tau_stokes_ms=(2670.0 if mat == 'Al' else 7900.0) * (d * 1e-6) ** 2 / (18 * MU_G) * 1e3)
                         for mat in ("Al", "steel") for d in sizes_um}
    # 2. Monte Carlo against the chamber with the viewport apertures
    vp = spec(ROOT / "cad")
    mc = {}
    for mat in ("Al", "steel"):
        rho = 2670.0 if mat == "Al" else 7900.0
        for d in (20, 35, 50, 100, 150, 200):
            for slow in (False, True):
                key = f"{mat}, {d} um, {'slow (speeds / 2)' if slow else 'Ly 2017 speeds'}"
                mc[key] = monte_carlo(d * 1e-6, rho, vp, n=3000 if d < 100 else 2000, slow=slow)
                print(key, {k: round(v, 4) for k, v in mc[key].items() if isinstance(v, float) and v > 0})
    res["monte_carlo_box_chamber"] = mc
    # 3. cooling and glow
    glow = {}
    for mat in ("Al",):
        for d in (35, 50, 100, 200):
            for T0 in (1500.0, 2200.0):
                t, T, x = cool(d * 1e-6, T0, 5.0, mat)
                row = dict(T0=T0)
                for cam_name, cam in CAMERAS.items():
                    for t_exp in (10e-6, 100e-6) if "Layer" not in cam_name else (10e-3,):
                        Tv = t_visible(cam, d * 1e-6, MATERIALS[mat]["eps"], 5.0, t_exp)
                        if Tv is None or Tv >= T0:
                            row[f"{cam_name}, {t_exp * 1e6:g} us"] = dict(T_visible_K=Tv, glow_ms=0.0, glow_path_mm=0.0)
                            continue
                        i = np.argmax(T < Tv) if (T < Tv).any() else len(T) - 1
                        row[f"{cam_name}, {t_exp * 1e6:g} us"] = dict(T_visible_K=round(Tv), glow_ms=float(t[i] * 1e3), glow_path_mm=float(x[i] * 1e3))
                i_sol = np.argmax(T < MATERIALS[mat]["T_sol"]) if (T < MATERIALS[mat]["T_sol"]).any() else len(T) - 1
                row["solid_after_ms"] = float(t[i_sol] * 1e3)
                i5 = np.argmax(T < 600.0) if (T < 600.0).any() else len(T) - 1
                row["below_600K_after_ms"] = float(t[i5] * 1e3)
                glow[f"{mat}, {d} um, T0 {T0:.0f} K, 5 m/s"] = row
    res["glow"] = glow
    # 4. motion blur (pixels) for the side cameras
    blur = {}
    for cam_name, cam in CAMERAS.items():
        if "Layer" in cam_name:
            continue
        for v in (0.5, 1.0, 5.0, 10.0, 20.0):
            for t_exp in (10e-6, 20e-6, 50e-6, 100e-6):
                blur[f"{cam_name.split(',')[0]}, {cam['px']:g} um/px, {v:g} m/s, {t_exp * 1e6:g} us"] = v * t_exp * 1e6 / cam["px"]
    res["motion_blur_px"] = blur
    (OUT / "spatter.json").write_text(json.dumps(res, indent=1, default=float))
    figure(res)


def figure(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.2), constrained_layout=True)
    cols = {2.0: "#2a78d6", 5.0: "#1baf7a", 10.0: "#eb6834", 20.0: "#6250d6"}
    sizes = (20, 35, 50, 63, 100, 150, 200)
    for v0, c in cols.items():
        axs[0].plot(sizes, [res["trajectories"][f"Al, {d} um, {v0:g} m/s, 80 deg"]["still"]["z_max_mm"] for d in sizes],
                    color=c, lw=1.5, label=f"Al, {v0:g} m/s")
        axs[0].plot(sizes, [res["trajectories"][f"steel, {d} um, {v0:g} m/s, 80 deg"]["still"]["z_max_mm"] for d in sizes],
                    color=c, lw=1.0, ls="--")
    axs[0].axhline(120, color="#52514e", lw=0.7, ls=":")
    axs[0].text(25, 123, "lid", fontsize=7, color="#52514e")
    axs[0].set_yscale("log")
    axs[0].set_xlabel("spatter diameter (um)")
    axs[0].set_ylabel("max height in still argon (mm)")
    axs[0].set_title("Launched 80 deg up: Al (solid), steel (dashed)", fontsize=9)
    axs[0].legend(fontsize=7, frameon=False)
    for (k, row), c in zip([(k, v) for k, v in res["glow"].items() if "2200" in k], ("#2a78d6", "#1baf7a", "#eb6834", "#6250d6")):
        d = k.split(",")[1].strip()
        t, T, x = cool(float(d.split()[0]) * 1e-6, 2200.0, 5.0)
        axs[1].plot(t * 1e3, T, color=c, lw=1.5, label=f"Al {d}")
    axs[1].axhline(MATERIALS["Al"]["T_liq"], color="#52514e", lw=0.6, ls=":")
    axs[1].set_xscale("log")
    axs[1].set_xlim(0.01, 2000)
    axs[1].set_xlabel("time after ejection (ms)")
    axs[1].set_ylabel("temperature (K)")
    axs[1].set_title("Cooling in argon from 2200 K, launched at 5 m/s", fontsize=9)
    axs[1].legend(fontsize=7, frameon=False)
    mc = res["monte_carlo_box_chamber"]
    ds = (20, 35, 50, 100, 150, 200)
    for key, c, lab in (("LW slide", "#eb6834", "LW slide"), ("LP slide", "#6250d6", "LP slide"), ("laser slide", "#2a78d6", "laser slide"),
                        ("LC bore", "#1baf7a", "layer camera bore")):
        axs[2].plot(ds, [100 * mc[f"Al, {d} um, Ly 2017 speeds"][key] for d in ds], color=c, lw=1.5, label=lab)
        axs[2].plot(ds, [100 * mc[f"Al, {d} um, slow (speeds / 2)"][key] for d in ds], color=c, lw=1.0, ls="--")
    axs[2].set_xlabel("spatter diameter (um)")
    axs[2].set_ylabel("share of launches (%)")
    axs[2].set_title("Al spatter reaching each window (box chamber, 1-D cross-flow)\nsolid: Ly 2017 speeds; dashed: halved", fontsize=9)
    axs[2].legend(fontsize=7, frameon=False)
    fig.savefig(OUT / "spatter.png", dpi=110)


if __name__ == "__main__":
    main()
