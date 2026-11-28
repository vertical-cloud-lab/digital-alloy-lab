"""How the eagar-tsai boiling-line numbers move with NIST-JANAF's boiling point of Al (#235).

The eagar-tsai comparisons (``arroyave-orchid-tools/eagar-tsai/``) and Xavier's Sobol sweep
(``edison-trajectories/eagar-tsai-alsi10mg-inputs/sobol-check/``) used 2743 K for aluminium's boiling
point. The later first-principles keyhole work in #249 traced that value to Alcock et al. 1984's
vapour-pressure equation, extrapolated far beyond its 1,800 K range. NIST-JANAF (table Al-001) gives
2,790.8 K, and the CRC Handbook agrees (2,791 K). With Raoult's law on Al alone, #249 also gives the
alloys' 1 atm boiling points: 2,814 K for AlSi10Mg and 2,852 K for the blend.

The boiling line only enters as a heuristic: eagar-tsai's peak temperature reaching T_b. This script
recounts every committed number that uses it, at each T_b, straight from the committed CSVs. It
doesn't re-run eagar-tsai, and it doesn't rewrite those CSVs: #249's keyhole scorer
(``scripts/keyhole_open_models.py``) reads their ``et_boiling`` column, and its committed outputs
should stay reproducible. At 2743 K the script must reproduce the committed numbers, and it asserts
that it does.

eagar-tsai's temperature rise is linear in the absorbed power A*P, so a boiling line drawn in power
moves by exactly (T_b' - T_plate) / (T_b - T_plate).

    # writes boiling-point-check.csv in about 2 s; needs eagar-tsai installed (for its defect classifier)
    python scripts/eagar_tsai_boiling_point_check.py --out arroyave-orchid-tools/eagar-tsai
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np
import pandas as pd

REPO = pathlib.Path(__file__).resolve().parents[1]
ET = REPO / "arroyave-orchid-tools" / "eagar-tsai"
AM = ET / "am-module-inhouse"
SOBOL = REPO / "edison-trajectories" / "eagar-tsai-alsi10mg-inputs" / "sobol-check"
sys.path.insert(0, str(REPO / "scripts"))
from eagar_tsai_vs_am_module_inhouse import MELT_POOLS  # noqa: E402  (the render points' speeds)

T_B_USED = 2743.0  # what the committed files used
T_B_JANAF = 2790.8  # NIST-JANAF Al-001, pure Al at 1 atm
T_B_ALLOY = {"alsi10mg": 2814.0, "byu-blend": 2852.0}  # #249, Raoult on x_Al at 1 atm

# The in-house AM-module maps: plate temperatures as in eagar_tsai_vs_am_module_inhouse.MAPS
MAP_RUNS = [  # (slug, pool-edge variant, plate K)
    ("alsi10mg", "liquidus-867K", 423.15),
    ("byu-blend", "eutectic-850K", 303.15),
    ("byu-blend", "liquidus-1019K", 303.15),
]


def tb_set(slug: str) -> dict[str, float]:
    return {"2743 K (used)": T_B_USED, "2791 K (NIST-JANAF, pure Al)": T_B_JANAF,
            "alloy at 1 atm (#249): AlSi10Mg 2814 K, blend 2852 K": T_B_ALLOY[slug]}


def maps(rows: list) -> None:
    summary = json.loads((AM / "summary.json").read_text())
    for slug, variant, T_plate in MAP_RUNS:
        A = summary[slug]["A_inferred"]
        g = pd.read_csv(AM / f"{slug}-eagar-tsai-grid-{variant}.csv")
        g = g[np.isclose(g["A"], A, atol=5e-5) & (g["am_class"] != "hidden")]
        b = pd.read_csv(AM / f"{slug}-eagar-tsai-boundary-absorptivity-{variant}.csv").dropna(subset=["P_am_keyhole_W"])
        am_kh = g["am_class"] == "keyhole"
        committed = next(v for v in summary[slug]["variants"].values() if v["slug"] == variant)["at_A_inferred"]
        for label, T_b in tb_set(slug).items():
            boil = g["T_peak_K"] >= T_b
            share = b["Q_boiling_W"] * (T_b - T_plate) / (T_B_USED - T_plate) / (A * b["P_am_keyhole_W"])
            res = {
                "visible grid points": len(g),
                "points where eagar-tsai's peak reaches T_b": int(boil.sum()),
                "... of which the AM module calls keyhole": int((boil & am_kh).sum()),
                "keyhole-or-not agreement with the AM map, calling keyhole where the peak reaches T_b": int((boil == am_kh).sum()),
                "boiling line ÷ the AM module's keyhole power, min (%)": round(100 * share.min(), 1),
                "boiling line ÷ the AM module's keyhole power, max (%)": round(100 * share.max(), 1),
            }
            if T_b == T_B_USED:  # must reproduce what is committed
                assert res["points where eagar-tsai's peak reaches T_b"] == committed["et_boiling"], (slug, variant)
                assert res["... of which the AM module calls keyhole"] == committed["et_boiling_and_am_keyhole"]
                assert (boil == g["et_boiling"].astype(bool)).all()
            for k, v in res.items():
                rows.append(dict(part="AM-module maps", case=f"{slug}, pool edge {variant}, A = {A:.3f}",
                                 quantity=k, T_b=label, value=v))


def transient(rows: list) -> None:
    d = pd.read_csv(AM / "transient" / "eagar-tsai-transient-history.csv")
    s = json.loads((AM / "transient" / "eagar-tsai-transient-history-summary.json").read_text())
    for case in ("alsi10mg", "byu-blend"):
        h = d[d["case"] == case].sort_values("tau_us")
        on, off = h[h["beam_on"]], h[~h["beam_on"]]
        t_off = s[case]["track_mm"] / MELT_POOLS[case]["v_mm_s"] * 1e6  # unrounded switch-off time, us
        for label, T_b in tb_set(case).items():
            i = int(np.argmax(on["peak_K"].to_numpy() >= T_b))
            hi = on["tau_us"].iloc[i]
            lo = on["tau_us"].iloc[i - 1] if i > 0 else 0.0
            j = int(np.argmax(off["peak_K"].to_numpy() < T_b))
            off_hi = off["tau_us"].iloc[j] - t_off
            off_lo = off["tau_us"].iloc[j - 1] - t_off if j > 0 else 0.0
            if T_b == T_B_USED:
                assert round(off_hi, 1) == s[case]["peak_below_boiling_us_after_off"], case
            rows.append(dict(part="transient (one track)", case=case,
                             quantity="surface first reaches T_b after switch-on, between samples (µs)",
                             T_b=label, value=f"{lo:.1f}–{hi:.1f}"))
            rows.append(dict(part="transient (one track)", case=case,
                             quantity="peak falls below T_b after switch-off, between samples (µs)",
                             T_b=label, value=f"{off_lo:.1f}–{off_hi:.1f}"))


def sobol(rows: list) -> None:
    import eagar_tsai_sobol_analysis as sa  # its regime() reads the module-level T_BOIL_AL_K

    first = pd.read_csv(SOBOL / "first-1024-rows-2um.csv")
    full = pd.read_csv(SOBOL / "sobol-m12-4096-rows-2um.csv")
    defect = sa.defect_class(full)
    T_liq, T_amb = 867.0, 298.0
    for label, T_b in tb_set("alsi10mg").items():
        sa.T_BOIL_AL_K = T_b
        melt1 = first["melt_width_um"] > 0
        reg = sa.regime(full)
        res = {
            "first 1,024 rows: melting rows": int(melt1.sum()),
            "first 1,024 rows: melting rows whose peak is above T_b": int((melt1 & (first["peak_temperature"] > T_b)).sum()),
            "4,096 rows: melt, peak below T_b": int((reg == "conduction").sum()),
            "4,096 rows: melt, peak above T_b": int((reg == "above_boiling").sum()),
            "4,096 rows: defect-free and peak below T_b": int(((defect == "defect_free") & (reg == "conduction")).sum()),
            "4,096 rows: 'defect-free' with the surface above T_b": int(((defect == "defect_free") & (reg == "above_boiling")).sum()),
            "4,096 rows: eagar-tsai 'keyhole' rows": int((defect == "keyhole").sum()),
            "4,096 rows: ... of which the peak is above T_b": int(((defect == "keyhole") & (reg == "above_boiling")).sum()),
            "boiling threshold on Θ·G(p), (T_b − 298) / (867 − 298)": round((T_b - T_amb) / (T_liq - T_amb), 2),
        }
        if T_b == T_B_USED:  # the numbers in the sweep's README
            assert res["first 1,024 rows: melting rows whose peak is above T_b"] == 281
            assert res["4,096 rows: melt, peak below T_b"] == 1963 and res["4,096 rows: melt, peak above T_b"] == 1097
            assert res["4,096 rows: defect-free and peak below T_b"] == 697
            assert res["4,096 rows: ... of which the peak is above T_b"] == 842
        for k, v in res.items():
            rows.append(dict(part="Sobol sweep (AlSi10Mg box)", case="Xavier's design, 2 µm grid", quantity=k,
                             T_b=label, value=v))
    sa.T_BOIL_AL_K = T_B_USED


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=pathlib.Path, required=True)
    a = ap.parse_args()
    rows: list = []
    maps(rows)
    transient(rows)
    sobol(rows)
    df = pd.DataFrame(rows)
    wide = df.pivot_table(index=["part", "case", "quantity"], columns="T_b", values="value", aggfunc="first",
                          sort=False).reset_index()
    a.out.mkdir(parents=True, exist_ok=True)
    wide.to_csv(a.out / "boiling-point-check.csv", index=False)
    with pd.option_context("display.width", 250, "display.max_colwidth", 90, "display.max_rows", 200):
        print(wide.to_string(index=False))


if __name__ == "__main__":
    main()
