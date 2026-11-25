"""Melt-pool scaling laws and P-v process maps for the desktop LPBF (issue #260; monitoring/melt-pool.md).

For each alloy, spot and (P, v): the absorptivity, Gan's keyhole number and keyhole depth, King's normalised enthalpy, the
Eagar-Tsai conduction pool (length, width, depth, peak temperature), the Peclet number, the Marangoni velocity scale, and a
regime (lack of fusion / conduction / transition / keyhole / unstable keyhole, plus a balling flag).

  Absorptivity   A = max(0.15, 0.7 [1 - exp(-0.6 Ke_m L_d*)]),  Ke_m L_d* = eta_m P / ((T_l - T0) pi rho c_p v r0^2)
                 Gan et al. 2021 (https://doi.org/10.1038/s41467-021-22704-0) Eq. 6-7 with eta_m = 0.047, the flat-melt value for Al
                 at 1.07 um (King et al. 2015, https://doi.org/10.1063/1.4937809, via Edison r8-melt-plume); floor 0.15, the
                 conduction-mode value Patel & Vlasea use for Al (via Edison). r0 = the 1/e^2 radius.
  Keyhole number Ke = A P / ((T_l - T0) pi rho c_p sqrt(alpha v r0^3)) (Gan Eq. 1); keyhole depth e = 0.4 (Ke - 1.4) r0 (Eq. 2);
                 conduction Ke < 1.4, transition 1.4-6, keyhole > 6; small fluctuation and almost no porosity below ~16, chaotic
                 above ~30 (Gan, Results).
  Normalised enthalpy  dH/h_s = A P / (h_s sqrt(pi alpha v sigma^3)), h_s = rho c T_m, sigma = r0/2 (Gaussian std) (King et al.
                 2014, https://doi.org/10.1016/j.jmatprotec.2014.06.005, Eq. 2.6); keyhole threshold pi T_b / T_m in theory
                 (Eq. 2.7), 30 +/- 4 measured on 316L.
  Pool           Eagar-Tsai (moving_source.py) with properties averaged from T0 to the liquidus and the latent heat folded into
                 c_eff = (H(T_l) - H(T0)) / (T_l - T0) ("sensible averaging").
  Lack of fusion (h/W)^2 + (t/D)^2 > 1 (Tang, Pistorius & Beuth 2017, https://doi.org/10.1016/j.addma.2016.12.001), hatch h
                 0.10 mm, layer t 30 um, D the larger of the conduction depth and Gan's keyhole depth.
  Balling        pool L/W > pi (Plateau-Rayleigh; Yadroitsev et al. 2010, https://doi.org/10.1016/j.jmatprotec.2010.05.010).
  Marangoni      u_M ~ (|dsigma/dT| dT)^(2/3) / (rho mu L)^(1/3), L = half-width, dT = min(T_peak, T_b) - T_l (Mukherjee, Zhang &
                 DebRoy 2017, https://doi.org/10.1063/1.4976006).

Run:  python analytic.py        (~2 min)  -> analysis/out/monitoring/melt/{analytic.json, process_map.png, process_map_alloys.png}
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
import moving_source as MS  # noqa: E402

OUT = HERE.parents[1] / "out" / "monitoring" / "melt"
ETA_M = 0.047
A_FLOOR = 0.15
HATCH, LAYER = 0.10e-3, 30e-6
SPOTS = {"48 um (IPG 5 mm)": 48e-6, "57 um (f 30)": 57e-6, "75 um (custom f 23)": 75e-6, "96 um (IPG 2.5 mm, drawn)": 96e-6}
V_GALVO = 1.1
REGIMES = ["lack of fusion", "conduction", "transition", "keyhole", "unstable keyhole"]
COLORS = {"lack of fusion": "#f2a600", "conduction": "#257de0", "transition": "#00b894", "keyhole": "#f47230",
          "unstable keyhole": "#6a4ce2"}


def point(alloy, P, v, d, T0=298.15, A=None, pool=True):
    al = alloy if isinstance(alloy, PR.Alloy) else PR.Alloy(alloy)
    r0 = d / 2
    mp = al.mean_props(T0)
    rho, cp, a, k = al.rho, mp["cp"], mp["alpha"], mp["k"]
    dTl = al.T_liq - T0
    keL = ETA_M * P / (dTl * math.pi * rho * cp * v * r0 * r0)
    A_gan = 0.7 * (1 - math.exp(-0.6 * keL))
    A_used = max(A_FLOOR, A_gan) if A is None else A
    Ke = A_used * P / (dTl * math.pi * rho * cp * math.sqrt(a * v * r0 ** 3))
    e_kh = max(0.0, 0.4 * (Ke - 1.4) * r0)
    sig = r0 / 2
    hs = rho * cp * al.T_liq
    dHhs = A_used * P / (hs * math.sqrt(math.pi * a * v * sig ** 3))
    Tb = al.T_boil()
    out = dict(alloy=al.name, P=P, v=v, d=d, T0=T0, A=A_used, A_gan=A_gan, Ke=Ke, e_keyhole=e_kh, dH_hs=dHhs,
               dH_hs_theory=math.pi * Tb / al.T_liq, Pe=v * r0 / a, Ld=math.sqrt(a / (r0 * v)), T_boil=Tb,
               E_line=P / v, alpha=a, k=k, cp=cp)
    if pool:
        c_eff = mp["dH_melt"] / dTl
        et = MS.pool_dims_et(A_used * P, v, rho * c_eff, k / (rho * c_eff), T0, r0, al.T_liq)
        et_peak = MS.pool_dims_et(A_used * P, v, rho * cp, a, T0, r0, 1e9)       # peak T without latent heat
        out.update(L=et["L"], W=et["W"], D=et["D"], T_peak=et_peak["T_peak"])
        D = max(et["D"], e_kh)
        out["D_eff"] = D
        out["LoF"] = bool(et["W"] == 0 or (HATCH / max(et["W"], 1e-9)) ** 2 + (LAYER / max(D, 1e-9)) ** 2 > 1)
        out["balling"] = bool(et["W"] > 0 and et["L"] / et["W"] > math.pi)
        Ts = min(out["T_peak"], Tb)
        dT = max(0.0, Ts - al.T_liq)
        Lh = max(et["W"] / 2, 1e-6)
        mu = float(al.mu(0.5 * (Ts + al.T_liq)))
        out["u_marangoni"] = (abs(al.dsigma_dT) * dT) ** (2 / 3) / (al.rho_l * mu * Lh) ** (1 / 3)
        a_l = float(al.k_liquid(0.5 * (Ts + al.T_liq), 1.0)) / (al.rho_l * al.cp_l)
        out["Pe_flow"] = out["u_marangoni"] * Lh / a_l
        out["Ma"] = abs(al.dsigma_dT) * dT * Lh / (mu * a_l)
        out["regime"] = regime(out)
    return out


def regime(p):
    if p.get("LoF"):
        return "lack of fusion"
    Ke = p["Ke"]
    if Ke < 1.4:
        return "conduction"
    if Ke < 6:
        return "transition"
    if Ke < 16:
        return "keyhole"
    return "unstable keyhole"


def grid(alloy, d, T0=298.15, Ps=None, vs=None):
    Ps = np.arange(100, 501, 50.0) if Ps is None else Ps
    vs = np.round(np.arange(0.2, 2.01, 0.15), 2) if vs is None else vs
    al = PR.Alloy(alloy)
    rows = [[point(al, float(P), float(v), d, T0) for v in vs] for P in Ps]
    return Ps, vs, rows


def plot_maps(maps, fname, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    from matplotlib.patches import Patch
    n = len(maps)
    fig, axs = plt.subplots(1, n, figsize=(3.6 * n, 3.9), sharey=True)
    cmap = ListedColormap([COLORS[r] for r in REGIMES])
    for ax, (lab, (Ps, vs, rows)) in zip(np.atleast_1d(axs), maps.items()):
        Z = np.array([[REGIMES.index(p["regime"]) for p in row] for row in rows])
        V, Pm = np.meshgrid(vs, Ps)
        ax.pcolormesh(V, Pm, Z, cmap=cmap, vmin=-0.5, vmax=len(REGIMES) - 0.5, shading="nearest", alpha=0.85)
        Ke = np.array([[p["Ke"] for p in row] for row in rows])
        cs = ax.contour(V, Pm, Ke, levels=[1.4, 6, 16, 30], colors="#191919", linewidths=0.8)
        ax.clabel(cs, fmt=lambda x: f"Ke {x:g}", fontsize=7)
        ball = np.array([[p["balling"] for p in row] for row in rows])
        if ball.any():
            ax.contourf(V, Pm, ball.astype(float), levels=[0.5, 1.5], colors="none", hatches=["////"])
        dH = np.array([[p["dH_hs"] for p in row] for row in rows])
        cs2 = ax.contour(V, Pm, dH, levels=[30.0], colors="#191919", linewidths=1.2, linestyles="--")
        ax.clabel(cs2, fmt=lambda x: "dH/h_s 30", fontsize=7)
        if "96" in lab or lab == "AlSi10Mg":
            for P, v, D, W in PATEL:
                ax.plot(v, P, marker="o", ms=5, mfc="white", mec="#191919", mew=1.0)
            ax.annotate("AlSi10Mg tracks, 108 um spot\n(Patel & Vlasea): D/W 0.32-0.36", xy=(0.917, 350), xytext=(1.2, 455),
                        fontsize=7, arrowprops=dict(arrowstyle="-", lw=0.6, color="#191919"))
        ax.axvspan(V_GALVO, vs.max() + 0.05, color="white", alpha=0.55, lw=0)
        ax.axvline(V_GALVO, color="#191919", lw=1.0)
        ax.text(V_GALVO + 0.03, Ps.min() + 10, "beyond the galvo's\n1.1 m/s", fontsize=7, color="#191919", va="bottom")
        ax.set_title(lab, fontsize=9)
        ax.set_xlabel("scan speed (m/s)")
        ax.set_xlim(vs.min() - 0.05, vs.max() + 0.05)
        ax.grid(alpha=0.2)
    np.atleast_1d(axs)[0].set_ylabel("laser power (W)")
    handles = [Patch(color=COLORS[r], label=r) for r in REGIMES] + [Patch(facecolor="none", hatch="////", label="balling (L/W > pi)")]
    fig.legend(handles=handles, loc="lower center", ncol=6, fontsize=8, frameon=False)
    fig.suptitle(title, fontsize=10)
    fig.tight_layout(rect=(0, 0.07, 1, 0.95))
    fig.savefig(OUT / fname, dpi=120)
    plt.close(fig)


def table_points():
    rows = []
    for alloy in ("AlSi10Mg", "6061", "7075", "Al"):
        for T0c in (25.0, 200.0):
            for P in (200.0, 320.0, 400.0):
                for v in (0.6, 1.1):
                    rows.append(point(alloy, P, v, 96e-6, T0c + 273.15))
    for lab, d in SPOTS.items():
        rows.append(point("AlSi10Mg", 320.0, 1.1, d) | {"spot_label": lab})
    return rows


PATEL = [(200, 0.917, 67.2, 185.1), (250, 0.917, 66.2, 195.6), (300, 0.917, 70.0, 202.4), (350, 0.917, 77.7, 239.4),
         (200, 0.688, 72.7, 205.0), (350, 0.688, 79.5, 234.7)]     # the 0.688 m/s rows are Edison's range ends, paired as given


def validation():
    """Patel & Vlasea's AlSi10Mg single tracks (108 um spot, 30 um layer), via Edison r8-melt-plume: depth / width (um)."""
    out = []
    for P, v, D, W in PATEL:
        p = point("AlSi10Mg", float(P), v, 108e-6)
        out.append(dict(P=P, v=v, D_meas_um=D, W_meas_um=W, DW_meas=D / W, A=p["A"], Ke=p["Ke"], dH_hs=p["dH_hs"],
                        W_ET_um=p["W"] * 1e6, D_ET_um=p["D"] * 1e6, e_keyhole_um=p["e_keyhole"] * 1e6, regime=p["regime"]))
    return out


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    maps = {lab: grid("AlSi10Mg", d) for lab, d in SPOTS.items()}
    plot_maps(maps, "process_map.png", "AlSi10Mg, 25 C plate, 30 um layer, 0.10 mm hatch: regimes from Gan's keyhole number and "
                                      "Tang's lack-of-fusion overlap (Eagar-Tsai pool)")
    maps_al = {a: grid(a, 96e-6) for a in ("AlSi10Mg", "6061", "7075", "Al")}
    plot_maps(maps_al, "process_map_alloys.png", "96 um spot, 25 C plate: the same map for each alloy")
    maps_hot = {a: grid(a, 96e-6, T0=473.15) for a in ("AlSi10Mg", "6061")}
    plot_maps(maps_hot, "process_map_200C.png", "96 um spot, 200 C plate")
    # where the regimes sit at the galvo's speed: power bands at 1.1 m/s, 96 um
    bands = {}
    for a in ("AlSi10Mg", "6061", "7075", "Al"):
        for T0 in (298.15, 473.15):
            Ps = np.arange(50, 501, 5.0)
            pts = [point(a, float(P), 1.1, 96e-6, T0, pool=False) for P in Ps]
            Ke = np.array([p["Ke"] for p in pts])
            bands[f"{a}_{T0 - 273.15:.0f}C"] = {f"P_at_Ke_{x:g}": (float(np.interp(x, Ke, Ps)) if Ke.min() <= x <= Ke.max() else None)
                                              for x in (1.4, 6.0, 16.0, 30.0)}
    res = dict(eta_m=ETA_M, A_floor=A_FLOOR, hatch_m=HATCH, layer_m=LAYER, table=table_points(), validation=validation(),
               power_bands_1p1ms_96um=bands,
               maps={lab: dict(P=list(map(float, m[0])), v=list(map(float, m[1])),
                               regime=[[p["regime"] for p in row] for row in m[2]],
                               Ke=[[round(p["Ke"], 2) for p in row] for row in m[2]]) for lab, m in maps.items()})
    (OUT / "analytic.json").write_text(json.dumps(res, indent=1, default=float))
    for r in res["validation"]:
        print(r)
    for k, b in bands.items():
        print(k, b)
    for r in res["table"]:
        print(f"{r['alloy']:8s} T0 {r['T0'] - 273.15:3.0f} P {r['P']:4.0f} v {r['v']:.1f} d {r['d'] * 1e6:3.0f}: A {r['A']:.2f} Ke {r['Ke']:5.1f} "
              f"e {r['e_keyhole'] * 1e6:5.0f} dH/hs {r['dH_hs']:5.1f} (th {r['dH_hs_theory']:4.1f}) L/W/D {r['L'] * 1e6:5.0f}/{r['W'] * 1e6:4.0f}/"
              f"{r['D'] * 1e6:4.0f} Tpk {r['T_peak']:6.0f} Tb {r['T_boil']:5.0f} Pe {r['Pe']:.2f} uM {r['u_marangoni']:.1f} "
              f"Pe_fl {r['Pe_flow']:.0f} {r['regime']}{' balling' if r['balling'] else ''}")


if __name__ == "__main__":
    main()
