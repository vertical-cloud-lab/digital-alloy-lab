#!/usr/bin/env python3
"""Mineral burden B = sum_i w_i * NIR_i / 100 for the benchmarks and the proposed seeds, as a range.

NIR_i is U.S. net import reliance in 2024 from USGS Mineral Commodity Summaries 2025, Figure 2
(doi:10.3133/mcs2025, p. 7). Several entries are bounds (">75", "<50", "<25"), so B is reported as a
[low, high] range. Al is excluded (it is the base of every alloy compared). Fe: "iron and steel" is
listed among commodities <20 % import reliant, and iron ore is a net export, so Fe is taken as 0-20 %.

This is a check on decision D9 (which burden metric), not the campaign paper's script
(al-campaign-paper/scripts/mineral_burden.py on claude/issue-277-20261127-1859), which should stay
the single source for the paper's numbers.

    python tools/mineral_burden_check.py
"""
NIR = {  # element: (low %, high %, MCS 2025 Figure 2 entry)
    "Mg": (75, 100, "MAGNESIUM METAL >75"),
    "Si": (0, 50, "SILICON, metal and ferrosilicon <50"),
    "Mn": (100, 100, "MANGANESE 100"),
    "Cr": (77, 77, "CHROMIUM, all forms 77"),
    "Zr": (0, 25, "ZIRCONIUM, ores and concentrates <25"),
    "Sc": (100, 100, "SCANDIUM 100"),
    "Fe": (0, 20, "iron and steel: listed as <20 %"),
    "Cu": (45, 45, "COPPER, refined 45"),
    "Ni": (48, 48, "NICKEL 48"),
    "Ti": (95, 100, "TITANIUM, sponge metal >95"),
    "Zn": (73, 73, "ZINC, refined 73"),
    "Er": (80, 80, "RARE EARTHS, compounds and metals 80"),
    "Ce": (80, 80, "RARE EARTHS, compounds and metals 80"),
}

# wt%; benchmarks at nominal composition, seeds as proposed in #275 (bofn-seeding/first-six @ 845356a)
ALLOYS = {
    "AlSi10Mg (nominal)": {"Si": 10.0, "Mg": 0.35},
    "Scalmalloy (D2)": {"Mg": 4.6, "Sc": 0.66, "Zr": 0.42, "Mn": 0.49},
    "S1 Al-4.8Mn-0.9Cr-1.1Zr-1.2Mg": {"Mn": 4.8, "Cr": 0.9, "Zr": 1.1, "Mg": 1.2},
    "S2 Al-1.9Fe-1.0Mg-1.0Zr": {"Fe": 1.9, "Mg": 1.0, "Zr": 1.0},
    "S3 Al-3.5Si-2.5Mg": {"Si": 3.5, "Mg": 2.5},
    "S4 Al-6Mg-2.5Si-0.7Ti": {"Mg": 6.0, "Si": 2.5, "Ti": 0.7},
    "O1 Al-3.6Mg-1.2Zr": {"Mg": 3.6, "Zr": 1.2},
    "O3 Al-4.8Mn-0.8Cr": {"Mn": 4.8, "Cr": 0.8},
}


def burden(comp: dict[str, float]) -> tuple[float, float]:
    lo = sum(w * NIR[e][0] / 100 for e, w in comp.items())
    hi = sum(w * NIR[e][1] / 100 for e, w in comp.items())
    return lo, hi


if __name__ == "__main__":
    ref_lo, ref_hi = burden(ALLOYS["Scalmalloy (D2)"])
    print(f"{'alloy':34} {'B low':>6} {'B high':>7}  vs Scalmalloy ({ref_lo:.2f}-{ref_hi:.2f})")
    for name, comp in ALLOYS.items():
        lo, hi = burden(comp)
        verdict = "lower" if hi < ref_lo else ("higher" if lo > ref_hi else "overlaps")
        print(f"{name:34} {lo:6.2f} {hi:7.2f}  {verdict}")
