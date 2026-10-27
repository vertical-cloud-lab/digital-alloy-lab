<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 9c720ce8-fc44-4a3b-a2c7-ec2be7d02b2b
- Submitted: 2026-10-17T19:01:09Z
- Fetched: 2026-10-17T19:35:23Z (status: success)
- Raw trajectory JSON: ../raw/el-39-Li.json.gz
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

ELEMENT UNDER REVIEW: Li (deoxidizer). Lithium as a deoxidizer for copper melts; any Cu-Li alloy use; volatility and reactivity with crucibles.

Answer for Li specifically, not for copper alloys in general:
1. ROLE: what Li does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Li ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Li changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Li, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Li, Cu-Ni-Li and Cu-Al-Li are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Li in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Li neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Li | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Li (deoxidizer). Lithium as a deoxidizer for copper melts; any Cu-Li alloy use; volatility and reactivity with crucibles.

Answer for Li specifically, not for copper alloys in general:
1. ROLE: what Li does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Li ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Li changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Li, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Li, Cu-Ni-Li and Cu-Al-Li are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Li in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Li neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Li | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Lithium (Li): decision for copper-alloy DED powder

**Decision: LIMIT Li as an incidental impurity; do not make it a composition-search variable.** [CITE] Lithium demonstrably deoxidizes molten copper, but the reported concentrations are *additions to the melt*, not measured Li retained in powder or deposited metal. No retrieved study establishes a Li concentration that improves the seawater corrosion of a Cu-rich alloy, survives the specified atomization and laser process, or improves a repair interface. One copper-melting study explicitly cautions that Li could decrease corrosion resistance. A **provisional screening target of ≤0.005 wt% Li (50 ppm) in both powder and deposit** is therefore proposed to keep residual Li below the smallest clearly reported experimental Li charge; it is **not** an ASTM, AWS, MIL, UNS or experimentally validated corrosion limit. Specify analytical verification rather than interpreting the target as a qualified acceptance criterion. (shatagin2008electricmeltingand pages 1-2, shatagin2008electricmeltingand pages 2-4, rzadkosz2014researchontechnology media 1de8aa6e)

## 1. Role and alloy precedent

[CITE] [NUMBERS] In a copper-casting experiment, **0.05 wt% Li charged** was associated with **39 ppm oxygen** and reported conductivity **54 MS/m**; untreated comparison melts contained **1,290 and 2,260 ppm oxygen**. This demonstrates deoxidation under those casting conditions, **not** that the finished copper contained 0.05 wt% Li or that an identically prepared untreated melt would lose a calculable percentage of its oxygen. Rzadkosz *et al.*, “Research on Technology of Alloyed Copper Casting,” *Archives of Foundry Engineering* **14** (2014) 79–84, doi:**10.2478/afe-2014-0041**; the cropped original Table 1 confirms the entries. (rzadkosz2014researchontechnology pages 1-2, rzadkosz2014researchontechnology media 1de8aa6e)

[CITE] [NUMBERS] Shatagin *et al.* used a **50:50 Li–Ca deoxidizer at 0.09–0.18 kg per metric ton Cu**: **0.0045–0.009 wt% Li charged**, calculated from their deoxidizer specification. They report dense conductor-copper castings after this treatment **and argon processing**; neither an independently isolated Li effect nor retained Li is measured. Their proposed reaction, **2Li + 2Cu₂O + H₂ → 4Cu + 2LiOH**, concerns removal of oxygen and hydrogen; Li-bearing oxides/hydroxides must separate rather than remain as inclusions. The authors explicitly note a *possible decrease* in copper’s corrosion resistance, without reporting a seawater experiment. Shatagin, Zhurilo and Zhurilo, “Electric Melting and Stable Continuous Casting of Secondary Copper,” *Russian Metallurgy (Metally)* **2008** (2008) 662–666, doi:**10.1134/S0036029508080041**. A review also describes Li as a degasifier for high-conductivity copper and **Cu–Sn bronze**; it supplies no retained composition or marine qualification: Kavanagh *et al.*, *Resources* **7** (2018) 57, doi:**10.3390/resources7030057**. (shatagin2008electricmeltingand pages 1-2, shatagin2008electricmeltingand pages 2-4, kavanagh2018globallithiumsources—industrial pages 13-15)

[SPEC] [GAP] **No verified Li-bearing range** was found for marine Cu–Ni (including C71500), C95800 NAB, Mn–Al bronze, gunmetal, brass, Cu–Ni–Sn, Cu–Ni–Si, or the cited repair fillers **ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl**. Do not turn the absence of a specified Li range into an assertion that every edition prohibits trace Li. In particular, the retrieved material does **not** establish a numerical Li maximum in **ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449 or UNS/CDA**; obtain the controlling edition before calling any ppm target a specification limit. No evidence identifies Li-derived precipitates, grain-refining particles, seawater-protective film chemistry or dealloying inhibition in those alloy families. A calculated growth-restriction ranking in a copper-grain-refinement thesis places Li high, but its reported validation melts added **other elements, not Li**; that ranking does not demonstrate Li grain refinement. Cziegler, *Aspects of Grain Refinement in Copper Alloys*, University of Leoben MSc thesis (2015), DOI **not established**. (cziegler2015aspectsofgrain pages 1-6, kavanagh2018globallithiumsources—industrial pages 13-15)

## 2. Seawater corrosion

[GAP] **No defensible beneficial or harmful Li interval in wt%, corrosion-rate change, ΔE*corr*, impedance/film resistance, pitting or crevice potential, selective-attack depth, erosion–corrosion change or velocity limit** was found for Li-added copper-rich alloys in natural seawater, ASTM D1141 substitute ocean water or 3.5 wt% NaCl. Thus **neither a range where Li helps nor one where it harms can be numerically assigned**. The caution about possibly reduced corrosion resistance above is qualitative and unaccompanied by a test. A Li-rich *surface* observed on Cu–Li in fusion-vacuum experiments is **not** evidence of a stable chloride-resistant oxide film in immersed copper alloy. For context only—not a Li effect—Lewis and LaQue report marine Cu–Ni C70600 resistance at seawater flow rates up to **3.0 m/s**: “Evaluation of Copper-Nickel Alloys for OTEC Applications,” report (1981), doi:**10.2172/6255887**. (shatagin2008electricmeltingand pages 1-2, schorn1989thesuitabilityof pages 2-3, schorn1989thesuitabilityof pages 1-2)

## 3. DED, welding and substrate dilution

[GAP] No retrieved **Cu-rich Li-bearing** laser-DED or welding experiment quantifies solidification or reheating-layer liquation cracking, pore fraction, Li loss, or corrosion after deposition on **cast C95800 or wrought C71500**. The cited filler designations cannot supply a Li-dependent effect when Li is not verified in their compositions. Casting evidence supports a *plausible* reduction of oxygen-/hydrogen-related pores if Li is added before melting and its reaction products are removed. Conversely, Li oxidation products or retained LiOH inclusions, composition loss and reheating of segregated zones are **risks to test**, not demonstrated Li-specific crack mechanisms in NAB or Cu–Ni DED. Dilution could further reduce an already unmeasured residual Li concentration; predicting a useful gradient, beneficial interface reaction or a Li-induced liquation threshold would be speculative. Al-base **Al–Cu–Li** laser-welding observations must not be transferred to Cu-base deposits. (rzadkosz2014researchontechnology pages 2-3, shatagin2008electricmeltingand pages 1-2, shatagin2008electricmeltingand pages 2-4)

## 4. Melt, powder and sonotrode

[CITE] [NUMBERS] Direct evidence that Li can leave **Cu-rich Cu–Li** exists, but from a *different* environment: a cast alloy nominally **17 at% Li ≈ 2.19 wt% Li** lost Li by evaporation from its surface above approximately **300 °C** in vacuum; the authors report approximately **20 mg Li per day per cm² at 450 °C**. This is not an atomization-loss coefficient for a dilute melt at 1,200 °C. Schorn *et al.*, “The Suitability of Copper/Lithium Alloys for Application as Wall Material in Tokamaks,” *Journal of Nuclear Materials* **162–164** (1989) 924–931, doi:**10.1016/0022-3115(89)90387-5**. Another group reported little Li loss during repeated arc melting of alloys containing up to approximately **15 at% Li ≈ 1.90 wt%**, so loss clearly depends on activity and processing conditions; Brooks *et al.*, *Fusion Technology* **8** (1985) 1275–1280, doi:**10.13182/FST85-A39943**. **Neither experiment resolves loss in argon-shielded ultrasonic atomization or infrared-laser DED.** (schorn1989thesuitabilityof pages 5-6, brooks1985currentstateof pages 2-3)

[GAP] Li is oxygen- and moisture-reactive; powder oxidation, variable retained Li between melt/powder/deposit, fume, slag and inclusion carryover therefore warrant monitoring. No relevant quantitative test establishes **trace Li in Cu melt at approximately 1,200 °C** reacting with an **Al₂O₃ or ZrO₂ crucible, graphite, or a Ti-alloy versus Mo ultrasonic sonotrode**. A separate review calls **graphite incompatible with *liquid lithium*** and reports Mo-alloy compatibility below **1,100 °C**; these refer to a *pure-Li coolant*, not dilute Cu–Li contact at the proposed processing temperature. Do not treat that comparison as proof of either crucible failure or sonotrode safety. No measured Li-dependent surface-tension or atomization-yield coefficient was verified. Farmer, *Survey of Materials for Fusion–Fission Hybrid Reactors*, UCRL-TR-232463 (2007), doi:**10.2172/1124815**. (shatagin2008electricmeltingand pages 1-2, schorn1989thesuitabilityof pages 5-6, farmer2007surveyofmaterials pages 23-26)

## 5. Phase relations and computational coverage

[CITE] [NUMBERS] Okamoto’s summary of the **Gąsior *et al.* assessed binary Cu–Li diagram** tabulates the Cu-rich fcc phase to **18.3 at% Li ≈ 2.39 wt% Li**. The table **does not state the temperature at which that maximum occurs**; it must not be reported as room-temperature solubility. It depicts elemental copper melting at **1,084.87 °C**, a **480 °C** feature, and a proposed **Cu₂Li₃** phase at **60 at% Li ≈ 14.1 wt% Li**. Those diagram labels do not by themselves establish the identity, composition and temperature of a Cu-rich invariant reaction. Okamoto, “Cu–Li (Copper–Lithium),” *Journal of Phase Equilibria and Diffusion* **32** (2011) 172, doi:**10.1007/s11669-010-9840-3**; underpinning assessment: Gąsior *et al.*, “Thermodynamic Evaluation of Cu–Li Phase Diagram from EMF Measurements and DTA Study,” *CALPHAD* **33** (2009) 215–220, doi:**10.1016/j.calphad.2008.10.006** (underlying article not obtained). (okamoto2011culi(copperlithium) pages 1-1)

[CITE] **Intermediate phases are contested.** The older Cu–Li diagram showed none; the assessed diagram proposes Cu₂Li₃ from EMF; subsequent powder-XRD work cited by Yu *et al.* could not confirm it and challenged the historical **Cu₄Li** assignment. Yu *et al.* instead *predict*, by zero-temperature first-principles searches, **Cu₇Li, Cu₂Li and CuLi₂**; these are not experimentally established precipitates in dilute as-deposited marine copper. Yu *et al.*, “Prediction of Stable Cu–Li Binary Intermetallics from First-Principles Calculations,” *Journal of Alloys and Compounds* **766** (2018) 640–648, doi:**10.1016/j.jallcom.2018.07.020**. (okamoto2011culi(copperlithium) pages 1-1, yu2018predictionofstable pages 1-7, yu2018predictionofstable pages 7-12)

[GAP] A **published binary assessment exists**, but no retrieved documentation establishes usable **Li-containing Cu–Li, Cu–Ni–Li or Cu–Al–Li parameters in TCCU or COST 531**. In Thermo-Calc, check the licensed database’s component list, assessed systems and phase models before accepting a calculation; importing a binary TDB into pycalphad would **not** validate missing ternaries. The assessed Cu-rich binary starts at **1,084.87 °C** and does not itself substantiate a Li-induced crossing of **1,250 °C** at trace Li. More importantly, it cannot certify that a **Ni-/Al-/Fe-/Mn-bearing base alloy** remains below the atomizer’s liquidus/superheat limit: calculate and experimentally check that *entire* composition. (nassar2025methodologyandtechnical pages 9-10, okamoto2011culi(copperlithium) pages 1-1)

## 6. Supply, safety and joint constraints

[CITE] [NAVY] Li is a U.S. critical mineral under the **2022** designation; the 2025 USGS technical input recommended adding **copper** to the 2025 list. A secondary account of the **final 2025** list identifies copper as added. The *technical-input report is not itself the final legal notice*; cite the final Federal Register notice when specifying legal effective status. Nassar *et al.*, USGS Open-File Report **2025–1047**, doi:**10.3133/ofr20251047**. No substantiated, dated **price per kg of elemental lithium metal** was retrieved; carbonate or battery prices would be an invalid substitute. (nassar2025methodologyandtechnical pages 9-10, nassar2025methodologyandtechnical pages 33-35, staff2022usgsminingreviewa pages 6-9)

[GAP] **Safety:** control oxygen/moisture during pure-metal charging and powder handling; assess combustible fine-powder dust, reactive Li-bearing fines, local exhaust and Li-containing laser fume. Soluble reaction products and occupational exposure require assessment even if a dilute, consolidated Cu–Li alloy is not equivalent to handling pure Li metal. No verified **Li-specific OSHA PEL**, **RoHS/REACH compositional ban**, or **Navy prohibition** on Li in these alloys was established by the retrieved sources; none should be invented. No validated toxicity threshold for *this powder* follows from lithium-medication or Li-ion-battery studies. (shatagin2008electricmeltingand pages 1-2, farmer2007surveyofmaterials pages 23-26)

**[NUMBERS] Joint-constraint notes.** Budget oxygen consumption using **2Li + O → Li₂O**: approximately **0.868 wt% Li charged per 1 wt% oxygen removed**, *if* all Li participates and the oxide separates; equivalently, **0.005 wt% Li** can stoichiometrically bind only approximately **0.0058 wt% oxygen (58 ppm)**. This is a mass-balance ceiling, **not** a demonstrated functional floor or permission to retain Li. Account also for moisture/hydrogen consumption and losses to slag/fume. No defensible required **Li/Ni, Li/Fe, Li/Mn or Li/Al** ratio, or demonstrated neutralization of an intermetallic or selective-corrosion phase, is available. For repair, separately calculate substrate dilution and base-alloy liquidus; monitor *measured residual Li* alongside oxygen and hydrogen rather than using charged Li as the composition coordinate. (rzadkosz2014researchontechnology pages 2-3, shatagin2008electricmeltingand pages 1-2, shatagin2008electricmeltingand pages 2-4)

**Bounds and evidence quality.** [NUMBERS] For **both Cu–Ni and Al-bronze**, conservative designed-addition maximum = **NA**, aggressive maximum = **NA**, and demonstrated retained-Li functional floor = **NA**: the measured *charge* examples (**0.0045–0.009** and **0.05 wt% Li**) establish a deoxidation route, not a qualified retained-alloy interval. Proposed **impurity maximum = 0.005 wt% Li in powder and deposit**, a **precautionary project control, not a specification-derived maximum**. Its failure modes are uncertain retention/evaporation, potential oxide or hydroxide inclusions, unquantified DED weld integrity, and completely unverified as-deposited marine corrosion. Direct evidence for the application-specific limit is therefore **thin**; if a specification-based limit is required, the only honest entry is **NA pending verification of the controlling specification**. (rzadkosz2014researchontechnology pages 1-2, shatagin2008electricmeltingand pages 1-2, shatagin2008electricmeltingand pages 2-4, schorn1989thesuitabilityof pages 5-6, rzadkosz2014researchontechnology media 1de8aa6e)

VERDICT | Li | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.005 | evidence=thin

References

1. (shatagin2008electricmeltingand pages 1-2): O. A. Shatagin, A. G. Zhurilo, and D. Yu. Zhurilo. Electric melting and stable continuous casting of secondary copper. Russian Metallurgy (Metally), 2008:662-666, Dec 2008. URL: https://doi.org/10.1134/s0036029508080041, doi:10.1134/s0036029508080041. This article has 1 citations.

2. (shatagin2008electricmeltingand pages 2-4): O. A. Shatagin, A. G. Zhurilo, and D. Yu. Zhurilo. Electric melting and stable continuous casting of secondary copper. Russian Metallurgy (Metally), 2008:662-666, Dec 2008. URL: https://doi.org/10.1134/s0036029508080041, doi:10.1134/s0036029508080041. This article has 1 citations.

3. (rzadkosz2014researchontechnology media 1de8aa6e): St. Rzadkosz, M. Kranc, A. Garbacz-Klempka, M. Piękoś, J. Kozana, and W. Cieślak. Research on technology of alloyed copper casting. Archives of Foundry Engineering, 14:79-84, Jun 2014. URL: https://doi.org/10.2478/afe-2014-0041, doi:10.2478/afe-2014-0041. This article has 11 citations.

4. (rzadkosz2014researchontechnology pages 1-2): St. Rzadkosz, M. Kranc, A. Garbacz-Klempka, M. Piękoś, J. Kozana, and W. Cieślak. Research on technology of alloyed copper casting. Archives of Foundry Engineering, 14:79-84, Jun 2014. URL: https://doi.org/10.2478/afe-2014-0041, doi:10.2478/afe-2014-0041. This article has 11 citations.

5. (kavanagh2018globallithiumsources—industrial pages 13-15): Laurence Kavanagh, Jerome Keohane, Guiomar Garcia Cabellos, Andrew Lloyd, and John Cleary. Global lithium sources—industrial use and future in the electric vehicle industry: a review. Resources, 7:57, Sep 2018. URL: https://doi.org/10.3390/resources7030057, doi:10.3390/resources7030057. This article has 505 citations.

6. (cziegler2015aspectsofgrain pages 1-6): A Cziegler. Aspects of grain refinement in copper alloys. Unknown journal, 2015.

7. (schorn1989thesuitabilityof pages 2-3): R.P. Schorn, E. Hintz, B. Baretzky, J. Bohdansky, W. Eckstein, J. Roth, and E. Taglauer. The suitability of copper/lithium alloys for application as wall material in tokamaks. Journal of Nuclear Materials, pages 924-931, Apr 1989. URL: https://doi.org/10.1016/0022-3115(89)90387-5, doi:10.1016/0022-3115(89)90387-5. This article has 10 citations and is from a domain leading peer-reviewed journal.

8. (schorn1989thesuitabilityof pages 1-2): R.P. Schorn, E. Hintz, B. Baretzky, J. Bohdansky, W. Eckstein, J. Roth, and E. Taglauer. The suitability of copper/lithium alloys for application as wall material in tokamaks. Journal of Nuclear Materials, pages 924-931, Apr 1989. URL: https://doi.org/10.1016/0022-3115(89)90387-5, doi:10.1016/0022-3115(89)90387-5. This article has 10 citations and is from a domain leading peer-reviewed journal.

9. (rzadkosz2014researchontechnology pages 2-3): St. Rzadkosz, M. Kranc, A. Garbacz-Klempka, M. Piękoś, J. Kozana, and W. Cieślak. Research on technology of alloyed copper casting. Archives of Foundry Engineering, 14:79-84, Jun 2014. URL: https://doi.org/10.2478/afe-2014-0041, doi:10.2478/afe-2014-0041. This article has 11 citations.

10. (schorn1989thesuitabilityof pages 5-6): R.P. Schorn, E. Hintz, B. Baretzky, J. Bohdansky, W. Eckstein, J. Roth, and E. Taglauer. The suitability of copper/lithium alloys for application as wall material in tokamaks. Journal of Nuclear Materials, pages 924-931, Apr 1989. URL: https://doi.org/10.1016/0022-3115(89)90387-5, doi:10.1016/0022-3115(89)90387-5. This article has 10 citations and is from a domain leading peer-reviewed journal.

11. (brooks1985currentstateof pages 2-3): J. N. Brooks, D. M. Gruen, A. R. Krauss, R. F. Mattas, and A. B. DeWald. Current state of development and expected performance of copper-lithium alloys as an impurity control system in fusion applications. Fusion Technology, 8:1275-1280, Jul 1985. URL: https://doi.org/10.13182/fst85-a39943, doi:10.13182/fst85-a39943. This article has 4 citations.

12. (farmer2007surveyofmaterials pages 23-26): Joseph Farmer. Survey of materials for fusion fission hybrid reactors vol 1 rev. 0. ArXiv, Jul 2007. URL: https://doi.org/10.2172/1124815, doi:10.2172/1124815. This article has 0 citations.

13. (okamoto2011culi(copperlithium) pages 1-1): H. Okamoto. Cu-li (copper-lithium). Journal of Phase Equilibria and Diffusion, 32:172, Jan 2011. URL: https://doi.org/10.1007/s11669-010-9840-3, doi:10.1007/s11669-010-9840-3. This article has 39 citations and is from a peer-reviewed journal.

14. (yu2018predictionofstable pages 1-7): Jiahui Yu, Dawei Zhou, Chunying Pu, Xin Tang, and Feiwu Zhang. Prediction of stable cu-li binary intermetallics from first-principles calculations: stoichiometries, crystal structures, and physical properties. Journal of Alloys and Compounds, 766:640-648, Oct 2018. URL: https://doi.org/10.1016/j.jallcom.2018.07.020, doi:10.1016/j.jallcom.2018.07.020. This article has 15 citations and is from a peer-reviewed journal.

15. (yu2018predictionofstable pages 7-12): Jiahui Yu, Dawei Zhou, Chunying Pu, Xin Tang, and Feiwu Zhang. Prediction of stable cu-li binary intermetallics from first-principles calculations: stoichiometries, crystal structures, and physical properties. Journal of Alloys and Compounds, 766:640-648, Oct 2018. URL: https://doi.org/10.1016/j.jallcom.2018.07.020, doi:10.1016/j.jallcom.2018.07.020. This article has 15 citations and is from a peer-reviewed journal.

16. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

17. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

18. (staff2022usgsminingreviewa pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.
