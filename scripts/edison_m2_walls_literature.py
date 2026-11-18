"""Edison literature queries for the M2 stepped-wall build (issue #100, PR #243, 2026-11-18).

Carl's first M2 build is 84 thin walls (7 a part, 3 parts on each of 4 panels), each wall with its own hatch power
and speed, sectioned for cross-section SEM and compared with the Thermo-Calc AM Module. These queries look for
what the build should show, what has already been measured or simulated that it can be compared against, what the
AM Module needs from experiments, and how to prepare and image the sections without artefacts.

LITERATURE_HIGH queries (deep, cited reports):

* ``window``: expected porosity and melt-pool depth versus P and v for 316L at a 100-130 um spot; published
  process maps and data tables, especially from Concept Laser M2 machines (LLNL), to compare against.
* ``walls``: thin walls (about 1.3 mm) as parameter-screening specimens: heat build-up, short vectors, contours,
  whether a wall's core matches bulk porosity, orientation to the recoater and gas flow, place on the plate.
* ``ammodule``: what the Thermo-Calc AM Module computes, how it has been validated (316L and others), which
  observables it was calibrated on, and which experiments would help refine it.
* ``metallography``: sectioning, mounting, polishing, unetched porosity imaging, etching 316L for melt-pool
  boundaries and cells, pore classification, area and fields needed, pitfalls.
* ``calibration``: how melt-pool and printability models have been calibrated against experiments (Bayesian
  calibration, GP emulators, batch BO), what experiment designs separate absorptivity from spot size, and whether a
  second spot size is worth adding.
* ``solidification``: 316L solidification under LPBF: primary mode, CALPHAD/Scheil predictions, cell spacing versus
  cooling rate, segregation, and what etched SEM can measure that the AM Module also predicts.

PRECEDENT queries ("has anyone done this?"):

* ``precedent_walls``: per-wall parameters on thin-wall or comb specimens compared with a CALPHAD printability map.
* ``precedent_tc``: the Thermo-Calc AM Module validated against measured 316L melt pools or porosity.

Usage (run from the repo root; needs EDISON_PLATFORM_API_KEY):

    python scripts/edison_m2_walls_literature.py submit   # writes _task_ids.json
    python scripts/edison_m2_walls_literature.py wait     # blocks until all finish, then fetches (sleep in Python)
    python scripts/edison_m2_walls_literature.py fetch    # fetch whatever has finished

``wait`` keeps its sleep inside Python, so in GitHub Actions it runs as a single foreground call (see CLAUDE.md).
Structure copied from scripts/edison_m2_track_design.py.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import sys
import time

from edison_client import EdisonClient, JobNames, TaskRequest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "edison-trajectories" / "m2-walls-literature"
RAW_DIR = OUT_DIR / "raw"
TASK_FILE = OUT_DIR / "_task_ids.json"
TERMINAL = {"success", "fail", "failed", "cancelled", "error"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

CONTEXT = (
    "Context: laser powder bed fusion (PBF-LB/M, L-PBF) of commercial gas-atomized 316L stainless steel powder "
    "(about 15-45 um) on a Concept Laser M2 cusing (CL WRX Control 2.4; two 400 W class continuous-wave Yb fibre "
    "lasers at about 1070 nm, only one used; galvanometer scanner; nitrogen or argon; no plate heating; layer "
    "thickness 30 or 50 um, not yet confirmed). The machine's production 316L parameter set uses, for the core "
    "hatch, 370 W, 1350 mm/s, 0.09 mm hatch spacing and a 130 um spot (P/v = 0.274 J/mm), contours at 100-120 W "
    "and 130-220 mm/s with a 50-70 um spot, and an upskin at 200 W, 980 mm/s, 0.075 mm hatch. "
    "The build: 12 'comb' parts, each a 44.5 x 12.7 mm base (printed with the production set) carrying 7 thin "
    "walls (fins) 1.27 mm thick, 12.7 mm long and 7.6 mm tall on a 7.2 mm pitch. Every wall has its own core and "
    "upskin laser power P and scan speed v (contours unchanged): 60 settings from a scrambled Sobol sequence over "
    "P = 150-370 W and P/v = 0.09-0.55 J/mm (v about 335-2930 mm/s; about 33-204 J/mm^3 at 30 um layers), plus "
    "the production hatch as a control. Three parts stand on each of four removable 88 mm square 316L panels; the "
    "fourth panel is turned 90 degrees so its walls run across the recoater instead of along it, and repeats 18 "
    "settings and the control, giving 21 pairs printed in both orientations. After the build each part is cut "
    "lengthwise near its centreline and between walls 4 and 5, hot-mounted in 1.25 in conductive mounts, ground "
    "to the centreline (a section through every wall's thickness and height at mid-length), polished, imaged "
    "unetched in an SEM (Thermo Fisher Apreo C) for porosity in each wall's core (at least 0.2 mm from the faces, "
    "1 mm from the base and the top), then etched to reveal the last layer's melt-pool boundaries. The results "
    "will be compared with the Thermo-Calc Additive Manufacturing (AM) Module (CALPHAD-based properties; "
    "steady-state and transient melt-pool calculations; printability maps of lack of fusion, keyholing and "
    "balling), to calibrate and test it, and later builds will choose settings by batch Bayesian optimization."
)

ASK = (
    "\n\nAnswer with citations and DOIs. Quote numbers with the conditions they apply to (material, P, v, spot "
    "size and how it was defined, hatch spacing, layer thickness, machine, gas). Prefer primary sources, say "
    "where sources disagree, and flag which statements are strongly versus weakly supported. Where a paper gives "
    "a data table or an open dataset we could compare against, say exactly where (table or figure number, "
    "repository and identifier)."
)

QUERIES: dict[str, dict[str, str]] = {
    "window": {
        "job": "LITERATURE_HIGH",
        "title": "Expected porosity and melt-pool depth for 316L across P 150-370 W, v 335-2930 mm/s at a 100-130 um spot",
        "outfile": "expected-316l-window.md",
        "query": (
            "What porosity (or relative density) and melt-pool depth should we expect from LPBF 316L stainless "
            "steel across laser power 150-370 W and scan speed 335-2930 mm/s with a 100-130 um spot and 0.09 mm "
            "hatch spacing, and which published measurements and process maps can our results be compared "
            "against? " + CONTEXT + ASK + "\n\nIn particular:\n"
            "1. Published 316L process maps and density data in or near this window, especially from Concept "
            "Laser M2 machines (for example the Lawrence Livermore National Laboratory work: density of 316L at "
            "powers up to 400 W, keyhole-mode melting, and the related single-track and Eagar-Tsai/normalized-"
            "enthalpy analyses), and from other machines with a similar spot (EOS M280/M290, SLM 280, Renishaw). "
            "Give the P, v, h, t, spot and the measured density or porosity, and where the lack-of-fusion and "
            "keyhole boundaries fell.\n"
            "2. Where the lack-of-fusion boundary sits in volumetric energy density, in P/v, and in "
            "dimensionless terms (normalized enthalpy dH/h_s, keyhole number, Tang et al.'s overlap criterion); "
            "how sharp it is; and how porosity rises below it.\n"
            "3. Where keyhole porosity starts for 316L at spots of 50-130 um, and whether a 130 um spot at up to "
            "370 W can keyhole at all at these speeds.\n"
            "4. How much porosity and melt-pool depth scatter between nominally identical specimens or "
            "positions on the plate (repeatability), so we know what difference between two walls is real.\n"
            "5. Open datasets (MeltpoolNet, NIST, LLNL, Zenodo, Materials Data Facility, Mendeley Data, journal "
            "supplements) with 316L P, v, spot, hatch, layer and porosity or melt-pool dimensions."
        ),
    },
    "walls": {
        "job": "LITERATURE_HIGH",
        "title": "Thin walls (about 1.3 mm) as LPBF parameter-screening specimens: what they show and what goes wrong",
        "outfile": "thin-walls-as-screening-specimens.md",
        "query": (
            "Do thin LPBF walls about 1.3 mm thick, each printed with its own core laser power and scan speed "
            "inside standard contours, give porosity and melt-pool depth that represent bulk material printed "
            "with the same parameters? What changes in a thin wall, and what can go wrong? " + CONTEXT + ASK
            + "\n\nIn particular:\n"
            "1. Heat accumulation in thin walls and small cross-sections: measured or simulated temperature rise "
            "layer by layer, its effect on melt-pool depth and porosity, and how it depends on wall thickness, "
            "height, P/v, layer time and the number of parts per layer.\n"
            "2. Short hatch vectors: if the hatch runs across a 1 mm wide core, every vector is about 1 mm long; "
            "how scanner acceleration, turnaround, skywriting and laser on/off delays change porosity "
            "(turnaround pores) and melt-pool depth; versus vectors along a 12.7 mm wall. Concept Laser's island "
            "scanning strategy and how it treats a narrow part.\n"
            "3. Contour and hatch interaction: porosity near the contour-hatch interface, keyhole pores from "
            "slow, focused contour scans, and how far inside the faces the core is free of contour effects.\n"
            "4. Published high-throughput parameter screening with thin walls, fins, combs, stepped or 'tree' "
            "specimens, pins or small cubes on one plate: how well the result matched bulk density cubes.\n"
            "5. Orientation of thin walls to the recoater and to the gas flow: recoater collision, wall "
            "deflection or swelling, powder-layer thickness next to walls, spatter landing; effects of the part's "
            "position on the plate (gas-flow inlet to outlet, distance from the laser's optical axis, angle of "
            "incidence, focus) on porosity and melt-pool size.\n"
            "6. Minimum wall thickness and height for a meaningful porosity measurement in a polished section, "
            "and where in the wall to measure."
        ),
    },
    "ammodule": {
        "job": "LITERATURE_HIGH",
        "title": "The Thermo-Calc AM Module: what it computes, how it has been validated, and what experiments refine it",
        "outfile": "thermo-calc-am-module-validation.md",
        "query": (
            "What does the Thermo-Calc Additive Manufacturing (AM) Module compute, how has it been validated "
            "against experiments (316L and other alloys), and what experimental data would best help calibrate and "
            "refine it? " + CONTEXT + ASK + "\n\nIn particular:\n"
            "1. The module's physics: steady-state, transient and transient-with-steady-state-heat-source modes; "
            "the heat-source options (Gaussian, double ellipsoid, conical, keyhole model) and how the keyhole "
            "model sets depth and absorptivity; Marangoni flow, evaporation and recoil; the powder layer; "
            "temperature-dependent CALPHAD properties (which databases, e.g. TCFE and TCAM); outputs (melt-pool "
            "width, depth, length, temperature field, thermal gradient G, solidification rate R, cooling rate, "
            "and printability maps from batch calculations with criteria for lack of fusion, keyholing and "
            "balling).\n"
            "2. Published validations and applications: which alloys (316L, 17-4PH, IN625, IN718, Ti-6Al-4V, "
            "AlSi10Mg, others), which machines, which observables (single-track width and depth, NIST AM Bench "
            "data, porosity, printability windows, G and R, cell spacing), and how well it agreed, with numbers.\n"
            "3. What absorptivity values and heat-source settings were calibrated for 316L and steels, and how "
            "they depend on speed, power and keyhole depth.\n"
            "4. Which experiments would best help a modelling group refine the module: single tracks on bare "
            "plate versus on powder; pads or walls; constant P/v at different speeds; spot-size variation; "
            "preheat; repeated specimens; the number of conditions; and what metadata (powder size distribution, "
            "chemistry, layer thickness, spot definition and measurement, measured laser power) they need.\n"
            "5. Comparisons of the AM Module (or similar CALPHAD-coupled melt-pool models) with Eagar-Tsai, "
            "Rosenthal, finite-element or CFD (for example FLOW-3D, ALE3D) predictions for the same conditions."
        ),
    },
    "metallography": {
        "job": "LITERATURE_HIGH",
        "title": "Sectioning, mounting, polishing, imaging and etching LPBF 316L thin walls for porosity and melt pools",
        "outfile": "metallography-sem-porosity-316l.md",
        "query": (
            "What is the best practice for preparing and imaging cross-sections of LPBF 316L thin walls to measure "
            "porosity and last-layer melt-pool depth in an SEM, and which artefacts bias the results? " + CONTEXT
            + ASK + "\n\nIn particular:\n"
            "1. Cutting (abrasive cut-off versus precision diamond saws; kerf; heat damage), conductive hot mounting "
            "and edge retention at the top of a wall, and the grinding and polishing sequence for 316L (SiC grits, "
            "diamond, colloidal silica or alumina, times and loads), including how much material to remove to reach "
            "a plane and how to stop at it.\n"
            "2. How polishing changes measured porosity in 316L: smearing that closes pores, pull-out, rounding of "
            "pore edges, and how to check (repeat polish, comparison with X-ray CT or Archimedes).\n"
            "3. Imaging porosity: optical versus SEM BSE versus SE; magnification and pixel size; the smallest pore "
            "that should be counted; stitched mosaics; how large an area is needed for a given uncertainty at 0.1%, "
            "1% and 5% porosity (ASTM E1245, E2109, ISO/ASTM 52900 family), and how many sections per specimen.\n"
            "4. Segmentation and classification: thresholding methods; classifying lack-of-fusion, keyhole and gas "
            "pores by size, circularity and aspect ratio, with the thresholds used.\n"
            "5. Etching 316L to reveal melt-pool boundaries and the cellular structure for SEM and optical "
            "imaging (electrolytic oxalic acid, aqua regia, Kalling's no. 2, glyceregia, V2A-Beize, Carpenter's): "
            "recipes, times, which works best for melt-pool boundaries, and why porosity must be imaged before "
            "etching.\n"
            "6. Measuring the last layer's melt-pool depth and width in a section through a wall: which pools "
            "count, how the section angle to the scan direction distorts them, and how many pools to average.\n"
            "7. Realistic hands-on time per mount and per SEM image for a set of about 24 mounts."
        ),
    },
    "calibration": {
        "job": "LITERATURE_HIGH",
        "title": "Calibrating melt-pool and printability models with experiments: designs, Bayesian calibration, spot size",
        "outfile": "model-calibration-and-experiment-design.md",
        "query": (
            "How have melt-pool and printability models for LPBF (analytical Eagar-Tsai, CALPHAD-coupled models such "
            "as the Thermo-Calc AM Module, finite-element and CFD) been calibrated and validated against experiments, "
            "and how should a build of 84 walls and later batch Bayesian-optimization builds be designed so the "
            "data best constrain such a model? " + CONTEXT + ASK + "\n\nIn particular:\n"
            "1. Bayesian calibration of melt-pool models (Kennedy-O'Hagan, GP emulators, MCMC) for 316L and other "
            "alloys: which parameters were calibrated (absorptivity, beam radius, effective conductivity, "
            "Marangoni), on which observables, how many experiments, and the remaining discrepancy.\n"
            "2. Printability maps (lack of fusion, keyhole, balling) computed from melt-pool models and checked "
            "against measured porosity: which criteria worked best for steels, and how well the predicted "
            "boundaries matched (for example the Texas A&M printability-map work on Ni-Nb, 316L and martensitic "
            "steels, and the keyhole number of Gan et al. 2021).\n"
            "3. Experiment design for separating absorptivity from spot size and from heat accumulation: varying "
            "the spot (defocus) at fixed P and v, constant P/v at different speeds, bare plate versus powder, "
            "single tracks versus walls versus cubes.\n"
            "4. Should a second spot size (for example 50-80 um, or a defocused 200 um) be added to a first build "
            "that already varies P and v at a 130 um spot, or saved for later? What does the literature on 316L "
            "spot size or defocus (density, melt-pool depth, keyhole onset, productivity) say?\n"
            "5. Batch Bayesian optimization or active learning for LPBF process windows: batch sizes, acquisition "
            "functions, how many builds were needed, and how replicates and hold-out points were handled."
        ),
    },
    "solidification": {
        "job": "LITERATURE_HIGH",
        "title": "316L solidification in LPBF: CALPHAD and Scheil predictions, cell spacing versus cooling rate, what SEM shows",
        "outfile": "solidification-316l-calphad-and-sem.md",
        "query": (
            "What does CALPHAD (equilibrium and Scheil) predict for the solidification of 316L stainless steel, how "
            "does 316L actually solidify in LPBF, and what can etched SEM sections measure that a CALPHAD-based "
            "melt-pool model also predicts? " + CONTEXT + ASK + "\n\nIn particular:\n"
            "1. Liquidus, solidus, freezing range and primary phase (austenite or delta ferrite) for 316L from "
            "CALPHAD (Thermo-Calc TCFE, MatCalc, open databases) and from experiment; Creq/Nieq (Schaeffler, WRC-1992) "
            "and the effect of composition within the 316L specification; suppression of ferrite at LPBF "
            "solidification rates; retained ferrite measured in as-built LPBF 316L.\n"
            "2. Cellular sub-structure: measured cell spacing in as-built LPBF 316L versus cooling rate or G x R "
            "(fitted relations such as lambda = a (G R)^-n, with constants), and how cell size changes from the "
            "melt-pool boundary to the centre and with P and v.\n"
            "3. Microsegregation of Cr, Mo, Ni and Si to the cell walls (TEM, APT, EDS) compared with Scheil "
            "predictions, and oxide inclusions.\n"
            "4. Which etchants and SEM conditions reveal the cells and melt-pool boundaries in 316L.\n"
            "5. How enthalpy, latent heat and temperature-dependent properties of 316L used in melt-pool models "
            "(and in the normalized enthalpy dH/h_s keyhole criterion) were obtained, with values."
        ),
    },
    "precedent_walls": {
        "job": "PRECEDENT",
        "title": "Precedent: per-wall parameters on thin-wall or comb specimens compared with a CALPHAD printability map",
        "outfile": "precedent-per-wall-parameters-vs-printability-map.md",
        "query": (
            "Has anyone printed laser powder bed fusion thin-wall, fin or comb specimens of 316L (or another "
            "steel or nickel alloy) with different laser power and scan speed on each wall of one part, measured "
            "porosity or melt-pool depth in cross-sections of the walls, and compared the results with a "
            "printability map from a melt-pool model (Eagar-Tsai, a CALPHAD-based model such as the Thermo-Calc "
            "Additive Manufacturing Module, or finite-element simulations)? Give the closest examples with DOIs and "
            "what they found."
        ),
    },
    "precedent_tc": {
        "job": "PRECEDENT",
        "title": "Precedent: the Thermo-Calc AM Module validated against measured 316L melt pools or porosity",
        "outfile": "precedent-thermo-calc-am-module-316l.md",
        "query": (
            "Has anyone compared predictions of the Thermo-Calc Additive Manufacturing (AM) Module with measured "
            "melt-pool cross-sections, porosity or printability windows for 316L stainless steel (or other "
            "steels) made by laser powder bed fusion? Give the closest examples with DOIs, the observables "
            "compared, the calibrated absorptivity, and how well the module agreed."
        ),
    },
}


def client() -> EdisonClient:
    key = os.environ.get("EDISON_PLATFORM_API_KEY")
    if not key:
        sys.exit("EDISON_PLATFORM_API_KEY is not set")
    return EdisonClient(api_key=key)


def load_ids(path: pathlib.Path = TASK_FILE) -> dict:
    return json.loads(path.read_text())


def submit(keys: list[str] | None = None) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    record = load_ids() if TASK_FILE.exists() else {
        "submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tasks": {}}
    c = client()
    for key in keys or list(QUERIES):
        if key in record["tasks"]:
            print(f"{key}: already submitted ({record['tasks'][key]['task_id']}), skipping", flush=True)
            continue
        q = QUERIES[key]
        job = getattr(JobNames, q["job"])
        task_id = c.create_task(TaskRequest(name=job, query=q["query"]))
        record["tasks"][key] = {"task_id": str(task_id), "job": job.value, "title": q["title"],
                                "outfile": q["outfile"]}
        print(f"submitted {key} ({q['job']}): {task_id}", flush=True)
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
    # The retrieved paper text carries corresponding-author emails; this repo is public.
    raw = EMAIL_RE.sub("[email redacted]", json.dumps(dump, indent=2, default=str))
    (RAW_DIR / f"{key}-task-verbose.json").write_text(raw + "\n")

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
        simple = c.get_task(task_id=meta["task_id"])
        dump_simple = simple.model_dump(mode="json")
        formatted = dump_simple.get("formatted_answer") or dump_simple.get("answer") or ""
    header = (
        "<!--\n"
        f"Edison Scientific {meta.get('job', '')} report: {meta['title']}\n"
        f"Task ID: {meta['task_id']}\n"
        f"Created: {dump.get('created_at')}  Status: {status}\n"
        "Retrieved with edison-client from GitHub Actions for issue #100 / PR #243.\n"
        "Prompt: QUERIES['" + key + "'] in scripts/edison_m2_walls_literature.py\n"
        "-->\n\n"
    )
    body = EMAIL_RE.sub("[email redacted]", formatted or plain)
    if references and references not in body:
        body += "\n\n## References\n\n" + EMAIL_RE.sub("[email redacted]", references)
    (OUT_DIR / meta["outfile"]).write_text(header + body.strip() + "\n")
    return status


def fetch(path: pathlib.Path = TASK_FILE) -> dict[str, str]:
    c = client()
    ids = load_ids(path)
    out = {}
    for key, meta in ids["tasks"].items():
        out[key] = fetch_one(c, key, meta)
        print(f"{key}: {out[key]}", flush=True)
    return out


def wait(poll_s: int = 120, max_s: int = 3300, path: pathlib.Path = TASK_FILE) -> None:
    c = client()
    ids = load_ids(path)
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
        submit(sys.argv[2:] or None)
    elif cmd == "fetch":
        fetch()
    elif cmd == "wait":
        wait(max_s=int(sys.argv[2]) if len(sys.argv) > 2 else 3300)
    else:
        sys.exit(__doc__)
