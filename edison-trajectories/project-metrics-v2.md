# FLAIME Phase I — Project Metrics (v2: Post-Edison Refinement #1)

*Refined based on Edison Scientific LITERATURE_HIGH feedback (task eb08ff46, 2026-04-05). Key changes: throughput targets reduced ~2× per LPBF bottleneck analysis, tiered metric framework adopted, strength-ductility targets separated, 25+ new metrics added for workforce, sustainability, digital thread, and benchmarking.*

---

## Tiered Framework

All metrics use three tiers:
- **Base** (≥90% confidence): Minimum acceptable for DOE go/no-go
- **Expected** (moderate confidence): Target performance level
- **Stretch** (aspirational): Demonstrates exceptional outcomes

---

## Category 1: Throughput & Efficiency

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Unique compositions synthesized (9 mo) | ≥100 | ≥175 | ≥250 | Lab inventory count |
| Compositions per week (steady state) | ≥5 | ≥8 | ≥12 | Weekly throughput log |
| Full pipeline cycle time (best case) | ≤5 days | ≤3 days | ≤2 days | Timestamped workflow |
| Median pipeline cycle time | ≤7 days | ≤5 days | ≤4 days | P50 from tracker |
| P90 pipeline cycle time | ≤10 days | ≤7 days | ≤5 days | P90 from tracker |
| CALPHAD compositions screened | ≥2,000 | ≥5,000 | ≥10,000 | Thermo-Calc batch log |
| CALPHAD-to-experiment funnel ratio | ≥5:1 | ≥15:1 | ≥30:1 | Screened / synthesized |
| Powder batches atomized | ≥100 | ≥175 | ≥250 | Atomization run log |
| LPBF builds completed | ≥100 | ≥175 | ≥225 | Build log at U of U |
| Tensile specimens tested | ≥200 | ≥350 | ≥500 | Testing log (tiered replication) |

> **Replication protocol**: 1 specimen for screening, 2 for confirmation, 3–5 for top candidates.

### Go/No-Go Milestones
| Month | Milestone | Minimum Target |
|:---:|---|---|
| 2 | First 5 compositions through full pipeline | 5 complete datasets |
| 4 | Steady-state throughput demonstrated | ≥5 compositions/week |
| 6 | Mid-project inventory | ≥50 compositions tested |
| 9 | Final inventory | ≥100 compositions + Pareto analysis |

---

## Category 2: Material Performance

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| **Strength-optimized track** | | | | |
| Best Al-Ce-X YS | ≥250 MPa | ≥300 MPa | ≥350 MPa | ASTM E8/E8M |
| Best Al-Ce-X UTS | ≥350 MPa | ≥450 MPa | ≥500 MPa | ASTM E8/E8M |
| Elongation at high strength | ≥2% | ≥3% | ≥5% | At YS ≥300 MPa |
| **Ductility-optimized track** | | | | |
| Best Al-Ce-X elongation | ≥6% | ≥8% | ≥11% | ASTM E8/E8M |
| YS at high ductility | ≥150 MPa | ≥200 MPa | ≥250 MPa | At EL ≥8% |
| **Combined targets** | | | | |
| Best joint (YS ≥250 AND EL ≥5%) | ≥1 alloy | ≥3 alloys | ≥5 alloys | Joint threshold |
| Compositions exceeding AlSi10Mg baseline | ≥5 | ≥10 | ≥20 | Matched conditions |
| Alloy systems explored | ≥2 | ≥3 | ≥4 | Family count |
| Pareto-optimal compositions (YS vs EL) | ≥5 | ≥10 | ≥15 | Replicated Pareto front |
| Specific strength leaders (YS/density) | ≥3 | ≥5 | ≥10 | Calculated from data |

> **AlSi10Mg baseline**: Compositions exceeding baseline on YS, UTS, and/or specific strength under matched build and test conditions.

---

## Category 3: AI/Autonomy Performance

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| BOFN sample efficiency vs random | ≥1.5× | ≥2× | ≥3× | Retrospective comparison |
| Best property at fixed budget vs standard BO | ≥5% improvement | ≥15% | ≥25% | Matched-budget ablation |
| Cost-per-qualified-alloy reduction vs manual | Track | ≥20% savings | ≥40% savings | Budget tracking |
| Cost-aware low-node decisions (% using CALPHAD screen only) | ≥30% | ≥40% | ≥50% | Decision log |
| Model prediction accuracy R² (YS) | ≥0.4 | ≥0.5 | ≥0.7 | Leave-one-out CV |
| Model prediction MAE (YS) | ≤40 MPa | ≤30 MPa | ≤20 MPa | Cross-validation |
| Autonomous decision cycles completed | ≥50 | ≥100 | ≥150 | Iteration log |
| Human intervention rate (start → end trend) | ≤40% → ≤25% | ≤30% → ≤15% | ≤20% → ≤10% | Override tracking |
| Model retraining frequency | Weekly | 2×/week | Daily | Update log |
| Decision traceability score | ≥90% | ≥95% | 100% | Audit log coverage |

---

## Category 4: Sustainability & Cost Awareness

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Compositions with $/kg cost assigned | 100% | 100% | 100% | Cost calculation |
| Cost-aware ranking used in acquisition function | Yes | Yes | Yes | BOFN config |
| Supply risk score assigned (DOE/USGS criticality) | 100% of tested | 100% | 100% | Criticality index |
| Critical mineral dependency score | Track | Minimize Ce dependency variants | Top alloys use ≤15 wt% Ce | Composition data |
| Performance-per-cost index (UTS/$/kg) | Report top 20 | Identify top 5 leaders | Top 5 exceed AlSi10Mg | Multi-objective analysis |
| Compositions on performance–cost Pareto front | ≥3 | ≥5 | ≥10 | YS/EL/cost front |
| Ce wt% distribution across tested alloys | Report | Show systematic variation | Full mapping 0–15 wt% | Composition records |
| Powder waste rate | Track | ≤50% waste | ≤40% waste | Mass balance per batch |
| Powder recyclability screening | Top 10 alloys | Top 10 + re-atomization test for 3 | Re-atomize + reprint 3 | Experiment log |
| Carbon footprint per qualified composition (est.) | Estimate model | Report for all qualified | Show downward trend | Energy + mass model |
| Cost per qualified alloy ($/alloy) | Track | Benchmark vs manual | Demonstrate ≥2× efficiency | Budget analysis |
| Energy per successful qualified alloy | Track | Report for top 20 | Show improvement trend | Process monitoring |

---

## Category 5: Workforce Development

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Total students trained | 12 | 12 | 12+ (include rotation students) | Roster |
| Total training hours logged | ≥400 | ≥600 | ≥800 | Training log |
| Students cross-trained on ≥2 pipeline nodes | ≥6 | ≥8 | ≥10 | Cross-training records |
| Student co-authored publications/outputs | ≥1 | ≥2 | ≥4 | Publication records |
| Student-led presentations/posters | ≥1 | ≥3 | ≥5 | Conference records |
| Skills assessment pre/post documented | 100% | 100% | 100% | Assessment forms |
| Student retention through project end | ≥75% | ≥85% | ≥95% | HR records |
| Conference presentations (total) | ≥1 | ≥2 | ≥4 | Abstract records |
| Workforce diversity (report) | Report | Report | Report | Demographics |

---

## Category 6: Data & Dissemination

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| FAIR structured database (all 4 nodes) | 1 database | 1 + public release | 1 + DOI + schema docs | Database/Zenodo |
| Data completeness (% compositions with full chain) | ≥70% | ≥85% | ≥95% | Database audit |
| Schema compliance rate | ≥85% | ≥95% | 100% | Validation scripts |
| Data latency (measurement → database) | ≤48 hours | ≤24 hours | ≤4 hours | Timestamp audit |
| Metadata capture rate | ≥90% | ≥95% | 100% | Automated metadata |
| Journal publications submitted | ≥1 | ≥1 | ≥2 | Submission records |
| Open-source code releases | ≥1 | ≥1 + examples | ≥1 + docs + schema | GitHub release |
| Decision traceability (AI recommendations logged) | 100% | 100% | 100% | Audit log |

---

## Category 7: Process Quality

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Powder yield in 15–63 μm (LPBF-usable) | ≥20% | ≥25% | ≥35% | PSD analysis |
| Powder sphericity (mean) | ≥0.82 | ≥0.85 | ≥0.90 | Image analysis (distribution) |
| LPBF relative density (down-selected alloys) | ≥98.5% | ≥99% | ≥99.5% | Archimedes method |
| LPBF screening gate density | ≥97% | ≥98% | ≥99% | Archimedes |
| Tensile replicate variability (CoV YS) | ≤15% | ≤10% | ≤7% | Statistical analysis |
| Build success rate (novel compositions) | ≥65% | ≥75% | ≥85% | Build log |
| Build success rate (baseline/control) | ≥85% | ≥90% | ≥95% | Build log |
| Atomization success rate | ≥80% | ≥85% | ≥95% | Run log |

---

## Category 8: Scalability & Transferability

| Metric | Base | Expected | Stretch | Measurement |
|---|---:|---:|---:|---|
| Time to onboard new alloy family | ≤6 weeks | ≤4 weeks | ≤2 weeks | Measured for Al-Cu-X after Al-Ce-X |
| Workflow reuse fraction on family switch | ≥60% | ≥75% | ≥90% | Code/pipeline audit |
| API/schema alloy-agnostic interfaces | Document | All 4 nodes documented | Tested with 2nd system | Interface audit |
| Platform autonomy level (self-assessed) | Level 2 | Level 3 | Level 4 | SDL autonomy framework |
| Acceleration factor vs manual workflow | ≥2× | ≥3× | ≥5× | Time comparison |

---

## Category 9: Benchmarking vs State-of-the-Art

| Metric | FLAIME (Expected) | A-Lab | ORNL MDF | Manual Lab | Source |
|---|---|---|---|---|---|
| Compositions per month | ~20 | ~72 (powder synth only) | ~7 LPBF builds | ~2–4 | Edison analysis |
| Cost per composition | ~$100–200 | ~$50 (no AM) | ~$1,000+ | ~$500–1,000 | Budget model |
| Full pipeline (powder→part→test) | Yes | No (synth only) | Partial | Yes (slow) | Workflow scope |
| Autonomous decision loop | Yes (BOFN) | Yes (synthesis) | No | No | Architecture |
| Time-to-discovery (novel alloy) | ~1–2 weeks | ~hours (different modality) | ~months | ~months | Cycle time |
| Discovery rate (compositions/$100K) | ~25–35 | ~100+ (different modality) | ~5–10 | ~3–8 | Budget model |

---

## Headline KPIs (for Executive Summary)

1. **Throughput**: ≥175 unique alloy compositions discovered in 9 months (≥3× manual workflow)
2. **Performance**: ≥1 alloy with YS ≥250 MPa AND EL ≥5% (strength-ductility breakthrough)
3. **Efficiency**: ≥2× sample efficiency vs random search, ≥20% cost savings from cost-aware BOFN
4. **Sustainability**: 100% of compositions assigned $/kg cost + supply risk score, integrated into acquisition
5. **Data**: FAIR database spanning all 4 nodes with ≥85% data completeness
6. **Workforce**: 12 students trained across ≥2 pipeline nodes, ≥85% retention
