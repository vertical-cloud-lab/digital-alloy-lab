"""Edison queries for PR #175: the lower cut (15-20 um end) for the Al LPBF powder.

    python run_edison.py submit   # upload the PSD files, create the three tasks, write _task_ids.json
    python run_edison.py wait     # block until every task finishes (foreground only, see CLAUDE.md)
    python run_edison.py fetch    # save each answer as markdown, plus metadata, trajectory and output files

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
UPLOAD_DIR = HERE / "upload"
# The PSD files are copied in from PR #226 (commit 80f3fa5) before submitting; only context.md is committed.
UPLOADS = ["context.md", "nab_k7m2q9_particles.csv", "nab_k7m2q9_summary.md", "fields.csv"]
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


CONTEXT = """\
Context. A university lab ultrasonically atomizes aluminium alloys (Al 4047 / AlSi12 and 6063) on an
AMAZEMET rePOWDER (about 40 kHz, molybdenum plate) in 100-250 g runs, for laser powder bed fusion on an
Aconity MIDI. The powder is highly spherical. An SEM image-analysis PSD of a nickel-aluminium bronze from the
same atomizer (5,937 particles) gave number D10/D50/D90 of 35/47/72 um and volume D10/D50/D90 of
46/104/209 um, with 2.1 % by number and under 0.1 % by volume below 20 um. A first SEM look at the Al lots
found the smallest particles mostly 40-60 um. The lab has 8 in (200 mm) stainless test sieves at 250 um
(No. 60) and 63 um (No. 230), with 45 um (No. 325) on order, and no sieve shaker yet. The runs plan targets a
15-45 um window; an earlier plan targeted 20-63 um.
"""

Q1 = CONTEXT + """
Question: does the sub-15/20 um fraction matter for LPBF of aluminium alloys, and is "no lower cut" defensible?
Use experimental papers and give numbers with sources.

1. Measured effects of fines (below 15-20 um) in Al alloy LPBF powders (AlSi10Mg, AlSi12, AlSi7Mg, 4047,
   6061/6063, Scalmalloy) on flowability (Hall/Carney flow, avalanche angle, revolution powder analysis,
   Hausner ratio, FT4 cohesion), spreadability and layer quality (blade, roller, brush or rubber recoaters),
   packing density, spatter and denudation, porosity (lack of fusion, keyhole), surface roughness, powder
   oxygen and hydrogen, and tensile properties. Which studies varied the fines content of one Al powder
   (blended fines, 0-63 vs 20-63 vs 15-45 um, or recycled powder that lost its fines), and what fines fraction
   (by volume and by number) changed the outcome? Explain the cohesion argument (granular Bond number,
   van der Waals versus weight) for Al at its low density, at 10, 20 and 45 um.
2. What do LPBF and powder papers on ultrasonically atomized powders (Al especially; AMAZEMET rePOWDER, ATO
   Lab/Lab+, other ultrasonic atomizers; e.g. Yankin 2025, Priyadarshi 2024, Ukabhai 2025, Balasz 2023/2024,
   Hinrichs 2021, Zrodowski, Pilarski, Kaminski) actually do: an upper cut only, a lower cut as well, or none?
   What sieves or classifiers, what PSD did they print or characterize, and what fraction was below 20 um?
3. Commercial LPBF Al powder specifications (EOS, Nikon SLM Solutions, Renishaw, Aconity, AP&C, Carpenter
   Additive, Valimet, ECKART, Toyal, IMR, Elementum): stated size range and how much material below 15 or
   20 um they allow (D10 limits, maximum percent below a size). What PSD and layer thickness do Aconity MIDI
   or AconityMINI users report for AlSi10Mg?
4. For research builds (single tracks, density cubes, a few tensile bars) on a research LPBF machine, with
   2 % by number and under 1 % by volume below 20 um, is printing without a lower cut defensible? What would a
   reviewer expect to see reported instead (PSD by laser diffraction or image analysis, flow and density
   measurements)? Under what conditions would the fines matter (e.g. thin layers, recycled powder, humid
   storage)?
5. Safety: how explosibility of aluminium dust (minimum ignition energy, Kst, minimum explosible
   concentration) depends on particle size between 10 and 60 um, and whether removing the fines changes the
   handling precautions (NFPA 484) for the remaining powder.

Finish with a short recommendation: lower cut or not for test builds, at what size, and what measurement
would change the answer.
"""

Q2 = CONTEXT + """
Question: if we want a lower cut at 15-25 um on 200-500 g lots of Al alloy powder (Al-12Si, 6063), what is
realistic in a university lab, and do we need a shaker for 8 in sieves at 45 and 63 um? Use the powder
technology, sieving-standard and AM-powder literature, and give numbers with sources.

1. Fine woven-wire test sieves, 200 mm / 8 in, No. 635 (20 um) and No. 450 (32 um), with and without backing
   cloth, on a tapping (Ro-Tap type) or vibratory (throw-action) shaker: recommended maximum charge per
   sieve (e.g. DIN 66165 / ISO 2591-1 / ASTM E11 / ASTM B214 tables), throughput (g per hour) and endpoint
   criteria, blinding and how quickly it sets in for metal powder, sieving aids (rubber balls or cubes,
   brushes, anti-static agents, flow aids such as fumed silica), ultrasonic deblinding of test sieves, mesh
   damage and sieve life, and measured cut efficiency and losses at 20-32 um.
2. Wet sieving (water, ethanol or isopropanol) of aluminium or Al-Si powder below 45 um: whether it is done,
   oxidation and hydrogen evolution in water, solvent choice, drying and the oxygen pick-up it causes, and
   whether wet-sieved Al powder has been printed by LPBF.
3. Sonic sifters (ATM / Advantech Sonic Sifter L3P) and air-jet sieves (Hosokawa Alpine e200 LS, Retsch AS 200
   jet): sample mass per run (analytical, about 5-100 g), cut size range, time per run, whether they can be
   run repeatedly as a preparative cut for a few hundred grams, recovery of the fines from the cyclone or
   filter, and Al dust hazards (the air-jet sieve's vacuum cleaner, filter, static).
4. Benchtop or pilot air classifiers (Hosokawa Alpine 50 ATP / 100 MZR / Turboplex, NETZSCH CFS 5 HD-S,
   Matsubo Elbow-Jet EJ-L, Nisshin Engineering Aerofine or Turbo Classifier, Sturtevant Whirlwind): minimum
   batch size, cut-size range, cut sharpness (kappa = d25/d75), yield and hold-up losses on a 200-500 g
   batch, whether nitrogen/argon closed-loop operation is available, and ATEX or NFPA 484 requirements for
   classifying aluminium. Which AM-powder papers classified a small lab batch, and with what?
5. Toll classification of aluminium powder by service providers: who does small lots, typical minimum lot
   size, turnaround, and what losses to expect.
6. Hand sieving versus a mechanical shaker on 8 in sieves at 45 and 63 um for 200-500 g of spherical Al
   powder: how far hand sieving falls short in completeness and repeatability (ASTM B214, ISO 4497, DIN
   66165, Haver & Boecker or Retsch application notes), the charge per pass, time to endpoint, and whether a
   tapping shaker (Ro-Tap) or a vibratory 3D shaker is preferred for metal powders.
7. Aluminium dust safety for each option, in a lab without a glovebox: ignition sources (motors, static,
   vacuum cleaners), inerting, grounding, and what NFPA 484 and NFPA 652 require.

Finish with a table comparing the options (cost class, throughput on 200-500 g, losses, blinding, Al dust
risk, cut size) and a recommendation for a lab that makes 100-250 g per run.
"""

Q3 = """\
The attached files are an SEM image-analysis particle size distribution of an ultrasonically atomized
nickel-aluminium bronze from our AMAZEMET rePOWDER; `context.md` explains every column and the measurement
limits. We want to know what this says about the fine end for our aluminium powder from the same atomizer,
which we plan to sieve with 8 in sieves at 250, 63 and 45 um for laser powder bed fusion.

Please analyse the data in Python and report, with code and figures:

1. Using only counted particles (`included == True`) and the Miles-Lantuejoul `weight`, the cumulative number
   (Q0) and volume (Q3, equivalent spheres) distributions of `ecd_um`, and the fractions below 10, 15, 20, 25,
   32, 45 and 63 um by number and by volume, with 95 % bootstrap intervals resampled over particles and,
   separately, over fields (the powder segregated by size across the stub, so the field interval matters).
2. The detection limit: particles under 10 px (6.7-10 um) are not counted. Bound how much the true
   sub-10 um and sub-15 um fractions could be underestimated, e.g. by fitting a log-normal or Rosin-Rammler to
   the counted data above 15 um and extrapolating, and compare with the counted values.
3. The fraction within the windows 20-63, 15-45, 20-45 and 0-63 um, by volume (that is, by mass), and what a
   lower cut at 20 um or at 15 um would remove from the material that passes a 63 um sieve and from the
   material that passes a 45 um sieve: grams per 100 g of sieved powder, with intervals.
4. Scaling to aluminium. Ultrasonic atomization theory (Lang 1962) gives a median droplet diameter
   d = 0.34 (8 pi sigma / (rho f^2))^(1/3). Using the liquid properties in `context.md`, estimate the size
   ratio of Al-12Si to NAB droplets at the same frequency, and rescale the NAB distribution by that ratio as
   one estimate of the Al distribution. Report the same fractions (below 15, 20, 25 um; within 20-63 and
   15-45 um) for the rescaled distribution. State plainly how uncertain this transfer is (alloy, melt flow
   rate, plate, amplitude, and the fact that the NAB stub may not be representative).
5. Plots: cumulative Q0 and Q3 with the 15, 20, 45 and 63 um lines marked, for NAB and for the rescaled Al
   estimate; and a histogram of the fine end (below 30 um) by number.

End with a short conclusion: given these numbers, does a lower cut at 15-20 um matter for mass yield, and how
many particles in a typical LPBF layer would be below 20 um?
"""

TASKS = {
    "q1_fines_in_lpbf_al": (JobNames.LITERATURE_HIGH, Q1, False),
    "q2_lower_cut_methods": (JobNames.LITERATURE_HIGH, Q2, False),
    "q3_psd_analysis": (JobNames.ANALYSIS, Q3, True),
}


def client():
    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def submit():
    if IDS_FILE.exists():
        sys.exit(f"{IDS_FILE.name} already exists; refusing to resubmit")
    c = client()
    uris = []
    for name in UPLOADS:
        uri = c.upload_file(UPLOAD_DIR / name, description=f"PR #175 lower-cut analysis: {name}")
        uris.append(uri)
        print("uploaded", name, uri, flush=True)
    ids = {}
    for key, (job, query, with_files) in TASKS.items():
        task_id = c.create_task(TaskRequest(name=job, query=query), files=uris if with_files else None)
        ids[key] = {"task_id": str(task_id), "job": job.name}
        print(key, job.name, task_id, flush=True)
    IDS_FILE.write_text(json.dumps({"submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                    "uploads": dict(zip(UPLOADS, uris)), "tasks": ids}, indent=2) + "\n")


def wait(max_minutes=float(os.environ.get("EDISON_WAIT_MINUTES", "45")), poll=120):
    c = client()
    ids = json.loads(IDS_FILE.read_text())["tasks"]
    deadline = time.time() + max_minutes * 60
    while True:
        statuses = {k: str(c.get_task(task_id=v["task_id"]).status) for k, v in ids.items()}
        print(time.strftime("%H:%M:%S", time.gmtime()), statuses, flush=True)
        if all(s in TERMINAL for s in statuses.values()) or time.time() > deadline:
            return
        time.sleep(poll)


TEXT_SUFFIXES = {".md", ".csv", ".py", ".json", ".jsonl", ".bib", ".ipynb", ".txt"}


def download_files(c, key, files):
    """Save every file the trajectory wrote, under <key>_files/ by its workspace path, scrubbed if text."""
    dest_root = HERE / f"{key}_files"
    seen = set()
    for entry in files.get("data", []):
        ds = entry.get("data_storage") or {}
        rel = (ds.get("file_path") or ds.get("name") or ds["id"]).removeprefix("/workspace/").lstrip("/")
        if rel in seen or ds.get("is_collection"):
            continue
        seen.add(rel)
        dest = dest_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        got = c.fetch_data_from_storage(data_storage_id=ds["id"])
        if isinstance(got, list):
            got = got[0] if got else None
        if isinstance(got, Path) and got.is_dir():
            # The zip bundle comes back unpacked: outputs/ again plus our own uploaded inputs.
            print(key, "skipped", rel, "(unpacked bundle:", ", ".join(sorted(p.name for p in got.rglob("*"))[:6]), "...)")
            dest.with_name(dest.name + ".SKIPPED.txt").write_text(
                "Unpacked bundle; it duplicates outputs/ and the uploaded inputs, so it is not committed.\n")
            continue
        if isinstance(got, Path):
            data = got.read_bytes()
        elif got is not None and getattr(got, "content", None) is not None:
            data = got.content if isinstance(got.content, bytes) else str(got.content).encode()
        else:
            print(key, "could not fetch", rel, type(got).__name__, flush=True)
            continue
        if dest.suffix in TEXT_SUFFIXES:
            data = scrub(data.decode("utf-8", errors="replace")).encode()
        dest.write_bytes(data)
        print(key, "saved", rel, len(data), "bytes", flush=True)


def fetch(keys=None):
    c = client()
    ids = json.loads(IDS_FILE.read_text())["tasks"]
    for key, info in ids.items():
        if keys and key not in keys:
            continue
        task_id = info["task_id"]
        data = c.get_task(task_id=task_id).model_dump(mode="json")
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
        try:
            files = c.list_files(trajectory_id=task_id)
        except Exception as exc:  # literature jobs have no output files
            print(key, "list_files:", type(exc).__name__, flush=True)
            continue
        for entry in files.get("data", []):  # account identifiers, not needed to read the files
            (entry.get("data_storage") or {}).pop("user_id", None)
        (HERE / f"{key}_files.json").write_text(json.dumps(files, indent=1, default=str) + "\n")
        download_files(c, key, files)


if __name__ == "__main__":
    if sys.argv[1] == "fetch":
        fetch(sys.argv[2:] or None)
    else:
        {"submit": submit, "wait": wait}[sys.argv[1]]()
