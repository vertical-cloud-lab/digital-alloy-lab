"""The vapour plume of the desktop LPBF machine, by hand: how much metal leaves the melt pool, how fast, how high the jet gets
in the argon cross-flow, what it condenses into, and how much it dims the beam and the coaxial signal (issue #260;
monitoring/plume.md §3).

Until worker A's analysis/out/monitoring/melt/plume_source.json exists, the surface temperatures are scenarios (stated below),
and the vapour pressures come from Clausius-Clapeyron anchored at each element's normal boiling point:
    p_i(T) = 1 atm * exp[ (dH_v,i / R) (1/T_b,i - 1/T) ]                  (dH_v at T_b, CRC Handbook of Chemistry and Physics)
Partial pressures over the alloy are Raoult's law (ideal solution, activity = mole fraction). If plume_source.json is present
(--source), its surface temperature(s), evaporating area and mass rate replace the scenarios.

Evaporation:
  - below the alloy's boiling point (total vapour pressure < 1 atm): no jet; each element diffuses into the argon boundary
    layer, j_i = h_m rho_i,sat, with h_m = Sh D_i / L (Sh ~ 2 on the hot spot), capped at the Hertz-Knudsen flux;
  - above it: Knight's (1979) jump conditions across the Knudsen layer (AIAA J. 17:519-523), with the outer pressure set to the
    ambient 1 atm (subsonic jet) until the sonic limit p_sat >= 4.85 atm.
The jet in the cross-flow: momentum length L_m = sqrt(J / (rho_a U^2)) and the far-field trajectory z / L_m = 2.3 (x / L_m)^(1/3)
(momentum-dominated jet in cross-flow, Hasselbrink & Mungal 2001, J. Fluid Mech. 443:1-25 and 27-68; Pratte & Baines 1967,
J. Hydraul. Div. 93:53-64). Without a jet, the bent-over buoyant plume (Briggs 1975): dz = 1.6 F^(1/3) x^(2/3) / U.
Condensation: the jet's centreline mixes as a variable-density round jet (Y_c = 5 d_eff / z, d_eff = d sqrt(rho_j / rho_a),
Thring-Newby; u_c = 6 u_0 d_eff / z); metal condenses once its partial pressure exceeds p_sat(T); primary particles grow by
free-molecular coagulation with full coalescence until the mixture cools below T_freeze, dv/dt = beta_FM(v, T) phi / 2
(Friedlander, Smoke, Dust and Haze, 2nd ed., 2000, ch. 7 and 8).
Optics: Mie efficiencies (miepython) for Al spheres (Rakic 1995, Appl. Opt. 34:4755, doi:10.1364/AO.34.004755, via
refractiveindex.info) and amorphous alumina (Boidin et al. 2016, Ceram. Int. 42:1177, doi:10.1016/j.ceramint.2015.09.048).

Run: /tmp/capmem 2 /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/plume/plume_jet.py [--source plume_source.json]
Writes analysis/out/monitoring/plume/plume_jet.json and plume_jet.png.
"""
from __future__ import annotations

import argparse
import json
import math
import pathlib

import numpy as np
from scipy.optimize import brentq
from scipy.special import erfc

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "out" / "monitoring" / "plume"
R, KB, ATM, G = 8.314462, 1.380649e-23, 101325.0, 9.81

# element: molar mass (kg/mol), normal boiling point (K) and enthalpy of vaporisation there (J/mol), CRC Handbook
ELEMENTS = {
    "Al": dict(M=26.982e-3, Tb=2792.0, dHv=294.0e3, rho=2700.0),
    "Mg": dict(M=24.305e-3, Tb=1363.0, dHv=127.4e3, rho=1740.0),
    "Zn": dict(M=65.38e-3, Tb=1180.0, dHv=115.3e3, rho=7140.0),
    "Si": dict(M=28.086e-3, Tb=3538.0, dHv=359.0e3, rho=2330.0),
    "Cu": dict(M=63.546e-3, Tb=2835.0, dHv=300.4e3, rho=8960.0),
}
# nominal compositions, wt% (Aluminum Association limits' mid-points; Al = balance)
ALLOYS = {
    "AlSi10Mg": {"Si": 10.0, "Mg": 0.35},
    "6061": {"Mg": 1.0, "Si": 0.6, "Cu": 0.28},
    "7075": {"Zn": 5.6, "Mg": 2.5, "Cu": 1.6},
}
# argon
M_AR, CP_AR = 39.948e-3, 520.0
RHO_AR = ATM * M_AR / (R * 298.15)                     # 1.63 kg/m3 at 25 C (make_case.py uses 1.65 at +10 mbar)
GAMMA = 5.0 / 3.0                                      # monatomic vapour and argon

# operating point (monitoring.md, gas-flow.md §0)
SPOT_D = 96e-6                                         # 1/e2 spot diameter
SCAN = (0.4, 1.1)                                      # m/s
HATCH, LAYER = 100e-6, 30e-6
U_CROSS = {"200 L/min (fix200), at 1 / 3 mm": (2.2, 2.94), "140 L/min (fix140), at 1 / 3 mm": (1.40, 2.03)}   # gas-flow.md §0.5

# Rakic (1995) Al, n and k (lambda in um), the rows from refractiveindex.info's copy (CC0) between 0.62 and 1.24 um
AL_NK = np.array([
    (0.61993, 1.3660, 7.4052), (0.65225, 1.5724, 7.7354), (0.68881, 1.8301, 8.0601), (0.72932, 2.1606, 8.3565),
    (0.77491, 2.6154, 8.4914), (0.79478, 2.7675, 8.3866), (0.81569, 2.7668, 8.2573), (0.83774, 2.6945, 8.1878),
    (0.88561, 2.2802, 8.1134), (0.91166, 1.9739, 8.3058), (0.93928, 1.6784, 8.5970), (0.96863, 1.4867, 9.0655),
    (0.99988, 1.4359, 9.4939), (1.0332, 1.3998, 9.8914), (1.1271, 1.3281, 10.969), (1.2399, 1.3157, 12.245)])
ALOX_N = 1.665                                         # amorphous Al2O3 film at ~0.9-1.07 um (Boidin et al. 2016)


def al_m(lam_um):
    n = np.interp(lam_um, AL_NK[:, 0], AL_NK[:, 1])
    k = np.interp(lam_um, AL_NK[:, 0], AL_NK[:, 2])
    return complex(n, -k)


def p_pure(el, T):
    e = ELEMENTS[el]
    return ATM * math.exp(e["dHv"] / R * (1.0 / e["Tb"] - 1.0 / T))


def mole_fractions(alloy):
    w = dict(ALLOYS[alloy])
    w["Al"] = 100.0 - sum(w.values())
    n = {el: wt / ELEMENTS[el]["M"] for el, wt in w.items()}
    tot = sum(n.values())
    return {el: v / tot for el, v in n.items()}


def p_partial(alloy, T):
    x = mole_fractions(alloy)
    return {el: x[el] * p_pure(el, T) for el in x}


def t_boil(alloy, p=ATM):
    return brentq(lambda T: sum(p_partial(alloy, T).values()) - p, 800.0, 4000.0)


def knight(M):
    """Knight (1979) jump conditions across the Knudsen layer for a monatomic vapour, Mach number M at its outer edge.
    Returns T_v/T_s, rho_v/rho_s and p_v/p_s (rho_s, p_s: saturated vapour at T_s)."""
    m = M * math.sqrt(GAMMA / 2.0)
    a = (GAMMA - 1.0) / (GAMMA + 1.0) * m / 2.0
    tr = (math.sqrt(1.0 + math.pi * a * a) - math.sqrt(math.pi) * a) ** 2
    e = math.exp(m * m) * erfc(m)
    rr = math.sqrt(1.0 / tr) * ((m * m + 0.5) * e - m / math.sqrt(math.pi)) + 0.5 / tr * (1.0 - math.sqrt(math.pi) * m * e)
    return tr, rr, tr * rr


def evaporation(alloy, Ts, area, u_gas=2.5, L=300e-6):
    """Mass flux (kg/m2/s), mass rate (kg/s), vapour composition, jet speed and temperature for a hot spot at Ts."""
    pp = p_partial(alloy, Ts)
    ps = sum(pp.values())
    y = {el: v / ps for el, v in pp.items()}                        # vapour mole fractions
    Mv = sum(y[el] * ELEMENTS[el]["M"] for el in y)
    out = dict(T_s=Ts, p_sat_atm=ps / ATM, vapour_mole_fraction={k: round(v, 4) for k, v in y.items() if v > 1e-4},
               M_vapour=Mv)
    j_hk = ps * math.sqrt(Mv / (2 * math.pi * R * Ts))              # Hertz-Knudsen, one-way
    if ps <= ATM:
        # diffusion-limited: D ~ 2e-5 m2/s at 300 K scaled with T^1.75 at the film temperature, Sh ~ 2
        Tf = 0.5 * (Ts + 300.0)
        D = 2.0e-5 * (Tf / 300.0) ** 1.75
        h_m = 2.0 * D / L
        j = min(sum(h_m * pp[el] * ELEMENTS[el]["M"] / (R * Ts) for el in pp), 0.82 * j_hk)
        out.update(regime="diffusion-limited (no jet)", mach=0.0, u_jet=0.0, T_v=Ts, rho_v=ps * Mv / (R * Ts), j=j,
                   j_hertz_knudsen=j_hk, h_m=h_m)
    else:
        ratio = ATM / ps
        if ratio <= knight(1.0)[2]:
            M = 1.0
        else:
            M = brentq(lambda mm: knight(mm)[2] - ratio, 1e-6, 1.0)
        tr, rr, _ = knight(M)
        rho_s = ps * Mv / (R * Ts)
        Tv, rho_v = tr * Ts, rr * rho_s
        u = M * math.sqrt(GAMMA * R * Tv / Mv)
        out.update(regime="jet (Knight jump, subsonic)" if M < 1 else "jet (sonic)", mach=M, u_jet=u, T_v=Tv, rho_v=rho_v,
                   j=rho_v * u, j_hertz_knudsen=j_hk, momentum_flux_density=rho_v * u * u + (ATM if M < 1 else 0) * 0)
    out["area_m2"] = area
    out["mdot_kg_s"] = out["j"] * area
    out["mdot_by_element_kg_s"] = {el: out["mdot_kg_s"] * y[el] * ELEMENTS[el]["M"] / Mv for el in y if y[el] > 1e-4}
    return out


def jet_in_crossflow(ev, d_src, U):
    """Momentum length and trajectory of the vapour jet in a cross-flow U (or the buoyant plume if there is no jet)."""
    if ev["u_jet"] > 0:
        J = ev["mdot_kg_s"] * ev["u_jet"]                           # N
        Lm = math.sqrt(J / (RHO_AR * U * U))
        r = math.sqrt(ev["rho_v"] * ev["u_jet"] ** 2 / (RHO_AR * U * U))
        x = np.array([0.5, 1, 2, 5, 10, 20, 50]) * 1e-3
        z = 2.3 * Lm * (x / Lm) ** (1.0 / 3.0)
        return dict(J_N=J, L_m_mm=Lm * 1e3, r=r, rd_mm=r * d_src * 1e3, x_mm=list(x * 1e3), z_mm=list(z * 1e3),
                    z_at_10mm=float(2.3 * Lm * (0.01 / Lm) ** (1 / 3)) * 1e3, z_at_50mm=float(2.3 * Lm * (0.05 / Lm) ** (1 / 3)) * 1e3)
    # buoyant bent-over plume: heat carried = enthalpy of the vapour + latent heat released on condensing (~2 W scale) plus the
    # melt pool's convective loss (small); F = g Q / (pi rho cp T)
    Q = ev["mdot_kg_s"] * 1.2e7 + 0.3
    F = G * Q / (math.pi * RHO_AR * CP_AR * 300.0)
    x = np.array([0.5, 1, 2, 5, 10, 20, 50]) * 1e-3
    z = 1.6 * F ** (1 / 3) * x ** (2 / 3) / U
    return dict(Q_W=Q, F_m4_s3=F, x_mm=list(x * 1e3), z_mm=list(z * 1e3), z_at_10mm=float(1.6 * F ** (1 / 3) * 0.01 ** (2 / 3) / U * 1e3),
                z_at_50mm=float(1.6 * F ** (1 / 3) * 0.05 ** (2 / 3) / U * 1e3))


def beta_fm(d, T, rho_p):
    """Free-molecular collision kernel for two equal spheres of diameter d (m3/s)."""
    v = math.pi / 6 * d ** 3
    return 4 * math.sqrt(2) * (3 / (4 * math.pi)) ** (1 / 6) * math.sqrt(6 * KB * T / rho_p) * v ** (1 / 6)


def primary_size(ev, d_src, alloy, T_freeze=900.0):
    """Primary particle diameter: coagulation with full coalescence along the plume's centreline until it cools below T_freeze.
    Jet: a variable-density round jet of pure vapour (u_c = 6 u_0 d_eff / z, Y = 5 d_eff / z). No jet: argon carrying the
    saturated vapour fraction p_sat / 1 atm off the hot spot in a ~0.3 mm boundary layer at ~1 m/s, diluted the same way
    (crude). The condensing species keep the vapour's composition; nucleation once the metal's partial pressure exceeds 10x
    the pure species' saturation pressures (weighted by the vapour composition)."""
    y = ev["vapour_mole_fraction"]
    tot = sum(y.values())
    y = {k: v / tot for k, v in y.items()}
    wsum = sum(y[k] * ELEMENTS[k]["M"] for k in y)
    rho_p = 1.0 / sum((y[k] * ELEMENTS[k]["M"] / wsum) / ELEMENTS[k]["rho"] for k in y)   # condensed metal, before oxidising
    Tv, Mv = ev["T_v"], ev["M_vapour"]
    if ev["u_jet"] <= 0:
        u0, d_eff = 1.0, 3e-4
        x0 = min(1.0, ev["p_sat_atm"])
        Y0 = x0 * Mv / (x0 * Mv + (1 - x0) * M_AR)
    else:
        u0 = ev["u_jet"]
        d_eff = d_src * math.sqrt(ev["rho_v"] / RHO_AR)
        Y0 = 1.0
    z = 5 * d_eff
    v = math.pi / 6 * (0.3e-9) ** 3                            # from atoms once supersaturated
    started, T_nuc, t = False, None, 0.0
    while True:
        f = min(1.0, 5 * d_eff / z)                            # source-fluid fraction on the centreline
        Yc = Y0 * f                                            # metal mass fraction
        T = 298.0 + (Tv - 298.0) * f
        uc = max(0.05, u0 * min(1.0, 6 * d_eff / z))
        Mmix = 1.0 / (Yc / Mv + (1 - Yc) / M_AR)
        rho_mix = ATM * Mmix / (R * T)
        phi = Yc * rho_mix / rho_p
        x_metal = (Yc / Mv) / (Yc / Mv + (1 - Yc) / M_AR)
        p_eq = sum(y[k] * p_pure(k, T) for k in y)
        if not started and x_metal * ATM > 10 * p_eq:
            started, T_nuc = True, T
        dz = z * 0.01
        dt = dz / uc
        if started:
            d = (6 * v / math.pi) ** (1 / 3)
            v += 0.5 * beta_fm(d, T, rho_p) * phi * dt
        t += dt
        z += dz
        if (started and T < T_freeze) or z > 0.05:
            break
    d = (6 * v / math.pi) ** (1 / 3)
    return dict(d_primary_nm=d * 1e9, T_nucleation_K=T_nuc, z_freeze_mm=z * 1e3, t_freeze_us=t * 1e6, d_eff_um=d_eff * 1e6,
                T_freeze_K=T_freeze, rho_condensate=rho_p)


def mie_mec(lam_um, d_m, material="Al", rho=2700.0):
    """Mass extinction / absorption / scattering coefficients (m2/kg) of spheres of diameter d."""
    import miepython
    m = al_m(lam_um) if material == "Al" else complex(ALOX_N, 0.0)
    qe, qs, _, _ = miepython.efficiencies(m, d_m * 1e6, lam_um)
    k = 3.0 / (2.0 * rho * d_m)
    return dict(ext=float(qe) * k, sca=float(qs) * k, abs=float(qe - qs) * k)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", default=str(HERE.parents[1] / "out" / "monitoring" / "melt" / "plume_source.json"))
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    res = dict(notes=[], alloys={})
    src = None
    if pathlib.Path(a.source).exists():
        src = json.loads(pathlib.Path(a.source).read_text())
        res["notes"].append(f"surface temperatures and areas from {a.source}")
    else:
        res["notes"].append("plume_source.json not found: surface temperatures are scenarios (Clausius-Clapeyron at T_s)")
    hot_area = math.pi * (SPOT_D / 2) ** 2 * 0.5               # conduction: hottest half of the spot area (assumption)
    kh_d = 0.7 * SPOT_D                                         # keyhole mouth ~0.7 x the spot (assumption)
    kh_area = math.pi * kh_d ** 2 / 4
    for alloy in ALLOYS:
        Tb = t_boil(alloy)
        r = dict(mole_fraction={k: round(v, 4) for k, v in mole_fractions(alloy).items()}, T_boil_alloy_K=Tb,
                 T_boil_Al_K=ELEMENTS["Al"]["Tb"], scenarios={})
        # scenarios: conduction at 2000 and 2300 K (or 0.9 Tb if lower), the alloy's own boiling point + 50 K (keyhole onset),
        # and the keyhole wall at p_sat = 2 atm (recoil + capillary pressure of a ~30 um keyhole)
        T2atm = t_boil(alloy, 2 * ATM)
        scen = {"conduction, T_s 2000 K": (min(2000.0, 0.97 * Tb), hot_area),
                "conduction, T_s 2300 K": (min(2300.0, 0.99 * Tb), hot_area),
                "keyhole onset, p_sat 1.2 atm": (t_boil(alloy, 1.2 * ATM), kh_area),
                "keyhole, p_sat 2 atm": (T2atm, kh_area)}
        if src and alloy in src.get("alloys", {}):
            s = src["alloys"][alloy]
            for k_, v_ in s.get("scenarios", {}).items():
                scen[f"plume_source: {k_}"] = (v_["T_s"], v_.get("area_m2", kh_area))
        for name, (Ts, area) in scen.items():
            ev = evaporation(alloy, Ts, area)
            d_src = kh_d if ev["u_jet"] > 0 else SPOT_D
            jic = {k: jet_in_crossflow(ev, d_src, U[1]) for k, U in U_CROSS.items()}
            ps = primary_size(ev, d_src, alloy, T_freeze=650.0 if alloy == "7075" else 900.0)
            mg = ev["mdot_kg_s"]
            r["scenarios"][name] = dict(evaporation=ev, jet=jic, primary=ps,
                                        mdot_g_per_h_lasing=mg * 3600 * 1e3,
                                        loss_wt_pct_of_new_material_at_0p4_1p1_m_s=[100 * mg / (v * HATCH * LAYER * 2680.0) for v in SCAN])
        res["alloys"][alloy] = r
    # composition-loss cross-check (measured losses as wt% of the deposited material)
    res["composition_loss_check"] = dict(
        note="mass rate = loss fraction x deposition rate (v x hatch x layer x 2680 kg/m3); deposition 3.2-8.8 mg/s at 0.4-1.1 m/s",
        cases={"7075, ~1 wt% Zn + 0.3 wt% Mg lost (Velikajne 2026 via preheat-and-plates.md, 400 C plate)":
               [0.013 * v * HATCH * LAYER * 2800 * 3600 * 1e3 for v in SCAN],
               "AlSi10Mg or 6061, 0.05-0.1 wt% lost (assumed, Mg plus Al)": [0.0005 * SCAN[0] * HATCH * LAYER * 2680 * 3600 * 1e3,
                                                                             0.001 * SCAN[1] * HATCH * LAYER * 2680 * 3600 * 1e3]},
        units="g per hour of lasing")
    # optics: Mie mass coefficients of primaries and compact agglomerates, Al and alumina
    lams = (0.70, 0.85, 0.90, 1.07)
    sizes = (10e-9, 20e-9, 50e-9, 100e-9, 300e-9, 1000e-9)
    res["mie_m2_per_kg"] = {f"{mat}, {d * 1e9:.0f} nm": {f"{lam:.2f} um": mie_mec(lam, d, mat, 2700.0 if mat == "Al" else 3000.0)
                                                         for lam in lams}
                            for mat in ("Al", "AlOx") for d in sizes}
    # beam / coaxial attenuation through the plume above the spot: column of condensed metal along the jet axis,
    # sigma = integral of C dz from the condensation height to L_m, C = Y_c rho_mix (upper bound: all condensed)
    att = {}
    for alloy in ALLOYS:
        for name, sc in res["alloys"][alloy]["scenarios"].items():
            ev = sc["evaporation"]
            mg = ev["mdot_kg_s"]
            if ev["u_jet"] > 0:
                d_eff = sc["primary"]["d_eff_um"] * 1e-6
                Lm = sc["jet"]["200 L/min (fix200), at 1 / 3 mm"]["L_m_mm"] * 1e-3
                z0 = max(5 * d_eff, sc["primary"]["z_freeze_mm"] * 1e-3 * 0.3)
                sigma = 5 * d_eff * ev["rho_v"] * math.log(max(Lm, 2 * z0) / z0)
            else:
                # no jet: condensate in a layer ~1-2 mm thick swept at U_rel ~ 2 m/s; beam crosses it vertically
                sigma = mg / (2.0 * 1.0e-3)                     # kg/m2 = mdot / (U_rel x layer width ~1 mm)
            att[f"{alloy}: {name}"] = dict(column_kg_m2=sigma, **{
                f"tau {lam:.2f} um, {lab}": sigma * res["mie_m2_per_kg"][key][f"{lam:.2f} um"]["ext"]
                for lam in (0.85, 1.07) for lab, key in (("20 nm primaries", "Al, 20 nm"), ("300 nm compact", "Al, 300 nm"))})
    res["plume_column_attenuation"] = att
    # chamber background: well-mixed limit C = mdot / Q over the 120 mm beam path
    res["background_well_mixed"] = {
        f"{alloy}, {name}": dict(C_mg_m3=sc["evaporation"]["mdot_kg_s"] / (240 / 60000) * 1e6,
                                 tau_1070_300nm_120mm=sc["evaporation"]["mdot_kg_s"] / (240 / 60000) * 0.12
                                 * res["mie_m2_per_kg"]["Al, 300 nm"]["1.07 um"]["ext"])
        for alloy in ALLOYS for name, sc in res["alloys"][alloy]["scenarios"].items()}
    (OUT / "plume_jet.json").write_text(json.dumps(res, indent=1, default=float))
    figure(res)
    summary(res)


def figure(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(13.5, 4.2), constrained_layout=True)
    T = np.linspace(1500, 3200, 200)
    cols = {"AlSi10Mg": "#2a78d6", "6061": "#1baf7a", "7075": "#eb6834"}
    for alloy, c in cols.items():
        axs[0].semilogy(T, [sum(p_partial(alloy, t).values()) / ATM for t in T], color=c, lw=1.6, label=alloy)
    for el, ls in (("Al", ":"), ("Mg", "--"), ("Zn", "-.")):
        axs[0].semilogy(T, [p_pure(el, t) / ATM for t in T], color="#52514e", lw=0.9, ls=ls, label=f"pure {el}")
    axs[0].axhline(1, color="#0b0b0b", lw=0.6)
    axs[0].set_ylim(1e-3, 1e3)
    axs[0].set_xlabel("surface temperature (K)")
    axs[0].set_ylabel("equilibrium vapour pressure (atm)")
    axs[0].set_title("Vapour pressure over the alloy (Raoult, ideal)", fontsize=9)
    axs[0].legend(fontsize=7, frameon=False)
    for (scn, c) in (("conduction, T_s 2300 K", "#1baf7a"), ("keyhole onset, p_sat 1.2 atm", "#2a78d6"), ("keyhole, p_sat 2 atm", "#eb6834")):
        sc = res["alloys"]["AlSi10Mg"]["scenarios"][scn]
        for k, ls in zip(U_CROSS, ("-", "--")):
            j = sc["jet"][k]
            axs[1].plot(j["x_mm"], j["z_mm"], color=c, ls=ls, lw=1.4, label=f"{scn.split(',')[0]}, {k.split(' (')[0]}")
    axs[1].axhline(1.0, color="#52514e", lw=0.7, ls=":")
    axs[1].text(30, 1.3, "Bitharas 2022: ~1 mm rise in 2.1 m/s", fontsize=6.5, color="#52514e")
    axs[1].axhspan(0, 20, color="#e8e8e4", zorder=0)
    axs[1].text(30, 18.5, "fixed layout's bed jet (~20 mm thick)", fontsize=6.5, color="#52514e")
    axs[1].set_ylim(0, 22)
    axs[1].set_xlabel("distance downstream of the spot (mm)")
    axs[1].set_ylabel("plume centreline height (mm)")
    axs[1].set_title("AlSi10Mg plume in the cross-flow: no jet, keyhole onset, keyhole", fontsize=9)
    axs[1].legend(fontsize=6, frameon=False, loc="center right")
    sizes = np.logspace(-8, -6, 40)
    for lam, ls in ((0.85, "--"), (1.07, "-")):
        axs[2].loglog(sizes * 1e9, [mie_mec(lam, d)["ext"] for d in sizes], color="#2a78d6", ls=ls, label=f"Al, {lam} um, extinction")
        axs[2].loglog(sizes * 1e9, [mie_mec(lam, d)["abs"] for d in sizes], color="#eb6834", ls=ls, label=f"Al, {lam} um, absorption")
        axs[2].loglog(sizes * 1e9, [mie_mec(lam, d, "AlOx", 3000.0)["ext"] for d in sizes], color="#1baf7a", ls=ls, label=f"alumina, {lam} um")
    axs[2].set_xlabel("particle diameter (nm)")
    axs[2].set_ylabel("mass coefficient (m²/kg)")
    axs[2].set_title("Mie: condensate per kg (spheres)", fontsize=9)
    axs[2].legend(fontsize=6.5, frameon=False)
    fig.savefig(OUT / "plume_jet.png", dpi=110)


def summary(res):
    for alloy, r in res["alloys"].items():
        print(f"{alloy}: boils at {r['T_boil_alloy_K']:.0f} K (pure Al {r['T_boil_Al_K']:.0f} K); x = {r['mole_fraction']}")
        for name, sc in r["scenarios"].items():
            ev = sc["evaporation"]
            j = sc["jet"]["200 L/min (fix200), at 1 / 3 mm"]
            print(f"  {name:32s} Ts {ev['T_s']:6.0f} K  p {ev['p_sat_atm']:6.2f} atm  {ev['regime'][:22]:22s} M {ev['mach']:.2f} "
                  f"u {ev['u_jet']:5.0f} m/s  mdot {sc['mdot_g_per_h_lasing']:7.3f} g/h  loss {sc['loss_wt_pct_of_new_material_at_0p4_1p1_m_s'][1]:.3f}-"
                  f"{sc['loss_wt_pct_of_new_material_at_0p4_1p1_m_s'][0]:.3f} wt%  z(10 mm) {j['z_at_10mm']:.1f} mm  "
                  f"Lm {j.get('L_m_mm', float('nan')):.2f} mm  d_p {sc['primary']['d_primary_nm']:.1f} nm  vapour {ev['vapour_mole_fraction']}")
    for k, v in res["plume_column_attenuation"].items():
        print(f"  {k:50s} column {v['column_kg_m2']:.2e} kg/m2  " + "  ".join(f"{kk} {vv:.1e}" for kk, vv in v.items() if kk.startswith("tau")))


if __name__ == "__main__":
    main()
