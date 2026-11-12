<!--
Edison Scientific LITERATURE task (batch 3)
- Task ID: 1c764462-13f2-4a2b-8501-9fc55b4650f2
- Submitted: 2026-10-17T05:46:10Z
- Fetched: 2026-10-17T06:17:02Z (status: success)
- Raw trajectory JSON: ../raw/b3-10-porosity-oxygen-cu-deposits.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What causes gas porosity in laser-deposited and welded Cu-Ni and
aluminum bronzes, and what powder oxygen and moisture limits follow? Cover
the steam reaction (Cu2O + 2H -> 2Cu + H2O), hydrogen and nitrogen pickup,
oxide films on Al-bronze powders, why ERCuNi filler metals contain Ti and Mn
(deoxidizers) and what happens without them, the porosity reported for
laser-deposited Cu-30Ni and blended Cu-Ni powders, shielding gas choices,
and any quantitative relationship between powder oxygen (ppm) and deposit
porosity for copper alloys in DED or LPBF. Should a DED powder for Cu-Ni
contain a deoxidizer such as Ti, and how much?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What causes gas porosity in laser-deposited and welded Cu-Ni and
aluminum bronzes, and what powder oxygen and moisture limits follow? Cover
the steam reaction (Cu2O + 2H -> 2Cu + H2O), hydrogen and nitrogen pickup,
oxide films on Al-bronze powders, why ERCuNi filler metals contain Ti and Mn
(deoxidizers) and what happens without them, the porosity reported for
laser-deposited Cu-30Ni and blended Cu-Ni powders, shielding gas choices,
and any quantitative relationship between powder oxygen (ppm) and deposit
porosity for copper alloys in DED or LPBF. Should a DED powder for Cu-Ni
contain a deoxidizer such as Ti, and how much?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.


# Gas porosity and feedstock controls for copper-alloy laser DED

**Bottom line.** Moisture, oxygen-bearing feedstock, atmospheric nitrogen, and inadequate fusion are distinct risks; a polished-section pore cannot be assigned to any one of them without additional evidence. The retrieved literature does **not** establish a transferable maximum powder-oxygen concentration, powder-moisture concentration, or titanium dosage that guarantees dense Cu–Ni or nickel–aluminum-bronze (NAB) blown-powder DED deposits. The most useful quantitative controls are therefore *experimental starting points*, not literature-validated acceptance limits. (littleton1974nitrogenporosityin pages 1-2, littleton1974nitrogenporosityin pages 3-4, jadhav2020modificationofelectrical pages 3-5, nemani2024advancementsinadditive pages 105-106)

## Mechanisms and directly relevant studies

**1. Steam reaction and atmospheric pickup. [CITE] [NUMBERS] [GAP]** Littleton, J.; Lammas, J.; Jordan, M. F. “Nitrogen Porosity in Gas Shielded Arc Welding of Copper.” *Welding Research Supplement* (December 1974), pp. 561-s–565-s as visible in the retrieved article. **DOI: not identified.** **Process/material:** gas-tungsten-arc and gas-metal-arc welding of oxygen-free high-conductivity (OFHC), electrolytic tough-pitch, and deoxidized high-phosphorus copper—not Cu–Ni DED. Dissolved hydrogen can reduce cuprous oxide according to **Cu₂O + 2H → 2Cu + H₂O**; water vapor formed or introduced into the molten pool can leave steam pores on solidification. The authors compared dry argon with argon containing **0.005 g H₂O/dm³** and found the added water significantly decreased weld-metal density. They also cite approximately **150 volume-ppm water vapor** as sufficient to produce comparable porosity in an earlier tough-pitch-copper weld experiment. These are *shielding-atmosphere observations*, **not powder-moisture limits** and not a demonstrated threshold for Cu–Ni. Their comparison of oxide-bearing tough-pitch and deoxidized copper supports treating oxide inventory and hydrogen exposure together. No saline-corrosion test, powder oxygen, deposit hardness, or DED density was reported for this comparison. (littleton1974nitrogenporosityin pages 1-2, littleton1974nitrogenporosityin pages 2-3)

**2. Nitrogen is a separate pore-forming mechanism—even with little oxygen. [CITE] [NUMBERS]** In the same Littleton–Lammas–Jordan study, autogenous GTAW on **3-mm OFHC Cu** at **250–315 A, 11 V, 2 or 6 mm/s**, with **15 L/min Ar/N₂**, developed appreciable porosity with only **0.1 vol% N₂** added to argon; porosity increased until approximately **0.6% N₂**, and faster travel reduced it. Gas released from pores made with **0.4% N₂/Ar** contained **91% and 94% nitrogen** in two analyses. Thus these pores resulted from nitrogen uptake and rejection during freezing, not merely trapped shielding gas; butt-joint geometry also promoted atmospheric entrainment. This quantitative threshold is for a copper *arc weld*, **not** an allowable nitrogen percentage in a laser-DED shielding stream. No seawater tests were performed. (littleton1974nitrogenporosityin pages 3-4, littleton1974nitrogenporosityin pages 2-3, littleton1974nitrogenporosityin pages 4-5)

**3. Deoxidation does not automatically prevent nitrogen porosity. [CITE] [NUMBERS]** Littleton and colleagues tested copper-welding filler **C7, 0.18 wt% Si–0.23 wt% Mn**, against **C8, 0.20 wt% Al–0.10 wt% Ti**, on OFHC Cu. Under GTAW with **0–1 vol% N₂ added to Ar**, the Si/Mn-bearing, substantially *deoxidizing* filler reduced but did not eliminate pores; the Al/Ti-bearing filler eliminated them over that range. This is direct evidence for **denitriding in addition to deoxidizing**. It does **not** demonstrate that 0.10 wt% Ti in a pre-alloyed Cu–Ni DED powder will reproduce that result, nor does it isolate Ti from Al. Nickel-containing ERCuNi and nickel–aluminum-bronze ERCuNiAl are different fillers: do not transfer the C7/C8 compositions to either designation. The retrieved sources did not provide a verifiable ERCuNi specification establishing its Ti and Mn ranges or a controlled ERCuNi-without-Ti/Mn comparison; the commonly stated rationale is oxygen scavenging by Ti and Mn, with Ti also potentially binding nitrogen, whereas omission leaves less protection against gas porosity. **That ERCuNi-specific omission claim remains a welding-metallurgy inference, not a measured finding from these sources.** (littleton1974nitrogenporosityin pages 3-4, littleton1974nitrogenporosityin pages 4-5, huo2025modulatingheatinput pages 4-5)

**4. Direct Cu–Ni evidence that gas is not the only explanation. [CITE] [NUMBERS] [NOVELTY-RISK]** Koeini, F.; Sohi, M. H.; Pirayesh, P. “Surface Alloying of Cupronickel Alloy with Aluminum using Tungsten Inert Gas Process.” *Archives of Metallurgy and Materials* **68** (2023), 161–170. **DOI: 10.24425/amm.2023.141490.** **Process:** argon-shielded GTA surface melting/alloying, **not laser DED**. **Substrate, wt%:** Cu 87.71, Ni 10.60, Fe 0.93, Zn 0.60, Pb 0.06, Sn 0.05, Mn 0.04, Co 0.01; aluminum-alloying feedstock was preplaced **>99.9% Al, <45 µm**, not a single pre-alloyed stream. At fixed **150 A, 70 mm/min**, increasing Ar flow from **8 to 16 L/min** substantially reduced visible pore number and size but changed melt depth from **3,082 to 1,622 µm**; changing heat input alone had little reported effect on pores. Al surface alloying removed the visible pores in the illustrated condition. Starting-substrate hardness was **140 HV0.1**, surface-melted hardness **70 HV0.1**, and Al-alloyed hardness **300 HV0.1**. Polarization used **3.5% NaCl at room temperature**, SCE reference and **2 mV/s**; no immersion duration, flow-controlled seawater exposure, powder oxygen, numerical pore fraction, or verified 70–30 Cu–Ni corrosion benchmark is supplied by these excerpts. The authors associate Cu–Ni melt porosity with oxygen/hydrogen absorption; their Al-alloying result cannot by itself distinguish chemical scavenging from altered melt behavior. More shielding flow is **not universally better**, because it also changes heat transfer and can disturb the pool. (koeini2023surfacealloyingof pages 1-2, koeini2023surfacealloyingof pages 2-4)

**5. Blended-elemental Cu–Ni powder already shows pores and unmelted Ni. [CITE] [NUMBERS] [NOVELTY-RISK]** Williams, N.; Snyder, K.; Smith, I.; Duong, A.; Carpenter, E.; Barua, R. “The First Layer: Single-Track Insights into Direct Energy Deposition Processed Cu-Ni Thermoelectric Alloys.” *Journal of Manufacturing and Materials Processing* **9** (2025), 170. **DOI: 10.3390/jmmp9060170.** **Process:** blown-powder laser DED, **single tracks** on 316L stainless steel; separate elemental copper and nickel powders were tumbler-blended for 8 h and fed together. The article calls the resulting feed **65 wt% Cu–35 wt% Ni**, although its mixing-method description says *65:35 atomic ratio*: that internal inconsistency warrants checking before treating the designation as a measured composition. At **800 W**, linear mass input was **0.011–0.026 g/mm** and heat input approximately **63–137 J/mm**; Ar was carrier and shield. Powder diameter averaged **57 ± 15 µm**; apparent/bulk and tapped densities were **4.74 and 5.20 g/cm³** (Hausner ratio **1.10**) and reported Hall throughput was **0.3 g/s**. Lower-input tracks showed large voids and approximately **50-µm unmelted Ni inclusions**; the proposed connection between pores and Cu/Ni melting-point disparity is explicitly a **hypothesis**, not proof of a gas mechanism. Some higher-feed tracks appeared free of porosity but showed inadequate substrate penetration; low-feed/high-dilution tracks cracked. **No numerical bulk porosity fraction, powder O/H₂O, strength, or marine corrosion result** is established. The proposed *compositionally pre-alloyed* single-powder feed is a meaningful distinction, but Cu–Ni laser deposition alone is **not novel**. (williams2025thefirstlayer pages 6-9, williams2025thefirstlayer pages 4-6, williams2025thefirstlayer pages 2-4)

**6. Previously reported Cu–30Ni and blended Cu–Ni laser deposition must be acknowledged without inventing measurements. [CITE] [NOVELTY-RISK] [GAP]** Bhattacharya, S.; Dinda, G. P.; Dasgupta, A. K.; Natu, H.; Dutta, B.; Mazumder, J. “Microstructural evolution and mechanical, and corrosion property evaluation of Cu–30Ni alloy formed by direct metal deposition process.” *Journal of Alloys and Compounds* **509** (2011), 6364–6373. **DOI: 10.1016/j.jallcom.2011.03.091.** **Process:** direct-metal-deposition laser processing of nominal **Cu–30 wt% Ni** on rolled **C71500**; a retrieved secondary account notes lower, approximately constant clad hardness versus the substrate. The **primary article was not retrievable here**: its pore fraction, feedstock oxygen/size, exact electrolyte, exposure duration, corrosion current/rate, potential, and strength **cannot responsibly be quoted**. Karnati, S.; Liou, F. F.; Newkirk, J. W. “Characterization of copper–nickel alloys fabricated using laser metal deposition and blended powder feedstocks.” *International Journal of Advanced Manufacturing Technology* **103** (2019), 239–250. **DOI: 10.1007/s00170-019-03553-0.** **Process:** blended-powder laser metal deposition, not verified here as one *pre-alloyed* powder; the primary text likewise could not be retrieved, so no numerical porosity, powder oxygen, mechanical, or corrosion values are asserted. These are **priority prior-art checks**, not evidence that a particular DED oxygen limit works. The retrieved review identifies porous Cu–Ni laser-deposited structures and identifies Cu–30Ni and blended Cu–Ni as existing research, but cannot replace the original experimental tables. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 110-112, nemani2024advancementsinadditive pages 106-108, s2022reviewonsurface pages 11-12)

**7. Aluminum bronze: oxide films are a powder-specific concern. [CITE] [GAP] [NOVELTY-RISK]** Nemani, A. V.; Ghaffari, M.; Bokati, K. S.; Valizade, N.; Afshari, E.; Nasiri, A. “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review.” *Journal of Manufacturing and Materials Processing* **8** (2024), 54. **DOI: 10.3390/jmmp8020054.** **Scope:** review of blown-powder laser DED, LPBF, and WAAM rather than a controlled powder-oxygen experiment. Al-bearing bronze particles should be expected to acquire a persistent **Al₂O₃-rich surface film**: an oxide-bearing surface is not equivalent to dissolved oxygen, and films can remain as inclusions or interfere with wetting and interlayer bonding; oxide and adsorbed moisture can also accompany hydrogen-bearing gas exposure. Accordingly, record oxygen **and** investigate oxide location/morphology, rather than assuming a single bulk-O assay quantifies film risk. The review reports existing **Cu–9Al–5Fe–5Ni wt% laser-metal-deposited NAB**, with approximately **593–713 MPa yield strength, 769–949 MPa ultimate strength, and 10–12% elongation**; these are secondary-source values, **not** demonstrations of oxide-free powder or as-deposited 30-day seawater performance. It also identifies laser DED **CuNi2SiCr repair layers on cast NAB** as porous and mechanically unsuitable for propeller repair. The specific alloy/substrate/oxide and seawater combination remains a gap, not the whole notion of NAB DED repair. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 105-106)

**8. Relevant as-deposited NAB corrosion benchmark—but a different feed and a short test. [CITE] [NUMBERS] [NAVY] [GAP]** Huo, R.; Wang, Z.; Wang, M.; Wang, R.; Zhang, S.; Zhang, C.; Wu, C.; Chen, H.; Chen, J. “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing.” *Materials* **18** (2025), 2205. **DOI: 10.3390/ma18102205.** **Process:** wire-arc DED/CMT WAAM of **ERCuNiAl**, *not* ERCuNi or powder, on an Al-bronze substrate; marine engineering is the stated application, but **Navy/DoD funding is not verified**. **Wire wt%:** Cu balance, Al **8.73**, Fe **5.90**, Ni **4.52**, Mn **1.39**. Ar shielding was **15 L/min**. At **243.8, 378.8, 502.8, 644.7 J/mm**, respectively, as-deposited hardness was **192.4 ± 6.9, 182.3 ± 2.8, 178.9 ± 2.9, 166.9 ± 0.3 HV**; polarization-derived *i*₍corr₎ was **2.56 ± 0.04, 3.85 ± 0.11, 5.03 ± 0.08, 7.52 ± 0.07 µA/cm²** and tabled potentials were **−269.61 ± 40, −466.62 ± 10, −517.77 ± 20, −700.94 ± 15 mV**. Film resistance fell from **1,152 to 185.8 Ω·cm²** and charge-transfer resistance from **2,485 to 707 Ω·cm²** between first and last settings. Tests used *aerated 3.5 wt% NaCl* in deionized water, **25 ± 5 °C**, **1 cm²**, SCE, **3,600-s OCP** before EIS (**0.01–100,000 Hz; 3-mV AC**) and **0.5 mV/s** polarization; **no 30-day immersion, ASTM D1141 seawater, flow exposure, selective-attack depth, powder oxygen, or C71500 control** was reported. Figure-derived 1-h OCP values differ from the tabled polarization potentials: do **not** interchange them. This is a Navy-*application*-relevant comparison, not documented Navy sponsorship or proof of meeting the proposed seawater criterion. (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 13-15)

**9. Powder oxygen in a copper-alloy LPBF experiment is not a porosity acceptance curve. [CITE] [NUMBERS] [GAP]** Jadhav, S. D.; Dadbakhsh, S.; Chen, R.; Shabadi, R.; Kruth, J.-P.; Van Humbeeck, J.; Vanmeensel, K. “Modification of Electrical and Mechanical Properties of Selective Laser-Melted CuCr0.3 Alloy Using Carbon Nanoparticles.” *Advanced Engineering Materials* **22** (2020). **DOI: 10.1002/adem.201900946.** **Process:** LPBF of pre-alloyed **Cu–0.26 wt% Cr** (measured) powder, **D50 = 33.7 µm**, with or without **0.05 wt% admixed carbon**; not Cu–Ni/NAB or single-stream pre-alloyed Cu–Ni. Virgin powder contained **0.14 wt% O = 1,400 ppm by mass**. Hall times were **13.6 versus 16.1 s**, apparent packing densities **51% versus 47%**. Optimized Ar-shielded builds at **600 W** attained dense specimens at **400 mm/s** without carbon and **300 mm/s** with carbon; across process settings **>98.5% relative density** was obtained at low speeds, but one virgin-powder pair yielded **98.6% versus 92.3%** density despite comparable reported energy input because scan speeds differed. Surface chromium oxides and carbon-assisted deoxidation were observed; anticipated CO/CO₂ **did not produce identifiable gas porosity**. Therefore **1,400 ppm oxygen is neither a demonstrated universal failure threshold nor a recommended Cu–Ni/NAB powder limit**. These authors did not determine a controlled powder-O(ppm)-to-pore-volume function. No seawater, repair substrate, or immersion data were reported. (jadhav2020modificationofelectrical pages 3-5, jadhav2020modificationofelectrical pages 7-11)

**10. Do not confuse shielding-atmosphere oxygen with oxygen in powder. [CITE] [NUMBERS] [GAP]** Stoll, T.; Trautnitz, P.; Schmiedeke, S.; Franke, J. E.; Travitzky, N. “Process development for laser powder bed fusion of pure copper.” *Laser 3D Manufacturing VII*, SPIE **11271** (2020), 112710I. **DOI: 10.1117/12.2563870.** Its abstract describes **>99.90%-pure Cu-ETP**, near-infrared LPBF at up to **500 W**, with a maximum **99.82% relative density**. Those values do **not** describe Cu–Ni DED. Separately retrieved copper-LPBF thesis text reports nitrogen-shielded chamber oxygen of approximately **0.13% = 1,300 ppm *gas-phase O₂***, alongside powder measured separately by inert-gas fusion; recycled and intentionally oxidized powder had roughly **2.5-fold and 5-fold** the virgin powder's oxygen, respectively, and recycled builds had approximately **1 ± 0.2 percentage points** lower relative density. **Caution:** the thesis passage and Stoll paper were incorrectly conflated in a retrieval result; these chamber-oxygen and recycling figures must **not** be attributed to Stoll, and the thesis's absolute powder-O ppm could not be verified in the available text. They do not establish an alloy-independent oxygen–porosity slope. (stoll2020processdevelopmentfor pages 85-90, stoll2020processdevelopmentfor pages 81-85, stoll2020processdevelopmentfor pages 95-100)

## Implications for the powder specification and Ti experiment

**Oxygen and moisture limits.** No defensible literature-derived numerical *powder* O maximum, powder H₂O maximum, or universal dry-gas dew point follows from the cited experiments. For a first-pass **internal screening target rather than a claimed threshold**, testing lots at **≤100–200 ppm O by mass**, then deliberately oxygen-enriched lots spanning several hundred ppm and approximately **1,000–1,500 ppm**, would allow the proposal to *measure* an alloy- and particle-size-specific acceptance region; the lower target is a conservative proposed design choice, **not a proven copper-alloy DED requirement**. Treat NAB separately from Cu–Ni because oxide chemistry differs. Measure inert-gas-fusion O before/after atomization, after storage and immediately before DED; measure moisture or hydrogen *independently*, record carrier/shield dew point and atmospheric ingress, and classify pores by micro-CT/metallography and, where possible, pore-gas/oxide analysis. The controlled experiment should hold energy input, particle-size range and shielding fixed while varying O and independently varying moisture. The sources do not validate a numerical dew-point or gravimetric moisture cutoff for these deposits. (littleton1974nitrogenporosityin pages 1-2, littleton1974nitrogenporosityin pages 3-4, jadhav2020modificationofelectrical pages 3-5, nemani2024advancementsinadditive pages 105-106)

**Shielding.** Start with verified-dry high-purity **Ar** for both carrier and shield; prevent room-air entrainment with nozzle design, overlap shielding where needed, and document delivered-gas moisture/O₂ rather than cylinder certification alone. Ar was used in the cited Cu–Ni laser tracks, Cu–Ni GTA study, CuCr LPBF, and NAB CMT study. Avoid using **N₂ as an unqualified default**, especially in trials without denitriding additions: copper arc-weld porosity appears at very low added N₂, though an LPBF review notes some other Cu-alloy experiments run under nitrogen, so transfer to the specific DED alloys must be tested. Helium or Ar–He can be explored to change heat input/penetration, but the retrieved material does not establish that either intrinsically prevents Cu–Ni/NAB gas pores. More Ar flow can reduce atmosphere pickup yet alter pool penetration. (littleton1974nitrogenporosityin pages 3-4, williams2025thefirstlayer pages 2-4, huo2025modulatingheatinput pages 4-5, koeini2023surfacealloyingof pages 2-4, nemani2024advancementsinadditive pages 26-28)

**Should Cu–Ni contain Ti?** **Yes, as a controlled *candidate*, not as a prescribed production addition.** Compare Ti-free pre-alloyed controls against, for example, **0.05, 0.10 and 0.20 wt% nominal Ti** in the *atomized alloy*, measuring **retained dissolved Ti**, oxide/nitride inclusion populations, deposit pore volume and as-deposited seawater behavior. **0.10 wt% is an experimental center point inferred from the Al/Ti copper-welding filler, not a proven Cu–Ni DED optimum**; the experiment also needs Mn-controlled arms to separate Mn deoxidation from Ti denitriding and check whether Ti-bearing particles worsen corrosion or flow. The available sources do not establish an ERCuNi-specific numerical Ti specification, a Ti-free/Ti-bearing pre-alloyed Cu–Ni DED comparison, or a dose–response for this proposal's corrosion target. (littleton1974nitrogenporosityin pages 3-4, jadhav2020modificationofelectrical pages 3-5, littleton1974nitrogenporosityin pages 4-5)

## Ranked top 5 things the PI should know

1. **Never promise a literature-certified ppm powder-oxygen limit or Ti dose.** The CuCr LPBF experiment combined **1,400 ppm powder O** with **>98.5% density** under some settings; gas-phase ppm, powder-mass ppm and powder moisture are different variables. Establish limits experimentally for each alloy family. (jadhav2020modificationofelectrical pages 3-5, jadhav2020modificationofelectrical pages 7-11)
2. **Design for both steam and nitrogen, not just oxidation.** Copper GTA welds developed pores with **0.1% N₂/Ar**; Si/Mn deoxidizers did not eliminate these nitrogen pores, whereas **0.20% Al–0.10% Ti filler** did under tested conditions. (littleton1974nitrogenporosityin pages 1-2, littleton1974nitrogenporosityin pages 3-4, littleton1974nitrogenporosityin media 90f3b4ae)
3. **Separate gas pores from incomplete melting and fusion.** Elementally blended Cu–Ni DED exhibited approximately **50-µm Ni inclusions**, hypothesized pores, cracking at high dilution, and inadequate interface penetration at other settings; pre-alloying plausibly addresses mixing but does not itself prove gas-free or repair-ready builds. (williams2025thefirstlayer pages 6-9, williams2025thefirstlayer pages 2-4)
4. **Existing Cu–30Ni laser deposition and NAB DED/repair are real prior art.** Frame novelty as *pre-alloyed composition–powder–DED–as-deposited seawater optimization on specified copper-alloy repair substrates*, rather than claiming first Cu–Ni or NAB deposition. Retrieve the original Bhattacharya and Karnati papers before quoting their porosity or corrosion numbers. (nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 110-112, s2022reviewonsurface pages 11-12)
5. **A brief 3.5% NaCl electrochemical screen cannot establish the seawater deliverable.** The as-deposited NAB WAAM benchmark spans **2.56–7.52 µA/cm²** as heat input rises, but provides no ASTM D1141/natural-seawater **30-day** exposure, flow or selective-attack depth, and no simultaneously tested wrought C71500 control. (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 10-13)

References

1. (littleton1974nitrogenporosityin pages 1-2): J Littleton and J Lammas. Nitrogen porosity in gas shielded arc welding of copper. Unknown journal, 1974.

2. (littleton1974nitrogenporosityin pages 3-4): J Littleton and J Lammas. Nitrogen porosity in gas shielded arc welding of copper. Unknown journal, 1974.

3. (jadhav2020modificationofelectrical pages 3-5): Suraj Dinkar Jadhav, Sasan Dadbakhsh, Rong Chen, Rajashekhara Shabadi, Jean-Pierre Kruth, Jan Van Humbeeck, and Kim Vanmeensel. Modification of electrical and mechanical properties of selective laser‐melted cucr0.3 alloy using carbon nanoparticles. Advanced Engineering Materials, Nov 2020. URL: https://doi.org/10.1002/adem.201900946, doi:10.1002/adem.201900946. This article has 52 citations and is from a peer-reviewed journal.

4. (nemani2024advancementsinadditive pages 105-106): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

5. (littleton1974nitrogenporosityin pages 2-3): J Littleton and J Lammas. Nitrogen porosity in gas shielded arc welding of copper. Unknown journal, 1974.

6. (littleton1974nitrogenporosityin pages 4-5): J Littleton and J Lammas. Nitrogen porosity in gas shielded arc welding of copper. Unknown journal, 1974.

7. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

8. (koeini2023surfacealloyingof pages 1-2): Fatemeh Koeini, Mahmoud Heydarzadeh Sohi, and Parham Pirayesh. Surface alloying of cupronickel alloy with aluminum using tungsten inert gas process. Archives of Metallurgy and Materials, pages 161-170, Jul 2023. URL: https://doi.org/10.24425/amm.2023.141490, doi:10.24425/amm.2023.141490. This article has 1 citations and is from a peer-reviewed journal.

9. (koeini2023surfacealloyingof pages 2-4): Fatemeh Koeini, Mahmoud Heydarzadeh Sohi, and Parham Pirayesh. Surface alloying of cupronickel alloy with aluminum using tungsten inert gas process. Archives of Metallurgy and Materials, pages 161-170, Jul 2023. URL: https://doi.org/10.24425/amm.2023.141490, doi:10.24425/amm.2023.141490. This article has 1 citations and is from a peer-reviewed journal.

10. (williams2025thefirstlayer pages 6-9): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

11. (williams2025thefirstlayer pages 4-6): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

12. (williams2025thefirstlayer pages 2-4): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

13. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

14. (nemani2024advancementsinadditive pages 110-112): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

15. (nemani2024advancementsinadditive pages 106-108): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

16. (s2022reviewonsurface pages 11-12): Pratheesh Kumar S, Anand K, Hari Chealvan S, and Karthikeya Muthu S. Review on surface characteristics of components produced by direct metal deposition process. Journal of Mechanical Engineering and Sciences, pages 9197-9229, Dec 2022. URL: https://doi.org/10.15282/jmes.16.4.2022.05.0729, doi:10.15282/jmes.16.4.2022.05.0729. This article has 7 citations.

17. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

18. (huo2025modulatingheatinput pages 13-15): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

19. (jadhav2020modificationofelectrical pages 7-11): Suraj Dinkar Jadhav, Sasan Dadbakhsh, Rong Chen, Rajashekhara Shabadi, Jean-Pierre Kruth, Jan Van Humbeeck, and Kim Vanmeensel. Modification of electrical and mechanical properties of selective laser‐melted cucr0.3 alloy using carbon nanoparticles. Advanced Engineering Materials, Nov 2020. URL: https://doi.org/10.1002/adem.201900946, doi:10.1002/adem.201900946. This article has 52 citations and is from a peer-reviewed journal.

20. (stoll2020processdevelopmentfor pages 85-90): Thomas Stoll, Pascal Trautnitz, Samuel Schmiedeke, Joerg Ernst Franke, and Nahum Travitzky. Process development for laser powder bed fusion of pure copper. Laser 3D Manufacturing VII, 11271:112710I-112710I-15, Mar 2020. URL: https://doi.org/10.1117/12.2563870, doi:10.1117/12.2563870. This article has 32 citations.

21. (stoll2020processdevelopmentfor pages 81-85): Thomas Stoll, Pascal Trautnitz, Samuel Schmiedeke, Joerg Ernst Franke, and Nahum Travitzky. Process development for laser powder bed fusion of pure copper. Laser 3D Manufacturing VII, 11271:112710I-112710I-15, Mar 2020. URL: https://doi.org/10.1117/12.2563870, doi:10.1117/12.2563870. This article has 32 citations.

22. (stoll2020processdevelopmentfor pages 95-100): Thomas Stoll, Pascal Trautnitz, Samuel Schmiedeke, Joerg Ernst Franke, and Nahum Travitzky. Process development for laser powder bed fusion of pure copper. Laser 3D Manufacturing VII, 11271:112710I-112710I-15, Mar 2020. URL: https://doi.org/10.1117/12.2563870, doi:10.1117/12.2563870. This article has 32 citations.

23. (nemani2024advancementsinadditive pages 26-28): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

24. (littleton1974nitrogenporosityin media 90f3b4ae): J Littleton and J Lammas. Nitrogen porosity in gas shielded arc welding of copper. Unknown journal, 1974.
