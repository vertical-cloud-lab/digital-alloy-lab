<!--
Edison Scientific LITERATURE task (batch 4)
- Task ID: e2806913-5a0a-4937-a752-e79545467dab
- Submitted: 2026-10-17T06:11:14Z
- Fetched: 2026-10-17T06:41:56Z (status: success)
- Raw trajectory JSON: ../raw/b4-07-bo-for-ded-process-windows.json.gz
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

QUESTION: How have Bayesian optimization, active learning, and
physics-informed or multi-fidelity surrogates been used to find blown-powder
DED process windows (single tracks, walls, blocks) for any alloy, and with
what savings? Include work that uses analytical thermal models or
normalized process maps as priors or low-fidelity sources, constrained BO
for crack-free/dense deposits, and studies that tune DED settings together
with alloy composition (e.g. compositionally graded DED, in-situ alloying
for alloy discovery). Name the closest analogues to a cost-aware search
over composition, powder, and DED settings with corrosion as an objective,
and report the number of experiments they needed.

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

QUESTION: How have Bayesian optimization, active learning, and
physics-informed or multi-fidelity surrogates been used to find blown-powder
DED process windows (single tracks, walls, blocks) for any alloy, and with
what savings? Include work that uses analytical thermal models or
normalized process maps as priors or low-fidelity sources, constrained BO
for crack-free/dense deposits, and studies that tune DED settings together
with alloy composition (e.g. compositionally graded DED, in-situ alloying
for alloy discovery). Name the closest analogues to a cost-aware search
over composition, powder, and DED settings with corrosion as an objective,
and report the number of experiments they needed.

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


# Evidence relevant to a DED process-window proposal

**Bottom line.** The strongest precedents demonstrate (i) multifidelity optimization of *simulated* DED melt-pool depth, (ii) experimental progression from beads to dense blocks, and (iii) active learning of DED alloy composition. They do **not**, in the studies verified here, demonstrate one cost-aware search spanning **pre-alloyed copper-powder manufacture, blown-powder DED settings, crack-free repair interfaces, and as-deposited seawater corrosion**. Counts below distinguish physical deposits from simulation evaluations and optimizer-only trials. Unless stated otherwise, the cited studies did **not** report a seawater test; consequently, seawater duration, flow, corrosion current, potential, impedance, and selective-attack depth are **not available** for them. (kitt2024machinelearningenhanced pages 5-8, menon2022multifidelitysurrogatebasedprocess pages 21-23, nelaturu2024multiprincipalelementalloy pages 8-13)

## Process windows, physical priors, and multifidelity savings

1. **N. Menon, S. Mondal and A. Basak, “Multi-Fidelity Surrogate-Based Process Mapping with Uncertainty Quantification in Laser Directed Energy Deposition,” *Materials* 15 (2022) 2902. DOI: 10.3390/ma15082902.** **Process/material:** laser DED thermal-model study of Ni-base **CMSX-4**; the paper also discusses IN625 single-layer experimental validation of the underlying model. A feedstock composition in wt% and powder-lot size, Hall flow, apparent density, and oxygen are not reported in the evidence examined. **Method:** an Eagar–Tsai analytical heat-source model supplies cheap melt-pool-depth predictions; Autodesk Netfabb finite elements supply expensive predictions. A multifidelity Gaussian process and BO select power and scan speed to maintain **1.00 ± 0.03 mm** depth through the transient. **Numbers:** **40 high-fidelity plus 80 low-fidelity model evaluations** gave a depth surrogate with **R² = 0.99** and **RMSE = 0.029 mm**. At 20 high-fidelity evaluations and six low-fidelity evaluations per high-fidelity evaluation, multifidelity modeling lowered prediction RMSE **55%** and predictive uncertainty **61%** relative to the single-fidelity comparator. In BO tests with a **five-step** maximum budget, average budget consumption fell approximately **12%**; a finite-element evaluation cost approximately **10×** an analytical evaluation at 2 s and **150×** at 10 s. These are **computational**, not demonstrated powder, build, or corrosion-test savings. The authors explicitly leave experimental data as a future highest-fidelity tier. **[CITE] [NUMBERS] [GAP] [NOVELTY-RISK: the analytical-thermal/multifidelity BO concept itself is established.]** This work was supported in part by the **U.S. Army**, not identified here as Navy-funded. (menon2022multifidelitysurrogatebasedprocess pages 9-11, menon2022multifidelitysurrogatebasedprocess pages 14-17, menon2022multifidelitysurrogatebasedprocess pages 19-21, menon2022multifidelitysurrogatebasedprocess pages 21-23)

2. **J. M. S. de Sousa *et al.*, “Gaussian process regression for optimizing L-DED processing parameters in AlSi10Mg additive manufacturing,” *International Journal of Advanced Manufacturing Technology* 146 (2026) 247–287. DOI: 10.1007/s00170-026-18817-9.** **Process/material:** blown-powder laser DED on Al5052; powder **Al–9.76Si–0.33Mg–0.14Fe–0.003Mn wt%, balance Al**, plasma-atomized **45–105 μm**, with **D10/D50/D90 = 58.9/69.7/83.7 μm**. **Sequence:** **36 physical single beads**, **30 single-layer observations** for GP cross-validation, triplicate validation layers, then ten-layer approximately **25.4-mm cubes**. The authors fit GPs for dilution, height, waviness, and powder-capture efficiency, and call their procedure multiobjective BO; importantly, its **100 optimizer trials per study are NSGA-II evaluations of fitted GP predictions, not 100 new DED experiments**. Bounds/penalties target **20–35% dilution** and **0.5–1.2 mm** layer height; this is *not* a demonstrated probabilistic crack-feasibility constraint. **Outcome:** multilayer relative densities **99.55–99.80%** in the abstract; a reported best cube is approximately **99.8%**. Deposition efficiencies reach **87–97%** across reported conditions. Regression-selected **2017 W, 381 mm/min, 1.66-mm hatch, 2.54-mm spot** produced measured **29.08 ± 1.72% dilution**, **92.45 ± 3.87% efficiency** in triplicate layers. The as-built hardness is **48 ± 3 HV**; **86 ± 8 HV** is *after T6* and must not be treated as an as-deposited result. GP leave-one-out **R² for efficiency was only 0.043**, an important warning about confidently optimizing powder capture from small datasets. **Savings:** no controlled experimental-count reduction against a conventional DOE is established. No corrosion measurements or lot oxygen/flow results are provided in the examined evidence. **[CITE] [NUMBERS] [NOVELTY-RISK: the bead→layer→block and surrogate workflow overlaps.] [GAP: no copper, seawater, or independently verified BO experiment savings.]** (sousa2026gaussianprocessregression pages 6-7, sousa2026gaussianprocessregression pages 1-2, sousa2026gaussianprocessregression pages 32-34, sousa2026gaussianprocessregression pages 7-9, sousa2026gaussianprocessregression pages 11-13, sousa2026gaussianprocessregression pages 37-38, sousa2026gaussianprocessregression pages 34-37)

3. **K.-H. Huang, C. D. Jamieson and A. Basak, “Uncertainty-aware reconstruction of full process maps in laser-directed energy deposition using scarce data,” *Welding in the World* (2026). DOI: 10.1007/s40194-026-02629-2.** **Process/material:** **44 laser-wire DED** single beads made with 316LSi wire on SS304 inform transfer to **20 laser-powder DED** IN718 single beads. The latter use **700 or 1000 W**, **3 or 6 g/min powder**, and five scan speeds at each power. An uncertainty-aware transfer model reconstructs bead **width, height and cross-sectional area**, achieving **R² = 0.95**, **5.13% coefficient of variation**, and **95% prediction-interval coverage** in the reported test. **Savings:** twenty target-process observations suffice for this reported prediction exercise; there is **no quantified comparison of physical experiments saved**, no prospective BO search, density, crack, or corrosion result. Alloy elemental wt%, powder flowability, and oxygen are not given in the examined evidence. **[CITE] [NUMBERS] [GAP: useful sparse-data transfer precedent, not a validated optimum.]** (huang2026uncertaintyawarereconstructionof pages 13-15, huang2026uncertaintyawarereconstructionof pages 1-2, huang2026uncertaintyawarereconstructionof pages 2-4)

4. **S. Mondal, D. Gwynn, A. Ray and A. Basak, “Investigation of Melt Pool Geometry Control in Additive Manufacturing Using Hybrid Modeling,” *Metals* 10 (2020) 683. DOI: 10.3390/met10050683.** The reported methodology combines a three-dimensional analytical thermal model, GP prediction and BO for time-dependent melt-pool-geometry control; it is an antecedent to item 1. **Evidence limitation:** the retrieved full-text chunks for this title displayed an **unrelated derivative-free-optimization article**. Accordingly, I cannot verify its alloy wt%, physical experiment count, numerical savings, or deposit-density values from its primary text, and do not assign it such numbers. **[CITE: methodological antecedent, subject to primary-text verification] [GAP].** (menon2022multifidelitysurrogatebasedprocess pages 26-27, dharmadhikari2023areinforcementlearning pages 1-2)

## Crack-aware processing and jointly exploring material and settings

5. **A. Kitt, C. Sun and L. Yuan, “Machine Learning Enhanced Development of Functionally Graded Materials Enabled by Directed Energy Deposition,” U.S. DOE final report (2024). DOI: 10.2172/2311804.** **Process/material:** laser DED of **IN718, René 41, and René 80**, including an **IN718→René 41 compositional gradient**; these commercial alloy designations are established, but feedstock and graded-zone elemental **wt% were not specified** in the examined passages. Thermodynamic/Scheil screening supported the gradient. Transfer using Bayesian hybrid modeling and IDACE selected settings for single-pass walls; the engineering *crack-propensity proxy* was bead width/(bead height + fusion depth) between **1.5 and 1.8**. **Experiment count:** **209 distinct trials across 22 physical builds** for the three alloys; approximately **eight** initial René 80 builds seeded transfer. Conventional IN718 bead→hatch→wall→cube development took **7 weeks**; transfer-guided René 80 development **5 weeks**, and the report’s development-timeline figure shows René 41 at **3 weeks** and its gradient at **2 weeks**. These are different alloy campaigns, **not** a randomized same-alloy head-to-head saving. René 41 cubes attained **>99.9% density**, but **crack-free René 80 cubes were not achieved**—a decisive limit on the constraint surrogate. The final graded component measured **99.96% density**, with no cracking reported in the mapped region; its estimated production costs were **$19.2k versus $21.5k**, approximately **10.7% projected cost saving**. **Tests:** strength/fatigue were evaluated; this is not a seawater-corrosion study. **Funding:** DOE/EERE, **not established as Navy-funded**. **[CITE] [NUMBERS] [NOVELTY-RISK: composition gradients, thermal/phase screening and crack-aware transfer overlap.] [GAP: no universally reliable crack-free cube prediction or seawater objective.]** (kitt2024machinelearningenhanced pages 5-8, kitt2024machinelearningenhanced pages 1-3, kitt2024machinelearningenhanced pages 24-29, kitt2024machinelearningenhanced media 57945781)

6. **P. Nelaturu, J. R. Hattrick-Simpers, M. Moorehead, V. Jambur, I. Szlufarska, A. Couet and D. J. Thoma, “Multi-principal element alloy discovery using directed energy deposition and machine learning,” *Materials Science and Engineering A* 891 (2024) 145945. DOI: 10.1016/j.msea.2023.145945.** **Process/material:** four-hopper, **in-situ elemental blending** of Cr, Fe, Mn and Ni by blown-powder LENS—**not one pre-alloyed powder**. Gas-atomized elemental powder was approximately **45–150 μm**; the reported **<5 ppm oxygen is chamber atmosphere, not powder-lot oxygen**. Physical printing parameters were first tuned with a **25-sample** power/speed array and a separate **25-sample** remelt array; the chosen condition was **350 W and 10.6 mm/s**, followed by three remelts at **500 W and 21.2 mm/s**. **Composition-search counts:** **115 initial bulk compositions**, of which **83 single-phase FCC compositions** trained the hardness learner; **42** learner-selected FCC alloys were then built from **788** screened candidates (**125 FCC learning specimens total**, not 125 total initial DED specimens). Across the 42 new alloys, hardness was **173.7–310.7 HV0.05**, against **138.3–281.7 HV0.05** initially. The leading alloy is **Cr33Fe23Mn1Ni43 in *atomic* percent**, at **310.7 HV0.05**; it would be incorrect to relabel those numbers wt%. The second round reduced prediction uncertainty **4.7%**, but its out-of-round hardness **R² was −0.3**. **Throughput:** **25 approximately 10 × 10 × 5 mm bulk alloys in four hours**, or **>100/week**; this is synthesis throughput, not proven BO savings. **Critical mismatch:** specimens were **homogenized at 1000 °C for 24 h** before hardness testing; no reported seawater corrosion or jointly learned DED-setting/composition/corrosion objective. **[CITE] [NUMBERS] [NOVELTY-RISK: the closest physical DED/compositional active-learning loop.] [GAP: in-situ blending and post-treatment do not establish pre-alloyed, as-deposited copper performance.]** (nelaturu2024multiprincipalelementalloy pages 16-20, nelaturu2024multiprincipalelementalloy pages 1-4, nelaturu2024multiprincipalelementalloy pages 4-8, nelaturu2024multiprincipalelementalloy pages 8-13)

7. **H. Tian, I. Saad, T. Chen, T. Gao, H. Yoong and B. L. Chua, “Optimizing material and process parameters in laser engineered net shaping using liquid neural networks,” *Scientific Reports* 16 (2026). DOI: 10.1038/s41598-026-52507-6.** **Process/material:** coaxial-powder LENS cladding on **AISI 4130**, selecting among **Ni60A, Stellite 6 and IN625** and varying laser power, speed, powder feed and overlap. **Ninety physical experimental samples** underpin a physics-informed liquid-neural-network/inverse multiobjective exercise. Reported Ni60A optimization gives **12.5% greater microhardness**, **18% lower dilution** and **23% better roughness**; the main quality targets also include clad uniformity. **Distinction:** categorical feedstock selection is *not* continuous alloy-composition optimization; the implemented experimental campaign was an orthogonal design, **not demonstrated sequential BO**. No quantitative seawater test or experiment-count saving is supplied. **[CITE] [NUMBERS] [GAP].** (tian2026optimizingmaterialand pages 1-2, tian2026optimizingmaterialand pages 2-4, tian2026optimizingmaterialand pages 14-15)

8. **X. Shang, E. Li, A. Talbot, H. Wen, T. Lyu, J. Zhang and Y. Zou, “Accurate Inverse Process Optimization Framework in Laser Directed Energy Deposition,” available preprint DOI: 10.48550/arXiv.2407.17338 (associated with *Additive Manufacturing*, 2025; a separate publisher DOI was not verified).** **Process/material:** laser-powder DED, primarily **316L and 17-4PH**, with pure-Ni transfer; elemental wt% and powder-lot metrics were not verified. AIDED fits machine-learning models to **444 physical single-track geometries** and **112 multi-track prints**, then uses a **genetic algorithm, not BO**, to optimize speed/resolution and validate multilayer cubes. Its cubes achieved **>99.9% density**. A fastest **10 × 10 × 5 mm** cube took **101.9 s**, a **62.6% printing-time reduction** against its highest-resolution case—not 62.6% fewer experiments. For Ni transfer, **71 new single tracks** yielded **56 images used for retraining**; the paper’s “fewer than 60” pertains to training images, not total Ni tracks fabricated. No seawater or prospective corrosion selection. **[CITE] [NUMBERS] [GAP: strong track→block inverse-design benchmark, but not BO.]** (shang2025accurateinverseprocess pages 25-29, shang2025accurateinverseprocess pages 8-11, shang2025accurateinverseprocess pages 3-8)

## Closest corrosion analogue—and the missing combination

9. **T. Duong, Y. Wang, X. Yan, A. Couet and S. Chaudhuri, “A First-Principles-Based Approach to the High-Throughput Screening of Corrosion-Resistant High Entropy Alloys,” preprint (2021). DOI: 10.48550/arXiv.2104.10590.** **Process/material:** computational screening of **Co–Cr–Fe–Mn–Mo–Ni** compositions with DFT surface energy/work function and **Bayesian CALPHAD**; *Bayesian modeling is not BO*. Predicted corrosion ranking favors some Ni/Co/Mo-rich compositions, but **no matched blown-powder DED fabrication count or aqueous seawater current/rate** is established by the retrieved paper. **[CITE: corrosion-screening concept] [GAP: not a physical seawater-DED optimization].** (duong2021afirstprinciplesbasedapproach pages 1-2, duong2021afirstprinciplesbasedapproach pages 4-6, duong2021afirstprinciplesbasedapproach pages 2-4)

A related **high-throughput corrosion experiment**, described in B. Goh, *Interpretable Machine Learning Trained on Experimental Data for Novel Insights into Complex Compositional Alloy Corrosion Phenomena in Molten Salts* (2023 thesis; **no DOI verified**), printed **110** Cr–Fe–Mn–Ni alloys by elemental-feed LENS. Its test was **LiCl–KCl 59:41 wt% + 2 wt% EuCl₃, 500 °C for 96 h**, assessing dissolution with **ICP-MS**; a reported subset of **90** alloys also received comparative depth-resolved analysis. These are **molten-salt, high-temperature, elemental-blend** corrosion tests, *not* ambient flowing seawater, a C71500 comparison, or demonstrated corrosion-directed BO. Because a thesis DOI and the underlying paper’s full primary citation were not verified, these counts are **contextual benchmarks, not a DOI-complete primary-paper claim**. **[NUMBERS] [NOVELTY-RISK: DED-made multi-alloy corrosion libraries exist.] [GAP: environment, feed and acquisition strategy differ.]** (goh2023interpretablemachinelearning pages 125-131, goh2023interpretablemachinelearning pages 150-155)

**What cannot responsibly be claimed:** This search did not establish a physical, prospectively **cost-aware function-network BO** study simultaneously optimizing alloy wt%, independently atomized **single-stream pre-alloyed** powder properties, DED power/speed/feed/hatch, crack and porosity constraints on both copper substrates, and **as-deposited** corrosion against wrought **C71500** in controlled 3.5 wt% NaCl, ASTM D1141 substitute seawater, or natural seawater. Accordingly, none of the studies above provides a defensible cross-paper numerical threshold for the proposal’s required **i_corr, E_corr, impedance, corrosion rate or selective-attack depth** under matching salinity, duration and flow. Neither an experimental saving for such a combined search nor a demonstrated advantage of *thermal-history-conditioned CALPHAD over equilibrium-only CALPHAD* can be borrowed from these examples. (kitt2024machinelearningenhanced pages 5-8, nelaturu2024multiprincipalelementalloy pages 1-4, menon2022multifidelitysurrogatebasedprocess pages 21-23)

## Ranked top 5 things the PI should know

1. **State the novel conjunction, not novel BO for DED.** Analytical-thermal multifidelity BO, bead→cube GP optimization, graded-alloy crack-aware transfer, and active-learning DED composition already exist individually. The credible gap is their **prospectively linked, cost-accounted integration with single-stream copper-powder manufacture, repair-substrate feasibility and as-deposited seawater corrosion**. (kitt2024machinelearningenhanced pages 5-8, menon2022multifidelitysurrogatebasedprocess pages 21-23, nelaturu2024multiprincipalelementalloy pages 8-13)
2. **Use honest savings denominators.** The clearest approximately **12% saving** is Menon’s *simulation BO budget*; de Sousa’s **100 trials are surrogate/NSGA-II evaluations**; Shang’s **62.6% is print time**; Kitt’s **10.7% is estimated production cost**. None demonstrates a percentage reduction in physical copper-corrosion experiments. (menon2022multifidelitysurrogatebasedprocess pages 19-21, sousa2026gaussianprocessregression pages 11-13, kitt2024machinelearningenhanced pages 24-29, shang2025accurateinverseprocess pages 25-29)
3. **Treat failure as an informative constraint.** René 80’s crack-free walls did **not** translate into crack-free cubes. Demonstrate separate, prospective feasibility checks for track, wall, block and each repair interface; do not infer bulk crack freedom from a single bead or a nominal weld-ratio window. (kitt2024machinelearningenhanced pages 5-8)
4. **Budget realistic physical anchor counts.** Existing illustrative scales are **36 beads plus 30 layers** for one Al alloy, **20 target-process beads** for transferred geometry prediction, and **115 initial compositions plus 42 acquired alloys** for elemental-mix hardness discovery. These counts are *precedents*, not justified sample-size predictions for a new copper/corrosion campaign. (sousa2026gaussianprocessregression pages 6-7, sousa2026gaussianprocessregression pages 32-34, huang2026uncertaintyawarereconstructionof pages 2-4, nelaturu2024multiprincipalelementalloy pages 8-13, nelaturu2024multiprincipalelementalloy pages 16-20)
5. **Make the naval acceptance comparison truly comparable.** Specify the same wrought C71500 control, surface condition, salinity, temperature, aeration, duration and flow for all deposits and interfaces; measure selective attack as well as electrochemistry, and score **as deposited**, before any heat treatment. The nearest alloy active-learning precedent instead relies on **24-h homogenization**, and the nearest large corrosion-library example used **500 °C molten chloride**, not seawater. (nelaturu2024multiprincipalelementalloy pages 8-13, goh2023interpretablemachinelearning pages 125-131)

References

1. (kitt2024machinelearningenhanced pages 5-8): Alex Kitt, Changjie Sun, and Lang Yuan. Machine learning enhanced development of functionally graded materials enabled by directed energy deposition. ArXiv, Jan 2024. URL: https://doi.org/10.2172/2311804, doi:10.2172/2311804. This article has 3 citations.

2. (menon2022multifidelitysurrogatebasedprocess pages 21-23): Nandana Menon, Sudeepta Mondal, and Amrita Basak. Multi-fidelity surrogate-based process mapping with uncertainty quantification in laser directed energy deposition. Materials, 15:2902, Apr 2022. URL: https://doi.org/10.3390/ma15082902, doi:10.3390/ma15082902. This article has 45 citations.

3. (nelaturu2024multiprincipalelementalloy pages 8-13): Phalgun Nelaturu, Jason R. Hattrick-Simpers, Michael Moorehead, Vrishank Jambur, Izabela Szlufarska, Adrien Couet, and Dan J. Thoma. Multi-principal element alloy discovery using directed energy deposition and machine learning. Jan 2024. URL: https://doi.org/10.1016/j.msea.2023.145945, doi:10.1016/j.msea.2023.145945. This article has 45 citations.

4. (menon2022multifidelitysurrogatebasedprocess pages 9-11): Nandana Menon, Sudeepta Mondal, and Amrita Basak. Multi-fidelity surrogate-based process mapping with uncertainty quantification in laser directed energy deposition. Materials, 15:2902, Apr 2022. URL: https://doi.org/10.3390/ma15082902, doi:10.3390/ma15082902. This article has 45 citations.

5. (menon2022multifidelitysurrogatebasedprocess pages 14-17): Nandana Menon, Sudeepta Mondal, and Amrita Basak. Multi-fidelity surrogate-based process mapping with uncertainty quantification in laser directed energy deposition. Materials, 15:2902, Apr 2022. URL: https://doi.org/10.3390/ma15082902, doi:10.3390/ma15082902. This article has 45 citations.

6. (menon2022multifidelitysurrogatebasedprocess pages 19-21): Nandana Menon, Sudeepta Mondal, and Amrita Basak. Multi-fidelity surrogate-based process mapping with uncertainty quantification in laser directed energy deposition. Materials, 15:2902, Apr 2022. URL: https://doi.org/10.3390/ma15082902, doi:10.3390/ma15082902. This article has 45 citations.

7. (sousa2026gaussianprocessregression pages 6-7): Jurandir Marcos Sá de Sousa, Henrique Santos Ferreira, Anselmo Thiesen, Marcos Vinicius Bento, William Mendes de Farias, Priscila Maria Barra Ferreira, Mustafa Awd, Evgeniya Kabliman, Alexandre Pinhel Soares, and Juliane Ribeiro da Cruz. Gaussian process regression for optimizing l-ded processing parameters in alsi10mg additive manufacturing. Jul 2026. URL: https://doi.org/10.1007/s00170-026-18817-9, doi:10.1007/s00170-026-18817-9. This article has 0 citations.

8. (sousa2026gaussianprocessregression pages 1-2): Jurandir Marcos Sá de Sousa, Henrique Santos Ferreira, Anselmo Thiesen, Marcos Vinicius Bento, William Mendes de Farias, Priscila Maria Barra Ferreira, Mustafa Awd, Evgeniya Kabliman, Alexandre Pinhel Soares, and Juliane Ribeiro da Cruz. Gaussian process regression for optimizing l-ded processing parameters in alsi10mg additive manufacturing. Jul 2026. URL: https://doi.org/10.1007/s00170-026-18817-9, doi:10.1007/s00170-026-18817-9. This article has 0 citations.

9. (sousa2026gaussianprocessregression pages 32-34): Jurandir Marcos Sá de Sousa, Henrique Santos Ferreira, Anselmo Thiesen, Marcos Vinicius Bento, William Mendes de Farias, Priscila Maria Barra Ferreira, Mustafa Awd, Evgeniya Kabliman, Alexandre Pinhel Soares, and Juliane Ribeiro da Cruz. Gaussian process regression for optimizing l-ded processing parameters in alsi10mg additive manufacturing. Jul 2026. URL: https://doi.org/10.1007/s00170-026-18817-9, doi:10.1007/s00170-026-18817-9. This article has 0 citations.

10. (sousa2026gaussianprocessregression pages 7-9): Jurandir Marcos Sá de Sousa, Henrique Santos Ferreira, Anselmo Thiesen, Marcos Vinicius Bento, William Mendes de Farias, Priscila Maria Barra Ferreira, Mustafa Awd, Evgeniya Kabliman, Alexandre Pinhel Soares, and Juliane Ribeiro da Cruz. Gaussian process regression for optimizing l-ded processing parameters in alsi10mg additive manufacturing. Jul 2026. URL: https://doi.org/10.1007/s00170-026-18817-9, doi:10.1007/s00170-026-18817-9. This article has 0 citations.

11. (sousa2026gaussianprocessregression pages 11-13): Jurandir Marcos Sá de Sousa, Henrique Santos Ferreira, Anselmo Thiesen, Marcos Vinicius Bento, William Mendes de Farias, Priscila Maria Barra Ferreira, Mustafa Awd, Evgeniya Kabliman, Alexandre Pinhel Soares, and Juliane Ribeiro da Cruz. Gaussian process regression for optimizing l-ded processing parameters in alsi10mg additive manufacturing. Jul 2026. URL: https://doi.org/10.1007/s00170-026-18817-9, doi:10.1007/s00170-026-18817-9. This article has 0 citations.

12. (sousa2026gaussianprocessregression pages 37-38): Jurandir Marcos Sá de Sousa, Henrique Santos Ferreira, Anselmo Thiesen, Marcos Vinicius Bento, William Mendes de Farias, Priscila Maria Barra Ferreira, Mustafa Awd, Evgeniya Kabliman, Alexandre Pinhel Soares, and Juliane Ribeiro da Cruz. Gaussian process regression for optimizing l-ded processing parameters in alsi10mg additive manufacturing. Jul 2026. URL: https://doi.org/10.1007/s00170-026-18817-9, doi:10.1007/s00170-026-18817-9. This article has 0 citations.

13. (sousa2026gaussianprocessregression pages 34-37): Jurandir Marcos Sá de Sousa, Henrique Santos Ferreira, Anselmo Thiesen, Marcos Vinicius Bento, William Mendes de Farias, Priscila Maria Barra Ferreira, Mustafa Awd, Evgeniya Kabliman, Alexandre Pinhel Soares, and Juliane Ribeiro da Cruz. Gaussian process regression for optimizing l-ded processing parameters in alsi10mg additive manufacturing. Jul 2026. URL: https://doi.org/10.1007/s00170-026-18817-9, doi:10.1007/s00170-026-18817-9. This article has 0 citations.

14. (huang2026uncertaintyawarereconstructionof pages 13-15): Kun-Hao Huang, Cory D. Jamieson, and Amrita Basak. Uncertainty-aware reconstruction of full process maps in laser-directed energy deposition using scarce data. Welding in the World, Sep 2026. URL: https://doi.org/10.1007/s40194-026-02629-2, doi:10.1007/s40194-026-02629-2. This article has 0 citations and is from a domain leading peer-reviewed journal.

15. (huang2026uncertaintyawarereconstructionof pages 1-2): Kun-Hao Huang, Cory D. Jamieson, and Amrita Basak. Uncertainty-aware reconstruction of full process maps in laser-directed energy deposition using scarce data. Welding in the World, Sep 2026. URL: https://doi.org/10.1007/s40194-026-02629-2, doi:10.1007/s40194-026-02629-2. This article has 0 citations and is from a domain leading peer-reviewed journal.

16. (huang2026uncertaintyawarereconstructionof pages 2-4): Kun-Hao Huang, Cory D. Jamieson, and Amrita Basak. Uncertainty-aware reconstruction of full process maps in laser-directed energy deposition using scarce data. Welding in the World, Sep 2026. URL: https://doi.org/10.1007/s40194-026-02629-2, doi:10.1007/s40194-026-02629-2. This article has 0 citations and is from a domain leading peer-reviewed journal.

17. (menon2022multifidelitysurrogatebasedprocess pages 26-27): Nandana Menon, Sudeepta Mondal, and Amrita Basak. Multi-fidelity surrogate-based process mapping with uncertainty quantification in laser directed energy deposition. Materials, 15:2902, Apr 2022. URL: https://doi.org/10.3390/ma15082902, doi:10.3390/ma15082902. This article has 45 citations.

18. (dharmadhikari2023areinforcementlearning pages 1-2): Susheel Dharmadhikari, Nandana Menon, and Amrita Basak. A reinforcement learning approach for process parameter optimization in additive manufacturing. Jun 2023. URL: https://doi.org/10.1016/j.addma.2023.103556, doi:10.1016/j.addma.2023.103556. This article has 170 citations and is from a highest quality peer-reviewed journal.

19. (kitt2024machinelearningenhanced pages 1-3): Alex Kitt, Changjie Sun, and Lang Yuan. Machine learning enhanced development of functionally graded materials enabled by directed energy deposition. ArXiv, Jan 2024. URL: https://doi.org/10.2172/2311804, doi:10.2172/2311804. This article has 3 citations.

20. (kitt2024machinelearningenhanced pages 24-29): Alex Kitt, Changjie Sun, and Lang Yuan. Machine learning enhanced development of functionally graded materials enabled by directed energy deposition. ArXiv, Jan 2024. URL: https://doi.org/10.2172/2311804, doi:10.2172/2311804. This article has 3 citations.

21. (kitt2024machinelearningenhanced media 57945781): Alex Kitt, Changjie Sun, and Lang Yuan. Machine learning enhanced development of functionally graded materials enabled by directed energy deposition. ArXiv, Jan 2024. URL: https://doi.org/10.2172/2311804, doi:10.2172/2311804. This article has 3 citations.

22. (nelaturu2024multiprincipalelementalloy pages 16-20): Phalgun Nelaturu, Jason R. Hattrick-Simpers, Michael Moorehead, Vrishank Jambur, Izabela Szlufarska, Adrien Couet, and Dan J. Thoma. Multi-principal element alloy discovery using directed energy deposition and machine learning. Jan 2024. URL: https://doi.org/10.1016/j.msea.2023.145945, doi:10.1016/j.msea.2023.145945. This article has 45 citations.

23. (nelaturu2024multiprincipalelementalloy pages 1-4): Phalgun Nelaturu, Jason R. Hattrick-Simpers, Michael Moorehead, Vrishank Jambur, Izabela Szlufarska, Adrien Couet, and Dan J. Thoma. Multi-principal element alloy discovery using directed energy deposition and machine learning. Jan 2024. URL: https://doi.org/10.1016/j.msea.2023.145945, doi:10.1016/j.msea.2023.145945. This article has 45 citations.

24. (nelaturu2024multiprincipalelementalloy pages 4-8): Phalgun Nelaturu, Jason R. Hattrick-Simpers, Michael Moorehead, Vrishank Jambur, Izabela Szlufarska, Adrien Couet, and Dan J. Thoma. Multi-principal element alloy discovery using directed energy deposition and machine learning. Jan 2024. URL: https://doi.org/10.1016/j.msea.2023.145945, doi:10.1016/j.msea.2023.145945. This article has 45 citations.

25. (tian2026optimizingmaterialand pages 1-2): Haijiang Tian, Ismail Saad, Tianshu Chen, Teng Gao, Houpin Yoong, and Bih Lii Chua. Optimizing material and process parameters in laser engineered net shaping using liquid neural networks. Scientific Reports, May 2026. URL: https://doi.org/10.1038/s41598-026-52507-6, doi:10.1038/s41598-026-52507-6. This article has 0 citations and is from a peer-reviewed journal.

26. (tian2026optimizingmaterialand pages 2-4): Haijiang Tian, Ismail Saad, Tianshu Chen, Teng Gao, Houpin Yoong, and Bih Lii Chua. Optimizing material and process parameters in laser engineered net shaping using liquid neural networks. Scientific Reports, May 2026. URL: https://doi.org/10.1038/s41598-026-52507-6, doi:10.1038/s41598-026-52507-6. This article has 0 citations and is from a peer-reviewed journal.

27. (tian2026optimizingmaterialand pages 14-15): Haijiang Tian, Ismail Saad, Tianshu Chen, Teng Gao, Houpin Yoong, and Bih Lii Chua. Optimizing material and process parameters in laser engineered net shaping using liquid neural networks. Scientific Reports, May 2026. URL: https://doi.org/10.1038/s41598-026-52507-6, doi:10.1038/s41598-026-52507-6. This article has 0 citations and is from a peer-reviewed journal.

28. (shang2025accurateinverseprocess pages 25-29): Xiao Shang, Evelyn Li, Ajay Talbot, Haitao Wen, Tianyi Lyu, Jiahui Zhang, and Yu Zou. Accurate inverse process optimization framework in laser directed energy deposition. Additive Manufacturing, Jul 2025. URL: https://doi.org/10.48550/arxiv.2407.17338, doi:10.48550/arxiv.2407.17338. This article has 57 citations and is from a highest quality peer-reviewed journal.

29. (shang2025accurateinverseprocess pages 8-11): Xiao Shang, Evelyn Li, Ajay Talbot, Haitao Wen, Tianyi Lyu, Jiahui Zhang, and Yu Zou. Accurate inverse process optimization framework in laser directed energy deposition. Additive Manufacturing, Jul 2025. URL: https://doi.org/10.48550/arxiv.2407.17338, doi:10.48550/arxiv.2407.17338. This article has 57 citations and is from a highest quality peer-reviewed journal.

30. (shang2025accurateinverseprocess pages 3-8): Xiao Shang, Evelyn Li, Ajay Talbot, Haitao Wen, Tianyi Lyu, Jiahui Zhang, and Yu Zou. Accurate inverse process optimization framework in laser directed energy deposition. Additive Manufacturing, Jul 2025. URL: https://doi.org/10.48550/arxiv.2407.17338, doi:10.48550/arxiv.2407.17338. This article has 57 citations and is from a highest quality peer-reviewed journal.

31. (duong2021afirstprinciplesbasedapproach pages 1-2): Thien Duong, Yafei Wang, Xiaoli Yan, Adrien Couet, and Santanu Chaudhuri. A first-principles-based approach to the high-throughput screening of corrosion-resistant high entropy alloys. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2104.10590, doi:10.48550/arxiv.2104.10590. This article has 5 citations.

32. (duong2021afirstprinciplesbasedapproach pages 4-6): Thien Duong, Yafei Wang, Xiaoli Yan, Adrien Couet, and Santanu Chaudhuri. A first-principles-based approach to the high-throughput screening of corrosion-resistant high entropy alloys. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2104.10590, doi:10.48550/arxiv.2104.10590. This article has 5 citations.

33. (duong2021afirstprinciplesbasedapproach pages 2-4): Thien Duong, Yafei Wang, Xiaoli Yan, Adrien Couet, and Santanu Chaudhuri. A first-principles-based approach to the high-throughput screening of corrosion-resistant high entropy alloys. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2104.10590, doi:10.48550/arxiv.2104.10590. This article has 5 citations.

34. (goh2023interpretablemachinelearning pages 125-131): B Goh. Interpretable machine learning trained on experimental data for novel insights into complex compositional alloy corrosion phenomena in molten salts. Unknown journal, 2023.

35. (goh2023interpretablemachinelearning pages 150-155): B Goh. Interpretable machine learning trained on experimental data for novel insights into complex compositional alloy corrosion phenomena in molten salts. Unknown journal, 2023.
