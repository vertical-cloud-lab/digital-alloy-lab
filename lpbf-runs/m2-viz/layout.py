"""The pilot's parameter sets and track map, from §4 of ../m2-single-track-schedule.md.

Shared by figures.py (static figures) and steps.py (the 3-D animation), so both draw the same tracks in the same
places. Everything here is the plan's example layout; the real track map comes from the job file (step A1).

The plate (PLATE ... PLATE_HOLE_IN) is measured from Nathan C.'s photo of it (PR #243): its outside is "about
10 in x 10 in" (his estimate), and everything else is scaled from that after rectifying the photo's top face, so read
these as +-5 %. Four square panels sit in four pockets in a 2 x 2 grid around the plate's centre, each with four
holes near its corners; the plate has a hole near each corner.

Block coordinates (mm), kept from the earlier 25 mm track block: the panel's centre is at (12.5, 12.5) and its top
face is [-31.5, 56.5] x [-31.5, 56.5] at z = 0. Each panel carries one row of 18 tracks across its middle (§4 of the
plan). Tracks run along +x (the scan direction, the same on every track), 12 mm long from x = 6.5 to 18.5, so every
track's mid-length lies on the line x = X_MID = 12.5: the target plane, which one strip of the panel holds (§3). The
tracks sit at 2 mm pitch in two groups of nine, y = -8.5 ... 7.5 and 17.5 ... 33.5; each group becomes one mount
piece (about 22 mm wide, for the 1.25 in mounts), and the 10 mm gap between them leaves room for the bandsaw cut that
splits them. The gas is assumed to flow along -y (inlet at high y, outlet at low y), so tracks are exposed from low y
to high y: from the outlet side toward the inlet.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

POWERS_W = (100, 200, 300, 375)    # axis ticks only: the window is 100-375 W ...
SPEEDS_MM_S = (250, 500, 1000, 2000)  # ... and 250-2000 mm/s (log scale)
CONTROL = "C"                      # the machine's standard stainless set (values from the kickoff)
# The pilot's 64 power-speed settings: a scrambled Sobol sequence, one 16-point block per panel (A = points 0-15,
# B = 16-31, ...). Written by ../m2-track-design/design.py; read from its CSV so this module needs no scipy.
SOBOL_CSV = Path(__file__).resolve().parent.parent / "m2-track-design" / "out" / "pilot_sobol_sets.csv"

# Nathan C.'s plate, from his photo (outside "about 10 in", his estimate; the rest scaled from it)
PLATE = 254.0                      # outside, square
PLATE_HOLE_IN = 26.0               # corner holes: centres this far in from both edges
POCKET = 90.0                      # four square pockets ...
POCKET_PITCH = 100.0               # ... centred at +-50 mm from the plate's centre (a 10 mm web between them)
PANEL = 88.0                       # the removable panels, about 3.5 in (the photo's dark outline round each,
                                   # about 2.5 mm wide, includes the edge breaks; the plan reads 88 mm in 90 mm)
PANEL_HOLE = 34.5                  # four holes per panel, at +-34.5 mm from its centre

BLOCK = 25.0                       # block coordinates: the panel's centre is at (BLOCK / 2, BLOCK / 2)
CENTRE = BLOCK / 2
TRACK_LEN = 12.0                   # plan §4: 3 mm at each end is discarded as start and end transients
PITCH = 2.0
GROUP_N = 9                        # tracks per mount piece
GROUP_GAP = 10.0                   # between the two groups' facing tracks: room for the bandsaw cut
X_MID = CENTRE                     # the target plane: every track's mid-length
ROW_X = ((X_MID - TRACK_LEN / 2, X_MID + TRACK_LEN / 2),)
_SPAN = 2 * (GROUP_N - 1) * PITCH + GROUP_GAP
TRACK_Y = tuple(CENTRE - _SPAN / 2 + PITCH * k + (GROUP_GAP - PITCH) * (k >= GROUP_N) for k in range(2 * GROUP_N))
INSERTS = ("A", "B", "C", "D")
SEED = 100                         # issue #100; example randomization only


def pilot_sets() -> list[dict]:
    """The 64 Sobol power-speed sets (P in W, v in mm/s), each with its panel and line energy P/v in J/mm."""
    with open(SOBOL_CSV) as fh:
        return [dict(id=r["id"], panel=r["panel"], P=float(r["P"]), v=float(r["v"]), E=float(r["P"]) / float(r["v"]))
                for r in csv.DictReader(fh)]


def grid_sets() -> list[dict]:
    """All of the pilot's power-speed sets (kept under its old name for screens.py): the 64 Sobol settings."""
    return pilot_sets()


def track_map(seed: int = SEED) -> list[dict]:
    """72 tracks: each panel carries its own 16-point Sobol block and 2 controls, in its own random order.

    Returns one dict per track with insert (the panel), row (always 1: one row per panel), k (0..17 along y), group
    (1 for the first nine, 2 for the rest: the mount piece it ends up in), the block-coordinate start and end points,
    the parameter set (P, v, E; None for controls) and its exposure order on the plate (0..71)."""
    rng = np.random.default_rng(seed)
    all_sets = pilot_sets()
    out = []
    order = 0
    x0, x1 = ROW_X[0]
    for ins in INSERTS:
        sets = [s for s in all_sets if s["panel"] == ins] + [dict(id=CONTROL, P=None, v=None, E=None)] * 2
        perm = rng.permutation(len(sets))
        for k, j in enumerate(perm):                                 # exposure order: low y first
            s = sets[j]
            out.append(dict(insert=ins, row=1, k=k, group=1 + (k >= GROUP_N), start=(x0, TRACK_Y[k]),
                            end=(x1, TRACK_Y[k]), set=s["id"], P=s["P"], v=s["v"], E=s["E"], order=order))
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
            {s["id"] for s in pilot_sets() if s["panel"] == ins} | {CONTROL}))
    Es = [s["E"] for s in grid_sets()]
    print("P/v range", min(Es), max(Es))
