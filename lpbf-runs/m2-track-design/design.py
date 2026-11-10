"""Power-speed sets for the M2 pilot and campaign: scrambled Sobol blocks, not a grid (issue #100, PR #243).

    python design.py        # -> out/pilot_sobol_sets.csv, prints a summary

Why Sobol blocks:
- A 2-D scrambled Sobol sequence (base 2) puts every one of n = 2^m points at a different power AND a different
  speed, so a GP sees 64 distinct levels of each instead of the grid's 4.
- Every block of 16 consecutive points that starts at a multiple of 16 is itself a balanced, space-filling set
  over the whole box (a (t, 4, 2)-net). So each panel gets one block: panel A alone already covers the window
  (it is sectioned first), and A-D together are a 64-point net.
- The campaign continues the same sequence (points 64-79, 80-95, ...). One such block per run stays as an
  unbiased, space-filling hold-out for validating the AM Module, while the rest of each run is chosen by batch BO.

Box: the plan's window for a 400 W M2, P 100-375 W and v 250-2000 mm/s, with speed sampled on a log scale (as
the grid's doubling speeds were). Corners give P/v 0.05-1.5 J/mm. On a 200 W machine, change P_RANGE.
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from scipy.stats import qmc

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"

P_RANGE = (100.0, 375.0)     # W
V_RANGE = (250.0, 2000.0)    # mm/s, sampled in log v
BLOCK = 16                   # Sobol points per panel (2^4)
PANELS = ("A", "B", "C", "D")
N_CONTROLS = 2               # per panel, at the machine's standard 316L set
SEED = 100                   # issue #100


def to_pv(u: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Unit square -> (P in W rounded to 1 W, v in mm/s rounded to 5 mm/s)."""
    P = P_RANGE[0] + u[:, 0] * (P_RANGE[1] - P_RANGE[0])
    lv = math.log(V_RANGE[0]) + u[:, 1] * (math.log(V_RANGE[1]) - math.log(V_RANGE[0]))
    return np.round(P), np.round(np.exp(lv) / 5.0) * 5.0


def sobol_points(n: int, start: int = 0, seed: int = SEED) -> np.ndarray:
    """Points start .. start+n-1 of the scrambled 2-D Sobol sequence, on the unit square."""
    eng = qmc.Sobol(d=2, scramble=True, seed=seed)
    if start:
        eng.fast_forward(start)
    return eng.random(n)


def pilot_sets(n_panels: int = 4, seed: int = SEED) -> list[dict]:
    """The pilot's 64 sets: Sobol points 0-63, block k (16 points) on panel k."""
    u = sobol_points(BLOCK * n_panels, 0, seed)
    P, v = to_pv(u)
    return [dict(id=f"S{i:03d}", sobol_index=i, panel=PANELS[i // BLOCK], P=float(P[i]), v=float(v[i]),
                 E=float(P[i] / v[i]), u_P=float(u[i, 0]), u_v=float(u[i, 1])) for i in range(u.shape[0])]


def discrepancy_report(sets: list[dict]) -> dict:
    """Centred L2 discrepancy (lower is more uniform) of the Sobol sets vs. the 4 x 4 grid, per panel and all."""
    def cd(u):
        return float(qmc.discrepancy(np.asarray(u), method="CD"))
    grid_u = np.array([[(p - P_RANGE[0]) / (P_RANGE[1] - P_RANGE[0]),
                        (math.log(v) - math.log(V_RANGE[0])) / (math.log(V_RANGE[1]) - math.log(V_RANGE[0]))]
                       for p in (100, 200, 300, 375) for v in (250, 500, 1000, 2000)])
    rep = {"grid_4x4": cd(grid_u)}
    for k in PANELS:
        rep[f"sobol_panel_{k}"] = cd([[s["u_P"], s["u_v"]] for s in sets if s["panel"] == k])
    rep["sobol_all_64"] = cd([[s["u_P"], s["u_v"]] for s in sets])
    rep["distinct_P_levels_grid"] = 4
    rep["distinct_P_levels_sobol"] = len({s["P"] for s in sets})
    rep["distinct_v_levels_sobol"] = len({s["v"] for s in sets})
    return rep


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    sets = pilot_sets()
    with open(OUT / "pilot_sobol_sets.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["id", "sobol_index", "panel", "P", "v", "E", "u_P", "u_v"])
        w.writeheader()
        for s in sets:
            w.writerow({k: (round(x, 4) if isinstance(x, float) else x) for k, x in s.items()})
    for k in PANELS:
        b = [s for s in sets if s["panel"] == k]
        print(k, "P", min(s["P"] for s in b), "-", max(s["P"] for s in b), " v", min(s["v"] for s in b), "-",
              max(s["v"] for s in b), " E", round(min(s["E"] for s in b), 3), "-", round(max(s["E"] for s in b), 3))
    print(discrepancy_report(sets))
