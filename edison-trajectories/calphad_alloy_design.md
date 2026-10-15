# CALPHAD-Guided Alloy Design for Additive Manufacturing

*Edison Scientific LITERATURE_HIGH query*

Question: What is the recent literature (2022-2026) on using CALPHAD (CALculation of PHAse Diagrams) methods and computational thermodynamics for designing alloys specifically for additive manufacturing? Cover: (1) CALPHAD-based printability criteria — solidification range, cracking susceptibility indices, Scheil solidification analysis, phase stability under rapid cooling, (2) integration of CALPHAD with machine learning for alloy screening — using thermodynamic features as ML model inputs, surrogate models for CALPHAD calculations, (3) available CALPHAD software and databases — Thermo-Calc, FactSage, Pandat, OpenCalphad, pycalphad — and their application to AM alloy design, (4) high-throughput CALPHAD workflows — batch calculations, automated phase diagram exploration, composition optimization, (5) validation of CALPHAD predictions against experimental LPBF results — where do predictions succeed and where do they fail for AM conditions? What are the key thermodynamic criteria that predict LPBF printability? How reliable is CALPHAD for non-equilibrium solidification conditions in LPBF?


# CALPHAD Methods and Computational Thermodynamics for Additive Manufacturing Alloy Design: A Review of Recent Literature (2022–2026)

## 1. CALPHAD-Based Printability Criteria

The recent literature has established a suite of thermodynamic and solidification-derived criteria, computed primarily from CALPHAD-based Scheil–Gulliver simulations, to predict the printability of alloys for additive manufacturing (AM), particularly laser powder bed fusion (LPBF).

### 1.1 Solidification Range and Freezing Range

The **freezing range (FR)**, defined as FR = T_Liquidus − T_Solidus (where the solidus is typically taken at solid fraction f_s ≈ 0.99 from Scheil simulations), is the most fundamental thermodynamic indicator. Larger freezing ranges correlate with wider mushy zones, more severe microsegregation, and higher susceptibility to solidification cracking (yang2023designmethodologyfor pages 10-14, wu2025advancesincrack pages 9-12). Liu et al. (2024) demonstrated that alloys with narrow solidification ranges such as IN625 are more readily printable by LPBF, while alloys with wide ranges such as CM247LC and AA7075 are prone to severe cracking (liu2024alloydesignfor pages 18-19). Scaglione et al. (2022) used Thermo-Calc Scheil simulations to map the solidification window across Al-Mg-Si-Er composition space, identifying composition regions (e.g., ~13–14 wt.% Si, 3–5 wt.% Mg) that minimize the solidification temperature interval and reduce segregation-related defects (scaglione2022solidificationcalculationsof pages 14-16).

### 1.2 Cracking Susceptibility Indices

Multiple cracking susceptibility indices have been adopted and refined for AM applications:

- **Kou Criterion (SCI)**: Defined from the slope dT/d(√f_s) evaluated near the end of solidification. A steeper slope implies longer interdendritic liquid channels, reduced liquid feeding, and higher cracking susceptibility. It is widely applied for LPBF aluminum alloys but has a key limitation: it does not account for rapid solidification effects such as solute trapping (wu2025advancesincrack pages 9-12, singh2025understandingsolidificationcrackingb pages 23-27).

- **Crack Susceptibility Coefficient (CSC)**: The ratio of time spent in the vulnerable late solidification stage (f_s = 0.90→0.99) to the time available for stress relaxation (f_s = 0.40→0.90). At AM cooling rates, temperature-based analogs from Scheil curves are used. Wang et al. (2025) demonstrated CSC for Cu-Inconel bimetallic systems, identifying interlayer compositions (65 wt.% In625) that minimize CSC and produce crack-free interfaces (wu2025advancesincrack pages 12-14, wang2025calphadguidedinterlayerdesign pages 1-2).

- **RDG and simplified RDG (sRDG)**: The Rappaz–Drezet–Gremaud criterion evaluates critical deformation rates for cavitation based on interdendritic feeding and shrinkage; the sRDG is a Scheil-computable surrogate requiring fewer material properties (yang2023designmethodologyfor pages 5-10, yang2023designmethodologyfor pages 10-14).

- **Critical Temperature Range (CTR)**: Defined as CTR = T(f_s = 0.99) − T(f_s = 0.95), quantifying the late-stage solidification interval most critical for cracking. Assi et al. (2024) used CTR alongside solidification mode (F, FA, AF, A) to screen austenitic stainless steels for LPBF, finding that primary ferrite formation (FA mode, Creq/Nieq ≈ 1.48) reduces solidification cracking (assi2024designandassessment pages 5-7).

- **HR-DR Model**: For Ni-based superalloys, the heat resistance–deformation resistance model quantifies interdendritic versus dendrite-core differences in solidus temperature and yield strength to predict cracking tendency (wu2025advancesincrack pages 12-14).

- **Strain-Age Cracking (SAC)**: Expressed through dV_γ′/dT or the composition-based index M_sac = W_Al + 0.5W_Ti + 0.3W_Nb + 0.15W_Ta, capturing post-build cracking risk from γ′ precipitation (wu2025advancesincrack pages 12-14, wu2025advancesincrack pages 9-12).

Yang et al. (2023) systematically combined FR, CSC, iCSC, sRDG, and Kou criterion maps with equilibrium and Scheil phase predictions to create composition feasibility diagrams for functionally graded materials, showing that crack-free AM correlates with small FR, low CSC/iCSC/sRDG, and eutectic reactions occurring early in solidification (yang2023designmethodologyfor pages 10-14, yang2023designmethodologyfor pages 5-10).

| Criterion | Definition/Formula | What it measures | Key references |
|---|---|---|---|
| Freezing Range (FR) | FR = T_L − T_S (often T_S at f_s ≈ 0.99 from Scheil) | Mushy-zone width and segregation severity; larger FR correlates with higher hot-crack risk | (wu2025advancesincrack pages 9-12, yang2023designmethodologyfor pages 10-14, liu2024alloydesignfor pages 18-19) |
| Kou Criterion (SCI) | SCI ∝ dT/d(√f_s) evaluated near end of solidification (f_s → 1) | Ease of interdendritic liquid feeding; higher slope implies longer liquid films and higher cracking risk | (wu2025advancesincrack pages 9-12, yang2023designmethodologyfor pages 10-14) |
| Crack Susceptibility Coefficient (CSC) | CSC = Δt(0.90→0.99)/Δt(0.40→0.90); at high cooling rates, use temperature-based analogs from Scheil | Relative time spent in vulnerable late stage versus available stress-relaxation time; lower is better | (wu2025advancesincrack pages 12-14, yang2023designmethodologyfor pages 10-14) |
| Integrated CSC (iCSC) | iCSC = ∫(late stage) f_s dT (e.g., X2→X3) | Cumulative vulnerability near the end of solidification; emphasizes last-stage cracking risk | (yang2023designmethodologyfor pages 10-14, yang2023designmethodologyfor pages 5-10) |
| RDG criterion | Critical deformation rate ε̇_p,max for cavitation based on interdendritic feeding, shrinkage, and deformation | Ability of mushy zone to accommodate strain without cavitation; predicts hot-tear onset | (yang2023designmethodologyfor pages 5-10, wu2025advancesincrack pages 9-12) |
| Simplified RDG (sRDG) | Scheil-based surrogate using shrinkage-driven pressure drop only (reduced input requirements) | Relative hot-tear tendency from feeding resistance without full material-property set | (yang2023designmethodologyfor pages 5-10, yang2023designmethodologyfor pages 10-14) |
| Heat Cracking Sensitivity (HCS) | Mechanical/thermal index quantifying susceptibility under thermal strain; formulation varies by study | Propensity for crack initiation/growth due to thermal contraction and insufficient feeding | (wu2025advancesincrack pages 9-12) |
| Critical Temperature Range (CTR) | CTR = T(f_s = 0.99) − T(f_s = 0.95) from Scheil | Width of late-stage solidification interval driving solidification cracking risk | (assi2024designandassessment pages 5-7) |
| HR–DR model | Heat resistance ΔT_S = T_S,ID − T_S,DC; deformation resistance Δσ_y = σ_y,ID − σ_y,DC | Interdendritic vs dendrite-core resistance to cracking; larger ΔT_S/Δσ_y imply higher cracking risk | (wu2025advancesincrack pages 12-14) |
| Strain-Age Cracking (SAC) index | Kinetic: dV_{γ'}/dT; composition-based Msac = W_Al + 0.5W_Ti + 0.3W_Nb + 0.15W_Ta | Risk of post-build cracking during aging due to γ' precipitation and lattice mismatch effects | (wu2025advancesincrack pages 12-14, wu2025advancesincrack pages 9-12) |


*Table: Summary of CALPHAD/Scheil-derived criteria used to predict alloy printability for AM, with concise definitions and what each measures. Citations point to 2022–2026 sources detailing formulation and application.*

### 1.3 Scheil Solidification Analysis and Phase Stability

Scheil–Gulliver solidification simulations provide temperature versus solid fraction (T–f_s) curves that serve as the foundation for nearly all the above indices. Chechik et al. (2023) compared three Scheil variants—classic Scheil, back-diffusion Scheil, and solute-trapping Scheil—for Ni superalloys. They found that the simplest classic Scheil is often sufficient, but that solute-trapping variants predict smaller freezing ranges and reduced segregation under LPBF conditions (~10⁵–10⁶ K/s), while back diffusion is more significant at slower L-DED cooling rates (chechik2023toolsforthe pages 19-21, chechik2023toolsforthe pages 6-9). Uba et al. (2025) used Scheil T–f_s curves to evaluate both initial (f_s < 0.1, affected by dispersoid formation and heterogeneous nucleation) and final-stage solidification behavior for Al 7xxx alloys, computing indices including TCR and HSI to design grain-refined, eutectic-solidification-enhanced compositions for LPBF (uba2025enhancingtheprintability pages 7-10).

## 2. Integration of CALPHAD with Machine Learning for Alloy Screening

### 2.1 Thermodynamic Features as ML Inputs

CALPHAD outputs serve as physics-rich features for machine learning models in alloy design. Common thermodynamic descriptors include phase fractions, transformation temperatures, liquidus and solidus temperatures, Gibbs free energies, chemical potentials, molar volumes, and solidification interval data from Scheil simulations (josyula2025calphadandmachine pages 39-43, assi2022alloysdesignfor pages 48-52). For Ni-based superalloys, JMatPro/CALPHAD-derived features such as melting temperature, γ′ dissolution temperature, γ′ fraction, γ/γ′ lattice mismatch, and TCP content are used for computational screening (wu2025advancesincrack pages 22-26). Wang et al. (2025) combined CALPHAD-derived Scheil segregation profiles with ML models predicting stacking fault energy to assess twinning propensity in AM 316L stainless steel (wang2023integratedcomputationalmaterials pages 32-38).

### 2.2 Surrogate Models for CALPHAD Calculations

Several approaches accelerate CALPHAD calculations using ML surrogates. Sheikh et al. (2025) developed a deep-learning surrogate for thermal/melt-pool models that achieves a **1,000-fold speedup** without loss of accuracy, enabling rapid construction of printability maps across the Co-Cr-Fe-Mn-Ni HEA space (sheikh2025highthroughputalloyand pages 1-3, sheikh2025highthroughputalloyand pages 3-5). Zhu et al. (2025) used machine learning interatomic potentials (M3GNet, CHGNet, MACE, ORB) to replace DFT in the CALPHAD/ATAT pipeline, achieving speedups exceeding **three orders of magnitude** while maintaining acceptable accuracy for phase stability predictions (zhu2025acceleratingcalphadbasedphase pages 1-2). The PyCalphad/ESPEI ecosystem integrates with SIPFENN, a deep neural network surrogate for DFT formation energies, enabling rapid generation of CALPHAD-compatible thermodynamic descriptions (olson2024genomicmaterialsdesign pages 29-34). Wang et al. (2025) demonstrated ML surrogates for CALPHAD outputs (using RF and XGBoost) trained on 60,480 compositions with CALPHAD-derived features including phase fractions and precipitation temperatures, achieving PREN prediction RMSE of ~0.004 (rahman2025reviewmachinelearning pages 25-26).

### 2.3 Bayesian Optimization with CALPHAD

Sundar et al. (2025) demonstrated multi-objective Bayesian optimization coupled with high-throughput CALPHAD calculations to discover Ni-Cr-Co-Al-Fe alloys with optimized CTE and sigma-phase dissolution temperatures, finding candidate alloys by sampling only ~7% of the composition space (sundar2025calphadbasedbayesianoptimization pages 1-2). Zhang et al. (2022) used Bayesian optimization with CALPHAD-generated Scheil solidification data to optimize Ti-modified Al-Si-Mg-Sr casting alloys, constructing composition–microstructure–property relationships (wang2023integratedcomputationalmaterials pages 32-38).

## 3. CALPHAD Software and Databases for AM Alloy Design

| Software/Tool | Type (Commercial/Open-source) | Key Databases for AM | AM-Relevant Capabilities | Representative References |
|---|---|---|---|---|
| Thermo-Calc (TC-Python, DICTRA, Scheil) | Commercial | TCHEA1/3; TCFE/TCNI; TCNOBL1 (examples) | Equilibrium/metastable phase diagrams; Scheil solidification; DICTRA 1D diffusion/back-diffusion; precipitation kinetics (TC-PRISMA); high-throughput scripting via TC-Python for AM workflows | (odetola2024exploringhighentropy pages 18-20, wang2023integratedcomputationalmaterials pages 32-38, scaglione2022solidificationcalculationsof pages 2-4, martucci2023ongoingchallengesof pages 3-4) |
| FactSage | Commercial | FactSage thermodynamic/kinetic databases (various) | Multicomponent equilibrium and phase diagrams; Scheil-style solidification; applied in AM alloy thermodynamics screening | (martucci2023ongoingchallengesof pages 3-4, josyula2025calphadandmachine pages 39-43, assi2022alloysdesignfor pages 211-213) |
| Pandat | Commercial | Pandat thermodynamic/kinetic databases (various) | Equilibrium phase stability; Scheil solidification; kinetic simulations; used in AM alloy design studies | (martucci2023ongoingchallengesof pages 3-4, josyula2025calphadandmachine pages 39-43) |
| OpenCalphad | Open-source | Reads TDB-format databases (community/industrial) | Programmatic equilibrium calculations; open framework for custom AM workflows and database testing | (martucci2023ongoingchallengesof pages 3-4, josyula2025calphadandmachine pages 39-43, olson2024genomicmaterialsdesign pages 29-34) |
| pycalphad/ESPEI | Open-source | Reads TDB; ESPEI for parameterization/UQ | Scripted Gibbs energy minimization; batch/high-throughput CALPHAD; Bayesian parameter optimization and uncertainty quantification; integrates with DFT/ML pipelines for AM | (olson2024genomicmaterialsdesign pages 29-34, martucci2023ongoingchallengesof pages 3-4) |
| JMatPro | Commercial | JMatPro internal databases | Thermophysical properties and phase fraction predictions (e.g., Tm, γ′ fraction/dissolution) used alongside CALPHAD features in AM screening | (wu2025advancesincrack pages 22-26, martucci2023ongoingchallengesof pages 3-4) |
| MatCalc | Commercial (academic licenses) | MatCalc precipitation databases | Precipitation kinetics and transformation modeling to support AM heat-treatment and microstructure design | (martucci2023ongoingchallengesof pages 3-4) |


*Table: Summary of widely used CALPHAD software for additive manufacturing alloy design, highlighting databases, AM-relevant capabilities (e.g., Scheil, DICTRA, HT scripting), and representative literature. This helps select appropriate tools and workflows for high-throughput, non-equilibrium AM alloy development.*

**Thermo-Calc** is the most widely used platform in the AM alloy design literature, with its TC-Python API enabling high-throughput scripted calculations, Scheil solidification simulations, and coupling with DICTRA for diffusion-controlled transformation modeling (wang2023integratedcomputationalmaterials pages 32-38, odetola2024exploringhighentropy pages 18-20). Databases such as TCHEA (versions 1–6) for high-entropy alloys and TCFE/TCNI for steels and Ni-based alloys are commonly employed (odetola2024exploringhighentropy pages 18-20, scaglione2022solidificationcalculationsof pages 2-4). Thermo-Calc's capability to predict credibility metrics (FAB, FAT) assessing database completeness for binary/ternary descriptions helps users gauge prediction reliability (odetola2024exploringhighentropy pages 18-20).

**Open-source alternatives** are gaining traction. PyCalphad provides programmatic, symbolic thermodynamic models and a decoupled equilibrium solver, while ESPEI automates parameter generation and Bayesian uncertainty quantification (olson2024genomicmaterialsdesign pages 29-34). OpenCalphad offers an open framework compatible with TDB-format databases (martucci2023ongoingchallengesof pages 3-4). These open-source tools enable custom AM workflows, reproducible research, and integration with DFT and ML pipelines. Martucci et al. (2023) noted that both commercial (Thermo-Calc, JMatPro, MatCalc, Pandat) and open-source (OpenCalphad, PyCalphad) tools are used for LPBF alloy design, with the choice depending on database availability and workflow requirements (martucci2023ongoingchallengesof pages 3-4, martucci2023developmentandcharacterisation pages 15-16).

## 4. High-Throughput CALPHAD Workflows

### 4.1 Batch Calculations and Automated Exploration

Ghassemali and Conway (2022) reviewed high-throughput CALPHAD (HT-CALPHAD) as a backbone for accelerated metallurgy, highlighting automated sweeps across vast composition spaces that produce datasets of temperatures, phase fractions, lattice parameters, and solutionizing windows to rank compositions into "islands of interest" (ghassemali2022highthroughputcalphada pages 2-4). Odetola et al. (2024) reported large-scale screening studies employing CALPHAD to compute equilibrium phases for 130,000 equiatomic compositions, demonstrating the scale achievable with batch calculations (odetola2024exploringhighentropy pages 18-20).

### 4.2 Integrated Frameworks for AM

Sheikh et al. (2025) introduced a comprehensive framework integrating CALPHAD-based material property predictions with thermal models and defect criteria to produce printability maps for LPBF. A tri-objective Pareto screening first filtered compositions for single-FCC phase stability (from CALPHAD), low hot-cracking susceptibility, and low balling susceptibility, followed by printability map construction using analytical and neural-network thermal models (sheikh2025highthroughputalloyand pages 40-42). Wu et al. (2025) described the HT-READ closed-loop workflow combining CALPHAD/ML screening, rapid sample synthesis (including 3D printing), automated characterization, and iterative redesign (wu2025advancesincrack pages 22-26). Gao et al. (2022) developed Malac-Distmas, a machine learning–accelerated distributed task management system for high-throughput CALPHAD computation, enabling coupling with various software for batch solidification simulations (ghassemali2022highthroughputcalphada pages 2-4).

### 4.3 Composition Optimization

Assi et al. (2022, 2024) demonstrated a multi-objective genetic algorithm–driven workflow using CALPHAD (Thermo-Calc/TC-Python) for equilibrium and Scheil simulations, coupled with ML meta-models and physical models, to optimize austenitic stainless steel compositions for LPBF. Objectives included maximizing austenite stability, minimizing CTR, and controlling solidification mode (assi2022alloysdesignfor pages 48-52, assi2024designandassessment pages 5-7).

## 5. Validation of CALPHAD Predictions Against Experimental LPBF Results

### 5.1 Where CALPHAD Predictions Succeed

CALPHAD-based methods reliably predict which phases form during solidification and provide qualitatively correct rankings of cracking susceptibility across compositions. Sargent (2024) demonstrated that CALPHAD-based ICME workflows coupling process models with DICTRA solidification simulations could predict solidification cracking susceptibility trends validated against 25 experimental crack-length measurements in Al-Cu alloys and showed a linear relationship between gross energy density and SCS in SS316L (sargent2024integratedcomputationaland pages 40-45, sargent2024integratedcomputationalanda pages 45-49). Wang et al. (2025) validated CALPHAD-predicted CSC against experimental Cu-Inconel bimetallic WAAM builds, successfully identifying the optimal interlayer composition for crack-free joints (wang2025calphadguidedinterlayerdesign pages 1-2). Sun et al. (2022) used thermodynamics-guided design to solve the hot cracking problem in IN738LC, using non-equilibrium solute partitioning analysis to guide Si content modification in a landmark Nature Communications study (sun2022thermodynamicsguidedalloyand pages 1-2).

### 5.2 Where CALPHAD Predictions Fail

CALPHAD predictions face significant challenges under LPBF's extreme non-equilibrium conditions. The key limitations include:

**Solute trapping**: At LPBF cooling rates (10⁵–10⁷ K/s) and solidification front velocities (~1 m/s), solute trapping causes the effective partition coefficient to approach unity, invalidating the local equilibrium assumption of standard Scheil simulations (singh2025understandingsolidificationcrackingb pages 23-27, singh2025understandingsolidificationcrackinga pages 17-23). Chechik et al. (2023) showed that solute-trapping Scheil variants can differ significantly from classic Scheil for L-PBF conditions, predicting smaller freezing ranges (chechik2023toolsforthe pages 19-21, chechik2023toolsforthe pages 6-9).

**Kinetic undercooling and non-equilibrium phases**: Standard CALPHAD does not capture kinetic undercooling at the solidification front, which can lead to morphological transitions (planar → cellular → dendritic → equiaxed → banded) and formation of non-equilibrium or metastable phases not predicted by equilibrium phase diagrams (singh2025understandingsolidificationcrackingb pages 17-23, martucci2023developmentandcharacterisation pages 15-16).

**Scheil assumptions**: The Scheil–Gulliver model assumes infinite liquid diffusion, zero solid back-diffusion, and local interface equilibrium—all of which are approximations for LPBF. Real LPBF shows less segregation than Scheil predicts because both liquid and solid diffusion contribute to mass redistribution. Scheil also cannot quantitatively account for changes in cooling rate or cyclic remelting encountered during AM (martucci2023ongoingchallengesof pages 3-4, sargent2024integratedcomputationalanda pages 40-45).

**Incomplete kinetic and thermophysical data**: Scarce thermophysical data for liquid alloys and incomplete multicomponent mobility assessments limit DICTRA and kinetic model accuracy. Numerical convergence issues, deficient mobility databases, and simplified geometry assumptions persist (sargent2024integratedcomputationaland pages 45-49, martucci2023developmentandcharacterisation pages 15-16).

**Weldability ≠ Printability**: Liu et al. (2024) critically demonstrated that conventional weldability criteria are not always applicable for estimating LPBF printability. For example, boron is beneficial in casting Ni superalloys but detrimental in LPBF because it lowers solidus temperature and promotes hot cracking via stabilized liquid films (liu2024alloydesignfor pages 1-3).

### 5.3 Improving CALPHAD Reliability for AM

Recent advances improve CALPHAD predictions for non-equilibrium conditions: (1) coupling Scheil with DICTRA for back-diffusion-corrected microsegregation modeling, where DICTRA predictions approach Scheil at high cooling rates relevant to LPBF (sargent2024integratedcomputationalanda pages 45-49, sargent2024integratedcomputationalanda pages 49-54); (2) modified Scheil models incorporating solute trapping and undercooling corrections (chechik2023toolsforthe pages 19-21); (3) multi-level modeling workflows combining Scheil, DICTRA, and phase-field simulations for microstructure evolution (martucci2023ongoingchallengesof pages 3-4, martucci2023developmentandcharacterisation pages 15-16); and (4) hybrid Scheil–equilibrium analyses to capture phase transformations below the solidus (yang2023designmethodologyfor pages 5-10, yang2023designmethodologyfor pages 10-14). Nonetheless, experimental validation remains essential, as many discrepancies between simulations and experiments persist (martucci2023ongoingchallengesof pages 3-4, martucci2023developmentandcharacterisation pages 15-16).

## Summary and Outlook

The 2022–2026 literature demonstrates that CALPHAD-based computational thermodynamics has become an indispensable pillar of alloy design for additive manufacturing. The combination of Scheil solidification analysis with multiple cracking susceptibility indices (FR, Kou/SCI, CSC, RDG, CTR, HR-DR) provides a robust framework for screening alloy compositions. Integration with machine learning—using thermodynamic features as physics-informed inputs, deep-learning surrogates for 1000× acceleration, and Bayesian optimization for efficient composition-space exploration—has dramatically expanded the throughput of alloy discovery. Commercial tools (particularly Thermo-Calc with TC-Python) and open-source alternatives (pycalphad/ESPEI, OpenCalphad) support increasingly automated high-throughput workflows. However, the fundamental assumption of local thermodynamic equilibrium limits CALPHAD reliability under the extreme non-equilibrium conditions of LPBF (10⁵–10⁷ K/s cooling rates), and continued development of solute-trapping models, kinetic corrections, and multi-scale coupled simulations is needed to bridge the gap between thermodynamic predictions and experimental AM outcomes.

References

1. (yang2023designmethodologyfor pages 10-14): Zhening Yang, Hui Sun, Zi-Kui Liu, and Allison M. Beese. Design methodology for functionally graded materials: framework for considering cracking. Additive Manufacturing, Mar 2023. URL: https://doi.org/10.48550/arxiv.2303.11849, doi:10.48550/arxiv.2303.11849. This article has 44 citations and is from a highest quality peer-reviewed journal.

2. (wu2025advancesincrack pages 9-12): Huabo Wu, Jialiao Zhou, Lan Huang, Zi Wang, Liming Tan, Jin Lv, and Feng Liu. Advances in crack formation mechanisms, evaluation models, and compositional strategies for additively manufactured nickel-based superalloys. Computer Modeling in Engineering &amp; Sciences, 143:2675-2709, Jan 2025. URL: https://doi.org/10.32604/cmes.2025.064854, doi:10.32604/cmes.2025.064854. This article has 6 citations.

3. (liu2024alloydesignfor pages 18-19): Zhuangzhuang Liu, Qihang Zhou, Xiaokang Liang, Xiebin Wang, Guichuan Li, Kim Vanmeensel, and Jianxin Xie. Alloy design for laser powder bed fusion additive manufacturing: a critical review. International Journal of Extreme Manufacturing, 6:022002, Jan 2024. URL: https://doi.org/10.1088/2631-7990/ad1657, doi:10.1088/2631-7990/ad1657. This article has 93 citations.

4. (scaglione2022solidificationcalculationsof pages 14-16): Federico Scaglione, Sergio Arnaboldi, Cristian Viscardi, Marcello Baricco, and Mauro Palumbo. Solidification calculations of precious alloys and al-base alloys for additive manufacturing. Metals, 12:322, Feb 2022. URL: https://doi.org/10.3390/met12020322, doi:10.3390/met12020322. This article has 5 citations.

5. (singh2025understandingsolidificationcrackingb pages 23-27): A Singh. Understanding solidification cracking as a function of part-specific location during laser powder bed fusion of aa2219. Unknown journal, 2025.

6. (wu2025advancesincrack pages 12-14): Huabo Wu, Jialiao Zhou, Lan Huang, Zi Wang, Liming Tan, Jin Lv, and Feng Liu. Advances in crack formation mechanisms, evaluation models, and compositional strategies for additively manufactured nickel-based superalloys. Computer Modeling in Engineering &amp; Sciences, 143:2675-2709, Jan 2025. URL: https://doi.org/10.32604/cmes.2025.064854, doi:10.32604/cmes.2025.064854. This article has 6 citations.

7. (wang2025calphadguidedinterlayerdesign pages 1-2): Liyi Wang, Luis Fernando Ladinos Pizano, Michael A. Klecka, Kelsay Neely, and Wei Xiong. Calphad-guided interlayer design for crack-free additive manufacturing of copper c18150 – inconel 625 bimetallic structures. Science and Technology of Advanced Materials, Nov 2025. URL: https://doi.org/10.1080/14686996.2025.2587393, doi:10.1080/14686996.2025.2587393. This article has 1 citations and is from a peer-reviewed journal.

8. (yang2023designmethodologyfor pages 5-10): Zhening Yang, Hui Sun, Zi-Kui Liu, and Allison M. Beese. Design methodology for functionally graded materials: framework for considering cracking. Additive Manufacturing, Mar 2023. URL: https://doi.org/10.48550/arxiv.2303.11849, doi:10.48550/arxiv.2303.11849. This article has 44 citations and is from a highest quality peer-reviewed journal.

9. (assi2024designandassessment pages 5-7): Mariam Assi, Julien Favre, Marcin Brykala, Franck Tancret, and Anna Fraczkiewicz. Design and assessment of an austenitic stainless alloy for laser powder bed additive manufacturing. Applied Sciences, Sep 2024. URL: https://doi.org/10.3390/app14198649, doi:10.3390/app14198649. This article has 5 citations.

10. (chechik2023toolsforthe pages 19-21): Lova Chechik, Katerina A. Christofidou, Lucy Farquhar, Martin Tse, Gavin Baxter, and Iain Todd. Tools for the assessment of the laser printability of nickel superalloys. Metallurgical and Materials Transactions A, 54:2421-2437, Mar 2023. URL: https://doi.org/10.1007/s11661-023-07029-5, doi:10.1007/s11661-023-07029-5. This article has 15 citations.

11. (chechik2023toolsforthe pages 6-9): Lova Chechik, Katerina A. Christofidou, Lucy Farquhar, Martin Tse, Gavin Baxter, and Iain Todd. Tools for the assessment of the laser printability of nickel superalloys. Metallurgical and Materials Transactions A, 54:2421-2437, Mar 2023. URL: https://doi.org/10.1007/s11661-023-07029-5, doi:10.1007/s11661-023-07029-5. This article has 15 citations.

12. (uba2025enhancingtheprintability pages 7-10): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

13. (josyula2025calphadandmachine pages 39-43): S Josyula. Calphad and machine learning driven design of high-temperature shape memory alloys. Unknown journal, 2025.

14. (assi2022alloysdesignfor pages 48-52): M Assi. Alloys design for additive manufacturing (adam). Unknown journal, 2022.

15. (wu2025advancesincrack pages 22-26): Huabo Wu, Jialiao Zhou, Lan Huang, Zi Wang, Liming Tan, Jin Lv, and Feng Liu. Advances in crack formation mechanisms, evaluation models, and compositional strategies for additively manufactured nickel-based superalloys. Computer Modeling in Engineering &amp; Sciences, 143:2675-2709, Jan 2025. URL: https://doi.org/10.32604/cmes.2025.064854, doi:10.32604/cmes.2025.064854. This article has 6 citations.

16. (wang2023integratedcomputationalmaterials pages 32-38): X Wang. Integrated computational materials design for alloy additive manufacturing: introducing data-driven approach to physical metallurgy. Unknown journal, 2023.

17. (sheikh2025highthroughputalloyand pages 1-3): Sofia Sheikh, Brent Vela, Pejman Honarmandi, Peter Morcos, David Shoukr, Abdelrahman Mostafa Kotb, Raymundo Arroyave, Ibrahim Karaman, and Alaa Elwany. High-throughput alloy and process design for metal additive manufacturing. Npj Computational Materials, Apr 2025. URL: https://doi.org/10.48550/arxiv.2304.04149, doi:10.48550/arxiv.2304.04149. This article has 16 citations and is from a peer-reviewed journal.

18. (sheikh2025highthroughputalloyand pages 3-5): Sofia Sheikh, Brent Vela, Pejman Honarmandi, Peter Morcos, David Shoukr, Abdelrahman Mostafa Kotb, Raymundo Arroyave, Ibrahim Karaman, and Alaa Elwany. High-throughput alloy and process design for metal additive manufacturing. Npj Computational Materials, Apr 2025. URL: https://doi.org/10.48550/arxiv.2304.04149, doi:10.48550/arxiv.2304.04149. This article has 16 citations and is from a peer-reviewed journal.

19. (zhu2025acceleratingcalphadbasedphase pages 1-2): Siya Zhu, Doğuhan Sarıtürk, and Raymundo Arróyave. Accelerating calphad-based phase diagram predictions in complex alloys using universal machine learning potentials: opportunities and challenges. ArXiv, Nov 2025. URL: https://doi.org/10.48550/arxiv.2411.15351, doi:10.48550/arxiv.2411.15351. This article has 40 citations.

20. (olson2024genomicmaterialsdesign pages 29-34): G.B. Olson and Z.K. Liu. Genomic materials design: calculation of phase dynamics. Calphad, 82:102590, Sep 2024. URL: https://doi.org/10.1016/j.calphad.2023.102590, doi:10.1016/j.calphad.2023.102590. This article has 27 citations.

21. (rahman2025reviewmachinelearning pages 25-26): Arafat Rahman, Md Sojib Hossain, and Abdullah-Bin Siddique. Review: machine learning approaches for diverse alloy systems. Journal of Materials Science, 60:12189-12221, Jul 2025. URL: https://doi.org/10.1007/s10853-025-11154-4, doi:10.1007/s10853-025-11154-4. This article has 12 citations and is from a peer-reviewed journal.

22. (sundar2025calphadbasedbayesianoptimization pages 1-2): Aditya Sundar, Xingru Tan, Shanshan Hu, and Michael C. Gao. Calphad-based bayesian optimization to accelerate alloy discovery for high-temperature applications. Journal of Materials Research, 40:112-122, Jan 2025. URL: https://doi.org/10.1557/s43578-024-01489-0, doi:10.1557/s43578-024-01489-0. This article has 7 citations and is from a peer-reviewed journal.

23. (odetola2024exploringhighentropy pages 18-20): Peter Ifeolu Odetola, Bukola Joseph Babalola, Ayodeji Ebenezer Afolabi, Ufoma Silas Anamu, Emmanuel Olorundaisi, Mutombo Christian Umba, Thabang Phahlane, Olusoji Oluremi Ayodele, and Peter Apata Olubambi. Exploring high entropy alloys: a review on thermodynamic design and computational modeling strategies for advanced materials applications. Heliyon, 10:e39660, Nov 2024. URL: https://doi.org/10.1016/j.heliyon.2024.e39660, doi:10.1016/j.heliyon.2024.e39660. This article has 63 citations.

24. (scaglione2022solidificationcalculationsof pages 2-4): Federico Scaglione, Sergio Arnaboldi, Cristian Viscardi, Marcello Baricco, and Mauro Palumbo. Solidification calculations of precious alloys and al-base alloys for additive manufacturing. Metals, 12:322, Feb 2022. URL: https://doi.org/10.3390/met12020322, doi:10.3390/met12020322. This article has 5 citations.

25. (martucci2023ongoingchallengesof pages 3-4): Alessandra Martucci, Alberta Aversa, and Mariangela Lombardi. Ongoing challenges of laser-based powder bed fusion processing of al alloys and potential solutions from the literature—a review. Materials, 16:1084, Jan 2023. URL: https://doi.org/10.3390/ma16031084, doi:10.3390/ma16031084. This article has 62 citations.

26. (assi2022alloysdesignfor pages 211-213): M Assi. Alloys design for additive manufacturing (adam). Unknown journal, 2022.

27. (martucci2023developmentandcharacterisation pages 15-16): A Martucci. Development and characterisation of al-based alloys processed by pbf-lb/m. Unknown journal, 2023.

28. (ghassemali2022highthroughputcalphada pages 2-4): Ehsan Ghassemali and Patrick L. J. Conway. High-throughput calphad: a powerful tool towards accelerated metallurgy. Frontiers in Materials, Apr 2022. URL: https://doi.org/10.3389/fmats.2022.889771, doi:10.3389/fmats.2022.889771. This article has 26 citations.

29. (sheikh2025highthroughputalloyand pages 40-42): Sofia Sheikh, Brent Vela, Pejman Honarmandi, Peter Morcos, David Shoukr, Abdelrahman Mostafa Kotb, Raymundo Arroyave, Ibrahim Karaman, and Alaa Elwany. High-throughput alloy and process design for metal additive manufacturing. Npj Computational Materials, Apr 2025. URL: https://doi.org/10.48550/arxiv.2304.04149, doi:10.48550/arxiv.2304.04149. This article has 16 citations and is from a peer-reviewed journal.

30. (sargent2024integratedcomputationaland pages 40-45): N Sargent. Integrated computational and experimental design of functionally graded materials made with additive manufacturing. Unknown journal, 2024.

31. (sargent2024integratedcomputationalanda pages 45-49): N Sargent. Integrated computational and experimental design of functionally graded materials made with additive manufacturing. Unknown journal, 2024.

32. (sun2022thermodynamicsguidedalloyand pages 1-2): Zhongji Sun, Yan Ma, Dirk Ponge, Stefan Zaefferer, Eric A. Jägle, Baptiste Gault, Anthony D. Rollett, and Dierk Raabe. Thermodynamics-guided alloy and process design for additive manufacturing. Nature Communications, Jul 2022. URL: https://doi.org/10.1038/s41467-022-31969-y, doi:10.1038/s41467-022-31969-y. This article has 143 citations and is from a highest quality peer-reviewed journal.

33. (singh2025understandingsolidificationcrackinga pages 17-23): A Singh. Understanding solidification cracking as a function of part-specific location during laser powder bed fusion of aa2219. Unknown journal, 2025.

34. (singh2025understandingsolidificationcrackingb pages 17-23): A Singh. Understanding solidification cracking as a function of part-specific location during laser powder bed fusion of aa2219. Unknown journal, 2025.

35. (sargent2024integratedcomputationalanda pages 40-45): N Sargent. Integrated computational and experimental design of functionally graded materials made with additive manufacturing. Unknown journal, 2024.

36. (sargent2024integratedcomputationaland pages 45-49): N Sargent. Integrated computational and experimental design of functionally graded materials made with additive manufacturing. Unknown journal, 2024.

37. (liu2024alloydesignfor pages 1-3): Zhuangzhuang Liu, Qihang Zhou, Xiaokang Liang, Xiebin Wang, Guichuan Li, Kim Vanmeensel, and Jianxin Xie. Alloy design for laser powder bed fusion additive manufacturing: a critical review. International Journal of Extreme Manufacturing, 6:022002, Jan 2024. URL: https://doi.org/10.1088/2631-7990/ad1657, doi:10.1088/2631-7990/ad1657. This article has 93 citations.

38. (sargent2024integratedcomputationalanda pages 49-54): N Sargent. Integrated computational and experimental design of functionally graded materials made with additive manufacturing. Unknown journal, 2024.