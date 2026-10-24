<!--
Edison Scientific LITERATURE task (batch 3)
- Task ID: 19d70011-c7ec-47ef-a020-16561f510d45
- Submitted: 2026-10-17T05:46:08Z
- Fetched: 2026-10-17T06:16:58Z (status: success)
- Raw trajectory JSON: ../raw/b3-07-navy-funded-cu-am-programs.json.gz
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

QUESTION: Which research groups have had ONR, NAVSEA, NAVAIR, NRL, NSWC,
or other US Navy support (2018-2026) for additive manufacturing, welding or
repair of copper-nickel and nickel-aluminum bronze, according to the
acknowledgments and affiliations of their papers, theses and reports? For
each give the group, institution, process (WAAM, wire-laser DED, powder DED,
LPBF, cold spray, friction stir), alloy, topic, and grant number if
printed. Known leads: Song, Jimenez, To and Fu (ONR N00014-21-1-2800, WAAM
Cu-Ni corrosion); Lewandowski (Case Western, ONR, WAAM 70-30 Cu-Ni with
Lincoln Electric and NRL); Kuprienko (Ohio State, ONR Manufacturing Science,
WAAM NAB); Doyle (Oregon State, Navy grant, wire-laser DED NAB); Sparrow,
Smith and Ansell (Naval Postgraduate School, LPBF C71500); Norkett and Fisher
(NSWC Carderock, NAB and Cu-Ni property databases); Penn State ARL. Which
gaps do these programs leave for blown-powder DED and alloy design?

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

QUESTION: Which research groups have had ONR, NAVSEA, NAVAIR, NRL, NSWC,
or other US Navy support (2018-2026) for additive manufacturing, welding or
repair of copper-nickel and nickel-aluminum bronze, according to the
acknowledgments and affiliations of their papers, theses and reports? For
each give the group, institution, process (WAAM, wire-laser DED, powder DED,
LPBF, cold spray, friction stir), alloy, topic, and grant number if
printed. Known leads: Song, Jimenez, To and Fu (ONR N00014-21-1-2800, WAAM
Cu-Ni corrosion); Lewandowski (Case Western, ONR, WAAM 70-30 Cu-Ni with
Lincoln Electric and NRL); Kuprienko (Ohio State, ONR Manufacturing Science,
WAAM NAB); Doyle (Oregon State, Navy grant, wire-laser DED NAB); Sparrow,
Smith and Ansell (Naval Postgraduate School, LPBF C71500); Norkett and Fisher
(NSWC Carderock, NAB and Cu-Ni property databases); Penn State ARL. Which
gaps do these programs leave for blown-powder DED and alloy design?

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


# U.S. Navy–connected Cu–Ni and nickel-aluminum-bronze research, 2018–October 2026

**Scope and evidence standard.** “Navy-supported” below distinguishes an **explicit ONR award**, a **Navy grant mentioned without an identifier**, a **Navy laboratory or school affiliation**, and a **Navy application only**. These are not interchangeable. Compositions are **wt%** unless stated otherwise. “Not reported” means the accessible source does not establish the requested measurement; electrochemical results from hours in NaCl are not evidence of performance after 30 days in flowing seawater. No publications by the proposed PI are included. (song2024microstructuresandcorrosion pages 2-5, camilleri2025coldsprayas pages 1-2, song2024microstructuresandcorrosion pages 14-17, doyle2022additivemanufacturingof pages 1-9)

## Documented groups and item-level benchmarks

1. **Song–Jimenez–To–Fu; Virginia Tech and University of Pittsburgh — explicit ONR funding.** Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu, “Microstructures and Corrosion Properties of Wire Arc Additive Manufactured Copper–Nickel Alloys,” *Materials* **17** (2024), 876. DOI: **10.3390/ma17040876**. **Process/alloy:** cold-metal-transfer **wire-arc DED (WAAM)**, using TECHALLOY 413 wire: Cu 67.5, Ni 30, Mn 0.7, Fe 0.55, Ti 0.25, Si 0.1; comparator **wrought** C71500 plate: Cu 68.046, Ni 30.46, Mn 0.73, Fe 0.56. **Test:** naturally aerated **3.5 wt% NaCl**, room temperature, **3 h** open-circuit exposure before impedance and cyclic polarization; no natural-seawater flow or 30-day immersion established. The favorable WAAM setting used 8 m/min wire feed, 1,000 mm/min travel and 3.85 mm track spacing. Optical examination found no visible pores or cracks, but did **not** establish a numerical relative density. Its fitted film resistance was **1.40 × 10⁵ Ω (XY)** and **1.66 × 10⁵ Ω (YZ)**, versus **1.08 × 10⁵** and **1.18 × 10⁵ Ω**, respectively, for the wrought comparator; these are fitted film resistances, **not** reported polarization resistances or corrosion rates. This deposit also had the lowest measured *passive* current density; an independently established numerical *corrosion* current density or long-term rate should not be inferred. The study identifies preferential attack in Ni-depleted interdendritic regions and acknowledges **ONR N00014-21-1-2800**. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK: as-built AM Cu–Ni already outperformed a wrought comparator in a short chloride test] [GAP: wire, not pre-alloyed blown powder; no flowing/long-term seawater or NAB/Cu–Ni repair interface].** (song2024microstructuresandcorrosion pages 1-2, song2024microstructuresandcorrosion pages 2-5, song2024microstructuresandcorrosion pages 13-14, song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 14-17)

2. **Lewandowski group, Case Western Reserve University; Lincoln Electric and NRL connection — explicit ONR funding.** Oluwatumininu Olugbemiga Adeeko, *Processing/Structure/Properties of Wire-Arc Additively Manufactured 70Cu–30Ni Alloy*, M.S. thesis, Case Western Reserve University, January **2026**; advisor John J. Lewandowski. **No thesis DOI verified.** **Process/alloy:** Lincoln Electric TECHALLOY 413 **WAAM**, Cu 67.5, Ni 30, Mn 0.7, Fe 0.55, Ti 0.25, Si 0.1; 160 × 60 × 180 mm deposit, 100% Ar shielding. The investigated block used **175 °C interpass**; a **120 °C** block was provided to **Steven Policastro at NRL**. Some specimens were subsequently treated at **650 °C for ≥5 h**; as-deposited and treated results must therefore be kept separate. **Tests:** tensile, impact and fatigue in air, plus exploratory slow-strain-rate tensile tests at **10⁻⁶ s⁻¹**, **20 °C**, in **ASTM D1141 substitute seawater, pH 8.2**, against air controls. For as-deposited x-oriented specimens, air versus solution gave **yield 262 versus 257 MPa, UTS 360 versus 358 MPa, and reduction in area 70% versus 69%**; y-oriented results were **278 versus 245 MPa**, **370 versus 348 MPa**, and **66% versus 76%**, respectively. These are **environmental tensile** measurements, **not** corrosion-current, immersion-loss, or 30-day service-life measurements. The thesis acknowledges **ONR-N00014-24-1-2165**, names Lincoln Electric collaborators, and identifies the NRL recipient. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK: ONR already funds 70–30 Cu–Ni fabrication and artificial-seawater testing] [GAP: powder feed, low-Ni composition search, repair substrates and prolonged corrosion remain unestablished].** (adeeko2026processingstructurepropertiesofwirearc pages 1-7, adeeko2026processingstructurepropertiesofwirearc pages 48-54, adeeko2026processingstructurepropertiesofwirearc pages 36-43, adeeko2026processingstructurepropertiesofwirearc pages 15-20, adeeko2026processingstructurepropertiesofwirearc pages 118-123)

3. **Fink–Kuprienko group, Ohio State University, with Edison Welding Institute — explicit ONR Manufacturing Science funding.** Alexey Kuprienko, *Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate*, Ph.D. dissertation, Ohio State, **2025** (**DOI not verified**); related publication: Alexey Kuprienko, Jacob Stickle, Dennis Harwig, Michael Carney, and Carolin Fink, “Effect of liquid nitrogen cryogenic cooling during wire arc directed energy deposition of nickel aluminum bronze,” *Welding in the World* **68** (2024), 515–524, DOI: **10.1007/s40194-024-01692-x**. **Process/alloy:** pulsed-GMAW **wire-arc DED**, MIL-CuNiAl wire **Cu 81.35, Al 9.09, Fe 3.94, Ni 4.53, Mn 1.00**, deposited on **wrought C63200 NAB**. NAVSEA-directed interpass limits were **232–260 °C for the first three layers** and **149–177 °C subsequently**. Liquid-nitrogen trailing cooling reduced build time **22%** and distortion **40%** for a wall, and **15%/31%** for a multibead block; placing cooling too close to the arc could instead coarsen the microstructure and lower hardness. A dissertation tensile series for as-deposited block material lists **105.7–106.5 ksi UTS**, **60.0–60.9 ksi yield**, and **27.2–31.9% elongation**. **No corrosion electrolyte, duration or corrosion metric** was established for this work. The dissertation explicitly credits ONR Manufacturing Science **contract N01294684**; do not automatically attribute that dissertation contract identifier to every separate publication without checking its own acknowledgement. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK: Navy-funded NAB deposition, NAB-substrate interfaces and thermal-history modeling are not new] [GAP: not blown-powder DED or demonstrated as-deposited seawater corrosion].** (kuprienko2025analysisofnickel pages 1-7, kuprienko2025analysisofnickel pages 67-72, kuprienko2025analysisofnickel pages 72-76, kuprienko2025analysisofnickel pages 81-87, kuprienko2025analysisofnickel pages 173-177)

4. **Pasebani–Doyle group, Oregon State University/ATAMI — Navy grant acknowledged, number unverified.** Ryan Patrick Doyle, *Additive Manufacturing of FeCrCoCuNi High Entropy Alloy via Laser Powder Bed Fusion and Nickel Aluminum Bronze via Laser Directed Energy Deposition*, M.S. thesis, Oregon State University, **2022** (**DOI not verified**); NAB chapter coauthors Ryan Doyle, Milad Ghayoor, Jakub Preis and Somayeh Pasebani. **Process/alloy:** **wire-laser DED**, *not* blown powder, of C95800 wire **Cu 82.0, Al 8.64, Ni 4.21, Fe 3.19, Mn 1.32, Si 0.05** on a **stainless-steel** build plate; a MELTIO M450 used six 976-nm diode lasers and 0.89-mm wire. Four screened laser/scan conditions gave **99.58–99.89% relative density** in deposited NAB characterization cubes. **As deposited:** yield **410.5 ± 6.3 MPa**, UTS **757.8 ± 5.4 MPa**, elongation **29.0 ± 1.0%**, hardness **218.8 ± 4.4 HV**; annealing at **675 °C for 6 h** gave **372.2 ± 6.7 MPa**, **714.5 ± 8.3 MPa**, **31.2 ± 0.25%**, and **204.1 ± 3.1 HV**, respectively. **No corrosion test** was performed. The NAB chapter states that OSU authors “will acknowledge” a Navy grant, but prints **no award number**; this wording supports a Navy-grant connection, not a verified ONR award. **Caution:** the thesis’s separate **99.8% LPBF-density** claim in its abstract concerns an FeCrCoCuNi *high-entropy alloy*; the NAB densities above come instead from the NAB chapter’s own table. **[CITE] [NUMBERS] [NAVY: chapter’s stated grant acknowledgement] [NOVELTY-RISK: dense, strong, as-deposited laser-DED NAB exists] [GAP: wire feed, stainless rather than cast-NAB substrate, no seawater results].** (doyle2022additivemanufacturingof pages 1-9, doyle2022additivemanufacturingof pages 43-47, doyle2022additivemanufacturingof pages 47-53, doyle2022additivemanufacturingof pages 53-58)

5. **Sparrow–Smith–Ansell, Naval Postgraduate School — Navy institutional affiliation, not a verified ONR award.** Andrew Sparrow, Walter Smith and Troy Y. Ansell, “LPBF Parameter Optimization of Mechanical, Non-Thermal Generated C71500 Powder,” *Metals* **16** (2026), 10; published **21 December 2025**. DOI: **10.3390/met16010010**. **Process/alloy:** **LPBF**, C71500 nominally Cu–30Ni made from **mechanically cut, non-atomized bar-stock powder**, not ultrasonic-atomized pre-alloyed blown-powder feed. Powder **D10/D50/D90 = 24/44/77 µm**, apparent density **3.12 g cm⁻³**, tap density **4.26 g cm⁻³**; a Hall-flow value was **not reported**. LPBF specimens reached **>99.8% relative density**, **165–175 HV0.2**; horizontal optimized specimens reached **404.0–423.3 MPa UTS**, **360.6–379.2 MPa yield**, and **24.8–32.0% elongation**, whereas vertical specimens were appreciably weaker. An approximately **5 wt% oxygen EDS signal** is **not a reliable bulk powder-oxygen measurement**: the authors specifically call for inert-gas-fusion analysis. They used Gaussian-process parameter optimization, but **did not measure seawater corrosion** or optimize alloy chemistry. **[CITE] [NUMBERS] [NAVY: NPS affiliation] [NOVELTY-RISK: Navy researchers already combine Cu–Ni powder AM and machine learning] [GAP: LPBF versus single-stream blown-powder DED; inadequate oxygen quantification and no corrosion qualification].** (sparrow2025lpbfparameteroptimization pages 3-6, sparrow2025lpbfparameteroptimization pages 11-12, sparrow2025lpbfparameteroptimization pages 1-3, sparrow2025lpbfparameteroptimization pages 8-11)

6. **Penn State/NSWC Carderock–connected NAB simulation and property-data effort — Navy affiliation; award unverified.** Glenn W. Hatala, Qian Wang, Edward W. Reutzel, Charles R. Fisher and Jennifer K. Semple, “A Thermo-Mechanical Analysis of Laser Hot Wire Additive Manufacturing of NAB,” *Metals* **11** (2021), 1023. DOI: **10.3390/met11071023**. **Process/alloy:** **laser-hot-wire DED** of nominal **C95800 NAB**, with experimentally measured temperature-dependent material properties incorporated into distortion calculations; constant room-temperature properties sometimes even predicted displacement in the **opposite direction**. This is thermal-mechanical modeling, **not** a corrosion or powder-lot study; a full elemental composition, marine exposure protocol and award number could not be verified because the retrieved article full text was inaccessible. Related NSWC-linked lead: Sean M. Orzolek, Jennifer K. Semple and Charles R. Fisher, “Influence of processing on the microstructure of Nickel Aluminum Bronze (NAB),” *Additive Manufacturing* **56** (2022), 102859, DOI: **10.1016/j.addma.2022.102859**; its inaccessible primary text does **not** justify assigning a Navy grant or quantitative corrosion result. **[CITE] [NAVY: Navy-laboratory-linked researchers] [NOVELTY-RISK: thermally informed NAB modeling has precedent] [GAP: phase predictions and corrosion validated against actual powder-DED thermal histories remain unestablished].** (hatala2021athermomechanicalanalysis pages 1-1, nemani2024advancementsinadditive pages 60-62, doyle2022additivemanufacturingof pages 43-47)

7. **Norkett–Fisher, NSWC Carderock — Navy laboratory affiliation; property databases, not alloy-design/corrosion demonstrations.** Searchable bibliographic records identify Justin E. Norkett and Charles R. Fisher, “Temperature-dependent material property database of cast 70/30 Cu–Ni material,” *Integrating Materials and Manufacturing Innovation* (2025), DOI: **10.1007/s40192-025-00409-2**; and “Temperature-dependent material property database for 90/10 Cu–Ni plate,” *Integrating Materials and Manufacturing Innovation* **15** (2026), 169–180, DOI: **10.1007/s40192-026-00444-7**. A related Justin E. Norkett, Jack H. Canaday, Sean M. Orzolek and Charles R. Fisher NAB **wire-arc** property-database article has DOI **10.1007/s40192-026-00454-5**. **Processes/alloys:** respectively **cast** nominal Cu–30Ni, **wrought plate** nominal Cu–10Ni, and **WAAM NAB**. The source texts were not obtainable: exact chemistries, award numbers and numerical property curves **cannot responsibly be supplied**. These are valuable thermal-model input leads, not evidence of seawater corrosion performance. **[CITE] [NAVY: NSWC affiliation as supplied by lead] [GAP: measured property inputs do not constitute thermal-history CALPHAD validation or repair qualification].** (kuprienko2025analysisofnickel pages 72-76)

8. **Penn State ARL acknowledged in a cold-spray NAB collaboration — *not* demonstrated U.S.-Navy funding.** Steven Camilleri, Tien Tran, Andrew Duguid and Kannoorpatti Narayanan Krishnan, “Cold spray as a powder metallurgy process for production of nickel aluminium bronze,” *PLOS ONE* **20** (2025), e0319333. DOI: **10.1371/journal.pone.0319333**. Authors are affiliated with **Charles Darwin University and SPEE3D, Australia**; funding is identified as **Australian Department of Education NIPhD 35017**, while **Penn State ARL and SPEE3D** are thanked for support. **Process/alloy:** **cold spray** of an *elemental/master-alloy blend*, comprising **11 wt% Al6061 powder, 5.8 wt% elemental Ni, 6.8 wt% elemental Fe and balance Cu powder**; this is **not** a pre-alloyed NAB powder and 11% Al6061 is **not** 11% elemental Al. Approximately **2% as-sprayed porosity/98% density** was reported; after homogenization/aging plus HIP, NAB attained **289 ± 1.6 MPa yield, 512 ± 2.7 MPa UTS, 22 ± 0.3% elongation and 160 ± 1.8 HB**. Without HIP, after sintering and aging, the corresponding numbers were **257 ± 1.1 MPa, 404 ± 2.9 MPa, 10 ± 0.7%, 150 ± 1.9 HB**. **No seawater corrosion test** is reported; the final mechanical performance depends on **substantial post-deposition processing**. **[CITE] [NUMBERS] [NAVY: only a potential maritime/ARL connection, *not* an established Navy award] [NOVELTY-RISK: other groups tailor Cu-alloy powder compositions] [GAP: elemental-blend solid-state deposition plus HIP does not meet single-stream, as-deposited powder-laser-DED objective].** (camilleri2025coldsprayas pages 10-12, camilleri2025coldsprayas pages 1-2, camilleri2025coldsprayas pages 3-6, camilleri2025coldsprayas pages 8-10)

**Important adjacent comparator, not a confirmed U.S.-Navy program.** Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz and Mohsen Mohammadi, “Corrosion performance of wire arc additively manufactured NAB alloy,” *npj Materials Degradation* **7** (2023), DOI: **10.1038/s41529-023-00405-x**. **Process/alloy:** **WAAM** C95800-class NAB versus **cast** NAB and heat-treated WAAM; **test:** **3.5 wt% NaCl** electrochemistry, not demonstrated long-duration flowing seawater. After **350 °C/2 h**, the reported *corrosion* current was approximately **4.4 µA cm⁻²** with charge-transfer resistance approximately **10.2 kΩ cm²**; **550 °C/4 h** gave approximately **6.6 µA cm⁻²** and **2.58 kΩ cm²**; **675 °C/6 h** gave approximately **8 µA cm⁻²** and **3.8 kΩ cm²**. The as-built material resisted chloride corrosion better than the more strongly heat-treated conditions. The retrieved evidence **does not establish U.S.-Navy funding** or a selective-attack depth. **[CITE] [NUMBERS] [GAP: strong justification for qualifying the *as-deposited* microstructure, not just heat-treated properties].** (shahriari2023corrosionperformanceof pages 1-2, shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 10-12)

**Friction-stir classification.** The retrieved Ohio State dissertation discusses **friction-stir processing of cast NAB** as background, but those cited experiments are **not** proof of a 2018–2026 Navy-funded powder-DED or friction-stir-repair program. Likewise, a 2025 Ohio State WAAM-NAB fatigue thesis establishes an institutional study and approximately **9 MPa√m** fatigue-crack-growth threshold, but its accessible acknowledgement **does not name Navy funding**. Neither should be relabeled ONR-supported. (kuprienko2025analysisofnickel pages 41-45, heniken2025influenceofmicrostructure pages 1-8)

## What remains genuinely open—and what does not

The defensible novelty is **not** “first AM of Cu–Ni,” “first laser DED of NAB,” “first powder AM of C71500,” “first NAB repair/substrate study,” or “first thermally informed AM model”: those claims collide with the work above. The stronger, **testable combination** is *one chemically controlled, pre-alloyed powder stream*; an in-house **composition → atomization/oxygen/flow → blown-powder laser DED → deposit and cast-NAB/wrought-Cu–Ni interfaces → as-deposited, long-duration seawater response** chain; and an ablation showing that **CALPHAD along measured/modelled local thermal histories** predicts microstructure and corrosion better than equilibrium-only CALPHAD and physics-free models. This is a **gap in the evidence examined, not a claim that no paper anywhere has attempted any individual element**. In particular, already-identified powder-laser-DED NAB and Cu–Ni-on-NAB literature could not be inspected sufficiently to declare powder deposition or repair itself unprecedented. (nemani2024advancementsinadditive pages 102-105, kuprienko2025analysisofnickel pages 55-61, doyle2022additivemanufacturingof pages 43-47, doyle2022additivemanufacturingof pages 47-53)

A rigorous proposal should compare **identical surface finish, orientation, exposed area, solution, oxygenation, temperature and flow** for wrought C71500, cast NAB, parent Cu–Ni, deposit and **cross-interface specimens**. Separate early screening by polarization/EIS from **30-day immersion, mass loss and maximum localized/selective-attack depth**; report powder size distribution, **Hall flow, apparent density and bulk oxygen by an appropriate chemical method** for every composition. None of the confirmed studies above supplies a complete matched dataset for those endpoints. The Song study also changes minor **Ti/Si** levels relative to its wrought comparator, so its short-term superiority cannot be attributed solely to the WAAM microstructure. (song2024microstructuresandcorrosion pages 1-2, sparrow2025lpbfparameteroptimization pages 11-12, song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 14-17)

## Top 5 things the PI should know

1. **Closest funded corrosion precedent:** Song et al.’s **ONR N00014-21-1-2800** study already beats a wrought 70–30 comparator in a **3-h/3.5%-NaCl electrochemical** comparison; win on **powder chemistry, rigorously matched interfaces and long-duration seawater**, not that headline alone. (song2024microstructuresandcorrosion pages 2-5, song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 14-17)
2. **Closest funded thermal/NAB precedent:** Ohio State’s ONR-funded NAB WAAM work already studies **cast/wrought NAB interfaces, controlled cooling and thermal modeling**; differentiate through **powder-laser thermal histories, microstructural phase prediction, and as-deposited corrosion validation**. (kuprienko2025analysisofnickel pages 1-7, kuprienko2025analysisofnickel pages 67-72, kuprienko2025analysisofnickel pages 72-76)
3. **Laser DED NAB is demonstrably established:** Oregon State reported **99.58–99.89% dense wire-laser NAB** and **410.5 MPa yield/757.8 MPa UTS as deposited**, but **no corrosion testing**. Do not transfer its separate high-entropy-alloy density figure to NAB. (doyle2022additivemanufacturingof pages 1-9, doyle2022additivemanufacturingof pages 47-53, doyle2022additivemanufacturingof pages 53-58)
4. **Powder and modeling novelty must be narrowly stated:** NPS already demonstrated **>99.8%-dense C71500 LPBF** with Gaussian-process optimization, while its own study warns that **EDS oxygen is not a bulk oxygen assay**. In-house ultrasonic atomization and a **cost-aware *network* of surrogates** must be shown to add value beyond LPBF process tuning. (sparrow2025lpbfparameteroptimization pages 6-8, sparrow2025lpbfparameteroptimization pages 11-12, sparrow2025lpbfparameteroptimization pages 8-11)
5. **The central service-life claim is still unsupported by these precedents:** short stationary NaCl electrochemistry, artificial-seawater tensile tests, and heat-treated cold-spray strength are **not** an as-deposited, **30-day flowing-seawater** comparison of pre-alloyed **low-Ni** powder-DED deposits and dissimilar-metal repairs against wrought C71500. Treat that full comparison as the proposal’s qualification target, not a result already demonstrated. (camilleri2025coldsprayas pages 1-2, adeeko2026processingstructurepropertiesofwirearc pages 48-54, song2024microstructuresandcorrosion pages 14-17, adeeko2026processingstructurepropertiesofwirearc pages 118-123, doyle2022additivemanufacturingof pages 53-58)

References

1. (song2024microstructuresandcorrosion pages 2-5): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

2. (camilleri2025coldsprayas pages 1-2): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

3. (song2024microstructuresandcorrosion pages 14-17): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

4. (doyle2022additivemanufacturingof pages 1-9): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

5. (song2024microstructuresandcorrosion pages 1-2): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

6. (song2024microstructuresandcorrosion pages 13-14): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

7. (song2024microstructuresandcorrosion pages 10-13): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

8. (adeeko2026processingstructurepropertiesofwirearc pages 1-7): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

9. (adeeko2026processingstructurepropertiesofwirearc pages 48-54): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

10. (adeeko2026processingstructurepropertiesofwirearc pages 36-43): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

11. (adeeko2026processingstructurepropertiesofwirearc pages 15-20): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

12. (adeeko2026processingstructurepropertiesofwirearc pages 118-123): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

13. (kuprienko2025analysisofnickel pages 1-7): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

14. (kuprienko2025analysisofnickel pages 67-72): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

15. (kuprienko2025analysisofnickel pages 72-76): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

16. (kuprienko2025analysisofnickel pages 81-87): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

17. (kuprienko2025analysisofnickel pages 173-177): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

18. (doyle2022additivemanufacturingof pages 43-47): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

19. (doyle2022additivemanufacturingof pages 47-53): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

20. (doyle2022additivemanufacturingof pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

21. (sparrow2025lpbfparameteroptimization pages 3-6): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

22. (sparrow2025lpbfparameteroptimization pages 11-12): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

23. (sparrow2025lpbfparameteroptimization pages 1-3): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

24. (sparrow2025lpbfparameteroptimization pages 8-11): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

25. (hatala2021athermomechanicalanalysis pages 1-1): Glenn W. Hatala, Qian Wang, Edward W. Reutzel, Charles R. Fisher, and Jennifer K. Semple. A thermo-mechanical analysis of laser hot wire additive manufacturing of nab. Metals, 11:1023, Jun 2021. URL: https://doi.org/10.3390/met11071023, doi:10.3390/met11071023. This article has 20 citations.

26. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

27. (camilleri2025coldsprayas pages 10-12): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

28. (camilleri2025coldsprayas pages 3-6): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

29. (camilleri2025coldsprayas pages 8-10): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

30. (shahriari2023corrosionperformanceof pages 1-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

31. (shahriari2023corrosionperformanceof pages 12-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

32. (shahriari2023corrosionperformanceof pages 10-12): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

33. (kuprienko2025analysisofnickel pages 41-45): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

34. (heniken2025influenceofmicrostructure pages 1-8): NH Heniken. Influence of microstructure on fatigue behavior, crack initiation, and crack growth in wire-arc additively manufactured nickel aluminum-bronze. Unknown journal, 2025.

35. (nemani2024advancementsinadditive pages 102-105): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

36. (kuprienko2025analysisofnickel pages 55-61): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

37. (sparrow2025lpbfparameteroptimization pages 6-8): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.
