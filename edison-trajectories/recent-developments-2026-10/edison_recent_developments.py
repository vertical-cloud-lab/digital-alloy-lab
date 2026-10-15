"""Edison follow-up queries: new developments (Apr-Oct 2026) relevant to the
AFOSR YIP white paper and the companion early-career proposals (PR #90).

Usage (from repo root):
    python edison-trajectories/recent-developments-2026-10/edison_recent_developments.py submit
    python edison-trajectories/recent-developments-2026-10/edison_recent_developments.py wait [max_minutes]
    python edison-trajectories/recent-developments-2026-10/edison_recent_developments.py fetch

`wait` blocks in a foreground Python loop (time.sleep) until every task is
terminal; run it as ONE long-timeout foreground call (see CLAUDE.md).
`fetch` writes one markdown answer per task plus the raw verbose JSON.

Requires: pip install edison-client ; EDISON_PLATFORM_API_KEY in the env.
"""

import json
import os
import pathlib
import sys
import time
from datetime import datetime, timezone

from edison_client import EdisonClient, JobNames, TaskRequest

HERE = pathlib.Path(__file__).resolve().parent
TASK_FILE = HERE / "_task_ids.json"
RAW_DIR = HERE / "raw"
TERMINAL = {"success", "fail", "failed", "cancelled", "error", "truncated"}

CONTEXT = """\
CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the PI's
own publications from recommendations) is preparing a one-page pre-solicitation
white paper for the AFOSR Young Investigator Program (Aerospace Materials for
Extreme Environments portfolio, Program Officer Dr. Ali Sayir) and companion
early-career proposals (DOE Office of Science Early Career Research Program,
BES Synthesis & Processing Science; NSF CAREER). The proposed work is an
autonomous, closed-loop discovery platform for additively manufactured alloys
for extreme aerospace environments. The powder-to-property pipeline (CALPHAD ->
powder atomization -> laser powder bed fusion (LPBF) -> microstructure ->
elevated-temperature property) is modeled as a directed acyclic graph of
surrogate models and optimized by cost-aware, multi-fidelity Bayesian
optimization of function networks with partial evaluations (Buathong, Frazier
et al., ICML 2024; Astudillo & Frazier, NeurIPS 2021), so the algorithm decides
when to query cheap nodes (thermodynamic simulations; low-cost proxy
experiments such as single tracks, density cubes, hardness) versus expensive
nodes (full elevated-temperature tensile tests). CALPHAD screening uses
pycalphad / Thermo-Calc (TCHEA, TCNI). Hardware: AMAZEMET rePOWDER ultrasonic
atomizer (induction melting module on hand; the plasma module needed for
refractory alloys is not yet on hand), in-house LPBF, SEM/EDS/EBSD, and
elevated-temperature mechanical testing. Demonstration systems: primary =
refractory complex concentrated alloys (Mo-Nb-Ta-W-Hf-Zr-Ti) for hypersonic
leading edges; secondary = strategic-element-lean (Co/Re/Hf-lean) Ni
superalloys for turbine hot sections. Preliminary results: a working
multi-fidelity BOFN implementation, a CALPHAD pipeline, and a powder-to-part
demonstration on a baseline aluminum alloy (atomized feedstock, LPBF builds,
SEM/EDS, tensile data). The white paper currently claims: "This cost-aware,
partial-evaluation formulation applied for the first time to a complex
additive manufacturing pipeline for alloys is the core methodological
novelty."
"""

WINDOW = """\
TIME WINDOW: Today is 2026-10-06. Find developments published or posted
(journal articles incl. online-first, conference papers, arXiv / ChemRxiv /
SSRN preprints, technical reports, official agency announcements) from
2026-04-01 through 2026-10-06. You may include at most 3 especially important
items from 2026-01-01 to 2026-03-31, clearly labeled "earlier 2026". Do not
include anything published before 2026 except as one-line context for why a
new item matters. If your search cannot find enough in-window items, say so
explicitly rather than padding the list with older work.
"""

OUTPUT = """\
OUTPUT FORMAT: For each item give: full citation with DOI (or arXiv ID / URL),
the exact publication or posting date (online-first date), a 2-3 sentence
summary of what is new, and one or more relevance tags:
[CITE-1PAGER] worth citing in the one-page white paper;
[CITE-FULL] worth citing in a full proposal;
[NOVELTY-RISK] overlaps with or weakens the novelty claim above (explain
exactly how, and how to reword the claim so it stays accurate);
[COMPETITOR] an active group or program likely to compete for the same money;
[AWARENESS] worth knowing but not citing.
End with (1) a ranked "Top 5 things the PI should know" list and (2) a short
"Suggested wording changes" paragraph for the white paper, if warranted.
"""

QUERIES = {
    "01-methods-novelty": {
        "job": "LITERATURE_HIGH",
        "query": CONTEXT + "\n" + WINDOW + """
QUESTION 1 - METHODS AND NOVELTY CHECK: What new work is there on
(a) Bayesian optimization of function networks, partial evaluations,
cascade / multi-stage / network-structured BO, cost-aware multi-fidelity BO,
and chained process-structure-property surrogates applied to materials or
manufacturing;
(b) closed-loop, autonomous, or self-driving-lab discovery of METALLIC alloys,
especially with additive manufacturing (LPBF, DED, binder jet) in the loop -
e.g., Texas A&M BIRDSHOT (Arroyave, Vela, Khatamsaz), NIST AMASE (Kusne),
University of Pittsburgh (Wei Xiong), AFRL autonomous research systems (ARES),
NASA Glenn BO benchmarking, ORNL, LLNL, Carnegie Mellon, Johns Hopkins APL,
and industry;
(c) LLM / agentic / foundation-model approaches to alloy design that are being
combined with BO or with physical experiments;
(d) BO for LPBF process-window optimization and printability of new alloys.
Most importantly: has anyone, in this window, published or preprinted
cost-aware or partial-evaluation BO over a multi-stage additive manufacturing
pipeline (composition -> powder -> print -> microstructure -> property) for
alloys? If so, how should the novelty claim be reworded so that it stays
accurate and defensible?
""" + "\n" + OUTPUT,
    },
    "02-extreme-env-alloys": {
        "job": "LITERATURE_HIGH",
        "query": CONTEXT + "\n" + WINDOW + """
QUESTION 2 - EXTREME-ENVIRONMENT ALLOYS BY ADDITIVE MANUFACTURING: What new
work is there on
(a) refractory complex concentrated / refractory high-entropy alloys (Mo, Nb,
Ta, W, Hf, Zr, Ti, V, Cr, Al additions) and Nb-based alloys (e.g., C103)
processed by LPBF, DED, or electron-beam powder bed fusion - printability and
cracking, ductilization strategies, oxidation resistance and coatings,
elevated-temperature (>= 1200 C) strength and creep, and use for hypersonic
leading edges or thermal protection;
(b) machine-learning- or CALPHAD-guided design of RCCAs, including new
thermodynamic databases or high-throughput CALPHAD assessments of refractory
systems;
(c) strategic-element-lean (low Co / Re / Hf / Ta) Ni-based or Co-Ni
superalloys designed for LPBF crack resistance (e.g., ABD-900AM-type alloys,
oxide-dispersion-strengthened NiCoCr such as NASA GRX-810, AI-designed
superalloys) and their creep and oxidation behavior;
(d) elevated-temperature aluminum alloys for AM (e.g., Al-Ce, Al-Zr-Sc-Er,
Al-Ni-Mn) that could serve as a low-melting-point bridge system for the
methodology demonstration, with aerospace-relevant service to ~300-400 C.
Highlight results that (i) make one demonstration system more or less
attractive for an AFOSR extreme-environments YIP, (ii) quantify current
performance gaps the platform should target (e.g., specific strength at
1200-1600 C, oxidation rate, room-temperature ductility thresholds,
crack-free LPBF windows), or (iii) come from AFRL, AFOSR-funded, NASA, or
DoD-laboratory groups.
""" + "\n" + OUTPUT,
    },
    "03-feedstock-hte": {
        "job": "LITERATURE_HIGH",
        "query": CONTEXT + "\n" + WINDOW + """
QUESTION 3 - FEEDSTOCK, HIGH-THROUGHPUT FABRICATION, AND CHARACTERIZATION:
What new work is there on
(a) ultrasonic atomization of metal powders (e.g., AMAZEMET rePOWDER with
induction vs. plasma melting) - especially of refractory alloys, refractory
high-entropy alloys, Nb / Ta / W / Mo-based alloys, Ni superalloys, and
aluminum alloys - including powder yield, sphericity, oxygen pickup, and LPBF
performance compared with gas-atomized powder;
(b) small-batch or rapid alloy powder production for alloy discovery (e.g.,
plasma spheroidization, in-situ alloying from elemental or master-alloy powder
blends in LPBF / DED, compositionally graded builds), and how well
in-situ-alloyed specimens predict pre-alloyed behavior;
(c) high-throughput or miniaturized elevated-temperature mechanical testing
(miniature tensile, small punch, nanoindentation / micro-compression at
temperature, profilometry-based indentation plastometry, high-throughput creep
screening) and its correlation with bulk properties;
(d) automated / robotic characterization and ML-based analysis for AM alloys
(autonomous SEM/EDS/EBSD, automated metallography, in-situ melt-pool
monitoring as a low-cost fidelity level, X-ray CT defect quantification) that
could serve as cheap proxy nodes in a multi-fidelity loop.
For each, note whether it supports the "cheap proxy experiments vs. expensive
full tensile tests" cost hierarchy in the proposal, and give any quantitative
cost, time, or correlation numbers.
""" + "\n" + OUTPUT,
    },
    "04-funding-policy-landscape": {
        "job": "LITERATURE_HIGH",
        "query": CONTEXT + "\n" + WINDOW + """
QUESTION 4 - FUNDING, PROGRAM, AND POLICY LANDSCAPE: What developments matter
for this PI's funding strategy? Cover:
(a) the AFOSR FY2027 Young Investigator Program solicitation (NOFO number,
white-paper and full-proposal deadlines, eligibility window, award size, any
change to the white-paper portal or process), and any changes to AFOSR
research topics or program officers relevant to Aerospace Materials for
Extreme Environments (Dr. Ali Sayir) or metallic materials;
(b) the DOE Office of Science Early Career Research Program for FY2027
(pre-application dates, changes to eligibility or BES Materials Sciences &
Engineering topic areas), and the DOE "Genesis Mission" AI-for-science
initiative (status of Phase I awards, follow-on calls, AMMTO / ASCR
AI-for-materials opportunities);
(c) NSF CAREER changes for 2026-2027, and NSF reorganization or budget effects
on DMR and CMMI advanced manufacturing;
(d) DoD / Air Force / DARPA / NASA programs or strategy documents on hypersonic
materials, high-temperature alloys, autonomous experimentation, or
AI-accelerated materials discovery (e.g., new BAAs, MURI topics, DURIP,
DEPSCoR, Manufacturing USA institutes such as America Makes project calls);
(e) critical-minerals policy developments for Co, Re, Hf, Ta, Nb, and W that
bear on the "strategic-element-lean" framing (export controls, price shocks,
stockpile actions).
Cite official sources (grants.gov / simpler.grants.gov, agency websites,
Federal Register) and give exact dates. Clearly separate confirmed facts from
expectations, and flag anything that changes the currently recommended
sequence: NSF CAREER (deadline July 22, 2026, now past) -> AFOSR YIP FY27
white paper -> DOE ECRP 2027 pre-application (~March 2027) -> DoD DURIP
(~April 2027).
""" + "\n" + OUTPUT,
    },
    "05-precedent-novelty": {
        "job": "PRECEDENT",
        "query": """\
Has anyone applied cost-aware Bayesian optimization of function networks
(BOFN) with partial evaluations - i.e., an optimizer that models a multi-stage
pipeline as a directed acyclic graph of surrogate models and chooses which
intermediate node (e.g., a cheap thermodynamic simulation or proxy experiment
vs. an expensive final property measurement) to evaluate next based on
information gained per unit cost - to an additive manufacturing pipeline for
metal alloys (composition -> powder atomization -> laser powder bed fusion ->
microstructure -> mechanical property)? Consider both journal papers and
preprints, with emphasis on anything from 2025-2026, and include close
analogues (multi-stage / cascade BO, multi-fidelity BO with intermediate
process outputs, process-structure-property chained Gaussian processes) in
metals AM, alloy design, or other materials-manufacturing pipelines. Exclude
publications by Sterling G. Baird. State clearly whether the claim "applied
for the first time to a complex additive manufacturing pipeline for alloys"
is still defensible, and suggest a safer wording if not.
""",
    },
}


def client() -> EdisonClient:
    return EdisonClient(api_key=os.environ["EDISON_PLATFORM_API_KEY"])


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def submit() -> None:
    if TASK_FILE.exists():
        sys.exit(f"{TASK_FILE} already exists; refusing to resubmit.")
    c = client()
    records = {}
    for name, spec in QUERIES.items():
        req = TaskRequest(name=getattr(JobNames, spec["job"]), query=spec["query"])
        task_id = str(c.create_task(task_data=req))
        records[name] = {"task_id": task_id, "job": spec["job"], "submitted": now()}
        print(f"{name}: {spec['job']} -> {task_id}", flush=True)
    TASK_FILE.write_text(json.dumps(records, indent=2) + "\n")


def wait(poll: int = 120, max_minutes: float = 55.0) -> None:
    c = client()
    records = json.loads(TASK_FILE.read_text())
    start = time.time()
    while True:
        statuses = {}
        for name, rec in records.items():
            try:
                statuses[name] = str(c.get_task(task_id=rec["task_id"]).status)
            except Exception as exc:  # transient API errors: keep polling
                statuses[name] = f"poll-error: {type(exc).__name__}"
        elapsed = (time.time() - start) / 60
        print(f"[{now()} +{elapsed:.1f} min] {statuses}", flush=True)
        if all(s in TERMINAL for s in statuses.values()):
            break
        if elapsed > max_minutes:
            print("Stopping wait: max_minutes reached.", flush=True)
            break
        time.sleep(poll)


def fetch() -> None:
    c = client()
    records = json.loads(TASK_FILE.read_text())
    RAW_DIR.mkdir(exist_ok=True)
    for name, rec in records.items():
        task = c.get_task(task_id=rec["task_id"])
        status = str(task.status)
        rec["status"] = status
        if status not in TERMINAL:
            print(f"{name}: still {status}; skipping", flush=True)
            continue
        verbose = c.get_task(task_id=rec["task_id"], verbose=True)
        (RAW_DIR / f"{name}.json").write_text(
            json.dumps(
                {
                    "task": task.model_dump(mode="json"),
                    "verbose": verbose.model_dump(mode="json"),
                },
                indent=1,
            )
            + "\n"
        )
        answer = (
            getattr(task, "formatted_answer", None)
            or getattr(task, "answer", None)
            or "(no answer returned)"
        )
        rec["fetched"] = now()
        header = (
            "<!--\n"
            f"Edison Scientific {rec['job']} task\n"
            f"- Task ID: {rec['task_id']}\n"
            f"- Submitted: {rec['submitted']}\n"
            f"- Fetched: {rec['fetched']} (status: {status})\n"
            f"- Raw trajectory JSON: raw/{name}.json\n"
            "- Companion to: README.md (synthesis), ../../afosr-yip-white-paper/\n"
            "-->\n\n"
        )
        body = f"Question:\n\n{QUERIES[name]['query'].strip()}\n\n---\n\n{answer.strip()}\n"
        (HERE / f"{name}.md").write_text(header + body)
        print(f"{name}: {status}, wrote {name}.md", flush=True)
    TASK_FILE.write_text(json.dumps(records, indent=2) + "\n")


if __name__ == "__main__":
    if sys.argv[1] == "wait" and len(sys.argv) > 2:
        wait(max_minutes=float(sys.argv[2]))
    else:
        {"submit": submit, "wait": wait, "fetch": fetch}[sys.argv[1]]()
