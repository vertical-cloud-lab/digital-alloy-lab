"""Edison Scientific queries for issue #254: why cryogenic testing matters for aerospace alloys,
with a focus on aluminum.

Subcommands (run with a Python that has edison-client >= 0.18 installed):

    python scripts/edison_cryo_testing.py submit   # submit every query not yet submitted
    python scripts/edison_cryo_testing.py wait     # block until all tasks finish (foreground only)
    python scripts/edison_cryo_testing.py fetch    # save answers and full trajectories

Task IDs are kept in edison-trajectories/cryo-testing-aerospace-alloys/_task_ids.json, so a
later session can fetch results that were not ready when this one ended.

Reads the API key from EDISON_PLATFORM_API_KEY and never prints it.
"""

from __future__ import annotations

import json
import os
import pathlib
import re
import sys
import time

from edison_client import EdisonClient, JobNames

OUT = pathlib.Path(__file__).resolve().parent.parent / "edison-trajectories" / "cryo-testing-aerospace-alloys"
IDS = OUT / "_task_ids.json"
DONE = {"success", "fail", "failed", "cancelled", "error"}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")

CONTEXT = (
    "Context: the BYU Vertical Cloud Lab designs aluminum alloys for laser powder bed fusion "
    "(LPBF) with AI and CALPHAD, including critical-mineral-lean compositions (less Sc, Li, Ce), "
    "makes its own powder by ultrasonic atomization, and tests in a ladder of single tracks, "
    "density cubes and tensile bars. It is deciding whether and how to add cryogenic mechanical "
    "testing. Prefer primary sources, NASA/NIST technical reports and standards; give DOIs or "
    "report numbers; give numbers with temperatures and units; and say which claims are strongly "
    "vs. weakly supported."
)

QUERIES: dict[str, dict[str, str]] = {
    "01-why-cryogenic-testing-matters": {
        "job": "LITERATURE_HIGH",
        "query": (
            "Why is cryogenic mechanical testing important for aerospace structural alloys, and "
            "what does it reveal that room-temperature testing does not? Cover, with citations "
            "and DOIs: "
            "(1) Applications that need cryogenic qualification: liquid hydrogen (20 K), liquid "
            "oxygen (90 K) and liquid methane (111 K) propellant tanks and feedlines on launch "
            "vehicles (Space Shuttle external tank, SLS, Falcon 9, Ariane, H-II/H3), "
            "liquid-hydrogen aircraft, cryogenic wind tunnels, cryocooled space instruments, and "
            "superconducting-magnet structures. "
            "(2) How yield and tensile strength, elongation, fracture toughness (K_Ic, J_Ic), "
            "fatigue and fatigue-crack growth, and impact energy change between 295 K, 77 K, "
            "20 K and 4 K for FCC (aluminum, austenitic stainless, nickel), BCC (ferritic "
            "steels) and HCP (titanium) alloys; ductile-to-brittle transitions; serrated or "
            "discontinuous plastic flow and adiabatic heating at 4 K; thermal contraction and "
            "thermal cycling; welds and heat-affected zones. "
            "(3) Failures, anomalies or design changes traced to missing or inadequate "
            "cryogenic property data, and the gaps in design-allowable databases (MMPDS) at "
            "cryogenic temperatures. "
            "(4) Test standards and practice (ASTM E1450, ISO 6892-3, ASTM E23 low-temperature "
            "Charpy, ASTM E1820/E399 and ASTM E647 at cryogenic temperature, JIS Z 2277), "
            "whether 77 K liquid-nitrogen tests are a valid proxy for 20 K or 4 K service, and "
            "how cost and helium scarcity shape what gets tested. "
            "(5) Hydrogen compatibility at cryogenic temperature for liquid-hydrogen service. "
            + CONTEXT
        ),
    },
    "02-aluminum-cryogenic-behavior": {
        "job": "LITERATURE_HIGH",
        "query": (
            "What is known, with quantitative data, citations and DOIs, about the cryogenic "
            "mechanical behavior of aluminum alloys used or proposed for aerospace cryogenic "
            "structures? Cover: "
            "(1) Wrought alloys: 2219 and 2014 (Al-Cu); 2195, 2050, 2060, 2098, 2198 and other "
            "Al-Li alloys; 5083, 5456 and 5182 (Al-Mg); 6061; 7050 and 7075. Give yield "
            "strength, tensile strength, elongation and fracture toughness at 295 K, 77 K, 20 K "
            "and 4 K. Explain why most aluminum alloys become both stronger and more ductile at "
            "cryogenic temperature (work-hardening and dislocation storage, suppression of "
            "Portevin-Le Chatelier serrations, T1 and delta-prime precipitates and grain-boundary "
            "effects in Al-Li), and the exceptions (alloys or tempers whose toughness drops, "
            "delamination in Al-Li plate). "
            "(2) Welds: friction stir and fusion welds of 2219 and 2195 at cryogenic temperature "
            "(Shuttle super-lightweight tank, SLS core stage, Falcon 9). "
            "(3) Additively manufactured aluminum: LPBF AlSi10Mg, AlSi7Mg/A357, Scalmalloy "
            "(Al-Mg-Sc-Zr), A20X/A205, Al-Cu-Ce, Al-Fe-Zr, Al-Mn-Sc, and 2219/2319 by wire-arc "
            "additive manufacturing: any data at 77 K or below, and the effect of porosity, the "
            "eutectic silicon network, anisotropy and heat treatment on cryogenic ductility and "
            "toughness. "
            "(4) Keep cryogenic service testing separate from cryogenic processing (cryorolling, "
            "deep cryogenic treatment) and say briefly what the processing literature shows. "
            "(5) Gaps: which aluminum alloy classes, especially AM alloys and alloys lean in Sc, "
            "Li or rare earths, lack cryogenic property data. "
            + CONTEXT
        ),
    },
    "03-precedent-lpbf-al-at-20K-4K": {
        "job": "PRECEDENT",
        "query": (
            "Has anyone measured tensile, fracture-toughness or fatigue properties of laser "
            "powder bed fusion (LPBF / selective laser melting) aluminum alloys, such as "
            "AlSi10Mg, Scalmalloy, A20X or other AM aluminum alloys, at liquid-hydrogen (about "
            "20 K) or liquid-helium (about 4 K) temperature, rather than only at 77 K?"
        ),
    },
    "04-precedent-high-throughput-cryo-testing": {
        "job": "PRECEDENT",
        "query": (
            "Has anyone built or used a high-throughput, automated or multi-specimen cryogenic "
            "mechanical testing system for metals, for example a cryostat that tests many "
            "tensile specimens per cooldown, miniaturized or small-punch specimens tested at "
            "77 K or 4 K, or a cryocooler-based conduction-cooled tensile rig, to screen alloys "
            "faster than one specimen per cooldown?"
        ),
    },
    "05-equipment-and-facilities": {
        "job": "LITERATURE",
        "query": (
            "What equipment and facilities are used for cryogenic mechanical testing of metals "
            "(tension, fracture toughness, fatigue) at 77 K, 20 K and 4 K? Cover liquid-nitrogen "
            "and liquid-helium immersion cryostats, cold-gas flow-through environmental chambers, "
            "cryocooler (Gifford-McMahon or pulse-tube) conduction-cooled rigs that need no "
            "liquid helium, and testing in liquid hydrogen; strain measurement and extensometry "
            "at cryogenic temperature; the commercial makers named in methods sections (load "
            "frames, cryostats, cryocoolers); the main documented test facilities (national labs, "
            "NASA centers, magnet labs, CERN, KIT, NIMS) with their temperature ranges; and cost, "
            "helium use and throughput where reported. Give citations and DOIs."
        ),
    },
    "06-industry-documented-usage": {
        "job": "LITERATURE",
        "query": (
            "How have launch-vehicle, spacecraft and aircraft programs documented the use of "
            "cryogenic mechanical testing to select and qualify aluminum alloys for cryogenic "
            "propellant tanks? Examples: the Space Shuttle external tank and super-lightweight "
            "tank (2219 to 2195 Al-Li), the SLS core stage (2219), Delta IV, Atlas V and Vulcan, "
            "Falcon 9 (Al-Li with friction stir welding), Ariane 5 and 6, H-IIA and H3, Chinese "
            "launch vehicles (2219, 5A06, Al-Li), and liquid-hydrogen aircraft tank studies "
            "(NASA, Airbus, DLR). For each, give the test temperatures used (77 K vs 20 K), the "
            "properties measured (for example the cryogenic-to-room-temperature fracture "
            "toughness ratio, weld strength, leak-before-break), and NASA technical reports or "
            "conference papers with citations, DOIs or NTRS numbers."
        ),
    },
}


def client() -> EdisonClient:
    key = os.environ.get("EDISON_PLATFORM_API_KEY")
    if not key:
        sys.exit("EDISON_PLATFORM_API_KEY is not set")
    return EdisonClient(api_key=key)


def load_ids() -> dict:
    return json.loads(IDS.read_text()) if IDS.exists() else {}


def submit() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ids = load_ids()
    c = client()
    for key, q in QUERIES.items():
        if key in ids:
            print(f"{key}: already submitted ({ids[key]['task_id']})")
            continue
        task_id = c.create_task({"name": getattr(JobNames, q["job"]), "query": q["query"]})
        ids[key] = {
            "task_id": str(task_id),
            "job": q["job"],
            "job_name": getattr(JobNames, q["job"]).value,
            "submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        IDS.write_text(json.dumps(ids, indent=2) + "\n")
        print(f"{key}: submitted {q['job']} -> {task_id}", flush=True)


def statuses(c: EdisonClient, ids: dict) -> dict[str, str]:
    out = {}
    for key, rec in ids.items():
        try:
            out[key] = str(c.get_task(task_id=rec["task_id"], lite=True).status)
        except Exception as e:  # noqa: BLE001 - keep polling through transient errors
            out[key] = f"poll-error:{type(e).__name__}"
    return out


def wait(max_minutes: float = 55.0, interval: int = 120) -> None:
    ids = load_ids()
    c = client()
    t0 = time.time()
    while True:
        st = statuses(c, ids)
        mins = (time.time() - t0) / 60
        print(f"[{time.strftime('%H:%M:%S', time.gmtime())} UTC, {mins:.1f} min] "
              + ", ".join(f"{k[:2]}={v}" for k, v in st.items()), flush=True)
        if all(v in DONE for v in st.values()) or mins > max_minutes:
            break
        time.sleep(interval)


def fetch() -> None:
    ids = load_ids()
    c = client()
    for key, rec in ids.items():
        task_id = rec["task_id"]
        verbose = c.get_task(task_id=task_id, verbose=True)
        status = str(verbose.status)
        rec["status"] = status
        if status not in DONE:
            print(f"{key}: {status}, not fetched")
            continue
        raw = verbose.model_dump(mode="json")
        # The retrieved paper text carries authors' e-mail addresses; this repo is public.
        traj = EMAIL.sub("[email redacted]", json.dumps(raw, indent=1, default=str))
        (OUT / f"{key}.trajectory.json").write_text(traj + "\n")
        resp = c.get_task(task_id=task_id)
        answer = getattr(resp, "formatted_answer", None) or getattr(resp, "answer", None) or ""
        has_ok = getattr(resp, "has_successful_answer", None)
        header = (
            "<!--\n"
            f"Edison Scientific {rec['job']} ({rec['job_name']})\n"
            f"Task ID: {task_id}\n"
            f"Submitted: {rec['submitted_utc']}; fetched: "
            f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}; status: {status}; "
            f"has_successful_answer: {has_ok}\n"
            "Retrieved with edison-client 0.18.0 (EDISON_PLATFORM_API_KEY) from GitHub Actions "
            "for issue #254. The full trajectory is in the .trajectory.json file beside this one.\n"
            "-->\n\n"
            f"**Question ({rec['job']}):** {QUERIES[key]['query']}\n\n---\n\n"
        )
        (OUT / f"{key}.md").write_text(header + EMAIL.sub("[email redacted]", str(answer)) + "\n")
        rec["fetched_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        print(f"{key}: {status}, {len(str(answer))} chars saved")
    IDS.write_text(json.dumps(ids, indent=2) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "submit"
    {"submit": submit, "wait": wait, "fetch": fetch}[cmd]()
