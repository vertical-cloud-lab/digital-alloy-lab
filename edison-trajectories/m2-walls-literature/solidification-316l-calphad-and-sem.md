<!--
Edison Scientific job-futurehouse-paperqa3-high report: 316L solidification in LPBF: CALPHAD and Scheil predictions, cell spacing versus cooling rate, what SEM shows
Task ID: 8357c8f2-d709-40d0-9d47-1ef8900a5ea6
Created: 2026-11-18T18:22:55.314036Z  Status: success
Retrieved with edison-client from GitHub Actions for issue #100 / PR #243.
Prompt: QUERIES['solidification'] in scripts/edison_m2_walls_literature.py
-->

Question: What does CALPHAD (equilibrium and Scheil) predict for the solidification of 316L stainless steel, how does 316L actually solidify in LPBF, and what can etched SEM sections measure that a CALPHAD-based melt-pool model also predicts? Context: laser powder bed fusion (PBF-LB/M, L-PBF) of commercial gas-atomized 316L stainless steel powder (about 15-45 um) on a Concept Laser M2 cusing (CL WRX Control 2.4; two 400 W class continuous-wave Yb fibre lasers at about 1070 nm, only one used; galvanometer scanner; nitrogen or argon; no plate heating; layer thickness 30 or 50 um, not yet confirmed). The machine's production 316L parameter set uses, for the core hatch, 370 W, 1350 mm/s, 0.09 mm hatch spacing and a 130 um spot (P/v = 0.274 J/mm), contours at 100-120 W and 130-220 mm/s with a 50-70 um spot, and an upskin at 200 W, 980 mm/s, 0.075 mm hatch. The build: 12 'comb' parts, each a 44.5 x 12.7 mm base (printed with the production set) carrying 7 thin walls (fins) 1.27 mm thick, 12.7 mm long and 7.6 mm tall on a 7.2 mm pitch. Every wall has its own core and upskin laser power P and scan speed v (contours unchanged): 60 settings from a scrambled Sobol sequence over P = 150-370 W and P/v = 0.09-0.55 J/mm (v about 335-2930 mm/s; about 33-204 J/mm^3 at 30 um layers), plus the production hatch as a control. Three parts stand on each of four removable 88 mm square 316L panels; the fourth panel is turned 90 degrees so its walls run across the recoater instead of along it, and repeats 18 settings and the control, giving 21 pairs printed in both orientations. After the build each part is cut lengthwise near its centreline and between walls 4 and 5, hot-mounted in 1.25 in conductive mounts, ground to the centreline (a section through every wall's thickness and height at mid-length), polished, imaged unetched in an SEM (Thermo Fisher Apreo C) for porosity in each wall's core (at least 0.2 mm from the faces, 1 mm from the base and the top), then etched to reveal the last layer's melt-pool boundaries. The results will be compared with the Thermo-Calc Additive Manufacturing (AM) Module (CALPHAD-based properties; steady-state and transient melt-pool calculations; printability maps of lack of fusion, keyholing and balling), to calibrate and test it, and later builds will choose settings by batch Bayesian optimization.

Answer with citations and DOIs. Quote numbers with the conditions they apply to (material, P, v, spot size and how it was defined, hatch spacing, layer thickness, machine, gas). Prefer primary sources, say where sources disagree, and flag which statements are strongly versus weakly supported. Where a paper gives a data table or an open dataset we could compare against, say exactly where (table or figure number, repository and identifier).

In particular:
1. Liquidus, solidus, freezing range and primary phase (austenite or delta ferrite) for 316L from CALPHAD (Thermo-Calc TCFE, MatCalc, open databases) and from experiment; Creq/Nieq (Schaeffler, WRC-1992) and the effect of composition within the 316L specification; suppression of ferrite at LPBF solidification rates; retained ferrite measured in as-built LPBF 316L.
2. Cellular sub-structure: measured cell spacing in as-built LPBF 316L versus cooling rate or G x R (fitted relations such as lambda = a (G R)^-n, with constants), and how cell size changes from the melt-pool boundary to the centre and with P and v.
3. Microsegregation of Cr, Mo, Ni and Si to the cell walls (TEM, APT, EDS) compared with Scheil predictions, and oxide inclusions.
4. Which etchants and SEM conditions reveal the cells and melt-pool boundaries in 316L.
5. How enthalpy, latent heat and temperature-dependent properties of 316L used in melt-pool models (and in the normalized enthalpy dH/h_s keyhole criterion) were obtained, with values.

## CALPHAD Predictions, LPBF Solidification, and Characterization of 316L Stainless Steel

### 1. CALPHAD Predictions: Liquidus, Solidus, Freezing Range, and Primary Phase

**Equilibrium solidification.** Thermo-Calc calculations for 316L stainless steel using the TCFE database predict an equilibrium liquidus temperature of approximately 1453 °C and a solidus of approximately 1424 °C, yielding a freezing range of about 29 K (wahib2024optimizationofheat pages 59-62). Sotiriou et al. (2021; DOI: 10.3390/iec2m-09237) used Thermo-Calc with TCFE6 for a nominal 316L composition of Fe–18Cr–14Ni–2.6Mo–1Mn–0.03C (wt%) and adopted a solidus of 1400 °C and liquidus of 1459 °C (a 59 K interval) as model inputs for their heat-transfer simulation, with a latent heat of 330 kJ/kg distributed over that range (sotiriou2021microstructuralandthermomechanical pages 2-4, sotiriou2021microstructuralandthermomechanical pages 4-6). These values differ from the Wahib (2024; DOI: 10.34901/mul.pub.2024.074) Thermo-Calc output because the alloy compositions and databases used are not identical—illustrating the sensitivity of CALPHAD predictions to both input chemistry and database version.

**Scheil–Gulliver solidification.** The Scheil–Gulliver model, which assumes no solid-state diffusion and complete liquid mixing, predicts a wider freezing range than equilibrium because extended solute rejection into the liquid depresses the terminal solidus temperature (sotiriou2021microstructuralandthermomechanical pages 8-9). Sotiriou et al. explicitly stated that the Scheil–Gulliver model yields the highest freezing range, while equilibrium gives the lowest, with DICTRA kinetic simulations falling in between depending on the imposed thermal cycle (sotiriou2021microstructuralandthermomechanical pages 8-9). Assi et al. (2024; DOI: 10.3390/app14198649) defined the "critical temperature range" from Scheil as the interval between 95% and 99% solid fraction, which is the most cracking-sensitive portion of the solidification path (assi2024designandassessment pages 5-7).

**Primary phase: δ-ferrite vs. austenite.** For typical mid-specification 316L compositions (Creq/Nieq ≈ 1.3–1.5), CALPHAD and Scheil calculations predict primary δ-ferrite solidification via the ferrite–austenite (FA) mode: L → L + δ → L + δ + γ → γ + δ (liu2026researchprogresson pages 17-19). Grosswendt et al. (2021; DOI: 10.3390/ma14154074) used Thermo-Calc Scheil–Gulliver simulations with an Fe–Cr–Ni pseudobinary at 70 mass% Fe and showed that alloys with Creq/Nieq = 1.35 and 1.43 solidify as primary bcc ferrite, while an alloy with Creq/Nieq = 1.00 solidifies as primary fcc austenite (grosswendt2021impactofthe pages 11-13).

**Creq/Nieq and composition effects.** The Schaeffler equivalents are Creq = %Cr + %Mo + 1.4(%Si) + 0.5(%Nb) and Nieq = %Ni + 0.5(%Mn) + 30(%C); the WRC-1992 equivalents are Creq = %Cr + %Mo + 0.7(%Nb) and Nieq = %Ni + 35(%C) + 20(%N) + 0.25(%Cu) (tonelli2021additivemanufacturingby pages 230-235, liu2026researchprogresson pages 17-19). Within the ASTM A276 316L specification, the permissible Creq/Nieq ratio can range from as low as 1.01 to as high as 2.21, spanning fully austenitic (A) through ferritic–austenitic (FA) solidification regimes (grosswendt2021impactofthe pages 15-17). Below approximately 1.3, fully austenitic solidification is expected; above approximately 1.49 (Schaeffler) or 1.59 (Hammar–Svensson), primary ferrite becomes dominant (grosswendt2021impactofthe pages 11-13, sutton2021developmentofa pages 34-41). This is a **strongly supported** finding from multiple independent studies. Grosswendt et al. recommend restricting the Ni equivalent and setting Cr to 17–18 mass% for PBF-LB/M to maintain Creq/Nieq > 1.3 and avoid ductility-dip cracking that accompanies fully austenitic solidification (grosswendt2021impactofthe pages 15-17).

**Retained ferrite in as-built LPBF 316L.** Despite equilibrium and Scheil predictions of primary δ-ferrite for mid-specification compositions, as-built LPBF 316L is typically fully austenitic with no detectable δ-ferrite by XRD (funch2023thermalstabilityof pages 2-3). This is attributed to the combination of rapid solidification (cooling rates of 10⁵–10⁷ K/s) and intrinsic reheating from subsequent layer deposition, which enables diffusion-driven transformation of initially solidified ferrite into austenite (grosswendt2021impactofthe pages 11-13, liu2026researchprogresson pages 17-19). Grosswendt et al. confirmed that their PBF-LB/M samples A and C were fully austenitic, while sample B retained only a small ferrite fraction (grosswendt2021impactofthe pages 11-13). Some studies have detected trace ferrite by TEM at cell boundaries in SLM 316L (ozel2023microstructureofselective pages 2-5), but the consensus is that the as-built phase is overwhelmingly austenitic. This represents a **strong** finding.

---

### 2. Cellular Sub-Structure: Cell Spacing vs. Cooling Rate

The solidification microstructure of LPBF 316L consists of columnar cellular sub-structures with cell spacings of approximately 0.2–0.8 µm, corresponding to estimated cooling rates of 10⁵–10⁷ K/s (vallejo2021processoptimizationand pages 13-14, fu2021comparisonofthe pages 20-24).

**Empirical relation.** The widely used fitted relation for stainless steels is:

λ (µm) = 80 · Ṫ⁻⁰·³³

where Ṫ is the cooling rate in K/s, a = 80 µm·(K/s)⁰·³³, and n = 0.33 (fu2021comparisonofthe pages 20-24, vallejo2021processoptimizationand pages 13-14, bertoli2019stabilityofcellular pages 5-7). This relation was used by both Fu et al. (2021; DOI: 10.1016/j.addma.2021.102067) and Vallejo et al. (2021; DOI: 10.3390/met11050832) for LPBF 316L, with consistent results.

Bertoli et al. (2019; DOI: 10.1016/j.msea.2018.10.051) systematically varied LPBF parameters and reported the solidification conditions summarized in the following table:

| Sample # | Laser power (W) | Scan speed (mm/s) | Hatch spacing (mm) | P/v (J/mm) | G (K/mm) | R (mm/s) | Modeled G·R (K/s) | G/R (K·s/mm²) | Measured cell size from micrographs (µm) | Estimated cell size from modeled G·R (µm) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 60 | 30 | 0.120 | 2.00 | 7.9×10³ | 15 | 3.1×10⁵ | 194 | ≈0.88 | 1.23 |
| 2 | 175 | 750 | 0.120 | 0.23 | 1.9×10⁴ | 137 | 2.7×10⁶ | 141 | ≈0.61 | 0.60 |
| 3 | 380 | 2500 | 0.025 | 0.15 | 2.3×10⁴ | 176 | 4.2×10⁶ | 132 | ≈0.50 | 0.52 |
| **Relation** | — | — | — | — | — | — | Cooling rate = G·R | — | Approximate values inferred from the cell-size-derived cooling rates reported by Bertoli et al.: 8.7×10⁵, 2.6×10⁶, and 4.7×10⁶ K/s | λ (µm) = 80·(G·R)^−0.33, with G·R in K/s (bertoli2019stabilityofcellular pages 5-7) |


*Table: LPBF 316L process and modeled solidification conditions reported by Bertoli et al. The comparison shows that increasing cooling rate refines the cellular spacing.*

The cooling rate is inversely proportional to the P/v ratio (linear energy density), confirming that G·R ∝ v/P (bertoli2019stabilityofcellular pages 5-7). The G/R ratio remained within a narrow range of 100–200 K·s/mm² across all tested conditions, which is why only columnar cellular morphology was observed—never equiaxed dendrites (bertoli2019stabilityofcellular pages 5-7).

**Spatial variation within melt pools.** Cell size varies systematically within a single melt pool. Near the melt-pool boundary, where the thermal gradient G is highest and the solidification rate R is lowest, finer cells form ("type 1" cells, 0.20–0.40 µm diameter). Toward the melt-pool center/top, where cooling rates decrease, coarser cells develop ("type 2") (hasenbusch2023acomparisonof pages 19-29). Wang et al. (2024; DOI: 10.1007/s11661-024-07644-w) confirmed that G/R decreases from the melt-pool boundary toward the center, promoting a gradual transition from columnar to more equiaxed morphologies (wang2024additivemanufacturinginducedcellstructure pages 4-6). The cells have a 3D prism-like morphology with their long axes aligned along <001> crystallographic directions, and undergo 90° side-branching near melt-pool boundary intersections (wang2024additivemanufacturinginducedcellstructure pages 4-6).

---

### 3. Microsegregation and Oxide Inclusions

**Quantitative STEM-EDS data.** Godec et al. (2020; DOI: 10.1016/j.matchar.2019.110074) provided the most detailed quantitative STEM-EDS measurements for LPBF 316L (EOS M280, 285 W, 960 mm/s, 0.11 mm hatch, nitrogen atmosphere). At the dislocation-based cell walls (position 3): Cr = 17.4 wt%, Mo = 4.2 wt%, Mn = 1.8 wt%, Ni = 13.7 wt%, Fe = 62.9 wt%. Inside the cell (position 2): Cr = 17.0 wt%, Mo = 3.3 wt%, Mn = 1.7 wt%, Ni = 13.5 wt%, Fe = 64.5 wt%. At the melt-pool boundary (position 1): Cr = 16.6 wt%, Mo = 3.1 wt%, Ni = 13.6 wt%, Fe = 64.9 wt% (godec2020quantitativemultiscalecorrelative pages 14-19). Thus, Mo is the most strongly segregated element, with approximately 27% enrichment at cell walls relative to the cell interior, while Cr shows modest enrichment (~2%) and Ni is essentially uniform. The melt-pool boundary is characterized by a Mo and Cr *deficit* relative to both the cell walls and cell interiors, explaining why even minor composition differences produce a strong etching effect that makes melt-pool boundaries visible under optical microscopy (godec2020quantitativemultiscalecorrelative pages 14-19).

**Comparison with Scheil predictions.** Hasenbusch et al. (2023; DOI: 10.1093/micmic/ozad065) compared measured STEM-EDX segregation ratios with both classic Scheil and Scheil-with-solute-trapping models for rapidly solidified 316L-type alloys. Both Scheil variants generally **overestimated** the degree of segregation relative to experiments (hasenbusch2023acomparisonof pages 49-54). This is consistent with the finding by Wang et al. (2024; DOI: 10.1007/s11661-024-07644-w) that Thermo-Calc Scheil simulations for L-PBF 316L show strong Cr and Mo segregation at the end of liquid–solid transformation, but after only 0.1 s the segregation weakens substantially, and after 1 s it is nearly absent, due to the high equilibrium partition coefficients of these elements in austenite (wang2024additivemanufacturinginducedcellstructure pages 4-6). This rapid homogenization explains why experimentally measured segregation is weaker than Scheil predicts.

**Oxide inclusions.** The predominant inclusions in as-built LPBF 316L are nanoscale (5–100 nm) Mn- and Si-rich oxide particles, identified as MnO–SiO₂ type (rhodonite, MnSiO₃), located primarily along cell walls (godec2020quantitativemultiscalecorrelative pages 14-19, hasenbusch2023acomparisonof pages 1-6, barode2025cellstructurein pages 4-7). These particles act as Zener-pinning sites for dislocations (hasenbusch2023acomparisonof pages 1-6). Funch et al. (2023; DOI: 10.1016/j.heliyon.2023.e16555) confirmed that in the as-built state, the particles are primarily Si- and O-rich (amorphous silicates), with average diameters of approximately 50 nm, coarsening to ~100 nm upon annealing at 800 °C (funch2023thermalstabilityof pages 10-13, barode2025cellstructurein pages 4-7).

---

### 4. Etchants and SEM Conditions

Multiple etchants have been documented for revealing cells and melt-pool boundaries in LPBF 316L:

| Etchant name | Composition | Application method and duration | Features revealed | Reference |
|---|---|---|---|---|
| Glycerine aqua regia (glyceregia) | 20 mL glycerine + 10 mL HNO₃ + 30 mL HCl | Chemical immersion; duration not reported | Cellular/dendritic microstructure and arc-shaped melt-pool boundaries | Godec et al. (2020), DOI: 10.1016/j.matchar.2019.110074 (godec2020quantitativemultiscalecorrelative pages 5-9) |
| Ferric-chloride solution | 5 g FeCl₃ + 10 mL HCl + 100 mL ethanol | Chemical immersion; duration not reported | Melt-pool lines preferentially, rather than the full cellular microstructure | Godec et al. (2020), DOI: 10.1016/j.matchar.2019.110074 (godec2020quantitativemultiscalecorrelative pages 5-9) |
| V2A etchant | Proprietary/standard V2A formulation; exact recipe not reported in the cited passage | Chemical immersion at room temperature for 30–60 s | Melt-pool boundaries, grains, subgrain boundaries, and round-to-elongated cellular structures | Özel et al. (2023), DOI: 10.3390/jeta1020005 (ozel2023microstructureofselective pages 2-5) |
| Kalling’s reagent | Exact recipe not reported by Chepkoech et al.; another LPBF-316L study used 100 mL HCl + 5 g CuCl₂ + 100 mL ethanol | Chemical immersion for 40–60 s in Chepkoech et al. | Melt pools and cellular/solidification microstructure | Chepkoech et al. (2024), DOI: 10.3390/ma17040913 (chepkoech2024investigationofmicrostructures pages 4-5, moazzen2025optimumcorrosionperformance pages 2-3) |
| HF–HNO₃–H₂O | HF:HNO₃:H₂O = 2:8:90 by volume | Chemical etching after 1 µm diamond and OP-S polishing; duration not reported | Fine cellular structure; useful for SEM examination of cell walls and associated particles | Barode et al. (2025), DOI: 10.3390/ma18030475 (barode2025cellstructurein pages 4-7, barode2025cellstructurein pages 2-4) |
| Electrolytic nitric acid | 60% aqueous HNO₃ | Electrochemical etching at 0.8 V; duration not reported | Solidification cells, molten-metal flow trails, interpass/melt-pool-related boundaries, and localized heat-affected regions; demonstrated on 316L made by LENS/DED rather than LPBF | Yang et al. (2017), DOI: 10.1007/s11666-016-0480-y (yang2017processstructurepropertyrelationshipsfor pages 8-15, yang2017processstructurepropertyrelationshipsfor pages 15-22) |


*Table: Etchants reported for revealing cellular solidification structures and melt-pool boundaries in additively manufactured 316L. The final nitric-acid procedure is DED-derived and should be validated before applying it to LPBF sections.*

**SEM conditions for microsegregation contrast.** Godec et al. (2020) used electron channelling contrast imaging (ECCI) with a Zeiss Merlin SEM at 30 kV, 2 nA beam current, 7 mm working distance, and a retractable 4-quadrant BSE detector to image dislocation cells and nano-inclusions in bulk polished (unetched) samples (godec2020quantitativemultiscalecorrelative pages 5-9). For EBSD, the same group used a JEOL 6500F at 15 kV, 1.2 nA, 70° tilt, 4×4 binning (godec2020quantitativemultiscalecorrelative pages 5-9). BSE imaging at 20 kV was also used by Bauer (2021; DOI: 10.3929/ethz-b-000503119) for melt-pool characterization (thomas2021predictionofprocess pages 73-76). The key point for the user's experiment (Thermo Fisher Apreo C) is that BSE imaging of unetched sections can directly reveal the cellular microstructure via atomic-number contrast from Mo/Cr segregation, while etching preferentially attacks the composition-different melt-pool boundaries and cell walls.

---

### 5. Thermophysical Properties and the Normalized Enthalpy Keyhole Criterion

The normalized enthalpy criterion, originally formulated by Hann et al. and applied to LPBF by King et al. (2014; DOI: 10.1016/j.jmatprotec.2014.06.005) on a **Concept Laser M2** machine with 316L (CL 20ES powder), defines the transition to keyhole-mode melting. The normalized enthalpy is:

ΔH/h_s = AP / [h_s √(π D u σ³)]

where A is absorptivity, P is laser power, h_s = ρcT_m is the enthalpy at melting, D is thermal diffusivity, u is scan speed, and σ is the Gaussian beam radius (1/e² standard deviation). The keyhole threshold occurs at ΔH/h_s ≈ π T_b/T_m ≈ 6 (king2014observationofkeyholemode pages 6-11).

The following table compiles thermophysical properties of 316L from multiple sources:

| Property | King 2014 | Thermo-Calc (Wahib 2024) | Sotiriou 2021 | Bauer 2021 (1.4404) |
|---|---:|---:|---:|---:|
| Absorptivity, A | 0.40 (king2014observationofkeyholemode pages 28-36) | Not reported | Not reported | Not reported |
| Density, ρ (kg·m⁻³) | 7,980 (king2014observationofkeyholemode pages 28-36) | 7,312 solid; 7,096 mushy; 6,951 liquid (wahib2024optimizationofheat pages 59-62) | 8,030, treated as constant (sotiriou2021microstructuralandthermomechanical pages 4-6) | 7,950 at room temperature; 7,236 at melting temperature (thomas2021predictionofprocess pages 47-49) |
| Enthalpy at melting, hₛ (J·kg⁻¹) | 1.2 × 10⁶ (king2014observationofkeyholemode pages 28-36) | Not reported | Not reported | Not reported |
| Latent heat of fusion (kJ·kg⁻¹) | Not separately reported | 268 (wahib2024optimizationofheat pages 59-62) | 330, distributed from 1,400 to 1,459 °C (sotiriou2021microstructuralandthermomechanical pages 4-6) | 260 (thomas2021predictionofprocess pages 49-52) |
| Thermal diffusivity, D (m²·s⁻¹) | 5.38 × 10⁻⁶ (king2014observationofkeyholemode pages 28-36) | Not reported | Not reported directly | 3.25 × 10⁻⁶ at room temperature; 6.0 × 10⁻⁶ at melting temperature (thomas2021predictionofprocess pages 49-52) |
| Solid thermal conductivity, k (W·m⁻¹·K⁻¹) | Not reported separately | 31.6; versus 29.8 mushy and 17.2 liquid (wahib2024optimizationofheat pages 59-62) | Temperature-dependent: 13.96 at 26.85 °C, 32.82 at 1,226.85 °C, and 35.96 at 1,526.85 °C (sotiriou2021microstructuralandthermomechanical pages 4-6) | 13.4 at room temperature; 28.5 at melting temperature (thomas2021predictionofprocess pages 47-49) |
| Solid specific heat, cₚ (J·kg⁻¹·K⁻¹) | Not reported separately | 909; versus 1,121 mushy and 1,133 liquid (wahib2024optimizationofheat pages 59-62) | Temperature-dependent: 498 at 26.85 °C, 658 at 1,226.85 °C, and 684 at 1,526.85 °C (sotiriou2021microstructuralandthermomechanical pages 4-6) | 470 at room temperature; 730 at melting temperature (thomas2021predictionofprocess pages 47-49) |
| Solidus, Tₛ (°C) | Not reported | 1,424 (wahib2024optimizationofheat pages 59-62) | 1,400, adopted model input rather than a reported TCFE result (sotiriou2021microstructuralandthermomechanical pages 4-6) | Not reported |
| Liquidus, Tₗ (°C) | Not reported | 1,453 (wahib2024optimizationofheat pages 59-62) | 1,459, adopted model input rather than a reported TCFE result (sotiriou2021microstructuralandthermomechanical pages 4-6) | Not reported |
| Freezing interval, Tₗ − Tₛ (K) | Not reported | 29 (wahib2024optimizationofheat pages 59-62) | 59 (sotiriou2021microstructuralandthermomechanical pages 4-6) | Not reported |
| Normalized-enthalpy keyhole threshold, ΔH/hₛ | Approximately 6; ΔH/hₛ = AP/[hₛ√(πDuσ³)], where σ is the Gaussian standard-deviation radius (king2014observationofkeyholemode pages 6-11) | Not reported | Not reported | Not reported |


*Table: Comparison of thermophysical inputs used in four 316L melt-pool modeling sources. The differences show why model predictions depend on the selected property dataset and temperature treatment.*

The significant variation in reported values (e.g., latent heat ranging from 260 to 330 kJ/kg, thermal diffusivity from 3.25 to 6.0 × 10⁻⁶ m²/s) underscores that model predictions are sensitive to the chosen property dataset and whether temperature-dependent or constant properties are used. The King et al. values (A = 0.4, h_s = 1.2 × 10⁶ J/kg, D = 5.38 × 10⁻⁶ m²/s) are particularly relevant because they were calibrated on the same Concept Laser M2 platform described in the user's experiment (king2014observationofkeyholemode pages 28-36, king2014observationofkeyholemode pages 6-11, king2014observationofkeyholemode pages 11-15).

**What etched SEM sections measure that a CALPHAD-based melt-pool model also predicts.** Etched cross-sections reveal melt-pool width and depth (from the last-layer melt-pool boundaries), which are the same geometric quantities predicted by Rosenthal-based or finite-element melt-pool models using CALPHAD-derived thermophysical properties (king2014observationofkeyholemode pages 6-11, king2014observationofkeyholemode pages 11-15). The normalized enthalpy framework collapses melt-pool depth (normalized by beam size) as a function of ΔH/h_s, enabling direct comparison of predicted and measured melt-pool aspect ratios to identify conduction-mode versus keyhole-mode melting regimes. The Thermo-Calc AM Module generates printability maps in P–v space that delineate lack-of-fusion, keyholing, and balling boundaries; the experimentally measured melt-pool dimensions and porosity from etched sections can be overlaid on these maps for calibration and validation (king2014observationofkeyholemode pages 11-15).

---

### Summary of Confidence Levels

| Topic | Confidence |
|---|---|
| Equilibrium liquidus/solidus from Thermo-Calc (~1453/1424 °C) | Moderate (single source with specific composition) |
| Primary δ-ferrite solidification for mid-spec 316L (FA mode) | **Strong** (multiple independent CALPHAD and experimental sources) |
| Fully austenitic as-built LPBF 316L (ferrite suppressed) | **Strong** (consistent across XRD, EBSD, TEM studies) |
| Cell spacing λ = 80·Ṫ⁻⁰·³³ with 0.2–0.8 µm range | **Strong** (multiple studies, well-established relation) |
| Creq/Nieq sensitivity within 316L spec (1.01–2.21 range) | **Strong** (Grosswendt et al. with ASTM A276 analysis) |
| Mo enrichment at cell walls (~27% relative to interior) | Moderate (quantitative from one study, qualitative from several) |
| Scheil overestimation of segregation | Moderate (demonstrated for 316L-type alloys, mechanism explained) |
| Keyhole threshold ΔH/h_s ≈ 6 for 316L on Concept Laser M2 | **Strong** (King et al. 2014, >2200 citations, same machine platform) |
| Latent heat and thermal property values | Moderate–weak (significant scatter across sources; values are composition- and database-dependent) |

---

### Key Data Tables and Open Datasets for Comparison

- Godec et al. (2020), Table 3 and Figure 6: quantitative STEM-EDS compositions at cell walls, cell interiors, and melt-pool boundaries (DOI: 10.1016/j.matchar.2019.110074).
- Bertoli et al. (2019), Table 3: G, R, G·R, G/R for three LPBF parameter sets; Table 4: mechanical properties (DOI: 10.1016/j.msea.2018.10.051).
- King et al. (2014), Table 3: thermophysical constants for normalized enthalpy; Figure 5: melt-pool depth vs. ΔH/h_s for 316L on Concept Laser M2 at two beam sizes (DOI: 10.1016/j.jmatprotec.2014.06.005).
- Grosswendt et al. (2021), Table with Creq/Nieq ratios for three 316L compositions (DOI: 10.3390/ma14154074).
- Wahib (2024), Table 8: Thermo-Calc solidus/liquidus and thermophysical properties for 316L (DOI: 10.34901/mul.pub.2024.074).
- Sotiriou et al. (2021), Table 1: temperature-dependent k and c_p for 316L (DOI: 10.3390/iec2m-09237).

References

1. (wahib2024optimizationofheat pages 59-62): Optimization of heat transfer model used in the continuous casting of stainless steel This article has 1 citations.

2. (sotiriou2021microstructuralandthermomechanical pages 2-4): Marios P. Sotiriou, John S. Aristeidakis, Maria-Ioanna T. Tzini, Ioanna Papadioti, Gregory N. Haidemenopoulos, and Nikolaos Aravas. Microstructural and thermomechanical simulation of the additive manufacturing process in 316l austenitic stainless steel. Proceedings of The 1st International Electronic Conference on Metallurgy and Metals, pages 20, Feb 2021. URL: https://doi.org/10.3390/iec2m-09237, doi:10.3390/iec2m-09237. This article has 12 citations.

3. (sotiriou2021microstructuralandthermomechanical pages 4-6): Marios P. Sotiriou, John S. Aristeidakis, Maria-Ioanna T. Tzini, Ioanna Papadioti, Gregory N. Haidemenopoulos, and Nikolaos Aravas. Microstructural and thermomechanical simulation of the additive manufacturing process in 316l austenitic stainless steel. Proceedings of The 1st International Electronic Conference on Metallurgy and Metals, pages 20, Feb 2021. URL: https://doi.org/10.3390/iec2m-09237, doi:10.3390/iec2m-09237. This article has 12 citations.

4. (sotiriou2021microstructuralandthermomechanical pages 8-9): Marios P. Sotiriou, John S. Aristeidakis, Maria-Ioanna T. Tzini, Ioanna Papadioti, Gregory N. Haidemenopoulos, and Nikolaos Aravas. Microstructural and thermomechanical simulation of the additive manufacturing process in 316l austenitic stainless steel. Proceedings of The 1st International Electronic Conference on Metallurgy and Metals, pages 20, Feb 2021. URL: https://doi.org/10.3390/iec2m-09237, doi:10.3390/iec2m-09237. This article has 12 citations.

5. (assi2024designandassessment pages 5-7): Mariam Assi, Julien Favre, Marcin Brykala, Franck Tancret, and Anna Fraczkiewicz. Design and assessment of an austenitic stainless alloy for laser powder bed additive manufacturing. Applied Sciences, Sep 2024. URL: https://doi.org/10.3390/app14198649, doi:10.3390/app14198649. This article has 6 citations.

6. (liu2026researchprogresson pages 17-19): Kai-Yu Liu, Hong-Biao Dong, and Li-Juan Zhang. Research progress on defect behavior, microstructure, and service performance of additively manufactured austenitic stainless steels. Materials, 19(20):4371, Oct 2026. URL: https://doi.org/10.3390/ma19204371, doi:10.3390/ma19204371. This article has 0 citations.

7. (grosswendt2021impactofthe pages 11-13): Felix Großwendt, Louis Becker, Arne Röttger, Abootorab Baqerzadeh Chehreh, Anna Luise Strauch, Volker Uhlenwinkel, Jonathan Lentz, Frank Walther, Rainer Fechte-Heinen, Sebastian Weber, and Werner Theisen. Impact of the allowed compositional range of additively manufactured 316l stainless steel on processability and material properties. Materials, 14:4074, Jul 2021. URL: https://doi.org/10.3390/ma14154074, doi:10.3390/ma14154074. This article has 14 citations.

8. (tonelli2021additivemanufacturingby pages 230-235): Lavinia Tonelli. Additive manufacturing by lpbf and waam of metals: correlation between production process, microstructure and mechanical properties. Text, Jan 2021. URL: https://doi.org/10.48676/unibo/amsdottorato/9629, doi:10.48676/unibo/amsdottorato/9629. This article has 0 citations and is from a peer-reviewed journal.

9. (grosswendt2021impactofthe pages 15-17): Felix Großwendt, Louis Becker, Arne Röttger, Abootorab Baqerzadeh Chehreh, Anna Luise Strauch, Volker Uhlenwinkel, Jonathan Lentz, Frank Walther, Rainer Fechte-Heinen, Sebastian Weber, and Werner Theisen. Impact of the allowed compositional range of additively manufactured 316l stainless steel on processability and material properties. Materials, 14:4074, Jul 2021. URL: https://doi.org/10.3390/ma14154074, doi:10.3390/ma14154074. This article has 14 citations.

10. (sutton2021developmentofa pages 34-41): BJ Sutton. Development of a primary solidification mode diagram for austenitic stainless steel weld metals using calphad-based modeling. Unknown journal, 2021.

11. (funch2023thermalstabilityof pages 2-3): Cecilie V. Funch, Flemming B. Grumsen, Alice B. da Silva Fanta, Thomas L. Christiansen, and Marcel A.J. Somers. Thermal stability of hierarchical microstructural features in additively manufactured stainless steel. Heliyon, 9:e16555, Jun 2023. URL: https://doi.org/10.1016/j.heliyon.2023.e16555, doi:10.1016/j.heliyon.2023.e16555. This article has 13 citations.

12. (ozel2023microstructureofselective pages 2-5): Emre Firat Özel, Dennis Pede, Claas Müller, Yi Thomann, Ralf Thomann, and Hadi Mozaffari-Jovein. Microstructure of selective laser melted 316l under non-equilibrium solidification conditions. Journal of Experimental and Theoretical Analyses, 1:64-73, Nov 2023. URL: https://doi.org/10.3390/jeta1020005, doi:10.3390/jeta1020005. This article has 7 citations.

13. (vallejo2021processoptimizationand pages 13-14): Nathalia Diaz Vallejo, Cameron Lucas, Nicolas Ayers, Kevin Graydon, Holden Hyer, and Yongho Sohn. Process optimization and microstructure analysis to understand laser powder bed fusion of 316l stainless steel. Metals, 11:832, May 2021. URL: https://doi.org/10.3390/met11050832, doi:10.3390/met11050832. This article has 135 citations.

14. (fu2021comparisonofthe pages 20-24): Jin Fu, Shuo Qu, Jun-Hao Ding, Xu Song, and Mingwang Fu. Comparison of the microstructure, mechanical properties and distortion of stainless steel 316 l fabricated by micro and conventional laser powder bed fusion. Additive Manufacturing, 44:102067, Aug 2021. URL: https://doi.org/10.1016/j.addma.2021.102067, doi:10.1016/j.addma.2021.102067. This article has 218 citations and is from a highest quality peer-reviewed journal.

15. (bertoli2019stabilityofcellular pages 5-7): Umberto Scipioni Bertoli, Benjamin E. MacDonald, and Julie M. Schoenung. Stability of cellular microstructure in laser powder bed fusion of 316l stainless steel. Materials Science and Engineering: A, 739:109-117, Jan 2019. URL: https://doi.org/10.1016/j.msea.2018.10.051, doi:10.1016/j.msea.2018.10.051. This article has 236 citations.

16. (hasenbusch2023acomparisonof pages 19-29): Zachary Arthur Hasenbusch, Andrew Deal, Ben Brown, Davis Wilson, Laurentiu Nastac, and Luke N Brewer. A comparison of solidification structures and submicroscale cellular segregation in rapidly solidified stainless steels produced via two-piston splat quenching and laser powder bed fusion. Microscopy and Microanalysis, 29:1328-1349, Jul 2023. URL: https://doi.org/10.1093/micmic/ozad065, doi:10.1093/micmic/ozad065. This article has 3 citations and is from a peer-reviewed journal.

17. (wang2024additivemanufacturinginducedcellstructure pages 4-6): Xiaobo Wang, Venkata Karthik Nadimpalli, Niels Skat Tiedje, Dorte Juul Jensen, and Tianbo Yu. Additive-manufacturing-induced cell structure in stainless steel 316l: 3d morphology and formation mechanism. Metallurgical and Materials Transactions A, 56:506-517, Nov 2024. URL: https://doi.org/10.1007/s11661-024-07644-w, doi:10.1007/s11661-024-07644-w. This article has 40 citations.

18. (godec2020quantitativemultiscalecorrelative pages 14-19): Matjaž Godec, Stefan Zaefferer, Bojan Podgornik, Mario Šinko, and Elena Tchernychova. Quantitative multiscale correlative microstructure analysis of additive manufacturing of stainless steel 316l processed by selective laser melting. Materials Characterization, 160:110074, Feb 2020. URL: https://doi.org/10.1016/j.matchar.2019.110074, doi:10.1016/j.matchar.2019.110074. This article has 293 citations and is from a peer-reviewed journal.

19. (hasenbusch2023acomparisonof pages 49-54): Zachary Arthur Hasenbusch, Andrew Deal, Ben Brown, Davis Wilson, Laurentiu Nastac, and Luke N Brewer. A comparison of solidification structures and submicroscale cellular segregation in rapidly solidified stainless steels produced via two-piston splat quenching and laser powder bed fusion. Microscopy and Microanalysis, 29:1328-1349, Jul 2023. URL: https://doi.org/10.1093/micmic/ozad065, doi:10.1093/micmic/ozad065. This article has 3 citations and is from a peer-reviewed journal.

20. (hasenbusch2023acomparisonof pages 1-6): Zachary Arthur Hasenbusch, Andrew Deal, Ben Brown, Davis Wilson, Laurentiu Nastac, and Luke N Brewer. A comparison of solidification structures and submicroscale cellular segregation in rapidly solidified stainless steels produced via two-piston splat quenching and laser powder bed fusion. Microscopy and Microanalysis, 29:1328-1349, Jul 2023. URL: https://doi.org/10.1093/micmic/ozad065, doi:10.1093/micmic/ozad065. This article has 3 citations and is from a peer-reviewed journal.

21. (barode2025cellstructurein pages 4-7): Jayant Barode, Marco Brander, Tianbo Yu, Venkata Karthik Nadimpalli, Dorte Juul Jensen, and Xiaobo Wang. Cell structure in lpbf 316l—microstructural heterogeneity, thermal stability, and mechanical properties. Materials, 18:475, Jan 2025. URL: https://doi.org/10.3390/ma18030475, doi:10.3390/ma18030475. This article has 25 citations.

22. (funch2023thermalstabilityof pages 10-13): Cecilie V. Funch, Flemming B. Grumsen, Alice B. da Silva Fanta, Thomas L. Christiansen, and Marcel A.J. Somers. Thermal stability of hierarchical microstructural features in additively manufactured stainless steel. Heliyon, 9:e16555, Jun 2023. URL: https://doi.org/10.1016/j.heliyon.2023.e16555, doi:10.1016/j.heliyon.2023.e16555. This article has 13 citations.

23. (godec2020quantitativemultiscalecorrelative pages 5-9): Matjaž Godec, Stefan Zaefferer, Bojan Podgornik, Mario Šinko, and Elena Tchernychova. Quantitative multiscale correlative microstructure analysis of additive manufacturing of stainless steel 316l processed by selective laser melting. Materials Characterization, 160:110074, Feb 2020. URL: https://doi.org/10.1016/j.matchar.2019.110074, doi:10.1016/j.matchar.2019.110074. This article has 293 citations and is from a peer-reviewed journal.

24. (chepkoech2024investigationofmicrostructures pages 4-5): Melody Chepkoech, Gbadebo Owolabi, and Grant Warner. Investigation of microstructures and tensile properties of 316l stainless steel fabricated via laser powder bed fusion. Materials, 17:913, Feb 2024. URL: https://doi.org/10.3390/ma17040913, doi:10.3390/ma17040913. This article has 25 citations.

25. (moazzen2025optimumcorrosionperformance pages 2-3): Parisa Moazzen, Ayda Shahriari, SeyedAmirReza Shamsdini, Payam Seraj, Foroozan Forooghi, Yahya Aghayar, Sajad Shakerin, Mackenzie Remington Purdy, and Mohsen Mohammadi. Optimum corrosion performance using microstructure design and additive manufacturing process control. npj Materials Degradation, Feb 2025. URL: https://doi.org/10.1038/s41529-024-00548-5, doi:10.1038/s41529-024-00548-5. This article has 29 citations and is from a peer-reviewed journal.

26. (barode2025cellstructurein pages 2-4): Jayant Barode, Marco Brander, Tianbo Yu, Venkata Karthik Nadimpalli, Dorte Juul Jensen, and Xiaobo Wang. Cell structure in lpbf 316l—microstructural heterogeneity, thermal stability, and mechanical properties. Materials, 18:475, Jan 2025. URL: https://doi.org/10.3390/ma18030475, doi:10.3390/ma18030475. This article has 25 citations.

27. (yang2017processstructurepropertyrelationshipsfor pages 8-15): Nancy Yang, J. Yee, B. Zheng, K. Gaiser, T. Reynolds, L. Clemon, W. Y. Lu, J. M. Schoenung, and E. J. Lavernia. Process-structure-property relationships for 316l stainless steel fabricated by additive manufacturing and its implication for component engineering. Journal of Thermal Spray Technology, 26:610-626, Apr 2017. URL: https://doi.org/10.1007/s11666-016-0480-y, doi:10.1007/s11666-016-0480-y. This article has 120 citations and is from a peer-reviewed journal.

28. (yang2017processstructurepropertyrelationshipsfor pages 15-22): Nancy Yang, J. Yee, B. Zheng, K. Gaiser, T. Reynolds, L. Clemon, W. Y. Lu, J. M. Schoenung, and E. J. Lavernia. Process-structure-property relationships for 316l stainless steel fabricated by additive manufacturing and its implication for component engineering. Journal of Thermal Spray Technology, 26:610-626, Apr 2017. URL: https://doi.org/10.1007/s11666-016-0480-y, doi:10.1007/s11666-016-0480-y. This article has 120 citations and is from a peer-reviewed journal.

29. (thomas2021predictionofprocess pages 73-76): Thomas Bauer. Prediction of process parameters in selective laser melting. ArXiv, 2021. URL: https://doi.org/10.3929/ethz-b-000503119, doi:10.3929/ethz-b-000503119. This article has 2 citations.

30. (king2014observationofkeyholemode pages 6-11): Wayne E. King, Holly D. Barth, Victor M. Castillo, Gilbert F. Gallegos, John W. Gibbs, Douglas E. Hahn, Chandrika Kamath, and Alexander M. Rubenchik. Observation of keyhole-mode laser melting in laser powder-bed fusion additive manufacturing. Journal of Materials Processing Technology, 214:2915-2925, Dec 2014. URL: https://doi.org/10.1016/j.jmatprotec.2014.06.005, doi:10.1016/j.jmatprotec.2014.06.005. This article has 2230 citations and is from a domain leading peer-reviewed journal.

31. (king2014observationofkeyholemode pages 28-36): Wayne E. King, Holly D. Barth, Victor M. Castillo, Gilbert F. Gallegos, John W. Gibbs, Douglas E. Hahn, Chandrika Kamath, and Alexander M. Rubenchik. Observation of keyhole-mode laser melting in laser powder-bed fusion additive manufacturing. Journal of Materials Processing Technology, 214:2915-2925, Dec 2014. URL: https://doi.org/10.1016/j.jmatprotec.2014.06.005, doi:10.1016/j.jmatprotec.2014.06.005. This article has 2230 citations and is from a domain leading peer-reviewed journal.

32. (thomas2021predictionofprocess pages 47-49): Thomas Bauer. Prediction of process parameters in selective laser melting. ArXiv, 2021. URL: https://doi.org/10.3929/ethz-b-000503119, doi:10.3929/ethz-b-000503119. This article has 2 citations.

33. (thomas2021predictionofprocess pages 49-52): Thomas Bauer. Prediction of process parameters in selective laser melting. ArXiv, 2021. URL: https://doi.org/10.3929/ethz-b-000503119, doi:10.3929/ethz-b-000503119. This article has 2 citations.

34. (king2014observationofkeyholemode pages 11-15): Wayne E. King, Holly D. Barth, Victor M. Castillo, Gilbert F. Gallegos, John W. Gibbs, Douglas E. Hahn, Chandrika Kamath, and Alexander M. Rubenchik. Observation of keyhole-mode laser melting in laser powder-bed fusion additive manufacturing. Journal of Materials Processing Technology, 214:2915-2925, Dec 2014. URL: https://doi.org/10.1016/j.jmatprotec.2014.06.005, doi:10.1016/j.jmatprotec.2014.06.005. This article has 2230 citations and is from a domain leading peer-reviewed journal.
