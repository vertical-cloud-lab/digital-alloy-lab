Question: What are the major publicly available and proprietary databases for alloy properties and compositions? Include databases for aluminum alloys, magnesium alloys, titanium alloys, nickel-based superalloys, steel/iron alloys, copper alloys, and high-entropy alloys. For each database, describe: (1) what alloy families it covers, (2) what types of data are available (composition, mechanical properties, thermodynamic data, phase diagrams, microstructure, processing parameters, fatigue, corrosion, etc.), (3) whether it is open-access, proprietary, or has educational/university access, (4) the URL or how to access it, and (5) its relevance for AI/machine-learning-guided alloy design campaigns. Include databases like Knovel, MatWeb, NIST, Citrine Informatics, AFLOW, Materials Project, CALPHAD databases (TCFE, TCAL, TCMG, TCNI, etc.), ASM International, Granta/ANSYS, JMatPro, PolyPlus/Total Materia, MPIE databases, and any others relevant to computational alloy design.

# Major Databases for Alloy Properties and Compositions: A Comprehensive Survey for Computational Alloy Design

## 1. Introduction

The landscape of materials databases for alloy design encompasses open-access computational repositories, proprietary commercial platforms, CALPHAD thermodynamic databases, and curated experimental collections. These resources vary widely in their alloy-family coverage, data types, access models, and suitability for AI/machine-learning (ML) workflows. Below, we provide a detailed description of each major database category, followed by a summary table.

| Database Name | Alloy Families Covered | Data Types | Access Model | URL / Access Point | ML/AI Relevance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Materials Project** | All inorganic materials, including alloys | DFT-computed energies, band structures, elastic constants, phase diagrams, convex hulls | Open Access (API & Web) | [materialsproject.org](https://materialsproject.org) | **High**; Extensive REST API (pymatgen), widely used for training ML potentials and stability models (jain2016researchupdatethe pages 4-5, ramakrishna2019materialsinformatics pages 4-5) |
| **AFLOW (AFLOWLIB)** | All inorganic materials, HEAs, metallic glasses | Formation energies, electronic structure, elastic constants, thermal properties, disorder models | Open Access (GNU License) | [aflow.org](http://aflow.org) | **Very High**; AFLOW-ML API, standardized descriptors for high-throughput screening (toher2019automatedcomputationof pages 12-13, oses2018datadrivendesignof pages 3-5) |
| **OQMD** | All inorganic compounds & alloys | DFT formation energies, crystal structures, convex hulls, thermodynamic stability | Open Access | [oqmd.org](http://oqmd.org) | **High**; Large datasets available for bulk download; focus on Heuslers and perovskites (jain2016researchupdatethe pages 4-5, jain2016researchupdatethe pages 11-13) |
| **NOMAD** | All computational materials | Raw DFT calculation inputs/outputs (VASP, CASTEP, etc.) | Open Access | [nomad-lab.eu](https://nomad-lab.eu) | **High**; Focus on reproducibility and raw data for training ML force fields; hosts ML competitions (ramakrishna2019materialsinformatics pages 4-5, hart2021machinelearningfor pages 22-22) |
| **Thermo-Calc (CALPHAD)** | Steels (TCFE), Al (TCAL), Mg (TCMG), Ni (TCNI), Ti (TCTI), Cu (TCCU), HEAs (TCHEA) | Thermodynamic data, phase diagrams, solidification paths, diffusion mobility | Proprietary (Commercial License) | [thermocalc.com](https://thermocalc.com) | **Very High**; TC-Python/TC-Toolbox enable batch calculations for generating physics-based features for ML (vary2023highthroughputstudyof pages 66-68) |
| **Pandat (CompuTherm)** | Al, Mg, Ni, Ti, Fe, Cu, HEA, solder alloys | Phase diagrams, thermodynamic properties, solidification simulation | Proprietary (Commercial License) | [computherm.com](https://computherm.com) | **Moderate**; Batch calculation capabilities for generating phase feature data (walle2018thethermodynamicdatabase pages 5-6) |
| **JMatPro** | Al, Ti, Steels, Ni superalloys, Mg, Co, Zr, Solder | Phase stability, mechanical properties, thermophysical properties, TTT/CCT diagrams | Proprietary (Commercial License) | [sentesoftware.co.uk](https://sentesoftware.co.uk) | **Moderate**; Fast property prediction models useful for generating synthetic training data (cote2020ontheelemental pages 3-4, cote2020ontheelemental pages 4-6) |
| **MatWeb** | All engineering alloys (metals, polymers, ceramics) | Composition, mechanical properties (yield, tensile), physical properties | Free (Searchable Web) | [matweb.com](http://matweb.com) | **Moderate**; Large dataset, but often requires scraping/manual extraction; data is unstructured (green2017fulfillingthepromise pages 12-13, ramakrishna2019materialsinformatics pages 4-5) |
| **ASM International** | Metals & Alloys (Steels, Al, Ti, Ni, Cu, Mg) | Phase diagrams, mechanical properties, corrosion data, micrographs, failure analysis | Proprietary (Subscription) | [asminternational.org](https://asminternational.org) | **Moderate**; Comprehensive, high-quality experimental data, but access is often restricted/non-API (green2017fulfillingthepromise pages 12-13) |
| **Granta / ANSYS** | All material classes (Metals, Polymers, Composites) | Mechanical, thermal, electrical, optical, environmental properties, Ashby charts | Proprietary (Commercial/Edu Licenses) | [ansys.com](https://ansys.com/products/materials) | **Moderate**; Highly curated property data; integration with FEA; "Synthesizer" tool for estimation (mercier2602acuratedliterature pages 3-5, mercier2602acuratedliterature pages 15-19) |
| **Total Materia** | All metallic alloys (>350,000 materials) | Composition, mechanical/physical properties, cross-referenced standards | Proprietary (Subscription) | [totalmateria.com](https://totalmateria.com) | **Moderate**; Massive coverage of commercial alloys and standards; valuable for finding equivalents (toher2019automatedcomputationof pages 12-13) |
| **Knovel (Elsevier)** | Broad engineering materials | Handbooks, technical references, property data tables | Proprietary (Subscription) | [knovel.com](https://knovel.com) | **Low-Moderate**; Reference data often in document format, less optimized for bulk ML extraction (green2017fulfillingthepromise pages 17-18) |
| **SpringerMaterials** | Broad materials (Landolt-Börnstein) | Crystal structures, phase diagrams, physical/chemical properties | Proprietary (Subscription) | [materials.springer.com](https://materials.springer.com) | **Moderate**; Curated high-quality reference data, mainly for lookup/validation (green2017fulfillingthepromise pages 17-18) |
| **NIST Materials Data** | Metals, alloys, general materials | Thermophysical properties, phase diagrams, SRDs (Standard Reference Data) | Open / Partially Open | [nist.gov/mml](https://nist.gov/mml) | **Moderate**; High-quality reference data; specific repositories (e.g., JARVIS) are ML-ready (green2017fulfillingthepromise pages 11-12) |
| **NIMS MatNavi** | Metals, polymers, ceramics | Mechanical properties (creep, fatigue), electronic/thermal properties | Open / Partially Open | [mits.nims.go.jp](https://mits.nims.go.jp) | **Moderate**; Valuable experimental datasets (e.g., creep, fatigue) for specific alloy classes (walle2018thethermodynamicdatabase pages 5-6, green2017fulfillingthepromise pages 17-18) |
| **Citrine Informatics** | Broad materials including alloys | Structure-property-process data; AI-driven platform | Proprietary Platform | [citrine.io](https://citrine.io) | **Very High**; Platform built specifically for ML/AI; includes Citrination (open) and proprietary tools (green2017fulfillingthepromise pages 12-13, ling2018machinelearningfor pages 1-2) |
| **ULTERA** | High-entropy alloys, refractory HEAs | Composition, mechanical properties, phase data | Research / Open | [ultera.org](http://ultera.org) | **Very High**; Largest curated dataset specifically for HEA mechanical properties and ML (hart2021machinelearningfor pages 22-22) |
| **Alloys-by-Design (ABD)** | Ni-based superalloys | Composition, phase stability, mechanical properties, creep | Proprietary (Industrial) | N/A (Internal/Service) | **High**; Industrial tool demonstrating computational screening of millions of compositions (rahman2025reviewmachinelearning pages 25-26) |
| **JARVIS (NIST)** | Broad inorganic materials | DFT properties, elastic, optical, solar efficiency, ML force fields | Open Access | [jarvis.nist.gov](https://jarvis.nist.gov) | **High**; Integration of classical force-fields and ML models; standardized data (yuan2024applicationsofmachine pages 16-17) |
| **Materials Commons** | Metals and alloys (Mg, structural) | Experimental process-structure-property data | Open Access | [materialscommons.org](https://materialscommons.org) | **Moderate**; Focus on FAIR experimental data and microstructure linkage (toher2019automatedcomputationof pages 12-13, ramakrishna2019materialsinformatics pages 4-5) |


*Table: A summary of key alloy databases categorizing their coverage, data types, access models, and relevance to machine learning workflows. The table spans computational repositories (e.g., Materials Project, AFLOW), commercial tools (e.g., Thermo-Calc, JMatPro), and experimental libraries (e.g., MatWeb, Total Materia).*

## 2. Open-Access Computational Repositories

### 2.1 Materials Project (materialsproject.org)
The Materials Project, hosted at Lawrence Berkeley National Laboratory, is one of the largest open-access ab initio materials databases, with over 150,000 inorganic materials. It provides DFT-computed formation energies, electronic band structures, elastic constants, piezoelectric tensors, and convex-hull phase diagrams (jain2016researchupdatethe pages 4-5, ramakrishna2019materialsinformatics pages 4-5). Data are accessible through a comprehensive REST API and the pymatgen Python library, making it highly amenable to ML workflows. The Phase Diagram App enables interactive thermodynamic stability analyses. While it primarily covers crystalline inorganic compounds rather than alloy-specific engineering properties, its thermodynamic stability data serve as foundational inputs for alloy screening and feature engineering in ML models (jain2016researchupdatethe pages 10-11).

### 2.2 AFLOW / AFLOWLIB (aflow.org)
AFLOW (Automatic FLOW for Materials Discovery) is a distributed repository of ab initio computed materials properties containing data for approximately 3.5 million materials entries with over 700 million calculated properties (toher2019automatedcomputationof pages 12-13, oses2018datadrivendesignof pages 3-5). The database stores formation energies, electronic structures (band structure, density of states), elastic constants, and thermal properties computed via Debye–Grüneisen modules. AFLOW provides a dedicated AFLOW-ML API that accepts structural data and returns JSON-formatted property predictions, enabling seamless integration into materials-design pipelines (toher2019automatedcomputationof pages 13-14). The software is distributed under the GNU license, and data are programmatically accessible via REST-APIs and the AFLUX Search-API (oses2018autonomousdatadrivendesign pages 3-5). AFLOW has been extensively used for predicting phase stability in high-entropy alloys, glass-forming ability, and training gradient-boosting and neural-network models for property prediction with validation metrics exceeding 90% accuracy (oses2018autonomousdatadrivendesign pages 2-3, oses2018datadrivendesignof pages 2-3).

### 2.3 Open Quantum Materials Database (OQMD, oqmd.org)
OQMD, centered at Northwestern University, contains comprehensive DFT calculations for hundreds of thousands of inorganic compounds, with a particular focus on popular structure types such as Heusler and perovskite compounds (jain2016researchupdatethe pages 4-5). It provides formation energies, relaxed crystal structures, and convex-hull stability data that are used for phase-diagram construction and new-compound discovery. OQMD data have been used extensively for thermodynamic screening in alloy design, including applications to high-entropy alloys and intermetallic discovery (jain2016researchupdatethe pages 11-13, hart2021machinelearningfor pages 22-22).

### 2.4 NOMAD (nomad-lab.eu)
The Novel Materials Discovery (NOMAD) repository is a European open-data infrastructure that archives raw DFT calculation inputs and outputs from multiple electronic-structure codes (ramakrishna2019materialsinformatics pages 4-5). NOMAD emphasizes reproducibility and verification of computational results and has hosted ML challenges (e.g., the NOMAD 2018 Kaggle competition) to benchmark data-driven approaches in materials science (hart2021machinelearningfor pages 22-22). Its raw-data orientation makes it particularly valuable for training ML interatomic potentials and validating computational workflows.

### 2.5 JARVIS (jarvis.nist.gov)
JARVIS (Joint Automated Repository for Various Integrated Simulations), maintained by NIST, provides DFT-derived properties including elastic constants, optical properties, solar efficiency metrics, and ML-ready datasets with integrated classical force-field and ML models (yuan2024applicationsofmachine pages 16-17). It is open-access and designed to support data-driven materials design.

### 2.6 Materials Commons (materialscommons.org)
Materials Commons, developed at the University of Michigan, is an open-access repository focused on experimental process–structure–property data for structural alloys, with particular emphasis on magnesium alloys (ramakrishna2019materialsinformatics pages 4-5). It follows FAIR data principles and supports uploading, sharing, and publishing experimental datasets including microstructural and mechanical property data.

## 3. CALPHAD Thermodynamic Databases

### 3.1 Thermo-Calc Software and Databases
Thermo-Calc is the most widely used commercial CALPHAD software platform, offering over 30 databases targeted to specific alloy families (vary2023highthroughputstudyof pages 66-68). Key databases include:
- **TCFE** (steels and iron-based alloys): Phase equilibria, solidification, and property data for Fe-based systems with comprehensive descriptions of carbide, nitride, and intermetallic phases.
- **TCAL** (aluminum alloys): Thermodynamic descriptions for Al alloys including precipitation sequences.
- **TCMG** (magnesium alloys): Phase equilibria for Mg-based systems.
- **TCNI** (nickel-based superalloys): Phase stability data for Ni-base superalloys including gamma/gamma-prime equilibria (walle2018thethermodynamicdatabase pages 5-6).
- **TCTI** (titanium alloys): Phase diagrams for Ti-based systems.
- **TCCU** (copper alloys): Thermodynamic data for Cu-based alloy systems.
- **TCHEA** (high-entropy alloys): Multi-component thermodynamic descriptions for HEAs covering up to 26 elements across multiple versions (TCHEA1 through TCHEA7) (vary2023highthroughputstudyof pages 66-68).

Each database is distributed as TDB files containing Gibbs-energy parameters and is accessed through the Thermo-Calc graphical interface, console mode, TC-Python SDK, or TC-Toolbox for MATLAB (vary2023highthroughputstudyof pages 66-68). These programmatic interfaces are critical for ML workflows, as they enable batch generation of thermodynamic features (phase fractions, driving forces, solidification paths) that serve as physics-based descriptors in ML models. Companion mobility databases (MOBFE, MOBNI, etc.) enable diffusion and kinetic simulations via DICTRA.

### 3.2 Pandat (CompuTherm, computherm.com)
Pandat offers CALPHAD-based thermodynamic databases for Al, Mg, Ni, Ti, Fe, Cu, HEA, and solder alloy systems (walle2018thethermodynamicdatabase pages 5-6). It provides phase diagram calculation, solidification simulation, and Scheil analysis capabilities with batch processing for generating datasets.

### 3.3 OpenCalphad
OpenCalphad is a free, open-source CALPHAD tool for thermodynamic calculations, and the related pycalphad Python library enables scripting of phase-equilibrium calculations using existing TDB files (walle2018thethermodynamicdatabase pages 5-6). These tools lower the barrier for integrating CALPHAD calculations into ML pipelines.

### 3.4 Thermodynamic Database Database (TDBDB)
The TDBDB is a repository that indexes and provides access to published CALPHAD thermodynamic database files, facilitating discovery and reuse of assessed thermodynamic parameter sets (walle2018thethermodynamicdatabase pages 5-6).

## 4. Commercial Property and Simulation Software

### 4.1 JMatPro (Sente Software, sentesoftware.co.uk)
JMatPro is a commercial CALPHAD-based software that calculates phase stability, mechanical properties (Young's modulus, thermal conductivity, Poisson's ratio), thermophysical properties, and transformation diagrams (TTT/CCT) for multicomponent alloy systems (cote2020ontheelemental pages 3-4, cote2020ontheelemental pages 4-6). It supports aluminum, titanium, steel, nickel superalloy, magnesium, and cobalt alloy families. JMatPro is noted for requiring fewer user inputs than other CALPHAD tools and directly computing engineering-relevant properties through proprietary mixture models, making it useful for rapid generation of property estimates across compositional ranges (cote2020ontheelemental pages 4-6).

### 4.2 Granta / ANSYS (ansys.com/products/materials)
The Granta ecosystem, now part of ANSYS, comprises three main products: **Granta EduPack** (educational), **Granta Selector** (professional materials selection), and **Granta MI** (enterprise materials information management) (mercier2602acuratedliterature pages 3-5). These tools provide curated databases covering metals, polymers, ceramics, composites, and natural materials with property profiles including mechanical (strength, modulus, hardness, fatigue), thermal (conductivity, expansion), electrical, optical, and environmental (Eco Audit, CO₂ footprint) properties (ashby2007teachingengineeringmaterials pages 9-11, ashby2007teachingengineeringmaterials pages 1-3). Ashby-style materials property charts enable graphical screening and ranking. The database includes specialized add-ons such as MMPDS aerospace metals data (ashby2007teachingengineeringmaterials pages 11-13). Granta EduPack is available through educational licenses at universities, while Selector and MI require commercial licenses. The Granta MI platform enables enterprise-scale management of materials data with links to simulation tools (mercier2602acuratedliterature pages 3-5, mercier2602acuratedliterature pages 15-19).

### 4.3 Total Materia (totalmateria.com)
Total Materia (Key to Metals) is a proprietary subscription-based database covering over 350,000 metallic materials from 75+ countries, providing composition data, mechanical and physical properties, and cross-referenced international standards and specifications. It covers steels, aluminum, titanium, nickel, copper, magnesium, and specialty alloys, making it one of the most comprehensive commercial alloy databases (green2017fulfillingthepromise pages 12-13).

### 4.4 Citrine Informatics (citrine.io)
Citrine Informatics provides an AI-driven materials informatics platform originally built around the Citrination open-data platform (now evolved into the AIRD platform). It combines structure–property–process data for over 17 million materials with ML recommendation engines and sequential design workflows (green2017fulfillingthepromise pages 12-13, ling2018machinelearningfor pages 1-2). Citrine has demonstrated ML-guided alloy discovery for thermoelectric materials, aluminum alloys, nickel superalloys, and shape memory alloys, making it one of the most ML-native platforms available. The platform is proprietary with enterprise licensing.

### 4.5 Alloys-by-Design (ABD)
ABD, originally developed by Rolls-Royce and collaborators, is an industrial platform for computational screening of nickel-based superalloy compositions. It can evaluate properties of millions of potential alloy compositions simultaneously, integrating thermodynamic calculations with property models for creep, oxidation, and phase stability (rahman2025reviewmachinelearning pages 25-26). Access is typically restricted to industrial partners.

## 5. Experimental and Reference Databases

### 5.1 MatWeb (matweb.com)
MatWeb is a widely used free online database containing property data for over 100,000 materials (metals, polymers, ceramics, semiconductors), cataloged from manufacturer datasheets and supplier data (green2017fulfillingthepromise pages 12-13, ramakrishna2019materialsinformatics pages 4-5). Data include composition, mechanical properties (yield strength, tensile strength, elongation, hardness), and physical properties. While accessible without registration, data extraction for large-scale ML studies typically requires manual effort as no bulk-download API is provided.

### 5.2 ASM International (asminternational.org)
ASM International provides several proprietary subscription-based databases focused on metals and alloys, including the Alloy Phase Diagram Center, ASM Alloy Center Database, and ASM Micrograph Center (green2017fulfillingthepromise pages 12-13). These cover steels, aluminum, titanium, nickel, copper, and magnesium alloys with data types encompassing phase diagrams, mechanical properties, corrosion data, micrographs, and failure analysis information. ASM data have been widely used as training data for ML models predicting alloy properties (ling2018machinelearningfor pages 4-6, durodola2022machinelearningfor pages 14-15).

### 5.3 NIST Materials Data Resources
NIST provides several materials data resources including the NIST Materials Data Repository, Standard Reference Data (SRDs) for thermophysical properties, and specialized databases for alloy phase equilibria. NIST has developed CALPHAD phase-diagram databases for metallic alloys capturing experimental and computational thermodynamics, kinetics, diffusion, and elastic properties (ramakrishna2019materialsinformatics pages 4-5). NIST data resources are generally open or partially open access.

### 5.4 NIMS MatNavi (mits.nims.go.jp)
The Japanese National Institute for Materials Science (NIMS) maintains MatNavi, a national materials database covering metals, polymers, and ceramics with data including mechanical properties (creep, fatigue), electronic properties, and thermal properties (ramakrishna2019materialsinformatics pages 4-5). Access is open or partially open, and the creep/fatigue datasets have been particularly valuable for ML applications in high-temperature alloy design.

### 5.5 Knovel (knovel.com)
Knovel, an Elsevier product, provides access to interactive engineering handbooks and technical reference data covering broad material classes. It includes searchable property tables from established references. Access is via institutional subscription, and while its data are high quality, the document-oriented format is less optimized for bulk ML extraction (green2017fulfillingthepromise pages 17-18).

### 5.6 SpringerMaterials (materials.springer.com)
SpringerMaterials (incorporating the Landolt-Börnstein data series) provides curated crystal structure data, phase diagrams, and physical/chemical property data across broad material classes. It is available via institutional subscription (green2017fulfillingthepromise pages 17-18).

## 6. Specialized Alloy-Family Databases

### 6.1 ULTERA (ultera.org)
ULTERA (Ultra-high Temperature Refractory Alloy) is described as the largest and highest-quality curated dataset of high-entropy alloy properties in the world (hart2021machinelearningfor pages 22-22). It provides composition, mechanical properties, and phase data for HEAs and refractory HEAs, specifically designed for ML-driven alloy discovery workflows.

### 6.2 Fatigue and Additive Manufacturing Databases
Specialized open-access databases have been developed for fatigue properties of additively manufactured alloys (e.g., FatigueData-AM2022), containing S-N, ε-N, and da/dN-ΔK data along with AM processing parameters, static mechanical properties, and testing conditions. Similar curated datasets exist for Ti alloy mechanical properties and microstructural features (282 multicomponent Ti alloys with composition, phase constituents, modulus, hardness, and strength data) and for Al alloy compositions extracted from literature and patents (ling2018machinelearningfor pages 4-6, rahman2025reviewmachinelearning pages 9-10).

## 7. Relevance for AI/ML-Guided Alloy Design

For ML-guided alloy design campaigns, the choice of database depends on the design stage and alloy family. Computational repositories (Materials Project, AFLOW, OQMD) provide large, consistently computed datasets ideal for training property-prediction models and constructing thermodynamic stability features (oses2018datadrivendesignof pages 2-3, jain2016researchupdatethe pages 4-5). CALPHAD databases (Thermo-Calc, Pandat) generate physics-based features (phase fractions, solidification ranges, driving forces) that significantly improve ML model accuracy when combined with composition descriptors (vary2023highthroughputstudyof pages 66-68, durodola2022machinelearningfor pages 14-15). Experimental databases (ASM, MatWeb, Total Materia) supply the engineering-relevant properties (fatigue, corrosion, creep, processing conditions) that are essential for connecting ML predictions to real-world performance requirements (ling2018machinelearningfor pages 4-6, rahman2025reviewmachinelearning pages 9-10). Platforms like Citrine Informatics and AFLOW-ML provide end-to-end ML infrastructure with built-in recommendation engines and uncertainty quantification (oses2018datadrivendesignof pages 3-5, ling2018machinelearningfor pages 1-2). For high-entropy alloys specifically, ULTERA and the TCHEA database provide the most comprehensive compositional and property coverage (vary2023highthroughputstudyof pages 66-68, rahman2025reviewmachinelearning pages 25-26). Typical ML data types for alloy design include composition vectors, processing parameters (heat treatment temperatures/times, manufacturing routes), thermodynamic descriptors from CALPHAD, and target properties such as yield strength, tensile strength, elongation, hardness, fatigue life, creep rupture, and corrosion resistance (rahman2025reviewmachinelearning pages 9-10, rahman2025reviewmachinelearning pages 10-12).

References

1. (jain2016researchupdatethe pages 4-5): Anubhav Jain, Kristin A. Persson, and Gerbrand Ceder. Research update: the materials genome initiative: data sharing and the impact of collaborative ab initio databases. APL Materials, 4:053102-053102, Mar 2016. URL: https://doi.org/10.1063/1.4944683, doi:10.1063/1.4944683. This article has 180 citations and is from a domain leading peer-reviewed journal.

2. (ramakrishna2019materialsinformatics pages 4-5): Seeram Ramakrishna, Tong-Yi Zhang, Wen-Cong Lu, Quan Qian, Jonathan Sze Choong Low, Jeremy Heiarii Ronald Yune, Daren Zong Loong Tan, Stéphane Bressan, Stefano Sanvito, and Surya R. Kalidindi. Materials informatics. Journal of Intelligent Manufacturing, 30:2307-2326, Jan 2019. URL: https://doi.org/10.1007/s10845-018-1392-0, doi:10.1007/s10845-018-1392-0. This article has 201 citations and is from a domain leading peer-reviewed journal.

3. (toher2019automatedcomputationof pages 12-13): Cormac Toher, Corey Oses, and Stefano Curtarolo. Automated computation of materials properties. Materials Informatics, pages 181-222, Aug 2019. URL: https://doi.org/10.1002/9783527802265.ch7, doi:10.1002/9783527802265.ch7. This article has 3 citations.

4. (oses2018datadrivendesignof pages 3-5): Corey Oses, Cormac Toher, and Stefano Curtarolo. Data-driven design of inorganic materials with the automatic flow framework for materials discovery. MRS Bulletin, 43:670-675, Sep 2018. URL: https://doi.org/10.1557/mrs.2018.207, doi:10.1557/mrs.2018.207. This article has 48 citations and is from a domain leading peer-reviewed journal.

5. (jain2016researchupdatethe pages 11-13): Anubhav Jain, Kristin A. Persson, and Gerbrand Ceder. Research update: the materials genome initiative: data sharing and the impact of collaborative ab initio databases. APL Materials, 4:053102-053102, Mar 2016. URL: https://doi.org/10.1063/1.4944683, doi:10.1063/1.4944683. This article has 180 citations and is from a domain leading peer-reviewed journal.

6. (hart2021machinelearningfor pages 22-22): Gus L. W. Hart, Tim Mueller, Cormac Toher, and Stefano Curtarolo. Machine learning for alloys. Nature Reviews Materials, 6:730-755, Jul 2021. URL: https://doi.org/10.1038/s41578-021-00340-w, doi:10.1038/s41578-021-00340-w. This article has 714 citations.

7. (vary2023highthroughputstudyof pages 66-68): C Vary. High-throughput study of multi-principal elements systems for the development of cobalt-free hardfacing coatings. Unknown journal, 2023.

8. (walle2018thethermodynamicdatabase pages 5-6): Axel van de Walle, Chiraag Nataraj, and Zi-Kui Liu. The thermodynamic database database. Calphad, 61:173-178, Jun 2018. URL: https://doi.org/10.1016/j.calphad.2018.04.003, doi:10.1016/j.calphad.2018.04.003. This article has 52 citations.

9. (cote2020ontheelemental pages 3-4): D. Cote, Bryer C. Sousa, Jr. Victor K. Champagne, and Jr. Richard D. Sisson. On the elemental impact factor, a method to determine an alloy’s compositional influences upon phase stability and metallurgical material properties. Materials, 13:5747, Dec 2020. URL: https://doi.org/10.3390/ma13245747, doi:10.3390/ma13245747. This article has 1 citations.

10. (cote2020ontheelemental pages 4-6): D. Cote, Bryer C. Sousa, Jr. Victor K. Champagne, and Jr. Richard D. Sisson. On the elemental impact factor, a method to determine an alloy’s compositional influences upon phase stability and metallurgical material properties. Materials, 13:5747, Dec 2020. URL: https://doi.org/10.3390/ma13245747, doi:10.3390/ma13245747. This article has 1 citations.

11. (green2017fulfillingthepromise pages 12-13): M. L. Green, C. L. Choi, J. R. Hattrick-Simpers, A. M. Joshi, I. Takeuchi, S. C. Barron, E. Campo, T. Chiang, S. Empedocles, J. M. Gregoire, A. G. Kusne, J. Martin, A. Mehta, K. Persson, Z. Trautt, J. Van Duren, and A. Zakutayev. Fulfilling the promise of the materials genome initiative with high-throughput experimental methodologies. Applied physics reviews, 4:011105, Mar 2017. URL: https://doi.org/10.1063/1.4977487, doi:10.1063/1.4977487. This article has 372 citations and is from a domain leading peer-reviewed journal.

12. (mercier2602acuratedliterature pages 3-5): A Curated Literature Database for Monitoring More Than 30 Years of Ansys Granta Product Usage This article has 0 citations.

13. (mercier2602acuratedliterature pages 15-19): A Curated Literature Database for Monitoring More Than 30 Years of Ansys Granta Product Usage This article has 0 citations.

14. (green2017fulfillingthepromise pages 17-18): M. L. Green, C. L. Choi, J. R. Hattrick-Simpers, A. M. Joshi, I. Takeuchi, S. C. Barron, E. Campo, T. Chiang, S. Empedocles, J. M. Gregoire, A. G. Kusne, J. Martin, A. Mehta, K. Persson, Z. Trautt, J. Van Duren, and A. Zakutayev. Fulfilling the promise of the materials genome initiative with high-throughput experimental methodologies. Applied physics reviews, 4:011105, Mar 2017. URL: https://doi.org/10.1063/1.4977487, doi:10.1063/1.4977487. This article has 372 citations and is from a domain leading peer-reviewed journal.

15. (green2017fulfillingthepromise pages 11-12): M. L. Green, C. L. Choi, J. R. Hattrick-Simpers, A. M. Joshi, I. Takeuchi, S. C. Barron, E. Campo, T. Chiang, S. Empedocles, J. M. Gregoire, A. G. Kusne, J. Martin, A. Mehta, K. Persson, Z. Trautt, J. Van Duren, and A. Zakutayev. Fulfilling the promise of the materials genome initiative with high-throughput experimental methodologies. Applied physics reviews, 4:011105, Mar 2017. URL: https://doi.org/10.1063/1.4977487, doi:10.1063/1.4977487. This article has 372 citations and is from a domain leading peer-reviewed journal.

16. (ling2018machinelearningfor pages 1-2): Julia Ling, Erin Antono, Saurabh Bajaj, Sean Paradiso, Maxwell Hutchinson, Bryce Meredig, and Brenna M. Gibbons. Machine learning for alloy composition and process optimization. Volume 6: Ceramics; Controls, Diagnostics, and Instrumentation; Education; Manufacturing Materials and Metallurgy, Jun 2018. URL: https://doi.org/10.1115/gt2018-75207, doi:10.1115/gt2018-75207. This article has 38 citations.

17. (rahman2025reviewmachinelearning pages 25-26): Arafat Rahman, Md Sojib Hossain, and Abdullah-Bin Siddique. Review: machine learning approaches for diverse alloy systems. Journal of Materials Science, 60:12189-12221, Jul 2025. URL: https://doi.org/10.1007/s10853-025-11154-4, doi:10.1007/s10853-025-11154-4. This article has 12 citations and is from a peer-reviewed journal.

18. (yuan2024applicationsofmachine pages 16-17): Junhao Yuan, Zhen Li, Yujia Yang, Anyi Yin, Wenjie Li, Dan Sun, and Qing Wang. Applications of machine learning method in high-performance materials design: a review. Journal of Materials Informatics, Sep 2024. URL: https://doi.org/10.20517/jmi.2024.15, doi:10.20517/jmi.2024.15. This article has 24 citations.

19. (jain2016researchupdatethe pages 10-11): Anubhav Jain, Kristin A. Persson, and Gerbrand Ceder. Research update: the materials genome initiative: data sharing and the impact of collaborative ab initio databases. APL Materials, 4:053102-053102, Mar 2016. URL: https://doi.org/10.1063/1.4944683, doi:10.1063/1.4944683. This article has 180 citations and is from a domain leading peer-reviewed journal.

20. (toher2019automatedcomputationof pages 13-14): Cormac Toher, Corey Oses, and Stefano Curtarolo. Automated computation of materials properties. Materials Informatics, pages 181-222, Aug 2019. URL: https://doi.org/10.1002/9783527802265.ch7, doi:10.1002/9783527802265.ch7. This article has 3 citations.

21. (oses2018autonomousdatadrivendesign pages 3-5): Corey Oses, Cormac Toher, and Stefano Curtarolo. Autonomous data-driven design of inorganic materials with aflow. Preprint, Jan 2018. URL: https://doi.org/10.48550/arxiv.1803.05035, doi:10.48550/arxiv.1803.05035. This article has 4 citations.

22. (oses2018autonomousdatadrivendesign pages 2-3): Corey Oses, Cormac Toher, and Stefano Curtarolo. Autonomous data-driven design of inorganic materials with aflow. Preprint, Jan 2018. URL: https://doi.org/10.48550/arxiv.1803.05035, doi:10.48550/arxiv.1803.05035. This article has 4 citations.

23. (oses2018datadrivendesignof pages 2-3): Corey Oses, Cormac Toher, and Stefano Curtarolo. Data-driven design of inorganic materials with the automatic flow framework for materials discovery. MRS Bulletin, 43:670-675, Sep 2018. URL: https://doi.org/10.1557/mrs.2018.207, doi:10.1557/mrs.2018.207. This article has 48 citations and is from a domain leading peer-reviewed journal.

24. (ashby2007teachingengineeringmaterials pages 9-11): MF Ashby, D Cebon, and A Silva. Teaching engineering materials: the ces edupack. Unknown journal, 2007.

25. (ashby2007teachingengineeringmaterials pages 1-3): MF Ashby, D Cebon, and A Silva. Teaching engineering materials: the ces edupack. Unknown journal, 2007.

26. (ashby2007teachingengineeringmaterials pages 11-13): MF Ashby, D Cebon, and A Silva. Teaching engineering materials: the ces edupack. Unknown journal, 2007.

27. (ling2018machinelearningfor pages 4-6): Julia Ling, Erin Antono, Saurabh Bajaj, Sean Paradiso, Maxwell Hutchinson, Bryce Meredig, and Brenna M. Gibbons. Machine learning for alloy composition and process optimization. Volume 6: Ceramics; Controls, Diagnostics, and Instrumentation; Education; Manufacturing Materials and Metallurgy, Jun 2018. URL: https://doi.org/10.1115/gt2018-75207, doi:10.1115/gt2018-75207. This article has 38 citations.

28. (durodola2022machinelearningfor pages 14-15): J.F. Durodola. Machine learning for design, phase transformation and mechanical properties of alloys. Jan 2022. URL: https://doi.org/10.1016/j.pmatsci.2021.100797, doi:10.1016/j.pmatsci.2021.100797. This article has 132 citations and is from a domain leading peer-reviewed journal.

29. (rahman2025reviewmachinelearning pages 9-10): Arafat Rahman, Md Sojib Hossain, and Abdullah-Bin Siddique. Review: machine learning approaches for diverse alloy systems. Journal of Materials Science, 60:12189-12221, Jul 2025. URL: https://doi.org/10.1007/s10853-025-11154-4, doi:10.1007/s10853-025-11154-4. This article has 12 citations and is from a peer-reviewed journal.

30. (rahman2025reviewmachinelearning pages 10-12): Arafat Rahman, Md Sojib Hossain, and Abdullah-Bin Siddique. Review: machine learning approaches for diverse alloy systems. Journal of Materials Science, 60:12189-12221, Jul 2025. URL: https://doi.org/10.1007/s10853-025-11154-4, doi:10.1007/s10853-025-11154-4. This article has 12 citations and is from a peer-reviewed journal.