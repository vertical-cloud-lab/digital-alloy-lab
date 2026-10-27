<!--
Edison Scientific LITERATURE task (batch 3)
- Task ID: 18dab2a5-9c9c-477b-a3a2-5856a68768aa
- Submitted: 2026-10-17T05:46:05Z
- Fetched: 2026-10-17T06:16:54Z (status: success)
- Raw trajectory JSON: ../raw/b3-03-as-built-vs-annealed-nab.json.gz
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

QUESTION: Across processes (LPBF, laser DED, wire-arc DED, welds, castings),
does post-build or post-weld annealing (e.g. 675 C / 6 h, 1250 F) improve or
worsen nickel-aluminum bronze corrosion and selective phase corrosion? Build
a table of studies that tested BOTH as-built and annealed NAB in the same
electrolyte. Verify from the primary article: Murray et al., "Selective
laser melting of nickel aluminium bronze", Additive Manufacturing 33 (2020)
101122 - natural or substitute seawater, exposure times, mass losses for
as-built vs cast vs wrought; Shahriari et al. 2023 (npj Mater. Degrad., WAAM
NAB, as-built best); Barr et al. 2022 (LPBF composition and heat treatment);
Morshed-Behbahani et al. 2024 (LPBF NAB, as-built vs tempered); and any
DED study. When does martensitic or beta-prime-rich as-deposited NAB corrode
less, and when more (e.g. heat-affected zones of welds)? What microstructural
variable best predicts the outcome?

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

QUESTION: Across processes (LPBF, laser DED, wire-arc DED, welds, castings),
does post-build or post-weld annealing (e.g. 675 C / 6 h, 1250 F) improve or
worsen nickel-aluminum bronze corrosion and selective phase corrosion? Build
a table of studies that tested BOTH as-built and annealed NAB in the same
electrolyte. Verify from the primary article: Murray et al., "Selective
laser melting of nickel aluminium bronze", Additive Manufacturing 33 (2020)
101122 - natural or substitute seawater, exposure times, mass losses for
as-built vs cast vs wrought; Shahriari et al. 2023 (npj Mater. Degrad., WAAM
NAB, as-built best); Barr et al. 2022 (LPBF composition and heat treatment);
Morshed-Behbahani et al. 2024 (LPBF NAB, as-built vs tempered); and any
DED study. When does martensitic or beta-prime-rich as-deposited NAB corrode
less, and when more (e.g. heat-affected zones of welds)? What microstructural
variable best predicts the outcome?

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


# Does annealing improve nickel–aluminium bronze (NAB) seawater corrosion?

**No general rule survives a controlled comparison.** In the strongest accessible additive-manufacturing comparison, annealing wire-arc-deposited NAB generally **worsened short-term chloride electrochemical performance**. In a separate paired study of cast and powder-metallurgical NAB, the *same* 700 °C anneal improved the 480-hour corrosion response of cast material but worsened that of powder-consolidated material. In welded NAB, retained martensitic β′ in the heat-affected zone (HAZ) was selectively attacked in natural seawater; that establishes a reason to investigate post-weld treatment, **not evidence that an annealed weld was actually more resistant**. Electrochemical rates measured in 3.5 wt% NaCl must not be presented as 30-day natural-seawater mass losses. (shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 14-14, fayanas2025nickelaluminiumbronze pages 5-7, dobson2024corrosionmechanismsand pages 154-157)

## Studies with *both* untreated and annealed material tested in the same electrolyte

| Primary study, process and composition | Matched electrolyte and treatments | Quantitative outcome and interpretation | Assessment |
|---|---|---|---|
| **A. Shahriari, D. Chalasani, B. S. Amirkhiz and M. Mohammadi**, “Corrosion performance of wire arc additively manufactured NAB alloy,” *npj Materials Degradation* **7** (2023), DOI **10.1038/s41529-023-00405-x**. **Wire-arc DED/WAAM**, with an as-cast NAB comparator. Described as C95800; actual measured elemental wt% could not be verified from the accessible article text. | Naturally aerated **3.5 wt% NaCl**, approximately **23 ± 2 °C**; polished specimens, OCP stabilised **1,800 s**, EIS **100 kHz–0.01 Hz**, and cyclic polarisation **0.166 mV s⁻¹**. As-built WAAM **A1** and cast **C1** were pre-immersed **96 h**; annealed WAAM **HT1–HT3 were pre-immersed 24 h**. HT1: **350 °C/2 h**; HT2: **550 °C/4 h**; HT3: **675 °C/6 h**, furnace cooled. **Important: same electrolyte, unequal pre-exposure; not a strictly exposure-matched causal annealing test.** | Authors identify **as-built A1 as best**. Reported annealed currents: HT1 **≈4.4**, HT2 **≈6.6**, HT3 **≈8.0 μA cm⁻²**; corresponding reported total resistance *R*ₜ **≈10.2, 2.58 and 3.8 kΩ cm²**. A1’s reported overall impedance was **≈103 kΩ cm²**; A1 OCP **≈−0.293 V versus Ag/AgCl**, compared with **≈−0.222 V** averaged across the other conditions: a more negative potential did **not** imply faster corrosion. A1’s α grains were about **10 μm**, growing to **≈17/20 μm** after HT2/HT3. As-built fine, sparse κ precipitates reduced galvanic attack of adjacent α; annealing coarsened/redistributed κ and introduced κV. A reported ≈**3 μm** interdendritic valley in HT1 is *not* a long-term seawater penetration benchmark. Exact A1/C1 current densities, alloy wt%, density and powder metrics were **not verified**. (shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 10-10, shahriari2023corrosionperformanceof pages 2-2, shahriari2023corrosionperformanceof pages 4-5, shahriari2023corrosionperformanceof pages 14-14, shahriari2023corrosionperformanceof pages 8-10) | **[CITE] [NUMBERS] [NAVY: marine application, not verified Navy funding] [GAP: unequal conditioning; no natural-seawater repair test]** |
| **A. Fayanas, A. Veiga, A. Perez, A. Concustell, S. Molas and N. Ordas**, “Nickel Aluminium Bronze Alloys With Enhanced Erosion-Corrosion Resistance And Mechanical Strength,” *Journal of the Japan Society of Powder and Powder Metallurgy* **72** (2025), S819–S826, DOI **10.2497/jjspm.15F-T13-08**. **Continuous cast** and **sintered + HIP powder-metallurgical** NAB, *not DED*. Cast: **Cu balance–9.7Al–4.4Ni–4.3Fe–0.9Mn wt%**; sinter+HIP: **Cu balance–10Al–5Ni–4Fe–1Mn wt%**. | Both routes examined **as processed** and after **700 °C/2 h, slow cooling**, in the **same room-temperature 3.5 wt% NaCl**. Polarisation was reported before immersion and after **480 h static immersion**; separate **48 h** erosion–corrosion tests used **3 wt% sand and 3.8 m s⁻¹** in 3.5 wt% NaCl. | **Cast, 0 h:** untreated→annealed *j*₍corr₎ **9.90→12.7 μA cm⁻²**, rate **0.12→0.13 mm y⁻¹**. **Cast, 480 h:** **6.45→2.12 μA cm⁻²**, **0.07→0.02 mm y⁻¹**: annealing improved the *later electrochemical measurement*. **Sinter+HIP, 0 h:** **6.85→12.3 μA cm⁻²**, **0.08→0.14 mm y⁻¹**. **Sinter+HIP, 480 h:** **3.02→10.4 μA cm⁻²**, **0.04→0.12 mm y⁻¹**: annealing worsened it. These **mm y⁻¹ figures are polarisation-derived instantaneous rates**, not measured 480-hour thickness losses. At 480 h, *E*₍corr₎ was cast **−0.208→−0.215 V** and sinter+HIP **−0.277→−0.298 V**. Cast yield/UTS/elongation/hardness changed **439→372 MPa / 773→740 MPa / 16.7→20.5% / 200→192 HV10**; sinter+HIP **331→331 MPa / 700→698 MPa / 15.6→16.4% / 190→191 HV10**. The as-processed powder-metallurgical material had the lowest reported **48 h sand erosion–corrosion loss, 7.6 versus 8.7 mg cm⁻² for untreated cast**; these figures must **not** be called static-immersion losses. The study reports corrosion adjacent to κ phases even where average electrochemistry is favourable. Its **100 ppm oxygen** observation concerns the *NNS-HIP* material, not the paired sinter+HIP powder. (fayanas2025nickelaluminiumbronze pages 1-2, fayanas2025nickelaluminiumbronze pages 2-5, fayanas2025nickelaluminiumbronze pages 5-7, fayanas2025nickelaluminiumbronze media 610774f0) | **[CITE] [NUMBERS] [NAVY: marine application, not verified Navy funding] [GAP: no laser DED; no C71500 comparator]** |

**Visual primary-source checks:** Fayanas and co-workers’ electrochemical **Table 3**, cross-sectional **Figure 11**, and erosion–corrosion **Figure 12** were inspected; the electrochemical and erosion numbers above are deliberately kept separate. (fayanas2025nickelaluminiumbronze pages 5-7, fayanas2025nickelaluminiumbronze media 610774f0, fayanas2025nickelaluminiumbronze media c4ce5705, fayanas2025nickelaluminiumbronze media b345465c)

## Essential studies that cannot be placed in that paired-treatment table

| Study and process | What can—and cannot—be established from the retrieved material | Assessment |
|---|---|---|
| **T. Murray, S. Thomas, Y. Wu, W. Neil and C. Hutchinson**, “Selective laser melting of nickel aluminium bronze,” *Additive Manufacturing* **33** (2020), 101122, DOI **10.1016/j.addma.2020.101122**. **LPBF**, with cast/wrought comparisons indicated by the research question. | **The primary article was unobtainable here.** Its title, authors and DOI are corroborated by other articles’ bibliographies, **not by inspection of its results**. Consequently I cannot verify whether its seawater was **natural or ASTM D1141 substitute**, its exposure duration, its as-built/cast/wrought **mass losses**, composition, or whether it even supplies a paired annealing experiment. **Do not invent a 30-day result or put this paper in the annealing table.** (timmons2025laserpowderbed pages 26-27, dobson2024corrosionmechanismsand pages 240-244, camilleri2025coldsprayas pages 12-13) | **[CITE: bibliographic lead only] [GAP: primary numbers unverified]** |
| **C. Barr, A. Pateras, A. Molotnikov, D. Clarke and M. Brandt**, “Effect of composition on the tensile and corrosion performance of nickel aluminium bronze produced via laser powder bed fusion,” *Additive Manufacturing* **54** (2022), 102771, DOI **10.1016/j.addma.2022.102771**. **LPBF composition design**. | Primary full text **unobtainable**. The verified title establishes **substantial prior-art overlap in NAB composition, LPBF, tensile properties and corrosion**; neither its compositions, corrosion numbers, nor a claimed **as-built-versus-heat-treated same-electrolyte comparison** can be verified here. Do not attribute a particular heat-treatment result to Barr without the article. (timmons2025laserpowderbed pages 26-27, nemani2024advancementsinadditive pages 112-113) | **[CITE: bibliographic lead] [NOVELTY-RISK: composition→AM→corrosion is not new by itself] [GAP: treatment comparison unverified]** |
| **K. Morshed-Behbahani, A. J. Rayner, D. P. Bishop and A. Nasiri**, “Perspectives on the unusual electrochemical corrosion of nickel aluminum bronze (NAB) alloy fabricated through laser-powder bed fusion additive manufacturing,” *Corrosion Science* **228** (2024), 111846, DOI **10.1016/j.corsci.2024.111846**. **LPBF**. | Citation identified in another paper’s references, but primary article **unobtainable**. **Whether it actually compares as-built and tempered coupons, and the direction, electrolyte and magnitude of any effect, remain unverified.** (camilleri2025coldsprayas pages 12-13) | **[CITE: bibliographic lead] [NOVELTY-RISK: LPBF NAB electrochemical corrosion] [GAP: numerical treatment result unverified]** |
| **T. H. E. Dobson**, *Corrosion Mechanisms and Fatigue Behaviour of Marine Biofouled Plasma Welded Nickel Aluminium Bronze* (2024 thesis; **no thesis DOI verified**). Corresponding journal study: **T. Dobson *et al*.**, “Corrosion mechanisms of plasma welded nickel aluminium bronze immersed in seawater,” *Corrosion Science* (2024), DOI **10.1016/j.corsci.2024.112004**; journal article’s primary text was **not** obtained. **Plasma weld on cast NAB**, rather than DED. Thesis cast starting composition reported **Al 9.14, Fe 4.38, Ni 4.84, Mn 0.09 wt%; Cu balance**; a separate EDX value is **Al 9.89, Fe 3.75, Ni 4.71, Cu 81.66 wt%**—**do not conflate nominal/starting composition with local EDX**. | Thesis’s **original experiments**, unlike its literature review, compared welded coupons in **natural seawater at Millbay Marina, Plymouth, for 12 and 18 months** with simulated-seawater/air controls. This is **not an as-welded versus post-weld-annealed trial**. HAZ width **0.96 ± 0.09 mm**; β′ near weld selectively corroded, transitioning towards κIII-selective attack farther away. Maximum **weld-toe pit** depths in natural seawater **668 μm at 12 months** and **738 μm at 18 months**, versus **12 μm** for the reported simulated-seawater weld-toe comparison; measured maximum κIII selective-phase penetration **1,331 μm at 12 months**, which is *not the same metric as pit depth*. Natural exposure produced much more serious damage than simulated exposure. The thesis proposes removing retained β′ by heat treatment but **did not demonstrate a paired post-weld treatment benefit**. Natural seawater and NaCl-only screening therefore answer different questions. (dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 130-135, dobson2024corrosionmechanismsand pages 135-143, dobson2024corrosionmechanismsand pages 143-147, dobson2024corrosionmechanismsand pages 119-122, dobson2024corrosionmechanismsand pages 92-95, dobson2024corrosionmechanismsand pages 122-126) | **[CITE: thesis primary observations; journal DOI bibliographic lead] [NUMBERS] [NAVY: defence-standard/ship-service relevance; Navy funding unverified] [GAP: annealed weld comparison absent]** |
| **A. J. Rayner, K. Morshedbehbahani, C. Spence, G. Wood, D. Hamre, A. Nasiri and D. P. Bishop**, “Directed Energy Deposition of UNS C63020 Nickel Aluminum Bronze Powder,” conference chapter (2024), DOI **10.1007/978-3-031-67398-6_13**. **Powder-fed laser DED**, judging by title; primary chapter unavailable. | **Direct novelty warning:** deposition of pre-alloyed **C63020 NAB powder by DED is existing work**. Its exact feed chemistry, powder size/Hall flow/oxygen, achieved density, substrate, annealing and corrosion test **cannot be verified** from the retrieved text. It therefore does **not** establish an existing paired DED corrosion result. | **[NOVELTY-RISK: pre-alloyed NAB powder DED already reported] [GAP: repair-interface and matched as-deposited seawater data unverified]** |
| **C. Xu *et al*.**, “Corrosion behavior of directed energy deposited Ni-Al bronze in 3.5 wt% NaCl solution,” preprint DOI **10.2139/ssrn.4263467**; **C. Xu, Y. Peng, L.-Y. Chen, T.-Y. Zhang, S. He and K.-H. Wang**, “Corrosion behavior of wire-arc additive manufactured and as-cast Ni-Al bronze in 3.5 wt% NaCl solution,” *Corrosion Science* **215** (2023), 111048. | **Do not classify by the preprint title alone.** An accessible 2025 paper identifies the published comparison explicitly as **wire-arc additive manufactured versus as-cast**, not established single-stream blown-powder laser DED. Primary preprint and final article were not obtained; final DOI, composition, annealing and numbers were **not independently verified**. (fayanas2025nickelaluminiumbronze pages 7-8) | **[CITE: bibliographic lead] [GAP: process identity and paired treatment require primary verification]** |

No study accessible in this search establishes **same-electrolyte, as-deposited-versus-annealed corrosion** for **single-stream pre-alloyed blown-powder laser DED NAB**, much less a **cast-NAB or wrought-Cu–Ni repair interface compared head-to-head with C71500 after extended seawater immersion**. This is an **evidence-limited gap claim**, not proof that no such paper exists. Nor can the retrieved primary evidence supply trustworthy LPBF/DED **porosity, Hall flow, apparent powder density or powder-lot oxygen** benchmarks for the requested comparisons. (camilleri2025coldsprayas pages 12-13, nemani2024advancementsinadditive pages 112-113, shahriari2023corrosionperformanceof pages 12-14)

## What predicts when β′-rich material fares better or worse?

The best *working predictor* is **the exposed, spatially connected area of selectively dissolving phases and their galvanic interfaces—including β′/α and κ/α boundaries—under the actual local electrolyte and film history**. It is **not** hardness, a bulk β′ percentage, *E*₍corr₎ alone or a nominal annealing temperature. For Shahriari’s relatively fine as-built WAAM NAB, sparse/fine κ reduced cathodic area and α-adjacent galvanic attack; subsequent κ coarsening/precipitation outweighed any presumed benefit from heat treatment. Fayanas’s as-processed sinter+HIP alloy likewise had the **lowest initial current despite its more negative potential and higher reported β′ fraction**, while annealing raised its 480-hour current; conversely, annealing lowered the *cast* alloy’s 480-hour current. These are *observed associations*, **not** a validated cross-process statistical predictor. (shahriari2023corrosionperformanceof pages 10-10, shahriari2023corrosionperformanceof pages 2-2, fayanas2025nickelaluminiumbronze pages 1-2, fayanas2025nickelaluminiumbronze pages 2-5, fayanas2025nickelaluminiumbronze pages 5-7)

The contrary case is a **weld HAZ containing spatially concentrated retained β′**, especially at a weld toe in **natural, biofouling-prone seawater**: Dobson directly observed β′-selective attack there, alongside κIII-selective penetration in adjacent regions. Which constituent dissolves can also change with local chemistry: the thesis relates κIII attack under biofouling to acidified crevice conditions. Thus **“β′-rich as deposited is corrosion-resistant” must never be extrapolated from short, aerated bulk NaCl tests to a welded interface or months of natural seawater**. Quantify β′ and κ **fraction, size, spacing and connectivity at the deposit, HAZ and interface**; measure phase-specific penetration as well as average current and long-duration mass loss. (dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 130-135, dobson2024corrosionmechanismsand pages 143-147)

## Top 5 things the PI should know

1. **A 675 °C/6 h anneal is not a seawater-corrosion guarantee.** WAAM short-term chloride performance deteriorated with high-temperature treatments, but Shahriari’s **96-versus-24-hour preimmersion confound** demands an exposure-matched replication. (shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 14-14)
2. **The annealing effect changes sign with starting microstructure and exposure time:** Fayanas’s **480-hour cast** polarisation rate improved **0.07→0.02 mm y⁻¹**, whereas **sinter+HIP worsened 0.04→0.12 mm y⁻¹**, under the same anneal and nominal electrolyte. (fayanas2025nickelaluminiumbronze pages 1-2, fayanas2025nickelaluminiumbronze pages 5-7, fayanas2025nickelaluminiumbronze media 610774f0)
3. **Repair-zone selective penetration is a separate acceptance criterion.** Natural-seawater welded NAB showed **668/738 μm weld-toe pits** and **up to 1,331 μm κIII penetration**; neither an attractive bulk *i*₍corr₎ nor crack-free, dense deposited metal demonstrates HAZ/interface durability. (dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 135-143, dobson2024corrosionmechanismsand pages 143-147)
4. **Frame novelty narrowly and accurately.** LPBF NAB **composition–corrosion** and pre-alloyed **C63020 powder DED** already have identifiable publications. The defensible proposed contribution is the *integrated*, lot-characterised **single-stream alloy-design → powder → laser DED → as-deposited deposit/repair interface → long-term seawater** pipeline, tested against **wrought C71500**, with function-network optimisation and thermal-history-informed phase prediction—not merely “first NAB DED” or “first NAB composition optimisation.” (timmons2025laserpowderbed pages 26-27, nemani2024advancementsinadditive pages 112-113)
5. **Keep unresolved primary-source claims unresolved.** Murray’s **natural-versus-substitute seawater, durations and as-built/cast/wrought mass losses**, and Barr’s and Morshed-Behbahani’s **specific heat-treatment results**, **could not be verified from their primary articles in this search**. Do not put guessed values or an asserted 30-day superiority over C71500 into the proposal. (timmons2025laserpowderbed pages 26-27, camilleri2025coldsprayas pages 12-13, nemani2024advancementsinadditive pages 112-113)

References

1. (shahriari2023corrosionperformanceof pages 12-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

2. (shahriari2023corrosionperformanceof pages 14-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

3. (fayanas2025nickelaluminiumbronze pages 5-7): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

4. (dobson2024corrosionmechanismsand pages 154-157): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

5. (shahriari2023corrosionperformanceof pages 10-10): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

6. (shahriari2023corrosionperformanceof pages 2-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

7. (shahriari2023corrosionperformanceof pages 4-5): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

8. (shahriari2023corrosionperformanceof pages 8-10): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

9. (fayanas2025nickelaluminiumbronze pages 1-2): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

10. (fayanas2025nickelaluminiumbronze pages 2-5): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

11. (fayanas2025nickelaluminiumbronze media 610774f0): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

12. (fayanas2025nickelaluminiumbronze media c4ce5705): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

13. (fayanas2025nickelaluminiumbronze media b345465c): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

14. (timmons2025laserpowderbed pages 26-27): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

15. (dobson2024corrosionmechanismsand pages 240-244): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

16. (camilleri2025coldsprayas pages 12-13): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

17. (nemani2024advancementsinadditive pages 112-113): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

18. (dobson2024corrosionmechanismsand pages 130-135): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

19. (dobson2024corrosionmechanismsand pages 135-143): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

20. (dobson2024corrosionmechanismsand pages 143-147): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

21. (dobson2024corrosionmechanismsand pages 119-122): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

22. (dobson2024corrosionmechanismsand pages 92-95): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

23. (dobson2024corrosionmechanismsand pages 122-126): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

24. (fayanas2025nickelaluminiumbronze pages 7-8): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.
