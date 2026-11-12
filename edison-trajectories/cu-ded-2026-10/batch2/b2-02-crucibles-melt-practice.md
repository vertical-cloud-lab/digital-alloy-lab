<!--
Edison Scientific LITERATURE task (batch 2)
- Task ID: 14972c4a-bfc1-4200-a826-5dedf50fafd1
- Submitted: 2026-10-17T05:37:00Z
- Fetched: 2026-10-17T06:08:51Z (status: success)
- Raw trajectory JSON: ../raw/b2-02-crucibles-melt-practice.json.gz
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

QUESTION: What crucible and melt practice is used for small (0.1-1 kg)
induction melts of Cu-Ni (10-30 wt% Ni) and nickel-aluminum bronze at
1150-1300 C under argon, as in small-batch powder atomizers? Compare
graphite (carbon pickup by Ni-bearing melts), clay-graphite, alumina,
zirconia, magnesia and boron nitride for reactions, contamination and thermal
shock, and say which are known to react with aluminum- or manganese-bearing
copper melts. Cover hydrogen and oxygen pickup and the steam reaction in
copper melts, deoxidizers used in Cu-Ni (Mn, Ti, Mg, B, Li, P) and their
effect on later weld or AM porosity, and how master alloys (Cu-Ni, Cu-Fe,
Cu-Mn, Cu-Al) are used to reach composition. Give typical composition losses
(e.g. Mn, Al volatilization or oxidation) if reported.

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

QUESTION: What crucible and melt practice is used for small (0.1-1 kg)
induction melts of Cu-Ni (10-30 wt% Ni) and nickel-aluminum bronze at
1150-1300 C under argon, as in small-batch powder atomizers? Compare
graphite (carbon pickup by Ni-bearing melts), clay-graphite, alumina,
zirconia, magnesia and boron nitride for reactions, contamination and thermal
shock, and say which are known to react with aluminum- or manganese-bearing
copper melts. Cover hydrogen and oxygen pickup and the steam reaction in
copper melts, deoxidizers used in Cu-Ni (Mn, Ti, Mg, B, Li, P) and their
effect on later weld or AM porosity, and how master alloys (Cu-Ni, Cu-Fe,
Cu-Mn, Cu-Al) are used to reach composition. Give typical composition losses
(e.g. Mn, Al volatilization or oxidation) if reported.

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


# Small-batch Cu–Ni and nickel–aluminum-bronze melting: evidence and recommendations

**Bottom line.** For a 0.1–1 kg, 1150–1300 °C induction melt intended for pre-alloyed powder, a **dry, high-purity, dense alumina crucible under dry argon** is a defensible *first trial*, not a literature-validated universal optimum. Compare it experimentally with a **stabilized-zirconia** crucible, especially for Al/Mn-bearing bronze. Minimize superheat and liquid hold time; use clean, dry charge and additions; sample the **charge, liquid/solidified alloy, and atomized powder separately** for composition and O/C/H. The sources below do not establish a best crucible—or quantitative carbon pickup, Al/Mn recovery, Hall flow, or powder oxygen—for these *specific* alloys in this *specific* atomizer. The recommendation is therefore a proposed qualification experiment, not an established recipe. (schwartz1953cruciblehandbooka pages 10-12, schwartz1953cruciblehandbooka pages 16-17, schwartz1953cruciblehandbooka pages 28-30, ciftcli2025alloydevelopmentfrom pages 1-3)

## 1. Crucibles and actual melt practice

**[CITE] [GAP] Schwartz, M. A., G. D. White and C. E. Curtis, *Crucible Handbook: A Compilation of Data on Crucibles Used for Calcining, Sintering, Melting, and Casting* (1953), DOI: 10.2172/4389738.** Process: refractory selection for **cast** metals, including induction melting; no specified Cu–Ni/NAB composition or corrosion test. Its comparative guidance is more useful here than an unsupported claim of alloy-specific chemical inertness:

| Candidate | Evidence-supported advantage and liability at the proposed temperatures |
|---|---|
| **Graphite** | Conductive, machinable and exceptionally thermal-shock tolerant; carbon can enter a melt, while graphite can reduce oxides and form carbides. Oxidation starts at approximately **500 °C** in an oxidizing environment. The handbook does **not** measure carbon pickup from 10–30 wt% Ni–Cu, nor prove that such pickup is inevitable. Treat graphite-contact time and measured carbon as experimental variables, particularly for Ni-bearing, Al-bearing melts. |
| **Clay–graphite** | Good shock tolerance and a conventional copper-alloy crucible, but its clay/silicate bond may introduce carbon and silicates, rehydrate when stored damp, and is reported in this handbook to have a **1200 °C** maximum. It is consequently not a safely qualified choice for a planned **1300 °C** hold merely because a foundry has used a differently rated commercial product. |
| **High-purity alumina** | A low-carbon starting choice: dense recrystallized alumina is reported at about **0.2% refractory porosity**; clay-bonded alumina offers better thermal-shock tolerance but contains silica-bearing bond. The handbook does not establish that Al/Mn-containing copper melts leave a particular alumina grade uncontaminated. Preheat and cool cautiously. |
| **Zirconia, not zircon** | Dense zirconia is a candidate without intentional C/SiO₂ bond; **unstabilized zirconia changes phase near 1100 °C with substantial volume change**, risking cracking during cycling. Use a suitably stabilized grade, noting that stabilizer chemistry can itself matter. **Zircon (ZrSiO₄)** is a different, comparatively shock-resistant material reported to withstand copper alloys, but introduces a potential silica source; do not label zircon and zirconia interchangeable. |
| **Magnesia** | Potential low-carbon, basic refractory; commercial clay-bonded grades can be porous (**15–20%**) or silica-bearing and are moisture-sensitive. No demonstrated superiority for the specified Cu–Ni/NAB melts was found. |
| **Boron nitride** | The handbook lists BN in connection with **boron**, not as a tested Cu–Ni/NAB induction crucible. Its compatibility, binder/BN-derived B or N pickup, manufacturability, and atomizer fit require direct testing; do not assert it is inert to molten Al/Mn-bearing bronze. |

These are **refractory properties, not deposit-porosity or corrosion measurements**. In particular, the available evidence does not prove that bulk Al or Mn in a dilute copper melt reduces Al₂O₃, ZrO₂ or MgO under the proposed argon conditions; it likewise does not establish that any is chemically nonreactive. Silica-containing clay, glazes and zircon, oxide films, and carbon-bearing surfaces are identifiable contamination *risks*. Examine used crucible walls and analyze melt inclusions and crucible-derived Si, Al, Zr, Mg, B and C rather than turning thermodynamic suspicion into a reported reaction. (schwartz1953cruciblehandbooka pages 9-10, schwartz1953cruciblehandbooka pages 10-12, schwartz1953cruciblehandbooka pages 16-17, schwartz1953cruciblehandbooka pages 17-19, schwartz1953cruciblehandbooka pages 19-20, schwartz1953cruciblehandbooka pages 20-23, schwartz1953cruciblehandbooka pages 28-30)

**[CITE] [NUMBERS] [GAP] Thongyothee, C. and S. Chareonvilisiri, “The Effect of Gas Venting on the Mechanical Properties of C95800 Aluminum Bronze Castings,” *Engineering, Technology & Applied Science Research* **15** (2025), 25068–25075. DOI: 10.48084/etasr.10993.** Process: **induction melt → sand cast**, *not* argon atomization. Commercial C95800 scrap was melted in a **SiC crucible**, **30 kg/charge**, approximately **1200–1250 °C**, in an **oxidizing** atmosphere; the reported specimen was Cu 76.57, Ni 4.16, Fe 3.81, Al 8.85, Mn 0.52 wt%. Charge and crucible were preheated/dried; a commercial degasser was added near 1200 °C, followed **5–10 min** later by a proprietary deoxidizing tube; flux was **0.25–0.5 wt%** of metal and the reported pour temperature **1250 ± 10 °C**. With mold venting, mean UTS was **590 MPa**, impact energy **13 J**, hardness **74 HRB** and elongation **15.3%**, versus **588 MPa, 10 J, 71 HRB and 15%** for the single unvented comparator. No quantified pore fraction, powder property or seawater test was reported. SiC is a *documented additional comparator*, not proof that a proprietary degassing/flux procedure transfers to a clean 0.1–1 kg argon melt. (thongyothee2025theeffectof pages 1-2, thongyothee2025theeffectof pages 2-4, thongyothee2025theeffectof pages 4-5, schwartz1953cruciblehandbooka pages 23-25)

**[CITE] [NUMBERS] [GAP] de Luca, R., P. H. T. do Nascimento, V. T. dos Santos, *et al.*, “Correlation of Solidification Thermal Variables with Microstructure and Hardness in CuMn11Al8Fe3Ni3 Manganese–Aluminum–Bronze Alloy,” *Materials* **18** (2025), 234. DOI: 10.3390/ma18020234.** Process: **muffle-furnace melt → directionally solidified cast**, not induction atomization. Approximately **2 kg** of nominal Cu–11Mn–8Al–3Fe–3Ni was held **10 min at 1250 °C** in a commercial *Salamander SiC/graphite* crucible. Measured incoming bar versus solidified ingot, in wt%, was **Mn 11.09→11.01, Al 8.96→8.93, Fe 2.39→2.37, Ni 1.61→1.59**. Those are *observed differences in one experiment*, **not general volatilization-loss allowances**; the authors describe no meaningful loss relative to specification. Cooling rates ranged **13.03→0.23 °C/s** and corresponding macrohardness **199→184 HB**. No corrosion or atomized-powder measurements. This shows that a carbon-containing crucible has actually been used with a high-Mn/Al bronze; it does not establish its carbon-transfer rate. (luca2025correlationofsolidification pages 4-6, luca2025correlationofsolidification pages 1-3, luca2025correlationofsolidification pages 3-4, luca2025correlationofsolidification pages 6-9)

**[CITE] [NUMBERS] [GAP] Grobecker, D. W., D. T. Doll and J. M. Taub, *Low-Copper Nickel-Silver of Improved Chemical and Physical Properties*, Los Alamos report LA-1321 (1951). DOI: 10.2172/4409730.** Process: **induction melt → cast**, but the alloy was approximately **Cu 40–Ni 32–Zn 28 wt%**, emphatically **not** C71500 or NAB. Commercial **clay–graphite** crucibles held **15–300 lb** charges. Cu–Ni charge alloy dissolved more readily than elemental Ni shot/powder; a covered, approximately **1175 °C** melt used a premelted **52% soda ash/27% borax/21% silica** slag. The investigators added nominal **0.02% P as Cu–P, 0.1% Mn and 0.5% Mg** during melt refining. Under *that zinc-bearing, slag-covered procedure*, cast Zn measured **0.25–0.75 percentage points below the charge**. This is evidence for charge design, deoxidation practice and composition checks—not an Al or Mn loss factor transferable to argon atomization. (grobecker1951lowcoppernickelsilverof pages 1-8, grobecker1951lowcoppernickelsilverof pages 8-24)

**[CITE] [GAP] Ciocan, A., “Versatility of Nickel-Aluminium Bronzes as Wear Resisting Materials,” *Annals of ‘Dunărea de Jos’ University of Galați, Fascicle IX: Metallurgy and Materials Science* **2** (2011), 5–13; DOI: *not identified*.** Process: **graphite-crucible furnace → cast**, with separate arc-weld overlays; a bearing bronze contained **Al 7.2, Ni 1.2, Fe 1.2, Mn 1.32 wt%**, Cu balance. The report describes argon bubbled through the bath (**0.2 Nm³**, reported gas pressure **0.3–0.5 daN/cm²**), charcoal cover, Cu–P deoxidation and casting at **≤1150 °C**. No C/O pickup, seawater corrosion current or powder data. This is a real lower-Ni melt precedent, *not* a validated marine-equivalent-to-C71500 result. (ciocan2011versatilityofnickelaluminium pages 3-5)

**Practical charge sequence, identified as an inference rather than a cited universal formula.** First balance the target composition from verified feedstock assays and master-alloy assays. Use clean Cu plus a **Cu–Ni master alloy** or clean pre-alloyed Cu–Ni stock as the base; introduce difficult-to-dissolve Fe through an assayed **Cu–Fe** addition rather than assuming Fe chips will dissolve during a short hold; add **Cu–Mn and Cu–Al** after the base has melted and limit their subsequent oxygen exposure and hold. If a target addition is supplied as a master alloy of mass fraction *f*, its *first-pass* charge mass is target added-element mass/*f*, corrected for the Cu introduced, initial Cu/Ni/Fe/Mn/Al already present, and **experimentally measured** recovery. A Cu–Ni charging benefit and the general utility of separately assayed master alloys are documented, but this precise four-master-alloy sequence has **not** been validated in the retrieved 0.1–1 kg NAB/Cu–Ni induction-atomization literature. Do not transfer the documented **Zn** loss above to Mn or Al, or claim Al volatilization has been measured here. (grobecker1951lowcoppernickelsilverof pages 1-8, grobecker1951lowcoppernickelsilverof pages 8-24, m.sadayappan2005grainrefinementof pages 10-14, m.sadayappan2005grainrefinementof pages 23-28, luca2025correlationofsolidification pages 6-9)

## 2. Gas control, deoxidants and downstream fusion defects

**[CITE] [GAP] Lancaster, J. F., “Non-ferrous metals,” in *Metallurgy of Welding* (1999), pp. 197–223. DOI: 10.1007/978-94-010-9506-8_9.** Process: **fusion welding** of copper and Cu–Ni; a mechanism/source, **not** a controlled atomization experiment. Copper oxide can react with hydrogen above approximately **500 °C** by **Cu₂O + H₂ → 2Cu + H₂O**; trapped steam can produce weld-pool pores and grain-boundary fissuring in heated oxygen-bearing parent copper. However, Lancaster explicitly cautions that measured weld-pore gas can be largely **hydrogen**, and that the exact contribution of steam to inert-gas copper-weld porosity is unresolved. Dry argon alone cannot undo O/H already in scrap, master alloys, a damp crucible or feedstock powder. The same account says **Cu–Ni, unlike inherently deoxidizing Al bronze, requires deoxidized filler**; **Ti** is an appropriate Cu–Ni filler deoxidant. In the wider copper-welding discussion, Si–Mn or Ti–Al filler combinations are used where P alone is inadequate: that does **not** establish Si or Al as acceptable intentional additions to every proposed seawater alloy. (lancaster1999nonferrousmetals pages 9-12, lancaster1999nonferrousmetals pages 12-15)

**Deoxidizer choice is also an alloy-design decision.** **Mn** is both a Cu–Ni specification addition and a practical oxygen scavenger; **Ti** is demonstrated in a Cu–Ni weld-wire formulation. **Mg** and **P** occur in a documented Cu–Ni–Zn casting treatment, but its large nominal Mg addition and residual-P behavior must *not* be copied into a marine pre-alloyed powder without chemistry/porosity/corrosion testing. **B** has been added to copper melts via Cu–B master alloy for grain refinement; it can yield hard particles in some Fe-containing *brasses*, which is not proof of the same outcome in Cu–Ni or NAB. No retrieved controlled comparison establishes useful residual levels, deoxidation efficiency or later laser-DED pore rates for **B, Li, Mg or P in the proposed compositions**. Treat Li and B as unqualified candidates, not established Cu–Ni atomizer recipes. Excess reactive addition can convert dissolved O into retained oxides/inclusions rather than guarantee a pore-free powder or deposit. (grobecker1951lowcoppernickelsilverof pages 1-8, grobecker1951lowcoppernickelsilverof pages 8-24, m.sadayappan2005grainrefinementof pages 8-10, m.sadayappan2005grainrefinementof pages 23-28, song2024microstructuresandcorrosion pages 1-2, lancaster1999nonferrousmetals pages 9-12, lancaster1999nonferrousmetals pages 12-15)

**[CITE] [NUMBERS] [GAP] Tumuluru, M. and E. F. Nippes, “Weld Ductility Studies in a Tin-Modified Copper-Nickel Alloy,” *Welding Journal*, Welding Research Supplement (May **1990**, pp. 197s–202s); DOI: *not identified*.** Process: **GTA and plasma-transferred-arc welding**, not DED, on **Cu–9Ni–6Sn wt%**—the Sn makes this an imperfect marine Cu–Ni analogue. Trials compared no addition with **0.1 wt% Mn + 0.01 wt% P**, with/without 0.20 wt% Zn. In one unmodified heat, gas analyses were **O 6 ppm/H 0.14 ppm as cast**, **O 7/H 0.18 ppm homogenized**, and **O 7/H 0.54 ppm in the GTA weld**; N was **<1 ppm**. Mn/P-bearing material showed reduced observed porosity and improved bend behavior, but some GTA welds still cracked; the principal cracking mechanism involved Sn-rich grain-boundary gamma phase. In this particular plasma-welding trial, **Ar–5% H₂** reduced visible pores versus Ar alone—*not* a recommendation to put hydrogen into atomization argon. The article’s catalog metadata gives 1988 whereas its accessible pages say **May 1990**; the latter is used here. No quantified percent porosity is established. (tumuluru1988weldductilitystudies pages 1-2, tumuluru1988weldductilitystudies pages 2-4, tumuluru1988weldductilitystudies pages 4-5)

**[CITE] [NUMBERS] [GAP] Ciftcli, J., T. Choma, B. Morończyk, *et al.*, “Alloy Development from Sustainable Materials—Close-Loop of Materials Using Ultrasonic Atomization,” *Journal of the Japan Society of Powder and Powder Metallurgy* **72** (2025), S729–S735. DOI: 10.2497/jjspm.15E-SIS13-03.** Process: **induction melting → ultrasonic powder atomization**, with a copper-alloy stream illustrated but quantitative powder measurements supplied for *other* alloys. Describes rePOWDER, an argon-driven pour from crucible to a **60 kHz** vibrating blade, and small feedstock quantities; a recycled Ti-alloy trial measured approximately **220 ppm oxygen pickup**, **<600 ppm total O**, with powder **D10/D50/D90 = 36/49/118 µm by volume**. These figures are **Ti-alloy results, not Cu–Ni or NAB powder targets**. The article also observes volatile-element problems in a Mg–Zn system; it provides no measured Al/Mn evaporation rate from the candidate Cu alloys. (ciftcli2025alloydevelopmentfrom pages 1-3, ciftcli2025alloydevelopmentfrom pages 3-6)

## 3. Benchmarks and prior-art boundaries—not substitutes for the requested melt data

**[CITE] [NUMBERS] [NOVELTY-RISK] [GAP] Song, J., X. A. Jimenez, A. C. To and Y. Fu, “Microstructures and Corrosion Properties of Wire Arc Additive Manufactured Copper–Nickel Alloys,” *Materials* **17** (2024), 876. DOI: 10.3390/ma17040876.** Process: **wire-arc DED/WAAM (CMT), not powder laser DED**. Nominal 70/30 wire actually analyzed **Cu 67.5/Ni 30/Mn 0.7/Fe 0.55/Ti 0.25/Si 0.1 wt%**; wrought C71500 comparator was **Cu 68.046/Ni 30.46/Mn 0.73/Fe 0.56 wt%**. Electrochemistry used naturally aerated **3.5 wt% NaCl at room temperature after 3 h open circuit**, on ground specimens; *not* ASTM D1141 seawater or 30-day immersion. EIS film resistance for best WAAM specimen **6** was **1.40 × 10⁵ Ω (XY), 1.66 × 10⁵ Ω (YZ)** versus wrought **1.08 × 10⁵ and 1.18 × 10⁵ Ω**; these are **absolute fitted film resistances, not Ω·cm²**. At least one other WAAM condition underperformed wrought. Optical examination reported **no observed pores or cracks**, not a measured 100% density; no quantitative *i*corr or long-term rate is established in the cited passage. The deposit showed up to approximately **20% relative Ni contrast** between dendritic core and interdendritic region. **Novelty risk:** “as-deposited Cu–Ni outperforming wrought 70/30 in short NaCl electrochemistry” is already demonstrated for *wire* DED. **Remaining gap:** single-stream pre-alloyed powder laser DED, lower Ni, repaired Cu–Ni and cast NAB interfaces, and matched long-duration marine testing. (song2024microstructuresandcorrosion pages 1-2, song2024microstructuresandcorrosion pages 13-14, song2024microstructuresandcorrosion pages 2-5, song2024microstructuresandcorrosion pages 10-13, song2024microstructuresandcorrosion media 4cae0ca0)

**[CITE] [NUMBERS] [NAVY] [GAP] Lewis, R. O. and F. LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, US Department of Energy report (1981). DOI: 10.2172/6255887.** Process: literature synthesis of **wrought/installed Cu–Ni** and cast marine alloys, not DED; **DOE funding**, with naval-vessel service discussed, so [NAVY] denotes application, **not Navy funding**. Commercial **C71500 ≈ Cu–30Ni–0.4–0.7Fe wt%** and **C70600 ≈ Cu–10Ni–1.0–1.8Fe** showed reported marine general-corrosion rates approximately **2.5–12.7 µm/year**; after **14–16 years** in quiescent/low-flow seawater, rates were **<2.5 µm/year**. These are **service/long-term natural-seawater figures**, *not* a legitimate numerical threshold for a 30-day 3.5% NaCl polarization test. Literature discussed in the report found approximately **1.3–2.0 wt% Fe** could bring **90/10 Cu–Ni** impingement behavior toward 70/30 in particular tests, whereas excessive Fe can increase crevice/pitting problems; Cr-modified alloys can improve high-flow impingement but worsen certain quiet-water localized-attack outcomes. No transferable single optimal Fe/Cr composition follows without matching seawater flow and exposure. (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 14-17)

**[CITE] [NUMBERS] [NAVY] [GAP] King, S., *The Hot Isostatic Processing Characteristics of 70/30 Cupronickel Castings*, PhD thesis, Sheffield Hallam University (1992), institutional archive; DOI: *not identified*.** Process: **cast** UK naval **70Cu–30Ni–Cr–Si** cupronickel and HIP, *not* wrought C71500 or as-deposited laser DED. The thesis acknowledges UK Ministry of Defence corrosion testing and reports that UK naval casting specifications restricted repair welding on seawater-wetted faces; welded NAB heat-affected zones were susceptible to preferential phase attack. Reported **cast** 70/30 Cr–Si alloy mechanical-property ranges were **305–374 MPa proof stress, 487–584 MPa UTS and 19–24% elongation**. A related cast IN768 natural-seawater exposure in **Langstone Harbour for one year** gave **0.02 mm/year average weight-loss rate** and **0.05 mm/year maximum metallographic attack**; a **3 m/s** submarine auxiliary seawater system gave an inferred **0.05 mm/year** after film development. These are *different materials/conditions* from wrought C71500 and must be labeled accordingly. This is a particularly relevant **[NAVY]** warning that repair-interface/HAZ integrity, not merely deposit *i*corr, determines acceptability. (king1992thehotisostatic pages 1-10, king1992thehotisostatic pages 21-27, king1992thehotisostatic pages 27-32, king1992thehotisostatic pages 32-38, king1992thehotisostatic pages 43-49)

**[CITE] [NUMBERS] [NOVELTY-RISK] [GAP] Huo, R., Z. Wang, M. Wang, *et al.*, “Modulating Heat Input to Optimize Corrosion Resistance of Nickel–Aluminum Bronze Manufactured by Cold Metal Transfer Additive Manufacturing,” *Materials* **18** (2025), 2205. DOI: 10.3390/ma18102205.** Process: **wire-arc DED/CMT**, *not powder laser DED*; wire **Cu balance, Al 8.73, Fe 5.90, Ni 4.52, Mn 1.39 wt%**, deposited onto a **Cu–8.62Al–2.32Fe substrate containing 0.005 Ni**, *not cast NAB*. At **243.8→644.7 J/mm** heat input, measured as-deposited corrosion current in aerated **3.5 wt% NaCl, 25 ± 5 °C, 1 h OCP stabilization** changed **2.56 ± 0.04→7.52 ± 0.07 µA/cm²**; reported Tafel potentials **−269.61 ± 40→−700.94 ± 15 mV versus SCE**. The results passage gives measured hardness **192.4 ± 6.9→166.9 ± 0.3 HV**, notwithstanding different values stated in the abstract; the body values are preferred. *No 30-day immersion, natural seawater, wrought C71500 comparator or measured density fraction.* **Novelty risk:** “as-deposited NAB corrosion improves with optimized AM thermal input” is already prior art, although in a different process/substrate. (huo2025modulatingheatinput pages 10-13, huo2025modulatingheatinput pages 4-5, huo2025modulatingheatinput pages 7-10, huo2025modulatingheatinput pages 2-4)

**[CITE] [NUMBERS] [NOVELTY-RISK] [GAP] Nemani, A. V., M. Ghaffari, K. S. Bokati, *et al.*, “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites: A Comprehensive Review,” *Journal of Manufacturing and Materials Processing* **8** (2024), 54. DOI: 10.3390/jmmp8020054.** Process: review, with separate **laser metal deposition/blown-powder laser DED, LPBF and WAAM** comparisons. It identifies Li, B., H. Zheng, C. Han and K. Zhou, “Nanotwins-containing microstructure and superior mechanical strength of a Cu–9Al–5Fe–5Ni alloy additively manufactured by laser metal deposition,” *Additive Manufacturing* **39** (2021), 101825, DOI **10.1016/j.addma.2021.101825**: as-built laser-DED NAB yielded reported **593–713 MPa yield strength, 769–949 MPa UTS, 10–12% elongation**, with no seawater corrosion benchmark supplied in the review. It identifies Barr, C., A. Pateras, A. Molotnikov, D. Clarke and M. Brandt, “Effect of composition on the tensile and corrosion performance of nickel aluminium bronze produced via laser powder bed fusion,” *Additive Manufacturing* **54** (2022), 102771, DOI **10.1016/j.addma.2022.102771**: **LPBF**, not DED, with feedstocks **Cu–10.2Al–4.8Fe–5.0Ni–0.2Si** and **Cu–9.0Al–4.0Fe–4.6Ni–1.9Mn wt%**; the review reports about **1120 MPa UTS but 3% elongation** for as-built C63000, without a directly extractable corrosion-current value in the retrieved material. It also identifies Yao, C.-L., H.-S. Kang, K.-Y. Lee, J.-G. Zhai and D.-S. Shim, “A Study on Mechanical Properties of CuNi2SiCr Layered on Nickel–Aluminum Bronze via Directed Energy Deposition,” *Journal of Materials Research and Technology* **18** (2022), 5337–5361, DOI: **not independently verified here**, and Yao, C.-L. and D.-S. Shim, “Corrosive Properties of CuNi2SiCr Fabricated Through Directed Energy Deposition on a Nickel-Aluminum Bronze Substrate,” *Journal of Alloys and Compounds* **918** (2022), 165776, DOI **10.1016/j.jallcom.2022.165776**. These two works directly overlap **laser-powder DED repair of cast NAB**; the review flags porosity and poor mechanical suitability of the CuNi2SiCr deposit. **The original Yao articles were not available for verifying powder preparation, numerical corrosion metrics, or whether feed was pre-alloyed: do not claim these specifics.** (nemani2024advancementsinadditive pages 74-79, nemani2024advancementsinadditive pages 113-114, nemani2024advancementsinadditive pages 60-62, nemani2024advancementsinadditive pages 79-83)

**Research gap, stated narrowly.** The retrieved evidence does **not** supply a controlled 0.1–1 kg argon induction crucible comparison for both targeted alloy families; quantitatively validated graphite-to-Ni-melt carbon pickup; independently transferable Mn/Al volatilization or oxidation allowances; or a common **as-deposited pre-alloyed single-stream powder laser-DED** data set reporting powder size/Hall flow/apparent density/O, density and cracking on both cast NAB and wrought Cu–Ni, and matched long-duration flowing seawater performance against wrought C71500. Nor can the studies above support numerical ASTM D1141-versus-natural-seawater equivalence. These are genuine validation opportunities, **not** proof that no unlocated publication exists. (grobecker1951lowcoppernickelsilverof pages 1-8, song2024microstructuresandcorrosion pages 2-5, nemani2024advancementsinadditive pages 102-105, nemani2024advancementsinadditive pages 79-83, ciftcli2025alloydevelopmentfrom pages 1-3)

## Top 5 things the PI should know

1. **Qualify crucible × alloy experimentally.** Begin with high-purity alumina and stabilized zirconia; include graphite or a suitably rated SiC/graphite commercial comparator only if C, inclusions and product chemistry are measured. The handbook’s clay–graphite **1200 °C** limit cannot be extrapolated to a **1300 °C** trial. (schwartz1953cruciblehandbooka pages 10-12, schwartz1953cruciblehandbooka pages 16-17, schwartz1953cruciblehandbooka pages 28-30, luca2025correlationofsolidification pages 4-6)
2. **The charge-to-powder chemistry is a measured link in the model, not a nominal input.** Assay master alloys and metal before/after atomization; no credible general **Mn or Al loss percentage** for these small Cu-alloy melts was established. The one documented high-Mn bronze trial found only small before/after differences under its own conditions. (grobecker1951lowcoppernickelsilverof pages 1-8, ciftcli2025alloydevelopmentfrom pages 1-3, luca2025correlationofsolidification pages 3-4, luca2025correlationofsolidification pages 6-9)
3. **Control H and O before trying to optimize DED.** Moist charge, refractory and gas handling affect melt/powder quality; Cu–Ni needs weld-compatible deoxidation, but nominal P/Mg/B/Li additions cannot be assumed to prevent later laser pores or preserve marine corrosion resistance. (thongyothee2025theeffectof pages 1-2, lancaster1999nonferrousmetals pages 9-12, lancaster1999nonferrousmetals pages 12-15, tumuluru1988weldductilitystudies pages 4-5)
4. **Position novelty against actual close prior art.** Wire-arc 70/30 Cu–Ni already outperformed wrought C71500 in a **3 h/3.5% NaCl** comparison, and powder laser DED on cast NAB with CuNi2SiCr has already been published. Distinguish the proposal by its measured **pre-alloyed-powder production → laser DED → both repair interfaces → as-deposited, matched marine durability** pipeline, not by claiming copper-alloy repair or short-test improvement is new. (song2024microstructuresandcorrosion pages 1-2, song2024microstructuresandcorrosion pages 10-13, nemani2024advancementsinadditive pages 113-114, song2024microstructuresandcorrosion media 4cae0ca0)
5. **Make the acceptance test marine-relevant.** Test matched wrought C71500 in the same bath, surface finish, exposure time and flow, while separately scoring repair-interface cracking, porosity, galvanic effects and maximum selective-attack depth. Neither an isolated *i*corr nor hardness establishes seawater service equivalence; historical naval experience specifically warns about welded HAZ attack. (lewis1981evaluationofcoppernickel pages 14-17, king1992thehotisostatic pages 27-32, king1992thehotisostatic pages 43-49, huo2025modulatingheatinput pages 10-13)

References

1. (schwartz1953cruciblehandbooka pages 10-12): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

2. (schwartz1953cruciblehandbooka pages 16-17): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

3. (schwartz1953cruciblehandbooka pages 28-30): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

4. (ciftcli2025alloydevelopmentfrom pages 1-3): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72(Supplement):S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

5. (schwartz1953cruciblehandbooka pages 9-10): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

6. (schwartz1953cruciblehandbooka pages 17-19): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

7. (schwartz1953cruciblehandbooka pages 19-20): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

8. (schwartz1953cruciblehandbooka pages 20-23): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

9. (thongyothee2025theeffectof pages 1-2): Chawanan Thongyothee and Sombun Chareonvilisiri. The effect of gas venting on the mechanical properties of c95800 aluminum bronze castings. Engineering, Technology &amp; Applied Science Research, Aug 2025. URL: https://doi.org/10.48084/etasr.10993, doi:10.48084/etasr.10993. This article has 1 citations and is from a peer-reviewed journal.

10. (thongyothee2025theeffectof pages 2-4): Chawanan Thongyothee and Sombun Chareonvilisiri. The effect of gas venting on the mechanical properties of c95800 aluminum bronze castings. Engineering, Technology &amp; Applied Science Research, Aug 2025. URL: https://doi.org/10.48084/etasr.10993, doi:10.48084/etasr.10993. This article has 1 citations and is from a peer-reviewed journal.

11. (thongyothee2025theeffectof pages 4-5): Chawanan Thongyothee and Sombun Chareonvilisiri. The effect of gas venting on the mechanical properties of c95800 aluminum bronze castings. Engineering, Technology &amp; Applied Science Research, Aug 2025. URL: https://doi.org/10.48084/etasr.10993, doi:10.48084/etasr.10993. This article has 1 citations and is from a peer-reviewed journal.

12. (schwartz1953cruciblehandbooka pages 23-25): M. A. Schwartz, G. D. White, and C. E. Curtis. Crucible handbook: a compilation of data on crucibles used for calcining, sintering, melting, and casting. ArXiv, Apr 1953. URL: https://doi.org/10.2172/4389738, doi:10.2172/4389738. This article has 7 citations.

13. (luca2025correlationofsolidification pages 4-6): Ricardo de Luca, Paulo Henrique Tedardi do Nascimento, Vinicius Torres dos Santos, Marcio Rodrigues da Silva, Flavia Gonçalves Lobo, Rogerio Teram, Mauricio Silva Nascimento, Antonio Augusto Couto, Anibal de Andrade Mendes Filho, and Givanildo Alves dos Santos. Correlation of solidification thermal variables with microstructure and hardness in cumn11al8fe3ni3 manganese–aluminum–bronze alloy. Materials, 18:234, Jan 2025. URL: https://doi.org/10.3390/ma18020234, doi:10.3390/ma18020234. This article has 1 citations.

14. (luca2025correlationofsolidification pages 1-3): Ricardo de Luca, Paulo Henrique Tedardi do Nascimento, Vinicius Torres dos Santos, Marcio Rodrigues da Silva, Flavia Gonçalves Lobo, Rogerio Teram, Mauricio Silva Nascimento, Antonio Augusto Couto, Anibal de Andrade Mendes Filho, and Givanildo Alves dos Santos. Correlation of solidification thermal variables with microstructure and hardness in cumn11al8fe3ni3 manganese–aluminum–bronze alloy. Materials, 18:234, Jan 2025. URL: https://doi.org/10.3390/ma18020234, doi:10.3390/ma18020234. This article has 1 citations.

15. (luca2025correlationofsolidification pages 3-4): Ricardo de Luca, Paulo Henrique Tedardi do Nascimento, Vinicius Torres dos Santos, Marcio Rodrigues da Silva, Flavia Gonçalves Lobo, Rogerio Teram, Mauricio Silva Nascimento, Antonio Augusto Couto, Anibal de Andrade Mendes Filho, and Givanildo Alves dos Santos. Correlation of solidification thermal variables with microstructure and hardness in cumn11al8fe3ni3 manganese–aluminum–bronze alloy. Materials, 18:234, Jan 2025. URL: https://doi.org/10.3390/ma18020234, doi:10.3390/ma18020234. This article has 1 citations.

16. (luca2025correlationofsolidification pages 6-9): Ricardo de Luca, Paulo Henrique Tedardi do Nascimento, Vinicius Torres dos Santos, Marcio Rodrigues da Silva, Flavia Gonçalves Lobo, Rogerio Teram, Mauricio Silva Nascimento, Antonio Augusto Couto, Anibal de Andrade Mendes Filho, and Givanildo Alves dos Santos. Correlation of solidification thermal variables with microstructure and hardness in cumn11al8fe3ni3 manganese–aluminum–bronze alloy. Materials, 18:234, Jan 2025. URL: https://doi.org/10.3390/ma18020234, doi:10.3390/ma18020234. This article has 1 citations.

17. (grobecker1951lowcoppernickelsilverof pages 1-8): LOW-COPPER NICKEL-SILVER OF IMPROVED CHEMICAL AND PHYSICAL PROPERTIES

18. (grobecker1951lowcoppernickelsilverof pages 8-24): LOW-COPPER NICKEL-SILVER OF IMPROVED CHEMICAL AND PHYSICAL PROPERTIES

19. (ciocan2011versatilityofnickelaluminium pages 3-5): A CIOCAN. Versatility of nickel-aluminium bronzes as wear resisting materials. Unknown journal, 2011.

20. (m.sadayappan2005grainrefinementof pages 10-14): Grain Refinement of Permanent Mold Cast Copper Base Alloys This article has 58 citations.

21. (m.sadayappan2005grainrefinementof pages 23-28): Grain Refinement of Permanent Mold Cast Copper Base Alloys This article has 58 citations.

22. (lancaster1999nonferrousmetals pages 9-12): J. F. Lancaster. Non-ferrous metals. ArXiv, pages 197-223, Jan 1999. URL: https://doi.org/10.1007/978-94-010-9506-8\_9, doi:10.1007/978-94-010-9506-8\_9. This article has 7 citations.

23. (lancaster1999nonferrousmetals pages 12-15): J. F. Lancaster. Non-ferrous metals. ArXiv, pages 197-223, Jan 1999. URL: https://doi.org/10.1007/978-94-010-9506-8\_9, doi:10.1007/978-94-010-9506-8\_9. This article has 7 citations.

24. (m.sadayappan2005grainrefinementof pages 8-10): Grain Refinement of Permanent Mold Cast Copper Base Alloys This article has 58 citations.

25. (song2024microstructuresandcorrosion pages 1-2): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

26. (tumuluru1988weldductilitystudies pages 1-2): M Tumuluru and EF Nippes. Weld ductility studies in a tin-modified copper-nickel alloy. Unknown journal, 1988.

27. (tumuluru1988weldductilitystudies pages 2-4): M Tumuluru and EF Nippes. Weld ductility studies in a tin-modified copper-nickel alloy. Unknown journal, 1988.

28. (tumuluru1988weldductilitystudies pages 4-5): M Tumuluru and EF Nippes. Weld ductility studies in a tin-modified copper-nickel alloy. Unknown journal, 1988.

29. (ciftcli2025alloydevelopmentfrom pages 3-6): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72(Supplement):S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 7 citations.

30. (song2024microstructuresandcorrosion pages 13-14): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

31. (song2024microstructuresandcorrosion pages 2-5): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

32. (song2024microstructuresandcorrosion pages 10-13): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

33. (song2024microstructuresandcorrosion media 4cae0ca0): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

34. (lewis1981evaluationofcoppernickel pages 17-19): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

35. (lewis1981evaluationofcoppernickel pages 14-17): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

36. (king1992thehotisostatic pages 1-10): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

37. (king1992thehotisostatic pages 21-27): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

38. (king1992thehotisostatic pages 27-32): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

39. (king1992thehotisostatic pages 32-38): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

40. (king1992thehotisostatic pages 43-49): S King. The hot isostatic processing characteristics of 70/30 cupronickel castings. Unknown journal, 1992.

41. (huo2025modulatingheatinput pages 10-13): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

42. (huo2025modulatingheatinput pages 4-5): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

43. (huo2025modulatingheatinput pages 7-10): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

44. (huo2025modulatingheatinput pages 2-4): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

45. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

46. (nemani2024advancementsinadditive pages 113-114): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

47. (nemani2024advancementsinadditive pages 60-62): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

48. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.

49. (nemani2024advancementsinadditive pages 102-105): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 99 citations.
