<!--
Edison Scientific LITERATURE task (batch 4)
- Task ID: 56cc4802-3f13-42c0-a2a9-556393227548
- Submitted: 2026-10-17T06:11:09Z
- Fetched: 2026-10-17T06:41:50Z (status: success)
- Raw trajectory JSON: ../raw/b4-02-sonotrode-and-wetting.json.gz
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

QUESTION: Which materials can contact molten copper, Cu-10Ni to Cu-30Ni, and
aluminum bronze at 1150-1300 C as an ultrasonic sonotrode or melt-delivery
nozzle without dissolving, being wetted, or contaminating the powder? Report
wetting angles and dissolution or erosion data for Cu and Cu-Ni melts on
molybdenum and TZM (note Ni-Mo solubility and intermetallics), tungsten,
niobium, tantalum, graphite and carbon fiber, SiC, Si3N4, sialon, alumina,
zirconia, and boron nitride, and any coatings used on ultrasonic horns or
sonotrodes in molten copper (e.g. ultrasonic degassing or melt treatment of
copper alloys). Which would you test first for a 20-60 kHz sonotrode?

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

QUESTION: Which materials can contact molten copper, Cu-10Ni to Cu-30Ni, and
aluminum bronze at 1150-1300 C as an ultrasonic sonotrode or melt-delivery
nozzle without dissolving, being wetted, or contaminating the powder? Report
wetting angles and dissolution or erosion data for Cu and Cu-Ni melts on
molybdenum and TZM (note Ni-Mo solubility and intermetallics), tungsten,
niobium, tantalum, graphite and carbon fiber, SiC, Si3N4, sialon, alumina,
zirconia, and boron nitride, and any coatings used on ultrasonic horns or
sonotrodes in molten copper (e.g. ultrasonic degassing or melt treatment of
copper alloys). Which would you test first for a 20-60 kHz sonotrode?

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


# Melt-contact materials for ultrasonic atomization of copper alloys

**Conclusion.** No material in the retrieved evidence is demonstrated to satisfy *all three* requirements—negligible dissolution, persistent non-wetting, and negligible powder contamination—for Cu, Cu–10–30 wt% Ni, and nickel–aluminum bronze (NAB) throughout 1150–1300 °C under ultrasound. **Test a dense alumina melt-delivery nozzle first and a replaceable, uncoated TZM sonotrode tip first**, with graphite and dense zirconia as nozzle controls. This is a *screening order*, not a finding that TZM is inert to Cu–Ni. In fact, its performance with the Ni-bearing melts is a critical unanswered question. A 2025 study documents a 30-mm TZM rod operated at **40 kHz** on an AMAZEMET rePOWDER, but it atomized **Nb–10Hf–1Ti**, not Cu–Ni; the same publication depicts induction-fed ultrasonic atomization of an **unspecified copper alloy** without reporting its contact-material chemistry, wear, or powder contamination. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6)

**How to read the evidence.** The measurements below concern *molten-metal/solid* contact angles, not room-temperature water contact angles. An angle above 90° indicates non-wetting under that particular surface, oxygen, temperature, and time condition; it does **not** establish chemical inertness or sonotrode endurance. Compositions are wt% unless **at%** is explicitly stated. The relevant processes are casting, melt conveyance, brazing or ultrasonic powder atomization—not DED corrosion tests. Thus seawater medium, exposure duration, flow, deposit density, hardness, and corrosion-current fields are **not applicable** to these melt-contact experiments; missing powder metrics are identified explicitly rather than inferred. (rado2000theroleof pages 1-2, rado2000theroleof pages 2-4, rado2000theroleof pages 4-6)

## Evidence by contact material

| Material; full citation and DOI | Process, melt composition and conditions | Quantitative finding and decision relevance | Tags |
|---|---|---|---|
| **Molybdenum and TZM.** J. Ciftcli *et al.*, “Alloy Development From Sustainable Materials—Close-Loop Of Materials Using Ultrasonic Atomization,” *J. Jpn. Soc. Powder Powder Metall.* **72** (2025) S729–S735. DOI: **10.2497/jjspm.15E-SIS13-03**. | **Ultrasonic powder atomization**, not DED: rePOWDER **30-mm TZM**, **40 kHz**, Ar; feed **Nb–10Hf–1Ti**. Separately, an induction-fed stream meets a blade operating at **60 kHz** for Mg alloy; a copper-alloy atomization image is shown, but its composition and contact-material identification are not reported. | Establishes *hardware precedent*, **not** a Cu/TZM or Cu–Ni/TZM angle, Mo dissolution rate, horn service life, or Mo concentration in Cu-alloy powder. No defensible numerical Cu or Cu–Ni dissolution/erosion rate was located. TZM must therefore be tested rather than assumed safe. | [CITE] [NUMBERS] [GAP] (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6) |
| **Tungsten.** M. Nicholas and D. M. Poole, “The influence of oxygen on wetting and bonding in the copper-tungsten system,” *J. Mater. Sci.* **2** (1967) 269–274. DOI: **10.1007/BF00555384**. I. Izaguirre *et al.*, “Wettability and microstructural evolution of copper filler in W and EUROFER brazed joints,” *Int. J. Adv. Manuf. Technol.* **131** (2024) 5905–5921. DOI: **10.1007/s00170-024-13338-9**. | **Cast/sessile-drop and brazing**, pure Cu on W: Nicholas/Poole used 99.9% W, vacuum better than **4 × 10⁻⁵ mmHg**, generally **15 min**; Cu oxygen ranged from oxygen-free to **251 ppm**. Izaguirre used >99.97% W, >99.9% Cu, **10⁻⁶ mbar**, **1105–1110 °C**, **1–10 min**. | Izaguirre: angle approximately **110° initially**, approximately **70° after 2–3 min**. Nicholas/Poole: oxygen-bearing Cu on W measured **110° at 1110 °C** but **62° at 1245 °C** for one surface finish; oxygen-free Cu wetted across the tested temperatures, while deliberately pre-oxidized W gave **140° at 1145 °C**. Thus W is **not reliably non-wetting**, and preserving a non-wetting oxide by controlling oxygen conflicts with low-oxygen powder production. Neither paper determines Cu–Ni/W erosion. | [CITE] [NUMBERS] [GAP] (izaguirre2024wettabilityandmicrostructural pages 2-4, izaguirre2024wettabilityandmicrostructural pages 4-5, nicholas1967theinfluenceof pages 1-2, nicholas1967theinfluenceof pages 2-4) |
| **Niobium.** R. A. Marks *et al.*, “Joining of alumina via copper/niobium/copper interlayers,” *Acta Mater.* **48** (2000) 4425–4438. DOI: **10.1016/S1359-6454(00)00229-9**. | **Brazing/joining** review of earlier **pure-Cu/Nb** sessile-drop measurements, **not** an original sonotrode test: cited Nb foil work used 99.999% Cu, 99.99% Nb, vacuum, **1150 °C**. | Cited Cu/Nb angle **67° initially**, **<40° at 5–10 min**, **<28° at 4 h**. Other cited tests at **1300 °C/5 min** ranged **0–59°**, depending on Nb oxygen and atmosphere. Strong wetting disqualifies Nb as a *non-wetting* tip even though Nb is used as a high-temperature sonotrode in other metals. Do not mistake Marks *et al.* for the original angle measurements; their article supplies the traceable secondary account. | [CITE] [NUMBERS] [GAP] (marks2000joiningofalumina pages 4-5, jaime2024fundamentalsofultrasonic pages 6-8) |
| **Tantalum.** D. A. Mortimer and M. Nicholas, “The wetting of carbon by copper and copper alloys,” *J. Mater. Sci.* **5** (1970) 149–155. DOI: **10.1007/BF00554633**. | **Cast/sessile-drop**, Cu with **1 at% Ta** *on carbon*, **1145 ± 5 °C**, vacuum, **60-min** reading. | **143° on vitreous carbon; 116° on HX30 graphite**, with a discontinuous/flaky carbon-interface reaction product. These are **not** angles of Cu *on tantalum*. A verified direct Cu/Ta or Cu–Ni/Ta angle or erosion rate was not found. | [CITE] [NUMBERS] [GAP] (mortimer1970thewettingof pages 1-2, mortimer1970thewettingof pages 2-5) |
| **Graphite, glassy carbon, carbon fiber.** Mortimer and Nicholas, citation and DOI above. R. H. Bharani, *Single Crystal Growth of Constantan by Vertical Bridgman Method* (2011), accessible thesis/report; **DOI not established** in the retrieved record. | **Cast/sessile-drop:** pure Cu and Cu + **1 at%** additions on HX30 or vitreous carbon, **1145 ± 5 °C**, vacuum, up to **2 h**; exact pure-Cu angle is not legible in the retrieved table. **Cast/Bridgman:** **Cu–45 wt% Ni**, graphite crucible, **1340 °C**, vacuum. | Pure Cu was **non-wetting and comparatively inert** to both bulk carbons. But Ni is not a safe extrapolation: the Cu–45 wt% Ni trial reported visibly destroyed graphite crucible walls, a carbide-rich specimen surface and approximately **43–44 wt% Ni** inferred in product versus **45 wt%** charged. That composition and temperature are **outside** the proposed 10–30 wt% Ni and 1150–1300 °C window; they establish a risk, **not a measured failure rate within that window**. No quantitative bare-carbon-fiber/Cu–10–30Ni lifetime was found. | [CITE] [NUMBERS] [GAP] (mortimer1970thewettingof pages 1-2, bharani2011singlecrystalgrowth pages 9-14) |
| **Graphite with proposed Cr-bearing melts.** Mortimer and Nicholas, DOI above. | **Cast/sessile-drop:** **Cu + 1 at% Cr** on carbon at **1145 ± 5 °C**; also **Cu + 1 at% Ni** and **Cu + 1 at% Mo**, each on carbon—not tests of Cu–Ni melts on metallic Mo. | At **60 min**, Cu–1 at% Cr angles were **50° on vitreous carbon and 45° on graphite**, with a continuous Cr-carbide layer; Cu–1 at% Ni gave **132° on vitreous carbon**, and Cu–1 at% Mo **131° on vitreous carbon/123° on graphite**. **1 at% Ni is not 10–30 wt% Ni**. Cr additions specifically undermine any claim that graphite is universally non-wetting for the proposed Cu–Ni–Cr family. | [CITE] [NUMBERS] [GAP] (mortimer1970thewettingof pages 1-2, mortimer1970thewettingof pages 2-5, mortimer1970thewettingof pages 5-6) |
| **Silicon carbide: dense monocrystal/sintered versus reaction-bonded nozzle.** G. G. Gnesin and Yu. V. Naidich, “Contact reaction of silicon carbide with fused copper,” *Sov. Powder Metall. Met. Ceram.* **8** (1969) 128–132. DOI: **10.1007/BF00774819**. C. Rado, B. Drevet and N. Eustathopoulos, “The role of compound formation in reactive wetting: the Cu/SiC system,” *Acta Mater.* **48** (2000) 4483–4491. DOI: **10.1016/S1359-6454(00)00235-4**. | **Cast/sessile-drop:** 99.99–99.999% Cu, single-crystal or sintered SiC, high vacuum or purified He; **1100–1300 °C**. **Industrial cast/melt-delivery nozzle:** self-bound, Si-containing reaction-bonded SiC, Cu at **1150–1170 °C**, N₂ shielding, **300 h**, approximately **1,000 tonnes** passed. | Initial monocrystal Cu/SiC angle about **140°** (Gnesin); Rado found **125 ± 10°** on the Si face at 1100 °C and about **137°**, persistent, on sintered SiC. **Non-wetting did not prevent dissolution:** Rado observed SiC recession of **several tens of micrometres**, and **3.5–5 at% Si** in solidified Cu after **20 min/1200 °C**; after **150 min/1200 °C**, **12.2–16 at% Si**. The reaction-bonded industrial nozzle retained its measured mass and dimensions and showed no visible cracks/corrosion after **300 h**, **but** its initially Si-rich binder became Cu-rich and softened: **1560 to 605 kg mm⁻²** microhardness. This is strong nozzle-endurance evidence **but not proof of contamination-free pre-alloy powder or sonotrode endurance**. | [CITE] [NUMBERS] [GAP] (gnesin1969contactreactionof pages 1-3, gnesin1969contactreactionof pages 3-4, rado2000theroleof pages 1-2, rado2000theroleof pages 2-4, rado2000theroleof pages 4-6) |
| **Si₃N₄ and boron nitride.** G. A. Yasinskaya, “The wetting of refractory carbides, borides, and nitrides by molten metals,” *Sov. Powder Metall. Met. Ceram.* **5** (1966) 557–559. DOI: **10.1007/BF00780116**. M. G. Nicholas *et al.*, “Some observations on the wetting and bonding of nitride ceramics,” *J. Mater. Sci.* **25** (1990) 2679–2689. DOI: **10.1007/BF00584866**. | **Cast/sessile-drop:** Yasinskaya tested Cu on hot-pressed nitride disks in Ar or **10⁻²–10⁻⁴ mmHg** vacuum; images **10–15 min after melting**, at melting temperature or some superheat; **exact temperature of each Cu/nitride value is not specified**. Nicholas tested **pure Cu** as well as **Cu–5, –7.5 and –10 wt% Ti**, approximately **1150 °C/15 min**, high vacuum. | Yasinskaya reports **125° for Cu/BN and 134° for Cu/Si₃N₄**. Nicholas reports that **pure Cu did not wet** BN or Si₃N₄; Cu–Ti wetting required reactive additions and produced roughly **10–30 µm** reaction layers. Those **Cu–Ti data are not Cu–Ni or aluminum bronze**. BN remains a plausible *nozzle or coating-screening* candidate, but no Cu–Ni/BN sonotrode erosion, coating adhesion or B/N powder-pickup result was located. | [CITE] [NUMBERS] [GAP] (yasinskaya1966thewettingof pages 1-2, nicholas1990someobservationson pages 1-2, nicholas1990someobservationson pages 5-6) |
| **Sialon.** Nicholas *et al.*, citation and DOI above; R. F. Jaime *et al.*, “Fundamentals of Ultrasonic Treatment of Aluminum Alloys,” *Int. J. Metalcasting* **18** (2024) 2783–2807. DOI: **10.1007/s40962-023-01253-w**. | **Cast/sessile-drop:** Nicholas tested pure Cu on two sialons at about **1150 °C/15 min** under vacuum. **Ultrasonic melt treatment:** Jaime reviews β-SiAlON probes for **aluminum**, not copper; reports a **20-kHz, 1500-W**, **22-mm** SiAlON hollow degassing probe. | Pure Cu **did not wet** either sialon in Nicholas’s comparison, but no dependable numerical pure-Cu/sialon angle could be extracted. The ultrasonic review gives β-SiAlON fracture toughness **7.7 MPa√m** versus **4.5 MPa√m** for alumina; these are *material properties*, not Cu-alloy erosion measurements. Cu–Ni and NAB stability, attachment, thermal shock and acoustic output remain to be established. | [CITE] [NUMBERS] [GAP] (nicholas1990someobservationson pages 1-2, nicholas1990someobservationson pages 5-6, jaime2024fundamentalsofultrasonic pages 6-8) |
| **Alumina.** L. I. Kuz’min, “The wetting of refractory products by copper and cuprous oxides,” *Refractories* **14** (1973) 763–768. DOI: **10.1007/BF01285084**. | **Cast/sessile-drop:** high-purity vacuum-remelted Cu on approximately **1%-porosity Al₂O₃** in purified He, **5-min** hold. | Cu/Al₂O₃ angle **130° at 1300 °C** (**153° at 1100 °C**). Adding Cu oxide to the refractory promotes wetting: **30 wt% cuprous oxide** in the substrate yielded **86° at 1300 °C**. Dense alumina therefore deserves an initial *delivery-nozzle* test, while atmosphere/oxide contamination must be controlled. These are **not** corrosion or sonotrode fatigue figures. | [CITE] [NUMBERS] [GAP] (kuzmin1973thewettingof pages 1-3, kuzmin1973thewettingof pages 3-4, kuzmin1973thewettingof pages 4-6) |
| **Zirconia.** K. Nogi, H. Takeda and K. Ogino, “Effect of Applied DC Voltage on the Wettability of ZrO₂ by Liquid Cu,” *J. Japan Inst. Metals* **53** (1989) 927–935. DOI: **10.2320/jinstmet1952.53.9_927**. | **Cast/sessile-drop:** Cu wire on **11 mol% CaO-stabilized ZrO₂**, Ar with graphite heater, **1423 K = 1150 °C**, **3.6 ks = 1 h**, without applied voltage for the baseline. | Five baseline angles **118.3°, 121.4°, 126.3°, 127.1°, 138.6°**, associated with **26–171 ppm** oxygen in reference Cu droplets; no obvious Cu penetration or reaction by baseline microscopy/EPMA. *Applying* DC voltage decreased angles and, in one polarity, produced **0.2 at% Zr** near the Cu-drop surface: proof that altered oxygen electrochemistry can invalidate an apparent inertness claim. No ultrasound or Cu–Ni comparison. | [CITE] [NUMBERS] [GAP] (nogi1989effectofapplied pages 1-3, nogi1989effectofapplied pages 3-6) |

**Mo–Ni warning.** The documented TZM horn use cannot be transferred to Cu–10–30Ni by reasoning from the near-inert behavior of *pure Cu*. Ni and Mo form solid solutions and ordered **Ni₄Mo/Ni₃Mo** phases in their binary system, so Mo uptake or interfacial reaction merits direct testing. Those phases should **not** be asserted to form at a 1150–1300 °C Cu–Ni/TZM liquid interface without a measured composition and phase analysis. Neither a Cu–10Ni nor Cu–30Ni sessile-drop angle on Mo/TZM, nor a comparative Mo-versus-W dissolution rate in those melts, was established in the accessible evidence. Similarly, there are **no established quantitative sonotrode erosion rates for these metals in NAB** here. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6)

**Coatings actually evidenced.** The ultrasonic-melt-treatment review mentions **Ni- or Cr-coated aluminum probes**, but says the probes **and coatings erode with time**; those observations concern **molten aluminum**, **not molten copper**. Its SiAlON example is an *uncoated ceramic probe*, likewise not a Cu-alloy coating trial. No verified BN-, oxide-, carbide- or nitride-coated ultrasonic **copper** horn with a measured service life or powder-pickup result was located. Moreover, do not substitute the Cu–Ti *active-braze* nitride reactions above for a protective coating test. (jaime2024fundamentalsofultrasonic pages 6-8, nicholas1990someobservationson pages 1-2, nicholas1990someobservationson pages 5-6)

## Proposed first 20–60-kHz comparison

**Sonotrode:** start with **bare, replaceable TZM** as the *instrument-compatible baseline*, alongside **bare W** if resonant design and jointing permit; include a **β-SiAlON** tip only as a carefully engineered ceramic-arm comparator. TZM has a documented **40-kHz** atomization implementation, whereas pure Cu demonstrably wets W and Nb. Neither TZM nor W is yet shown clean in Cu–Ni/NAB; ceramic fracture, acoustic coupling and thermal shock remain separate acceptance tests. **No candidate should be called contamination-free on the basis of a static wetting angle.** (ciftcli2025alloydevelopmentfrom pages 1-3, izaguirre2024wettabilityandmicrostructural pages 2-4, izaguirre2024wettabilityandmicrostructural pages 4-5, marks2000joiningofalumina pages 4-5, jaime2024fundamentalsofultrasonic pages 6-8)

**Nozzle:** start with **dense alumina**, add **dense stabilized zirconia** and **reaction-bonded SiC** controls, and evaluate **BN** after establishing grade, density and coating/bulk form. The 300-h SiC feeder result is unusually useful engineering evidence, but its Cu-rich, softened binder and the measured SiC dissolution make it an unsafe default for a chemistry-sensitive powder campaign. Test **graphite separately in every Ni/Cr-bearing composition**, rather than extrapolating from pure Cu. (kuzmin1973thewettingof pages 1-3, kuzmin1973thewettingof pages 3-4, nogi1989effectofapplied pages 1-3, gnesin1969contactreactionof pages 3-4, rado2000theroleof pages 2-4, rado2000theroleof pages 4-6, mortimer1970thewettingof pages 2-5, yasinskaya1966thewettingof pages 1-2)

**Go/no-go protocol:** make composition-matched melts at the *actual liquid processing temperature* for Cu, Cu–10Ni and Cu–30Ni and representative NAB, including proposed Fe/Mn/Cr variants. Record angle versus time under the actual oxygen potential; follow static exposures with powered **20-, 40- and/or 60-kHz** exposures matched for amplitude, duty cycle and cumulative liquid contact. Weigh and section tips/nozzles; quantify recession and adherent/reaction-layer thickness; measure **Mo, W, Nb, Ta, C, Si, Al, Zr and B** in starting melt, filtered powder fractions and deposits with suitable trace-element methods. Measure each lot’s powder size distribution, Hall flow, apparent density and oxygen. Set acceptance limits *before* screening; the literature above supplies **no validated ppm-pickup or mg h⁻¹ erosion threshold** for this instrument and alloy set. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6, rado2000theroleof pages 4-6, nogi1989effectofapplied pages 1-3, nogi1989effectofapplied pages 3-6)

## Scope and proposal-relevance limits

A retrieved copper-scrap/ultrasonic-powder/laser-DED publication is **M. Cabrioli *et al.*, “Upcycling of Copper Scrap into High-Quality Powder for Additive Manufacturing: Processing, Characterization, and Sustainability Assessment,” *J. Manuf. Mater. Process.* 9 (2025) 320, DOI: 10.3390/jmmp9090320**. Its search metadata describe approximately **99.5 wt% Cu** powder and laser DED, but the associated retrieved *full text was mismatched to an unrelated report*. Accordingly, no numerical horn material, wear, powder size/flow/oxygen, DED density, hardness or corrosion value from that item is treated as verified. This is a **process precedent**, not evidence for Cu–Ni or NAB melt-contact compatibility or a novelty claim about the proposal’s complete pipeline. [NOVELTY-RISK] [GAP]

Likewise, the literature assessed here does **not** provide an apples-to-apples dataset of **as-deposited, single-pre-alloyed-powder laser DED** on cast NAB and wrought Cu–Ni with **30-day natural/ASTM D1141 seawater** corrosion benchmarked against **wrought C71500**. Consequently, deposit porosity/density, *i*₍corr₎, *E*₍corr₎, impedance, selective-attack depth, hardness, strength/elongation, powder Hall flow and lot oxygen **cannot responsibly be supplied for the melt-contact papers**. Those are distinct proposal outcomes, not missing entries to be filled with unrelated alloys or 3.5 wt% NaCl results. [NAVY] is relevant to the *proposed repair application*, but Navy/DoD funding of the cited wetting studies has **not** been verified. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6, gnesin1969contactreactionof pages 1-3, gnesin1969contactreactionof pages 3-4)

## Top 5 things the PI should know

1. **TZM at 40 kHz is a real rePOWDER precedent, not a Cu–Ni qualification**; make horn-to-powder Mo transfer an explicit measured risk. [CITE] [GAP] (ciftcli2025alloydevelopmentfrom pages 1-3)
2. **A high angle does not mean zero contamination:** Cu/SiC can remain near **137°** while transferring **3.5–5 at% Si in 20 min at 1200 °C**. [CITE] [NUMBERS] (rado2000theroleof pages 2-4, rado2000theroleof pages 4-6)
3. **Treat oxygen as a controlled variable:** W switches wetting behavior with oxygen/temperature; oxide-loaded alumina becomes more wettable, and zirconia responds strongly to changed oxygen conditions. [CITE] [NUMBERS] (nicholas1967theinfluenceof pages 1-2, nicholas1967theinfluenceof pages 2-4, kuzmin1973thewettingof pages 1-3, kuzmin1973thewettingof pages 4-6, nogi1989effectofapplied pages 1-3, nogi1989effectofapplied pages 3-6)
4. **Do not transfer pure-Cu/graphite results to Cu–Ni–Cr or NAB:** **1 at% Cr** makes Cu wet graphite, and an out-of-window **Cu–45 wt% Ni** trial damaged a graphite crucible. [CITE] [NUMBERS] [GAP] (mortimer1970thewettingof pages 1-2, mortimer1970thewettingof pages 2-5, bharani2011singlecrystalgrowth pages 9-14)
5. **Separate nozzle and horn decisions.** Alumina and reaction-bonded SiC have directly informative *passive-delivery* evidence; no cited ceramic has demonstrated long-life, contamination-free **20–60-kHz Cu–Ni sonotrode** service. This missing coupled chemical–acoustic–powder dataset is the defensible materials-process gap. [CITE] [NUMBERS] [GAP] (kuzmin1973thewettingof pages 1-3, gnesin1969contactreactionof pages 3-4, jaime2024fundamentalsofultrasonic pages 6-8, ciftcli2025alloydevelopmentfrom pages 1-3)

References

1. (ciftcli2025alloydevelopmentfrom pages 1-3): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72(Supplement):S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

2. (ciftcli2025alloydevelopmentfrom pages 3-6): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72(Supplement):S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

3. (rado2000theroleof pages 1-2): C. Rado, B. Drevet, and N. Eustathopoulos. The role of compound formation in reactive wetting: the cu/sic system. Acta Materialia, 48:4483-4491, Dec 2000. URL: https://doi.org/10.1016/s1359-6454(00)00235-4, doi:10.1016/s1359-6454(00)00235-4. This article has 142 citations and is from a highest quality peer-reviewed journal.

4. (rado2000theroleof pages 2-4): C. Rado, B. Drevet, and N. Eustathopoulos. The role of compound formation in reactive wetting: the cu/sic system. Acta Materialia, 48:4483-4491, Dec 2000. URL: https://doi.org/10.1016/s1359-6454(00)00235-4, doi:10.1016/s1359-6454(00)00235-4. This article has 142 citations and is from a highest quality peer-reviewed journal.

5. (rado2000theroleof pages 4-6): C. Rado, B. Drevet, and N. Eustathopoulos. The role of compound formation in reactive wetting: the cu/sic system. Acta Materialia, 48:4483-4491, Dec 2000. URL: https://doi.org/10.1016/s1359-6454(00)00235-4, doi:10.1016/s1359-6454(00)00235-4. This article has 142 citations and is from a highest quality peer-reviewed journal.

6. (izaguirre2024wettabilityandmicrostructural pages 2-4): Ignacio Izaguirre, Javier de Prado, María Sánchez, and Alejandro Ureña. Wettability and microstructural evolution of copper filler in w and eurofer brazed joints. The International Journal of Advanced Manufacturing Technology, 131:5905-5921, Mar 2024. URL: https://doi.org/10.1007/s00170-024-13338-9, doi:10.1007/s00170-024-13338-9. This article has 17 citations.

7. (izaguirre2024wettabilityandmicrostructural pages 4-5): Ignacio Izaguirre, Javier de Prado, María Sánchez, and Alejandro Ureña. Wettability and microstructural evolution of copper filler in w and eurofer brazed joints. The International Journal of Advanced Manufacturing Technology, 131:5905-5921, Mar 2024. URL: https://doi.org/10.1007/s00170-024-13338-9, doi:10.1007/s00170-024-13338-9. This article has 17 citations.

8. (nicholas1967theinfluenceof pages 1-2): M. Nicholas and D. M. Poole. The influence of oxygen on wetting and bonding in the copper-tungsten system. Journal of Materials Science, 2:269-274, May 1967. URL: https://doi.org/10.1007/bf00555384, doi:10.1007/bf00555384. This article has 42 citations and is from a peer-reviewed journal.

9. (nicholas1967theinfluenceof pages 2-4): M. Nicholas and D. M. Poole. The influence of oxygen on wetting and bonding in the copper-tungsten system. Journal of Materials Science, 2:269-274, May 1967. URL: https://doi.org/10.1007/bf00555384, doi:10.1007/bf00555384. This article has 42 citations and is from a peer-reviewed journal.

10. (marks2000joiningofalumina pages 4-5): R. A. Marks, D. Chapman, D. T. Danielson, and A. M. Glaeser. Joining of alumina via copper/niobium/copper interlayers. Acta Materialia, 48:4425-4438, Dec 2000. URL: https://doi.org/10.1016/s1359-6454(00)00229-9, doi:10.1016/s1359-6454(00)00229-9. This article has 82 citations and is from a highest quality peer-reviewed journal.

11. (jaime2024fundamentalsofultrasonic pages 6-8): Raquel F. Jaime, Hélder Puga, Miodrag Prokic, Carl Söderhjelm, and Diran Apelian. Fundamentals of ultrasonic treatment of aluminum alloys. International Journal of Metalcasting, 18:2783-2807, Jan 2024. URL: https://doi.org/10.1007/s40962-023-01253-w, doi:10.1007/s40962-023-01253-w. This article has 36 citations and is from a peer-reviewed journal.

12. (mortimer1970thewettingof pages 1-2): D. A. Mortimer and M. Nicholas. The wetting of carbon by copper and copper alloys. Journal of Materials Science, 5:149-155, Feb 1970. URL: https://doi.org/10.1007/bf00554633, doi:10.1007/bf00554633. This article has 244 citations and is from a peer-reviewed journal.

13. (mortimer1970thewettingof pages 2-5): D. A. Mortimer and M. Nicholas. The wetting of carbon by copper and copper alloys. Journal of Materials Science, 5:149-155, Feb 1970. URL: https://doi.org/10.1007/bf00554633, doi:10.1007/bf00554633. This article has 244 citations and is from a peer-reviewed journal.

14. (bharani2011singlecrystalgrowth pages 9-14): RH Bharani. Single crystal growth of constantan by vertical bridgman method. Unknown journal, 2011.

15. (mortimer1970thewettingof pages 5-6): D. A. Mortimer and M. Nicholas. The wetting of carbon by copper and copper alloys. Journal of Materials Science, 5:149-155, Feb 1970. URL: https://doi.org/10.1007/bf00554633, doi:10.1007/bf00554633. This article has 244 citations and is from a peer-reviewed journal.

16. (gnesin1969contactreactionof pages 1-3): G. G. Gnesin and Yu. V. Naidich. Contact reaction of silicon carbide with fused copper. Soviet Powder Metallurgy and Metal Ceramics, 8:128-132, Feb 1969. URL: https://doi.org/10.1007/bf00774819, doi:10.1007/bf00774819. This article has 40 citations.

17. (gnesin1969contactreactionof pages 3-4): G. G. Gnesin and Yu. V. Naidich. Contact reaction of silicon carbide with fused copper. Soviet Powder Metallurgy and Metal Ceramics, 8:128-132, Feb 1969. URL: https://doi.org/10.1007/bf00774819, doi:10.1007/bf00774819. This article has 40 citations.

18. (yasinskaya1966thewettingof pages 1-2): G. A. Yasinskaya. The wetting of refractory carbides, borides, and nitrides by molten metals. Soviet Powder Metallurgy and Metal Ceramics, 5:557-559, Jul 1966. URL: https://doi.org/10.1007/bf00780116, doi:10.1007/bf00780116. This article has 92 citations.

19. (nicholas1990someobservationson pages 1-2): M. G. Nicholas, D. A. Mortimer, L. M. Jones, and R. M. Crispin. Some observations on the wetting and bonding of nitride ceramics. Journal of Materials Science, 25:2679-2689, Jun 1990. URL: https://doi.org/10.1007/bf00584866, doi:10.1007/bf00584866. This article has 218 citations and is from a peer-reviewed journal.

20. (nicholas1990someobservationson pages 5-6): M. G. Nicholas, D. A. Mortimer, L. M. Jones, and R. M. Crispin. Some observations on the wetting and bonding of nitride ceramics. Journal of Materials Science, 25:2679-2689, Jun 1990. URL: https://doi.org/10.1007/bf00584866, doi:10.1007/bf00584866. This article has 218 citations and is from a peer-reviewed journal.

21. (kuzmin1973thewettingof pages 1-3): L. I. Kuz'min. The wetting of refractory products by copper and cuprous oxides. Refractories, 14:763-768, Nov 1973. URL: https://doi.org/10.1007/bf01285084, doi:10.1007/bf01285084. This article has 3 citations.

22. (kuzmin1973thewettingof pages 3-4): L. I. Kuz'min. The wetting of refractory products by copper and cuprous oxides. Refractories, 14:763-768, Nov 1973. URL: https://doi.org/10.1007/bf01285084, doi:10.1007/bf01285084. This article has 3 citations.

23. (kuzmin1973thewettingof pages 4-6): L. I. Kuz'min. The wetting of refractory products by copper and cuprous oxides. Refractories, 14:763-768, Nov 1973. URL: https://doi.org/10.1007/bf01285084, doi:10.1007/bf01285084. This article has 3 citations.

24. (nogi1989effectofapplied pages 1-3): K. Nogi, Hiroyuki Takeda, and K. Ogino. Effect of applied dc voltage on the wettability of zro 2 by liquid cu. Journal of The Japan Institute of Metals, 53:927-935, 1989. URL: https://doi.org/10.2320/jinstmet1952.53.9\_927, doi:10.2320/jinstmet1952.53.9\_927. This article has 6 citations and is from a peer-reviewed journal.

25. (nogi1989effectofapplied pages 3-6): K. Nogi, Hiroyuki Takeda, and K. Ogino. Effect of applied dc voltage on the wettability of zro 2 by liquid cu. Journal of The Japan Institute of Metals, 53:927-935, 1989. URL: https://doi.org/10.2320/jinstmet1952.53.9\_927, doi:10.2320/jinstmet1952.53.9\_927. This article has 6 citations and is from a peer-reviewed journal.
