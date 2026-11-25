<!--
Edison Scientific LITERATURE task (batch 3)
- Task ID: 925abe7b-5acf-4953-8379-f19edb1a8e9f
- Submitted: 2026-10-17T05:46:03Z
- Fetched: 2026-10-17T06:16:51Z (status: success)
- Raw trajectory JSON: ../raw/b3-01-dmd-cuni-corrosion-details.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: Report the experimental details and results of S. Bhattacharya,
G. P. Dinda, A. K. Dasgupta, H. Natu, B. Dutta, J. Mazumder,
"Microstructural evolution and mechanical, and corrosion property evaluation
of Cu-30Ni alloy formed by direct metal deposition process", J. Alloys Compd.
509 (2011) 6364-6373 (doi:10.1016/j.jallcom.2011.03.091): powder source,
whether pre-alloyed, size, laser and nozzle, substrate, porosity, phases and
segregation, hardness and tensile data, and the corrosion test (electrolyte,
method, duration, values for deposit vs wrought C71500) and the stated cause
of any difference. Do the same, as far as available, for the companion
Cu-38Ni CO2 vs diode laser paper (J. Mater. Sci. 49 (2014) 2415), Adak et al.
2005 (laser cladding of Cu-30Ni), Karnati et al. 2019 (laser metal
deposition of Cu-Ni from blended powders, porosity linked to Ni powder
oxygen), Williams et al. 2025 (J. Manuf. Mater. Process. 9, 170, DED Cu-35Ni
single tracks), and Zhou et al. 2025 (Wear, laser-cladded Cu-Ni-xCr
coatings). Also identify the 2012 shipbuilding review by Andric et al. on
materials and fabrication that summarizes the 2011 study.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: Report the experimental details and results of S. Bhattacharya,
G. P. Dinda, A. K. Dasgupta, H. Natu, B. Dutta, J. Mazumder,
"Microstructural evolution and mechanical, and corrosion property evaluation
of Cu-30Ni alloy formed by direct metal deposition process", J. Alloys Compd.
509 (2011) 6364-6373 (doi:10.1016/j.jallcom.2011.03.091): powder source,
whether pre-alloyed, size, laser and nozzle, substrate, porosity, phases and
segregation, hardness and tensile data, and the corrosion test (electrolyte,
method, duration, values for deposit vs wrought C71500) and the stated cause
of any difference. Do the same, as far as available, for the companion
Cu-38Ni CO2 vs diode laser paper (J. Mater. Sci. 49 (2014) 2415), Adak et al.
2005 (laser cladding of Cu-30Ni), Karnati et al. 2019 (laser metal
deposition of Cu-Ni from blended powders, porosity linked to Ni powder
oxygen), Williams et al. 2025 (J. Manuf. Mater. Process. 9, 170, DED Cu-35Ni
single tracks), and Zhou et al. 2025 (Wear, laser-cladded Cu-Ni-xCr
coatings). Also identify the 2012 shipbuilding review by Andric et al. on
materials and fabrication that summarizes the 2011 study.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.


# Cu–Ni laser-deposition literature: verified results and limits

**Evidence limitation.** The 2011 Bhattacharya paper and several other requested primary papers were identifiable bibliographically but their full experimental text was not available in the retrieved material. Consequently, the requested numerical 2011 corrosion comparison **cannot be verified**. The strongest accessible account of its results is a 2012 shipbuilding review; the Williams 2025 paper was available in full. “Not verified” below means that a value should not be quoted as a benchmark, not that the original authors necessarily omitted it. (caprace2012specialistcommitteev. pages 16-17, williams2025thefirstlayer pages 2-4)

## 1. Bhattacharya et al., 2011 — closest marine-repair precedent

S. Bhattacharya, G. P. Dinda, A. K. Dasgupta, H. Natu, B. Dutta, and J. Mazumder, “Microstructural evolution and mechanical, and corrosion property evaluation of Cu-30Ni alloy formed by direct metal deposition process,” *Journal of Alloys and Compounds* **509** (2011), 6364–6373. DOI: **10.1016/j.jallcom.2011.03.091**. **[CITE] [NAVY: marine application, not verified Navy funding] [NOVELTY-RISK: Cu–30Ni laser deposition onto C71500 and direct corrosion comparison]**. The process was **CO₂-laser direct metal deposition**, identified as Cu–30Ni (nominal wt%) deposited on a *rolled/wrought C71500 plate*, rather than repair of cast NAB. Neither the powder’s manufacturer, pre-alloyed status and size nor the nozzle and laser settings can be established from the available account. (caprace2012specialistcommitteev. pages 16-17, caprace2012specialistcommitteev. pages 32-34)

The deposit’s **ultimate tensile strength was higher**, but its **yield strength and elongation were lower**, than those of the C71500 substrate. A separate review describes **lower, relatively uniform clad microhardness** compared with the substrate. The marine review reports porosity in the clad but gives **no defensible porosity fraction, hardness, yield strength, UTS, or elongation number**. Phases and elemental segregation likewise could not be verified. (caprace2012specialistcommitteev. pages 16-17, s2022reviewonsurface pages 11-12)

**Corrosion distinction:** the *standalone* DMD Cu–30Ni clad was **less corrosion-resistant than wrought C71500**; the review says performance **improved for the clad/C71500-substrate specimen**. It attributes the clad’s higher corrosion rate to **porosity in its deposited layers**. The retrieved account specifies **neither electrolyte nor electrochemical/immersion method, test duration or flow**, and gives **no numerical deposit-versus-wrought corrosion rate, corrosion-current density, corrosion potential, impedance, or selective-attack depth**. Thus this paper establishes a consequential *negative comparison*, **not** a verified numerical seawater pass criterion. [GAP: dense, as-deposited material must independently meet the wrought reference.] (caprace2012specialistcommitteev. pages 16-17)

## 2. Companion Cu–38Ni laser comparison

S. Bhattacharya, G. P. Dinda, A. K. Dasgupta, and J. Mazumder, “A comparative study of microstructure and mechanical behavior of CO₂ and diode laser deposited Cu–38Ni alloy,” *Journal of Materials Science* **49** (2014), 2415–2429. DOI: **10.1007/s10853-013-7883-7**. **[CITE] [NOVELTY-RISK: laser source/thermal history changes Cu–Ni deposit properties]**. This is **laser deposition** of nominal Cu–38Ni (wt%), comparing CO₂ and diode sources—not evidence of a new alloy designed for seawater. An accessible later paper reports **higher tensile properties** and a larger grain-size distribution for diode-laser deposits; CO₂ deposits were relatively **harder**, with less-uniform microhardness. Feedstock source/pre-alloying, size, substrate, nozzle, porosity, numerical strength/hardness, and corrosion electrolyte, duration and results **were not verified**; the identified paper concerns microstructure and mechanical behavior, not a demonstrated C71500 corrosion comparison. (kuklinski2018microstructureandselected pages 2-4, kuklinski2018microstructureandselected pages 13-13)

## 3. Adak et al., 2005 — early same-alloy cladding

B. Adak, P. Nash, D. Chen, and A. Swiglo, “Microstructural characterization of laser cladding of Cu-30Ni,” *Journal of Materials Science* **40** (2005), 2051–2054. DOI: **10.1007/s10853-005-1231-5**. **[CITE] [NOVELTY-RISK: Cu–30Ni-on-Cu–30Ni laser cladding predates the proposal] [GAP: no established long-duration marine-corrosion benchmark]**. Subsequent descriptions identify **diode-laser cladding** on the same Cu–30Ni alloy and report **crack-free, predominantly dendritic** clad with a thin **cellular-solidification region at the interface**. Whether powder was pre-alloyed, its source/size, nozzle, exact substrate certification, numeric porosity, hardness and strength, and any corrosion conditions or values **could not be verified**. A crack-free micrograph alone does not establish zero porosity. (kuklinski2018microstructureandselected pages 2-4, santhanakrishnan2011anexperimentallybased pages 1-2, kuklinski2018microstructureandselected pages 13-13)

## 4. Karnati et al., 2019 — distinguish the feedstock strategy

S. Karnati, F. F. Liou, and J. W. Newkirk, “Characterization of copper–nickel alloys fabricated using laser metal deposition and blended powder feedstocks,” *The International Journal of Advanced Manufacturing Technology* **103** (2019), 239–250. DOI: **10.1007/s00170-019-03553-0**. **[CITE] [NOVELTY-RISK: laser-metal-deposition Cu–Ni composition studies] [GAP: elemental blending does not validate one pre-alloyed powder feed]**. Its process is **laser metal deposition using blended Cu and Ni powders**, not single-stream deposition of individually pre-alloyed Cu–Ni particles. An accessible review reports approximately **4% deviation from designed to deposited composition** and use of **pulse-width-modulated laser power** to improve melt-pool homogenization; those observations should not be transferred quantitatively to pre-alloyed powder. (nemani2024advancementsinadditive pages 110-112, chen2020areviewon pages 10-13)

The question’s proposed link between **Ni-powder oxygen and porosity was not independently verifiable** from accessible text: no Ni-powder oxygen concentration, pore fraction, or experimental evidence for that specific causal attribution was recovered. Treat it as a **primary-paper verification item**, not a measured result established here. The actual composition series, substrates, feedstock size/flow, density, hardness, tensile results and corrosion conditions/values also remain unverified. (williams2025thefirstlayer pages 13-13, chen2020areviewon pages 10-13)

## 5. Williams et al., 2025 — quantitative *track*, not bulk-corrosion, benchmark

N. Williams, K. Snyder, I. Smith, A. Duong, E. Carpenter, and R. Barua, “The First Layer: Single-Track Insights into Direct Energy Deposition Processed Cu-Ni Thermoelectric Alloys,” *Journal of Manufacturing and Materials Processing* **9** (2025), 170. DOI: **10.3390/jmmp9060170**. **[CITE] [NUMBERS: powder and single-track process window] [NOVELTY-RISK: structured Cu–Ni DED process optimization already exists] [GAP: no pre-alloyed feed or marine bulk/repair validation]**. Critically, nominal **65Cu–35Ni wt%** was produced by tumbling **elemental** Oerlikon METCO 55 Cu (>99% purity) and METCO 56C-NS Ni (99.3%) for **8 h**. It was **not pre-alloyed powder**. A Precitec YC50 blown-powder head, **800 W** laser power and Ar carrier/shield gas produced isolated **single laser-DED tracks on 316L stainless steel**—not self-built multilayer Cu–Ni, NAB, or wrought Cu–Ni repair. (williams2025thefirstlayer pages 2-4)

Reported powder metrics were **57 ± 15 µm mean particle diameter**, **4.74 g/cm³ apparent density**, **5.20 g/cm³ tap density**, **1.10 Hausner ratio**, **0.3 g/s Hall flow**, and **27.42° angle of repose**. Linear powder input ranged **0.011–0.026 g/mm** and laser heat input **63–137 J/mm**. Its *qualitatively scored* favorable regions were **<70 J/mm at 0.016–0.021 g/mm** and **98–137 J/mm at 0.026 g/mm**; the authors describe approximately **4000 ± 500 kJ/g** energy per mass. At **0.016 g/mm and 67 J/mm**, a representative track stood approximately **500 µm high** with approximately **100 µm substrate penetration**. These are track-geometry observations, **not bulk relative-density or mechanical acceptance limits**. (williams2025thefirstlayer pages 4-6, williams2025thefirstlayer pages 6-9, williams2025thefirstlayer pages 9-11)

Low feed gave insufficient buildup and centerline cracking; at **0.021 g/mm** and **<100 J/mm**, incomplete elemental-Ni melting produced approximately **50 µm Ni-rich inclusions**. High feed caused excessive buildup and little substrate penetration. SEM/EDS maps visualize those inclusions and the change in Fe dilution; EBSD showed columnar grains. **No quantitative bulk porosity fraction, powder oxygen, corrosion test, seawater duration/flow, hardness, tensile result, or wrought-C71500 comparison was established**, and the authors explicitly did **not** measure thermoelectric properties. Figure-based evidence concerns cross-sections, not a corrosion performance claim. (williams2025thefirstlayer pages 6-9, williams2025thefirstlayer media b3f596ec, williams2025thefirstlayer media 1fee5c51, williams2025thefirstlayer pages 1-2)

## 6. Zhou et al., 2025 — Cr overlap requiring direct inspection

Y. Zhou, D. Wen, and X. Zuo, “Current-carrying fretting wear and electrochemical corrosion properties of laser-cladded Cu-Ni-xCr coatings,” *Wear* (2025), article **205960**. DOI: **10.1016/j.wear.2025.205960**. **[CITE] [NOVELTY-RISK: Cr-modified Cu–Ni *laser cladding plus electrochemical corrosion* is already claimed] [GAP: electrical-fretting coatings are not automatically as-deposited marine-repair alloys]**. The identifiable scope is **laser-cladded Cu–Ni–xCr coatings**, evaluated for electrical-contact fretting and electrochemical corrosion. Its full experimental results were unavailable: **x in wt%, powder architecture, substrate, processing conditions, hardness, porosity, chloride medium, duration/flow, *E*₍corr₎, *i*₍corr₎, impedance, wear and attack depth cannot be supplied responsibly**. In particular, a title containing “electrochemical corrosion” does **not** establish natural-seawater durability or equivalence to wrought C71500. Its DOI and title were identified bibliographically, but neither a quantitative result nor Navy funding was verified. [GAP] (nemani2024advancementsinadditive pages 102-105)

## 7. The 2012 shipbuilding review that recounts the 2011 result

ISSC **Committee V.3**, chaired by **Ingrid Schipperen**, with **Jerolim Andrić** among its members, “Materials and Fabrication Technology,” *Proceedings of the 18th International Ship and Offshore Structures Congress*, **vol. 2**, Rostock, 2012, pp. **113 onward**; the Bhattacharya summary is on **p. 128**, §3.3.2. **No DOI was verified for this committee report**. **[CITE] [NAVY: ship/offshore-structure application, not demonstrated US Navy sponsorship]**. It expressly identifies CO₂-laser Cu–30Ni deposition on rolled C71500, separates the standalone clad from the clad/substrate specimen in its corrosion comparison, and assigns the higher clad corrosion rate to porosity. It is a **secondary account**, not a source of numerical corrosion conditions. (caprace2012specialistcommitteev. pages 1-4, caprace2012specialistcommitteev. pages 16-17)

### Ranked: Top 5 things the PI should know

1. **Do not claim Cu–30Ni/C71500 DED is new—or that its corrosion already meets C71500.** The 2011 precedent exists, and the accessible shipbuilding synthesis says its standalone deposit performed *worse*, attributed to pores. Numerical rate and test conditions must be checked in the original article before inclusion in a proposal table. (caprace2012specialistcommitteev. pages 16-17)
2. **Make powder architecture an explicit novelty boundary.** Both Karnati 2019 and Williams 2025 used **blended elemental Cu/Ni**; Williams even visualized surviving ≈50 µm Ni particles. A characterized **single pre-alloyed powder per composition** addresses a materially different composition-control problem, although the claimed Ni-powder-oxygen mechanism still requires primary-source checking. (nemani2024advancementsinadditive pages 110-112, williams2025thefirstlayer pages 2-4, williams2025thefirstlayer pages 6-9, williams2025thefirstlayer pages 13-13)
3. **Measure the seawater objective directly on the *as-deposited* material and repair interface.** Report wrought-C71500 control and identical surface preparation, electrolyte identity, exposure time/flow, electrochemical results **and** long-immersion mass loss/local-attack depth. None of the accessible named studies establishes that combined pre-alloyed-feed, repair-substrate, as-deposited comparison; a favorable short polarization curve alone would not establish a 30-day outcome. (caprace2012specialistcommitteev. pages 16-17, nemani2024advancementsinadditive pages 102-105)
4. **Position Cu–Ni–Cr optimization against Zhou 2025 rather than ignoring it.** Its title already occupies Cr-containing laser-clad Cu–Ni with electrochemical testing; verify the primary paper’s **Cr levels and testing environment** before claiming novelty for Cr additions. Differentiate by pre-alloyed powder, lower-Ni formulation, marine-repair substrates, long seawater exposure and coupled model-guided search only where experimentally demonstrated. (nemani2024advancementsinadditive pages 102-105)
5. **Avoid conflating tracks, coatings, WAAM, LPBF and repair deposits.** Williams supplies excellent *elemental-blend/316L single-track* feed and heat-input numbers, **not** bulk density or seawater performance. Published copper-alloy reviews also show that NAB microstructure and performance depend strongly on AM route and subsequent heating; the proposed thermal-history-informed, no-post-treatment validation therefore needs explicit comparison with equilibrium-only and data-only predictions on actual DED builds. (williams2025thefirstlayer pages 2-4, williams2025thefirstlayer pages 9-11, nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 79-83)

References

1. (caprace2012specialistcommitteev. pages 16-17): JD Caprace, I Schipperen, J Andric, D Brennan, C Chou, J Gordo, J Lee, S Li, and S Liu. Specialist committee v. 3 entitled" materials and fabrication technology" of the 18th international ship and offshore structure congress. Unknown journal, 2012.

2. (williams2025thefirstlayer pages 2-4): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

3. (caprace2012specialistcommitteev. pages 32-34): JD Caprace, I Schipperen, J Andric, D Brennan, C Chou, J Gordo, J Lee, S Li, and S Liu. Specialist committee v. 3 entitled" materials and fabrication technology" of the 18th international ship and offshore structure congress. Unknown journal, 2012.

4. (s2022reviewonsurface pages 11-12): Pratheesh Kumar S, Anand K, Hari Chealvan S, and Karthikeya Muthu S. Review on surface characteristics of components produced by direct metal deposition process. Journal of Mechanical Engineering and Sciences, pages 9197-9229, Dec 2022. URL: https://doi.org/10.15282/jmes.16.4.2022.05.0729, doi:10.15282/jmes.16.4.2022.05.0729. This article has 7 citations.

5. (kuklinski2018microstructureandselected pages 2-4): Mateusz Kukliński, Aneta Bartkowska, and Damian Przestacki. Microstructure and selected properties of monel 400 alloy after laser heat treatment and laser boriding using diode laser. The International Journal of Advanced Manufacturing Technology, 98:3005-3017, Jul 2018. URL: https://doi.org/10.1007/s00170-018-2343-9, doi:10.1007/s00170-018-2343-9. This article has 51 citations.

6. (kuklinski2018microstructureandselected pages 13-13): Mateusz Kukliński, Aneta Bartkowska, and Damian Przestacki. Microstructure and selected properties of monel 400 alloy after laser heat treatment and laser boriding using diode laser. The International Journal of Advanced Manufacturing Technology, 98:3005-3017, Jul 2018. URL: https://doi.org/10.1007/s00170-018-2343-9, doi:10.1007/s00170-018-2343-9. This article has 51 citations.

7. (santhanakrishnan2011anexperimentallybased pages 1-2): Soundarapandian Santhanakrishnan, Fanrong Kong, and Radovan Kovacevic. An experimentally based thermo-kinetic hardening model for high power direct diode laser cladding. Journal of Materials Processing Technology, 211:1247-1259, Jul 2011. URL: https://doi.org/10.1016/j.jmatprotec.2011.02.006, doi:10.1016/j.jmatprotec.2011.02.006. This article has 91 citations and is from a domain leading peer-reviewed journal.

8. (nemani2024advancementsinadditive pages 110-112): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

9. (chen2020areviewon pages 10-13): Yitao Chen, Xinchang Zhang, Mohammad Masud Parvez, and Frank Liou. A review on metallic alloys fabrication using elemental powder blends by laser powder directed energy deposition process. Materials, 13:3562, Aug 2020. URL: https://doi.org/10.3390/ma13163562, doi:10.3390/ma13163562. This article has 79 citations.

10. (williams2025thefirstlayer pages 13-13): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

11. (williams2025thefirstlayer pages 4-6): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

12. (williams2025thefirstlayer pages 6-9): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

13. (williams2025thefirstlayer pages 9-11): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

14. (williams2025thefirstlayer media b3f596ec): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

15. (williams2025thefirstlayer media 1fee5c51): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

16. (williams2025thefirstlayer pages 1-2): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

17. (nemani2024advancementsinadditive pages 102-105): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

18. (caprace2012specialistcommitteev. pages 1-4): JD Caprace, I Schipperen, J Andric, D Brennan, C Chou, J Gordo, J Lee, S Li, and S Liu. Specialist committee v. 3 entitled" materials and fabrication technology" of the 18th international ship and offshore structure congress. Unknown journal, 2012.

19. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

20. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.
