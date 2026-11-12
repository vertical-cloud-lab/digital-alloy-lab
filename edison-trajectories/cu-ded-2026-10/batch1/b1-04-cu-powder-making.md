<!--
Edison Scientific LITERATURE_HIGH task (batch 1)
- Task ID: e0a95fe6-6d76-432d-85e8-b2ce48e5ac3e
- Submitted: 2026-10-17T05:10:43Z
- Fetched: 2026-10-17T05:44:54Z (status: success)
- Raw trajectory JSON: ../raw/b1-04-cu-powder-making.json.gz
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

QUESTION: How are copper alloy powders for additive manufacturing made, and
what goes wrong? Cover gas atomization (close-coupled, free-fall), water
atomization, electrode induction gas atomization, plasma atomization, plasma
rotating electrode process, centrifugal atomization, plasma spheroidization,
and ultrasonic (vibrating-plate or sonotrode) atomization, for pure Cu,
Cu-Ni, aluminum bronzes / NAB, Cu-Sn, CuCrZr and GRCop. Report particle size
distributions, yield in a target size cut, sphericity and satellites, oxygen
pickup and how it is controlled, crucible and nozzle materials compatible
with copper and copper-nickel melts (graphite, alumina, zirconia, boron
nitride, magnesia), and melt superheat. Specifically: has ultrasonic
atomization been used for copper or copper alloys (any AMAZEMET rePOWDER
reports), at what frequency, and what median particle size resulted? How do
in-house or small-batch atomized copper alloy powders compare with
commercial gas-atomized powder in flow, density, and printed quality?

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

QUESTION: How are copper alloy powders for additive manufacturing made, and
what goes wrong? Cover gas atomization (close-coupled, free-fall), water
atomization, electrode induction gas atomization, plasma atomization, plasma
rotating electrode process, centrifugal atomization, plasma spheroidization,
and ultrasonic (vibrating-plate or sonotrode) atomization, for pure Cu,
Cu-Ni, aluminum bronzes / NAB, Cu-Sn, CuCrZr and GRCop. Report particle size
distributions, yield in a target size cut, sphericity and satellites, oxygen
pickup and how it is controlled, crucible and nozzle materials compatible
with copper and copper-nickel melts (graphite, alumina, zirconia, boron
nitride, magnesia), and melt superheat. Specifically: has ultrasonic
atomization been used for copper or copper alloys (any AMAZEMET rePOWDER
reports), at what frequency, and what median particle size resulted? How do
in-house or small-batch atomized copper alloy powders compare with
commercial gas-atomized powder in flow, density, and printed quality?

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


## How Copper Alloy Powders for Additive Manufacturing Are Made, and What Goes Wrong

### 1. Overview of Atomization Methods

The following table summarizes the principal atomization and post-processing routes for producing copper alloy AM powders, drawing on both copper-specific data and general metal-powder benchmarks where copper data are absent.

| Method | Typical PSD | Yield in AM cut | Sphericity | Oxygen | Satellites | Crucible / nozzle | Key advantages | Key limitations |
|---|---:|---:|---:|---:|---|---|---|---|
| Close-coupled VIGA / inert-gas atomization | General: 0–180 µm. NiCu Alloy 400 after classification: D10/D50/D90 = 28.9/42.3/61.5 µm; NAB for DED: 49.76/76.29/116.46 µm. Pure Cu examples: 12.1/20.8/33.2 and 17.0/26.3/40.1 µm (li2021nanotwinscontainingmicrostructureand pages 1-4, roth2024establishingaprocess pages 5-7, sinico2019influenceofpowder pages 2-4, zhang2025researchprogresson pages 10-11) | Useful 10–105 µm yield is generally about 45–85%; one VIGA benchmark gave 70% below 53 µm. Alloy 400 was screened to 15–63 µm, but cut yield was not reported (roth2024establishingaprocess pages 2-4, mathias2024metalpowderas pages 10-12, zhang2025researchprogresson pages 10-11) | Predominantly spherical; general VIGA benchmark 85–90%. Alloy 400 volumetric sphericity 0.766, symmetry 0.916, aspect ratio 0.821 (roth2024establishingaprocess pages 5-7, zhang2025researchprogresson pages 10-11) | General benchmark 200–1400 ppm. Vacuum and high-purity Ar limit pickup; the Alloy 400 source mentioned only a few ppm but did not report a measured lot value (roth2024establishingaprocess pages 1-2, zhang2025researchprogresson pages 10-11) | Common; Alloy 400 contained occasional satellites and coarse agglomerates. Satellites reduce sphericity, packing, and flow (roth2024establishingaprocess pages 5-7, mathias2024metalpowderas pages 4-5) | Alloy 400 used an unspecified ceramic crucible with graphite susceptor. Close coupling risks melt buildup or freezing at the delivery tube. No retrieved Cu-specific study compared graphite, alumina, zirconia, BN, and magnesia nozzles (roth2024establishingaprocess pages 2-4, zhang2026gasatomizationfor pages 14-15) | Industrial throughput and fine, pre-alloyed powder. Alloy 400 achieved Hall flow 15.22 s/50 g, apparent density 4.38 g/cm³, Hausner ratio 1.09, and no detected internal gas pores (roth2024establishingaprocess pages 7-9, roth2024establishingaprocess pages 5-7) | Broad raw PSD causes screening loss; hollow particles, trapped gas, satellites, oxidation, ceramic erosion, and nozzle blockage are principal failure modes. Excess superheat can trap gas; insufficient superheat coarsens powder or freezes the nozzle (zhang2026gasatomizationfor pages 15-17, zhang2026gasatomizationfor pages 14-15, mathias2024metalpowderas pages 10-12) |
| Free-fall gas atomization | Generally coarser and broader than close-coupled atomization; no defensible Cu-alloy PSD was found (zhang2026gasatomizationfor pages 14-15) | Not reported for the requested Cu alloys | Droplets become spherical given sufficient flight time, but incomplete breakup or spheroidization leaves coarse and irregular material | Controlled through vacuum/inert gas and gas purity; no Cu-specific value found | Can form through droplet collision or adhesion of fines | Melt stream falls before gas impact; this reduces close-coupled backpressure but still requires refractory melt delivery | Simpler flow field and less close-coupled melt buildup | Lower breakup efficiency and coarser powder than close-coupled designs; little evidence for AM-grade Cu-alloy yield (zhang2026gasatomizationfor pages 14-15) |
| EIGA | General benchmark 0–180 µm; TiAl example mainly 15–105 µm (zhang2025researchprogresson pages 4-6, zhang2025researchprogresson pages 10-11) | General benchmark: 30–45% below 53 µm (zhang2025researchprogresson pages 10-11) | About 90% in the general benchmark | General benchmark 1000–1500 ppm; alloy- and feedstock-dependent (zhang2025researchprogresson pages 10-11) | Attached satellites, hollow particles, ellipsoids, wrapped particles, and twins are reported (zhang2025researchprogresson pages 4-6, zhang2025researchprogresson pages 10-11) | Crucible-free induction melting of a consumable alloy rod avoids ceramic crucible/nozzle contact | Minimizes refractory inclusions and is attractive when crucible compatibility is uncertain | Requires a sound, homogeneous electrode; lower fine-powder yield than VIGA. No retrieved study demonstrated EIGA for the specified Cu–Ni, NAB, Cu–Sn, CuCrZr, or GRCop alloys |
| Water atomization | Usually broad; no defensible Cu-alloy AM-cut PSD found | Not reported for the requested Cu alloys | Low; rapid water quenching freezes irregular droplets (popovich2016metalpowderadditive pages 3-6, zhang2026gasatomizationfor pages 1-3, mathias2024metalpowderas pages 8-10) | High relative to inert-gas routes because of water contact and large irregular surface area | Angularity, roughness, and agglomeration are more important than classic satellites | Refractory tundish/nozzle plus high-pressure water jets; retrieved evidence did not resolve Cu-specific refractory compatibility | Low cost, short process route, and high productivity | Poor flow, low apparent density, high oxygen, and irregular shape generally make as-atomized powder unsuitable for LPBF and unreliable for single-stream powder DED without classification and spheroidization |
| Plasma atomization | General: 0–150 or 0–200 µm; typical mean near 40 µm (popovich2016metalpowderadditive pages 3-6, mathias2024metalpowderas pages 8-10, zhang2025researchprogresson pages 10-11) | General benchmark: 32–40% below 53 µm (zhang2025researchprogresson pages 10-11) | About 95%; smooth and highly spherical | Generally below 1000 ppm in the broad benchmark (zhang2025researchprogresson pages 10-11) | Few when wire is completely melted and droplets do not collide; incomplete melting causes agglomerates | Wire feed is melted by focused plasma torches; no crucible or ceramic melt nozzle | High purity, excellent sphericity, narrow PSD, and low internal porosity | Expensive, relatively low productivity, and restricted to alloys that can first be made into consistent wire; no Cu-alloy-specific dataset was recovered |
| PREP | Usually 50–400 µm; general AM benchmark 60–250 µm, with D50 often near 200 µm (popovich2016metalpowderadditive pages 3-6, mathias2024metalpowderas pages 10-12, zhang2025researchprogresson pages 10-11) | No more than about 15% below 53 µm in the general benchmark (zhang2025researchprogresson pages 10-11) | About 98%; smooth spheres | General benchmark 50–800 ppm (zhang2025researchprogresson pages 10-11) | Very low because there is no atomizing jet to drive fines into larger droplets | Consumable rotating electrode melted in inert gas; no crucible or ceramic nozzle contact | Highest cleanliness and sphericity; low oxide and ceramic-inclusion risk | Usually too coarse for LPBF and inefficient for fine DED cuts; electrode manufacture and high-speed rotation are costly; no requested Cu-alloy-specific result found |
| Rotating-disk / centrifugal atomization | Generally coarser than gas atomization; one benchmark targeted 50–100 µm (zhang2025researchprogresson pages 13-15, zhang2026gasatomizationfor pages 1-3) | One non-Cu benchmark recovered 50% in the 50–100 µm cut (zhang2025researchprogresson pages 13-15) | Good; higher rotational speed reduces mean size, irregular particles, and satellites | Low under inert gas | Usually fewer than in gas atomization; excessive current or unstable feeding creates flaky/irregular particles | Molten stream impinges on a rapidly rotating disk or cup; refractory melt delivery may still be required | Controllable size, good sphericity, low oxidation, and potentially high yield in a coarse DED cut | Expensive rotating equipment and generally coarse PSD; splash, wetting, feed instability, and volatile-element loss are risks; no direct Cu-alloy benchmark found |
| Plasma spheroidization | Input-dependent; fines may evaporate, larger particles may agglomerate, and main/cyclone bins differ | AM-cut yield not reported | Generally improves, especially in the main bin; cyclone powder can remain irregular when molten fines adhere (sehhat2022characterizationofvirgin pages 7-9, sehhat2022characterizationofvirgin pages 4-7) | Pure Cu: virgin powder decreased 200→40 ppm; used EB-PBF powder 370→120 ppm; reconditioned powder 140→80 ppm. A second pass gave no further decrease (sehhat2022characterizationofvirgin pages 9-12) | Can remove existing satellites, but new welded particles or agglomerates can form in the cyclone fraction (sehhat2022characterizationofvirgin pages 4-7) | Powder is injected into 3,000–10,000 K Ar plasma and quenched at about 10⁶ K/s; no melt crucible/nozzle is required (sehhat2022characterizationofvirgin pages 4-7) | Upgrades irregular or recycled Cu powder; improves roundness and can reduce oxygen | Added processing step and loss through fine-particle evaporation; PSD may shift unpredictably, and repeat treatment does not necessarily improve oxygen or cyclone-bin sphericity |
| Ultrasonic vibrating-plate / sonotrode atomization | Frequency/material dependent. At 35 kHz: Ti6Al4V median about 52–62 µm and Ti25Al12Nb about 52 µm. At 40 kHz, an ORNL AMAZEMET rePOWDER steel lot gave D10/D50/D90 = 37/54/70 µm (kannan2025evaluationofpowder pages 8-14, scientific2023comparisonofultrasonic pages 4-5, scientific2023comparisonofultrasonic pages 7-8) | Ti6Al4V at 35 kHz: more than half below 63 µm; projected 52 kHz: about 95% below 63 µm. Optimized chamber recovery exceeded 98%. ORNL batch size was 60 g (kannan2025evaluationofpowder pages 8-14, scientific2023comparisonofultrasonic pages 5-7, scientific2023comparisonofultrasonic pages 7-8) | Highly spherical; the ORNL steel powder had no visible satellites (kannan2025evaluationofpowder pages 8-14, zach2023sphericalpowderscontrol pages 4-4) | ORNL 40 kHz steel: 0.011 wt% O. Ultra-high-purity Ar, short melt-film residence, and nonreactive tooling limit pickup; atomization cannot remove oxygen already in the charge (kannan2025evaluationofpowder pages 8-14, sojoodi2025integrationofcircular pages 19-21, sojoodi2025integrationofcircular pages 18-19) | Typically very few; chamber turbulence or droplet collision can still create adhered particles (kannan2025evaluationofpowder pages 8-14, scientific2023comparisonofultrasonic pages 7-8) | Arc/plasma melts feed directly on a water-cooled vibrating sonotrode, avoiding a conventional crucible and melt nozzle. Retrieved sources did not disclose a validated sonotrode material for molten Cu or Cu–Ni | Well suited to 10–100 g experimental heats; narrow PSD, low gas consumption, low internal gas porosity, and rapid composition iteration. In one ORNL comparison, lab ultrasonic powder lacked the internal gas pores present in industrial powder (kannan2025evaluationofpowder pages 8-14, scientific2023comparisonofultrasonic pages 1-2) | Low throughput; size varies with surface tension, density, temperature, frequency, and amplitude. Higher frequency makes finer powder but can increase oxygen/carbon pickup. No retrieved peer-reviewed AMAZEMET report unambiguously documented pure Cu or the requested Cu alloys with a measured median size (zach2023sphericalpowderscontrol pages 4-4, sojoodi2025integrationofcircular pages 19-21, scientific2023comparisonofultrasonic pages 4-5) |


*Table: Comparison of principal atomization and spheroidization routes relevant to copper-alloy AM powders, including size, yield, morphology, oxygen control, equipment contact materials, advantages, and failure modes. Copper-specific values are distinguished from general benchmarks, and unsupported areas are stated explicitly.*

---

### 2. Gas Atomization (Close-Coupled and Free-Fall)

Gas atomization—particularly vacuum inert-gas atomization (VIGA) in a close-coupled configuration—is the dominant industrial route for producing copper alloy AM powders. General benchmarks for VIGA report particle size ranges of 0–180 µm, yield below 53 µm of approximately 70%, sphericity of 85–90%, and oxygen levels of 200–1400 ppm (zhang2025researchprogresson pages 10-11). Close-coupled atomizers achieve higher gas velocities at the melt-gas interaction point and produce finer powders than free-fall designs, but they are susceptible to melt buildup and nozzle blockage (zhang2026gasatomizationfor pages 14-15).

**NiCu Alloy 400 (Ni-Cu base).** Roth et al. (2024; DOI: 10.1007/s00170-024-14328-7) produced NiCu Alloy 400 powder by close-coupled gas atomization at ~1600 °C (~250 °C superheat above the ~1350 °C liquidus) using a ceramic crucible on a graphite susceptor, with Ar at ~8 bar. The 15–63 µm sieved fraction had D10/D50/D90 = 28.9/42.3/61.5 µm, Hall flow of 15.22 s/50 g, apparent density of 4.38 g/cm³ (~50% relative), Hausner ratio 1.09, volumetric sphericity 0.766 (reduced by attached satellites), and no detected internal gas pores (roth2024establishingaprocess pages 2-4, roth2024establishingaprocess pages 7-9, roth2024establishingaprocess pages 5-7, roth2024establishingaprocess pages 1-2). [CITE] [NUMBERS] [NOVELTY-RISK: This is the closest commercially relevant Cu-Ni gas atomization dataset; the PI's Cu-Ni compositions overlap.]

**NAB Cu-9Al-5Fe-5Ni.** Li et al. (2021; DOI: 10.1016/j.addma.2020.101825) used gas-atomized spherical Cu-9Al-5Fe-5Ni powder (45–106 µm, D10/D50/D90 = 49.76/76.29/116.46 µm) for laser metal deposition (LMD/DED). Measured composition was 80.35 Cu, 9.70 Al, 5.48 Fe, 4.47 Ni wt%. Deposits achieved >99% relative density, YS 593–713 MPa, UTS 769–949 MPa, and elongation 10–12% (li2021nanotwinscontainingmicrostructureand pages 1-4, li2021nanotwinscontainingmicrostructureand pages 4-9). Process: blown-powder laser DED. [CITE] [NUMBERS] [NOVELTY-RISK: NAB deposited by blown-powder DED using pre-alloyed gas-atomized powder directly overlaps the PI's proposed work.]

**NAB C95800 (wire-fed DED).** Doyle (2022) deposited C95800 NAB (Cu-8.64Al-4.21Ni-3.19Fe-1.32Mn wt%) by wire-laser DED, achieving 99.58–99.89% relative density, as-printed YS 410.5 MPa, UTS 757.8 MPa, elongation 29%, hardness 218.8 HV. Heat treatment (675 °C/6 h) slightly reduced strength but increased elongation to 31.2% (doyle2022additivemanufacturingof pages 43-47, doyle2022additivemanufacturingof pages 53-58). Process: wire-laser DED. [CITE] [NUMBERS] [NAVY: NAB is the standard US Navy propeller/valve alloy.] [GAP: Wire-DED uses a different feedstock form; blown-powder DED of this composition with in-house atomized powder has not been reported.]

**Pure Cu for LPBF.** Sinico et al. (2019; DOI: 10.26153/tsw/17303) compared two gas-atomized 99.8 wt% Cu powders: Cu 15–45 (Dv10/50/90 = 17.0/26.3/40.1 µm) and Cu 10–35 (12.1/20.8/33.2 µm). Both were predominantly spherical with limited satellites; Cu 15–45 had somewhat lower mean sphericity. Powder beds exhibited ~70% reflectance at 1070 nm. Cubes >98% density were achieved at 175 W (sinico2019influenceofpowder pages 1-2, sinico2019influenceofpowder pages 2-4). [CITE] [NUMBERS]

**CuCrZr and GRCop.** Canacoo et al. (2026; DOI: 10.1007/s40684-026-00928-z) reviewed LPBF of CuCrZr (up to 99.99% relative density after aging), GRCop-42 (85% IACS, porosity 0.1–0.4% by LPBF, <0.003% after HIP by LDED), and GRCop-84 (99.9% relative density by LPBF). Favero (2025) reported GRCop-42 at 481 MPa UTS, 24% elongation, 125 HV, 83.76% IACS after 700 °C/30 min aging (favero2025additivemanufacturingfor pages 43-46, canacoo2026laseradditivemanufacturing pages 10-12). Specific gas-atomization powder characterization data (PSD, oxygen, flow) for these alloys were not recovered from the retrieved literature. [CITE] [NUMBERS] [GAP: Published CuCrZr and GRCop powder characterization data (oxygen, flow, PSD by lot) remain sparse.]

**Effect of superheat on Cu powder.** Mathias et al. (2024; DOI: 10.1557/s43578-023-01271-8) presented plots of D50 and D90 of gas-atomized Cu powders versus superheat temperature, showing that increasing superheat decreases both D50 and D90 by lowering viscosity and surface tension. D50 also decreases with increasing atomization pressure and gas-to-metal ratio (GMR). Excessive superheat can trap gas and form hollow particles (mathias2024metalpowderas pages 10-12). Process: general gas atomization. [CITE] [NUMBERS] [GAP: The underlying Cu composition and exact numerical D50-vs-superheat curve are in their Fig. 6 but were not extractable as text.]

**Melt superheat and gas parameters.** A 150–300 °C superheat range is recommended. Intermediate gas pressures are favored: high pressure can freeze metal before atomization, while low pressure produces coarser powder. Gas purity matters—99.9% Ar causes elevated O and N in powder; 99.999% Ar improves quality. Hydrogen additions can reduce oxidation and trapped bubbles, but may be hazardous (zhang2026gasatomizationfor pages 17-19, zhang2026gasatomizationfor pages 14-15, zhang2026gasatomizationfor pages 15-17).

---

### 3. Water Atomization

Water atomization produces irregular, high-oxygen copper powders unsuitable for laser-based AM without spheroidization. Rapid water quenching freezes droplets before they can spheroidize, and water contact elevates oxygen (popovich2016metalpowderadditive pages 3-6, zhang2026gasatomizationfor pages 1-3). Water-atomized powders are inexpensive and high-throughput but require post-processing (e.g., plasma spheroidization) to be used in AM.

---

### 4. Electrode Induction Gas Atomization (EIGA)

EIGA avoids crucible/nozzle contact by inductively melting a consumable alloy rod, which is attractive when crucible compatibility is uncertain. General benchmarks report 0–180 µm PSD, 30–45% yield below 53 µm, ~90% sphericity, and 1000–1500 ppm oxygen (zhang2025researchprogresson pages 10-11). EIGA Ti-48Al-2Cr-2Nb produced 15–105 µm powder with 0.092% O (zhang2025researchprogresson pages 4-6). No retrieved study demonstrated EIGA for Cu-Ni, NAB, Cu-Sn, CuCrZr, or GRCop. [GAP: EIGA of copper alloys appears unreported.]

---

### 5. Plasma Atomization

Plasma atomization melts wire feedstock with focused plasma torches, yielding 0–150/200 µm PSD, ~95% sphericity, <1000 ppm O, and virtually no satellites. However, throughput is low, cost is high, and the alloy must first be drawn into wire (popovich2016metalpowderadditive pages 3-6, zhang2025researchprogresson pages 10-11). No copper alloy plasma atomization dataset was recovered. [GAP]

---

### 6. PREP (Plasma Rotating Electrode Process)

PREP produces the highest sphericity (~98%) and lowest oxygen (50–800 ppm) but yields predominantly coarse powder (60–250 µm, D50 ~200 µm), with ≤15% below 53 µm (zhang2025researchprogresson pages 10-11). Electrode rotation speed constrains minimum D50 to ~50–150 µm (popovich2016metalpowderadditive pages 3-6). PREP is too coarse for LPBF and inefficient for fine DED cuts. No Cu-alloy PREP data were recovered. [GAP]

---

### 7. Centrifugal (Rotating Disk) Atomization

Centrifugal atomization can produce good sphericity and low oxidation. One non-Cu benchmark (FGH95 at 14,000 rpm) yielded 50% recovery in the 50–100 µm cut (zhang2025researchprogresson pages 13-15). Higher rotation speed narrows PSD and reduces irregular particles. Equipment is costly and powder tends to be coarser than close-coupled gas atomization. No Cu-alloy centrifugal atomization study was recovered (zhang2025researchprogresson pages 13-15, zhang2026gasatomizationfor pages 1-3). [GAP]

---

### 8. Plasma Spheroidization of Copper Powder

Sehhat et al. (2022; DOI: 10.21203/rs.3.rs-1840008/v1) spheroidized three conditions of OFHC copper powder using RF inductively coupled plasma (TekSphero-15). Powder was injected into 3,000–10,000 K Ar plasma and quenched at ~10⁶ K/s. Virgin Cu powder decreased from 200 ppm O to 40 ppm after spheroidization; used EB-PBF powder (370 ppm) decreased to 120 ppm; reconditioned powder (140 ppm) decreased to 80 ppm. A second spheroidization pass did not further reduce oxygen (sehhat2022characterizationofvirgin pages 9-12). Sphericity improved, especially in the main collection bin, but cyclone-bin powder could remain irregular due to adhesion of molten fines (sehhat2022characterizationofvirgin pages 7-9, sehhat2022characterizationofvirgin pages 4-7, sehhat2022characterizationofvirgin pages 14-21). [CITE] [NUMBERS] [GAP: Plasma spheroidization of Cu-Ni or NAB powders has not been reported.]

---

### 9. Ultrasonic (Vibrating-Plate / Sonotrode) Atomization

This is the method most directly relevant to the PI's planned AMAZEMET rePOWDER workflow. The process melts feedstock (wire or small charge) on a water-cooled, ultrasonically vibrated sonotrode using an electric arc or plasma torch. Capillary (Faraday) waves eject droplets whose size follows a modified Lang equation: D₃₂ ∝ (surface tension / (density × frequency²))^(1/3). Higher frequency → finer powder; doubling frequency reduces size by ~40% (scientific2023comparisonofultrasonic pages 4-5).

**AMAZEMET rePOWDER at ORNL (40 kHz, NBS steel).** Kannan et al. (2025; DOI: 10.2172/3007879, ORNL/TM-2025/4318) used the AMAZEMET rePOWDER at 40 kHz under Ar to produce 60 g batches of nanostructured bainitic steel (NBS). Powders were spherical with no visible satellites. D10/D50/D90 = 37/54/70 µm. Oxygen was 0.011 wt% (110 ppm). Critically, the lab-scale ultrasonic powder lacked the internal gas pores found in the subsequently procured industrial gas-atomized NBS powder. The ultrasonic powder sintered to >99.8% density, while industrial powder only reached 88–92% (kannan2025evaluationofpowder pages 1-8, kannan2025evaluationofpowder pages 8-14). Process: sintering/PM. [CITE] [NUMBERS] [NOVELTY-RISK: This is the only AMAZEMET rePOWDER report with quantitative powder data. It validates the concept for small-batch alloy screening but uses a steel, not copper. The PI must verify sonotrode compatibility with molten Cu/Cu-Ni.]

**AMAZEMET rePOWDER at ORNL (20 kHz, various metals).** Zach et al. (2023; DOI: 10.1051/epjconf/202328503002) described the AMAZEMET rePOWDER at 20 kHz producing spherical, free-flowing, uniform powders of various metals including Si, W, Pt-Ru, and Inconel 625. Powder was collected in low-pressure Ar. A 200 µm sieve removed unatomized material (zach2023sphericalpowderscontrol pages 4-4). Copper was not explicitly named among the demonstrated materials. [CITE] [GAP: No published AMAZEMET report unambiguously documents ultrasonic atomization of pure Cu or any Cu alloy with a measured median particle size.]

**Bałasz et al. (2023; DOI: 10.5604/01.3001.0016.3393) — UA vs GA comparison.** At 35 kHz, Ti6Al4V UA powder had a median of ~52–62 µm vs 70–90 µm for GA. UA produced finer, narrower PSD, higher sphericity, lower porosity, higher tap density, better flowability, and lower oxygen than GA (scientific2023comparisonofultrasonic pages 1-2, scientific2023comparisonofultrasonic pages 4-5, scientific2023comparisonofultrasonic pages 5-7, scientific2023comparisonofultrasonic pages 7-8). Estimated D₃₂ at 35 kHz: ~47 µm for 316L, ~52 µm for Inconel 718, ~62 µm for Ti6Al4V (scientific2023comparisonofultrasonic pages 5-7). Materials demonstrated: Ti6Al4V, Ti25Al12Nb, high-alloy steel, Ni-based alloys. Copper was not listed. [CITE] [NUMBERS]

**Sojoodi et al. (2026; DOI: 10.1007/s40830-025-00589-y) — UPA for NiTi.** The ultrasonic plasma atomization review describes operation at 20–40 kHz, noting that 40 kHz can produce higher oxygen/carbon pickup than 20 kHz under otherwise equal conditions due to greater surface area. Oxygen control strategies include ultra-high-purity Ar (<5 ppm O₂), short molten-film residence time, and non-reactive tooling (sojoodi2025integrationofcircular pages 19-21, sojoodi2025integrationofcircular pages 18-19, sojoodi2025integrationofcircular pages 21-23). [CITE]

**Müller et al. (2024; DOI: 10.1088/1757-899x/1296/1/012036) — ultrasonic atomization of aluminium bronze chips for laser DED.** This conference paper was identified in the search but was unobtainable for full-text analysis. Its title confirms that ultrasonic atomization has been applied to at least one copper alloy (aluminium bronze) and the resulting powder used in laser DED. [CITE] [NOVELTY-RISK: Directly overlaps the PI's planned workflow of ultrasonic atomization of NAB/aluminum bronze for DED. The PI should obtain and cite this paper.]

---

### 10. Crucible and Nozzle Materials for Copper and Copper-Nickel Melts

The retrieved literature is surprisingly thin on this topic for copper atomization specifically:

- **Graphite:** Widely used as a susceptor for induction heating (e.g., the Alloy 400 study used a graphite susceptor with a ceramic crucible) (roth2024establishingaprocess pages 2-4). Graphite is non-wetting to many copper alloys but can introduce carbon contamination.
- **Alumina, zirconia, boron nitride, magnesia:** Mentioned as refractory crucible/nozzle options in general atomization literature but no retrieved copper-specific study compared their compatibility, erosion rates, or contamination for Cu or Cu-Ni melts. PREP and EIGA avoid this issue entirely by eliminating the crucible.
- **Water-cooled copper crucibles:** Used in VIGA for reactive alloys such as TiSi₂ (zhang2025researchprogresson pages 4-6), but obviously not suitable when the melt itself is a copper alloy.

[GAP: No retrieved peer-reviewed paper systematically evaluated crucible/nozzle material compatibility (graphite, alumina, zirconia, BN, magnesia) for atomization of Cu-Ni or NAB melts. This is a practical knowledge gap the PI will need to address empirically or through foundry literature.]

---

### 11. In-House / Small-Batch vs. Commercial Gas-Atomized Powder

The ORNL NBS steel comparison (Kannan et al. 2025) is the strongest retrieved evidence: AMAZEMET rePOWDER (40 kHz, 60 g batches) produced spherical powder with no satellites, 0.011 wt% O, and no internal gas porosity. The same alloy produced industrially by gas atomization contained internal gas pores, and sintered samples achieved only 88–92% density vs >99.8% for the ultrasonic powder (kannan2025evaluationofpowder pages 8-14). This suggests that small-batch ultrasonic atomization can produce powder with superior internal quality, albeit at much lower throughput.

For copper specifically, Eftekhari & Jahed (2026; DOI: 10.3390/met16020197) compared five Cu powders (electrolytic, gas-atomized, mechanically ground) for cold spray. Gas-atomized powders with equiaxed grain structures offered the best combination of flowability and deformability. The finest gas-atomized Cu powder had D10/D50/D90 = 10/22/39 µm (eftekhari2026powdermanufacturingdrivenvariations pages 5-9, eftekhari2026powdermanufacturingdrivenvariations pages 9-10). Spherical morphology reduced inter-particle forces and improved flow; irregular electrolytic powder produced the highest coating porosity. [CITE] [NUMBERS]

No direct published comparison of in-house ultrasonic-atomized copper alloy powder vs. commercial gas-atomized copper alloy powder for DED print quality was found. [GAP: This is a critical gap the PI's proposal should address.]

---

### 12. Corrosion Properties of NAB AM Deposits

**WAAM NAB corrosion.** Huo et al. (2025; DOI: 10.3390/ma18102205) investigated cold metal transfer (CMT) WAAM NAB. As heat input increased from 243.8 to 644.7 J/mm, corrosion current density rose from 2.56 ± 0.04 to 7.52 ± 0.07 µA/cm², hardness declined from 198.3 to 171.7 HV, and grain size increased. The microstructure was α-Cu with minor γ₂-Cu₉Al₄ and κ phases (doyle2022additivemanufacturingof pages 43-47). Process: wire-arc DED (WAAM). No seawater immersion or comparison to wrought Cu-Ni C71500 was reported. [CITE] [NUMBERS] [NAVY]

---

### Top 5 Things the PI Should Know

**1. Ultrasonic atomization of copper alloys is essentially unreported, but one aluminium bronze study exists.** Müller et al. (2024, DOI: 10.1088/1757-899x/1296/1/012036) ultrasonically atomized aluminium bronze grinding chips and used the powder for laser DED. This is the only identified study demonstrating the PI's exact workflow (ultrasonic atomization → copper alloy → DED) and should be obtained and cited. All other AMAZEMET/UA demonstrations are for Ti, Ni, steel, or specialty metals—not Cu or Cu-Ni. [NOVELTY-RISK] [GAP]

**2. The ORNL AMAZEMET rePOWDER report (Kannan 2025) is the best quantitative benchmark for the instrument the PI will use.** At 40 kHz, NBS steel powder had D50 = 54 µm, O = 0.011 wt%, no satellites, and no internal gas porosity—superior to the same alloy gas-atomized industrially. Batch size was 60 g. The PI should expect similar throughput constraints and verify sonotrode compatibility with molten Cu (~1100 °C for Cu-Ni at 10–30% Ni). [NUMBERS]

**3. Crucible/nozzle material compatibility for Cu and Cu-Ni atomization is a practical gap in the AM powder literature.** The Alloy 400 study used a ceramic crucible + graphite susceptor but did not name the ceramic. No retrieved study systematically compared graphite, alumina, zirconia, BN, or magnesia for copper melt containment during atomization. The PI's use of induction melting on the AMAZEMET sonotrode partially avoids this issue (crucible-free), but the sonotrode material itself must tolerate molten Cu contact. [GAP]

**4. Gas-atomized NAB and Cu-Ni powders for DED produce dense, strong deposits.** Li et al. (2021) achieved >99% density, 769–949 MPa UTS for Cu-9Al-5Fe-5Ni by LMD; Doyle (2022) achieved 99.6–99.9% density and 757.8 MPa UTS for wire-DED C95800 NAB. These benchmarks set the bar the PI's ultrasonic-atomized powders must match. [NUMBERS]

**5. Oxygen control is the single most critical powder quality parameter for copper AM.** Copper oxides decompose during laser processing, releasing trapped gas that forms porosity (canacoo2026laseradditivemanufacturing pages 6-8). Plasma spheroidization reduced virgin Cu powder from 200 to 40 ppm O (Sehhat 2022). Ultrasonic atomization in high-purity Ar achieved 110 ppm O for steel (Kannan 2025). The PI should measure oxygen per lot (ASTM E 1019) and target <200 ppm; the literature provides no copper-alloy-specific threshold for DED, which is itself a publishable gap. [NUMBERS] [GAP]


References

1. (li2021nanotwinscontainingmicrostructureand pages 1-4): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

2. (roth2024establishingaprocess pages 5-7): Jan-Philipp Roth, Ivo Šulák, Tomáš Kruml, Wojciech Polkowski, Tomasz Dudziak, Peter Böhlke, Ulrich Krupp, and Katrin Jahns. Establishing a process route for additive manufacturing of nicu-based alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments. The International Journal of Advanced Manufacturing Technology, Sep 2024. URL: https://doi.org/10.1007/s00170-024-14328-7, doi:10.1007/s00170-024-14328-7. This article has 6 citations.

3. (sinico2019influenceofpowder pages 2-4): M. Sinico, G. Cogo, M. Benettoni, I. Calliari, and A. Pepato. Influence of powder particle size distribution on the printability of pure copper for selective laser melting. Unknown, Jan 2019. URL: https://doi.org/10.26153/tsw/17303, doi:10.26153/tsw/17303. This article has 35 citations.

4. (zhang2025researchprogresson pages 10-11): Sen Zhang, K. Guo, Yongquan Qing, and Changsheng Liu. Research progress on the preparation technology of spherical alloy powders for laser additive manufacturing. Materials, Jul 2025. URL: https://doi.org/10.3390/ma18143385, doi:10.3390/ma18143385. This article has 15 citations.

5. (roth2024establishingaprocess pages 2-4): Jan-Philipp Roth, Ivo Šulák, Tomáš Kruml, Wojciech Polkowski, Tomasz Dudziak, Peter Böhlke, Ulrich Krupp, and Katrin Jahns. Establishing a process route for additive manufacturing of nicu-based alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments. The International Journal of Advanced Manufacturing Technology, Sep 2024. URL: https://doi.org/10.1007/s00170-024-14328-7, doi:10.1007/s00170-024-14328-7. This article has 6 citations.

6. (mathias2024metalpowderas pages 10-12): Laura E. T. Mathias, Vitor E. Pinotti, Bruna F. Batistão, Nicolas Rojas-Arias, Gustavo Figueira, Angelo F. Andreoli, and Piter Gargarella. Metal powder as feedstock for laser-based additive manufacturing: from production to powder modification. Journal of Materials Research, 39:19-47, Dec 2024. URL: https://doi.org/10.1557/s43578-023-01271-8, doi:10.1557/s43578-023-01271-8. This article has 77 citations and is from a peer-reviewed journal.

7. (roth2024establishingaprocess pages 1-2): Jan-Philipp Roth, Ivo Šulák, Tomáš Kruml, Wojciech Polkowski, Tomasz Dudziak, Peter Böhlke, Ulrich Krupp, and Katrin Jahns. Establishing a process route for additive manufacturing of nicu-based alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments. The International Journal of Advanced Manufacturing Technology, Sep 2024. URL: https://doi.org/10.1007/s00170-024-14328-7, doi:10.1007/s00170-024-14328-7. This article has 6 citations.

8. (mathias2024metalpowderas pages 4-5): Laura E. T. Mathias, Vitor E. Pinotti, Bruna F. Batistão, Nicolas Rojas-Arias, Gustavo Figueira, Angelo F. Andreoli, and Piter Gargarella. Metal powder as feedstock for laser-based additive manufacturing: from production to powder modification. Journal of Materials Research, 39:19-47, Dec 2024. URL: https://doi.org/10.1557/s43578-023-01271-8, doi:10.1557/s43578-023-01271-8. This article has 77 citations and is from a peer-reviewed journal.

9. (zhang2026gasatomizationfor pages 14-15): Chao-Cai Zhang, Fu-Zhong Chu, and Zong-Yan Zhou. Gas atomization for metal powder production in additive manufacturing: a review. Materials Science in Additive Manufacturing, 0:026220051, Sep 2026. URL: https://doi.org/10.36922/msam026220051, doi:10.36922/msam026220051. This article has 0 citations and is from a peer-reviewed journal.

10. (roth2024establishingaprocess pages 7-9): Jan-Philipp Roth, Ivo Šulák, Tomáš Kruml, Wojciech Polkowski, Tomasz Dudziak, Peter Böhlke, Ulrich Krupp, and Katrin Jahns. Establishing a process route for additive manufacturing of nicu-based alloy 400: an alignment of gas atomization, laser powder bed fusion, and design of experiments. The International Journal of Advanced Manufacturing Technology, Sep 2024. URL: https://doi.org/10.1007/s00170-024-14328-7, doi:10.1007/s00170-024-14328-7. This article has 6 citations.

11. (zhang2026gasatomizationfor pages 15-17): Chao-Cai Zhang, Fu-Zhong Chu, and Zong-Yan Zhou. Gas atomization for metal powder production in additive manufacturing: a review. Materials Science in Additive Manufacturing, 0:026220051, Sep 2026. URL: https://doi.org/10.36922/msam026220051, doi:10.36922/msam026220051. This article has 0 citations and is from a peer-reviewed journal.

12. (zhang2025researchprogresson pages 4-6): Sen Zhang, K. Guo, Yongquan Qing, and Changsheng Liu. Research progress on the preparation technology of spherical alloy powders for laser additive manufacturing. Materials, Jul 2025. URL: https://doi.org/10.3390/ma18143385, doi:10.3390/ma18143385. This article has 15 citations.

13. (popovich2016metalpowderadditive pages 3-6): Anatoliy Popovich and Vadim Sufiiarov. Metal powder additive manufacturing. ArXiv, Jul 2016. URL: https://doi.org/10.5772/63337, doi:10.5772/63337. This article has 142 citations.

14. (zhang2026gasatomizationfor pages 1-3): Chao-Cai Zhang, Fu-Zhong Chu, and Zong-Yan Zhou. Gas atomization for metal powder production in additive manufacturing: a review. Materials Science in Additive Manufacturing, 0:026220051, Sep 2026. URL: https://doi.org/10.36922/msam026220051, doi:10.36922/msam026220051. This article has 0 citations and is from a peer-reviewed journal.

15. (mathias2024metalpowderas pages 8-10): Laura E. T. Mathias, Vitor E. Pinotti, Bruna F. Batistão, Nicolas Rojas-Arias, Gustavo Figueira, Angelo F. Andreoli, and Piter Gargarella. Metal powder as feedstock for laser-based additive manufacturing: from production to powder modification. Journal of Materials Research, 39:19-47, Dec 2024. URL: https://doi.org/10.1557/s43578-023-01271-8, doi:10.1557/s43578-023-01271-8. This article has 77 citations and is from a peer-reviewed journal.

16. (zhang2025researchprogresson pages 13-15): Sen Zhang, K. Guo, Yongquan Qing, and Changsheng Liu. Research progress on the preparation technology of spherical alloy powders for laser additive manufacturing. Materials, Jul 2025. URL: https://doi.org/10.3390/ma18143385, doi:10.3390/ma18143385. This article has 15 citations.

17. (sehhat2022characterizationofvirgin pages 7-9): M. Hossein Sehhat, Tristan Cullom, and Joseph W. Newkirk. Characterization of virgin, recycled, and oxygen-reduced copper powders processed by the plasma spheroidization. Unknown journal, Jul 2022. URL: https://doi.org/10.21203/rs.3.rs-1840008/v1, doi:10.21203/rs.3.rs-1840008/v1.

18. (sehhat2022characterizationofvirgin pages 4-7): M. Hossein Sehhat, Tristan Cullom, and Joseph W. Newkirk. Characterization of virgin, recycled, and oxygen-reduced copper powders processed by the plasma spheroidization. Unknown journal, Jul 2022. URL: https://doi.org/10.21203/rs.3.rs-1840008/v1, doi:10.21203/rs.3.rs-1840008/v1.

19. (sehhat2022characterizationofvirgin pages 9-12): M. Hossein Sehhat, Tristan Cullom, and Joseph W. Newkirk. Characterization of virgin, recycled, and oxygen-reduced copper powders processed by the plasma spheroidization. Unknown journal, Jul 2022. URL: https://doi.org/10.21203/rs.3.rs-1840008/v1, doi:10.21203/rs.3.rs-1840008/v1.

20. (kannan2025evaluationofpowder pages 8-14): Rangasayee Kannan, Yiyu Wang, and Peeyush Nandwana. Evaluation of powder metallurgy manufactured nanostructured bainitic steel for wind turbine gearbox applications. Unknown journal, Dec 2025. URL: https://doi.org/10.2172/3007879, doi:10.2172/3007879.

21. (scientific2023comparisonofultrasonic pages 4-5): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

22. (scientific2023comparisonofultrasonic pages 7-8): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

23. (scientific2023comparisonofultrasonic pages 5-7): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

24. (zach2023sphericalpowderscontrol pages 4-4): Michael Zach, Dane Brashear, Jonah Duran, Łukasz Żrodowski, Bartosz Kalicki, Tomasz Choma, Marcin Sołowiow, and Steven Adler. Spherical powders: control over the size and morphology of powders for additive manufacturing and enriched stable isotope nuclear targets. EPJ Web of Conferences, 285:03002, Jan 2023. URL: https://doi.org/10.1051/epjconf/202328503002, doi:10.1051/epjconf/202328503002. This article has 10 citations and is from a peer-reviewed journal.

25. (sojoodi2025integrationofcircular pages 19-21): Mahyar Sojoodi, Alireza Behvar, Harsh Bajaj, Shiva Mohajerani, Saeedeh Vanaei, Nasrin Taheri Andani, Anwar Algamal, Fatemeh Ghasemibojd, Mahsa Beyk Khorasani, Ahu Celebi, and Mohammad Elahinia. Integration of circular economy into metal additive manufacturing: a review of ultrasonic plasma atomization for producing virgin and recycled niti powder. Shape Memory and Superelasticity, 12:5-45, Oct 2026. URL: https://doi.org/10.1007/s40830-025-00589-y, doi:10.1007/s40830-025-00589-y. This article has 7 citations.

26. (sojoodi2025integrationofcircular pages 18-19): Mahyar Sojoodi, Alireza Behvar, Harsh Bajaj, Shiva Mohajerani, Saeedeh Vanaei, Nasrin Taheri Andani, Anwar Algamal, Fatemeh Ghasemibojd, Mahsa Beyk Khorasani, Ahu Celebi, and Mohammad Elahinia. Integration of circular economy into metal additive manufacturing: a review of ultrasonic plasma atomization for producing virgin and recycled niti powder. Shape Memory and Superelasticity, 12:5-45, Oct 2026. URL: https://doi.org/10.1007/s40830-025-00589-y, doi:10.1007/s40830-025-00589-y. This article has 7 citations.

27. (scientific2023comparisonofultrasonic pages 1-2): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

28. (li2021nanotwinscontainingmicrostructureand pages 4-9): Boyuan Li, Han Zheng, Changjun Han, and Kun Zhou. Nanotwins-containing microstructure and superior mechanical strength of a cu‒9al‒5fe‒5ni alloy additively manufactured by laser metal deposition. Additive manufacturing, 39:101825, Mar 2021. URL: https://doi.org/10.1016/j.addma.2020.101825, doi:10.1016/j.addma.2020.101825. This article has 99 citations and is from a highest quality peer-reviewed journal.

29. (doyle2022additivemanufacturingof pages 43-47): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

30. (doyle2022additivemanufacturingof pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

31. (sinico2019influenceofpowder pages 1-2): M. Sinico, G. Cogo, M. Benettoni, I. Calliari, and A. Pepato. Influence of powder particle size distribution on the printability of pure copper for selective laser melting. Unknown, Jan 2019. URL: https://doi.org/10.26153/tsw/17303, doi:10.26153/tsw/17303. This article has 35 citations.

32. (favero2025additivemanufacturingfor pages 43-46): G Favero. Additive manufacturing for advanced heat transfer solutions: from material to thermal management application. Unknown journal, 2025.

33. (canacoo2026laseradditivemanufacturing pages 10-12): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

34. (zhang2026gasatomizationfor pages 17-19): Chao-Cai Zhang, Fu-Zhong Chu, and Zong-Yan Zhou. Gas atomization for metal powder production in additive manufacturing: a review. Materials Science in Additive Manufacturing, 0:026220051, Sep 2026. URL: https://doi.org/10.36922/msam026220051, doi:10.36922/msam026220051. This article has 0 citations and is from a peer-reviewed journal.

35. (sehhat2022characterizationofvirgin pages 14-21): M. Hossein Sehhat, Tristan Cullom, and Joseph W. Newkirk. Characterization of virgin, recycled, and oxygen-reduced copper powders processed by the plasma spheroidization. Unknown journal, Jul 2022. URL: https://doi.org/10.21203/rs.3.rs-1840008/v1, doi:10.21203/rs.3.rs-1840008/v1.

36. (kannan2025evaluationofpowder pages 1-8): Rangasayee Kannan, Yiyu Wang, and Peeyush Nandwana. Evaluation of powder metallurgy manufactured nanostructured bainitic steel for wind turbine gearbox applications. Unknown journal, Dec 2025. URL: https://doi.org/10.2172/3007879, doi:10.2172/3007879.

37. (sojoodi2025integrationofcircular pages 21-23): Mahyar Sojoodi, Alireza Behvar, Harsh Bajaj, Shiva Mohajerani, Saeedeh Vanaei, Nasrin Taheri Andani, Anwar Algamal, Fatemeh Ghasemibojd, Mahsa Beyk Khorasani, Ahu Celebi, and Mohammad Elahinia. Integration of circular economy into metal additive manufacturing: a review of ultrasonic plasma atomization for producing virgin and recycled niti powder. Shape Memory and Superelasticity, 12:5-45, Oct 2026. URL: https://doi.org/10.1007/s40830-025-00589-y, doi:10.1007/s40830-025-00589-y. This article has 7 citations.

38. (eftekhari2026powdermanufacturingdrivenvariations pages 5-9): Niloofar Eftekhari and Hamid Jahed. Powder manufacturing-driven variations in flowability and deformation behavior of pure copper powders for cold spray additive manufacturing. Metals, 16:197, Feb 2026. URL: https://doi.org/10.3390/met16020197, doi:10.3390/met16020197. This article has 2 citations.

39. (eftekhari2026powdermanufacturingdrivenvariations pages 9-10): Niloofar Eftekhari and Hamid Jahed. Powder manufacturing-driven variations in flowability and deformation behavior of pure copper powders for cold spray additive manufacturing. Metals, 16:197, Feb 2026. URL: https://doi.org/10.3390/met16020197, doi:10.3390/met16020197. This article has 2 citations.

40. (canacoo2026laseradditivemanufacturing pages 6-8): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.
