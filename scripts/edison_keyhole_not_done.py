"""Edison LITERATURE_HIGH queries for the first-principles keyhole model's open items (PR #249, issue #235).

Sterling asked (PR #249) for the first-principles model's "not done" items: Mg evaporation, a powder layer, a
tilted keyhole, melt flow, the blend's liquid resistivity above 12 wt% Si, sourced liquid resistivities for Gan
et al.'s alloys, and a sourced solid conductivity. These three queries ask Edison for leads to the numbers those
need. Nothing Edison says is used unless it is checked in the source.

* ``resistivity``: liquid electrical resistivity of hypereutectic Al-Si, Ti-6Al-4V, 316L and Al6061.
* ``conductivity_viscosity``: solid thermal conductivity of LPBF AlSi10Mg and hypereutectic Al-Si against
  temperature; liquid Al and Al-Si viscosity and surface-tension coefficient.
* ``mg_powder``: Mg evaporation from Al alloys in laser processing, and powder-bed absorptance of Al alloys.

Usage (run from the repo root; needs EDISON_PLATFORM_API_KEY):

    python scripts/edison_keyhole_not_done.py submit   # writes _task_ids.json
    python scripts/edison_keyhole_not_done.py wait     # blocks until all finish, then fetches
    python scripts/edison_keyhole_not_done.py fetch    # fetch whatever has finished
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
OUT_DIR = REPO_ROOT / "edison-trajectories" / "keyhole-not-done"

CONTEXT = (
    "Context: we have written our own physics-based keyhole and melt-pool model for laser powder bed fusion "
    "(1070 nm fibre laser, Gaussian beam 1/e^2 radius 40-45 um, 75-400 W, 0.3-2.4 m/s) of AlSi10Mg and a "
    "hypereutectic Al-24.3Si-0.14Mg (wt%) blend. It uses Drude-Fresnel optics of the liquid from its measured "
    "electrical resistivity, a ray tracer for multiple reflections in the keyhole, an energy balance at a keyhole "
    "wall at the boiling point, and CALPHAD enthalpies. We are now adding Mg evaporation, a powder layer, a "
    "tilted keyhole whose shape comes from a point-by-point wall energy balance, and Marangoni melt flow, and "
    "we need sourced inputs. "
)

QUERIES = {
    "resistivity": {
        "title": "Liquid electrical resistivity of hypereutectic Al-Si, Ti-6Al-4V, 316L and Al6061",
        "outfile": "resistivity.md",
        "query": CONTEXT + (
            "Question: what measured electrical resistivity data exist for (a) liquid Al-Si alloys above 12 wt% "
            "Si (hypereutectic, ideally up to 25-30 wt% Si or across the whole Al-Si system, including liquid Si), "
            "with the temperature coefficient; (b) liquid Ti-6Al-4V near melting and as high in temperature as "
            "measured (pulse heating, e.g. Boivineau et al. 2006); (c) liquid 316 or 316L stainless steel "
            "(pulse heating or levitation, e.g. the Graz group); (d) liquid Al6061 or Al-Mg-Si alloys. For each, "
            "give the numbers or the fitted equation, the temperature range, whether it is corrected for thermal "
            "expansion, the method and uncertainty, and the paper with its DOI and the table or figure number."
        ),
    },
    "conductivity_viscosity": {
        "title": "Solid conductivity of LPBF AlSi10Mg and hypereutectic Al-Si; liquid Al-Si viscosity",
        "outfile": "conductivity_viscosity.md",
        "query": CONTEXT + (
            "Question: (a) what is the measured thermal conductivity, as a function of temperature from room "
            "temperature to the solidus, of as-built laser powder bed fusion AlSi10Mg (laser flash diffusivity "
            "with density and heat capacity), and how does heat treatment change it? (b) the same for "
            "hypereutectic Al-Si alloys with 17-30 wt% Si (cast, spray formed, or LPBF Al-20Si / Al-25Si / A390), "
            "and for pure Si; (c) the dynamic viscosity of liquid Al and liquid Al-Si alloys (up to 25 wt% Si) "
            "against temperature, with reference correlations (e.g. Assael et al. 2006, J. Phys. Chem. Ref. Data) "
            "and the Arrhenius parameters; (d) the temperature coefficient of surface tension for Al-Si and "
            "AlSi10Mg melts, with and without oxygen. Give numbers, temperature ranges, methods, and DOIs with "
            "table or figure numbers."
        ),
    },
    "mg_powder": {
        "title": "Mg evaporation from Al alloys under a laser, and powder-bed absorptance of Al alloys",
        "outfile": "mg_powder.md",
        "query": CONTEXT + (
            "Question: (a) how is selective Mg evaporation from Al-Mg and Al-Si-Mg melts modelled and measured "
            "under laser welding and LPBF: the Mg activity coefficient in liquid Al, the Langmuir and Knudsen-"
            "layer flux, diffusion-limited depletion of Mg at the surface, and measured Mg loss (e.g. Zhao and "
            "DebRoy 2001 for Al 5182; Mg loss in LPBF AlSi10Mg and in Al 5xxx keyhole welding)? Does Mg vapour "
            "lower the keyhole wall temperature, and by how much? Give the diffusion coefficient of Mg in liquid "
            "Al with its source. (b) What absorptance has been measured or computed at 1.06-1.07 um for powder "
            "layers of AlSi10Mg, Al-Si or Al (integrating sphere, calorimetry, ray tracing such as Boley et al. "
            "2015, radiation transfer such as Gusarov and Kruth 2005), and how does it depend on layer thickness, "
            "packing density and particle size? Give the extinction coefficient formula used for packed beds of "
            "opaque spheres and typical AlSi10Mg powder-layer packing densities. Give DOIs with table or figure "
            "numbers."
        ),
    },
}

base.OUT_DIR = OUT_DIR
base.RAW_DIR = OUT_DIR / "raw"
base.TASK_FILE = OUT_DIR / "_task_ids.json"
base.QUERIES = QUERIES
base.PROMPT_SCRIPT = "scripts/edison_keyhole_not_done.py"


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
