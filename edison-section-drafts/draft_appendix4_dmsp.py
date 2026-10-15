#!/usr/bin/env python3
"""Edison ANALYSIS: Draft DMSP (Data Management and Sharing Plan).

Drafts the DMSP planning content (not required at submission but needed at award).
"""

import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from edison_utils import (
    create_edison_client, upload_files, submit_and_poll, save_result,
    get_core_context_files, get_section_specific_files,
)

SECTION = "data_sources"  # Reuse data_sources context files
OUTPUT_FILE = "appendix4_dmsp_draft.md"

QUERY = """You are drafting Appendix 4 — Data Management and Sharing Plan (DMSP) for a DOE Genesis Mission Phase I proposal (Topic 3B, AMMTO).

PROJECT: FLAIME (Fast Learning AI for Mineral Efficiency)

NOTE: Per FOA §IV.C, the DMSP is "NOT required at submission; required at award." However, the proposal may request DMSP implementation costs in the budget. Draft a planning version that demonstrates the team's data management readiness.

The DMSP must address (per DOE guidelines):

1. **Types of Data:** Composition data (wt%/at% of Al, Mn, Cr, Zr, etc.), CALPHAD simulation outputs (phase diagrams, Scheil curves, solidification parameters), powder characterization (PSD, SEM/EDS, flowability), LPBF processing parameters (power, speed, hatch, layer thickness), mechanical properties (YS, UTS, elongation from ASTM E8), microstructural images (SEM, EBSD), BOFN/pKGFN model parameters and acquisition function logs.

2. **Data Formats:** CSV/JSON for tabular data, HDF5 for large simulation arrays, TIFF/PNG for microscopy, Python pickle/ONNX for ML models, BibTeX for references.

3. **Sharing and Preservation:**
   - Public datasets on Zenodo and Figshare with DOIs (within 12 months of collection)
   - Digital thread hosted on American Science Cloud (AmSC) per Genesis Mission framework
   - Code on GitHub under MIT/Apache-2.0 license
   - PI track record: MPTS-52 dataset, Matbench-genmetrics, extensive Zenodo deposits

4. **Access and Reuse:** FAIR principles (Findable, Accessible, Interoperable, Reusable). Schema.org metadata. CC-BY-4.0 for data, MIT for code.

5. **Oversight:** PI responsible for DMSP compliance. Quarterly data audits during 9-month Phase I.

Draft ~300 words. Formal DOE style, demonstrating readiness for data stewardship.
"""


def main():
    client = create_edison_client()
    files = get_core_context_files() + get_section_specific_files(SECTION)
    print(f"Uploading {len(files)} files for {SECTION}...")
    file_ids = upload_files(client, files)
    print(f"Submitting ANALYSIS task for {SECTION}...")
    result = submit_and_poll(client, QUERY, file_ids)
    save_result(OUTPUT_FILE, f"# Appendix 4 — DMSP (Edison Draft)\n\n{result}")
    print("Done.")


if __name__ == "__main__":
    main()
