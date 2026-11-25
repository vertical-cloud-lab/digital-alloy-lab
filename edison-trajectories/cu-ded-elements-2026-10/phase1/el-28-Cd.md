<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 3df9fabf-2a1f-4c2a-829c-4d6938a091fe
- Submitted: 2026-10-17T19:00:12Z
- Fetched: 2026-10-17T19:28:07Z (status: success)
- Raw trajectory JSON: ../raw/el-28-Cd.json.gz
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

ELEMENT UNDER REVIEW: Cd (impurity / free-machining). Cadmium copper C16200 (0.7-1.2 Cd); toxic, restricted (RoHS, OSHA); boils at 767 C.

Answer for Cd specifically, not for copper alloys in general:
1. ROLE: what Cd does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Cd ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Cd changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Cd, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Cd, Cu-Ni-Cd and Cu-Al-Cd are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Cd in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Cd neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Cd | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Cd (impurity / free-machining). Cadmium copper C16200 (0.7-1.2 Cd); toxic, restricted (RoHS, OSHA); boils at 767 C.

Answer for Cd specifically, not for copper alloys in general:
1. ROLE: what Cd does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Cd ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Cd changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Cd, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Cd, Cu-Ni-Cd and Cu-Al-Cd are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Cd in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Cd neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Cd | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Cd in copper-alloy powder for marine laser DED

**Decision—LIMIT Cd as an impurity; do not design it into either the Cu–Ni or aluminum-bronze palette.** Cadmium’s documented copper-alloy benefit is strength with relatively little loss of electrical conductivity in historical conductor alloys, not demonstrated as-deposited seawater resistance. The Copper Development Association (CDA) also specifically warns about toxic Cd vapor during copper-alloy melting and casting. A fusion-welding review says Cd evaporates at welding temperatures; it does **not** establish that a Cd-containing DED powder makes a sound or corrosion-resistant deposit. With no verified Cd-dependent marine performance gain to offset vapor loss and exposure risk, an intentional addition is not justified for this process. [CITE] CDA, *High Conductivity Coppers*, copper-cadmium section (1999), DOI: 10.1108/acmm.1999.12846cab.036; Czajkowski and Butters, *Investigation in Hardsurfacing a Nickel-Copper Alloy (Monel 400)*, Brookhaven National Laboratory report (2001), DOI: 10.2172/791763. (coppers1999copperdevelopmentassociation pages 50-53, czajkowski2001investigationinhardsurfacing pages 51-55)

The evidence matrix separates established facts from the particularly important missing experiments.

| Topic | Quantitatively supported fact | What remains unverified | Evidence source / DOI |
|---|---|---|---|
| Historical Cu–Cd electrical alloy | Cd strengthens Cu with less conductivity loss than many solutes; historical uses were catenary, trolley and telephone wire, and heat-exchanger fins. The user-provided C16200 range is **0.7–1.2 wt% Cd**, but the accessible CDA table did not expose that row, so this is **not independent specification verification**. | No demonstrated seawater-corrosion function; no verified Navy application; no basis for calling Cd a free-machining addition in C16200. | Copper Development Association, *High Conductivity Coppers* (coppers1999copperdevelopmentassociation pages 50-53); DOI: **10.1108/ACMM.1999.12846CAB.036** |
| Marine Cu–Ni, NAB and Mn–Al bronze | No retrieved ASTM, MIL, Navy, or peer-reviewed source identified Cd as a specified addition or quantified a beneficial range in these families. | Cd-dependent corrosion rate, *E*<sub>corr</sub>, polarization resistance, pitting/crevice behavior, selective attack, erosion–corrosion velocity, film chemistry, deoxidation, grain refinement, or dealloying inhibition in seawater/3.5 wt% NaCl. | Evidence gap; the accessible copper-corrosion handbook establishes general marine-alloy context but no Cd effect. Arthur Cohen, *Corrosion of Copper and Copper Alloys*; DOI: **10.31399/ASM.HB.V13B.A0003816** |
| Tin bronze, gunmetal and brasses | No retrieved commercial or Navy specification verified an intentional Cd range or marine-corrosion role. | Whether trace Cd changes dezincification, dealuminification, tin-bronze film chemistry, pitting, erosion–corrosion, or weldability. | **[GAP]** No Cd-controlled marine-alloy study or applicable specification located. |
| Cu–Ni–Sn and Cu–Ni–Si | No retrieved source established Cd-containing commercial grades or a precipitation reaction involving Cd in these systems. | Cd partitioning to existing precipitates, formation of Cd-bearing phases, cracking response, and seawater performance. | **[GAP]** No direct evidence located. |
| Welding and DED | A BNL review states that Cd “usually causes no ill effects” in fusion welding because it **evaporates at welding temperatures**; this was background literature, not a Cd-bearing weld experiment. | Deposit retention, solidification/liquation cracking, porosity, keyhole instability, layer-reheating effects, composition gradients, and corrosion of Cd-bearing laser DED. Evaporation is **not evidence of sound DED deposits**. | Czajkowski & Butters, *Investigation in Hardsurfacing a Nickel-Copper Alloy (Monel 400)* (czajkowski2001investigationinhardsurfacing pages 51-55); DOI: **10.2172/791763** |
| Dilution into C95800 or C71500 | No quantified Cd-dilution study was found. Because Cd is volatile, nominal powder Cd cannot be assumed to equal retained weld/deposit Cd. | Partitioning and vapor loss across the fusion boundary; effects on NAB κ phases or Cu–Ni solid solution; galvanic and selective-attack consequences. | **[GAP]** No Cd-bearing DED, ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl dilution experiment located. |
| Induction melting and ultrasonic atomization | CDA explicitly warns of toxic Cd vapor during melting and casting; Cd boils at **767 °C** according to the problem context, far below the proposed Cu-alloy melt temperature. | Quantitative Cd recovery, oxidation, droplet chemistry, surface tension, or reactions with alumina, zirconia, graphite, Ti-alloy or Mo sonotrodes on rePOWDER equipment. | Copper Development Association (coppers1999copperdevelopmentassociation pages 50-53); DOI: **10.1108/ACMM.1999.12846CAB.036** |
| Cu–Cd phase diagram and CALPHAD | A published binary Cu–Cd thermodynamic assessment exists. | Exact maximum Cu-rich solid solubility and temperature, invariant reactions, intermetallic stability, validated Cu–Ni–Cd/Cu–Al–Cd descriptions, and implementation in Thermo-Calc TCCU or COST 531 were not verified from accessible primary text. | Chen et al., “Thermodynamic assessment of Cu–Cd system,” *Transactions of Nonferrous Metals Society of China* **20** (2010) 649–654; DOI: **10.1016/S1003-6326(09)60193-X** |
| Liquidus constraint | No evidence indicates that trace Cd raises a Cu-rich alloy liquidus above **1,250 °C**; volatility, rather than excessive liquidus, is the evident processing constraint. | Quantitative multicomponent liquidus shifts in Cu–Ni–Cd and Cu–Al–Cd and useful atomization superheat after Cd loss. | Binary assessment identified above; multicomponent data remain **[GAP]**. DOI: **10.1016/S1003-6326(09)60193-X** |
| Occupational exposure and laser fume | OSHA Cd PEL reported as **0.005 mg/m³ (5 µg/m³), 8 h TWA**; study action level was one-half, **0.0025 mg/m³**. CdO is classified as carcinogenic and can cause severe delayed pulmonary edema, emphysema and kidney injury. | Process-specific Cd/CdO emission rate for fiber-laser DED and ultrasonic atomization. | Siert occupational-exposure study (siert2001exposureassessmentand pages 132-135); Spiegel-Ciobanu et al., *Hazardous Substances in Welding and Allied Processes* (spiegelciobanu2020hazardoussubstancesin pages 35-38); DOI: **10.1007/978-3-030-36926-2** |
| RoHS and REACH | RoHS2 limits Cd to **0.01 wt% (100 ppm)** in homogeneous material for **in-scope electrical/electronic equipment**, subject to exemptions. It is not a universal powder, naval-alloy, ASTM, MIL, or Navy limit. | Product-scope determination, exemptions, REACH authorization/restriction duties, and any Navy-specific prohibition for the proposed repair alloy. | Miehe et al. (miehe2015integratedhazardousmaterials pages 2-3); DOI: **10.1007/S40684-015-0035-6** |
| Critical-mineral status | The complete final **2025** U.S. list contains Cu and Ni but **not Cd**. | Cd status on the **2022** list was not independently confirmed from the primary list and should not be asserted from the retrieved material. | USGS final-2025 list reproduced in the mining review (staff2022usgsminingreview pages 6-9, staff2022usgsminingreview pages 9-11); methodology DOI: **10.3133/OFR20251047** |
| Proposed bounds | **Decision: LIMIT as impurity only. Proposed powder and deposit maximum: 0.01 wt% Cd (100 ppm)** as a conservative procurement/project limit aligned with the RoHS threshold where applicable—not as an ASTM, AWS, MIL, or Navy specification. Designed-addition conservative maximum, aggressive maximum, and functional floor: **NA**. | Whether an even lower analytical/action limit is required by the atomizer’s industrial-hygiene assessment; lot-to-lot retention and fume mass balance. | Regulatory benchmark: Miehe et al. (miehe2015integratedhazardousmaterials pages 2-3), DOI: **10.1007/S40684-015-0035-6**; processing hazard: CDA (coppers1999copperdevelopmentassociation pages 50-53), DOI: **10.1108/ACMM.1999.12846CAB.036** |


*Table: Cd-specific evidence matrix separating demonstrated quantitative facts from unverified marine-alloy, DED, atomization, and CALPHAD claims. It supports treating Cd as a controlled impurity rather than a designed addition.*

## 1. Role, alloys, and specifications

[CITE] **Established role.** CDA describes Cu–Cd as a *non-heat-treatable, high-conductivity* alloy: Cd strengthens Cu while impairing conductivity less than many other additions. Its reported applications are catenary, trolley and telephone wires and heat-exchanger fins—not qualified seawater repair deposits. CDA discusses free-machining copper separately and attributes its machinability to relatively insoluble additions such as S, Te, Se or Pb; its Cu–Cd account does not establish Cd as a free-machining agent or deoxidizer. CDA instead identifies P, B and Li as copper deoxidants. [GAP] No retrieved evidence demonstrates that Cd refines grains, improves a seawater protective film, inhibits dezincification/dealuminification, or forms useful Cd-containing strengthening precipitates in the proposed deposits. CDA, *High Conductivity Coppers*, DOI: 10.1108/acmm.1999.12846cab.036. (coppers1999copperdevelopmentassociation pages 50-53, coppers1999copperdevelopmentassociation pages 47-50)

[NUMBERS] **Commercial grade distinguished from a marine qualification:** the supplied C16200 designation and **0.7–1.2 wt% Cd** range describe historical cadmium copper, but the accessible CDA text did not expose its composition-table row; that range was **not independently checked against a current UNS/CDA or ASTM specification** in this search. [SPEC][NAVY][GAP] No intentional Cd range was verified for seawater-service Cu–Ni, nickel-aluminum bronze (NAB), Mn–Al bronze, tin bronze/gunmetal, brasses, Cu–Ni–Sn or Cu–Ni–Si; nor for ASTM B111, B171, B466, B148 or B369, MIL-T-16420, MIL-B-24480 or MIL-C-15726, AWS A5.7, or EN 12449. The retrieved sources likewise do not verify a Cd-bearing Navy filler or a Cd maximum in those documents. **An element missing from a listed nominal composition is not proof of an independently specified zero-Cd limit.** CDA, *High Conductivity Coppers*, DOI: 10.1108/acmm.1999.12846cab.036. (coppers1999copperdevelopmentassociation pages 50-53)

## 2. Seawater corrosion

[GAP] No controlled Cd-series measurements were retrieved for these copper-alloy families in natural seawater, ASTM D1141 water or **3.5 wt% NaCl**. Consequently, there is **no defensible Cd wt% interval known to improve seawater performance**, nor a measured interval at which Cd worsens it. Specific Cd-dependent corrosion rates, *E*₍corr₎ shifts, film/charge-transfer resistances, pit or crevice depths, dezincification/dealuminification depths, erosion–corrosion rates and allowable water velocities cannot be supplied. In particular, C16200’s electrical service does not demonstrate parity with wrought C71500 in a 30-day as-deposited immersion test. Do not import results for **Cd-plated steel**, Cd ions dissolved in the electrolyte, or Zn–Cd galvanizing baths as results for Cd *alloyed into copper*. The accessible CDA account supports the distinction between historical conductor performance and an untested marine-corrosion claim. CDA, *High Conductivity Coppers*, DOI: 10.1108/acmm.1999.12846cab.036. (coppers1999copperdevelopmentassociation pages 50-53)

## 3. DED, joining, and repair dilution

[CITE][NAVY] Brookhaven’s Monel 400 hardfacing report states that Cd “usually causes no ill effects” during fusion welding **because it evaporates from the copper at welding temperatures**. This is a general welding statement, **not** a Cd-bearing weld or laser-DED comparison: the reported material analyses did not identify Cd as an experimental variable. It cannot be read as evidence of retained composition, freedom from solidification cracks or safety. The same discussion names Sb, As, P, Bi, Se, S and Te—not Cd—as possible hot-cracking contributors in Ni-containing copper alloys; those warnings do not quantify a Cd interaction. Czajkowski and Butters, Brookhaven report, DOI: 10.2172/791763. (czajkowski2001investigationinhardsurfacing pages 51-55)

[GAP] No Cd-specific measurements were found for DED solidification cracking, reheated-layer liquation cracking, keyhole/gas porosity, evaporation fraction, oxide-inclusion loading, or chemistry and corrosion across a deposited-Cd/C95800 or deposited-Cd/C71500 fusion boundary. Vapor generation makes powder-to-deposit Cd retention **uncertain** and provides a plausible porosity and fume hazard, not a demonstrated defect rate. Dilution into NAB could change local Al/Ni/Fe/Mn chemistry, whereas dilution into wrought Cu–Ni changes local Ni/Fe/Mn chemistry; no Cd–substrate interaction or quantitative dilution threshold was established. Nor was a Cd-bearing comparison verified for ERCuNi, ERCuAl-A2, ERCuNiAl or ERCuMnNiAl. These are **welding-derived cautions where AM evidence is missing**, not claimed filler specifications. Brookhaven report, DOI: 10.2172/791763. (czajkowski2001investigationinhardsurfacing pages 51-55)

## 4. Powder manufacture, phase relations, and CALPHAD

[NUMBERS] Cd’s approximately **767 °C** normal boiling point, given in the process brief, is below both the planned melt temperature and the Cu melting point. The direct CDA warning is that melting/casting Cu–Cd produces toxic vapor. Thus a nominal Cd charge cannot be equated with Cd in a 0.5-kg atomized powder lot, let alone Cd retained after a 1.07-µm laser pass. Charge, residual melt, collected powder, deposits and captured fume would all require Cd mass-balance assays. CDA, *High Conductivity Coppers*, DOI: 10.1108/acmm.1999.12846cab.036; Brookhaven report, DOI: 10.2172/791763. (coppers1999copperdevelopmentassociation pages 50-53, czajkowski2001investigationinhardsurfacing pages 51-55)

[GAP] Quantitative Cd oxidation loss; reactions with alumina, zirconia, graphite, a Ti-alloy or Mo sonotrode; Cd-dependent liquid surface tension, droplet size and oxide skins; and performance on the specified ultrasonic atomizer were **not established**. It would be unsound to assign any crucible/sonotrode compatibility coefficient or claim Cd reduces surface tension by a particular amount. [CITE] A published **binary Cu–Cd thermodynamic assessment** exists: Chen, Liu, Zhang, Bo and Jin, “Thermodynamic assessment of Cu–Cd system,” *Transactions of Nonferrous Metals Society of China* **20** (2010), 649–654, DOI: 10.1016/S1003-6326(09)60193-X. Its full assessment was not accessible here. Accordingly, **maximum Cu-rich solid solubility (wt% and temperature), exact invariant temperatures/compositions, and the identity/stability of any Cu–Cd intermetallics remain unverified**; no numerical phase boundary should be guessed. Published binary assessment is not proof that assessed Cu–Ni–Cd or Cu–Al–Cd ternaries—or even a usable Cd constituent—are installed in the local Thermo-Calc **TCCU** or **COST 531** database. [GAP] Check actual database constituent coverage and version before running Thermo-Calc or pycalphad. Neither a Cd-induced liquidus crossing of the **1,200–1,250 °C** usable-superheat ceiling nor a measured multicomponent liquidus shift was documented; the directly supported Cd-specific obstacle is volatilization. CDA, *High Conductivity Coppers*, DOI: 10.1108/acmm.1999.12846cab.036. (coppers1999copperdevelopmentassociation pages 50-53)

## 5. Supply, worker protection, and regulatory meaning of a limit

[NUMBERS][CITE] The reproduced **2025 final U.S. critical-minerals list** contains **Cu and Ni, but not Cd**; USGS assessed Cd as a commodity, which must not be confused with inclusion on the final list. The **2022 Cd status was not verified from the primary 2022 list** in this search. USGS, Nassar *et al.*, *Methodology and Technical Input for the 2025 U.S. List of Critical Minerals*, Open-File Report 2025–1047, DOI: 10.3133/ofr20251047; *Annual Review 2025: Mining*, reproduced final-list Table 3, citing **90 FR 50494**. [GAP] A date- and form-specific, verifiable metal-Cd **USD/kg price** was not obtained; no numerical quotation is warranted, and metal price would omit containment, analytical and waste-management costs. (nassar2025methodologyandtechnical pages 33-35, staff2022usgsminingreview pages 6-9, staff2022usgsminingreview pages 9-11)

[NUMBERS][CITE] The cited occupational-exposure compilation reports the OSHA Cd permissible exposure limit as **0.005 mg/m³ (5 µg/m³), 8-h time-weighted average**; this is an **air concentration, not an allowable alloy composition**. The study’s half-limit action threshold corresponds to **2.5 µg/m³**. CdO-bearing welding fume is carcinogenic and can cause delayed severe lung injury and kidney damage. Treat collected fines and exhaust filters as a Cd exposure/waste concern; assess engineering capture and personal exposure for melting, atomization, powder transfer, DED and cleanup. Siert, *Exposure Assessment and Longitudinal Pulmonary Function of Electric Utility Power Plant Maintenance Welders* (2001); Spiegel-Ciobanu, Costa and Zschiesche, *Hazardous Substances in Welding and Allied Processes* (2020), DOI: 10.1007/978-3-030-36926-2. [NAVY][GAP] No specific Navy prohibition on Cd *alloying in these powders* was verified; historical military Cd **plating** rules must not be presented as alloy rules. (siert2001exposureassessmentand pages 132-135, spiegelciobanu2020hazardoussubstancesin pages 35-38)

[SPEC][NUMBERS] EU **RoHS 2011/65/EU** sets **0.01 wt% Cd (100 ppm)** in homogeneous material for *covered electrical/electronic equipment*, subject to applicable exemptions. It is **not** an ASTM/AWS/MIL requirement or a universal prohibition on naval repair powder. REACH **Regulation (EC) 1907/2006** has separate substance, article-information, authorization and restriction duties; do not substitute an article-notification threshold for RoHS’s Cd-in-homogeneous-material limit. Miehe *et al.*, “Integrated hazardous materials management,” *International Journal of Precision Engineering and Manufacturing–Green Technology* **2** (2015), 289–298, DOI: 10.1007/s40684-015-0035-6. (miehe2015integratedhazardousmaterials pages 2-3)

## 6. Bounds and later joint constraints

**Proposed procurement and acceptance rule—both families:** specify **Cd ≤0.01 wt% (≤100 ppm) in each powder lot *and* deposit**, with **no intentional Cd addition**. [SPEC] This is an explicitly **project-selected impurity ceiling benchmarked to the RoHS Cd threshold where RoHS applies**, *not* a limit extracted from ASTM B111/B171/B466/B148/B369, the listed MIL documents, AWS A5.7, EN 12449 or a Cd-specific DED study. Where the powder or repair is outside RoHS scope, its value is a conservative contractual choice rather than a statutory permission or occupational-safety guarantee. Verify the powder and representative deposited builds analytically; dilution and preferential Cd evaporation make a powder assay alone insufficient. [GAP] No retrieved study establishes the highest *technically tolerable* Cd concentration for either marine family. The failure modes motivating the project cap are avoidable carcinogenic fume, volatile-composition instability and unqualified as-deposited marine performance—not a proven crack-onset or corrosion threshold at 0.01 wt%. Miehe *et al.*, DOI: 10.1007/s40684-015-0035-6; CDA, DOI: 10.1108/acmm.1999.12846cab.036; Brookhaven report, DOI: 10.2172/791763. (miehe2015integratedhazardousmaterials pages 2-3, coppers1999copperdevelopmentassociation pages 50-53, czajkowski2001investigationinhardsurfacing pages 51-55)

**Designed-addition bounds:** conservative maximum **NA**, nonconservative maximum **NA**, functional floor **NA**, and applicable designed-addition family **none**. C16200’s supplied **0.7–1.2 wt% Cd** does not qualify as either bound for as-deposited marine Cu–Ni or NAB: it is a historical *conductor* composition, not a seawater/laser-processing benchmark. [GAP] No validated constraint of the form Cd+Ni, Cd+Fe, Cd+Mn, Cd+Al, Cd/Ni or Cd/Al was found; no Cd neutralization of harmful S/P/Bi or improvement of Cu–Ni/NAB seawater-film chemistry was shown. For later analysis, keep **Cd ≤0.01 wt% independently of the other alloying variables**, and treat any Cd-by-element hypothesis as unvalidated rather than assigning a synergistic coefficient. CDA, DOI: 10.1108/acmm.1999.12846cab.036; Brookhaven report, DOI: 10.2172/791763. (coppers1999copperdevelopmentassociation pages 50-53, czajkowski2001investigationinhardsurfacing pages 51-55)

**Evidence quality:** **thin for Cd-specific marine corrosion, powder atomization, DED integrity, ternary CALPHAD and quantitative phase boundaries; stronger for historical conductor function, evaporation warning, RoHS scope and fume hazard.** The apparent favorable weldability sentence is compatible with *loss of Cd by evaporation* and does not contradict the hazard-based exclusion from the designed palette. No publication by the identified PI is used. (coppers1999copperdevelopmentassociation pages 50-53, czajkowski2001investigationinhardsurfacing pages 51-55, spiegelciobanu2020hazardoussubstancesin pages 35-38, miehe2015integratedhazardousmaterials pages 2-3)

VERDICT | Cd | decision=LIMIT | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.01 | evidence=thin

References

1. (coppers1999copperdevelopmentassociation pages 50-53): High Conductivity Coppers. Copper development association. ArXiv, Jun 1999. URL: https://doi.org/10.1108/acmm.1999.12846cab.036, doi:10.1108/acmm.1999.12846cab.036. This article has 1 citations.

2. (czajkowski2001investigationinhardsurfacing pages 51-55): C. CZAJKOWSKI and M. BUTTERS. Investigation in hardsurfacing a nickel-copper alloy (monel400). ArXiv, Dec 2001. URL: https://doi.org/10.2172/791763, doi:10.2172/791763. This article has 5 citations.

3. (siert2001exposureassessmentand pages 132-135): AW Siert. Exposure assessment and longitudinal pulmonary function of electric utility power plant maintenance welders. Unknown journal, 2001.

4. (spiegelciobanu2020hazardoussubstancesin pages 35-38): Vilia Elena Spiegel-Ciobanu, Luca Costa, and Wolfgang Zschiesche. Hazardous substances in welding and allied processes. ArXiv, Jan 2020. URL: https://doi.org/10.1007/978-3-030-36926-2, doi:10.1007/978-3-030-36926-2. This article has 17 citations.

5. (miehe2015integratedhazardousmaterials pages 2-3): Robert Miehe, Sebastian Mueller, Ralph Schneider, Sylvia Wahren, and Markus Hornberger. Integrated hazardous materials management: combining requirements from various environmental legislations to enable effective business compliance processes in industries. International Journal of Precision Engineering and Manufacturing-Green Technology, 2:289-298, Jul 2015. URL: https://doi.org/10.1007/s40684-015-0035-6, doi:10.1007/s40684-015-0035-6. This article has 23 citations.

6. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

7. (staff2022usgsminingreview pages 9-11): US Staff. Usgs mining review. Unknown journal, 2022.

8. (coppers1999copperdevelopmentassociation pages 47-50): High Conductivity Coppers. Copper development association. ArXiv, Jun 1999. URL: https://doi.org/10.1108/acmm.1999.12846cab.036, doi:10.1108/acmm.1999.12846cab.036. This article has 1 citations.

9. (nassar2025methodologyandtechnical pages 33-35): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.
