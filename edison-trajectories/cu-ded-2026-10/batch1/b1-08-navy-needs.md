<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: 547ec63c-d418-4e5b-a51e-19a259f65ed1
- Submitted: 2026-10-17T05:10:47Z
- Fetched: 2026-10-17T05:42:09Z (status: success)
- Raw trajectory JSON: ../raw/b1-08-navy-needs.json.gz
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

QUESTION: What does the published literature (including technical reports and
conference papers) say about Navy needs for additively manufactured Cu-Ni and
NAB parts, and about Navy-funded work on them? Cover seawater piping, valves,
pump impellers, propellers and propulsor parts, heat exchangers, and repair
of cast NAB (propellers) by laser cladding or DED; NAVSEA qualification and
AM material specifications; work from NSWC Carderock, NSWC Philadelphia, NRL,
Penn State ARL, Naval Postgraduate School, and ONR-funded university groups;
and casting supply-chain delays. Give exact citations and say which claims
come from peer-reviewed sources and which from trade press.

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

QUESTION: What does the published literature (including technical reports and
conference papers) say about Navy needs for additively manufactured Cu-Ni and
NAB parts, and about Navy-funded work on them? Cover seawater piping, valves,
pump impellers, propellers and propulsor parts, heat exchangers, and repair
of cast NAB (propellers) by laser cladding or DED; NAVSEA qualification and
AM material specifications; work from NSWC Carderock, NSWC Philadelphia, NRL,
Penn State ARL, Naval Postgraduate School, and ONR-funded university groups;
and casting supply-chain delays. Give exact citations and say which claims
come from peer-reviewed sources and which from trade press.

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


# Navy-relevant Cu–Ni and nickel–aluminum bronze additive manufacturing: evidence assessment

**Scope and evidence standard.** The clearest directly documented Navy connections found are a Naval Postgraduate School (NPS) C71500 study and a Navy-grant-supported Oregon State University NAB study. Naval applications cited in journal articles are not, by themselves, evidence of Navy funding or component qualification. Composition figures below are **wt%**; “not reported” means the examined source does not establish the requested value. No Sterling G. Baird publication is included. (sparrow2025lpbfparameteroptimization pages 1-3, doyle2022additivemanufacturingof pages 53-58, guerra2023microstructureandmechanical pages 1-2)

## Application need, specifications, and casting supply chain

1. **Guerra, C.; Ramos-Grez, J. A.; La Fé-Perdomo, I.; Castillo, A.; Walczak, M. “Microstructure and Mechanical Properties of Cu-11Al-5Ni-4Fe wt% Manufactured by LPBF.” *Metals* 13 (2023), 459. DOI: 10.3390/met13030459.** **Peer-reviewed; application statement and experiment.** Process: laser powder-bed fusion (**LPBF**), not blown-powder DED. Composition: Cu–11Al–5Ni–4Fe. The authors identify **seawater piping and valves**, sealing flanges, sonar equipment, flexible couplings, and periscope assemblies as naval NAB applications; the paper does not document installation or Navy funding for its own specimens. Nitrogen-atomized powder was <40 µm, with median <17 µm and 90th percentile <30 µm; specimens attained approximately **97.5% relative density** and up to **1,300 MPa compressive strength at 20% strain**. No seawater experiment, corrosion current, flow test, or powder Hall-flow/oxygen measurement is reported in the examined passages. **[CITE] [NUMBERS] [NAVY: application] [GAP: no service corrosion]** (guerra2023microstructureandmechanical pages 1-2, guerra2023microstructureandmechanical pages 2-4)

2. **Tan, Y.; Xie, H.; Feng, X.; Huang, S.; Zhang, W.; Peng, L.; Wang, W.; Zhao, Y. “Effect of Al/Ni Ratio on the Microstructure and Properties of Nickel–Aluminum Bronze Alloys.” *Materials* 17 (2024), 1330. DOI: 10.3390/ma17061330.** **Peer-reviewed, non-Navy comparator.** Process: vacuum-melted/**cast**, not AM. Four compositions, expressed as Al–Ni–Fe–Mn with Cu balance, were **7–7–4–2, 8–6–4–2, 9–5–4–2, and 10–4–4–2**. The article identifies ship valves, pumps, and propellers as NAB applications. In **static 3.5 wt% NaCl**, the 7Al–7Ni alloy gave **0.00267 mm/year** after 30 days; after 30 days its polarization fit gave **E_corr −281.48 mV, i_corr 0.35 µA/cm², and R_p 173.48 kΩ·cm²**. Across the four compositions, hardness rose **104→202 HV** and tensile strength **356→751 MPa**, while elongation fell **50.5→11.0%** as Al/Ni rose. These are controlled **cast-NAB trade-offs**, not evidence that a deposited, lower-Ni NAB will perform similarly or that either alloy meets C71500 corrosion performance. No flowing seawater test is established. **[CITE] [NUMBERS] [GAP: AM and flow]** (tan2024effectofalni pages 1-2, tan2024effectofalni pages 6-10, tan2024effectofalni pages 10-12)

3. **Doyle, R. P. *Additive Manufacturing of FeCrCoCuNi High Entropy Alloy via Laser Powder Bed Fusion and Nickel Aluminum Bronze via Laser Directed Energy Deposition*. MS thesis, Oregon State University, 2022; NAB chapter: “Effect of Wire-Fed Laser Directed Energy Deposition Parameters and Heat Treatment on the Microstructure and Mechanical Properties of NAB C95800.” DOI: not verified.** **University thesis, not peer-reviewed journal article; its NAB chapter explicitly acknowledges a Navy grant.** Process: **wire-laser DED**, *not powder-fed DED*; wire composition **Cu 82.0, Al 8.64, Ni 4.21, Fe 3.19, Mn 1.32, Si 0.05, Zn 0.003, Pb 0.004**. Four selected deposits achieved **99.58–99.89% relative density**. As-deposited material gave **YS 410.5 ± 6.3 MPa, UTS 757.8 ± 5.4 MPa, elongation 29.0 ± 1.0%, hardness 218.8 ± 4.4 HV**; after **675 °C/6 h**, the corresponding values were **372.2 ± 6.7 MPa, 714.5 ± 8.3 MPa, 31.2 ± 0.25%, and 204.1 ± 3.1 HV**. The thesis attributes to NAVSEA **cast-C95800 coupon minima** of roughly **241 MPa YS, 586 MPa UTS, and 15% elongation**, and cites ASTM B505 for the casting anneal. **Passing cited casting tensile minima does not constitute NAVSEA qualification of an AM material or repair.** No corrosion experiment is supplied; the author expressly recommends extensive corrosion testing. **[CITE] [NUMBERS] [NAVY: acknowledged grant and cited casting requirements] [NOVELTY-RISK: as-deposited laser-built NAB already demonstrated] [GAP: powder, substrate repair, seawater]** (doyle2022additivemanufacturingof pages 1-9, doyle2022additivemanufacturingof pages 43-47, doyle2022additivemanufacturingof pages 47-53, doyle2022additivemanufacturingof pages 53-58)

4. **Shuvo, M. M.; King, P.; Voigt, R.; Manogharan, G. “Toward Reducing Casting Defects via 3D Risers via 3D Sand-Printing: A Simulation Study.” *International Journal of Metalcasting* 19 (2025). DOI: 10.1007/s40962-024-01353-1.** **Peer-reviewed simulation, Penn State authors; not evidence of Navy funding or metal DED.** Process: **sand-mold printing followed by conventional casting**; one simulated alloy is **C95800 NAB**, but its elemental assay is not supplied in the examined text. Spherical-riser designs were predicted to improve casting yield by as much as **45%** across the modeled alloys; the authors explicitly say experimental validation remains necessary. They discuss the potential for shorter **small-batch mold-making** lead times, but supply **no measured Navy casting procurement delay**. This is an important competing supply-chain remedy: not every delayed casting requires direct metal AM. No seawater data. **[CITE] [NUMBERS: simulated, not measured] [GAP: Navy procurement lead time]** (shuvo2025towardreducingcasting pages 1-2, shuvo2025towardreducingcasting pages 10-12)

**Qualification finding.** The inspected material supports identification of casting requirements and ASTM comparators, **not** an exact NAVSEA-approved Cu–Ni or NAB AM material specification, qualified powder chemistry, acceptance limits for DED porosity, or approval procedure for propeller repair. Such a specification should not be claimed as existing or absent on this search alone. Likewise, no defensible numerical Navy casting lead time was recovered. (doyle2022additivemanufacturingof pages 53-58, shuvo2025towardreducingcasting pages 1-2)

## Direct experimental precedents and corrosion benchmarks

5. **Sparrow, A.; Smith, W.; Ansell, T. Y. “LPBF Parameter Optimization of Mechanical, Non-Thermal Generated C71500 Powder.” *Metals* 16 (2026), 10; published 21 December 2025. DOI: 10.3390/met16010010.** **Peer-reviewed; all authors list NPS. Navy affiliation is documented; a specific funding award is not established here.** Process: **LPBF**, using mechanically cut C71500 bar-stock powder, **not ultrasonic atomization or blown-powder DED**. C71500 identifies nominal **Cu–30Ni**; the examined paper passages do not establish a measured Fe/Mn impurity assay. Powder: **D10 24, D50 44, D90 77 µm; apparent density 3.12 g/cm³; tapped density 4.26 g/cm³**; GranuDrum cohesion indices **15 at 2 and 10 rpm, 18 at 20 rpm**, which are **not Hall-flow seconds**. Optimized prints were **>99.8% relatively dense**, **165–175 HV0.2**, and approximately **15 µm R_a**. Eight tested bars averaged **UTS 384.7 MPa, YS 317.2 MPa, elongation 31.1%**; horizontal UTS values **404.0–423.3 MPa** versus vertical **350.9–355.7 MPa** expose anisotropy. The authors state their EDS indicated roughly **5 wt% oxygen** in examined powder sets but expressly caution that this does **not** quantify oxygen uptake and recommend inert-gas-fusion analysis: it must **not** be presented as a validated lot oxygen specification. **No seawater corrosion tests.** Their Gaussian-process-assisted optimization of LPBF *settings* is a narrower methodological overlap than a multi-stage, cost-aware composition-to-corrosion network. **[CITE] [NUMBERS] [NAVY: NPS] [NOVELTY-RISK: Cu–30Ni powder/process optimization and ML] [GAP: composition design, validated powder oxygen, DED, corrosion]** (sparrow2025lpbfparameteroptimization pages 3-6, sparrow2025lpbfparameteroptimization pages 11-12, sparrow2025lpbfparameteroptimization pages 1-3, sparrow2025lpbfparameteroptimization pages 8-11, sparrow2025lpbfparameteroptimization media e92f46e3)

6. **Shahriari, A.; Chalasani, D.; Amirkhiz, B. S.; Mohammadi, M. “Corrosion performance of wire arc additively manufactured NAB alloy.” *npj Materials Degradation* 7 (2023). DOI: 10.1038/s41529-023-00405-x.** **Peer-reviewed; Navy funding is not established by the inspected evidence.** Process: **WAAM/GMAW**, comparing as-built NAB with **cast** NAB and heat-treated WAAM; filler is **AWS A5.7 ERCuNiAl/C95800-type**, but an exact measured wt% assay is not established in the available extracts. Tests used **naturally aerated 3.5 wt% NaCl**, approximately **23 ± 2 °C**, a saturated Ag/AgCl reference, and **static** exposures of **96 h for as-built and cast versus 24 h for heat-treated samples**—a consequential limitation for direct comparisons. EIS covered **100 kHz–0.01 Hz** at 10 mV after a **1,800 s** OCP stabilization. As-built WAAM had the **lowest corrosion current** qualitatively; its reported E_corr was approximately **−0.293 V versus Ag/AgCl**, versus approximately **−0.222 V** as an average for cast/heat-treated conditions. For WAAM after **350 °C/2 h**, **i_corr ~4.4 µA/cm² and R_t ~10.2 kΩ·cm²**; after **550 °C/4 h**, **~6.6 µA/cm² and ~2.58 kΩ·cm²**; after **675 °C/6 h**, **~8 µA/cm² and ~3.8 kΩ·cm²**. The reported maximum local surface depression for the first heat treatment is approximately **3 µm**, **not** an established long-term selective-attack penetration rate. As-built superiority is attributed to fewer/finer cathodic κ phases. The inspected extracts do not substantiate exact as-built or cast i_corr/R_t values. **[CITE] [NUMBERS] [NOVELTY-RISK: as-built NAB corrosion and processing–phase correlations] [GAP: matched-duration C71500 benchmark, natural/flowing seawater, powder-laser DED]** (shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 14-14, shahriari2023corrosionperformanceof pages 2-2, shahriari2023corrosionperformanceof pages 10-10)

7. **Murray, T.; Thomas, S.; Wu, Y.; Neil, W.; Hutchinson, C. “Selective laser melting of nickel aluminium bronze.” *Additive Manufacturing* 33 (2020), 101122. DOI: not independently verified in the retrieved text.** **Peer-reviewed study identified through a peer-reviewed review; numerical comparison below is secondary-source reporting.** Process: **LPBF**; reported powder **Cu–9.8Al–5.2Ni–4.6Fe–0.3Mn**. A review of the study states that **as-built** nearly uniform martensitic material suffered approximately **one order of magnitude less mass loss** than cast and wrought NAB after **3 and 6 months of seawater exposure**, although the as-built condition was brittle. The inspected account does **not** establish whether this was natural seawater or ASTM D1141 substitute, flow rate, absolute mass losses, i_corr, or selective-attack depths. Thus, “as-deposited NAB corrosion can be better than casting” is **already in the literature**, but “it meets wrought C71500 in flowing seawater” does not follow. **[CITE] [NUMBERS: relative comparison only] [NOVELTY-RISK: as-built NAB seawater comparison] [GAP: specified medium/flow and C71500 comparator]** (nemani2024advancementsinadditive pages 71-74, nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 113-114)

8. **Barr, C.; Pateras, A.; Molotnikov, A.; Clarke, D.; Brandt, M. “Effect of composition on the tensile and corrosion performance of nickel aluminium bronze produced via laser powder bed fusion.” *Additive Manufacturing* 54 (2022), 102771. DOI: not independently verified in the retrieved text.** **Peer-reviewed study identified through a peer-reviewed review; findings below are secondary-source reporting.** Process: **LPBF** using **C63000: Cu–10.2Al–4.8Fe–5.0Ni–0.2Si**, versus **C95800: Cu–9.0Al–4.0Fe–4.6Ni–1.9Mn**. Reported as-built C63000 reached approximately **1,120 MPa tensile strength but only 3% elongation**; chemistry changed α/β′ morphology and corrosion behavior. Heat-treated coupons reportedly had corrosion behavior similar to wrought NAB. The examined review does not establish electrolyte, duration, reference electrode, or numerical i_corr for these experiments. **This is a substantial composition–microstructure–corrosion novelty precedent**, even though it uses LPBF and standard rather than newly atomized single-stream DED powders. **[CITE] [NUMBERS] [NOVELTY-RISK: NAB composition-dependent corrosion] [GAP: DED repair and documented as-deposited C71500 parity]** (nemani2024advancementsinadditive pages 60-62, nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 112-113)

9. **Li, B.; Zheng, H.; Han, C.; Zhou, K. “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition.” *Additive Manufacturing* 39 (2021), 101825. DOI: not independently verified in the retrieved text.** **Peer-reviewed study, numerical results obtained from a peer-reviewed review.** Process: **laser metal deposition/laser DED** of **Cu–9Al–5Fe–5Ni**. Reported as-built **YS 593–713 MPa, UTS 769–949 MPa, elongation 10–12%**, with nanoscale twins and approximately **250 nm martensite plates**. The reviewed evidence does not establish feedstock preparation, whether a single pre-alloyed powder feed was used, or seawater test conditions/values; those distinctions **must not be assumed**. **[CITE] [NUMBERS] [NOVELTY-RISK: laser DED of NAB already exists] [GAP: verified single-stream feedstock, corrosion and cast-NAB repair]** (nemani2024advancementsinadditive pages 113-114, nemani2024advancementsinadditive pages 79-83)

10. **Yao, C.-L.; Kang, H.-S.; Lee, K.-Y.; Zhai, J.-G.; Shim, D.-S. “A study on mechanical properties of CuNi2SiCr layered on nickel–aluminum bronze via directed energy deposition.” *Journal of Materials Research and Technology* 18 (2022), 5337–5361. DOI: 10.1016/j.jmrt.2022.04.159.** **Peer-reviewed; characterization reported here through a peer-reviewed review.** Process: **powder laser DED** of nominal **CuNi2SiCr** on **cast AlBC3 NAB**, explicitly exploring marine-propeller repair. The alloy shorthand suggests approximately 2% Ni but the inspected source does not verify an exact powder or deposit elemental assay. The review reports **porous, predominantly α-phase deposit lacking NAB’s strengthening phases** and concludes that this material was **not suitable as the proposed propeller repair** owing to inferior hardness/strength/wear resistance; exact porosity and mechanical numbers were not recovered. This is **direct repair overlap**, not an unexplored use case. **[CITE] [NAVY: marine application, not established US Navy funding] [NOVELTY-RISK: copper-alloy powder DED on cast NAB] [GAP: a demonstrably sound, corrosion-resistant alternative]** (nemani2024advancementsinadditive pages 113-114, nemani2024advancementsinadditive pages 79-83)

11. **Yao, C.-L.; Shim, D.-S. “Corrosive properties of CuNi2SiCr fabricated through directed energy deposition on a nickel-aluminum bronze substrate.” *Journal of Alloys and Compounds* 918 (2022), 165776. DOI: 10.1016/j.jallcom.2022.165776.** **Peer-reviewed, direct competing corrosion-and-repair study**, identified in the retrieved review bibliography. Process: **laser DED**, nominal **CuNi2SiCr on cast NAB**; exact wt% assay, solution, exposure, E_corr, i_corr, impedance, and attack-depth results **could not be verified** because its primary full text was not obtained. Do not describe its outcome by copying the *mechanical* paper’s conclusion without reading this separate corrosion paper. **[CITE] [NOVELTY-RISK: corrosion of a powder-DED/cast-NAB interface has specifically been studied] [GAP: numerical comparison unavailable here]** (nemani2024advancementsinadditive pages 113-114)

12. **Queguineur, A.; Marolleau, J.; Lavergne, A.; Rückert, G. “Evaluation of tandem controlled short-circuit GMAW for improved deposition in additive manufacture of large Nickel Aluminium Bronze naval components.” *Welding in the World* 64 (2020), 1389–1395. DOI: 10.1007/s40194-020-00925-z.** **Peer-reviewed; explicitly naval *application*, with Navy funding not established here.** Process: **tandem wire-arc DED/WAAM**, alloys identified as **CuAl8Ni2Fe2Mn2** and **CuAl9Ni5** variants in the review (remaining chemistry not verified). Twin-wire deposition widened the bead and increased deposition rate but accumulated heat, imposing longer interlayer cooling; the authors favored sufficiently large parts. No measured seawater corrosion, flow, density, or complete composition is established in the inspected summary. This demonstrates an established route for **large naval NAB components**, not a precedent for single-feed blown powder. **[CITE] [NAVY: explicit component application] [NOVELTY-RISK: large-format NAB AM] [GAP: as-built service corrosion]** (nemani2024advancementsinadditive pages 68-71, nemani2024advancementsinadditive pages 60-62, nemani2024advancementsinadditive pages 112-113)

13. **Camilleri, S.; Tran, T.; Duguid, A.; Krishnan, K. N. “Cold spray as a powder metallurgy process for production of nickel aluminium bronze.” *PLOS ONE* 20 (2025), e0319333. DOI: 10.1371/journal.pone.0319333.** **Peer-reviewed; acknowledges *technical support* from Penn State ARL, but explicitly declares Australian Department of Education funding and no additional external funding. Do not label it Navy-funded.** Process: **cold spray of blended elemental/Al6061 powders plus extensive subsequent thermal processing**, not laser DED or as-deposited pre-alloyed feed. Initial blend: **11% Al6061, 5.8% Ni powder, 6.8% Fe powder, remainder Cu powder**—these are **feed-mixture fractions, not a verified final NAB elemental assay**. The authors report approximately **98% density**; after sintering, HIP, and aging, **YS 289 ± 1.6 MPa, UTS 512 ± 2.7 MPa, elongation 22 ± 0.3%, hardness 160 ± 1.8 HB**. No quantitative marine-corrosion experiment is documented. **[CITE] [NUMBERS] [NAVY: ARL acknowledged only] [GAP: no as-deposited laser-DED performance]** (camilleri2025coldsprayas pages 1-2, camilleri2025coldsprayas pages 10-12)

14. **Nemani, A. V.; Ghaffari, M.; Bokati, K. S.; Valizade, N.; Afshari, E.; Nasiri, A. “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review.” *Journal of Manufacturing and Materials Processing* 8 (2024), 54. DOI: 10.3390/jmmp8020054.** **Peer-reviewed *review*, not independent Navy experiment.** It explicitly calls for more **AM Cu–Ni in-service/corrosion studies** and **as-printed versus heat-treated NAB seawater comparisons with conventionally manufactured material**. It documents earlier **Karnati, S.; Liou, F. F.; Newkirk, J. W. “Characterization of copper–nickel alloys fabricated using laser metal deposition and blended powder feedstocks,” *International Journal of Advanced Manufacturing Technology* 103 (2019), 239–250**, and **Karnati, S.; Zhang, Y.; Liou, F. F.; Newkirk, J. W. “On the feasibility of tailoring copper–nickel functionally graded materials fabricated through laser metal deposition,” *Metals* 9 (2019), 287**; their DOI, detailed compositions, and corrosion values were not verified. Crucially, these are **blended-feedstock or graded** precedents, not proof of a demonstrated **single-stream pre-alloyed-powder** workflow. A report of WAAM Cu–Ni polarization/EIS in the review lacks a wrought control and therefore cannot establish C71500 parity. **[CITE] [NOVELTY-RISK: laser Cu–Ni deposition and composition tailoring are not new] [GAP: controlled single-feed powder and validated seawater performance]** (nemani2024advancementsinadditive pages 102-105, nemani2024advancementsinadditive pages 105-106, nemani2024advancementsinadditive pages 41-43, nemani2024advancementsinadditive pages 110-112)

## What the retrieved evidence does **not** substantiate

**Propellers and propulsors:** NAB propellers and cast-NAB repair are directly motivated and studied, but the inspected sources do **not** document a qualified US Navy blown-powder DED propeller repair, a specific Navy propulsor-part production record, or acceptable cavitation/fatigue life for the proposed deposits. The Ohio State University **Heniken, N. H., *Influence of Microstructure on Fatigue Behavior, Crack Initiation, and Crack Growth in Wire-Arc Additively Manufactured Nickel Aluminum-Bronze*, MS thesis (2025; DOI not verified)** reports a **~9 MPa√m fatigue-crack-growth threshold** for WAAM NAB, but its examined text does not establish Navy funding or corrosion–fatigue service performance. (heniken2025influenceofmicrostructure pages 1-8, guerra2023microstructureandmechanical pages 1-2, nemani2024advancementsinadditive pages 79-83)

**Pumps and heat exchangers:** Peer-reviewed application descriptions support NAB pumps and valves, and ship internal seawater systems serve cooling and heat-exchange functions. **Davidson, I.; Cahill, P.; Hinz, A.; Kluza, D.; Scianni, C.; Georgiades, E. “A Review of Biofouling of Ships’ Internal Seawater Systems.” *Frontiers in Marine Science* 8 (2021). DOI: 10.3389/fmars.2021.761531** describes impaired flow, corrosion, and cooling performance, **not an AM Cu–Ni heat-exchanger qualification**. No verified Navy Cu–Ni/NAB printed pump-impeller or heat-exchanger corrosion test was recovered. (camilleri2025coldsprayas pages 1-2)

**Organizational attribution and trade press:** Specific Cu–Ni/NAB primary experimental results from **NSWC Carderock, NSWC Philadelphia, or NRL**, an explicitly **ONR-funded** Cu–Ni/NAB alloy-design experiment, and named Navy casting-delay measurements were **not verified**. Penn State ARL’s acknowledgment in the cold-spray paper is **not** proof of Navy funding; NPS affiliation and Oregon State’s explicitly acknowledged Navy grant are firmer, but different, connections. No independently verified trade-press article with reliable alloy/test numbers was recovered; **none of the numerical benchmarks above is attributed to trade press**. Proposed seawater tests should explicitly distinguish **3.5% NaCl, ASTM D1141 substitute seawater, and natural/flowing seawater**, which are not interchangeable evidence of shipboard durability. (sparrow2025lpbfparameteroptimization pages 1-3, doyle2022additivemanufacturingof pages 53-58, shahriari2023corrosionperformanceof pages 14-14, camilleri2025coldsprayas pages 1-2, shuvo2025towardreducingcasting pages 1-2)

## Top 5 things the PI should know

1. **Frame novelty narrowly and accurately:** laser-deposited NAB, composition-dependent NAB corrosion, as-built seawater exposure, and powder-DED deposition onto cast NAB each have precedents. The stronger distinct contribution is a **measured, single-pre-alloyed-powder composition→powder→laser-DED→as-deposited corrosion network**, including **both cast NAB and wrought Cu–Ni repair interfaces**. (nemani2024advancementsinadditive pages 74-79, doyle2022additivemanufacturingof pages 53-58, nemani2024advancementsinadditive pages 113-114, nemani2024advancementsinadditive pages 79-83)
2. **Use a true concurrent control:** measure wrought **C71500 alongside every deposited composition** under the **same** electrolyte, immersion duration, surface preparation, and hydrodynamic conditions; published NaCl tests and unmatched 24/96-hour exposures cannot establish the stated performance threshold. (nemani2024advancementsinadditive pages 102-105, shahriari2023corrosionperformanceof pages 14-14, shahriari2023corrosionperformanceof pages 2-2)
3. **Make corrosion and integrity separate gates:** high density and strength alone did not make the published CuNi2SiCr-on-NAB repair suitable, while heat treatment reduced NAB corrosion resistance in WAAM experiments. Quantify **interface cracking, porosity, microgalvanic/selective attack, and corrosion** in the **as-deposited** state. (doyle2022additivemanufacturingof pages 53-58, shahriari2023corrosionperformanceof pages 12-14, nemani2024advancementsinadditive pages 79-83)
4. **Benchmark powder production against NPS without conflating metrologies:** its D10/D50/D90 and apparent density are useful, but GranuDrum cohesion is not Hall flow, and its ~5 wt% EDS oxygen is **not** a validated oxygen-content specification. Record lot-by-lot **chemistry, oxygen by an appropriate quantitative method, size distribution, Hall flow, and apparent density**. (sparrow2025lpbfparameteroptimization pages 11-12, sparrow2025lpbfparameteroptimization pages 8-11)
5. **Do not claim procurement savings or NAVSEA approval prematurely:** distinguish **peer-reviewed naval application**, **documented Navy grant**, **NPS affiliation**, **ARL technical acknowledgment**, and **formal NAVSEA qualification**. Quantified shipyard casting delays, qualification criteria, flow-seawater Cu–Ni baselines, and verified results from several named Navy laboratories remain **evidence gaps**, not facts to fill from trade-press inference. (doyle2022additivemanufacturingof pages 43-47, doyle2022additivemanufacturingof pages 53-58, camilleri2025coldsprayas pages 1-2, shuvo2025towardreducingcasting pages 1-2)

References

1. (sparrow2025lpbfparameteroptimization pages 1-3): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

2. (doyle2022additivemanufacturingof pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

3. (guerra2023microstructureandmechanical pages 1-2): Carolina Guerra, Jorge A. Ramos-Grez, Iván La Fé-Perdomo, Alejandro Castillo, and Magdalena Walczak. Microstructure and mechanical properties of cu-11al-5ni-4fe wt% manufactured by lpbf. Metals, 13:459, Feb 2023. URL: https://doi.org/10.3390/met13030459, doi:10.3390/met13030459. This article has 11 citations.

4. (guerra2023microstructureandmechanical pages 2-4): Carolina Guerra, Jorge A. Ramos-Grez, Iván La Fé-Perdomo, Alejandro Castillo, and Magdalena Walczak. Microstructure and mechanical properties of cu-11al-5ni-4fe wt% manufactured by lpbf. Metals, 13:459, Feb 2023. URL: https://doi.org/10.3390/met13030459, doi:10.3390/met13030459. This article has 11 citations.

5. (tan2024effectofalni pages 1-2): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

6. (tan2024effectofalni pages 6-10): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

7. (tan2024effectofalni pages 10-12): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

8. (doyle2022additivemanufacturingof pages 1-9): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

9. (doyle2022additivemanufacturingof pages 43-47): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

10. (doyle2022additivemanufacturingof pages 47-53): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

11. (shuvo2025towardreducingcasting pages 1-2): Md Moinuddin Shuvo, Philip King, Robert Voigt, and Guha Manogharan. Toward reducing casting defects via 3d risers via 3d sand-printing: a simulation study. International Journal of Metalcasting, May 2025. URL: https://doi.org/10.1007/s40962-024-01353-1, doi:10.1007/s40962-024-01353-1. This article has 5 citations and is from a peer-reviewed journal.

12. (shuvo2025towardreducingcasting pages 10-12): Md Moinuddin Shuvo, Philip King, Robert Voigt, and Guha Manogharan. Toward reducing casting defects via 3d risers via 3d sand-printing: a simulation study. International Journal of Metalcasting, May 2025. URL: https://doi.org/10.1007/s40962-024-01353-1, doi:10.1007/s40962-024-01353-1. This article has 5 citations and is from a peer-reviewed journal.

13. (sparrow2025lpbfparameteroptimization pages 3-6): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

14. (sparrow2025lpbfparameteroptimization pages 11-12): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

15. (sparrow2025lpbfparameteroptimization pages 8-11): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

16. (sparrow2025lpbfparameteroptimization media e92f46e3): Andrew Sparrow, Walter Smith, and Troy Y. Ansell. Lpbf parameter optimization of mechanical, non-thermal generated c71500 powder. Metals, 16:10, Dec 2025. URL: https://doi.org/10.3390/met16010010, doi:10.3390/met16010010. This article has 1 citations.

17. (shahriari2023corrosionperformanceof pages 12-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

18. (shahriari2023corrosionperformanceof pages 14-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

19. (shahriari2023corrosionperformanceof pages 2-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

20. (shahriari2023corrosionperformanceof pages 10-10): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 30 citations and is from a peer-reviewed journal.

21. (nemani2024advancementsinadditive pages 71-74): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

22. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

23. (nemani2024advancementsinadditive pages 113-114): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

24. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

25. (nemani2024advancementsinadditive pages 112-113): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

26. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

27. (nemani2024advancementsinadditive pages 68-71): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

28. (camilleri2025coldsprayas pages 1-2): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

29. (camilleri2025coldsprayas pages 10-12): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

30. (nemani2024advancementsinadditive pages 102-105): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

31. (nemani2024advancementsinadditive pages 105-106): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

32. (nemani2024advancementsinadditive pages 41-43): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

33. (nemani2024advancementsinadditive pages 110-112): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

34. (heniken2025influenceofmicrostructure pages 1-8): NH Heniken. Influence of microstructure on fatigue behavior, crack initiation, and crack growth in wire-arc additively manufactured nickel aluminum-bronze. Unknown journal, 2025.
