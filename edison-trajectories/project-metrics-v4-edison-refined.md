# FLAIME Phase I — Project Metrics (v4: Topic 3B Edison Scientific Refinement)

*This document presents the FLAIME metrics framework for DOE Genesis Mission Phase I (DE-FOA-0003612, Topic 3B: "AI-Enabled Materials Discovery and Engineering — Reducing Demand for Critical Minerals"). Built on v3-final (2 prior Edison rounds), it incorporates 14 Edison Scientific iterations: 8 with mock program manager and panel reviewer feedback (culminating in a Topic 3B-specific reassessment), plus 6 individual KPI deep-dive reviews and 1 holistic cross-KPI synthesis (Iterations 9-15).*

*Material strategy: Al-Zr and Al-Mn-Cr-Zr families PRIMARY (~80% Phase I effort, reducing dependence on supply-constrained Sc/Mg/REE/Be), Cu-Cr-Zr COMPLEMENT (~20% stretch, replacing Be-Cu). AlSi10Mg is LPBF process baseline; Scalmalloy (Al-Mg-Sc-Zr) is primary supply-risk comparator.*

*Note on Zr/Mn/Cr criticality: Zr, Mn, and Cr appear on the USGS 2022 Critical Minerals List. However, FLAIME's net supply-risk reduction is substantial because: (a) Zr, Mn, Cr have moderate supply risk (Helbig SRI ~0.3-0.5) vs. very high risk for Sc (~0.9), Be (~0.8), and REEs (~0.7-0.9); (b) the mass fractions of Zr (~0.1-0.5 wt%), Mn (~5 wt%), and Cr (~0.8 wt%) result in lower composition-weighted criticality than Sc-containing incumbents like Scalmalloy; (c) Mn and Cr have diversified global supply chains and established domestic recycling pathways, unlike Sc. The proposal frames this as "reducing dependence on the most supply-constrained critical minerals" rather than absolute mineral avoidance.*

---

## Evolution Summary

| Version | Edison Task | Focus | Key Changes |
|---|---|---|---|
| v1 | — | Initial brainstorm | 6 categories, ~30 metrics |
| v2 | `eb08ff46` | LITERATURE_HIGH #1 | Throughput reduced 2×, tiered framework, 25+ new metrics |
| v3-final | `e5f1a050` | LITERATURE_HIGH #2 | Discovery Yield headline, LPBF batching, sustainability formulas |
| **v4 iter 1** | `61255bd4` | Comprehensive brainstorm + mock PM | Proposal-ready KPI table, autonomy rubric L0-L5, acceleration factor, digital thread |
| **v4 iter 2** | `6c16c2ee` | 3-reviewer panel critique | Pre-registered benchmark, LPBF process quality as headline, MRL/AMRL gates |
| **v4 iter 3** | `2bc2cf14` | Go/no-go framework | 8 mandatory gates, 0-100 scoring rubric, early warning indicators |
| **v4 iter 4** | `488f6697` | Skeptical PM stress test | Literature defensibility audit, statistical rigor concerns |
| **v4 iter 5** | `cce2900d` | AI advantage demonstration | 4-baseline design, pre-registration protocol, time-ledger methodology |
| **v4 iter 6** | `92f0a824` | Funded program comparison | Cross-program gap analysis vs ULTIMATE, DuAlumin-3D, TCR, DMREF, DARPA DSO |
| **v4 iter 7** | `f9d8415e` | Final proposal-ready synthesis | Concise 5 KPIs, 6 go/no-go gates, pre-registered benchmark protocol, 9-month timeline |
| **v4 iter 8** | `9763811e` | **Topic 3B reassessment** | Revised KPIs for critical minerals, mineral-burden BOFN gate, Al-Zr/Al-Mn-Cr-Zr targets, supply-risk metrics |
| **v4 iter 9** | `aec55322` | KPI 1 deep-dive: Discovery Yield | Family-specific thresholds, multi-tier classification, ≥20% base target, supply-risk-reduced framing |
| **v4 iter 10** | `553ca7e3` | KPI 2 deep-dive: CMDRI | Scalmalloy comparator, Helbig+Ferro hybrid, element-level decomposition |
| **v4 iter 11** | `a3ae145c` | KPI 3 deep-dive: AI Acceleration Factor | 5th baseline (BOFN−mineral), win rate reporting, power analysis |
| **v4 iter 12** | `26900c82` | KPI 4 deep-dive: Throughput | Tiered throughput, phased ramp-up, pipeline efficiency metric |
| **v4 iter 13** | `6b28cf12` | KPI 5 deep-dive: Mineral-Burden Efficacy | Broader search space baseline, explicit MOBO, conflict pre-check |
| **v4 iter 14** | `6790f2f0` | KPI 6 deep-dive: Digital Thread | Formal provenance schema, FAIR sub-metrics, supply-risk metadata |
| **v4 iter 15** | `590666ce` | Holistic cross-KPI synthesis | Cross-KPI consistency, top 10 recommendations, Zr/Mn/Cr framing |

---

## Tiered Framework

- **Base** (≥90% confidence): Minimum acceptable for DOE go/no-go
- **Expected** (moderate confidence): Target performance
- **Stretch** (aspirational): Exceptional outcomes

---

## 6 Headline KPIs (Topic 3B — Proposal-Ready)

The headline KPIs foreground critical-mineral demand reduction alongside autonomous discovery. Three original KPIs survive with modification (Discovery Yield, AI Acceleration Factor, Throughput), one survives as-is (Digital Thread Completeness), one is retired (Autonomy Level, folded into go/no-go gates), and two new KPIs are introduced (Critical Mineral Demand Reduction Index, Mineral-Burden Optimization Efficacy). Iterations 9-14 refined each KPI with literature-grounded deep-dives.

| # | KPI | Phase I Baseline | Phase I Target (9 mo) | Phase II Target | Measurement |
|:---:|---|---|---|---|---|
| 1 | **Supply-Risk-Reduced Discovery Yield** — fraction of BOFN-proposed alloys meeting family-specific performance thresholds AND supply-risk reduction vs incumbent (Scalmalloy/Be-Cu) | 0% (no data yet) | ≥20% of tested compositions (Stretch: ≥30%) | ≥50% | ASTM E8 tensile + ICP-OES composition verification + Helbig SRI calculation; family-specific thresholds: Al-Mn-Cr-Zr YS≥250 aged/EL≥5%, Al-Zr YS≥200 as-built/EL≥8%, Cu-Cr-Zr YS≥200 aged/≥50% IACS; per Ge et al. (2025), Arena et al. (2024), Biffi et al. (2024) |
| 2 | **Critical Mineral Demand Reduction Index (CMDRI)** — composite supply-risk score reduction vs Scalmalloy (Al-Mg-Sc-Zr, primary comparator) and AlSi10Mg (LPBF process benchmark), using Helbig 12-indicator + Ferro & Bonollo Alloy Criticality Index | SRI_mean of Scalmalloy ≈ 0.65 (Sc-dominated) | ≥40% SRI_mean reduction vs Scalmalloy in best alloy; ≥15% vs AlSi10Mg (Stretch: ≥50% vs Scalmalloy) | ≥50% mean reduction across 3+ families | Dual reporting: Helbig 12-indicator per Mulukutla et al. (2024) + Ferro & Bonollo (2019) alloy criticality index; element-level waterfall decomposition |
| 3 | **AI Acceleration Factor** — iterations to reach performance threshold vs baselines | Random search baseline | ≥3× fewer than random, ≥1.5× vs standard BO (Base: ≥2× vs random); report win rate across seeds | ≥5× vs random | Pre-registered benchmark with 4 baselines (random, expert DOE, standard BO, BOFN−mineral ablation) + BOFN as method under test, ≥20 seeds (increase to ≥30 if power analysis indicates), bootstrap CI; per Hastings et al. (2024), Adesiji et al. (2026), Turner et al. (2021) |
| 4 | **Closed-Loop Throughput** — alloy compositions with complete property records per month through full pipeline | 0 (manual workflow) | ≥8 compositions/month sustained (Base: ≥5/month); pipeline completion rate ≥70% | ≥20 compositions/month | Tiered: Primary = compositions with full tensile records; Secondary = compositions entered into pipeline (including failures); Tertiary = compositions with ≥ density data; per Volk & Abolhasani (2024) demonstrated vs theoretical throughput |
| 5 | **Mineral-Burden Optimization Efficacy** — Pareto improvement when mineral-burden objective is added to BOFN vs performance-only BO over a broader composition space | Performance-only BO over expanded search space (including Sc/Mg-containing candidates) | Hypervolume ratio ≥1.15 (Base: ≥1.10); demonstrate mineral-burden/performance trade-off conflict exists before claiming improvement | Multi-objective Pareto with ≥3 performance + mineral-burden objectives | Pareto hypervolume indicator + number of non-dominated solutions + mineral-burden variance across Pareto set, ≥20 seeds; per Mulukutla et al. (2024), Daulton et al. (2020) qEHVI |
| 6 | **Digital Thread Completeness** — fraction of alloy iterations with full provenance from CALPHAD through tensile result per formal schema | 0% | ≥90% (Base: ≥85%) with supply-risk metadata linked to every composition | 100% with FAIR compliance | Automated schema-validation audit against defined minimum metadata set (composition, CALPHAD version, powder batch, LPBF params, ASTM E8 results, BOFN trace, SRI score); FAIR sub-metrics (Findable, Accessible, Interoperable, Reusable) tracked separately |

> **Supply-Risk-Reduced Discovery Yield** is the single most memorable metric for Topic 3B: it captures BOFN efficiency, throughput, AND supply-risk reduction in one number. The shift from "mineral-lean" to "supply-risk-reduced" acknowledges that Zr, Mn, Cr are themselves critical minerals while demonstrating net reduction vs Sc/Mg/REE/Be-dependent incumbents.

> **CMDRI** directly addresses Topic 3B's mandate: "REDUCING DEMAND for critical minerals." Comparing against Scalmalloy (SRI_mean ≈ 0.65) rather than AlSi10Mg (SRI_mean ≈ 0.25) produces a more impactful and defensible supply-risk reduction claim. Element-level decomposition shows exactly where risk reduction comes from.

### Multi-Tier Discovery Classification

Instead of a single pass/fail, Discovery Yield is classified in three tiers to give credit for partial successes that inform BOFN iterations:

| Tier | Criteria | Phase I Target |
|------|----------|---------------|
| Tier 1 (Full Pass) | Family-specific YS/EL threshold AND SRI reduction ≥ 25% vs incumbent | ≥20% |
| Tier 2 (Partial Pass) | Meets YS OR EL threshold AND SRI reduction ≥ 15% vs incumbent | ≥40% |
| Tier 3 (Printable) | Crack-free, ≥99% density, any properties, composition verified | ≥70% |

---

## Phase I Go/No-Go Decision Framework (Topic 3B)

### 7 Mandatory "Go" Gates

All mandatory gates must pass for a GO decision. Gates 2 and 4 are Topic 3B-specific additions for critical mineral displacement and mineral-burden BOFN demonstration. Gate criteria have been refined based on KPI deep-dive reviews (Iterations 9-14).

| Gate | Criterion | Minimum Threshold | Evidence Required | Timing |
|:---:|---|---|---|---|
| 1 | **Closed-loop autonomy** | ≥3 autonomous CALPHAD→atomization→LPBF→tensile→BOFN cycles without manual intervention; pipeline completion rate ≥60% | Timestamped logs showing end-to-end autonomous execution + completion rate calculation | Month 4 |
| 2 | **Supply-risk-reduced alloy discovery** | ≥1 Al-Zr or Al-Mn-Cr-Zr alloy meets family-specific YS/EL threshold (Al-Mn-Cr-Zr: YS≥250 aged/EL≥5%; Al-Zr: YS≥200 as-built/EL≥8%) with SRI_mean ≥25% below Scalmalloy, verified by ICP-OES | Tensile test certificate + ICP-OES composition report + Helbig SRI calculation with element-level waterfall | Month 6 |
| 3 | **Printable process window** | ≥99.0% relative density for ≥2 distinct supply-risk-reduced compositions via LPBF; specify as-built condition and build orientation | Archimedes density or CT scan data with orientation documented | Month 5 |
| 4 | **Mineral-burden BOFN demonstration** | BOFN with supply-risk objective shows Pareto improvement over performance-only BO on broader search space (including Sc/Mg-containing candidates), hypervolume ratio ≥1.10; must first demonstrate trade-off conflict exists | Benchmark comparison plot with ≥20 seeds and bootstrap CI + conflict pre-check correlation analysis | Month 7 |
| 5 | **Mechanical property threshold** | ≥2 supply-risk-reduced compositions meet family-specific targets: Al-Zr YS≥200 as-built/EL≥8%; Al-Mn-Cr-Zr YS≥250 aged/EL≥5%; tested in most conservative build orientation (Z or whichever is weakest) | ASTM E8 tensile data with ≥3 replicates per composition, orientation specified | Month 7 |
| 6 | **AI optimization advantage** | BOFN reaches performance threshold in ≥2× fewer iterations than random and ≥1.3× vs standard BO; win rate ≥ 65% across seeds; report vs all 4 baselines + ablation | Pre-registered benchmark statistical analysis with win rate, median AF, and bootstrap CI | Month 8 |
| 7 | **Digital thread & scaling evidence** | ≥85% digital thread completeness per formal provenance schema; supply-risk metadata linked to ≥90% of compositions; documented Phase II scale-up pathway | Schema validation report + FAIR sub-metric audit + Phase II scaling plan | Month 9 |

### Scoring Rubric (0-100)

| Component | Points | Evidence |
|---|---:|---|
| A. Supply-risk reduction & CMDRI demonstration | 20 | Gates 2, 4 |
| B. Mechanical performance (supply-risk-reduced alloys) | 15 | Gate 5 |
| C. AI/BOFN optimization advantage | 15 | Gate 6 |
| D. Closed-loop autonomy & throughput | 15 | Gates 1, 3 |
| E. Digital thread & data quality | 15 | Gate 7 |
| F. Scaling evidence & Phase II readiness | 10 | Gate 7 |
| G. Cu-Cr-Zr stretch demonstration | 10 | Stretch goal evidence |
| **Total** | **100** | |

**Decision rules:**
- **GO**: All mandatory gates passed AND score ≥75
- **CONDITIONAL GO**: All mandatory gates passed AND score 65-74 AND approved risk-mitigation plan
- **NO-GO**: Any mandatory gate failed OR score <65

### Early Warning Indicators

| Month | Warning Signal | Risk |
|:---:|---|---|
| 2 | <1 autonomous cycle executed end-to-end | Integration risk |
| 2 | No locked baseline defined for EF/AF benchmarking (all 4 baselines + ablation) | Evaluation risk |
| 2 | Al-Zr/Al-Mn-Cr-Zr powder atomization not demonstrated | Material risk |
| 2 | Supply-risk index calculator not built (Helbig + Ferro & Bonollo) | CMDRI risk |
| 4 | No supply-risk-reduced parameter set achieves ≥99.0% density | Printability risk |
| 4 | BOFN mineral-burden scalarization not implemented; trade-off conflict not verified | AI development risk |
| 4 | Pipeline completion rate <50% | Throughput risk |
| 6 | No supply-risk-reduced alloy meets YS≥200 MPa (any family) | Critical mineral gate risk |
| 6 | No credible EF/AF >1 even retrospectively; win rate <50% | AI advantage risk |
| 6 | No Helbig SRI calculation validated against Scalmalloy benchmark | CMDRI risk |

### Monthly Milestone Timeline

| Month | Milestone | Target |
|:---:|---|---|
| 1 | Infrastructure: BOFN deployed, CALPHAD pipeline for Al-Zr/Al-Mn-Cr-Zr operational, first powder batch, SRI calculator built (Helbig + Ferro & Bonollo) | Systems operational; Scalmalloy SRI benchmark calculated |
| 2 | First 3 supply-risk-reduced compositions through full pipeline; all 4 baselines + ablation locked; formal provenance schema deployed | 3 complete datasets; pre-registration filed; benchmark design frozen |
| 3 | LPBF batching validated (≥2 compositions/build); mineral-burden conflict pre-check completed | Demonstrated; ≥10 compositions total; trade-off between performance and supply-risk confirmed |
| 4 | Steady-state throughput; BOFN mineral-burden objective active over broader search space | ≥5 compositions/month; mineral-burden objective integrated; pipeline completion rate tracked |
| 5 | Mid-project performance assessment | ≥25 compositions; initial EF/AF estimates with win rates; ≥2 compositions at ≥99.0% density |
| 6 | Mid-project review: supply-risk-reduced alloy discovery gate check | ≥1 alloy meeting family-specific threshold + SRI reduction vs Scalmalloy; all early warnings resolved |
| 7 | Mineral-burden BOFN benchmark; mechanical property gate | Hypervolume ratio ≥1.10 with conflict pre-check documented; ≥2 compositions meeting family targets |
| 8 | Cu-Cr-Zr stretch: atomization + printability feasibility; CMDRI element-level decomposition published | Cu-Cr-Zr powder produced; ≥99.0% density; waterfall chart for all qualified alloys |
| 9 | Final: go/no-go package, CMDRI calculation vs Scalmalloy and AlSi10Mg, Phase II plan | All gates assessed; CMDRI ≥40% vs Scalmalloy; digital thread ≥85% with supply-risk metadata; FAIR audit |

---

## Material Performance Targets (Topic 3B)

### Al-Zr Family (Primary, ~40% of Phase I effort)

Al₃Zr L1₂ nanoprecipitates provide precipitation strengthening without Sc or REE. Ge et al. (2025) reported ICME-optimized Al-Zr-Er-Ni with YS 279 MPa as-built / 395 MPa peak-aged (400°C/8h), with 16% as-built elongation. FLAIME's Al-Zr compositions will avoid Er (an REE), focusing on binary Al-Zr and ternary Al-Zr-X where X is non-critical (e.g., Fe, Si, Ti). Note: binary Al-Zr (without Mn/Cr multi-element strengthening) typically achieves lower YS but higher EL than the Al-Mn-Cr-Zr family, hence the family-specific threshold of YS≥200 MPa / EL≥8% (vs. YS≥250 / EL≥5% for Al-Mn-Cr-Zr).

### Al-Mn-Cr-Zr Family (Primary, ~40% of Phase I effort)

All constituents (Al, Mn, Cr, Zr) have moderate-to-low supply risk (Helbig SRI ~0.3–0.5) compared to Sc (~0.9) and REE (~0.7–0.9) in incumbent alloys, though Mn and Cr appear on the USGS 2022 Critical Minerals List. Arena et al. (2024) reported Al-HS1 (Al-5Mn-0.8Cr-0.6Zr-0.17Fe-0.24Si) with YS 250 MPa as-printed, ~350 MPa after aging at 375°C. Mehta et al. (2022) demonstrated crack-free LPBF at ~99.5% density with 98.9–103.4 HV as-printed, 130–144 HV after direct aging.

### Cu-Cr-Zr (Stretch, ~20% of Phase I effort)

Be-Cu replacement pathway. Biffi et al. (2024) reported LPBF Cu-Cr-Zr (99.3% density) with as-built YS 167 MPa, UTS 230 MPa, EL 31%; after solution annealing + aging, UTS 265 MPa with 22% EL.

| Alloy Family | Property | Literature Baseline | Phase I Target | Phase II Target |
|---|---|---|---|---|
| Al-Zr family | Yield strength (YS) | 279 MPa as-built; 395 MPa peak-aged (Ge et al., 2025) | ≥200 MPa as-built; ≥280 MPa aged | ≥350 MPa aged |
| Al-Zr family | UTS | ~400 MPa (Ge et al., 2025) | ≥250 MPa as-built; ≥320 MPa aged | ≥400 MPa |
| Al-Zr family | Elongation | 0.9–16% depending on composition (Ge et al., 2025) | ≥5% (Base); ≥8% (Tier 1 pass) | ≥8% |
| Al-Zr family | Relative density | >99.5% (Ge et al., 2025) | ≥99.0% | ≥99.5% |
| Al-Mn-Cr-Zr family | Yield strength (YS) | 250 MPa as-printed, ~350 MPa aged (Arena et al., 2024) | ≥250 MPa aged | ≥350 MPa |
| Al-Mn-Cr-Zr family | UTS | ~350–400 MPa range (Arena et al., 2024) | ≥300 MPa | ≥400 MPa |
| Al-Mn-Cr-Zr family | Elongation | ≥3–5% est. (Mehta et al., 2022; Arena et al., 2024) | ≥5% (Tier 1 pass) | ≥6% |
| Al-Mn-Cr-Zr family | Hardness | 103 HV as-built; 130–144 HV peak-aged (Mehta et al., 2022) | ≥110 HV as-built; ≥130 HV aged | ≥140 HV |
| Cu-Cr-Zr (stretch) | YS | 141–167 MPa LPBF as-built (Biffi et al., 2024) | ≥200 MPa aged | ≥400 MPa |
| Cu-Cr-Zr (stretch) | UTS | 230–265 MPa LPBF (Biffi et al., 2024) | ≥300 MPa | ≥500 MPa |
| Cu-Cr-Zr (stretch) | Elongation | 22–31% LPBF (Biffi et al., 2024) | ≥15% | ≥18% at higher strength |
| Cu-Cr-Zr (stretch) | Conductivity | ~80% IACS wrought; LPBF data limited (Biffi et al., 2024) | ≥50% IACS | ≥75% IACS |
| AlSi10Mg (benchmark) | YS / UTS / EL | 250–300 / 350–400 / 5–10% (Arena et al., 2024) | Benchmark only | Benchmark only |

---

## AI Advantage Demonstration Protocol (Pre-Registered)

### Pre-Registered Benchmark Design

FLAIME will pre-register a benchmark protocol before experiments begin, following SDL benchmarking best practices (Adesiji et al., 2026; Volk & Abolhasani, 2024).

**Four baselines plus one BOFN ablation** ensure the AI advantage claim is defensible and isolate each component's contribution:

| ID | Description | Budget | Purpose |
|---|---|---|---|
| B1: Random | Uniform random sampling from CALPHAD-feasible supply-risk-reduced space | 20 compositions | Lower bound; any method should beat this |
| B2: Expert DOE | Latin hypercube or factorial design by domain expert | 20 compositions | Tests whether structure alone suffices |
| B3: Standard BO | Single-task GP-BO (no function networks, no mineral-burden objective) | 20 compositions | Isolates BOFN's multi-node advantage |
| **BOFN** (method under test) | Full BOFN with mineral-burden scalarization and cost-aware p-KGFN acquisition | 20 compositions | The method under test — not a baseline |
| B4: BOFN−mineral (ablation) | BOFN without mineral-burden objective (performance-only BOFN) | 20 compositions | Isolates the mineral-burden objective's contribution from the BOFN architecture advantage |

All baselines and the BOFN ablation use identical search spaces, property evaluation methods, and stopping criteria. ≥20 replicate seeds per condition for statistical power (increase to ≥30 if prospective power analysis using CALPHAD surrogates indicates marginal power at 20 seeds). Primary metrics: Enhancement Factor `EF(n) = y*_BOFN(n) / y*_baseline(n)` and Acceleration Factor `AF(y) = n_baseline / n_BOFN` to reach target y. Pre-specify whether AF is computed at a fixed performance threshold (80% of best-known) or at the campaign's realized best.

**Statistical analysis**: Paired bootstrap CI (1000 resamples) on EF/AF following Adesiji et al. (2026) *Digital Discovery* and Volk & Abolhasani (2024) *Nature Communications*; Mann-Whitney U test; Bonferroni correction for 4 pairwise comparisons (B1-BOFN, B2-BOFN, B3-BOFN, B4-BOFN). Effect size reported as Cohen's d. Pre-declared α=0.05. Minimum meaningful effect: EF≥1.2 (corresponding to ≥20% property improvement at fixed budget). **Report win rate** (fraction of seeds where BOFN outperforms each baseline) alongside median AF to transparently handle the "BO sometimes loses" problem per Turner et al. (2021). Report EF trajectories as a function of normalized experiment number (n/d, where d is dimensionality) per Adesiji et al. (2026).

### Time-Ledger Methodology

Following Kavalsky et al. (2023), FLAIME will decompose total acceleration into three components:

1. **Automation acceleration**: Time saved from automated sample handling, data transfer, and workflow orchestration vs. manual operation
2. **AI acceleration**: Experiments saved from intelligent selection vs. random/DOE baseline
3. **Throughput acceleration**: Parallelism and batching gains from LPBF multi-composition builds

Each experiment is timestamped at every stage (BOFN recommendation → atomization → LPBF build → characterization → database entry → next recommendation). The time ledger enables honest reporting even if AI advantage is modest: a platform showing 1.5× AI acceleration but 3× automation acceleration and 2× throughput acceleration still delivers ~9× total acceleration — a compelling Phase II case.

### Risk Framework: Modest AI Advantage

If BOFN achieves only ~2× acceleration (Base target), the honest reporting framework is:
- Report total platform acceleration (automation × AI × throughput) which may still be substantial
- Identify specific decision types where BOFN excelled vs. where it matched baselines
- Highlight the mineral-burden objective's contribution: even modest AI advantage, combined with supply-risk-reduced discovery constraint, is novel
- Document that the digital thread, qualification infrastructure, and supply-risk framework are independently valuable for Phase II

---

## Critical Mineral Impact Metrics (New for Topic 3B)

A dedicated metric category quantifying the central deliverable of Topic 3B. The Supply Risk Index follows the Helbig-style 12-indicator framework as implemented by Mulukutla et al. (2024), while the Alloy Criticality Index is adapted from Ferro & Bonollo (2019). Both are reported for transparency (Helbig provides granular supply-risk assessment; Ferro & Bonollo provides compositionally interpretable alloy-level scoring). Supply-risk comparisons are made against Scalmalloy (Al-Mg-Sc-Zr, primary comparator) and AlSi10Mg (LPBF process benchmark).

| Metric | Definition | Phase I Target | Phase II Target | Method |
|---|---|---|---|---|
| Supply-risk-reduced compositions discovered | Unique compositions meeting family-specific performance thresholds with SRI_mean ≥25% below Scalmalloy | ≥3 compositions | ≥15 across 3+ families | ICP-OES + ASTM E8 + Helbig SRI |
| Supply Risk Index Reduction vs Scalmalloy (ΔSR) | % reduction in Helbig SRI_mean vs Scalmalloy (SRI ≈ 0.65, Sc-dominated) | ≥40% for best alloy | ≥50% mean across portfolio | 12-indicator calculation per Mulukutla et al. (2024) |
| Supply Risk Index Reduction vs AlSi10Mg (ΔSR) | % reduction in Helbig SRI_mean vs AlSi10Mg (SRI ≈ 0.25) | ≥15% for best alloy | ≥25% mean across portfolio | 12-indicator calculation |
| Element-level supply-risk decomposition | Waterfall chart showing per-element contribution to alloy SRI for each qualified composition | Report for all qualified alloys | Published with element-level uncertainty | Helbig per-element scores × mass fraction |
| Critical element mass displacement | kg of Sc/Mg/REE/Be displaced per metric ton of FLAIME alloy vs incumbent | Calculate for 1 MT scenario | Validated for 10 MT scenario | Mass balance analysis |
| Beryllium elimination potential | Fraction of Be-Cu performance envelope (YS × conductivity product) reached by Cu-Cr-Zr | ≥30% of Be-Cu product (stretch) | ≥70% | Strength-conductivity comparison |
| Compositional search space efficiency | Fraction of tested compositions yielding Tier 1 (Full Pass) qualifying alloys | ≥15% hit rate | ≥30% | Pre-registered benchmark data |
| Incumbent parity index | Number of key properties where FLAIME alloy matches/exceeds Scalmalloy and AlSi10Mg | Parity with AlSi10Mg in ≥2 of 3 properties for Al; ≥1 of 3 vs Scalmalloy | Full parity for ≥2 families vs both | Property-wise comparison |

---

## Condensed Proposal-Ready KPI Table

| Category | KPI | Phase I Baseline | Phase I Target | Phase II Target | Method |
|---|---|---|---|---|---|
| Platform | Closed-loop cycle time (median) | 7-14 days/comp | ≤72 h/comp | ≤24 h screened; ≤72 h qualified | Timestamp logs |
| Platform | Throughput: complete tensile records/month | 0 (manual) | ≥8/month sustained | ≥20/month sustained | Database count (primary metric) |
| Platform | Throughput: compositions entered pipeline/month | 0 | ≥12/month | ≥30/month | Pipeline log (secondary metric) |
| Platform | Pipeline completion rate | — | ≥70% | ≥85% | Completed/initiated runs |
| Platform | Hands-free fraction | <20% | ≥70% | ≥90% | Workflow audit |
| AI/BOFN | Acceleration factor vs random | 1.0× | ≥3.0× | ≥5.0× | Pre-registered 4-baseline + ablation benchmark per Hastings et al. (2024), Adesiji et al. (2026) |
| AI/BOFN | Win rate vs random (across seeds) | 50% | ≥80% | ≥90% | Bootstrap analysis per Turner et al. (2021) |
| AI/BOFN | Mineral-burden hypervolume ratio (broader space) | 1.0 | ≥1.15 | MOBO with ≥3 objectives | Pareto hypervolume per Mulukutla et al. (2024), Daulton et al. (2020) |
| AI/BOFN | Predictive MAE (YS) | >75 MPa | ≤40 MPa | ≤25 MPa across families | Nested CV + prospective holdout |
| AI/BOFN | Uncertainty calibration (90% PICP) | Uncalibrated | 0.80-0.95 | 0.85-0.95 | Reliability diagrams, conformal prediction |
| Critical Minerals | CMDRI vs Scalmalloy (supply-risk reduction) | 0% | ≥40% vs Scalmalloy | ≥50% across families | Helbig 12-indicator + Ferro & Bonollo per Mulukutla et al. (2024) |
| Critical Minerals | CMDRI vs AlSi10Mg | 0% | ≥15% | ≥25% | Helbig 12-indicator |
| Critical Minerals | Supply-risk-reduced qualifying compositions | 0 | ≥3 | ≥15 across 3+ families | ICP-OES + ASTM E8 + SRI |
| Critical Minerals | Be-elimination potential (stretch) | 0% | ≥30% of Be-Cu | ≥70% | Strength × conductivity product |
| Materials | ASTM E8 tensile dataset volume | 0 | ≥100 specimens | ≥500 specimens | Linked composition/process metadata |
| Materials | Powder chemistry accuracy | >±1.0 at.% | ≤±0.3 at.% | ≤±0.2 at.% | ICP-OES/XRF vs charge recipe |
| Materials | LPBF build density (screening) | 95-98% | ≥99.0% | ≥99.5% | Archimedes + metallographic/XCT |
| Qualification | ASTM E8/E8M compliance rate | <25% | 100% | 100% | QA audit |
| Qualification | Digital-thread completeness (per schema) | <30% | ≥90% with SRI metadata | ≥99% with FAIR | UUID-linked provenance audit + schema validation |
| Scaling | Transfer-learning lift (new family) | 0% | ≥20% data efficiency for Cu-Cr-Zr | ≥40% for expanded families | Warm vs cold start campaigns |

> **Tier note**: "Phase I Target" values in this table correspond to Expected-tier targets. Mandatory go/no-go gate thresholds use Base-tier minimums (see §Go/No-Go Gates above).

---

## Detailed Category Metrics

### Category 1: Throughput & Efficiency

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Unique supply-risk-reduced compositions with complete tensile records (9 mo) | ≥30 | ≥50 | ≥80 | Lab inventory (steady state reached ~month 4) |
| Compositions with complete records per month (steady state, months 4-9) | ≥5 | ≥8 | ≥12 | Monthly log (primary throughput metric) |
| Compositions entered into pipeline per month (incl. failures) | ≥8 | ≥12 | ≥18 | Monthly log (secondary throughput metric) |
| Compositions with ≥ density data per month (exploits BOFN partial evaluation) | ≥10 | ≥15 | ≥22 | Monthly log (tertiary throughput metric) |
| Pipeline completion rate | ≥60% | ≥70% | ≥80% | Complete records / entered pipeline |
| Compositions per LPBF build (batching) | ≥2 | ≥3 | ≥4 | Build records |
| Best-case pipeline cycle time | ≤5 days | ≤3 days | ≤2 days | Timestamps |
| Median pipeline cycle time | ≤7 days | ≤5 days | ≤4 days | P50 tracker |
| Demonstrated vs theoretical throughput ratio | ≥50% | ≥70% | ≥85% | Per Volk & Abolhasani (2024) |
| CALPHAD compositions screened (supply-risk-reduced space) | ≥2,000 | ≥4,000 | ≥8,000 | Batch log |

### Category 2: Material Performance (Supply-Risk-Reduced Alloys)

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Best Al-Zr YS (as-built) | ≥150 MPa | ≥200 MPa | ≥280 MPa | ASTM E8/E8M |
| Best Al-Zr YS (aged) | ≥200 MPa | ≥280 MPa | ≥350 MPa | ASTM E8/E8M |
| Best Al-Zr EL (at YS target) | ≥5% | ≥8% | ≥12% | ASTM E8/E8M (Z-orientation) |
| Best Al-Mn-Cr-Zr YS (aged) | ≥200 MPa | ≥250 MPa | ≥350 MPa | ASTM E8/E8M |
| Best Al-Mn-Cr-Zr UTS | ≥250 MPa | ≥300 MPa | ≥400 MPa | ASTM E8/E8M |
| Best Al-Mn-Cr-Zr EL (at YS target) | ≥3% | ≥5% | ≥6% | ASTM E8/E8M (Z-orientation) |
| Supply-risk-reduced alloys meeting Tier 1 (Full Pass) | ≥1 | ≥3 | ≥5 | Family-specific YS/EL + SRI threshold |
| Supply-risk-reduced alloys meeting Tier 2 (Partial Pass) | ≥3 | ≥6 | ≥10 | YS or EL threshold + SRI reduction |
| Pareto-optimal supply-risk-reduced compositions | ≥3 | ≥5 | ≥10 | Replicated, with confidence bounds |
| Cu-Cr-Zr YS (aged, stretch) | ≥150 MPa | ≥200 MPa | ≥300 MPa | ASTM E8 |
| Cu-Cr-Zr conductivity (stretch) | ≥40% IACS | ≥50% IACS | ≥60% IACS | 4-point probe |

### Category 3: AI/Autonomy Performance

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| BOFN acceleration factor vs random | ≥2× | ≥3× | ≥5× | Pre-registered 4-baseline + ablation benchmark |
| BOFN acceleration vs standard BO | ≥1.3× | ≥1.5× | ≥2× | Multi-seed comparison |
| BOFN vs BOFN−mineral (mineral-burden contribution) | ≥1.05× | ≥1.15× | ≥1.3× | Isolates mineral-burden objective value |
| Win rate vs random (across seeds) | ≥65% | ≥80% | ≥90% | Bootstrap per Turner et al. (2021) |
| Win rate vs standard BO (across seeds) | ≥55% | ≥65% | ≥75% | Bootstrap |
| Mineral-burden hypervolume ratio (broader space) | ≥1.10 | ≥1.15 | ≥1.25 | Pareto hypervolume |
| Model MAE (YS) | ≤50 MPa | ≤40 MPa | ≤25 MPa | Nested CV |
| Uncertainty calibration (90% PICP) | 0.70-0.95 | 0.80-0.95 | 0.85-0.95 | Conformal prediction |
| Autonomous decision cycles | ≥10 | ≥30 | ≥60 | Iteration log |
| Human intervention rate (trend) | 40%→25% | 30%→15% | 20%→10% | Override tracking |
| Discovery Yield vs random (supply-risk-reduced) | ≥2× | ≥3× | ≥5× | Yield comparison |

### Category 4: Critical Mineral Impact

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Supply-risk-reduced qualifying compositions (Tier 1) | ≥1 | ≥3 | ≥5 | ICP-OES + ASTM E8 + SRI |
| CMDRI vs Scalmalloy (best alloy) | ≥25% | ≥40% | ≥50% | Helbig 12-indicator SRI_mean |
| CMDRI vs AlSi10Mg (best alloy) | ≥10% | ≥15% | ≥25% | Helbig 12-indicator SRI_mean |
| CMDRI vs Scalmalloy (portfolio mean) | Track | ≥25% | ≥40% | Helbig 12-indicator SRI_mean |
| Element-level supply-risk decomposition | Report for ≥1 alloy | All qualified alloys | Published waterfall charts | Helbig per-element × mass fraction |
| Critical element mass displacement (1 MT scenario) | Calculate | Report all elements | Published | Mass balance |
| Be-elimination potential (Cu-Cr-Zr) | Feasibility only | ≥30% | ≥50% | Strength × conductivity |
| Search space efficiency (Tier 1 pass rate) | ≥10% | ≥15% | ≥25% | Tier 1 qualifying / tested |
| Incumbent parity vs Scalmalloy (Al families) | 1 of 3 properties | 2 of 3 | 3 of 3 | Property comparison |
| Incumbent parity vs AlSi10Mg (Al families) | 2 of 3 properties | 3 of 3 | Exceed all | Property comparison |

### Category 5: Resource Efficiency & Sustainability

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Compositions with $/kg assigned | 100% | 100% | 100% | Σ(element_price × mass_fraction) |
| Supply Risk Index (SRI) tracked | 100% | Minimize across top alloys | Top alloys SRI<0.3 | Helbig 12-indicator |
| Specific Energy Consumption (atomization) | Track kWh/kg | Report + benchmark | Show improvement | E_total / m_deposited |
| Buy-to-Fly Ratio | Track | ≤2.0 | ≤1.5 | m_input / m_final_part |
| CO₂ intensity estimate | Model built | Report for all qualified | Show downward trend | Σ(CO₂_material + CO₂_process) |
| Cost per qualified supply-risk-reduced alloy | Track | Benchmark vs manual | ≥2× efficiency | Program cost / qualified alloys |

### Category 6: Workforce Development

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Total students trained | 12 | 12 | 12+ | Roster |
| Cross-trained on ≥2 nodes | ≥6 | ≥8 | ≥10 | Records |
| Student retention (9 months) | ≥75% | ≥85% | ≥95% | HR records |
| First-generation participation | Report | ≥25% | ≥30% | Demographics |
| URG representation | Report | ≥20% | Match ASEE benchmarks | Demographics |
| Pre/post skills assessment (Cohen's d) | Documented | d≥0.5 | d≥1.0 | Validated instrument |
| Student co-authored outputs | ≥1 | ≥2 | ≥4 | Publications |

### Category 7: Data Infrastructure & FAIR

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| FAIR structured database | 1 database | + public release | + DOI + schema | Zenodo |
| Data completeness (Tier 1: density+hardness+comp) | ≥85% | ≥90% | ≥95% | Schema validation audit |
| Data completeness (Tier 2: full tensile+SEM) | ≥50% | ≥70% | ≥85% | Schema validation audit |
| Data latency (measurement → database) | ≤48 hr | ≤24 hr | ≤4 hr | Timestamps |
| Decision traceability (BOFN recommendation trace linked) | ≥90% | ≥95% | 100% | Audit log |
| Supply-risk metadata linked (Helbig SRI + per-element scores) | ≥80% | ≥95% | 100% | SRI attached to each composition |
| Formal provenance schema coverage | Deployed | 100% new records | 100% all records | Schema validation |
| FAIR Findable sub-metric (unique PIDs, searchable metadata) | Deployed | ≥90% | 100% | FAIR assessment tool |
| FAIR Accessible sub-metric (open protocols, authentication) | Deployed | ≥90% | 100% | FAIR assessment tool |
| FAIR Interoperable sub-metric (controlled vocabularies, linked data) | Deployed | ≥80% | ≥95% | FAIR assessment tool |
| FAIR Reusable sub-metric (rich metadata, domain standards, license) | Deployed | ≥80% | ≥95% | FAIR assessment tool |

### Category 8: Process Quality

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Powder yield 15-63 μm | ≥25% | ≥35% | ≥50% | PSD analysis |
| LPBF relative density (screening) | ≥97% | ≥98% | ≥99% | Archimedes |
| LPBF relative density (down-selected) | ≥98.5% | ≥99% | ≥99.5% | Archimedes + XCT |
| Tensile replicate variability (CoV YS) | ≤15% | ≤10% | ≤7% | Statistical |
| Build success rate (novel supply-risk-reduced) | ≥60% | ≥70% | ≥80% | Build log |

---

## Phase II Readiness Indicators (Topic 3B)

The Phase II narrative is reoriented from temperature upgrade to expanded supply-risk-reduced discovery and Cu-Cr-Zr full optimization.

1. **Expanded supply-risk-reduced discovery**: ≥3 compositions meeting family-specific performance thresholds with SRI_mean ≥25% below Scalmalloy across ≥2 alloy families (Al-Zr and Al-Mn-Cr-Zr); BOFN convergence trajectories documented in digital thread with element-level supply-risk decomposition
2. **Cu-Cr-Zr full optimization pathway**: Phase I printability demonstration (≥99.0% density) + initial BOFN-guided property data; Phase II BOFN configuration incorporating conductivity as additional objective per BIRDSHOT paradigm (Hastings et al., 2024)
3. **Multi-alloy-family platform validation**: Pipeline is alloy-system-agnostic — can switch between Al-Zr, Al-Mn-Cr-Zr, and Cu-Cr-Zr without architectural changes, validated by ≥1 closed-loop cycle in each family
4. **Supply-risk Pareto portfolio**: BOFN Pareto frontier in (performance, supply-risk) space demonstrated over broader search space; Phase II extends to ≥3 performance + 1 supply-risk objective in full MOBO per Mulukutla et al. (2024) and Daulton et al. (2020) qEHVI
5. **Demonstrated AI advantage**: Pre-registered AF≥2× vs random (minimum meaningful effect EF≥1.2) with CI excluding 1.0 and win rate ≥65% proves BOFN adds value beyond automation alone; mineral-burden objective contribution isolated via BOFN−mineral ablation comparison
6. **Scaling evidence**: Atomization batch sizes, LPBF build rates, and tensile throughput sufficient to project Phase II at ≥20 compositions/month; pipeline completion rate ≥70%; bottlenecks identified with mitigation plans

**Narrative bridge**: FLAIME's autonomous closed-loop framework is the invariant asset; the alloy search space is the expandable variable. Phase I proves supply-risk-reduced Al alloy discovery and supply-risk-aware optimization on accessible alloys; Phase II scales into Cu-Cr-Zr (Be-Cu replacement), expanded Al families (Al-Ce for REE supply chain stabilization), and potentially Ni-free/Co-free steels using the same BOFN engine, data schemas, and qualification metrics. The critical mineral demand reduction grows with each alloy family added.

> **Note on Phase II availability**: DE-FOA-0003612 states "PHASE II APPLICATIONS WILL NOT BE ACCEPTED IN THIS FOCUS AREA" for Topic 3B. This exclusion applies to the current solicitation. Future solicitations may offer Phase II opportunities under different focus areas, and Phase I teams can also pivot to a Phase-II-eligible focus area within the current round. Phase II readiness indicators above are therefore framed as evidence that Phase I would generate to justify a future Phase II application.

---

## Benchmarking vs State-of-the-Art (Topic 3B)

| Platform | Domain | Closed-Loop? | Supply-Risk Integration? | Key Results | FLAIME Differentiator |
|---|---|---|---|---|---|
| **FLAIME** (proposed) | Supply-risk-reduced Al + Cu-Cr-Zr LPBF | Yes (BOFN) | Yes — mineral-burden objective + Helbig SRI + Ferro ACI | Target: ≥3 alloys, CMDRI ≥40% vs Scalmalloy | First closed-loop SDL with powder→AM→tensile AND supply-risk objective |
| **Scalmalloy®** (incumbent) | Al-Mg-Sc-Zr | No | No — depends on critical Sc (SRI ≈ 0.65) | UTS ~496 MPa after heat treatment (Knoop et al., 2020) | FLAIME eliminates Sc dependence; primary CMDRI comparator |
| BIRDSHOT/ULTIMATE (Texas A&M) | CoCrFeNiVAl FCC HEA; refractory HEA | Yes — 5 optimization iterations | No explicit mineral-burden | 3-obj Pareto; 0.15% design-space sampling; 54% hypervolume increase (Hastings et al., 2024; Paramore et al., 2025) | FLAIME adds mineral-burden objective + LPBF manufacturing |
| Mulukutla et al. (2024) | MoNbTiVW refractory HEA | Computational only | Yes — Helbig SRmean objective | Supply-risk steered search to lower-risk compositions (Mulukutla et al., 2024) | FLAIME closes loop experimentally on Al/Cu LPBF |
| CMI Hub Al-Ce (Ames Lab) | Al-Ce binary/ternary | No — conventional | Indirect (Ce coproduct) | 459 MPa UTS / 274 MPa YS for Al-7Cu-3Ce SLM (Czerwinski, 2020; Sims et al., 2017) | FLAIME avoids REEs entirely; autonomous discovery |
| AlSi10Mg (benchmark) | Commercial LPBF | No | No (SRI ≈ 0.25, low criticality) | YS 250–300, UTS 350–400, EL 5–10% (Arena et al., 2024) | LPBF process benchmark only; weak supply-risk comparator |
| A-Lab (Berkeley) | Inorganic synthesis | Yes (L4-L5) | No | 2.4 mat/day; XRD only (Szymanski et al., 2023) | A-Lab performs inorganic synthesis with XRD characterization — no AM manufacturing or tensile testing |
| AMASE (thin-film) | Thin-film combinatorial | Yes | No | Thin-film only; no bulk alloy | FLAIME targets bulk AM alloys with full tensile qualification |
| Nelaturu et al. (DED) | DED alloy exploration | Partial | No | Hardness screening only; no tensile, no atomization | FLAIME integrates atomization + LPBF + ASTM E8 tensile |
| ORNL Peregrine | LPBF process monitoring | Yes (in-situ) | No | Process control, not composition discovery | FLAIME discovers new compositions; Peregrine monitors known alloys |
| Manual lab | Any AM alloy | No | No | 2-4 comp/month (baseline) | Baseline comparison |

> **FLAIME's unique Topic 3B differentiator**: First closed-loop SDL integrating powder production + LPBF printing + full mechanical testing + supply-risk-aware Bayesian optimization in a single autonomous decision loop targeting critical mineral demand reduction. Comparing against Scalmalloy (SRI ≈ 0.65) rather than AlSi10Mg (SRI ≈ 0.25) makes the supply-risk reduction claim ~3× more impactful.

---

## Partnership & Collaboration Structure

FLAIME's partnership structure supports Genesis Mission's collaborative requirements with 3 funded industry partners (letters of collaboration) and 8 letters of support (including Ames National Lab).

### Letters of Collaboration (Funded)

| Partner | Role | Contribution | Est. Subaward |
|---|---|---|---|
| **Valimet** (industry) | Gas atomization scale-up | GA service for promising compositions identified via BOFN; produces LPBF-grade powders (15–63 μm) for qualification | $15–40K |
| **AMAZEMET** (industry) | Ultrasonic atomization | Atomizer installed at BYU; consumables, process support, maintenance; enables rapid screening of novel compositions before GA scale-up | $20–40K |
| **Thermo-Calc** (industry) | CALPHAD/AM Module simulations | AM Module licenses + technical support; simulations for solidification pathway prediction; supports Scheil and equilibrium calculations on BYU HPC | $10–25K |

### Letters of Support (Unfunded)

| Supporter | Affiliation | Relevance |
|---|---|---|
| **Ames National Lab** | DOE National Laboratory | GARS gas atomization expertise; Phase II partnership pathway for 10–100 kg batches |
| **Fehrmann Alloys** | Industry | Alloy development and powder supply chain |
| **Taylor Sparks** | University of Utah | LPBF printing collaboration; printed AlSi10Mg tensile specimens for FLAIME preliminary results |
| **Ashley Speer** | Industry/Academic | AM alloy development expertise |
| **Adam Clare** | University of Nottingham (FREng) | AM process expertise; international collaboration |
| **Chris Stiles** | Industry | AM applications and industry perspective |
| **Jae Hattrick-Simpers** | National Lab/Academic | High-throughput materials characterization; SDL expertise |
| **Keith Brown** | Boston University | Self-driving laboratory development; autonomous experimentation |

---

## Preliminary Results Evidence (In Hand)

The following preliminary results demonstrate FLAIME's readiness to begin Phase I immediately upon award. All items are completed or in hand as of April 2026.

| # | Evidence Item | Status | Relevance to Metrics |
|---|---|---|---|
| 1 | AMAZEMET ultrasonic atomizer installed at BYU | ✅ Complete | Enables KPI 4 (throughput); supports Gate 1 (closed-loop autonomy) |
| 2 | AlSi10Mg tensile specimen printed at University of Utah (Taylor Sparks) | ✅ Complete | Validates LPBF pipeline for process baseline; supports KPI 1 (discovery yield benchmark) |
| 3 | Tensile data for U of Utah AlSi10Mg specimen | ✅ Complete | Provides benchmark data for KPI 1 comparison and Gate 5 (mechanical property threshold) |
| 4 | AlSi10Mg tensile specimen from 3D Powder Tech | ✅ Complete | Cross-validates tensile testing methodology; supports KPI 4 (throughput pipeline) |
| 5 | SEM and EDS for precursor powders (AlSi10Mg, Si powder) | ✅ Complete | Validates powder characterization pipeline; supports KPI 6 (digital thread) |
| 6 | SEM and EDS for AMAZEMET-atomized mixture (Al wire + Si addition → slight composition change from original AlSi10Mg) | ✅ Complete | Demonstrates UA composition control; supports Gate 2 (alloy discovery) |
| 7 | High-temperature tensile data using standard aluminum tensile specimen | ✅ Complete | Validates high-T mechanical testing capability; supports Gate 5 |
| 8 | Thermo-Calc AM Module simulations provided by Thermo-Calc | ✅ Complete | Validates CALPHAD node; supports KPI 6 (digital thread) |
| 9 | Thermo-Calc CALPHAD simulations run on BYU HPC clusters | ✅ Complete | Demonstrates computational throughput for CALPHAD screening; supports KPIs 5 (mineral-burden optimization) and 6 (digital thread) |
| 10 | Full pKGFN pipeline implementation (BoTorch 0.12+) | ✅ Complete | Core of KPI 3 (AI acceleration); enables Gate 6 (AI advantage); supports KPI 5 (mineral-burden BOFN) |
| 11 | Automated powder dispensing demonstration | ✅ Complete | Supports KPI 4 (throughput); enables Gate 1 (closed-loop autonomy) |

> These 11 evidence items collectively demonstrate that FLAIME has operational infrastructure (items 1, 11), validated characterization pipelines (items 2–7), computational readiness (items 8–10), and the AI optimization engine (item 10) needed to begin Phase I immediately. No major capability gaps remain.

---

## Edison Scientific Task References

| Iteration | Task ID | Job Type | Focus | Chars |
|:---:|---|---|---|---:|
| Prior #1 | `eb08ff46` | LITERATURE_HIGH | Throughput/tiered framework | — |
| Prior #2 | `e5f1a050` | LITERATURE_HIGH | LPBF batching/sustainability | — |
| v4 Iter 1 | `61255bd4` | LITERATURE | Comprehensive brainstorm + mock PM | 41,996 |
| v4 Iter 2 | `6c16c2ee` | LITERATURE | 3-reviewer panel critique | 37,645 |
| v4 Iter 3 | `2bc2cf14` | LITERATURE | Go/no-go framework design | 36,167 |
| v4 Iter 4 | `488f6697` | LITERATURE | Skeptical PM stress test | 34,420 |
| v4 Iter 5 | `cce2900d` | LITERATURE | AI advantage demonstration plan | 36,475 |
| v4 Iter 6 | `92f0a824` | LITERATURE | Funded program comparison (ULTIMATE, DuAlumin-3D, TCR, DMREF, DARPA) | 36,729 |
| v4 Iter 7 | `f9d8415e` | LITERATURE | Final proposal-ready synthesis (5 KPIs, 6 gates, 9-month timeline) | 24,783 |
| **v4 Iter 8** | `9763811e` | **LITERATURE_HIGH** | **Topic 3B reassessment: revised KPIs, gates, material targets, supply-risk metrics** | **49,569** |
| **v4 Iter 9** | `aec55322` | LITERATURE_HIGH | KPI 1 deep-dive: Discovery Yield — family-specific thresholds, multi-tier classification | 39,863 |
| **v4 Iter 10** | `553ca7e3` | LITERATURE_HIGH | KPI 2 deep-dive: CMDRI — Scalmalloy comparator, Helbig+Ferro hybrid, element decomposition | 47,245 |
| **v4 Iter 11** | `a3ae145c` | LITERATURE_HIGH | KPI 3 deep-dive: AI Acceleration — 5th baseline, win rate, power analysis | 44,340 |
| **v4 Iter 12** | `26900c82` | LITERATURE_HIGH | KPI 4 deep-dive: Throughput — tiered metric, pipeline efficiency, phased ramp-up | 36,937 |
| **v4 Iter 13** | `6b28cf12` | LITERATURE_HIGH | KPI 5 deep-dive: Mineral-Burden — broader baseline, explicit MOBO, conflict pre-check | 37,460 |
| **v4 Iter 14** | `6790f2f0` | LITERATURE_HIGH | KPI 6 deep-dive: Digital Thread — provenance schema, FAIR sub-metrics, supply-risk metadata | 54,161 |
| **v4 Iter 15** | `590666ce` | ANALYSIS | Holistic cross-KPI synthesis: consistency check, top 10 recommendations, Zr/Mn/Cr framing | pending |

### Key Literature References (from Edison iterations)

1. Kavalsky et al. (2023) "By how much can closed-loop frameworks accelerate computational materials discovery?" *Digital Discovery* 2:1112-1125. 25 citations.
2. Hung et al. (2024) "Autonomous laboratories for accelerated materials discovery: a community survey" *Digital Discovery*. 31 citations.
3. Tom et al. (2024) "Self-driving laboratories for chemistry and materials science" *Chemical Reviews* 124:9633-9732. 609 citations.
4. Stach et al. (2021) "Autonomous experimentation systems for materials development" *Matter* 4:2702-2726. 363 citations.
5. Volk & Abolhasani (2024) "Performance metrics to unleash the power of self-driving labs" *Nature Communications*. 79 citations.
6. Adesiji et al. (2026) "Benchmarking self-driving labs" *Digital Discovery* 5:14-27. 5 citations.
7. Singh et al. (2026) "Datascribe: an AI-native platform for multi-objective materials design" — Digital thread/provenance framework.
8. Stuckner et al. (2026) "Benchmarking Bayesian optimization" — Multi-seed BO evaluation methodology.
9. Arroyave (2024) "ULTIMATE: BIRDSHOT Final Technical Report" DOE/ARPA-E. doi:10.2172/2305503. 4 citations.
10. Plotkowski et al. (2025) "Additively manufacturing high-temperature aluminum alloy for automotive engine pistons" ORNL DuAlumin-3D. doi:10.2172/2573209.
11. Angelopoulos & Bates (2023) "Conformal prediction: a gentle introduction" *Found. Trends Mach. Learn.* 16:494-591. 2025 citations.
12. Mulukutla et al. (2024) "Supply risk-aware alloy discovery and design" *arXiv* 2409.15391. 1 citation.
13. Hastings et al. (2024) "An interoperable multi-objective batch Bayesian optimization framework for high-throughput materials discovery" *arXiv* 2405.08900. 1 citation.
14. Ge et al. (2025) "High-strength additively manufacturable Al-Zr-Er-Ni alloys with high as-built ductility and thermal stability" *Preprint* doi:10.21203/rs.3.rs-6558867/v1.
15. Arena et al. (2024) "Novel aluminum alloy tailored for additive manufacturing: structural characterization and qualification perspectives" *Applied Sciences* 14:4647.
16. Mehta et al. (2022) "High performance aluminium alloy for additive manufacturing" *Powder Metallurgy* 65:33-36.
17. Biffi et al. (2024) "CuCrZr alloy manufactured by LPBF" — LPBF mechanical/conductivity data.
18. Ferro & Bonollo (2019) "Materials selection in a critical raw materials perspective" *Materials & Design* 177:107848.
19. Czerwinski (2020) "Cerium in aluminum alloys" *Journal of Materials Science* 55:24-72.
20. Sims et al. (2017) "High performance aluminum-cerium alloys for high-temperature applications" *Materials Horizons* 4:1070-1078.
21. Knoop et al. (2020) "A tailored AlSiMg alloy for laser powder bed fusion" *Metals* 10:514.
22. Turner et al. (2021) "Bayesian optimization is superior to random search for machine learning hyperparameter tuning" — Multi-seed BO benchmarking, escalation from 10→30 seeds for robust claims.
23. Daulton et al. (2020) "Differentiable expected hypervolume improvement for parallel multi-objective Bayesian optimization" — qEHVI for explicit multi-objective optimization; 506 citations.
24. Helbig et al. (2021) "An overview of indicator choice and normalization in raw material supply risk assessments" *Resources* 10:79. 50 citations.
25. Helbig et al. (2020) "Supply risk considerations for the elements in nickel-based superalloys" *Resources* 9:106. 25 citations.
26. Asghar et al. (2025) "A novel aluminium alloys design strategy for low usage of critical raw materials" *Int. J. Metalcasting*. 7 citations.
27. Martucci et al. (2023) "Development and characterisation of Al-Mn-Cr-Zr alloys" — Multi-element Al-Mn-Cr-Zr LPBF properties.
28. Scheffler et al. (2022) "FAIR data enabling new horizons for materials research" *Nature* 604:635-642. — FAIR principles for materials data.
29. Hartmann et al. (2023) "Strategic plan: decrease critical minerals waste through enabling advanced manufacturing techniques" DOE/INL. doi:10.2172/2481581.
30. Delgado-Licona & Abolhasani (2023) "Research acceleration in self-driving labs" *Advanced Intelligent Systems*. 71 citations.
