<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: e863848a-c917-4dad-af1a-4c69ce2190e2
- Submitted: 2026-10-17T19:00:18Z
- Fetched: 2026-10-17T19:33:13Z (status: success)
- Raw trajectory JSON: ../raw/el-30-H.json.gz
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

ELEMENT UNDER REVIEW: H (interstitial / gas). Hydrogen embrittlement (steam reaction with Cu2O) and porosity in Cu-Ni welds; moisture on powder. Answer as an impurity limit (ppm) and as a process control.

Answer for H specifically, not for copper alloys in general:
1. ROLE: what H does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their H ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how H changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-H, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-H, Cu-Ni-H and Cu-Al-H are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of H in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that H neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | H | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: H (interstitial / gas). Hydrogen embrittlement (steam reaction with Cu2O) and porosity in Cu-Ni welds; moisture on powder. Answer as an impurity limit (ppm) and as a process control.

Answer for H specifically, not for copper alloys in general:
1. ROLE: what H does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their H ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how H changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-H, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-H, Cu-Ni-H and Cu-Al-H are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of H in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that H neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | H | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# H — impurity limit and process control for marine copper-alloy DED

**Decision: LIMIT, for both Cu–Ni and aluminum-bronze development.** Hydrogen is not a defensible designed constituent of the proposed pre-alloyed powders. Interstitial H has very low, pressure-dependent solubility in solid Cu; H-bearing gas or moisture can instead produce pores, and H reacting with internal Cu₂O can produce damaging steam. A copper electron-beam-welding materials requirement specifies **H <1 weight ppm (0.0001 wt%)**, together with **O <5 weight ppm**. Adopt **H <1 weight ppm in both powder and as-deposited metal as a provisional acceptance target**, with **<0.6 weight ppm (0.00006 wt%) as a stretch target** drawn from oxygen-free phosphorus copper (OFP-Cu). Neither is an established DED qualification limit for C71500 or C95800: measure their achievability and relationship to defects rather than representing them as such. (robitz1990closuredevelopmentfor pages 36-37, magnusson2013selfdiffusionandimpurity pages 1-6, ledford2019characteristicsandprocessing pages 7-10)

## 1. Role and specified alloys

[CITE] H enters Cu-rich metal principally as a dilute, mobile **interstitial**, not as a strengthening, grain-refining or seawater-film-forming addition. In Cu–Cr–Zr, Cr-containing particles, Cu₄Zr precipitates and other defects can trap H; nanoscale Al₂O₃ traps it in dispersion-strengthened Cu. These are observations in *other copper materials*, not proof that Ni–Al bronze κ phases, Cu–Ni–Sn precipitates or Cu–Ni–Si precipitates beneficially retain H. Hydrogen is not the constituent responsible for protective Cu₂O/Ni-oxide films in Cu–Ni. Gaseous H₂ can reduce oxygen from molten copper to H₂O, but that **processing reaction does not make retained H a useful deoxidizing alloy addition**. (magnusson2013selfdiffusionandimpurity pages 1-6, romero2025thermochemicalaspectsof pages 8-12, li2023stresscorrosioncracking pages 8-10, pealva2012interactionofcopper pages 13-16)

[SPEC] **No designed H range in wt% was established** for the marine grades C70600, C71500, C95800, or the cited AWS A5.7 filler families ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl; nor for the requested tin bronzes/gunmetals, brasses, Mn–Al bronzes, Cu–Ni–Sn or Cu–Ni–Si. Accordingly, do **not** assign an H interval to ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726 or EN 12449 without the applicable edition and an actual H-analysis clause. The verified numerical *non-marine* precedents are SKB OFP-Cu **H <0.00006 wt%**, and the SKB-related copper electron-beam-weld material requirement **H <0.0001 wt%**; these must not be relabeled Navy specifications. (robitz1990closuredevelopmentfor pages 36-37, magnusson2013selfdiffusionandimpurity pages 1-6)

## 2. Seawater corrosion: what can and cannot be quantified

[GAP] No verified controlled comparison varied **retained alloy H in weight ppm** and measured corrosion rate, E_corr, impedance/film resistance, pit or crevice depth, dealloying, erosion–corrosion, or a velocity limit for Cu–Ni or NAB in seawater, ASTM D1141 water or 3.5 wt% NaCl. Consequently there is **no demonstrated helpful H-content range**, harmful *seawater-corrosion* threshold, or credible H-specific improvement relative to as-deposited C71500. Do not mistake solution hydrogen ions, H₂S concentration, cathodically generated H, or H in an external gas for specified H in the powder. A marine Cu–Ni review attributes normal corrosion protection to Cu₂O and Ni-derived oxide/hydroxide; it describes film rupture and selective dissolution—not routine H embrittlement—as prevailing Cu–Ni SCC mechanisms. (li2023stresscorrosioncracking pages 8-10, li2023stresscorrosioncracking pages 10-11)

[NUMBERS] A review tabulates Cu–10Ni in NaCl plus sulfide with approximately **97 h to failure at 100 ppm sulfide** versus **41 h at 1,000 ppm sulfide**, reporting an interpretation of anodic dissolution at lower sulfide and hydrogen-assisted cracking at higher sulfide. Another cited study found no SCC in chloride-plus-sulfide conditions; the review also reports severe Cu–30Ni SCC at **3,120 ppm sulfide**. These are **sulfide-environment/loaded-specimen results**, not H concentration in alloy, a clean-seawater H dose–response, or evidence that H improves corrosion. A separate OTEC assessment reports C70600 resistance up to **3.0 m/s seawater flow**, likewise **not an H-dependent velocity limit**. (li2023stresscorrosioncracking pages 11-12)

## 3. DED, welding and repair interfaces

[CITE][NUMBERS] The strongest powder-to-build warning is **Ledford et al., *Applied Sciences* 9 (2019) 3993, DOI:10.3390/app9193993**. After hydrogen treatment, oxygen-rich copper powder accumulated H and internal H₂O: medium-O powder rose **1.81 → 31.83 weight ppm H** while O fell **462.17 → 282.33 weight ppm**; high-O powder rose **1.95 → 76.44 weight ppm H** while O fell **1,507.33 → 586.97 weight ppm**. Low-O powder changed only **0.87 → 1.56 weight ppm H** while O fell **226.51 → 54.76 weight ppm**. Internal Cu₂O + H produced trapped steam, grain-boundary particle fracture on heating, bubbles and melt ejection. The study's **electron-beam powder-bed** successive remelting nevertheless yielded dense copper with approximately **50 weight ppm O and negligible residual H**: powder H, retained water and final-metal H must be measured separately. This is *not* evidence that argon-shielded, single-stream **laser DED** will expel steam equally well. (ledford2019characteristicsandprocessing pages 7-10, ledford2019characteristicsandprocessing pages 16-19, ledford2019characteristicsandprocessing media 37e413d8)

[NAVY][GAP] For the proposed repair builds, characterize the first diluted bead and reheated interface separately from bulk deposits. Oxygen/oxide- or moisture-bearing cast NAB and wrought Cu–Ni can introduce gas or oxide at their interfaces, while subsequent passes can expose trapped pores; these are **testable risks, not demonstrated substrate-specific H thresholds**. The copper electron-beam-weld report associates oxygen and hydrogen with weld defects and specifies **<1 weight ppm H, <5 weight ppm O**; it observes root porosity and warns that connected defects can create leakage paths. A separate dissimilar-welding review identifies **Fe pickup and P-associated brittle nickel phosphides** as Cu–Ni hot-cracking concerns. Thus **do not call H porosity evidence proof that H controls solidification cracking or reheated-layer liquation cracking**: those crack mechanisms require composition/dilution, thermal-cycle and metallographic tests. Filler experience is an analogy, not qualification of the candidate DED powders. (robitz1990closuredevelopmentfor pages 36-37, carlone2019dissimilarmetalwelding pages 13-14, carlone2019dissimilarmetalwelding pages 14-16, robitz1990closuredevelopmentfor pages 37-39)

## 4. Melting, ultrasonic atomization and controls

[CITE] In an induction melt under Ar, H is mainly a **gas-pressure, oxygen-activity and cleanliness variable**: wet feedstock, adsorbed powder moisture, damp refractories, leaky shielding or H-bearing process gas are plausible inputs. Hydrogen–oxygen reaction can make H₂O, rather than leaving a useful fixed H composition; liquid-copper deoxidation calculations explicitly represent H₂ + dissolved O → H₂O. Neither a measured H-induced liquidus change nor measured H effects on copper-alloy surface tension, evaporation under the 1.07-µm laser, or reaction with the specified **alumina/zirconia/graphite crucibles or Ti-alloy/Mo sonotrodes** were verified for this setup. Avoid claiming a particular crucible–H reaction or volatilization loss. Independently monitor Ti/Mo pickup, oxides and other contamination rather than assigning them to H. (romero2025thermochemicalaspectsof pages 8-12, corrigall2020achemicalpotential pages 1-2)

**Process-control recommendation:** dry and protect charge materials, master alloys, crucible and collected powder; use dry, leak-checked Ar for atomization, storage, delivery and DED; avoid deliberate H₂ additions and unvalidated hydrogen-reduction treatments; minimize air exposure and segregate powder lots. Determine **total H by a validated inert-gas-fusion method** in charge, atomized powder, reused/stored powder, first interface bead and final deposit; measure O and moisture separately, since fusion-measured H can include hydrogen in retained H₂O rather than dissolved lattice H. Confirm the method's copper-matrix calibration, blanks, detection limit and recovery at **<1 weight ppm**. Pair cross-sectional pore/crack inspection and density with corrosion comparisons on **as-deposited** C71500 controls; separately report the 30-day selective-attack depth. These are proposed controls, not verified equipment-specific limits. (ledford2019characteristicsandprocessing pages 7-10, ledford2019characteristicsandprocessing pages 16-19, robitz1990closuredevelopmentfor pages 36-37)

## 5. Phase equilibrium and CALPHAD

[NUMBERS] **A unique “maximum solid solubility of H in Cu, wt% at temperature” cannot be assigned without specifying H₂ pressure/fugacity.** Corrigall *et al.*, *Journal of Phase Equilibria and Diffusion* **41** (2020) 27–34, **DOI:10.1007/s11669-019-00776-2**, measured dilute Cu–H equilibrium at **350–450 °C** under approximately **60–280 MPa H₂**; inferred Cu contents were **a few weight ppm**, or order **0.0001 wt%**, and followed a Sieverts-type pressure dependence. Those high-pressure data are **not** a maximum near Cu's melting temperature and are not a safe alloy-addition bound. Its experimental table labels **65–236 weight ppm values as hydrogen in the *zirconium probe*, not copper**. Its authors also note a discrepancy with an earlier CALPHAD-derived solubility expression. No defensible specified-pressure numerical terminal solid solubility at approximately **1,084 °C** was established here. (corrigall2020achemicalpotential pages 3-5, corrigall2020achemicalpotential pages 1-2, corrigall2020achemicalpotential pages 5-7, corrigall2020achemicalpotential pages 2-3, corrigall2020achemicalpotential media e633ddfa)

[CITE][GAP] The literature **does** include Magnusson and Frisk, “Thermodynamic Evaluation of the Copper-Rich Part of the Cu–H–O–S–P System at Low Temperatures,” *CALPHAD* **47** (2014) 148–160, **DOI:10.1016/j.calphad.2014.09.004**; that is **not** verification that a Cu–H assessment, much less assessed **Cu–Ni–H or Cu–Al–H** interaction parameters, exists in the installed **Thermo-Calc TCCU** database. **COST 531 concerns lead-free solder thermodynamics**, not a validated marine-Cu–H database: Kroupa *et al.*, *JOM* **59** (2007) 20–25, **DOI:10.1007/s11837-007-0084-6**. Check TCCU's *actual* element list and phase definitions before attempting a pycalphad H calculation. No relevant Cu–H intermetallic, hydride-based strengthening route, alloy-design invariant reaction, or credible route by which **sub-ppm H** pushes the liquidus above **1,250 °C** was established. Continue screening the **metallic** alloying elements for the atomizer's liquidus constraint; treat H by gas/melt chemistry, not a substitute Cu–H solidification diagram. (corrigall2020achemicalpotential pages 7-8, corrigall2020achemicalpotential pages 1-2, corrigall2020achemicalpotential pages 5-7)

## 6. Supply, safety, interactions and evidence quality

[NUMBERS] Hydrogen is **not an alloy-cost opportunity or a US critical *mineral*** in the sense relevant to choosing a metallic palette. The 2022 US critical-minerals revision added **Ni**; the final 2025 list includes **Cu and Ni**. A US national-laboratory scenario gives modeled H₂ production around **$1.89–1.93/kg** for high-temperature steam electrolysis—not a purchasable H-in-Cu addition price; specifying ppm H by commodity $/kg has no meaningful procurement benefit. Hydrogen gas is a flammability/asphyxiation and ignition-control issue, rather than a toxic metallic solute justifying an OSHA exposure-based H-in-alloy limit: its flammable interval is approximately **4.1–74 vol% in air** at ambient conditions. Apply **29 CFR 1910.103** and applicable compressed-gas/fire and powder-handling controls; extract and characterize laser fumes according to the **actual other alloying elements**, not presumed evaporated H metal. No verified H-specific RoHS/REACH composition restriction or Navy H-in-Cu specification was found. (iii2026usgscriticalminerals pages 1-2, staff2024usgsmineralreview pages 6-8, staff2022usgsminingreview pages 6-9, knighton2021technoeconomicanalysisof pages 128-131, cadwallader1999safetyissueswith pages 18-21, cadwallader1999safetyissueswith pages 65-67)

**Joint constraints:** prioritize **H × O**, including internal Cu₂O and powder moisture: low *measured residual H* alone does not establish absence of trapped steam. Oxygen removal by H₂ in a melt competes with H₂O generation; oxide-forming alloy constituents and substrate dilution may change the distribution of oxygen-containing inclusions, but **no numerical H:O acceptance ratio** is validated for Cu–Ni/NAB DED. Cu–Cr–Zr and Al₂O₃-containing copper establish that precipitates can trap H, not that adding Ni, Fe, Mn or Al at a specified ratio neutralizes it. Keep independent constraints for O, Fe/P-related hot cracking, powder moisture and interfacial dilution. Evidence is **strong for the demonstrated Cu-powder steam mechanism, moderate for the copper EB-weld precedent, and thin for transferring a particular numerical H limit or seawater effect to laser-DED Cu–Ni/NAB**. (ledford2019characteristicsandprocessing pages 7-10, robitz1990closuredevelopmentfor pages 36-37, romero2025thermochemicalaspectsof pages 8-12, carlone2019dissimilarmetalwelding pages 13-14, pealva2012interactionofcopper pages 13-16)

**Bound-setting failure mode:** **impurity_max_wt = 0.0001** is a provisional powder-and-deposit target taken from a *different copper welding application*; gas porosity/steam defects set the rationale. **0.00006 wt%** is a more stringent, likewise non-marine OFP benchmark, **not** a second independently established Cu–Ni/NAB threshold. Designed-addition conservative maximum, aggressive maximum and functional floor are **NA**: none has been demonstrated to improve as-deposited seawater performance. (robitz1990closuredevelopmentfor pages 36-37, magnusson2013selfdiffusionandimpurity pages 1-6, ledford2019characteristicsandprocessing pages 7-10)

VERDICT | H | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.0001 | evidence=thin

References

1. (robitz1990closuredevelopmentfor pages 36-37): Closure development for high-level nuclear waste containers for the tuff repository; Phase 1, Final report This article has 2 citations.

2. (magnusson2013selfdiffusionandimpurity pages 1-6): H Magnusson and K Frisk. Self-diffusion and impurity diffusion of hydrogen, oxygen, sulphur and phosphorus in copper. Unknown journal, 2013.

3. (ledford2019characteristicsandprocessing pages 7-10): Christopher Ledford, Christopher Rock, Paul Carriere, Pedro Frigola, Diana Gamzina, and Timothy Horn. Characteristics and processing of hydrogen-treated copper powders for eb-pbf additive manufacturing. Applied Sciences, 9:3993, Sep 2019. URL: https://doi.org/10.3390/app9193993, doi:10.3390/app9193993. This article has 66 citations.

4. (romero2025thermochemicalaspectsof pages 8-12): Alberto Rivera Romero, Félix Antonio López, and Carola Celada-Casero. Thermochemical aspects of substituting natural gas by hydrogen in blister copper deoxidation. Metallurgical and Materials Transactions B, Aug 2025. URL: https://doi.org/10.1007/s11663-025-03735-0, doi:10.1007/s11663-025-03735-0. This article has 3 citations.

5. (li2023stresscorrosioncracking pages 8-10): Dandan Li, Kaiyang Li, Jiajie Gao, Yunfeng Liu, Chao Qin, Jianfeng Li, Yongshuai Li, Wei Cao, Yunlong Zhai, and Guojie Huang. Stress corrosion cracking of copper–nickel alloys: a review. Coatings, 13:1690, Sep 2023. URL: https://doi.org/10.3390/coatings13101690, doi:10.3390/coatings13101690. This article has 20 citations.

6. (pealva2012interactionofcopper pages 13-16): I. Pealva, G. Alberro, F. Legarda, G. A., and B. Riccardi. Interaction of copper alloys with hydrogen. ArXiv, Mar 2012. URL: https://doi.org/10.5772/34469, doi:10.5772/34469. This article has 22 citations.

7. (li2023stresscorrosioncracking pages 10-11): Dandan Li, Kaiyang Li, Jiajie Gao, Yunfeng Liu, Chao Qin, Jianfeng Li, Yongshuai Li, Wei Cao, Yunlong Zhai, and Guojie Huang. Stress corrosion cracking of copper–nickel alloys: a review. Coatings, 13:1690, Sep 2023. URL: https://doi.org/10.3390/coatings13101690, doi:10.3390/coatings13101690. This article has 20 citations.

8. (li2023stresscorrosioncracking pages 11-12): Dandan Li, Kaiyang Li, Jiajie Gao, Yunfeng Liu, Chao Qin, Jianfeng Li, Yongshuai Li, Wei Cao, Yunlong Zhai, and Guojie Huang. Stress corrosion cracking of copper–nickel alloys: a review. Coatings, 13:1690, Sep 2023. URL: https://doi.org/10.3390/coatings13101690, doi:10.3390/coatings13101690. This article has 20 citations.

9. (ledford2019characteristicsandprocessing pages 16-19): Christopher Ledford, Christopher Rock, Paul Carriere, Pedro Frigola, Diana Gamzina, and Timothy Horn. Characteristics and processing of hydrogen-treated copper powders for eb-pbf additive manufacturing. Applied Sciences, 9:3993, Sep 2019. URL: https://doi.org/10.3390/app9193993, doi:10.3390/app9193993. This article has 66 citations.

10. (ledford2019characteristicsandprocessing media 37e413d8): Christopher Ledford, Christopher Rock, Paul Carriere, Pedro Frigola, Diana Gamzina, and Timothy Horn. Characteristics and processing of hydrogen-treated copper powders for eb-pbf additive manufacturing. Applied Sciences, 9:3993, Sep 2019. URL: https://doi.org/10.3390/app9193993, doi:10.3390/app9193993. This article has 66 citations.

11. (carlone2019dissimilarmetalwelding pages 13-14): P. Carlone and A. Astarita. Dissimilar metal welding. Metals, Nov 2019. URL: https://doi.org/10.3390/met9111206, doi:10.3390/met9111206. This article has 23 citations.

12. (carlone2019dissimilarmetalwelding pages 14-16): P. Carlone and A. Astarita. Dissimilar metal welding. Metals, Nov 2019. URL: https://doi.org/10.3390/met9111206, doi:10.3390/met9111206. This article has 23 citations.

13. (robitz1990closuredevelopmentfor pages 37-39): Closure development for high-level nuclear waste containers for the tuff repository; Phase 1, Final report This article has 2 citations.

14. (corrigall2020achemicalpotential pages 1-2): J. L. Corrigall, C. St Louis, C. E. Coleman, and G. A. McRae. A chemical potential probe to determine the solubility of hydrogen in metals: an example with copper. Journal of Phase Equilibria and Diffusion, 41:27-34, Jan 2020. URL: https://doi.org/10.1007/s11669-019-00776-2, doi:10.1007/s11669-019-00776-2. This article has 9 citations and is from a peer-reviewed journal.

15. (corrigall2020achemicalpotential pages 3-5): J. L. Corrigall, C. St Louis, C. E. Coleman, and G. A. McRae. A chemical potential probe to determine the solubility of hydrogen in metals: an example with copper. Journal of Phase Equilibria and Diffusion, 41:27-34, Jan 2020. URL: https://doi.org/10.1007/s11669-019-00776-2, doi:10.1007/s11669-019-00776-2. This article has 9 citations and is from a peer-reviewed journal.

16. (corrigall2020achemicalpotential pages 5-7): J. L. Corrigall, C. St Louis, C. E. Coleman, and G. A. McRae. A chemical potential probe to determine the solubility of hydrogen in metals: an example with copper. Journal of Phase Equilibria and Diffusion, 41:27-34, Jan 2020. URL: https://doi.org/10.1007/s11669-019-00776-2, doi:10.1007/s11669-019-00776-2. This article has 9 citations and is from a peer-reviewed journal.

17. (corrigall2020achemicalpotential pages 2-3): J. L. Corrigall, C. St Louis, C. E. Coleman, and G. A. McRae. A chemical potential probe to determine the solubility of hydrogen in metals: an example with copper. Journal of Phase Equilibria and Diffusion, 41:27-34, Jan 2020. URL: https://doi.org/10.1007/s11669-019-00776-2, doi:10.1007/s11669-019-00776-2. This article has 9 citations and is from a peer-reviewed journal.

18. (corrigall2020achemicalpotential media e633ddfa): J. L. Corrigall, C. St Louis, C. E. Coleman, and G. A. McRae. A chemical potential probe to determine the solubility of hydrogen in metals: an example with copper. Journal of Phase Equilibria and Diffusion, 41:27-34, Jan 2020. URL: https://doi.org/10.1007/s11669-019-00776-2, doi:10.1007/s11669-019-00776-2. This article has 9 citations and is from a peer-reviewed journal.

19. (corrigall2020achemicalpotential pages 7-8): J. L. Corrigall, C. St Louis, C. E. Coleman, and G. A. McRae. A chemical potential probe to determine the solubility of hydrogen in metals: an example with copper. Journal of Phase Equilibria and Diffusion, 41:27-34, Jan 2020. URL: https://doi.org/10.1007/s11669-019-00776-2, doi:10.1007/s11669-019-00776-2. This article has 9 citations and is from a peer-reviewed journal.

20. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

21. (staff2024usgsmineralreview pages 6-8): U Staff. Usgs mineral review. Unknown journal, 2024.

22. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

23. (knighton2021technoeconomicanalysisof pages 128-131): Lane Knighton, Daniel Wendt, James Richards, Cristian Rabiti, Abdalla Abou Jaoude, Tyler Westover, Kurt Vedros, Samuel Bates, Amgad Elgowainy, Adarsh Bafana, Richard Boardman, Krishna Reddi, Guiyan Zang, Mark Ruth, Bethany Frew, Daniel Levie, Paige Jadun, Jal Desai, Sherry Bernhoft, Brittany Westlakd, David McCollum, Daniel Ludwig, Molly Strasser, and Bryan Ramler. Techno-Economic Analysis of Product Diversification Options for Sustainability of the Monticello and Prairie Island Nuclear Power Plants. Office of Scientific and Technical Information (OSTI), Nov 2021. URL: https://doi.org/10.2172/1843030, doi:10.2172/1843030.

24. (cadwallader1999safetyissueswith pages 18-21): Lee Charles Cadwallader and James Stephen Herring. Safety issues with hydrogen as a vehicle fuel. ArXiv, Oct 1999. URL: https://doi.org/10.2172/911496, doi:10.2172/911496. This article has 78 citations.

25. (cadwallader1999safetyissueswith pages 65-67): Lee Charles Cadwallader and James Stephen Herring. Safety issues with hydrogen as a vehicle fuel. ArXiv, Oct 1999. URL: https://doi.org/10.2172/911496, doi:10.2172/911496. This article has 78 citations.
