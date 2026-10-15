# Alloy Databases for AI-Guided Design Campaigns (Topic 3B — Critical Minerals)

Comprehensive survey of databases relevant to the FLAIME Genesis Mission proposal targeting **DOE Topic 3B: "AI-Enabled Materials Discovery and Engineering" (AMMTO)** under "Securing America's Critical Minerals Supply." Emphasis on aluminum and magnesium alloys and materials criticality data sources for supply-risk-aware alloy optimization.

**Partnership context:** Letters of collaboration from Valimet (gas atomization), AMAZEMET (ultrasonic atomization — atomizer installed at BYU), and Thermo-Calc (CALPHAD/AM Module — simulations already running on BYU HPC). Letters of support from Ames National Lab, Fehrmann Alloys, Taylor Sparks (University of Utah), Ashley Speer, Adam Clare, Chris Stiles, Jae Hattrick-Simpers, and Keith Brown.

**Preliminary results available:** AMAZEMET atomizer installed, AlSi10Mg tensile specimens (University of Utah + 3D Powder Tech), tensile data, SEM/EDS of precursor powders and atomized mixture, high-temperature tensile data, Thermo-Calc AM Module simulations (provided by TC), BYU HPC CALPHAD runs, full pKGFN pipeline implementation, and automated powder dispensing demonstration.

Informed by Edison Scientific (PaperQA3 LITERATURE_HIGH) research — full outputs in [edison-trajectories/alloy_databases_overview.md](edison-trajectories/alloy_databases_overview.md), [edison-trajectories/al_mg_databases.md](edison-trajectories/al_mg_databases.md), and [edison-trajectories/materials_criticality_databases.md](edison-trajectories/materials_criticality_databases.md).

## Quick-Reference Summary

| Database | Alloy Families | Key Data Types | Access Model | BYU/UUtah Access | ML Suitability | Programmatic Access |
| :--- | :--- | :--- | :--- | :--- | :---: | :---: |
| **Knovel (Elsevier)** | Broad (Al, Mg, Ti, Ni, steels, Cu) | Handbook data: mechanical, thermal, corrosion | Proprietary (subscription) | ✅ U of Utah has access | Low–Moderate | Excel export; no API |
| **Total Materia** | All metallic (350K+ materials) | Composition, mechanical, physical, standards cross-refs | Proprietary (subscription) | ❓ Check institutional access | Moderate | Web portal; some export |
| **ASM Alloy Center** | Metals (Al, Mg, Ti, Ni, Cu, steels) | Phase diagrams, mechanical, corrosion, micrographs | Proprietary (subscription) | ❓ Check institutional access | Moderate | Web; some export |
| **Granta/ANSYS EduPack** | Broad (metals, polymers, ceramics) | Mechanical, thermal, electrical, fatigue, Ashby charts | Proprietary / Educational | ❓ BYU had 10 licenses (Eric Homer, 2020); checking reactivation with Ansys | Moderate | Desktop; limited export |
| **MMPDS/MDHB** | Aerospace metals (Al, Ti, Ni, steels, some Mg) | Design allowables: tensile, fatigue, creep, fracture toughness | Proprietary (subscription) | ❓ Check institutional access | Low | PDF/printed; no API |
| **MatWeb** | Broad (100K+ materials) | Mechanical, thermal, physical datasheets | Free (web) | ✅ Open | Moderate | Web; no bulk download |
| **MatNavi/NIMS** | Metals, polymers, ceramics | Mechanical, creep, fatigue, thermal | Free (registration) | ✅ Open | Moderate | Web platform |
| **Materials Project** | Inorganic compounds (incl. metallic) | DFT: formation energies, elastic constants, phase diagrams | Open (API) | ✅ Open | **High** | REST API, pymatgen |
| **AFLOW/AFLOWLIB** | Inorganic (3.5M entries, HEAs) | DFT: formation energies, elastic, thermal, electronic | Open (GNU) | ✅ Open | **Very High** | REST API, AFLOW-ML |
| **OQMD** | Inorganic compounds & alloys | DFT: formation energies, convex hulls | Open | ✅ Open | **High** | Bulk download |
| **NOMAD** | Computational materials (raw DFT) | Raw DFT inputs/outputs | Open | ✅ Open | **High** | API |
| **JARVIS (NIST)** | Broad inorganic | DFT, elastic, optical, ML force fields | Open | ✅ Open | **High** | API |
| **Thermo-Calc (CALPHAD)** | TCAL, TCMG, TCFE, TCNI, TCTI, TCCU, TCHEA | Phase diagrams, solidification, diffusion, AM Module | **Collaboration partner** (Genesis Mission) | ✅ Active (BYU HPC) | **Very High** | TC-Python API |
| **Pandat (CompuTherm)** | Al, Mg, Ni, Ti, Fe, Cu, HEA | Phase diagrams, solidification, Scheil | Proprietary (commercial) | ❓ Check academic license | Moderate | Batch mode |
| **JMatPro** | Al, Ti, steels, Ni, Mg, Co, Zr | Phase stability, mechanical, TTT/CCT | Proprietary (commercial) | ❓ Check academic license | Moderate | Batch mode |
| **ULTERA** | High-entropy alloys, refractory HEAs | Composition, mechanical, phase data | Research / Open | ✅ Open | **Very High** | Research access |
| **Materials Commons** | Structural alloys (emphasis Mg) | Experimental process–structure–property | Open | ✅ Open | Moderate | FAIR data |
| **SpringerMaterials** | Broad (Landolt-Börnstein) | Crystal structures, phase diagrams, properties | Proprietary (subscription) | ❓ Check institutional access | Moderate | Web |
| **CINDAS** | High-performance metals | Thermal, electrical, mechanical vs temperature | Proprietary (institutional) | ❓ Check institutional access | Moderate | Database platform |
| **Aluminum Association** | Al wrought (1xxx–8xxx), cast | Composition limits, typical properties | Proprietary (purchase) | ❓ Purchase required | Low | PDF/standards |
| | | | | | | |
| **— Materials Criticality —** | | | | | | |
| **USGS Mineral Commodity Summaries** | 80+ mineral commodities | Production, reserves, trade, prices, import reliance | Open (government) | ✅ Open | **High** (after ETL) | Annual PDF/tables; bulk download |
| **DOE Critical Materials Assessment** | Energy-sector critical materials | Criticality matrices (supply risk × importance), short/medium-term | Open (government) | ✅ Open | **High** | PDF report; structured tables |
| **EU JRC RMIS** | ~100 raw materials | Supply risk, economic importance, recycling, governance | Open (government) | ✅ Open | Moderate | Web dashboards; PDF factsheets |
| **UN Comtrade** | All traded commodities | Bilateral trade flows by HS code | Open (API) | ✅ Open | **Very High** | REST API |
| **World Bank WGI** | 200+ countries | Governance indicators (6 dimensions, annual) | Open | ✅ Open | **Very High** | Downloadable CSV; API |
| **ESSENZ (TU Berlin)** | ~40 abiotic resources | Supply-risk characterization factors (11 categories) | Open (academic) | ✅ Open | **High** | Published CFs at TU Berlin website |
| **Ferro & Bonollo CIA Dataset** | Metallic alloys (CRM perspective) | Alloy Criticality Index, Ashby-style maps | Open (Mendeley) | ✅ Open | **High** | Excel on Mendeley Data |
| **Helbig et al. Superalloy SR** | Ni-based superalloys | Elemental supply risk (12 indicators), alloy-level aggregation | Open (supplementary) | ✅ Open | **High** | Supplementary spreadsheets |
| **Mulukutla SupplyRiskAwareDesign** | HEAs (MoNbTiVW) | Elemental supply risk + Batch BO for alloy optimization | Open (GitHub) | ✅ Open | **Very High** | GitHub repo with code + data |
| **Matminer** | Broad inorganic/materials | Data retrieval + 47 featurization classes for ML | Open (Python) | ✅ Open | **Very High** | Python package; API wrappers |
| **USGS Critical Minerals Atlas** | Critical minerals | Geospatial production, reserves, trade data | Open (GIS) | ✅ Open | Moderate | ArcGIS REST API; CSV/GeoJSON |
| **Kaggle Supply Risk Index** | USGS-derived | Critical minerals supply risk indices | Open (Kaggle) | ✅ Open | **High** | CSV download; Kaggle API |
| **BGS Supply Risk Index** | 40+ elements | 7-criteria supply risk score (1–10 scale) | Open | ✅ Open | **High** | PDF reports; data tables |

## 1. Aluminum Alloy Databases (Priority)

### 1.1 Knovel (Elsevier)

- **Coverage**: Digitized handbooks covering wrought (1xxx–8xxx) and cast aluminum alloys
- **Properties**: Mechanical (YS, UTS, elongation, hardness), thermal (conductivity, expansion), corrosion data — varies by source handbook
- **Data type**: Experimental
- **Access**: Proprietary subscription; **University of Utah has access**
- **Format**: Interactive tables, Excel export for individual datasets; no bulk API
- **ML suitability**: Low–Moderate — document-oriented format requires manual extraction for large-scale ML use (green2017fulfillingthepromise pages 17-18)
- **Notes**: Good starting point for looking up individual alloy properties; less suited for automated dataset construction

### 1.2 Total Materia (formerly PolyPlus / Key to Metals)

- **Coverage**: 350,000+ metallic materials from 75+ countries, including comprehensive Al alloy coverage
- **Properties**: Composition, mechanical properties, physical properties, cross-referenced international standards
- **Data type**: Experimental
- **Access**: Proprietary subscription
- **Format**: Web portal with some export capability; no bulk download API
- **ML suitability**: Moderate — massive coverage but licensing restricts bulk extraction (wang2024datadriveninnovationsin pages 66-68)
- **Notes**: One of the most comprehensive commercial alloy databases; valuable for finding international equivalents and standards cross-references

### 1.3 MMPDS / MDHB (Metallic Materials Properties Development and Standardization)

- **Coverage**: Aerospace aluminum alloys (wrought/cast, 1xxx–8xxx series), some magnesium alloys
- **Properties**: Design allowables — room/elevated-temperature tensile (YS, UTS, elongation), compression, shear, bearing, fracture toughness, fatigue (S-N), fatigue crack growth (da/dN-ΔK), creep/creep-rupture, stress–strain, elastic moduli
- **Data type**: Experimental (statistically analyzed A-basis and B-basis allowables)
- **Access**: Proprietary subscription (Battelle Memorial Institute)
- **Format**: PDF/printed tables; no programmatic access
- **ML suitability**: Low — gold standard for validated engineering properties but non-machine-readable (gavert2018criticalsurveysof pages 16-18, jackson2007definitionofdesign pages 5-13)

### 1.4 Thermo-Calc TCAL Database ⭐ (Collaboration Partner)

- **Coverage**: Multi-component Al alloy systems
- **Properties**: Phase equilibria, Scheil solidification (solidification range, fraction solid vs temperature), precipitation kinetics via TC-PRISMA, AM Module for additive manufacturing process simulation
- **Data type**: Computational (CALPHAD)
- **Access**: **Collaboration partner** — Thermo-Calc providing letter of collaboration for Genesis Mission. AM Module simulations already provided by Thermo-Calc; additional CALPHAD runs already executed on BYU HPC clusters.
- **Format**: **TC-Python API** enables high-throughput batch calculation — ideal for generating physics-based features across candidate compositions
- **ML suitability**: **Very High** — programmatic access to physics-based features (phase fractions, driving forces, solidification paths) that improve model accuracy (cote2020ontheelemental pages 8-10, vary2023highthroughputstudyof pages 66-68)
- **Status**: Active — TC AM Module simulations completed, BYU HPC CALPHAD screening underway for Al-Zr and Al-Mn-Cr-Zr systems (Topic 3B target alloys)

### 1.5 JMatPro — Aluminum Database

- **Coverage**: Multi-component Al alloy systems
- **Properties**: Phase stability, YS, UTS, thermal/electrical conductivity, elastic moduli, density, thermal expansion, TTT/CCT diagrams, Scheil solidification
- **Data type**: Computational (CALPHAD + property models)
- **Access**: Proprietary commercial license
- **Format**: Batch mode available
- **ML suitability**: Moderate — generates engineering-relevant properties directly from composition; fewer user inputs required (chinella2011computationalthermodynamicscharacterization pages 16-19, cote2020ontheelemental pages 4-6)

### 1.6 Open Research Datasets — Aluminum

**AlSi10Mg Process-Structure-Property Dataset (Luo et al. 2024)**
- 60 LPBF processing parameter combinations
- Properties: Vickers hardness, YS, UTS, elongation, elastic modulus; porosity, pore morphology, grain/cell features from XCT/EBSD/SEM
- Format: Zenodo, Excel + raw data files
- Access: **Open** — CC license
- ML suitability: **High** (luo2024datasetofprocessstructureproperty pages 1-3)

**AlloyML / DoS Dataset (Mangos & Birbilis)**
- Al-Mg (5xxx) alloys: 516 DoS entries + 1,154 mechanical property entries (YS, UTS, elongation)
- Sources: CES EduPack, MatWeb, Matminer, literature
- Format: Excel, GitHub repo (AlloyML)
- Access: **Open**
- ML suitability: **High** (mangos2105aluminiumalloydesign pages 3-7)

**LPBF Relative Density Dataset (Barrionuevo et al. 2025)**
- 1,579 samples from 85 papers; 6 alloys including AlSi10Mg
- Features: 10 processing parameters → relative density
- Format: Excel on Harvard Dataverse; code on GitHub
- Access: **Open**
- ML suitability: **High** (barrionuevo2025laserpowderbed pages 3-4)

### 1.7 Aluminum Association (Teal Sheets)

- **Coverage**: Official composition limits for all registered wrought (1xxx–8xxx) and cast Al alloys
- **Properties**: Composition ranges, typical mechanical properties
- **Data type**: Standards-based
- **Access**: Proprietary (purchase required)
- **Format**: PDF/printed; no programmatic access
- **ML suitability**: Low — requires manual digitization (gavert2018criticalsurveysof pages 16-18)

## 2. Magnesium Alloy Databases (Priority)

### 2.1 Materials Commons (materialscommons.org)

- **Coverage**: Structural alloys with **particular emphasis on magnesium alloys**
- **Properties**: Experimental process–structure–property data, microstructural data
- **Data type**: Experimental
- **Access**: **Open** (FAIR data principles)
- **Format**: Upload/download/publish workflow; structured data
- **ML suitability**: Moderate — FAIR experimental data with microstructure linkage (ramakrishna2019materialsinformatics pages 4-5)
- **Notes**: Developed at University of Michigan; particularly relevant for Mg alloy design

### 2.2 Multi-Component Mg CALPHAD Database (Xu et al. 2016)

- **Coverage**: 23-component system (Mg–Ag–Al–Ca–Ce–Cu–Fe–Gd–K–La–Li–Mn–Na–Nd–Ni–Pr–Si–Sn–Sr–Th–Y–Zn–Zr); 145 binary and 48 ternary sub-systems
- **Properties**: Phase equilibria, solidification paths (Scheil), heat-treatment windows
- **Validated on**: AZ91/AZ91D, AM50A, AM60B, AE42, AE44, AS21, AS31 — covers AZ, AM, AE, AS series and can model ZK, WE, Elektron-type RE-containing alloys
- **Data type**: Computational (CALPHAD)
- **Access**: Published literature — parameters usable with CALPHAD software
- **ML suitability**: Moderate — enables generating thermodynamic features for Mg alloy ML models (xu2016thermodynamicdatabaseof pages 13-15)

### 2.3 Thermo-Calc TCMG Database ⭐ (Collaboration Partner)

- **Coverage**: Multi-component Mg alloy systems
- **Properties**: Phase equilibria, solidification, diffusion
- **Data type**: Computational (CALPHAD)
- **Access**: **Collaboration partner** — same license as TCAL (see Section 1.4)
- **Format**: TC-Python API for batch calculations
- **ML suitability**: **Very High** — same programmatic advantages as TCAL

### 2.4 JMatPro / Pandat — Magnesium Databases

- **Coverage**: Mg alloy systems (JMatPro Mg database; Pandat PanMg database)
- **Properties**: Phase stability, mechanical properties, thermophysical, TTT/CCT, Scheil
- **Data type**: Computational (CALPHAD + property models)
- **Access**: Proprietary commercial license
- **Format**: Batch mode available
- **ML suitability**: Moderate (cote2020ontheelemental pages 8-10)

### 2.5 Knovel / ASM / Total Materia — Magnesium Coverage

All three proprietary platforms include magnesium alloy coverage (AZ, AM, ZK, WE, Elektron families):
- **Knovel**: Handbook-based Mg alloy properties (University of Utah access confirmed)
- **ASM Alloy Center**: Mg compositions, phase diagrams, corrosion data
- **Total Materia**: Mg standards cross-references and properties

## 3. Broad Alloy Family Databases

### 3.1 Open-Access Computational Repositories

| Database | Entries | Key Strengths | API |
| :--- | :--- | :--- | :--- |
| **Materials Project** | 150K+ inorganics | pymatgen library; phase diagram app; convex hulls | REST API |
| **AFLOW/AFLOWLIB** | 3.5M materials, 700M+ properties | AFLOW-ML API; standardized descriptors; HEA support | REST + AFLUX Search |
| **OQMD** | 100K+ compounds | Formation energies; Heusler/perovskite focus | Bulk download |
| **NOMAD** | Millions of calculations | Raw DFT data; reproducibility focus; ML challenges | API |
| **JARVIS (NIST)** | Broad inorganics | Integrated ML models; force fields | API |

These repositories primarily cover crystalline inorganic compounds via DFT calculations. While not alloy-engineering-property databases, they provide foundational thermodynamic stability, elastic, and electronic data for alloy screening and feature engineering (jain2016researchupdatethe pages 4-5, oses2018datadrivendesignof pages 3-5).

### 3.2 CALPHAD Software Suites

| Software | Databases | Alloy Families | License |
| :--- | :--- | :--- | :--- |
| **Thermo-Calc** | TCFE, TCAL, TCMG, TCNI, TCTI, TCCU, TCHEA (26 elements, v1-7) | Steels, Al, Mg, Ni, Ti, Cu, HEAs | **Collaboration partner** (Genesis Mission) |
| **Pandat** | PanFe, PanAl, PanMg, PanNi, PanTi | Fe, Al, Mg, Ni, Ti, Cu, HEA, solder | Commercial |
| **JMatPro** | Internal databases | Al, Ti, steels, Ni, Mg, Co, Zr, solder | Commercial |
| **pycalphad** (open-source) | Uses TDB files | Any system with available TDB | MIT |
| **OpenCalphad** (open-source) | Uses TDB files | Any system with available TDB | GNU GPL |
| **TDBDB** (Thermodynamic Database Database) | Index of published TDB files | Various | Open |

CALPHAD tools are critical for generating physics-based features (phase fractions, solidification ranges, driving forces) that significantly improve model accuracy beyond composition-only descriptors. For Topic 3B, Thermo-Calc is a collaboration partner — AM Module simulations have already been provided, and CALPHAD screening for Al-Zr and Al-Mn-Cr-Zr systems (critical-mineral-lean alternatives) is running on BYU HPC (vary2023highthroughputstudyof pages 66-68, durodola2022machinelearningfor pages 14-15).

### 3.3 Commercial Property Databases

| Database | Focus | Key Strengths | Access |
| :--- | :--- | :--- | :--- |
| **ASM International** | Metals & alloys | Phase Diagram Center; Alloy Center; Micrograph Center; failure analysis | Subscription |
| **Granta/ANSYS** | All materials | Ashby charts; EduPack for teaching; MI for enterprise; MMPDS add-on | Commercial / Edu (BYU: 10 licenses from 2020, checking reactivation with Ansys) |
| **Total Materia** | All metallic alloys | 350K+ materials; 75+ countries; standards cross-references | Subscription |
| **Knovel** | Engineering reference | Digitized handbooks; interactive tables | Subscription |
| **SpringerMaterials** | Broad (Landolt-Börnstein) | Crystal structures; phase diagrams; curated reference data | Subscription |
| **CINDAS** | High-performance metals | Thermal/electrical/mechanical properties vs temperature | Institutional |
| **MMPDS/MDHB** | Aerospace metals | Gold-standard design allowables (A/B-basis) | Subscription |
| **Aluminum Association** | Al alloys | Official composition limits for all registered alloys | Purchase |

### 3.4 Specialized Databases

**ULTERA (ultera.org)** — High-Entropy Alloys
- Largest curated HEA mechanical property dataset
- Open research access; specifically designed for ML-driven HEA discovery (hart2021machinelearningfor pages 22-22)

**Alloys-by-Design (ABD)** — Ni-Based Superalloys
- Industrial platform (Rolls-Royce origin) for screening millions of Ni superalloy compositions
- Integrates CALPHAD with creep, oxidation, phase stability models (rahman2025reviewmachinelearning pages 25-26)
- Access: Industrial partners only

### 3.5 Open Research Datasets (ML-Ready)

| Dataset | Alloys | Properties | Size | Format | Source |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **FatigueData-CMA2022** (Zhang 2023) | Complex metallic alloys | S-N, ε-N, da/dN-ΔK; YS, UTS, elong. | 272 datasets from 1,249 articles | MAT, JSON, Excel (CC BY 4.0) | Figshare + GitHub |
| **LPBF Relative Density** (Barrionuevo 2025) | 316L, IN718, Ti6Al4V, CuCrZr, AlSi10Mg, 18Ni300 | Relative density; 10 process params | 1,579 samples, 85 papers | Excel | Harvard Dataverse + GitHub |
| **AlSi10Mg PSP** (Luo 2024) | LPBF AlSi10Mg | Hardness, YS, UTS, elong., E; porosity, microstructure | 60 parameter sets | Excel + raw files | Zenodo |
| **AlloyML DoS** (Mangos & Birbilis) | Al-Mg (5xxx) | DoS (ASTM G67), YS, UTS, elong. | 516 + 1,154 entries | Excel | GitHub (AlloyML) |

These open datasets are the most immediately useful for training models — clean, structured, machine-readable, with explicit features and targets (zhang2023fatiguedatabaseof pages 1-2, barrionuevo2025laserpowderbed pages 3-4).

## 3A. Materials Criticality Databases (Topic 3B Alignment)

With the shift to DOE Genesis Mission Topic 3B ("AI-Enabled Materials Discovery and Engineering" under "Securing America's Critical Minerals Supply"), databases for materials criticality assessment are central to the proposal. FLAIME's closed-loop platform (pKGFN pipeline — already implemented) integrates a mineral-burden objective node M(x) = Σ(wt%_i × CF_i) that requires element-level supply risk characterization factors from these sources. Collaboration partners Valimet (gas atomization), AMAZEMET (ultrasonic atomization — atomizer installed at BYU), and Thermo-Calc (CALPHAD/AM Module) provide the experimental and computational infrastructure; the criticality databases below provide the supply-risk data layer.

### 3A.1 Government & Institutional Sources

#### USGS Mineral Commodity Summaries (MCS)
- **Coverage**: Annual commodity tables for 80+ mineral commodities
- **Properties**: Production, reserves, net import reliance, trade, prices, market context
- **Data type**: Statistical/economic
- **Access**: **Open** (government publication, annual updates)
- **Format**: PDF tables; some CSV via [USGS Critical Minerals Atlas](https://apps.usgs.gov/critical-minerals/critical-minerals-atlas.html) (ArcGIS REST API, GeoJSON)
- **ML suitability**: High after ETL — strong authority, annual cadence, but requires extraction from PDF/tables for consistent panel datasets (helbig2021anoverviewof pages 18-20, nassar2025methodologyandtechnical pages 9-10)
- **Notes**: Primary production dataset used in virtually all criticality methods. Also see [Kaggle: Critical Minerals Supply Risk Index](https://www.kaggle.com/datasets/philipdave/critical-minerals-supply-risk-index) for a pre-processed ML-ready version

#### DOE 2023 Critical Materials Strategy (CMS)
- **Coverage**: Energy-sector critical materials (short-term and medium-term assessments)
- **Properties**: Criticality matrices (supply risk × importance to clean energy), critical/near-critical classifications
- **Data type**: Assessment/policy
- **Access**: **Open** (DOE publication, [DOI: 10.2172/1998242](https://doi.org/10.2172/1998242))
- **Format**: PDF with structured tables
- **ML suitability**: High — provides the authoritative DOE criticality classifications; short-term critical: Co, Dy, Ga, graphite, Ir, Nd, Tb; near-critical: Li, U, electrical steel, Ni, **Mg**, SiC (bauer20232023criticalmaterials pages 16-18, 133-136)
- **Notes**: Mg is DOE near-critical (short-term) → critical (medium-term). Key policy basis for Topic 3B framing

#### EU JRC Raw Materials Information System (RMIS)
- **Coverage**: ~100 raw material profiles with 20+ indicators per material
- **Properties**: Reserves, production, EU trade, recycling, governance, supply risk, economic importance
- **Data type**: Assessment/dashboard
- **Access**: **Open** — [RMIS Portal](https://rmis.jrc.ec.europa.eu/critical-and-strategic-materials); also [SCRREEN3 CRM Factsheets](https://scrreen.eu/crms-2023/)
- **Format**: Web dashboards, PDF factsheets; some downloadable data. Full assessment report: [EU CRM 2023 Study (PDF)](https://ec.europa.eu/newsroom/cipr/items/787007/en)
- **ML suitability**: Moderate — rich data but primarily dashboard-oriented; requires extraction for ML use (manfredi2024rawmaterialsinformation pages 1-2)
- **Notes**: 2023 EU CRM list: 34 critical raw materials + new "strategic raw materials" category

#### British Geological Survey (BGS) Supply Risk Index
- **Coverage**: 40+ elements
- **Properties**: 7-criteria supply risk score (1–10 scale): production concentration, reserve distribution, recycling rate, substitutability, governance
- **Data type**: Risk assessment
- **Access**: **Open** (BGS reports)
- **ML suitability**: High — numeric, standardized per-element scores ready for direct use as ML features (bachmann2022d1.4critical pages 121-124)

#### UN Comtrade
- **Coverage**: All internationally traded commodities
- **Properties**: Bilateral trade flows by HS code, used for import-share and trade-dependency features
- **Data type**: Trade statistics
- **Access**: **Open** (API) — [comtradeplus.un.org](https://comtradeplus.un.org/)
- **ML suitability**: Very High — structured, API-accessible, excellent for graph/time-series models of supply chain risk (cimprich2019rawmaterialcriticality pages 3-5)

#### World Bank Worldwide Governance Indicators (WGI)
- **Coverage**: 200+ countries, 6 governance dimensions, annual
- **Properties**: Political stability, government effectiveness, regulatory quality, rule of law, control of corruption, voice and accountability
- **Data type**: Governance metrics
- **Access**: **Open** — [info.worldbank.org/governance/wgi](https://info.worldbank.org/governance/wgi/)
- **ML suitability**: Very High — numeric, country-level, annual, with documented uncertainty intervals; core input to GeoPolRisk, ESSENZ, Yale/Graedel methods (graedel2012methodologyofmetal pages 53-57, cimprich2019rawmaterialcriticality pages 2-3)

### 3A.2 Criticality Characterization Factor Methods & Datasets

#### ESSENZ (TU Berlin)
- **Coverage**: ~40 abiotic resources across 11 supply-risk categories
- **Properties**: Characterization factors for political stability, demand growth, mining capacity, trade barriers, production/reserve concentration, company concentration, co-production, price volatility, exploration feasibility
- **Data type**: Characterization factors
- **Access**: **Open** — published at [TU Berlin ESSENZ page](https://www.see.tu-berlin.de/menue/forschung/ergebnisse/essenz/parameter/en/) (bach2019analyzingchangesin pages 1-3)
- **ML suitability**: High — numeric per-element factors; directly usable as ML features or BO objective inputs
- **Notes**: Supersedes the earlier ESP method. Uses USGS, World Bank WGI, WEF, and SNL data

#### Yale/Graedel Criticality Methodology
- **Coverage**: Individual metals in 3D criticality space
- **Properties**: Supply risk, vulnerability to supply restriction, environmental implications; uses HHI, WGI-PV, PPI, HDI, Net Import Reliance, GII
- **Data type**: Methodology + published per-element assessments
- **Access**: **Open** (published papers and supplementary materials) — Graedel et al. 2012, *Environmental Science & Technology* (786 citations)
- **ML suitability**: High — foundational framework; Monte Carlo uncertainty quantification included (graedel2012methodologyofmetal pages 23-26, 53-57)

#### GeoPolRisk
- **Coverage**: Region-specific supply risk for mineral commodities
- **Properties**: Geopolitical supply risk characterization factors using WGI political stability weighted by import shares
- **Data type**: Characterization factors
- **Access**: **Open** (academic publications) (cimprich2019rawmaterialcriticality pages 3-5)
- **ML suitability**: High — accounts for domestic production as "risk-free"; has endpoint extension (GeoPolEndpoint) modeling socio-economic damage

### 3A.3 Alloy-Level Criticality Indices

#### Ferro & Bonollo Alloy Criticality Index (CIA)
- **Coverage**: Metallic alloys from a critical raw materials perspective
- **Properties**: Per-element CICRM scores aggregated by composition to alloy-level CIA; Ashby-style criticality-performance material selection charts
- **Data type**: Index methodology + dataset
- **Access**: **Open** — dataset on [Mendeley Data](https://data.mendeley.com/datasets/4vtrtxgxzm/1); paper in *Materials & Design* (134 citations)
- **Format**: Excel files with criticality indicators, material maps, worked examples
- **ML suitability**: High — provides formula and data for computing alloy-level criticality from composition (ferro2019materialsselectionin pages 3-4, 8-9)
- **Notes**: Uses EU CRM factsheet data. Directly applicable to Ashby-style screening with criticality as an axis. Extended in Ferro & Bonollo 2020 (alloy substitution) and 2023 (lightweight design vs. criticality)

#### Helbig et al. Alloy-Level Supply Risk for Ni-Based Superalloys
- **Coverage**: 12 alloying elements in Ni-based superalloys
- **Properties**: 12 supply risk indicators across 4 categories (supply reduction, demand increase, market concentration, political risk); 4 alloy-level aggregation methods
- **Data type**: Supplementary datasets
- **Access**: **Open** (supplementary spreadsheets in *Resources* journal, 25 citations)
- **Format**: Excel with alloy compositions, element prices, computed supply risk values
- **ML suitability**: High — structured numeric data; demonstrates that aggregation method choice (arithmetic mean vs. cost-share weighting) significantly affects rankings (helbig2020supplyriskconsiderations pages 9-12)
- **Notes**: Cost-share aggregation reveals Re as dominant driver of supply risk in single-crystal superalloys

#### Mulukutla et al. SupplyRiskAwareDesign
- **Coverage**: HEAs (demonstrated on MoNbTiVW system)
- **Properties**: Elemental supply risk indicators (auto-extracted via LLM pipeline from USGS data), integrated into multi-objective Batch Bayesian Optimization
- **Data type**: Code + data repository
- **Access**: **Open** — [GitHub: mrinalinimulukutla/SupplyRiskAwareDesign](https://github.com/mrinalinimulukutla/SupplyRiskAwareDesign)
- **Format**: Tables S1–S4 (Elemental Info, Calculation Detail, HHIL Calculation, Element Price History) + Python code
- **ML suitability**: **Very High** — most directly relevant ML-ready resource for supply-risk-aware alloy design; LLM-based extraction pipeline + MOBO framework (mulukutla2024supplyriskawarealloy pages 6-8, 16-18, 18-20)
- **Notes**: Closest direct precedent for criticality-aware alloy BO. Supply risk indicators configurable via JSON. Pareto-optimal HEAs balancing performance with minimized supply risk

### 3A.4 Materials Informatics Tools (Sparks/Baird)

#### Matminer
- **Coverage**: Broad inorganic/materials data retrieval + featurization
- **Properties**: 47 featurization classes; API interfaces to Materials Project, MDF, and other databases
- **Data type**: Python toolkit
- **Access**: **Open** — [hackingmaterials/matminer](https://github.com/hackingmaterials/matminer) (1,152 citations)
- **ML suitability**: **Very High** — standardized pandas DataFrames, scikit-learn compatible; essential infrastructure for composition-to-property models (ward2018matmineranopen pages 1-3)

#### Matbench
- **Coverage**: 13 benchmark ML tasks (312 to 132,752 samples)
- **Properties**: Optical, thermal, electronic, thermodynamic, tensile, elastic properties
- **Data type**: Benchmark datasets
- **Access**: **Open** — [materialsproject/matbench](https://github.com/materialsproject/matbench) (450 citations)
- **ML suitability**: **Very High** — standardized benchmarks for materials property prediction (dunn2020benchmarkingmaterialsproperty pages 2-3)

#### Mohanty, Sayeed & Sparks (2025) — Global Mineral Commodities Analysis
- **Coverage**: USGS mineral commodity data
- **Properties**: Analysis, visualization, and intelligent assistance tools for mineral commodity data exploration
- **Data type**: Tool/analysis
- **Access**: Published in *PRX Energy* (2025)
- **ML suitability**: High — directly relevant for mineral criticality data exploration and feature engineering
- **Notes**: From Taylor Sparks' group at University of Utah — directly relevant to PI's network

### 3A.5 Meta-Review & Emerging Resources

#### Helbig et al. (2021) Meta-Review of 88 Criticality Methods
- **Coverage**: Systematic review of 88 criticality assessment methods (through 2020)
- **Properties**: 618 individual applications of supply risk criteria, 98 unique criteria in 10 indicator categories
- **Access**: **Open** (supplementary spreadsheets in *Resources* journal, 50 citations)
- **ML suitability**: High — structured meta-dataset valuable for ontology building and automated indicator selection (helbig2021anoverviewof pages 2-4)

#### Andrieu et al. (2025) — Global Database of Critical Mineral Lists
- **Coverage**: 206 jurisdictions worldwide
- **Properties**: Cross-country comparison of critical mineral designations
- **Data type**: Database (preprint stage)
- **Access**: Preprint (LLM-assisted discovery of national CRM lists)
- **ML suitability**: Moderate — emerging resource for policy-aware criticality modeling
- **Notes**: Built with LLM-assisted discovery; useful for understanding how criticality designations vary by country

### 3A.6 Key Insight for Topic 3B

No single, centralized, ML-ready criticality dataset exists that combines all relevant indicators across all elements in a standardized, versioned, API-accessible format. The field remains fragmented across government reports (often PDF-first), academic supplementary materials, and proprietary databases. The most promising foundations for FLAIME's supply-risk-aware alloy optimization pipeline (pKGFN — already implemented) are:

1. **Mulukutla et al. SupplyRiskAwareDesign** — open code + data, LLM extraction pipeline, MOBO integration (closest precedent)
2. **Ferro & Bonollo CIA** — open dataset, alloy-level criticality formula, Ashby-style screening
3. **USGS MCS + Kaggle preprocessed data** — authoritative production/reserves data (9 critical mineral CSVs already downloaded)
4. **ESSENZ CFs** — standardized numeric characterization factors for ~40 resources
5. **Matminer** — infrastructure for featurization and data retrieval (already installed, generating Magpie features)

For FLAIME's BOFN, a critical-mineral-burden objective node M(x) = Σ(wt%_i × CF_i) can be computed deterministically from alloy composition using any of these characterization factor sources, making it a "cheap" node in the DAG that requires no experimental evaluation. This integrates directly with the full pKGFN pipeline (already implemented) and Thermo-Calc CALPHAD screening (already running on BYU HPC for Al-Zr and Al-Mn-Cr-Zr systems).

## 4. Access and Cost Summary

### Open Access (Free)

| Resource | Best For |
| :--- | :--- |
| Materials Project, AFLOW, OQMD, NOMAD, JARVIS | DFT-computed thermodynamic/elastic properties |
| MatWeb | Quick property lookup for common alloys |
| MatNavi/NIMS | Creep and fatigue data for metals |
| Materials Commons | Experimental Mg alloy process-structure-property data |
| ULTERA | HEA composition-property data |
| TDBDB | Finding published CALPHAD TDB parameter sets |
| pycalphad / OpenCalphad | CALPHAD calculations with available TDB files |
| FatigueData-CMA2022, Barrionuevo LPBF, Luo AlSi10Mg, AlloyML | ML-ready curated datasets |
| USGS MCS, DOE CMS, EU JRC RMIS, BGS, UN Comtrade, WGI | Materials criticality & supply risk data |
| ESSENZ CFs, GeoPolRisk, Yale/Graedel | Elemental criticality characterization factors |
| Ferro & Bonollo CIA, Helbig et al. SR, Mulukutla SupplyRiskAwareDesign | Alloy-level criticality indices & supply-risk-aware optimization |
| Matminer, Matbench | Materials informatics infrastructure & ML benchmarks |

### Educational / University Access

| Resource | Notes |
| :--- | :--- |
| **Knovel** | ✅ U of Utah confirmed access; check BYU |
| **Granta EduPack** | Widely available via educational site licenses |
| **SpringerMaterials** | Via institutional library subscriptions |
| **CINDAS** | Via institutional subscriptions |

### Proprietary (Commercial License Required)

| Resource | Approx. Cost | Notes |
| :--- | :--- | :--- |
| Thermo-Calc + databases (TCAL, TCMG, etc.) | ~$5K–15K/yr academic | **Collaboration partner** — letter of collaboration; AM Module provided; BYU HPC active |
| JMatPro | ~$5K–10K/yr | Fast engineering property predictions |
| Pandat | ~$5K–10K/yr | Strong Al/Mg databases |
| Total Materia | ~$2K–5K/yr | Massive commercial alloy coverage |
| ASM International | ~$1K–5K/yr | Phase diagrams, micrographs, failure analysis |
| MMPDS | ~$1K–3K/yr | Aerospace design allowables (gold standard) |

## 5. Recommendations for BYU VCL (Topic 3B — Genesis Mission)

### Immediate Actions (Free / Low Cost)
1. ✅ **Open ML-ready datasets downloaded** — FatigueData-CMA2022, Barrionuevo LPBF, Luo AlSi10Mg PSP, AlloyML (all in `database-samples/`)
2. **Register for MatNavi/NIMS** — free registration, valuable creep/fatigue data
3. **Use Materials Project / AFLOW APIs** — set up pymatgen and AFLOW-ML for thermodynamic screening
4. **Explore Materials Commons** — particularly for Mg alloy experimental data
5. **Access ULTERA** — for any HEA design campaigns
6. ✅ **pycalphad + TDBDB** — open-source CALPHAD with published TDB files (samples downloaded)
7. ✅ **Mulukutla SupplyRiskAwareDesign repo cloned** — open code + elemental supply risk data for criticality-aware BO (directly relevant to Topic 3B mineral-burden objective)
8. ✅ **Ferro & Bonollo CIA dataset** — Mendeley Data Excel files for alloy-level criticality computation (identified, browser download needed)
9. ✅ **USGS MCS data downloaded** — 9 critical mineral CSVs via ScienceBase API (Al, Zr, Cr, Mn, Be, Co, Ga, Sc, REE)
10. ✅ **Matminer installed** — composition featurization generating 132 Magpie features per alloy (samples in `database-samples/criticality/`)

### Check University Access
1. **Verify BYU Knovel access** — University of Utah confirmed; BYU library may also subscribe
2. **Verify Granta EduPack** — BYU has existing licenses via Eric Homer (2020); checking reactivation status with Ansys account manager
3. **Check ASM International / SpringerMaterials** — via library subscriptions; BYU may already have ASM access (some data accessible on home network)

### Active — Collaboration Partner (Thermo-Calc)
1. ✅ **Thermo-Calc AM Module simulations** — provided by Thermo-Calc (collaboration partner, letter of collaboration)
2. ✅ **BYU HPC CALPHAD runs** — Thermo-Calc simulations running on BYU HPC for Al-Zr and Al-Mn-Cr-Zr screening (Topic 3B target alloys)
3. **TC-Python batch screening** — high-throughput CALPHAD feature generation for pKGFN pipeline integration

### Active — Experimental Infrastructure
1. ✅ **Valimet gas atomization** — collaboration partner (letter of collaboration) for gas-atomized powder feedstock
2. ✅ **AMAZEMET ultrasonic atomizer installed** at BYU (collaboration partner, letter of collaboration)
3. ✅ **AlSi10Mg tensile specimens** — printed at University of Utah (Taylor Sparks, letter of support) and 3D Powder Tech
4. ✅ **Tensile data collected** — stress–strain, YS/UTS/elongation for printed specimens
5. ✅ **SEM/EDS** — precursor powders (AlSi10Mg, Si) and AMAZEMET atomized mixture (composition change from Al wire + Si addition)
6. ✅ **High-temperature tensile data** — standard aluminum specimen
7. ✅ **Full pKGFN pipeline implemented** — BOFN with mineral-burden objective node ready for Topic 3B closed-loop optimization
8. ✅ **Automated powder dispensing demonstration** — proof-of-concept for Topic 3B closed-loop workflow

### Strategic Acquisitions (Budget Dependent)
1. **Total Materia** — if broad commercial alloy property lookup is needed (single-user academic ~€1,330/yr)
2. **ASM Alloy Center** — $1,950/yr academic; may already be accessible via BYU library

### Key Insight
The most effective alloy design pipelines for Topic 3B combine:
- **Open DFT databases** (Materials Project, AFLOW) → thermodynamic stability screening
- **CALPHAD tools** (Thermo-Calc — collaboration partner, pycalphad) → physics-based features (phase fractions, solidification range)
- **Experimental databases** (curated datasets, ASM, MMPDS) → target properties (strength, fatigue, corrosion)
- **Criticality data** (USGS MCS, ESSENZ CFs, Ferro & Bonollo CIA) → supply risk objectives for multi-objective optimization
- **pKGFN pipeline** (already implemented) → sequential optimization with mineral-burden objective as cheap DAG node

Data scarcity, heterogeneous reporting, and the lack of standardized benchmarks remain key challenges, but the FLAIME closed-loop approach — combining Thermo-Calc CALPHAD screening with experimental validation (AMAZEMET atomizer, LPBF printing, tensile testing) and supply-risk-aware BOFN — is designed to overcome these limitations through active learning (rahman2025reviewmachinelearning pages 1-3, rahman2025reviewmachinelearning pages 10-12).

## 6. Access Verification & Sample Data

Programmatic access was tested for all databases. Small data subsets were downloaded where possible. See [database-samples/](database-samples/) for the actual files and [database-samples/README.md](database-samples/README.md) for full details.

### ✅ Successfully Accessed & Downloaded

| Database | Method | Sample Data | Key Finding |
| :--- | :--- | :--- | :--- |
| **AFLOW/AFLOWLIB** | REST API (no key) | Al, Mg, Al-Mg binary alloys (10 entries each) | Fully open; AFLUX search API works well; returns compound, space group, formation enthalpy |
| **OQMD** | REST API (no key) | Al, Mg, Al-Mg compounds (10 entries each) | Fully open; returns entry ID, composition, formation energy, stability, band gap |
| **NOMAD** | POST query API (no key) | Al compounds (10 entries) | Fully open; returns entry ID, chemical formula, structural type |
| **JARVIS (NIST)** | Python package (`jarvis-tools`) | Al, Mg compounds (10 entries each from 76K-entry dataset) | Auto-downloads full dataset from Figshare; returns JID, formula, formation energy, elastic moduli, density |
| **FatigueData-CMA2022** | Figshare direct download | Full dataset (762 KB Excel, CC BY 4.0) | 272 fatigue datasets from 1,249 articles; immediately ML-ready |
| **Barrionuevo LPBF** | Harvard Dataverse download | Full dataset (222 KB Excel) | 1,579 samples, 6 alloys, 10 processing parameters → relative density |
| **HCF AlSi10Mg/316L** | Zenodo download | Full dataset (22 KB Excel) | High-cycle fatigue compilation for SLM alloys |
| **AlloyML** (Mangos & Birbilis) | GitHub download | Input templates (CSV) | Training data (516+1,154 entries) not in repo; referenced from Dropbox in paper |
| **pycalphad** | Python package (built-in TDBs) | Al-Mg, Cu-Mg, Al-Co-Cr-Ni HEA phase info | 35 test TDB files ship with pycalphad; open-source CALPHAD calculations |
| **ULTERA** | GitHub (PhasesResearchLab) | Contribution template + example | Template shows HEA data schema; actual database requires contacting PhasesResearchLab |

### ❌ Not Accessible (Require Credentials or Blocked)

| Database | Status | What's Needed |
| :--- | :--- | :--- |
| **Materials Project** | API key required (401) | Free registration at materialsproject.org → API key |
| **MatWeb** | Blocks automated access (403) | Manual web browser only; no bulk download |
| **MatNavi/NIMS** | Network blocked from sandbox | Free registration at mits.nims.go.jp |
| **Materials Commons** | API endpoints changed (404) | Web UI browsing works from normal browser |
| **Knovel** | Login required | University of Utah institutional subscription |
| **Total Materia** | Login required | Proprietary subscription |
| **ASM International** | Login required | Proprietary subscription |
| **SpringerMaterials** | No public API (404) | Institutional library subscription |
| **MMPDS / Granta / Thermo-Calc / JMatPro / Pandat** | Commercial software | Requires purchased license |

### ✅ Criticality Databases — Successfully Accessed & Downloaded

| Database | Method | Sample Data | Key Finding |
| :--- | :--- | :--- | :--- |
| **USGS MCS 2025** | ScienceBase REST API | 10 critical mineral CSVs (Al, Zr, Cr, Mn, Be, Co, Ga, Sc, REE) | Full salient data zip (171 files, 400 KB); authoritative US production/trade/price data 2020–2024 |
| **Mulukutla SupplyRiskAwareDesign** | GitHub raw content | Supply risk scores, elemental properties, config JSON | Closest precedent for criticality-aware alloy BO; includes LLM extraction pipeline + MOBO code |
| **Matminer** (v0.10.0) | Python package (`pip install matminer`) | Elastic tensor Al (20 entries), glass binary Al (20), steel strength (10), Magpie features (7 alloys × 132 features) | 45 total built-in datasets available; `ElementProperty.from_preset('magpie')` generates 132 composition features per alloy |
| **EU JRC RMIS** | Web page loads | HTML page only | Portal accessible but data is in interactive dashboards and PDF factsheets; no public REST API |
| **Kaggle Supply Risk Index** | Web page loads | Page accessible (9.7 KB) | Bulk download requires Kaggle API key (free registration) |

### ❌ Criticality Databases — Not Accessible from Sandbox

| Database | Status | What's Needed |
| :--- | :--- | :--- |
| **DOE 2023 Critical Materials Strategy** | energy.gov blocked from sandbox | Open government PDF — accessible from browser |
| **BGS Supply Risk Index** | Site restructured; risk list URLs return 404 | Open — risk list published as PDF/web tables at bgs.ac.uk |
| **UN Comtrade** | API v1 requires authentication (401) | Free API key registration at comtradeplus.un.org |
| **World Bank WGI** | API indicator codes changed/archived | Open — direct CSV download at info.worldbank.org/governance/wgi |
| **ESSENZ (TU Berlin)** | Page loads but CFs are in published papers | Open academic publications |
| **GeoPolRisk / Yale-Graedel** | Data in published supplementary materials | Open academic publications |
| **Ferro & Bonollo CIA** | Mendeley Data search doesn't resolve correct dataset | Open — Mendeley Data, needs DOI-based browser lookup |
| **Helbig et al. Superalloy SR** | Supplementary in journal paper | Open academic supplementary |

All criticality samples are in [database-samples/criticality/](database-samples/criticality/) with reproduction steps.

## 7. Vendor Contacts for Official Quotes

For obtaining official pricing quotes for the licensed/proprietary databases. Each entry includes a brief use-case description that can be shared with the vendor when requesting a quote.

### Thermo-Calc — Thermo-Calc Software AB ⭐ (Collaboration Partner)
- **Contact:** Web form — [Request Quotation](https://thermocalc.com/request-a-quotation/) or [Sales Team](https://thermocalc.com/contact-us/sales-team/)
- **Status:** **Letter of collaboration** for Genesis Mission Topic 3B. AM Module simulations already provided; BYU HPC CALPHAD runs active. Eric Homer (same department — BYU Mechanical Engineering) also has a Thermo-Calc license.
- **Ask for:** Academic license with TCAL (aluminum) and TCMG (magnesium) databases; optionally TCHEA (high-entropy alloys). TC-Python API access. Also ask about the [free educational package](https://thermocalc.com/academia/free-educational-package/).
- **Use case:** We are conducting alloy design research at BYU targeting DOE Genesis Mission Topic 3B (Critical Minerals). We need Thermo-Calc with TC-Python to run CALPHAD phase diagram and solidification calculations (equilibrium, Scheil) for aluminum and magnesium alloy systems, with focus on critical-mineral-lean compositions (Al-Zr, Al-Mn-Cr-Zr). We would use TC-Python to programmatically compute thermodynamic properties (phase fractions, solidification ranges, driving forces) across candidate compositions as part of a closed-loop alloy optimization platform.

### JMatPro — Sente Software Ltd
- **Contact:** Web form — [Get a Quote](https://www.sentesoftware.co.uk/get-a-quote) or [Contact / Reps](https://www.sentesoftware.co.uk/Contact)
- **Ask for:** Academic license with Al and Mg alloy modules. Batch/scripting capability.
- **Use case:** We need JMatPro to predict engineering-level mechanical properties (yield strength, UTS, hardness), TTT/CCT diagrams, and physical properties for aluminum and magnesium alloys as part of an alloy design research program at BYU targeting critical-mineral-lean alloy compositions. We would use its batch mode to generate property predictions across candidate compositions.

### Pandat — CompuTherm LLC
- **Contact:** info@computherm.com or [computherm.com/contact-us](https://computherm.com/contact-us/)
- **Ask for:** Academic license with PanAluminum and PanMagnesium databases. Batch calculation capability.
- **Use case:** We need Pandat for CALPHAD-based phase equilibrium and solidification calculations for aluminum and magnesium alloy design at BYU, with focus on critical-mineral-lean compositions for DOE-funded research. We would use it to compute phase diagrams, liquidus/solidus temperatures, and Scheil solidification paths across candidate compositions.

### Total Materia — Key to Metals AG
- **Contact:** Web form — [Contact Us](https://www.totalmateria.com/en-us/contact-us/) or [Order Now](https://www.totalmateria.com/en-us/order-now/). Option to "Speak with a Specialist."
- **Ask for:** Academic subscription for a small research group.
- **Use case:** We need Total Materia to look up and cross-reference mechanical properties, compositions, and international standards equivalents for aluminum and magnesium alloys at BYU. We need access to property data (tensile strength, yield strength, elongation, hardness) across alloy variants to support our alloy design research targeting critical-mineral-lean compositions.

### ASM International — ASM International
- **Contact:** onlineDBsales@asminternational.org · +1-440-338-5151 · [Alloy Center](https://www.asminternational.org/wkcl-shop/online-databases/single-user-asm-alloy-center-database/)
- **Ask for:** Academic pricing for ASM Alloy Center Database. Single-user starts at ~$475/yr (member) or ~$525/yr (non-member).
- **Use case:** We need the ASM Alloy Center for phase diagram data, mechanical property datasheets, and corrosion data for aluminum and magnesium alloys at BYU. We need access to curated experimental data across alloy families to support our alloy design research targeting critical-mineral-lean compositions.

### MMPDS — Battelle Memorial Institute
- **Contact:** SCALF@battelle.org or bcommpds@battelle.org · +1-614-424-6557 · [Purchase Handbook](https://www.mmpds.org/purchase-handbook/)
- **Ask for:** Academic subscription or handbook access. Note: Battelle asks students/academics to contact them before registering.
- **Use case:** We need MMPDS for statistically validated design allowables (A-basis, B-basis) for aerospace aluminum alloys at BYU — specifically tensile, fatigue S-N, fatigue crack growth, and fracture toughness data. We need high-confidence experimental data as ground truth for validating computational predictions in our alloy design research targeting critical-mineral-lean aerospace alloys.

### Knovel — Elsevier
- **Contact:** Elsevier account manager · US: +1-888-615-4500 · [Knovel Support](https://www.elsevier.support/knovel/contact)
- **Ask for:** Access for BYU. Confirm whether BYU already subscribes through the library (University of Utah has confirmed access). Ask about the metals/materials engineering collection.
- **Use case:** We need Knovel for digitized handbook data on aluminum and magnesium alloy properties (mechanical, thermal, corrosion) at BYU. We need access to engineering handbook property data to support our alloy design research targeting critical-mineral-lean compositions.

### Granta EduPack — ANSYS Inc
- **Contact:** academic@ansys.com · [Academic Contact](https://www.ansys.com/academic/contact)
- **Ask for:** Academic research license. BYU has 10 licenses purchased by Eric Homer in 2020 — checking reactivation status with the Ansys account manager and BYU IT. Free student editions may also be available.
- **Use case:** We need Granta EduPack for its curated materials property database and Ashby-style screening at BYU. We would use it for initial materials selection and to access structured property data (mechanical, thermal, fatigue) across metal alloy families for alloy design research targeting critical-mineral-lean compositions.

### SpringerMaterials — Springer Nature
- **Contact:** Web form — [Licensing](https://www.springernature.com/gp/librarians/licensing/agc/databases) or [Support](https://support.springernature.com/en/support/solutions/articles/6000206179-contact-customer-support). Contact your local Springer Nature rep.
- **Ask for:** Academic subscription. Check if BYU library already has access.
- **Use case:** We need SpringerMaterials (Landolt-Börnstein) for crystal structure data, binary/ternary phase diagrams, and thermophysical properties for aluminum and magnesium alloy systems at BYU. This data would support CALPHAD validation and computational modeling in our alloy design research targeting critical-mineral-lean compositions.

### CINDAS — CINDAS LLC
- **Contact:** [Web form](https://cindasdata.com/support/contact) · +1-765-807-5400 (ask for pricing)
- **Ask for:** Academic subscription for the Aerospace Structural Metals Database (ASMD) or Thermophysical Properties of Matter Database (TPMD).
- **Use case:** We need CINDAS for temperature-dependent thermophysical and mechanical property data for high-performance aluminum and magnesium alloys at BYU. We need thermal conductivity, specific heat, and emissivity data as a function of temperature to support additive manufacturing process simulation in our alloy design research targeting critical-mineral-lean compositions.
