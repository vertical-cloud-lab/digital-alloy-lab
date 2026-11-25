"""Tables for monitoring/melt-pool.md, generated from the JSON outputs so the note's numbers trace to the runs (issue #260).

Run:  python report.py   -> analysis/out/monitoring/melt/tables.md
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import props as PR  # noqa: E402
import evap as EV  # noqa: E402

OUT = HERE.parents[1] / "out" / "monitoring" / "melt"


def load():
    rows = {}
    for l in (OUT / "fv_cases.jsonl").read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            rows[r["case"]["tag"]] = r
    J = {n: json.loads((OUT / f"{n}.json").read_text()) for n in ("analytic", "transient", "plume_source", "apparent")
         if (OUT / f"{n}.json").exists()}
    return rows, J


def f(x, nd=0):
    return "–" if x is None or (isinstance(x, float) and not np.isfinite(x)) else f"{x:.{nd}f}"


def props_table():
    L = ["| Alloy | Solidus / liquidus (°C) | Freezing range (K) | k solid, 25 °C / at solidus (W/m K) | k liquid at liquidus "
         "(W/m K) | Latent heat (kJ/kg) | Enthalpy to melt from 25 °C (kJ/kg) | Mean diffusivity to liquidus (mm²/s) | "
         "Boils at 1 atm, Raoult (°C) | Vapour at that point (mol %) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for name in PR.ALLOYS:
        a = PR.Alloy(name)
        mp = a.mean_props(298.15)
        Tb = a.T_boil()
        pp = a.partial_pressures(Tb)
        s = sum(pp.values())
        vap = ", ".join(f"{el} {100 * p / s:.0f}" for el, p in sorted(pp.items(), key=lambda kv: -kv[1]) if p / s > 0.01)
        L.append(f"| {a.label} | {a.T_sol - 273.15:.0f} / {a.T_liq - 273.15:.0f} | {a.T_liq - a.T_sol:.0f} | "
                 f"{float(a.k_solid(298.15)):.0f} / {float(a.k_solid(a.T_sol)):.0f} | {a.k_l_liq:.0f} | {a.L_f / 1e3:.0f} | "
                 f"{mp['dH_melt'] / 1e3:.0f} | {mp['alpha'] * 1e6:.0f} | {Tb - 273.15:.0f} | {vap} |")
    return L


def analytic_table(J):
    a = J["analytic"]
    L = ["| Alloy | Plate (°C) | P (W) | v (m/s) | A (Gan Eq. 6) | Ke | Gan keyhole depth (µm) | ΔH/h_s | Rosenthal L × W × D (µm) | "
         "Eagar–Tsai L × W × D (µm) | Marangoni scale (m/s) | Flow Péclet | Regime by Ke |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in a["table"]:
        if r.get("spot_label"):
            continue
        L.append(f"| {r['alloy']} | {r['T0'] - 273.15:.0f} | {r['P']:.0f} | {r['v']} | {r['A']:.2f} | {r['Ke']:.1f} | "
                 f"{r['e_keyhole'] * 1e6:.0f} | {r['dH_hs']:.0f} | "
                 f"{r.get('L_R', 0) * 1e6:.0f} × {r.get('W_R', 0) * 1e6:.0f} × {r.get('D_R', 0) * 1e6:.0f} | "
                 f"{r['L'] * 1e6:.0f} × {r['W'] * 1e6:.0f} × {r['D'] * 1e6:.0f} | "
                 f"{r['u_marangoni']:.0f} | {r['Pe_flow']:.0f} | {r['regime']}{', balling' if r['balling'] else ''} |")
    return L


def spot_table(J):
    a = J["analytic"]
    L = ["| Spot | A | Ke | Gan keyhole depth (µm) | ΔH/h_s | Regime by Ke |", "|---|---|---|---|---|---|"]
    for r in a["table"]:
        if not r.get("spot_label"):
            continue
        L.append(f"| {r['spot_label']} | {r['A']:.2f} | {r['Ke']:.1f} | {r['e_keyhole'] * 1e6:.0f} | {r['dH_hs']:.0f} | {r['regime']} |")
    return L


def bands_table(J):
    b = J["analytic"]["power_bands_1p1ms_96um"]
    L = ["| Alloy, plate | Ke 1.4 (conduction ends) | Ke 6 (keyhole by Gan) | Ke 16 (porosity risk) |", "|---|---|---|---|"]
    for k, v in b.items():
        L.append(f"| {k.replace('_', ', ')} | {f(v['P_at_Ke_1.4'])} W | {f(v['P_at_Ke_6'])} W | {f(v['P_at_Ke_16'])} W |")
    return L


def validation_table(rows, J):
    L = ["| P (W), v (m/s) | Measured W / D (µm), D/W | Rosenthal / Eagar–Tsai, A from Gan: W / D (µm) | Gan: A, Ke, keyhole depth (µm) | "
         "3D model, A 0.35: W / D below powder top / D into substrate (µm) | 3D peak T (K) |", "|---|---|---|---|---|---|"]
    for v in J["analytic"]["validation"]:
        tag = f"val_{v['P']:.0f}W_{v['v']:.3f}ms"
        r = rows.get(tag)
        fv = "–"
        pk = "–"
        if r:
            fv = f"{r['liquid']['W_any'] * 1e6:.0f} / {r['liquid']['D'] * 1e6:.0f} / {r['liquid']['D'] * 1e6 - 30:.0f}"
            pk = f"{r['T_peak']:.0f}"
        L.append(f"| {v['P']}, {v['v']} | {v['W_meas_um']:.0f} / {v['D_meas_um']:.0f}, {v['DW_meas']:.2f} | "
                 f"{v.get('W_R_um', 0):.0f} / {v.get('D_R_um', 0):.0f}; {v['W_ET_um']:.0f} / {v['D_ET_um']:.0f} | "
                 f"{v['A']:.2f}, {v['Ke']:.1f}, {v['e_keyhole_um']:.0f} | {fv} | {pk} |")
    for A in (0.30, 0.40):
        r = rows.get(f"val_300W_0.917ms_A{A:.2f}")
        if r:
            L.append(f"| 300, 0.917, A {A:.2f} | 202 / 70 | | | {r['liquid']['W_any'] * 1e6:.0f} / {r['liquid']['D'] * 1e6:.0f} / "
                     f"{r['liquid']['D'] * 1e6 - 30:.0f} | {r['T_peak']:.0f} |")
    return L


def fv_table(rows, J):
    ap = J.get("apparent", {})
    L = ["| Case | Liquid pool L × W × D (µm) | Pixels at 8 µm/px (L × W) | Peak T, flat model (K) | Alloy boils / depression wall (K) | "
         "Si camera 850 nm, 12-bit: sees above (K), L × W (µm) | InGaAs 1550 nm, 12-bit: above (K), L × W (µm) | Photodiode vs "
         "AlSi10Mg 1.1 m/s 25 °C |", "|---|---|---|---|---|---|---|---|"]
    for t, r in sorted(rows.items()):
        if not t.startswith(("ref_", "map_")):
            continue
        Lq = r["liquid"]
        a = ap.get(t, {})
        si, ig = a.get("Si_850nm_12bit", {}), a.get("InGaAs_1550nm_12bit", {})
        L.append(f"| {t.replace('ref_', '').replace('map_', '')} | {Lq['L'] * 1e6:.0f} × {Lq['W_any'] * 1e6:.0f} × {Lq['D'] * 1e6:.0f} | "
                 f"{Lq['L'] * 1e6 / 8:.0f} × {Lq['W_any'] * 1e6 / 8:.0f} | {r['T_peak']:.0f} | {r['T_boil_alloy']:.0f} / "
                 f"{f(a.get('T_wall_K'))} | {f(si.get('T_floor_K'))}, {f(si.get('L_um'))} × {f(si.get('W_um'))} | "
                 f"{f(ig.get('T_floor_K'))}, {f(ig.get('L_um'))} × {f(ig.get('W_um'))} | {f(a.get('photodiode_rel'), 2)} | "
                 f"{f(a.get('ratio_T_700_900_K'))} |")
    return L


def sol_table(rows):
    L = ["| Case | Time liquid, surface centre (µs) | Mushy time, surface centre / range (µs) | Cooling at the liquidus, "
         "centre / median / max (10⁶ K/s) | G at the liquidus, min–max (10⁶ K/m) | R min–max (m/s) | G/R median (K s/mm²) |",
         "|---|---|---|---|---|---|---|"]
    for t, r in sorted(rows.items()):
        if not t.startswith(("ref_", "map_")) or "solid" not in r:
            continue
        s = r["solid"]
        c = s["centre"]
        GR = np.median([1.0]) if False else s["G_range"][1] / max(s["R_range"][1], 1e-9) / 1e6
        L.append(f"| {t.replace('ref_', '').replace('map_', '')} | {c['t_liquid'] * 1e6:.0f} | {c['t_sol'] * 1e6:.0f} / "
                 f"{s['t_sol_range'][0] * 1e6:.0f}–{s['t_sol_range'][2] * 1e6:.0f} | {c['Tdot_liq'] / 1e6:.2f} / "
                 f"{s['Tdot_range'][1] / 1e6:.2f} / {s['Tdot_range'][2] / 1e6:.2f} | {s['G_range'][0] / 1e6:.2f}–{s['G_range'][2] / 1e6:.1f} | "
                 f"{s['R_range'][0]:.2f}–{s['R_range'][2]:.2f} | {GR:.1f} |")
    return L


def sens_table(rows):
    base = rows.get("sens_base_coarse")
    L = ["| Change (AlSi10Mg, 320 W, 1.1 m/s, A 0.35, 25 °C) | L × W × D (µm) | Peak T (K) | Cooling at liquidus, median (10⁶ K/s) | "
         "Evaporation (W) |", "|---|---|---|---|---|"]
    for t, lab in (("sens_base_coarse", "base, coarse grid (8/6/5 µm), Marangoni factor 2.5, 30 µm powder"),
                   ("sens_fine", "fine grid (4/3.5/3 µm)"), ("ref_AlSi10Mg_320W_1.1ms_25C", "reference grid (6/5/4 µm)"),
                   ("sens_fM1.0", "no Marangoni enhancement (f_M 1)"), ("sens_fM3.0", "f_M 3"),
                   ("sens_bare", "bare plate, no powder layer"), ("sens_noevap", "no evaporation sink")):
        r = rows.get(t)
        if not r:
            continue
        Lq = r["liquid"]
        L.append(f"| {lab} | {Lq['L'] * 1e6:.0f} × {Lq['W_any'] * 1e6:.0f} × {Lq['D'] * 1e6:.0f} | {r['T_peak']:.0f} | "
                 f"{r['solid']['Tdot_range'][1] / 1e6:.2f} | {r['energy']['evaporation_W']:.1f} |")
    return L


def track_table(J):
    t = J["transient"]
    L = ["| Speed | Track end | Photodiode peak / mid-track | Liquid area peak / mid-track |", "|---|---|---|---|"]
    for key in ("track_end_1p1", "track_end_0p6"):
        d = t[key]
        for lab, c in d["cases"].items():
            L.append(f"| {d['v']} m/s | {lab} | {c['peak_signal_rel']:.2f} | {c['peak_liquid_area_rel']:.2f} |")
    return L


def buildup_table(J):
    L = ["| Part | Layer energy (J) | Scan time (s) | Top after the scan, 15 mm tall (°C) | Top at the next layer's start, 15 mm (°C) |",
         "|---|---|---|---|---|"]
    for k, v in J["transient"]["buildup_summary"].items():
        L.append(f"| {k} | {v['E_layer_J']:.0f} | {v['t_scan_s']:.2f} | {v['after_scan_last']:.0f} | {v['last']:.1f} |")
    return L


def plume_table(J):
    L = ["| Case | Wall reading, HKL (µg/mm) | of which Mg / Zn / Al (µg/mm) | Best: measured Mg/Zn + HKL Al (µg/mm; g per hour lasing) | "
         "Best vapour mol % | Evaporation power (W) | Exit: Mach, velocity (m/s), T (K) | Recoil at the wall (kPa) | "
         "HKL Mg shift per layer (×) | Measured loss (fraction) |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for c in J["plume_source"]["cases"]:
        w = c["readings"]["wall"]
        e = c["exit"]["wall"]
        lpm = w["loss_ug_per_mm"]
        b = c["best"]
        x = ", ".join(f"{k} {100 * v:.0f}" for k, v in b["vapour_mole_fraction"].items() if v > 0.01)
        meas = "; ".join(f"{k} {v['loss_fraction']:.2f}" for k, v in c.get("measured", {}).items()) or "–"
        L.append(f"| {c['tag'].replace('ref_', '').replace('map_', '')} | {lpm['total']:.2f} | {lpm.get('Mg', 0):.2f} / "
                 f"{lpm.get('Zn', 0):.2f} / {lpm.get('Al', 0):.2f} | {b['loss_ug_per_mm']['total']:.2f}; {b['g_per_hour_lasing']:.2f} | "
                 f"{x} | {w['evap_power_W']:.1f} | {e['mach']:.2f}, "
                 f"{e['u_m_s']:.0f}, {e['T_vapour_K']:.0f} | {e['recoil_Pa'] / 1e3:.0f} | "
                 f"{w['shift_per_layer_frac'].get('Mg', float('nan')):.1f} | {meas} |")
    return L


def timescale_table(J):
    L = ["| Case | Spot transit (µs) | Pool transit (µs) | Mushy time, centre (µs) | Pool capillary mode (kHz) | Depression capillary mode (kHz) |",
         "|---|---|---|---|---|---|"]
    for k, v in sorted(J["transient"]["timescales"].items()):
        L.append(f"| {k.replace('ref_', '').replace('map_', '')} | {v['spot_transit_us']:.0f} | {v['pool_transit_us']:.0f} | "
                 f"{v['t_sol_centre_us']:.0f} | {v['f_capillary_pool_kHz']:.1f} | {v['f_capillary_depression_kHz']:.0f} |")
    return L


def main():
    rows, J = load()
    S = ["# Tables for melt-pool.md (generated by report.py; do not edit by hand)", ""]
    for title, tab in (("Properties", props_table()), ("Scaling laws, 96 µm spot", analytic_table(J)),
                       ("Spot options, AlSi10Mg 320 W 1.1 m/s 25 °C", spot_table(J)), ("Power at each Ke at 1.1 m/s, 96 µm", bands_table(J)),
                       ("Validation", validation_table(rows, J)), ("3D model: pools", fv_table(rows, J)),
                       ("3D model: solidification", sol_table(rows)), ("3D model: sensitivity", sens_table(rows)),
                       ("Track ends", track_table(J)), ("Build-up", buildup_table(J)), ("Plume source", plume_table(J)),
                       ("Time scales", timescale_table(J))):
        S += [f"## {title}", ""] + tab + [""]
    (OUT / "tables.md").write_text("\n".join(S) + "\n")
    print((OUT / "tables.md").read_text())


if __name__ == "__main__":
    main()
