"""Edison LITERATURE_HIGH search for issue #225: best practice for image-based particle size and shape
distributions of atomized metal powder from SEM images.

    python run_edison.py submit   # create the task, write _task_ids.json
    python run_edison.py wait     # block until the task finishes (foreground only)
    python run_edison.py fetch    # save the answer as markdown, plus metadata and the full trajectory as JSON

The API key is read from EDISON_PLATFORM_API_KEY and never printed.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

from edison_client import EdisonClient, JobNames, TaskRequest

HERE = Path(__file__).resolve().parent
IDS_FILE = HERE / "_task_ids.json"
TERMINAL = {"success", "fail", "failed", "cancelled", "error"}
# Paper excerpts in a trajectory carry authors' e-mail addresses and phone numbers; this repo is public
# and CLAUDE.md bars those, so scrub every decoded string before saving.
REDACTIONS = [
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[email redacted]"),
    (re.compile(r"(?i)\b(?:tel|phone|fax)\b\.?:?\s*[\d\s().+-]{7,}\d"), "[phone redacted]"),
    (re.compile(r"\+\d[\d\s().-]{8,}\d"), "[phone redacted]"),
]


def scrub(obj):
    if isinstance(obj, str):
        for pattern, repl in REDACTIONS:
            obj = pattern.sub(repl, obj)
        return obj
    if isinstance(obj, list):
        return [scrub(v) for v in obj]
    if isinstance(obj, dict):
        return {k: scrub(v) for k, v in obj.items()}
    return obj


QUERY = """\
Context. We ultrasonically atomized a nickel-aluminium bronze (UNS C63000, Cu-10Al-5Ni-4Fe) on an
AMAZEMET rePOWDER and want a particle size and shape distribution from SEM images, done to best
practice, before sieving to a directed-energy-deposition cut of 50-200 um. The powder is mostly
spherical, from <10 um fines to ~260 um, with satellites and a few irregular or agglomerated
particles. It was sprinkled on carbon tape on one stub and imaged in a Thermo Fisher Apreo C with the
secondary-electron (ETD) detector: nine usable 3072 x 2048 px fields at 133-200x (0.67-1.01 um per
pixel), densely packed, with many touching and overlapping particles. A naive Hough-circle detection
returned thousands of overlapping false circles per field. We plan distance-transform watershed
segmentation and are weighing pretrained models (Cellpose, StarDist, Segment Anything / SAM, and
SEM-powder-specific deep-learning models), and we have a few hand measurements to validate against.

Please give the best-practice method, with numbers and sources, for:

1. Standards. What ISO 13322-1 (static image analysis), ISO 9276-1, -2 and -6 (representation of
   results, moments, and shape descriptors), ISO 14488 (sample splitting), ASTM F3049 (characterizing
   powders for AM), ASTM B822 (laser diffraction for metal powders) and ASTM B214 (sieve analysis)
   require or recommend for image-based particle sizing: the size measure (projected-area equivalent
   circle diameter vs Feret diameters), magnification and pixel requirements, minimum particle
   counts, calibration and traceability (stage micrometer / certified reference beads), and what a
   report must state.

2. Counting statistics. The minimum number of particles for D10, D50 and D90 by number and by volume
   at a stated precision (e.g. the ISO 13322-1 / Masuda-Gotoh style estimate of the count needed for
   a given relative error in a volume-weighted percentile, and the ~10,000-particle figures quoted for
   robust morphology). How should confidence intervals on percentiles be computed (bootstrap,
   order-statistic, Masuda-Gotoh), and why does the volume-weighted D90 need far more particles than
   the number-weighted D50?

3. Pixel resolution. The minimum number of pixels across (or pixel area of) the smallest particle
   for reliable size, and separately for reliable shape (circularity, aspect ratio, solidity), with
   quantitative estimates of the bias in circularity and perimeter for small, pixelated objects, and
   how perimeter estimators (Crofton, chain-code corrections) reduce it. What lower size cut-off
   should be applied for a given pixel size?

4. Segmentation of touching and overlapping spherical particles: thresholding (Otsu, local/adaptive),
   distance-transform marker-controlled watershed (h-maxima marker selection, over- and
   under-segmentation), ellipse/circle fitting on contours, Cellpose, StarDist, SAM / micro-SAM and
   powder-specific CNNs (e.g. Mask R-CNN models trained on AM-powder SEM images). Report published
   accuracy comparisons on metal powders or similar dense spherical particles (precision/recall, size
   bias versus manual measurement), and what validation is considered adequate.

5. Edge effects. Exclusion of particles that touch the image frame and the standard bias correction
   (Miles-Lantuejoul guard-frame weighting, w = (W*H)/((W - d)(H - d)) for a particle of extent d), and
   how it is reported. Also: double counting in overlapping fields, and how to handle partially
   hidden (occluded) particles in multilayer fields.

6. Number- to volume-weighted conversion. Converting a number distribution of projected-area
   equivalent diameters to volume (mass) weighting (q0 to q3 via ISO 9276-2 moments, d^3 weighting),
   the error amplification from a few large particles, and whether a sphericity correction is needed.

7. SEM image analysis versus laser diffraction and sieving for spherical gas- and ultrasonically
   atomized metal powders: typical systematic differences in D10/D50/D90 (and their direction), the
   reasons (2D projection, orientation, sedimentation and size segregation on the stub, fines adhering
   to coarse particles, satellites, agglomerates, laser-diffraction volume weighting and Mie model
   assumptions), and published side-by-side numbers. Also dynamic image analysis (Camsizer, QICPIC,
   Morphologi 4) as a reference method.

8. Satellites and agglomerates. How satellite fraction and agglomerates are quantified from SEM
   images (solidity/convexity thresholds, convexity defects, manual classification, counts of
   satellites per particle), and typical values reported for gas- and ultrasonically atomized powders.

9. Imaging practice. Secondary-electron versus backscattered-electron contrast for segmenting metal
   powder on carbon tape; dispersion methods (dry dispersion, sprinkling, solvent dispersion,
   mounting in epoxy and cross-sectioning) that avoid overlap and size segregation; how many fields,
   stubs and splits are needed; and a magnification ladder when the size range spans more than a
   decade (e.g. 10-260 um).

10. Reporting conventions: the minimum content of a report (counts, n per size class, weighting,
    descriptor definitions, pixel size, exclusion rules, confidence intervals, cumulative Q0 and Q3
    curves, span (D90-D10)/D50), shape descriptor definitions per ISO 9276-6 (circularity
    4*pi*A/P^2 versus sqrt form, aspect ratio, solidity, convexity), and how AM-powder papers report
    these.

Finish with a concise, numbered protocol for the next powder lot on the same SEM (stub prep, detector,
magnification and pixel size, fields and particle counts, segmentation and validation, exclusions and
corrections, reporting), and say plainly which of our current choices would not meet ISO 13322-1.
"""

TASKS = {
    "literature_high_sem_psd_best_practice": (JobNames.LITERATURE_HIGH, QUERY),
}


def client():
    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def submit():
    if IDS_FILE.exists():
        sys.exit(f"{IDS_FILE.name} already exists; refusing to resubmit")
    c = client()
    ids = {}
    for key, (job, query) in TASKS.items():
        try:
            ids[key] = str(c.create_task(TaskRequest(name=job, query=query)))
        except Exception as exc:  # fall back to LITERATURE if HIGH is unavailable
            print(key, "LITERATURE_HIGH failed:", type(exc).__name__, "- retrying as LITERATURE", flush=True)
            ids[key] = str(c.create_task(TaskRequest(name=JobNames.LITERATURE, query=query)))
        print(key, ids[key], flush=True)
    IDS_FILE.write_text(json.dumps({"submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                    "tasks": ids}, indent=2) + "\n")


def wait(max_minutes=float(os.environ.get("EDISON_WAIT_MINUTES", "40")), poll=120):
    c = client()
    ids = json.loads(IDS_FILE.read_text())["tasks"]
    deadline = time.time() + max_minutes * 60
    while True:
        statuses = {k: str(c.get_task(task_id=v, lite=True).status) for k, v in ids.items()}
        print(time.strftime("%H:%M:%S", time.gmtime()), statuses, flush=True)
        if all(s in TERMINAL for s in statuses.values()) or time.time() > deadline:
            return
        time.sleep(poll)


def fetch():
    c = client()
    ids = json.loads(IDS_FILE.read_text())["tasks"]
    for key, task_id in ids.items():
        task = c.get_task(task_id=task_id)
        data = task.model_dump(mode="json")
        answer = scrub(data.get("formatted_answer") or data.get("answer") or "")
        meta = {k: data.get(k) for k in ("task_id", "status", "job_name", "created_at", "query",
                                          "has_successful_answer", "total_cost", "total_queries")}
        (HERE / f"{key}.json").write_text(json.dumps(meta, indent=2) + "\n")
        if answer:
            (HERE / f"{key}.md").write_text(
                f"# Edison {meta['job_name']} result: {key}\n\n"
                f"**Task ID:** `{task_id}`  \n**Status:** {meta['status']}\n\n"
                f"<details><summary>Query</summary>\n\n```text\n{meta['query']}\n```\n\n</details>\n\n"
                f"{answer}\n")
        verbose = scrub(c.get_task(task_id=task_id, verbose=True).model_dump(mode="json"))
        (HERE / f"{key}_trajectory.json").write_text(json.dumps(verbose, indent=1, default=str) + "\n")
        print(key, meta["status"], len(answer), "chars", flush=True)


if __name__ == "__main__":
    {"submit": submit, "wait": wait, "fetch": fetch}[sys.argv[1]]()
