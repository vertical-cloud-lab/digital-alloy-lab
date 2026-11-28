# Browser search log (issue #254, second round)

Searches typed into headed Chrome on the runner's virtual display, with its traffic tunnelled through a lab Raspberry Pi so it left from BYU's network (AS6510). For each search, xdotool moved the mouse to the site's search box, clicked it, typed the query and pressed Enter, then scrolled with the mouse wheel. Page text was read through Chrome DevTools. Run on 2026-11-28 between 08:52 and 09:34 UTC with byu-vcl's pinned `rig.sh` and a small driver script (kept in `/tmp`, not committed). The lists below give the first results on each page, in the order shown, unfiltered; the synthesis says which ones mattered.

- **Google Scholar:** blocked again. On the first page load, before any query was typed, it showed its "unusual traffic from your computer network" page with a CAPTCHA. No attempt was made to get past it, and no Scholar results are included.
- **NASA NTRS** uses AND matching, so one long query returned nothing; it is listed as such. Two NTRS queries had to be re-run because the results list had not rendered when the page was read.
- **Semantic Scholar's API** returned HTTP 429 from the runner, so abstracts were read from the paper pages in the Pi browser (clicking the abstract's *Expand* control) or from OpenAlex.


### Semantic Scholar: "creep laser powder bed fusion aluminum alloy 300 C" (250 results)

1. On the Enhanced Creep Performance in Ti6246 Achieved Through Laser Powder Bed Fusion (LPBF) Processing
1. Microstructural Evolution of a High-Strength Zr-Ti-Modified 2139 Aluminum Alloy for Laser Powder Bed Fusion
1. Aluminum–Calcium Alloy for Laser Powder Bed Fusion
1. Densification, microstructure, mechanical properties, and thermal stability of high-strength Ti-modified Al-Si-Mg-Zr aluminum alloy fabricated by laser-powder bed fusion
1. Heat treatment response and mechanical properties of a Zr-modified AA2618 aluminum alloy fabricated by laser powder bed fusion
1. Fatigue crack propagation and fracture toughness of AlSi10Mg alloy processed by powder bed fusion: effects of post-processing heat treatments
1. A High-Strength TiB2-Modified Al–Si–Mg–Zr Alloy Fabricated by Laser Powder-Bed Fusion
1. Effect of Powder Spreading Parameters on Laser Absorption Behavior and Processability of High‐Strength Aluminum Alloy Fabricated by Laser Powder Bed Fusion


### Semantic Scholar: "Al-Ce alloy additive manufacturing elevated temperature tensile" (About 1,710 results)

1. Microstructure and properties of a high temperature Al–Ce–Mn alloy produced by additive manufacturing
1. Additive manufacturing of crack-free Al-alloy with coarsening-resistant τ1-CeAlSi strengthening phase
1. Elevated temperature characterization of electron beam freeform fabricated Ti–6Al–4V and dispersion strengthened Ti–8Al–1Er
1. Elevated-Temperature Tensile Behavior and Properties of Inconel 718 Fabricated by In-Envelope Additive–Subtractive Hybrid Manufacturing and Post-Process Precipitation Hardening
1. Elevated temperature tensile and fracture behavior of Ti-6Al-4 V alloy fabricated by wire-based laser additive manufacturing: Microstructural evolution and deformation mechanism
1. Elevated temperature tensile behaviour of 5183 aluminium alloy made by electrospark deposition additive manufacturing
1. A Novel Approach for Enhanced Mechanical Properties in Solid-State Additive Manufacturing by Additive Friction Stir Deposition Using Thermally Stable Al-Ce-Mg Alloy
1. Additively manufactured Al-Ce-Ni-Mn alloy with improved elevated-temperature fatigue resistance


### Semantic Scholar: "AlSi10Mg elevated temperature tensile properties 200 300 C selective laser melting" (137 results)

1. Microstructure and Mechanical Properties of a Novel Lightweight and Heat-Resistant Al-3.0Ce-0.9Ca-1.9Mn-1.2Zr Alloy Fabricated by Selective Laser Melting
1. Investigation of High-Temperature Tensile Properties and Fracture Mechanisms of GH3536 Alloy Fabricated by Selective Laser Melting
1. Relationship between Anisotropic Stress Rupture Properties at High Temperature and Microstructure of Selective Laser Melting Mar‐M247 Alloy
1. Microstructure evolution and mechanical properties at high temperature of selective laser melted AlSi10Mg
1. Optimizing Selective Laser Melting of a High-Alloyed Ni-Based Superalloy: Achieving Crack-Free Fabrication with Enhanced Microstructure and Mechanical Properties
1. Rate-Dependent and Temperature-Sensitive Behavior of Selective Laser Melting 316L Stainless Steel: Dynamic Impact Modeling of a Hat-Shaped Specimen
1. Experimental and Statistical Analysis of the Effect of Heat Treatment on Surface Roughness and Mechanical Properties of Thin-Walled Samples Obtained by Selective Laser Melting from the Material…
1. Effect of NiTi and heat treatment on the microstructure and mechanical properties of AlSi10Mg alloy fabricated by selective laser melting


### Semantic Scholar: "2618 aluminum alloy creep thermal exposure supersonic" (42 results)

1. Effect of Thermal Exposure on Mechanical Properties of Al-Si-Cu-Ni-Mg Aluminum Alloy
1. Microstructural Changes and Thermal Stability of A201, 319s and 2618 Aluminum Alloys during Thermal Exposure
1. MECHANICAL PROPERTIES OF 2618 ALUMINUM ALLOY
1. Microstructure, Thermal Stability during Creep and Fractography Study of Friction-Stir-Processed AA2024-T3 Aluminum Alloy
1. Towards Application of Aluminum Alloy 6082 For Harsh Environment Sensing in Oil and Gas Installations: An Empirical Model for Low Temperature Creep
1. Effect of Thermal Exposure on the Tensile Properties of Aluminum Alloys for Elevated Temperature Service
1. A 2xxx aluminum alloy crept at medium temperature: role of thermal activation on dislocation mechanisms
1. Press-and-sinter processing of a PM counterpart to wrought aluminum 2618


### Semantic Scholar: "AlSi10Mg split Hopkinson bar high strain rate" (About 7,130 results)

1. Role of hierarchical microstructure of additively manufactured AlSi10Mg on dynamic loading behavior
1. Influence of Selective Laser Melting Machine Source on the Dynamic Properties of AlSi10Mg Alloy
1. MODELING THE DYNAMIC MECHANICAL BEHAVIOUR AND TEXTURE EVOLUTION OF ADDITIVELY MANUFACTURED AlSi10Mg_200C
1. High Strain Rate Response of Sandstones with Different Porosity under Dynamic Loading Using Split Hopkinson Pressure Bar (SHPB)
1. High strain rate compressive strength behavior of cemented paste backfill using split Hopkinson pressure bar
1. Strain rate effect of concrete based on split Hopkinson pressure bar (SHPB) test
1. Numerical simulation of AA7075 under high strain rate with different shape of striker of split Hopkinson Pressure bar
1. High Strain Rate Response of Rocks Under Dynamic Loading Using Split Hopkinson Pressure Bar


### Semantic Scholar: "strain rate sensitivity selective laser melted aluminum quasi-static" (51 results)

1. Thermal compression behavior and microstructural evolution of selective laser melted AlMgScZr high-strength aluminum alloys
1. Strain rate sensitivity and mechanical anisotropy of selective laser melted 17-4 PH stainless steel
1. Rate-Dependent and Temperature-Sensitive Behavior of Selective Laser Melting 316L Stainless Steel: Dynamic Impact Modeling of a Hat-Shaped Specimen
1. Influence of Post Deposition Heat Treatments on Tensile Strain Rate Effects for Selective Laser Melting (SLM) Inconel 718
1. High Strain Rate Compressive Behaviour of Selective Laser Melted Ti-6Al-4V
1. On the effects of build orientation, strain rate sensitivity and sample thickness on the mechanical behavior of 316l Stainless Steel manufactured by Selective Laser Melting
1. Investigation into the dynamic mechanical properties of selective laser melted Ti-6Al-4V alloy at high strain rate tensile loading
1. Strain rate sensitivity and fracture mechanism of AlSi10Mg parts produced by Selective Laser Melting


### Semantic Scholar: "Scalmalloy high temperature mechanical properties" (About 129,000 results)

1. Heat Treatment Post-Processing for the Improved Mechanical Properties of Scalmalloy® Processed via Directed Energy Deposition
1. Research on the mechanical properties of PEEK material artificial bone implants fabricated by high-temperature air-assisted 3D printing.
1. Influence of Mo on Microstructure and High-Temperature Mechanical Properties of Fire-Resistant Steels
1. High-temperature mechanical properties evaluation of 310S stainless steel
1. Mechanical properties measurement of chromium coatings based on laser ultrasonic technology in high-temperature conditions
1. High-Temperature Oxidation Behavior of Pt-10Rh-Zr(Y) Alloys and its Influence on their Mechanical Properties
1. Study on the mechanical properties of rice husk ash-based geopolymer-regenerated mortar reinforced by polyimide fiber and carbon fiber after high-temperature exposure
1. Effect of high-temperature thermomechanical treatment modes on change of physical and mechanical properties of reinforcing steels


### Semantic Scholar: "small punch test additively manufactured aluminum alloy" (About 1,590 results)

1. Mechanical properties assessment of additively manufactured Ti64 alloy using small punch tests
1. Constitutive modeling of the hot deformation behavior of additively manufactured AlSi10Mg aluminum alloy
1. Prediction of fracture behavior during the small punch test for aluminum alloy 6061
1. Pre-qualification of additively manufactured 316L stainless steel using small punch and uniaxial creep testing
1. Martensite Decomposition and Ultrafine Grain Formation during Small Punch Creep Testing of Additively Manufactured Ti64
1. Local mechanical properties of thin sheet AA6061 aluminum alloy friction stir welds evaluated by Small Punch Test (SPT)
1. Creep Behavior of Additively Manufactured High Strength A205 Aluminum Alloy
1. Experimental evaluation of fracture properties of aluminum alloy 1050-H14 by small punch test


### Semantic Scholar: "profilometry-based indentation plastometry aluminium" (41 results)

1. Mechanical Characterization by Profilometry-Based Indentation Plastometry of Locally Heat-Treated Blanks for Sheet Injection Applications
1. Low-Pressure Die Casting of Aluminium Alloy Components for Electric Vehicle Battery Enclosures
1. Effects of Creep in Titanium at Room Temperature during Tensile and Profilometry‐Based Indentation Plastometry Testing
1. Profilometry‐Based Indentation Plastometry Testing of Tungsten at High Temperature
1. Validation of Profilometry‐Based Indentation Plastometry (PIP) Testing for Rapid Qualification of Electron Beam‐Powder Bed Fusion (EB‐PBF) With Ti–6Al–4V Builds
1. Comparison of Stress–Strain Properties from Profilometry-Based Indentation Plastometry (PIP) and Conventional Tensile Testing
1. Profilometry-based indentation plastometry (PIP) integrated finite element (FE) model validation using neutron diffraction
1. Source-Separated Uncertainty Quantification in the Stochastic Plasticity of Cold-Sprayed Al 7075 Using Profilometry-Based Indentation Plastometry and Residual Analysis


### Semantic Scholar: "fatigue laser powder bed fusion AlSi10Mg surface roughness HIP machined" (136 results)

1. Fatigue life of laser powder bed fusion (L-PBF) AlSi10Mg alloy: effects of surface roughness and porosity
1. Fatigue Performance of Additively Manufactured Ti‐6Al‐4V: Impact of Different Kinds of Porosities, Surface, and Heat Treatments in Laser Powder Bed Fusion Productivity Parameters
1. Effect of surface roughness on rotating fatigue strength of as-built AlSi10Mg produced by laser powder bed fusion
1. Microstructural effects on the rotating bending fatigue behavior of Ti-6Al-4V produced via laser powder bed fusion with novel heat treatments
1. The efficiency of tumble finishing as a final post-treatment for fatigue enhancement of notched laser powder bed fusion AlSi10Mg
1. Enhancing Fatigue Life of Metal Parts Produced by High-Speed Laser Powder Bed Fusion Through In Situ Surface Quality Improvement
1. Fatigue crack nucleation and growth in laser powder bed fusion AlSi10Mg under as built and post-treated conditions
1. Killer notches: The effect of as-built surface roughness on fatigue failure in AlSi10Mg produced by laser powder bed fusion


### Semantic Scholar: "Johnson-Cook parameters 2024-T3 aluminum high strain rate" (About 1,650 results)

1. AN IMPROVED METHOD TO MORE ACCURATELY ASSESS THE JOHNSON-COOK HIGH STRAIN-RATE DEFORMATION MATERIAL MODEL PARAMETERS - PART I
1. The modified Johnson-Cook constitutive model of 2A10 aluminum alloys under electromagnetic impact loading
1. Determination and Verification of the Johnson–Cook Constitutive Model Parameters in the Precision Machining of Ti6Al4V Alloy
1. Sensitivity Analysis of the Johnson-Cook Model for Ti-6Al-4V in Aeroengine Applications
1. Parametric Analysis and Improvement of the Johnson-Cook Model for a TC4 Titanium Alloy
1. Experimental Determination and Simulation Validation: Johnson–Cook Model Parameters and Grinding Simulation of 06Cr18Ni11Ti Stainless Steel Welds
1. Identification of material parameters at high strain rates using ballistic impact tests and inverse finite element analysis
1. Assessing Feed-Forward Backpropagation Artificial Neural Networks for Strain-Rate-Sensitive Mechanical Modeling


### Semantic Scholar: "high temperature aluminum alloy additive manufacturing creep cerium" (614 results)

1. High-temperature tensile behaviors of an ultra-strong aluminum alloy fabricated by additive manufacturing
1. Optimization of Process Parameters to Minimize Porosity and Splash in Cold Metal Transfer and Pulse Wire Arc Additive Manufacturing of High‐Strength Aluminum Alloy
1. The Influence of the Composite Process of Sand Mold Additive Manufacturing and Low-Temperature Treatment on the Macro- and Micro-Properties of A356 Aluminum Alloy for Aircraft Thin-Walled Cabins
1. A review of additive manufacturing heat-resistant aluminum alloys: Materials, properties and strengthening strategies at high temperature
1. Design of high-performance sustainable aluminum alloy series for laser additive manufacturing
1. Strong yet ductile heat-resistant aluminum alloy by additive manufacturing
1. Numerical Simulation of Arc Characteristics of VP-CMT Aluminum Alloy Arc Additive Manufacturing
1. SIMULATION OF THE PROPERTIES OF A357 ALUMINUM ALLOY IN SEMI-SOLID STATE FOR EXTRUSION ADDITIVE MANUFACTURING OF METAL


### NASA NTRS: "High Speed Research aluminum alloy thermal exposure"

1. Effect of Thermal Exposure on the Tensile Properties of Aluminum Alloys for Elevated Temperature Service ([NTRS 20040047195](https://ntrs.nasa.gov/citations/20040047195))


### NASA NTRS: "elevated temperature aluminum alloy creep supersonic transport"

No results listed (the site returned none for this query).


### NASA NTRS: "additive manufacturing aluminum high temperature"

1. Reaction Synthesis Feedstocks for Additive Manufacturing ([NTRS 20200003560](https://ntrs.nasa.gov/citations/20200003560))
1. Maturation of Additive Manufactured Aerospace Alloys and Development of Mechanical and Thermophysical Properties for Space Applications ([NTRS 20220016247](https://ntrs.nasa.gov/citations/20220016247))
1. Fatigue Life of Flow-Formed Aluminum 2195 and 6061 Alloys ([NTRS 20260001601](https://ntrs.nasa.gov/citations/20260001601))
1. Hot Cracking Behavior and Beam-Induced Grain Refinement in Electron Beam Freeform Fabricated Al 7075 ([NTRS 20230005342](https://ntrs.nasa.gov/citations/20230005342))
1. Advancement of Extreme Environment Additively Manufactured Alloys for Next Generation Space Propulsion Applications ([NTRS 20220013950](https://ntrs.nasa.gov/citations/20220013950))
1. MSFC Manufacturing ([NTRS 20260011001](https://ntrs.nasa.gov/citations/20260011001))
1. Thermal Inspection of Low Emissivity Surfaces Using a Pulsed Light Emitting Diodes (PLED) Heat Source ([NTRS 20240003960](https://ntrs.nasa.gov/citations/20240003960))
1. Open-source Numerical Modeling of Solidification Cracking Susceptibility: Application to Refractory Alloy Systems ([NTRS 20230012726](https://ntrs.nasa.gov/citations/20230012726))


### NASA NTRS: "Johnson-Cook aluminum 2024"

1. Impact and Penetration of Thin Aluminum 2024 Flat Panels at Oblique Angles of Incidence ([NTRS 20160000816](https://ntrs.nasa.gov/citations/20160000816))


### NASA NTRS: "aluminum alloy 2618 elevated temperature"

1. Elevated temperature crack growth in aluminum alloys: Tensile deformation of 2618 and FVS0812 aluminum alloys ([NTRS 19900013338](https://ntrs.nasa.gov/citations/19900013338))
1. Tensile deformation of 2618 and Al-Fe-Si-V aluminum alloys at elevated temperatures ([NTRS 19910029640](https://ntrs.nasa.gov/citations/19910029640))


### OSTI.GOV: "Al-Ce alloy additive manufacturing high temperature creep"

1. Additively-manufactured Al-0.3Zr-0.2Ce-0.2Cu alloy with high creep resistance and electrical conductivity ([OSTI 3009459](https://www.osti.gov/biblio/3009459))
1. Influence of microstructural heterogeneities on small-scale mechanical properties of an additively manufactured Al-Ce-Ni-Mn alloy ([OSTI 1959627](https://www.osti.gov/biblio/1959627))
1. Evaluation of high-temperature properties of binary, eutectic Ni-X alloys (X = B, Ca, Ce, La, Y, Zr) ([OSTI 3682492](https://www.osti.gov/biblio/3682492))
1. Mechanical behavior of ultrahigh strength aluminum alloys ([OSTI 17428371](https://www.osti.gov/biblio/17428371))
1. Coarsening- and creep behavior of supersaturated Al-Zr-X (X = Mn, Cr, V, Mo, W) alloys processed by laser powder-bed fusion ([OSTI 17315112](https://www.osti.gov/biblio/17315112))
1. Optimization of Processing, Microstructure, and Hardness of an Al–Ce–Ni–Mn–Zr Alloy With Laser Additive Manufacturing ([OSTI 3252736](https://www.osti.gov/biblio/3252736))
1. Mechanical behaviour of additively manufactured metals ([OSTI 3013534](https://www.osti.gov/biblio/3013534))
1. Strain-rate hardening enhances fatigue resistance of AlSi10Mg alloy at 350°C ([OSTI 3030499](https://www.osti.gov/biblio/3030499))


### OSTI.GOV: "Al-Cu-Mn-Zr ACMZ alloy elevated temperature"

1. Grain Refinement Effect on the Hot-Tearing Resistance of Higher-Temperature Al–Cu–Mn–Zr Alloys ([OSTI 1608199](https://www.osti.gov/biblio/1608199))
1. Low-Mass and High-Efficiency Engine for Medium-Duty Truck Applications ([OSTI 2586587](https://www.osti.gov/biblio/2586587))
1. Corrosion evaluation of Al-Cu-Mn-Zr cast alloys in 3.5% NaCl solution ([OSTI 2476704](https://www.osti.gov/biblio/2476704))
1. Co-, Ni- and Fe-rich grain-boundary phases enhance creep resistance in θ'-strengthened Al-Cu alloys ([OSTI 2438901](https://www.osti.gov/biblio/2438901))
1. The many faces of θ'-Al2Cu precipitates: Energetics of pristine and solute segregated Al/θ' semi-coherent interfaces ([OSTI 2474760](https://www.osti.gov/biblio/2474760))
1. 2024 Annual Merit Review - Vehicle Technologies Office: Results Report ([OSTI 3010237](https://www.osti.gov/biblio/3010237))
1. Progression of creep deformation from grain boundaries to grain interior in Al-Cu-Mn-Zr alloys ([OSTI 1968690](https://www.osti.gov/biblio/1968690))
1. Decarbonization of Off-Road, Rail, Marine, and Aviation (DORMA) Program (2023 Annual Progress Report) ([OSTI 3010220](https://www.osti.gov/biblio/3010220))


### OSTI.GOV: "AlSi10Mg fatigue 350 C ultrasonic"

1. Strain-rate hardening enhances fatigue resistance of AlSi10Mg alloy at 350°C ([OSTI 3030499](https://www.osti.gov/biblio/3030499))
1. X-ray tomography of damage dynamics in advanced materials using a laser wakefield accelerator ([OSTI 3685178](https://www.osti.gov/biblio/3685178))
1. A critical review on additive manufacturing of refractory alloys from a data analytics perspective- beyond nickel-based superalloys ([OSTI 3015568](https://www.osti.gov/biblio/3015568))
1. Fatigue life prediction of powder bed fused–laser beam AlSi10Mg: Incorporating critical defects via crystal plasticity modelling ([OSTI 2940375](https://www.osti.gov/biblio/2940375))
1. A high strength Al-2Ni-0.5Zr conductor alloy fabricated via laser powder bed fusion ([OSTI 3002432](https://www.osti.gov/biblio/3002432))
1. Advances in high-pressure and high-temperature heat exchangers: Innovations via additive manufacturing and their applications ([OSTI 2572165](https://www.osti.gov/biblio/2572165))
1. Simulated effect of defect volume and location on very high cycle fatigue of laser beam powder bed fused AlSi10Mg ([OSTI 2529491](https://www.osti.gov/biblio/2529491))
1. Effect of Zr and Sc additions on coarsening- and creep resistance of AlSi10Mg fabricated by laser powder bed fusion ([OSTI 2537975](https://www.osti.gov/biblio/2537975))


### Pages opened in the same browser

Each was opened by typing its address into the omnibox with xdotool; for Semantic Scholar pages the abstract's *Expand* control was clicked with the mouse. Springer pages showed BYU library access.

- [Heat treatment response and mechanical properties of a Zr-modified AA2618 aluminum alloy fabricated by laser powder bed fusion](https://www.semanticscholar.org/paper/Heat-treatment-response-and-mechanical-properties-a-Schuster-Luca/101025a718cf17fbf85616fb6c638972a6df5516)
- [Coarsening- and Creep-Resistant, Fine-grained Al-Ni-Fe-Zr Eutectic Alloy by Laser Powder-Bed Fusion](https://www.semanticscholar.org/paper/Coarsening-and-Creep-Resistant%2C-Fine-grained-Alloy-Dorn-Park/b877269645e5f0bc4f702873916e83e3dbf7bd5f)
- [Microstructure and properties of a high temperature Al–Ce–Mn alloy produced by additive manufacturing](https://www.semanticscholar.org/paper/Microstructure-and-properties-of-a-high-temperature-Plotkowski-Sisco/5bf7670b076c5d758cc5aaeb4b699c47a649ad52)
- [Additively manufactured Al-Ce-Ni-Mn alloy with improved elevated-temperature fatigue resistance](https://www.semanticscholar.org/paper/Additively-manufactured-Al-Ce-Ni-Mn-alloy-with-Michi-Simpson/5c3f0fd1cba857fdf9e4e8b4bb6cb99f6e76d11c)
- [Microstructure evolution and mechanical properties at high temperature of selective laser melted AlSi10Mg](https://www.semanticscholar.org/paper/Microstructure-evolution-and-mechanical-properties-Cao-Lin/4cc1d7bf508c88ca285947ab18246d71177f873e)
- [Role of hierarchical microstructure of additively manufactured AlSi10Mg on dynamic loading behavior](https://www.semanticscholar.org/paper/Role-of-hierarchical-microstructure-of-additively-Hadadzadeh-Amirkhiz/3cb397d34904ef7de5d34e46f715bbacddeeb767)
- [Strain rate sensitivity and fracture mechanism of AlSi10Mg parts produced by Selective Laser Melting](https://www.semanticscholar.org/paper/Strain-rate-sensitivity-and-fracture-mechanism-of-Rosenthal-Stern/8ebffd571ef3b1153725dfc2de2215386993ed21)
- [Creep Behavior of Additively Manufactured High Strength A205 Aluminum Alloy](https://www.semanticscholar.org/paper/Creep-Behavior-of-Additively-Manufactured-High-A205-Kulkarni-Srinivasan/124a0c21b987db4f2241d2d30b8c949e28c3569f)
- [Profilometry‐Based Indentation Plastometry Testing of Tungsten at High Temperature](https://www.semanticscholar.org/paper/Profilometry%E2%80%90Based-Indentation-Plastometry-Testing-Miller-McKeown/d6eaf7e00b5d4ecfd0644f1bda8c157362e31605)
- [Comparison of Stress–Strain Properties from Profilometry-Based Indentation Plastometry (PIP) and Conventional Tensile Testing](https://www.semanticscholar.org/paper/Comparison-of-Stress%E2%80%93Strain-Properties-from-(PIP)-Poorganji-Castillo/e01196c9e2daccb1c20c5f05872cfb92e8b7ea05)
- [Profilometry‐Based Indentation Plastometry at High Temperature](https://www.semanticscholar.org/paper/Profilometry%E2%80%90Based-Indentation-Plastometry-at-High-Tammpere-McKeown/bd3b73da11ae4af848ed3f188443873237466527)
- [Profilometry‐Based Indentation Plastometry and Uniaxial Testing of Pipelines: Detection of In‐Plane Anisotropy and Potential for Simplification of Test Procedures](https://www.semanticscholar.org/paper/Profilometry%E2%80%90Based-Indentation-Plastometry-and-of-Vaka-Warwick/67ea00888bbe49ae915ec0e797d2b7bd605fdd4a)
- [Killer notches: The effect of as-built surface roughness on fatigue failure in AlSi10Mg produced by laser powder bed fusion](https://www.semanticscholar.org/paper/Killer-notches%3A-The-effect-of-as-built-surface-on-Plessis-Beretta/4cca3dde8d2cbd6ed6ec213c3339bb42ab7a5c4a)
- [Strain-rate hardening enhances fatigue resistance of AlSi10Mg alloy at 350°C](https://www.osti.gov/biblio/3030499)
- [Creep ductility limiting mechanisms in an additively manufactured Al-Ce-Ni-Mn-Zr alloy](https://www.osti.gov/biblio/3009477)
- [Coarsening- and creep behavior of supersaturated Al-Zr-X (X = Mn, Cr, V, Mo, W) alloys processed by laser powder-bed fusion](https://www.osti.gov/biblio/17315112)
- [Effect of Thermal Exposure on the Tensile Properties of Aluminum Alloys for Elevated Temperature Service](https://ntrs.nasa.gov/citations/20040047195)
- [Tensile deformation of 2618 and Al-Fe-Si-V aluminum alloys at elevated temperatures](https://ntrs.nasa.gov/citations/19910029640)
- [Direct Impact Split-Hopkinson Bar Experiment for Compression Testing at Strain Rate of 50,000 S-1](https://ntrs.nasa.gov/citations/20240014937)
- [High-Temperature Mechanical Properties of Stress-Relieved AlSi10Mg Produced via Laser Powder Bed Fusion Additive Manufacturing](https://www.mdpi.com/1996-1944/15/20/7386)
- [Study on Microstructure and High-Temperature Mechanical Properties of Al-Mg-Sc-Zr Alloy Processed by LPBF](https://www.mdpi.com/2075-4701/14/8/890)
- [High Strength Aluminum Additive Manufacturing](https://www.osti.gov/biblio/2301648)
- [Additively manufacturing high-temperature aluminum alloy for automotive engine pistons](https://www.osti.gov/biblio/2573209)
- [Strain Rate Sensitivity of the Additive Manufacturing Material Scalmalloy®](https://link.springer.com/article/10.1007/s40870-021-00298-4)
- [Microstructural Variations in Laser Powder Bed Fused Al–15%Fe Alloy at Intermediate Temperatures](https://www.mdpi.com/1996-1944/15/13/4497)
- [Creep properties of heat-resistant ultrafine-grained Al (HITEMAL©) determined by small punch testing](https://link.springer.com/article/10.1007/s10853-024-10139-z)
- [SAE AMS7003, Laser Powder Bed Fusion Process](https://www.sae.org/standards/ams7003-laser-powder-bed-fusion-process/) (the page body did not render; the redirect address gives the title)
- [ASTM B871, Standard Test Method for Tear Testing of Aluminum Alloy Products (Withdrawn 2017)](https://store.astm.org/b0871-01r13.html)

### Screenshots

Two full-display captures from the virtual display (1920×1080), showing the headed browser after an xdotool-typed search:

- [`browser-screenshots/semantic-scholar-high-temperature-am-aluminum-creep-cerium.png`](browser-screenshots/semantic-scholar-high-temperature-am-aluminum-creep-cerium.png)
- [`browser-screenshots/osti-alsi10mg-fatigue-350c.png`](browser-screenshots/osti-alsi10mg-fatigue-350c.png)
