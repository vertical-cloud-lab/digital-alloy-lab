<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 3a6a153c-2f65-4e4c-9f0a-f7d9baf9bfa1
- Submitted: 2026-10-17T19:01:20Z
- Fetched: 2026-10-17T19:28:13Z (status: success)
- Raw trajectory JSON: ../raw/el-43-Y.json.gz
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

ELEMENT UNDER REVIEW: Y (rare earth). Yttrium as an oxygen getter and grain refiner in copper and Cu-Ni; yttria crucibles and coatings.

Answer for Y specifically, not for copper alloys in general:
1. ROLE: what Y does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Y ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Y changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Y, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Y, Cu-Ni-Y and Cu-Al-Y are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Y in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Y neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Y | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Y (rare earth). Yttrium as an oxygen getter and grain refiner in copper and Cu-Ni; yttria crucibles and coatings.

Answer for Y specifically, not for copper alloys in general:
1. ROLE: what Y does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Y ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Y changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Y, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Y, Cu-Ni-Y and Cu-Al-Y are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Y in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Y neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Y | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Yttrium (Y): a narrow Cu–Ni research addition, not a qualified marine-alloy constituent

**Decision — INCLUDE, for exploratory Cu–Ni compositions only.** [CITE][NUMBERS] The directly relevant result is for **as-cast 90Cu–10Ni–0.021Y wt%**: after 30 days in **3.5 wt% NaCl**, its inner corrosion-product-film resistance exceeded **1,500 kΩ**. Resistance first improved and then deteriorated as Y increased. This warrants a tightly bounded composition variable, not a claim that Y-bearing deposits will meet wrought C71500 performance or that the result transfers to nickel-aluminum bronze (NAB). The retrieved study supplies neither a validated upper failure concentration nor a DED result. Zhang *et al.*, *International Journal of Electrochemical Science* **15** (2020), 4161–4178, DOI: **10.20964/2020.05.47**. (zhang2020microstructureandcorrosion pages 1-1)

## 1. Role, alloy families, and specifications

[CITE] In the cast Cu–Ni experiment, Y refined **secondary dendrite spacing**; increasing Y also increased the number and size of **Y-rich oxysulfide inclusions**. The authors attributed the improved film to suppression of the change from Cu₂O to Cu₂(OH)₃Cl and an effect on Ni diffusion. These are reported observations and proposed mechanisms, respectively—not evidence of useful bulk solid-solution strengthening, a Y-bearing precipitation-hardening treatment, or proven inhibition of dealuminification or dezincification. Zhang *et al.*, DOI: **10.20964/2020.05.47**. (zhang2020microstructureandcorrosion pages 1-1)

[GAP] No verified **metallic-Y range** was found for commercial or Navy C70600, C71500, C95800 or other NAB, Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si; nor for the corresponding filler classifications **ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl**. In particular, none of the consulted ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449, or UNS/CDA categories yielded a **verified specified Y range or Y impurity limit**. This is *not* a certification that every edition of every standard prohibits Y: absence of a specified Y range is different from a specification-based zero-Y maximum. A frequently tempting aluminum-bronze comparison, Li *et al.*, *Journal of Materials Engineering and Performance* **15** (2006), 102–110, DOI: **10.1361/105994906X83466**, lists unspecified rare-earth material and describes **cerium** addition, not a measured Y addition; its corrosion numbers must not be assigned to Y. (li2006corrosionwearbehavior pages 2-4, li2006corrosionwearbehavior pages 1-2)

## 2. Seawater corrosion: what is measured

[NUMBERS][CITE] For **90Cu–10Ni**, the documented beneficial point is **0.021 wt% Y**, **30 days**, **3.5 wt% NaCl**, and **inner-film resistance >1,500 kΩ**. At higher Y the reported corrosion resistance deteriorated and Y-rich oxysulfides became more numerous and larger. The available retrieved text does **not** give the other tested Y contents, their numerical film resistances, corrosion rates, *E*corr, or a concentration at which the Y-bearing alloy becomes worse than its Y-free control. Thus the helpful *measured point* is 0.021 wt%; neither a continuous beneficial range nor a numerical harmful threshold is established. Zhang *et al.*, DOI: **10.20964/2020.05.47**. (zhang2020microstructureandcorrosion pages 1-1)

[GAP] There is no verified Y-specific comparison against **wrought C71500**, or Y-specific natural-seawater/ASTM D1141 cyclic-polarization, 30-day selective-attack depth, pitting, crevice, erosion–corrosion, or limiting-flow-velocity result for the intended deposits. Do not translate the reported impedance into a corrosion rate or a service velocity. The Li *et al.* Al-bronze study reports **0.0264, 0.0258, and 0.026 g m⁻² h⁻¹** for its as-cast Cu–14Al–X, heat-treated Cu–14Al–X, and QAl9-4 comparators, respectively, but **does not isolate Y**; these are specifically *not* Y-effect estimates. Li *et al.*, DOI: **10.1361/105994906X83466**. (li2006corrosionwearbehavior pages 2-4, li2006corrosionwearbehavior pages 1-2)

## 3. DED, repair welding, and powder manufacture

[GAP] No retrieved study measures metallic Y's effect on **fiber-laser, single-stream blown-powder Cu-alloy DED**: solidification or reheating-layer liquation cracking, pore fraction, powder-to-deposit Y retention, or dilution into cast C95800 or wrought Cu–Ni. The cast dendrite-refinement result provides a *hypothesis* for reducing localized segregation, not evidence of crack suppression. Conversely, oxide/oxysulfide accumulation and an unverified terminal Cu–Y-rich liquid could impair feeding or create reheating-sensitive boundaries; neither failure mode has been demonstrated for these DED compositions. AWS A5.7 filler names establish useful **Y-free repair comparators**, not evidence that their weldability can be transferred to Y-modified deposits. Zhang *et al.*, DOI: **10.20964/2020.05.47**. (zhang2020microstructureandcorrosion pages 1-1)

[GAP] For the specified **≤1,300 °C induction module**, distinguish the starting melt from a nominal powder composition: some charged Y may instead report to slag, crucible/interface reaction products, or powder-surface oxide. Premelt Cu–Y master alloy versus pure Y, addition order, hold time, oxygen and sulfur in the charge, and **metallic versus total Y** should be recorded for each ~0.5-kg heat. Alumina and zirconia crucibles, yttria coatings, and Ti-alloy or Mo sonotrodes require *separate* blank heats and post-run microscopy/chemical assays; a yttria-coated vessel introduces **Y₂O₃ ceramic**, not automatically useful metallic Y. Oxide-crucible compatibility literature retrieved here concerns **Ti–Al melts**, not Y-bearing Cu melt: Kostov and Friedrich, *Journal of Mining and Metallurgy B* **41** (2005), 113–125, DOI: **10.2298/JMMB0501113K**. No defensible Cu–Y-specific numerical vapor-loss, sonotrode-attack, contact-angle, surface-tension, or atomization-yield coefficient was found. (kostov2005selectionofcrucible pages 1-5, fedorov2021zirconiumdioxide.review pages 1-3)

## 4. Phase diagram and CALPHAD

[CITE] Cu-rich equilibrium experiments in **Mg–Cu–Y at 673 K (400 °C)** identify **Cu₆Y, Cu₄Y, Cu₇Y₂, and Cu₂Y** and report **no detected Y solubility in fcc Cu**. Crucially, approximately **1 at% Mg** dissolving in those compounds is **not** 1 wt% Y soluble in copper. The retrieved results do **not** establish a numerical **maximum Y solubility in Cu in wt% at its maximum-solubility temperature**, a trustworthy Cu–Y invariant-reaction temperature or composition, or a Cu-rich liquidus slope. Accordingly, those requested numerical quantities are **unknown here**, rather than inferred from compound stoichiometry. Mezbahul-Islam and Medraj, *Scientific Reports* **3** (2013), article 3033, DOI: **10.1038/srep03033**. (mezbahulislam2013phaseequilibriumin pages 2-3, mezbahulislam2013phaseequilibriumin pages 9-10)

[GAP] The experimentally demonstrated **0.021 wt% Y** addition alone does not establish that a *given multicomponent* Cu–Ni or Cu–Al alloy's liquidus remains below **1,200–1,250 °C**. Reject candidate **full compositions**, not elemental Y in isolation, when calculated or measured liquidus plus necessary atomization superheat exceeds the module's ~1,300 °C capability. Existence of binary/ternary phase literature does **not** verify an assessed **Cu–Y, Cu–Ni–Y, or Cu–Al–Y description in the installed Thermo-Calc TCCU, COST 531, or an accessible pycalphad TDB**. Confirm the actual database's constituent list and assessed interactions before trusting phase fractions, terminal liquid, or liquidus predictions; otherwise treat them as extrapolations requiring DSC and microanalysis. The available Mg–Cu–Y study cannot serve as a validated Cu–Ni–Y or Cu–Al–Y database. Mezbahul-Islam and Medraj, DOI: **10.1038/srep03033**. (mezbahulislam2013phaseequilibriumin pages 2-3, mezbahulislam2013phaseequilibriumin pages 9-10)

## 5. Supply, cost, exposure, and joint constraints

[CITE][NAVY] Y is a **U.S. critical mineral**; the reviewed USGS account explicitly lists it, alongside Cu and Ni, on the **final 2025 list**, published **7 November 2025, 90 FR 50494**. The USGS technical supply-risk assessment is Nassar *et al.*, *Open-File Report 2025–1047* (2025), DOI: **10.3133/ofr20251047**. Its mineral-risk graphic identifies Y, Cu, and Ni separately; mineral criticality is a supply concern, **not a Navy prohibition on Y**. Y was also on the 2022 critical-minerals list, but no verified commodity quote was obtained from these sources for **metallic Y at powder-atomization purity**. Consequently, an approximate **$/kg price cannot responsibly be stated from the evidence reviewed**; quote purchase form, purity, date, and batch scale rather than substituting an yttria price. (nassar2025methodologyandtechnical pages 1-4, staff2022usgsminingreview pages 9-11, staff2022usgsminingreview pages 6-9, nassar2025methodologyandtechnical media 13b75bd1)

[GAP] No Y-specific OSHA permissible-exposure limit, RoHS/REACH alloy concentration limit, or Navy Y restriction was established by the retrieved sources. That does **not** waive applicable controls: segregate fine reactive metal powder from ignition sources; use inert-handling and combustible-dust precautions where the actual powder classification warrants them, local laser-fume extraction, and exposure assessment for the **Cu/Ni-bearing** aerosol as well as Y-bearing oxide particulates. Toxicity and regulatory compliance require the supplier SDS and facility-specific review; no unsupported numerical exposure limit is implied.

**Interactions to retain in joint constraints.** [CITE][GAP] Track **retained Y** jointly with oxygen and sulfur: an increasing Y-rich **oxysulfide inclusion burden** is the experimentally observed adverse interaction, whereas the useful corrosion-film effect was observed in a **Cu–Ni matrix** and attributed partly to changed Ni diffusion. Assess Y and Ni jointly without assuming a numerical Y:Ni ratio or that Y can replace enough Ni to reproduce C71500 behavior. For NAB, evaluate Y with **Al, Ni, Fe, and Mn** against phase partitioning, dilution, and any cast-substrate reaction; no verified beneficial Y:(Al, Fe, or Mn) ratio exists. Treat oxide-derived Y separately from retained metallic Y, and do not assume that Y neutralizes NAB dealuminification, brass dezincification, or Cu–Ni–Sn selective attack. Zhang *et al.*, DOI: **10.20964/2020.05.47**; Mezbahul-Islam and Medraj, DOI: **10.1038/srep03033**. (zhang2020microstructureandcorrosion pages 1-1, mezbahulislam2013phaseequilibriumin pages 2-3)

## 6. Composition bounds and evidence quality

The following table separates the observed Cu–Ni result from proposed search limits. (zhang2020microstructureandcorrosion pages 1-1, li2006corrosionwearbehavior pages 1-2)

| Metallic Y (wt%) | Family / condition | Evidence or bound | Interpretation / limitation |
|---:|---|---|---|
| 0 | Cu-Ni control | A Y-free comparator was included in the as-cast 90Cu-10Ni study, but the retrieved text does not report its numerical film resistance. Zhang et al. (2020), DOI: [10.20964/2020.05.47](https://doi.org/10.20964/2020.05.47) (zhang2020microstructureandcorrosion pages 1-1) | Baseline only; no quantitative value is available from the retrieved evidence. |
| 0.021 | As-cast 90Cu-10Ni; 30 d in 3.5 wt% NaCl | Inner-film resistance **>1,500 kΩ**. Corrosion resistance first improved and then deteriorated as Y increased. Proposed mechanisms were inhibited conversion of Cu₂O to Cu₂(OH)₃Cl, altered Ni diffusion, and dendrite refinement. Higher Y produced more and larger Y-rich oxysulfide inclusions. Zhang et al. (2020), DOI: [10.20964/2020.05.47](https://doi.org/10.20964/2020.05.47) (zhang2020microstructureandcorrosion pages 1-1) | The only directly supported beneficial metallic-Y composition found for a seawater-relevant Cu alloy. |
| **0.021** | Cu-Ni | **Trial conservative ceiling** | Set at the demonstrated optimum, not at a commercial or specification limit. The failure mode above it is growth of Y-rich oxysulfide inclusions accompanied by nonmonotonic deterioration of corrosion resistance. |
| **0.021** | Cu-Ni | **Functional floor** | Lowest composition having a retrieved, measurable Y-specific corrosion effect; this does **not** prove that smaller additions are ineffective. |
| **0.05** | Cu-Ni | **Hypothetical exploratory ceiling; unsupported by direct evidence** | Not validated by Cu-Ni corrosion, welding, cladding, or DED evidence and not source-based. Use only as a deliberately aggressive screening point; otherwise report the nonconservative maximum as **NA**. |
| Unknown | Aluminum bronze / NAB | No metallic-Y composition bound was found. The retrieved Cu-14Al-X study used an unspecified rare-earth addition and separately identifies cerium during melting, so it cannot establish a Y bound. DOI: [10.1361/105994906X83466](https://doi.org/10.1361/105994906X83466) (li2006corrosionwearbehavior pages 2-4, li2006corrosionwearbehavior pages 1-2) | Do not transfer the Cu-Ni value to NAB without experiments. |
| Not equivalent | Y₂O₃ powder or yttria crucible/coating | Y₂O₃ is an oxide ceramic, not a metallic-Y alloy addition; its wt% cannot be entered directly as alloyed Y. Yttria or yttria-stabilized zirconia may contribute inclusions or oxygen rather than dissolved Y (kostov2005selectionofcrucible pages 1-5, fedorov2021zirconiumdioxide.review pages 1-3) | Track metallic Y and oxide-borne Y separately in charge balance, powder analysis, and deposit chemistry. |
| None found | Commercial and Navy specifications | No Y range or limit was found in the reviewed UNS/CDA, ASTM, MIL, EN, or AWS copper-alloy and filler categories. | **0.021 wt% is experimental, not a standard limit; no specification-based impurity maximum is available.** |


*Table: This table separates directly demonstrated metallic-Y behavior from proposed search bounds and from non-equivalent Y₂O₃ additions. It highlights that only 0.021 wt% Y in as-cast 90Cu-10Ni has direct marine-corrosion support.*

[NUMBERS] **Conservative maximum: 0.021 wt% Y, Cu–Ni only.** It is the *experimental as-cast corrosion point*, **not** a commercial/Navy/DED qualification limit. **Functional floor: 0.021 wt% Y, Cu–Ni only**, meaning the lowest *retrieved demonstrated* Y-specific point, **not** proof that a smaller concentration has no effect. **Non-conservative screening maximum: 0.05 wt% Y, Cu–Ni only**, explicitly a **proposal-design extrapolation, not a measured safe bound**: its purpose is to test whether the higher-Y oxysulfide/corrosion reversal occurs before this point. The retrieved study cannot certify it as beneficial. For Al-bronze/NAB there is **no defensible evidence-derived Y upper bound or floor**. The principal upper-bound failure is **Y-rich inclusions coupled to worsening corrosion**; terminal segregation, cracking, and loss during processing remain unquantified risks. No specification-based Y **impurity maximum** can be assigned. Zhang *et al.*, DOI: **10.20964/2020.05.47**. (zhang2020microstructureandcorrosion pages 1-1)

**Evidence grade: thin for this DED decision.** One directly relevant **cast, 90Cu–10Ni, laboratory-NaCl** experiment supports a narrow Y trial; it does not answer natural seawater, comparative wrought C71500 resistance, 30-day selective-attack depth in deposits, Y-bearing NAB repair, weld cracking, powder retention, or full-composition CALPHAD. A successful impedance result is therefore a **screening rationale**, not evidence that the proposed as-deposited Navy repair material already meets its corrosion objective. (zhang2020microstructureandcorrosion pages 1-1, mezbahulislam2013phaseequilibriumin pages 2-3)

VERDICT | Y | decision=INCLUDE | family=Cu-Ni | conservative_max_wt=0.021 | nonconservative_max_wt=0.05 | floor_wt=0.021 | impurity_max_wt=NA | evidence=thin

References

1. (zhang2020microstructureandcorrosion pages 1-1): Yinghui Zhang, Chunmei Song, Yanfeng Cao, Hang Wang, Zhigang Wang, and Bin Yang. Microstructure and corrosion behavior of as-cast 90cu-10ni alloys with different yttrium content. International Journal of Electrochemical Science, 15:4161-4178, May 2020. URL: https://doi.org/10.20964/2020.05.47, doi:10.20964/2020.05.47. This article has 15 citations and is from a peer-reviewed journal.

2. (li2006corrosionwearbehavior pages 2-4): W.S. Li, Z.P. Wang, Y. Lu, and L.H. Yuan. Corrosion wear behavior of al-bronzes in 3.5% nacl solution. Journal of Materials Engineering and Performance, 15:102-110, Feb 2006. URL: https://doi.org/10.1361/105994906x83466, doi:10.1361/105994906x83466. This article has 19 citations and is from a peer-reviewed journal.

3. (li2006corrosionwearbehavior pages 1-2): W.S. Li, Z.P. Wang, Y. Lu, and L.H. Yuan. Corrosion wear behavior of al-bronzes in 3.5% nacl solution. Journal of Materials Engineering and Performance, 15:102-110, Feb 2006. URL: https://doi.org/10.1361/105994906x83466, doi:10.1361/105994906x83466. This article has 19 citations and is from a peer-reviewed journal.

4. (kostov2005selectionofcrucible pages 1-5): A. Kostov and B. Friedrich. Selection of crucible oxides in molten titanium and titanium aluminum alloys by thermo-chemistry calculations. Journal of Mining and Metallurgy, Section B, 41:113-125, Jan 2005. URL: https://doi.org/10.2298/jmmb0501113k, doi:10.2298/jmmb0501113k. This article has 42 citations.

5. (fedorov2021zirconiumdioxide.review pages 1-3): Pavel P. Fedorov and Evgeniya G. Yarotskaya. Zirconium dioxide. review. Kondensirovannye sredy i mezhfaznye granitsy = Condensed Matter and Interphases, 23:169-187, Jun 2021. URL: https://doi.org/10.17308/kcmf.2021.23/3427, doi:10.17308/kcmf.2021.23/3427. This article has 96 citations.

6. (mezbahulislam2013phaseequilibriumin pages 2-3): Mohammad Mezbahul-Islam and Mamoun Medraj. Phase equilibrium in mg-cu-y. Scientific Reports, Oct 2013. URL: https://doi.org/10.1038/srep03033, doi:10.1038/srep03033. This article has 14 citations and is from a peer-reviewed journal.

7. (mezbahulislam2013phaseequilibriumin pages 9-10): Mohammad Mezbahul-Islam and Mamoun Medraj. Phase equilibrium in mg-cu-y. Scientific Reports, Oct 2013. URL: https://doi.org/10.1038/srep03033, doi:10.1038/srep03033. This article has 14 citations and is from a peer-reviewed journal.

8. (nassar2025methodologyandtechnical pages 1-4): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

9. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.

10. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

11. (nassar2025methodologyandtechnical media 13b75bd1): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.
