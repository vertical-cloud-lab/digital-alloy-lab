# FLAIME Phase I — Project Metrics (v3: Final, Post-Edison Refinement #2)

*Final version incorporating two rounds of Edison Scientific LITERATURE_HIGH feedback (tasks eb08ff46 and e5f1a050, 2026-04-05). Key v2→v3 changes: throughput raised to ≥200 leveraging LPBF batching (3-4 compositions/build), powder yield revised upward to ≥30-50%, "Discovery Yield" added as headline KPI, quantitative sustainability formulas added (SEC, BTF, SRI), workforce metrics expanded with first-gen/URG tracking and pre/post effect sizes, benchmarking table expanded to 8 platforms.*

---

## Tiered Framework

- **Base** (≥90% confidence): Minimum acceptable for DOE go/no-go
- **Expected** (moderate confidence): Target performance
- **Stretch** (aspirational): Exceptional outcomes

---

## 5 Headline KPIs

| # | KPI | Base | Expected | Stretch |
|:---:|---|---|---|---|
| 1 | **Discovery Yield** (alloys meeting thresholds / total tested) | ≥1.5% | ≥3% | ≥5% |
| 2 | **Throughput** (unique compositions characterized) | ≥125 | ≥200 | ≥300 |
| 3 | **Performance** (alloys with YS≥250 MPa AND EL≥5%) | ≥1 | ≥3 | ≥5 |
| 4 | **Resource Efficiency** (sample efficiency vs random + $/kg tracking + supply risk) | ≥1.5× efficiency, 100% tracked | ≥2×, ≥20% cost savings | ≥3×, ≥40% savings |
| 5 | **Workforce** (students trained, retention, demographics) | 12 trained, ≥75% retention | 12 trained, ≥85% retention, ≥25% first-gen | 12+, ≥95%, longitudinal tracking |

> **Discovery Yield** is the single most memorable metric: It captures BO efficiency, throughput, and performance in one number. Historical random exploration yields <0.5% for new AM alloys; FLAIME targets ≥3%.

> **Data/FAIR** is a cross-cutting enabler supporting all 5 KPIs, not a standalone headline.

---

## Category 1: Throughput & Efficiency

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Unique compositions characterized (9 mo) | ≥125 | ≥200 | ≥300 | Lab inventory |
| Compositions per week (steady state) | ≥5 | ≥8 | ≥12 | Weekly log |
| Compositions per LPBF build (batching) | ≥2 | ≥3 | ≥4 | Build records |
| Best-case pipeline cycle time | ≤5 days | ≤3 days | ≤2 days | Timestamps |
| Median pipeline cycle time | ≤7 days | ≤5 days | ≤4 days | P50 tracker |
| P90 pipeline cycle time | ≤10 days | ≤7 days | ≤5 days | P90 tracker |
| CALPHAD compositions screened | ≥3,000 | ≥5,000 | ≥10,000 | Batch log |
| CALPHAD-to-experiment funnel ratio | ≥10:1 | ≥25:1 | ≥50:1 | Ratio |
| Powder batches atomized | ≥125 | ≥200 | ≥300 | Run log |
| LPBF builds completed | ≥50 | ≥65 | ≥100 | Build log |
| Tensile specimens tested | ≥250 | ≥400 | ≥600 | Test log |

> **Batching basis**: Weaver et al. 2021 demonstrated 24 columns/unit on one LPBF plate; Huang et al. 2021 fit 40 miniature tensile bars per plate. Conservative 3-4 compositions/build × 5 builds/week × ~30 effective weeks = 450-600 theoretical max. Target 200 accounts for ramp-up and failures.

### Go/No-Go Milestones
| Month | Milestone | Target |
|:---:|---|---|
| 2 | First 5 compositions through full pipeline | 5 complete datasets |
| 3 | Batching validated (≥3 compositions/build) | Demonstrated |
| 4 | Steady-state throughput | ≥5 compositions/week |
| 6 | Mid-project inventory + interim BOFN performance | ≥60 compositions, R²≥0.3 |
| 9 | Final inventory + Pareto analysis + discovery yield | ≥125 compositions, yield ≥1.5% |

---

## Category 2: Material Performance

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| **Strength-optimized track** | | | | |
| Best Al-Ce-X YS | ≥250 MPa | ≥300 MPa | ≥350 MPa | ASTM E8/E8M |
| Best Al-Ce-X UTS | ≥350 MPa | ≥450 MPa | ≥500 MPa | ASTM E8/E8M |
| Elongation at high strength | ≥2% | ≥3% | ≥5% | At YS≥300 MPa |
| **Ductility-optimized track** | | | | |
| Best Al-Ce-X elongation | ≥6% | ≥8% | ≥11% | ASTM E8/E8M |
| YS at high ductility | ≥150 MPa | ≥200 MPa | ≥250 MPa | At EL≥8% |
| **Combined** | | | | |
| Alloys with YS≥250 AND EL≥5% | ≥1 | ≥3 | ≥5 | Joint threshold |
| Compositions exceeding AlSi10Mg baseline | ≥5 | ≥12 | ≥20 | Matched conditions |
| Alloy systems explored | ≥2 | ≥3 | ≥4 | Family count |
| Pareto-optimal compositions (YS vs EL) | ≥5 | ≥10 | ≥15 | Replicated, with confidence bounds |
| Specific strength leaders (YS/ρ) | ≥3 | ≥5 | ≥10 | Calculated |
| Qualified-alloy yield rate | ≥3% | ≥5% | ≥10% | Top alloys / total tested |

> **Literature anchors**: Al-8Ce-10Mg: YS=377, UTS=469, EL=1.8% (Liu 2024). Al-10Ce binary: YS=222, EL=10.8% (Zhou 2020). Strength-ductility tradeoff is fundamental.

---

## Category 3: AI/Autonomy Performance

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| BOFN sample efficiency vs random | ≥1.5× | ≥2× | ≥3× | Retrospective |
| Best property at fixed budget vs standard BO | ≥5% better | ≥15% | ≥25% | Ablation study |
| Best property at fixed budget vs cost-unaware BOFN | ≥5% | ≥10% | ≥20% | Ablation |
| Cost-per-qualified-alloy reduction vs manual | Track | ≥20% | ≥40% | Budget tracking |
| Low-cost node utilization (CALPHAD-only decisions) | ≥30% | ≥40% | ≥50% | Decision log |
| Model R² (YS prediction) | ≥0.3 | ≥0.5 | ≥0.7 | Leave-one-out CV |
| Model MAE (YS prediction) | ≤50 MPa | ≤30 MPa | ≤20 MPa | CV |
| Model calibration (uncertainty coverage) | ≥70% | ≥80% | ≥90% | Calibration plot |
| Autonomous decision cycles completed | ≥50 | ≥100 | ≥150 | Iteration log |
| Human intervention rate (trend) | 40%→25% | 30%→15% | 20%→10% | Override tracking |
| Model retraining frequency | Weekly | 2×/week | Daily | Update log |
| Decision traceability | ≥90% | ≥95% | 100% | Audit log |
| Discovery Yield vs random baseline | ≥2× | ≥3× | ≥5× | Yield comparison |

---

## Category 4: Resource Efficiency & Sustainability

| Metric | Base | Expected | Stretch | Formula/Method |
|---|---:|---:|---:|---|
| **Cost tracking** | | | | |
| Compositions with $/kg assigned | 100% | 100% | 100% | Σ(element_price × mass_fraction) |
| Cost-aware ranking in BOFN acquisition | Yes | Yes | Yes | Embedded in p-KGFN |
| Cost per qualified alloy ($/alloy) | Track | Benchmark vs manual | ≥2× efficiency | Program cost / qualified alloys |
| Discovery cost efficiency ($/composition) | Track trend | Downward trend | <$500/composition | Total cost / compositions tested |
| **Supply chain & critical minerals (Topic 3B alignment)** | | | | |
| Supply Risk Index (SRI) | 100% tracked | Minimize across top alloys | Top alloys SRI<0.3 | Σ(HHI_i × mass_fraction_i) |
| **Critical mineral burden reduction** | ≥1 alloy with ≤2 wt% Mg+Sc+REE | ≥3 alloys with ≤2 wt% Mg+Sc+REE | ≥5 alloys + equivalent performance | Composition analysis |
| Critical mineral dependency score | Track | ≤15 wt% Ce in top alloys | Low-Ce alternatives identified | Composition data |
| Ce wt% distribution mapped | Report | Systematic 0–15 wt% | Full composition-property map | |
| **Be-Cu replacement** (stretch) | Feasibility assessed | ≥1 Cu-Cr-Zr composition atomized | Cu-Cr-Zr with YS ≥ Be-Cu baseline | Phase I stretch → Phase II primary |
| **Energy & environment** | | | | |
| Specific Energy Consumption (SEC) atomization | Track | Report kWh/kg deposited | Show improvement | E_total / m_deposited |
| SEC LPBF | Track | Report | Benchmark vs literature | E_total / m_deposited |
| Buy-to-Fly Ratio (BTF) | Track | ≤2.0 | ≤1.5 | m_input / m_final_part |
| Powder waste rate | ≤60% | ≤50% | ≤40% | 1 - (m_usable / m_atomized) |
| Powder recyclability (re-atomization) | Top 10 assessed | 3 re-atomized + reprinted | Composition drift <2% | Experiment |
| Lifecycle CO₂ intensity (estimate) | Estimate model built | Report for all qualified | Show downward trend | Σ(CO2_material + CO2_process - CO2_recycle) |
| Material Utilization Efficiency | Track | ≥25% | ≥40% | m_final_part / m_feedstock_produced |
| Energy Return on Research Investment (ERORI) | Estimate model | Report for top alloys | Show positive return | Projected savings / discovery energy |
| Performance-per-cost index (UTS/$/kg) | Report top 20 | Top 5 exceed AlSi10Mg | Top 5 Pareto leaders | UTS × density / raw_material_$/kg |

> **Key formulas**: SEC = E_total / m_deposited (kWh/kg). BTF = m_input / m_final. SRI = Σ(HHI_i × wt%_i). LPBF energy ~15-100 MJ/kg (Kellens 2017). Al atomization ~7-42 MJ/kg (Yadegari 2025).

---

## Category 5: Workforce Development

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Total students trained | 12 | 12 | 12+ | Roster |
| Training hours logged | ≥400 | ≥600 | ≥800 | Training log |
| Cross-trained on ≥2 nodes | ≥6 | ≥8 | ≥10 | Records |
| Student co-authored outputs | ≥1 | ≥2 | ≥4 | Publications |
| Student-led presentations/posters | ≥1 | ≥3 | ≥5 | Conference records |
| Pre/post skills assessment (Cohen's d) | Documented | d≥0.5 | d≥1.0 | Validated Likert instrument |
| Student retention (9 months) | ≥75% | ≥85% | ≥95% | HR records |
| First-generation student participation | Report | ≥25% | ≥30% | Demographics |
| URG representation | Report | ≥20% | Match national ASEE benchmarks | Demographics |
| EPSCoR jurisdiction participation | Report | Document | ≥1 from EPSCoR state | Roster |
| STEM degree completion (tracked) | Report | ≥80% | ≥90% | 2-year follow-up |
| Graduate school placement rate | Report | ≥30% | ≥50% | 2-year follow-up |
| Longitudinal career tracking initiated | No | Yes (3-year plan) | Active tracking | LinkedIn/Scholar |
| Students producing public artifacts | ≥2 | ≥4 | ≥8 | Talks, posters, code |

---

## Category 6: Data Infrastructure & FAIR

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| FAIR structured database (all 4 nodes) | 1 database | 1 + public release | 1 + DOI + schema | Database/Zenodo |
| Data completeness (Tier 1: density+hardness+comp) | ≥85% | ≥90% | ≥95% | Audit |
| Data completeness (Tier 2: full tensile+SEM) | ≥50% | ≥70% | ≥85% | Audit |
| Schema compliance rate | ≥85% | ≥95% | 100% | Validation |
| Data latency (measurement → database) | ≤48 hr | ≤24 hr | ≤4 hr | Timestamps |
| Metadata capture rate | ≥90% | ≥95% | 100% | Automated |
| Journal publications submitted | ≥1 | ≥1 | ≥2 | Records |
| Open-source code releases | ≥1 | ≥1 + examples | ≥1 + docs + schema | GitHub |
| Decision traceability (AI logged with rationale) | 100% | 100% | 100% | Audit |

> **Tiered data completeness**: Tier 1 (screening) = density + hardness + composition. Tier 2 (confirmation) = full tensile + SEM/EDS/EBSD. This resolves the throughput vs quality tension: maintain ≥85% Tier 1 completeness while being selective for Tier 2.

---

## Category 7: Process Quality

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Powder yield 15–63 μm (LPBF-usable) | ≥25% | ≥35% | ≥50% | PSD analysis |
| Powder sphericity (mean + distribution) | ≥0.82 | ≥0.85 | ≥0.90 | Image analysis |
| LPBF relative density (screening gate) | ≥97% | ≥98% | ≥99% | Archimedes |
| LPBF relative density (down-selected) | ≥98.5% | ≥99% | ≥99.5% | Archimedes |
| Tensile replicate variability (CoV YS) | ≤15% | ≤10% | ≤7% | Statistical |
| Build success rate (novel compositions) | ≥65% | ≥75% | ≥85% | Build log |
| Build success rate (baseline/control) | ≥85% | ≥90% | ≥95% | Build log |
| Atomization success rate | ≥80% | ≥85% | ≥95% | Run log |

> **Powder yield basis**: Ge et al. 2025 report 40-70% yield for rePOWDER Al alloys. Yankin et al. 2025 report ~75% <63μm for AlSi12. Our 25-50% target is conservative.

---

## Category 8: Scalability & Transferability

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Time to onboard new alloy family | ≤6 weeks | ≤4 weeks | ≤2 weeks | Al-Cu-X after Al-Ce-X |
| Workflow reuse on family switch | ≥60% | ≥75% | ≥90% | Code audit |
| API/schema alloy-agnostic interfaces | Document | All 4 nodes | Tested with 2nd system | Audit |
| Platform autonomy level (start→end) | Level 2→2 | Level 2→3 | Level 2→4 | SDL framework |
| Acceleration factor vs manual | ≥2× | ≥3× | ≥5× | Time comparison |
| Reuse fraction on system switch | ≥50% | ≥75% | ≥90% | Architecture audit |

---

## Category 9: Benchmarking vs State-of-the-Art

| Platform | Domain | Throughput | Automation | Loop Closure | Mechanical Testing? | Key Ref |
|---|---|---|---|---|---|---|
| **FLAIME** (proposed) | Metal AM (Al alloys) | ~200 comp/9mo | Semi-autonomous | Closed (BOFN) | ✅ ASTM E8 tensile | This proposal |
| A-Lab (Berkeley) | Inorganic synthesis | 2.4 mat/day | Fully autonomous | Closed | ❌ XRD only | Szymanski 2023, *Nature* |
| ORNL MDF | Nuclear AM | ~10-20/yr | Manual + HT char | Open | Partial | ORNL AMMT reports |
| HT-READ (UCSD) | Combinatorial alloys | ~100+ comp/campaign | Semi-automated | Open | ✅ Mini-tensile | Vecchio 2021, *Acta Mat* |
| BEAR System | Polymer AM (FDM) | Per-build optimization | Fully autonomous | Closed (BO) | ✅ Tensile | Doloi 2025, *Digital Discovery* |
| PolyBot | Polymer synthesis | Batch optimization | Fully autonomous | Closed (BO) | ❌ | Tom 2024, *Chemical Reviews* |
| ARES (AFRL) | Polymer/carbon | Continuous | Fully autonomous | Closed (BO) | ❌ | Maruyama group |
| LDED gradient | Multi-alloy AM | 80-200+ comp/build | Semi-automated | Open | Partial | Liu 2024, *MGEA* |
| Manual lab | Any AM alloy | 2-4 comp/month | Manual | None | ✅ | Baseline |

> **FLAIME's unique differentiator**: First closed-loop SDL integrating powder production + LPBF printing + full mechanical testing in a single autonomous decision loop. No published system achieves this.

---

## Edison Scientific Task References

| Query | Task ID | Job Type | Key Findings |
|---|---|---|---|
| Metrics critique #1 | `eb08ff46` | LITERATURE_HIGH | Throughput 2× too aggressive, split strength/ductility targets, add 25+ metrics, tiered framework |
| Metrics critique #2 | `e5f1a050` | LITERATURE_HIGH | LPBF batching enables ≥200, raise powder yield target, Discovery Yield as headline, quantitative sustainability formulas, workforce gaps |
