# LPBF Baseplate Preheating: Necessity & Industrial Relevance

*Edison Scientific LITERATURE_HIGH (`job-futurehouse-paperqa3-high`)*
*Task ID: `21adb4d9-96f8-4e93-9581-333143b4678c` — status: success — 47 reference entries*

This file is the verbatim Edison answer to a high-effort literature query on whether
build-plate preheating is necessary for finding optimal LPBF print conditions and how
industrially relevant/standard it is on commercial machines.

---

Question: In laser powder bed fusion (LPBF / L-PBF / SLM) of metals, how necessary is baseplate (build-plate / substrate) preheating for finding optimal processing conditions, and how industrially relevant is it? Please address, with citations and quantitative detail where possible:

1) Mechanistic role of baseplate preheating: how it affects thermal gradients, residual stress, cracking/distortion susceptibility, cooling rate, microstructure, and the size/shape of the feasible process window. Does preheating expand, shift, or merely translate the feasible region in (laser power, scan speed, hatch, layer thickness) space, and is it a true extra optimization dimension or a fixed enabling condition?

2) Material dependence: for which alloy classes is preheating effectively mandatory (e.g., crack-prone Ni superalloys, Ti-Al intermetallics, tool steels, refractory and high-gamma-prime alloys) versus optional or unnecessary (e.g., AlSi10Mg, 316L, common aluminum alloys)? What preheat temperatures are typically used per class?

3) Industrial relevance and machine availability: is bed/build-plate preheating a standard option on industrially relevant commercial LPBF machines? Which OEMs and platforms (e.g., EOS, SLM Solutions / Nikon SLM, Renishaw, GE/Concept Laser, TRUMPF, DMG MORI, Aconity3D, Velo3D, Farsoon) offer preheating, and what temperature ranges do standard vs. high-temperature configurations reach (e.g., ~80-200 C standard vs. 500/800/1000+ C high-temperature options)? How common is high-temperature preheating in production versus research machines?

4) Practical implications for autonomous/Bayesian optimization of LPBF process parameters: should baseplate preheat temperature be treated as an explicit search dimension, a fixed context variable, or a per-alloy constraint? Summarize the consensus and any disagreements in the literature.

Please use vision/quantitative reasoning where helpful and give a clear, structured, well-cited synthesis.

# Baseplate Preheating in Laser Powder Bed Fusion (LPBF): Necessity, Material Dependence, Industrial Relevance, and Implications for Process Optimization

## 1. Mechanistic Role of Baseplate Preheating

### 1.1 Thermal Gradients and Residual Stress

The primary mechanism by which baseplate preheating affects LPBF outcomes is through the **Temperature Gradient Mechanism (TGM)**. During laser scanning, extreme local heating of upper layers causes thermal expansion against cooler underlying material, generating compressive plastic deformation (upset) that converts to residual tensile stresses upon cooling (kempen2013producingcrackfreehigh pages 1-4, kempen2013loweringthermalgradients pages 1-4). Preheating the build plate raises the baseline temperature of the surrounding material, thereby reducing the magnitude of temperature gradients between the melt pool and its surroundings and lowering the resultant shrinkage stresses (mirkoohi2021mechanicsmodelingof pages 1-3, kaess2023residualstressformation pages 1-2).

Quantitatively, for 316L stainless steel, FEM simulations show that preheating significantly reduces part bending and residual stress development, with pronounced effects from ~300 °C onward and clearly visible reductions above 450 °C (kaess2023residualstressformation pages 11-13, kaess2023residualstressformation pages 10-11). For IN718, preheating in the 50–150 °C range reduced σ_z residual stress by approximately 22% (maly2022effectofpreheating pages 12-13). However, the relationship is non-monotonic: simulations predict that preheating in the 250–500 °C range can *increase* residual stress through grain coarsening and reduced yield strength (maly2022effectofpreheating pages 12-13, mirkoohi2021mechanicsmodelingof pages 11-13). For aluminum alloys, Buchbinder et al. reported that substrate preheat to 250 °C completely eliminated distortion (mirkoohi2021mechanicsmodelingof pages 3-5).

### 1.2 Cooling Rate and Microstructure

Preheating reduces cooling rates during solidification, with measurable effects on microstructure. For LPBF 316L, a 150 °C preheat reduced the simulated cooling rate from 1.65 × 10⁶ °C/s to 1.43 × 10⁶ °C/s, which correlated with larger melt pools, fewer large pores, and a shift toward more equiaxed-cellular microstructure (nezhadfar2019effectofpreheating pages 5-8). At 800 °C build-plate preheating, the cellular substructure in 316L showed approximately 60% growth in cell size and significantly reduced dislocation density (wang2026influenceofbuild pages 1-2). For IN939, preheating to 400 °C increased melt-pool width by ~35 μm and columnar grain width by ~16%, while reducing elongation by 48.8% (maly2022effectofpreheating pages 12-13).

### 1.3 Cracking Susceptibility

Preheating mitigates cracking through multiple mechanisms: reducing thermal stress that drives cold cracking, lowering cooling rates to reduce segregation of embrittling elements at grain boundaries, and stabilizing the melt pool (zhao2026mitigatingsolidificationcracking pages 7-10, fabian2022laserpreheatingfor pages 6-8). However, excessive preheating can promote grain-boundary liquation, precipitation of embrittling phases (e.g., γ′ in Ni superalloys), and grain coarsening that reduces ductility—potentially worsening cracking susceptibility (mirkoohi2021mechanicsmodelingof pages 1-3, maly2022effectofpreheating pages 12-13, mariana2025innovationsinin939 pages 16-19).

### 1.4 Effect on the Process Window

Preheating does not merely translate the feasible process window—it **shifts and reshapes** it in a regime-dependent, non-monotonic manner. Chen et al. demonstrated that for IN718, preheating from 100 to 500 °C increased melt pool depth by ~49% in the conduction regime and ~33% in the keyhole regime, while reducing the width-to-depth ratio from ~2 to ~1.5 (chen2021elucidatingtheeffect pages 1-4, chen2021elucidatingtheeffect pages 6-9). This means that at fixed laser power and scan speed, preheating can push a parameter set from conduction into transition or keyhole behavior, potentially introducing new defect modes (chen2021elucidatingtheeffect pages 24-28). For K418 superalloy, 350 °C preheating widened the viable process window at 30 μm layer thickness by enabling uniform, dense, defect-free microstructures across a broader power range (~200–380 W), but was counterproductive at 60 μm layer thickness due to excessive thermal accumulation (zhao2026mitigatingsolidificationcracking pages 7-10, zhao2026mitigatingsolidificationcracking pages 10-12). For M2 HSS, 200 °C preheating allowed higher scan speeds (550 vs. 500 mm/s) to achieve the same density (98.3%), effectively expanding the feasible region (kempen2013loweringthermalgradients pages 4-8).

These findings collectively demonstrate that **preheating is a true extra optimization dimension**, not merely a fixed enabling condition, as it modifies melt pool morphology, shifts regime boundaries, and interacts non-trivially with other parameters (chen2021elucidatingtheeffect pages 24-28, chen2021elucidatingtheeffect pages 6-9).

## 2. Material Dependence

The necessity for preheating is strongly material-dependent. The following table summarizes the key findings across alloy classes:

| Alloy Class | Representative Alloys | Preheating Necessity | Typical Preheat Temperature Range | Key Effect of Preheating | Notes |
|---|---|---|---|---|---|
| γ′-strengthened Ni superalloys | CM247LC, IN738LC, K418, IN939 | Often mandatory or near-mandatory for crack suppression; sometimes still insufficient without alloy/process redesign | ~350–400 °C in LPBF for some alloys; much higher local/substrate temperatures ~800–1050 °C reported in related high-temperature AM studies | Reduces thermal gradients/cooling rate and can suppress hot cracking, but can also enlarge melt pools, promote segregation/precipitation, or even raise residual stress at too-high temperatures | K418: 350 °C with 30 µm layers and VED 60–80 J/mm³ gave >99% density with minimal cracking; 200 °C was insufficient. IN939 studied to 400 °C; high preheat increased distortion/strength and reduced ductility. For CM247LC/IN738LC, literature emphasizes combining preheat with alloy modification and scan/process redesign rather than relying on preheat alone (zhao2026mitigatingsolidificationcracking pages 20-21, zhao2026mitigatingsolidificationcracking pages 1-2, zhao2026mitigatingsolidificationcracking pages 7-10, zhao2026mitigatingsolidificationcracking pages 10-12, griffiths2020combiningalloyand pages 1-2, adegoke2020reviewoflaser pages 10-12, maly2022effectofpreheating pages 12-13, mariana2025innovationsinin939 pages 16-19) |
| Moderate Ni superalloys | IN718 | Beneficial, usually not mandatory | ~100–500 °C studied; low-to-moderate preheat commonly used, very high values mainly for research | Lowers residual stress and changes melt-pool geometry, but also shifts toward deeper penetration/keyhole behavior at fixed P–v; excessive preheat can become counterproductive | Melt-pool depth increased monotonically with preheat, by about +49% in conduction regime at 500 °C; literature on IN718 suggests modest preheating can reduce residual stress, while very high preheat can worsen stress via coarsening/lowered yield strength (chen2021elucidatingtheeffect pages 1-4, chen2021elucidatingtheeffect pages 6-9, chen2021elucidatingtheeffect pages 24-28, mirkoohi2021mechanicsmodelingof pages 3-5) |
| TiAl intermetallics | Ti-48Al-2Cr-2Nb | Effectively mandatory for crack-free LPBF | ~800 °C in demonstrated HT-LPBF systems; lower values such as 400–450 °C generally insufficient | Suppresses cold cracking by moving material above the ductile–brittle transition and reducing thermal stress; enables stable powder bed and successful layer accumulation | Ambient builds failed after ~10 layers with crack density 4.23 mm/mm², whereas 800 °C inductive preheating enabled stable builds and crack-free optical inspection with >99% apparent density in one LPBF study (caprio2018developmentofnovel pages 8-10, caprio2018developmentofnovel pages 5-8, caprio2020defectfreelaserpowder pages 7-11) |
| Tool steels | M2 HSS, H13 | Usually mandatory/strongly beneficial for crack-free processing | Commonly ~200 °C; H13 literature also points to ~200–400 °C | Reduces thermal gradients and martensite-driven cracking, stabilizes melt pool, allows denser/crack-free builds at broader speed windows | M2 HSS: 200 °C produced crack-free parts with 99.8–99.88% density. H13: 200 °C generally aided density and eliminated crack formation; some literature suggests 400 °C may further improve behavior/microstructure (kempen2013loweringthermalgradients pages 1-4, kempen2013loweringthermalgradients pages 8-9, kempen2013producingcrackfreehigh pages 1-4, narvan2019processstructurepropertyrelationshipsof pages 1-3, he2020astudyof pages 1-5, bergmueller2022crackfreeinsitu pages 1-2) |
| High-strength Al alloys, 6xxx | EN AW 6182 / AlSi1MgZr, Al6061 | Beneficial to mandatory for crack-free LPBF, depending on chemistry | Often ~500 °C for crack-free builds | Strongly reduces hot cracking and promotes columnar-to-equiaxed transition | EN AW 6182 required 500 °C to obtain crack-free parts, fully equiaxed microstructure, and >99% density; process window shifts to lower optimal energy as preheat increases (riener2022processabilityofhighstrength pages 1-2, riener2022processabilityofhighstrength pages 10-12, stopyra2020laserpowderbed pages 6-9) |
| High-strength Al alloys, 7xxx | AA7075 / EN AW 7075 | Beneficial but usually insufficient alone | 100–400 °C studied; 200 °C often insufficient, 400 °C can alter but not eliminate cracking | Modestly reduces thermal gradients/retained stress but often fails to suppress hot cracking; high preheat can change crack morphology and promote segregation | For EN AW 7075, 100–200 °C gave no significant crack-density reduction; 400 °C caused columnar crack networks, stress relaxation, and lower hardness. Consensus: preheating alone is not enough; alloy/feedstock modification is often needed (velikajne2026influenceofbase pages 1-2, velikajne2026influenceofbase pages 8-11) |
| Castable Al-Si alloys | AlSi10Mg | Optional or often unnecessary beyond standard machine warm-up | None to low standard machine preheat, often ~80–200 °C depending on machine | Usually used more for distortion control/consistency than for crack suppression | Literature characterizes AlSi10Mg as comparatively weldable and much less crack-prone than 6xxx/7xxx alloys; it is widely processable without aggressive preheating (velikajne2026influenceofbase pages 1-2, rehman2021laserpowderbed pages 34-35) |
| Austenitic stainless steels | 316L | Optional | None to modest preheat such as 150 °C in studies; high-temperature preheat up to 800 °C mainly for microstructure research | Lowers cooling rate and residual stress, reduces porosity, enlarges melt pools slightly, and can coarsen/anneal cellular structure at high temperature | 316L is readily processable without preheat; 150 °C reduced simulated cooling rate from 1.65×10^6 to 1.43×10^6 °C/s and improved elongation. At 800 °C, cell size increased by ~60% with reduced dislocation density (nezhadfar2019effectofpreheating pages 1-3, nezhadfar2019effectofpreheating pages 5-8, wang2026influenceofbuild pages 1-2) |
| Ti alloys | Ti-6Al-4V | Usually optional for printability, beneficial for stress/microstructure control | ~150–250 °C for distortion reduction; ~570 °C explored for in situ microstructure modification | Reduces distortion/residual stress and can drive in situ tempering/martensite decomposition | Literature cited in LPBF preheat studies reports ~10% curling reduction up to 180 °C and marked α′→α+β decomposition/mechanical-property changes near 570 °C; generally an optimization lever rather than an enabling requirement (chen2021elucidatingtheeffect pages 4-6) |


*Table: This table summarizes how necessary baseplate preheating is across major LPBF alloy classes, the temperature ranges reported, and the main process or microstructural effects. It is useful for deciding whether preheating should be treated as mandatory, beneficial, or optional in process development.*

### Key highlights:

- **Mandatory preheating**: γ-TiAl intermetallics require ~800 °C preheating due to a ductile-to-brittle transition around 750 °C; ambient builds fail within ~10 layers with crack densities of 4.23 mm/mm² (caprio2018developmentofnovel pages 8-10, caprio2018developmentofnovel pages 5-8). Tool steels (M2 HSS) are effectively unprocessable without ~200 °C preheating, which enables crack-free parts at 99.8% density (kempen2013loweringthermalgradients pages 1-4, kempen2013producingcrackfreehigh pages 1-4). High-strength 6xxx Al alloys require ~500 °C for crack-free, equiaxed microstructures (riener2022processabilityofhighstrength pages 1-2, riener2022processabilityofhighstrength pages 10-12).

- **Strongly beneficial but complex**: High-γ′ Ni superalloys (K418, IN939, CM247LC, IN738LC) benefit from preheating at 350–400 °C in LPBF, but alloy modification and scan strategy optimization are often additionally required (zhao2026mitigatingsolidificationcracking pages 20-21, zhao2026mitigatingsolidificationcracking pages 1-2, griffiths2020combiningalloyand pages 1-2). For IN738LC via DMD, crack-free processing required substrate temperatures of ~975–1050 °C (fabian2022laserpreheatingfor pages 6-8).

- **Optional**: 316L and AlSi10Mg are processable without preheating; 316L benefits from modest preheat (~150 °C) for improved microstructural homogeneity and mechanical properties (nezhadfar2019effectofpreheating pages 1-3, nezhadfar2019effectofpreheating pages 5-8), while AlSi10Mg exhibits comparatively good weldability and reduced cracking tendency (velikajne2026influenceofbase pages 1-2).

- **Insufficient alone**: For 7xxx Al alloys, preheating up to 400 °C is insufficient to suppress hot cracking and can even promote alternative crack mechanisms; alloy modification (grain refiners, inoculants) is typically required (velikajne2026influenceofbase pages 1-2, velikajne2026influenceofbase pages 8-11).

## 3. Industrial Relevance and Machine Availability

### 3.1 Preheating Technology Tiers

The literature identifies three tiers of preheating technology for LPBF machines (caprio2020defectfreelaserpowder pages 5-7, caprio2018developmentofnovel pages 1-3):

1. **Standard resistive baseplate heating (~80–200 °C)**: The most common configuration on industrial LPBF machines. Most major OEMs offer this as standard. Examples include the EOS M290 with heating modules and thermocouple monitoring (chen2021elucidatingtheeffect pages 4-6, narvan2019processstructurepropertyrelationshipsof pages 3-5), and the Concept Laser M3 Linear with a resistive under-platform heater controlled to ±2 °C (kempen2013loweringthermalgradients pages 1-4).

2. **Advanced resistive/IR heating (~200–500 °C)**: More recent commercial systems reach ~500 °C. These are available from select OEMs and enable processing of tool steels and some crack-prone alloys. SLM Solutions (now Nikon SLM) and some EOS configurations offer elevated preheating in this range.

3. **High-temperature induction heating (>800–1200 °C)**: Primarily available on research/specialty machines. The Project Grisù prototype demonstrated inductive preheating above 800 °C with ±10 °C control and 5 °C/min controlled cooling, enabling crack-free TiAl processing (caprio2018developmentofnovel pages 8-10, caprio2018developmentofnovel pages 5-8, caprio2020defectfreelaserpowder pages 7-11, caprio2018developmentofnovel pages 3-5). Aconity3D is known in the field for offering high-temperature preheating (induction-based) up to ~1000–1200 °C. EBM systems (e.g., Arcam/GE) inherently achieve powder-bed temperatures on the order of 1000 °C through electron-beam preheating scans (maly2022effectofpreheating pages 2-4, caprio2020defectfreelaserpowder pages 5-7).

### 3.2 Practical Limitations

Baseplate preheating effectiveness diminishes with build height, as heat transfer from the plate to upper layers is attenuated (caprio2020defectfreelaserpowder pages 5-7). Intrinsic (process-induced) preheating from heat accumulation during scanning can reach up to ~600 °C in 316L builds and is often the dominant source of elevated temperature in upper layers, especially with short inter-layer times (wang2026influenceofbuild pages 1-2). Additionally, high-temperature powder-bed preheating risks degrading unfused powder and limiting recycling potential (maly2022effectofpreheating pages 2-4). These factors mean that high-temperature preheating in production is currently limited to niche applications (TiAl, specialized superalloys) and is not yet standard practice for large-volume industrial LPBF.

## 4. Practical Implications for Autonomous/Bayesian Optimization of LPBF Process Parameters

### 4.1 Preheating as an Optimization Dimension

The literature provides strong evidence that baseplate preheat temperature should **not be ignored** in process optimization. Chen et al. demonstrated that preheating modifies melt pool morphology in a regime-dependent, non-monotonic manner—shifting the boundaries between conduction, transition, and keyhole modes—making it a genuine additional optimization dimension rather than merely a fixed enabling condition (chen2021elucidatingtheeffect pages 24-28, chen2021elucidatingtheeffect pages 6-9). Kavas et al. showed in a Bayesian optimization study of closed-loop LPBF control that preheat directly affects melt-pool emissions and controller behavior, and if not properly accounted for, can drive laser power outside the viable process window, causing lack-of-fusion defects (kavas2025insitucontrollerautotuning pages 26-29).

### 4.2 Recommended Treatment

Based on the literature, the recommended treatment of preheating in autonomous optimization depends on the alloy class:

- **For crack-prone alloys** (tool steels, high-γ′ Ni superalloys, TiAl, high-strength Al): Preheating temperature should be treated as an **explicit search dimension** or, at minimum, a **per-alloy constraint** with a specified minimum threshold. The interaction between preheat and layer thickness is particularly important—for K418, 350 °C preheating was beneficial at 30 μm but counterproductive at 60 μm layer thickness (zhao2026mitigatingsolidificationcracking pages 1-2, zhao2026mitigatingsolidificationcracking pages 7-10, zhao2026mitigatingsolidificationcracking pages 10-12), demonstrating strong parameter coupling that a naive single-variable optimization would miss.

- **For easily processable alloys** (316L, AlSi10Mg, Ti-6Al-4V): Preheating can be treated as a **fixed context variable** set to the machine default (typically 80–200 °C or ambient), since these materials are processable across a range of preheat values and the primary optimization dimensions remain laser power, scan speed, hatch spacing, and layer thickness. However, if microstructural control is an objective (e.g., cell size, texture, dislocation density), preheating becomes a relevant tunable parameter (wang2026influenceofbuild pages 1-2, nezhadfar2019effectofpreheating pages 5-8).

- **General principle**: Normalized energy-input models explicitly include ambient/preheat temperature (T₀) as a material/process parameter that affects the energy required for melting and the resulting thermal gradients (bajaj2020precipitationduringintrinsic pages 58-60). Any physics-informed Bayesian optimization framework should therefore include T₀ in its thermal model, even if the experimental search space is constrained to a fixed preheat value for practical reasons.

### 4.3 Consensus and Disagreements

There is broad consensus in the literature that:
- Preheating reduces thermal gradients and generally reduces residual stress at moderate temperatures (kempen2013producingcrackfreehigh pages 1-4, mirkoohi2021mechanicsmodelingof pages 1-3, kaess2023residualstressformation pages 1-2).
- The effect is non-monotonic: excessive preheating can increase residual stress through grain coarsening and yield-strength reduction (maly2022effectofpreheating pages 12-13, mirkoohi2021mechanicsmodelingof pages 11-13, maly2022effectofpreheating pages 1-2).
- Preheating alone is often insufficient for the most crack-prone alloys; combined process-alloy strategies are needed (griffiths2020combiningalloyand pages 1-2, adegoke2020reviewoflaser pages 20-21, velikajne2026influenceofbase pages 1-2).

A point of disagreement concerns whether preheating primarily *expands* the feasible window or *shifts* it. The evidence suggests both occur simultaneously: preheating expands the window by suppressing cracking at parameter combinations that would otherwise fail, but also shifts regime boundaries (e.g., conduction to keyhole), potentially introducing new defect modes at parameter sets that were previously safe (chen2021elucidatingtheeffect pages 24-28, chen2021elucidatingtheeffect pages 1-4). This dual effect reinforces the argument for treating preheat as an active optimization variable rather than a simple on/off enabling condition.

## Summary

Baseplate preheating in LPBF is a physically significant process variable that reduces thermal gradients, lowers cooling rates, modifies microstructure, and can suppress cracking—but its effects are strongly material-dependent and non-monotonic. For crack-prone alloy classes (TiAl, tool steels, high-γ′ superalloys, high-strength Al), preheating is effectively mandatory and requires temperatures ranging from 200 °C to >800 °C depending on the alloy. For readily processable alloys (316L, AlSi10Mg), it is optional but beneficial for property optimization. Standard industrial LPBF machines offer ~80–200 °C resistive preheating, with advanced systems reaching ~500 °C and specialized research machines exceeding 800–1200 °C via induction heating. In autonomous process optimization, preheating should be treated as either an explicit search dimension (for crack-prone alloys) or a fixed context variable (for easily processable alloys), but never ignored, as it fundamentally alters melt pool physics and the shape of the feasible process window.

References

1. (kempen2013producingcrackfreehigh pages 1-4): K. Kempen, L. Thijs, B. Vrancken, S. Buls, J. Van Humbeeck, and J.-P. Kruth. Producing crack-free, high density m2 hss parts by selective laser melting: pre-heating the baseplate. Aug 2013. URL: https://doi.org/10.26153/tsw/15419, doi:10.26153/tsw/15419. This article has 146 citations.

2. (kempen2013loweringthermalgradients pages 1-4): K Kempen, B Vrancken, L Thijs, and S Buls. Lowering thermal gradients in selective laser melting by pre-heating the baseplate. Unknown journal, 2013.

3. (mirkoohi2021mechanicsmodelingof pages 1-3): Elham Mirkoohi, Hong-Chuong Tran, Yu-Lung Lo, You-Cheng Chang, Hung-Yu Lin, and Steven Liang. Mechanics modeling of residual stress considering effect of preheating in laser powder bed fusion. Journal of Manufacturing and Materials Processing, 5:46, Mar 2021. URL: https://doi.org/10.20944/preprints202103.0359.v1, doi:10.20944/preprints202103.0359.v1. This article has 38 citations.

4. (kaess2023residualstressformation pages 1-2): Moritz Kaess, Martin Werz, and Stefan Weihe. Residual stress formation mechanisms in laser powder bed fusion—a numerical evaluation. Materials, 16:2321, Mar 2023. URL: https://doi.org/10.3390/ma16062321, doi:10.3390/ma16062321. This article has 39 citations.

5. (kaess2023residualstressformation pages 11-13): Moritz Kaess, Martin Werz, and Stefan Weihe. Residual stress formation mechanisms in laser powder bed fusion—a numerical evaluation. Materials, 16:2321, Mar 2023. URL: https://doi.org/10.3390/ma16062321, doi:10.3390/ma16062321. This article has 39 citations.

6. (kaess2023residualstressformation pages 10-11): Moritz Kaess, Martin Werz, and Stefan Weihe. Residual stress formation mechanisms in laser powder bed fusion—a numerical evaluation. Materials, 16:2321, Mar 2023. URL: https://doi.org/10.3390/ma16062321, doi:10.3390/ma16062321. This article has 39 citations.

7. (maly2022effectofpreheating pages 12-13): Martin Malý, Klára Nopová, Lenka Klakurková, Ondřej Adam, Libor Pantělejev, and Daniel Koutný. Effect of preheating on the residual stress and material properties of inconel 939 processed by laser powder bed fusion. Materials, 15:6360, Sep 2022. URL: https://doi.org/10.3390/ma15186360, doi:10.3390/ma15186360. This article has 28 citations.

8. (mirkoohi2021mechanicsmodelingof pages 11-13): Elham Mirkoohi, Hong-Chuong Tran, Yu-Lung Lo, You-Cheng Chang, Hung-Yu Lin, and Steven Liang. Mechanics modeling of residual stress considering effect of preheating in laser powder bed fusion. Journal of Manufacturing and Materials Processing, 5:46, Mar 2021. URL: https://doi.org/10.20944/preprints202103.0359.v1, doi:10.20944/preprints202103.0359.v1. This article has 38 citations.

9. (mirkoohi2021mechanicsmodelingof pages 3-5): Elham Mirkoohi, Hong-Chuong Tran, Yu-Lung Lo, You-Cheng Chang, Hung-Yu Lin, and Steven Liang. Mechanics modeling of residual stress considering effect of preheating in laser powder bed fusion. Journal of Manufacturing and Materials Processing, 5:46, Mar 2021. URL: https://doi.org/10.20944/preprints202103.0359.v1, doi:10.20944/preprints202103.0359.v1. This article has 38 citations.

10. (nezhadfar2019effectofpreheating pages 5-8): P.D. Nezhadfar, Arash Soltani-Tehrani, and Nima Shamsaei. Effect of preheating build platform on microstructure and mechanical properties of additively manufactured 316l stainless steel. Jan 2019. URL: https://doi.org/10.26153/tsw/17281, doi:10.26153/tsw/17281. This article has 16 citations.

11. (wang2026influenceofbuild pages 1-2): Xiaobo Wang, Frank Adjei-Kyeremeh, Wayne Edgar Alphonso, Venkata Karthik Nadimpalli, Mohamad Bayat, Iris Raffeis, Dorte Juul Jensen, and Tianbo Yu. Influence of build plate preheating on the cell structure in stainless steel 316l produced by laser powder bed fusion. Metallurgical and Materials Transactions A, 57:2918-2931, Apr 2026. URL: https://doi.org/10.1007/s11661-026-08174-3, doi:10.1007/s11661-026-08174-3. This article has 0 citations.

12. (zhao2026mitigatingsolidificationcracking pages 7-10): Deqin Zhao, Jie Pei, Chenxue Ma, and Rengeng Li. Mitigating solidification cracking in lpbf-processed k418 superalloy via substrate preheating and layer thickness optimization. Materials, 19:501, Jan 2026. URL: https://doi.org/10.3390/ma19030501, doi:10.3390/ma19030501. This article has 1 citations.

13. (fabian2022laserpreheatingfor pages 6-8): Fabian Soffel, Konrad J.M. Papis, Markus Bambach, and Konrad Wegener. Laser preheating for hot crack reduction in direct metal deposition of inconel 738lc. Metals, Apr 2022. URL: https://doi.org/10.3390/met12040614, doi:10.3390/met12040614. This article has 23 citations.

14. (mariana2025innovationsinin939 pages 16-19): Sgambaro De Lorenzi Mariana, Verner Soh, Delvin Wuu, Si Rong Ng, Desmond Lau, Siyuan Wei, Chee Koon Ng, Wenqi Guo, Pei Wang, Zhongji Sun, and Zhili Dong. Innovations in in939: from cast alloy to additive manufacturing. High-Temperature Materials, 2:10003-10003, Jan 2025. URL: https://doi.org/10.70322/htm.2025.10003, doi:10.70322/htm.2025.10003. This article has 5 citations.

15. (chen2021elucidatingtheeffect pages 1-4): Qian Chen, Yunhao Zhao, Seth Strayer, Yufan Zhao, Kenta Aoyagi, Yuichiro Koizumi, Akihiko Chiba, Wei Xiong, and Albert C. To. Elucidating the effect of preheating temperature on melt pool morphology variation in inconel 718 laser powder bed fusion via simulation and experiment. Additive Manufacturing, 37:101642, Jan 2021. URL: https://doi.org/10.1016/j.addma.2020.101642, doi:10.1016/j.addma.2020.101642. This article has 164 citations and is from a highest quality peer-reviewed journal.

16. (chen2021elucidatingtheeffect pages 6-9): Qian Chen, Yunhao Zhao, Seth Strayer, Yufan Zhao, Kenta Aoyagi, Yuichiro Koizumi, Akihiko Chiba, Wei Xiong, and Albert C. To. Elucidating the effect of preheating temperature on melt pool morphology variation in inconel 718 laser powder bed fusion via simulation and experiment. Additive Manufacturing, 37:101642, Jan 2021. URL: https://doi.org/10.1016/j.addma.2020.101642, doi:10.1016/j.addma.2020.101642. This article has 164 citations and is from a highest quality peer-reviewed journal.

17. (chen2021elucidatingtheeffect pages 24-28): Qian Chen, Yunhao Zhao, Seth Strayer, Yufan Zhao, Kenta Aoyagi, Yuichiro Koizumi, Akihiko Chiba, Wei Xiong, and Albert C. To. Elucidating the effect of preheating temperature on melt pool morphology variation in inconel 718 laser powder bed fusion via simulation and experiment. Additive Manufacturing, 37:101642, Jan 2021. URL: https://doi.org/10.1016/j.addma.2020.101642, doi:10.1016/j.addma.2020.101642. This article has 164 citations and is from a highest quality peer-reviewed journal.

18. (zhao2026mitigatingsolidificationcracking pages 10-12): Deqin Zhao, Jie Pei, Chenxue Ma, and Rengeng Li. Mitigating solidification cracking in lpbf-processed k418 superalloy via substrate preheating and layer thickness optimization. Materials, 19:501, Jan 2026. URL: https://doi.org/10.3390/ma19030501, doi:10.3390/ma19030501. This article has 1 citations.

19. (kempen2013loweringthermalgradients pages 4-8): K Kempen, B Vrancken, L Thijs, and S Buls. Lowering thermal gradients in selective laser melting by pre-heating the baseplate. Unknown journal, 2013.

20. (zhao2026mitigatingsolidificationcracking pages 20-21): Deqin Zhao, Jie Pei, Chenxue Ma, and Rengeng Li. Mitigating solidification cracking in lpbf-processed k418 superalloy via substrate preheating and layer thickness optimization. Materials, 19:501, Jan 2026. URL: https://doi.org/10.3390/ma19030501, doi:10.3390/ma19030501. This article has 1 citations.

21. (zhao2026mitigatingsolidificationcracking pages 1-2): Deqin Zhao, Jie Pei, Chenxue Ma, and Rengeng Li. Mitigating solidification cracking in lpbf-processed k418 superalloy via substrate preheating and layer thickness optimization. Materials, 19:501, Jan 2026. URL: https://doi.org/10.3390/ma19030501, doi:10.3390/ma19030501. This article has 1 citations.

22. (griffiths2020combiningalloyand pages 1-2): S. Griffiths, H. Ghasemi Tabasi, T. Ivas, X. Maeder, A. De Luca, K. Zweiacker, R. Wróbel, J. Jhabvala, R.E. Logé, and C. Leinenbach. Combining alloy and process modification for micro-crack mitigation in an additively manufactured ni-base superalloy. Additive manufacturing, 36:101443, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101443, doi:10.1016/j.addma.2020.101443. This article has 246 citations and is from a highest quality peer-reviewed journal.

23. (adegoke2020reviewoflaser pages 10-12): Olutayo Adegoke, Joel Andersson, Håkan Brodin, and Robert Pederson. Review of laser powder bed fusion of gamma-prime-strengthened nickel-based superalloys. Metals, 10:996, Jul 2020. URL: https://doi.org/10.3390/met10080996, doi:10.3390/met10080996. This article has 87 citations.

24. (caprio2018developmentofnovel pages 8-10): L. Caprio, G. Chiari, A.G. Demir, and B. Previtali. Development of novel high temperature laser powder bed fusion system for the processing of crack-susceptible alloys. Jan 2018. URL: https://doi.org/10.26153/tsw/17221, doi:10.26153/tsw/17221. This article has 14 citations.

25. (caprio2018developmentofnovel pages 5-8): L. Caprio, G. Chiari, A.G. Demir, and B. Previtali. Development of novel high temperature laser powder bed fusion system for the processing of crack-susceptible alloys. Jan 2018. URL: https://doi.org/10.26153/tsw/17221, doi:10.26153/tsw/17221. This article has 14 citations.

26. (caprio2020defectfreelaserpowder pages 7-11): Leonardo Caprio, Ali Gökhan Demir, Gianmarco Chiari, and Barbara Previtali. Defect-free laser powder bed fusion of ti–48al–2cr–2nb with a high temperature inductive preheating system. Journal of Physics: Photonics, 2:024001, Feb 2020. URL: https://doi.org/10.1088/2515-7647/ab7080, doi:10.1088/2515-7647/ab7080. This article has 75 citations.

27. (kempen2013loweringthermalgradients pages 8-9): K Kempen, B Vrancken, L Thijs, and S Buls. Lowering thermal gradients in selective laser melting by pre-heating the baseplate. Unknown journal, 2013.

28. (narvan2019processstructurepropertyrelationshipsof pages 1-3): Morteza Narvan, Kassim S. Al-Rubaie, and Mohamed Elbestawi. Process-structure-property relationships of aisi h13 tool steel processed with selective laser melting. Materials, 12:2284, Jul 2019. URL: https://doi.org/10.3390/ma12142284, doi:10.3390/ma12142284. This article has 162 citations.

29. (he2020astudyof pages 1-5): Yining He, Ming-Qiang Zhong, J. Beuth, and B. Webler. A study of microstructure and cracking behavior of h13 tool steel produced by laser powder bed fusion using single-tracks, multi-track pads, and 3d cubes. Journal of Materials Processing Technology, 286:116802, Dec 2020. URL: https://doi.org/10.1016/j.jmatprotec.2020.116802, doi:10.1016/j.jmatprotec.2020.116802. This article has 98 citations and is from a domain leading peer-reviewed journal.

30. (bergmueller2022crackfreeinsitu pages 1-2): Simon Bergmueller, Lukas Kaserer, Lorenz Fuchs, Jakob Braun, Nikolaus Weinberger, Ilse Letofsky-Papst, and Gerhard Leichtfried. Crack-free in situ heat-treated high-alloy tool steel processed via laser powder bed fusion: microstructure and mechanical properties. Heliyon, 8:e10171, Aug 2022. URL: https://doi.org/10.1016/j.heliyon.2022.e10171, doi:10.1016/j.heliyon.2022.e10171. This article has 10 citations.

31. (riener2022processabilityofhighstrength pages 1-2): Kirstin Riener, Tino Pfalz, Florian Funcke, and Gerhard Leichtfried. Processability of high-strength aluminum 6182 series alloy via laser powder bed fusion (lpbf). The International Journal of Advanced Manufacturing Technology, 119:4963-4977, Jan 2022. URL: https://doi.org/10.1007/s00170-022-08673-8, doi:10.1007/s00170-022-08673-8. This article has 48 citations.

32. (riener2022processabilityofhighstrength pages 10-12): Kirstin Riener, Tino Pfalz, Florian Funcke, and Gerhard Leichtfried. Processability of high-strength aluminum 6182 series alloy via laser powder bed fusion (lpbf). The International Journal of Advanced Manufacturing Technology, 119:4963-4977, Jan 2022. URL: https://doi.org/10.1007/s00170-022-08673-8, doi:10.1007/s00170-022-08673-8. This article has 48 citations.

33. (stopyra2020laserpowderbed pages 6-9): Wojciech Stopyra, Konrad Gruber, Irina Smolina, Tomasz Kurzynowski, and Bogumiła Kuźnicka. Laser powder bed fusion of aa7075 alloy: influence of process parameters on porosity and hot cracking. Additive manufacturing, 35:101270, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101270, doi:10.1016/j.addma.2020.101270. This article has 319 citations and is from a highest quality peer-reviewed journal.

34. (velikajne2026influenceofbase pages 1-2): Nejc Velikajne, Jožef Medved, Črtomir Donik, and Irena Paulin. Influence of base plate preheating on laser powder bed fusion–processed en aw-7075 aluminium alloy. Materials, 19:970, Mar 2026. URL: https://doi.org/10.3390/ma19050970, doi:10.3390/ma19050970. This article has 2 citations.

35. (velikajne2026influenceofbase pages 8-11): Nejc Velikajne, Jožef Medved, Črtomir Donik, and Irena Paulin. Influence of base plate preheating on laser powder bed fusion–processed en aw-7075 aluminium alloy. Materials, 19:970, Mar 2026. URL: https://doi.org/10.3390/ma19050970, doi:10.3390/ma19050970. This article has 2 citations.

36. (rehman2021laserpowderbed pages 34-35): Asif Ur Rehman, Fatih Pitir, and Metin Uymaz Salamci. Laser powder bed fusion (lpbf) of in718 and the impact of pre-heating at 500 and 1000 °c: operando study. Materials, 14:6683, Nov 2021. URL: https://doi.org/10.3390/ma14216683, doi:10.3390/ma14216683. This article has 28 citations.

37. (nezhadfar2019effectofpreheating pages 1-3): P.D. Nezhadfar, Arash Soltani-Tehrani, and Nima Shamsaei. Effect of preheating build platform on microstructure and mechanical properties of additively manufactured 316l stainless steel. Jan 2019. URL: https://doi.org/10.26153/tsw/17281, doi:10.26153/tsw/17281. This article has 16 citations.

38. (chen2021elucidatingtheeffect pages 4-6): Qian Chen, Yunhao Zhao, Seth Strayer, Yufan Zhao, Kenta Aoyagi, Yuichiro Koizumi, Akihiko Chiba, Wei Xiong, and Albert C. To. Elucidating the effect of preheating temperature on melt pool morphology variation in inconel 718 laser powder bed fusion via simulation and experiment. Additive Manufacturing, 37:101642, Jan 2021. URL: https://doi.org/10.1016/j.addma.2020.101642, doi:10.1016/j.addma.2020.101642. This article has 164 citations and is from a highest quality peer-reviewed journal.

39. (caprio2020defectfreelaserpowder pages 5-7): Leonardo Caprio, Ali Gökhan Demir, Gianmarco Chiari, and Barbara Previtali. Defect-free laser powder bed fusion of ti–48al–2cr–2nb with a high temperature inductive preheating system. Journal of Physics: Photonics, 2:024001, Feb 2020. URL: https://doi.org/10.1088/2515-7647/ab7080, doi:10.1088/2515-7647/ab7080. This article has 75 citations.

40. (caprio2018developmentofnovel pages 1-3): L. Caprio, G. Chiari, A.G. Demir, and B. Previtali. Development of novel high temperature laser powder bed fusion system for the processing of crack-susceptible alloys. Jan 2018. URL: https://doi.org/10.26153/tsw/17221, doi:10.26153/tsw/17221. This article has 14 citations.

41. (narvan2019processstructurepropertyrelationshipsof pages 3-5): Morteza Narvan, Kassim S. Al-Rubaie, and Mohamed Elbestawi. Process-structure-property relationships of aisi h13 tool steel processed with selective laser melting. Materials, 12:2284, Jul 2019. URL: https://doi.org/10.3390/ma12142284, doi:10.3390/ma12142284. This article has 162 citations.

42. (caprio2018developmentofnovel pages 3-5): L. Caprio, G. Chiari, A.G. Demir, and B. Previtali. Development of novel high temperature laser powder bed fusion system for the processing of crack-susceptible alloys. Jan 2018. URL: https://doi.org/10.26153/tsw/17221, doi:10.26153/tsw/17221. This article has 14 citations.

43. (maly2022effectofpreheating pages 2-4): Martin Malý, Klára Nopová, Lenka Klakurková, Ondřej Adam, Libor Pantělejev, and Daniel Koutný. Effect of preheating on the residual stress and material properties of inconel 939 processed by laser powder bed fusion. Materials, 15:6360, Sep 2022. URL: https://doi.org/10.3390/ma15186360, doi:10.3390/ma15186360. This article has 28 citations.

44. (kavas2025insitucontrollerautotuning pages 26-29): Baris Kavas, Efe C. Balta, Michael Tucker, Raamadaas Krishnadas, Alisa Rupenyan, John Lygeros, and Markus Bambach. In-situ controller autotuning by bayesian optimization for closed-loop feedback control of laser powder bed fusion process. ArXiv, Jun 2025. URL: https://doi.org/10.48550/arxiv.2406.19096, doi:10.48550/arxiv.2406.19096. This article has 21 citations.

45. (bajaj2020precipitationduringintrinsic pages 58-60): P. Bajaj, B. Svendsen, and D. Raabe. Precipitation during intrinsic heat treatment in laser additive manufacturing. ArXiv, pages 2020, Oct 2020. URL: https://doi.org/10.18154/rwth-2020-10461, doi:10.18154/rwth-2020-10461. This article has 2 citations.

46. (maly2022effectofpreheating pages 1-2): Martin Malý, Klára Nopová, Lenka Klakurková, Ondřej Adam, Libor Pantělejev, and Daniel Koutný. Effect of preheating on the residual stress and material properties of inconel 939 processed by laser powder bed fusion. Materials, 15:6360, Sep 2022. URL: https://doi.org/10.3390/ma15186360, doi:10.3390/ma15186360. This article has 28 citations.

47. (adegoke2020reviewoflaser pages 20-21): Olutayo Adegoke, Joel Andersson, Håkan Brodin, and Robert Pederson. Review of laser powder bed fusion of gamma-prime-strengthened nickel-based superalloys. Metals, 10:996, Jul 2020. URL: https://doi.org/10.3390/met10080996, doi:10.3390/met10080996. This article has 87 citations.