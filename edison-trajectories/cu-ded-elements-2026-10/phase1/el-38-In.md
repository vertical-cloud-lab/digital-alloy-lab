<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 37e1f94f-6c6e-4d43-b7a3-953a8e95ff25
- Submitted: 2026-10-17T19:01:06Z
- Fetched: 2026-10-17T19:30:55Z (status: success)
- Raw trajectory JSON: ../raw/el-38-In.json.gz
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

ELEMENT UNDER REVIEW: In (solid solution). Cu-In and Cu-Ni-In; indium is a US critical mineral; any corrosion or dealloying data in chloride.

Answer for In specifically, not for copper alloys in general:
1. ROLE: what In does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their In ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how In changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-In, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-In, Cu-Ni-In and Cu-Al-In are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of In in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that In neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | In | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: In (solid solution). Cu-In and Cu-Ni-In; indium is a US critical mineral; any corrosion or dealloying data in chloride.

Answer for In specifically, not for copper alloys in general:
1. ROLE: what In does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their In ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how In changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-In, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-In, Cu-Ni-In and Cu-Al-In are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of In in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that In neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | In | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Indium (In) for pre-alloyed marine-copper DED powder

**Decision: LIMIT In to an incidental impurity; do not include it as a designed composition variable.** The Cu–In phase diagram establishes substantial *high-temperature binary* solubility, and a dilute Cu–In experiment establishes strong surface segregation. Neither establishes seawater protection. I found no qualifying comparison of In-bearing, copper-rich deposits against as-deposited C71500, nor an In-containing marine-copper filler with a demonstrated DED processing window. The principal concern is untested enrichment of In in the last liquid to solidify and at subsequently reheated interfaces—not a demonstrated In-induced weld crack. The proposed **0.01 wt% In maximum** below is a *project procurement and reporting rule*, **not** a published metallurgical tolerance or specification limit. (liu2002thermodynamicassessmentof pages 1-2, madito2012thesegregationof pages 1-15, cziegler2015aspectsofgrain pages 57-64, davies1993anoteon pages 1-3)

## 1. Role and commercial precedent

[CITE][NUMBERS] In substitutes into copper-rich fcc solid solution. In an experiment on dilute, polycrystalline Cu–In, **0.059 atomic% In, equivalent to approximately 0.107 wt% In**, produced approximately **16–25% In coverage of the analyzed surface atomic layer** during heating at **460–580 °C in ultrahigh vacuum**. This is evidence of *surface enrichment*, not evidence of an In₂O₃ film protecting an alloy in seawater. The same experiment found that segregating sulfur eventually displaced surface In; it does **not** demonstrate sulfur neutralization or grain-boundary strengthening. Madito, *The Segregation of Indium from Polycrystalline Copper Crystals*, University of the Free State MSc thesis (2012; no DOI identified). (madito2012thesegregationof pages 1-15, madito2012thesegregationof pages 69-77)

[GAP] I found **no verified commercial or Navy Cu–Ni, aluminum-bronze/NAB, Mn–Al-bronze, tin-bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si composition specifying a deliberate In range in wt%**. Specifically, no In range was established here from ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449, or a UNS/CDA marine-copper designation. Their familiar Ni, Al, Fe, Mn, Sn and other constituents must **not** be mistaken for evidence that they contain In. A silver brazing alloy *used to join* aluminum bronze, manganese bronze and other copper alloys likewise does not make In an alloying constituent of those base metals: Dev and Sivaramakrishnan’s tested BAg-1 was Ag–Cu–Zn–Cd, **without In**. *Materials & Design* **17** (1996), 75–78, doi:**10.1016/S0261-3069(96)00035-0**. (dev1996anindigenoustechnology pages 1-2, dev1996anindigenoustechnology pages 2-4)

[CITE][GAP] Deoxidation, grain refinement, an In-bearing protective marine film, and suppression of selective dissolution are **unproven In-specific functions** in the target alloys. Particularly important: Davies did **not** measure beneficial In inhibition of brass dezincification. He recommended *future* tests of bismuth-bearing brasses with and without In. D. D. Davies, *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions*, Copper Development Association report 7013-0009 (1993; no DOI identified). This recommendation cannot be converted into a beneficial In dose. (davies1993anoteon pages 6-8, davies1993anoteon pages 1-3)

## 2. Chloride and seawater corrosion

[GAP] For **bulk copper-rich alloys with controlled In additions**, I found no defensible In-dependent numerical corrosion rates, open-circuit or corrosion-potential shifts, polarization or film resistances, pitting/crevice potentials, 30-day selective-attack depths, erosion-corrosion rates, or seawater velocity limits in natural seawater, ASTM D1141 water, or **3.5 wt% NaCl**. Accordingly, the experimentally supported ranges where In **helps** or **harms** the specified marine deposits are both **unknown**. Neither a corrosion-resistant In-containing solder nor an In-activated *aluminum sacrificial anode* would establish protection of an as-deposited Cu–Ni or NAB repair. Davies’s proposed brass experiment provides no missing numerical result. (davies1993anoteon pages 6-8, dev1996anindigenoustechnology pages 1-2, dev1996anindigenoustechnology pages 2-4)

## 3. DED, welding and repair interfaces

[CITE][NUMBERS] A diagram-derived Cu–In solidification estimate gives **partition coefficient k ≈ 0.48**, **Cu-rich liquidus slope ≈ −6.12 °C per wt% In**, and growth-restriction parameter **Q/c₀ ≈ 3.18 °C per wt% In**. These estimates imply rejection into remaining liquid; they are **not** measurements of DED cracks or grain refinement by In. A. Cziegler, *Aspects of Grain Refinement in Copper Alloys*, thesis (2015; no DOI identified). (cziegler2015aspectsofgrain pages 57-64)

[GAP] There is no retrieved In-controlled single-stream, infrared-laser Cu-alloy DED study establishing a safe In concentration for solidification cracking, reheated-layer liquation cracking, porosity, spatter, oxidation/evaporation loss, or as-deposited corrosion. No In-containing **ERCuNi, ERCuAl-A2, ERCuNiAl or ERCuMnNiAl** comparison was verified; therefore welding-filler success cannot be claimed as a demonstrated In benefit. During repair, dilution into cast C95800 and wrought Cu–Ni must be treated as **separate experimental conditions**: dilution changes the Ni–Al–Fe–Mn balance as well as local In concentration. For either substrate, an In-rich interdendritic constituent or remelting-related liquation is a *plausible phase-diagram-based failure hypothesis*, not an observed defect or an established concentration threshold. (liu2002thermodynamicassessmentof pages 2-4, liu2002thermodynamicassessmentof pages 4-6, cziegler2015aspectsofgrain pages 57-64)

## 4. Induction melting and ultrasonic atomization

[CITE][GAP] In melts at about **156.6 °C**, far below a molten Cu charge; charge addition, dissolution and retention should therefore be checked by measuring *charge, atomized powder and deposited metal separately*. An In-on-Cu diffusion experiment deliberately covered its In with Cu and increased temperature stepwise to avoid melting/evaporation during preparation; that procedure **does not quantify** In loss from an argon-shielded, approximately **1,200–1,300 °C** induction melt or a laser pool. Madito (2012). (madito2012thesegregationof pages 1-15, madito2012thesegregationof pages 15-23)

[GAP] I found no applicable measured In-dependent oxidation or evaporation loss, droplet surface tension, atomization yield, or reaction rate with **alumina, zirconia, graphite, a Ti-alloy sonotrode, or a Mo sonotrode** for this process. In-containing oxides and crucible/sonotrode pickup merit analysis, but claiming that In is an effective melt deoxidizer or that a named crucible is incompatible would overstate the evidence. The binary Cu-rich **negative liquidus slope** points toward *lowering*, rather than raising, the liquidus with a small In addition; the full Ni–Al–Fe–Mn-containing powder still requires a qualified multicomponent calculation or thermal measurement before concluding that it meets the **approximately 1,200–1,250 °C useful-superheat ceiling**. (cziegler2015aspectsofgrain pages 57-64)

## 5. Phase diagram and usable CALPHAD coverage

[CITE][NUMBERS] Liu *et al.*, “Thermodynamic Assessment of the Cu–In Binary System,” *Journal of Phase Equilibria* **23** (2002), 409–415, doi:**10.1361/105497102770331352**, calculated the Cu-rich **L + fcc(Cu) → intermediate-phase peritectic at 978 K (705 °C)**. Its fcc phase contains **9.4 atomic% In = approximately 15.8 wt% In**; the corresponding calculated liquid contains **21.1 atomic% In = approximately 32.6 wt% In**. Reported experimental peritectic temperatures were **983 and 988 K**. Thus, approximately **15.8 wt% In near 705 °C** is a *binary, high-temperature maximum fcc-solubility estimate*, emphatically **not** an allowable DED or seawater bound. Their calculated Cu-rich eutectoid is **844 K (571 °C)** with fcc containing **9.2 atomic% In ≈ 15.5 wt% In**. The authors acknowledge deviations between assessed and experimental fcc solvi. (liu2002thermodynamicassessmentof pages 1-2, liu2002thermodynamicassessmentof pages 4-6)

[CITE] The assessed binary includes Cu–In intermediate phases near **Cu₉In₄/Cu₇In₃**, a higher-In phase near **Cu₂In**, and **Cu₁₁In₉**; reported **CuIn₂** from thin films was treated as metastable rather than included as an equilibrium bulk phase. A Cu–In–Sn phase compilation also reports these Cu–In-related structures; its ternary assessments cannot be substituted for Cu–Ni–In or Cu–Al–In. Liu *et al.* (2002), doi:**10.1361/105497102770331352**; MSIT, “Cu–In–Sn,” *Landolt-Börnstein* (2007), doi:**10.1007/978-3-540-47004-5_26**. (liu2002thermodynamicassessmentof pages 1-2, liu2002thermodynamicassessmentof pages 2-4, http2007cuinsn(copperindiumtin) pages 6-9)

[CITE][GAP] A documented **2022, 32-element TCCU/MOBCU framework omits In**. Consequently its Cu–In binary assessment and Cu–Ni–In/Cu–Al–In predictions cannot simply be assumed available for Thermo-Calc/TCCU or exported to pycalphad. I did **not** verify a usable Cu–Ni–In or Cu–Al–In assessment in COST 531 or a published TDB, nor rule out a later licensed database release; inspect the installed version, constituent lists and actual interaction parameters before claiming coverage. Jansson *et al.*, “Phase Transformations and Kinetic Simulations of Cu-based Alloys,” *Copper Alloys 2022* proceedings (DOI not identified). (janssonUnknownyearphasetransformationsand pages 26-28)

The table separates numerical phase evidence from the missing application evidence. (davies1993anoteon pages 6-8, liu2002thermodynamicassessmentof pages 4-6, madito2012thesegregationof pages 1-15, cziegler2015aspectsofgrain pages 57-64)

| Evidence tier | Finding | Quantitative result | Interpretation for alloy bounds | Source |
|---|---|---|---|---|
| Binary equilibrium assessment | Cu-rich peritectic, liquid + fcc(Cu) → intermediate phase | 978 K (705 °C); fcc(Cu) = 9.4 at.% In = **15.78 wt.% In**; liquid = 21.1 at.% In ≈ **32.57 wt.% In** | CALPHAD equilibrium/phase-boundary evidence, **not** a corrosion, weldability, or safe-design bound | Liu et al. (2002) (liu2002thermodynamicassessmentof pages 4-6) |
| Binary equilibrium assessment | Cu-rich eutectoid involving fcc(Cu) | 844 K (571 °C); fcc(Cu) = 9.2 at.% In ≈ **15.49 wt.% In** | Confirms large high-temperature binary solubility but does not establish retention in multicomponent Cu–Ni–Al–Fe alloys or suitability for DED | Liu et al. (2002) (liu2002thermodynamicassessmentof pages 4-6) |
| Diagram-derived solidification estimate | Cu–In partitioning and growth-restriction parameters | Partition coefficient **k = 0.48**; liquidus slope **m = −6.12 K/(wt.% In)**; **Q/c₀ = 3.18 K/(wt.% In)** | Predicts moderate rejection of In to interdendritic liquid; estimates came from printed binary diagrams, not direct In-bearing DED experiments | Cziegler (2015) (cziegler2015aspectsofgrain pages 57-64) |
| Direct dilute-alloy experiment | Surface segregation from polycrystalline Cu–In under UHV | Bulk **0.059 at.% In = 0.1065 wt.% In**; surface coverage approximately **16–25% of the analyzed atomic layer** at **460–580 °C** | Demonstrates strong surface enrichment at only ~0.1 wt.% bulk In; experiment was under UHV and provides **no chloride-corrosion result** | Madito (2012) (madito2012thesegregationof pages 1-15, madito2012thesegregationof pages 64-69, madito2012thesegregationof pages 69-77) |
| Direct marine/application evidence | Cu-rich Cu–In electrochemistry and standardized marine-alloy In range | **Absent:** no quantitative Cu–In result found for natural/substitute seawater or 3.5 wt.% NaCl, and no numeric In range verified in the cited marine Cu-alloy or AWS filler specifications | No evidence-based functional floor, beneficial range, commercial upper bound, or specification-derived impurity maximum can be assigned; proposed brass work explicitly called for future testing rather than reporting an In benefit | Targeted evidence review; Davies (1993) (davies1993anoteon pages 6-8) |


*Table: The strongest numerical evidence concerns binary Cu–In equilibrium and surface segregation, not marine corrosion or DED performance. It therefore supports risk identification but not a designed-addition bound.*

## 6. Supply, cost, regulation and worker safety

[CITE][NAVY] In is a U.S. critical mineral in the **2022 list** and remains relevant to the **2025 list**; the cited USGS *technical recommendation*, rather than the final Federal Register notice, explicitly recommends **adding copper** in 2025. Do not confuse a recommended addition with independent verification of final-list wording. Nassar *et al.*, USGS *Open-File Report* **2025-1047**, doi:**10.3133/ofr20251047**. (nassar2025methodologyandtechnical pages 9-10)

[NUMBERS] An identified indium-market source quotes approximately **US$699/kg on 1 January 2025**; this is a dated market indication, **not** a current quote for certified, atomization-grade metal. At that price, **0.01 wt% In** corresponds to about **US$0.07 per kg of alloy**, and **0.10 wt%** to **US$0.70 per kg**, excluding losses and processing. The same source estimates China at about **70% of global output** but also supplies internally inconsistent production figures; use its price and concentration only as approximate planning values. K. Younas, *Indium Recovery from Waste Liquid Crystal Displays* (2026 thesis; DOI not identified). (younas2026indiumrecoveryfrom pages 18-23)

[CITE][NUMBERS] Inhaled In-containing particulate is a substantive powder/fume concern. A study of **57 indium-ingot workers and 63 controls** reported workplace airborne In of **78.4 µg/m³**, associated with lung-injury/inflammation biomarkers; animal responses differed between soluble salts and poorly soluble In₂O₃/ITO. Liu *et al.*, *Particle and Fibre Toxicology* **19** (2022), 69, doi:**10.1186/s12989-022-00510-w**. Occupational reports document pulmonary alveolar proteinosis, fibrosis and emphysema after exposure to indium compounds; **the same incidence cannot be assigned to Cu–In powder or laser fume without exposure characterization**. Chonan *et al.*, *Tohoku Journal of Experimental Medicine* **248** (2019), 143–150, doi:**10.1620/tjem.248.143**. Capture DED fumes locally; contain atomizer/powder transfers; assess respirable particle size and In on filters; and apply the facility’s metal-powder fire controls. (kim2021assessmentofoccupational pages 1-2, liu2022pulmonaryeffectsof pages 1-2, chonan2019indiumlungdiscovery pages 1-2)

[NUMBERS][GAP] One study quotes an **ACGIH respirable-indium TLV of 0.0001 mg/m³** and distinguishes it from Korean limits. This is **not an OSHA permissible exposure limit** and is not an alloy-composition maximum. I did not verify a current, In-specific OSHA PEL, an applicable RoHS/REACH prohibition on metallic In in these alloys, or a Navy-specific In restriction; none should be invented. Kim *et al.*, *Biomolecules* **11** (2021), 419, doi:**10.3390/biom11030419**. (kim2021assessmentofoccupational pages 1-2)

## 7. Bounds and decision rule

**LIMIT, for both Cu–Ni and aluminum-bronze/NAB candidate families.** Set **In ≤ 0.01 wt% (≤100 ppm by mass)** in *powder and deposit* as a **provisional, self-imposed procurement/ICP-screening criterion**; require no intentional In charge. This is **not** a claim that 0.011 wt% cracks, 0.010 wt% is corrosion-neutral, or that ASTM/AWS/MIL specifies 100 ppm In. No retrieved standard or experiment establishes an In-specific *maximum tolerable* impurity concentration; scientifically, that threshold is **undetermined**. The 0.01 wt% operational cap keeps adventitious In substantially below the approximately **0.107 wt%** at which surface segregation was directly studied, while limiting an uncalibrated model dimension and avoiding an unevaluated critical-mineral addition. The failure mode setting the *policy*, rather than a measured limit, is uncontrolled interfacial/last-liquid enrichment coupled to unknown as-deposited chloride behavior. For a genuinely specification-derived impurity maximum, **NA** is the honest answer. (madito2012thesegregationof pages 1-15, madito2012thesegregationof pages 69-77, cziegler2015aspectsofgrain pages 57-64, janssonUnknownyearphasetransformationsand pages 26-28)

Conservative designed-addition maximum **NA**; aggressive designed-addition maximum **NA**; functional floor for *marine corrosion improvement* **NA**. Neither the **~15.8 wt%** high-temperature binary solvus nor the **~0.107 wt%** experimentally segregating Cu–In composition establishes any of those three application bounds. The latter is a *measurable surface-segregation point*, not a demonstrated beneficial floor. (liu2002thermodynamicassessmentof pages 4-6, madito2012thesegregationof pages 1-15)

## 8. Interactions to retain in joint-constraint analysis

[NUMBERS][GAP] **Ni × In:** Ni-bearing repair dilution can raise a Cu-alloy liquidus, while Cu–In’s binary Cu-rich slope is approximately **−6.12 °C/(wt% In)**; **do not add the binary slopes** to certify a Cu–Ni–In melt temperature. **Al–Fe–Mn × In:** NAB introduces its own constituent phases and interdendritic chemistry; no verified Cu–Al–In–Ni–Fe–Mn phase relation supports an In/Al, In/Ni, In/Fe or In/Mn safe ratio. **S × In:** S displaced In from the surface of dilute Cu–In on laboratory heating, so neither an In–S detoxification rule nor an In–S protective-film synergy is justified. **Sn/Zn × In:** the Cu–In–Sn phase record and Davies’s proposed In-containing brass trials demonstrate *questions to model or test*, not inhibition of tin-bronze dealloying or brass dezincification. Use measured powder/deposit chemistry and dilution-zone maps, rather than an invented compositional sum constraint. (davies1993anoteon pages 6-8, liu2002thermodynamicassessmentof pages 4-6, madito2012thesegregationof pages 1-15, cziegler2015aspectsofgrain pages 57-64, http2007cuinsn(copperindiumtin) pages 6-9)

**Evidence quality: thin for the requested decision.** Binary phase-equilibrium evidence is substantive, and dilute Cu–In surface segregation is directly observed; seawater benefit, AM/weldability, multicomponent thermodynamics and an In-specific specification impurity limit are not established. No publication of the excluded PI has been used. (davies1993anoteon pages 6-8, liu2002thermodynamicassessmentof pages 4-6, madito2012thesegregationof pages 1-15, janssonUnknownyearphasetransformationsand pages 26-28)

VERDICT | In | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.01 | evidence=thin

References

1. (liu2002thermodynamicassessmentof pages 1-2): H. S. Liu, Yuwen Cui, K. Ishida, X. J. Liu, C. P. Wang, I. Ohnuma, R. Kainuma, and Zhanpeng Jin. Thermodynamic assessment of the cu-in binary system. Journal of Phase Equilibria, 23:409-415, Oct 2002. URL: https://doi.org/10.1361/105497102770331352, doi:10.1361/105497102770331352. This article has 69 citations.

2. (madito2012thesegregationof pages 1-15): MJ Madito. The segregation of indium from polycrystalline copper crystals. Unknown journal, 2012.

3. (cziegler2015aspectsofgrain pages 57-64): A Cziegler. Aspects of grain refinement in copper alloys. Unknown journal, 2015.

4. (davies1993anoteon pages 1-3): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

5. (madito2012thesegregationof pages 69-77): MJ Madito. The segregation of indium from polycrystalline copper crystals. Unknown journal, 2012.

6. (dev1996anindigenoustechnology pages 1-2): S.C. Dev and C.S. Sivaramakrishnan. An indigenous technology for a silver brazing alloy. Materials & Design, 17:75-78, Jan 1996. URL: https://doi.org/10.1016/s0261-3069(96)00035-0, doi:10.1016/s0261-3069(96)00035-0. This article has 18 citations and is from a highest quality peer-reviewed journal.

7. (dev1996anindigenoustechnology pages 2-4): S.C. Dev and C.S. Sivaramakrishnan. An indigenous technology for a silver brazing alloy. Materials & Design, 17:75-78, Jan 1996. URL: https://doi.org/10.1016/s0261-3069(96)00035-0, doi:10.1016/s0261-3069(96)00035-0. This article has 18 citations and is from a highest quality peer-reviewed journal.

8. (davies1993anoteon pages 6-8): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

9. (liu2002thermodynamicassessmentof pages 2-4): H. S. Liu, Yuwen Cui, K. Ishida, X. J. Liu, C. P. Wang, I. Ohnuma, R. Kainuma, and Zhanpeng Jin. Thermodynamic assessment of the cu-in binary system. Journal of Phase Equilibria, 23:409-415, Oct 2002. URL: https://doi.org/10.1361/105497102770331352, doi:10.1361/105497102770331352. This article has 69 citations.

10. (liu2002thermodynamicassessmentof pages 4-6): H. S. Liu, Yuwen Cui, K. Ishida, X. J. Liu, C. P. Wang, I. Ohnuma, R. Kainuma, and Zhanpeng Jin. Thermodynamic assessment of the cu-in binary system. Journal of Phase Equilibria, 23:409-415, Oct 2002. URL: https://doi.org/10.1361/105497102770331352, doi:10.1361/105497102770331352. This article has 69 citations.

11. (madito2012thesegregationof pages 15-23): MJ Madito. The segregation of indium from polycrystalline copper crystals. Unknown journal, 2012.

12. (http2007cuinsn(copperindiumtin) pages 6-9): Materials Science International Team MSIT® http. Cu-In-Sn (Copper-Indium-Tin), pages 249-273. Springer Berlin Heidelberg, Jan 2007. URL: https://doi.org/10.1007/978-3-540-47004-5\_26, doi:10.1007/978-3-540-47004-5\_26. This article has 0 citations.

13. (janssonUnknownyearphasetransformationsand pages 26-28): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

14. (madito2012thesegregationof pages 64-69): MJ Madito. The segregation of indium from polycrystalline copper crystals. Unknown journal, 2012.

15. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

16. (younas2026indiumrecoveryfrom pages 18-23): K Younas. Indium recovery from waste liquid crystal displays. Unknown journal, 2026.

17. (kim2021assessmentofoccupational pages 1-2): Boo Wook Kim, Wonseok Cha, Sungwon Choi, Jungah Shin, Byung-Soon Choi, and Miyeon Kim. Assessment of occupational exposure to indium dust for indium-tin-oxide manufacturing workers. Biomolecules, 11:419, Mar 2021. URL: https://doi.org/10.3390/biom11030419, doi:10.3390/biom11030419. This article has 13 citations.

18. (liu2022pulmonaryeffectsof pages 1-2): Nan Liu, Yi Guan, Yan Yu, Gai Li, Ling Xue, Weikang Li, Xiaoyu Qu, Ning Li, and Sanqiao Yao. Pulmonary effects of exposure to indium and its compounds: cross-sectional survey of exposed workers and experimental findings in rodents. Particle and Fibre Toxicology, Dec 2022. URL: https://doi.org/10.1186/s12989-022-00510-w, doi:10.1186/s12989-022-00510-w. This article has 20 citations and is from a domain leading peer-reviewed journal.

19. (chonan2019indiumlungdiscovery pages 1-2): Tatsuya Chonan, Atsuko Amata, Yoshinori Kawabata, and Kazuyuki Omae. Indium lung: discovery, pathophysiology and prevention. The Tohoku journal of experimental medicine, 248 3:143-150, Jul 2019. URL: https://doi.org/10.1620/tjem.248.143, doi:10.1620/tjem.248.143. This article has 23 citations.
