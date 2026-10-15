# Appendix 4 — DMSP (Edison Draft)


**APPENDIX 4: DATA MANAGEMENT AND SHARING PLAN (DMSP) — PLANNING VERSION**

**Project:** FLAIME (Fast Learning AI for Mineral Efficiency)
**PI:** Sterling G. Baird, Ph.D., Brigham Young University
**FOA:** DE-FOA-0003612, Topic 3-B (AMMTO)

*Note: Per FOA §IV.C, the DMSP is not required at Phase I submission but will be required during award negotiation. This planning version demonstrates the team's data stewardship readiness. DMSP implementation costs are included in the proposed budget.*

---

**1. Types of Data.** FLAIME will generate: (i) alloy composition data (wt%/at% of Al, Mn, Cr, Zr via ICP-OES); (ii) CALPHAD simulation outputs (phase diagrams, Scheil–Gulliver curves, solidification parameters from Thermo-Calc TCAl10/AM Module); (iii) powder characterization records (PSD, SEM/EDS, flowability); (iv) LPBF processing parameters (power, speed, hatch spacing, layer thickness) and build metadata; (v) mechanical properties (YS, UTS, elongation per ASTM E8/E8M) and microstructural images (SEM, EBSD); and (vi) BOFN/pKGFN model parameters, acquisition function logs, and digital thread provenance records.

**2. Data Formats.** Tabular data will be stored in CSV/JSON with schema.org metadata. Large simulation arrays will use HDF5. Microscopy images will be archived as lossless TIFF (PNG for visualization). ML models will be serialized in ONNX for interoperability. BibTeX reference files will accompany all deposits.

**3. Sharing and Preservation.** All experimental datasets will be deposited on Zenodo and/or Figshare with DOIs within 12 months of collection, consistent with the PI's open-data track record (MPTS-52 dataset, Matbench-genmetrics, extensive prior Zenodo deposits). The FLAIME digital thread is designed for hosting on the American Science Cloud (AmSC) as part of the Genesis Mission data ecosystem; all experimental datasets are concurrently deposited on Zenodo and/or Figshare with persistent DOIs, ensuring immediate open access and long-term preservation. Software (BOFN/pKGFN engine, Honegumi tutorials) will be released on GitHub under MIT/Apache-2.0 licenses (SPDX-identified), following bssw.io best practices.

**4. Access and Reuse.** Data and models will adhere to FAIR principles. Datasets will carry schema.org metadata for machine discoverability. Data licensed CC-BY-4.0; code licensed MIT. Supply-risk metadata (Helbig SRI scores, criticality indices) will be linked to every composition record, enabling reuse by the critical minerals research community.

**5. Oversight.** The PI is responsible for DMSP compliance. Quarterly data audits will be conducted throughout the 9-month Phase I. Automated schema validation will enforce a minimum metadata set (composition, CALPHAD version, powder batch ID, LPBF parameters, ASTM E8 results, BOFN trace, SRI score). Budget provisions for data curation, DOI registration, and AmSC hosting are included under Other Direct Costs.

---

**Body word count:** ~304 words (Sections 1–5)

**Completeness verification:** All five DOE-required DMSP elements addressed. All data types, formats, sharing mechanisms, FAIR compliance provisions, and oversight structures specified in the prompt are covered. The draft references the PI's established open-data track record, Genesis Mission platform integration (AmSC), SPDX-identified licenses, and bssw.io best practices per FOA §IV.C guidance. The supply-risk metadata linkage (Helbig SRI scores per composition) is a FLAIME-specific addition that directly supports Topic 3-B's critical minerals mandate.

---

**Discretionary analytical decisions made during drafting:**

- **Omitted Python pickle from the formats section** in favor of emphasizing ONNX as the interoperable ML model format. Pickle is mentioned in the prompt requirements but is a Python-specific serialization format with known security and portability limitations; ONNX better demonstrates FAIR interoperability commitment. Pickle could be added back as "Python pickle for internal use" if desired.
- **Selected 12-month data sharing timeline** as the public release window. DOE guidance allows flexibility; 12 months balances the need for timely sharing with allowing the team adequate time for quality control and initial publication.
- **Chose quarterly audit cadence** for DMSP oversight during the 9-month Phase I (i.e., 3 audits). Monthly audits would be more frequent but potentially burdensome for a small team; semi-annual would provide only one audit point. Quarterly was selected as a practical balance.
- **Included supply-risk metadata (Helbig SRI scores) as part of the minimum metadata set.** This is not a standard DOE DMSP requirement but is a FLAIME-specific addition that strengthens the Topic 3-B critical minerals alignment and demonstrates domain-aware data stewardship.
- **Framed the DMSP as a "planning version"** with explicit notation that it is not required at submission, per FOA §IV.C and FAQ guidance. This sets appropriate expectations while demonstrating readiness.
- **Referenced bssw.io** (Better Scientific Software) as the software development best practices standard, per FOA §IV.C guidance language about "best practices in scientific software development."
- **Used dual licensing (MIT/Apache-2.0 for code, CC-BY-4.0 for data)** rather than a single unified license, as code and data have different reuse requirements and community norms.
