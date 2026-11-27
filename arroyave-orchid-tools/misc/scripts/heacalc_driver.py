"""Run HEACalculator (Python API) on a few compositions and re-derive the core parameters by
hand from the package's own element/pair tables for the Cu-Ni and Al-Si-Mg cases.

Usage: python -I heacalc_driver.py <out_dir>
"""
import json
import math
import sys
from importlib import resources
from pathlib import Path

import pandas as pd
from HEACalculator import HEACalculator

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)

ALLOYS = {
    "Cantor CoCrFeMnNi (reference HEA)": "CoCrFeMnNi",
    "FeCoCrNi (README example)": "FeCoCrNi",
    "AlCoCrFeNi (Al-containing HEA)": "AlCoCrFeNi",
    "Al-10Si-0.35Mg at.% (AlSi10Mg-like, Al-rich)": "Al89.65Si10Mg0.35",
    "Cu-30Ni at.% (cupronickel)": "Cu70Ni30",
    "Cu-50Ni at.%": "Cu50Ni50",
    "Cu-0.8Cr-0.1Zr at.% (CuCrZr-like)": "Cu99.1Cr0.8Zr0.1",
}
KEYS = ["delta", "delta_chi_pauling", "vec", "mixing_enthalpy", "mixing_entropy", "melting_temperature",
        "omega", "gamma", "lambda", "phi", "density", "microstructure"] + [f"model_{i}" for i in range(1, 9)]
rows = []
for label, f in ALLOYS.items():
    try:
        d = HEACalculator(f).get_dict()
        rows.append({"alloy": label, "formula": f} | {k: d.get(k) for k in KEYS})
    except Exception as e:  # record, don't stop
        rows.append({"alloy": label, "formula": f, "error": f"{type(e).__name__}: {e}"})
df = pd.DataFrame(rows)
pd.set_option("display.width", 250, "display.max_columns", 40)
print(df.drop(columns=[c for c in df.columns if c.startswith("model_")]).to_string(index=False))
print()
print(df[["formula"] + [c for c in df.columns if c.startswith("model_")]].to_string(index=False))
df.to_csv(out / "heacalculator_compositions.csv", index=False)

# ---- hand check: textbook formulas, numbers taken from the package's own JSON tables ----
data = resources.files("HEACalculator") / "data"
EL = json.loads((data / "elements.json").read_text())
MIX = json.loads((data / "mixing_enthalpy.json").read_text())
R = 8.314462618


def hmix_pair(a, b):
    return MIX.get(f"{a}-{b}", MIX.get(f"{b}-{a}"))


def hand(comp):
    tot = sum(comp.values())
    c = {k: v / tot for k, v in comp.items()}
    els = list(c)
    smix = -R * sum(x * math.log(x) for x in c.values())
    hmix = sum(4 * hmix_pair(a, b) * c[a] * c[b] for i, a in enumerate(els) for b in els[i + 1:])
    rbar = sum(c[e] * EL[e]["atomic_radius"] for e in els)
    delta = 100 * math.sqrt(sum(c[e] * (1 - EL[e]["atomic_radius"] / rbar) ** 2 for e in els))
    vec = sum(c[e] * EL[e]["nvalence"] for e in els)
    tm = sum(c[e] * EL[e]["melting_point"] for e in els)
    omega = tm * smix / abs(hmix * 1000) if hmix else float("inf")
    return {"mixing_entropy": smix, "mixing_enthalpy": hmix, "delta": delta, "vec": vec,
            "melting_temperature": tm, "omega": omega,
            "pairs_kJ/mol": {f"{a}-{b}": hmix_pair(a, b) for i, a in enumerate(els) for b in els[i + 1:]},
            "radii_pm": {e: EL[e]["atomic_radius"] for e in els}}


checks = {}
for f, comp in (("Cu70Ni30", {"Cu": 70, "Ni": 30}), ("Al89.65Si10Mg0.35", {"Al": 89.65, "Si": 10, "Mg": 0.35})):
    h = hand(comp)
    d = HEACalculator(f).get_dict()
    checks[f] = {"hand": h, "package": {k: d[k] for k in ("mixing_entropy", "mixing_enthalpy", "delta", "vec", "melting_temperature", "omega")}}
    print(f"\nHand check {f}:")
    for k in ("mixing_entropy", "mixing_enthalpy", "delta", "vec", "melting_temperature", "omega"):
        hv, pv = h[k], float(d[k])
        print(f"  {k:20s} hand={hv:12.5f}  package={pv:12.5f}  rel.diff={abs(hv - pv) / (abs(pv) + 1e-12):.2e}")
    print("  pair enthalpies (kJ/mol):", h["pairs_kJ/mol"], " radii (pm):", h["radii_pm"])
(out / "heacalculator_handcheck.json").write_text(json.dumps(checks, indent=2, default=float))
