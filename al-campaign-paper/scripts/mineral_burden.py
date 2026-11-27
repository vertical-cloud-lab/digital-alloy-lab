#!/usr/bin/env python3
"""Critical-mineral burden of an aluminum alloy, three ways.

The paper's claim "uses less critical minerals than Scalmalloy" needs a number, and the number
depends on the metric. This module computes three, from per-element inputs in
``data/element-criticality.csv`` (sources in that file's ``source`` column):

``B_nir``   mass-weighted U.S. net import reliance of the alloying additions,
            sum over elements other than Al of w_i * NIR_i / 100 (w in wt %, NIR in %).
            Units: wt % of the alloy that the U.S. imports, net. USGS reports some reliances
            only as bounds (Si ">50", Mg ">75", Zr "<25"), so B_nir comes as an interval
            (B_nir_low, B_nir_high) and its midpoint.
``B_cost``  raw-material cost of the critical alloying additions, USD per kg of alloy,
            sum over elements on the 2025 list, other than Al, of (w_i / 100) * price_i.
``B_mass``  mass of the alloying elements on the 2025 list, wt % (every listed element counts 1).
``Sc``      scandium content, wt %.

Aluminum is left out of all of them: it is the base of every alloy compared, so it cancels.

**Comparing two alloys on B_nir.** The bounds on Si, Mg and Zr are the same unknowns for every
alloy: Mg's reliance can't be 75 % for one alloy and 100 % for another. So two alloys are compared
under the same import reliances, not interval against interval. ``paired_difference`` gives the
range of B_nir(a) - B_nir(b) over every allowed choice of the bounded reliances. Because the
difference is linear in each reliance, its extremes sit at the bounds: the upper end takes each
element's high bound where alloy a has more of it, and its low bound where a has less. Alloy a is
robustly below b when that upper end is below zero.
Elements whose inputs are missing are reported, not guessed: the metric comes back as NaN
with the missing elements listed, so a placeholder shows in the paper instead of a wrong number.

Usage:
    python mineral_burden.py            # prints the table for every alloy in data/alloys.csv
"""
from __future__ import annotations

import math
import os
from pathlib import Path

import pandas as pd

PAPER = Path(__file__).resolve().parents[1]
DATA = Path(os.environ.get("CAMPAIGN_DATA", PAPER / "data"))

ELEMENTS = ["si", "mg", "mn", "cr", "zr", "sc", "fe", "cu", "ni", "ce", "er", "ti", "v", "zn", "ag", "b"]


def load_criticality(path: Path = DATA / "element-criticality.csv") -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["element", "on_2025_list", "nir_low_pct", "nir_high_pct",
                                     "price_usd_per_kg"]).set_index("element")
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


def _num(x) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def burden(comp: dict[str, float], crit: pd.DataFrame) -> dict[str, object]:
    """B_nir as an interval (USGS gives some reliances only as bounds, e.g. ">50"), its midpoint,
    B_cost over the elements on the 2025 list, and Sc. Elements off the list (Fe) count zero."""
    if not any(w > 0 for w in comp.values()):
        # No composition entered yet: say so rather than report a burden of zero.
        return {"Sc": float("nan"), "B_nir": float("nan"), "B_nir_low": float("nan"), "B_nir_high": float("nan"),
                "B_nir_missing": "composition", "B_cost": float("nan"), "B_cost_missing": "composition"}
    out: dict[str, object] = {"Sc": comp.get("sc", 0.0)}
    lo = hi = cost = mass = 0.0
    miss_n, miss_c = [], []
    w_al = 100.0 - sum(comp.values())
    for el, w in comp.items():
        if w <= 0:
            continue
        if el not in crit.index:
            miss_n.append(el); miss_c.append(el)
            continue
        r = crit.loc[el]
        on_list = str(r.get("on_2025_list", "")).strip().lower() == "yes"
        l, h = _num(r.get("nir_low_pct")), _num(r.get("nir_high_pct"))
        if math.isnan(l) or math.isnan(h):
            miss_n.append(el)
        else:
            lo += w * l / 100.0
            hi += w * h / 100.0
        if on_list:
            mass += w
            p = _num(r.get("price_usd_per_kg"))
            if math.isnan(p):
                miss_c.append(el)
            else:
                cost += (w / 100.0) * p
    out["B_nir_low"] = float("nan") if miss_n else lo
    out["B_nir_high"] = float("nan") if miss_n else hi
    out["B_nir"] = float("nan") if miss_n else (lo + hi) / 2.0
    out["B_nir_missing"] = ",".join(miss_n)
    out["B_cost"] = float("nan") if miss_c else cost
    out["B_cost_missing"] = ",".join(miss_c)
    # B_mass needs only the list status, so an element missing from the inputs makes it NaN.
    out["B_mass"] = float("nan") if any(el not in crit.index for el, w in comp.items() if w > 0) else mass
    # Cost over the priced elements only (e.g. A20X, whose boron has no element price).
    out["B_cost_priced"] = cost
    # Sensitivity: the same interval with aluminum counted at its own import reliance.
    if "al" in crit.index and not miss_n:
        al_lo, al_hi = _num(crit.loc["al"].get("nir_low_pct")), _num(crit.loc["al"].get("nir_high_pct"))
        out["B_nir_al_low"] = lo + w_al * al_lo / 100.0
        out["B_nir_al_high"] = hi + w_al * al_hi / 100.0
    else:
        out["B_nir_al_low"] = out["B_nir_al_high"] = float("nan")
    return out


def paired_difference(comp_a: dict[str, float], comp_b: dict[str, float],
                      crit: pd.DataFrame) -> tuple[float, float]:
    """(min, max) of B_nir(a) - B_nir(b) with both alloys under the same import reliances.

    Each reliance can sit anywhere in its USGS bounds, but at the same value for both alloys.
    NaN if either alloy has an element without reliance inputs."""
    lo = hi = 0.0
    for el in sorted(set(comp_a) | set(comp_b)):  # fixed order, so rounding is the same on every run
        d = comp_a.get(el, 0.0) - comp_b.get(el, 0.0)
        if d == 0:
            continue
        if el not in crit.index:
            return float("nan"), float("nan")
        l, h = _num(crit.loc[el].get("nir_low_pct")), _num(crit.loc[el].get("nir_high_pct"))
        if math.isnan(l) or math.isnan(h):
            return float("nan"), float("nan")
        a, b = d * l / 100.0, d * h / 100.0
        lo += min(a, b)
        hi += max(a, b)
    return lo, hi


def robustly_below(comp_a: dict[str, float], comp_b: dict[str, float], crit: pd.DataFrame) -> bool:
    """True if alloy a has a lower B_nir than b under every allowed choice of the bounded reliances."""
    _, hi = paired_difference(comp_a, comp_b, crit)
    return not math.isnan(hi) and hi < 0


def pareto_front(points: list[tuple[str, float, float]]) -> list[str]:
    """IDs of the points no other point beats on both axes: lower burden and higher strength.

    points: (id, burden, strength). A point is dominated if another has burden <= and strength >=,
    with at least one strict. Points with a NaN coordinate are left out."""
    pts = [(i, b, s) for i, b, s in points if not (math.isnan(b) or math.isnan(s))]
    front = []
    for i, b, s in pts:
        if not any((b2 <= b and s2 >= s) and (b2 < b or s2 > s) for _, b2, s2 in pts):
            front.append(i)
    return front


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
