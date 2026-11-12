<!--
Edison Scientific LITERATURE task (batch 4)
- Task ID: fd7064b9-a644-42dc-9196-47550bffdeb8
- Submitted: 2026-10-17T06:11:13Z
- Fetched: 2026-10-17T06:41:54Z (status: success)
- Raw trajectory JSON: ../raw/b4-06-accelerated-corrosion-screening.json.gz
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

QUESTION: What accelerated or high-throughput corrosion screening methods
have been used for copper alloys in seawater or chloride, and how well do
they predict longer tests? Cover scanning droplet cells and combinatorial
electrochemistry, multi-electrode arrays, electrochemical noise, zero-
resistance-ammeter galvanic tests, accelerated pre-filming of Cu-Ni (e.g.
ferrous sulfate dosing, controlled clean-seawater prefilming), jet
impingement and rotating cylinder electrodes, and autonomous or robotic
corrosion testing. Give timescales, throughput, and any reported rank
correlation with 30-day or longer immersion for Cu-Ni or NAB.

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

QUESTION: What accelerated or high-throughput corrosion screening methods
have been used for copper alloys in seawater or chloride, and how well do
they predict longer tests? Cover scanning droplet cells and combinatorial
electrochemistry, multi-electrode arrays, electrochemical noise, zero-
resistance-ammeter galvanic tests, accelerated pre-filming of Cu-Ni (e.g.
ferrous sulfate dosing, controlled clean-seawater prefilming), jet
impingement and rotating cylinder electrodes, and autonomous or robotic
corrosion testing. Give timescales, throughput, and any reported rank
correlation with 30-day or longer immersion for Cu-Ni or NAB.

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


# Accelerated corrosion screening for marine Cu–Ni and nickel-aluminum bronze

**Bottom line.** Short electrochemical measurements, electrochemical noise, galvanic-current measurements, and five-hour erosion–corrosion tests have all been applied to relevant copper alloys. They are useful for *triage*, but the retrieved literature does **not** establish a numerical Spearman or Kendall rank correlation between any of these screens and ≥30-day mass loss or selective-attack depth across a set of Cu–Ni or nickel-aluminum bronze (NAB) compositions. A study that measures electrochemistry at seven days and photographs specimens at 30 days is not such a validation. None of the studies below tests the proposed single-stream, pre-alloyed-powder, blown-powder laser DED → as-deposited seawater-performance workflow. (qian2025corrosivestudyof pages 2-3, takaloo2011corrosionbehaviorof pages 3-5, qian2025corrosivestudyof pages 7-10)

The matrix distinguishes measured short-test performance from evidence that it predicts longer exposure:

| Screen | Specimen / process | Documented conditions and timescale | Observed quantitative benchmark | ≥30-day prediction evidence |
|---|---|---|---|---|
| Autonomous scanning droplet cell (SDC) | Electrodeposited/composition-spread **Al–Ni–Ti**, not Cu–Ni or NAB; approximately 4.5 mm cell footprint | Neutral NaCl; automated LSV analyzed for passivation current and plateau slope; Gaussian-process multiobjective search | Convergence toward both objectives in **fewer than 10 simulated active-learning queries**; this was retrospective simulation using an existing dataset, not demonstrated Cu-alloy throughput | **None:** no ≥30-day immersion validation or measured rank correlation; relevance is platform architecture only (decost2022towardsautomateddesign pages 4-7, decost2022towardsautomateddesign pages 1-4, decost2022towardsautomateddesign pages 7-10) |
| Flow-loop EIS and polarization | Annealed wrought tubes: Cu–10.72Ni–1.68Fe–0.76Mn and Cu–30.4Ni–0.75Fe–0.88Mn, wt% | **1 wt% NaCl**, 10 days, 0.5–4.7 m/s; EIS from 100 kHz to 10 mHz at ±10 mV; terminal polarization from −0.5 to +1.2 V versus OCP | Best film resistance at **1.5 m/s** for 90/10 and **0.5 m/s** for 70/30; critical velocities **3–4 m/s** and **greater than 4.7 m/s**, respectively; 70/30 film phase angle 60–80° versus 40–60° for 90/10 | **None:** no ≥30-day endpoint and no rank correlation with long immersion (wu2023erosion–corrosionbehaviorof pages 2-4, wu2023erosion–corrosionbehaviorof pages 4-7) |
| Static EIS, polarization, and Cu–Ni/Cu–Ni galvanic current | Wrought B10: Cu–11.266Ni–1.751Fe–0.725Mn; B30: Cu–30.050Ni–0.726Fe–0.718Mn, wt% | ASTM-D1141-like artificial seawater, pH approximately 8, 25 °C, renewed every 12 h; EIS/polarization through **7 days**; 1:1 coupled tubes observed through **30 days** | At 7 days, charge-transfer resistance was approximately **5.40 kΩ·cm²** for B10 and **10.05 kΩ·cm²** for B30; coupled current stabilized after 27 h at **−3.90 µA**, approximately −0.927 µA/cm²; 30-day morphology showed products and surface roughening | **Weak within-study bridge only:** 7-day electrochemistry and 30-day qualitative morphology used the same alloys, but there was no quantitative 30-day mass-loss or attack-depth endpoint and **no measured rank correlation** (qian2025corrosivestudyof pages 3-6, qian2025corrosivestudyof pages 2-3, qian2025corrosivestudyof pages 6-7, qian2025corrosivestudyof pages 7-10) |
| Electrochemical noise and ZRA | Cast C95520 NAB: Cu balance–11.54Al–4.47Fe–4.60Ni wt%; heat-treated variants | ASTM D1141-98 artificial seawater, pH 8.26, dissolved oxygen approximately 7 ppm, 27 °C; ZRA at **11, 20, 40, 50, and 75 days**, with records lasting 1,400–6,000 s | NAB normalized at 675 °C had the highest reported potential, **−123.4631 mV**, and lowest reported 75-day current, approximately **3.1348 µA**; normalized material showed fewer pits and its corrosion rate decreased approximately 19% | **Direct ≥30-day observations**, but not a prospective short-test validation: no reported Spearman or Kendall correlation between early ZRA/noise and 40–75-day damage (takaloo2011corrosionbehaviorof pages 2-3, takaloo2011corrosionbehaviorof pages 3-5, takaloo2011corrosionbehaviorof pages 9-12, takaloo2011corrosionbehaviorof pages 12-13) |
| Jet impingement plus ECN | Cast NAB: Cu–9Al–5Ni–4.5Fe–1.10Mn; HVOF NAB coating: Cu–8.71Al–5.55Ni–4.50Fe–1.02Cr–0.15Mo wt% | **3.5 wt% NaCl**, 25 °C, 5 h; 3.1–6.0 m/s, 90° jet; optional 3 wt% silica; ECN sampled at 2 Hz during hours 3–4 | Flow-corrosion rate **0.5–0.8 mm/y** for cast NAB and **0.8–1.5 mm/y** for HVOF NAB; at 5 m/s and 0.23 J, erosion–corrosion mass loss was **12.1 mg** cast versus **18.3 mg** HVOF; the ECN–mass-loss relationship was material-dependent and uncorrelated for cast NAB under erosion–corrosion | **None:** the five-hour acceleration was not validated against ≥30-day immersion; no rank correlation. The work involved Dstl and naval-platform applications (barik2005erosionanderosion–corrosion pages 3-6, barik2005erosionanderosion–corrosion pages 8-11, barik2005erosionanderosion–corrosion pages 1-2, barik2005erosionanderosion–corrosion pages 6-7) |
| Galvanic-current test | Cast ZCuAl10Fe5Ni5: Cu balance–10.45Al–5.44Fe–4.69Ni–0.49Zn wt%, coupled to SAF2507 | ASTM D1141-98 substitute seawater; area ratios 1:1 and 1:50; repeated 10-minute current measurements through **360 h, or 15 days** | At a 1:50 bronze-to-steel area ratio, bronze-anode current density was **approximately 38 µA/cm² initially**, approximately 2 µA/cm² at 72 h, and approximately 4 µA/cm² at 360 h; current was near zero at 1:1 | **None:** only 15 days; no ≥30-day corrosion-depth or mass-loss validation and no rank correlation (luo2026thegalvaniccorrosion pages 3-4, luo2026thegalvaniccorrosion pages 4-6, luo2026thegalvaniccorrosion pages 9-11) |
| Controlled clean-seawater prefilming and long exposure | Wrought C70600-type 90/10 Cu–Ni; typical Cu–9–11Ni–1–2Fe–0.5–1Mn wt% | Clean-seawater commissioning: initial film in days, **2–3 months** to mature at 15–17 °C, and faster near 27 °C; Langstone Harbour exposure for **7 years** | Seven-year foil thinning averaged **5.5 µm/y** and decreased with time; earlier long-term data stabilized below **2 µm/y** | Demonstrates why hours-to-days tests may not predict mature performance; no paired early-screen/long-test rank correlation (powell2004corrosionandbiofouling pages 1-4, schleich2004typicalfailuresof pages 3-6, powell2004corrosionandbiofouling pages 9-10) |
| Ferrous-sulfate-assisted prefilming | Primarily wrought 90/10 Cu–Ni marine tubing | Used as a remedial or precautionary ferrous-ion treatment in polluted or corrosive seawater; should not coincide with chlorination | Reported to suppress corrosion, but the retrieved source gives **no controlled dose–time–response numbers**; most ship systems operate without dosing | **No validated rank correlation** and no retrieved controlled comparison with ≥30-day immersion; clean-seawater prefilming has stronger quantitative time evidence (powell2004corrosionandbiofouling pages 4-6) |
| Multi-electrode or wire-beam arrays | No directly verified Cu–Ni or NAB seawater composition-screening study retrieved | Applicable to spatial current mapping and localized-corrosion detection, but not demonstrated here as a high-throughput alloy-ranking workflow | No defensible Cu–Ni/NAB throughput, corrosion-rate, or attack-depth benchmark found | **Evidence gap:** no reported rank correlation with 30-day-or-longer Cu–Ni or NAB immersion |
| Robotic corrosion testing beyond SDC | No directly verified robotic Cu–Ni or NAB seawater campaign retrieved | Autonomous electrochemical platforms exist for other alloy systems, but translation from thin-film/local-cell results to bulk DED deposits remains unvalidated | No defensible samples-per-day figure for Cu–Ni or NAB corrosion screening found | **Evidence gap:** no ≥30-day validation or rank correlation for Cu–Ni/NAB, DED deposits, or repair interfaces |


*Table: Comparison of accelerated and high-throughput corrosion screens relevant to Cu–Ni and nickel-aluminum bronze, including conditions, quantitative benchmarks, and long-test validation. The matrix distinguishes direct evidence from unvalidated extrapolation and identifies the absence of reported rank correlations.*

## Evidence by method

**1. Scanning droplet cells, combinatorial electrochemistry, and robotics — [CITE] [NOVELTY-RISK] [GAP].** Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers, “Towards Automated Design of Corrosion Resistant Alloy Coatings with an Autonomous Scanning Droplet Cell,” *JOM* **74** (2022), 2941–2950, DOI **10.1007/s11837-022-05367-0**. **Process/alloys:** electrodeposited coatings and composition-spread thin films, **not DED**; illustrative systems are Al–Ni–Ti and Ti–Nb–Ta, with composition-dependent wt% not reported in the retrieved discussion. An automated flow cell addresses an approximately **4.5-mm-diameter** spot and acquires localized voltammetry; the Al–Ni–Ti benchmark uses **neutral NaCl**, although its concentration and individual-test duration are not specified in the available text. Gaussian-process optimization approached the measured passivation-current/passivation-slope trade-off in **fewer than ten *simulated* active-learning queries** on an existing dataset. This is prior art for *autonomous corrosion-oriented alloy optimization*, but neither ten completed robotic experiments, a samples/day throughput, nor long-immersion predictive validity for Cu–Ni or NAB is demonstrated. No relevant DED density, powder-quality, hardness, or seawater-attack data are reported. The proposed novelty must therefore be the physically linked **powder → bulk DED → corrosion** workflow and its prospective validation, not the general idea of robotic electrochemistry plus Bayesian optimization. (decost2022towardsautomateddesign pages 4-7, decost2022towardsautomateddesign pages 1-4, decost2022towardsautomateddesign pages 7-10)

**2. Repeated electrochemistry under controlled flow — [CITE] [NUMBERS] [GAP].** Lei Wu, Aili Ma, Lianmin Zhang, Guangming Li, Lingyue Hu, Zhengbin Wang, and Yugui Zheng, “Erosion–Corrosion Behavior of 90/10 and 70/30 Copper–Nickel Tubes in 1 wt% NaCl Solution,” *Metals* **13** (2023), 401, DOI **10.3390/met13020401**. **Process:** annealed, wrought Cu–Ni tubes, not deposited material. **Measured composition, wt%:** 90/10, Cu balance–10.72Ni–1.68Fe–0.76Mn; 70/30, Cu balance–30.4Ni–0.75Fe–0.88Mn. **Conditions:** **1 wt% NaCl**, explicitly a brackish-water surrogate rather than ASTM D1141 seawater; **10 days** in a flow loop at **0.5, 1.5, 3, 4, or 4.7 m/s**. In situ EIS spans **100 kHz–10 mHz**, ±10 mV about OCP; polarization follows the final EIS measurement. Film resistance rises particularly rapidly during the first **12 h**. Best measured film resistance occurs at **1.5 m/s** for 90/10 and **0.5 m/s** for 70/30; reported critical film-disruption velocity is **3–4 m/s** for 90/10 and **above 4.7 m/s** for 70/30. EIS phase-angle ranges are **40–60°** and **60–80°**, respectively. These are flow/film benchmarks, **not** a demonstrated ten-day-to-30-day ranking calibration. A rotating-cylinder or impinging-jet screen may be faster, but the authors argue that their flow loop better approximates tube hydrodynamics; no samples/day throughput is reported. (wu2023erosion–corrosionbehaviorof pages 2-4, wu2023erosion–corrosionbehaviorof pages 4-7)

**3. Cu–Ni galvanic current, EIS, and a 30-day observation — [CITE] [NUMBERS] [NAVY] [GAP].** Feng Qian, Xvhui Liu, Rui Cui, Kai Wang, Chao Wang, Xiong Bao, Dongsheng Dong, Mengni Zhou, Zunhua Zhang, Xiaofeng Guo, and Jie Wang, “Corrosive study of B10/B30 copper-nickel alloys coupled pipeline in static seawater,” *Advanced Composites and Hybrid Materials* **8** (2025), article 113, DOI **10.1007/s42114-024-01174-0**. **Process:** wrought tubular ship-seawater-system alloys. **Measured wt%:** B10, Cu balance–11.266Ni–1.751Fe–0.725Mn; B30, Cu balance–30.050Ni–0.726Fe–0.718Mn, with minor reported constituents. **Conditions:** laboratory artificial seawater containing **24.53 g/L NaCl plus MgCl₂, sulfate and other salts**, approximately **pH 8 and 25 °C**; static medium replaced every **12 h**; a **1:1** tube couple. EIS and polarization were reported at **3 h, 1, 3, 5 and 7 days**; coupled-specimen appearance was documented through **30 days**. Fitted **7-day charge-transfer resistances** were **5,401.6 Ω·cm²** for B10 and **10,050.6 Ω·cm²** for B30. Coupling current settled around **−3.90 μA** after **27 h**, reported as approximately **−0.927 μA/cm²**. B10 generally acts as the anodic partner, although the paper’s narrative also mentions a transient polarity reversal; that inconsistency warrants care. The 30-day evidence is **qualitative morphology**, not paired 30-day mass loss or maximum attack depth. Its ship-piping application merits [NAVY], but **Navy/DoD funding is not established**. (qian2025corrosivestudyof pages 3-6, qian2025corrosivestudyof pages 2-3, qian2025corrosivestudyof pages 6-7, qian2025corrosivestudyof pages 7-10, qian2025corrosivestudyof pages 10-11)

**4. Electrochemical noise and zero-resistance-ammeter measurements with long immersion — [CITE] [NUMBERS] [GAP].** Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar, “Corrosion Behavior of Heat Treated Nickel-Aluminum Bronze Alloy in Artificial Seawater,” *Materials Sciences and Applications* **2** (2011), 1542–1555, DOI **10.4236/msa.2011.211207**. **Process:** cast ASTM B148 C95520 NAB, subsequently **heat treated**—therefore not evidence for an *as-deposited* outcome. **Measured wt%:** Cu balance–11.54Al–4.47Fe–4.60Ni; Mn **0.001**. **Conditions:** ASTM **D1141-98** artificial seawater, **pH 8.26**, dissolved O₂ approximately **7 ppm**, **27 °C**; electrochemical noise measured between equal-area, similarly treated specimens with a ZRA after **11, 20, 40, 50 and 75 days** immersion. Record lengths were **1,400–6,000 s** at those respective visits. Specimen normalized at **675 °C** had the lowest reported **75-day ZRA current, approximately 3.1348 μA**, versus **6.148 μA** for the untreated reference; its quoted potential was approximately **−123.4631 mV**. These are **couple/noise readings, not Tafel-derived corrosion current densities or an assured common-reference E_corr**. The normalized condition also showed fewer pits and favorable EIS/polarization, furnishing a *qualitative* short-/long-response agreement, but **no calculated early-versus-75-day rank statistic or measured maximum selective-attack depth**. The casting’s reported hardness is **162 HV** and tensile strength approximately **630 MPa**. The PDF’s actual bibliographic header is *Materials Sciences and Applications* **2**, 1542–1555, rather than the inconsistent database journal/page metadata. (takaloo2011corrosionbehaviorof pages 1-2, takaloo2011corrosionbehaviorof pages 2-3, takaloo2011corrosionbehaviorof pages 3-5, takaloo2011corrosionbehaviorof pages 9-12, takaloo2011corrosionbehaviorof pages 12-13)

**5. Jet impingement and current noise — [CITE] [NUMBERS] [NAVY] [GAP].** R. C. Barik, J. A. Wharton, R. J. K. Wood, K. S. Tan, and K. R. Stokes, “Erosion and erosion–corrosion performance of cast and thermally sprayed nickel–aluminium bronze,” *Wear* **259** (2005), 230–242, DOI **10.1016/j.wear.2005.02.033**. **Process:** cast NAB versus **HVOF thermal-sprayed** NAB coating—not laser cladding or blown-powder DED. **Wt%:** cast Cu balance–9Al–5Ni–4.5Fe–1.10Mn; sprayed coating Cu balance–8.71Al–5.55Ni–4.50Fe–1.02Cr–0.15Mo. **Conditions:** **3.5 wt% NaCl**, approximately **25 °C**, **five-hour** 90° jet tests over approximately **3.1–6 m/s**, with either no sand or **3 wt% silica**; electrochemical *current* noise sampled at **2 Hz** during hours **3–4**. At roughly **5 m/s** and **0.23 μJ** reported particle kinetic energy, five-hour slurry erosion–corrosion losses were **12.1 mg cast** versus **18.3 mg HVOF**. The sprayed coating had approximately **1% porosity** and **290 HV**, versus **235 HV** for cast NAB; those are *HVOF* properties, not DED density or hardness. Five-hour flow-corrosion rates extrapolated to annual units were **0.5–0.8 mm/year cast** and **0.8–1.5 mm/year sprayed**: do **not** interpret these accelerated, short-exposure rates as measured year-long immersion rates. Importantly, noise standard deviation tracked erosion–corrosion loss for the sprayed coating but was described as **uncorrelated for cast NAB** under slurry impingement. One coauthor was at UK **Dstl**, and the paper explicitly addresses naval propulsion and seawater systems; this is defensible [NAVY], not evidence of ONR funding. No ≥30-day ranking validation was performed. (barik2005erosionanderosion–corrosion pages 3-6, barik2005erosionanderosion–corrosion pages 2-3, barik2005erosionanderosion–corrosion pages 8-11, barik2005erosionanderosion–corrosion pages 1-2, barik2005erosionanderosion–corrosion pages 6-7)

**6. Short galvanic tests must preserve area ratio — [CITE] [NUMBERS] [GAP].** Kun Luo, Pu Zhao, Ke-Wei Fang, Wan-Xiang Zhao, Jiachang Lu, Hong-Qun Liu, Shui-Yong Wang, Mengmeng Zhu, and Y.-X. Qiao, “The Galvanic Corrosion Behavior of ZCuAl10Fe5Ni5 Coupled with SAF2507 Duplex Stainless Steel in Seawater,” *Metals* **16** (2026), 473, DOI **10.3390/met16050473**. **Process:** cast aluminum bronze paired with wrought duplex steel; **not** a deposited NAB-on-NAB repair interface. **Measured bronze wt%:** Cu balance–10.45Al–5.44Fe–4.69Ni–0.49Zn. **Conditions:** ASTM **D1141-98** substitute seawater, repeated **10-minute** galvanic-current acquisitions during immersion to **360 h (15 days)**, with bronze:steel exposed-area ratios **1:1 and 1:50**. At **1:50**, bronze-anode current density was approximately **38 μA/cm² initially**, **2 μA/cm² at 72 h**, and **4 μA/cm² at 360 h**; at **1:1** it was close to zero. Bronze hardness averaged **222.3 HV**. This supports including **repair-interface galvanic-current measurements at realistic exposed-area ratios**, but provides neither ≥30-day prediction nor Cu–Ni/NAB repair-interface numbers. (luo2026thegalvaniccorrosion pages 3-4, luo2026thegalvaniccorrosion pages 4-6, luo2026thegalvaniccorrosion pages 9-11)

**7. Clean-seawater and ferrous-sulfate prefilming — [CITE] [NUMBERS] [NAVY] [GAP].** Carol Powell, “Corrosion and Biofouling Resistance Evaluation of 90-10 Copper-Nickel” (2004, Copper Development Association technical review; **DOI not identified**), and Wilhelm Schleich, “Typical Failures of CuNi 90/10 Seawater Tubing Systems and How to Avoid Them” (2004, technical review; **DOI not identified**). **Process:** conventionally produced/wrought **CuNi10Fe1Mn** marine tubing and sheet, not DED. Powell gives typical C70600 composition ranges, **wt% Cu balance–9–11Ni–1–2Fe–0.5–1Mn**. Initial protective film forms in days, but maturation in clean temperate seawater takes **approximately 2–3 months**; Schleich recommends up to **three months of continuous clean-seawater commissioning** and refreshment of intermittently stagnant seawater within **4–5 days**. Powell reports **seven-year** Langstone Harbour foil thinning averaging **5.5 μm/year** and earlier long-exposure rates stabilizing below **2 μm/year**. Powell’s earlier sentence prints “5.5 mm/year,” inconsistent with its own **5.5 μm/year conclusion**; the latter is the usable figure with this qualification. Ferrous-sulfate/ferrous-ion dosing is described as a corrosion-suppressing **remedy or precaution**, *not* a required treatment for successful ship service; it should **not be simultaneous with chlorination**. No verified dose–duration schedule, samples/day throughput, or quantitative comparison of dosed versus clean-prefilmed screens against 30-day alloy rankings was recovered. Critically, prefilming is a **test-history variable**, not a permissible post-build heat treatment, and should not silently replace the proposed as-deposited baseline. (powell2004corrosionandbiofouling pages 1-4, schleich2004typicalfailuresof pages 3-6, powell2004corrosionandbiofouling pages 4-6, powell2004corrosionandbiofouling pages 9-10)

**8. Multi-electrode arrays / wire-beam electrodes — [GAP].** These approaches spatially resolve local anodic and cathodic activity, making them conceptually useful for phase-selective attack or a repair boundary. However, a directly inspectable primary experiment providing **Cu–Ni or NAB alloy-composition screening throughput and a ≥30-day immersion rank correlation** was **not recovered**. Do not cite a steel wire-beam experiment as proof of Cu–Ni/NAB predictive accuracy, and do not assign an unsupported number of electrodes or samples/day. Likewise, none of the retrieved papers supplies powder size distribution, Hall flow, apparent powder density, powder oxygen, laser-DED deposit porosity, or strength/elongation *for an alloy screened by these methods*; those proposed process metrics cannot be taken from cast, wrought, HVOF, or electrodeposited specimens. (wu2023erosion–corrosionbehaviorof pages 2-4, decost2022towardsautomateddesign pages 1-4, barik2005erosionanderosion–corrosion pages 3-6)

## Top 5 things the PI should know

1. **Make predictive validation an explicit result, not an assumption:** measure blinded early-test rankings against **30-day-or-longer gravimetric loss *and* maximum local/selective-attack depth** on the *same* Cu–Ni, NAB, and C71500 specimens; report Spearman/Kendall correlations, uncertainty, and ranking reversals. None of the inspected Cu–Ni/NAB studies supplies that statistic. (takaloo2011corrosionbehaviorof pages 3-5, qian2025corrosivestudyof pages 7-10)
2. **Separate bare as-deposited from prefilmed performance.** A Cu–Ni film changes rapidly over hours yet may take **2–3 months** to mature; short polarization current or a five-hour jet rate is not automatically a service-life estimate. Include controlled clean-seawater exposure as an explicit covariate and ferrous-ion dosing as a separately labeled optional stress-test condition, not as evidence that an untreated deposit meets the goal. (powell2004corrosionandbiofouling pages 1-4, schleich2004typicalfailuresof pages 3-6, barik2005erosionanderosion–corrosion pages 6-7)
3. **Test the deposited repair couple, not merely its constituents.** Galvanic current can change dramatically with cathode:anode exposed-area ratio; capture both self-deposits and DED-on-cast-NAB/DED-on-wrought-Cu–Ni interfaces, with an area-ratio series and cross-sectional selective-attack measurements. (qian2025corrosivestudyof pages 2-3, luo2026thegalvaniccorrosion pages 9-11)
4. **Use hydrodynamic and localized-corrosion tests as complementary, not interchangeable, low-cost nodes.** Ten-day Cu–Ni loop tests identify different critical velocities for 90/10 and 70/30, while five-hour NAB jet/noise relationships depend on process and can fail even for cast NAB. Record electrolyte identity, oxygen, flow geometry, initial surface state, and film age in every model input. (wu2023erosion–corrosionbehaviorof pages 2-4, wu2023erosion–corrosionbehaviorof pages 4-7, barik2005erosionanderosion–corrosion pages 8-11)
5. **Claim novelty narrowly and defensibly.** Autonomous droplet-cell corrosion optimization already exists, and heat-treated cast NAB has already been studied by polarization/EIS/noise out to **75 days**. The defensible gap is a validated, cost-aware **composition → pre-alloyed powder → single-stream laser DED → as-deposited microstructure/repair interface → long-duration marine corrosion** model; none of the cited papers demonstrates that complete chain. (decost2022towardsautomateddesign pages 4-7, takaloo2011corrosionbehaviorof pages 3-5, decost2022towardsautomateddesign pages 7-10)

References

1. (qian2025corrosivestudyof pages 2-3): Feng Qian, Xvhui Liu, Rui Cui, Kai Wang, Chao Wang, Xiong Bao, Dongsheng Dong, Mengni Zhou, Zunhua Zhang, Xiaofeng Guo, and Jie Wang. Corrosive study of b10/b30 copper-nickel alloys coupled pipeline in static seawater. Advanced Composites and Hybrid Materials, Jan 2025. URL: https://doi.org/10.1007/s42114-024-01174-0, doi:10.1007/s42114-024-01174-0. This article has 12 citations and is from a peer-reviewed journal.

2. (takaloo2011corrosionbehaviorof pages 3-5): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 5 citations and is from a peer-reviewed journal.

3. (qian2025corrosivestudyof pages 7-10): Feng Qian, Xvhui Liu, Rui Cui, Kai Wang, Chao Wang, Xiong Bao, Dongsheng Dong, Mengni Zhou, Zunhua Zhang, Xiaofeng Guo, and Jie Wang. Corrosive study of b10/b30 copper-nickel alloys coupled pipeline in static seawater. Advanced Composites and Hybrid Materials, Jan 2025. URL: https://doi.org/10.1007/s42114-024-01174-0, doi:10.1007/s42114-024-01174-0. This article has 12 citations and is from a peer-reviewed journal.

4. (decost2022towardsautomateddesign pages 4-7): Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers. Towards automated design of corrosion resistant alloy coatings with an autonomous scanning droplet cell. JOM, 74:2941-2950, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05367-0, doi:10.1007/s11837-022-05367-0. This article has 29 citations and is from a peer-reviewed journal.

5. (decost2022towardsautomateddesign pages 1-4): Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers. Towards automated design of corrosion resistant alloy coatings with an autonomous scanning droplet cell. JOM, 74:2941-2950, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05367-0, doi:10.1007/s11837-022-05367-0. This article has 29 citations and is from a peer-reviewed journal.

6. (decost2022towardsautomateddesign pages 7-10): Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers. Towards automated design of corrosion resistant alloy coatings with an autonomous scanning droplet cell. JOM, 74:2941-2950, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05367-0, doi:10.1007/s11837-022-05367-0. This article has 29 citations and is from a peer-reviewed journal.

7. (wu2023erosion–corrosionbehaviorof pages 2-4): Lei Wu, Aili Ma, Lianmin Zhang, Guangming Li, Lingyue Hu, Zhengbin Wang, and Yugui Zheng. Erosion–corrosion behavior of 90/10 and 70/30 copper–nickel tubes in 1 wt% nacl solution. Metals, 13:401, Feb 2023. URL: https://doi.org/10.3390/met13020401, doi:10.3390/met13020401. This article has 42 citations.

8. (wu2023erosion–corrosionbehaviorof pages 4-7): Lei Wu, Aili Ma, Lianmin Zhang, Guangming Li, Lingyue Hu, Zhengbin Wang, and Yugui Zheng. Erosion–corrosion behavior of 90/10 and 70/30 copper–nickel tubes in 1 wt% nacl solution. Metals, 13:401, Feb 2023. URL: https://doi.org/10.3390/met13020401, doi:10.3390/met13020401. This article has 42 citations.

9. (qian2025corrosivestudyof pages 3-6): Feng Qian, Xvhui Liu, Rui Cui, Kai Wang, Chao Wang, Xiong Bao, Dongsheng Dong, Mengni Zhou, Zunhua Zhang, Xiaofeng Guo, and Jie Wang. Corrosive study of b10/b30 copper-nickel alloys coupled pipeline in static seawater. Advanced Composites and Hybrid Materials, Jan 2025. URL: https://doi.org/10.1007/s42114-024-01174-0, doi:10.1007/s42114-024-01174-0. This article has 12 citations and is from a peer-reviewed journal.

10. (qian2025corrosivestudyof pages 6-7): Feng Qian, Xvhui Liu, Rui Cui, Kai Wang, Chao Wang, Xiong Bao, Dongsheng Dong, Mengni Zhou, Zunhua Zhang, Xiaofeng Guo, and Jie Wang. Corrosive study of b10/b30 copper-nickel alloys coupled pipeline in static seawater. Advanced Composites and Hybrid Materials, Jan 2025. URL: https://doi.org/10.1007/s42114-024-01174-0, doi:10.1007/s42114-024-01174-0. This article has 12 citations and is from a peer-reviewed journal.

11. (takaloo2011corrosionbehaviorof pages 2-3): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 5 citations and is from a peer-reviewed journal.

12. (takaloo2011corrosionbehaviorof pages 9-12): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 5 citations and is from a peer-reviewed journal.

13. (takaloo2011corrosionbehaviorof pages 12-13): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 5 citations and is from a peer-reviewed journal.

14. (barik2005erosionanderosion–corrosion pages 3-6): R.C. Barik, J.A. Wharton, R.J.K. Wood, K.S. Tan, and K.R. Stokes. Erosion and erosion–corrosion performance of cast and thermally sprayed nickel–aluminium bronze. Wear, 259:230-242, Jul 2005. URL: https://doi.org/10.1016/j.wear.2005.02.033, doi:10.1016/j.wear.2005.02.033. This article has 178 citations and is from a highest quality peer-reviewed journal.

15. (barik2005erosionanderosion–corrosion pages 8-11): R.C. Barik, J.A. Wharton, R.J.K. Wood, K.S. Tan, and K.R. Stokes. Erosion and erosion–corrosion performance of cast and thermally sprayed nickel–aluminium bronze. Wear, 259:230-242, Jul 2005. URL: https://doi.org/10.1016/j.wear.2005.02.033, doi:10.1016/j.wear.2005.02.033. This article has 178 citations and is from a highest quality peer-reviewed journal.

16. (barik2005erosionanderosion–corrosion pages 1-2): R.C. Barik, J.A. Wharton, R.J.K. Wood, K.S. Tan, and K.R. Stokes. Erosion and erosion–corrosion performance of cast and thermally sprayed nickel–aluminium bronze. Wear, 259:230-242, Jul 2005. URL: https://doi.org/10.1016/j.wear.2005.02.033, doi:10.1016/j.wear.2005.02.033. This article has 178 citations and is from a highest quality peer-reviewed journal.

17. (barik2005erosionanderosion–corrosion pages 6-7): R.C. Barik, J.A. Wharton, R.J.K. Wood, K.S. Tan, and K.R. Stokes. Erosion and erosion–corrosion performance of cast and thermally sprayed nickel–aluminium bronze. Wear, 259:230-242, Jul 2005. URL: https://doi.org/10.1016/j.wear.2005.02.033, doi:10.1016/j.wear.2005.02.033. This article has 178 citations and is from a highest quality peer-reviewed journal.

18. (luo2026thegalvaniccorrosion pages 3-4): Kun Luo, Pu Zhao, Ke-Wei Fang, Wan-Xiang Zhao, Jiachang Lu, Hong-Qun Liu, Shui-Yong Wang, Mengmeng Zhu, and Y.-X. Qiao. The galvanic corrosion behavior of zcual10fe5ni5 coupled with saf2507 duplex stainless steel in seawater. Metals, 16:473, Apr 2026. URL: https://doi.org/10.3390/met16050473, doi:10.3390/met16050473. This article has 0 citations.

19. (luo2026thegalvaniccorrosion pages 4-6): Kun Luo, Pu Zhao, Ke-Wei Fang, Wan-Xiang Zhao, Jiachang Lu, Hong-Qun Liu, Shui-Yong Wang, Mengmeng Zhu, and Y.-X. Qiao. The galvanic corrosion behavior of zcual10fe5ni5 coupled with saf2507 duplex stainless steel in seawater. Metals, 16:473, Apr 2026. URL: https://doi.org/10.3390/met16050473, doi:10.3390/met16050473. This article has 0 citations.

20. (luo2026thegalvaniccorrosion pages 9-11): Kun Luo, Pu Zhao, Ke-Wei Fang, Wan-Xiang Zhao, Jiachang Lu, Hong-Qun Liu, Shui-Yong Wang, Mengmeng Zhu, and Y.-X. Qiao. The galvanic corrosion behavior of zcual10fe5ni5 coupled with saf2507 duplex stainless steel in seawater. Metals, 16:473, Apr 2026. URL: https://doi.org/10.3390/met16050473, doi:10.3390/met16050473. This article has 0 citations.

21. (powell2004corrosionandbiofouling pages 1-4): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.

22. (schleich2004typicalfailuresof pages 3-6): W Schleich. Typical failures of cuni 90/10 seawater tubing systems and how to avoid them. Unknown journal, 2004.

23. (powell2004corrosionandbiofouling pages 9-10): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.

24. (powell2004corrosionandbiofouling pages 4-6): C Powell. Corrosion and biofouling resistance evaluation of 90-10 copper-nickel. Unknown journal, 2004.

25. (qian2025corrosivestudyof pages 10-11): Feng Qian, Xvhui Liu, Rui Cui, Kai Wang, Chao Wang, Xiong Bao, Dongsheng Dong, Mengni Zhou, Zunhua Zhang, Xiaofeng Guo, and Jie Wang. Corrosive study of b10/b30 copper-nickel alloys coupled pipeline in static seawater. Advanced Composites and Hybrid Materials, Jan 2025. URL: https://doi.org/10.1007/s42114-024-01174-0, doi:10.1007/s42114-024-01174-0. This article has 12 citations and is from a peer-reviewed journal.

26. (takaloo2011corrosionbehaviorof pages 1-2): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 5 citations and is from a peer-reviewed journal.

27. (barik2005erosionanderosion–corrosion pages 2-3): R.C. Barik, J.A. Wharton, R.J.K. Wood, K.S. Tan, and K.R. Stokes. Erosion and erosion–corrosion performance of cast and thermally sprayed nickel–aluminium bronze. Wear, 259:230-242, Jul 2005. URL: https://doi.org/10.1016/j.wear.2005.02.033, doi:10.1016/j.wear.2005.02.033. This article has 178 citations and is from a highest quality peer-reviewed journal.
