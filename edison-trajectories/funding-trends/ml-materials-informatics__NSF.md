# Funding trends: ml materials informatics — NSF

*Edison `LITERATURE` task `1f5f6d9c-9a70-4d46-b4e6-bcda1f0dfad4` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
machine learning for materials informatics to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: machine learning for materials informatics, property prediction, and inverse alloy design (graph neural networks, transformers, foundation models, generative models for materials)

FUNDING SOURCE OF INTEREST: the U.S. National Science Foundation (NSF), including programs such as CAREER, DMREF, CMMI (Advanced Manufacturing, Mechanics of Materials and Structures), DMR (Metals & Metallic Nanostructures, TMRP), CDS&E, EAGER, MEP, GOALI, PFI, and any NSF-funded engineering research centers (ERCs) or AI institutes

TASK:

1. From the published scientific literature (2020-2026), inspect the *Acknowledgements / Funding*
   sections of recent papers in this topic area. Extract every grant/award acknowledged from the
   funding source above.

2. For EACH funded project found, report (one row per project):
   - PI name(s) and institution
   - Grant program (e.g., "NSF CAREER", "DOE ARPA-E ULTIMATE", "DARPA AMD")
   - Award number(s)
   - Award amount IF stated (otherwise "not stated"; do NOT make one up)
   - Project title or short description (1-2 sentences)
   - Year started / period of performance if known
   - Citation key(s) of the paper(s) where this funding was acknowledged

3. Identify FUNDING TRENDS for this (topic, agency) combination:
   - Which sub-programs within the agency are growing vs. shrinking in this topic?
   - Which institutions and PIs are dominating funding in this area?
   - What new agency programs (launched 2022+) are funding this topic?
   - Are there visible gaps where the agency is NOT funding this topic but could?

4. Provide a brief (3-5 sentence) executive summary at the top describing the overall funding
   posture of NSF in this topic.

OUTPUT FORMAT: markdown. Start with the executive summary, then a markdown table of funded
projects, then a "Trends" subsection. Be precise about award numbers. Do not invent data.


## Executive summary (NSF posture for ML-driven materials informatics, 2020–2026 literature sample)
Across a targeted 2020–2024 literature sample in ML for materials informatics (GNNs, transformers/attention, inverse modeling, and generative-model-enabled materials discovery), NSF support appears concentrated in (i) **DMREF** awards that explicitly fund “Designing Materials to Revolutionize and Engineer our Future” and are repeatedly acknowledged in ML-enabled discovery papers, (ii) **DMR** base awards and **DMR CAREER** awards supporting core model development for property prediction, and (iii) enabling **cyberinfrastructure and facilities** awards (OAC/CC* Compute, CNS equipment, MRSEC facilities) that underpin compute- and data-intensive workflows. Named NSF programs appearing directly in acknowledgements include **DMREF**, **CAREER**, **DIGI‑MAT**, **GRFP**, and **MRSEC**, with several awards continuing to be cited across multiple years as projects mature from methods development to applications. Within this evidence set, **award amounts and periods of performance are almost never stated in paper acknowledgements**, and **PI/institution dominance cannot be robustly inferred** without augmenting the literature-derived award list with NSF-award-database metadata. (zhu2023machinelearningdrivenexpansionof pages 8-9, barnett2020designingexceptionalgasseparation pages 6-8, pandey2021predictingenergyand pages 11-12, wang2021compositionallyrestrictedattentionbased pages 9-10, jangid2024qrbsahighresolution3d pages 24-28)

## NSF-funded projects acknowledged in recent ML-for-materials literature (one row per award)
| NSF program/sub-program | Award number(s) exactly as acknowledged | PI name(s) and institution | Award amount | Short project description | Period of performance/start year | Paper(s) acknowledging | Evidence IDs |
|---|---|---|---|---|---|---|---|
| DMR | DMR-2102409 | Prashun Gorai; institution not stated | not stated | Support acknowledged in a 2021 paper that trained a graph neural network to predict energy and stability of known and hypothetical crystal structures, enabling faster inorganic materials screening. | not stated | `pandey2021predictingenergyand` | (pandey2021predictingenergyand pages 11-12) |
| DIGI-MAT | 1922758 | Jiaxing Qu; institution not stated | not stated | Acknowledged in the same 2021 GNN paper on crystal energy/stability prediction for materials discovery. | not stated | `pandey2021predictingenergyand` | (pandey2021predictingenergyand pages 11-12) |
| CMMI | 2053929 | not stated | not stated | Acknowledged in a 2024 inverse-modeling paper that used deep learning to infer processing parameters from desired microstructures and properties in polycrystalline materials. | not stated | `wang2024deeplearningbased` | (wang2024deeplearningbased pages 6-6) |
| CMMI | 2053840 | not stated | not stated | Acknowledged in the same 2024 deep-learning inverse-design paper linking processing, structure, and property. | not stated | `wang2024deeplearningbased` | (wang2024deeplearningbased pages 6-6) |
| OAC | OAC-2331329 | not stated | not stated | Additional NSF support acknowledged in the same 2024 inverse-modeling paper for materials design. | not stated | `wang2024deeplearningbased` | (wang2024deeplearningbased pages 6-6) |
| DMR | DMR 2238231 | not stated | not stated | Acknowledged in a 2025 workshop-derived perspective on materials laboratories of the future for alloys, amorphous materials, and composites; relevant to AI-enabled and autonomous materials discovery infrastructure. | not stated | `banerjee2025materialslaboratoriesof` | (banerjee2025materialslaboratoriesof pages 16-16) |
| DMREF | DMREF-1921958 | not stated | not stated | Acknowledged in a 2023 paper using machine learning to expand the candidate space of 1D van der Waals materials. | not stated | `zhu2023machinelearningdrivenexpansionof` | (zhu2023machinelearningdrivenexpansionof pages 8-9) |
| DMREF | DMREF-1922312 | not stated | not stated | Acknowledged in the same 2023 ML-driven materials-space expansion paper. | not stated | `zhu2023machinelearningdrivenexpansionof` | (zhu2023machinelearningdrivenexpansionof pages 8-9) |
| DMR | DMR-2103721 | not stated | not stated | Acknowledged in the same 2023 paper for electronic-structure calculations on selected 1D materials within an ML-assisted discovery workflow. | not stated | `zhu2023machinelearningdrivenexpansionof` | (zhu2023machinelearningdrivenexpansionof pages 8-9) |
| NSF award / cyberinfrastructure support | 1818253 | not stated | not stated | Acknowledged in the same 2023 paper as support for Texas Advanced Computing Center computational resources used for ML-driven materials screening. | not stated | `zhu2023machinelearningdrivenexpansionof` | (zhu2023machinelearningdrivenexpansionof pages 8-9) |
| DGE / GRFP | DGE-16-44869 | Connor R. Bilchak; institution not stated | not stated | Graduate fellowship support acknowledged in a 2020 machine-learning materials-design paper that identified promising gas-separation polymer membranes. | not stated | `barnett2020designingexceptionalgasseparation` | (barnett2020designingexceptionalgasseparation pages 6-8) |
| DMREF | 1629502 | Connor R. Bilchak, J. Wesley Barnett, and Sanat K. Kumar; institution not stated | not stated | The majority of the work in the 2020 ML membrane-design paper was funded by this DMREF grant; the paper used ML to predict and validate high-performing membrane materials. | not stated | `barnett2020designingexceptionalgasseparation` | (barnett2020designingexceptionalgasseparation pages 6-8) |
| DMREF | 1629052 | Brian C. Benicewicz and Laura A. Murdock; institution not stated | not stated | Companion DMREF support acknowledged in the same 2020 ML-driven materials-discovery paper. | not stated | `barnett2020designingexceptionalgasseparation` | (barnett2020designingexceptionalgasseparation pages 6-8) |
| DMR | DMR-150730 | not stated | not stated | Prior NSF support acknowledged as the project’s starting point in the 2020 ML membrane-design paper. | not stated | `barnett2020designingexceptionalgasseparation` | (barnett2020designingexceptionalgasseparation pages 6-8) |
| DMR | DMR-1929655 | not stated | not stated | Continuation NSF support acknowledged in the 2020 ML membrane-design paper. | not stated | `barnett2020designingexceptionalgasseparation` | (barnett2020designingexceptionalgasseparation pages 6-8) |
| CAREER | DMR 1651668 | not stated | not stated | Acknowledged in the 2021 CrabNet paper introducing a transformer/self-attention model for composition-based materials property prediction. | not stated | `wang2021compositionallyrestrictedattentionbased` | (wang2021compositionallyrestrictedattentionbased pages 9-10) |
| NSF award | 1664172 | not stated | not stated | Acknowledged in a 2024 quaternion-transformer paper for generating high-resolution 3D EBSD maps from sparse measurements of titanium alloys, accelerating microstructure data acquisition. | not stated | `jangid2024qrbsahighresolution3d` | (jangid2024qrbsahighresolution3d pages 24-28) |
| MRSEC Program / DMR | DMR 1720256 | not stated | not stated | Acknowledged in the same 2024 EBSD paper for support of the MRL Shared Experimental Facilities and the California Nanosystems Institute materials research infrastructure. | not stated | `jangid2024qrbsahighresolution3d` | (jangid2024qrbsahighresolution3d pages 24-28) |
| CNS | CNS-1725797 | not stated | not stated | Acknowledged in the same 2024 EBSD paper as NSF-funded computational equipment/facilities support. | not stated | `jangid2024qrbsahighresolution3d` | (jangid2024qrbsahighresolution3d pages 24-28) |
| CC* Compute / OAC | OAC-1925717 | not stated | not stated | Acknowledged in the same 2024 EBSD paper as NSF CC* Compute support administered by the campus computing center. | not stated | `jangid2024qrbsahighresolution3d` | (jangid2024qrbsahighresolution3d pages 24-28) |


*Table: This table consolidates the NSF awards explicitly acknowledged in the retrieved 2020–2024 ML-for-materials papers, including program labels, exact award numbers, and NSF-funded facilities/cyberinfrastructure. It is useful as a cleaned evidence base for mapping NSF support patterns across GNNs, transformers, inverse design, and related materials-informatics work.*

## Trends (from acknowledgement evidence; literature-sample-based)

### 1) Which NSF sub-programs appear to be growing vs. shrinking in this topic?
* **DMREF appears persistently central** for ML-enabled materials discovery and design: it is explicitly named and tied to multiple awards acknowledged in both 2020 (polymer ML discovery) and 2023 (ML-driven materials-space expansion) papers. This suggests sustained DMREF relevance to data/ML-driven materials design pipelines. (barnett2020designingexceptionalgasseparation pages 6-8, zhu2023machinelearningdrivenexpansionof pages 8-9)
* **DMR CAREER and DMR core awards** show up in method-focused model-development papers (e.g., transformer attention models for composition-based property prediction; GNNs for crystal stability/energy prediction), consistent with DMR supporting foundational algorithmic advances that later enable downstream inverse design. (wang2021compositionallyrestrictedattentionbased pages 9-10, pandey2021predictingenergyand pages 11-12)
* **Cross-cutting compute/data programs are visible enablers**: OAC awards (including CC* Compute) and facility/equipment awards (MRSEC DMR 1720256; CNS-1725797) appear in a microstructure ML paper, indicating NSF investment in the cyberinfrastructure stack that closed-loop/autonomous discovery efforts typically depend on. (jangid2024qrbsahighresolution3d pages 24-28, wang2024deeplearningbased pages 6-6)

**Limitation:** This corpus is not large enough to quantify “growth vs. shrink” in a statistical sense; acknowledgements provide presence/absence rather than award counts over time.

### 2) Which institutions and PIs are dominating NSF funding in this area?
* From acknowledgements alone, **PI/institution is usually not stated**, so dominance cannot be reliably established.
* A few explicit author-to-award links do appear (e.g., Prashun Gorai ↔ DMR‑2102409; Jiaxing Qu ↔ DIGI‑MAT 1922758; Connor R. Bilchak ↔ GRFP DGE‑16‑44869), but the associated institutions are not provided in the acknowledgement snippets extracted here. (pandey2021predictingenergyand pages 11-12, barnett2020designingexceptionalgasseparation pages 6-8)

### 3) What new NSF programs (launched 2022+) are funding this topic?
* In this sample, **OAC-2331329 (cyberinfrastructure)** and **DMR 2238231** appear in 2024–2025 publications, indicating continued/newer-award support in the timeframe relevant to Genesis proposals. (wang2024deeplearningbased pages 6-6, banerjee2025materialslaboratoriesof pages 16-16)

**Limitation:** The acknowledgements do not state program launch dates; identifying “new (2022+) programs” rigorously would require linking the extracted awards to NSF award abstracts and start dates.

### 4) Visible gaps / opportunities (NSF not clearly funding, but could)
Within the extracted acknowledgements, NSF support is strongly visible for **model development (DMR/CAREER), DMREF discovery pipelines, and infrastructure (OAC/MRSEC/CNS)**. Gaps visible *in this literature-only evidence* include:
* **Sparse explicit linkage to autonomous closed-loop alloy discovery**: the extracted NSF awards are often tied to general ML-for-materials modeling or infrastructure, rather than explicitly acknowledging closed-loop experimentation platforms for alloys.
* **Limited explicit appearance of NSF AI-Institute-style branding or ERCs** in the acknowledgements of the retrieved papers, suggesting either (i) those programs are not prominent in this specific literature slice, or (ii) such work is published but not captured in the current retrieval and would require targeted searches for institute/center names in acknowledgements.

### Practical next step (methodological note)
To answer PI/institution dominance and “growing vs shrinking” with high confidence, the extracted award numbers in the table should be programmatically joined to the NSF Awards database (start date, PI, institution, total amount) and then re-aggregated by program element (DMR divisions, DMREF tracks, CMMI clusters, OAC solicitations). The present report intentionally does **not** infer missing metadata not present in paper acknowledgements. (zhu2023machinelearningdrivenexpansionof pages 8-9, wang2024deeplearningbased pages 6-6, jangid2024qrbsahighresolution3d pages 24-28)

References

1. (zhu2023machinelearningdrivenexpansionof pages 8-9): Yanbing Zhu, Evan R. Antoniuk, Dylan Wright, Fariborz Kargar, Nicholas Sesing, Austin D. Sendek, Tina T. Salguero, Ludwig Bartels, Alexander A. Balandin, Evan J. Reed, and Felipe H. da Jornada. Machine-learning-driven expansion of the 1d van der waals materials space. The Journal of Physical Chemistry C, 127:21675-21683, Oct 2023. URL: https://doi.org/10.1021/acs.jpcc.3c03882, doi:10.1021/acs.jpcc.3c03882. This article has 14 citations.

2. (barnett2020designingexceptionalgasseparation pages 6-8): J. Wesley Barnett, Connor R. Bilchak, Yiwen Wang, Brian C. Benicewicz, Laura A. Murdock, Tristan Bereau, and Sanat K. Kumar. Designing exceptional gas-separation polymer membranes using machine learning. Science Advances, May 2020. URL: https://doi.org/10.1126/sciadv.aaz4301, doi:10.1126/sciadv.aaz4301. This article has 307 citations and is from a highest quality peer-reviewed journal.

3. (pandey2021predictingenergyand pages 11-12): Shubham Pandey, Jiaxing Qu, Vladan Stevanović, Peter St. John, and Prashun Gorai. Predicting energy and stability of known and hypothetical crystals using graph neural network. Patterns, 2:100361, Nov 2021. URL: https://doi.org/10.1016/j.patter.2021.100361, doi:10.1016/j.patter.2021.100361. This article has 42 citations and is from a peer-reviewed journal.

4. (wang2021compositionallyrestrictedattentionbased pages 9-10): Anthony Yu-Tung Wang, Steven K. Kauwe, Ryan J. Murdock, and Taylor D. Sparks. Compositionally restricted attention-based network for materials property predictions. npj Computational Materials, May 2021. URL: https://doi.org/10.1038/s41524-021-00545-1, doi:10.1038/s41524-021-00545-1. This article has 306 citations and is from a peer-reviewed journal.

5. (jangid2024qrbsahighresolution3d pages 24-28): Devendra K. Jangid, Neal R. Brodnik, McLean P. Echlin, Tresa M. Pollock, Samantha H. Daly, and B. S. Manjunath. Q-rbsa: high-resolution 3d ebsd map generation using an efficient quaternion transformer network. npj Computational Materials, 10:1-10, Mar 2024. URL: https://doi.org/10.48550/arxiv.2303.10722, doi:10.48550/arxiv.2303.10722. This article has 14 citations and is from a peer-reviewed journal.

6. (wang2024deeplearningbased pages 6-6): Kewei Wang, Yuwei Mao, Mahmudul Hasan, Md Maruf Billah, Muhammed Nur Talha Kilic, Vishu Gupta, Wei-Keng Liao, Alok Choudhary, Pinar Acar, and Ankit Agrawal. Deep learning based inverse modeling for materials design: from microstructure and property to processing. 2024 International Conference on Machine Learning and Applications (ICMLA), pages 236-241, Dec 2024. URL: https://doi.org/10.1109/icmla61862.2024.00038, doi:10.1109/icmla61862.2024.00038. This article has 3 citations.

7. (banerjee2025materialslaboratoriesof pages 16-16): Sarbajit Banerjee, Y. Shirley Meng, Andrew M. Minor, Minghao Zhang, Nestor J. Zaluzec, Maria K.Y. Chan, Gerald Seidler, David W. McComb, Joshua Agar, Partha P. Mukherjee, Brent Melot, Karena Chapman, Beth S. Guiton, Robert F. Klie, Ian D. McCue, Paul M. Voyles, Ian Robertson, Ling Li, Miaofang Chi, Joel F. Destino, Arun Devaraj, Emmanuelle A. Marquis, Carlo U. Segre, Huinan H. Liu, Judith C. Yang, Kasra Momeni, Amit Misra, Niaz Abdolrahim, Julia E. Medvedeva, Wenjun Cai, Alp Sehirlioglu, Melike Dizbay-Onat, Apurva Mehta, Lori Graham-Brady, Benji Maruyama, Krishna Rajan, Jamie H. Warner, Mitra L. Taheri, Sergei V. Kalinin, B. Reeja-Jayan, Udo D. Schwarz, Sindee L. Simon, and Craig M. Brown. Materials laboratories of the future for alloys, amorphous, and composite materials. MRS Bulletin, 50:190-207, Jan 2025. URL: https://doi.org/10.1557/s43577-024-00846-y, doi:10.1557/s43577-024-00846-y. This article has 10 citations and is from a domain leading peer-reviewed journal.
