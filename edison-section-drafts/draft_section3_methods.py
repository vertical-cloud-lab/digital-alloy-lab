#!/usr/bin/env python3
"""Edison ANALYSIS: Draft §3 — Proposed Research and Methods (~400 words).

Drafts the methods section with 3 activity blocks, project management, and risk mitigation.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "methods"
OUTPUT_FILE = "section3_methods_draft.md"

QUERY = """You are drafting §3 — Proposed Research and Methods for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

WORD BUDGET: ~400 words. This is the largest narrative section.

STRUCTURE — 3 Activity blocks + management + risk:

**Activity 1: AI-Guided Computational Screening (~100w)**
- BOFN DAG over CALPHAD nodes, pKGFN acquisition function
- Mineral-burden multi-objective optimization
- Thermo-Calc TCAL10/TCMG6 + AM Module for printability screening
- HPC parallelization on BYU cluster
- Responsibility: PI (BYU)

**Activity 2: Experimental Validation Pipeline (~100w)**
- Ultrasonic atomization (AMAZEMET at BYU) + gas atomization (Valimet subaward)
- LPBF printing (U Utah Taylor Sparks lab; 3D Powder Tech backup)
- MVS progression: single tracks → density cubes → tensile bars
- Tiered screening: ~50 full tensile + ~150 hardness/density only
- Responsibility: PI + partners

**Activity 3: Closed-Loop Integration, Dissemination & Qualification (~100w)**
- Autonomous campaign orchestration, pKGFN-driven experiment selection
- ISO 52902 benchmark geometry, digital thread assembly
- Scalable deployment: PI has track record via POSE, Acceleration Consortium standards, FAIR practices, GCMAC
- Honegumi tutorials + Meta BoTorch integration (letter of support from Meta)
- Workflow orchestration expertise from Acceleration Consortium
- Responsibility: PI

**Project Management (~75w)**
- Weekly PI-partner sync calls, monthly all-hands reviews
- Shared FAIR-compliant database with version control
- PI retains final go/no-go decision authority
- Data sharing via Genesis Mission AmSC platform
- UG supervision: shift-based lab roles with PI/MS oversight, each UG assigned specific pipeline stage
- 10 UGs framed as throughput ADVANTAGE: 6-day/week operation → >=8 compositions/month

**Risk Mitigation (~50w)**
- Low atomization yield → fallback to Valimet gas atomization
- Modest BOFN advantage → honest reporting via time-ledger decomposition
- LPBF access disrupted → 3D Powder Tech backup
- Tiered screening manages throughput risk

**Preliminary results to weave in:**
- pKGFN verified on manufacturing benchmark (convergence plot)
- TC simulations running on BYU HPC
- SEM/EDS of atomized powders confirming composition control (Fig. 2)
- AlSi10Mg tensile baseline from U Utah

Reference Fig. 1 (pKGFN pipeline + convergence) and Fig. 3 (4-panel composite). Include "Relationship to Prior Work" paragraph.

Using attached documents, draft polished prose for LaTeX. Formal, quantitative, reviewer-ready.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# §3 — Proposed Research and Methods (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
