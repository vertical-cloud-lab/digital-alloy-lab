"""Higher-fidelity Edison pass for issue #219: a tungsten- instead of molybdenum-dipped carbon-fiber plate.

The broad LITERATURE comparison of W and Mo is in ../atomizer-cu30ni-w-plate/. These tasks ask for the
numbers that decide the question: W solubility and dissolution rate in a Cu-30Ni melt, how W coatings on
carbon-fiber composites fail, what "dipping" in W can mean, and any W sonotrode precedent.

    python run_edison.py submit   # create the tasks, write _task_ids.json
    python run_edison.py wait     # block until every task finishes (foreground only)
    python run_edison.py fetch    # save each answer as markdown, plus metadata and the full trajectory as JSON

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

CONTEXT = """\
Context. We will ultrasonically atomize 1.1 kg of 70 wt% Cu / 30 wt% Ni (binary cupronickel, near
UNS C71500; liquidus ~1240 C, solidus ~1170 C) in an AMAZEMET rePOWDER. The charge is induction-melted
in a BN-coated crucible to roughly 1260-1300 C (the induction module's practical limit is ~1300 C), then
poured in argon through a bottom nozzle (BN stopper rod) onto a horizontal plate on an ultrasonic
sonotrode (1:1.5 booster, 100% generator amplitude). The plate is the atomizing surface: a thin melt
film on it is continuously renewed for the length of the pour, likely 5-30 minutes. The plate is a
carbon-fiber composite (probably carbon-carbon) that was "dipped" in molybdenum. A previous review
flagged the Mo coat as high risk: a Cu-32Ni melt dissolves ~3.7 wt% Mo at 1300 C (Teodorovich 1980,
doi:10.1007/bf00791375), and a Ni-rich alloy atomized on a solid Mo sonotrode in a rePOWDER picked up
~2.6 wt% Mo (Goncharov 2026, doi:10.3390/met16030318). A colleague now proposes a carbon-fiber plate
dipped in TUNGSTEN instead.
"""

LITERATURE_QUERY = CONTEXT + """
A separate, broader query is already comparing W and Mo qualitatively. For this one we need numbers
with sources, and physical estimates with the inputs shown where the literature is silent.

1. Solubility of W in the melt. Report the equilibrium solubility of W (wt% and at%) in liquid
   Cu-30Ni, and along the Cu-Ni join, at 1250, 1300 and 1350 C, from experimental Cu-Ni-W phase
   equilibria and CALPHAD assessments (name them and give their values). Cross-check against:
   (i) the Ni-W binary (W in liquid Ni near the ~1495 C peritectic; (Ni) dissolves ~17.5 at% W);
   (ii) Cu-W (W solubility in liquid Cu); (iii) the W content of the Ni-Cu matrix in
   liquid-phase-sintered W-Ni-Cu heavy alloys versus Ni:Cu ratio and sintering temperature;
   (iv) Mo in the same melts. At W saturation and 1250-1300 C, is the phase in equilibrium with the
   melt pure (W), a (Ni,W) fcc solid solution, or a Ni-W intermetallic (Ni4W, NiW)? Could a solid
   Ni-W-rich layer form and grow on the plate, raising the local liquidus and seeding freezing of
   the thin film?

2. Rate of attack. Give measured dissolution rate constants or recession rates of W, and of Mo for
   comparison, in liquid Ni, Cu-Ni or Ni-base melts (rotating-disc, immersion or diffusion-couple
   studies, e.g., W wire or W crucibles in Ni-base superalloy melts), and say whether dissolution is
   diffusion- or interface-controlled. Report what is known about ultrasonic or cavitation
   enhancement of dissolution and erosion of W, Mo, Nb, Ti or steel sonotrodes in metal melts. Then
   estimate, with stated assumptions, the recession depth (micrometres) at the melt impingement zone
   for a W coat and for a Mo coat during a 10-30 minute pour, and the resulting W or Mo content of
   the 1.1 kg of powder.

3. W coatings on carbon-fiber composites. Summarize precedents with numbers: the JET ITER-like wall W
   coatings on CFC (combined magnetron sputtering and ion implantation, ~10-25 um W on a Mo
   interlayer), vacuum-plasma-sprayed W on CFC or graphite, and CVD W on C/C. Give their adhesion,
   the thickness above which they delaminate, cracking under thermal cycling and high heat flux, the
   onset temperature and growth rate of W2C/WC at the W/C interface and its effect on adhesion,
   diffusion barriers (Re, Mo), and recrystallization and embrittlement of W coatings at 1200-1400 C.
   How would such coatings respond to sustained 20-60 kHz vibration at an atomizing plate's
   displacement amplitude?

4. What "dipping" in W can practically mean, since W melts at 3422 C: slurry or paint dip coats with
   sintering (temperatures; sintering aids such as Ni, Fe or Co that would themselves dissolve in
   Cu-Ni), molten-salt electrodeposition of W, CVD from WF6, chemical vapour infiltration, and thermal
   spray. Give typical thickness, density or porosity and adhesion for each, and say whether a porous
   W layer would be infiltrated by a Cu-Ni melt (W-Cu composites are made by infiltrating porous W
   with Cu, and Ni activates the wetting), giving the melt a path to the carbon.

5. Wetting. Contact angles of liquid Cu, Ni and Cu-Ni on W, on Mo and on graphite or carbon fiber at
   1100-1400 C in argon or vacuum, including the effect of surface oxides (WO2/WO3, MoO2/MoO3) and of
   Ni as a wetting activator. Is complete wetting desirable on an ultrasonic atomizing plate, or does
   it promote film pinning, infiltration and erosion?

6. Acoustics. For a thin plate on an ultrasonic horn, estimate the added mass and the
   resonant-frequency shift from a W coat versus a Mo coat of the same thickness (densities 19.3 and
   10.2 g/cm3; C/C ~1.6-1.9 g/cm3), for 25, 100 and 250 um per side on a 2-3 mm plate, and say
   whether a typical generator's frequency-tracking range would still lock. Comment on damping and
   heating in a porous coat.

7. Powder consequences. At the W pickup estimated in item 2, would W stay in solution in Cu-30Ni
   powder or appear as W particles, and what would it do to compliance with UNS C71500 (and the
   military specifications that cite it), to seawater corrosion, and to laser powder-bed fusion?

Finish with (a) a direct verdict on W versus Mo for this run, (b) a table of failure mode -> Mo coat
-> W coat (numbers where possible) -> mitigation, and (c) the plate you would choose for this run and
why (solid Mo or TZM, solid W or W-La2O3, W-coated Mo, or a ceramic such as BN, alumina, zirconia or
SiC-coated C/C), naming any ultrasonic-atomization or ultrasonic-melt-processing precedent for it.
"""

PRECEDENT_QUERY = """\
Has anyone used tungsten, a tungsten alloy (W-Re, W-La2O3, W-Ni-Fe or W-Ni-Cu heavy alloy) or a
tungsten-coated carbon or graphite part as an ultrasonic sonotrode, horn tip or atomizing plate in
contact with molten metal, especially copper, nickel or copper-nickel alloys (for example in an
AMAZEMET rePOWDER or another ultrasonic atomizer, or in ultrasonic melt treatment)? If so, report the
melt, temperature, frequency and amplitude, how long the part lasted, how much it eroded or dissolved,
and how much W ended up in the product. If not, give the closest precedents: W or W-coated parts in
contact with molten Cu or Ni alloys (crucibles, nozzles, thermocouple sheaths, casting molds), and Mo
or Nb sonotrodes used with Cu or Ni melts.
"""

TASKS = {
    "literature_high_w_plate": (JobNames.LITERATURE_HIGH, LITERATURE_QUERY),
    "precedent_w_sonotrode": (JobNames.PRECEDENT, PRECEDENT_QUERY),
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
        verbose = c.get_task(task_id=task_id, verbose=True).model_dump(mode="json")
        (HERE / f"{key}_trajectory.json").write_text(json.dumps(verbose, indent=1, default=str) + "\n")
        print(key, meta["status"], len(answer), "chars", flush=True)


if __name__ == "__main__":
    {"submit": submit, "wait": wait, "fetch": fetch}[sys.argv[1]]()
