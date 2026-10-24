<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 37922a77-287d-4c31-891b-142a1ded1f38
- Submitted: 2026-10-17T19:00:04Z
- Fetched: 2026-10-17T19:25:33Z (status: success)
- Raw trajectory JSON: ../raw/el-25-Se.json.gz
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

ELEMENT UNDER REVIEW: Se (impurity / free-machining). Free-machining with Bi (SeBiLOY C89510); impurity limit in Cu-Ni and copper.

Answer for Se specifically, not for copper alloys in general:
1. ROLE: what Se does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Se ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Se changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Se, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Se, Cu-Ni-Se and Cu-Al-Se are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Se in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Se neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Se | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Se (impurity / free-machining). Free-machining with Bi (SeBiLOY C89510); impurity limit in Cu-Ni and copper.

Answer for Se specifically, not for copper alloys in general:
1. ROLE: what Se does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Se ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Se changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Se, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Se, Cu-Ni-Se and Cu-Al-Se are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Se in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Se neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Se | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Selenium (Se): composition decision for seawater-service copper DED

**Decision — LIMIT Se as an impurity, not a designed addition.** The documented function of appreciable Se in commercial copper alloys is chip breaking, particularly alongside Bi in cast free-machining alloys—not improved seawater corrosion. A copper–nickel metallurgy review reports that Se can be extremely harmful to hot workability and cites control **as low as 0.006 wt% (60 ppm)**. That is a defensible *provisional screening ceiling* for both incoming powder and the analyzed deposit, especially where the deposit or dilution zone contains Ni. It is **not** a demonstrated DED cracking threshold, a seawater-performance threshold, or an ASTM Se specification. No Se concentration has been shown to make an as-deposited alloy match wrought C71500 in seawater. [CITE] Riley and Makar, “Impurity effects in secondary copper alloys,” *Conservation & Recycling* **9** (1986), 315–323, DOI: **10.1016/0361-3658(86)90066-4**. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6)

## 1. Role, mechanisms, and identified alloys

[CITE] The Copper Development Association describes Se as an **insoluble second-phase** free-machining addition: particles facilitate machining rather than strengthening copper through useful solid solution. It also cautions that free-machining additions reduce hot and cold ductility. Riley and Makar distinguish machinability additions, including Se, from additions used to inhibit dezincification or deoxidize copper alloys; those latter functions must **not** be attributed to Se. [GAP] No evidence recovered establishes Se-based protective seawater-film chemistry, dealloying inhibition, grain refinement, or beneficial Se precipitation in Cu–Ni, NAB, Mn–Al bronze, tin bronze, Cu–Ni–Sn, or Cu–Ni–Si. [CITE] Copper Development Association, *High Conductivity Coppers*, free-machining-coppers section, no verified document DOI; McMahon, U.S. Bureau of Mines, *Copper: A Materials Survey*, Information Circular 8225 (1965), no verified DOI. (coppers1999copperdevelopmentassociation pages 50-53, riley1986impurityeffectsin pages 1-3, mcmahon1965informationcircular8225 pages 18-20)

[NUMBERS][SPEC] The following **reported UNS composition ranges** are for free-machining plumbing alloys, not marine Cu–Ni or NAB. Zhou’s review identifies ASTM **B30** copper-alloy ingots as covering several C895xx Bi–Se grades; its composition table and the pertinent cropped image support the ranges. The review is a secondary source, **not the controlling edition of ASTM B30**. [CITE] Zhou Nianrun, “Research Progress of Free-Cutting Unleaded Bismuth Brass for Sanitary Ware Industry,” *Jixie Gongcheng Cailiao* **41** (2017), DOI: **10.11973/jxgccl201708002**. (nianrunUnknownyearresearchprogressof pages 1-4, nianrunUnknownyearresearchprogressof pages 4-7, nianrunUnknownyearresearchprogressof media 39024751)

| Alloy / constraint | Se (wt%) | Bi (wt%) | Status and relevance | Source |
|---|---:|---:|---|---|
| SeBiLOY C89510 | 0.35–0.75 | 0.5–1.5 | Cast free-machining plumbing/gunmetal alloy; not seawater NAB and not identified as Navy-certified | Zhou, 2017, DOI: 10.11973/jxgccl201708002 (nianrunUnknownyearresearchprogressof pages 1-4, nianrunUnknownyearresearchprogressof media 39024751) |
| SeBiLOY C89520 | 0.8–1.1 | 1.6–2.2 | Cast free-machining plumbing/gunmetal alloy; not seawater NAB and not identified as Navy-certified | Zhou, 2017, DOI: 10.11973/jxgccl201708002 (nianrunUnknownyearresearchprogressof pages 1-4, nianrunUnknownyearresearchprogressof media 39024751) |
| SeBiLOY C89550 | 0.01–0.1 | 0.6–1.2 | Cast free-machining brass; not seawater NAB and not identified as Navy-certified | Zhou, 2017, DOI: 10.11973/jxgccl201708002 (nianrunUnknownyearresearchprogressof pages 1-4, nianrunUnknownyearresearchprogressof media 39024751) |
| C49300 | ≤0.2 | 0.5–2.0 | Wrought Bi–Sn brass; Se is a secondary maximum, not a required addition; not seawater NAB or Navy-certified | Zhou, 2017, DOI: 10.11973/jxgccl201708002 (nianrunUnknownyearresearchprogressof pages 1-4) |
| Cu–Ni hot-workability screening ceiling | ≤0.006 (60 ppm) | — | Literature screening limit for harmful Se in Cu–Ni; reported by a study/review, **not** an ASTM composition specification or Navy certification | Riley and Makar, 1986, DOI: 10.1016/0361-3658(86)90066-4 (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6) |


*Table: Comparison of commercial free-machining copper-alloy selenium ranges with the much lower Cu–Ni hot-workability screening ceiling. The SeBiLOY values do not establish suitability for seawater NAB, DED, or Navy service.*

In cast **C89520**, the review describes discrete Bi and Zn–Se-rich particles associated with chip breaking; this identifies a **Zn–Se-rich phase**, but its text does not establish a uniquely quantified stoichiometric compound or show the same phase in Zn-free marine alloys. It reports that Se evaporates during melting and complicates composition control. [NUMBERS] The review reports approximately **75%** relative machinability for C89510 and **85%** for C89520, against its stated machining comparator; these are **not corrosion measurements**. Its observation that Bi–Se casting alloys may be difficult to weld cannot be assigned to Se alone because Bi, Zn, Sn, and solidification conditions also differ. [CITE] Zhou (2017), DOI: **10.11973/jxgccl201708002**. (nianrunUnknownyearresearchprogressof pages 1-4, nianrunUnknownyearresearchprogressof pages 4-7)

[NAVY][GAP] The evidence examined does **not** identify Se as a specified intentional constituent of **C71500/C70600**, **C95800 NAB**, or an ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl Navy repair filler. Nor does it verify a Se limit from **ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, or EN 12449**. A grade not specifying Se is *not* proof that its Se content is zero. Confirm the purchased edition and product form before representing any of these specifications as setting a Se limit. The C895xx ingot ranges do not certify Navy or seawater service. (nianrunUnknownyearresearchprogressof pages 1-4, nianrunUnknownyearresearchprogressof pages 4-7)

## 2. Seawater corrosion

[GAP] No controlled Se-versus-Se-free experiment was retrieved for these copper-alloy families in natural seawater, ASTM D1141 water, or **3.5 wt% NaCl**. Consequently, **no quantitative Se-dependent** corrosion-rate, *E*₍corr₎, film-resistance, pit-depth, crevice, selective-attack, erosion-corrosion, or flow-velocity benefit or harm can be assigned. There is **no established helpful concentration interval** and **no corrosion-derived harmful threshold**. Plumbing-alloy machinability and drinking-water suitability cannot establish as-deposited C71500-equivalent marine performance; the proposed OCP, polarization/EIS, and 30-day depth-of-attack comparison remains necessary. (nianrunUnknownyearresearchprogressof pages 1-4, nianrunUnknownyearresearchprogressof pages 4-7)

## 3. DED, welding, and repair interfaces

[CITE][NUMBERS] The strongest directly relevant metallurgical warning is Riley and Makar’s Cu–Ni **0.006 wt% Se** hot-workability control. Their discussion associates poorly soluble, segregating impurity phases with loss of ductility, but its detailed **low-temperature liquid-film/fire-cracking example concerns Pb**, not a measured Cu–Se liquid-film temperature. **Hot rolling is not laser DED:** Se enrichment in the final interdendritic liquid could plausibly increase solidification-crack susceptibility; remelting or reheating enriched boundaries could plausibly contribute to interlayer liquation cracking. Neither mechanism nor a Se-specific critical concentration has been demonstrated here for DED. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6)

[GAP] No retrieved Se-resolved study of ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl weld deposits quantifies Se effects on hot cracking, reheated-layer cracking, or porosity. The Bi–Se plumbing-casting welding caution is **indirect, confounded evidence**, not a filler qualification. For repairs, Cu–Ni substrate dilution can raise local Ni even if the feed powder is nominally Ni-lean; cast NAB dilution introduces Al, Ni, Fe, and potentially existing interdendritic heterogeneity. These are reasons to assay Se and inspect **interfaces and remelted layers**, not evidence that Ni or Al chemically neutralizes it. Evaporation-driven Se loss, oxidation products, and vapor-related pores under the approximately **1.07 μm** laser are hypotheses requiring powder/deposit mass balance, fume collection, and metallography. (riley1986impurityeffectsin pages 3-4, nianrunUnknownyearresearchprogressof pages 1-4, nianrunUnknownyearresearchprogressof pages 4-7)

## 4. Melting, atomization, phase equilibria, and CALPHAD

[CITE] The reported volatility of Se during **conventional Bi–Se brass melting** supports minimizing intentional Se in an induction-melt/ultrasonic-atomization campaign and verifying Se by analysis both **before and after atomization**. [GAP] No retrieved measurement establishes Se evaporation rate, oxygen uptake, surface-tension shift, sonotrode wetting or wear, or reactions with **alumina, zirconia, graphite, Ti alloy, or Mo** for the specified Cu-rich melt and argon process. Do not present plausible crucible/sonotrode contamination or fume mechanisms as observed failures. [CITE] Zhou (2017), DOI: **10.11973/jxgccl201708002**. (nianrunUnknownyearresearchprogressof pages 1-4)

[GAP] The sources establish that Se is essentially an insoluble-second-phase addition in copper and that Cu–Se-containing chalcogenide equilibria exist; they do **not** provide an auditable maximum equilibrium **Se solubility in Cu in wt% at a stated temperature**, a validated Cu-rich eutectic temperature/composition, or a usable Cu-rich liquidus calculation. Assigning an exact solubility, invariant reaction, or Cu₂Se melting datum from semiconductor-chalcogenide work to dilute, multicomponent Cu–Ni–Al bronze would be unsound. Likewise, the evidence does not verify usable **Cu–Se, Cu–Ni–Se, or Cu–Al–Se assessments** in the installed Thermo-Calc **TCCU**, COST 531, or an identified compatible published TDB. Inspect the licensed database’s element/phase coverage and calculate a baseline **with Se omitted or explicitly marked unmodeled**; pycalphad cannot infer missing assessed parameters. No evidence suggests trace Se raises a Cu-rich liquidus **above 1,250 °C**, but a numeric shift or process-superheat guarantee cannot be claimed. [CITE] Copper Development Association, *High Conductivity Coppers*; Babanly *et al.*, “Complex copper-based chalcogenides: a review of phase equilibria and thermodynamic properties,” *Condensed Matter and Interphases* **26** (2024), 579–619, DOI: **10.17308/kcmf.2024.26/12367**. (coppers1999copperdevelopmentassociation pages 50-53, babanly2024complexcopperbasedchalcogenides pages 1-2)

## 5. Supply, price, and safety

[CITE] Selenium is commonly recovered **as a by-product of copper refining**, so specifying it is not a demonstrated route to reducing primary critical-mineral dependence. USGS’s **2025 technical recommendation** explicitly added copper; that recommendation must not be confused with the legally operative **final 2025 list**. The examined USGS sources establish a 60-commodity final list but did not furnish a reliable *text-readable selenium-specific listing* or a direct 2022-versus-final-2025 Se comparison; **Se’s formal status on each list remains unverified here**, rather than inferred from a periodic-table image. [CITE] Reich and Simon, “Critical Minerals,” *Annual Review of Earth and Planetary Sciences* (2025), DOI: **10.1146/annurev-earth-040523-023316**; Nassar *et al.*, USGS Open-File Report **2025–1047**, DOI: **10.3133/ofr20251047**; USGS, *Critical Minerals Memory Match Game*, General Information Product **266** (2026), DOI: **10.3133/gip266**. (nassar2025methodologyandtechnical pages 9-10, olinger2026criticalmineralsmemory pages 1-2, reich2025criticalminerals pages 5-6)

[NUMBERS] Zhou reports an indicative historical selenium price of approximately **CNY 100,000 per metric tonne = CNY 100/kg** for its 2017 context; this is **not a current USD/kg quotation**, and no defensible current price was verified. [NUMBERS][CITE] A toxicology chapter reports the **OSHA PEL for Se and its compounds as 0.2 mg/m³**; it describes respiratory/mucosal effects from inhaled Se vapor and systemic effects at high exposure. Powder-transfer enclosures, local capture of atomizer and laser fumes, exposure monitoring, and appropriate waste characterization are therefore warranted; **0.2 mg/m³ is an airborne-exposure limit, not an alloy-composition limit**. [GAP] No Se-specific RoHS/REACH prohibition or Navy procurement prohibition was verified; do not equate restrictions on Pb in drinking-water components with a Se ban. [CITE] Zhou (2017), DOI: **10.11973/jxgccl201708002**; Kodali, Erdely and Zeidler-Erdely, “Toxicity of Airborne Metals,” *Reference Module in Biomedical Sciences* (2026), DOI: **10.1016/B978-0-323-95488-4.00102-9**. (nianrunUnknownyearresearchprogressof pages 1-4, elesh1979healthhazardevaluation pages 4-6, kodali2026toxicityofairborne pages 5-6)

## 6. Bounds and joint constraints

[NUMBERS] **LIMIT:** specify **Se ≤0.006 wt% (≤60 ppm)** in *both* purchased/atomized powder and measured as-deposited material as a **provisional Cu–Ni-derived maximum** for the cross-family repair program. Apply the same screening value to NAB-side deposits for procurement simplicity, while acknowledging that it is **not an experimentally established NAB limit**. Set **no intentional Se target, conservative addition maximum, aggressive addition maximum, or functional floor**. The limiting failure mode is **Cu–Ni hot-ductility loss**, with DED solidification/reheat cracking a plausible but unquantified extension. A tighter limit can be adopted after validated crack and marine-corrosion comparisons, not asserted from current evidence. [CITE] Riley and Makar (1986), DOI: **10.1016/0361-3658(86)90066-4**. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6)

[NUMBERS][GAP] For a later joint-constraint screen, keep **Se separately from Bi, Te, Pb, and S** as potential concurrent hot-ductility risks rather than inventing an allowable sum. Riley and Makar also cite **Bi 0.001 wt%** and **Te 0.003 wt%** Cu–Ni controls alongside **Se 0.006 wt%**; these are *individual reported controls*, not a proven substitution ratio. Bi:Se of approximately **2:1 or higher** is described for free-machining SeBiLOY castings, but applying it to Ni-bearing DED would deliberately introduce Bi and is inappropriate. No validated **Se/Ni, Se/Fe, Se/Mn, or Se/Al** neutralization, phase-selection, or corrosion-resistance ratio was found. (riley1986impurityeffectsin pages 3-4, riley1986impurityeffectsin pages 4-6, nianrunUnknownyearresearchprogressof pages 1-4)

**Evidence quality:** **thin for the proposal’s decision**, despite a concrete older Cu–Ni hot-workability warning and well-documented SeBiLOY casting compositions. The central missing links are Se-controlled DED/weld cracking tests, composition-matched as-deposited seawater experiments, dilute-Cu phase/thermodynamic measurements, and verified current product-standard limits. (riley1986impurityeffectsin pages 3-4, nianrunUnknownyearresearchprogressof pages 1-4)

VERDICT | Se | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.006 | evidence=thin

References

1. (riley1986impurityeffectsin pages 3-4): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

2. (riley1986impurityeffectsin pages 4-6): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

3. (coppers1999copperdevelopmentassociation pages 50-53): High Conductivity Coppers. Copper development association. ArXiv, Jun 1999. URL: https://doi.org/10.1108/acmm.1999.12846cab.036, doi:10.1108/acmm.1999.12846cab.036. This article has 1 citations.

4. (riley1986impurityeffectsin pages 1-3): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

5. (mcmahon1965informationcircular8225 pages 18-20): AD McMahon. Information circular 8225: copper: a materials survey. Unknown journal, 1965.

6. (nianrunUnknownyearresearchprogressof pages 1-4): Z Nianrun. Research progress of free-cutting unleaded bismuth brass for sanitary ware industry. Unknown journal, Unknown year. URL: https://doi.org/10.11973/jxgccl201708002, doi:10.11973/jxgccl201708002.

7. (nianrunUnknownyearresearchprogressof pages 4-7): Z Nianrun. Research progress of free-cutting unleaded bismuth brass for sanitary ware industry. Unknown journal, Unknown year. URL: https://doi.org/10.11973/jxgccl201708002, doi:10.11973/jxgccl201708002.

8. (nianrunUnknownyearresearchprogressof media 39024751): Z Nianrun. Research progress of free-cutting unleaded bismuth brass for sanitary ware industry. Unknown journal, Unknown year. URL: https://doi.org/10.11973/jxgccl201708002, doi:10.11973/jxgccl201708002.

9. (babanly2024complexcopperbasedchalcogenides pages 1-2): Mahammad B. Babanly, Leyla F. Mashadieva, Samira Z. Imamaliyeva, Dunya M. Babanly, Dilgam B. Taghiyev, and Yusif A. Yusibov. Complex copper-based chalcogenides: a review of phase equilibria and thermodynamic properties. Kondensirovannye sredy i mezhfaznye granitsy = Condensed Matter and Interphases, 26:579-619, Oct 2024. URL: https://doi.org/10.17308/kcmf.2024.26/12367, doi:10.17308/kcmf.2024.26/12367. This article has 19 citations.

10. (nassar2025methodologyandtechnical pages 9-10): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

11. (olinger2026criticalmineralsmemory pages 1-2): Danielle A. Olinger. Critical minerals memory match game. General Information Product, Jan 2026. URL: https://doi.org/10.3133/gip266, doi:10.3133/gip266. This article has 0 citations.

12. (reich2025criticalminerals pages 5-6): Martin Reich and Adam C. Simon. Critical minerals. Annual Review of Earth and Planetary Sciences, Dec 2025. URL: https://doi.org/10.1146/annurev-earth-040523-023316, doi:10.1146/annurev-earth-040523-023316. This article has 120 citations and is from a highest quality peer-reviewed journal.

13. (elesh1979healthhazardevaluation pages 4-6): WE Elesh and BJ Gunter. Health hazard evaluation determination report no. 78-136-643: kennecott smelter: garfield, utah. Unknown journal, 1979.

14. (kodali2026toxicityofairborne pages 5-6): Vamsi K. Kodali, Aaron Erdely, and Patti C. Zeidler-Erdely. Toxicity of Airborne Metals. Elsevier, Jan 2026. URL: https://doi.org/10.1016/b978-0-323-95488-4.00102-9, doi:10.1016/b978-0-323-95488-4.00102-9. This article has 0 citations.
