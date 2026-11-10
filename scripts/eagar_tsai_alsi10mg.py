"""Run ArroyaveLab/eagar-tsai for AlSi10Mg with the Edison-sourced inputs (issue #235).

Inputs come from the two Edison LITERATURE_HIGH reports in
edison-trajectories/eagar-tsai-alsi10mg-inputs/ (see README.md there for the
sources behind each number). Outputs go to the same folder:

* alsi10mg-temperature-field.png  single point at the nominal parameter set
* alsi10mg-sensitivity.csv        one-at-a-time sweep of each input over its range
* alsi10mg-printability-map.png  power-velocity map over the recommended sweep

Install and run (Python >= 3.12; eagar-tsai is GPL-3.0, so keep it out of this repo):

    python -m venv /tmp/etvenv && /tmp/etvenv/bin/pip install "eagar-tsai[plot]" pandas
    /tmp/etvenv/bin/python scripts/eagar_tsai_alsi10mg.py
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")

import pandas as pd
from eagar_tsai import (
    BeamParameters,
    MaterialProperties,
    PrintabilityParameters,
    SimulationDomain,
    compute_single_point,
)
from eagar_tsai.plot import plot_printability_map

OUT = pathlib.Path(__file__).resolve().parent.parent / "edison-trajectories" / "eagar-tsai-alsi10mg-inputs"

# ---------------------------------------------------------------------------
# Inputs (SI units, eagar-tsai conventions). beam_diameter is 2*sigma, i.e.
# HALF of the 1/e^2 spot diameter that machine datasheets quote.
# ---------------------------------------------------------------------------
# Beam: Edison beam report, summary table (central values). 40 um = the MIDI's
# 80 um focused spot (assumed 1/e^2) / 2.
NOMINAL_BEAM = dict(beam_diameter=40e-6, power=300.0, velocity=1.0, absorptivity=0.25)

# Material: two candidate sets from the Edison material report.
#  * "edison_practical": the report's closing recommendation (k and rho near the
#    solidus, cp of the liquid). Used as the nominal set.
#  * "liquid_at_liquidus": every property for the liquid at 867 K (Pelevin et al.
#    2025), matching eagar-tsai's "evaluated at the liquidus" convention. k is
#    alpha_l * rho*cp = (1.88e-5 + 6.43e-9 * 867) * 2.6e6 = 63 W/(m K); Edison's
#    report says 53, which is an arithmetic slip.
MATERIAL_SETS = {
    "edison_practical": dict(liquidus_temperature=867.0, thermal_conductivity=110.0, density=2650.0, specific_heat=1040.0),
    "liquid_at_liquidus": dict(liquidus_temperature=867.0, thermal_conductivity=63.0, density=2500.0, specific_heat=1040.0),
}
NOMINAL_MATERIAL = MATERIAL_SETS["edison_practical"]

# (low, high) for the one-at-a-time sensitivity sweep, from the two reports.
RANGES = {
    "beam_diameter": (25e-6, 50e-6),  # 50-100 um 1/e^2 focused spots across machines
    "power": (200.0, 370.0),  # dense-part window
    "velocity": (0.8, 1.3),  # dense-part window
    "absorptivity": (0.15, 0.35),  # Edison sensitivity cases
    "liquidus_temperature": (860.0, 870.0),
    "thermal_conductivity": (63.0, 155.0),  # liquid at liquidus .. cast/annealed solid
    "density": (2500.0, 2670.0),  # liquid at liquidus .. room-temperature solid
    "specific_heat": (920.0, 1365.0),  # solid near 400 C .. effective cp with latent heat
}

# Printability-map sweep (Edison beam report) and fixed process settings.
# Layer and hatch are NOT from the Edison reports: 30 um layer and 190 um hatch
# are the EOS AlSi10Mg 30 um defaults the beam report mentions without a citation.
MAP_POWER = (50.0, 400.0)  # W
MAP_VELOCITY = (0.1, 2.5)  # m/s
LAYER_THICKNESS = 30e-6  # m
HATCH_SPACING = 190e-6  # m


def run(beam_kw: dict, mat_kw: dict, domain: SimulationDomain):
    r = compute_single_point(BeamParameters(**beam_kw), MaterialProperties(**mat_kw), domain)
    return {
        "length_um": round(r.length_um, 1),
        "width_um": round(r.width_um, 1),
        "depth_um": round(r.depth_um, 1),
        "peak_T_K": round(r.peak_temperature),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    domain = SimulationDomain(x_length_um=600.0, y_length_um=300.0, z_depth_um=200.0, spatial_resolution_um=2.0)

    # 1. Nominal single point + temperature field figure.
    beam = BeamParameters(**NOMINAL_BEAM)
    material = MaterialProperties(**NOMINAL_MATERIAL)
    result = compute_single_point(beam, material, domain)
    result.plot(output=str(OUT / "alsi10mg-temperature-field.png"))
    print(
        f"nominal: L={result.length_um:.1f} um  W={result.width_um:.1f} um  "
        f"D={result.depth_um:.1f} um  Tpeak={result.peak_temperature:.0f} K"
    )

    # 2. One-at-a-time sensitivity over each input's range.
    rows = [{"input": "nominal", "value": "", **run(NOMINAL_BEAM, NOMINAL_MATERIAL, domain)}]
    for set_name, props in MATERIAL_SETS.items():
        rows.append({"input": f"material set: {set_name}", "value": "", **run(NOMINAL_BEAM, props, domain)})
    for name, (lo, hi) in RANGES.items():
        for val in (lo, hi):
            b, m = dict(NOMINAL_BEAM), dict(NOMINAL_MATERIAL)
            (b if name in b else m)[name] = val
            rows.append({"input": name, "value": val, **run(b, m, domain)})
    # The beam-diameter convention trap: entering the 1/e^2 spot (4 sigma) instead of 2 sigma.
    b = dict(NOMINAL_BEAM, beam_diameter=2 * NOMINAL_BEAM["beam_diameter"])
    rows.append({"input": "beam_diameter entered as 1/e^2 spot (2x)", "value": b["beam_diameter"], **run(b, NOMINAL_MATERIAL, domain)})
    sens = pd.DataFrame(rows)
    sens.to_csv(OUT / "alsi10mg-sensitivity.csv", index=False)
    print(sens.to_string(index=False))

    # 3. Power-velocity printability map (Sheikh et al. 2024 criteria, as implemented in eagar-tsai).
    process = PrintabilityParameters(
        beam_diameter_m=NOMINAL_BEAM["beam_diameter"],
        absorptivity=NOMINAL_BEAM["absorptivity"],
        layer_thickness_m=LAYER_THICKNESS,
        hatch_spacing_m=HATCH_SPACING,
    )
    map_domain = SimulationDomain(x_length_um=600.0, y_length_um=300.0, z_depth_um=200.0, spatial_resolution_um=5.0)
    fig = plot_printability_map(
        process,
        material,
        power_range=MAP_POWER,
        velocity_range=MAP_VELOCITY,
        n_power=25,
        n_velocity=25,
        domain=map_domain,
        workers=-1,
        output=str(OUT / "alsi10mg-printability-map.png"),
    )
    del fig


if __name__ == "__main__":
    main()
