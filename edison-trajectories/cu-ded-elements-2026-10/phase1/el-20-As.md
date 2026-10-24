<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 183535ec-e1e6-40fa-b116-b28129c937c3
- Submitted: 2026-10-17T18:59:50Z
- Fetched: 2026-10-17T19:33:06Z (status: success)
- Raw trajectory JSON: ../raw/el-20-As.json.gz
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

ELEMENT UNDER REVIEW: As (dealloying inhibitor). Arsenical admiralty brass C44300 and aluminum brass C68700 (0.02-0.06 As) to inhibit dezincification; As is limited in Cu-Ni. Toxic; volatile.

Answer for As specifically, not for copper alloys in general:
1. ROLE: what As does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their As ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how As changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-As, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-As, Cu-Ni-As and Cu-Al-As are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of As in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that As neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | As | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: As (dealloying inhibitor). Arsenical admiralty brass C44300 and aluminum brass C68700 (0.02-0.06 As) to inhibit dezincification; As is limited in Cu-Ni. Toxic; volatile.

Answer for As specifically, not for copper alloys in general:
1. ROLE: what As does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their As ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how As changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-As, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-As, Cu-Ni-As and Cu-Al-As are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of As in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that As neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | As | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Arsenic in pre-alloyed copper powder for seawater-service DED

**Decision: LIMIT As as an incidental impurity, not a designed addition.** [CITE] Arsenic’s established marine-alloy function is suppression of *dezincification in predominantly α-phase brass*. That is not evidence that it suppresses selective attack of Ni–Al bronze (NAB), Cu–Ni, or an as-deposited composition between those families. Conversely, a welding technical report specifically identifies As as a potential hot-cracking contributor **when Ni is present**, and an accelerated seawater study associates As with poorer stress-corrosion-cracking (SCC) resistance in aluminum brass. Both repair substrates introduce Ni. There is no retrieved As-dosed, blown-powder DED seawater comparison against wrought C71500. The resulting impurity ceiling below is a **precautionary feedstock criterion**, not a demonstrated safe threshold for these deposits. (davies1993anoteon pages 1-3, czajkowski2001investigationinhardsurfacing pages 51-55, beavers1980corrosionrelatedfailuresin pages 169-175)

## 1. Role, alloy families, and specifications

- **α-brasses—including arsenical Admiralty and aluminum brass:** [CITE] Dissolved, deliberately added As inhibits preferential Zn loss. Proposed explanations differ: As in the *bulk* alloy is necessary in one set of plating experiments; another proposes As(III) dissolution and redeposition as an As-rich surface film that impedes Cu redeposition; an electrochemical account proposes surface arsenite/arsenate adsorption that impedes Zn dissolution. Neither mechanism establishes a protective As-containing film on Cu–Ni or NAB. The retrieved experiments find little effect through **0.014 wt% As**, inhibition around **0.024 wt% As**, and minimum measured attack around **0.05–0.084 wt% As**, depending on experiment. These are brass findings, not transferable composition bounds. (davies1993anoteon pages 1-3, davies1993anoteon pages 3-4)
- **Cu–As itself:** [CITE] At trace concentrations, thermodynamic calculations for high-purity Cu put As in the **Cu solid solution**, rather than predicting an arsenide precipitate; much higher As concentrations can form Cu arsenides. A separate Cu–As materials account reports reduced casting porosity, including under oxidizing casting conditions, but supplies no DED validation or evidence that As substitutes for controlled deoxidation of the proposed multicomponent melt. No demonstrated As grain-refining, Cu–Ni protective-film, or NAB κ-phase-control function was retrieved. (modlinger2023structuresandphase pages 5-10, magnusson2017thermodynamicevaluationof pages 12-14, magnusson2017thermodynamicevaluationof pages 14-16)
- **Cu–Ni, NAB/other aluminum bronzes, Mn–Al bronze, tin bronze/gunmetal, Cu–Ni–Sn and Cu–Ni–Si:** [GAP] The retrieved evidence establishes no *designed As addition with a quantified seawater benefit* in these families. An archaeological account notes As/Sb-rich regions of ancient tin bronzes associated with resistance to bacteria-influenced attack; that observation is not a commercial marine-alloy specification or a controlled As-versus-no-As comparison. In Ni-containing alloys, the pertinent documented role is instead **potential weld-hot-cracking impurity**. (modlinger2023structuresandphase pages 5-10, czajkowski2001investigationinhardsurfacing pages 51-55)
- **[SPEC] What can be stated securely:** A cited compositional table for oxygen-free **UNS C10100** gives **As ≤0.0005 wt% (5 ppm)**. This is a high-purity-Cu *precedent for feedstock control*, **not** an ASTM B148 C95800, ASTM B111 C71500, or AWS A5.7 filler limit. The user-supplied **0.02–0.06 wt% As** ranges for arsenical **C44300/C68700** are consistent with the historical brass-inhibition window but could **not be independently checked against the controlling editions of ASTM B111/B171/B466 or UNS/CDA composition sheets** in the retrieved texts; they must not be presented as verified specification quotations. Likewise, no explicit As limit was verified here for **C70600, C71500, C95800, ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl**, or for MIL-T-16420, MIL-B-24480, or MIL-C-15726. Absence of a reported As entry is **not** an As-zero specification. (magnusson2017thermodynamicevaluationof pages 9-12)

## 2. Seawater corrosion: benefits and adverse findings

**[NUMBERS][CITE] Brass inhibition window:** A copper-industry review reports that brass with up to **0.014 wt% As** still dezincified, **0.024 wt% As** inhibited dezincification in the investigated α-brasses, and **0.084 wt% As** gave a minimum corrosion rate in that experimental series. A different study of α 70–30 brass found corrosion and dezincification rates decreased up to about **0.05 wt% As**. These reports do **not** supply directly comparable corrosion rates in mm/year, electrochemical film resistances, or ASTM D1141 exposures; some underlying tests used aggressive CuCl₂/HCl media. They establish a *brass-specific effect threshold*, not that an As-bearing DED repair equals C71500 in seawater. (davies1993anoteon pages 3-4, sarver2010submittedoctober2009 pages 92-94)

**[NUMBERS][CITE] Where As harms or fails:** In a duplex approximately 60–40 brass, **0.25 wt% As** was reported to **more than triple** the dezincification rate; in a separate Pb-bearing duplex brass, a similar addition increased it by about **30%**. Arsenical Admiralty brass also showed a reported tendency toward intercrystalline attack in seawater. An accelerated test of **aluminum brass in seawater amended with 1 g/L Cu²⁺ and ammonia** found SCC resistance declined as As increased from **0 to 0.08 wt%**, especially in the elastic stress range; at **0.10 wt%**, specimens at approximately **1% elongation** did not fail. That non-monotonic result and deliberately contaminated environment preclude a simple seawater-safe threshold. In a *different* experiment, **0.30 wt% As** in Cu–**1 wt% Al**–**2.2 wt% Fe** suffered moderate surface cracking during rolling and all stressed samples failed within **160 h** in **177 °C wet steam**; the no-addition control also failed within **160 h**. Steam results cannot be labeled seawater corrosion results. (davies1993anoteon pages 3-4, beavers1980corrosionrelatedfailuresin pages 169-175)

**[GAP]** No credible retrieved matched As-dosed versus As-free measurements of seawater **E_corr, polarization resistance, impedance, cyclic-polarization breakdown, penetration depth, crevice or pitting statistics, erosion-corrosion, or critical flow velocity** were found for C71500-type Cu–Ni, C95800-type NAB, or their DED deposits. A report finds conventional C70600 generally suitable to approximately **3 m/s** seawater flow, but supplies **no As comparison**; quoting that as an As-dependent velocity limit would be incorrect. (barros2026performanceofcoppernickel pages 7-15, beavers1980corrosionrelatedfailuresin pages 23-28)

## 3. Laser DED, substrate dilution, and powder manufacture

**[CITE] Welding evidence, not AM proof.** A technical report on Cu–Ni welding states that As ordinarily does not pose a welding problem in Cu alloys **unless Ni is present**, then lists As among residual elements capable of causing hot cracking in Ni-bearing Cu alloys. It does **not** determine an As threshold, prove that As caused the particular weld failure studied, or separate solidification cracking from reheated-layer liquation cracking. Thus As segregation into last-to-freeze liquid and possible boundary-film remelting in overlapping DED tracks are **risk hypotheses**, not observed As-specific DED defects. Ni from either Cu–Ni repair stock or C95800 dilution makes a nominally Ni-free powder an inadequate control. Assess the highest-dilution first layer as well as self-built layers; measure As by analysis in **charge → powder → each deposit region**, rather than assuming nominal charge equals deposited composition. No As-specific evidence was retrieved for the four named AWS filler grades. (czajkowski2001investigationinhardsurfacing pages 51-55)

**[CITE][GAP] Melt and atomizer:** Cu–As synthesis studies used **sealed quartz**, gradual heating, and precautions against oxidation. As₂O₃ vapor condensed from an As-cleaning experiment at **300 °C**; a separate thermal-analysis setup used **alumina** with an added Cu cap intended to capture As vapor, and As loss/redeposition was observed in As-rich samples. This supports a real volatility and fume-control concern, **not** a measured loss fraction for an argon induction melt, ultrasonic atomization, or a 1.07-µm laser. Neither a reaction rate with **alumina, zirconia, graphite, Ti-alloy or Mo sonotrodes**, nor an As-dependent melt surface-tension change was verified. As in an oxygen-free Cu charge is not established as a reliable deoxidizer. Powder, condensate, filters, enclosure surfaces and laser plume require As-specific sampling before asserting safe operation. (modlinger2023cu3asuncommoncrystallographic pages 2-4, modlinger2023structuresandphase pages 22-26, modlinger2023structuresandphase pages 10-16, modlinger2023structuresandphase pages 16-18)

## 4. Phase diagram and CALPHAD

**[NUMBERS][CITE]** An assessed Cu–As phase-diagram account places peak As solubility in α-Cu at **6.83 at%**, equivalent by atomic-weight conversion to approximately **7.95 wt% As**; the examined excerpt does **not** establish the temperature of that maximum, so an exact temperature should not be supplied. This equilibrium limit is *not* a safe weldability or seawater design limit. A 2023 experimental study finds approximately stoichiometric **Cu₃As melts congruently at 835 °C**, revising the earlier assessed **827 °C** value; other reported phases include a β arsenide with disputed formula and a δ phase often denoted **Cu₅As₂**, reported to form peritectically around **709 °C**. The study disputes an earlier proposed Cu₃As polymorphic transition. A reliable numerical Cu-rich eutectic composition/temperature was **not established** from retrieved text. (modlinger2023structuresandphase pages 5-10, modlinger2023cu3asuncommoncrystallographic pages 1-2, magnusson2017thermodynamicevaluationof pages 23-28)

**[CITE] Published CALPHAD exists:** Uhland, Lechtman and Kaufman, *Calphad* **25** (2001) 109–124, **DOI 10.1016/S0364-5916(01)00034-7**, assessed **As–Cu–Ni** and therefore its Cu–As description; the independent Cu–As assessment by Shishin and Jak, *Calphad* (2018), **DOI 10.1016/j.calphad.2017.12.005**, is also identifiable. The experimental Cu–As review is Subramanian and Laughlin, *Bulletin of Alloy Phase Diagrams* **9** (1988) 605–618, **DOI 10.1007/BF02881964**. [GAP] A usable, validated **Cu–Al–As** ternary assessment and As-enabled **TCCU/COST 531** installation were **not verified**. Inspect the *actual installed TCCU element list and parameter/phase inventory* before pycalphad calculations; published As–Cu–Ni parameters do not establish that the installed commercial database contains As or trustworthy As interactions with Al–Fe–Mn. (modlinger2023structuresandphase pages 50-53, magnusson2017thermodynamicevaluationof pages 12-14, magnusson2017thermodynamicevaluationof pages 23-28)

**Liquidus constraint:** [CITE] The Cu-rich assessment reports some liquid-model disagreement but reasonable agreement within the first few percent As; no verified slope at **≤0.0005 wt% As** was retrieved. On physical grounds, adding a few ppm As to Cu cannot plausibly raise the liquidus of an otherwise atomizable Cu-rich alloy from approximately copper’s melting region to **>1,250 °C**; *Ni/Al and the full alloy composition*, not an As impurity bound, control that screening decision. No defensible As-induced temperature shift in °C should be claimed without a validated database calculation. Figure A-1 in the cited thermodynamic report plots **As mole fraction**, not wt%: converting the axis is necessary before applying a composition constraint. (magnusson2017thermodynamicevaluationof pages 23-28, magnusson2017thermodynamicevaluationof media 9a3abe1d)

## 5. Supply, controls, interactions, and bound

**[NAVY][CITE] Criticality:** As appears on the **2022 U.S. critical-minerals list** and the **final 2025 list**. Crucially, a 2025 USGS *technical proposal* suggested deleting As, whereas the eventual final list **retained As**; Cu appears on the final list. The suggested deletion must not be mistaken for the final federal decision. No Navy-specific ban on As-bearing Cu alloys was verified. (nassar2025methodologyandtechnical pages 33-35, staff2022usgsminingreview pages 6-9, halkes2024uk2024criticality pages 45-51)

**[NUMBERS][CITE] Health and cost:** The OSHA inorganic-As standard, **29 CFR 1910.1018**, sets an **8-hour PEL of 10 µg As/m³** and an **action level of 5 µg As/m³**. These are *air concentrations*, not allowable powder or alloy compositions. A NIOSH evaluation of thermal metal cutting identified inhalation, dermal and ingestion pathways and documented contaminated work surfaces; use enclosed transfer, local exhaust/HEPA procedures appropriate to the assessed hazard, personal sampling and controlled waste handling. **[GAP]** No defensible current **$/kg price for alloy-grade elemental As** was recovered; As₂O₃ commodity prices must not be substituted for a quoted metal-powder procurement price. RoHS is not an automatic blanket ban on elemental As in a naval bronze; applicability of particular REACH entries and contract clauses requires material/form/use review. (methner2003healthhazardevaluation pages 4-6, magnusson2017thermodynamicevaluationof pages 9-12)

**[SPEC][NUMBERS] Recommended LIMIT:** Set **As ≤0.0005 wt% (5 ppm) in both powder and measured deposit**, with **no intentional As charge**, for **both Cu–Ni and Al-bronze-family candidates**. The numerical precedent is the **UNS C10100** As maximum reported in the SKB specification table—not a demonstrated permissible limit for C71500/C95800 or an AWS filler. The failure modes setting this *conservative programmatic limit* are Ni-associated weld-hot-cracking concern, uncertain interlayer liquation/volatilization and toxicity, coupled with the lack of proven benefit outside Zn-rich α-brass. It is **not** a claim that **6 ppm** cracks or that **5 ppm** guarantees a crack-free deposit. At **0.0005 wt%**, a **0.5-kg** charge contains at most **2.5 mg As**, before any process loss; the dose alone does not determine airborne exposure. Because the decision is LIMIT, there is **no proposed conservative designed-addition maximum, aggressive maximum, or functional floor** for these two families. A brass-only functional threshold of **0.024 wt%** would exceed the proposed impurity criterion by roughly **48-fold** and would solve a different, Zn-dealloying problem. (davies1993anoteon pages 3-4, czajkowski2001investigationinhardsurfacing pages 51-55, magnusson2017thermodynamicevaluationof pages 9-12)

**Interactions for joint constraints:** [CITE] As’s demonstrated inhibitor function requires an α-*Cu–Zn* context and does not rescue β-rich brass; **0.04 wt% As** failed to prevent attack in two studied Si-rich brasses. In brass experiments, Fe and Mn could worsen dezincification, while Ni or Sn had their *own* composition-dependent benefits; there is no defensible numerical **As/(Ni, Fe, Mn or Al)** rule for NAB or Cu–Ni. In welding, **As × Ni** is the principal qualitative interaction to track, including **substrate dilution**. At impurity levels the cited high-purity-Cu equilibrium model leaves As in solution and does not predict an As–P precipitate; do not infer that P neutralizes As or that adding As neutralizes harmful Pb/Bi/S/Se/Te. These observations do not replace deposit-specific composition mapping and corrosion/depth-of-attack tests. (davies1993anoteon pages 4-5, czajkowski2001investigationinhardsurfacing pages 51-55, magnusson2017thermodynamicevaluationof pages 12-14, magnusson2017thermodynamicevaluationof pages 14-16)

**Evidence rating: thin for the requested DED decision.** [GAP] Brass dealloying thresholds and Cu–As phase chemistry are documented; quantitative **As-controlled, as-deposited** comparisons across Cu–Ni/NAB, repeated-layer cracking, crucible/sonotrode compatibility, and the specified 30-day ASTM D1141 versus wrought C71500 acceptance test are not. A **5-ppm screening rule is therefore a testable conservative choice, not an experimentally proven cross-family tolerance**. No publication by the identified PI is relied on above. (davies1993anoteon pages 3-4, czajkowski2001investigationinhardsurfacing pages 51-55, beavers1980corrosionrelatedfailuresin pages 169-175, magnusson2017thermodynamicevaluationof pages 9-12)

VERDICT | As | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.0005 | evidence=thin

References

1. (davies1993anoteon pages 1-3): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

2. (czajkowski2001investigationinhardsurfacing pages 51-55): C. CZAJKOWSKI and M. BUTTERS. Investigation in hardsurfacing a nickel-copper alloy (monel400). ArXiv, Dec 2001. URL: https://doi.org/10.2172/791763, doi:10.2172/791763. This article has 5 citations.

3. (beavers1980corrosionrelatedfailuresin pages 169-175): J. A. Beavers, A. K. Agrawal, and W. E. Berry. Corrosion-related failures in power plant condensers. final report. [pwr]. Unknown journal, Aug 1980. URL: https://doi.org/10.2172/5047866, doi:10.2172/5047866. This article has 6 citations.

4. (davies1993anoteon pages 3-4): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

5. (modlinger2023structuresandphase pages 5-10): M Mödlinger. Structures and phase equilibria in the ternary cu-as-sb system. Unknown journal, 2023.

6. (magnusson2017thermodynamicevaluationof pages 12-14): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

7. (magnusson2017thermodynamicevaluationof pages 14-16): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

8. (magnusson2017thermodynamicevaluationof pages 9-12): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

9. (sarver2010submittedoctober2009 pages 92-94): E Sarver, Y Zhang, and M Edwards. Submitted: october, 2009 to: corrosion reviews status: published july, 2010 (vol. 28, no. 3-4). Unknown journal, 2010.

10. (barros2026performanceofcoppernickel pages 7-15): Edilson F. de Barros and Fernando B. Mainier. Performance of copper-nickel alloy used in synthetic seawater contaminated by nitrogenated fertilizers. Unknown journal, Jun 2026. URL: https://doi.org/10.70593/978-93-7185-452-8, doi:10.70593/978-93-7185-452-8.

11. (beavers1980corrosionrelatedfailuresin pages 23-28): J. A. Beavers, A. K. Agrawal, and W. E. Berry. Corrosion-related failures in power plant condensers. final report. [pwr]. Unknown journal, Aug 1980. URL: https://doi.org/10.2172/5047866, doi:10.2172/5047866. This article has 6 citations.

12. (modlinger2023cu3asuncommoncrystallographic pages 2-4): Marianne Mödlinger, Alessia Provino, Pavlo Solokha, Federico Caglieris, Michele Ceccardi, Daniele Macciò, Marcella Pani, Cristina Bernini, Dario Cavallo, Andrea Ciccioli, and Pietro Manfrinetti. Cu3as: uncommon crystallographic features, low-temperature phase transitions, thermodynamic and physical properties. Materials, 16:2501, Mar 2023. URL: https://doi.org/10.3390/ma16062501, doi:10.3390/ma16062501. This article has 8 citations.

13. (modlinger2023structuresandphase pages 22-26): M Mödlinger. Structures and phase equilibria in the ternary cu-as-sb system. Unknown journal, 2023.

14. (modlinger2023structuresandphase pages 10-16): M Mödlinger. Structures and phase equilibria in the ternary cu-as-sb system. Unknown journal, 2023.

15. (modlinger2023structuresandphase pages 16-18): M Mödlinger. Structures and phase equilibria in the ternary cu-as-sb system. Unknown journal, 2023.

16. (modlinger2023cu3asuncommoncrystallographic pages 1-2): Marianne Mödlinger, Alessia Provino, Pavlo Solokha, Federico Caglieris, Michele Ceccardi, Daniele Macciò, Marcella Pani, Cristina Bernini, Dario Cavallo, Andrea Ciccioli, and Pietro Manfrinetti. Cu3as: uncommon crystallographic features, low-temperature phase transitions, thermodynamic and physical properties. Materials, 16:2501, Mar 2023. URL: https://doi.org/10.3390/ma16062501, doi:10.3390/ma16062501. This article has 8 citations.

17. (magnusson2017thermodynamicevaluationof pages 23-28): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

18. (modlinger2023structuresandphase pages 50-53): M Mödlinger. Structures and phase equilibria in the ternary cu-as-sb system. Unknown journal, 2023.

19. (magnusson2017thermodynamicevaluationof media 9a3abe1d): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

20. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

21. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

22. (halkes2024uk2024criticality pages 45-51): R Halkes, N Idoine, C Mitchell, I Watkins, and F Price. Uk 2024 criticality assessment. Unknown journal, 2024.

23. (methner2003healthhazardevaluation pages 4-6): MM Methner. Health hazard evaluation report: heta# 2002-0351-2903: bechtel-jacobs co., llc, piketon, ohio. Unknown journal, 2003.

24. (davies1993anoteon pages 4-5): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.
