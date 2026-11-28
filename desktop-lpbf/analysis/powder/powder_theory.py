"""Powder-spreading theory for the desktop LPBF (issue #260): cohesion and Bond numbers across the PSD, what passes
under the blade, speed scales, blade loads, the 200 C plate (moisture, thermal growth of the gap) and cross-flow
pick-up. Prints a summary and writes desktop-lpbf/analysis/out/powder/theory.json and theory.md.

Re-run:  /tmp/venv/bin/python desktop-lpbf/analysis/powder/powder_theory.py
Every input is a named assumption below; sources are DOIs in REF (checked against Crossref on 2026-11-20).
"""
import json
import math
import os

import numpy as np

OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "powder"))

REF = {
    "bergstrom1997": "https://doi.org/10.1016/S0001-8686(97)00003-1",   # Hamaker constants of inorganic materials
    "rabinovich2000": "https://doi.org/10.1006/jcis.2000.7167",         # adhesion between nanoscale rough surfaces
    "capece2015": "https://doi.org/10.1016/j.powtec.2015.08.031",       # multi-component granular Bond number
    "yang2000": "https://doi.org/10.1103/PhysRevE.62.3900",             # packing of fine (cohesive) particles, DEM
    "shao_lu2000": "https://doi.org/10.1029/2000JD900304",              # threshold friction velocity with cohesion
    "meier2019a": "https://doi.org/10.1016/j.jmatprotec.2018.10.037",   # particle size + adhesion vs layer uniformity
    "meier2019b": "https://doi.org/10.1016/j.powtec.2018.11.072",       # cohesion in fine metal powders (surface energy)
    "nan2018": "https://doi.org/10.1016/j.powtec.2018.07.030",          # jamming in the blade gap
    "haeri2017a": "https://doi.org/10.1016/j.powtec.2016.11.002",       # DEM + experiment, blade vs roller, speed
    "haeri2017b": "https://doi.org/10.1016/j.powtec.2017.08.011",       # blade edge profile optimisation
    "mindt2016": "https://doi.org/10.1007/s11661-016-3470-2",           # powder-bed layer characteristics
    "wischeropp2019": "https://doi.org/10.1016/j.addma.2019.04.019",    # measured single-layer height and packing
    "bidare2017": "https://doi.org/10.1016/j.addma.2017.06.007",        # Heriot-Watt rig, layer transient
    "lu2026": "https://doi.org/10.1038/s41598-025-29968-2",             # steady stacking height H/delta (via Edison)
    "salehi2023": "https://doi.org/10.3390/pr11082276",                 # gap/D90 and speed vs packing (via Edison)
    "girnth2024": "https://doi.org/10.1007/s40964-023-00543-3",         # AlSi10Mg DEM parameters (via Edison)
    "ye2026": "https://doi.org/10.1080/27525783.2026.2694875",          # AlSi10Mg DEM parameters (via Edison)
    "brocksieper2026": "https://doi.org/10.1007/s40964-026-01690-z",    # AlSi10Mg layer roughness vs speed (via Edison)
}

# ---------------------------------------------------------------- powder ----------------------------------------
RHO = 2680.0               # kg/m3 AlSi10Mg
G = 9.81
D50, SIG = 36.0, 0.36      # um, volume log-normal (same as dem_spread.py); sieved 15-63 um
CUT = (15.0, 63.0)


def phi_n(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def cdf_v(d):
    return phi_n(math.log(d / D50) / SIG)


def cut_cdf_v(d):
    lo, hi = cdf_v(CUT[0]), cdf_v(CUT[1])
    return (cdf_v(min(max(d, CUT[0]), CUT[1])) - lo) / (hi - lo)


def dq(q):
    lo, hi = CUT
    for _ in range(60):
        mid = math.sqrt(lo * hi)
        if cut_cdf_v(mid) < q:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


def number_frac_below(d):
    """Number fraction finer than d in the sieved distribution (number pdf ~ volume pdf / d^3)."""
    ds = np.geomspace(CUT[0], CUT[1], 2000)
    pv = np.diff([cut_cdf_v(x) for x in ds])
    dm = np.sqrt(ds[1:] * ds[:-1])
    pn = pv / dm ** 3
    return float(pn[dm < d].sum() / pn.sum())


def weight(d_um):
    return RHO * G * math.pi / 6 * (d_um * 1e-6) ** 3


# ---------------------------------------------------------------- 1. van der Waals with roughness --------------
A_OX = 15e-20       # J, Al2O3 across vacuum/argon (Bergstrom 1997 lists ~15e-20 J for alumina); the native film is a
A_METAL = 33e-20    # few nm thick, so at contact the oxide sets A. 33e-20 J (bare Al) is an upper bound only.
Z0 = 0.4e-9         # m, contact separation used in powder technology


def f_vdw(rstar, a=A_OX, rms=0.0, lam=200e-9):
    """Rabinovich et al. (2000) single-scale asperity model, sphere pair with effective radius R*."""
    smooth = a * rstar / (6 * Z0 ** 2)
    if rms == 0:
        return smooth
    return smooth * (1 / (1 + 58 * rstar * rms / lam ** 2) + 1 / (1 + 1.82 * rms / Z0) ** 2)


def gamma_equiv(force, rstar):
    """Work of adhesion that gives the same pull-off force in JKR (F = 1.5 pi Gamma R*)."""
    return force / (1.5 * math.pi * rstar)


def main():
    res = {"refs": REF}
    d10, d50, d90 = dq(0.1), dq(0.5), dq(0.9)
    res["psd"] = dict(D10=d10, D50=d50, D90=d90, cut=CUT, mass_below_20um=cut_cdf_v(20.0),
                      number_below_20um=number_frac_below(20.0))

    sizes = [15, 20, 25, 30, 36, 45, 57, 63]
    rough = {"smooth": 0.0, "rms 1 nm": 1e-9, "rms 3 nm": 3e-9, "rms 10 nm": 10e-9}
    tab = []
    for d in sizes:
        rs = d * 1e-6 / 4                                    # equal spheres: R* = R/2 = D/4
        row = dict(D_um=d, weight_N=weight(d))
        for k, rms in rough.items():
            f = f_vdw(rs, rms=rms)
            row[k] = dict(F_N=f, Bo=f / weight(d), Gamma_mJm2=gamma_equiv(f, rs) * 1e3)
        for g in (0.2e-3, 1.0e-3):                           # the two DEM cohesion levels
            f = 1.5 * math.pi * g * rs
            row[f"DEM Gamma {g*1e3:g}"] = dict(F_N=f, Bo=f / weight(d))
        tab.append(row)
    res["vdw"] = tab
    # mass fraction of the powder with Bo > 1, 10, 100 for rms 3 nm
    ds = np.geomspace(CUT[0], CUT[1], 400)
    bo3 = np.array([f_vdw(x * 1e-6 / 4, rms=3e-9) / weight(x) for x in ds])
    wv = np.diff([cut_cdf_v(x) for x in ds])
    bom = 0.5 * (bo3[1:] + bo3[:-1])
    res["mass_frac_Bo_gt"] = {str(t): float(wv[bom > t].sum()) for t in (1, 10, 100)}

    # ------------------------------------------------------------ 2. moisture -------------------------------------
    gw = 0.072                                                # N/m water
    rs50 = d50 * 1e-6 / 4
    res["moisture"] = dict(
        capillary_full_D50_N=2 * math.pi * gw * rs50, capillary_full_D50_Bo=2 * math.pi * gw * rs50 / weight(d50),
        capillary_asperity50nm_N=2 * math.pi * gw * 50e-9,
        capillary_asperity50nm_Bo=2 * math.pi * gw * 50e-9 / weight(d50),
        kelvin_radius_nm={f"RH {rh:g}": 0.52 / math.log(1 / rh) for rh in (0.004, 0.1, 0.3, 0.5, 0.7)},
        note="0.52 nm = gamma*Vm/(R*T) for water at 25 C; RH 0.4 % is a -40 C dew point at 25 C",
    )

    # ------------------------------------------------------------ 3. what passes under the blade ------------------
    rz = 10.0                                                 # um, roughness of the last lased layer (assumed)
    gaps = [30, 50, 60, 75, 100, 120, 150]
    res["gap_passage"] = [dict(gap_um=g, gap_over_D90=g / d90, gap_over_D50=g / d50,
                               mass_too_big_to_pass=1 - cut_cdf_v(g - rz), mass_too_big_bare_plate=1 - cut_cdf_v(g))
                          for g in gaps]

    # ------------------------------------------------------------ 4. speed scales ----------------------------------
    res["speed"] = [dict(v_mms=v, froude_D50=(v * 1e-3) / math.sqrt(G * d50 * 1e-6), t_pass_D50_ms=d50 / v,
                         t_fall_D50_ms=math.sqrt(2 * d50 * 1e-6 / G) * 1e3, t_100mm_s=100 / v)
                    for v in (10, 25, 50, 100, 150, 250)]

    # ------------------------------------------------------------ 5. blade loads ----------------------------------
    mods = {"S25": (18.0, 45.0), "M50": (72.0, 70.0), "L75": (163.0, 95.0)}   # g per 15 mm build, dose line mm
    loads = {}
    for m, (g15, lmm) in mods.items():
        per_layer = g15 / 500.0                               # 500 layers of 30 um
        w_pile = per_layer * 1e-3 * G / (lmm * 1e-3)          # N per m of dose line
        loads[m] = dict(dose_g_per_layer=per_layer, pile_weight_N_per_m=w_pile,
                        pile_section_mm2=per_layer / (RHO * 1e-3 * 0.5) / lmm,   # bulk at 50 % solids
                        push_force_mN_mu1=w_pile * lmm * 1e-3 * 1e3,
                        push_force_mN_mu10=10 * w_pile * lmm * 1e-3 * 1e3)
    res["blade_loads"] = loads
    # one coarse particle jammed between the blade and the part: plastic flattening at ~hardness
    h_al = 1.3e9                                              # Pa, ~130 HV for as-atomised AlSi10Mg (assumed)
    jam = []
    for d, squeeze in ((57, 5), (63, 10), (63, 20)):
        a = math.sqrt(d / 2 * 1e-6 * squeeze / 2 * 1e-6)      # contact radius, squeeze shared by two contacts
        jam.append(dict(D_um=d, squeeze_um=squeeze, force_N=h_al * math.pi * a ** 2))
    res["jam_force"] = jam
    res["blade_compliance_um_per_N"] = 3.4 / 10.0             # FEA case 4 as built: 3.4 um at 10 N up

    # ------------------------------------------------------------ 6. the 200 C plate --------------------------------
    a6061, amacor, ahss = 24.0e-6, 9.3e-6, 11.0e-6            # 1/K mean, 20-200 C
    stack = [("plate 10 mm 6061/5083", 10e-3, a6061, 175), ("heater block 14 mm 6061", 14e-3, a6061, 185),
             ("Macor standoffs 8 mm", 8e-3, amacor, 100)]
    grow = [(n, L * a * dt * 1e6) for n, L, a, dt in stack]
    res["thermal"] = dict(
        plate_stack_rise_um={n: g for n, g in grow}, plate_stack_rise_total_um=sum(g for _, g in grow),
        per_K_of_hanging_aluminium_per_40mm_um=40e-3 * a6061 * 1e6,
        holder31_blade18_per_K_um=(31e-3 * a6061 + 18e-3 * ahss) * 1e6,
        z_stack_180mm_al_per_K_um=180e-3 * a6061 * 1e6,
        powder_layer_heating_tau_s=1340 * 900 * (60e-6) ** 2 / 0.15,
    )

    # ------------------------------------------------------------ 7. cross-flow pick-up ----------------------------
    def argon(tk):
        rho = 101325 * 0.039948 / (8.314 * tk)
        mu = 2.125e-5 * (tk / 273.15) ** 1.5 * (273.15 + 144) / (tk + 144)      # Sutherland
        return rho, mu

    def u_star_t(d_um, rho_a, gamma_sl):
        d = d_um * 1e-6
        return math.sqrt(0.0123 * (RHO / rho_a * G * d + gamma_sl / (rho_a * d)))

    xf = []
    for tc in (25, 200):
        rho_a, mu = argon(tc + 273.15)
        nu = mu / rho_a
        for u in (2.0, 2.5, 4.0):
            for x in (0.02, 0.05):
                rex = u * x / nu
                ustar = u * math.sqrt(0.332 / math.sqrt(rex))          # laminar (Blasius) wall shear
                thr = {f"D{d}": u_star_t(d, rho_a, 3e-4) for d in (20, 36, 63)}
                thr_low = {f"D{d}": u_star_t(d, rho_a, 1.65e-4) for d in (20, 36, 63)}
                xf.append(dict(T_C=tc, U_ms=u, x_m=x, Re_x=rex, u_star=ustar, u_star_t_gamma3e4=thr,
                               u_star_t_gamma1p65e4=thr_low, ratio_min=ustar / min(thr_low.values())))
    res["crossflow"] = xf

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "theory.json"), "w") as f:
        json.dump(res, f, indent=1)
    write_md(res)
    return res


def write_md(r):
    p = r["psd"]
    L = []
    A = L.append
    A("# Powder-spreading theory: numbers (generated by `analysis/powder/powder_theory.py`)\n")
    A(f"PSD: log-normal by volume, D50 {D50:g} µm, σ_ln {SIG}, sieved {CUT[0]:g}–{CUT[1]:g} µm → "
      f"D10/D50/D90 = {p['D10']:.1f} / {p['D50']:.1f} / {p['D90']:.1f} µm. "
      f"Below 20 µm: {p['mass_below_20um']*100:.1f} % of the mass, {p['number_below_20um']*100:.0f} % of the particles.\n")
    A("## 1. Cohesion: van der Waals of oxidised Al, asperity-reduced (Rabinovich 2000), A = 15e-20 J, z0 = 0.4 nm\n")
    A("| D (µm) | weight (nN) | smooth: F (nN), Bo | rms 1 nm | rms 3 nm | rms 10 nm | DEM Γ 0.2 mJ/m²: Bo | DEM Γ 1.0: Bo |")
    A("|---|---|---|---|---|---|---|---|")
    for t in r["vdw"]:
        cells = [f"{t[k]['F_N']*1e9:.3g}, {t[k]['Bo']:.3g}" for k in ("smooth", "rms 1 nm", "rms 3 nm", "rms 10 nm")]
        A(f"| {t['D_um']} | {t['weight_N']*1e9:.3g} | " + " | ".join(cells) +
          f" | {t['DEM Gamma 0.2']['Bo']:.3g} | {t['DEM Gamma 1']['Bo']:.3g} |")
    t36 = [t for t in r["vdw"] if t["D_um"] == 36][0]
    A(f"\nEquivalent JKR work of adhesion at D = 36 µm: smooth {t36['smooth']['Gamma_mJm2']:.0f} mJ/m², rms 1 nm "
      f"{t36['rms 1 nm']['Gamma_mJm2']:.2f}, rms 3 nm {t36['rms 3 nm']['Gamma_mJm2']:.2f}, rms 10 nm "
      f"{t36['rms 10 nm']['Gamma_mJm2']:.3f} mJ/m² (DEM-calibrated AlSi10Mg values: 0.5–3.5, Girnth 2024; 0.8, Ye 2026).")
    A(f"Mass fraction with Bo > 1 / 10 / 100 at rms 3 nm: {r['mass_frac_Bo_gt']['1']:.2f} / "
      f"{r['mass_frac_Bo_gt']['10']:.2f} / {r['mass_frac_Bo_gt']['100']:.2f}.\n")
    m = r["moisture"]
    A("## 2. Moisture\n")
    A(f"A full water meniscus between two D50 spheres pulls {m['capillary_full_D50_N']*1e6:.1f} µN (Bo ≈ "
      f"{m['capillary_full_D50_Bo']:.0f}); a meniscus held at a 50 nm asperity pulls {m['capillary_asperity50nm_N']*1e9:.0f} nN "
      f"(Bo ≈ {m['capillary_asperity50nm_Bo']:.0f}). Kelvin radius: " +
      ", ".join(f"{k} → {v:.2f} nm" for k, v in m["kelvin_radius_nm"].items()) + ". " + m["note"] + ".\n")
    A("## 3. What passes under the blade (last layer roughness Rz 10 µm assumed)\n")
    A("| gap (µm) | gap/D90 | gap/D50 | mass too big to pass (on a part) | on a bare plate |")
    A("|---|---|---|---|---|")
    for g in r["gap_passage"]:
        A(f"| {g['gap_um']} | {g['gap_over_D90']:.2f} | {g['gap_over_D50']:.2f} | {g['mass_too_big_to_pass']*100:.1f} % | "
          f"{g['mass_too_big_bare_plate']*100:.1f} % |")
    A("\n## 4. Speed scales (D50)\n")
    A("| v (mm/s) | v/√(gD50) | time to pass one D50 (ms) | free fall of one D50 (ms) | 100 mm stroke (s) |")
    A("|---|---|---|---|---|")
    for s in r["speed"]:
        A(f"| {s['v_mms']} | {s['froude_D50']:.1f} | {s['t_pass_D50_ms']:.2f} | {s['t_fall_D50_ms']:.2f} | {s['t_100mm_s']:.1f} |")
    A("\n## 5. Blade loads\n")
    A("| module | dose per 30 µm layer (g) | pile weight (N/m) | pile section (mm²) | push force at μ_eff 1 / 10 (mN) |")
    A("|---|---|---|---|---|")
    for k, v in r["blade_loads"].items():
        A(f"| {k} | {v['dose_g_per_layer']:.3f} | {v['pile_weight_N_per_m']:.3f} | {v['pile_section_mm2']:.2f} | "
          f"{v['push_force_mN_mu1']:.1f} / {v['push_force_mN_mu10']:.0f} |")
    A("\nOne coarse particle jammed between the HSS blade and the part, flattened at ~1.3 GPa: " +
      "; ".join(f"D {j['D_um']} µm squeezed {j['squeeze_um']} µm → {j['force_N']*1e3:.0f} mN" for j in r["jam_force"]) +
      f". The as-built holder deflects {r['blade_compliance_um_per_N']:.2f} µm/N (FEA case 4).\n")
    t = r["thermal"]
    A("## 6. The 200 °C plate\n")
    A("Rise of the plate top from 25 °C to 200 °C with a cool piston head: " +
      ", ".join(f"{k} {v:.0f} µm" for k, v in t["plate_stack_rise_um"].items()) +
      f"; **total {t['plate_stack_rise_total_um']:.0f} µm**. Blade edge drop per K of holder (31 mm 6061) + blade "
      f"(18 mm HSS): {t['holder31_blade18_per_K_um']:.2f} µm/K; a 180 mm aluminium Z path: {t['z_stack_180mm_al_per_K_um']:.1f} µm/K. "
      f"A 60 µm powder layer reaches the plate temperature in ~{t['powder_layer_heating_tau_s']*1e3:.0f} ms (time constant).\n")
    A("## 7. Cross-flow pick-up (laminar wall shear from the nozzle; Shao & Lu 2000 threshold)\n")
    A("| gas T (°C) | U (m/s) | x from nozzle (mm) | u* (m/s) | threshold u*t at D 20 / 36 / 63 µm, γ 1.65e-4 N/m | u*/u*t, worst size (the coarse end) |")
    A("|---|---|---|---|---|---|")
    for c in r["crossflow"]:
        th = c["u_star_t_gamma1p65e4"]
        A(f"| {c['T_C']} | {c['U_ms']} | {c['x_m']*1e3:.0f} | {c['u_star']:.3f} | "
          f"{th['D20']:.2f} / {th['D36']:.2f} / {th['D63']:.2f} | {c['ratio_min']:.2f} |")
    A("\nSources: " + ", ".join(f"[{k}]({v})" for k, v in r["refs"].items()) + "\n")
    with open(os.path.join(OUT, "theory.md"), "w") as f:
        f.write("\n".join(L))


if __name__ == "__main__":
    out = main()
    print(open(os.path.join(OUT, "theory.md")).read())
