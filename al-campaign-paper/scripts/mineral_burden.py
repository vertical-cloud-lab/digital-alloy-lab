#!/usr/bin/env python3
"""Critical-mineral burden of an aluminum alloy, three ways.

The paper's claim "uses less critical minerals than Scalmalloy" needs a number, and the number
depends on the metric. This module computes three, from per-element inputs in
``data/element-criticality.csv`` (sources in that file's ``source`` column):

``B_nir``   mass-weighted U.S. net import reliance of the alloying additions,
            sum over elements other than Al of w_i * NIR_i / 100 (w in wt %, NIR in %).
            Units: wt % of the alloy that the U.S. imports, net.
``B_cost``  raw-material cost of the alloying additions, USD per kg of alloy,
            sum over elements other than Al of (w_i / 100) * price_i.
``Sc``      scandium content, wt %.

Aluminum is left out of all three: it is the base of every alloy compared, so it cancels.
Elements whose inputs are missing are reported, not guessed: the metric comes back as NaN
with the missing elements listed, so a placeholder shows in the paper instead of a wrong number.

Usage:
    python mineral_burden.py            # prints the table for every alloy in data/alloys.csv
"""
from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

PAPER = Path(__file__).resolve().parents[1]
DATA = PAPER / "data"

ELEMENTS = ["si", "mg", "mn", "cr", "zr", "sc", "fe", "cu", "ni", "ce", "er", "ti", "v", "zn", "ag", "b"]


def load_criticality(path: Path = DATA / "element-criticality.csv") -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["element", "on_2025_list", "nir_pct", "price_usd_per_kg"]).set_index("element")
    df = pd.read_csv(path, comment="#")
    df["element"] = df["element"].str.strip().str.lower()
    return df.set_index("element")


def composition(row: pd.Series) -> dict[str, float]:
    """wt % of each alloying element in a row of alloys.csv (blank = 0)."""
    comp = {}
    for el in ELEMENTS:
        v = row.get(el, float("nan"))
        try:
            v = float(v)
        except (TypeError, ValueError):
            v = float("nan")
        comp[el] = 0.0 if math.isnan(v) else v
    return comp


def burden(comp: dict[str, float], crit: pd.DataFrame) -> dict[str, object]:
    if not any(w > 0 for w in comp.values()):
        # No composition entered yet: say so rather than report a burden of zero.
        return {"Sc": float("nan"), "B_nir": float("nan"), "B_nir_missing": "composition",
                "B_cost": float("nan"), "B_cost_missing": "composition"}
    out: dict[str, object] = {"Sc": comp.get("sc", 0.0)}
    for metric, col in (("B_nir", "nir_pct"), ("B_cost", "price_usd_per_kg")):
        total, missing = 0.0, []
        for el, w in comp.items():
            if w <= 0:
                continue
            val = crit[col].get(el, float("nan")) if col in crit.columns else float("nan")
            try:
                val = float(val)
            except (TypeError, ValueError):
                val = float("nan")
            if math.isnan(val):
                missing.append(el)
                continue
            total += w * val / 100.0
        out[metric] = float("nan") if missing else total
        out[metric + "_missing"] = ",".join(missing)
    return out


def table(alloys: pd.DataFrame | None = None, crit: pd.DataFrame | None = None) -> pd.DataFrame:
    if alloys is None:
        alloys = pd.read_csv(DATA / "alloys.csv")
    if crit is None:
        crit = load_criticality()
    rows = []
    for _, r in alloys.iterrows():
        b = burden(composition(r), crit)
        rows.append({"alloy_id": r["alloy_id"], **b})
    return pd.DataFrame(rows).set_index("alloy_id")


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    print(table())
