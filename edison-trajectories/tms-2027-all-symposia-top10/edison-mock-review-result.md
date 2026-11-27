Question: # Edison persona-grounded mock-review prompt — emergent AI/data-cluster candidates (TMS 2027)

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


# Mock Panel Review: Multi-Modal Characterization-Parameter Optimization Abstract for TMS 2027

## 1. Per-Symposium Verdict Table

The following table presents mock reviewer verdicts from each symposium's organizing committee, grounded in the organizers' published research personas.

| Symposium | Verdict | Scope-Fit Score (1-5) | Strongest FOR | Strongest AGAINST | Key Tailoring Advice |
|---|---|---:|---|---|---|
| Flyer 022 — AI/ML/Data Informatics for Materials Discovery | ACCEPT-WITH-REVISIONS | 4 | The RAG + agentic workflow, FAIR/provenance-tracked dataset, and multimodal integration across SEM/EDS/EBSD/XRD/XRF map directly onto this symposium’s stated interests in LLMs, agentic AI, multimodal data, and FAIR metadata; this is especially aligned with Choudhary’s JARVIS/data-infrastructure work and Saal’s multimodal experimental data-management emphasis (bauer2024roadmapondatacentric pages 34-36, allec2024acasestudy pages 25-25, zhang2026towardsagenticintelligence pages 36-38, zhang2026towardsagenticintelligence pages 11-13). | The center of gravity is instrument setup optimization, not materials discovery or property prediction; it risks reading as “better microscope knobs” rather than a discovery-enabling informatics contribution (kavalsky2023byhowmuch pages 23-27, fowler2024beyondcombinatorialmaterials pages 2-4). | Make the AI/data contribution the headline: foreground the RAG architecture, ASTM-grounded retrieval, provenance schema, and FAIR dataset; demote the AlSi10Mg case studies to validation examples; explicitly cast the work as a multimodal foundation/decision-support problem for characterization workflows (bauer2024roadmapondatacentric pages 27-29, bauer2024roadmapondatacentric pages 55-58, zhang2026towardsagenticintelligence pages 36-38, zhang2026towardsagenticintelligence pages 4-5). |
| Flyer 024 — Artificial Intelligence Applications in Integrated Computational Materials Engineering (AI-ICME) | ACCEPT-WITH-REVISIONS | 4 | The abstract hits nearly every scope bullet: AI-enabled microstructure characterization, multimodal data, closed-loop decision support, standards/provenance/traceability, and reproducibility; Acar’s microstructure-sensitive design perspective and Bocklund-style standardization logic make the EBSD/EDS optimization story plausible here (kavalsky2023byhowmuch pages 23-27, bauer2024roadmapondatacentric pages 55-58, bauer2024roadmapondatacentric pages 27-29). | It does not complete the ICME chain: process → structure → property → performance is implied but not demonstrated; the loop ends at characterization quality rather than downstream materials response or certification-relevant prediction (bauer2024roadmapondatacentric pages 55-58, zhang2026towardsagenticintelligence pages 34-36). | Add one explicit sentence that optimized characterization settings improve downstream property-model inputs, uncertainty bounds, or certification traceability; position the system as the characterization node in an ICME digital thread rather than as a standalone microscopy assistant (kavalsky2023byhowmuch pages 23-27, bauer2024roadmapondatacentric pages 55-58, bauer2024roadmapondatacentric pages 27-29). |
| Flyer 023 — Algorithms Development in Materials Science and Engineering | ACCEPT-WITH-REVISIONS | 3 | The strongest fit is the algorithmic scaffold: agentic orchestration, simulation-informed parameter recommendation, multimodal evidence fusion, and a verification benchmark against ICP-MS/MS; that resonates with Dingreville’s interest in multimodal ML and benchmarked autonomous workflows (boyce2024beyondfingerprintingaiguideddiscovery pages 45-49, boyce2024beyondfingerprintingaiguideddiscovery pages 37-41, fowler2024beyondcombinatorialmaterials pages 2-4, zhang2026towardsagenticintelligence pages 34-36). | The novelty currently reads as workflow composition rather than a genuinely new algorithmic method; for a Sandia/ORNL-heavy algorithms audience, the work may look more like applied lab automation than a methods paper (boyce2024beyondfingerprintingaiguideddiscovery pages 94-96, boyce2024beyondfingerprintingaiguideddiscovery pages 45-49, boyce2024beyondfingerprintingaiguideddiscovery pages 37-41). | Reframe around the decision policy: define how the agent selects the next parameter sweep, what objective it optimizes, how uncertainty enters, and what constitutes convergence; present eZAF-vs-ICP-MS and EBSD CI improvement as formal V&V benchmarks (kavalsky2023byhowmuch pages 23-27, fowler2024beyondcombinatorialmaterials pages 2-4, zhang2026towardsagenticintelligence pages 34-36). |
| Flyer 021 — AI-Enabled Materials Processing | REJECT (soft) | 2 | The AM alloy context, especially LPBF AlSi10Mg, overlaps with the organizer base in additive manufacturing and process-structure-property work; there is philosophical alignment with efforts to elevate processing in AI-driven materials workflows (zhang2026towardsagenticintelligence pages 2-4, zhang2026towardsagenticintelligence pages 34-36). | This is fundamentally not a processing paper: it optimizes characterization parameters, not manufacturing parameters or closed-loop processing. EBSD beam current correction is not LPBF process optimization, and the abstract does not feed recommendations back to fabrication; companion-abstract collision makes the stretch worse. | Only submit here if radically reframed to show characterization-driven feedback into AM process optimization, defect control, or process maps; otherwise this is the wrong room. |


*Table: This table gives mock oral-talk verdicts, fit scores, strongest pros/cons, and targeted reframing advice for the four new TMS 2027 symposia. It is useful for deciding where the abstract has the best odds and how to rewrite it for each audience.*

---

## 2. Detailed Per-Symposium Reviews

### Flyer 022 — AI/ML/Data Informatics for Materials Discovery (ACCEPT-WITH-REVISIONS, 4/5)

**Role-playing the committee (Stiles, Choudhary, Saal, Sparks, Wines, Pagan, et al.):**

This abstract hits several of our explicit scope calls. Choudhary, whose JARVIS infrastructure provides one of the largest FAIR materials databases in the community, immediately recognizes the provenance-tracked, FAIR characterization-parameter dataset as addressing an acute gap—experimental characterization metadata is exactly the data modality that remains under-standardized relative to computational data (bauer2024roadmapondatacentric pages 34-36). Saal, whose Citrine-affiliated work on multimodal, multi-institutional data management for combinatorial materials science demonstrated the difficulty of standardizing experimental datasets across instruments and institutions, would find the ASTM-grounded retrieval augmented generation (RAG) system compelling (allec2024acasestudy pages 25-25, bauer2024roadmapondatacentric pages 55-58). Stiles, who led closed-loop ML discovery for superconductors at JHU APL, understands the value of iterative experimental-feedback loops (boyce2024beyondfingerprintingaiguideddiscovery pages 94-96). The symposium explicitly calls for "agentic AI for workflow assistance" and "FAIR/metadata/provenance"—this abstract is arguably more aligned with those bullets than typical submissions that focus on ML property prediction.

**Strongest FOR:** The RAG-over-standards architecture, the multi-source-of-truth design (standards, simulation, accumulated data), and the FAIR dataset deliverable directly instantiate the symposium's vision for data-centric, LLM-grounded materials informatics (zhang2026towardsagenticintelligence pages 36-38, zhang2026towardsagenticintelligence pages 11-13).

**Strongest AGAINST:** The abstract optimizes instrument parameters, not material properties. The audience gravitates toward discovering new materials or predicting properties; "better SEM knobs" is not intuitively a "discovery" contribution. This requires reframing.

**Tailoring:** Foreground the AI/data architecture: the RAG retrieval over ASTM E1508/E2627, the interaction-volume simulation as physics-informed inductive bias, and the provenance schema. Relegate AlSi10Mg/LPBF results to validation vignettes. Explicitly position this as a multimodal decision-support problem analogous to how agentic systems integrate tool-use and evidence-grounded reasoning (zhang2026towardsagenticintelligence pages 11-13, zhang2026towardsagenticintelligence pages 4-5).

---

### Flyer 024 — AI Applications in ICME (ACCEPT-WITH-REVISIONS, 4/5)

**Role-playing the committee (Xu, Zhang, Bocklund, Devanathan, Emdadi, Miller, Acar, Mishra, Pilania):**

This abstract maps cleanly onto our scope's AI-enabled microstructure characterization, closed-loop experimentation, data curation/standards/provenance, and LLM-for-decision-support bullets. Acar, whose physics-informed neural network work on microstructure-sensitive design at Virginia Tech treats microstructural representations as first-class design variables, would appreciate that EBSD confidence index improvement directly affects the quality of orientation distribution functions used in downstream ICME models. Bocklund, who works on CALPHAD data standardization at LLNL, understands the challenge of maintaining provenance and traceability across data workflows (kavalsky2023byhowmuch pages 23-27). Pilania at GE Aerospace Research would be interested in the reproducibility/certification angle—if characterization parameters are not reproducible, downstream property predictions inherit that uncertainty.

**Strongest FOR:** The scope match is nearly line-by-line, especially the intersection of AI-enabled characterization, multimodal data, provenance/traceability, and decision support (bauer2024roadmapondatacentric pages 55-58, bauer2024roadmapondatacentric pages 27-29).

**Strongest AGAINST:** The abstract does not complete the ICME chain. Process → structure → property → performance is the ICME DNA; this work stops at "better characterization" without demonstrating that improved characterization parameters actually improve downstream property predictions or certification outcomes (zhang2026towardsagenticintelligence pages 34-36).

**Tailoring:** Add one sentence connecting optimized characterization to downstream ICME utility—e.g., "corrected EBSD phase models reduce orientation-distribution-function uncertainty, tightening bounds on predicted anisotropic yield surfaces." Frame the system as the "characterization node" in an ICME digital thread. Cite reproducibility as an adoption barrier for qualification and certification workflows—Pilania's aerospace context makes this resonate.

---

### Flyer 023 — Algorithms Development in Materials Science and Engineering (ACCEPT-WITH-REVISIONS, 3/5)

**Role-playing the committee (Dingreville, Desai, Lim, Mason, Reeve, Ramanuj):**

Dingreville's Sandia team works on physics-informed ML frameworks for multimodal data analysis, including variational inference for cross-modal discovery and neural-operator-accelerated microstructure simulations (boyce2024beyondfingerprintingaiguideddiscovery pages 45-49). The abstract's agentic orchestration across simulation (interaction-volume modeling), text retrieval (ASTM standards), and experimental feedback (parameter sweeps) has algorithmic substance. Desai would appreciate the V&V angle—benchmarking eZAF against ICP-MS/MS is exactly the kind of verification protocol this symposium values (boyce2024beyondfingerprintingaiguideddiscovery pages 37-41).

**Strongest FOR:** The multi-source decision architecture (RAG + simulation + accumulated data) and the ICP-MS/MS verification benchmark align with the symposium's interests in agentic workflows, multimodal data fusion, and V&V (boyce2024beyondfingerprintingaiguideddiscovery pages 45-49, fowler2024beyondcombinatorialmaterials pages 2-4).

**Strongest AGAINST:** This is a Sandia/ORNL-heavy algorithms symposium. The committee expects novel mathematical methods—optimization algorithms, surrogate-model architectures, convergence proofs. The current abstract reads as a workflow orchestrator, not a methods contribution. The "algorithm" is implicit (boyce2024beyondfingerprintingaiguideddiscovery pages 94-96, boyce2024beyondfingerprintingaiguideddiscovery pages 37-41).

**Tailoring:** Formalize the decision loop: what objective function does the agent optimize? How is parameter-space exploration balanced against exploitation? What is the convergence criterion? Present the eZAF-vs-ICP-MS comparison as a formal verification case study and the EBSD CI improvement as a validation metric. This transforms the talk from "we built a helpful tool" into "here is a novel decision algorithm with verified performance."

---

### Flyer 021 — AI-Enabled Materials Processing (REJECT, soft; 2/5)

**Role-playing the committee (Raguraman, Sharma Priyadarshini, Weihs, Voisin, Beese, Webster):**

Raguraman and Weihs at JHU recently published a Nature Reviews Materials commentary arguing for elevating the role of processing in AI-driven materials design. Voisin's LPBF microstructure work at LLNL and Beese's process-structure-property datasets on AlSi10Mg at Penn State mean the AM material system is familiar. However, this abstract fundamentally optimizes characterization parameters (beam current, EDS acquisition settings, EBSD phase models), not manufacturing parameters (laser power, scan speed, hatch spacing). The closed loop feeds back to the microscope, not to the printer. That is a category error for a processing symposium.

**Strongest FOR:** The AlSi10Mg LPBF application overlaps with Beese's and Voisin's core systems, and the philosophical alignment with Raguraman's "process-aware" AI vision is real (zhang2026towardsagenticintelligence pages 2-4).

**Strongest AGAINST:** Characterization-parameter optimization ≠ process-parameter optimization. EBSD beam current is not LPBF laser power. The companion-abstract collision further complicates the submission.

**Tailoring:** Only viable if radically reframed to show that AI-optimized characterization feeds actionable data back into processing decisions—e.g., "EBSD-derived microstructure maps at >77% CI enable statistically significant detection of process-induced texture anomalies, feeding closed-loop build-parameter correction." That would be a different abstract.

---

## 3. Ranked Recommendation Across All Six Symposia

The following table ranks all six venues—four new candidates plus the two incumbents (Flyer 012 and Flyer 086)—from best to worst home for this abstract.

| Rank | Symposium | Scope-Fit Score (1-5) | Verdict | Rationale for Ranking |
|---:|---|---:|---|---|
| 1 | Flyer 022 — AI/ML/Data Informatics for Materials Discovery | 4 | ACCEPT-WITH-REVISIONS | Best home. The abstract’s core pieces—agentic AI, retrieval-grounded standards use, multimodal fusion across SEM/EDS/EBSD/XRD/XRF, and a FAIR/provenance-tracked dataset—map almost line-by-line onto this symposium’s stated interests. Choudhary’s JARVIS/data-infrastructure work and Saal’s multimodal experimental data-management perspective make this an unusually natural audience for the dataset/provenance contribution, even if the “materials discovery” label is a mild stretch (bauer2024roadmapondatacentric pages 34-36, allec2024acasestudy pages 25-25, zhang2026towardsagenticintelligence pages 36-38, zhang2026towardsagenticintelligence pages 11-13, zhang2026towardsagenticintelligence pages 4-5). |
| 2 | Flyer 024 — Artificial Intelligence Applications in Integrated Computational Materials Engineering (AI-ICME) | 4 | ACCEPT-WITH-REVISIONS | Very close second. This symposium explicitly welcomes AI-enabled characterization, multimodal data, autonomous closed-loop workflows, provenance/traceability, and LLM-based decision support, so the fit is real. It ranks just behind 022 because the abstract stops at better characterization decisions and does not convincingly carry the ICME thread through to property/performance prediction or certification outcomes, though that gap is fixable in revision (kavalsky2023byhowmuch pages 23-27, bauer2024roadmapondatacentric pages 55-58, bauer2024roadmapondatacentric pages 27-29, zhang2026towardsagenticintelligence pages 34-36). |
| 3 | Flyer 086 — Fullwood Microstructure-Sensitive Design & Advanced Characterization | 3.5 | ACCEPT-WITH-REVISIONS | Strong incumbent. The EBSD confidence-index jump, AM-alloy characterization focus, and reproducible parameter dataset are exactly the sort of advanced characterization story this audience understands. It falls behind 022/024 because the abstract’s most novel layer is the AI/agentic orchestration, and that is less central to a characterization-first audience than to an AI/data-centric one (abdelal2026criticalreviewof pages 47-48, abdelal2026criticalreviewof pages 31-33, abdelal2026criticalreviewof pages 36-38). |
| 4 | Flyer 012 — Rapid Acquisition/Large Datasets | 3 | ACCEPT-WITH-REVISIONS | Plausible incumbent, but not ideal. The accumulating parameter-sweep library and reproducible acquisition setup fit a rapid-acquisition/large-dataset frame, and workflow design for characterization is relevant. Still, the real novelty is not throughput itself; it is the agentic decision-support system and standards/simulation-guided parameter recommendation, so this symposium captures the byproduct more than the intellectual center (bauer2024roadmapondatacentric pages 27-29, bauer2024roadmapondatacentric pages 55-58). |
| 5 | Flyer 023 — Algorithms Development in Materials Science and Engineering | 3 | ACCEPT-WITH-REVISIONS | Workable but not first-choice. Dingreville-style interests in multimodal data fusion, AI-guided workflows, and benchmarked autonomous systems create a legitimate opening. The problem is that the current abstract reads more like a smart orchestration framework for experimental characterization than a clearly novel algorithm paper; for this audience, the decision policy, objective function, uncertainty treatment, and verification protocol would need much sharper formalization (boyce2024beyondfingerprintingaiguideddiscovery pages 94-96, boyce2024beyondfingerprintingaiguideddiscovery pages 45-49, boyce2024beyondfingerprintingaiguideddiscovery pages 37-41, fowler2024beyondcombinatorialmaterials pages 2-4, zhang2026towardsagenticintelligence pages 34-36). |
| 6 | Flyer 021 — AI-Enabled Materials Processing | 2 | REJECT (soft) | Worst home. Despite overlap in AM alloys and organizers with strong LPBF/process-structure-property expertise, the abstract is about optimizing characterization parameters, not processing parameters or manufacturing control. Beam current, phase model selection, and characterization setup are not substitutes for process-aware ML on fabrication variables, and the companion-abstract collision adds unnecessary risk (zhang2026towardsagenticintelligence pages 2-4, zhang2026towardsagenticintelligence pages 34-36). |


*Table: This table ranks all six symposium options from best to worst home for the abstract, with fit scores, oral-talk verdicts, and concise rationale grounded in the organizers’ research personas and the symposium scopes.*

---

## 4. Do Any of the Four New Symposia Beat the Two Incumbents?

**Yes—both Flyer 022 and Flyer 024 beat both incumbents for this specific abstract.** The reasoning is straightforward:

- **Flyer 086 (Fullwood/Microstructure-Sensitive Design)** is a strong characterization venue and the EBSD CI story would be well understood, but the abstract's intellectual center of gravity is the AI/agentic system, not the characterization results themselves. An advanced-characterization audience will treat the AI layer as supporting infrastructure rather than as the contribution, which undervalues the work.

- **Flyer 012 (Rapid Acquisition/Large Datasets)** captures the dataset-generation aspect but misses the decision-support and standards-retrieval architecture, which is the novelty.

- **Flyer 022** and **Flyer 024** are both AI/data-native symposia where the agentic architecture, RAG-over-standards, and FAIR provenance schema *are* the contribution, not backdrop. They also explicitly scope LLMs, agentic AI, multimodal data, and provenance—terms that describe this abstract's core innovations.

---

## 5. The Single Best Home and the Reframe That Maximizes Acceptance

**Best home: Flyer 022 — AI/ML/Data Informatics for Materials Discovery.**

**The reframe:** Retitle the talk to lead with the data-informatics contribution rather than the characterization application. For example:

> *"An Agentic, Standards-Grounded Decision-Support System for FAIR Characterization-Parameter Optimization: Architecture, Retrieval-Augmented Reasoning, and Validation on AM Aluminum Alloys"*

In the abstract body: (1) open with the data-centric problem—characterization metadata is the least standardized, least FAIR link in the materials-data pipeline, citing the roadmap-level calls for machine-readable SOPs and provenance schemas (bauer2024roadmapondatacentric pages 27-29, bauer2024roadmapondatacentric pages 55-58); (2) present the three-source-of-truth architecture (RAG over ASTM standards, interaction-volume simulation, provenance-tracked parameter sweeps) as the core AI/informatics contribution; (3) use the eZAF Mg over-reporting and EBSD CI improvement as quantitative validation vignettes, not as the headline; (4) close with the FAIR dataset deliverable as a community resource, connecting to the multimodal data integration and data extraction/curation scope bullets. This framing speaks directly to Choudhary's JARVIS-style data-infrastructure philosophy (bauer2024roadmapondatacentric pages 34-36), Saal's multimodal experimental data-management work (allec2024acasestudy pages 25-25, kavalsky2023byhowmuch pages 23-27), and the broader agentic-AI-for-materials paradigm that Zhang et al. describe as the frontier of materials informatics (zhang2026towardsagenticintelligence pages 36-38, zhang2026towardsagenticintelligence pages 2-4, zhang2026towardsagenticintelligence pages 11-13).

References

1. (bauer2024roadmapondatacentric pages 34-36): Stefan Bauer, Peter Benner, Tristan Bereau, Volker Blum, Mario Boley, Christian Carbogno, C Richard A Catlow, Gerhard Dehm, Sebastian Eibl, Ralph Ernstorfer, Ádám Fekete, Lucas Foppa, Peter Fratzl, Christoph Freysoldt, Baptiste Gault, Luca M Ghiringhelli, Sajal K Giri, Anton Gladyshev, Pawan Goyal, Jason Hattrick-Simpers, Lara Kabalan, Petr Karpov, Mohammad S Khorrami, Christoph T. Koch, Sebastian Kokott, Thomas Kosch, Igor Kowalec, Kurt Kremer, Andreas Leitherer, Yue Li, Christian H Liebscher, Andrew J Logsdail, Zhongwei Lu, Felix Luong, Andreas Marek, Florian Merz, Jaber R Mianroodi, Jörg Neugebauer, Zongrui Pei, Thomas A R Purcell, Dierk Raabe, Markus Rampp, Mariana Rossi, Jan-Michael Rost, James Saal, Ulf Saalmann, Kasturi Narasimha Sasidhar, Alaukik Saxena, Luigi Sbailò, Markus Scheidgen, Marcel Schloz, Daniel F Schmidt, Simon Teshuva, Annette Trunschke, Ye Wei, Gerhard Weikum, R Patrick Xian, Yi Yao, Junqi Yin, Meng Zhao, and Matthias Scheffler. Roadmap on data-centric materials science. Modelling and Simulation in Materials Science and Engineering, 32:063301, Jul 2024. URL: https://doi.org/10.1088/1361-651x/ad4d0d, doi:10.1088/1361-651x/ad4d0d. This article has 33 citations and is from a peer-reviewed journal.

2. (allec2024acasestudy pages 25-25): Sarah I. Allec, Eric S. Muckley, Nathan S. Johnson, Christopher K. H. Borg, Dylan J. Kirsch, Joshua Martin, Rohit Pant, Ichiro Takeuchi, Andrew S. Lee, James E. Saal, Logan Ward, and Apurva Mehta. A case study of multimodal, multi-institutional data management for the combinatorial materials science community. Integrating Materials and Manufacturing Innovation, 13:406-419, Mar 2024. URL: https://doi.org/10.1007/s40192-024-00345-7, doi:10.1007/s40192-024-00345-7. This article has 7 citations and is from a peer-reviewed journal.

3. (zhang2026towardsagenticintelligence pages 36-38): Huan Zhang, Yizhan Li, Wenhao Huang, Ziyu Hou, Yu Song, Xuye Liu, Farshid Effaty, Jinyan Jiang, Sifan Wu, Qianggang Ding, Izumi Takahara, L. MacGillivray, Teruyasu Mizoguchi, Tianshu Yu, Lizi Liao, Yuyu Luo, Yu Rong, Jia Li, Ying Diao, Heng Ji, and Bang Liu. Towards agentic intelligence for materials science. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2602.00169, doi:10.48550/arxiv.2602.00169. This article has 4 citations.

4. (zhang2026towardsagenticintelligence pages 11-13): Huan Zhang, Yizhan Li, Wenhao Huang, Ziyu Hou, Yu Song, Xuye Liu, Farshid Effaty, Jinyan Jiang, Sifan Wu, Qianggang Ding, Izumi Takahara, L. MacGillivray, Teruyasu Mizoguchi, Tianshu Yu, Lizi Liao, Yuyu Luo, Yu Rong, Jia Li, Ying Diao, Heng Ji, and Bang Liu. Towards agentic intelligence for materials science. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2602.00169, doi:10.48550/arxiv.2602.00169. This article has 4 citations.

5. (kavalsky2023byhowmuch pages 23-27): Lance Kavalsky, Vinay I. Hegde, Eric Muckley, Matthew S. Johnson, Bryce Meredig, and Venkatasubramanian Viswanathan. By how much can closed-loop frameworks accelerate computational materials discovery? Digital Discovery, 2:1112-1125, Jan 2023. URL: https://doi.org/10.1039/d2dd00133k, doi:10.1039/d2dd00133k. This article has 27 citations and is from a peer-reviewed journal.

6. (fowler2024beyondcombinatorialmaterials pages 2-4): J. Elliott Fowler, Matthew A. Kottwitz, Nat Trask, and Rémi Dingreville. Beyond combinatorial materials science: the 100 prisoners problem. Integrating Materials and Manufacturing Innovation, 13:83-91, Jan 2024. URL: https://doi.org/10.1007/s40192-023-00330-6, doi:10.1007/s40192-023-00330-6. This article has 12 citations and is from a peer-reviewed journal.

7. (bauer2024roadmapondatacentric pages 27-29): Stefan Bauer, Peter Benner, Tristan Bereau, Volker Blum, Mario Boley, Christian Carbogno, C Richard A Catlow, Gerhard Dehm, Sebastian Eibl, Ralph Ernstorfer, Ádám Fekete, Lucas Foppa, Peter Fratzl, Christoph Freysoldt, Baptiste Gault, Luca M Ghiringhelli, Sajal K Giri, Anton Gladyshev, Pawan Goyal, Jason Hattrick-Simpers, Lara Kabalan, Petr Karpov, Mohammad S Khorrami, Christoph T. Koch, Sebastian Kokott, Thomas Kosch, Igor Kowalec, Kurt Kremer, Andreas Leitherer, Yue Li, Christian H Liebscher, Andrew J Logsdail, Zhongwei Lu, Felix Luong, Andreas Marek, Florian Merz, Jaber R Mianroodi, Jörg Neugebauer, Zongrui Pei, Thomas A R Purcell, Dierk Raabe, Markus Rampp, Mariana Rossi, Jan-Michael Rost, James Saal, Ulf Saalmann, Kasturi Narasimha Sasidhar, Alaukik Saxena, Luigi Sbailò, Markus Scheidgen, Marcel Schloz, Daniel F Schmidt, Simon Teshuva, Annette Trunschke, Ye Wei, Gerhard Weikum, R Patrick Xian, Yi Yao, Junqi Yin, Meng Zhao, and Matthias Scheffler. Roadmap on data-centric materials science. Modelling and Simulation in Materials Science and Engineering, 32:063301, Jul 2024. URL: https://doi.org/10.1088/1361-651x/ad4d0d, doi:10.1088/1361-651x/ad4d0d. This article has 33 citations and is from a peer-reviewed journal.

8. (bauer2024roadmapondatacentric pages 55-58): Stefan Bauer, Peter Benner, Tristan Bereau, Volker Blum, Mario Boley, Christian Carbogno, C Richard A Catlow, Gerhard Dehm, Sebastian Eibl, Ralph Ernstorfer, Ádám Fekete, Lucas Foppa, Peter Fratzl, Christoph Freysoldt, Baptiste Gault, Luca M Ghiringhelli, Sajal K Giri, Anton Gladyshev, Pawan Goyal, Jason Hattrick-Simpers, Lara Kabalan, Petr Karpov, Mohammad S Khorrami, Christoph T. Koch, Sebastian Kokott, Thomas Kosch, Igor Kowalec, Kurt Kremer, Andreas Leitherer, Yue Li, Christian H Liebscher, Andrew J Logsdail, Zhongwei Lu, Felix Luong, Andreas Marek, Florian Merz, Jaber R Mianroodi, Jörg Neugebauer, Zongrui Pei, Thomas A R Purcell, Dierk Raabe, Markus Rampp, Mariana Rossi, Jan-Michael Rost, James Saal, Ulf Saalmann, Kasturi Narasimha Sasidhar, Alaukik Saxena, Luigi Sbailò, Markus Scheidgen, Marcel Schloz, Daniel F Schmidt, Simon Teshuva, Annette Trunschke, Ye Wei, Gerhard Weikum, R Patrick Xian, Yi Yao, Junqi Yin, Meng Zhao, and Matthias Scheffler. Roadmap on data-centric materials science. Modelling and Simulation in Materials Science and Engineering, 32:063301, Jul 2024. URL: https://doi.org/10.1088/1361-651x/ad4d0d, doi:10.1088/1361-651x/ad4d0d. This article has 33 citations and is from a peer-reviewed journal.

9. (zhang2026towardsagenticintelligence pages 4-5): Huan Zhang, Yizhan Li, Wenhao Huang, Ziyu Hou, Yu Song, Xuye Liu, Farshid Effaty, Jinyan Jiang, Sifan Wu, Qianggang Ding, Izumi Takahara, L. MacGillivray, Teruyasu Mizoguchi, Tianshu Yu, Lizi Liao, Yuyu Luo, Yu Rong, Jia Li, Ying Diao, Heng Ji, and Bang Liu. Towards agentic intelligence for materials science. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2602.00169, doi:10.48550/arxiv.2602.00169. This article has 4 citations.

10. (zhang2026towardsagenticintelligence pages 34-36): Huan Zhang, Yizhan Li, Wenhao Huang, Ziyu Hou, Yu Song, Xuye Liu, Farshid Effaty, Jinyan Jiang, Sifan Wu, Qianggang Ding, Izumi Takahara, L. MacGillivray, Teruyasu Mizoguchi, Tianshu Yu, Lizi Liao, Yuyu Luo, Yu Rong, Jia Li, Ying Diao, Heng Ji, and Bang Liu. Towards agentic intelligence for materials science. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2602.00169, doi:10.48550/arxiv.2602.00169. This article has 4 citations.

11. (boyce2024beyondfingerprintingaiguideddiscovery pages 45-49): Brad Boyce, Rémi Dingreville, David Adams, Carianne Martinez, James Fowler, Jamin Pillars, Ryan Wixom, Harry Moffat, Warren Davis, Sarah Ackerman, Ann Speed, Anthony Garland, Scott Roberts, Jonathan Coleman, Frank DelRio, Dale Cillessen, Jay Carroll, Habib Najm, John Curry, Kyle Johnson, Sarah Dudley, Sadhvikas Addamane, Amelia Henriksen, Joyce Custer, Jacqueline Wentz, Saaketh Desai, Kimberly Bassett, Troy Shilt, Elise Walker, Matias Kalaswad, Ankit Shrivastava, Tomas Babuska, Matthew Kottwitz, Kaitlynn Fitzgerald, Jonas Actor, Niladri Das, Nathan Bianco, Tylan Watkins, Kyle Dorman, Reese Jones, and Mohammad Khalil. Beyondfingerprinting: ai-guided discovery of robust materials & processes. ArXiv, Sep 2024. URL: https://doi.org/10.2172/2462990, doi:10.2172/2462990. This article has 0 citations.

12. (boyce2024beyondfingerprintingaiguideddiscovery pages 37-41): Brad Boyce, Rémi Dingreville, David Adams, Carianne Martinez, James Fowler, Jamin Pillars, Ryan Wixom, Harry Moffat, Warren Davis, Sarah Ackerman, Ann Speed, Anthony Garland, Scott Roberts, Jonathan Coleman, Frank DelRio, Dale Cillessen, Jay Carroll, Habib Najm, John Curry, Kyle Johnson, Sarah Dudley, Sadhvikas Addamane, Amelia Henriksen, Joyce Custer, Jacqueline Wentz, Saaketh Desai, Kimberly Bassett, Troy Shilt, Elise Walker, Matias Kalaswad, Ankit Shrivastava, Tomas Babuska, Matthew Kottwitz, Kaitlynn Fitzgerald, Jonas Actor, Niladri Das, Nathan Bianco, Tylan Watkins, Kyle Dorman, Reese Jones, and Mohammad Khalil. Beyondfingerprinting: ai-guided discovery of robust materials & processes. ArXiv, Sep 2024. URL: https://doi.org/10.2172/2462990, doi:10.2172/2462990. This article has 0 citations.

13. (boyce2024beyondfingerprintingaiguideddiscovery pages 94-96): Brad Boyce, Rémi Dingreville, David Adams, Carianne Martinez, James Fowler, Jamin Pillars, Ryan Wixom, Harry Moffat, Warren Davis, Sarah Ackerman, Ann Speed, Anthony Garland, Scott Roberts, Jonathan Coleman, Frank DelRio, Dale Cillessen, Jay Carroll, Habib Najm, John Curry, Kyle Johnson, Sarah Dudley, Sadhvikas Addamane, Amelia Henriksen, Joyce Custer, Jacqueline Wentz, Saaketh Desai, Kimberly Bassett, Troy Shilt, Elise Walker, Matias Kalaswad, Ankit Shrivastava, Tomas Babuska, Matthew Kottwitz, Kaitlynn Fitzgerald, Jonas Actor, Niladri Das, Nathan Bianco, Tylan Watkins, Kyle Dorman, Reese Jones, and Mohammad Khalil. Beyondfingerprinting: ai-guided discovery of robust materials & processes. ArXiv, Sep 2024. URL: https://doi.org/10.2172/2462990, doi:10.2172/2462990. This article has 0 citations.

14. (zhang2026towardsagenticintelligence pages 2-4): Huan Zhang, Yizhan Li, Wenhao Huang, Ziyu Hou, Yu Song, Xuye Liu, Farshid Effaty, Jinyan Jiang, Sifan Wu, Qianggang Ding, Izumi Takahara, L. MacGillivray, Teruyasu Mizoguchi, Tianshu Yu, Lizi Liao, Yuyu Luo, Yu Rong, Jia Li, Ying Diao, Heng Ji, and Bang Liu. Towards agentic intelligence for materials science. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2602.00169, doi:10.48550/arxiv.2602.00169. This article has 4 citations.

15. (abdelal2026criticalreviewof pages 47-48): Gasser Abdelal, Chi-Wai Chan, and Sean McLoone. Critical review of recent advances in ai-enhanced sem and eds techniques for metallic microstructure characterization. Applied Sciences, 16:975, Jan 2076. URL: https://doi.org/10.3390/app16020975, doi:10.3390/app16020975. This article has 3 citations.

16. (abdelal2026criticalreviewof pages 31-33): Gasser Abdelal, Chi-Wai Chan, and Sean McLoone. Critical review of recent advances in ai-enhanced sem and eds techniques for metallic microstructure characterization. Applied Sciences, 16:975, Jan 2076. URL: https://doi.org/10.3390/app16020975, doi:10.3390/app16020975. This article has 3 citations.

17. (abdelal2026criticalreviewof pages 36-38): Gasser Abdelal, Chi-Wai Chan, and Sean McLoone. Critical review of recent advances in ai-enhanced sem and eds techniques for metallic microstructure characterization. Applied Sciences, 16:975, Jan 2076. URL: https://doi.org/10.3390/app16020975, doi:10.3390/app16020975. This article has 3 citations.