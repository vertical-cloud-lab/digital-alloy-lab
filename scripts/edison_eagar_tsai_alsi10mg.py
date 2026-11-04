"""Edison LITERATURE_HIGH queries for eagar-tsai inputs for AlSi10Mg (issue #235).

Two queries, submitted in parallel:

* ``beam``: ranges for the four ``eagar_tsai.BeamParameters`` inputs
  (beam_diameter, power, velocity, absorptivity) for LPBF of AlSi10Mg on an
  Aconity MIDI.
* ``material``: the four ``eagar_tsai.MaterialProperties`` inputs
  (liquidus_temperature, thermal_conductivity, density, specific_heat) for
  AlSi10Mg, evaluated at the liquidus.

Usage (run from the repo root; needs EDISON_PLATFORM_API_KEY):

    python scripts/edison_eagar_tsai_alsi10mg.py submit   # writes _task_ids.json
    python scripts/edison_eagar_tsai_alsi10mg.py wait     # blocks until both finish, then fetches
    python scripts/edison_eagar_tsai_alsi10mg.py fetch    # fetch whatever has finished

``wait`` keeps its sleep inside Python, so in GitHub Actions it can run as a
single foreground call (see CLAUDE.md).
"""

from __future__ import annotations

import json
import os
import pathlib
import sys
import time

from edison_client import EdisonClient, JobNames, TaskRequest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "edison-trajectories" / "eagar-tsai-alsi10mg-inputs"
RAW_DIR = OUT_DIR / "raw"
TASK_FILE = OUT_DIR / "_task_ids.json"
TERMINAL = {"success", "fail", "failed", "cancelled", "error"}

ET_CONTEXT = (
    "Context: we are setting up the Eagar-Tsai analytical melt-pool model (a travelling Gaussian "
    "surface heat source on a semi-infinite solid with constant properties; Eagar & Tsai 1983, "
    "Welding Journal) for laser powder bed fusion (LPBF / PBF-LB/M) of AlSi10Mg. We will compare "
    "its predictions against the Thermo-Calc AM Module and against single-track melt-pool "
    "cross-sections (width and depth) that we will print on an Aconity MIDI open-architecture "
    "LPBF system at the University of Utah. The implementation is the ArroyaveLab `eagar-tsai` "
    "Python package. It takes four beam/process inputs, beam_diameter (m), power (W), velocity "
    "(m/s) and absorptivity (dimensionless, in (0, 1]), and four material inputs evaluated at the "
    "liquidus temperature: liquidus_temperature (K), thermal_conductivity (W/(m K)), density "
    "(kg/m^3) and specific_heat (J/(kg K)). Its beam_diameter is defined as 2*sigma, where sigma "
    "is the standard deviation of the Gaussian heat-source distribution, so it equals HALF of the "
    "commonly quoted 1/e^2 (D4sigma = 4*sigma) spot diameter and about 0.85x the FWHM."
)

QUERIES: dict[str, dict[str, str]] = {
    "beam": {
        "title": "Eagar-Tsai beam/process parameter ranges for AlSi10Mg LPBF on an Aconity MIDI",
        "outfile": "beam-parameter-ranges.md",
        "query": (
            "What input ranges should we use for the four Eagar-Tsai beam/process parameters "
            "(beam diameter, laser power, scan velocity, absorptivity) when modelling laser powder "
            "bed fusion of AlSi10Mg on an Aconity MIDI? "
            + ET_CONTEXT
            + "\n\nPlease answer each part with citations and DOIs:\n"
            "1. Aconity MIDI hardware: the laser source options (maximum power, wavelength, "
            "single-mode vs multimode fibre laser), the focused spot-size range and whether the spot "
            "can be varied (z-shifter / defocus), and the maximum scan speed. Compare with the "
            "machines most used in the AlSi10Mg LPBF literature (EOS M290/M400, SLM Solutions "
            "SLM 280/500, Concept Laser M2, Renishaw AM 400, TRUMPF TruPrint, 3D Systems ProX DMP, "
            "AconityMINI/AconityLAB).\n"
            "2. Laser power and scan velocity for AlSi10Mg: (a) the full range explored in "
            "single-track and density-cube studies; (b) the typical dense-part (>=99.5% relative "
            "density) processing window and common vendor default parameter sets (e.g., EOS "
            "AlSi10Mg 30 um and 60 um layer parameters); (c) a power-velocity printability-map "
            "sweep range wide enough to span the lack-of-fusion, balling and keyhole regimes. "
            "Report scan speed in both mm/s and m/s.\n"
            "3. Beam diameter: the spot sizes reported in AlSi10Mg studies, stating which "
            "definition each source uses (1/e^2 diameter, FWHM, 2*sigma, or unspecified), and "
            "convert each to the eagar-tsai 2*sigma convention. Note studies that deliberately use "
            "large or defocused spots.\n"
            "4. Absorptivity at ~1060-1080 nm for AlSi10Mg and other Al alloys, separated into: "
            "(a) flat, polished solid; (b) liquid aluminium; (c) measured powder-bed absorptance "
            "(integrating-sphere or calorimetric measurements, e.g. Trapp et al. 2017, and ray-"
            "tracing calculations such as Boley et al. 2015); (d) keyhole-mode effective "
            "absorptivity and how it rises with energy density; (e) effective values back-"
            "calibrated by fitting Eagar-Tsai, Rosenthal or finite-element models to measured "
            "AlSi10Mg melt-pool widths and depths. Explain how the oxide film, multiple scattering "
            "in the powder layer, and Mg evaporation affect it, and what values the Thermo-Calc "
            "AM Module and CALPHAD-based printability-map studies (e.g. Johnson et al. 2019 Acta "
            "Materialia; Whalen et al. 2021; Sheikh et al. 2024 npj Computational Materials) used "
            "for aluminium alloys.\n\n"
            "Finish with a summary table, one row per eagar-tsai input (beam_diameter in um and in "
            "m under the 2*sigma convention, power in W, velocity in m/s, absorptivity), giving: "
            "minimum, typical/recommended value for AlSi10Mg on an Aconity MIDI, maximum, a "
            "recommended sweep range for a power-velocity printability map, and the supporting "
            "sources with DOIs. Flag which numbers are strongly versus weakly supported."
        ),
    },
    "material": {
        "title": "AlSi10Mg thermophysical properties for the Eagar-Tsai model (at the liquidus)",
        "outfile": "material-properties.md",
        "query": (
            "What are the liquidus temperature, thermal conductivity, density and specific heat "
            "of AlSi10Mg (Al with 9-11 wt% Si and 0.2-0.45 wt% Mg; EN AC-43000 family) that we "
            "should use as constant inputs to the Eagar-Tsai melt-pool model, evaluated at the "
            "liquidus temperature? "
            + ET_CONTEXT
            + "\n\nPlease answer each part with citations and DOIs:\n"
            "1. Liquidus temperature, solidus temperature and Al-Si eutectic temperature of "
            "AlSi10Mg: measured values (DSC/DTA, on heating and cooling) and CALPHAD values "
            "(equilibrium and Scheil, e.g. Thermo-Calc TCAL), and how they vary across the "
            "composition specification.\n"
            "2. Thermal conductivity: room-temperature values for as-cast, LPBF as-built, "
            "stress-relieved/annealed and T6 conditions (and anisotropy with build direction); "
            "the temperature dependence up to the solidus; and the liquid value at or just above "
            "the liquidus. State the measurement method (laser-flash diffusivity x density x "
            "specific heat, Wiedemann-Franz from electrical resistivity, etc.).\n"
            "3. Density: room-temperature solid, temperature-dependent solid, and liquid density "
            "at the liquidus (with any linear fit rho(T)).\n"
            "4. Specific heat: room-temperature and temperature-dependent solid values, the "
            "liquid value near the liquidus, the latent heat of fusion, and the effective or "
            "apparent specific heat that some LPBF models use to fold latent heat into cp.\n"
            "5. The values that published LPBF melt-pool models have used for AlSi10Mg (or "
            "near-eutectic Al-Si alloys): Eagar-Tsai or Rosenthal analytical models, printability "
            "maps, finite-element and CFD (e.g. FLOW-3D) simulations, and Thermo-Calc AM Module, "
            "Thermo-Calc property-model or JMatPro calculations.\n\n"
            "Finish with a summary table, one row per property (liquidus_temperature in K, "
            "thermal_conductivity in W/(m K), density in kg/m^3, specific_heat in J/(kg K)), "
            "giving: a recommended single value for an Eagar-Tsai model evaluated at the liquidus, "
            "a plausible range, the temperature/state it refers to, the method (measured vs "
            "CALPHAD vs assumed), and sources with DOIs. Where sources disagree, explain why "
            "(condition, porosity, temperature, method) and flag which numbers are strongly "
            "versus weakly supported."
        ),
    },
}


def client() -> EdisonClient:
    key = os.environ.get("EDISON_PLATFORM_API_KEY")
    if not key:
        sys.exit("EDISON_PLATFORM_API_KEY is not set")
    return EdisonClient(api_key=key)


def load_ids() -> dict:
    return json.loads(TASK_FILE.read_text())


def submit() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if TASK_FILE.exists():
        sys.exit(f"{TASK_FILE} already exists; refusing to resubmit")
    c = client()
    record = {"job": JobNames.LITERATURE_HIGH.value, "submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tasks": {}}
    for key, q in QUERIES.items():
        task_id = c.create_task(TaskRequest(name=JobNames.LITERATURE_HIGH, query=q["query"]))
        record["tasks"][key] = {"task_id": str(task_id), "title": q["title"], "outfile": q["outfile"]}
        print(f"submitted {key}: {task_id}", flush=True)
    TASK_FILE.write_text(json.dumps(record, indent=2) + "\n")


def _dig(obj, *path):
    for p in path:
        if isinstance(obj, dict) and p in obj:
            obj = obj[p]
        else:
            return None
    return obj


def fetch_one(c: EdisonClient, key: str, meta: dict) -> str:
    task = c.get_task(task_id=meta["task_id"], verbose=True)
    status = str(task.status)
    if status != "success":
        return status
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    dump = task.model_dump(mode="json")
    (RAW_DIR / f"{key}-task-verbose.json").write_text(json.dumps(dump, indent=2, default=str) + "\n")

    # Pull the answer out of the environment frame (PaperQA3 layout), with fallbacks.
    frame = dump.get("environment_frame") or {}
    answer = (
        _dig(frame, "state", "state", "response", "answer")
        or _dig(frame, "state", "response", "answer")
        or {}
    )
    formatted = (answer.get("formatted_answer") if isinstance(answer, dict) else None) or ""
    plain = (answer.get("answer") if isinstance(answer, dict) else None) or ""
    references = (answer.get("references") if isinstance(answer, dict) else None) or ""
    if not formatted:
        # Lite/simple response as a last resort.
        simple = c.get_task(task_id=meta["task_id"])
        dump_simple = simple.model_dump(mode="json")
        formatted = dump_simple.get("formatted_answer") or dump_simple.get("answer") or ""
    header = (
        "<!--\n"
        f"Edison Scientific LITERATURE_HIGH report: {meta['title']}\n"
        f"Job: {JobNames.LITERATURE_HIGH.value} (LITERATURE_HIGH)\n"
        f"Task ID: {meta['task_id']}\n"
        f"Created: {dump.get('created_at')}  Status: {status}\n"
        "Retrieved with edison-client from GitHub Actions for issue #235.\n"
        "Prompt: QUERIES['" + key + "'] in scripts/edison_eagar_tsai_alsi10mg.py\n"
        "-->\n\n"
    )
    body = formatted or plain
    if references and references not in body:
        body += "\n\n## References\n\n" + references
    (OUT_DIR / meta["outfile"]).write_text(header + body.strip() + "\n")
    return status


def fetch() -> dict[str, str]:
    c = client()
    ids = load_ids()
    out = {}
    for key, meta in ids["tasks"].items():
        out[key] = fetch_one(c, key, meta)
        print(f"{key}: {out[key]}", flush=True)
    return out


def wait(poll_s: int = 120, max_s: int = 3300) -> None:
    c = client()
    ids = load_ids()
    start = time.time()
    pending = set(ids["tasks"])
    while pending and time.time() - start < max_s:
        for key in sorted(pending):
            meta = ids["tasks"][key]
            status = str(c.get_task(task_id=meta["task_id"]).status)
            print(f"[{int(time.time() - start):5d}s] {key}: {status}", flush=True)
            if status in TERMINAL:
                print(f"  -> fetch {key}: {fetch_one(c, key, meta)}", flush=True)
                pending.discard(key)
        if pending:
            time.sleep(poll_s)
    if pending:
        print(f"still pending after {max_s}s: {sorted(pending)}", flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "submit":
        submit()
    elif cmd == "fetch":
        fetch()
    elif cmd == "wait":
        wait(max_s=int(sys.argv[2]) if len(sys.argv) > 2 else 3300)
    else:
        sys.exit(__doc__)
