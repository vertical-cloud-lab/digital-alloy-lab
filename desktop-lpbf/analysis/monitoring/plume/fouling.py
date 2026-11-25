"""Window and cover-slide fouling: how fast each window loses transmission, and how often its slide needs changing
(issue #260; monitoring/plume.md §4).

Inputs:
  - particles.json : condensate deposition per unit source on each window (J/S, kg/m2/s per kg/s), purge off and on, and
                     the share of spatter that lands on each window, per size (this folder's particles.py);
  - plume_source.json (--source; default analysis/out/monitoring/melt/plume_source.json, worker A's melt-pool model): the
                     condensate source. Its 'best' reading is used: the measured Mg and Zn loss rates (Li 2024 via Edison;
                     Velikajne et al. 2026 for 7075) plus its depression-wall Hertz-Knudsen reading for Al. Nominal = the
                     320 W, 1.1 m/s case on a 200 C plate.
Without that file, the source falls back to the composition-only rate: measured Mg and Zn losses (AlSi10Mg 57 % of its Mg,
6061 17 %, 7075 19 % of its Mg and 3-30 % of its Zn) times the deposition rate v x hatch x layer x density at 0.4-1.1 m/s,
times a factor for the Al that leaves with them (x1.5 over AlSi10Mg, x1.07 over 6061, x1.0 over 7075). It is kept in the
output as the lower bound either way. No measured Al fume rate was found.

Optics of a deposit on a fused-silica slide (normal incidence, characteristic-matrix method; Macleod, Thin-Film Optical
Filters, 4th ed., 2010, ch. 2), with Al from Rakic (1995) and amorphous alumina from Boidin et al. (2016):
  - "dense Al film"     : a continuous metal film of the same mass (the bound that over-states it: a film this thin is
                          islands, not a continuous layer);
  - "porous Al, f 0.1"  : Maxwell Garnett mixture of Al spheres in void, 10 % filled (isolated nanoparticles, the
                          condensate's likely form at low coverage);
  - "oxide, f 0.1"      : the same for amorphous alumina (fully oxidised condensate: absorbs nothing, scatters little).
Spatter: each molten droplet that sticks covers a splat ~2.75 d across (Pasandideh-Fard et al. 1996, xi = 0.5 Re^0.25 for
a 100 um Al droplet at 5 m/s, Phys. Fluids 8:650, doi:10.1063/1.868850); a solid one, its own cross-section.

Run: /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/plume/fouling.py
Writes analysis/out/monitoring/plume/fouling.json and fouling.png.
"""
from __future__ import annotations

import importlib.util
import json
import math
import pathlib

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "out" / "monitoring" / "plume"
_s = importlib.util.spec_from_file_location("plume_jet", HERE / "plume_jet.py")
PJ = importlib.util.module_from_spec(_s)
_s.loader.exec_module(PJ)

N_SIO2 = {0.70: 1.4553, 0.85: 1.4525, 1.07: 1.4496}        # Malitson 1965 fused silica
HATCH, LAYER = 100e-6, 30e-6
LOSSES = {  # wt % of each element lost (fraction of its content), and content wt % (via Edison r8-melt-plume, Li 2024)
    "AlSi10Mg": dict(Mg=(0.35, 0.57)),
    "6061": dict(Mg=(1.0, 0.17)),
    "7075": dict(Mg=(2.5, 0.19), Zn=(5.6, (0.03, 0.30))),
}
# Al leaving with the Mg / Zn, by mass, from plume_jet.py's keyhole-onset vapour (Raoult): AlSi10Mg 31 mol % Al, 6061 6 %,
# 7075 under 0.1 %
AL_FACTOR = {"AlSi10Mg": 1.5, "6061": 1.07, "7075": 1.0}
THRESH = {"laser": ("absorption", 3e-4, "optics.md §2.2: >0.03 % absorbed puts the spot outside +/-10 %"),
          "LW": ("transmission loss", 0.10, "camera: 10 % less light (exposure or gain can make it up)"),
          "LP": ("transmission loss", 0.10, "camera"),
          "LC": ("transmission loss", 0.10, "layer camera (window in the boss, protected by its bore)"),
          "BW": ("transmission loss", 0.20, "light window: 20 % less light")}
SPATTER_RATE = (30.0, 100.0, 300.0)                          # spatters (all sizes) per second of lasing: assumed range;
# 100/s of this size mix is ~0.3 g/h, ~1-3 % of the deposited mass (no Al count per mm of track was found)
SIZE_SHARE = {20: 0.35, 35: 0.30, 50: 0.20, 100: 0.10, 150: 0.04, 200: 0.01}   # by number (Chebil 2021: >50 % below 60 um;
# Nagato 2023: ~1 droplet >= 63 um per 4 smaller)


def source_composition_only():
    """Mg and Zn from measured losses, plus the Al that leaves with them by plume_jet.py's Raoult split (the lower bound)."""
    out = {}
    for alloy, el in LOSSES.items():
        lo = hi = 0.0
        for e, (wt, frac) in el.items():
            f0, f1 = (frac, frac) if not isinstance(frac, tuple) else frac
            lo += wt / 100 * f0
            hi += wt / 100 * f1
        rho = 2680.0 if alloy != "7075" else 2810.0
        rates = [w * v * HATCH * LAYER * rho * 3600 * 1e3 * AL_FACTOR[alloy] for w, v in ((lo, 0.4), (hi, 1.1))]
        out[alloy] = dict(loss_wt_pct=(100 * lo, 100 * hi), g_per_h_lasing=rates, nominal=math.sqrt(rates[0] * rates[1]))
    return out


def source_g_per_h(path):
    """The condensate source per alloy, g per hour of lasing. From worker A's melt-pool model when its plume_source.json is
    there: its 'best' reading (measured Mg and Zn loss rates, and the depression-wall reading for Al), nominal = the 320 W
    case on a 200 C plate at 1.1 m/s (else any 320 W case), range = every case of that alloy. Else the composition-only rate."""
    comp = source_composition_only()
    p = pathlib.Path(path) if path else None
    if not (p and p.exists()):
        for v in comp.values():
            v["reading"] = "composition only (measured Mg/Zn losses + Raoult Al share)"
        return comp, None
    src = json.loads(p.read_text())
    out = {}
    for alloy in LOSSES:
        cases = [c for c in src["cases"] if c["inputs"]["alloy"] == alloy and c.get("best", {}).get("g_per_hour_lasing")]
        if not cases:
            out[alloy] = dict(comp[alloy], reading="composition only (no worker-A case for this alloy)")
            continue
        pick = ([c for c in cases if c["inputs"]["P_W"] == 320 and c["inputs"]["T0_K"] > 400 and c["inputs"]["v_m_s"] == 1.1]
                or [c for c in cases if c["inputs"]["P_W"] == 320 and c["inputs"]["v_m_s"] == 1.1] or cases)[0]
        rates = [c["best"]["g_per_hour_lasing"] for c in cases]
        out[alloy] = dict(nominal=pick["best"]["g_per_hour_lasing"], nominal_case=pick["tag"], g_per_h_lasing=[min(rates), max(rates)],
                          cases={c["tag"]: c["best"]["g_per_hour_lasing"] for c in cases},
                          vapour_mole_fraction=pick["best"]["vapour_mole_fraction"],
                          reading="worker A 'best': measured Mg/Zn rates + 'wall' reading for Al (plume_source.json)",
                          composition_only=comp[alloy])
    return out, str(p)


def film_rta(n_film, t, lam_um):
    """R, T, A of a film (complex index n - ik, thickness t in m) on fused silica, light from the argon side."""
    ns = N_SIO2[min(N_SIO2, key=lambda k: abs(k - lam_um))]
    d = 2 * math.pi * n_film * t / (lam_um * 1e-6)
    eta1 = n_film
    B = np.cos(d) + 1j * np.sin(d) / eta1 * ns
    C = 1j * eta1 * np.sin(d) + np.cos(d) * ns
    Y = C / B
    R = abs((1 - Y) / (1 + Y)) ** 2
    T = 4 * ns / abs(B + C) ** 2
    return float(R), float(T), float(1 - R - T)


def bare_T(lam_um):
    ns = N_SIO2[min(N_SIO2, key=lambda k: abs(k - lam_um))]
    return 4 * ns / (1 + ns) ** 2


def maxwell_garnett(eps_i, f, eps_m=1.0):
    a = (eps_i - eps_m) / (eps_i + 2 * eps_m)
    return eps_m * (1 + 2 * f * a) / (1 - f * a)


def deposit_optics(m_kg_m2, lam_um, kind):
    """Relative transmission loss and absorption of a deposit of areal mass m on the slide."""
    if m_kg_m2 <= 0:
        return 0.0, 0.0
    if kind == "dense Al film":
        nf, rho = PJ.al_m(lam_um), 2700.0
        t = m_kg_m2 / rho
    elif kind == "porous Al, f 0.1":
        nm = PJ.al_m(lam_um)
        eps = maxwell_garnett(complex(nm.real, -nm.imag) ** 2, 0.1)    # use +ik internally
        nf = np.sqrt(eps)
        nf = complex(nf.real, -abs(nf.imag))
        t = m_kg_m2 / (0.1 * 2700.0)
    else:
        nf = complex(math.sqrt(maxwell_garnett(PJ.ALOX_N ** 2, 0.1).real), 0.0)
        t = m_kg_m2 / (0.1 * 3000.0)
    R, T, A = film_rta(nf, t, lam_um)
    return 1 - T / bare_T(lam_um), A


def hours_to(threshold, kind_q, rate_kg_m2_h, lam_um, kind):
    """Lasing hours until the deposit reaches the threshold (bisection on the areal mass)."""
    if rate_kg_m2_h <= 0:
        return float("inf")
    f = (lambda m: deposit_optics(m, lam_um, kind)[1]) if kind_q == "absorption" else (lambda m: deposit_optics(m, lam_um, kind)[0])
    lo, hi = 0.0, 1e-9
    while f(hi) < threshold and hi < 1.0:
        hi *= 2
    if f(hi) < threshold:
        return float("inf")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) < threshold:
            lo = mid
        else:
            hi = mid
    return hi / rate_kg_m2_h


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default=str(HERE.parents[1] / "out" / "monitoring" / "melt" / "plume_source.json"),
                    help="worker A's plume_source.json (its 'best' reading is used); missing = composition-only source")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    src, src_path = source_g_per_h(a.source)
    res = dict(source=src, source_file=src_path)
    # optics curves
    masses = np.logspace(-8, -2, 61)                         # kg/m2 (1e-8 = 0.01 mg/m2 ... 10 g/m2)
    res["optics_curves"] = {f"{kind}, {lam} um": dict(m_kg_m2=list(masses), loss=[deposit_optics(m, lam, kind)[0] for m in masses],
                                                      absorption=[deposit_optics(m, lam, kind)[1] for m in masses])
                            for kind in ("dense Al film", "porous Al, f 0.1", "oxide, f 0.1") for lam in (0.85, 1.07)}
    pj = OUT / "particles.json"
    if pj.exists():
        P = json.loads(pj.read_text())
        res["windows"] = {}
        for case, r in P.items():
            rows = {}
            for band, dep in r["deposition_per_source"].items():
                for w, row in dep.items():
                    kind_q, thr, why = THRESH[w]
                    lam = 1.07 if w == "laser" else 0.85
                    for size_key in ("0.05 um, dT 0 K", "0.1 um, dT 0 K", "0.3 um, dT 0 K", "0.1 um, dT 10 K"):
                        J_S = row[size_key]["J_per_S"]                        # kg/m2/s per kg/s
                        for alloy, src in res["source"].items():
                            S = src["nominal"] / 3600 / 1e3              # kg/s of lasing
                            rate_h = J_S * S * 3600                      # kg/m2 per hour of lasing
                            key = f"{w} | {band} | {size_key} | {alloy}"
                            rows[key] = dict(mg_m2_per_h=rate_h * 1e6,
                                             **{f"hours ({kind})": hours_to(thr, kind_q, rate_h, lam, kind)
                                                for kind in ("dense Al film", "porous Al, f 0.1")},
                                             threshold=f"{kind_q} {thr:g} ({why})")
            # spatter hits per hour of lasing
            hits = {}
            if "spatter" in r:
                for lab, bysize in r["spatter"].items():
                    for w in ("LW", "BW", "LP", "LC", "laser"):
                        n_h, area_h = 0.0, 0.0
                        for d_s, share in SIZE_SHARE.items():
                            frac = bysize[str(d_s)]["windows"].get(w, 0.0)
                            n = SPATTER_RATE[1] * share * frac * 3600
                            n_h += n
                            area_h += n * math.pi * (2.75 * d_s * 1e-3 / 2) ** 2 if d_s >= 50 else n * math.pi * (d_s * 1e-3 / 2) ** 2
                        hits[f"{w} | {lab}"] = dict(hits_per_h_at_100_per_s=n_h, splat_mm2_per_h=area_h)
            res["windows"][case] = dict(condensate=rows, spatter=hits)
    (OUT / "fouling.json").write_text(json.dumps(res, indent=1, default=float))
    figure(res)
    for a, s in res["source"].items():
        print(a, s)


def figure(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.2), constrained_layout=True)
    cols = {"dense Al film": "#eb6834", "porous Al, f 0.1": "#2a78d6", "oxide, f 0.1": "#1baf7a"}
    for kind, c in cols.items():
        for lam, ls in ((1.07, "-"), (0.85, "--")):
            cur = res["optics_curves"][f"{kind}, {lam} um"]
            m = np.array(cur["m_kg_m2"]) * 1e6
            axs[0].loglog(m, np.maximum(1e-7, cur["absorption"]), color=c, ls=ls, lw=1.5, label=f"{kind}, {lam} um")
            axs[1].semilogx(m, 100 * np.array(cur["loss"]), color=c, ls=ls, lw=1.5, label=f"{kind}, {lam} um")
    axs[0].axhline(3e-4, color="#52514e", lw=0.8, ls=":")
    axs[0].text(0.012, 3.6e-4, "0.03 %: laser slide limit (optics.md §2.2)", fontsize=7, color="#52514e")
    axs[0].set_xlabel("deposit on the slide (mg/m²)")
    axs[0].set_ylabel("absorbed fraction")
    axs[0].set_title("Absorption of a condensate deposit on fused silica", fontsize=9)
    axs[0].legend(fontsize=6.5, frameon=False)
    axs[1].axhline(10, color="#52514e", lw=0.8, ls=":")
    axs[1].set_xlabel("deposit on the slide (mg/m²)")
    axs[1].set_ylabel("transmission loss (%)")
    axs[1].set_ylim(0, 100)
    axs[1].set_title("Transmission loss (camera windows: change at ~10 %)", fontsize=9)
    fig.savefig(OUT / "fouling.png", dpi=110)


if __name__ == "__main__":
    main()
