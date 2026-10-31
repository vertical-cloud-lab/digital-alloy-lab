"""One Edison LITERATURE_HIGH task: why a re-sprayed BN coat on the atomizer's graphite crucible cracked (#219).

On 30 Oct 2026 the graphite crucible of the AMAZEMET rePOWDER was re-sprayed with Momentive Boron Nitride
Spray II after two 630 bronze (C63000) runs and left to dry in a fume hood; when the operator came back the
coat was cracked. The first coat, sprayed on the bare crucible before the 27 Oct run, did not crack.

    python run_edison.py submit   # create the task, write _task_ids.json
    python run_edison.py wait     # block until the task finishes (run in the foreground only)
    python run_edison.py fetch    # save the answer as markdown, plus metadata and the full trajectory as JSON

The API key is read from EDISON_PLATFORM_API_KEY and never printed. Names of partner-company or
national-lab staff to redact go in an untracked file (one per line) named by EDISON_REDACT_NAMES_FILE.
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


QUERY = """\
Context. We run an AMAZEMET rePOWDER ultrasonic atomizer. The charge is induction-melted in a graphite
crucible (grade not yet confirmed, probably a fine-grained isostatic graphite) whose interior is sprayed
with a boron nitride release coating, then pushed by argon pressure through a bottom hBN nozzle. The alloy
is nickel aluminum bronze UNS C63000 (Cu-10Al-5Ni-3Fe wt%) melted at 1300 C under argon, in charges of
0.86-1.08 kg.

The coating is Momentive Technologies "Boron Nitride Spray II, High-Temperature Release Coating"
(material number 2111750, 13 oz / 369 g aerosol can). Its SDS, as we read it (please verify), lists
hexagonal BN in ethanol and acetone, LPG (propane/butane) propellant and 1-5% organoclay (a
bentonite-based rheology additive), so the dry film is BN platelets with very little binder. Momentive
rates a can for roughly 100 sq ft.

History:
- Coat 1 (before a 27 Oct run): sprayed onto the clean, bare graphite and left to dry. It did NOT crack.
  It was not baked before use: the chamber filled with smoke at about 500 C during the first heat-up,
  with the metal charge already loaded (binder burnout in the furnace).
- After that run a thin metal skull stayed on the crucible bottom. When it was removed after cooling it
  pulled away crescent-shaped patches of the BN coat, leaving bare graphite. A second run used the
  crucible with those bare patches, without recoating.
- Coat 2 (30 Oct): the crucible was re-sprayed with the same product and left to dry in a laboratory fume
  hood. When the operator came back, the coat was cracked. It cracked at room temperature during drying,
  before any heating. We do not yet know: whether the old fired coat was fully stripped or the new coat
  went over it (or over the patch edges); how many passes, how far from the surface, or how long the can
  was shaken; whether the crucible had just been wiped with isopropanol (our recoat notes say to wipe with
  IPA and never water); the room humidity; the crack pattern (polygonal "mud-crack" network, curling
  flakes, or single long cracks); and whether only the coat cracked or the graphite too.

Please answer as a literature review with numbers and sources (papers with DOIs, manufacturer data sheets
and application instructions). Mark every estimate as an estimate and show its inputs. Start with a
short ranked list of the most likely causes, then cover:

1. Mechanism. Explain drying cracks in sprayed particulate coatings: capillary pressure in the drying
   particle network, constraint by the substrate, and the critical cracking thickness (for example Chiu
   et al. 1993 in J. Am. Ceram. Soc.; Routh and Russel; Tirumkudulu and Russel 2005; Singh and
   Tirumkudulu 2007; Lee and Routh; work on films of platelet particles). How do particle size, packing, platelet shape and
   orientation (hBN platelets of about 0.5-10 um), a few percent clay or organic binder, solvent surface
   tension (acetone and ethanol, about 22-23 mN/m) and drying rate change the critical thickness? Estimate
   the critical cracking thickness of a hBN-platelet film with 1-5% organoclay, and compare it with the
   wet and dry thickness an aerosol deposits per pass. How many grams of spray per square centimetre give
   what dry thickness? Is a dry BN film of 50-150 um above or below the critical thickness?
2. Substrate and history. Why would the same spray crack on a crucible that had already been coated and
   fired, when it did not crack on bare graphite? Consider: a porous, binder-free fired BN layer (or
   residual borate or B2O3) that wicks the solvent and consolidates the new film from below; poor adhesion
   or a weak boundary layer under the new film; locally doubled thickness where new spray overlaps old
   coat or fills the bare crescents; residues from the skull (Al2O3, metal, reaction products); solvent or
   moisture left in porous graphite or in the old coat after an IPA wipe; hydration of B2O3 or borate in
   the fired coat to boric acid; and porosity or surface texture of the graphite. Which of these are
   supported by literature or vendor guidance, and which are speculation?
3. Drying conditions. What does strong airflow (a fume hood face velocity of about 0.3-0.5 m/s) do to an
   acetone/ethanol BN film: faster evaporation, skin formation, lateral drying fronts, evaporative cooling
   below the dew point with water condensing into the film ("blushing"), and non-uniform drying in a deep
   cup? Would slower drying (still air, a lid, or gentle warming) avoid cracking? Quantify where you can.
4. Spray technique. Effects of insufficient shaking (BN settles quickly), spray distance, can and part
   temperature, a nearly empty can (lower propellant pressure giving a wetter, coarser spray), spraying
   into a deep cylindrical crucible (overspray pooling on the bottom and in the corner), and the number of
   passes and the flash time between them. Collect vendor instructions with numbers from Momentive, ZYP
   Coatings (BN Lubricoat and Hardcoat aerosols), Saint-Gobain (Combat), Henze (HeBoCoat), 3M and others,
   especially statements that cracking, flaking or peeling means the coat is too thick, and their advice
   on recoating over an existing or fired coat versus stripping it first.
5. Momentive Boron Nitride Spray II specifically. What do Momentive's technical data sheet, SDS and
   application notes say about composition, binder, thickness per coat, drying time, whether to bake
   before contact with metal, maximum use temperature in air and in inert gas, and recoating? Is another
   product (Momentive's water-based BN paints, or a hard-coat BN with an inorganic binder) better suited
   to repeated recoating of a graphite crucible for an aluminum-containing copper melt at 1300 C?
6. Consequences and diagnosis. How do you tell drying mud-cracks in the coat from cracks in the graphite
   (for example thermal-shock cracks that show through) or old cracks telegraphing through the new coat?
   Is a finely mud-cracked but adherent BN release coat acceptable for a 1300 C aluminum bronze melt, or
   does the melt penetrate the cracks, reach the graphite (Al4C3, carbon pickup, skull adhesion) and lift
   flakes into the melt and the nozzle? Must it be stripped?
7. Fix. Give a step-by-step strip, recoat, dry and inspect procedure for this product on a graphite
   crucible that avoids cracking: how to strip a cracked or fired BN coat without water, surface
   preparation, passes, thickness per pass and in total, flash time, where and how to dry, an optional
   low-temperature warm-up and the burnout or bake before the first melt, and pass/fail inspection
   criteria. Also propose a small coupon test (graphite offcuts) that would identify which factor caused
   the cracking, for example clean graphite versus a fired coat, fume-hood draft versus still air, and
   one versus three versus six passes, with weighing to estimate thickness.
"""

TASKS = {
    "literature_high_bn_cracking": (JobNames.LITERATURE_HIGH, QUERY),
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
        statuses = {k: str(c.get_task(task_id=v, verbose=True).status) for k, v in ids.items()}
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
        meta = scrub(meta)
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
