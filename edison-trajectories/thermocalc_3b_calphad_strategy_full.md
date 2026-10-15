
# CALPHAD Strategy Assessment for FLAIME Genesis Mission — Topic 3B (Critical Minerals, AMMTO)

## Executive Summary

The switch from Topic 12F to Topic 3B fundamentally reframes the CALPHAD strategy. The prior Edison analysis (thermocalc_discussion_analysis.md) was written for Al-Si-Mg as the primary system. This assessment updates all eight dimensions for Al-Zr and Al-Mn-Cr-Zr primary families (~80% Phase I) with Cu-Cr-Zr complement (~20%), where AlSi10Mg serves only as calibration baseline.

---

## 1. CALPHAD Screening Strategy for Topic 3B

### Key Equilibrium & Metastable Phases to Screen

**Al-Zr binary (primary system):**
- **L12-Al₃Zr (METASTABLE, cubic):** The critical strengthening phase for AM. Coherent with FCC-Al (lattice mismatch ~0.75%). Forms during rapid solidification in LPBF. Gibbs energy: -42,500 + 8.5T J/mol. This is the PRIMARY screening target.
- **D023-Al₃Zr (EQUILIBRIUM, tetragonal):** Stable phase. Gibbs energy: -43,299 + 8.8T J/mol (only ~800 J/mol more stable than L12 at 298K). Transforms from L12 during prolonged aging >475-500°C.
- **D022-Al₃M:** Generic tetragonal intermetallic; dissolves Sc, Ti, Zr.
- **Al₂Zr, AlZr, Al₃Zr₂, etc.:** Zr-rich intermetallics — only relevant if compositions stray far from dilute Al-rich corner.

**Al-Mn-Cr-Zr quaternary (dispersoid-strengthened system):**
- **Al₆Mn (orthorhombic):** Primary Mn dispersoid. Dissolves Cr and Fe. Ellipsoid to rod-like morphology. Gibbs energy: -17,795 + 7.67T J/mol.
- **Al₁₂Mn (BCC, metastable):** Occasionally observed. Dissolves Cr and Fe. Gibbs energy: -125,730 + 54.98T + 12·G(Al).
- **Al₁₃Cr₂ / Al₇Cr (monoclinic):** Common Cr-precipitate in 7xxx Al alloys. Key dispersoid phase.
- **Al₁₁Cr₂ (monoclinic):** High-T equilibrium phase (>700°C).
- **α-AlMnSi type (ALCRFEMNSI_A, cubic):** Multicomponent dispersoid — important for quaternary predictions.
- **Mn₂Zr (Laves C15):** Potential competing phase if Mn and Zr levels are high. Forms in liquid.
- **Cr-Zr Laves (C15):** Similar competing intermetallic.

**Cu-Cr-Zr ternary (complement system):**
- **BCC Cr precipitates** from FCC Cu matrix
- **Cu₅Zr:** Precipitation hardening phase
- **Cu-Zr intermetallics:** CuZr, CuZr₂, Cu₅Zr, Cu₈Zr₃, Cu₁₀Zr₇, Cu₅₁Zr₁₄

### Screening Criteria — How Al-Zr/Al-Mn-Cr-Zr Differ from Al-Si-Mg

| Criterion | Al-Si-Mg (Baseline) | Al-Zr / Al-Mn-Cr-Zr (Target) |
|-----------|---------------------|-------------------------------|
| Solidification type | Near-eutectic | **Peritectic** (Al-Zr) |
| Freezing range | Narrow | **Wide** — critical risk factor |
| Crack susceptibility | LOW | **MODERATE-HIGH** — primary screening constraint |
| Strengthening mechanism | Si eutectic + Mg₂Si | **L12-Al₃Zr precipitation** + dispersoid hardening |
| Metastable phase importance | Low | **HIGH** — L12 vs D023 distinction is critical |
| Scheil solidification path | Well-established | Requires careful peritectic treatment |
| Supersaturation relevance | Moderate | **Critical** — Zr solubility in FCC-Al is only 0.083 at.% at equilibrium but 1-3 at.% under LPBF rapid solidification |
| Inoculant/grain refiner | External (TiB₂) | **Intrinsic** — Al₃Zr itself acts as grain refiner |
| Mineral burden | Contains Mg (50% import reliance) | Contains Zr (<25%), Mn (100%), Cr (74%) |

### Recommended Screening Criteria for BOFN Node 0

1. **Crack Susceptibility Index (CSI):** Scheil-derived (Kou criterion or Rappaz-Drezet-Gremaud). Binary constraint: CSI > threshold → reject. Also continuous objective to minimize.
2. **Freezing range (ΔT):** Liquidus − solidus from Scheil. Narrower = better for crack resistance.
3. **L12-Al₃Zr phase fraction:** Maximize volume fraction of L12 precipitates predicted from post-solidification aging simulation.
4. **Zr supersaturation in FCC:** Maximize Zr retained in FCC solid solution after Scheil (proxy for precipitation potential).
5. **Absence of deleterious phases:** Screen against Mn₂Zr Laves, coarse Al₆Mn at grain boundaries.
6. **Mineral burden score:** Weighted critical mineral content (see Section 3).
7. **Equiaxed grain tendency:** G/R ratio from AM Module predictions (equiaxed grains resist hot cracking).

---

## 2. Database Adequacy

### Critical Finding: Free TDB is Insufficient for Quaternary Predictions

Analysis of the open-source MatCalc mc_al_v2.035.tdb (12 elements, 187 phases) reveals:

**Binary coverage — ADEQUATE for all 6 subsystems:**
| Binary | FCC L₀ (J/mol) | Status |
|--------|----------------|--------|
| Al-Zr | -120,000 + 30T | ✓ Complete (strong ordering) |
| Al-Mn | -69,300 + 25T | ✓ Complete |
| Al-Cr | -39,200 + 16T | ✓ Complete |
| Mn-Cr | -19,088 + 17.5T | ✓ Complete |
| Mn-Zr | +20,000 (positive!) | ✓ Complete (immiscible in FCC) |
| Cr-Zr | +20,000 (positive!) | ✓ Complete (immiscible in FCC) |

**Ternary coverage — CRITICAL GAPS:**
| Ternary | mc_al_v2.035 | TCAl8 | TCAl10 |
|---------|-------------|-------|--------|
| Al-Cr-Mn | ✓ 4 params | ✓ | ✓ |
| **Al-Mn-Zr** | **✗ 0 params** | **?** | **✓ (likely)** |
| **Al-Cr-Zr** | **✗ 0 params** | **?** | **✓ (likely)** |
| **Cr-Mn-Zr** | **✗ 0 params** | **?** | **?** |
| Al-Cu-Zr | ✗ 0 params | ? | ✓ (likely) |
| Cr-Cu-Zr | ✓ 3 params (liquid) | ✓ | ✓ |

**The absence of Al-Mn-Zr and Al-Cr-Zr ternary assessments in the free database means quaternary Al-Mn-Cr-Zr predictions from mc_al_v2.035 rely solely on binary extrapolation.** This is scientifically unreliable for multicomponent alloy design.

### Database Recommendation

| Stage | Database | Purpose | Cost |
|-------|----------|---------|------|
| Stage 1 (initial screen) | mc_al_v2.035 via pycalphad | Binary Al-Zr screening (100K+ compositions); ternary Al-Cr-Mn subspace | $0 |
| Stage 2 (refined) | **TCAl10** via TC-Python | Full quaternary Al-Mn-Cr-Zr + Cu-Cr-Zr predictions; top 1,000 candidates | [licence cost removed] |
| Stage 3 (printability) | TC AM Module | Process maps, melt pool geometry for top 50-100 | Included in license |

**TCAl10 is essential**, not optional. TCAl10 (48 elements, 725 phases, 123 ternary systems) vs TCAl8 (BYU current, ~40 elements, ~500+ phases, ~110 ternaries). TCAl10 added 4 new + 6 reassessed ternary systems specifically improving grain refiner understanding and recycling investigations — directly relevant to Al-Zr alloy design. Verification needed on whether TCAl8 covers Al-Mn-Zr and Al-Cr-Zr ternaries.

**ESPEI open-source alternative:** No ESPEI-assessed datasets exist for Al-Zr, Al-Mn, Mn-Zr, or Cr-Zr. Not viable.

---

## 3. Mineral-Burden Objective Quantification

### Proposed Formulation

The mineral burden score (MBS) should be a CALPHAD-integrated screening criterion in the multi-objective BOFN framework:

**MBS(x) = Σᵢ wᵢ · xᵢ**

where xᵢ is the mass fraction of element i, and wᵢ is a criticality weight:

| Element | Import Reliance | wᵢ (proposed) | Rationale |
|---------|----------------|---------------|-----------|
| Sc | 100% | 10.0 | Extremely scarce, $98-350/kg alloy |
| REE (Ce, La) | ~90% | 8.0 | China-dominated supply chain |
| Mg | ~50% | 5.0 | Moderate import reliance |
| Mn | 100% | 7.0 | 100% import-dependent (no US production since 1970) |
| Cr | 74% | 4.0 | Strong recycling base (26% secondary) |
| Zr | <25% | 2.0 | Domestic production exists |
| Cu | Newly critical (2025) | 3.0 | Added to 2025 list |
| Al | 0% (domestic) | 0.0 | Abundant domestic production |
| Si | On 2025 list | 1.0 | Low risk for metallurgical Si |
| Fe | Not critical | 0.5 | Abundant |

**Multi-objective scalarization for BOFN:**

```
Minimize: α₁·CSI(x) + α₂·MBS(x) - α₃·Strength_proxy(x)
Subject to: CSI(x) < CSI_threshold
            MBS(x) < MBS_threshold  
            L12_fraction(x) > min_precipitate
```

Where Strength_proxy = f(Zr_supersaturation, dispersoid_fraction) from CALPHAD.

**Key insight for Topic 3B framing:** The MBS objective explicitly shows that Al-Zr (wZr=2.0) and Al-Mn-Cr-Zr (weighted average ~4-5) alloys have LOWER mineral burden than Al-Sc (wSc=10.0) or Al-Mg-Sc-REE systems (weighted average ~7-8), even though all elements are critical minerals. The score quantifies supply chain risk reduction.

**Note on Mn vulnerability:** Mn's 100% import reliance (wMn=7.0) is actually worse than Mg (wMg=5.0) on a per-element basis. The proposal must frame this carefully: (1) Mn is globally abundant (1.9 billion tons reserves vs. 30-40 t/yr Sc), (2) Mn sources are geographically diversified (Gabon 25%, South Africa 21%, Australia 10%), and (3) the composition optimization can minimize Mn content while maintaining dispersoid strengthening from Cr (lower burden at wCr=4.0).

---

## 4. Updated Hybrid Architecture for Topic 3B

### Reframed Pipeline: pycalphad → TC-Python → AM Module

**Stage 1: Open-Source Binary/Ternary Screen (pycalphad, $0)**
- Database: mc_al_v2.035.tdb (free, ODbL license)
- Scope: 100K+ compositions in Al-Zr binary and Al-Cr-Mn ternary subspaces
- Calculations: Phase equilibria, Scheil solidification, CSI, freezing range
- Outputs: CSI map, Zr supersaturation in FCC, phase fraction maps
- Limitation: Cannot screen full Al-Mn-Cr-Zr quaternary (missing ternary assessments)
- Speed: ~118 calcs/sec (pycalphad vectorized) or 1,000-2,500/sec/core (OpenCalphad)

**Stage 2: Commercial Multicomponent Refinement (TC-Python + TCAl10)**
- Scope: Top 1,000 candidates from Stage 1, extended into full quaternary space
- Calculations: Full quaternary phase equilibria, Scheil with back-diffusion (MOBAL8), TC-PRISMA precipitation kinetics for L12-Al₃Zr aging
- Key addition vs. prior analysis: **TC-PRISMA for L12 precipitation kinetics** — essential for Al-Zr (not needed for Al-Si-Mg where eutectic strengthening dominates)
- Outputs: Refined CSI, L12 number density/size predictions, dispersoid coarsening resistance, mineral burden ranking

**Stage 3: AM Printability Assessment (TC AM Module)**
- Scope: Top 50-100 candidates from Stage 2
- Mode: Steady-state (as recommended by Thermo-Calc's account manager for high-throughput)
- Outputs: Melt pool geometry (depth/width/length), process maps with lack-of-fusion boundaries, G/R solidification conditions, equiaxed-to-columnar transition, thermal profiles
- Key Al-Zr–specific output: **Equiaxed transition prediction** — Al₃Zr acts as intrinsic grain refiner, so G/R → equiaxed boundary is a positive design feature, not just a constraint

**NEW Node 0.5 in BOFN DAG (updated for Topic 3B):**
- Between CALPHAD screening (Node 0) and powder production (Node 1)
- Inputs: composition + machine parameters
- Outputs: printability score, process window width, predicted melt pool dimensions
- Al-Zr specific: absorptivity correction factor (calibrated on AlSi10Mg baseline)
- Cost hierarchy: Node 0 ($0) → Node 0.5 ($) → Nodes 1-8 ($$$)

### Architecture Change from Prior Analysis
The prior analysis assumed Al-Si-Mg as primary, where Scheil solidification was relatively straightforward (near-eutectic). For Al-Zr:
1. **TC-PRISMA becomes essential** (not just nice-to-have) for L12 precipitation kinetics
2. **Metastable phase treatment is critical** — must include L12-Al₃Zr in Scheil calculations
3. **Supersaturation tracking** — equilibrium Zr solubility (0.083 at.%) vs. LPBF-retained (1-3 at.%) creates a gap that equilibrium CALPHAD cannot bridge without Scheil + kinetic modeling
4. **Stage 1 scope is limited** to binaries and Al-Cr-Mn ternary (cannot do full quaternary with free TDB)

---

## 5. AM Module Considerations for Al-Zr

### Absorptivity Challenge (Amplified for Al-Zr)

Thermo-Calc's account manager's key point: AM Module calculates absorptivity from electrical resistivity of the liquid, which works for steels/Ni alloys but fails for aluminum due to the Al₂O₃ oxide film. This applies to ALL aluminum alloys, not just Al-Si-Mg.

**Al-Zr specific considerations:**
- Zr additions increase oxide film stability (Zr is a strong oxide former; ZrO₂ forms alongside Al₂O₃)
- The absorptivity pre-factor calibrated on AlSi10Mg may NOT transfer to Al-Zr compositions
- **Calibration strategy:** (1) Calibrate on AlSi10Mg first (commercially available powder), (2) Print single tracks of Al-Zr at 5-10 power/speed combinations, (3) Cross-section melt pools to measure width/depth, (4) Adjust pre-factor, (5) Treat as Bayesian learnable parameter in BOFN for novel compositions

### Solidification Behavior Differences

| Property | Al-Si-Mg (AlSi10Mg) | Al-Zr (dilute, 0.5-2 wt% Zr) |
|----------|---------------------|-------------------------------|
| Solidification type | Eutectic | **Peritectic** |
| Primary phase | α-Al + Si eutectic | α-Al (supersaturated with Zr) |
| Freezing range | ~30-50°C (narrow) | **~100-200°C (wide)** |
| Liquid feeding | Excellent (eutectic) | **Poor** (no eutectic healing) |
| Grain structure | Columnar-dominant | **Equiaxed possible** (Al₃Zr nucleation) |
| Post-print strengthening | Minimal (already strengthened) | **Aging required** (L12 precipitation at 350-425°C) |
| Thermal stability | Degrades >200°C | **Excellent** (L12 stable to ~400°C) |

### Printability Assessment
Al-Zr alloys present a fundamentally different printability profile:
- **Risk:** Wide freezing range → hot cracking
- **Opportunity:** Intrinsic grain refinement → equiaxed grains → crack mitigation
- The AM Module's equiaxed transition model (G/R-based) becomes a **design optimization target**, not just a diagnostic. Thermo-Calc's account manager mentioned tunable parameters (dendrite tip undercooling: 2-3 K) that would need calibration.

### Calibration Challenges Specific to Al-Zr
1. **Absorptivity:** Zr oxide effects on top of Al₂O₃ — may need composition-dependent pre-factor
2. **Equiaxed transition parameters:** Dendrite tip undercooling for Al₃Zr nucleation — no published calibration data for LPBF
3. **Powder characteristics:** Ultrasonic atomization of Al-Zr may produce different particle morphology than gas-atomized AlSi10Mg — affects packing density and effective thermal conductivity inputs
4. **No existing AM Module validation for Al-Zr:** This is uncharted territory. AlSi10Mg has extensive validation; Al-Zr has essentially none for the AM Module.

---

## 6. Risk Assessment

### CALPHAD-Specific Risks for Al-Zr/Al-Mn-Cr-Zr

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|------------|
| **Ternary database gaps** | **CRITICAL** | mc_al_v2.035 has ZERO ternary parameters for Al-Mn-Zr, Al-Cr-Zr, Cr-Mn-Zr. Quaternary predictions unreliable without TCAl10. | TCAl10 essential. Verify coverage before purchase. Stage 1 limited to binaries. |
| **Peritectic crack susceptibility** | **HIGH** | Al-Zr wide freezing range inherently crack-prone. No eutectic healing mechanism. | Scheil-based CSI as primary filter. Inoculant design. Process parameter optimization. |
| **Metastable L12 prediction gap** | **HIGH** | Equilibrium CALPHAD predicts D023, not L12. L12 retention under LPBF cooling rates requires non-equilibrium treatment. | Scheil with metastable L12 phase included. TC-PRISMA for precipitation kinetics. Experimental validation essential. |
| **Absorptivity model failure** | **MODERATE-HIGH** | AM Module absorptivity based on electrical resistivity — invalid for Al due to oxide. Zr additions may worsen. | AlSi10Mg calibration first. Bayesian learnable pre-factor. Relative predictions even if absolute values off. |
| **Mn₂Zr Laves phase competition** | **MODERATE** | Mn-Zr FCC interaction is +20,000 J/mol (immiscible), but Mn₂Zr Laves forms in liquid. May consume Zr intended for L12 precipitation. | Screen against Laves formation in Scheil. Constrain Mn/Zr ratio. |
| **TCAl8 vs TCAl10 coverage uncertainty** | **MODERATE** | BYU currently has TCAl8. Unknown if TCAl8 covers Al-Mn-Zr and Al-Cr-Zr ternaries. TCAl10 adds 4 new ternaries but specific systems unconfirmed. | Request TCAl10 ternary system list from Thermo-Calc's account manager before purchase. |
| **Quaternary phase space unexplored** | **MODERATE** | Al-Mn-Cr-Zr is largely uncharted experimentally. CALPHAD predictions in this space are extrapolative. | This is actually the opportunity — FLAIME's value proposition is exploring this space. But validate early. |
| **Equiaxed transition model tuning** | **LOW-MODERATE** | G/R model has tunable parameters (dendrite tip undercooling) with no Al-Zr LPBF calibration data. | Use as directional guidance. Validate with EBSD. Report parameter sensitivity. |
| **Cu-Cr-Zr atomization** | **MODERATE** | No ultrasonic atomization precedent. Very high reflectivity at 1064nm for LPBF. | Phase II only (~20% effort). Gas atomization for Cu-Cr-Zr. |

### Risk Comparison: Al-Si-Mg vs Al-Zr

The switch to Al-Zr introduces HIGHER CALPHAD risk than the original Al-Si-Mg focus:
- Al-Si-Mg: Well-characterized eutectic system, extensive AM validation, abundant literature
- Al-Zr: Peritectic system with metastable phase complexity, no AM Module validation, sparse quaternary data

**However, this higher risk is the competitive advantage** — it positions FLAIME as doing genuinely novel alloy discovery rather than incremental optimization of a known system.

---

## 7. Thermo-Calc Collaboration Reframing for Topic 3B

### Letter of Support — Updated Positioning

The prior framing emphasized Al alloy discovery broadly. For Topic 3B, the letter should emphasize:

1. **Critical mineral mission alignment:** "Thermo-Calc supports BYU's mission to discover aluminum alloys that reduce dependence on critical minerals (Mg, Sc, REE) through computational screening of Al-Zr and Al-Mn-Cr-Zr alloy families."

2. **TCAl10 as enabling infrastructure:** "The TCAl10 database provides assessed thermodynamic descriptions for all binary and ternary subsystems of the Al-Mn-Cr-Zr quaternary space, enabling reliable predictions in a composition domain with limited experimental data."

3. **Reciprocal data value (ENHANCED for Topic 3B):** The prior analysis noted a Thermo-Calc specialist's suggestion to include data feedback in the letter. For Topic 3B this is even stronger: BYU would provide Thermo-Calc with the FIRST AM Module validation data for Al-Zr alloys — a composition space with zero existing calibration. This is more valuable to TC than additional Al-Si-Mg data.

4. **Crack susceptibility model testing:** a Thermo-Calc specialist explicitly suggested testing edge-case compositions at predicted crack/no-crack boundaries. For Al-Zr peritectic alloys, this is particularly valuable because crack models are less validated in peritectic systems than eutectic ones.

5. **Five AM Module outputs** confirmed by a Thermo-Calc specialist (melt pool shape, process maps, G/R conditions, equiaxed transition, thermal profiles) should be listed explicitly.

### AM Module Demo — Updated Request

Send Thermo-Calc's account manager: Al-0.5wt%Zr composition + standard LPBF parameters (200W, 800mm/s, 30μm layer, 100μm hatch). Request:
- Process map showing lack-of-fusion and keyholing boundaries
- Melt pool geometry prediction
- G/R map with equiaxed transition line
- Comparison with AlSi10Mg at same parameters

This directly demonstrates the value for Topic 3B (Al-Zr) rather than the generic Al alloy demo originally planned.

### Advisory Hours — Updated Focus

The "single-digit hours per year" advisory commitment should focus on:
1. Validating Scheil solidification paths for peritectic Al-Zr (Month 1-2)
2. Reviewing quaternary Al-Mn-Cr-Zr phase predictions (Month 2-3)
3. Absorptivity calibration review for Al-Zr (Month 3-4)
4. Crack susceptibility model interpretation for novel compositions (Month 4-6)

---

## 8. Competitive Advantage

### CALPHAD Capabilities Uniquely Positioning FLAIME for Topic 3B

1. **Three-tier computational funnel:** pycalphad ($0, 100K+ compositions) → TC-Python/TCAl10 (top 1,000) → AM Module (top 50-100). No competitor has this integrated cost-aware pipeline. The prior analysis noted 88% sample savings from BOFN; the three-tier funnel extends this into composition space.

2. **Mineral burden as a first-class CALPHAD objective:** No existing alloy discovery framework integrates USGS critical mineral supply chain data as a quantitative optimization objective alongside phase stability and printability. The MBS formulation (Section 3) is novel.

3. **Peritectic system expertise:** Most CALPHAD-guided AM alloy discovery focuses on eutectic systems (Al-Si, Al-Ce). Al-Zr peritectic alloys require different screening criteria (supersaturation, L12 metastable phase, intrinsic grain refinement). FLAIME's framework handles this through Scheil + TC-PRISMA integration.

4. **Closed-loop BOFN integration:** The 9-node DAG with p-KGFN cost-aware evaluation is uniquely suited to the multi-fidelity CALPHAD pipeline. Crack susceptibility (Node 0, $0) filters before printability assessment (Node 0.5, $) filters before expensive experiments (Nodes 1-8, $$$).

5. **Uncharted composition space = high discovery potential:** Al-Mn-Cr-Zr quaternary has essentially no prior experimental AM data. CALPHAD-guided exploration of this space is exactly what Topic 3B calls for — AI-enabled discovery of new alloys, not incremental optimization.

6. **Reciprocal TC collaboration value:** First AM Module validation for Al-Zr LPBF. Thermo-Calc is providing a **letter of collaboration** (not just support), with AM Module simulations already delivered as preliminary results and TC-Python running on BYU HPC. This differentiates from competitors with generic TC support letters.

7. **Open-source + commercial hybrid:** Using pycalphad for initial screening (transparent, reproducible, free) combined with TCAl10 for refined predictions addresses both the open-science ethos of DOE and the practical need for validated multicomponent databases.

### What Competitors Likely Cannot Match

- Most CALPHAD-only approaches lack the BOFN cost-aware experimental optimization loop
- Most ML-only approaches lack physics-based CALPHAD grounding for novel composition spaces
- The mineral burden quantification as an optimization objective is novel and directly aligned with Topic 3B
- The AlSi10Mg → Al-Zr absorptivity transfer learning approach (Bayesian learnable parameter) is a unique methodological contribution

---

## Key Quantitative Parameters from Retrieved Data

- **Al-Zr FCC L₀:** -120,000 + 30T J/mol (strong ordering tendency)
- **Al-Zr Liquid L₀:** -150,000 + 45.7T J/mol (very strong liquid interaction)
- **Equilibrium Zr solubility in FCC-Al:** ~0.083 at.% at peritectic (~661°C)
- **LPBF-retained Zr in FCC:** 1-3 at.% (10⁵-10⁷ K/s cooling rates)
- **L12-Al₃Zr Gibbs energy:** -42,500 + 8.5T J/mol
- **D023-Al₃Zr Gibbs energy:** -43,299 + 8.8T J/mol (only ~800 J/mol more stable)
- **Mn-Zr FCC L₀:** +20,000 J/mol (positive = immiscible in solid state)
- **Cr-Zr FCC L₀:** +20,000 J/mol (positive = immiscible in solid state)
- **Free TDB ternary gaps:** 0 parameters for Al-Mn-Zr, Al-Cr-Zr, Cr-Mn-Zr
- **TCAl10:** 48 elements, 725 phases, 123 ternary systems
- **Zr import reliance:** <25% (domestic production exists)
- **Mn import reliance:** 100% (no US production since 1970)
- **Cr import reliance:** 74% (26% from recycling)
- **Sc import reliance:** 100% (30-40 t/yr global supply) — the element being replaced

---

## Discretionary Analytical Decisions

- **Mineral burden weight assignment (wᵢ values):** Weights were assigned proportionally to US import reliance with adjustments for supply concentration risk and global abundance. Alternative weighting schemes (e.g., based on price volatility, Herfindahl-Hirschman Index of supply concentration, or DOE CMS pillar scores) would be equally valid and could shift the relative ranking of Mn (wMn=7.0) vs Mg (wMg=5.0).

- **Characterization of Al-Zr crack susceptibility as "MODERATE-HIGH":** This qualitative assessment is based on the peritectic solidification mechanism and wide freezing range. Some researchers classify dilute Al-Zr as moderate risk due to intrinsic grain refinement by Al₃Zr. The actual crack susceptibility is highly composition-dependent and should be determined quantitatively via Scheil-based CSI calculations.

- **TCAl10 recommended over TCAl8 without confirmed ternary system list:** The recommendation to upgrade is based on TCAl10's 4 new + 6 reassessed ternary systems and 725 vs ~500+ phases, but the specific ternary systems added were not confirmed from the product page. It is possible TCAl8 already covers Al-Mn-Zr and Al-Cr-Zr. Verification with Thermo-Calc's account manager is recommended before purchase decision.

- **Three-tier architecture (pycalphad → TC-Python → AM Module) rather than two-tier:** Chose to recommend a three-stage funnel rather than using TC-Python for all screening. An alternative valid approach would be to use TCAl10 via TC-Python from the start (simpler workflow but higher license utilization and no open-source reproducibility at Stage 1).

- **Mn₂Zr Laves phase classified as moderate risk rather than high:** The positive Mn-Zr FCC interaction (+20,000 J/mol) confirms FCC immiscibility, but Laves formation depends on composition and cooling rate. At dilute Mn/Zr levels typical for wrought Al alloys, Laves formation may be kinetically suppressed. Higher Mn/Zr ratios would warrant elevating this to high risk.

- **Absorptivity treated as Bayesian learnable parameter:** Recommended treating the AM Module absorptivity pre-factor as a composition-dependent learnable parameter in BOFN rather than a single calibration constant. A simpler approach (calibrate once on AlSi10Mg, hold fixed for all Al alloys) would be computationally cheaper but less accurate for novel compositions.

- **Use of MatCalc mc_al_v2.035 as the reference free TDB:** Other free TDBs exist (e.g., from TDBDB or individual publications). The MatCalc database was selected because it contains all 12 relevant elements (Al, Cr, Cu, Fe, Mg, Mn, Ni, Sc, Si, Ti, Zn, Zr) in a single consistent assessment with 187 phases under an open license. Individual publication TDBs may have more accurate binary assessments for specific subsystems but cannot be reliably combined.

- **Proposed aging temperature range of 350-425°C for L12-Al₃Zr precipitation:** This range is based on the general literature for Al-Zr alloys. The optimal aging temperature for LPBF-specific microstructures (which have higher initial Zr supersaturation) may differ and should be determined via TC-PRISMA simulations and experimental validation.
