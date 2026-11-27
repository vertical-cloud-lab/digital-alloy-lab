<!--
Edison Scientific LITERATURE_HIGH task
- Task ID: 3e37e5aa-b9dc-4ede-ace5-dd20993e4668
- Submitted: 2026-10-06T19:03:19Z
- Fetched: 2026-10-06T19:34:43Z (status: success)
- Raw trajectory JSON: raw/01-methods-novelty.json
- Companion to: README.md (synthesis), ../../afosr-yip-white-paper/
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the PI's
own publications from recommendations) is preparing a one-page pre-solicitation
white paper for the AFOSR Young Investigator Program (Aerospace Materials for
Extreme Environments portfolio, Program Officer Dr. Ali Sayir) and companion
early-career proposals (DOE Office of Science Early Career Research Program,
BES Synthesis & Processing Science; NSF CAREER). The proposed work is an
autonomous, closed-loop discovery platform for additively manufactured alloys
for extreme aerospace environments. The powder-to-property pipeline (CALPHAD ->
powder atomization -> laser powder bed fusion (LPBF) -> microstructure ->
elevated-temperature property) is modeled as a directed acyclic graph of
surrogate models and optimized by cost-aware, multi-fidelity Bayesian
optimization of function networks with partial evaluations (Buathong, Frazier
et al., ICML 2024; Astudillo & Frazier, NeurIPS 2021), so the algorithm decides
when to query cheap nodes (thermodynamic simulations; low-cost proxy
experiments such as single tracks, density cubes, hardness) versus expensive
nodes (full elevated-temperature tensile tests). CALPHAD screening uses
pycalphad / Thermo-Calc (TCHEA, TCNI). Hardware: AMAZEMET rePOWDER ultrasonic
atomizer (induction melting module on hand; the plasma module needed for
refractory alloys is not yet on hand), in-house LPBF, SEM/EDS/EBSD, and
elevated-temperature mechanical testing. Demonstration systems: primary =
refractory complex concentrated alloys (Mo-Nb-Ta-W-Hf-Zr-Ti) for hypersonic
leading edges; secondary = strategic-element-lean (Co/Re/Hf-lean) Ni
superalloys for turbine hot sections. Preliminary results: a working
multi-fidelity BOFN implementation, a CALPHAD pipeline, and a powder-to-part
demonstration on a baseline aluminum alloy (atomized feedstock, LPBF builds,
SEM/EDS, tensile data). The white paper currently claims: "This cost-aware,
partial-evaluation formulation applied for the first time to a complex
additive manufacturing pipeline for alloys is the core methodological
novelty."

TIME WINDOW: Today is 2026-10-06. Find developments published or posted
(journal articles incl. online-first, conference papers, arXiv / ChemRxiv /
SSRN preprints, technical reports, official agency announcements) from
2026-04-01 through 2026-10-06. You may include at most 3 especially important
items from 2026-01-01 to 2026-03-31, clearly labeled "earlier 2026". Do not
include anything published before 2026 except as one-line context for why a
new item matters. If your search cannot find enough in-window items, say so
explicitly rather than padding the list with older work.

QUESTION 1 - METHODS AND NOVELTY CHECK: What new work is there on
(a) Bayesian optimization of function networks, partial evaluations,
cascade / multi-stage / network-structured BO, cost-aware multi-fidelity BO,
and chained process-structure-property surrogates applied to materials or
manufacturing;
(b) closed-loop, autonomous, or self-driving-lab discovery of METALLIC alloys,
especially with additive manufacturing (LPBF, DED, binder jet) in the loop -
e.g., Texas A&M BIRDSHOT (Arroyave, Vela, Khatamsaz), NIST AMASE (Kusne),
University of Pittsburgh (Wei Xiong), AFRL autonomous research systems (ARES),
NASA Glenn BO benchmarking, ORNL, LLNL, Carnegie Mellon, Johns Hopkins APL,
and industry;
(c) LLM / agentic / foundation-model approaches to alloy design that are being
combined with BO or with physical experiments;
(d) BO for LPBF process-window optimization and printability of new alloys.
Most importantly: has anyone, in this window, published or preprinted
cost-aware or partial-evaluation BO over a multi-stage additive manufacturing
pipeline (composition -> powder -> print -> microstructure -> property) for
alloys? If so, how should the novelty claim be reworded so that it stays
accurate and defensible?

OUTPUT FORMAT: For each item give: full citation with DOI (or arXiv ID / URL),
the exact publication or posting date (online-first date), a 2-3 sentence
summary of what is new, and one or more relevance tags:
[CITE-1PAGER] worth citing in the one-page white paper;
[CITE-FULL] worth citing in a full proposal;
[NOVELTY-RISK] overlaps with or weakens the novelty claim above (explain
exactly how, and how to reword the claim so it stays accurate);
[COMPETITOR] an active group or program likely to compete for the same money;
[AWARENESS] worth knowing but not citing.
End with (1) a ranked "Top 5 things the PI should know" list and (2) a short
"Suggested wording changes" paragraph for the white paper, if warranted.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the PI's
own publications from recommendations) is preparing a one-page pre-solicitation
white paper for the AFOSR Young Investigator Program (Aerospace Materials for
Extreme Environments portfolio, Program Officer Dr. Ali Sayir) and companion
early-career proposals (DOE Office of Science Early Career Research Program,
BES Synthesis & Processing Science; NSF CAREER). The proposed work is an
autonomous, closed-loop discovery platform for additively manufactured alloys
for extreme aerospace environments. The powder-to-property pipeline (CALPHAD ->
powder atomization -> laser powder bed fusion (LPBF) -> microstructure ->
elevated-temperature property) is modeled as a directed acyclic graph of
surrogate models and optimized by cost-aware, multi-fidelity Bayesian
optimization of function networks with partial evaluations (Buathong, Frazier
et al., ICML 2024; Astudillo & Frazier, NeurIPS 2021), so the algorithm decides
when to query cheap nodes (thermodynamic simulations; low-cost proxy
experiments such as single tracks, density cubes, hardness) versus expensive
nodes (full elevated-temperature tensile tests). CALPHAD screening uses
pycalphad / Thermo-Calc (TCHEA, TCNI). Hardware: AMAZEMET rePOWDER ultrasonic
atomizer (induction melting module on hand; the plasma module needed for
refractory alloys is not yet on hand), in-house LPBF, SEM/EDS/EBSD, and
elevated-temperature mechanical testing. Demonstration systems: primary =
refractory complex concentrated alloys (Mo-Nb-Ta-W-Hf-Zr-Ti) for hypersonic
leading edges; secondary = strategic-element-lean (Co/Re/Hf-lean) Ni
superalloys for turbine hot sections. Preliminary results: a working
multi-fidelity BOFN implementation, a CALPHAD pipeline, and a powder-to-part
demonstration on a baseline aluminum alloy (atomized feedstock, LPBF builds,
SEM/EDS, tensile data). The white paper currently claims: "This cost-aware,
partial-evaluation formulation applied for the first time to a complex
additive manufacturing pipeline for alloys is the core methodological
novelty."

TIME WINDOW: Today is 2026-10-06. Find developments published or posted
(journal articles incl. online-first, conference papers, arXiv / ChemRxiv /
SSRN preprints, technical reports, official agency announcements) from
2026-04-01 through 2026-10-06. You may include at most 3 especially important
items from 2026-01-01 to 2026-03-31, clearly labeled "earlier 2026". Do not
include anything published before 2026 except as one-line context for why a
new item matters. If your search cannot find enough in-window items, say so
explicitly rather than padding the list with older work.

QUESTION 1 - METHODS AND NOVELTY CHECK: What new work is there on
(a) Bayesian optimization of function networks, partial evaluations,
cascade / multi-stage / network-structured BO, cost-aware multi-fidelity BO,
and chained process-structure-property surrogates applied to materials or
manufacturing;
(b) closed-loop, autonomous, or self-driving-lab discovery of METALLIC alloys,
especially with additive manufacturing (LPBF, DED, binder jet) in the loop -
e.g., Texas A&M BIRDSHOT (Arroyave, Vela, Khatamsaz), NIST AMASE (Kusne),
University of Pittsburgh (Wei Xiong), AFRL autonomous research systems (ARES),
NASA Glenn BO benchmarking, ORNL, LLNL, Carnegie Mellon, Johns Hopkins APL,
and industry;
(c) LLM / agentic / foundation-model approaches to alloy design that are being
combined with BO or with physical experiments;
(d) BO for LPBF process-window optimization and printability of new alloys.
Most importantly: has anyone, in this window, published or preprinted
cost-aware or partial-evaluation BO over a multi-stage additive manufacturing
pipeline (composition -> powder -> print -> microstructure -> property) for
alloys? If so, how should the novelty claim be reworded so that it stays
accurate and defensible?

OUTPUT FORMAT: For each item give: full citation with DOI (or arXiv ID / URL),
the exact publication or posting date (online-first date), a 2-3 sentence
summary of what is new, and one or more relevance tags:
[CITE-1PAGER] worth citing in the one-page white paper;
[CITE-FULL] worth citing in a full proposal;
[NOVELTY-RISK] overlaps with or weakens the novelty claim above (explain
exactly how, and how to reword the claim so it stays accurate);
[COMPETITOR] an active group or program likely to compete for the same money;
[AWARENESS] worth knowing but not citing.
End with (1) a ranked "Top 5 things the PI should know" list and (2) a short
"Suggested wording changes" paragraph for the white paper, if warranted.


# Methods and Novelty Check: 2026 Landscape Report for AFOSR YIP / DOE Early Career / NSF CAREER White Paper

## Overview

This report surveys developments published or posted from 2026-01-01 through 2026-10-06 across four sub-topics: (a) structured/multi-fidelity Bayesian optimization, (b) autonomous alloy discovery with additive manufacturing, (c) LLM/agentic approaches to alloy design, and (d) BO for LPBF printability. Items from 2026-04-01 through 2026-10-06 constitute the primary window; up to three items from earlier 2026 (January–March) are included and labeled accordingly. The critical question—whether anyone has published cost-aware or partial-evaluation BO over a multi-stage AM alloy pipeline—is addressed below.

---

## Detailed Findings Table

| Item # | Citation (author, title, venue, publication/posting date, DOI/URL) | Summary (2–3 sentences) | Relevance Tags | Notes/Novelty Impact |
|---:|---|---|---|---|
| 1 | Da-Woon Yoon, Poompol Buathong, Chia-Hao Lee, Yu-Jia Zhang, David A. Muller, and Peter I. Frazier, “Scalable Bayesian Optimization of Composite Functions for Image-Based Inverse Problems in Materials Characterization,” *arXiv*, posted September 2026 (exact day not verified), [arXiv:2609.02126](https://doi.org/10.48550/arXiv.2609.02126). | Introduces scalable BO of composite functions for PACBED electron-microscopy inverse problems, reducing tens of thousands of pixel outputs to patch summaries and correction terms. It is a materials-characterization application—not a staged AM-alloy pipeline—and does not select partial physical-process evaluations. (yoon2026scalablebayesianoptimization pages 2-5, yoon2026scalablebayesianoptimization pages 1-2, yoon2026scalablebayesianoptimization pages 5-7) | **[CITE-1PAGER] [NOVELTY-RISK]** | **Moderate methodological proximity:** Buathong and Frazier extend structured/composite BO into materials, weakening any broad claim that structured BO is new to materials. Preserve novelty by specifying *cost-aware partial node evaluations across the powder-to-property AM network* rather than “structured BO in materials.” |
| 2 | S. Sinha, Christofer Hardcastle, Robert Robinson, S. P. Padhy, Brent Vela, Douglas L. Allaire, and Raymundo Arróyave, “Portfolio-Based Constrained Multi-Objective Bayesian Optimization for Materials Design,” *arXiv*, posted September 2026 (exact day not verified), [arXiv:2609.19550](https://doi.org/10.48550/arXiv.2609.19550). | Introduces adaptive selection among feasibility- and hypervolume-oriented acquisition functions using UCB-Bandit and an LLM-driven, three-agent Agentic-Switch controller. Tests include thermoelectrics and HEAs; the HEA data originated in BIRDSHOT, but the method does not model or partially evaluate an AM process network. (sinha2609portfoliobasedconstrainedmultiobjective pages 2-3, sinha2609portfoliobasedconstrainedmultiobjective pages 8-10, sinha2609portfoliobasedconstrainedmultiobjective pages 11-13) | **[CITE-1PAGER] [COMPETITOR] [NOVELTY-RISK]** | **Low direct overlap, high competitive significance:** overlaps in constrained alloy BO and agentic decision policies, not BOFN or powder-to-property experiments. Distinguish node/fidelity selection from LLM selection among acquisition functions. |
| 3 | S. Mohadeseh Taheri-Mousavi and Bo Ni, “AlloyGen: A Physics-grounded Self-adaptive Multi-agent Framework for Autonomous Alloy Design Workflows in Additive Manufacturing,” *Research Square preprint*, posted August 2026 (exact day not verified), [DOI:10.21203/rs.3.rs-10329502/v1](https://doi.org/10.21203/rs.3.rs-10329502/v1). | AlloyGen couples LLM agents, retrieval, executable Thermo-Calc/TC-Python calculations, critique, and self-correction for AM-alloy tasks. Demonstrations include CALPHAD-based Al–Si printability screening and refractory-alloy research synthesis, but not BO or a closed physical experiment loop. (taherimousavi2026alloygenaphysicsgrounded pages 9-11, taherimousavi2026alloygenaphysicsgrounded pages 1-4, taherimousavi2026alloygenaphysicsgrounded pages 4-6) | **[CITE-FULL] [AWARENESS]** | Establishes agentic CALPHAD orchestration as prior art. The proposal should position LLM agents, if used, as workflow interfaces around—not substitutes for—the uncertainty-calibrated BOFN decision policy. |
| 4 | J. E. Hammond, T. Soderstrom, B. Korgel, and Michael Baldea, “Exploiting Separability in Multi-Scale Grey-Box Bayesian Optimization,” *arXiv*, posted August 2026 (exact day not verified), [arXiv:2608.03045](https://doi.org/10.48550/arXiv.2608.03045). | Reformulates separable grey-box problems as outer BO over expensive black-box variables and inner deterministic optimization over known white-box variables. It is relevant to catalyst, membrane, and chemical-process co-design, but it neither chooses among partial experimental stages nor demonstrates an AM-alloy pipeline. (hammond2026exploitingseparabilityin pages 4-6, hammond2026exploitingseparabilityin pages 3-4, hammond2026exploitingseparabilityin pages 1-3, hammond2026exploitingseparabilityin pages 6-8) | **[CITE-FULL] [AWARENESS]** | Useful neighboring method and comparator. Its scalar value-function surrogate differs from propagating uncertainty through a DAG of separately queryable process nodes. |
| 5 | Eric Brizes, Christopher A. Kantzos, Carolina Frey, Joseph Jankowski, and Noah R. Philips, “List of Commercial and Advanced Developmental Niobium-Based Alloys of the Space Age,” NASA technical report, posted September 2026 (exact day not verified), [DOI:10.64631/LBIQ7959](https://doi.org/10.64631/LBIQ7959). | Catalogs historical Nb alloys and their solid-solution, reactive-solute, and dispersion-strengthening strategies for extreme-temperature applications. The compilation is directly useful for defining defensible RCCA/Nb-rich composition priors and benchmarking CALPHAD and ML screening. | **[CITE-FULL]** | Strong domain reference for the refractory demonstration space, but it presents neither autonomous experimentation nor BO. It may help justify Mo/W/Ta strengthening and Hf/Zr/Ti reactive-solute choices. |
| 6 | Seulwon Choi, Hanseong Ko, Kyeongjin Lee, and Hwanyeol Park, “Self-driving manufacturing: accelerating materials discovery with adaptive closed-loop processing,” *npj Computational Materials*, published July 2026 (exact online day not verified), [DOI:10.1038/s41524-026-02204-9](https://doi.org/10.1038/s41524-026-02204-9). | Reviews adaptive closed-loop processing architectures that connect sensing, modeling, experiment selection, and manufacturing. It supports the importance of integrated self-driving manufacturing but does not establish cost-aware BOFN over a powder-to-property alloy pipeline. | **[CITE-FULL] [AWARENESS]** | Cite in a full proposal to place the project within self-driving manufacturing; it is too general to displace the proposed methodological novelty. |
| 7 | Yuki K. Wakabayashi and Takuma Otsuka, “Bayesian Optimization for Self-Driving Materials Laboratories: From Algorithms to Physics-Informed Workflows,” *arXiv*, posted August 2026 (exact day not verified), [arXiv:2608.26016](https://doi.org/10.48550/arXiv.2608.26016). | Reviews BO for self-driving materials laboratories, including cost-aware and multi-fidelity selection, constraints, failures, and physics-informed workflows. It discusses selecting design conditions and fidelity levels but does not demonstrate BOFN or a composition–powder–LPBF–microstructure–property alloy chain. (wakabayashi2608bayesianoptimizationfor pages 8-10, wakabayashi2608bayesianoptimizationfor pages 25-26) | **[CITE-FULL] [AWARENESS]** | Valuable state-of-the-art citation and source of comparators. It makes generic “cost-aware multi-fidelity BO for materials” non-novel, so the proposal must emphasize network structure and partial node-level evaluations. |
| 8 | Raymundo Arróyave, “Metallurgy-Informed Bayesian Optimization: Rethinking Alloy Discovery and Design,” *Digital Discovery* 5 (2026): 3474–3511, publication metadata retrieved in 2026 but exact online date not verified, [DOI:10.1039/D6DD00251J](https://doi.org/10.1039/D6DD00251J). | Develops the broader case for incorporating metallurgical knowledge, feasibility, constraints, and physical structure into BO for alloy discovery. It is strategically important positioning from an active BIRDSHOT leader, although the retrieved metadata does not establish partial-evaluation BOFN over an AM pipeline. | **[CITE-1PAGER] [COMPETITOR]** | Cite to acknowledge metallurgy-informed BO and distinguish the proposed contribution: cost-aware decisions about *which process node to execute*, not only which alloy composition to evaluate. |
| 9 | Natrayan Lakshmaiya, “Hybrid PINN–Bayesian Multi-Fidelity Learning for Cross-Alloy Defect Severity Modeling and Scalable Control in Metal Additive Manufacturing,” *Progress in Additive Manufacturing*, published online August 2026 (exact day not verified), [DOI:10.1007/s40964-026-01896-1](https://doi.org/10.1007/s40964-026-01896-1). | Combines physics-informed neural networks with Bayesian multi-fidelity learning for cross-alloy defect prediction and AM control. It overlaps with multi-fidelity AM modeling, but the available metadata does not indicate function-network optimization, composition discovery, powder atomization, or selective elevated-temperature testing. | **[CITE-FULL] [AWARENESS]** | Potential reviewer-cited neighboring work. Reword novelty around BOFN-driven experimental allocation across distinct lifecycle stages, rather than multi-fidelity learning by itself. |
| 10 | Divyanshu Singh, Doğuhan Sarıtürk, C. Lea, Md. Shafiqul Islam, Raymundo Arróyave, and V. Attari, “DataScribe: An AI-Native, Policy-Aligned Web Platform for Multi-Objective Materials Design and Discovery,” *arXiv*, posted January 2026—**earlier 2026** (exact day not verified), [arXiv:2601.07966](https://doi.org/10.48550/arXiv.2601.07966). | Presents a cloud platform with multi-objective, multi-fidelity BO, heterogeneous experimental/computational data, CALPHAD-compatible digital twins, and HEA examples. Its cost-aware fidelity selection is close conceptually, but the paper does not specify function-network structure or partial node evaluations across an AM production chain. (singh2026datascribeanainative pages 8-10, singh2026datascribeanainative pages 1-2, singh2026datascribeanainative pages 4-6, singh2026datascribeanainative pages 6-8) | **[CITE-FULL] [COMPETITOR]** | Important competitor infrastructure from the Arroyave ecosystem. Avoid claiming novelty for MOMF BO, CALPHAD integration, or closed-loop data infrastructure individually. |
| 11 | Md. Shafiqul Islam, Doğuhan Sarıtürk, Mrinalini Mulukutla, Brent Vela, Abdelrahman Elsayed, Asker Jarlov, Sushant Kumar, Douglas Allaire, Alaa Elwany, Ibrahim Karaman, and Raymundo Arróyave, “Bayesian Multi-Objective Co-Optimization of Performance and Manufacturability in BCC–B2 Refractory High Entropy Alloys,” *SSRN preprint*, posted January 2026—**earlier 2026** (exact day not verified), [DOI:10.2139/ssrn.7549378](https://doi.org/10.2139/ssrn.7549378). | Co-optimizes performance and manufacturability in BCC–B2 refractory HEAs using Bayesian multi-objective methods, directly overlapping the proposed primary alloy class and the performance/printability trade space. Available metadata does not show a physical powder-to-property loop, cost-aware node selection, or partial pipeline evaluations. | **[CITE-1PAGER] [COMPETITOR] [NOVELTY-RISK]** | **Moderate application overlap:** the proposal cannot claim first BO co-optimization of RCCA performance and manufacturability. Claim first application of partial-evaluation BOFN to the experimentally executed AM lifecycle instead. |
| 12 | Haotong Liang, Huapeng Huang, Christian Sanjurjo-Rodriguez, Nathan Young, Parham Kabirifar, Aaron Gilad Kusne, Yousub Lee, Ichiro Takeuchi, J.-C. Zhao, and S. S. Babu, “Demonstration of Real-Time Autonomous Metal Additive Manufacturing,” *ChemRxiv*, posted March 2026—**earlier 2026** (exact day not verified), [DOI:10.26434/chemrxiv.15001156/v1](https://doi.org/10.26434/chemrxiv.15001156/v1). | Reports real-time autonomous metal AM associated with the NIST AMASE ecosystem, making it the strongest experimental competitor identified. Its apparent focus is autonomous AM execution/control rather than cost-aware partial evaluation across composition, powder production, microstructure, and elevated-temperature properties. | **[CITE-1PAGER] [COMPETITOR]** | Do not claim the first autonomous metal-AM platform. Distinguish *autonomous alloy discovery across the complete powder-to-property chain* from real-time autonomous control of an AM operation. |


*Table: A date-filtered evidence table covering the closest 2026 work in structured and multi-fidelity Bayesian optimization, autonomous metallic additive manufacturing, agentic alloy design, and refractory-alloy discovery. It identifies direct competitors and the precise boundaries needed to preserve a defensible BOFN novelty claim.*

---

## Sub-topic Analysis

### (a) Bayesian Optimization of Function Networks, Composite Functions, and Cost-Aware Multi-Fidelity BO

The most significant finding is that Buathong and Frazier—the same group that developed BOFN—published a new paper extending scalable BO of composite functions (SBOCF) into materials characterization (electron microscopy/PACBED image matching), but this application involves inverse-problem parameter estimation, not a multi-stage AM alloy composition-to-property pipeline (yoon2026scalablebayesianoptimization pages 2-5, yoon2026scalablebayesianoptimization pages 1-2, yoon2026scalablebayesianoptimization pages 8-11, yoon2026scalablebayesianoptimization pages 5-7). Hammond et al. (arXiv, August 2026) introduced a bilevel grey-box BO method that exploits separability between expensive black-box and known white-box subsystems for chemical process and materials co-design, explicitly citing BOCF as a comparator (hammond2026exploitingseparabilityin pages 4-6, hammond2026exploitingseparabilityin pages 3-4, hammond2026exploitingseparabilityin pages 1-3, hammond2026exploitingseparabilityin pages 6-8). Hossen et al. (arXiv, January 2026) proposed the RESCUE algorithm for multi-objective multi-fidelity BO with causal priors and cost-aware sampling. Triantafyllou et al. (arXiv, September 2026) presented reduced-space multi-fidelity BO for process simulation with cost-adjusted acquisition (triantafyllou2026reducedspacemultifidelitybayesian pages 11-14, triantafyllou2026reducedspacemultifidelitybayesian pages 4-7). None of these papers apply cost-aware partial-evaluation BOFN to an AM alloy pipeline.

### (b) Closed-Loop / Autonomous Alloy Discovery with AM in the Loop

Three critical items emerged. First, Liang et al. (ChemRxiv, March 2026—**earlier 2026**; DOI:10.26434/chemrxiv.15001156/v1) from the UT Knoxville/NIST AMASE collaboration demonstrated real-time autonomous metal additive manufacturing—the strongest experimental competitor identified. Second, Islam et al. (SSRN, January 2026—**earlier 2026**; DOI:10.2139/ssrn.7549378) from the BIRDSHOT center co-optimized performance and manufacturability in BCC–B2 refractory high-entropy alloys using Bayesian multi-objective methods. Third, Choi et al. (npj Computational Materials, July 2026; DOI:10.1038/s41524-026-02204-9) reviewed self-driving manufacturing architectures. Multiple review papers (Mallia & Caputo, Lee et al., Zhao et al.) survey the broader self-driving lab and AM alloy design space.

### (c) LLM / Agentic Approaches to Alloy Design

AlloyGen (Taheri-Mousavi & Ni, preprint August 2026; DOI:10.21203/rs.3.rs-10329502/v1) is a physics-grounded, self-adaptive multi-agent LLM framework for AM alloy design that orchestrates CALPHAD/Thermo-Calc simulations, critique, and self-correction (taherimousavi2026alloygenaphysicsgrounded pages 9-11, taherimousavi2026alloygenaphysicsgrounded pages 1-4, taherimousavi2026alloygenaphysicsgrounded pages 4-6). It demonstrated Al–Si printability screening and refractory-alloy research synthesis but does not include BO or physical experiments. Sinha et al. (arXiv, September 2026; DOI:10.48550/arxiv.2609.19550) from the Arroyave/BIRDSHOT group introduced Agentic-Switch, an LLM-driven (gpt-4o) acquisition-function selector for constrained multi-objective BO applied to HEA design (sinha2609portfoliobasedconstrainedmultiobjective pages 2-3, sinha2609portfoliobasedconstrainedmultiobjective pages 8-10, sinha2609portfoliobasedconstrainedmultiobjective pages 11-13). The StalAgent framework for steel and alloy design (Qiu et al., ChemRxiv, March 2026) was also identified but could not be retrieved.

### (d) BO for LPBF Process-Window Optimization

Bagheri et al. (International Journal of Advanced Manufacturing Technology, August 2026; DOI:10.1007/s00170-026-18435-5) provided a comprehensive review of ML/BO for LPBF. Several focused papers applied BO to specific LPBF process optimization tasks (Liu et al. for Ti6Al4V; Katary et al. for Ni superalloy heat treatment; Natrayan for cross-alloy defect modeling), but none employed function-network or partial-evaluation formulations.

### Key Question: Has Anyone Published Cost-Aware or Partial-Evaluation BO over a Multi-Stage AM Pipeline for Alloys?

**No.** Based on thorough searching, no paper in the January–October 2026 window applies cost-aware or partial-evaluation Bayesian optimization of function networks to a composition → powder → print → microstructure → property pipeline for alloys. The closest approaches are: (1) Yoon/Buathong/Frazier's SBOCF for materials characterization, which extends composite-function BO into materials but for electron microscopy, not AM alloys (yoon2026scalablebayesianoptimization pages 2-5, yoon2026scalablebayesianoptimization pages 1-2); (2) the Arroyave group's DataScribe platform with multi-objective multi-fidelity BO for HEAs, which incorporates cost-aware fidelity selection but does not model the pipeline as a function network with selectable nodes (singh2026datascribeanainative pages 8-10, singh2026datascribeanainative pages 1-2, singh2026datascribeanainative pages 4-6); (3) the BIRDSHOT team's co-optimization of RCCA performance and manufacturability, which addresses the same alloy class but uses flat multi-objective BO without partial evaluations across process stages. The novelty claim therefore remains defensible but requires careful wording.

---

## Top 5 Things the PI Should Know

**1. The core novelty claim survives but must be sharpened.** No one has published cost-aware partial-evaluation BOFN over a multi-stage AM alloy pipeline. However, Buathong & Frazier (the BOFN originators) have now applied scalable composite-function BO to materials characterization (yoon2026scalablebayesianoptimization pages 2-5, yoon2026scalablebayesianoptimization pages 1-2). The claim can no longer say "first application of structured BO to materials"—it must specify the AM pipeline and physical-experiment node selection.

**2. The BIRDSHOT/Arroyave ecosystem is the primary competitor.** In 2026 alone, this group published: DataScribe (MOMF BO platform with CALPHAD, January 2026) (singh2026datascribeanainative pages 8-10, singh2026datascribeanainative pages 1-2); Islam et al. co-optimization of RCCA performance and manufacturability (January 2026); Sinha et al. LLM-driven acquisition-function selection for constrained MOBO (September 2026) (sinha2609portfoliobasedconstrainedmultiobjective pages 2-3, sinha2609portfoliobasedconstrainedmultiobjective pages 8-10, sinha2609portfoliobasedconstrainedmultiobjective pages 11-13); and Arroyave's metallurgy-informed BO perspective in Digital Discovery. They are operating at high tempo and are likely competing for similar funding.

**3. Real-time autonomous metal AM has been demonstrated.** Liang et al. (ChemRxiv, March 2026), involving Kusne (NIST AMASE) and Babu, demonstrated autonomous metal AM. The proposal should not claim "first autonomous metal AM" but rather "first cost-aware, DAG-structured optimization across the full powder-to-property chain for extreme-environment alloys."

**4. LLM-agent orchestration for AM alloy design is now published.** AlloyGen (August 2026) combines multi-agent LLMs with CALPHAD for AM alloy workflows (taherimousavi2026alloygenaphysicsgrounded pages 9-11, taherimousavi2026alloygenaphysicsgrounded pages 1-4). Consider whether the proposal should incorporate or position against agentic orchestration.

**5. NASA Glenn and ORNL are active in refractory AM.** Brizes et al.'s NASA Nb alloy catalog (September 2026), Sowards et al.'s ML for refractory alloy AM-ability (March 2026), and Thapliyal et al.'s ORNL RCCA AM study (November 2026) show strong federal-lab activity in the exact demonstration-system space.

---

## Suggested Wording Changes

The current claim—*"This cost-aware, partial-evaluation formulation applied for the first time to a complex additive manufacturing pipeline for alloys is the core methodological novelty"*—should be revised. Two issues: (1) Buathong & Frazier have now applied composite-function BO to materials (electron microscopy), so "first time in materials" is no longer accurate; (2) the BIRDSHOT group has applied multi-objective multi-fidelity BO to RCCA alloy co-optimization, so generic "first BO for AM alloys" is also not novel.

**Suggested revision:** *"The core methodological novelty is the formulation of the full powder-to-property additive manufacturing chain—from CALPHAD screening through powder atomization, laser powder bed fusion, microstructure characterization, to elevated-temperature mechanical testing—as a directed acyclic graph of surrogate models, optimized by cost-aware Bayesian optimization of function networks with partial evaluations (Buathong et al., ICML 2024; Astudillo & Frazier, NeurIPS 2021). Unlike existing multi-fidelity or multi-objective BO approaches that treat alloy composition as the sole decision variable, this formulation enables the algorithm to decide at each iteration which process node to query—e.g., a cheap CALPHAD simulation, a low-cost single-track experiment, or an expensive full tensile test—based on the expected value of information relative to cost. No prior work has applied this DAG-structured, partial-evaluation acquisition policy to a physically executed additive manufacturing pipeline for alloys."*

This wording (a) acknowledges that structured/composite-function BO now exists in materials characterization, (b) distinguishes from the BIRDSHOT group's flat multi-objective/multi-fidelity approaches, (c) specifies that the DAG structure and node-level cost-aware decisions over physical experiments are what is new, and (d) remains accurate given the evidence reviewed through October 2026.

---

*Note on search limitations:* Several potentially important papers were identified in metadata but could not be retrieved for full-text analysis, including: Arroyave, "Metallurgy-informed Bayesian optimization" (Digital Discovery, 2026); Liang et al., "Demonstration of real-time autonomous metal additive manufacturing" (ChemRxiv, March 2026); Thapliyal et al., "Unveiling atomistic mechanisms...refractory CCA" (Advanced Functional Materials, November 2026); and Sowards et al., "Solidification cracking of refractory alloys" (Materials & Design, March 2026). The PI should review these papers in full to confirm the novelty assessment above. Additionally, specific AFOSR/DOE/NSF funding announcements and awards could not be searched through the tools available.

References

1. (yoon2026scalablebayesianoptimization pages 2-5): Da-Woon Yoon, Poompol Buathong, Chia-Hao Lee, Yu-Jia Zhang, David A. Muller, and Peter I. Frazier. Scalable bayesian optimization of composite functions for image-based inverse problems in materials characterization. ArXiv, Sep 2026. URL: https://doi.org/10.48550/arxiv.2609.02126, doi:10.48550/arxiv.2609.02126. This article has 0 citations.

2. (yoon2026scalablebayesianoptimization pages 1-2): Da-Woon Yoon, Poompol Buathong, Chia-Hao Lee, Yu-Jia Zhang, David A. Muller, and Peter I. Frazier. Scalable bayesian optimization of composite functions for image-based inverse problems in materials characterization. ArXiv, Sep 2026. URL: https://doi.org/10.48550/arxiv.2609.02126, doi:10.48550/arxiv.2609.02126. This article has 0 citations.

3. (yoon2026scalablebayesianoptimization pages 5-7): Da-Woon Yoon, Poompol Buathong, Chia-Hao Lee, Yu-Jia Zhang, David A. Muller, and Peter I. Frazier. Scalable bayesian optimization of composite functions for image-based inverse problems in materials characterization. ArXiv, Sep 2026. URL: https://doi.org/10.48550/arxiv.2609.02126, doi:10.48550/arxiv.2609.02126. This article has 0 citations.

4. (sinha2609portfoliobasedconstrainedmultiobjective pages 2-3): S. Sinha, Christofer Hardcastle, Robert Robinson, S. P. Padhy, Brent Vela, Douglas L. Allaire, and Raymundo Arróyave. Portfolio-based constrained multi-objective bayesian optimization for materials design. ArXiv, Sep 2609. URL: https://doi.org/10.48550/arxiv.2609.19550, doi:10.48550/arxiv.2609.19550. This article has 0 citations.

5. (sinha2609portfoliobasedconstrainedmultiobjective pages 8-10): S. Sinha, Christofer Hardcastle, Robert Robinson, S. P. Padhy, Brent Vela, Douglas L. Allaire, and Raymundo Arróyave. Portfolio-based constrained multi-objective bayesian optimization for materials design. ArXiv, Sep 2609. URL: https://doi.org/10.48550/arxiv.2609.19550, doi:10.48550/arxiv.2609.19550. This article has 0 citations.

6. (sinha2609portfoliobasedconstrainedmultiobjective pages 11-13): S. Sinha, Christofer Hardcastle, Robert Robinson, S. P. Padhy, Brent Vela, Douglas L. Allaire, and Raymundo Arróyave. Portfolio-based constrained multi-objective bayesian optimization for materials design. ArXiv, Sep 2609. URL: https://doi.org/10.48550/arxiv.2609.19550, doi:10.48550/arxiv.2609.19550. This article has 0 citations.

7. (taherimousavi2026alloygenaphysicsgrounded pages 9-11): S. Mohadeseh Taheri-Mousavi and Bo Ni. Alloygen: a physics-grounded self-adaptive multi-agent framework for autonomous alloy design workflows in additive manufacturing. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10329502/v1, doi:10.21203/rs.3.rs-10329502/v1.

8. (taherimousavi2026alloygenaphysicsgrounded pages 1-4): S. Mohadeseh Taheri-Mousavi and Bo Ni. Alloygen: a physics-grounded self-adaptive multi-agent framework for autonomous alloy design workflows in additive manufacturing. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10329502/v1, doi:10.21203/rs.3.rs-10329502/v1.

9. (taherimousavi2026alloygenaphysicsgrounded pages 4-6): S. Mohadeseh Taheri-Mousavi and Bo Ni. Alloygen: a physics-grounded self-adaptive multi-agent framework for autonomous alloy design workflows in additive manufacturing. Unknown journal, Aug 2026. URL: https://doi.org/10.21203/rs.3.rs-10329502/v1, doi:10.21203/rs.3.rs-10329502/v1.

10. (hammond2026exploitingseparabilityin pages 4-6): J. E. Hammond, T. Soderstrom, B. Korgel, and Michael Baldea. Exploiting separability in multi-scale grey-box bayesian optimization. ArXiv, Aug 2026. URL: https://doi.org/10.48550/arxiv.2608.03045, doi:10.48550/arxiv.2608.03045. This article has 0 citations.

11. (hammond2026exploitingseparabilityin pages 3-4): J. E. Hammond, T. Soderstrom, B. Korgel, and Michael Baldea. Exploiting separability in multi-scale grey-box bayesian optimization. ArXiv, Aug 2026. URL: https://doi.org/10.48550/arxiv.2608.03045, doi:10.48550/arxiv.2608.03045. This article has 0 citations.

12. (hammond2026exploitingseparabilityin pages 1-3): J. E. Hammond, T. Soderstrom, B. Korgel, and Michael Baldea. Exploiting separability in multi-scale grey-box bayesian optimization. ArXiv, Aug 2026. URL: https://doi.org/10.48550/arxiv.2608.03045, doi:10.48550/arxiv.2608.03045. This article has 0 citations.

13. (hammond2026exploitingseparabilityin pages 6-8): J. E. Hammond, T. Soderstrom, B. Korgel, and Michael Baldea. Exploiting separability in multi-scale grey-box bayesian optimization. ArXiv, Aug 2026. URL: https://doi.org/10.48550/arxiv.2608.03045, doi:10.48550/arxiv.2608.03045. This article has 0 citations.

14. (wakabayashi2608bayesianoptimizationfor pages 8-10): Yuki K. Wakabayashi and Takuma Otsuka. Bayesian optimization for self-driving materials laboratories: from algorithms to physics-informed workflows. ArXiv, Aug 2608. URL: https://doi.org/10.48550/arxiv.2608.26016, doi:10.48550/arxiv.2608.26016. This article has 0 citations.

15. (wakabayashi2608bayesianoptimizationfor pages 25-26): Yuki K. Wakabayashi and Takuma Otsuka. Bayesian optimization for self-driving materials laboratories: from algorithms to physics-informed workflows. ArXiv, Aug 2608. URL: https://doi.org/10.48550/arxiv.2608.26016, doi:10.48550/arxiv.2608.26016. This article has 0 citations.

16. (singh2026datascribeanainative pages 8-10): Divyanshu Singh, Doğuhan Sarıtürk, C. Lea, Md.Shafiqul Islam, Raymundo Arróyave, and V. Attari. Datascribe: an ai-native, policy-aligned web platform for multi-objective materials design and discovery. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2601.07966, doi:10.48550/arxiv.2601.07966. This article has 1 citations.

17. (singh2026datascribeanainative pages 1-2): Divyanshu Singh, Doğuhan Sarıtürk, C. Lea, Md.Shafiqul Islam, Raymundo Arróyave, and V. Attari. Datascribe: an ai-native, policy-aligned web platform for multi-objective materials design and discovery. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2601.07966, doi:10.48550/arxiv.2601.07966. This article has 1 citations.

18. (singh2026datascribeanainative pages 4-6): Divyanshu Singh, Doğuhan Sarıtürk, C. Lea, Md.Shafiqul Islam, Raymundo Arróyave, and V. Attari. Datascribe: an ai-native, policy-aligned web platform for multi-objective materials design and discovery. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2601.07966, doi:10.48550/arxiv.2601.07966. This article has 1 citations.

19. (singh2026datascribeanainative pages 6-8): Divyanshu Singh, Doğuhan Sarıtürk, C. Lea, Md.Shafiqul Islam, Raymundo Arróyave, and V. Attari. Datascribe: an ai-native, policy-aligned web platform for multi-objective materials design and discovery. ArXiv, Jan 2026. URL: https://doi.org/10.48550/arxiv.2601.07966, doi:10.48550/arxiv.2601.07966. This article has 1 citations.

20. (yoon2026scalablebayesianoptimization pages 8-11): Da-Woon Yoon, Poompol Buathong, Chia-Hao Lee, Yu-Jia Zhang, David A. Muller, and Peter I. Frazier. Scalable bayesian optimization of composite functions for image-based inverse problems in materials characterization. ArXiv, Sep 2026. URL: https://doi.org/10.48550/arxiv.2609.02126, doi:10.48550/arxiv.2609.02126. This article has 0 citations.

21. (triantafyllou2026reducedspacemultifidelitybayesian pages 11-14): Niki Triantafyllou, A. Bernardi, and Maria M. Papathanasiou. Reduced-space multi-fidelity bayesian optimization of process simulation models. ArXiv, Sep 2026. URL: https://doi.org/10.48550/arxiv.2609.17440, doi:10.48550/arxiv.2609.17440. This article has 0 citations.

22. (triantafyllou2026reducedspacemultifidelitybayesian pages 4-7): Niki Triantafyllou, A. Bernardi, and Maria M. Papathanasiou. Reduced-space multi-fidelity bayesian optimization of process simulation models. ArXiv, Sep 2026. URL: https://doi.org/10.48550/arxiv.2609.17440, doi:10.48550/arxiv.2609.17440. This article has 0 citations.
