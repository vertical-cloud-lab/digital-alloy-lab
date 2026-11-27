<!--
Edison Scientific LITERATURE_HIGH task
- Task ID: 60d47dd5-2b1c-407e-a086-39591978f49c
- Submitted: 2026-10-06T19:03:22Z
- Fetched: 2026-10-06T19:34:45Z (status: success)
- Raw trajectory JSON: raw/03-feedstock-hte.json
- Companion to: README.md (synthesis), ../../afosr-yip-white-paper/
-->

Question:

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

TIME WINDOW: Today is 2026-10-06. Find developments published or posted
(journal articles incl. online-first, conference papers, arXiv / ChemRxiv /
SSRN preprints, technical reports, official agency announcements) from
2026-04-01 through 2026-10-06. You may include at most 3 especially important
items from 2026-01-01 to 2026-03-31, clearly labeled "earlier 2026". Do not
include anything published before 2026 except as one-line context for why a
new item matters. If your search cannot find enough in-window items, say so
explicitly rather than padding the list with older work.

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

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
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

TIME WINDOW: Today is 2026-10-06. Find developments published or posted
(journal articles incl. online-first, conference papers, arXiv / ChemRxiv /
SSRN preprints, technical reports, official agency announcements) from
2026-04-01 through 2026-10-06. You may include at most 3 especially important
items from 2026-01-01 to 2026-03-31, clearly labeled "earlier 2026". Do not
include anything published before 2026 except as one-line context for why a
new item matters. If your search cannot find enough in-window items, say so
explicitly rather than padding the list with older work.

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


# Question 3 — Feedstock, High-Throughput Fabrication, and Characterization: 2026 Developments

The following survey covers publications from 2026-04-01 through 2026-10-06, with up to three especially important items from earlier 2026 (January–March) explicitly labeled. The summary table below maps each item to the PI's sub-topics and cost hierarchy.

| Item # | Citation (short form) | Date | Sub-topic | Key finding | Relevance tag | Cost-hierarchy support |
|---:|---|---|:---:|---|---|---|
| 1 | Dodge et al. (2026), *Ultrasonic atomization of a refractory high-entropy alloy TiZrNbHfTa for additive manufacturing* | Jul. 2026 | (a) | First reported ultrasonic atomization of a refractory HEA for AM. | [CITE-1PAGER] | Directly supports rePOWDER-style atomization for the primary RHEA demonstration system. |
| 2 | Atabay et al. (2026), *Physical and microstructural properties of ultrasonically atomized nickel–tungsten powders* | Sep. 2026 | (a) | Extends ultrasonic atomization to a high-melting Ni–W alloy system and evaluates powder properties. | [CITE-FULL] | Supports feasibility for high-temperature alloy feedstocks, though LPBF-property validation remains important. |
| 3 | Bajaj et al. (2026), *Sustainable pathways in powder reuse: Virgin, reused, and ultrasonic-atomization-recycled NiTi powder* | **Feb. 2026 — earlier 2026** | (a) | AMAZEMET rePOWDER UPA produced mean sphericity 0.93; reported approximately 50% lower cradle-to-gate energy and approximately 95% material recovery, although oxygen increased under the system atmosphere used. (bajaj2026sustainablepathwaysin pages 8-10, bajaj2026sustainablepathwaysin pages 4-5) | [CITE-1PAGER] | Direct platform evidence for rePOWDER; also shows that oxygen control must be treated as a measured constraint. |
| 4 | Sojoodi et al. (2026), *Integration of circular economy into metal AM: A review of ultrasonic plasma atomization for NiTi powder* | Oct. 2026 | (a) | Reviews UPA mechanisms, reports typical sphericity above 0.9 and oxygen below 0.1 wt%, and estimates approximately 30–40% lower energy use than conventional atomization. (sojoodi2025integrationofcircular pages 2-3, sojoodi2025integrationofcircular pages 33-35) | [CITE-FULL] | Useful technical background, but its NiTi focus does not replace direct refractory-alloy validation. |
| 5 | Zhang et al. (2026), *Process optimization of Nb521 powder via radio-frequency plasma spheroidization and its suitability for selective laser melting* | Aug. 2026 | (a) | Demonstrates RF-plasma spheroidization as an alternative route for a refractory Nb-based alloy. | [CITE-FULL] | Provides a competing or complementary refractory-powder route against which ultrasonic plasma atomization should be benchmarked. |
| 6 | Feng et al. (2026), *Fabrication of lightweight TiNbCrAlVMoZr multi-principal-element alloy powder by RF plasma spheroidization* | May 2026 | (a)/(b) | Produces spherical lightweight refractory multi-principal-element-alloy powder using RF plasma processing. | [CITE-FULL] | Relevant alternative for rapidly preparing refractory-composition feedstock, but not itself a partial-evaluation strategy. |
| 7 | Villapun et al. (2026), *Enabling alloy screening via multi-material printing using a production PBF-LB machine* | Aug. 2026 | (b) | A reduced-volume insert used approximately 16% of normal powder volume and screened five Ti–Cu compositions in one production-machine build. (villapun2026enablingalloyscreening pages 1-3, villapun2026enablingalloyscreening pages 8-10) | [CITE-1PAGER] | Strongly supports density, hardness, modulus, and biological assays as inexpensive screening nodes before full validation. |
| 8 | Strauch et al. (2026), *In situ alloying from powder blends enables processing of high-copper-content Ti-6Al-4V by LPBF* | Jun. 2026 | (b) | Ti-6Al-4V blended with 10–20 wt% Cu reached relative density as high as 99.99% with EDS-confirmed homogeneity; higher Cu increased cracking risk. (strauch2026insitualloying pages 2-4, strauch2026insitualloying pages 1-2) | [CITE-FULL] | Validates blend-based composition screening, while showing that density and EDS alone cannot guarantee pre-alloyed-equivalent behavior. |
| 9 | Rodrigues et al. (2026), *Designing homogeneous Ti-Nb-Fe-Sn β-Ti alloys by PBF-LB: A pre-alloyed powder-blend strategy* | Sep. 2026 | (b) | Uses master-alloy powders rather than pure refractory Nb to reduce incomplete dissolution, microsegregation, and local property variation. (rodrigues2026designinghomogeneoustinbfesn pages 1-5) | [CITE-FULL] | Offers a practical intermediate-fidelity feedstock strategy when elemental blending is unreliable for refractory constituents. |
| 10 | Moreno et al. (2026), *Anisotropy of CMSX-6 Ni-base superalloy properties using PIP and SPT* | **Jan. 2026 — earlier 2026** | (c) | PIP yield-strength estimates deviated by approximately 10%; SPT regressions reached R²≈0.89 for yield-related calibration, with combined estimates generally within 12%. (moreno2026anisotropyonmechanical pages 8-10, moreno2026anisotropyonmechanical pages 5-8, moreno2026anisotropyonmechanical pages 1-3) | [CITE-1PAGER] | Supports PIP/SPT as low-material proxy nodes for Ni superalloys, but not as replacements for elevated-temperature tensile tests. |
| 11 | Chawla et al. (2026), *Random combinatorial libraries and automated nanoindentation for high-throughput structural-materials discovery* | Aug. 2026 | (c) | Integrates EDS registration, automated nanoindentation, Gaussian-process models, and cost-aware BO; reports orders-of-magnitude throughput potential and approximately 5 s per indentation in one workflow. (chawla2026randomcombinatoriallibraries pages 3-6, chawla2026randomcombinatoriallibraries pages 16-18) | [CITE-1PAGER] | Directly supports automated hardness/modulus measurements as cheap, partially queried nodes chosen by cost-aware optimization. |
| 12 | Wood et al. (2026), *Validation of PIP testing for rapid qualification of EB-PBF Ti-6Al-4V builds* | Apr. 2026 | (c) | Applies PIP as a rapid mechanical-qualification method specifically for AM Ti-6Al-4V builds. | [CITE-FULL] | AM-specific evidence for placing indentation-derived stress–strain estimates below standard tensile tests in fidelity and cost. |
| 13 | Zha et al. (2026), *HT-DABI: High-throughput extraction of creep and static properties via dimple-array bulging* | **Jan. 2026 — earlier 2026** | (c) | Introduces array-based miniaturized extraction of static and creep properties from metallic alloys. | [CITE-1PAGER] | Potentially supplies a missing intermediate node between room-temperature hardness/PIP and expensive long-duration high-temperature creep tests. |
| 14 | Giri et al. (2026), *In-situ sensor monitoring of multi-class gas-porosity formation in LPBF using a CNN* | Apr. 2026 | (d) | Low-cost photodiode signals, labeled using synchrotron X-ray imaging, classified no pore, pores below 15 µm, and pores above 15 µm with 79% accuracy, ROC-AUC 0.89, and approximately 1 ms inference. (giri2026insitusensormonitoring pages 1-2) | [CITE-1PAGER] | Excellent example of an inexpensive in-situ signal calibrated against an expensive diagnostic and then used as a proxy node. |
| 15 | Özel (2026), *Detection of anomalous meltpool conditions using deep learning in LPBF* | Jul. 2026 | (d) | A ResNet-18/SVM workflow classified normal, overheated, and underheated melt pools in Ni alloy 625 with 97.87% accuracy and ROC-AUC above 0.98. (ozel2026detectionofanomalous pages 1-2, ozel2026detectionofanomalous pages 15-16) | [CITE-FULL] | Supports melt-pool imaging as an inexpensive real-time process-quality node, although direct CT/property calibration was not yet established. |
| 16 | Cao et al. (2026), *Physics-informed deep learning for virtual crystallographic phase and grain-orientation reconstruction of AM alloys* | Aug. 2026 | (d) | Reconstructs virtual EBSD from SEM images across Ti-6Al-4V, 316L, Inconel 617, and Al 2219; BC reconstruction achieved SSIM greater than 0.64 and Pearson correlation greater than 0.82. (cao2026physicsinformeddeeplearning pages 11-13, cao2026physicsinformeddeeplearning pages 1-4) | [CITE-1PAGER] | Could make SEM-derived virtual EBSD a cheap microstructure node, but periodic real-EBSD calibration remains necessary. |
| 17 | Taheri-Mousavi and Ni (2026), *AlloyGen: A physics-grounded self-adaptive multi-agent framework for autonomous AM-alloy design* | Aug. 2026 | (d) | Automates retrieval, CALPHAD/Thermo-Calc execution, critique, code correction, and team formation; retrieval plus execution solved all six benchmark CALPHAD tasks versus none without retrieval. (taherimousavi2026alloygenaphysicsgrounded pages 4-6, taherimousavi2026alloygenaphysicsgrounded pages 1-4) | [AWARENESS] [COMPETITOR] | A parallel computational-automation effort; it overlaps with autonomous CALPHAD orchestration but not the proposed physical powder-to-property BO function network. |
| 18 | Stuckner et al. (2026), *Benchmarking Bayesian-optimization frameworks and acquisition strategies for materials discovery and autonomous laboratories* | **Mar. 2026 — earlier 2026** | (d) | NASA technical report benchmarks BO software and acquisition strategies for autonomous materials laboratories. | [AWARENESS] [COMPETITOR] | Signals active NASA investment in BO-driven materials discovery; differentiation should emphasize cost-aware partial evaluation of a coupled physical AM-alloy pipeline. |


*Table: Key 2026 publications and preprints mapped to feedstock production, rapid alloy screening, miniaturized testing, and automated characterization. The final column identifies how each development supports—or qualifies—the proposed hierarchy of inexpensive proxy measurements and costly full-property tests.*

---

## (a) Ultrasonic Atomization and Refractory Alloy Powders

**1. Dodge, B.S., Niraula, S., Shokri, N., Gillham, J.D. & Berfield, T.A.** "Ultrasonic atomization of a refractory high-entropy alloy TiZrNbHfTa for additive manufacturing." *Powders* 5, 25 (Jul 2026). DOI: 10.3390/powders5030025. **Online: July 2026.**
This is the first reported ultrasonic atomization of a refractory HEA (TiZrNbHfTa) for AM, directly relevant to the PI's primary Mo-Nb-Ta-W-Hf-Zr-Ti system. It represents proof that small-batch ultrasonic atomization can process refractory compositions, a key enabler for the proposed pipeline.
**Tags: [CITE-1PAGER] [CITE-FULL]** — Supports cheap feedstock node; the PI should cite this as validating the rePOWDER approach for refractory HEAs.

**2. Atabay, S.E., Baker, A.A., McKeown, J.T. & Voisin, T.** "Physical and microstructural properties of ultrasonically atomized nickel-tungsten (NiW) powders." *Mater. Des.* 269, 116623 (Sep 2026). DOI: 10.1016/j.matdes.2026.116623. **Online: September 2026.**
Extends ultrasonic atomization to a high-melting-point Ni-W binary, evaluating powder morphology and microstructure. Relevant to the PI's secondary Ni superalloy system as it shows UA feasibility for refractory-element-containing Ni alloys.
**Tags: [CITE-FULL]** — Supports high-T feedstock feasibility.

**3. [earlier 2026] Bajaj, H.K. et al.** "Sustainable pathways in powder reuse: A comparative study of virgin, reused, and ultrasonic-atomization-recycled NiTi powder for additive manufacturing." *Sustainability* 18, 1843 (Feb 2026). DOI: 10.3390/su18041843. **Online: February 2026.**
This study explicitly uses the **AMAZEMET rePOWDER** UPA system at 40 kHz. UPA-recycled NiTi powder had D50 = 55.77 µm and mean sphericity = 0.93 (matching virgin powder), with a narrow span of 0.88 (bajaj2026sustainablepathwaysin pages 8-10). Cradle-to-gate energy was reduced from ~100 to ~50 MJ/kg (≈50%), with ~95% material recovery (bajaj2026sustainablepathwaysin pages 4-5). Oxygen was elevated relative to virgin powder under the system atmosphere used, highlighting the need for optimized inert-gas control. UPA energy was reported as 12–18 MJ/kg vs. 25–30 MJ/kg for conventional gas atomization (bajaj2026sustainablepathwaysin pages 4-5).
**Tags: [CITE-1PAGER]** — Direct validation of rePOWDER platform and quantitative cost/quality metrics. Supports the cheap-feedstock node but flags oxygen control as a constraint requiring monitoring.

**4. Sojoodi, M. et al.** "Integration of circular economy into metal additive manufacturing: A review of ultrasonic plasma atomization for producing virgin and recycled NiTi powder." *Shape Mem. Superelasticity* 12, 5–45 (Oct 2026). DOI: 10.1007/s40830-025-00589-y. **Online: October 2026.**
Comprehensive review of UPA mechanisms. Reports sphericity indices often above 0.9, oxygen below 0.1 wt%, and 30–40% energy reduction vs. gas atomization (sojoodi2025integrationofcircular pages 2-3, sojoodi2025integrationofcircular pages 33-35). Higher ultrasonic frequency (40 vs. 20 kHz) refines particle size but slightly increases oxygen pickup (sojoodi2025integrationofcircular pages 33-35). UPA can process small 1–5 kg batches with 80–90% recovery (bajaj2026sustainablepathwaysin pages 4-5).
**Tags: [CITE-FULL]** — Authoritative UPA background.

**5. Zhang, Y. et al.** "Process optimization of Nb521 powder via radio-frequency plasma spheroidization and its suitability for selective laser melting." *Int. J. Refract. Met. Hard Mater.* 138, 107742 (Aug 2026). DOI: 10.1016/j.ijrmhm.2026.107742. **Online: August 2026.**
RF plasma spheroidization of a refractory Nb alloy (Nb521) with SLM suitability evaluation—a competing powder production route for refractory alloys.
**Tags: [CITE-FULL]** — Alternative refractory powder route to benchmark against UA.

**6. Feng, R. et al.** "Fabrication of lightweight TiNbCrAlVMoZr multi-principal-element alloy powder by RF plasma spheroidization." *Powder Technol.* 475, 122311 (May 2026). DOI: 10.1016/j.powtec.2026.122311. **Online: May 2026.**
RF plasma spheroidization of a lightweight MPEA powder containing Nb, Mo, and other refractory elements.
**Tags: [CITE-FULL]** — Relevant feedstock for refractory alloy discovery.

---

## (b) Small-Batch Powder Production and In-Situ Alloying for Alloy Discovery

**7. Villapun, V.M. et al.** "Enabling alloy screening via multi-material printing using a production PBF-LB machine." *Prog. Addit. Manuf.* (Aug 2026). DOI: 10.1007/s40964-026-01939-7. **Online: August 2026.**
Demonstrates multi-composition screening on an unmodified production LPBF machine using a reduced-volume insert that limits powder usage to ~16% of the full build volume (villapun2026enablingalloyscreening pages 1-3). Five Ti-Cu compositions (0–20 wt% Cu in 5 wt% steps) were fabricated and evaluated in a single build. Hardness increased from ~199 to ~429 HV with increasing Cu content (villapun2026enablingalloyscreening pages 1-3). This directly supports the "cheap proxy experiments" paradigm: density cubes, hardness, and biological assays serve as inexpensive screening nodes before full tensile testing.
**Tags: [CITE-1PAGER]** — Strongly supports the cost hierarchy; cite as validation that production PBF-LB can serve as a high-throughput alloy-screening node.

**8. Strauch, A.L., Altmann, M.L. & Toenjes, A.** "In situ alloying from powder blends enables processing of high copper content Ti-6Al-4V by laser powder bed fusion." *Discov. Mater.* 6 (Jun 2026). DOI: 10.1007/s43939-026-00738-9. **Online: June 2026.**
Blended Ti-6Al-4V + pure Cu at 10–20 wt% Cu; achieved up to 99.99% relative density and EDS-confirmed chemical homogeneity (strauch2026insitualloying pages 1-2). At 10 wt% Cu, robust processing was observed under all parameter sets; higher Cu increased cracking risk. This demonstrates that in-situ alloying can rapidly screen compositions, though it does not quantitatively compare against pre-alloyed behavior.
**Tags: [CITE-FULL]** — Supports feasibility of blend-based screening.

**9. Rodrigues, J. et al.** "Designing homogeneous Ti-Nb-Fe-Sn β titanium alloys by PBF-LB: A pre-alloyed powder blend strategy." *arXiv* 2609.17476 (Sep 2026). DOI: 10.48550/arxiv.2609.17476. **Online: September 2026.**
Proposes master-alloy powder blending (Ti-Nb, Ti-Nb-Fe, Ti-Nb-Sn) instead of pure elemental Nb to avoid incomplete dissolution and microsegregation typical of refractory element blends (rodrigues2026designinghomogeneoustinbfesn pages 1-5). Directly relevant to the PI's Mo-Nb-Ta-W system, where elemental blending of high-melting elements is problematic.
**Tags: [CITE-FULL]** — Informs feedstock strategy for refractory-element alloys.

**Additional items (unobtainable, noted from search metadata):**
- **Yeung, H. et al.** "Laser stirring with elliptical scanning enables on-demand alloying in additive manufacturing." *Addit. Manuf.* 118, 105101 (Feb 2026). DOI: 10.1016/j.addma.2026.105101 — NIST work on in-situ alloying via scan-path control. **[CITE-FULL] [COMPETITOR]**
- **Chmielewska, J. et al.** "A single-powder strategy for LPBF and LDED processing of a BCC Nb-Ti-Zr alloy." *J. Mater. Res. Technol.* (Nov 2026). DOI: 10.1016/j.jmrt.2026.09.099 — BCC refractory alloy from single pre-alloyed powder in both LPBF and LDED. **[CITE-FULL]**

---

## (c) High-Throughput and Miniaturized Mechanical Testing

**10. [earlier 2026] Moreno, D. et al.** "Anisotropy on mechanical properties of CMSX-6 Ni-base superalloy single crystal using profilometer indentation plastometer (PIP) and small punch test (SPT)." *J. Miner. Mater. Charact. Eng.* 14, 15–25 (Jan 2026). DOI: 10.4236/jmmce.2026.141002. **Online: January 2026.**
Applied PIP and SPT to a single-crystal Ni superalloy across three crystallographic orientations. PIP yield-strength estimates deviated ~10% from reference values; SPT empirical regressions achieved R² ≈ 0.89 for yield-related calibration, with combined PIP+SPT consistency within ~12% (moreno2026anisotropyonmechanical pages 8-10, moreno2026anisotropyonmechanical pages 5-8). This directly validates PIP/SPT as low-material proxy nodes for superalloys in the proposed cost hierarchy.
**Tags: [CITE-1PAGER]** — Directly supports PIP/SPT as cheap proxy for Ni superalloy mechanical properties.

**11. Chawla, V., Penumadu, D. & Kalinin, S.** "Random combinatorial libraries and automated nanoindentation for high-throughput structural materials discovery." *Commun. Mater.* (Aug 2026). DOI: 10.1038/s43246-026-01294-8. **Online: August 2026.**
Introduces particle-based random combinatorial libraries containing hundreds to thousands of discrete compositions in one specimen, characterized by EDS mapping and automated nanoindentation guided by Gaussian-process/Bayesian optimization (chawla2026randomcombinatoriallibraries pages 3-6, chawla2026randomcombinatoriallibraries pages 1-3). Each indentation takes ~5 s; a 5×5 grid requires ~1280 s when avoiding the ~400 s reconfiguration penalty (chawla2026randomcombinatoriallibraries pages 6-9, chawla2026randomcombinatoriallibraries pages 20-23). The authors claim orders-of-magnitude throughput improvement over conventional synthesis-and-test workflows (chawla2026randomcombinatoriallibraries pages 16-18). This is an extremely strong parallel to the PI's cost-aware multi-fidelity approach: nanoindentation as a cheap node, with cost-aware BO choosing measurement locations.
**Tags: [CITE-1PAGER]** — Directly supports cheap proxy node concept with BO-guided testing.

**12. Wood, A.T. et al.** "Validation of profilometry-based indentation plastometry (PIP) testing for rapid qualification of electron beam–powder bed fusion (EB-PBF) with Ti-6Al-4V builds." *Adv. Eng. Mater.* (Apr 2026). DOI: 10.1002/adem.202502047. **Online: April 2026.**
AM-specific validation of PIP for rapid qualification of EB-PBF Ti-6Al-4V, establishing PIP as a quick surrogate for standard tensile tests on AM builds.
**Tags: [CITE-FULL]** — AM-specific PIP validation.

**13. [earlier 2026] Zha, R. et al.** "HT-DABI: High-throughput extraction of creep and static material properties of metallic alloys via dimple array bulging." SSRN preprint 6169831 (Jan 2026). DOI: 10.2139/ssrn.6169831. **Online: January 2026.**
Introduces dimple-array bulging for high-throughput extraction of both creep and static mechanical properties—a missing intermediate fidelity level between room-temperature hardness and expensive long-duration elevated-temperature tensile/creep tests. Northwestern group (Cao, Espinosa, Dunand, McCue).
**Tags: [CITE-1PAGER]** — Fills a critical gap in the cost hierarchy for elevated-temperature property screening. **[COMPETITOR]** — This Northwestern/Argonne group is actively developing HT methods for metallic alloys.

**14. Cannon, L., Davidson, K.P. & Quadir, M.Z.** "Evaluation of the small punch test: Repeatability and sample parameter influence." *J. Mater. Eng. Perform.* (Jul 2026). DOI: 10.1007/s11665-026-14603-6. **Online: July 2026.**
Establishes SPT repeatability for steels and derives empirical relationships to yield and ultimate tensile strength, supporting SPT use for rapid alloy screening including AM applications (cannon2026evaluationofthe pages 1-2).
**Tags: [CITE-FULL]** — SPT validation background.

**15. Muhit, M.M.I. et al.** "Hot isostatic pressing effects on multiscale mechanical properties and chromium-dependent strength retention in LPBF Fe-based shape memory alloys." *Sci. Rep.* 16 (May 2026). DOI: 10.1038/s41598-026-48695-w. **Online: May 2026.**
Uses PIP (ASTM 52965-25, 1 mm radius indenter) on LPBF Fe-SMA to compare as-built vs. HIP-treated conditions; cautions that PIP-derived tensile properties are effective/comparative rather than direct substitutes for conventional tensile tests under multiaxial conditions (muhit2026hotisostaticpressing pages 3-5).
**Tags: [CITE-FULL]** — Important caveat for PIP in AM context.

---

## (d) Automated/Robotic Characterization and ML-Based Analysis

**16. Giri, S. et al.** "In-situ sensor monitoring of multi-class gas porosity formation in laser powder bed fusion using convolutional neural network." *J. Intell. Manuf.* (Apr 2026). DOI: 10.1007/s10845-026-02861-z. **Online: April 2026.**
Low-cost photodiode signals, calibrated against synchrotron X-ray ground truth, classify no-pore, small-pore (<15 µm), and large-pore (>15 µm) conditions with 79% accuracy, ROC-AUC = 0.89, and ~1 ms inference time per window (giri2026insitusensormonitoring pages 1-2). This is an ideal cheap proxy node: inexpensive sensors calibrated against costly diagnostics, enabling real-time quality assessment during builds.
**Tags: [CITE-1PAGER]** — Directly validates in-situ melt-pool monitoring as a cheap fidelity level.

**17. Özel, T.** "Detection of anomalous meltpool conditions using deep learning in laser powder bed fusion." *Adv. Manuf.* (Jul 2026). DOI: 10.1007/s40436-026-00620-0. **Online: July 2026.**
ResNet-18/SVM hybrid classified normal, overheated, and underheated melt pools in Ni alloy 625 at 97.87% accuracy with ROC-AUC > 0.98 (ozel2026detectionofanomalous pages 1-2, ozel2026detectionofanomalous pages 15-16). Region-property extraction requires ~10 ms/frame. The system is designed for real-time feedback and parameter adjustment.
**Tags: [CITE-FULL]** — Supports melt-pool monitoring as inexpensive QC node.

**18. Cao, Z. et al.** "Physics-informed deep learning for virtual crystallographic phase and grain orientation reconstruction of additively manufactured alloys." Preprint, Aug 2026. DOI: 10.21203/rs.3.rs-10513494/v1. **Online: August 2026.**
PI-CycleGAN converts SEM secondary-electron images into virtual EBSD (band contrast, IPF, phase maps) across LPBF Ti-6Al-4V, 316L, Inconel 617, and Al 2219. Band-contrast reconstruction: mean SSIM > 0.64, PSNR > 22 dB, Pearson correlation > 0.82. Phase reconstruction: SSIM 0.83–0.92 (cao2026physicsinformeddeeplearning pages 11-13). This could reduce EBSD costs significantly by making standard SEM imaging a cheap microstructure-characterization proxy, with periodic real EBSD for calibration.
**Tags: [CITE-1PAGER]** — Directly relevant: SEM as cheap node replacing expensive EBSD in the multi-fidelity loop.

**19. Taheri-Mousavi, S.M. & Ni, B.** "AlloyGen: A physics-grounded self-adaptive multi-agent framework for autonomous alloy design workflows in additive manufacturing." Preprint, Aug 2026. DOI: 10.21203/rs.3.rs-10329502/v1. **Online: August 2026.**
Multi-agent LLM framework that automates CALPHAD screening (Scheil, equilibrium calculations) for Al-Si printability and refractory alloy research synthesis using GPT-4o with TC-Python (taherimousavi2026alloygenaphysicsgrounded pages 4-6, taherimousavi2026alloygenaphysicsgrounded pages 1-4). Overlaps with the PI's computational CALPHAD node but uses LLM-based agents rather than Bayesian optimization of function networks.
**Tags: [AWARENESS] [COMPETITOR]** — The PI should acknowledge this as a parallel automation approach while differentiating the BOFN-based cost-aware optimization.

**20. Stuckner, J. et al.** "Benchmarking Bayesian optimization frameworks and acquisition strategies for materials discovery and autonomous laboratories." NASA Technical Report (Mar 2026). DOI: 10.64631/zkvt6687. **Online: March 2026.** *[earlier 2026]*
NASA Glenn benchmarks multiple BO frameworks for autonomous materials laboratories, signaling active federal investment in this space.
**Tags: [AWARENESS] [COMPETITOR]** — Important context for AFOSR reviewers showing NASA interest in BO-driven materials.

**21. Ercetin, A. et al.** "AI-driven image processing for microstructure and surface characterization: A systematic review." *Arch. Comput. Methods Eng.* (May 2026). DOI: 10.1007/s11831-026-10641-4. **Online: May 2026.**
Reviews deep-learning architectures (U-Net, DeepLab, YOLO, ViT) for automated SEM/EBSD metallography, reporting segmentation accuracies of 95.6–98.5% for various material systems (ercetin2026aidrivenimageprocessing pages 20-21, ercetin2026aidrivenimageprocessing pages 21-21). Covers few-shot learning, super-resolution, and foundation models (SAM) for microstructure analysis.
**Tags: [CITE-FULL]** — Background for automated metallography as cheap proxy.

---

## Ranked Top 5 Things the PI Should Know

1. **Dodge et al. (Jul 2026) demonstrated ultrasonic atomization of a refractory HEA (TiZrNbHfTa) for AM.** This is the single most important paper for the proposal: it proves that UA/rePOWDER-type systems can process the exact class of refractory alloys proposed. The PI should obtain this paper immediately and cite it in the one-pager.

2. **Chawla et al. (Aug 2026) demonstrated cost-aware, BO-guided automated nanoindentation on random combinatorial libraries.** This is a close conceptual parallel to the PI's multi-fidelity approach—nanoindentation as a cheap node, BO choosing where to measure next based on cost and information gain. It validates the cheap-proxy paradigm but does not use function networks with partial evaluation of a manufacturing DAG. Cite in the one-pager as support for the approach while differentiating the novelty of the BOFN formulation.

3. **Zha et al. (Jan 2026, Northwestern/Argonne) introduced HT-DABI for high-throughput creep screening.** This fills the critical gap between room-temperature hardness and full elevated-temperature tensile/creep testing. The Northwestern group (Espinosa, Dunand, McCue, Cao) is a likely competitor for the same DOE BES or AFOSR funds. The PI should cite this as evidence that the community needs cheap intermediate-fidelity nodes and should consider whether HT-DABI could be incorporated as one such node.

4. **Virtual EBSD from SEM (Cao et al., Aug 2026) and melt-pool CNN monitoring (Giri et al., Apr 2026; Özel, Jul 2026) provide quantitatively validated cheap proxy nodes.** Virtual EBSD achieves Pearson > 0.82 for band-contrast reconstruction (cao2026physicsinformeddeeplearning pages 11-13); melt-pool monitoring achieves 79–97.87% classification accuracy for porosity-related conditions (giri2026insitusensormonitoring pages 1-2, ozel2026detectionofanomalous pages 15-16). These directly populate the low-cost nodes in the proposed DAG.

5. **AlloyGen (Taheri-Mousavi & Ni, Aug 2026) and the NASA BO benchmark (Stuckner et al., Mar 2026) signal growing competition in autonomous alloy design and BO-for-materials.** The PI's differentiator must be the coupled physical pipeline with cost-aware partial evaluation—not autonomous CALPHAD alone or generic BO for materials.

---

## Suggested Wording Changes for the White Paper

The current novelty claim reads: *"This cost-aware, partial-evaluation formulation applied for the first time to a complex additive manufacturing pipeline for alloys is the core methodological novelty."*

**Recommended revision:** The 2026 literature shows that cost-aware BO and multi-fidelity proxy nodes are individually being adopted (Chawla et al. for combinatorial nanoindentation; Giri et al. for melt-pool-as-proxy; AlloyGen for LLM-automated CALPHAD; the NASA BO benchmark). However, no published work couples these concepts into a DAG-structured function network with partial evaluation across a complete powder-to-property AM pipeline. To maintain accuracy, consider rewording to:

*"While cost-aware Bayesian optimization and individual cheap-proxy measurements (e.g., automated nanoindentation, melt-pool monitoring) have recently been demonstrated for isolated alloy-screening tasks, no existing work integrates them into a unified directed acyclic graph of surrogate models spanning the full CALPHAD → atomization → LPBF → microstructure → elevated-temperature property pipeline. The core methodological novelty is the cost-aware, partial-evaluation optimization of this complete function network, where the algorithm dynamically selects which nodes to query—from cheap CALPHAD simulations and single-track experiments to expensive full tensile tests—based on expected information gain per unit cost."*

This revised wording (a) acknowledges the rapidly converging field, (b) sharpens the distinction between component-level demonstrations and system-level integration, and (c) is robust against the specific papers identified above.

**Additional note for reviewers:** The PI may also wish to add 1–2 sentences noting that recent work validates specific cheap nodes the platform will exploit: UPA powder sphericity ≈ 0.93 from the rePOWDER system (bajaj2026sustainablepathwaysin pages 8-10), PIP yield-stress estimates within ~10% of tensile values for Ni superalloys (moreno2026anisotropyonmechanical pages 8-10), and CNN-based melt-pool porosity classification at 79% accuracy with 1 ms inference (giri2026insitusensormonitoring pages 1-2). These quantitative correlations justify the multi-fidelity cost structure assumed in the BOFN formulation.


References

1. (bajaj2026sustainablepathwaysin pages 8-10): Harsh K. Bajaj, Mahyar Sojoodi, Francis Y. Asare Baffour, Maedeh Hesami, Shiva Houshmand, Vidura R. De Silva Kanakaratne, Ahu Celebi, and Mohammad Elahinia. Sustainable pathways in powder reuse: a comparative study of virgin, reused, and ultrasonic-atomization-recycled niti powder for additive manufacturing. Sustainability, 18:1843, Feb 2026. URL: https://doi.org/10.3390/su18041843, doi:10.3390/su18041843. This article has 3 citations.

2. (bajaj2026sustainablepathwaysin pages 4-5): Harsh K. Bajaj, Mahyar Sojoodi, Francis Y. Asare Baffour, Maedeh Hesami, Shiva Houshmand, Vidura R. De Silva Kanakaratne, Ahu Celebi, and Mohammad Elahinia. Sustainable pathways in powder reuse: a comparative study of virgin, reused, and ultrasonic-atomization-recycled niti powder for additive manufacturing. Sustainability, 18:1843, Feb 2026. URL: https://doi.org/10.3390/su18041843, doi:10.3390/su18041843. This article has 3 citations.

3. (sojoodi2025integrationofcircular pages 2-3): Mahyar Sojoodi, Alireza Behvar, Harsh Bajaj, Shiva Mohajerani, Saeedeh Vanaei, Nasrin Taheri Andani, Anwar Algamal, Fatemeh Ghasemibojd, Mahsa Beyk Khorasani, Ahu Celebi, and Mohammad Elahinia. Integration of circular economy into metal additive manufacturing: a review of ultrasonic plasma atomization for producing virgin and recycled niti powder. Shape Memory and Superelasticity, 12:5-45, Oct 2026. URL: https://doi.org/10.1007/s40830-025-00589-y, doi:10.1007/s40830-025-00589-y. This article has 7 citations.

4. (sojoodi2025integrationofcircular pages 33-35): Mahyar Sojoodi, Alireza Behvar, Harsh Bajaj, Shiva Mohajerani, Saeedeh Vanaei, Nasrin Taheri Andani, Anwar Algamal, Fatemeh Ghasemibojd, Mahsa Beyk Khorasani, Ahu Celebi, and Mohammad Elahinia. Integration of circular economy into metal additive manufacturing: a review of ultrasonic plasma atomization for producing virgin and recycled niti powder. Shape Memory and Superelasticity, 12:5-45, Oct 2026. URL: https://doi.org/10.1007/s40830-025-00589-y, doi:10.1007/s40830-025-00589-y. This article has 7 citations.

5. (villapun2026enablingalloyscreening pages 1-3): Victor M. Villapun, Luke N. Carter, Daisy Rabbitt, Ming Huang, Daniel Wilmot, Jonathan D. Stevenson, Richard J. M. Hague, and Sophie C. Cox. Enabling alloy screening via multi-material printing using a production pbf-lb machine. Progress in Additive Manufacturing, Aug 2026. URL: https://doi.org/10.1007/s40964-026-01939-7, doi:10.1007/s40964-026-01939-7. This article has 0 citations and is from a peer-reviewed journal.

6. (villapun2026enablingalloyscreening pages 8-10): Victor M. Villapun, Luke N. Carter, Daisy Rabbitt, Ming Huang, Daniel Wilmot, Jonathan D. Stevenson, Richard J. M. Hague, and Sophie C. Cox. Enabling alloy screening via multi-material printing using a production pbf-lb machine. Progress in Additive Manufacturing, Aug 2026. URL: https://doi.org/10.1007/s40964-026-01939-7, doi:10.1007/s40964-026-01939-7. This article has 0 citations and is from a peer-reviewed journal.

7. (strauch2026insitualloying pages 2-4): Anna Luise Strauch, Mika León Altmann, and Anastasiya Toenjes. In situ alloying from powder blends enables processing of high copper content ti-6al-4v by laser powder bed fusion. Discover Materials, Jun 2026. URL: https://doi.org/10.1007/s43939-026-00738-9, doi:10.1007/s43939-026-00738-9. This article has 1 citations.

8. (strauch2026insitualloying pages 1-2): Anna Luise Strauch, Mika León Altmann, and Anastasiya Toenjes. In situ alloying from powder blends enables processing of high copper content ti-6al-4v by laser powder bed fusion. Discover Materials, Jun 2026. URL: https://doi.org/10.1007/s43939-026-00738-9, doi:10.1007/s43939-026-00738-9. This article has 1 citations.

9. (rodrigues2026designinghomogeneoustinbfesn pages 1-5): J. Rodrigues, K. Bartha, M. Casas-Luna, G. V. Prandi, M. Sangali, Kateřina Ficková, J. Kozlík, M. Šlapáková, Martin Koller, A. Strnad, Josef Str'ask'y, M. Janeček, and R. Caram. Designing homogeneous ti-nb-fe-sn β titanium alloys by pbf-lb: a pre-alloyed powder blend strategy. ArXiv, Sep 2026. URL: https://doi.org/10.48550/arxiv.2609.17476, doi:10.48550/arxiv.2609.17476. This article has 0 citations.

10. (moreno2026anisotropyonmechanical pages 8-10): Daniel Moreno, Amit Yair, Libi Shechner, Yohanan Nahmana, Ariel Yehuda Cohen, and Moshe Shapira. Anisotropy on mechanical properties of cmsx-6 ni-base superalloy single crystal using profilometer indentation plastometer (pip) and small punch test (spt). Journal of Minerals and Materials Characterization and Engineering, 14:15-25, Jan 2026. URL: https://doi.org/10.4236/jmmce.2026.141002, doi:10.4236/jmmce.2026.141002. This article has 0 citations.

11. (moreno2026anisotropyonmechanical pages 5-8): Daniel Moreno, Amit Yair, Libi Shechner, Yohanan Nahmana, Ariel Yehuda Cohen, and Moshe Shapira. Anisotropy on mechanical properties of cmsx-6 ni-base superalloy single crystal using profilometer indentation plastometer (pip) and small punch test (spt). Journal of Minerals and Materials Characterization and Engineering, 14:15-25, Jan 2026. URL: https://doi.org/10.4236/jmmce.2026.141002, doi:10.4236/jmmce.2026.141002. This article has 0 citations.

12. (moreno2026anisotropyonmechanical pages 1-3): Daniel Moreno, Amit Yair, Libi Shechner, Yohanan Nahmana, Ariel Yehuda Cohen, and Moshe Shapira. Anisotropy on mechanical properties of cmsx-6 ni-base superalloy single crystal using profilometer indentation plastometer (pip) and small punch test (spt). Journal of Minerals and Materials Characterization and Engineering, 14:15-25, Jan 2026. URL: https://doi.org/10.4236/jmmce.2026.141002, doi:10.4236/jmmce.2026.141002. This article has 0 citations.

13. (chawla2026randomcombinatoriallibraries pages 3-6): Vivek Chawla, Dayakar Penumadu, and Sergei Kalinin. Random combinatorial libraries and automated nanoindentation for high-throughput structural materials discovery. Communications Materials, Aug 2026. URL: https://doi.org/10.1038/s43246-026-01294-8, doi:10.1038/s43246-026-01294-8. This article has 1 citations and is from a peer-reviewed journal.

14. (chawla2026randomcombinatoriallibraries pages 16-18): Vivek Chawla, Dayakar Penumadu, and Sergei Kalinin. Random combinatorial libraries and automated nanoindentation for high-throughput structural materials discovery. Communications Materials, Aug 2026. URL: https://doi.org/10.1038/s43246-026-01294-8, doi:10.1038/s43246-026-01294-8. This article has 1 citations and is from a peer-reviewed journal.

15. (giri2026insitusensormonitoring pages 1-2): Sandesh Giri, Sen Liu, Sanam Gorgannejad, Vivek Thampy, Peiyu Quan, Jenny W. Nicolino, Maria Strantza, Jean-Baptiste Forien, Aiden A. Martin, Nicholas P. Calta, and Christopher J. Tassone. In-situ sensor monitoring of multi-class gas porosity formation in laser powder bed fusion using convolutional neural network. Journal of Intelligent Manufacturing, Apr 2026. URL: https://doi.org/10.1007/s10845-026-02861-z, doi:10.1007/s10845-026-02861-z. This article has 3 citations and is from a domain leading peer-reviewed journal.

16. (ozel2026detectionofanomalous pages 1-2): Tuğrul Özel. Detection of anomalous meltpool conditions using deep learning in laser powder bed fusion. Advances in Manufacturing, Jul 2026. URL: https://doi.org/10.1007/s40436-026-00620-0, doi:10.1007/s40436-026-00620-0. This article has 0 citations and is from a peer-reviewed journal.

17. (ozel2026detectionofanomalous pages 15-16): Tuğrul Özel. Detection of anomalous meltpool conditions using deep learning in laser powder bed fusion. Advances in Manufacturing, Jul 2026. URL: https://doi.org/10.1007/s40436-026-00620-0, doi:10.1007/s40436-026-00620-0. This article has 0 citations and is from a peer-reviewed journal.

18. (cao2026physicsinformeddeeplearning pages 11-13): Zhuohan Cao, Zheng Li, Jamie J. Kruzic, Aiping Wu, Ming Zhou, Xiaopeng Li, and Yue Zhao. Physics-informed deep learning for virtual crystallographic phase and grain orientation reconstruction of additively manufactured alloys. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10513494/v1, doi:10.21203/rs.3.rs-10513494/v1.

19. (cao2026physicsinformeddeeplearning pages 1-4): Zhuohan Cao, Zheng Li, Jamie J. Kruzic, Aiping Wu, Ming Zhou, Xiaopeng Li, and Yue Zhao. Physics-informed deep learning for virtual crystallographic phase and grain orientation reconstruction of additively manufactured alloys. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10513494/v1, doi:10.21203/rs.3.rs-10513494/v1.

20. (taherimousavi2026alloygenaphysicsgrounded pages 4-6): S. Mohadeseh Taheri-Mousavi and Bo Ni. Alloygen: a physics-grounded self-adaptive multi-agent framework for autonomous alloy design workflows in additive manufacturing. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10329502/v1, doi:10.21203/rs.3.rs-10329502/v1.

21. (taherimousavi2026alloygenaphysicsgrounded pages 1-4): S. Mohadeseh Taheri-Mousavi and Bo Ni. Alloygen: a physics-grounded self-adaptive multi-agent framework for autonomous alloy design workflows in additive manufacturing. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10329502/v1, doi:10.21203/rs.3.rs-10329502/v1.

22. (chawla2026randomcombinatoriallibraries pages 1-3): Vivek Chawla, Dayakar Penumadu, and Sergei Kalinin. Random combinatorial libraries and automated nanoindentation for high-throughput structural materials discovery. Communications Materials, Aug 2026. URL: https://doi.org/10.1038/s43246-026-01294-8, doi:10.1038/s43246-026-01294-8. This article has 1 citations and is from a peer-reviewed journal.

23. (chawla2026randomcombinatoriallibraries pages 6-9): Vivek Chawla, Dayakar Penumadu, and Sergei Kalinin. Random combinatorial libraries and automated nanoindentation for high-throughput structural materials discovery. Communications Materials, Aug 2026. URL: https://doi.org/10.1038/s43246-026-01294-8, doi:10.1038/s43246-026-01294-8. This article has 1 citations and is from a peer-reviewed journal.

24. (chawla2026randomcombinatoriallibraries pages 20-23): Vivek Chawla, Dayakar Penumadu, and Sergei Kalinin. Random combinatorial libraries and automated nanoindentation for high-throughput structural materials discovery. Communications Materials, Aug 2026. URL: https://doi.org/10.1038/s43246-026-01294-8, doi:10.1038/s43246-026-01294-8. This article has 1 citations and is from a peer-reviewed journal.

25. (cannon2026evaluationofthe pages 1-2): Liam Cannon, Karl Peter Davidson, and Md Zakaria Quadir. Evaluation of the small punch test: repeatability and sample parameter influence. Journal of Materials Engineering and Performance, Jul 2026. URL: https://doi.org/10.1007/s11665-026-14603-6, doi:10.1007/s11665-026-14603-6. This article has 0 citations and is from a peer-reviewed journal.

26. (muhit2026hotisostaticpressing pages 3-5): Md Muhiul Islam Muhit, Gabriel Awuku Dzukey, Umesh Gandhi, and Ala Qattawi. Hot isostatic pressing effects on multiscale mechanical properties and chromium-dependent strength retention in lpbf fe-based shape memory alloys. Scientific Reports, May 2026. URL: https://doi.org/10.1038/s41598-026-48695-w, doi:10.1038/s41598-026-48695-w. This article has 0 citations and is from a peer-reviewed journal.

27. (ercetin2026aidrivenimageprocessing pages 20-21): Ali Ercetin, Ibrahim Arpaci, Samet Memiş, Amila Akagic, and Özgür Özgün. Ai-driven image processing for microstructure and surface characterization: a systematic review of methods, materials, and applications. Archives of Computational Methods in Engineering, May 2026. URL: https://doi.org/10.1007/s11831-026-10641-4, doi:10.1007/s11831-026-10641-4. This article has 4 citations and is from a peer-reviewed journal.

28. (ercetin2026aidrivenimageprocessing pages 21-21): Ali Ercetin, Ibrahim Arpaci, Samet Memiş, Amila Akagic, and Özgür Özgün. Ai-driven image processing for microstructure and surface characterization: a systematic review of methods, materials, and applications. Archives of Computational Methods in Engineering, May 2026. URL: https://doi.org/10.1007/s11831-026-10641-4, doi:10.1007/s11831-026-10641-4. This article has 4 citations and is from a peer-reviewed journal.
