"""Time-dependent melt-pool pieces that matter for monitoring (issue #260; monitoring/melt-pool.md section 4).

(a) Track ends and hatch turnarounds. The beam path is the command low-passed by the galvo: a first-order lag with the
    basiCube 20's 0.25 ms tracking error as its time constant (SCANLAB data sheet; a simplification of the real servo). The
    temperature is a superposition of instantaneous Gaussian surface sources along the actual path (constant properties, the
    Eagar-Tsai kernel; latent heat folded into the heat capacity). What a coaxial photodiode sees is the in-band radiance
    (520-985 nm, silicon responsivity ~ wavelength) integrated over a 1 mm field centred on the actual beam, with the surface
    capped at the depression-wall temperature (the conduction field runs past boiling) and emissivity 0.15. Reported as the
    ratio to the steady mid-track signal.
(b) Layer-to-layer heat build-up: 1D conduction along a part growing 30 um per layer on a 200 C plate, the layer's absorbed
    energy put into its top during the scan, then 8 s of recoat (heat.md's cycle). The part's top temperature when the next
    layer starts is the melt pool's baseline.
(c) Time scales from the 3D solutions (fv_cases.jsonl): transit, time liquid, solidification time, cooling rate, plus
    capillary and Marangoni estimates -> the frame rates and bandwidths monitoring needs.

Run:  python transient.py     -> analysis/out/monitoring/melt/{transient.json, track_ends.png, buildup.png}
"""
from __future__ import annotations

import json
import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import props as PR  # noqa: E402

OUT = HERE.parents[1] / "out" / "monitoring" / "melt"
TAU_GALVO = 0.25e-3
H_PL, C_LIGHT, K_B = 6.62607015e-34, 2.99792458e8, 1.380649e-23


def band_radiance_table(lo=520e-9, hi=985e-9):
    """In-band radiance x silicon responsivity (arbitrary units), tabulated against T."""
    lam = np.linspace(lo, hi, 300)
    Tg = np.linspace(300.0, 4000.0, 1500)
    B = 2 * H_PL * C_LIGHT ** 2 / lam[None, :] ** 5 / np.expm1(H_PL * C_LIGHT / (lam[None, :] * K_B * Tg[:, None]))
    S = np.trapezoid(B * (lam / 1e-6)[None, :], lam, axis=1)
    return Tg, S


TG, SG = band_radiance_table()


def band(T):
    return np.interp(T, TG, SG)


class Path:
    """Commanded segments -> actual beam path through a first-order lag; laser power schedule."""

    def __init__(self, dt=2e-6):
        self.dt = dt

    @staticmethod
    def lag(cmd, dt, tau=TAU_GALVO):
        a = dt / (tau + dt)
        out = np.empty_like(cmd)
        out[0] = cmd[0]
        for i in range(1, len(cmd)):
            out[i] = out[i - 1] + a * (cmd[i] - out[i - 1])
        return out


def scenario(kind, v, P, hatch=0.1e-3, t_before=4e-3, t_after=1.5e-3, dt=2e-6, t_off=TAU_GALVO, t_jump=0.3e-3,
             t_on=0.1e-3):
    """Return times, actual beam (x, y), power. Track 1 runs +x and its command ends at x = 0 at t = 0."""
    t = np.arange(-t_before, t_after, dt)
    xc = np.where(t < 0, v * t, 0.0)
    yc = np.zeros_like(t)
    if kind == "skywriting":
        # the mirrors keep moving at v through the end (the command is extended); laser off exactly when the beam is at x = 0
        x = v * t
        y = yc
        Pw = np.where(t < 0, P, 0.0)
        return t, x, y, Pw
    if kind.startswith("end"):
        # no skywriting: the command stops at x = 0; the beam lags (tau) and decelerates; laser off t_off after the command ends
        # start the lag in steady state: the actual beam trails the command by v tau
        x = xc - v * TAU_GALVO
        for i in range(1, len(t)):
            if t[i] >= 0:
                x[i] = x[i - 1] + dt / (TAU_GALVO + dt) * (xc[i] - x[i - 1])
        Pw = np.where(t < t_off, P, 0.0)
        return t, x, yc, Pw
    if kind.startswith("turn"):
        # meander without skywriting: end of track 1 at x = 0; jump to (0, hatch); track 2 commanded from t_jump toward -x
        x = xc - v * TAU_GALVO
        y = np.zeros_like(t)
        ycmd = np.where(t >= 0, hatch, 0.0)
        xcmd = np.where(t < t_jump, xc, -v * (t - t_jump))
        for i in range(1, len(t)):
            if t[i] >= 0:
                a = dt / (TAU_GALVO + dt)
                x[i] = x[i - 1] + a * (xcmd[i] - x[i - 1])
                y[i] = y[i - 1] + a * (ycmd[i] - y[i - 1])
        Pw = np.where((t < t_off) | (t >= t_jump + t_on), P, 0.0)
        return t, x, y, Pw
    if kind == "turn_sky":
        raise ValueError
    raise ValueError(kind)


def field_at(tn, t, x, y, Pw, A, rho_c, a, w, gx, gy, T0):
    """Surface temperature on points (gx, gy) at time tn from all source steps before tn (analytic z-integral per step)."""
    m = (t < tn) & (Pw > 0)
    if not m.any():
        return np.full(gx.shape, T0)
    tk, xk, yk, Pk = t[m], x[m], y[m], Pw[m]
    dt = t[1] - t[0]
    tau2 = tn - tk
    tau1 = np.maximum(tau2 - dt, 0.0)
    taum = 0.5 * (tau1 + tau2)
    s2 = (w / 2) ** 2
    den = 2 * (s2 + 2 * a * taum)                    # 2 sigma^2 + 4 a tau
    zint = 2 * (np.sqrt(tau2) - np.sqrt(tau1)) / math.sqrt(4 * math.pi * a)     # Int tau^-1/2 dtau / sqrt(4 pi a)
    wgt = 2.0 * A * Pk / rho_c * zint / (math.pi * den)        # per step: energy A P dt, the dt is inside zint
    out = np.zeros(gx.size)
    gxf, gyf = gx.ravel(), gy.ravel()
    for i0 in range(0, gxf.size, 400):
        dx = gxf[i0:i0 + 400, None] - xk[None, :]
        dy = gyf[i0:i0 + 400, None] - yk[None, :]
        out[i0:i0 + 400] = (wgt[None, :] * np.exp(-(dx * dx + dy * dy) / den[None, :])).sum(axis=1)
    return T0 + out.reshape(gx.shape)


def track_end_study(alloy="AlSi10Mg", P=320.0, v=1.1, A=0.35, T0=298.15, d=96e-6):
    al = PR.Alloy(alloy)
    mp = al.mean_props(T0)
    c_eff = mp["dH_melt"] / (al.T_liq - T0)
    rho_c = al.rho * c_eff
    a = mp["k"] / rho_c
    w = d / 2
    import evap as EV
    T_cap = EV.T_wall(al, w)
    fov = 0.5e-3
    n = 41
    gxl = np.linspace(-fov, fov, n)
    GX, GY = np.meshgrid(gxl, gxl, indexing="ij")
    inside = GX ** 2 + GY ** 2 <= fov ** 2
    dA = (gxl[1] - gxl[0]) ** 2
    res = {}
    kinds = {"skywriting (laser off at the end, mirrors keep moving)": dict(kind="skywriting"),
             "no skywriting, laser-off delay 0.25 ms": dict(kind="end", t_off=0.25e-3),
             "no skywriting, laser-off delay 0.5 ms": dict(kind="end", t_off=0.5e-3),
             "meander turnaround, no skywriting (off 0.25 ms, next vector at 0.3 ms, laser-on delay 0.1 ms)":
                 dict(kind="turn", t_off=0.25e-3, t_jump=0.3e-3, t_on=0.1e-3)}
    for lab, kw in kinds.items():
        t, x, y, Pw = scenario(kw.pop("kind"), v, P, **kw)
        times = np.arange(-0.6e-3, 1.2e-3, 10e-6)
        sig, Tpk, area_liq, speed = [], [], [], []
        for tn in times:
            i = min(np.searchsorted(t, tn), len(t) - 1)
            bx, by = x[i], y[i]
            T = field_at(tn, t, x, y, Pw, A, rho_c, a, w, GX + bx, GY + by, T0)
            Tc = np.minimum(T, T_cap)
            eps = np.where(T >= al.T_liq, 0.15, 0.10)
            sig.append(float((eps * band(Tc) * inside).sum() * dA))
            Tpk.append(float(T[inside].max()))
            area_liq.append(float(((T >= al.T_liq) & inside).sum() * dA))
            j = max(i - 1, 0)
            speed.append(float(math.hypot(x[i] - x[j], y[i] - y[j]) / max(t[i] - t[j], 1e-12)))
        # steady reference: the signal 0.5 ms before the end
        i_ref = int(np.argmin(np.abs(times + 0.5e-3)))
        S = np.array(sig)
        res[lab] = dict(t_us=(times * 1e6).tolist(), signal_rel=(S / S[i_ref]).tolist(), T_peak_K=Tpk,
                        liquid_area_rel=(np.array(area_liq) / max(area_liq[i_ref], 1e-30)).tolist(), speed_m_s=speed,
                        peak_signal_rel=float((S / S[i_ref]).max()), peak_liquid_area_rel=float(max(area_liq) / max(area_liq[i_ref], 1e-30)))
    return dict(alloy=alloy, P=P, v=v, A=A, T0=T0, d=d, T_cap_K=T_cap, fov_m=2 * fov, cases=res,
                props=dict(rho_c_eff=rho_c, alpha_eff=a))


# ------------------------------------------------------------------------------------------------- (b) layer heat build-up
def buildup(alloy="AlSi10Mg", P=320.0, v=1.1, A=0.35, hatch=0.10e-3, layer=30e-6, T_plate=473.15, t_recoat=8.0,
            t_jump=0.2, area_mm2=100.0, n_layers=500, k_part=None):
    """1D column: the part (bulk Al alloy) grows by one 30 um layer per cycle; heat in at the top during the scan; plate at
    T_plate below; no lateral loss (the powder around it conducts ~1000x less). Returns the top temperature at each layer start."""
    al = PR.Alloy(alloy)
    k = k_part or float(al.k_solid(T_plate + 50.0))
    rho_c = al.rho * float(al.cp_solid(T_plate + 50.0))
    a = k / rho_c
    t_scan = area_mm2 * 1e-6 / (v * hatch) + t_jump
    q_top = A * P * (t_scan - t_jump) / t_scan / (area_mm2 * 1e-6)     # W/m2 over the scan time
    dz = layer
    T = np.array([T_plate])
    starts, ends = [], []
    for n in range(n_layers):
        T = np.append(T, T[-1])           # new layer
        N = len(T)
        # implicit steps: scan (heat on), then recoat (heat off)
        for dur, q in ((t_scan, q_top), (t_recoat, 0.0)):
            nsteps = 20 if q > 0 else 40
            ht = dur / nsteps
            r = a * ht / dz ** 2
            main = np.full(N, 1 + 2 * r)
            lower = np.full(N - 1, -r)
            upper = np.full(N - 1, -r)
            main[-1] = 1 + r                   # top: flux
            main[0] = 1.0                      # bottom node held at the plate
            upper[0] = 0.0
            from scipy.linalg import solve_banded
            ab = np.zeros((3, N))
            ab[0, 1:] = upper
            ab[1] = main
            ab[2, :-1] = lower
            for _ in range(nsteps):
                rhs = T.copy()
                rhs[0] = T_plate
                rhs[-1] += q * ht / (rho_c * dz)
                T = solve_banded((1, 1), ab, rhs)
            if q > 0:
                ends.append(float(T[-1]))
        starts.append(float(T[-1]))
    return dict(alloy=alloy, area_mm2=area_mm2, t_scan_s=t_scan, q_top_W_m2=q_top, E_layer_J=A * P * (t_scan - t_jump),
                T_top_at_layer_start_K=starts, T_top_after_scan_K=ends, k=k, alpha=a)


# ------------------------------------------------------------------------------------------------- (c) time scales
def timescales():
    log = OUT / "fv_cases.jsonl"
    rows = {}
    for l in log.read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            rows[r["case"]["tag"]] = r
    out = {}
    for tag, r in rows.items():
        if not tag.startswith(("ref_", "map_")):
            continue
        c = r["case"]
        al = PR.Alloy(c["alloy"])
        L, W, D = r["liquid"]["L"], r["liquid"]["W"], r["liquid"]["D"]
        s = r.get("solid", {})
        v = c["v"]
        sig = float(al.sigma(2000.0))
        kc = math.pi / max(W, 1e-9)
        f_cap_pool = math.sqrt(sig * kc ** 3 / al.rho_l) / (2 * math.pi)      # lowest capillary mode across the pool
        r_d = c["d_spot"] / 2
        f_cap_dep = math.sqrt(sig * (math.pi / (2 * r_d)) ** 3 / al.rho_l) / (2 * math.pi)
        out[tag] = dict(alloy=c["alloy"], P=c["P"], v=v, T0_C=c["T0"] - 273.15,
                        spot_transit_us=c["d_spot"] / v * 1e6, pool_transit_us=L / v * 1e6,
                        time_liquid_centre_us=s.get("centre", {}).get("t_liquid", float("nan")) * 1e6,
                        t_sol_centre_us=s.get("centre", {}).get("t_sol", float("nan")) * 1e6,
                        t_sol_range_us=[x * 1e6 for x in s.get("t_sol_range", [])],
                        Tdot_liq_range_K_s=s.get("Tdot_range"), G_range_K_m=s.get("G_range"), R_range_m_s=s.get("R_range"),
                        f_capillary_pool_kHz=f_cap_pool / 1e3, f_capillary_depression_kHz=f_cap_dep / 1e3,
                        L_um=L * 1e6, W_um=W * 1e6, D_um=D * 1e6, T_peak_K=r["T_peak"])
    return out


def plots(te, bu):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cols = ["#257de0", "#f47230", "#00b894", "#6a4ce2"]
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.6))
    for (lab, d), ccol in zip(te["cases"].items(), cols):
        axs[0].plot(d["t_us"], d["signal_rel"], color=ccol, lw=1.6, label=lab)
        axs[1].plot(d["t_us"], d["liquid_area_rel"], color=ccol, lw=1.6)
    for ax, yl in zip(axs, ("photodiode signal / mid-track signal", "liquid area in the 1 mm field / mid-track")):
        ax.axvline(0, color="#666666", lw=0.8)
        ax.set_xlabel("time from the end of the commanded vector (us)")
        ax.set_ylabel(yl)
        ax.grid(alpha=0.25)
    fig.legend(*axs[0].get_legend_handles_labels(), loc="lower center", ncol=2, fontsize=7, frameon=False)
    fig.suptitle(f"Track end at {te['v']} m/s, {te['P']:.0f} W, {te['d'] * 1e6:.0f} um, {te['alloy']} (galvo lag 0.25 ms, "
                 "first-order; constant-property superposition)", fontsize=9)
    fig.tight_layout(rect=(0, 0.13, 1, 1))
    fig.savefig(OUT / "track_ends.png", dpi=120)
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for (lab, d), ccol in zip(bu.items(), cols):
        n = np.arange(1, len(d["T_top_at_layer_start_K"]) + 1)
        ax.plot(n * 0.03, np.array(d["T_top_at_layer_start_K"]) - 273.15, color=ccol, lw=1.6, label=lab)
    ax.set_xlabel("part height (mm)")
    ax.set_ylabel("part top at the next layer's start (C)")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=7, frameon=False)
    ax.set_title("Heat build-up in the part between layers, 200 C plate held (plate drift: heat.md)", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "buildup.png", dpi=120)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    te = track_end_study()
    te06 = track_end_study(v=0.6)
    bu = {"10 x 10 mm block, 8 s recoat": buildup(),
          "10 x 10 mm block, 2 s recoat": buildup(t_recoat=2.0),
          "20 x 20 mm block, 8 s recoat": buildup(area_mm2=400.0),
          "10 x 10 mm block, 8 s recoat, 0.6 m/s": buildup(v=0.6)}
    ts = timescales()
    res = dict(track_end_1p1=te, track_end_0p6=te06, buildup={k: dict(v, T_top_at_layer_start_K=v["T_top_at_layer_start_K"][::10],
                                                                    T_top_after_scan_K=v["T_top_after_scan_K"][::10])
                                                            for k, v in bu.items()},
               buildup_summary={k: dict(first=v["T_top_at_layer_start_K"][0] - 273.15, last=v["T_top_at_layer_start_K"][-1] - 273.15,
                                        after_scan_last=v["T_top_after_scan_K"][-1] - 273.15, E_layer_J=v["E_layer_J"],
                                        t_scan_s=v["t_scan_s"]) for k, v in bu.items()},
               timescales=ts)
    (OUT / "transient.json").write_text(json.dumps(res, indent=1, default=float))
    plots(te, bu)
    for k, d in te["cases"].items():
        print(f"1.1 m/s {k[:60]:60s} peak signal x{d['peak_signal_rel']:.2f}  liquid area x{d['peak_liquid_area_rel']:.2f}")
    for k, d in te06["cases"].items():
        print(f"0.6 m/s {k[:60]:60s} peak signal x{d['peak_signal_rel']:.2f}  liquid area x{d['peak_liquid_area_rel']:.2f}")
    for k, v in res["buildup_summary"].items():
        print(k, {a: round(b, 2) for a, b in v.items()})


if __name__ == "__main__":
    main()
