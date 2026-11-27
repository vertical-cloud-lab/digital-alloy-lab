"""Edison LITERATURE_HIGH queries for the first-principles keyhole model (PR #249, issue #235).

Sterling asked (PR #249) for our own keyhole and melt-pool model written from first principles, with
properties taken from databases and papers, each cited. These three queries ask Edison for what that
model needs, submitted in parallel:

* ``properties``: temperature-dependent properties of liquid and solid Al and Al-Si (density, heat
  capacity, enthalpy of fusion, thermal conductivity, electrical resistivity, surface tension,
  viscosity, vapour pressure, enthalpy of vaporisation) and optical constants near 1.07 um.
* ``models``: physics-based keyhole models (energy balance at the keyhole wall, conical keyhole,
  front-wall drilling, point-plus-line sources, recoil pressure, multiple reflections), their
  equations and how well they predict measured keyhole depths.
* ``absorptance``: measured absorptance against keyhole depth or aspect ratio, to check a ray tracer.

Usage (run from the repo root; needs EDISON_PLATFORM_API_KEY):

    python scripts/edison_keyhole_first_principles.py submit   # writes _task_ids.json
    python scripts/edison_keyhole_first_principles.py wait     # blocks until all finish, then fetches
    python scripts/edison_keyhole_first_principles.py fetch    # fetch whatever has finished

The report-fetching code is shared with scripts/edison_keyhole_alternatives.py. ``wait`` keeps its
sleep inside Python, so in GitHub Actions it can run as one foreground call (see CLAUDE.md).
"""

from __future__ import annotations

import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import edison_keyhole_alternatives as base  # noqa: E402
from edison_client import JobNames, TaskRequest  # noqa: E402

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "edison-trajectories" / "keyhole-first-principles"

CONTEXT = (
    "Context: we are writing our own physics-based (first-principles, no parameters fitted to keyhole "
    "data) model of laser keyholing and keyhole-mode melt-pool size for laser powder bed fusion of "
    "AlSi10Mg and a hypereutectic Al-24Si-0.14Mg (wt%) blend, to replace the Thermo-Calc Additive "
    "Manufacturing Module where conduction models (Eagar-Tsai) fail. Settings: 1070 nm fibre laser, "
    "Gaussian beam with 1/e^2 radius 40-45 um, 75-400 W, 0.3-2.4 m/s, 30-150 C plate. The model has "
    "three parts: (1) absorptivity from the Drude-Fresnel optics of the liquid metal with multiple "
    "reflections ray-traced inside the keyhole; (2) the keyhole's depth and shape from an energy "
    "balance at a wall held near the boiling point (moving line/point sources, Kaplan-style local "
    "conduction, evaporation losses, recoil pressure against surface tension); (3) the melt pool as "
    "the liquidus isotherm of the resulting sources. We will check it against Gan et al. 2021 "
    "(Nat. Commun. 12, 2379) X-ray keyhole depths for Ti-6Al-4V, Al6061 and SS316, and against the "
    "AM Module's maps. "
)

QUERIES = {
    "properties": {
        "title": "Temperature-dependent properties of liquid and solid Al and Al-Si for a keyhole model",
        "outfile": "properties.md",
        "query": CONTEXT + (
            "Question: what are the best critically evaluated or directly measured values, as functions "
            "of temperature, for liquid and solid aluminium and Al-Si alloys (Al-7Si to Al-25Si, "
            "AlSi10Mg) of: (a) density; (b) specific heat capacity and enthalpy, including the enthalpy "
            "of fusion and its split over the freezing range; (c) thermal conductivity, solid through "
            "liquid; (d) electrical resistivity, solid, at melting, and liquid up to as high a "
            "temperature as measured (pulse-heating data near the boiling point if any); (e) surface "
            "tension and its temperature coefficient, including the effect of Si and of oxygen; "
            "(f) viscosity; (g) saturated vapour pressure (Clausius-Clapeyron or Antoine coefficients) "
            "and enthalpy of vaporisation, and Mg's effect on the vapour; (h) optical constants n and k, "
            "or normal-incidence absorptance, near 1.06-1.07 um for solid and liquid Al and Al-Si. "
            "For each, give the equation or numbers, the temperature range, the uncertainty, the "
            "method (levitation, pulse heating, sessile drop, ellipsometry, ...), and the paper with its "
            "DOI. Prefer reference compilations (e.g. J. Phys. Chem. Ref. Data, Int. J. Thermophys., "
            "Metall. Mater. Trans.) and say where sources disagree. Finish with one table of "
            "recommended values for a model at 1 atm."
        ),
    },
    "models": {
        "title": "Physics-based keyhole models: equations, assumptions and measured-depth errors",
        "outfile": "models.md",
        "query": CONTEXT + (
            "Question: which physics-based reduced-order keyhole models predict keyhole depth and shape "
            "without fitting to keyhole data, and how well? Cover: Kaplan's point-by-point energy "
            "balance at the keyhole wall (J. Phys. D 1994) and his later Fresnel-absorption analysis; "
            "the conical keyhole of Lankalapalli, Tu and Gartner (J. Phys. D 1996); the front-wall "
            "drilling model of Fabbro and Chouf (J. Appl. Phys. 2000) and Fabbro's later scaling of "
            "keyhole depth; the point-plus-line source of Steen, Dowden and Davis (1988); the "
            "recoil-pressure energy balance of Semak and Matsunawa (1997); recoil pressure as about "
            "0.54 of the saturated vapour pressure and the 18 % back-flux (Anisimov 1968; Knight 1979); "
            "multiple-reflection absorptivity of a cavity (Gouffe; ray tracing). For each give the "
            "governing equations with their symbols, the assumptions (wall temperature, cross-section "
            "shape, latent heat, evaporation), and any quantitative comparison with measured keyhole "
            "depths, especially in-situ X-ray depths in LPBF (Cunningham 2019, Gan 2021, Simonds 2021) "
            "and for aluminium alloys. Which assumption most limits accuracy at LPBF scales "
            "(beam radius 40-70 um, 0.3-1.5 m/s)? Give DOIs."
        ),
    },
    "absorptance": {
        "title": "Measured absorptance against keyhole depth and aspect ratio",
        "outfile": "absorptance.md",
        "query": CONTEXT + (
            "Question: what direct measurements of laser absorptance during spot or line melting relate "
            "the absorbed fraction to the depression or keyhole depth, width or aspect ratio, for "
            "aluminium alloys (Al6061, AlSi10Mg, pure Al) and for comparison Ti-6Al-4V, 316L and IN625? "
            "Include integrating-sphere measurements made together with X-ray imaging (e.g. Simonds et "
            "al. 2021, Applied Materials Today), calorimetry (Trapp et al. 2017; Ye et al. 2019), and "
            "any keyhole-mode absorptance for Al at 1 um. Give the numbers: power, speed or dwell, spot "
            "size, measured absorptance, depression depth and width, and the reported relation (for "
            "example absorptance against depth/width), with DOIs, so that a ray-tracing absorptivity "
            "model can be checked against them. Also: what flat-surface absorptance at 1.06-1.07 um "
            "has been measured for liquid aluminium, and does a Drude model reproduce it?"
        ),
    },
}

base.OUT_DIR = OUT_DIR
base.RAW_DIR = OUT_DIR / "raw"
base.TASK_FILE = OUT_DIR / "_task_ids.json"
base.QUERIES = QUERIES
base.PROMPT_SCRIPT = "scripts/edison_keyhole_first_principles.py"


def submit() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if base.TASK_FILE.exists():
        sys.exit(f"{base.TASK_FILE} already exists; refusing to resubmit")
    c = base.client()
    record = {"job": JobNames.LITERATURE_HIGH.value,
              "submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tasks": {}}
    for key, q in QUERIES.items():
        task_id = c.create_task(TaskRequest(name=JobNames.LITERATURE_HIGH, query=q["query"]))
        record["tasks"][key] = {"task_id": str(task_id), "title": q["title"], "outfile": q["outfile"]}
        print(f"submitted {key}: {task_id}", flush=True)
        base.TASK_FILE.write_text(json.dumps(record, indent=2) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "submit":
        submit()
    elif cmd == "fetch":
        base.fetch()
    elif cmd == "wait":
        base.wait(max_s=int(sys.argv[2]) if len(sys.argv) > 2 else 3300)
    else:
        sys.exit(__doc__)
