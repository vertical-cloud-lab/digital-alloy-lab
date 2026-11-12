<!--
Edison Scientific LITERATURE task (batch 5)
- Task ID: 332a778e-556a-4651-a1b9-30c710b8332e
- Submitted: 2026-10-17T06:20:07Z
- Fetched: 2026-10-17T06:51:56Z (status: success)
- Raw trajectory JSON: ../raw/b5-06-corrosion-metrology-cu.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What are the known pitfalls in measuring corrosion rates of copper
alloys (Cu-Ni, NAB) electrochemically, and what protocol gives defensible
numbers? Cover Tafel extrapolation when the cathodic reaction is
oxygen-diffusion limited, Stern-Geary B values used for Cu-Ni and NAB in
LPR (ASTM G59/G102), EIS equivalent circuits for duplex Cu2O films, effects
of surface finish and pre-immersion time, reference electrodes in seawater,
substitute ocean water (ASTM D1141) vs 3.5% NaCl vs natural seawater, and
how selective phase corrosion depth is measured after immersion
(cross-sections, profilometry, CT). Recommend a protocol for a one-hour
screen plus 30-day immersion on small AM coupons.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: What are the known pitfalls in measuring corrosion rates of copper
alloys (Cu-Ni, NAB) electrochemically, and what protocol gives defensible
numbers? Cover Tafel extrapolation when the cathodic reaction is
oxygen-diffusion limited, Stern-Geary B values used for Cu-Ni and NAB in
LPR (ASTM G59/G102), EIS equivalent circuits for duplex Cu2O films, effects
of surface finish and pre-immersion time, reference electrodes in seawater,
substitute ocean water (ASTM D1141) vs 3.5% NaCl vs natural seawater, and
how selective phase corrosion depth is measured after immersion
(cross-sections, profilometry, CT). Recommend a protocol for a one-hour
screen plus 30-day immersion on small AM coupons.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.


# Measuring corrosion of as-deposited Cu–Ni and nickel–aluminum bronze

**Bottom line.** A one-hour electrochemical measurement is a *screen of a newly exposed surface*, not a defensible estimate of its 30-day seawater penetration rate. Report open-circuit potential (OCP), solution-resistance-corrected polarization resistance and impedance as time-stamped measurements; reserve claims of corrosion rate and repair suitability for independently measured metal loss and maximum local attack after immersion. On cast NAB, in-situ measurements found approximately **500 nm of selective β′-phase attack by 150 minutes** even as a protective film developed. On wrought 70/30 Cu–Ni, reported polarization-derived current fell from **8.44 to 1.01 µA cm⁻² over 10 days** in aerated simulated seawater. Neither observation can be inferred reliably from the first hour alone. (ding2019evolutionofthe pages 9-12, ding2019evolutionofthe pages 12-14, yuan2007surfacecharacterizationand pages 5-8)

## Measurement pitfalls and decisions

1. **Tafel extrapolation and oxygen transport.** The cathodic reaction in aerated seawater is predominantly oxygen reduction. A limiting-current plateau, curved branch, or film/diffusion-controlled response is **not** a cathodic Tafel region; extrapolating its apparent slope to obtain *i*₍corr₎, or using that slope to calculate Stern–Geary *B*, produces a model-dependent number. Sulfide exposure, for example, shifted reported 70/30 Cu–Ni cathodic slopes from approximately 130–150 to 182–189 mV decade⁻¹, and the authors attributed the changed response to oxygen-reduction transport limitation. Low-frequency EIS diffusion tails are not uniquely diagnostic of oxygen transport: soluble copper species and transport through a corrosion-product layer are also possibilities. If two convincingly linear, activation-controlled branches are absent, label a polarization fit **“apparent *i*₍corr₎”** or do not report one. Use destructive, wide-range scans only on separate sacrificial coupons, not on coupons destined for immersion. (yuan2007surfacecharacterizationand pages 5-8, yuan2007surfacecharacterizationand pages 8-11, zhao2022thelaserdeposited pages 10-13, abreu2024influenceofdeep pages 10-12)

2. **LPR and the actual *B* values.** With area-normalized, uncompensated-solution-resistance-corrected *R*ₚ, the conditional relationship is *i*₍corr₎ = *B*/*R*ₚ, where *B* = βₐ|β꜀|/[2.303(βₐ + |β꜀|)]. ASTM G59-style LPR measures the near-OCP slope; ASTM G102-style conversion of current to penetration additionally requires an appropriate equivalent weight and alloy density. **Neither makes 26 mV a universal Cu–Ni or NAB constant.** From Yuan and Pehkonen’s published slopes for pristine 70/30 Cu–Ni, *B* calculated for freshly polished and ten-day-exposed material is approximately **20.1 and 24.3 mV**, respectively. From Zhao and colleagues’ NAB slopes, calculated *B* for N-1/N-2/N-3 is approximately **20.8/28.0/25.2 mV**. These are *calculated from those authors’ fitted curves*, not independently validated calibration constants; diffusion-limited curves invalidate the underlying activation-control assumption. Report raw *R*ₚ in Ω cm², the slopes and provenance of any *B*, sensitivity to plausible *B* values, and a gravimetrically calibrated rate separately. A single equivalent weight is particularly inadequate as a description of phase-selective NAB attack. (macdonald1990someadvantagesand pages 2-3, yuan2007surfacecharacterizationand pages 5-8, zhao2022thelaserdeposited media e16dd9cf, ding2019evolutionofthe pages 9-12)

3. **EIS is a film measurement, not an automatic rate meter.** Yuan and Pehkonen fitted newly exposed 70/30 Cu–Ni with a charge-transfer/diffusion model, one-day exposure with a film model, and three-to-ten-day exposure with a **three-time-constant duplex-film model**: solution resistance, interfacial charge-transfer/CPE response, outer porous-film resistance/CPE and inner compact-film resistance/CPE. XPS supported **inner Cu₂O and outer CuO**; at ten days fitted outer and inner resistances were approximately **0.622 and 19.84 kΩ**, respectively, with *R*꜀ₜ **13.75 kΩ**. Sulfide produced a different, porous Cu₂S-rich film. **Do not transfer Cu–Ni layer chemistry to NAB:** a cast-NAB study identified an **Al-rich inner and Cu-rich outer** film, 4.3 µm thick after 240 h in 3.5 wt% NaCl. For each exposure time fit the *fewest* physically credible circuits supported by distinguishable Bode-phase features; disclose frequency range, perturbation, CPE exponents, fitted parameter uncertainty/residuals and whether the low-frequency intercept was actually reached. A low-frequency |Z| value, *R*꜀ₜ, film resistance and DC *R*ₚ are not interchangeable; equivalent circuits alone do not establish chemical identity. (yuan2007surfacecharacterizationand pages 11-15, yuan2007surfacecharacterizationand media 735d685f, yuan2007surfacecharacterizationand pages 8-11, ding2019evolutionofthe pages 3-6, macdonald1990someadvantagesand pages 1-2)

4. **Surface finish, clock start, and edges.** A rough as-built DED surface has different exposed area, oxide history and crevice geometry from a polished metallographic face. Compare candidates and wrought C71500 at a **matched specified finish**, document *R*ₐ/topography, and test a second, application-relevant machined/as-deposited condition separately. Mask edges and seal electrical connections; inspect the mask line after exposure. Do not chemically etch the electrochemical face. Fix immersion time from first wetting and record OCP versus time: published NAB examples used **20 minutes** before electrochemistry or **3,600 seconds** before EIS; cast NAB required **60 minutes** for quasi-stationary OCP in another study, and selective attack continued beyond that. These are different experimental states, not interchangeable equilibration rules. A one-hour OCP/EIS/LPR sequence must therefore be designed so it genuinely finishes within one hour; if not, call it a longer test. (zhao2022thelaserdeposited pages 2-4, huo2025modulatingheatinput pages 4-5, abreu2024influenceofdeep pages 4-5, ding2019evolutionofthe pages 9-12)

5. **Reference electrodes and seawater.** State both the electrode and **its filling solution** with every potential. One deposited-NAB study used saturated-KCl Ag/AgCl (**+0.1981 V versus SHE**, as specified by the authors); another used SCE, and cast-NAB authors specified SCE as approximately **+0.242 V versus SHE**. Thus their unconverted *E*₍corr₎ values differ in reference scale by approximately 44 mV before any material effect is considered. Calibrate reference potential before/after a run, minimize junction-potential and chloride-contamination changes, and isolate any reference electrolyte with a suitable bridge when necessary; never compare unconverted SCE, saturated-KCl Ag/AgCl and seawater Ag/AgCl potentials as though identical. (zhao2022thelaserdeposited pages 2-4, huo2025modulatingheatinput pages 4-5, abreu2024influenceofdeep pages 4-5)

6. **“Seawater” must be identified chemically and biologically.** ASTM D1141 **substitute ocean water** is a reproducible abiotic qualification/screening medium if prepared to its stated recipe; **3.5 wt% NaCl is not ASTM D1141 or natural seawater**. The 70/30 Cu–Ni film study used a *different*, explicitly specified nine-salt synthetic seawater at pH **8.2 ± 0.1**, 25 ± 0.1 °C, stagnant and air-equilibrated; it should not be relabeled D1141. Hold and disclose salinity, pH, dissolved oxygen, temperature, replenishment and flow. Natural seawater additionally introduces variable microbes, nutrients and reduced sulfur: **10 ppm sulfide raised initial reported Cu–Ni current from 8.44 to 87.39 µA cm⁻²** in the cited synthetic-water comparison. Neither stagnant NaCl nor clean synthetic water proves resistance under natural seawater or shipboard flow. (yuan2007surfacecharacterizationand pages 3-5, yuan2007surfacecharacterizationand pages 5-8, yuan2007surfacecharacterizationand pages 8-11)

## Directly useful studies and quantitative benchmarks

**[CITE] [NUMBERS] [NAVY] [GAP]** S. J. Yuan and S. O. Pehkonen, “Surface characterization and corrosion behavior of 70/30 Cu–Ni alloy in pristine and sulfide-containing simulated seawater,” *Corrosion Science* **49** (2007), 1276–1304. **DOI: 10.1016/j.corsci.2006.07.003.** **Process:** wrought/as-received plate, not AM. **Composition, wt%:** Cu 67.84, Ni 30.6, Fe 0.63, Mn 0.6, Zn 0.02, C 0.018, S 0.002, traces. **Test:** stagnant, aerated nine-salt simulated seawater, pH 8.2 ± 0.1, 25 ± 0.1 °C; fresh and 1/3/6/10 days; 1200-grit finish; Ag/AgCl; EIS 100 kHz–5 mHz, 10 mV; optional initial 10 ppm sulfide. **Numbers:** pristine fitted polarization *i*₍corr₎ 8.44 → 1.01 µA cm⁻²; fitted *R*꜀ₜ 1.27 → 13.75 kΩ at 0 → 10 days. Sulfide initial *i*₍corr₎ 87.39 µA cm⁻². **Interpretation:** directly relevant C71500 benchmark and duplex Cu₂O/CuO-film model; no measured 30-day metal-loss or D1141 qualification here. “[NAVY]” denotes the marine service application, **not** verified DoD funding. (yuan2007surfacecharacterizationand pages 3-5, yuan2007surfacecharacterizationand pages 5-8, yuan2007surfacecharacterizationand pages 11-15, yuan2007surfacecharacterizationand media 735d685f)

**[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK] [GAP]** L. Zhao, K. Li, J. Yao, Y. Yuan and B. Du, “The laser deposited nickel-aluminum bronze coatings on SUS630 stainless steel and its corrosion resistance in 3.5 wt.% NaCl solution,” *Metals* **12** (2022), 781. **DOI: 10.3390/met12050781.** **Process:** powder-fed laser deposition/cladding, with either no interlayer or a separate Ni–Al or Ni–Cr powder interlayer; **not** single-stream, single-composition repair of cast NAB or wrought Cu–Ni. **Powder wt%:** NAB Cu 81.1, Al 10.8, Ni 4.1, Fe 4.0; reported size **53–120 µm**, with no verified Hall-flow/oxygen benchmark. **Test:** polished 1 cm², 3.5 wt% NaCl at 25 ± 5 °C, 20-min pre-immersion, saturated-KCl Ag/AgCl, triplicates; 21-day immersion and cross-sections. **Numbers:** direct/interlayer-NiAl/interlayer-NiCr *i*₍corr₎ **7.82/4.65/4.09 µA cm⁻²**, *E*₍corr₎ **−248/−255/−252 mV versus Ag/AgCl**, and maximum reported cross-sectional attack **3.4 ± 0.1/2.0 ± 0.1/1.8 ± 0.1 µm**; as-deposited NAB tensile strength **669 ± 10.4 MPa**, elongation **17.46 ± 1.2%**. Fe-rich dilution degraded direct-on-steel performance. Its mass **increased** at some later exposures as corrosion products accumulated, demonstrating why uncleaned mass change cannot be treated as metal loss. The paper reports dense coatings but **does not quantify porosity**, nor demonstrate a 30-day natural-seawater result. “[NAVY]” denotes propeller/marine relevance, not verified DoD funding. (zhao2022thelaserdeposited pages 2-4, zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited media e16dd9cf, zhao2022thelaserdeposited pages 13-14)

**[CITE] [NUMBERS] [NAVY] [GAP]** Y. Ding, R. Zhao, Z. Qin, Z. Wu, L. Wang, L. Liu and W. Lu, “Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % NaCl solution,” *Materials* **12** (2019), 209. **DOI: 10.3390/ma12020209.** **Process:** cast C95800-type NAB, **wt%** Cu balance, Al 9.22, Fe 4.17, Ni 4.17, Mn 1.23. **Test:** aerated 3.5 wt% NaCl at 20 ± 2 °C; 48/120/240 h immersion, plus in-situ AFM/SVET through 180 min; polished to 0.5 µm; SCE reference. **Numbers:** lamellar α in α+κIII attacked approximately **25 nm at 60 min**, β′ attack exceeded **50 nm at 60 min** and approached **500 nm at 150 min**; corrosion-product film thickness **4.3 µm at 240 h**, **not** 4.3 µm metal loss. The study motivates reporting phase-specific penetration independently of average-current estimates. Marine relevance is clear; Navy funding was **not verified**. (ding2019evolutionofthe pages 1-3, ding2019evolutionofthe pages 3-6, ding2019evolutionofthe pages 9-12)

**[CITE] [NUMBERS] [NAVY] [NOVELTY-RISK] [GAP]** R. Huo *et al.*, “Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing,” *Materials* **18** (2025), 2205. **DOI: 10.3390/ma18102205.** **Process:** **wire-arc DED/CMT**, not laser-powder DED. **Feed wire wt%:** Cu balance, Al 8.73, Fe 5.90, Ni 4.52, Mn 1.39. **Test:** as-deposited polished surface, aerated 3.5 wt% NaCl at 25 ± 5 °C, SCE, 3,600-s OCP before EIS, EIS 10⁵–10⁻² Hz at 3 mV; no reported long natural-seawater immersion. **Numbers:** increasing heat input **243.8 → 644.7 J mm⁻¹** changed fitted-polarization *i*₍corr₎ **2.56 ± 0.04 → 7.52 ± 0.07 µA cm⁻²**, *E*₍corr₎ **−269.61 ± 40 → −700.94 ± 15 mV versus SCE**, fitted film resistance **1,152 → 185.8 Ω cm²**, and measured hardness **192.4 ± 6.9 → 166.9 ± 0.3 HV**. Already demonstrates that as-deposited NAB corrosion depends strongly on deposition thermal input; do not claim that general relationship as new. Marine application, not verified Navy funding. (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 13-15)

**[CITE] [NUMBERS] [GAP]** D. D. Macdonald, “Some Advantages and Pitfalls of Electrochemical Impedance Spectroscopy,” *Corrosion* **46** (1990), 229–242. **DOI: 10.5006/1.3585096.** **Process:** methodological paper including conventionally produced 90/10 and 70/30 Cu–Ni exposed to **flowing seawater**, rather than AM; detailed composition beyond nominal Cu/Ni and 30-day penetration were not established here. A reported example used **1.62 m s⁻¹**, **26 °C**, and dissolved oxygen **0.85 mg L⁻¹**. Small-amplitude AC, potential-step and linear-polarization measurements yielded comparable *R*ₚ versus exposure time. This supports checking *R*ₚ by more than one small-signal method **under fixed flow and oxygen**, not inferring absolute metal loss from *R*ₚ without a valid *B*. (macdonald1990someadvantagesand pages 1-2, macdonald1990someadvantagesand pages 2-3, macdonald1990someadvantagesand pages 3-5)

**[CITE] [GAP]** C. M. Abreu, I. Feijoo, G. Pena and M. C. Pérez, “Influence of Deep Cryogenic Treatment on the Mechanical Properties and Corrosion Resistance of Nickel–Aluminum Bronze,” *Corrosion and Materials Degradation* **5** (2024), 624–640. **DOI: 10.3390/cmd5040030.** **Process:** cast C95800, with subsequent cryogenic/annealing treatments—**not an as-deposited comparator**. **Wt%:** Cu balance, Al 8.96, Ni 4.93, Fe 5.09, Mn 1.24, Si 0.09, Zn 0.53, others 0.06. **Test:** 3.5% NaCl adjusted to pH 7.9, SCE, 60-min OCP, EIS at 1–72 h. **Numbers:** a fitted one-hour charge-transfer parameter *R*₁ of **4,055 Ω cm²** for the cryogenic-only condition; other treatments differed. Its one-time-constant-plus-Warburg interpretation, unlike the aged Cu–Ni three-time-constant circuit, reinforces choosing a circuit by measured time constants rather than prescribing “duplex” at one hour. (abreu2024influenceofdeep pages 2-4, abreu2024influenceofdeep pages 4-5, abreu2024influenceofdeep pages 12-14)

**[CITE] [NOVELTY-RISK] [GAP]** A. V. Nemani, M. Ghaffari, K. S. Bokati, N. Valizade, E. Afshari and A. Nasiri, “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review,” *Journal of Manufacturing and Materials Processing* **8** (2024), 54. **DOI: 10.3390/jmmp8020054.** **Process:** review spanning LPBF, WAAM and laser DED. It identifies **powder laser-metal-deposited Cu–9Al–5Fe–5Ni NAB**, reporting reviewed mechanical ranges of **593–713 MPa yield**, **769–949 MPa tensile strength** and **10–12% elongation**; those are **not corrosion results**. It also describes CuNi2SiCr laser-DED repair deposition onto cast NAB as porous and mechanically unsuitable in the cited example. **Composition/medium/duration:** not reported sufficiently in those review passages for defensible numerical corrosion comparison. These antecedents preclude claiming first-ever NAB powder laser DED or first-ever deposition on cast NAB; the defensible distinction to test is an optimized, characterized **single pre-alloyed feed**, as-deposited seawater performance and explicit comparison to wrought C71500. The review predates later relevant 2025–2026 papers; absence from it does **not** establish an exhaustive present-day novelty search. (nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 79-83)

## Recommended small-coupon protocol

**One-hour, low-cost ranking—not a 30-day corrosion-rate claim.** For each composition and powder lot record actual powder and deposit composition, size distribution, Hall flow, apparent density and oxygen, plus polished-section porosity/crack fraction and deposit/substrate dilution. Include matched wrought C71500 and cast NAB in every batch; stratify deposit-on-self, deposit-on-NAB and deposit-on-wrought-Cu–Ni. Use at least three independently prepared coupons per condition, with a measured, identically finished exposed face of approximately **1 cm²**, sealed edges, and a separate rough/as-deposited-surface cohort. Start the exposure clock at first wetting. Use fresh, aerated **ASTM D1141 substitute ocean water**, fixed temperature (for example **25 ± 1 °C**), fixed quiescent cell geometry or a specified reproducible flow, and log pH, salinity and dissolved oxygen; run 3.5 wt% NaCl only as an explicitly labeled cheap *secondary* medium. Record OCP continuously to 60 minutes; acquire a **short, prespecified, 5–10 mV near-OCP LPR** and a **bounded-time, 5–10 mV EIS** at OCP if both can finish within the hour. Set the minimum EIS frequency according to this time budget and report the actual low-frequency limit rather than implying a resolved DC intercept. Time-stamp every quantity; obtain independent sacrificial coupons for any wider polarization scan. Rank primarily on soundness, OCP evolution, reproducible *R*ₚ and impedance, **not** an unverified Stern–Geary-derived mm y⁻¹. Published Cu–Ni and NAB experiments support these measurement types but do not validate this particular 60-minute composite protocol as a predictor of 30-day loss. (yuan2007surfacecharacterizationand pages 3-5, zhao2022thelaserdeposited pages 2-4, huo2025modulatingheatinput pages 4-5, macdonald1990someadvantagesand pages 2-3, ding2019evolutionofthe pages 9-12)

**Thirty-day, higher-cost qualification.** Run fresh replicate coupons and both controls for **30 days/720 h**, first under controlled aerated D1141 and, for finalists, in separately documented **natural seawater** with defined sourcing, filtration policy, refresh/flow and biological conditions. Use sufficient solution volume and planned renewal to avoid unreported pH/oxygen drift; record OCP and minimally perturbative EIS/LPR at baseline and, for example, days **1, 3, 7, 14 and 30**, with readings on dedicated unpolarized controls where practicable. Preserve representative *unstripped* coupons for cross-sectional oxide/phase analysis. On other coupons photograph and inspect **before** cleaning; then use an alloy-validated, controlled corrosion-product removal and blank-correction procedure, weigh to an appropriate precision, and report **30-day mass loss per area per time** and an equivalent *average* thickness-loss rate using measured density. Report cleaned and uncleaned masses independently: deposited NAB has shown mass gain from accumulated products despite underlying attack. Compare each candidate and C71500 within the **same medium, finish, flow, temperature and 30-day run**, with replicate scatter. (yuan2007surfacecharacterizationand pages 3-5, yuan2007surfacecharacterizationand pages 5-8, zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 2-4)

**Selective attack and interfaces.** Before immersion map fiducial-marked surfaces and obtain baseline optical/confocal profilometry. After immersion acquire **registered 3D confocal/white-light profiles**, preferably across retained masked reference lands, and report maximum metal recession, distribution/percentiles and affected area—not corrosion-product thickness. Section **multiple preselected plus worst-looking locations** normal to the surface and across both sides of each repair interface; vacuum-impregnate, polish, examine by SEM/BSE and EDS/EBSD as appropriate, and report maximum penetration below the *original* metal datum together with implicated α, β′, κ, segregation bands, pores or interface. Published laser-deposit work derived micrometre-scale attack from post-immersion cross-sections; in-situ AFM resolved submicrometre phase loss. **Micro-CT** is valuable before/after exposure for connected pores, internal defects and gross/subsurface attack *if calibrated spatial resolution resolves the feature*, but ordinary CT should **not** be represented as proof of the approximately 0.5–3 µm selective-attack depths reported in these studies. No retrieved Cu–Ni/NAB study established a validated CT-to-cross-section detection threshold for this use. (zhao2022thelaserdeposited pages 2-4, zhao2022thelaserdeposited pages 7-10, ding2019evolutionofthe pages 9-12, ding2019evolutionofthe pages 3-6)

**Evidence limits.** The retrieved sources do not establish a universal experimentally validated Cu–Ni/NAB Stern–Geary *B*, a numeric 30-day D1141-versus-NaCl-versus-natural-seawater conversion factor, or a 30-day natural-seawater C71500-equivalent result for the proposed single-stream pre-alloyed laser-DED repairs. Powder Hall-flow/oxygen values, quantitative porosity, and CT-resolved selective-attack depths likewise cannot be supplied for the central deposited-NAB corrosion benchmark without inventing data. Relevant later laser-DED/LPBF and wire-based publications appeared in search results but their full results were not available for verification here; novelty conclusions therefore remain **provisional**. (nemani2024advancementsinadditive pages 26-28, nemani2024advancementsinadditive pages 79-83, zhao2022thelaserdeposited pages 2-4, yuan2007surfacecharacterizationand pages 3-5)

## Top 5 things the PI should know

1. **Make 30-day measured metal loss and maximum selective/interface penetration the pass–fail endpoints;** one-hour electrochemistry is a cost-saving ranker, not a seawater-lifetime claim. (yuan2007surfacecharacterizationand pages 5-8, ding2019evolutionofthe pages 9-12, zhao2022thelaserdeposited pages 7-10)
2. **Never use a diffusion-limited cathodic segment as a Tafel slope, or 26 mV as an unquestioned alloy-independent *B*.** Publish *R*ₚ first and validate any converted rate against cleaned mass loss. (yuan2007surfacecharacterizationand pages 8-11, yuan2007surfacecharacterizationand pages 5-8, zhao2022thelaserdeposited media e16dd9cf)
3. **Benchmark as-deposited candidates directly against wrought C71500 in the same controlled D1141 and confirm finalists in natural seawater;** NaCl alone is insufficient and sulfide can reverse an apparently favorable result. (yuan2007surfacecharacterizationand pages 3-5, yuan2007surfacecharacterizationand pages 8-11)
4. **Expect the controlling film and vulnerable phase to change with time:** Cu–Ni forms an inner Cu₂O-rich protective layer, whereas NAB can expose β′/eutectoid-selective attack before its Al-rich inner film becomes protective. (yuan2007surfacecharacterizationand pages 11-15, ding2019evolutionofthe pages 3-6, ding2019evolutionofthe pages 9-12)
5. **Position novelty narrowly and verifiably:** powder-laser-deposited NAB, deposition on a different substrate, and NAB repair-adjacent work already exist; the proposed distinctive test is reproducible single-pre-alloyed-powder composition design linked to powder quality, dense repair interfaces and **as-deposited 30-day seawater parity with C71500**, not merely “first corrosion-resistant AM copper.” (zhao2022thelaserdeposited pages 2-4, nemani2024advancementsinadditive pages 79-83, nemani2024advancementsinadditive pages 62-68)

References

1. (ding2019evolutionofthe pages 9-12): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

2. (ding2019evolutionofthe pages 12-14): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

3. (yuan2007surfacecharacterizationand pages 5-8): S.J. Yuan and S.O. Pehkonen. Surface characterization and corrosion behavior of 70/30 cu-ni alloy in pristine and sulfide-containing simulated seawater. Corrosion Science, 49:1276-1304, Mar 2007. URL: https://doi.org/10.1016/j.corsci.2006.07.003, doi:10.1016/j.corsci.2006.07.003. This article has 298 citations and is from a highest quality peer-reviewed journal.

4. (yuan2007surfacecharacterizationand pages 8-11): S.J. Yuan and S.O. Pehkonen. Surface characterization and corrosion behavior of 70/30 cu-ni alloy in pristine and sulfide-containing simulated seawater. Corrosion Science, 49:1276-1304, Mar 2007. URL: https://doi.org/10.1016/j.corsci.2006.07.003, doi:10.1016/j.corsci.2006.07.003. This article has 298 citations and is from a highest quality peer-reviewed journal.

5. (zhao2022thelaserdeposited pages 10-13): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

6. (abreu2024influenceofdeep pages 10-12): Carmen M. Abreu, Iria Feijoo, Gloria Pena, and M. Consuelo Pérez. Influence of deep cryogenic treatment on the mechanical properties and corrosion resistance of nickel–aluminum bronze. Corrosion and Materials Degradation, 5:624-640, Dec 2024. URL: https://doi.org/10.3390/cmd5040030, doi:10.3390/cmd5040030. This article has 1 citations.

7. (macdonald1990someadvantagesand pages 2-3): D. D. Macdonald. Some advantages and pitfalls of electrochemical impedance spectroscopy. Corrosion, 46:229-242, Mar 1990. URL: https://doi.org/10.5006/1.3585096, doi:10.5006/1.3585096. This article has 134 citations and is from a peer-reviewed journal.

8. (zhao2022thelaserdeposited media e16dd9cf): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

9. (yuan2007surfacecharacterizationand pages 11-15): S.J. Yuan and S.O. Pehkonen. Surface characterization and corrosion behavior of 70/30 cu-ni alloy in pristine and sulfide-containing simulated seawater. Corrosion Science, 49:1276-1304, Mar 2007. URL: https://doi.org/10.1016/j.corsci.2006.07.003, doi:10.1016/j.corsci.2006.07.003. This article has 298 citations and is from a highest quality peer-reviewed journal.

10. (yuan2007surfacecharacterizationand media 735d685f): S.J. Yuan and S.O. Pehkonen. Surface characterization and corrosion behavior of 70/30 cu-ni alloy in pristine and sulfide-containing simulated seawater. Corrosion Science, 49:1276-1304, Mar 2007. URL: https://doi.org/10.1016/j.corsci.2006.07.003, doi:10.1016/j.corsci.2006.07.003. This article has 298 citations and is from a highest quality peer-reviewed journal.

11. (ding2019evolutionofthe pages 3-6): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

12. (macdonald1990someadvantagesand pages 1-2): D. D. Macdonald. Some advantages and pitfalls of electrochemical impedance spectroscopy. Corrosion, 46:229-242, Mar 1990. URL: https://doi.org/10.5006/1.3585096, doi:10.5006/1.3585096. This article has 134 citations and is from a peer-reviewed journal.

13. (zhao2022thelaserdeposited pages 2-4): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

14. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

15. (abreu2024influenceofdeep pages 4-5): Carmen M. Abreu, Iria Feijoo, Gloria Pena, and M. Consuelo Pérez. Influence of deep cryogenic treatment on the mechanical properties and corrosion resistance of nickel–aluminum bronze. Corrosion and Materials Degradation, 5:624-640, Dec 2024. URL: https://doi.org/10.3390/cmd5040030, doi:10.3390/cmd5040030. This article has 1 citations.

16. (yuan2007surfacecharacterizationand pages 3-5): S.J. Yuan and S.O. Pehkonen. Surface characterization and corrosion behavior of 70/30 cu-ni alloy in pristine and sulfide-containing simulated seawater. Corrosion Science, 49:1276-1304, Mar 2007. URL: https://doi.org/10.1016/j.corsci.2006.07.003, doi:10.1016/j.corsci.2006.07.003. This article has 298 citations and is from a highest quality peer-reviewed journal.

17. (zhao2022thelaserdeposited pages 7-10): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

18. (zhao2022thelaserdeposited pages 13-14): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

19. (ding2019evolutionofthe pages 1-3): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

20. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

21. (huo2025modulatingheatinput pages 13-15): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

22. (macdonald1990someadvantagesand pages 3-5): D. D. Macdonald. Some advantages and pitfalls of electrochemical impedance spectroscopy. Corrosion, 46:229-242, Mar 1990. URL: https://doi.org/10.5006/1.3585096, doi:10.5006/1.3585096. This article has 134 citations and is from a peer-reviewed journal.

23. (abreu2024influenceofdeep pages 2-4): Carmen M. Abreu, Iria Feijoo, Gloria Pena, and M. Consuelo Pérez. Influence of deep cryogenic treatment on the mechanical properties and corrosion resistance of nickel–aluminum bronze. Corrosion and Materials Degradation, 5:624-640, Dec 2024. URL: https://doi.org/10.3390/cmd5040030, doi:10.3390/cmd5040030. This article has 1 citations.

24. (abreu2024influenceofdeep pages 12-14): Carmen M. Abreu, Iria Feijoo, Gloria Pena, and M. Consuelo Pérez. Influence of deep cryogenic treatment on the mechanical properties and corrosion resistance of nickel–aluminum bronze. Corrosion and Materials Degradation, 5:624-640, Dec 2024. URL: https://doi.org/10.3390/cmd5040030, doi:10.3390/cmd5040030. This article has 1 citations.

25. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

26. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

27. (nemani2024advancementsinadditive pages 26-28): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.
