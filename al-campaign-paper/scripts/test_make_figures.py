#!/usr/bin/env python3
"""Run make_figures.py on synthetic campaign data, so the code paths that only run once real data
arrives are exercised now, not in February.

    python al-campaign-paper/scripts/test_make_figures.py

The synthetic rows are written to a temporary copy of data/; the real data, figures and tables
are not touched. Nothing here is a result: the values are made up to have the right shape.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"


def append(path: Path, rows: list[dict]) -> None:
    df = pd.read_csv(path)
    df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
    df.to_csv(path, index=False)


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="campaign-test-"))
    data, fig, gen = tmp / "data", tmp / "figures", tmp / "generated"
    shutil.copytree(DATA, data)
    fig.mkdir()
    gen.mkdir()
    alloys = ["SYN-A", "SYN-B", "SYN-C"]
    append(data / "alloys.csv", [
        {"alloy_id": a, "name": a, "role": r, "family": "Al-Mg-Zr", "mg": 3.0 + i, "zr": 1.0, "fe": 0.5 * i}
        for i, (a, r) in enumerate(zip(alloys, ["seed", "pick", "finalist"]))])
    append(data / "runs.csv", [{"run_id": f"r{i}", "date": "2027-01-05", "alloy_id": a, "block": "S",
                                "charge_g": 250, "outcome": "ok"} for i, a in enumerate(alloys)])
    append(data / "calphad_screen.csv", [
        {"composition_id": f"c{i}", "family": "Al-Mg-Zr", "freezing_range_c": 20 + 3 * i,
         "strengthening_phase_frac": 0.01 * (i % 7), "burden_B": 0.3 * i, "picked_as": "seed" if i % 9 == 0 else ""}
        for i in range(40)])
    append(data / "powder.csv", [{"lot_id": f"l{i}", "run_id": f"r{i}", "alloy_id": a, "d10_um": 20, "d50_um": 55 + i,
                                  "d90_um": 110} for i, a in enumerate(alloys)])
    append(data / "density.csv", [{"specimen_id": f"d{i}{j}", "alloy_id": a, "rel_density_pct": 98.5 + 0.3 * j}
                                  for i, a in enumerate(alloys) for j in range(3)])
    append(data / "hardness.csv", [{"specimen_id": f"h{i}{c}", "alloy_id": a, "condition": c, "hv_mean": 90 + 10 * i}
                                   for i, a in enumerate(alloys) for c in ("as built", "aged")])
    append(data / "tensile.csv", [{"specimen_id": f"t{a}{j}", "alloy_id": a, "ys_mpa": 260 + 20 * j, "uts_mpa": 320,
                                   "el_pct": 8 + j, "valid": "yes"} for a in alloys[1:] for j in range(3)])
    append(data / "corrosion.csv", [{"specimen_id": f"k{i}{j}", "alloy_id": a, "icorr_ua_cm2": 0.5 + i, "valid": "yes"}
                                    for i, a in enumerate(alloys) for j in range(3)])
    env = dict(os.environ, CAMPAIGN_DATA=str(data), CAMPAIGN_FIG=str(fig), CAMPAIGN_GEN=str(gen),
               CAMPAIGN_STATUS=str(tmp / "figure-status.md"))
    r = subprocess.run([sys.executable, str(HERE / "make_figures.py")], env=env, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
        print("FAIL: make_figures.py crashed on synthetic data")
        return 1
    checks = {
        "Fig1 draws campaign tensile": "(a) campaign tensile drawn" in r.stdout,
        "Fig2 drawn": "Fig2: drawn from" in r.stdout,
        "Fig3 drawn": "Fig3: drawn from" in r.stdout,
        "Fig4 drawn": "Fig4: drawn from" in r.stdout,
        "Fig5 hardness drawn": "(a) drawn" in r.stdout,
        "Fig6 drawn": "Fig6: drawn from" in r.stdout,
        "all figure files written (6 main + SI S1)": len(list(fig.glob("*.pdf"))) == 7,
        "composition count filled": r"\newcommand{\NCompositions}{3}" in (gen / "numbers.tex").read_text(),
        "run count filled": r"\newcommand{\NAlRuns}{3}" in (gen / "numbers.tex").read_text(),
    }
    for k, ok in checks.items():
        print(("ok   " if ok else "FAIL ") + k)
    shutil.rmtree(tmp)
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
