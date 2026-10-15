# Edison Iteration 6: Funded Program Comparison

*Edison Scientific LITERATURE query (task 92f0a824, 2026-04-09). Compares FLAIME metrics against actual metrics from funded DOE/DARPA programs: ARPA-E ULTIMATE, AMMTO DuAlumin-3D, BES/DMREF, NSF CAREER, DARPA DSO, and DOE TCR.*

---

Question: 
CONTEXT: FLAIME is a DOE Genesis Mission Phase I proposal for autonomous closed-loop alloy discovery.
After 5 rounds of Edison refinement, the metrics framework is mature. This iteration focuses on 
comparing FLAIME's proposed metrics against ACTUAL metrics from funded DOE materials/AI programs.

TASK: Compare FLAIME's proposed metrics structure and targets against published metrics from these 
specific funded programs:

1. **DOE ARPA-E ULTIMATE** (Ames Lab, gas atomization + alloy development) — what metrics did they use?
2. **DOE AMMTO DuAlumin-3D** (ORNL, Al alloy development for AM) — throughput, properties, qualification metrics?
3. **DOE BES DMREF programs** in materials discovery — what KPIs do they report?
4. **NSF CAREER awards** in autonomous materials discovery — metrics structure?
5. **DARPA DSO** materials programs — what go/no-go criteria do they use?
6. **DOE TCR (Transformational Challenge Reactor)** at ORNL — qualification metrics for AM nuclear components?

For EACH program:
- What quantitative metrics did they propose/report?
- How did they structure their go/no-go decisions?
- What throughput levels did they actually achieve?
- What AI/ML performance metrics did they report?
- How did they handle workforce development metrics?

Then: Identify GAPS where FLAIME is missing metrics that these funded programs include, and 
STRENGTHS where FLAIME's metrics are more rigorous than typical funded programs.

Finally: Recommend the TOP 5 metrics additions or modifications based on this competitive analysis.

Include specific citations and program identifiers where possible.


## Competitive analysis scope and evidence limitations
This response compares FLAIME’s *intended* metric needs for autonomous closed-loop alloy discovery against **published/archival metrics** from the funded programs you listed. However, **the FLAIME proposal and its mature Edison-refined metric framework were not available in the retrieved document set**, so “gaps/strengths” are identified relative to a generic closed-loop alloy-discovery metrics stack (technical targets, throughput, ML, and workforce). Likewise, **primary DARPA DSO program BAAs/performer reports with explicit go/no-go criteria were not retrieved**, and **NSF CAREER award documents (award numbers and required education/workforce reporting) were not retrieved**; those parts are flagged as evidence gaps rather than inferred.

## Per-program comparison (metrics, gates, throughput, AI/ML, workforce)
A compact cross-program table is provided first.

| Program / identifier | Quantitative technical targets / metrics | Go / no-go structure | Throughput achieved | AI/ML performance metrics | Workforce development metrics |
|---|---|---|---|---|---|
| DOE ARPA-E ULTIMATE / BIRDSHOT (Ames Lab-led refractory alloy discovery) | Program targets included 1300°C yield strength ≥400 MPa; density limits as low as ≤9.0-9.1 g/cc in screening; thermal conductivity ≥12 W/m·K; fracture strain ≥2%; solidus thresholds ≥1900-2000°C; screening over an 11-element space; curated data assets of 363 hardness, 388 temperature-dependent yield-strength, and 177 fracture-strain experiments; 140 unique RHEA compositions synthesized and 116 homogenized/characterized; average synthesis rate 13 alloys/week (arroyave2024ultimatebirdshot.final pages 14-16, arroyave2024ultimatebirdshot.final pages 11-14, arroyave2024ultimatebirdshot.final pages 5-7) | Explicit milestone structure (e.g., MS.3.2 go/no-go required identifying 5-10 candidate alloys); project reported 13 initial candidates and final top 3 compositions; report states modified milestones were met/exceeded (arroyave2024ultimatebirdshot.final pages 5-7, arroyave2024ultimatebirdshot.final pages 16-19) | Planned ~12.6 million calculations (252 quinaries × ~50,000 calculations each); 140 arc-melted alloys; 108 characterized by SEM/EDX/XRD; 31 alloys tested in compression at 1300°C; atomizer capability 50-100 tons/year; Retech noted >500 materials melted on atomizer (arroyave2024ultimatebirdshot.final pages 5-7, arroyave2024ultimatebirdshot.final pages 9-11, arroyave2024ultimatebirdshot.final pages 16-19) | Hierarchical Gaussian Process models with informative priors; report says HGPs outperformed standard GPs and assessed MAE, RMSE, and Spearman rank-order coefficient, but no numeric ML scores were provided in retrieved excerpts (arroyave2024ultimatebirdshot.final pages 11-14) | Collaboration across Texas A&M, Brown, Ames, Thermo-Calc, and ORNL reported; no quantitative trainee/student metrics found in retrieved sources (arroyave2024ultimatebirdshot.final pages 16-19) |
| DOE AMMTO DuAlumin-3D (ORNL Al alloy for AM) | Nominal composition Al-9Ce-4Ni-0.5Mn-1Zr; LPBF on EOS M290 at 370 W, 1300 mm/s, 0.19 mm hatch, 30 μm layer thickness, 150°C preheat; built 104 mm diameter × 75 mm height cylinder; heat treated 350°C for 8 h; tensile RT-350°C at 5×10^-4 s^-1; fatigue at 150/250/350°C, R = -1, 50 Hz, runout 10^7 cycles; elastic modulus ~81 GPa (plotkowski2025additivelymanufacturinghightemperature pages 8-12) | Qualification-oriented test structure via ASTM E1461 and temperature-specific tensile/fatigue protocols; no explicit published go/no-go gate found in retrieved sources (plotkowski2025additivelymanufacturinghightemperature pages 8-12) | One representative near-net-shape build (104 mm × 75 mm) and multiple specimen types extracted; no explicit samples/day or builds/week throughput found in retrieved sources (plotkowski2025additivelymanufacturinghightemperature pages 8-12) | Not found in retrieved sources (plotkowski2025additivelymanufacturinghightemperature pages 8-12) | Not found in retrieved sources (plotkowski2025additivelymanufacturinghightemperature pages 8-12) |
| DMREF (program-level) + DMREF exemplar project: AM feedstock designed for uniform metallic printing | Program-level: 139 projects, 528 PIs, $172M total investment; ~75% of projects co-funded; project durations shifted from 3 to 4 years. Exemplar project metrics: 12 ASTM E8/E8M tensile specimens required (6 XY, 6 Z); UTS coefficient of variation target <3.5%; UTS >90% of commercial alloys; no UTS orientation difference at 95% confidence; achieved >99.6% density; defects <~20 μm and <~30 μm; measured CVs 0.33-0.94% and 0.7-1.8%; UTS reached 123% and 157% of benchmark alloys (schlueter2018designingmaterialsand pages 2-4, nuechterlein2021additivemanufacturingfeedstock pages 1-3) | Program evaluation emphasizes acceleration, iterative collaboration, training, and open access, but no universal DMREF go/no-go gate found. Exemplar project used milestone-like acceptance thresholds on specimen count, CV, benchmark-relative UTS, and orientation parity (schlueter2018designingmaterialsand pages 2-4, nuechterlein2021additivemanufacturingfeedstock pages 1-3) | Exemplar project printed required 12 tensile specimens; no broader DMREF throughput standard found in retrieved sources (nuechterlein2021additivemanufacturingfeedstock pages 1-3, schlueter2018designingmaterialsand pages 2-4) | Program description mentions ML/data mining/sparse approximation as desired capabilities, but no quantitative DMREF-wide AI/ML performance metrics found in retrieved sources (schlueter2018designingmaterialsand pages 2-4) | Program description explicitly emphasizes graduate student/postdoc co-advising, student exchange, new courses, symposia, outreach to underrepresented groups and K-12, and open educational materials; no quantitative trainee counts in retrieved sources (schlueter2018designingmaterialsand pages 2-4, schlueter2018designingmaterialsand pages 1-2) |
| NSF CAREER / autonomous discovery benchmark (represented by SDL metrics framework + closed-loop superconductors literature) | Suggested SDL metrics structure: degree of autonomy, operational lifetime, throughput, experimental precision, material usage, accessible parameter space, optimization efficiency. Example reported values from SDL literature: demonstrated unassisted lifetime 700 samples; demonstrated throughput 30-33 samples/hour; material usage 0.06-0.2 mL/sample; accessible parameter space 1.6×10^11. Closed-loop superconductors study ran 4 loops, rediscovered 5 superconductors absent from training data, found 1 new superconductor and 2 additional promising phase diagrams; one round evaluated 39 compounds from 190 candidates, with 39 stable and 83 nearly stable compositions (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto pages 2-3, pogue2023closedloopsuperconductingmaterials pages 1-2, pogue2023closedloopsuperconductingmaterials pages 2-3, pogue2023closedloopsuperconductingmaterials pages 5-6) | SDL framework recommends explicit autonomy-level classification and benchmarking, but no universal go/no-go thresholds. In superconductors closed loop, candidate filters included highest-Tc tertile and minimum classification score 0.66, plus stability/synthesizability screening before experiment (volk2024performancemetricsto pages 2-3, pogue2023closedloopsuperconductingmaterials pages 5-6) | SDL literature examples report 30-33 samples/hour, and in one cited platform 100 samples/hour demonstrated / 1200 measurements/hour theoretical; superconductors paper did not report end-to-end samples/day throughput in retrieved excerpts (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto pages 3-5, pogue2023closedloopsuperconductingmaterials pages 1-2) | Superconductors workflow used uncertainty-aware RooSt ensembles and LOCO-CV/Uniform-CV, but no standard metrics such as accuracy/AUC were numerically reported in retrieved excerpts; success rate stated to have more than doubled. SDL benchmarking paper also reports only 23% of surveyed studies used real-world benchmarking and 62% of ML-using studies validated models (pogue2023closedloopsuperconductingmaterials pages 1-2, pogue2023closedloopsuperconductingmaterials pages 5-6, volk2024performancemetricsto pages 5-6) | Not found in retrieved sources for NSF CAREER-specific trainee counts; broader SDL/NSF-adjacent literature emphasizes accessibility and training needs rather than quantified workforce KPIs in retrieved excerpts (volk2024performancemetricsto pages 5-6) |
| DARPA DSO materials programs | Not found in retrieved sources | Not found in retrieved sources | Not found in retrieved sources | Not found in retrieved sources | Not found in retrieved sources |
| DOE TCR (ORNL Transformational Challenge Reactor; AM qualification / digital thread) | Qualification framed around part-specific, localized property prediction. Quantitative metrics include 6299 tensile specimens for model training; ~230 GB public co-registered dataset; ~180 million pixelwise annotations for anomaly segmentation; ~3000 SS-J3 tensile samples tested in FY21 against a 5000-sample target; 485 MPa classification threshold; GNN R2 = 0.877; prediction uncertainty 31.9 MPa; 96.2% correct classification across 687 test super-voxels; 61% error reduction in UTS prediction relative to no in situ information (scime2023adatadrivenframework pages 1-2, scime2023adatadrivenframework pages 3-5, scime2021reportondiagnostic pages 44-47) | Explicit deployment guardrail: model returns "cannot predict" for out-of-distribution feature vectors; qualification paradigm shifts from locked-down process/feedstock qualification toward validated in situ sensor suites + algorithms and part-specific digital threads/digital twins (scime2021reportondiagnostic pages 44-47, scime2020reportonprogress pages 31-36, scime2023adatadrivenframework pages 2-3) | Thousands of tensile specimens tracked; 235-train/117-test early model split reported in 2020 progress work; FY21 campaign reached ~3000 samples with Phase 2 targeting another 5000 (scime2020reportonprogress pages 27-31, scime2021reportondiagnostic pages 44-47) | 61% UTS prediction error reduction; GNN R2 = 0.877; 31.9 MPa uncertainty; 96.2% threshold-classification accuracy; early work identified defect classes most correlated with YTS (powder, printed area, recoater streaking, swelling) (scime2023adatadrivenframework pages 1-2, scime2020reportonprogress pages 27-31, scime2021reportondiagnostic pages 44-47) | Not found in retrieved sources |


*Table: This table compares the published metrics structures, gates, throughput, AI/ML reporting, and workforce indicators across the requested benchmark programs. It is useful as a compact evidence-backed reference for identifying where FLAIME aligns with, exceeds, or misses common funded-program practices.*

### 1) DOE ARPA‑E ULTIMATE (Ames Lab; “ULTIMATE: BIRDSHOT” and related ULTIMATE projects)
**Quantitative metrics (technical targets and reported values)**
- ULTIMATE/BIRDSHOT used explicit, application-coupled property targets and filters in a staged downselect: e.g., **1300 °C yield strength ≥400 MPa**, **thermal conductivity ≥12 W/m·K**, **fracture strain ≥2%**, **solidus thresholds ≥1900–2000 °C** (stage-dependent), and **density limits down to ≤9.0–9.1 g/cc** in some filters. (arroyave2024ultimatebirdshot.final pages 14-16)
- Reported “data asset”/measurement-count metrics included **363 hardness experiments, 388 temperature-dependent yield-strength experiments, and 177 fracture-strain experiments** (curated). (arroyave2024ultimatebirdshot.final pages 14-16, arroyave2024ultimatebirdshot.final pages 16-19)

**Go/no-go and decision structure**
- BIRDSHOT documented a milestone gate **MS.3.2 Go/No‑Go: identify 5–10 candidate alloys**. The team reported 13 initial candidates and a final top set of compositions. (arroyave2024ultimatebirdshot.final pages 5-7)
- Related ULTIMATE projects also used explicit “Go/No-Go Milestone” language tied to phase reviews and meeting Phase 1 goals. (sharon2023computationallyguidedodsrefractory pages 4-6)

**Throughput (actual achieved and/or planned)**
- Computational exploration plan: **252 quinary systems × ~50,000 calculations each (~12.6 million calculations)**. (arroyave2024ultimatebirdshot.final pages 5-7)
- Experimental throughput: **140 unique alloys synthesized**, with an **average synthesis rate of ~13 alloys/week**; substantial characterization counts (e.g., SEM/EDX/XRD on 108 alloys) and high-temperature mechanical test development. (arroyave2024ultimatebirdshot.final pages 11-14, arroyave2024ultimatebirdshot.final pages 9-11)
- Manufacturing-scale throughput indicator (supply chain readiness): atomizer OEM capability **~50–100 tons/year**; also noted operational experience (hundreds of melts). (arroyave2024ultimatebirdshot.final pages 16-19, arroyave2024ultimatebirdshot.final pages 14-16)

**AI/ML performance metrics reported**
- AI/ML methods are described (Bayesian updating, k‑medoids sampling, hierarchical Gaussian processes, multi-objective Bayesian optimization), and BIRDSHOT reports using metrics like MAE/RMSE/Spearman Rs for evaluation, **but the retrieved excerpts do not provide numeric ML scores**. (arroyave2024ultimatebirdshot.final pages 11-14, arroyave2024ultimatebirdshot.final pages 16-19)

**Workforce development metrics**
- Collaboration breadth is described, but **no quantitative workforce metrics (students trained, hires, curricula, etc.) are reported** in the retrieved excerpts. (arroyave2024ultimatebirdshot.final pages 16-19)

### 2) DOE AMMTO DuAlumin‑3D (ORNL; Al alloy development for additive manufacturing)
**Quantitative metrics (technical and qualification-style testing)**
- Published work reports explicit AM processing parameters (e.g., LPBF on EOS M290: **370 W, 1300 mm/s, 0.19 mm hatch, 30 µm layer, 150 °C preheat**), a representative build (**104 mm diameter × 75 mm height**), heat treatment (**350 °C × 8 h**), and property test conditions (tensile RT–350 °C; high-cycle fatigue at **150/250/350 °C**, **R = −1**, **50 Hz**, **runout 10^7 cycles**). (plotkowski2025additivelymanufacturinghightemperature pages 8-12)

**Go/no-go and decision structure**
- The retrieved DuAlumin‑3D publication reads like a qualification-oriented test campaign description, but **does not state explicit go/no-go thresholds** (e.g., pass/fail allowables). (plotkowski2025additivelymanufacturinghightemperature pages 8-12)

**Throughput actually achieved**
- Build and specimen extraction are described, but **no explicit throughput rates (builds/week, specimens/day) are reported**. (plotkowski2025additivelymanufacturinghightemperature pages 8-12)

**AI/ML performance metrics**
- **Not reported** in retrieved sources. (plotkowski2025additivelymanufacturinghightemperature pages 8-12)

**Workforce metrics**
- **Not reported** in retrieved sources. (plotkowski2025additivelymanufacturinghightemperature pages 8-12)

### 3) DOE BES / NSF DMREF programs (materials discovery)
Because DMREF is an NSF program (not DOE BES), the evidence retrieved was (i) DMREF program-level reporting and (ii) a DMREF-funded project with explicit quantitative KPIs.

**Quantitative metrics (program-level)**
- Program scale metrics reported: **139 projects**, **528 PIs**, **$172 M total investment**, and **~75%** of projects attracting co-funding. (schlueter2018designingmaterialsand pages 2-4)

**Go/no-go / evaluation structure**
- The DMREF program description emphasizes evaluation criteria such as acceleration, integrated iterative collaboration, workforce training, and open access to outputs, but **does not publish a universal go/no-go metric gate** (in the retrieved document). (schlueter2018designingmaterialsand pages 2-4)

**Project-level KPI example (DMREF-funded AM feedstock project)**
- Explicit milestone/KPI structure: print **12 ASTM E8/E8M tensile specimens (6 XY, 6 Z)**; achieve **UTS coefficient of variation <3.5%**; **UTS >90% of commercial alloys**; and **no orientation UTS difference at 95% confidence**. (nuechterlein2021additivemanufacturingfeedstock pages 1-3)
- Achieved metrics were substantially better than targets: **>99.6% density**, defect-size upper bounds **~20–30 µm**, and CVs **0.33–0.94%** and **0.7–1.8%**; UTS of **123%** and **157%** of reference alloys. (nuechterlein2021additivemanufacturingfeedstock pages 1-3)

**Throughput and AI/ML metrics**
- DMREF program-level documents emphasize ML and data-driven approaches, but **do not provide quantitative AI/ML performance KPIs** in the retrieved excerpt. (schlueter2018designingmaterialsand pages 2-4)

**Workforce development metrics**
- DMREF program intent includes co-advising, exchanges, new courses, symposia, and outreach; **quantitative trainee counts were not found** in the retrieved documents. (schlueter2018designingmaterialsand pages 2-4, schlueter2018designingmaterialsand pages 1-2)

### 4) NSF CAREER awards in autonomous materials discovery
**Evidence gap note:** no CAREER award abstracts/reports (award IDs, milestone tables, education plans) were retrieved.

**Proxy: widely cited autonomous lab metrics structure used by NSF-adjacent community**
- A standardized SDL metrics structure proposes tracking: **degree of autonomy, operational lifetime, throughput, experimental precision, material usage, accessible parameter space, and optimization efficiency**. (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto pages 2-3)
- Example quantitative metrics (from surveyed SDL literature) include **700 samples** unassisted lifetime, **30–33 samples/hour** throughput, **0.06–0.2 mL/sample** material usage, and parameter-space magnitude **1.6×10^11**. (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto media 9bb86ea1)

**Workforce development metrics**
- Not CAREER-specific in retrieved sources; SDL perspective focuses on reporting standards rather than education-plan counting. (volk2024performancemetricsto pages 5-6)

### 5) DARPA DSO materials programs
**Evidence gap note:** DARPA DSO BAAs/performer reports with explicit milestone go/no-go gates were not retrieved in the current evidence set.

### 6) DOE TCR (Transformational Challenge Reactor) at ORNL — qualification metrics for AM nuclear components
**Quantitative metrics (qualification + ML-enabled QA)**
- TCR’s digital-thread qualification approach reports unusually explicit **dataset-scale and prediction-performance** metrics:
  - **6,299 tensile specimens** used to train property-prediction models and a **~230 GB public dataset** for co-registered in situ/ex situ data. (scime2023adatadrivenframework pages 1-2)
  - **~180 million pixel-wise annotations** used to train anomaly segmentation; spatial mapping to **1 mm “super-voxels”** (localized property prediction) after co-registration. (scime2023adatadrivenframework pages 3-5)
  - A reported **61% error reduction** in UTS predictions relative to estimates without in situ data. (scime2023adatadrivenframework pages 1-2)
  - A 2021 report describes a final GNN with **R² = 0.877**, **prediction uncertainty 31.9 MPa**, and **96.2% correct classification** against a **485 MPa** threshold across **687 test super-voxels**. (scime2021reportondiagnostic pages 44-47)

**Go/no-go and guardrails**
- Explicit “qualification gate” behavior for deployment: the model outputs **“cannot predict”** when feature vectors are dissimilar to training (an out-of-distribution guardrail). (scime2021reportondiagnostic pages 44-47, scime2020reportonprogress pages 31-36)

**Throughput actually achieved**
- The TCR campaign explicitly targeted thousands of specimens: FY21 tested **~3,000** SS‑J3 tensile samples (short of a 5,000 target) with Phase 2 planned for another **5,000**. (scime2021reportondiagnostic pages 44-47)

**Workforce development metrics**
- Not quantified in retrieved sources.

## Cross-program gaps vs. what FLAIME should benchmark against
Because FLAIME’s internal metric taxonomy was not available, these are framed as competitive “must-haves” for a closed-loop alloy-discovery program.

### Gaps likely in FLAIME if not already present
1) **Explicit, numeric go/no-go gates tied to program phases**
   - ARPA‑E ULTIMATE/BIRDSHOT uses milestone go/no-go downselects (e.g., identify 5–10 candidates) plus property constraints (strength, density, solidus, etc.). (arroyave2024ultimatebirdshot.final pages 5-7, arroyave2024ultimatebirdshot.final pages 14-16)
   - DMREF exemplar shows clear acceptance thresholds (CV <3.5%, orientation parity at 95% confidence). (nuechterlein2021additivemanufacturingfeedstock pages 1-3)

2) **Qualification-style “born qualified” metrics and OOD guardrails**
   - TCR demonstrates deployable gates: threshold classification (485 MPa) and “cannot predict” for OOD inputs. (scime2021reportondiagnostic pages 44-47)

3) **Dataset-scale and pedigree metrics** (for credibility, reuse, and downstream certification)
   - TCR reports dataset size (230 GB), annotation volume (~180M), and specimen counts (6,299). (scime2023adatadrivenframework pages 1-2, scime2023adatadrivenframework pages 3-5)

4) **Standardized throughput reporting (demonstrated vs theoretical)**
   - SDL metric frameworks emphasize reporting demonstrated/theoretical throughput and lifetime, not just total experiments. (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto pages 2-3)

5) **Quantitative workforce development outcomes**
   - Many program descriptions state workforce intent but often omit counts; competitive proposals benefit from explicit KPIs even when others do not. DMREF emphasizes training but does not report numbers in the retrieved excerpt. (schlueter2018designingmaterialsand pages 2-4)

### Strengths FLAIME could claim (if its Edison-mature framework includes these)
Relative to typical published program reporting, a mature metrics framework is already “more rigorous” if it includes:
- **End-to-end closed-loop latency + iteration rate** and “decision-quality” measures (optimization efficiency, trials-to-optimum) aligned with SDL best practice (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto pages 5-6)
- **Model reliability metrics beyond accuracy** (calibration, OOD detection, uncertainty-aware downselects) consistent with TCR guardrails and superconductors candidate-score thresholds (scime2021reportondiagnostic pages 44-47, pogue2023closedloopsuperconductingmaterials pages 5-6)
- **Explicit target-property envelopes tied to application readiness** as in ULTIMATE (strength/density/solidus/creep, etc.) rather than generic “discover a better alloy” objectives (arroyave2024ultimatebirdshot.final pages 14-16, sharon2023computationallyguidedodsrefractory pages 4-6)

## Top 5 recommended metric additions/modifications for FLAIME
These are the most competitively differentiating additions, anchored in the funded-program evidence above.

1) **DARPA/ARPA‑E style gated milestone metrics with numeric thresholds**
   - Implement Phase gates such as: “downselect to N candidates meeting all hard constraints” (ULTIMATE MS.3.2 model), and specify N and the constraints (e.g., high‑T yield, density ceiling, solidus floor, ductility). (arroyave2024ultimatebirdshot.final pages 5-7, arroyave2024ultimatebirdshot.final pages 14-16)

2) **Standardized throughput and latency accounting (demonstrated vs theoretical)**
   - Report: experiments/week, alloys/week, measurements/hour, and closed-loop cycle time (design→make→test→learn), separated into demonstrated and theoretical as recommended by SDL metrics frameworks. (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto pages 2-3)

3) **ML reliability and “safe autonomy” metrics (OOD + uncertainty)**
   - Include: (i) OOD detection rate and “cannot predict” fraction (TCR paradigm), (ii) calibration error / uncertainty quality, and (iii) threshold-classification metrics relevant to qualification decisions (e.g., >X MPa pass/fail with accuracy). (scime2021reportondiagnostic pages 44-47)

4) **Qualification-ready data pedigree metrics (digital thread completeness)**
   - Track and report: dataset size, sensor modalities, annotation counts (if applicable), and linkage completeness across composition/process/structure/property. TCR’s publication-quality reporting provides a competitive benchmark (6299 tensile, 230 GB, 180M annotations). (scime2023adatadrivenframework pages 1-2, scime2023adatadrivenframework pages 3-5)

5) **Workforce development KPIs with counts (not just narratives)**
   - Add explicit annual targets: #students/postdocs trained in autonomy+metallurgy, #cross-trained operators, #modules/courses delivered, #industry/DOE rotations, and #open datasets/tutorials released. DMREF articulates workforce intent but does not quantify outcomes in the retrieved program description; quantification would be a proposal differentiator. (schlueter2018designingmaterialsand pages 2-4)

## Program identifiers and citation notes
- ARPA‑E ULTIMATE: “ULTIMATE: BIRDSHOT. Final Technical Report” (OSTI/DOE identifier via DOI 10.2172/2305503) (arroyave2024ultimatebirdshot.final pages 16-19)
- DuAlumin‑3D: ORNL-designed Al alloy work with OSTI DOI 10.2172/2573209 (plotkowski2025additivelymanufacturinghightemperature pages 8-12)
- TCR digital qualification: OSTI/peer-reviewed outputs with DOIs 10.3390/ma16237293 and 10.2172/1831630 (scime2023adatadrivenframework pages 1-2, scime2021reportondiagnostic pages 44-47)
- SDL metrics framework: Nature Communications 2024, DOI 10.1038/s41467-024-45569-5 (volk2024performancemetricsto pages 1-2, volk2024performancemetricsto media 9bb86ea1)

## Practical next step for a higher-fidelity FLAIME-specific gap analysis
To make the gap/strength conclusions *fully* specific to FLAIME, the analysis needs the current FLAIME metrics framework (even a bullet list). Without it, the recommendations above should be treated as a competitive “checklist” against ULTIMATE/TCR/DMREF and SDL best-practice reporting, not a strict audit of FLAIME’s existing metrics.


References

1. (arroyave2024ultimatebirdshot.final pages 14-16): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

2. (arroyave2024ultimatebirdshot.final pages 11-14): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

3. (arroyave2024ultimatebirdshot.final pages 5-7): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

4. (arroyave2024ultimatebirdshot.final pages 16-19): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

5. (arroyave2024ultimatebirdshot.final pages 9-11): Raymundo Arroyave. Ultimate: birdshot. final technical report. ArXiv, Feb 2024. URL: https://doi.org/10.2172/2305503, doi:10.2172/2305503. This article has 4 citations.

6. (plotkowski2025additivelymanufacturinghightemperature pages 8-12): Alex Plotkowski, Jovid Rakhmonov, and Xavier Ferlet. Additively manufacturing high-temperature aluminum alloy for automotive engine pistons. ArXiv, Feb 2025. URL: https://doi.org/10.2172/2573209, doi:10.2172/2573209. This article has 0 citations.

7. (schlueter2018designingmaterialsand pages 2-4): John Schlueter. Designing materials and devices to revolutionize and engineer the future of electronics and photonics through computationally led and data-driven approaches. Micro- and Nanotechnology Sensors, Systems, and Applications X, 10639:10, May 2018. URL: https://doi.org/10.1117/12.2305496, doi:10.1117/12.2305496. This article has 2 citations.

8. (nuechterlein2021additivemanufacturingfeedstock pages 1-3): J Nuechterlein. Additive manufacturing feedstock designed for uniform printing of metallic builds. Unknown journal, 2021.

9. (schlueter2018designingmaterialsand pages 1-2): John Schlueter. Designing materials and devices to revolutionize and engineer the future of electronics and photonics through computationally led and data-driven approaches. Micro- and Nanotechnology Sensors, Systems, and Applications X, 10639:10, May 2018. URL: https://doi.org/10.1117/12.2305496, doi:10.1117/12.2305496. This article has 2 citations.

10. (volk2024performancemetricsto pages 1-2): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 79 citations and is from a highest quality peer-reviewed journal.

11. (volk2024performancemetricsto pages 2-3): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 79 citations and is from a highest quality peer-reviewed journal.

12. (pogue2023closedloopsuperconductingmaterials pages 1-2): Elizabeth A. Pogue, Alexander New, Kyle McElroy, Nam Q. Le, Michael J. Pekala, Ian McCue, Eddie Gienger, Janna Domenico, Elizabeth Hedrick, Tyrel M. McQueen, Brandon Wilfong, Christine D. Piatko, Christopher R. Ratto, Andrew Lennon, Christine Chung, Timothy Montalbano, Gregory Bassen, and Christopher D. Stiles. Closed-loop superconducting materials discovery. npj Computational Materials, 9:1-8, Oct 2023. URL: https://doi.org/10.1038/s41524-023-01131-3, doi:10.1038/s41524-023-01131-3. This article has 27 citations and is from a peer-reviewed journal.

13. (pogue2023closedloopsuperconductingmaterials pages 2-3): Elizabeth A. Pogue, Alexander New, Kyle McElroy, Nam Q. Le, Michael J. Pekala, Ian McCue, Eddie Gienger, Janna Domenico, Elizabeth Hedrick, Tyrel M. McQueen, Brandon Wilfong, Christine D. Piatko, Christopher R. Ratto, Andrew Lennon, Christine Chung, Timothy Montalbano, Gregory Bassen, and Christopher D. Stiles. Closed-loop superconducting materials discovery. npj Computational Materials, 9:1-8, Oct 2023. URL: https://doi.org/10.1038/s41524-023-01131-3, doi:10.1038/s41524-023-01131-3. This article has 27 citations and is from a peer-reviewed journal.

14. (pogue2023closedloopsuperconductingmaterials pages 5-6): Elizabeth A. Pogue, Alexander New, Kyle McElroy, Nam Q. Le, Michael J. Pekala, Ian McCue, Eddie Gienger, Janna Domenico, Elizabeth Hedrick, Tyrel M. McQueen, Brandon Wilfong, Christine D. Piatko, Christopher R. Ratto, Andrew Lennon, Christine Chung, Timothy Montalbano, Gregory Bassen, and Christopher D. Stiles. Closed-loop superconducting materials discovery. npj Computational Materials, 9:1-8, Oct 2023. URL: https://doi.org/10.1038/s41524-023-01131-3, doi:10.1038/s41524-023-01131-3. This article has 27 citations and is from a peer-reviewed journal.

15. (volk2024performancemetricsto pages 3-5): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 79 citations and is from a highest quality peer-reviewed journal.

16. (volk2024performancemetricsto pages 5-6): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 79 citations and is from a highest quality peer-reviewed journal.

17. (scime2023adatadrivenframework pages 1-2): Luke Scime, Chase Joslin, David A. Collins, Michael Sprayberry, Alka Singh, William Halsey, Ryan Duncan, Zackary Snow, Ryan Dehoff, and Vincent Paquit. A data-driven framework for direct local tensile property prediction of laser powder bed fusion parts. Materials, 16:7293, Nov 2023. URL: https://doi.org/10.3390/ma16237293, doi:10.3390/ma16237293. This article has 20 citations.

18. (scime2023adatadrivenframework pages 3-5): Luke Scime, Chase Joslin, David A. Collins, Michael Sprayberry, Alka Singh, William Halsey, Ryan Duncan, Zackary Snow, Ryan Dehoff, and Vincent Paquit. A data-driven framework for direct local tensile property prediction of laser powder bed fusion parts. Materials, 16:7293, Nov 2023. URL: https://doi.org/10.3390/ma16237293, doi:10.3390/ma16237293. This article has 20 citations.

19. (scime2021reportondiagnostic pages 44-47): Luke Scime, Michael Sprayberry, David Collins, Alka Singh, Chase Joslin, Ryan Duncan, Joseph Simpson, Fred List III, Keith Carver, Alex Huning, James Haley, and Vincent Paquit. Report on diagnostic and predictive capabilities of the tcr digital platform. ArXiv, Sep 2021. URL: https://doi.org/10.2172/1831630, doi:10.2172/1831630. This article has 5 citations.

20. (scime2020reportonprogress pages 31-36): Luke Scime, J. Haley, William Halsey, Ashutosh Kumar Singh, Michael Sprayberry, Amir K. Ziabari, and V. Paquit. Report on progress of correlation of in-situ and ex-situ data and the use of artificial intelligence to predict defects. ArXiv, Oct 2020. URL: https://doi.org/10.2172/1684671, doi:10.2172/1684671. This article has 7 citations.

21. (scime2023adatadrivenframework pages 2-3): Luke Scime, Chase Joslin, David A. Collins, Michael Sprayberry, Alka Singh, William Halsey, Ryan Duncan, Zackary Snow, Ryan Dehoff, and Vincent Paquit. A data-driven framework for direct local tensile property prediction of laser powder bed fusion parts. Materials, 16:7293, Nov 2023. URL: https://doi.org/10.3390/ma16237293, doi:10.3390/ma16237293. This article has 20 citations.

22. (scime2020reportonprogress pages 27-31): Luke Scime, J. Haley, William Halsey, Ashutosh Kumar Singh, Michael Sprayberry, Amir K. Ziabari, and V. Paquit. Report on progress of correlation of in-situ and ex-situ data and the use of artificial intelligence to predict defects. ArXiv, Oct 2020. URL: https://doi.org/10.2172/1684671, doi:10.2172/1684671. This article has 7 citations.

23. (sharon2023computationallyguidedodsrefractory pages 4-6): John Sharon, Anthony Ventura, Ryan Deacon, Ken Smith, and Soumalya Sarkar. Computationally-guided ods refractory heas via additive manufacturing. ArXiv, Oct 2023. URL: https://doi.org/10.2172/2375527, doi:10.2172/2375527. This article has 0 citations.

24. (volk2024performancemetricsto media 9bb86ea1): Amanda A. Volk and Milad Abolhasani. Performance metrics to unleash the power of self-driving labs in chemistry and materials science. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45569-5, doi:10.1038/s41467-024-45569-5. This article has 79 citations and is from a highest quality peer-reviewed journal.