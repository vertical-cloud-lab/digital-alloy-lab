"""Edison second opinion on the final option-B design, its build and test procedure and its alarm set points (#269).

    python edison/run_edison_final.py submit   # writes _task_ids_final.json
    python edison/run_edison_final.py fetch    # answer (md), metadata and full trajectory (json), names scrubbed

Uses run_edison.py's scrubbing (e-mails, phone numbers, and the names listed in EDISON_REDACT_NAMES_FILE).
"""

import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run_edison as RE  # noqa: E402
from edison_client import JobNames, TaskRequest  # noqa: E402

IDS = HERE / "_task_ids_final.json"

QUERY = """\
Context. A university lab is replacing the powder collection container of an AMAZEMET rePOWDER ultrasonic
atomizer after a run (0.82 kg of nickel-aluminium bronze, UNS C63000, poured at about 1300 C) produced 1-3 mm
shot instead of powder; the shot piled up on a splash plate and a butterfly valve just under the container's
top seal, burned the EPDM valve seat and cracked the borosilicate tube. The chamber is evacuated to about
10 mbar absolute, backfilled with argon several times and runs at +150 mbar gauge; its relief valve opens at
+0.8 bar gauge. The container hangs from the water-cooled cone's ISO-KF-50 outlet on a hinged clamp.

Final design (please critique, with sources): a TIG-welded vessel, 250 mm long, made of a KF-50 x 2 in
butt-weld stub (304L), a 3 x 2 in concentric butt-weld reducer (316L, 101.6 mm long, 0.065 in wall), a 3 in OD x
0.065 in 316 tube and an 8 mm 316L floor disc (three square-butt / chamfered welds, ER316L, argon back-purge).
Inside: a loose 304 catch puck (70 x 25 mm) on the floor and a loose 304 liner tube (2-3/4 in x 0.065 in) standing
on it, both sacrificial. No valve, no splash plate and no ledge inside the top; the bore only widens below the
seal. A stainless centring ring with an FKM O-ring and an over-pressure ring (rated 50 psig) at the cone joint.
The manufacturer's splash shields (thin discs) lie in the cone's mouth above the joint. Two type K washer
thermocouples under worm clamps: on the stub just below the flange, and 6 mm above the floor, read by a
2-channel meter with relay alarms at 120 C (top) and 150 C (bottom).

Our CalculiX axisymmetric transient model (packed bed of shot at 1050 C, 70 % liquid, k_eff 5 W/m K, pile on the
puck, radiation from the pile top by Monte-Carlo view factors, outside convection 8 W/m2K plus radiation) gives a
peak O-ring temperature of 26 / 32 / 45 C for 100 / 400 / 816 g of shot and a floor peak of about 120 / 255 / 340 C;
a catalogue alternative (KF-50 nipple 160 mm with a blank on the bottom and the puck inside the bottom
centring ring) reaches 128 / 207 / 245 C at its bottom O-ring for 100 / 250 / 400 g. Static FEA gives 7 MPa at
+1.2 bar, 6 MPa under full vacuum and 86 MPa thermal stress at the floor's inside corner (yield about 106 MPa at
320 C).

Questions:
1. What would you change in this design or its materials for this duty (hot copper-alloy shot, Al and Cu alloy
   powders, vacuum/argon cycling)? Any concern with 304L welded to 316L, with ER316L on 0.065 in wall, or with
   sensitisation, distortion of the KF flange 19 mm from a weld, or galling of the loose liner?
2. Is a peak thermal stress near yield at a sharp inside corner of a welded flat floor acceptable for a few
   hundred thermal cycles (shakedown, ASME VIII-2 / III ratcheting rules)? Should the corner get an inside
   fillet weld or a dished floor?
3. Are the alarm set points sensible? What do atomizer or vacuum-furnace operators use to detect unatomized
   melt reaching a collector (thermocouples, pyrometers, load cells, cameras)?
4. Leak and pressure testing: acceptance criteria for a rate-of-rise test on a ~10-20 L chamber at 10 mbar,
   bench soap testing, and whether a pneumatic proof test at 1.5 x the relief setting is appropriate for a
   small stainless vessel with a KF joint (or whether a hydrostatic test is better practice).
5. Any published incidents or lessons on KF joints under positive pressure, over-pressure rings, or elastomer
   seals near hot powder.
Give numbers with sources (standards, vendor technical notes, papers with DOIs) and mark estimates.
"""


def submit():
    if IDS.exists():
        sys.exit(f"{IDS.name} already exists; refusing to resubmit")
    c = RE.client()
    tid = str(c.create_task(TaskRequest(name=JobNames.LITERATURE_HIGH, query=QUERY)))
    IDS.write_text(json.dumps({"submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                               "tasks": {"literature_high_final_design_check": tid}}, indent=2) + "\n")
    print("submitted", flush=True)


def fetch():
    RE.IDS_FILE = IDS
    RE.fetch()


def wait(max_minutes=40, poll=120):
    RE.IDS_FILE = IDS
    return RE.wait(max_minutes=max_minutes, poll=poll)


if __name__ == "__main__":
    {"submit": submit, "fetch": fetch, "wait": wait}[sys.argv[1]]()
