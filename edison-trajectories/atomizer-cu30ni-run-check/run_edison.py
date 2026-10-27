"""Edison check of the planned Cu-30Ni ultrasonic atomizer run (issue #219).

    python run_edison.py submit   # create the tasks, write _task_ids.json
    python run_edison.py wait     # block until every task finishes (foreground only)
    python run_edison.py fetch    # save each answer as markdown plus metadata JSON

The API key is read from EDISON_PLATFORM_API_KEY and never printed.
"""

import json
import os
import sys
import time
from pathlib import Path

from edison_client import EdisonClient, JobNames, TaskRequest

HERE = Path(__file__).resolve().parent
IDS_FILE = HERE / "_task_ids.json"
TERMINAL = {"success", "fail", "failed", "cancelled", "error"}

RUN_PLAN = """\
We are about to run an AMAZEMET rePOWDER ultrasonic atomizer with its induction-melting module: the
charge is melted in a crucible, then poured through a bottom nozzle, opened by lifting a stopper
("sealing") rod, onto an ultrasonically vibrating plate on the sonotrode inside an argon-filled
chamber. Earlier literature reviews for our lab put the rePOWDER induction module's practical limit
at about 1100-1300 C. So far we have atomized only aluminum alloys on this machine; this is our
first copper-nickel run.

Planned run:
1. Charge: 1.1 kg of 70 wt% Cu / 30 wt% Ni (binary cupronickel, close to UNS C71500 but possibly
   without its Fe and Mn additions). The charge may be pre-alloyed, or elemental Cu plus Ni pieces.
   Liquidus about 1240 C, solidus about 1170 C.
2. Stopper (sealing) rod: hexagonal boron nitride (BN).
3. Crucible: interior coated with BN (base crucible material not confirmed; consider graphite,
   alumina and other common choices).
4. Cleaning: the whole atomization chamber and the powder collection container are wiped with
   Kimwipes and isopropyl alcohol (IPA) beforehand.
5. Ultrasonics: 1:1.5 booster (amplitude gain) with the generator at 100% amplitude.
6. Atomizing surface: a carbon-fiber plate (likely a carbon-carbon composite) dip-coated in
   molybdenum, mounted on the sonotrode.
7. Argon pressures as set on the machine: "melting pressure" 0.1 bar (chamber pressure while
   induction melting), "graining pressure" 0.19 bar (overpressure used while pouring/atomizing to
   push melt through the nozzle), "turbo pressure" 1.5 bar (supply for the turbo / cooling /
   powder-transport gas stream). Our reading of these HMI labels may be imperfect; discuss sensible
   interpretations, including absolute versus gauge pressure.
"""

LITERATURE_QUERY = RUN_PLAN + """
Identify the problems, failure modes and complications each item could cause, with literature
evidence (and physical or thermodynamic reasoning where the literature is thin), quantified where
possible:

(a) Thermal window: superheat needed for reliable ultrasonic atomization of Cu-30Ni versus a ~1300 C
    induction limit; nozzle freeze-off, skull formation and freezing on the plate; time to dissolve
    Ni (melting point 1455 C) into molten Cu if charged as elemental pieces, and melt homogeneity;
    consequences of the ~70 C freezing range.
(b) BN stopper rod and BN-coated crucible against a Cu-Ni melt at 1250-1350 C: wetting,
    erosion/dissolution, B or N pickup, binder phases in hot-pressed BN (B2O3, calcium borate)
    softening or volatilizing, moisture uptake and outgassing, coating spallation, the stopper
    leaking or sticking in its seat; carbon pickup if the base crucible is graphite (C solubility in
    Cu-Ni).
(c) Molybdenum-dip-coated carbon-fiber plate: Ni-Mo and Cu-Mo interactions (Mo dissolution into
    Ni-containing melts, intermetallics), Mo-C reaction (Mo2C), coating CTE mismatch and spallation
    under ultrasonic loading and thermal shock, Ni attack on carbon fiber where the coating is
    breached, wetting of Cu-Ni on Mo versus carbon, Mo or C contamination of the powder, Mo
    oxidation (volatile MoO3) with residual oxygen, plate damping/heating, resonance-frequency shift
    and fatigue.
(d) Ultrasonic settings: what a 1:1.5 booster at 100% amplitude implies for a dense,
    high-surface-tension melt (Cu-30Ni surface tension ~1.3-1.5 N/m, liquid density ~7.9-8.0 g/cm3):
    median droplet size from Lang's relation at 20-40 kHz, the atomization threshold amplitude, the
    risks of too much amplitude (spatter, coarse droplets, satellites, chaotic breakup, plate
    cracking, generator overload or loss of frequency tracking), and how melt flow rate compares
    with the atomization capacity of the plate (flooding).
(e) Pressures: Cu evaporation and composition shift at 0.1 bar absolute and ~1300 C (vapour
    pressures of Cu versus Ni; Mn loss if C71500-type feedstock containing Mn is used), condensate on
    viewports and the coil; arcing or glow discharge at the induction coil at reduced argon pressure
    (Paschen); whether a ~0.09 bar pressure difference plus metallostatic head overcomes the
    capillary threshold of a non-wetting BN nozzle and what melt flow rate results; effect of a
    1.5 bar gas stream on droplet trajectories, satellite formation, cooling and fines carry-over.
(f) Cleaning with IPA and Kimwipes: residual IPA, water and lint as sources of O, H and C;
    flammability of IPA vapour in the chamber before pumping and inerting; cross-contamination from
    earlier aluminum-alloy runs (Al, Si, Mg, Ce powder left in the chamber or collector).
(g) Powder quality and safety: oxygen pickup, hydrogen porosity in Cu-Ni, expected particle size and
    sphericity compared with published ultrasonic atomization of copper and nickel alloys,
    inhalation and sensitization hazards of nickel-containing powder, combustibility of fine Cu-Ni
    powder when the chamber is vented.
(h) The powder is for a marine/defense application. Does a binary Cu-30Ni meet UNS C71500 or the
    relevant military specification chemistry (Fe, Mn limits), and how do Fe and Mn affect seawater
    corrosion and erosion-corrosion behaviour?

Finish with a table of parameter -> potential problem -> likelihood/severity -> recommended
mitigation or pre-run check, then list which parameters you would change, and to what.
"""

PRECEDENT_QUERY = """\
Has anyone ultrasonically atomized copper-nickel (cupronickel) alloys such as Cu-30Ni (UNS C71500)
or Cu-10Ni (UNS C70600) into powder, especially by melting in an induction crucible and pouring
through a nozzle onto a vibrating sonotrode (for example an AMAZEMET rePOWDER or a similar
ultrasonic atomizer)? If so, report the melt temperature and superheat, the sonotrode or plate
material (molybdenum, TZM, graphite or carbon composite, ceramic), frequency and amplitude, gas
atmosphere and pressures, crucible and stopper materials (for example boron nitride), particle size
distribution, sphericity, oxygen content, and any problems reported (nozzle clogging, freezing on
the sonotrode, plate erosion or reaction with the melt, contamination). If not, give the closest
precedents: ultrasonic atomization of pure Cu, Cu alloys or Ni alloys; gas atomization of
cupronickel; contact between Cu-Ni melts and boron nitride or molybdenum.
"""

TASKS = {
    "literature_high": (JobNames.LITERATURE_HIGH, LITERATURE_QUERY),
    "precedent": (JobNames.PRECEDENT, PRECEDENT_QUERY),
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
        answer = data.get("formatted_answer") or data.get("answer") or ""
        meta = {k: data.get(k) for k in ("task_id", "status", "job_name", "created_at", "query",
                                          "has_successful_answer", "total_cost", "total_queries")}
        (HERE / f"{key}.json").write_text(json.dumps(meta, indent=2) + "\n")
        if answer:
            (HERE / f"{key}.md").write_text(
                f"# Edison {meta['job_name']} result: {key}\n\n"
                f"**Task ID:** `{task_id}`  \n**Status:** {meta['status']}\n\n"
                f"<details><summary>Query</summary>\n\n```text\n{meta['query']}\n```\n\n</details>\n\n"
                f"{answer}\n")
        print(key, meta["status"], len(answer), "chars", flush=True)


if __name__ == "__main__":
    {"submit": submit, "wait": wait, "fetch": fetch}[sys.argv[1]]()
