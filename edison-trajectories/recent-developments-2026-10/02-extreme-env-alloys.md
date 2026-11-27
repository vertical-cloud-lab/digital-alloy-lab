<!--
Edison Scientific LITERATURE_HIGH task
- Task ID: bf148e03-9f78-415b-b30f-ae10a5995bbb
- Submitted: 2026-10-06T19:03:21Z
- Fetched: 2026-10-06T19:34:44Z (status: success)
- Raw trajectory JSON: raw/02-extreme-env-alloys.json
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

QUESTION 2 - EXTREME-ENVIRONMENT ALLOYS BY ADDITIVE MANUFACTURING: What new
work is there on
(a) refractory complex concentrated / refractory high-entropy alloys (Mo, Nb,
Ta, W, Hf, Zr, Ti, V, Cr, Al additions) and Nb-based alloys (e.g., C103)
processed by LPBF, DED, or electron-beam powder bed fusion - printability and
cracking, ductilization strategies, oxidation resistance and coatings,
elevated-temperature (>= 1200 C) strength and creep, and use for hypersonic
leading edges or thermal protection;
(b) machine-learning- or CALPHAD-guided design of RCCAs, including new
thermodynamic databases or high-throughput CALPHAD assessments of refractory
systems;
(c) strategic-element-lean (low Co / Re / Hf / Ta) Ni-based or Co-Ni
superalloys designed for LPBF crack resistance (e.g., ABD-900AM-type alloys,
oxide-dispersion-strengthened NiCoCr such as NASA GRX-810, AI-designed
superalloys) and their creep and oxidation behavior;
(d) elevated-temperature aluminum alloys for AM (e.g., Al-Ce, Al-Zr-Sc-Er,
Al-Ni-Mn) that could serve as a low-melting-point bridge system for the
methodology demonstration, with aerospace-relevant service to ~300-400 C.
Highlight results that (i) make one demonstration system more or less
attractive for an AFOSR extreme-environments YIP, (ii) quantify current
performance gaps the platform should target (e.g., specific strength at
1200-1600 C, oxidation rate, room-temperature ductility thresholds,
crack-free LPBF windows), or (iii) come from AFRL, AFOSR-funded, NASA, or
DoD-laboratory groups.

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

QUESTION 2 - EXTREME-ENVIRONMENT ALLOYS BY ADDITIVE MANUFACTURING: What new
work is there on
(a) refractory complex concentrated / refractory high-entropy alloys (Mo, Nb,
Ta, W, Hf, Zr, Ti, V, Cr, Al additions) and Nb-based alloys (e.g., C103)
processed by LPBF, DED, or electron-beam powder bed fusion - printability and
cracking, ductilization strategies, oxidation resistance and coatings,
elevated-temperature (>= 1200 C) strength and creep, and use for hypersonic
leading edges or thermal protection;
(b) machine-learning- or CALPHAD-guided design of RCCAs, including new
thermodynamic databases or high-throughput CALPHAD assessments of refractory
systems;
(c) strategic-element-lean (low Co / Re / Hf / Ta) Ni-based or Co-Ni
superalloys designed for LPBF crack resistance (e.g., ABD-900AM-type alloys,
oxide-dispersion-strengthened NiCoCr such as NASA GRX-810, AI-designed
superalloys) and their creep and oxidation behavior;
(d) elevated-temperature aluminum alloys for AM (e.g., Al-Ce, Al-Zr-Sc-Er,
Al-Ni-Mn) that could serve as a low-melting-point bridge system for the
methodology demonstration, with aerospace-relevant service to ~300-400 C.
Highlight results that (i) make one demonstration system more or less
attractive for an AFOSR extreme-environments YIP, (ii) quantify current
performance gaps the platform should target (e.g., specific strength at
1200-1600 C, oxidation rate, room-temperature ductility thresholds,
crack-free LPBF windows), or (iii) come from AFRL, AFOSR-funded, NASA, or
DoD-laboratory groups.

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


# Extreme-Environment Alloys by Additive Manufacturing: Developments April–October 2026

This report synthesizes new work published or posted between 2026-04-01 and 2026-10-06 across four sub-topics relevant to the PI's proposed autonomous alloy discovery platform for AM extreme-environment alloys. Items from January–March 2026 are included only when especially important and are labeled "earlier 2026." Several highly relevant papers were identified but could not be obtained for full-text verification; these are flagged accordingly.

The summary table below organizes the most consequential items by topic, relevance tag, and actionable significance.

| Citation | Abbreviated title | Date | Topic | Relevance tags | Why it matters |
|---|---|---:|---|---|---|
| Brizes et al. (2026) | LDNb-ODS LPBF and elevated-temperature performance | Sep 2026 | (a) | [CITE-1PAGER] [CITE-FULL] [COMPETITOR] | NASA-led result: 6.73 g cm⁻³ LPBF Nb alloy achieved 21.4 h rupture life at 1093 °C and 20.7 MPa uncoated—about 10× C103—and 84.8 h with an R512E silicide coating; oxidation remains life-limiting. (brizes2026adispersionstrengthenedlowdensity pages 18-21, brizes2026adispersionstrengthenedlowdensity pages 5-8) |
| Frey, Mullin et al. (2026 issue) | Historical and contemporary refractory-alloy development | Online date appears Dec 2025; 2026 issue | (a) | [AWARENESS] | Authoritative roadmap: refractory AM still lacks mature processing maps, solidification data, interstitial-aware databases, and established ductility/toughness thresholds for crack-free printing. Treat as outside the requested window unless the publisher confirms a 2026 online-first date. (frey2026aperspectiveon pages 25-26, frey2026aperspectiveon pages 26-27, frey2026aperspectiveon pages 28-30) |
| Keller et al. (2026) | AM of refractory niobium alloys: review | May 2026 | (a) | [CITE-FULL] | Useful Nb/C103 state-of-field review: oxygen can drive Nb ductility nearly to zero at roughly 1 at.% O, underscoring atmosphere, powder-handling, and contamination control as central research variables. (keller2026additivemanufacturingof pages 1-2) |
| Jabir, Salazar & Li (2026) | TiWMo refractory MEA by LPBF | Mar 2026; earlier 2026 | (a) | [CITE-FULL] | Elemental-powder LPBF produced a dominant single BCC phase; fine 5–25 μm W, 350 W, and 250 mm s⁻¹ reduced unmelted W to 0.01% and reached 633 HV. Demonstrates a low-cost composition-screening route but not tensile ductility or ≥1200 °C performance. (jabir2026investigationofprocess pages 1-2, jabir2026investigationofprocess pages 4-7) |
| Rubio-Ejchel et al. (2026) | Ti64–C103–GRCop-42 graded materials by LP-DED | Sep 2026 | (a) | [CITE-FULL] | CALPHAD-informed C103 bridging avoided the worst Cu–Ti region and yielded >99% dense Ti64–C103 gradients; the Ti64–C103 sandwich reached 390 MPa yield, 510 MPa UTS, and ~45% local C103 elongation, but Cu–Hf phases caused brittle C103–GRCop failure. (rubioejchel2026laserpowderdirected pages 11-12, rubioejchel2026laserpowderdirected pages 6-7, rubioejchel2026laserpowderdirected pages 2-3) |
| Dodge et al. (2026) | Ultrasonic atomization of TiZrNbHfTa for AM | Jul 2026 | (a) | [CITE-1PAGER] [CITE-FULL] | Directly relevant to rePOWDER feasibility: establishes ultrasonic atomization of a refractory HEA as an active route. Full-text verification of yield, oxygen pickup, size distribution, and plasma-versus-induction limitations is still needed. |
| Xiao et al. (2026) | WMoTaNbV RHEA by EB-PBF | Oct 2026 | (a) | [CITE-FULL] | Timely evidence that EB-PBF/preheating is being used for a canonical W–Mo–Ta–Nb–V system; compare density, cracking, texture, ductility, and elevated-temperature properties against LPBF before citing quantitative claims. |
| Sowards et al. (2026) | ML/computational study of refractory-alloy solidification cracking | Mar 2026; earlier 2026 | (a)/(b) | [CITE-1PAGER] [CITE-FULL] [NOVELTY-RISK] [COMPETITOR] | Composition-dependent cracking prediction overlaps the proposed cheap printability-surrogate layer, though not the full powder-to-property BOFN. Position the platform as using such models as network nodes rather than claiming first use of ML for refractory-AM manufacturability. |
| Kumaravel et al. (2026) | Ti-alloying mitigation of RCCA AM challenges | Jan 2026; earlier 2026 | (a) | [CITE-FULL] | Ti alloying and multi-material feedstock provide a concrete ductilization/printability strategy for RCCAs. It strengthens the case for composition–process co-design but requires full-text confirmation of cracking and tensile metrics. |
| Peterson et al. (2026) | ML-guided CALPHAD design of Ru-stabilized BCC–B2 alloys | Sep 2026 preprint | (b) | [CITE-FULL] [COMPETITOR] | Random-forest active learning screened 500 Nb–Ta–Mo–V–Ru–Ti–Zr–Hf–Al–Y compositions with TCHEA4; 100 met BCC+B2, no-liquid, purity, and 15–55% secondary-phase criteria. It competes at the CALPHAD-screening node, not at autonomous AM execution. (peterson2609machinelearningguided pages 1-3, peterson2609machinelearningguided pages 17-19) |
| Omprakash et al. (2026) | First-principles phase fields for refractory alloys | Sep 2026 preprint | (b) | [CITE-FULL] | DFT-informed pycalphad databases cover Cr–Hf–Mo–Nb–Ta–Ti–V–W–Zr and generate diagrams for 36 binaries, 84 ternaries, 126 quaternaries, and 126 quinaries. Liquid thermodynamics remain absent, making measured solidification/AM data a valuable calibration target. (omprakash2026firstprinciplesbasedpredictionof pages 8-11) |
| Ray et al. (2026) | Electronic manifolds for extrapolative alloy discovery | Mar 2026; earlier-2026 candidate | (b) | [CITE-1PAGER] [CITE-FULL] | Physics-informed descriptors transferred from Al–Nb–Ti–Zr to Mo–Nb–Ta–Ti–V–W–Zr; fewer than 0.2% of the source dataset gave <2% bulk-modulus error, and 20 target samples produced <3% error for seven-component alloys. Strong benchmark for sample efficiency, but it predicts computational properties rather than navigating an AM function network. (ray2026universalelectronicmanifolds pages 8-9, ray2026universalelectronicmanifolds pages 1-2) |
| Islam et al. / Arroyave group (2026) | Bayesian co-optimization of BCC–B2 RHEA performance and manufacturability | Jan 2026; earlier 2026 | (b) | [NOVELTY-RISK] [COMPETITOR] [CITE-FULL] | Directly overlaps Bayesian composition optimization and joint performance/manufacturability objectives. Distinguish the proposed work by its explicit DAG, node-level partial evaluations, cost-aware stopping/query decisions, physical powder-to-LPBF execution, and elevated-temperature terminal tests. |
| Jiang et al. (2026) | Multi-fidelity active learning for TaNbMoVW RHEAs | Feb 2026; earlier-2026 candidate | (b) | [NOVELTY-RISK] [COMPETITOR] [CITE-FULL] | Most important semantic risk to broad “first multi-fidelity optimization of RCCAs” language. It does not, based on available metadata, establish BOFN partial evaluation across atomization, LPBF, microstructure, and high-temperature testing; narrow the novelty claim accordingly. |
| Chen et al. (2026) | Yttria-content effects in LPBF GRX-810 | Jul 2026 | (c) | [CITE-1PAGER] [CITE-FULL] [COMPETITOR] | NASA co-authored study identifies 0.30–0.45 wt.% Y₂O₃ as the favorable window. Above 0.5%, as-built elongation fell from 27% to ~4%; HIP restored up to ~42% elongation but reduced yield strength from ~785 to ~685 MPa. (chen2026thecorrelationbetween pages 17-18, chen2026thecorrelationbetween pages 1-2) |
| Li et al. (2026) | Strong, ductile, heat-resistant Al alloy by LPBF | Apr 2026 | (d) | [CITE-1PAGER] [CITE-FULL] [COMPETITOR] | Raises the bridge-system benchmark: 582 MPa room-temperature tensile strength and 114 MPa at 400 °C, with creep tests at 400 °C and 25–40 MPa. Aluminum remains experimentally accessible, but the proposal should frame it as platform commissioning rather than the extreme-environment endpoint. (li2026strongyetductile pages 1-6, li2026strongyetductile pages 27-31) |
| Guo et al. (2026) | Al–Ni–Ce–Mn–Fe alloy by DED | Jan 2026; earlier 2026 | (d) | [CITE-FULL] | Ultrasonic-atomized powder produced <5 μm features and <32 MPa residual stress; versus DED AlSi10Mg, yield and UTS increased 70% and 50%. Highly relevant to atomization-to-AM commissioning, although no 300–400 °C property data were reported in the available evidence. (guo2026mechanicalandin pages 1-3) |
| Mallia & Caputo (2026) | AI-guided self-driving laboratories; LLNL APEX | Aug 2026 | Novelty/competitor | [NOVELTY-RISK] [COMPETITOR] [CITE-FULL] | Identifies LLNL APEX as a DED-based platform integrating robotic handling, post-processing, and characterization for closed-loop composition–process–property iteration. Available evidence does not show BOFN, partial-node evaluations, or fidelity/cost-aware decisions, so it weakens broad autonomy claims but not the specific methodological claim. (mallia2026aiguidedselfdrivinglaboratories pages 6-12, mallia2026aiguidedselfdrivinglaboratories pages 12-17) |
| Zhao et al. (2026) | Alloy-design paradigms in AM | Mar 2026; earlier 2026 | Novelty/competitor | [AWARENESS] [NOVELTY-RISK] | Articulates an emerging “AI Auto-Lab for AM Materials” paradigm integrating design, fabrication, verification, and iterative optimization. It is primarily a roadmap, but it makes generic “first autonomous AM-alloy platform” wording untenable. (zhao2026alloydesignparadigms pages 10-12) |
| Priyadarshini et al. (2026) | ML-driven closed-loop discovery of hard MPEAs | Jul 2026 | Novelty/competitor | [NOVELTY-RISK] [COMPETITOR] [CITE-FULL] | Demonstrates closed-loop MPEA discovery and therefore blocks a general claim of first closed-loop complex-alloy discovery. The defensible distinction is the cost-aware BOFN treatment of a physically executed, multi-stage AM pipeline with optional intermediate-node queries and an elevated-temperature terminal objective. |


*Table: The table organizes the most consequential 2026 publications by refractory AM, computational design, superalloys, aluminum bridge systems, and novelty/competition. Items lacking full-text evidence are explicitly treated as leads requiring verification.*

---

## (a) Refractory Complex Concentrated Alloys and Nb-Based Alloys Processed by AM

**Brizes, E. et al., "A Dispersion-Strengthened Low-Density Niobium Alloy and Its Elevated Temperature Mechanical Performance," NASA Technical Report, Sep 2026. DOI: 10.64631/zcym1460**
Online: September 2026. NASA GRC/AFRL-relevant team fabricated an oxide-dispersion-strengthened low-density Nb alloy (LDNb-ODS) by LPBF from blended Nb521 + Ti64 + Cr + Y₂O₃ nanoparticle powder. Density was 6.73 g/cm³ with ~30 nm yttria dispersoids. Room-temperature UTS reached 1,005 MPa; specific yield strength of 60–85 MPa/(g/cm³) was maintained to 800 °C, surpassing Ni625, Ni230, and GRX-810 in that regime. At 1,093 °C/20.7 MPa, uncoated LDNb-ODS survived 21.4 h (10× legacy C-103), while R512E silicide coating extended life to 84.8 h. Oxidation—not creep—was the dominant life-limiting mechanism. Lack-of-fusion defects and Ti volatilization (31.5→24.8 wt%) were identified as processability challenges (brizes2026adispersionstrengthenedlowdensity pages 18-21, brizes2026adispersionstrengthenedlowdensity pages 5-8, brizes2026adispersionstrengthenedlowdensity pages 9-11). **Tags: [CITE-1PAGER] [CITE-FULL] [COMPETITOR]** — This NASA result directly quantifies the performance gap the PI's platform should target and validates LPBF of Nb-based ODS alloys.

**Keller, T. et al., "Additive manufacturing of refractory niobium alloys: a review," Progress in Additive Manufacturing, 11:6491–6517, May 2026. DOI: 10.1007/s40964-026-01728-2**
Online: May 2026. Comprehensive review of AM Nb alloy processing covering LPBF and EB-PBF. Highlights that oxygen pickup can drive Nb ductility to nearly zero at ~1 at.% O, underscoring the importance of atmosphere control and powder handling throughout the pipeline (keller2026additivemanufacturingof pages 1-2). **Tags: [CITE-FULL]**

**Jabir, A.A.M. et al., "Investigation of process parameters to fabricate TiWMo refractory medium entropy alloy via LPBF," Progress in Additive Manufacturing, 11:5567–5577, Mar 2026. DOI: 10.1007/s40964-026-01648-1** *(earlier 2026)*
Online: March 2026. Elemental-blend LPBF of equimolar TiWMo produced a single BCC phase with 633 HV max hardness. Fine W powder (5–25 µm) at 350 W / 250 mm/s reduced unmelted W to 0.01%. Demonstrates a low-cost composition-screening route from elemental powders but does not report tensile ductility or elevated-temperature properties (jabir2026investigationofprocess pages 1-2, jabir2026investigationofprocess pages 4-7). **Tags: [CITE-FULL]**

**Rubio-Ejchel, D. et al., "Laser powder directed energy deposition fabrication and tensile sandwich evaluation of Ti64-C103-GRCop-42 functionally graded materials," J. Mater. Res., Sep 2026. DOI: 10.1557/s43578-026-01964-w**
Online: September 2026. CALPHAD/Scheil-informed LP-DED grading with C103 as intermediate bridge: Ti64→C103 gradient achieved >99% density and 390 MPa yield / 510 MPa UTS / ~45% local elongation in C103, but Cu–Hf intermetallics caused brittle failure at the C103→GRCop-42 interface (rubioejchel2026laserpowderdirected pages 11-12, rubioejchel2026laserpowderdirected pages 6-7, rubioejchel2026laserpowderdirected pages 2-3). **Tags: [CITE-FULL]**

**Dodge, B.S. et al., "Ultrasonic atomization of a refractory high-entropy alloy TiZrNbHfTa for additive manufacturing," Powders, 5:25, Jul 2026. DOI: 10.3390/powders5030025** *(unobtainable — full-text verification needed)*
Directly relevant to the PI's rePOWDER ultrasonic atomizer: establishes ultrasonic atomization of a quinary refractory HEA. **Tags: [CITE-1PAGER] [CITE-FULL]**

**Xiao, B. et al., "Microstructure and mechanical properties of WMoTaNbV refractory high-entropy alloy via electron-beam powder-bed fusion," Appl. Mater. Today, 52:103378, Oct 2026. DOI: 10.1016/j.apmt.2026.103378** *(unobtainable)*
Timely EB-PBF data on the canonical W-Mo-Ta-Nb-V system. **Tags: [CITE-FULL]**

**Sowards, J.W. et al., "Solidification cracking of refractory alloys: a computational and machine learning study," Materials & Design, 263:115679, Mar 2026. DOI: 10.1016/j.matdes.2026.115679** *(earlier 2026, unobtainable)*
ML-based composition-dependent cracking prediction for refractory AM. Partially overlaps the proposed cheap-printability-surrogate node. **Tags: [CITE-1PAGER] [CITE-FULL] [NOVELTY-RISK] [COMPETITOR]** — The PI should position such models as constituent nodes within the DAG, not claim novelty of ML for refractory cracking prediction per se.

**Kumaravel, M. et al., "Mitigating the challenges in AM of refractory CCAs using Ti alloying via multi-material feedstock," MSEA, Jan 2026. DOI: 10.1016/j.msea.2026.149867** *(earlier 2026, unobtainable)*
Ti alloying as a ductilization strategy for RCCA LPBF. **Tags: [CITE-FULL]**

**Frey, C. et al., "A Perspective on the Historical and Contemporary Development of Refractory Alloys," Met. Mater. Trans. A, 57:461–503, 2026 issue. DOI: 10.1007/s11661-025-07996-x**
Identifies key gaps: minimum low-temperature ductility/toughness for crack-free printing is unknown; partition coefficients and solidus/liquidus data are sparse; current CALPHAD databases typically omit interstitial elements (C, O) despite their critical effects on cracking and ductility (frey2026aperspectiveon pages 25-26, frey2026aperspectiveon pages 26-27, frey2026aperspectiveon pages 28-30). **Tags: [AWARENESS]** — Treat as outside the primary window unless online-first date confirmed in 2026.

---

## (b) ML- or CALPHAD-Guided Design of RCCAs

**Ray, P. et al., "Electronic manifolds for extrapolative alloy discovery," Digital Discovery, Mar 2026. DOI: 10.48550/arxiv.2603.06953** *(earlier 2026)*
Physics-informed pseudo-electron-density descriptors enable Bayesian active learning that predicts bulk modulus with <2% NMAE from only 10 training samples (~0.2% of dataset) in the Al-Nb-Ti-Zr space, and transfers zero-shot to the 7-component Mo-Nb-Ta-Ti-V-W-Zr system; 20 actively selected target samples yield <3% NMAE (ray2026universalelectronicmanifolds pages 8-9, ray2026universalelectronicmanifolds pages 1-2). Demonstrates radical sample efficiency for RCCA property prediction. **Tags: [CITE-1PAGER] [CITE-FULL]**

**Peterson, N.E. et al., "Machine Learning Guided CALPHAD Design of Ru-Stabilized BCC B2 Refractory Alloys," arXiv:2609.14925, Sep 2026.**
Random-forest active learning coupled to Thermo-Calc TCHEA4 screened 500 compositions in the Nb-Ta-Mo-V-Ru-Ti-Zr-Hf-Al-Y space, identifying 100 meeting BCC+B2 stability, phase purity, and precipitate-fraction criteria at 1300 °C. Promising Nb-Mo-Ti-Ru-Hf-Zr and Nb-Ta-Ru-Hf compositions identified (peterson2609machinelearningguided pages 1-3, peterson2609machinelearningguided pages 17-19). **Tags: [CITE-FULL] [COMPETITOR]**

**Omprakash, P. et al., "First-principles-based Prediction of Phase Fields: Part I. Binary and Ternary Refractory Alloys," arXiv:2609.06627, Sep 2026.**
DFT-informed pycalphad databases cover the full Cr-Hf-Mo-Nb-Ta-Ti-V-W-Zr element pool, generating phase diagrams for 36 binaries through 126 quinaries. Liquidus data remain absent, making experimental solidification benchmarks valuable. This directly validates the PI's pycalphad pipeline and identifies where that pipeline adds value (omprakash2026firstprinciplesbasedpredictionof pages 8-11). **Tags: [CITE-FULL]**

**Shen, C. et al., "How Can Machine Learning Accelerate CALPHAD Free Energy Modeling?" arXiv:2606.01305, May 2026.**
Proposes ML surrogates for CALPHAD Gibbs energy functions spanning transition metals and refractory elements. **Tags: [AWARENESS]**

**Yan, Y. et al., "Machine learning-enabled discovery of refractory high entropy alloys on curated data," Research Square preprint, Aug 2026. DOI: 10.21203/rs.3.rs-10354540/v1**
Curated RHEA dataset with phase-label reassessment; F1=0.89 for predicting single-phase BCC stability, identifying mismatch in most-stable oxidation state (MSO_dv > 15) as a new ordering descriptor. **Tags: [CITE-FULL]**

**Islam, M.S. et al. / Arroyave group, "Bayesian multi-objective co-optimization of performance and manufacturability in BCC-B2 refractory high entropy alloys," SSRN 7549378, Jan 2026.** *(earlier 2026, unobtainable)*
**Tags: [NOVELTY-RISK] [COMPETITOR] [CITE-FULL]** — This work explicitly combines Bayesian multi-objective optimization with manufacturability constraints for RHEAs. It overlaps the PI's claim of "first" Bayesian optimization for AM RCCA pipelines. However, based on metadata, it appears to be a computational co-optimization rather than a physically executed AM loop with DAG-structured partial evaluations. The PI should sharpen the novelty claim accordingly.

**Jiang, T. et al., "Multi-fidelity, active-learning assisted design of TaNbMoVW refractory high-entropy alloys with superior mechanical properties," J. Phys.: Mater., 9:025003, Feb 2026. DOI: 10.1088/2515-7639/ae44d1** *(earlier 2026, unobtainable)*
**Tags: [NOVELTY-RISK] [COMPETITOR] [CITE-FULL]** — Multi-fidelity active learning applied specifically to TaNbMoVW RHEAs. This is the most direct semantic challenge to broad "first multi-fidelity optimization of RCCAs" language; however, it likely concerns computational fidelity layers (DFT vs. empirical), not the physical AM pipeline nodes with partial evaluations that the PI proposes.

---

## (c) Strategic-Element-Lean Superalloys for LPBF

**Chen, Y. et al., "The correlation between yttria content and thermal–mechanical properties of GRX-810," Progress in Additive Manufacturing, 11:8975–8992, Jul 2026. DOI: 10.1007/s40964-026-01834-1**
Online: July 2026. NASA co-authored (including Gradl). LPBF GRX-810 with 0.3–1.0 wt% Y₂O₃: the 0.30–0.45 wt% window gives the best strength–ductility balance. Above 0.5 wt%, as-built elongation drops from 27% to ~4%. HIP restores elongation to ~42% (≤0.45% Y₂O₃) or ~18% (>0.5% Y₂O₃) while reducing yield from ~785 to ~685 MPa. Thermal conductivity degradation from LPBF defects is also recovered by HIP. No new creep or oxidation data are reported in this paper (chen2026thecorrelationbetween pages 17-18, chen2026thecorrelationbetween pages 1-2). **Tags: [CITE-1PAGER] [CITE-FULL]** — Sets a quantitative yttria-content target and confirms GRX-810 as a viable secondary demonstration system.

**Wassermann, N.A. et al., "Influence of melt pool overlap on inclusion entrapment and dispersoid characteristics in ODS Ni-20Cr fabricated by PBF-LB," SSRN 6635781, Jan 2026.** *(earlier 2026, unobtainable)*
Examines how melt-pool overlap during LPBF affects oxide-dispersoid trapping and distribution in Ni-20Cr ODS. **Tags: [CITE-FULL]**

**Ding, H. et al., "Dual-doped IN939 superalloy with superior strength and high temperature oxidation resistance via LPBF," MSEA, 961:150144, Jun 2026. DOI: 10.1016/j.msea.2026.150144** *(unobtainable)*
Dual-doped (likely Y₂O₃ + another species) IN939 by LPBF with enhanced strength and oxidation resistance. Relevant as an alternative strategic-element-lean superalloy approach. **Tags: [CITE-FULL]**

No ABD-900AM-specific paper or newly AI-designed Ni superalloy was found within the April–October 2026 window.

---

## (d) Elevated-Temperature Aluminum Alloys for AM

**Li, G. et al., "Strong yet ductile heat-resistant aluminum alloy by additive manufacturing," Nature Communications, 17, Apr 2026. DOI: 10.1038/s41467-026-71926-7**
Online: April 2026. LPBF produced an Al alloy with ~14 vol% heat-resistant multicomponent intermetallic nanophases (HMINPs) embedded in cell boundaries. Room-temperature UTS of 582 MPa; 114 MPa retained at 400 °C. Creep tests at 400 °C / 25–40 MPa demonstrated exceptional resistance. Partial solid-state amorphization of HMINPs at 300–400 °C provides an additional toughening mechanism (li2026strongyetductile pages 1-6, li2026strongyetductile pages 27-31). **Tags: [CITE-1PAGER] [CITE-FULL]** — This Nature Communications result raises the benchmark significantly for any Al-based bridge system, and the compositional details are worth checking for compatibility with the PI's atomization capability.

**Guo, D. et al., "Mechanical and in situ thermal-related behavior during DED AM of a high-performance Al alloy," Int. J. Extreme Manuf., 8:035002, Jan 2026. DOI: 10.1088/2631-7990/ae3349** *(earlier 2026)*
DED of an Al-Ni-Ce-Mn-Fe alloy using ultrasonic-atomized powder achieved <5 µm microstructure, <32 MPa residual stress, and 70%/50% improvements in yield/UTS over DED AlSi10Mg. Novel multimodal in situ characterization (synchrotron XRD + X-ray imaging + IR) elucidated phase evolution and stress accumulation during DED (guo2026mechanicalandin pages 1-3). **Tags: [CITE-FULL]** — Highly relevant to the PI's ultrasonic atomization → AM commissioning pathway.

**Bazaleeva, K.O. et al., "Deformation behavior of an Al-Ce-Fe-Ni-Zr alloy fabricated by L-PBF," Physical Mesomechanics, 29:931–943, Sep 2026. DOI: 10.1134/s1029959926600102** *(unobtainable)*
LPBF of an Al-Ce-Fe-Ni-Zr alloy — directly in the compositional space of interest for elevated-temperature Al alloys. **Tags: [CITE-FULL]**

---

## Novelty Risk and Competitor Assessment

**LLNL APEX** — The Autonomous Alloy Prediction and Experimentation platform is a DED-based self-driving laboratory integrating robotic handling, post-processing, and automated characterization (mallia2026aiguidedselfdrivinglaboratories pages 6-12, mallia2026aiguidedselfdrivinglaboratories pages 12-17). It is classified as {MSS-3 (bulk metallurgy), HAL-2 (linked modules), SAL-2 (reactive closed-loop BO)}. Available evidence does not show it using BOFN, partial-evaluation fidelity management, or cost-aware node-selection decisions. **Tags: [COMPETITOR] [NOVELTY-RISK]** — APEX weakens generic "first autonomous AM alloy platform" claims but does not preempt the specific BOFN/partial-evaluation methodology.

**Priyadarshini, M.S. et al., "Machine learning-driven closed-loop discovery of hard multiple principal element alloys," Materials Horizons, Jul 2026. DOI: 10.1039/d6mh00103c** *(unobtainable)*
**Tags: [NOVELTY-RISK] [COMPETITOR]** — Closed-loop MPEA discovery. Blocks a blanket "first closed-loop complex-alloy discovery" claim.

**Zhao, L. et al., "Alloy design paradigms in additive manufacturing," Int. J. Extreme Manuf., 8:033003, Mar 2026. DOI: 10.1088/2631-7990/ae45de** *(earlier 2026)*
Proposes an "AI Auto-Lab for AM Materials" paradigm (zhao2026alloydesignparadigms pages 10-12). Although primarily a roadmap, it makes generic "first autonomous AM alloy platform" language untenable. **Tags: [AWARENESS] [NOVELTY-RISK]**

---

## Top 5 Things the PI Should Know

1. **The novelty claim needs tightening immediately.** At least three 2026 publications (Islam/Arroyave Bayesian multi-objective RHEA co-optimization; Jiang et al. multi-fidelity AL for TaNbMoVW; Priyadarshini et al. closed-loop MPEA discovery) use Bayesian or multi-fidelity optimization for complex alloy design. LLNL's APEX demonstrates a closed-loop DED-based alloy discovery platform. None, however, demonstrate cost-aware BOFN with partial evaluations across a physically executed multi-stage AM pipeline (powder → LPBF → microstructure → elevated-temperature property). The novelty claim must be narrowed to this specific DAG/partial-evaluation architecture.

2. **NASA's LDNb-ODS result (Brizes et al., Sep 2026) is the single most important refractory-AM benchmark.** It directly quantifies the performance gap the PI's platform should target: specific yield strength of 60–85 MPa/(g/cm³) to 800 °C, 10× improvement over C-103 in rupture at 1,093 °C, and oxidation as the life-limiting factor. This is from a NASA group (Smith, Kantzos) and should be cited in the one-pager.

3. **CALPHAD databases for refractory systems are expanding but remain incomplete.** Omprakash et al. generated DFT-informed pycalphad databases covering the full Cr-Hf-Mo-Nb-Ta-Ti-V-W-Zr pool but lack liquidus/solidification data (omprakash2026firstprinciplesbasedpredictionof pages 8-11). Frey et al. emphasize missing interstitial (C, O) thermodynamics (frey2026aperspectiveon pages 28-30). These gaps directly support the PI's value proposition of coupling CALPHAD screening with experimental AM validation.

4. **GRX-810 yttria-content optimization (Chen et al., Jul 2026) narrows the design space for the secondary system.** The optimal window is 0.30–0.45 wt% Y₂O₃; above 0.5%, ductility degrades severely. This NASA co-authored result (with Gradl) is directly relevant to an AFOSR-aligned secondary demonstration (chen2026thecorrelationbetween pages 17-18, chen2026thecorrelationbetween pages 1-2).

5. **Elevated-temperature Al alloys for AM have advanced rapidly (Li et al., Nature Comms, Apr 2026).** A 582 MPa RT / 114 MPa at 400°C LPBF Al alloy with exceptional creep resistance at 400 °C sets a high benchmark for any bridge-system demonstration (li2026strongyetductile pages 1-6). The PI should frame the Al system as platform commissioning/validation, not an extreme-environment result per se.

---

## Suggested Wording Changes for the White Paper

The current claim—*"This cost-aware, partial-evaluation formulation applied for the first time to a complex additive manufacturing pipeline for alloys is the core methodological novelty"*—should be revised in light of recent work demonstrating Bayesian multi-objective optimization for RHEA design (Islam et al., SSRN 7549378, Jan 2026), multi-fidelity active learning for TaNbMoVW (Jiang et al., J. Phys.: Mater. 9:025003, Feb 2026), closed-loop MPEA discovery (Priyadarshini et al., Mater. Horiz., Jul 2026), and LLNL's APEX autonomous DED platform (Mallia & Caputo, Aug 2026) (mallia2026aiguidedselfdrivinglaboratories pages 12-17, mallia2026aiguidedselfdrivinglaboratories pages 6-12).

**Suggested rewording:** *"While closed-loop Bayesian optimization and multi-fidelity surrogate strategies have recently been applied to alloy composition screening and individual AM process steps, no prior work has modeled the complete powder-to-elevated-temperature-property pipeline as a directed acyclic graph of heterogeneous surrogate nodes and optimized it via cost-aware Bayesian optimization of function networks with partial evaluations—where the algorithm autonomously decides when to query cheap nodes (CALPHAD simulations, single-track scans, density cubes, hardness maps) versus expensive terminal nodes (full elevated-temperature tensile/creep tests). This DAG-structured, partial-evaluation formulation applied to a physically executed, multi-stage additive manufacturing pipeline for refractory and superalloy systems is the core methodological novelty."*

This revision (i) acknowledges existing multi-fidelity and closed-loop work, (ii) specifies the DAG/BOFN/partial-evaluation architecture as the unique contribution, and (iii) ties the novelty to the physical AM pipeline rather than to computational-only optimization.

References

1. (brizes2026adispersionstrengthenedlowdensity pages 18-21): A Dispersion-Strengthened Low-Density Niobium Alloy and Its Elevated Temperature Mechanical Performance

2. (brizes2026adispersionstrengthenedlowdensity pages 5-8): A Dispersion-Strengthened Low-Density Niobium Alloy and Its Elevated Temperature Mechanical Performance

3. (frey2026aperspectiveon pages 25-26): Carolina Frey, Kaitlyn M. Mullin, Joseph Jankowski, Leah H. Mills, Noah R. Philips, and Tresa M. Pollock. A perspective on the historical and contemporary development of refractory alloys. Metallurgical and Materials Transactions A, 57:461-503, Dec 2026. URL: https://doi.org/10.1007/s11661-025-07996-x, doi:10.1007/s11661-025-07996-x. This article has 16 citations.

4. (frey2026aperspectiveon pages 26-27): Carolina Frey, Kaitlyn M. Mullin, Joseph Jankowski, Leah H. Mills, Noah R. Philips, and Tresa M. Pollock. A perspective on the historical and contemporary development of refractory alloys. Metallurgical and Materials Transactions A, 57:461-503, Dec 2026. URL: https://doi.org/10.1007/s11661-025-07996-x, doi:10.1007/s11661-025-07996-x. This article has 16 citations.

5. (frey2026aperspectiveon pages 28-30): Carolina Frey, Kaitlyn M. Mullin, Joseph Jankowski, Leah H. Mills, Noah R. Philips, and Tresa M. Pollock. A perspective on the historical and contemporary development of refractory alloys. Metallurgical and Materials Transactions A, 57:461-503, Dec 2026. URL: https://doi.org/10.1007/s11661-025-07996-x, doi:10.1007/s11661-025-07996-x. This article has 16 citations.

6. (keller2026additivemanufacturingof pages 1-2): Thomas Keller, Cheng Zeng, Nathan Post, Jack Lesko, and Andrew Neils. Additive manufacturing of refractory niobium alloys: a review of processing, properties, modeling, and applications. Progress in Additive Manufacturing, 11:6491-6517, May 2026. URL: https://doi.org/10.1007/s40964-026-01728-2, doi:10.1007/s40964-026-01728-2. This article has 5 citations and is from a peer-reviewed journal.

7. (jabir2026investigationofprocess pages 1-2): Abdullah Al Masum Jabir, Lindsey Salazar, and Jianzhi Li. Investigation of process parameters to fabricate tiwmo refractory medium entropy alloy via laser powder bed fusion. Progress in Additive Manufacturing, 11:5567-5577, Mar 2026. URL: https://doi.org/10.1007/s40964-026-01648-1, doi:10.1007/s40964-026-01648-1. This article has 4 citations and is from a peer-reviewed journal.

8. (jabir2026investigationofprocess pages 4-7): Abdullah Al Masum Jabir, Lindsey Salazar, and Jianzhi Li. Investigation of process parameters to fabricate tiwmo refractory medium entropy alloy via laser powder bed fusion. Progress in Additive Manufacturing, 11:5567-5577, Mar 2026. URL: https://doi.org/10.1007/s40964-026-01648-1, doi:10.1007/s40964-026-01648-1. This article has 4 citations and is from a peer-reviewed journal.

9. (rubioejchel2026laserpowderdirected pages 11-12): Daniel Rubio-Ejchel, Michael Lester, KenHee Ryou, Christopher Tandoc, Dillon K. Jobes, Jun Fan, Wenda Tan, William S. LePage, Yong-Jie Hu, and Jerard V. Gordon. Laser powder directed energy deposition fabrication and tensile sandwich evaluation of ti64-c103-grcop-42 functionally graded materials. Journal of Materials Research, Sep 2026. URL: https://doi.org/10.1557/s43578-026-01964-w, doi:10.1557/s43578-026-01964-w. This article has 1 citations and is from a peer-reviewed journal.

10. (rubioejchel2026laserpowderdirected pages 6-7): Daniel Rubio-Ejchel, Michael Lester, KenHee Ryou, Christopher Tandoc, Dillon K. Jobes, Jun Fan, Wenda Tan, William S. LePage, Yong-Jie Hu, and Jerard V. Gordon. Laser powder directed energy deposition fabrication and tensile sandwich evaluation of ti64-c103-grcop-42 functionally graded materials. Journal of Materials Research, Sep 2026. URL: https://doi.org/10.1557/s43578-026-01964-w, doi:10.1557/s43578-026-01964-w. This article has 1 citations and is from a peer-reviewed journal.

11. (rubioejchel2026laserpowderdirected pages 2-3): Daniel Rubio-Ejchel, Michael Lester, KenHee Ryou, Christopher Tandoc, Dillon K. Jobes, Jun Fan, Wenda Tan, William S. LePage, Yong-Jie Hu, and Jerard V. Gordon. Laser powder directed energy deposition fabrication and tensile sandwich evaluation of ti64-c103-grcop-42 functionally graded materials. Journal of Materials Research, Sep 2026. URL: https://doi.org/10.1557/s43578-026-01964-w, doi:10.1557/s43578-026-01964-w. This article has 1 citations and is from a peer-reviewed journal.

12. (peterson2609machinelearningguided pages 1-3): Nathan E. Peterson, A. Mahata, Nicholas Beaver, and M. Kivy. Machine learning guided calphad design of ru-stabilized bcc b2 refractory alloys. ArXiv, Sep 2609. URL: https://doi.org/10.48550/arxiv.2609.14925, doi:10.48550/arxiv.2609.14925. This article has 0 citations.

13. (peterson2609machinelearningguided pages 17-19): Nathan E. Peterson, A. Mahata, Nicholas Beaver, and M. Kivy. Machine learning guided calphad design of ru-stabilized bcc b2 refractory alloys. ArXiv, Sep 2609. URL: https://doi.org/10.48550/arxiv.2609.14925, doi:10.48550/arxiv.2609.14925. This article has 0 citations.

14. (omprakash2026firstprinciplesbasedpredictionof pages 8-11): P. Omprakash, N. Crnkovich, J. Cavin, Nathan Curtis, Adrien Couet, and Rohan Mishra. First-principles-based prediction of phase fields: part i. binary and ternary refractory alloys. ArXiv, Sep 2026. URL: https://doi.org/10.48550/arxiv.2609.06627, doi:10.48550/arxiv.2609.06627. This article has 0 citations.

15. (ray2026universalelectronicmanifolds pages 8-9): Pranoy Ray, Sayan Bhowmik, Phanish Suryanarayana, Surya R. Kalidindi, and Andrew J. Medford. Electronic manifolds for extrapolative alloy discovery. Digital Discovery, Mar 2026. URL: https://doi.org/10.48550/arxiv.2603.06953, doi:10.48550/arxiv.2603.06953. This article has 2 citations and is from a peer-reviewed journal.

16. (ray2026universalelectronicmanifolds pages 1-2): Pranoy Ray, Sayan Bhowmik, Phanish Suryanarayana, Surya R. Kalidindi, and Andrew J. Medford. Electronic manifolds for extrapolative alloy discovery. Digital Discovery, Mar 2026. URL: https://doi.org/10.48550/arxiv.2603.06953, doi:10.48550/arxiv.2603.06953. This article has 2 citations and is from a peer-reviewed journal.

17. (chen2026thecorrelationbetween pages 17-18): Yehong Chen, Huan Ding, Selami Emanet, Ehsan Bagheri, Michael M. Talachian, Paul R. Gradl, and Shengmin Guo. The correlation between yttria content and thermal–mechanical properties of grx-810. Progress in Additive Manufacturing, 11:8975-8992, Jul 2026. URL: https://doi.org/10.1007/s40964-026-01834-1, doi:10.1007/s40964-026-01834-1. This article has 0 citations and is from a peer-reviewed journal.

18. (chen2026thecorrelationbetween pages 1-2): Yehong Chen, Huan Ding, Selami Emanet, Ehsan Bagheri, Michael M. Talachian, Paul R. Gradl, and Shengmin Guo. The correlation between yttria content and thermal–mechanical properties of grx-810. Progress in Additive Manufacturing, 11:8975-8992, Jul 2026. URL: https://doi.org/10.1007/s40964-026-01834-1, doi:10.1007/s40964-026-01834-1. This article has 0 citations and is from a peer-reviewed journal.

19. (li2026strongyetductile pages 1-6): Gan Li, Yu-He Huang, Chunlu Zhao, Xi He, Shuo Wang, Qiyang Tan, Ying Li, Fucong Lyu, Guanghui Feng, Jun-Hua Luan, Wanqian Hu, Zhen-Min Li, Xinggang Li, Yanjin Xu, Yuan-Song Zeng, Zhi-Qiang Li, Xin-Ping Mao, Ming-Xing Zhang, Le-Hua Qi, Qiang Zhu, and Jian Lu. Strong yet ductile heat-resistant aluminum alloy by additive manufacturing. Nature Communications, Apr 2026. URL: https://doi.org/10.1038/s41467-026-71926-7, doi:10.1038/s41467-026-71926-7. This article has 11 citations and is from a highest quality peer-reviewed journal.

20. (li2026strongyetductile pages 27-31): Gan Li, Yu-He Huang, Chunlu Zhao, Xi He, Shuo Wang, Qiyang Tan, Ying Li, Fucong Lyu, Guanghui Feng, Jun-Hua Luan, Wanqian Hu, Zhen-Min Li, Xinggang Li, Yanjin Xu, Yuan-Song Zeng, Zhi-Qiang Li, Xin-Ping Mao, Ming-Xing Zhang, Le-Hua Qi, Qiang Zhu, and Jian Lu. Strong yet ductile heat-resistant aluminum alloy by additive manufacturing. Nature Communications, Apr 2026. URL: https://doi.org/10.1038/s41467-026-71926-7, doi:10.1038/s41467-026-71926-7. This article has 11 citations and is from a highest quality peer-reviewed journal.

21. (guo2026mechanicalandin pages 1-3): Da Guo, Chengbo Zhu, Harry E. Chapman, Kai Zhang, Wei Li, Shishira Bhagavath, Robert Atwood, Stefan Michalik, Dmitry G. Eskin, Iakovos Tzanakis, Chu Lun Alex Leung, and Peter. D. Lee. Mechanical and in situ thermal-related behavior during directed energy deposition additive manufacturing of a high-performance al alloy. International Journal of Extreme Manufacturing, 8:035002, Jan 2026. URL: https://doi.org/10.1088/2631-7990/ae3349, doi:10.1088/2631-7990/ae3349. This article has 2 citations.

22. (mallia2026aiguidedselfdrivinglaboratories pages 6-12): Bernard Mallia and Rossana Caputo. Ai-guided self-driving laboratories for advanced materials discovery. Computing&amp;AI Connect, Aug 2026. URL: https://doi.org/10.69709/caic.2026.133382, doi:10.69709/caic.2026.133382. This article has 0 citations.

23. (mallia2026aiguidedselfdrivinglaboratories pages 12-17): Bernard Mallia and Rossana Caputo. Ai-guided self-driving laboratories for advanced materials discovery. Computing&amp;AI Connect, Aug 2026. URL: https://doi.org/10.69709/caic.2026.133382, doi:10.69709/caic.2026.133382. This article has 0 citations.

24. (zhao2026alloydesignparadigms pages 10-12): Li Zhao, Tianshu Liu, Hyoung Seop Kim, Tarasankar Debroy, Tomasz Kurzynowski, Konrad Gruber, Xiaowei Hu, and Chaolin Tan. Alloy design paradigms in additive manufacturing: a new era of material innovation. International Journal of Extreme Manufacturing, 8:033003, Mar 2026. URL: https://doi.org/10.1088/2631-7990/ae45de, doi:10.1088/2631-7990/ae45de. This article has 10 citations.

25. (brizes2026adispersionstrengthenedlowdensity pages 9-11): A Dispersion-Strengthened Low-Density Niobium Alloy and Its Elevated Temperature Mechanical Performance
