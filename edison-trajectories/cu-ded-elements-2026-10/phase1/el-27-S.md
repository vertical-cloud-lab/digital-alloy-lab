<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: f460e55f-026d-422c-839b-fb279ee3a944
- Submitted: 2026-10-17T19:00:10Z
- Fetched: 2026-10-17T19:33:10Z (status: success)
- Raw trajectory JSON: ../raw/el-27-S.json.gz
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

ELEMENT UNDER REVIEW: S (impurity / free-machining). Sulfur copper C14700; Cu-Ni specifications limit S to about 0.02 wt% for welding; hot cracking. (Sulfide in polluted seawater is a separate issue: answer for S in the alloy, and mention the polluted-water effect only briefly.)

Answer for S specifically, not for copper alloys in general:
1. ROLE: what S does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their S ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how S changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-S, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-S, Cu-Ni-S and Cu-Al-S are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of S in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that S neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | S | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: S (impurity / free-machining). Sulfur copper C14700; Cu-Ni specifications limit S to about 0.02 wt% for welding; hot cracking. (Sulfide in polluted seawater is a separate issue: answer for S in the alloy, and mention the polluted-water effect only briefly.)

Answer for S specifically, not for copper alloys in general:
1. ROLE: what S does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their S ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how S changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-S, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-S, Cu-Ni-S and Cu-Al-S are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of S in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that S neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | S | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Sulfur (S): composition-palette assessment

**Decision: LIMIT S as an impurity in both Cu–Ni and aluminum-bronze candidates.** Set **S ≤0.010 wt% (100 ppm)** in both the atomized powder and the as-deposited metal, with **≤0.005 wt% (50 ppm) as a procurement target**, not a demonstrated cracking threshold. The 0.010 wt% ceiling is a conservative project control: commercial-purity Cu–10Ni in one hot-ductility study contained 0.0051 wt% S, and its complex Cu–Ni comparison alloys contained 0.006–0.007 wt% S. That study does **not** show that 0.010 wt% is a safe DED limit; its unusually favorable result for S added alone cannot establish seawater performance or repair-interface integrity. Analyze S after atomization and deposition rather than assuming the charged amount survives. (gavin1978effectoftrace pages 1-2, gavin1978effectoftrace pages 2-3, gavin1978effectoftrace pages 4-5)

## 1. Role, alloy families, and documented limits

[CITE][NUMBERS] In copper, S is principally a **low-solubility sulfide former**, not a useful Cu-matrix solid-solution strengthener. A thermodynamic evaluation predicts **Cu₂S** precipitation and identifies S among copper-embrittling impurities. Sulfur in free-machining copper improves chip breaking through dispersed second-phase particles; it is not established as a seawater-film former, deoxidizer, grain refiner, or inhibitor of dezincification or other dealloying. A U.S. Bureau of Mines review explicitly distinguishes S/Se/Te additions for *machinability* from additions used for *dealloying resistance*. No benefit from intentional S additions was established for seawater-service Cu–Ni, aluminum bronze/NAB, Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si. The sulfides that might form in multicomponent compositions require phase identification rather than assignment from the binary alone. (riley1986impurityeffectsin pages 1-3, magnusson2017thermodynamicevaluationof pages 1-9, magnusson2017thermodynamicevaluationof pages 14-16, magnusson2017thermodynamicevaluationof pages 16-21)

[SPEC][NUMBERS] **Verified numerical examples, with their scope:** ASTM/UNS **C10100 oxygen-free copper** permits **S ≤0.0015 wt% (15 ppm)**; the separate Swedish OFP-copper canister requirement cited in the same technical report is **<0.0012 wt% (12 ppm)**. **MIL-N-24106 Monel 400**—a *Ni-base* Cu–Ni alloy, **not** C71500—specifies **S ≤0.015 wt%** in the Brookhaven report. These are useful cleanliness comparators, not interchangeable requirements for NAB or ERCuNi. Cu–10Ni material analyzed by Gavin *et al.* contained 0.0015 wt% S in the high-purity heat and 0.0051 wt% in the commercial-purity heat. The retrieved source identifying **C14700 sulfur copper** supports its free-machining role but did **not** establish a verifiable numerical C14700 S range; none is asserted here. Nor was an S-specific limit verified here for **ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449**, or the requested NAB, Mn–Al-bronze, Cu–Ni–Sn and Cu–Ni–Si grades. An unspecified element limit or an alloy’s general impurity allowance must not be represented as an S specification. (czajkowski2001investigationinhardsurfacing pages 8-11, riley1986impurityeffectsin pages 1-3, magnusson2017thermodynamicevaluationof pages 9-12, gavin1978effectoftrace pages 1-2)

[CITE][NUMBERS] An important *counterexample to an absolute prohibition* is Gavin, Billingham, Chubb and Hancock, “Effect of trace impurities on hot ductility of as-cast cupronickel alloys,” *Metals Technology* **5** (1978) 397–401, **doi:10.1179/mt.1978.5.1.397**. In a **simple Cu–10 wt% Ni** alloy, separately added S was comparatively innocuous in their simulated-TIG-cycle tensile test **up to 0.075 wt% (750 ppm)**. This does not qualify that composition for seawater immersion, actual weld-crack freedom, or the more complex NAB/Cu–Ni design space. The authors explicitly found stronger impurity interactions in a complex **Cu–11Ni–8.5Mn–5.6Fe–1.35Al–0.2Ti–0.1Si** alloy. (gavin1978effectoftrace pages 1-2, gavin1978effectoftrace pages 2-3, gavin1978effectoftrace pages 4-5)

## 2. Seawater corrosion: what can and cannot be quantified

[GAP] **No defensible S-in-alloy dose–response** was located for seawater, ASTM D1141 substitute water, or 3.5 wt% NaCl in these alloy families. Consequently there is **no established beneficial S range**, and no attributable numerical change in *E*₍corr₎, corrosion rate, impedance/film resistance, maximum selective-attack depth, pit or crevice depth, or erosion–corrosion velocity limit. In particular, a sulfide detected *on a corroded specimen* does not demonstrate that S originally in the powder improved its film. A reported **3.0 m/s** seawater-flow performance for C70600 is an **alloy-level** observation, not an S-dependent velocity limit: Lewis and LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications* (1981), **doi:10.2172/6255887**. (riley1986impurityeffectsin pages 1-3, magnusson2017thermodynamicevaluationof pages 14-16, magnusson2017thermodynamicevaluationof pages 16-21, beaver1978stateoftheartsurveyof pages 44-48)

[CITE][GAP] Keep **S in the alloy** distinct from **sulfide already in polluted water**. Environmental sulfide can replace protective oxide with a less protective sulfide-rich surface film; Gao and Liu report **0.15 mm/year initially**, declining to approximately **0.09 mm/year after 168 h**, for C71500 in their *high-sulfide simulated seawater*, **not** for deliberately S-alloyed C71500: “Corrosion Behavior of High-Strength C71500 Copper-Nickel Alloy in Simulated Seawater with High Concentration of Sulfide,” *Materials* **15** (2022) 8513, **doi:10.3390/ma15238513**. Neither value can set an alloy-S bound. (smith2007thecorrosionand pages 73-77, phull20172.18–marine pages 25-27)

## 3. DED, welding, and repair dilution

[CITE][NUMBERS][NAVY] The strongest directly relevant welding surrogate is the **modified-Gleeble, cooling-leg simulated TIG cycle**, *not* a laser-DED cracking test, in Gavin *et al.* Their Cu–10Ni specimens had an approximately **850–1100 K** intergranular ductility trough. Isolated S was less harmful than Bi, Te, Pb or Se, but combinations were cumulative. Their exploratory impurity index, with every input in **ppm by mass**, was **BiE = Bi + 0.7Te + 0.4Pb + 0.2Se + 0.1S**. It ranks simple-alloy hot-ductility risk; the authors caution that it is not quantitatively transferable to complex precipitation-hardened Cu–Ni. The study used an alloy supplied by an Admiralty dockyard laboratory; it did **not** measure DED crack incidence. (gavin1978effectoftrace pages 1-2, gavin1978effectoftrace pages 3-4, gavin1978effectoftrace pages 4-5)

[CITE][GAP] A separate **brazing**, rather than DED, source warns that Cu–Ni base material should be free of S or Pb because either can cause cracking during the brazing cycle. It also describes **0.20–0.50 wt% Ti** in historical RCuNi/ECuNi filler as a **deoxidizer and porosity-control addition**; those are *Ti* concentrations, **not S limits or evidence that S deoxidizes copper**. Beaver, *State-of-the-Art Survey of Joinability of Materials for OTEC Heat Exchangers*, ORNL/TM-6284 (1978), **doi:10.2172/6523751**. A reported Monel 400 hard-surfacing failure involved intergranular fractures and Mg/Ca/S-bearing features, but its investigators explicitly **did not establish S as the cause**: Czajkowski and Butters, *Investigation in Hardsurfacing a Nickel-Copper Alloy (Monel 400)* (2001), **doi:10.2172/791763**. (czajkowski2001investigationinhardsurfacing pages 8-11, beaver1978stateoftheartsurveyof pages 39-44)

[GAP] For single-stream DED, **terminal sulfide segregation and an extended final-freezing interval are plausible solidification-crack mechanisms**; reheating an S-enriched interface could plausibly permit local liquation, and S-bearing surface contamination could contribute to pores or inclusions. These remain **hypotheses for the specified powder, laser, cast C95800, and wrought Cu–Ni**: no sulfur-controlled DED/ERCuAl-A2/ERCuNiAl/ERCuMnNiAl comparison located here establishes their incidence or thresholds. Measure transverse and reheated-layer cracks, pores, and S distribution through the dilution zones separately; cast-NAB base-metal segregation and Cu–Ni substrate cleanliness need separate controls. Do not relabel the above brazing caution as a measured laser-cladding result. (magnusson2017thermodynamicevaluationof pages 14-16, sineva2010studyofthe pages 1-2, gavin1978effectoftrace pages 1-2, beaver1978stateoftheartsurveyof pages 39-44)

## 4. Induction melting and ultrasonic atomization

[CITE][NUMBERS] Charged S need not equal retained S. In Gavin *et al.*, S was added as a **copper-sulfide charge wrapped in Cu foil explicitly to minimize vaporization loss**, in an **argon-protected alumina crucible**, and the investigators analyzed the resulting metal. That is direct support for controlling loss by measurement, but **not** a measured loss fraction for a 0.5 kg ultrasonic-atomization batch. Sineva *et al.* report increasing sulfur pressure over **high-S Cu–S melts**; those experiments concern compositions much richer in S than the proposed impurity limit. (sineva2010studyofthe pages 2-4, gavin1978effectoftrace pages 1-2)

[GAP] No measured reaction rate or contamination budget was found for S-bearing Cu–Ni/NAB melts against **alumina, zirconia, graphite, Ti-alloy or Mo sonotrodes**, nor an S-specific particle-size, oxygen-pickup, SO₂-fume, or retention curve for this machine. S is surface-active in molten Cu, so altered breakup is a **testable hypothesis**, not a demonstrated powder improvement; Baes and Kellogg, “Effect of dissolved sulphur on the surface tension of liquid copper,” *JOM* **5** (1953) 643–648, **doi:10.1007/BF03397527** (identified bibliographically; quantitative data not verified here). Screen crucible/sonotrode pickup, powder versus charge S and O, inclusions, morphology, and off-gas rather than assigning an invented evaporation or oxidation percentage. (sineva2010studyofthe pages 2-4, gavin1978effectoftrace pages 1-2)

## 5. Cu–S phase equilibria and CALPHAD

[CITE][NUMBERS] Sineva, Starykh and Zakhryapin, “Study of the Liquidus and Solidus Surfaces … Cu–Ni–S,” *Russian Metallurgy (Metally)* **2010** 448–455, **doi:10.1134/S0036029510050162**, report **S solubility in solid Cu ≈0.0001 wt% at 600 °C and ≈0.007 wt% at 1000 °C**. These are **two reported temperatures, not a verified global maximum**. Their Cu-rich binary has **L → Cu + Cu₂S at 1067 °C and 0.77 wt% S**, a **1105 ± 1 °C monotectic** associated with a liquid miscibility gap at much higher S, and Cu₂±xS melting at **1130 ± 1 °C**. The eutectic **0.77 wt% S is the composition of a *liquid***: it is emphatically **not solid solubility** or an allowable weld-powder addition. Trace S on the Cu-rich side does not, by itself, imply a liquidus above the **~1200–1250 °C** atomization limit; the *combined* Ni/Al/other-element liquidus still needs calculation and verification. (sineva2010studyofthe pages 1-2, sineva2010studyofthe pages 2-4)

[CITE][GAP] A published **Cu–H–O–S–P thermodynamic evaluation** is identified by Magnusson and Frisk, *Thermodynamic Evaluation of Cu–H–O–S–P System: Phase Stabilities and Solubilities for OFP-Copper*, SKB TR-13-11 (2013), cited in Magnusson, *Thermodynamic Evaluation of Impurity Elements in OFP Copper*, **SKB R-17-20** (2017; report without a verified DOI). The latter predicts Cu₂S in Cu and says P does not eliminate it. **Cu–Ni–S experimental phase-equilibrium work exists**, but its existence does not prove an assessed description in **Thermo-Calc TCCU**. The retrieved evidence does **not** verify TCCU version-specific S coverage, a **Cu–Al–S** assessment, **COST 531** coverage, or a distributable pycalphad `.tdb` with all necessary phases and parameters. Before committing to a S-containing calculation, inspect the installed database’s `ELEMENT`, `PHASE`, and parameter listings and reproduce the binary Cu–S anchors; report unsupported ternary extrapolation explicitly. (magnusson2017thermodynamicevaluationof pages 9-12, magnusson2017thermodynamicevaluationof pages 14-16, magnusson2017thermodynamicevaluationof pages 16-21, magnusson2017thermodynamicevaluationof pages 21-23, sineva2010studyofthe pages 1-2)

## 6. Supply, safety, interactions, and evidence quality

[GAP] No verified primary-list text or price quotation was retrieved establishing S’s exact entry status on the **2022** or **2025 final U.S. critical-minerals lists**, nor an auditable **USD/kg** S price; these should not be inferred from the stated critical status of Ni and Cu. No S-specific **RoHS/REACH article prohibition, Navy composition restriction, or OSHA limit for elemental S in this copper powder** was verified. Hazard assessment should distinguish elemental-S dust from **inhalable Cu/Ni-bearing powder and welding fume**, and from possible **SO₂ if S oxidizes**; use the applicable chemical SDS, combustible-dust assessment, local exhaust, and measured fume composition. Do not claim that ordinary sulfate in ASTM D1141 is an S-in-alloy exposure. (sineva2010studyofthe pages 2-4, gavin1978effectoftrace pages 1-2)

[CITE][NUMBERS] For a later joint-constraint screen, retain the empirical **BiE impurity sum above** and explicitly flag its **simple Cu–10Ni-only** calibration. The real phase competition between Cu₂S and sulfides involving **Ni, Mn, Fe, Ti, or Zr** needs evaluation at the selected Al/Ni contents; neither a fixed Mn:S neutralization ratio nor a permissible Fe:S or Ni:S ratio was established. In cast **tin bronzes/gunmetals**, a copper-alloy grain-refinement review reports that S **destroys the beneficial Zr refinement**, while Mg can restore it; this is a relevant interaction, not evidence that adding S refines grains: Sadayappan *et al.*, *Grain Refinement of Permanent Mold Cast Copper Base Alloys*, DOE report, **doi:10.2172/840819**. (m.sadayappan2005grainrefinementof pages 8-10, sineva2010studyofthe pages 2-4, gavin1978effectoftrace pages 4-5)

**Bound rationale and confidence.** [NUMBERS][GAP] **0.010 wt%** is a *chosen screening maximum* for powder **and** deposit, aimed at limiting sulfide-bearing heterogeneity and multielement/reheat risk while remaining near measured commercial Cu–Ni impurity levels; **0.005 wt%** is a stricter operational target. Neither is a Navy/ASTM/AWS sulfur limit for both families, a seawater-corrosion threshold, or a proven DED crack threshold. A useful high-purity sensitivity control is **≤0.0015 wt%**, the independently documented C10100 S maximum, although applying it to NAB is a research choice rather than a C95800 requirement. Gavin’s isolated-S **0.075 wt%** tolerance **contradicts an assertion that S inevitably cracks Cu–Ni at 0.020 wt%**; it does not contradict limiting S for untested multicomponent *as-deposited seawater* service. Evidence is **moderate for Cu–S equilibrium and simple-alloy hot-ductility ranking**, but **thin for the specified DED repair and S-dependent seawater endpoints**. (magnusson2017thermodynamicevaluationof pages 9-12, m.sadayappan2005grainrefinementof pages 8-10, gavin1978effectoftrace pages 1-2, gavin1978effectoftrace pages 4-5, beaver1978stateoftheartsurveyof pages 39-44, sineva2010studyofthe pages 2-4)

VERDICT | S | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.010 | evidence=thin

References

1. (gavin1978effectoftrace pages 1-2): S. A. Gavin, J. Billingham, J. P. Chubb, and P. Hancock. Effect of trace impurities on hot ductility of as-cast cupronickel alloys. Metals Technology, 5B:397-401, Jan 1978. URL: https://doi.org/10.1179/mt.1978.5.1.397, doi:10.1179/mt.1978.5.1.397. This article has 29 citations.

2. (gavin1978effectoftrace pages 2-3): S. A. Gavin, J. Billingham, J. P. Chubb, and P. Hancock. Effect of trace impurities on hot ductility of as-cast cupronickel alloys. Metals Technology, 5B:397-401, Jan 1978. URL: https://doi.org/10.1179/mt.1978.5.1.397, doi:10.1179/mt.1978.5.1.397. This article has 29 citations.

3. (gavin1978effectoftrace pages 4-5): S. A. Gavin, J. Billingham, J. P. Chubb, and P. Hancock. Effect of trace impurities on hot ductility of as-cast cupronickel alloys. Metals Technology, 5B:397-401, Jan 1978. URL: https://doi.org/10.1179/mt.1978.5.1.397, doi:10.1179/mt.1978.5.1.397. This article has 29 citations.

4. (riley1986impurityeffectsin pages 1-3): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

5. (magnusson2017thermodynamicevaluationof pages 1-9): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

6. (magnusson2017thermodynamicevaluationof pages 14-16): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

7. (magnusson2017thermodynamicevaluationof pages 16-21): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

8. (czajkowski2001investigationinhardsurfacing pages 8-11): C. CZAJKOWSKI and M. BUTTERS. Investigation in hardsurfacing a nickel-copper alloy (monel400). ArXiv, Dec 2001. URL: https://doi.org/10.2172/791763, doi:10.2172/791763. This article has 5 citations.

9. (magnusson2017thermodynamicevaluationof pages 9-12): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

10. (beaver1978stateoftheartsurveyof pages 44-48): R. J. Beaver. State-of-the-art survey of joinability of materials for otec heat exchangers. ArXiv, 80:10647, Dec 1978. URL: https://doi.org/10.2172/6523751, doi:10.2172/6523751. This article has 1 citations.

11. (smith2007thecorrosionand pages 73-77): JM Smith. The corrosion and electrochemistry of copper in aqueos, anoxic sulphide solutions. Unknown journal, 2007.

12. (phull20172.18–marine pages 25-27): B Phull and AA Abdullahi. 2.18 – marine corrosion. ArXiv, 2:1107-1148, Jan 2017. URL: https://doi.org/10.1016/b978-044452787-5.00046-9, doi:10.1016/b978-044452787-5.00046-9. This article has 61 citations.

13. (gavin1978effectoftrace pages 3-4): S. A. Gavin, J. Billingham, J. P. Chubb, and P. Hancock. Effect of trace impurities on hot ductility of as-cast cupronickel alloys. Metals Technology, 5B:397-401, Jan 1978. URL: https://doi.org/10.1179/mt.1978.5.1.397, doi:10.1179/mt.1978.5.1.397. This article has 29 citations.

14. (beaver1978stateoftheartsurveyof pages 39-44): R. J. Beaver. State-of-the-art survey of joinability of materials for otec heat exchangers. ArXiv, 80:10647, Dec 1978. URL: https://doi.org/10.2172/6523751, doi:10.2172/6523751. This article has 1 citations.

15. (sineva2010studyofthe pages 1-2): S. I. Sineva, R. V. Starykh, and S. B. Zakhryapin. Study of the liquidus and solidus surfaces in the quaternary fe-ni-cu-s system: iii. construction of a meltability diagram and determination of miscibility gap boundaries for the ternary cu-ni-s sulfide system. Russian Metallurgy (Metally), 2010:448-455, Sep 2010. URL: https://doi.org/10.1134/s0036029510050162, doi:10.1134/s0036029510050162. This article has 6 citations.

16. (sineva2010studyofthe pages 2-4): S. I. Sineva, R. V. Starykh, and S. B. Zakhryapin. Study of the liquidus and solidus surfaces in the quaternary fe-ni-cu-s system: iii. construction of a meltability diagram and determination of miscibility gap boundaries for the ternary cu-ni-s sulfide system. Russian Metallurgy (Metally), 2010:448-455, Sep 2010. URL: https://doi.org/10.1134/s0036029510050162, doi:10.1134/s0036029510050162. This article has 6 citations.

17. (magnusson2017thermodynamicevaluationof pages 21-23): H Magnusson. Thermodynamic evaluation of impurity elements in ofp copper. Unknown journal, 2017.

18. (m.sadayappan2005grainrefinementof pages 8-10): Grain Refinement of Permanent Mold Cast Copper Base Alloys This article has 58 citations.
