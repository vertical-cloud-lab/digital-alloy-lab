"""Edison vetting of sinter-based metal vat photopolymerization (PR #229, issue #228).

Sterling asked (29 Oct 2026) for commercializability, target markets and applications, technology
maturity, a comparison with the other metal AM processes, a vetting of the process physics, and who
funds this on the government side. Only the metal kind (metal powder in a light-cured binder,
debound and sintered, as in Greene Group's PureForm, ex-Holo) is in scope, not generic polymer or
ceramic vat photopolymerization.

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
Context. We are a university alloy-development lab (laser powder bed fusion of Al-Zr and Al-Mn-Cr-Zr
alloys, a Cu-Cr-Zr complement, and our own ultrasonic atomization of powder). We are evaluating
sinter-based metal vat photopolymerization: metal powder (usually MIM grade, D50 under ~20 um, about
45-60 vol%) in a light-curable binder is cured layer by layer by DLP or laser stereolithography, and
the green part is cleaned, debound and sintered as in metal injection molding (MIM). Examples:
Holo Inc.'s PureForm (2017-2024; pure copper above 92% IACS, then stainless steel), whose assets
Greene Group Industries, a US MIM contract manufacturer, bought in March 2024 and now sells as a
parts service in 17-4PH and 316 (film-fed bottom-up DLP; design guide: 0.07 mm minimum wall, 3.5 mm
maximum wall, +/-0.025 mm up to 12 mm, 0.8-1.6 um Ra as printed); Incus GmbH's Lithography-based
Metal Manufacturing (LMM; Hammer printers; steels, Ti-6Al-4V, 99.9% Cu, precious metals); and
Admatec's Admaflex DLP. Adjacent routes that make metal through a photopolymer step (Caltech's
hydrogel infusion AM, metal-organic or metal-ion photoresins, two-photon lithography) count too.
Generic polymer or ceramic vat photopolymerization is out of scope except where it informs metal
parts.
"""

COMMERCIAL_QUERY = CONTEXT + """
Question. How commercially viable is sinter-based metal vat photopolymerization?
1. Who has commercialized it (printer vendors, feedstock suppliers, parts services), with founding
   dates, funding, ownership changes and failures (for example Holo's 2024 asset sale to Greene Group,
   and Nano Dimension's 2022 purchase and 2025 exit of Admatec), and installed base where reported.
2. Which markets and applications have actually adopted it, with named examples: orthodontic and
   dental parts, medical and surgical instruments, watch and jewelry parts, micromechanics, RF and
   microwave parts, copper cold plates and heat sinks for electronics, electrical interconnects,
   nozzles and fluidics, tooling inserts, and any defense or aerospace use.
3. Economics: printer price, feedstock cost, build rate, parts per build, cost per part against MIM
   (break-even volume once mold tooling is counted), binder jetting and micro laser powder bed fusion,
   and typical lead times.
4. Barriers: part size and wall-thickness limits, feedstock availability, qualification and standards
   (MPIF Standard 35, ISO/ASTM 52900 classification), the key patents and who holds them, and
   competition.
5. Your judgement of where the process is headed and which niches it can hold.
Cite peer-reviewed papers, standards, market reports and trade press, and flag any figure that comes
only from a vendor.
"""

PHYSICS_QUERY = CONTEXT + """
Question. Critically vet the technical basis of sinter-based metal vat photopolymerization, with
numbers and citations.
1. Curing in metal-loaded slurries: how metal particles absorb and scatter UV and visible light; how
   cure depth and lateral overcure depend on solids loading, particle size, refractive index and
   absorbance (Jacobs working curve, Griffith-Halloran-type models, and models for absorbing
   particles); the layer thicknesses and smallest features reported for steels, copper, titanium,
   tungsten and other metals.
2. Feedstock: achievable solids loading (vol%), viscosity limits for recoated or film-fed systems,
   settling, photoinitiator and absorber choice, dispersants, slurry versus paste.
3. Debinding: thermal versus solvent debinding of photopolymer networks, why crosslinked acrylates
   are harder to remove than MIM binders, cracking and blistering, the maximum wall thickness this
   sets (3.5 mm in Greene Group's design guide; Incus reports around 10 mm), and the residual carbon
   and oxygen left in steel, copper and titanium parts.
4. Sintering: linear shrinkage (often 13-20%) and how it differs between the build direction and the
   build plane, distortion and slumping, final density, grain size, and how these compare with MIM of
   the same powder.
5. Properties: tensile, fatigue and corrosion data for 17-4PH, 316L, Ti-6Al-4V and copper (with
   electrical conductivity in % IACS) made this way, against MIM, wrought and MPIF Standard 35 values.
6. Which metals are hard or impossible by this route, and why: aluminum, titanium, refractory metals,
   and reactive alloying elements such as Cr and Zr in copper.
End with three lists: vendor claims the literature supports, claims it contradicts, and claims with
no independent data.
"""

COMPARISON_QUERY = CONTEXT + """
Question. Compare sinter-based metal vat photopolymerization (PureForm, Incus LMM, Admaflex) with
the other ways of making small, intricate metal parts: laser powder bed fusion (standard and micro
LPBF), electron beam powder bed fusion, binder jetting, bound-metal material extrusion (FFF and
bound metal deposition), metal injection molding (the conventional benchmark), directed energy
deposition, electrochemical additive manufacturing (Fabric8Labs), nanoparticle jetting (XJet),
two-photon lithography and hydrogel infusion routes, and micromachining or micro-EDM. Make a table
giving, for each: smallest feature and wall, as-built surface roughness (Ra), dimensional
tolerance, largest part, thickest wall, typical relative density, build rate (cm3/h), support
needs, residual stress, anisotropy, range of alloys, equipment cost class, cost per part at 10,
1,000 and 100,000 parts, and how far qualification has got (aerospace, medical). Mark vendor claims
as such. Then say for which parts (size, feature scale, alloy, volume) metal vat photopolymerization
is the best choice, where another process beats it, and how its technology readiness compares with
binder jetting and micro LPBF.
"""

FUNDING_QUERY = CONTEXT + """
Question. Who funds research and development of metal vat photopolymerization? In scope: DLP,
stereolithography, LMM or two-photon lithography that ends in metal parts (photocurable metal-powder
slurries that are debound and sintered; metal-ion, metal-salt or metal-organic photoresins and
hydrogel infusion that are calcined and reduced to metal). Out of scope: polymer-only or
ceramic-only vat photopolymerization, and polymer lattices that are only electroplated. For each
paper or project give the agency and program (for example NSF CMMI, NSF SBIR/STTR, DOE Office of
Science BES, DOE AMMTO or AMO, ARPA-E, ONR, AFOSR, ARO, AFRL, DARPA, NASA, NIH, NIST), the grant or
contract number exactly as acknowledged, the principal investigator and institution or company, the
year, and the metal. Include company awards (for example to Holo Inc.) and US national-lab programs
(LLNL, ORNL, Sandia, ARL, AFRL) where they appear, and the non-US public funders (EU Horizon, the
Austrian FFG for Incus or TU Wien, Fraunhofer) for comparison. Quote the acknowledgment sentence where
you can, and say which agencies and program areas fund the most of this work.
"""

PRECEDENT_QUERY = """\
Has anyone made aluminum-alloy or copper-chromium-zirconium (Cu-Cr-Zr, C18150 or C18200) parts by
vat photopolymerization of a metal-powder slurry (DLP, stereolithography or lithography-based metal
manufacturing) followed by debinding and sintering? If so, report density, oxygen and carbon
content, strength, electrical conductivity and the sintering atmosphere. Also report any vat
photopolymerization of aluminum powder at all (including cure-depth studies of Al-filled resins),
and any Cu-Cr, Cu-Zr or oxide-dispersion-strengthened copper made by photopolymerization of a metal
or metal-oxide feedstock.
"""

TASKS = {
    "literature_high_commercial": (JobNames.LITERATURE_HIGH, COMMERCIAL_QUERY),
    "literature_high_physics": (JobNames.LITERATURE_HIGH, PHYSICS_QUERY),
    "literature_high_comparison": (JobNames.LITERATURE_HIGH, COMPARISON_QUERY),
    "literature_high_funding": (JobNames.LITERATURE_HIGH, FUNDING_QUERY),
    "precedent_al_cucrzr": (JobNames.PRECEDENT, PRECEDENT_QUERY),
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
