<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 41b884d2-755a-4c74-98fd-9b3ae0a36029
- Submitted: 2026-10-17T18:59:55Z
- Fetched: 2026-10-17T19:33:08Z (status: success)
- Raw trajectory JSON: ../raw/el-22-P.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

ELEMENT UNDER REVIEW: P (dealloying inhibitor). Phosphorus-deoxidized copper C12200 (0.015-0.040 P), phosphor bronzes (0.03-0.35 P), inhibited admiralty C44500; impurity limit in Cu-Ni (about 0.02 wt% for weldable grades) because P promotes hot cracking in Cu-Ni welds.

Answer for P specifically, not for copper alloys in general:
1. ROLE: what P does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their P ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how P changes corrosion of
   copper alloys in natural or substitute seawater or 3.5 wt% NaCl (corrosion
   rate, Ecorr, film resistance, pitting, crevice, dealloying, erosion-
   corrosion and velocity limits). Give the range where it helps and where it
   harms.
3. DED AND WELDING: effect on solidification cracking, liquation cracking in
   reheated layers, porosity, evaporation or oxidation loss under a laser,
   and on dilution into cast NAB or wrought Cu-Ni repair substrates. Use
   welding and cladding literature (ERCuNi, ERCuAl-A2, ERCuNiAl, ERCuMnNiAl
   fillers) where AM data are missing, and say so.
4. POWDER MAKING: problems in induction melting and atomization (oxidation,
   reaction with alumina, zirconia or graphite crucibles or with a titanium-
   alloy or molybdenum sonotrode, vapor loss, effect on liquidus and surface
   tension).
5. PHASE DIAGRAM AND CALPHAD: maximum solid solubility in Cu (wt%, and the
   temperature), intermetallics and invariant reactions in Cu-P, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-P, Cu-Ni-P and Cu-Al-P are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of P in the alloy (Cu balance):
   a. DECISION: INCLUDE as a designed addition, LIMIT as an impurity only, or
      EXCLUDE, with a one-paragraph reason.
   b. If INCLUDE: a CONSERVATIVE upper bound (from established commercial or
      Navy alloys, or demonstrated AM or cladding), a NON-CONSERVATIVE upper
      bound (defensible but aggressive: experimental alloys, solubility or
      phase-boundary limits, the liquidus limit), and a FUNCTIONAL FLOOR (the
      smallest content with a measurable effect). Say which family (Cu-Ni,
      aluminum bronze, or both) each bound applies to.
   c. If LIMIT: the maximum tolerable content (wt% or ppm) in DED powder and
      deposit, and the specification or study it comes from.
   d. The failure mode that sets each bound.
8. INTERACTIONS for a later joint-constraint analysis: sums or ratios with Ni,
   Fe, Mn, Al or other elements; elements that P neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | P | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

ELEMENT UNDER REVIEW: P (dealloying inhibitor). Phosphorus-deoxidized copper C12200 (0.015-0.040 P), phosphor bronzes (0.03-0.35 P), inhibited admiralty C44500; impurity limit in Cu-Ni (about 0.02 wt% for weldable grades) because P promotes hot cracking in Cu-Ni welds.

Answer for P specifically, not for copper alloys in general:
1. ROLE: what P does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their P ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how P changes corrosion of
   copper alloys in natural or substitute seawater or 3.5 wt% NaCl (corrosion
   rate, Ecorr, film resistance, pitting, crevice, dealloying, erosion-
   corrosion and velocity limits). Give the range where it helps and where it
   harms.
3. DED AND WELDING: effect on solidification cracking, liquation cracking in
   reheated layers, porosity, evaporation or oxidation loss under a laser,
   and on dilution into cast NAB or wrought Cu-Ni repair substrates. Use
   welding and cladding literature (ERCuNi, ERCuAl-A2, ERCuNiAl, ERCuMnNiAl
   fillers) where AM data are missing, and say so.
4. POWDER MAKING: problems in induction melting and atomization (oxidation,
   reaction with alumina, zirconia or graphite crucibles or with a titanium-
   alloy or molybdenum sonotrode, vapor loss, effect on liquidus and surface
   tension).
5. PHASE DIAGRAM AND CALPHAD: maximum solid solubility in Cu (wt%, and the
   temperature), intermetallics and invariant reactions in Cu-P, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-P, Cu-Ni-P and Cu-Al-P are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of P in the alloy (Cu balance):
   a. DECISION: INCLUDE as a designed addition, LIMIT as an impurity only, or
      EXCLUDE, with a one-paragraph reason.
   b. If INCLUDE: a CONSERVATIVE upper bound (from established commercial or
      Navy alloys, or demonstrated AM or cladding), a NON-CONSERVATIVE upper
      bound (defensible but aggressive: experimental alloys, solubility or
      phase-boundary limits, the liquidus limit), and a FUNCTIONAL FLOOR (the
      smallest content with a measurable effect). Say which family (Cu-Ni,
      aluminum bronze, or both) each bound applies to.
   c. If LIMIT: the maximum tolerable content (wt% or ppm) in DED powder and
      deposit, and the specification or study it comes from.
   d. The failure mode that sets each bound.
8. INTERACTIONS for a later joint-constraint analysis: sums or ratios with Ni,
   Fe, Mn, Al or other elements; elements that P neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | P | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Phosphorus (P): composition decision for seawater-exposed copper-alloy DED

**Decision — LIMIT P as an impurity, not a designed dealloying inhibitor, across both Cu–Ni and aluminum-bronze candidates.** Specify **P ≤0.020 wt% (200 ppm by mass) in both atomized powder and deposited metal**, with **≤0.015 wt% (150 ppm) as a tighter screening target for aluminum-bronze compositions**. These are *proposed project controls*, not proof of a universal cracking threshold: a welding-grade C70600 composition table reports 0.020 wt% maximum, while an aluminum-bronze C61400 entry reports 0.015 wt%; published metallurgy also explicitly identifies P as detrimental to Cu–Ni weldability and keeps it low in aluminum bronze for ductility. Most importantly, I found no controlled evidence that increasing P in an *as-deposited*, weldable Cu–Ni/NAB alloy improves seawater resistance. The genuine beneficial examples involve different matrices, environments, or combined additions. The constraint should apply to the **measured deposit**, not just the charge, because substrate dilution and processing losses can change its composition. (carlone2019dissimilarmetalwelding media c13403fc, konynenburg1990backgroundstudiesin pages 149-155, galai2021effectofphosphorus pages 1-2)

## 1. Metallurgical role and relevant alloys

**[CITE][SPEC] Distinguish residual P from a designed P-bearing alloy.** Phosphorus-deoxidized copper **C12200** is commonly identified with **0.015–0.040 wt% P**, and phosphor bronzes with roughly **0.03–0.35 wt% P**; these ranges are useful comparators but **are not transferable specifications for Cu–Ni or NAB**. A reproduced alloy-composition table specifically identifies phosphor bronze **C51000 at 0.03–0.35 wt% P**; the same table identifies **C61400 aluminum bronze at 0.015 wt% maximum**, **welding-grade C70600 at 0.020 wt% maximum**, and a **C71581/ERCuNi entry at 0.020 wt% maximum**. The table's machine-extracted columns are badly disordered; its visually inspected assignments should be checked against the current purchase edition of **ASTM B111/B171/B466/B148/B369 or AWS A5.7**, as applicable, before claiming formal compliance. I could not authenticate P ranges from those standards for C95800, ERCuNiAl, ERCuMnNiAl, or C71500 in the retrieved material. Likewise, **C44500 “inhibited admiralty brass” must not automatically be called a phosphorus-specified grade**: inhibitor discussions encompass *alternatives* including arsenic, antimony, and P, but an authoritative C44500 P requirement was not verified. (carlone2019dissimilarmetalwelding media c13403fc, carlone2019dissimilarmetalwelding pages 18-18, carlone2019dissimilarmetalwelding pages 18-19, davies1993anoteon pages 1-3)

**[CITE] Mechanisms are family dependent.** In copper and tin bronze, P scavenges oxygen during melting, can remain in α-Cu solid solution, and at higher local concentrations produces **Cu₃P**; tin-bearing bronze can develop a late **α + tin-rich δ + Cu₃P** constituent. In Ni-bearing copper, P can instead form **Ni₂P, Ni₃P or MnNiP**, depending on composition and thermal history. Choi and Lee directly identified **Ni₂P** strengthening in *aged* Cu–0.89Ni–0.22P and **MnNiP** in aged Cu–Ni–Mn–P; those are electronic alloys requiring solution treatment and aging, **not evidence of useful as-deposited seawater films**. A cast Cu–20Pb–5Sn alloy containing **2 wt% Ni** developed increasing Ni₃P and then Cu₃P with additions of **0.1–0.5 wt% P**; its microscopy documents a plausible phosphide/segregation hazard, not an allowable NAB addition. Specific P-derived protective *phosphate* film chemistry on bulk Cu–Ni or NAB in seawater was not established. Nor was a reproducible P-specific grain-refinement benefit established for NAB or Mn–Al bronze. (choi2007agingcharacteristicsand pages 1-2, ren2024strengtheningmechanismof pages 2-5, ren2024strengtheningmechanismof media 0b15dc47, ren2024strengtheningmechanismof pages 5-8, konynenburg1990backgroundstudiesin pages 142-149)

**[CITE] Dealloying inhibition has a narrower meaning.** A Copper Development Association review reports that small P additions can suppress preferential Zn dissolution in **single-phase α-brass**, possibly through an inhibitor-bearing surface film; it says the same approach is ineffective against bulk dezincification of **α–β or β brass**. A cited experiment compared **0, 0.1 and 0.2 wt%** As, Sb, or P in **5% CuCl₂**: Sb performed best; P and As were variable; increasing inhibitor above **0.1 wt%** afforded little additional benefit. The review also recounts an intergranular/corrosion-fatigue concern and a historical recommendation to keep **P below 0.015 wt%**. Suppressing *dezincification of α-brass* does not demonstrate suppression of selective attack on NAB κ phases or Cu–Ni in seawater. (davies1993anoteon pages 1-3, davies1993anoteon pages 3-4, davies1993anoteon pages 6-8)

## 2. Quantitative corrosion evidence—and its limits

**[NUMBERS][GAP] No validated P-benefit window in the specified seawater test exists in the retrieved studies.** I found no matched-composition bulk Cu–Ni, NAB, Mn–Al bronze, gunmetal, Cu–Ni–Sn, or Cu–Ni–Si series that isolates **P wt%** and reports a seawater/ASTM D1141/3.5 wt% NaCl corrosion rate, E<sub>corr</sub>, film resistance, pitting potential, crevice depth, erosion–corrosion loss, or P-dependent velocity limit. Accordingly, neither an effective seawater floor nor a concentration at which P begins to harm seawater corrosion can be stated quantitatively. A published evaluation supports **C70600 service in seawater flow up to approximately 3.0 m s⁻¹**, but this is a **base-alloy** observation, *not* a P-dependent velocity allowance. Do not use electroless Ni–P coating results as evidence for pre-alloyed copper deposits. (galai2021effectofphosphorus pages 1-2, beavers1980corrosionrelatedfailuresin pages 133-137, lewis1981evaluationofcoppernickel pages 24-26, konynenburg1990backgroundstudiesin pages 149-155)

**[NUMBERS] What controlled but nontransferable tests actually show:** Galai *et al.* tested bulk α-brasses with **0.00016, 0.057 and 0.137 wt% P** in **moist Azrou soil, not seawater**. Their respective 30-day gravimetric corrosion rates were **88.7, 68 and 18.2 µm yr⁻¹**; polarization-resistance values were approximately **55.37, 242 and 851.6 kΩ cm²**. This substantiates a P benefit in that soil/brass system only. Separately, P-deoxidized copper containing **0.014, 0.028 and 0.056 wt% P** showed falling general-corrosion rates of **38, 27 and 16 mils yr⁻¹**, respectively, in a **35 °C ammonia/air/water-vapor atmosphere**, while stress-corrosion failure under the study load accelerated to **6,298, 642 and 428 min**. Those opposing outcomes demonstrate why a reduced general-corrosion number alone is insufficient; neither test establishes a seawater DED limit. (galai2021effectofphosphorus pages 2-4, galai2021effectofphosphorus pages 4-5, galai2021effectofphosphorus pages 5-7, konynenburg1990backgroundstudiesin pages 186-192)

## 3. DED, repair welding, and atomization

**[CITE][GAP] Welding is a proxy, not P-specific DED validation.** In Cu–Ni welding, P is classified with other unacceptable impurity elements. The plausible concern in laser DED is P-enriched last liquid and/or brittle Ni phosphides along interdendritic boundaries, followed by solidification cracking or **reheating/liquation of a prior layer**. For a **wrought Cu–Ni repair**, dilution does not justify loading the powder with P: examine both the mixed first-layer composition and the unmixed upper layers. For **cast C95800 NAB**, dilution can introduce Ni, Fe and Al into a P-bearing melt and expose heterogeneous interdendritic/κ-bearing material to thermal cycling; the resulting phosphide distribution and crack response remain **untested**. No retrieved experiment gives a P-specific crack threshold for pre-alloyed, infrared-laser blown-powder DED on either substrate, and no authenticated P-limit comparison across **ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl** was available. (konynenburg1990backgroundstudiesin pages 149-155, choi2007agingcharacteristicsand pages 1-2, carlone2019dissimilarmetalwelding media c13403fc)

**[NUMBERS][CITE] A critical counterexample prevents an overbroad “P always causes Cu–Ni cracking” claim.** In *wrought/welded* **C72700, nominal Cu–9Ni–6Sn**, Tumuluru and Nippes investigated heats containing **0.10 wt% Mn together with 0.01 wt% P**. Relative to an unmodified heat, the combined additions moved brittle tin-rich γ, approximately **(Cu,Ni)₃Sn**, away from damaging grain-boundary networks and improved bend behavior; process atmosphere strongly affected porosity. There was **no P-only heat isolating its effect**, and the principal reported crack mechanism was tin-rich γ in a partially melted zone—not proof that 0.01 wt% P improves standard 70–30 Cu–Ni or NAB repair welds. Oxygen removal can reduce one source of gas pores, but P oxides/inclusions and hydrogen or shielding-related porosity must be measured independently; no P-specific 1.07-µm-laser evaporation or oxidation-loss fraction was located. (tumuluru1988weldductilitystudies pages 1-2, tumuluru1988weldductilitystudies pages 7-8, tumuluru1988weldductilitystudies pages 5-7)

**[GAP] Powder making.** Cast-bronze work demonstrates staged addition of **13.5 wt% P Cu–P master alloy** as a deoxidizer and melting in a **graphite crucible**; that is a practical charging precedent, not validation for an AMAZEMET ultrasonic atomizer. P can partition to oxides/slag or phosphides, so assay **charge, retained melt, collected powder by size fraction, deposit and fume** rather than assuming nominal P retention. No retrieved quantitative study establishes P pickup/loss, surface-tension change, aerosol yield, or reaction rates against **alumina versus zirconia crucibles**, or a **Ti-alloy versus Mo sonotrode**, under this apparatus's conditions; potential phosphate formation or Ti/Mo phosphide contamination should be treated as tests, not asserted outcomes. Add a small Cu–P master-alloy charge late under dry Ar, record oxygen and P mass balance, and qualify both powder flow and deposit chemistry before regarding P as controlled. (ren2024strengtheningmechanismof pages 2-5, konynenburg1990backgroundstudiesin pages 136-142, schlesinger2002thethermodynamicproperties pages 23-25)

## 4. Phase equilibria and CALPHAD

**[NUMBERS][CITE] Do not substitute tin-bronze solubility for binary Cu solubility.** A published Cu–P phase diagram depicts a copper-rich **L → α-Cu + Cu₃P eutectic at approximately 714 °C and 8.3–8.4 wt% P**, with maximum α-Cu solubility **approximately 1.7–1.75 wt% P at that temperature**. The separate **0.15 wt% at 714 °C** reported in a tin-bronze calculation applies to *that alloy*, not to pure binary Cu. Thus the binary solubility ceiling is emphatically **not** a safe DED/welding upper bound. The binary Cu–P liquidus falls toward the Cu-rich eutectic from pure Cu's approximately **1,085 °C** melting point; a small P addition by itself therefore does **not** push pure Cu above the approximately **1,200–1,250 °C useful-atomization liquidus ceiling**. Ni/Al/Fe-containing multicomponent liquidus and, more critically, the *terminal solidification temperature* must nevertheless be calculated for each composition. Under different P chemical potentials the assessed Cu–P system also includes **CuP₂ and Cu₂P₇**; these are not evidence that such phases precipitate in dilute Cu-rich DED metal. (schlesinger2002thethermodynamicproperties media cb6f0e44, ren2024strengtheningmechanismof pages 5-8, schlesinger2002thethermodynamicproperties pages 23-25)

**[CITE][GAP] Database audit is essential.** The Cu–P binary has a published thermodynamic assessment discussed by Schlesinger; a recent bronze study calculated a phase diagram with **Thermo-Calc**, but neither fact verifies that the laboratory's installed **TCCU version** contains **assessed Cu–Ni–P and Cu–Al–P ternaries**, or that **COST 531** supplies a validated description for these particular Cu-rich repair alloys. An executable pycalphad TDB must actually include **P in the LIQUID, FCC_A1 and relevant phosphide phase definitions** and compatible assessments at the selected Ni/Al/Mn levels. Check the installed database's assessed-systems list and reproduce the binary invariant before trusting ternary calculated crack-risk rankings. (schlesinger2002thethermodynamicproperties pages 23-25, ren2024strengtheningmechanismof pages 2-5, ren2024strengtheningmechanismof pages 5-8)

## 5. Supply, safety, and coupled constraints

**[CITE] Criticality needs a date.** The USGS's **final 2025 list** is cited as *Final 2025 List of Critical Minerals*, **90 Fed. Reg. 50494–50497 (7 November 2025)**. A USGS explanatory publication describes **60 listed commodities**, distinguishing **54 elements** from six separately named commodities including **phosphate rock**, and displays P, Ni and Cu in its accompanying periodic table. The retrieved sources did **not independently establish P's classification on the 2022 U.S. list**; do not silently equate phosphate rock, elemental P, and the copper–phosphorus master alloy, or claim an unchanged 2022-to-2025 designation. No sufficiently comparable, dated U.S. **$/kg quotation** for metallurgical Cu–P master alloy or elemental P was recovered; procurement should compare delivered **$/kg of contained P** and batch minimums, rather than quoting fertilizer/phosphate-rock prices. (olinger2026criticalmineralsmemory pages 1-2, olinger2026criticalmineralsmemory pages 2-4, rupkeUnknownyearutahmining2025 pages 31-31)

**[GAP] Safety and regulation.** Treat airborne **Cu/Ni-containing powder and laser fume** as an inhalation and combustible-metal-powder control issue; minimize fine-powder release, use suitable local exhaust and grounded/inert handling, and obtain the specific feedstock SDS and industrial-hygiene review. Elemental P, Cu–P master alloy, phosphate residues and phosphine are chemically different hazards; do **not** infer phosphine generation from a Cu–P powder without measurements. I could not verify a P-specific **OSHA exposure limit for this alloy**, a blanket **RoHS/REACH ban on P in bulk Cu alloys**, or a **Navy prohibition** in the retrieved sources. Specify occupational limits for the *measured chemical species and fume*, and applicable contract requirements, rather than inventing a P-specific Navy rule. (konynenburg1990backgroundstudiesin pages 136-142, schlesinger2002thethermodynamicproperties pages 23-25)

**[NUMBERS] Interaction constraints for subsequent optimization.** Track **P × Ni** (Ni₂P/Ni₃P competition with Cu₃P), **P × Mn × Ni** (Mn₂P/MnNiP; the reported MnNiP optimum was approximately **1:1:1 atomic Ni:Mn:P**, not a wt% recipe), and **P × Sn** (tin-rich last liquid and ternary eutectic). Track **P × oxygen** as retained oxide/inclusion burden versus deoxidation benefit, and **P × Fe** because brass grain growth changed direction around **0.005–0.007 wt% Fe** in one non-NAB study. Evaluate **P × Al × Ni × Fe** specifically for diluted NAB and its selective-attack depth; no reliable numerical ‘P + Al’ or ‘P/Ni’ seawater-safe ratio was found. The C72700 **0.01 wt% P + 0.10 wt% Mn** benefit and aged electronic-alloy phosphide strengthening are counterexamples to simplistic single-element rules, not permission to exceed the repair limit. (choi2007agingcharacteristicsand pages 1-2, davies1993anoteon pages 6-8, tumuluru1988weldductilitystudies pages 1-2, ren2024strengtheningmechanismof pages 5-8)

**Bounds and evidence quality.** **[SPEC][NUMBERS]** `impurity_max_wt=0.020` applies to **both powder and deposit** and is anchored to the retrieved **C70600 welding-grade/C71581 filler composition table**, with the stronger **0.015 wt% aluminum-bronze screening target** anchored to its C61400 entry; these are conservative *engineering choices* pending verification of controlling procurement standards. Their governing failure modes are loss of weld ductility through segregation/phosphides and reheated-boundary cracking, with uncertain localized-corrosion penalties. **Conservative designed-addition maximum, aggressive designed-addition maximum, and functional floor are NA:** assigning any would imply a reproducible seawater benefit in an as-deposited, dual-substrate repair alloy that has not been demonstrated. Confidence is **moderate for limiting P on welding/metallurgical grounds, thin for any P-specific seawater benefit or DED threshold**. (carlone2019dissimilarmetalwelding media c13403fc, konynenburg1990backgroundstudiesin pages 149-155, galai2021effectofphosphorus pages 1-2, tumuluru1988weldductilitystudies pages 7-8)

VERDICT | P | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.020 | evidence=moderate

References

1. (carlone2019dissimilarmetalwelding media c13403fc): P. Carlone and A. Astarita. Dissimilar metal welding. Metals, Nov 2019. URL: https://doi.org/10.3390/met9111206, doi:10.3390/met9111206. This article has 23 citations.

2. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

3. (galai2021effectofphosphorus pages 1-2): Mouhsine Galai, Hanane Benqlilou, Mohamed EbnTouhami, Hakima Nassali, Tounsi Belhaj, Khalifa Berrami, Ilyas Mansouri, and Bennaceur ouaki. Effect of phosphorus content of α-brass on its corrosion resistance in aggressive soil: experimental and characterization studies. Euro-Mediterranean Journal for Environmental Integration, Apr 2021. URL: https://doi.org/10.1007/s41207-021-00244-9, doi:10.1007/s41207-021-00244-9. This article has 3 citations.

4. (carlone2019dissimilarmetalwelding pages 18-18): P. Carlone and A. Astarita. Dissimilar metal welding. Metals, Nov 2019. URL: https://doi.org/10.3390/met9111206, doi:10.3390/met9111206. This article has 23 citations.

5. (carlone2019dissimilarmetalwelding pages 18-19): P. Carlone and A. Astarita. Dissimilar metal welding. Metals, Nov 2019. URL: https://doi.org/10.3390/met9111206, doi:10.3390/met9111206. This article has 23 citations.

6. (davies1993anoteon pages 1-3): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

7. (choi2007agingcharacteristicsand pages 1-2): Joon Hwan Choi and Dong Nyung Lee. Aging characteristics and precipitate analysis of cu–ni–mn–p alloy. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 458:295-302, Jun 2007. URL: https://doi.org/10.1016/j.msea.2006.12.074, doi:10.1016/j.msea.2006.12.074. This article has 33 citations.

8. (ren2024strengtheningmechanismof pages 2-5): Xiaoyan Ren, Zhenghua Shi, Guowei Zhang, Ningning Chen, Yougui Zhang, Zhiming Guo, Jinzhi Hu, and Hong Xu. Strengthening mechanism of sub-nano ni3p and cu3p phases particles on the pb–sn bronze alloy. Heliyon, 10:e34624, Aug 2024. URL: https://doi.org/10.1016/j.heliyon.2024.e34624, doi:10.1016/j.heliyon.2024.e34624. This article has 10 citations.

9. (ren2024strengtheningmechanismof media 0b15dc47): Xiaoyan Ren, Zhenghua Shi, Guowei Zhang, Ningning Chen, Yougui Zhang, Zhiming Guo, Jinzhi Hu, and Hong Xu. Strengthening mechanism of sub-nano ni3p and cu3p phases particles on the pb–sn bronze alloy. Heliyon, 10:e34624, Aug 2024. URL: https://doi.org/10.1016/j.heliyon.2024.e34624, doi:10.1016/j.heliyon.2024.e34624. This article has 10 citations.

10. (ren2024strengtheningmechanismof pages 5-8): Xiaoyan Ren, Zhenghua Shi, Guowei Zhang, Ningning Chen, Yougui Zhang, Zhiming Guo, Jinzhi Hu, and Hong Xu. Strengthening mechanism of sub-nano ni3p and cu3p phases particles on the pb–sn bronze alloy. Heliyon, 10:e34624, Aug 2024. URL: https://doi.org/10.1016/j.heliyon.2024.e34624, doi:10.1016/j.heliyon.2024.e34624. This article has 10 citations.

11. (konynenburg1990backgroundstudiesin pages 142-149): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

12. (davies1993anoteon pages 3-4): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

13. (davies1993anoteon pages 6-8): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

14. (beavers1980corrosionrelatedfailuresin pages 133-137): J. A. Beavers, A. K. Agrawal, and W. E. Berry. Corrosion-related failures in power plant condensers. final report. [pwr]. Unknown journal, Aug 1980. URL: https://doi.org/10.2172/5047866, doi:10.2172/5047866. This article has 6 citations.

15. (lewis1981evaluationofcoppernickel pages 24-26): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

16. (galai2021effectofphosphorus pages 2-4): Mouhsine Galai, Hanane Benqlilou, Mohamed EbnTouhami, Hakima Nassali, Tounsi Belhaj, Khalifa Berrami, Ilyas Mansouri, and Bennaceur ouaki. Effect of phosphorus content of α-brass on its corrosion resistance in aggressive soil: experimental and characterization studies. Euro-Mediterranean Journal for Environmental Integration, Apr 2021. URL: https://doi.org/10.1007/s41207-021-00244-9, doi:10.1007/s41207-021-00244-9. This article has 3 citations.

17. (galai2021effectofphosphorus pages 4-5): Mouhsine Galai, Hanane Benqlilou, Mohamed EbnTouhami, Hakima Nassali, Tounsi Belhaj, Khalifa Berrami, Ilyas Mansouri, and Bennaceur ouaki. Effect of phosphorus content of α-brass on its corrosion resistance in aggressive soil: experimental and characterization studies. Euro-Mediterranean Journal for Environmental Integration, Apr 2021. URL: https://doi.org/10.1007/s41207-021-00244-9, doi:10.1007/s41207-021-00244-9. This article has 3 citations.

18. (galai2021effectofphosphorus pages 5-7): Mouhsine Galai, Hanane Benqlilou, Mohamed EbnTouhami, Hakima Nassali, Tounsi Belhaj, Khalifa Berrami, Ilyas Mansouri, and Bennaceur ouaki. Effect of phosphorus content of α-brass on its corrosion resistance in aggressive soil: experimental and characterization studies. Euro-Mediterranean Journal for Environmental Integration, Apr 2021. URL: https://doi.org/10.1007/s41207-021-00244-9, doi:10.1007/s41207-021-00244-9. This article has 3 citations.

19. (konynenburg1990backgroundstudiesin pages 186-192): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

20. (tumuluru1988weldductilitystudies pages 1-2): M Tumuluru and EF Nippes. Weld ductility studies in a tin-modified copper-nickel alloy. Unknown journal, 1988.

21. (tumuluru1988weldductilitystudies pages 7-8): M Tumuluru and EF Nippes. Weld ductility studies in a tin-modified copper-nickel alloy. Unknown journal, 1988.

22. (tumuluru1988weldductilitystudies pages 5-7): M Tumuluru and EF Nippes. Weld ductility studies in a tin-modified copper-nickel alloy. Unknown journal, 1988.

23. (konynenburg1990backgroundstudiesin pages 136-142): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

24. (schlesinger2002thethermodynamicproperties pages 23-25): Mark E. Schlesinger. The thermodynamic properties of phosphorus and solid binary phosphides. Chemical reviews, 102 11:4267-301, Oct 2002. URL: https://doi.org/10.1021/cr000039m, doi:10.1021/cr000039m. This article has 209 citations and is from a highest quality peer-reviewed journal.

25. (schlesinger2002thethermodynamicproperties media cb6f0e44): Mark E. Schlesinger. The thermodynamic properties of phosphorus and solid binary phosphides. Chemical reviews, 102 11:4267-301, Oct 2002. URL: https://doi.org/10.1021/cr000039m, doi:10.1021/cr000039m. This article has 209 citations and is from a highest quality peer-reviewed journal.

26. (olinger2026criticalmineralsmemory pages 1-2): Danielle A. Olinger. Critical minerals memory match game. General Information Product, Jan 2026. URL: https://doi.org/10.3133/gip266, doi:10.3133/gip266. This article has 0 citations.

27. (olinger2026criticalmineralsmemory pages 2-4): Danielle A. Olinger. Critical minerals memory match game. General Information Product, Jan 2026. URL: https://doi.org/10.3133/gip266, doi:10.3133/gip266. This article has 0 citations.

28. (rupkeUnknownyearutahmining2025 pages 31-31): A Rupke, SE Mills, MD Vanden Berg, and N Christensen. Utah mining 2025. Unknown journal, Unknown year.
