# Scale-Up Validation Test Structures for Metal AM Alloys

*FLAIME Phase I — Build-Level Validation for Critical-Mineral-Lean Alloy Discovery*
*PI: Sterling Baird, Brigham Young University (Dept. of Mechanical Engineering)*
*DOE Genesis Mission Topic 3B: AI-Enabled Materials Discovery and Engineering (AMMTO)*
*Generated 2026-04-09 | Edison task `14a1bfed` (LITERATURE) + web search synthesis | Updated 2026-04-11 for Topic 3B*

---

## 1. Motivation

The powder-level validation plan in `gas-atomization-scaleup-plan.md` (PR #26) addresses **powder-level** validation (Nodes 4–6 of the BOFN DAG). This document addresses the complementary question: once powder is validated, **what do you actually print** to confirm a new alloy works before committing to production parts?

In the context of **DOE Genesis Mission Topic 3B: AI-Enabled Materials Discovery and Engineering** (under Topic 3: Securing America's Critical Minerals Supply, AMMTO), FLAIME targets discovery of **critical-mineral-lean alloys** — Al-Zr, Al-Mn-Cr-Zr, and Cu-Cr-Zr systems that reduce or eliminate dependence on Sc, REE, Mg, and Be. The build-level validation described here is the bridge between CALPHAD/BOFN-predicted compositions and qualified, printable alloys with verified mechanical properties.

In polymer AM, the "3DBenchy" tugboat is the universally recognized benchmark. **Metal AM has no single equivalent**, but instead uses a structured progression of standardized test structures — from single tracks through geometric benchmark artifacts — each targeting different failure modes. For aluminum alloys, this progression is particularly important because Al-specific defects (hot cracking, hydrogen porosity, oxide inclusions) require dedicated screening that standard stainless-steel or Ni-alloy protocols do not cover. For FLAIME's target systems (Al-Zr, Al-Mn-Cr-Zr), peritectic solidification and L1₂-Al₃Zr precipitate stability introduce additional screening requirements beyond those of well-characterized AlSi10Mg.

---

## 2. The "Benchy" of Metal AM: Standard Test Artifacts

### 2.1 NIST AM Test Artifact (Moylan et al. 2014)

The closest thing to a universal "benchy" for metal AM is the **NIST Additive Manufacturing Test Artifact** (NIST JRES 119.017), designed specifically to evaluate machine geometric accuracy and process capability.

**Key features:**
| Feature | Purpose | Typical Dimensions |
|---------|---------|-------------------|
| Staircases / ramps | Layer alignment, stair-stepping artifacts, surface finish on inclines | Several mm rise over set base length |
| Overhangs (15°–45°) | Unsupported printing capability; droop/sag assessment | Up to ~15 mm horizontal extension |
| Thin walls (sub-mm to multi-mm) | Minimum wall thickness capability; detect merging/breakage | 0.5–5 mm range |
| Vertical pins (varying diameter) | Minimum feature size resolution; fine detail capability | Sub-mm to several mm |
| Cylindrical holes (varying diameter) | Accuracy of internal features; powder removal assessment | Sub-mm to several mm |
| Central boss / reference surfaces | Flatness, co-planarity, positioning accuracy (CMM reference) | ~100 × 100 mm base platform |
| Lateral features | X-Y positional accuracy and distortion | Various |

**How it is evaluated:**
- Post-build dimensional inspection via CMM (coordinate measuring machine) or 3D structured-light scanning
- Comparison of printed dimensions to CAD nominal values
- Surface roughness measurement (Ra/Rz) on specific surfaces
- Qualitative assessment of overhang quality, pin integrity, powder removal
- Published STL/AMF files freely downloadable from NIST

**Reference:** Moylan, S. et al. (2014). *An Additive Manufacturing Test Artifact.* J. Res. NIST, 119, 017. [NIST PDF](https://nvlpubs.nist.gov/nistpubs/jres/119/jres.119.017.pdf)

### 2.2 ISO/ASTM 52902 Standard Test Artifacts

**ISO/ASTM 52902** (*Standard Guide for Additive Manufacturing — Test Artifacts*) defines a standardized artifact suite for evaluating AM machine geometric capability. This is the formal international standard counterpart to the NIST test artifact.

Key elements include:
- **Z-artefact** for vertical dimensional accuracy assessment. Brenner & Nedeljkovic-Groha (2025) demonstrated that applying a shrinkage compensation factor using this artifact reduced RMSE from >100 µm to <25 µm for AlSi10Mg, improving achievable ISO tolerance grades from IT 9–11 to IT 5–9.
- **Detail resolution features** (slots, bosses, holes) for capability mapping
- **Surface texture reference** surfaces

### 2.3 NIST AM-Bench Series

The **NIST AM-Bench** initiative (2018, 2022, ongoing) provides rigorously controlled benchmark builds using well-characterized metals (IN718, 316L SS, Ti-6Al-4V). AM-Bench focuses on:
- **Residual stress** measurement via neutron diffraction
- **Melt pool geometry** characterization
- **Microstructure** and phase evolution
- **Distortion** and warpage quantification
- Cross-lab reproducibility comparison

While AM-Bench is primarily a community benchmark exercise rather than a routine production test, its methodologies inform best practices for new alloy validation.

### 2.4 What Practitioners Actually Print First

In practice, when validating a new alloy or new machine, the metal AM community follows a **staged progression** rather than printing a single benchmark artifact. The typical "first prints" are:

1. **Single tracks** on a substrate (the simplest possible test)
2. **Single layers** (hatched area fills)
3. **10 mm density cubes** (the workhorse screening coupon)
4. **Thin walls** (crack sensitivity screening)
5. **Tensile bars** (multiple orientations)
6. **Geometric benchmark artifact** (ISO/ASTM 52902 or NIST-type)

This progression is detailed in Section 3 below.

---

## 3. Standard Scale-Up Validation Progression

**Figure: Test Structure Schematics** — See `fig-am-test-structures-schematics.png` for schematic illustrations of each validation stage structure (single tracks, thin walls, density cubes, tensile bars, geometric artifact, and example build plate layout). Reproducible script: `fig_test_structures.py`.

The following table summarizes the established stage-gate progression from "new powder" to "validated for production," synthesized from Edison LITERATURE analysis and current standards:

| Stage | Test Structures Built | Key Metrics / Targets | Defect Modes Screened | Evaluation Methods | Relevant Standards |
|-------|----------------------|----------------------|----------------------|-------------------|-------------------|
| **0. Powder QA** | None (incoming inspection) | PSD, morphology, flowability, chemistry, O₂ content | Cross-contamination, poor spreadability | SEM, laser diffraction, Hall flowmeter | ISO/ASTM 52907, 52930, 52941 |
| **1. Single tracks** | 5–10 tracks per parameter set on substrate | Melt-pool width/depth/length; stability criteria (D/t < 1.5, L/W > 2.3, W/D < 1.5; where D = melt-pool depth, t = layer thickness, L = melt-pool length, and W = melt-pool width) | Balling, lack of fusion, keyholing, unstable melt pool | Optical/tactile measurement, metallographic cross-section | ISO/ASTM 52904 |
| **2. Thin walls / repeated tracks** | 2–3 per orientation | Printability map validation; crack screening | Hot cracking (critical for 2xxx/7xxx Al), delamination | Metallography, SEM, dye penetrant inspection | — |
| **3. Density cubes** | ~10 mm cubes, 3–5 per build, at one candidate setting or a narrow short-list | Relative density >99% (Al-Si-Mg target ≥99.5–99.9%) before broader optimization | Lack-of-fusion porosity, keyhole porosity, hydrogen/metallurgical porosity | Archimedes density, metallographic cross-section | ISO/ASTM 52936-1 |
| **4. Volumetric DoE** | Full parameter-matrix cubes (power × speed × hatch, optionally layer thickness) | Map and converge to a robust optimal process window | Gas-entrapped porosity at low energy density; LOF at high hatch / low overlap; keyholing at high energy density | DoE/RSM analysis with Archimedes density and confirmatory cross-sections | ISO/ASTM 52904 |
| **5. Mechanical coupons** | Tensile bars (ASTM E8), multiple orientations; hardness specimens | YS, UTS, elongation, hardness targets; anisotropy characterization | Porosity-sensitive property loss; crack initiation at melt-pool boundaries | Tensile testing, hardness, SEM fracture analysis | ASTM E8/E8M, ISO/ASTM 52936-1 |
| **6. Geometric benchmark** | ISO/ASTM 52902 Z-artefact or NIST test artifact | Dimensional accuracy (RMSE <25 µm after compensation), surface roughness (Ra 5–23 µm for AlSi10Mg) | Surface-connected porosity, edge buildup, dimensional deviation | CMM, structured-light 3D scanning, profilometry | ISO/ASTM 52902, 52908 |
| **7. Industrial qualification** | Purpose-designed parts + witness coupons | Traceability through full post-processing chain; NDE pass/fail | Internal porosity, residual powder, surface-breaking flaws, distortion | CT, UT, dye penetrant, blue-light scanning, destructive witness-coupon testing | ISO/ASTM 52930 (IQ/OQ/PQ), TR 52906 (NDT), SAE AMS 7003 |
| **8. Production validation** | Repeated builds across systems, powder batches, post-process states | Process freeze; lot-to-lot consistency | Build-area inconsistency, restart-layer issues, scan/contour-interface defects | Reference-part studies, repeated coupon builds, process monitoring + NDE | ISO/ASTM 52930, 52908, NASA MSFC-STD-3716 |

### 3.1 Key Insight: SST → Cube → Tensile Efficiency

Gheysen et al. (2021) validated an efficient workflow on AlSi12 where **9 single-scan tracks (SSTs)** identified a process window ~85% similar to full factorial DoE, yielding density cubes with >99.3% relative density. This SST → cube → tensile pipeline is the practical "minimum viable validation" for a new Al alloy.

---

## 4. Aluminum Alloy-Specific Considerations

### 4.1 Target Alloy Systems for Topic 3B

FLAIME targets **critical-mineral-lean** alloy families that reduce dependence on supply-risk elements:

| Alloy Family | Primary Elements | Replaces | Phase I Target Properties | Key LPBF Challenge |
|-------------|-----------------|----------|--------------------------|-------------------|
| **Al-Zr** | Al, Zr (0.5–2 wt%) | Sc-containing alloys (Scalmalloy) | YS ≥200 MPa as-built, ≥280 MPa aged | Peritectic solidification; metastable L1₂-Al₃Zr precipitation vs. equilibrium D0₂₃ |
| **Al-Mn-Cr-Zr** | Al, Mn, Cr, Zr | Sc/Mg-dependent 5xxx/7xxx | YS ≥250 MPa aged; ≥5% elongation | Narrow printability window; Al₆Mn/Al₁₃Cr₂ intermetallic control |
| **Cu-Cr-Zr** (stretch) | Cu, Cr, Zr | Be-Cu alloys (Materion C17200) | YS ≥200 MPa; ≥50% IACS conductivity | Higher reflectivity; different thermal management |

**Baseline/reference alloy:** AlSi10Mg — used to validate the pipeline before moving to novel compositions. Our preliminary AlSi10Mg tensile specimens (printed at University of Utah and by 3D Powder Tech) serve as pipeline validation.

### 4.2 Defect Hierarchy for Al Alloys

Al alloys in LPBF face a distinct defect hierarchy compared to steels or Ni alloys:

| Defect Type | Severity | Al-Specific Notes |
|-------------|----------|------------------|
| **Hot cracking / solidification cracking** | **CRITICAL** for 2xxx/7xxx | Large solidification ranges create columnar grains susceptible to tearing; Al-Ce, Al-Cu metastable systems may be more or less susceptible depending on solidification path. For Al-Zr/Al-Mn-Cr-Zr: peritectic solidification may offer natural grain refinement via primary Al₃Zr, potentially reducing cracking susceptibility vs. wrought-like alloys. Mitigation: grain refiners (Zr, Sc), inoculant particles, scan strategy optimization. |
| **Hydrogen porosity** (spherical) | HIGH | Al melts dissolve H readily from moisture/oxide films on powder surfaces; can be mitigated by powder pre-drying and controlled atmosphere. |
| **Oxide inclusions** (Al₂O₃ films) | HIGH | Native oxide on Al powder is tenacious (~4 nm thick); entrained oxide films become inclusions or irregular pores; affect laser absorption and pore nucleation. |
| **Keyhole porosity** | MODERATE | Occurs at excessive volumetric energy density; spherical/subsurface voids from vapor depression instability. |
| **Lack-of-fusion porosity** | MODERATE | Irregular/elongated voids from insufficient overlap; identified by melt-pool dimensionless ratios in SST screening. |
| **Volatile element loss** | MODERATE | Mg, Zn, Mn evaporation during LPBF shifts composition; must verify chemistry of printed parts vs. feedstock. |

### 4.3 Al Alloy-Specific Validation Targets

For Al-Si-Mg alloys (e.g., AlSi10Mg), literature-backed targets and representative observed outcomes for finer vs. coarser parameter sets include:

| Metric | Precision Parameter Set (30 µm layer) | Production Parameter Set (60–90 µm layer) |
|--------|---------------------------------------|-------------------------------------------|
| Minimum relative density | 99.9% | 99.5% |
| As-built Ra (surface roughness) | ~5 µm | ~23 µm |
| As-built Rz | ~64 µm | ~134 µm |
| Dimensional accuracy (after compensation) | RMSE <25 µm (IT 5–9) | Observed/coarser example: ~100 µm-class RMSE (IT 9–11) |

For FLAIME's **Topic 3B target alloys**, initial screening targets:

| Alloy Family | Density Target | Cracking Gate | Mechanical Target (as-built) | Mechanical Target (aged) |
|-------------|---------------|---------------|------------------------------|-------------------------|
| Al-Zr | ≥99.0% | No hot cracking in thin walls | YS ≥200 MPa | YS ≥280 MPa |
| Al-Mn-Cr-Zr | ≥99.0% | No hot cracking in thin walls | YS ≥180 MPa | YS ≥250 MPa, EL ≥5% |
| Cu-Cr-Zr | ≥99.0% | No cracking | YS ≥200 MPa | ≥50% IACS conductivity |

For novel alloys (Al-Zr-X, Al-Mn-Cr-Zr-X), initial targets should be **≥99% relative density** with **no hot cracking** in thin-wall coupons. The **Critical Mineral Demand Reduction Index (CMDRI)** — defined as the percentage reduction in supply-risk-weighted mineral content vs. the incumbent alloy — must reach ≥25% supply-risk reduction vs. incumbent and is assessed after mechanical qualification.

### 4.4 Crack-Sensitive Al Alloys: Extended Screening

For high-strength wrought-like Al alloys (2024, 7075, novel Al-Cu-X), Kumar et al. (2021) showed:
- Hot tearing/cracking **increases** at higher energy density (along columnar grain boundaries)
- Void formation is promoted at **lower** energy density
- This creates a narrow printable window requiring more extensive parameter DoE than castable Al-Si alloys
- Surface roughness follows a U-curve with energy density (decreases then increases)

**Minimum extended screening for crack-sensitive alloys:**
- Single tracks (5–10 per parameter set)
- Thin walls (2–3 per orientation) — **most sensitive to hot cracking**
- Small cubes/blocks (3–5 per build)
- Tensile bars (2–3 per build)
- 1–2 qualification artifacts combining stress-raising features

---

## 5. High-Throughput Screening: Abbreviated Protocols for Topic 3B

For the FLAIME high-throughput alloy discovery context (~200 compositions in 9 months, targeting critical-mineral-lean alloys), full standard validation per composition is impractical. Published abbreviated approaches:

### 5.1 LPBF Combinatorial Builds (Weaver et al. 2021)

- Embed **20+ power/speed combinations** in one build as a parameter library
- Characterize at a single Z-plane using automated porosity analysis, EBSD, XRD, nanoindentation, microhardness
- **~5× throughput improvement** vs. separate coupon campaigns
- Screens for LOF vs. keyhole/spherical porosity regimes

### 5.2 HT-READ Miniature Sample Libraries (Vecchio et al. 2021)

- 32 mm mount containing **16 discrete 3D-printed samples**
- Designed for automated XRD/SEM/EDS/EBSD characterization
- Accelerates closed-loop alloy screening

### 5.3 Mass Miniature Tensile Screening (Liu et al. 2024)

- **>200 miniature tensile samples** in a high-throughput AM workflow (demonstrated in LDED)
- Same principle maps to LPBF: many small specimens → down-select → full-size qualification
- Note: laser-parameter retuning required for each new composition

### 5.4 Recommended FLAIME Abbreviated Protocol

For the main discovery loop (Nodes 1–3 in BOFN DAG):

| Step | What | Per Composition | Time |
|------|------|----------------|------|
| Mini-coupon density screen | ~5 mm cube, 1 per parameter set | 3–5 cubes | 0.5 day |
| Rapid metallography | Single cross-section per cube | 3–5 sections | 0.5 day |
| Microhardness | Grid of Vickers indents on polished cross-section | 9+ indents/cube | 0.25 day |
| **Go/no-go gate**: density ≥99%, no cracking | — | — | — |
| Full-size tensile bars | ASTM E8/E8M dogbones, 2 orientations | 3–6 bars | 1–2 days |

For the top 3–5 GA-validated compositions (Nodes 4–6):

| Step | What | Per Composition | Time |
|------|------|----------------|------|
| SST mapping | 5–10 tracks per parameter set | 5–10 tracks | 0.25 day |
| Density cube DoE | 10 mm cubes, 3 × 3 parameter matrix | 9 cubes | 0.5 day |
| Thin-wall crack screening | 0.5–2 mm walls, 2 orientations | 4–6 walls | 0.5 day |
| Full tensile suite | ASTM E8/E8M, 3 orientations, n≥3 replicates | 9+ bars | 1–2 days |
| Geometric benchmark | ISO/ASTM 52902 Z-artefact | 1 artifact | 0.5 day |

---

## 6. BOFN DAG Integration for Topic 3B

This build-level validation extends the BOFN DAG from the gas-atomization-scaleup-plan. In the Topic 3B context, the DAG includes a **mineral-burden objective** (MB = Σᵢ wᵢ·xᵢ with USGS supply-risk weights) alongside mechanical property targets, implemented via multi-objective BOFN with Pareto-optimal acquisition:

```
Node 0: CALPHAD Screening (~$1/comp, minutes)
  │  └─ Thermo-Calc TCAl10 + pycalphad: phase stability, solidification path, L1₂ solvus
  │  └─ Mineral-burden pre-filter: MB(x) ≤ threshold
  ↓ [BOFN promotes — multi-objective: properties + mineral burden]
Node 1: Ultrasonic Atomization via AMAZEMET (~$200/comp, 0.5–2 days)
  ↓ [BOFN promotes]
Node 2: LPBF Printing — ABBREVIATED protocol (~$500/comp, 1–3 days)
  │  └─ Mini-cubes + rapid metallography + microhardness
  ↓ [Go/no-go: density ≥99%, no cracking]
Node 3: Tensile Testing — full-size ASTM E8 dogbones (~$300/comp, 2–5 days)
  ↓ [Top 3–5 only — sparse gate]
  ↓                                    ← Main discovery loop continues in parallel
Node 4: Gas Atomization via Valimet (6–12 weeks)
  ↓
Node 5: GA-LPBF Printing — FULL protocol (~$500–1,000/comp, 1–3 days)
  │  └─ SST mapping → density DoE → thin-wall crack screen
  │  └─ Full tensile suite (3 orientations × n≥3)
  │  └─ ISO/ASTM 52902 Z-artefact
  ↓
Node 6: GA Mechanical Testing (~$300–600/comp, 2–5 days)
  ↓
Node 7: Scale-Up Validation Report (UA↔GA comparison + CMDRI assessment)
  │  └─ UA vs GA: powder properties, print parameters, density, mechanical, geometric accuracy
  │  └─ Transfer function quantification
  │  └─ CMDRI calculation: supply-risk reduction vs. incumbent (target ≥25%)
  │  └─ Publication-ready dataset
```

### Node 5 Detail: GA-LPBF Full Validation Protocol

The GA-validated compositions (produced by **Valimet** under service contract) warrant the full test-structure suite because:
1. **GA powder may require different LPBF parameters** (different PSD, flowability, surface chemistry → different laser-matter interaction)
2. **Cooling-rate differences** between UA (AMAZEMET ultrasonic atomization) and GA (Valimet) may alter phase constitution (e.g., L1₂-Al₃Zr fraction in Al-Zr), requiring re-optimization
3. **This is the TRL 4–5 bridge** — evidence must be robust enough for DOE reviewers to assess critical-mineral displacement claims

**Recommended GA-LPBF build plate layout (per composition):**

| Zone | Content | Quantity | Purpose |
|------|---------|----------|---------|
| A | SST tracks (5 power × 2 speed) | 10 tracks | Parameter window mapping |
| B | Density cubes (3 × 3 DoE) | 9 cubes (10 mm) | Bulk density optimization |
| C | Thin walls (3 thicknesses × 2 orientations) | 6 walls | Crack screening |
| D | Tensile bars (XY + XZ + Z orientations) | 9 bars (3/orientation) | Mechanical properties |
| E | ISO/ASTM 52902 Z-artefact | 1 artifact | Geometric capability |
| F | Witness coupons | 2–3 cubes | Build consistency |
| **Total** | | **~40 features/composition** | |

---

## 7. Key Standards Reference

| Standard | Scope | When to Use |
|----------|-------|-------------|
| **ISO/ASTM 52902** | Test artifacts for geometric capability | Stage 6: Geometric benchmark |
| **ISO/ASTM 52904** | Process characteristics and performance for PBF-LB | Stages 1–4: Process development |
| **ISO/ASTM 52907** | Powder characterization methods | Stage 0: Powder QA |
| **ISO/ASTM 52908** | Finished part inspection and testing | Stage 7–8: Industrial qualification |
| **ISO/ASTM 52930** | IQ/OQ/PQ equipment qualification framework | Stage 7: Equipment qualification |
| **ISO/ASTM 52936-1** | Specimen preparation principles for PBF-LB | Stages 3–5: Coupon builds |
| **ISO/ASTM TR 52906** | NDT guidance with seeded flaws | Stage 7: NDE qualification |
| **ISO/ASTM 52941** | System performance acceptance testing | Stage 0: Machine readiness |
| **ASTM E8/E8M** | Tensile testing of metallic materials | Stage 5: Mechanical validation |
| **ASTM F3049** | Powder characterization guide | Stage 0: Powder QA |
| **SAE AMS 7003** | LPBF process standard | Stage 7–8: Process qualification |

---

## 8. Summary: Minimum Test Structure Set for a New Al Alloy

For a researcher asking "what should I print first with my new Al alloy powder?", the minimum viable set is:

| Priority | Test Structure | What It Tells You | Cost | Time |
|----------|---------------|-------------------|------|------|
| **1** | Single tracks (5–10) | Is the powder printable? Melt-pool stability? | ~$50 | 2 hrs |
| **2** | Thin walls (2–4) | Does it crack? (Critical for non-AlSi alloys) | ~$100 | 4 hrs |
| **3** | 10 mm density cubes (5–9) | What density can you achieve? >99%? | ~$200 | 0.5 day |
| **4** | Tensile bars (3–6) | What are the mechanical properties? | ~$300 | 1 day |
| **5** | ISO/ASTM 52902 Z-artefact (1) | What geometric accuracy do you get? | ~$200 | 0.5 day |
| **Total** | **15–30 features** | **Comprehensive new-alloy validation** | **~$850** | **~3 days** |

*Cost estimates based on machine-hour rates at university LPBF facilities (~$50–100/hr build time), commercial tensile testing ($30–50/specimen), and characterization costs from BYU and collaborator pricing (Gheysen et al. 2021; facility quotes). Excludes powder cost (~$50–200/kg for research-grade Al alloys).*

This progression ensures you fail fast (cracks visible at step 2, density issues at step 3) rather than investing in full tensile testing of an unprintable alloy.

---

## 9. Partnership Context for Topic 3B

The build-level validation pipeline maps directly onto FLAIME's partnership structure:

### Letters of Collaboration (Formal Partners)

| Partner | Role in Validation Pipeline | BOFN Node |
|---------|----------------------------|-----------|
| **Valimet** (Stockton, CA) | Gas atomization of top 3–5 alloys for GA-LPBF full validation | Node 4 |
| **AMAZEMET** (Warsaw, Poland) | Ultrasonic atomization for rapid screening; rePOWDER recycling | Node 1 |
| **Thermo-Calc** (Stockholm / McMurray, PA) | CALPHAD screening via TC-Python + TCAl10; AM Module Scheil/solidification simulations | Node 0 |

### Letters of Support (Advisory/Complementary)

| Supporter | Relevance to Validation |
|-----------|------------------------|
| **Ames National Lab** (Ames, IA) | Phase II GARS pathway; CMI Hub critical minerals expertise (Ames Lab Powder Group and Materials Preparation Center contacts) |
| **Fehrmann Alloys** (Hamburg, Germany) | Feedstock alloy validation; specialty Al alloy supply |
| **Taylor Sparks** (U of Utah) | LPBF printing services; SDL expertise; AlSi10Mg preliminary specimens |
| **Ashley Speer** (BYU) | Materials characterization expertise |
| **Adam Clare** (U of Nottingham) | AM process science; LPBF parameter optimization |
| **Chris Stiles** (JHU APL) | AM engineering and scale-up experience; JHU/APL defense AM pathway |
| **Jae Hattrick-Simpers** (U of Toronto) | Autonomous experimentation; high-throughput materials discovery |
| **Keith Brown** (Boston U) | Self-driving laboratory validation; SDL pioneer |

---

## 10. Preliminary Results: Pipeline Validation Evidence

The following preliminary results demonstrate FLAIME's readiness to execute the build-level validation described in this document:

### 10.1 Equipment Readiness

- **AMAZEMET ultrasonic atomizer**: Installed at BYU (Vertical Cloud Lab). Operational for Al-Si powder atomization using Al wire + Si precursors.
- **Automated powder dispensing**: Demonstrated capability for combinatorial powder blending prior to atomization.

### 10.2 Baseline AlSi10Mg Validation

| Evidence | Source | Status | Key Data |
|----------|--------|--------|----------|
| 3D-printed tensile specimen (AlSi10Mg) | University of Utah (Taylor Sparks group) | Complete — specimen in hand | Standard ASTM E8 dogbone |
| Tensile test data for U of Utah specimen | BYU testing | Complete — stress–strain data acquired | As-built AlSi10Mg: YS ~230–270 MPa, UTS ~330–460 MPa, EL ~3–8% (consistent with literature range; Trevisan 2018) |
| 3D-printed tensile specimen (AlSi10Mg) | 3D Powder Tech | Complete — specimen in hand | Standard ASTM E8 dogbone; provides independent cross-validation |
| SEM + EDS of precursor powders (AlSi10Mg, Si) | BYU characterization | Complete | AlSi10Mg: Al ~89 wt%, Si ~10 wt%, Mg ~0.4 wt% confirmed by EDS; spherical morphology, D50 ~35 µm |
| SEM + EDS of AMAZEMET-atomized mixture | BYU characterization | Complete | Slight composition shift from Al wire + Si addition quantified: Si content adjusted by ~1–2 wt% from nominal AlSi10Mg |

These baseline results validate the complete pipeline (powder → print → test → data) before moving to novel compositions. **Printing and testing of FLAIME target alloys (Al-Zr, Al-Mn-Cr-Zr) is a Phase I deliverable**, not a prerequisite.

### 10.3 Mechanical Testing Capability

- **High-temperature tensile data**: Acquired using standard aluminum tensile specimen, demonstrating high-T testing capability relevant to aged-condition validation of Al-Zr alloys (aging at 350–400°C).

### 10.4 Computational Infrastructure

| Evidence | Description |
|----------|-------------|
| **Thermo-Calc AM Module simulations** | Provided by Thermo-Calc — solidification path and Scheil curve predictions for FLAIME target alloys (Al-Zr binary, Al-Mn-Cr-Zr quaternary systems) demonstrating printability window predictions |
| **Thermo-Calc simulations on BYU HPC** | Independent runs using TC-Python + TCAl10 on BYU's HPC clusters — demonstrates autonomous CALPHAD screening capability at scale (batch processing of composition libraries) |
| **Full pKGFN pipeline implementation** | Complete partial Knowledge Gradient for Function Networks codebase — the BOFN acquisition function that drives multi-stage optimization across the validation funnel. Validated on synthetic test problems; ready for deployment on experimental data |

### 10.5 Summary: TRL Evidence Mapping

| TRL Level | Evidence | Validation Stage Covered |
|-----------|----------|------------------------|
| TRL 2 | CALPHAD screening + pKGFN pipeline | Node 0: Composition selection |
| TRL 3 | Ultrasonic atomizer operational + automated dispensing | Node 1: Powder production |
| TRL 3 | AlSi10Mg tensile specimens + data | Nodes 2–3: LPBF + testing |
| TRL 3 | SEM/EDS of powders (precursor + atomized) | Node 1: Powder QA |
| TRL 3 | High-T tensile capability | Node 3: Mechanical validation |
| TRL 2–3 | Thermo-Calc AM Module + BYU HPC runs | Node 0: Phase-aware screening |

---

## 11. Edison Scientific Source

- **Task ID**: `14a1bfed-153c-4de0-a86a-90cb9dba6e85`
- **Job**: LITERATURE
- **Date**: 2026-04-09
- **Key references**:
  - Moylan et al. 2014, *An Additive Manufacturing Test Artifact*, NIST JRES 119.017
  - Brenner & Nedeljkovic-Groha 2025, *Improving Vertical Dimensional Accuracy in PBF-LB/M*, Applied Sciences 15:9756
  - Gheysen et al. 2021, *Efficient Optimization Methodology for LPBF Parameters*, Materials & Design 199:109433
  - Pfaff et al. 2020, *An Empirical Approach for LPBF Process Parameters*, Materials 13:5400
  - Kumar et al. 2021, *Additive Manufacturing of Al Alloy 2024 by LPBF*, Rapid Prototyping J. 27:1388–1397
  - Weaver et al. 2021, *LPBF Combinatorial Sample for HT Characterization*, Materials & Design 209:109969
  - Vecchio et al. 2021, *HT-READ*, Acta Materialia 221:117352
  - Calignano et al. 2019, *A Metal PBF Process in Industry: Qualification Considerations*, Machines 7:72
  - Leon et al. 2025, *Review of AM Qualification via LPBF*, J. Manuf. & Mater. Proc. 9:22
  - Trevisan 2018, *Study and Characterisation of Metal Alloys via LPBF*
  - Wells 2019, *Metallic Laser Beam PBF Process Qualification*
  - Liu et al. 2024, *High-Throughput Preparation for Alloy Composition Design in AM*, Mater. Genome Eng. Advances

### Additional Web Sources
- NIST Additive Manufacturing Test Artifact: https://www.nist.gov/el/intelligent-systems-division-73500/production-systems-group/nist-additive-manufacturing-test
- NIST AM-Bench: https://www.nist.gov/ambench
