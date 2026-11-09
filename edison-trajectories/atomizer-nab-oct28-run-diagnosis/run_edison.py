"""Edison check of why the second 630 bronze (C63000) atomizer run on 28 Oct 2026 failed (#219).

Run A (27 Oct, k7m2q9) atomized ~97% of a 1.08 kg charge. Run B (28 Oct) reused the plate, nozzle and
crucible, with BN missing from patches of the crucible coat, and most of the melt ended up in the catch
crucible. These tasks ask about re-applying the BN coat and about the ultrasonics.

    python run_edison.py submit   # create the tasks, write _task_ids.json
    python run_edison.py wait     # block until every task finishes (foreground only)
    python run_edison.py fetch    # save each answer as markdown, plus metadata and the full trajectory as JSON

The API key is read from EDISON_PLATFORM_API_KEY and never printed. Names of partner-company staff to
redact go in an untracked file (one per line) named by EDISON_REDACT_NAMES_FILE.
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
REDACTIONS = [
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "[email redacted]"),
    (re.compile(r"(?i)\b(?:tel|phone|fax)\b\.?:?\s*[\d\s().+-]{7,}\d"), "[phone redacted]"),
    (re.compile(r"\+\d[\d\s().-]{8,}\d"), "[phone redacted]"),
]
if os.environ.get("EDISON_REDACT_NAMES_FILE"):
    for name in Path(os.environ["EDISON_REDACT_NAMES_FILE"]).read_text().splitlines():
        if name.strip():
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
Context. We run an AMAZEMET rePOWDER ultrasonic atomizer: a charge is induction-melted in a crucible,
argon over-pressure ("graining" pressure) pushes the melt through a bottom nozzle once a stopper
(sealing) rod is lifted, the stream falls onto an inclined plate driven by an ultrasonic sonotrode
(booster plus horn), and melt that the plate does not atomize runs off into a catch crucible below.
A separate "turbo" button applies 1.5 bar to push the melt out (it replaces, rather than adds to, the
graining pressure). Pressures are read on the HMI; whether they are gauge or absolute is unconfirmed.

Alloy: nickel aluminum bronze UNS C63000 ("630 bronze" rod; Cu-10Al-5Ni-3Fe wt%; liquidus ~1054 C;
liquid density ~6.9-7.0 g/cm3; surface tension ~1.1-1.3 N/m). Melt setpoint 1300 C (the module's
hard limit; ~245 C superheat), read by a thermocouple at the crucible. Crucible: graphite (material to
be confirmed) with its interior sprayed with a boron nitride paint; BN stopper rod; hBN nozzle (bore
about 0.5 mm, to be confirmed). Plate: carbon-fiber composite coated with tungsten (the vendor's
W-coated plate for copper alloys). Booster 1:1.5. Argon atmosphere. In training with aluminum, the
vendor's trainer set the plate so that the melt landed on the plate and rolled down about a third of
the plate's length before it atomized.

Run A (27 Oct): new plate, fresh BN coat, new nozzle, 1080 g charge (four rod pieces), O2 24 ppm,
amplitude 90%, graining 0.19 bar, held 2 min after the charge melted. The stream hit right at the
lower (free) end of the plate. The melt kept flowing only while the operator held the turbo (1.5 bar)
for most of the run; ~97% of the charge was collected as powder, with a visible fraction of flakes.
A thin metal skull stayed on the crucible bottom. When it was removed after cooling, BN came away with
it: light grey crescents of BN on the underside of the skull match the bare patches in the crucible's
coat.

Run B (28 Oct): the same plate (second use; it looked fine), the same nozzle (the bore looked clear),
the same crucible with small bare patches where the BN had come off (not recoated), 858 g charge (five
rod pieces), O2 11 ppm, amplitude 90% for the first quarter of the pour, then 100%; graining 0.23 bar
at the start, back to 0.19 bar about halfway; held 1 min after melting. The plate was moved up a little
so that the stream landed farther up the plate rather than at its very end. Result: the melt "really
struggled to atomize"; some powder was made, but most of the charge ended up as a solid puck in the
catch crucible. Changing amplitude and pressure during the pour did not help.
"""

BN_QUERY = CONTEXT + """
Focus on the boron nitride coating of the crucible (and of the stopper rod and nozzle). Give numbers
with sources (manufacturer data sheets, foundry practice, papers with DOIs) and mark any estimate.

1. Why would a C63000 skull bond to a sprayed BN coat strongly enough to pull the coat off the
   crucible on cooling? Consider the binders in common BN paints and aerosols (aluminum phosphate,
   silicate, B2O3, organic binders), reaction of the Al in the melt with B2O3 or silica in the binder
   (and the wetting this causes), Al2O3 films, thermal contraction mismatch, coat thickness, and
   whether the coat was fully dried and baked before the first melt.
2. Best practice for re-applying BN on a graphite crucible used for copper alloys and aluminum
   bronze: surface preparation (removing loose coating and skull residue; abrading or not; solvent
   cleaning; avoiding water), stripping the whole coat versus patching the bare spots, number of coats,
   target thickness, drying time between coats, the cure or bake schedule (temperature, atmosphere such
   as air, argon or vacuum, and ramp rate), re-baking to drive off absorbed moisture before use, how to
   check coverage and adhesion, and how many melts a coat typically lasts. Include vendor guidance
   with numbers (for example ZYP Coatings BN Lubricoat and Hardcoat, Momentive or Saint-Gobain Combat
   BN paints, Henze BN, 3M) and say which product types suit an aluminum-containing copper melt.
3. What a patched or partly bare coat does to a C63000 melt at 1300 C: wetting of bare graphite by
   Cu-Al melts (Al4C3 formation), carbon pickup, skull adhesion and melt retention, flakes of coating,
   binder or skull entering the melt and lodging in a ~0.5 mm nozzle bore or otherwise disturbing the
   stream, and B, Si or P pickup in the powder. Could the bare patches or coating debris plausibly
   have caused run B's poor atomization, or are they mainly a contamination and crucible-life issue?
4. Avoiding and removing the skull: draining the crucible fully, end-of-pour pressure, crucible shape,
   keeping the crucible hot until drained, and removing a skull without taking the coat with it.
5. Alternatives for aluminum bronze: thicker or hard-coat BN, solid hBN or pyrolytic BN liners,
   alumina, zirconia or magnesia crucibles, and zirconia or yttria washes.
6. A step-by-step recoat, cure and inspection procedure for the next run, with a go/no-go checklist.
"""

ULTRASONIC_QUERY = CONTEXT + """
Focus on the ultrasonic atomization itself and what differed between run A and run B. Give numbers
with sources (DOIs) and show the inputs to any estimate.

1. Capillary-wave atomization needs a thin melt film that wets the plate and a vibration amplitude
   above threshold. For liquid C63000 at 1150-1300 C (viscosity ~4-5 mPa s) and, for comparison,
   liquid aluminum, estimate the capillary wavelength and median droplet size at 20, 35 and 40 kHz,
   the threshold amplitude, the thickest film that still atomizes, and the largest mass flow rate a
   plate can atomize per unit area and per unit acoustic power. How does NAB's ~2.8x higher density
   than aluminum change the needed amplitude, the plate's capacity, and how far the film runs down an
   inclined plate before it atomizes?
2. Plate position: for a plate driven by a sonotrode, how does the vibration amplitude vary over the
   plate (flexural modes, nodal lines, the free end versus near the horn)? If the stream lands higher
   up the plate instead of at its free end, could it fall near a node or a low-amplitude zone and fail
   to atomize? How should the impact point be chosen and checked (for example a powder or water
   pattern on the vibrating plate, or a laser vibrometer)?
3. Plate reuse: what does one ~1 kg run of NAB do to a W-coated carbon-fiber plate (adhered metal or
   an Al2O3 film, coating dissolution or cracking where the stream landed, poorer wetting of an
   oxidized surface, added mass that detunes the resonance, a joint to the sonotrode loosened by
   thermal cycling)? Estimate the frequency shift from a few grams of adhered metal. Which of these
   could make a second run fail? How should the plate be inspected and cleaned between runs, and which
   generator readings (frequency, power, amplitude, overload or error flags) show a detuned or
   damaged plate?
4. Flow rate versus capacity: estimate the mass flow through a 0.5 mm and a 1 mm nozzle at 0.19 and
   0.23 bar and at 1.5 bar turbo, with the metallostatic head of 858 g versus 1080 g in a crucible of
   ~50-60 mm inner diameter, and say whether exceeding the plate's capacity makes melt run off the plate
   into the catch crucible. Does run A's success with turbo held suggest the plate can take high flow
   when the stream lands at the free end?
5. Thermal effects: plate temperature during the pour, cooling of the film on the plate, freezing or
   solid build-up on the plate that stops atomization, the effect of a 1 min versus 2 min hold on the
   melt temperature reaching the nozzle, and whether raising amplitude from 90% to 100% mid-pour helps
   or hurts (transducer heating, frequency drift, splashing).
6. Rank the candidate causes of run B's failure by likelihood, and give a plan for the next run: which
   single variable to change first, what to log (generator frequency and power, pressures, where the
   stream lands, video), a plate-position rule for NAB versus aluminum, and pass/fail criteria.
"""

PRECEDENT_QUERY = """\
Find reports of ultrasonic atomization of metals (plate or sonotrode atomizers such as the AMAZEMET
rePOWDER, or laboratory ultrasonic atomizers) where a run partly failed: melt that did not atomize and
ran off the plate or sonotrode into the collector, solid build-up on the plate, lower yield on a
second run with a reused plate or sonotrode, nozzle clogging, or loss of resonance. Prefer copper
alloys, aluminum bronze or other aluminum-containing melts. For each report give the alloy, set-up,
the cause the authors identified and the fix. Also report any published guidance on where the melt
stream should land on the plate, on plate inclination, and on how plates are cleaned or replaced
between runs.
"""

TASKS = {
    "literature_high_bn_recoat": (JobNames.LITERATURE_HIGH, BN_QUERY),
    "literature_high_ultrasonics": (JobNames.LITERATURE_HIGH, ULTRASONIC_QUERY),
    "precedent_failed_runs": (JobNames.PRECEDENT, PRECEDENT_QUERY),
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


def wait(max_minutes=float(os.environ.get("EDISON_WAIT_MINUTES", "45")), poll=120):
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
