"""Key tables from the plume study's JSON outputs, as Markdown (monitoring/plume.md quotes them).

Run after plume_jet.py, spatter.py, particles.py and fouling.py:
    /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/plume/summarize.py
Writes analysis/out/monitoring/plume/summary.md.
"""
from __future__ import annotations

import json
import math
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parents[1] / "out" / "monitoring" / "plume"
WIN = ("laser", "LW", "LP", "LC", "BW")
WNAME = {"laser": "laser slide (lid, centre)", "LW": "LW slide (left wall, 13°)", "LP": "LP slide (lid, front-left, 54°)",
         "LC": "layer-camera bore (lid)", "BW": "BW light window (back wall, 8°)"}
SPEEDS = ("Ly 2017 speeds", "slow (speeds / 2)", "Al lognormal (median 2.5 m/s)")


def load(name):
    p = OUT / name
    return json.loads(p.read_text()) if p.exists() else None


def pct(v, nd=1):
    return "–" if v is None else f"{100 * v:.{nd}f} %"


def fmt(v, nd=3):
    if v is None or (isinstance(v, float) and (math.isinf(v) or math.isnan(v))):
        return "–"
    return f"{v:.{nd}g}"


def main():
    P, F, S, J = load("particles.json"), load("fouling.json"), load("spatter.json"), load("plume_jet.json")
    L = ["# Plume study: key numbers", "", "Written by `analysis/monitoring/plume/summarize.py` from the JSON files in this folder.", ""]
    if J:
        L += ["## Vapour plume by hand (plume_jet.py)", "",
              "| Alloy | Scenario | T_s (K) | p_sat (atm) | Regime | Jet speed (m/s) | Metal out (g/h of lasing) | Vapour (mol) | "
              "Plume height 10 mm downstream, 200 / 140 L/min (mm) | Primary particles (nm) |", "|---|---|---|---|---|---|---|---|---|---|"]
        for alloy, r in J["alloys"].items():
            for name, sc in r["scenarios"].items():
                ev = sc["evaporation"]
                jets = list(sc["jet"].values())
                vap = ", ".join(f"{k} {100 * v:.0f} %" for k, v in sorted(ev["vapour_mole_fraction"].items(), key=lambda kv: -kv[1]) if v > 0.01)
                L.append(f"| {alloy} | {name.split(',')[0]} | {ev['T_s']:.0f} | {ev['p_sat_atm']:.2f} | {'jet' if ev['u_jet'] > 0 else 'no jet'} | "
                         f"{ev['u_jet']:.0f} | {sc['mdot_g_per_h_lasing']:.3g} | {vap} | {jets[0]['z_at_10mm']:.1f} / {jets[1]['z_at_10mm']:.1f} | "
                         f"{sc['primary']['d_primary_nm']:.0f} |")
        L += ["", "Alloy boiling points (Raoult, ideal): " + ", ".join(f"{a} {r['T_boil_alloy_K']:.0f} K" for a, r in J["alloys"].items()), ""]
        L += ["| Beam / coaxial attenuation through the plume above the spot | column (mg/m²) | τ at 1.07 µm, 20 nm / 300 nm | τ at 0.85 µm, 20 nm / 300 nm |",
              "|---|---|---|---|"]
        for k, v in J["plume_column_attenuation"].items():
            L.append(f"| {k} | {v['column_kg_m2'] * 1e6:.3g} | {v['tau 1.07 um, 20 nm primaries']:.1e} / {v['tau 1.07 um, 300 nm compact']:.1e} | "
                     f"{v['tau 0.85 um, 20 nm primaries']:.1e} / {v['tau 0.85 um, 300 nm compact']:.1e} |")
        L.append("")
    if P:
        L += ["## Condensate in the CFD (particles.py)", ""]
        for case, r in P.items():
            L += [f"### {case}: {r['q_lpm']:g} + {r['upper_lpm']:g} L/min, LW purge {r['lw_purge_lpm']:g} L/min, {r['cells'] / 1000:.0f}k cells, "
                  f"{r['iterations']:.0f} iterations", "",
                  f"Bed: {r['bed']['z3_d75']['mean']:.2f} m/s mean at 3 mm over Ø75 ({r['bed']['z3_d75']['min']:.2f}–{r['bed']['z3_d75']['max']:.2f}); "
                  f"under the laser slide (z 121): {r['window_z121']['mean_speed']:.2f} m/s, Uy {r['window_z121']['mean_uy']:+.2f}.", "",
                  "| Released | n | Out in 8 s | Out by the end (t_end) | Median time out (s) | Near the beam axis under the lid | " + " | ".join(f"Entered {w} recess" for w in WIN) + " |",
                  "|---|---|---|---|---|---|" + "---|" * len(WIN)]
            for band, c in r["condensate"].items():
                L.append(f"| {band} | {c['n']} | {pct(c.get('out_within_8s', c['outlet']))} | {pct(c['outlet'])} ({c.get('t_end_s', 8):g} s) | "
                         f"{fmt(c['median_time_to_outlet_s'], 2)} | {pct(c['passed_within_30mm_of_window_axis_above_z105'])} | "
                         + " | ".join(pct(c["entered_recess"][w], 2) for w in WIN) + " |")
            L += ["", "Condensate concentration per unit source, C/S (s/m³), next to each window and at other places (in brackets: how many "
                  "tracers visited; the counting noise is ~1/sqrt of it):", "",
                  "| Control volume | " + " | ".join(r["condensate"]) + " |", "|---|" + "---|" * len(r["condensate"])]
            keys = list(next(iter(r["condensate"].values()))["concentration_per_source"])
            for k in keys:
                L.append(f"| {k} | " + " | ".join(fmt(c["concentration_per_source"][k]["C_per_S_s_m3"])
                                                   + (f" ({c['concentration_per_source'][k]['n_visited']})" if "n_visited" in c["concentration_per_source"][k] else "")
                                                   for c in r["condensate"].values()) + " |")
            L += ["", "| Window | u* (m/s) | gas speed 1 mm off the face (m/s) |", "|---|---|---|"]
            pn = {"laser": "slide", "LW": "lwSlide", "LP": "lpSlide", "LC": "lcWindow", "BW": "bwWindow"}
            for w in WIN:
                us = r["u_star"].get(pn[w])
                gs = r["gas_at_windows"].get(w)
                L.append(f"| {WNAME[w]} | {fmt(us['u_star_mean'], 2) if us else '–'} | {fmt(gs['mean_speed'], 2) if gs else '–'} |")
            L.append("")
            if "spatter" in r:
                L += ["Spatter (Al) landing on each window, share of launches:", "",
                      "| Speeds | d (µm) | " + " | ".join(WNAME[w] for w in WIN) + " | plate (Ø75) | floor | outlet | lid | door side | other walls and parts |",
                      "|---|---|" + "---|" * (len(WIN) + 6)]
                for lab in SPEEDS:
                    if lab not in r["spatter"]:
                        continue
                    for d, sp in r["spatter"][lab].items():
                        f = sp["fates"]
                        L.append(f"| {lab} | {d} | " + " | ".join(pct(sp["windows"].get(w, 0.0), 2) for w in WIN)
                                 + f" | {pct(f.get('plate', 0.0))} | {pct(f.get('floor', 0.0))} | {pct(f.get('outlet slot', 0.0))} | {pct(f.get('lid', 0.0))} | "
                                 + f"{pct(f.get('wall: door side')) if 'wall: door side' in f else '–'} | "
                                 + f"{pct(sum(v for k, v in f.items() if ('wall' in k or 'part' in k) and k != 'wall: door side'))} |")
                L.append("")
    if F and F.get("windows"):
        L += ["## Fouling (fouling.py)", "", "Condensate source, g per hour of lasing (from measured Mg / Zn losses x 1.5 for Al): "
              + ", ".join(f"{a} {v['g_per_h_lasing'][0]:.2g}–{v['g_per_h_lasing'][1]:.2g} (nominal {v['nominal']:.2g})" for a, v in F["source"].items()), ""]
        for case, w in F["windows"].items():
            L += [f"### {case}", "", "| Window | Released | Size, ΔT | Alloy | mg/m² per h of lasing | h to the limit, dense Al film | h, porous Al (f 0.1) |",
                  "|---|---|---|---|---|---|---|"]
            for k, v in w["condensate"].items():
                win, band, size, alloy = [s.strip() for s in k.split("|")]
                if v["mg_m2_per_h"] <= 0 or alloy == "6061":
                    continue
                L.append(f"| {win} | {band} | {size} | {alloy} | {fmt(v['mg_m2_per_h'])} | {fmt(v['hours (dense Al film)'])} | {fmt(v['hours (porous Al, f 0.1)'])} |")
            L += ["", "| Window, speeds | Spatter hits per hour of lasing at 100 spatters/s | splat area (mm²/h) |", "|---|---|---|"]
            for k, v in w["spatter"].items():
                L.append(f"| {k} | {v['hits_per_h_at_100_per_s']:.0f} | {v['splat_mm2_per_h']:.1f} |")
            L.append("")
    if S:
        L += ["## Spatter glow and blur (spatter.py)", "", "| Spatter | Camera, exposure | visible above (K) | glows for (ms) | over (mm) |", "|---|---|---|---|---|"]
        for k, row in S["glow"].items():
            if "2200" not in k:
                continue
            for cam, g in row.items():
                if isinstance(g, dict):
                    L.append(f"| {k} | {cam} | {fmt(g['T_visible_K'], 4)} | {g['glow_ms']:.1f} | {g['glow_path_mm']:.0f} |")
        L.append("")
    if P and F and F.get("windows"):
        L += doc_tables(P, F)
    (OUT / "summary.md").write_text("\n".join(L) + "\n")
    print("wrote", OUT / "summary.md")


def doc_tables(P, F):
    """The compact tables monitoring/plume.md quotes, one block per case."""
    L = ["## Compact tables (as quoted in monitoring/plume.md)", ""]
    pn = {"laser": "slide", "LW": "lwSlide", "LP": "lpSlide", "LC": "lcWindow", "BW": "bwWindow"}
    for case, r in P.items():
        c1, c2 = r["condensate"]["0.5-5 mm"], r["condensate"]["5-20 mm"]
        L += [f"### {case}", "", "| Released | Out in 8 s | Out in 20 s | Median time out | Near the beam axis under the lid | laser | LW | LP | LC | BW |",
              "|---|---|---|---|---|---|---|---|---|---|"]
        for band, c in (("0.5–5 mm", c1), ("5–20 mm", c2)):
            L.append(f"| {band} | {pct(c.get('out_within_8s', c['outlet']))} | {pct(c['outlet'])} | {fmt(c['median_time_to_outlet_s'], 2)} s | "
                     f"{pct(c['passed_within_30mm_of_window_axis_above_z105'])} | " + " | ".join(pct(c["entered_recess"][w], 2) for w in WIN) + " |")
        L += ["", "| Where | 0.5–5 mm | 5–20 mm |", "|---|---|---|"]
        for k in c1["concentration_per_source"]:
            a, b = c1["concentration_per_source"][k], c2["concentration_per_source"][k]
            L.append(f"| {k} | {fmt(a['C_per_S_s_m3'], 2)} ({a.get('n_visited', '?')}) | {fmt(b['C_per_S_s_m3'], 2)} ({b.get('n_visited', '?')}) |")
        L += ["", "| Window | u* | gas 1 mm off | J/S 0.1 um dT0, low / high (mg/m2/h per g/h) |", "|---|---|---|---|"]
        for w in WIN:
            d1 = r["deposition_per_source"]["0.5-5 mm"][w]["0.1 um, dT 0 K"]["J_per_S"]
            d2 = r["deposition_per_source"]["5-20 mm"][w]["0.1 um, dT 0 K"]["J_per_S"]
            us = r["u_star"].get(pn[w])
            gs = r["gas_at_windows"].get(w)
            L.append(f"| {w} | {fmt(us['u_star_mean'], 2) if us else '-'} | {fmt(gs['mean_speed'], 2) if gs else '-'} | {d1 * 1e3:.2g} / {d2 * 1e3:.2g} |")
        fw = F["windows"].get(case)
        if fw:
            L += ["", "| Window | v_d 0.1 um | mg/m2/h low / high (AlSi10Mg) | 10 K colder | h porous (dense), high | 10 K colder |", "|---|---|---|---|---|---|"]
            for w in WIN:
                g = lambda band, size: fw["condensate"].get(f"{w} | {band} | {size} | AlSi10Mg")
                lo0, hi0, lo10, hi10 = g("0.5-5 mm", "0.1 um, dT 0 K"), g("5-20 mm", "0.1 um, dT 0 K"), g("0.5-5 mm", "0.1 um, dT 10 K"), g("5-20 mm", "0.1 um, dT 10 K")
                vd = r["deposition_per_source"]["5-20 mm"][w]["0.1 um, dT 0 K"]["v_d"]
                L.append(f"| {w} | {vd:.2g} | {fmt(lo0['mg_m2_per_h'], 2)} / {fmt(hi0['mg_m2_per_h'], 2)} | {fmt(lo10['mg_m2_per_h'], 2)} / {fmt(hi10['mg_m2_per_h'], 2)} | "
                         f"{fmt(hi0['hours (porous Al, f 0.1)'], 2)} ({fmt(hi0['hours (dense Al film)'], 2)}) | {fmt(hi10['hours (porous Al, f 0.1)'], 2)} ({fmt(hi10['hours (dense Al film)'], 2)}) |")
            L += ["", "| Window | Al-like hits/h, mm2/h | Ly hits/h, mm2/h |", "|---|---|---|"]
            for w in WIN:
                a = fw["spatter"].get(f"{w} | Al lognormal (median 2.5 m/s)", {})
                b = fw["spatter"].get(f"{w} | Ly 2017 speeds", {})
                L.append(f"| {w} | {a.get('hits_per_h_at_100_per_s', 0):.0f} / {a.get('splat_mm2_per_h', 0):.1f} | {b.get('hits_per_h_at_100_per_s', 0):.0f} / {b.get('splat_mm2_per_h', 0):.1f} |")
        if "spatter" in r:
            L += ["", "| Speeds | d | laser | LW | LP | plate | floor | outlet | lid | door side |", "|---|---|---|---|---|---|---|---|---|---|"]
            for lab in SPEEDS:
                for d, sp in r["spatter"].get(lab, {}).items():
                    f = sp["fates"]
                    L.append(f"| {lab} | {d} | " + " | ".join(pct(sp["windows"].get(w, 0.0), 2) for w in ("laser", "LW", "LP"))
                             + f" | {pct(f.get('plate', 0.0))} | {pct(f.get('floor', 0.0))} | {pct(f.get('outlet slot', 0.0))} | {pct(f.get('lid', 0.0))} | {pct(f.get('wall: door side', 0.0))} |")
        L.append("")
    return L


if __name__ == "__main__":
    main()
