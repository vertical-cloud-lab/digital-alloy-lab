# Edison persona-grounded mock-review prompt — emergent AI/data-cluster candidates (TMS 2027)

## Task
You are a panel of TMS 2027 symposium organizers. For EACH symposium below, role-play its named
organizing committee (use their real research personas/affiliations) and give a mock reviewer verdict on
the abstract that follows: (a) ACCEPT / ACCEPT-WITH-REVISIONS / REJECT for an oral talk; (b) a 1-5
scope-fit score; (c) the single strongest reason for and against; (d) concrete tailoring to maximize
acceptance and audience resonance. Then rank the symposia from best to worst home for this specific
abstract, and state whether any beats the two incumbents (Flyer 012 "Rapid Acquisition/Large Datasets"
and Flyer 086 "Fullwood Microstructure-Sensitive Design & Advanced Characterization", already reviewed
separately). Be blunt about stretches. Ground every claim about the organizers in their actual work.

## Abstract under review
Multi-modal characterization-parameter optimization for compositional & microstructural analysis of AM
alloys. A closed-loop, agentic decision-support system that recommends and iteratively refines
acquisition/processing parameters across SEM, EDS, EBSD, XRD, and XRF for a given sample and analysis
goal. Grounded in three sources of truth: (1) retrieval-augmented generation over characterization
standards/texts (ASTM E1508, E2627), (2) electron-beam / interaction-volume simulation, and (3) an
accumulating, provenance-tracked dataset of parameter sweeps acting as in-house "standards." Validated on
commercial (AlSi10Mg) and supply-chain-resilient aluminum in powder and printed form, benchmarking
EDS/XRF composition against orthogonal ICP-MS/MS. Motivating data: standardless eZAF over-reports Mg in
AlSi10Mg several-fold; EBSD CI yield on LPBF Al-Si rose from ~40% to ~77% once beam current and phase
model were corrected. Deliverable: a labeled, FAIR characterization-parameter dataset making expert
instrument setup reproducible and transferable. Early-stage group ("we are building"; "emerging").

## Symposia to review (organizers to role-play)

### Flyer 022 — AI/ML/Data Informatics for Materials Discovery: Bridging Experiment, Theory, and Modeling
Scope: frontiers of AI/ML/DI for materials discovery; data-centric challenges (sparse/noisy/multimodal);
LLMs, multimodal foundation models, agentic AI for workflow assistance/literature mining; hybrid AI +
physics-based models; AI-driven data generation/extraction/curation; FAIR/metadata/provenance; integrate
experimental + computational + literature data. Organizers: Christopher Stiles (JHU APL), Niaz Abdolrahim
(U Rochester), Kamal Choudhary (JHU), Dehao Liu (Binghamton), Darren Pagan (Penn State), James Saal
(Citrine Informatics), Daniel Wines (NIST), Taylor Sparks (University of Utah), Mahmood Mamivand (Boise State).

### Flyer 024 — Artificial Intelligence Applications in Integrated Computational Materials Engineering (AI-ICME)
Scope: AI across ICME process-structure-property-performance; AI-enabled microstructure characterization
and structure-property inference from multimodal data (images, spectra, processing history); active
learning/Bayesian optimization/autonomous closed-loop experimentation; data curation, standards,
provenance/traceability, reproducible MLOps; foundation models/LLMs for knowledge extraction, workflow
assistance, decision support; data quality, reproducibility, adoption in certification contexts.
Organizers: Wenwu Xu (SDSU), Qiaofu Zhang (U Alabama), Brandon Bocklund (LLNL), Ram Devanathan (PNNL),
Arezoo Emdadi (Missouri S&T), Victoria Miller (U Florida), Pinar Acar (Virginia Tech), Avanish Mishra
(LANL), Ghanshyam Pilania (GE Aerospace Research).

### Flyer 023 — Algorithms Development in Materials Science and Engineering
Scope: novel algorithms; data mining/ML/image processing; surrogate/reduced-order models; agentic
workflows for planning, decision-making, and orchestration of complex materials simulations; fusing and
evaluating quality of multimodal data; FAIRization of data; V&V benchmarks. Organizers: Remi Dingreville
(Sandia), Saaketh Desai (Sandia), Hojun Lim (Sandia), Jeremy Mason (UC Davis), Sam Reeve (ORNL), Vimal
Ramanuj (ORNL).

### Flyer 021 — AI-Enabled Materials Processing: Integrating Accelerated Experimental Workflows and Processing-Aware ML
Scope: AI integrated with experimental processing; process-aware microstructure/property control; Bayesian
optimization, adaptive experimentation, closed-loop control; high-quality processing-structure-property
datasets. (NOTE: a companion abstract already targets this symposium — flag collision risk.) Organizers:
Sreenivas Raguraman (JHU), Maitreyee Sharma Priyadarshini (Virginia Tech), Timothy Weihs (JHU), Thomas
Voisin (LLNL), Allison Beese (Penn State), Samantha Webster (Colorado School of Mines).

## Deliverables
1. Per-symposium verdict table (accept/revise/reject, 1-5 fit, for/against, tailoring).
2. A ranked recommendation across all four PLUS the two incumbents (012, 086).
3. The single best home and why, with the specific reframe that would maximize acceptance there.

---
**Job:** `JobNames.LITERATURE_HIGH`, task `af856509-eb79-4a0f-81eb-7497792ae504`, submitted 2026-07-09.
Fetch with `client.get_task("af856509-eb79-4a0f-81eb-7497792ae504")`. Poll ~15 min (high-effort literature).

**STATUS: FETCHED 2026-07-10** (`status=success`). Full result → [`edison-mock-review-result.md`](edison-mock-review-result.md);
verdict + tailoring appended to [`top-10-symposium-fit-ranking.md`](top-10-symposium-fit-ranking.md).
Bottom line: **022 (best) and 024 both beat both incumbents (086, 012); 021 is a soft reject.**
