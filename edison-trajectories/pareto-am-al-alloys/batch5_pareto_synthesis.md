# Batch 5: Pareto Analysis, Standards, Sustainability, High-Temp Applications

*Edison Scientific LITERATURE queries for AM Al alloy Pareto front identification*

## Query 1

**Question:** What explicit Pareto front or multi-objective optimization studies exist for additively manufactured aluminum alloys? Provide examples of strength-ductility, strength-thermal stability, or cost-performance Pareto analyses with quantitative data points.

**Task ID:** `e2d15346-d2c5-489e-89a9-939b66b8df97`

**Status:** complete

This review scoped *explicit* Pareto-front or multi-objective optimization (MOO) studies where the material is an additively manufactured aluminum alloy and the tradeoff is reported as a Pareto front or non-dominated solution set with quantitative coordinates.

| Study (author, year) | AM process & alloy | Objective axes (with units) | Optimization method | Where Pareto shown | Example quantitative Pareto points | Notes/limitations |
|---|---|---|---|---|---|---|
| Zhu et al., 2022 | SLM / LPBF of AlSi10Mg | Energy consumption (MJ) vs tensile strength (MPa) | NSGA-II | Explicit Pareto front in Fig. 12; representative Pareto solutions in Table 8 | S1-No.1: 83.2 MJ, 427.7 MPa; S1-No.2: 84.7 MJ, 440.8 MPa; S1-No.3: 87.7 MJ, 451.7 MPa. Process settings respectively: (343 W, 900 mm/s, overlap 0.25, hatch 86 µm), (320 W, 830 mm/s, 0.25, 86 µm), (320 W, 642 mm/s, 0.25, 100 µm). Single-objective comparison points reported: min-energy S2 = 95 MJ, 413.4 MPa; max-strength S3 = 104 MJ, 453.2 MPa; manufacturer setting S4 = 90 MJ, 440.0 MPa. (zhu2022multiobjectiveoptimizationof pages 15-17, zhu2022multiobjectiveoptimizationof media 660e21aa, zhu2022multiobjectiveoptimizationof media 55d34c7a) | This is the clearest explicit Pareto-front study in the current AM-Al evidence set, and it is a cost/performance-style tradeoff (energy vs strength), not strength–ductility. |
| Ince et al., 2024 | LPBF of Al6061 | Relative porosity / porosity (%) vs relative crack density / crack density (units not clearly specified in excerpt) | MATLAB MOGA (`gamultiobj`) and `paretosearch` | Pareto optimization is explicitly formulated; provided excerpts do not show tabulated Pareto-point coordinates | Example run values from Table 2 / text: 190 W, 100 mm/s, h = 0.1 mm → porosity 3.35, crack 0.70; 200 W, 100 mm/s, h = 0.1 mm → porosity 0.60, crack 0.23; 275 W, 400 mm/s, h = 0.1 mm → porosity 0.70, crack 2.01. Additional reported trend: porosity decreased from 10.42% to 1.58% when hatch spacing increased from 0.06 to 0.10 mm under one parameter set. (ince2024anexperimentalprocess pages 5-6, ince2024anexperimentalprocess pages 8-9, ince2024anexperimentalprocess pages 6-8) | Explicit bi-objective tradeoff study for AM Al, but the accessible pages do not provide confirmed non-dominated coordinates; example values are experimental tradeoff points, not verified Pareto-front points. This is a quality/defect tradeoff rather than strength–ductility or cost–performance. |
| Taheri-Mousavi et al., 2024 | Alloy design for AM high-strength Al alloy (printable Al-Er-Zr-Y-Yb-Ni-type design space; AM-focused alloy design workflow) | Composite printability / thermal-stability objectives (e.g., coarsening metric, L1\_2 fraction metrics, crack-susceptibility-related printability metrics); no explicit strength–ductility or strength–thermal-stability Pareto axes plotted in provided pages | Bayesian optimization with composite objectives | No explicit Pareto front or non-dominated table in the provided pages | Reported outcome metrics instead of Pareto points: ~40% enhancement in L1\_2 at.% and 3.5× reduction in coarsening metric vs benchmark; as-built hardness ~180 HV; ~50% higher hardness than benchmark at peak aging; ~50% higher yield strength vs benchmark alloy, with improved hardness retention during 400 °C aging. (taherimousavi2024additivelymanufacturablehighstrength pages 7-9, taherimousavi2024additivelymanufacturablehighstrength pages 12-15, taherimousavi2024additivelymanufacturablehighstrength pages 1-4) | Useful contrast case: clearly multi-objective/inverse design for AM Al with thermal-stability intent, but not an explicit Pareto-front paper in the provided text. Therefore it should not be counted as an explicit strength–thermal-stability Pareto analysis unless supplementary figures reveal such a frontier. |


*Table: This table summarizes the additively manufactured aluminum alloy studies in the current evidence that use explicit multi-objective or Pareto-style optimization. It distinguishes papers with true quantitative Pareto points from those that only formulate multi-objective tradeoffs without tabulated non-dominated solutions.*

## 1) Cost/performance-type Pareto: energy consumption vs tensile strength (SLM AlSi10Mg)
Zhu et al. perform NSGA-II MOO for SLM (LPBF/SLM) AlSi10Mg with two objectives: **minimize energy consumption (MJ)** and **maximize tensile strength (MPa)**, and explicitly plot the Pareto front (their Fig. 12) and tabulate representative Pareto solutions (their Table 8). (zhu2022multiobjectiveoptimizationof pages 15-17, zhu2022multiobjectiveoptimizationof media 660e21aa, zhu2022multiobjectiveoptimizationof media 55d34c7a)

Representative *Pareto (non-dominated) points* reported (Energy, Tensile strength) include:
- (83.2 MJ, 427.7 MPa) (S1-No.1) (zhu2022multiobjectiveoptimizationof pages 15-17, zhu2022multiobjectiveoptimizationof media 55d34c7a)
- (84.7 MJ, 440.8 MPa) (S1-No.2) (zhu2022multiobjectiveoptimizationof pages 15-17, zhu2022multiobjectiveoptimizationof media 55d34c7a)
- (87.7 MJ, 451.7 MPa) (S1-No.3) (zhu2022multiobjectiveoptimizationof pages 15-17, zhu2022multiobjectiveoptimizationof media 55d34c7a)

They also report comparison points for single-objective “min-energy” and “max-strength” solutions and a manufacturer setting in the same table (useful as dominated/baseline points), e.g., 95 MJ & 413.4 MPa (min-energy), 104 MJ & 453.2 MPa (max-strength), and 90 MJ & 440 MPa (manufacturer). (zhu2022multiobjectiveoptimizationof pages 15-17, zhu2022multiobjectiveoptimizationof media 55d34c7a)

## 2) Quality/defect Pareto: porosity vs crack density (LPBF Al6061)
Ince et al. formulate a bi-objective optimization for LPBF Al6061 minimizing **relative porosity** (ϕrel) and **relative crack density** (εrel) as a two-objective problem, and state they solved it using MATLAB’s multi-objective genetic algorithm (`gamultiobj`) and `paretosearch`, i.e., explicitly a Pareto-front approach. (ince2024anexperimentalprocess pages 5-6, ince2024anexperimentalprocess pages 6-8)

However, in the retrieved text segments the authors do **not** provide an explicit list of Pareto-front coordinates (non-dominated porosity–crack-density pairs). What is available quantitatively are experimental run points (process parameters → porosity, crack density), which demonstrate the tradeoff trend they describe (“minimizing porosity leads to increasing crack density whereas minimizing crack density results in high porosity”). (ince2024anexperimentalprocess pages 8-9)

Example quantitative tradeoff points (not asserted to be non-dominated) from their Table 2 include:
- 190 W, 100 mm/s, h = 0.1 mm → porosity 3.35, crack 0.70 (ince2024anexperimentalprocess pages 5-6)
- 200 W, 100 mm/s, h = 0.1 mm → porosity 0.60, crack 0.23 (ince2024anexperimentalprocess pages 5-6)
- 275 W, 400 mm/s, h = 0.1 mm → porosity 0.70, crack 2.01 (ince2024anexperimentalprocess pages 5-6)

## 3) Strength–thermal stability multi-objective alloy design (exists, but not as an explicit Pareto front in retrieved pages)
Taheri-Mousavi et al. present a hybrid ML + Bayesian optimization workflow for *additively manufacturable high-strength aluminum alloys* emphasizing thermally stable microstructures (e.g., improving an L1\_2-related metric and reducing a coarsening metric while managing printability-related objectives). (taherimousavi2024additivelymanufacturablehighstrength pages 7-9, taherimousavi2024additivelymanufacturablehighstrength pages 1-4)

In the retrieved pages, their approach is described via **composite objectives** and single “optimized” outcomes rather than an explicit Pareto front or a table of non-dominated strength–thermal-stability (or strength–ductility) points. Quantitative outcomes reported include ~40% enhancement in L1\_2 at.% and 3.5× reduction in a coarsening metric vs a benchmark, and mechanical-property comparisons such as ~180 HV as-built hardness and ~50% higher yield strength than a benchmark printable alloy, including discussion of hardness evolution on aging at 400 °C. (taherimousavi2024additivelymanufacturablehighstrength pages 7-9, taherimousavi2024additivelymanufacturablehighstrength pages 12-15)

## Evidence gap relative to the request (strength–ductility and explicit strength–thermal stability Pareto fronts)
Within the *retrieved full-text corpus*, I did not find an AM-aluminum paper that explicitly provides a **strength–ductility Pareto front** (e.g., UTS/YS vs elongation) with quantitative Pareto-point coordinates, nor an explicit **strength–thermal stability Pareto front** with non-dominated points reported as (strength, stability metric). The strongest match to the user’s requested categories with explicit, quantitative Pareto coordinates is the **energy-consumption vs tensile-strength** Pareto study in SLM AlSi10Mg (Zhu 2022). (zhu2022multiobjectiveoptimizationof pages 15-17, zhu2022multiobjectiveoptimizationof media 660e21aa, zhu2022multiobjectiveoptimizationof media 55d34c7a)

References

1. (zhu2022multiobjectiveoptimizationof pages 15-17): Chengcheng Zhu, Xiaoming Chen, Honglin Wu, Jun Zhu, Tao Peng, Jingxiang Lv, and Yihang Wu. Multi-objective optimization of selective laser melting processes for minimizing energy consumption and maximizing product tensile strength. Metals, 12:1782, Oct 2022. URL: https://doi.org/10.3390/met12111782, doi:10.3390/met12111782. This article has 18 citations.

2. (zhu2022multiobjectiveoptimizationof media 660e21aa): Chengcheng Zhu, Xiaoming Chen, Honglin Wu, Jun Zhu, Tao Peng, Jingxiang Lv, and Yihang Wu. Multi-objective optimization of selective laser melting processes for minimizing energy consumption and maximizing product tensile strength. Metals, 12:1782, Oct 2022. URL: https://doi.org/10.3390/met12111782, doi:10.3390/met12111782. This article has 18 citations.

3. (zhu2022multiobjectiveoptimizationof media 55d34c7a): Chengcheng Zhu, Xiaoming Chen, Honglin Wu, Jun Zhu, Tao Peng, Jingxiang Lv, and Yihang Wu. Multi-objective optimization of selective laser melting processes for minimizing energy consumption and maximizing product tensile strength. Metals, 12:1782, Oct 2022. URL: https://doi.org/10.3390/met12111782, doi:10.3390/met12111782. This article has 18 citations.

4. (ince2024anexperimentalprocess pages 5-6): Faik Derya Ince, Sivaji Karna, Tianyu Zhang, Andrew J. Gross, Timothy Krentz, Dale Hitchcock, Lang Yuan, and Tuğrul Özel. An experimental process parameter study on the identification of defects in additively fabricated al6061 with laser powder bed fusion. Materials Science in Additive Manufacturing, 3:3652, Aug 2024. URL: https://doi.org/10.36922/msam.3652, doi:10.36922/msam.3652. This article has 10 citations and is from a peer-reviewed journal.

5. (ince2024anexperimentalprocess pages 8-9): Faik Derya Ince, Sivaji Karna, Tianyu Zhang, Andrew J. Gross, Timothy Krentz, Dale Hitchcock, Lang Yuan, and Tuğrul Özel. An experimental process parameter study on the identification of defects in additively fabricated al6061 with laser powder bed fusion. Materials Science in Additive Manufacturing, 3:3652, Aug 2024. URL: https://doi.org/10.36922/msam.3652, doi:10.36922/msam.3652. This article has 10 citations and is from a peer-reviewed journal.

6. (ince2024anexperimentalprocess pages 6-8): Faik Derya Ince, Sivaji Karna, Tianyu Zhang, Andrew J. Gross, Timothy Krentz, Dale Hitchcock, Lang Yuan, and Tuğrul Özel. An experimental process parameter study on the identification of defects in additively fabricated al6061 with laser powder bed fusion. Materials Science in Additive Manufacturing, 3:3652, Aug 2024. URL: https://doi.org/10.36922/msam.3652, doi:10.36922/msam.3652. This article has 10 citations and is from a peer-reviewed journal.

7. (taherimousavi2024additivelymanufacturablehighstrength pages 7-9): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

8. (taherimousavi2024additivelymanufacturablehighstrength pages 12-15): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

9. (taherimousavi2024additivelymanufacturablehighstrength pages 1-4): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.


---

## Query 2

**Question:** What comprehensive property databases or compilation tables exist for additively manufactured aluminum alloys? Identify review papers that provide side-by-side property comparisons across multiple AM Al alloy families.

**Task ID:** `f3cbe584-8ece-4226-9dfd-53d6fc98bae3`

**Status:** complete

## Scope
This response focuses on **property databases / compilation tables** for **additively manufactured (AM) aluminum alloys**, emphasizing review papers that include **side-by-side** comparisons across **multiple AM Al alloy families/series**.

## Review papers with cross-family, side-by-side property compilations (strongest evidence)

### 1) Boillat et al. 2021 (Crystals/MDPI): cross-family *as-built* mechanical property table
Boillat et al. include a compilation table explicitly titled **“Mechanical properties of AM fabricated aluminum alloys in the as-built condition and notable conventionally processed counterparts”** (their **Table 2**). The table functions like a compact property database, listing **yield strength (YS), ultimate tensile strength (UTS), elongation, and hardness** side-by-side for multiple AM aluminum compositions and families, and also includes conventional counterparts for context. Alloy families/compositions represented include **Al–Si (AlSi7Mg0.3, AlSi10Mg; and A356), 2xxx-like Al–Cu–Mg–Mn, 6061 (6xxx), 7075 (7xxx), Scalmalloy® (Al–Mg–Sc–Zr), and ADDAlloy™ (Al–Mg–Zr)**, among others. (boillat2021theeffectof pages 5-6, boillat2021theeffectof media a59a74eb)

### 2) Wang et al. 2020 (Materials/MDPI): series-level property-range table spanning multiple Al series
Wang et al. present **Table 1** that compiles **mechanical-property ranges (YS, UTS, elongation/plastic strain)** across multiple **SLM/LPBF aluminum series** in a single side-by-side table organized by series: **1xxx (pure Al), 2xxx (Al–Cu / Al–Cu–Mg), 4xxx, 6xxx, and 7xxx (Al–Zn–Mg–Cu (Zr))**. This table provides a series-level “meta-database” summarizing achievable strength/ductility ranges for SLM Al alloys across families. (wang2020selectivelasermelting pages 37-40)

Wang et al. also include **family-specific compilation tables/figures** useful as deeper property compilations once a family is selected, including:
- **Table 2** summarizing tensile properties for **Al–xSi** alloys; plus composition-dependent property plots (tensile strength/proof stress and elongation) across Al–Si compositions. (wang2020selectivelasermelting pages 40-43)
- **Table 5** titled **“Mechanical properties of SLM 7075 alloys under different loading conditions”**, and figures compiling **fatigue crack growth** for SLM EN AW-7075. (wang2020selectivelasermelting pages 47-49)

## Other compilation-table style reviews (useful, but not cross-family numerical “databases” in provided evidence)

### Ponnusamy et al. 2020: compilation of literature, mainly Al–Si-focused
Ponnusamy et al. explicitly include **Table 1** described as a **compilation of key published literature** on SLM of aluminum alloys (in practice largely **Al–Si** systems such as **AlSi10Mg, AlSi12, A356, A357**). This is valuable as a **study-index / evidence map** (process conditions, heat treatment, property categories, machine), but it is not evidenced here as a **single numerical, cross-family side-by-side property database** spanning 2xxx/6xxx/7xxx/Sc–Zr families. (ponnusamy2020mechanicalpropertiesof pages 1-4)

### Liu et al. 2024 (International Journal of Extreme Manufacturing): DED/LDED benchmark-property summary (candidate)
For laser directed energy deposition (LDED), Liu et al. state that **“benchmark mechanical properties”** of LDED Al alloys are summarized in the review. This makes it a promising DED-focused compilation source, but the excerpts available here do not expose the specific table/figure identifiers needed to confirm a side-by-side cross-family property table. (wang2020selectivelasermelting pages 1-3)

## Catalog of identified compilation sources
| Source (citation) | AM process scope (SLM/LPBF, DED, etc.) | Cross-family? (yes/no) | Compilation table(s)/figure(s) (numbers and titles) | Alloy families included | Property types included (tensile, hardness, fatigue, etc.) | Notes/limitations |
|---|---|---|---|---|---|---|
| Boillat, Isanaka & Liou, *The Effect of Nanostructures in Aluminum Alloys Processed Using Additive Manufacturing on Microstructural Evolution and Mechanical Performance Behavior* (2021) (boillat2021theeffectof pages 5-6, boillat2021theeffectof media a59a74eb) | Mostly SLM/LPBF, with some DED/comparison to conventional processing | Yes | **Table 2**: “Mechanical properties of AM fabricated aluminum alloys in the as-built condition and notable conventionally processed counterparts” | Pure Al; Al-Si alloys (AlSi7Mg0.3, AlSi10Mg, A356); Al-Cu-Mg-Mn (2xxx-like); 6061 (6xxx); 7075 (7xxx); Scalmalloy® (Al-Mg-Sc-Zr); ADDAlloy™ (Al-Mg-Zr) | Yield strength, UTS, elongation, hardness; process direction noted; conventional comparators | Strongest directly evidenced cross-family compilation found. Table is visually validated and functions like a compact property database, but mainly for **as-built** condition and not a full fatigue/fracture/corrosion database. |
| Wang et al., *Selective Laser Melting of Aluminum and Its Alloys* (2020) (wang2020selectivelasermelting pages 37-40, wang2020selectivelasermelting pages 40-43, wang2020selectivelasermelting pages 47-49, wang2020selectivelasermelting pages 49-52) | SLM/LPBF only | Yes | **Table 1**: cross-series summary of mechanical-property ranges for SLM Al alloys by series; **Table 2**: tensile properties of Al-xSi alloys; **Table 3**: tensile properties of Al-12Si across processing methods; **Table 5**: “Mechanical properties of SLM 7075 alloys under different loading conditions”; **Figure 50**: hardness vs aging time for SLM Al7075; **Figure 56**: tensile strength/proof stress across Al-xSi compositions; **Figure 57**: fracture elongation across Al-xSi compositions; **Figure 58**: tensile-property comparison of Al-12Si by die casting/sand casting/SLM; **Figure 65**: fatigue crack growth curves for SLM EN AW-7075 | Series-level Table 1 includes 1xxx, 2xxx, 4xxx, 6xxx, 7xxx; later tables/figures include Al-Si and 7xxx in more detail; review also covers Al-Mg and nanocrystalline alloys elsewhere | Yield strength, UTS, elongation/plastic strain; hardness; compressive behavior; fatigue crack growth; some tribology/wear in later figures | Best broad **review-style compilation source** after Boillat. Cross-family comparison is clearest in Table 1; later tables are mostly family-specific rather than one single unified database. |
| Liu et al., *Review on Laser Directed Energy Deposited Aluminum Alloys* (2024) (wang2020selectivelasermelting pages 1-3) | LDED/DED | Likely yes at family level, but not explicitly table-verified from excerpt | Review states that “benchmark mechanical properties and primary strengthening mechanism of LDED Al alloys are summarized” | LDED Al alloys broadly; excerpt references 7075 and poorer properties than LPBF, implying multi-family coverage | Benchmark mechanical properties; strengthening mechanisms | Promising **DED-specific** source for a compilation table/database, but excerpt does not provide table/figure numbers, so it cannot be claimed with the same confidence as Boillat or Wang. |
| Ponnusamy et al., *Mechanical Properties of SLM-Printed Aluminium Alloys: A Review* (2020) (ponnusamy2020mechanicalpropertiesof pages 1-4) | SLM/LPBF | No for cross-family; mostly Al-Si-focused | **Table 1**: compilation of key published literature on SLM of aluminum alloys, including process conditions, main findings, property categories, and machine used | Mainly Al-Si family: AlSi10Mg, AlSi12, A356, A357 | Mechanical-property categories across studies: tensile/compression, fatigue, heat-treatment effects, anisotropy/build orientation | Useful as a **study-compilation table**, but not a side-by-side multi-family numerical property database spanning 2xxx/6xxx/7xxx/Sc-Zr families. |
| Kotadia et al., *A Review of Laser Powder Bed Fusion Additive Manufacturing of Aluminium Alloys: Microstructure and Properties* (2021) (kotadiaUnknownyear…hr pages 1-4) | L-PBF/LPBF | Likely yes at review scope, but not table-verified from excerpt | No specific compilation table/figure identified in the available excerpt | Cast Al-Si alloys; wrought Al alloys; AM-specific Al-Mg-Sc-type alloys; explicitly mentions printable near-eutectic Al-Si compositions such as AlSi7Mg, AlSi10Mg, AlSi12Mg | Microstructure-property relationships; mechanical-property discussion implied | High-value candidate review for side-by-side comparisons, but available excerpt does not expose exact table numbers/titles, so evidence is insufficient to assert a specific property database table. |
| Aversa et al., *New Aluminum Alloys Specifically Designed for Laser Powder Bed Fusion: A Review* (2019) (aversa2019newaluminumalloys pages 6-8) | LPBF/L-PBF | Review scope spans multiple families, but no explicit side-by-side table verified from excerpt | No database-style property table identified in the available excerpt; figures mentioned are microstructure/process oriented (e.g., Figures 5–6) | Al-Si (AlSi10Mg), Al-Cu-Mg (near-2024), 6061, 7050/7075, Zr-containing modifications | Narrative summaries with some quantitative tensile values from individual studies | Important alloy-design review spanning 2xxx/6xxx/7xxx and modified systems, but evidence available here supports it more as a **narrative comparative review** than a verified side-by-side property-table source. |
| Galy et al., *Main Defects Observed in Aluminum Alloy Parts Produced by SLM: From Causes to Consequences* (2018) (galy2018maindefectsobserved pages 1-5) | SLM | No clear evidence of side-by-side property tables | No compilation property table identified from excerpt | Multiple SLM Al alloys considered qualitatively | Defects, anisotropy, porosity, cracking, surface quality; not a property-database review | Useful defect review, but not evidenced here as a comprehensive mechanical-property compilation source. |


*Table: This table catalogs the review papers most relevant to side-by-side property comparisons for additively manufactured aluminum alloys. It distinguishes clearly evidenced cross-family compilation tables from broader reviews that discuss multiple alloy families but were not table-verified in the available excerpts.*

## Practical takeaways: “comprehensive property databases” for AM Al alloys (as of the evidence retrieved here)
1. **Closest to a single-table cross-family property database:** Boillat et al. Table 2 (as-built tensile + hardness across many AM Al families, with conventional comparators). (boillat2021theeffectof pages 5-6, boillat2021theeffectof media a59a74eb)
2. **Best series-level cross-family summary:** Wang et al. Table 1 (property ranges by Al series for SLM). (wang2020selectivelasermelting pages 37-40)
3. **Family-deep compilation tables:** Wang et al. Tables/Figures for Al–Si and 7xxx (and likely other series elsewhere in the review), including fatigue crack growth for 7075. (wang2020selectivelasermelting pages 40-43, wang2020selectivelasermelting pages 47-49)
4. **Literature compilation rather than property table:** Ponnusamy et al. Table 1 (study-level index) is useful for building a database, but it is not itself a cross-family side-by-side numerical property comparison in the excerpted evidence. (ponnusamy2020mechanicalpropertiesof pages 1-4)

## Evidence limitations
Several high-value AM Al reviews were retrieved (e.g., Kotadia et al.; Aversa et al.), but the available excerpts did not include their key tables/appendices. Therefore, this answer only *asserts* side-by-side multi-family compilation tables where the table content/description is present in the retrieved evidence (not inferred). (aversa2019newaluminumalloys pages 6-8, kotadiaUnknownyear…hr pages 1-4)

References

1. (boillat2021theeffectof pages 5-6): Rachel Boillat, Sriram Praneeth Isanaka, and Frank Liou. The effect of nanostructures in aluminum alloys processed using additive manufacturing on microstructural evolution and mechanical performance behavior. Crystals, 11(5):524, May 2021. URL: https://doi.org/10.3390/cryst11050524, doi:10.3390/cryst11050524. This article has 32 citations.

2. (boillat2021theeffectof media a59a74eb): Rachel Boillat, Sriram Praneeth Isanaka, and Frank Liou. The effect of nanostructures in aluminum alloys processed using additive manufacturing on microstructural evolution and mechanical performance behavior. Crystals, 11(5):524, May 2021. URL: https://doi.org/10.3390/cryst11050524, doi:10.3390/cryst11050524. This article has 32 citations.

3. (wang2020selectivelasermelting pages 37-40): Zhi Wang, Raghunandan Ummethala, Neera Singh, Shengyang Tang, Challapalli Suryanarayana, Jürgen Eckert, and Konda Gokuldoss Prashanth. Selective laser melting of aluminum and its alloys. Materials, 13:4564, Oct 2020. URL: https://doi.org/10.3390/ma13204564, doi:10.3390/ma13204564. This article has 131 citations.

4. (wang2020selectivelasermelting pages 40-43): Zhi Wang, Raghunandan Ummethala, Neera Singh, Shengyang Tang, Challapalli Suryanarayana, Jürgen Eckert, and Konda Gokuldoss Prashanth. Selective laser melting of aluminum and its alloys. Materials, 13:4564, Oct 2020. URL: https://doi.org/10.3390/ma13204564, doi:10.3390/ma13204564. This article has 131 citations.

5. (wang2020selectivelasermelting pages 47-49): Zhi Wang, Raghunandan Ummethala, Neera Singh, Shengyang Tang, Challapalli Suryanarayana, Jürgen Eckert, and Konda Gokuldoss Prashanth. Selective laser melting of aluminum and its alloys. Materials, 13:4564, Oct 2020. URL: https://doi.org/10.3390/ma13204564, doi:10.3390/ma13204564. This article has 131 citations.

6. (ponnusamy2020mechanicalpropertiesof pages 1-4): Panneer Ponnusamy, Rizwan Abdul Rahman Rashid, Syed Hasan Masood, Dong Ruan, and Suresh Palanisamy. Mechanical properties of slm-printed aluminium alloys: a review. Materials, 13:4301, Sep 2020. URL: https://doi.org/10.3390/ma13194301, doi:10.3390/ma13194301. This article has 190 citations.

7. (wang2020selectivelasermelting pages 1-3): Zhi Wang, Raghunandan Ummethala, Neera Singh, Shengyang Tang, Challapalli Suryanarayana, Jürgen Eckert, and Konda Gokuldoss Prashanth. Selective laser melting of aluminum and its alloys. Materials, 13:4564, Oct 2020. URL: https://doi.org/10.3390/ma13204564, doi:10.3390/ma13204564. This article has 131 citations.

8. (wang2020selectivelasermelting pages 49-52): Zhi Wang, Raghunandan Ummethala, Neera Singh, Shengyang Tang, Challapalli Suryanarayana, Jürgen Eckert, and Konda Gokuldoss Prashanth. Selective laser melting of aluminum and its alloys. Materials, 13:4564, Oct 2020. URL: https://doi.org/10.3390/ma13204564, doi:10.3390/ma13204564. This article has 131 citations.

9. (kotadiaUnknownyear…hr pages 1-4): HR Kotadia. … , hr, gibbons, g, das, a and howes, pd a review of laser powder bed fusion additive manufacturing of aluminium alloys: microstructure and properties http …. Unknown journal, Unknown year.

10. (aversa2019newaluminumalloys pages 6-8): Alberta Aversa, Giulio Marchese, Abdollah Saboori, Emilio Bassini, Diego Manfredi, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. New aluminum alloys specifically designed for laser powder bed fusion: a review. Materials, 12:1007, Mar 2019. URL: https://doi.org/10.3390/ma12071007, doi:10.3390/ma12071007. This article has 301 citations.

11. (galy2018maindefectsobserved pages 1-5): Cassiopée Galy, Emilie Le Guen, Eric Lacoste, and Corinne Arvieu. Main defects observed in aluminum alloy parts produced by slm: from causes to consequences. Additive Manufacturing, 22:165-175, Aug 2018. URL: https://doi.org/10.1016/j.addma.2018.05.005, doi:10.1016/j.addma.2018.05.005. This article has 428 citations and is from a highest quality peer-reviewed journal.


---

## Query 3

**Question:** What in-situ alloying approaches have been demonstrated for LPBF aluminum alloys? Provide examples of powder mixing, reactive synthesis, or compositional blending with measured properties of the resulting alloys.

**Task ID:** `0c62023e-6691-4bcc-8951-26106e6ab9c6`

**Status:** complete

## Scope
This summary covers *demonstrated* in‑situ alloying approaches during laser powder bed fusion (LPBF) of aluminum alloys, emphasizing (i) **powder mixing/compositional blending** (elemental additions into an Al alloy powder), (ii) **elemental powder blends** to synthesize a new Al alloy chemistry, and (iii) **reactive synthesis / in‑situ phase formation** (e.g., in‑situ grain refiners). Quantitative measured properties are reported where available.

## Evidence-based examples of in‑situ alloying in LPBF Al alloys

### 1) Powder mixing / compositional blending into an Al alloy feedstock

#### 1.1 AlSi10Mg + Cu (in‑situ Al–Si–Cu strengthening)
Bosio et al. mechanically blended **AlSi10Mg + 4 wt% Cu** (96:4 by weight) and processed it by LPBF, achieving an average **Cu content of 3.96 ± 0.26 wt%** in the built alloy (bosio2021strengtheningstrategiesfor pages 1-2). In the as-built condition, the blended alloy exhibited higher strength than the baseline AlSi10Mg:
- **As-built AlSi10Mg:** YS **250 ± 6 MPa**, UTS **362 ± 4.2 MPa**, elongation **3.3 ± 0.30%** (Table A1 excerpted) (bosio2021strengtheningstrategiesfor pages 11-14).
- **As-built AlSi10Mg + 4Cu:** YS **339 ± 6.9 MPa**, UTS **433 ± 4.6 MPa**, elongation **2.2 ± 0.31%** (bosio2021strengtheningstrategiesfor pages 11-14).

Direct aging was used to exploit precipitation of Al2Cu-related phases and Si (bosio2021strengtheningstrategiesfor pages 1-2). A reported **peak-aged hardness of 163.9 HV** occurred after **175 °C for 1 h** (bosio2021strengtheningstrategiesfor pages 8-10), consistent with the aging response shown in the extracted figure/table (bosio2021strengtheningstrategiesfor media 8cfbf2c7, bosio2021strengtheningstrategiesfor media a5280b36). Tensile properties for two direct-aged conditions were (bosio2021strengtheningstrategiesfor pages 11-14):
- **175 °C/1 h:** YS **325 ± 6.9 MPa**, UTS **366 ± 8.7 MPa**, elongation **1.4 ± 0.34%**.
- **190 °C/2 h:** YS **301 ± 2.2 MPa**, UTS **369 ± 4.6 MPa**, elongation **1.6 ± 0.08%**.

Microstructurally, the Cu-modified alloy showed XRD evidence of **h‑Al2Cu** precipitates and Cu segregation preferentially in overlapping melt pool regions (bosio2021strengtheningstrategiesfor pages 8-10, bosio2021strengtheningstrategiesfor pages 6-8), consistent with typical limitations of in‑situ LPBF mixing (local inhomogeneity).

#### 1.2 Al6182 (6xxx) + Zr + Ti (grain-refinement via in‑situ trialuminides)
Riener et al. demonstrated LPBF of Al6182 (AlMgSi1Zr) with **mechanically mixed Zr and Ti additions** (reported as a powder mixture containing **0.7 wt% Zr and 0.7 wt% Ti**) (riener2022processingofaluminum pages 7-10). This produced a **crack-free** and nearly fully dense build:
- **Relative density:** **99.95 ± 0.05%** (riener2022processingofaluminum pages 7-10).
- **Microstructure:** equiaxed α‑Al grains with **~1.2 µm** average grain size (riener2022processingofaluminum pages 7-10).
- **In‑situ formed phases / nucleants:** orthorhombic **D022 Al3(Ti,Zr)** trialuminides (coherent interface with α‑Al) were identified and implicated as effective heterogeneous nucleation sites; some unmolten/partially molten Zr/Ti particles remained (riener2022processingofaluminum pages 7-10).

Measured mechanical properties were (riener2022processingofaluminum pages 7-10):
- **As-built:** hardness **62 ± 3 HV3**, YS **155 ± 5 MPa**, UTS **191 ± 2 MPa**, elongation **25.1 ± 1.8%**.
- **After T6:** hardness **117 ± 1 HV3**, YS **294 ± 2 MPa**, UTS **329 ± 4 MPa**, elongation **11.4 ± 0.9%**.

### 2) Elemental powder blends (new alloy chemistry synthesized in the melt pool)

#### 2.1 Al–Sc, Al–Zr, Al–Sc–Zr (precipitation-strengthened Al via elemental blends)
Glerum et al. used **elemental powder blends** (Al + Sc and/or Zr) to fabricate **Al‑1.5Sc**, **Al‑1.5Zr**, and **Al‑0.75Sc‑0.75Zr** (at.%) by SLM/LPBF, relying on rapid melting/mixing to form primary L12 trialuminide precipitates (glerum2020synthesisofprecipitationstrengthened pages 6-7).

Key measured microstructural metrics included primary precipitate size and grain size (glerum2020synthesisofprecipitationstrengthened pages 6-7):
- Primary L12 precipitate major axis: **0.61 µm** (Al‑1.5Sc), **1.68 µm** (Al‑1.5Zr), **0.86 µm** (Al‑0.75Sc‑0.75Zr).
- α‑Al grain sizes: **2.1 ± 0.6 µm** (Al‑1.5Sc), **3.4 ± 0.9 µm** (Al‑1.5Zr), **2.6 ± 0.6 µm** (Al‑0.75Sc‑0.75Zr).

Mechanical property metrics reported in the as-melted condition (note the paper reports hardness in MPa units) were (glerum2020synthesisofprecipitationstrengthened pages 9-10):
- **As-melted hardness:** **331 MPa** for Al‑Zr; **503–602 MPa** for Al‑Sc and Al‑Sc‑Zr, compared to **~200 MPa** for pure cast Al.

After peak aging (example given for Al‑0.75Sc‑0.75Zr at **350 °C/24 h**), atom probe tomography quantified nanoscale secondary L12 precipitates with (glerum2020synthesisofprecipitationstrengthened pages 7-8):
- Median radius **1.5 nm** (q1 0.9 nm, q3 1.9 nm),
- Number density **1.4 × 10^24 m−3**,
- Volume fraction **2.5%**.
The achieved matrix/tip composition for the Al‑0.75Sc‑0.75Zr starting blend was reported as **Al‑0.30Sc‑0.31Zr‑0.02Si (at.%)**, implying substantial partitioning of Sc and Zr into primary L12 precipitates (glerum2020synthesisofprecipitationstrengthened pages 7-8).

### 3) Reactive synthesis / in‑situ grain refiner formation from blended reactants

#### 3.1 A6061 + Ti + B4C (“RAM2”) → in‑situ TiAl3 nucleants
Rosito et al. processed a blended powder termed **A6061 RAM2** (A6061 + Ti + B4C) to promote in‑situ synthesis of grain refiners during LPBF (rosito2023processabilityofa6061 pages 1-2). While the full ceramic reaction was incomplete, **TiAl3** formed in situ and was associated with partial grain refinement and crack suppression (rosito2023processabilityofa6061 pages 1-2).

Quantitative tensile properties for optimized A6061 RAM2 builds were reported as (rosito2023processabilityofa6061 pages 12-14):
- Young’s modulus **73 ± 6 GPa**,
- Yield strength **230 ± 6 MPa**,
- UTS **256 ± 11 MPa**,
- Elongation **4 ± 1.6%**.
The microstructure was described as bimodal with fine equiaxed grains **~1–5 µm** localized at melt pool boundaries (rosito2023processabilityofa6061 pages 12-14). (Numeric part density/porosity was not provided in the extracted pages; only that the maximum density occurred at 90 W and 635 mm/s, VED 90 J/mm³.) (rosito2023processabilityofa6061 pages 14-16).

### 4) Additional demonstrated routes (reported in review literature; quantitative properties not in provided excerpt)
A recent review summarizes further *demonstrated* LPBF Al in‑situ alloying and reactive-additive routes, including additions of **1 vol% ZrH2 nanoparticles** to Al7075 and Al6061 (reported to eliminate hot cracking), Ti/TiN hybrid grain refiners for 7050, and “RAM” commercial powder systems designed to form in‑situ nucleants/precipitates (yadegari2025aluminumlaseradditive pages 14-15). The excerpt does not provide numeric property values for these cases.

## Summary table of demonstrated approaches and properties
| Study | In-situ approach category | Feedstock powders and target composition | In-situ formed phases / microstructure notes | Key measured properties |
|---|---|---|---|---|
| Bosio et al. 2021 | Powder mixing / compositional blending | AlSi10Mg + 4 wt% Cu powder blend; achieved Cu = 3.96 ± 0.26 wt% | Dual eutectic microstructure with Si and h-Al2Cu; Cu segregation mainly at overlapping melt-pool regions; equiaxed Al grain size 7.34 µm vs 7.56 µm for AlSi10Mg; peak aging at 175 °C for 1 h (bosio2021strengtheningstrategiesfor pages 1-2, bosio2021strengtheningstrategiesfor pages 8-10, bosio2021strengtheningstrategiesfor media 8cfbf2c7, bosio2021strengtheningstrategiesfor media a5280b36) | Peak hardness = 163.9 HV at 175 °C/1 h; vs as-built AlSi10Mg, hardness +8.8% and YS +35.6%; tensile: as-built AlSi10Mg = YS 250 ± 6 MPa, UTS 362 ± 4.2 MPa, ε 3.3 ± 0.30%; as-built AlSi10Mg+4Cu = YS 339 ± 6.9 MPa, UTS 433 ± 4.6 MPa, ε 2.2 ± 0.31%; aged 175 °C/1 h = YS 325 ± 6.9 MPa, UTS 366 ± 8.7 MPa, ε 1.4 ± 0.34%; aged 190 °C/2 h = YS 301 ± 2.2 MPa, UTS 369 ± 4.6 MPa, ε 1.6 ± 0.08% (bosio2021strengtheningstrategiesfor pages 11-14, bosio2021strengtheningstrategiesfor pages 8-10, bosio2021strengtheningstrategiesfor pages 10-11) |
| Riener et al. 2022 | Powder mixing / elemental addition | Al6182 (AlMgSi1Zr) powder with 0.5 wt% Zr + 0.5 wt% Ti mechanically added; mixture described as 0.7 wt% each Zr and Ti in processed powder system | Crack-free, fully equiaxed α-Al microstructure; average grain size ~1.2 µm; orthorhombic D022 Al3(Ti,Zr) / Al3(Zr,Ti) trialuminides with coherent or semi-coherent interface to α-Al act as grain refiners; some unmolten/partially molten Zr/Ti particles remain (riener2022processingofaluminum pages 7-10, riener2022processingofaluminum pages 1-2) | Relative density 99.95 ± 0.05% (>99.9% by µCT); as-built hardness 62 ± 3 HV3, YS 155 ± 5 MPa, UTS 191 ± 2 MPa, ε 25.1 ± 1.8%; after T6: hardness 117 ± 1 HV3, YS 294 ± 2 MPa, UTS 329 ± 4 MPa, ε 11.4 ± 0.9% (riener2022processingofaluminum pages 7-10, riener2022processingofaluminum pages 1-2) |
| Glerum et al. 2020 | Elemental powder blend | Elemental Al + Sc and/or Zr; studied Al-1.5Sc, Al-1.5Zr, Al-0.75Sc-0.75Zr (at.%) | Primary micron-scale L12 precipitates form during SLM and nucleate fine α-Al grains; primary precipitate major axis: 0.61 µm (Al-1.5Sc), 1.68 µm (Al-1.5Zr), 0.86 µm (Al-0.75Sc-0.75Zr); grain size: 2.1 ± 0.6 µm, 3.4 ± 0.9 µm, 2.6 ± 0.6 µm respectively; for Al-0.75Sc-0.75Zr after aging, secondary L12 precipitates are Sc-rich core/Zr-rich shell (glerum2020synthesisofprecipitationstrengthened pages 6-7, glerum2020synthesisofprecipitationstrengthened pages 9-10, glerum2020synthesisofprecipitationstrengthened pages 8-9) | As-melted hardness: 331 MPa (Al-Zr) and 503–602 MPa (Al-Sc and Al-Sc-Zr), vs ~200 MPa for pure cast Al; peak aging increases hardness by factor 1.7–2.5; for aged Al-0.75Sc-0.75Zr, precipitate median radius 1.5 nm, number density 1.4 × 10^24 m^-3, volume fraction 2.5%; measured matrix/tip composition Al-0.30Sc-0.31Zr-0.02Si at.% indicating ~60% of Sc and Zr precipitated as primary L12 (glerum2020synthesisofprecipitationstrengthened pages 7-8, glerum2020synthesisofprecipitationstrengthened pages 9-10, glerum2020synthesisofprecipitationstrengthened pages 8-9) |
| Rosito et al. 2023 | Reactive synthesis | A6061 RAM2 powder blend = A6061 + Ti + B4C | Intended ceramic reaction incomplete, but TiAl3 formed in situ; no solidification cracking in optimized samples; bimodal microstructure with fine equiaxed grains 1–5 µm at melt-pool boundaries and columnar grains inside melt pools (rosito2023processabilityofa6061 pages 1-2, rosito2023processabilityofa6061 pages 12-14, rosito2023processabilityofa6061 pages 14-16, rosito2023processabilityofa6061 pages 8-9) | Optimized processing at 90 W and 635 mm/s (VED 90 J/mm^3) gave highest density (numeric density not reported in provided evidence); tensile: E 73 ± 6 GPa, YS 230 ± 6 MPa, UTS 256 ± 11 MPa, ε 4 ± 1.6%; baseline LPBF A6061 in cited comparison: E 27.6 GPa, YS 56.6 MPa, UTS 62.1 MPa, ε 0.7% (rosito2023processabilityofa6061 pages 12-14, rosito2023processabilityofa6061 pages 14-16) |
| Review examples summarized in Yadegari et al. 2025 | Reactive synthesis / elemental addition / compositional blending | Reported LPBF additions include 1 vol% ZrH2 nanoparticles to Al7075 and Al6061; Ti/TiN hybrid grain refiners in 7050; tailored printable alloys such as Scalmalloy, A20X, Aheadd CP1/HT1, Elementum 3D Al6061/7050 RAM | In-situ precipitation/nucleant formation including Al3Zr, Al3Sc, nano-Al3Zr and Al13Fe4; used to suppress hot cracking and refine grains (yadegari2025aluminumlaseradditive pages 14-15) | Quantitative metrics not given in the excerpt, but review explicitly reports hot-crack elimination in Al7075 and Al6061 with 1 vol% ZrH2 and improved yield/fatigue/ductility/thermal stability for several designed LPBF alloys (yadegari2025aluminumlaseradditive pages 14-15) |


*Table: This table summarizes demonstrated in-situ alloying strategies for LPBF aluminum alloys, organized by approach type and supported with explicit measured properties where available. It is useful for comparing how powder mixing, elemental blending, and reactive synthesis changed microstructure, density, hardness, and tensile behavior.*

## Notes and limitations
- Some studies explicitly show that powder-mixed in‑situ alloying can leave local compositional inhomogeneity (e.g., Cu segregation in AlSi10Mg+Cu), which can trade ductility for strength (bosio2021strengtheningstrategiesfor pages 6-8, bosio2021strengtheningstrategiesfor pages 11-14).
- For several in‑situ strategies (e.g., ZrH2 nanoparticle additions to 7xxx/6xxx alloys) the provided evidence excerpt is qualitative; additional full-text extraction would be required to report their measured tensile/hardness values (yadegari2025aluminumlaseradditive pages 14-15).

References

1. (bosio2021strengtheningstrategiesfor pages 1-2): Federico Bosio, Paolo Fino, Diego Manfredi, and Mariangela Lombardi. Strengthening strategies for an al alloy processed by in-situ alloying during laser powder bed fusion. Materials & Design, 212:110247, Dec 2021. URL: https://doi.org/10.1016/j.matdes.2021.110247, doi:10.1016/j.matdes.2021.110247. This article has 42 citations and is from a highest quality peer-reviewed journal.

2. (bosio2021strengtheningstrategiesfor pages 11-14): Federico Bosio, Paolo Fino, Diego Manfredi, and Mariangela Lombardi. Strengthening strategies for an al alloy processed by in-situ alloying during laser powder bed fusion. Materials & Design, 212:110247, Dec 2021. URL: https://doi.org/10.1016/j.matdes.2021.110247, doi:10.1016/j.matdes.2021.110247. This article has 42 citations and is from a highest quality peer-reviewed journal.

3. (bosio2021strengtheningstrategiesfor pages 8-10): Federico Bosio, Paolo Fino, Diego Manfredi, and Mariangela Lombardi. Strengthening strategies for an al alloy processed by in-situ alloying during laser powder bed fusion. Materials & Design, 212:110247, Dec 2021. URL: https://doi.org/10.1016/j.matdes.2021.110247, doi:10.1016/j.matdes.2021.110247. This article has 42 citations and is from a highest quality peer-reviewed journal.

4. (bosio2021strengtheningstrategiesfor media 8cfbf2c7): Federico Bosio, Paolo Fino, Diego Manfredi, and Mariangela Lombardi. Strengthening strategies for an al alloy processed by in-situ alloying during laser powder bed fusion. Materials & Design, 212:110247, Dec 2021. URL: https://doi.org/10.1016/j.matdes.2021.110247, doi:10.1016/j.matdes.2021.110247. This article has 42 citations and is from a highest quality peer-reviewed journal.

5. (bosio2021strengtheningstrategiesfor media a5280b36): Federico Bosio, Paolo Fino, Diego Manfredi, and Mariangela Lombardi. Strengthening strategies for an al alloy processed by in-situ alloying during laser powder bed fusion. Materials & Design, 212:110247, Dec 2021. URL: https://doi.org/10.1016/j.matdes.2021.110247, doi:10.1016/j.matdes.2021.110247. This article has 42 citations and is from a highest quality peer-reviewed journal.

6. (bosio2021strengtheningstrategiesfor pages 6-8): Federico Bosio, Paolo Fino, Diego Manfredi, and Mariangela Lombardi. Strengthening strategies for an al alloy processed by in-situ alloying during laser powder bed fusion. Materials & Design, 212:110247, Dec 2021. URL: https://doi.org/10.1016/j.matdes.2021.110247, doi:10.1016/j.matdes.2021.110247. This article has 42 citations and is from a highest quality peer-reviewed journal.

7. (riener2022processingofaluminum pages 7-10): Kirstin Riener, Alexander Nagler, Ilse Letofsky-Papst, and Gerhard Leichtfried. Processing of aluminum alloy 6182 with high scanning speed in lpbf by in-situ alloying with zr and ti powder. Alloys, 1:277-287, Dec 2022. URL: https://doi.org/10.3390/alloys1030018, doi:10.3390/alloys1030018. This article has 7 citations.

8. (glerum2020synthesisofprecipitationstrengthened pages 6-7): Jennifer A. Glerum, Christoph Kenel, Tao Sun, and David C. Dunand. Synthesis of precipitation-strengthened al-sc, al-zr and al-sc-zr alloys via selective laser melting of elemental powder blends. Additive Manufacturing, 36:101461, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101461, doi:10.1016/j.addma.2020.101461. This article has 105 citations and is from a highest quality peer-reviewed journal.

9. (glerum2020synthesisofprecipitationstrengthened pages 9-10): Jennifer A. Glerum, Christoph Kenel, Tao Sun, and David C. Dunand. Synthesis of precipitation-strengthened al-sc, al-zr and al-sc-zr alloys via selective laser melting of elemental powder blends. Additive Manufacturing, 36:101461, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101461, doi:10.1016/j.addma.2020.101461. This article has 105 citations and is from a highest quality peer-reviewed journal.

10. (glerum2020synthesisofprecipitationstrengthened pages 7-8): Jennifer A. Glerum, Christoph Kenel, Tao Sun, and David C. Dunand. Synthesis of precipitation-strengthened al-sc, al-zr and al-sc-zr alloys via selective laser melting of elemental powder blends. Additive Manufacturing, 36:101461, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101461, doi:10.1016/j.addma.2020.101461. This article has 105 citations and is from a highest quality peer-reviewed journal.

11. (rosito2023processabilityofa6061 pages 1-2): Michele Rosito, Matteo Vanzetti, Elisa Padovano, Flavia Gili, Roberta Sampieri, Federica Bondioli, and Claudio Francesco Badini. Processability of a6061 aluminum alloy using laser powder bed fusion by in situ synthesis of grain refiners. Metals, 13:1128, Jun 2023. URL: https://doi.org/10.3390/met13061128, doi:10.3390/met13061128. This article has 18 citations.

12. (rosito2023processabilityofa6061 pages 12-14): Michele Rosito, Matteo Vanzetti, Elisa Padovano, Flavia Gili, Roberta Sampieri, Federica Bondioli, and Claudio Francesco Badini. Processability of a6061 aluminum alloy using laser powder bed fusion by in situ synthesis of grain refiners. Metals, 13:1128, Jun 2023. URL: https://doi.org/10.3390/met13061128, doi:10.3390/met13061128. This article has 18 citations.

13. (rosito2023processabilityofa6061 pages 14-16): Michele Rosito, Matteo Vanzetti, Elisa Padovano, Flavia Gili, Roberta Sampieri, Federica Bondioli, and Claudio Francesco Badini. Processability of a6061 aluminum alloy using laser powder bed fusion by in situ synthesis of grain refiners. Metals, 13:1128, Jun 2023. URL: https://doi.org/10.3390/met13061128, doi:10.3390/met13061128. This article has 18 citations.

14. (yadegari2025aluminumlaseradditive pages 14-15): Mohammad Javad Yadegari, Alessandra Martucci, Sara Biamino, Daniele Ugues, Laura Montanaro, Paolo Fino, and Mariangela Lombardi. Aluminum laser additive manufacturing: a review on challenges and opportunities through the lens of sustainability. Applied Sciences, 15:2221, Feb 2025. URL: https://doi.org/10.3390/app15042221, doi:10.3390/app15042221. This article has 11 citations.

15. (bosio2021strengtheningstrategiesfor pages 10-11): Federico Bosio, Paolo Fino, Diego Manfredi, and Mariangela Lombardi. Strengthening strategies for an al alloy processed by in-situ alloying during laser powder bed fusion. Materials & Design, 212:110247, Dec 2021. URL: https://doi.org/10.1016/j.matdes.2021.110247, doi:10.1016/j.matdes.2021.110247. This article has 42 citations and is from a highest quality peer-reviewed journal.

16. (riener2022processingofaluminum pages 1-2): Kirstin Riener, Alexander Nagler, Ilse Letofsky-Papst, and Gerhard Leichtfried. Processing of aluminum alloy 6182 with high scanning speed in lpbf by in-situ alloying with zr and ti powder. Alloys, 1:277-287, Dec 2022. URL: https://doi.org/10.3390/alloys1030018, doi:10.3390/alloys1030018. This article has 7 citations.

17. (glerum2020synthesisofprecipitationstrengthened pages 8-9): Jennifer A. Glerum, Christoph Kenel, Tao Sun, and David C. Dunand. Synthesis of precipitation-strengthened al-sc, al-zr and al-sc-zr alloys via selective laser melting of elemental powder blends. Additive Manufacturing, 36:101461, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101461, doi:10.1016/j.addma.2020.101461. This article has 105 citations and is from a highest quality peer-reviewed journal.

18. (rosito2023processabilityofa6061 pages 8-9): Michele Rosito, Matteo Vanzetti, Elisa Padovano, Flavia Gili, Roberta Sampieri, Federica Bondioli, and Claudio Francesco Badini. Processability of a6061 aluminum alloy using laser powder bed fusion by in situ synthesis of grain refiners. Metals, 13:1128, Jun 2023. URL: https://doi.org/10.3390/met13061128, doi:10.3390/met13061128. This article has 18 citations.


---

## Query 4

**Question:** What standards and qualification frameworks exist for additively manufactured aluminum alloy parts? Summarize ASTM, ISO, and industry-specific requirements. What minimum property requirements must AM Al parts meet?

**Task ID:** `cf964432-6899-4992-9680-627ef6d5b07b`

**Status:** complete

## Technical summary: standards and qualification frameworks for AM aluminum alloy parts

### 1) ASTM standards relevant to additively manufactured aluminum alloy parts

**Material/part specification (aluminum-specific).** The principal ASTM finished-part specification identified in the retrieved evidence is **ASTM F3318-18**, a specification for **AlSi10Mg produced by powder bed fusion–laser beam (PBF‑LB)**. Secondary sources describing F3318 indicate it addresses ordering information, feedstock requirements, chemical composition, post-build composition, microstructure, mechanical properties, inspection/retest/rejection, certification, and quality program elements for finished parts (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyofa pages 35-40).

**Test methods used in qualification.** In AM Al studies that explicitly follow F3318 heat-treatment conditions, tensile testing is performed using established ASTM tensile standards (e.g., ASTM E8; and another study cites ASTM E28 for tensile-testing procedures) (diaz2022comparisonofmultiple pages 1-4, caballero2023acomparisonof pages 1-3). These are enabling test methods rather than acceptance criteria.

**Practical implication.** In ASTM-based acceptance, minimum properties for AM aluminum parts are typically taken directly from the relevant material/part specification (e.g., F3318 for AlSi10Mg) and verified via coupon/test specimen programs and/or part-specific inspections; however, the exact numeric minima from F3318 itself were not reproduced in the retrievable excerpts (ferramacho2025qualitystudyof pages 35-40).

### 2) ISO/ASTM and ISO standards (cross-sector) used for qualification and acceptance

**Purchase/contract definition and acceptance planning (ISO/ASTM 52901).** ISO/ASTM **52901:2016** defines what must be included in purchase orders for AM parts, including part definition (drawings/digital files), characteristics (e.g., dimensional accuracy, defects, mechanical properties, residual stress, chemistry), and acceptance criteria. It explicitly includes traceability fields (serial/lot numbers and inspection identifiers) and requires documentation of process-control information during manufacturing (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyofa pages 101-104).

**Powder/feedstock qualification and traceability (ISO/ASTM 52907).** ISO/ASTM **52907:2019** addresses metallic powder feedstock requirements, including documentation/traceability, sampling, particle size distribution, chemical composition, characteristic densities, morphology, flowability, contamination, and packaging. It also requires detailed information in statements of conformity/inspection documents (supplier identity, powder lot reference, product description/chemistry, production process, packaging details, date of analysis, and storage/preservation instructions) (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyof pages 104-106).

**PBF process control for critical applications (ISO/ASTM 52904).** ISO/ASTM **52904:2019** is a practice for operation and production control of metal powder bed fusion to meet requirements for critical applications (e.g., aerospace), applying to production parts and mechanical test specimens (ferramacho2025qualitystudyof pages 35-40).

**Qualification of equipment/sites/personnel (ISO/ASTM 52920 series, 52930/52926-2/52941/52942).** The retrieved sources point to an ISO/ASTM “qualification ecosystem,” including (i) **ISO/ASTM 52920** entries addressing conformity assessment and industrial AM site requirements (afkhami2021metaladditivemanufacturing pages 38-40), and (ii) standards/technical specifications associated with **IQ/OQ/PQ** and acceptance testing of PBF‑LB equipment and operator qualification, including references to **DIN CEN ISO ASTM TS 52930** and drafts linked to **IQ/OQ/PQ** for PBF‑LB systems and **DIN EN ISO ASTM 52942** as an acceptance-test standard (poka2025qualityassurancevia pages 10-12, afkhami2021metaladditivemanufacturing pages 40-42). These standards tend to define *how* to qualify the capability of the production system and personnel, rather than setting alloy-specific tensile minima.

### 3) Industry-specific qualification frameworks (aerospace, spaceflight, pressure hardware, petroleum)

**Aerospace quality systems and accreditation (AS9100 + Nadcap).** In aerospace, AM part production is commonly embedded in a certified QMS such as **SAE AS9100** and may be audited/accredited via **Nadcap**, which has AM-specific audit checklists (including **AC7110/14**) and has performed AM supplier audits/accreditations (russell2019qualificationandcertification pages 6-9).

**Aviation certification expectations (FAA draft guidance).** A draft FAA certification path for additively produced aviation engine components was described as including requirements for feedstock attributes and vendor qualification; powder handling/reprocessing/reuse limits; machine control windows; deposition-environment controls; validation of test-sample performance versus design allowables; post-processing controls (including heat treatment); NDE of components and witness parts; component acceptance testing; and cut-up assessment (russell2019qualificationandcertification pages 11-15).

**Spaceflight qualification (NASA).** NASA’s framework includes a center technical standard and companion specification (MSFC‑STD‑3716 and MSFC‑SPEC‑3717) plus a broader agency direction (e.g., NASA-STD-6030 is listed among spaceflight AM requirements documents). These documents emphasize process control, training, equipment calibration/maintenance, qualified metallurgical processes, and risk/criticality-driven inspection/testing; for higher-criticality classes, NASA requires comprehensive surface and volumetric NDE, with fracture-critical parts requiring a quantitative NDE rationale with probability of detection requirements (wells2018qualification&certification pages 1-16, russell2019qualificationandcertification pages 19-21, russell2019qualificationandcertification pages 25-27, huning2022advancementofcertification pages 46-47).

**Design allowables gap (MMPDS).** MMPDS is cited as the accepted metallic design-allowables handbook used by FAA/DoD/NASA, but the evidence notes that **no metal AM alloys are currently included**, and inclusion requires public specifications and common process/property limits—both still emerging for AM (russell2019qualificationandcertification pages 9-11).

**Industry material specifications for AM aluminum beyond AlSi10Mg (SAE AMS).** Sector specs explicitly listing AM aluminum include **SAE AMS7045 (powder)** and **SAE AMS7046 (LPBF parts)** for a specific Al‑Zn‑Mg‑Zr‑Cu alloy system; AMS7046 is cited as requiring SR + HIP + T7 post-processing (huning2022advancementofcertification pages 46-47).

**Pressure-containing/pressure-loaded aluminum AM hardware (SAE AS8775 / ARP1383).** For AM aluminum pressure components (e.g., hydraulic manifolds), qualification may be governed by pressure-component standards such as **SAE AS8775** (proof/burst pressure) and **SAE ARP1383** (fatigue qualification), which define acceptance as meeting proof/burst multipliers and fatigue/endurance requirements (arena2024novelaluminumalloy pages 8-11).

**Petroleum-industry AM components (API STD 20S).** The petroleum sector has a dedicated standard, **API STD 20S**, for additively manufactured metallic components (huning2022advancementofcertification pages 46-47).

### 4) Minimum property requirements: what AM aluminum parts must meet

#### 4.1 What “minimum property requirements” means in practice
Across standards and sectors, “minimum properties” for AM aluminum parts typically emerge from **(i) an alloy/process material specification (e.g., ASTM F3318 or SAE AMS specifications), (ii) part criticality classification and contract/drawing requirements (e.g., ISO/ASTM 52901), and (iii) the qualification framework imposed by the sector regulator/customer (FAA/NASA/Nadcap)** (ferramacho2025qualitystudyof pages 35-40, russell2019qualificationandcertification pages 11-15, russell2019qualificationandcertification pages 25-27). Many ISO/ASTM documents define **how** to set up traceability, process control, and acceptance plans, rather than prescribing universal numerical strength minima applicable to all AM aluminum (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyofa pages 101-104).

#### 4.2 Numeric minimum/acceptance-style requirements retrievable from the provided evidence
Only a limited set of explicit numeric minima/thresholds were recoverable from the retrieved documents:

1) **Stress-relieved AlSi10Mg (reference requirement set used under an ASTM F3318 SR1 heat-treatment regime).** A study whose specimens were produced and heat-treated according to **ASTM F3318-18 Condition SR1** reports a reference property set for stress-relieved AlSi10Mg: **UTS 410 MPa; YS 240 MPa; elongation 5 ± 2%** (monkova2025apreliminarystudy media a2d05494, monkova2025apreliminarystudy media b73f0830). In that paper, measured orientation-dependent results were compared against these reference values.

2) **Pressure-hardware proof/burst and fatigue acceptance.** For an AM aluminum hydraulic manifold case study, the cited standards require **proof pressure = 1.5×design operating pressure (DOP)** and **burst pressure = 2.5×DOP** (example DOP 207 bar → proof 310.5 bar, burst 517.5 bar). Fatigue acceptance was assessed via **safety margin MS > 0.0** and **cumulative fatigue damage D < 1.0** (arena2024novelaluminumalloy pages 8-11).

#### 4.3 Common minima that are *expected* but not numerically extractable from the current evidence
The evidence clearly indicates that specifications and qualification plans commonly require conformance to (a) **powder chemistry/quality** and (b) **part mechanical properties/microstructure**, with inspection/rejection/certification requirements (e.g., ASTM F3318; ISO/ASTM 52907; ISO/ASTM 52901). However, the retrieved excerpts did **not** reproduce the numerical acceptance limits for: alloy chemistry ranges; relative density/porosity thresholds; or the full set of minimum tensile properties and any location/orientation-specific minima that may be defined in ASTM F3318 or SAE AMS part specs (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyofa pages 101-104, huning2022advancementofcertification pages 46-47).

### 5) Practical compliance checklist (minimum set of “must-haves” across frameworks)
For AM aluminum parts intended for production/critical service, the combined ASTM/ISO/industry evidence supports the following minimum requirements categories:

- **Contract/purchase definition and acceptance plan:** define part, build orientation, post-processing steps, acceptance characteristics and test frequencies; include traceability fields (ISO/ASTM 52901) (ferramacho2025qualitystudyofa pages 101-104).
- **Feedstock control:** document and verify powder lot traceability, sampling, PSD, chemistry, morphology/flowability/contamination, packaging and storage (ISO/ASTM 52907) (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyof pages 104-106).
- **Process control for critical applications:** implement production control practices for PBF (ISO/ASTM 52904) and system qualification (IQ/OQ/PQ concepts and acceptance testing where applicable) (ferramacho2025qualitystudyof pages 35-40, poka2025qualityassurancevia pages 10-12).
- **Material/part specification compliance:** meet the applicable alloy/part specification (e.g., ASTM F3318 for AlSi10Mg PBF‑LB; SAE AMS aluminum AM specs where used) and demonstrate properties through test specimens (ferramacho2025qualitystudyof pages 35-40, huning2022advancementofcertification pages 46-47).
- **Sector qualification overlays:** for aerospace/space, implement QMS/accreditation and sector-specific NDE/qualification requirements (AS9100 + Nadcap checklists; NASA class-driven qualification and NDE; FAA certification elements) (russell2019qualificationandcertification pages 11-15, russell2019qualificationandcertification pages 6-9, russell2019qualificationandcertification pages 25-27).

## Consolidated table of standards and minimum properties

| Section | Standard / framework | Scope / what it covers | Explicit numeric requirements available in evidence |
|---|---|---|---|
| Standards & qualification frameworks | ASTM F3318-18 | Specification for PBF-LB AlSi10Mg finished parts; secondary sources say it covers ordering, feedstock, chemistry, post-build composition, microstructure, mechanical properties, inspection, retest/rejection, certification, and quality program requirements (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyofa pages 35-40) | Numeric minima not reproduced in available excerpts; underlying specification is where formal minimum tensile/property limits are defined (ferramacho2025qualitystudyof pages 35-40) |
| Standards & qualification frameworks | ASTM E8 / ASTM E28 | Supporting tensile-test procedures used in AM aluminum studies that followed ASTM F3318 heat-treatment conditions (caballero2023acomparisonof pages 1-3, diaz2022comparisonofmultiple pages 1-4) | No acceptance minima; test methods only (caballero2023acomparisonof pages 1-3, diaz2022comparisonofmultiple pages 1-4) |
| Standards & qualification frameworks | ISO/ASTM 52901 | Purchase requirements for AM parts: order information, part definition, characteristics/function/performance, acceptance criteria, traceability fields, inspection/test frequencies, and documentation of process control (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyof pages 104-106, ferramacho2025qualitystudyofa pages 101-104) | No universal numeric property minima; acceptance characteristics must be specified in the order/contract (ferramacho2025qualitystudyof pages 104-106, ferramacho2025qualitystudyofa pages 101-104) |
| Standards & qualification frameworks | ISO/ASTM 52907 | Metallic powder/feedstock requirements: documentation and traceability, sampling, PSD, chemistry, densities, morphology, flowability, contamination, packaging, and conformity/inspection documents (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyof pages 104-106, ferramacho2025qualitystudyofa pages 35-40) | No universal part-property minima; standard governs feedstock characterization/traceability (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyof pages 104-106) |
| Standards & qualification frameworks | ISO/ASTM 52904 | Practice for operation and production control of metal PBF for critical applications (e.g., aerospace/medical), applicable to production parts and test specimens (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyofa pages 35-40) | No explicit numeric part minima in evidence (ferramacho2025qualitystudyof pages 35-40) |
| Standards & qualification frameworks | ISO/ASTM 52920 series | Qualification principles / industrial AM site conformity assessment; cited as covering industrial-use conformity assessment and site requirements (afkhami2021metaladditivemanufacturing pages 38-40) | No explicit numeric property minima in evidence (afkhami2021metaladditivemanufacturing pages 38-40) |
| Standards & qualification frameworks | ISO/ASTM 52930 / 52926-2 / 52941 / 52942 | Qualification and acceptance-testing ecosystem for PBF-LB: IQ/OQ/PQ concepts, machine acceptance testing, machine-operator qualification, aerospace PBF acceptance methods (poka2025qualityassurancevia pages 10-12, afkhami2021metaladditivemanufacturing pages 40-42, butler2020standardsinadditive pages 4-6) | No material-property minima; these govern equipment/operator/site qualification and acceptance testing (poka2025qualityassurancevia pages 10-12, butler2020standardsinadditive pages 4-6) |
| Standards & qualification frameworks | AS9100 + Nadcap AC7110 / AC7110/14 | Aerospace QMS and special-process accreditation; AM-specific Nadcap checklists for L-PBF/EB-PBF suppliers and critical structural applications (russell2019qualificationandcertification pages 16-19, russell2019qualificationandcertification pages 6-9) | No direct material minima; establishes accredited production/quality framework (russell2019qualificationandcertification pages 16-19, russell2019qualificationandcertification pages 6-9) |
| Standards & qualification frameworks | FAA draft AM engine-component certification path | Qualification elements for aviation engine AM parts: feedstock/vendor qualification, powder reuse limits, machine control windows, environment control, allowables validation, post-processing, NDE/witness parts, acceptance tests, cut-up assessment (russell2019qualificationandcertification pages 11-15) | No alloy-specific minima in excerpts; design allowables and acceptance testing are required (russell2019qualificationandcertification pages 11-15) |
| Standards & qualification frameworks | NASA MSFC-STD-3716 / MSFC-SPEC-3717 / NASA-STD-6030 | Spaceflight AM qualification framework: AM control plan, metallurgical/process qualification, calibration, training, powder/reuse control, restart procedures, post-processing controls, risk/class-based qualification, mandatory NDE for higher classes (russell2019qualificationandcertification pages 19-21, russell2019qualificationandcertification pages 25-27, wells2018qualification&certification pages 1-16, huning2022advancementofcertification pages 46-47) | No aluminum-specific tensile minima in evidence; requirements are risk/class dependent and process-control heavy (russell2019qualificationandcertification pages 25-27) |
| Standards & qualification frameworks | MMPDS | Metallic design-allowables handbook used by FAA/DoD/NASA; cited as not yet including metal AM alloys because public specifications and common process/property limits are still emerging (russell2019qualificationandcertification pages 9-11) | No AM aluminum allowables in evidence; important gap for certification (russell2019qualificationandcertification pages 9-11) |
| Standards & qualification frameworks | SAE AMS7045 / AMS7046 | Aluminum AM industry specs cited for a specific Al-Zn-Mg-Zr-Cu alloy powder and LPBF parts, with AMS7046 tied to SR + HIP + T7 post-processing (huning2022advancementofcertification pages 46-47) | Numeric minima not available in excerpts; underlying AMS specs govern composition/process/property acceptance (huning2022advancementofcertification pages 46-47) |
| Standards & qualification frameworks | SAE AS8775 / SAE ARP1383 | Pressure-component qualification standards used for AM aluminum hydraulic manifolds: proof/burst pressure and fatigue/endurance qualification (arena2024novelaluminumalloy pages 8-11) | Proof = 1.5×DOP; Burst = 2.5×DOP; example DOP 207 bar gives proof 310.5 bar and burst 517.5 bar; cumulative fatigue damage acceptance D < 1.0 and safety margin MS > 0.0 (arena2024novelaluminumalloy pages 8-11) |
| Standards & qualification frameworks | API STD 20S | Petroleum-industry standard for additively manufactured metallic components (huning2022advancementofcertification pages 46-47) | No aluminum-specific numeric minima in evidence (huning2022advancementofcertification pages 46-47) |
| Minimum / typical acceptance properties from evidence | Stress-relieved AlSi10Mg (reference requirements used for ASTM F3318-18 SR1 comparison) | Reference sheet values for SR AlSi10Mg used as acceptance/comparison targets in a study whose specimens were produced and heat treated per ASTM F3318-18 Condition SR1 (monkova2025apreliminarystudy media a2d05494, monkova2025apreliminarystudy media b73f0830) | UTS 410 MPa; YS 240 MPa; elongation 5 ± 2% (monkova2025apreliminarystudy media a2d05494, monkova2025apreliminarystudy media b73f0830) |
| Minimum / typical acceptance properties from evidence | AM aluminum pressure component qualification | Hydraulic manifold qualification per SAE AS8775 / ARP1383 (arena2024novelaluminumalloy pages 8-11) | Proof pressure 1.5×DOP; burst pressure 2.5×DOP; example DOP = 207 bar → proof 310.5 bar, burst 517.5 bar; fatigue acceptance D < 1.0 and safety margin MS > 0.0 (arena2024novelaluminumalloy pages 8-11) |
| Minimum / typical acceptance properties from evidence | ASTM F3318 AlSi10Mg minima | The available evidence confirms ASTM F3318 is the governing finished-part specification for PBF-LB AlSi10Mg and that studies compare results against its minimum tensile-property requirements (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyof pages 1-11) | Exact numeric minima were not reproduced in available excerpts; they are typically specified directly in ASTM F3318 / purchaser-approved material specs and drawings (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyof pages 1-11) |
| Minimum / typical acceptance properties from evidence | Density / porosity / chemistry | Evidence shows these are acceptance topics under ISO/ASTM 52901, ISO/ASTM 52907, ASTM F3318, and aerospace qualification plans, with traceability and inspection requirements (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyof pages 104-106, ferramacho2025qualitystudyofa pages 101-104, russell2019qualificationandcertification pages 19-21) | No universal numeric density/porosity thresholds were reproduced in the available excerpts; these are usually contract-, standard-, or part-class-specific (ferramacho2025qualitystudyof pages 35-40, ferramacho2025qualitystudyofa pages 101-104, russell2019qualificationandcertification pages 19-21) |


*Table: This table summarizes the main ASTM, ISO/ASTM, and industry qualification frameworks used for additively manufactured aluminum parts, plus the explicit property thresholds available from the evidence. It is useful for distinguishing general qualification requirements from the few numeric acceptance values that were actually recoverable from the retrieved sources.*



References

1. (ferramacho2025qualitystudyof pages 35-40): ALSM Ferramacho. Quality study of parts for aeronautic sector produced by l-pbf: from feedstock to final product. Unknown journal, 2025.

2. (ferramacho2025qualitystudyofa pages 35-40): ALSM Ferramacho. Quality study of parts for aeronautic sector produced by l-pbf: from feedstock to final product. Unknown journal, 2025.

3. (diaz2022comparisonofmultiple pages 1-4): J. Diaz, K. Caballero, V.A. Medrano, E. Arrieta, M. Benedict, D. Godfrey, R. B. Wicker, and F. Medina. Comparison of multiple heat treatments by observing mechanical properties and microstructure of lpbf fabricated aluminum f357. Unknown, Jan 2022. URL: https://doi.org/10.26153/tsw/44561, doi:10.26153/tsw/44561. This article has 0 citations.

4. (caballero2023acomparisonof pages 1-3): K. Caballero, V.A. Medrano, E. Arrietam, J. Merino, B. Ruvalcaba, B. Ramirez, J. Diemann, L.E. Murr, R.B. Wicker, D. Godfrey, M. Benedict, and F. Medina. A comparison of the mechanical behavior of alsi7mg alloy produced through additive manufacturing and subjected to different heat treatment and aging conditions. ConferencePaper, Jan 2023. URL: https://doi.org/10.26153/tsw/50938, doi:10.26153/tsw/50938. This article has 0 citations.

5. (ferramacho2025qualitystudyofa pages 101-104): ALSM Ferramacho. Quality study of parts for aeronautic sector produced by l-pbf: from feedstock to final product. Unknown journal, 2025.

6. (ferramacho2025qualitystudyof pages 104-106): ALSM Ferramacho. Quality study of parts for aeronautic sector produced by l-pbf: from feedstock to final product. Unknown journal, 2025.

7. (afkhami2021metaladditivemanufacturing pages 38-40): Shahriar Afkhami, Mohsen Amraei, Anna Unt, Heidi Piili, and Timo Björk. Metal additive manufacturing for industrial applications. Text, Jan 2021. URL: https://doi.org/10.13140/rg.2.2.30891.35368, doi:10.13140/rg.2.2.30891.35368. This article has 4 citations and is from a peer-reviewed journal.

8. (poka2025qualityassurancevia pages 10-12): Konstantin Poka, Sozol Ali, Waleed Saeed, Benjamin Merz, Martin Epperlein, and Kai Hilgenberg. Quality assurance via a cyber physical system of a pbf-lb/m machine. Progress in Additive Manufacturing, 10:1771-1783, Feb 2025. URL: https://doi.org/10.1007/s40964-025-00978-w, doi:10.1007/s40964-025-00978-w. This article has 4 citations and is from a peer-reviewed journal.

9. (afkhami2021metaladditivemanufacturing pages 40-42): Shahriar Afkhami, Mohsen Amraei, Anna Unt, Heidi Piili, and Timo Björk. Metal additive manufacturing for industrial applications. Text, Jan 2021. URL: https://doi.org/10.13140/rg.2.2.30891.35368, doi:10.13140/rg.2.2.30891.35368. This article has 4 citations and is from a peer-reviewed journal.

10. (russell2019qualificationandcertification pages 6-9): Richard Russell, Douglas Wells, Jess Waller, Behrang Poorganji, Eric Ott, Tsuyoshi Nakagawa, Hector Sandoval, Nima Shamsaei, and Mohsen Seifi. Qualification and certification of metal additive manufactured hardware for aerospace applications. Additive Manufacturing for the Aerospace Industry, pages 33-66, Jan 2019. URL: https://doi.org/10.1016/b978-0-12-814062-8.00003-0, doi:10.1016/b978-0-12-814062-8.00003-0. This article has 139 citations.

11. (russell2019qualificationandcertification pages 11-15): Richard Russell, Douglas Wells, Jess Waller, Behrang Poorganji, Eric Ott, Tsuyoshi Nakagawa, Hector Sandoval, Nima Shamsaei, and Mohsen Seifi. Qualification and certification of metal additive manufactured hardware for aerospace applications. Additive Manufacturing for the Aerospace Industry, pages 33-66, Jan 2019. URL: https://doi.org/10.1016/b978-0-12-814062-8.00003-0, doi:10.1016/b978-0-12-814062-8.00003-0. This article has 139 citations.

12. (wells2018qualification&certification pages 1-16): DN Wells. Qualification & certification of additively manufactured parts for nasa applications. Unknown journal, 2018.

13. (russell2019qualificationandcertification pages 19-21): Richard Russell, Douglas Wells, Jess Waller, Behrang Poorganji, Eric Ott, Tsuyoshi Nakagawa, Hector Sandoval, Nima Shamsaei, and Mohsen Seifi. Qualification and certification of metal additive manufactured hardware for aerospace applications. Additive Manufacturing for the Aerospace Industry, pages 33-66, Jan 2019. URL: https://doi.org/10.1016/b978-0-12-814062-8.00003-0, doi:10.1016/b978-0-12-814062-8.00003-0. This article has 139 citations.

14. (russell2019qualificationandcertification pages 25-27): Richard Russell, Douglas Wells, Jess Waller, Behrang Poorganji, Eric Ott, Tsuyoshi Nakagawa, Hector Sandoval, Nima Shamsaei, and Mohsen Seifi. Qualification and certification of metal additive manufactured hardware for aerospace applications. Additive Manufacturing for the Aerospace Industry, pages 33-66, Jan 2019. URL: https://doi.org/10.1016/b978-0-12-814062-8.00003-0, doi:10.1016/b978-0-12-814062-8.00003-0. This article has 139 citations.

15. (huning2022advancementofcertification pages 46-47): Alexander Huning, Adam Smith, Luke Scime, Michael Russell, Alyson Coates, Vincent Paquit, and Ryan Dehoff. Advancement of certification methods and applications for industrial deployments of components derived from advanced manufacturing technologies. Oak Ridge National Laboratory Technical Report ORNL/TM-2022/2585, Sep 2022. URL: https://doi.org/10.2172/1890290, doi:10.2172/1890290. This article has 8 citations.

16. (russell2019qualificationandcertification pages 9-11): Richard Russell, Douglas Wells, Jess Waller, Behrang Poorganji, Eric Ott, Tsuyoshi Nakagawa, Hector Sandoval, Nima Shamsaei, and Mohsen Seifi. Qualification and certification of metal additive manufactured hardware for aerospace applications. Additive Manufacturing for the Aerospace Industry, pages 33-66, Jan 2019. URL: https://doi.org/10.1016/b978-0-12-814062-8.00003-0, doi:10.1016/b978-0-12-814062-8.00003-0. This article has 139 citations.

17. (arena2024novelaluminumalloy pages 8-11): Maurizio Arena, Bharat Mehta, Tommaso Tirelli, Paolo Ambrogiani, Martina Castaldo, Sven Bengtsson, and Lars Nyborg. Novel aluminum alloy tailored for additive manufacturing: structural characterization and qualification perspectives. Applied Sciences, 14:4647, May 2024. URL: https://doi.org/10.3390/app14114647, doi:10.3390/app14114647. This article has 0 citations.

18. (monkova2025apreliminarystudy media a2d05494): Katarina Monkova, Marianthi Bouzouni, George A. Pantazopoulos, Anagnostis I. Toulfatzis, and Sofia Papadopoulou. A preliminary study of the effect of 3d printing orientation on mechanical properties and fracture of samples made from alsi10mg. Materials, 18:5294, Nov 2025. URL: https://doi.org/10.3390/ma18235294, doi:10.3390/ma18235294. This article has 0 citations.

19. (monkova2025apreliminarystudy media b73f0830): Katarina Monkova, Marianthi Bouzouni, George A. Pantazopoulos, Anagnostis I. Toulfatzis, and Sofia Papadopoulou. A preliminary study of the effect of 3d printing orientation on mechanical properties and fracture of samples made from alsi10mg. Materials, 18:5294, Nov 2025. URL: https://doi.org/10.3390/ma18235294, doi:10.3390/ma18235294. This article has 0 citations.

20. (butler2020standardsinadditive pages 4-6): David Butler and Peter Woolliams. Standards in additive manufacturing. Precision Metal Additive Manufacturing, pages 133-156, Sep 2020. URL: https://doi.org/10.1201/9780429436543-6, doi:10.1201/9780429436543-6. This article has 5 citations.

21. (russell2019qualificationandcertification pages 16-19): Richard Russell, Douglas Wells, Jess Waller, Behrang Poorganji, Eric Ott, Tsuyoshi Nakagawa, Hector Sandoval, Nima Shamsaei, and Mohsen Seifi. Qualification and certification of metal additive manufactured hardware for aerospace applications. Additive Manufacturing for the Aerospace Industry, pages 33-66, Jan 2019. URL: https://doi.org/10.1016/b978-0-12-814062-8.00003-0, doi:10.1016/b978-0-12-814062-8.00003-0. This article has 139 citations.

22. (ferramacho2025qualitystudyof pages 1-11): ALSM Ferramacho. Quality study of parts for aeronautic sector produced by l-pbf: from feedstock to final product. Unknown journal, 2025.


---

## Query 5

**Question:** How do additively manufactured aluminum alloy properties compare to wrought aluminum alloys in the same composition system? Provide property-by-property comparisons for AlSi10Mg vs A360/A380, Scalmalloy vs 5xxx, and AM 2xxx/7xxx vs wrought 2024/7075.

**Task ID:** `d0ba0af5-19a6-462a-bb8b-e216638e4427`

**Status:** complete

## Summary
Additive manufacturing (AM) in aluminum is strongly property- and process-condition-dependent. In the same nominal composition system, AM commonly achieves **higher strength-to-weight and refined microstructures**, but the **defect population (porosity, lack-of-fusion, surface roughness)** often limits ductility and especially fatigue unless post-processing is optimized; conventional wrought/cast alloys generally show **more mature property consistency** and, for certain systems (5xxx), **better-characterized corrosion/EAC behavior**. The comparisons below are restricted to quantitative values present in the retrieved excerpts; missing values are explicitly marked as not available in those excerpts.

## Consolidated property-by-property comparison table
| System | Material / process condition | Yield strength | UTS | Elongation | Hardness | Density / porosity | Fatigue strength / limit | Fracture / tear / crack-growth notes | Corrosion / EAC notes | Notes |
|---|---|---:|---:|---:|---:|---|---|---|---|---|
| Al-Si-Mg | LPBF AlSi10Mg, as-built / stress-relieved literature set | not in retrieved excerpts | not in retrieved excerpts | 12% (EOS), 19% (LPW) | ~140 HV (as-built) | Relative density 96.4% as-built; porosity dominated by LoF/gas pores in sub-optimal build; gas pores typically <100 µm, LoF pores >100 µm and irregular | Strain-controlled, fully reversed; at strain amplitude 0.0010 mm/mm, stress amplitude ~73–74 MPa with runout >10,000,000 reversals (machined specimens) | Defects strongly orientation-sensitive; as-built microstructure gives high hardness/strength but T6 generally degrades them; pores/LoF defects govern fatigue initiation | not in retrieved excerpts | EOS/LPW M290 builds, stress-relieved only in Muhammad et al.; hardness/density from Kan et al. (muhammad2021acomparativeinvestigation pages 10-11, kan2019factorsthataffect pages 14-19, kan2019factorsthataffect pages 1-5) |
| Al-Si-Mg | LPBF AlSi10Mg, T5 | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | 122 ± 1 HB10 before fatigue runout; 110 ± 2 HB10 after runout | Crack initiation mostly from sub-surface gas/keyhole pores, 50–100 µm | Rotating-bending, room temperature: 92 ± 15 MPa; at 200 °C: 74 ± 12 MPa | Fatigue cracks initiate at killer pores; thermal exposure softens alloy | not in retrieved excerpts | Direct aging 4 h at 160 °C (egidio2023roomandhightemperature pages 7-9, egidio2023roomandhightemperature pages 1-2, egidio2023roomandhightemperature pages 9-13) |
| Al-Si-Mg | LPBF AlSi10Mg, rapid T6 (T6R) | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | 94 ± 3 HB10 before fatigue runout; 72 ± 2 HB10 after runout | As above; pore-driven initiation | Rotating-bending, room temperature: 108 ± 5 MPa; at 200 °C: 91 ± 4 MPa | Better fatigue than T5 despite lower hardness, attributed to strength-ductility balance and compressive residual stress | not in retrieved excerpts | Rapid solution 10 min at 510 °C + aging 6 h at 160 °C (egidio2023roomandhightemperature pages 7-9, egidio2023roomandhightemperature pages 1-2, egidio2023roomandhightemperature pages 9-13) |
| Al-Si-Mg | LPBF AlSi10Mg, T6 / HIP / HIP+T6 (sub-optimal-parameter study) | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | T6 reduces hardness by ~20% vs as-built; HIP by ~65%; HIP+T6 ~T6-only | Relative density: T6-only 96.1%, HIP-only 96.5%, HIP+T6 96.2%; HIP could not fully close gas-filled defects | Kan study: fatigue data not numerically reported in retrieved excerpt; Macías reports no total-fatigue-life improvement after HIP 497 °C + T6 or HIP 350 °C/300 MPa/2 h | HIP improves ductility but reduces strength; remaining/re-opened pores limit fatigue gains | not in retrieved excerpts | Use caution: these values come from intentionally sub-optimal LPBF parameters with unusually low density (~96%) (kan2019factorsthataffect pages 14-19, macias2022hotisostaticpressing pages 12-14) |
| Al-Si-Mg | HPDC A360, as-cast | 169–178 MPa | 289–310 MPa | 2.8–3.5% | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | Tear strength 235 MPa; total tear energy 1.474 N·m; TYR 1.39 | not in retrieved excerpts | Values from Lumley 2008 and Lumley 2019 handbook-style summary (lumley2019thedevelopmentof pages 2-5, lumley2008apreliminaryevaluation pages 3-4) |
| Al-Si-Mg | HPDC A360, T4 | 180 MPa | 297 MPa | 5.1% | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | Tear strength 277 MPa; total tear energy 2.88 N·m; TYR 1.54 | not in retrieved excerpts | Solution + natural aging (lumley2008apreliminaryevaluation pages 3-4) |
| Al-Si-Mg | HPDC A360, UA / T6 | 269 MPa (UA), 292 MPa (T6) | 330 MPa (UA), 335 MPa (T6) | 2.0% (UA), 1.7% (T6) | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | Tear strength 293 MPa (UA), 262 MPa (T6); total tear energy 1.422 N·m (UA), 1.042 N·m (T6); TYR 1.09 (UA), 0.90 (T6) | not in retrieved excerpts | T6 raises strength but reduces ductility and fracture resistance vs T4 (lumley2008apreliminaryevaluation pages 3-4) |
| Al-Si-Mg | HPDC A380, as-cast | 172–190 MPa | 300–354 MPa | 1.9–4.0% | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | Tear strength 218 MPa; total tear energy 0.918 N·m; TYR 1.15 | Cast-alloy corrosion generally inferior to wrought; modern processes including AM reviewed, but no numeric A380 corrosion values in retrieved excerpt | Range spans Lumley 2008 and Lumley 2019 / Udvardy cast-to-size data (lumley2019thedevelopmentof pages 2-5, lumley2008apreliminaryevaluation pages 3-4, udvardy2017castingsolutionsfor pages 10-14) |
| Al-Si-Mg | HPDC A380, T4 | 232 MPa | 338 MPa | 2.4% | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | Tear strength 311 MPa; total tear energy 1.693 N·m; TYR 1.34 | not in retrieved excerpts | T4 improves fracture resistance more than T6 (lumley2008apreliminaryevaluation pages 3-4) |
| Al-Si-Mg | HPDC A380, UA / T6 | 290 MPa (UA), 350 MPa (T6) | 362 MPa (UA), 393 MPa (T6) | 2.0% (UA), 1.2% (T6) | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | Tear strength 300 MPa (UA), 233 MPa (T6); total tear energy 1.443 N·m (UA), 0.625 N·m (T6); TYR 1.03 (UA), 0.67 (T6) | not in retrieved excerpts | T6 maximizes strength but strongly penalizes ductility/tear resistance (lumley2008apreliminaryevaluation pages 3-4) |
| Al-Mg-Sc-Zr vs 5xxx | LPBF Scalmalloy, stress-relieved / as-built type reports | ~450–480 MPa | ~520 MPa (one report); broader literature range 350–500 MPa | >10%, ~13%, or ~16% before aging depending on study | 95–170 HV (broad literature range) | Density >99%; one report 2.67 g/cm3; intrinsic pores ~200 µm in base material | Smooth-specimen fatigue at 10^8 cycles ~140–160 MPa; notched ~100–125 MPa; strain-controlled Scalmalloy runouts at stress amplitude ~145 MPa for strain amplitude 0.0020 mm/mm | Crack-growth behavior described as similar to AA7075-T7351/AA7050-T7451; aging can raise strength from ~400 to 480 MPa while reducing elongation from 16% to 4% | not in retrieved excerpts | Scalmalloy is precipitation-hardened AM alloy, not a direct wrought 5xxx analog, so comparison is strengthening-system-based rather than same temper/product form (mirandola2024microstructuresandmechanical pages 1-2, remorUnknownyearexperimentalanalysisof pages 29-34, jones2021characterisingcrackgrowth pages 1-3, jones2021describingcrackgrowth pages 1-2) |
| Al-Mg-Sc-Zr vs 5xxx | Wrought AA5083-H111/H116 representative 5xxx | 140 MPa (H111 excerpt); 120–235 MPa residual yield after thermal exposure in H116 study; room-temp UTS/elongation not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | EAC/fatigue-related threshold note: ST-plane splitting observed near Kmax ~20 MPa√m; overload near Kmax ~35 MPa√m | Sensitization/EAC vulnerability: plastic zone ~481 µm; ST split depths 43–462 µm (avg 235 ± 172 µm) | Strong sensitivity to sensitization: top-region GB coverage ~90% and ~100 nm GB precipitate thickness after 175 °C/100 h; middle region ~81% and ~80 nm; severe intergranular corrosion after sensitization | Representative wrought 5xxx benchmark is corrosion-resistant in benign condition but vulnerable to sensitization/EAC, unlike Scalmalloy literature retrieved here which focused more on strength/fatigue than corrosion (seifi2018sensitizationandremediation pages 10-12, summers2014residualmechanicalproperties pages 4-6, gao2019throughthicknessinhomogeneityof pages 12-20, abuzaid2021mechanicalpropertiesof pages 7-10) |
| 2xxx | LPBF 2024, raw/unmodified | 53 ± 3 MPa | 53 ± 3 MPa | 0.3 ± 0.1% | 108 ± 6 HVmean | not in retrieved excerpts | not in retrieved excerpts | Poor printability; hot cracking and porosity tied to columnar grains and wide solidification range | AA2024 in PBF-LB/M is challenging; no quantitative corrosion in this excerpted row | RAW-2024 from CaB6 study table (mair2022dependenceofmechanical pages 8-9) |
| 2xxx | LPBF 2024 + 2 wt% CaB6 (ND-2024), as-built | 348 ± 16 MPa | 391 ± 22 MPa | 12.6 ± 0.6% | 132 ± 4 HV5 | Density/processability improved; cracking largely eliminated qualitatively | not in retrieved excerpts | CaB6 gives equiaxed fine grains; Zener pinning and heterogeneous nucleation improve crack resistance | not in retrieved excerpts | Single composition point from Mair 2021 (mair2021laserpowderbed pages 7-8) |
| 2xxx | LPBF 2024 + CaB6, optimized content series, as-built | 333 ± 16 to 457 ± 5 MPa | 399 ± 20 to 482 ± 1 MPa | 3.8 ± 1.1% to 13.2 ± 0.1% | 129 ± 2 to 141 ± 2 HVmean | Crack- and pore-free processing claimed at suitable CaB6 levels | not in retrieved excerpts | Best balance near 1.0 wt% CaB6: 428 ± 3 MPa YS, 478 ± 4 MPa UTS, 13.2 ± 0.1% A; highest strength at 2.0 wt% CaB6: 457 ± 5 MPa YS, 482 ± 1 MPa UTS, 12.0 ± 0.4% A | Corrosion of AM AA2024 noted in references, but no numeric corrosion data in retrieved excerpts | Table 5 values across RAW and ND variants (mair2022dependenceofmechanical pages 8-9) |
| 2xxx | Wrought AA2024 benchmark | O: <140 MPa YS, <220 MPa UTS, >13% A; T3: >290 MPa YS, >435 MPa UTS, >14% A; T4: >275 MPa YS, >425 MPa UTS, >13% A; T6: 345 MPa YS, 435 MPa UTS, 5% A | same cell | same cell | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | Useful direct benchmark for LPBF-modified 2024 from Rasch review excerpt (rasch2019grainstructureevolution pages 1-3) |
| 7xxx | LPBF AA7075, unmodified | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | Relative density 99.50% in one parameter set, but crack density 154 cracks/cm²; extensive hot cracks | not in retrieved excerpts | Beam-based AM suffers hot cracking and vaporization losses (~25% Zn, ~32% Mg in prior report summarized by Yoder) | not in retrieved excerpts | Unmodified LPBF 7075 generally crack-prone (heiland2021requirementsforprocessing pages 12-15, yoder2021deformationbasedadditivemanufacturing pages 1-2, heiland2021requirementsforprocessing pages 10-12) |
| 7xxx | LPBF AA7075 + TiC nanoparticles, as-built | not in retrieved excerpts | UTS close to 330 MPa (best as-built tensile level reported) | not in retrieved excerpts | not in retrieved excerpts | Best density/crack combination at 2.5% TiC: 99.9% density, ~2 cracks/cm²; average grain size reduced to 1.7 µm | not in retrieved excerpts | TiC changes grains from columnar (~44.7 µm unmodified) to equiaxed; grain refinement alone insufficient unless grains <~2 µm | not in retrieved excerpts | Heiland as-built LPBF with modified powders; still below wrought 7075 strength (heiland2021requirementsforprocessing pages 12-15, heiland2021requirementsforprocessing pages 10-12) |
| 7xxx | Solid-state AM AA7075 (AFSD/MELD) + solution/aging | 477 MPa | 541 MPa | 8.2% | not in retrieved excerpts | No surface or interface porosity reported qualitatively | not in retrieved excerpts | Wrought-like properties retained without melting; avoids hot cracking and solute loss of beam-based AM | not in retrieved excerpts | Solid-state deposition, not LPBF; included because user asked for AM 2xxx/7xxx broadly (yoder2021deformationbasedadditivemanufacturing pages 1-2) |
| 7xxx | Wrought AA7075-T6 feed/reference | 503 MPa | 575 MPa | 10.5% | not in retrieved excerpts | not in retrieved excerpts | not in retrieved excerpts | Jones papers note Scalmalloy crack-growth behavior similar to AA7075-T7351 / AA7075-T6 master curves, but no 7075 fatigue numbers in retrieved excerpts | not in retrieved excerpts | Direct feed-material benchmark from Yoder (yoder2021deformationbasedadditivemanufacturing pages 1-2) |


*Table: This table compares retrieved property data for additively manufactured aluminum alloys against conventional counterparts across AlSi10Mg, Scalmalloy, and 2xxx/7xxx systems. It highlights where AM already exceeds, matches, or still trails legacy alloys, while flagging gaps where the retrieved excerpts did not provide numeric values.*

## 1) AlSi10Mg (AM) vs A360/A380 (conventional Al–Si–Mg casting family)
### Yield strength / UTS / elongation
* **Conventional HPDC A360/A380:**
  * A360 as-cast: YS 169 MPa, UTS 289 MPa, A 2.8%; A360-T6: YS 292 MPa, UTS 335 MPa, A 1.7%. (lumley2008apreliminaryevaluation pages 3-4)
  * A380 as-cast: YS 190 MPa, UTS 300 MPa, A 1.9%; A380-T6: YS 350 MPa, UTS 393 MPa, A 1.2%. (lumley2008apreliminaryevaluation pages 3-4)
  * A380 and A360 as-cast values in a separate HPDC summary are similar (e.g., A380: YS 172 MPa, UTS 354 MPa, A 4%; A360: YS 178 MPa, UTS 310 MPa, A 3.5%). (lumley2019thedevelopmentof pages 2-5)
* **LPBF AlSi10Mg:** the retrieved excerpts did **not** include room-temperature YS/UTS values for AlSi10Mg in a consistent as-built/T6/HIP condition, but they did report elongations for stress-relieved builds (EOS AlSi10Mg 12%; LPW AlSi10Mg 19%). (muhammad2021acomparativeinvestigation pages 10-11)

Interpretation: within this evidence set, conventional A360/A380 provide complete static tensile property sets, whereas AM AlSi10Mg is represented mainly by ductility and fatigue metrics; therefore, a full YS/UTS head-to-head cannot be completed from retrieved excerpts.

### Hardness
* LPBF AlSi10Mg hardness in one study: ~140 HV as-built; applying T6 reduces hardness by ~20%, HIP by ~65%, and HIP+T6 returns hardness comparable to T6-only. (kan2019factorsthataffect pages 14-19)
* In a separate LPBF fatigue study: Brinell hardness values reported for T5 (122 ± 1 HB10) and rapid T6 (T6R) (94 ± 3 HB10) conditions. (egidio2023roomandhightemperature pages 7-9)

### Density / porosity
* LPBF AlSi10Mg in Kan et al. used sub-optimal parameters and showed low relative density (~96.4% as-built; ~96.1–96.5% after T6/HIP/HIP+T6), with large lack-of-fusion defects that HIP could not close. (kan2019factorsthataffect pages 14-19)
* LPBF fatigue fractography indicates crack initiation from sub-surface gas/keyhole pores with Feret diameter ~50–100 µm. (egidio2023roomandhightemperature pages 9-13)

### Fatigue
* LPBF AlSi10Mg (rotating-bending, fully reversed) fatigue strengths:
  * T5: 92 ± 15 MPa (RT), 74 ± 12 MPa (200 °C). (egidio2023roomandhightemperature pages 9-13)
  * Rapid T6 (T6R): 108 ± 5 MPa (RT), 91 ± 4 MPa (200 °C). (egidio2023roomandhightemperature pages 1-2, egidio2023roomandhightemperature pages 9-13)
* LPBF AlSi10Mg strain-controlled fatigue (fully reversed) showed runout >10,000,000 reversals at stress amplitude ~73–74 MPa for εa = 0.0010 (machined specimens). (muhammad2021acomparativeinvestigation pages 10-11)

### Fracture resistance / tear toughness (conventional casting alloys)
* HPDC tear testing shows **T4 gives higher tear energies than T6** for A360/A380, even though T6 maximizes proof stress. For example A380: total tear energy 1.693 N·m (T4) vs 0.625 N·m (T6). (lumley2008apreliminaryevaluation pages 3-4)


## 2) Scalmalloy (AM Al–Mg–Sc–Zr) vs wrought 5xxx (Al–Mg) (e.g., AA5083)
### Yield strength / UTS / elongation
* LPBF Scalmalloy:
  * Reported YS > 450 MPa and elongation > 10% in two crack-growth papers. (jones2021describingcrackgrowth pages 1-2, jones2021characterisingcrackgrowth pages 1-3)
  * One experimental report: YS ~480 MPa, UTS ~520 MPa, elongation ~13%, modulus ~70 GPa, density 2.67 g/cm³. (remorUnknownyearexperimentalanalysisof pages 29-34)
  * Aging can increase strength from ~400 to ~480 MPa while reducing elongation from 16% to 4%. (mirandola2024microstructuresandmechanical pages 1-2)
* Wrought 5xxx (AA5083): room-temperature yield strength reported as 140 MPa for AA5083-H111 in one excerpt. (abuzaid2021mechanicalpropertiesof pages 7-10)

Interpretation: in the retrieved evidence, Scalmalloy’s YS (≈450–480 MPa) is substantially higher than the cited AA5083 value (140 MPa), reflecting that Scalmalloy is precipitation-strengthened (Al3(Sc,Zr)) rather than strain-hardened like typical 5xxx.

### Density / porosity
* LPBF Scalmalloy can exceed 99% density; intrinsic pore equivalent diameters ~200 µm in base material were reduced to ~60 µm after friction stir welding in one study. (mirandola2024microstructuresandmechanical pages 1-2)

### Fatigue
* LPBF Scalmalloy fatigue strength (reported as literature ranges in one excerpt): ~140–160 MPa at 10^8 cycles for smooth specimens; ~100–125 MPa for notched specimens. (mirandola2024microstructuresandmechanical pages 1-2)
* In strain-controlled fully reversed tests, Scalmalloy runouts were observed at stress amplitude ~145 MPa for εa = 0.0020 (machined specimens). (muhammad2021acomparativeinvestigation pages 10-11)

### Crack growth / damage tolerance
* Crack-growth behavior for AM Scalmalloy was reported as similar to aerospace 7xxx alloys (AA7075-T7351 / AA7050-T7451) in the Hartman–Schijve framework; numeric fracture toughness values were not in the excerpt. (jones2021describingcrackgrowth pages 1-2, jones2021characterisingcrackgrowth pages 1-3)

### Corrosion / EAC comparison (system-level)
* Wrought 5xxx (AA5083) exhibits well-known sensitization-driven IGC/EAC pathways:
  * Sensitized AA5083 shows quantified Mg-rich GB precipitation coverage/thickness differences through-thickness (e.g., top region ~90% GB coverage, ~100 nm thickness after 175 °C/100 h; middle ~81%, ~80 nm). (gao2019throughthicknessinhomogeneityof pages 12-20)
  * In EAC/fatigue contexts, ST-plane splitting correlated with Kmax, with splitting observed around Kmax ~20 MPa√m; split depths reported 43–462 µm (avg 235 ± 172 µm). (seifi2018sensitizationandremediation pages 10-12)
* Comparable corrosion/EAC metrics for Scalmalloy were not present in the retrieved excerpts; thus, only the 5xxx side can be quantitatively summarized here.


## 3) AM 2xxx/7xxx vs wrought 2024/7075
### 3.1 AM 2024 (LPBF, nanoparticle-modified) vs wrought 2024
**Wrought AA2024 benchmarks (from a PBF-LB/M 2024 discussion):**
* O temper: YS <140 MPa, UTS <220 MPa, A >13%
* T3: YS >290 MPa, UTS >435 MPa, A >14%
* T4: YS >275 MPa, UTS >425 MPa, A >13%
* T6: YS 345 MPa, UTS 435 MPa, A 5% (rasch2019grainstructureevolution pages 1-3)

**AM 2024 (LPBF + CaB6 nanoparticles):**
* Poor/unmodified (RAW-2024): YS 53 ± 3 MPa, UTS 53 ± 3 MPa, A 0.3 ± 0.1%, hardness 108 ± 6 HVmean. (mair2022dependenceofmechanical pages 8-9)
* With CaB6 additions (as-built series): strength and ductility increase dramatically; e.g.
  * ND-1.0-2024: YS 428 ± 3 MPa, UTS 478 ± 4 MPa, A 13.2 ± 0.1%, hardness 141 ± 1 HVmean. (mair2022dependenceofmechanical pages 8-9)
  * ND-2.0-2024: YS 457 ± 5 MPa, UTS 482 ± 1 MPa, A 12.0 ± 0.4%. (mair2022dependenceofmechanical pages 8-9)

Interpretation: within this evidence set, optimized LPBF 2024 with CaB6 achieves YS/UTS above the cited wrought 2024-T6 benchmark while maintaining elongation comparable to wrought T3/T4 levels. (mair2022dependenceofmechanical pages 8-9, rasch2019grainstructureevolution pages 1-3)

### 3.2 AM 7075 vs wrought 7075
**Printability limitation (LPBF):** AA7075 is prone to hot cracking in PBF-LB/M; TiC nanoparticle modification can reduce crack density and refine grains. (heiland2021requirementsforprocessing pages 12-15)

**AM 7075 (LPBF + TiC nanoparticles):**
* Relative densities up to 99.9% with low crack densities (~2 cracks/cm²) were achieved for 7075/TiC/2.5 under an identified parameter set; grain size reduced to ~1.7 µm under the best condition. (heiland2021requirementsforprocessing pages 10-12)
* Tensile: UTS “close to 330 MPa” reported in the as-built condition for TiC-modified variants. (heiland2021requirementsforprocessing pages 12-15)

**AM 7075 (solid-state AM, AFSD/MELD) vs wrought 7075-T6:**
* Printed AA7075 after solution/aging: YS 477 MPa, UTS 541 MPa, A 8.2%. (yoder2021deformationbasedadditivemanufacturing pages 1-2)
* Feed wrought AA7075-T6 (same lot): YS 503 MPa, UTS 575 MPa, A 10.5%. (yoder2021deformationbasedadditivemanufacturing pages 1-2)

Interpretation: in this evidence set, LPBF 7075 (even when crack-mitigated) remains well below wrought 7075-T6 strength in as-built tensile terms, whereas solid-state AM can approach wrought-like properties by avoiding melt-related cracking and solute loss. (heiland2021requirementsforprocessing pages 12-15, yoder2021deformationbasedadditivemanufacturing pages 1-2)


## Evidence limitations (explicit)
* Full **tensile property sets for LPBF AlSi10Mg** (YS/UTS/elongation in consistent as-built/T6/HIP conditions) were not present in the retrieved excerpts, so the AlSi10Mg vs A360/A380 comparison is strongest for **fatigue, hardness, density/defects, and casting-alloy fracture/tear trends** rather than a complete static-tensile head-to-head. (kan2019factorsthataffect pages 14-19, egidio2023roomandhightemperature pages 7-9, lumley2008apreliminaryevaluation pages 3-4)
* For the **Scalmalloy vs 5xxx** comparison, the retrieved excerpts provided limited room-temperature 5xxx tensile values (one yield value) and extensive 5xxx sensitization/EAC quantification; thus static strength differences are clear, but ductility/UTS and fatigue comparisons for 5xxx are incomplete from retrieved excerpts. (abuzaid2021mechanicalpropertiesof pages 7-10, seifi2018sensitizationandremediation pages 10-12, gao2019throughthicknessinhomogeneityof pages 12-20)



References

1. (muhammad2021acomparativeinvestigation pages 10-11): Muztahid Muhammad, P.D. Nezhadfar, Spencer Thompson, Ankit Saharan, Nam Phan, and Nima Shamsaei. A comparative investigation on the microstructure and mechanical properties of additively manufactured aluminum alloys. International Journal of Fatigue, 146:106165, May 2021. URL: https://doi.org/10.1016/j.ijfatigue.2021.106165, doi:10.1016/j.ijfatigue.2021.106165. This article has 145 citations and is from a domain leading peer-reviewed journal.

2. (kan2019factorsthataffect pages 14-19): Wen Hao Kan, Yves Nadot, Matthew Foley, Lionel Ridosz, Gwénaëlle Proust, and Julie M. Cairney. Factors that affect the properties of additively-manufactured alsi10mg: porosity versus microstructure. Additive Manufacturing, 29:100805, Oct 2019. URL: https://doi.org/10.1016/j.addma.2019.100805, doi:10.1016/j.addma.2019.100805. This article has 181 citations and is from a highest quality peer-reviewed journal.

3. (kan2019factorsthataffect pages 1-5): Wen Hao Kan, Yves Nadot, Matthew Foley, Lionel Ridosz, Gwénaëlle Proust, and Julie M. Cairney. Factors that affect the properties of additively-manufactured alsi10mg: porosity versus microstructure. Additive Manufacturing, 29:100805, Oct 2019. URL: https://doi.org/10.1016/j.addma.2019.100805, doi:10.1016/j.addma.2019.100805. This article has 181 citations and is from a highest quality peer-reviewed journal.

4. (egidio2023roomandhightemperature pages 7-9): Gianluca Di Egidio, Lorella Ceschini, Alessandro Morri, and Mattia Zanni. Room- and high-temperature fatigue strength of the t5 and rapid t6 heat-treated alsi10mg alloy produced by laser-based powder bed fusion. Metals, 13:263, Jan 2023. URL: https://doi.org/10.3390/met13020263, doi:10.3390/met13020263. This article has 15 citations.

5. (egidio2023roomandhightemperature pages 1-2): Gianluca Di Egidio, Lorella Ceschini, Alessandro Morri, and Mattia Zanni. Room- and high-temperature fatigue strength of the t5 and rapid t6 heat-treated alsi10mg alloy produced by laser-based powder bed fusion. Metals, 13:263, Jan 2023. URL: https://doi.org/10.3390/met13020263, doi:10.3390/met13020263. This article has 15 citations.

6. (egidio2023roomandhightemperature pages 9-13): Gianluca Di Egidio, Lorella Ceschini, Alessandro Morri, and Mattia Zanni. Room- and high-temperature fatigue strength of the t5 and rapid t6 heat-treated alsi10mg alloy produced by laser-based powder bed fusion. Metals, 13:263, Jan 2023. URL: https://doi.org/10.3390/met13020263, doi:10.3390/met13020263. This article has 15 citations.

7. (macias2022hotisostaticpressing pages 12-14): Juan Guillermo Santos Macías, Lv Zhao, David Tingaud, Brigitte Bacroix, Grzegorz Pyka, Camille van der Rest, Laurence Ryelandt, and Aude Simar. Hot isostatic pressing of laser powder bed fusion alsi10mg: parameter identification and mechanical properties. Journal of Materials Science, 57:9726-9740, Feb 2022. URL: https://doi.org/10.1007/s10853-022-07027-9, doi:10.1007/s10853-022-07027-9. This article has 39 citations and is from a peer-reviewed journal.

8. (lumley2019thedevelopmentof pages 2-5): Roger Lumley. The development of high strength and ductility in high-pressure die-cast al-si-mg alloys from secondary sources. JOM, 71:382-390, Sep 2019. URL: https://doi.org/10.1007/s11837-018-3121-8, doi:10.1007/s11837-018-3121-8. This article has 26 citations and is from a peer-reviewed journal.

9. (lumley2008apreliminaryevaluation pages 3-4): Roger N. Lumley. A preliminary evaluation on the fracture toughness of heat treated aluminium high pressure diecastings. Advanced Materials Research, 41-42:141-146, Apr 2008. URL: https://doi.org/10.4028/www.scientific.net/amr.41-42.141, doi:10.4028/www.scientific.net/amr.41-42.141. This article has 4 citations and is from a peer-reviewed journal.

10. (udvardy2017castingsolutionsfor pages 10-14): S Udvardy, B Glim, and S Midson. Casting solutions for readiness program: development of mechanical properties for high performance die casting alloys for specifications and standards/design …. Unknown journal, 2017.

11. (mirandola2024microstructuresandmechanical pages 1-2): Pietro Mirandola, David Novel, Matteo Perini, Matteo Benedetti, Franco Lombardi, Vincenzo Lunetto, and Pasquale Russo Spena. Microstructures and mechanical properties of friction stir welded additively manufactured scalmalloy®. The International Journal of Advanced Manufacturing Technology, 134:1645-1660, Aug 2024. URL: https://doi.org/10.1007/s00170-024-14237-9, doi:10.1007/s00170-024-14237-9. This article has 8 citations.

12. (remorUnknownyearexperimentalanalysisof pages 29-34): F Remor. Experimental analysis of fatigue behaviour and metallographic characterization of sc-al alloy coupons. Unknown journal, Unknown year.

13. (jones2021characterisingcrackgrowth pages 1-3): Rhys Jones, Jan Cizek, Ondrej Kovarik, Jeff Lang, Andrew Ang, and John G. Michopoulos. Characterising crack growth in scalmalloy. Procedia Structural Integrity, 34:39-44, Jan 2021. URL: https://doi.org/10.1016/j.prostr.2021.12.006, doi:10.1016/j.prostr.2021.12.006. This article has 1 citations and is from a peer-reviewed journal.

14. (jones2021describingcrackgrowth pages 1-2): Rhys Jones, Jan Cizek, Ondrej Kovarik, Jeff Lang, Andrew Ang, and John G. Michopoulos. Describing crack growth in additively manufactured scalmalloy. Additive Manufacturing Letters, 1:100020, Dec 2021. URL: https://doi.org/10.1016/j.addlet.2021.100020, doi:10.1016/j.addlet.2021.100020. This article has 16 citations and is from a peer-reviewed journal.

15. (seifi2018sensitizationandremediation pages 10-12): M. Seifi, I. Ghamarian, P. Samimi, P.C. Collins, N.J.H. Holroyd, and J.J. Lewandowski. Sensitization and remediation effects on environmentally assisted cracking of al-mg naval alloys. Corrosion Science, 138:219-241, Jul 2018. URL: https://doi.org/10.1016/j.corsci.2018.03.027, doi:10.1016/j.corsci.2018.03.027. This article has 43 citations and is from a highest quality peer-reviewed journal.

16. (summers2014residualmechanicalproperties pages 4-6): P.T. Summers, S.W. Case, and B.Y. Lattimer. Residual mechanical properties of aluminum alloys aa5083-h116 and aa6061-t651 after fire. Engineering Structures, 76:49-61, Oct 2014. URL: https://doi.org/10.1016/j.engstruct.2014.06.033, doi:10.1016/j.engstruct.2014.06.033. This article has 55 citations and is from a highest quality peer-reviewed journal.

17. (gao2019throughthicknessinhomogeneityof pages 12-20): Wenbin Gao, Dongpo Wang, Mohsen Seifi, and John J. Lewandowski. Through-thickness inhomogeneity of environmentally assisted cracking (eac) in aa5083-h128 alloy. Materials Science and Engineering: A, 740-741:34-48, Jan 2019. URL: https://doi.org/10.1016/j.msea.2018.10.079, doi:10.1016/j.msea.2018.10.079. This article has 32 citations.

18. (abuzaid2021mechanicalpropertiesof pages 7-10): Wael Abuzaid, Rami Hawileh, and Jamal Abdalla. Mechanical properties of strengthening 5083-h111 aluminum alloy plates at elevated temperatures. Infrastructures, 6:87, Jun 2021. URL: https://doi.org/10.3390/infrastructures6060087, doi:10.3390/infrastructures6060087. This article has 16 citations.

19. (mair2022dependenceofmechanical pages 8-9): Philipp Mair, Lukas Kaserer, Jakob Braun, Janko Stajkovic, Christian Klein, David Schimbäck, Lukas Perfler, Evgeny Zhuravlev, Olaf Kessler, and Gerhard Leichtfried. Dependence of mechanical properties and microstructure on solidification onset temperature for al2024–cab6 alloys processed using laser powder bed fusion. Materials Science and Engineering: A, 833:142552, Jan 2022. URL: https://doi.org/10.1016/j.msea.2021.142552, doi:10.1016/j.msea.2021.142552. This article has 41 citations.

20. (mair2021laserpowderbed pages 7-8): Philipp Mair, Valerie Sue Goettgens, Tobias Rainer, Nikolaus Weinberger, Ilse Letofsky-Papst, Stefan Mitsche, and Gerhard Leichtfried. Laser powder bed fusion of nano-cab6 decorated 2024 aluminum alloy. Journal of Alloys and Compounds, 863:158714, May 2021. URL: https://doi.org/10.1016/j.jallcom.2021.158714, doi:10.1016/j.jallcom.2021.158714. This article has 134 citations and is from a peer-reviewed journal.

21. (rasch2019grainstructureevolution pages 1-3): Michael Rasch, Johannes Heberle, Maximilian A. Dechet, Dominic Bartels, Martin R. Gotterbarm, Lukas Klein, Andrey Gorunov, Jochen Schmidt, Carolin Körner, Wolfgang Peukert, and Michael Schmidt. Grain structure evolution of al–cu alloys in powder bed fusion with laser beam for excellent mechanical properties. Materials, 13:82, Dec 2019. URL: https://doi.org/10.3390/ma13010082, doi:10.3390/ma13010082. This article has 33 citations.

22. (heiland2021requirementsforprocessing pages 12-15): Steffen Heiland, Benjamin Milkereit, Kay-Peter Hoyer, Evgeny Zhuravlev, Olaf Kessler, and Mirko Schaper. Requirements for processing high-strength alznmgcu alloys with pbf-lb/m to achieve crack-free and dense parts. Materials, 14:7190, Nov 2021. URL: https://doi.org/10.3390/ma14237190, doi:10.3390/ma14237190. This article has 21 citations.

23. (yoder2021deformationbasedadditivemanufacturing pages 1-2): Jake K. Yoder, R. Joey Griffiths, and Hang Z. Yu. Deformation-based additive manufacturing of 7075 aluminum with wrought-like mechanical properties. Materials &amp; Design, 198:109288, Jan 2021. URL: https://doi.org/10.1016/j.matdes.2020.109288, doi:10.1016/j.matdes.2020.109288. This article has 151 citations and is from a highest quality peer-reviewed journal.

24. (heiland2021requirementsforprocessing pages 10-12): Steffen Heiland, Benjamin Milkereit, Kay-Peter Hoyer, Evgeny Zhuravlev, Olaf Kessler, and Mirko Schaper. Requirements for processing high-strength alznmgcu alloys with pbf-lb/m to achieve crack-free and dense parts. Materials, 14:7190, Nov 2021. URL: https://doi.org/10.3390/ma14237190, doi:10.3390/ma14237190. This article has 21 citations.


---

## Query 6

**Question:** What Al-Cu-Mg-Ag and Al-Cu-Li alloys have been processed by LPBF or DED? Provide quantitative mechanical properties. These are important for aerospace high-temperature aluminum applications.

**Task ID:** `5e6a2e49-48b4-4c7a-a8f0-c6a3865d327c`

**Status:** complete

Additive-manufactured Al–Cu–Mg–Ag and Al–Cu–Li alloys with quantitative mechanical properties are currently supported in the retrieved corpus for (i) **LPBF Al2139 (Al–Cu–Mg–Ag)** and (ii) **DED (bypass-GMA) Al–5.51Cu–0.48Li**. A WAAM review also reports hardness changes for **WAAM (VP‑GTAW) 2050 (Al–Cu–Li)**, but not tensile properties.

A consolidated summary table is provided below.

| Alloy (designation/composition) | AM process (LPBF or DED variant) | Post-processing / heat treatment | Mechanical properties (RT tensile: YS/UTS/elongation; hardness; elevated-temp exposure if available) | Notes |
|---|---|---|---|---|
| **Al2139 (Al–Cu–Mg–Ag)** | **LPBF / PBF-LB/M** | **As-printed**; crack-free tensile specimens fabricated at selected parameters/energy density 1721 J/mm³. RT tensile test. (elambasseril2022effectofprocess pages 4-7, elambasseril2022effectofprocess pages 7-11, elambasseril2022effectofprocess media fb1d1464) | **RT tensile:** YS ~108 MPa, UTS ~226 MPa, elongation ~11% (elambasseril2022effectofprocess media fb1d1464) | Quantitative values were read from Fig. 13. Authors state PBF-LB/M Al2139 shows lower YS but better ductility than wrought/cast counterparts; significant Mg loss occurred during PBF-LB/M (Mg 0.60 wt.% in powder to 0.28 wt.% in printed alloy at 1721 J/mm³). (elambasseril2022effectofprocess pages 7-11, elambasseril2022effectofprocess pages 12-14, elambasseril2022effectofprocess media fb1d1464) |
| **Al2139 (Al–Cu–Mg–Ag)** | **LPBF / PBF-LB/M** | **T6:** homogenize 490 °C/24 h + solution treat 525 °C/2 h + water quench + age 160 °C/24 h. RT tensile test. (elambasseril2022effectofprocess pages 4-7) | **RT tensile:** YS ~302 MPa, UTS ~424 MPa, elongation ~11% (elambasseril2022effectofprocess media fb1d1464) | T6 markedly increased strength over as-printed. Lower YS than wrought Al2139 T8 was attributed to Mg evaporation/loss during high-energy LPBF. (elambasseril2022effectofprocess pages 12-14, elambasseril2022effectofprocess pages 14-15, elambasseril2022effectofprocess media fb1d1464) |
| **Al2139-AlTiB (Al–Cu–Mg–Ag + grain refiner)** | **LPBF / PBF-LB/M** | **As-printed** at same selected energy density (1721 J/mm³); RT tensile test. (elambasseril2022effectofprocess pages 4-7, elambasseril2022effectofprocess pages 7-11, elambasseril2022effectofprocess media fb1d1464) | **RT tensile:** YS ~95 MPa, UTS ~222 MPa, elongation ~16% (elambasseril2022effectofprocess media fb1d1464) | AlTiB reduced hot tearing and refined grains, but strength was slightly lower and ductility higher than unmodified Al2139; Mg loss also present (printed Mg ~0.23 wt.%). (elambasseril2022effectofprocess pages 7-11, elambasseril2022effectofprocess pages 12-14, elambasseril2022effectofprocess media fb1d1464) |
| **Al2139-AlTiB (Al–Cu–Mg–Ag + grain refiner)** | **LPBF / PBF-LB/M** | **T6:** homogenize 490 °C/24 h + solution treat 525 °C/2 h + water quench + age 160 °C/24 h. (elambasseril2022effectofprocess pages 4-7) | **RT tensile:** YS ~300 MPa, UTS ~430 MPa, elongation ~13% (elambasseril2022effectofprocess media fb1d1464) | Crack-free tensile specimens were produced; T6 improved strength strongly, but AlTiB variant still showed slightly lower strength and higher ductility than LPBF Al2139. (elambasseril2022effectofprocess pages 4-7, elambasseril2022effectofprocess pages 12-14, elambasseril2022effectofprocess media fb1d1464) |
| **Al–5.51Cu–0.48Li** (minor Mg/Zn/Mn/Ti/Fe/Zr also measured) | **DED / bypass-GMA DED** | **As-deposited, longitudinal** | **RT tensile:** YS 227 MPa, UTS 310 MPa, elongation 3.0% (cao2025anovelbypassgas pages 12-16) | In-situ synthesized Al–Cu–Li alloy. Longitudinal fracture tended to occur at interlayer fusion line, contributing to lower longitudinal strength than transverse. Alloy chemistry measured as Cu 5.51, Li 0.48, Mg 0.18, Zn 0.26, Mn 0.29, Ti 0.08, Fe 0.21, Zr 0.15 wt.%. (cao2025anovelbypassgas pages 1-3, cao2025anovelbypassgas pages 6-9, cao2025anovelbypassgas pages 16-18, cao2025anovelbypassgas pages 12-16) |
| **Al–5.51Cu–0.48Li** | **DED / bypass-GMA DED** | **As-deposited, transverse** | **RT tensile:** YS 250 MPa, UTS 371 MPa, elongation 5.18% (cao2025anovelbypassgas pages 12-16) | Transverse strength and ductility exceeded longitudinal values, consistent with anisotropic layer/fusion-boundary microstructure. Average microhardness of deposited alloy: **92.4 HV**. (cao2025anovelbypassgas pages 16-18, cao2025anovelbypassgas pages 12-16) |
| **Al–5.51Cu–0.48Li** | **DED / bypass-GMA DED** | **T6, longitudinal** | **RT tensile:** YS 440 MPa, UTS 492 MPa, elongation 2.5% (cao2025anovelbypassgas pages 12-16) | After T6, strengthening phases θ′, θ′′, δ′ and T1 were reported; longitudinal strength increased strongly but elongation decreased. (cao2025anovelbypassgas pages 1-3, cao2025anovelbypassgas pages 9-12, cao2025anovelbypassgas pages 12-16, cao2025anovelbypassgas pages 18-21) |
| **Al–5.51Cu–0.48Li** | **DED / bypass-GMA DED** | **T6, transverse** | **RT tensile:** YS 416 MPa, UTS 591 MPa, elongation 5.15%; average microhardness **146.4 HV** (cao2025anovelbypassgas pages 16-18, cao2025anovelbypassgas pages 12-16, cao2025anovelbypassgas pages 18-21) | Highest reported strength in this evidence set; quality index Q reported as 715 MPa. Hardness increased markedly after T6. (cao2025anovelbypassgas pages 16-18, cao2025anovelbypassgas pages 18-21) |
| **2050 Al–Cu–Li wire** | **DED / WAAM variant: VP-GTAW** | **Deposited vs. post-deposition heat-treated** | **Hardness only reported in review:** deposited **71 HV**; heat-treated **141 HV** (≈98.6% increase vs deposited; ≈55% above wire hardness 91 HV). (rodriguezgonzalez2023wirearcadditive pages 12-14) | Review states a thin straight wall was deposited successfully with 2050 wire; inner layers refined equiaxed grains, interlayers coarse columnar grains; θ (Al2Cu) and δ′ (Al3Li) dispersed along grain boundaries after post-deposition heat treatment. No tensile data given in available evidence. (rodriguezgonzalez2023wirearcadditive pages 12-14) |


*Table: This table summarizes the additively manufactured Al–Cu–Mg–Ag and Al–Cu–Li alloys supported by the retrieved evidence, including AM route, heat treatment, and quantitative mechanical properties. It is useful for quickly identifying which aerospace-relevant high-strength alloys have documented LPBF or DED processing and what property levels were achieved.*

## Al–Cu–Mg–Ag: LPBF (PBF‑LB/M) processed alloys
**Al2139 (Al–Cu–Mg–Ag) and Al2139‑AlTiB (grain-refined)** were processed by LPBF and tested in as‑printed and T6 conditions, with RT tensile properties reported from the mechanical-property chart (Fig. 13). (elambasseril2022effectofprocess media fb1d1464)

The paper specifies a **T6 heat treatment** (homogenize 490 °C/24 h; solution 525 °C/2 h; water quench; age 160 °C/24 h) and indicates tensile testing at **room temperature**. (elambasseril2022effectofprocess pages 4-7)

Quantitatively, Fig. 13 indicates approximately:
- **LPBF Al2139 (as‑printed):** YS ~108 MPa, UTS ~226 MPa, elong. ~11%. (elambasseril2022effectofprocess media fb1d1464)
- **LPBF Al2139 (T6):** YS ~302 MPa, UTS ~424 MPa, elong. ~11%. (elambasseril2022effectofprocess media fb1d1464)
- **LPBF Al2139‑AlTiB (as‑printed):** YS ~95 MPa, UTS ~222 MPa, elong. ~16%. (elambasseril2022effectofprocess media fb1d1464)
- **LPBF Al2139‑AlTiB (T6):** YS ~300 MPa, UTS ~430 MPa, elong. ~13%. (elambasseril2022effectofprocess media fb1d1464)

The authors attribute reduced yield strength vs wrought/cast benchmarks partly to **Mg evaporation/loss** during high‑energy LPBF; compositions measured in printed cubes (at 1721 J/mm³) show Mg reduced from 0.60 wt.% (powder) to 0.28 wt.% (Al2139) and 0.23 wt.% (Al2139‑AlTiB). (elambasseril2022effectofprocess pages 7-11, elambasseril2022effectofprocess pages 12-14)

## Al–Cu–Li: DED-processed alloys
### Bypass‑GMA DED (wire-based arc DED) Al–5.51Cu–0.48Li
Cao et al. report an **in‑situ synthesized Al–Cu–Li alloy** fabricated by **bypass‑GMA DED**; measured composition includes Cu 5.51 wt.% and Li 0.48 wt.% (with minor Mg/Zn/Mn/Ti/Fe/Zr). (cao2025anovelbypassgas pages 1-3, cao2025anovelbypassgas pages 6-9)

They provide **room-temperature tensile properties** in both **longitudinal and transverse** directions for **as‑deposited** and **T6** conditions:
- **As‑deposited, longitudinal:** YS 227 MPa, UTS 310 MPa, elong. 3.0%. (cao2025anovelbypassgas pages 12-16)
- **As‑deposited, transverse:** YS 250 MPa, UTS 371 MPa, elong. 5.18%. (cao2025anovelbypassgas pages 12-16)
- **T6, longitudinal:** YS 440 MPa, UTS 492 MPa, elong. 2.5%. (cao2025anovelbypassgas pages 12-16)
- **T6, transverse:** YS 416 MPa, UTS 591 MPa, elong. 5.15%. (cao2025anovelbypassgas pages 12-16)

Microhardness increased from ~**92.4 HV** (deposited) to ~**146.4 HV** (T6), and the T6 quality index Q was reported as 715 MPa. (cao2025anovelbypassgas pages 16-18, cao2025anovelbypassgas pages 18-21)

### WAAM (VP‑GTAW) 2050 wire: hardness change (tensile not reported in retrieved evidence)
A WAAM review reports that **VP‑GTAW WAAM** was applied to an Al–Cu–Li alloy using **2050 wire**, and provides microhardness values: **71 HV deposited** and **141 HV after post‑deposition heat treatment**. (rodriguezgonzalez2023wirearcadditive pages 12-14)

## Limitations of the current evidence set
- Within the retrieved and readable corpus, **Al2139** is the only Al–Cu–Mg–Ag alloy with directly extractable **LPBF tensile data**. Additional WAAM/DED studies on Al–Cu–Mg–Ag (including 2139 WAAM) were identified in search results but were not obtainable here (e.g., several 2023–2025 papers listed as unobtainable), so they cannot be quoted with quantitative properties in this answer.
- For Al–Cu–Li, the corpus contains strong quantitative data for **DED (bypass‑GMA) Al–5.51Cu–0.48Li**, but does not yet include an accessible experimental paper for **LPBF of a named commercial Al–Cu–Li grade** (e.g., 2195/2198/2199/2099) with tensile values.

Overall, the quantitative results above demonstrate that both **LPBF Al–Cu–Mg–Ag (Al2139)** and **DED Al–Cu–Li (Al–5.51Cu–0.48Li)** can reach aerospace-relevant strength levels after T6-type treatments, with notable anisotropy in DED and notable Mg-loss sensitivity in LPBF for Al–Cu–Mg–Ag systems. (elambasseril2022effectofprocess pages 12-14, cao2025anovelbypassgas pages 12-16)

References

1. (elambasseril2022effectofprocess pages 4-7): Joe Elambasseril, Michael J. Benoit, Suming Zhu, Mark A. Easton, Edward Lui, Craig A. Brice, Ma Qian, and Milan Brandt. Effect of process parameters and grain refinement on hot tearing susceptibility of high strength aluminum alloy 2139 in laser powder bed fusion. Progress in Additive Manufacturing, 7:887-901, Feb 2022. URL: https://doi.org/10.1007/s40964-021-00259-2, doi:10.1007/s40964-021-00259-2. This article has 49 citations and is from a peer-reviewed journal.

2. (elambasseril2022effectofprocess pages 7-11): Joe Elambasseril, Michael J. Benoit, Suming Zhu, Mark A. Easton, Edward Lui, Craig A. Brice, Ma Qian, and Milan Brandt. Effect of process parameters and grain refinement on hot tearing susceptibility of high strength aluminum alloy 2139 in laser powder bed fusion. Progress in Additive Manufacturing, 7:887-901, Feb 2022. URL: https://doi.org/10.1007/s40964-021-00259-2, doi:10.1007/s40964-021-00259-2. This article has 49 citations and is from a peer-reviewed journal.

3. (elambasseril2022effectofprocess media fb1d1464): Joe Elambasseril, Michael J. Benoit, Suming Zhu, Mark A. Easton, Edward Lui, Craig A. Brice, Ma Qian, and Milan Brandt. Effect of process parameters and grain refinement on hot tearing susceptibility of high strength aluminum alloy 2139 in laser powder bed fusion. Progress in Additive Manufacturing, 7:887-901, Feb 2022. URL: https://doi.org/10.1007/s40964-021-00259-2, doi:10.1007/s40964-021-00259-2. This article has 49 citations and is from a peer-reviewed journal.

4. (elambasseril2022effectofprocess pages 12-14): Joe Elambasseril, Michael J. Benoit, Suming Zhu, Mark A. Easton, Edward Lui, Craig A. Brice, Ma Qian, and Milan Brandt. Effect of process parameters and grain refinement on hot tearing susceptibility of high strength aluminum alloy 2139 in laser powder bed fusion. Progress in Additive Manufacturing, 7:887-901, Feb 2022. URL: https://doi.org/10.1007/s40964-021-00259-2, doi:10.1007/s40964-021-00259-2. This article has 49 citations and is from a peer-reviewed journal.

5. (elambasseril2022effectofprocess pages 14-15): Joe Elambasseril, Michael J. Benoit, Suming Zhu, Mark A. Easton, Edward Lui, Craig A. Brice, Ma Qian, and Milan Brandt. Effect of process parameters and grain refinement on hot tearing susceptibility of high strength aluminum alloy 2139 in laser powder bed fusion. Progress in Additive Manufacturing, 7:887-901, Feb 2022. URL: https://doi.org/10.1007/s40964-021-00259-2, doi:10.1007/s40964-021-00259-2. This article has 49 citations and is from a peer-reviewed journal.

6. (cao2025anovelbypassgas pages 12-16): F Cao, D Wang, Y Gu, J Shen, Z Bai, Z Tan, and Z Liang. A novel bypass-gas metal arc directed energy deposition for in-situ synthesis al–cu–li alloy. Unknown journal, 2025.

7. (cao2025anovelbypassgas pages 1-3): F Cao, D Wang, Y Gu, J Shen, Z Bai, Z Tan, and Z Liang. A novel bypass-gas metal arc directed energy deposition for in-situ synthesis al–cu–li alloy. Unknown journal, 2025.

8. (cao2025anovelbypassgas pages 6-9): F Cao, D Wang, Y Gu, J Shen, Z Bai, Z Tan, and Z Liang. A novel bypass-gas metal arc directed energy deposition for in-situ synthesis al–cu–li alloy. Unknown journal, 2025.

9. (cao2025anovelbypassgas pages 16-18): F Cao, D Wang, Y Gu, J Shen, Z Bai, Z Tan, and Z Liang. A novel bypass-gas metal arc directed energy deposition for in-situ synthesis al–cu–li alloy. Unknown journal, 2025.

10. (cao2025anovelbypassgas pages 9-12): F Cao, D Wang, Y Gu, J Shen, Z Bai, Z Tan, and Z Liang. A novel bypass-gas metal arc directed energy deposition for in-situ synthesis al–cu–li alloy. Unknown journal, 2025.

11. (cao2025anovelbypassgas pages 18-21): F Cao, D Wang, Y Gu, J Shen, Z Bai, Z Tan, and Z Liang. A novel bypass-gas metal arc directed energy deposition for in-situ synthesis al–cu–li alloy. Unknown journal, 2025.

12. (rodriguezgonzalez2023wirearcadditive pages 12-14): Paula Rodríguez-González, Elisa María Ruiz-Navas, and Elena Gordo. Wire arc additive manufacturing (waam) for aluminum-lithium alloys: a review. Materials, 16:1375, Feb 2023. URL: https://doi.org/10.3390/ma16041375, doi:10.3390/ma16041375. This article has 39 citations.


---

## Query 7

**Question:** What are the solidification path characteristics (freezing range, eutectic fraction, hot cracking index) for aluminum alloys processable by LPBF? Provide Scheil simulation or experimental data ranking alloy systems by printability.

**Task ID:** `162f0116-6ed4-4b8e-a312-a31dc061ab46`

**Status:** complete

## Scope and metrics
Solidification-path “printability” for LPBF Al alloys is commonly quantified with a Scheil-derived (or modified-Scheil) solidification-cracking index based on Kou’s criterion: the hot-cracking susceptibility (HCS/CSI) is taken as the maximum steepness of the terminal solidification curve, \(\max |dT/d\sqrt{f_s}|\), where \(f_s\) is the solid fraction; larger values imply poorer interdendritic liquid feeding and higher cracking risk (hyer2021compositiondependentsolidificationcracking pages 2-3, kou2015asimpleindex pages 1-2, singh2025understandingsolidificationcracking pages 49-54). Complementary solidification-path descriptors are (i) freezing range/solidification interval (e.g., liquidus–solidus, or a “brittleness” interval tied to high \(f_s\)), and (ii) eutectic fraction \(f_E\) (or terminal liquid/eutectic content), which tends to improve feeding and reduce cracking when high and interconnected.

## Quantitative solidification-path data for LPBF-relevant Al alloy systems
The table below consolidates the quantitative values that were extractable from the retrieved full-text (Scheil/equilibrium/modified Scheil/experimental) for LPBF-processable or LPBF-studied Al alloy systems, including freezing/solidification interval (when reported), eutectic fraction (or a measured eutectic/liquid fraction proxy), and hot-cracking indices.

| Alloy system / example composition | Data type | Freezing range or solidification interval (°C or K) with definition | Eutectic fraction or terminal liquid fraction | Hot cracking index / CSI / HCS definition and numeric value(s) | Printability outcome | Notes |
|---|---|---|---|---|---|---|
| Binary Al-Si, 0.5 wt% Si | Equilibrium/Kou Table 1 plus LPBF experiment | Not explicitly tabulated for 0.5 wt% in excerpt; low-Si side has a large interval, with maximum near the solubility limit and shrinking toward eutectic (hyer2021compositiondependentsolidificationcracking pages 3-3, hyer2021compositiondependentsolidificationcracking media 1577b2b2) | fE = 0.024 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Kou index max dT/d(√fs) = 5874.82; larger means higher susceptibility (hyer2021compositiondependentsolidificationcracking pages 3-3, hyer2021compositiondependentsolidificationcracking pages 2-3) | Hairline cracks observed; one analysis gives peak susceptibility at 0.5 wt% Si (hyer2021effectsofalloy pages 7-8) | Worst or near-worst printability in binary Al-Si despite small eutectic fraction |
| Binary Al-Si, 1.0 wt% Si | Equilibrium/Kou Table 1 plus LPBF experiment | Not explicitly tabulated; still in wide-interval hypoeutectic regime (hyer2021compositiondependentsolidificationcracking pages 3-3, hyer2021compositiondependentsolidificationcracking media 1577b2b2) | fE = 0.059 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Kou index = 2292.17 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Clear solidification cracking observed experimentally; maximum crack density occurred at 1.0 wt% Si (hyer2021effectsofalloy pages 7-8, hyer2021compositiondependentsolidificationcracking pages 1-2) | Experimentally more crack-prone than 0.5 wt% under LPBF, though the calculated peak can shift with diffusion |
| Binary Al-Si, 2.0 wt% Si | Equilibrium/Kou Table 1 plus LPBF experiment | Largest freezing range occurs near maximum Si solubility, about 76 °C at about 1.7 wt% Si; 2.0 wt% remains in the wide-range regime (hyer2021compositiondependentsolidificationcracking pages 3-3) | fE = 0.135 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Kou index = 944.74 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Solidification cracking observed experimentally (hyer2021effectsofalloy pages 7-8, hyer2021compositiondependentsolidificationcracking pages 1-2) | Higher eutectic fraction than 1 wt% Si but still crack-prone |
| Binary Al-Si, 4.0 wt% Si | Equilibrium/Kou Table 1 | Freezing range reduced relative to low-Si alloys; exact value not given in excerpt (hyer2021compositiondependentsolidificationcracking pages 3-3, hyer2021compositiondependentsolidificationcracking media 1577b2b2) | fE = 0.277 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Kou index = 449.00 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Predicted much better than 1 to 2 wt% Si; no cracking report in excerpt (hyer2021compositiondependentsolidificationcracking pages 3-3) | Intermediate printability; increased eutectic helps feeding |
| Binary Al-Si, 10.0 wt% Si | Equilibrium/Kou Table 1 plus LPBF practice | Approaches eutectic; freezing range very small (hyer2021compositiondependentsolidificationcracking pages 3-4, hyer2021compositiondependentsolidificationcracking media 1577b2b2) | fE = 0.769 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Kou index = 94.53 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Near-eutectic and high-Si Al-Si alloys are generally dense and crack-free in LPBF (hyer2021compositiondependentsolidificationcracking pages 1-2, liu2024alloydesignfor pages 14-15) | High eutectic fraction and narrow interval explain excellent printability |
| Binary Al-Si, 12.6 wt% Si eutectic | Equilibrium/Kou Table 1 plus LPBF practice | Freezing range = 0 at eutectic composition by definition in the table and figure summary (hyer2021compositiondependentsolidificationcracking pages 3-4, hyer2021compositiondependentsolidificationcracking media 1577b2b2) | fE = 1.000 (hyer2021compositiondependentsolidificationcracking pages 3-4, hyer2021compositiondependentsolidificationcracking pages 3-3) | Kou index = 0.000 (hyer2021compositiondependentsolidificationcracking pages 3-3) | Fully dense and crack-free comparator alloy in LPBF (hyer2021effectsofalloy pages 7-8, hyer2021compositiondependentsolidificationcracking pages 1-2) | Best printability benchmark among Al-Si compositions |
| Al7075 base, Al-4.01Zn-1.69Mg-1.51Cu-0.17Si | Equilibrium plus Scheil/Gulliver plus LPBF experiment | About 97 °C equilibrium solidification range, 630 to 533 °C (li2021investigationofsolidification pages 4-5) | Not numerically stated; wide interval and no strong eutectic healing in base alloy (li2021investigationofsolidification pages 2-3, li2021investigationofsolidification pages 4-5) | Kou index for baseline Al7075 = 6504, reported with C in text; metric is max dT/d(√fs) (li2021investigationofsolidification pages 15-16, li2021investigationofsolidification pages 1-2) | Extensive solidification cracks throughout as-built sample (li2021investigationofsolidification pages 15-16, li2021investigationofsolidification pages 1-2, li2021investigationofsolidification pages 12-14) | Very poor LPBF printability in unmodified 7xxx state |
| 7075 plus Zn/Mg-adjusted composition | Kou-model design study | Freezing range not separately reported in excerpt (li2021investigationofsolidification pages 15-16, li2021investigationofsolidification pages 2-3) | Not numerically stated (li2021investigationofsolidification pages 2-3) | Kou index reduced from 6504 to 5966 by Zn and Mg adjustment (li2021investigationofsolidification pages 15-16, li2021investigationofsolidification pages 1-2) | Improvement predicted but susceptibility remains high; crack-free state not yet attributed to this step alone (li2021investigationofsolidification pages 15-16) | Intermediate design step before Si addition |
| Si-modified 7075, Al-5.10Zn-2.67Mg-1.55Cu-3.74Si | Equilibrium plus Scheil/Gulliver plus DSC plus LPBF experiment | About 94 °C equilibrium solidification range, 610 to 516 °C; liquidus lowered by about 20 °C versus base 7075 (li2021investigationofsolidification pages 4-5) | Si promotes eutectic alpha-Al/Si formation; exact fE not reported in excerpt (li2021investigationofsolidification pages 2-3, li2021investigationofsolidification pages 4-5) | Kou index = 3960 at 3.74 wt% Si; lowest susceptibility reported for about 3 to 4 wt% Si range (li2021investigationofsolidification pages 15-16, li2021investigationofsolidification pages 1-2) | Crack-free LPBF parts with relative density above 99.94% (li2021investigationofsolidification pages 15-16, li2021investigationofsolidification pages 1-2) | Demonstrates eutectic-assisted healing strategy for crack-prone 7xxx alloys |
| AA2219 LPBF, non-cracked RF location | Modified Scheil plus experiment | Solidus reported as 821 K; explicit freezing range not given in excerpt (singh2025understandingsolidificationcracking pages 54-59) | Measured eutectic fraction 12.7 ± 2.3 vol%; terminal liquid fraction about 4 vol% in non-cracked region (singh2025understandingsolidificationcracking pages 49-54, singh2025understandingsolidificationcracking pages 45-49, singh2025understandingsolidificationcracking pages 39-45) | HCS = 21 using Kou-type max dT/d(√fs) from modified Scheil with tip undercooling (singh2025understandingsolidificationcracking pages 49-54) | Non-cracked or lower cracking susceptibility (singh2025understandingsolidificationcracking pages 49-54) | Higher eutectic fraction and lower terminal liquid fraction correlated with crack resistance |
| AA2219 LPBF, highly cracked 45°(T) location | Modified Scheil plus experiment | Solidus reported as 821 K; explicit freezing range not given in excerpt (singh2025understandingsolidificationcracking pages 54-59) | Measured eutectic fraction 7.3 ± 0.6 vol%; terminal liquid fraction about 9 vol% in highly cracked zone (singh2025understandingsolidificationcracking pages 49-54, singh2025understandingsolidificationcracking pages 45-49, singh2025understandingsolidificationcracking pages 39-45) | HCS = 42, about 2 times the RF value (singh2025understandingsolidificationcracking pages 49-54) | Highly cracked (singh2025understandingsolidificationcracking pages 49-54) | Lower eutectic fraction and higher retained liquid at terminal stage correlated with cracking |
| AA6xxx series commercial Al-Mg-Si-Cu family | Improved Scheil with back diffusion, high-throughput CSI maps | Series-level comparison; no single freezing range given in excerpt (zhang2021predictionofcracking pages 14-15, zhang2021predictionofcracking pages 9-12, zhang2021predictionofcracking pages 7-9) | No single fE value; high-risk tail follows Mg/Si ratio about 1.6 to 2.0 near Mg2Si stoichiometry (zhang2021predictionofcracking pages 14-15, zhang2021predictionofcracking pages 7-9) | CSI scale maximum = 7; most commercial AA6xxx alloys fall at CSI about 3 to 5, lowest among AA2xxx, AA6xxx, and AA7xxx sets (zhang2021predictionofcracking pages 14-15, zhang2021predictionofcracking pages 9-12) | Best overall printability among these commercial wrought series, though Cu raises susceptibility (zhang2021predictionofcracking pages 14-15, zhang2021predictionofcracking pages 9-12) | Commercially still less printable than near-eutectic Al-Si, but better than 2xxx and 7xxx |
| AA2xxx series summary | Improved Scheil with back diffusion, high-throughput CSI maps | Series-level comparison only; no single freezing range in excerpt (zhang2021predictionofcracking pages 14-15, zhang2021predictionofcracking pages 7-9) | No single fE value; Fe and Mn removal slightly lowers susceptibility (zhang2021predictionofcracking pages 7-9) | CSI scale maximum = 12; most AA2xxx alloys fall at CSI about 3 to 8 (zhang2021predictionofcracking pages 14-15) | More crack susceptible than AA6xxx; LPBF often requires alloy modification or process tailoring (zhang2021predictionofcracking pages 14-15) | Broad family includes AA2219, whose local HCS values show strong location sensitivity |
| AA7xxx series summary | Improved Scheil with back diffusion, high-throughput CSI maps | Series-level comparison only; no single freezing range in excerpt (zhang2021predictionofcracking pages 14-15, zhang2021predictionofcracking pages 9-12, zhang2021predictionofcracking pages 12-14) | No single fE value; most susceptible stripe runs roughly from 6Zn-2Mg to 10Zn-1Mg; Cu and low back diffusion worsen susceptibility (zhang2021predictionofcracking pages 9-12, zhang2021predictionofcracking pages 12-14) | CSI scale maximum = 12; most AA7xxx alloys fall at CSI about 3 to 8; vulnerable compositions are widened by about 0.5 wt% Cu (zhang2021predictionofcracking pages 14-15, zhang2021predictionofcracking pages 12-14) | Generally poor LPBF printability without composition modification; Si-modified 7075 is a key exception (li2021investigationofsolidification pages 15-16, zhang2021predictionofcracking pages 12-14) | High-strength but crack-prone family |
| Near-eutectic Al-Ce, for example about Al-10.6Ce or AlCe10MgSi | Phase-diagram or Scheil-informed alloy design plus LPBF experiments | Binary Al-Ce eutectic at about 10.6 wt% Ce and about 644.5 °C; full freezing range not given in excerpt (hesselmann2022effectofprecipitationforming pages 1-3, hesselmann2022effectofprecipitationforming pages 3-5) | Quantitative eutectic fraction not given in available excerpt; near-eutectic compositions intentionally maximize eutectic solidification (hesselmann2022effectofprecipitationforming pages 1-3, hesselmann2022effectofprecipitationforming pages 3-5) | No numeric Kou or CSI value available in provided text (hesselmann2022effectofprecipitationforming pages 11-14, hesselmann2022effectofprecipitationforming pages 1-3) | Reported high melt fluidity, wide LPBF processing window, and crack-free near-eutectic Al-Ce samples (hesselmann2022effectofprecipitationforming pages 1-3) | Strong practical printability evidence, but fewer numeric solidification-path metrics are available in the retrieved excerpts |


*Table: This table consolidates extracted Scheil, improved-Scheil, equilibrium, and experimental solidification-path metrics for LPBF-processable aluminum alloy systems. It aligns freezing range, eutectic or terminal liquid behavior, and Kou-type hot-cracking indices with observed cracked versus crack-free outcomes.*

Key image-backed evidence for Al–Si: Hyer et al. provide freezing-range trends vs Si, tabulated eutectic fractions \(f_E\), and the Kou index \(\max |dT/d\sqrt{f_s}|\) versus composition; these are shown in their Figure/Table set (hyer2021compositiondependentsolidificationcracking media 1577b2b2, hyer2021compositiondependentsolidificationcracking media f8afade2, hyer2021compositiondependentsolidificationcracking media d0ab0ffa, hyer2021compositiondependentsolidificationcracking media a6538230).

## Ranking alloy systems by printability from solidification-path metrics
Because different sources use different absolute normalizations (Kou index in °C units, series-level CSI maps, or modified-Scheil HCS), the most defensible ranking is within each alloy family, plus a cross-family qualitative ordering anchored by (i) very low Kou index near eutectics, (ii) narrow freezing range, and (iii) high eutectic fraction/terminal eutectic liquid.

### A. Al–Si (binary; benchmark LPBF-printable family)
**Best printability (lowest cracking risk): near-eutectic/hypereutectic Al–Si**. At the eutectic composition (12.6 wt% Si), the freezing range collapses to ~0, \(f_E=1\), and the Kou index goes to 0 in Hyer et al.’s tabulation (hyer2021compositiondependentsolidificationcracking pages 3-4, hyer2021compositiondependentsolidificationcracking pages 3-3, hyer2021compositiondependentsolidificationcracking media 1577b2b2). At 10 wt% Si, \(f_E\) is already high (~0.769) and Kou index is low (~94.5) (hyer2021compositiondependentsolidificationcracking pages 3-3). These compositions correspond to widely observed dense, crack-free LPBF outcomes (hyer2021compositiondependentsolidificationcracking pages 1-2).

**Poor printability (highest cracking risk): low-Si hypoeutectic Al–Si (~0.5–2 wt% Si)**. Hyer et al.’s Kou index is very high at 0.5 wt% Si (5874.8) and remains elevated at 1 wt% Si (2292.2) and 2 wt% Si (944.7), with small eutectic fractions (\(f_E\) from 0.024 to 0.135) (hyer2021compositiondependentsolidificationcracking pages 3-3). In LPBF experiments, the 1 and 2 wt% Si alloys exhibited solidification cracking (hyer2021compositiondependentsolidificationcracking pages 1-2), and the experimentally measured maximum crack density occurred at ~1 wt% Si in a related analysis (hyer2021effectsofalloy pages 7-8).

**Al–Si printability ordering (best → worst)**: ~12.6Si ≈ 10Si ≫ 4Si ≫ 2Si ≳ 1Si ≳ 0.5Si, consistent with the monotonic rise in \(f_E\) and strong reduction in Kou index as Si approaches eutectic (hyer2021compositiondependentsolidificationcracking pages 3-3, hyer2021compositiondependentsolidificationcracking media 1577b2b2).

### B. 7xxx-type Al–Zn–Mg–Cu (high-strength, crack-prone; improved by eutectic engineering)
**Base 7075 is highly crack-susceptible** by Kou index: 6504 (reported as “C” in the source text) and exhibits extensive solidification cracking throughout the as-built LPBF microstructure (li2021investigationofsolidification pages 15-16, li2021investigationofsolidification pages 1-2).

**Eutectic engineering with Si substantially improves printability**: a Si-modified 7075-type alloy (Al-5.10Zn-2.67Mg-1.55Cu-3.74Si) reduced the Kou index to 3960 and enabled crack-free LPBF parts (relative density 99.94%) (li2021investigationofsolidification pages 15-16, li2021investigationofsolidification pages 1-2). Equilibrium solidification intervals reported for base and Si-modified compositions are both wide (~97 °C and ~94 °C), so the improvement is attributed primarily to modified terminal solidification behavior (eutectic α-Al/Si formation) rather than a dramatic collapse of the total equilibrium freezing range (li2021investigationofsolidification pages 2-3, li2021investigationofsolidification pages 4-5).

At the broader series level (improved Scheil with back diffusion), AA7xxx alloys show higher peak cracking indices than AA6xxx: the AA7xxx CSI scale has a maximum of 12, and susceptibility depends strongly on Cu and the Zn–Mg balance (zhang2021predictionofcracking pages 14-15, zhang2021predictionofcracking pages 12-14).

### C. 2xxx-type Al–Cu (example: AA2219; location-dependent cracking)
AA2219 in LPBF shows that **terminal liquid/eutectic fraction and Kou-type HCS can discriminate cracked vs non-cracked conditions within the same nominal alloy**. In a location-dependent study, measured eutectic (Al2Cu) fractions were 12.7 ± 2.3 vol% (non-cracked RF location) versus 7.3 ± 0.6 vol% (highly cracked 45°(T) location) (singh2025understandingsolidificationcracking pages 49-54). Using a modified Scheil approach with tip undercooling, the authors reported terminal liquid fractions of ~4 vol% (non-cracked) versus ~9 vol% (highly cracked) and corresponding HCS values of 21 versus 42, respectively (singh2025understandingsolidificationcracking pages 49-54). Thus, higher HCS coincided with the cracked location, and reduced eutectic fraction was implicated in poorer feeding and higher cracking (singh2025understandingsolidificationcracking pages 49-54).

At the broader series level, AA2xxx also reaches a maximum CSI of 12 (higher than AA6xxx) in the improved-Scheil high-throughput maps (zhang2021predictionofcracking pages 14-15).

### D. 6xxx-type Al–Mg–Si (generally more crack-resistant among wrought series; still composition-sensitive)
High-throughput improved-Scheil maps predict **lower overall cracking susceptibility for AA6xxx than AA2xxx/AA7xxx**, with AA6xxx maximum CSI = 7 and most AA6xxx alloys falling around CSI ≈ 3–5 (zhang2021predictionofcracking pages 14-15). However, a composition “tail” of higher susceptibility follows \(w(Mg)/w(Si)\approx 1.6–2.0\) (near Mg2Si stoichiometry), and Cu increases susceptibility (zhang2021predictionofcracking pages 14-15, zhang2021predictionofcracking pages 7-9).

### E. Near-eutectic Al–Ce (emerging LPBF-printable family; limited numeric solidification metrics in retrieved text)
Near-eutectic Al–Ce alloys are frequently reported as LPBF-processable with wide parameter windows and crack-free builds. The Al–Ce eutectic is near 10.6 wt% Ce at ~644.5 °C, and prior work is cited as reporting crack-free LPBF samples for near-eutectic compositions (hesselmann2022effectofprecipitationforming pages 1-3). However, in the retrieved excerpts, explicit eutectic fractions, freezing ranges, and Kou/CSI values were not numerically tabulated for Al–Ce(-Mg/Si) compositions, limiting a strictly quantitative ranking against Al–Si or modified 7xxx systems (hesselmann2022effectofprecipitationforming pages 11-14, hesselmann2022effectofprecipitationforming pages 3-5).

## Overall printability ordering (based on available quantitative indices)
1. **Near-eutectic Al–Si (~10–12.6 wt% Si)**: minimal freezing range and near-zero Kou index at eutectic; consistently crack-free in LPBF (hyer2021compositiondependentsolidificationcracking pages 3-3, hyer2021compositiondependentsolidificationcracking pages 1-2, hyer2021compositiondependentsolidificationcracking media 1577b2b2).
2. **Moderate-Si Al–Si (~4 wt% Si)**: reduced index (\~449) and higher eutectic fraction (\~0.277) than low-Si Al–Si; expected improved printability vs low-Si Al–Si (hyer2021compositiondependentsolidificationcracking pages 3-3).
3. **Commercial wrought-series baseline tendency (series-level CSI)**: **AA6xxx generally more crack-resistant than AA2xxx/AA7xxx** (max CSI 7 vs 12) (zhang2021predictionofcracking pages 14-15).
4. **Modified high-strength 7xxx (e.g., Si-modified 7075-type)**: crack-free achievable with engineered eutectic solidification despite still-large Kou index relative to Al–Si benchmarks (3960) (li2021investigationofsolidification pages 15-16).
5. **Crack-prone zones/conditions in 2xxx and unmodified 7xxx**: base 7075 (Kou index 6504; pervasive cracking) and highly cracked AA2219 conditions (HCS 42) (li2021investigationofsolidification pages 15-16, singh2025understandingsolidificationcracking pages 49-54).

## Limitations of the present synthesis
The retrieved full texts provide strong quantitative ranking for Al–Si and for a Si-modified 7075 strategy, plus illustrative AA2219 location-dependent HCS/eutectic-fraction data. Comparable numeric Scheil-derived freezing ranges, eutectic fractions, and Kou indices for additional LPBF-developed alloy families (e.g., Al–Sc–Zr, Al–Fe–Ni, Al–Ce–Mg) were not present in the available excerpts, so they are not ranked quantitatively here beyond qualitative printability statements (hesselmann2022effectofprecipitationforming pages 1-3).

References

1. (hyer2021compositiondependentsolidificationcracking pages 2-3): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.

2. (kou2015asimpleindex pages 1-2): S Kou. A simple index for predicting the susceptibility to solidification cracking. Unknown journal, 2015.

3. (singh2025understandingsolidificationcracking pages 49-54): A Singh. Understanding solidification cracking as a function of part-specific location during laser powder bed fusion of aa2219. Unknown journal, 2025.

4. (hyer2021compositiondependentsolidificationcracking pages 3-3): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.

5. (hyer2021compositiondependentsolidificationcracking media 1577b2b2): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.

6. (hyer2021effectsofalloy pages 7-8): Holden Hyer, Le Zhou, Abhishek Mehta, and Yongho Sohn. Effects of alloy composition and solid-state diffusion kinetics on powder bed fusion cracking susceptibility. Journal of Phase Equilibria and Diffusion, 42:5-13, Nov 2021. URL: https://doi.org/10.1007/s11669-020-00844-y, doi:10.1007/s11669-020-00844-y. This article has 38 citations and is from a peer-reviewed journal.

7. (hyer2021compositiondependentsolidificationcracking pages 1-2): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.

8. (hyer2021compositiondependentsolidificationcracking pages 3-4): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.

9. (liu2024alloydesignfor pages 14-15): Zhuangzhuang Liu, Qihang Zhou, Xiaokang Liang, Xiebin Wang, Guichuan Li, Kim Vanmeensel, and Jianxin Xie. Alloy design for laser powder bed fusion additive manufacturing: a critical review. International Journal of Extreme Manufacturing, 6:022002, Jan 2024. URL: https://doi.org/10.1088/2631-7990/ad1657, doi:10.1088/2631-7990/ad1657. This article has 104 citations.

10. (li2021investigationofsolidification pages 4-5): Guichuan Li, Suraj Dinkar Jadhav, Arturo Martín, Maria L. Montero-Sistiaga, Jeroen Soete, Maria San Sebastian, Carmen M. Cepeda-Jiménez, and Kim Vanmeensel. Investigation of solidification and precipitation behavior of si-modified 7075 aluminum alloy fabricated by laser-based powder bed fusion. Metallurgical and Materials Transactions A, 52:194-210, Nov 2021. URL: https://doi.org/10.1007/s11661-020-06073-9, doi:10.1007/s11661-020-06073-9. This article has 77 citations.

11. (li2021investigationofsolidification pages 2-3): Guichuan Li, Suraj Dinkar Jadhav, Arturo Martín, Maria L. Montero-Sistiaga, Jeroen Soete, Maria San Sebastian, Carmen M. Cepeda-Jiménez, and Kim Vanmeensel. Investigation of solidification and precipitation behavior of si-modified 7075 aluminum alloy fabricated by laser-based powder bed fusion. Metallurgical and Materials Transactions A, 52:194-210, Nov 2021. URL: https://doi.org/10.1007/s11661-020-06073-9, doi:10.1007/s11661-020-06073-9. This article has 77 citations.

12. (li2021investigationofsolidification pages 15-16): Guichuan Li, Suraj Dinkar Jadhav, Arturo Martín, Maria L. Montero-Sistiaga, Jeroen Soete, Maria San Sebastian, Carmen M. Cepeda-Jiménez, and Kim Vanmeensel. Investigation of solidification and precipitation behavior of si-modified 7075 aluminum alloy fabricated by laser-based powder bed fusion. Metallurgical and Materials Transactions A, 52:194-210, Nov 2021. URL: https://doi.org/10.1007/s11661-020-06073-9, doi:10.1007/s11661-020-06073-9. This article has 77 citations.

13. (li2021investigationofsolidification pages 1-2): Guichuan Li, Suraj Dinkar Jadhav, Arturo Martín, Maria L. Montero-Sistiaga, Jeroen Soete, Maria San Sebastian, Carmen M. Cepeda-Jiménez, and Kim Vanmeensel. Investigation of solidification and precipitation behavior of si-modified 7075 aluminum alloy fabricated by laser-based powder bed fusion. Metallurgical and Materials Transactions A, 52:194-210, Nov 2021. URL: https://doi.org/10.1007/s11661-020-06073-9, doi:10.1007/s11661-020-06073-9. This article has 77 citations.

14. (li2021investigationofsolidification pages 12-14): Guichuan Li, Suraj Dinkar Jadhav, Arturo Martín, Maria L. Montero-Sistiaga, Jeroen Soete, Maria San Sebastian, Carmen M. Cepeda-Jiménez, and Kim Vanmeensel. Investigation of solidification and precipitation behavior of si-modified 7075 aluminum alloy fabricated by laser-based powder bed fusion. Metallurgical and Materials Transactions A, 52:194-210, Nov 2021. URL: https://doi.org/10.1007/s11661-020-06073-9, doi:10.1007/s11661-020-06073-9. This article has 77 citations.

15. (singh2025understandingsolidificationcracking pages 54-59): A Singh. Understanding solidification cracking as a function of part-specific location during laser powder bed fusion of aa2219. Unknown journal, 2025.

16. (singh2025understandingsolidificationcracking pages 45-49): A Singh. Understanding solidification cracking as a function of part-specific location during laser powder bed fusion of aa2219. Unknown journal, 2025.

17. (singh2025understandingsolidificationcracking pages 39-45): A Singh. Understanding solidification cracking as a function of part-specific location during laser powder bed fusion of aa2219. Unknown journal, 2025.

18. (zhang2021predictionofcracking pages 14-15): Fan Zhang, Songmao Liang, Chuan Zhang, Shuanglin Chen, Duchao Lv, Weisheng Cao, and Sindo Kou. Prediction of cracking susceptibility of commercial aluminum alloys during solidification. Metals, 11:1479, Sep 2021. URL: https://doi.org/10.3390/met11091479, doi:10.3390/met11091479. This article has 23 citations.

19. (zhang2021predictionofcracking pages 9-12): Fan Zhang, Songmao Liang, Chuan Zhang, Shuanglin Chen, Duchao Lv, Weisheng Cao, and Sindo Kou. Prediction of cracking susceptibility of commercial aluminum alloys during solidification. Metals, 11:1479, Sep 2021. URL: https://doi.org/10.3390/met11091479, doi:10.3390/met11091479. This article has 23 citations.

20. (zhang2021predictionofcracking pages 7-9): Fan Zhang, Songmao Liang, Chuan Zhang, Shuanglin Chen, Duchao Lv, Weisheng Cao, and Sindo Kou. Prediction of cracking susceptibility of commercial aluminum alloys during solidification. Metals, 11:1479, Sep 2021. URL: https://doi.org/10.3390/met11091479, doi:10.3390/met11091479. This article has 23 citations.

21. (zhang2021predictionofcracking pages 12-14): Fan Zhang, Songmao Liang, Chuan Zhang, Shuanglin Chen, Duchao Lv, Weisheng Cao, and Sindo Kou. Prediction of cracking susceptibility of commercial aluminum alloys during solidification. Metals, 11:1479, Sep 2021. URL: https://doi.org/10.3390/met11091479, doi:10.3390/met11091479. This article has 23 citations.

22. (hesselmann2022effectofprecipitationforming pages 1-3): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 23 citations and is from a highest quality peer-reviewed journal.

23. (hesselmann2022effectofprecipitationforming pages 3-5): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 23 citations and is from a highest quality peer-reviewed journal.

24. (hesselmann2022effectofprecipitationforming pages 11-14): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 23 citations and is from a highest quality peer-reviewed journal.

25. (hyer2021compositiondependentsolidificationcracking media f8afade2): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.

26. (hyer2021compositiondependentsolidificationcracking media d0ab0ffa): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.

27. (hyer2021compositiondependentsolidificationcracking media a6538230): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 225 citations and is from a highest quality peer-reviewed journal.


---

## Query 8

**Question:** What post-build heat treatment optimization studies exist for LPBF aluminum alloys? Compare T5, T6, HIP, and novel heat treatments. Which treatments achieve the best property combinations for each alloy system?

**Task ID:** `8af7c1ee-55fa-437d-b806-6fddc770581f`

**Status:** complete

Post-build heat-treatment optimization for LPBF aluminum alloys is highly alloy-dependent because the as-built state contains a process-created supersaturated solid solution, high dislocation density, and (in Al–Si) a fine eutectic-Si network; heat treatments trade off (i) precipitation strengthening, (ii) preservation vs collapse/spheroidization of fine-scale features, and (iii) defect closure (HIP) versus microstructural coarsening. The key comparative studies and the best property combinations per alloy family are summarized below.

| Alloy system | T5 / direct aging (optimized examples) | Conventional T6 / solution + aging | Rapid / novel variants | HIP / HIP+T6 | Best property combination(s) / performance focus | Key citations |
|---|---|---|---|---|---|---|
| AlSi10Mg | **T5:** 160 °C × 4 h. Preserves cellular Si network; high strength but limited ductility. Reported fatigue strength: **92 MPa RT**, **78 MPa at 200 °C**. Hardness after exposure: ~122 HB10 initially, dropping after thermal exposure. Other DA studies show UTS can remain ~**487–515 MPa** when the fine network is preserved. (egidio2023roomandhightemperature pages 1-2, egidio2023roomandhightemperature pages 7-9, zhu2023microstructuralanalysisof pages 12-14) | **T6B:** 540 °C × 1 h + 160 °C × 4 h. Breaks up Si network and increases ductility but usually lowers UTS versus AB/T5; in related AlSi10Mg/AlSi7Mg literature T6 commonly gives lower strength and moderate ductility. (egidio2023influenceofmicrostructure pages 1-2, egidio2022anovelt6 pages 22-24, wang2024areviewon pages 9-11) | **T6R:** 510 °C × 10 min + 160 °C × 6 h. Versus conventional T6, reported **+14% YS, +4% UTS, +7% elongation**; versus T5, similar YS, lower UTS, much higher ductility (~**210%** elongation increase). Fatigue strength: **108 MPa RT**, **92 MPa at 200 °C**. Microstructure: finer, more homogeneous globular Si than T6B. (egidio2022anovelt6 pages 1-4, egidio2023roomandhightemperature pages 1-2, egidio2022anovelt6 pages 22-24, egidio2022anovelt6 pages 18-22) | **HIP:** classic ~500–530 °C / 100 MPa / 1–2 h reduces porosity but strongly softens; examples **YS ~80–97 MPa, UTS ~127–146 MPa, elongation ~30–36%**. **HIP+T6:** can partially restore strength; example **YS 240 ± 8 MPa, UTS 305 ± 8 MPa, e 16.2 ± 1.4%**, but long aging can re-soften to **YS ~94 MPa, UTS ~144 MPa, e ~29%**. Lower-T/high-P HIP (350 °C, 300 MPa, 2 h) improved fatigue metric more than classic HIP in one study. (merino2021multiplecomparativeheat pages 8-10, merino2021multiplecomparativeheat pages 14-14, macias2022hotisostaticpressing pages 1-3) | **Best for strength retention:** T5/direct aging. **Best balanced strength-ductility-fatigue:** **rapid T6R**. **Best ductility / defect closure:** HIP, but strength penalty is large. **Best for fatigue-critical AlSi10Mg among compared post-build routes:** T6R > T5 in rotating-bending fatigue. (egidio2023roomandhightemperature pages 1-2, egidio2023roomandhightemperature pages 7-9, zhu2023microstructuralanalysisof pages 12-14) | (egidio2022anovelt6 pages 1-4, merino2021multiplecomparativeheat pages 8-10, egidio2023roomandhightemperature pages 1-2, merino2021multiplecomparativeheat pages 14-14, macias2022hotisostaticpressing pages 1-3, egidio2023roomandhightemperature pages 7-9, egidio2023influenceofmicrostructure pages 1-2, zhu2023microstructuralanalysisof pages 12-14, egidio2022anovelt6 pages 22-24, egidio2022anovelt6 pages 18-22) |
| AlSi7Mg / A357 / F357 | **T5 / DA:** For LPBF AlSi7Mg, solution-free aging gives the strongest state in cited study: **UTS 411 MPa, YS 309 MPa, e 4.8%, HV 137**. Tonelli et al. report optimized DA can match redesigned T6 in hardness, but not in residual-stress relief. (casati2021insightintothe pages 1-2, tonelli2021roleofdirect pages 1-2) | **Conventional T6:** example route **540 °C × 1 h + WQ + 160 °C × 4 h** (AlSi7Mg) gave **UTS 306 MPa, YS 256 MPa, e 4.7%, HV 113**; F357 ASTM-type T6 route **530 °C × 360 min + 160 °C × 360 min** used broadly. T6 gives full residual-stress relief but lower strength than T5 in AlSi7Mg. (casati2021insightintothe pages 1-2, diaz2022comparisonofmultiple pages 1-4, tonelli2021roleofdirect pages 1-2) | **Redesigned / rapid T6:** shortened solution for LPBF A357/F357, e.g. **~10–15 min at 540 °C** plus aging; reported to reduce anisotropy, fully relieve residual stress, and improve strength–ductility balance versus cast-style T6. In F357 aging matrices, **T6 + 100 h at 140 °C** gave highest YS ~**291–295 MPa** across machines/orientations. (yadegari2025aluminumlaseradditive pages 29-30, lorenzetti2022a357aluminiumalloy pages 1-2, caballero2023acomparisonof pages 22-24) | **HIP:** F357/AlSi7Mg HIP at **515 °C, 100 MPa, 180 min** gives homogenized microstructure and high ductility but low strength; YS about **85–87 MPa**, elongation **25–31%**. **HIP+T6:** used industrially; aging can push elongation as high as **42%** after HIP + 1000 h at 177 °C, while sacrificing strength. Sequence matters in AlF357: **SR+HIP+T6** gave ~**45% higher YS** and **32% higher UTS** than **SR+T6+HIP**, with slightly lower ductility and better fatigue resistance. (caballero2023acomparisonof pages 22-24, caballero2023acomparisonof pages 3-6, khan2024effectofheat pages 1-3, diaz2022comparisonofmultiple pages 1-4) | **Best for peak strength/hardness:** **T5/direct aging** in AlSi7Mg. **Best for residual-stress relief + balanced properties:** redesigned/rapid T6 for LPBF A357/F357. **Best for ductility / defect healing:** HIP or HIP+aging. **Best processing sequence when HIP is needed in AlF357:** HIP before T6. (casati2021insightintothe pages 1-2, tonelli2021roleofdirect pages 1-2, lorenzetti2022a357aluminiumalloy pages 1-2, khan2024effectofheat pages 1-3) | (caballero2023acomparisonof pages 22-24, lorenzetti2022a357aluminiumalloy pages 1-2, caballero2023acomparisonof pages 3-6, khan2024effectofheat pages 1-3, diaz2022comparisonofmultiple pages 1-4, casati2021insightintothe pages 1-2, tonelli2021roleofdirect pages 1-2) |
| Scalmalloy (Al-Mg-Sc-Zr) | **Direct aging / T5:** strongest mainstream route. **325 °C × 4 h** gives about **YS 456–469 MPa, UTS 512–521 MPa, e 12–13%**; Mehta et al. report **YS 468 MPa, UTS 517 MPa, e 8.5%, 172 HV** from **598 K × 4 h**. Lower-T long aging (**150 °C × 168–504 h**) gives **UTS ~527–528 MPa, YS ~459–468 MPa, e ~12%, HV ~162–166**. (mehta2021laserpowderbed pages 10-11, cerri2024mainheattreatments pages 14-16, cerri2024mainheattreatments pages 1-2, mehta2021laserpowderbed pages 1-2) | **T6 / homogenize + age:** higher-T solution/homogenization erases bimodal LPBF microstructure and reduces supersaturation; subsequent aging is needed to recover strength. Generally less attractive than direct aging for standard Scalmalloy because it sacrifices the as-built strengthening architecture. (cerri2024mainheattreatments pages 1-2, cerri2024mainheattreatments pages 2-5) | **Novel variants:** homogenization at **~505 °C** followed by higher-temperature aging can produce peak-aging in minutes; 350 °C can peak in ~0.5 h in some reports, whereas 300 °C may need much longer. These are process-time optimization routes rather than property leaders in the review. (cerri2024mainheattreatments pages 14-16, cerri2024mainheattreatments pages 2-5) | **HIP at aging temperature:** e.g. **325 °C / 1000 bar / 2–4 h** lowers porosity (~0.22→0.04%) and gives about **YS 475–493 MPa, UTS 510–547 MPa, e ~13%**, hardness ~**157–158 HV**. HIP therefore improves density and often slightly improves both strength and ductility versus direct aging alone. (cerri2024mainheattreatments pages 14-16, cerri2024mainheattreatments pages 1-2) | **Best overall property combination in LPBF Scalmalloy:** **low-temperature HIP / HIP+aging-temperature treatment**; it gives the highest or near-highest YS/UTS while retaining ~13% ductility and lowering porosity. **Best simple post-build route:** direct aging at ~325 °C × 4 h. (cerri2024mainheattreatments pages 14-16, cerri2024mainheattreatments pages 1-2, cerri2024mainheattreatments media c3043fdf) | (mehta2021laserpowderbed pages 10-11, cerri2024mainheattreatments pages 14-16, cerri2024mainheattreatments pages 1-2, mehta2021laserpowderbed pages 1-2, cerri2024mainheattreatments pages 2-5, cerri2024mainheattreatments media c3043fdf) |
| Al-Mn-Mg-Sc-Zr | **T5:** **300 °C × 5 h** gave the best reported state: **YS 484 ± 1 MPa, UTS 507 ± 3 MPa, e 15 ± 1%, HV 166 ± 2**. Preserves bimodal LPBF microstructure and precipitates fine secondary Al3Sc. (cao2025effectofheat pages 1-2, cao2025effectofheat pages 7-9, cao2025effectofheat pages 4-7) | **T6:** solution + aging caused recrystallization and precipitate coarsening; reported **YS 371 ± 10 MPa, UTS 442 ± 8 MPa, e 9 ± 1%, HV 142 ± 2**. Clearly inferior to T5 for both strength and ductility in cited work. (cao2025effectofheat pages 7-9, cao2025effectofheat pages 4-7) | No separate rapid T6R reported in the retrieved evidence. (cao2025effectofheat pages 1-2) | No HIP/HIP+T6 data found in the retrieved evidence. (cao2025effectofheat pages 1-2) | **Best property combination:** **T5 at 300 °C × 5 h**; it outperforms T6 in strength and ductility and is the recommended route for this alloy family. (cao2025effectofheat pages 1-2, cao2025effectofheat pages 7-9) | (cao2025effectofheat pages 1-2, cao2025effectofheat pages 7-9, cao2025effectofheat pages 4-7) |
| Al-Cu-Mg (2024-type and related) | No clear T5/direct-aging optimization for standard LPBF 2024-type alloy found in retrieved texts. (qi2020mechanicalbehaviorand pages 7-10, qi2020mechanicalbehaviorand pages 1-2) | **Optimized solution + aging:** in LPBF Al-Cu-Mg, **540 °C × 1 h + WQ + 190 °C × 6 h** gave the highest reported **YS 400.0 ± 3.0 MPa**. Aging increased YS through fine acicular Al2CuMg precipitates but reduced UTS/ductility because coarse phases promoted cracking. A 2024-type composition with grain refiner + T6 is tabulated at **UTS 432 MPa, YS 286 MPa, e ~10%**. (qi2020mechanicalbehaviorand pages 7-10, kotadiaUnknownyearkotadiahrgibbons pages 8-10) | Conventional T6 often needs redesign because LPBF supersaturation and defect structure change kinetics; no robust T6R-style route for standard 2024 was extracted here. (qi2020mechanicalbehaviorand pages 1-2) | No HIP/HIP+T6 data located for standard LPBF 2024-type alloy in the retrieved evidence. (qi2020mechanicalbehaviorand pages 7-10, qi2020mechanicalbehaviorand pages 1-2) | **Best demonstrated route in retrieved evidence:** **solution + controlled artificial aging** (around **540 °C × 1 h + 190 °C × 6 h**) for high YS. **Trade-off:** strength rises, but ductility degrades after aging. This family still lacks the same mature LPBF heat-treatment consensus seen in AlSi10Mg or Scalmalloy. (qi2020mechanicalbehaviorand pages 7-10, qi2020mechanicalbehaviorand pages 1-2, kotadiaUnknownyearkotadiahrgibbons pages 8-10) | (qi2020mechanicalbehaviorand pages 7-10, qi2020mechanicalbehaviorand pages 1-2, kotadiaUnknownyearkotadiahrgibbons pages 8-10) |
| A20X (Al-Cu-Mg-Ag-TiB2) | No explicit T5 optimization extracted in retrieved evidence. (shakil2024theeffectof pages 1-2) | **Tailored solution + aging / T7-like routes:** one cited short route **530 °C × 1 h + 190 °C aging** gave **UTS 435 ± 13 MPa, e 7.3 ± 0.3%**. Other cited studies report **T7 ~483 MPa UTS, e ~9.5%**; as-built values vary widely (~**350 MPa UTS, 12.5% e** to **401 ± 2 MPa UTS, 17.7% e**). (shakil2024theeffectof pages 1-2) | Review table also lists strong age-hardening behavior in related PBF-specific Al-Cu-Mg family members; however, specific rapid T6 nomenclature is not established in the extracted A20X evidence. (shakil2024theeffectof pages 1-2, kotadiaUnknownyearkotadiahrgibbons pages 8-10) | **HIP:** cited study used **510 °C, 103 MPa, 2 h** before tailored heat treatment to remove LPBF defects; HIP alone is not sufficient because precipitation state is not optimized. Retrieved excerpt emphasizes **HIP + tailored aging/solution treatment** rather than HIP-only properties. (shakil2024theeffectof pages 1-2) | **Best available combination from retrieved evidence:** **HIP followed by tailored solution/aging (T6/T7-type)** for dense microstructure plus precipitation strengthening. Among reported absolute values, **T7-like aging (~483 MPa UTS, 9.5% e)** appears the strongest cited route, while as-built can retain more ductility. (shakil2024theeffectof pages 1-2) | (shakil2024theeffectof pages 1-2, kotadiaUnknownyearkotadiahrgibbons pages 8-10) |


*Table: This table compares optimized post-build heat treatments across major LPBF aluminum alloy systems, including T5, T6, HIP, and novel routes, with reported property outcomes. It highlights which treatments deliver the best strength, ductility, or fatigue balance for each alloy family.*

### 1) Al–Si–Mg family: AlSi10Mg (and near-eutectic Al–Si) 
**T5 / direct aging (DA) optimization (strength retention).** Direct aging retains much of the as-built cellular/eutectic-Si network and therefore tends to preserve high tensile strength; Zhu et al. reported DA giving only modest changes but maintaining high UTS, with UTS increasing from an as-built value of ~486 MPa to ~487–502 MPa (horizontal) and ~515 MPa (vertical), consistent with the idea that preserving the fine Si network and high dislocation density maintains strength (and typically limits ductility gains). (zhu2023microstructuralanalysisof pages 12-14)

**Conventional T6 (ductility and homogenization, but often softening).** In many AlSi10Mg reports, full solutionizing collapses the Si network and coarsens Si particles; strength decreases substantially and is only partly recovered by aging (e.g., transverse UTS ~256 MPa after solution treatment, recovering to ~281 MPa after subsequent aging in Zhu et al.). (zhu2023microstructuralanalysisof pages 12-14)

**Novel/rapid T6 (T6R) optimization (best combined properties for AlSi10Mg).** Di Egidio et al. introduced a rapid T6R consisting of 510 °C × 10 min solution + 160 °C × 6 h aging; relative to a conventional T6B (540 °C × 1 h + 160 °C × 4 h), T6R improved YS/UTS/elongation by ~14%/4%/7% and was designed to limit pore growth and microstructural coarsening while still spheroidizing Si. (egidio2022anovelt6 pages 22-24)

**Fatigue comparison (T5 vs T6R).** In rotating-bending fatigue, T6R outperformed T5 for LPBF AlSi10Mg: fatigue strength at room temperature was **108 MPa (T6R) vs 92 MPa (T5)** and at 200 °C was **92 MPa (T6R) vs 78 MPa (T5)**, with T5 defined as 160 °C × 4 h and T6R as 510 °C × 10 min + 160 °C × 6 h. (egidio2023roomandhightemperature pages 1-2)

**HIP and HIP+T6 (defect closure vs strength).** Merino et al. show the classic trade-off: HIP strongly increases ductility but causes major strength loss (e.g., HIP: YS ~80–97 MPa, UTS ~127–146 MPa, e ~30–36%). HIP+T6 can partially restore strength (e.g., YS 240 ± 8 MPa, UTS 305 ± 8 MPa, e 16.2 ± 1.4%), but extended aging can re-soften substantially (e.g., YS ~94 MPa, e ~29% after long aging in one variant), showing sensitivity to the full thermal history. (merino2021multiplecomparativeheat pages 8-10, merino2021multiplecomparativeheat pages 14-14)

**Best combination for AlSi10Mg.**
- **Best strength retention (static tensile):** T5/direct aging (preserves as-built strengthening features). (zhu2023microstructuralanalysisof pages 12-14)
- **Best overall strength–ductility–fatigue balance among compared treatments:** rapid T6R. (egidio2023roomandhightemperature pages 1-2, egidio2022anovelt6 pages 22-24)
- **Best ductility/defect healing (at significant strength cost):** HIP (often followed by tailored re-aging if strength must be recovered). (merino2021multiplecomparativeheat pages 8-10, merino2021multiplecomparativeheat pages 14-14)

### 2) Hypoeutectic Al–Si–Mg family: AlSi7Mg / A357 / F357 
**T5 vs T6: direct aging can outperform T6 in strength/hardness in LPBF AlSi7Mg.** Casati et al. (citing [5]) report: 
- As-built: UTS 398 MPa, YS 257 MPa, e 7.6%, HV 102
- **T5:** UTS **411 MPa**, YS **309 MPa**, e 4.8%, HV 137
- **T6:** UTS **306 MPa**, YS 256 MPa, e 4.7%, HV 113
This indicates that, for AlSi7Mg in that dataset, T5 gave the highest strength/hardness but at reduced ductility, while conventional T6 did not improve strength and reduced UTS markedly. (casati2021insightintothe pages 1-2)

**Residual-stress relief and “redesigned/shortened” T6.** Tonelli et al. report that optimized direct aging and a redesigned T6 can reach comparable hardness, but complete residual stress relief was obtained only with T6, motivating shortened-solution T6 routes for LPBF A357-type alloys. (tonelli2021roleofdirect pages 1-2)

**HIP and HIP+T6 for F357 (ductility focus).** Caballero et al. report HIP (515 °C, 100 MPa, 180 min) yields very low YS (~85–87 MPa for Z builds) but high elongation (25–31%), and the maximum elongation (42%) occurred after HIP plus long aging (1000 h at 177 °C), illustrating how HIP+aging can maximize ductility at the expense of strength. (caballero2023acomparisonof pages 22-24, caballero2023acomparisonof pages 3-6)

**Sequence optimization for combined HIP and T6 in AlF357.** Khan et al. compared SR+HIP+T6 vs SR+T6+HIP and found HIP-before-T6 gave ~45% higher YS and ~32% higher UTS, with slightly lower ductility but better fatigue resistance—i.e., if both HIP and T6 are needed, sequence matters. (khan2024effectofheat pages 1-3)

**Best combination for AlSi7Mg/A357/F357.**
- **Best peak strength/hardness:** T5/direct aging (in available tensile dataset). (casati2021insightintothe pages 1-2)
- **Best residual-stress relief with competitive hardness:** redesigned/shortened T6 concepts (often chosen for dimensional stability and isotropy). (tonelli2021roleofdirect pages 1-2)
- **Best ductility and defect tolerance:** HIP (optionally HIP+aging). (caballero2023acomparisonof pages 22-24, caballero2023acomparisonof pages 3-6)
- **When using HIP+T6:** HIP before T6 appears superior for strength and fatigue in AlF357. (khan2024effectofheat pages 1-3)

### 3) Al–Mg–Sc–Zr family: Scalmalloy® and related Al–(Mn)–Mg–Sc–Zr alloys
**Direct aging (T5) is the dominant “best practice” for Scalmalloy strength–ductility.** Scalmalloy as-built is typically ~YS 256–278 MPa, UTS 349–353 MPa, e 19–21%. Direct aging at **325 °C × 4 h** increases strength to ~YS 456–469 MPa and UTS 512–521 MPa with e ~12–13%. (cerri2024mainheattreatments pages 1-2)

**HIP at aging temperature can further improve properties while reducing porosity.** The Scalmalloy review summarizes HIP at **325 °C × 4 h, 1000 bar** as reducing porosity and raising strength further (YS ~482–493 MPa, UTS ~523–547 MPa). These comparisons are summarized visually in the extracted tables/figure. (cerri2024mainheattreatments pages 1-2, cerri2024mainheattreatments media c3043fdf)

**Heat-treatment optimization data in primary study.** Mehta et al. identified a peak-hardness condition of **598 K (325 °C) for 4 h** giving peak hardness 172 HV and tensile properties changing from as-printed 287/364 MPa (YS/UTS) to 468/517 MPa after peak aging, demonstrating rapid qualification of aging schedules. (mehta2021laserpowderbed pages 1-2)

**Related Al–Mn–Mg–Sc–Zr alloys: T5 can outperform T6.** For LPBF Al–Mn–Mg–Sc–Zr, Cao et al. report:
- AB: YS 294 ± 11 MPa, UTS 337 ± 1 MPa, e 24 ± 2%, HV 99 ± 5
- **T5:** YS **484 ± 1 MPa**, UTS **507 ± 3 MPa**, e **15 ± 1%**, HV 166 ± 2
- **T6:** YS 371 ± 10 MPa, UTS 442 ± 8 MPa, e 9 ± 1%, HV 142 ± 2
indicating direct aging gives the best overall combination in that system, while T6 triggers recrystallization/coarsening and worsens both strength and ductility. (cao2025effectofheat pages 7-9)

**Best combination for Scalmalloy / Al–Mg–Sc–Zr systems.**
- **Best overall combination (strength + ductility + density):** low-temperature HIP at aging temperature (HIP+aging-temperature schedule), when available. (cerri2024mainheattreatments pages 1-2, cerri2024mainheattreatments media c3043fdf)
- **Best simple route:** direct aging around 325 °C × 4 h. (cerri2024mainheattreatments pages 1-2, mehta2021laserpowderbed pages 1-2)
- **For Al–Mn–Mg–Sc–Zr:** T5 at ~300 °C × 5 h is clearly superior to T6. (cao2025effectofheat pages 7-9)

### 4) Al–Cu–Mg family: 2xxx-type (2024-like) and A20X (Al–Cu–Mg–Ag–TiB2)
**Solution + aging optimization (T6-like) for LPBF Al–Cu–Mg.** Qi et al. show that a solution treatment at **540 °C × 1 h** + water quench followed by artificial aging can be tuned for strength; aging at **190 °C for 6 h** produced the highest reported YS (**400.0 ± 3.0 MPa**) driven by dense acicular ultrafine Al2CuMg precipitates. They also report the typical trade-off: artificial aging increased YS but reduced UTS and ductility due to coarser phases and cracking tendency. (qi2020mechanicalbehaviorand pages 7-10)

**2024-type property benchmark (grain refiner + T6).** A tabulated LPBF 2024-type with grain refiner + T6 shows UTS 432 MPa, YS 286 MPa, e ~10%, illustrating feasible strength/ductility but also indicating that printability and microstructural control (grain refinement) can be as critical as heat treatment in this family. (kotadiaUnknownyearkotadiahrgibbons pages 8-10)

**A20X: HIP plus tailored precipitation heat treatment.** Shakil et al. report HIP at **510 °C, 103 MPa, 2 h** as a defect-reduction step, but emphasize that HIP alone is not sufficient because precipitation state must be optimized with subsequent heat treatment. Cited optimized short route: **530 °C × 1 h** solution + **190 °C aging** gave **UTS 435 ± 13 MPa** and **e 7.3 ± 0.3%**; other cited work reports **T7 ~483 MPa UTS** with **~9.5% elongation**, showing that overaging-type schedules may provide strong, relatively ductile states for this PBF-tailored alloy. (shakil2024theeffectof pages 1-2)

**Best combination for Al–Cu–Mg / A20X (based on retrieved evidence).**
- **Al–Cu–Mg (non-A20X):** best-demonstrated route is optimized solution + artificial aging (high YS, but ductility penalty). (qi2020mechanicalbehaviorand pages 7-10)
- **A20X:** best approach is **HIP + tailored solution/aging (T6/T7-type)** to combine defect closure with precipitation strengthening; T7-like outcomes appear to give the strongest cited UTS while retaining moderate ductility. (shakil2024theeffectof pages 1-2)

### Cross-cutting conclusions: how T5, T6, HIP, and “novel” routes compare
- **T5/direct aging** is most advantageous when the as-built microstructure is already highly strengthening (supersaturation + very fine cellular/eutectic networks) and when solutionizing would erase those advantages; this is strongly supported in AlSi7Mg and Scalmalloy/Sc-bearing alloys, and often in AlSi10Mg strength retention. (casati2021insightintothe pages 1-2, cerri2024mainheattreatments pages 1-2, zhu2023microstructuralanalysisof pages 12-14)
- **Conventional T6** is often selected for **residual-stress relief and microstructural homogenization**, but it can **soften** LPBF Al–Si alloys unless redesigned (shortened solution time/temperature). (tonelli2021roleofdirect pages 1-2, zhu2023microstructuralanalysisof pages 12-14)
- **Novel/rapid T6 variants (e.g., T6R)** are the clearest example of post-build heat-treatment optimization tailored to LPBF microstructures, improving the strength–ductility balance and fatigue versus simpler aging in AlSi10Mg. (egidio2023roomandhightemperature pages 1-2, egidio2022anovelt6 pages 22-24)
- **HIP** is the most effective defect-closure method and can dramatically increase ductility, but it frequently incurs a strength penalty due to coarsening; combining HIP with tailored aging/solution-aging (and optimizing sequence) is therefore the active optimization direction. (merino2021multiplecomparativeheat pages 8-10, merino2021multiplecomparativeheat pages 14-14, khan2024effectofheat pages 1-3, shakil2024theeffectof pages 1-2)

### Evidence gaps (in the retrieved corpus)
Quantitative, like-for-like comparisons of T5 vs T6 vs HIP vs HIP+T6 vs novel multistage treatments remain much more complete for **AlSi10Mg** and **Scalmalloy** than for **standard 2024-type** or **7xxx** LPBF alloys; for the latter, optimization is often tightly coupled to alloy redesign and crack-mitigation strategies, and fewer directly comparable post-build heat-treatment datasets were accessible here. (yadegari2025aluminumlaseradditive pages 29-30, qi2020mechanicalbehaviorand pages 7-10, kotadiaUnknownyearkotadiahrgibbons pages 8-10)

References

1. (egidio2023roomandhightemperature pages 1-2): Gianluca Di Egidio, Lorella Ceschini, Alessandro Morri, and Mattia Zanni. Room- and high-temperature fatigue strength of the t5 and rapid t6 heat-treated alsi10mg alloy produced by laser-based powder bed fusion. Metals, 13:263, Jan 2023. URL: https://doi.org/10.3390/met13020263, doi:10.3390/met13020263. This article has 15 citations.

2. (egidio2023roomandhightemperature pages 7-9): Gianluca Di Egidio, Lorella Ceschini, Alessandro Morri, and Mattia Zanni. Room- and high-temperature fatigue strength of the t5 and rapid t6 heat-treated alsi10mg alloy produced by laser-based powder bed fusion. Metals, 13:263, Jan 2023. URL: https://doi.org/10.3390/met13020263, doi:10.3390/met13020263. This article has 15 citations.

3. (zhu2023microstructuralanalysisof pages 12-14): Suming Zhu, Indrajeet Katti, Dong Qiu, Joy H. Forsmark, and Mark A. Easton. Microstructural analysis of the influences of platform preheating and post-build heat treatment on mechanical properties of laser powder bed fusion manufactured alsi10mg alloy. Materials Science and Engineering: A, 882:145486, Aug 2023. URL: https://doi.org/10.1016/j.msea.2023.145486, doi:10.1016/j.msea.2023.145486. This article has 31 citations.

4. (egidio2023influenceofmicrostructure pages 1-2): Gianluca Di Egidio, Carla Martini, Johan Börjesson, Ehsan Ghassemali, Lorella Ceschini, and Alessandro Morri. Influence of microstructure on fracture mechanisms of the heat-treated alsi10mg alloy produced by laser-based powder bed fusion. Materials, 16:2006, Feb 2023. URL: https://doi.org/10.3390/ma16052006, doi:10.3390/ma16052006. This article has 37 citations.

5. (egidio2022anovelt6 pages 22-24): Gianluca Di Egidio, Lorella Ceschini, Alessandro Morri, Carla Martini, and Mattia Merlin. A novel t6 rapid heat treatment for alsi10mg alloy produced by laser-based powder bed fusion: comparison with t5 and conventional t6 heat treatments. Metallurgical and Materials Transactions B, 53:284-303, Jan 2022. URL: https://doi.org/10.1007/s11663-021-02365-6, doi:10.1007/s11663-021-02365-6. This article has 59 citations.

6. (wang2024areviewon pages 9-11): Xin Wang, Dongyun Zhang, Ang Li, Denghao Yi, and Tianci Li. A review on traditional processes and laser powder bed fusion of aluminum alloy microstructures, mechanical properties, costs, and applications. Materials, 17:2553, May 2024. URL: https://doi.org/10.3390/ma17112553, doi:10.3390/ma17112553. This article has 39 citations.

7. (egidio2022anovelt6 pages 1-4): Gianluca Di Egidio, Lorella Ceschini, Alessandro Morri, Carla Martini, and Mattia Merlin. A novel t6 rapid heat treatment for alsi10mg alloy produced by laser-based powder bed fusion: comparison with t5 and conventional t6 heat treatments. Metallurgical and Materials Transactions B, 53:284-303, Jan 2022. URL: https://doi.org/10.1007/s11663-021-02365-6, doi:10.1007/s11663-021-02365-6. This article has 59 citations.

8. (egidio2022anovelt6 pages 18-22): Gianluca Di Egidio, Lorella Ceschini, Alessandro Morri, Carla Martini, and Mattia Merlin. A novel t6 rapid heat treatment for alsi10mg alloy produced by laser-based powder bed fusion: comparison with t5 and conventional t6 heat treatments. Metallurgical and Materials Transactions B, 53:284-303, Jan 2022. URL: https://doi.org/10.1007/s11663-021-02365-6, doi:10.1007/s11663-021-02365-6. This article has 59 citations.

9. (merino2021multiplecomparativeheat pages 8-10): Jorge Merino, Bryan Ruvalcaba, Jaime Varela, Edel Arrieta, Lawrence E. Murr, Ryan B. Wicker, Mark Benedict, and Francisco Medina. Multiple, comparative heat treatment and aging schedules for controlling the microstructures and mechanical properties of laser powder bed fusion fabricated alsi10mg alloy. Journal of Materials Research and Technology, 13:669-685, Jul 2021. URL: https://doi.org/10.1016/j.jmrt.2021.04.062, doi:10.1016/j.jmrt.2021.04.062. This article has 53 citations and is from a peer-reviewed journal.

10. (merino2021multiplecomparativeheat pages 14-14): Jorge Merino, Bryan Ruvalcaba, Jaime Varela, Edel Arrieta, Lawrence E. Murr, Ryan B. Wicker, Mark Benedict, and Francisco Medina. Multiple, comparative heat treatment and aging schedules for controlling the microstructures and mechanical properties of laser powder bed fusion fabricated alsi10mg alloy. Journal of Materials Research and Technology, 13:669-685, Jul 2021. URL: https://doi.org/10.1016/j.jmrt.2021.04.062, doi:10.1016/j.jmrt.2021.04.062. This article has 53 citations and is from a peer-reviewed journal.

11. (macias2022hotisostaticpressing pages 1-3): Juan Guillermo Santos Macías, Lv Zhao, David Tingaud, Brigitte Bacroix, Grzegorz Pyka, Camille van der Rest, Laurence Ryelandt, and Aude Simar. Hot isostatic pressing of laser powder bed fusion alsi10mg: parameter identification and mechanical properties. Journal of Materials Science, 57:9726-9740, Feb 2022. URL: https://doi.org/10.1007/s10853-022-07027-9, doi:10.1007/s10853-022-07027-9. This article has 39 citations and is from a peer-reviewed journal.

12. (casati2021insightintothe pages 1-2): R. Casati, M. Coduri, S. Checchia, and M. Vedani. Insight into the effect of different thermal treatment routes on the microstructure of alsi7mg produced by laser powder bed fusion. Materials Characterization, 172:110881, Feb 2021. URL: https://doi.org/10.1016/j.matchar.2021.110881, doi:10.1016/j.matchar.2021.110881. This article has 34 citations and is from a peer-reviewed journal.

13. (tonelli2021roleofdirect pages 1-2): Lavinia Tonelli, Erica Liverani, Alessandro Morri, and Lorella Ceschini. Role of direct aging and solution treatment on hardness, microstructure and residual stress of the a357 (alsi7mg0.6) alloy produced by powder bed fusion. Metallurgical and Materials Transactions B, 52:2484-2496, May 2021. URL: https://doi.org/10.1007/s11663-021-02179-6, doi:10.1007/s11663-021-02179-6. This article has 55 citations.

14. (diaz2022comparisonofmultiple pages 1-4): J. Diaz, K. Caballero, V.A. Medrano, E. Arrieta, M. Benedict, D. Godfrey, R. B. Wicker, and F. Medina. Comparison of multiple heat treatments by observing mechanical properties and microstructure of lpbf fabricated aluminum f357. Unknown, Jan 2022. URL: https://doi.org/10.26153/tsw/44561, doi:10.26153/tsw/44561. This article has 0 citations.

15. (yadegari2025aluminumlaseradditive pages 29-30): Mohammad Javad Yadegari, Alessandra Martucci, Sara Biamino, Daniele Ugues, Laura Montanaro, Paolo Fino, and Mariangela Lombardi. Aluminum laser additive manufacturing: a review on challenges and opportunities through the lens of sustainability. Applied Sciences, 15:2221, Feb 2025. URL: https://doi.org/10.3390/app15042221, doi:10.3390/app15042221. This article has 11 citations.

16. (lorenzetti2022a357aluminiumalloy pages 1-2): L. Lorenzetti, L. Tonelli, L. Ceschini, E. Liverani, and C. Martini. A357 aluminium alloy produced by lpbf: tribological behaviour in dry sliding conditions. Wear, 510-511:204488, Dec 2022. URL: https://doi.org/10.1016/j.wear.2022.204488, doi:10.1016/j.wear.2022.204488. This article has 18 citations and is from a highest quality peer-reviewed journal.

17. (caballero2023acomparisonof pages 22-24): K. Caballero, V.A. Medrano, E. Arrietam, J. Merino, B. Ruvalcaba, B. Ramirez, J. Diemann, L.E. Murr, R.B. Wicker, D. Godfrey, M. Benedict, and F. Medina. A comparison of the mechanical behavior of alsi7mg alloy produced through additive manufacturing and subjected to different heat treatment and aging conditions. ConferencePaper, Jan 2023. URL: https://doi.org/10.26153/tsw/50938, doi:10.26153/tsw/50938. This article has 0 citations.

18. (caballero2023acomparisonof pages 3-6): K. Caballero, V.A. Medrano, E. Arrietam, J. Merino, B. Ruvalcaba, B. Ramirez, J. Diemann, L.E. Murr, R.B. Wicker, D. Godfrey, M. Benedict, and F. Medina. A comparison of the mechanical behavior of alsi7mg alloy produced through additive manufacturing and subjected to different heat treatment and aging conditions. ConferencePaper, Jan 2023. URL: https://doi.org/10.26153/tsw/50938, doi:10.26153/tsw/50938. This article has 0 citations.

19. (khan2024effectofheat pages 1-3): MF Khan, PR Gradl, D Godfrey, J Diemann, and S Shao. Effect of heat treatment on the micro-/defect-structure and mechanical behavior of additively manufactured alf357 aluminum alloy. Unknown journal, 2024.

20. (mehta2021laserpowderbed pages 10-11): Bharat Mehta, Arvid Svanberg, and Lars Nyborg. Laser powder bed fusion of an al-mg-sc-zr alloy: manufacturing, peak hardening response and thermal stability at peak hardness. Metals, 12:57, Dec 2021. URL: https://doi.org/10.3390/met12010057, doi:10.3390/met12010057. This article has 18 citations.

21. (cerri2024mainheattreatments pages 14-16): Emanuela Cerri, Lorenzo Curti, and Emanuele Ghio. Main heat treatments currently applied on laser powder bed-fused scalmalloy®: a review. Crystals, 15:25, Dec 2024. URL: https://doi.org/10.3390/cryst15010025, doi:10.3390/cryst15010025. This article has 8 citations.

22. (cerri2024mainheattreatments pages 1-2): Emanuela Cerri, Lorenzo Curti, and Emanuele Ghio. Main heat treatments currently applied on laser powder bed-fused scalmalloy®: a review. Crystals, 15:25, Dec 2024. URL: https://doi.org/10.3390/cryst15010025, doi:10.3390/cryst15010025. This article has 8 citations.

23. (mehta2021laserpowderbed pages 1-2): Bharat Mehta, Arvid Svanberg, and Lars Nyborg. Laser powder bed fusion of an al-mg-sc-zr alloy: manufacturing, peak hardening response and thermal stability at peak hardness. Metals, 12:57, Dec 2021. URL: https://doi.org/10.3390/met12010057, doi:10.3390/met12010057. This article has 18 citations.

24. (cerri2024mainheattreatments pages 2-5): Emanuela Cerri, Lorenzo Curti, and Emanuele Ghio. Main heat treatments currently applied on laser powder bed-fused scalmalloy®: a review. Crystals, 15:25, Dec 2024. URL: https://doi.org/10.3390/cryst15010025, doi:10.3390/cryst15010025. This article has 8 citations.

25. (cerri2024mainheattreatments media c3043fdf): Emanuela Cerri, Lorenzo Curti, and Emanuele Ghio. Main heat treatments currently applied on laser powder bed-fused scalmalloy®: a review. Crystals, 15:25, Dec 2024. URL: https://doi.org/10.3390/cryst15010025, doi:10.3390/cryst15010025. This article has 8 citations.

26. (cao2025effectofheat pages 1-2): Zhiqiang Cao, Hui Yin, Jin Jiang, Mingliang Cui, Hao Zhang, and Sheng Cao. Effect of heat treatment on microstructure and tensile property of laser-powder-bed-melted al–mn–mg–sc–zr alloy. Materials, 18:1638, Apr 2025. URL: https://doi.org/10.3390/ma18071638, doi:10.3390/ma18071638. This article has 1 citations.

27. (cao2025effectofheat pages 7-9): Zhiqiang Cao, Hui Yin, Jin Jiang, Mingliang Cui, Hao Zhang, and Sheng Cao. Effect of heat treatment on microstructure and tensile property of laser-powder-bed-melted al–mn–mg–sc–zr alloy. Materials, 18:1638, Apr 2025. URL: https://doi.org/10.3390/ma18071638, doi:10.3390/ma18071638. This article has 1 citations.

28. (cao2025effectofheat pages 4-7): Zhiqiang Cao, Hui Yin, Jin Jiang, Mingliang Cui, Hao Zhang, and Sheng Cao. Effect of heat treatment on microstructure and tensile property of laser-powder-bed-melted al–mn–mg–sc–zr alloy. Materials, 18:1638, Apr 2025. URL: https://doi.org/10.3390/ma18071638, doi:10.3390/ma18071638. This article has 1 citations.

29. (qi2020mechanicalbehaviorand pages 7-10): Yang Qi, Hu Zhang, Junjie Zhu, Xiaojia Nie, Zhiheng Hu, Haihong Zhu, and Xiaoyan Zeng. Mechanical behavior and microstructure evolution of al-cu-mg alloy produced by laser powder bed fusion: effect of heat treatment. Materials Characterization, 165:110364, Jul 2020. URL: https://doi.org/10.1016/j.matchar.2020.110364, doi:10.1016/j.matchar.2020.110364. This article has 45 citations and is from a peer-reviewed journal.

30. (qi2020mechanicalbehaviorand pages 1-2): Yang Qi, Hu Zhang, Junjie Zhu, Xiaojia Nie, Zhiheng Hu, Haihong Zhu, and Xiaoyan Zeng. Mechanical behavior and microstructure evolution of al-cu-mg alloy produced by laser powder bed fusion: effect of heat treatment. Materials Characterization, 165:110364, Jul 2020. URL: https://doi.org/10.1016/j.matchar.2020.110364, doi:10.1016/j.matchar.2020.110364. This article has 45 citations and is from a peer-reviewed journal.

31. (kotadiaUnknownyearkotadiahrgibbons pages 8-10): HR Kotadia. Kotadia, hr, gibbons, g, das, a and howes, pd a review of laser powder bed fusion additive manufacturing of aluminium alloys: microstructure and …. Unknown journal, Unknown year.

32. (shakil2024theeffectof pages 1-2): Shawkat I. Shakil, Chad Beamer, Moataz M. Attallah, and Meysam Haghshenas. The effect of heat treatment on local mechanical properties of laser powder bed fused and hot isostatically pressed al-cu-mg-ag-tib_2 (a20x) aluminum alloy. JOM, 76:31-41, Nov 2024. URL: https://doi.org/10.1007/s11837-023-06233-3, doi:10.1007/s11837-023-06233-3. This article has 7 citations and is from a peer-reviewed journal.


---

## Query 9

**Question:** What environmental and sustainability data exists for AM aluminum alloys? Compare energy consumption, material waste, and carbon footprint of LPBF vs conventional manufacturing for aluminum parts.

**Task ID:** `5c8dc779-70fb-42b6-901a-802dc0d97393`

**Status:** complete

## Scope and evidence base
Environmental and sustainability data for LPBF aluminum alloys exist primarily as (i) process- and factory-level energy inventories (kWh/kg or kWh/job), (ii) cradle-to-gate or cradle-to-grave LCAs reporting energy demand and global warming potential (GWP), and (iii) material-efficiency indicators such as buy-to-fly (B2F) ratio and powder-yield/reuse assumptions. For aluminum LPBF, the most directly comparable LPBF-vs-conventional dataset in the retrieved corpus is a cradle-to-gate comparison of an aerospace bracket made by CNC machining (Al 7175-T7351) vs LPBF (Scalmalloy®) with explicit energy, CO2e, and B2F values. (sargioti2026simulationdrivenbuildstrategies pages 12-15, sargioti2026simulationdrivenbuildstrategies pages 15-16, sargioti2026simulationdrivenbuildstrategies media b3ceac34)

| Study/case | Alloy & route | Functional unit | System boundary | Energy metric | Carbon metric | Material waste metric | Key assumptions/sensitivities |
|---|---|---|---|---|---|---|---|
| Sargioti et al. 2026 — CNC baseline | Al 7175-T7351, 3-axis CNC from billet | 1 aerospace bearing bracket | Cradle-to-gate | Total energy demand >100 kWh/part; ingot production alone >40 kWh/part | ~11,000 g CO2e/part | Buy-to-fly (B2F) 1:7; ~86% of raw material lost as waste | Results depend on bracket geometry, billet route, and electricity mix; study uses Norwegian grid assumptions and includes recycling credits (sargioti2026simulationdrivenbuildstrategies pages 12-15, sargioti2026simulationdrivenbuildstrategies pages 15-16, sargioti2026simulationdrivenbuildstrategies pages 5-7) |
| Sargioti et al. 2026 — LPBF strategy 1 | Scalmalloy®, LPBF single-part build | 1 aerospace bearing bracket | Cradle-to-gate | ~40 kWh/part | ~1,122 g CO2e/part | B2F ~1:1.2 | Single-part build; support/build strategy affects distortion, build time, and emissions (sargioti2026simulationdrivenbuildstrategies pages 12-15, sargioti2026simulationdrivenbuildstrategies pages 15-16) |
| Sargioti et al. 2026 — LPBF strategy 2 | Scalmalloy®, LPBF three-part nested build | 1 aerospace bearing bracket | Cradle-to-gate | ~37 kWh/part | ~820 g CO2e/part | B2F ~1:1.2 | Multi-part nesting improves per-part energy/CO2 vs strategy 1 while keeping similar material efficiency (sargioti2026simulationdrivenbuildstrategies pages 12-15, sargioti2026simulationdrivenbuildstrategies pages 15-16, sargioti2026simulationdrivenbuildstrategies media b3ceac34) |
| Weiss et al. 2022 — AlSi10Mg LPBF impeller, low utilization scenario | AlSi10Mg, LPBF + post-processing | 1 impeller; scenario totals based on 1,840 components over 8 years | Cradle-to-gate | LPBF Al component energy literature range cited as 73–94 MJ/kg; much higher reports 374–520 MJ/kg on other systems; total electricity for modeled functional unit 238,696 kWh | 131.19 kg CO2e/part | Gas atomization yield only ~30% in 20–63 µm usable fraction; some >63 µm powder not counted as waste | LPBF downtime/base load is major driver; machine + cooling account for 42% of electricity during downtime; Al extraction contributes ~42–47% of impacts (weiss2022evaluationofthe pages 17-19, weiss2022evaluationofthe pages 14-17, weiss2022evaluationofthe pages 1-3) |
| Weiss et al. 2022 — AlSi10Mg LPBF impeller, higher utilization scenario | AlSi10Mg, LPBF + post-processing | 1 impeller; scenario totals based on 7,360 components over 8 years | Cradle-to-gate | Same process context; 4 impellers/build lowers per-part burden; scenario build reported elsewhere in review as 775.6 kWh/build for 4 impellers | 41.35 kg CO2e/part | Same ~30% usable atomization yield; reuse/reconditioning of unmelted powder assumed | Higher machine utilization sharply lowers per-part CO2; downtime share falls to ~33% of electricity; switching to secondary Al can reduce total CO2e by ~60–63% in optimized scenarios (weiss2022evaluationofthe pages 17-19, weiss2022evaluationofthe pages 14-17, yadegari2025aluminumlaseradditive pages 4-6) |
| Priarone et al. 2023 — conventional reference | Cast iron bracket, casting + finish machining | 1 automotive bracket | Cradle-to-grave study; values below are manufacturing/material inputs | Casting 10–11 MJ/kg; finish machining 5–6 MJ/kg removed | Cast iron primary material CO2: 2.3–2.5 kg CO2/kg; substituted/end-of-life-adjusted material CO2: 2.9–4.2 kg CO2/kg | Material yield yCM = 1.57 | Conventional bracket is heavier; study assumes car life 200,000 km and compares against lightweighted redesign rather than same-geometry part (priarone2023additivemanufacturingfor pages 8-9, priarone2023additivemanufacturingfor pages 9-10) |
| Priarone et al. 2023 — LPBF redesign | Topology-optimized AlSi10Mg bracket, DMLS/LPBF | 1 automotive bracket; AM job produced 2 brackets at 0.428 kg each | Cradle-to-grave study; values below are manufacturing/material inputs | DMLS specific electric energy 328 MJ/kg; measured machine energy 90.4 kWh/job (2 h setup + 27 h deposition for 2 brackets); powder atomization adds 8.1 MJ/kg | AlSi10Mg primary material CO2: 11.5–12.7 kg CO2/kg; powder atomization adds ~0.5 kg CO2/kg | Material yield yAM = 1.22 | 69% mass reduction (k = 0.31) is central; AlSi10Mg powder has ~4–5× higher material carbon intensity than cast iron, but use-phase savings and recycling can offset this (priarone2023additivemanufacturingfor pages 8-9, priarone2023additivemanufacturingfor pages 9-10) |
| Yadegari et al. 2025 review — favorable LPBF range | Aluminum alloys (mainly AlSi10Mg), LPBF/PBF-LB/M | Per kg printed part | Cradle-to-gate | 73–94 MJ/kg | 5.0–6.4 kg CO2/kg | Powder yield for PBF feedstock often 20–40%; discarded fractions can dominate embodied impacts | Review synthesizes multiple studies; favorable values reflect better electricity/process efficiency and should not be treated as universal (yadegari2025aluminumlaseradditive pages 4-6, yadegari2025aluminumlaseradditive pages 6-8) |
| Yadegari et al. 2025 review — unfavorable LPBF range | Aluminum alloys (mainly AlSi10Mg), LPBF/PBF-LB/M | Per kg printed part | Cradle-to-gate | 374–520 MJ/kg | 25.4–35.4 kg CO2/kg | Poor powder yield and inert-gas-intensive atomization can push usable-powder burdens above 180 MJ/kg and >25 kg CO2/kg | Review notes powder production, gas choice, build utilization, and design optimization are dominant sensitivities; AM advantage over conventional routes appears mainly for high complexity/lightweighting cases (yadegari2025aluminumlaseradditive pages 4-6, yadegari2025aluminumlaseradditive pages 6-8) |


*Table: This table compiles the most directly relevant quantitative environmental data found for aluminum-alloy LPBF and comparable conventional routes. It highlights where evidence is strong at the part level, where only LPBF-specific ranges exist, and which assumptions most strongly change the comparison.*

## LPBF aluminum alloys: what quantitative sustainability data exists?
### 1) Energy consumption
Published cradle-to-gate LPBF aluminum energy intensities span a wide range depending on machine, utilization, and system boundary. A review focused on aluminum laser AM reports a “favorable” range of ~73–94 MJ/kg printed (≈20–26 kWh/kg) and CO2 of ~5.0–6.4 kg CO2/kg, but also reports “unfavorable” cases of 374–520 MJ/kg (≈104–144 kWh/kg) and 25.4–35.4 kg CO2/kg under less favorable efficiency/electricity assumptions. (yadegari2025aluminumlaseradditive pages 4-6)

At the part/job level, a topology-optimized automotive bracket printed in AlSi10Mg via DMLS/LPBF reported ~90.4 kWh electrical energy for a job producing two brackets (2 h setup + 27 h deposition), with a DMLS specific electric energy reported as 328 MJ/kg (≈91 kWh/kg). (priarone2023additivemanufacturingfor pages 8-9)

### 2) Material waste / material efficiency
Material-efficiency reporting for LPBF aluminum commonly includes:
- Powder atomization yield into the “in-spec” particle-size distribution for LPBF (often a minority of atomized mass). An AlSi10Mg LPBF ecological-footprint case study assumes only ~30% of atomized powder is in the 20–63 µm fraction needed for LPBF. (weiss2022evaluationofthe pages 17-19)
- Part-level B2F ratio (printed mass + supports relative to final part mass). In the aerospace bracket comparison, LPBF achieved B2F ≈ 1:1.2 (i.e., low waste), while CNC was far higher waste. (sargioti2026simulationdrivenbuildstrategies pages 15-16, sargioti2026simulationdrivenbuildstrategies media b3ceac34)

### 3) Carbon footprint (CO2e)
Cradle-to-gate carbon footprints for AlSi10Mg LPBF parts are reported at part-level in specific case studies and at per-kg level in reviews.
- In an AlSi10Mg impeller case study, cradle-to-gate CO2e varied strongly with utilization: ~131.19 kg CO2e/part in a low utilization scenario vs ~41.35 kg CO2e/part in a higher utilization scenario. (weiss2022evaluationofthe pages 17-19)
- The aluminum laser AM review cited above reports the per-kg ranges (5.0–6.4 kg CO2/kg favorable; 25.4–35.4 kg CO2/kg unfavorable), emphasizing strong sensitivity to electricity mix, powder production, and utilization. (yadegari2025aluminumlaseradditive pages 4-6)

## Direct comparison for aluminum parts: LPBF vs conventional manufacturing
### Comparative case: CNC machining vs LPBF for an aerospace bearing bracket
A cradle-to-gate study comparing CNC machining (Al 7175-T7351) to LPBF (Scalmalloy®) reported all three requested metrics:

**Energy consumption (per part):** CNC machining exceeded 100 kWh/part, whereas LPBF consumed ~40 kWh/part (single-part build) or ~37 kWh/part (three-part nested build). (sargioti2026simulationdrivenbuildstrategies pages 12-15, sargioti2026simulationdrivenbuildstrategies pages 15-16, sargioti2026simulationdrivenbuildstrategies media b3ceac34)

**Material waste (B2F / scrap):** CNC had B2F = 1:7 with ~86% of raw material lost as waste; LPBF had B2F ≈ 1:1.2. (sargioti2026simulationdrivenbuildstrategies pages 15-16, sargioti2026simulationdrivenbuildstrategies media b3ceac34)

**Carbon footprint (cradle-to-gate CO2e per part):** CNC was ~11,000 g CO2e/part; LPBF was ~1,122 g CO2e/part (strategy 1) and ~820 g CO2e/part (strategy 2), i.e., >90% reduction in this specific study. (sargioti2026simulationdrivenbuildstrategies pages 15-16, sargioti2026simulationdrivenbuildstrategies media b3ceac34, sargioti2026simulationdrivenbuildstrategies media 24d97300)

This comparison indicates that, for this part and electricity assumptions, LPBF reduced both energy and GWP while greatly improving material efficiency. However, the same broader literature emphasizes that LPBF is not universally lower-impact; results flip when utilization is low, powder production burdens are high, or post-processing is extensive. (yadegari2025aluminumlaseradditive pages 4-6, weiss2022evaluationofthe pages 14-17)

### Conventional route context beyond CNC (casting + machining)
In a cradle-to-grave automotive case study (cast-iron bracket baseline vs topology-optimized LPBF AlSi10Mg redesign), the authors report conventional-process energy intensities of ~10–11 MJ/kg for casting and ~5–6 MJ/kg per kg removed in finish machining. They also report a higher conventional material yield factor (yCM = 1.57) versus the AM route (yAM = 1.22), reflecting higher waste for the conventional route in their modeled comparison. (priarone2023additivemanufacturingfor pages 8-9)

## Key drivers and how to interpret the comparison
1. **LPBF electricity and utilization dominate LPBF impacts.** In the AlSi10Mg impeller case study, LPBF downtime and base-load electricity were major contributors; increasing parts per build reduced CO2e/part markedly. (weiss2022evaluationofthe pages 17-19, weiss2022evaluationofthe pages 14-17)
2. **Powder production and powder-yield assumptions are critical for aluminum LPBF.** The assumed fraction of atomized powder in the usable PSD (e.g., ~30%) can strongly influence upstream burdens, and reviews highlight that powder production (including inert gas use) can dominate cradle-to-gate impacts. (yadegari2025aluminumlaseradditive pages 6-8, weiss2022evaluationofthe pages 17-19)
3. **Material waste differs by mechanism:** CNC waste is dominated by chip/swarf (captured by B2F); LPBF waste is dominated by supports, spatter, and powder losses/refresh, plus upstream atomization yield losses. Direct numerical comparisons are therefore most meaningful when the system boundary includes both feedstock production and recycling credits. (sargioti2026simulationdrivenbuildstrategies pages 15-16, weiss2022evaluationofthe pages 17-19)

## Bottom line comparison (supported by retrieved evidence)
- **Energy consumption:** In the best-documented aluminum-part head-to-head dataset, LPBF (37–40 kWh/part) used less energy than CNC machining (>100 kWh/part). Literature ranges for LPBF aluminum per-mass energy are broad (~73–94 MJ/kg favorable up to 374–520 MJ/kg unfavorable), indicating strong dependence on machine and boundary assumptions. (sargioti2026simulationdrivenbuildstrategies pages 15-16, yadegari2025aluminumlaseradditive pages 4-6)
- **Material waste:** LPBF can drastically reduce material waste for machined-from-billet parts (B2F ~1:1.2 vs 1:7 in the bracket case), but powder-production yields (e.g., ~30% in-spec) and powder handling/reconditioning determine whether “system-level” waste is truly low. (sargioti2026simulationdrivenbuildstrategies pages 15-16, weiss2022evaluationofthe pages 17-19)
- **Carbon footprint:** For the aerospace bracket, LPBF reduced cradle-to-gate CO2e from ~11,000 g/part to ~820–1,122 g/part (>90% reduction). For AlSi10Mg LPBF parts more generally, reported CO2e varies substantially with utilization (e.g., ~131 vs ~41 kg CO2e/impeller in two scenarios). (sargioti2026simulationdrivenbuildstrategies pages 15-16, weiss2022evaluationofthe pages 17-19)

## Evidence gaps
Within the retrieved sources, aluminum-specific, like-for-like comparisons of LPBF vs **casting/forging of the same aluminum part geometry** with explicit energy/waste/CO2 values are limited; much of the detailed comparative evidence is part-specific (bracket case) or is reported as ranges/review synthesis rather than harmonized functional units. (yadegari2025aluminumlaseradditive pages 4-6, baroutaji2025criticalreviewon pages 11-13)

References

1. (sargioti2026simulationdrivenbuildstrategies pages 12-15): Nikoletta Sargioti, Evangelia K. Karaxi, Amin S. Azar, and Elias P. Koumoulos. Simulation-driven build strategies and sustainability analysis of cnc machining and laser powder bed fusion for aerospace brackets. Applied Sciences, 16:1360, Jan 2026. URL: https://doi.org/10.3390/app16031360, doi:10.3390/app16031360. This article has 0 citations.

2. (sargioti2026simulationdrivenbuildstrategies pages 15-16): Nikoletta Sargioti, Evangelia K. Karaxi, Amin S. Azar, and Elias P. Koumoulos. Simulation-driven build strategies and sustainability analysis of cnc machining and laser powder bed fusion for aerospace brackets. Applied Sciences, 16:1360, Jan 2026. URL: https://doi.org/10.3390/app16031360, doi:10.3390/app16031360. This article has 0 citations.

3. (sargioti2026simulationdrivenbuildstrategies media b3ceac34): Nikoletta Sargioti, Evangelia K. Karaxi, Amin S. Azar, and Elias P. Koumoulos. Simulation-driven build strategies and sustainability analysis of cnc machining and laser powder bed fusion for aerospace brackets. Applied Sciences, 16:1360, Jan 2026. URL: https://doi.org/10.3390/app16031360, doi:10.3390/app16031360. This article has 0 citations.

4. (sargioti2026simulationdrivenbuildstrategies pages 5-7): Nikoletta Sargioti, Evangelia K. Karaxi, Amin S. Azar, and Elias P. Koumoulos. Simulation-driven build strategies and sustainability analysis of cnc machining and laser powder bed fusion for aerospace brackets. Applied Sciences, 16:1360, Jan 2026. URL: https://doi.org/10.3390/app16031360, doi:10.3390/app16031360. This article has 0 citations.

5. (weiss2022evaluationofthe pages 17-19): C. Weiss, C. Boedger, E. Schiefer, D. Heussen, and C.L. Haefner. Evaluation of the ecological footprint for parts from alsi10mg manufactured by laser powder bed fusion. Unknown, Jan 2022. URL: https://doi.org/10.26153/tsw/44578, doi:10.26153/tsw/44578. This article has 10 citations.

6. (weiss2022evaluationofthe pages 14-17): C. Weiss, C. Boedger, E. Schiefer, D. Heussen, and C.L. Haefner. Evaluation of the ecological footprint for parts from alsi10mg manufactured by laser powder bed fusion. Unknown, Jan 2022. URL: https://doi.org/10.26153/tsw/44578, doi:10.26153/tsw/44578. This article has 10 citations.

7. (weiss2022evaluationofthe pages 1-3): C. Weiss, C. Boedger, E. Schiefer, D. Heussen, and C.L. Haefner. Evaluation of the ecological footprint for parts from alsi10mg manufactured by laser powder bed fusion. Unknown, Jan 2022. URL: https://doi.org/10.26153/tsw/44578, doi:10.26153/tsw/44578. This article has 10 citations.

8. (yadegari2025aluminumlaseradditive pages 4-6): Mohammad Javad Yadegari, Alessandra Martucci, Sara Biamino, Daniele Ugues, Laura Montanaro, Paolo Fino, and Mariangela Lombardi. Aluminum laser additive manufacturing: a review on challenges and opportunities through the lens of sustainability. Applied Sciences, 15:2221, Feb 2025. URL: https://doi.org/10.3390/app15042221, doi:10.3390/app15042221. This article has 11 citations.

9. (priarone2023additivemanufacturingfor pages 8-9): Paolo C. Priarone, Angioletta R. Catalano, and Luca Settineri. Additive manufacturing for the automotive industry: on the life-cycle environmental implications of material substitution and lightweighting through re-design. Progress in Additive Manufacturing, 8:1229-1240, Jan 2023. URL: https://doi.org/10.1007/s40964-023-00395-x, doi:10.1007/s40964-023-00395-x. This article has 83 citations and is from a peer-reviewed journal.

10. (priarone2023additivemanufacturingfor pages 9-10): Paolo C. Priarone, Angioletta R. Catalano, and Luca Settineri. Additive manufacturing for the automotive industry: on the life-cycle environmental implications of material substitution and lightweighting through re-design. Progress in Additive Manufacturing, 8:1229-1240, Jan 2023. URL: https://doi.org/10.1007/s40964-023-00395-x, doi:10.1007/s40964-023-00395-x. This article has 83 citations and is from a peer-reviewed journal.

11. (yadegari2025aluminumlaseradditive pages 6-8): Mohammad Javad Yadegari, Alessandra Martucci, Sara Biamino, Daniele Ugues, Laura Montanaro, Paolo Fino, and Mariangela Lombardi. Aluminum laser additive manufacturing: a review on challenges and opportunities through the lens of sustainability. Applied Sciences, 15:2221, Feb 2025. URL: https://doi.org/10.3390/app15042221, doi:10.3390/app15042221. This article has 11 citations.

12. (sargioti2026simulationdrivenbuildstrategies media 24d97300): Nikoletta Sargioti, Evangelia K. Karaxi, Amin S. Azar, and Elias P. Koumoulos. Simulation-driven build strategies and sustainability analysis of cnc machining and laser powder bed fusion for aerospace brackets. Applied Sciences, 16:1360, Jan 2026. URL: https://doi.org/10.3390/app16031360, doi:10.3390/app16031360. This article has 0 citations.

13. (baroutaji2025criticalreviewon pages 11-13): Ahmad Baroutaji, Arun Arjunan, John Robinson, Aaron Vance, and Abul Arafat. Critical review on the sustainability of metal additive manufacturing: environmental and economic perspectives. Renewable and Sustainable Energy Technology, Jul 2025. URL: https://doi.org/10.53941/rset.2025.100006, doi:10.53941/rset.2025.100006. This article has 3 citations.


---

## Query 10

**Question:** What are the most promising aluminum alloy compositions for high-temperature AM applications (sustained service above 200°C)? Rank systems by strength retention at 250°C and 300°C with quantitative data. Include Al-Ce, Al-Fe-V-Si, Al-Mn-Sc, and Al-Cu-Mn-Zr.

**Task ID:** `dd8b81be-95fc-4ae4-ba40-e21df60f3761`

**Status:** complete

## Objective
Identify and rank aluminum alloy systems reported for high-temperature additive manufacturing (AM) with sustained service above 200 °C, focusing on quantitative strength retention at **250 °C** and **300 °C**. The requested systems were: **Al–Ce**, **Al–Fe–V–Si**, **Al–Mn–Sc**, and **Al–Cu–Mn–Zr**.

## Evidence-based ranked comparison (strength at temperature)
The most directly comparable metric across the available sources is **0.2% offset tensile yield strength (YS)** measured at temperature. Where room-temperature (RT) YS is available for the same condition, retention ratios are computed.

| System | Representative composition (wt%) | Process | Condition | Metric type | RT YS (MPa) | YS at 250°C (MPa) | Retention at 250°C vs RT | YS at 300°C (MPa) | Retention at 300°C vs RT | Rank at 250°C | Rank at 300°C | Notes on extraction |
|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Al–Mn–Sc | Al–Mn–Sc (exact bulk wt% not stated in retrieved text); aged condition strengthened by Al3(Sc,Zr) | LPBF/SLM | Heat-treated, aged 300°C/5 h | YS | 572 ± 4 | ~245 | ~0.43 | ~178 | ~0.31 | 1 | 1 | 250°C and 300°C values read from Fig. 9a at 10^-3 s^-1; RT YS from text (yan2023microstructuresandhigh media 79078106, yan2023microstructuresandhigh media 8f198239, yan2023microstructuresandhigh pages 6-10) |
| Al–Cu–Mn–Zr | Al–9Cu–Mn–0.9Zr | LPBF/SLM | As-printed, 200°C baseplate | YS | — | ~180 | — | ~130 | — | 2 | 2 | 250°C and 300°C values approximated from Fig. 4b; text confirms strength advantage persists to ~300°C but does not tabulate values (shyam2020anadditivelymanufactured media 5969efef, shyam2020anadditivelymanufactured pages 1-4, shyam2020anadditivelymanufactured pages 4-9) |
| Al–Ce | Al–10Ce–8Mn | LPBF | As-fabricated | YS | 268 ± 15 | ~110 | ~0.41 | ~90 | ~0.34 | 3 | 3 | 250°C and 300°C values estimated from Fig. 7b; RT YS from Table 3 (plotkowski2020microstructureandproperties media 1c5a5410, plotkowski2020microstructureandproperties pages 6-8) |
| Al–Fe–V–Si | Al–8.5Fe–1.3V–1.7Si | SLM | As-deposited / preheated build | YS not reported; RT UTS only | — | not reported in retrieved sources | — | not reported in retrieved sources | — | — | — | Retrieved sources report RT UTS = 454 MPa for horizontal samples, but no 250°C/300°C tensile YS values for AM condition were found (sun2023microstructurecrackingbehavior pages 8-10, sun2015selectivelasermelting pages 8-10) |
| Ranking summary | — | — | — | YS at 250°C | — | — | — | — | — | 1: Al–Mn–Sc; 2: Al–Cu–Mn–Zr; 3: Al–10Ce–8Mn; 4: Al–Fe–V–Si (insufficient data) | — | Ranking uses only available 250°C YS values from retrieved figures/text (shyam2020anadditivelymanufactured media 5969efef, plotkowski2020microstructureandproperties media 1c5a5410, yan2023microstructuresandhigh media 79078106, yan2023microstructuresandhigh media 8f198239, plotkowski2020microstructureandproperties pages 6-8) |
| Ranking summary | — | — | — | YS at 300°C | — | — | — | — | — | — | 1: Al–Mn–Sc; 2: Al–Cu–Mn–Zr; 3: Al–10Ce–8Mn; 4: Al–Fe–V–Si (insufficient data) | Ranking uses only available 300°C YS values from retrieved figures/text (shyam2020anadditivelymanufactured media 5969efef, plotkowski2020microstructureandproperties media 1c5a5410, yan2023microstructuresandhigh media 79078106, yan2023microstructuresandhigh media 8f198239, plotkowski2020microstructureandproperties pages 6-8) |


*Table: This table ranks the requested AM aluminum alloy systems by available tensile yield strength at 250°C and 300°C using only quantitative values extracted from the retrieved figures and text. It also reports room-temperature baselines and calculated retention where those baselines were available.*

### Rank by yield strength at 250 °C (523 K)
1. **Al–Mn–Sc (LPBF, aged 300 °C/5 h)**: **YS ≈ 245 MPa at 250 °C** (10−3 s−1). (yan2023microstructuresandhigh media 79078106, yan2023microstructuresandhigh media 8f198239)
2. **Al–Cu–Mn–Zr / “ACMZ” (LPBF, as-printed, 200 °C baseplate)**: **YS ≈ 180 MPa at 250 °C** (estimated from tensile-property vs temperature plot). (shyam2020anadditivelymanufactured media 5969efef)
3. **Al–Ce–Mn (LPBF Al–10Ce–8Mn)**: **YS ≈ 110 MPa at 250 °C** (estimated from YS vs temperature plot). (plotkowski2020microstructureandproperties media 1c5a5410)
4. **Al–Fe–V–Si (SLM Al–8.5Fe–1.3V–1.7Si)**: **not rankable at 250 °C** from retrieved sources (no 250 °C tensile YS/UTS provided). (sun2023microstructurecrackingbehavior pages 8-10, sun2015selectivelasermelting pages 8-10)

### Rank by yield strength at 300 °C (573 K)
1. **Al–Mn–Sc (LPBF, aged 300 °C/5 h)**: **YS ≈ 178 MPa at 300 °C** (10−3 s−1). (yan2023microstructuresandhigh media 79078106, yan2023microstructuresandhigh media 8f198239)
2. **Al–Cu–Mn–Zr / “ACMZ” (LPBF, as-printed)**: **YS ≈ 120–140 MPa at 300 °C** (estimated; AM and cast converge near 300 °C). (shyam2020anadditivelymanufactured media 5969efef, shyam2020anadditivelymanufactured pages 4-9)
3. **Al–Ce–Mn (LPBF Al–10Ce–8Mn)**: **YS ≈ 90 MPa at 300 °C** (estimated from YS vs temperature plot). (plotkowski2020microstructureandproperties media 1c5a5410)
4. **Al–Fe–V–Si (SLM Al–8.5Fe–1.3V–1.7Si)**: **not rankable at 300 °C** from retrieved sources (no 300 °C tensile YS/UTS provided). (sun2023microstructurecrackingbehavior pages 8-10, sun2015selectivelasermelting pages 8-10)

## Strength retention (where RT baselines were available in retrieved sources)
### Al–Mn–Sc (LPBF, aged 300 °C/5 h)
RT YS after aging is reported as **572 ± 4 MPa**. (yan2023microstructuresandhigh pages 6-10)
* Retention at 250 °C: ~245/572 ≈ **0.43**. (yan2023microstructuresandhigh media 79078106, yan2023microstructuresandhigh media 8f198239, yan2023microstructuresandhigh pages 6-10)
* Retention at 300 °C: ~178/572 ≈ **0.31**. (yan2023microstructuresandhigh media 79078106, yan2023microstructuresandhigh media 8f198239, yan2023microstructuresandhigh pages 6-10)

### Al–Ce–Mn (LPBF Al–10Ce–8Mn)
RT YS is reported as **268 ± 15 MPa** in selected tensile data. (plotkowski2020microstructureandproperties pages 6-8)
* Retention at 250 °C: ~110/268 ≈ **0.41** (approx.). (plotkowski2020microstructureandproperties media 1c5a5410, plotkowski2020microstructureandproperties pages 6-8)
* Retention at 300 °C: ~90/268 ≈ **0.34** (approx.). (plotkowski2020microstructureandproperties media 1c5a5410, plotkowski2020microstructureandproperties pages 6-8)

### Al–Cu–Mn–Zr (LPBF ACMZ)
High-temperature YS values at 250 °C and 300 °C are available from the figure, and the study describes ASTM E8/E21 testing with a 30 min soak and specified strain-rate schedule, but **a numeric RT YS for the same condition was not extractable from the retrieved text pages** (it may be in Fig. 4a/other sections not captured numerically in the provided excerpt). (shyam2020anadditivelymanufactured media 5969efef, shyam2020anadditivelymanufactured pages 4-9)

## Most promising compositions (within the requested set)
### 1) Al–Mn–Sc (Sc/Zr-containing) — best YS at 250 °C and 300 °C in retrieved data
A representative LPBF Al–Mn–Sc alloy, aged at **300 °C for 5 h**, achieves high RT YS (≈572 MPa) with elevated-temperature YS ≈245 MPa at 250 °C and ≈178 MPa at 300 °C (10−3 s−1), suggesting the best strength retention among the systems with directly comparable data in the retrieved set. (yan2023microstructuresandhigh media 79078106, yan2023microstructuresandhigh media 8f198239, yan2023microstructuresandhigh pages 6-10)

### 2) Al–Cu–Mn–Zr (ACMZ; ~Al–9Cu–Mn–0.9Zr wt%) — strong at 250–300 °C with θ′ strengthening stability
The LPBF ACMZ alloy built on a **200 °C baseplate** shows **YS ≈180 MPa at 250 °C** and **≈120–140 MPa at 300 °C**, consistent with an Al–Cu alloy benefiting from in-situ θ′ precipitation and thermal stability to ~350 °C discussed in the paper. (shyam2020anadditivelymanufactured media 5969efef, shyam2020anadditivelymanufactured pages 4-9)

### 3) Al–Ce–Mn (Al–10Ce–8Mn wt%) — stable microstructure; moderate YS at 250–300 °C but notable retention vs its RT strength
For LPBF Al–10Ce–8Mn, the retrieved figure indicates **YS ≈110 MPa at 250 °C** and **≈90 MPa at 300 °C**, with RT YS ≈268 MPa in selected tests; this corresponds to ~0.41–0.34 retention (approx.). (plotkowski2020microstructureandproperties media 1c5a5410, plotkowski2020microstructureandproperties pages 6-8)

### 4) Al–Fe–V–Si (AA8009-type: Al–8.5Fe–1.3V–1.7Si wt%) — promising class but missing 250/300 °C tensile data in retrieved sources
SLM Al–8.5Fe–1.3V–1.7Si produced crack-free coupons and reported **RT UTS ≈454 MPa** (horizontal builds) but the accessible sources here did not provide tensile YS/UTS at 250 °C or 300 °C for ranking. (sun2023microstructurecrackingbehavior pages 8-10, sun2015selectivelasermelting pages 8-10)

## Limitations of this ranking
* **Al–Fe–V–Si**: quantitative **250 °C/300 °C tensile strength** is not available in the retrieved documents, so it cannot be fairly ranked against the other systems on the user’s requested basis. (sun2023microstructurecrackingbehavior pages 8-10, sun2015selectivelasermelting pages 8-10)
* Several values are **estimated from plots** (not tabulated). Those entries are explicitly marked as approximate and should be re-digitized from the original high-resolution figures for design allowables. (shyam2020anadditivelymanufactured media 5969efef, plotkowski2020microstructureandproperties media 1c5a5410, yan2023microstructuresandhigh media 79078106, yan2023microstructuresandhigh media 8f198239)

## Conclusion
Within the retrieved quantitative dataset, the most promising systems for sustained >200 °C AM service (by tensile YS retention at 250 °C and 300 °C) are, in order: **Al–Mn–Sc (aged)** > **Al–Cu–Mn–Zr (ACMZ)** > **Al–10Ce–8Mn**. **Al–Fe–V–Si** remains a strong candidate class for heat-resistant Al, but **cannot be ranked at 250 °C/300 °C here due to missing tensile-at-temperature data in the retrieved sources**.

References

1. (yan2023microstructuresandhigh media 79078106): Yuqing Yan, Chengqi Lu, Zhenyu Chen, Yuhao Zhuo, Chuanyang Wang, and Qingbo Jia. Microstructures and high temperature tensile behaviours of laser powder bed fusion fabricated al-mn-sc alloy. Metals, 13:788, Apr 2023. URL: https://doi.org/10.3390/met13040788, doi:10.3390/met13040788. This article has 9 citations.

2. (yan2023microstructuresandhigh media 8f198239): Yuqing Yan, Chengqi Lu, Zhenyu Chen, Yuhao Zhuo, Chuanyang Wang, and Qingbo Jia. Microstructures and high temperature tensile behaviours of laser powder bed fusion fabricated al-mn-sc alloy. Metals, 13:788, Apr 2023. URL: https://doi.org/10.3390/met13040788, doi:10.3390/met13040788. This article has 9 citations.

3. (yan2023microstructuresandhigh pages 6-10): Yuqing Yan, Chengqi Lu, Zhenyu Chen, Yuhao Zhuo, Chuanyang Wang, and Qingbo Jia. Microstructures and high temperature tensile behaviours of laser powder bed fusion fabricated al-mn-sc alloy. Metals, 13:788, Apr 2023. URL: https://doi.org/10.3390/met13040788, doi:10.3390/met13040788. This article has 9 citations.

4. (shyam2020anadditivelymanufactured media 5969efef): A. Shyam, A. Plotkowski, S. Bahl, K. Sisco, L.F. Allard, Y. Yang, J.A. Haynes, and R.R. Dehoff. An additively manufactured alcumnzr alloy microstructure and tensile mechanical properties. Materialia, 12:100758, Aug 2020. URL: https://doi.org/10.1016/j.mtla.2020.100758, doi:10.1016/j.mtla.2020.100758. This article has 66 citations and is from a peer-reviewed journal.

5. (shyam2020anadditivelymanufactured pages 1-4): A. Shyam, A. Plotkowski, S. Bahl, K. Sisco, L.F. Allard, Y. Yang, J.A. Haynes, and R.R. Dehoff. An additively manufactured alcumnzr alloy microstructure and tensile mechanical properties. Materialia, 12:100758, Aug 2020. URL: https://doi.org/10.1016/j.mtla.2020.100758, doi:10.1016/j.mtla.2020.100758. This article has 66 citations and is from a peer-reviewed journal.

6. (shyam2020anadditivelymanufactured pages 4-9): A. Shyam, A. Plotkowski, S. Bahl, K. Sisco, L.F. Allard, Y. Yang, J.A. Haynes, and R.R. Dehoff. An additively manufactured alcumnzr alloy microstructure and tensile mechanical properties. Materialia, 12:100758, Aug 2020. URL: https://doi.org/10.1016/j.mtla.2020.100758, doi:10.1016/j.mtla.2020.100758. This article has 66 citations and is from a peer-reviewed journal.

7. (plotkowski2020microstructureandproperties media 1c5a5410): A. Plotkowski, K. Sisco, S. Bahl, A. Shyam, Ying Yang, Lawrence F. Allard, P. Nandwana, A. Rossy, and R. Dehoff. Microstructure and properties of a high temperature al–ce–mn alloy produced by additive manufacturing. Acta Materialia, 196:595-608, Sep 2020. URL: https://doi.org/10.1016/j.actamat.2020.07.014, doi:10.1016/j.actamat.2020.07.014. This article has 250 citations and is from a highest quality peer-reviewed journal.

8. (plotkowski2020microstructureandproperties pages 6-8): A. Plotkowski, K. Sisco, S. Bahl, A. Shyam, Ying Yang, Lawrence F. Allard, P. Nandwana, A. Rossy, and R. Dehoff. Microstructure and properties of a high temperature al–ce–mn alloy produced by additive manufacturing. Acta Materialia, 196:595-608, Sep 2020. URL: https://doi.org/10.1016/j.actamat.2020.07.014, doi:10.1016/j.actamat.2020.07.014. This article has 250 citations and is from a highest quality peer-reviewed journal.

9. (sun2023microstructurecrackingbehavior pages 8-10): Shao-Bo Sun, Li-Jing Zheng, Jin-Hui Liu, and Hu Zhang. Microstructure, cracking behavior and control of al–fe–v–si alloy produced by selective laser melting. Rare Metals, 42:1353-1362, Jan 2023. URL: https://doi.org/10.1007/s12598-016-0846-9, doi:10.1007/s12598-016-0846-9. This article has 36 citations and is from a peer-reviewed journal.

10. (sun2015selectivelasermelting pages 8-10): Shaobo Sun, Lijing Zheng, Yingying Liu, Jinhui Liu, and Hu Zhang. Selective laser melting of al-fe-v-si heat-resistant aluminum alloy powder: modeling and experiments. The International Journal of Advanced Manufacturing Technology, 80:1787-1797, Apr 2015. URL: https://doi.org/10.1007/s00170-015-7137-8, doi:10.1007/s00170-015-7137-8. This article has 43 citations.


---

