#!/usr/bin/env python3
"""Fill the tables in README.md from the result files, between `<!-- TABLE:name -->` and `<!-- /TABLE -->`.

    python bofn-seeding/first-six/make_tables.py

Keeping the numbers in the README generated means they cannot drift from the CSV files beside it.
"""
from __future__ import annotations

import csv
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
RES = HERE / "results"


def rows(path):
    return list(csv.DictReader(open(path))) if path.exists() else []


def md(header, body):
    out = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in body]
    return "\n".join(out)


def f(x, nd=0):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "–"
    if v != v:
        return "–"
    return f"{v:.{nd}f}"


LABEL = {"D1": "Al–10Si–0.35Mg", "D2": "Al–4.6Mg–0.66Sc–0.42Zr–0.49Mn", "S1": "Al–4.8Mn–0.9Cr–1.1Zr–1.2Mg",
         "S2": "Al–1.9Fe–1.0Mg–1.0Zr", "S3": "Al–3.5Si–2.5Mg", "S4": "Al–6Mg–2.5Si–0.7Ti", "O1": "Al–3.6Mg–1.2Zr",
         "O2": "Al–6.4Mg–0.7Mn–0.4Er–1.1Zr", "O3": "Al–4.8Mn–0.8Cr"}
CAL = {"D1": "D1", "D2": "D2", "S1": "S1", "S2": "S2", "S3": "S3", "S4": "S4", "O1": "O1", "O2": "O2-noEr", "O3": "O3"}
PHASE = {"FCC_A1": "α-Al", "AL3ZR1": "Al₃Zr", "AL3ZR": "Al₃Zr", "AL3SC": "Al₃Sc", "AL4CR": "Al₄(Cr,Mn)", "AL3TI_L": "Al₃Ti",
         "AL3TI_H": "Al₃Ti", "AL3M_DO22": "Al₃Ti", "AL13FE4": "Al₁₃Fe₄", "AL6MN": "Al₆Mn", "ALSIZR_T1": "Al–Si–Zr τ1",
         "AL11MN4": "Al₁₁Mn₄", "AL4MN": "Al₄Mn", "AL13CR2": "Al₇Cr", "AL7CR": "Al₇Cr", "AL11CR2": "Al₁₁Cr₂", "AL8MN5": "Al₈Mn₅"}


def ph(x):
    return PHASE.get(x, x or "–")


def t_recipes():
    s = rows(HERE / "seeds.csv")
    return md(["Seed", "Weigh for a 250 g charge on 6063", "Melt composition this gives (wt%)"],
              [[r["id"], r["charge_250g"], r["melt_wt_on_6063"]] for r in s])


def t_atomization():
    a = {r["seed"]: r for r in rows(RES / "process" / "atomization.csv")}
    s = rows(HERE / "seeds.csv")
    body = []
    for r in s:
        x = a.get(r["id"], {})
        top = f"{f(x.get('highest_liquidus_C'))} ({ph(x.get('highest_liquidus_phase'))})"
        if x.get("setpoint_note"):
            top = f"{f(x.get('liquidus_matcalc_C'))} or {f(x.get('liquidus_cost507_C'))}: the databases disagree"
        body.append([r["id"], top, f(x.get("alpha_start_C")),
                     f"**{f(x.get('melt_setpoint_C'))}**", r["hold_min"], f(x.get("lang_d50_um")),
                     f"{100 * float(x.get('frac_20_63', 'nan')):.0f} %" if x else "–", x.get("flight_loss_60um", "–"),
                     x.get("cool_rate_60um_K_s", "–")])
    return md(["Seed", "Highest liquidus, °C (first solid)", "α-Al starts, °C", "Melt setpoint, °C", "Hold, min",
               "Lang D50, µm", "Mass below 63 µm", "Loss in flight (60 µm drop)", "Cooling rate, K/s"], body)


def t_lpbf():
    w = [r for r in rows(RES / "process" / "lpbf_window.csv") if r["layer_um"] == "50"]
    return md(["Seed", "Published set it starts from", "Model depth of that set, µm", "MIDI start: W / mm·s⁻¹ / hatch µm / layer µm",
               "Plate, °C", "Energy density, J/mm³", "Model pool: width / depth, µm", "Direct age"],
              [[r["seed"], r["ref"], r["ref_pool_d_um"], f"{r['midi_P_W']} / {r['midi_v_mm_s']} / {r['midi_hatch_um']} / 50",
                r["plate_C"], r["ved_J_mm3"], f"{r['pool_w_um']} / {r['pool_d_um']}", r["direct_age"]] for r in w])


def t_calphad():
    c = {(r["id"], r["base"]): r for r in rows(RES / "calphad" / "named.csv")}
    body = []
    for sid, cid in CAL.items():
        for base, nm in (("pureAl", "high-purity Al"), ("6063", "6063")):
            r = c.get((cid, base))
            if not r:
                continue
            note = "stopped early" if r.get("flag") else ("Er left out" if sid == "O2" else "")
            body.append([sid, nm, r["composition_wt"], f(r["T_fcc_start_C"]), f(r["T_end_C"]), f(r["dT_90_99_K"]), f(r["kou_index_K"]),
                         f"{100 * float(r['fs_at_fcc_start']):.1f} %", note])
    return md(["Seed", "Base", "Melt composition (wt%)", "α-Al starts, °C", "Freezing ends, °C", "Range for the last 10 %, K",
               "Kou index, K", "Solid before α-Al", "Note"], body)


def t_validation():
    c = {(r["id"], r["base"]): r for r in rows(RES / "calphad" / "named.csv")}
    groups = [("Cracks in published builds", ["7075", "6061", "2024", "Mg3", "Mg6", "ChalmersE-cracked", "MnMgZr-Yu"]),
              ("Prints crack-free with no grain refiner", ["D1", "A357", "S3", "AlMg9.6Si4.9", "O3", "S1-noMg", "Fe2.5", "Fe2.5Mn2"]),
              ("Prints crack-free with Zr, Sc or Ti", ["D2", "S1", "O1", "S2", "CP1", "Mair", "5083-0.7Zr", "6061-1Zr", "S4"])]
    body = []
    for g, ids in groups:
        for i in ids:
            r = c.get((i, "pureAl"))
            if r:
                body.append([g, r["composition_wt"], f(r["dT_90_99_K"]), f(r["kou_index_K"]), f(r["csc"], 2)])
    return md(["What experiments found", "Alloy (wt%)", "Range for the last 10 %, K", "Kou index, K", "CSC"], body)


def t_saasbo():
    s = rows(RES / "saasbo_handoff" / "summary.csv")
    fin = [r for r in s if r.get("seedset", "draft") == "final" and r["model"] == "saasbo"]
    use = "final" if len(fin) >= 4 and min(int(r["n"]) for r in fin) >= 12 else "draft"
    s = [r for r in s if r.get("seedset", "draft") == use]
    third = "six + O1, O2, O3, then the optimizer" if use == "final" else "six + 3 hand-picked (Zn-Cu, Er and Ni-Ti alloys), then the optimizer"
    name = {"six": "six seeds, then the optimizer", "six+3sobol": "six + 3 Sobol, then the optimizer",
            "six+3axis": third, "nine-sobol": "nine Sobol, then the optimizer"}
    model = {"saasbo": "SAASBO", "gp": "standard GP", "random": "random picks"}
    body = []
    rank = {"six": 0, "six+3sobol": 1, "six+3axis": 2, "nine-sobol": 3}
    for m in ("saasbo", "gp", "random"):
        for r in sorted(s, key=lambda r: rank.get(r["strategy"], 9)):
            if r["model"] != m or r["delay"] != "1":
                continue
            diff = "–" if r["strategy"] == "six" else f"{float(r['paired_diff_vs_six']):+.0f} ± {float(r['paired_diff_se']):.0f}"
            body.append([model[m], "six seeds, then random" if m == "random" else name[r["strategy"]], r["n"],
                         f"{float(r['best']):.0f} ± {float(r['best_se']):.0f}", diff, f(r["regret"]),
                         f"{float(r['bo_new_element_runs']):.1f} of {float(r['n_bo']):.0f}",
                         f"{100 * float(r['found_hidden_pair']):.0f} %"])
    note = ("Seed set: the six and the optional three exactly as proposed above." if use == "final" else
            "Seed set: a draft of the six (S1 without Mg at 0.6 Zr, and O1 in place of S4). The rerun with the final six is in "
            "`results/saasbo_handoff/`.")
    return note + "\n\n" + md(["Model", "Start", "Instances", "Best of 25, MPa (± s.e.)", "Paired difference from six seeds", "Regret, MPa",
                               "Optimizer runs with an element no seed has", "Found the hidden pair"], body)


def t_liquidus():
    q = rows(RES / "calphad" / "liquidus_vs_content.csv")
    by = {}
    for r in q:
        if r["liquidus_cost507_C"] in ("", "None"):
            continue
        by.setdefault(r["grid"], []).append((r["composition_wt"], float(r["liquidus_cost507_C"]), ph(r["primary_phase_cost507"])))
    names = {"liq-Zr": "Zr", "liq-Zr-Mg4.5": "Zr, with 4.5 Mg", "liq-Ti": "Ti", "liq-Cr": "Cr", "liq-Mn": "Mn", "liq-Fe": "Fe",
             "liq-MnCr": "Cr, with 4.8 Mn"}
    body = []
    for g, label in names.items():
        if g in by:
            pts = by[g]
            body.append([label, "; ".join(f"{c.replace('-', '–')}: {t:.0f}" for c, t, _ in pts), pts[-1][2]])
    return md(["Addition", "Liquidus, °C, by content (wt%)", "First solid"], body)


TABLES = dict(recipes=t_recipes, atomization=t_atomization, lpbf=t_lpbf, calphad=t_calphad, validation=t_validation,
              saasbo=t_saasbo, liquidus=t_liquidus)


def main():
    p = HERE / "README.md"
    s = p.read_text()
    for name, fn in TABLES.items():
        pat = re.compile(r"(<!-- TABLE:%s -->\n).*?(<!-- /TABLE -->)" % re.escape(name), re.S)
        if not pat.search(s):
            print("no marker for", name)
            continue
        try:
            table = fn()
        except Exception as e:  # noqa: BLE001
            print(name, "failed:", type(e).__name__, e)
            continue
        s = pat.sub(lambda m: m.group(1) + table + "\n" + m.group(2), s)
        print("filled", name, table.count("\n") - 1, "rows")
    p.write_text(s)


if __name__ == "__main__":
    main()
