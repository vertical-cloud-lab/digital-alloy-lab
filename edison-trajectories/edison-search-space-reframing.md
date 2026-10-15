
# FLAIME Search Space Reframing Assessment
## DOE Genesis Mission Phase I — AI-Enabled Al Alloy Discovery ($750K, 9 months)

---

## Overall Assessment

**Current proposal grade: B** — The narrow Al-Mn-Cr-Zr + Al-Zr framing is experimentally feasible but looks incremental for a Genesis Mission proposal. The mineral-burden KPI is trivially satisfied, and the AI platform's discovery power is underutilized.

**Proposed reframing grade: A-** — A 15-element palette with hierarchical CALPHAD→experimental screening is ambitious yet computationally feasible, creates genuine supply-risk tradeoffs, and represents a novel contribution (NChooseK element selection via BO + mineral burden).

---

## 1. CALPHAD Database Coverage (TCAl10)

**TCAl10 statistics** (from official Thermo-Calc technical documentation, 76-page PDF, June 2025):
- 48 elements, 313 assessed binaries, 123 assessed ternaries, 14 assessed quaternaries, 725 phases
- Thermophysical properties: molar volume, electrical resistivity, thermal conductivity, viscosity, surface tension
- Compatible with AM Module (printability maps, melt pool simulation)

**Coverage tiers for candidate palette elements** (ranked by assessed Al-X-Y ternary count):

| Tier | Elements | Al-X-Y Ternaries | Reliability |
|------|----------|-------------------|-------------|
| Tier 1 (Excellent, ≥6) | Mg(18), Si(17), Cu(15), Ti(11), Zn(10), Sn(9), Fe(9), Ni(8), Mn(8), Ce(7), Li(6), Cr(6), Sc(6) | 6–18 | High for multicomponent |
| Tier 2 (Good, 4–5) | Zr(5), Y(4) | 4–5 | Good, some extrapolation |
| Tier 3 (Moderate, 2–3) | Er(3), B(3), Nb(2) | 2–3 | Moderate uncertainty |
| Tier 4 (Weak, 0–1) | V(1), W(1), Mo(1), Ag(1), Hf(0), Be(0), Co(0) | 0–1 | Binary extrapolation only |

**CRITICAL FINDING for current target system:** Al-Mn-Cr-Zr has **0 of 4 constituent ternaries assessed** in TCAl10. Neither Al-Mn-Cr, Al-Mn-Zr, Al-Cr-Zr, nor Cr-Mn-Zr are in the assessed ternary list. All predictions rely entirely on binary Muggianu extrapolation. This is standard CALPHAD practice and acceptable for dilute Al-rich compositions (Al ≥ 85 at.%), but represents a non-trivial uncertainty that the proposal should acknowledge.

**Realistic palette size:** 15 elements is the sweet spot. At this size:
- 53.3% of element pairs (56/105) have assessed Al-X-Y ternaries
- 93 of 455 quaternary sub-systems (20.4%) have 3/4 constituent ternaries assessed (the maximum achievable — 0 systems achieve 4/4)
- Computationally feasible: C(15,4)=1,365 sub-systems × 100 compositions = 136,500 CALPHAD evaluations (hours on HPC)
- Beyond 20 elements, the fraction of well-covered ternary pairs drops rapidly, and Tier 4 elements (Hf, Be, Co) add no ternary coverage

---

## 2. Hierarchical Search Strategy

**Feasibility: YES.** A two-level approach is computationally natural and well-precedented:

**Level 1 — Element Combination Selection (CALPHAD + BOFN):**
- Screen C(15,4) = 1,365 quaternary sub-systems from 15-element palette
- ~20–100 representative Al-rich compositions per system
- Criteria: Scheil solidification range, precipitate fraction (L1₂, θ′, β″), cracking susceptibility index, mineral-burden score
- BOFN acquisition function selects which sub-systems to explore further
- Output: Top ~20–50 most promising sub-systems

**Level 2 — Composition Optimization:**
- Fine-grained composition optimization within selected sub-systems
- TC-Python + TCAl10 for high-fidelity predictions
- AM Module for printability maps
- BOFN/pKGFN drives experimental composition selection

**Published precedents:**
- Vazquez et al. 2023 (npj Comput. Mater.): 500K TC-Python → DNN → screen billions (hierarchical approach)
- Wang et al. 2025 (npj Comput. Mater.): 150K → ML → 2 billion compositions (most extreme published)
- Sundar et al. 2025 (J. Mater. Res.): CALPHAD-based BO, explored only 7% of space
- Sheikh & Arroyave 2025: HT HEA printability screening with TC AM Module
- Ghassemali & Conway 2022 (Front. Mater.): Established "islands of interest" coarse-to-fine paradigm

**Novel contribution:** No published study combines NChooseK element COMBINATION selection via Bayesian optimization from a broad palette (>10 elements) with a mineral-burden multi-objective. This would be the first.

---

## 3. DOE Reviewer Perception

**Sweet spot framing: "Computationally broad, experimentally focused"**

The optimal positioning is:
- **Too narrow** (current): "Just optimizing within Al-Mn-Cr-Zr" — looks incremental, doesn't justify the AI platform's cost, mineral-burden KPI is trivially satisfied
- **Too broad** (C(25,8) = 1M+ sub-systems): Appears infeasible for 9 months, no experimental grounding
- **Just right** (C(15,4) = 1,365 sub-systems): Ambitious but bounded, computationally trivial (hours of CALPHAD), converges to focused experimental validation

**Recommended language:**
> "FLAIME screens 1,365 quaternary sub-systems drawn from a 15-element Al-alloy palette via CALPHAD-guided BOFN element selection, then focuses experimental validation on the top 3–5 sub-systems — including the Al-Mn-Cr-Zr anchor — screening ≥200 compositions through the full powder-to-tensile pipeline."

**Key risk mitigation for reviewers:**
- Al-Mn-Cr-Zr and Al-Zr remain as guaranteed ANCHOR systems that receive experimental validation regardless of Level 1 results
- CALPHAD screening is computationally cheap (~$1/eval vs. $500/experimental composition) — the broad screen costs almost nothing
- Phase I deliverables remain concrete: ≥200 experimental compositions, ≥3% discovery yield

---

## 4. Computational Feasibility

| Configuration | Key Scenario: C(15,4) × 100 = 136,500 evals |
|---|---|
| pycalphad, 1 core (~10 calcs/sec) | ~3.8 hours |
| pycalphad, 16 cores (1 HPC node) | ~14 minutes |
| pycalphad, 160 cores (10 nodes) | ~1.4 minutes |
| TC-Python batch, 1 session (~5 calcs/sec) | ~7.6 hours |
| TC-Python, 20 SLURM jobs | ~23 minutes |
| ML surrogate (after training) | <1 minute |

**Comparison to published campaigns:** Wang & Xiong (2020) screened 450,000 compositions; Vazquez et al. (2023) screened 500,000+; Wang et al. (2025) trained on 150,000 for 2B surrogate inference. The FLAIME 136,500-point screen is moderate by published standards and trivially feasible on any university HPC cluster.

**Key constraint:** TC-Python is capped at 32 logical processors per license (Kwon et al. 2024). For the coarse Level 1 screen, use free pycalphad with COST507/TDBDB databases (no license limit). Reserve TC-Python + TCAl10 for Level 2 refinement of top ~1,000 candidates.

---

## 5. The "Trivial Satisfaction" Problem

**This is a real and significant problem with the current framing.**

**Narrow palette (Al-Mn-Cr-Zr):**
- Import reliance: Mn=100%, Cr=77%, Zr=25%
- Mean: 67.3%, Standard deviation: 31.4%
- ALL three non-Al elements are medium-to-high criticality
- The mineral-burden score MBS = Σᵢ wᵢ·xᵢ is essentially a proxy for total solute content, NOT a supply-risk tradeoff
- Any composition with less total alloying content automatically has lower MBS — there's no genuine multi-objective tension

**Broad palette (15 elements):**
- Import reliance spans 0% (Fe) to 100% (Mn, Sc)
- Mean: 61.9%, Standard deviation: 28.1%, but critically the **range** is 0–100%
- Creates genuine Pareto tradeoffs: Can you replace Sc (100%) with Zr (25%) while maintaining properties? Can Fe (0%) and Si (30%) contribute structural function to offset Mn (100%)?
- The optimizer faces a real multi-objective problem that requires AI to solve

**Specific examples of meaningful tradeoffs enabled:**
- Scalmalloy (Al-4.5Mg-0.7Sc-0.3Zr): MBS ≈ 82 (Mg=75%, Sc=100%, Zr=25%)
- Al-Mn-Cr-Zr candidate: MBS ≈ 85-90 (high criticality across all elements)
- Al-Fe-Si-Zr candidate: MBS ≈ 12 (Fe=0%, Si=30%, Zr=25%) — 85% reduction IF properties compete
- The broad palette makes the 40% MBS reduction target DEFENSIBLE as a genuine achievement

---

## 6. Recommended Element Palette (15 Elements)

**Selection criteria:** (1) ≥4 assessed Al-X-Y ternaries in TCAl10, (2) demonstrated AM/LPBF relevance in published literature, (3) supply-risk variance spanning 0–100% USGS import reliance.

| Category | Elements | Rationale |
|---|---|---|
| **Core (6)** | Mn, Cr, Zr, Mg, Si, Cu | Current FLAIME targets + essential AM alloy families (3xxx–7xxx) |
| **Expanded Core (5)** | Ti, Fe, Ni, Ce, Sc | High AM relevance, good TCAl10 coverage, supply-risk diversity; Ce = CMI alloy precedent; Sc = benchmark to beat |
| **Exploratory (4)** | Li, Er, Zn, Sn | Moderate coverage, some AM relevance; Li = aerospace; Er = Sc substitute candidate; Zn = 7xxx; Sn = grain boundary engineering |

**Excluded elements and reasons:**
- Hf, Be, Co: 0 assessed Al-X-Y ternaries — predictions would be binary-extrapolated only
- V, W, Mo, Ag: Only 1 assessed ternary each — insufficient for reliable multicomponent screening
- Y: Included if palette expanded to 16 (4 ternaries, 100% import reliance), but marginal
- B: Primarily a grain refiner additive at trace levels (<0.05 at.%), not a compositional design variable
- Nb: Only 2 ternaries, 100% import reliance, limited Al-alloy relevance

**Palette statistics:**
- C(15,4) = 1,365 quaternary sub-systems
- C(15,5) = 3,003 quinary sub-systems  
- 56/105 element pairs (53.3%) have assessed Al-X-Y ternaries
- 93/455 quaternary sub-systems (20.4%) have 3/4 constituent ternaries assessed (best achievable)

---

## Specific Language Recommendations

**Abstract (key sentence replacement):**
> BEFORE: "Phase I targets the Al–Mn–Cr–Zr and Al–Zr alloy families, screening ≥200 compositions..."
> AFTER: "Phase I screens 1,365 quaternary sub-systems drawn from a 15-element Al-alloy palette via CALPHAD-guided BOFN element selection, then focuses experimental validation on the top 3–5 sub-systems — including the Al–Mn–Cr–Zr anchor — screening ≥200 compositions through the full powder-to-tensile pipeline."

**Activity 1 (Methods, ~80 words to replace current text):**
> "FLAIME operates at two hierarchical levels. At Level 1, BOFN+pKGFN screens element COMBINATIONS: C(15,4)=1,365 quaternary sub-systems from a 15-element palette are evaluated via batch CALPHAD (Scheil solidification, precipitate fraction, cracking susceptibility) with a mineral-burden filter — a novel NChooseK-style search over alloy families. At Level 2, pKGFN optimizes COMPOSITIONS within selected sub-systems. Al–Mn–Cr–Zr and Al–Zr are guaranteed anchor systems."

**Mineral-Burden KPI (Decision Gates, ~50 words):**
> "MBS = Σᵢ wᵢ·xᵢ where wᵢ is the USGS import-reliance weight (0–100%) for element i. By searching across elements spanning 0% (Fe) to 100% (Mn, Sc) import reliance, BOFN navigates a genuine strength-vs-supply-risk Pareto front. Target: MBS ≥40% below Scalmalloy while meeting mechanical thresholds."

---

## Discretionary Analytical Decisions

- **Ternary coverage threshold for tier classification:** Set at ≥4 for Tier 2 (Good) and ≥6 for Tier 1 (Excellent). These thresholds are judgment calls — a threshold of 3 or 5 would change the tier assignments for several elements (Y, Er, Zr). Chose ≥4 because it indicates at least 4 independent ternary interactions have been assessed, providing reasonable multicomponent extrapolation confidence.

- **Palette size recommendation of 15 elements:** Multiple valid sizes exist (12–18 are all defensible). Chose 15 as the intersection of: (a) keeping >50% assessed ternary pair coverage, (b) including all elements from industrial Al alloy series 1xxx–8xxx, (c) maintaining computational feasibility for quaternary screening within hours on HPC. A 12-element palette would have better coverage (~60%) but exclude potentially important elements (Li, Er); an 18-element palette would drop coverage below 45%.

- **Use of USGS import reliance percentage as supply-risk weight:** Alternative metrics exist (OECD supply risk index, Helbig et al. 2020 alloy-level supply risk, European Commission criticality assessment). Chose USGS import reliance because: (a) directly quantitative, (b) U.S.-specific (relevant for DOE proposal), (c) publicly available from MCS 2025, (d) simple to explain to non-specialist reviewers. Helbig SRI weights would be more nuanced but harder to justify and source.

- **100 compositions per quaternary sub-system estimate:** This is a rough estimate for Al-rich (≥85 at.%) composition sampling. Actual counts depend on grid resolution and simplex constraint handling. Could range from ~20 (very coarse, 3 levels per minor element) to ~500 (fine grid). Used 100 as a moderate estimate for computational cost projections.

- **Excluded Sn from "Expanded Core" and placed in "Exploratory":** Despite having 9 assessed ternaries (high coverage), Sn has limited AM/LPBF relevance in structural Al alloys. It is primarily used in bearing and free-machining alloys. A different analyst might include it in Expanded Core based on database coverage alone.

- **Treatment of Er as "Exploratory" rather than "Expanded Core":** Er has only 3 assessed ternaries (moderate coverage) but is a promising Sc-substitute forming L1₂-Al₃Er precipitates. Its classification is borderline — strong metallurgical motivation but modest database support. A more optimistic analyst could elevate it.

- **Assessment that the Al-Mn-Cr-Zr ternary coverage gap is "not a showstopper":** This is a judgment call. For Al ≥ 85 at.%, minor element interactions (Mn-Cr, Mn-Zr, Cr-Zr) are all dilute (<5 at.% each), and the Muggianu binary extrapolation is generally adequate in this regime. However, ternary intermetallics or unexpected phase stabilities could be missed. The proposal should acknowledge this limitation.

- **Grading the current proposal as "B" and proposed reframing as "A-":** Grades are subjective assessments based on the analysis of six specific criteria. Different reviewers might weight criteria differently — e.g., if experimental feasibility is weighted most heavily, the narrow framing scores better.
