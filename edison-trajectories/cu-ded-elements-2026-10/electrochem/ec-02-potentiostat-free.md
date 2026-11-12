<!--
Edison Scientific LITERATURE task (phase 4)
- Task ID: ae047073-dfe1-428f-a501-8ca6b9721354
- Submitted: 2026-10-17T19:03:34Z
- Fetched: 2026-10-17T19:28:18Z (status: success)
- Raw trajectory JSON: ../raw/ec-02-potentiostat-free.json.gz
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

LAB CONTEXT: the lab has a small open-frame gantry liquid handler (about
390 x 230 x 120 mm working volume; one head carrying a 20 uL pipette, a vial
capper and cameras; no tool changer; Python/YAML control software that drives
PalmSens EmStat and Admiral Squidstat potentiostats for OCP, CV,
chronoamperometry and chronopotentiometry, not yet EIS). It owns no
potentiostat and can borrow a conventional benchtop one. Specimens are small:
polished faces of DED single tracks, thin walls and blocks (a few mm to 20 mm
across), and cross-sections of repair coupons that cross the fusion line into
cast NAB or wrought Cu-Ni.

QUESTION: For ranking copper alloys (Cu-Ni, aluminum bronze, NAB) by seawater
corrosion, what can be measured WITHOUT a full potentiostat, and how well does
it agree with LPR, EIS and long immersion? Cover: (1) open-circuit potential
time series with a high-impedance voltmeter during immersion (film formation
and ennoblement of Cu-Ni over days); (2) metal release: copper and nickel
dissolved into the immersion solution, sampled in small aliquots over time
and measured by ICP-MS/OES or colorimetry (e.g. bathocuproine or
bicinchoninic acid for copper, dimethylglyoxime for nickel), including
published copper release rates of 90-10 and 70-30 Cu-Ni in seawater; (3)
mass loss of small coupons (ASTM G31/G1) and its detection limit for alloys
corroding at about 0.01-0.05 mm/yr; (4) image-based measures (corrosion
product color, area fraction attacked) and dealloying depth; (5) galvanic
coupling of a deposit to cast NAB or wrought Cu-Ni with a zero-resistance
ammeter, relevant to repairs; (6) low-cost open-source or module
potentiostats (Rodeostat, MYSTAT, EmStat Pico, ABE-Stat, KickStat or similar)
validated against commercial instruments for corrosion LPR or EIS. Which of
these could replace or supplement a one-hour electrochemical screen as a
cheap node in a cost-aware search, and which cannot? Give DOIs and numbers.

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

LAB CONTEXT: the lab has a small open-frame gantry liquid handler (about
390 x 230 x 120 mm working volume; one head carrying a 20 uL pipette, a vial
capper and cameras; no tool changer; Python/YAML control software that drives
PalmSens EmStat and Admiral Squidstat potentiostats for OCP, CV,
chronoamperometry and chronopotentiometry, not yet EIS). It owns no
potentiostat and can borrow a conventional benchtop one. Specimens are small:
polished faces of DED single tracks, thin walls and blocks (a few mm to 20 mm
across), and cross-sections of repair coupons that cross the fusion line into
cast NAB or wrought Cu-Ni.

QUESTION: For ranking copper alloys (Cu-Ni, aluminum bronze, NAB) by seawater
corrosion, what can be measured WITHOUT a full potentiostat, and how well does
it agree with LPR, EIS and long immersion? Cover: (1) open-circuit potential
time series with a high-impedance voltmeter during immersion (film formation
and ennoblement of Cu-Ni over days); (2) metal release: copper and nickel
dissolved into the immersion solution, sampled in small aliquots over time
and measured by ICP-MS/OES or colorimetry (e.g. bathocuproine or
bicinchoninic acid for copper, dimethylglyoxime for nickel), including
published copper release rates of 90-10 and 70-30 Cu-Ni in seawater; (3)
mass loss of small coupons (ASTM G31/G1) and its detection limit for alloys
corroding at about 0.01-0.05 mm/yr; (4) image-based measures (corrosion
product color, area fraction attacked) and dealloying depth; (5) galvanic
coupling of a deposit to cast NAB or wrought Cu-Ni with a zero-resistance
ammeter, relevant to repairs; (6) low-cost open-source or module
potentiostats (Rodeostat, MYSTAT, EmStat Pico, ABE-Stat, KickStat or similar)
validated against commercial instruments for corrosion LPR or EIS. Which of
these could replace or supplement a one-hour electrochemical screen as a
cheap node in a cost-aware search, and which cannot? Give DOIs and numbers.

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Potentiostat-free seawater screening of deposited copper alloys

**Conclusion.** A high-impedance open-circuit-potential (OCP) trace and standardized photographs are inexpensive *triage* measurements, not substitutes for a one-hour linear-polarization-resistance (LPR) or electrochemical-impedance-spectroscopy (EIS) screen. Serial dissolved-metal measurements provide a more relevant, but slower, measure of release; a deposit–substrate zero-resistance-ammeter (ZRA) test adds a repair-specific galvanic measurement. Thirty-day microscopy and, where detectable, cleaned-coupon mass loss remain the checks on localized damage and net metal consumption. There is no established numerical conversion from one-hour OCP or color to 30-day corrosion of as-deposited, single-stream, blown-powder laser DED Cu–Ni/NAB repairs. [GAP] (mantzavinos2001durabilitystudiesrelevant pages 123-128, song2024microstructuresandcorrosion pages 10-13, malaret2024semiquantitativecategorizationmethod pages 4-6, king1992thehotisostatic pages 43-49)

The measurements, their time scales, and their principal blind spots are compared here. **Numbers identified as calculated are detection estimates, not published release measurements.**

| Method / signal | Duration | Quantitative output | Agreement with electrochemical or immersion tests | Replace 1 h screen? | Main confound / control |
|---|---:|---|---|---|---|
| OCP time series with high-impedance voltmeter and stable reference | 1 h initial; **2–7 d** early film; weeks–months maturation | Potential and drift. Cu–10 wt% Ni measured about **−220 to −233 mV** in artificial seawater; polarization improved after **2 d** and further after **7 d**. Temperate-water Cu–Ni films mature in roughly **2–3 months**. (mantzavinos2001durabilitystudiesrelevant pages 123-128, powell2004corrosionandbiofouling pages 1-4) | Indicates film evolution and galvanic polarity, not corrosion rate. WAAM Cu–30 wt% Ni OCP values clustered near **−175 to −200 mV**, although EIS clearly distinguished film resistance. (song2024microstructuresandcorrosion media d9e0f494, song2024microstructuresandcorrosion media 65e1a8b7) | **No** alone; **yes** as a nearly free supplement and instability flag. | Reference drift, temperature, aeration, finish, crevices, and exposure age; compare identical histories and reference scales. |
| Dissolved Cu and Ni by ICP-MS/OES or matrix-validated colorimetry | **1–30 d** with serial aliquots | Cumulative release, interval flux, and Cu-to-Ni ratio. Analyze a **0.45 µm-filtered** aliquot for dissolved metal and a separately digested unfiltered aliquot for total recoverable metal. Reported **62 mg m⁻² d⁻¹** and **2,500 mg m⁻² d⁻¹** values were weight-loss or total-product rates, not measured dissolved-Cu fluxes. (cottrell2000zebramusseladhesion pages 150-155, malaret2024semiquantitativecategorizationmethod pages 4-6) | Integrates released metal and detects selective release, but may differ from mass loss because products remain on the surface, precipitate, become particulate, or adsorb to vessels. | **No** at 1 h for low-rate alloys; **strong multi-day supplement** when analyses are batched. | Seawater matrix, background metals, adsorption, precipitation, filtration, and aliquot depletion; validate bathocuproine, BCA, or DMG by spike recovery against ICP. |
| Coupon mass loss using ASTM G31 exposure and ASTM G1 cleaning | Preferably **30 d or longer** | Average penetration after product removal. **Calculated estimate:** one exposed **1 cm²** face at **8.9 g cm⁻³** loses only **0.073–0.366 mg** in 30 d at **0.01–0.05 mm y⁻¹**. Published quiet-seawater ranges are **0.2–0.6 mil y⁻¹** for 90–10 and **0.3–0.5 mil y⁻¹** for 70–30 Cu–Ni. (lewis1981evaluationofcoppernickel pages 43-48) | Best simple anchor for average long-term loss, but does not resolve kinetics or mechanism; cleaning error can dominate sub-milligram signals. (malaret2024semiquantitativecategorizationmethod pages 2-4, malaret2024semiquantitativecategorizationmethod pages 4-6) | **No** for 1 h; **yes** as a validation tier with sufficient area, duration, replication, and balance resolution. | Sound-metal loss during cleaning, retained products, exposed-area error, and edge crevices; use unexposed cleaning blanks and repeated cleaning cycles. |
| Standardized images of product color and attacked-area fraction | Hours to **30 d**, serial and nondestructive | Color coordinates, fraction attacked, pit density, and localization at melt pools, cracks, or fusion lines. Cu–Ni products can be brown, greenish-brown, or brownish-black. (powell2004corrosionandbiofouling pages 1-4) | Detects spatially localized failure that area-averaged LPR can miss, but color and area fraction do not uniquely determine penetration or polarization resistance. | **Supplement only**; suitable for automated cheap ranking, not stand-alone qualification. | Lighting, white balance, wet or dry state, deposits, roughness, and threshold selection; use fixed imaging and a color standard. |
| Metallographic dealloying or selective-attack depth | Destructive endpoint after **30 d or longer** | Maximum and mean depth across deposit, fusion line, substrate, phases, pores, and cracks. Cast NAB preferential attack at crevices and weld-affected zones has been reported near **1 mm y⁻¹**; a cast 70–30 Cu–Ni candidate showed **0.02 mm y⁻¹** average loss and **0.05 mm y⁻¹** maximum attack after one year. (king1992thehotisostatic pages 43-49) | Most relevant localized endpoint for repair integrity; LPR and EIS can miss deep attack occupying little area. | **No**; essential down-selection or validation endpoint for NAB repairs. | Section placement, polishing pullout, sparse attack statistics, pre-existing DED porosity, and unjustified linear extrapolation. |
| Deposit–substrate galvanic coupling with zero-resistance ammeter | Minutes initially; preferably **days–30 d** | Signed current, anodic-area-normalized current density, integrated charge, and individual potentials. Flowing-seawater potentials were about **−0.20 to −0.24 V vs SCE** for 70–30 and **−0.22 to −0.29 V vs SCE** for 90–10 Cu–Ni, depending on temperature. (beavers1980corrosionrelatedfailuresin pages 133-137) | Directly measures repair-specific coupling unavailable from separate OCP, LPR, or EIS specimens; prediction depends on reproducing repair geometry and area ratio. | **Yes** as a repair-specific adjunct; **no** for intrinsic resistance or localized attack. | Cathode-to-anode area ratio, edges, IR drop, oxygen transport, and evolving films; test realistic deposit-to-NAB and deposit-to-Cu–Ni ratios. |
| True potentiostat LPR and EIS at OCP | About **1 h** after controlled stabilization; repeat after aging | LPR gives polarization resistance; EIS separates solution and film-related contributions. WAAM Cu–30 wt% Ni film resistances spanned approximately **0.68–1.66 × 10⁵ Ω**, while OCP varied little. (song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion media d9e0f494) | Fast mechanistic ranker, but a 1 h result represents an immature Cu–Ni film and cannot guarantee 30 d loss or maximum dealloying depth. | **Reference screen**; calibrate cheaper nodes against it and against immersion endpoints. | Immature film, exposed-area definition, preparation, reference placement, equivalent-circuit ambiguity, and averaging over localized corrosion. |


*Table: Decision matrix comparing potentiostat-free and electrochemical screening nodes for Cu–Ni and NAB repairs. Calculated mass-loss detectability is distinguished from published measurements, and historical weight-loss values are not presented as dissolved-metal release.*

## 1. OCP: a nearly free film-history measurement, not a rate measurement

[CITE, NUMBERS] Measure the deposit against a stable Ag/AgCl reference with a high-input-impedance voltmeter, recording the reference construction, temperature, aeration, surface preparation and time since immersion. A reference and voltmeter measure potential without a *full* potentiostat; a potential difference between two exposed metals alone does not give either metal's corrosion current. In flowing seawater, reported potentials versus saturated calomel electrode (SCE) were −0.20, −0.24 and −0.22 V for approximately Cu–30 wt% Ni at 26.7, 17 and 6 °C, respectively; corresponding approximately Cu–10 wt% Ni values were −0.22, −0.29 and −0.24 V at 24, 17 and 6 °C. Neither a universal potential threshold nor a ranking that ignores temperature is justified. Beavers, Agrawal and Berry, *Corrosion-Related Failures in Power Plant Condensers*, final technical report (1980), DOI **10.2172/5047866**. (beavers1980corrosionrelatedfailuresin pages 133-137)

[CITE, NUMBERS] Film age matters more than a tidy one-hour endpoint. In artificial seawater at 20 °C, Cu–10 wt% Ni showed less active polarization after **2 days**, with stronger film-associated protection after **7 days**; a marine Cu–Ni review reports initial film formation over days and maturation over approximately **2–3 months** in temperate seawater. A cast approximately Cu–30 wt% Ni alloy's seawater potential was reported to shift from about **−0.180 to −0.100 V versus SCE** on prolonged exposure. Thus log OCP at one hour, one day, days 2–7 and during the immersion trial; an ennobling trend is evidence of changing surface chemistry, **not proof of decreasing dissolution**. Mantzavinos, *Durability Studies Relevant to Marine Equipment*, University of Glasgow thesis (2001), DOI **10.5525/gla.thesis.73974**; Powell, “Corrosion and Biofouling Resistance Evaluation of 90-10 Copper-Nickel” (2004 conference/review; **no DOI verified**); King, *The Hot Isostatic Processing Characteristics of 70/30 Cupronickel Castings* (1992 thesis; **no DOI verified**). (mantzavinos2001durabilitystudiesrelevant pages 123-128, powell2004corrosionandbiofouling pages 1-4, king1992thehotisostatic pages 43-49)

[CITE, NUMBERS] The directly relevant AM counterexample is Song *et al.*, “Microstructures and Corrosion Properties of Wire Arc Additive Manufactured Copper–Nickel Alloys,” *Materials* **17**, 876 (2024), DOI **10.3390/ma17040876**. In their **wire-arc**, not laser-powder, approximately Cu–30 wt% Ni material tested in **3.5 wt% NaCl, not ASTM D1141**, OCPs varied little between processing conditions while EIS fitted film resistances varied from roughly **0.68 to 1.66 × 10⁵ Ω** across specimens/planes. Do not use OCP to declare processing condition 6 equivalent to condition 1 simply because their potentials are close. (song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion pages 2-5, song2024microstructuresandcorrosion media d9e0f494)

## 2. Cu and Ni release: strong multi-day adjunct, but do not mislabel weight loss as dissolved copper

[CITE] Immerse measured exposed areas in separate, matched vessels of ASTM D1141 substitute ocean water; remove small, recorded-volume aliquots at fixed times, replacing solution if necessary and correcting the mass balance for every withdrawn aliquot. Quantify **both Cu and Ni** by ICP-MS or ICP-OES after appropriate seawater-matrix calibration. A filtered aliquot operationally measures dissolved metal; a separately digested, unfiltered aliquot measures more of the suspended/total-recoverable inventory. Vessel blanks, solution blanks, dilution/spike recoveries, adsorption to vessel walls and detached films are essential: dissolved inventory is not identical to metal removed from a specimen. A published gravimetric mass-balance treatment explicitly distinguishes metal remaining in adherent products, metal in solution and other losses. Malaret, “Semi-Quantitative Categorization Method for the Corrosion Behavior of Metals Based on Immersion Test,” *Metals* **14**, 409 (2024), DOI **10.3390/met14040409**. (malaret2024semiquantitativecategorizationmethod pages 4-6)

[NUMBERS] For each interval report the **blank-corrected, aliquot-corrected** change in solution metal mass divided by exposed area and elapsed days, separately in **mg m⁻² d⁻¹** for Cu and Ni; report cumulative mass as well. Compare with wrought C71500 under **the identical exposure**, rather than assuming the ion flux tracks alloy Ni wt% or LPR current. Bathocuproine or bicinchoninic-acid Cu assays and dimethylglyoxime Ni assays are plausible lower-instrument-cost *development options*, but the evidence obtained here does **not** establish their detection limits, selectivity or agreement with ICP in ASTM D1141 solution containing both metals and corrosion products. Validate each with matrix-matched blanks, additions and paired ICP measurements before ranking alloys. [GAP] (malaret2024semiquantitativecategorizationmethod pages 4-6)

[CITE, NUMBERS, GAP] **Published numbers frequently repeated as “copper release rates” require particular caution.** A secondary account attributes approximately **62 mg m⁻² d⁻¹** after five years to **90–10 and 70–30 Cu–Ni**, versus **186 mg m⁻² d⁻¹** for copper; it expressly says these derive from corrosion/weight-loss measurements that include oxide and both metals, **not measured dissolved Cu**. Its approximately **2,500 mg m⁻² d⁻¹** for Cu–30 wt% Ni over the last 11 days of a 16-day seawater exposure is likewise a *weight-loss* rate, not an ICP copper flux. Cottrell, *Zebra Mussel Adhesion and Aspects of Its Prevention Using Copper* (2000 thesis; **no DOI verified**), recounting Efird (1976) and LaQue and Clapp (1945). I did **not** verify defensible, separate, time-resolved dissolved-Cu release-rate numbers for seawater-exposed C70600 and C71500 in the available papers; supplying them as though the weight-loss numbers were dissolved Cu would be incorrect. [GAP] (cottrell2000zebramusseladhesion pages 150-155)

## 3. Gravimetry: a real endpoint, generally too insensitive at one hour

[SPEC, CITE, NUMBERS] ASTM **G31**, *Standard Guide for Laboratory Immersion Corrosion Testing of Metals*, governs immersion comparisons; ASTM **G1**, *Standard Practice for Preparing, Cleaning, and Evaluating Corrosion Test Specimens*, governs product removal and cleaning corrections. ASTM **G46** addresses pitting evaluation. These are **test-method standards, not C71500 acceptance-rate specifications**; no verified DOI for the individual ASTM editions is supplied here. Document area, duration, solution volume and preparation; photograph before removing the film, clean with matched unexposed control coupons, and report the repeatability of cleaning loss. Malaret (2024), DOI **10.3390/met14040409**, explains why retained product and removal of sound metal bias the result. (malaret2024semiquantitativecategorizationmethod pages 2-4, malaret2024semiquantitativecategorizationmethod pages 4-6)

[NUMBERS] **Detection calculation, not a standard-specified limit:** for one exposed **1 cm²** face and an assumed Cu-alloy density of **8.9 g cm⁻³**, a uniform rate of **0.01–0.05 mm y⁻¹** consumes only **0.073–0.366 mg in 30 days**; in **one hour**, only approximately **0.00010–0.00051 mg**. At 30 days, a hypothetical **0.1 mg** net-mass resolution corresponds to approximately **0.014 mm y⁻¹** for that exposed area *before* blank-cleaning and replicate uncertainty. Scale these quantities with the actual exposed area; a small mounted track showing only part of its face may be worse, while a genuinely exposed **2 cm²** doubles the signal. General Cu–Ni seawater figures support the low-rate problem: Lewis and LaQue report **0.2–0.6 mil y⁻¹** in quiet seawater for 90–10 and **0.3–0.5 mil y⁻¹** for 70–30, equivalent to approximately **0.0051–0.0152** and **0.0076–0.0127 mm y⁻¹**. Lewis and LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, technical report (1981), DOI **10.2172/6255887**. [NAVY: marine-service evidence, not a DED qualification.] (lewis1981evaluationofcoppernickel pages 43-48)

## 4. Images and depths: prioritize damage at the repair interface

[CITE, NUMBERS] Fixed illumination, white balance, magnification and wet/dry state make serial photographs useful for film coverage, color and attacked-area fraction. Cu–Ni's oxide may be brown, greenish brown or brownish black: color is **not** a calibrated penetration rate. On polished cross-sections after the **30-day** exposure, measure maximum and distribution of selective-attack depths independently in deposit, fusion line/heat-affected region and cast NAB or wrought Cu–Ni; include cracks, melt-pool boundaries, porosity and phase-selective paths. A marine-service account reports preferential-phase attack of **cast NAB at crevices and weld-affected regions of order 1 mm y⁻¹**, whereas its cast Cu–Ni comparator averaged **0.02 mm y⁻¹** by one-year mass loss but reached **0.05 mm y⁻¹ maximum** by metallography. These are **casting/service observations, not expected 30-day DED rates**, and should not be linearly imposed as a pass/fail depth. King (1992 thesis; no verified DOI); Malaret (2024), DOI **10.3390/met14040409**. [NAVY] (king1992thehotisostatic pages 43-49, malaret2024semiquantitativecategorizationmethod pages 4-6)

## 5. Galvanic repair test: cheap only if it measures current correctly

[CITE, NUMBERS] Measure each member's separate OCP, then electrically connect a **deposit and cast-NAB pair**, and separately a **deposit and wrought-Cu–Ni pair**, through a proper **ZRA** while both share electrolyte. Record signed current, potential, actual wetted **anodic and cathodic areas**, and current integrated over time; inspect the anodic member and fusion-line cross-section afterward. A voltmeter across a conventional ammeter's burden resistance is **not automatically** a zero-resistance measurement. Cu–30 wt% Ni is generally slightly more noble than Cu–10 wt% Ni, but identical-sign, small OCP differences cannot establish negligible coupling, and aged films or changed area ratios can alter it. Historical flowing-seawater tests found Cu–10 wt% Ni coupled to certain bronzes suffered roughly similar, sometimes slightly *lower*, attack than uncoupled Cu–Ni; those data do **not** demonstrate safety for **C95800 laser-DED repair couples**. Beavers *et al.* (1980), DOI **10.2172/5047866**; Powell (2004; no verified DOI). [GAP] (beavers1980corrosionrelatedfailuresin pages 133-137, powell2004corrosionandbiofouling pages 4-6)

## 6. Inexpensive potentiostats: distinguish electrochemical validation from seawater-corrosion validation

[CITE, NUMBERS, NAVY] **ACEstat**, the *Army Corps of Engineers* open-source design, has a published approximately **$60** small-volume board cost, **50 pA–3 mA** stated current range, and EIS capability. Its CV anodic peak differed by **20 nA (<0.1%)** from commercial **EmStat Pico** for ferrocene methanol; ferri/ferrocyanide EIS fits showed **no statistically significant difference** in charge-transfer or uncompensated resistance between devices. That is encouraging **EIS instrument validation**, **not demonstrated LPR accuracy or resistance to corrosion artifacts on D1141-exposed Cu alloys**. Brown *et al.*, “ACEstat: A DIY Guide to Unlocking the Potential of Integrated Circuit Potentiostats for Open-Source Electrochemical Analysis,” *Analytical Chemistry* **94**, 4906–4912 (2022), DOI **10.1021/acs.analchem.1c04226**. (brown2022acestatadiy pages 2-3, brown2022acestatadiy pages 3-5, brown2022acestatadiy pages 1-2)

[CITE, NUMBERS] **MYSTAT** costs approximately **$226.22** in the published build, spans **±200 mA**, and matched a **Bio-Logic SP-300** ferricyanide CV with **0.18 µA mean current difference** in the reported comparison. It is **DC-only: no published EIS capability** in that design; the article does not benchmark Cu-alloy corrosion LPR. **Rodeostat** is listed at approximately **$250**, **1 µA–1 mA**, with *no EIS* in the compared feature table; **KickStat** is listed for voltammetric methods, not EIS or an established Cu-alloy LPR comparison. Irving, Cecil and Yates, “MYSTAT: A Compact Potentiostat/Galvanostat for General Electrochemistry Measurements,” *HardwareX* **9**, e00163 (2021), DOI **10.1016/j.ohx.2020.e00163**; Brown *et al.* (2022), DOI **10.1021/acs.analchem.1c04226**. (irving2021mystatacompact pages 1-3, irving2021mystatacompact pages 5-8, irving2021mystatacompact pages 11-13, irving2021mystatacompact pages 16-17, brown2022acestatadiy pages 1-2)

[CITE, NUMBERS] **ABE-STAT** has published EIS capability—Jenkins *et al.*, “ABE-STAT, a Fully Open-Source and Versatile Wireless Potentiostat Project Including Electrochemical Impedance Spectroscopy,” *Journal of The Electrochemical Society* **166**, B3056–B3065 (2019), DOI **10.1149/2.0061909jes**—but a Cu–Ni/NAB marine-LPR validation was not found. As an additional, specifically quantified comparison, **TBISTAT** measured **1 Hz–10 kHz** EIS against commercial **Autolab/M204**: reported impedance-magnitude differences were below approximately **2%** for a dummy circuit and **2.5%** for its biosensor, with larger low-frequency discrepancies. Its qualified impedance range was **100 Ω–35 kΩ**; the test was **biosensing, not seawater corrosion**, and that low-frequency limit matters for a protective Cu–Ni film. Burgos-Flórez *et al.*, *PLOS ONE* **17**, e0263738 (2022), DOI **10.1371/journal.pone.0263738**. (burgosflorez2022tbistatanopensource pages 24-25, burgosflorez2022tbistatanopensource pages 13-17, burgosflorez2022tbistatanopensource pages 12-13, burgosflorez2022tbistatanopensource pages 20-21)

[CITE, NUMBERS] **FreiStat** demonstrates an actual steel-in-**0.5 M NaCl** remote Tafel scan (**±200 mV** around OCP, **1 mV s⁻¹**, inferred **~0.6 mm y⁻¹**); its comparison against commercial instruments and EmStat Pico is chiefly voltammetry, **not a same-coupon seawater LPR/EIS corrosion-rate comparison**. Bill *et al.*, “Electrochemical Methods in the Cloud: FreiStat, an IoT-Enabled Embedded Potentiostat,” *Analytical Chemistry* **95**, 13003–13009 (2023), DOI **10.1021/acs.analchem.3c02114**. The commercially packaged **EmStat Pico** is a genuine EIS-capable potentiostat module, not a voltmeter-only workaround; capability still does not validate a particular miniature repair-cell geometry. (bill2023electrochemicalmethodsin pages 3-5, bill2023electrochemicalmethodsin pages 5-6, zheng2026portableelectrochemicalsystems pages 9-10)

**Cost-aware decision.** Run one-hour OCP and fixed photographs on every as-deposited track or wall as inexpensive flags; do **not** assign a corrosion-rate score from either. Carry surviving compositions into replicated multi-day Cu/Ni release measurements and matched deposit–substrate ZRA tests; use a borrowed benchtop instrument to establish **LPR and EIS at one hour and again after film aging** on representative compositions. Only then consider an ACEstat-class EIS node after a **same-cell, same-reference, same-exposed-area comparison** against that benchtop instrument. Retain **30-day D1141 exposure with depth across both repair interfaces**, plus gravimetry wherever cleaning-corrected loss exceeds the measured detection limit, as the decision endpoint. No retrieved study supplies a universal OCP/release/ZRA-to-LPR/EIS correlation or proves that any listed low-cost device reproduces **as-deposited laser DED C71500-equivalent seawater performance**. [GAP] (mantzavinos2001durabilitystudiesrelevant pages 123-128, song2024microstructuresandcorrosion pages 10-13, malaret2024semiquantitativecategorizationmethod pages 4-6, king1992thehotisostatic pages 43-49, brown2022acestatadiy pages 3-5)

References

1. (mantzavinos2001durabilitystudiesrelevant pages 123-128): Dimitris Mantzavinos. Durability studies relevant to marine equipment. Text, Jan 2001. URL: https://doi.org/10.5525/gla.thesis.73974, doi:10.5525/gla.thesis.73974. This article has 1 citations and is from a peer-reviewed journal.

2. (song2024microstructuresandcorrosion pages 10-13): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

3. (malaret2024semiquantitativecategorizationmethod pages 4-6): Francisco Malaret. Semi-quantitative categorization method for the corrosion behavior of metals based on immersion test. Metals, 14:409, Mar 2024. URL: https://doi.org/10.3390/met14040409, doi:10.3390/met14040409. This article has 9 citations.

4. (king1992thehotisostatic pages 43-49): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

5. (powell2004corrosionandbiofouling pages 1-4): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.

6. (song2024microstructuresandcorrosion media d9e0f494): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

7. (song2024microstructuresandcorrosion media 65e1a8b7): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

8. (cottrell2000zebramusseladhesion pages 150-155): C Cottrell. Zebra mussel adhesion and aspects of its prevention using copper. Unknown journal, 2000.

9. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

10. (malaret2024semiquantitativecategorizationmethod pages 2-4): Francisco Malaret. Semi-quantitative categorization method for the corrosion behavior of metals based on immersion test. Metals, 14:409, Mar 2024. URL: https://doi.org/10.3390/met14040409, doi:10.3390/met14040409. This article has 9 citations.

11. (beavers1980corrosionrelatedfailuresin pages 133-137): J. A. Beavers, A. K. Agrawal, and W. E. Berry. Corrosion-related failures in power plant condensers. final report. [pwr]. Unknown journal, Aug 1980. URL: https://doi.org/10.2172/5047866, doi:10.2172/5047866. This article has 6 citations.

12. (song2024microstructuresandcorrosion pages 2-5): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

13. (powell2004corrosionandbiofouling pages 4-6): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.

14. (brown2022acestatadiy pages 2-3): Eric W. Brown, Matthew W. Glasscott, Keith Conley, Jesse Barr, Jason D. Ray, Lee C. Moores, and Anton Netchaev. Acestat: a diy guide to unlocking the potential of integrated circuit potentiostats for open-source electrochemical analysis. Analytical chemistry, 94:4906-4912, Mar 2022. URL: https://doi.org/10.1021/acs.analchem.1c04226, doi:10.1021/acs.analchem.1c04226. This article has 45 citations and is from a highest quality peer-reviewed journal.

15. (brown2022acestatadiy pages 3-5): Eric W. Brown, Matthew W. Glasscott, Keith Conley, Jesse Barr, Jason D. Ray, Lee C. Moores, and Anton Netchaev. Acestat: a diy guide to unlocking the potential of integrated circuit potentiostats for open-source electrochemical analysis. Analytical chemistry, 94:4906-4912, Mar 2022. URL: https://doi.org/10.1021/acs.analchem.1c04226, doi:10.1021/acs.analchem.1c04226. This article has 45 citations and is from a highest quality peer-reviewed journal.

16. (brown2022acestatadiy pages 1-2): Eric W. Brown, Matthew W. Glasscott, Keith Conley, Jesse Barr, Jason D. Ray, Lee C. Moores, and Anton Netchaev. Acestat: a diy guide to unlocking the potential of integrated circuit potentiostats for open-source electrochemical analysis. Analytical chemistry, 94:4906-4912, Mar 2022. URL: https://doi.org/10.1021/acs.analchem.1c04226, doi:10.1021/acs.analchem.1c04226. This article has 45 citations and is from a highest quality peer-reviewed journal.

17. (irving2021mystatacompact pages 1-3): P. Irving, R. Cecil, and M. Z. Yates. Mystat: a compact potentiostat/galvanostat for general electrochemistry measurements. HardwareX, 9:e00163, Apr 2021. URL: https://doi.org/10.1016/j.ohx.2020.e00163, doi:10.1016/j.ohx.2020.e00163. This article has 64 citations and is from a peer-reviewed journal.

18. (irving2021mystatacompact pages 5-8): P. Irving, R. Cecil, and M. Z. Yates. Mystat: a compact potentiostat/galvanostat for general electrochemistry measurements. HardwareX, 9:e00163, Apr 2021. URL: https://doi.org/10.1016/j.ohx.2020.e00163, doi:10.1016/j.ohx.2020.e00163. This article has 64 citations and is from a peer-reviewed journal.

19. (irving2021mystatacompact pages 11-13): P. Irving, R. Cecil, and M. Z. Yates. Mystat: a compact potentiostat/galvanostat for general electrochemistry measurements. HardwareX, 9:e00163, Apr 2021. URL: https://doi.org/10.1016/j.ohx.2020.e00163, doi:10.1016/j.ohx.2020.e00163. This article has 64 citations and is from a peer-reviewed journal.

20. (irving2021mystatacompact pages 16-17): P. Irving, R. Cecil, and M. Z. Yates. Mystat: a compact potentiostat/galvanostat for general electrochemistry measurements. HardwareX, 9:e00163, Apr 2021. URL: https://doi.org/10.1016/j.ohx.2020.e00163, doi:10.1016/j.ohx.2020.e00163. This article has 64 citations and is from a peer-reviewed journal.

21. (burgosflorez2022tbistatanopensource pages 24-25): Francisco Burgos-Flórez, Alexander Rodríguez, Eliana Cervera, Valtencir Zucolotto, Marco Sanjuán, and Pedro J. Villalba. Tbistat: an open-source, wireless portable, electrochemical impedance spectroscopy capable potentiostat for the point-of-care detection of s100b in plasma samples. PLOS ONE, 17:e0263738, Feb 2022. URL: https://doi.org/10.1371/journal.pone.0263738, doi:10.1371/journal.pone.0263738. This article has 37 citations and is from a peer-reviewed journal.

22. (burgosflorez2022tbistatanopensource pages 13-17): Francisco Burgos-Flórez, Alexander Rodríguez, Eliana Cervera, Valtencir Zucolotto, Marco Sanjuán, and Pedro J. Villalba. Tbistat: an open-source, wireless portable, electrochemical impedance spectroscopy capable potentiostat for the point-of-care detection of s100b in plasma samples. PLOS ONE, 17:e0263738, Feb 2022. URL: https://doi.org/10.1371/journal.pone.0263738, doi:10.1371/journal.pone.0263738. This article has 37 citations and is from a peer-reviewed journal.

23. (burgosflorez2022tbistatanopensource pages 12-13): Francisco Burgos-Flórez, Alexander Rodríguez, Eliana Cervera, Valtencir Zucolotto, Marco Sanjuán, and Pedro J. Villalba. Tbistat: an open-source, wireless portable, electrochemical impedance spectroscopy capable potentiostat for the point-of-care detection of s100b in plasma samples. PLOS ONE, 17:e0263738, Feb 2022. URL: https://doi.org/10.1371/journal.pone.0263738, doi:10.1371/journal.pone.0263738. This article has 37 citations and is from a peer-reviewed journal.

24. (burgosflorez2022tbistatanopensource pages 20-21): Francisco Burgos-Flórez, Alexander Rodríguez, Eliana Cervera, Valtencir Zucolotto, Marco Sanjuán, and Pedro J. Villalba. Tbistat: an open-source, wireless portable, electrochemical impedance spectroscopy capable potentiostat for the point-of-care detection of s100b in plasma samples. PLOS ONE, 17:e0263738, Feb 2022. URL: https://doi.org/10.1371/journal.pone.0263738, doi:10.1371/journal.pone.0263738. This article has 37 citations and is from a peer-reviewed journal.

25. (bill2023electrochemicalmethodsin pages 3-5): David Bill, Mark Jasper, Andreas Weltin, Gerald A. Urban, Stefan J. Rupitsch, and Jochen Kieninger. Electrochemical methods in the cloud: freistat, an iot-enabled embedded potentiostat. Analytical Chemistry, 95:13003-13009, Aug 2023. URL: https://doi.org/10.1021/acs.analchem.3c02114, doi:10.1021/acs.analchem.3c02114. This article has 33 citations and is from a highest quality peer-reviewed journal.

26. (bill2023electrochemicalmethodsin pages 5-6): David Bill, Mark Jasper, Andreas Weltin, Gerald A. Urban, Stefan J. Rupitsch, and Jochen Kieninger. Electrochemical methods in the cloud: freistat, an iot-enabled embedded potentiostat. Analytical Chemistry, 95:13003-13009, Aug 2023. URL: https://doi.org/10.1021/acs.analchem.3c02114, doi:10.1021/acs.analchem.3c02114. This article has 33 citations and is from a highest quality peer-reviewed journal.

27. (zheng2026portableelectrochemicalsystems pages 9-10): Yu-Jie Zheng, Jin Chen, Liang-Zun Fu, and Xi-Wei Huang. Portable electrochemical systems for on-site detection of heavy metal ions: principles, hardware architectures, and field applications. Smart Materials and Devices, Jan 2026. URL: https://doi.org/10.70401/smd.2026.0035, doi:10.70401/smd.2026.0035. This article has 1 citations.
