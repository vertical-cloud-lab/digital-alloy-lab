"""The pilot's parameter sets and track map, from §4 of ../m2-single-track-schedule.md.

Shared by figures.py (static figures) and steps.py (the 3-D animation), so both draw the same tracks in the same
places. Everything here is the plan's example layout; the real track map comes from the job file (step A1).

The plate (PLATE ... PLATE_HOLE_IN) is measured from Nathan C.'s photo of it (PR #243): its outside is "about
10 in x 10 in" (his estimate), and everything else is scaled from that after rectifying the photo's top face, so read
these as +-5 %. Four square panels sit in four pockets in a 2 x 2 grid around the plate's centre, each with four
holes near its corners; the plate has a hole near each corner.

Block coordinates (mm): each panel carries one 25 mm track block at its centre, whose top face is the square
[0, 25] x [0, 25] at z = 0 (so the panel's top face is [-31.5, 56.5] x [-31.5, 56.5]). Tracks run along +x (the scan
direction, the same on every track): row 1 from x = 3 to 11, row 2 from x = 14 to 22 (8 mm long, rows 3 mm apart).
Track centres are at y = 4.5 + 2k, k = 0..8 (2 mm pitch). The block is sized for the 1.25 in mounts (one row's
section is about 22 mm wide), and the bandsaw cuts it out of the panel before sectioning. The gas is assumed to
flow along -y (inlet at high y, outlet at y = 0), so tracks are exposed from low y to high y: from the outlet side
toward the inlet.
"""
from __future__ import annotations

import numpy as np

POWERS_W = (100, 200, 300, 375)
SPEEDS_MM_S = (250, 500, 1000, 2000)
CONTROL = "C"                      # the machine's standard stainless set (values from the kickoff)

# Nathan C.'s plate, from his photo (outside "about 10 in", his estimate; the rest scaled from it)
PLATE = 254.0                      # outside, square
PLATE_HOLE_IN = 26.0               # corner holes: centres this far in from both edges
POCKET = 90.0                      # four square pockets ...
POCKET_PITCH = 100.0               # ... centred at +-50 mm from the plate's centre (a 10 mm web between them)
PANEL = 88.0                       # the removable panels, about 3.5 in (the photo's dark outline round each,
                                   # about 2.5 mm wide, includes the edge breaks; the plan reads 88 mm in 90 mm)
PANEL_HOLE = 34.5                  # four holes per panel, at +-34.5 mm from its centre

BLOCK = 25.0                       # the track block at each panel's centre (top face [0, 25]^2)
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

    Returns one dict per track with insert, row (1 or 2), k (0..8 along y), the block-coordinate start and end points,
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
