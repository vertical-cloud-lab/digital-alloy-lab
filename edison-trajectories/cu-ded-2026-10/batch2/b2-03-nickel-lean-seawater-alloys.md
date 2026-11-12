<!--
Edison Scientific LITERATURE task (batch 2)
- Task ID: c9833365-3e58-47e0-a285-58a7c69d8305
- Submitted: 2026-10-17T05:37:01Z
- Fetched: 2026-10-17T06:08:53Z (status: success)
- Raw trajectory JSON: ../raw/b2-03-nickel-lean-seawater-alloys.json.gz
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

QUESTION: Which copper alloys with less nickel than 70-30 Cu-Ni come closest
to its seawater performance, and on what evidence? Compare 90-10 Cu-Ni,
Cu-Ni with Cr (C72200), manganese-aluminum bronze (C95700), aluminum bronzes
with and without Ni, Cu-Al-Fe-Mn, Cu-Ni-Sn, Cu-Ni-Al (e.g. Hiduron-type),
and Cu-Mn-Al alloys for general corrosion rate, velocity (erosion-corrosion)
limits, pitting and selective attack, sulfide resistance, and biofouling.
Give measured corrosion rates and critical velocities with test conditions.
Which of these have been made by any AM process, and with what corrosion
results? Is there evidence for a composition that matches 70-30 Cu-Ni with
substantially less nickel?

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

QUESTION: Which copper alloys with less nickel than 70-30 Cu-Ni come closest
to its seawater performance, and on what evidence? Compare 90-10 Cu-Ni,
Cu-Ni with Cr (C72200), manganese-aluminum bronze (C95700), aluminum bronzes
with and without Ni, Cu-Al-Fe-Mn, Cu-Ni-Sn, Cu-Ni-Al (e.g. Hiduron-type),
and Cu-Mn-Al alloys for general corrosion rate, velocity (erosion-corrosion)
limits, pitting and selective attack, sulfide resistance, and biofouling.
Give measured corrosion rates and critical velocities with test conditions.
Which of these have been made by any AM process, and with what corrosion
results? Is there evidence for a composition that matches 70-30 Cu-Ni with
substantially less nickel?

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


# Lower-nickel copper alloys for seawater-facing additive repair

**Bottom line.** Wrought **90–10 Cu–Ni (C70600)** is the best-established low-nickel substitute for wrought 70–30 Cu–Ni (C71500) in *ordinary, relatively clean seawater*: long exposures give similarly low general corrosion, although its conventional flow-design allowance is lower. **Cu–Ni–Cr C72200** has the strongest evidence for *exceeding* C71500’s resistance to fast seawater while using much less nickel, but it has not been shown here to match C71500 across prolonged immersion, sulfide exposure, localized attack, biofouling, and as-deposited powder-fed DED repair. Aluminum bronzes offer much lower nickel demand but have a consequential selective-phase-attack question. **No retrieved study demonstrates that one substantially lower-nickel composition meets the complete proposed, as-deposited C71500-equivalent specification.** (lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 48-55, berlangalabari2025theeffectof pages 4-7, nemani2024advancementsinadditive pages 79-83)

**Reading the numbers.** Compositions below are **wt%**, balance Cu unless specified; *mpy* means **0.0254 mm/year**. Historical tube-design velocities, laboratory critical velocities, cavitation tests, and sliding-wear tests are different measurements. A polarization-derived rate in NaCl is not a measured 30-day penetration rate in natural or ASTM D1141 substitute seawater. Unless explicitly identified as natural seawater, the cited laboratory electrolyte is NaCl solution. (lewis1981evaluationofcoppernickel pages 48-55, tang2004effectoflaser pages 2-4, berlangalabari2025theeffectof pages 2-4)

## Comparative seawater evidence

1. **Reference C71500 and lower-nickel C70600. [CITE] [NUMBERS] [NAVY]** R. O. Lewis and F. LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, technical report, 1981, DOI **10.2172/6255887**. **Process:** conventional tube/wrought-alloy seawater exposure, not AM. Approximately **Cu–30Ni–0.5Fe** versus **Cu–10Ni–1.4Fe**; the C70600 commercial composition is more specifically **9–11 Ni, 1–2 Fe, 0.5–1 Mn**. In the report’s low-velocity **quiet natural seawater**, C71500 lost **0.3–0.5 mpy (7.6–12.7 µm/y)** and C70600 **0.2–0.6 mpy (5.1–15.2 µm/y)**; at **2 ft/s (0.61 m/s)**, respectively **0.5–0.7 mpy (12.7–17.8 µm/y)** and **0.5–1.1 mpy (12.7–27.9 µm/y)**. Reported pitting was **1–3 mils (25–76 µm)** for C71500 and **1–2 mils (25–51 µm)** for C70600 in the respective low-flow tests. The table does not establish that these are lifetime maximum pit depths. The report gives accepted maximum **tube-design** velocities of **4.6 versus 3.6 m/s**; a *different*, temperature-dependent critical-shear experiment found **4.1 m/s at 12 °C, 479 dyn/cm²** for C71500 and **4.5 m/s at 27 °C, 431 dyn/cm²** for C70600. Do **not** interpret the reversal in those two critical speeds as superior C70600 design performance: temperatures and test criteria differ. (lewis1981evaluationofcoppernickel pages 43-48, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel media d926d953)

   **Long-term, fouling, and sulfide qualification. [NUMBERS]** C. Powell, *Corrosion and Biofouling Resistance Evaluation of 90-10 Copper-Nickel* (2004; report/article, **DOI not established**), describes **14 years** in tidal, quiet, and **0.6 m/s** flowing seawater: C70600’s rate declined and stabilized near **1.3 µm/y** after approximately **5–6 years**. This is *not* a matched 14-year C71500 comparison. Exposed 90–10 resists attached macrofouling, although microfouling and loosely removable growth occur; sulfides in polluted or stagnant seawater disrupt the developing protective oxide and increase corrosion/pitting. Lewis and LaQue’s **78-day natural-seawater** fouling comparison likewise found no visible fouling on **80Cu–20Ni**, versus *incipient* fouling on **70Cu–30Ni**; those observations cannot establish a quantitative 90–10-versus-70–30 fouling advantage under every condition. Cu–Ni chloride pitting and crevice attack are generally uncommon in clean seawater, but ammonia and sulfide invalidate an unconditional immunity claim. (powell2004corrosionandbiofouling pages 1-4, powell2004corrosionandbiofoulinga pages 4-6, lewis1981evaluationofcoppernickel pages 55-60)

2. **C72200, the unusually promising high-flow low-Ni comparator. [CITE] [NUMBERS] [GAP]** Lewis and LaQue, DOI **10.2172/6255887**; **conventional Cu–approximately 16Ni–0.5Cr**, reported as C72200. In the same historical low-flow comparison, its quiet-water corrosion was **0.4–0.9 mpy (10.2–22.9 µm/y)**, versus C71500’s **0.3–0.5 mpy**; at **0.61 m/s**, **0.8–1.2 mpy (20.3–30.5 µm/y)**, versus C71500’s **0.5–0.7 mpy**. Thus it is **not proven equal on general corrosion in that particular test**. Its accepted tubular design velocity is **>9.0 m/s**, and its measured critical velocity **12.0 m/s at 27 °C**, critical shear **2,969 dyn/cm²**—far above the other two alloys in the reported comparison. Separately, **30 days** of clean seawater at **2.0 m/s** yielded **16.4 and 20.1 µm/y** for two C72200 specimens, against **89.5 and 95.1 µm/y** for two C71500 specimens; this short, initially forming-film test conflicts with any simplistic ranking based on the other, lower-flow exposures. The report cautions that chromium-bearing Cu–Ni may be more locally attacked in quiet water. No directly verified **C72200 pre-alloyed-powder DED**, long-duration sulfide, or matched biofouling result was recovered. Crucially, **CuNi2SiCr** contains approximately **2% Ni** and added **Si**: it is *not* C72200. (lewis1981evaluationofcoppernickel pages 43-48, lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 55-60, nemani2024advancementsinadditive pages 79-83)

3. **Nickel-free aluminum bronze versus NAB. [CITE] [NUMBERS] [NAVY] [GAP]** Lewis and LaQue’s DOI **10.2172/6255887** compiles **one-year, equal-area, 0.6 m/s flowing-seawater** galvanic-couple data. *Uncoupled* generic aluminum bronze was **43.2 µm/y (1.7 mpy)**, generic nickel-aluminum bronze **150 µm/y (5.9 mpy)**, C70600 **30.5 µm/y**, and C71500 **20.3 µm/y**. These are **unspecified bronze grades and one particular exposure**, not evidence that every nickel-free bronze is superior to NAB. Equal-area coupling C71500/aluminum bronze gave **17.8/63.5 µm/y**, and C71500/NAB **43.2/142.2 µm/y**, respectively; the **deposit/substrate interface and exposed-area ratio** consequently matter. Independent modern *cast* NAB/MAB tests find α-, β-, and κ-phase-dependent localized attack rather than proof that low average loss prevents deep penetration. Neither the historical generic-bronze results nor available tests establish a comparable critical seawater velocity for C95400, C95800, or a nickel-free Cu–Al–Fe–Mn formulation. (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 55-60, berlangalabari2025theeffectof pages 1-2, berlangalabari2025theeffectof pages 7-11)

4. **C95700 manganese–aluminum bronze and Cu–Al–Fe–Mn/Cu–Mn–Al. [CITE] [NUMBERS] [NAVY] [GAP]** C. H. Tang, F. T. Cheng and H. C. Man, “Effect of laser surface melting on the corrosion and cavitation erosion behaviors of a manganese-nickel-aluminium bronze,” *Materials Science and Engineering A* **373** (2004) 195–203, DOI **10.1016/j.msea.2004.01.016**. **Process:** cast C95700 subsequently **laser-surface-melted—not laser cladding, DED, or an AM-built component**. Measured starting composition **Cu 75.6, Mn 10.8, Al 7.8, Fe 3.6, Ni 2.2**. In **quiescent 3.5 wt% NaCl, 23 °C, 12 h**, the as-received and best laser-melted specimens had mass-loss rates **31.85 and 16.59 µg/cm²·h** (*micro-unit lost in text extraction; check original typeset table before reuse*) and polarization **i_corr 9.52 and 4.26 µA/cm²**, **E_corr −372 and −290 mV versus SCE**. Hardness rose from **160 to 333 HV0.2** for that laser condition. A distinct **12-h, 20-kHz ultrasonic cavitation** test in 3.5% NaCl gave combined mass-loss rates **2,284 versus 431 µg/cm²·h**. Neither number is a **seawater pipe critical velocity** or long-term immersion result. The cast alloy’s preferential phase attack and its improved response after surface homogenization make the as-deposited phase distribution a material design variable. (tang2004effectoflaser pages 2-4, tang2004effectoflaser pages 4-6)

   C. Berlanga-Labari, A. Claver, M. V. Biezma-Moraleda and J. Fernández-Palacio, “The Effect of Kappa Phases on Tribocorrosion Behaviour of Nickel Aluminum Bronze (NAB) and Manganese Aluminum Bronze (MAB),” *Lubricants* **13** (2025) 290, DOI **10.3390/lubricants13070290**. **Process:** cast **CuAl10Fe5Ni5-type NAB** versus **CuAl10Mn12Fe5-type C95700 MAB**; these are *nominal*, not precise measured bulk compositions. **1 M NaCl, static polarization versus 3,600-s sliding with 10- or 40-N load**: approximately **0.02 mm/y** polarization-derived corrosion rate without wear, rising to approximately **0.1 mm/y** during wear; NAB OCP approximately **−250 mV**, MAB **−500 mV** (the provided excerpt does not establish the reference electrode). At **10 N**, wear coefficient was **5.5 × 10⁻⁶ mm³/N·m NAB** versus **2.2 × 10⁻⁶ MAB**; at **40 N**, **1.6 × 10⁻⁵** versus **6.1 × 10⁻⁶**. NAB pitted in wear tracks; MAB selectively attacked κ-rich regions. This demonstrates a trade-off, **not** seawater-wide MAB superiority, a nickel-free C95700 specification, or measured velocity thresholds. A genuinely **Ni-free Cu–Al–Fe–Mn or Cu–Mn–Al candidate** remains unqualified against C71500 by the recovered exposure evidence. (berlangalabari2025theeffectof pages 2-4, berlangalabari2025theeffectof pages 4-7, berlangalabari2025theeffectof pages 7-11)

5. **Cu–Ni–Sn and Cu–Ni–Al/Hiduron-type. [CITE] [GAP]** The quantitative literature recovered here does **not** provide matched natural-seawater rate, critical flow velocity, pit/phase-attack depth, sulfide tolerance, and biofouling against C71500 for either family. **Cu–15Ni–8Sn**, for example, is a lower-Ni alloy already manufactured by **LPBF from pre-alloyed powder**: G. Zhang *et al.*, “Additive manufacturing of fine-structured copper alloy by selective laser melting of pre-alloyed Cu-15Ni-8Sn powder,” *International Journal of Advanced Manufacturing Technology* **96** (2018) 4223–4230 (**DOI not verified in the available text**). Another LPBF corrosion example is approximately **Cu–14.8Ni–7Sn–1.6Pb** tested in **3% NaCl and 1 M HCl**; 3% NaCl is *not natural seawater*, and its retrieved review excerpt does not substantiate a C71500-equivalent rate. A **Cu–6.9Ni–2.97Al–0.99Fe–1.06Mn** *cast* alloy was described by R. Yang *et al.*, “Effect of heat treatment on microstructure and mechanical properties…,” *Materials Science and Technology* **36** (2020) 83–91, DOI **10.1080/02670836.2019.1684035**: reported strength improved **305→588 MPa only after solution treatment and 550 °C/6 h aging**; this is neither as-deposited seawater evidence nor evidence for a Hiduron-type alloy’s performance without aging. These families merit screening but **cannot presently be ranked above C70600 or C72200 on the complete seawater criteria**. (nemani2024advancementsinadditive pages 26-28, nemani2024advancementsinadditive pages 110-112)

## AM precedents: what is actually established

- **90–10 Cu–Ni, arc DED, not powder DED. [CITE] [NOVELTY-RISK] [GAP]** M. Maleta *et al.*, “Microstructure, Mechanical and Corrosion Properties of Copper-Nickel 90/10 Alloy Produced by CMT-WAAM Method,” *Materials* **17** (2024) article **50**, DOI **10.3390/ma17010050**; and J. Song, X. A. Jimenez, A. C. To and Y. Fu, “Microstructures and Corrosion Properties of Wire Arc Additive Manufactured Copper–Nickel Alloys,” *Materials* **17** (2024) article **876**, DOI **10.3390/ma17040876**. The accessible bibliography establishes **wire-arc/CMT Cu–Ni deposition with corrosion investigations**, defeating a claim that *AM Cu–Ni corrosion* is novel. Their full experimental text was not recovered: **no i_corr, E_corr, measured composition, porosity, test duration, or rate is asserted here**, and neither verifies one-stream pre-alloyed-*powder* laser DED on both proposed repair substrates. **Do not describe the wire papers as powder-fed DED.** (li2025additivemanufacturingprospects pages 18-19)

- **NAB LPBF, including actual seawater immersion. [CITE] [NUMBERS] [NOVELTY-RISK]** T. Murray, S. Thomas, Y. Wu, W. Neil and C. Hutchinson, “Selective laser melting of nickel aluminium bronze,” *Additive Manufacturing* **33** (2020) 101122, DOI **10.1016/j.addma.2020.101122**. **Process:** LPBF of pre-alloyed **Cu–9.8Al–5.2Ni–4.6Fe–0.3Mn** powder. The as-built martensitic material reportedly lost **approximately tenfold less mass** than *cast and wrought NAB counterparts* after **3 and 6 months’ seawater immersion**; the accessible review does **not** give absolute mass-loss/area, seawater chemistry, flow, or C71500 control. The as-printed condition was mechanically brittle; heat treatment altered the phases. **This is important evidence that as-built phase control may help corrosion, not evidence of C71500 equivalence or of crack-free DED.** C. Barr *et al.*, “Effect of composition on the tensile and corrosion performance of nickel aluminium bronze produced via laser powder bed fusion,” *Additive Manufacturing* **54** (2022) 102771, DOI **10.1016/j.addma.2022.102771**, already compare **pre-alloyed C63000 powder (Cu–10.2Al–4.8Fe–5.0Ni–0.2Si)** with **C95800 powder (Cu–9.0Al–4.0Fe–4.6Ni–1.9Mn)**. As-built C63000 achieved **~1,120 MPa UTS but ~3% elongation**; the retrieved review characterizes heat-treated corrosion as similar to wrought NAB, *not* as-deposited C71500-matched seawater resistance. Thus composition-dependent NAB AM corrosion itself is **not** novel. (nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 113-114)

- **NAB powder-fed laser DED and NAB-on-NAB precedent. [CITE] [NOVELTY-RISK] [GAP]** B. Li, H. Zheng, C. Han and K. Zhou, “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition,” *Additive Manufacturing* **39** (2021) 101825, DOI **not verified from its recovered reference list**: the review gives as-built **593–713 MPa yield strength, 769–949 MPa UTS, 10–12% elongation**. **No seawater-corrosion result was established for this particular deposition.** R. P. Doyle, *Additive Manufacturing of FeCrCoCuNi High Entropy Alloy via Laser Powder Bed Fusion and Nickel Aluminum Bronze via Laser Directed Energy Deposition* (thesis, 2022; **DOI unavailable in retrieved record**), demonstrates **wire-laser DED**, *not* powder-laser DED, using **Cu–8.64Al–4.2Ni–3.2Fe** C95800 wire: as-built **410.5 MPa YS, 757.8 MPa UTS, 29% elongation, 218.8 HV**; no verified seawater corrosion. C.-L. Yao and D.-S. Shim, “Corrosive properties of CuNi2SiCr fabricated through directed energy deposition on a nickel-aluminum bronze substrate,” *Journal of Alloys and Compounds* **918** (2022) 165776, DOI **10.1016/j.jallcom.2022.165776**, explicitly overlaps **powder-fed laser DED repair on cast NAB**, albeit with **CuNi2SiCr**, *not* C72200 or a demonstrated C71500-equivalent composition. The accessible review reports **porous CuNi2SiCr layers and inadequate reinforcement/hardness for propeller repair**; its corrosion numbers and test conditions were **not recoverable**, so avoid claiming they establish marine equivalence. (doyle2022additivemanufacturingof pages 53-58, doyle2022additivemanufacturingof pages 43-47, nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 113-114)

- **As-built NAB corrosion depends on deposition heat history. [CITE] [NUMBERS] [NOVELTY-RISK]** R. Huo *et al.*, “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing,” *Materials* **18** (2025) 2205, DOI **10.3390/ma18102205**. **Process:** wire-arc DED/CMT using *single pre-alloyed wire*, not powder; wire **Al 8.73, Fe 5.90, Ni 4.52, Mn 1.39**, balance Cu. In **aerated 3.5 wt% NaCl at 25 ± 5 °C**, increasing build heat input **243.8→644.7 J/mm** changed **i_corr 2.56 ± 0.04→7.52 ± 0.07 µA/cm²** and reported **E_corr approximately −270→−701 mV**; mean hardness **192.4→166.9 HV**. The article’s abstract also gives a different hardness comparison (**198.3→171.7 HV**); preserve each measure’s definition instead of combining them. No demonstrated density, 30-day immersion rate, flowing-seawater performance, or powder quality number follows from that result. (huo2025modulatingheatinput pages 15-16, huo2025modulatingheatinput pages 2-4, huo2025modulatingheatinput pages 4-5)

- **Nickel-free bronze and Cu–Ni–Sn feasibility is not the requested repair demonstration. [CITE] [NUMBERS] [NAVY] [GAP]** K. A. Timmons, A. Nasiri and D. P. Bishop, “Laser Powder Bed Fusion Processing of UNS C64200 Aluminum–Silicon–Bronze,” *Journal of Manufacturing and Materials Processing* **9** (2025) 147, DOI **10.3390/jmmp9050147**: **LPBF**, essentially Ni-free **Cu 91.89, Al 6.29, Si 1.52, Ni 0.05** measured in pre-alloyed powder. Argon-atomized powder had mean particle size **33 µm**, **3.1 g/s** powder-flow measurement, apparent density **4.45 g/cm³**; reported optimized product density **>99.9%**. The paper notes defense-standard applications and mechanical performance, **but supplies no demonstrated C71500-matched seawater-corrosion result in the retrieved evidence**; it is not a Cu–Al–Fe–Mn DED repair trial. LPBF **Cu–15Ni–8Sn** and LPBF **Cu–5/10/15Ni** likewise establish AM feasibility, whereas the identified laser-metal-deposition Cu–Ni study explicitly uses **blended powder feedstocks**, outside the one-pre-alloyed-powder novelty claim: S. Karnati, F. F. Liou and J. W. Newkirk, “Characterization of copper–nickel alloys fabricated using laser metal deposition and blended powder feedstocks,” *International Journal of Advanced Manufacturing Technology* **103** (2019) 239–250 (**DOI not established here**). Do not infer natural-seawater performance from either fabrication study. (nemani2024advancementsinadditive pages 26-28, timmons2025laserpowderbed pages 2-4, nemani2024advancementsinadditive pages 110-112)

**Unresolved scope.** The retrieved material does not support numerical **Hall-flow time, lot oxygen, apparent density, powder size or deposit porosity across the proposed custom pre-alloyed DED composition series**, except the distinct C64200 LPBF powder example above; nor does it supply directly comparable **sulfide resistance or marine biofouling** for C95700, Cu–Al–Fe–Mn, Cu–Ni–Sn, Cu–Ni–Al/Hiduron, and custom Cu–Mn–Al. Likewise, no defensible common **critical-flow velocity** can be assigned to these latter families from a 1 M NaCl sliding test or ultrasonic cavitation test. Available sources also do not validate composition→powder→deposit→microstructure→corrosion *function-network Bayesian optimization* or thermal-history-coupled CALPHAD against the specified baselines; these are potentially differentiating **methods**, not established corrosion results. The full texts of several particularly relevant newer AM articles were unobtainable, so absence of retrieved proof is **not proof that no such paper exists**. (lewis1981evaluationofcoppernickel pages 48-55, tang2004effectoflaser pages 2-4, berlangalabari2025theeffectof pages 7-11, nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 26-28)

## Top 5 things the PI should know

1. **Use C70600 as the defensible 10%-Ni, long-exposure general-corrosion benchmark—but acknowledge its lower 3.6 m/s tube-design allowance versus C71500’s 4.6 m/s.** [CITE] [NUMBERS] (powell2004corrosionandbiofouling pages 1-4, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48)
2. **Test C72200 early:** about **16% Ni** and exceptionally high reported velocity/shear threshold, but contradictory short- versus low-flow corrosion rankings make **long-duration pits and sulfides** essential discriminators. [CITE] [NUMBERS] [GAP] (lewis1981evaluationofcoppernickel pages 43-48, lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 55-60)
3. **Novelty is not “AM marine copper alloys” or “NAB corrosion”:** LPBF NAB seawater immersion, composition-dependent LPBF NAB corrosion, WAAM 90–10 corrosion, and powder DED CuNi2SiCr-on-NAB already exist. Distinguish **new pre-alloyed compositions, single-stream powder-laser DED, both repair substrates, as-deposited long-duration seawater outcomes, and linked cost-aware optimization**. [NOVELTY-RISK] [GAP] (nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 79-83, li2025additivemanufacturingprospects pages 18-19, nemani2024advancementsinadditive pages 113-114)
4. **Measure worst localized damage and the repair interface, not just i_corr:** MAB can outperform NAB under mechanical sliding yet selectively lose κ phases, and published equal-area bronze/Cu–Ni couples change corrosion rates. Specify deposit, heat-affected zone, substrate, coupled area, maximum attack depth, and exposure history. [NUMBERS] [NAVY] (lewis1981evaluationofcoppernickel pages 48-55, berlangalabari2025theeffectof pages 7-11, berlangalabari2025theeffectof pages 2-4)
5. **The decisive claim remains unproven:** there is **no verified as-deposited, dense/crack-free, substantially lower-Ni single-powder DED composition** that matches C71500 simultaneously on **30-day seawater loss, flow/erosion, pits/selective attack, sulfides, and fouling** on both NAB and Cu–Ni repair substrates. Treat it as the proposal’s testable objective, not a literature-established fact. [GAP] (lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 48-55, nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 79-83)

References

1. (lewis1981evaluationofcoppernickel pages 14-17): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

2. (lewis1981evaluationofcoppernickel pages 48-55): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

3. (berlangalabari2025theeffectof pages 4-7): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

4. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

5. (tang2004effectoflaser pages 2-4): C.H Tang, F.T Cheng, and H.C Man. Effect of laser surface melting on the corrosion and cavitation erosion behaviors of a manganese-nickel-aluminium bronze. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 373:195-203, May 2004. URL: https://doi.org/10.1016/j.msea.2004.01.016, doi:10.1016/j.msea.2004.01.016. This article has 168 citations.

6. (berlangalabari2025theeffectof pages 2-4): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

7. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

8. (lewis1981evaluationofcoppernickel media d926d953): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

9. (powell2004corrosionandbiofouling pages 1-4): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.

10. (powell2004corrosionandbiofoulinga pages 4-6): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.

11. (lewis1981evaluationofcoppernickel pages 55-60): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

12. (berlangalabari2025theeffectof pages 1-2): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

13. (berlangalabari2025theeffectof pages 7-11): Carlos Berlanga-Labari, Adrián Claver, María Victoria Biezma-Moraleda, and José Fernández-Palacio. The effect of kappa phases on tribocorrosion behaviour of nickel aluminum bronze (nab) and manganese aluminum bronze (mab). Lubricants, 13:290, Jun 2025. URL: https://doi.org/10.3390/lubricants13070290, doi:10.3390/lubricants13070290. This article has 4 citations.

14. (tang2004effectoflaser pages 4-6): C.H Tang, F.T Cheng, and H.C Man. Effect of laser surface melting on the corrosion and cavitation erosion behaviors of a manganese-nickel-aluminium bronze. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 373:195-203, May 2004. URL: https://doi.org/10.1016/j.msea.2004.01.016, doi:10.1016/j.msea.2004.01.016. This article has 168 citations.

15. (nemani2024advancementsinadditive pages 26-28): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

16. (nemani2024advancementsinadditive pages 110-112): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

17. (li2025additivemanufacturingprospects pages 18-19): Zeyuan Li, Hulong Ruan, Minghao Li, Chenglong Yu, Qixing Jia, Junjun Wang, and Lina Chen. Additive manufacturing: prospects and diverse applications. Metals, 15:158, Feb 2025. URL: https://doi.org/10.3390/met15020158, doi:10.3390/met15020158. This article has 15 citations.

18. (nemani2024advancementsinadditive pages 71-74): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

19. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

20. (nemani2024advancementsinadditive pages 113-114): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

21. (doyle2022additivemanufacturingof pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

22. (doyle2022additivemanufacturingof pages 43-47): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

23. (huo2025modulatingheatinput pages 15-16): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

24. (huo2025modulatingheatinput pages 2-4): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

25. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

26. (timmons2025laserpowderbed pages 2-4): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.
