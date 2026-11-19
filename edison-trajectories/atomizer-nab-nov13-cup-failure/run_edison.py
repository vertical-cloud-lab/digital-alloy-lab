"""Edison check of the Nov 13 2026 630 bronze (C63000) atomizer run (#269, #219).

The plate barely atomized, coarse shot and molten bronze reached the collection container, the seal
between the chamber's cone and the container smoked, a white crust was left where that seal sits, and
the container's glass cylinder cracked at its top rim. Before the run the O2 reading stuck at its
1000 ppm limit after the machine was switched off by accident. These tasks ask why, and how to stop it.

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
Context. We run an AMAZEMET rePOWDER ultrasonic atomizer at about 1400 m altitude (room pressure about
850-865 mbar). A charge is induction-melted in a BN-coated graphite crucible; argon over-pressure
("graining" pressure, 0.19 bar on the HMI) pushes the melt through a 0.5 mm hBN nozzle once a stopper
rod is lifted, and the stream falls onto an inclined W-coated carbon-fibre plate driven at 40 kHz
(1:1.5 booster, 90 % amplitude). A "turbo" button applies 1.5 bar while held. Melt the plate does not
atomize is meant to run off into a ceramic catch bowl on the chamber floor. Powder falls through a
water-cooled stainless cone at the bottom of the chamber into a collection container: a glass cylinder
(probably borosilicate; to be confirmed) about 100 mm across, clamped between a stainless top flange
and a stainless bottom plate by four tie rods, inside a perforated steel guard. Elastomer seals
(material not yet known: silicone, FKM or EPDM) seal each end of the glass and the joint between the
cone and the container's top flange. A removable stainless splash disc sits in the top flange. The
chamber is evacuated to about -850 mbar gauge (about 10 mbar absolute) and backfilled with argon
several times, with washes at 250 and 500 C, and runs at about +150 mbar gauge during the pour. An
oxygen sensor reads the chamber gas through a small continuous bleed to the room; its bleed valve is
open only above +50 mbar and closed under vacuum, the display tops out at 1000 ppm, and the reading is
not meaningful under vacuum. Normal runs read the low 20s ppm before the pour and rise to 100-240 ppm
during it.

Alloy: nickel aluminium bronze UNS C63000 (Cu-10Al-5Ni-3Fe wt%; solidus about 1040 C, liquidus about
1054 C), melted at 1300 C (about 245 C superheat). Good runs (Oct 27 and Nov 10, 816-1080 g, new
plate) made fine powder (d50 roughly 100 um) at 75-91 % yield; failed runs (Oct 28, Nov 5) left most
of the charge as a solid puck in the catch bowl or froze in the nozzle. None of those runs damaged the
collection container.

The Nov 13 run (816 g C63000, the Nov 10 plate flipped over to use its other W face, 5 min hold at
1300 C, graining 0.18 bar then 0.19 bar):
1. Before heating, after the first cold purge, the machine was switched off by accident and turned
   back on. From then on the O2 reading sat at its 1000 ppm limit. On the next backfill it fell to
   about 700 ppm, then read 1000 ppm again once the chamber was back at full vacuum. About four extra
   purge cycles did not help. The vacuum only reached about -830 mbar gauge instead of the usual
   -850 mbar, and the operator suspected a small leak at the joint between the cone and the collection
   container (no hiss was heard). The top of the collection container had been taken off two days
   earlier to sample powder. During the pour the HMI read 351 ppm O2 at +142 mbar.
2. The plate scanned and tested normally (one peak at 40.12 kHz; 79 W at 90 % during the pour), but
   it barely atomized: almost all of the charge came off as small shot ("pellets", roughly 1-3 mm)
   with very little powder, and molten bronze piled up on the back wall of the chamber, blackening
   the steel. Bronze fused around the cone's outlet, which has a burnt dark spot at its top edge.
   Video during the pour shows the glass cylinder glowing orange from hot metal inside it.
3. About three quarters of the way through the pour there was a smell of burning rubber, and smoke
   came out of the seal between the cone and the collection container (that is, outward, from the
   overpressured chamber into the room).
4. Afterwards: under a mass of bronze that had piled up at the container's entrance and slid down the
   inside of the glass, a white, crusty, mud-cracked ring about 19 mm tall lined the wall of the
   container's entrance where that seal sits; white powder from it is mixed into the little powder
   that was made. The seal at the bottom of the glass is charred black. The inside of the glass is
   coated with a yellow-brown film, and the glass cylinder has cracked at its top rim, with a piece
   broken out of the edge that sits in the top flange.
"""

FAILURE_QUERY = CONTEXT + """
Explain this failure and how to prevent it. Give numbers with sources (data sheets, standards, papers
with DOIs) and mark every estimate with its inputs.

1. The seal. For silicone (VMQ), FKM (Viton), EPDM and FFKM seals: continuous and short-term
   temperature limits, how each decomposes in argon with a few hundred ppm O2 versus in air, and what
   each leaves behind (colour, texture, composition). Is a white, cracked, crusty residue the
   signature of silicone turning to silica? Would FKM or EPDM char black instead? What are the
   decomposition products and their hazards (siloxanes and amorphous silica from silicone; HF and
   carbonyl fluoride from FKM above roughly 300-400 C), and how should the residue, the contaminated
   powder and the parts be handled and cleaned?
2. Heat. Estimate the enthalpy of 816 g of C63000 from 1300 C to room temperature (sensible plus
   latent heat). For droplets of 50 um, 200 um, 1 mm and 3 mm falling about 0.5-1 m through argon,
   estimate the time to solidify and the temperature on arrival, and compare fine powder with coarse
   shot and with molten runoff. How hot and how fast would a stainless flange and an elastomer seal
   next to a pile of a few hundred grams of bronze at 900-1050 C get? Why would a run that makes shot
   instead of powder overheat the collection container when good runs and runs that end as a puck in
   the catch bowl do not?
3. The glass. Thermal-shock limits (allowable temperature difference, and the rule of thumb for a
   local hot spot) for soda-lime glass, borosilicate 3.3 and fused quartz, with thickness. Was the
   crack more likely from hot metal touching the glass rim, from the steel flange heating and
   expanding against a clamped rim, or from point loads where the seal burned away? What does a piece
   broken out of the clamped edge indicate? What causes a yellow-brown film on the inside of the glass?
4. Oxygen. Rank the likely causes of the 1000 ppm reading and the 351 ppm during the pour: a real air
   leak at the disturbed collection-container joint (consistent with -830 instead of -850 mbar, or is
   a 20 mbar difference within day-to-day barometric change?), air drawn in or the sensor exposed to
   air when the machine lost power, the sensor's bleed valve being shut under vacuum so room air can
   diffuse back into the sensor, a zirconia cell not yet back at temperature after the power cut, or
   an electrochemical (galvanic) trace sensor saturated by air and slow to recover. How do zirconia
   and electrochemical trace-O2 sensors behave after a power cut and after exposure to air, and how
   long do they take to recover? Give a test that tells a real leak from a sensor fault (for example a
   rate-of-rise test with the pump valved off, soap or helium checks of the clamped joints, and a
   check of the sensor against argon straight from the cylinder).
5. Links between the problems. Could 350-1000 ppm O2 have caused or worsened the failure to atomize
   (Al2O3 skins on a melt with 10 % Al, oxidation of the W coating or carbon fibre, poorer wetting),
   and the seal burning? Could the seal already have been leaking before the run? Separate what the
   evidence supports from what it does not.
6. Prevention, ranked by benefit and cost: a stop rule (abort the pour when the plate makes shot or
   melt piles up); keeping hot metal out of the container (a larger catch bowl, a deflector, or a
   sacrificial metal sleeve or liner protecting the cone outlet, the seal and the top of the glass);
   seal materials and designs suited to occasional hot metal (FFKM, graphite or metal seals, seals set
   back behind a cooled or shielded lip); swapping the glass for fused quartz or an all-metal
   container for copper alloys; a thermocouple on the container's top flange with an alarm; leak
   checks after any part is disturbed; an O2 go/no-go rule (no heating above a set ppm, and what to do
   after a power cut). Include anything known about how other atomizer makers (gas or ultrasonic)
   protect powder collection containers and their seals from hot metal.
"""

PRECEDENT_QUERY = """\
Find reports, manuals, application notes or papers on metal powder atomizers (ultrasonic such as the
AMAZEMET rePOWDER, gas, or centrifugal) and other inert-gas melting equipment in which hot metal,
coarse shot or molten runoff reached the powder collection container or its seals, so that elastomer
seals or gaskets overheated, smoked or burned, glass collection vessels or view ports cracked from
thermal shock, or the atmosphere's oxygen rose because a collector seal leaked. For each give the
equipment, what happened, the cause found and the fix (for example seal material, heat shields,
cooled flanges, metal collection pots, catch trays, interlocks or stop rules). Also report published
guidance on choosing seals and glass for powder collectors under melts above 1000 C, on leak testing
(rate of rise, helium) of atomizer chambers, and on how trace-oxygen sensors on such chambers should
be checked after a power failure.
"""

TASKS = {
    "literature_high_cup_failure": (JobNames.LITERATURE_HIGH, FAILURE_QUERY),
    "precedent_collector_failures": (JobNames.PRECEDENT, PRECEDENT_QUERY),
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
