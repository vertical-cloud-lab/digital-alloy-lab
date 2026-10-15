Question: How do free/open CALPHAD thermodynamic databases (like those indexed in TDBDB, COST507, MatCalc open databases) compare in quality and scope to commercial assessed databases like Thermo-Calc's TCFE, TCHEA, and TCNI? 

Specifically:
1. What are the known limitations of free/academic TDB files vs commercial databases?
2. Has anyone published direct comparisons of predictions from free vs commercial databases?
3. What experimental data is needed to build a high-quality assessed CALPHAD database (the CALPHAD assessment process)?
4. What types of experiments are required (calorimetry, diffusion couples, phase diagram mapping, etc.)?
5. How much effort (person-years, number of experiments) does it typically take to assess a multicomponent database?
6. Are there any open-source database assessment efforts that approach commercial quality?

## Free/Open vs. Commercial CALPHAD Thermodynamic Databases: A Comprehensive Comparison

### 1. Known Limitations of Free/Academic TDB Files vs. Commercial Databases

Free and academic CALPHAD TDB files differ from commercial databases in several critical dimensions:

**Scope and Coverage.** Commercial databases such as TCHEA1 (15 elements, 105 fully assessed binaries, 200 ternaries with 104 fully assessed, 163 phases), TCNI8 (~27 elements, ~490 phases, 280 binary and 272 higher-order assessed systems), and SSOL6 (~79 elements, 1331 phases, 575 binary and 153 higher-order assessed systems) provide far broader elemental and subsystem coverage than typical open TDB files (mao2017tchea1athermodynamic pages 1-2, hardwick2020developmentofnovel pages 57-60). In contrast, a general-purpose open database like PanSol defines only 785 of 3003 possible binary combinations from 78 elements (wertz2018towardmultiprincipalcomponent pages 2-3). Free databases often cover binaries near the corners of major-component systems but leave full composition ranges and many ternary interactions unassessed (mao2017tchea1athermodynamic pages 1-2, chen2018databasedevelopmentand pages 5-7).

**Consistency and Quality Assurance.** Commercial databases undergo rigorous internal consistency checks: phase models, sublattice descriptions, and naming conventions are harmonized across all subsystems, and unassessed interaction parameters are explicitly estimated rather than defaulted to zero (fries2005developmentofmulticomponent pages 1-2, fries2005developmentofmulticomponent pages 2-4). Open TDB files assembled from disparate literature assessments frequently suffer from format variations across software implementations, ambiguous notation, limited metadata and provenance tracking, and conversion-induced errors (mianiUnknownyearperspectivestudyfor pages 1-4, mianiUnknownyear…forthe pages 1-4). The TDBDB project, which indexed 766 data entries from 528 publications, required a dedicated utility (ocutil) to fix common formatting problems such as truncated lines, nonprintable characters, and misordered keywords (walle2018thethermodynamicdatabase pages 2-3, walle2018thethermodynamicdatabase pages 1-2).

**Extrapolation Reliability.** Because free databases typically lack comprehensive ternary and higher-order descriptions, their predictions in multicomponent space rely heavily on extrapolation rather than interpolation, increasing uncertainty (wertz2018towardmultiprincipalcomponent pages 2-3). Commercial databases are designed to include as many assessed ternary systems as feasible — for instance, TCNI8 includes 272 ternary/higher-order systems — specifically to reduce extrapolation errors (hardwick2020developmentofnovel pages 57-60, chen2018databasedevelopmentand pages 7-10).

**Additional Properties.** Commercial databases increasingly include molar volume, thermal expansion, and elastic property descriptions, which are generally absent from open TDB files (kattner2016thecalphadmethod pages 11-13, mao2017tchea1athermodynamic pages 1-2).

| Database | Type | Platform | Elements | Assessed binaries | Assessed ternaries | Phases | Notable features/limitations |
|---|---|---|---|---|---|---|---|
| TCHEA1 | Commercial | Thermo-Calc | 15 | 105 | 200 (104 fully) | 163 | HEA-focused; validated across many HEA systems; includes volume data (mao2017tchea1athermodynamic pages 1-2) |
| TCHEA4 | Commercial | Thermo-Calc | ~26 | 307 | 493 (higher-order) | ~500 | Expanded HEA/MPEA coverage vs earlier versions (hardwick2020developmentofnovel pages 57-60) |
| TCNI8 | Commercial | Thermo-Calc | ~27 | 280 | 272 (ternary/higher) | ~490 | Ni-base superalloys; broad higher-order coverage (hardwick2020developmentofnovel pages 57-60) |
| TCFE8 | Commercial | Thermo-Calc | Steels (not specified) | – | – | – | Widely used steel DB; commercial examples listed (kattner2016thecalphadmethod pages 11-13) |
| SSOL6 | Commercial | Thermo-Calc | ~79 | 575 | 153 (ternary/higher) | 1331 | General solutions DB; some binaries still unassessed (e.g., Cu–Ga, Fe–Ga, Fe–Ge, Ge–Ni) (hardwick2020developmentofnovel pages 57-60) |
| COST 507 (Light alloys) | Open/EU-funded | Various (Thermo-Calc, Pandat, MTDATA, FactSage) | Light alloys (Al/Mg/Ti, etc.) | – | – | – | EU assessment program for light alloys; widely referenced (kattner2016thecalphadmethod pages 17-19) |
| COST 531 (Lead-free solders) | Open/EU-funded | Various (Thermo-Calc, Pandat, MTDATA, FactSage) | ~10 (Ag, Cu, Sn, Au, Ni, Bi, Sb, In, Pb, Zn) | – | ~20 assessed | – | Focused on solder/substrate systems; critical re-assessments and calorimetry/phase data (kroupa2007thedevelopmentof pages 1-2, kroupa2007thedevelopmentof pages 4-5) |
| MatCalc mc_fe (steel DB) | Open/community | MatCalc | Fe-based steels (varies) | – | – | – | Community/open steel TDB reported for MatCalc; details and scope vary (kattner2016thecalphadmethod pages 17-19, kattner2016thecalphadmethod pages 11-13) |
| TDBDB collection | Open index | TDB index with OpenCalphad previews | Varies | Aggregates literature | Aggregates literature | – | 766 data entries from 528 publications; ocutil fixes common TDB format issues; limited plotting (walle2018thethermodynamicdatabase pages 2-3, walle2018thethermodynamicdatabase pages 1-2, walle2018thethermodynamicdatabase pages 3-5) |
| PanSol (PanDat) | Commercial | Pandat | Up to 78 candidates | 785 defined (of 3003 possible) | Sparse (varies) | Solution phases (varies) | Broad solution DB with sparse binary coverage vs tailored DBs (wertz2018towardmultiprincipalcomponent pages 2-3, wertz2018towardmultiprincipalcomponent pages 3-4) |
| SGTE binary collection | Reference | SGTE/various | 80 | 1238 unique binary systems (2773 datasets) | – | – | Multiple assessments/system; format/provenance inconsistencies motivate XML standardization (mianiUnknownyearperspectivestudyfor pages 1-4, mianiUnknownyear…forthe pages 1-4) |


*Table: Side-by-side comparison of notable free/open and commercial CALPHAD databases, highlighting scope, assessed subsystems, and distinguishing features. Citations indicate sources for counts and notable limitations.*

### 2. Published Direct Comparisons of Predictions from Free vs. Commercial Databases

While head-to-head comparisons between explicitly "free" and "commercial" databases are rare, several studies have compared predictions across different commercial databases, revealing the same types of discrepancies that would be even more pronounced with less comprehensive open databases:

**Ravi & Wolverton (2005)** directly compared the Thermotech and Computherm databases for 3xx and 6xxx aluminum alloys. They found both qualitative and quantitative differences, particularly for Fe-, Mn-, Cr-, and Zn-containing intermetallics. Some phases were present in one database but absent in the other (e.g., Al₃Ti, Al₁₃Cr₄Si₄), and quantitative differences in phase fractions of Q-phase and Al₂Cu were observed (ravi2005comparisonofthermodynamic pages 1-2, ravi2005comparisonofthermodynamic pages 5-7, ravi2005comparisonofthermodynamic pages 3-5). First-principles DFT calculations were used to arbitrate between databases (ravi2005comparisonofthermodynamic pages 11-11).

**Wertz, Miller & Senkov (2018)** conducted a large-scale comparison of eight Pandat databases (PanAl, PanCo, PanFe, PanMo, PanNb, PanNi, PanSol, PanTi) for predicting ternary alloy systems, generating ~29,000 unique compositions and ~78,850 composition-database calculations. They introduced quantitative metrics — fraction of assessed binaries (FAB) and fraction of assessed ternaries (FAT) — and found that each fully assessed binary raised the fraction of matching ternary predictions by ~20% on average, with partial assessments recovering ~75% of the benefit of full assessment (wertz2018towardmultiprincipalcomponent pages 3-4, wertz2018towardmultiprincipalcomponent pages 9-11, wertz2018towardmultiprincipalcomponent pages 11-12).

**Gorsse & Senkov (2018)** systematically examined extrapolation reliability and concluded that extrapolation from binaries alone (without ternary descriptions) can produce correct quaternary predictions only when: (i) binary miscibility gaps are absent, (ii) binary intermetallics are few, and (iii) no ternary intermetallic phases exist (gorsse2018aboutthereliability pages 1-3). These restrictive conditions are rarely met in practice.

**Presoly et al. (2016)** compared systematic DSC measurements on high-purity model steel alloys against existing database predictions and found discrepancies in eutectic ranges and δ-region stability, motivating database re-optimization (presoly2016thermodynamicoptimizationof pages 9-9).

### 3. Experimental Data Required for High-Quality CALPHAD Database Assessment

Building a high-quality CALPHAD database requires a comprehensive suite of experimental data types, organized hierarchically from unary through binary and ternary systems (campbell2014thedevelopmentof pages 7-9, kattner2020theneedfor pages 19-20, kattner2020theneedfor pages 1-3, kattner2020theneedfor pages 6-8):

**Phase equilibria data:** Phase boundary measurements from thermal analysis (DTA/DSC), isothermal equilibration experiments, and temperature-scanning techniques identify invariant reactions, liquidus/solidus temperatures, and phase transition sequences (kattner2020theneedfor pages 19-20, presoly2016thermodynamicoptimizationof pages 1-4).

**Thermochemical data:** Directly measured enthalpies from solution, drop, and reaction calorimetry; chemical potentials and activities from EMF and vapor pressure measurements; and heat capacities from DSC or adiabatic calorimetry (campbell2014thedevelopmentof pages 7-9, kattner2020theneedfor pages 19-20, kattner2020theneedfor pages 6-8).

**Phase identification and composition:** XRD, neutron diffraction, and EBSD for phase identification and crystal structure determination; EPMA/WDS/EDS for quantitative phase compositions and tie-line determination (campbell2014thedevelopmentof pages 7-9, kattner2020theneedfor pages 19-20).

**Kinetic/diffusion data:** Diffusion couple experiments and tracer diffusion measurements provide interdiffusion coefficients and atomic mobilities essential for mobility databases (campbell2014thedevelopmentof pages 7-9, perrut2015thermodynamicmodelingby pages 8-9).

**Structural data:** Crystallographic information (space groups, Wyckoff positions, site occupancies) is needed to define sublattice models within the Compound Energy Formalism (campbell2014thedevelopmentof pages 7-9, campbell2014thedevelopmentof pages 5-7).

| Experimental Technique | Data Type Obtained | Role in CALPHAD Assessment | Notes |
|---|---|---|---|
| DTA/DSC | Phase transition temperatures (liquidus/solidus, invariant reactions), transformation enthalpies, heat capacity | Constrain phase boundaries and transitions; calibrate Cp(T) and validate invariant equilibria | Requires equilibrated samples and careful baseline/metadata; widely used for mapping phase diagrams (kattner2020theneedfor pages 19-20, campbell2014thedevelopmentof pages 7-9) |
| Solution calorimetry | Enthalpies of mixing/formation | Fit excess Gibbs energy parameters; assess short-/medium-range order in solutions | Critical for solution-phase models; complements phase equilibria (kattner2020theneedfor pages 19-20, campbell2014thedevelopmentof pages 7-9) |
| Drop calorimetry | Enthalpy increments; heat capacity vs T | Anchor temperature dependence of Gibbs energies for solids/liquids | Useful at elevated T; supports Cp(T) and H(T) functions (kattner2020theneedfor pages 19-20) |
| EMF measurements | Activities; partial Gibbs energies/chemical potentials | Directly constrain activities and endmember chemical potentials; validate Gibbs–Duhem consistency | High information content for solution phases; key for fitting activities (kattner2020theneedfor pages 19-20, campbell2014thedevelopmentof pages 7-9) |
| Vapor pressure measurements | Partial pressures; activities; partial Gibbs energies | Constrain vapor–condensed equilibria; calibrate volatile-species thermodynamics | Important for high-T systems and elements with significant vapor pressures (kattner2020theneedfor pages 19-20) |
| EPMA/EDS/WDS | Equilibrium phase compositions; tie-lines/tie-triangles | Define tie-lines in binary/ternary systems; validate phase-equilibria calculations | Requires careful sample prep and metadata; essential for robust diagram mapping (campbell2014thedevelopmentof pages 7-9, kattner2020theneedfor pages 19-20) |
| XRD/neutron diffraction | Phase identification; crystal structure; site occupancies | Select and validate sublattice/ordering models; enforce lattice stabilities | Crystal-structure identifiers aid consistent phase modeling across systems (campbell2014thedevelopmentof pages 7-9, kattner2020theneedfor pages 19-20) |
| Optical/SEM/TEM microscopy | Microstructure; phase identification; phase fractions/morphologies | Support phase-fraction validation; confirm presence/absence of phases; infer equilibrated states | Complements diffraction and composition analysis (kattner2020theneedfor pages 19-20, campbell2014thedevelopmentof pages 7-9) |
| Diffusion couples/tracer diffusion | Composition profiles; interdiffusion coefficients; tracer diffusivities | Build and fit mobility databases; combine with thermodynamic factors for kinetic simulations | Kinetic data are parameterized with CALPHAD conventions for mobility; essential for DICTRA-style models (campbell2014thedevelopmentof pages 7-9, kattner2020theneedfor pages 6-8) |
| Dilatometry | Transformation signatures; thermal expansion; molar volume changes | Constrain molar-volume models and detect phase transitions | Useful for coupled thermodynamic–mechanical modeling (kattner2020theneedfor pages 19-20) |
| High-temperature levitation/pulse heating | Cp and enthalpy of refractory/undercooled liquids; high-T properties | Fill high-T data gaps for liquid/undercooled states; improve liquid-phase models | Containerless methods reduce contamination and enable extreme-T measurements (kattner2020theneedfor pages 6-8) |


*Table: Summary of key experimental techniques that provide the phase-equilibria, thermochemical, structural, and kinetic data required for high-quality CALPHAD assessments. Entries highlight what each method measures and how those data are used to parameterize and validate thermodynamic and mobility models (kattner2020theneedfor pages 19-20, campbell2014thedevelopmentof pages 7-9, kattner2020theneedfor pages 6-8).*

### 4. Types of Experiments Required

The specific experimental techniques employed in CALPHAD assessment span multiple categories (kattner2020theneedfor pages 19-20):

- **Thermal analysis:** DTA, DSC, thermogravimetry (TG) for phase transitions and transformation enthalpies
- **Calorimetry:** Solution, drop, and adiabatic calorimetry for enthalpies of mixing/formation and heat capacities
- **Electrochemistry:** EMF measurements for activities and partial Gibbs energies
- **Vapor pressure:** Knudsen effusion and related techniques for volatile systems
- **Composition analysis:** EPMA, WDS, EDS for equilibrium phase compositions
- **Structural characterization:** XRD, neutron diffraction for phase identification, crystal structure, and site occupancies
- **Microscopy:** Optical, SEM, TEM for microstructural observation and phase fraction estimation
- **Diffusion experiments:** Diffusion couples, diffusion triples, and radioactive tracer studies (perrut2015thermodynamicmodelingby pages 8-9, hackenberg2011thermodynamicsandphase pages 4-6)
- **High-temperature methods:** Containerless (levitation), pulse-heating techniques for refractory systems and undercooled liquids (kattner2020theneedfor pages 6-8)
- **Dilatometry/interferometry:** For molar volume changes and thermal expansion (kattner2020theneedfor pages 19-20)

### 5. Scale of Effort for Multicomponent Database Assessment

The effort required to build a comprehensive CALPHAD database is enormous due to the combinatorial scaling of subsystems. A 12-component system comprises 66 binary, 220 ternary, and 495 quaternary subsystems; a 15-element database requires 105 binary and 455 ternary descriptions; a 25-element framework involves ~300 binaries and ~2300 ternaries (kattner2016thecalphadmethod pages 13-14, chen2018databasedevelopmentand pages 7-10, wertz2018towardmultiprincipalcomponent pages 2-3). In practice, the SGTE effort to compile binary phase diagram assessments has involved over 1,000 person-years across the community and produced 2773 datasets covering 1238 unique binary systems for 80 elements (mianiUnknownyearperspectivestudyfor pages 1-4).

Commercial databases are described as "costly and time-consuming" to develop (chen2018databasedevelopmentand pages 7-10). A typical "good" commercial database for conventional alloys includes ~70 fully assessed ternaries (e.g., TCAL4, TCMG4), while the most comprehensive contain more than 200 (e.g., TCNI8 with 272 ternary/higher descriptions) (chen2018databasedevelopmentand pages 7-10). Each binary assessment typically requires the critical evaluation and fitting of all available experimental phase diagram and thermochemical data, a process that can take weeks to months per system depending on data availability and complexity. Ternary assessments are considerably more labor-intensive, as they require reconciling multiple binary descriptions and generating new experimental data where gaps exist (schmidfetzer2007assessmenttechniquesdatabase pages 2-3, schmidfetzer2007assessmenttechniquesdatabase pages 3-4). While explicit person-year estimates per binary or ternary system are not consistently reported in the literature, the overall scale of commercial database development clearly represents decades of cumulative expert effort.

### 6. Open-Source Database Assessment Efforts Approaching Commercial Quality

Several open-source efforts are making significant progress toward closing the gap with commercial databases, though none yet match the full scope and validated coverage of mature commercial products:

**OpenCalphad (OC)** is a GNU-licensed, open-source CALPHAD implementation developed by Sundman et al. that provides multicomponent equilibrium calculations, parallelized computation, and a programming interface for coupling to simulation codes. At the time of its publication, it was described as the first high-quality open-source software for multicomponent CALPHAD calculations (sundman2015opencalphada pages 1-3). OC implements core CALPHAD models but relies on external databases; it does not itself provide a comprehensive assessed database (kattner2016thecalphadmethod pages 11-13).

**PyCalphad and ESPEI** represent the most advanced open-source ecosystem for automated CALPHAD database development. PyCalphad is a Python library for computing phase diagrams and Gibbs energy minimization, while ESPEI (Extensible Self-optimizing Phase Equilibria Infrastructure) automates database construction through a two-step workflow: (1) parameter generation from thermochemical and first-principles data via linear fitting with AICc model selection, and (2) Bayesian MCMC optimization using the emcee ensemble sampler to simultaneously fit all parameters against phase-equilibrium data with explicit uncertainty quantification (bocklund2024espeiforefficient pages 1-5, bocklund2021computationaldesignof pages 54-58, bocklund2024espeiforefficient pages 5-9). ESPEI is the first CALPHAD tool to provide systematic uncertainty quantification for multicomponent systems, propagating parameter uncertainties to phase diagram predictions via 95% highest density intervals (bocklund2024espeiforefficient pages 13-17, bocklund2024espeiforefficient pages 17-21). PyCalphad has been recognized with a NASA Software Award runner-up and is used in both academic and industrial settings including SpaceX (olson2024genomicmaterialsdesign pages 29-34).

**TDBDB (Thermodynamic Database Database)** by van de Walle et al. serves as an aggregation and search engine for published TDB files, indexing 766 data entries from 528 publications with links to source papers and OpenCalphad-generated phase diagram previews (walle2018thethermodynamicdatabase pages 2-3, walle2018thethermodynamicdatabase pages 1-2). While invaluable for discovery and reuse of published assessments, it is an index rather than a curated, self-consistent database.

**MatCalc open databases** (e.g., mc_fe for steels) provide community-developed thermodynamic descriptions that have been used in numerous published studies on precipitation kinetics and microstructure evolution in steels and Ni-base superalloys. However, these databases have been shown to require modifications for specific applications — for example, Buerstmayr et al. (2024) found that the MCNI database lacked adequate descriptions for certain carbide phases in René 41 and required re-assessment (kattner2016thecalphadmethod pages 17-19).

**COST-funded projects** (COST 507 for light alloys, COST 531 for lead-free solders) represent important EU-funded, publicly accessible database development efforts. COST 531 produced a self-consistent database for ~10 elements with ~20 assessed ternary systems for solder applications, including new calorimetric and phase-diagram measurements and critical reassessments to ensure internal consistency (kroupa2007thedevelopmentof pages 1-2, kroupa2007thedevelopmentof pages 4-5). These databases demonstrate that coordinated academic efforts can produce high-quality, focused databases, but their scope remains limited compared to broad commercial offerings.

**Proposed standardization efforts** such as XTDB (XML-based TDB format) aim to address the interoperability and provenance-tracking problems that plague open TDB files, by introducing systematic metadata, explicit model specification, and compatibility testing across software implementations (mianiUnknownyearperspectivestudyfor pages 1-4, mianiUnknownyear…forthe pages 1-4).

### Summary

The gap between free/open and commercial CALPHAD databases is fundamentally one of scope, consistency, and sustained investment. Commercial databases benefit from decades of cumulative expert effort, systematic quality assurance, hundreds of assessed binary and ternary subsystems, and ongoing maintenance and updates. Open databases and tools — particularly the PyCalphad/ESPEI ecosystem, OpenCalphad, TDBDB, and COST-funded projects — are advancing rapidly, especially in methodological innovation (automated assessment, uncertainty quantification, first-principles integration). However, no open-source effort yet matches the breadth (tens of elements, hundreds of assessed ternaries) or the validated, internally consistent coverage of commercial products like TCFE, TCNI, or TCHEA for their target alloy systems. The most promising path forward appears to involve combining automated tools like ESPEI with high-throughput first-principles calculations and community data-sharing infrastructure to systematically build and validate open databases at scale.

References

1. (mao2017tchea1athermodynamic pages 1-2): Huahai Mao, Hai-Lin Chen, and Qing Chen. Tchea1: a thermodynamic database not limited for “high entropy” alloys. Journal of Phase Equilibria and Diffusion, 38:353-368, Jul 2017. URL: https://doi.org/10.1007/s11669-017-0570-7, doi:10.1007/s11669-017-0570-7. This article has 203 citations and is from a peer-reviewed journal.

2. (hardwick2020developmentofnovel pages 57-60): L Hardwick. Development of novel ni-based brazing filler metals. Unknown journal, 2020.

3. (wertz2018towardmultiprincipalcomponent pages 2-3): Katelun N. Wertz, Jonathan D. Miller, and Oleg N. Senkov. Toward multi-principal component alloy discovery: assessment of calphad thermodynamic databases for prediction of novel ternary alloy systems. Journal of Materials Research, 33:3204-3217, Oct 2018. URL: https://doi.org/10.1557/jmr.2018.61, doi:10.1557/jmr.2018.61. This article has 29 citations and is from a peer-reviewed journal.

4. (chen2018databasedevelopmentand pages 5-7): Hai-Lin Chen, Huahai Mao, and Qing Chen. Database development and calphad calculations for high entropy alloys: challenges, strategies, and tips. Materials Chemistry and Physics, 210:279-290, May 2018. URL: https://doi.org/10.1016/j.matchemphys.2017.07.082, doi:10.1016/j.matchemphys.2017.07.082. This article has 240 citations and is from a peer-reviewed journal.

5. (fries2005developmentofmulticomponent pages 1-2): Suzana G. Fries and Bo Sundman. Development of multicomponent thermodynamic databases for use in process modelling and simulations. Journal of Physics and Chemistry of Solids, 66:226-230, Feb 2005. URL: https://doi.org/10.1016/j.jpcs.2004.07.026, doi:10.1016/j.jpcs.2004.07.026. This article has 6 citations and is from a peer-reviewed journal.

6. (fries2005developmentofmulticomponent pages 2-4): Suzana G. Fries and Bo Sundman. Development of multicomponent thermodynamic databases for use in process modelling and simulations. Journal of Physics and Chemistry of Solids, 66:226-230, Feb 2005. URL: https://doi.org/10.1016/j.jpcs.2004.07.026, doi:10.1016/j.jpcs.2004.07.026. This article has 6 citations and is from a peer-reviewed journal.

7. (mianiUnknownyearperspectivestudyfor pages 1-4): F Miani. Perspective study for the demonstration of the viability and usability of an xml-based standardization for calphad thermodynamic database. a design study …. Unknown journal, Unknown year.

8. (mianiUnknownyear…forthe pages 1-4): F Miani. … for the demonstration of the viability and usability of an xml-based standardization for calphad thermodynamic database. a design study based on the binary …. Unknown journal, Unknown year.

9. (walle2018thethermodynamicdatabase pages 2-3): Axel van de Walle, Chiraag Nataraj, and Zi-Kui Liu. The thermodynamic database database. Calphad, 61:173-178, Jun 2018. URL: https://doi.org/10.1016/j.calphad.2018.04.003, doi:10.1016/j.calphad.2018.04.003. This article has 52 citations.

10. (walle2018thethermodynamicdatabase pages 1-2): Axel van de Walle, Chiraag Nataraj, and Zi-Kui Liu. The thermodynamic database database. Calphad, 61:173-178, Jun 2018. URL: https://doi.org/10.1016/j.calphad.2018.04.003, doi:10.1016/j.calphad.2018.04.003. This article has 52 citations.

11. (chen2018databasedevelopmentand pages 7-10): Hai-Lin Chen, Huahai Mao, and Qing Chen. Database development and calphad calculations for high entropy alloys: challenges, strategies, and tips. Materials Chemistry and Physics, 210:279-290, May 2018. URL: https://doi.org/10.1016/j.matchemphys.2017.07.082, doi:10.1016/j.matchemphys.2017.07.082. This article has 240 citations and is from a peer-reviewed journal.

12. (kattner2016thecalphadmethod pages 11-13): Ursula R. Kattner. The calphad method and its role in material and process development. Tecnologia em metalurgia, materiais e mineracao, 13 1:3-15, Jan 2016. URL: https://doi.org/10.4322/2176-1523.1059, doi:10.4322/2176-1523.1059. This article has 235 citations.

13. (kattner2016thecalphadmethod pages 17-19): Ursula R. Kattner. The calphad method and its role in material and process development. Tecnologia em metalurgia, materiais e mineracao, 13 1:3-15, Jan 2016. URL: https://doi.org/10.4322/2176-1523.1059, doi:10.4322/2176-1523.1059. This article has 235 citations.

14. (kroupa2007thedevelopmentof pages 1-2): A. Kroupa, A. T. Dinsdale, A. Watson, J. Vrestal, J. Vízdal, and A. Zemanova. The development of the cost 531 lead-free solders thermodynamic database. JOM, 59:20-25, Jul 2007. URL: https://doi.org/10.1007/s11837-007-0084-6, doi:10.1007/s11837-007-0084-6. This article has 85 citations and is from a peer-reviewed journal.

15. (kroupa2007thedevelopmentof pages 4-5): A. Kroupa, A. T. Dinsdale, A. Watson, J. Vrestal, J. Vízdal, and A. Zemanova. The development of the cost 531 lead-free solders thermodynamic database. JOM, 59:20-25, Jul 2007. URL: https://doi.org/10.1007/s11837-007-0084-6, doi:10.1007/s11837-007-0084-6. This article has 85 citations and is from a peer-reviewed journal.

16. (walle2018thethermodynamicdatabase pages 3-5): Axel van de Walle, Chiraag Nataraj, and Zi-Kui Liu. The thermodynamic database database. Calphad, 61:173-178, Jun 2018. URL: https://doi.org/10.1016/j.calphad.2018.04.003, doi:10.1016/j.calphad.2018.04.003. This article has 52 citations.

17. (wertz2018towardmultiprincipalcomponent pages 3-4): Katelun N. Wertz, Jonathan D. Miller, and Oleg N. Senkov. Toward multi-principal component alloy discovery: assessment of calphad thermodynamic databases for prediction of novel ternary alloy systems. Journal of Materials Research, 33:3204-3217, Oct 2018. URL: https://doi.org/10.1557/jmr.2018.61, doi:10.1557/jmr.2018.61. This article has 29 citations and is from a peer-reviewed journal.

18. (ravi2005comparisonofthermodynamic pages 1-2): C. Ravi and C. Wolverton. Comparison of thermodynamic databases for 3xx and 6xxx aluminum alloys. Metallurgical and Materials Transactions A, 36:2013-2023, Aug 2005. URL: https://doi.org/10.1007/s11661-005-0322-x, doi:10.1007/s11661-005-0322-x. This article has 36 citations.

19. (ravi2005comparisonofthermodynamic pages 5-7): C. Ravi and C. Wolverton. Comparison of thermodynamic databases for 3xx and 6xxx aluminum alloys. Metallurgical and Materials Transactions A, 36:2013-2023, Aug 2005. URL: https://doi.org/10.1007/s11661-005-0322-x, doi:10.1007/s11661-005-0322-x. This article has 36 citations.

20. (ravi2005comparisonofthermodynamic pages 3-5): C. Ravi and C. Wolverton. Comparison of thermodynamic databases for 3xx and 6xxx aluminum alloys. Metallurgical and Materials Transactions A, 36:2013-2023, Aug 2005. URL: https://doi.org/10.1007/s11661-005-0322-x, doi:10.1007/s11661-005-0322-x. This article has 36 citations.

21. (ravi2005comparisonofthermodynamic pages 11-11): C. Ravi and C. Wolverton. Comparison of thermodynamic databases for 3xx and 6xxx aluminum alloys. Metallurgical and Materials Transactions A, 36:2013-2023, Aug 2005. URL: https://doi.org/10.1007/s11661-005-0322-x, doi:10.1007/s11661-005-0322-x. This article has 36 citations.

22. (wertz2018towardmultiprincipalcomponent pages 9-11): Katelun N. Wertz, Jonathan D. Miller, and Oleg N. Senkov. Toward multi-principal component alloy discovery: assessment of calphad thermodynamic databases for prediction of novel ternary alloy systems. Journal of Materials Research, 33:3204-3217, Oct 2018. URL: https://doi.org/10.1557/jmr.2018.61, doi:10.1557/jmr.2018.61. This article has 29 citations and is from a peer-reviewed journal.

23. (wertz2018towardmultiprincipalcomponent pages 11-12): Katelun N. Wertz, Jonathan D. Miller, and Oleg N. Senkov. Toward multi-principal component alloy discovery: assessment of calphad thermodynamic databases for prediction of novel ternary alloy systems. Journal of Materials Research, 33:3204-3217, Oct 2018. URL: https://doi.org/10.1557/jmr.2018.61, doi:10.1557/jmr.2018.61. This article has 29 citations and is from a peer-reviewed journal.

24. (gorsse2018aboutthereliability pages 1-3): Stéphane Gorsse and Oleg Senkov. About the reliability of calphad predictions in multicomponent systems. Entropy, 20:899, Nov 2018. URL: https://doi.org/10.3390/e20120899, doi:10.3390/e20120899. This article has 131 citations.

25. (presoly2016thermodynamicoptimizationof pages 9-9): P. Presoly, J. Six, and C. Bernhard. Thermodynamic optimization of individual steel database by means of systematic dsc measurements according the calphad approach. IOP Conference Series: Materials Science and Engineering, 119:012013, Mar 2016. URL: https://doi.org/10.1088/1757-899x/119/1/012013, doi:10.1088/1757-899x/119/1/012013. This article has 11 citations.

26. (campbell2014thedevelopmentof pages 7-9): Carelyn E Campbell, Ursula R Kattner, and Zi-Kui Liu. The development of phase-based property data using the calphad method and infrastructure needs. Integrating Materials and Manufacturing Innovation, 3:1-23, Apr 2014. URL: https://doi.org/10.1186/2193-9772-3-12, doi:10.1186/2193-9772-3-12. This article has 76 citations and is from a peer-reviewed journal.

27. (kattner2020theneedfor pages 19-20): URSULA R. KATTNER. The need for reliable data in computational thermodynamics. High temperatures - high pressures, 49 1-2:31-47, Jan 2020. URL: https://doi.org/10.32908/hthp.v49.853, doi:10.32908/hthp.v49.853. This article has 12 citations and is from a peer-reviewed journal.

28. (kattner2020theneedfor pages 1-3): URSULA R. KATTNER. The need for reliable data in computational thermodynamics. High temperatures - high pressures, 49 1-2:31-47, Jan 2020. URL: https://doi.org/10.32908/hthp.v49.853, doi:10.32908/hthp.v49.853. This article has 12 citations and is from a peer-reviewed journal.

29. (kattner2020theneedfor pages 6-8): URSULA R. KATTNER. The need for reliable data in computational thermodynamics. High temperatures - high pressures, 49 1-2:31-47, Jan 2020. URL: https://doi.org/10.32908/hthp.v49.853, doi:10.32908/hthp.v49.853. This article has 12 citations and is from a peer-reviewed journal.

30. (presoly2016thermodynamicoptimizationof pages 1-4): P. Presoly, J. Six, and C. Bernhard. Thermodynamic optimization of individual steel database by means of systematic dsc measurements according the calphad approach. IOP Conference Series: Materials Science and Engineering, 119:012013, Mar 2016. URL: https://doi.org/10.1088/1757-899x/119/1/012013, doi:10.1088/1757-899x/119/1/012013. This article has 11 citations.

31. (perrut2015thermodynamicmodelingby pages 8-9): Mikael Perrut. Thermodynamic modeling by the calphad method and its applications to innovative materials. AerospaceLab Journal, Jan 2015. URL: https://doi.org/10.12762/2015.al09-10, doi:10.12762/2015.al09-10. This article has 60 citations.

32. (campbell2014thedevelopmentof pages 5-7): Carelyn E Campbell, Ursula R Kattner, and Zi-Kui Liu. The development of phase-based property data using the calphad method and infrastructure needs. Integrating Materials and Manufacturing Innovation, 3:1-23, Apr 2014. URL: https://doi.org/10.1186/2193-9772-3-12, doi:10.1186/2193-9772-3-12. This article has 76 citations and is from a peer-reviewed journal.

33. (hackenberg2011thermodynamicsandphase pages 4-6): RE Hackenberg. Thermodynamics and phase stability-needed data requirements. Unknown journal, 2011.

34. (kattner2016thecalphadmethod pages 13-14): Ursula R. Kattner. The calphad method and its role in material and process development. Tecnologia em metalurgia, materiais e mineracao, 13 1:3-15, Jan 2016. URL: https://doi.org/10.4322/2176-1523.1059, doi:10.4322/2176-1523.1059. This article has 235 citations.

35. (schmidfetzer2007assessmenttechniquesdatabase pages 2-3): R. Schmid-Fetzer, D. Andersson, P.Y. Chevalier, L. Eleno, O. Fabrichnaya, U.R. Kattner, B. Sundman, C. Wang, A. Watson, L. Zabdyr, and M. Zinkevich. Assessment techniques, database design and software facilities for thermodynamics and diffusion. Calphad-computer Coupling of Phase Diagrams and Thermochemistry, 31:38-52, Mar 2007. URL: https://doi.org/10.1016/j.calphad.2006.02.007, doi:10.1016/j.calphad.2006.02.007. This article has 193 citations.

36. (schmidfetzer2007assessmenttechniquesdatabase pages 3-4): R. Schmid-Fetzer, D. Andersson, P.Y. Chevalier, L. Eleno, O. Fabrichnaya, U.R. Kattner, B. Sundman, C. Wang, A. Watson, L. Zabdyr, and M. Zinkevich. Assessment techniques, database design and software facilities for thermodynamics and diffusion. Calphad-computer Coupling of Phase Diagrams and Thermochemistry, 31:38-52, Mar 2007. URL: https://doi.org/10.1016/j.calphad.2006.02.007, doi:10.1016/j.calphad.2006.02.007. This article has 193 citations.

37. (sundman2015opencalphada pages 1-3): Bo Sundman, Ursula R Kattner, Mauro Palumbo, and Suzana G Fries. Opencalphad - a free thermodynamic software. Integrating Materials and Manufacturing Innovation, 4:1-15, Jan 2015. URL: https://doi.org/10.1186/s40192-014-0029-1, doi:10.1186/s40192-014-0029-1. This article has 199 citations and is from a peer-reviewed journal.

38. (bocklund2024espeiforefficient pages 1-5): Brandon Bocklund, Richard Otis, Aleksei Egorov, Abdulmonem Obaied, Irina Roslyakova, and Zi-Kui Liu. Espei for efficient thermodynamic database development, modification, and uncertainty quantification: application to cu–mg. Zentropy, pages 393-416, May 2024. URL: https://doi.org/10.1201/9781003514466-19, doi:10.1201/9781003514466-19. This article has 1 citations.

39. (bocklund2021computationaldesignof pages 54-58): B Bocklund. Computational design of additively manufactured functionally graded materials by thermodynamic modeling with uncertainty quantification. Unknown journal, 2021.

40. (bocklund2024espeiforefficient pages 5-9): Brandon Bocklund, Richard Otis, Aleksei Egorov, Abdulmonem Obaied, Irina Roslyakova, and Zi-Kui Liu. Espei for efficient thermodynamic database development, modification, and uncertainty quantification: application to cu–mg. Zentropy, pages 393-416, May 2024. URL: https://doi.org/10.1201/9781003514466-19, doi:10.1201/9781003514466-19. This article has 1 citations.

41. (bocklund2024espeiforefficient pages 13-17): Brandon Bocklund, Richard Otis, Aleksei Egorov, Abdulmonem Obaied, Irina Roslyakova, and Zi-Kui Liu. Espei for efficient thermodynamic database development, modification, and uncertainty quantification: application to cu–mg. Zentropy, pages 393-416, May 2024. URL: https://doi.org/10.1201/9781003514466-19, doi:10.1201/9781003514466-19. This article has 1 citations.

42. (bocklund2024espeiforefficient pages 17-21): Brandon Bocklund, Richard Otis, Aleksei Egorov, Abdulmonem Obaied, Irina Roslyakova, and Zi-Kui Liu. Espei for efficient thermodynamic database development, modification, and uncertainty quantification: application to cu–mg. Zentropy, pages 393-416, May 2024. URL: https://doi.org/10.1201/9781003514466-19, doi:10.1201/9781003514466-19. This article has 1 citations.

43. (olson2024genomicmaterialsdesign pages 29-34): G.B. Olson and Z.K. Liu. Genomic materials design: calculation of phase dynamics. Calphad, 82:102590, Sep 2024. URL: https://doi.org/10.1016/j.calphad.2023.102590, doi:10.1016/j.calphad.2023.102590. This article has 27 citations.