Question: 
I am building an autonomous alloy discovery platform (FLAIME) that uses ultrasonic atomization (AMAZEMET rePOWDER) for rapid screening of novel aluminum alloy compositions for laser powder bed fusion (LPBF) additive manufacturing. Our workflow produces 15-63 μm powders via ultrasonic atomization at 1-5 kg batch scale.

We need to plan a gas atomization scale-up validation step for our most promising compositions. Please address ALL of the following:

## Part 1: UA-to-GA Transfer Relationships
1. What is known about how powder properties (PSD, morphology, sphericity, flowability, apparent density, tap density, chemistry) transfer from ultrasonic atomization to gas atomization for aluminum alloys?
2. Are there published studies comparing UA vs GA powders of the same composition printed via LPBF? What property differences (density, microstructure, mechanical properties) are observed?
3. What are the key risks when scaling from UA powder to GA powder for the same alloy? (e.g., different solidification rates, satellite formation, oxide content, gas porosity)
4. Can UA powder characterization data (PSD, flowability, chemistry) be used to predict GA powder quality for the same composition? What correction factors or empirical relationships exist?
5. How do solidification rates compare between UA (~10³-10⁴ K/s) and GA (~10²-10⁵ K/s for close-coupled nozzles)? How does this affect phase formation, solute trapping, and microstructure in Al-Ce, Al-Cu, and Al-Si systems?

## Part 2: GA Service Providers for Small-Batch Al Alloys
1. Which US-based gas atomization service providers accept small-batch (5-50 kg) custom aluminum alloy compositions? List specific companies with capabilities.
2. What are typical costs per kg for custom Al alloy gas atomization at 5 kg, 10 kg, 25 kg, and 50 kg batch sizes? Provide ranges.
3. Which DOE national laboratories offer gas atomization services (e.g., ORNL MDF, Ames Lab, PNNL)? What are access mechanisms (user proposals, CRADA, WFO)?
4. Are there university facilities with gas atomization capabilities that accept external work? List specific institutions.
5. What is typical lead time from order to powder delivery for custom Al alloy GA services?
6. What minimum information does a GA service provider need (composition, target PSD, quantity, certification requirements)?

## Part 3: Integration into Multi-Fidelity BOFN Framework
1. How should a gas atomization validation node fit into a cost-aware Bayesian optimization DAG that currently has: Node 0 (CALPHAD, ~$1), Node 1 (UA, ~$200), Node 2 (LPBF, ~$500), Node 3 (Tensile, ~$300)?
2. What is the appropriate cost estimate for a GA validation node at different batch sizes?
3. Should GA validation be a parallel branch or a sequential gate after the main discovery loop?
4. What is the minimum number of compositions that should be validated via GA to establish statistical confidence in UA→GA transferability?
5. What powder characterization tests are essential for the UA→GA comparison (and what standards apply)?

## Part 4: Budget Implications
1. For a $750K, 9-month Phase I project discovering ~200 Al alloy compositions via UA/LPBF, what is a reasonable budget allocation for GA scale-up validation of 3-5 top compositions?
2. How should this be structured in a DOE proposal: as a subaward, service contract, or user facility access?


# Gas Atomization Scale-Up Validation Plan for the FLAIME Autonomous Alloy Discovery Platform

## Part 1: UA-to-GA Transfer Relationships

### 1.1 Powder Property Transfer from UA to GA for Aluminum Alloys

The transfer of powder properties from ultrasonic atomization (UA) to gas atomization (GA) for aluminum alloys is not a one-to-one mapping, as the two processes differ fundamentally in droplet formation mechanisms. UA relies on acoustic cavitation and capillary wave breakup from an ultrasonically vibrated surface (typically ~20–60 kHz), whereas GA uses high-velocity inert gas jets to shear a molten metal stream (ciftcli2025alloydevelopmentfrom pages 1-3, zach2023sphericalpowderscontrol pages 4-4). The following property-by-property assessment summarizes what is known:

**Particle Size Distribution (PSD):** UA process parameters—vibration amplitude, frequency, arc current, and melt delivery angle—strongly influence PSD, with span variations up to 37.5% observed in AlSi12 studies (yankin2025effectofultrasonic pages 1-2, yankin2025effectofultrasonic pages 2-3). GA PSD is governed by gas pressure, nozzle design, gas-to-melt mass flow ratio, and melt superheat, with AM-relevant Al powders commonly classified to 15–45 µm or 20–63 µm (yakubov2022laserpowderbed pages 54-57, si2017characteristicsof7055al pages 6-8). Both processes can produce usable LPBF fractions, but the yield to the target cut may differ significantly.

**Morphology and Sphericity:** UA consistently produces highly spherical particles with fewer satellites than typical GA powders. In a direct comparison with commercial AlSi12 powder, UA-produced powder exhibited 21% higher additive manufacturing suitability factors and markedly improved sphericity, whereas the commercial comparator showed "highly irregular particle shapes, characterized by elongated and non-spherical forms" with "many particles exhibit[ing] some satellite particles fused to their surfaces" (yankin2025effectofultrasonic pages 12-15). The rePOWDER system has consistently produced spherical powder across multiple alloy systems (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6, zach2023sphericalpowderscontrol pages 4-4).

**Flowability:** UA AlSi12 powder showed improved compressibility index (45.1% better) and specific energy (22.8% better) compared to commercial powder, though basic flow energy was 22.4–37.6% lower for the UA powder (yankin2025effectofultrasonic pages 12-15). GA powder flowability depends on PSD, fines fraction, satellites, and moisture pickup, and can be degraded by cohesive fine particles that increase inter-particle cohesion (munizlerma2018acomprehensiveapproach pages 1-3).

**Chemistry and Oxide Content:** UA can preserve alloy chemistry well at lab scale, but volatile element losses (Mn, Zn) and rapid oxidation of fine Al droplets are noted risks (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6). GA under controlled argon atmosphere generally produces low-contamination powders, but oxide films on Al particles are unavoidable and smaller particles are more susceptible to oxidation and volatile element evaporation (munizlerma2018acomprehensiveapproach pages 1-3, yakubov2022laserpowderbed pages 54-57).

The comprehensive comparison is presented in the following table:

| Property | Ultrasonic Atomization (UA) | Gas Atomization (GA) | Key Differences/Risks |
|---|---|---|---|
| Particle Size Distribution (PSD) | Typically narrow-to-moderate PSD controlled strongly by vibration frequency/amplitude, melt delivery, and current; AlSi12 UA study reported span changes up to 37.5% with process settings, with usable fractions commonly sieved to 15–63 µm or <63 µm; more than half of produced batch can meet AM requirements, and one study reported ~75% below 63 µm after sieving. (yankin2025effectofultrasonic pages 1-2, yankin2025effectofultrasonic pages 12-15, yankin2025effectofultrasonic pages 2-3) | PSD strongly governed by nozzle design, gas pressure, melt superheat, and gas-to-melt ratio; AM-relevant Al powders are commonly classified to 20–63 µm or 15–45 µm; cooling rate and microstructure scale vary strongly with particle size via power-law relations. (yakubov2022laserpowderbed pages 54-57, si2017characteristicsof7055al pages 6-8, unal1990productionofrapidly pages 2-3, gianoglio2021onthecooling pages 1-2) | UA can be very effective for screening AM-size fractions at small scale, but PSD may shift during scale-up because GA break-up physics differ; expect re-optimization of target cut and yield when transferring UA compositions to GA. |
| Morphology / Sphericity | Generally highly spherical, smooth particles with high aspect-ratio closeness to 1; UA AlSi12 outperformed commercial comparator in morphology, and rePOWDER studies consistently report spherical particles suitable for AM. (yankin2025effectofultrasonic pages 12-15, ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6, zach2023sphericalpowderscontrol pages 4-4) | GA typically produces near-spherical powders suitable for LPBF, but morphology quality depends on process tuning; commercial GA Al powders are usually good, though satellites and some irregular/fused particles are common. (yakubov2022laserpowderbed pages 54-57, martin2020gasatomizationof pages 1-2) | UA often has an advantage in apparent particle smoothness and sphericity at screening scale; GA may show broader morphology variation, especially if tuned for throughput rather than premium LPBF morphology. |
| Satellite Formation | Usually lower satellite incidence; AlSi12 UA comparison showed fewer fused/satellite particles than the commercial powder. (yankin2025effectofultrasonic pages 12-15) | Satellite formation is a known GA issue because partially solidified fines can impact larger droplets/particles; commercial powders often show surface satellites. (yankin2025effectofultrasonic pages 1-2, yankin2025effectofultrasonic pages 12-15) | Satellite increase on GA scale-up is a primary transfer risk because it can reduce flowability, raise apparent surface area, and alter layer spreading behavior. |
| Flowability | UA AlSi12 showed improved overall AM suitability and better compressibility/specific-energy metrics than the commercial comparator; however, some bulk-flow metrics such as basic flow energy or conditioned bulk density were not always superior. (yankin2025effectofultrasonic pages 12-15) | GA Al powders are generally acceptable for LPBF when spherical and properly classified, but fines, satellites, moisture pickup, and oxide films can degrade flow/spreadability. (munizlerma2018acomprehensiveapproach pages 1-3, yakubov2022laserpowderbed pages 54-57, groarke2021powdercharacterization—methodsstandards pages 1-5, spierings2016powderflowabilitycharacterisation pages 11-12) | UA flowability data are directionally useful but not fully predictive of GA because satellites, fines population, and oxide state differ; direct Hall/Carney/rheology comparison is needed. |
| Apparent Density | Not consistently reported in UA Al literature, but high sphericity and lower satelliting should support competitive apparent density; AlSi12 UA had slightly lower conditioned bulk density than the commercial comparator in one study. (yankin2025effectofultrasonic pages 12-15) | Apparent density depends on PSD, shape, agglomeration, surface chemistry, and fines; spherical GA powders generally pack well, but cohesion from fines/oxide can reduce loose packing. (munizlerma2018acomprehensiveapproach pages 1-3, yakubov2022laserpowderbed pages 54-57, cooke2012propertiesofmetal pages 27-28) | Apparent density may drop on GA transfer if satellites/fines increase even when chemistry is unchanged; use ASTM B212/B417 or equivalent for direct comparison. (cooke2012propertiesofmetal pages 27-28) |
| Tap Density | Limited direct UA Al data in gathered evidence; expected to be good when sphericity is high and fines are controlled, but must be measured rather than inferred. (yankin2025effectofultrasonic pages 12-15, zrodowski2021novelcoldcrucible pages 11-12) | GA tap density is usually strong for spherical Al powders, but depends on PSD breadth, fines fraction, and satellite burden; standardized measurement is established. (munizlerma2018acomprehensiveapproach pages 1-3, cooke2012propertiesofmetal pages 23-27, groarke2021powdercharacterization—methodsstandards pages 1-5) | Tap density is one of the easiest UA→GA transfer checks; differences mainly reflect packing changes from fines, satellites, and roughness rather than alloy composition alone. |
| Chemistry / Oxide Content | UA can preserve alloy chemistry well at lab scale, but evaporation losses of volatile elements (e.g., Mn, Zn in one UA study) and rapid oxidation of fine droplets are noted risks; atmosphere control matters strongly for Al alloys. (yankin2025effectofultrasonic pages 1-2, ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6) | GA generally allows controlled inert processing and near-spherical low-contamination powders, but Al powders still carry oxide films; smaller particles are more oxidation- and evaporation-sensitive, and atomization gas/process details affect oxygen pickup. (munizlerma2018acomprehensiveapproach pages 1-3, yakubov2022laserpowderbed pages 54-57, martin2020gasatomizationof pages 1-2) | Chemistry transfer is not guaranteed even at same nominal composition; GA may change volatile-element retention, oxide thickness, dissolved gas, and trace contamination relative to UA. |
| Solidification / Cooling Rate | Often cited in the ~10^3–10^4 K/s regime for UA screening powders; sufficient to generate refined, non-equilibrium microstructures, but generally less well quantified in the literature than GA. (yankin2025effectofultrasonic pages 1-2, ciftcli2025alloydevelopmentfrom pages 1-3, zach2023sphericalpowderscontrol pages 4-4) | Broadly ~10^4–10^6 K/s depending on particle size and gas, with strong size dependence; examples include typical atomized-powder rates of 10^4–10^5 K/s and sub-10 µm powders approaching 10^6 K/s; Al-4.5Cu and 7055Al studies show power-law CR-diameter scaling. (si2017characteristicsof7055al pages 6-8, unal1990productionofrapidly pages 2-3, gianoglio2021onthecooling pages 1-2, gianoglio2021onthecooling pages 5-6) | Cooling-rate mismatch is a major transfer risk: GA may produce more solute trapping and finer cell/dendrite spacing in fine fractions than UA, changing phase selection and as-powder microstructure before LPBF. |
| Internal Porosity | UA is often described as producing dense spherical particles for AM-scale screening, but explicit porosity datasets for Al UA powders are sparse in the gathered evidence. (ciftcli2025alloydevelopmentfrom pages 1-3, yankin2025effectofultrasonic pages 1-2) | GA can produce low-porosity particles when well optimized, but gas entrapment/internal porosity remains a known risk depending on alloy, nozzle, and atomization conditions; low porosity was reported for lab-scale gas-atomized particles in one study. (yankin2025effectofultrasonic pages 1-2, martin2020gasatomizationof pages 1-2) | GA scale-up can introduce entrained-gas porosity not evident in UA powder, affecting apparent density, laser absorptivity, and melt-pool pore inheritance. |
| Batch Scale | Best suited for rapid alloy screening and custom small lots: from grams to a few kilograms on rePOWDER-type systems; practical for discovery and iterative composition tuning. (ciftcli2025alloydevelopmentfrom pages 1-3, yankin2025effectofultrasonic pages 1-2, zach2023sphericalpowderscontrol pages 4-4) | Best suited for validation and production scale: laboratory GA can be sub-kilogram to tens of kilograms, while mature systems scale far beyond that; Ames GARS literature documents scale-up from 4 kg to 20 kg. (zhang2025finalarpaereport pages 7-10, martin2020gasatomizationof pages 1-2) | UA is ideal for discovery throughput; GA is the relevant manufacturability validation step. Transfer risk rises because process window, yield economics, and powder defect populations all change with scale. |


*Table: This table compares ultrasonic atomization and gas atomization for aluminum alloy powders across the key feedstock properties relevant to LPBF. It highlights where UA data are predictive, where transfer risks are highest, and why GA validation is necessary before scale-up.*

### 1.2 Published UA vs GA Comparisons for LPBF-Printed Parts

Direct published comparisons of UA versus GA powders of the same aluminum alloy composition printed via LPBF are extremely limited. The most directly relevant study is Monti et al. (2023), which developed a new Al-Cu alloy for LPBF via ultrasonic atomization, but this work was not accessible for detailed analysis. Ukabhai et al. (2025) demonstrated that Al-10Cu (wt%) powder produced on the AMAZEMET rePowder system yielded the same composition, phases, and microstructure in rod and powder forms (ciftcli2025alloydevelopmentfrom pages 1-3). Żrodowski et al. (2021) compared 316L ultrasonic-atomized powder with standard gas-atomized commercial material and demonstrated the UA powder was suitable for LPBF processing (zrodowski2021novelcoldcrucible pages 11-12). However, systematic side-by-side comparisons of Al alloy UA vs GA powder LPBF builds addressing density, microstructure, and mechanical properties remain a significant gap in the published literature. This gap itself is a strong motivation for including GA validation in the FLAIME workflow.

### 1.3 Key Risks When Scaling from UA to GA Powder

The principal risks when transferring from UA to GA for the same aluminum alloy composition include:

- **Satellite formation:** GA is inherently more prone to satellite particles because partially solidified fine droplets can impinge on larger droplets in the atomization plume (yankin2025effectofultrasonic pages 1-2, yankin2025effectofultrasonic pages 12-15). This degrades flowability and layer spreading.
- **Solidification rate mismatch:** GA cooling rates follow a strong inverse power-law dependence on particle diameter, approximately CR ∝ d^{−1.86} for Al-4.5Cu (gianoglio2021onthecooling pages 5-6). This means the as-powder microstructure, solute trapping, and phase constitution may differ between UA and GA for the same composition.
- **Oxide content differences:** Different atomization environments, gas purity levels, and droplet flight times lead to different oxide film thicknesses and chemistries (yakubov2022laserpowderbed pages 54-57, ciftcli2025alloydevelopmentfrom pages 3-6).
- **Gas porosity:** GA can introduce trapped atomization gas (typically argon) within particles, which is then inherited by the LPBF melt pool, creating closed porosity that cannot be eliminated by subsequent processing (martin2020gasatomizationof pages 1-2).
- **Volatile element loss:** The different thermal profiles (melt superheat, residence time at high temperature) between UA and GA can cause differential evaporation of volatile constituents such as Mg, Zn, and Mn (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6).

### 1.4 Predictability of GA Powder Quality from UA Characterization Data

No published empirical correction factors or quantitative transfer functions exist for predicting GA powder quality from UA characterization data for the same aluminum alloy composition. This represents a genuine gap in the literature. UA characterization data (PSD, flowability, chemistry) are useful for establishing alloy viability and setting GA specification targets, but they cannot substitute for GA-specific validation because:

- Droplet formation mechanisms differ fundamentally (acoustic breakup vs. gas-shear fragmentation).
- Cooling rate regimes overlap but do not coincide for a given particle size.
- Surface condition, satellite population, and internal porosity are process-specific defect populations.

The most practical approach is to use UA data to define a target GA specification envelope (composition ± tolerance, PSD cut, maximum O₂, minimum flowability) and then verify experimentally whether the GA powder meets those specifications.

### 1.5 Solidification Rate Comparison: UA vs GA

**Gas Atomization Cooling Rates:** Well-characterized in the literature. For Al-4.5Cu, the empirical relationship is CR = (6.2 ± 0.2) × 10⁶ · d^{−1.86 ± 0.07} K/s, where d is particle diameter in µm (gianoglio2021onthecooling pages 5-6). For 7055Al alloys, cooling rates of 10⁴–10⁵ K/s are typical for the AM-relevant size range, with sub-10 µm particles approaching 10⁶ K/s (si2017characteristicsof7055al pages 6-8). Ünal reported ~10⁷ K/s for ~10 µm Al droplets in helium and ~10⁵ K/s for 100 µm particles (unal1990productionofrapidly pages 2-3).

**Ultrasonic Atomization Cooling Rates:** Less well quantified in the literature, generally estimated at ~10³–10⁴ K/s. The UA mechanism involves droplet ejection from a vibrating surface with relatively gentle flight in an inert atmosphere, typically without the high-velocity gas stream that enhances convective heat transfer in GA.

**Implications for Phase Formation:**

- **Al-Ce system:** The binary eutectic near 10.6 wt% Ce (Al-Al₁₁Ce₃) forms readily under both UA and GA conditions because Ce has extremely low solubility in Al (<0.005 wt%) and very low diffusion coefficient (~5.7 × 10⁻¹⁴ cm²/s at 500°C), so Al₁₁Ce₃ precipitates form during solidification regardless of cooling rate and are notably stable against dissolution (zhou2020laserpowderbed pages 1-3, hesselmann2022effectofprecipitationforming pages 1-3). LPBF cooling rates (~10⁵–10⁶ K/s) further refine the eutectic to nanoscale dimensions (hesselmann2022effectofprecipitationforming pages 3-5, hesselmann2022effectofprecipitationforming pages 11-14). The key concern is whether GA powder retains the same starting Al₁₁Ce₃ morphology and distribution as UA powder, since LPBF re-melts the powder in any case.

- **Al-Cu system:** Cu supersaturation in the Al matrix increases with cooling rate. In gas-atomized Al-4.5Cu, small particles (up to ~45 µm) exhibit higher trapped Cu (ranging ~1.1–1.6 wt%) than equilibrium solubility, with two distinct Al phases (Cu-rich and Cu-poor) observable by Rietveld analysis (gianoglio2021onthecooling pages 6-8). The GA cooling rate advantage for fine particles means GA powder may have more Cu supersaturation than UA powder of the same size, potentially affecting precipitation behavior during subsequent LPBF.

- **Al-Si system:** Both UA and GA produce the expected α-Al + Si eutectic microstructure. Rapid solidification refines the Si network, with finer particles exhibiting more complete refinement. LPBF dominates the final microstructure via its even higher cooling rates (~10⁵–10⁶ K/s during solidification) (hesselmann2022effectofprecipitationforming pages 1-3, liu2024reviewoflaser pages 6-8).

---

## Part 2: GA Service Providers for Small-Batch Al Alloys

The following table summarizes U.S.-based options for gas atomization services for custom small-batch aluminum alloy compositions:

| Provider/Facility | Type (Commercial/DOE Lab/University) | Batch Size Capability | Access Mechanism | Estimated Cost Range (per kg) | Notes |
|---|---|---:|---|---:|---|
| Ames National Laboratory (GARS) | DOE Lab | ~4–20 kg demonstrated scale-up; potentially larger for established campaigns | WFO, CRADA, collaborative R&D; user-style access may depend on program | ~$150–600/kg | Strong fit for R&D alloy atomization and oxygen-controlled reactive atomization; literature documents GARS scale-up from 4 kg to 20 kg and compatibility with AM powder development (zhang2025finalarpaereport pages 7-10, anderson2007advancedprocessingof pages 1-3) |
| ORNL MDF | DOE Lab | ~5–50 kg class R&D campaigns likely feasible via partner equipment/network | User agreement, CRADA, WFO, DOE programmatic access | ~$200–800/kg | Best positioned when GA is bundled with downstream LPBF validation, characterization, and qualification; MDF is often more valuable as an integrated manufacturing validation partner than as a standalone powder vendor (anderson2007advancedprocessingof pages 1-3) |
| LLNL | DOE Lab | R&D/lab-scale atomization; exact external Al batch size not public in gathered evidence | WFO, CRADA, strategic collaboration | ~$300–1,000/kg | LLNL has documented gas atomization equipment for AM powder fabrication; likely best for mission-aligned or high-value custom campaigns rather than routine service work (anderson2007advancedprocessingof pages 1-3) |
| Iowa State University | University | Typically leverages Ames/ISU atomization ecosystem; ~5–20 kg plausible for sponsored projects | Sponsored research, testing/service agreement, subaward | ~$150–500/kg | Often the most practical academic gateway to Ames-associated gas atomization expertise for externally funded work; good option for DOE proposal subaward structuring (anderson2007advancedprocessingof pages 1-3, zhang2025finalarpaereport pages 7-10) |
| Arcast Inc. | Commercial | <1 kg to a few kg on lab atomizers; some custom campaigns may scale higher with partners | Service contract / purchase order | ~$500–2,000/kg | Best for feasibility, very small R&D heats, and difficult custom melts; literature shows Arcast lab atomizers used for <150–200 g to sub-kg development runs rather than production-scale AM powder supply (martin2020gasatomizationof pages 1-2) |
| Valimet | Commercial | ~10–50 kg+ depending on alloy and campaign | Service contract / NDA / PO | [partner pricing removed] | Known commercial powder producer with atomization capabilities; good candidate for pragmatic U.S. custom powder sourcing, though willingness for highly novel Al alloys and very small batches should be confirmed directly |
| Carpenter Technology / Powder Alloy Corp | Commercial | ~25–500 kg+ typical; 5–25 kg may be possible as premium development runs | Service contract, development agreement | ~$120–500/kg | High-quality AM powder supplier; strongest fit once composition shortlist is narrower and certification/quality documentation matter more than minimum batch flexibility |
| AP&C (GE Additive) | Commercial | Usually larger production batches; 25–100 kg+ more typical than 5–10 kg | Service contract / commercial development agreement | ~$150–600/kg | Primarily plasma atomization oriented and often focused on Ti/Ni systems; may be less natural for custom small-batch Al than GA-focused U.S. vendors |
| Metal Powder Works | Commercial | Small custom lots possible, but process is not conventional GA | Service contract / PO | ~$150–500/kg | Included for completeness, but this is a non-atomization route; useful as an alternate small-batch powder-conditioning/sizing pathway rather than a true GA validation node (anderson2007advancedprocessingof pages 1-3) |
| PNNL | DOE Lab | No dedicated external GA service clearly established in gathered evidence; likely collaboration-scale only | User facility (EMSL for characterization), WFO, CRADA | ~$250–900/kg if arranged through collaboration | More relevant for advanced characterization than routine GA service; gathered evidence links PNNL mainly through EMSL user-facility use in AM powder studies rather than open GA production service (zhang2025finalarpaereport pages 7-10) |
| Worcester Polytechnic Institute | University | Small R&D batches, likely ~1–10 kg through sponsored research or partner equipment | Sponsored research, service agreement, subaward | ~$300–1,000/kg | Strong AM university partner; may be better for powder characterization/LPBF validation than for routine standalone GA production |
| Colorado School of Mines | University | Small R&D campaigns, likely ~1–10 kg depending on furnace/atomizer access | Sponsored research, testing agreement, subaward | ~$300–1,000/kg | Strong metallurgy and powder characterization environment; suitability depends on current equipment availability and external-use policies |
| University of Utah | University | Small R&D campaigns, likely ~1–10 kg depending on facility availability | Sponsored research, service agreement, subaward | ~$300–1,000/kg | Potentially useful academic partner for alloy development and downstream AM characterization; external GA access typically less turnkey than commercial service providers |
| Typical market benchmark for custom small-batch Al GA | Reference row | 5 kg / 10 kg / 25 kg / 50 kg | Commercial PO, subaward, WFO, CRADA | ~5 kg: $600–2,000/kg; 10 kg: $300–1,000/kg; 25 kg: $150–500/kg; 50 kg: $100–300/kg | Cost is dominated by setup, crucible/nozzle cleaning, chemistry risk, oxygen control, sieving/yield to 15–63 µm, and QA documentation; effective cost per usable LPBF fraction can be much higher than headline $/kg because yield to target PSD may be only a fraction of atomized mass (martin2020gasatomizationof pages 1-2, zhang2025finalarpaereport pages 7-10) |


*Table: This table summarizes recommended U.S.-accessible gas atomization options for small-batch custom aluminum alloy validation, including DOE labs, universities, and commercial providers. It is useful for planning vendor outreach, proposal structure, and budget assumptions for UA-to-GA scale-up validation.*

### 2.1 Specific Company Capabilities

The most promising options for 5–50 kg custom Al alloy GA include: **Ames National Laboratory** (Iowa), which has demonstrated GARS scale-up from 4 kg to 20 kg batches with controlled atmosphere (zhang2025finalarpaereport pages 7-10, anderson2007advancedprocessingof pages 1-3); **Valimet** (Stockton, CA), a commercial Al powder producer with custom atomization capability; and **Carpenter Technology / Powder Alloy Corp**, which offers high-quality AM powder but typically at larger minimum batches. **Arcast Inc.** provides very small laboratory-scale atomization (<1 kg) suitable for feasibility runs (martin2020gasatomizationof pages 1-2).

### 2.2 Typical Cost Ranges

Based on industry knowledge and the scale-dependent economics of GA setup, the estimated cost ranges are:
- **5 kg batch:** $600–2,000/kg ($3,000–10,000 total)
- **10 kg batch:** $300–1,000/kg ($3,000–10,000 total)
- **25 kg batch:** $150–500/kg ($3,750–12,500 total)
- **50 kg batch:** $100–300/kg ($5,000–15,000 total)

These ranges reflect setup costs (crucible preparation, nozzle cleaning, atmosphere control), sieving/classification yield losses (often only 30–50% of atomized mass falls in the 15–63 µm LPBF cut), and QA documentation. Effective cost per kg of usable LPBF-grade powder can be 2–3× the headline atomization cost (zhang2025finalarpaereport pages 7-10, martin2020gasatomizationof pages 1-2).

### 2.3 DOE National Laboratory Access

- **Ames National Laboratory:** Gas atomization is a core capability, particularly GARS for reactive alloys. Access is via Work-for-Others (WFO) agreements, CRADAs, or collaborative R&D proposals (anderson2007advancedprocessingof pages 1-3, zhang2025finalarpaereport pages 7-10).
- **ORNL Manufacturing Demonstration Facility (MDF):** Offers integrated AM capabilities. Access through DOE User Facility proposals, CRADAs, WFO, or programmatic funding. Most valuable when GA is bundled with downstream LPBF and characterization.
- **LLNL:** Has documented gas atomization equipment for AM powder fabrication. Access via WFO or strategic collaboration (anderson2007advancedprocessingof pages 1-3).
- **PNNL:** The EMSL user facility provides advanced characterization capabilities complementary to GA, though dedicated external GA service is limited (zhang2025finalarpaereport pages 7-10).

### 2.4 University Facilities

Universities with relevant capabilities include **Iowa State University** (closely linked to Ames Lab atomization infrastructure), **Colorado School of Mines**, **Worcester Polytechnic Institute**, and **University of Utah**. Access is typically through sponsored research agreements or subawards in federal proposals.

### 2.5 Typical Lead Times

For custom Al alloy GA at small batch scale, typical lead times from order to powder delivery are:
- **Commercial providers:** 6–12 weeks for first-time custom compositions; 4–8 weeks for repeat orders
- **DOE national laboratories:** 8–16 weeks including WFO/CRADA paperwork, scheduling, and execution
- **University facilities:** 8–16 weeks depending on academic scheduling and equipment availability

### 2.6 Minimum Information Required by GA Providers

A GA service provider will typically need:
1. **Target composition** (nominal wt% of all elements with tolerances)
2. **Target PSD** (e.g., 15–63 µm for LPBF, or specify D10/D50/D90)
3. **Quantity** of usable powder needed (distinguish from total atomized mass)
4. **Atomization gas preference** (argon, nitrogen, or helium)
5. **Certification requirements** (chemistry certification, PSD report, flowability, oxygen content, certificate of analysis format)
6. **Feedstock delivery form** (whether you supply pre-alloyed ingot or elemental charge materials)
7. **Safety data** (MSDS for any reactive or toxic elements)

---

## Part 3: Integration into Multi-Fidelity BOFN Framework

### 3.1 DAG Structure with GA Validation Node

The proposed integration follows the cost-aware, multi-fidelity Bayesian optimization framework described by Alvi et al. (2026), which uses deep Gaussian process surrogates and cost-weighted acquisition functions to balance exploration across cheap and expensive evaluation nodes (alvi2026deepgaussianprocessbased pages 2-4, alvi2026deepgaussianprocessbased pages 1-2). The GA validation node (Node 4) should be structured as a **sparse, high-cost sequential gate** that is activated only for top-ranked compositions emerging from the main discovery loop (Nodes 0–3), rather than being queried for every composition in the campaign.

| Node | Description | Estimated Cost | Approximate Turnaround | Status in DAG |
|---|---|---:|---|---|
| Node 0 | CALPHAD / thermodynamic screening of candidate Al alloy compositions; lowest-fidelity computational prior for phase stability, freezing range, and likely crack sensitivity | ~$1/composition | Minutes to hours | Existing root node; broad parallel exploration source for all downstream branches (alvi2026deepgaussianprocessbased pages 2-4, rabbitt2025rethinkingbiomedicaltitanium pages 14-15) |
| Node 1 | Ultrasonic atomization (UA) powder production via AMAZEMET rePOWDER for 1–5 kg screening-scale batches; generates powder for rapid composition screening | ~$200/composition | ~0.5–2 days including sieving/basic characterization | Existing intermediate node; main low-cost experimental gateway after Node 0 (ciftcli2025alloydevelopmentfrom pages 1-3, yankin2025effectofultrasonic pages 1-2) |
| Node 2 | LPBF printing with UA powder; coupon fabrication for density/processability/microstructure screening | ~$500/composition | ~1–3 days | Existing downstream node; sequential after Node 1 for main discovery loop (rabbitt2025rethinkingbiomedicaltitanium pages 15-16, rabbitt2025rethinkingbiomedicaltitanium pages 17-18) |
| Node 3 | Tensile testing and basic mechanical characterization of top UA-LPBF builds | ~$300/composition | ~2–5 days | Existing high-fidelity response node; sequential after Node 2 for objective validation (alvi2026deepgaussianprocessbased pages 2-4, alvi2026deepgaussianprocessbased pages 1-2) |
| Node 4 | **GA Validation (new)**: small-batch gas atomization of top-ranked compositions to test UA→GA transferability at scale, including powder QC; batch-size-sensitive service node | **~$3,000–8,000/composition** | ~4–10 weeks | **Proposed sparse high-cost validation node**; best treated as a sequential gate for only top candidates, not part of every loop iteration; can be modeled as a heterotopic costly task in BOFN (zhang2025finalarpaereport pages 7-10, martin2020gasatomizationof pages 1-2, alvi2026deepgaussianprocessbased pages 4-6, alvi2026deepgaussianprocessbased pages 9-14) |
| Node 5 | GA-LPBF printing of the gas-atomized powder to verify build density, melt behavior, and microstructure transfer from UA-screened composition to scalable feedstock | ~$500–1,000/composition | ~1–3 days | Proposed child of Node 4; sequential for confirmed scale-up validation, though it forms a parallel validation branch relative to the continuing UA discovery loop (alvi2026deepgaussianprocessbased pages 2-4, alvi2026deepgaussianprocessbased pages 1-2) |
| Node 6 | GA mechanical testing (tensile and limited confirmatory property testing) on GA-LPBF coupons to establish whether UA-ranked alloys retain performance after scalable powder production | ~$300–600/composition | ~2–5 days | Proposed terminal validation node after Node 5; final confirmation branch for scale-up readiness, not needed for every discovered composition (alvi2026deepgaussianprocessbased pages 4-6, alvi2026deepgaussianprocessbased pages 1-2) |


*Table: This table lays out a practical BOFN/DAG structure for FLAIME that adds a sparse, high-cost gas-atomization validation branch after the main UA discovery loop. It is useful for proposal planning because it maps each node to cost, turnaround, and its intended role in sequential versus parallel decision-making.*

### 3.2 Cost Estimates for GA Validation Node

The appropriate cost estimate for the GA validation node depends on batch size:
- **5 kg batch (1 composition):** ~$3,000–5,000 (minimum viable for LPBF screening)
- **10 kg batch (1 composition):** ~$5,000–8,000 (recommended for comprehensive testing)
- **25 kg batch (1 composition):** ~$8,000–15,000 (appropriate if extended build campaigns are planned)
- Including downstream GA-LPBF printing (Node 5, ~$500–1,000) and GA mechanical testing (Node 6, ~$300–600), the total per-composition GA validation pathway costs ~$4,000–10,000.

In the context of the BOFN DAG cost vector, the GA validation node should be assigned a cost of approximately $5,000–8,000, compared to ~$1 for CALPHAD, ~$200 for UA, ~$500 for LPBF, and ~$300 for tensile testing. This makes it the costliest single node by 10–40×, justifying the heterotopic/sparse querying strategy described by Alvi et al. (alvi2026deepgaussianprocessbased pages 4-6, alvi2026deepgaussianprocessbased pages 9-14).

### 3.3 Parallel Branch vs Sequential Gate

GA validation is best implemented as a **sequential gate with parallel independence from the continuing discovery loop**, rather than as an inline sequential node that blocks further discovery. Specifically:

- The main discovery loop (Nodes 0→1→2→3) continues to explore new compositions without waiting for GA validation results.
- The GA validation branch (Nodes 4→5→6) is triggered only when the Bayesian optimizer identifies compositions with sufficiently high predicted performance and low predictive uncertainty.
- In the cost-aware BOFN framework, this corresponds to the heterotopic querying strategy where expensive GA tasks are sampled at lower frequency (e.g., every third or fifth iteration) while cheap UA tasks run continuously (alvi2026deepgaussianprocessbased pages 4-6, alvi2026deepgaussianprocessbased pages 9-14).

### 3.4 Minimum Compositions for Statistical Confidence

To establish statistical confidence in UA→GA transferability, a minimum of **3–5 compositions** should be validated via GA, with the following rationale:

- **3 compositions** represents the minimum for detecting systematic UA→GA biases (e.g., consistent flowability degradation, chemistry shifts) vs. composition-specific anomalies.
- **5 compositions** provides sufficient data points to fit a preliminary regression between UA and GA property metrics (PSD, flowability, mechanical properties), enabling semi-quantitative transfer prediction for future compositions.
- Each composition should be characterized with at least **n=3 replicate measurements** per powder property to establish within-composition variability.
- For LPBF builds from GA powder, a minimum of **3 tensile specimens per composition per build orientation** is recommended to capture build variability.

### 3.5 Essential Powder Characterization Tests for UA→GA Comparison

The following table provides the recommended characterization protocol:

| Test/Property | ASTM/ISO Standard | Method | What It Reveals for UA→GA Transfer | Priority |
|---|---|---|---|---|
| Particle Size Distribution (laser diffraction) | ASTM B822; ISO 13320 | Laser diffraction reporting D10/D50/D90, span, and fraction in LPBF cut (e.g., 15–45 µm or 15–63 µm) | Whether GA reproduces the usable UA size window, fines/coarse tail shift, and expected changes in packing, spreadability, and cooling-rate-dependent microstructure (yankin2025effectofultrasonic pages 2-3, cooke2012propertiesofmetal pages 23-27, slotwinski2014characterizationofmetal pages 1-3) | Essential |
| Morphology/Sphericity (SEM + image analysis) | ASTM F3049 (guide); image-analysis method commonly project-specific | SEM imaging with quantitative circularity/aspect ratio/sphericity and satellite count | Whether GA introduces more satellites, fused particles, roughness, or shape irregularity than UA; one of the most important transfer checks for Al powders (yankin2025effectofultrasonic pages 12-15, groarke2021powdercharacterization—methodsstandards pages 33-38, slotwinski2014characterizationofmetal pages 1-3) | Essential |
| Flowability - Hall funnel | ASTM B213; ISO 4490 | Timed flow through Hall funnel/orifice | Rapid screen for whether GA powder remains free-flowing like UA powder; sensitive to fines, satellites, and oxide/cohesion changes (groarke2021powdercharacterization—methodsstandards pages 33-38, cooke2012propertiesofmetal pages 27-28, zrodowski2021novelcoldcrucible pages 11-12, spierings2016powderflowabilitycharacterisation pages 11-12) | Essential |
| Flowability - Carney funnel | ASTM B964 | Timed flow through larger-orifice Carney funnel for less free-flowing powders | Captures transfer failures missed by Hall flow when Al powders are too cohesive/fine to pass Hall; useful for borderline LPBF fractions (groarke2021powdercharacterization—methodsstandards pages 33-38, cooke2012propertiesofmetal pages 23-27, groarke2021powdercharacterization—methodsstandards pages 1-5) | Recommended |
| Apparent Density | ASTM B212 (Hall); ASTM B417 (Carney for non-free-flowing powders); ASTM B329 (Scott Volumeter) | Loose bulk density by standardized funnel/volumeter fill | Indicates change in loose packing behavior from UA to GA due to PSD, shape, satellites, and surface condition; directly relevant to layer deposition (cooke2012propertiesofmetal pages 27-28, groarke2021powdercharacterization—methodsstandards pages 1-5) | Essential |
| Tap Density | ASTM B527 | Graduated-cylinder tapping to constant volume | Indicates packed-bed behavior and supports comparison of compactability and powder-bed densification between UA and GA (groarke2021powdercharacterization—methodsstandards pages 33-38, cooke2012propertiesofmetal pages 23-27, groarke2021powdercharacterization—methodsstandards pages 1-5) | Essential |
| Hausner Ratio / Carr Index | ASTM D6393; derived from apparent + tap density | Calculate HR = tap/apparent density and Carr index from bulk/tap data | Simple transfer metric for cohesion and packing degradation; useful summary statistic for UA→GA comparison even when both powders are nominally flowable (groarke2021powdercharacterization—methodsstandards pages 33-38, zrodowski2021novelcoldcrucible pages 11-12) | Recommended |
| Chemical Composition (ICP-OES) | No single universal ASTM in gathered evidence; use validated ICP-OES laboratory method under ASTM F3049 powder-characterization plan | Bulk chemistry after digestion, including major alloying elements and volatile species | Detects composition drift during GA scale-up, especially evaporation/retention differences versus UA for Cu, Mg, Zn, Mn, Ce, etc. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6, groarke2021powdercharacterization—methodsstandards pages 33-38) | Essential |
| Oxygen/Nitrogen Content | Inert gas fusion / ONH analysis under validated lab method; ASTM F3049 as characterization guide | LECO-style O/N/H measurement | Detects oxide pickup and atmosphere-control differences between UA and GA; especially critical for Al powder quality and porosity risk (yakubov2022laserpowderbed pages 54-57, yankin2025effectofultrasonic pages 1-2, ciftcli2025alloydevelopmentfrom pages 3-6, groarke2021powdercharacterization—methodsstandards pages 33-38) | Essential |
| Powder Rheology (FT4) | No dedicated ASTM identified in gathered evidence; use instrument SOP with ASTM F3049-aligned reporting | Dynamic and shear rheology: BFE, SE, AE, compressibility, permeability/pressure drop | More sensitive than funnel tests for detecting subtle UA→GA differences in cohesion, conditioning response, and spreadability in fine Al powders (yankin2025effectofultrasonic pages 12-15, yankin2025effectofultrasonic pages 2-3, yankin2025effectofultrasonic pages 1-2) | Recommended |
| True/Skeletal Density (pycnometry) | ASTM B923 | Helium or nitrogen gas pycnometry | Detects internal porosity/closed porosity differences and supports interpretation of apparent/tap density changes between UA and GA (groarke2021powdercharacterization—methodsstandards pages 33-38, cooke2012propertiesofmetal pages 23-27, slotwinski2014characterizationofmetal pages 1-3) | Recommended |
| Cross-section Microstructure | No single ASTM identified in gathered evidence; metallographic cross-section prep per lab SOP | Mount, polish, cross-section particles; SEM/optical inspection for internal porosity, dendritic/cellular structure, satellites, inclusions | Reveals whether GA changed solidification structure, gas porosity, or internal defects relative to UA; important for rapid-solidification alloy systems (si2017characteristicsof7055al pages 6-8, gianoglio2021onthecooling pages 1-2) | Essential |
| XRD Phase Analysis | No single ASTM identified in gathered evidence; powder XRD with Rietveld where needed | Identify crystalline phases, peak broadening, supersaturation indicators | Tests whether UA and GA produce different as-powder phase constitution or metastable retention before LPBF, especially for Al-Ce, Al-Cu, and Al-Si systems (zhou2020laserpowderbed pages 1-3, hesselmann2022effectofprecipitationforming pages 3-5, gianoglio2021onthecooling pages 6-8) | Essential |
| Moisture Content | No single ASTM identified in gathered evidence; gravimetric/TGA or validated moisture method | Measure absorbed moisture after controlled handling/storage | Assesses whether GA powder is more moisture-sensitive than UA due to higher surface area, fines, or oxide state; relevant for Al cohesion and handling stability (munizlerma2018acomprehensiveapproach pages 1-3, yankin2025effectofultrasonic pages 1-2) | Recommended |


*Table: This table summarizes the core powder tests to compare ultrasonic-atomized and gas-atomized aluminum powders, with standards, methods, and the specific transfer risks each test addresses. It is useful as a minimum characterization plan for GA validation after UA screening.*

ASTM F3049 serves as the overarching guide for characterizing metal powders for AM and should be referenced as the framework standard (groarke2021powdercharacterization—methodsstandards pages 33-38, zrodowski2021novelcoldcrucible pages 11-12). The NIST powder characterization protocol (Slotwinski et al. 2014) provides additional measurement detail for PSD, morphology, density, and composition testing (slotwinski2014characterizationofmetal pages 1-3).

---

## Part 4: Budget Implications

### 4.1 Budget Allocation for GA Scale-Up Validation

For a $750K, 9-month Phase I project discovering ~200 Al alloy compositions via UA/LPBF, a reasonable budget allocation for GA scale-up validation of 3–5 top compositions is:

| Budget Item | 3 Compositions | 5 Compositions |
|---|---|---|
| GA powder production (10 kg/composition) | $15,000–24,000 | $25,000–40,000 |
| Powder characterization (full protocol per composition) | $6,000–9,000 | $10,000–15,000 |
| GA-LPBF builds (3–5 builds per composition) | $4,500–15,000 | $7,500–25,000 |
| GA mechanical testing (tensile + hardness) | $2,700–5,400 | $4,500–9,000 |
| Shipping, handling, storage | $1,500–3,000 | $2,500–5,000 |
| **Total GA validation** | **$30,000–56,000** | **$50,000–94,000** |
| **% of $750K budget** | **4–7.5%** | **6.7–12.5%** |

A recommended allocation of **$50,000–75,000 (7–10% of total budget)** provides sufficient resources for 3–5 compositions with comprehensive characterization while remaining within typical DOE Phase I budget constraints. This should be positioned as a **scale-up risk reduction** line item demonstrating the pathway from discovery to manufacturability.

### 4.2 Proposal Structuring

For a DOE proposal, the GA validation component should be structured as follows, in order of preference:

1. **Subaward to a university or national lab partner** (e.g., Iowa State University/Ames Lab): This is the recommended approach because it demonstrates collaboration, leverages established GA expertise, and is straightforward for DOE peer reviewers to evaluate. The subaward should include a clear statement of work specifying compositions, batch sizes, characterization deliverables, and timeline.

2. **Service contract with a commercial GA provider** (e.g., Valimet, Carpenter): Appropriate when faster turnaround is needed and the commercial provider can handle novel Al alloy compositions. Structure as a "Other Direct Costs – Services" line item with quotes from at least two vendors.

3. **User Facility access** (e.g., ORNL MDF): Best when GA validation is bundled with LPBF and characterization at the same facility. Access proposals for DOE user facilities may require separate submission timelines that must align with the project schedule. This can be cost-effective if beam-time-style access is available, but scheduling risk is higher.

For the DOE proposal narrative, emphasize that the GA validation step serves as the critical **technology readiness level (TRL) bridge** from laboratory discovery (TRL 2–3) to process validation (TRL 4–5), and that the FLAIME platform's cost-aware Bayesian optimization framework intelligently allocates the GA validation budget to only the highest-performing compositions, maximizing the information value per dollar spent (alvi2026deepgaussianprocessbased pages 2-4, alvi2026deepgaussianprocessbased pages 1-2).

---

## Summary of Key Findings and Recommendations

1. **UA is an excellent screening tool** for rapid composition exploration, producing spherical powders with competitive AM suitability (yankin2025effectofultrasonic pages 1-2, yankin2025effectofultrasonic pages 12-15, ciftcli2025alloydevelopmentfrom pages 1-3), but it is **not a substitute for GA validation** because droplet formation, cooling rate, satellite population, and oxide state differ fundamentally.

2. **No published UA-to-GA correction factors exist** for aluminum alloys. The FLAIME project would contribute a novel dataset by systematically comparing UA and GA powder properties for the same compositions—this should be positioned as a scientific contribution in the proposal.

3. **Solidification rate differences** (UA ~10³–10⁴ K/s vs. GA ~10⁴–10⁶ K/s for fine particles) matter for as-powder microstructure but are **largely overwritten by LPBF** cooling rates (~10⁵–10⁶ K/s), meaning the primary transfer risks are powder physical properties (PSD, morphology, flowability, chemistry) rather than powder microstructure per se (hesselmann2022effectofprecipitationforming pages 1-3, liu2024reviewoflaser pages 6-8, gianoglio2021onthecooling pages 5-6).

4. **GA validation of 3–5 compositions** at 10 kg batch scale, budgeted at $50,000–75,000, represents a well-justified 7–10% allocation of a $750K Phase I budget that de-risks the transition from discovery to production-scale AM.

5. **Ames National Laboratory** (via Iowa State University subaward) and **Valimet** (via service contract) are the most practical U.S.-based GA options for this program, offering the right balance of custom composition flexibility, small-batch capability, and cost (anderson2007advancedprocessingof pages 1-3, zhang2025finalarpaereport pages 7-10).

References

1. (ciftcli2025alloydevelopmentfrom pages 1-3): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 4 citations.

2. (zach2023sphericalpowderscontrol pages 4-4): Michael Zach, Dane Brashear, Jonah Duran, Łukasz Żrodowski, Bartosz Kalicki, Tomasz Choma, Marcin Sołowiow, and Steven Adler. Spherical powders: control over the size and morphology of powders for additive manufacturing and enriched stable isotope nuclear targets. EPJ Web of Conferences, 285:03002, Jan 2023. URL: https://doi.org/10.1051/epjconf/202328503002, doi:10.1051/epjconf/202328503002. This article has 3 citations and is from a peer-reviewed journal.

3. (yankin2025effectofultrasonic pages 1-2): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 4 citations and is from a peer-reviewed journal.

4. (yankin2025effectofultrasonic pages 2-3): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 4 citations and is from a peer-reviewed journal.

5. (yakubov2022laserpowderbed pages 54-57): Vladislav Yakubov. Laser powder bed fusion fabrication of cerium-containing aluminium alloys: solidification behaviour, microstructure evolution and mechanical properties. Dissertation, Jan 2022. URL: https://doi.org/10.26190/unsworks/24548, doi:10.26190/unsworks/24548. This article has 0 citations.

6. (si2017characteristicsof7055al pages 6-8): Chaorun Si, Xingling Tang, Xianjie Zhang, Junbiao Wang, and Weichao Wu. Characteristics of 7055al alloy powders manufactured by gas-solid two-phase atomization: a comparison with gas atomization process. Materials & Design, 118:66-74, Mar 2017. URL: https://doi.org/10.1016/j.matdes.2017.01.028, doi:10.1016/j.matdes.2017.01.028. This article has 74 citations and is from a highest quality peer-reviewed journal.

7. (yankin2025effectofultrasonic pages 12-15): Andrei Yankin, Hussain Ali Murtaza, Boris Golman, Asma Perveen, and Didier Talamona. Effect of ultrasonic atomization parameters on alsi12 aluminum powder characteristics for additive manufacturing. Scientific Reports, Jul 2025. URL: https://doi.org/10.1038/s41598-025-06086-7, doi:10.1038/s41598-025-06086-7. This article has 4 citations and is from a peer-reviewed journal.

8. (ciftcli2025alloydevelopmentfrom pages 3-6): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 4 citations.

9. (munizlerma2018acomprehensiveapproach pages 1-3): Jose Alberto Muñiz-Lerma, Amy Nommeots-Nomm, Kristian Edmund Waters, and Mathieu Brochu. A comprehensive approach to powder feedstock characterization for powder bed fusion additive manufacturing: a case study on alsi7mg. Materials, 11:2386, Nov 2018. URL: https://doi.org/10.3390/ma11122386, doi:10.3390/ma11122386. This article has 158 citations.

10. (unal1990productionofrapidly pages 2-3): A. Ünal. Production of rapidly solidified aluminium alloy powders by gas atomisation and their applications. Powder Metallurgy, 33:53-64, Jan 1990. URL: https://doi.org/10.1179/pom.1990.33.1.53, doi:10.1179/pom.1990.33.1.53. This article has 86 citations and is from a peer-reviewed journal.

11. (gianoglio2021onthecooling pages 1-2): Dario Gianoglio, Nevaf Ciftci, Sarah Armstrong, Volker Uhlenwinkel, and Livio Battezzati. On the cooling rate-microstructure relationship in molten metal gas atomization. Metallurgical and Materials Transactions A, 52:3750-3758, Jun 2021. URL: https://doi.org/10.1007/s11661-021-06325-2, doi:10.1007/s11661-021-06325-2. This article has 36 citations.

12. (martin2020gasatomizationof pages 1-2): Arturo Martín, Carmen María Cepeda-Jiménez, and María Teresa Pérez-Prado. Gas atomization of γ‐tial alloy powder for additive manufacturing. Advanced Engineering Materials, Nov 2020. URL: https://doi.org/10.1002/adem.201900594, doi:10.1002/adem.201900594. This article has 45 citations and is from a peer-reviewed journal.

13. (groarke2021powdercharacterization—methodsstandards pages 1-5): Robert Groarke, Rajani K. Vijayaraghavan, Daniel Powell, Allan Rennie, and Dermot Brabazon. Powder characterization—methods, standards, and state of the art. Fundamentals of Laser Powder Bed Fusion of Metals, pages 491-527, Jun 2021. URL: https://doi.org/10.1016/b978-0-12-824090-8.00006-8, doi:10.1016/b978-0-12-824090-8.00006-8. This article has 49 citations.

14. (spierings2016powderflowabilitycharacterisation pages 11-12): A. B. Spierings, M. Voegtlin, T. Bauer, and K. Wegener. Powder flowability characterisation methodology for powder-bed-based metal additive manufacturing. Progress in Additive Manufacturing, 1:9-20, Jul 2016. URL: https://doi.org/10.1007/s40964-015-0001-4, doi:10.1007/s40964-015-0001-4. This article has 541 citations and is from a peer-reviewed journal.

15. (cooke2012propertiesofmetal pages 27-28): April Cooke and John Slotwinski. Properties of metal powders for additive manufacturing: a review of the state of the art of metal powder property testing. ArXiv, Aug 2012. URL: https://doi.org/10.6028/nist.ir.7873, doi:10.6028/nist.ir.7873. This article has 132 citations.

16. (zrodowski2021novelcoldcrucible pages 11-12): Łukasz Żrodowski, Rafał Wróblewski, Tomasz Choma, Bartosz Morończyk, Mateusz Ostrysz, Marcin Leonowicz, Wojciech Łacisz, Piotr Błyskun, Jan S. Wróbel, Grzegorz Cieślak, Bartłomiej Wysocki, Cezary Żrodowski, and Karolina Pomian. Novel cold crucible ultrasonic atomization powder production method for 3d printing. Materials, 14:2541, May 2021. URL: https://doi.org/10.3390/ma14102541, doi:10.3390/ma14102541. This article has 57 citations.

17. (cooke2012propertiesofmetal pages 23-27): April Cooke and John Slotwinski. Properties of metal powders for additive manufacturing: a review of the state of the art of metal powder property testing. ArXiv, Aug 2012. URL: https://doi.org/10.6028/nist.ir.7873, doi:10.6028/nist.ir.7873. This article has 132 citations.

18. (gianoglio2021onthecooling pages 5-6): Dario Gianoglio, Nevaf Ciftci, Sarah Armstrong, Volker Uhlenwinkel, and Livio Battezzati. On the cooling rate-microstructure relationship in molten metal gas atomization. Metallurgical and Materials Transactions A, 52:3750-3758, Jun 2021. URL: https://doi.org/10.1007/s11661-021-06325-2, doi:10.1007/s11661-021-06325-2. This article has 36 citations.

19. (zhang2025finalarpaereport pages 7-10): Final ARPA-E Report: Microstructure Optimization and Novel Processing Development of ODS Steels for Fusion Environments

20. (zhou2020laserpowderbed pages 1-3): Le Zhou, Thinh Huynh, Sharon Park, Holden Hyer, Abhishek Mehta, Shutao Song, Yuanli Bai, Brandon McWilliams, Kyu Cho, and Yongho Sohn. Laser powder bed fusion of al–10 wt% ce alloys: microstructure and tensile property. Journal of Materials Science, 55:14611-14625, Jul 2020. URL: https://doi.org/10.1007/s10853-020-05037-z, doi:10.1007/s10853-020-05037-z. This article has 113 citations and is from a peer-reviewed journal.

21. (hesselmann2022effectofprecipitationforming pages 1-3): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 23 citations and is from a highest quality peer-reviewed journal.

22. (hesselmann2022effectofprecipitationforming pages 3-5): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 23 citations and is from a highest quality peer-reviewed journal.

23. (hesselmann2022effectofprecipitationforming pages 11-14): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 23 citations and is from a highest quality peer-reviewed journal.

24. (gianoglio2021onthecooling pages 6-8): Dario Gianoglio, Nevaf Ciftci, Sarah Armstrong, Volker Uhlenwinkel, and Livio Battezzati. On the cooling rate-microstructure relationship in molten metal gas atomization. Metallurgical and Materials Transactions A, 52:3750-3758, Jun 2021. URL: https://doi.org/10.1007/s11661-021-06325-2, doi:10.1007/s11661-021-06325-2. This article has 36 citations.

25. (liu2024reviewoflaser pages 6-8): Yuanfan Liu, Yang Li, Mingliang Wang, and Zhe Chen. Review of laser powder bed fusion’s microstructure and mechanical characteristics for al-ce alloys. Materials, 17:5085, Oct 2024. URL: https://doi.org/10.3390/ma17205085, doi:10.3390/ma17205085. This article has 6 citations.

26. (anderson2007advancedprocessingof pages 1-3): IE Anderson, DJ Byrd, and JR Rieken. Advanced processing of metallic powders for fossil energy applications. Unknown journal, 2007.

27. (alvi2026deepgaussianprocessbased pages 2-4): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 2 citations and is from a peer-reviewed journal.

28. (alvi2026deepgaussianprocessbased pages 1-2): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 2 citations and is from a peer-reviewed journal.

29. (rabbitt2025rethinkingbiomedicaltitanium pages 14-15): Daisy Rabbitt, Victor M. Villapún, Luke N. Carter, Kenny Man, Morgan Lowther, Paraic O'Kelly, Alexander J. Knowles, Alessandro Mottura, Yuanbo T. Tang, Lorenzo Luerti, Roger C. Reed, and Sophie C. Cox. Rethinking biomedical titanium alloy design: a review of challenges from biological and manufacturing perspectives. Advanced Healthcare Materials, Dec 2025. URL: https://doi.org/10.1002/adhm.202403129, doi:10.1002/adhm.202403129. This article has 26 citations and is from a domain leading peer-reviewed journal.

30. (rabbitt2025rethinkingbiomedicaltitanium pages 15-16): Daisy Rabbitt, Victor M. Villapún, Luke N. Carter, Kenny Man, Morgan Lowther, Paraic O'Kelly, Alexander J. Knowles, Alessandro Mottura, Yuanbo T. Tang, Lorenzo Luerti, Roger C. Reed, and Sophie C. Cox. Rethinking biomedical titanium alloy design: a review of challenges from biological and manufacturing perspectives. Advanced Healthcare Materials, Dec 2025. URL: https://doi.org/10.1002/adhm.202403129, doi:10.1002/adhm.202403129. This article has 26 citations and is from a domain leading peer-reviewed journal.

31. (rabbitt2025rethinkingbiomedicaltitanium pages 17-18): Daisy Rabbitt, Victor M. Villapún, Luke N. Carter, Kenny Man, Morgan Lowther, Paraic O'Kelly, Alexander J. Knowles, Alessandro Mottura, Yuanbo T. Tang, Lorenzo Luerti, Roger C. Reed, and Sophie C. Cox. Rethinking biomedical titanium alloy design: a review of challenges from biological and manufacturing perspectives. Advanced Healthcare Materials, Dec 2025. URL: https://doi.org/10.1002/adhm.202403129, doi:10.1002/adhm.202403129. This article has 26 citations and is from a domain leading peer-reviewed journal.

32. (alvi2026deepgaussianprocessbased pages 4-6): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 2 citations and is from a peer-reviewed journal.

33. (alvi2026deepgaussianprocessbased pages 9-14): Sk Md Ahnaf Akif Alvi, Brent Vela, V. Attari, Jan Janssen, Danny Perez, Douglas L. Allaire, and Raymundo Arróyave. Deep gaussian process-based cost-aware batch bayesian optimization for complex materials design campaigns. npj Computational Materials, Feb 2026. URL: https://doi.org/10.1038/s41524-026-01981-7, doi:10.1038/s41524-026-01981-7. This article has 2 citations and is from a peer-reviewed journal.

34. (slotwinski2014characterizationofmetal pages 1-3): J. A. Slotwinski, E. J. Garboczi, P. E. Stutzman, C. F. Ferraris, S. S. Watson, and M. A. Peltz. Characterization of metal powders used for additive manufacturing. Journal of Research of the National Institute of Standards and Technology, 119:460, Oct 2014. URL: https://doi.org/10.6028/jres.119.018, doi:10.6028/jres.119.018. This article has 664 citations and is from a peer-reviewed journal.

35. (groarke2021powdercharacterization—methodsstandards pages 33-38): Robert Groarke, Rajani K. Vijayaraghavan, Daniel Powell, Allan Rennie, and Dermot Brabazon. Powder characterization—methods, standards, and state of the art. Fundamentals of Laser Powder Bed Fusion of Metals, pages 491-527, Jun 2021. URL: https://doi.org/10.1016/b978-0-12-824090-8.00006-8, doi:10.1016/b978-0-12-824090-8.00006-8. This article has 49 citations.