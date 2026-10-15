
# CALPHAD Screening Strategy Assessment for FLAIME Topic 3B Pivot

## Q1: CALPHAD Screening Criteria — Al-Zr vs Al-Si-Mg

**Fundamental difference: Peritectic vs Eutectic Solidification**

**Al-Si-Mg (baseline AlSi10Mg):** Eutectic system (T_eutectic ≈ 555–577°C). Near-eutectic compositions yield narrow freezing ranges and LOW crack susceptibility. Scheil solidification drives progressive enrichment toward terminal eutectic that heals cracks via backfilling. Screening criteria: maximize eutectic fraction, minimize freezing range. Mg₂Si is the primary strengthening phase with well-characterized β″/β′ precipitation.

**Al-Zr (primary target):** Peritectic system (T_peritectic ≈ 661°C, equilibrium Zr solubility ~0.28 wt%). The key strengthening phase is metastable L1₂ Al₃Zr (coherent, 5–20 nm nanoprecipitates), which forms either as a PRIMARY phase from the melt in hyperperitectic compositions or as SECONDARY nanoprecipitates during LPBF intrinsic heat treatment (~300–400°C reheating window). D0₂₃ Al₃Zr is the equilibrium (incoherent) phase that forms above ~580–600°C on prolonged aging — modeling the L1₂→D0₂₃ transition is essential for thermal stability predictions. LPBF enables solute trapping of ~1.0–1.5 wt% Zr in α-Al (literature: Griffiths measured ~1.5 wt% Zr retained in columnar α-Al; Mehta reports metastable peritectic shifts to ~0.5 wt% Zr when D0₂₃ is suppressed). Scheil implications are fundamentally different: peritectic solidification depletes Zr from liquid (opposite of eutectic enrichment), providing NO terminal eutectic healing mechanism and a wider crack-vulnerable window at fs = 0.9–0.99.

**Al-Mn-Cr-Zr (quaternary target) key phases:**
- L1₂ Al₃Zr: primary strengthening (must remain stable)
- Al₆Mn: equilibrium intermetallic, peritectic formation ~710°C
- Al₁₃Cr₂ (Al₇Cr): monoclinic, peritectic formation ~661°C
- Metastable Al₁₂Mn: stabilized by Cr, suppressed by Fe/Si
- α-Al(Mn,Cr)Si dispersoids: if Si present as impurity

**New screening criteria for 3B (replacing Al-Si-Mg criteria):**
1. L1₂ Al₃Zr volume fraction at service temperature (target >1 vol%)
2. L1₂ solvus temperature exceeding service T by adequate margin
3. Scheil freezing range with D0₂₃ SUSPENDED (peritectic-aware, non-standard calculation)
4. Crack susceptibility via |dT/d(fs^0.5)| at fs = 0.9–0.99 (Kou criterion)
5. Coarse primary intermetallic avoidance (Al₆Mn, Al₁₃Cr₂ fraction < threshold)
6. Mineral-burden score (new 3B-specific objective)

---

## Q2: Database Adequacy — TDBDB Free TDB vs TCAl10

**TDBDB coverage analysis (from actual database queries):**

| System | Free TDBs | Ternary Params? | Adequate? |
|--------|-----------|-----------------|-----------|
| Al-Zr binary | 1 dedicated (Wang 2001) + COST507 | N/A | PARTIAL* |
| Al-Mn binary | Multiple (Lindahl 2015, Zheng 2018) | N/A | YES (binary only) |
| Al-Cr binary | 1 dedicated (Wang 2011) + COST507 | N/A | YES (binary only) |
| Al-Mn-Zr ternary | COST507 only | NO — zero ternary parameters | NO |
| Al-Cr-Zr ternary | COST507 only | NO — zero ternary parameters | NO |
| Al-Mn-Cr ternary | COST507 only | NO — zero ternary parameters | NO |
| Al-Mn-Cr-Zr quaternary | COST507 only | NO | NO |
| Al-Mg-Si ternary | 3+ dedicated TDBs | YES | YES |

**COST 507 critical limitations verified from the actual TDB file:**
1. AL3ZR modeled as STOICHIOMETRIC line compound (2 sublattices: AL:ZR, 3:1) — cannot model L1₂ ordering or composition-dependent solvus
2. FCC_L12 phase ENTIRELY COMMENTED OUT (all lines prefixed with $) — no L1₂ precipitation modeling possible
3. D0₂₃ structure COMPLETELY ABSENT (zero mentions in 304 KB file) — cannot compute L1₂↔D0₂₃ phase boundary
4. AL3M_D022 constituents are AL,MO,TI,V : CR,MO,NB,TA,TI,V — Zr NOT included
5. Zero ternary interaction parameters for Al-Mn-Zr, Al-Cr-Zr, or Al-Mn-Cr

**VERDICT: TCAl10 is ESSENTIAL, not optional.** Free TDBs cannot model the L1₂ Al₃Zr precipitation that is the entire basis for Al-Zr strengthening in AM. This represents a STRONGER justification for the TCAl10 license than existed for Al-Si-Mg work, where COST507 + Povoden-Karadeniz 2013 TDB provided adequate ternary coverage. COST 507 remains useful only for binary sanity checks in pycalphad Stage 1 screening.

---

## Q3: Mineral-Burden Objective Formulation

**MB = Σ(wᵢ × xᵢ)** where wᵢ = USGS Net Import Reliance (NIR) as supply risk weight, xᵢ = weight fraction.

**USGS MCS 2024 data (retrieved from ScienceBase):**

| Element | NIR (2023) | On 2022 CML | On 2025 CML | Proposed wᵢ |
|---------|-----------|-------------|-------------|-------------|
| Sc | 100% | YES | YES | 1.00 |
| Mn | 100% | YES | YES | 1.00 |
| Y | 100% | YES | YES | 1.00 |
| REE (Ce,La,Nd) | >95% | YES | YES | 0.95 |
| Cr | 74% | YES | YES | 0.74 |
| Mg (metal) | >50% | YES | YES | 0.55 |
| Si | >50% | NO→YES(2025) | YES | 0.50 |
| Al | 44% | YES | YES | 0.44 |
| Zr | <25% | YES | YES | 0.25 |

**Critical insight:** Zr has the LOWEST import reliance (<25%) among all candidate alloying elements, making Al-Zr the most supply-secure binary. However, Mn (100% NIR) and Cr (74% NIR) in the quaternary system are high-risk — mineral-burden optimization must minimize Mn+Cr content while maintaining dispersoid strengthening.

**Integration into CALPHAD screening:**
1. Compute MB for each candidate composition (trivial, O(1) per composition)
2. Multi-objective BOFN: minimize MB alongside maximize strength, minimize crack susceptibility
3. Pareto front identifies performance-to-burden tradeoffs systematically
4. 3B framing: "Substituting Sc (w=1.0) + Mg (w=0.55) with Zr (w=0.25) achieves 3–4× reduction in mineral burden per unit strengthening element"
5. Constraint: MB_new < MB_baseline (AlSi10Mg reference)

**Proposal formula:**
- MB_alloy = 0.25·x_Zr + 1.00·x_Mn + 0.74·x_Cr + 0.44·x_Al
- MB_baseline = 0.55·x_Mg + 0.50·x_Si + 0.44·x_Al (for AlSi10Mg)
- ΔMB = MB_baseline − MB_alloy (positive = improvement)

---

## Q4: Updated Three-Stage Funnel for Critical-Mineral-Lean Alloy Discovery

**Stage 1: CALPHAD Coarse Screen (pycalphad + COST507, $0)**
- Input: 100,000+ Al-Zr-Mn-Cr compositions on grid
- Criteria: (a) Stoichiometric AL3ZR phase fraction > 0 at 300–400°C (proxy for L1₂); (b) Scheil freezing range < threshold; (c) No coarse primary Al₆Mn or Al₁₃Cr₂ > 5 vol% in Scheil; (d) Mineral-burden MB < threshold; (e) Liquidus < 800°C
- Output: ~1,000–5,000 candidates
- Limitation: Cannot resolve L1₂ vs D0₂₃; binary-only interactions

**Stage 2: CALPHAD Refined Screen (TC-Python + TCAl10, ~$10K)**
- Input: Top 1,000 from Stage 1
- Criteria: (a) L1₂ solvus > service T + margin; (b) D0₂₃-suspended Scheil for metastable solidification path; (c) Ternary/quaternary interaction effects; (d) Kou crack susceptibility index from Scheil; (e) Equilibrium phase fraction maps (200–600°C); (f) Driving force for L1₂ precipitation from supersaturated α-Al
- Output: Top 50–100 candidates

**Stage 3: AM Printability Screen (TC AM Module)**
- Input: Top 50–100 from Stage 2
- Criteria: (a) Process maps with lack-of-fusion & keyhole boundaries; (b) Melt pool depth > layer thickness; (c) G/R solidification conditions for equiaxed transition; (d) Absorptivity with oxide-film pre-factor; (e) Thermal profiles for intrinsic heat treatment estimation
- Output: 3–5 candidates for experimental validation (PR #44 target)

**3B-specific additions vs original 12F funnel:** Mineral-burden score at EVERY stage; D0₂₃ suspension in Stage 2 Scheil (new for peritectic systems); L1₂ solvus as explicit criterion (replaces β″ solvus); peritectic solidification path analysis (replaces eutectic healing assessment).

---

## Q5: AM Module Risk Factors for Al-Zr

**Risk 1 — Absorptivity Model (HIGH):** AM Module calculates absorptivity from liquid electrical resistivity, which works for steels/Ni but fails for Al due to Al₂O₃ oxide film. Al-Zr may have different oxide behavior: ZrO₂ has higher thermodynamic stability than Al₂O₃, mixed oxide layers are possible, and the pre-factor calibrated on AlSi10Mg may not transfer. Mitigation: Bayesian learnable absorptivity parameter in BOFN; calibrate AlSi10Mg first, then re-calibrate with Al-Zr.

**Risk 2 — Peritectic Solidification (HIGH):** AM Module process maps assume eutectic-type solidification. Peritectic path: Zr depletes from liquid, no terminal eutectic backfilling, wider crack-vulnerable window. Primary Al₃Zr particles can nucleate equiaxed grains (beneficial) but may affect powder spreading if coarse. Mitigation: validate against Al-Zr single-track cross-sections.

**Risk 3 — Oxide Layer on Powder (MODERATE-HIGH):** Zr is highly reactive; ZrO₂ on powder surface affects flowability, laser absorption, and creates oxide inclusions. Higher stability than Al₂O₃ → harder to break during melting. Mitigation: characterize powder oxide layer.

**Risk 4 — Low Zr Solubility Limit (MODERATE):** Equilibrium 0.28 wt% extended to ~1.0–1.5 wt% by LPBF solute trapping. AM Module steady-state thermal model may not capture velocity-dependent partitioning. Mitigation: extract thermal profiles from AM Module, apply separate partitioning model.

**Risk 5 — Narrow Process Window (MODERATE):** Peritectic alloys have narrower printability windows; no extensive LPBF literature for Al-Zr vs thousands of AlSi10Mg studies. Mitigation: frame as opportunity — BYU provides FIRST Al-Zr AM Module validation data.

---

## Q6: Thermo-Calc Letter of Support Reframing for 3B

The letter must shift from "TC enables AI-driven alloy design for AM" (12F framing) to critical minerals mission alignment:

1. **Mission alignment:** "TC's CALPHAD capabilities enable discovery of critical-mineral-lean aluminum alloys, directly supporting DOE AMMTO's mission to reduce dependence on Sc, Mg, and REE imports"
2. **Supply chain security:** "TCAl10 is the ONLY tool capable of modeling L1₂ Al₃Zr precipitation enabling Sc/REE-free strengthening — no open-source alternative exists for this specific phase" (verified: COST507 has L1₂ commented out, D0₂₃ absent)
3. **Reciprocal value (strengthened):** "BYU provides TC with first systematic LPBF validation data for Al-Zr peritectic alloys — a system with NO existing AM Module calibration data, addressing a critical gap with broader DOE relevance"
4. **Mineral-burden quantification:** "CALPHAD screening integrated with mineral-burden scoring enables systematic alloy identification meeting performance AND supply risk targets"
5. **Five AM Module outputs + peritectic solidification path** as sixth 3B-specific capability
6. **Policy relevance:** Direct DOE CMS 5-Pillar alignment (Pillars 2/3/5)

Letter commitments unchanged: advisory hours, student training, sample calculations, reciprocal data exchange, publication support.

---

## Q7: Competitive Advantage of CALPHAD+BOFN for Topic 3B

1. **Unique multi-objective capability:** No other group combines CALPHAD + Bayesian optimization + mineral-burden scoring in a single closed-loop framework. BOFN's cost-aware p-KGFN naturally handles three competing objectives (performance, printability, mineral burden).
2. **Zero-cost mineral-burden tagging:** Each of 100K+ screened compositions tagged with MB score at zero additional computational cost — trivial for CALPHAD, impossible without it.
3. **Peritectic system expertise as differentiator:** Most competing Al AM groups work in Al-Si eutectic space (mature). Al-Zr peritectic is underexplored, requires more sophisticated CALPHAD (L1₂ modeling), and presents a higher barrier to entry.
4. **Closed-loop feedback:** Each BOFN iteration simultaneously improves alloy understanding, process understanding, AND mineral-burden optimization. The 88% cost savings from BOFN pre-screening is amplified by 3B framing: fewer experiments = less material = less critical mineral consumption.
5. **Open-source scalability:** pycalphad Stage 1 is $0 and HPC-parallelizable; commercial TC used only where essential — demonstrates responsible DOE fund usage.
6. **Reciprocal TC data value:** First Al-Zr AM Module validation → unique academic partnership positioning.

---

## Q8: CALPHAD-Specific Risks — Al-Zr vs Al-Si-Mg

| Risk | Al-Si-Mg | Al-Zr | Severity Change |
|------|----------|-------|----------------|
| Database coverage (free TDB) | GOOD (3+ ternary TDBs) | POOR (no L1₂, no D0₂₃, no ternary params) | ↑↑ MUCH HIGHER |
| L1₂ ordering model needed | NO | YES (essential) | NEW RISK |
| D0₂₃ phase boundary needed | NO | YES (essential) | NEW RISK |
| Ternary interaction parameters | Available in COST507 | ABSENT in all free TDBs | ↑↑ MUCH HIGHER |
| Metastable phase suppression | Minor | CRITICAL (must suspend D0₂₃) | ↑↑ MUCH HIGHER |
| Scheil solidification mode | Eutectic (backfilling) | Peritectic (no healing) | FUNDAMENTALLY DIFFERENT |
| Crack susceptibility model validity | Validated for eutectic Al | Unvalidated for peritectic | ↑ HIGHER |
| Solute trapping modeling | Minor effect | CRITICAL (0.28→1.5 wt% Zr) | ↑↑ MUCH HIGHER |
| Equilibrium solubility limit | ~1.65 wt% Si | ~0.28 wt% Zr | ↑ HIGHER (much narrower) |
| AM Module calibration data | Extensive (AlSi10Mg) | NONE for Al-Zr | ↑↑ MUCH HIGHER |

**Key new risks:**
1. L1₂/D0₂₃ boundary accuracy in TCAl10 determines validity of ALL downstream predictions
2. Non-standard Scheil with phase suspension required (TC-Python specific commands)
3. TCAl10 quality for Al-Mn-Zr, Al-Cr-Zr ternary interactions is unknown — may be extrapolated
4. Kou crack criterion developed for eutectic Al may over/under-predict for peritectic
5. Mn (NIR=100%) content in quaternary may partially offset mineral-burden gains — Pareto analysis essential

---

## Discretionary Analytical Decisions

- **Used USGS Net Import Reliance (NIR) as the supply risk weight wᵢ** in the mineral-burden formula rather than alternative criticality metrics (e.g., Graedel multi-dimensional criticality, HHI concentration index, or Ferro's CIA). NIR was chosen for simplicity, direct policy relevance to DOE/AMMTO, and availability from MCS 2024 data. Alternative multi-dimensional scores (supply risk × vulnerability × environmental impact) would produce different element rankings.

- **Set wᵢ values as direct NIR percentages normalized to [0,1]** (e.g., Mn at 100% NIR → wᵢ = 1.00, Zr at <25% NIR → wᵢ = 0.25). An alternative would be to use nonlinear transformations (e.g., logistic scaling) or categorical risk tiers.

- **Used stoichiometric AL3ZR phase fraction as a proxy for L1₂ screening** in Stage 1 (pycalphad + COST507). This is the best available approximation given that COST507 lacks L1₂ ordering, but it will overestimate AL3ZR stability and miss composition-dependent solvus effects. An alternative would be to skip Stage 1 entirely and begin all screening at Stage 2 with TCAl10.

- **Set 5 vol% as the threshold for coarse primary intermetallic avoidance** (Al₆Mn, Al₁₃Cr₂) in Stage 1 screening. This is a judgment call; literature values for acceptable intermetallic fractions in AM vary from 2–10%.

- **Classified absorptivity transfer risk as HIGH rather than MODERATE** based on the reasoning that ZrO₂ has different thermodynamic stability than Al₂O₃ and mixed oxide behavior is uncertain. Some researchers might rate this as moderate given that the pre-factor approach is inherently empirical.

- **Chose Kou criterion |dT/d(fs^0.5)| as the primary crack susceptibility metric** rather than alternatives (Clyne-Davies, RDG model, or Rappaz-Drezet-Gremaud). Kou criterion was selected for consistency with the prior Edison analysis and because it is directly computable from Scheil curves, but it was developed primarily for eutectic Al systems.

- **Used 2024 MCS data rather than 2025 MCS** for NIR values because 2024 was the most recent complete dataset retrieved. The 2025 critical minerals list (60 minerals, adding Si) was referenced for list membership but NIR values may differ slightly.

- **Treated Cu-Cr-Zr as a 20% complement** and did not develop a parallel three-stage funnel for it, consistent with the context document's scope allocation (~80% Phase I for Al systems). A more detailed analysis could develop Cu-Cr-Zr-specific CALPHAD screening criteria.
