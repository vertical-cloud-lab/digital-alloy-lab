<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: 83c4382b-0668-473f-9f8a-ab068b3c6c91
- Submitted: 2026-10-17T05:10:42Z
- Fetched: 2026-10-17T05:42:02Z (status: success)
- Raw trajectory JSON: ../raw/b1-02-ded-nab.json.gz
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

QUESTION: What is known about blown-powder laser DED (laser metal deposition,
laser cladding) of nickel-aluminum bronze (e.g. C95800, CuAl10Fe5Ni5)? Cover
process windows (power, speed, powder feed, spot), porosity and cracking, the
as-deposited microstructure (martensitic beta', retained beta, kappa phases
I-IV, Widmanstatten alpha) and how reheating by later layers changes it,
mechanical properties, and corrosion in NaCl or seawater, especially
selective phase corrosion (de-aluminification) as deposited vs after heat
treatment. Compare with wire-arc DED NAB (which the Navy has specified, with
a 1250 F / 6 h anneal) and with LPBF NAB.

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

QUESTION: What is known about blown-powder laser DED (laser metal deposition,
laser cladding) of nickel-aluminum bronze (e.g. C95800, CuAl10Fe5Ni5)? Cover
process windows (power, speed, powder feed, spot), porosity and cracking, the
as-deposited microstructure (martensitic beta', retained beta, kappa phases
I-IV, Widmanstatten alpha) and how reheating by later layers changes it,
mechanical properties, and corrosion in NaCl or seawater, especially
selective phase corrosion (de-aluminification) as deposited vs after heat
treatment. Compare with wire-arc DED NAB (which the Navy has specified, with
a 1250 F / 6 h anneal) and with LPBF NAB.

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


# Nickel–aluminum bronze made by blown-powder laser DED

**Scope and interpretation.** The literature establishes that pre-alloyed NAB powder can be laser-deposited to high density and high strength, but the best-documented powder-DED process study did **not** test seawater corrosion. Results for laser deposition onto stainless steel, WAAM, and laser powder-bed fusion (LPBF) are informative but are not demonstrations of crack-free, corrosion-qualified repair of cast NAB or wrought Cu–Ni. Compositions below are **wt%**; “not reported” means that the cited evidence does not supply a defensible value. The PI’s publications are excluded. (li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand pages 9-14, shahriari2023corrosionperformanceof pages 14-14, nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 79-83)

## Direct powder-fed laser DED and laser cladding

**1. Li, B., Zheng, H., Han, C., and Zhou, K. “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition.” *Additive Manufacturing* 39 (2021), 101825. DOI: 10.1016/j.addma.2020.101825.** **Process:** single pre-alloyed, gas-atomized-powder laser metal deposition, building NAB on itself; not elemental-powder blending. **Composition:** measured powder Cu 80.35 ± 0.91, Al 9.70 ± 0.89, Fe 5.48 ± 0.86, Ni 4.47 ± 0.60. Specified powder cut 45–106 µm; measured D10/D50/D90 = 49.76/76.29/116.46 µm. Hall flow, apparent density, and powder oxygen were not reported. **Window:** 500–2250 W and 0.25–2 m/min screened as single tracks; satisfactory bulk builds principally 1000–1500 W, 0.5–1.5 m/min, 1.5–2 mm hatch; 2-mm spot and alternating 90° hatch. The reported **32 g/min is helium carrier-gas flow, not powder mass-feed rate**; powder feed was not quantified. (li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand pages 9-14)

Most bulk specimens exceeded **99% relative density** by Archimedes; the best was **99.55%**, at **1500 W, 1 m/min, 2-mm hatch**. At 1500 W and 2 m/min, gas pores occurred; at 750 W and 1 m/min, lack-of-fusion pores, unmelted particles, and layer delamination prevented tensile-coupon manufacture. Excessive-power *single tracks* developed hot cracks. Thus a good-looking single track does not establish a dense, crack-free multilayer window. Figure 3 documents the track/cracking window and Figure 4 the density series. **No NaCl, seawater, or post-build-corrosion testing was reported.** [CITE] [NUMBERS] [NOVELTY-RISK: single-stream, pre-alloyed NAB powder, density and tensile optimization already demonstrated] [GAP: no seawater or repair-interface qualification]. (li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand media e4936506, li2021nanotwinscontainingmicrostructureand media b262c03b, li2021nanotwinscontainingmicrostructureand pages 24-29)

**As-deposited phases:** high-temperature β transforms to a metastable plate-like martensite denoted **β\*** by these authors; do not uncritically equate its reported FCC-like diffraction with every conventional β′ designation. Approximately **250-nm** martensite plates, nanotwins, **600–900-nm** primary Widmanstätten α sideplates, intragranular basketweave α, and Fe₃Al/**κII** and NiAl nanoprecipitates were identified. NiAl can grow on Fe₃Al. Melt-pool centers and boundaries show different β\* morphologies, consistent with different local cooling histories. The study did **not** establish retained-β fraction or separately quantify κI, κIII, and κIV, nor did it isolate the effects of reheating by later layers. **Mechanical:** yield **593–713 MPa**, ultimate tensile strength **769–949 MPa**, elongation **10–12%**; deposit hardness was not reported. These are not corrosion results. [CITE] [NUMBERS] [GAP: phase-resolved thermal-history and corrosion linkage]. (li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 14-19, li2021nanotwinscontainingmicrostructureand pages 24-29)

**2. Zhao, L., Du, B., Yao, J., Chen, H., Ding, R., and Li, K. “Microstructure and Mechanical Properties of Nickel-Aluminum Bronze Coating on 17-4PH Stainless Steel by Laser Cladding.” *Chinese Journal of Mechanical Engineering* 35 (2022), 140. DOI: 10.1186/s10033-022-00807-z.** **Process:** pre-alloyed NAB powder laser cladding on **17-4PH stainless steel**, not NAB-on-NAB or NAB-on-Cu–Ni repair. **Composition:** powder Cu balance, Al **10.80**, Ni **4.73**, Fe **4.10**, O **0.025**; particle size **45–100 µm**. **Settings:** 1500, 1800, 2100, or 2400 W; **1.2 m/min**; **3.4-mm** spot; **1.7-mm** hatch; one- and four-layer specimens. Powder mass-feed and quantitative bulk porosity were not reported. Penetrant/metallographic examination found no visible pores or cracks, but this is **not** a measured 100%-density claim. (zhao2022microstructureandmechanical pages 1-2, zhao2022microstructureandmechanical pages 2-4, zhao2022microstructureandmechanical pages 11-12)

The deposit contained α-Cu, Fe-rich structures and Fe–Al/Ni–Al **κ** intermetallics; substrate Fe/Cr dilution and thermal history matter. Upper regions were finer, lower/interface regions coarser; greater energy input coarsened grains. Hardness was **204–266 HV0.2**, compared in the paper with approximately **159 HV0.2** for a heat-treated C95800 propeller-blade specimen. A joint tensile specimen broke in bronze rather than at the interface; inferred interface strength exceeded **767.80 MPa**. **No corrosion experiment was reported in this particular paper.** [CITE] [NUMBERS] [NAVY: propeller/bimetal application, not evidence of Navy sponsorship] [NOVELTY-RISK: powder-fed NAB laser cladding and dissimilar-interface integrity already studied] [GAP: cast-NAB and Cu–Ni substrates and seawater]. (zhao2022microstructureandmechanical pages 11-12, zhao2022microstructureandmechanical pages 2-4, zhao2022microstructureandmechanical pages 1-2, zhao2022microstructureandmechanical pages 9-11)

**Relevant but not numerically verified here:** Zhao, L., Li, K., Yao, J., Yuan, Y., and Du, B. “The Laser Deposited Nickel-Aluminum Bronze Coatings on SUS630 Stainless Steel and Its Corrosion Resistance in 3.5 wt.% NaCl Solution.” *Metals* 12 (2022), 781. DOI: **10.3390/met12050781**. SUS630 is 17-4PH; this **is** a directly relevant powder-laser-deposit/NaCl study, so a blanket claim that no laser-deposited NAB corrosion study exists would be wrong. Its full experimental results were not obtained in this search: **do not assign it an invented i_corr, E_corr, exposure duration, or selective-attack depth**, or treat its steel substrate as cast-NAB repair. [CITE] [NOVELTY-RISK: already tests laser-deposited NAB corrosion in 3.5% NaCl] [GAP: qualifying performance against C71500 in prolonged seawater remains unestablished here]. (zhao2022microstructureandmechanical pages 1-2)

**Boundary of the alloy family:** Pi, Z., Du, K., Chen, X., Zheng, Z., and Wang, C. “Laser cladding remanufacturing of propeller ZCuAl8Mn13Fe3Ni2 alloy.” *Scientific Reports* 15 (2025). DOI: **10.1038/s41598-025-96674-4**. **Process:** powder laser cladding onto matching cast **manganese–aluminum bronze**, **not conventional approximately 5%-Ni NAB**. Measured powder: Cu balance, Al **8.15**, Mn **13.16**, Fe **3.03**, Ni **2.11**. At **1600 W**, **6 mm/s**, feeder **2 rpm** (not a calibrated mass flow), and gas **3.5 L/min**, the deposit showed α, β, γ₂ and κ, **278 HB**, and i_corr **3.729 × 10⁻² mA/cm²** (**37.29 µA/cm²**), E_corr **−0.271 V**; matching cast material gave **31.42 µA/cm²** and **−0.266 V**. The article describes artificial-seawater mass-loss measurement, but the retrieved evidence does not establish its formulation, immersion duration, flow, reference electrode for those potentials, or phase-selective penetration depth. Its **18.68% higher i_corr** than cast is a warning that increased hardness need not mean better corrosion. [CITE] [NUMBERS] [NOVELTY-RISK: lower-Ni manganese-bronze matching-cast propeller repair already investigated] [GAP: not a C71500 or standard-NAB comparison]. (ziqiang2025lasercladdingremanufacturing pages 1-3, ziqiang2025lasercladdingremanufacturing pages 3-6)

An older processing lead should not be misclassified without its methods: Hyatt, C. V., Magee, K. H., and Betancourt, T. “The effect of heat input on the microstructure and properties of nickel aluminum bronze laser clad with a consumable of composition Cu-9.0Al-4.6Ni-3.9Fe-1.2Mn.” *Metallurgical and Materials Transactions A* 29 (1998), 1677–1690. DOI: **10.1007/s11661-998-0090-5**. A later powder-cladding paper reports **entirely martensitic deposit at 42.5 J/mm**, increasing α with heat input, and peak hardness at **64 J/mm**. Because the accessible account says *consumable* rather than establishing a pre-alloyed blown-powder feed, these are **laser-cladding heat-input/phase observations, not a verified powder-DED recipe**. [CITE] [NUMBERS] [GAP: exact feed form and seawater response not verified]. (zhao2022microstructureandmechanical pages 1-2)

## What subsequent thermal cycles and seawater comparisons actually show

**3. Dharmendra, C., Hadadzadeh, A., Amirkhiz, B. S., Janaki Ram, G. D., and Mohammadi, M. “Microstructural evolution and mechanical behavior of nickel aluminum bronze Cu-9Al-4Fe-4Ni-1Mn fabricated through wire-arc additive manufacturing.” *Additive Manufacturing* 30 (2019), 100872. DOI: 10.1016/j.addma.2019.100872.** **Process:** GMAW wire-arc DED, **not powder laser DED**, on 316L; nominal deposited Cu–9Al–4Fe–4Ni–1Mn, compared against cast C95800-type NAB. Settings: **6.5 m/min** wire feed, **480 mm/min** travel, **114 A**, **12.5 V**, approximately **170 J/mm**. The authors reported near-fully-dense **25-mm-square, 160-mm-high** bars without observed layer-interface defects, but no quantified percent porosity. Cast microstructure contained α and κI–IV; WAAM suppressed coarse rosette **κI** but retained globular Fe₃Al **κII**, lamellar NiAl **κIII**, and **5–10-nm κIV** in α. WAAM **did not show the martensite-dominated structure seen in faster laser processes**. [CITE] [NUMBERS] [NAVY: marine component application]. (dharmendra2019microstructuralevolutionand pages 2-3, dharmendra2019microstructuralevolutionand pages 1-2, dharmendra2019microstructuralevolutionand pages 9-13, dharmendra2019microstructuralevolutionand pages 14-15)

The WAAM article provides a physically useful warning about **later-layer reheating**, not a measured laser-DED transformation map: material reheated above the approximately **830 °C β solvus** can partially/fully dissolve κ precipitates, then reprecipitate κII and transform β to α + κIII on cooling. Subsolvus reheating can instead coarsen κII and drive α + κIII ⇄ β transformations; location and successive thermal peaks matter, especially through approximately **850–500 °C**. Measured WAAM versus its cast comparator: **yield 388 ± 12 versus 300 ± 15 MPa; UTS 685 ± 10 versus 670 ± 8 MPa; elongation 26 ± 1 versus 16 ± 2%**. These are **mechanical**, not saltwater, comparisons. [CITE] [NUMBERS] [GAP: validate these transformations separately for laser-DED cooling histories]. (dharmendra2019microstructuralevolutionand pages 9-13, dharmendra2019microstructuralevolutionand pages 13-14)

**4. Shahriari, A., Chalasani, D., Shalchi Amirkhiz, B., and Mohammadi, M. “Corrosion performance of wire arc additively manufactured NAB alloy.” *npj Materials Degradation* 7 (2023), 85. DOI: 10.1038/s41529-023-00405-x.** **Process:** GMAW-WAAM using NAB wire on 316L, compared with cast NAB. Relevant wire nominally Cu–9Al–4Fe–4Ni–1Mn; an independently verified specimen-by-specimen analysis was not available. **Test:** naturally aerated **3.5 wt% NaCl**, approximately **23 ± 2 °C**, **no reported imposed flow**; OCP stabilization **1800 s**; saturated Ag/AgCl reference; EIS **100 kHz–0.01 Hz**, 10-mV amplitude; cyclic polarization **0.166 mV/s**. Importantly, **as-built WAAM and cast were immersed 96 h, but heat-treated samples 24 h**: comparisons must note this differing exposure duration. 3.5% NaCl is neither natural seawater nor ASTM D1141 substitute seawater. (shahriari2023corrosionperformanceof pages 1-2, shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 14-14, dharmendra2019microstructuralevolutionand pages 2-3)

The **as-built** WAAM condition had the best reported impedance, approximately **103 kΩ·cm²**, despite a *less noble* approximately **−0.293 V vs Ag/AgCl** versus approximately **−0.222 V** averaged over cast and treated conditions. A more negative E_corr therefore **did not** imply faster corrosion. Treatment at **350 °C/2 h** enlarged κIV, with approximately **4.4 µA/cm²** and **10.2 kΩ·cm²** total fitted resistance; **550 °C/4 h** produced/coarsened cathodic κ phases including needle-like κV, with approximately **6.6 µA/cm²** and **2.58 kΩ·cm²**; **675 °C/6 h**, essentially **1250 °F/6 h**, gave approximately **8 µA/cm²** and **3.8 kΩ·cm²**. These reported total resistances are **not interchangeable with E_corr, instantaneous corrosion rate, or a 30-day mass-loss result**. κII/κIII/κIV (and treatment-induced κV) are relatively cathodic; the adjacent **α matrix**, including interdendritic α, preferentially dissolves. Local interdendritic depressions of approximately **3 µm** were reported; that is **not** a proven maximum 30-day de-aluminification depth. [CITE] [NUMBERS] [NAVY: directly tests the approximately 1250 °F/6 h anneal relevant to naval practice] [NOVELTY-RISK: as-built-versus-annealed phase-selective chloride corrosion already studied for WAAM] [GAP: analogous laser-powder-DED and equal-duration seawater tests]. (shahriari2023corrosionperformanceof pages 2-2, shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 14-14, shahriari2023corrosionperformanceof pages 10-10, shahriari2023corrosionperformanceof pages 8-10)

**Important qualification on the “Navy-specified” anneal:** Dharmendra and colleagues describe **675 °C for at least 6 h as generally recommended for *sand-cast C95800* seawater service** and propose examining it for WAAM; Shahriari *actually tests* 675 °C/6 h WAAM and finds worse electrochemical behavior than as-built. The accessible sources do **not** verify the wording or applicability of a binding Navy WAAM specification. Cite a primary naval specification separately before asserting that it mandates this treatment for every WAAM build. [CITE] [NAVY] [GAP]. (dharmendra2019microstructuralevolutionand pages 14-15, shahriari2023corrosionperformanceof pages 1-2)

**5. Barr, C., Pateras, A., Molotnikov, A., Clarke, D., and Brandt, M. “Effect of composition on the tensile and corrosion performance of nickel aluminium bronze produced via laser powder bed fusion.” *Additive Manufacturing* 54 (2022), 102771. DOI: 10.1016/j.addma.2022.102771.** **Process:** **LPBF**, not powder-fed DED. A 2024 peer-reviewed synthesis identifies feedstocks **C63000: Cu–10.2Al–4.8Fe–5.0Ni–0.2Si** and **C95800: Cu–9.0Al–4.0Fe–4.6Ni–1.9Mn**. As-built C63000 was predominantly β′, with approximately **1120 MPa UTS but only 3% elongation**; lower-Al C95800 developed continuous α along β′ boundaries and was more ductile. On heat treatment, β′ converted toward α + κIII; the review describes heat-treated corrosion as similar to wrought NAB. **The primary full text and its electrolyte, immersion duration, numerical polarization currents, and exact post-treatment schedule were not recovered**, so no numerical LPBF i_corr is assigned. [CITE] [NUMBERS: mechanical only] [NOVELTY-RISK: composition → as-built phase → tensile/corrosion has been explored, but in LPBF] [GAP: laser-DED and Cu–Ni repair are distinct]. (nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 113-114)

**6. Murray, T., Thomas, S., Wu, Y., Neil, W., and Hutchinson, C. “Selective laser melting of nickel aluminium bronze.” *Additive Manufacturing* 33 (2020), 101122. DOI: 10.1016/j.addma.2020.101122.** **Process:** LPBF; reviewed feedstock **Cu–9.8Al–5.2Ni–4.6Fe–0.3Mn**. An independent later paper reports a lowest porosity of **0.05 ± 0.01%**. A 2024 review describes as-printed twinned martensite with little/no κ, brittle tensile response, and about **one order of magnitude less mass loss** than cast and wrought NAB after **three and six months’ seawater immersion**. Heating at **600–700 °C for 1 h** produced α plus κ; **800–900 °C for 1 h** produced coarser κ and additional transformation products. **Natural versus substitute seawater, flow, individual mass losses, and treatment-specific corrosion values were not independently verified from the primary text**, so neither a rate nor a transferable DED corrosion prediction follows. [CITE] [NUMBERS: porosity and comparative immersion magnitude] [GAP: martensite-rich laser DED is not automatically equivalently corrosion resistant]. (nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 74-79, zhao2022microstructureandmechanical pages 1-2, nemani2024advancementsinadditive pages 113-114)

**Supplementary cast baseline:** Fayanas, A., Veiga, A., Perez, A., Concustell, A., Molas, S., and Ordas, N. “Nickel Aluminium Bronze Alloys with Enhanced Erosion-Corrosion Resistance and Mechanical Strength.” *Journal of the Japan Society of Powder and Powder Metallurgy* 72, Supplement (2025), S819–S826. DOI: **10.2497/jjspm.15f-t13-08**. **Processes:** cast, sinter-plus-HIP and encapsulated-powder HIP—**not DED or LPBF**. Cast composition Cu balance, Al **9.7**, Ni **4.4**, Fe **4.3**, Mn **0.9**. As-processed cast benchmark: **439 ± 5 MPa yield, 773 ± 4 MPa UTS, 16.7 ± 1.2% elongation, 200 ± 1 HV10**. At room temperature in **3.5% NaCl**, with 20-min OCP monitoring and polarization before and after **480 h static immersion**, cast corrosion-rate estimates were **0.12 mm/y initially** and **0.07 mm/y at 480 h**; the same cast material after **700 °C/2 h** gave **0.13** and **0.02 mm/y**, respectively. These **polarization-derived rates are not 480-hour measured penetration depths**. Separate flowing slurry erosion–corrosion employed **3.5% NaCl, 3% silica sand <355 µm, 3.8 m/s, 48 h**; do not mix these data with static immersion. This cast result and Shahriari’s WAAM result demonstrate that the effect of annealing **depends on starting microstructure and test**, rather than supporting a universal “annealing helps/hurts NAB corrosion” rule. [CITE] [NUMBERS] [GAP: no direct C71500 benchmark]. (fayanas2025nickelaluminiumbronze pages 1-2, fayanas2025nickelaluminiumbronze pages 5-7, fayanas2025nickelaluminiumbronze pages 2-5)

## Evidence gaps that should determine the experiments

* **No established answer from the recovered evidence** gives, on the **same pre-alloyed laser-DED coupons**, as-deposited versus annealed **30-day** static and flowing natural/ASTM D1141 seawater performance; phase-resolved de-aluminification depth; and matched **wrought C71500** results. Short NaCl polarization is a screening test, not proof of seawater equivalence. (li2021nanotwinscontainingmicrostructureand pages 24-29, shahriari2023corrosionperformanceof pages 14-14, zhao2022microstructureandmechanical pages 1-2)
* Powder laser deposition onto **cast C95800** and **wrought Cu–Ni** with measured interface cracking/dilution and marine corrosion is not demonstrated by Li’s self-builds or Zhao’s 17-4PH joints. A retrieved review notes that another **CuNi2SiCr-on-cast-NAB** DED repair attempt produced porous, weak deposits; this is a *different deposited alloy*, and cannot be counted as successful NAB-powder repair. (li2021nanotwinscontainingmicrostructureand pages 4-9, nemani2024advancementsinadditive pages 79-83, zhao2022microstructureandmechanical pages 1-2)
* Distinguish **β retained at room temperature**, β′ or Li’s **β\*** martensite, and **κI–κIV** by appropriate diffraction/chemistry; do not infer all four κ variants from a generic XRD “κ” peak. Couple measured thermal cycles and layer position to phase fractions and selective attack; compare thermal-history-driven CALPHAD predictions with equilibrium-only and no-physics baselines rather than claiming phase-equilibrium calculations alone predict martensite. (li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 14-19, zhao2022microstructureandmechanical pages 2-4, dharmendra2019microstructuralevolutionand pages 9-13)
* The retrieved powder studies leave **lot-resolved Hall flow, apparent density, and often powder-feed mass rate or powder oxygen** unreported. Zhao provides powder oxygen **0.025 wt%**, but neither its value nor Li’s gas flow supplies a universal acceptable atomization specification. Measure those attributes separately for each composition/lot and model them as intermediate variables. (li2021nanotwinscontainingmicrostructureand pages 4-9, zhao2022microstructureandmechanical pages 2-4)

## Ranked: Top 5 things the PI should know

1. **Do not claim novelty for simply printing dense pre-alloyed NAB by laser powder DED:** Li already reports **99.55% density** and **769–949 MPa UTS**. The strongest differentiator is a *powder-lot → thermal history → as-deposited phase → matched long-duration seawater/repair performance* demonstration. (li2021nanotwinscontainingmicrostructureand pages 4-9, li2021nanotwinscontainingmicrostructureand pages 9-14, li2021nanotwinscontainingmicrostructureand pages 24-29)
2. **Retrieve and explicitly address the separate Zhao *Metals* 2022 NaCl corrosion paper.** It prevents an inaccurate “first laser-deposited NAB corrosion” claim, even though its **steel substrate** does not answer cast-NAB/Cu–Ni repair or C71500 equivalence. (zhao2022microstructureandmechanical pages 1-2)
3. **As-deposited is a scientifically consequential target, not a missing processing step.** WAAM’s approximately **1250 °F/6 h** treatment changed κ populations and degraded the tested short-term chloride electrochemistry relative to as-built WAAM; do not, however, portray this result as proof that the same treatment harms all cast or laser-DED NAB. (shahriari2023corrosionperformanceof pages 12-14, fayanas2025nickelaluminiumbronze pages 5-7, dharmendra2019microstructuralevolutionand pages 14-15)
4. **Optimize corrosion at the phase/interface scale, not hardness alone.** Cathodic κ near anodic α drives localized interdendritic attack; LPBF compositions show a strong martensite–ductility trade-off, while laser DED can produce β\*, Widmanstätten α and κII/NiAl together. Directly measure local attack and repair-interface behavior. (li2021nanotwinscontainingmicrostructureand pages 14-19, shahriari2023corrosionperformanceof pages 10-10, nemani2024advancementsinadditive pages 74-79)
5. **Preserve comparability in the proposal’s benchmark hierarchy:** identical surface finish, aeration/flow, reference electrode, exposure time and solution for as-deposited candidate, cast NAB, and **wrought C71500**, with full powder-lot metadata. In particular, a **24-h heat-treated versus 96-h as-built** electrochemical comparison, a **3.5% NaCl** polarization curve, and a **months-long seawater** mass-loss result are not interchangeable acceptance tests. (shahriari2023corrosionperformanceof pages 14-14, fayanas2025nickelaluminiumbronze pages 5-7, nemani2024advancementsinadditive pages 74-79)

References

1. (li2021nanotwinscontainingmicrostructureand pages 4-9): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

2. (li2021nanotwinscontainingmicrostructureand pages 9-14): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

3. (shahriari2023corrosionperformanceof pages 14-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

4. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

5. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

6. (li2021nanotwinscontainingmicrostructureand media e4936506): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

7. (li2021nanotwinscontainingmicrostructureand media b262c03b): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

8. (li2021nanotwinscontainingmicrostructureand pages 24-29): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

9. (li2021nanotwinscontainingmicrostructureand pages 14-19): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

10. (zhao2022microstructureandmechanical pages 1-2): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

11. (zhao2022microstructureandmechanical pages 2-4): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

12. (zhao2022microstructureandmechanical pages 11-12): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

13. (zhao2022microstructureandmechanical pages 9-11): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

14. (ziqiang2025lasercladdingremanufacturing pages 1-3): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

15. (ziqiang2025lasercladdingremanufacturing pages 3-6): Pi Ziqiang, Du Kaiping, Chen Xing, Zheng Zhaoran, and Wang Chen. Laser cladding remanufacturing of propeller zcual8mn13fe3ni2 alloy. Scientific Reports, Apr 2025. URL: https://doi.org/10.1038/s41598-025-96674-4, doi:10.1038/s41598-025-96674-4. This article has 7 citations and is from a peer-reviewed journal.

16. (dharmendra2019microstructuralevolutionand pages 2-3): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

17. (dharmendra2019microstructuralevolutionand pages 1-2): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

18. (dharmendra2019microstructuralevolutionand pages 9-13): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

19. (dharmendra2019microstructuralevolutionand pages 14-15): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

20. (dharmendra2019microstructuralevolutionand pages 13-14): C. Dharmendra, A. Hadadzadeh, B.S. Amirkhiz, G.D. Janaki Ram, and M. Mohammadi. Microstructural evolution and mechanical behavior of nickel aluminum bronze cu-9al-4fe-4ni-1mn fabricated through wire-arc additive manufacturing. Additive manufacturing, 30:100872, Dec 2019. URL: https://doi.org/10.1016/j.addma.2019.100872, doi:10.1016/j.addma.2019.100872. This article has 187 citations and is from a highest quality peer-reviewed journal.

21. (shahriari2023corrosionperformanceof pages 1-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

22. (shahriari2023corrosionperformanceof pages 12-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

23. (shahriari2023corrosionperformanceof pages 2-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

24. (shahriari2023corrosionperformanceof pages 10-10): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

25. (shahriari2023corrosionperformanceof pages 8-10): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

26. (nemani2024advancementsinadditive pages 113-114): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

27. (nemani2024advancementsinadditive pages 71-74): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

28. (fayanas2025nickelaluminiumbronze pages 1-2): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

29. (fayanas2025nickelaluminiumbronze pages 5-7): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

30. (fayanas2025nickelaluminiumbronze pages 2-5): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.
