<!--
Edison Scientific LITERATURE task (batch 5)
- Task ID: 768b1c22-c6f9-4a77-9253-c3c35c417c4d
- Submitted: 2026-10-17T06:20:06Z
- Fetched: 2026-10-17T06:42:02Z (status: success)
- Raw trajectory JSON: ../raw/b5-04-cavitation-ded-waam-nab.json.gz
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

QUESTION: Report the methods and numbers of "Advanced cavitation
erosion-corrosion resistance of nickel-aluminum bronze prepared by directed
energy deposition", Corros. Sci. (2024) 111982
(doi:10.1016/j.corsci.2024.111982), and "Comparative analysis of cavitation
erosion behavior in wire-arc directed energy deposition and cast
nickel-aluminum bronze alloys", Ultrason. Sonochem. (2025) 107235
(doi:10.1016/j.ultsonch.2025.107235): process (powder or wire, laser or
arc), composition, test standard and medium, incubation time, mass-loss
rates vs cast NAB, and the microstructural reasons. Also cover friction-stir
processed NAB cavitation as a reference. What does this imply for using a
cavitation test as a mid-cost screening node for propeller-repair alloys?

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

QUESTION: Report the methods and numbers of "Advanced cavitation
erosion-corrosion resistance of nickel-aluminum bronze prepared by directed
energy deposition", Corros. Sci. (2024) 111982
(doi:10.1016/j.corsci.2024.111982), and "Comparative analysis of cavitation
erosion behavior in wire-arc directed energy deposition and cast
nickel-aluminum bronze alloys", Ultrason. Sonochem. (2025) 107235
(doi:10.1016/j.ultsonch.2025.107235): process (powder or wire, laser or
arc), composition, test standard and medium, incubation time, mass-loss
rates vs cast NAB, and the microstructural reasons. Also cover friction-stir
processed NAB cavitation as a reference. What does this imply for using a
cavitation test as a mid-cost screening node for propeller-repair alloys?

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


# Cavitation evidence for deposited propeller-repair alloys

**Evidence limit.** Bibliographic records identify both requested articles, but their primary full texts were unavailable in the retrieved literature. Consequently, their incubation times, mass-loss rates, exact compositions, test standards and media, and proposed microstructural explanations **cannot be reported reliably**. In particular, “directed energy deposition” in the 2024 title does not establish whether its feedstock was powder or wire, or its energy source laser or arc. The 2025 title does establish *wire-arc* DED versus cast NAB. Numbers from other studies must not be assigned to either article. A review independently lists the 2025 article but does not reproduce its experimental results. (zhong2025enhancingmechanicalstrength pages 12-13)

The following comparison distinguishes the inaccessible target studies from directly verifiable benchmarks. All compositions are **wt%**; “not reported” below means *not verifiable from the material retrieved*, rather than proof that the authors did not measure it.

| Paper / process | Verified alloy and medium | Verified cavitation or corrosion results | Not established from accessible evidence |
|---|---|---|---|
| **Xu et al. (2024), “Advanced cavitation erosion-corrosion resistance of nickel-aluminum bronze prepared by directed energy deposition.” _Corrosion Science_ 231, 111982.** DOI: [10.1016/j.corsci.2024.111982](https://doi.org/10.1016/j.corsci.2024.111982). **DED; feedstock and energy source unconfirmed.** | NAB; exact composition and medium unverified. | No quantitative result could be verified because the primary full text was unavailable. | Powder versus wire; laser versus arc; ASTM standard; medium, duration, flow, incubation time, mass-loss rate versus cast NAB, density/porosity, electrochemistry, hardness, mechanical properties, powder size, Hall flow, apparent density and oxygen. |
| **Cai et al. (2025), “Comparative analysis of cavitation erosion behavior in wire-arc directed energy deposition and cast nickel-aluminum bronze alloys.” _Ultrasonics Sonochemistry_, 107235.** DOI: [10.1016/j.ultsonch.2025.107235](https://doi.org/10.1016/j.ultsonch.2025.107235). **Wire-arc DED versus cast.** (zhong2025enhancingmechanicalstrength pages 12-13) | NAB; exact compositions and medium unverified. | No quantitative result could be verified because the primary full text was unavailable. | Arc variant; ASTM standard; medium, duration, flow, incubation time, absolute mass-loss rates, porosity/density, electrochemistry, hardness and mechanical properties. Powder metrics are inapplicable to the wire-fed route and were not reported for the cast comparator. |
| **Song et al. (2013), “Comparison of Corrosion and Cavitation Erosion Behaviors Between the As-Cast and Friction-Stir-Processed Nickel Aluminum Bronze.” _Corrosion_ 69(11), 1111–1121.** DOI: [10.5006/0984](https://doi.org/10.5006/0984). **Cast versus friction-stir processed (FSP), not AM.** | UNS C95800: Al 9.18, Ni 4.49, Fe 4.06, Mn 1.03 and Cu balance (wt%). Distilled water and 3.5 wt% NaCl; 20 kHz, 60 μm amplitude, 0.5 mm horn–sample gap and approximately 20 °C. (song2013comparisonofcorrosion pages 4-8) | At 16 h in NaCl: cast **33.4 mg and 2.09 mg/h**; FSP **15.9 mg and 1.0 mg/h**. In distilled water: cast **16.1 mg** versus FSP **11.2 mg**. The article’s stated NaCl increases of 50% and 25% conflict with those raw 16 h values. FSP refined and homogenized the structure, reduced galvanic sites and κ-particle detachment, and limited deep cracking and cavities. Cast cavities exceeded 150 μm after 20 h in distilled water versus less than 10 μm for FSP. (song2013comparisonofcorrosion pages 15-19, song2013comparisonofcorrosion pages 8-12) | ASTM G32 compliance was not stated; no flow rate. Incubation is only graphically apparent at roughly **3–5 h**, not reported as a rigorously fitted value. No density/porosity fraction, powder size, Hall flow, apparent density or oxygen. (song2013comparisonofcorrosion media 3de21790) |
| **Huo et al. (2025), “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing.” _Materials_ 18, 2205.** DOI: [10.3390/ma18102205](https://doi.org/10.3390/ma18102205). **Wire-arc DED/CMT additive manufacturing; no cavitation test.** | ERCuNiAl wire: Al 8.73, Fe 5.90, Ni 4.52, Mn 1.39 and Cu balance (wt%). Aerated 3.5 wt% NaCl at 25 ± 5 °C; heat input 243.8–644.7 J/mm. (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 2-4) | As heat input rose, corrosion current density increased from **2.56 ± 0.04** to **7.52 ± 0.07 μA/cm²**, while polarization-derived potential shifted from **−269.61 ± 40** to **−700.94 ± 15 mV versus SCE**. Hardness fell from **192.4 ± 6.9** to **166.9 ± 0.3 HV**, and grain size rose from 38.26 to 74.62 μm. Causes included grain and κ-phase coarsening, uneven κ distribution and Al-solute redistribution. (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 7-10) | No cavitation standard, incubation time or mass loss; no cast-NAB control, seawater immersion or as-deposited C71500 comparison. No powder size, Hall flow, apparent density or oxygen because commercial 1.2 mm wire—not powder—was used. |


*Table: Compact evidence table separating verified quantitative results from details that could not be established. It avoids assigning unverified methods or values to the two inaccessible target studies.*

## Requested articles

**Xu, C.; Peng, Y.; Chen, L.-Y.; Huang, Y.; Zhang, T.-Y.; Cheng, J.-J.; Wang, K.-H.** “Advanced cavitation erosion-corrosion resistance of nickel-aluminum bronze prepared by directed energy deposition.” *Corrosion Science* **231** (2024), 111982. DOI: **10.1016/j.corsci.2024.111982**. **Process:** DED; powder/wire and laser/arc **unverified**. **Composition, conditions, results:** exact NAB composition, ASTM G32 status, NaCl versus natural/substitute seawater, duration and flow, incubation, absolute or cast-relative loss rates, density/porosity, electrochemistry, hardness, strength and powder metrics cannot be verified. Thus its title signals a direct *topic* overlap, not proven single-stream **blown-powder laser** DED or substrate-repair overlap. **[CITE] [NAVY: application relevance, not verified funding] [NOVELTY-RISK: deposited NAB cavitation–corrosion] [GAP: inaccessible methods and results].** The accessible review documents other laser-metal-deposited NAB studies, but supplies none of this article’s requested numbers. (nemani2024advancementsinadditive pages 79-83)

**Cai, X.; Yang, M.; Li, S.; Wang, C.; Qiao, Y.; Zhou, J.; Xue, F.** “Comparative analysis of cavitation erosion behavior in wire-arc directed energy deposition and cast nickel-aluminum bronze alloys.” *Ultrasonics Sonochemistry* (2025), article 107235. DOI: **10.1016/j.ultsonch.2025.107235**. **Process:** wire-arc DED/WAAM versus cast, **not powder-fed laser DED**. **Composition, conditions, results:** wire and cast chemistries, standard, water chemistry, exposure duration/flow, incubation and mass-loss-rate comparison, and the particular authors’ microstructural mechanism are not verifiable; no absolute numbers or improvement factor should be quoted. **[CITE] [NAVY: propeller-relevant application, funding unverified] [NOVELTY-RISK: AM-versus-cast NAB cavitation comparison] [GAP: not demonstrated here for powder-laser repair or C71500-level seawater resistance].** The title and bibliographic reference verify its comparison, not its outcome. (zhong2025enhancingmechanicalstrength pages 12-13)

## Quantitative reference: cast versus friction-stir-processed NAB

**Song, Q. N.; Zheng, Y. G.; Jiang, S. L.; Ni, D. R.; Ma, Z. Y.** “Comparison of Corrosion and Cavitation Erosion Behaviors Between the As-Cast and Friction-Stir-Processed Nickel Aluminum Bronze.” *Corrosion* **69** (2013), 1111–1121. DOI: **10.5006/0984**. **Process:** cast UNS C95800 versus solid-state friction-stir processing (FSP), **not DED**. Composition: **Cu balance–9.18 Al–4.49 Ni–4.06 Fe–1.03 Mn**. FSP used a **1,200-rpm** tool and **50 mm/min** traverse. Cavitation employed an ultrasonic horn at **20 kHz**, **60 µm** amplitude, **0.5 mm** above specimens in approximately **20 °C** distilled water or **3.5 wt% NaCl**. The paper describes this geometry but the inspected methods do **not expressly claim ASTM G32 compliance**. No imposed flow rate or ASTM D1141/natural-seawater medium is stated. **[CITE] [NUMBERS] [NAVY: cites prior U.S. Naval Surface Warfare Center FSP propeller-repair work, not proof this paper was Navy-funded].** (song2013comparisonofcorrosion pages 1-4, song2013comparisonofcorrosion pages 4-8)

At **16 h in 3.5 wt% NaCl**, cumulative mass losses were **33.4 mg cast** and **15.9 mg FSP**; reported cumulative-average rates were **2.09** and **1.0 mg/h**, respectively: approximately **2.1-fold less loss after FSP**. The corresponding **distilled-water** losses were **16.1** and **11.2 mg**. The article describes minimal loss over the **first approximately 5 h in distilled water**; neither an independently fitted saline incubation time nor a confidently comparable incubation-time advantage is available. The text also says NaCl increased losses by **50% cast/25% FSP** relative to distilled water, but its stated 16-h values instead imply approximately **107%/42%** increases; use the measured values and flag this discrepancy rather than repeating the percentages as established facts. The image of its saline mass-loss curves provides a visual cross-check, not a precise fitted incubation estimate. **[NUMBERS] [GAP: no ASTM-confirmed cross-study incubation benchmark].** (song2013comparisonofcorrosion pages 8-12, song2013comparisonofcorrosion media 3de21790)

**Mechanism:** casting contains coarse α, β′, κ particles and phase boundaries. Under cavitation, boundaries crack and κ particles detach; chloride-driven microgalvanic attack promotes α dissolution adjacent to κ and loss of lamellar α+κIII. FSP refines/homogenizes this structure, reducing detachment sites and allowing more distributed plastic deformation. After **20 h in distilled water**, observed cast cavities exceeded **150 µm** deep versus **<10 µm** after FSP. During prolonged **3.5 wt% NaCl** immersion, FSP produced much higher film impedance—about an **order of magnitude** higher Nyquist semicircle diameter after **10 days**—yet short-term electrochemistry under active cavitation distinguished the materials poorly because film was continually stripped. This is direct evidence that a short polarization measurement and a cavitation-loss measurement probe different failure modes. **[CITE] [NUMBERS] [GAP: no deposited repair interface].** (song2013comparisonofcorrosion pages 12-15, song2013comparisonofcorrosion pages 15-19, song2013comparisonofcorrosion pages 8-12)

## Process-distinct benchmarks and novelty boundaries

**Huo, R.; Wang, Z.; Wang, M.; Wang, R.; Zhang, S.; Zhang, C.; Wu, C.; Chen, H.; Chen, J.** “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing.” *Materials* **18** (2025), 2205. DOI: **10.3390/ma18102205**. **Process:** CMT **wire-arc** deposition, 1.2-mm ERCuNiAl wire onto copper, not powder laser DED or cast-NAB repair. Wire composition **Cu balance–8.73 Al–5.90 Fe–4.52 Ni–1.39 Mn**. In aerated **3.5 wt% NaCl**, approximately **25 ± 5 °C**, heat input increasing **243.8 → 644.7 J/mm** increased *i*₍corr₎ **2.56 ± 0.04 → 7.52 ± 0.07 µA/cm²**; its polarization-derived potential changed **−269.61 ± 40 → −700.94 ± 15 mV** with an SCE reference electrode. Measured surface hardness declined **192.4 ± 6.9 → 166.9 ± 0.3 HV** and mean grain size increased **38.26 → 74.62 µm**. Coarser grains and less uniform/coarser κ accompanied the decline. **No cavitation, immersion-service, cast comparator or powder lot was tested**; its electrochemical values must not be compared to cavitation mass-loss rates. **[CITE] [NUMBERS] [NOVELTY-RISK: thermal-history/microstructure/corrosion linkage in NAB] [GAP: no powder, cavitation or repair].** (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 7-10, huo2025modulatingheatinput pages 2-4)

**Li, B.; Zheng, H.; Han, C.; Zhou, K.** “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition.” *Additive Manufacturing* **39** (2021), 101825. DOI: **10.1016/j.addma.2021.101825**. **Process:** laser metal deposition/laser DED NAB, according to the accessible review; do **not** equate the review’s account with verified single-stream atomized-powder specifications. Reviewed as-deposited microstructure includes β′-like martensite, α, nanoscale Fe₃Al/NiAl and nanotwins; review-reported ranges are yield strength **593–713 MPa**, UTS **769–949 MPa**, elongation **10–12%**. Neither its cavitation response, cast-substrate repair, seawater-test conditions nor powder size/flow/oxygen is established here. **[CITE: secondary-source account] [NUMBERS: secondary-source mechanical benchmark] [NOVELTY-RISK: laser DED NAB itself is not new] [GAP: as-deposited marine-cavitation and interface validation].** (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 113-114)

**Yao, C.-L.; Kang, H.-S.; Lee, K.-Y.; Zhai, J.-G.; Shim, D.-S.** “A study on mechanical properties of CuNi2SiCr layered on nickel–aluminum bronze via directed energy deposition.” *Journal of Materials Research and Technology* **18** (2022), 5337–5361. DOI: **10.1016/j.jmrt.2022.04.129** **[DOI not verified in the accessible bibliography; verify before citing]**. **Process:** powder-fed laser DED of **CuNi2SiCr onto cast NAB**, according to the review; nominal Cu–2Ni–Si–Cr notation is **not** a measured complete wt% composition. The review describes porosity, single-phase α deposited material and inferior hardness/strength/wear to NAB; it advises against this particular repair pairing. Exact porosity fraction, powder properties, quantitative interface performance and corrosion numbers cannot be extracted from the available passage. **[CITE: bibliographic details except DOI require checking] [NAVY: propeller-repair application, funding unverified] [NOVELTY-RISK: powder laser-DED-on-cast-NAB repair already studied] [GAP: alternative alloy chemistry and linked screening].** A related corrosion study is **Yao, C.-L.; Shim, D.-S.**, “Corrosive properties of CuNi2SiCr fabricated through directed energy deposition on a nickel-aluminum bronze substrate,” *Journal of Alloys and Compounds* **918** (2022), 165776, DOI **10.1016/j.jallcom.2022.165776**; its quantitative results were not available here. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 113-114)

**Nemani, A. V.; Ghaffari, M.; Bokati, K. S.; Valizade, N.; Afshari, E.; Nasiri, A.** “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review.” *Journal of Manufacturing and Materials Processing* **8** (2024), 54. DOI: **10.3390/jmmp8020054**. **Process:** literature review spanning LPBF, wire-arc and laser DED; **not an additional cavitation experiment**. It specifically identifies AM Cu–Ni corrosion/service performance and NAB **as-printed versus heat-treated seawater** behavior as research needs, while documenting prior laser-deposited NAB and cast-NAB bimetallic work. It supplies **no transferable C71500 equivalence threshold**, and no measured powder Hall flow, apparent density or oxygen for the two target studies. **[CITE] [GAP] [NOVELTY-RISK: do not claim first laser DED NAB or first copper-alloy repair of NAB].** (nemani2024advancementsinadditive pages 102-105, nemani2024advancementsinadditive pages 79-83)

## Implication: a mid-cost cavitation node

**Yes—use cavitation as a conditional, mid-cost *screen*, not a seawater-qualification surrogate.** First gate powders and deposits on chemistry/lot oxygen, particle-size distribution, Hall flow and apparent density, then measure density, cracks and the *deposit–cast-NAB* or *deposit–wrought-Cu–Ni* interface. Run identically finished **as-deposited** specimens beside same-geometry **cast NAB, wrought C71500 and incumbent repair material**, in separate distilled-water and controlled saline exposures; specify and report the ultrasonic configuration/ASTM G32 conformity, amplitude, gap, temperature, dissolved oxygen, solution replacement and exposure schedule. Record **incubation, full time-resolved mass-loss curve, steady erosion rate, maximum attack depth, SEM/phase-specific damage and interface attack**, with replication. A flow-controlled/seawater exposure remains a later validation step: a stationary ultrasonic NaCl bath neither reproduces propeller flow nor establishes 30-day seawater equivalence. This protocol is a *proposal recommendation*, not a reported protocol of the inaccessible 2024/2025 articles. The Song study supports pairing saline and non-saline tests and demonstrates why early electrochemistry alone can miss substantial accumulated damage. (song2013comparisonofcorrosion pages 15-19, song2013comparisonofcorrosion pages 4-8, song2013comparisonofcorrosion pages 8-12)

Within the proposed function network, prioritize the cavitation node after inexpensive CALPHAD/thermal-history predictions, metallography, density and short electrochemistry, but before long immersion. Treat its outcome as **multivariate**: low loss is insufficient if porosity, brittle κ/γ₂, a weak repair boundary or selective interface attack is present; conversely, hardness alone cannot predict loss. Compare predicted *as-deposited* phase fractions/length scales against observed selective damage and use paired still-water/cavitation exposures to test film-removal sensitivity. Because cavitation measures coupled mechanical erosion and corrosion, **passing it does not demonstrate corrosion at least as good as wrought C71500**; reserve that acceptance claim for directly matched long-duration seawater corrosion testing. This is a proposed experimental interpretation supported by the cast/FSP mechanism and the observed thermal-input dependence of wire-arc NAB. (song2013comparisonofcorrosion pages 12-15, song2013comparisonofcorrosion pages 15-19, huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 7-10)

## Top 5 things the PI should know

1. **Do not quote the requested 2024/2025 papers’ incubation or erosion rates without their full texts.** Neither numerical comparison nor the 2024 feedstock route was verifiable here. (zhong2025enhancingmechanicalstrength pages 12-13)
2. **A defensible quantitative reference exists:** in Song’s controlled **16-h, 3.5 wt% NaCl** comparison, cast NAB lost **33.4 mg** versus **15.9 mg** after FSP; the improvement followed microstructural refinement, not a change in bulk alloy chemistry. Its quoted percentage comparisons to distilled water conflict with its reported raw values. (song2013comparisonofcorrosion pages 15-19, song2013comparisonofcorrosion pages 8-12)
3. **Claim novelty narrowly.** Laser-deposited NAB, WAAM-versus-cast cavitation and powder laser deposition onto cast NAB are existing topics; differentiated contributions are *new, characterized pre-alloyed feedstocks*, both repair substrates, **as-deposited** C71500-referenced seawater performance and cost-aware network optimization—not DED of NAB per se. (zhong2025enhancingmechanicalstrength pages 12-13, nemani2024advancementsinadditive pages 79-83)
4. **Measure phases, defects and the repair interface—not just hardness or short-run *i*₍corr₎.** Cast κ detachment and microgalvanic attack drove deep cavitation damage; wire-arc NAB heat input also markedly changed *i*₍corr₎ and hardness. These are distinct measurements, not interchangeable performance scores. (song2013comparisonofcorrosion pages 12-15, song2013comparisonofcorrosion pages 15-19, huo2025modulatingheatinput pages 10-13)
5. **Use the cavitation test between cheap screens and long immersion, with cast NAB and wrought C71500 run concurrently.** It can reject erosion-prone candidate deposits and interrogate corrosion–mechanical synergy, but cannot certify propeller service or the proposed seawater-corrosion acceptance criterion on its own. (song2013comparisonofcorrosion pages 15-19, song2013comparisonofcorrosion pages 4-8, nemani2024advancementsinadditive pages 102-105)

References

1. (zhong2025enhancingmechanicalstrength pages 12-13): W. Zhong, Liang Wang, Dun Miao, Xiang Cai, Meng-Meng Yang, Yanxin Qiao, Qi-chao Zhang, and Jian Zhou. Enhancing mechanical strength and tribological performance in tin bronze alloys via rolling treatment. npj Materials Degradation, Aug 2025. URL: https://doi.org/10.1038/s41529-025-00655-x, doi:10.1038/s41529-025-00655-x. This article has 4 citations and is from a peer-reviewed journal.

2. (song2013comparisonofcorrosion pages 4-8): Q. Song, Yingkui Zheng, Shenglin Jiang, D. Ni, and Zhi Ma. Comparison of corrosion and cavitation erosion behaviors between the as-cast and friction-stir-processed nickel aluminum bronze. Jul 2013. URL: https://doi.org/10.5006/0984, doi:10.5006/0984. This article has 63 citations and is from a peer-reviewed journal.

3. (song2013comparisonofcorrosion pages 15-19): Q. Song, Yingkui Zheng, Shenglin Jiang, D. Ni, and Zhi Ma. Comparison of corrosion and cavitation erosion behaviors between the as-cast and friction-stir-processed nickel aluminum bronze. Jul 2013. URL: https://doi.org/10.5006/0984, doi:10.5006/0984. This article has 63 citations and is from a peer-reviewed journal.

4. (song2013comparisonofcorrosion pages 8-12): Q. Song, Yingkui Zheng, Shenglin Jiang, D. Ni, and Zhi Ma. Comparison of corrosion and cavitation erosion behaviors between the as-cast and friction-stir-processed nickel aluminum bronze. Jul 2013. URL: https://doi.org/10.5006/0984, doi:10.5006/0984. This article has 63 citations and is from a peer-reviewed journal.

5. (song2013comparisonofcorrosion media 3de21790): Q. Song, Yingkui Zheng, Shenglin Jiang, D. Ni, and Zhi Ma. Comparison of corrosion and cavitation erosion behaviors between the as-cast and friction-stir-processed nickel aluminum bronze. Jul 2013. URL: https://doi.org/10.5006/0984, doi:10.5006/0984. This article has 63 citations and is from a peer-reviewed journal.

6. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

7. (huo2025modulatingheatinput pages 2-4): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

8. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

9. (huo2025modulatingheatinput pages 7-10): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

10. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

11. (song2013comparisonofcorrosion pages 1-4): Q. Song, Yingkui Zheng, Shenglin Jiang, D. Ni, and Zhi Ma. Comparison of corrosion and cavitation erosion behaviors between the as-cast and friction-stir-processed nickel aluminum bronze. Jul 2013. URL: https://doi.org/10.5006/0984, doi:10.5006/0984. This article has 63 citations and is from a peer-reviewed journal.

12. (song2013comparisonofcorrosion pages 12-15): Q. Song, Yingkui Zheng, Shenglin Jiang, D. Ni, and Zhi Ma. Comparison of corrosion and cavitation erosion behaviors between the as-cast and friction-stir-processed nickel aluminum bronze. Jul 2013. URL: https://doi.org/10.5006/0984, doi:10.5006/0984. This article has 63 citations and is from a peer-reviewed journal.

13. (nemani2024advancementsinadditive pages 113-114): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

14. (nemani2024advancementsinadditive pages 102-105): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.
