<!--
Edison Scientific LITERATURE task (batch 2)
- Task ID: 4f682962-96a3-4ab9-8128-08ceaae95e73
- Submitted: 2026-10-17T05:37:00Z
- Fetched: 2026-10-17T06:08:50Z (status: success)
- Raw trajectory JSON: ../raw/b2-01-ultrasonic-atomization-cu-melts.json.gz
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

QUESTION: What limits ultrasonic (vibrating-sonotrode) atomization of copper
and copper-nickel melts? Specifically: (a) does Lang's relation
d50 = 0.34 (8 pi sigma / (rho f^2))^(1/3) hold for metal melts on a vibrating
plate, and what surface tension and density values (vs temperature and Ni,
Al, Fe, Mn content) should be used for Cu, 90-10 and 70-30 Cu-Ni, and NAB?
(b) How much melt superheat does ultrasonic or other drop-on-plate
atomization need to avoid freezing on the sonotrode, given that an induction
module limited to about 1300 C leaves only ~60 C above the 70-30 Cu-Ni
liquidus (1238 C)? (c) Which sonotrode materials survive copper alloy melts
(Ti-6Al-4V reacts with Cu to form liquid at low temperature; molybdenum/TZM,
niobium, ceramics or coatings), and is wetting or erosion of the sonotrode by
Cu melts reported? (d) What oxygen contents result when copper alloys are
atomized under argon, and how do 20, 35, 40 and 60 kHz compare in size,
yield and oxygen? Report any ultrasonic atomization of Cu, Cu-Ni, bronzes,
NAB or other alloys melting near 1100-1250 C, with numbers.

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

QUESTION: What limits ultrasonic (vibrating-sonotrode) atomization of copper
and copper-nickel melts? Specifically: (a) does Lang's relation
d50 = 0.34 (8 pi sigma / (rho f^2))^(1/3) hold for metal melts on a vibrating
plate, and what surface tension and density values (vs temperature and Ni,
Al, Fe, Mn content) should be used for Cu, 90-10 and 70-30 Cu-Ni, and NAB?
(b) How much melt superheat does ultrasonic or other drop-on-plate
atomization need to avoid freezing on the sonotrode, given that an induction
module limited to about 1300 C leaves only ~60 C above the 70-30 Cu-Ni
liquidus (1238 C)? (c) Which sonotrode materials survive copper alloy melts
(Ti-6Al-4V reacts with Cu to form liquid at low temperature; molybdenum/TZM,
niobium, ceramics or coatings), and is wetting or erosion of the sonotrode by
Cu melts reported? (d) What oxygen contents result when copper alloys are
atomized under argon, and how do 20, 35, 40 and 60 kHz compare in size,
yield and oxygen? Report any ultrasonic atomization of Cu, Cu-Ni, bronzes,
NAB or other alloys melting near 1100-1250 C, with numbers.

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


# Limits of vibrating-sonotrode atomization for copper-alloy DED powders

**Bottom line.** Nickel–aluminum bronze (NAB) has been induction-melted at **1300 °C** and atomized onto a **40 kHz carbon-fiber sonotrode** under argon, producing spherical, flowing powder—but with measurable sonotrode-fiber contamination. That demonstration does **not** establish that a Cu–30Ni melt with only about 62 °C nominal superheat will atomize continuously without freezing, nor does it validate a copper-alloy-specific frequency–size law. Direct, composition-resolved Cu–Ni atomization results were not established in the accessible evidence. [CITE] [NUMBERS] [NOVELTY-RISK: NAB powder production itself is demonstrated] [GAP] (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 6-7)

## (a) Lang scaling and melt properties

**What the equation predicts.** The commonly used expression is \(D\simeq0.34[8\pi\sigma/(\rho f^{2})]^{1/3}\), with **liquid** surface tension \(\sigma\), **liquid** density \(\rho\), and frequency \(f\) in SI units. In one metal-powder study it is presented as a *Sauter mean diameter*, \(D_{32}\), and as a first-order, deep-pool approximation—not a proven identity for the measured powder **volume-median \(D_{50}\)**. Film depth, acoustic amplitude, feed rate, viscosity, cavitation, oxidation and solidification shrinkage can change the result. A study of 20 kHz Sn–Ag–Cu solder found that increasing feed from 15 to 25 kg/h increased median size, while increasing vibrational amplitude from 60% to 90% increased it from approximately 100 to 116 µm under its tested conditions: neither trend is encoded in Lang’s expression. [CITE] [NUMBERS] [GAP: no validated Cu–Ni or NAB \(D_{50}\) calibration] (scientific2023comparisonofultrasonic pages 4-5, scientific2023comparisonofultrasonic pages 5-7, wisutmethangoon2011productionofsac305 pages 3-6, wisutmethangoon2011productionofsac305 pages 1-2, wisutmethangoon2011productionofsac305 pages 2-3)

**Use measured properties at the *plate-film temperature*, not room-temperature alloy density or furnace set point.** Egry, Brillo and Matsushita measured liquid **pure Cu** at its 1358 K liquidus: \(\rho_L=7.89\) g cm⁻³ and \(\sigma_L=1.29\) N m⁻¹. Their fitted temperature laws are \(\rho(T)=7.89[1-1.0\times10^{-4}(T-1358)]\) g cm⁻³ and \(\sigma(T)=1.29-2.34\times10^{-4}(T-1358)\) N m⁻¹, where \(T\) is in kelvin and the laws should be used within the experimentally appropriate temperature range. Thus **at 1300 °C (1573 K)** these fits give approximately **7.72 g cm⁻³ and 1.24 N m⁻¹**; the corresponding *illustrative* Lang diameters are approximately **92, 63, 58 and 44 µm** at **20, 35, 40 and 60 kHz**, respectively. These are calculated liquid-drop characteristic sizes, **not measured Cu powder medians or yields**. An independent sessile-drop experiment at **1373 K** instead found \(\sigma=1.348\pm0.033\) N m⁻¹ using \(\rho=7.925\) g cm⁻³, demonstrating meaningful inter-study sensitivity. Dissolved or atmospheric oxygen can substantially lower Cu surface tension and even change the sign of its apparent temperature coefficient. [CITE] [NUMBERS] (sangiorgi1988wettabilityofhotpressed pages 2-4, morita2006surfacetensionof pages 1-3, sangiorgi1988wettabilityofhotpressed pages 4-6, egry2005thermophysicalpropertiesof pages 2-3)

**Cu–Ni, Fe/Mn/Cr and NAB require composition-aware inputs.** The measured Cu–Fe–Ni study finds density approximately linear with temperature at fixed composition, but *nonlinear* composition dependence: liquid Cu–Ni has a **negative excess molar volume**, parameterized there as \(-0.85c_{\rm Cu}c_{\rm Ni}\) cm³ mol⁻¹ when mole fractions are used. Its surface-tension analysis uses a Butler surface-segregation model, rather than simply averaging elemental tensions. The paper reports Cu–Fe–Ni compositions and liquidus-based fits, **not certified numerical \(\rho(T),\sigma(T)\) pairs for commercial 90–10 or 70–30 Cu–Ni, or for Mn/Cr-bearing Cu–Ni and NAB**. Its Cu–Fe–Ni trends cannot substitute uncritically for Cu–Ni–Al–Fe–Mn, particularly because Al changes chemistry and an oxide-bearing surface changes the relevant effective interface. Obtain composition-specific liquidus and liquid properties, measure or bound \(\sigma\) under the actual argon/oxygen conditions, and calibrate predicted \(D_{32}\) against *unsieved* measured PSD; otherwise report predictions as sensitivity ranges, not validated \(D_{50}\). [CITE] [GAP] (egry2005thermophysicalpropertiesof pages 1-2, egry2005thermophysicalpropertiesof pages 2-3, egry2005thermophysicalpropertiesof pages 3-5, morita2006surfacetensionof pages 1-3)

## (b) Superheat and freeze-on-plate risk

**No defensible universal minimum superheat was found for drop-on-plate Cu–Ni atomization.** A furnace set to **1300 °C** against the stipulated **1238 °C** Cu–30Ni liquidus gives **62 °C nominal furnace superheat**, *not* 62 °C guaranteed at the nozzle or sonotrode. A directly relevant precedent demonstrates induction atomization of **CuAl10Ni5Fe5** chips at **1300 °C**, through a **1.5 bar** nozzle system, onto a **40 kHz** carbon-fiber plate in **grade-5.0 argon**; it does not give the film temperature, liquidus-to-film margin, run-to-run freeze rate or equivalent 70–30 Cu–Ni test. A separate 20 kHz drop-fed Sn–Ag–Cu solder experiment operated at **270–350 °C** versus a **217–219 °C melting interval**—roughly **51–133 °C** furnace superheat—but cannot define a copper-alloy threshold because the thermophysical properties and heated hardware differ. [CITE] [NUMBERS] [GAP] (uhlmann2024acomparativeevaluation pages 4-6, wisutmethangoon2011productionofsac305 pages 1-2, wisutmethangoon2011productionofsac305 pages 2-3)

The constraint is a **local, transient heat balance**: cooling from the crucible through the nozzle and free stream plus transfer into the plate must be offset by sensible/latent heat delivery and any local heating. A 62 °C margin can therefore be viable in a sufficiently hot, short, well-controlled path, or inadequate on a cold plate or during startup; neither outcome is established experimentally here. Arc-on-plate atomization provides a different boundary condition: its authors explicitly maintain a molten pool on a cooled sonotrode with a local arc and state that separated melting/draining can interrupt atomization. Their preferred operating window for *Ti–6Al–4V* is approximately **1.3–1.5 times its absolute liquidus temperature**; applying that figure to Cu–30Ni as a required superheat would be unjustified. Test 70–30 with measured nozzle exit and plate-film temperatures, recorded flow interruptions, adherent-frozen mass and usable-powder mass before claiming a minimum margin. [CITE] [GAP] (scientific2023comparisonofultrasonic pages 2-4, scientific2023comparisonofultrasonic pages 5-7, wisutmethangoon2011productionofsac305 pages 2-3)

## (c) Sonotrode survival, wetting and erosion

* **Ti–6Al–4V: reject as a presumed inert Cu-contact plate.** Li and Lin found **excellent wetting** when Cu thin films contacted Ti–6Al–4V at **1125 °C for 60 s in flowing Ar**; Ti dissolved rapidly after Cu melted, and Ti–Cu reaction products occurred. They identify Ti–Cu eutectic temperatures of **875 and 960 °C**. This is a joining experiment, **not a measured sonotrode lifetime**; it nevertheless provides strong evidence against assuming Ti alloy remains chemically isolated from a 1100–1300 °C copper-alloy film. [CITE] [NUMBERS] (li2004activejoiningof pages 1-3, li2004activejoiningof pages 3-6)
* **Carbon fiber: demonstrated with NAB, but not contamination-free.** In the **40 kHz, 1300 °C** NAB experiment, microscopy found detached fibers approximately **20 µm** long in the atomized powder, attributed to the binder-free woven-carbon sonotrode. The publication does not quantify service life, melt wetting or carbon pickup in each powder lot. [CITE] [NUMBERS] [NAVY: recycled marine-propeller bronze] [NOVELTY-RISK: directly overlaps ultrasonic NAB feedstock] (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 10-12)
* **TZM/Mo: a plausible refractory candidate, not Cu–Ni-qualified.** Ciftcli and coauthors used a **30 mm TZM rod at 40 kHz** to ultrasonically atomize **C103 (Nb–10Hf–1Ti, wt%)** under argon. This establishes a working refractory-sonotrode architecture, **not** measured copper wetting, Mo dissolution into Cu–Ni, plate erosion or survival through repeated 1300 °C induction pours. **Nb and ceramic/coated plates likewise lack demonstrated copper-alloy sonotrode lifetimes in the evidence reviewed.** Static sessile-drop data show pure Cu on several hot-pressed **Si₃N₄** ceramics at **1373 K** has contact angles around **135°** (non-wetting), but static non-wetting is not proof that a vibrating, thermally shocked ceramic plate will couple acoustic energy or survive. Screen plate candidates by continuous-run lifetime, contact angle *and* ultrasonic response, adhered metal and powder C/Mo/Nb/Ti/Si contamination. [CITE] [NUMBERS] [GAP] (ciftcli2025alloydevelopmentfrom pages 1-3, sangiorgi1988wettabilityofhotpressed pages 1-2, sangiorgi1988wettabilityofhotpressed pages 2-4)

## (d) Actual powders, oxygen and frequency comparisons

The relevant measurements are **not a controlled 20-versus-35-versus-40-versus-60 kHz Cu-alloy experiment**: different machines, melts, measurement conventions and sieving prevent attributing their differences solely to frequency. Moreover, **Carney flow in s/150 g is not Hall flow in s/50 g**. [CITE] [GAP] (uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 6-7, scientific2023comparisonofultrasonic pages 10-11, scientific2023comparisonofultrasonic pages 8-10)

1. **E. Uhlmann, J. Polte, J. M. Fasselt, V. Müller, C. Klötzer-Freese, R. Kleba-Ehrhardt, M. Biegler and M. Rethmeier, “A Comparative Evaluation of Powder Characteristics of Recycled Material from Bronze Grinding Chips for Additive Manufacturing,” *Materials* 17 (2024) 3396, DOI: 10.3390/ma17143396.** **Process:** ultrasonic production of candidate **blown-powder laser DED** feedstock from ship-propeller grinding chips, **not** a seawater test of its resulting deposit. **Alloy:** nominal Cu–10Al–5Ni–5Fe (wt%; CC333G; Mn permitted up to 3); powder EDX: Cu **75.16**, Al **9.83**, Fe **6.76**, Ni **5.91**, Mn **2.33 wt%** (EDX is not a precise bulk-assay guarantee). **Atomization:** 1300 °C induction, 40 kHz carbon-fiber plate, argon 5.0, 1.5 bar nozzle-system pressure; powder sieved at 200 µm. **Powder:** area-equivalent \(X_{A,10}/X_{A,50}/X_{A,90}=\)**48/98/174 µm**; aspect ratio mean **0.935**, **82%** of particles above 0.9; **0.019 wt% O = 190 ppm**, compared with **0.073 wt% = 730 ppm** in starting chips. **Carney**, not Hall, flow **8.62 s/150 g**; Hausner ratio **1.05**. Carbon-fiber debris was observed. No usable-size mass yield, seawater exposure, deposit porosity or deposit corrosion current was reported in this powder comparison. [CITE] [NUMBERS] [NAVY] [NOVELTY-RISK: NAB powder is prior art] [GAP: Cu–Ni and deposit qualification remain] (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 2-4, uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 7-10, uhlmann2024acomparativeevaluation pages 6-7, uhlmann2024acomparativeevaluation pages 12-13)
2. **J. Ciftcli, T. Choma, B. Morończyk, B. Kalicki, F. Puchalski and Ł. Żrodowski, “Alloy Development from Sustainable Materials – Close-Loop of Materials Using Ultrasonic Atomization,” *Journal of the Japan Society of Powder and Powder Metallurgy* 72 Suppl. (2025) S729–S735, DOI: 10.2497/jjspm.15E-SIS13-03.** **Process:** rePOWDER ultrasonic atomization, not a demonstrated Cu-alloy DED/corrosion comparison. A figure depicts **induction atomization of a copper alloy**, but provides **no copper composition, copper PSD, Cu powder oxygen, melt temperature or Cu yield**. Its *separate* **40 kHz** recycled Ti-alloy-chip run reports volume-based **D10/D50/D90 = 36/49/118 µm**, **>85% below 100 µm**, oxygen pickup approximately **220 ppm**, final oxygen **<600 ppm**; its **60 kHz** induction example is *Mg–1Ag*, not copper. Do not quote Ti/Mg oxygen or yields as copper values. [CITE] [NUMBERS: non-Cu only] [GAP] (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6)
3. **B. Bałasz, M. Bielecki, W. Gulbiński and Ł. Słoboda, “Comparison of Ultrasonic and Other Atomization Methods in Metal Powder Production,” *Journal of Achievements in Materials and Manufacturing Engineering* 116 (2023) 11–24, DOI: 10.5604/01.3001.0016.3393.** **Process:** arc-heated **35 kHz** ultrasonic atomization of **Ti–6Al–4V (wt%)**, *not* Cu–Ni. It reports **94%** feed converted into <100 µm powder and **70.3% of powder mass** in its classified 63 ± 20 µm fraction; classified volume-based **D10/D50/D90 = 45.4/55.0/62.4 µm**; apparent/tap densities **2.62/2.86 g cm⁻³**; **Hall flow 25.1–27.9 s/50 g**; powder porosity **0.27%**; feed-to-powder oxygen **0.0036→0.0039 wt% (36→39 ppm)**. These yield and oxygen numbers belong to this **arc-on-plate Ti setup**, not an induction-fed copper run. [CITE] [NUMBERS] [GAP] (scientific2023comparisonofultrasonic pages 10-11, scientific2023comparisonofultrasonic pages 7-8, scientific2023comparisonofultrasonic pages 8-10, scientific2023comparisonofultrasonic pages 11-13)
4. **S. Wróbel, P. Ostachowski, K. Żaba, P. Maj, I. Różycka and P. Wesołowski, “Enhancing Niobium Powder Quality for Additive Manufacturing Through Ultrasonic Atomization and Calibrated Rolling,” *International Journal of Advanced Manufacturing Technology* 145 (2026) 4097–4111, DOI: 10.1007/s00170-026-18599-0.** **Process:** arc-on-plate **35 kHz** ultrasonic atomization of **elemental Nb**, not Cu: sieved <100 µm powder **D10/D50/D90 = 44.12/54.99/66.85 µm**, mean sphericity **0.94**. A **56.57 µm** model *Sauter mean* was compared with measured **54.99 µm D50**; this close agreement for Nb is not a validation for Cu–Ni. Its **<10 ppm oxygen** setting refers to *chamber gas*, **not reported Nb powder oxygen**. [CITE] [NUMBERS] [GAP] (wrobel2026enhancingniobiumpowder pages 2-5, wrobel2026enhancingniobiumpowder pages 5-7, wrobel2026enhancingniobiumpowder pages 7-10)
5. **P. Kustron, M. Korzeniowski, A. Sajbura, T. Piwowarczyk, P. Kaczynski and P. Sokolowski, “Development of High-Power Ultrasonic System Dedicated to Metal Powder Atomization,” *Applied Sciences* 13 (2023) 8984, DOI: 10.3390/app13158984.** **Process:** **20-versus-70 kHz water** atomization on prototype plates; reported 50%-droplet ranges **35–55 versus 10–25 µm**. Its table’s “liquid metal” diameters **86.15 versus 37.37 µm** are **calculated**, not an experimental Cu or Cu–Ni yield/oxygen comparison. [CITE] [NUMBERS: water experiment only] [GAP] (kustron2023developmentofhighpower pages 2-4)

**For 20, 35, 40 and 60 kHz specifically:** \(f^{-2/3}\) gives *relative theoretical diameters*, referenced to 20 kHz, of **1.00, 0.69, 0.63 and 0.48** at unchanged \(\sigma/\rho\). It supplies **no experimentally justified Cu-alloy size yield or oxygen ranking**: 20 kHz metal results above are Ti and low-melting solder; 35 kHz are Ti/Nb; 40 kHz is the directly quantified NAB result; and the retrieved 60 kHz induction example is Mg alloy. Oxygen must be measured for each **powder lot** alongside incoming feed oxygen and chamber oxygen; argon alone does not set a universal copper-powder ppm value. [CITE] [GAP] (uhlmann2024acomparativeevaluation pages 4-6, ciftcli2025alloydevelopmentfrom pages 1-3, scientific2023comparisonofultrasonic pages 4-5, kustron2023developmentofhighpower pages 2-4, scientific2023comparisonofultrasonic pages 10-11, wrobel2026enhancingniobiumpowder pages 7-10)

## Marine qualification and novelty boundaries

**Do not equate a chloride polarization result with 30-day seawater durability.** Two nearby, but different, additive benchmarks show why the proposed comparison should hold electrolyte, conditioning, surface finish and test duration constant:

* **L. Zhao, K. Li, J. Yao, Y. Yuan and B. Du, “The Laser Deposited Nickel-Aluminum Bronze Coatings on SUS630 Stainless Steel and Its Corrosion Resistance in 3.5 wt.% NaCl Solution,” *Metals* 12 (2022) 781, DOI: 10.3390/met12050781.** **Process:** blown-powder laser deposition of **Cu–10.8Al–4.1Ni–4.0Fe wt% NAB** onto **SUS630 steel**, directly or over Ni–Al/Ni–Cr intermediate layers—not single-stream NAB-on-NAB repair. **Tests:** polished surfaces, **3.5 wt% NaCl**, approximately **25 °C**, 20 min before polarization; immersion to **21 days**. Direct/Ni–Al/Ni–Cr configurations gave \(i_{corr}=\)**7.82/4.65/4.09 µA cm⁻²**, \(E_{corr}=\)**−248/−255/−252 mV versus Ag/AgCl**, and maximum reported attack depths **3.4/2.0/1.8 µm**, respectively. As-deposited NAB tensile strength/elongation were **669 MPa/17.46%**; Fe-rich dilution in the direct steel build favored selective attack. No C71500-in-identical-seawater comparison. [CITE] [NUMBERS] [NOVELTY-RISK: laser-deposited NAB corrosion is prior art; substrate and intermediate-layer strategy differ] [GAP] (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 2-4, zhao2022thelaserdeposited pages 4-7)
* **R. Huo *et al.*, “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing,” *Materials* 18 (2025) 2205, DOI: 10.3390/ma18102205.** **Process:** **wire-arc DED/CMT**, not powder-laser DED; wire **Cu–8.73Al–5.9Fe–4.52Ni–1.39Mn wt%** on a Cu–Al substrate. **Test:** as-deposited, polished, aerated **3.5 wt% NaCl**, **25 ± 5 °C**, **1 h** OCP stabilization; not 30-day seawater. Heat input **243.8→644.7 J mm⁻¹** coincided with \(i_{corr}=\)**2.56→7.52 µA cm⁻²** and measured surface hardness **192.4→166.9 HV**; intermediate currents were **3.85 and 5.03 µA cm⁻²**. This supports controlling thermal-history-dependent κ/γ₂ distributions, but cannot establish a laser-DED powder optimum. [CITE] [NUMBERS] [NOVELTY-RISK: as-deposited NAB corrosion/process-property link already studied] [GAP] (huo2025modulatingheatinput pages 2-4, huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 4-5)
* **L. Wu *et al.*, “Erosion–Corrosion Behavior of 90/10 and 70/30 Copper–Nickel Tubes in 1 wt% NaCl Solution,” *Metals* 13 (2023) 401, DOI: 10.3390/met13020401.** **Process:** **wrought/annealed tubing**, not AM. Actual 90–10 composition **Ni 10.72, Fe 1.68, Mn 0.76 wt%, Cu balance**; 70–30 **Ni 30.4, Fe 0.75, Mn 0.88 wt%, Cu balance**. **Test:** **10 days**, flowing **1 wt% NaCl** (not ASTM D1141 or natural seawater) at **0.5–4.7 m s⁻¹**. Reported critical-flow range: **3–4 m s⁻¹** for 90–10 versus **>4.7 m s⁻¹** for 70–30. This is a useful **flow-dependent reference**, not an interchangeable corrosion-rate threshold for a static immersion test. [CITE] [NUMBERS] [NAVY: marine Cu–Ni service relevance] (wu2023erosion–corrosionbehaviorof pages 2-4, wu2023erosion–corrosionbehaviorof pages 18-19)

A 2011 **Cu–30Ni direct-metal-deposition** study by Bhattacharya and colleagues (DOI: **10.1016/j.jallcom.2011.03.091**) and the 2023 **ultrasonic-bronze-to-laser-DED** report by Müller and colleagues (DOI: **10.1088/1757-899x/1296/1/012036**) are particularly important **novelty checks**, but their full experimental results were not accessible here; assigning them corrosion or density numbers would be speculative. Likewise, the accessible sources do **not** establish an as-deposited, single-feed Cu–Ni/NAB powder-laser DED repair on **both cast NAB and wrought C71500**, tested head-to-head against wrought C71500 in the **same** specified seawater, flow and exposure duration. [NOVELTY-RISK] [GAP] (uhlmann2024acomparativeevaluation pages 2-4, nemani2024advancementsinadditive pages 41-43, zhao2022thelaserdeposited pages 7-10)

## Ranked: Top 5 things the PI should know

1. **The most direct manufacturing precedent is already NAB at 1300 °C/40 kHz, with 190 ppm O and 48/98/174 µm powder—but carbon fibers in the product.** Differentiate by alloy design, controlled contamination, single-feed DED repair and seawater performance rather than claiming first ultrasonic NAB powder. (uhlmann2024acomparativeevaluation pages 4-6, uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 6-7)
2. **A 62 °C *furnace* margin for 70–30 Cu–Ni is not a measured *plate-film* margin.** Qualify continuous flow and freezing empirically before treating Cu–30Ni as an assured in-house powder. (uhlmann2024acomparativeevaluation pages 4-6, scientific2023comparisonofultrasonic pages 2-4, wisutmethangoon2011productionofsac305 pages 2-3)
3. **Lang is a first-pass \(f^{-2/3}\) design prior, not a guaranteed DED-fraction yield or \(D_{50}\).** Compare unsieved and classified PSD and mass balance for each alloy and plate setting; use liquid, oxygen-aware properties. (scientific2023comparisonofultrasonic pages 4-5, scientific2023comparisonofultrasonic pages 5-7, wisutmethangoon2011productionofsac305 pages 3-6, egry2005thermophysicalpropertiesof pages 2-3)
4. **Do not choose Ti–6Al–4V for Cu contact merely because it works for other atomizers.** Ti–Cu wets/reacts; carbon fiber demonstrably sheds; TZM, Nb and ceramic/coated candidates need copper-specific lifetime and contamination tests. (li2004activejoiningof pages 1-3, li2004activejoiningof pages 3-6, uhlmann2024acomparativeevaluation pages 10-12, ciftcli2025alloydevelopmentfrom pages 1-3, sangiorgi1988wettabilityofhotpressed pages 1-2)
5. **The seawater claim needs a matched C71500 control and long-term, localized-attack readout.** Publish the as-deposited deposit *and repair interface* results alongside the identical wrought control; record flow, solution chemistry, exposure time and preparation because published AM chloride tests and wrought flowing-tube tests are not directly comparable. (zhao2022thelaserdeposited pages 7-10, wu2023erosion–corrosionbehaviorof pages 2-4, huo2025modulatingheatinput pages 10-13)

References

1. (uhlmann2024acomparativeevaluation pages 4-6): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

2. (uhlmann2024acomparativeevaluation pages 10-12): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

3. (uhlmann2024acomparativeevaluation pages 6-7): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

4. (scientific2023comparisonofultrasonic pages 4-5): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

5. (scientific2023comparisonofultrasonic pages 5-7): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

6. (wisutmethangoon2011productionofsac305 pages 3-6): Sirikul Wisutmethangoon, Thawatchai Plookphol, and Phairote Sungkhaphaitoon. Production of sac305 powder by ultrasonic atomization. Powder Technology, 209:105-111, May 2011. URL: https://doi.org/10.1016/j.powtec.2011.02.016, doi:10.1016/j.powtec.2011.02.016. This article has 41 citations and is from a domain leading peer-reviewed journal.

7. (wisutmethangoon2011productionofsac305 pages 1-2): Sirikul Wisutmethangoon, Thawatchai Plookphol, and Phairote Sungkhaphaitoon. Production of sac305 powder by ultrasonic atomization. Powder Technology, 209:105-111, May 2011. URL: https://doi.org/10.1016/j.powtec.2011.02.016, doi:10.1016/j.powtec.2011.02.016. This article has 41 citations and is from a domain leading peer-reviewed journal.

8. (wisutmethangoon2011productionofsac305 pages 2-3): Sirikul Wisutmethangoon, Thawatchai Plookphol, and Phairote Sungkhaphaitoon. Production of sac305 powder by ultrasonic atomization. Powder Technology, 209:105-111, May 2011. URL: https://doi.org/10.1016/j.powtec.2011.02.016, doi:10.1016/j.powtec.2011.02.016. This article has 41 citations and is from a domain leading peer-reviewed journal.

9. (sangiorgi1988wettabilityofhotpressed pages 2-4): R. Sangiorgi, M. L. Muolo, and A. Bellosi. Wettability of hot-pressed silicon nitride materials by liquid copper. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 103:277-283, Sep 1988. URL: https://doi.org/10.1016/0025-5416(88)90518-6, doi:10.1016/0025-5416(88)90518-6. This article has 20 citations.

10. (morita2006surfacetensionof pages 1-3): Z. Morita and A. Kasama. Surface tension of liquid copper in dilute oxygen concentrations. Journal of The Japan Institute of Metals, 40:787-795, 2006. URL: https://doi.org/10.2320/jinstmet1952.40.8\_787, doi:10.2320/jinstmet1952.40.8\_787. This article has 23 citations and is from a peer-reviewed journal.

11. (sangiorgi1988wettabilityofhotpressed pages 4-6): R. Sangiorgi, M. L. Muolo, and A. Bellosi. Wettability of hot-pressed silicon nitride materials by liquid copper. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 103:277-283, Sep 1988. URL: https://doi.org/10.1016/0025-5416(88)90518-6, doi:10.1016/0025-5416(88)90518-6. This article has 20 citations.

12. (egry2005thermophysicalpropertiesof pages 2-3): Ivan Egry, Jürgen Brillo, and Taishi Matsushita. Thermophysical properties of liquid cu-fe-ni alloys. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 413:460-464, Dec 2005. URL: https://doi.org/10.1016/j.msea.2005.09.007, doi:10.1016/j.msea.2005.09.007. This article has 33 citations.

13. (egry2005thermophysicalpropertiesof pages 1-2): Ivan Egry, Jürgen Brillo, and Taishi Matsushita. Thermophysical properties of liquid cu-fe-ni alloys. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 413:460-464, Dec 2005. URL: https://doi.org/10.1016/j.msea.2005.09.007, doi:10.1016/j.msea.2005.09.007. This article has 33 citations.

14. (egry2005thermophysicalpropertiesof pages 3-5): Ivan Egry, Jürgen Brillo, and Taishi Matsushita. Thermophysical properties of liquid cu-fe-ni alloys. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 413:460-464, Dec 2005. URL: https://doi.org/10.1016/j.msea.2005.09.007, doi:10.1016/j.msea.2005.09.007. This article has 33 citations.

15. (scientific2023comparisonofultrasonic pages 2-4): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

16. (li2004activejoiningof pages 1-3): J.H Li and R.Y Lin. Active joining of ti–6al–4v with electroplated cu thin film. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 381:39-50, Sep 2004. URL: https://doi.org/10.1016/j.msea.2004.03.028, doi:10.1016/j.msea.2004.03.028. This article has 12 citations.

17. (li2004activejoiningof pages 3-6): J.H Li and R.Y Lin. Active joining of ti–6al–4v with electroplated cu thin film. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 381:39-50, Sep 2004. URL: https://doi.org/10.1016/j.msea.2004.03.028, doi:10.1016/j.msea.2004.03.028. This article has 12 citations.

18. (ciftcli2025alloydevelopmentfrom pages 1-3): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72(Supplement):S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

19. (sangiorgi1988wettabilityofhotpressed pages 1-2): R. Sangiorgi, M. L. Muolo, and A. Bellosi. Wettability of hot-pressed silicon nitride materials by liquid copper. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 103:277-283, Sep 1988. URL: https://doi.org/10.1016/0025-5416(88)90518-6, doi:10.1016/0025-5416(88)90518-6. This article has 20 citations.

20. (scientific2023comparisonofultrasonic pages 10-11): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

21. (scientific2023comparisonofultrasonic pages 8-10): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

22. (uhlmann2024acomparativeevaluation pages 2-4): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

23. (uhlmann2024acomparativeevaluation pages 7-10): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

24. (uhlmann2024acomparativeevaluation pages 12-13): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

25. (ciftcli2025alloydevelopmentfrom pages 3-6): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72(Supplement):S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

26. (scientific2023comparisonofultrasonic pages 7-8): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

27. (scientific2023comparisonofultrasonic pages 11-13): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 38 citations.

28. (wrobel2026enhancingniobiumpowder pages 2-5): Sebastian Wróbel, Paweł Ostachowski, Krzysztof Żaba, Piotr Maj, Ilona Różycka, and Paweł Wesołowski. Enhancing niobium powder quality for additive manufacturing through ultrasonic atomization and calibrated rolling. The International Journal of Advanced Manufacturing Technology, 145:4097-4111, Jun 2026. URL: https://doi.org/10.1007/s00170-026-18599-0, doi:10.1007/s00170-026-18599-0. This article has 0 citations.

29. (wrobel2026enhancingniobiumpowder pages 5-7): Sebastian Wróbel, Paweł Ostachowski, Krzysztof Żaba, Piotr Maj, Ilona Różycka, and Paweł Wesołowski. Enhancing niobium powder quality for additive manufacturing through ultrasonic atomization and calibrated rolling. The International Journal of Advanced Manufacturing Technology, 145:4097-4111, Jun 2026. URL: https://doi.org/10.1007/s00170-026-18599-0, doi:10.1007/s00170-026-18599-0. This article has 0 citations.

30. (wrobel2026enhancingniobiumpowder pages 7-10): Sebastian Wróbel, Paweł Ostachowski, Krzysztof Żaba, Piotr Maj, Ilona Różycka, and Paweł Wesołowski. Enhancing niobium powder quality for additive manufacturing through ultrasonic atomization and calibrated rolling. The International Journal of Advanced Manufacturing Technology, 145:4097-4111, Jun 2026. URL: https://doi.org/10.1007/s00170-026-18599-0, doi:10.1007/s00170-026-18599-0. This article has 0 citations.

31. (kustron2023developmentofhighpower pages 2-4): Pawel Kustron, Marcin Korzeniowski, Adam Sajbura, Tomasz Piwowarczyk, Pawel Kaczynski, and Pawel Sokolowski. Development of high-power ultrasonic system dedicated to metal powder atomization. Applied Sciences, 13:8984, Aug 2023. URL: https://doi.org/10.3390/app13158984, doi:10.3390/app13158984. This article has 44 citations.

32. (zhao2022thelaserdeposited pages 7-10): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

33. (zhao2022thelaserdeposited pages 2-4): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

34. (zhao2022thelaserdeposited pages 4-7): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

35. (huo2025modulatingheatinput pages 2-4): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

36. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

37. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

38. (wu2023erosion–corrosionbehaviorof pages 2-4): Lei Wu, Aili Ma, Lianmin Zhang, Guangming Li, Lingyue Hu, Zhengbin Wang, and Yugui Zheng. Erosion–corrosion behavior of 90/10 and 70/30 copper–nickel tubes in 1 wt% nacl solution. Metals, 13:401, Feb 2023. URL: https://doi.org/10.3390/met13020401, doi:10.3390/met13020401. This article has 42 citations.

39. (wu2023erosion–corrosionbehaviorof pages 18-19): Lei Wu, Aili Ma, Lianmin Zhang, Guangming Li, Lingyue Hu, Zhengbin Wang, and Yugui Zheng. Erosion–corrosion behavior of 90/10 and 70/30 copper–nickel tubes in 1 wt% nacl solution. Metals, 13:401, Feb 2023. URL: https://doi.org/10.3390/met13020401, doi:10.3390/met13020401. This article has 42 citations.

40. (nemani2024advancementsinadditive pages 41-43): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.
