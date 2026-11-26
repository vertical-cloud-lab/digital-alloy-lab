#!/usr/bin/env python3
"""Composition lists for the CALPHAD screen (#275): named alloys and family grids.

Named alloys are run on a pure-Al base and, for the seeds and their near neighbours, as they would come
out of a charge built on 6063 (which brings about 0.55 Mg, 0.40 Si and 0.20 Fe; see process_models.recipe).
Known crack-prone alloys (7075, 6061, 2024, Al-3Mg, a cracked Al-Mn-Cr-Zr-Mg variant) are included on
purpose, to check whether the cracking indices rank them where experiments put them.

    python bofn-seeding/first-six/make_lists.py      # writes lists/named.json and lists/grids.json
"""
from __future__ import annotations

import itertools
import json
import pathlib

from process_models import recipe

HERE = pathlib.Path(__file__).resolve().parent

# id: (composition wt%, group, also run on a 6063 base?, note)
NAMED = {
    # the six seeds (D1, D2, S1-S4) and the optional three (O1-O3)
    "D1": (dict(Si=10.0, Mg=0.35), "seed", True, "AlSi10Mg-type benchmark"),
    "D2": (dict(Mg=4.6, Sc=0.66, Zr=0.42, Mn=0.49), "seed", True, "Scalmalloy-type benchmark"),
    "S1": (dict(Mn=4.8, Cr=0.9, Zr=1.1, Mg=1.2), "seed", True, "Chalmers alloy F"),
    "S1-noMg": (dict(Mn=5.0, Cr=0.8, Zr=0.6), "relative", True, "Chalmers alloy C: S1 without Mg and at 0.6 Zr"),
    "S2": (dict(Fe=1.87, Mg=1.02, Zr=1.03), "seed", True, "Al-Fe-Mg-Zr, Li et al. 2025"),
    "S3": (dict(Si=3.5, Mg=2.5), "seed", True, "AlSi3.5Mg2.5 nominal, Knoop et al. 2020"),
    "S4": (dict(Mg=6.0, Si=2.5, Ti=0.7), "seed", True, "Al-Mg-Si-Ti, Wen et al. 2024 (exploratory)"),
    "O1": (dict(Mg=3.6, Zr=1.2), "optional", True, "Al-Mg-Zr, Croteau et al. 2018"),
    "O2-noEr": (dict(Mg=6.4, Mn=0.72, Zr=1.1), "optional", True, "Guo et al. 2022 Al-Mg-Mn-Er-Zr with the Er left out (Er is in neither database)"),
    "O3": (dict(Mn=4.8, Cr=0.8), "optional", True, "Zr-free Al-Mn-Cr, Chalmers alloy B"),
    "7xxx-Zr": (dict(Zn=5.5, Mg=2.3, Cu=1.5, Zr=1.0), "relative", True, "7xxx + Zr (7A77-type window)"),
    "Mg4.5Mn0.5Zr0.6": (dict(Mg=4.5, Mn=0.5, Zr=0.6), "relative", True, "Al-Mg-Mn-Zr at lower Mg and Zr"),
    # close relatives and literature points
    "S3-measured": (dict(Si=3.3, Mg=2.3), "relative", False, "Knoop powder as measured"),
    "AlSi4Mg2": (dict(Si=4.0, Mg=2.0), "relative", False, "Kimura et al. 2019 ladder"),
    "AlMg9.6Si4.9": (dict(Mg=9.6, Si=4.9), "relative", False, "Al-Mg2Si pseudo-eutectic, Yang et al. 2023"),
    "A357": (dict(Si=7.0, Mg=0.6), "relative", False, "AlSi7Mg0.6"),
    "ChalmersD": (dict(Mn=4.7, Cr=0.8, Zr=1.2), "relative", True, "high Zr, no Mg"),
    "ChalmersE-cracked": (dict(Mn=4.7, Cr=0.8, Zr=0.7, Mg=1.0), "known-cracker", False, "cracked in LPBF"),
    "HS1": (dict(Mn=4.8, Cr=0.8, Zr=0.8), "relative", True, "Hoganas forAM Al-HS1 datasheet"),
    "Mair": (dict(Mn=4.8, Ti=0.82, Zr=0.71), "relative", True, "Al-Mn-Ti-Zr powder as measured, Mair et al. 2022"),
    "MnTi-noZr": (dict(Mn=4.8, Ti=0.8), "relative", True, "Mair's alloy without Zr"),
    # other Zr-free candidates looked at for the exploratory seed
    "Mg5Si2Ti0.7": (dict(Mg=5.0, Si=2.0, Ti=0.7), "exploratory", True, "Al-Mg-Si-Ti at lower Mg and Si"),
    "S3-Ti": (dict(Si=3.5, Mg=2.5, Ti=0.7), "exploratory", True, "S3 plus Ti"),
    "MgMnTi": (dict(Mg=4.5, Mn=0.5, Ti=0.8), "exploratory", True, "Ti in place of Sc and Zr in an Al-Mg-Mn alloy"),
    "S2-Ti-noZr": (dict(Fe=1.9, Mg=1.0, Ti=0.8), "exploratory", True, "S2 with Ti in place of Zr"),
    "S1-Ti-noZr": (dict(Mn=4.8, Cr=0.9, Mg=1.2, Ti=0.8), "exploratory", True, "S1 with Ti in place of Zr"),
    "S1-noZr": (dict(Mn=4.7, Cr=0.8, Mg=1.0), "exploratory", True, "S1 without Zr: a cracking-boundary probe"),
    "O1-Mn": (dict(Mg=3.6, Zr=1.2, Mn=0.5), "exploratory", True, "O1 with Mn"),
    "Fe2.5Mn2Mg1": (dict(Fe=2.5, Mn=2.0, Mg=1.0), "exploratory", True, "Zr-free Al-Fe-Mn-Mg"),
    "Mg5.4Zn3Si2Mn": (dict(Mg=5.39, Zn=3.08, Si=1.96, Mn=0.75), "exploratory", True, "Zr-free Al-Mg-Zn-Si-Mn, Yang et al. 2022 (as reported by Edison q4)"),
    "Mn7": (dict(Mn=7.0), "relative", False, "Al-7Mn patent example"),
    "CP1": (dict(Fe=1.0, Zr=1.0), "relative", True, "Aheadd CP1 mid-range"),
    "CP1-patentA": (dict(Fe=1.04, Zr=1.78), "relative", False, "patent example"),
    "Fe2.5": (dict(Fe=2.5), "relative", True, "near-eutectic Al-Fe, Qi et al. 2020"),
    "Fe2.5Mn2": (dict(Fe=2.5, Mn=2.0), "relative", True, "Wang et al. 2023"),
    "Fe4": (dict(Fe=4.0), "relative", False, "patent example"),
    "Croteau-1.57Zr": (dict(Mg=3.66, Zr=1.57), "relative", False, "Croteau et al. 2018"),
    "Al5X1-mid": (dict(Mg=3.4, Zr=1.2, Mn=0.5), "relative", True, "EOS / Constellium Al5X1 mid-range"),
    "5083-0.7Zr": (dict(Mg=4.5, Mn=0.7, Cr=0.15, Zr=0.7), "relative", False, "Zhou et al. 2019"),
    "MgCrZr": (dict(Mg=5.2, Cr=0.5, Zr=1.0), "relative", False, "patent example"),
    "D2-lowSc": (dict(Mg=4.5, Sc=0.2, Zr=0.6, Mn=0.5), "relative", True, "low-Sc bridge"),
    "Mg3.2Sc0.36": (dict(Mg=3.2, Sc=0.36), "relative", False, "Zr-free low-Sc patent example"),
    "AlMnSc": (dict(Mn=4.52, Mg=1.32, Sc=0.79, Zr=0.74), "relative", False, "Jia et al. 2019"),
    "AlMg8Si1.3ScZr": (dict(Mg=8.0, Si=1.3, Mn=0.5, Sc=0.5, Zr=0.3), "relative", False, "Li et al. 2020"),
    "MnMgZr-Yu": (dict(Mn=5.82, Mg=2.68, Zr=0.54), "known-cracker", False, "Yu et al. 2023 without its Er; cracked over most of its window"),
    "NiMnFeZr": (dict(Mn=1.5, Ni=3.9, Fe=2.0, Zr=0.8), "relative", False, "patent example"),
    "MnNiCuZr": (dict(Mn=4.0, Ni=3.0, Cu=2.0, Zr=2.0), "relative", False, "Al-Mn-Ni-Cu-Zr family"),
    "6061-1Zr": (dict(Mg=0.83, Si=0.62, Cu=0.23, Cr=0.08, Fe=0.25, Zr=1.0), "relative", False, "Mehta et al. 2021"),
    # controls
    "6063": (dict(Mg=0.55, Si=0.40, Fe=0.20), "baseline", False, "the base itself"),
    "7075": (dict(Zn=5.4, Mg=2.25, Cu=1.54, Cr=0.19), "known-cracker", False, "Martin et al. 2017 powder"),
    "6061": (dict(Mg=0.83, Si=0.62, Cu=0.23, Cr=0.08, Fe=0.25), "known-cracker", False, ""),
    "2024": (dict(Cu=4.4, Mg=1.5, Mn=0.6), "known-cracker", False, ""),
    "Mg3": (dict(Mg=3.0), "known-cracker", False, "binary Al-Mg cracks at low Mg"),
    "Mg6": (dict(Mg=6.0), "known-cracker", False, ""),
}


def up(d):
    return {k.upper(): v for k, v in d.items()}


def named():
    items = []
    for nid, (wt, group, on6063, note) in NAMED.items():
        tags = {"set": "named", "id": nid, "group": group, "note": note}
        items.append({"name": f"{nid}|pureAl", "wt": up(wt), "tags": {**tags, "base": "pureAl"}})
        if on6063:
            r = recipe(wt, base="6063")
            items.append({"name": f"{nid}|6063", "wt": up(r["melt_wt"]), "tags": {**tags, "base": "6063", "f_base": r["f_base"], "f_4047": r["f_4047"]}})
    # seeds first, so a partial run already covers them
    order = {"seed": 0, "optional": 1, "known-cracker": 2, "baseline": 2, "relative": 3, "exploratory": 4}
    items.sort(key=lambda it: order[it["tags"]["group"]])
    return items


def grids():
    items = []

    def add(tag, wt, **extra):
        wt = {k: v for k, v in wt.items() if v > 0}
        nm = tag + ":" + "-".join(f"{k}{v:g}" for k, v in sorted(wt.items()))
        items.append({"name": nm, "wt": wt, "tags": {"set": "grid", "grid": tag}, **extra})

    for si, mg in itertools.product([0, 2, 3.5, 6, 10], [0.35, 1, 2.5, 4.5, 6.5]):
        add("SiMg", {"SI": si, "MG": mg, "FE": 0.15})
    for mn, cr in itertools.product([3, 4.8, 6], [0, 0.8, 1.6]):
        add("MnCr", {"MN": mn, "CR": cr})
    for fe, extra in itertools.product([1.0, 2.0, 3.0], [{}, {"MN": 2.0}, {"MG": 1.0}]):
        add("FeX", {"FE": fe, **extra})
    for mg, zr in itertools.product([3.5, 6.5], [0.6, 1.2]):
        add("MgZr", {"MG": mg, "ZR": zr})
    # what the 6063 base does: Mg and Si added to two Mg-free, Si-free alloys
    for si, mg in ((0.0, 0.3), (0.0, 0.55), (0.2, 0.0), (0.4, 0.0), (0.2, 0.3), (0.4, 0.55)):
        add("MnCrZr+base", {"MN": 5.0, "CR": 0.8, "ZR": 0.6, "SI": si, "MG": mg})
    for si, mg in ((0.0, 0.55), (0.4, 0.0), (0.4, 0.55)):
        add("FeZr+base", {"FE": 1.0, "ZR": 1.0, "SI": si, "MG": mg})
    # liquidus only, for the element this database has and COST 507 lacks (Sc). The Zr, Ti, Cr, Mn and Fe
    # liquidus curves come from COST 507 (liquidus_cost507.py), because this database has no Al3Zr liquidus.
    for sc in [0.2, 0.4, 0.7, 1.0]:
        add("liq-Sc", {"SC": sc}, liquidus_only=True)
        add("liq-Sc-Mg4.5", {"SC": sc, "MG": 4.5}, liquidus_only=True)
    return items


if __name__ == "__main__":
    out = HERE / "lists"
    out.mkdir(exist_ok=True)
    for name, items in (("named", named()), ("grids", grids())):
        (out / f"{name}.json").write_text(json.dumps(items, indent=1) + "\n")
        print(name, len(items))
