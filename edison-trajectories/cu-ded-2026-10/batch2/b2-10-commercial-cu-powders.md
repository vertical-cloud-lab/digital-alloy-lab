<!--
Edison Scientific LITERATURE task (batch 2)
- Task ID: 01090695-cefa-423d-b504-06ede2b4db8a
- Submitted: 2026-10-17T05:37:07Z
- Fetched: 2026-10-17T06:09:01Z (status: success)
- Raw trajectory JSON: ../raw/b2-10-commercial-cu-powders.json.gz
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

QUESTION: What is published about commercial gas-atomized Cu-Ni (90-10,
70-30) and NAB powders for AM: suppliers, size cuts offered for DED versus
LPBF, typical oxygen content, flow and apparent density, and minimum order or
lot sizes for custom compositions from industrial gas atomizers? Which
peer-reviewed studies characterized these powders before printing, and what
do studies of powder reuse in DED or LPBF report for copper alloys
(oxidation, satellites, size shift, effect on porosity)? Cite sources for any
minimum lot size; if only vendor pages state it, say so.

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

QUESTION: What is published about commercial gas-atomized Cu-Ni (90-10,
70-30) and NAB powders for AM: suppliers, size cuts offered for DED versus
LPBF, typical oxygen content, flow and apparent density, and minimum order or
lot sizes for custom compositions from industrial gas atomizers? Which
peer-reviewed studies characterized these powders before printing, and what
do studies of powder reuse in DED or LPBF report for copper alloys
(oxidation, satellites, size shift, effect on porosity)? Cite sources for any
minimum lot size; if only vendor pages state it, say so.

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


# Commercial Cu–Ni and nickel–aluminium-bronze powder for AM: evidence audit

**Bottom line.** The retrieved literature establishes useful *research-scale* powder and reuse benchmarks, but it does **not** establish a verified commercial specification or minimum custom-atomization order for gas-atomized Cu–10Ni, Cu–30Ni, or nickel–aluminium bronze (NAB). In particular, a process’s usual particle-size range is not proof that a named supplier offers that alloy in that cut. No retrieved source supports assigning these three powders a “typical” bulk oxygen content, Hall flow, apparent density, or minimum lot size. **No numerical minimum order or lot size is asserted here:** none could be traced to a citable vendor page, quotation, or peer-reviewed source. [GAP] (sun2024characterizationpreparationand pages 5-6)

## Verified powder and reuse measurements

The following comparison separates measurements on the *requested alloys* from measurements on other copper-containing feedstocks. None of these powder-focused experiments reports seawater corrosion, so corrosion current, *E*cor­r, impedance, selective-attack depth, hardness, and tensile results are **not applicable to their powder comparisons**, rather than missing values that can be inferred. (roth2024establishingaprocess pages 5-7, alistair2022chemicalrecoveryof pages 7-9)

| Feedstock / study | Process and composition (wt%) | Pre-print powder particle size | Oxygen, flow, apparent density | Limits |
|---|---|---|---|---|
| Roth et al. (2024), *Establishing a process route for additive manufacturing of NiCu-based Alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments*. DOI: [10.1007/s00170-024-14328-7](https://doi.org/10.1007/s00170-024-14328-7) (roth2024establishingaprocess pages 5-7, roth2024establishingaprocess pages 7-9) | LPBF; gas-atomized Ni-majority Alloy 400: Ni 63.2, Cu 31.6, Fe 1.9, Mn 1.0 (wet chemical analysis) | D10 28.9 µm; D50 42.3 µm; D90 61.5 µm; final classified fraction 15–63 µm | Oxygen: unreported; Hall flow: 15.22 s/50 g; apparent/bulk density: 4.38 g/cm³ | **Not** Cu–30Ni (70–30 Cu–Ni): this is approximately Ni–32Cu. Mostly spherical, with sporadic satellites/agglomerates; no detected internal gas porosity or impurity. Best reported LPBF optical relative density: 99.94%. |
| Speidel et al. (2022), *Chemical recovery of spent copper powder in laser powder bed fusion*. DOI: [10.1016/j.addma.2022.102711](https://doi.org/10.1016/j.addma.2022.102711) (alistair2022chemicalrecoveryof pages 2-3, alistair2022chemicalrecoveryof pages 5-6, alistair2022chemicalrecoveryof pages 7-9) | LPBF; ECKA gas-atomized nominally pure Cu; virgin versus powder recovered after 12 builds | Supplier maximum ≤45 µm; virgin D50 7.3 µm, mean 9.4 µm; spent D50 7.9 µm, mean 11.6 µm; acid-deoxidized spent D50 10.6 µm, mean 14.3 µm | Surface EDS oxygen: virgin 2.13 ± 0.75 at%; spent 17.50 ± 6.92 at%; deoxidized 2.71 ± 0.70 at%. These are **not bulk oxygen values**. Flow and apparent density: unreported. | Spent powder shifted slightly coarser because of spatter agglomerates and partial fusion. Spent-powder tracks had extensive porosity; acid treatment reduced it toward virgin-powder behavior, but no quantitative porosity percentage was reported. This is pure Cu, not Cu–Ni or NAB. |
| Sun et al. (2024), *Characterization, preparation, and reuse of metallic powders for laser powder bed fusion: a review*. DOI: [10.1088/2631-7990/acfbc3](https://doi.org/10.1088/2631-7990/acfbc3) (sun2024characterizationpreparationand pages 5-6) | General review; not alloy- or supplier-specific | Typical DED range: approximately 50–150 µm; typical LPBF range: approximately 20–45 µm | No Cu–Ni/NAB-specific oxygen, Hall flow, or apparent-density values | These are general process ranges, **not verified commercial size offerings**. No direct repeated-reuse experiment for Cu–10Ni, Cu–30Ni, or NAB was identified in this source. |


*Table: Only directly verified quantitative evidence is included. No verified vendor minimum-order quantity or commercial certificate data for Cu–10Ni, Cu–30Ni, or NAB powder—including lot-specific oxygen, Hall flow, apparent density, and offered size cuts—were found in the retrieved sources.*

1. **Roth, Jan-Philipp; Šulák, Ivo; Kruml, Tomáš; Polkowski, Wojciech; Dudziak, Tomasz; Böhlke, Peter; Krupp, Ulrich; and Jahns, Katrin. “Establishing a process route for additive manufacturing of NiCu-based Alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments.” *The International Journal of Advanced Manufacturing Technology* 134 (2024): 3433–3452. DOI: 10.1007/s00170-024-14328-7.** **Process:** in-house gas atomization followed by LPBF, **not** blown-powder DED. **Powder composition, wt% by wet chemical analysis:** Ni 63.2, Cu 31.6, Fe 1.9, Mn 1.0, Si 0.2, Al 0.2. Approximately 10 kg of bulk Alloy 400 was atomized in one reported experimental run; this is **not an industrial supplier’s minimum order**. The classified LPBF fraction was 15–63 µm; measured D10/D50/D90 were 28.9/42.3/61.5 µm, Hall flow was 15.22 s/50 g, and powder apparent/bulk density was 4.38 g/cm³. Particles were mostly spherical with occasional satellites; powder oxygen was not reported. One LPBF condition yielded 99.94% *optical* relative density, whereas another condition at a similar nominal volumetric energy density yielded 97.26%. **Critical qualification:** this is **Ni-majority Alloy 400**, not C71500 or any other Cu-majority 70–30 Cu–Ni. **Corrosion testing:** none reported in the powder/printing results cited here. [CITE] [NUMBERS] [GAP] (roth2024establishingaprocess pages 2-4, roth2024establishingaprocess pages 5-7, roth2024establishingaprocess pages 7-9, roth2024establishingaprocess media 4fc8da04)

2. **Speidel, Alistair; Gargalis, Leonidas; Ye, Jianchao; Matthews, Manyalibo J.; Spierings, Adriaan; Hague, Richard; Clare, Adam T.; and Murray, James W. “Chemical recovery of spent copper powder in laser powder bed fusion.” *Additive Manufacturing* 52 (2022): 102711. DOI: 10.1016/j.addma.2022.102711.** **Process/composition:** LPBF, nominally pure gas-atomized **Cu**, not Cu–Ni or NAB; the virgin powder is identified as ECKA Granules Cu. Spent powder was recovered near the gas outlet after **12 build cycles** and sieved below 45 µm. Virgin versus spent D50 increased from **7.3 to 7.9 µm** (means **9.4 to 11.6 µm**); agglomerated spatter and partial particle fusion contributed to the coarser distribution. Oxygen by **EDS**, an interaction-volume measurement rather than a bulk oxygen assay, was **2.13 ± 0.75 versus 17.50 ± 6.92 atomic%** for virgin versus spent powder; after 20 minutes’ chemical deoxidation, it was **2.71 ± 0.70 atomic%**. XPS interrogated a shallower surface region and must not be substituted for either EDS or bulk wt% oxygen. Spent-powder single tracks showed extensive porosity; deoxidation markedly reduced it toward virgin-track behavior, but the cited results provide **no defensible numerical part-porosity percentage**. The comparison used single LPBF tracks on Cu discs under Ar, rather than full DED repair builds; no seawater exposure or corrosion metric was reported. [CITE] [NUMBERS] [GAP] (alistair2022chemicalrecoveryof pages 3-5, alistair2022chemicalrecoveryof pages 2-3, alistair2022chemicalrecoveryof pages 5-6, alistair2022chemicalrecoveryof pages 7-9)

3. **Sun, Xiaoyu; Chen, Minan; Liu, Tingting; Zhang, Kai; Wei, Huiliang; Zhu, Zhiguang; and Liao, Wenhe. “Characterization, preparation, and reuse of metallic powders for laser powder bed fusion: a review.” *International Journal of Extreme Manufacturing* 6 (2024): 012003. DOI: 10.1088/2631-7990/acfbc3.** **Process/composition:** cross-alloy powder review, not a Cu–Ni or NAB experiment. Its approximate **50–150 µm for DED** and **20–45 µm for LPBF** are *general process ranges*, **not supplier offerings**. Powder-size distribution, shape, flow, and reuse history can alter packing and defect formation; the review explicitly notes that reuse trends depend on alloy and powder-handling protocol. It does not establish an oxygen threshold or safe reuse-cycle count for Cu–Ni or NAB. [CITE] [NUMBERS] [GAP] (sun2024characterizationpreparationand pages 3-5, sun2024characterizationpreparationand pages 5-6)

## Directly relevant studies requiring full-text verification

These are **publication leads, not sources of verified supplier specifications or extracted test numbers**. Their titles and DOIs identify direct prior-art risks; their full articles were unavailable in this search. Consequently, powder manufacturer, gas-atomized status, pre-print PSD/oxygen/flow/apparent density, as-built porosity, corrosion electrolyte and exposure duration, and mechanical values **cannot be supplied responsibly from them**.

- **Rayner, A. J.; Morshedbehbahani, K.; Spence, C.; Wood, G.; Hamre, D.; Nasiri, A.; and Bishop, D. P. “Directed energy deposition of UNS C63020 nickel aluminum bronze powder.” In *Proceedings of the 63rd Conference of Metallurgists, COM 2024* (2024): 53–58. DOI: 10.1007/978-3-031-67398-6_13.** **Process:** powder DED; **alloy:** UNS C63020 NAB; precise measured wt% and powder tests unverified here. The publication is a conference proceeding, **not verified here as a peer-reviewed journal article**. Its direct pre-alloyed NAB-powder DED subject is a **[NOVELTY-RISK]**; whether it studies corrosion, repair interfaces, or powder qualification remains unverified. [CITE] [NOVELTY-RISK] [GAP]
- **Rayner, A. J.; Hierlihy, J.; Trask, M.; Cooke, R. W.; and Bishop, D. P. “Laser powder bed fusion processing of UNS C63020 nickel aluminum bronze powder.” *Progress in Additive Manufacturing* 10 (2025): 427–449. DOI: 10.1007/s40964-024-00633-w.** **Process:** LPBF; **alloy:** UNS C63020 NAB. This is a peer-reviewed, direct powder-characterization lead, but numerical powder and build properties could not be verified from its unavailable text. LPBF findings must not be presented as DED performance. [CITE] [NOVELTY-RISK] [GAP]
- **Liu, Zhuangzhuang; Zhang, Qianwen; Zhang, Bowei; Wang, Yixuan; Zuo, Pengcheng; Zhang, Zequn; Wu, Junsheng; Yan, Xiongbo; Huang, Yizhong; and Li, Xiaogang. “Investigation on mechanical properties and corrosion behavior of laser powder bed fusion 70/30 copper-nickel alloy.” *Corrosion Science* (2024). DOI: 10.1016/j.corsci.2024.112040.** **Process/composition:** LPBF Cu–30Ni nominally, **not DED**. Directly threatens a claim that *as-built 70–30 Cu–Ni corrosion has not been studied*, but its precise powder specification, NaCl/seawater conditions, corrosion values, and treatment state could not be checked. [CITE] [NOVELTY-RISK] [GAP]
- **Roshan, Mojtaba; Mahtabi, MohammadBagher; Bednarczyk, Wiktor; Gajewska, Marta; Cios, Grzegorz; Mahbooba, Zaynab; Saharan, Ankit; and Haghshenas, Meysam. “Powder bed fused–laser beam (PBF-LB) 70/30 copper-nickel (Cu-30Ni): hierarchical microstructure and mechanical properties.” *Journal of Alloys and Compounds* (2025). DOI: 10.1016/j.jallcom.2025.183312.** **Process/composition:** LPBF, nominal Cu–30Ni. It is direct precedent on the alloy, but neither pre-print powder numbers nor part-property values were accessible for verification. [CITE] [NOVELTY-RISK] [GAP]

A reviewed NAB-AM literature inventory also records LPBF studies on nominal **C63000 (Cu–10.2Al–4.8Fe–5.0Ni–0.2Si)** and **C95800 (Cu–9.0Al–4.0Fe–4.6Ni–1.9Mn)**, including a **675 °C/6 h post-treatment** entry. Those compositions and treatment details are from **Nemani, Alireza Vahedi; Ghaffari, Mahya; Bokati, Kazem Sabet; Valizade, Nima; Afshari, Elham; and Nasiri, Ali. “Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review.” *Journal of Manufacturing and Materials Processing* 8 (2024): 54. DOI: 10.3390/jmmp8020054**; they are *not* evidence of as-deposited seawater resistance or commercial powder specifications. Its separate WAAM and laser-DED entries must not be counted as powder-DED characterizations without checking the primary feedstock description. [CITE] [NOVELTY-RISK] [GAP] (nemani2024advancementsinadditive pages 60-62, nemani2024advancementsinadditive pages 62-68)

## Commercial and reuse questions still unanswered

**Suppliers and custom lots.** ECKA is attributable to the **pure-Cu powder actually used** by Speidel and colleagues; that does **not** verify an ECKA Cu–Ni or NAB catalogue product. Roth and colleagues atomized Alloy 400 themselves, so their approximately 10 kg research melt is **neither a custom-powder vendor quote nor an MOQ**. No attributable commercial listing or certificate was retrieved for the requested Cu–10Ni, Cu–30Ni, or NAB in distinct DED and LPBF cuts. Supplier names, offered cuts, custom-composition minimum melts/orders, delivered usable yield per cut, and lot-certified **bulk** oxygen, Hall flow, and apparent density therefore remain open procurement questions. Any eventual minimum should be cited to its specific vendor page or quotation and labeled **vendor-stated**, not peer-reviewed. [GAP] (alistair2022chemicalrecoveryof pages 2-3, roth2024establishingaprocess pages 2-4, sun2024characterizationpreparationand pages 5-6)

**Alloy-specific reuse.** The directly verified copper reuse experiment above concerns **pure Cu in LPBF**, not repeated recycling of Cu–10Ni, Cu–30Ni, or NAB in blown-powder DED. It supports a *hazard to test*—oxidation and spatter-related size/morphology changes can accompany much greater track porosity—but supplies **no quantitative reuse limit for the proposed alloys or DED process**. It also shows why surface-sensitive EDS/XPS oxygen figures cannot serve as acceptance limits for a lot’s measured bulk oxygen wt%. [GAP] (alistair2022chemicalrecoveryof pages 5-6, alistair2022chemicalrecoveryof pages 7-9, sun2024characterizationpreparationand pages 5-6)

**Seawater and Navy relevance.** These powder studies provide **no matched natural-seawater, ASTM D1141 substitute-seawater, or 3.5 wt% NaCl exposure series** and no 30-day, flow-controlled comparison with as-deposited and wrought C71500. No Navy/DoD funding is established by the verified powder-study passages; a marine-use alloy or repair application alone does not substantiate a **[NAVY]** funding designation. Thus no powder or reuse datum here establishes the proposal’s seawater-performance target. [GAP] (roth2024establishingaprocess pages 5-7, alistair2022chemicalrecoveryof pages 7-9, nemani2024advancementsinadditive pages 62-68)

## Top 5 things the PI should know

1. **Do not claim novelty for “NAB powder DED” or “AM 70–30 Cu–Ni corrosion” in isolation.** The Rayner DED proceeding and Liu LPBF corrosion study are direct prior-art leads. Distinguish *new pre-alloyed compositions, measured powder-to-deposit links, cast-NAB/wrought-Cu–Ni repair, and as-deposited long-duration seawater performance* instead. [NOVELTY-RISK] [GAP] (nemani2024advancementsinadditive pages 62-68)
2. **Obtain primary supplier documentation before budgeting custom gas atomization.** No source found supports a numerical custom-alloy MOQ or a commercial Cu–Ni/NAB DED-versus-LPBF product matrix; Roth’s ~10 kg experimental atomization run is not one. [GAP] (roth2024establishingaprocess pages 2-4)
3. **Specify and measure powder properties by lot rather than borrowing Alloy 400 values.** Its excellent documented Hall flow, apparent density, and LPBF density are useful characterization exemplars, but it contains **63.2 wt% Ni**, opposite the proposal’s low-Ni Cu-majority objective. [CITE] [NUMBERS] (roth2024establishingaprocess pages 5-7, roth2024establishingaprocess pages 7-9)
4. **Treat reuse and oxidation as experimentally coupled process variables.** Pure-Cu LPBF powder recovered after 12 builds was more oxidized by EDS, shifted modestly coarser, and produced porous tracks; neither its oxygen values nor its cycle count is a qualified limit for Cu–Ni/NAB DED. [CITE] [NUMBERS] [GAP] (alistair2022chemicalrecoveryof pages 2-3, alistair2022chemicalrecoveryof pages 5-6, alistair2022chemicalrecoveryof pages 7-9)
5. **Keep qualification claims on the requested test basis.** General DED/LPBF size ranges are not vendor cuts, LPBF and wire-fed precedents are not blown-powder DED, and no powder study above demonstrates **as-deposited** parity with wrought C71500 in 30-day seawater exposure. [CITE] [GAP] (doyle2022additivemanufacturingof pages 43-47, nemani2024advancementsinadditive pages 62-68, sun2024characterizationpreparationand pages 5-6)

References

1. (sun2024characterizationpreparationand pages 5-6): Xiaoyu Sun, Minan Chen, Tingting Liu, Kai Zhang, Huiliang Wei, Zhiguang Zhu, and Wenhe Liao. Characterization, preparation, and reuse of metallic powders for laser powder bed fusion: a review. Oct 2024. URL: https://doi.org/10.1088/2631-7990/acfbc3, doi:10.1088/2631-7990/acfbc3. This article has 124 citations.

2. (roth2024establishingaprocess pages 5-7): Jan-Philipp Roth, Ivo Šulák, Tomáš Kruml, Wojciech Polkowski, Tomasz Dudziak, Peter Böhlke, Ulrich Krupp, and Katrin Jahns. Establishing a process route for additive manufacturing of nicu-based alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments. The International Journal of Advanced Manufacturing Technology, Sep 2024. URL: https://doi.org/10.1007/s00170-024-14328-7, doi:10.1007/s00170-024-14328-7. This article has 6 citations.

3. (alistair2022chemicalrecoveryof pages 7-9): Alistair Speidel, Leonidas Gargalis, Jianchao Ye, Manyalibo J. Matthews, Adriaan Spierings, Richard Hague, Adam T. Clare, and James W. Murray. Chemical recovery of spent copper powder in laser powder bed fusion. Additive Manufacturing, Apr 2022. URL: https://doi.org/10.1016/j.addma.2022.102711, doi:10.1016/j.addma.2022.102711. This article has 23 citations and is from a highest quality peer-reviewed journal.

4. (roth2024establishingaprocess pages 7-9): Jan-Philipp Roth, Ivo Šulák, Tomáš Kruml, Wojciech Polkowski, Tomasz Dudziak, Peter Böhlke, Ulrich Krupp, and Katrin Jahns. Establishing a process route for additive manufacturing of nicu-based alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments. The International Journal of Advanced Manufacturing Technology, Sep 2024. URL: https://doi.org/10.1007/s00170-024-14328-7, doi:10.1007/s00170-024-14328-7. This article has 6 citations.

5. (alistair2022chemicalrecoveryof pages 2-3): Alistair Speidel, Leonidas Gargalis, Jianchao Ye, Manyalibo J. Matthews, Adriaan Spierings, Richard Hague, Adam T. Clare, and James W. Murray. Chemical recovery of spent copper powder in laser powder bed fusion. Additive Manufacturing, Apr 2022. URL: https://doi.org/10.1016/j.addma.2022.102711, doi:10.1016/j.addma.2022.102711. This article has 23 citations and is from a highest quality peer-reviewed journal.

6. (alistair2022chemicalrecoveryof pages 5-6): Alistair Speidel, Leonidas Gargalis, Jianchao Ye, Manyalibo J. Matthews, Adriaan Spierings, Richard Hague, Adam T. Clare, and James W. Murray. Chemical recovery of spent copper powder in laser powder bed fusion. Additive Manufacturing, Apr 2022. URL: https://doi.org/10.1016/j.addma.2022.102711, doi:10.1016/j.addma.2022.102711. This article has 23 citations and is from a highest quality peer-reviewed journal.

7. (roth2024establishingaprocess pages 2-4): Jan-Philipp Roth, Ivo Šulák, Tomáš Kruml, Wojciech Polkowski, Tomasz Dudziak, Peter Böhlke, Ulrich Krupp, and Katrin Jahns. Establishing a process route for additive manufacturing of nicu-based alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments. The International Journal of Advanced Manufacturing Technology, Sep 2024. URL: https://doi.org/10.1007/s00170-024-14328-7, doi:10.1007/s00170-024-14328-7. This article has 6 citations.

8. (roth2024establishingaprocess media 4fc8da04): Jan-Philipp Roth, Ivo Šulák, Tomáš Kruml, Wojciech Polkowski, Tomasz Dudziak, Peter Böhlke, Ulrich Krupp, and Katrin Jahns. Establishing a process route for additive manufacturing of nicu-based alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments. The International Journal of Advanced Manufacturing Technology, Sep 2024. URL: https://doi.org/10.1007/s00170-024-14328-7, doi:10.1007/s00170-024-14328-7. This article has 6 citations.

9. (alistair2022chemicalrecoveryof pages 3-5): Alistair Speidel, Leonidas Gargalis, Jianchao Ye, Manyalibo J. Matthews, Adriaan Spierings, Richard Hague, Adam T. Clare, and James W. Murray. Chemical recovery of spent copper powder in laser powder bed fusion. Additive Manufacturing, Apr 2022. URL: https://doi.org/10.1016/j.addma.2022.102711, doi:10.1016/j.addma.2022.102711. This article has 23 citations and is from a highest quality peer-reviewed journal.

10. (sun2024characterizationpreparationand pages 3-5): Xiaoyu Sun, Minan Chen, Tingting Liu, Kai Zhang, Huiliang Wei, Zhiguang Zhu, and Wenhe Liao. Characterization, preparation, and reuse of metallic powders for laser powder bed fusion: a review. Oct 2024. URL: https://doi.org/10.1088/2631-7990/acfbc3, doi:10.1088/2631-7990/acfbc3. This article has 124 citations.

11. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

12. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

13. (doyle2022additivemanufacturingof pages 43-47): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.
