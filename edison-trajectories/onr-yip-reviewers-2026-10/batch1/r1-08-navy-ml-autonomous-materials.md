<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: 8bd7b931-a979-4239-9eaa-debbc9977e60
- Submitted: 2026-10-24T05:26:01Z
- Fetched: 2026-10-24T05:59:16Z (status: success)
- Raw trajectory JSON: not committed here (see ../README.md); r1-08-navy-ml-autonomous-materials.json.gz in the agent-staging drop
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal for the Materials &
Processes for Additive Manufacturing program (ONR Code 332). The work designs
new pre-alloyed copper alloy powders for single-stream blown-powder laser
directed energy deposition (DED). Goals: deposits that are dense and
crack-free, both built on themselves and deposited on cast nickel-aluminum
bronze (NAB) and wrought Cu-Ni (repair), and that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe, Mn, Cr; aluminum
bronzes / NAB with Ni, Fe, Mn. Lower nickel content is a secondary objective.
Powder is made in-house by ultrasonic atomization. Method: composition ->
powder -> DED deposit -> microstructure -> corrosion/hardness is a network of
linked models searched by cost-aware Bayesian optimization (cheap steps such
as CALPHAD, pre-placed powder tracks and one-hour electrochemical screens are
run more often than expensive ones such as 2 kg blown-powder builds and
30-day immersion). CALPHAD is evaluated along a heat-flow model of the DED
thermal history. Purchased DED sessions run at outside facilities.

QUESTION: Which Navy and ONR-funded researchers have published on machine
learning, Bayesian optimization, active learning, autonomous or
high-throughput experimentation for alloy design, additive manufacturing
process development, or corrosion prediction since 2018 (including NRL,
NSWC and ONR-funded university groups)? A reviewer from this group will
judge the method: cost-aware Bayesian optimization of a network of linked
models with steps of different costs and durations. What have these groups
already shown, what would they consider new, and what benchmarks or
baselines would they expect the proposal to report?

OUTPUT FORMAT: First, a short profile built only from the published record
(papers, technical reports, conference talks, program pages): positions and
affiliations with years, main research topics, methods, and recurring
co-authors. Then the publications most relevant to the proposal, each with a
full citation and DOI and one line on what it found. Then 3-6 numbered
IMPLICATIONS for the proposal: what this reader is likely to value, what they
would probe or doubt, which of their own results the proposal should cite or
build on, and wording or framing that would land well or badly with them.
Tag claims that rest on a single source or on a program web page rather than
a peer-reviewed paper. If the record is thin or a name is ambiguous (several
people share it), say so plainly instead of guessing, and do not invent
affiliations, titles or papers.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal for the Materials &
Processes for Additive Manufacturing program (ONR Code 332). The work designs
new pre-alloyed copper alloy powders for single-stream blown-powder laser
directed energy deposition (DED). Goals: deposits that are dense and
crack-free, both built on themselves and deposited on cast nickel-aluminum
bronze (NAB) and wrought Cu-Ni (repair), and that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe, Mn, Cr; aluminum
bronzes / NAB with Ni, Fe, Mn. Lower nickel content is a secondary objective.
Powder is made in-house by ultrasonic atomization. Method: composition ->
powder -> DED deposit -> microstructure -> corrosion/hardness is a network of
linked models searched by cost-aware Bayesian optimization (cheap steps such
as CALPHAD, pre-placed powder tracks and one-hour electrochemical screens are
run more often than expensive ones such as 2 kg blown-powder builds and
30-day immersion). CALPHAD is evaluated along a heat-flow model of the DED
thermal history. Purchased DED sessions run at outside facilities.

QUESTION: Which Navy and ONR-funded researchers have published on machine
learning, Bayesian optimization, active learning, autonomous or
high-throughput experimentation for alloy design, additive manufacturing
process development, or corrosion prediction since 2018 (including NRL,
NSWC and ONR-funded university groups)? A reviewer from this group will
judge the method: cost-aware Bayesian optimization of a network of linked
models with steps of different costs and durations. What have these groups
already shown, what would they consider new, and what benchmarks or
baselines would they expect the proposal to report?

OUTPUT FORMAT: First, a short profile built only from the published record
(papers, technical reports, conference talks, program pages): positions and
affiliations with years, main research topics, methods, and recurring
co-authors. Then the publications most relevant to the proposal, each with a
full citation and DOI and one line on what it found. Then 3-6 numbered
IMPLICATIONS for the proposal: what this reader is likely to value, what they
would probe or doubt, which of their own results the proposal should cite or
build on, and wording or framing that would land well or badly with them.
Tag claims that rest on a single source or on a program web page rather than
a peer-reviewed paper. If the record is thin or a name is ambiguous (several
people share it), say so plainly instead of guessing, and do not invent
affiliations, titles or papers.


## Published-record profile

**Most directly documented Navy connection.** Patrick G. Callahan was identified in a **2022** publication as a researcher in the Materials Science and Technology Division of the **U.S. Naval Research Laboratory (NRL)**. He and Andrew T. Polonsky edited a *JOM* topic on autonomous data collection and active learning; Polonsky was at **Sandia National Laboratories**, not NRL. Their editorial explicitly acknowledges NRL support under ONR auspices, but reports other groups’ studies rather than a Callahan-led experimental campaign. Recurring collaborators or a later position for Callahan cannot be established from this record. (polonsky2022applicationsofautonomous pages 1-2)

**Closest ONR-funded corrosion/active-learning cluster.** In **2023–2024**, John R. Scully and Debashish Sur were listed at the **University of Virginia**; Jason Hattrick-Simpers and Kangming Li at the **University of Toronto**; and Howie Joress and Brian DeCost at **NIST** in the relevant publications. Recurring combinations include Scully–Sur–Hattrick-Simpers, Joress–DeCost–Hattrick-Simpers, and Runze Zhang–Li–Scully–Hattrick-Simpers. Their methods span high-throughput electrochemistry, Gaussian-process active learning of corrosion responses, and Bayesian interpretation of impedance spectra. The Sur and Zhang papers explicitly acknowledge **ONR MURI N00014-20-1-2368**; NIST employment or coauthorship alone does *not* establish ONR funding for every NIST paper. Their published corrosion screens use particular alloy libraries and electrolytes, not demonstrations of as-deposited DED copper outperforming wrought C71500 in seawater. (decost2022towardsautomateddesign pages 1-4, sur2023ahighthroughput pages 1-2, sur2023ahighthroughput pages 6-7, zhang2024anassessmentof pages 1-5, zhang2023editors’choice—autoeisautomated pages 23-28)

**Relevant ONR-supported AM/modeling cluster.** A **2019** paper lists Abdalla R. Nassar at **Penn State’s Applied Research Laboratory** and Mohammad Montazeri and Prahalada Rao at the **University of Nebraska–Lincoln**. Its acknowledgment assigns ONR support to work at Penn State and NSF support for Rao’s spectral-graph-modeling contribution: it should **not** be described as wholly ONR-funded. A **2021** paper by Robert Saunders, Celia Butler, John Michopoulos, Dimitris Lagoudas, Alaa Elwany and Amit Bagchi acknowledges ONR support through **NRL core funding**; it models AM microstructure–mechanical-response links using functional Gaussian processes, rather than optimizing corrosion. [Single-paper evidence for each funding attribution.] (montazeri2019inprocessmonitoringof pages 1-5, saunders2021mechanicalbehaviorpredictions pages 11-11, montazeri2019inprocessmonitoringof pages 30-33)

**Methodological comparators, not automatically Navy-funded reviewers.** Kristofer G. Reyes (**University at Buffalo**, 2022) and Jiaqian Liu and Carlos Juan Díaz Vargas published the particularly pertinent multistage-screening benchmark, but its acknowledgment names **NSF and Brookhaven LDRD, not ONR**. Peter C. Collins and Thomas K. Ales (**Iowa State University**, 2026) published an *aspirational* autonomous-AM laboratory design with an imagined naval-brass/DED/erosion-corrosion case study; this is not an accomplished naval-brass experiment or evidence of ONR funding. Benji Maruyama’s published **2022** affiliation was the **Air Force Research Laboratory**, not NRL; Hattrick-Simpers was at Toronto. The reviewed record does not securely identify an **NSWC-based author** of a directly comparable cost-aware, linked-model BO study. None of these publications identifies an actual proposal reviewer. (maruyama2022artificialintelligencefor pages 1-2, reyes2022decisionmakingunderuncertainty pages 1-3, reyes2022decisionmakingunderuncertainty pages 16-19, collins2026additivemanufacturingenabled pages 1-2, collins2026additivemanufacturingenabled pages 18-20)

## Publications to cite or distinguish

1. **A. T. Polonsky and P. G. Callahan**, “Applications of Autonomous Data Collection and Active Learning,” *JOM* **74**, 2895–2896 (2022). **DOI: 10.1007/s11837-022-05374-1.** NRL-connected **editorial**, not a new experimental result; highlights both autonomous corrosion screening and rigorous multistage-screening tests. (polonsky2022applicationsofautonomous pages 1-2)
2. **B. DeCost, H. Joress, S. Sarker, A. Mehta and J. Hattrick-Simpers**, “Towards Automated Design of Corrosion Resistant Alloy Coatings with an Autonomous Scanning Droplet Cell,” *JOM* **74**, 2941–2950 (2022). **DOI: 10.1007/s11837-022-05367-0.** Demonstrated an automated electrochemical platform; its Al–Ni–Ti multiobjective active-learning convergence was evaluated by **simulation on measured/interpolated data**, and its Ti–Nb–Ta analysis linked composition, structure and corrosion. Do not present the simulation as a seawater-validated autonomous DED campaign. (decost2022towardsautomateddesign pages 4-7, decost2022towardsautomateddesign pages 1-4, decost2022towardsautomateddesign pages 7-10)
3. **K. G. Reyes, J. Liu and C. J. Díaz Vargas**, “Decision-Making Under Uncertainty for Multi-stage Pipelines: Simulation Studies to Benchmark Screening Strategies,” *JOM* **74**, 2897–2907 (2022). **DOI: 10.1007/s11837-022-05368-z.** Under simulated stage-dependent covariance, a seemingly sensible screening funnel **sometimes underperformed random selection**. **Not verified as ONR-funded.** (reyes2022decisionmakingunderuncertainty pages 1-3, reyes2022decisionmakingunderuncertainty pages 13-16, reyes2022decisionmakingunderuncertainty pages 16-19, reyes2022decisionmakingunderuncertainty media 4d2684c2)
4. **D. Sur, H. Joress, J. Hattrick-Simpers and J. R. Scully**, “A High Throughput Aqueous Passivation Testing Methodology for Compositionally Complex Alloys Using a Scanning Droplet Cell,” *Journal of The Electrochemical Society* **170**, 081507 (2023). **DOI: 10.1149/1945-7111/aceeb8.** ONR-MURI-supported rapid impedance/polarization screening resolved composition-dependent passivation in an Al–Co–Cr–Fe–Ni library; leading candidates did **not** match the reported 316L comparison on all metrics. Its **acidic sulfate** test is not a seawater Cu-alloy performance baseline. (sur2023ahighthroughput pages 1-2, sur2023ahighthroughput pages 6-7, sur2023ahighthroughput pages 4-6)
5. **R. Zhang, R. Black, D. Sur, P. Karimi, K. Li, B. DeCost, J. R. Scully and J. Hattrick-Simpers**, “Editors’ Choice—AutoEIS: Automated Bayesian Model Selection and Analysis for Electrochemical Impedance Spectroscopy,” *Journal of The Electrochemical Society* **170**, 086502 (2023). **DOI: 10.1149/1945-7111/aceab2.** ONR-MURI-acknowledged software produced statistically assessed equivalent circuits competitive with expert choices across three electrochemical applications, including alloy corrosion; it does **not** directly predict immersion lifetime. (zhang2023editors’choice—autoeisautomated pages 1-5, zhang2023editors’choice—autoeisautomated pages 23-28)
6. **R. Zhang, D. Sur, K. Li, J. Witt, R. Black, A. Whittingham, J. R. Scully and J. Hattrick-Simpers**, “Bayesian Assessment of Commonly Used Equivalent Circuit Models for Corrosion Analysis in Electrochemical Impedance Spectroscopy,” *npj Materials Degradation* **8**, 120 (2024). **DOI: 10.1038/s41529-024-00537-8.** ONR-MURI-acknowledged analysis of simulated spectra identified when a circuit was unidentifiable and when shorter frequency sweeps preserved reliable parameter estimates. **Single-study quantitative example:** for a selected simulated coated-metal case, omitting measurements below 0.018 Hz yielded less than 4% error in a reported parameter and over 94% less acquisition time; this is not a general validated time saving for DED seawater coupons. (zhang2024bayesianassessmentof pages 1-2, zhang2024anassessmentof pages 14-19)
7. **M. Montazeri, A. R. Nassar, A. J. Dunbar and P. Rao**, “In-process Monitoring of Porosity in Additive Manufacturing Using Optical Emission Spectroscopy,” *IISE Transactions* **52**, 500–515 (2020; online 2019). **DOI: 10.1080/24725854.2019.1659525.** Partially ONR-supported Penn State work used optical signatures and CT ground truth to predict layerwise porosity of laser-powder-bed-fused alloy 718; it compared graph-derived features with simpler statistical features. **Different AM process from blown-powder DED.** (montazeri2019inprocessmonitoringof pages 1-5, montazeri2019inprocessmonitoringof pages 30-33)
8. **R. Saunders, C. Butler, J. Michopoulos, D. Lagoudas, A. Elwany and A. Bagchi**, “Mechanical Behavior Predictions of Additively Manufactured Microstructures Using Functional Gaussian Process Surrogates,” *npj Computational Materials* **7**, 81 (2021). **DOI: 10.1038/s41524-021-00548-y.** NRL/ONR-core-supported, directed microstructure-to-mechanical-response surrogate network learned from crystal-plasticity simulations; it was **not** a cost-scheduled experimental corrosion campaign. (saunders2021mechanicalbehaviorpredictions pages 9-10, saunders2021mechanicalbehaviorpredictions pages 11-11)
9. **X. Wang and W. Xiong**, “Uncertainty Quantification and Composition Optimization for Alloy Additive Manufacturing Through a CALPHAD-Based ICME Framework,” *npj Computational Materials* **6**, 188 (2020). **DOI: 10.1038/s41524-020-00454-9.** Screened approximately 450,000 modeled HSLA-steel compositions and reported a **44.7% increase in predicted successful-build probability** after composition optimization. **ONR support for this particular paper was not verified from the inspected acknowledgment; do not claim it without checking the published version.** (wang2020uncertaintyquantificationand pages 1-4)
10. **P. C. Collins and T. K. Ales**, “Additive Manufacturing Enabled Autonomous Laboratory for Materials Discovery and Concurrent Design of Materials and Shape,” *MRS Bulletin* **51**, 746–769 (2026). **DOI: 10.1557/s43577-026-01078-y.** A **perspective**, not validation: its explicit *hypothetical* naval-brass case already proposes DED, rapid surrogate tests, subsequent erosion-corrosion tests and human oversight. Thus that general workflow, by itself, is not a defensible first. (collins2026additivemanufacturingenabled pages 1-2, collins2026additivemanufacturingenabled pages 18-20, collins2026additivemanufacturingenabled pages 20-21)
11. **B. Maruyama, J. Hattrick-Simpers, W. Musinski, L. Graham-Brady, K. Li, J. Hollenbach, A. Singh and M. L. Taheri**, “Artificial Intelligence for Materials Research at Extremes,” *MRS Bulletin* **47**, 1154–1164 (2022). **DOI: 10.1557/s43577-022-00466-4.** **Perspective:** explicitly discusses the decision between fast, inexpensive and slow, expensive experiments, and demands validated uncertainty and attention to false acceptance/rejection. Do not attribute its authors collectively to the Navy. (maruyama2022artificialintelligencefor pages 1-2, maruyama2022artificialintelligencefor pages 5-7)

## Implications for the proposal

1. **State the novelty narrowly and experimentally.** Frame the contribution as *learning, calibrating and actively choosing among linked, unequal-cost composition→powder→DED→microstructure→corrosion decisions to obtain an as-deposited, substrate-compatible copper repair*, not as inventing autonomous alloy design, CALPHAD optimization, rapid electrochemistry or a naval-brass/DED concept. Collins and Ales already articulate the last concept, while DeCost and colleagues already demonstrate corrosion-oriented GP screening. The distinguishers require actual paired observations and final builds, not merely a workflow diagram. (collins2026additivemanufacturingenabled pages 1-2, collins2026additivemanufacturingenabled pages 18-20, decost2022towardsautomateddesign pages 4-7, decost2022towardsautomateddesign pages 7-10)

2. **Prove that cheap measurements predict the *right* expensive result.** Quantify stage-to-stage correlations **and conditional uncertainty**: CALPHAD versus powder chemistry; pre-placed tracks versus blown-powder bulk and repair-interface quality; one-hour electrochemistry versus **30-day seawater outcomes**. Reserve some full DED builds and immersion specimens for prospective, held-out testing. Report the fraction of desirable alloys rejected by each gate and false passes to costly builds: Reyes and colleagues showed why a funnel can otherwise do worse than random. Treat substrate, atomization batch and facility as possible transfer effects, rather than pooling them silently. (reyes2022decisionmakingunderuncertainty pages 1-3, reyes2022decisionmakingunderuncertainty pages 13-16, reyes2022decisionmakingunderuncertainty pages 16-19, reyes2022decisionmakingunderuncertainty media 4d2684c2, montazeri2019inprocessmonitoringof pages 30-33)

3. **Show the decision advantage under the real purchasing constraint.** Compare the complete policy with random/space-filling design, a fixed top-*k* funnel, conventional single-fidelity BO, and ablations lacking cross-stage dependence, cost awareness, physics inputs or crack-feasibility constraints. Use **identical starting data** and plot probability of finding an alloy satisfying *all* requirements, feasible Pareto performance, false-reject rate and uncertainty calibration against **dollars, elapsed time and number of purchased DED sessions**—not iterations alone. The cited corrosion platform already used multiobjective GP acquisition; a novelty claim requires demonstrating incremental value beyond it. (decost2022towardsautomateddesign pages 4-7, decost2022towardsautomateddesign pages 7-10, reyes2022decisionmakingunderuncertainty pages 1-3, hickman2023olympusenhancedbenchmarking pages 10-12)

4. **Keep corrosion endpoints and comparators honest.** Assess final **as-deposited** candidates on self-builds and separately on cast NAB and wrought Cu–Ni substrates, against contemporaneously tested **wrought C71500** under the *same specified seawater conditions*. Distinguish uniform loss, localized attack and repair-interface behavior; electrochemical surrogate metrics and acid-sulfate passivation cannot establish the 30-day seawater requirement. Justify the one-hour assay’s informativeness empirically; Zhang and colleagues’ faster-EIS result establishes a way to check information loss, not permission to assume every shortened assay predicts long-term service. [The exact proposed acceptance tests are recommendations inferred from the cited limitations, not previously published results.] (sur2023ahighthroughput pages 1-2, sur2023ahighthroughput pages 4-6, zhang2024bayesianassessmentof pages 1-2, zhang2024anassessmentof pages 14-19)

5. **Use probabilistic physics without overclaiming autonomy.** CALPHAD evaluated on modeled thermal histories is useful as an uncertain, testable input; the proposal should specify how thermal-history and thermodynamic error propagate into downstream recommendations, when an out-of-domain prediction triggers confirmation, and how failed powder or cracked builds are recorded. Call the execution a *human-supervised, cost-aware sequential campaign* if outside DED booking and immersion remain manual. ‘Fully autonomous’ or ‘first Navy AI-designed corrosion-resistant copper’ would clash with both the published definitions of autonomy and existing ONR-supported corrosion work. (stach2021autonomousexperimentationsystems pages 13-16, maruyama2022artificialintelligencefor pages 5-7, stach2021autonomousexperimentationsystems pages 2-3, sur2023ahighthroughput pages 6-7)

6. **Avoid invented reviewer identities.** The demonstrably Navy-connected experimental/technical record here is not evidence that Callahan, Scully, Nassar or any named person is assigned to review this proposal. Cite their *results and limitations*, distinguish NRL from ONR-funded universities, NIST and AFRL, and identify the NSWC-specific record as unresolved rather than assigning a plausible-sounding name. (polonsky2022applicationsofautonomous pages 1-2, decost2022towardsautomateddesign pages 1-4, reyes2022decisionmakingunderuncertainty pages 16-19, maruyama2022artificialintelligencefor pages 1-2)

For a compact list of **budget-matched baselines, ablations and validation endpoints**, the benchmark matrix below separates the proposed linked-model gain from gains due merely to more measurements or a permissive screening gate. (reyes2022decisionmakingunderuncertainty pages 1-3, reyes2022decisionmakingunderuncertainty pages 13-16)

| Benchmark or ablation | Same information available? | Cost/time accounted for? | Required comparison and metric | Why a Navy/ONR-informed reviewer would expect it |
|---|---:|---:|---|---|
| Random sampling and space-filling DOE | Yes | Report both fixed-campaign and matched-budget versions | Best feasible alloy versus cumulative dollars, calendar time, and expensive-build count; feasible-discovery probability over repeated seeded campaigns | Autonomous-experimentation studies benchmark against random or grid sampling, and reported acceleration can disappear without a matched baseline. CAMEO used one-tenth the grid measurements, while other work showed algorithmic sampling reaching random sampling’s coverage with far fewer experiments. (stach2021autonomousexperimentationsystems pages 13-16, stach2021autonomousexperimentationsystems pages 8-9) |
| Single-fidelity, ungated Bayesian optimization | Yes | No heterogeneous-cost correction | Regret or hypervolume versus cost; number of infeasible/cracked recommendations; calibration of predictive intervals | Tests whether value comes from the proposed cost-aware linked network rather than ordinary GP/BO. Corrosion work already demonstrated GP confidence-bound search and random scalarization for multi-objective optimization. (decost2022towardsautomateddesign pages 4-7, decost2022towardsautomateddesign pages 7-10) |
| Fixed funnel or top-*k* staged screening | Yes | Fixed allocation by stage | Final-stage success rate, false-negative rate at each gate, survivor enrichment, and cost per validated success | Stage-wise covariance can make a plausible screening pipeline worse than random; therefore gates and cheap surrogates cannot be assumed valid. (reyes2022decisionmakingunderuncertainty pages 1-3, reyes2022decisionmakingunderuncertainty pages 13-16, reyes2022decisionmakingunderuncertainty pages 16-19) |
| Multifidelity models with independent objectives or stages | Yes | Acquisition chooses fidelity but omits cross-stage network structure | Compare composition recommendations, high-fidelity regret, and uncertainty calibration; ablate learned cross-stage covariance and conditional dependence | Distinguishes a linked composition→powder→DED→microstructure→corrosion model from merely pooling cheap and expensive labels. Prior work specifically calls for cost–benefit decisions across experiments, simulations, and characterization of different fidelities. (stach2021autonomousexperimentationsystems pages 13-16, maruyama2022artificialintelligencefor pages 1-2) |
| Cost-aware linked-model BO **without feasibility constraints** | Yes | Yes | Crack/porosity failure rate, fraction of budget wasted, feasible hypervolume, and probability of meeting every requirement | Dense, crack-free deposition and substrate compatibility are constraints, not soft objectives; a method may improve corrosion predictions while repeatedly proposing unbuildable alloys. Constrained expected improvement has been benchmarked against Thompson sampling, UCB, and constrained probability of improvement for crack-free AM alloy selection. (talbot2026activelearningfor pages 19-24) |
| Full linked-model BO with constraints but **without physics-informed inputs** | Yes | Yes | Out-of-distribution error, physical-violation count, extrapolation performance, and final recommendation stability | Establishes the contribution of CALPHAD evaluated over thermal history rather than treating it as decorative feature engineering. Naval/DoD autonomous-materials reviews emphasize mechanistic models, uncertainty, and regular experimental grounding over black-box optimization. (stach2021autonomousexperimentationsystems pages 13-16, maruyama2022artificialintelligencefor pages 5-7) |
| Cheap electrochemical screen versus long immersion | Paired specimens required | Report hours and dollars separately | Rank correlation and calibration against 30-day mass loss/localized attack; false-pass and false-reject rates relative to C71500 | Fast corrosion measurements are useful only if they predict the service-relevant endpoint. Bayesian EIS work showed that acquisition time can be shortened substantially without losing parameter accuracy, but also supplied explicit posterior checks and validity limits. (zhang2024anassessmentof pages 14-19, zhang2024bayesianassessmentof pages 1-2) |
| Surrogate tracks/small coupons versus purchased blown-powder builds | Paired compositions and matched process descriptors required | Include queue delays, setup charges, powder mass, and build time | Transfer error for density, cracking, dilution, hardness, and corrosion; probability that a cheap-stage pass succeeds in a 2 kg build | Directly tests the most consequential cross-fidelity link. Existing ONR-supported AM work used CT-grounded defect labels and reported predictive error and classification performance rather than assuming sensor or coupon transfer. (montazeri2019inprocessmonitoringof pages 30-33) |
| Final physical validation on self-build, cast NAB, and wrought Cu–Ni substrates | Held-out confirmatory alloys; no model updating before scoring | Count every atomization batch and external DED session | Replicated density/crack criteria, hardness, 30-day seawater performance relative to wrought C71500, uncertainty intervals, and reproducibility across powder/build batches | The decisive benchmark is not surrogate regret but an as-deposited, feasible repair alloy that meets the stated Navy reference. Report negative results and stopping rules; autonomous-laboratory frameworks require explicit objectives, constraints, exit criteria, uncertainty, and human oversight. (collins2026additivemanufacturingenabled pages 1-2, collins2026additivemanufacturingenabled pages 18-20, collins2026additivemanufacturingenabled pages 20-21, stach2021autonomousexperimentationsystems pages 2-3) |


*Table: Evidence-backed benchmark matrix for isolating the value of cost-aware, constrained Bayesian optimization over a linked materials-process-corrosion network. It emphasizes budget-matched baselines, cross-stage validation, uncertainty calibration, and held-out physical confirmation.*

References

1. (polonsky2022applicationsofautonomous pages 1-2): Andrew T. Polonsky and Patrick G. Callahan. Applications of autonomous data collection and active learning. JOM, 74:2895-2896, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05374-1, doi:10.1007/s11837-022-05374-1. This article has 0 citations and is from a peer-reviewed journal.

2. (decost2022towardsautomateddesign pages 1-4): Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers. Towards automated design of corrosion resistant alloy coatings with an autonomous scanning droplet cell. JOM, 74:2941-2950, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05367-0, doi:10.1007/s11837-022-05367-0. This article has 29 citations and is from a peer-reviewed journal.

3. (sur2023ahighthroughput pages 1-2): Debashish Sur, Howie Joress, Jason Hattrick-Simpers, and John R. Scully. A high throughput aqueous passivation testing methodology for compositionally complex alloys using a scanning droplet cell. Journal of The Electrochemical Society, 170:081507, Aug 2023. URL: https://doi.org/10.1149/1945-7111/aceeb8, doi:10.1149/1945-7111/aceeb8. This article has 21 citations and is from a peer-reviewed journal.

4. (sur2023ahighthroughput pages 6-7): Debashish Sur, Howie Joress, Jason Hattrick-Simpers, and John R. Scully. A high throughput aqueous passivation testing methodology for compositionally complex alloys using a scanning droplet cell. Journal of The Electrochemical Society, 170:081507, Aug 2023. URL: https://doi.org/10.1149/1945-7111/aceeb8, doi:10.1149/1945-7111/aceeb8. This article has 21 citations and is from a peer-reviewed journal.

5. (zhang2024anassessmentof pages 1-5): Runze Zhang, Debashish Sur, Kangming Li, Julia Witt, Robert Black, Alexander Whittingham, John R. Scully, and Jason Hattrick-Simpers. An assessment of commonly used equivalent circuit models for corrosion analysis: a bayesian approach to electrochemical impedance spectroscopy. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2407.20297, doi:10.48550/arxiv.2407.20297. This article has 1 citations.

6. (zhang2023editors’choice—autoeisautomated pages 23-28): Runze Zhang, Robert Black, Debashish Sur, Parisa Karimi, Kangming Li, Brian DeCost, John R. Scully, and Jason Hattrick-Simpers. Editors’ choice—autoeis: automated bayesian model selection and analysis for electrochemical impedance spectroscopy. Journal of The Electrochemical Society, 170:086502, Aug 2023. URL: https://doi.org/10.1149/1945-7111/aceab2, doi:10.1149/1945-7111/aceab2. This article has 47 citations and is from a peer-reviewed journal.

7. (montazeri2019inprocessmonitoringof pages 1-5): Mohammad Montazeri, Abdalla R. Nassar, Alexander J. Dunbar, and Prahalada Rao. In-process monitoring of porosity in additive manufacturing using optical emission spectroscopy. IISE Transactions, 52:500-515, Oct 2019. URL: https://doi.org/10.1080/24725854.2019.1659525, doi:10.1080/24725854.2019.1659525. This article has 163 citations.

8. (saunders2021mechanicalbehaviorpredictions pages 11-11): Robert Saunders, Celia Butler, John Michopoulos, Dimitris Lagoudas, Alaa Elwany, and Amit Bagchi. Mechanical behavior predictions of additively manufactured microstructures using functional gaussian process surrogates. npj Computational Materials, 7:1-11, Jun 2021. URL: https://doi.org/10.1038/s41524-021-00548-y, doi:10.1038/s41524-021-00548-y. This article has 37 citations and is from a peer-reviewed journal.

9. (montazeri2019inprocessmonitoringof pages 30-33): Mohammad Montazeri, Abdalla R. Nassar, Alexander J. Dunbar, and Prahalada Rao. In-process monitoring of porosity in additive manufacturing using optical emission spectroscopy. IISE Transactions, 52:500-515, Oct 2019. URL: https://doi.org/10.1080/24725854.2019.1659525, doi:10.1080/24725854.2019.1659525. This article has 163 citations.

10. (maruyama2022artificialintelligencefor pages 1-2): B. Maruyama, J. Hattrick-Simpers, W. Musinski, L. Graham-Brady, K. Li, J. Hollenbach, A. Singh, and M. L. Taheri. Artificial intelligence for materials research at extremes. MRS Bulletin, 47:1154-1164, Nov 2022. URL: https://doi.org/10.1557/s43577-022-00466-4, doi:10.1557/s43577-022-00466-4. This article has 21 citations and is from a domain leading peer-reviewed journal.

11. (reyes2022decisionmakingunderuncertainty pages 1-3): Kristofer G. Reyes, Jiaqian Liu, and Carlos Juan D'iaz Vargas. Decision-making under uncertainty for multi-stage pipelines: simulation studies to benchmark screening strategies. JOM, 74:2897-2907, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05368-z, doi:10.1007/s11837-022-05368-z. This article has 2 citations and is from a peer-reviewed journal.

12. (reyes2022decisionmakingunderuncertainty pages 16-19): Kristofer G. Reyes, Jiaqian Liu, and Carlos Juan D'iaz Vargas. Decision-making under uncertainty for multi-stage pipelines: simulation studies to benchmark screening strategies. JOM, 74:2897-2907, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05368-z, doi:10.1007/s11837-022-05368-z. This article has 2 citations and is from a peer-reviewed journal.

13. (collins2026additivemanufacturingenabled pages 1-2): Peter C. Collins and Thomas K. Ales. Additive manufacturing enabled autonomous laboratory for materials discovery and concurrent design of materials and shape. MRS Bulletin, 51:746-769, Jun 2026. URL: https://doi.org/10.1557/s43577-026-01078-y, doi:10.1557/s43577-026-01078-y. This article has 2 citations and is from a domain leading peer-reviewed journal.

14. (collins2026additivemanufacturingenabled pages 18-20): Peter C. Collins and Thomas K. Ales. Additive manufacturing enabled autonomous laboratory for materials discovery and concurrent design of materials and shape. MRS Bulletin, 51:746-769, Jun 2026. URL: https://doi.org/10.1557/s43577-026-01078-y, doi:10.1557/s43577-026-01078-y. This article has 2 citations and is from a domain leading peer-reviewed journal.

15. (decost2022towardsautomateddesign pages 4-7): Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers. Towards automated design of corrosion resistant alloy coatings with an autonomous scanning droplet cell. JOM, 74:2941-2950, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05367-0, doi:10.1007/s11837-022-05367-0. This article has 29 citations and is from a peer-reviewed journal.

16. (decost2022towardsautomateddesign pages 7-10): Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers. Towards automated design of corrosion resistant alloy coatings with an autonomous scanning droplet cell. JOM, 74:2941-2950, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05367-0, doi:10.1007/s11837-022-05367-0. This article has 29 citations and is from a peer-reviewed journal.

17. (reyes2022decisionmakingunderuncertainty pages 13-16): Kristofer G. Reyes, Jiaqian Liu, and Carlos Juan D'iaz Vargas. Decision-making under uncertainty for multi-stage pipelines: simulation studies to benchmark screening strategies. JOM, 74:2897-2907, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05368-z, doi:10.1007/s11837-022-05368-z. This article has 2 citations and is from a peer-reviewed journal.

18. (reyes2022decisionmakingunderuncertainty media 4d2684c2): Kristofer G. Reyes, Jiaqian Liu, and Carlos Juan D'iaz Vargas. Decision-making under uncertainty for multi-stage pipelines: simulation studies to benchmark screening strategies. JOM, 74:2897-2907, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05368-z, doi:10.1007/s11837-022-05368-z. This article has 2 citations and is from a peer-reviewed journal.

19. (sur2023ahighthroughput pages 4-6): Debashish Sur, Howie Joress, Jason Hattrick-Simpers, and John R. Scully. A high throughput aqueous passivation testing methodology for compositionally complex alloys using a scanning droplet cell. Journal of The Electrochemical Society, 170:081507, Aug 2023. URL: https://doi.org/10.1149/1945-7111/aceeb8, doi:10.1149/1945-7111/aceeb8. This article has 21 citations and is from a peer-reviewed journal.

20. (zhang2023editors’choice—autoeisautomated pages 1-5): Runze Zhang, Robert Black, Debashish Sur, Parisa Karimi, Kangming Li, Brian DeCost, John R. Scully, and Jason Hattrick-Simpers. Editors’ choice—autoeis: automated bayesian model selection and analysis for electrochemical impedance spectroscopy. Journal of The Electrochemical Society, 170:086502, Aug 2023. URL: https://doi.org/10.1149/1945-7111/aceab2, doi:10.1149/1945-7111/aceab2. This article has 47 citations and is from a peer-reviewed journal.

21. (zhang2024bayesianassessmentof pages 1-2): Runze Zhang, Debashish Sur, Kangming Li, Julia Witt, Robert Black, Alexander Whittingham, John R. Scully, and Jason Hattrick-Simpers. Bayesian assessment of commonly used equivalent circuit models for corrosion analysis in electrochemical impedance spectroscopy. npj Materials Degradation, Nov 2024. URL: https://doi.org/10.1038/s41529-024-00537-8, doi:10.1038/s41529-024-00537-8. This article has 47 citations and is from a peer-reviewed journal.

22. (zhang2024anassessmentof pages 14-19): Runze Zhang, Debashish Sur, Kangming Li, Julia Witt, Robert Black, Alexander Whittingham, John R. Scully, and Jason Hattrick-Simpers. An assessment of commonly used equivalent circuit models for corrosion analysis: a bayesian approach to electrochemical impedance spectroscopy. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2407.20297, doi:10.48550/arxiv.2407.20297. This article has 1 citations.

23. (saunders2021mechanicalbehaviorpredictions pages 9-10): Robert Saunders, Celia Butler, John Michopoulos, Dimitris Lagoudas, Alaa Elwany, and Amit Bagchi. Mechanical behavior predictions of additively manufactured microstructures using functional gaussian process surrogates. npj Computational Materials, 7:1-11, Jun 2021. URL: https://doi.org/10.1038/s41524-021-00548-y, doi:10.1038/s41524-021-00548-y. This article has 37 citations and is from a peer-reviewed journal.

24. (wang2020uncertaintyquantificationand pages 1-4): Xin Wang and Wei Xiong. Uncertainty quantification and composition optimization for alloy additive manufacturing through a calphad-based icme framework. npj Computational Materials, Dec 2020. URL: https://doi.org/10.1038/s41524-020-00454-9, doi:10.1038/s41524-020-00454-9. This article has 86 citations and is from a peer-reviewed journal.

25. (collins2026additivemanufacturingenabled pages 20-21): Peter C. Collins and Thomas K. Ales. Additive manufacturing enabled autonomous laboratory for materials discovery and concurrent design of materials and shape. MRS Bulletin, 51:746-769, Jun 2026. URL: https://doi.org/10.1557/s43577-026-01078-y, doi:10.1557/s43577-026-01078-y. This article has 2 citations and is from a domain leading peer-reviewed journal.

26. (maruyama2022artificialintelligencefor pages 5-7): B. Maruyama, J. Hattrick-Simpers, W. Musinski, L. Graham-Brady, K. Li, J. Hollenbach, A. Singh, and M. L. Taheri. Artificial intelligence for materials research at extremes. MRS Bulletin, 47:1154-1164, Nov 2022. URL: https://doi.org/10.1557/s43577-022-00466-4, doi:10.1557/s43577-022-00466-4. This article has 21 citations and is from a domain leading peer-reviewed journal.

27. (hickman2023olympusenhancedbenchmarking pages 10-12): Riley Hickman, Priyansh Parakh, Austin Cheng, Qianxiang Ai, Joshua Schrier, Matteo Aldeghi, and Alán Aspuru-Guzik. Olympus, enhanced: benchmarking mixed-parameter and multi-objective optimization in chemistry and materials science. ChemRxiv, May 2023. URL: https://doi.org/10.26434/chemrxiv-2023-74w8d, doi:10.26434/chemrxiv-2023-74w8d. This article has 15 citations.

28. (stach2021autonomousexperimentationsystems pages 13-16): Eric Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown, Kristofer G. Reyes, Joshua Schrier, Simon Billinge, Tonio Buonassisi, Ian Foster, Carla P. Gomes, John M. Gregoire, Apurva Mehta, Joseph Montoya, Elsa Olivetti, Chiwoo Park, Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, and Benji Maruyama. Autonomous experimentation systems for materials development: a community perspective. Matter, 4:2702-2726, Sep 2021. URL: https://doi.org/10.1016/j.matt.2021.06.036, doi:10.1016/j.matt.2021.06.036. This article has 493 citations and is from a peer-reviewed journal.

29. (stach2021autonomousexperimentationsystems pages 2-3): Eric Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown, Kristofer G. Reyes, Joshua Schrier, Simon Billinge, Tonio Buonassisi, Ian Foster, Carla P. Gomes, John M. Gregoire, Apurva Mehta, Joseph Montoya, Elsa Olivetti, Chiwoo Park, Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, and Benji Maruyama. Autonomous experimentation systems for materials development: a community perspective. Matter, 4:2702-2726, Sep 2021. URL: https://doi.org/10.1016/j.matt.2021.06.036, doi:10.1016/j.matt.2021.06.036. This article has 493 citations and is from a peer-reviewed journal.

30. (stach2021autonomousexperimentationsystems pages 8-9): Eric Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown, Kristofer G. Reyes, Joshua Schrier, Simon Billinge, Tonio Buonassisi, Ian Foster, Carla P. Gomes, John M. Gregoire, Apurva Mehta, Joseph Montoya, Elsa Olivetti, Chiwoo Park, Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, and Benji Maruyama. Autonomous experimentation systems for materials development: a community perspective. Matter, 4:2702-2726, Sep 2021. URL: https://doi.org/10.1016/j.matt.2021.06.036, doi:10.1016/j.matt.2021.06.036. This article has 493 citations and is from a peer-reviewed journal.

31. (talbot2026activelearningfor pages 19-24): Ajay Talbot, Soumya S. Dash, Jialu Li, Changjun Cheng, Madhi Ramesh, Xiao Shang, Jiahui Zhang, Cristian Cojocaru, Jason Hattrick-Simpers, and Yu Zou. Active learning for the accelerated discovery of complex concentrated nicocr alloys in additive manufacturing. npj Advanced Manufacturing, Jun 2026. URL: https://doi.org/10.1038/s44334-026-00098-5, doi:10.1038/s44334-026-00098-5. This article has 2 citations.
