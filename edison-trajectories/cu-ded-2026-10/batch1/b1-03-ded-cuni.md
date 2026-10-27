<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: 70814fb7-d0ca-4d06-8818-841e6a0154c9
- Submitted: 2026-10-17T05:10:43Z
- Fetched: 2026-10-17T05:42:03Z (status: success)
- Raw trajectory JSON: ../raw/b1-03-ded-cuni.json.gz
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

QUESTION: What is known about additive manufacturing of copper-nickel alloys
(90-10 C70600, 70-30 C71500, Cu-Ni-Fe-Mn, Cr-modified Cu-Ni such as C72200
or CuNi30Cr2) by blown-powder laser DED or laser cladding, and by wire-arc
DED and LPBF for comparison? Report printability (porosity, hot cracking,
lack of fusion), microsegregation of Ni, Fe and Mn and dendrite spacing,
hardness and tensile data, and any seawater or NaCl corrosion testing of the
printed material versus wrought. Is there ANY corrosion study of Cu-Ni made by
blown-powder laser DED? Which groups (Navy labs, Penn State ARL, NSWC
Carderock, universities, companies) have published on printed Cu-Ni?

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

QUESTION: What is known about additive manufacturing of copper-nickel alloys
(90-10 C70600, 70-30 C71500, Cu-Ni-Fe-Mn, Cr-modified Cu-Ni such as C72200
or CuNi30Cr2) by blown-powder laser DED or laser cladding, and by wire-arc
DED and LPBF for comparison? Report printability (porosity, hot cracking,
lack of fusion), microsegregation of Ni, Fe and Mn and dendrite spacing,
hardness and tensile data, and any seawater or NaCl corrosion testing of the
printed material versus wrought. Is there ANY corrosion study of Cu-Ni made by
blown-powder laser DED? Which groups (Navy labs, Penn State ARL, NSWC
Carderock, universities, companies) have published on printed Cu-Ni?

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


# Additively manufactured marine copper–nickel: evidence and proposal risks

**The central correction is that a corrosion study of blown-powder laser-deposited Cu–Ni does exist.** Bhattacharya and colleagues reported corrosion testing of direct-metal-deposited (DMD) Cu–30Ni on wrought C71500 in 2011. A shipbuilding literature review states that the deposited material corroded more than the wrought substrate and attributes the difference to deposit porosity. Thus, the defensible gap is **not** “first corrosion test of laser-DED Cu–Ni”; it is a controlled demonstration of *pre-alloyed, single-stream powders*, composition optimization, and **as-deposited** performance on both Cu–Ni and cast NAB repair substrates against a wrought C71500 benchmark. The primary 2011 article was not available in full text here, so its electrolyte, exposure duration, corrosion rate, and pore fraction cannot be verified. (andric2012materialsandfabrication pages 15-17)

## Laser powder DED and laser cladding

1. **[CITE] [NAVY] [NOVELTY-RISK] [GAP]** S. Bhattacharya, G. P. Dinda, A. K. Dasgupta, H. Natu, B. Dutta, and J. Mazumder, “Microstructural evolution and mechanical, and corrosion property evaluation of Cu–30Ni alloy formed by direct metal deposition process,” *Journal of Alloys and Compounds* **509** (2011), 6364–6373. **DOI: 10.1016/j.jallcom.2011.03.091.** Process: CO₂-laser DMD of nominal **70Cu–30Ni wt%** onto *rolled C71500 plate*, for a marine-corrosion application. The contemporary shipbuilding review reports higher ultimate strength but lower yield strength and elongation for the clad material than for the substrate. It reports **worse corrosion resistance for the standalone DMD clad than wrought C71500**, associated with clad porosity, and discusses a clad/substrate specimen separately. This is a direct prior-art challenge to any unqualified novelty claim about powder-laser-DED Cu–Ni corrosion. **Unverified from the accessible evidence:** powder provenance and size, whether pre-alloyed, electrolyte, flow, exposure, density, exact mechanical or corrosion values, and whether the clad alone was tested in its as-deposited state. The bibliographic particulars identify the primary article; the experimental findings above come from a secondary account, not inspection of that article. (andric2012materialsandfabrication pages 15-17)

2. **[CITE] [NUMBERS] [GAP]** S. Yadav, A. N. Jinoop, N. Sinha, C. P. Paul, and K. S. Bindra, “Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers,” *International Journal of Advanced Manufacturing Technology* **108** (2020), 3779–3791. **DOI: 10.1007/s00170-020-05644-9.** Process: blown-powder laser DED, **not pre-alloyed single-stream powder**: elemental Cu and Ni powders, each **45–105 µm**, premixed for 18 h into **25Cu–75Ni, 50Cu–50Ni, and 75Cu–25Ni wt%** feeds, then deposited in graded layers on Cu plate preheated to 250 °C. Optimized tracks used **1.8 kW** and **0.7, 0.7, and 0.5 m min⁻¹**, respectively. Image-based relative density was **>99%** overall; reported porosity was **<0.5%** in Ni-rich/middle regions but approached **2%** in Cu-richer regions/interfaces. The authors identify trapped gas, incomplete melting/lack of fusion, and Cu’s high reflectivity/heat conduction as concerns. Fine cellular/dendritic lower layers transitioned toward equiaxed upper layers; hardness spanned approximately **115 HV at the Ni end to 47 HV at the Cu end**, measured at a **1.96 N** load. **No tensile, measured dendrite-arm-spacing, Fe/Mn segregation, or corrosion test** is reported. The designation *CuNi25* means **75Cu–25Ni**, not C71500. This establishes processing feasibility, but neither marine-grade chemistry nor the proposed feedstock/corrosion combination. (yadav2020parametricinvestigationand pages 2-4, yadav2020parametricinvestigationand pages 7-10, yadav2020parametricinvestigationand pages 10-12)

3. **[CITE] [GAP]** B. Adak, P. Nash, D. Chen, and A. Swiglo, “Microstructural characterization of laser cladding of Cu-30Ni,” *Journal of Materials Science* **40** (2005), 2051–2054. **DOI: 10.1007/s10853-005-1231-5**; and S. Bhattacharya, G. P. Dinda, A. K. Dasgupta, and J. Mazumder, “A comparative study of microstructure and mechanical behavior of CO₂ and diode laser deposited Cu–38Ni alloy,” *Journal of Materials Science* **49** (2014), 2415–2429. **DOI: 10.1007/s10853-013-7883-7.** These are further **laser-cladding/laser-deposition** Cu–Ni precedents: nominal **70Cu–30Ni** and **62Cu–38Ni wt%**, respectively. Their primary texts could not be inspected; consequently powder type, porosity, dendrite spacing, hardness, strength, and corrosion conditions **must not be assigned numerical values here**. The latter is not a 10–30 wt% Ni marine-grade deposit. (andric2012materialsandfabrication pages 15-17)

4. **[NOVELTY-RISK] [GAP]** Y. Zhou, D. Wen, and X. Zuo, “Current-carrying fretting wear and electrochemical corrosion properties of laser-cladded Cu-Ni-xCr coatings,” *Wear* (2025), article **205960**. **DOI: 10.1016/j.wear.2025.205960.** Its title identifies **laser-cladded Cu–Ni–Cr and electrochemical corrosion**, so claims that *no* laser-cladded Cu–Ni–Cr corrosion work exists are unsafe. The source was unobtainable: **x, deposition feed mode, NaCl composition, corrosion numbers, and marine applicability are unverified**. In particular, a current-carrying fretting experiment cannot automatically be treated as static seawater immersion or as evidence for C72200/CuNi30Cr2. No verified pre-alloyed-powder DED seawater dataset for either of those named grades emerged from the accessible primary evidence. (andric2012materialsandfabrication pages 15-17)

## Wire-arc DED and wrought comparators

5. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK]** O. O. Adeeko, *Processing/Structure/Properties of Wire-Arc Additively Manufactured 70Cu-30Ni Alloy*, MS thesis, Case Western Reserve University, January **2026**; **DOI not established**. John J. Lewandowski advised this **ONR-funded** work; Lincoln Electric made the WAAM blocks, and a second block was supplied to Steven Policastro at the **Naval Research Laboratory**. The Techalloy 413 feed wire was approximately **67.5Cu–30Ni–0.70Mn–0.55Fe–0.25Ti–0.10Si wt%**. On examined cross-sections, the as-deposited build showed **no visible pores or cracks**—*not* a quantified bulk-density determination—and exhibited columnar/equiaxed dendrites. SEM-EDS found **Ni-rich dendrite cores and Cu-rich interdendritic material**; a numerical dendrite spacing is not established here, nor are trustworthy Fe/Mn segregation amplitudes. As-deposited tensile results were **303/444 MPa yield/UTS** along the deposition direction and **295/442 MPa** transverse, with **52%/46% reduction in area (RA)**. *RA is not tensile elongation.* Measured as-deposited Rockwell B hardness varied by sampled plane: **69.3 HRB (XY), 53.5 HRB (YZ), 70.7 HRB (XZ)**; it must not be presented as HV. (adeeko2026processingstructurepropertiesofwirearc pages 1-7, adeeko2026processingstructurepropertiesofwirearc pages 15-20, adeeko2026processingstructurepropertiesofwirearc pages 36-43, adeeko2026processingstructurepropertiesofwirearc pages 59-71, adeeko2026processingstructurepropertiesofwirearc pages 71-80, adeeko2026processingstructurepropertiesofwirearc pages 92-102, adeeko2026processingstructurepropertiesofwirearc pages 128-138)

   **Environmental test distinction:** the thesis performed **slow-strain-rate tensile testing, not an electrochemical corrosion-rate or 30-day immersion test**, at **10⁻⁶ s⁻¹**, approximately **20 °C**, in ASTM **D1141 Formula A substitute ocean water** adjusted to **pH 8.2**, against tests in air. As-deposited longitudinal samples gave **257 MPa yield/358 MPa UTS/69% RA in solution** versus **262/360 MPa/70% RA in air**; transverse samples gave **245/348 MPa/76% RA in solution** versus **278/370 MPa/66% RA in air**. The varying responses and single-condition scope do **not** establish equivalent long-term corrosion resistance to wrought C71500. The thesis reports no *i*₍corr₎, *E*₍corr₎, impedance, immersion rate, or selective-attack depth for these deposits. (adeeko2026processingstructurepropertiesofwirearc pages 48-54, adeeko2026processingstructurepropertiesofwirearc pages 118-123)

6. **[CITE] [NUMBERS] [GAP]** C. Guo, T. Kang, S. Wu, M. Ying, W. M. Liu, and F. Chen, “Microstructure, mechanical, and corrosion resistance of copper nickel alloy fabricated by wire-arc additive manufacturing,” *MRS Communications* **11** (2021), 910–916. **DOI: 10.1557/s43579-021-00120-1.** Process: **WAAM**, reported in a later thesis as nominal **70Cu–30Ni**, with a predominantly dendritic, single-FCC-phase deposit and columnar, remelted, and heat-affected regions. That thesis reproduces longitudinal **219 MPa yield, 367 MPa UTS, 37% RA** and transverse **199 MPa, 341 MPa, 38% RA**. The article’s corrosion methodology and quantitative result could not be checked against its primary text; **do not infer seawater composition, corrosion rate, or a wrought-matched improvement** from its title. (adeeko2026processingstructurepropertiesofwirearc pages 138-144, adeeko2026processingstructurepropertiesofwirearc pages 26-31, adeeko2026processingstructurepropertiesofwirearc pages 102-107)

7. **[CITE] [NOVELTY-RISK] [GAP]** J. Song, X. A. Jimenez, A. C. To, and Y. Fu, “Microstructures and Corrosion Properties of Wire Arc Additive Manufactured Copper–Nickel Alloys,” *Materials* **17** (2024), article **876**. **DOI: 10.3390/ma17040876** (*inferred from the journal’s volume/issue/article-number convention; verify against the publisher before submission*). A subsequent thesis identifies **three-layer, approximately 100-mm-long WAAM 70Cu–30Ni tracks** and reports that dendrite-arm spacing varies near fusion boundaries. It describes **potentiodynamic-test corrosion anisotropy**, with the **YZ face outperforming XY**. The primary paper was inaccessible here: exact spacing, feed chemistry, electrolyte, polarization numbers, density, and wrought control remain **unverified**. The Penn State-affiliated A. C. To group is thus a relevant **wire-arc**, not proof of a pre-alloyed powder-laser-DED study. (adeeko2026processingstructurepropertiesofwirearc pages 138-144, adeeko2026processingstructurepropertiesofwirearc pages 26-31)

8. **[NUMBERS]** For *context rather than a same-batch corrosion control*, the Adeeko thesis lists representative **annealed wrought 70/30 tube: 170 MPa proof strength, 420 MPa UTS, 42% elongation, 105 HV10**; and annealed plate: approximately **150 MPa, 390 MPa, 42%, 95 HV10**. Product temper and proof-stress definition matter: these tabulated values are **not** matched specimens tested beside the WAAM blocks, and **HV10 cannot be numerically equated with HRB**. (adeeko2026processingstructurepropertiesofwirearc pages 31-36)

## LPBF and lower-Ni cast-alloy comparisons

9. **[CITE] [NOVELTY-RISK] [GAP]** Z. Liu *et al.*, “Investigation on mechanical properties and corrosion behavior of laser powder bed fusion 70/30 copper-nickel alloy,” *Corrosion Science* (2024), article **112040**. **DOI: 10.1016/j.corsci.2024.112040**; M. Nadimi, J. Song, L. Cheng, and Y. Fu, “Corrosion evaluation and microstructural characteristics of 70/30 copper-nickel alloy fabricated by laser powder bed fusion,” *Journal of Alloys and Metallurgical Systems* (2025), article **100155**. **DOI: 10.1016/j.jalmes.2025.100155**; and M. Roshan *et al.*, “Powder bed fused–laser beam (PBF-LB) 70/30 copper-nickel (Cu-30Ni): hierarchical microstructure and mechanical properties,” *Journal of Alloys and Compounds* (2025). **DOI: 10.1016/j.jallcom.2025.183312.** Their discoverable bibliographic records establish **LPBF 70/30 mechanical/corrosion prior art**, including work associated with the Song/Fu group; they do **not** establish blown-powder DED results. None of these primary articles was available for extraction, so reporting specific density, powder oxygen, *i*₍corr₎, *E*₍corr₎, impedance, selective-attack depth, tensile values, seawater chemistry, or wrought comparison would be speculative. (adeeko2026processingstructurepropertiesofwirearc pages 138-144)

10. **[CITE] [NUMBERS] [GAP]** R. Yang, J. Wen, Y. Zhou, K. Song, and Z. Song, “Effect of Al Element on the Microstructure and Properties of Cu-Ni-Fe-Mn Alloys,” *Materials* **11** (2018), 1777. **DOI: 10.3390/ma11091777.** Process: **vacuum-induction-melted conventional alloy**, *not* AM or NAB. Tested **Cu-balance–7Ni–(0–7)Al–1Fe–1Mn wt%** in **room-temperature artificial seawater for 10 days**, changing solution on day seven. At **3 wt% Al**, tensile strength was **395 MPa** and weight-loss corrosion rate **0.0215 mm yr⁻¹**; the paper reports **245 MPa** and **0.0359 mm yr⁻¹** for its commercial **C70600** comparison. The seawater recipe included **24.53 g L⁻¹ NaCl** plus magnesium/calcium chlorides, sulfate, and minor seawater salts. These are useful lower-Ni design signals, **not evidence that an as-deposited laser powder will duplicate cast-alloy behavior**, and C70600 is **not** the requested C71500 acceptance control. The article’s conclusion contains an internally inconsistent sentence about whether all Al-containing alloys outperform Al-free alloy; rely on its explicitly stated **3%-Al-versus-C70600** comparison rather than that generalization. (yang2018effectofal pages 1-3, yang2018effectofal pages 9-11)

## Evidence boundaries and relevant groups

**No verified quantitative printed-material evidence** was obtained for **C70600 powder-laser DED**, **C72200/CuNi30Cr2 pre-alloyed single-stream DED**, **wire-laser DED of marine Cu–Ni**, Cu–Ni repair deposits **on cast NAB**, or measured **Fe/Mn interdendritic partition coefficients, powder Hall flow/apparent density/oxygen, 30-day marine immersion, flow-dependent attack, and selective-attack depth** across a matched printed-versus-wrought series. The retrieved records identify some LPBF and laser-clad corrosion studies, but their titles alone cannot supply these missing measurements. In particular, **3.5 wt% NaCl, ASTM D1141 substitute seawater, and natural flowing seawater are different exposures** and should not be merged into one corrosion benchmark. (andric2012materialsandfabrication pages 15-17, adeeko2026processingstructurepropertiesofwirearc pages 48-54, yang2018effectofal pages 1-3)

**Published contributors distinguishable from these sources:** Dinda/Dasgupta/Dutta/Mazumder and coworkers published the consequential laser-DMD Cu–30Ni work; Yadav/Jinoop/Paul/Bindra published graded elemental-powder LDED; Guo and coworkers published WAAM Cu–Ni; Song/Jimenez/To/Fu published WAAM corrosion work; Case Western/Lewandowski, **Lincoln Electric**, and **NRL** appear explicitly in the ONR-funded 2026 WAAM program. The provided evidence **does not establish that Penn State Applied Research Laboratory or NSWC Carderock authored one of the specific verified Cu–Ni powder-DED papers**, and it would be misleading to label the 2011 DMD paper as Carderock research without an affiliation or funding record. (andric2012materialsandfabrication pages 15-17, yadav2020parametricinvestigationand pages 2-4, adeeko2026processingstructurepropertiesofwirearc pages 138-144, adeeko2026processingstructurepropertiesofwirearc pages 15-20, adeeko2026processingstructurepropertiesofwirearc pages 36-43)

## Top 5 things the PI should know

1. **Prior-art red flag:** the **2011 Bhattacharya Cu–30Ni DMD corrosion comparison** already exists; explicitly cite and improve on its reported **porosity-associated deficit relative to wrought C71500**. (andric2012materialsandfabrication pages 15-17)
2. **Define novelty narrowly and verifiably:** pre-alloyed, single-stream powder composition and lot quality; dense crack-free *as-deposited* deposits **on themselves and on both repair substrates**; matched C71500 corrosion tests; and thermal-history-conditioned CALPHAD/network optimization—not merely “first Cu–Ni DED” or “first Cu–Ni DED corrosion.” (andric2012materialsandfabrication pages 15-17, yadav2020parametricinvestigationand pages 2-4, adeeko2026processingstructurepropertiesofwirearc pages 36-43)
3. **Expect spatially nonuniform behavior:** Cu-rich portions of graded laser builds showed more pores, and WAAM showed **Ni-rich dendrite cores** and face-dependent corrosion; measure defect distributions, microsegregation, and both surface orientations rather than using one bulk-density or polarization value. (yadav2020parametricinvestigationand pages 7-10, adeeko2026processingstructurepropertiesofwirearc pages 92-102, adeeko2026processingstructurepropertiesofwirearc pages 26-31)
4. **Specify the performance comparison in advance:** wrought **C71500 from the same test campaign**, identical preparation and exposure, plus short electrochemistry and long immersion; do not equate seawater SSRT, polarization, and 30-day mass-loss outcomes. (adeeko2026processingstructurepropertiesofwirearc pages 48-54, adeeko2026processingstructurepropertiesofwirearc pages 118-123, andric2012materialsandfabrication pages 15-17)
5. **Lower Ni is promising but unproved in AM:** conventional **7Ni–3Al–1Fe–1Mn** reportedly outperformed its C70600 comparator in a 10-day artificial-seawater experiment; transferring that outcome to DED and achieving the more demanding **C71500** target, particularly across NAB repair interfaces, remain experimental questions. (yang2018effectofal pages 1-3, yang2018effectofal pages 9-11)

References

1. (andric2012materialsandfabrication pages 15-17): J Andric, D Brennan, JD Caprace, CM Chou, and J Gordo. Materials and fabrication technology. Unknown journal, 2012.

2. (yadav2020parametricinvestigationand pages 2-4): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

3. (yadav2020parametricinvestigationand pages 7-10): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

4. (yadav2020parametricinvestigationand pages 10-12): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

5. (adeeko2026processingstructurepropertiesofwirearc pages 1-7): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

6. (adeeko2026processingstructurepropertiesofwirearc pages 15-20): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

7. (adeeko2026processingstructurepropertiesofwirearc pages 36-43): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

8. (adeeko2026processingstructurepropertiesofwirearc pages 59-71): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

9. (adeeko2026processingstructurepropertiesofwirearc pages 71-80): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

10. (adeeko2026processingstructurepropertiesofwirearc pages 92-102): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

11. (adeeko2026processingstructurepropertiesofwirearc pages 128-138): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

12. (adeeko2026processingstructurepropertiesofwirearc pages 48-54): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

13. (adeeko2026processingstructurepropertiesofwirearc pages 118-123): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

14. (adeeko2026processingstructurepropertiesofwirearc pages 138-144): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

15. (adeeko2026processingstructurepropertiesofwirearc pages 26-31): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

16. (adeeko2026processingstructurepropertiesofwirearc pages 102-107): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

17. (adeeko2026processingstructurepropertiesofwirearc pages 31-36): OO Adeeko. Processing/structure/properties of wire-arc additively manufactured 70cu-30ni alloy. Unknown journal, 2026.

18. (yang2018effectofal pages 1-3): Ran Yang, Jiuba Wen, Yanjun Zhou, Kexing Song, and Zhengcheng Song. Effect of al element on the microstructure and properties of cu-ni-fe-mn alloys. Materials, 11:1777, Sep 2018. URL: https://doi.org/10.3390/ma11091777, doi:10.3390/ma11091777. This article has 28 citations.

19. (yang2018effectofal pages 9-11): Ran Yang, Jiuba Wen, Yanjun Zhou, Kexing Song, and Zhengcheng Song. Effect of al element on the microstructure and properties of cu-ni-fe-mn alloys. Materials, 11:1777, Sep 2018. URL: https://doi.org/10.3390/ma11091777, doi:10.3390/ma11091777. This article has 28 citations.
