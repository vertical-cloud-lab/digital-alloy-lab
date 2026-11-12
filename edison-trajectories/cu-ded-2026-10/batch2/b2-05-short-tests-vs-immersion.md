<!--
Edison Scientific LITERATURE task (batch 2)
- Task ID: 14416633-6364-4823-b85e-daa613017132
- Submitted: 2026-10-17T05:37:03Z
- Fetched: 2026-10-17T06:08:55Z (status: success)
- Raw trajectory JSON: ../raw/b2-05-short-tests-vs-immersion.json.gz
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

QUESTION: How well do short electrochemical tests predict long immersion or
service results for Cu-Ni and NAB in seawater, and how should a one-hour
screen be designed? Report studies that measured polarization resistance,
corrosion current, breakdown/pitting potential or impedance at several
exposure times (minutes, hours, days, weeks) alongside mass loss or
long-term exposure, and the correlation they found. How long must a fresh
Cu-Ni surface be exposed before LPR or EIS values become stable, and does
pre-filming change the ranking? For NAB selective phase corrosion, how is
attack depth measured after immersion (cross-section metallography, X-ray
CT), what depths are typical after 30-90 days for cast, heat-treated and AM
NAB, and what acceptance limits do the Navy, ship classification societies,
or industry use?

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

QUESTION: How well do short electrochemical tests predict long immersion or
service results for Cu-Ni and NAB in seawater, and how should a one-hour
screen be designed? Report studies that measured polarization resistance,
corrosion current, breakdown/pitting potential or impedance at several
exposure times (minutes, hours, days, weeks) alongside mass loss or
long-term exposure, and the correlation they found. How long must a fresh
Cu-Ni surface be exposed before LPR or EIS values become stable, and does
pre-filming change the ranking? For NAB selective phase corrosion, how is
attack depth measured after immersion (cross-section metallography, X-ray
CT), what depths are typical after 30-90 days for cast, heat-treated and AM
NAB, and what acceptance limits do the Navy, ship classification societies,
or industry use?

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


# Short electrochemical screens for marine Cu–Ni and nickel–aluminium bronze

**Conclusion.** A one-hour electrochemical measurement is useful for detecting grossly poor behaviour, but the retrieved studies do **not** establish that one-hour polarization resistance (LPR), impedance (EIS), or polarization current predicts 30-day mass loss, maximum selective-attack depth, or seawater service life across these alloys. Film formation changes the measured response substantially; localized attack and natural-seawater fouling introduce failure modes that an area-averaged, one-hour measurement can miss. No verified numerical Navy or classification-society acceptance limit for NAB selective-attack depth was found. (yuan2007surfacecharacterizationand pages 5-8, ding2019evolutionofthe pages 6-9, tan2024effectofalni pages 12-16, dobson2024corrosionmechanismsand pages 119-122)

## Evidence, by study

**Yuan, S. J., and S. O. Pehkonen. “Surface characterization and corrosion behavior of 70/30 Cu-Ni alloy in pristine and sulfide-containing simulated seawater.” *Corrosion Science* 49 (2007): 1276–1304. DOI: 10.1016/j.corsci.2006.07.003. [CITE] [NUMBERS]** Process: wrought CDA 715 sheet; measured wt% Cu 67.84, Ni 30.60, Fe 0.63, Mn 0.60, Zn 0.02. Conditions: stagnant, aerated synthetic seawater, pH 8.2 ± 0.1, 25 ± 0.1 °C; polarization and EIS after 0, 1, 3, 6, and 10 days. In clean solution, *i*₍corr₎ was **8.44, 7.76, 4.09, 1.69, and 1.01 µA cm⁻²**, respectively: the fresh value was **8.4 times** the 10-day value. With initially 10 ppm sulfide, fresh-surface current was approximately **87 µA cm⁻²**; despite sulfide disappearing by day 4, current remained approximately **20 µA cm⁻²** late in exposure. Sulfide pre-exposure therefore left a damaging film rather than resetting the specimen to clean-seawater behaviour. This paper measures film-dependent electrochemistry, **not** a correlation with 30-day gravimetric or service outcomes. [GAP] (yuan2007surfacecharacterizationand pages 3-5, yuan2007surfacecharacterizationand pages 5-8)

**Ding, Y., R. Zhao, Z.-B. Qin, Z. Wu, L. Wang, L. Liu, and W. Lu. “Evolution of the Corrosion Product Film on Nickel-Aluminum Bronze and Its Corrosion Behavior in 3.5 wt % NaCl Solution.” *Materials* 12 (2019): 209. DOI: 10.3390/ma12020209. [CITE] [NUMBERS]** Process: conventional NAB; measured wt% Al 9.22, Fe 4.17, Ni 4.17, Mn 1.23, Cu balance. Conditions: 3.5 wt% NaCl, 20 ± 2 °C; electrochemistry initially and after 48, 120, and 240 h; local in-situ measurements over 30–180 min. Across those four bulk measurements, *i*₍corr₎ declined **11.35 → 5.32 → 5.04 → 3.78 µA cm⁻²**, while fitted charge-transfer resistance rose **318 → 3,698 → 10,362 → 35,939 Ω cm²**. These are evolving film measurements, not proof that a fresh one-hour value is stable. At a scratch in an existing 240-h film, local anodic current was approximately **260, 190, 160, and 340 µA cm⁻²** initially and at 30, 60, and 90 min; the 90-min spike illustrates why a single early reading can mislead. Local activity resembled the surrounding filmed surface by approximately **150 min**. In-situ AFM measured approximately **25 nm** attack of eutectoid α at 60 min and β′ attack exceeding **50 nm** at 60 min, approaching **500 nm = 0.5 µm** by 150 min. That 500-nm observation is **not** a 30–90-day penetration benchmark. [GAP] (ding2019evolutionofthe pages 1-3, ding2019evolutionofthe pages 6-9, ding2019evolutionofthe pages 9-12, ding2019evolutionofthe media 9dde056f)

**Tan, Y., H. Xie, X. Feng, S. Huang, W. Zhang, L. Peng, W. Wang, and Y. Zhao. “Effect of Al/Ni Ratio on the Microstructure and Properties of Nickel–Aluminum Bronze Alloys.” *Materials* 17 (2024): 1330. DOI: 10.3390/ma17061330. [CITE] [NUMBERS] [NOVELTY-RISK: composition–corrosion optimisation, but cast rather than DED]** Process: four vacuum-melted, cast alloys; measured Al/Ni/Fe/Mn wt% were **6.94/6.82/4.10/1.72**, **7.90/6.13/3.92/2.12**, **8.94/5.18/4.12/2.18**, and **9.94/3.99/3.94/1.82**, Cu balance. Conditions: static 3.5 wt% NaCl at 25 °C for **30 days**, refreshed weekly; mass-loss specimens and separate electrochemical/SEM specimens. At **10 days**, the four *i*₍corr₎ values in that order were **0.50, 1.34, 1.77, 2.16 µA cm⁻²**; at **30 days**, **0.35, 0.36, 0.69, 0.78 µA cm⁻²**. Polarization-derived *R*ₚ ranked the alloys in the same order at 10 and 30 days. The lowest-Al/highest-Ni alloy had a 30-day mass-loss-derived rate of **0.00267 mm year⁻¹** and the best electrochemical ranking; the two highest-Al alloys had similarly higher gravimetric rates. Thus, **10-day** electrochemistry and **30-day** mass-loss rankings agree qualitatively in this particular four-alloy series; the authors do not establish a one-hour predictor or report a predictive correlation coefficient. Cross-sectional SEM/EDS after 30 days found maximum local depth **greater than 3 µm** in the highest-Al/lowest-Ni alloy, near β′/κIII; an oxide thickness of **1.2–1.5 µm** is reported for a different composition and must not be mistaken for attack depth. Hardness rose approximately **104 → 202 HV**, tensile strength **356 → 751 MPa**, and elongation fell **50.5 → 11.0%** across the composition range. The apparent low-nickel strength gain carried a corrosion and ductility penalty. (tan2024effectofalni pages 2-4, tan2024effectofalni pages 10-12, tan2024effectofalni pages 1-2, tan2024effectofalni pages 12-16, tan2024effectofalni pages 6-10, tan2024effectofalni media 77717194)

**Huo, R., Z. Wang, M. Wang, R. Wang, S. Zhang, C. Zhang, C. Wu, H. Chen, and J. Chen. “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing.” *Materials* 18 (2025): 2205. DOI: 10.3390/ma18102205. [CITE] [NUMBERS] [NOVELTY-RISK: as-deposited AM NAB electrochemistry, but wire-arc rather than powder-laser DED]** Process: cold-metal-transfer **WAAM**, ERCuNiAl wire; nominal wt% Al 8.73, Fe 5.90, Ni 4.52, Mn 1.39, Cu balance. Conditions: 3.5 wt% NaCl, 25 ± 5 °C; **3,600 s OCP** before EIS, then additional OCP monitoring before polarization. Across four increasing-heat-input builds (**243.8–644.7 J mm⁻¹**), *i*₍corr₎ was **2.56 ± 0.04, 3.85 ± 0.11, 5.03 ± 0.08, 7.52 ± 0.07 µA cm⁻²**; measured surface hardness was **192.4 ± 6.9, 182.3 ± 2.8, 178.9 ± 2.9, 166.9 ± 0.3 HV**. The OCP changed rapidly for approximately **150 s** in one build but approximately **2,000 s** in others. Its one-hour procedure demonstrates that an operational **one-hour OCP/electrochemical screen is practicable**, not that Cu–Ni or NAB film properties or corrosion rankings have reached long-term stability. There is no paired 30-day mass-loss or selective-depth validation here. (huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 10-13)

**King, S. *The Hot Isostatic Processing Characteristics of 70/30 Cupronickel Castings* (1992), thesis; DOI not verified. [NUMBERS] [NAVY]** Process: cast approximately 70/30 Cu–Ni for naval components. One-year immersion in natural seawater at Langstone Harbour gave **0.02 mm year⁻¹** mean gravimetric loss versus **0.05 mm year⁻¹** maximum metallographically estimated attack. A probe downstream of a strainer, approximately 1 m inside a submarine hull valve and exposed to approximately **3 m s⁻¹** flow, showed polarization admittance dropping from **18 to 7 pA mV⁻¹ over 40 days**; the later level was interpreted as about **0.05 mm year⁻¹** and monitored for another 50 days. This is useful service-context agreement at **weeks**, not validation of hour-one LPR against one-year loss: flow and measurement locations differ. The thesis describes Royal Navy use of NAB and a chromium-containing Cu–Ni replacement in a naval engineering specification. (king1992thehotisostatic pages 43-49, king1992thehotisostatic pages 27-32)

**Dobson, T. H. E., A. Yunnie, D. Kaloudis, N. Larrosa, and H. Coules. “Biofouling and corrosion rate of welded nickel aluminium bronze in natural and simulated seawater.” *Biofouling* 40 (2024): 193–208. DOI: 10.1080/08927014.2024.2326067. Related primary thesis: Dobson, *Corrosion Mechanisms and Fatigue Behaviour of Marine Biofouled Plasma Welded Nickel Aluminium Bronze* (2024), thesis DOI not verified. [CITE] [NUMBERS] [NAVY: marine welded-component relevance, not verified US-Navy funding]** Process: cast **plasma-welded** NAB, wt% Al 9.14, Fe 4.38, Ni 4.84, Mn 0.09, Cu balance; natural marina seawater versus simulated seawater, including **12- and 18-month** retrievals. The thesis reports simulated-seawater general corrosion rates approximately **tenfold lower** than natural-seawater rates, and identifies macrofouling-associated localized attack. Reported maxima in biofouled parent material were **986 µm pit depth** and **1,331 µm κIII-associated selective-attack depth**; these are long-exposure observations, **not** 30–90-day cast-NAB benchmarks. X-ray CT was used in the broader fatigue investigation at **15.19-µm voxel size**; it must **not** be presented as a validated method for resolving the cited phase-selective penetration. (dobson2024corrosionmechanismsand pages 92-95, dobson2024corrosionmechanismsand pages 235-240, dobson2024corrosionmechanismsand pages 186-190, dobson2024corrosionmechanismsand pages 154-157, dobson2024corrosionmechanismsand pages 119-122)

**Uhlmann, E., J. Polte, J. M. Fasselt, V. Müller, C. Klötzer-Freese, R. Kleba-Ehrhardt, M. Biegler, and M. Rethmeier. “A Comparative Evaluation of Powder Characteristics of Recycled Material from Bronze Grinding Chips for Additive Manufacturing.” *Materials* 17 (2024): 3396. DOI: 10.3390/ma17143396. [CITE] [NUMBERS] [NOVELTY-RISK: ultrasonic-atomized NAB powder for laser DED] [GAP]** Process: remelting/ultrasonic atomization of nominal **CuAl10Fe5Ni5** propeller-grinding chips for prospective **blown-powder laser DED**; **powder characterisation, not a demonstrated corrosion-resistant deposit**. Atomized powder had image-derived size percentiles **48/98/174 µm** (*D*₁₀/*D*₅₀/*D*₉₀), **0.019 wt% oxygen**, **8.62 s/150 g Carney flow**, mean aspect ratio **0.935**, and Hausner ratio **1.05**. The comparable gas-atomized reference contained **0.013 wt% oxygen**; mechanically milled recycled powders contained **0.119–0.190 wt%**. **Carney s/150 g is not Hall s/50 g**; no comparable Hall value or corrosion/immersion result is established. This is especially close to the proposed atomization node but leaves the proposed powder-to-deposit-to-service link open. (uhlmann2024acomparativeevaluation pages 2-4, uhlmann2024acomparativeevaluation pages 10-12, uhlmann2024acomparativeevaluation pages 6-7)

**Fayanas, A., A. Veiga, A. Perez, A. Concustell, S. Molas, and N. Ordas. “Nickel Aluminium Bronze Alloys with Enhanced Erosion-Corrosion Resistance and Mechanical Strength.” *Journal of the Japan Society of Powder and Powder Metallurgy* 72 (2025): S819–S826. DOI: 10.2497/jjspm.15f-t13-08. [CITE] [GAP]** Process: continuous cast versus sinter/HIP and near-net-shape HIP NAB—not laser DED. The cast alloy contained wt% Al 9.7, Ni 4.4, Fe 4.3, Mn 0.9, Cu balance; powder-metallurgy comparators contained approximately **4.5–5 wt% Ni**. Conditions: room-temperature **3.5 wt% NaCl, 480-h** static immersion; OCP monitored **20 min** before polarization. The study addresses film development and processing effects, but the retrieved evidence does not yield a quantified hour-one-to-480-h ranking or selective-attack depth. (fayanas2025nickelaluminiumbronze pages 1-2, fayanas2025nickelaluminiumbronze pages 7-8)

## What one hour can—and cannot—mean

**Fresh-surface stability.** There is **no defensible universal minimum exposure time** after which a freshly prepared Cu–Ni surface’s LPR or EIS is a stable, service-representative value. The measured 70/30 corrosion current was still falling between **day 1 and day 10**; a review of 90/10 Cu–Ni film studies reports substantial Fe/Ni enrichment developing over **6–8 weeks**. NAB data likewise change between fresh exposure and **240 h**. Distinguish a locally steady **OCP over minutes** from a mature corrosion film: neither an OCP plateau nor the end of a one-hour measurement establishes long-term LPR/EIS stability. (yuan2007surfacecharacterizationand pages 5-8, kear2004electrochemicalcorrosionbehaviour pages 4-5, ding2019evolutionofthe pages 6-9, huo2025modulatingheatinput pages 10-13)

**Pre-filming and ranking.** Pre-filming demonstrably changes *values* and can alter the mechanism: clean-seawater filming suppresses Cu–Ni current, whereas sulfide pre-exposure leaves high current even after sulfide is gone. In Tan’s four cast alloys, the **10-day** electrochemical ordering agrees qualitatively with the **30-day** ordering and mass-loss trend. These observations do **not** establish whether **one-hour** clean-water pre-filming reverses any candidate-alloy ranking; that comparison remains an experiment to perform, not a published conclusion. (yuan2007surfacecharacterizationand pages 5-8, tan2024effectofalni pages 10-12, tan2024effectofalni pages 6-10)

**Recommended one-hour screen—an explicitly provisional triage protocol.** Use polished, area-defined, separately tested as-deposited deposit and deposit/substrate-interface specimens, alongside identically prepared wrought C71500 and cast NAB controls. Specify whether the electrolyte is **3.5 wt% NaCl, ASTM D1141 substitute ocean water, or natural seawater**; these are not interchangeable. Record temperature, pH, dissolved oxygen, flow, surface finish and reference electrode; include replicate coupons. Log OCP continuously for up to 60 min and record its *slope*, rather than assuming stabilization at a preset minute. On separate replicates, make a small-amplitude near-OCP LPR measurement and EIS measurement when feasible, explicitly recording exposure age and measurement duration. Reserve destructive wide-range polarization/breakdown tests for separate coupons: sweeping to high anodic potential changes the surface subsequently used for immersion. Compare one-hour response **within matched test conditions** as a flag for unexpectedly high current, low resistance, unstable OCP or localized breakdown—not as an annualized corrosion rate or pass/fail service criterion. Promote diverse candidates, including ambiguous ones, to repeated measurements at **24 h, several days and 10–30 days**, paired **30- and 90-day** mass loss and maximum-depth measurements; test a separately pre-filmed arm and, where relevant, flow, sulfide or natural-water exposure. Fit and prospectively validate the hour-one-to-immersion ranking, reporting rank errors and uncertainty rather than assuming correlation. This design follows the observed timescales and the natural/artificial seawater discrepancy. (yuan2007surfacecharacterizationand pages 3-5, yuan2007surfacecharacterizationand pages 5-8, ding2019evolutionofthe pages 6-9, dobson2024corrosionmechanismsand pages 119-122, huo2025modulatingheatinput pages 4-5)

## Selective-attack measurement and acceptance

For immersion coupons, preserve an **unstripped specimen for surface and cross-sectional SEM/optical metallography with phase identification**; measure penetration from the original metal surface to the deepest connected attacked phase over predefined section lengths and multiple orientations, reporting the **maximum, distribution, and location**, separately from oxide thickness and gravimetric average. Tan’s 30-day sections demonstrate the method and a **>3-µm** cast-alloy observation. AFM resolves Ding’s **submicrometre early phase relief**. CT may locate larger subsurface pits or connected defects without destroying the coupon, but voxel size and corrosion-product contrast must be shown adequate before claiming quantitative micrometre-scale selective-phase depth; Dobson’s **15.19-µm** CT voxels cannot resolve a 3-µm benchmark. (ding2019evolutionofthe pages 3-6, ding2019evolutionofthe pages 9-12, tan2024effectofalni pages 12-16, dobson2024corrosionmechanismsand pages 186-190)

**Missing comparisons and limits.** The retrieved evidence does **not** establish comparable **30–90-day maximum selective-attack depths for heat-treated cast, as-deposited blown-powder DED, WAAM, and LPBF NAB**, nor a Navy/NAVSEA, ABS, DNV, or Lloyd’s numerical maximum-depth acceptance rule. The retrieved UK **Defence Standard 02-747 Part 2** description instead specifies heat treatment of seawater-service NAB castings at **675 ± 15 °C for at least six hours**; that processing requirement is neither a selective-depth limit nor approval of an as-deposited repair. ASTM D1141 describes substitute seawater and ASTM G31 guides immersion testing; neither supplies the missing project-specific selective-depth pass/fail value. Specify any proposed depth limit as a **programme-defined, jointly agreed qualification target**, not as an existing Navy rule. (dobson2024corrosionmechanismsand pages 256-259, dobson2024corrosionmechanismsand pages 59-64)

## Top 5 things the PI should know

1. **Do not train a service-life surrogate as though one-hour *i*₍corr₎ were ground truth.** Fresh 70/30 current fell **8.4-fold in ten days**; measure time-dependent film formation as a model node. (yuan2007surfacecharacterizationand pages 5-8)
2. **Make maximum local depth a separate outcome from mass loss or LPR.** Thirty-day cast NAB showed **>3 µm** phase-associated penetration; substantially deeper long-service, biofouled attack cannot be excluded by low average loss. (tan2024effectofalni pages 12-16, dobson2024corrosionmechanismsand pages 154-157)
3. **Control the seawater condition and film history.** Sulfide pre-exposure persisted after removal, and simulated seawater substantially understated natural-seawater corrosion in the retrieved welded-NAB comparison. (yuan2007surfacecharacterizationand pages 5-8, dobson2024corrosionmechanismsand pages 119-122)
4. **Differentiate novelty precisely.** Independently published work already covers **ultrasonic-atomized NAB feedstock** and **one-hour as-built WAAM electrochemistry**; the defensible proposed gap is validated, as-deposited **single-pre-alloy powder laser-DED** composition-to-long-immersion performance, including dissimilar-substrate repair. (huo2025modulatingheatinput pages 4-5, uhlmann2024acomparativeevaluation pages 13-15, uhlmann2024acomparativeevaluation pages 2-4)
5. **Do not invent a qualification threshold.** Obtain application-specific Navy/classification requirements and negotiate a 30/90-day maximum-depth target; a cast-NAB heat-treatment prescription does not certify an unheated DED deposit. (dobson2024corrosionmechanismsand pages 59-64)

References

1. (yuan2007surfacecharacterizationand pages 5-8): S.J. Yuan and S.O. Pehkonen. Surface characterization and corrosion behavior of 70/30 cu-ni alloy in pristine and sulfide-containing simulated seawater. Corrosion Science, 49:1276-1304, Mar 2007. URL: https://doi.org/10.1016/j.corsci.2006.07.003, doi:10.1016/j.corsci.2006.07.003. This article has 298 citations and is from a highest quality peer-reviewed journal.

2. (ding2019evolutionofthe pages 6-9): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

3. (tan2024effectofalni pages 12-16): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

4. (dobson2024corrosionmechanismsand pages 119-122): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

5. (yuan2007surfacecharacterizationand pages 3-5): S.J. Yuan and S.O. Pehkonen. Surface characterization and corrosion behavior of 70/30 cu-ni alloy in pristine and sulfide-containing simulated seawater. Corrosion Science, 49:1276-1304, Mar 2007. URL: https://doi.org/10.1016/j.corsci.2006.07.003, doi:10.1016/j.corsci.2006.07.003. This article has 298 citations and is from a highest quality peer-reviewed journal.

6. (ding2019evolutionofthe pages 1-3): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

7. (ding2019evolutionofthe pages 9-12): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

8. (ding2019evolutionofthe media 9dde056f): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

9. (tan2024effectofalni pages 2-4): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

10. (tan2024effectofalni pages 10-12): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

11. (tan2024effectofalni pages 1-2): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

12. (tan2024effectofalni pages 6-10): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

13. (tan2024effectofalni media 77717194): Yinxun Tan, Haofeng Xie, Xue Feng, Shuhui Huang, Wenjing Zhang, Lijun Peng, Wanyu Wang, and Yizhi Zhao. Effect of al/ni ratio on the microstructure and properties of nickel–aluminum bronze alloys. Materials, 17:1330, Mar 2024. URL: https://doi.org/10.3390/ma17061330, doi:10.3390/ma17061330. This article has 14 citations.

14. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

15. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

16. (king1992thehotisostatic pages 43-49): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

17. (king1992thehotisostatic pages 27-32): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

18. (dobson2024corrosionmechanismsand pages 92-95): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

19. (dobson2024corrosionmechanismsand pages 235-240): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

20. (dobson2024corrosionmechanismsand pages 186-190): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

21. (dobson2024corrosionmechanismsand pages 154-157): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

22. (uhlmann2024acomparativeevaluation pages 2-4): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

23. (uhlmann2024acomparativeevaluation pages 10-12): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

24. (uhlmann2024acomparativeevaluation pages 6-7): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.

25. (fayanas2025nickelaluminiumbronze pages 1-2): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

26. (fayanas2025nickelaluminiumbronze pages 7-8): Aintzane Fayanas, Angela Veiga, Alejandro Perez, Amadeu Concustell, Silvia Molas, and Nerea Ordas. Nickel aluminium bronze alloys with enhanced erosion-corrosion resistance and mechanical strength. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S819-S826, Mar 2025. URL: https://doi.org/10.2497/jjspm.15f-t13-08, doi:10.2497/jjspm.15f-t13-08. This article has 1 citations.

27. (kear2004electrochemicalcorrosionbehaviour pages 4-5): G. Kear, B.D. Barker, K. Stokes, and F.C. Walsh. Electrochemical corrosion behaviour of 90—10 cu—ni alloy in chloride-based electrolytes. Journal of Applied Electrochemistry, 34:659-669, Jul 2004. URL: https://doi.org/10.1023/b:jach.0000031164.32520.58, doi:10.1023/b:jach.0000031164.32520.58. This article has 238 citations and is from a peer-reviewed journal.

28. (ding2019evolutionofthe pages 3-6): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 60 citations.

29. (dobson2024corrosionmechanismsand pages 256-259): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

30. (dobson2024corrosionmechanismsand pages 59-64): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

31. (uhlmann2024acomparativeevaluation pages 13-15): Eckart Uhlmann, Julian Polte, Janek Maria Fasselt, Vinzenz Müller, Christian Klötzer-Freese, Rafael Kleba-Ehrhardt, Max Biegler, and Michael Rethmeier. A comparative evaluation of powder characteristics of recycled material from bronze grinding chips for additive manufacturing. Jul 2024. URL: https://doi.org/10.3390/ma17143396, doi:10.3390/ma17143396. This article has 11 citations.
