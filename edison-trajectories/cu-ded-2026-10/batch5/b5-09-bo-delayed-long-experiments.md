<!--
Edison Scientific LITERATURE task (batch 5)
- Task ID: 04c29905-5680-4dc7-9348-8204ec420901
- Submitted: 2026-10-17T06:20:09Z
- Fetched: 2026-10-17T06:52:00Z (status: success)
- Raw trajectory JSON: ../raw/b5-09-bo-delayed-long-experiments.json.gz
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

QUESTION: What Bayesian optimization and active-learning methods handle
experiments that take weeks and give partial readings along the way (e.g.
corrosion films that evolve, creep, fatigue), and experiments still pending
when the next choice is made? Cover freeze-thaw BO and learning-curve
extrapolation, multi-fidelity BO with time or duration as the fidelity,
asynchronous batch BO with pending points (fantasies, local penalization),
BO with delayed feedback, and cost-aware stopping of running experiments.
Report any applications to corrosion, materials degradation, or alloy design,
and say which is closest to deciding, candidate by candidate, whether a
30-day immersion is worth starting given a one-hour electrochemical screen.

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

QUESTION: What Bayesian optimization and active-learning methods handle
experiments that take weeks and give partial readings along the way (e.g.
corrosion films that evolve, creep, fatigue), and experiments still pending
when the next choice is made? Cover freeze-thaw BO and learning-curve
extrapolation, multi-fidelity BO with time or duration as the fidelity,
asynchronous batch BO with pending points (fantasies, local penalization),
BO with delayed feedback, and cost-aware stopping of running experiments.
Report any applications to corrosion, materials degradation, or alloy design,
and say which is closest to deciding, candidate by candidate, whether a
30-day immersion is worth starting given a one-hour electrochemical screen.

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


# Bayesian optimization with weeks-long, partially observed experiments

**Bottom line.** The closest published decision model for *whether to start an expensive test on a particular candidate after seeing its cheap-test result* is **two-test Bayesian screening** by Hook, Hand and Whitfield. For an immersion **already under way**, trace-aware multi-fidelity Bayesian optimization and Bayesian stopping are closer models. Pending immersions require an additional asynchronous acquisition rule. These are complementary components, not one method already demonstrated for one-hour electrochemistry followed by 30-day corrosion of pre-alloyed, blown-powder laser-DED copper alloys. (hook2020bayesianscreeningmultitest pages 1-3, dai2019bayesianoptimizationmeets pages 3-4, balandat2019botorchprogrammablebayesian pages 6-7, hook2020bayesianscreeningmultitest pages 10-13)

## Methods and what each decision means

For the algorithm papers below, **process, alloy wt%, saline conditions, porosity, corrosion and mechanical measurements are not applicable** unless an application is explicitly identified. Reported computational speedups must not be read as corrosion-test speedups.

1. **Start the long test after a short screen — most direct match.** James Hook, Calum Hand and Emma Whitfield, “Bayesian Screening: Multi-test Bayesian Optimization Applied to in silico Material Screening” (2020), preprint, **DOI: 10.48550/arXiv.2009.05418**. Its state records which candidate has a cheap result but no expensive result; the next action can be that candidate’s expensive test. A covariate GP learns an *unknown nonlinear* cheap-to-expensive relationship, preferable to treating a one-hour corrosion measurement as an unbiased 30-day measurement. In simulated screens using previously calculated covalent-organic-framework methane-storage data, cheap void fraction cost 0.1 versus expensive deliverable-capacity cost 1; at budget 1,000, sequential greedy testing used approximately **2,742 cheap and 725 expensive tests**, obtaining reward **63.9**, versus **42.3** for 1,000 expensive-only tests with the poorer information set. A second, metal–organic-framework gas-separation screen used approximately **1,613 cheap and 387 expensive** tests. These are *computational porous materials*, not copper alloys or immersion experiments; their rewards are not corrosion rates. **[CITE] [NUMBERS] [GAP]** (hook2020bayesianscreeningmultitest pages 1-3, hook2020bayesianscreeningmultitest pages 10-13)

2. **Choose the candidate *and duration*, using all intermediate readings.** Jian Wu, Saul Toscano-Palmerin, Peter I. Frazier and Andrew Gordon Wilson, “Practical Multi-fidelity Bayesian Optimization for Hyperparameter Tuning” (2020), *Proceedings of the Conference on Uncertainty in Artificial Intelligence*; accessible preprint **DOI: 10.48550/arXiv.1903.04703**. Trace-aware knowledge gradient (taKG) models outcome against design and continuous fidelity, and scores a prospective run by its **expected reduction in best full-fidelity loss divided by evaluation cost**. A longer run yields a *trace* of shorter-duration observations; cached progress can be extended. For immersion, substitute elapsed exposure for training iterations, and explicitly charge for a new vessel versus extending one already occupied. Its published tests concern machine learning, **not corrosion**, and extending a running corrosion test is not necessarily as reversible as resuming computer training. **[CITE] [GAP]** (wu2020practicalmultifidelitybayesian pages 1-2, wu2020practicalmultifidelitybayesian pages 3-4, wu2020practicalmultifidelitybayesian pages 4-6)

   Related continuous-fidelity work is Aaron Klein, Stefan Falkner, Simon Bartels, Philipp Hennig and Frank Hutter, “Fast Bayesian Hyperparameter Optimization on Large Datasets,” *Electronic Journal of Statistics* **11** (2017), 4945–4968, **DOI: 10.1214/17-EJS1335SI**. FABOLAS chooses test configuration and training-set size for information about the full-size optimum *per unit time*; its reported **10–100-fold** acceleration is for machine-learning hyperparameters, not days of saltwater exposure. It establishes the cost-versus-bias principle, but duration and evolving corrosion films require a different response model. **[CITE] [NUMBERS] [GAP]** (klein2017fastbayesianhyperparameter pages 1-3)

3. **Stop or revisit an individual partially observed run.** Kevin Swersky, Jasper Snoek and Ryan Prescott Adams, “Freeze-Thaw Bayesian Optimization” (2014), preprint, **DOI: 10.48550/arXiv.1406.3896**, models partial learning curves to decide whether to pause a configuration, start another, or resume a previous one. Tobias Domhan, Jost Tobias Springenberg and Frank Hutter, “Speeding up Automatic Hyperparameter Optimization of Deep Neural Networks by Extrapolation of Learning Curves,” *Proceedings of IJCAI* (2015), 3460–3468 (**no DOI verified here**), probabilistically extrapolates incomplete runs and terminates predicted losers; the reported gain is roughly **twofold** in neural-network tuning. For immersion, stopping can save vessel time and analysis but **cannot restore an interrupted film to its uninterrupted state**: “freeze–thaw” is best interpreted as reallocating attention among continuously running specimens, unless pause/resume is experimentally validated. Film breakdown can also invalidate an assumed monotonic learning-curve shape. **[CITE] [NUMBERS] [GAP]** (lee2026costsensitivefreezethawbayesian pages 1-2, domhan2015speedingupautomatic pages 1-2, dogan2021bayesianmachinelearning pages 6-7)

4. **Make stopping explicitly cost-sensitive.** Zhongxiang Dai, Haibin Yu, Bryan Kian Hsiang Low and Patrick Jaillet, “Bayesian Optimization Meets Bayesian Optimal Stopping,” *Proceedings of ICML* **97** (2019) (**no DOI verified here**), combines GP-UCB choice of a configuration with a Bayesian decision at each subsequent epoch: stop because the completed outcome is unlikely to beat the incumbent, or pay to continue. Its loss includes erroneous stopping and continuation cost; an additional posterior-uncertainty condition guards against premature elimination. This is **stopping one evaluation**, not stopping the whole research program. Dong Bok Lee *et al.*, “Cost-Sensitive Freeze-thaw Bayesian Optimization for Efficient Hyperparameter Tuning,” NeurIPS 2025 preprint, **DOI: 10.48550/arXiv.2510.21379**, instead incorporates user cost–performance utility when allocating further training *and* stopping the overall search. Neither supplies validated seawater stopping thresholds. **[CITE] [GAP]** (dai2019bayesianoptimizationmeets pages 1-2, dai2019bayesianoptimizationmeets pages 3-4, lee2026costsensitivefreezethawbayesian pages 1-2)

5. **Dispatch a new test while others remain pending.** Ahsan S. Alvi, Binxin Ru, Jan Calliess, Stephen J. Roberts and Michael A. Osborne, “Asynchronous Batch Bayesian Optimisation with Improved Local Penalisation,” *Proceedings of ICML* **97** (2019), preprint **DOI: 10.48550/arXiv.1901.10452**, assigns work immediately to a freed worker and penalizes acquisitions near busy candidate locations; its underlying local-penalization approach is Javier González, Zhenwen Dai, Philipp Hennig and Neil D. Lawrence, “Batch Bayesian Optimization via Local Penalization,” *Proceedings of AISTATS* (2016), 648–657, preprint **DOI: 10.48550/arXiv.1505.08052**. Alternatively, **fantasies** sample unknown outcomes at pending locations and average decisions over them. Maximilian Balandat *et al.*, “BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization” (2020), preprint **DOI: 10.48550/arXiv.1910.06403**, describes joint noisy expected improvement with pending locations and posterior-fantasy updates. This solves scheduling and duplicate selection; **pending-point handling alone does not use the measurements accumulating inside a pending vessel**. **[CITE] [GAP]** (gonzalez2016batchbayesianoptimization pages 1-2, gonzalez2016batchbayesianoptimization pages 3-5, alvi2019asynchronousbatchbayesian pages 1-2, alvi2019asynchronousbatchbayesian pages 3-5, balandat2019botorchprogrammablebayesian pages 6-7)

6. **Learn from delayed but progressive outcomes.** Thomas M. McDonald, Lucas Maystre, Mounia Lalmas, Daniel Russo and Kamil Ciosek, “Impatient Bandits: Optimizing Recommendations for the Long-Term Without Delay,” *Proceedings of KDD* (2023), 1687–1697, **DOI: 10.1145/3580305.3599386**; expanded treatment by Kelly W. Zhang *et al.*, “Impatient Bandits: Optimizing for the Long-Term Without Delay” (2025), preprint **DOI: 10.48550/arXiv.2501.07761**. Bayesian filtering combines early and complete observations while Thompson sampling chooses new arms without awaiting the weeks-later reward. The demonstrated application is **two-month podcast engagement**, not corrosion. This distinction matters: a running coupon with day-1 EIS is *partially observed*, not an outcome-free pending point. **[CITE] [GAP]** (zhang2025impatientbanditsoptimizing pages 1-3, zhang2025impatientbanditsoptimizing pages 3-5)

7. **Preserve the linked experimental pipeline.** Raul Astudillo and Peter I. Frazier, “Bayesian Optimization of Function Networks,” *NeurIPS* (2021), preprint **DOI: 10.48550/arXiv.2112.15311**, learns separate models for network nodes and exploits intermediate outputs rather than fitting only the final score. Shunya Kusakawa *et al.*, “Bayesian Optimization for Cascade-Type Multistage Processes,” *Neural Computation* **34** (2022), 2408–2431, **DOI: 10.1162/neco_a_01550**, adds decisions after an intermediate stage and a *suspension* formulation with stage costs. Its demonstration involves solar-cell simulation and synthetic cascades, **not copper corrosion**. Neither citation, alone, establishes an off-the-shelf optimizer jointly handling pre-alloyed powder production, ongoing immersion traces, pending vessels and candidate-specific stop/start decisions. **[CITE] [GAP]** (kusakawa2022bayesianoptimizationfor pages 3-5, astudillo2021bayesianoptimizationof pages 1-2, kusakawa2022bayesianoptimizationfor pages 11-13)

## Directly relevant corrosion and alloy evidence

8. **Actual BO of copper corrosion protection, but not bulk alloy design.** Gül Dogan *et al.*, “Bayesian Machine Learning for Efficient Minimization of Defects in ALD Passivation Layers,” *ACS Applied Materials & Interfaces* **13** (2021), 54503–54515, **DOI: 10.1021/acsami.1c14586**. **Process:** atomic-layer-deposited Al₂O₃ on electrodeposited **99.999%-pure Cu**, approximately 1.5 μm thick—not DED. **Tests:** defect-revealing **40 vol% nitric acid, 30 minutes**, *separate from* polarization in **0.1 M NaCl**; neither is seawater. At 300 °C/60 ms precursor pulse/5-minute plasma pretreatment, reported *i*₍corr₎ is **9.00 × 10⁻¹¹ A cm⁻²**, versus **1.50 × 10⁻⁵ A cm⁻²** for bare Cu; reported electrochemical coating porosity is **0.0007%**. BO reached its etched-area target in two or three iterations of each initialized search. **These porosity figures describe an ALD film, not DED-deposit density.** Powder size, Hall flow, oxygen and bulk tensile properties: not applicable. **[CITE] [NUMBERS] [GAP]** (dogan2021bayesianmachinelearning pages 6-7, dogan2021bayesianmachinelearning pages 8-9, dogan2021bayesianmachinelearning pages 9-10)

9. **Thirty-day, composition-resolved NAB benchmark—not AM or BO.** Yinxun Tan *et al.*, “Effect of Al/Ni Ratio on the Microstructure and Properties of Nickel–Aluminum Bronze Alloys,” *Materials* **17** (2024), 1330, **DOI: 10.3390/ma17061330**. **Process:** vacuum-induction **cast** alloy, as cast; **test:** static **3.5 wt% NaCl**, **25 °C**, **30 days**, solution changed weekly—not ASTM D1141 or natural seawater. Measured compositions below are **wt%**, Cu balance; *E*₍corr₎ is versus Ag/AgCl. These results directly demonstrate that reducing Ni by raising Al can worsen the corrosion–ductility balance. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK: composition variation and 30-day NAB testing already exist, but not the proposed powder-DED decision pipeline]** (tan2024effectofalni pages 10-12, tan2024effectofalni pages 1-2, tan2024effectofalni pages 2-4, tan2024effectofalni pages 4-6)

   | Cast NAB: Al/Ni/Fe/Mn, wt%; Cu balance | 30-day *i*₍corr₎, μA cm⁻² | 30-day *E*₍corr₎, mV | 30-day Tafel *R*ₚ, kΩ cm² |
   |---|---:|---:|---:|
   | 6.94/6.82/4.10/1.72 | 0.35 | −281.48 | 173.48 |
   | 7.90/6.13/3.92/2.12 | 0.36 | −295.55 | 100.12 |
   | 8.94/5.18/4.12/2.18 | 0.69 | −249.35 | 54.41 |
   | 9.94/3.99/3.94/1.82 | 0.78 | −257.75 | 54.04 |

   Across the first-to-last composition, **hardness 104→202 HV**, **ultimate tensile strength 356→751 MPa**, and **elongation 50.50→11.00%**; the highest-Ni alloy’s reported 30-day **mass-loss rate is 0.00267 mm/year**. These values are for *cast NAB*, **not** wrought C71500 and **not** powder DED. **[NUMBERS]** (tan2024effectofalni pages 10-12, tan2024effectofalni pages 1-2, tan2024effectofalni pages 2-4)

10. **As-deposited marine-alloy comparator with a different feedstock.** Lamei Zhang, Xiaoyu Cai, Baiyu Song, Bolun Dong, Sanbao Lin and Fuad Khoshnaw, “Effect of low-level Ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of WAAM-processed nickel-aluminium bronze,” *Advanced Materials Joining* **1** (2026), article 17, **DOI: 10.1007/s44500-026-00016-x**. **Process:** cold-metal-transfer **wire-arc DED/WAAM** using NAB wire and *interlayer-applied Ti nanoparticle solution*—neither laser powder DED nor one pre-alloyed powder. Reported wire chemistry lists Al **8.73**, Ni **4.28**, Fe **3.22**, Mn **1.44 wt%**; the paper prints “Mg: Bal.” for its balance element, an apparent inconsistency for NAB, so **do not silently relabel that entry as a measured Cu balance**. **Tests:** static room-temperature **3.5 wt% NaCl** for **7, 14 and 21 days**, plus polarization. Baseline/0.1-wt%-Ti *i*₍corr₎ = **10.06/8.49 μA cm⁻²**; *E*₍corr₎ = **−192.91/−188.57 mV versus SCE**. The 0.1%-Ti sample’s reported corrosion rate is **0.167 g m⁻² day⁻¹**, longitudinal **UTS 718.2 MPa**, **YS 372.5 MPa**, **elongation 28.0%**. The article reports observable phase-associated pits; it does **not** validate a 30-day C71500-equivalent result. **[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK: as-deposited composition modification and chloride corrosion of AM NAB, but different deposition and feedstock]** (zhang2026effectoflowlevel pages 1-2, zhang2026effectoflowlevel pages 11-13, zhang2026effectoflowlevel pages 2-4, zhang2026effectoflowlevel pages 13-16)

11. **Why a one-hour reading cannot simply stand in for exposure age.** Polyxeni Vourna, Aphrodite Ktena, Evangelos V. Hristoforou and Nikolaos D. Papadopoulos, “Assessment of Corrosion in Naval Steels Submerged in Artificial Seawater Utilizing a Magnetic Non-Destructive Sensor,” *Sensors* **25** (2025), 5015, **DOI: 10.3390/s25165015**. **Process/alloy:** commercial DH36 naval **wrought steel**, Fe balance, Mn **1.23**, Si **0.32**, C **0.17**, P **0.025**, S **0.1 wt%**; **not copper**. **Tests:** **static ASTM D1141 artificial seawater** at **7, 49 and 84 days**, solution refreshed every five days, alongside natural seawater exposure near Rafina; **no controlled continuous flow rate reported**. Fitted artificial-seawater EIS corrosion-layer resistance *R*꜀ at 7/49/84 days is **1,508/2,489/1,198 Ω**, respectively: protection grows then deteriorates. These **steel** resistances must not be used as NAB or Cu–Ni pass/fail values. The study illustrates why time should be modeled and why early and final responses require paired calibration. **[CITE] [NUMBERS] [NAVY] [GAP]** (vourna2025assessmentofcorrosion pages 1-2, vourna2025assessmentofcorrosion pages 3-6, vourna2025assessmentofcorrosion pages 14-15, vourna2025assessmentofcorrosion pages 6-8, vourna2025assessmentofcorrosion pages 8-11)

12. **Adjacent active-learning examples, with important limits.** Wanyu Wang *et al.*, “A physics-informed active learning framework for the inverse design of vacuum coatings,” *Friction* (2026), **DOI: 10.26599/FRICT.2026.9441292**, uses **magnetron-sputtered CoCrFeNi/Ti multilayers**, not bulk copper alloys or DED. The study optimized *process parameters*, assessed polarization in **35 g L⁻¹ NaCl**, and advanced from **five initial to eleven total coatings**; its highest reported hardness is approximately **13.4 GPa**. Neither a bulk film composition in wt% nor a numeric *i*₍corr₎ for the optimized sample was verified in the available main-text evidence. **[CITE] [NUMBERS] [GAP]** (wang2026aphysicsinformedactive pages 1-5, wang2026aphysicsinformedactive pages 19-22, wang2026aphysicsinformedactive pages 27-31)

   Aditya Sundar, Xingru Tan, Shanshan Hu and Michael C. Gao, “CALPHAD-based Bayesian optimization to accelerate alloy discovery for high-temperature applications,” *Journal of Materials Research* **40** (2025), 112–122, **DOI: 10.1557/s43578-024-01489-0**, optimizes *calculated* thermal expansion and σ-phase dissolution across Ni–Cr–Co–Al–Fe, finding target alloys after exploring **7%** of its computational composition space. **Process:** computation only; **no fabricated powder, deposit, seawater test or corrosion-rate measurement**. It establishes precedent for CALPHAD-plus-BO, not for DED-thermal-history validation or duration-aware copper corrosion. **[CITE] [NUMBERS] [GAP]** (sundar2025calphadbasedbayesianoptimization pages 1-2, sundar2025calphadbasedbayesianoptimization pages 4-5)

## Decision rule and evidentiary boundary

For each candidate, use its composition, *measured powder-lot properties*, DED/substrate and defect information, and one-hour electrochemical result to update a **calibrated joint posterior** for the *30-day outcome*. Compare the expected benefit of **starting that candidate’s immersion** with its incremental cost and the value of screening another candidate; for vessels already running, separately compare **continue, measure again, or stop**, incorporating their observed time traces and the cost of occupying a vessel. Condition new selections on pending tests through fantasies or a defensible local penalty. Keep an independent set of full-duration tests—including early-screen failures—to measure false-negative screening and late film failure. This is a proposed combination of published decision principles, **not a previously validated corrosion algorithm**. (hook2020bayesianscreeningmultitest pages 1-3, dai2019bayesianoptimizationmeets pages 3-4, balandat2019botorchprogrammablebayesian pages 6-7, hook2020bayesianscreeningmultitest pages 10-13, zhang2025impatientbanditsoptimizing pages 3-5)

**Unanswered in the verified literature:** no demonstrated probability that a **one-hour Cu–Ni or NAB electrochemical screen** predicts *that same* single-stream pre-alloyed powder laser-DED candidate’s **30-day** seawater corrosion or selective-attack depth; no defensible universal starting threshold; and no source-supported numeric **C71500 wrought reference**, matched seawater-flow benchmark, or linked powder **particle size, Hall flow, apparent density and oxygen** values for that complete comparison. The cast, WAAM, sputtered-film and steel figures above cannot fill those blanks. **[GAP]** (dogan2021bayesianmachinelearning pages 9-10, tan2024effectofalni pages 10-12, hook2020bayesianscreeningmultitest pages 10-13, zhang2026effectoflowlevel pages 13-16)

## Top 5 things the PI should know

1. **Use two-test Bayesian screening for the start/no-start decision**, with an explicitly nonlinear, empirically calibrated short-test→30-day model; it is the closest published method, **not** an existing copper-DED demonstration. (hook2020bayesianscreeningmultitest pages 1-3, hook2020bayesianscreeningmultitest pages 10-13)
2. **Add elapsed-duration fidelity and trace-aware value of information** for specimens already immersed; a cheap early measurement and an early immersion reading are different data-generating processes. (wu2020practicalmultifidelitybayesian pages 1-2, wu2020practicalmultifidelitybayesian pages 3-4)
3. **Separate three decisions:** start a new immersion, stop an individual immersion, and stop the *campaign*. BO-BOS addresses the second; cost-sensitive freeze–thaw can address the third; asynchronous pending-point BO allocates freed capacity. (dai2019bayesianoptimizationmeets pages 3-4, lee2026costsensitivefreezethawbayesian pages 1-2, balandat2019botorchprogrammablebayesian pages 6-7)
4. **Expect misleading early ranks:** the cast NAB study shows a measurable 30-day Ni/Al corrosion–mechanics trade-off, while time-resolved marine-steel EIS demonstrates that film protection can reverse. Neither establishes an early-screen threshold for deposited Cu alloys. (tan2024effectofalni pages 10-12, tan2024effectofalni pages 2-4, vourna2025assessmentofcorrosion pages 14-15)
5. **State the novelty narrowly and test it directly:** candidate-level, cost-aware promotion from electrochemistry to 30-day exposure, coupled to *one pre-alloyed powder stream*, as-deposited laser-DED self-build and repair interfaces, with prospective checks against a simultaneously tested wrought C71500 control. Existing BO coating studies, cast NAB compositions, WAAM microalloying and CALPHAD searches each cover only pieces. (dogan2021bayesianmachinelearning pages 1-2, zhang2026effectoflowlevel pages 2-4, tan2024effectofalni pages 2-4, sundar2025calphadbasedbayesianoptimization pages 1-2)

References

1. (hook2020bayesianscreeningmultitest pages 1-3): James Hook, Calum Hand, and Emma Whitfield. Bayesian screening: multi-test bayesian optimization applied to in silico material screening. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.2009.05418, doi:10.48550/arxiv.2009.05418. This article has 0 citations.

2. (dai2019bayesianoptimizationmeets pages 3-4): Z Dai, H Yu, BKH Low, and P Jaillet. Bayesian optimization meets bayesian optimal stopping. Unknown journal, 2019.

3. (balandat2019botorchprogrammablebayesian pages 6-7): Maximilian Balandat, Brian Karrer, Daniel R. Jiang, Samuel Daulton, Benjamin Letham, Andrew Gordon Wilson, and Eytan Bakshy. Botorch: a framework for efficient monte-carlo bayesian optimization. Text, Jan 2020. URL: https://doi.org/10.48550/arxiv.1910.06403, doi:10.48550/arxiv.1910.06403. This article has 2003 citations and is from a peer-reviewed journal.

4. (hook2020bayesianscreeningmultitest pages 10-13): James Hook, Calum Hand, and Emma Whitfield. Bayesian screening: multi-test bayesian optimization applied to in silico material screening. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.2009.05418, doi:10.48550/arxiv.2009.05418. This article has 0 citations.

5. (wu2020practicalmultifidelitybayesian pages 1-2): Jian Wu, Saul Toscano-Palmerin, Peter I. Frazier, and Andrew Gordon Wilson. Practical multi-fidelity bayesian optimization for hyperparameter tuning. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.1903.04703, doi:10.48550/arxiv.1903.04703. This article has 276 citations.

6. (wu2020practicalmultifidelitybayesian pages 3-4): Jian Wu, Saul Toscano-Palmerin, Peter I. Frazier, and Andrew Gordon Wilson. Practical multi-fidelity bayesian optimization for hyperparameter tuning. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.1903.04703, doi:10.48550/arxiv.1903.04703. This article has 276 citations.

7. (wu2020practicalmultifidelitybayesian pages 4-6): Jian Wu, Saul Toscano-Palmerin, Peter I. Frazier, and Andrew Gordon Wilson. Practical multi-fidelity bayesian optimization for hyperparameter tuning. Preprint, Jan 2020. URL: https://doi.org/10.48550/arxiv.1903.04703, doi:10.48550/arxiv.1903.04703. This article has 276 citations.

8. (klein2017fastbayesianhyperparameter pages 1-3): Aaron Klein, Stefan Falkner, Simon Bartels, Philipp Hennig, and Frank Hutter. Fast bayesian hyperparameter optimization on large datasets. Electronic Journal of Statistics, Jan 2017. URL: https://doi.org/10.1214/17-ejs1335si, doi:10.1214/17-ejs1335si. This article has 103 citations and is from a domain leading peer-reviewed journal.

9. (lee2026costsensitivefreezethawbayesian pages 1-2): Dong Bok Lee, Aoxuan Zhang, Byungjoo Kim, Junhyeon Park, Steven Adriaensen, Juho Lee, Sung Ju Hwang, and Hae Beom Lee. Cost-sensitive freeze-thaw bayesian optimization for efficient hyperparameter tuning. ArXiv, Oct 2026. URL: https://doi.org/10.48550/arxiv.2510.21379, doi:10.48550/arxiv.2510.21379. This article has 5 citations.

10. (domhan2015speedingupautomatic pages 1-2): T Domhan, JT Springenberg, and F Hutter. Speeding up automatic hyperparameter optimization of deep neural networks by extrapolation of learning curves. Unknown journal, 2015.

11. (dogan2021bayesianmachinelearning pages 6-7): Gül Dogan, Sinan O. Demir, Rico Gutzler, Herbert Gruhn, Cem B. Dayan, Umut T. Sanli, Christian Silber, Utku Culha, Metin Sitti, Gisela Schütz, Corinne Grévent, and Kahraman Keskinbora. Bayesian machine learning for efficient minimization of defects in ald passivation layers. ACS Applied Materials & Interfaces, 13:54503-54515, Nov 2021. URL: https://doi.org/10.1021/acsami.1c14586, doi:10.1021/acsami.1c14586. This article has 39 citations and is from a domain leading peer-reviewed journal.

12. (dai2019bayesianoptimizationmeets pages 1-2): Z Dai, H Yu, BKH Low, and P Jaillet. Bayesian optimization meets bayesian optimal stopping. Unknown journal, 2019.

13. (gonzalez2016batchbayesianoptimization pages 1-2): Javier González, Zhenwen Dai, Philipp Hennig, and Neil D. Lawrence. Batch bayesian optimization via local penalization. Preprint, Jan 2016. URL: https://doi.org/10.48550/arxiv.1505.08052, doi:10.48550/arxiv.1505.08052. This article has 3 citations.

14. (gonzalez2016batchbayesianoptimization pages 3-5): Javier González, Zhenwen Dai, Philipp Hennig, and Neil D. Lawrence. Batch bayesian optimization via local penalization. Preprint, Jan 2016. URL: https://doi.org/10.48550/arxiv.1505.08052, doi:10.48550/arxiv.1505.08052. This article has 3 citations.

15. (alvi2019asynchronousbatchbayesian pages 1-2): Ahsan S. Alvi, Binxin Ru, Jan Calliess, Stephen J. Roberts, and Michael A. Osborne. Asynchronous batch bayesian optimisation with improved local penalisation. Preprint, Jan 2019. URL: https://doi.org/10.48550/arxiv.1901.10452, doi:10.48550/arxiv.1901.10452. This article has 88 citations.

16. (alvi2019asynchronousbatchbayesian pages 3-5): Ahsan S. Alvi, Binxin Ru, Jan Calliess, Stephen J. Roberts, and Michael A. Osborne. Asynchronous batch bayesian optimisation with improved local penalisation. Preprint, Jan 2019. URL: https://doi.org/10.48550/arxiv.1901.10452, doi:10.48550/arxiv.1901.10452. This article has 88 citations.

17. (zhang2025impatientbanditsoptimizing pages 1-3): Kelly W. Zhang, Thomas Baldwin-McDonald, Kamil Ciosek, Lucas Maystre, and Daniel Russo. Impatient bandits: optimizing for the long-term without delay. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2501.07761, doi:10.48550/arxiv.2501.07761. This article has 5 citations.

18. (zhang2025impatientbanditsoptimizing pages 3-5): Kelly W. Zhang, Thomas Baldwin-McDonald, Kamil Ciosek, Lucas Maystre, and Daniel Russo. Impatient bandits: optimizing for the long-term without delay. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2501.07761, doi:10.48550/arxiv.2501.07761. This article has 5 citations.

19. (kusakawa2022bayesianoptimizationfor pages 3-5): Shunya Kusakawa, Shion Takeno, Yu Inatsu, Kentaro Kutsukake, Shogo Iwazaki, Takashi Nakano, Toru Ujihara, Masayuki Karasuyama, and Ichiro Takeuchi. Bayesian optimization for cascade-type multistage processes. Neural Computation, 34:2408-2431, Nov 2022. URL: https://doi.org/10.1162/neco\_a\_01550, doi:10.1162/neco\_a\_01550. This article has 31 citations and is from a highest quality peer-reviewed journal.

20. (astudillo2021bayesianoptimizationof pages 1-2): Raul Astudillo and Peter I. Frazier. Bayesian optimization of function networks. Preprint, Jan 2021. URL: https://doi.org/10.48550/arxiv.2112.15311, doi:10.48550/arxiv.2112.15311. This article has 84 citations.

21. (kusakawa2022bayesianoptimizationfor pages 11-13): Shunya Kusakawa, Shion Takeno, Yu Inatsu, Kentaro Kutsukake, Shogo Iwazaki, Takashi Nakano, Toru Ujihara, Masayuki Karasuyama, and Ichiro Takeuchi. Bayesian optimization for cascade-type multistage processes. Neural Computation, 34:2408-2431, Nov 2022. URL: https://doi.org/10.1162/neco\_a\_01550, doi:10.1162/neco\_a\_01550. This article has 31 citations and is from a highest quality peer-reviewed journal.

22. (dogan2021bayesianmachinelearning pages 8-9): Gül Dogan, Sinan O. Demir, Rico Gutzler, Herbert Gruhn, Cem B. Dayan, Umut T. Sanli, Christian Silber, Utku Culha, Metin Sitti, Gisela Schütz, Corinne Grévent, and Kahraman Keskinbora. Bayesian machine learning for efficient minimization of defects in ald passivation layers. ACS Applied Materials & Interfaces, 13:54503-54515, Nov 2021. URL: https://doi.org/10.1021/acsami.1c14586, doi:10.1021/acsami.1c14586. This article has 39 citations and is from a domain leading peer-reviewed journal.

23. (dogan2021bayesianmachinelearning pages 9-10): Gül Dogan, Sinan O. Demir, Rico Gutzler, Herbert Gruhn, Cem B. Dayan, Umut T. Sanli, Christian Silber, Utku Culha, Metin Sitti, Gisela Schütz, Corinne Grévent, and Kahraman Keskinbora. Bayesian machine learning for efficient minimization of defects in ald passivation layers. ACS Applied Materials & Interfaces, 13:54503-54515, Nov 2021. URL: https://doi.org/10.1021/acsami.1c14586, doi:10.1021/acsami.1c14586. This article has 39 citations and is from a domain leading peer-reviewed journal.

24. (tan2024effectofalni pages 10-12): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

25. (tan2024effectofalni pages 1-2): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

26. (tan2024effectofalni pages 2-4): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

27. (tan2024effectofalni pages 4-6): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

28. (zhang2026effectoflowlevel pages 1-2): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

29. (zhang2026effectoflowlevel pages 11-13): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

30. (zhang2026effectoflowlevel pages 2-4): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

31. (zhang2026effectoflowlevel pages 13-16): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

32. (vourna2025assessmentofcorrosion pages 1-2): Polyxeni Vourna, Aphrodite Ktena, Evangelos V. Hristoforou, and Nikolaos D. Papadopoulos. Assessment of corrosion in naval steels submerged in artificial seawater utilizing a magnetic non-destructive sensor. Sensors, 25:5015, Aug 2025. URL: https://doi.org/10.3390/s25165015, doi:10.3390/s25165015. This article has 12 citations and is from a peer-reviewed journal.

33. (vourna2025assessmentofcorrosion pages 3-6): Polyxeni Vourna, Aphrodite Ktena, Evangelos V. Hristoforou, and Nikolaos D. Papadopoulos. Assessment of corrosion in naval steels submerged in artificial seawater utilizing a magnetic non-destructive sensor. Sensors, 25:5015, Aug 2025. URL: https://doi.org/10.3390/s25165015, doi:10.3390/s25165015. This article has 12 citations and is from a peer-reviewed journal.

34. (vourna2025assessmentofcorrosion pages 14-15): Polyxeni Vourna, Aphrodite Ktena, Evangelos V. Hristoforou, and Nikolaos D. Papadopoulos. Assessment of corrosion in naval steels submerged in artificial seawater utilizing a magnetic non-destructive sensor. Sensors, 25:5015, Aug 2025. URL: https://doi.org/10.3390/s25165015, doi:10.3390/s25165015. This article has 12 citations and is from a peer-reviewed journal.

35. (vourna2025assessmentofcorrosion pages 6-8): Polyxeni Vourna, Aphrodite Ktena, Evangelos V. Hristoforou, and Nikolaos D. Papadopoulos. Assessment of corrosion in naval steels submerged in artificial seawater utilizing a magnetic non-destructive sensor. Sensors, 25:5015, Aug 2025. URL: https://doi.org/10.3390/s25165015, doi:10.3390/s25165015. This article has 12 citations and is from a peer-reviewed journal.

36. (vourna2025assessmentofcorrosion pages 8-11): Polyxeni Vourna, Aphrodite Ktena, Evangelos V. Hristoforou, and Nikolaos D. Papadopoulos. Assessment of corrosion in naval steels submerged in artificial seawater utilizing a magnetic non-destructive sensor. Sensors, 25:5015, Aug 2025. URL: https://doi.org/10.3390/s25165015, doi:10.3390/s25165015. This article has 12 citations and is from a peer-reviewed journal.

37. (wang2026aphysicsinformedactive pages 1-5): Wanyu Wang, Bowen Xu, Zhangli Hou, Zhen Li, Zhi-Yi Wang, Qi-Feng Cui, and Zhi-Nan Zhang. A physics-informed active learning framework for the inverse design of vacuum coatings. Friction, Jul 2026. URL: https://doi.org/10.26599/frict.2026.9441292, doi:10.26599/frict.2026.9441292. This article has 0 citations and is from a peer-reviewed journal.

38. (wang2026aphysicsinformedactive pages 19-22): Wanyu Wang, Bowen Xu, Zhangli Hou, Zhen Li, Zhi-Yi Wang, Qi-Feng Cui, and Zhi-Nan Zhang. A physics-informed active learning framework for the inverse design of vacuum coatings. Friction, Jul 2026. URL: https://doi.org/10.26599/frict.2026.9441292, doi:10.26599/frict.2026.9441292. This article has 0 citations and is from a peer-reviewed journal.

39. (wang2026aphysicsinformedactive pages 27-31): Wanyu Wang, Bowen Xu, Zhangli Hou, Zhen Li, Zhi-Yi Wang, Qi-Feng Cui, and Zhi-Nan Zhang. A physics-informed active learning framework for the inverse design of vacuum coatings. Friction, Jul 2026. URL: https://doi.org/10.26599/frict.2026.9441292, doi:10.26599/frict.2026.9441292. This article has 0 citations and is from a peer-reviewed journal.

40. (sundar2025calphadbasedbayesianoptimization pages 1-2): Aditya Sundar, Xingru Tan, Shanshan Hu, and Michael C. Gao. Calphad-based bayesian optimization to accelerate alloy discovery for high-temperature applications. Journal of Materials Research, 40:112-122, Jan 2025. URL: https://doi.org/10.1557/s43578-024-01489-0, doi:10.1557/s43578-024-01489-0. This article has 19 citations and is from a peer-reviewed journal.

41. (sundar2025calphadbasedbayesianoptimization pages 4-5): Aditya Sundar, Xingru Tan, Shanshan Hu, and Michael C. Gao. Calphad-based bayesian optimization to accelerate alloy discovery for high-temperature applications. Journal of Materials Research, 40:112-122, Jan 2025. URL: https://doi.org/10.1557/s43578-024-01489-0, doi:10.1557/s43578-024-01489-0. This article has 19 citations and is from a peer-reviewed journal.

42. (dogan2021bayesianmachinelearning pages 1-2): Gül Dogan, Sinan O. Demir, Rico Gutzler, Herbert Gruhn, Cem B. Dayan, Umut T. Sanli, Christian Silber, Utku Culha, Metin Sitti, Gisela Schütz, Corinne Grévent, and Kahraman Keskinbora. Bayesian machine learning for efficient minimization of defects in ald passivation layers. ACS Applied Materials & Interfaces, 13:54503-54515, Nov 2021. URL: https://doi.org/10.1021/acsami.1c14586, doi:10.1021/acsami.1c14586. This article has 39 citations and is from a domain leading peer-reviewed journal.
