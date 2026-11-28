"""Edison second opinion on the lab-built collection cup for the rePowder atomizer (#269).

On Nov 13 2026 a 630 bronze run threw most of its charge as 1-3 mm shot that reached the collection cup
still hot. The cup's EPDM valve seat burned, the seals under the glass were damaged and the glass
cracked at its top rim. A replacement from AMAZEMET has no date, so the lab is designing its own.
These tasks ask for a design review and for precedents.

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
Context. A university lab runs an AMAZEMET rePOWDER ultrasonic atomizer at about 1400 m altitude (room
pressure about 850-865 mbar). A 0.3-1.1 kg charge (aluminium alloys, and copper alloys such as
nickel-aluminium bronze UNS C63000 poured at about 1300 C) is induction-melted in a graphite crucible,
pushed through a 0.5 mm nozzle by argon over-pressure, and falls onto a plate vibrating at 40 kHz that
breaks it into powder (d50 roughly 100 um on good runs). Powder falls through a water-cooled stainless
cone under the chamber into a collection container that hangs from the cone's outlet flange on a
hinged clamp (ISO-KF style with a centring ring and O-ring, or possibly sanitary tri-clamp; size about
DN40-50, being confirmed). The chamber is evacuated to about 10 mbar absolute and backfilled with argon
several times, then runs at about +150 mbar gauge; a mechanical relief valve opens at +0.8 bar.
The stock container, top to bottom: the flange on a short neck, a conical reducer, a valve body with a
lever-operated flap valve whose seat is an EPDM ring, a borosilicate(?) glass tube about 100 mm across
in a perforated steel guard, sealed by elastomer rings in grooves of a top and a bottom stainless plate,
and four tie rods. A curved stainless splash plate sits in the bore at the top. The manufacturer also
supplies protective "shields" that fit in the cone; on the failed run they were not fitted and the
splash plate was in backwards.

The failure (Nov 13 2026): the plate barely atomized, so most of an 816 g C63000 charge left it as 1-3 mm
shot, still partly liquid when it reached the container about 0.4 s later. Bronze piled up at the
container's entrance; the glass glowed orange; the EPDM valve seat burned (white crust, smoke out of
the joint); the seals under the glass were damaged; the glass cracked at its top rim. Good runs never
damaged the container. The manufacturer says a "much simpler metal cup, without the glass" exists
(a stainless tube with a separate sanitary butterfly valve), and that in their own lab they mostly use
"the simple stainless steel" tube because it is easier to make and clean, but its delivery date is
unknown. The lab wants to build its own container within days to a few weeks, glass or metal.

The lab's design so far (to be reviewed, not assumed correct):
A. All-metal, catalogue parts only: a 316L ISO-KF full nipple (bore about 48 mm, 200-250 mm long) hung
   from the cone with the existing clamp; a KF blank flange at the bottom with a stainless centring ring
   and FKM O-ring; a drop-in 304/316 sacrificial liner sleeve in the top bore so that hot metal cannot
   touch the top O-ring; a loose copper or steel "catch puck" at the bottom to soak up heat and keep the
   pile off the bottom joint; Type K thermocouples clamped on the outside at the top flange and near the
   bottom, read by a panel meter with an alarm; no valve (a KF blank and clamp go on the top after
   removal), or a full-port valve whose seats are hidden behind the ball when open.
B. All-metal, turned and TIG-welded: one 316L vessel (KF weld stub, a 63-76 mm tube, a 10 mm welded
   bottom, no bottom seal), with an internal shoulder that locates the sacrificial liner.
C. Glass rebuild: the stock plates, valve and tie rods with a fused-quartz tube in place of the
   borosilicate, FKM or silicone seals, and a stainless liner sleeve that covers the glass rim and the
   top seal.
"""

DESIGN_QUERY = CONTEXT + """
Review these designs and recommend one. Give numbers with sources (data sheets, standards, papers with
DOIs, vendor technical notes) and mark every estimate with its inputs.

1. Materials. 304 vs 316L for the body, liner and puck; copper or graphite as a liner or catch puck
   (wetting and sticking of molten copper alloys and aluminium on each; galling; contamination of the
   powder). Fused quartz vs borosilicate 3.3 for a 100 mm tube: thermal-shock limits, cost, and what
   happens if 1000 C metal touches it. Is a metal body clearly better for this duty?
2. Seals. Temperature limits (continuous and short excursions) of FKM, VMQ silicone, EPDM, FFKM and
   PTFE in KF centring rings and tri-clamp gaskets; which survive vacuum service to 10 mbar with low
   permeation; is a metal (aluminium or copper) KF seal or a spring-energised seal practical here? How
   far must an O-ring be from a hot pile, and how much does a metal centring ring between them help?
3. Heat. If 100-800 g of bronze shot at about 1000 C lands in the container, how hot do a 1 kg vs 3 kg
   stainless container, a copper puck, and the seals get, and how fast? What thermal mass, spacing or
   cooling (fins, water jacket, an argon purge) keeps the seals below their limits? Is a sacrificial
   liner worth it, and what gap and length should it have?
4. Valve. Does the container need an isolation valve at all for Al and Cu alloy powders that are
   emptied in air within an hour? If so, which type keeps its seals out of the falling metal (full-port
   ball valve with PTFE seats, butterfly, knife gate, flap)? What do gas-atomizer and powder-handling
   systems use for powder collection canisters (for example Ames Lab HPGA, commercial VIGA/EIGA units,
   AMAZEMET rePowder and similar), and how do they protect them from unatomized metal?
5. Sealing and leaks. ISO-KF vs sanitary tri-clamp for a joint that cycles between 10 mbar absolute
   and +150 mbar gauge: leak rates, clamp loads, how centring rings and gaskets behave after heating,
   and what a lab should check (rate-of-rise, soap at overpressure, helium) before trusting the O2
   reading.
6. Rank the risks of each design (A, B, C) for a lab that wants something working within days, and
   say what you would change.
"""

PRECEDENT_QUERY = CONTEXT + """
Find precedents: published designs, manuals, theses, patents or incident reports for powder
collection canisters, cans or cyclones under metal atomizers (gas, ultrasonic, centrifugal, plasma),
especially how they are protected from unatomized molten metal, shot or splats, what materials and
seals they use, whether they have isolation valves, how they are cooled or instrumented, and any
failures where hot metal reached the collection container, melted seals or cracked glass. Include
lab-scale and university-built atomizers. Give citations with DOIs or URLs.
"""

TASKS = {
    "literature_high_design_review": (JobNames.LITERATURE_HIGH, DESIGN_QUERY),
    "precedent_collection_canisters": (JobNames.PRECEDENT, PRECEDENT_QUERY),
}


def client():
    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def submit():
    c = client()
    ids = {}
    for key, (job, query) in TASKS.items():
        ids[key] = str(c.create_task(TaskRequest(name=job, query=query)))
        print("submitted", key, flush=True)
    IDS_FILE.write_text(json.dumps({"submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                    "tasks": ids}, indent=2) + "\n")


def wait(max_minutes=float(os.environ.get("EDISON_WAIT_MINUTES", "45")), poll=120):
    c = client()
    ids = json.loads(IDS_FILE.read_text())["tasks"]
    t0 = time.time()
    while True:
        statuses = {k: str(c.get_task(task_id=v, lite=True).status) for k, v in ids.items()}
        print(time.strftime("%H:%M:%S"), statuses, flush=True)
        if all(s in TERMINAL for s in statuses.values()) or time.time() - t0 > max_minutes * 60:
            return statuses
        time.sleep(poll)


def fetch():
    c = client()
    ids = json.loads(IDS_FILE.read_text())["tasks"]
    for key, task_id in ids.items():
        task = c.get_task(task_id=task_id)
        data = task.model_dump(mode="json") if hasattr(task, "model_dump") else dict(task)
        answer = scrub(data.get("formatted_answer") or data.get("answer") or "")
        meta = {k: data.get(k) for k in ("task_id", "status", "job_name", "created_at", "query",
                                          "has_successful_answer", "total_cost", "total_queries")}
        meta = scrub(meta)
        (HERE / f"{key}.json").write_text(json.dumps(meta, indent=2) + "\n")
        if answer:
            (HERE / f"{key}.md").write_text(
                f"# Edison {meta.get('job_name')}: {key}\n\n"
                f"Task `{task_id}`, status {meta.get('status')}.\n\n"
                f"<details><summary>Query</summary>\n\n```text\n{meta['query']}\n```\n\n</details>\n\n"
                f"{answer}\n")
        verbose = scrub(c.get_task(task_id=task_id, verbose=True).model_dump(mode="json"))
        (HERE / f"{key}_trajectory.json").write_text(json.dumps(verbose, indent=1, default=str) + "\n")
        print(key, meta["status"], len(answer), "chars", flush=True)


if __name__ == "__main__":
    {"submit": submit, "wait": wait, "fetch": fetch}[sys.argv[1]]()
