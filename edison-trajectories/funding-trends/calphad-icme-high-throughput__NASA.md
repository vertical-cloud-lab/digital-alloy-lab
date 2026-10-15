# Funding trends: calphad icme high throughput — NASA

*Edison `LITERATURE` task `9db566b3-8a22-4534-807b-9e37b481192c` (1 credit). Generated 2026-05-05.*

---

Question: CONTEXT: I am surveying recent (2020-2026) U.S. federal research funding trends in
CALPHAD/ICME/high-throughput alloy design to inform a DOE Genesis Mission Phase I proposal on autonomous closed-loop alloy
discovery (FLAIME). I want to identify which programs and PIs are being funded by which agencies.

TOPIC: CALPHAD thermodynamic modeling, ICME (integrated computational materials engineering), and high-throughput experimental alloy design for accelerated alloy discovery

FUNDING SOURCE OF INTEREST: the U.S. National Aeronautics and Space Administration (NASA), including STMD (Space Technology Mission Directorate), Early Career Faculty (ECF), Early Stage Innovations (ESI), SBIR/STTR, ULI, EPSCoR, and NASA center programs (Marshall, Glenn, Langley, JPL) related to additive manufacturing, advanced metallic alloys, and AI for materials

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
   posture of NASA in this topic.

OUTPUT FORMAT: markdown. Start with the executive summary, then a markdown table of funded
projects, then a "Trends" subsection. Be precise about award numbers. Do not invent data.


## Executive summary (NASA posture, 2020–2026; CALPHAD/ICME/high-throughput alloy design)
Within the retrieved 2020–2026 CALPHAD/ICME/alloy-design literature, NASA support appears primarily in three lanes: (i) **NASA EPSCoR** cooperative agreements supporting academic modeling work relevant to in-space manufacturing and solidification (80NSSC19M0149), (ii) **NASA STMD** mission-enabling technology grants (e.g., Small Spacecraft Technology) supporting additive manufacturing of advanced metallic components for spacecraft systems (80NSSC23M0234), and (iii) **NASA SMD/Biological and Physical Sciences (BPS)** funding and NASA High-End Computing resources supporting reduced-gravity/microgravity ICME studies (award number not stated). (momeni2022engineeringthesurface pages 8-9, ghosh2022aphasefieldmodel pages 23-25, oconnor2025reducedgravityanda pages 75-76, guenka2024additivemanufacturingand pages 12-17)
NASA HQ **University Leadership Initiative (ULI)** awards also appear as a mechanism supporting computational materials/alloy design connected to aerospace system needs (NNX17AJ96A). (jha2020discoveryofnew pages 11-13)
Across this limited literature sample, **award numbers are often omitted** (notably for SMD/BPS projects), which complicates PI-level mapping from papers alone and suggests that supplementing with NASA NSPIRES/award databases is necessary for a complete funding landscape. (oconnor2025reducedgravityanda pages 75-76)

## NASA-funded projects acknowledged in the literature (2020–2026)
| NASA program/subprogram | Award number(s) | PI(s) and institution | Award amount | Project title/short description | Start year/period | NASA center | Paper(s) citing acknowledgement |
|---|---|---|---|---|---|---|---|
| NASA HQ University Leadership Initiative (ULI) | NNX17AJ96A | not stated (paper authors: Rajesh Jha, Florida International University; George S. Dulikravich, Florida International University). Award managed by Texas A&M University | not stated | **Adaptive Aerostructures for Revolutionary Supersonic Transportation.** In the citing paper, the award supported CALPHAD + AI discovery of Ti-Nb-Zr-Sn biomaterial alloys to stabilize the beta phase and suppress alpha''/omega formation. | not stated | not stated | (jha2020discoveryofnew pages 11-13) |
| NASA Established Program to Stimulate Competitive Research (EPSCoR) | 80NSSC19M0149 | not stated (paper authors: Kasra Momeni, University of Alabama; Sara Neshani, University of Alabama; Chukwudalu Uba, University of Alabama; Huan Ding, University of Alabama; Jonathan Raush, University of Alabama; Shengmin Guo, University of Alabama) | not stated | NASA EPSCoR support for in-space manufacturing and alloy/phase-transformation modeling. In the citing paper, the work studied surface-melt thermodynamics and feedstock/alloying effects for additively manufactured aluminum parts for in-space manufacturing. | not stated | not stated | (momeni2022engineeringthesurface pages 8-9, momeni2022engineeringthesurface media 50b3e8ec) |
| NASA Established Program to Stimulate Competitive Research (EPSCoR) | 80NSSC19M0149 | not stated (paper authors: Manoj Ghosh, University of Alabama; Muhannad Hendy, University of Alabama; Jonathan Raush, University of Alabama; Kasra Momeni, University of Alabama) | not stated | NASA EPSCoR support for in-space manufacturing and alloy solidification modeling. In the citing paper, the work developed a phase-field model for solidification of binary alloys, tuned for Ni-Cu feedstocks, relevant to metallic in-space manufacturing. | not stated | not stated | (ghosh2022aphasefieldmodel pages 23-25) |
| NASA Science Mission Directorate (SMD), Biological and Physical Sciences (BPS) Division | not stated | not stated (paper authors: A. O'Connor; L. Littles; B. Richter; E. Glaessgen; A. Karma; institutions not stated in extracted acknowledgement) | not stated | Reduced gravity and microgravity ICME project. The citing report/paper describes ICME for alloy solidification and additive manufacturing under reduced gravity/microgravity, with CALPHAD/DFT-informed modeling and validation emphasis. | not stated | Ames Research Center (computational resources via NASA HEC / NAS Division) | (oconnor2025reducedgravityanda pages 75-76, oconnor2025reducedgravityand pages 75-76) |
| NASA Space Technology Mission Directorate (STMD), Small Spacecraft Technology (SST) program | 80NSSC23M0234 | not stated (paper authors: T. Guenka; R. Hamilton; C. Greer; S. Bilén; institutions not stated in extracted acknowledgement) | not stated | Support for additive manufacturing and experimental characterization of nickel-titanium shape-memory-alloy wick structures and heat pipes for spacecraft thermal control. The work is adjacent to high-throughput/alloy-process design through AM of advanced metallic alloys for space systems. | not stated | not stated | (guenka2024additivemanufacturingand pages 12-17, guenka2024additivemanufacturingand pages 1-12) |


*Table: This table consolidates the distinct NASA-funded projects and awards explicitly acknowledged in the retrieved 2020-2026 literature relevant to CALPHAD, ICME, and alloy/additive-manufacturing research. It is useful for tracing which NASA subprograms appear in the literature, which awards are explicit, and where award-number precision is available versus absent.*

## Trends (grounded in extracted acknowledgements)
### Sub-programs growing vs. shrinking (as visible in this corpus)
* **Visible post-2022 activity in STMD/SST:** A 2024 acknowledgement explicitly cites NASA STMD’s Small Spacecraft Technology program with an 80NSSC23* award number (80NSSC23M0234), indicating ongoing STMD technology investment tied to additively manufactured metallic hardware for spacecraft subsystems. (guenka2024additivemanufacturingand pages 12-17)
* **Sustained EPSCoR presence (2019-start award):** The same NASA EPSCoR cooperative agreement (80NSSC19M0149) is acknowledged in both 2022 and 2023 publications, consistent with multi-year, institution-centered awards that continue to generate publications. (momeni2022engineeringthesurface pages 8-9, ghosh2022aphasefieldmodel pages 23-25)
* **Program-level (not award-number-level) SMD/BPS support:** The reduced-gravity/microgravity ICME report acknowledges SMD/BPS funding and NASA HEC/NAS (Ames) computing, but provides no award identifier, making quantitative “growth vs. shrinkage” inference impossible from paper acknowledgements alone. (oconnor2025reducedgravityanda pages 75-76)

### Dominant institutions and PIs (in this extracted set)
* **University of Alabama cluster (EPSCoR 80NSSC19M0149):** Two separate papers acknowledging the same NASA EPSCoR cooperative agreement are authored by a University of Alabama team (Momeni, Raush, Guo, and collaborators), suggesting this group is a prominent NASA EPSCoR-associated publisher in in-space-manufacturing-related alloy/solidification modeling in this sample. (momeni2022engineeringthesurface pages 8-9, ghosh2022aphasefieldmodel pages 23-25)
* **Florida International University (ULI-supported paper):** A CALPHAD+AI alloy discovery study acknowledges NASA HQ ULI award NNX17AJ96A; the paper authors are at Florida International University, while the award is described as managed by Texas A&M University. (jha2020discoveryofnew pages 11-13)
* **Ames Research Center as a computational enabler:** NASA Advanced Supercomputing (NAS) via the NASA High-End Computing program at Ames is explicitly acknowledged for compute resources in the reduced-gravity/microgravity ICME study. (oconnor2025reducedgravityanda pages 75-76)

### New programs (launched 2022+) funding this topic (as visible here)
* In the extracted acknowledgements, the only clearly *recent* (post-2022) NASA award identified is the **STMD Small Spacecraft Technology (SST)** grant **80NSSC23M0234**, acknowledged in 2024. (guenka2024additivemanufacturingand pages 12-17)
* No explicit acknowledgements to NASA ECF, ESI, SBIR/STTR, or NASA center internal programs were captured in this literature set; absence here should not be interpreted as absence in NASA’s overall portfolio, only as not observed in the sampled papers. (jha2020discoveryofnew pages 11-13, guenka2024additivemanufacturingand pages 12-17)

### Gaps/opportunities suggested by the acknowledgement record
* **Award-number under-reporting:** Some NASA-supported work (e.g., SMD/BPS reduced-gravity/microgravity ICME) lacks an award identifier in the acknowledgement, limiting traceability from literature alone; encouraging standardized award citation in publications would improve portfolio analytics. (oconnor2025reducedgravityanda pages 75-76)
* **Limited visibility of “autonomous closed-loop” framing:** The acknowledged NASA projects emphasize enabling modeling (phase-field/thermodynamics) and AM component demonstrations; explicit closed-loop autonomy or high-throughput autonomous experimentation is not prominent in the mined acknowledgements, suggesting an opportunity area for proposals positioning autonomy as a multiplier for ICME/CALPHAD and AM alloy maturation. (momeni2022engineeringthesurface pages 8-9, guenka2024additivemanufacturingand pages 12-17)
* **Sparse evidence of NASA SBIR/STTR/ESI/ECF in this topic’s journal acknowledgements:** Within the retrieved corpus, NASA SBIR/STTR, Early Stage Innovations, and Early Career Faculty mechanisms did not appear in acknowledgements, which could indicate either (i) these awards are less represented in publishable CALPHAD/ICME AM literature, or (ii) they are present but not captured by this limited sample—either way, a focused search in SBIR/STTR solicitations and NASA award databases would be needed to assess the gap rigorously. (guenka2024additivemanufacturingand pages 12-17, guenka2024additivemanufacturingand pages 1-12)

References

1. (momeni2022engineeringthesurface pages 8-9): Kasra Momeni, Sara Neshani, Chukwudalu Uba, Huan Ding, Jonathan Raush, and Shengmin Guo. Engineering the surface melt for in-space manufacturing of aluminum parts. Journal of Materials Engineering and Performance, 31:6092-6100, Jun 2022. URL: https://doi.org/10.1007/s11665-022-07054-2, doi:10.1007/s11665-022-07054-2. This article has 15 citations and is from a peer-reviewed journal.

2. (ghosh2022aphasefieldmodel pages 23-25): Manoj Ghosh, Muhannad Hendy, Jonathan Raush, and Kasra Momeni. A phase-field model for in-space manufacturing of binary alloys. Materials, 16:383, Dec 2022. URL: https://doi.org/10.3390/ma16010383, doi:10.3390/ma16010383. This article has 8 citations.

3. (oconnor2025reducedgravityanda pages 75-76): A O'Connor, L Littles, B Richter, E Glaessgen, and A Karma. Reduced gravity and microgravity integrated computational materials engineering (icme). Unknown journal, 2025.

4. (guenka2024additivemanufacturingand pages 12-17): T Guenka, R Hamilton, C Greer, and S Bilén. Additive manufacturing and experimental characterization of nickel-titanium shape-memory alloy wick structures and heat pipes for spacecraft thermal control. Unknown journal, 2024.

5. (jha2020discoveryofnew pages 11-13): Rajesh Jha and George S. Dulikravich. Discovery of new ti-based alloys aimed at avoiding/minimizing formation of α” and ω-phase using calphad and artificial intelligence. Metals, 11:15, Dec 2020. URL: https://doi.org/10.3390/met11010015, doi:10.3390/met11010015. This article has 21 citations.

6. (momeni2022engineeringthesurface media 50b3e8ec): Kasra Momeni, Sara Neshani, Chukwudalu Uba, Huan Ding, Jonathan Raush, and Shengmin Guo. Engineering the surface melt for in-space manufacturing of aluminum parts. Journal of Materials Engineering and Performance, 31:6092-6100, Jun 2022. URL: https://doi.org/10.1007/s11665-022-07054-2, doi:10.1007/s11665-022-07054-2. This article has 15 citations and is from a peer-reviewed journal.

7. (oconnor2025reducedgravityand pages 75-76): A O'Connor, L Littles, B Richter, E Glaessgen, and A Karma. Reduced gravity and microgravity integrated computational materials engineering (icme). Unknown journal, 2025.

8. (guenka2024additivemanufacturingand pages 1-12): T Guenka, R Hamilton, C Greer, and S Bilén. Additive manufacturing and experimental characterization of nickel-titanium shape-memory alloy wick structures and heat pipes for spacecraft thermal control. Unknown journal, 2024.
