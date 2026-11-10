"""Edison LITERATURE_HIGH queries: open-source replacements for the AM module's keyhole model (issue #235).

eagar-tsai matched the Thermo-Calc AM module's lack-of-fusion boundaries but not its keyholing
(see arroyave-orchid-tools/eagar-tsai/README.md). These four queries look for what could replace
the AM module there, submitted in parallel:

* ``models``: open or re-implementable models of keyhole onset and keyhole-mode pool size
  (scaling laws, semi-analytical keyhole profiles, surrogates, open thermal-fluid codes).
* ``thermocalc``: how the AM module itself models the keyhole, and what it was validated on.
* ``data``: open measurements that could seed an ORCHID-style benchmark of keyhole models.
* ``aluminium``: keyhole thresholds, absorptivity and keyhole-mode pools for Al-Si alloys.

Usage (run from the repo root; needs EDISON_PLATFORM_API_KEY):

    python scripts/edison_keyhole_alternatives.py submit   # writes _task_ids.json
    python scripts/edison_keyhole_alternatives.py wait     # blocks until all finish, then fetches
    python scripts/edison_keyhole_alternatives.py fetch    # fetch whatever has finished

``wait`` keeps its sleep inside Python, so in GitHub Actions it can run as a single foreground
call (see CLAUDE.md).
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
OUT_DIR = REPO_ROOT / "edison-trajectories" / "keyhole-open-alternatives"
RAW_DIR = OUT_DIR / "raw"
TASK_FILE = OUT_DIR / "_task_ids.json"
TERMINAL = {"success", "fail", "failed", "cancelled", "error"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

KH_CONTEXT = (
    "Context: we use ArroyaveLab's open-source `eagar-tsai` Python package (a conduction-mode "
    "Eagar-Tsai travelling Gaussian surface heat source on a semi-infinite solid with constant "
    "properties) as a cheap stand-in for the Thermo-Calc Additive Manufacturing (AM) Module when "
    "building laser powder bed fusion (LPBF) printability maps for AlSi10Mg and a hypereutectic "
    "Al-24Si-0.14Mg (wt%) blend: Gaussian beam with 1/e^2 radius 40-45 um, 75-400 W, 0.3-2.4 m/s, "
    "30 um layer, 100-130 um hatch, 30-150 C build plate. Against the AM Module's maps, eagar-tsai "
    "reproduced the lack-of-fusion boundaries (pool depth D <= layer t, and depth at half the hatch "
    "<= t) to within about 20 W, but not keyholing. The AM Module flags keyholes with the aspect "
    "ratio of the keyhole (vapour cavity) itself, Wk/Dk <= 0.7, and only at 2-4 times the power at "
    "which eagar-tsai's pool reaches W/D = 2.5 or its peak temperature reaches Al's boiling point. "
    "A conduction model's W/D never drops below about 2 (the semicircle limit), and it has no "
    "evaporation cap on peak temperature (eagar-tsai gives 6,400 K where the AM Module gives "
    "3,044 K at 250 W, 0.9 m/s). In keyhole mode (375 W, 0.4 m/s, Al-24Si, 45 um beam radius, "
    "absorptivity about 0.38) the AM Module gives a pool 349 um deep, about 460 um wide and 1.47 mm "
    "long, which eagar-tsai cannot reach at any absorptivity up to 1. Measured AlSi10Mg single "
    "tracks (Solyaev et al. 2025, arXiv:2507.23422; 80 um spot) were in keyhole mode (D/W > 0.75) "
    "for P > 220 W and v < 0.8 m/s. We want the best open-source replacement for the AM Module's "
    "keyhole prediction: fast enough for printability maps (ideally seconds per point, at most "
    "hours for a few hundred points) and validated, preferably on aluminium alloys."
)

QUERIES: dict[str, dict[str, str]] = {
    "models": {
        "title": "Open-source models for keyhole onset and keyhole-mode melt-pool size in LPBF",
        "outfile": "models-keyhole-onset-and-depth.md",
        "query": (
            "Which open-source, or fully published and re-implementable, models best predict "
            "(a) the onset of keyhole-mode melting and of keyhole porosity, and (b) the depth, width "
            "and length of keyhole-mode melt pools in laser powder bed fusion, so that they could "
            "replace the Thermo-Calc AM Module's keyhole model in printability maps? "
            + KH_CONTEXT
            + "\n\nPlease cover each of the following with the model's formulas, fitted constants, "
            "validity range, the alloys and spot sizes it was validated on, and its quantitative "
            "accuracy against in situ synchrotron X-ray keyhole measurements or cross-sections:\n"
            "1. Dimensionless scaling laws and criteria: the normalized enthalpy dH/h_s (Hann et al. "
            "2011; the keyhole threshold of King et al. 2014), the keyhole number Ke of Gan et al. "
            "2021 (Nature Communications, universal scaling laws of keyhole stability and porosity), "
            "the normalized parameters of Rubenchik, Wu, Mitchell et al. 2018 and Ye et al. 2019, "
            "Fabbro's keyhole-depth models, the power-density threshold of Cunningham et al. 2019 "
            "(Science), and the W/D, D/W and peak-temperature-above-boiling criteria used in "
            "printability maps (Seede et al. 2020; Johnson et al. 2019; Zhu et al.; Sheikh et al. "
            "2024). Which of these predict keyhole DEPTH, not just onset, and how well?\n"
            "2. Semi-analytical keyhole-profile models: Kaplan 1994 (point-by-point energy balance "
            "with Fresnel absorption), Lankalapalli et al. 1996, Steen's point-plus-line source, "
            "Fabbro and Chouf, Pang et al., and the model inside Thermo-Calc's AM Module; any "
            "open-source code that implements them; runtime per point.\n"
            "3. Reduced-order or surrogate models trained on X-ray or CFD data (e.g., Gaussian-process "
            "or neural-network surrogates of keyhole depth) whose code and data are public.\n"
            "4. Open-source high-fidelity thermal-fluid codes that resolve the keyhole (recoil "
            "pressure, Fresnel ray tracing, evaporative cooling): laserbeamFoam and beamWeldFoam "
            "(OpenFOAM), MeltPoolDG (deal.II), Lethe, MOOSE's navier_stokes laser-welding examples, "
            "AdditiveFOAM (ORNL) and others. For each: licence, maintenance status, validation "
            "against X-ray keyhole depth (alloy, error) and compute cost per single track.\n\n"
            "Finish with a ranked table: model or tool, what it predicts (onset, porosity threshold, "
            "depth, width, length), inputs, validated alloys (flag any aluminium-alloy validation), "
            "reported error, cost per point, open-source status with a link, and your recommendation "
            "for (i) a fast printability-map screen and (ii) a reference keyhole-mode pool size for "
            "an Al-Si alloy. Cite DOIs and flag which claims are strongly versus weakly supported."
        ),
    },
    "thermocalc": {
        "title": "How the Thermo-Calc AM Module models the keyhole, and what it was validated against",
        "outfile": "thermocalc-am-module-keyhole-model.md",
        "query": (
            "How does the Thermo-Calc Additive Manufacturing (AM) Module model keyhole-mode melting, "
            "and what has it been validated against? "
            + KH_CONTEXT
            + "\n\nPlease answer each part with citations and DOIs or URLs:\n"
            "1. The AM Module's heat-transfer and fluid-flow formulation (steady state vs transient, "
            "free surface, Marangoni flow, evaporation and recoil pressure), and specifically its "
            "keyhole model: the physics, the published model it is based on, how the keyhole width "
            "Wk and depth Dk are computed, and how absorptivity is calculated (electrical "
            "resistivity, Fresnel or Hagen-Rubens, multiple reflections in the keyhole), including "
            "the absorptivity prefactor.\n"
            "2. The definitions of its printability-map criteria (keyhole Wk/Dk <= 0.7, lack of "
            "fusion D/t, lack of fusion at the hatch Dh/t, balling) and where those thresholds come "
            "from.\n"
            "3. Validation of the AM Module against measured melt pools or keyhole depths: "
            "Thermo-Calc's own examples (e.g., AM_09 316L printability map, AM_11 AlSi10Mg single "
            "tracks) and peer-reviewed papers that used the AM Module for Al alloys, 316L, "
            "Ti-6Al-4V or IN718, including any absorptivity scaling they needed (e.g., x1.8 for "
            "AlSi10Mg) and the errors they report.\n"
            "4. Which open-source models reproduce the same physics most closely.\n\n"
            "Keep what Thermo-Calc documents separate from what is inferred, and say when a source "
            "could not be accessed."
        ),
    },
    "data": {
        "title": "Open measured keyhole thresholds and depths that could seed an ORCHID-style benchmark",
        "outfile": "data-open-keyhole-measurements.md",
        "query": (
            "What openly available measurements of keyhole onset thresholds, keyhole depth and "
            "keyhole-mode melt-pool dimensions exist for laser powder bed fusion and laser spot or "
            "track melting of metals, which could seed an open, curated benchmark for scoring cheap "
            "keyhole models? The model for the benchmark is ORCHID, an open repository of CALPHAD "
            "assessments with accepted reference values that are used to score models. "
            + KH_CONTEXT
            + "\n\nPlease list:\n"
            "1. In situ synchrotron X-ray imaging studies of keyholes (APS 32-ID, ESRF, SLS, "
            "Diamond, SPring-8): alloy, bare plate or powder, power, speed and spot ranges, reported "
            "keyhole depth versus P and v, the keyhole-onset and porosity thresholds, and whether "
            "the data are public (repository, DOI, supplementary tables). For example Cunningham et "
            "al. 2019, Zhao et al. 2020, Gan et al. 2021, Huang et al., Wang et al., Hojjatzadeh et "
            "al., and aluminium-alloy studies (Al6061, AlSi10Mg, Al-Si, Al-Cu).\n"
            "2. NIST AM-Bench single-track measurements (2018, 2022, 2025) and other open melt-pool "
            "datasets (Materials Data Facility, Zenodo, Mendeley Data, figshare), with what they "
            "measured.\n"
            "3. Single-track cross-section datasets for AlSi10Mg and other Al alloys that span the "
            "conduction-to-keyhole transition, with spot size and absorptivity.\n"
            "4. Any existing community benchmark or database that scores melt-pool or keyhole models "
            "against shared measurements (AM-Bench challenge results, MeltpoolNet, melt-pool "
            "databases), and what an ORCHID-like curation (accepted values with uncertainty, model "
            "scoring) would need.\n\n"
            "Finish with a table: dataset, alloy(s), quantity measured, condition ranges, licence or "
            "access, link or DOI, and how suitable it is for benchmarking keyhole onset and depth."
        ),
    },
    "aluminium": {
        "title": "Keyhole thresholds, absorptivity and keyhole-mode pools in AlSi10Mg and Al-Si alloys",
        "outfile": "aluminium-keyhole-thresholds.md",
        "query": (
            "For AlSi10Mg and hypereutectic Al-Si alloys processed by laser powder bed fusion or "
            "laser track melting, what are the measured keyhole-onset conditions and keyhole-mode "
            "melt-pool dimensions, and which models (analytical, semi-analytical or CFD) reproduced "
            "them? "
            + KH_CONTEXT
            + "\n\nPlease cover, with citations and DOIs:\n"
            "1. Measured transitions from conduction to transition to keyhole mode for AlSi10Mg "
            "(single tracks and X-ray imaging), expressed as power, speed and spot size and, where "
            "given, as normalized enthalpy, keyhole number or linear energy density, with the D/W "
            "or other criterion each study used.\n"
            "2. The absorptivity of Al alloys in conduction versus keyhole mode (calorimetric and in "
            "situ measurements, e.g., Trapp et al. 2017 and Simonds et al. 2020; the rise with "
            "keyhole depth), and what absorptivity models (Fresnel, multiple reflections, "
            "correlations of absorptivity with keyhole aspect ratio or keyhole number) predict.\n"
            "3. Evaporation of Mg and Al, recoil pressure, and the boiling or vaporization "
            "temperature relevant to keyholing in Al alloys.\n"
            "4. How Si content (10 versus about 24 wt%) changes the keyhole threshold or pool shape "
            "(thermal properties, absorptivity, surface tension, viscosity), including any "
            "measurements on hypereutectic Al-Si.\n"
            "5. Models that reproduced Al-alloy keyhole depth quantitatively, with their errors.\n\n"
            "Finish with a table of the best-supported numbers (thresholds, absorptivities, keyhole "
            "depths), each with its source and DOI."
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
    record = {
        "job": JobNames.LITERATURE_HIGH.value,
        "submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "tasks": {},
    }
    for key, q in QUERIES.items():
        task_id = c.create_task(TaskRequest(name=JobNames.LITERATURE_HIGH, query=q["query"]))
        record["tasks"][key] = {"task_id": str(task_id), "title": q["title"], "outfile": q["outfile"]}
        print(f"submitted {key}: {task_id}", flush=True)
        # Write after every submission, so a failure part-way still records what was sent.
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

    # Pull the answer out of the environment frame (PaperQA layout), with fallbacks.
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
        "Retrieved with edison-client from GitHub Actions for issue #235.\n"
        "Prompt: QUERIES['" + key + "'] in scripts/edison_keyhole_alternatives.py\n"
        "-->\n\n"
    )
    body = formatted or plain
    if references and references not in body:
        body += "\n\n## References\n\n" + references
    (OUT_DIR / meta["outfile"]).write_text(EMAIL_RE.sub("[email redacted]", header + body.strip()) + "\n")
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
