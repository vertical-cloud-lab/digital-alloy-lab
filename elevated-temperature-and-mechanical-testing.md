# Elevated-temperature testing, tests beyond tensile, and strain rate, with a focus on aluminum

*Issue [#254](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/254), second round, 2026-11-28.
The first round, on cryogenic testing, is [`cryogenic-testing-aerospace-alloys.md`](cryogenic-testing-aerospace-alloys.md).*

**Sources.**

- **Edison.** Nine Edison Scientific tasks: four `LITERATURE_HIGH` reviews, three `PRECEDENT` searches and two
  `LITERATURE` questions. All answers and full trajectories are in
  [`edison-trajectories/elevated-temp-and-mechanical-testing/`](edison-trajectories/elevated-temp-and-mechanical-testing/).
  The script is [`scripts/edison_elevated_temp_testing.py`](scripts/edison_elevated_temp_testing.py).
- **Browser.** Headed Chrome sent its traffic out through a lab Raspberry Pi on BYU's network, and xdotool drove
  the mouse and keyboard. It ran 12 Semantic Scholar, 5 NASA NTRS and 3 OSTI searches, and opened 28 papers, records and
  standards pages, including Edison-cited papers whose numbers I checked
  ([search log](edison-trajectories/elevated-temp-and-mechanical-testing/browser-search-log.md)).
- **Web survey.** It covered equipment makers, test labs and industry write-ups, and fetched about 50 pages.

Section 9 says which source each fact came from and where I corrected Edison. Marks used throughout:

- **Pi:** I read it myself in the Pi-tunnelled browser.
- **via Edison NN:** Edison's reading of a source I did not open.
- **survey:** the web survey fetched the page.

## Bottom line

- **Heat does three separate things to aluminum, and a room-temperature tensile bar sees none of them.**
  1. **Strength drops while the part is hot.** For example, LPBF AlSi10Mg's UTS goes from 280 MPa at room
     temperature to 163 MPa at 250 °C and 34 MPa at 450 °C ([Lehmhus et al. 2022](https://doi.org/10.3390/ma15207386), Pi).
  2. **Strength is lost for good after long exposure (overaging), even when the part is measured cold.**
     - **NASA's High-Speed Research (HSR) program:** candidate airframe alloys kept their tensile strength to within
       about 5 % after 30,000 h at 93–107 °C, but lost up to 25 % after 15,000 h at 135 °C. One candidate (RX818)
       was dropped after 5,000 h for poor fracture toughness ([NASA/TP-2004-212988](https://ntrs.nasa.gov/citations/20040047195), Pi).
  3. **Parts creep under steady load.** Creep can fail a part at loads a tensile test calls safe.
     - In an LPBF Al-Ce-Ni-Mn-Zr alloy at 300–400 °C, creep ductility was only 0.2–2.4 %, against 12–21 % in
       tensile tests at the same temperatures ([Rakhmonov et al. 2025](https://doi.org/10.1016/j.addma.2025.104983), Pi).
- **The precedent is Concorde.** Its AU2GN/RR58 (2618A) skin ran at about 120 °C, with local spots up to 150 °C.
  - About 10,000 specimens were tested at 20, 130 and 150 °C, before and after exposure.
  - Five alloys survived a 10,000 h screen, and AU2GN was then taken to 30,000 h.
  - Strength fell by at most about 20 MPa after 30,000 h at 130 °C, and creep strain stayed at or below 0.02 %
    ([*Air & Cosmos*, 1964](https://cap-avenir-concorde.fr/wp-content/uploads/2023/06/1-Air-Cosmos-16-01-1964-Choix-dun-alliage-leger-pour-la-construction-de-Concorde.pdf), survey).
- **Most aluminum alloys are limited to about 120–200 °C, and the familiar AM alloys are no exception.**
  - **7xxx:** η′ overages above about 120–150 °C.
  - **2xxx:** θ′ and S coarsen above about 150–225 °C.
  - **LPBF Al-Mg-Sc-Zr:** UTS falls from 561 MPa to 103 MPa at 200 °C and 54 MPa at 250 °C
    ([Ren et al. 2024](https://doi.org/10.3390/met14080890), Pi).
  - **Alloys that hold up are built on slow-diffusing elements:** high-intermetallic Al-Ce, Al-Ce-Ni-Mn-Zr, Al-Cu-Mn-Zr
    and Al-Fe(-V-Si). ORNL's LPBF Al-9Ce-4Ni-0.5Mn-1Zr keeps a yield strength of about 115 MPa at 398 °C, where
    wrought 2219-T61 is down to about 25 MPa (ORNL/TM-2024/3244, via Edison 02).
- **Data on AM aluminum at temperature are thin, and that matters for this lab.**
  - **Creep data exist** for a handful of LPBF alloys: Al-Ce, Al-Ce-Ni-Mn(-Zr), Al-Cu-Mn-Zr, Al-Mg-Zr, Al-Zr-X and A20X.
  - **No 1,000 h stress-rupture life was found for any Sc-free LPBF alloy.** The 1,000 h results are all unstressed
    aging (Edison 05; Scalmalloy, AlSi10Mg and A20X were outside that search).
  - **Fatigue at temperature is almost absent.** One exception is ORNL's piston alloy, with fatigue strengths of
    115, 100 and 60 MPa at 150, 250 and 350 °C (via Edison 09).
  - **No composition-resolved hot screen was found** (Edison 06, which calls this a search-limited finding).
  - **Sc-lean Al-Mg-Zr, Al-Fe-Zr and Al-Ni-Zr have the least data** (Edison 02).
- **Beyond tensile, fatigue usually decides whether an LPBF aluminum part survives.**
  - **Fatigue** is limited by rough as-built surfaces ("killer notches"), pores and build orientation.
  - **Toughness and corrosion:** fracture toughness, fatigue-crack growth, and stress-corrosion and exfoliation
    tests matter for 2xxx and 7xxx alloys.
  - **Cheap screening tools:** hardness (within ±15–30 % of yield once calibrated), small punch (an 8 mm × 0.5 mm
    disc) and indentation plastometry (a stress-strain curve in minutes, with a hot stage to 800 °C). They save
    powder.
  - **What MMPDS requires:** tensile, compression, shear and bearing data for a new alloy. Elevated-temperature,
    fatigue and toughness data are only "recommended" (survey).
- **Strain rate matters less than temperature for aluminum at room temperature, with three exceptions that apply here.**
  - **The usual case:** most alloys have a small rate sensitivity (m ≈ 0.001–0.02). 2024-T351 shows little change
    in flow stress up to about 5,000 s⁻¹.
  - **Exception 1, ductility:** it often *rises* at high rate. AA6016's elongation went up 75–105 % at 500 s⁻¹, and
    Scalmalloy's failure strain rose at 1,000 s⁻¹.
  - **Exception 2, Al-Mg alloys:** they show negative rate sensitivity and serrated (Portevin-Le Chatelier) flow
    at ordinary test rates. This covers Scalmalloy and the Al-Mg-Zr family.
  - **Exception 3, heat:** rate sensitivity grows sharply at temperature.
    - AA6061's yield strength at 250 °C ranged from 192 to 220 MPa over two decades of rate.
    - LPBF AlSi12 went from negative rate sensitivity at room temperature to positive at 200 °C.
    - LPBF AlSi10Mg fatigued at 350 °C lasted longer at 20 kHz than at 20 Hz.

  So every tensile result, and above all every hot one, needs its strain rate and control method stated.
- **What it could mean for the lab (section 8):**
  1. Fix and report the strain rate now (ISO 6892-1 Method A).
  2. Add one strain-rate jump per alloy.
  3. Add hot tensile tests at 150–300 °C, and room-temperature tests after 100 h and 1,000 h of exposure.
  4. Screen compositions with hardness, indentation plastometry or small punch.
  5. Send fatigue, creep and Hopkinson-bar work to partners.

## 1. Why elevated-temperature testing matters

### 1.1 Where aerospace aluminum gets hot

| Location | Temperature | What is tested | Source |
|---|---:|---|---|
| Concorde skin (Mach 2.0–2.2 cruise) | about 120 °C, local spots up to 150 °C, and an equilibrium of about 130 °C at Mach 2.2 (300 °C at Mach 3) (*Air & Cosmos*); a maximum of about 130 °C at Mach 2.05 (Hénaff) | Hot and post-exposure tensile, creep, fatigue; 10,000 to 30,000 h exposures | *Air & Cosmos* 1964 (survey †); [Hénaff et al.](https://doi.org/10.5772/15153) (via Edison 09) |
| NASA HSCT (Mach 2.4 study) | 93–135 °C (200–275 °F) | 30,000 h exposures, hot tensile, creep, toughness. The 60,000 h life was a *goal*, not a test length | [NASA/TP-2004-212988](https://ntrs.nasa.gov/citations/20040047195) (Pi); NASA CR-4517 (via Edison 09) |
| Aluminum under a thermal-protection system (Shuttle, hypersonic concepts) | kept at or below about 175 °C (350 °F) | Hot strength of the structure under the tiles | [Tenney et al. 1989](https://doi.org/10.2514/3.45868) (via Edison 01, 09) |
| Turbocharger and small-engine compressor wheels (2618A) | up to about 230 °C in service | Fatigue at room temperature and 230 °C; creep and fatigue after aging | [Fraunhofer IWM](https://iwm.fraunhofer.de/en/services/materials-assessment-lifetime-concepts/highlights/aging-lifetime-radial-compressor-wheels.html); [Sheffield thesis](https://etheses.whiterose.ac.uk/12861/) (survey) |
| Brackets, ducts and heat exchangers near engines, APUs, nacelles | installation-specific | Needs a measured *part-metal* temperature; hot zones go to titanium, steel or nickel | Edison 01, 09; [Boyer et al. 2015](https://doi.org/10.1557/mrs.2015.278) |
| Fire | transient, far above service limits | Prescribed heat-flux histories, not one temperature | Edison 01 |

### 1.2 What a room-temperature test misses

1. **Strength at temperature.** It falls steeply once precipitates start to coarsen or dissolve. Elongation usually
   rises at the same time, so a hot tensile curve looks ductile while carrying a fraction of the load (Ren 2024:
   72 % elongation at 250 °C).
2. **Strength after exposure.** This is measured back at room temperature after hours to tens of thousands of hours
   hot. It is a different property from hot strength, and MMPDS plots it on separate "effect of exposure" curves.
   - **NASA HSR:** C415, C416 and ML377 (Al-Cu-Mg-Ag and Al-Cu-Li-Mg-Ag) beat the Concorde alloy CM001 and the
     Tu-144-derived 1143 by at least 20 % in yield strength (Pi).
   - **Concorde:** 15,000 cycles of 2 h holds did the same damage as 30,000 h of continuous heating (*Air & Cosmos*,
     survey †).
3. **Creep and stress rupture.**
   - **Concorde:** the design held permanent strain to 0.1 % over the life of the aircraft (via Edison 01).
   - **2519-T87 at 135 °C:** creep-brittle. Cracks grew under sustained K, with only 1.2–2.0 % creep strain to
     failure ([ASTM STP 1297, OSTI 624244](https://www.osti.gov/biblio/624244), survey).
   - **LPBF:** creep ductility can be ten times lower than tensile ductility (Rakhmonov 2025, Pi).
4. **Fatigue at temperature, thermomechanical fatigue and creep-fatigue.** Hold times at peak temperature cut life
   in ways that separate fatigue and creep tests don't predict (ASTM E2714, E2368; Edison 01).
   - Test frequency is itself a rate variable at temperature. LPBF AlSi10Mg at 350 °C had a fatigue strength of
     30 MPa at 10⁷ cycles and 20 Hz. That is 0.73 of its UTS at that temperature. At 20 kHz it lasted longer,
     because it strain-rate hardens ([Bahl et al. 2025](https://doi.org/10.1016/j.actamat.2025.121866), Pi).
5. **Dynamic strain aging.** Al-Mg alloys show serrated flow and negative rate sensitivity in particular windows of
   temperature and rate; Al 3004 did so from −20 to 180 °C at 5.6 × 10⁻⁵ to 5.6 × 10⁻³ s⁻¹ (via Edison 01). See §4.3.

### 1.3 How design data handle temperature

- **MMPDS gives two kinds of curve** (Edison 01; MMPDS presentation, survey):
  - "effect of temperature": the property at temperature as a fraction of the room-temperature value;
  - "effect of exposure": the room-temperature property after a soak, from about 0.5 h to 10,000 h.
- **Example:** after 100 h at 150 °C, 2024-T351 keeps 96 % of its tensile strength and 93 % of its yield strength.
  6061-T6 keeps 100 % (MMPDS-01 values quoted in a [LIGO bake-out note](https://dcc-llo.ligo.org/public/0021/T1000564/001/T1000564-v1%20bake%20temperatures%20for%20aluminum%20alloys.pdf), survey †).
- **For a new alloy,** MMPDS requires tensile, compression, shear and bearing data. Elevated-temperature, fatigue
  and toughness tests are only "recommended" ([MMPDS AeroMat 2007 presentation](https://www.mmpds.org/wp-content/uploads/2015/03/mmpds_2015_2007aeromat_presentation.pdf), survey †).
- **Long lives are extrapolated** from shorter tests with three relations. All three are sensitive to their
  fitted constants (Edison 01):
  - the Larson-Miller parameter, P = T(C + log t), with C usually near 20;
  - Monkman-Grant, which predicts rupture time from the minimum creep rate;
  - the Wilshire equations, which normalize stress by the UTS at temperature.

### 1.4 Standards

| Standard | Scope |
|---|---|
| ASTM E21; ISO 6892-2 | Tensile testing at elevated temperature. Control gauge temperature (a classic practice held ±2.8 °C), soak before loading, measure strain on the specimen |
| ASTM E139; ISO 204 | Creep, creep-rupture and stress-rupture |
| ASTM E328 | Stress relaxation (bolt preload, interference fits) |
| ASTM E606 | Strain-controlled (low-cycle) fatigue |
| ASTM E2368 | Thermomechanical fatigue (temperature and strain cycled together, in or out of phase) |
| ASTM E2714 | Creep-fatigue (cycling with holds) |
| ASTM E1457 | Creep-crack growth |
| ASTM E466, E647, E399/E1820 at temperature | High-cycle fatigue, crack growth and toughness, run in a furnace |

## 2. Aluminum at elevated temperature

### 2.1 Why aluminum alloys soften, and what slows it

| Strengthening phase | Alloys | What happens hot | Practical limit (approximate) |
|---|---|---|---|
| η′ (MgZn₂) | 7075, 7050 | Coarsens and dissolves | about 120–150 °C |
| S (Al₂CuMg); Fe-Ni intermetallics | 2024; 2618/2618A | Coarsens; Fe-Ni phases help 2618 but don't stop overaging | about 150–200 °C |
| θ′ (Al₂Cu) | 2219, 2014, 2519 | Coarsens above about 225 °C, then turns into incoherent θ | about 200–250 °C |
| Ω (with Ag and Mg) | 2039/2139, A20X/A205 | More stable than θ′, still overages | about 200–250 °C |
| θ′ stabilized by Mn and Zr | ACMZ (Al-Cu-Mn-Zr) | No measurable θ′ coarsening after 5,000 h at 300 °C (cast) | about 300–350 °C |
| L1₂ Al₃(Sc,Zr) | Scalmalloy and other Al-Mg-Sc-Zr | Precipitates resist coarsening, but the Mg-strengthened matrix softens; coarsening is measurable near 325 °C | precipitates stable to about 300 °C, but most of the strength is gone by 250 °C |
| Al₁₁Ce₃ eutectic | Al-Ce, Al-Ce-Mg | Ce barely dissolves or diffuses in Al; cast alloys keep more than 60 % of their yield strength at 300 °C | about 300–400 °C, pending creep data |
| Al₁₂(Fe,V)₃Si dispersoids | 8009 (FVS0812, powder metallurgy) | Creep threshold stresses of 112, 95, 70 and 55 MPa at 300, 350, 400 and 450 °C; sheet unchanged after 504 h at 400 °C | about 400–450 °C |
| Al₃Ni, Al-Ce-Ni eutectic, plus Al₃Zr | Al-Ce-Ni-Mn(-Zr), "DuAlumin-3D" | Thermally stable intermetallic skeleton | about 300–400 °C |

From Edison 02 (Bahl et al. 2021, [10.1016/j.matdes.2020.109378](https://doi.org/10.1016/j.matdes.2020.109378); Peng et al. 1999,
[10.1016/S0921-5093(98)00876-4](https://doi.org/10.1016/S0921-5093(98)00876-4); Sims et al. 2017, [10.1039/C7MH00391A](https://doi.org/10.1039/C7MH00391A);
Michi et al. 2022, [10.1080/09506608.2021.1951580](https://doi.org/10.1080/09506608.2021.1951580)). The limits are rules of thumb that depend on exposure time and stress,
not allowables.

### 2.2 Wrought and conventional alloys

| Alloy | Data | Source |
|---|---|---|
| AU2GN / RR58 / CM001 (2618A), Concorde | At most about 20 MPa strength loss and ≤ 0.02 % creep after 30,000 h at 130 °C | *Air & Cosmos* 1964 (survey †) |
| C415, C416, ML377 (HSR candidates) | ≤ 5 % tensile loss after 30,000 h at 93–107 °C; up to 25 % after 15,000 h at 135 °C. NASA set their upper service range at 93–107 °C | NASA/TP-2004-212988 (Pi; detail via Edison 09) |
| 2219-T61 | Yield about 275, 255, 230, 55 and 25 MPa at room temperature, 93, 204, 343 and 398 °C (read from the report's figures) | ORNL/TM-2024/3244, [OSTI 2301648](https://www.osti.gov/biblio/2301648) (record Pi; numbers via Edison 02) |
| 2618 and 8009 (FVS0812) | Both alloys soften after only 1–5 % uniform strain at temperature, which neither Ramberg-Osgood nor Bodner-Partom captures | [Leng, Porr & Gangloff 1990](https://doi.org/10.1016/0956-716X(90)90504-A), [NTRS 19910029640](https://ntrs.nasa.gov/citations/19910029640) (Pi) |
| 2519-T87 | Creep-brittle at 135 °C | OSTI 624244 (survey) |
| 2618A compressor wheels | 2618A is "virtually the only material"; Al₂CuMg coarsens in service. Fatigue at 230 °C; ignoring flat intergranular regions overestimated life about tenfold | Fraunhofer IWM; Sheffield thesis (survey) |

Edison did not recover MMPDS temperature tables for 2024, 2014, 6061, 7050 or 7075. They are in MMPDS, which is not
freely distributed.

### 2.3 Additively manufactured aluminum at temperature

| Alloy (LPBF unless noted; condition) | Test | Result | Source |
|---|---|---|---|
| AlSi10Mg, stress-relieved 350 °C / 2 h, vertical | Hot tensile | UTS 280.2, 162.8 and 34.4 MPa at room temperature, 250 and 450 °C; elongation 6.4, 15.6 and 26.5 % | [Lehmhus et al. 2022](https://doi.org/10.3390/ma15207386) (Pi) |
| AlSi10Mg, as built | Hot tensile after 30 min holds | YS about 300 MPa at room temperature, little change below 200 °C, about 25 MPa at 400 °C as Si coarsens | [Cao et al. 2020](https://doi.org/10.1016/j.jmst.2020.04.066) (Pi abstract) |
| AlSi10Mg | Fatigue at 350 °C | 30 MPa at 10⁷ cycles at 20 Hz; longer lives at 20 kHz | [Bahl et al. 2025](https://doi.org/10.1016/j.actamat.2025.121866) (Pi) |
| Al-Mg-Sc-Zr, 350 °C / 4 h | Hot tensile | UTS and elongation: 560.6 MPa and 11.1 % at room temperature; 435.1 and 25.8 at 100 °C; 269.4 and 20.1 at 150 °C; 102.8 and 47.9 at 200 °C; 54.0 and 72.2 at 250 °C | [Ren et al. 2024](https://doi.org/10.3390/met14080890) (Pi) |
| Scalmalloy, aged | Yield | 468–493 MPa at room temperature after 325 °C / 4 h ([Cerri et al.](https://doi.org/10.3390/cryst15010025)); about 60 MPa at 300 °C, read from the Michi et al. 2022 review's figure | via Edison 02 |
| Al-10Ce-8Mn | Hot tensile to 400 °C; after 200 h at 400 °C | Strength retention up to 400 °C better than wrought and AM benchmarks | [Plotkowski et al. 2020](https://doi.org/10.1016/j.actamat.2020.07.014) (Pi abstract) |
| Al-11Ce-7Mg, Al-15Ce-9Mg | Hot tensile | Higher yield than AlSi10Mg up to 350 °C, better retention than Scalmalloy | [Sisco et al. 2021](https://doi.org/10.1038/s41598-021-86370-4) (via Edison 02) |
| Al-9Ce-4Ni-0.5Mn-1Zr ("DuAlumin-3D"), 350 °C / 8 h | Hot tensile, two orientations | Yield about 350, 300, 240, 170 and 115 MPa at room temperature, 93, 204, 343 and 398 °C; beat 2219-T61 throughout | ORNL/TM-2024/3244 (record Pi; numbers via Edison 02) |
| Same alloy, automotive-piston project | Fully reversed fatigue at 50 Hz, 10⁷ runout | 115, 100 and 60 MPa at 150, 250 and 350 °C; tensile tests to 350 °C at 5 × 10⁻⁴ s⁻¹ | DOE report [10.2172/2573209](https://doi.org/10.2172/2573209) (record Pi; numbers via Edison 09) |
| Al-Ce-Ni-Mn | Creep, 300–400 °C | Threshold stresses of 16–28 MPa, about 40–50 % below PM 8009 at the same creep rate | [Michi et al. 2022](https://doi.org/10.1016/j.actamat.2022.117699) (via Edison 02) |
| Al-7.5Ce-4.5Ni-0.4Mn-0.7Zr, peak-aged and overaged | Tensile creep, 300–400 °C | Creep ductility 0.2–2.4 %, against 12–21 % in tensile tests; cavities start in denuded zones at melt-pool and grain boundaries | [Rakhmonov et al. 2025](https://doi.org/10.1016/j.addma.2025.104983) (Pi) |
| Al-8.6Cu-0.5Mn-0.9Zr (ACMZ) | Hot tensile and creep at 300 °C | YS 121 ± 2 MPa as built, 53 ± 1 MPa after 400 °C / 200 h. Stress for a minimum creep rate of 10⁻⁷ s⁻¹: 56 MPa as built, 30 MPa after the heat treatment | [Michi et al. 2023](https://doi.org/10.1016/j.actamat.2022.118557) (via Edison 02, 05) |
| Al-10Ce | Stress rupture | 92 h at 325 °C / 21 MPa; 18 h at 350 °C / 21 MPa; stopped unbroken after more than 765 h at 300 °C / 21 MPa | Stinehart 2023 thesis (via Edison 05) |
| A20X (A205), solutionized and aged | Creep at 200 °C | Minimum creep rates of 10⁻⁸ to 10⁻⁶ s⁻¹ at 120–180 MPa. A small cantilever bending test gave the same rates as uniaxial creep | [Kulkarni et al. 2023](https://doi.org/10.1016/j.addlet.2023.100142) (abstract via OpenAlex) |
| Al-3.6Mg-1.2Zr, Al-2.9Mg-2.1Zr (Sc-free) | Compressive creep at 260 °C | Threshold stress about 40 MPa as built and 14 MPa after aging in 8 h tests; converged by 168 h | [Griffiths et al. 2020](https://doi.org/10.1016/j.actamat.2020.02.008) (via Edison 05) |
| Al-0.4Zr-1X (at. %), X = Mn, Cr, V, Mo, W | Compressive creep at 400 °C; aging up to 2,016 h at 400 °C | Every ternary alloy crept less than Al-0.4Zr; V, Mo and W stayed in solution after 2,016 h | [Senvardarli, Dunand et al. 2026](https://doi.org/10.1016/j.addma.2026.105145) (Pi) |
| Al-5Mn-0.8Cr-0.6Zr | 1,000 h at 350 °C, unstressed | Hardness fell 13 % | [Mehta et al. 2023](https://doi.org/10.1016/j.jallcom.2023.171685) (via Edison 05) |
| Al-15Fe | 1,000 h at 300 °C, unstressed | Nanoscale α-Al/Al₆Fe cells dissolved, Al₁₃Fe₄ formed, hardness fell moderately | [Wang et al. 2022](https://doi.org/10.3390/ma15134497) (Pi) |
| Al-La-Sc-Zr | Hot tensile | YS 418 MPa at room temperature, about 246 MPa at 300 °C | [Ma et al. 2025](https://doi.org/10.1038/s41467-025-66441-0) (via Edison 02) |

### 2.4 Gaps that matter for this lab

1. **No stress-rupture life of 1,000 h or more was found for any Sc-free LPBF aluminum alloy.** The 1,000–2,016 h
   results are unstressed aging, not creep lives (Edison 05). Edison's search didn't cover Scalmalloy, AlSi10Mg or A20X.
2. **Fatigue at temperature is almost absent.** Exceptions: ORNL's piston alloy at 150–350 °C (via Edison 09), and
   AlSi10Mg at 350 °C (Pi). Creep-fatigue data are scarce (Edison 02). I found no thermomechanical-fatigue data for
   LPBF aluminum, but didn't search for it specifically.
3. **Sc-lean and rare-earth-lean alloys have the least data.** Al-Mg-Zr (Addalloy-type), Al-Fe-Zr, Al-Ni-Zr and
   lean Al-Mn-Sc lack creep maps, hot fatigue and long-exposure property data (Edison 02).
4. **No composition-resolved hot screen.** Hot indentation, bending creep and parallel small-punch creep have each
   been done on aluminum. Edison found no study running them across a graded or combinatorial AM aluminum library, and
   calls that a search-limited finding (Edison 06).
5. **Commercial AM grades** (Constellium Aheadd, HRL 7A77) publish little or no elevated-temperature data. HRL's
   7A77 datasheet is room-temperature only (survey).

## 3. Mechanical tests beyond the tensile test

### 3.1 What each test adds

| Test | Standard | What it shows that tensile doesn't | Specimen, material, time | For LPBF aluminum |
|---|---|---|---|---|
| Plane-strain fracture toughness | ASTM E399 (Al practice B645, B646) | Resistance to a sharp crack (K_Ic) | Fatigue-precracked C(T) or SE(B). Validity can demand thick specimens: 18–38 mm for a low-yield cast Al (A413) | Needed for damage-tolerant parts; depends on orientation and defects |
| Elastic-plastic toughness, R-curve | ASTM E1820 (J, CTOD), E561 | Toughness when K_Ic validity is impractical; stable tearing | Precracked; more complex | Usual route for tough Al |
| Kahn tear | ASTM B871 (withdrawn 2017, no replacement) | Tear initiation and propagation energy of sheet | 35 × 60 mm × thickness, no precrack, cheap | Low-cost toughness ranking of thin sections |
| High-cycle fatigue | ASTM E466 | S-N curve, endurance limit; sensitivity to surface and defects | 15–30 specimens per curve; days to weeks | Usually the limiting property (§3.2) |
| Low-cycle fatigue | ASTM E606 | Cyclic hardening or softening, strain-life | Extensometer, about 10⁻³ s⁻¹ | Thermally cycled parts |
| Very-high-cycle fatigue | Ultrasonic, 20 kHz | Life to 10⁹ cycles in about 14 h (579 days at 20 Hz, Edison 08); internal initiation | Small resonant specimens; watch self-heating and rate effects (Edison 08) | Pores inside LPBF parts |
| Fatigue-crack growth | ASTM E647 | da/dN versus ΔK, threshold | C(T) or M(T); weeks | Damage tolerance |
| Charpy impact | ASTM E23 | Absorbed energy; brittle transition in steels | 10 × 10 × 55 mm | Discriminates poorly for Al, which has no ductile-to-brittle transition (Edison 03, moderate support) |
| Notched tension | ASTM E602 | Notch-strength ratio, notch sensitivity | Notched round bar | Cheap check relevant to rough surfaces |
| Compression | ASTM E9 | Compressive yield; tension-compression asymmetry | Short cylinders; minutes | Required by MMPDS (survey); separates anisotropy from inhomogeneity |
| Shear, bearing | ASTM B769, B565; E238 | Shear strength (about 55–65 % of UTS); bearing strength (about 1.5–2 × UTS) | Small plates and pins | Required by MMPDS (survey); fastened joints |
| Hardness | ASTM E18, E92, E384, E10 | Fast proxy for yield: σ_y ≈ 0.383 HV − 101.5 for Al-Mg-Si (R² 0.94); within ±15–30 % once calibrated | Seconds per indent | Screening and mapping; calibrate per alloy family |
| Nanoindentation | ISO 14577 | Local hardness and modulus, maps; vendors' hot stages go to 800–1,000 °C (survey), though one 800 °C stage was used only to 500 °C (Edison 08) | Hundreds to thousands of indents; about 0.2 s each in fast modes | Composition gradients; size effects and pile-up need care |
| Stress corrosion, exfoliation | ASTM G47, G139; G34 | Environment-assisted cracking; layered corrosion | 20–30 days (G47); 48–96 h (G34) | Needed for 2xxx and 7xxx. G47 and G139 may not rank close tempers |
| Residual stress | XRD, hole drilling (E837), contour, neutron diffraction | Built-in surface tension that speeds crack initiation | — | High in as-built LPBF |
| Small punch | ASTM E3205 | Estimates of yield and UTS; creep (small-punch creep, Edison 06) | 8 mm × 0.5 mm disc, about 25 mm³ | Many compositions from one build |
| Profilometry-based indentation plastometry (PIP) | Plastometrex | A full stress-strain curve from one spherical indent and an inverse finite-element fit | Minutes; probes about 1 mm across | Screening and maps; hot stage to 800 °C |
| Micropillar compression | — | Flow of a single grain or phase | Hours of FIB milling per pillar | Mechanisms, not engineering data |
| Bending creep with DIC | — | Tension and compression creep at several stresses from one beam | Small beams | For LPBF A20X at 200 °C, rates matched uniaxial creep below 170 MPa and were within a factor of two above it; an AlSi10Mg result at 250 °C is reported second-hand (Edison 06) |

From Edison 03 unless marked. ASTM B871's withdrawal is from the survey and the Pi browser; Edison 03 presents B871 as current.

### 3.2 Why fatigue, not tensile strength, limits LPBF aluminum

- **Surface.** As-built roughness (Ra about 1.5–25 µm, depending on orientation and layer height) gives "killer
  notches". X-ray CT before and after testing matched each fatigue crack to the surface notch it started from
  ([du Plessis et al. 2020](https://doi.org/10.1016/j.addma.2020.101424), Pi).
  - **LPBF Al2024-RAM2:** as-built fatigue limits at 2 × 10⁶ cycles were 109–118 MPa. Grinding to Ra 0.6 µm raised
    the limit to 200 MPa (via Edison 03).
- **Pores.** Their size and position matter more than total porosity. HIP closes them, but it coarsens Si in
  AlSi10Mg (Edison 03).
- **Orientation.** For LPBF AlSi10Mg, horizontal yield was 307 ± 11 MPa and vertical 210 ± 8 MPa. The difference was
  traced to lack-of-fusion defects ([Kan et al. 2019](https://doi.org/10.1016/j.addma.2019.100805), via Edison 04).
- **The underlying reason:** a tensile test averages over the gauge, while fatigue fails at the worst flaw in the
  stressed volume. NASA-STD-6030 and MSFC-STD-3716 therefore require fatigue and fracture tests on witness specimens
  from production builds, not only tensile tests (via Edison 03).

### 3.3 Qualification numbers

- **A-basis** is the value that 99 % of the population exceeds with 95 % confidence. **B-basis** is 90 % with 95 %
  confidence (via Edison 03).
- **Data needed:** the full MMPDS route uses about 100 observations from 10 or more lots. Reduced B-basis plans start
  from about 20 samples from 3 heats (via Edison 03).
- **AM:** process variability makes the full route costly, which is why NASA is working on statistically updated,
  process-control-based approaches (via Edison 03).
- **AMS 7003** is SAE's specification for the LPBF process. Edison 03 called it a wire-feed specification, which is
  wrong (see §9).

## 4. Tensile tests at other settings: strain rate and the rest

### 4.1 Quasi-static rate and how it is controlled

- **ASTM E8/E8M and B557.** The usual rate is 0.015 ± 0.006 /min (about 2.5 × 10⁻⁴ s⁻¹) through yield. After yield it
  may rise to 0.05–0.5 /min (about 10⁻³–10⁻² s⁻¹).
- **ISO 6892-1 Method A** is strain-rate control. It recommends 0.00025 s⁻¹ through the proof strength and
  0.0067 s⁻¹ for tensile strength and elongation, each ±20 %.
  - **Method A1** closes the loop on the extensometer and needs no pre-tests. ZwickRoell
    ([page](https://www.zwickroell.com/industries/metals/metals-standards/tensile-test-iso-6892-1/)) confirms the
    0.00025 s⁻¹ value, the ±20 % tolerance and how A1 works.
  - **Method A2** presets a crosshead speed, which needs the machine's stiffness.
  - **Method B** controls the stress rate instead.
  - Edison 04 repeated my own query's list of four ranges, which included 0.025 s⁻¹; I couldn't confirm that list.
- **Crosshead control does not give a constant specimen strain rate.** Machine compliance, grip slip and
  specimen hardening change the actual rate as the test goes on.
  - With crosshead control, a nominal 0.4 %/s test actually ran at 0.369–0.428 %/s on average, with excursions up to
    0.278 %/s. DIC-based closed-loop control held the nominal rate (via Edison 04).
  - In older steel data, closed-loop extensometer control cut the scatter in yield strength from ±3.0 to ±1.7 ksi
    compared with open-loop machines (via Edison 04).

### 4.2 How big the rate effect is in aluminum

| Material | Rates | Result | Source |
|---|---|---|---|
| AA6061 | 2.5 × 10⁻³, 2.5 × 10⁻² and 2.5 × 10⁻¹ s⁻¹, at room temperature and 250 °C | Yield about 270–272 MPa at room temperature, barely rate-dependent; 192–220 MPa at 250 °C | Ma'at et al. 2019 (via Edison 04) |
| AA6016-T4 / T6 sheet | 10⁻³ against 500 s⁻¹ | Yield +54 % / +38 %; UTS +13–14 %; elongation +75 % / +105 % | [Ubertalli et al. 2020](https://doi.org/10.3390/met10020242) (via Edison 04) |
| AA5754, AA5182 sheet | 600–1,500 s⁻¹ against 3.3 × 10⁻³ s⁻¹ | Flow stress changed little; failure elongation rose markedly at high rate | [Smerd et al. 2005](https://doi.org/10.1016/j.ijimpeng.2005.04.013) (via Edison 04, 09) |
| AA5082, AA5182 | 10⁻⁴ to 10³ s⁻¹ | Negative rate sensitivity and serrated flow from 10⁻⁴ to 10⁻¹ s⁻¹; AA5182 turns positive near 100 s⁻¹ | [Yamada et al. 2018](https://doi.org/10.3390/met8080576) (via Edison 04) |
| 2024-T351 plate | 10⁻⁴ to 10⁴ s⁻¹, −50 to 450 °C | Little change in plastic flow up to about 5,000 s⁻¹; tension, compression and shear curves differ | [Seidt & Gilat 2013](https://doi.org/10.1016/j.ijsolstr.2013.02.006) (via Edison 09) |
| 2024-T351 | Direct-impact Hopkinson bar, about 5 × 10⁴ s⁻¹ | Small rate sensitivity above 10⁴ s⁻¹ | NASA Glenn, [NTRS 20240014937](https://ntrs.nasa.gov/citations/20240014937) (Pi) |
| LPBF AlSi10Mg | 2.8 × 10⁻⁶ to 2.8 × 10⁻¹ s⁻¹ | Rate-sensitive, unlike conventionally made Al: flow stress and hardening exponent change with rate | [Rosenthal et al. 2017](https://doi.org/10.1016/j.msea.2016.11.070) (Pi abstract) |
| LPBF AlSi10Mg, as built | 10⁻² to 10⁻¹ s⁻¹ | Turns to negative rate sensitivity | Salandari-Rabori 2022 thesis (via Edison 04) |
| LPBF Scalmalloy, as built and aged 325 °C / 4 h | 10⁻³ to 1,000 s⁻¹ (servo-hydraulic and split Hopkinson tension) | UTS weakly *negative* with rate; failure strain up at 1,000 s⁻¹ (as built 342.5 MPa and 29.5 %; aged 497.0 MPa and 15.0 %) | [Jakkula et al. 2021](https://doi.org/10.1007/s40870-021-00298-4) (Pi abstract; numbers via Edison 07) |
| LPBF AlSi12 | Split Hopkinson compression: 750 s⁻¹ at room temperature, 1,500 s⁻¹ at 200 °C | Negative rate effect at room temperature, positive at 200 °C | [Ponnusamy et al. 2018](https://doi.org/10.1088/1757-899X/377/1/012167) (via Edison 07) |
| LPBF Al6061, 3.5–5 % porosity | Split Hopkinson compression, 500–1,800 s⁻¹ | Positive rate sensitivity in every heat-treatment state | Yilmaz et al. 2026, [10.1016/j.msea.2025.149574](https://doi.org/10.1016/j.msea.2025.149574) (via Edison 07) |

No test at 100 s⁻¹ or faster was found for LPBF A20X, AlSi7Mg, Al-Ce or Al-Fe-Zr (Edison 07).

### 4.3 Negative rate sensitivity and serrated flow in Al-Mg alloys

- **The mechanism.** Mg atoms diffuse to dislocations held up at obstacles and pin them. At low rates there is time
  for this to happen, so flow becomes jerky (Portevin-Le Chatelier bands) and the alloy gets *weaker* as the rate
  rises. At high rates the Mg can't keep up, and the effect disappears (Edison 04).
- **What it costs.** PLC bands reduce the strain to necking and roughen the surface (Hopperstad et al. 2007, via Edison 04).
- **Why it matters here.** Scalmalloy (Al-4.5Mg-Sc-Zr) and the Sc-lean Al-Mg-Zr family are Al-Mg alloys.
  - **Measured yield and elongation depend on the rate.** For these alloys, both shift with the chosen quasi-static
    rate, and serrations can make the 0.2 % offset ambiguous.
  - **A one-specimen check:** a strain-rate jump test (for example 10⁻⁴ ↔ 10⁻² s⁻¹), or a stress-relaxation hold,
    measures m. The sign of m flags this behavior.

### 4.4 Intermediate and high rates

| Method | Strain rate | Notes |
|---|---|---|
| Ordinary servo-hydraulic frame | up to about 10 s⁻¹ | Above about 50 s⁻¹, actuator and grip inertia and stress waves corrupt the load signal |
| High-speed servo-hydraulic (ISO 26203-2) | about 1–1,000 s⁻¹ | A slack adaptor lets the actuator get up to speed but rings when it engages. Load measured on the specimen or with an elastic bar helps (Bhujangrao et al. 2020, [10.3390/met10070894](https://doi.org/10.3390/met10070894)) |
| Drop tower, "Dropkinson" bar | up to about 600 s⁻¹ | Short pulse; mainly compression |
| Split Hopkinson (Kolsky) bar, in compression, tension or torsion | about 10²–10⁴ s⁻¹ (SwRI states 1–20,000 s⁻¹) | Usually built in-house. Short gauge lengths cut ring-up time; heated versions exist (NIST pulse-heated bar; Sandia/ORNL induction-heated tension bar, 1,030 °C at 860 s⁻¹) |
| Direct-impact Hopkinson bar | about 5 × 10⁴ s⁻¹ | NASA Glenn, with high-speed DIC |
| Taylor impact, plate impact, ballistic | higher | Projectile speed is not specimen strain rate |

**Heating during the test.**

- Above roughly 10² s⁻¹ the test is close to adiabatic, so most of the plastic work turns into heat in the specimen.
  The fraction is usually taken as about 0.9; FAA's 2024-T351 program measured it with infrared imaging (survey).
- Local temperatures in Hopkinson tests of LPBF AlSi10Mg may pass 150 °C (Ghisi et al. 2022, via Edison 04). That is
  enough to start changing the Si network.
- The Scalmalloy authors caution that their data can't separate rate effects from adiabatic heating (via Edison 07).

**Johnson-Cook parameters are fits, not constants.** The model is σ = (A + Bεⁿ)(1 + C ln ε̇*)(1 − T*ᵐ). Published
sets for the same alloy differ widely:

| Alloy | A (MPa) | B (MPa) | n | C | m | Source |
|---|---:|---:|---:|---:|---:|---|
| 2024-T3 | 369 | 684 | 0.73 | 0.0083 | 1.70 | Widely reused set, as compiled by Edison 04 |
| 6061-T6 | 324 | 114 | 0.42 | 0.0028 | 1.34 | same |
| 6061, own calibration (1,000–3,000 s⁻¹, 20–200 °C) | 318 | 395 | 0.74 | 0.012 | 1.77 | [Yadav et al. 2022](https://doi.org/10.1155/2022/3707200) (via Edison 04) |
| 7075-T6 | 546 | 678 | 0.71 | 0.0024 | 1.56 | as compiled by Edison 04 |
| LPBF AlSi10Mg, flat / vertical / horizontal | 179 / 183 / 192 | 735 / 2,160 / 1,045 | 0.56 / 0.77 / 0.65 | 0.017 / 0.014 / 0.004 | not fitted | Ghisi et al. 2022 (via Edison 04) |

FAA found that a Johnson-Cook model calibrated on 0.125 in. 2024-T3 plate mispredicted the ballistic limit of
thinner and thicker plates. It moved to a tabulated model (LS-DYNA MAT_224) that depends on stress state,
temperature and rate (via Edison 09).

### 4.5 The other settings that change a tensile result

| Setting | Effect | Source |
|---|---|---|
| Gauge length and elongation definition | Elongation depends on gauge length; strength doesn't. ISO uses L₀ = 5.65√A₀ and ASTM E8 uses 4D (about 4.5√A₀), so their elongations differ. Fixed A50 and A80 lengths can't be compared with proportional ones. Going from 40 to 90 mm gauge changed strain at fracture by up to 36 % | Edison 04 |
| Sub-size or non-standard specimens | 2024-T3: yield 304 against 290 MPa (4.6 %) between geometries; short and long AA6016 specimens gave overlapping curves | Edison 04 |
| Surface (as built or machined) | At 60 µm layers, as-built Ra was 25 µm; vertical as-built specimens lost 19 % strength and 64 % ductility against flat ones | García-Zapata et al. 2024, [10.3390/ma17153655](https://doi.org/10.3390/ma17153655) (via Edison 04) |
| Build orientation | Horizontal 307 ± 11 MPa against vertical 210 ± 8 MPa yield (AlSi10Mg) | Kan et al. 2019 (via Edison 04) |
| Test temperature and soak | AA6060 shows negligible rate sensitivity below 200 °C but strong positive sensitivity above; ORNL hot tests used 30 min equilibration and about 10⁻⁴ s⁻¹ | Vilamosa et al. 2015 (via Edison 04); Plotkowski 2020 (via Edison 09) |
| Machine stiffness and control loop | Can shift measured yield by up to about 18 MPa under crosshead control | Clinch 1997 (via Edison 04) |
| Strain measurement | Clip-on extensometers average over the gauge; video and DIC give full fields and post-necking strain, within about 2 % of a clip-on when set up well; DIC is the only option at high rate | Edison 04 |

**What to report with every tensile result:**

- the standard and control method (ISO 6892-1 A1, A2 or B; or E8/B557 with the method), and the actual strain rate
  in each segment;
- the strain-measurement method;
- specimen geometry, gauge length and the elongation definition;
- build orientation and surface state;
- temperature, soak time and thermocouple placement for hot tests;
- the heat-treatment and exposure history.

## 5. Equipment, vendors and test labs

The ranges are each vendor's own statements; the survey fetched every page listed (2026-11-28). Instron's pages
returned 403, so none of its claims are included. Nothing found sells small-punch rigs or Kahn tear fixtures off
the shelf.

| Category | Vendor or lab, and page | What it offers | Stated range |
|---|---|---|---|
| Hot tensile: furnaces and extensometers | **MTS** [Model 653 furnaces](https://www.mts.com/in/products/materials/chambers-furnaces/model-653-high-temperature-furnaces) and [air-cooled extensometers](https://www.mts.com/en/products/materials/extensometers/air-cooled-high-temperature-extensometers); **Epsilon Technology** [furnace extensometers](https://www.epsilontech.com/) (3448, 3549, 7650A) | 1–3 zone clamshell furnaces for tension, fatigue and bend (ASTM E21, ISO 6892-2, E606); contact extensometers | 200–1,000 °C (furnace); extensometers to 1,200 °C, 1,600 °C with the high-temperature option |
| Hot tensile: non-contact strain | **ZwickRoell** [laserXtens](https://www.zwickroell.com/en/extensometers/laserxtens) | Measures through a furnace port or window (ISO 6892-2, ASTM E21) | −80 to 1,600 °C (2,000 °C for some models) |
| Creep frames | **ZwickRoell** [Kappa Multistation](https://www.zwickroell.com/en/creep-testing-machines/kappa-multistation); **Applied Test Systems** lever-arm frames ([listing](https://www.plantautomation-technology.com/products/applied-test-systems/lever-arm-test-systems)) | Up to 3 axes at 50 kN for metals (ISO 204, ASTM E139); dead-weight lever-arm creep and rupture | to 1,200 °C with furnaces |
| Thermomechanical simulator | **Dynamic Systems** [Gleeble 3800-GTC](https://www.gleeble.com/products/gleeble-3000-series/gleeble-3800) | Direct-resistance heating; hot tension and compression, stress relaxation, creep; stroke rates 0.001–2,000 mm/s | to 3,000 °C; heating to 10,000 °C/s |
| Thermomechanical fatigue | **MTS** [TMF subsystem](https://www.mts.com/en/products/materials/high-temp-subsystems/thermomechanical-fatigue-tmf-subsystem) | Induction heating with air cooling; ASTM E2368, ISO 12111 templates | to 1,200 °C |
| High rate: servo-hydraulic | **ZwickRoell** [HTM](https://zwickroell.com/en/servohydraulic-testing-machines/high-speed-testing-machine); **Shimadzu** [HITS-TX](https://shimadzu.com/an/products/materials-testing/fatigue-testingimpact-testing/hits-x-series/spec.html) | 25–160 kN, ISO 26203-2 (HTM); 10 kN, 0.0001–20 m/s (HITS-TX) | 12–20 m/s; HTM hot tests "up to 1,000 °C" |
| High rate: Hopkinson bars | **REL Inc.** [split Hopkinson bars](https://www.relinc.com/split-hopkinson-pressure-bar-testing) | Custom bars in compression, tension, torsion and direct impact | not stated |
| Fatigue | **Shimadzu** [USF-2000A](https://www.shimadzu.com/an/products/materials-testing/fatigue-testingimpact-testing/usf-2000a/spec.html) (20 kHz; lists aluminum); **ZwickRoell** [LTM electrodynamic](https://www.zwickroell.com/products/dynamic-and-fatigue-testing-systems/ltm-electrodynamic-testing-machine/); **RUMUL** resonant machines ([user lab](https://www.tu-chemnitz.de/mb/WOT/abteilungen/laborbereiche/technische_ausruestung/ta83_rumul.php.en)) | Ultrasonic, electrodynamic and resonant fatigue | 20 kHz; up to 100–120 Hz; 40–250 Hz |
| Impact | **ZwickRoell** [HIT pendulums](https://www.zwickroell.com/products/products-for-impact-testing/pendulum-impact-testers-for-tests-on-metals) | Instrumented Charpy, ISO 148-1, ASTM E23 | 300–750 J |
| Hot hardness and nanoindentation | **Hegewald & Peschke** [hot hardness](https://www.hegewald-peschke.com/products/detail/hot-hardness-testing-system/); **Bruker** [Hysitron xSol](https://www.bruker.com/products/surface-and-dimensional-analysis/nanomechanical-test-instruments/nanomechanical-upgrade-options/xsol-high-temperature-stage.html); **Micro Materials** [NanoTest Xtreme](https://www.micromaterials.co.uk/); **Alemnis** [in-SEM indenters](https://alemnis.com/) | Vickers in vacuum; heated nanoindentation; in-SEM tests with high-temperature and high-rate modules | 300–1,500 °C; to 800 °C; −40 to 1,000 °C |
| Indentation plastometry | **Plastometrex** [PLX-Benchtop](https://www.plastometrex.com/) and [PLX-HotStage](https://www.plastometrex.com/products/plx-hotstage) | Stress-strain curves "in just a few minutes" from small or irregular samples; property maps | HotStage to 800 °C |
| Commercial labs | **Westmoreland (WMT&R)** [creep](https://www.wmtr.com/en.creep.html) and [tensile](https://www.wmtr.com/en.tensile-testing.html); **Metcut** [metallic testing](https://metcut.com/metallic-mechanical-testing/); **Element** [creep and rupture](https://www.element.com/materials-testing-services/stress-rupture-and-creep-testing) | ASTM E21, E139, E606, E399/E1820, E647, E1457. WMT&R has capacity for 500 creep machines; Metcut has 146 creep and rupture frames | room temperature to about 1,200 °C |
| High-rate labs | **Southwest Research Institute** [High-Rate Test Laboratory](https://Swri.org/node/8663951); **Ohio State** [Dynamic Mechanics of Materials Lab](https://mae.osu.edu/dmml/materials) | Hopkinson bars in tension, compression and torsion, including hot; OSU's tension bar has tested 2024-T351 | 1–20,000 s⁻¹ (SwRI) |
| Government | **NASA Glenn** (hot tensile, creep, low-cycle fatigue and crack growth; Hopkinson bars); **NIST** (pulse-heated Kolsky bar, [6061-T6 dataset](https://www.nist.gov/node/1619051)); **Sandia/ORNL** (heated Kolsky tension bar, [OSTI 1319194](https://www.osti.gov/biblio/1319194)); **ORNL** [creep laboratory](https://www.ornl.gov/capabilities/creep-laboratory/) (more than 200 frames); **Argonne** (nine lever-arm creep frames run concurrently) | — | — |

**Throughput.** It means running creep tests side by side; nothing makes an individual creep test faster.

- **Concurrent frames:** Argonne loaded nine lever-arm frames at once (via Edison 08).
- **Specimens in series:** a single frame carrying four miniature specimens of different cross-section gave four
  stresses in about the time of the slowest test (316L at 650 °C; via Edison 06, 08).
- **Parallel small-punch creep:** four discs ran at once in one furnace on an Al-Al₂O₃ composite at 300–400 °C
  ([Krizik et al. 2024](https://doi.org/10.1007/s10853-024-10139-z), Pi).

## 6. Documented industry use

- **Concorde (1960s).** Sud Aviation explained its choice of AU2GN in *Air & Cosmos* (survey †):
  - the screen was 10,000 h of exposure, then 30,000 h for AU2GN;
  - about 10,000 specimens were tested at 20, 130 and 150 °C.

  CM001, the RR58 variant, was tuned for creep, durability and toughness; NASA lists 2618 as the US equivalent
  (NASA/TP-2004-212988). The design life was 7,000 flights or 15,000 h (Hénaff et al., via Edison 09).
- **NASA High-Speed Research (1990s).** The program aimed ingot 2xxx and 6xxx alloys at Mach 2.0 and
  powder-metallurgy alloys at Mach 2.4 ([NASA/CR-1997-206248](https://ntrs.nasa.gov/citations/19980013930), survey).
  - **Tensile campaign:** exposures to 30,000 h at 93, 107 and 135 °C; tests at −54 °C, room temperature, 93, 107 and
    135 °C (NASA/TP-2004-212988, Pi).
  - **Companion work:** creep tests (Taminger et al. 1998) and a parallel toughness study, which dropped RX818.
- **Supersonic successors.** Later damage-tolerance work on 2650-T6 for a supersonic skin tested exposures of 30,000 h at 100 and
  130 °C and 20,000 h at 175 °C, then creep, fatigue and creep-fatigue crack growth on compact-tension specimens
  (Hénaff et al., [10.5772/15153](https://doi.org/10.5772/15153), via Edison 09).
- **Compressor wheels.** Turbocharger 2618A wheels coarsen in service, which motivated aging-dependent fatigue and
  creep tests (Fraunhofer IWM, survey).
- **Printed high-temperature aluminum, engine-adjacent.** None of the three below is a certified allowable:
  - **ORNL with industry:** an LPBF Al-Ce-Ni-Mn-Zr alloy for pistons, with hot tensile tests and 150–350 °C fatigue
    (DOE report 10.2172/2573209).
  - **NASA RAMFIRE:** an Elementum 3D A6061-RAM2 rocket nozzle made by directed-energy deposition. It ran 22 starts
    and about 579 s ([NTRS 20240000197](https://ntrs.nasa.gov/citations/20240000197), survey).
  - **Conflux:** an AlSi10Mg heat exchanger ([EOS case study](https://www.eos.info/industries/customer-success-stories/conflux-heat-exchanger-produced-with-additive-manufacturing), survey).
- **Engine debris and fan-blade containment (FAA and NASA).**
  - **New constants from Hopkinson bars:** they gave Johnson-Cook constants for 2024-T3 and Ti-6Al-4V
    ([DOT/FAA/AR-00/25](https://rosap.ntl.bts.gov/view/dot/93874), survey).
  - **Ballistic tests on 2024 panels:** NASA Glenn checked whether coupon-calibrated failure models transfer
    ([NASA/TM-2012-217625](https://ntrs.nasa.gov/citations/20120013210)).
  - **2024-T351 calibration:** later FAA work tested miniature specimens from 10⁻⁴ to 6,000 s⁻¹ with high-speed DIC
    and infrared imaging ([DOT/FAA/TC-19/41 P2](https://rosap.ntl.bts.gov/view/dot/63526), survey).
  - **Certification:** fan-blade-off containment (14 CFR 33.94) needs an engine test, with analysis only as a
    supplement (via Edison 09).
- **Automotive crash.** Folding zones reach roughly 500 s⁻¹. Crash work on AA5754 and AA5182 showed that a crash
  model needs ductility data at rate, not only yield stress (Smerd et al. 2005, via Edison 04, 09).

## 7. Representative links

| Category | Link | Why |
|---|---|---|
| Edison-cited review | [Michi et al. 2022, *Int. Mater. Rev.*](https://doi.org/10.1080/09506608.2021.1951580) | AM aluminum for 200–450 °C; high-temperature testing "severely deficient" |
| Documented long-exposure program | [NASA/TP-2004-212988](https://ntrs.nasa.gov/citations/20040047195) | 30,000 h exposures of supersonic-transport alloys at 93–135 °C |
| Industry history | [*Air & Cosmos* 1964 on Concorde's alloy](https://cap-avenir-concorde.fr/wp-content/uploads/2023/06/1-Air-Cosmos-16-01-1964-Choix-dun-alliage-leger-pour-la-construction-de-Concorde.pdf) | 10,000 specimens, 30,000 h at 130 °C, cyclic against continuous exposure |
| LPBF Al at temperature | [Lehmhus et al. 2022](https://doi.org/10.3390/ma15207386) · [Ren et al. 2024](https://doi.org/10.3390/met14080890) | Hot tensile curves for AlSi10Mg and Al-Mg-Sc-Zr |
| Found in the Pi browser (Edison missed both) | [Rakhmonov et al. 2025](https://www.osti.gov/biblio/3009477) · [Bahl et al. 2025](https://www.osti.gov/biblio/3030499) | Creep ductility 0.2–2.4 % against 12–21 % tensile ductility in LPBF Al-Ce-Ni-Mn-Zr; LPBF AlSi10Mg fatigue at 350 °C lasts longer at 20 kHz than at 20 Hz |
| Fatigue at temperature | [DOE report, AM piston alloy](https://www.osti.gov/biblio/2573209) | Fully reversed fatigue of LPBF Al-Ce-Ni-Mn-Zr at 150, 250 and 350 °C |
| Strain rate, AM | [Jakkula et al. 2021](https://doi.org/10.1007/s40870-021-00298-4) · [Rosenthal et al. 2017](https://doi.org/10.1016/j.msea.2016.11.070) | Scalmalloy from 10⁻³ to 1,000 s⁻¹; LPBF AlSi10Mg rate sensitivity |
| Strain rate, documented use | [DOT/FAA/TC-19/41 P2](https://rosap.ntl.bts.gov/view/dot/63526) · [NTRS 20240014937](https://ntrs.nasa.gov/citations/20240014937) | 2024-T351 from 10⁻⁴ to 5 × 10⁴ s⁻¹ for engine-debris models |
| Equipment (hot) | [ZwickRoell laserXtens](https://www.zwickroell.com/en/extensometers/laserxtens) · [Epsilon](https://www.epsilontech.com/) · [ZwickRoell Kappa Multistation](https://www.zwickroell.com/en/creep-testing-machines/kappa-multistation) | Non-contact and contact hot strain; multi-axis creep |
| Equipment (rate, screening) | [ZwickRoell HTM](https://zwickroell.com/en/servohydraulic-testing-machines/high-speed-testing-machine) · [REL](https://www.relinc.com/split-hopkinson-pressure-bar-testing) · [Plastometrex HotStage](https://www.plastometrex.com/products/plx-hotstage) | High-speed tension; Hopkinson bars; indentation plastometry to 800 °C |
| Test services | [WMT&R creep](https://www.wmtr.com/en.creep.html) · [Metcut](https://metcut.com/metallic-mechanical-testing/) · [SwRI high-rate](https://Swri.org/node/8663951) | Creep, hot tensile, fatigue, toughness; Hopkinson bars to 20,000 s⁻¹ |
| Industry article | [Fraunhofer IWM on 2618A compressor wheels](https://iwm.fraunhofer.de/en/services/materials-assessment-lifetime-concepts/highlights/aging-lifetime-radial-compressor-wheels.html) | Service aging of the Concorde alloy family |

## 8. Options for the lab

Cheapest first. Steps 1–4 fit the existing ladder of single tracks, density cubes and tensile bars, and use little powder.

1. **Fix and report the test settings now (no new hardware if the frame has an extensometer).**
   - **Control:** run ISO 6892-1 Method A1, at 0.00025 s⁻¹ to Rp0.2 and 0.0067 s⁻¹ after.
   - **Report:** gauge length, k, orientation and surface every time (§4.5).
   - **Add one strain-rate jump per alloy** (10⁻⁴ ↔ 10⁻² s⁻¹). It gives m, and flags negative rate sensitivity in
     the Al-Mg family before it confuses a dataset.
2. **Exposure curves with a box furnace.**
   - **What:** soak finished bars or hardness coupons for 100 h and 1,000 h at 200, 250 and 300 °C, then test at room
     temperature.
   - **Why:** this is the MMPDS "effect of exposure" curve and the HSR protocol, scaled down. It ranks thermal
     stability with no hot-test equipment.
3. **Hot tensile (ASTM E21, ISO 6892-2) at 150, 200, 250 and 300 °C.**
   - **Hardware:** a split furnace and a high-temperature or video extensometer on the existing frame.
   - **Conditions:** 10–30 min soak and a fixed rate. ORNL's hot tests used about 10⁻⁴ s⁻¹, so that rate makes results
     comparable with theirs.
   - **Second rate:** running one more rate (10⁻² s⁻¹) at 250 °C shows how rate-sensitive the alloy is hot.
4. **Screening across compositions.**
   - **Tests:** hardness (and hot hardness), PIP with a hot stage, or small-punch discs cut from a single build.
     Calibrate each against a few full tensile or creep tests.
   - **Why it's new:** Edison found no published composition-resolved hot screen of AM aluminum (Edison 06).
   - **Bending creep:** cantilever creep with DIC has been checked against uniaxial creep on LPBF A20X and AlSi10Mg
     (Edison 06). It is a cheap creep
     ranking that needs a small furnace, a camera and dead weights.
5. **Fatigue and toughness on the down-selected alloys.** Machined and as-built high-cycle fatigue (ASTM E466) tells
   whether the alloy or the surface limits life. Add E399/E1820 toughness, or a Kahn-type tear test for thin sections.
6. **Partners for creep and high rate.**
   - **Creep:** E139 creep and rupture to 1,000 h or more, which Edison found for no Sc-free LPBF alloy. Candidates are
     ORNL's creep lab, a commercial lab or a university with lever-arm frames.
   - **High rate:** 10²–10³ s⁻¹ through SwRI or a university Hopkinson-bar lab such as Ohio State. This only matters
     if crash, impact or debris loads are in scope.
7. **Multi-fidelity optimization.**
   - **Low fidelity:** hardness, PIP, small punch and post-exposure hardness. They are fast and cheap.
   - **High fidelity:** hot tensile and creep.
   - **The model:** treat these as fidelities in the lab's Bayesian optimization of Sc-, Li- and rare-earth-lean LPBF
     alloys. This mirrors the 77 K / 20 K pairing proposed in the cryogenic note.

## 9. Provenance, and corrections to Edison

**Read in the Pi-tunnelled browser:** NASA/TP-2004-212988, Lehmhus 2022, Ren 2024 and Wang 2022 (full text on
MDPI); Jakkula 2021 and Krizik 2024 (Springer, BYU access); the abstracts in OSTI records 3030499, 3009477, 17315112,
2301648 and 2573209; NTRS 19910029640 and 20240014937; Semantic Scholar abstracts of Rosenthal 2017, Plotkowski 2020,
Cao 2020 and du Plessis 2020. Rakhmonov 2025, Bahl 2025, Rosenthal 2017, Cao 2020 and the NASA Glenn Hopkinson-bar preprint turned up only in the browser searches; Edison didn't cite them. Everything else is marked "via Edison" or "survey". † marks PDFs whose text the survey
extracted with pypdf because WebFetch couldn't read them.

**Corrections to Edison:**

- **Concorde's life.** Edison 01 attributed a "60,000 h" structural life to Concorde. That was the HSCT program's
  goal. Concorde's design life was 15,000 h (Edison 09), and AU2GN was exposed for up to 30,000 h (*Air & Cosmos*).
- **Concorde's skin temperature.** Edison 01 cited a high-school research journal and an unpublished comparison. I
  used the 1964 *Air & Cosmos* article and Hénaff et al. instead.
- **HSCT soak temperature.** My query said HSCT exposures ran to 177 °C. Edison 09 correctly said the tensile campaign
  stopped at 135 °C; 177 °C is the TPS-protected structure limit.
- **ASTM B871.** Edison 03 described it as a current standard. ASTM's store page lists it as "Withdrawn 2017, No
  replacement" ([page](https://store.astm.org/b0871-01r13.html), survey and Pi).
- **AMS 7003.** Edison 03 called it a wire-feed specification. It is SAE's laser powder bed fusion process
  specification: SAE's own address for it is `standards/ams7003-laser-powder-bed-fusion-process` (Pi).
- **ORNL report figure.** Its caption labels the benchmark "2618-T61", but the text says 2219-T61. Edison 02 noticed
  this and used 2219-T61, as here.
- **"2219 compressor wheel".** Edison 09 found that the documented 2219 engine part is a cast fan *case*, not a
  rotating wheel, so I don't cite 2219 wheels.
- **ISO 6892-1 Method B.** Edison 04 described it as crosshead-displacement control. It controls the stress rate
  (ZwickRoell's page).
- **ISO 6892-1 ranges.** Edison 04 repeated my query's four-range list, including 0.025 s⁻¹. I give only the two
  recommended rates, which ZwickRoell and the standard's well-known values support.
- **Johnson-Cook sets.** Edison 04 took the 2024-T3, 6061-T6 and 7075-T6 parameters from a 2026 compilation, not from
  the original calibrations. Trace a set to its source before using it in a model.

**Not verified:**

- MMPDS tables themselves, which are restricted distribution.
- Instron product claims (403).
- Prices: none are given here. Edison found no published purchase prices or per-test rates.
- The numbers marked "via Edison" from papers behind ScienceDirect, which showed a Cloudflare check in the last round
  and wasn't retried.

**Google Scholar** again showed its "unusual traffic" CAPTCHA on the first page load from the Pi's network. I left
it, and used Semantic Scholar, NTRS and OSTI instead.
