"""The pilot's parameter sets and track map, from §4 of ../m2-single-track-schedule.md.

Shared by figures.py (static figures) and steps.py (the 3-D animation), so both draw the same tracks in the same
places. Everything here is the plan's example layout; the real track map comes from the job file (step A1).

Insert coordinates (mm): the insert's top face is the square [0, 25] x [0, 25] at z = 0. Tracks run along +x (the
scan direction, the same on every track): row 1 from x = 3 to 11, row 2 from x = 14 to 22 (8 mm long, rows 3 mm
apart). Track centres are at y = 4.5 + 2k, k = 0..8 (2 mm pitch). The gas is assumed to flow along -y (inlet at
high y, outlet at y = 0), so tracks are exposed from low y to high y: from the outlet side toward the inlet.
"""
from __future__ import annotations

import numpy as np

POWERS_W = (100, 200, 300, 375)
SPEEDS_MM_S = (250, 500, 1000, 2000)
CONTROL = "C"                      # the machine's standard stainless set (values from the kickoff)

INSERT = 25.0                      # cube edge, mm (the plan's example; rescale to the real inserts)
TRACK_LEN = 8.0
ROW_X = ((3.0, 11.0), (14.0, 22.0))
TRACK_Y = tuple(4.5 + 2.0 * k for k in range(9))
INSERTS = ("A", "B", "C", "D")
SEED = 100                         # issue #100; example randomization only


def grid_sets() -> list[dict]:
    """The 16 power-speed sets, with their line energy P/v in J/mm."""
    return [dict(id=f"P{p}-v{v}", P=p, v=v, E=p / v) for p in POWERS_W for v in SPEEDS_MM_S]


def track_map(seed: int = SEED) -> list[dict]:
    """72 tracks: each insert carries the 16 grid sets and 2 controls in its own random order.

    Returns one dict per track with insert, row (1 or 2), k (0..8 along y), the insert-local start and end points,
    the parameter set (P, v, E; None for controls) and its exposure order on the plate (0..71)."""
    rng = np.random.default_rng(seed)
    sets = grid_sets() + [dict(id=CONTROL, P=None, v=None, E=None)] * 2
    out = []
    order = 0
    for ins in INSERTS:
        perm = rng.permutation(len(sets))
        slots = [(row, k) for k in range(9) for row in (1, 2)]       # exposure order: low y first, row 1 then 2
        for (row, k), j in zip(slots, perm):
            x0, x1 = ROW_X[row - 1]
            s = sets[j]
            out.append(dict(insert=ins, row=row, k=k, start=(x0, TRACK_Y[k]), end=(x1, TRACK_Y[k]),
                            set=s["id"], P=s["P"], v=s["v"], E=s["E"], order=order))
            order += 1
    return out


def regime(E: float | None) -> str:
    """Illustrative only: a coarse regime by line energy, for drawing. The AM Module's printability map replaces it."""
    if E is None:
        return "control"
    if E < 0.1:
        return "balling / lack of fusion"
    if E < 0.4:
        return "conduction"
    if E < 0.8:
        return "transition"
    return "keyhole"


if __name__ == "__main__":
    tm = track_map()
    for ins in INSERTS:
        ts = [t for t in tm if t["insert"] == ins]
        print(ins, len(ts), sum(t["set"] == CONTROL for t in ts), sorted({t["set"] for t in ts}) == sorted(
            {s["id"] for s in grid_sets()} | {CONTROL}))
    Es = [s["E"] for s in grid_sets()]
    print("P/v range", min(Es), max(Es))
