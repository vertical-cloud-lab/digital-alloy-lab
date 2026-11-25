<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: ca860c2f-4b64-4ce6-b5d1-7863b5292af9
- Submitted: 2026-10-24T05:25:59Z
- Fetched: 2026-10-24T05:57:58Z (status: success)
- Raw trajectory JSON: not committed here (see ../README.md); r1-06-yip-program-and-pm.json.gz in the agent-staging drop
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal for the Materials &
Processes for Additive Manufacturing program (ONR Code 332). The work designs
new pre-alloyed copper alloy powders for single-stream blown-powder laser
directed energy deposition (DED). Goals: deposits that are dense and
crack-free, both built on themselves and deposited on cast nickel-aluminum
bronze (NAB) and wrought Cu-Ni (repair), and that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe, Mn, Cr; aluminum
bronzes / NAB with Ni, Fe, Mn. Lower nickel content is a secondary objective.
Powder is made in-house by ultrasonic atomization. Method: composition ->
powder -> DED deposit -> microstructure -> corrosion/hardness is a network of
linked models searched by cost-aware Bayesian optimization (cheap steps such
as CALPHAD, pre-placed powder tracks and one-hour electrochemical screens are
run more often than expensive ones such as 2 kg blown-powder builds and
30-day immersion). CALPHAD is evaluated along a heat-flow model of the DED
thermal history. Purchased DED sessions run at outside facilities.

QUESTION: The ONR Young Investigator Program is managed by Dr. Reginald G.
Williams (ONR Code 34). What is his published research background? Then,
from papers that acknowledge ONR Young Investigator Program grants, which
YIP-funded projects since 2015 dealt with additive manufacturing of metals,
alloy design, welding, or corrosion, and what did they emphasize
(fundamental mechanisms, Navy transition, new capabilities)? What does that
record suggest about how a materials YIP proposal should balance basic
science against Navy application?

OUTPUT FORMAT: First, a short profile built only from the published record
(papers, technical reports, conference talks, program pages): positions and
affiliations with years, main research topics, methods, and recurring
co-authors. Then the publications most relevant to the proposal, each with a
full citation and DOI and one line on what it found. Then 3-6 numbered
IMPLICATIONS for the proposal: what this reader is likely to value, what they
would probe or doubt, which of their own results the proposal should cite or
build on, and wording or framing that would land well or badly with them.
Tag claims that rest on a single source or on a program web page rather than
a peer-reviewed paper. If the record is thin or a name is ambiguous (several
people share it), say so plainly instead of guessing, and do not invent
affiliations, titles or papers.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal for the Materials &
Processes for Additive Manufacturing program (ONR Code 332). The work designs
new pre-alloyed copper alloy powders for single-stream blown-powder laser
directed energy deposition (DED). Goals: deposits that are dense and
crack-free, both built on themselves and deposited on cast nickel-aluminum
bronze (NAB) and wrought Cu-Ni (repair), and that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe, Mn, Cr; aluminum
bronzes / NAB with Ni, Fe, Mn. Lower nickel content is a secondary objective.
Powder is made in-house by ultrasonic atomization. Method: composition ->
powder -> DED deposit -> microstructure -> corrosion/hardness is a network of
linked models searched by cost-aware Bayesian optimization (cheap steps such
as CALPHAD, pre-placed powder tracks and one-hour electrochemical screens are
run more often than expensive ones such as 2 kg blown-powder builds and
30-day immersion). CALPHAD is evaluated along a heat-flow model of the DED
thermal history. Purchased DED sessions run at outside facilities.

QUESTION: The ONR Young Investigator Program is managed by Dr. Reginald G.
Williams (ONR Code 34). What is his published research background? Then,
from papers that acknowledge ONR Young Investigator Program grants, which
YIP-funded projects since 2015 dealt with additive manufacturing of metals,
alloy design, welding, or corrosion, and what did they emphasize
(fundamental mechanisms, Navy transition, new capabilities)? What does that
record suggest about how a materials YIP proposal should balance basic
science against Navy application?

OUTPUT FORMAT: First, a short profile built only from the published record
(papers, technical reports, conference talks, program pages): positions and
affiliations with years, main research topics, methods, and recurring
co-authors. Then the publications most relevant to the proposal, each with a
full citation and DOI and one line on what it found. Then 3-6 numbered
IMPLICATIONS for the proposal: what this reader is likely to value, what they
would probe or doubt, which of their own results the proposal should cite or
build on, and wording or framing that would land well or badly with them.
Tag claims that rest on a single source or on a program web page rather than
a peer-reviewed paper. If the record is thin or a name is ambiguous (several
people share it), say so plainly instead of guessing, and do not invent
affiliations, titles or papers.


## Published-record profile

**Reginald G. Williams.** The question identifies Williams as manager of ONR’s Young Investigator Program in Code 34. The publication record located here does **not** establish his earlier positions or their dates, research topics, methods, recurring co-authors, or authorship of a materials-science paper. An indexed 2017 conference presentation under “Reginald Williams” concerns ONR science and technology, but its text was unavailable for verification; a publication under that name alone cannot safely be assigned to this official. **[Record too thin to infer a research background.]** In particular, the YIP-funded papers below are *awardees’ research*, not Williams’s results. One corrosion publication expressly names **Dr. Airan Perez**, rather than Williams, as manager of its YIP award. (schrock2019theeffectsof pages 8-8)

## Publications most relevant to the proposal

The following are **distinct award lines**, not a claim that all metal-AM or corrosion work funded by ONR was YIP-funded. The cited papers acknowledge the indicated awards; their aims illustrate fundamental mechanisms and enabling capabilities more directly than a demonstrated Navy transition.

- **Alloy-model capability — YIP N00014-16-1-2621.** Xiang-Guo Li, Chongze Hu, Chi Chen, Zhi Deng, Jian Luo, and Shyue Ping Ong, “Quantum-Accurate Spectral Neighbor Analysis Potential Models for Ni-Mo Binary Alloys and FCC Metals,” *Physical Review B* **98** (2018), 094104. DOI: **10.1103/PhysRevB.98.094104**. The paper explicitly acknowledges ONR YIP support; its learned Ni–Mo potential reproduced phase-diagram behavior substantially better than the comparison EAM potential, providing an atomistic modeling capability—not a seawater-corrosion demonstration. (li2018quantumaccuratespectralneighbor pages 15-19, li2018quantumaccuratespectralneighbor pages 1-4)

- **Marine corrosion mechanism — YIP N00014-16-1-2756.** D. J. Schrock and J. S. (Warner) Locke, “The Effects of Loading Frequency, Sensitization, and Crack Length on Corrosion Fatigue of AA5456-H116,” *CORROSION* **76** (2020), 63–70. DOI: **10.5006/3366**. In immersed NaCl, heavily sensitized aluminum showed faster fatigue-crack growth at lower loading frequency; crack length did not explain that dependence. The paper explicitly calls its ONR funding a Young Investigator Award managed by Perez. This is an example of a **service-motivated question resolved through mechanism-sensitive testing**, not a report of field qualification. (schrock2019theeffectsof pages 1-2, schrock2019theeffectsof pages 8-8)

- **Metal-AM processing and cracking capability — YIP N00014-22-1-2420.** Poulomi Mukherjee, Ashlee Gabourel, Samad A. Firdosy, Douglas C. Hofmann, and Atieh Moridi, “Additive Manufacturing of Refractory Metals and Carbides for Extreme Environments: An Overview,” *Science and Technology of Welding and Joining* **29** (2024), 99–115. DOI: **10.1177/13621718241235471**. This **review**, which acknowledges Moridi’s ONR Young Investigator Award, organizes cracking around brittle oxides, high ductile-to-brittle transition temperatures, and process-induced microstructures, then evaluates possible processing remedies; it is not itself proof that every reviewed remedy was developed under that award. (mukherjee2024additivemanufacturingof pages 11-12)

- **Metal-AM alloy formation — the same Moridi YIP award, not a fourth project.** Chenxi Tian, Kaushalendra Singh, Akane Wakai, Adrita Dass, Jenniffer Bustillos, Andrew C. Chuang, and Atieh Moridi, “Tunable TiAl3-Reinforced Aluminum Matrix Composites via In-Situ Reactive Printing: Insights from Operando Synchrotron Analysis and Microstructural Characterization,” *npj Advanced Manufacturing* **2** (2025). DOI: **10.1038/s44334-024-00014-9**. The paper acknowledges ONR Young Investigator award N00014-22-1-2420; it uses reactive Al–Ti printing and operando observations to connect formation of TiAl₃ reinforcement with grain refinement and strengthening. Its feedstock and process differ materially from single-stream pre-alloyed Cu-alloy DED. (tian2025tunabletial3reinforcedaluminum pages 1-2, tian2025tunabletial3reinforcedaluminum pages 13-14)

**Important comparator, not YIP:** Xin Wang and Wei Xiong, “Uncertainty Quantification and Composition Optimization for Alloy Additive Manufacturing through a CALPHAD-Based ICME Framework,” *npj Computational Materials* **6** (2020). DOI: **10.1038/s41524-020-00454-9**. Their HSLA-steel study screened 450,000 compositions and predicted improved probability of meeting strength, toughness, and weldability requirements under powder-composition uncertainty. Its acknowledged ONR support was **AMANE N00014-17-1-2586**, not a verified YIP award; cite it for the technical precedent, not as evidence of YIP selection. (wang2020uncertaintyquantificationand pages 16-24, wang2020uncertaintyquantificationand pages 7-10, wang2020uncertaintyquantificationand pages 1-4)

The search did **not** verify a separate welding-only YIP project or a YIP paper demonstrating as-deposited Cu–Ni/NAB repair that meets a wrought C71500 seawater benchmark. Nor does this small, acknowledgment-verified sample establish an exhaustive history of ONR materials YIP awards.

## IMPLICATIONS

1. **Lead with a generalizable scientific question, then state the naval test.** A defensible formulation is: *How do powder-composition uncertainty and DED thermal history jointly determine segregation, cracking, interfacial integrity, and corrosion of as-deposited copper alloys?* State cast-NAB and wrought-Cu–Ni repair and the C71500 comparator as demanding validation conditions. The retrieved YIP examples couple mechanism to an application; they do not justify portraying a proposed repair as already transition-ready. **[Inference from the awardee papers, not evidence of Williams’s personal preference.]** (li2018quantumaccuratespectralneighbor pages 15-19, tian2025tunabletial3reinforcedaluminum pages 1-2, schrock2019theeffectsof pages 1-2)

2. **Make each model link falsifiable.** Explain what CALPHAD evaluated along the predicted thermal history will—and will not—predict; measure actual atomized-powder composition, deposited phases and segregation, cracking, and model uncertainty. Wang and Xiong provide the closest *non-YIP* precedent for composition uncertainty and weldability-aware screening; their paper itself identifies database and model-quality limitations. A claim that CALPHAD alone establishes crack-free, corrosion-resistant DED would land badly. (wang2020uncertaintyquantificationand pages 16-24, wang2020uncertaintyquantificationand pages 7-10, wang2020uncertaintyquantificationand pages 10-13)

3. **Treat cheap screens as triage, not substitutes for qualification.** Specify how pre-placed tracks and one-hour electrochemistry predict—or fail to predict—blown-powder builds, substrate interfaces, and longer seawater exposure. Reserve purchased DED sessions and extended immersion for prespecified decisions, with replication and comparison of **as-deposited** specimens to wrought C71500. The corrosion YIP example shows why service-relevant loading or exposure can change an apparently favorable ranking. **[Cross-system inference: its data concern sensitized Al–Mg, not Cu alloys.]** (akman2021corrosionfatigueperformance pages 1-7, schrock2019theeffectsof pages 1-2, schrock2019theeffectsof pages 8-8)

4. **Position the deliverable as a capability plus validated physical insight.** The record supports proposals that produce transferable alloy/process-design rules, calibrated measurements, and a credible route to Navy-relevant repair—not merely a Bayesian-optimization workflow or a lowest-Ni recipe. Distinguish deposition on itself from deposition onto each dissimilar substrate, and make lower Ni subordinate to density, sound interfaces, and as-deposited seawater performance. **[Proposal inference, not a stated ONR selection criterion.]** (li2018quantumaccuratespectralneighbor pages 15-19, mukherjee2024additivemanufacturingof pages 11-12, schrock2019theeffectsof pages 1-2)

5. **Do not personalize the pitch to an unverified bibliography.** Cite Li *et al.* for alloy-potential methodology, Schrock–Locke for the value of service-relevant corrosion mechanisms, and Wang–Xiong for uncertainty-aware AM alloy selection—but do **not** call any of these “Williams’s own results” or mislabel AMANE as YIP. The available published evidence cannot support predictions about what Williams individually will probe or prefer. (wang2020uncertaintyquantificationand pages 16-24, li2018quantumaccuratespectralneighbor pages 15-19, schrock2019theeffectsof pages 8-8)

References

1. (schrock2019theeffectsof pages 8-8): D.J. Schrock and J.S. (Warner) Locke. The effects of loading frequency, sensitization, and crack length on corrosion fatigue of aa5456-h116. Corrosion, 76:63-70, Nov 2019. URL: https://doi.org/10.5006/3366, doi:10.5006/3366. This article has 13 citations and is from a peer-reviewed journal.

2. (li2018quantumaccuratespectralneighbor pages 15-19): Xiang-Guo Li, Chongze Hu, Chi Chen, Zhi Deng, Jian Luo, and Shyue Ping Ong. Quantum-accurate spectral neighbor analysis potential models for ni-mo binary alloys and fcc metals. Physical Review B, Sep 2018. URL: https://doi.org/10.1103/physrevb.98.094104, doi:10.1103/physrevb.98.094104. This article has 181 citations and is from a domain leading peer-reviewed journal.

3. (li2018quantumaccuratespectralneighbor pages 1-4): Xiang-Guo Li, Chongze Hu, Chi Chen, Zhi Deng, Jian Luo, and Shyue Ping Ong. Quantum-accurate spectral neighbor analysis potential models for ni-mo binary alloys and fcc metals. Physical Review B, Sep 2018. URL: https://doi.org/10.1103/physrevb.98.094104, doi:10.1103/physrevb.98.094104. This article has 181 citations and is from a domain leading peer-reviewed journal.

4. (schrock2019theeffectsof pages 1-2): D.J. Schrock and J.S. (Warner) Locke. The effects of loading frequency, sensitization, and crack length on corrosion fatigue of aa5456-h116. Corrosion, 76:63-70, Nov 2019. URL: https://doi.org/10.5006/3366, doi:10.5006/3366. This article has 13 citations and is from a peer-reviewed journal.

5. (mukherjee2024additivemanufacturingof pages 11-12): Poulomi Mukherjee, Ashlee Gabourel, Samad A. Firdosy, Douglas C. Hofmann, and Atieh Moridi. Additive manufacturing of refractory metals and carbides for extreme environments: an overview. Science and Technology of Welding and Joining, 29:99-115, Mar 2024. URL: https://doi.org/10.1177/13621718241235471, doi:10.1177/13621718241235471. This article has 30 citations and is from a peer-reviewed journal.

6. (tian2025tunabletial3reinforcedaluminum pages 1-2): Chenxi Tian, Kaushalendra Singh, Akane Wakai, Adrita Dass, Jenniffer Bustillos, Andrew C. Chuang, and Atieh Moridi. Tunable tial3-reinforced aluminum matrix composites via in-situ reactive printing: insights from operando synchrotron analysis and microstructural characterization. npj Advanced Manufacturing, Feb 2025. URL: https://doi.org/10.1038/s44334-024-00014-9, doi:10.1038/s44334-024-00014-9. This article has 6 citations.

7. (tian2025tunabletial3reinforcedaluminum pages 13-14): Chenxi Tian, Kaushalendra Singh, Akane Wakai, Adrita Dass, Jenniffer Bustillos, Andrew C. Chuang, and Atieh Moridi. Tunable tial3-reinforced aluminum matrix composites via in-situ reactive printing: insights from operando synchrotron analysis and microstructural characterization. npj Advanced Manufacturing, Feb 2025. URL: https://doi.org/10.1038/s44334-024-00014-9, doi:10.1038/s44334-024-00014-9. This article has 6 citations.

8. (wang2020uncertaintyquantificationand pages 16-24): Xin Wang and Wei Xiong. Uncertainty quantification and composition optimization for alloy additive manufacturing through a calphad-based icme framework. npj Computational Materials, Dec 2020. URL: https://doi.org/10.1038/s41524-020-00454-9, doi:10.1038/s41524-020-00454-9. This article has 86 citations and is from a peer-reviewed journal.

9. (wang2020uncertaintyquantificationand pages 7-10): Xin Wang and Wei Xiong. Uncertainty quantification and composition optimization for alloy additive manufacturing through a calphad-based icme framework. npj Computational Materials, Dec 2020. URL: https://doi.org/10.1038/s41524-020-00454-9, doi:10.1038/s41524-020-00454-9. This article has 86 citations and is from a peer-reviewed journal.

10. (wang2020uncertaintyquantificationand pages 1-4): Xin Wang and Wei Xiong. Uncertainty quantification and composition optimization for alloy additive manufacturing through a calphad-based icme framework. npj Computational Materials, Dec 2020. URL: https://doi.org/10.1038/s41524-020-00454-9, doi:10.1038/s41524-020-00454-9. This article has 86 citations and is from a peer-reviewed journal.

11. (wang2020uncertaintyquantificationand pages 10-13): Xin Wang and Wei Xiong. Uncertainty quantification and composition optimization for alloy additive manufacturing through a calphad-based icme framework. npj Computational Materials, Dec 2020. URL: https://doi.org/10.1038/s41524-020-00454-9, doi:10.1038/s41524-020-00454-9. This article has 86 citations and is from a peer-reviewed journal.

12. (akman2021corrosionfatigueperformance pages 1-7): AM Akman. Corrosion fatigue performance of in-service and laboratory accelerated sensitized aa5456-h116 for marine applications. Unknown journal, 2021.
