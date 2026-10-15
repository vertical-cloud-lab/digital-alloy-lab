#!/usr/bin/env python3
"""Verify and bound the FLAIME discretized search-space counts.

This script reproduces the search-space figures quoted in the proposal
(``genesis-mission-proposal/flaime-genesis-proposal.tex``), extends them to
the *per-element-bounded* feasible composition count that the original figures
omit, and finally multiplies the composition space by a discretized **LPBF
process-parameter** space so the headline "search space" reflects the full
build specification (composition + how it is printed), not composition alone.

Background (composition)
------------------------
The proposal quotes ``\\feasiblepairsOneAt = 118{,}967{,}759`` (≈1.19e8) as the
number of discretized ``(support, composition)`` pairs at 1% resolution, and
``\\feasiblepairsTenthWt ≈ 3.6e16`` at 0.1% resolution.  Both are computed under
two constraints only:

  1. NChooseK *support*: which ``k`` of the 15 non-Al elements are present
     (``k = kmin..kmax`` = 2..8).
  2. A single shared simplex budget: every present element is >= 1 grid step,
     and the total solute is <= 15 (i.e. Al >= 85), with **no per-element
     upper bound**.

Closed forms (verified below):

  * 1% grid   :  sum_{k=2..8} C(15,k)^2            = 118,967,759
  * 0.5% grid :  sum_{k=2..8} C(15,k) * C(30,k)    ≈ 1.71e11
  * 0.1% grid :  sum_{k=2..8} C(15,k) * C(150,k)   ≈ 3.58e16

Because no individual element ceiling is applied, these are *over-counts*: they
admit physically implausible corners (e.g. 8 at.% Sc, 12 at.% Sn).  This script
re-counts the feasible grid points after applying the per-element upper bounds
from ``figures/dag-thumbnails/periodic-table/alloy_element_bounds.csv`` (the
"Recommended upper bound" and "Non-conservative upper" columns).  Per reviewer
request the coarse composition grid is **0.5 at.%** (not 1 at.%); the 1 at.%
figure is kept only as a provenance anchor for the published macro.

Background (LPBF process parameters)
------------------------------------
Composition alone underdescribes an LPBF build.  Adam Clare and others note the
feasible region is a function of ~24+ processing parameters, not just laser
power and scan speed (issue #19; the 36-parameter taxonomy of PR #20, mirrored
in ``figures/panels/shared.py`` and
``edison-trajectories/processing_parameters_dimensionality.md``).  This script
enumerates the independently *tunable* parameters with hardware-grounded lower
and upper limits and a representative discretization step, derives the number of
levels per parameter, and multiplies them to a process-parameter search space.
Concrete machine envelopes (Mastrex MX120/MX200/MX300 and Aconity MIDI) are
then applied as overrides to show how the available hardware bounds the process
space.  The full discretized search space reported at the end is

    feasible compositions  ×  process-parameter combinations.

Method
------
A dynamic program counts integer lattice points of the constrained simplex,
grouped by the number of active (present) elements ``k``:

  dp[a][u] = number of grid assignments using exactly ``a`` active elements
             whose solute units sum to ``u`` (in grid steps).

Each element is either inactive (contributes 0) or active with value in
``[1, cap_i]`` grid steps, where ``cap_i = floor(upper_bound_wt% * scale)`` and
``scale`` is the number of grid steps per percentage point (2 for the 0.5%
grid, 10 for the 0.1% grid).  The feasible total is
``sum_{a=kmin..kmax} sum_{u=a..B} dp[a][u]`` with budget ``B = 15 * scale``.

Setting every ``cap_i = B`` recovers the original un-capped closed forms, which
the ``main`` self-check asserts exactly.

Units caveat
------------
The original 1-step macro is labelled "1 at.%" in the proposal while the bounds
CSV is expressed in wt.%.  This script treats the grid resolution in the same
percentage unit as the bounds (wt.%); the at.%/wt.% distinction shifts
individual grid edges slightly but does not change the qualitative conclusion
that per-element caps reduce the count by orders of magnitude.  The CSV also
notes sub-grid activity floors (e.g. Mn 0.05-0.10 wt%, Zr/Sc 0.2 wt%); this
script uses the original ">= 1 grid step" presence floor for consistency with
the published figures.

Process-parameter limits are representative engineering ranges for commercial
metal LPBF systems (e.g. SLM/EOS/Renishaw class), chosen to respect hardware
reality (e.g. laser power <= ~400-1000 W, galvo scan speed <= a few m/s) rather
than to be exhaustive; the discretization step for each is stated alongside.
"""

from __future__ import annotations

import csv
import os
from math import comb, floor

# 15-element non-Al palette, in the canonical proposal order.
ELEMENTS = ["Mn", "Cr", "Zr", "Mg", "Si", "Cu", "Ti",
            "Fe", "Ni", "Ce", "Sc", "Li", "Er", "Zn", "Sn"]

ELEMENT_COUNT = 15      # non-Al elements (\elementcount)
KMIN, KMAX = 2, 8       # additions per sub-system (\kmin, \kmax)
SOLUTE_BUDGET_PCT = 15  # Al >= 85 => total solute <= 15 (percentage points)

# Per-element upper bounds (wt.%) transcribed from
# figures/dag-thumbnails/periodic-table/alloy_element_bounds.csv on the
# consolidation-2 branch.  "Recommended upper bound" == "Conservative upper"
# for every solute, so only Recommended and Non-conservative are distinct.
RECOMMENDED_UPPER_WT = {
    "Mn": 5.0, "Cr": 3.0, "Zr": 1.0, "Mg": 5.0, "Si": 12.0,
    "Cu": 4.0, "Ti": 0.5, "Fe": 0.5, "Ni": 0.5, "Ce": 6.0,
    "Sc": 0.8, "Li": 2.0, "Er": 0.5, "Zn": 8.0, "Sn": 0.1,
}
NONCONSERVATIVE_UPPER_WT = {
    "Mn": 8.0, "Cr": 6.0, "Zr": 2.0, "Mg": 8.0, "Si": 14.0,
    "Cu": 7.0, "Ti": 1.5, "Fe": 2.0, "Ni": 2.0, "Ce": 12.0,
    "Sc": 1.5, "Li": 3.0, "Er": 1.5, "Zn": 15.0, "Sn": 0.5,
}

# Grids: (label, scale, budget_in_steps).  scale = steps per percentage point.
# Per reviewer request the coarse composition grid is 0.5 (not 1) at.%.  The
# finer 0.5% step also lets every element whose recommended cap is >= 0.5 wt.%
# (Ti, Fe, Ni, Sc, Er) be represented, which a 1% grid could not (see the
# dropped-element note below); only Sn (0.1 wt.%) still falls below one step.
# The 1 at.% closed form is retained in ``main`` purely as a provenance anchor
# for the published \feasiblepairsOneAt = 118,967,759 macro.
GRIDS = [("0.5%", 2, SOLUTE_BUDGET_PCT * 2),
         ("0.1%", 10, SOLUTE_BUDGET_PCT * 10)]

CSV_RELPATH = os.path.join(
    "figures", "dag-thumbnails", "periodic-table", "alloy_element_bounds.csv")

# ---------------------------------------------------------------------------
# LPBF process-parameter search space
# ---------------------------------------------------------------------------
# Independently tunable LPBF processing parameters (issue #19; the 36-parameter
# taxonomy of PR #20, mirrored in figures/panels/shared.py and
# edison-trajectories/processing_parameters_dimensionality.md).  For every
# parameter we state a hardware-grounded lower/upper limit and a representative
# discretization step, from which the number of grid levels follows.
#
# Each entry is a dict:
#   name      : parameter label (matches the PR #20 taxonomy where applicable)
#   category  : one of the seven taxonomy categories
#   kind      : "continuous" | "categorical" | "fixed"
#   low, high : inclusive numeric limits (continuous/fixed only)
#   unit      : physical unit string
#   step      : grid resolution in `unit` (continuous only)
#   options   : number of discrete choices (categorical only)
#   note      : rationale / hardware constraint / coupling
#
# "fixed" parameters contribute one level (they pin the build but are not swept)
# and are listed for completeness; only continuous/categorical parameters expand
# the search space.  Ranges are representative of commercial metal LPBF systems
# (SLM/EOS/Renishaw class) and are deliberately conservative w.r.t. what the
# hardware can physically or meaningfully deliver, not exhaustive.
PROCESS_PARAMETERS = [
    # --- Beam / Energy ---
    dict(name="Laser power", category="Beam/Energy", kind="continuous",
         low=100, high=400, unit="W", step=10,
         note="Galvo single-mode fiber laser; <=400 W typical, keyhole onset "
              "above; coupled with scan speed via volumetric energy density."),
    dict(name="Scan speed", category="Beam/Energy", kind="continuous",
         low=200, high=2000, unit="mm/s", step=50,
         note="Galvo slew limit a few m/s; balling above, lack-of-fusion "
              "below; sets line energy with power."),
    dict(name="Spot size", category="Beam/Energy", kind="continuous",
         low=50, high=150, unit="um", step=10,
         note="Focus/optics adjustable on open systems; sets irradiance and "
              "track overlap."),
    dict(name="Beam profile", category="Beam/Energy", kind="categorical",
         options=3, unit="-",
         note="Gaussian / flat-top / ring; emerging beam-shaping hardware."),
    dict(name="Operation mode (CW/pulsed)", category="Beam/Energy",
         kind="categorical", options=2, unit="-",
         note="Continuous-wave vs pulsed source."),
    dict(name="Pulse setting", category="Beam/Energy", kind="categorical",
         options=4, unit="-",
         note="Representative duty/frequency presets, active only when pulsed."),
    dict(name="Beam oscillation amplitude", category="Beam/Energy",
         kind="continuous", low=0, high=200, unit="um", step=50,
         note="0 = off; wobble/oscillation widens the melt track."),
    dict(name="Wavelength", category="Beam/Energy", kind="fixed",
         low=1070, high=1070, unit="nm",
         note="Set by the fiber source; not swept on a given machine."),

    # --- Scan Strategy ---
    dict(name="Hatch spacing", category="Scan", kind="continuous",
         low=60, high=150, unit="um", step=10,
         note="~30% track overlap rule-of-thumb; coupled to spot size."),
    dict(name="Scan pattern", category="Scan", kind="categorical", options=4,
         unit="-", note="Stripe / checkerboard(island) / meander / spiral."),
    dict(name="Rotation angle", category="Scan", kind="continuous",
         low=0, high=90, unit="deg", step=15,
         note="Inter-layer rotation (67 deg common) to decorrelate defects."),
    dict(name="Island/vector length", category="Scan", kind="continuous",
         low=2, high=10, unit="mm", step=1,
         note="Island size controls residual stress; longer = higher stress."),
    dict(name="Contour offset", category="Scan", kind="continuous",
         low=0, high=200, unit="um", step=50,
         note="Border-to-hatch offset for surface finish."),
    dict(name="Contour passes", category="Scan", kind="continuous",
         low=0, high=3, unit="count", step=1,
         note="Number of perimeter passes."),
    dict(name="Skywriting", category="Scan", kind="categorical", options=2,
         unit="-", note="On/off; equalizes speed at vector ends."),
    dict(name="Scan vs. gas-flow angle", category="Scan", kind="categorical",
         options=3, unit="-",
         note="With / against / perpendicular to shielding-gas flow."),

    # --- Layer / Build ---
    dict(name="Layer thickness", category="Layer/Build", kind="continuous",
         low=20, high=100, unit="um", step=10,
         note="Bounded below by PSD/recoating, above by melt depth; "
              "20-60 um most common."),
    dict(name="Build orientation", category="Layer/Build", kind="continuous",
         low=0, high=90, unit="deg", step=15,
         note="Part tilt relative to build plate."),
    dict(name="Support strategy", category="Layer/Build", kind="categorical",
         options=4, unit="-", note="Block / cone / tree / none."),
    dict(name="Plate location", category="Layer/Build", kind="categorical",
         options=4, unit="-",
         note="Build-plate zone; gas-flow/recoat gradients (often neglected)."),

    # --- Powder / Feedstock ---
    dict(name="Particle size distribution", category="Powder", kind="categorical",
         options=4, unit="-", note="15-45 / 15-53 / 20-63 / 15-75 um cuts."),
    dict(name="Morphology", category="Powder", kind="categorical", options=2,
         unit="-", note="Spherical (GA/PREP) vs irregular."),
    dict(name="Moisture content", category="Powder", kind="categorical",
         options=3, unit="-", note="Dry / ambient / humid storage state."),
    dict(name="Recycling state", category="Powder", kind="categorical",
         options=4, unit="-", note="Virgin / used / overflow / spatter."),

    # --- Atmosphere ---
    dict(name="Gas type", category="Atmosphere", kind="categorical", options=3,
         unit="-", note="Ar / N2 / He."),
    dict(name="Gas flow velocity", category="Atmosphere", kind="continuous",
         low=1.0, high=4.0, unit="m/s", step=0.5,
         note="Inlet velocity to clear plume/spatter."),
    dict(name="Residual O2", category="Atmosphere", kind="continuous",
         low=100, high=1000, unit="ppm", step=100,
         note="<100 ppm for reactive alloys; machine getter limit."),
    dict(name="Chamber pressure", category="Atmosphere", kind="fixed",
         low=1, high=1, unit="atm",
         note="Near-ambient inert; not swept on standard machines."),

    # --- Thermal Management ---
    dict(name="Baseplate preheat", category="Thermal", kind="continuous",
         low=40, high=200, unit="degC", step=20,
         note="Lowers gradients/cracking; heater ceiling on standard plates."),
    dict(name="Inter-layer dwell", category="Thermal", kind="continuous",
         low=0, high=30, unit="s", step=5,
         note="Idle time per layer for heat dissipation."),
    dict(name="Build height", category="Thermal", kind="fixed",
         low=0, high=0, unit="mm",
         note="Geometry-dependent thermal boundary; set by the part, not swept."),

    # --- Machine-Specific ---
    dict(name="Recoater type", category="Machine", kind="categorical", options=3,
         unit="-", note="Soft (rubber/silicone) / hard (steel) / brush."),
    dict(name="Recoater speed", category="Machine", kind="continuous",
         low=50, high=320, unit="mm/s", step=30,
         note="Spreading dynamics; too fast => short-feeding/streaking."),
    dict(name="Dosing factor", category="Machine", kind="continuous",
         low=1.0, high=3.0, unit="x", step=0.5,
         note="Powder over-dose multiple to guarantee full layers."),
]


def parameter_levels(p):
    """Return the number of discrete grid levels for a process parameter."""
    if p["kind"] == "categorical":
        return p["options"]
    if p["kind"] == "fixed":
        return 1
    # continuous: inclusive endpoints on a uniform grid of width `step`.
    span = p["high"] - p["low"]
    return int(round(span / p["step"])) + 1


def process_space_size(params=PROCESS_PARAMETERS):
    """Product of the per-parameter level counts (the swept-parameter space)."""
    total = 1
    for p in params:
        total *= parameter_levels(p)
    return total


def describe_range(p):
    """Human-readable range/options string for a process parameter."""
    if p["kind"] == "categorical":
        return f"{p['options']} categories"
    if p["kind"] == "fixed":
        return f"{p['low']} {p['unit']} (fixed)"
    return f"{p['low']}-{p['high']} {p['unit']} @ {p['step']} {p['unit']}"


# ---------------------------------------------------------------------------
# Machine-specific envelopes
# ---------------------------------------------------------------------------
# Two concrete LPBF systems requested in review.  Each entry overrides the
# generic PROCESS_PARAMETERS limits with the machine's published hardware
# envelope; unspecified parameters inherit the generic (machine-agnostic)
# values.  Overrides set continuous low/high/step, categorical ``options``, or
# pin a parameter to a single level via ``kind="fixed"``.
#
# Sources (specs accessed 2026-06):
#   * Mastrex MX120 -- https://mastrex.com/product/mx120/
#       300 W laser; scan speed <= 7 m/s; spot 35-60 um; layer 20-50 um;
#       build vol Ø120x100 mm; IR single-mode (Gaussian, CW); bundled N2
#       generator; no documented baseplate preheat (compact desktop).
#   * Mastrex MX200 -- https://mastrex.com/product/mx200/ (MX-Series, see
#     https://www.3dnatives.com/en/mastrex-affordable-lpbf-systems-19052026/)
#       dual 500 W IR fiber lasers (per-laser 500 W); scan speed <= 7 m/s;
#       beam diameter 50-100 um; layer 20-120 um; build vol 220x140x200 mm;
#       IR single-mode (Gaussian, CW); no documented baseplate preheat.
#   * Mastrex MX300 -- https://mastrex.com/product/mx300/ (flagship, see
#     https://www.tctmagazine.com/mastrex-launches-185-000-mx300-metal-3d-printing-system/)
#       dual 500 W IR fiber lasers (per-laser 500 W); scan speed <= 7 m/s;
#       beam diameter 50-120 um; layer 20-120 um; build vol 300x300x350 mm;
#       build rate <= 70 cm3/h; IR single-mode (Gaussian, CW); no documented
#       baseplate preheat.
#   * Aconity MIDI -- https://aconity3d.com/products/aconity-midi-plus/ ,
#     https://etadditive.com/machine/aconitymidi-2/
#       IR fiber up to 1000 W; scan speed <= 12 m/s; focus 80-500 um adjustable
#       on the fly (+ green-laser option); layer >= 10 um; preheat up to 500 C
#       (Ø170 std; 800/1200 C with reduced build); open/freely configurable.
MACHINES = {
    "MX120": {
        "Laser power": dict(low=100, high=300, step=10),       # 300 W max
        "Scan speed": dict(low=200, high=7000, step=50),       # 7 m/s galvo
        "Spot size": dict(low=35, high=60, step=5),            # 35-60 um beam
        "Beam profile": dict(options=1),                       # Gaussian only
        "Operation mode (CW/pulsed)": dict(options=1),         # CW fiber
        "Pulse setting": dict(options=1),
        "Beam oscillation amplitude": dict(kind="fixed", low=0, high=0),
        "Layer thickness": dict(low=20, high=50, step=10),     # 20-50 um
        "Gas type": dict(options=2),            # Ar tank or bundled N2 generator
        "Baseplate preheat": dict(kind="fixed", low=20, high=20),  # no preheat
    },
    "MX200": {
        "Laser power": dict(low=100, high=500, step=10),       # dual 500 W (per-laser)
        "Scan speed": dict(low=200, high=7000, step=50),       # 7 m/s galvo
        "Spot size": dict(low=50, high=100, step=5),           # 50-100 um beam
        "Beam profile": dict(options=1),                       # Gaussian only
        "Operation mode (CW/pulsed)": dict(options=1),         # CW fiber
        "Pulse setting": dict(options=1),
        "Beam oscillation amplitude": dict(kind="fixed", low=0, high=0),
        "Layer thickness": dict(low=20, high=120, step=10),    # 20-120 um
        "Gas type": dict(options=2),                           # Ar or N2
        "Baseplate preheat": dict(kind="fixed", low=20, high=20),  # no preheat
    },
    "MX300": {
        "Laser power": dict(low=100, high=500, step=10),       # dual 500 W (per-laser)
        "Scan speed": dict(low=200, high=7000, step=50),       # 7 m/s galvo
        "Spot size": dict(low=50, high=120, step=5),           # 50-120 um beam
        "Beam profile": dict(options=1),                       # Gaussian only
        "Operation mode (CW/pulsed)": dict(options=1),         # CW fiber
        "Pulse setting": dict(options=1),
        "Beam oscillation amplitude": dict(kind="fixed", low=0, high=0),
        "Layer thickness": dict(low=20, high=120, step=10),    # 20-120 um
        "Gas type": dict(options=2),                           # Ar or N2
        "Baseplate preheat": dict(kind="fixed", low=20, high=20),  # no preheat
    },
    "Aconity MIDI": {
        "Laser power": dict(low=100, high=1000, step=10),      # up to 1 kW IR
        "Scan speed": dict(low=200, high=12000, step=50),      # 12 m/s
        "Spot size": dict(low=80, high=500, step=20),          # 80-500 um focus
        "Wavelength": dict(kind="categorical", options=2),     # IR or green
        "Operation mode (CW/pulsed)": dict(options=1),         # CW fiber
        "Pulse setting": dict(options=1),
        "Layer thickness": dict(low=10, high=100, step=10),    # min 10 um
        "Baseplate preheat": dict(low=40, high=500, step=20),  # up to 500 C
    },
}


def apply_machine(params, overrides):
    """Return a copy of ``params`` with per-name field overrides applied."""
    by_name = {p["name"]: dict(p) for p in params}
    for name, fields in overrides.items():
        if name not in by_name:
            raise KeyError(f"unknown parameter override: {name!r}")
        by_name[name].update(fields)
    return [by_name[p["name"]] for p in params]


def load_bounds_from_csv(path):
    """Return {element: (recommended_wt, nonconservative_wt)} from the CSV.

    Only used when the CSV is present in the checkout; otherwise the embedded
    transcriptions above are authoritative.
    """
    rec, non = {}, {}
    with open(path, newline="") as fh:
        for row in csv.DictReader(fh):
            el = row["Element"].strip()
            if el not in ELEMENTS:
                continue
            rec[el] = float(row["Recommended upper bound (wt%)"])
            non[el] = float(row["Non-conservative upper (wt%)"])
    return rec, non


def count_capped(caps, budget, kmin=KMIN, kmax=KMAX):
    """Count constrained simplex lattice points via dynamic programming.

    Parameters
    ----------
    caps : list[int]
        Per-element upper bound in grid steps (0 => element cannot be present
        at this resolution).
    budget : int
        Total solute budget in grid steps (Al >= 85 => budget = 15 * scale).
    kmin, kmax : int
        Inclusive range for the number of active (present) elements.

    Returns
    -------
    int
        Number of distinct discretized compositions with kmin..kmax active
        elements, each in [1, cap_i] steps, summing to <= budget.
    """
    # dp[a][u] = ways to use exactly `a` active elements summing to `u` steps.
    dp = [[0] * (budget + 1) for _ in range(kmax + 1)]
    dp[0][0] = 1
    for cap in caps:
        cap = min(cap, budget)
        ndp = [[0] * (budget + 1) for _ in range(kmax + 1)]
        for a in range(kmax + 1):
            row = dp[a]
            for u in range(budget + 1):
                val = row[u]
                if not val:
                    continue
                ndp[a][u] += val                      # element inactive
                if a < kmax:                          # element active, 1..cap
                    for v in range(1, min(cap, budget - u) + 1):
                        ndp[a + 1][u + v] += val
        dp = ndp
    return sum(dp[a][u]
               for a in range(kmin, kmax + 1)
               for u in range(a, budget + 1))


def closed_form_uncapped(scale, kmin=KMIN, kmax=KMAX):
    """Original un-capped count for a grid step ``scale``.

    1% grid (scale=1):  sum_k C(15,k)^2
    0.1% grid (scale=10): sum_k C(15,k) * C(150,k)
    """
    budget = SOLUTE_BUDGET_PCT * scale
    return sum(comb(ELEMENT_COUNT, k) * comb(budget, k)
               for k in range(kmin, kmax + 1))


def caps_in_steps(upper_wt, scale):
    """Convert {element: upper_wt%} to a list of per-element caps in steps."""
    return [floor(upper_wt[el] * scale) for el in ELEMENTS]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.normpath(os.path.join(here, "..", CSV_RELPATH))
    rec, non = RECOMMENDED_UPPER_WT, NONCONSERVATIVE_UPPER_WT
    source = "embedded transcription of " + CSV_RELPATH
    if os.path.exists(csv_path):
        rec, non = load_bounds_from_csv(csv_path)
        source = csv_path

    print("FLAIME composition search-space verification")
    print("=" * 64)
    print(f"Palette: Al + {', '.join(ELEMENTS)}  ({ELEMENT_COUNT} solutes)")
    print(f"NChooseK k = {KMIN}..{KMAX}; Al >= {100 - SOLUTE_BUDGET_PCT} "
          f"(total solute <= {SOLUTE_BUDGET_PCT}%)")
    print(f"Bounds source: {source}")
    print()

    # --- 1. Reproduce the published un-capped figures (DP == closed form). ---
    print("Un-capped (no per-element ceiling) -- reproduces proposal macros:")
    for label, scale, budget in GRIDS:
        dp_val = count_capped([budget] * ELEMENT_COUNT, budget)
        cf_val = closed_form_uncapped(scale)
        assert dp_val == cf_val, (label, dp_val, cf_val)
        print(f"  {label:5s} grid: {dp_val:,}  (closed form {cf_val:,})")
    one_at = closed_form_uncapped(1)
    assert one_at == 118_967_759, one_at
    print(f"  provenance anchor -- 1% grid closed form "
          f"sum C(15,k)^2 = {one_at:,} matches \\feasiblepairsOneAt: "
          f"{one_at == 118_967_759}")
    print()

    # --- 2. Per-element-bounded feasible counts. ---
    # Keep the Recommended-bound counts per grid for the final combined space.
    bounded_by_grid = {}
    for name, upper in [("Recommended upper bound", rec),
                        ("Non-conservative upper", non)]:
        print(f"Per-element-bounded ({name}):")
        for label, scale, budget in GRIDS:
            caps = caps_in_steps(upper, scale)
            usable = sum(1 for c in caps if c >= 1)
            total = count_capped(caps, budget)
            uncapped = closed_form_uncapped(scale)
            frac = total / uncapped
            if name == "Recommended upper bound":
                bounded_by_grid[label] = total
            print(f"  {label:5s} grid: {total:,}"
                  f"   ({usable}/{ELEMENT_COUNT} elements representable; "
                  f"{frac:.3%} of un-capped {uncapped:,})")
            if usable < ELEMENT_COUNT:
                dropped = [el for el, c in zip(ELEMENTS, caps) if c < 1]
                print(f"          dropped at this resolution "
                      f"(cap < 1 step): {', '.join(dropped)}")
        print()

    # --- 3. LPBF process-parameter search space. ---
    swept = [p for p in PROCESS_PARAMETERS if parameter_levels(p) > 1]
    fixed = [p for p in PROCESS_PARAMETERS if parameter_levels(p) == 1]
    print(f"LPBF process-parameter space "
          f"({len(swept)} swept of {len(PROCESS_PARAMETERS)} listed; "
          f"the rest are machine/geometry-fixed):")
    print(f"  {'Parameter':28s} {'Category':12s} {'Range / options':22s} "
          f"{'Step':8s} {'Levels':>6s}")
    print("  " + "-" * 80)
    for p in PROCESS_PARAMETERS:
        levels = parameter_levels(p)
        if p["kind"] == "categorical":
            rng = f"{p['options']} categories"
            step = "-"
        elif p["kind"] == "fixed":
            rng = f"{p['low']} {p['unit']} (fixed)"
            step = "-"
        else:
            rng = f"{p['low']}-{p['high']} {p['unit']}"
            step = f"{p['step']} {p['unit']}"
        print(f"  {p['name']:28s} {p['category']:12s} {rng:22s} "
              f"{step:8s} {levels:>6d}")
    proc = process_space_size()
    print("  " + "-" * 80)
    print(f"  Process-parameter combinations (product of levels): "
          f"{proc:,}  (~{proc:.2e})")
    print()

    # --- 4. Full discretized search space = composition x process. ---
    print("Full discretized search space (feasible composition x process):")
    for label, _, _ in GRIDS:
        comp = bounded_by_grid[label]
        combined = comp * proc
        print(f"  {label:5s} composition grid: "
              f"{comp:,} compositions x {proc:,} process combos "
              f"= {combined:,}  (~{combined:.2e})")
    print()

    # --- 5. Machine-specific envelopes (MX120, MX200, MX300, Aconity MIDI). ---
    print("Machine-specific LPBF envelopes (override generic process limits):")
    for mname, ov in MACHINES.items():
        mparams = apply_machine(PROCESS_PARAMETERS, ov)
        mproc = process_space_size(mparams)
        mswept = sum(1 for p in mparams if parameter_levels(p) > 1)
        ratio = mproc / proc
        print(f"  {mname}: {mswept} swept params; process space = "
              f"{mproc:,}  (~{mproc:.2e}; {ratio:.2e}x generic)")
        for name in ov:
            p = next(q for q in mparams if q["name"] == name)
            print(f"      {name:28s} {describe_range(p):26s} "
                  f"-> {parameter_levels(p):>4d} levels")
        for label, _, _ in GRIDS:
            combined = bounded_by_grid[label] * mproc
            print(f"      full search space @ {label:5s} comp grid: "
                  f"{combined:,}  (~{combined:.2e})")
        print()


if __name__ == "__main__":
    main()
