"""Edison LITERATURE_HIGH queries for the M2 single-track design (issue #100, PR #243).

Four queries, submitted in parallel:

* ``transients``: how far along a single track the melt pool takes to reach steady state, what happens at the
  end of the track, scanner (galvo) effects at the ends, and so the minimum track length and where to section.
* ``interaction``: how neighbouring single tracks on one powder layer affect each other (denudation, powder
  entrainment, spatter, gas flow, heat), and so the spacing and exposure order.
* ``doe``: Sobol vs. batch Bayesian optimization / active learning for a single-track campaign whose purpose is
  to calibrate and validate the Thermo-Calc AM Module; replicates, along-track variability, sections per track.
* ``ss316l``: constant-property inputs for an Eagar-Tsai model of 316L, and published 316L single-track
  cross-section data (P, v, spot, layer, width, depth) to check that model against.

Usage (run from the repo root; needs EDISON_PLATFORM_API_KEY):

    python scripts/edison_m2_track_design.py submit   # writes _task_ids.json
    python scripts/edison_m2_track_design.py wait     # blocks until all finish, then fetches
    python scripts/edison_m2_track_design.py fetch    # fetch whatever has finished

``wait`` keeps its sleep inside Python, so in GitHub Actions it can run as a single foreground call
(see CLAUDE.md). Pattern copied from scripts/edison_eagar_tsai_alsi10mg.py (PR #238).
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
OUT_DIR = REPO_ROOT / "edison-trajectories" / "m2-single-track-design"
RAW_DIR = OUT_DIR / "raw"
TASK_FILE = OUT_DIR / "_task_ids.json"
TERMINAL = {"success", "fail", "failed", "cancelled", "error"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

CONTEXT = (
    "Context: we are planning single-track laser powder bed fusion (PBF-LB/M, L-PBF) experiments in 316L "
    "stainless steel on a Concept Laser M2 cusing (continuous-wave Yb fibre laser at about 1070 nm, 200 W or "
    "400 W depending on configuration, focused spot about 50-90 um 1/e^2 diameter, galvanometer scanner, "
    "nitrogen or argon shielding gas flowing across the plate). Commercial gas-atomized 316L powder "
    "(about 15-45 um) is spread as ONE powder layer (nominally 30-50 um) on 316L substrate panels "
    "(roughly 80 mm square, bolted flush into a 250 mm build plate), and each track is a single scan vector "
    "with its own laser power P and scan speed v (P about 50-400 W, v about 0.1-3 m/s). Each build holds "
    "tens to about a hundred tracks. After the build we cut the panels with a bandsaw and a precision "
    "abrasive saw, grind to a section plane perpendicular to the scan direction (a transverse cross-section "
    "through all tracks in a row at once), mount, polish, etch and image in an SEM, and measure melt-pool "
    "width, depth below the substrate surface, height above it and area, and classify the regime "
    "(lack of fusion/discontinuous, balling, conduction, transition, keyhole). The measured cross-sections "
    "will be compared with STEADY-STATE single-track predictions of the Thermo-Calc Additive Manufacturing "
    "(AM) Module (CALPHAD-derived properties, Gaussian or keyhole heat source with absorptivity to calibrate), "
    "and with the analytical Eagar-Tsai model (travelling Gaussian surface source, constant properties). "
    "We want to calibrate the model's heat-source parameters on part of the tracks and validate on the rest."
)

QUERIES: dict[str, dict[str, str]] = {
    "transients": {
        "title": "Start and end transients of single LPBF tracks: track length and where to section",
        "outfile": "track-transients-and-length.md",
        "query": (
            "How long must a single laser powder bed fusion track in 316L (or similar steels and Ni alloys) be, and "
            "where along it should a transverse cross-section be taken, so that the section reflects the "
            "steady-state melt pool rather than the start or end of the track? "
            + CONTEXT
            + "\n\nPlease answer each part with citations and DOIs, quoting numbers (distances in um or mm, times "
            "in us or ms, with the P, v, spot size and material they apply to):\n"
            "1. Start transient. How far from the start of a track (distance and time) does the melt pool take to "
            "reach steady-state width, depth and shape, in conduction mode and in keyhole mode? Evidence from "
            "in-situ high-speed X-ray imaging (e.g. Argonne APS: Cunningham et al. 2019 Science, Zhao et al. "
            "2017/2019, Guo et al., Khairallah et al. 2016/2020 LLNL), high-speed optical or thermal imaging, "
            "longitudinal sections, serial sections along a track, and transient simulations (FEM, CFD, "
            "analytical). How does the transient scale with the thermal diffusion time, the melt-pool length, "
            "P, v and spot size? Is the start of a track wider/deeper/narrower, and is there a bead or ball at "
            "the start?\n"
            "2. End of track. What happens at the end: keyhole collapse and end-of-track porosity, the end "
            "crater, the melt pool shrinking after the laser turns off, and over what distance from the end "
            "the cross-section is unrepresentative. Turnaround/end-of-vector pores (Martin et al. 2019 Nature "
            "Communications) and mitigation by ramping power down.\n"
            "3. Scanner and laser dynamics on galvanometer systems: acceleration and deceleration at the start "
            "and end of a vector, skywriting, laser-on/off and mark delays, and the resulting extra energy per "
            "length at the vector ends; typical distances at 0.2-2 m/s; anything specific to Concept Laser "
            "(CL WRX) machines or similar EOS/SLM Solutions machines.\n"
            "4. Practice in published single-track studies: what track lengths have been used (e.g. Yadroitsev "
            "et al. 2010, Aboulkhair et al. 2016, Ghasemi-Tabasi et al. 2020, Scipioni Bertoli et al. 2017, "
            "Kamath / LLNL 316L on a Concept Laser M2, Johnson et al. 2019, Zhang et al. 2022, Weissbach, "
            "Penny and Hart 2024, NIST AM Bench 2018/2022 single tracks, Ghayoor, Gunenthiram et al.), how much "
            "they discarded at each end, how many cross-sections they took per track and where, and how much "
            "width/depth varied along a track (coefficient of variation, Plateau-Rayleigh undulation, humping).\n"
            "5. Thermo-Calc AM Module perspective: does its steady-state calculation correspond to the "
            "middle of a long track, and how have AM Module or other steady-state model validations chosen "
            "the measurement location? Can its transient mode give the distance to steady state for a "
            "single track?\n\n"
            "Finish with a practical recommendation table for 316L single tracks at P 50-400 W and v 0.1-3 m/s: "
            "minimum distance to discard at the start, at the end, the minimum track length that leaves a "
            "steady-state zone long enough for a section plane located to +/- 1 mm by sawing and grinding, and "
            "the number of sections per track. Flag which numbers are strongly versus weakly supported."
        ),
    },
    "interaction": {
        "title": "Interactions between neighbouring single tracks on one powder layer: spacing and exposure order",
        "outfile": "track-spacing-and-order.md",
        "query": (
            "How far apart must neighbouring single laser powder bed fusion tracks on the same powder layer be, "
            "and in what order and direction should they be exposed, so that each track behaves as if it were "
            "alone on an undisturbed powder layer? "
            + CONTEXT
            + "\n\nPlease answer each part with citations and DOIs, quoting numbers with the P, v, spot, layer "
            "thickness, gas and pressure they apply to:\n"
            "1. Powder denudation: the width of the powder-depleted zone on each side of a single track in 316L "
            "and other alloys as a function of P, v, layer thickness and ambient pressure (e.g. Matthews et al. "
            "2016 Acta Materialia, Bidare et al. 2018, Ly et al. 2017 Scientific Reports, Yin et al., Zheng et "
            "al., Mindt, Aboulkhair, Yadroitsev). Its mechanism (vapour-jet-driven gas entrainment toward the "
            "track at 1 atm, outward expulsion at low pressure, melt-pool capture, particles pulled sideways). "
            "Ratio of denuded-zone width to track width.\n"
            "2. How a previously fused neighbour changes the next track: thinner or missing powder in the "
            "overlap with the neighbour's denuded zone, particles already pulled into the neighbour, a raised "
            "bead next to the new track, and the effect on the new track's width, height, depth, balling or "
            "continuity. Any experiments that varied the spacing between single tracks, or that compared the "
            "first and later tracks of a set.\n"
            "3. Spatter and ejecta: how far spatter and hot ejected particles travel and land (mm), how the "
            "shielding gas flow carries them, the typical gas velocity over the plate, and how exposing tracks "
            "from the gas outlet side toward the inlet (or the scan direction relative to the gas flow) changes "
            "contamination of the remaining powder and track quality. Plume interaction with the beam and its "
            "dependence on the scan direction relative to the gas flow.\n"
            "4. Heat from neighbouring tracks: substrate temperature rise at a given lateral distance and delay "
            "after a track, and when it can be neglected for a single layer of separate tracks; whether "
            "exposure order or waiting time matters for single tracks.\n"
            "5. Practice: the spacing, track length and number of tracks per substrate used in published single-"
            "track studies (Yadroitsev, Aboulkhair, Ghasemi-Tabasi, Kamath/LLNL M2, Johnson/Karayagiz, NIST AM "
            "Bench, Weissbach/Hart 2024, others), and how sectioning several tracks in one transverse cut "
            "constrains spacing (saw kerf, mount size, field of view).\n"
            "6. The effective powder layer: for one layer spread on a flat substrate, the effective powder "
            "thickness and packing fraction compared with the nominal layer thickness; how substrate flatness "
            "or insert height offsets change it; and how the Thermo-Calc AM Module and similar models treat the "
            "powder layer in single-track steady-state calculations.\n\n"
            "Finish with a practical recommendation table for 316L at P 50-400 W, v 0.1-3 m/s and a 30-50 um "
            "layer at 1 atm: minimum centre-to-centre spacing between tracks (with how it scales with melt-pool "
            "width), whether to randomize positions, exposure order and direction relative to the gas flow, "
            "and margin from panel edges. Flag which numbers are strongly versus weakly supported."
        ),
    },
    "doe": {
        "title": "Sobol vs batch Bayesian optimization for a single-track campaign that calibrates a melt-pool model",
        "outfile": "sampling-sobol-vs-batch-bo.md",
        "query": (
            "For a laser powder bed fusion single-track campaign whose goal is to calibrate and validate a melt-"
            "pool model (the Thermo-Calc AM Module, steady state) against measured cross-sections, how should "
            "the power-speed (and possibly spot-size or layer) settings be chosen: a quasi-random space-filling "
            "design such as scrambled Sobol or Latin hypercube, or batch Bayesian optimization / active "
            "learning, and with what batch sizes and replicates? "
            + CONTEXT
            + " We expect roughly 50-100 tracks per build, about one build per week, 4-7 builds in total "
            "(about 250-600 tracks), with sectioning and SEM as the bottleneck.\n\n"
            "Please answer each part with citations and DOIs:\n"
            "1. Published uses of space-filling designs (Sobol, Latin hypercube, Halton) versus grids or "
            "one-factor-at-a-time sweeps for LPBF single tracks or process windows, and what they gained.\n"
            "2. Published uses of Bayesian optimization, active learning or sequential design for LPBF single "
            "tracks, printability maps and melt-pool regimes (e.g. keyhole and lack-of-fusion boundaries, "
            "balling): the objectives and acquisition functions (expected improvement, uncertainty sampling, "
            "integrated variance reduction, level-set or boundary estimation, classification-based), the "
            "surrogate (Gaussian process, multi-fidelity with an analytical or FE model as low fidelity), batch "
            "sizes, and how many tracks they needed. Examples might include Tapia et al. 2018 (GP for 316L "
            "melt-pool depth on single tracks), Kamath 2016, Mondal et al. 2020, Sheikh/Arroyave group "
            "printability and BO work, Menon et al., Gongora/Brown (BEAR), Aboutaleb et al., Wang et al.\n"
            "3. Bayesian model calibration (Kennedy-O'Hagan style, with a discrepancy term) of melt-pool models "
            "to single-track data: which parameters were calibrated (absorptivity, its dependence on energy "
            "density or keyhole depth, beam radius, effective conductivity, Marangoni enhancement), how many "
            "tracks were needed, and which designs worked best for calibration versus validation (held-out "
            "points, extrapolation tests).\n"
            "4. Noise and replication: the run-to-run, track-to-track and along-track variability of measured "
            "width and depth in 316L single tracks; how many replicates or cross-sections per setting are "
            "needed; using repeated control tracks to estimate noise and block effects (build, panel, position "
            "on the plate); randomization and blocking.\n"
            "5. Which input space to sample: raw (P, v), (P, log v), linear energy P/v, normalized enthalpy "
            "or the dimensionless groups of King et al. 2014 / Hann et al., and the effect of constraints such "
            "as excluding settings certain to not melt or to keyhole badly.\n\n"
            "Finish with a recommendation for our case: the initial design (method, number of points, whether "
            "to use a power of two for Sobol, controls and replicates per build), the batch BO/active-learning "
            "formulation for later builds (objective, acquisition, batch size equal to one build, stopping "
            "rule), and the split between calibration and held-out validation tracks. Flag which choices are "
            "strongly versus weakly supported."
        ),
    },
    "ss316l": {
        "title": "316L inputs for an Eagar-Tsai model and published single-track data to check it against",
        "outfile": "ss316l-eagar-tsai-inputs-and-single-track-data.md",
        "query": (
            "What constant thermophysical properties and absorptivity should an Eagar-Tsai melt-pool model use "
            "for 316L stainless steel in laser powder bed fusion, and what published single-track cross-section "
            "measurements (laser power, scan speed, spot size, layer thickness, melt-pool width and depth) can we "
            "use to check it? "
            + CONTEXT
            + "\n\nPlease answer each part with citations and DOIs:\n"
            "1. 316L liquidus and solidus temperatures; thermal conductivity, density and specific heat near "
            "the solidus/liquidus (solid and liquid), latent heat of fusion, boiling point; and the constant "
            "values used by published Eagar-Tsai, Rosenthal or other analytical models of 316L LPBF (e.g. "
            "Kamath 2016 / LLNL with the Concept Laser M2, Tapia et al. 2018, Johnson et al. 2019, Mukherjee, "
            "Rubenchik et al. 2018 scaling laws).\n"
            "2. Absorptivity of 316L at about 1070 nm: flat solid, powder bed, conduction-mode and keyhole-mode "
            "values from calorimetry (e.g. Trapp et al. 2017, Ye et al. 2019), and effective values back-"
            "calibrated by fitting analytical or FE models to measured 316L melt pools.\n"
            "3. The Concept Laser M2 laser and optics: power options, wavelength, spot size and its definition "
            "(1/e^2, D4sigma, FWHM), beam quality, and maximum scan speed; what LLNL (Kamath et al.) and others "
            "reported for their M2.\n"
            "4. Tabulated or digitizable single-track data for 316L: for each study, the P, v, spot size, "
            "layer thickness (or bare plate), measured width and depth, and the regime (conduction, transition, "
            "keyhole), especially Kamath / King et al. on the M2, Ghasemi-Tabasi, Yadroitsev, Scipioni Bertoli, "
            "NIST, and any public datasets (e.g. MeltpoolNet, Akbari et al. 2022) that include 316L.\n"
            "5. Thresholds used to label the regime from cross-sections for 316L: keyhole onset by depth/"
            "half-width or depth/width, normalized enthalpy thresholds, lack of fusion by depth versus layer, "
            "and balling/Plateau-Rayleigh criteria by length/width.\n\n"
            "Finish with a table of recommended Eagar-Tsai inputs for 316L (liquidus K, conductivity W/(m K), "
            "density kg/m^3, specific heat J/(kg K), absorptivity for conduction and keyhole mode, with ranges) "
            "and a table of the single-track data points you found (study, P W, v mm/s, spot um and its "
            "definition, layer um, width um, depth um, regime). Flag which numbers are strongly versus weakly "
            "supported."
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
    record = {"job": JobNames.LITERATURE_HIGH.value,
              "submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "tasks": {}}
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
        f"Edison Scientific LITERATURE_HIGH report: {meta['title']}\n"
        f"Job: {JobNames.LITERATURE_HIGH.value} (LITERATURE_HIGH)\n"
        f"Task ID: {meta['task_id']}\n"
        f"Created: {dump.get('created_at')}  Status: {status}\n"
        "Retrieved with edison-client from GitHub Actions for issue #100 / PR #243.\n"
        "Prompt: QUERIES['" + key + "'] in scripts/edison_m2_track_design.py\n"
        "-->\n\n"
    )
    body = EMAIL_RE.sub("[email redacted]", formatted or plain)
    if references and references not in body:
        body += "\n\n## References\n\n" + EMAIL_RE.sub("[email redacted]", references)
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
