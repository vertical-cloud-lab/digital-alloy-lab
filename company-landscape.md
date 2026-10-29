# Company Landscape: Digital Alloy Discovery & Additive Manufacturing

This document identifies companies involved in the autonomous alloy discovery, high-throughput additive manufacturing, and AI-accelerated materials development space. Companies are categorized by role in the VCL pipeline, maturity, geography, and **Genesis Mission partnership potential** (DOE DE-FOA-0003612, Topic 3B: Critical Minerals, AMMTO). Includes companies relevant to critical mineral substitution, Be-Cu replacement, and supply chain resilience.

> **Sources:** All PRs in this repository (#2–#14, #26 for Topic 3B context), Edison trajectory analyses (including 3 dedicated Edison Scientific LITERATURE_HIGH queries on powder atomization, alloy design software, and LPBF/characterization equipment — results in `edison-trajectories/companies_*.md`), [RAPID+TCT 2026](https://www.rapid3devent.com/) exhibitor directory and conference schedule (April 13–16, 2026, Boston, MA; Edison review in `edison-trajectories/companies_rapid2026_review.md`), alloy-workflow-review.md, grant-targeting-analysis.md, DOE Critical Materials Innovation Hub partner lists, USGS 2025 Critical Minerals List, and supplementary web research.

---

## 1. Powder Production & Atomization

| Company | HQ | Founded | Stage | What They Do | VCL Relevance | Genesis Mission Fit |
|---|---|---|---|---|---|---|
| **[Amazemet](https://www.amazemet.com/)** | Warsaw, Poland | — | Startup | Ultrasonic atomization (rePOWDER); AI-driven autonomous powder production; atomization-as-a-service from €1K/50g | **Active PoC partner.** Samples shipped Feb 2026. Solves the critical powder bottleneck. University partnerships with TUM, RWTH Aachen. Unveiled AI-controlled rePOWDER at Formnext 2025. | ★★★★★ — Strong Genesis Mission partner: startup, active collaboration, directly enables VCL's core differentiator. Non-US but letter of collaboration possible. |
| **[Elementum 3D](https://www.elementum3d.com/)** | Thornton, CO, USA | 2014 | Growth-stage startup | Patented Reactive Additive Manufacturing (RAM) powder technology; novel printable alloys (Al 6061, 7075, Cu, Ni); NASA & USAF partnerships | Potential powder supplier for difficult-to-print alloy compositions. America Makes member. Colorado School of Mines collaboration on solidification modeling. Sumitomo investment. | ★★★★★ — US-based startup with defense ties, proven academic collaborations, and directly relevant technology. Strong Genesis Mission partner. |
| **[Höganäs AB](https://www.hoganas.com/)** | Höganäs, Sweden | 1797 | Established | World's largest metal powder producer; gas and water atomized powders for AM | Standard commercial powder supplier. Broad alloy portfolio but not focused on custom small-batch R&D quantities. | ★★ — Too large/established for typical partnerships; could be unfunded collaborator. |
| **[AP&C (GE Additive)](https://www.advancedpowders.com/)** | Montreal, Canada | 2000 | Established (GE subsidiary) | Plasma atomization for spherical Ti, Ni, and specialty powders | High-quality spherical powder supplier for aerospace alloys. Owned by GE Additive since 2018. | ★ — Corporate subsidiary; limited Genesis Mission fit. |
| **[Tekna](https://www.tekna.com/)** | Sherbrooke, QC, Canada | 1990 | Established | Plasma atomization and spheroidization; Ti, Ni, Al, and refractory powders | Alternative high-quality powder source for specialty alloys. | ★ — Large established company. |
| **[Equispheres](https://www.equispheres.com/)** | Ottawa, ON, Canada | 2015 | Growth-stage startup | Proprietary atomization for ultra-narrow PSD Al powders optimized for AM; partnerships with Aconity3D, AddUp | Specialized Al powder producer with narrow particle-size distributions tailored for LPBF. Could supply optimized Al feedstock. | ★★★ — Non-US startup; IRES/international supplement route possible. |
| **[Uniformity Labs](https://uniformitylabs.com/)** | Fremont, CA, USA | 2014 | Growth-stage startup | Proprietary powder optimization and Al alloy development for AM; patented packing algorithms | US-based Al-focused powder innovator. Could partner on powder characterization or supply. | ★★★★ — US startup, directly relevant to Al alloy AM work. |
| **[Solid State Metal](https://www.solidmetal.tech/)** | USA (Pacific Northwest) | — | Early-stage startup | Cleantech: solid-state manufacturing converts scrap metal into wire feedstocks for DED/WAAM; circular economy / sustainable metal supply chain | Produces wire feedstock (not LPBF powder), but represents emerging solid-state approach to AM feedstock from recycled scrap. Linked to PNNL solid-phase processing research (ShAPE). Relevant if VCL expands to DED or hybrid AM. | ★★★ — US startup; early stage; wire-based feedstock adjacent to VCL's powder-based pipeline but relevant to broader AM ecosystem. |
| **[6K Additive](https://6kadditive.com/)** | Burgettstown, PA, USA | 2017 | Growth-stage startup | UniMelt® microwave plasma powder production; converts scrap/recycled metal into AM-ready powder; 91% lower emissions vs. conventional; Siemens Energy recycling partnership (20 tons processed); DOE $107M grant for Tennessee facility | Unique circular-economy powder producer. US-based with defense and sustainability focus. Potential supplier of recycled Ni/Ti/Al powders. Exhibitor at RAPID+TCT 2026 (#1643). | ★★★★ — US startup with DOE backing, circular economy angle, defense relevance. Strong Genesis Mission partner for sustainable powder supply. |

### Atomization Equipment OEMs (Edison Scientific)

The following companies manufacture atomization *equipment* (as opposed to selling powder only). Identified via Edison Scientific LITERATURE_HIGH queries with peer-reviewed citations.

| Company | HQ | Stage | What They Do | VCL Relevance |
|---|---|---|---|---|
| **[ALD Vacuum Technologies](https://www.ald-vt.com/)** | Hanau, Germany | Established | World leader in gas atomization equipment (VIGA, EIGA); lab models (1–2 L) to industrial (250 L); part of AMG N.V. | Could supply lab-scale VIGA atomizer for VCL gas atomization capability. VIGA lab models produce 15–60 µm powders. |
| **[Phoenix Scientific Industries (PSI)](https://www.psiltd.co.uk/)** | Hailsham, UK | Established | Hermiga series gas atomizers (3–200 kg capacity); spherical powders with 10³–10⁶ K/s cooling rates | Lab-scale Hermiga 75/3 (3 kg) suitable for research. Produces 10–100 µm particles. |
| **[Atomising Systems Ltd (ASL)](https://www.atomising.co.uk/)** | Sheffield, UK | Established | Multi-technology atomizers (ultrasonic, gas, water, centrifugal); lab (1–5 kg/day) to industrial (>5 t/day) | One of only 3 European atomizer OEMs; offers ultrasonic atomization alongside gas. |
| **[Arcast Inc.](https://www.arcastinc.com/)** | Oxford, ME, USA | Established | Vacuum arc furnaces and gas atomization equipment | US-based atomizer OEM; research-grade equipment. |
| **[PyroGenesis Canada](https://www.pyrogenesis.com/)** | Montreal, QC, Canada | Established (1991) | NexGen plasma atomization systems; invented the plasma torch technology used by AP&C | Plasma atomization OEM. Publicly traded (TSX: PYR). |
| **[TLS Technik](https://www.tls-technik.de/)** | Bitterfeld, Germany | Established | EIGA titanium powder specialist | Niche Ti powder producer via EIGA. |

### Additional Powder Producers (Edison Scientific)

| Company | HQ | Stage | What They Do |
|---|---|---|---|
| **Carpenter Technology** | Philadelphia, PA, USA | Established (1889) | Gas atomized metal powders (CarTech); broad alloy portfolio |
| **GKN Hoeganaes** | Cinnaminson, NJ, USA | Established | Gas atomized AM powders (AncorAM product line) |
| **Sandvik Osprey** | Neath, UK (Sandvik parent) | Established | Gas atomized powders (Osprey® process); licensed tech to ALD |
| **ATI (Allegheny Technologies)** | Dallas, TX, USA | Established | Titanium gas atomization; aerospace/defense focus |
| **Praxair / Linde** | Danbury, CT, USA | Established | Titanium gas atomization |
| **H.C. Starck** | Goslar, Germany | Established | Refractory metal powders (Ta, Nb, Mo, W) |

---

## 2. LPBF / Metal AM Equipment

### Established OEMs

| Company | HQ | Stage | What They Do | VCL Relevance | Genesis Mission Fit |
|---|---|---|---|---|---|
| **[EOS](https://www.eos.info/)** | Krailling, Germany | Established | LPBF systems (M 100–M 400); largest global installed base; academic partnership programs | Equipment option with university pricing, training, and application support. | ★★★ — Academic partnerships exist; could support equipment cost-share. |
| **[Nikon SLM Solutions](https://www.slm-solutions.com/)** | Lübeck, Germany (Nikon) | Established | LPBF systems; Leading Minds Consortium for AM adoption | Academic collaboration program; part of broader Nikon metrology ecosystem. | ★★★ — Academic programs; Nikon acquisition (2023) adds metrology capabilities. |
| **[Trumpf](https://www.trumpf.com/)** | Ditzingen, Germany | Established | LPBF systems (TruPrint); strong process monitoring and quality control | Research partnerships; particularly strong in in-situ monitoring relevant to data-driven AM. | ★★ — Large corporation; research partnership possible but limited Genesis Mission fit. |
| **[Renishaw](https://www.renishaw.com/)** | Wotton-under-Edge, UK | Established | LPBF systems (RenAM 500Q); in-process monitoring and metrology | University lab partnerships; strong real-time monitoring capabilities relevant to closed-loop AM. | ★★ — UK-based; academic programs available. |
| **[GE Additive / Colibrium Additive](https://www.colibriumadditive.com/)** | Cincinnati, OH, USA | Established | Concept Laser M2 Series 5 LPBF; Arcam EBM systems | **Existing asset:** BYU Crabtree building has a Concept Laser M2 Cusing (currently down ~2 years). New ~$400K; used ~$150K. | ★ — Corporate; existing relationship through installed equipment. |
| **[Velo3D](https://www.velo3d.com/)** | Fremont, CA, USA | 2014 | Established | Sapphire/Sapphire XC support-free (SupportFree™) LPBF; dual 1kW lasers; Assure™ quality assurance; US Navy and DoD contracts ($11.5M + $9.8M, 2026); Dyndrite integration | US-designed and built LPBF. Defense contracts for rapid production of CuNi naval components. Exhibitor and keynote panelist at RAPID+TCT 2026. | ★★★ — US company with defense relevance; large-format support-free printing unique capability. |
| **[AddUp](https://www.addupsolutions.com/)** | Cébazat, France / Blue Ash, OH, USA | 2016 | Established (JV) | FormUp 350 modular LPBF; Michelin-FIVES joint venture; DED capabilities; US Solution Center in Ohio | Modular, production-grade LPBF with US presence. Used for serial production (Michelin tire molds). Exhibitor at RAPID+TCT 2026 (#2232). | ★★★ — JV with US office; modular LPBF with production pedigree. |
| **[Farsoon Technologies](https://www.farsoon.com/)** | Changsha, China | 2009 | Established | Open-platform LPBF (FS301M, FS421M) and SLS systems; open-material architecture | Chinese LPBF OEM with open-material philosophy. Growing global presence. Exhibitor at RAPID+TCT 2026 (#1211). | ★ — Chinese company; limited Genesis Mission fit but relevant as open-material platform competitor. |
| **[Bright Laser Technologies (BLT)](https://en.xa-blt.com/)** | Xi'an, China | 2011 | Established | LPBF and DED systems; one of China's largest metal AM equipment manufacturers | Major Chinese metal AM OEM. Exhibitor at RAPID+TCT 2026 (#1647). | ★ — Chinese company; competitive intelligence only. |
| **[Seurat Technologies](https://www.seurat.com/)** | Wilmington, MA, USA | 2015 | Growth-stage startup | Area Printing® proprietary high-throughput metal AM; LLNL-origin; 130+ patents; contract manufacturing model (not printer sales); 100K sq ft Boston factory; NVIDIA-backed | Disruptive throughput approach to metal AM. Contract manufacturing model means VCL wouldn't buy a printer but could outsource prints. Edison-recommended addition. | ★★★ — US startup; LLNL-origin; disruptive Area Printing could alter AM economics. |

### Desktop / Benchtop LPBF (Emerging)

| Company | HQ | Founded | Stage | What They Do | VCL Relevance | Genesis Mission Fit |
|---|---|---|---|---|---|---|
| **[Xact Metal](https://xactmetal.com/)** | State College, PA, USA | 2017 | Startup | Affordable LPBF (XM200C ~$65K, XM200G ~$90K); 150+ units shipped | Strong candidate for VCL's desktop LPBF acquisition. US-made, affordable, industrial-grade. Academic-friendly pricing. | ★★★★★ — US startup, affordable, ideal for Equipment partnership via letter of collaboration. |
| **[One Click Metal](https://www.oneclickmetal.com/)** | Tamm, Germany | 2020 | Startup | MPRINT+ benchtop LPBF; simplified powder handling; SME/education focus | Compact, safety-focused system. Good for education integration. | ★★★ — Non-US; education focus aligns with NSF broader impacts. |
| **[2OneLab](https://www.2onelab.com/)** | Linz, Austria | — | Startup | 2CREATE compact LPBF; open-material platform; 250W fiber laser | Open-material design allows custom powder experimentation — critical for alloy discovery. | ★★★ — Non-US; open-material platform is attractive for research. |
| **[AO Metal](https://aometal.com/)** | USA | — | Startup | Desktop LPBF (~$59K); blue laser technology; open materials | Affordable US-based option with open-material flexibility. | ★★★★ — US startup, low cost, research-friendly. |
| **[Shaaz](https://www.shaaz.in/)** | India | — | Startup | Ultra-compact LPBF (S100); medical/dental/lab focus | Ultra-low-cost entry for micro-scale AM R&D. | ★★ — Non-US; niche size. |
| **[Aconity3D](https://www.aconity3d.com/)** | Herzogenrath, Germany | — | Startup | Aconity MINI modular open-architecture LPBF research platform | Open-architecture with modular design for research flexibility. Equispheres partnership. | ★★★ — Non-US; research-focused open platform. |
| **[3D Systems](https://www.3dsystems.com/)** | Rock Hill, SC, USA | 1986 | Established | ProX DMP 200 LPBF; used in HT AM studies at Sandia (250 tensile bars/build) | Proven for high-throughput AM research. Sandia validated 25 tensile bars per array. | ★★ — Large corporation; limited Genesis Mission fit. |

### Sinter-Based Vat Photopolymerization (DLP + MIM-style debind and sinter)

These processes print a green part from metal powder in a light-cured binder, then debind and sinter it as in MIM.
Added for issue #228; details are in [vat-photopolymerization-metal-am.md](vat-photopolymerization-metal-am.md).

| Company | HQ | Founded | Stage | What They Do | VCL Relevance | Genesis Mission Fit |
|---|---|---|---|---|---|---|
| **[Greene Group Industries (PureForm™)](https://www.greenegroup.com/capabilities/metal-3d-printing/)** | Oceanside, CA, USA | — (bought Holo's assets in March 2024) | Established SME (private-equity owned) | MIM contract manufacturer for medical devices (ISO 13485). PureForm cures MIM powder in a photopolymer slurry by bottom-up DLP, then debinds and sinters it on the MIM line. 17-4PH and 316 only; 0.07 mm walls; ±0.025 mm up to 12 mm. Sells parts, not printers | No fit for the LPBF Al alloys: no aluminum, and sintering would erase the rapid-solidification microstructure. Possible Phase II trial for Cu-Cr-Zr, since PureForm began as Holo's pure-copper process (>92% IACS) | ★★ — US-based, but a parts shop with no alloy R&D and no aluminum. |
| **[Incus](https://www.incus3d.com/)** | Austria | 2019 | Startup | Lithography-based Metal Manufacturing (LMM). Sells Hammer Evo35 (R&D) and Pro25 (production) printers and makes its own feedstock. Steels, Ti, 99.9% Cu, precious metals | The VPP option if the lab ever wanted to buy a printer and develop custom feedstock ("standard and customized materials"). Same aluminum limits as PureForm | ★ — Non-US printer vendor. |
| **Admatec Additive Solutions** | Netherlands | — | Relaunched (2025) | Admaflex 130/300 DLP printers for ceramics and metals (Cu, IN625, steel). Nano Dimension bought Admatec in 2022, dropped it in 2025, and former management relaunched it | Context only | ★ — Non-US; unsettled after the relaunch. |

---

## 3. Characterization & Testing Equipment

| Company | HQ | Founded | Stage | What They Do | VCL Relevance | Genesis Mission Fit |
|---|---|---|---|---|---|---|
| **[Plastometrex](https://www.plastometrex.com/)** | Cambridge, UK | 2018 | Startup | Profilometry-based Indentation Plastometry (PIP); rapid stress-strain measurement; ASTM E3499-25 standard | **Planned PoC partner.** University case studies (Cambridge, Limerick). ASTRO America defense partnership. Could provide PLX-Benchtop access or discounted testing. | ★★★★★ — Startup with active academic partnerships and defense relevance. Non-US but strong Genesis Mission partner via international supplement. |
| **[Alemnis](https://www.alemnis.com/)** | Thun, Switzerland | 2011 | Established niche | In-situ micro-mechanical testing systems; strain-rate testing under extreme conditions | Referenced in funded programs (Iowa State DURIP). Specialized characterization tool. | ★★ — Swiss niche company; less directly relevant to VCL pipeline. |

### Mechanical Testing & High-Throughput Characterization (Edison Scientific)

Identified via Edison Scientific LITERATURE_HIGH query with peer-reviewed citations from high-throughput AM characterization studies.

| Company | HQ | Stage | What They Do | VCL Relevance |
|---|---|---|---|---|
| **[Instron](https://www.instron.com/)** | Norwood, MA, USA | Established | Universal testing machines; automated HT tensile workflows demonstrated (25 tests/hr at Sandia) | Industry standard for tensile/compression/fatigue. HT automation demonstrated in literature. |
| **[ZwickRoell](https://www.zwickroell.com/)** | Ulm, Germany | Established | Zwicki Z2.5 benchtop; hardness/indentation platforms; instrumented microindentation | Compact benchtop options suitable for VCL. Used in HT process-property studies for Al-6061. |
| **[MTS Systems](https://www.mts.com/)** | Eden Prairie, MN, USA | Established | Servo-hydraulic load frames; automated sequential tensile testing (25+ tests/hr) | Core component of Sandia's Generation II automated HT tensile testing system. |
| **[Bruker / Hysitron](https://www.bruker.com/)** | Billerica, MA, USA | Established | Hysitron TI Premier nanoindenter; automated nanoindentation arrays; 1–6 measurements/sec | High-throughput nanoindentation mapping for property screening across compositionally graded samples. |
| **[Struers](https://www.struers.com/)** | Ballerup, Denmark | Established | Duramin-40 automated Vickers/Knoop hardness tester | Used in HT recrystallization studies. Automated hardness traverses and mapping. ~$30K–$80K. |
| **[Anton Paar](https://www.anton-paar.com/)** | Graz, Austria | Established | Automated nanoindentation and micro/macro hardness testers | Benchtop systems for modulus/hardness mapping. ~$100K–$400K. |
| **[KLA](https://www.kla.com/)** | Milpitas, CA, USA | Established | iMicro/iNano nanoindenters with automated array testing | High-throughput nanoindentation; common in academic materials labs. ~$200K–$500K. |

### In-Situ AM Monitoring (Edison-recommended addition)

| Company | HQ | Stage | What They Do | VCL Relevance |
|---|---|---|---|---|
| **[Phase3D](https://www.phase-3d.com/)** | Chicago, IL, USA | Startup | Fringe Inspection™ digital fringe projection (DFP) for in-situ layer-by-layer monitoring of LPBF; micron-level topography; machine-agnostic (Renishaw, EOS); USAF/NASA defect correlation validated | Addresses a critical VCL gap: in-situ quality monitoring. Layer topography data could augment the optimization loop with real-time defect signals, improving closed-loop print quality. Edison recommended as HIGH priority addition. |

---

## 4. Software & AI Platforms

### Commercial CALPHAD / Thermodynamic Software

| Company | HQ | Founded | Stage | What They Do | VCL Relevance | Genesis Mission Fit |
|---|---|---|---|---|---|---|
| **[Thermo-Calc Software AB](https://thermocalc.com/)** | Solna, Sweden | 1997 | Established | CALPHAD software (Thermo-Calc, DICTRA, TC-PRISMA); thermodynamic databases (TCFE, TCHEA, TCAL); 2,000+ organizations in 60+ countries | **Core software dependency.** TCAL10/TCHEA5 databases in the licence budget. Industry-standard for alloy thermodynamics. US office in Pittsburgh. | ★★★ — Established but has academic licensing programs. Could provide in-kind software support for proposals. |
| **[CompuTherm LLC](https://computherm.com/)** | Middleton, WI, USA | 1996 | Established SME | Pandat CALPHAD software; modular architecture (PanPhaseDiagram, PanEvolution, PanDiffusion, PanSolidification); custom thermodynamic databases | US-based alternative to Thermo-Calc. UW-Madison spin-off with SBIR/STTR history. Pandat has strong Al, Ni, Ti database coverage. | ★★★★ — US-based SME with academic roots; good Genesis Mission fit for CALPHAD integration. |
| **[GTT Technologies](https://gtt-technologies.de/)** | Aachen, Germany | 1988 | Established | FactSage CALPHAD software (joint with Ecole Polytechnique Montréal); ceramic and slag databases | Alternative CALPHAD platform. Less focused on metallic alloy AM but comprehensive for oxide/slag systems. | ★★ — Non-US; less directly relevant. |
| **[Sente Software (JMatPro)](https://www.sentesoftware.co.uk/)** | Guildford, UK | — | Established | JMatPro materials properties simulation; calculates mechanical, physical, and thermophysical properties | Used extensively in academic materials research for property prediction. Developed with Thermotech. | ★★ — Non-US; niche CALPHAD alternative. |

### Open-Source CALPHAD Tools (Not Companies, but Key Software)

| Tool | Maintainer | License | Notes |
|---|---|---|---|
| **[pycalphad](https://pycalphad.org/)** | R. Otis (Penn State origin) | MIT | Python-native; ~3-10 calcs/sec; reads TDB format; VCL's primary free screening tool |
| **[OpenCalphad](https://github.com/sundmanbo/opencalphad)** | B. Sundman (KTH origin) | GPL | Fortran; ~1000-2500 calcs/sec; highest throughput for HPC screening |
| **[Equilipy](https://github.com/ORNL/Equilipy)** | ORNL | BSD | Python+Fortran; ~20-40 calcs/sec; ChemSage .dat format only |
| **[ESPEI](https://espei.org/)** | Penn State (ZK Liu group) | MIT | Automated CALPHAD database assessment with pycalphad |

### Materials Informatics / AI Platforms

| Company | HQ | Founded | Stage | What They Do | VCL Relevance | Genesis Mission Fit |
|---|---|---|---|---|---|---|
| **[Citrine Informatics](https://citrine.io/)** | Redwood City, CA, USA | 2013 | Growth-stage startup | AI platform for materials & chemicals R&D; ML-driven composition screening and property prediction; SaaS model | **Potential partner.** External Research Department partners on grant-funded academic projects. Could provide platform access for AI-guided alloy screening. Series C (2025). | ★★★★★ — US startup with established academic partnership program; directly relevant AI/ML platform. Top Genesis Mission partner. |
| **[QuesTek Innovations](https://www.questek.com/)** | Evanston, IL, USA | 1997 | Established SME | ICME-based alloy design (Materials by Design®, ICMD® SaaS); designed alloys for Stoke Space rockets in 12 months; Aubert & Duval partnership | Pioneer in computational alloy design. Named Fast Company Most Innovative 2025. Could partner on ICME-guided alloy selection for VCL pipeline. | ★★★★ — US SME, strong defense/aerospace track record. Genesis Mission partner for computational screening integration. |
| **[Ansys (Granta Design)](https://www.ansys.com/products/materials)** | Cambridge, UK / Canonsburg, PA, USA | — | Established | Granta MI materials data management; Granta Selector; Granta EduPack for teaching | Materials data/informatics platform. Academic partnerships with Politecnico di Milano, Cambridge, Chalmers. Extensive academic licensing. | ★★ — Large corporation; academic licensing useful but limited Genesis Mission fit. |

### AM Process Simulation Software (Edison Scientific)

Identified via Edison Scientific LITERATURE_HIGH query with peer-reviewed citations from AM simulation studies.

| Company | HQ | Stage | What They Do | VCL Relevance |
|---|---|---|---|---|
| **[Ansys Inc.](https://www.ansys.com/)** | Canonsburg, PA, USA | Established | ANSYS Additive Suite, Fluent, Mechanical; extensive academic licensing | Dominant AM simulation platform. Could simulate melt pool dynamics and residual stress for VCL's LPBF. |
| **[Hexagon / MSC Software](https://hexagon.com/)** | Newport Beach, CA, USA | Established | Simufact Additive (PBF/DED distortion prediction) | Used in university AM projects for build distortion and process optimization. |
| **[Flow Science](https://www.flow3d.com/)** | Santa Fe, NM, USA | Established | FLOW-3D AM, FLOW-3D WELD (melt pool CFD dynamics) | Specialized melt pool simulation. Used in university research for LPBF physics. |
| **[Altair / Additive Works](https://www.altair.com/)** | Troy, MI, USA | Established | Amphyon build simulation and support optimization | Academic use for AM process strategy optimization. |
| **[COMSOL](https://www.comsol.com/)** | Stockholm, Sweden / Burlington, MA, USA | Established | COMSOL Multiphysics (multi-physics AM modeling) | Widely used in universities for coupled thermal-mechanical-fluid AM simulations. |
| **[Autodesk (Netfabb)](https://www.autodesk.com/)** | San Francisco, CA, USA | Established | Autodesk Netfabb (AM build preparation and simulation) | Academic licensing available. Build preparation and lattice optimization. |
| **[AlphaSTAR Corporation](https://www.alphastar.com/)** | Long Beach, CA, USA | Established | GENOA 3DP multi-scale AM simulation | Defense research collaborations. Multi-scale process-property prediction. |
| **[Materialise](https://www.materialise.com/)** | Leuven, Belgium / Plymouth, MI, USA | Established (1990) | Magics AM build preparation; Build Processor OEM integration; CO-AM workflow platform; AM software/service leader | Industry-standard AM build prep software. Integrates with all major LPBF OEMs. Keynote panelist at RAPID+TCT 2026. | 
| **[Oqton (3DXpert)](https://www.oqton.com/)** | San Francisco, CA, USA / Ghent, Belgium | Established (acquired by 3D Systems 2021) | 3DXpert all-in-one metal AM software; AI-driven print preparation; used by Baker Hughes for downhole tools | End-to-end metal AM workflow software. Highlighted at RAPID+TCT 2026 (Baker Hughes presentation). |

---

## 5. Industry Consortia & Organizations

| Organization | Type | Relevance |
|---|---|---|
| **[America Makes](https://www.americamakes.us/)** | DoD-funded consortium (AFRL) | Coordinates AM funding (PADAM 2.0, AIM-4AM). BYU not currently a member. Membership enables proposal eligibility and industry networking. Awards up to $2M. |
| **[ASTRO America](https://astroamerica.com/)** | Defense manufacturing consortium | Plastometrex partnership. Focuses on advanced manufacturing for defense. Relevant for DoD-aligned proposals. |
| **[SGTE](https://www.sgte.net/)** (Scientific Group Thermodata Europe) | Thermodynamic data consortium | Maintains assessed databases underpinning Thermo-Calc and FactSage. Proprietary; requires consortium membership. |
| **[RAPID+TCT](https://www.rapid3devent.com/)** | SME conference & exhibition | North America's largest AM event. April 13–16, 2026, Boston, MA. 450+ exhibitors. Key networking venue for VCL partnerships. |

### RAPID+TCT 2026 — Key Presentations Relevant to VCL Pipeline

> Source: [RAPID+TCT 2026 Conference Schedule](https://rapidtct2026.eventscribe.net/agenda.asp?pfp=BrowseConferencebyDate), April 13–16, 2026, Boston, MA.

| Presentation | Day | VCL Relevance |
|---|---|---|
| **Accelerating Qualification in AM with Profilometry-Based Indentation Plastometry (PIP)** | Mon April 13 | Directly relevant — Plastometrex (VCL planned PoC partner) presenting PIP for AM qualification |
| **Accelerating the Development and Adoption of Novel Alloys in Flight-Critical Aerospace Applications Using ICME** | Wed April 15 | ICME-based alloy design for AM — overlaps with VCL's computational screening approach |
| **Innovative Powders - Centrifugal Atomization: Enhanced Atomizing Technology for AM Powders** | Tue April 14 | Alternative atomization technology; competitive intelligence for VCL's ultrasonic approach |
| **Melt Pool to Macro-Scale: Size-Dependent LPBF 316L Properties** | Tue April 14 | LPBF process-property relationships; relevant to VCL's multi-scale characterization |
| **Selective Laser Melting of Graphene nanoplatelets-Inconel 718 Nanocomposites** | Tue April 14 | Novel alloy/composite LPBF; nanoparticle-enhanced alloys similar to RAM approach |
| **An Approach to Crack-Free Printing Gamma Prime Nickel Superalloys** | Wed April 15 | Directly relevant to Ni superalloy LPBF alloy design challenges |
| **High productivity parameter development framework for laser powder bed fusion of copper** | Wed April 15 | HT LPBF parameter optimization; relevant methodology for VCL's autonomous pipeline |
| **Advancing Toward Closed-Loop AI integration for Traceable Additive Manufacturing** | Wed April 15 | Closed-loop AI for AM — VCL competitor/comparator |
| **Multi-Agent AI Systems for Automated CAD-to-Print Workflows** | Wed April 15 | Agentic AI for AM automation; VCL adjacent |
| **Agentic AI for Additive: From Design Rules to Intelligent Workflow Automation** | Mon April 13 | AI workflow automation for AM; emerging competitor space |
| **Machine Learning in AM: Layer-by-Layer Defect Detection in Powder Bed Fusion** | Tue April 14 | ML for in-situ LPBF monitoring; relevant to VCL's quality assurance |
| **Industrializing Sustainability: Engineering Waste Streams into Printable Feedstocks** | Thu April 16 | Circular economy / recycled feedstocks; relates to 6K Additive and Solid State Metal approaches |
| **Forward-Deployed Manufacturing for Indo-Pacific Readiness: Inside ASTRO America's GAMMA Initiative** | Wed April 15 | ASTRO America (existing in landscape) defense AM initiative; relevant for DoD proposals |
| **Enabling Aluminum 7075 Forgings via Additive Friction Stir Deposition for Defense Needs** | Wed April 15 | Al 7075 for defense via solid-state AM; competitive approach to Al alloy development |
| **Functionally Graded Structures via LPBF: Interfacial Bonding and Corrosion Performance** | Thu April 16 | Multi-material LPBF; possible extension of VCL compositional screening |
| **Cross-Platform Properties Prediction in Laser Powder Bed Fusion** | Thu April 16 | Transfer learning across LPBF platforms; relevant to VCL's BOFN framework |

#### RAPID+TCT 2026 Keynote Panels

| Keynote | Panelists | VCL Relevance |
|---|---|---|
| **Scaling AM for Aerospace and Defense** | Stratasys, Siemens, US Army, Velo3D | Defense AM ecosystem; Velo3D now in landscape |
| **Life Saver: How AM Is Transforming Point-of-Care** | 3D Systems, Carbon, HP, Materialise | Medical AM; tangential but Materialise now in landscape |
| **From MIT to Mainstream: The Era of Manufacturing** | Dr. Neil Gershenfeld (MIT), Max Lobovsky (Formlabs) | Digital fabrication vision; MIT competing platform |

---

## 6. Materials Suppliers (Commodity)

| Company | HQ | What They Supply | VCL Role |
|---|---|---|---|
| **[McMaster-Carr](https://www.mcmaster.com/)** | Elmhurst, IL, USA | 1100 Al wire, Si powder (~45 µm), lab equipment | Raw materials for initial powder mixture preparation |
| **[MSE Supplies](https://www.msesupplies.com/)** | Tucson, AZ, USA | AlSi10Mg powder (15–45 µm); IATA hazmat documentation | Specialty AM powder supplier; confirmed materials non-hazardous |
| **[OnlineMetals](https://www.onlinemetals.com/)** | Seattle, WA, USA | 1100 Al wire and sheet | Feedstock for atomization experiments |

---

## 7. Used Equipment Marketplaces

| Source | URL | VCL Context |
|---|---|---|
| **CAE Online** | caeonline.com | Used Concept Laser M2 (~$150K) |
| **Resale.biz** | resale.biz | Used Concept Laser M2 listings |
| **Colibrium Additive** | colibriumadditive.com | New Concept Laser M2 Series 5 (~$400K) |

---

## 8. Competing Research Platforms (Academic / National Lab)

These are not companies but represent the competitive landscape for autonomous alloy discovery:

| Platform | Institution | Country | What It Does | Key Limitation vs. VCL |
|---|---|---|---|---|
| **APEX** | LLNL | US | Autonomous DED synthesis + automated characterization; ~48 samples/day | Uses DED, not LPBF; no autonomous powder production |
| **AMASE** | UMD / NIST | US | Real-time BO + CALPHAD for phase diagram mapping; 6× experiment reduction | Thin films only; no bulk alloy or AM |
| **PAL 2.0** | JHU / JHU APL | US | Closed-loop ML + BO with arc-melting; discovered 2 MPEAs (Vickers >1200) | Manual arc melting; no AM; no automated characterization |
| **Cooper Group SDL** | U. Liverpool | UK | Multi-robot PXRD + modular SDL; Lunt 2024 (99 citations) | Chemistry-focused; not metals/AM |
| **A-Lab** | UC Berkeley | US | AlabOS autonomous synthesis for inorganic materials | Ceramic/inorganic focus; not metallic alloys or AM |
| **EHLA + ML** | RWTH Aachen | Germany | High-speed laser cladding + ML; 20+ alloy variants screened | Uses EHLA, not LPBF; bypasses powder production |
| **Hybrid ML-CALPHAD-LPBF** | MIT | US | Computational design → LPBF validation; matched Al7075 strength | Conventional powder atomization; manual sample prep |
| **Constrained MOBO** | Texas A&M | US | Entropy-based BO for Mo-Nb-Ti-V-W MPEAs; 21 Pareto-optimal alloys | Purely computational; no experimental loop |
| **AutoMAT** | NTU Singapore et al. | Singapore | LLM ideation → automated CALPHAD → experimental validation; 43K→3,161 compositions; 28.2% YS improvement in <2 weeks (Yang 2025) | Purely computational; no physical infrastructure; depends on external AM facilities |
| **MELD Manufacturing (AFSD)** | Christiansburg, VA | US | Additive Friction Stir Deposition; solid-state AM bypasses fusion printability limits; defense/aerospace | Solid-state process, not LPBF; no powder production; different alloy design constraints |

---

## 9. Strategic Genesis Mission Partnership Recommendations

Based on the analysis above, the following companies represent the strongest Genesis Mission partnership candidates for FLAIME, ranked by strategic fit:

### Tier 1 — Highest Priority (directly enable VCL's unique pipeline)

| Company | Why | Partnership Mechanism | Estimated In-Kind Value |
|---|---|---|---|
| **Citrine Informatics** | AI/ML screening platform; established academic research program; US-based | Letter of collaboration or unfunded collaborator | Platform access ($50K–$100K/yr value) |
| **Elementum 3D** | Novel AM powder technology; US-based; NASA/USAF partnerships; academic collaboration track record | Letter of collaboration | Powder supply, characterization data |
| **Xact Metal** | Affordable desktop LPBF; US-based; academic pricing; addresses VCL's printer acquisition need | Equipment partnership via letter of collaboration | Printer at academic pricing ($65K–$90K) |

### Tier 2 — Strong Candidates (letter of collaboration or unfunded)

| Company | Why | Partnership Mechanism |
|---|---|---|
| **Amazemet** | Critical powder production partner; active PoC; AI-driven atomization | Letter of collaboration (international) |
| **Plastometrex** | Rapid mechanical characterization; ASTM standard; defense partnerships | Letter of collaboration or beta-testing agreement |
| **CompuTherm** | US-based CALPHAD software (Pandat); academic roots; SBIR/STTR history | Letter of collaboration or software license |
| **6K Additive** | US-based sustainable powder production; DOE-backed; circular economy angle for sustainability-focused proposals | Letter of collaboration or unfunded collaborator for recycled powder supply |

### Tier 3 — Supporting Partnerships

| Company | Why | Partnership Mechanism |
|---|---|---|
| **QuesTek Innovations** | ICME alloy design pioneer; US-based; aerospace track record | Letter of collaboration for computational alloy design |
| **Thermo-Calc Software** | Industry-standard CALPHAD; US office (Pittsburgh); academic licensing | In-kind software/database support via letter of collaboration |
| **Uniformity Labs** | US Al powder innovator; could supply optimized feedstock | Letter of collaboration |

---

## 10. Summary by Geography

### US-Based Companies
- **Citrine Informatics** (Redwood City, CA) — AI/ML materials platform
- **Elementum 3D** (Thornton, CO) — RAM alloy powders
- **Xact Metal** (State College, PA) — Desktop LPBF printers
- **QuesTek Innovations** (Evanston, IL) — ICME alloy design
- **CompuTherm** (Middleton, WI) — Pandat CALPHAD software
- **Uniformity Labs** (Fremont, CA) — Al powder optimization
- **AO Metal** (USA) — Desktop LPBF
- **Solid State Metal** (USA, Pacific Northwest) — Solid-state scrap-to-wire feedstock for DED/WAAM
- **6K Additive** (Burgettstown, PA) — UniMelt plasma powder recycling/production
- **Velo3D** (Fremont, CA) — Support-free LPBF (Sapphire)
- **Seurat Technologies** (Wilmington, MA) — Area Printing high-throughput metal AM
- **Phase3D** (Chicago, IL) — In-situ LPBF monitoring (Fringe Inspection)
- **GE Additive / Colibrium** (Cincinnati, OH) — LPBF equipment
- **3D Systems** (Rock Hill, SC) — LPBF equipment
- **Arcast Inc.** (Oxford, ME) — Gas atomization equipment OEM
- **Carpenter Technology** (Philadelphia, PA) — Gas atomized powders
- **GKN Hoeganaes** (Cinnaminson, NJ) — Gas atomized AM powders
- **ATI** (Dallas, TX) — Titanium gas atomization
- **Praxair / Linde** (Danbury, CT) — Titanium gas atomization
- **Ansys Inc.** (Canonsburg, PA) — AM simulation (Additive Suite, Fluent)
- **Hexagon / MSC Software** (Newport Beach, CA) — Simufact Additive
- **Flow Science** (Santa Fe, NM) — FLOW-3D AM melt pool CFD
- **Altair** (Troy, MI) — Amphyon AM build simulation
- **Autodesk** (San Francisco, CA) — Netfabb AM simulation
- **AlphaSTAR Corporation** (Long Beach, CA) — GENOA 3DP defense simulation
- **Oqton / 3DXpert** (San Francisco, CA) — Metal AM workflow software
- **Instron** (Norwood, MA) — Universal testing machines
- **MTS Systems** (Eden Prairie, MN) — Servo-hydraulic testing
- **Bruker / Hysitron** (Billerica, MA) — Nanoindentation
- **KLA** (Milpitas, CA) — Nanoindenters
- **McMaster-Carr** (Elmhurst, IL) — Materials supplier
- **MSE Supplies** (Tucson, AZ) — Specialty AM powder
- **OnlineMetals** (Seattle, WA) — Metal feedstock
- **Valimet** (Stockton, CA) — Custom Al gas atomization *(3B: Priority 1 GA partner)*
- **Materion** (Mayfield Heights, OH) — Be-Cu incumbent *(3B: benchmark for Cu-Cr-Zr)*
- **AMETEK SMP** (Wallingford, CT) — Pfinodal® Be-free Cu-Ni-Sn *(3B: Be-Cu replacement)*
- **IBC Advanced Alloys** (Franklin, IN) — Be-free CuNiSiCr castings *(3B: Be-Cu replacement)*
- **MP Materials** (Mountain Pass, CA) — US rare earth mining *(3B: supply chain context)*
- **Phoenix Tailings** (Woburn, MA) — Zero-waste REE extraction *(3B: recycling context)*
- **Momentum Technologies** (Carrollton, TX) — REE recycling (MSX) *(3B: CMI Hub partner)*
- **Niron Magnetics** (Minneapolis, MN) — REE-free magnets *(3B: substitution model)*
- **Eck Industries** (Manitowoc, WI) — Licensed Al-Ce alloys from CMI Hub *(3B: CMI commercialization partner)*
- **Fortius Metals** (Lafayette, CO) — Inoculated Al alloy development *(3B: Sc-free AM alloys)*

### European Companies
- **Amazemet** (Warsaw, Poland) — Ultrasonic atomization
- **Plastometrex** (Cambridge, UK) — PIP mechanical testing
- **Thermo-Calc Software AB** (Solna, Sweden) — CALPHAD software
- **EOS** (Krailling, Germany) — LPBF systems
- **Trumpf** (Ditzingen, Germany) — LPBF systems
- **Renishaw** (Wotton-under-Edge, UK) — LPBF + metrology
- **Nikon SLM Solutions** (Lübeck, Germany) — LPBF systems
- **One Click Metal** (Tamm, Germany) — Desktop LPBF
- **2OneLab** (Linz, Austria) — Desktop LPBF
- **Aconity3D** (Herzogenrath, Germany) — Research LPBF
- **ALD Vacuum Technologies** (Hanau, Germany) — VIGA/EIGA atomization equipment
- **Phoenix Scientific Industries** (Hailsham, UK) — Hermiga gas atomizers
- **Atomising Systems Ltd** (Sheffield, UK) — Multi-technology atomizers
- **TLS Technik** (Bitterfeld, Germany) — EIGA Ti powder
- **Sandvik Osprey** (Neath, UK) — Gas atomized powders
- **H.C. Starck** (Goslar, Germany) — Refractory metal powders
- **GTT Technologies** (Aachen, Germany) — FactSage CALPHAD
- **Sente Software** (Guildford, UK) — JMatPro
- **Ansys / Granta Design** (Cambridge, UK) — Materials data/informatics
- **COMSOL** (Stockholm, Sweden) — Multi-physics simulation
- **Höganäs AB** (Höganäs, Sweden) — Metal powders
- **Alemnis** (Thun, Switzerland) — Micro-mechanical testing
- **ZwickRoell** (Ulm, Germany) — Mechanical testing
- **Struers** (Ballerup, Denmark) — Automated hardness testing
- **Anton Paar** (Graz, Austria) — Nanoindentation/hardness
- **AddUp** (Cébazat, France / Blue Ash, OH) — FormUp 350 LPBF (Michelin-FIVES JV)
- **Materialise** (Leuven, Belgium) — AM software (Magics, Build Processor)
- **Constellium** (Paris, France / Baltimore, MD) — Aheadd® CP1 Al-Zr-Fe LPBF alloy *(3B: Sc-free competitor)*
- **APWORKS** (Taufkirchen/Munich, Germany) — Scalmalloy® Al-Mg-Sc *(3B: Sc-dependent incumbent)*
- **Aeromet International** (UK) — A20X Al-Cu-Mg-Ag+TiB₂ Sc-free LPBF alloy *(3B: Sc-free competitor)*

### Canadian Companies
- **AP&C / GE Additive** (Montreal, QC) — Plasma atomization
- **Tekna** (Sherbrooke, QC) — Plasma atomization
- **Equispheres** (Ottawa, ON) — Narrow-PSD Al powders
- **PyroGenesis Canada** (Montreal, QC) — Plasma atomization systems

### Other
- **Shaaz** (India) — Ultra-compact LPBF
- **Farsoon Technologies** (Changsha, China) — Open-platform LPBF
- **Bright Laser Technologies (BLT)** (Xi'an, China) — LPBF/DED OEM

---

## 11. Summary by Maturity

### Startups (< 10 years, high growth)
Amazemet, Elementum 3D, Xact Metal, Plastometrex, Citrine Informatics, Equispheres, Uniformity Labs, One Click Metal, 2OneLab, AO Metal, Shaaz, Aconity3D, Solid State Metal, 6K Additive, Seurat Technologies, Phase3D, Phoenix Tailings, Momentum Technologies, Niron Magnetics, Fortius Metals

### Established SMEs (> 10 years, specialized)
QuesTek Innovations, CompuTherm, Alemnis, Arcast Inc., Flow Science, AlphaSTAR Corporation, Sente Software, Valimet, IBC Advanced Alloys, Eck Industries

### Large / Public Corporations
EOS, Trumpf, Renishaw, Nikon SLM Solutions, GE Additive, 3D Systems, Velo3D, AddUp, Farsoon Technologies, Bright Laser Technologies, Höganäs AB, Tekna, AP&C, Carpenter Technology, GKN Hoeganaes, Sandvik Osprey, ATI, Praxair/Linde, ALD Vacuum Technologies, PyroGenesis Canada, Thermo-Calc Software AB, GTT Technologies, Ansys, Hexagon, COMSOL, Autodesk, Altair, Materialise, Oqton/3DXpert, Instron, ZwickRoell, MTS Systems, Bruker, Struers, Anton Paar, KLA, McMaster-Carr, Materion, AMETEK SMP, MP Materials, Constellium, APWORKS (Airbus), Aeromet International

---

## 12. Likelihood of Real-World Application Impact

| Tier | Companies | Rationale |
|---|---|---|
| **Already in production** | EOS, Trumpf, Nikon SLM, Renishaw, GE Additive, 3D Systems, Velo3D, AddUp, Höganäs, Carpenter Technology, Sandvik Osprey, ATI, Thermo-Calc, Ansys, COMSOL, Materialise, Instron, ZwickRoell, MTS Systems, Bruker, Materion, AMETEK SMP, Constellium, APWORKS, MP Materials, Aeromet International | Equipment, software, and alloys already used in certified aerospace/automotive/defense production |
| **Transitioning to production** | Elementum 3D, QuesTek, Equispheres, Tekna, AP&C, ALD Vacuum Technologies, PyroGenesis, 6K Additive, Seurat Technologies, Hexagon, Altair, Autodesk, Oqton/3DXpert, Niron Magnetics, Eck Industries | Alloys/powders/software entering qualification pipelines; defense and space applications |
| **High potential, pre-production** | Amazemet, Citrine Informatics, Plastometrex, Xact Metal, Uniformity Labs, Aconity3D, CompuTherm, Flow Science, AlphaSTAR, Phase3D, Phoenix Tailings, Momentum Technologies, Valimet, Fortius Metals | Technology proven in R&D; adoption growing but not yet in certified production environments |
| **Early/niche** | One Click Metal, 2OneLab, AO Metal, Shaaz, Alemnis, Sente Software, Anton Paar, KLA, Struers, Solid State Metal, Farsoon Technologies, Bright Laser Technologies, IBC Advanced Alloys | Serving education/R&D niches; production deployment uncertain or narrowly focused |

---

## 13. Materials Criticality & Supply Chain (Topic 3B Alignment)

> **Context:** FLAIME now targets [DOE Genesis Mission Topic 3B](https://science.osti.gov/) — Critical Minerals (AMMTO). The material strategy centers on discovering Al alloys that **eliminate dependence on supply-constrained critical minerals** (Mg, Sc, REEs) while maintaining high AM performance. Primary alloy families: Al-Zr and Al-Mn-Cr-Zr (~80% Phase I). Complement: Cu-Cr-Zr (~20%) for beryllium-free Cu alloy replacement. Note: Zr, Mn, and Cr are themselves on the [USGS 2025 Critical Minerals List](https://www.federalregister.gov/documents/2025/11/07/2025-19813/final-2025-list-of-critical-minerals) (60 minerals), but are far more abundant and domestically available than Sc or REEs.

### 13.1 Critical-Mineral-Lean Alloy Developers (Competitors & Comparators)

| Company | HQ | Stage | What They Do | VCL/3B Relevance |
|---|---|---|---|---|
| **[Constellium](https://www.constellium.com/)** | Paris, France / Baltimore, MD, USA | Established (2011) | Aheadd® CP1 (Al-Zr-Fe) — scandium-free, REE-free LPBF alloy; no volatile elements (Mg, Zn); stable to 250–300°C; 2–4× build rate vs AlSi10Mg; also developing Aheadd® HT1 (Al-Mn-Ni-Cu-Zr) for high-temp service (~260°C); America Makes member; F1-qualified; partnerships with Nikon AM, AddUp, Eplus3D | **Closest commercial competitor** to FLAIME's Al-Zr alloy strategy. Aheadd CP1 is the commercial incumbent that FLAIME-discovered alloys must match or exceed. Key reference: Al-Zr-Fe system with no critical minerals. |
| **[APWORKS](https://www.apworks.de/)** (Airbus subsidiary) | Taufkirchen (Munich), Germany | Established | Scalmalloy® (Al-Mg-Sc) — high-strength AM alloy (YS ~480 MPa, UTS ~520 MPa, EL ~8–13%); Airbus-qualified; FIA-approved; Equispheres partnership for North American production | **Represents the Sc-dependent incumbent** that FLAIME's mineral-lean alloys aim to displace. Scalmalloy's ~$200–500/kg powder cost (Sc premium) vs FLAIME's target <$100/kg demonstrates the cost/supply-chain value proposition. |
| **[Elementum 3D](https://www.elementum3d.com/)** *(already in Section 1)* | Thornton, CO, USA | Growth-stage startup | RAM alloy powders including Al 6061-RAM1, 7075-RAM2 — enables difficult-to-print alloys via in-situ ceramic nanoparticle inoculation; avoids Sc/REE additions | **Direct 3B alignment:** achieves grain refinement through ceramic inoculants rather than Sc/REEs. Complementary approach to FLAIME's Zr-based strategy. |
| **[Aeromet International](https://www.aerometinternational.com/)** | UK | Established | A20X (Al-Cu-Mg-Ag + TiB₂ nanoparticles) — Sc-free, REE-free high-strength AM alloy; patented technology | Sc-free alternative using TiB₂ grain refinement. Different approach from FLAIME's Zr-based strategy but validates the Sc-free AM alloy market demand. |
| **[Eck Industries](https://www.eckindustries.com/)** | Manitowoc, WI, USA | Established | Licensed Al-Ce alloys from CMI Hub; continuous production including atomized powders for automotive/military/aerospace; co-assignee with UT-Battelle on AM patents | **CMI Hub commercialization partner.** Demonstrates DOE-funded pathway from critical mineral research to commercial production — strong precedent for FLAIME's 3B narrative. |
| **[Fortius Metals](https://fortiusmetals.com/)** | Lafayette, CO, USA | Startup | Inoculated high-strength aluminum alloy development for AM welding/DED; adjacent to LPBF alloy design | Developing mineral-lean grain-refined Al alloys; adjacent to FLAIME's LPBF focus but relevant to the broader Sc-free Al AM ecosystem. |

### 13.2 Beryllium-Copper Replacement Ecosystem

FLAIME's Cu-Cr-Zr complement (~20% Phase I) targets replacement of Be-Cu alloys (C17200) — a critical safety and environmental driver.

| Company | HQ | Stage | What They Do | VCL/3B Relevance |
|---|---|---|---|---|
| **[Materion Corporation](https://www.materion.com/)** (NYSE: MTRN) | Mayfield Heights, OH, USA | Established (1931) | World's largest Be-Cu producer (Brush Alloy 25, Alloy 190); 3,000+ employees; aerospace/defense/electronics | **The incumbent** that Be-free Cu-Cr-Zr alloys aim to replace. Materion defines the performance benchmarks (YS ~1,000+ MPa aged, conductivity ~20% IACS) FLAIME must approach. Key letter-of-support or benchmark data source. |
| **[AMETEK SMP](https://www.ametek-ct.com/)** | Wallingford, CT, USA | Established | Pfinodal® (C72900) spinodal Cu-Ni-Sn alloy — leading commercial Be-Cu replacement; non-sparking, non-magnetic; 50+ years metallurgy | Commercial Be-free alloy producer. FLAIME's Cu-Cr-Zr targets a different approach (precipitation hardening vs spinodal) but Pfinodal® is a key benchmark. |
| **[IBC Advanced Alloys](https://ibcadvancedalloys.com/)** | Franklin, IN, USA | Established | Thermal-Mould™ Super CuNiSiCr (C18000) — Be-free high-strength copper castings/forgings; vertically integrated (ingot → machined part) | Another Be-free copper alloy producer. CuNiSiCr represents the cast/wrought approach vs FLAIME's AM approach to Be-free Cu alloys. |

### 13.3 Critical Mineral Supply Chain & Recycling

These companies address the broader critical minerals ecosystem relevant to Topic 3B framing.

| Company | HQ | Stage | What They Do | VCL/3B Relevance |
|---|---|---|---|---|
| **[MP Materials](https://mpmaterials.com/)** (NYSE: MP) | Mountain Pass, CA, USA | Established (2017) | Only large-scale US rare earth mine; supplies 10–15% of global REE market; Pentagon $400M investment (2025); 10-year DoD offtake; building downstream magnet manufacturing | US domestic REE supply chain. Context for FLAIME's narrative: "our alloys bypass the REE supply chain that MP Materials is trying to secure." |
| **[Phoenix Tailings](https://phoenixtailings.com/)** | Woburn, MA, USA | Startup (2019) | Zero-waste REE extraction from mining tailings; clean electrochemistry; MIT spinoff; 200→1,000+ tons/yr facility in Exeter, NH; DOE $1.6M grant | US startup solving REE supply via recycling. Demonstrates the difficulty of REE supply that FLAIME's mineral-lean approach avoids entirely. |
| **[Momentum Technologies](https://momentum.technology/)** | Carrollton, TX, USA | Startup | Membrane Solvent Extraction (MSX) for REE recovery; ORNL-licensed technology; CMI Hub partner; processing scrapped magnets, batteries, mine tailings | CMI Hub commercialization partner. REE recycling technology exemplifies the "avoid the problem entirely" framing of FLAIME's mineral-lean alloys. |
| **[Niron Magnetics](https://www.nironmagnetics.com/)** | Minneapolis, MN, USA | Startup (2014) | Iron Nitride (Fe₁₆N₂) rare-earth-free permanent magnets ("Clean Earth Magnets"); 70K sq ft Minneapolis pilot plant; 1,500 tons/yr Sartell MN facility (2027); backed by Stellantis, Samsung | Model for REE substitution success story. Demonstrates that critical mineral substitution is a fundable, impactful research direction — validates FLAIME's premise. |
| **[6K Additive](https://6kadditive.com/)** *(already in Section 1)* | Burgettstown, PA, USA | Growth-stage startup | UniMelt® plasma converts scrap metal → AM-ready powder; 91% lower emissions; DOE $107M grant | **Directly 3B-aligned:** circular economy approach to AM powder that reduces virgin critical mineral extraction. |
| **[Solid State Metal](https://www.solidmetal.tech/)** *(already in Section 1)* | USA (Pacific Northwest) | Early-stage startup | Solid-state scrap-to-wire feedstock; PNNL ShAPE research | **3B-aligned:** converts scrap into AM feedstock, reducing demand for newly mined critical minerals. |

### 13.4 Custom Powder Atomization Partners (Phase I GA Validation)

| Company | HQ | Stage | What They Do | VCL/3B Relevance |
|---|---|---|---|---|
| **[Valimet](https://valimet.com/)** | Stockton, CA, USA | Established (1987) | Custom spherical Al and Al-alloy gas atomization; family-owned; 30+ years experience; tailored PSD and custom compositions | **Priority 1 GA partner** for FLAIME Phase I. Service contract for 3–5 custom Al-Zr/Al-Mn-Cr-Zr compositions at 5–10 kg each. US-based, flexible batch sizes, established AM powder quality. |
| **Ames National Laboratory** *(See PR #26)* | Ames, IA, USA | National Lab | Gas Atomization Reaction Synthesis (GARS) gas atomization (4–20 kg); Powder Synthesis & Development Capability (PSDC); Ames Lab's Materials Preparation Center manager is a responsive contact; an Ames Lab contact heads the Powder Group | **Phase II gas atomization (GA) partner.** Letter of support pointing to future GARS collaboration. Internal Genesis Mission deadline limits Phase I participation. |

### 13.5 DOE Critical Materials Innovation (CMI) Hub

| Organization | Type | Relevance |
|---|---|---|
| **[CMI Hub](https://www.ameslab.gov/cmi/)** (Ames National Lab) | DOE Energy Innovation Hub | Lead hub for critical mineral substitution, recycling, and supply chain R&D. 36+ industry partners. 20+ licensed technologies. Four research thrusts including alloy substitution. Direct programmatic alignment with FLAIME's Topic 3B narrative. |

### 13.6 Topic 3B Partnership Tier Updates

With the shift to Topic 3B, the following companies gain elevated strategic importance:

| Tier | Company | 3B-Specific Rationale |
|---|---|---|
| **1 (elevated)** | **Elementum 3D** | RAM inoculant approach eliminates Sc/REE need — direct 3B "mineral-lean alloy design" alignment |
| **1 (elevated)** | **Citrine Informatics** | AI platform can incorporate mineral criticality as optimization objective (supply risk index alongside mechanical properties) |
| **2 (new)** | **Constellium** | Aheadd CP1 benchmark partner — could provide powder samples and data for direct comparison with FLAIME alloys; America Makes member |
| **2 (elevated)** | **6K Additive** | Circular economy powder production directly addresses DOE Critical Minerals Strategy Pillars 2 (recycling) and 5 (workforce) |
| **2 (new)** | **Valimet** | Priority 1 custom Al powder atomization partner for Phase I GA validation; US-based, flexible |
| **3 (context)** | **Materion** | Be-Cu incumbent; benchmark data source for Cu-Cr-Zr complement. Letter of support for "replacing hazardous Be alloys" |
| **3 (context)** | **APWORKS** | Scalmalloy incumbent; defines the Sc-dependent performance ceiling FLAIME must match without Sc/REEs |

### 13.7 DOE 5-Pillar Critical Minerals Strategy Alignment

| DOE CMS Pillar | FLAIME Alignment | Key Companies |
|---|---|---|
| **Pillar 1: Diversify supply** | Alloys using Zr/Mn/Cr (more abundant) instead of Sc/REEs | Valimet, Elementum 3D, Constellium |
| **Pillar 2: Develop substitutes** | Al-Zr, Al-Mn-Cr-Zr families replace Sc-dependent alloys; Cu-Cr-Zr replaces Be-Cu | Citrine Informatics, QuesTek, CompuTherm |
| **Pillar 3: Improve recycling** | 6K Additive (scrap→powder), Solid State Metal (scrap→wire) | 6K Additive, Solid State Metal |
| **Pillar 5: Grow workforce** | 12 undergrads trained in mineral-aware alloy design | (internal VCL capability) |

---

## 14. Key Contact Directory

Contact information for Genesis Mission partnership outreach. Verified via web research and Edison Scientific literature review.

### Tier 1 Partners (Highest Priority)

| Company | Key Contact | Title | Contact Info | Notes |
|---|---|---|---|---|
| **Valimet** | Valimet's president | President | sales@valimet.com; +1 (209) 444-1600 | **Priority 1 gas atomization (GA) partner.** 431 Sperry Rd, Stockton, CA 95206 |
| **Citrine Informatics** | Bryce Meredig | CEO & Co-founder | bryce@citrine.io; info@citrine.io | 2629 Broadway St, Redwood City, CA 94063. COO: Greg Mulholland (greg@citrine.io). Academic partnerships via External Research Dept |
| **Elementum 3D** | Dr. Jacob Nuechterlein | Founder, President & CEO | sales@elementum3d.com | 400 Young Ct Unit 1, Erie, CO 80516. COO: Thomas Stalcup; CTO: Jeremy Iten |
| **Xact Metal** | Juan Mario Gomez | CEO | +1 (814) 205-1505 | 200 Innovation Blvd, Suite 257, State College, PA 16803 (Penn State Innovation Park). Co-founders: Matt Woods, Jonathon Hollahan |
| **Thermo-Calc Software** | Thermo-Calc's account manager | North America contact | via thermocalc.com | A Thermo-Calc specialist is also an NA contact. Advisory role with letter of support (not funded partner). See thermocalc-discussion-transcript.md |

### Tier 2 Partners

| Company | Key Contact | Title | Contact Info | Notes |
|---|---|---|---|---|
| **Amazemet** | Amazemet's founder | Founder | office@amazemet.com | Al. Jana Pawła II 27, 00-867 Warsaw, Poland. Warsaw Univ. of Technology spinoff |
| **Plastometrex** | Dr. James Dean | CEO & Co-founder | info@plastometrex.com; +44 1353 881390 | 204 Cambridge Science Park, Milton Rd, Cambridge CB4 0GZ, UK. CTO: Dr. Jimmy Campbell |
| **CompuTherm LLC** | Dr. Fan Zhang, FASM | President | Fan.Zhang@computherm.com; info@computherm.com; +1 (608) 203-8843 | 8401 Greenway Blvd, Suite 248, Middleton, WI 53562. Founded by Prof. Y. Austin Chang (1996) |
| **6K Additive** | Frank Roberts | CEO | +1 (724) 215-7049 | 541 Steubenville Pike, Burgettstown, PA 15021. IPO 2026; DPA Title III $23.4M grant |
| **Constellium (Aheadd)** | Dr. Ravi Shahani | Technical Lead, AM alloys | aheadd@constellium.com | C-TEC Constellium Technology Center, France. BD Manager: Syam Unnikrishnan |
| **Phase3D** | Niall O'Dowd | Founder | niall@phase-3.com; sales@phase-3d.com; +1 (206) 369-4982 | 2415 W. 19th St, Suite 2B-1, Chicago, IL 60608. DARPA SURGE-backed |

### Tier 3 & Context Partners

| Company | Key Contact | Title | Contact Info | Notes |
|---|---|---|---|---|
| **QuesTek Innovations** | Aziz Asphahani | Chairman & CEO | +1 (847) 328-5800 | 1820 Ridge Ave, Evanston, IL 60201. Chief Science Officer: Dr. Greg Olson |
| **APWORKS** | Sebastian Lepa (2026) | CEO | info@apworks.de; +49 89 954 738 766 | Willy-Messerschmitt-Str. 1, 82024 Taufkirchen, Germany. Prior CEOs: Joachim Zettler, Jon Myer |
| **Materion Corporation** | (Technical Sales) | — | +1 (800) 862-4118 | 6070 Parkland Blvd, Mayfield Heights, OH 44124. Be-Cu incumbent benchmark |
| **Ames National Laboratory** | an Ames Lab contact | Materials Preparation Center (MPC) Manager | vulcan@ameslab.gov | Powder Group Head: an Ames Lab contact (PSD@ameslab.gov). Phase II Gas Atomization Reaction Synthesis (GARS) partner |

### National Lab & Consortium Contacts

| Organization | Key Contact | Title | Contact Info | Notes |
|---|---|---|---|---|
| **Ames Lab / CMI Hub** | an Ames Lab contact | Materials Preparation Center (MPC) Manager | vulcan@ameslab.gov | An Ames Lab contact heads the Powder Group. Internal Genesis Mission deadline limits Phase I participation |
| **ORNL MDF** | — | — | — | Priority 3 backup for gas atomization partnership |
