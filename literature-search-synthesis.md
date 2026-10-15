# Deep Literature Search Synthesis: Autonomous AM Alloy Discovery

*Synthesis of eight Edison Scientific LITERATURE_HIGH queries, retrieved 2026-03-08. Full trajectories in [`edison-trajectories/`](edison-trajectories/).*

## Overview

This document synthesizes findings from a deep literature search covering eight technical pillars essential to building an autonomous additive manufacturing (AM) alloy discovery workflow. Combined with the [prior literature searches](edison-trajectories/) on AI/ML-accelerated alloy discovery and LPBF alloy development, these results map the full landscape of capabilities, gaps, and opportunities for a closed-loop autonomous pipeline at BYU VCL.

### New Edison trajectories

| # | Topic | File | Key Focus |
|---|---|---|---|
| 1 | Self-Driving Labs | [`self_driving_labs.md`](edison-trajectories/self_driving_labs.md) | Autonomous experimentation platforms, hardware/software architectures, SDL demonstrations in metals |
| 2 | Powder Production | [`powder_production.md`](edison-trajectories/powder_production.md) | Atomization methods, custom alloy powders, batch sizes, high-throughput screening approaches |
| 3 | Automated Characterization | [`automated_characterization.md`](edison-trajectories/automated_characterization.md) | High-throughput microscopy, mechanical testing, XRD, AI-driven microstructure analysis |
| 4 | CALPHAD for AM | [`calphad_alloy_design.md`](edison-trajectories/calphad_alloy_design.md) | Computational thermodynamics, printability criteria, Scheil analysis, ML+CALPHAD integration |
| 5 | ML for LPBF PSP | [`ml_process_structure_property.md`](edison-trajectories/ml_process_structure_property.md) | Process-structure-property ML models, Bayesian process optimization, in-situ monitoring |
| 6 | Digital Twins for AM | [`digital_twins_am.md`](edison-trajectories/digital_twins_am.md) | Thermal/melt pool simulation, residual stress, microstructure modeling, ML surrogates |
| 7 | Function Networks for BO | [`function_networks_bo.md`](edison-trajectories/function_networks_bo.md) | Frazier's BOFN framework, knowledge gradient, grey-box BO for multi-stage pipelines |
| 8 | LLM-Enhanced BO | [`llm_bayesian_optimization.md`](edison-trajectories/llm_bayesian_optimization.md) | LLAMBO, LILO (Meta AE), BORA, Reasoning BO, LLM priors for function networks |

---

## Key Findings by Pillar

### 1. Self-Driving Labs — The Orchestration Layer

The SDL landscape has exploded since 2022, with 100+ implementations cataloged globally. Current systems operate at Level 2–3 autonomy (human-on-the-loop). Key platforms relevant to alloy discovery:

- **A-Lab** (UC Berkeley/LBNL): 41/58 novel inorganic compounds synthesized in 17 days (71% success) — demonstrates feasibility of autonomous solid-state synthesis
- **APEX** (LLNL): First DED-based autonomous alloy discovery platform targeting ~48 samples/day with integrated grinding, polishing, microscopy, indentation, and compression
- **AMASE** (NIST/UMD): Real-time experiment-theory closed-loop CALPHAD updating — determined Sn-Bi eutectic with ~6× fewer experiments
- **AutoMAT**: Hierarchical autonomous search identified Ti-Al-V-Fe alloy with high specific strength, compressing ~2-year task to <1 week

**Software frameworks**: ChemOS 2.0, HELAO, ARES OS, and AlabOS provide orchestration; Bayesian optimization is the dominant decision-making approach; LLM-enabled agents are an emerging trend.

**Critical gap for VCL**: No existing SDL seamlessly integrates alloy design → powder atomization → LPBF → characterization in a single closed loop. The APEX platform at LLNL is closest but uses DED rather than LPBF. This gap is estimated at 5–10 years by current literature — representing the core VCL opportunity.

### 2. Powder Production — The Feedstock Bottleneck

Custom alloy powder production has historically been the critical bottleneck for high-throughput alloy screening. Key developments:

- **Ultrasonic atomization** (e.g., Amazemet rePowder) enables 1 g to few-kg batches in hours with high sphericity and narrow PSD — transformative for lab-scale screening
- **Conventional VIGA** requires 100–500 kg batches with weeks–months lead time — unsuitable for rapid screening
- **Powder blending** of elemental/pre-alloyed powders provides a rapid alternative for composition screening, though homogeneity and interparticle segregation remain challenges
- **Multi-tiered screening strategy** emerging in literature: computational CALPHAD screening → DED combinatorial synthesis (~1,000 compositions/day) → ultrasonic atomization for LPBF validation of top candidates

**VCL implication**: Ultrasonic atomization (Amazemet or similar) is the key enabling technology for closing the powder production gap in a closed-loop pipeline. BYU should prioritize acquisition of a small-batch atomizer.

### 3. Automated Characterization — Closing the Measurement Loop

High-throughput characterization has achieved dramatic speedups but sample preparation remains the dominant bottleneck:

- **EBSD acquisition** no longer limiting (CMOS detectors); automated dry electropolishing + batch EBSD achieved 600+ datasets in ~10 labor hours (482× speedup)
- **AI-driven microstructure analysis**: Correlative SEM-EBSD labeling enables CNN training without manual annotation; ensemble models generalize across imaging modes with <0.5 µm grain-size error
- **Robotic sample prep**: RASI system (BAM) uses UR5e robot for full grinding/polishing/etching/imaging automation; HT-READ (UCSD) wagon-wheel geometry enables 50 alloys/24 h
- **Nanoindentation mapping**: High-speed arrays (up to 8,000 indents/hour) enable combinatorial mechanical property mapping across graded/multi-composition samples
- **Multimodal integration**: BIRDSHOT consortium achieved 13–46× modality speedups with Bayesian optimization finding Pareto sets in 5 iterations from 50,000 candidates

**VCL implication**: Automated sample preparation (robotic polishing) and AI-driven image analysis are the two highest-leverage investments for characterization throughput. Off-the-shelf solutions exist (RASI-style robot, correlative EBSD-CNN pipelines).

### 4. CALPHAD for AM — Computational Alloy Screening

CALPHAD-based printability prediction is well-established with a mature toolkit:

- **Printability criteria**: Freezing range (FR), Kou criterion (SCI), crack susceptibility coefficient (CSC), critical temperature range (CTR), and simplified RDG (sRDG) — all computable from Scheil simulations
- **Key limitation**: Standard Scheil assumes equilibrium-like conditions; at LPBF cooling rates (10⁵–10⁷ K/s), solute trapping, kinetic undercooling, and non-equilibrium phases violate these assumptions
- **ML acceleration**: ML interatomic potentials (M3GNet, CHGNet, MACE) achieve >1,000× DFT speedups; neural-network surrogates for thermal models enable ~1,000× faster printability map construction
- **Software**: Thermo-Calc (dominant, TC-Python API), pycalphad/ESPEI (open-source, Bayesian parameter optimization), OpenCalphad

**VCL implication**: CALPHAD + ML surrogates form the computational screening backbone. pycalphad/ESPEI provides an open-source path; Thermo-Calc academic license provides the broadest database coverage. The non-equilibrium limitation is a research opportunity — developing rapid-solidification-aware CALPHAD screening criteria for LPBF.

### 5. ML for Process-Structure-Property — Data-Driven LPBF Optimization

ML models now span the full PSP chain for LPBF:

- **Process → Defect**: Tree ensembles (CatBoost, XGBoost) achieve ~92% accuracy for defect classification; CNNs reach ~98% for larger defect detection from imaging data
- **Process → Microstructure**: Physics-informed approaches (PINNs, phase-field+ML hybrids) reduce data requirements; cGANs and 3D U-Nets generate synthetic microstructures from process parameters
- **Microstructure → Properties**: CNN-based MPR-Net achieves R² ≈ 0.96 for tensile strength prediction from metallography; graph neural networks capture grain-topology effects
- **Process optimization**: MOBO with GP surrogates converges in ~6 iterations for SS316L (0.2–0.37% porosity, 224–235 HV); active learning cuts test error by ~30%
- **Transfer learning**: Cross-alloy transfer (IN718→IN625) achieves R = 0.95 with teacher-student models; alloy-agnostic melt-pool classifiers reach 96% accuracy

**Critical gap**: No integrated ML system autonomously detects, classifies, and corrects defects in real-time LPBF production. Composition-based defect datasets are rare — VCL could contribute novel datasets connecting alloy chemistry to LPBF defect formation.

### 6. Digital Twins — Simulation-Guided Manufacturing

Physics-based simulation and ML surrogates are converging to enable real-time digital twins:

- **Simulation accuracy**: FEM thermal models achieve ±2–7% melt pool error; high-fidelity CFD ±10–20% but computationally prohibitive for part-scale; analytical models ±20–50% but near-instantaneous
- **ML surrogates**: PINNs achieve <2.5% MAPE for temperature with 8.5× faster training; GNNs reach 3.77% MAPE with near-instantaneous inference vs. ~4 hours FEA; POD-GPR ROM achieves ±0.001 mm distortion with ~1,800× speedup
- **Open-source tools**: OpenFOAM, MOOSE framework, ExaCA (grain structure), SPPARKS (KMC microstructure)
- **Commercial tools**: ANSYS Additive Suite, Simufact Additive, Autodesk Netfabb, FLOW-3D AM

**VCL implication**: ML surrogates are mature enough to embed in a closed-loop workflow for real-time process guidance. MOOSE + ExaCA provide an open-source simulation stack. A PINN or GNN surrogate trained on high-fidelity simulation data could provide the real-time digital twin layer.

### 7. Function Networks — The Decision Engine for Multi-Stage Pipelines

Peter Frazier and collaborators (Astudillo, Buathong, Daulton, Balandat) have developed **Bayesian optimization over function networks (BOFN)** — a framework that decomposes complex multi-stage optimization into directed acyclic graphs (DAGs) of interconnected sub-functions, each modeled with its own Gaussian process:

- **Core idea**: Instead of treating the full pipeline (composition → powder → LPBF → characterization) as a single black-box, BOFN places independent GPs on each stage and leverages intermediate observations (powder PSD, in-situ melt pool data, phase ID) to update beliefs about downstream performance. This "instantly reduces the effective dimensionality" by a factor equal to the number of nodes.
- **Key papers**: Astudillo & Frazier (2021) *Bayesian Optimization of Function Networks* (73 citations), Buathong et al. (2023) *BO of Function Networks with Partial Evaluations* — introduces **p-KGFN**, a cost-aware knowledge gradient that selectively evaluates cheap upstream nodes (CALPHAD screening) before expensive downstream nodes (LPBF builds).
- **Performance**: EI-FN substantially outperforms standard BO, with improvements ranging from ~5% to orders of magnitude, particularly for higher-dimensional multi-stage problems.
- **Implementation**: BoTorch (PyTorch-based, open-source, Meta) provides the building blocks — MC acquisition functions, `fantasize()` API, composite objectives. Ax platform provides experiment management on top.
- **Comparison**: BOFN is complementary to multi-fidelity BO (which uses cheaper approximate evaluations at varying fidelities) and multi-objective BO (which optimizes Pareto fronts). A function network node could itself be evaluated at multiple fidelities (e.g., CALPHAD vs. DFT for thermodynamic predictions).

**VCL implication**: The autonomous alloy discovery pipeline is a natural function network — alloy composition → powder quality → LPBF microstructure → mechanical properties. BOFN with p-KGFN would enable **cost-aware partial evaluations** (run only CALPHAD screening without committing to LPBF builds when information gain is insufficient), **early termination** of unpromising candidates, and **rational budget allocation** across pipeline stages. BoTorch provides a production-ready implementation. This framework should be the decision engine at the core of VCL's SDL orchestration layer.

---

## The Autonomous AM Alloy Discovery Pipeline — Gap Analysis

Mapping the eight pillars against a closed-loop autonomous pipeline reveals where technology is mature vs. where VCL fills critical gaps:

| Pipeline Stage | Technology Readiness | Key Tools Available | VCL Opportunity |
|---|---|---|---|
| **1. AI alloy screening** | ★★★★☆ High | CALPHAD (Thermo-Calc, pycalphad), ML surrogates, BO/active learning | Integrate CALPHAD printability criteria with ML property prediction in a unified screening loop |
| **2. Powder production** | ★★★☆☆ Medium | Ultrasonic atomization (Amazemet), powder blending | First lab to embed automated ultrasonic atomization directly in an autonomous loop |
| **3. LPBF printing** | ★★★★☆ High | Commercial LPBF systems, DOE-guided parameter optimization | Automated build plate loading, multi-composition builds, process monitoring integration |
| **4. In-situ monitoring** | ★★★☆☆ Medium | Thermal imaging, melt pool cameras, acoustic sensors + ML | Closed-loop defect detection → parameter adjustment during builds |
| **5. Automated characterization** | ★★★☆☆ Medium | Robotic polishing (RASI), EBSD, nanoindentation, AI segmentation | Integrate characterization robots with SDL orchestration software |
| **6. Data → next experiment** | ★★★★★ Very High | BOFN/p-KGFN (BoTorch), LLAMBO, LILO, BORA, Reasoning BO | Deploy **LLM-enhanced BOFN** — function network BO with LLM warmstarting, NL feedback interpretation, and cost-aware stage selection |
| **7. Full pipeline integration** | ★☆☆☆☆ Low | No existing platform achieves this | **Core VCL differentiator** — first AI→powder→LPBF→characterization closed loop |

### What makes VCL unique

Based on this literature search, no research group has demonstrated a fully integrated autonomous pipeline combining all seven stages above. The closest platforms are:

1. **APEX (LLNL)** — uses DED not LPBF, limited alloy systems, prototype stage
2. **A-Lab (Berkeley)** — inorganic powders, not metals/AM
3. **AMASE (NIST)** — thin-film screening, not bulk alloys
4. **PAL 2.0 (JHU APL)** — arc-melting validation, not AM

VCL's proposed pipeline fills the "processability gap" between computational alloy design and validated LPBF parts — a gap that every review paper identifies as the critical missing link.

---

## Recommended Next Steps

1. **Acquire small-batch atomizer** — Amazemet rePowder or equivalent ultrasonic atomizer for 1 g–5 kg custom alloy powders
2. **Set up CALPHAD screening pipeline** — pycalphad/ESPEI + Thermo-Calc TC-Python for automated Scheil-based printability screening
3. **Deploy automated characterization** — robotic sample prep (UR robot + polisher) + correlative SEM-EBSD with CNN segmentation
4. **Implement LLM-enhanced BOFN decision engine** — Use BoTorch BOFN (EI-FN / p-KGFN) with LLM warmstarting (LLAMBO-style) and NL feedback interpretation (LILO-style). See [`bofn-llm-bo-synthesis.md`](bofn-llm-bo-synthesis.md) for architecture and implementation path.
5. **Build SDL orchestration layer** — Adapt Ax platform or custom Python framework for experiment planning, integrating LLM-BOFN for cost-aware stage selection
6. **Develop ML surrogates** — Train PINN/GNN on melt pool simulations for real-time process guidance
7. **Start with a constrained demonstration** — 2–3 alloy system (e.g., Al-Si-Mg family) with known CALPHAD databases to validate the pipeline before expanding to novel compositions

---

## References to Edison Trajectories

All findings are sourced from Edison Scientific LITERATURE_HIGH queries with full citations in the individual trajectory files:

- [Self-Driving Labs](edison-trajectories/self_driving_labs.md)
- [Powder Production](edison-trajectories/powder_production.md)
- [Automated Characterization](edison-trajectories/automated_characterization.md)
- [CALPHAD for AM](edison-trajectories/calphad_alloy_design.md)
- [ML for LPBF PSP](edison-trajectories/ml_process_structure_property.md)
- [Digital Twins for AM](edison-trajectories/digital_twins_am.md)
- [Function Networks for BO](edison-trajectories/function_networks_bo.md)
- [LLM-Enhanced Bayesian Optimization](edison-trajectories/llm_bayesian_optimization.md)
- [AI/ML Alloy Discovery (prior)](edison-trajectories/literature_alloy_discovery.md)
- [LPBF Alloy Development (prior)](edison-trajectories/literature_lpbf_alloys.md)
