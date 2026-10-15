#!/usr/bin/env python3
"""Edison ANALYSIS: Draft Appendix 2 — Facilities & Other Resources.

Drafts the facilities section covering BYU lab, partner LPBF access, and computing.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "facilities"
OUTPUT_FILE = "appendix2_facilities_draft.md"

QUERY = """You are drafting Appendix 2 — Facilities & Other Resources for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

CONSTRAINT: <=0.5 page (~250 words). Dense, factual, equipment-focused.

MUST COVER:

**BYU Laboratory (Lead Institution):**
- AMAZEMET ultrasonic atomizer (installed, operational) — enables rapid custom powder production
- SEM/EDS/EBSD suite for powder and part characterization
- Universal testing machine (ASTM E8/E8M tensile testing capability)
- Powder characterization: PSD (laser diffraction), flowability, apparent density

**Partner LPBF Access:**
- University of Utah (Prof. Taylor Sparks lab) — LPBF printing capability
- 3D Powder Tech — backup LPBF printing capacity (letter of support)

**Computing Resources:**
- BYU HPC cluster for CALPHAD screening (TC-Python parallelized)
- Thermo-Calc licenses: TCAL10, TCMG6, AM Module (via collaboration letter)
- GPU nodes for BoTorch/GPyTorch model training

**Appendix figures to reference (not in word count):**
- AMAZEMET atomizer installation photo
- LPBF parameter space tile grid (36-parameter taxonomy)
- AM test structure schematics (build plate layout: single tracks → tensile bars)
- pKGFN convergence and cost efficiency plots

Using attached documents (especially am-scaleup-test-structures.md and calphad_hpc.md), draft polished prose for LaTeX. Formal, equipment-focused, reviewer-ready.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# Appendix 2 — Facilities & Other Resources (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
