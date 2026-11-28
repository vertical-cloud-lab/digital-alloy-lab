"""Edison Scientific queries for issue #254, second round: elevated-temperature testing of aerospace
alloys (aluminum in focus), mechanical tests beyond the tensile test, and tensile tests at other
settings such as strain rate. The first round (cryogenic testing) is scripts/edison_cryo_testing.py.

Subcommands (run with a Python that has edison-client >= 0.18 installed; it needs Python < 3.14):

    python scripts/edison_elevated_temp_testing.py submit   # submit every query not yet submitted
    python scripts/edison_elevated_temp_testing.py wait     # block until all tasks finish (foreground only)
    python scripts/edison_elevated_temp_testing.py fetch    # save answers and full trajectories

Task IDs are kept in edison-trajectories/elevated-temp-and-mechanical-testing/_task_ids.json, so a
later session can fetch results that were not ready when this one ended.

Reads the API key from EDISON_PLATFORM_API_KEY and never prints it.
"""

from __future__ import annotations

import importlib.metadata
import json
import os
import pathlib
import re
import sys
import time

from edison_client import EdisonClient, JobNames

OUT = (pathlib.Path(__file__).resolve().parent.parent / "edison-trajectories"
       / "elevated-temp-and-mechanical-testing")
IDS = OUT / "_task_ids.json"
DONE = {"success", "fail", "failed", "cancelled", "error"}
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
# Publisher PDFs stamp "downloaded from IP address a.b.c.d" (the crawler's address) into the text.
DOWNLOAD_IP = re.compile(r"(downloaded from IP address )(?:\d{1,3}\.){3}\d{1,3}")


def redact(text: str) -> str:
    return DOWNLOAD_IP.sub(r"\1[redacted]", EMAIL.sub("[email redacted]", text))

CONTEXT = (
    "Context: the BYU Vertical Cloud Lab designs aluminum alloys for laser powder bed fusion "
    "(LPBF) with AI and CALPHAD, including critical-mineral-lean compositions (less Sc, Li, Ce), "
    "makes its own powder by ultrasonic atomization, and tests in a ladder of single tracks, "
    "density cubes and room-temperature tensile bars. It is deciding which elevated-temperature, "
    "non-tensile and rate-dependent mechanical tests to add. Prefer primary sources, NASA, NIST "
    "and AFRL technical reports, MMPDS and standards; give DOIs or report numbers; give numbers "
    "with temperatures, exposure times, strain rates and units; and say which claims are strongly "
    "vs. weakly supported."
)

QUERIES: dict[str, dict[str, str]] = {
    "01-why-elevated-temperature-testing-matters": {
        "job": "LITERATURE_HIGH",
        "query": (
            "Why is elevated-temperature mechanical testing important for aerospace structural "
            "alloys, and what does it reveal that room-temperature testing does not? Cover, with "
            "citations and DOIs: "
            "(1) Where aerospace structures get hot: aerodynamic heating of supersonic and "
            "hypersonic skins (Concorde at Mach 2 cruise, the NASA High-Speed Research / HSCT "
            "program, missiles and hypersonic vehicles), engine nacelles, pylons, thrust reversers "
            "and bleed-air ducts, auxiliary power units, compressor wheels and impellers, heat "
            "exchangers, structures near rocket engines and thermal-protection-system "
            "substructure, and fire exposure. "
            "(2) What changes with temperature and with time at temperature: loss of yield and "
            "tensile strength, elongation and modulus at temperature; property loss after thermal "
            "exposure (overaging, precipitate coarsening) measured back at room temperature; "
            "creep, stress rupture and stress relaxation; low-cycle and thermomechanical fatigue "
            "and creep-fatigue interaction; fatigue-crack growth and fracture toughness at "
            "temperature; oxidation; dynamic strain aging; and how long-time behavior is "
            "extrapolated (Larson-Miller, Wilshire, Monkman-Grant). "
            "(3) How design allowables handle temperature: MMPDS 'effect of temperature' and "
            "'effect of exposure time' curves (for example 0.5 h to 10,000 h), and how this "
            "differs for aluminum, titanium, steels and nickel superalloys. "
            "(4) Test standards and practice: ASTM E21 (elevated-temperature tension), ISO "
            "6892-2, ASTM E139 and ISO 204 (creep and stress rupture), ASTM E328 (stress "
            "relaxation), ASTM E606 (strain-controlled fatigue), ASTM E2368 (thermomechanical "
            "fatigue), ASTM E2714 (creep-fatigue), ASTM E1457 (creep-crack growth); heating "
            "methods, temperature-uniformity and soak-time requirements, and high-temperature "
            "extensometry. "
            "(5) Failures, anomalies or design changes traced to missing or inadequate "
            "elevated-temperature property data. "
            + CONTEXT
        ),
    },
    "02-aluminum-elevated-temperature": {
        "job": "LITERATURE_HIGH",
        "query": (
            "What is known, with quantitative data, citations and DOIs, about the "
            "elevated-temperature mechanical behavior of aluminum alloys for aerospace? Cover: "
            "(1) Wrought alloys: 2618/2618A (RR58, Concorde), 2219, 2024, 2014, 2519, 2039/2139 "
            "(Al-Cu-Mg-Ag), 6061, 6013, 7075 and 7050, and dispersion-strengthened 8009 "
            "(Al-Fe-V-Si). Give yield strength, tensile strength and elongation at 100, 150, 200, "
            "250, 300 and 350 C, after short and long exposures (for example 0.5 h, 100 h, "
            "1000 h, 10,000 h), plus creep and stress-rupture data. Explain why "
            "precipitation-hardened alloys lose strength above about 150-200 C (coarsening and "
            "dissolution of theta-prime, S and eta-prime), and how Sc, Zr, Mn, Fe, Ni, Ce and Ag "
            "additions (L1_2 Al3(Sc,Zr), Al3Zr, Al20Cu2Mn3, Al11Ce3, Al3Ni, Omega phase) improve "
            "stability. "
            "(2) Cast alloys: A356/A357, 354, 319, 242, 4032, and the ORNL ACMZ (Al-Cu-Mn-Zr) and "
            "Al-Ce alloys. "
            "(3) Additively manufactured aluminum: LPBF AlSi10Mg, Scalmalloy, Addalloy (Al-Mg-Zr), "
            "A20X/A205, Constellium Aheadd alloys, Al-Ce-Mg, Al-Ce-Ni-Mn, Al-Fe-Zr, Al-Ni-Zr, "
            "Al-Mn-Sc, Al-Cu-Mn-Zr, and NASA or industry alloys designed for 250-400 C: "
            "elevated-temperature tensile, creep and thermal-stability data, and how the fine "
            "LPBF microstructure, the eutectic Si network and solute supersaturation help or hurt "
            "at temperature. "
            "(4) Which properties a designer of a 150-300 C aluminum part actually needs, and how "
            "much they differ from room-temperature tensile values. "
            "(5) Gaps: which AM aluminum alloys, especially those lean in Sc, Li or rare earths, "
            "lack creep, elevated-temperature fatigue or long-exposure data. "
            + CONTEXT
        ),
    },
    "03-mechanical-tests-beyond-tensile": {
        "job": "LITERATURE_HIGH",
        "query": (
            "Beyond the uniaxial tensile test, which mechanical tests are used to select and "
            "qualify aerospace aluminum alloys and additively manufactured metal parts, what does "
            "each reveal that a tensile test cannot, and how much material and time does each "
            "take? Cover, with citations and DOIs: fracture toughness (ASTM E399, E1820, B645, "
            "B646, E561 R-curves) and the Kahn tear test (ASTM B871); fatigue (high-cycle per "
            "ASTM E466, low-cycle per E606, ultrasonic fatigue at 20 kHz) and fatigue-crack "
            "growth (E647); Charpy impact (E23) and why it is little used for aluminum; notched "
            "tension (E602) and notch sensitivity; compression (E9); shear (B769, B565 pin shear, "
            "V-notch); bearing (E238); hardness (Rockwell, Vickers, Brinell) and nanoindentation, "
            "and how well hardness predicts yield strength for aluminum; stress-corrosion "
            "cracking (G47, G139) and exfoliation (G34); residual-stress measurement; and "
            "small-specimen methods (small punch per ASTM E3205, shear punch, miniature tensile, "
            "micropillar compression, profilometry-based indentation plastometry). "
            "For additively manufactured parts, cover NASA-STD-6030 and MSFC-STD-3716, AMS 7032 "
            "and AMS 7003, MMPDS and CMH-17-style A- and B-basis allowables, the role of surface "
            "roughness, porosity, build orientation and HIP in fatigue, and why fatigue rather "
            "than tensile strength usually limits LPBF aluminum. "
            "Finally, which of these tests have been run in a high-throughput or automated way to "
            "screen alloys (automated hardness or nanoindentation maps, small punch, miniaturized "
            "tensile arrays, robotic test cells). "
            + CONTEXT
        ),
    },
    "04-strain-rate-and-test-settings": {
        "job": "LITERATURE_HIGH",
        "query": (
            "How do test settings, especially strain rate, change the measured tensile properties "
            "of aluminum alloys, and how should a lab choose and report them? Cover, with "
            "citations and DOIs: "
            "(1) Quasi-static rate: ASTM E8/E8M and B557 rate limits, ISO 6892-1 Method A "
            "(strain-rate control, ranges such as 0.00007, 0.00025, 0.0067 and 0.025 1/s) versus "
            "Method B, crosshead versus extensometer control, and how much yield strength, UTS "
            "and elongation shift across these ranges for 2xxx, 5xxx, 6xxx and 7xxx alloys and "
            "for LPBF AlSi10Mg. "
            "(2) Strain-rate sensitivity: the exponent m, negative strain-rate sensitivity and "
            "Portevin-Le Chatelier serrations in Al-Mg alloys and in LPBF aluminum, strain-rate "
            "jump and stress-relaxation tests that measure m on one specimen, and coupling of "
            "temperature and rate (Zener-Hollomon parameter, dynamic strain aging, superplastic "
            "forming windows). "
            "(3) Intermediate and high rates: servo-hydraulic high-speed tensile testing "
            "(1-1000 1/s, ISO 26203-2), drop-weight towers, split Hopkinson (Kolsky) tension and "
            "compression bars (10^2-10^4 1/s), Taylor impact and plate impact; specimen design, "
            "load ringing and adiabatic heating; and constitutive models (Johnson-Cook, "
            "Zerilli-Armstrong) fitted for 2024, 6061, 7075 and LPBF AlSi10Mg, with parameter "
            "values. "
            "(4) Applications that need rate data: crashworthiness, bird strike, fan-blade-out "
            "containment, ballistic and blast protection, and forming. "
            "(5) Other settings that change the result: specimen size and geometry (sub-size, "
            "round versus flat), gauge length and the elongation definition (A5 versus A50 mm), "
            "surface condition (as-built versus machined LPBF), build orientation, test "
            "temperature and soak, machine stiffness, and the strain-measurement method (clip-on "
            "extensometer, video extensometer, digital image correlation). "
            + CONTEXT
        ),
    },
    "05-precedent-sc-free-lpbf-al-creep": {
        "job": "PRECEDENT",
        "query": (
            "Has anyone measured creep, stress-rupture or long-exposure (1000 h or more) thermal "
            "stability at 250 C or above for a laser powder bed fusion aluminum alloy that "
            "contains no scandium, such as Al-Ce, Al-Fe-Zr, Al-Ni-Zr, Al-Mn-Zr or Al-Cu-Mn-Zr "
            "alloys?"
        ),
    },
    "06-precedent-high-throughput-hot-screening": {
        "job": "PRECEDENT",
        "query": (
            "Has anyone screened aluminum alloys for elevated-temperature strength or creep "
            "resistance with high-throughput methods, for example hot hardness or "
            "high-temperature nanoindentation on compositionally graded or combinatorial "
            "additively manufactured samples, small-punch creep tests, or multi-specimen creep "
            "frames?"
        ),
    },
    "07-precedent-lpbf-al-high-strain-rate": {
        "job": "PRECEDENT",
        "query": (
            "Has anyone measured the high-strain-rate (100 1/s or more, for example with a split "
            "Hopkinson bar) tensile or compressive response of laser powder bed fusion aluminum "
            "alloys other than AlSi10Mg, such as Scalmalloy, A20X/A205, AlSi7Mg, Al-Ce or Al-Fe-Zr "
            "alloys, including the effect of test temperature?"
        ),
    },
    "08-equipment-and-facilities": {
        "job": "LITERATURE",
        "query": (
            "What equipment is used for elevated-temperature, high-strain-rate and non-tensile "
            "mechanical testing of metals, and who makes it? Cover: (1) elevated-temperature "
            "tension and fatigue: split-tube resistance furnaces, induction heating, radiant or "
            "infrared heating, and direct-resistance heating in thermomechanical simulators "
            "(Gleeble); temperature uniformity and thermocouple attachment; high-temperature "
            "extensometers (ceramic-rod contact, laser speckle, video) and high-temperature "
            "digital image correlation; (2) creep and stress rupture: dead-weight lever-arm creep "
            "frames, multi-station or multi-specimen creep machines, and their throughput; "
            "(3) high strain rate: servo-hydraulic high-speed machines, drop towers, split "
            "Hopkinson bars and gas guns, with the makers named in methods sections; (4) fatigue "
            "and fracture: servo-hydraulic and electrodynamic frames, resonant and ultrasonic "
            "(20 kHz) fatigue machines; (5) small-specimen and indentation methods: small-punch "
            "rigs, high-temperature nanoindentation and profilometry-based indentation "
            "plastometry; (6) the main documented facilities (NASA Glenn and Langley, AFRL, NIST, "
            "Southwest Research Institute, national labs) and commercial test labs, with "
            "temperature and rate ranges, and cost and throughput where reported. Give citations "
            "and DOIs."
        ),
    },
    "09-industry-documented-usage": {
        "job": "LITERATURE",
        "query": (
            "How have aerospace and automotive programs documented elevated-temperature and "
            "strain-rate testing to select and qualify aluminum alloys? Examples: Concorde's "
            "2618A (RR58 / AU2GN) skin and its long-time creep and thermal-exposure testing at "
            "about 100-130 C; the NASA High-Speed Research (HSCT) program's evaluation of 2xxx "
            "and 6xxx alloys (for example C415, C416, 2519, 6013) for 60,000 h at about "
            "107-177 C; MMPDS thermal-exposure data; aluminum in engine nacelles, pylons, inlets "
            "and auxiliary power units; 2618 and 2219 in compressor wheels and impellers; "
            "aluminum on missiles and hypersonic vehicles; and additively manufactured "
            "high-temperature aluminum parts (heat exchangers, brackets near engines). Also crash "
            "and impact testing of aluminum (automotive crash boxes, bird strike, fan-blade "
            "containment) that drove high-strain-rate testing and Johnson-Cook calibration. For "
            "each, give the temperatures, exposure times or strain rates used, the properties "
            "measured, and NASA, FAA or AFRL technical reports or conference papers with "
            "citations, DOIs or NTRS numbers."
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
    if len(sys.argv) > 2:
        max_minutes = float(sys.argv[2])
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
    version = importlib.metadata.version("edison-client")
    for key, rec in ids.items():
        if rec.get("fetched_utc") and (OUT / f"{key}.md").exists():
            print(f"{key}: already fetched")
            continue
        task_id = rec["task_id"]
        verbose = c.get_task(task_id=task_id, verbose=True)
        status = str(verbose.status)
        rec["status"] = status
        if status not in DONE:
            print(f"{key}: {status}, not fetched")
            continue
        raw = verbose.model_dump(mode="json")
        # The retrieved paper text carries authors' e-mail addresses and download stamps; this repo is public.
        traj = redact(json.dumps(raw, indent=1, default=str))
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
            f"Retrieved with edison-client {version} (EDISON_PLATFORM_API_KEY) from GitHub "
            "Actions for issue #254. The full trajectory is in the .trajectory.json file beside "
            "this one.\n"
            "-->\n\n"
            f"**Question ({rec['job']}):** {QUERIES[key]['query']}\n\n---\n\n"
        )
        (OUT / f"{key}.md").write_text(header + redact(str(answer)) + "\n")
        rec["fetched_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        print(f"{key}: {status}, {len(str(answer))} chars saved")
    IDS.write_text(json.dumps(ids, indent=2) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "submit"
    {"submit": submit, "wait": wait, "fetch": fetch}[cmd]()
