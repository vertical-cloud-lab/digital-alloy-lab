#!/usr/bin/env python3
"""Turn our own phase-boundary measurements (DSC liquidus/solidus, solvus from quench-and-XRD,
EDS/EPMA tie-lines) into ESPEI "ZPF" datasets and ORCHID-style rows, so they can be scored and
fitted next to the literature data PR #238 pulled from ORCHID.

Input: measurements.csv, one row per measured boundary point:

  system        e.g. AL-MN-CR-ZR (sorted elements, as in ORCHID's al-cu-coverage.csv)
  sample_id     our alloy / run ID
  T_K, u_T_K    temperature and its standard uncertainty
  kind          liquidus | solidus | solvus | tie_line
  known_phase   phase whose composition we know (the alloy's own: LIQUID for a liquidus,
                FCC_A1 for a solidus or solvus)
  other_phases  ';'-separated phases in equilibrium whose compositions are unknown
                (the primary phase for a liquidus, identified by XRD/SEM of the DSC sample)
  x_json        measured overall composition as mole fractions of all but the dependent
                component, e.g. {"MN": 0.0055, "CR": 0.0021, "ZR": 0.0040} (from ICP-OES)
  method        e.g. "DSC heating, 3 rates extrapolated to 0 K/min"
  link          URL of the run record (issue comment, data file)

ESPEI's rule (docs/reference/dataset_schema.qmd, ESPEI c9143c8): each phase region needs at least one
phase with a prescribed composition, and unknown phase compositions are written as null.
For a liquidus on an alloy of known composition that is [["LIQUID", comps, x], [primary, comps, null]].

CLI:
    python espei_export.py measurements.csv --dependent AL --reference "VCL-2026" --out-dir espei/
    python espei_export.py --demo
"""
from __future__ import annotations

import argparse
import csv
import json
import os
from collections import defaultdict


def zpf_region(row, comps_indep):
    x = json.loads(row["x_json"])
    known = [row["known_phase"], comps_indep, [x[c] for c in comps_indep]]
    others = [[ph, comps_indep, [None] * len(comps_indep)]
              for ph in row["other_phases"].split(";") if ph.strip()]
    return [known] + others


def to_espei(rows, dependent="AL", reference="VCL", comment=""):
    """Group rows by system -> one ESPEI ZPF dataset each."""
    by_sys = defaultdict(list)
    for r in rows:
        by_sys[r["system"]].append(r)
    datasets = {}
    for system, rs in by_sys.items():
        elements = sorted(set(system.split("-")))
        if dependent not in elements:
            raise ValueError(f"{system}: dependent component {dependent} not in system")
        indep = [e for e in elements if e != dependent]
        phases = sorted({r["known_phase"] for r in rs} |
                        {p for r in rs for p in r["other_phases"].split(";") if p.strip()})
        datasets[system] = {
            "components": elements,
            "phases": phases,
            "conditions": {"P": 101325, "T": [float(r["T_K"]) for r in rs]},
            "broadcast_conditions": False,
            "output": "ZPF",
            "values": [zpf_region(r, indep) for r in rs],
            "reference": reference,
            "comment": comment or "; ".join(sorted({r["method"] for r in rs})),
        }
    return datasets


def to_orchid_rows(rows):
    """Subset of ORCHID's invariant CSV columns (see PR #238 al-cu-literature-invariants.csv)."""
    out = []
    for r in rows:
        x = json.loads(r["x_json"])
        out.append({
            "system": r["system"], "record_id": f"VCL-{r['sample_id']}-{r['kind']}",
            "T_K": float(r["T_K"]), "T_C": round(float(r["T_K"]) - 273.15, 2), "u_T_K": r.get("u_T_K", ""),
            "transition_kind": r["kind"],
            "model_phases": "; ".join([r["known_phase"]] + [p for p in r["other_phases"].split(";") if p]),
            "x_by_phase_mole_fraction": json.dumps({r["known_phase"]: x}),
            "origin": "measured_in_house", "observation_type": r["method"], "measured_in_raw": r.get("link", ""),
        })
    return out


DEMO_ROWS = [
    {"system": "AL-MN-ZR", "sample_id": "S1", "T_K": "935.2", "u_T_K": "1.5", "kind": "liquidus",
     "known_phase": "LIQUID", "other_phases": "AL3ZR_D023", "x_json": json.dumps({"MN": 0.0055, "ZR": 0.0040}),
     "method": "DSC heating 5/10/20 K/min, extrapolated to 0", "link": "https://example.invalid/run/S1"},
    {"system": "AL-MN-ZR", "sample_id": "S1", "T_K": "929.0", "u_T_K": "1.5", "kind": "solidus",
     "known_phase": "FCC_A1", "other_phases": "LIQUID", "x_json": json.dumps({"MN": 0.0055, "ZR": 0.0040}),
     "method": "DSC heating 5/10/20 K/min, extrapolated to 0", "link": "https://example.invalid/run/S1"},
]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv", nargs="?")
    p.add_argument("--dependent", default="AL")
    p.add_argument("--reference", default="VCL")
    p.add_argument("--out-dir")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args(argv)
    if a.demo:
        rows = DEMO_ROWS
    else:
        if not a.csv:
            p.error("measurements.csv required (or --demo)")
        with open(a.csv, newline="") as fh:
            rows = list(csv.DictReader(fh))
    ds = to_espei(rows, a.dependent, a.reference)
    orc = to_orchid_rows(rows)
    if a.out_dir:
        os.makedirs(a.out_dir, exist_ok=True)
        for system, d in ds.items():
            with open(os.path.join(a.out_dir, f"{system}-zpf-{a.reference}.json"), "w") as fh:
                json.dump(d, fh, indent=2)
        with open(os.path.join(a.out_dir, "orchid-style-rows.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(orc[0]))
            w.writeheader()
            w.writerows(orc)
    print(json.dumps({"espei": ds, "orchid_rows": orc}, indent=2))


if __name__ == "__main__":
    main()
