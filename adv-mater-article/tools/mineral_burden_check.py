#!/usr/bin/env python3
"""Mineral burden B = sum_i w_i * NIR_i / 100 for the baselines and the proposed seeds, as a range.

NIR_i is U.S. net import reliance. Several USGS entries are bounds (">75", "<25"), so B is reported as a
[low, high] range. Al is excluded (it is the base of every alloy compared).

Two editions:
  2026 (default)  the campaign paper's inputs: al-campaign-paper/data/element-criticality.csv on
                  claude/issue-277-20261127-1859 @ b4cf060 (USGS Mineral Commodity Summaries 2026; Fe counted
                  as zero, as the campaign paper does). Use this one, so both papers report the same B.
  2025            MCS 2025, Figure 2 (doi:10.3133/mcs2025, p. 7), the edition the first draft of this
                  check used; Fe taken as 0-20 %.

This is a check for decision D9 (which burden metric) and for the draft Fig. 5c. The campaign paper's script
(al-campaign-paper/scripts/mineral_burden.py) stays the single source of the numbers both papers publish.

    python tools/mineral_burden_check.py [--edition 2025|2026]
"""
from __future__ import annotations

import argparse

NIR_EDITIONS = {
    "2026": {  # element: (low %, high %), from the campaign paper's element-criticality.csv @ b4cf060
        "Mg": (75, 100), "Si": (50, 100), "Mn": (100, 100), "Cr": (79, 79), "Zr": (0, 25),
        "Sc": (100, 100), "Fe": (0, 0), "Cu": (57, 57), "Ni": (41, 41), "Ti": (100, 100),
        "Zn": (73, 73), "Er": (100, 100), "Ce": (67, 67), "Ag": (77, 77), "V": (41, 41), "B": (0, 0),
    },
    "2025": {  # MCS 2025 Figure 2
        "Mg": (75, 100), "Si": (0, 50), "Mn": (100, 100), "Cr": (77, 77), "Zr": (0, 25),
        "Sc": (100, 100), "Fe": (0, 20), "Cu": (45, 45), "Ni": (48, 48), "Ti": (95, 100),
        "Zn": (73, 73), "Er": (80, 80), "Ce": (80, 80),
    },
}
NIR = NIR_EDITIONS["2026"]

# wt %. Benchmarks and baselines at nominal composition, using the campaign paper's alloys.csv and
# literature-alloys.csv @ b4cf060 so that both papers use the same numbers:
#   AlSi10Mg     midpoints of the EN AC-43000 / EOS ranges (Si 9-11, Mg 0.20-0.45)
#   Scalmalloy   midpoints of the Nikon SLM sheet's ranges (Mg 4.50-4.90, Sc 0.68-0.84, Mn 0.2-0.7, Zr 0.2-0.4)
#   Al5X1        midpoints of EOS's material data sheet ranges (Mg 2.5-4.2, Zr 0.6-1.8, Mn 0.1-1.0); Fe, Si
#                and Ti (each 0-1 wt %) left out, as for the other alloys' impurity limits
#   Al-HS1       Hoganas data sheet 3312HOG-3, typical values
#   Aheadd CP1   midpoints of EOS's ranges (Fe 0.8-1.2, Zr 0.9-1.35); context, not a baseline
# Seeds as melted on the 6063 base (#275, bofn-seeding/first-six), from the same alloys.csv.
ALLOYS = {
    "AlSi10Mg (nominal)": {"Si": 10.0, "Mg": 0.325},
    "Scalmalloy (nominal)": {"Mg": 4.70, "Sc": 0.76, "Zr": 0.30, "Mn": 0.45},
    "Al5X1 (EOS, nominal)": {"Mg": 3.35, "Zr": 1.2, "Mn": 0.55},
    "Al-HS1 (Hoganas, typical)": {"Mn": 4.8, "Cr": 0.8, "Zr": 0.8},
    "Aheadd CP1 (nominal)": {"Fe": 1.0, "Zr": 1.125},
    "S1 Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg": {"Si": 0.33, "Mg": 1.2, "Mn": 4.8, "Cr": 0.9, "Zr": 1.1, "Fe": 0.17},
    "S2 Al-1.9Fe-1.0Mg-1.0Zr": {"Si": 0.35, "Mg": 1.02, "Zr": 1.03, "Fe": 1.87},
    "S3 Al-3.5Si-2.5Mg": {"Si": 3.5, "Mg": 2.5, "Fe": 0.22},
    "S4 Al-6Mg-2.5Si-0.7Ti": {"Si": 2.5, "Mg": 6.0, "Ti": 0.7, "Fe": 0.21},
    "O1 Al-3.6Mg-1.2Zr": {"Si": 0.34, "Mg": 3.6, "Zr": 1.2, "Fe": 0.17},
    "O3 Al-4.8Mn-0.8Cr": {"Si": 0.38, "Mg": 0.52, "Mn": 4.8, "Cr": 0.8, "Fe": 0.19},
}


def burden(comp: dict[str, float], nir: dict[str, tuple[float, float]] | None = None) -> tuple[float, float]:
    nir = nir or NIR
    lo = sum(w * nir[e][0] / 100 for e, w in comp.items())
    hi = sum(w * nir[e][1] / 100 for e, w in comp.items())
    return lo, hi


def paired_lower(a: dict[str, float], b: dict[str, float], nir: dict[str, tuple[float, float]] | None = None) -> bool:
    """True if B(a) < B(b) for every import-reliance vector inside the USGS bounds (both alloys share them)."""
    nir = nir or NIR
    worst = 0.0
    for e in set(a) | set(b):
        d = a.get(e, 0.0) - b.get(e, 0.0)
        worst += max(d * nir[e][0], d * nir[e][1]) / 100
    return worst < 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--edition", choices=sorted(NIR_EDITIONS), default="2026")
    args = ap.parse_args()
    nir = NIR_EDITIONS[args.edition]
    ref = ALLOYS["Scalmalloy (nominal)"]
    ref_lo, ref_hi = burden(ref, nir)
    base = ALLOYS["Al5X1 (EOS, nominal)"]
    print(f"MCS {args.edition}")
    print(f"{'alloy':34} {'B low':>6} {'B high':>7}  vs Scalmalloy ({ref_lo:.2f}-{ref_hi:.2f})  paired vs Al5X1")
    for name, comp in ALLOYS.items():
        lo, hi = burden(comp, nir)
        verdict = "lower" if hi < ref_lo else ("higher" if lo > ref_hi else "overlaps")
        if comp is base:
            vs5x1 = "-"
        elif paired_lower(comp, base, nir):
            vs5x1 = "lower"
        elif paired_lower(base, comp, nir):
            vs5x1 = "higher"
        else:
            vs5x1 = "depends on NIR"
        print(f"{name:34} {lo:6.2f} {hi:7.2f}  {verdict:8}  {vs5x1}")
