<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 55689735-1895-4174-a832-26168d8b1abf
- Submitted: 2026-10-17T18:59:41Z
- Fetched: 2026-10-17T19:30:41Z (status: success)
- Raw trajectory JSON: ../raw/el-17-Ag.json.gz
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

ELEMENT UNDER REVIEW: Ag (strengthening addition). Silver-bearing coppers (C10700, C11300 series, 0.03-0.1 Ag), Cu-Ag high-strength conductors (several wt% Ag). Costly; silver was added to the US critical minerals list in 2025.

Answer for Ag specifically, not for copper alloys in general:
1. ROLE: what Ag does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ag ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ag changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ag, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ag, Cu-Ni-Ag and Cu-Al-Ag are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ag in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ag neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ag | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Ag (strengthening addition). Silver-bearing coppers (C10700, C11300 series, 0.03-0.1 Ag), Cu-Ag high-strength conductors (several wt% Ag). Costly; silver was added to the US critical minerals list in 2025.

Answer for Ag specifically, not for copper alloys in general:
1. ROLE: what Ag does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ag ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ag changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Ag, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ag, Cu-Ni-Ag and Cu-Al-Ag are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ag in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Ag neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ag | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Ag in pre-alloyed copper powder for marine laser DED

**Decision: INCLUDE Ag as a narrowly bounded experimental addition in the Al-bronze branch, not as a proven seawater-resistant strengthening addition.** The most pertinent corrosion observation is for **0.25 wt% Ag nanoparticles** in a Cu–Al–Ni *shape-memory alloy*, not cast C95800 nickel-aluminum bronze (NAB), wrought C71500 Cu–Ni, or a DED deposit. It establishes a testable hypothesis, not equivalence to wrought 70–30 Cu–Ni. In contrast, Cu–Ag laser studies at much higher Ag contents establish process effects but provide no marine-corrosion qualification. The bounds below are therefore **research-screening bounds, not certified service limits**. Publications by the named PI were excluded. (dawood2020areviewof pages 5-8, chen2023highreflectivityand pages 4-7, robinson2021effectofsilver pages 12-14)

### 1. Role, mechanisms, and alloy provenance

- **[CITE][NUMBERS] Cu-rich Cu–Ag:** Ag can remain in fcc Cu solid solution at elevated temperature and separate into an Ag-rich fcc phase as solubility falls. Solid-solution strengthening and Ag-rich phase/interface strengthening are plausible; neither requires a Cu–Ag intermetallic. A documented **nonmarine** precedent is cast **NARloy-A, Cu–3.5 wt% Ag**, and NASA rocket-liner **NARloy-Z, Cu–3 wt% Ag–0.5 wt% Zr**. Their high-temperature service does **not** demonstrate seawater resistance or as-deposited strengthening. An LPBF Cu–Ag study attributes strength increases partly to phase boundaries, but its **10–30 wt% nominal Ag** range is far outside a trace-addition study. (luo1996phaseequilibriaof pages 4-5, robinson2021effectofsilver pages 12-14, minneci2021copperbasedalloysfor pages 3-5)
- **[CITE][NUMBERS] Al-bronze-related evidence:** A review of Saud *et al.* reports that **0.25 wt% Ag nanoparticles** changed the corrosion response of Cu–Al–Ni shape-memory alloy; reported surface products included AgCl and Ag₂O alongside Cu₂O, CuCl, and Al₂O₃/Al(OH)₃. This is evidence of Ag-bearing corrosion products, **not proof that Ag constructs a durable protective film** on NAB. Nanoparticle incorporation is also not equivalent to melting pure Ag into a pre-alloyed powder. (dawood2020areviewof pages 5-8)
- **[SPEC][GAP] Commercial/Navy identification:** Silver-bearing electrical coppers in the **UNS C10700/C11300 series** are relevant manufacturing precedents, but the retrieved primary material does **not** establish their individual certified Ag ranges; the approximate **0.03–0.1 wt% Ag** range supplied in the question must not be assigned to individual UNS grades without checking their current UNS/CDA chemistry records. Likewise, **no Ag design range or Ag-specific impurity maximum was verified** for C71500 under ASTM B111/B171/B466 or MIL-T-16420, C95800 under ASTM B148/B369 or MIL-B-24480, the cited MIL-C-15726, EN 12449, or AWS A5.7 fillers **ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl**. Do not call an unspecified residual an intentional Navy alloying addition. No qualifying Ag range was verified for marine Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si. Specifically, Ag is **not established here** as their deoxidizer, grain refiner, dezincification inhibitor, or substitute for Ni/Fe/Al marine-film chemistry. (dawood2020areviewof pages 5-8, luo1996phaseequilibriaof pages 4-5, minneci2021copperbasedalloysfor pages 3-5)

### 2. Seawater and chloride corrosion

**[CITE][NUMBERS][GAP] Closest composition-controlled indication:** The review reports **0.25 wt% Ag** in Cu–Al–Ni shape-memory alloy, an *E*₍corr₎ change from **−277.1 to −307.4 mV**, and an Ag-bearing current density of **5.61 µA cm⁻²**. A **more negative** potential is not itself evidence of improvement. The accessible account does not securely specify the electrolyte for *this Ag comparison*, give its Ag-free current density, or provide corrosion rate, film resistance, or pit depth. The frequently adjacent **3.5 wt% NaCl** wording also covers *other* Mn/Ti experiments; it must not be silently attributed to the Ag experiment. The original paper is Saud *et al.*, “Microstructure and corrosion behaviour of Cu–Al–Ni shape memory alloys with Ag nanoparticles,” *Materials and Corrosion* **66** (2015) 527–534, **doi:10.1002/maco.201407658**; its numerical account here comes through Dawood, “A review of microstructure and corrosion behavior of Cu Al Ni shape memory alloy,” *Iraqi Journal for Mechanical and Materials Engineering* **20** (2020) 362–375, **doi:10.32852/iqjfmme.v20i4.530**. (dawood2020areviewof pages 5-8)

**[CITE][NUMBERS][GAP] Chloride data that must *not* be treated as a bulk-alloy dose response:** Selectively plated Cu coatings containing Ag particles had, in **3.5 wt% NaCl**, corrosion rates of **0.028493 mm y⁻¹** (alkaline-plated, 20 nm Ag), **0.038638** (alkaline, 3 µm), **0.089871** (acidic, 20 nm), and **0.10276** (acidic, 3 µm); corresponding *i*₍corr₎ values were **2.455, 3.2936, 7.6608, and 8.7595 µA cm⁻²**. Neither the Ag loading in **wt% of the whole coating** nor a comparable Ag-free control was established. Deposition chemistry changed alongside Ag particle size; these values establish **neither a beneficial nor a harmful bulk Ag concentration interval**. The Ag/AgCl *reference electrode* is not added Ag. Yankova *et al.*, “Corrosion resistance and wettability of selective plated copper-based coatings containing silver particles,” *Proceedings of the Bulgarian Academy of Sciences* (2026), **doi:10.7546/crabs.2026.04.09**. (yankova2026corrosionresistanceand pages 4-7)

**[CITE][GAP] Potential failure mechanism, not a seawater threshold:** Experiments on bulk **Cu–20 wt% Ag** and **Cu–80 wt% Ag** in **0.5 M NaOH plus sulfide**, *not seawater*, observed Cu-selective dissolution, Ag₂S/CuₓS formation, and pits. They do not justify claiming that marine Cu–Ni or NAB is harmed above **0.25, 1, or 3 wt% Ag**; they do establish that noble Ag-rich phases and sulfide contamination cannot simply be assumed protective. Zaky, Abd El-Rehim and Mohamed, “Effect of addition of sulphide ions on the electrochemical behaviour and corrosion of Cu–Ag alloys in alkaline solutions,” *International Journal of Electrochemical Science* **1** (2006) 17–31, **doi:10.20964/1010017**. **No Ag-specific quantitative seawater rate, EIS film resistance, crevice/pitting depth, dealloying rate, erosion-corrosion rate, or allowable flow velocity** was verified for the target marine families. (zaky2006effectofaddition pages 1-3)

The evidence cases and their limitations are separated here:

| Evidence case | Ag content (wt%) | Material/process | Marine alloy? | As-deposited seawater corrosion measured? | Key result | Can establish a marine-safe Ag upper bound? |
|---|---:|---|---|---|---|---|
| Ag-nanoparticle-modified Cu–Al–Ni shape-memory alloy | 0.25 | Cu–Al–Ni SMA with added Ag nanoparticles; non-DED study | No—shape-memory alloy, not NAB or a marine aluminum-bronze grade | No. A review reports icorr = 5.61 µA/cm², Ecorr shifting from −277.1 to −307.4 mV, and AgCl, Ag₂O, Cu₂O, CuCl, and Al₂O₃/Al(OH)₃ products, but the excerpt does not securely identify the electrolyte or as-deposited condition (dawood2020areviewof pages 5-8) | Suggests that 0.25 wt% Ag can alter corrosion-film chemistry in one Cu–Al–Ni SMA | **No.** It is one indirect result and does not establish either a functional minimum or an upper bound for marine DED alloys |
| Cu–Ag LPBF, nominal CuAg10 | 10 nominal; 7.49–16.41 measured by EDX depending on sampling | In-situ-alloyed LPBF Cu–Ag; 370 W, approximately 1.07 µm infrared laser | No—high-conductivity Cu–Ag alloy | No | Increasing Ag across the 10–30 wt% series reduced pores, but CuAg10 porosity increased 164% after annealing; composition uniformity was imperfect (robinson2021thefeasabilityof pages 131-135, robinson2021effectofsilver pages 12-14, robinson2021effectofsilver pages 3-5, robinson2021effectofsilver pages 5-8) | **No.** No seawater data, no Cu–Ni/NAB chemistry, and nominal-to-measured composition scatter is large |
| Cu–Ag LPBF, nominal CuAg20 | 20 nominal; 27.50–29.00 measured by EDX | In-situ-alloyed LPBF Cu–Ag | No—high-conductivity Cu–Ag alloy | No | Higher modulus, yield strength, and UTS than nominal CuAg10; failure strain was highest near nominal CuAg20, but pores remained (robinson2021effectofsilver pages 12-14, robinson2021effectofsilver pages 8-12, robinson2021effectofsilver pages 3-5) | **No.** Mechanical and pore trends cannot demonstrate marine-corrosion safety |
| Cu–Ag LPBF, nominal CuAg30 | 30 nominal; 35.42–35.80 measured by EDX | In-situ-alloyed LPBF Cu–Ag | No—high-conductivity Cu–Ag alloy | No | Lowest pore-defect content in the tested series; from nominal 10 to 30 wt% Ag, pore count fell 87% as built and average pore size fell 40%, but no corrosion qualification was performed (robinson2021thefeasabilityof pages 131-135, robinson2021effectofsilver pages 12-14, robinson2021effectofsilver pages 1-2, robinson2021thefeasabilityofb pages 131-135) | **No.** Demonstrates LPBF processability only at economically extreme Ag levels |
| **Ag7.5Cu** LPBF alloy—notation means **7.5 wt% Cu and approximately 92.5 wt% Ag**, not 7.5 wt% Ag | Approximately 92.5 | Gas-atomized Ag-rich powder in Ag7.5Cu/Cu10Sn multi-material LPBF | No—silver-rich electronic or jewelry-type material | No | Microcracks occurred mainly in the Ag7.5Cu region and followed melt-pool or grain boundaries; high thermal stress and inadequate liquid backfilling were proposed causes (chen2023highreflectivityand pages 2-4, chen2023highreflectivityand pages 4-7, chen2023highreflectivityand media a43719fe) | **No.** Instead, it is evidence that very Ag-rich laser deposits may crack |
| Commercial marine AWS A5.7 filler baseline: ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl | Ag not established as a specified designed addition in the evidence reviewed | Commercial Cu–Ni or aluminum-bronze welding fillers used as indirect DED baselines | Yes, depending on filler and application | Not established here for an Ag-versus-zero comparison | The retrieved evidence provides no verified AWS Ag range and therefore cannot support inventing one | **No.** Treat these as Ag-free or Ag-unspecified baselines pending direct inspection of current AWS A5.7 chemistry tables |
| Cu–Ag binary eutectic | 72.0 Ag, reported as Ag–28.0 Cu; approximately 71.999 Ag by calculation | Equilibrium Cu–Ag binary system | No—phase-diagram reference composition | No | Simple eutectic liquid → Ag(fcc) + Cu(fcc) at approximately 778 °C; no equilibrium Cu–Ag intermetallic is reported (luo1996phaseequilibriaof pages 4-5) | **No.** It defines a phase boundary and severe Ag-rich segregation limit, not a corrosion-safe marine-alloy bound |


*Table: This table separates direct Ag observations from evidence that cannot establish a safe composition bound for as-deposited marine DED. It also disambiguates the silver-rich Ag7.5Cu notation and flags missing seawater and commercial-specification evidence.*

### 3. DED, reheating, and repair interfaces

**[CITE][NUMBERS] Direct laser evidence is LPBF, *not blown-powder DED*.** Robinson *et al.* tested in-situ-mixed Cu–Ag powders at **10, 20, and 30 wt% nominal Ag**. Local EDX measurements differed markedly from nominal values: **7.49, 27.50, and 35.80 wt% Ag** in one set of measurements. Across nominal **10→30 wt% Ag**, as-built pore *number* fell **87%** and average pore size **40%**; this does **not** demonstrate dense, crack-free deposits at **0.25 wt% Ag**. Strength rose across the high-Ag series, whereas a **500 °C, 30 min** anneal increased the nominal-10 wt% sample’s pore count **164%**—and post-build heat treatment is disallowed here. Robinson *et al.*, “Effect of silver addition in copper-silver alloys fabricated by laser powder bed fusion in situ alloying,” *Journal of Alloys and Compounds* **857** (2021) 157561, **doi:10.1016/j.jallcom.2020.157561**. (robinson2021thefeasabilityof pages 131-135, robinson2021effectofsilver pages 12-14, robinson2021effectofsilver pages 3-5)

**[CITE][NUMBERS] Cracking caution:** A separate LPBF Ag7.5Cu/Cu10Sn sandwich exhibited **microcracks mainly on its Ag-rich side**, including at melt-pool boundaries. **Ag7.5Cu means approximately 92.5 wt% Ag–7.5 wt% Cu, *not* Cu–7.5 wt% Ag.** The authors attributed cracking to thermal stress/columnar boundaries and inadequate liquid backfilling; their **~90 and ~40 µm** interface mixing-zone widths depend on build direction. Figure 4 visibly documents the Ag-rich microcracks. This is not a measured cracking threshold for Cu-rich marine powder. Chen *et al.*, “High reflectivity and thermal conductivity Ag–Cu multi-material structures fabricated via laser powder bed fusion,” *Micromachines* **14** (2023) 362, **doi:10.3390/mi14020362**. (chen2023highreflectivityand pages 2-4, chen2023highreflectivityand pages 4-7, chen2023highreflectivityand media a43719fe)

**[GAP] DED-specific risk assessment:** Segregation toward a low-melting Ag-rich residual liquid creates a *plausible* solidification-cracking and **reheated-layer liquation** pathway; Cu–Ni–Ag phase separation makes this especially important at a Cu–Ni repair interface. Dilution into cast NAB introduces Al/Ni/Fe-containing interdendritic regions, whereas dilution into C71500 raises local Ni; neither interface has an Ag-specific crack, porosity, evaporation, oxidation-loss, or corrosion result. AWS A5.7 filler families provide welding *baselines*, not evidence that their welds tolerate an invented Ag percentage. Measure powder/feed/deposit Ag by bulk analysis; run self-build and both-substrate crack sections before claiming weldability. (chen2023highreflectivityand pages 4-7, luo1996phaseequilibriaof pages 4-5, luo1996phaseequilibriaof pages 5-7, robinson2021effectofsilver pages 12-14)

### 4. Powder manufacture and phase/CALPHAD constraints

**[CITE][NUMBERS] Binary phase diagram:** Cu–Ag is a simple fcc-Cu/fcc-Ag eutectic with **liquid → (Cu) + (Ag) at approximately 778 °C and 72 wt% Ag–28 wt% Cu**, *without a reported equilibrium binary intermetallic*. Strongly Ag-rich liquid may persist at boundaries even when nominal Ag is much lower than the eutectic composition. The sources inspected do **not** provide a securely citable numerical **maximum solubility of Ag in Cu**, so a particular wt%/temperature must **not** be used as this proposal’s upper bound. Note that **8.27 wt% at 779.1 °C**, quoted by Chen *et al.*, is **Cu dissolved in Ag**, the *opposite* solubility. Luo and Chen, “Phase equilibria of the ternary Ag–Cu–Ni system and the interfacial reactions in the Ag–Cu/Ni couples,” *Journal of Materials Science* **31** (1996) 5059–5067, **doi:10.1007/BF00355906**; Chen *et al.*, **doi:10.3390/mi14020362**. (chen2023highreflectivityand pages 4-7, luo1996phaseequilibriaof pages 4-5)

**[CITE][NUMBERS] Interactions and model availability:** Luo and Chen experimentally/modelled **Ag–Cu–Ni** sections at **700, 795, and 860 °C**. They found (Cu,Ni), Ag-rich, and sometimes liquid regions, **no ternary compound**, and near-exclusion of Ni from the Ag-rich phase. Their Ag–15 wt% Cu/Ni diffusion couple at **860 °C** developed liquid-filled penetration along Ni—a **high-Ag brazing analogue**, not evidence that a **0.25 wt% Ag** Cu–Ni repair will penetrate its substrate. This is a **published thermodynamic ternary assessment**; it does *not* verify its presence or coverage in a particular installed Thermo-Calc **TCCU** release or COST 531 database. Cu–Al–Ag ternary assessment/Al–Ag reaction products and transferability of an Ag-containing TDB to TCCU/pycalphad remain to be checked against actual database constituent/parameter lists. (luo1996phaseequilibriaof pages 1-2, luo1996phaseequilibriaof pages 2-4, luo1996phaseequilibriaof pages 4-5, luo1996phaseequilibriaof pages 5-7)

**[NUMBERS][GAP] The specified ~1,300 °C melt:** In the **Cu-rich binary**, adding Ag toward its **778 °C** eutectic depresses, rather than raises, the Cu-end liquidus; Ag alone is **not** a reason to reject a candidate for crossing **~1,200–1,250 °C**. This does **not** clear Ag–Ni-, Ag–Al-, or other multicomponent compositions: calculate **their actual liquidus and superheat**, including the Ni-rich branch, before each ~0.5 kg charge. A published Cu–Ag preparation melted **20 and 80 wt% Ag** alloys in a **graphite crucible**; that is evidence of laboratory feasibility, not proof of clean atomization with alumina, zirconia, a Ti-alloy sonotrode, or Mo. No quantified Ag-dependent surface tension, crucible reaction, sonotrode dissolution, vaporization fraction, or powder oxygen uptake was verified for this apparatus. Treat Ag volatilization in the laser pool and any claimed Ag deoxidation as **unmeasured**, and assay the powder and deposit rather than assume charge retention. (zaky2006effectofaddition pages 1-3, luo1996phaseequilibriaof pages 4-5)

### 5. Supply, occupational limits, and proposed composition bounds

**[CITE][NUMBERS] Supply/cost:** The USGS technical assessment recommended **silver and copper** among six additions to its **draft 2025** U.S. critical-minerals list; **that report is not itself proof of the final Federal Register designation**. Its predecessor **2022 list** did not identify Ag as an established addition in this assessment; the relevant legal lists should be cited separately when asserting final status. Nassar *et al.*, USGS *Open-File Report 2025–1047*, **doi:10.3133/ofr20251047**. A reported **September 2025 silver price of ~$41.19/troy oz** converts to **~$1,324/kg of Ag** (1 troy oz = 0.0311035 kg): at that *illustrative historical spot price*, **0.25 wt%** contributes **~$3.31/kg alloy**, **1 wt% ~$13.24/kg**, and a **0.5 kg** charge at **0.25 wt%** requires **1.25 g Ag**. Purchasing, fabrication, and future spot prices differ. Lan, “Silver’s dual identity,” *Mineral Economics* (2026), **doi:10.1007/s13563-026-00660-9**. (lan2026silver’sdualidentity pages 5-11, nassar2025methodologyandtechnical pages 33-35)

**[CITE][NUMBERS] Safety/regulation:** The cited toxicology review reports **OSHA PEL and NIOSH REL of 0.01 mg Ag/m³**, eight-hour time-weighted average, for metallic and soluble silver; prolonged high exposure can cause argyria. Enclose/locally extract powder transfer and atomization, capture laser fume, avoid dry sweeping, and monitor the relevant **Cu/Ni-containing mixed-metal aerosol as well as Ag**. A bulk Ag composition is not an airborne-exposure limit. No Ag-specific RoHS/REACH concentration prohibition or Navy material ban was verified: do not invent one. Kodali, Erdely and Zeidler-Erdely, “Toxicity of airborne metals,” *Reference Module in Biomedical Sciences* (2026), **doi:10.1016/B978-0-323-95488-4.00102-9**. (kodali2026toxicityofairborne pages 6-8)

**[NUMBERS][GAP] Bound decision—Cu balance, deposit composition in wt%:**

| Family | Functional floor | Conservative maximum | Non-conservative maximum | What actually sets the number |
|---|---:|---:|---:|---|
| **Experimental Al-bronze/Cu–Al–Ni branch** | **0.25** | **0.25** | **1.0** | **0.25 wt%** is the smallest *retrieved* Cu–Al–Ni corrosion-effect test, **not a proven minimum** and not commercial/Navy precedent. **1.0 wt%** is an explicitly **provisional experimental ceiling**, not a demonstrated safe composition or a measured phase boundary: it keeps the screen near trace-Ag levels rather than importing the **3–30 wt%** nonmarine strengthening alloys. Stop earlier if as-deposited selective attack, Ag-rich connected boundaries, cracks, or lack of superheat appear. |
| **Cu–Ni branch** | **NA** | **NA** | **NA** | No verified Cu–Ni **Ag-addition** seawater benefit or crack-free DED limit. Hold Ag at the measured feedstock-background level pending evidence; **no specification-based numerical impurity maximum has been verified**. |

These values deliberately **do not claim an established commercial or Navy Ag upper limit**: the conservative Al-bronze bound is *experimental* because the requested type of commercial precedent was not substantiated. **No defensible specification-derived impurity maximum (ppm or wt%)** is available for either target family; hence it would be misleading to relabel **0.25 wt%** an allowable impurity. For a joint-constraint study, record **Ni–Ag phase partitioning** and local Ag enrichment with **Ni, Al, Fe, and Mn** after dilution; inspect Al-bearing corrosion films and possible AgCl/Ag₂S separately. No validated sums such as **Ag+Ni**, **Ag+Fe**, or Ag:Al ratio, and no verified Ag neutralization of a harmful element, were found. (dawood2020areviewof pages 5-8, luo1996phaseequilibriaof pages 4-5, luo1996phaseequilibriaof pages 5-7, minneci2021copperbasedalloysfor pages 3-5)

**Evidence quality: thin for the marine-DED decision.** There is one indirectly reported **0.25 wt%** Cu–Al–Ni nanoparticle corrosion response, coating data lacking bulk Ag dosage, nonmarine high-Ag LPBF processing results, and useful binary/ternary thermodynamics; **none** establishes as-deposited DED corrosion equivalence to C71500. The Ag experiment’s electrolyte and control current are insufficiently documented in the accessible review. Test at least **0 and 0.25 wt% Ag** with identical non-Ag chemistry, followed—only if both repair interfaces are crack-free—by intermediate compositions up to the **provisional 1.0 wt%** ceiling; compare 30-day maximum selective-attack *depth* as well as electrochemical response against wrought C71500. (dawood2020areviewof pages 5-8, yankova2026corrosionresistanceand pages 4-7, chen2023highreflectivityand pages 4-7, robinson2021effectofsilver pages 12-14)

VERDICT | Ag | decision=INCLUDE | family=Al-bronze | conservative_max_wt=0.25 | nonconservative_max_wt=1.0 | floor_wt=0.25 | impurity_max_wt=NA | evidence=thin

References

1. (dawood2020areviewof pages 5-8): Nawal Mohammed Dawood. A review of microstructure and corrosion behavior of cu al ni shape memory alloy. THE IRAQI JOURNAL FOR MECHANICAL AND MATERIALS ENGINEERING, 20:362-375, Dec 2020. URL: https://doi.org/10.32852/iqjfmme.v20i4.530, doi:10.32852/iqjfmme.v20i4.530. This article has 1 citations.

2. (chen2023highreflectivityand pages 4-7): Qiao-Yu Chen, Yongbin Jing, Jie Yin, Zheng Li, Wei Xiong, Ping Gong, Lu Zhang, Simeng Li, Rui-Qi Pan, Xi-Ya Zhao, and Liang Hao. High reflectivity and thermal conductivity ag–cu multi-material structures fabricated via laser powder bed fusion: formation mechanisms, interfacial characteristics, and molten pool behavior. Micromachines, 14:362, Jan 2023. URL: https://doi.org/10.3390/mi14020362, doi:10.3390/mi14020362. This article has 47 citations.

3. (robinson2021effectofsilver pages 12-14): John Robinson, Arun Arjunan, Mark Stanford, Iain Lyall, and Craig Williams. Effect of silver addition in copper-silver alloys fabricated by laser powder bed fusion in situ alloying. Mar 2021. URL: https://doi.org/10.1016/j.jallcom.2020.157561, doi:10.1016/j.jallcom.2020.157561. This article has 61 citations and is from a peer-reviewed journal.

4. (luo1996phaseequilibriaof pages 4-5): Huey-Tsyr Luo and Sinn-Wen Chen. Phase equilibria of the ternary ag-cu-ni system and the interfacial reactions in the ag-cu/ni couples. Journal of Materials Science, 31:5059-5067, Oct 1996. URL: https://doi.org/10.1007/bf00355906, doi:10.1007/bf00355906. This article has 57 citations and is from a peer-reviewed journal.

5. (minneci2021copperbasedalloysfor pages 3-5): Robert P. Minneci, Eric A. Lass, Jeffrey R. Bunn, Hahn Choo, and Claudia J. Rawn. Copper-based alloys for structural high-heat-flux applications: a review of development, properties, and performance of cu-rich cu–cr–nb alloys. International Materials Reviews, 66:394-425, Oct 2021. URL: https://doi.org/10.1080/09506608.2020.1821485, doi:10.1080/09506608.2020.1821485. This article has 183 citations and is from a domain leading peer-reviewed journal.

6. (yankova2026corrosionresistanceand pages 4-7): Radostina Yankova, Ivan Rusev, Ina Koleva, and Deyan Veselinov. Corrosion resistance and wettability of selective plated copper-based coatings containing silver particles. Proceedings of the Bulgarian Academy of Sciences, Apr 2026. URL: https://doi.org/10.7546/crabs.2026.04.09, doi:10.7546/crabs.2026.04.09. This article has 0 citations.

7. (zaky2006effectofaddition pages 1-3): Ayman M. Zaky, Sayed S. Abd El-Rehim, and Basheer M. Mohamed. Effect of addition of sulphide ions on the electrochemical behaviour and corrosion of cu-ag alloys in alkaline solutions. International Journal of Electrochemical Science, 1:17-31, May 2006. URL: https://doi.org/10.20964/1010017, doi:10.20964/1010017. This article has 16 citations and is from a peer-reviewed journal.

8. (robinson2021thefeasabilityof pages 131-135): J Robinson. The feasability of processing silver and copper. Unknown journal, 2021.

9. (robinson2021effectofsilver pages 3-5): John Robinson, Arun Arjunan, Mark Stanford, Iain Lyall, and Craig Williams. Effect of silver addition in copper-silver alloys fabricated by laser powder bed fusion in situ alloying. Mar 2021. URL: https://doi.org/10.1016/j.jallcom.2020.157561, doi:10.1016/j.jallcom.2020.157561. This article has 61 citations and is from a peer-reviewed journal.

10. (robinson2021effectofsilver pages 5-8): John Robinson, Arun Arjunan, Mark Stanford, Iain Lyall, and Craig Williams. Effect of silver addition in copper-silver alloys fabricated by laser powder bed fusion in situ alloying. Mar 2021. URL: https://doi.org/10.1016/j.jallcom.2020.157561, doi:10.1016/j.jallcom.2020.157561. This article has 61 citations and is from a peer-reviewed journal.

11. (robinson2021effectofsilver pages 8-12): John Robinson, Arun Arjunan, Mark Stanford, Iain Lyall, and Craig Williams. Effect of silver addition in copper-silver alloys fabricated by laser powder bed fusion in situ alloying. Mar 2021. URL: https://doi.org/10.1016/j.jallcom.2020.157561, doi:10.1016/j.jallcom.2020.157561. This article has 61 citations and is from a peer-reviewed journal.

12. (robinson2021effectofsilver pages 1-2): John Robinson, Arun Arjunan, Mark Stanford, Iain Lyall, and Craig Williams. Effect of silver addition in copper-silver alloys fabricated by laser powder bed fusion in situ alloying. Mar 2021. URL: https://doi.org/10.1016/j.jallcom.2020.157561, doi:10.1016/j.jallcom.2020.157561. This article has 61 citations and is from a peer-reviewed journal.

13. (robinson2021thefeasabilityofb pages 131-135): J Robinson. The feasability of processing silver and copper. Unknown journal, 2021.

14. (chen2023highreflectivityand pages 2-4): Qiao-Yu Chen, Yongbin Jing, Jie Yin, Zheng Li, Wei Xiong, Ping Gong, Lu Zhang, Simeng Li, Rui-Qi Pan, Xi-Ya Zhao, and Liang Hao. High reflectivity and thermal conductivity ag–cu multi-material structures fabricated via laser powder bed fusion: formation mechanisms, interfacial characteristics, and molten pool behavior. Micromachines, 14:362, Jan 2023. URL: https://doi.org/10.3390/mi14020362, doi:10.3390/mi14020362. This article has 47 citations.

15. (chen2023highreflectivityand media a43719fe): Qiao-Yu Chen, Yongbin Jing, Jie Yin, Zheng Li, Wei Xiong, Ping Gong, Lu Zhang, Simeng Li, Rui-Qi Pan, Xi-Ya Zhao, and Liang Hao. High reflectivity and thermal conductivity ag–cu multi-material structures fabricated via laser powder bed fusion: formation mechanisms, interfacial characteristics, and molten pool behavior. Micromachines, 14:362, Jan 2023. URL: https://doi.org/10.3390/mi14020362, doi:10.3390/mi14020362. This article has 47 citations.

16. (luo1996phaseequilibriaof pages 5-7): Huey-Tsyr Luo and Sinn-Wen Chen. Phase equilibria of the ternary ag-cu-ni system and the interfacial reactions in the ag-cu/ni couples. Journal of Materials Science, 31:5059-5067, Oct 1996. URL: https://doi.org/10.1007/bf00355906, doi:10.1007/bf00355906. This article has 57 citations and is from a peer-reviewed journal.

17. (luo1996phaseequilibriaof pages 1-2): Huey-Tsyr Luo and Sinn-Wen Chen. Phase equilibria of the ternary ag-cu-ni system and the interfacial reactions in the ag-cu/ni couples. Journal of Materials Science, 31:5059-5067, Oct 1996. URL: https://doi.org/10.1007/bf00355906, doi:10.1007/bf00355906. This article has 57 citations and is from a peer-reviewed journal.

18. (luo1996phaseequilibriaof pages 2-4): Huey-Tsyr Luo and Sinn-Wen Chen. Phase equilibria of the ternary ag-cu-ni system and the interfacial reactions in the ag-cu/ni couples. Journal of Materials Science, 31:5059-5067, Oct 1996. URL: https://doi.org/10.1007/bf00355906, doi:10.1007/bf00355906. This article has 57 citations and is from a peer-reviewed journal.

19. (lan2026silver’sdualidentity pages 5-11): Kung-Ming Lan. Silver’s dual identity: the energy transition, the great divergence, and taiwan’s strategic challenge. Jun 2026. URL: https://doi.org/10.1007/s13563-026-00660-9, doi:10.1007/s13563-026-00660-9. This article has 0 citations and is from a peer-reviewed journal.

20. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

21. (kodali2026toxicityofairborne pages 6-8): Vamsi K. Kodali, Aaron Erdely, and Patti C. Zeidler-Erdely. Toxicity of Airborne Metals. Elsevier, Jan 2026. URL: https://doi.org/10.1016/b978-0-323-95488-4.00102-9, doi:10.1016/b978-0-323-95488-4.00102-9. This article has 0 citations.
