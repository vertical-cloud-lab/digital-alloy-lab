#!/usr/bin/env python3
"""Edison ANALYSIS: Draft §5 — Data Sources and Models (~160 words).

Drafts the data sources section covering CALPHAD, databases, AI frameworks, and AmSC integration.
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "data_sources"
OUTPUT_FILE = "section5_data_sources_draft.md"

QUERY = """You are drafting §5 — Data Sources and Models for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

WORD BUDGET: ~160 words. Concise and information-dense.

MUST COVER:
1. Data sources: Thermo-Calc TCAL10/TCMG6 databases, Materials Project, MMPDS handbook
2. Team access: BYU HPC Thermo-Calc license, TC collaboration letter, TC-Python API access
3. AI models/frameworks: BoTorch/BOFN, pKGFN acquisition function, GPyTorch surrogates
4. Genesis Mission platform integration (BIDIRECTIONAL):
   - FLAIME hosts digital thread, alloy database, and BOFN/pKGFN models on American Science Cloud (AmSC)
   - Team participates in Genesis Mission coordination activities
   - BOFN/pKGFN released as domain-specific "plug-and-play" capability per GM framework
   - FLAIME leverages other GM teams' validated data (shared characterization databases, benchmark alloy property sets) to accelerate CALPHAD surrogate training
5. Open data and software dissemination:
   - All experimental data published on Zenodo/Figshare with DOIs
   - PI track record: MPTS-52 dataset heavily reused by crystal structure generative AI community
   - BOFN/pKGFN code released as open-source Python packages with Honegumi tutorials
   - Software contributions targeted for Meta's BoTorch tutorial ecosystem (letter of support from Meta)

NOTE: Computing resources go in Appendix 2, NOT here.

Using attached documents, draft polished prose for LaTeX. Formal, quantitative, reviewer-ready.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# §5 — Data Sources and Models (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
