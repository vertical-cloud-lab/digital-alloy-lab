# Cryogenic testing of aerospace alloys, with a focus on aluminum

*Issue [#254](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/254), 2026-11-12.*

**Sources.** Six Edison Scientific tasks: two `LITERATURE_HIGH` reviews, two `PRECEDENT` searches
and two `LITERATURE` questions. All answers and full trajectories are in
[`edison-trajectories/cryo-testing-aerospace-alloys/`](edison-trajectories/cryo-testing-aerospace-alloys/).
I also ran searches in a headed Chrome whose traffic left through a lab Raspberry Pi on BYU's network;
xdotool drove the mouse and keyboard ([search log](edison-trajectories/cryo-testing-aerospace-alloys/browser-search-log.md)).
In the same browser I opened the key articles, including several that Edison cited.
Finally, a web survey covered equipment vendors, test labs and industry write-ups. Section 8 says
which source each fact came from and where I corrected Edison.

## Bottom line

- **Aerospace alloys are tested cold because the hardware works cold.** Liquid oxygen is at 90 K,
  liquid methane at 111 K and liquid hydrogen at 20 K. Tank walls, domes, welds and feedlines are
  sized from properties measured at those temperatures. Liquid-hydrogen aircraft tanks, cryogenic
  space instruments and superconducting-magnet structures add 20 K and 4 K requirements.
- **Room-temperature tests can't predict the cold result. The Shuttle's tank is the textbook case.**
  Some lots of the Al-Li alloy 2195 plate for the Space Shuttle super-lightweight tank were rejected
  for low *cryogenic* fracture toughness. MSFC devised a two-step aging treatment, after which five
  previously rejected lots passed simulated-service testing, each tougher cold than warm
  ([NASA/TM-2002-211547](https://ntrs.nasa.gov/citations/20020030745)). The cryogenic-to-ambient
  toughness ratio depends on where T1 (Al₂CuLi) precipitates form, which is set by processing. So the
  ratio has to be measured; it can't be assumed.
- **Aluminum is the default cryogenic tank metal for a reason, but the reason has exceptions.** Al is
  FCC, so it has no ductile-to-brittle transition, and most alloys get stronger *and* more ductile
  when cold. For example, 2195-T8 goes from a UTS of 614 MPa at 298 K to 859 MPa at 20 K, and its
  elongation rises from about 11 % to 14 %. The exceptions: 7075-T6 and some peak-aged Al-Li tempers
  lose toughness by 77 K, short-transverse (S-L) toughness of Al-Li plate falls, and 2050-T84's L-T
  toughness dropped at 77 K.
- **For additively manufactured aluminum the data are very thin, and that matters for this lab.**
  - Tensile data exist only for a handful of alloys: LPBF AlSi10Mg and A6061-RAM2 tested in liquid
    hydrogen at 20 K, HIPed LPBF AlSi10Mg at 15 K, and LPBF A205 and 2219 at 77 K.
  - No cryogenic fracture-toughness or fatigue data were found for *any* AM aluminum alloy.
  - None were found for Scalmalloy either, although NASA picked Scalmalloy LPBF for a 2026
    cryogenic sample container.
  - None were found for Sc-, Li- or rare-earth-lean AM alloys, the kind this lab designs.
- **77 K is cheap, 20 K and 4 K are not.**
  - **77 K:** tests in liquid nitrogen are routine and use an ordinary load frame. They are the usual
    screening step.
  - **4 K:** testing in liquid helium uses about 25 to 30 L of helium per test in CERN's 100 kN cryostat.
  - **20 K:** cryocooler rigs need no liquid helium but took 8 to 13 h to cool one specimen to about
    20 K. Liquid-hydrogen immersion means a hydrogen-safe facility.
  - **Several specimens per cooldown:** this has been done (a six-specimen 4.2 K turret in 1977), but
    it is rare.
- **What it could mean for the lab:** the cheapest useful step is 77 K tensile testing of the AM
  alloys it already makes, followed by 20 K tests through a partner or a commercial lab. That would
  start filling a gap the literature leaves open: cryogenic data for critical-mineral-lean LPBF aluminum.
  See section 7.

## 1. Why cryogenic testing matters for aerospace alloys

### 1.1 Where aerospace structures get cold

| Fluid or environment | Temperature | Aerospace hardware |
|---|---:|---|
| Liquid methane (LCH₄) | 111 K | Methalox launch-vehicle tanks and feedlines |
| Liquid oxygen (LOX) | 90 K | Oxidizer tanks on every LOX launcher |
| Liquid nitrogen (LN₂) | 77 K | The usual laboratory test bath; ground systems |
| Liquid hydrogen (LH₂) | 20 K | Upper stages and core stages (SLS, Centaur, H3, Ariane), proposed LH₂ aircraft tanks |
| Liquid helium (LHe) | 4 K | Superconducting-magnet structures, cryogenic instruments; the standard test bath for 4 K data |

### 1.2 What a room-temperature test misses

1. **Fracture toughness can go either way.**
   - Strength nearly always rises on cooling, but toughness does not follow a single rule.
   - **Rises:** in 2090-T8E41, K_Ic (L-T) went from 36 to 51 MPa√m at 77 K, and in 8091-T8X from 20 to
     38 MPa√m ([Rao & Ritchie 1989](https://doi.org/10.1007/BF02653929)).
   - **Falls:**
     - 2091-T8X: L-T from 46 to 44 MPa√m, and S-L from 25 to 16 MPa√m.
     - 7075-T6 and 7475-T6: the fracture mode changes from void coalescence to transgranular shear, and
       toughness falls.
     - 2050-T84: L-T conditional toughness fell from 42.2 to 35.6 MPa√m at 77 K, while the T-L and L-S
       orientations rose ([NASA TM, NTRS 20160010564](https://ntrs.nasa.gov/citations/20160010564)).
   - Direction matters as much as temperature.
2. **Processing changes the cold result more than the warm one.** The SLWT lot rejections above, and
   the link between subgrain-boundary T1 and the cryogenic toughness ratio
   ([Chen et al. 1998](https://doi.org/10.1361/105994998770347576)), show that two lots with the same
   room-temperature properties can differ cold. NASA accepted 2195 lots on cryogenic toughness for
   this reason.
3. **Welds set the margin.**
   - Friction-stir welds of 2219-T87 tested at room temperature, 77 K and 20 K always failed in the
     thermo-mechanically affected zone, the weakest and least ductile region.
   - The friction-stir joints beat TIG joints by 79, 99 and 156 MPa in UTS at room temperature, 77 K
     and 20 K respectively.
   - The authors call fracture toughness (K_Ic or J_Ic) of each weld zone at all three temperatures
     "essential … to estimate the margins available for flight certification"
     ([Manikandan et al. 2021](https://doi.org/10.1007/s11661-021-06337-y)).
4. **Some effects only appear at very low temperature.**
   - Near 4 K, low heat capacity lets plastic work heat the specimen in bursts. This gives serrated
     ("discontinuous") yielding, which is why ASTM E1450 and ISO 6892-4 require displacement control
     and slow strain rates.
   - In 5xxx aluminum the opposite happens: Portevin-Le Chatelier serrations seen at room temperature
     disappear when cold. They also vanished in LPBF A205 at 77 K.
5. **Hydrogen service adds a second variable.** Testing *in* liquid hydrogen tests temperature and
   hydrogen exposure together; cold helium gas at 20 K is only a thermal stand-in. At NASA MSFC, LH₂
   immersion and cold-helium fatigue-crack-growth results agreed for Inconel 718, but LH₂ testing was
   expensive enough that a planned near-threshold test was dropped (NASA/TM-2005-213948, from Edison's
   equipment answer). Aluminum alloys are generally regarded as compatible with hydrogen, which is
   part of why they are used for LH₂ tanks.

### 1.3 Standards

| Standard | Scope |
|---|---|
| ISO 6892-3 | Tensile testing at low temperature, down to −196 °C (77 K) |
| [ISO 6892-4:2015](https://www.standards.nimonik.com/products/iso/6892-4/) | Tensile testing in liquid helium (4 K); replaced ISO 19819:2004 |
| [ASTM E1450](https://webstore.ansi.org/standards/astm/astme145016) | Tension testing of structural alloys in liquid helium (latest revision E1450-24) |
| ASTM E1820, E399 | Fracture toughness (J_Ic, K_Ic). Used at 77 K, 20 K and 4 K by NHMFL, KIT and the 2219 FSW study |
| ASTM E647 | Fatigue-crack growth. NASA MSFC used it in LH₂ at 20 K |
| ASTM E23 | Charpy impact, including low temperature (not a fracture-toughness value) |
| ASTM B557 | Tension testing of aluminum products. The room-temperature half of the 2219 FSW study |

### 1.4 Is 77 K a good stand-in for 20 K?

77 K is often a stand-in for 20 K. Nearly all of the AM-aluminum and alloy-screening literature
stops at 77 K because liquid nitrogen is cheap. For aluminum the trend from 77 K to 20 K is usually
the same direction: more strength, and usually more elongation. In 2195-T8, elongation stays near
11 % from 93 K to 298 K and only climbs to 14 % below 55 K. But toughness does not follow reliably,
for two reasons:

- 2195's toughness ratio changes little, or even falls, from 295 K to 77 K, then rises
  significantly at 20 K (Edison, from the 2195 literature).
- In 7075, toughness peaks near 30 K and falls toward 4 K.

So 77 K is a good screening temperature, but qualifying a part for LH₂ service needs 20 K data.

## 2. Aluminum specifically

### 2.1 Wrought alloys

| Alloy, temper, direction | T (K) | YS (MPa) | UTS (MPa) | El. (%) | Toughness (MPa√m) | Source |
|---|---:|---:|---:|---:|---|---|
| 2195-T8 | 298 | 586 | 614 | ≈11 | — | [Metals 2023](https://doi.org/10.3390/met13040740) † |
| 2195-T8 | 20 | 724 | 859 | ≈14 | — | [Metals 2023](https://doi.org/10.3390/met13040740) † |
| 2195-T8, L (1.85 in plate) | 77 | 641 | 696 | 10.9 | — | NASA evaluation (Edison 02) |
| 2050-T84, L, t/6 | 77 | 562 | 612 | 16.9 | L-T 35.6 (from 42.2 at RT) ‡ | [NTRS 20160010564](https://ntrs.nasa.gov/citations/20160010564) |
| 2090-T8E41, L | 298 / 77 | 552 / 587 | 589 / 642 | 11 / 14 | L-T 36 / 51 | [Rao & Ritchie 1989](https://doi.org/10.1007/BF02653929) |
| 2091-T8X, L | 298 / 77 | 425 / 483 | 481 / 610 | 8 / 14 | L-T 46 / 44; S-L 25 / 16 | same |
| 8091-T8X, L | 298 / 77 | 537 / 574 | 581 / 697 | 6 / 12 | L-T 20 / 38 | same |
| 5083-H112, 6061-T6 | 300 / 20 | all rise | all rise | rise | Reduction of area falls: 53.6→34.6 % (5083), 43.0→23.5 % (6061) | [Kim et al. 2022](https://doi.org/10.3390/pr10112401) † |
| 7075-T6 | 298 → 77 | rises | rises | — | **falls** (fracture-mode transition) | Rao & Ritchie 1989; Edison 02 |

† Read in full in the Pi-tunnelled browser. ‡ Conditional K_Q from J (not ASTM-valid K_Ic). For 2219-T87,
2014, 5456, 6061 and 7075, NASA's 1960s–70s **Materials Data Handbooks** compile properties from cryogenic to
elevated temperature
([2219](https://ntrs.nasa.gov/citations/19720022811), [6061](https://ntrs.nasa.gov/citations/19720022808),
[5456](https://ntrs.nasa.gov/citations/19720022807), [7075](https://ntrs.nasa.gov/citations/19720022809),
[2014](https://ntrs.nasa.gov/citations/19720023885)). 5456 flew in the Saturn I/IB first stages.

**Why Al gets stronger and more ductile when cold.** These are the mechanisms Edison rates as strongly
supported:

- Thermally activated cross-slip and dynamic recovery are suppressed, so dislocations pile up faster.
  In 2195-T8, dislocation density went from about 2 × 10¹⁴ m⁻² at 298 K to 5 × 10¹⁴ m⁻² at 20 K.
- The higher work-hardening rate pushes the Considère necking point to larger strain.
- Dynamic strain aging (Portevin-Le Chatelier) is suppressed.
- In Al-Li plate, delamination between pancake grains splits a crack front into thinner, nearer-plane-stress
  ligaments, which raises L-T toughness. The same delamination is what drags S-L toughness down.

### 2.2 Welds

- **External Tank:** NASA MSFC developed friction stir welding for the Space Shuttle External Tank. The
  switch from 2219-T87 to 2195 Al-Li for the super-lightweight tank (first flight STS-91, 1998) saved
  about 7,500 lb.
- **Fusion-weld filler:** for fusion welds of 2195, NASA, Lockheed Martin and McCook Metals developed
  the B218 Al-Cu filler wire. They qualified it against 4043 with room-temperature and cryogenic
  tensile tests and fracture-toughness tests ([NTRS 20000112954](https://ntrs.nasa.gov/citations/20000112954)).
- **SLS:** the SLS core-stage hydrogen-tank barrels are 2219, friction stir welded at Michoud
  ([NASA](https://www.nasa.gov/centers-and-facilities/marshall/first-liquid-hydrogen-tank-barrel-segment-for-the-sls-core-stage-completed-at-michoud/)).
  NASA has also developed 2195-T8 gores for SLS domes ([NTRS 20160008018](https://ntrs.nasa.gov/citations/20160008018)).
- **Weld zones in 2219-T87:** see §1.2 point 3. That is the cleanest open dataset on weld zones at
  room temperature, 77 K and 20 K.

### 2.3 Additively manufactured aluminum

| Alloy (process, condition) | T (K) | Result | Source |
|---|---:|---|---|
| AlSi10Mg (SLM, EOS M290), XY / ZX | 20, in LH₂ | UTS 483 ± 21 / 512 ± 43 MPa; E 73.5 / 65.1 GPa; elongation not measured (strain gauge over range); n = 5 each | [Adams, Rinauro & Leachman 2024](https://doi.org/10.1088/1757-899X/1302/1/012006) (WSU), via Edison 03 |
| A6061-RAM2 (SLM), XY / ZX | 20, in LH₂ | UTS 568 ± 16 / 516 ± 41 MPa | same |
| Al10SiMg (LPBF + **HIP**) | 15 | UTS 395 MPa, **uniform elongation 25 %**; the Si network carries load while the Al matrix keeps work-hardening (in-situ neutron diffraction, J-PARC; GM-cryocooler load cell) | [Naeem et al. 2025](https://doi.org/10.1038/s43246-025-00793-4) †. Found in the browser search; Edison's precedent search missed it |
| A205 / A20X family (LPBF) | 77 | As-built YS 317, UTS 371 MPa, 15.5 %; heat-treated YS 367, UTS 486 MPa, 14.8 %; serrated flow gone at 77 K | Tumulu 2025 thesis, via Edison 02 |
| 2219 (LPBF; as-built, T5, T6) | 77 | YS and UTS up in all three conditions; numbers in the thesis tables | same |
| Scalmalloy (LPBF) | ≤ 77 | **No cryogenic mechanical data found.** KIT measured thermal conductivity, expansion and heat capacity down to about 4 K ([Weiss et al. 2024](https://doi.org/10.1088/1757-899X/1302/1/012005)). A Siemens-led LH₂-aviation project reported only that "initial cryogenic tests" were unsatisfactory, with no numbers ([Rehme & Weidermann 2024](https://doi.org/10.1088/1757-899X/1301/1/012047), as read by Edison) | Edison 02, 03 |
| Al-Fe-Zr, Al-Mn-Sc, Al-Cu-Ce (LPBF); 2319/2219 (WAAM) | ≤ 77 | No cryogenic data found | Edison 02 |

Even so, NASA chose **Scalmalloy LPBF** for the subscale secondary sealed container of the
FROSTE lunar-regolith sample project, which keeps samples at cryogenic temperature
([NTRS 20260004465](https://ntrs.nasa.gov/citations/20260004465)). Its rationale was strength-to-weight,
thermal conductivity and "robust mechanical behavior at cryogenic temperatures". AM aluminum is
already being picked for cryogenic hardware ahead of the property data.

### 2.4 Gaps that matter for this lab

1. No cryogenic **fracture toughness** or **fatigue** for any AM aluminum alloy (Edison 02 and 03).
2. No 4 K tensile data for any LPBF aluminum alloy; only two 15 to 20 K datasets.
3. No cryogenic data for **Scalmalloy, Al-Fe-Zr, Al-Mn-Sc, Al-Cu-Ce**, or any Sc-, Li- or rare-earth-lean
   AM composition. That is exactly the composition space FLAIME searches.
4. Sparse open data for third-generation Al-Li (2060, 2098, 2198), even though Falcon 9 tanks use 2198
   sheet and 2195 plate (see §5).
5. The role of LPBF porosity and the eutectic-Si network on cryogenic ductility has barely been studied.
   The 15 K neutron study suggests the Si network *helps*, which a solutionizing heat treatment would remove.

## 3. How it is done: methods, equipment and throughput

| Architecture | Specimen temperature | Documented examples | Helium, time, throughput |
|---|---|---|---|
| LN₂ immersion (dewar around the grips) | 77 K | Nearly every 77 K study. 2195-T8 used an LN₂ chamber for 93 to 298 K and direct immersion at 77 K | Cheap. Works on an ordinary load frame with a cryostat or dewar fixture |
| LHe immersion cryostat | 4 K | **CERN** in-house 100 kN cryostat (300 to 4 K) ([10.1088/1757-899X/102/1/012007](https://doi.org/10.1088/1757-899X/102/1/012007)); **NHMFL** 100 kN servo-hydraulic frames for 4 K tension, crack growth and J_Ic ([10.1088/1757-899X/279/1/012001](https://doi.org/10.1088/1757-899X/279/1/012001)); **NIST** MTS 55-kip frame at 77 and 4 K ([NIST TN 2229](https://doi.org/10.6028/NIST.TN.2229)) | CERN: **25 to 30 L LHe per test**, 20 to 25 min cooldown between tests |
| Recondensing LHe bath | 4 K | NRIM/NIMS Tsukuba fatigue plant | About 50 L LHe and 300 kg LN₂ to start; about 15 L LHe after each specimen change; more than 460 h of continuous running |
| Two-chamber transfer cooling (not immersed) | RT to 4.2 K | **KIT CryoMaK**: MTS 25/50/100, ATLAS 650 kN, PHOENIX 100 kN ([10.12776/ams.v21i4.650](https://doi.org/10.12776/ams.v21i4.650)) | Avoids boiling bubbles that disturb extensometers |
| Cold-gas flow chamber | 20 K | NASA MSFC cold-He fatigue-crack-growth rig | Continuous LHe from a tanker; needed constant monitoring |
| LH₂ immersion | 20 K | NASA MSFC Hydrogen Test Facility; WSU HYPER lab (CRAFT: Cryomech PT-415 pulse tube + MTS Acumen 12, liquefies its own H₂) ([10.1088/1757-899X/1240/1/012080](https://doi.org/10.1088/1757-899X/1240/1/012080)); a compact platform that condenses 2 to 3 L LH₂ on site with a two-stage cryocooler ([10.1088/1757-899X/1327/1/012099](https://doi.org/10.1088/1757-899X/1327/1/012099)) † | Hydrogen-safe facility needed. MSFC calls LH₂ tests expensive |
| Cryocooler, conduction plus He exchange gas | about 16 to 20 K | KIMM (Korea): ULVAC GM cooler, Walter + bai frame, Epsilon 3442 extensometer ([Kim et al. 2022](https://doi.org/10.3390/pr10112401)); China: two GM coolers, DIC through windows ([10.1088/1757-899X/278/1/012083](https://doi.org/10.1088/1757-899X/278/1/012083)); NASA Glenn LESTR, 40 to 125 K | **No liquid helium**, but **8 to 13 h to cool one specimen**. A cold head rated at 4 K does not mean a 4 K specimen |
| Miniature and small-punch | 77 K and 4.2 K | 10 × 10 × 0.5 mm coupons ([Misawa 1989](https://doi.org/10.1016/0022-3115(89)90538-2); [Shindo 2004](https://doi.org/10.1016/j.cryogenics.2004.04.008)); micro-samples on a pulse-tube cold head ([10.1088/1757-899X/102/1/012011](https://doi.org/10.1088/1757-899X/102/1/012011)) † | Little material and little cryogen. Toughness needs correlating to standard specimens |
| **Several specimens per cooldown** | 4.2 K | Six-specimen rotating turret ([Ishikawa & Tsuya 1977](https://doi.org/10.1016/0011-2275(77)90199-0)); eight-position indexed in-reactor holder tested aluminum ([10.1007/BF01235494](https://doi.org/10.1007/BF01235494)) | Turret: **12 to 15 L He for six tests**, about 3 h at 4.2 K. Still rare (Edison 04) |

**Strain measurement.** Clip-on extensometers rated for cryogenic use, calibrated at each bath temperature:

- NIST used Shepic clip gauges.
- CERN uses its own C- and W-shaped gauges.
- KIMM used Epsilon 3442.
- KIT builds clip-ons on 350 Ω strain-gauge bridges.
- Digital image correlation (DIC) through windows works at 20 K.

Measure temperature at the specimen, not at the cold head.

## 4. Vendors, manufacturers and test labs

From the web survey. "Pi" means I also opened the page in the Pi-tunnelled browser and checked the
claim (2026-11-12). The rest were fetched by the survey. Lowest temperatures are as each vendor states
them.

**Off-the-shelf 4 K mechanical testing barely exists.** NPL's 2022 requirements study says mechanical-test
cryostats "are not readily available as off-the-shelf items and require bespoke designs"
([NPL MAT 102](https://eprintspublications.npl.co.uk/9464/1/MAT102.pdf)). Among the frame makers, only MTS
advertises a liquid-helium cryostat.

| Category | Vendor and page | What it offers | Lowest stated T |
|---|---|---|---|
| Load frame + cryostat | **MTS**, [cryogenic testing](https://www.mts.com/en/articles/materials/cryogenic) (Pi) | Turnkey cryostat "that works with liquid helium or liquid nitrogen" on Landmark 100 or 250 kN frames. Tension, compression, tension-compression fatigue; 632/634 extensometers that work in the cryostat | 4 K |
| Load frame + cryostat | **ZwickRoell**, [testing at cryogenic temperatures](https://www.zwickroell.com/industries/energy/testing-at-cryogenic-temperatures) (Pi) | LN₂ immersion cryostats and chambers, up to 100 kN. Helium cooling to reach 20 K, described for composites. Advises weighing helium's much higher cost against nitrogen | 20 K (77 K in LN₂) |
| Chambers | **Instron** ([chambers](https://www.instron.com/en/products/testing-accessories/environmental-chambers-furnaces/environmental-chambers/)), **Tinius Olsen** ([−150 °C chamber](https://www.tiniusolsen.com/?p=23996)), **Shimadzu** ([thermostatic chambers](https://www.ssi.shimadzu.com/products/materials-testing/uni-ttm-system/thermostatic-chambers/index.html)) | LN₂-cooled gas chambers, not cryostats | about −150 °C (Shimadzu −70 °C) |
| Custom cryostats | **Lake Shore (Janis)**, [custom systems](https://www.lakeshore.com/products/product-detail/janis/custom-engineered-cryogenic-systems); **Absolut System**, [products](https://www.absolut-system.com/) | Janis lists tensile-testing cryostats among its custom builds. Absolut System makes cryostats and cryocoolers and runs a test lab | down to 1.8 K (systems) |
| Cryocoolers for helium-free rigs | **Bluefors (Cryomech)**, [PT415](https://bluefors.com/products/pulse-tube-cryocoolers/pt415-pulse-tube-cryocooler/) (in WSU's [CRAFT](https://hydrogen.wsu.edu/craft/)); **SHI Cryogenics (Sumitomo)**, [RDK-415D2](https://shicryogenics.com/?p=79); ULVAC GM (KIMM rig) | 1.5 W at 4.2 K cold heads. Specimens in published metal rigs reached about 16 to 20 K, not 4 K | cold head about 3 K |
| Cryogenic extensometers | **MTS** [634.11F-21 / 634.12F-21](https://mts.com/en/products/materials/extensometers/axial-extensometers-25mm-gage) ("-21 … down to −269 °C"); **Epsilon Technology** 3542 -LT/-LHT ([datasheet](https://aml-instruments.s3.amazonaws.com/uploads/2019/11/Axial-Extensometer-Epsilon-Model-3542.pdf)) | Clip-on axial extensometers | −269 to −270 °C |
| In-situ stages (micro-tensile, SEM or optical) | **Linkam** [Modular Force Stage](https://www.linkam.co.uk/mfs) and TST350; **Kammrath & Weiss** [cryo module](https://eden-instruments.com/en/in-situ-equipments/kammrath-weiss/cryo-module-80-kelvin) | Small-specimen tension or bending with LN₂ cooling. K&W lists an LHe substage to 5 K | −196 °C (K&W LHe substage 5 K) |
| Test labs (commercial) | **Element**, [cryogenic testing](https://www.element.com/materials-testing-services/mechanical-testing-services/cryogenics-testing) (Pi) | Tensile, fracture toughness, fatigue and fatigue-crack growth down to 4 K; names aluminum and Al-Li alloys. ASTM E1450, ISO 6892-4, JIS Z 2277/2283/2284 | 4 K |
| Test labs (commercial) | **Linde Engineering** [PLANTSERV](https://www.engineering.linde.com/PLANTSERV-Charpy-Impact-and-Tensile-Testing-in-Liquid-Helium); **Westmoreland (WMT&R)** [mechanical testing](https://www.wmtr.com/en.mechanicaltesting.html); **AAC** (Austria) [cryogenic testing](https://aac-research.at/services/testing/cryogenic-mechanical-testing); **Lucideon** (UK) [cryogenic testing](https://www.lucideon.com/uk/testing-characterisation/high-temperature-performance-testing/cryogenic-high-temp-mechanical-testing) | Tensile and Charpy at 4.2 K (Linde); "−450 °F to +2400 °F" (WMT&R); tensile, fatigue, toughness and crack growth (AAC); 77 K (Lucideon) | 4 K to 77 K |
| 20 K for hydrogen | **NLR** (Netherlands) [cryostat](https://www.nlr.org/newsroom/facility/cryostat/) | Static coupon tests at 20 K, up to 100 kN; fatigue and in-situ H₂ testing planned. NLR calls 20 K static testing "shared by only a few test houses globally (if any)" | 20 K |
| Government and academic | **NIST Boulder** ([2023 spotlight](https://www.nist.gov/news-events/news/2023/05/spotlight-putting-steel-test-under-cryogenic-temperatures)); **NASA MSFC** Hydrogen Test Facility ([NTRS 20090028713](https://ntrs.nasa.gov/citations/20090028713)); **NASA White Sands** ([materials testing](https://www.nasa.gov/centers-and-facilities/white-sands/material-level-testing)); **National MagLab** ([100 kN spec sheet](https://nationalmaglab.org/media/t3offpd4/100kn-specsheet.pdf)); **PNNL** ([cryogenic frame](https://www.pnnl.gov/publications/mechanical-test-frame-property-evaluations-cryogenic-temperature)); **WSU HYPER** ([CRAFT](https://hydrogen.wsu.edu/craft/)); **KIT CryoMaK**; **CERN** | 4 K immersion (NIST, MagLab, CERN, KIT); 20 K in H₂ with 8 test cells (MSFC); LN₂ and LOX (White Sands); a 10 kN continuous-flow cryostat (PNNL); 20 K in LH₂ with the pulse tube liquefying its own hydrogen (WSU) | 4 K to 77 K |

## 5. Documented industry use (aluminum)

- **Space Shuttle super-lightweight tank.** The tank moved from 2219 to 2195 Al-Li: 30 % stronger,
  5 % less dense, and "withstands fractures to a temperature of minus 423 degrees"
  ([NASA fact sheet](https://www.nasa.gov/sites/default/files/113020main_shuttle_lightweight.pdf)).
  Plate lots were accepted on cryogenic fracture toughness ([NASA/TM-2002-211547](https://ntrs.nasa.gov/citations/20020030745)).
  Weld filler B218 replaced 4043 after room-temperature and cryogenic qualification
  ([NTRS 20000112954](https://ntrs.nasa.gov/citations/20000112954)).
- **The producer's design rule.** Constellium's 2019 *Light Metal Age* article says launch designers
  "require that the metallic tankage solutions exhibit 10-30% improvement in fracture toughness when
  tanks are chilled to the cryogenic range". It adds that 2xxx alloys meet this while some 7xxx alloys
  embrittle. The article covers 2050 at LOX and LH₂ temperatures and names SLS, Orion, Falcon, New
  Glenn, Vulcan and Ariane ([Light Metal Age](https://www.lightmetalage.com/news/industry-news/aerospace/article-the-evolution-of-constellium-al-li-alloys-for-space-launch-and-crew-module-applications/), Pi).
- **SLS.** The core-stage LH₂ tank barrels are 2219, friction stir welded at Michoud
  ([NASA](https://www.nasa.gov/centers-and-facilities/marshall/first-liquid-hydrogen-tank-barrel-segment-for-the-sls-core-stage-completed-at-michoud/)).
  NASA has developed 2195-T8 dome gores ([NTRS 20160008018](https://ntrs.nasa.gov/citations/20160008018))
  and 5.5 m spin-formed Al-Li tank domes from friction-stir-welded blanks, which were characterized
  by tensile, fracture-toughness, stress-corrosion and simulated-service tests
  ([NTRS 20130014077](https://ntrs.nasa.gov/citations/20130014077); [Alcoa 2010](https://www.howmet.com/press-release/2010-03-30/nasas-friction-stir-welded-spun-formed-tank-dome-debuts-with-alcoa-aluminum-lithium)).
  NASA Langley wants thick Al-Li plate (2195, 2050) for cryotanks ([NTRS 20200010741](https://ntrs.nasa.gov/citations/20200010741)).
- **Falcon 9.** The tanks are friction-stir-welded Al-Li: 2198 sheet and 2195 plate, according to a
  2008 Alcan/SpaceX AeroMat paper ([abstract](https://asm.confex.com/asm/aero08/techprogram/paper_19826.htm)).
  Light Metal Age names Airware 2195-T8 for barrels and domes
  ([2019](https://www.lightmetalage.com/news/industry-news/aerospace/how-light-metals-help-spacex-land-falcon-9-rockets-with-astonishing-accuracy/)).
- **Composite vs. aluminum LH₂ tanks.** The X-33 composite LH₂ tank failed by microcracking, and the
  program switched to aluminum ([Spaceflight Now, 2000](https://spaceflightnow.com/news/n0009/29x33/)).
  NASA's later composite tanks were cycled with LH₂ at Marshall against an Al-Li baseline
  ([CompositesWorld](https://www.compositesworld.com/articles/nasaboeing-composite-launch-vehicle-fuel-tank-scores-firsts)).
- **LH₂ aircraft.** Airbus stores LH₂ at −253 °C in a metallic tank built in Nantes, and tested the
  first one with nitrogen ([Airbus, 2022](https://www.airbus.com/en/newsroom/stories/2022-11-the-cold-heart-that-powers-our-zeroe-aircraft)).
  NLR says "establishing 'material allowables' at 20 K is crucial due to the lack of prior experience"
  ([NLR, 2024](https://www.nlr.org/news/cold-testing-has-become-hot), Pi). An academic digital model
  of a 2219 LH₂ aircraft tank is in [Aerospace 2024](https://doi.org/10.3390/aerospace11020161).
- **AM aluminum in cryogenic hardware.** NASA's FROSTE lunar-sample container uses Scalmalloy LPBF
  ([NTRS 20260004465](https://ntrs.nasa.gov/citations/20260004465)). Fraunhofer IWS and partners printed
  AlSi40 cryogenic mirrors, which are already in this repo's
  [downstream-applications review](edison-trajectories/pareto-am-al-alloys/downstream_applications.md).
- **Outside aerospace.** LNG tanks are the other big aluminum cryogenic application. Moss-type spherical
  LNG tanks moved from 9 % Ni steel to 5083 ([TWI](https://www.twi-global.com/technical-knowledge/published-papers/fabricating-lng-carriers-september-2006)),
  and the qualification data for 5083-O are in [ASTM STP 579](https://www.osti.gov/biblio/7264681).

## 6. Representative links

A short list, one or two per category. The rest are in the tables above.

| Category | Link | Why it's representative |
|---|---|---|
| Edison: AM Al at 20 K | [Adams, Rinauro & Leachman 2024](https://doi.org/10.1088/1757-899X/1302/1/012006) | LPBF AlSi10Mg and A6061-RAM2 pulled in liquid hydrogen at 20 K, the only such dataset found |
| Pi browser: AM Al at 15 K | [Naeem et al. 2025, *Commun. Mater.*](https://doi.org/10.1038/s43246-025-00793-4) | HIPed LPBF Al10SiMg: UTS 395 MPa and 25 % uniform elongation at 15 K, with the mechanism from neutron diffraction |
| Edison: Al-Li toughness | [Rao & Ritchie 1989](https://doi.org/10.1007/BF02653929) | Cryogenic toughness can rise (2090, 8091) or fall (2091-T8X, 7075) |
| Documented use | [NASA/TM-2002-211547](https://ntrs.nasa.gov/citations/20020030745) | Shuttle 2195 lots rejected and then recovered on cryogenic fracture toughness |
| Industry article | [Light Metal Age / Constellium 2019](https://www.lightmetalage.com/news/industry-news/aerospace/article-the-evolution-of-constellium-al-li-alloys-for-space-launch-and-crew-module-applications/) | The 10–30 % cryogenic toughness-gain requirement, and the 7xxx warning |
| AM in service | [NTRS 20260004465](https://ntrs.nasa.gov/citations/20260004465) | NASA picked Scalmalloy LPBF for cryogenic hardware without published cryogenic mechanical data |
| Equipment vendor | [MTS cryogenic testing](https://www.mts.com/en/articles/materials/cryogenic) | The off-the-shelf LHe/LN₂ cryostat on a standard frame |
| Test service | [Element cryogenic testing](https://www.element.com/materials-testing-services/mechanical-testing-services/cryogenics-testing) | Commercial 4 K tensile, toughness and fatigue testing for Al and Al-Li |
| Facility practice | [CERN cryostat (IOP 2015)](https://doi.org/10.1088/1757-899X/102/1/012007) | What a 4 K test costs in helium (25–30 L per test) |
| 20 K for hydrogen | [WSU HYPER CRAFT](https://hydrogen.wsu.edu/craft/) / [NLR](https://www.nlr.org/news/cold-testing-has-become-hot) | The academic and institute side of 20 K hydrogen testing |

## 7. What this could mean for the lab

These are options to discuss, not decisions.

1. **Add a 77 K step to the tensile rung.**
   - **What:** test sub-size tensile bars cut from the same builds in liquid nitrogen, using an LN₂
     cryostat or dewar fixture on a standard frame and a clip-on extensometer rated for cryogenic use
     (e.g., MTS 634.xxF-21 or Epsilon 3542-LT).
   - **Why:** it is the cheapest cryogenic data point, and it would catch alloys that embrittle when
     cold (as 7075-T6 does).
   - **Who:** either the group that runs the room-temperature tensile tests adds the fixture, or a
     commercial lab does it (Element, Lucideon, WMT&R).
2. **Confirm the best candidates at 20 K.** 77 K does not reliably predict 20 K toughness, so send a
   few candidates for 20 K tests in LH₂ or cold helium.
   - WSU's HYPER lab has tested LPBF AlSi10Mg in LH₂, so it is a natural academic collaborator.
   - Element (to 4 K) and NLR (20 K) are commercial and institute options.
3. **Aim at the clearest gap: cryogenic fracture toughness of AM aluminum.**
   - No K_Ic, J_Ic or fatigue data exist at 77 K or below for any AM Al alloy.
   - Small specimens suit AM builds. Small-punch testing at 77 K has been correlated with toughness
     for steels, but not yet for aluminum, so a correlation study would be needed first.
   - Standard compact-tension J_Ic tests (ASTM E1820) at a partner lab would anchor the results.
4. **Fold cryogenic properties into the optimization.**
   - **As outputs:** 77 K strength and elongation, or the 77 K to room-temperature toughness ratio,
     become extra output nodes, or a constraint such as "no loss of toughness when cold".
   - **As a cheap proxy:** cheap 77 K results are a natural low-fidelity proxy for expensive 20 K
     tests, which suits multi-fidelity Bayesian optimization.
   - **The opening:** this is new ground for Sc-, Li- and rare-earth-lean LPBF alloys, where no
     cryogenic data exist.
5. **Throughput is itself an open problem.** Testing several specimens per cooldown has rarely been
   done since the 1970s turret. A cryocooler rig with a specimen carousel would fit the lab's
   self-driving-lab work, but it would be a substantial engineering project.

## 8. Method and provenance

**Edison Scientific.** Six tasks were submitted at 16:41 UTC with
[`scripts/edison_cryo_testing.py`](scripts/edison_cryo_testing.py) (edison-client 0.18.0). Every
answer is saved as `.md` and every full trajectory as `.trajectory.json`, with authors' e-mail
addresses from the retrieved paper text redacted.

| # | Question | Job | Task ID | Answer |
|---|---|---|---|---|
| 01 | Why cryogenic testing matters for aerospace alloys | `LITERATURE_HIGH` | `5060ace2-75c9-4e0d-ab83-1a87573d6dc4` | pending; fetch with `python scripts/edison_cryo_testing.py fetch` |
| 02 | Aluminum alloys at cryogenic temperature (wrought, Al-Li, welds, AM, gaps) | `LITERATURE_HIGH` | `c690cb5a-afe5-4b91-87eb-7a59884a1a71` | [02-aluminum-cryogenic-behavior.md](edison-trajectories/cryo-testing-aerospace-alloys/02-aluminum-cryogenic-behavior.md) |
| 03 | Has LPBF aluminum been tested at 20 K or 4 K? | `PRECEDENT` | `3ccea3dc-454b-4b67-818a-50d167d91589` | [03-precedent-lpbf-al-at-20K-4K.md](edison-trajectories/cryo-testing-aerospace-alloys/03-precedent-lpbf-al-at-20K-4K.md) |
| 04 | Has anyone tested several specimens per cooldown? | `PRECEDENT` | `44cb0c12-3873-4e7e-9a98-4172d8d50516` | [04-precedent-high-throughput-cryo-testing.md](edison-trajectories/cryo-testing-aerospace-alloys/04-precedent-high-throughput-cryo-testing.md) |
| 05 | Equipment and facilities for 77 K, 20 K and 4 K testing | `LITERATURE` | `5bd53d09-b488-4318-a51d-2f7c2bb6069d` | [05-equipment-and-facilities.md](edison-trajectories/cryo-testing-aerospace-alloys/05-equipment-and-facilities.md) |
| 06 | Documented use by launch-vehicle and aircraft programs | `LITERATURE` | `948ef097-73ce-4328-acd5-07bf874cb16e` | pending; fetch with `python scripts/edison_cryo_testing.py fetch` |

**Headed browser through the Pi.**
- **Setup:** Xvfb display `:99` with headed Chrome 157. Its traffic went through an SSH SOCKS tunnel
  to a lab Raspberry Pi on the tailnet; the rig is byu-vcl's pinned `rig.sh`, as in CLAUDE.md's
  Onshape section. The tunnel's exit checked as Brigham Young University (AS6510).
- **Driving it:** `xdotool` moved the mouse to each search box, clicked, typed the query and pressed
  Enter, and scrolled the results with the wheel. Playwright, attached over DevTools, only read the
  page text and element positions.
- **Searches:** 11 Semantic Scholar searches and 10 NASA NTRS searches, listed in the
  [browser search log](edison-trajectories/cryo-testing-aerospace-alloys/browser-search-log.md) with
  two screenshots.
- **Pages read:** about 15 article and vendor pages, including Edison-cited papers.
- **Blocked:** Google Scholar showed its "unusual traffic" CAPTCHA on the first page load, before any
  query was typed. IOPscience showed a bot check once, and ScienceDirect a Cloudflare challenge. All
  three were skipped, with no attempt to get past them.
- **Downloads:** none. No PDFs were downloaded or committed.

**Vendor and industry survey.** A web search-and-fetch pass checked every URL. I then re-opened the
top five (MTS, Element, ZwickRoell, Light Metal Age/Constellium, NLR) in the Pi browser and confirmed
the quoted claims.

**Where I corrected or added to Edison.**
- Edison 02 lists the 15 K Al10SiMg (Naeem 2025) as "as-built". The paper tested **LPBF + HIP**
  material.
- Edison 02 says Falcon 9 "reportedly" uses 2219. Its tanks are **Al-Li (2198 sheet, 2195 plate)**.
- Edison 02 calls 2195 "the primary alloy" of the SLS core stage. The LH₂ tank barrels are **2219**;
  2195 is used for some dome development.
- Edison 03's precedent search missed Naeem 2025 (15 K). The browser search found it.
- Edison 02 says Adams' 20 K AlSi10Mg strength is a "near-doubling" of room-temperature strength. The
  room-temperature baseline wasn't checked, so that claim is left out here.
