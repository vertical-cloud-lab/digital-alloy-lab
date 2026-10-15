# Pareto Front Analysis: Additively Manufactured Aluminum Alloys

*Compiled from 50 Edison Scientific LITERATURE queries across 5 batches*

## Executive Summary

This analysis identifies Pareto-optimal AM aluminum alloys across multiple property axes using quantitative data extracted from peer-reviewed literature (2017–2026). The primary Pareto fronts examined are:

1. **Strength–Ductility** (YS or UTS vs. elongation)
2. **Strength–Thermal Stability** (RT strength vs. strength retention at 250–300°C)
3. **Strength–Fatigue Life** (UTS vs. fatigue limit at 10⁷ cycles)
4. **Strength–Cost** (specific strength vs. powder/process cost)
5. **Printability–Properties** (process window width vs. mechanical performance)

---

## 1. Strength–Ductility Pareto Front

### Ranked by Strength–Ductility Index (SDI = UTS × Elongation)

| Rank | Alloy System | AM Process | Condition | UTS (MPa) | Elong. (%) | SDI | Source |
|---:|---|---|---|---:|---:|---:|---|
| 1 | Al-Mg-Si-Sc-Zr | LPBF | Optimized high-ductility | 376 | 35.0 | 13,160 | li2020developingahighstrength pp. 13–14 |
| 2 | Zr-modified AA6061 | LPBF | As-built | 268 | 26.5 | 7,102 | mehta2021additivemanufacturingand pp. 9–10 |
| 3 | Al-Mg-Sc-Zr (Scalmalloy-type) | LPBF | Aged 330°C × 1h | 479 | 14.5 | 6,946 | shen2021effectofheat pp. 9–10 |
| 4 | A20X (Al-Cu-Mg + TiB₂) | LPBF | T6 | 486 | 14.0 | 6,797 | belelli2021investigationontwo pp. 9–12 |
| 5 | A2024-CaB₆ | LPBF | As-built | 478 | 13.2 | 6,310 | mair2022dependenceofmechanical pp. 8–9 |
| 6 | Scalmalloy (Al-Mg-Sc-Zr) | LPBF | As-built, optimized | 415 | 14.8 | 6,142 | ekubaru2022excellentstrength pp. 11–12 |
| 7 | Al-Mg-Si-Sc-Zr | LPBF | As-printed, high-strength | 497 | 11.0 | 5,467 | li2020developingahighstrength pp. 13–14 |
| 8 | Al-Zn-Mg-Cu + 5%Si (7075+Si) | LPBF | As-printed | 537 | 9.7 | 5,209 | dixit2022laseradditivemanufacturing pp. 15–16 |
| 9 | Tailored AlSi3.5Mg2.5 | LPBF | Direct aged | 484 | 10.5 | 5,082 | knoop2020atailoredalsimg pp. 10–12 |

**Source keys** reference the Edison LITERATURE citation IDs from Query 10 in `batch1_core_mechanical.md`.

### Key Observations
- **Al-Mg-Si-Sc-Zr** systems dominate the Pareto front due to exceptional ductility (>30%) with moderate strength
- **Scalmalloy-type alloys** offer the best balance in the high-strength regime (UTS > 450 MPa, EL > 14%)
- **AlSi10Mg** (the most common LPBF Al alloy) is NOT on the Pareto front: typical SDI ≈ 2,000–2,700 (UTS 340–465 MPa, EL 4–6% as-built)
- **2xxx/7xxx-based** alloys achieve high UTS (>500 MPa) but with lower ductility (<10%), placing them below the Pareto front

### Property Ranges by Alloy Family

| Alloy Family | YS (MPa) | UTS (MPa) | Elong. (%) | Best Condition |
|---|---|---|---|---|
| AlSi10Mg | 180–314 | 254–469 | 0.7–11.7 | As-built or T5 |
| Scalmalloy (Al-Mg-Sc-Zr) | 287–572 | 390–530 | 7–18 | Aged 300–350°C |
| 2xxx (Al-Cu) | 180–400 | 300–485 | 3–14 | T6 or grain-refined |
| 7xxx (Al-Zn-Mg-Cu) | 200–530 | 350–600 | 2–12 | T6 with Si/Zr modification |
| Al-Ce | 150–268 | 200–350 | 8–25 | As-built (thermally stable) |
| Al-Mn-Sc-Zr | 400–572 | 450–530 | 7–14 | Aged 300°C |
| Al-Fe-V-Si | 280–350 | 400–454 | 2–8 | As-built |
| A20X (Al-Cu-Ti-B) | 300–430 | 400–486 | 5–14 | T6 |
| Hypereutectic Al-Si (>12%Si) | 200–350 | 300–450 | 1–5 | As-built (wear-resistant) |

---

## 2. Strength–Thermal Stability Pareto Front

### Yield Strength at Elevated Temperature

| Rank | Alloy System | RT YS (MPa) | YS at 250°C (MPa) | Retention | YS at 300°C (MPa) | Retention |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Al-Mn-Sc | 572 | ~245 | 43% | ~178 | 31% |
| 2 | Al-Cu-Mn-Zr (Al-9Cu) | — | ~180 | — | ~130 | — |
| 3 | Al-10Ce-8Mn | 268 | ~110 | 41% | ~90 | 34% |
| 4 | Al-Fe-V-Si | — | N/R | — | N/R | — |

### Key Observations
- **Al-Mn-Sc** achieves the highest absolute strength at temperature due to thermally stable Al₃(Sc,Zr) precipitates
- **Al-Ce alloys** offer excellent thermal stability (high retention ratio) but lower absolute strength
- **AlSi10Mg** loses strength rapidly above 200°C due to Si network coarsening
- **Al-Fe-V-Si** has promising thermodynamics but lacks AM-specific high-T tensile data

---

## 3. Fatigue Performance (Mixed Test Conditions)

### Reported Fatigue Strength Values

| Alloy System | Condition | Fatigue Strength (MPa) | R-ratio | Runout/Criterion | Notes |
|---|---|---:|---|---|---|
| AlSi10Mg | As-built, machined/polished | 125 | R=−1 | 10⁷ cycles | Rotating beam |
| AlSi10Mg | Heat-treated (T6) | ~80 | R=−1 | Basquin extrapolation | Axial |
| AlSi10Mg | As-built, not machined | ~50 | R=−1 | 10⁷ cycles | Axial |
| AlSi10Mg | HIPed, machined | N/A | — | — | +14% vs as-built; normalized to UTS |
| Scalmalloy | Untreated | 51.6 | Not specified | Cited value | From FCG study |
| Scalmalloy | Aged | 126.4 | Not specified | Cited value | Al₃(Sc,Zr) strengthened |
| Al-Mn-Sc-Zr | Direct aged | ~180–220 | Not specified | S-N data | S-N data reported |
| Al-Mn-Sc-Zr | HIPed | 340 | Not specified | Model-derived | Defect-size model applied |

### Key Observations
- **Surface condition** is the dominant factor for AlSi10Mg fatigue (machined vs as-built: 125 vs ~50 MPa)
- **Al-Mn-Sc-Zr with HIP** achieves the highest reported fatigue strength (340 MPa) among LPBF Al alloys
- **Scalmalloy after aging** matches machined AlSi10Mg fatigue performance (~126 MPa)

---

## 4. Fracture Toughness

| Alloy System | Condition | KIC or Equivalent (MPa√m) | Notes |
|---|---|---:|---|
| AlSi10Mg | As-built | 20–35 | Orientation-dependent |
| AlSi10Mg | T6/HIP | 25–42 | Improved with ductility gains |
| Scalmalloy | Aged | 25–40 | Limited data |
| Al-Cu (2xxx) | T6 | 20–30 | Crack-free samples required |
| Al-Ce | As-built | 15–25 | Thermally stable |

---

## 5. Hardness Rankings

### Peak Hardness Values by Alloy System (Vickers)

| Alloy System | Condition | Peak HV | Notes |
|---|---|---:|---|
| Al-Zn-Mg-Cu-Zr (7xxx) | T6 | 218 ± 11 | Highest reported LPBF Al |
| AlCe10MgSi | As-built, high VED | 214 ± 12 | Strong intermetallic contribution |
| Al-15%Fe | As-built | ~210 | Hypereutectic, Al₁₃Fe₄ |
| AlSi10Mg + 4Cu | Peak aged | >180 | Cu addition raises peak |
| Scalmalloy | Direct aged | 170 ± 10 | Al₃(Sc,Zr) precipitates |
| Al-Zn-Mg-Cu + 5%Si | Aged 160°C/6h | 153 | Si-modified 7075 |
| AlSi10Mg | As-built (optimized) | 136–144 | Scan-strategy dependent |
| 2024 + LaB₆ | As-built | 135 | Grain-refined |

---

## 6. Corrosion Resistance

- **AlSi10Mg (LPBF)** shows *improved* corrosion resistance vs cast A360/A380 due to refined Si network
- **Heat treatment (T6)** of AlSi10Mg *degrades* corrosion resistance (Si network coarsens → galvanic coupling)
- **Al-Ce alloys** expected to have good corrosion resistance (Ce intermetallics are cathodic but not as galvanically active as Cu-containing phases)
- **2xxx/7xxx alloys** remain susceptible to intergranular/pitting corrosion in AM form, similar to wrought

---

## 7. Printability Rankings

### Process Window and Cracking Susceptibility

| Alloy System | Printability | Cracking Risk | Best Grain Refiner | Max Density (%) |
|---|---|---|---|---:|
| AlSi10Mg | Excellent | Very low (eutectic) | None needed | >99.8 |
| Scalmalloy | Good | Low (fine grains) | Inherent Sc/Zr | >99.5 |
| Al-Ce | Good | Low (eutectic) | None needed | >99.5 |
| 2xxx (Al-Cu) | Poor→Good | High→Low | TiB₂, CaB₆, ZrH₂ | >99.5 with refiners |
| 7xxx (Al-Zn-Mg-Cu) | Poor→Moderate | High→Moderate | Si addition, Zr, TiB₂ | >99.0 with modification |
| Al-Fe-V-Si | Moderate | Moderate | — | >99.0 |
| Al-Mn-Sc-Zr | Good | Low | Inherent Sc/Zr | >99.5 |

### Key Findings
- **Eutectic and near-eutectic** compositions (AlSi10Mg, Al-Ce, hypereutectic Al-Si) have the widest process windows
- **Grain refiners** (TiB₂ 1–4 vol%, ZrH₂, CaB₆) are critical for crack-free 2xxx/7xxx printing
- **VED ranges**: AlSi10Mg 50–80 J/mm³; Scalmalloy 80–200 J/mm³; 2xxx 80–150 J/mm³; 7xxx 100–200 J/mm³

---

## 8. Cost–Performance Tradeoffs

| Alloy System | Approx. Powder Cost ($/kg) | Printability | Peak UTS (MPa) | Cost-Performance Tier |
|---|---:|---|---:|---|
| AlSi10Mg | 30–60 | Excellent | 469 | Best value |
| A20X | 50–100 | Good | 486 | Good value |
| Scalmalloy | 150–400 | Good | 530 | Premium |
| Custom Al-Mn-Sc-Zr | 200–500 | Good | 530 | Premium |
| 2xxx + grain refiners | 60–150 | Moderate | 478 | Moderate |
| 7xxx + Si modification | 80–200 | Moderate | 600 | Moderate–Premium |
| Al-Ce | 80–200 | Good | 350 | Niche (thermal) |

---

## 9. Multi-Objective Pareto Summary

### Identified Pareto-Optimal Alloys by Application

| Application Requirement | Pareto-Optimal Alloy(s) | Key Property | Trade-off |
|---|---|---|---|
| **General structural** | AlSi10Mg | Cost, printability | Lower strength |
| **High strength + ductility** | Al-Mg-Si-Sc-Zr, Scalmalloy | SDI > 6,000 | High powder cost |
| **Maximum strength** | 7xxx + Si, Al-Cu-Mn-Zr | UTS > 500 MPa | Printability, ductility |
| **High temperature** | Al-Mn-Sc, Al-Ce, Al-Cu-Mn-Zr | Retention at 300°C | Cost (Sc), strength (Ce) |
| **Fatigue-critical** | Al-Mn-Sc-Zr + HIP | 340 MPa fatigue | Cost, processing |
| **Wear resistance** | Hypereutectic Al-Si | High hardness, low CoF | Low ductility |
| **Thermal management** | AlSi10Mg (HT), Al-Ce | High λ after T6 | Strength reduction |
| **Minimum cost** | AlSi10Mg | $30–60/kg powder | Limited max properties |

---

## 10. Key Gaps Identified

1. **Fatigue data** for most alloys beyond AlSi10Mg is sparse; S-N curves needed for Scalmalloy, Al-Ce, 7xxx
2. **Elevated temperature data** for Al-Fe-V-Si in AM is nearly absent despite promising thermodynamics
3. **Fracture toughness** measurements are limited; most alloys lack KIC values
4. **Cost data** is poorly documented in literature; powder costs are estimates
5. **Multi-property Pareto studies** are rare; only Zhu 2022 (energy vs strength for AlSi10Mg) provides explicit Pareto fronts
6. **Creep data** for AM Al alloys is extremely limited
7. **Corrosion data** is mostly limited to AlSi10Mg; other systems lack electrochemical characterization
8. **Size effects** on mechanical properties are understudied for most alloy systems

---

## References

All data extracted from Edison Scientific LITERATURE searches across 50 queries in 5 batches:
- **Batch 1**: Core mechanical properties (YS, UTS, elongation) by alloy system
- **Batch 2**: Additional mechanical properties (fatigue, fracture toughness, hardness, creep, wear, etc.)
- **Batch 3**: Process-property relationships, corrosion, printability, computational design
- **Batch 4**: DED/WAAM, microstructure-property, anisotropy, emerging systems
- **Batch 5**: Pareto synthesis, standards, sustainability, high-temperature applications

Individual query results with full citations are in the companion batch files:
- `batch1_core_mechanical.md`
- `batch2_additional_mechanical.md`
- `batch3_process_property.md`
- `batch4_microstructure_emerging.md`
- `batch5_pareto_synthesis.md`
