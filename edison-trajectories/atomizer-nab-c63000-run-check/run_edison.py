"""Edison re-check of the #219 atomizer run for the alloy actually used: 630 bronze (UNS C63000).

Every earlier Edison pass on #219 (../../ on branches claude/issue-219-20261027-2020 and -2129) assumed
binary Cu-30Ni. The charge was nickel aluminum bronze C63000 (Cu-10Al-5Ni-3Fe), so these tasks redo the
parameter check for that alloy and ask about what run 1 on Oct 27 showed: the melt kept flowing only
while the turbo pressure was held, and the powder contains shiny flakes.

    python run_edison.py submit   # create the tasks, write _task_ids.json
    python run_edison.py wait     # block until every task finishes (foreground only)
    python run_edison.py fetch    # save each answer as markdown, plus metadata and the full trajectory as JSON

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
# and CLAUDE.md bars those, so scrub every decoded string before saving. Names of partner-company staff
# to redact go in an untracked file (one per line) named by EDISON_REDACT_NAMES_FILE, so that this
# script never spells them out.
REDACTIONS = [
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[email redacted]"),
    (re.compile(r"(?i)\b(?:tel|phone|fax)\b\.?:?\s*[\d\s().+-]{7,}\d"), "[phone redacted]"),
    (re.compile(r"\+\d[\d\s().-]{8,}\d"), "[phone redacted]"),
]
if os.environ.get("EDISON_REDACT_NAMES_FILE"):
    for name in Path(os.environ["EDISON_REDACT_NAMES_FILE"]).read_text().splitlines():
        if name.strip():
            # Not inside a longer word ("Duran" spares "endurance"), but citation keys such as
            # "name2023title" are still caught.
            pattern = r"(?<![^\W\d_])" + re.escape(name.strip()) + r"(?![^\W\d_])"
            REDACTIONS.append((re.compile(pattern, re.I), "[name redacted]"))


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
Context. On 27 Oct 2026 we ultrasonically atomized 1,080 g of nickel aluminum bronze UNS C63000
("630 bronze", ASTM B150 rod; nominal Cu-10Al-5Ni-3Fe wt%; limits Al 9.0-11.0, Ni 4.0-5.5, Fe 2.0-4.0,
Mn <= 1.5, Si <= 0.25, Zn <= 0.30; solidus ~1035 C, liquidus ~1054 C; density 7.58 g/cm3) in an
AMAZEMET rePOWDER ultrasonic atomizer. An earlier review wrongly assumed the alloy was binary Cu-30Ni
(liquidus ~1240 C), so its conclusions (only ~60 C of superheat at 1300 C, heavy dissolution of a Mo or
W plate coating by a Ni-rich melt, C71500 chemistry) must be re-checked for C63000.

Set-up: induction melting in a graphite crucible whose interior was sprayed with a boron nitride
coating (aerosol BN paint) and dried; a boron nitride sealing (stopper) rod (the written plan called for
alumina); an hBN bottom nozzle (planned bore 0.5 mm); chamber and powder container wiped with lint-free
wipes and isopropanol beforehand; argon atmosphere with 24 ppm O2 at the pour. HMI pressures: melting
0.1 bar, "graining" (pouring) 0.19 bar, "turbo" 1.5 bar; we have not confirmed whether these are gauge
or absolute. Melt setpoint 1300 C, read by a type N thermocouple at the crucible wall (the module's
stated maximum), held about 2 min after the charge melted. Atomizing surface: a carbon-fiber composite
plate coated with tungsten (described as "dipped in W"; the vendor's kit includes a W plasma-coated
carbon-fiber plate that it recommends for copper alloys) on a 1:1.5 booster at 90% generator
amplitude.

Outcome of run 1: atomization ran to the end of the charge and the operator estimates ~97% yield, but
the melt only kept flowing while the operator held the turbo (1.5 bar) pressure almost the whole time.
The powder is gold-coloured and contains a visible fraction of shiny flakes. A thin skull remained in
the crucible, and fine gold-coloured dust coated the chamber walls.
"""

LITERATURE_QUERY = CONTEXT + """
Please re-assess the run parameters for C63000, give numbers with sources, and show the inputs to any
estimate where the literature is silent.

1. Melt temperature. 1300 C is ~245 C above the liquidus. Compare with foundry pouring temperatures
   for aluminum bronzes (C95800, C95500, C63000), with gas atomization of nickel aluminum bronze for
   additive manufacturing, and with the published ultrasonic atomization of NAB on this kind of
   atomizer (e.g., doi:10.3390/ma17143396 and doi:10.1088/1757-899X/1296/1/012036, which melted at
   1300 C). What does excess superheat cost here (oxidation and dross, Al and Mn loss, attack on the
   crucible, rod, nozzle and plate, plate overheating, particle shape), and what does too little risk
   (freezing in a 0.5 mm nozzle, skulls)? Recommend a setpoint range for the next run.

2. Why did the melt need near-continuous turbo pressure to keep flowing? Weigh these with estimates:
   (a) Al2O3 skin, dross and oxide bifilms on an aluminum bronze melt, collecting in or over a 0.5 mm
   nozzle (compare alumina clogging of nozzles in Al-killed steel casting, and aluminum bronze oxide
   behaviour in foundry practice); (b) freezing at the nozzle exit (cold nozzle, gas flow beneath it);
   (c) capillary back-pressure of a non-wetting melt in a 0.5 mm bore (surface tension of liquid
   Cu-10Al roughly 1.1-1.3 N/m, contact angle on hBN), compared with 0.19 bar plus the metallostatic
   head; (d) reaction products from the BN coating or rod; (e) the pressure difference across the
   melt if the chamber pressure rises during the pour. How should we diagnose this, and what should we
   change (bore size, nozzle preheat, O2 target, skimming or filtering, graining pressure)?

3. Compatibility of a C63000 melt at 1250-1300 C with each material it touches, using thermodynamic
   estimates: the activity of Al (and of Fe and Ni) in liquid Cu-10Al-5Ni-3Fe; whether Al + BN ->
   AlN + B, Al + C -> Al4C3, or Al reduction of Al2O3-SiO2 binders can proceed at that activity;
   carbon pickup by the Fe and Ni from a graphite crucible or carbon-fiber plate; boron and nitrogen
   pickup; silicon from a silicate binder in the BN paint. Is a BN-painted graphite crucible suitable
   for aluminum bronze, and is a BN or an alumina sealing rod the better choice?

4. The plate. The earlier review used 0.66 wt% W and 3.7 wt% Mo saturation in Cu-30Ni at 1300 C. How
   much W (and Mo) can a Cu-10Al-5Ni-3Fe melt dissolve at 1250-1300 C, given the much lower Ni, the
   Fe, and the Al (Al-W and Al-Mo intermetallics)? How do Al-bronze melts wet W, Mo and carbon, and
   what does the alumina skin do to that? Estimate W pickup in the powder and plate life over repeated
   runs. Is a W-coated carbon-fiber plate appropriate for NAB, and how should it be inspected?

5. Flakes. What produces flakes or splats in ultrasonic atomization (melt flow above the plate's
   atomization capacity, a film too thick to break up, droplets hitting the walls or splash guards
   before they solidify, high amplitude ejecting large ligaments), how would holding the turbo
   pressure (higher flow rate) change this, and how do oxide skins on aluminum bronze affect
   sphericity? How should the flake fraction be measured and reduced?

6. Powder for additive manufacturing and naval parts: expected oxygen pickup (ppm) for aluminum
   bronze powder made in argon with ~20-30 ppm O2, and typical O, N and C limits for NAB powder for
   laser powder-bed fusion or directed energy deposition; the rapid-solidification microstructure
   (martensitic beta-prime, suppressed kappa phases) and the post-build heat treatment usually needed
   for corrosion resistance in seawater; and whether anything in these parameters is likely to push
   the powder out of C63000 limits (Al or Mn loss, W, B, C or Si pickup; C63000 requires Cu plus named
   elements >= 99.5%).

7. Charge size: we charged 1.08 kg, against 250-500 g in the vendor's guidance and published runs.
   What does a larger charge change (time to melt, temperature non-uniformity and thermocouple lag,
   plate heat load and coating wear over a longer pour)?

8. Safety for handling this powder (Ni content, combustible metal dust).

Finish with (a) a table: parameter -> issue for C63000 -> evidence or estimate -> recommended setting
for the next run; and (b) a list of which conclusions of a Cu-30Ni assessment no longer apply, which
still apply, and which new risks C63000 adds.
"""

PRECEDENT_QUERY = """\
Has anyone ultrasonically atomized nickel aluminum bronze or aluminum bronze (UNS C63000, C95800,
C95500, CuAl10Ni5Fe4, CuAl10Fe3 and similar), for example in an AMAZEMET rePOWDER or another
ultrasonic atomizer? For each report give the feedstock, melt temperature, crucible, nozzle and plate
(sonotrode) materials, frequency and amplitude, atmosphere and oxygen level, yield, particle size
distribution, morphology (satellites, flakes, irregular particles), oxygen content, and any problems
such as nozzle clogging, plate wear or interrupted flow. If there are none, give the closest
precedents: ultrasonic atomization of other aluminum-containing copper alloys, and gas atomization of
nickel aluminum bronze powder for laser powder-bed fusion or directed energy deposition.
"""

TASKS = {
    "literature_high_nab": (JobNames.LITERATURE_HIGH, LITERATURE_QUERY),
    "precedent_nab_ultrasonic": (JobNames.PRECEDENT, PRECEDENT_QUERY),
}


def client():
    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def submit():
    if IDS_FILE.exists():
        sys.exit(f"{IDS_FILE.name} already exists; refusing to resubmit")
    c = client()
    ids = {}
    for key, (job, query) in TASKS.items():
        ids[key] = str(c.create_task(TaskRequest(name=job, query=query)))
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
