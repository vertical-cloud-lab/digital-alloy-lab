"""Edison follow-up for issue #219: a tungsten- instead of molybdenum-dipped carbon-fiber plate.

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

QUERY = """\
We plan to ultrasonically atomize 1.1 kg of 70 wt% Cu / 30 wt% Ni (liquidus ~1240 C, melt at roughly
1260-1300 C) in an AMAZEMET rePOWDER: the melt is induction-melted in a BN-coated crucible and poured
through a bottom nozzle (BN stopper rod) onto an ultrasonically vibrating plate on the sonotrode
(1:1.5 booster, 100% amplitude) in argon. The atomizing plate is a carbon-fiber (likely carbon-carbon
composite) plate. A previous review found that a molybdenum dip coat on that plate is a high risk:
a Cu-32Ni melt dissolves ~3.7 wt% Mo at 1300 C (Teodorovich 1980), a Ni-rich alloy atomized on a Mo
sonotrode in a rePOWDER picked up ~2.6% Mo (Goncharov 2026, doi:10.3390/met16030318), so a thin coat
is likely eaten through, exposing carbon that Cu-Ni wets poorly.

A colleague now proposes dipping the carbon-fiber plate in TUNGSTEN instead of molybdenum. Compare a
W coating with a Mo coating for this run, quantified and with literature evidence where possible:

(a) Solubility and dissolution rate of W versus Mo in liquid Cu-Ni (and in liquid Ni and Cu
    separately) at 1250-1350 C; Cu-Ni-W and Cu-Ni-Mo phase equilibria; evidence from W-Ni-Cu
    heavy alloys (liquid-phase sintering, W solubility in the Ni-Cu matrix, solution-reprecipitation)
    and from Mo-Ni-Cu systems; how many micrometres of W or Mo a film of melt would remove in the
    seconds-to-minutes of contact during a 1.1 kg pour, including ultrasonic/cavitation erosion.
(b) Wetting: contact angle of Cu-Ni melts on W versus Mo versus carbon; is good wetting desirable
    on an ultrasonic atomizing plate, and does the Ni activation of W wetting matter?
(c) W-C reaction (W2C, WC) versus Mo2C at the coating/carbon interface during dip coating and at
    run temperature; embrittlement and adhesion.
(d) Thermo-mechanics under ultrasonic loading: CTE of W (~4.5e-6/K) and Mo (~5e-6/K) versus a C/C
    composite; density (W 19.3 vs Mo 10.2 g/cm3) and the added mass and resonance-frequency shift of a
    coated plate for a given coating thickness; brittleness/DBTT of W versus Mo, fatigue and spallation
    under thermal shock.
(e) What "dipped in tungsten" can even mean practically, given W melts at 3422 C (versus Mo 2623 C):
    slurry/paint plus sintering, CVD, plasma spray, etc.; achievable thickness, porosity and
    adhesion, and whether porosity lets Cu-Ni reach the carbon.
(f) Oxidation: WO3 versus MoO3 volatility with residual oxygen in the argon.
(g) Powder contamination: W versus Mo pickup and its consequence for a marine/defense UNS C71500
    type powder; W particle inclusions.
(h) Alternatives worth considering for a Cu-Ni melt (solid W or Mo plate, TZM, W-coated Mo,
    ceramics such as BN, alumina, zirconia, SiC coatings) and what is known about their use on
    ultrasonic atomizers.

Finish with a direct verdict (W better / similar / worse than Mo for this run, and why) and a table
of risk -> Mo coat -> W coat -> mitigation.
"""

TASKS = {
    "literature_w_vs_mo": (JobNames.LITERATURE, QUERY),
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
