<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: a1d1eede-9769-433a-9931-b31276d3db8e
- Submitted: 2026-10-17T18:58:51Z
- Fetched: 2026-10-17T19:30:31Z (status: success)
- Raw trajectory JSON: ../raw/el-09-Si.json.gz
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

ELEMENT UNDER REVIEW: Si (major seawater addition). Silicon bronze C65500 (2.8-3.8 Si), aluminum-silicon bronze C64200 (1.5-2.2 Si), Cu-Ni-Si Corson alloys (C70250, Ni2Si precipitates), silicon brass C87500; Si is also a deoxidizer and a weld-cracking concern in Cu-Ni.

Answer for Si specifically, not for copper alloys in general:
1. ROLE: what Si does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Si ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Si changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Si, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Si, Cu-Ni-Si and Cu-Al-Si are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Si in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Si neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Si | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Si (major seawater addition). Silicon bronze C65500 (2.8-3.8 Si), aluminum-silicon bronze C64200 (1.5-2.2 Si), Cu-Ni-Si Corson alloys (C70250, Ni2Si precipitates), silicon brass C87500; Si is also a deoxidizer and a weld-cracking concern in Cu-Ni.

Answer for Si specifically, not for copper alloys in general:
1. ROLE: what Si does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Si ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Si changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Si, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Si, Cu-Ni-Si and Cu-Al-Si are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Si in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Si neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Si | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Silicon (Si): composition-palette assessment

**Decision: INCLUDE, conditionally, in both families.** Silicon is a credible designed addition because commercial silicon and aluminum–silicon bronzes use it, small additions can alter brass dealloying, and Cu–Ni–Si alloys exploit both dissolved Si and nickel silicides. This is **not** evidence that an as-deposited Si-bearing repair will equal wrought C71500 in seawater. The proposed bounds are screening limits for *measured Si in the powder and deposit*, not qualified corrosion or weldability limits. In particular, a high-Si silicon-bronze composition must not be assumed compatible with C95800 or wrought Cu–Ni after dilution. [CITE] (kimstach2025siandmn pages 2-3, davies1993anoteon pages 4-5, li2025themicrostructuresand pages 9-11, marusic2010protectionofpatinated pages 17-26)

## 1. Metallurgical role and alloy precedents

In Cu-rich silicon bronze, Si can remain in the α-Cu solid solution, providing solid-solution strengthening; segregation can instead produce Cu–Si-rich phases. Silicon also serves as a melt deoxidizer and is associated with good castability and weldability. These are distinct mechanisms: a sound, deoxidized casting is not proof of a protective SiO₂ film in flowing seawater. In low-Al Cu–Al–Si–Mn cast bronze, an experiment spanning **0–2 wt% Si**, **3–9 wt% Al**, and **0–2 wt% Mn** reported single-phase structures; replacing Al with Si/Mn increased ductility but *decreased* tensile and yield strengths. That result cannot be transferred without testing to approximately 9–11 wt% Al, Ni/Fe-containing NAB. [CITE][NUMBERS] (kimstach2025siandmn pages 1-2, kimstach2025siandmn pages 2-3, kimstach2025siandmn pages 4-6)

In Corson-type Cu–Ni–Si, Si first strengthens dissolved α-Cu and, where processing permits, forms δ-Ni₂Si; Ni₃Si and, in Co-bearing compositions, (Ni,Co)₂Si are also reported. The frequently cited precipitation strengths follow **aging**, so they are not assured in the stipulated as-deposited condition. Ordinary marine Cu–Ni relies principally on its Cu-rich surface film and Ni/Fe alloying rather than a demonstrated Si-specific seawater mechanism. Conventional NAB κ phases are principally Fe–Al- and Ni–Al-bearing: observing more κ in an Si-added NAB does not establish a silicon-containing κ phase. [CITE] (li2025themicrostructuresand pages 4-6, li2025themicrostructuresand pages 9-11)

**Specification audit.** [SPEC] The project’s stated UNS/CDA precedents are wrought silicon bronze **C65500, 2.8–3.8 wt% Si**, and aluminum–silicon bronze **C64200, 1.5–2.2 wt% Si**; a source independently identifies C64200/AMS 4634 and cast **C95600** as roughly **2 wt% Si, 7 wt% Al**, and a separate source describes silicon bronze as approximately **3 wt% Si, 1 wt% Mn**. C70250 (Corson Cu–Ni–Si) and cast C87500 (silicon brass) are relevant families, but their controlling edition-specific Si ranges were **not verified** in the retrieved standard text; neither should be assigned a fabricated range. Likewise, no verified Si limit for **C95800, C70600, C71500**, ASTM **B111/B171/B466/B148/B369**, MIL-T-16420, MIL-B-24480, MIL-C-15726, EN 12449, or AWS A5.7 **ERCuNi, ERCuAl-A2, ERCuNiAl, ERCuMnNiAl** was obtained here. Do not treat the C65500/C64200 values as a citation to an uninspected ASTM edition or assume their permitted impurity limits apply to a novel powder. [NAVY][GAP] (kimstach2025siandmn pages 2-3, marusic2010protectionofpatinated pages 17-26)

For tin bronze, gunmetal and Cu–Ni–Sn, Si may be proposed as a deoxidizing/minor alloying addition, but a controlled Si-dependent marine corrosion benefit or defensible composition interval was **not established** in the retrieved evidence. Leaded gunmetal and phosphor bronze also present welding difficulties independent of Si. [GAP] (marusic2010protectionofpatinated pages 17-26)

## 2. Seawater corrosion: what the numbers actually show

* **Brass dealloying is composition- and phase-dependent, not monotonically improved by Si.** A Copper Development Association review reports that **0.33 wt% Si** in a leaded Cu–Zn brass produced a dezincification-susceptible duplex structure; silicon-rich precipitates in two approximately **3 wt% Si** arsenical leaded brasses were likewise associated with susceptibility. Other as-cast silicon brasses improved up to the highest tested **3.7 wt% Si**, whereas **0.5 wt% Si** reportedly retarded dezincification in duplex 60/40 brass but could initiate preferential attack at silicon-rich particles in an α-brass. These are brass-specific dealloying observations, **not** proof that 0.5–3.7 wt% Si improves NAB or Cu–Ni in seawater. [CITE][NUMBERS] Davies, *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions*, Copper Development Association (1993; no DOI identified). (davies1993anoteon pages 1-3, davies1993anoteon pages 4-5)
* **A nominal Si–NAB experiment is not reliable enough to set a corrosion optimum.** Dongo *et al.* report a no-added-Si corrosion rate of **5.4962 mm/y** and a claimed minimum of about **9.87 × 10⁻⁵ mm/y** in **3.5 wt% NaCl**, after cold deformation and **450 °C/60 min annealing**. However, the purported **0, 2, 4, 6, 8, 10 wt%** Si series is tabulated as measured **0, 0.16, 0.32, 0.48, 0.64, 0.80 wt% Si**; the alleged “2 wt%” optimum is inconsistently labeled X2 (elsewhere nominal 4 wt%); some reported corrosion rates and current densities are *negative*. Its charge also used scrap. The dramatic minimum therefore cannot establish a **2 wt% measured-Si** optimum, nor predict untreated DED corrosion. [CITE][NUMBERS][GAP] Dongo *et al.*, *FUOYE Journal of Engineering and Technology* **9**, 117–123 (2024), DOI: **10.4314/fuoyejet.v9i1.18**. (dongo2024quantitativeanalysisof pages 1-2, dongo2024quantitativeanalysisof pages 2-4, dongo2024quantitativeanalysisof pages 4-6, dongo2024quantitativeanalysisof pages 6-7)
* **C71500 comparison remains unproved.** A marine Cu–Ni review reports acceptable C70600 behavior up to about **3.0 m/s**, but this velocity observation is for conventional Cu–Ni, **not a Si-induced improvement** or a limit for the proposed deposit. No defensible Si-controlled C71500-versus-deposit corrosion-rate difference, ΔE_corr, film resistance, pitting/crevice depth, or Si-specific impingement-velocity limit was found. Test these endpoints, including the 30-day maximum selective-attack depth, on both undiluted builds and each repair interface. [NAVY][GAP] Lewis and LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, OSTI (1981), DOI: **10.2172/6255887**. (lewis1981evaluationofcoppernickel pages 1-7, lewis1981evaluationofcoppernickel pages 7-10)

## 3. DED, welding and powder production

[CITE][NUMBERS] An AM review reports that Cu–Ni–Si variants processed by **laser powder-bed fusion**, using **5–25 μm** powder and **10–15 μm** layers, achieved **<1.5% porosity**, against **25%** reported for its pure-Cu comparator. This is a *combined Ni/Si/process/powder-size comparison*, not an isolated Si effect and not blown-powder DED. The same review describes **blended CuNi₂SiCr and Al–Mg–Si powders** in laser DED; Al variation controlled the reported corrosion trend. Neither example qualifies a **single-stream, pre-alloyed Si** powder or as-deposited C71500-equivalent seawater performance. [GAP] Canacoo *et al.*, *International Journal of Precision Engineering and Manufacturing–Green Technology* (2026), DOI: **10.1007/s40684-026-00928-z**. (canacoo2026laseradditivemanufacturing pages 10-12, canacoo2026laseradditivemanufacturing pages 12-14)

[CITE] Welding experience makes silicon bronze a plausible weldable starting point, but a bronze-welding discussion warns that restrained single-phase deposits can crack in weld metal or heat-affected zones, while porosity requires rigorous cleaning and preheat/interpass temperatures must be controlled. Silicon segregation into the last liquid, re-melting of segregated interlayer regions, oxide inclusions, or dilution-generated Ni–Si and Al–Si phases are **testable cracking/porosity hypotheses**, not established failure thresholds for Si-bearing Cu–Ni or C95800 DED. A Brookhaven Ni–Cu **Monel 400** report quotes a **0.50 wt% Si maximum under MIL-N-24106**; its cracking investigation did *not* establish Si as the cause, and this Ni-rich specification must **not** be represented as an ERCuNi or C71500 Si limit. [SPEC][GAP] Czajkowski and Butters, Brookhaven report BNL-52651 (2001), DOI: **10.2172/791763**. (marusic2010protectionofpatinated pages 17-26, czajkowski2001investigationinhardsurfacing pages 8-11)

For approximately **0.5 kg** induction charges, the practical concerns are Si uptake versus loss on melting, SiO₂-bearing skins/inclusions under imperfect argon shielding, entrained ceramic, and composition drift between charge, atomized powder and laser deposit. Determine O and Si analytically at **all three stages** and examine alumina-versus-zirconia crucibles and the actual Ti-alloy-versus-Mo sonotrode by witness coupons/chemical analysis. A related Cu/SiC thermal-spray experiment observed silicide formation and porosity near decomposed SiC, but is **not** evidence that these particular atomizer ceramics or sonotrodes react at the same rate. No measured Si evaporation fraction, Si-dependent surface tension, or crucible/sonotrode contamination rate for this apparatus was retrieved; avoid assigning one. [GAP] Kang and Kang, *Materials Science and Engineering A* **428**, 336–345 (2006), DOI: **10.1016/j.msea.2006.05.054**. (kang2006thermaldecompositionof pages 1-2)

## 4. Phase limits and CALPHAD

[CITE][NUMBERS] The maximum binary α-Cu solubility is approximately **5.25 wt% Si near 842–852 °C**; it is a **high-temperature** maximum, not permission to retain that much as one phase at room temperature or in Ni/Al-containing alloys. Independent phase-diagram assessments identify Cu₃Si polymorphs, Cu₁₅Si₄, Cu₃₃Si₇ and high-temperature bcc/hcp phases. The 2024 assessment places a Cu-rich peritectic near **848.6 °C** and subsequent Cu-rich reaction near **839.4 °C**. Figure 4 of that assessment shows that adding Si on the Cu-rich side **depresses**, rather than raises, the binary-Cu liquidus from pure Cu; thus Si alone is not a reason to predict a liquidus **>1,250 °C**. Whether a particular Ni/Fe/Al-rich multicomponent candidate exceeds the atomizer’s approximately **1,200–1,250 °C** useful limit needs its *calculated and measured* liquidus. [GAP] McCloskey *et al.*, *Gold Bulletin* **34**, 3–13 (2001), DOI: **10.1007/bf03214802**; Kroupa *et al.*, *Journal of Phase Equilibria and Diffusion* **45**, 1206–1243 (2024), DOI: **10.1007/s11669-024-01160-5**. (mccloskey2001siliconmicrosegregationin pages 2-4, kroupa2024calphadtypereassessmentof pages 6-7, kroupa2024calphadtypereassessmentof pages 3-6, kroupa2024calphadtypereassessmentof media 118e7dd4, kroupa2024calphadtypereassessmentof media c5172161)

[CITE] **Cu–Si and Al–Cu–Si have published thermodynamic assessments**: Kroupa *et al.* provide phase models and Gibbs-energy parameters, including an assessed Al–Cu–Si ternary, suitable for independent implementation *after checking model completeness and compatibility*. An earlier COST**507** Cu–Si description is cited in that paper; do **not** silently relabel it COST **531**. Neither the retrieved material nor an inspected TCCU release verifies which ternaries or parameters are actually installed in the PI’s **TCCU version**, or provides a validated **Cu–Ni–Si–Al–Fe–Mn** joint assessment. Verify the version and phase list before relying on Thermo-Calc/pycalphad equilibrium, Scheil or liquidus output. [GAP] Kroupa *et al.* (2024), DOI: **10.1007/s11669-024-01160-5**. (kroupa2024calphadtypereassessmentof pages 1-3, kroupa2024calphadtypereassessmentof pages 3-6, kroupa2024calphadtypereassessmentof pages 37-38, kroupa2024calphadtypereassessmentof pages 7-8, kroupa2024calphadtypereassessmentof pages 25-26, kroupa2024calphadtypereassessmentof pages 16-20)

## 5. Supply, safety, bounds and coupled constraints

[NAVY][CITE] USGS recommended adding silicon to the **2025** US critical-minerals list; a subsequent USGS account explicitly lists **silicon on the final 2025 list**. Its description of the addition indicates it was not on the earlier list, although the original **2022 final-list notice was not directly inspected** here. No defensible contemporaneous **metallic Si purchase price in USD/kg**, OSHA exposure limit applicable specifically to this powder/fume, RoHS/REACH Si prohibition, or Navy elemental-Si restriction was established; a commodity quote and applicable SDS/OSHA particulate and welding-fume rules should be checked before assigning numbers. Elemental bulk-Si toxicity is not a substitute for evaluating respirable Cu/Ni-bearing powder, airborne laser oxides and combustible-fine-powder controls. [GAP] Nassar *et al.*, USGS Open-File Report **2025-1047** (2025), DOI: **10.3133/ofr20251047**. (nassar2025methodologyandtechnical pages 33-35, staff2022usgsminingreview pages 6-9)

**Proposed screening bounds, all measured wt% Si, Cu balance.** [NUMBERS] **Functional floor: 0.5 wt%** for exploratory *both-family* screening, justified only as the smallest retrieved Si dose with a reported dealloying response (**in brass**); the floor for an independently measurable improvement in as-deposited Cu–Ni or NAB is **unknown**. **Conservative maximum: 2.0 wt%** for the *Al-bronze branch* (upper end of the cast low-Al Cu–Al–Si–Mn experiment, approximately consistent with the C64200/C95600 precedent); **do not apply it automatically to high-Al C95800**. For the *Cu–Ni branch*, treat approximately **≤1.0 wt%** as an **exploratory sub-cap**, rather than an established marine/welding specification: the retrieved Cu–Ni–Co–Si review says Si is *usually below 1.5 wt%*, predominantly for age-hardened electrical alloys. **Non-conservative maximum: 3.8 wt%**, *only for a separate silicon-bronze/low-Al Al-bronze exploration*, from the stated C65500 upper endpoint; it is **not** justified as a Cu–Ni or cast-NAB repair bound. At either upper limit, failure to watch for includes Si-rich segregation/intermetallics, reheated-layer cracking, phase-selective corrosion and unacceptable dilution; the floor fails if oxidation/processing scatter overwhelms a small measured benefit. As this is an **INCLUDE** verdict, an impurity-only maximum is **not applicable**. (kimstach2025siandmn pages 1-2, kimstach2025siandmn pages 2-3, davies1993anoteon pages 4-5, li2025themicrostructuresand pages 9-11, marusic2010protectionofpatinated pages 17-26)

**Joint constraints to calculate, not assume.** [CITE][GAP] Vary **Ni:Si** around the Ni₂Si stoichiometric mass ratio of approximately **4.18:1** (2 × 58.69/28.09) while measuring whether Si remains dissolved after DED; excess Si or Ni can move the phase balance. Hold **Al–Si–Mn** jointly because the demonstrated single-phase cast domain traded lower Al against added Si/Mn. Evaluate Si alongside **Fe and Ni** in NAB because their κ phases and galvanic response, rather than Si alone, govern selective attack. Keep **Zn/Pb and α/β fractions** explicit when using silicon-brass dealloying precedents. For each first layer, calculate both powder and dilution-weighted local compositions and use cross-sectional chemistry, crack inspection and site-specific 30-day attack depth: composition averaged over the entire deposit can conceal a susceptible interface. (li2025themicrostructuresand pages 4-6, davies1993anoteon pages 4-5, li2025themicrostructuresand pages 9-11, kimstach2025siandmn pages 4-6)

**Evidence grade: thin for the proposed application.** The phase equilibria and existence of weldable silicon bronzes are comparatively well supported, but the decisive experiment—**pre-alloyed, single-stream blown-powder laser DED, as deposited, tested against wrought C71500 on self, C95800 and wrought Cu–Ni, with Si alone varied**—was not found. The only retrieved quantitative Si–NAB saline comparison is internally inconsistent, while LPBF and brass results answer materially different questions. (dongo2024quantitativeanalysisof pages 1-2, dongo2024quantitativeanalysisof pages 2-4, canacoo2026laseradditivemanufacturing pages 10-12, davies1993anoteon pages 4-5)

VERDICT | Si | decision=INCLUDE | family=both | conservative_max_wt=2.0 | nonconservative_max_wt=3.8 | floor_wt=0.5 | impurity_max_wt=NA | evidence=thin

References

1. (kimstach2025siandmn pages 2-3): T. V Kimstach, K. I Uzlov, O. P Bilyi, and S. I Repyakh. Si and mn effect on mechanical properties and linear shrinking of non-magnetic cu-al system cast bronzes. Naukovyi Visnyk Natsionalnoho Hirnychoho Universytetu, pages 113-120, Apr 2025. URL: https://doi.org/10.33271/nvngu/2025-2/113, doi:10.33271/nvngu/2025-2/113. This article has 0 citations.

2. (davies1993anoteon pages 4-5): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

3. (li2025themicrostructuresand pages 9-11): Fang Li, Wenteng Liu, Chao Ding, Shujuan Wang, and Xiangpeng Meng. The microstructures and properties of cu-ni-co-si alloys: a critical review. Metals, 15:564, May 2025. URL: https://doi.org/10.3390/met15050564, doi:10.3390/met15050564. This article has 16 citations.

4. (marusic2010protectionofpatinated pages 17-26): K Marušić. Protection of patinated bronze by non-toxic inhibitors. Unknown journal, 2010.

5. (kimstach2025siandmn pages 1-2): T. V Kimstach, K. I Uzlov, O. P Bilyi, and S. I Repyakh. Si and mn effect on mechanical properties and linear shrinking of non-magnetic cu-al system cast bronzes. Naukovyi Visnyk Natsionalnoho Hirnychoho Universytetu, pages 113-120, Apr 2025. URL: https://doi.org/10.33271/nvngu/2025-2/113, doi:10.33271/nvngu/2025-2/113. This article has 0 citations.

6. (kimstach2025siandmn pages 4-6): T. V Kimstach, K. I Uzlov, O. P Bilyi, and S. I Repyakh. Si and mn effect on mechanical properties and linear shrinking of non-magnetic cu-al system cast bronzes. Naukovyi Visnyk Natsionalnoho Hirnychoho Universytetu, pages 113-120, Apr 2025. URL: https://doi.org/10.33271/nvngu/2025-2/113, doi:10.33271/nvngu/2025-2/113. This article has 0 citations.

7. (li2025themicrostructuresand pages 4-6): Fang Li, Wenteng Liu, Chao Ding, Shujuan Wang, and Xiangpeng Meng. The microstructures and properties of cu-ni-co-si alloys: a critical review. Metals, 15:564, May 2025. URL: https://doi.org/10.3390/met15050564, doi:10.3390/met15050564. This article has 16 citations.

8. (davies1993anoteon pages 1-3): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

9. (dongo2024quantitativeanalysisof pages 1-2): Isaac Dongo, Joseph Omotoyinbo, Akinlabi Oyetunji, and Oloruntoba Daniel. Quantitative analysis of silicon influence and deformation impact on the mechanical and corrosion characteristics of nickel aluminium bronze (nab) alloy. FUOYE Journal of Engineering and Technology, 9:117-123, May 2024. URL: https://doi.org/10.4314/fuoyejet.v9i1.18, doi:10.4314/fuoyejet.v9i1.18. This article has 1 citations.

10. (dongo2024quantitativeanalysisof pages 2-4): Isaac Dongo, Joseph Omotoyinbo, Akinlabi Oyetunji, and Oloruntoba Daniel. Quantitative analysis of silicon influence and deformation impact on the mechanical and corrosion characteristics of nickel aluminium bronze (nab) alloy. FUOYE Journal of Engineering and Technology, 9:117-123, May 2024. URL: https://doi.org/10.4314/fuoyejet.v9i1.18, doi:10.4314/fuoyejet.v9i1.18. This article has 1 citations.

11. (dongo2024quantitativeanalysisof pages 4-6): Isaac Dongo, Joseph Omotoyinbo, Akinlabi Oyetunji, and Oloruntoba Daniel. Quantitative analysis of silicon influence and deformation impact on the mechanical and corrosion characteristics of nickel aluminium bronze (nab) alloy. FUOYE Journal of Engineering and Technology, 9:117-123, May 2024. URL: https://doi.org/10.4314/fuoyejet.v9i1.18, doi:10.4314/fuoyejet.v9i1.18. This article has 1 citations.

12. (dongo2024quantitativeanalysisof pages 6-7): Isaac Dongo, Joseph Omotoyinbo, Akinlabi Oyetunji, and Oloruntoba Daniel. Quantitative analysis of silicon influence and deformation impact on the mechanical and corrosion characteristics of nickel aluminium bronze (nab) alloy. FUOYE Journal of Engineering and Technology, 9:117-123, May 2024. URL: https://doi.org/10.4314/fuoyejet.v9i1.18, doi:10.4314/fuoyejet.v9i1.18. This article has 1 citations.

13. (lewis1981evaluationofcoppernickel pages 1-7): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

14. (lewis1981evaluationofcoppernickel pages 7-10): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

15. (canacoo2026laseradditivemanufacturing pages 10-12): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

16. (canacoo2026laseradditivemanufacturing pages 12-14): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

17. (czajkowski2001investigationinhardsurfacing pages 8-11): C. CZAJKOWSKI and M. BUTTERS. Investigation in hardsurfacing a nickel-copper alloy (monel400). ArXiv, Dec 2001. URL: https://doi.org/10.2172/791763, doi:10.2172/791763. This article has 5 citations.

18. (kang2006thermaldecompositionof pages 1-2): Hyun-Ki Kang and Suk Bong Kang. Thermal decomposition of silicon carbide in a plasma-sprayed cu/sic composite deposit. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 428:336-345, Jul 2006. URL: https://doi.org/10.1016/j.msea.2006.05.054, doi:10.1016/j.msea.2006.05.054. This article has 133 citations.

19. (mccloskey2001siliconmicrosegregationin pages 2-4): John C McCloskey, Shankar Aithal, and Paul R Welch. Silicon microsegregation in 14k yellow gold yellow gold. Gold Bulletin, 34:3-13, Mar 2001. URL: https://doi.org/10.1007/bf03214802, doi:10.1007/bf03214802. This article has 20 citations and is from a peer-reviewed journal.

20. (kroupa2024calphadtypereassessmentof pages 6-7): Ales Kroupa, Ondrej Zobac, Adela Zemanova, and Klaus W. Richter. Calphad-type reassessment of cu-si and full assessment of the al-cu-si systems. Journal of Phase Equilibria and Diffusion, 45:1206-1243, Dec 2024. URL: https://doi.org/10.1007/s11669-024-01160-5, doi:10.1007/s11669-024-01160-5. This article has 5 citations and is from a peer-reviewed journal.

21. (kroupa2024calphadtypereassessmentof pages 3-6): Ales Kroupa, Ondrej Zobac, Adela Zemanova, and Klaus W. Richter. Calphad-type reassessment of cu-si and full assessment of the al-cu-si systems. Journal of Phase Equilibria and Diffusion, 45:1206-1243, Dec 2024. URL: https://doi.org/10.1007/s11669-024-01160-5, doi:10.1007/s11669-024-01160-5. This article has 5 citations and is from a peer-reviewed journal.

22. (kroupa2024calphadtypereassessmentof media 118e7dd4): Ales Kroupa, Ondrej Zobac, Adela Zemanova, and Klaus W. Richter. Calphad-type reassessment of cu-si and full assessment of the al-cu-si systems. Journal of Phase Equilibria and Diffusion, 45:1206-1243, Dec 2024. URL: https://doi.org/10.1007/s11669-024-01160-5, doi:10.1007/s11669-024-01160-5. This article has 5 citations and is from a peer-reviewed journal.

23. (kroupa2024calphadtypereassessmentof media c5172161): Ales Kroupa, Ondrej Zobac, Adela Zemanova, and Klaus W. Richter. Calphad-type reassessment of cu-si and full assessment of the al-cu-si systems. Journal of Phase Equilibria and Diffusion, 45:1206-1243, Dec 2024. URL: https://doi.org/10.1007/s11669-024-01160-5, doi:10.1007/s11669-024-01160-5. This article has 5 citations and is from a peer-reviewed journal.

24. (kroupa2024calphadtypereassessmentof pages 1-3): Ales Kroupa, Ondrej Zobac, Adela Zemanova, and Klaus W. Richter. Calphad-type reassessment of cu-si and full assessment of the al-cu-si systems. Journal of Phase Equilibria and Diffusion, 45:1206-1243, Dec 2024. URL: https://doi.org/10.1007/s11669-024-01160-5, doi:10.1007/s11669-024-01160-5. This article has 5 citations and is from a peer-reviewed journal.

25. (kroupa2024calphadtypereassessmentof pages 37-38): Ales Kroupa, Ondrej Zobac, Adela Zemanova, and Klaus W. Richter. Calphad-type reassessment of cu-si and full assessment of the al-cu-si systems. Journal of Phase Equilibria and Diffusion, 45:1206-1243, Dec 2024. URL: https://doi.org/10.1007/s11669-024-01160-5, doi:10.1007/s11669-024-01160-5. This article has 5 citations and is from a peer-reviewed journal.

26. (kroupa2024calphadtypereassessmentof pages 7-8): Ales Kroupa, Ondrej Zobac, Adela Zemanova, and Klaus W. Richter. Calphad-type reassessment of cu-si and full assessment of the al-cu-si systems. Journal of Phase Equilibria and Diffusion, 45:1206-1243, Dec 2024. URL: https://doi.org/10.1007/s11669-024-01160-5, doi:10.1007/s11669-024-01160-5. This article has 5 citations and is from a peer-reviewed journal.

27. (kroupa2024calphadtypereassessmentof pages 25-26): Ales Kroupa, Ondrej Zobac, Adela Zemanova, and Klaus W. Richter. Calphad-type reassessment of cu-si and full assessment of the al-cu-si systems. Journal of Phase Equilibria and Diffusion, 45:1206-1243, Dec 2024. URL: https://doi.org/10.1007/s11669-024-01160-5, doi:10.1007/s11669-024-01160-5. This article has 5 citations and is from a peer-reviewed journal.

28. (kroupa2024calphadtypereassessmentof pages 16-20): Ales Kroupa, Ondrej Zobac, Adela Zemanova, and Klaus W. Richter. Calphad-type reassessment of cu-si and full assessment of the al-cu-si systems. Journal of Phase Equilibria and Diffusion, 45:1206-1243, Dec 2024. URL: https://doi.org/10.1007/s11669-024-01160-5, doi:10.1007/s11669-024-01160-5. This article has 5 citations and is from a peer-reviewed journal.

29. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

30. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.
