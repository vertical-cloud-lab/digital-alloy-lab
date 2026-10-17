<!--
Edison Scientific LITERATURE task (batch 4)
- Task ID: 9864ee44-946d-4a61-a4aa-f3c82e2666b4
- Submitted: 2026-10-17T06:11:11Z
- Fetched: 2026-10-17T06:41:52Z (status: success)
- Raw trajectory JSON: ../raw/b4-04-chromium-modified-cuni.json.gz
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

QUESTION: What is known about chromium-modified copper-nickel alloys
(C72200 Cu-16Ni-0.5Cr; CuNi30Cr2 / IN-768 castings used by navies; Cu-30Ni-
xCr) as seawater alloys and as candidates for welding or additive
manufacturing? Cover Cr solubility and Cr-rich precipitates, the effect of
Cr segregation on quiet-water localized corrosion, erosion-corrosion and
critical velocity data, weldability and filler metals, and any laser
cladding, DED or LPBF studies (e.g. Gao et al. 2025 SLM Cu-30Ni-xCr with
mixed powders; Zhou et al. 2025 Wear, laser-cladded Cu-Ni-xCr). What Cr
range would a DED powder design space reasonably span?

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

QUESTION: What is known about chromium-modified copper-nickel alloys
(C72200 Cu-16Ni-0.5Cr; CuNi30Cr2 / IN-768 castings used by navies; Cu-30Ni-
xCr) as seawater alloys and as candidates for welding or additive
manufacturing? Cover Cr solubility and Cr-rich precipitates, the effect of
Cr segregation on quiet-water localized corrosion, erosion-corrosion and
critical velocity data, weldability and filler metals, and any laser
cladding, DED or LPBF studies (e.g. Gao et al. 2025 SLM Cu-30Ni-xCr with
mixed powders; Zhou et al. 2025 Wear, laser-cladded Cu-Ni-xCr). What Cr
range would a DED powder design space reasonably span?

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


# Chromium-modified Cu–Ni for seawater and laser deposition

**Assessment.** Chromium is a credible addition to marine Cu–Ni, particularly where flowing seawater threatens the protective film. It is not an unqualified corrosion improvement: historical low-flow exposures show greater localized attack for a Cr-modified 70/30 alloy than for conventional C71500, while Navy casting experience identifies coring, impurity control, and restrictions on seawater-wetted weld repairs. None of the retrieved evidence demonstrates that an **as-deposited, single-stream, pre-alloyed-powder laser DED** repair meets or exceeds wrought C71500 in seawater. (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 43-48, king1992thehotisostatic pages 21-27, king1992thehotisostatic pages 27-32)

The table separates verified benchmarks from results that could not be checked. Values from different processes and exposures should not be treated as a common corrosion ranking. (lewis1981evaluationofcoppernickel pages 17-19, polan1981erosioncorrosionresistanceof pages 3-6, lewis1981evaluationofcoppernickel pages 43-48)

| Alloy / process | Environment | Reliable numbers | Interpretive caveat |
|---|---|---|---|
| **C72200, wrought sheet; rotating-disc erosion-corrosion** — Polan et al. (1981) | ASTM D1141-75 substitute ocean water, **40°C**, **1000 ppm 5 µm sharp silica**, **2.1 m/s**, **14 d** | Composition: Cu–**16.1Ni–0.64Cr–0.65Fe–0.71Mn wt%**. Extrapolated loss: annealed **0.108 mm/y**; 40% cold-worked **0.088 mm/y**; C70600 control **0.275 mm/y**. Vickers hardness: **87** annealed and **150** at 40% cold work. (polan1981erosioncorrosionresistanceof pages 3-6, polan1981erosioncorrosionresistanceof pages 1-3) | Short, abrasive accelerated test—not quiet natural seawater. The **4.2 m/s** results were distorted by flow separation and are not a metal breakaway-velocity benchmark. |
| **C71900 Cu–30Ni–Cr versus C71500; wrought, low-velocity exposure** — Lewis & LaQue (1981) | Natural seawater averaging **64°F**; no flow or **2 ft/s** | No flow: C71900, **6–9 months**, **0.0006–0.001 in/y**, localized depth **0.003–0.009 in** at crevices and **0.004–0.009 in** elsewhere; C71500, **1 y**, **0.0003–0.0009 in/y**, **nil–0.006 in** at crevices and **nil–0.004 in** elsewhere. At 2 ft/s: C71900 **0.001–0.003 in/y**, localized **0.002–0.006 / 0.003–0.007 in**; C71500 **0.0002–0.0008 in/y**, **nil–0.003 in / incipient**. (lewis1981evaluationofcoppernickel pages 43-48, lewis1981evaluationofcoppernickel media 6b86b115) | Durations are unmatched—**6–9 months** for C71900 versus **1 year** for C71500—so this supports a quiet-water localized-corrosion warning, not a controlled head-to-head rate claim. |
| **IN768, cast Cu–30Ni–Cr–Si; UK Navy/submarine application** — King (1992) | Natural seawater: Langstone Harbour full immersion **1 y**; submarine auxiliary seawater system at **3 m/s** for **90 d** | Trial chemistry reported: **30.10Ni–0.60Fe–0.70Mn–0.49Si wt%**, with the alloy described as about **1.6Cr**. Harbour: average **0.02 mm/y**, maximum **0.05 mm/y**. Submarine probe: admittance fell **18→7 µA/mV** in **40 d**, then remained steady to removal **50 d** later; steady corrosion equivalent **0.05 mm/y**. One-year crevice maximum **0.18 mm**. (king1992thehotisostatic pages 43-49, king1992thehotisostatic pages 49-55, king1992thehotisostatic pages 27-32, king1992thehotisostatic pages 304-311) | Navy-relevant cast evidence, not DED. IN768 exhibits strong **Ni coring**—up to **44.5 wt% Ni** locally—but the retrieved evidence does not prove analogous Cr segregation. |
| **NES 824 cast Cu–Ni–Cr versus cast NAB** — King (1992) | Marine-performance compilation; cavitation condition **40 m/s**, cavitation number **0.08** | NES 824: proof stress **300–320 MPa**, UTS **480–540 MPa**, elongation **18–25%**, HB **170–200**; NAB: **270 MPa**, **660 MPa**, **15%**, HB **160**. Full-immersion rates **0.02 versus 0.07 mm/y**; cavitation volume loss **3.2 versus 1.0 mm³/h**. (king1992thehotisostatic pages 304-311) | Cr-bearing Cu–Ni has better general seawater corrosion but **worse cavitation loss than NAB**; high-flow corrosion and mechanical cavitation are not interchangeable. |
| **IN732 Cu–30Ni–2.8Cr; multipass GTAW and simulated HAZ** — Holsberg (1970) | Four-pass GTAW plate; two-pass GTAW pipe; natural-seawater SCC exposure **1000 h** | Base alloy: **30Ni–2.8Cr–0.7Mn–0.1Si–0.05Ti–0.15Zr wt%**; UTS/yield/elongation **87/52 ksi/30%**. Four-pass weld: UTS **80 ksi**, 2-in-gage and HAZ yield **55 ksi**, weld-metal yield **50 ksi**. Two-pass pipe: UTS **88→83 ksi**, a **6%** loss. No HAZ cracking in Varestraint tests and no SCC failure in **1000 h**. (holsberg1970weldabilitystudiesof pages 1-2, holsberg1970weldabilitystudiesof pages 3-4, holsberg1970weldabilitystudiesof pages 4-5, holsberg1970weldabilitystudiesof pages 5-5) | Strong evidence that a high-Cr grade can be fusion welded under controlled shielding, but GTAW plate/pipe does not establish crack-free multilayer powder DED or as-deposited seawater equivalence. |
| **NES 825 / IN732-type welding wire; wire feedstock specification** — King (1992) | Intended for MIG/TIG joining of NES 824 castings | Cu balance; **29.0–32.0Ni, 2.0–2.4Cr, 1.4–2.0Mn, 0.2–0.4Si, 0.05–0.15Zr, 0.1–0.2Ti wt%**; Fe maximum **0.05 wt%** and total listed impurities tightly limited. MIG trials produced sound, ductile weld deposits. (king1992thehotisostatic pages 27-32, king1992thehotisostaticb pages 304-311, king1992thehotisostatic pages 304-311) | The mature filler composition is a useful upper-Cr feasibility anchor, but it contains Zr/Ti and is not evidence for atomized pre-alloyed powder flow, oxygen, DED density, or seawater corrosion. |
| **Chromium-free Cu–Ni LPBF literature; review** — Nemani et al. (2024) | LPBF studies; one corrosion study used **3% NaCl** and **1 M HCl** | Cu–5/10/15Ni: powder **20–43 µm**, steel plate at **80°C**, **240 W**, **200–500 mm/s**, **0.2 mm** hatch, **0.06 mm** layers. Cu–19Ni: **40 µm** powder, **200 W**, **0.02 mm** layers. Higher Ni improved density qualitatively. (nemani2024advancementsinadditive pages 26-28) | These alloys contain no Cr; the review reports no quantitative density or corrosion values in the retrieved passage. It demonstrates Cu–Ni laser processability, not Cu–Ni–Cr marine performance. |
| **Gao et al. (2025), reported mixed-powder SLM Cu–30Ni–xCr** | Not verifiable from the retrieved corpus | **No reliable composition, powder, density, hardness, mechanical, or corrosion numbers recovered.** | Do not cite numerical claims until the full bibliographic record and primary paper are obtained. Mixed elemental powders would overlap composition screening but **not** the proposed single-stream pre-alloyed-powder DED route. |
| **Zhou, Wen & Zuo (2025), laser-cladded Cu–Ni–xCr coatings**, *Wear*, article 205960, DOI **10.1016/j.wear.2025.205960** | Current-carrying fretting wear and electrochemical corrosion; exact electrolyte and protocol unavailable in the retrieved corpus | DOI and article identity verified; **no reliable Cr levels, powder data, porosity, hardness, wear, corrosion potential, corrosion-current density, or impedance values recovered**. | Relevant laser-cladding overlap, but not enough accessible evidence to claim seawater testing, pre-alloyed feedstock, bulk DED buildability, or any quantitative advantage. |


*Table: Compact evidence table separating verified seawater, welding, casting, and additive-manufacturing results from inaccessible or unverified claims. It highlights process and exposure differences that limit direct comparisons with pre-alloyed blown-powder DED.*

## Relevant items and interpretation

1. **N. W. Polan, M. A. Heine, J. M. Popplewell, and C. J. Gaffoglio, “Erosion-corrosion resistance of copper alloy C72200 in sea water containing suspended sand,” *Desalination* 38 (1981) 223–231. DOI: [10.1016/S0011-9164(00)86069-5](https://doi.org/10.1016/S0011-9164(00)86069-5).** **Process:** wrought, annealed or cold-worked sheet; *not* AM. **Composition:** measured C72200 Cu–16.1Ni–0.64Cr–0.65Fe–0.71Mn wt%. **Test:** rotating specimens in ASTM D1141-75 substitute ocean water at 40 °C, with 1,000 ppm silica for 14 days. At 2.1 m/s with 5-µm sharp silica, extrapolated erosion-corrosion losses were **0.108 mm/y** annealed, **0.088 mm/y** after 40% cold work, versus **0.275 mm/y** for C70600. Corresponding C72200 hardnesses were 87 and 150 Vickers. These are short-term, sand-abrasion benchmarks, **not** 30-day quiet-water corrosion rates. The authors explicitly caution that flow separation distorted their 4.2-m/s measurements; that speed is **not** an alloy critical or breakaway velocity. **[CITE] [NUMBERS] [GAP]**—no atomized powder or DED result. (polan1981erosioncorrosionresistanceof pages 3-6, polan1981erosioncorrosionresistanceof pages 1-3, polan1981erosioncorrosionresistanceof pages 6-9)

2. **R. O. Lewis and F. LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications* (1981), technical report. DOI: [10.2172/6255887](https://doi.org/10.2172/6255887).** **Process:** compilation of wrought and cast seawater tests, not an AM experiment. Jet tests covering **1.2–15.3 m/s** found **no measurable impingement attack at or below 4.6 m/s** for Cr-modified C72200 and C71900, including cast IN768. This is an apparatus- and exposure-dependent *observed no-attack limit*, not a universal pipe-design critical velocity. The report’s low-velocity table is an essential counterweight: in seawater averaging 64 °F and **no flow**, C71900 exhibited **0.0006–0.001 in/y** general loss and **0.004–0.009 in** localized attack away from crevices after **6–9 months**; C71500 exhibited **0.0003–0.0009 in/y** and **nil–0.004 in**, respectively, after **one year**. At **2 ft/s**, the respective general-loss ranges were **0.001–0.003** and **0.0002–0.0008 in/y**. Durations differ, precluding a controlled equal-time comparison, but the Cr alloy plainly cannot be presumed superior in quiet water. The same report lists C72200 general loss at **0.4–0.9 mil/y** in quiet and **0.8–1.2 mil/y** at 2 ft/s; those are separate exposures. **[CITE] [NUMBERS] [GAP]**—the mechanism and as-deposited response are not established. (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 43-48, lewis1981evaluationofcoppernickel media 6b86b115)

3. **S. King, *The Hot Isostatic Processing Characteristics of 70/30 Cupronickel Castings* (1992), thesis; DOI: not identified in the retrieved record.** **Process:** cast IN768/CN1 and Naval Engineering Standard NES 824 cast Cu–Ni–Cr, with comparisons to cast NAB; **HIP results must not be presented as as-deposited results**. The IN768 marine-trial material is reported as **30.10Ni–0.60Fe–0.70Mn–0.49Si wt%**, Cu balance and Cr-bearing; the discussion describes the selected casting alloy as approximately **1.6 wt% Cr**, but the Cr entry of the trial-composition table was not recoverable, so **1.6% should not be represented as that specimen’s verified chemical analysis**. At Langstone Harbour, one-year full immersion yielded **0.02 mm/y** mean general loss and **0.05 mm/y** maximum metallographic attack; a submarine seawater-system probe at approximately **3 m/s** gave an estimated steady **0.05 mm/y**. A separate one-year crevice exposure reached **0.18 mm** maximum penetration. Compiled NES 824 cast-property ranges were **300–320 MPa** proof stress, **480–540 MPa** UTS, **18–25%** elongation and **170–200 HB**. Its compiled cavitation loss was **3.2 mm³/h**, versus **1.0 mm³/h** for NAB under the stated 40-m/s, cavitation-number-0.08 condition: improved seawater impingement must **not** be translated into superior cavitation resistance. **[CITE] [NUMBERS] [NAVY] [GAP]**—cast naval performance, not Cu–Ni–Cr powder DED performance. (king1992thehotisostatic pages 43-49, king1992thehotisostatic pages 49-55, king1992thehotisostatic pages 27-32, king1992thehotisostatic pages 304-311)

4. **P. W. Holsberg, “Weldability Studies of Modified 70-30 CuNi Alloys,” *Welding Journal*, Research Supplement (December 1970), pp. 554-s–558-s; DOI: not identified in the retrieved record.** **Process:** wrought **IN732**, simulated weld HAZ, Varestraint and gas-tungsten-arc welded plate and pipe—not laser DED. **Nominal composition:** Cu–30Ni–2.8Cr–0.7Mn–0.1Si–0.05Ti–0.15Zr wt%, with 0.10 Fe listed. Parent typical UTS/yield/elongation were **87/52 ksi/30%**. Four-pass welded plate reached **80 ksi UTS** and **50 ksi weld-metal yield**; two-pass pipe UTS fell **88 to 83 ksi**, a **6%** reduction. No HAZ cracking was found in the reported Varestraint work, and no failure occurred in **1,000-hour natural-seawater** stress-corrosion tests of base and simulated-HAZ specimens. The tests establish conditional fusion-welding feasibility, **not** a seawater corrosion-rate benchmark or crack-free multilayer DED. **[CITE] [NUMBERS] [NAVY] [GAP]**. (holsberg1970weldabilitystudiesof pages 1-2, holsberg1970weldabilitystudiesof pages 2-3, holsberg1970weldabilitystudiesof pages 3-4, holsberg1970weldabilitystudiesof pages 4-5, holsberg1970weldabilitystudiesof pages 5-5)

5. **King (1992), reporting Navy NES 825 Issue 2 filler requirements; thesis citation and DOI as in item 3.** **Process:** MIG/TIG welding wire for cast Cu–Ni–Cr; **not** the composition specification for the NES 824 casting. **Specified major-element ranges, wt%:** Cu balance; **Ni 29.0–32.0, Cr 2.0–2.4, Mn 1.4–2.0, Si 0.2–0.4, Zr 0.05–0.15, Ti 0.1–0.2**; Fe maximum 0.05. King reports sound, ductile MIG deposits using IN732-type filler, but also explains that impurity/defect accumulation can cause cast-HAZ intergranular cracking and that the contemporary Navy specification restricted welding on seawater-wetted castings because of premature-corrosion concern. Thus, successful wire welding **does not qualify a wetted repair**. **[CITE] [NUMBERS] [NAVY] [GAP]**. (king1992thehotisostatic pages 21-27, king1992thehotisostatic pages 27-32, king1992thehotisostatic pages 304-311)

6. **A. Vahedi Nemani, M. Ghaffari, K. Sabet Bokati, N. Valizade, E. Afshari, and A. Nasiri, “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review,” *Journal of Manufacturing and Materials Processing* 8 (2024) 54. DOI: [10.3390/jmmp8020054](https://doi.org/10.3390/jmmp8020054).** **Processes:** review of Cu–Ni LPBF, laser DED and WAAM, and a **separate Cu–Cr** literature. Its Cr-free Cu–5/10/15Ni LPBF examples used **20–43 µm** powder, a **240-W** laser, **200–500 mm/s** scanning and **60-µm** layers. One reviewed Cu–Ni–Sn–Pb LPBF corrosion experiment used **3% NaCl**, not natural seawater or an otherwise equivalent C71500 comparison. The review’s findings about **Cr-rich precipitates and their microgalvanic effects concern binary Cu–Cr**; they cannot establish Cr solubility, precipitate identity, or corrosion mechanism in marine Cu–Ni–Cr. The retrieved passages supply no verified Cu–Ni–Cr DED density, powder flow/oxygen or corrosion-current benchmark. **[CITE] [GAP]**. (nemani2024advancementsinadditive pages 18-21, nemani2024advancementsinadditive pages 21-26, nemani2024advancementsinadditive pages 26-28)

7. **Y. Zhou, D. Wen, and X. Zuo, “Current-carrying fretting wear and electrochemical corrosion properties of laser-cladded Cu-Ni-xCr coatings,” *Wear* (2025), article 205960. DOI: [10.1016/j.wear.2025.205960](https://doi.org/10.1016/j.wear.2025.205960).** **Process:** laser cladding, as identified by the bibliographic record; **[NOVELTY-RISK]** because the Cu–Ni–Cr laser-cladding composition/property theme overlaps. Its full text was **unobtainable in this search**. Consequently, Cr levels, whether feedstock was pre-alloyed, substrate, electrolyte, test duration, porosity, hardness, *E*<sub>corr</sub>, *i*<sub>corr</sub> and impedance **cannot responsibly be reported**. Its title establishes neither natural-seawater qualification nor bulk, single-stream powder-DED repair. **[GAP]**—retrieve the paper before asserting that distinction more strongly.

8. **“Gao et al. (2025), SLM Cu–30Ni–xCr”**—the user-identified mixed-powder study. **Process, if the supplied identification is correct:** LPBF/SLM using mixed powders, *not* one pre-alloyed blown-powder DED feed. **[NOVELTY-RISK]** for composition screening and laser-solidification claims; **[GAP]** for the proposed feedstock/process/repair route. Targeted searches did **not** recover a verifiable full citation or DOI or inspectable primary text. Accordingly, no Cr concentrations, test medium, density, corrosion-current, hardness or powder metrics are assigned to this item; its existence and details need bibliographic confirmation before proposal citation.

### Solubility, segregation and a defensible Cr range

**What is established—and what is not.** Cr-modified cast 70/30 Cu–Ni is reported to benefit in impingement tests from additions as low as **0.2 wt%**, with studied beneficial ranges **0.2–1.75%** or **0.3–1.0%** depending on study; a historical review describes controlled marine additions of **0.5–3.0%**, improvement toward approximately **2%** at high velocity, a roughly **2% weldability limit** for its casting context, and worse low-velocity corrosion at higher Cr. These are empirical observations, **not measurements of equilibrium Cr solubility**. The same casting literature documents marked **Ni coring**—one analysis averaged **41.4 wt% Ni in dendrites versus 23.7% in matrix**—but does **not** establish that Cr segregates in the same direction or give a Cu–30Ni–Cr solvus or identified Cr-rich precipitate chemistry. IN732 strengthening was interpreted as spinodal compositional modulation; treating that account as proof of discrete Cr particles would be misleading. Determine Cr partitioning and phases experimentally in the *powder and as-deposited DED material*, rather than transferring conclusions from binary Cu–Cr. (holsberg1970weldabilitystudiesof pages 1-2, holsberg1970weldabilitystudiesof pages 2-3, king1992thehotisostatic pages 49-55, king1992thehotisostatic pages 60-67)

**Recommended design space:** use **0–2.0 wt% Cr** as the main Cu–Ni powder range, with **0, 0.2, 0.5, 1.0, 1.5 and 2.0%** as informative initial levels. Include an explicitly *exploratory*, gated **2.4–2.8%** extension only if atomization, as-deposited phase mapping, crack testing and quiet-water localized corrosion justify it: 2.0–2.4% reflects historical filler specification, whereas 2.8% is an IN732 welding precedent, not a demonstrated optimum for wetted DED. Include a C71500-matched **Cr-free control at the same Ni, Fe and Mn** and a lower-Ni C72200-like **~16Ni–0.5–0.7Cr** anchor. Because Ni/Fe/Mn, Cr, cooling history and surface preparation can alter the result, treat the range as a **screening hypothesis**, not a guaranteed seawater specification. (holsberg1970weldabilitystudiesof pages 1-2, polan1981erosioncorrosionresistanceof pages 3-6, king1992thehotisostatic pages 60-67, polan1981erosioncorrosionresistanceof pages 1-3, king1992thehotisostatic pages 27-32, king1992thehotisostatic pages 304-311)

**Unanswered proposal-critical measurements.** Retrieved sources do not give a defensible alloy-specific Cr solubility limit, phase-resolved Cr-segregation-to-quiet-water-attack relationship, or verified as-built Cu–Ni–Cr DED values for density/porosity, powder size distribution/Hall flow/apparent density/oxygen, crack frequency, *i*<sub>corr</sub>, *E*<sub>corr</sub>, impedance, or 30-day immersion loss relative to wrought C71500. Nor do they establish a seawater-wetted laser-DED bond on cast NAB or wrought Cu–Ni. Separately measure **static/crevice localization and flowing/impingement loss**: a favorable high-flow result cannot substitute for the quiet-water acceptance test, and a short polarization or 3.5% NaCl result cannot establish 30-day natural-seawater equivalence. (lewis1981evaluationofcoppernickel pages 17-19, king1992thehotisostatic pages 49-55, lewis1981evaluationofcoppernickel pages 43-48, nemani2024advancementsinadditive pages 26-28, king1992thehotisostatic pages 21-27)

## Top 5 things the PI should know

1. **The principal failure mode to avoid is a trade-off:** Cr improves impingement resistance, while historical C71900 low-flow exposures show substantial localized attack. Test *both* regimes against matched C71500 controls. (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 43-48)
2. **Use 0–2 wt% Cr for the principal powder search; make 2.4–2.8% a gated extension**, not the default, because filler weldability does not demonstrate as-deposited corrosion. (holsberg1970weldabilitystudiesof pages 1-2, king1992thehotisostatic pages 60-67, king1992thehotisostatic pages 304-311)
3. **Navy welding history makes the repair target unusually demanding:** sound welds were possible, yet seawater-wetted cast repairs faced explicit restrictions; demonstrate the actual deposited interface and HAZ in both substrate types. (holsberg1970weldabilitystudiesof pages 5-5, king1992thehotisostatic pages 21-27, king1992thehotisostatic pages 27-32)
4. **Do not infer Cr-rich particles from Ni coring or binary Cu–Cr AM.** Phase/segregation mapping along the DED thermal history is a material scientific gap and a meaningful test of the proposed physics model. (king1992thehotisostatic pages 49-55, nemani2024advancementsinadditive pages 18-21, nemani2024advancementsinadditive pages 21-26)
5. **Frame novelty narrowly and verify the 2025 papers:** Cu–Ni–Cr laser cladding already has a 2025 bibliographic record, and the reported Gao LPBF work may overlap alloy screening; the presently unverified combination is *pre-alloyed single-stream powder, as-deposited blown-powder DED, wetted dissimilar-substrate repair, and controlled long-duration seawater comparison*. (nemani2024advancementsinadditive pages 26-28, king1992thehotisostatic pages 21-27)

References

1. (lewis1981evaluationofcoppernickel pages 17-19): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

2. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

3. (king1992thehotisostatic pages 21-27): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

4. (king1992thehotisostatic pages 27-32): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

5. (polan1981erosioncorrosionresistanceof pages 3-6): N.W. Polan, M.A. Heine, J.M. Popplewell, and C.J. Gaffoglio. Erosion-corrosion resistance of copper alloy c72200 in sea water containing suspended sand. Desalination, 38:223-231, Nov 1981. URL: https://doi.org/10.1016/s0011-9164(00)86069-5, doi:10.1016/s0011-9164(00)86069-5. This article has 6 citations and is from a domain leading peer-reviewed journal.

6. (polan1981erosioncorrosionresistanceof pages 1-3): N.W. Polan, M.A. Heine, J.M. Popplewell, and C.J. Gaffoglio. Erosion-corrosion resistance of copper alloy c72200 in sea water containing suspended sand. Desalination, 38:223-231, Nov 1981. URL: https://doi.org/10.1016/s0011-9164(00)86069-5, doi:10.1016/s0011-9164(00)86069-5. This article has 6 citations and is from a domain leading peer-reviewed journal.

7. (lewis1981evaluationofcoppernickel media 6b86b115): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

8. (king1992thehotisostatic pages 43-49): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

9. (king1992thehotisostatic pages 49-55): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

10. (king1992thehotisostatic pages 304-311): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

11. (holsberg1970weldabilitystudiesof pages 1-2): PW HOLSBERG. Weldability studies of modified 70-30 cuni alloys. Unknown journal, 1970.

12. (holsberg1970weldabilitystudiesof pages 3-4): PW HOLSBERG. Weldability studies of modified 70-30 cuni alloys. Unknown journal, 1970.

13. (holsberg1970weldabilitystudiesof pages 4-5): PW HOLSBERG. Weldability studies of modified 70-30 cuni alloys. Unknown journal, 1970.

14. (holsberg1970weldabilitystudiesof pages 5-5): PW HOLSBERG. Weldability studies of modified 70-30 cuni alloys. Unknown journal, 1970.

15. (king1992thehotisostaticb pages 304-311): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

16. (nemani2024advancementsinadditive pages 26-28): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

17. (polan1981erosioncorrosionresistanceof pages 6-9): N.W. Polan, M.A. Heine, J.M. Popplewell, and C.J. Gaffoglio. Erosion-corrosion resistance of copper alloy c72200 in sea water containing suspended sand. Desalination, 38:223-231, Nov 1981. URL: https://doi.org/10.1016/s0011-9164(00)86069-5, doi:10.1016/s0011-9164(00)86069-5. This article has 6 citations and is from a domain leading peer-reviewed journal.

18. (holsberg1970weldabilitystudiesof pages 2-3): PW HOLSBERG. Weldability studies of modified 70-30 cuni alloys. Unknown journal, 1970.

19. (nemani2024advancementsinadditive pages 18-21): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

20. (nemani2024advancementsinadditive pages 21-26): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

21. (king1992thehotisostatic pages 60-67): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.
