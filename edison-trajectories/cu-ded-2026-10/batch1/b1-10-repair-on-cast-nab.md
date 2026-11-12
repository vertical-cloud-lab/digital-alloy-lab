<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: 0112f9fd-a99c-45d7-9b7a-dd53c3a55555
- Submitted: 2026-10-17T05:10:48Z
- Fetched: 2026-10-17T05:42:12Z (status: success)
- Raw trajectory JSON: ../raw/b1-10-repair-on-cast-nab.json.gz
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

QUESTION: What is known about depositing copper alloys by laser DED, laser
cladding or arc processes onto cast NAB and wrought Cu-Ni for repair? Cover
dilution, fusion-line defects, liquation and solidification cracking, the
heat-affected zone in cast NAB (kappa dissolution, martensite formation,
hardness peaks), residual stress, and the corrosion of the fusion zone and
HAZ (galvanic coupling between deposit and substrate). Also cover dissimilar
deposition of Cu-Ni or NAB on steel, since the Navy uses bimetallic parts.
How do existing studies judge repair quality, and which tests would a Navy
reviewer expect?

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

QUESTION: What is known about depositing copper alloys by laser DED, laser
cladding or arc processes onto cast NAB and wrought Cu-Ni for repair? Cover
dilution, fusion-line defects, liquation and solidification cracking, the
heat-affected zone in cast NAB (kappa dissolution, martensite formation,
hardness peaks), residual stress, and the corrosion of the fusion zone and
HAZ (galvanic coupling between deposit and substrate). Also cover dissimilar
deposition of Cu-Ni or NAB on steel, since the Navy uses bimetallic parts.
How do existing studies judge repair quality, and which tests would a Navy
reviewer expect?

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


# Copper-alloy deposition for naval repair: evidence and qualification priorities

**Scope and evidence limits.** Laser deposition *onto cast nickel–aluminum bronze (NAB)* has been studied, as has arc deposition onto cast NAB and copper-alloy deposition onto steel. The accessible evidence does **not** establish a qualified, single-stream **pre-alloyed-powder** laser-DED repair of **wrought C71500 Cu–Ni** that is dense, crack-free, and demonstrably as corrosion-resistant as wrought C71500 in long-duration seawater exposure. Several particularly pertinent original papers were identifiable by DOI but their full results were unavailable; findings attributed to those papers through a review are identified as **review-reported** below. Compositions are wt% unless specified. A value not reported or verified is marked **NR**, rather than inferred. Most cited electrochemical experiments use *3.5% NaCl*, not natural seawater or ASTM D1141 substitute seawater; their currents must not be treated as interchangeable with 30-day seawater penetration rates. (nemani2024advancementsinadditive pages 102-105, nemani2024advancementsinadditive pages 79-83, shahriari2023corrosionperformanceof pages 14-14)

## Directly relevant deposition and repair

1. **Hyatt, C. V., Magee, K. H., and Betancourt, T. “The effect of heat input on the microstructure and properties of nickel aluminum bronze laser clad with a consumable of composition Cu-9.0Al-4.6Ni-3.9Fe-1.2Mn.” *Metallurgical and Materials Transactions A* 29 (1998): 1677–1690. DOI: 10.1007/s11661-998-0090-5.** **Process:** laser cladding, wire consumable **Cu–9.0Al–4.6Ni–3.9Fe–1.2Mn**, onto **cast NAB**. A detailed subsequent review of this work reports single- and multibead experiments at **42.5–595 J/mm**: the lowest-input deposits were predominantly β martensite with some grain-boundary α; Widmanstätten α increased with input, and hardness generally decreased, although reported peak microhardness exceeded **300 HV** across conditions. Related thermal simulations found that rapid thermal cycling can transform initially cast-like phases into martensite; this is a strong rationale to measure the *substrate* HAZ, not only the added metal. **Seawater corrosion, dilution percentages, powder properties:** NR; this was wire, not powder deposition. **[CITE] [NUMBERS] [NOVELTY-RISK]** NAB-on-cast-NAB laser repair and thermal-history-sensitive phases precede the proposal. (kuprienko2025analysisofnickel pages 50-55)

2. **Kim, J.-s., Kim, J., and Pyo, C. “Comparison of Mechanical Properties of Ni-Al-Bronze Alloy Fabricated through Wire Arc Additive Manufacturing with Ni-Al-Bronze Alloy Fabricated through Casting.” *Metals* 10 (2020): 1164. DOI: 10.3390/met10091164.** **Process:** CMT **wire-arc DED/WAAM**, ERCuNiAl on **cast NAB**. Cast substrate: **Cu balance, 9.11 Al, 4.28 Ni, 3.3 Fe, 0.9 Mn**; wire: **Cu balance, 8.8 Al, 5.2 Ni, 3.3 Fe, 0.8 Mn**. At approximately **163–165 A, 11.8–12.0 V, 30 cm/min**, the deposited material averaged **727 MPa UTS, 408 MPa yield, 26.4% elongation**, versus cast substrate **597 MPa, 267 MPa, 16.4%**. Transverse/longitudinal deposit hardness averaged **196.8/218.4 HV**, versus cast **170.8 HV**; a bead-to-substrate traverse showed an HAZ as hard as or slightly harder than deposit. Deposit and cast Charpy absorbed energies were approximately **41.61 and 24.3 J**. **Tests:** ASTM E8 tension, ASTM E92 hardness, ASTM E23 impact, dry ball-on-disc wear; **no saline-corrosion, interfacial tensile, density or porosity qualification reported here**. Their assertion of a “50%” UTS improvement conflicts with the listed **727 versus 597 MPa**; use the actual numbers, not that percentage. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]** direct cast-substrate demonstration, but arc/wire rather than the proposed powder/laser process. (kim2020comparisonofmechanical pages 3-6, kim2020comparisonofmechanical pages 6-8, kim2020comparisonofmechanical pages 8-12)

3. **Yao, C.-L., Kang, H.-S., Lee, K.-Y., Zhai, J.-G., and Shim, D.-S. “A study on mechanical properties of CuNi2SiCr layered on nickel–aluminum bronze via directed energy deposition.” *Journal of Materials Research and Technology* 18 (2022): 5337–5361. DOI: 10.1016/j.jmrt.2022.04.159.** **Process:** laser DED of **CuNi2SiCr powder** onto **cast AlBC3 NAB**, intended for propeller repair; nominal designation implies approximately **2 Ni**, with Si and Cr concentrations **NR** in accessible evidence. **Review-reported:** porous, single-α-phase deposit without the substrate’s hard β/κ constituents; it had lower strength, hardness and wear resistance than NAB, and its authors advised **against** this particular propeller-repair combination. **Pore fraction, interface dilution, hardness, tensile figures, electrochemical conditions:** NR in accessible evidence. **[CITE] [NAVY] [NOVELTY-RISK]** directly overlaps laser-powder repair onto NAB; **[GAP]** does not validate a seawater-resistant Ni-bearing *NAB or 10–30 Ni Cu–Ni* powder. (nemani2024advancementsinadditive pages 113-114, nemani2024advancementsinadditive pages 79-83)

4. **Yao, C.-L., and Shim, D.-S. “Corrosive properties of CuNi2SiCr fabricated through directed energy deposition on a nickel-aluminum bronze substrate.” *Journal of Alloys and Compounds* 918 (2022): 165776. DOI: 10.1016/j.jallcom.2022.165776.** **Process:** laser DED **CuNi2SiCr onto NAB**. This is the **closest identifiable corrosion study for the proposed NAB fusion-line experiment**. The accessible review identifies its citation but does not supply its electrolyte, exposed configuration, individual deposit/FZ/HAZ current densities, coupling current, attack depths or duration. **Do not claim that this paper proves satisfactory—or unsatisfactory—galvanic performance without checking its original data.** **[CITE] [NAVY] [NOVELTY-RISK] [GAP]** a necessary paper to distinguish explicitly in the proposal. (nemani2024advancementsinadditive pages 113-114)

5. **Li, B., Zheng, H., Han, C., and Zhou, K. “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition.” *Additive Manufacturing* 39 (2021): 101825. DOI: 10.1016/j.addma.2021.101825.** **Process:** laser metal deposition, **Cu–9Al–5Fe–5Ni**, as built. **Review-reported:** β* martensite with approximately **250-nm** plates, Widmanstätten α, nanoscale Fe₃Al/NiAl and twins; **593–713 MPa yield, 769–949 MPa UTS, 10–12% elongation** over processing conditions. **Repair substrate, powder flow/oxygen, saline-corrosion and FZ/HAZ results:** NR in the evidence. **[CITE] [NUMBERS] [NOVELTY-RISK]** powder/laser NAB itself is *not new*; **[GAP]** its combined as-deposited repair/seawater performance remains unestablished here. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 113-114)

6. **Williams, N., Snyder, K., Smith, I., Duong, A., Carpenter, E., and Barua, R. “The First Layer: Single-Track Insights into Direct Energy Deposition Processed Cu-Ni Thermoelectric Alloys.” *Journal of Manufacturing and Materials Processing* 9 (2025): 170. DOI: 10.3390/jmmp9060170.** **Process:** blown-powder laser DED, **premixed *elemental* Cu and Ni**, nominal **Cu–35Ni**, single tracks **on 316L steel**, not pre-alloyed powder or Cu–Ni repair. Powder mean diameter **57 ± 15 µm**, apparent/tap densities **4.74/5.20 g/cm³**, Hall flow **0.3 g/s** (**50 g ≈167 s**), measured angle of repose **27.42°**; **powder oxygen NR**. At **800 W**, linear input **63–137 J/mm** and mass input **0.011–0.026 g/mm**, very low mass loading produced full steel penetration and **solidification-centerline hot cracks**. At **0.016 g/mm, 67 J/mm**, track height was approximately **500 µm**, substrate penetration approximately **100 µm**, with limited Fe dilution. Higher energy promoted Fe dilution/cracking; excessive powder loading gave poor steel interfacial mixing and trapped approximately **50-µm** unmelted Ni inclusions. The authors’ preferred windows were **<70 J/mm** at **0.016–0.021 g/mm** or **98–137 J/mm** at **0.026 g/mm**; this is a **qualitative single-track score**, not multilayer density or marine qualification. Note the article inconsistently describes its feed as an atomic **65:35** blend in one methods passage and **65:35 wt%** elsewhere; do not assume the former is its verified chemistry. **[CITE] [NUMBERS] [NOVELTY-RISK]** composition–process optimization and interface scoring already exist, albeit for elemental blends; **[GAP]** no seawater or cast-NAB/wrought-C71500 repair data. (williams2025thefirstlayer pages 2-4, williams2025thefirstlayer pages 6-9, williams2025thefirstlayer pages 9-11, williams2025thefirstlayer pages 4-6)

7. **Adak, B., Nash, P., Chen, D., and Swiglo, A. “Microstructural characterization of laser cladding of Cu-30Ni.” *Journal of Materials Science* 40 (2005): 2051–2054. DOI: 10.1007/s10853-005-1231-5.** **Process:** laser cladding **Cu–30Ni**; exact feed and substrate form, dilution, corrosion conditions and quantitative density/strength **not recoverable from the available cited material**. **[CITE] [NOVELTY-RISK]** laser-clad 70–30 composition is not unprecedented; **[GAP]** neither wrought-C71500 repair qualification nor 30-day seawater parity follows from this citation. (cheng2022anoverviewof pages 33-34)

8. **Karnati, S., Liou, F. F., and Newkirk, J. W. “Characterization of copper–nickel alloys fabricated using laser metal deposition and blended powder feedstocks.” *International Journal of Advanced Manufacturing Technology* 103 (2019): 239–250; and Karnati, S., Zhang, Y., Liou, F. F., and Newkirk, J. W. “On the feasibility of tailoring copper–nickel functionally graded materials fabricated through laser metal deposition.” *Metals* 9 (2019): 287, DOI: 10.3390/met9030287.** The first paper’s DOI is **NR in the retrieved bibliographic evidence**. **Process:** laser DED of **blended elemental Cu/Ni**, including compositionally graded structures—not a single pre-alloyed feed. A subsequent review reports approximately **4% discrepancy** between target and delivered Cu–Ni composition, use of modulated laser power to improve mixing, and porosity linked to elemental Ni powder oxygen; replacing pure Ni with a **96 wt% Ni** alloy containing some Si addressed that issue. **Marine tests/repair substrates:** NR. **[CITE] [NOVELTY-RISK]** Cu–Ni laser DED and adaptive process control already exist; **[GAP]** a separately atomized, single-stream alloy with measured lot oxygen and verified corrosion remains distinguishable. (nemani2024advancementsinadditive pages 110-112, chen2020areviewon pages 13-15, chen2020areviewon pages 10-13)

## Cast-NAB HAZ, cracking, residual stress, and as-deposited corrosion

9. **Kuprienko, A. “Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate.” 2025 thesis; persistent DOI **NR** in the available bibliographic record.** This is a *secondary technical synthesis plus its own arc experiments*, not a laser-repair paper. It notes that reheating cast NAB above its transformation temperatures can **dissolve or redistribute κ constituents**, produce high-temperature β, and generate α/β′ martensite during cooling; phase identifications based on dark optical contrast alone are unsafe. Electron diffraction in some arc-deposited NAB instead identified fine **α + κII + κIII** in apparently “martensitic” dark regions, **without martensite**. The reviewed laser-cladding thermal-simulation experiments used approximately **150 J/mm** clad material, **800–1000°C** HAZ/reheat peaks, and measured **188°C/s** air-quench and **750°C/s** water-quench cooling between 800 and 500°C; direct HAZ κ-solvus kinetics and depth-resolved seawater loss were not supplied. Distinguish **β′ formation in the cast substrate** from a β*-rich *as-deposited* NAB, and confirm by EBSD/TEM/XRD plus spatial phase and hardness mapping. **[CITE] [NUMBERS] [GAP]** equilibrium CALPHAD alone cannot establish retained phases after repeated thermal cycling. (kuprienko2025analysisofnickel pages 41-45, kuprienko2025analysisofnickel pages 45-50, kuprienko2025analysisofnickel pages 50-55, kuprienko2025analysisofnickel pages 55-61)

10. **Kuprienko, A., *ibid.*, original arc-on-wrought-NAB experimental chapters** (**same thesis; DOI NR**). **Process:** pulsed-GMA **wire-arc DED** MIL-CuNiAl wire **Cu–9.09Al–3.94Fe–4.53Ni–1.00Mn** on **wrought C63200 NAB**, **not cast NAB or Cu–Ni**. The experiment maintained interpass approximately **232–260°C for layers 1–3** and **149–177°C thereafter**, citing a NAVSEA DED process publication. It performed **visual, liquid-penetrant, radiographic or ultrasonic inspection**, tensile tests both *within deposit and across the substrate interface*, **12%-outer-fiber-strain bends**, **−20°C Charpy**, and **HV0.3 maps**. Block/wall deposit mean hardness **204/187 HV0.3**; HAZ reached locally **278 HV0.3**—the author cautions these isolated maxima may reflect indent error, not proven martensite. Full-size Charpy energies were **33–37 J in deposit versus 18–31 J at fusion line/HAZ**; one tensile specimen failed at **83.9 ksi and 6.7% elongation** from a lack-of-fusion defect **missed by ultrasonic inspection**. Trailing cryogenic cooling reduced measured wall/block distortion by **40%/31%** and build time **22%/15%**, but the modeled peak equivalent residual stresses were **795 versus 800 MPa**, a **simulation**, not measured stress reduction. **No seawater-corrosion result.** **[CITE] [NUMBERS] [NAVY] [GAP]** an unusually useful illustration that deposit-only tensile data and NDE-negative findings do not prove repair-interface integrity. (kuprienko2025analysisofnickel pages 61-67, kuprienko2025analysisofnickel pages 67-72, kuprienko2025analysisofnickel pages 72-76, kuprienko2025analysisofnickel pages 76-81, kuprienko2025analysisofnickel pages 81-87)

11. **Shahriari, A., Chalasani, D., Amirkhiz, B. S., and Mohammadi, M. “Corrosion performance of wire arc additively manufactured NAB alloy.” *npj Materials Degradation* 7 (2023), article DOI: 10.1038/s41529-023-00405-x.** **Process:** NAB **wire-arc DED** versus **cast NAB**; comparison of **as-built** and **350°C/2 h, 550°C/4 h, 675°C/6 h** treated deposits. **Test:** naturally aerated **3.5 wt% NaCl, 23 ± 2°C**, Ag/AgCl reference, **30-min OCP**, EIS **100 kHz–0.01 Hz/10 mV**, cyclic polarization **0.166 mV/s**; as-built/cast immersion **96 h**, heat-treated immersion **24 h**. As-built **E_corr approximately −0.293 V versus Ag/AgCl**, while cast and treated specimens averaged approximately **−0.222 V**: **less noble does not mean faster corrosion**. As-built had better pseudopassivity and the lowest reported current. For the heat-treated deposits, reported *i_corr* approximately **4.4, 6.6 and 8 µA/cm²** for 350/550/675°C, respectively, and charge-transfer resistance approximately **10.2, 2.58 and 3.8 kΩ·cm²**. κ particles serve as local cathodes against α-Cu; the needle-like κV generated by higher-temperature treatments can worsen corrosion. **No quantitative deposit–cast FZ/HAZ *macrogalvanic* current or C71500 reference.** **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]** as-built corrosion optimization already exists for arc NAB; **[GAP]** no repaired interface under long-term flowing seawater. (shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 14-14, shahriari2023corrosionperformanceof pages 1-2, shahriari2023corrosionperformanceof pages 2-2)

12. **Huo, R., Wang, Z., Wang, M., Wang, R., Zhang, S., Zhang, C., Wu, C., Chen, H., and Chen, J. “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing.” *Materials* 18 (2025): 2205. DOI: 10.3390/ma18102205.** **Process:** CMT **arc DED**, wire **Cu balance–8.73Al–5.9Fe–4.52Ni–1.39Mn** on copper-based substrate (**8.62Al–2.32Fe–0.005Ni–0.258Mn**); **not cast-NAB repair**. **As-deposited**, static aerated **3.5 wt% NaCl**, approximately **25 ± 5°C**, polarization/EIS; no long-term seawater service test. At **243.8 → 644.7 J/mm**, average grain size **38.26 → 74.62 µm**, measured surface microhardness **192.4 ± 6.9 → 166.9 ± 0.3 HV**, *i_corr* **2.56 ± 0.04 → 7.52 ± 0.07 µA/cm²**, fitted **R_ct 2485 → 707 Ω·cm²**, and fitted **R_f 1152 → 185.8 Ω·cm²**. The paper’s polarization table calls its potentials **“E”**, **−269.61 ± 40 → −700.94 ± 15 mV**, while its independently reported **one-hour OCPs** are approximately **−237 → −421 mV**; do **not** confuse these quantities or cite an unverified reference electrode. The paper also inconsistently gives other hardness values in its abstract; the values above are those in its results/conclusion. **[CITE] [NUMBERS] [NOVELTY-RISK]** low thermal input and κ/Al distribution already demonstrably change short-term corrosion; **[GAP]** not a C71500-matched long-duration test. (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 7-10, huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 13-15, huo2025modulatingheatinput pages 15-16)

## Dissimilar copper/steel deposition: the interface is the critical region

13. **Dharmendra, C., Shakerin, S., Ram, G. D. J., and Mohammadi, M. “Wire-arc additive manufacturing of nickel aluminum bronze/stainless steel hybrid parts—Interfacial characterization, prospects, and problems.” *Materialia* 13 (2020): 100834. DOI: 10.1016/j.mtla.2020.100834; and Dharmendra, C., Shakerin, S., and Mohammadi, M. “Metallurgical Assessment of Additive Manufactured Nickel Aluminum Bronze-316L Stainless Steel Bimetallic Structure: Effect of Deposit Geometry on the Interfacial Characteristics and Cracking.” *Journal of Materials Engineering and Performance* 30 (2021): 8746–8762; **DOI NR** in accessible evidence.** **Process:** ERCuNiAl **wire-arc DED** nominal **Cu–9Al–4Ni–4Fe–1Mn** onto **316L steel**. **Review-reported:** an apparently bonded Fe₃Al-containing mixed region nevertheless had occasional **intergranular cracks extending into the steel HAZ**, associated with *liquid Cu penetration into steel grain boundaries on the first track*; **114 A, 170 J/mm** are reported for the cracking case. Suggested mitigations were finer-grained steel, an Inconel 625 buffer or a preliminary laser-clad NAB layer. **Quantitative dilution, penetration-crack length, corrosion conditions and strength:** NR in available excerpts. Calling this a *steel-side liquid-metal penetration/liquation* problem is more precise than assuming the bronze itself suffered classic solidification cracking. **[CITE] [NAVY] [NUMBERS] [NOVELTY-RISK]** dissimilar NAB/steel processing is established; **[GAP]** marine-coupled edge performance is not demonstrated. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 113-114)

14. **Cai, X., Wang, Z., Dong, L., Yang, M., Zhou, J., and Xue, F. “Advanced mechanical properties of nickel-aluminum bronze/steel composite structure prepared by wire-arc additive manufacturing.” *Materials & Design* 221 (2022): 110969; DOI **NR** in the retrieved full-text evidence.** **Process:** **wire-arc DED** NAB/316L steel. The review reports an interface **without observed penetration cracks** at **60 A** and **48.9 J/cm**, versus the **114 A/170 J/mm** conditions above. **Important: the review prints *J/cm* for Cai but *J/mm* for Dharmendra; verify these original units before interpreting a 35-fold difference.** The mechanism suggested by the review—lower Cu liquid penetration at lower input—is plausible, not a controlled cross-study demonstration. **Corrosion/electrolyte, strength and interfacial porosity:** NR in accessible evidence. **[CITE] [NUMBERS] [NOVELTY-RISK] [GAP]** first-layer thermal control is likely critical but no universal crack-free threshold is established. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 112-113)

15. **Liu, Y., Li, B., Zhang, W., Liu, Z., and Jiang, M. “Interfacial Behavior of Copper/Steel Bimetallic Composites Fabricated by CMT-WAMM.” *Coatings* 14 (2024): 803. DOI: 10.3390/coatings14070803.** **Process:** CMT **wire-arc DED**, **silicon bronze**, **not Cu–Ni or NAB**: ERCuSi-A **Cu balance–3.50Si–1.30Mn–0.50Fe** on ER120S-G steel over Q235 steel. **Test:** *3.5 wt% NaCl, 35°C*, **30-min OCP**, polarization at **10 mV/min**. At **100 A and 500 mm/min** for bronze, bimetal UTS/yield were **404/352 MPa**, fracture on bronze side; interface **190 HV** versus bronze **~150 HV** and steel **~350 HV**. Individually tested steel and bronze gave respectively **7.304 and 2.035 µA/cm²**, *E_corr* **−0.564 and −0.325 V**; the exposed mixed-interface specimen gave **7.992 µA/cm² and −0.611 V**. Thus a sound, strong interface was **more corrosion-active than either exposed constituent** under those conditions. **These are separate polarization specimens, not a measured zero-resistance-ammeter galvanic current; reference-electrode identity and longer-term rates NR.** **[CITE] [NUMBERS] [NAVY]** explicit marine-filter motivation; **[GAP]** shows why a favorable clad-only *i_corr* cannot qualify a bimetallic edge. (liu2024interfacialbehaviorof pages 2-4, liu2024interfacialbehaviorof pages 4-6, liu2024interfacialbehaviorof pages 11-13)

16. **Li, B., Han, C., Lim, C. W. J., and Zhou, K. “Interface formation and deformation behaviors of an additively manufactured nickel-aluminum-bronze/15-5 PH multimaterial via laser-powder directed energy deposition.” *Materials Science and Engineering A* 829 (2022): 142101. DOI: 10.1016/j.msea.2021.142101.** **Process:** **laser-powder DED** dissimilar **NAB/15-5 PH steel**; original report not available for verification of deposition order, specific chemistry, cracking, dilution or mechanical values. **[CITE] [NOVELTY-RISK]** laser-powder NAB/steel bimetal itself is published; **[GAP]** corrosion of exposed interfaces in seawater is unestablished by the evidence retrieved. (nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 113-114)

## What a Navy reviewer should expect

**Make the acceptance article a *repaired joint*, not merely an attractive standalone coupon.** For *each* single pre-alloyed powder and both repair substrates, report powder composition and its **post-atomization versus deposited composition**, particle-size distribution, morphology/satellites, ASTM-method Hall flow, apparent/tap density and lot oxygen; publish the **actual values**, not nominal powder specifications. Compare the *first bead*, overlapping first layer and multilayer build: optical/SEM cross sections and µCT or calibrated density/porosity measurement; fusion penetration and EDS/EPMA traverses of **Fe, Ni, Al, Mn and Cr** to measure dilution; serial sections through track starts/stops and bead intersections; and metallography for lack of fusion, solidification-centerline cracks and substrate-side grain-boundary penetration. The elemental-blend Cu–Ni/316L study shows why crack-free height, measurable penetration and little Fe pickup must be balanced rather than independently maximized. (chen2020areviewon pages 13-15, chen2020areviewon pages 10-13, williams2025thefirstlayer pages 6-9, williams2025thefirstlayer pages 4-6)

**Explicitly qualify the cast-NAB HAZ.** Map fine-step HV across deposit → fusion boundary → substrate HAZ → unaffected casting; determine transformed-HAZ width, κII/κIII/κIV dissolution or coarsening, retained β/β′/γ₂ with EBSD/XRD and targeted TEM, and identify the *peak-temperature/cooling-history* responsible. Measure residual stress by a defensible method such as XRD or hole drilling and record distortion; **do not present an FEA Von Mises maximum as an experimentally verified residual stress**. Use registered cross-interface tensile, bend and Charpy/fracture specimens alongside deposit-only longitudinal/transverse properties; include fatigue or corrosion-fatigue if a propeller, shaft or cyclically loaded component is the use case. The available arc experiment found weaker fusion-line/HAZ impact energies and an ultrasonic-test-missed lack-of-fusion defect. (kuprienko2025analysisofnickel pages 45-50, kuprienko2025analysisofnickel pages 67-72, kuprienko2025analysisofnickel pages 76-81, kuprienko2025analysisofnickel pages 81-87)

**Separate corrosion screening from service evidence.** In the **as-deposited** condition, machine and mask replicates to expose separately **bulk deposit, first-layer dilution zone, cast-NAB or wrought-C71500 HAZ, intact repair cross section and exposed bimetal edge**, plus *same-batch wrought C71500*; report solution, temperature, aeration, reference electrode, surface finish and exposed area. Screen using stable OCP, EIS and polarization in **3.5% NaCl**, but verify ranking with at least **30-day natural seawater or explicitly ASTM D1141 substitute seawater**, specifying static versus controlled flow, renewal, dissolved oxygen, temperature, pH and sulfide/biofouling exposure as applicable. Add electrically coupled deposit/substrate **zero-resistance-ammeter current at realistic exposed-area ratios**, crevice/edge configurations and local scanning electrochemical or post-test cross-sectional profiling. Report mass-loss corrosion rate **and maximum pit/selective-attack/HAZ penetration depth** rather than inferring 30-day depth from short scans. For steel-backed parts, expose an intentional edge flaw and check the *steel-side* preferential attack, not only intact bronze coverage. These are **recommended qualification tests**, not established results for the proposed powder. (shahriari2023corrosionperformanceof pages 14-14, liu2024interfacialbehaviorof pages 11-13, lv2015investigationofthe pages 2-5, lewis1981evaluationofcoppernickel pages 1-7, phull20172.18–marine pages 19-20)

**Standards/precedents should be matched to the claim, not listed as a substitute for data:** ASTM D1141 defines substitute seawater; ASTM E8/E92/E23 and AWS B4.0 exemplify mechanical/hardness/impact/bend testing in the cited repairs; NAVSEA-style **visual, penetrant, volumetric radiography/ultrasonics, interface-spanning mechanical specimens** were actually used for a NAB arc build. Specify the edition and applicable naval component acceptance authority in the proposal rather than claiming that these publications themselves constitute Navy certification. The DoE OTEC review by **Lewis, R. O., and LaQue, F. L., *Evaluation of Copper-Nickel Alloys for OTEC Applications* (Argonne, 1981), DOI: 10.2172/6255887** documents flowing-seawater and galvanic-service considerations for C71500/C70600; it is a service comparator **not** a DED test or Navy-funded study. (kim2020comparisonofmechanical pages 3-6, kuprienko2025analysisofnickel pages 67-72, lewis1981evaluationofcoppernickel pages 1-7)

## Top 5 things the PI should know

1. **Lead with the precise unmet intersection:** a *single pre-alloyed powder stream*, **both** cast-NAB and wrought-C71500 repairs, and **as-deposited** corrosion parity to an actually tested wrought-C71500 control. Existing laser NAB, Cu–Ni and NAB-on-NAB repair studies make broader “first-ever” claims untenable. (cheng2022anoverviewof pages 33-34, nemani2024advancementsinadditive pages 113-114, nemani2024advancementsinadditive pages 79-83)
2. **The vulnerable product is often the first-layer FZ/HAZ, not the top of the wall:** Cu/steel can crack by liquid penetration or by solidification, while cast NAB can acquire a hardened, phase-transformed HAZ. Explicitly control and characterize first-track heat input and dilution. (kuprienko2025analysisofnickel pages 45-50, kuprienko2025analysisofnickel pages 76-81, nemani2024advancementsinadditive pages 79-83, williams2025thefirstlayer pages 6-9)
3. **Electrochemical ranking is not repair qualification:** as-built arc NAB can outperform its heat-treated counterpart in NaCl, while a copper/steel mixed interface can corrode faster than *either* constituent. Measure coupled-interface current and depth-resolved attack over time. (shahriari2023corrosionperformanceof pages 12-14, liu2024interfacialbehaviorof pages 11-13)
4. **Avoid Ni-content and physics-model shortcuts:** elemental-blend studies already optimize Cu–Ni tracks but show Ni inclusions, oxygen-sensitive pores and composition deviations; measured *powder-to-deposit chemistry*, time-resolved phase evidence and independent held-out repairs are appropriate tests of the proposed pre-alloying/thermal-history ICME advantage. (chen2020areviewon pages 13-15, chen2020areviewon pages 10-13, williams2025thefirstlayer pages 6-9)
5. **Demonstrate Navy-relevant failure detection and mechanical margins:** deposit-only strength, optical “soundness,” and a negative ultrasonic scan each miss potential fusion-line damage; pair NDE with sectioning, cross-interface tensile/bend/low-temperature impact, HAZ hardness and appropriately chosen fatigue/cavitation tests. (kim2020comparisonofmechanical pages 3-6, kuprienko2025analysisofnickel pages 67-72, kuprienko2025analysisofnickel pages 76-81)

References

1. (nemani2024advancementsinadditive pages 102-105): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

2. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

3. (shahriari2023corrosionperformanceof pages 14-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

4. (kuprienko2025analysisofnickel pages 50-55): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

5. (kim2020comparisonofmechanical pages 3-6): Ji-sun Kim, Jaewoong Kim, and Changmin Pyo. Comparison of mechanical properties of ni-al-bronze alloy fabricated through wire arc additive manufacturing with ni-al-bronze alloy fabricated through casting. Metals, 10:1164, Aug 2020. URL: https://doi.org/10.3390/met10091164, doi:10.3390/met10091164. This article has 52 citations.

6. (kim2020comparisonofmechanical pages 6-8): Ji-sun Kim, Jaewoong Kim, and Changmin Pyo. Comparison of mechanical properties of ni-al-bronze alloy fabricated through wire arc additive manufacturing with ni-al-bronze alloy fabricated through casting. Metals, 10:1164, Aug 2020. URL: https://doi.org/10.3390/met10091164, doi:10.3390/met10091164. This article has 52 citations.

7. (kim2020comparisonofmechanical pages 8-12): Ji-sun Kim, Jaewoong Kim, and Changmin Pyo. Comparison of mechanical properties of ni-al-bronze alloy fabricated through wire arc additive manufacturing with ni-al-bronze alloy fabricated through casting. Metals, 10:1164, Aug 2020. URL: https://doi.org/10.3390/met10091164, doi:10.3390/met10091164. This article has 52 citations.

8. (nemani2024advancementsinadditive pages 113-114): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

9. (williams2025thefirstlayer pages 2-4): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

10. (williams2025thefirstlayer pages 6-9): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

11. (williams2025thefirstlayer pages 9-11): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

12. (williams2025thefirstlayer pages 4-6): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

13. (cheng2022anoverviewof pages 33-34): Jian Cheng, Yun-Hao Xing, En-Jie Dong, Lin-Jie Zhao, He-Nan Liu, Ting-Cheng Chang, Mingjun Chen, Jing-He Wang, Jun-Wen Lu, and J. Wan. An overview of laser metal deposition for cladding: defect formation mechanisms, defect suppression methods and performance improvements of laser-cladded layers. Materials, 15:5522, Aug 2022. URL: https://doi.org/10.3390/ma15165522, doi:10.3390/ma15165522. This article has 124 citations.

14. (nemani2024advancementsinadditive pages 110-112): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

15. (chen2020areviewon pages 13-15): Yitao Chen, Xinchang Zhang, Mohammad Masud Parvez, and Frank Liou. A review on metallic alloys fabrication using elemental powder blends by laser powder directed energy deposition process. Materials, 13:3562, Aug 2020. URL: https://doi.org/10.3390/ma13163562, doi:10.3390/ma13163562. This article has 79 citations.

16. (chen2020areviewon pages 10-13): Yitao Chen, Xinchang Zhang, Mohammad Masud Parvez, and Frank Liou. A review on metallic alloys fabrication using elemental powder blends by laser powder directed energy deposition process. Materials, 13:3562, Aug 2020. URL: https://doi.org/10.3390/ma13163562, doi:10.3390/ma13163562. This article has 79 citations.

17. (kuprienko2025analysisofnickel pages 41-45): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

18. (kuprienko2025analysisofnickel pages 45-50): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

19. (kuprienko2025analysisofnickel pages 55-61): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

20. (kuprienko2025analysisofnickel pages 61-67): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

21. (kuprienko2025analysisofnickel pages 67-72): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

22. (kuprienko2025analysisofnickel pages 72-76): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

23. (kuprienko2025analysisofnickel pages 76-81): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

24. (kuprienko2025analysisofnickel pages 81-87): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

25. (shahriari2023corrosionperformanceof pages 12-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

26. (shahriari2023corrosionperformanceof pages 1-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

27. (shahriari2023corrosionperformanceof pages 2-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

28. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

29. (huo2025modulatingheatinput pages 7-10): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

30. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

31. (huo2025modulatingheatinput pages 13-15): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

32. (huo2025modulatingheatinput pages 15-16): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

33. (nemani2024advancementsinadditive pages 112-113): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

34. (liu2024interfacialbehaviorof pages 2-4): Yan Liu, Bo Li, Wenguang Zhang, Zhaozhen Liu, and Maofa Jiang. Interfacial behavior of copper/steel bimetallic composites fabricated by cmt-wamm. Coatings, 14:803, Jun 2024. URL: https://doi.org/10.3390/coatings14070803, doi:10.3390/coatings14070803. This article has 22 citations.

35. (liu2024interfacialbehaviorof pages 4-6): Yan Liu, Bo Li, Wenguang Zhang, Zhaozhen Liu, and Maofa Jiang. Interfacial behavior of copper/steel bimetallic composites fabricated by cmt-wamm. Coatings, 14:803, Jun 2024. URL: https://doi.org/10.3390/coatings14070803, doi:10.3390/coatings14070803. This article has 22 citations.

36. (liu2024interfacialbehaviorof pages 11-13): Yan Liu, Bo Li, Wenguang Zhang, Zhaozhen Liu, and Maofa Jiang. Interfacial behavior of copper/steel bimetallic composites fabricated by cmt-wamm. Coatings, 14:803, Jun 2024. URL: https://doi.org/10.3390/coatings14070803, doi:10.3390/coatings14070803. This article has 22 citations.

37. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

38. (lv2015investigationofthe pages 2-5): Yuting Lv, Liqiang Wang, Xiaoyan Xu, Yuanfei Han, and Weijie Lu. Investigation of the microstructure and corrosion properties of friction stir processed cast nial bronze. Materials Transactions, 56:1523-1529, Sep 2015. URL: https://doi.org/10.2320/matertrans.m2015125, doi:10.2320/matertrans.m2015125. This article has 17 citations and is from a peer-reviewed journal.

39. (lewis1981evaluationofcoppernickel pages 1-7): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

40. (phull20172.18–marine pages 19-20): B Phull and AA Abdullahi. 2.18 – marine corrosion. ArXiv, 2:1107-1148, Jan 2017. URL: https://doi.org/10.1016/b978-044452787-5.00046-9, doi:10.1016/b978-044452787-5.00046-9. This article has 61 citations.
