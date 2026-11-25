"""Figures and the summary table from the 3D melt-pool runs (issue #260; monitoring/melt-pool.md).

Run:  python plots.py   -> analysis/out/monitoring/melt/{surface_fields.png, sections.png, gr_map.png, fv_summary.md}
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
RUNS = pathlib.Path("/tmp/melt_runs")
CAM_PX, CAM_FIELD = 8.0, 1000.0     # coaxial camera: 8 um/px, ~1 mm field (monitoring.md section 2.2)


def rows():
    out = {}
    for l in (OUT / "fv_cases.jsonl").read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            out[r["case"]["tag"]] = r
    return out


def surface_figure(R):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    tags = [t for t in R if t.startswith("ref_")]
    tags.sort(key=lambda t: (R[t]["case"]["alloy"], -R[t]["case"]["v"], R[t]["case"]["T0"]))
    n = len(tags)
    ncol = 4
    nrow = math.ceil(n / ncol)
    fig, axs = plt.subplots(nrow, ncol, figsize=(4.0 * ncol, 2.9 * nrow), squeeze=False)
    for ax, t in zip(axs.ravel(), tags):
        d = np.load(RUNS / f"{t}.npz")
        r = R[t]
        al = PR.Alloy(r["case"]["alloy"])
        X, Y = np.meshgrid(d["xg"], d["yg"], indexing="ij")
        Ts = d["Ts"]
        m = ax.pcolormesh(X, Y, Ts, cmap="Blues_r" if False else "magma", vmin=r["case"]["T0"], vmax=3400, shading="auto")
        cs = ax.contour(X, Y, Ts, levels=[al.T_sol, al.T_liq, r["T_boil_alloy"]], colors=["#9c9c9c", "#ffffff", "#00b894"],
                        linewidths=[0.8, 1.0, 1.2])
        # 1 mm coaxial-camera field centred on the beam
        ax.add_patch(plt.Rectangle((-CAM_FIELD / 2, -CAM_FIELD / 2), CAM_FIELD, CAM_FIELD, fill=False, ec="#257de0", lw=0.8,
                                   ls="--"))
        c = r["case"]
        L = r["liquid"]
        ax.set_title(f"{c['alloy']} {c['P']:.0f} W {c['v']} m/s, plate {c['T0'] - 273.15:.0f} C\n"
                     f"pool {L['L'] * 1e6:.0f} x {L['W'] * 1e6:.0f} x {L['D'] * 1e6:.0f} um "
                     f"({L['L'] * 1e6 / CAM_PX:.0f} x {L['W'] * 1e6 / CAM_PX:.0f} px at 8 um/px)", fontsize=8)
        ax.set_aspect("equal")
        ax.set_xlim(-900, 250)
        ax.set_ylim(-300, 300)
        ax.tick_params(labelsize=7)
    for ax in axs.ravel()[n:]:
        ax.axis("off")
    for ax in axs[-1]:
        ax.set_xlabel("x (um), beam moving +x", fontsize=8)
    for ax in axs[:, 0]:
        ax.set_ylabel("y (um)", fontsize=8)
    cb = fig.colorbar(m, ax=axs, shrink=0.6, pad=0.01)
    cb.set_label("surface temperature (K)", fontsize=8)
    fig.suptitle("Surface temperature, 96 um spot, A 0.35 (fv3d.py). Contours: solidus (grey), liquidus (white), the alloy's "
                 "1 atm boiling point (green: inside it the real surface is a vapour depression). Dashed: 1 mm camera field",
                 fontsize=9)
    fig.savefig(OUT / "surface_fields.png", dpi=110, bbox_inches="tight")
    plt.close(fig)


def sections_figure(R):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    tags = [t for t in ("ref_AlSi10Mg_320W_1.1ms_25C", "ref_AlSi10Mg_320W_0.6ms_25C", "ref_6061_320W_1.1ms_25C",
                        "ref_AlSi10Mg_320W_1.1ms_200C") if t in R]
    fig, axs = plt.subplots(len(tags), 2, figsize=(11, 2.2 * len(tags)), squeeze=False,
                            gridspec_kw=dict(width_ratios=[3, 1]))
    for (a1, a2), t in zip(axs, tags):
        d = np.load(RUNS / f"{t}.npz")
        r = R[t]
        al = PR.Alloy(r["case"]["alloy"])
        xc, yc, zc = d["xc"] * 1e6, d["yc"] * 1e6, d["zc"] * 1e6
        X, Z = np.meshgrid(xc, zc, indexing="ij")
        a1.pcolormesh(X, Z, d["T_xz"], cmap="magma", vmin=r["case"]["T0"], vmax=3400, shading="auto")
        a1.contour(X, Z, d["T_xz"], levels=[al.T_sol, al.T_liq], colors=["#9c9c9c", "#ffffff"], linewidths=[0.8, 1.0])
        a1.axhline(-r["case"]["t_layer"] * 1e6, color="#00b894", lw=0.8, ls="--")
        a1.set_xlim(-800, 200)
        a1.set_ylim(-200, 5)
        a1.set_aspect("equal")
        a1.set_title(f"{t.replace('ref_', '')}: centre plane (dashed: bottom of the 30 um powder layer)", fontsize=8)
        Y, Z2 = np.meshgrid(np.concatenate([-yc[::-1], yc]), zc, indexing="ij")
        Tyz = np.concatenate([d["T_yz"][::-1], d["T_yz"]], axis=0)
        a2.pcolormesh(Y, Z2, Tyz, cmap="magma", vmin=r["case"]["T0"], vmax=3400, shading="auto")
        a2.contour(Y, Z2, Tyz, levels=[al.T_sol, al.T_liq], colors=["#9c9c9c", "#ffffff"], linewidths=[0.8, 1.0])
        a2.set_xlim(-250, 250)
        a2.set_ylim(-200, 5)
        a2.set_aspect("equal")
        a2.set_title(f"cross-section at x = {float(d['x_yz']) * 1e6:.0f} um", fontsize=8)
        for a in (a1, a2):
            a.tick_params(labelsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "sections.png", dpi=110)
    plt.close(fig)


def gr_figure(R):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cols = {"AlSi10Mg": "#257de0", "6061": "#f47230", "7075": "#6a4ce2", "Al": "#00b894"}
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    done = set()
    for t, r in R.items():
        if not t.startswith(("ref_", "map_")) or "200C" in t or (t.startswith("map_7075") and "fvol" not in t):
            continue
        d = np.load(RUNS / f"{t}.npz")
        s = d["sol"]
        if s.size == 0:
            continue
        al = r["case"]["alloy"]
        lab = al if al not in done else None
        done.add(al)
        ax.scatter(s[:, 3], s[:, 2], s=4, color=cols.get(al, "#666666"), alpha=0.35, lw=0, label=lab)
    Rg = np.geomspace(1e-3, 3, 50)
    for Td in (1e5, 1e6, 1e7):
        ax.plot(Rg, Td / Rg, color="#9c9c9c", lw=0.8, ls="--")
        ax.text(Rg[-1] * 0.5, Td / (Rg[-1] * 0.5) * 1.1, f"{Td:.0e} K/s".replace("e+0", "e"), fontsize=7, color="#666666")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-2, 2)
    ax.set_ylim(1e5, 1e8)
    ax.set_xlabel("solidification velocity R (m/s)")
    ax.set_ylabel("thermal gradient G at the liquidus (K/m)")
    ax.grid(alpha=0.2, which="both")
    ax.legend(fontsize=8, frameon=False, markerscale=3, title="25 C plate, 200-400 W, 0.4-1.1 m/s", title_fontsize=7)
    ax.set_title("Where the melt pool solidifies: every point of the rear liquidus surface (fv3d.py)", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "gr_map.png", dpi=120)
    plt.close(fig)


H_PL, C_LIGHT, K_B = 6.62607015e-34, 2.99792458e8, 1.380649e-23


def planck(lam, T):
    return 2 * H_PL * C_LIGHT ** 2 / lam ** 5 / np.expm1(H_PL * C_LIGHT / (lam * K_B * T))


def apparent(R):
    """What a coaxial camera or photodiode sees in each reference field. The surface is capped at the depression-wall
    temperature (evap.T_wall); emissivity is taken equal everywhere (it cancels in these ratios). For a camera at 850 nm (Si) and
    1550 nm (InGaAs) with the hottest pixel at full scale: the isotherm at 1/1023 and 1/4095 of full scale (10 and 12 bit),
    and the length and width of the region above it. Photodiode: in-band (520-985 nm, responsivity ~ wavelength) signal over a
    1 mm field, relative to AlSi10Mg 320 W 1.1 m/s on a 25 C plate."""
    import evap as EV
    import transient as TR
    out = {}
    ref = None
    for t, r in sorted(R.items()):
        if not t.startswith(("ref_", "map_")):
            continue
        d = np.load(RUNS / f"{t}.npz")
        al = PR.Alloy(r["case"]["alloy"])
        Tw = EV.T_wall(al, r["case"]["d_spot"] / 2, r["case"].get("f_vol", 1.0))
        Ts = np.minimum(d["Ts"].astype(float), Tw)
        xg, yg = d["xg"], d["yg"]
        dA = (xg[1] - xg[0]) * (yg[1] - yg[0]) * 1e-12
        X, Y = np.meshgrid(xg, yg, indexing="ij")
        fov = (X ** 2 + Y ** 2) <= 500.0 ** 2
        sig = float((TR.band(Ts) * fov).sum() * dA)
        o = dict(T_wall_K=Tw, photodiode=sig)
        # two-colour coaxial channel (700 and 900 nm, grey body): the ratio temperature of the whole 1 mm field
        l1, l2 = 700e-9, 900e-9
        S1 = float((planck(l1, Ts) * fov).sum())
        S2 = float((planck(l2, Ts) * fov).sum())
        Tg = np.linspace(800.0, 4000.0, 3201)
        rg = planck(l1, Tg) / planck(l2, Tg)
        o["ratio_T_700_900_K"] = float(np.interp(S1 / S2, rg, Tg))
        for lam, nm in ((850e-9, "Si_850nm"), (1550e-9, "InGaAs_1550nm")):
            Lmax = planck(lam, Tw)
            for bits in (10, 12):
                thr = Lmax / (2 ** bits - 1)
                # temperature whose radiance is thr
                T_thr = H_PL * C_LIGHT / (lam * K_B) / np.log1p(2 * H_PL * C_LIGHT ** 2 / (lam ** 5 * thr))
                m = Ts >= T_thr
                Lx = float(xg[m.any(axis=1)].max() - xg[m.any(axis=1)].min()) if m.any() else 0.0
                Wy = float(yg[m.any(axis=0)].max() - yg[m.any(axis=0)].min()) if m.any() else 0.0
                o[f"{nm}_{bits}bit"] = dict(T_floor_K=float(T_thr), L_um=Lx, W_um=Wy, area_um2=float(m.sum() * dA * 1e12))
        out[t] = o
        if t == "ref_AlSi10Mg_320W_1.1ms_25C":
            ref = sig
    if ref:
        for o in out.values():
            o["photodiode_rel"] = o["photodiode"] / ref
    (OUT / "apparent.json").write_text(json.dumps(out, indent=1))
    return out


def summary_md(R):
    L = ["| Case | A | Pool L × W × D (µm) | D/W | Peak T, flat model (K) | Alloy boils at (K) | Liquid at the surface centre (µs) | "
         "Mushy time, centre (µs) | Cooling at the liquidus, median (K/s) | G median (K/m) | Energy: evaporated (W) | Cells, iterations |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t, r in sorted(R.items()):
        c, Lq, s = r["case"], r["liquid"], r.get("solid", {})
        cen = s.get("centre", {})
        L.append(f"| {t} | {c['A']:.2f} | {Lq['L'] * 1e6:.0f} × {Lq['W'] * 1e6:.0f} × {Lq['D'] * 1e6:.0f} | "
                 f"{Lq['D'] / max(Lq['W'], 1e-9):.2f} | {r['T_peak']:.0f} | {r['T_boil_alloy']:.0f} | "
                 f"{cen.get('t_liquid', float('nan')) * 1e6:.0f} | {cen.get('t_sol', float('nan')) * 1e6:.0f} | "
                 f"{s.get('Tdot_range', [0, float('nan')])[1]:.2g} | {s.get('G_range', [0, float('nan')])[1]:.2g} | "
                 f"{r['energy']['evaporation_W']:.1f} | {r['cells']}, {r['iterations']}{'' if r['converged'] else ' (not converged)'} |")
    (OUT / "fv_summary.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    R = rows()
    summary_md(R)
    ap = apparent(R)
    for t, o in ap.items():
        print(f"{t:34s} PD x{o.get('photodiode_rel', float('nan')):.2f}  Tw {o['T_wall_K']:.0f}  Tratio {o['ratio_T_700_900_K']:.0f}  " + "  ".join(
            f"{k}: >{v['T_floor_K']:.0f}K {v['L_um']:.0f}x{v['W_um']:.0f}" for k, v in o.items() if isinstance(v, dict)))
    surface_figure(R)
    sections_figure(R)
    gr_figure(R)
    print("done", len(R))
