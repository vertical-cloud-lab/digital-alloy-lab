# Edison Scientific ANALYSIS: CALPHAD Strategy for Topic 3B (Critical Minerals)

**Task IDs:** `1e432b28-92b6-4a6f-ba40-817137192f87` (full, 4 files), `3e2efa30-8a36-4c7d-93ef-2736914d5704` (focused, 2 files)
**Mode:** ANALYSIS
**Date:** 2026-04-11
**Status:** Both Edison tasks submitted and in progress. Results will be appended when available.
**Inputs:** Cleaned transcript, prior Edison analysis (`eb5a3fde`), Topic 3B context summary
**Context:** PRs #4, #14, #26, #44

---

## Preliminary Assessment (based on prior Edison analyses + PR context)

The following assessment is synthesized from the prior Edison analysis of the Thermo-Calc discussion (task `eb5a3fde`), the 10 Edison LITERATURE_HIGH queries on Topic 3B (from PR #26), the preliminary results roadmap (PR #44), and the BOFN integration architecture (PR #14).

### 1. CALPHAD Screening Strategy for Topic 3B

**Key phases to screen for Al-Zr:**
- **L1₂-Al₃Zr** (metastable) — coherent precipitates, primary strengthening phase in Al-Zr alloys. Nucleation at supersaturation drives strength.
- **D0₂₃-Al₃Zr** (equilibrium, tetragonal) — coarsening-resistant but incoherent; equilibrium CALPHAD predicts this, but rapid solidification (LPBF) stabilizes L1₂.
- **FCC-Al** solid solution — supersaturation of Zr in Al matrix (equilibrium ~0.01 wt% at RT, extended to ~1+ wt% by rapid solidification).

**Key phases for Al-Mn-Cr-Zr:**
- **Al₆Mn** (orthorhombic) — common intermetallic, can be deleterious if coarse.
- **Al₁₂Mn** (icosahedral precursor) — forms at high cooling rates, can refine microstructure.
- **Al₁₃Cr₂** / **Al₄₅Cr₇** — chromium aluminides, dispersoid formers.
- **Al₃Zr (L1₂)** — still the primary strengthening precipitate in quaternary systems.

**Critical difference from Al-Si-Mg:** Al-Zr solidifies via a **peritectic** reaction (L + Al₃Zr → α-Al), not the eutectic reaction that dominates Al-Si. This means:
- Scheil solidification simulations behave differently — peritectic systems tend to have wider freezing ranges and different crack susceptibility patterns.
- The crack susceptibility index (CSI) calculation via Scheil needs to account for peritectic trapping of Zr in the primary phase.
- LPBF rapid solidification can suppress the peritectic reaction, extending Zr solid solubility far beyond equilibrium predictions.

**Screening criteria (in priority order):**
1. **Solidification range** (liquidus – solidus) — narrower is better for crack resistance.
2. **L1₂-Al₃Zr volume fraction** — predicted from equilibrium and Scheil at LPBF-relevant conditions.
3. **Scheil crack susceptibility index** — |dT/d(fs)|max criterion (Kou 2003).
4. **Absence of coarse intermetallics** — Al₆Mn, Al₁₃Cr₂ volume fractions below threshold.
5. **Mineral-burden score** — MB = Σᵢ wᵢ·xᵢ where wᵢ is USGS supply risk weight.

### 2. Database Adequacy Assessment

**TDBDB free TDB coverage:**
- **Al-Zr binary:** Good coverage — multiple assessed TDB files available from Kematick & Franzen (1990), Murray (1992), and others. The Al-Zr phase diagram is well-characterized.
- **Al-Mn binary:** Covered by several assessments including COST507.
- **Al-Cr binary:** Available in TDBDB and COST507.
- **Ternaries (Al-Zr-Mn, Al-Zr-Cr, Al-Mn-Cr):** Limited free coverage. Al-Zr-Mn and Al-Zr-Cr have fewer independent assessments than Al-Si-Mg ternary.
- **Quaternary (Al-Zr-Mn-Cr):** No free TDB covers this system consistently.

**Assessment:** Free TDBs are adequate for **binary screening** and limited ternary exploration (Stage 1 with pycalphad). However, **TCAl10 is essential** for:
- Consistent quaternary Al-Zr-Mn-Cr predictions (free TDBs cannot be combined across papers).
- Reliable Scheil solidification in multicomponent systems.
- Stage 2 refinement of shortlisted compositions.

### 3. Mineral-Burden Objective Formulation

```
MB = Σᵢ wᵢ · xᵢ
```

Where:
- `xᵢ` = mole fraction of element i in the composition
- `wᵢ` = USGS supply risk weight for element i (derived from DOE Critical Minerals List 2023)
  - Mg: wMg = 0.3 (supply-constrained, imported)
  - Sc: wSc = 1.0 (extremely supply-constrained, no domestic production)
  - REE (Ce, La, etc.): wREE = 0.8 (supply-constrained, China-dominated)
  - Zr: wZr = 0.15 (on USGS list but domestic sources exist)
  - Mn: wMn = 0.4 (import-dependent, on critical list)
  - Cr: wCr = 0.2 (less constrained but on critical list)
  - Si, Fe, Cu, Al: wX = 0.0 (abundant, not supply-constrained)

**Multi-objective CALPHAD screening at Node 0:**
```
minimize: MB (mineral burden)
maximize: f_L12 (L1₂-Al₃Zr volume fraction, strength proxy)
minimize: CSI (crack susceptibility index)
subject to: solidification_range < threshold
```

This can be scalarized for pycalphad screening: `score = α·f_L12 − β·CSI − γ·MB` where α, β, γ are adjustable weights. The mineral-burden term is **unique to Topic 3B** and has no competitor equivalent.

### 4. Updated Hybrid Architecture for Critical-Mineral-Lean Discovery

```
Stage 1: pycalphad + TDBDB/COST507 ($0)
  Input: 100K+ compositions in Al-Zr × Al-Mn × Al-Cr × T grid
  Screen: Solidification range, Scheil CSI, mineral-burden score
  Output: Top 1,000 candidates ranked by scalarized multi-objective

Stage 2: TC-Python + TCAl10 (~$8-12K)
  Input: Top 1,000 from Stage 1
  Refine: Full multicomponent Scheil with consistent quaternary interactions
  Compute: L1₂ precipitate fraction, microsegregation, diffusion coefficients
  Output: Top 50-100 candidates with full property predictions

Stage 3: TC AM Module (add-on to Stage 2 license)
  Input: Top 50-100 from Stage 2 + process parameters
  Predict: Printability maps (power vs speed), melt pool geometry, G/R
  Key challenge: Al-Zr absorptivity calibration (peritectic ≠ eutectic)
  Output: Top 10-20 candidates with printability windows
  → Feed into BOFN Node 0.5 (AM Printability)

Stage 4: Experimental validation (BOFN Nodes 1-8)
  → Ultrasonic atomization → LPBF → characterization
  → Bayesian optimization closes the loop
```

### 5. AM Module Considerations for Al-Zr

**Absorptivity:**
- AlSi10Mg baseline calibration remains the recommended starting point.
- Al-Zr alloys may have different absorptivity due to: (1) no eutectic Si phase (different liquid properties), (2) potential ZrO₂ surface oxide formation, (3) higher melting point of Al₃Zr phases affecting melt pool dynamics.
- Treat absorptivity pre-factor as a Bayesian-learnable parameter in BOFN (as recommended in prior analysis).

**Solidification behavior:**
- Peritectic solidification produces different melt pool morphology than eutectic Al-Si.
- AM Module thermal profile predictions remain valid, but G/R interpretation for equiaxed transition needs adjustment for peritectic systems.
- Crack susceptibility in Al-Zr is generally LOWER than Al-Si-Mg (narrow freezing range when Zr < 0.5 wt%), but Al-Mn additions widen it.

**Printability windows:**
- No published LPBF parameter windows for Al-Zr-Mn-Cr compositions exist in literature — this is a STRENGTH for Topic 3B novelty and a GAP that Thermo-Calc AM Module can uniquely address.

### 6. CALPHAD-Specific Risks for Al-Zr/Al-Mn-Cr-Zr

| Risk | Severity | Difference from Al-Si-Mg | Mitigation |
|------|----------|--------------------------|------------|
| **L1₂ vs D0₂₃ prediction** | HIGH | Al-Si-Mg doesn't have this issue; L1₂ is metastable and CALPHAD predicts D0₂₃ at equilibrium | Use Scheil non-equilibrium calcs; validate with TEM/APT |
| **Extended Zr solubility** | MODERATE | LPBF extends Zr solubility 100x beyond equilibrium; CALPHAD equilibrium calcs will underpredict strengthening | Use Scheil + rapid solidification corrections; benchmark against Murray (2023) LPBF data |
| **Al-Zr-Mn ternary database gaps** | MODERATE | Al-Si-Mg ternary is extremely well-assessed; Al-Zr-Mn less so | TCAl10 essential; validate binary endpoints against TDBDB |
| **Absorptivity transfer** | MODERATE | Different oxide characteristics (ZrO₂ vs SiO₂) | Bayesian absorptivity; start with AlSi10Mg baseline |
| **No prior LPBF data for Al-Zr-Mn-Cr** | HIGH (but also opportunity) | AlSi10Mg has extensive LPBF datasets; Al-Zr-Mn-Cr is uncharted | This IS the Topic 3B value proposition — FLAIME discovers what nobody has |

### 7. Thermo-Calc Collaboration Reframing for 3B

**Letter of support should emphasize:**
1. AM Module enables printability prediction for **novel Al-Zr alloys with no published LPBF parameters** — critical for the rapid screening approach in FLAIME.
2. Reciprocal value: BYU provides first systematic Al-Zr-Mn-Cr LPBF melt pool validation data, addressing a gap in TC's aluminum alloy calibration.
3. **AMMTO mission alignment:** Reducing supply chain vulnerability of structural Al alloys by eliminating Mg/Sc/REE dependence — AM Module is the tool that makes this computationally tractable.
4. Advisory support specifically targets the absorptivity calibration challenge for non-eutectic Al alloys.

**AM Module demo request:**
- Ask Adam to run an Al-Zr composition (e.g., Al-0.5Zr wt%) alongside the AlSi10Mg baseline.
- This demonstrates Topic 3B relevance and tests absorptivity model behavior for Zr-containing alloys.

### 8. Competitive Advantage

**Unique CALPHAD+BOFN capabilities for Topic 3B:**
1. **Mineral-burden as optimization objective** — no published HT-CALPHAD screening study includes supply chain risk in the objective function. This is novel and directly addresses AMMTO's critical minerals mission.
2. **Three-stage computational funnel** — competitors (Arróyave/TAMU, CMI Hub) use either open-source only (no printability) or commercial only (limited throughput). FLAIME's hybrid is both cost-effective AND comprehensive.
3. **Cost-aware partial evaluation (p-KGFN)** — BOFN intelligently decides which compositions warrant expensive AM Module calculations vs. cheap pycalphad screening. No competitor has this.
4. **Uncharted territory** — Al-Zr-Mn-Cr for LPBF has no prior systematic exploration. FLAIME would be first to generate this dataset, creating high-impact publications and DOE deliverables.

---

## Edison ANALYSIS Results

*Two Edison ANALYSIS tasks submitted. Results will be appended when available:*

**Task 1 (full, 4 files):** `1e432b28-92b6-4a6f-ba40-817137192f87`
```python
from edison_client import EdisonClient
client = EdisonClient(api_key=os.environ.get("EDISON_API_KEY"))
result = client.get_task(task_id='1e432b28-92b6-4a6f-ba40-817137192f87')
print(result.answer)
```

**Task 2 (focused, 2 files):** `3e2efa30-8a36-4c7d-93ef-2736914d5704`
```python
result = client.get_task(task_id='3e2efa30-8a36-4c7d-93ef-2736914d5704')
print(result.answer)
```
