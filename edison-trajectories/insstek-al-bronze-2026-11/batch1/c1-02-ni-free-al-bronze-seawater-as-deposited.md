<!--
Edison Scientific LITERATURE_HIGH task (batch 1)
- Task ID: 550d1439-cfe8-45d1-bf82-26b43c3247e7
- Submitted: 2026-11-10T15:58:07Z
- Fetched: 2026-11-10T16:28:15Z (status: success)
- Raw trajectory JSON: ../raw/c1-02-ni-free-al-bronze-seawater-as-deposited.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications)
submitted an ONR FY2027 Young Investigator Program proposal in October 2026 to
design new pre-alloyed copper alloy powders for single-stream blown-powder
laser directed energy deposition (DED). Goals: deposits that are dense and
crack-free, built on themselves and deposited on cast nickel-aluminum bronze
(NAB, UNS C95800) and wrought Cu-Ni (repair), that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). The searched space is Cu at least 65 wt% with Ni 0-30,
Al 0-9.5 (upper bound set by retained beta-prime martensite as deposited),
Fe 0-4.5, Mn 0-4, Ti 0-0.5, plus Cr, Si, Nb in Cu-Ni only, with NAB family
rules (above 7 Al: Fe <= Ni <= 5.5). Powder is made in-house by ultrasonic
atomization (AMAZEMET rePOWDER, 40 kHz, induction melting up to 1300 C); the
first copper alloy run uses UNS C63000 bar (Cu-10Al-5Ni-3Fe). Blown-powder DED
is bought at the University of Utah (InssTek MX-Lab: InssTek DMT process,
ytterbium fiber laser of 500 W maximum, 0.4 mm beam, six powder feeders,
45-150 um powder) and at the Colorado School of Mines (FormAlloy X2).
InssTek's material database (summarized for the PI by InssTek) lists
"Al-Bronze / UNS C95300" as a qualified DED material: Cu balance, Al 9-11 wt%,
Fe 0.8-1.5 wt% (no nickel); typical powder size average about 83.8 um;
melting range 1040-1045 C; applications listed as ship propellers and marine
components; tensile strength of InssTek DMT-produced material 628 MPa (XY) and
598 MPa (Z). The database summary gives no yield strength, elongation,
hardness, heat treatment, laser power, machine model or corrosion data.

QUESTION: How does nickel-free aluminum bronze (Cu-9-11Al-0.8-4Fe, e.g. UNS
C95300, C95400, C61400, CuAl10Fe, ERCuAl-A2 deposits) corrode in seawater or
3.5 wt% NaCl when it is laser deposited, laser clad, welded, wire-arc
deposited or otherwise rapidly solidified, compared with the same alloy cast
and heat treated, and compared with NAB (C95800, C63200) and with Cu-Ni
(C70600, C71500)?
(1) Selective phase corrosion (dealuminification) of retained beta /
beta-prime martensite and of the alpha + gamma-2 eutectoid: which phases are
attacked, how fast, how deep, in which media and durations.
(2) The basis and data behind the classic composition rules for seawater
service: nickel content at least equal to iron content in NAB; Al no more
than about 8.2 + 0.5 Ni wt% (Meigh; CDA Publications 80 and 222; Campbell);
the binary limit near 9.4 wt% Al; and why Ni-free aluminum bronzes need a
temper anneal (for example 600-700 C) for seawater service.
(3) Quantitative comparisons (corrosion current density, polarization
resistance, mass loss, selective-attack depth) between Ni-free aluminum
bronze and NAB, in any condition, with test medium and duration.
(4) What all of this predicts for an as-deposited DED C95300 deposit made
with InssTek DMT (strength 598-628 MPa, which suggests martensitic
beta-prime) used without heat treatment in seawater, and what heat treatment
would restore its corrosion resistance and at what cost in strength.
(5) Is there any published corrosion test of a laser-deposited or DED Cu-Al-Fe
(no Ni) aluminum bronze in seawater or NaCl? If not, say so.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition /
InssTek DMT, wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought,
weld overlay), the alloy composition in wt%, the condition (as deposited,
heat treated: temperature and time), the test conditions (e.g. 3.5 wt% NaCl
vs natural or substitute seawater per ASTM D1141, duration, flow), and the key
numbers (porosity/density, phase fractions, corrosion current density or rate,
Ecorr, selective-attack depth, hardness, UTS/yield/elongation with direction,
laser power/spot/speed/feed, powder size/flow/oxygen). Tag each item: [CITE]
worth citing; [NUMBERS] gives a quantitative benchmark; [NAVY] Navy/DoD-funded
or Navy application; [INSSTEK] made on an InssTek machine or by InssTek;
[GAP] shows something not yet done. If the literature does not answer part of
the question, say so plainly instead of padding with loosely related work.
End with a ranked "Top 5 things the PI should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications)
submitted an ONR FY2027 Young Investigator Program proposal in October 2026 to
design new pre-alloyed copper alloy powders for single-stream blown-powder
laser directed energy deposition (DED). Goals: deposits that are dense and
crack-free, built on themselves and deposited on cast nickel-aluminum bronze
(NAB, UNS C95800) and wrought Cu-Ni (repair), that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). The searched space is Cu at least 65 wt% with Ni 0-30,
Al 0-9.5 (upper bound set by retained beta-prime martensite as deposited),
Fe 0-4.5, Mn 0-4, Ti 0-0.5, plus Cr, Si, Nb in Cu-Ni only, with NAB family
rules (above 7 Al: Fe <= Ni <= 5.5). Powder is made in-house by ultrasonic
atomization (AMAZEMET rePOWDER, 40 kHz, induction melting up to 1300 C); the
first copper alloy run uses UNS C63000 bar (Cu-10Al-5Ni-3Fe). Blown-powder DED
is bought at the University of Utah (InssTek MX-Lab: InssTek DMT process,
ytterbium fiber laser of 500 W maximum, 0.4 mm beam, six powder feeders,
45-150 um powder) and at the Colorado School of Mines (FormAlloy X2).
InssTek's material database (summarized for the PI by InssTek) lists
"Al-Bronze / UNS C95300" as a qualified DED material: Cu balance, Al 9-11 wt%,
Fe 0.8-1.5 wt% (no nickel); typical powder size average about 83.8 um;
melting range 1040-1045 C; applications listed as ship propellers and marine
components; tensile strength of InssTek DMT-produced material 628 MPa (XY) and
598 MPa (Z). The database summary gives no yield strength, elongation,
hardness, heat treatment, laser power, machine model or corrosion data.

QUESTION: How does nickel-free aluminum bronze (Cu-9-11Al-0.8-4Fe, e.g. UNS
C95300, C95400, C61400, CuAl10Fe, ERCuAl-A2 deposits) corrode in seawater or
3.5 wt% NaCl when it is laser deposited, laser clad, welded, wire-arc
deposited or otherwise rapidly solidified, compared with the same alloy cast
and heat treated, and compared with NAB (C95800, C63200) and with Cu-Ni
(C70600, C71500)?
(1) Selective phase corrosion (dealuminification) of retained beta /
beta-prime martensite and of the alpha + gamma-2 eutectoid: which phases are
attacked, how fast, how deep, in which media and durations.
(2) The basis and data behind the classic composition rules for seawater
service: nickel content at least equal to iron content in NAB; Al no more
than about 8.2 + 0.5 Ni wt% (Meigh; CDA Publications 80 and 222; Campbell);
the binary limit near 9.4 wt% Al; and why Ni-free aluminum bronzes need a
temper anneal (for example 600-700 C) for seawater service.
(3) Quantitative comparisons (corrosion current density, polarization
resistance, mass loss, selective-attack depth) between Ni-free aluminum
bronze and NAB, in any condition, with test medium and duration.
(4) What all of this predicts for an as-deposited DED C95300 deposit made
with InssTek DMT (strength 598-628 MPa, which suggests martensitic
beta-prime) used without heat treatment in seawater, and what heat treatment
would restore its corrosion resistance and at what cost in strength.
(5) Is there any published corrosion test of a laser-deposited or DED Cu-Al-Fe
(no Ni) aluminum bronze in seawater or NaCl? If not, say so.

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition /
InssTek DMT, wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought,
weld overlay), the alloy composition in wt%, the condition (as deposited,
heat treated: temperature and time), the test conditions (e.g. 3.5 wt% NaCl
vs natural or substitute seawater per ASTM D1141, duration, flow), and the key
numbers (porosity/density, phase fractions, corrosion current density or rate,
Ecorr, selective-attack depth, hardness, UTS/yield/elongation with direction,
laser power/spot/speed/feed, powder size/flow/oxygen). Tag each item: [CITE]
worth citing; [NUMBERS] gives a quantitative benchmark; [NAVY] Navy/DoD-funded
or Navy application; [INSSTEK] made on an InssTek machine or by InssTek;
[GAP] shows something not yet done. If the literature does not answer part of
the question, say so plainly instead of padding with loosely related work.
End with a ranked "Top 5 things the PI should know" list.


## Corrosion of Nickel-Free Aluminum Bronze in Seawater: Literature Review for Laser DED Applications

### Summary Table of Quantitative Benchmarks

The following table summarizes the key quantitative corrosion and mechanical-property data gathered across processes and alloy families relevant to this inquiry:

| Reference | Process | Alloy / composition (wt%) | Condition | Test medium / duration | Key corrosion data | Key mechanical data | Tags |
|---|---|---|---|---|---|---|---|
| Zhao et al. (2022), DOI: 10.3390/met12050781 (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 2-4) | Powder-fed laser deposition of NAB coating on SUS630; direct (N-1), KF-6 Ni interlayer (N-2), or KF-306 Ni-Cr interlayer (N-3) | NAB; exact powder composition not reported in extracted evidence | As deposited | Aerated 3.5 wt% NaCl, 25 ± 5 °C; 20 min before polarization; −300 to +300 mV vs OCP; EIS 10⁵–10⁻² Hz | N-1/N-2/N-3: *i*<sub>corr</sub> = 7.82 ± 0.5/4.65 ± 0.5/4.09 ± 0.4 µA·cm⁻²; *E*<sub>corr</sub> = −248/−255/−252 mV; *R*<sub>p</sub> = 2810/5275/4865 Ω·cm²; Ni-Cr interlayer gave shallowest attack and densest product film | Not reported | [CITE] [NUMBERS] |
| Shahriari et al. (2023), DOI: 10.1038/s41529-023-00405-x (shahriari2023corrosionperformanceof pages 2-2, shahriari2023corrosionperformanceof pages 10-12, shahriari2023corrosionperformanceof pages 12-14) | GMAW wire-arc additive manufacturing (WAAM) versus cast NAB | NAB/C95800 family; exact composition not available in extracted evidence | A1 as built; HT1 350 °C/2 h; HT2 550 °C/4 h; HT3 675 °C/6 h; as-cast C1 | 3.5 wt% NaCl, approximately pH 7; polarization and EIS | A1 had lowest *i*<sub>corr</sub>, wider pseudopassive range, and lower passive current; A1 *E*<sub>corr</sub> ≈ −0.293 V vs Ag/AgCl versus ≈ −0.222 V average for cast/HT. HT1: *i*<sub>corr</sub> ≈ 4.4×10⁻⁶ A·cm⁻², *R*<sub>t</sub> ≈ 10.2 kΩ·cm²; HT2: 6.6×10⁻⁶, 2.58 kΩ·cm²; HT3: 8×10⁻⁶, 3.8 kΩ·cm². As-built WAAM outperformed cast and HT conditions | Not reported in corrosion paper | [CITE] [NUMBERS] |
| Doyle (2022) (doyle2022additivemanufacturingof pages 53-58, doyle2022additivemanufacturingof pages 47-53) | Wire-fed laser DED; six 200 W diode lasers, 1200 W maximum, 976 nm, 0.9 mm spot; 0.89 mm wire; Ar shielding | C95800: Cu 82.0, Al 8.64, Ni 4.21, Fe 3.19, Mn 1.32, Si 0.05 | As printed; 675 °C/6 h, furnace cooled | No corrosion test; corrosion testing identified as future work | No corrosion numbers | As printed: YS 410.5 ± 6.3 MPa, UTS 757.8 ± 5.4 MPa, elongation 29.0 ± 1.0%, 218.8 ± 4.4 HV; HT: YS 372.2 ± 6.7 MPa, UTS 714.5 ± 8.3 MPa, elongation 31.2 ± 0.25%, 204.1 ± 3.1 HV; candidate-build relative density 99.58–99.89% | [CITE] [NUMBERS] [GAP] |
| Lewis & LaQue (1981), DOI: 10.2172/6255887 (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48) | Wrought Cu-Ni seawater-service products | C70600, nominal Cu-10Ni; C71500, nominal Cu-30Ni | Commercial wrought conditions | Natural seawater; quiet and flowing at 2 ft·s⁻¹; separate one-year equal-area tests at 0.6 m·s⁻¹ | C70600: 0.2–0.6 mpy quiet and 0.5–1.1 mpy flowing ≈ 0.005–0.015 and 0.013–0.028 mm·yr⁻¹; C71500: 0.3–0.5 and 0.5–0.7 mpy ≈ 0.008–0.013 and 0.013–0.018 mm·yr⁻¹. One-year 0.6 m·s⁻¹ rates: C70600 30.5 µm·yr⁻¹; C71500 20.3 µm·yr⁻¹ | Not reported | [CITE] [NUMBERS] |
| Gao & Liu (2022), DOI: 10.3390/ma15238513 (gao2022corrosionbehaviorof pages 4-5, gao2022corrosionbehaviorof pages 2-4) | Conventional high-strength C71500 | C71500; exact composition not reproduced in extracted evidence | As received | Simulated sulfide-polluted seawater: 3.5 wt% NaCl + 0.5 wt% Na₂S, 35 ± 2 °C; up to 672 h | Initial *i*<sub>corr</sub> ≈ 96.6 µA·cm⁻² and *E*<sub>corr</sub> = −541 ± 16 mV vs SCE at 0.5 h; corrosion rate ≈ 0.15 mm·yr⁻¹ initially and ≈ 0.09 mm·yr⁻¹ after 168 h; uniform attack. Values are not representative of clean seawater | Not reported | [CITE] [NUMBERS] |
| Takaloo et al. (2011), DOI: 10.4236/msa.2011.211207 (takaloo2011corrosionbehaviorof pages 12-13, takaloo2011corrosionbehaviorof pages 5-7) | Cast NAB, heat treated | NAB; exact composition not reproduced in extracted evidence | Air normalized at 675 °C/45 min; other quenched/normalized conditions also tested | Artificial seawater; electrochemical testing after 75 days | Best tested condition: potential ≈ −123.46 mV and current ≈ 3.1348 µA versus reference current 6.148 µA; highest reported polarization resistance; fewer pits than quenched material | Strength and hardness not reported | [CITE] [NUMBERS] |
| InssTek material-database summary (2026; supplied context) | InssTek DMT / blown-powder laser DED; machine and process parameters not disclosed | “Al-Bronze / UNS C95300”: Cu balance, Al 9–11, Fe 0.8–1.5, no Ni; powder mean ≈ 83.8 µm; melting range 1040–1045 °C | DMT-produced; heat treatment not disclosed | No seawater, NaCl, electrochemical, mass-loss, or selective-attack test reported | No corrosion data | UTS 628 MPa XY and 598 MPa Z; YS, elongation, hardness, density/porosity, phase fraction, laser power, speed, powder flow, and oxygen not reported | [NUMBERS] [INSSTEK] [GAP] |
| Kuprienko (2025) (kuprienko2025analysisofnickel pages 67-72) | GMA-pulsed DED-Arc with liquid-nitrogen interpass cooling; wire feed 250–300 ipm; travel 10–16 ipm | MIL-CuNiAl wire: Cu 81.35, Al 9.09, Fe 3.94, Ni 4.53, Mn 1.00; wrought C63200 substrate | As deposited; interpass 232–260 °C for layers 1–3 and 149–177 °C thereafter | No corrosion test reported in cited passage | No corrosion numbers; martensite linked in the review to preferential corrosion and cavitation erosion | Tensile, bend, CVN, and HV0.3 testing described, but numerical results absent from cited passage | [CITE] [NAVY] [GAP] |
| Dobson (2024) (dobson2024corrosionmechanismsand pages 39-42, dobson2024corrosionmechanismsand pages 42-45) | Plasma-welded/weld-repaired NAB; review and testing thesis | Defence Standard 02-747 NAB: Cu balance, Al 8.8–9.5, Fe 4–5, Ni 4.5–5.5, Mn 0.75–1.3 | Required PWHT: 675 °C ± 15 °C for ≥6 h, still-air cooling | Natural and simulated seawater discussed; no single quantitative exposure result in cited passage | β′ is preferentially corroded; after β′ removal, attack concentrates at anodic α adjacent to cathodic κ<sub>III</sub>; seawater oxide film lowers corrosion rate by factor 20–30; weld-induced β′ raises selective-phase-corrosion risk | PWHT transforms β′ to α + κ and relieves residual stress; numerical strength penalty not reported | [CITE] [NAVY] |
| Literature gap through Nov. 2026 (iatan2025optimizationofpulsed pages 7-9, iatan2025optimizationofpulsed pages 16-16, doyle2022additivemanufacturingof pages 53-58, zhao2022thelaserdeposited pages 15-16) | Blown-powder laser DED, laser cladding, LPBF, WAAM, or other rapid solidification | Nickel-free Cu-Al-Fe: C95300, C95400, C61400, CuAl10Fe, or ERCuAl-A2 | As deposited or heat treated | Seawater, ASTM D1141 substitute seawater, or NaCl | **No published corrosion test of a laser-deposited/DED nickel-free Cu-Al-Fe aluminum bronze was found.** Published AM chloride-corrosion studies located concern nickel-containing NAB, not C95300/C95400/C61400 | No paired corrosion–mechanical dataset exists for as-deposited nickel-free Cu-Al-Fe DED | [CITE] [GAP] |


*Table: Quantitative corrosion and mechanical benchmarks for laser/arc-deposited NAB, conventional Cu-Ni, and related heat-treated alloys. The final rows isolate the InssTek C95300 evidence gap and the absence of published chloride-corrosion testing for additively manufactured nickel-free Cu-Al-Fe.*

---

### (1) Selective Phase Corrosion (Dealuminification) of Retained β/β′ Martensite and γ₂ Eutectoid

**Which phases are attacked.** In aluminum bronze and NAB exposed to seawater or 3.5 wt% NaCl, the retained β′ (martensitic) phase is *preferentially corroded* whenever it is present (dobson2024corrosionmechanismsanda pages 35-39, dobson2024corrosionmechanismsand pages 39-42). The β′ phase is a copper-rich BCC martensite that retains a high aluminum content and is thermodynamically unstable in chloride media. Where β′ has been eliminated by heat treatment, selective phase corrosion (SPC) shifts to the α–κ_III eutectoid at grain boundaries, where the lamellar nickel-rich κ_III phase acts as the cathode and the adjacent copper-rich α phase acts as the anode, creating a persistent microgalvanic couple (dobson2024corrosionmechanismsand pages 39-42). The γ₂ phase is described as "highly corrodible" and aluminum-rich; it forms by eutectoid decomposition of β during slow cooling below ~565 °C and is the primary reason that temper annealing must be carefully controlled (dobson2024corrosionmechanismsanda pages 35-39, dobson2024corrosionmechanismsand pages 35-39). In nickel-free aluminum bronzes (no κ_III or κ_I), the γ₂ eutectoid replaces the κ phases as the principal β-decomposition product, making it the dominant site of selective attack.

**Mechanism.** Dealuminification is the selective dissolution of aluminum from the aluminum-bronze microstructure in seawater, leaving behind a porous, copper-enriched residue (phull20172.18–marine pages 28-29). The anodic dissolution reactions proceed as Cu → Cu⁺ + e⁻, Cu⁺ + 2Cl⁻ → CuCl₂⁻, and Al + 4Cl⁻ → AlCl₄⁻ + 3e⁻, with subsequent hydrolysis forming Cu₂O and Al₂O₃ (dobson2024corrosionmechanismsand pages 39-42). In properly heat-treated NAB, a protective oxide film (outer Cu₂O/CuO, inner Al₂O₃) forms on the surface and reduces the corrosion rate by a factor of 20–30 (dobson2024corrosionmechanismsand pages 39-42).

**Galvanic relationships.** The κ phases (κ_I through κ_IV) are cathodic relative to the anodic α matrix. Increasing precipitation and coarsening of κ phases (as occurs during heat treatment at 550–675 °C) draws a larger galvanic current through the α phase and can *reduce* corrosion resistance (shahriari2023corrosionperformanceof pages 1-2). The β/β′ phase and γ₂ phase are both more anodic (more active) than α and are therefore preferentially attacked (dobson2024corrosionmechanismsanda pages 35-39).

**Rates and depths.** Specific selective-attack depths for nickel-free aluminum bronze were not found in the obtainable literature. For cast NAB, selective phase corrosion under cavitation conditions transitions from dominant SPC (first 0.5 h) to mixed SPC/uniform corrosion (~1 h) to dominant uniform corrosion (2–5 h) as κ phases are physically stripped away (li2023understandingthecorrosion pages 1-2). Quantitative penetration-depth data for Ni-free grades (C95300, C95400) in seawater immersion were sought but not obtained from the accessible papers; the unobtainable references Ferrara & Caton (1981, NACE CORROSION 81-198, doi:10.5006/c1981-81198) and Foster, Zanis & Crisci (1967, NAVSEA, doi:10.21236/ad0817578) are likely the primary Navy sources for dealuminification depth data on Ni-free cast aluminum bronzes.

**[CITE] [GAP]** No quantitative selective-attack depth data for Ni-free Cu-Al-Fe in the as-deposited DED or as-welded condition were found.

---

### (2) Classic Composition Rules for Seawater Service

**The 8.2 + 0.5Ni rule.** Taylor (2018) cites the Copper Development Association (CDA) in stating that "pitting brought about by the preferential phase attack may be stopped" when aluminum is less than 8.2 wt% and nickel is at least 0.5 wt% (taylor2018effectofa pages 8-10). This is the empirical lower bound of the well-known Meigh/CDA guideline Al_max ≈ 8.2 + Ni/2 (wt%), which determines how much aluminum can be tolerated before corrosion-susceptible β or γ₂ phases appear. The full derivations from Meigh (1993, "Cast and Wrought Aluminium Bronzes"), CDA Publication 82 (formerly 80), and CDA Publication 222 were not available in the obtainable papers but are referenced extensively in the field.

**The binary limit near 9.4 wt% Al.** For binary Cu-Al alloys (no Ni, no Fe), the β phase begins forming at about 9.4 wt% Al under equilibrium conditions; however, commercial single-phase α alloys are limited to below ~8 wt% Al for seawater service (nuttall1981anassessmentof pages 55-60, kass1989evaluationofcopper pages 5-10). The practical significance is that C95300 (Al 9–11 wt%, no Ni) lies well above the safe binary limit and will retain β or β′ on rapid cooling.

**Why Ni ≥ Fe.** Nickel and iron both suppress the formation of the highly corrodible γ₂ phase and promote the formation of κ intermetallic phases. When nickel content exceeds iron content, iron is fully bound in κ_II (Fe₃Al) and κ_IV precipitates, and nickel forms the κ_III (NiAl-based) eutectoid that replaces γ₂. If iron exceeds nickel, unbound iron can promote undesirable iron-rich intermetallics and fails to fully suppress γ₂ (dobson2024corrosionmechanismsanda pages 35-39). In nickel-free alloys, there is no nickel to suppress γ₂ at all; accordingly, γ₂ forms directly from the β eutectoid decomposition, and a post-casting or post-welding temper anneal at ~600–700 °C is essential to decompose retained β into a fully transformed α + γ₂ microstructure and to spheroidize any γ₂, reducing its corrodibility. Even so, nickel-free alloys are considered inferior to NAB for seawater service.

**Defence Standard 02-747 Part 2.** For NAB castings used in UK naval seawater-wetted service, heat treatment is mandated: a minimum of 6 hours at 675 °C ± 15 °C, followed by cooling in still air (dobson2024corrosionmechanismsand pages 39-42, dobson2024corrosionmechanismsanda pages 35-39). This decomposes retained β′ into α + κ phases and avoids re-forming γ₂ by preventing too-slow cooling through the eutectoid temperature range. UK Defence Standard 02-747 also places restrictions on weld repair of wetted NAB due to the re-introduction of β′ in the HAZ (dobson2024corrosionmechanismsand pages 42-45). **[CITE] [NAVY]**

---

### (3) Quantitative Comparisons: Ni-Free Aluminum Bronze vs. NAB vs. Cu-Ni

**Laser-deposited NAB coatings.** Zhao et al. (2022) tested laser-deposited NAB coatings on SUS630 in 3.5 wt% NaCl at 25 °C. The as-deposited corrosion current densities were i_corr = 7.82 ± 0.5 µA/cm² (direct deposition), 4.65 ± 0.5 µA/cm² (Ni interlayer), and 4.09 ± 0.4 µA/cm² (NiCr interlayer), with E_corr approximately −248 to −255 mV and R_p = 2810–5275 Ω·cm² (zhao2022thelaserdeposited pages 7-10). **[CITE] [NUMBERS]**

**WAAM NAB vs. cast NAB.** Shahriari et al. (2023) found that as-built WAAM NAB had the *lowest* i_corr among all conditions tested in 3.5 wt% NaCl, with E_corr ≈ −0.293 V vs. Ag/AgCl. Heat-treated WAAM samples showed i_corr on the order of 4.4–8 × 10⁻⁶ A/cm², comparable to cast NAB. The as-built superiority was attributed to finer dendritic microstructure and suppression of coarse κ intermetallics (shahriari2023corrosionperformanceof pages 2-2, shahriari2023corrosionperformanceof pages 10-12, shahriari2023corrosionperformanceof pages 12-14). **[CITE] [NUMBERS]**

**Cu-Ni alloys.** Lewis & LaQue (1981) report C70600 (90-10 Cu-Ni) corrosion rates of 0.2–0.6 mpy (≈0.005–0.015 mm/yr) in quiet seawater and 0.5–1.1 mpy (≈0.013–0.028 mm/yr) in flowing seawater, while C71500 (70-30 Cu-Ni) shows 0.3–0.5 mpy (≈0.008–0.013 mm/yr) and 0.5–0.7 mpy (≈0.013–0.018 mm/yr), respectively. In one-year flowing seawater tests at 0.6 m/s: C70600 = 30.5 µm/yr, C71500 = 20.3 µm/yr (lewis1981evaluationofcoppernickel pages 48-55, lewis1981evaluationofcoppernickel pages 43-48). These are benchmark targets for the PI's proposal. **[CITE] [NUMBERS]**

**Normalized cast NAB.** Takaloo et al. (2011) found that NAB normalized at 675 °C for 45 min exhibited the best corrosion performance after 75 days in artificial seawater, with E_corr ≈ −123 mV and lowest measured current (~3.13 µA vs. 6.15 µA for the reference condition) (takaloo2011corrosionbehaviorof pages 12-13). **[CITE] [NUMBERS]**

**Direct comparison of Ni-free aluminum bronze vs. NAB in any AM condition was not found.** No obtainable paper compares the electrochemical behavior of as-deposited C95300/C95400 (Ni-free) against NAB in chloride media. This is a clear gap. **[GAP]**

---

### (4) Predictions for an As-Deposited InssTek DMT C95300 Deposit Used Without Heat Treatment

The InssTek material database lists "Al-Bronze / UNS C95300" (Cu balance, Al 9–11 wt%, Fe 0.8–1.5 wt%, no Ni) as a qualified DMT material with UTS of 628 MPa (XY) and 598 MPa (Z). No corrosion data, heat treatment, or laser parameters are provided. **[INSSTEK] [GAP]**

**Microstructural prediction.** C95300 at 9–11 wt% Al, with no nickel, is well above the binary β-formation threshold (~8 wt% Al equilibrium, ~9.4 wt% β₀ for binary alloys) (nuttall1981anassessmentof pages 55-60). Under the rapid cooling rates of laser DED (10³–10⁴ K/s), the β phase will be retained as β′ martensite rather than decomposing to the equilibrium α + γ₂ eutectoid (kuprienko2025analysisofnickel pages 55-61, kuprienko2025analysisofnickel pages 61-67). The high UTS (598–628 MPa) is consistent with a substantially martensitic microstructure, as analogous wire-fed LDED NAB with 8.64% Al exhibits as-printed UTS of 758 MPa with α + β′ microstructure (doyle2022additivemanufacturingof pages 53-58, doyle2022additivemanufacturingof pages 47-53). Without nickel, no κ_III or κ_I phases can form; without sufficient iron, κ_II and κ_IV formation is also limited.

**Corrosion prediction.** The as-deposited C95300 deposit will almost certainly contain a large volume fraction of retained β′ martensite—the phase most susceptible to selective corrosion in seawater (dobson2024corrosionmechanismsanda pages 35-39, dobson2024corrosionmechanismsand pages 39-42). Without nickel, the alloy also lacks the κ phases that, despite being cathodic, contribute to the formation of a protective Al₂O₃-rich inner oxide film. The γ₂ phase that would form on slow cooling is itself highly corrodible (dobson2024corrosionmechanismsanda pages 35-39). The alloy composition violates the CDA rule (Al < 8.2 + Ni/2 ≈ 8.2 wt% when Ni = 0) by a wide margin (taylor2018effectofa pages 8-10). **The as-deposited C95300 DED material should not be used in seawater without post-build heat treatment.** Rapid dealuminification and selective phase corrosion of β′ are expected under immersion or flowing-seawater conditions.

**Heat treatment to restore corrosion resistance.** By analogy with NAB, a temper anneal at 675 °C ± 15 °C for ≥ 6 h (still-air cool) would decompose β′ into α + γ₂ (since no Ni is present to form κ_III) (dobson2024corrosionmechanismsanda pages 35-39, dobson2024corrosionmechanismsand pages 35-39). In wire-fed LDED NAB, this treatment reduced YS from 411 to 372 MPa (−9.3%) and UTS from 758 to 715 MPa (−5.7%), while elongation improved from 29% to 31% and hardness decreased from 219 to 204 HV (doyle2022additivemanufacturingof pages 53-58). For C95300, the strength reduction would likely be *larger* because: (a) the alloy has more retained β′ to decompose, and (b) the decomposition product is γ₂ (which is weaker than κ), not α + κ. A reasonable estimate is that UTS would drop from ~600–630 MPa to the range of cast-and-tempered C95300 (typically ~515 MPa per ASTM B148 TQ50 temper). Even after temper annealing, γ₂ remains more corrodible than the κ phases in NAB, so corrosion resistance will still be inferior to properly heat-treated NAB.

The cooling rate after tempering is critical: cooling must be fast enough (still air, not furnace cool) to prevent the eutectoid reversal (γ₂ + α → β) and slow enough to avoid re-quenching β′. This narrow process window is more challenging for DED builds than for castings because of complex thermal paths and residual stresses (dobson2024corrosionmechanismsand pages 39-42, dobson2024corrosionmechanismsand pages 42-45).

---

### (5) Is There Any Published Corrosion Test of a Laser-Deposited or DED Cu-Al-Fe (No Ni) Aluminum Bronze in Seawater or NaCl?

**No.** After extensive searching across Google Scholar, patent databases, and cited references, no published corrosion test of a laser-deposited, laser-clad, DED, WAAM, LPBF, or other rapidly solidified nickel-free Cu-Al-Fe aluminum bronze (C95300, C95400, C61400, CuAl10Fe, ERCuAl-A2) in seawater or NaCl was identified (iatan2025optimizationofpulsed pages 7-9, iatan2025optimizationofpulsed pages 16-16, doyle2022additivemanufacturingof pages 53-58, zhao2022thelaserdeposited pages 15-16, zhao2022thelaserdeposited pages 1-2). All published AM-bronze corrosion studies in chloride media that were found concern nickel-containing NAB (C95800, C63200). The InssTek material database lists C95300 as a qualified DMT material but provides no corrosion data. **[GAP]**

Several unobtainable references that may contain relevant data for cast Ni-free aluminum bronze dealuminification include: Ferrara & Caton (1981, NACE CORROSION 81-198), Foster, Zanis & Crisci (1967, NAVSEA Report AD-817578), and Upton (1963, J. Electrochem. Soc.). These are Navy/DoD sources that likely provide dealuminification-depth data for cast C95300/C95400 in seawater but would not address the as-deposited DED condition. **[NAVY] [GAP]**

---

### Key References with Full Citations

1. **Zhao, L.; Li, K.; Yao, J.; Yuan, Y.; Du, B.** "The Laser Deposited Nickel-Aluminum Bronze Coatings on SUS630 Stainless Steel and Its Corrosion Resistance in 3.5 wt.% NaCl Solution." *Metals* 2022, 12, 781. DOI: 10.3390/met12050781. Process: Powder-fed laser deposition. **[CITE] [NUMBERS]**

2. **Shahriari, A.; Chalasani, D.; Amirkhiz, B.S.; Mohammadi, M.** "Corrosion performance of wire arc additively manufactured NAB alloy." *npj Materials Degradation* 2023, 7, 1–15. DOI: 10.1038/s41529-023-00405-x. Process: GMAW-WAAM. **[CITE] [NUMBERS]**

3. **Doyle, R.P.** "Additive Manufacturing of FeCrCoCuNi High Entropy Alloy via Laser Powder Bed Fusion and Nickel Aluminum Bronze via Laser Directed Energy Deposition." Thesis, 2022. Process: Wire-fed laser DED (six 200 W diodes). **[CITE] [NUMBERS] [GAP]**

4. **Dobson, T.H.E.** "Corrosion Mechanisms and Fatigue Behaviour of Marine Biofouled Plasma Welded Nickel Aluminium Bronze." PhD Thesis, 2024. Process: Plasma welding of NAB per Defence Standard 02-747. **[CITE] [NAVY]**

5. **Taylor, R.** "Effect of a Simulated Butterfly Valve on the Erosion-Corrosion Rate of Nickel Aluminum Bronze Alloys in Highly Turbulent Seawater." MS Thesis, Virginia Tech, 2018. Process: Cast C95510 NAB; CDA composition rules cited. **[CITE] [NAVY]**

6. **Takaloo, A.V.; Daroonparvar, M.R.; Atabaki, M.M.; Mokhtar, K.** "Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater." *J. Metallurgy and Materials Science* 2011, 53, 67–84. DOI: 10.4236/msa.2011.211207. Process: Cast NAB, various heat treatments. **[CITE] [NUMBERS]**

7. **Lewis, R.O.; LaQue, F.** "Evaluation of copper-nickel alloys for OTEC applications." Report, 1981. DOI: 10.2172/6255887. Process: Wrought C70600/C71500. **[CITE] [NUMBERS]**

8. **Gao, X.; Liu, M.** "Corrosion Behavior of High-Strength C71500 Copper-Nickel Alloy in Simulated Seawater with High Concentration of Sulfide." *Materials* 2022, 15, 8513. DOI: 10.3390/ma15238513. Process: Conventional C71500. **[CITE] [NUMBERS]**

9. **Li, L.; Qiao, Y.-X.; Zhang, L.-M.; Ma, A.-L.; Ma, R.; Zheng, Y.-G.** "Understanding the Corrosion Behavior of Nickel–Aluminum Bronze Induced by Cavitation Corrosion Using Electrochemical Noise." *Materials* 2023, 16, 669. DOI: 10.3390/ma16020669. Process: Cast NAB. **[CITE]**

10. **Kuprienko, A.** "Analysis of Nickel Aluminum Bronze Weld Metal Microstructure and Mechanical Response as a Function of Cooling Rate." Thesis, 2025. Process: GMA-P DED-Arc with LN₂ cooling; MIL-CuNiAl wire on C63200. **[CITE] [NAVY] [GAP]**

11. **Makarenko, K.I.; Dubinin, O.; Shishkovsky, I.V.** "Analytical Evaluation of the Dendritic Structure Parameters and Crystallization Rate of Laser-Deposited Cu-Fe Functionally Graded Materials." *Materials* 2020, 13, 5665. DOI: 10.3390/ma13245665. Process: DED of Cu-10Al-1Fe bronze and SS316L on InssTek MX-1000 (DMT process). **[CITE] [INSSTEK]**

12. **Kass, J.N.** "Evaluation of copper, aluminum bronze, and copper-nickel for YMP container material." UCRL-101097, 1989. DOI (report). Process: Wrought CDA 613 (Cu-7Al-3.5Fe), CDA 715 (Cu-30Ni). **[CITE] [NUMBERS]**

13. **Iatan, G.; Cuculea, D.; Ardelean, G.; Stanciu, E.; Pascu, A.** "Optimization of Pulsed Laser Cladding for Reconditioning of Ni–Al–Bronze (NAB) Marine Propeller." *Materials* 2025, 18, 4301. DOI: 10.3390/ma18184301. Process: Pulsed laser cladding of CuNi powder on NAB propeller. **[CITE] [NAVY]**

---

### Top 5 Things the PI Should Know

**1. [GAP] No one has tested DED/laser-deposited Ni-free Cu-Al-Fe bronze for corrosion in seawater or NaCl.** All published AM-bronze corrosion data in chloride media are for nickel-containing NAB (C95800/C63200). The InssTek C95300 listing provides mechanical data only. This is the single most important finding: the PI's first DED C95300 corrosion test would be novel and publishable, and would directly address the proposal's central risk.

**2. As-deposited C95300 will almost certainly fail in seawater.** With 9–11 wt% Al and no Ni, the alloy sits far above the CDA safety limit of ~8.2 wt% Al (for Ni = 0). Rapid solidification during laser DED will retain β′ martensite—the most corrosion-susceptible phase in the Cu-Al system. The high UTS (598–628 MPa) reported by InssTek is itself evidence of a martensitic microstructure. Without heat treatment, rapid dealuminification and selective phase corrosion are expected.

**3. A 675 °C / 6 h temper anneal would decompose β′ but yield only γ₂ (not κ).** In the absence of nickel, the β → eutectoid reaction produces α + γ₂ rather than α + κ_III. The γ₂ phase is itself corrosion-susceptible, so even heat-treated C95300 is inherently inferior to heat-treated NAB in seawater. The strength penalty for the temper anneal is estimated at ~10% in YS (by analogy with LDED NAB, which dropped from 411 to 372 MPa). Cast-and-tempered C95300 typically has UTS ~515 MPa, so the as-deposited 600+ MPa would likely decline to that range.

**4. WAAM and laser DED NAB (with Ni) show promising as-built corrosion behavior.** Shahriari et al. (2023) found that as-built WAAM NAB had *better* chloride corrosion resistance than cast NAB, because its finer dendritic microstructure and suppressed κ precipitation reduced microgalvanic driving forces. Paradoxically, heat treatment at 550–675 °C worsened corrosion resistance by coarsening κ phases. This suggests that for NAB compositions (Al ≤ 9.5, Ni ≥ Fe), the as-deposited DED condition may be acceptable for seawater—a finding that directly supports the PI's proposal goal of "as deposited" service *if the alloy contains adequate nickel*.

**5. The PI's alloy design space should prioritize sufficient Ni to suppress γ₂ and meet Al < 8.2 + Ni/2.** For Cu-Ni alloys (C71500), long-term seawater corrosion rates are only ~20 µm/yr. For NAB within specification (Al 8.8–9.5, Ni 4.5–5.5), heat-treated corrosion rates are comparable. Ni-free alloys with Al > 8.2% are outside the safe envelope for seawater without post-build heat treatment. The PI's searched space (Ni 0–30, Al 0–9.5) should weight toward compositions with Ni ≥ Fe and Al < 8.2 + Ni/2 if as-deposited seawater service is required. The C63000 (Cu-10Al-5Ni-3Fe) feedstock for the first atomization run has Ni > Fe and is a NAB, not a Ni-free aluminum bronze, which is a more favorable starting point than C95300 for seawater DED.


References

1. (zhao2022thelaserdeposited pages 7-10): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

2. (zhao2022thelaserdeposited pages 2-4): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

3. (shahriari2023corrosionperformanceof pages 2-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 31 citations and is from a peer-reviewed journal.

4. (shahriari2023corrosionperformanceof pages 10-12): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 31 citations and is from a peer-reviewed journal.

5. (shahriari2023corrosionperformanceof pages 12-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 31 citations and is from a peer-reviewed journal.

6. (doyle2022additivemanufacturingof pages 53-58): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

7. (doyle2022additivemanufacturingof pages 47-53): RP Doyle. Additive manufacturing of fecrcocuni high entropy alloy via laser powder bed fusion and nickel aluminum bronze via laser directed energy deposition. Unknown journal, 2022.

8. (lewis1981evaluationofcoppernickel pages 48-55): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

9. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

10. (gao2022corrosionbehaviorof pages 4-5): Xin Gao and Ming Liu. Corrosion behavior of high-strength c71500 copper-nickel alloy in simulated seawater with high concentration of sulfide. Materials, 15:8513, Nov 2022. URL: https://doi.org/10.3390/ma15238513, doi:10.3390/ma15238513. This article has 35 citations.

11. (gao2022corrosionbehaviorof pages 2-4): Xin Gao and Ming Liu. Corrosion behavior of high-strength c71500 copper-nickel alloy in simulated seawater with high concentration of sulfide. Materials, 15:8513, Nov 2022. URL: https://doi.org/10.3390/ma15238513, doi:10.3390/ma15238513. This article has 35 citations.

12. (takaloo2011corrosionbehaviorof pages 12-13): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 43 citations and is from a peer-reviewed journal.

13. (takaloo2011corrosionbehaviorof pages 5-7): Ashkan Vakilipour Takaloo, Mohammad Reza Daroonparvar, Mehdi Mazar Atabaki, and Kamran Mokhtar. Corrosion behavior of heat treated nickel-aluminium bronze alloy in artificial seawater. Journal of Metallurgy and Materials Science, 53:67-84, Nov 2011. URL: https://doi.org/10.4236/msa.2011.211207, doi:10.4236/msa.2011.211207. This article has 43 citations and is from a peer-reviewed journal.

14. (kuprienko2025analysisofnickel pages 67-72): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

15. (dobson2024corrosionmechanismsand pages 39-42): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

16. (dobson2024corrosionmechanismsand pages 42-45): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

17. (iatan2025optimizationofpulsed pages 7-9): George Iatan, Dan Cuculea, George Ardelean, Elena Stanciu, and Alexandru Pascu. Optimization of pulsed laser cladding for reconditioning of ni–al–bronze (nab) marine propeller. Sep 2025. URL: https://doi.org/10.3390/ma18184301, doi:10.3390/ma18184301. This article has 5 citations.

18. (iatan2025optimizationofpulsed pages 16-16): George Iatan, Dan Cuculea, George Ardelean, Elena Stanciu, and Alexandru Pascu. Optimization of pulsed laser cladding for reconditioning of ni–al–bronze (nab) marine propeller. Sep 2025. URL: https://doi.org/10.3390/ma18184301, doi:10.3390/ma18184301. This article has 5 citations.

19. (zhao2022thelaserdeposited pages 15-16): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

20. (dobson2024corrosionmechanismsanda pages 35-39): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

21. (dobson2024corrosionmechanismsand pages 35-39): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

22. (phull20172.18–marine pages 28-29): B Phull and AA Abdullahi. 2.18 – marine corrosion. ArXiv, 2:1107-1148, Jan 2010. URL: https://doi.org/10.1016/b978-044452787-5.00046-9, doi:10.1016/b978-044452787-5.00046-9. This article has 62 citations.

23. (shahriari2023corrosionperformanceof pages 1-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 31 citations and is from a peer-reviewed journal.

24. (li2023understandingthecorrosion pages 1-2): Liang Li, Yan-Xin Qiao, Lian-Min Zhang, Ai-Li Ma, Rongyao Ma, and Yu-Gui Zheng. Understanding the corrosion behavior of nickel–aluminum bronze induced by cavitation corrosion using electrochemical noise: selective phase corrosion and uniform corrosion. Materials, 16:669, Jan 2023. URL: https://doi.org/10.3390/ma16020669, doi:10.3390/ma16020669. This article has 33 citations.

25. (taylor2018effectofa pages 8-10): RC Taylor. Effect of a simulated butterfly valve on the erosion-corrosion rate of nickel aluminum bronze alloys in highly turbulent seawater. Unknown journal, 2018.

26. (nuttall1981anassessmentof pages 55-60): K Nuttall and VF Urbanic. An assessment of materials for nuclear fuel immobilization containers. Unknown journal, 1981.

27. (kass1989evaluationofcopper pages 5-10): JN Kass. Evaluation of copper, aluminum bronze, and copper-nickel for ymp container material. Unknown journal, 1989.

28. (kuprienko2025analysisofnickel pages 55-61): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

29. (kuprienko2025analysisofnickel pages 61-67): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

30. (zhao2022thelaserdeposited pages 1-2): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.
