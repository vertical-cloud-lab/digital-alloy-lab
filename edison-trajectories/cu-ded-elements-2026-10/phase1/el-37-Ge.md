<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: be061b72-07f4-4bf6-89dc-c581dca1e992
- Submitted: 2026-10-17T19:01:03Z
- Fetched: 2026-10-17T19:23:04Z (status: success)
- Raw trajectory JSON: ../raw/el-37-Ge.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

ELEMENT UNDER REVIEW: Ge (solid solution). Cu-Ge alpha solid solution; germanium makes silver alloys tarnish resistant; critical mineral; any corrosion data in chloride.

Answer for Ge specifically, not for copper alloys in general:
1. ROLE: what Ge does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ge ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ge changes corrosion of
   copper alloys in natural or substitute seawater or 3.5 wt% NaCl (corrosion
   rate, Ecorr, film resistance, pitting, crevice, dealloying, erosion-
   corrosion and velocity limits). Give the range where it helps and where it
   harms.
3. DED AND WELDING: effect on solidification cracking, liquation cracking in
   reheated layers, porosity, evaporation or oxidation loss under a laser,
   and on dilution into cast NAB or wrought Cu-Ni repair substrates. Use
   welding and cladding literature (ERCuNi, ERCuAl-A2, ERCuNiAl, ERCuMnNiAl
   fillers) where AM data are missing, and say so.
4. POWDER MAKING: problems in induction melting and atomization (oxidation,
   reaction with alumina, zirconia or graphite crucibles or with a titanium-
   alloy or molybdenum sonotrode, vapor loss, effect on liquidus and surface
   tension).
5. PHASE DIAGRAM AND CALPHAD: maximum solid solubility in Cu (wt%, and the
   temperature), intermetallics and invariant reactions in Cu-Ge, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ge, Cu-Ni-Ge and Cu-Al-Ge are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ge in the alloy (Cu balance):
   a. DECISION: INCLUDE as a designed addition, LIMIT as an impurity only, or
      EXCLUDE, with a one-paragraph reason.
   b. If INCLUDE: a CONSERVATIVE upper bound (from established commercial or
      Navy alloys, or demonstrated AM or cladding), a NON-CONSERVATIVE upper
      bound (defensible but aggressive: experimental alloys, solubility or
      phase-boundary limits, the liquidus limit), and a FUNCTIONAL FLOOR (the
      smallest content with a measurable effect). Say which family (Cu-Ni,
      aluminum bronze, or both) each bound applies to.
   c. If LIMIT: the maximum tolerable content (wt% or ppm) in DED powder and
      deposit, and the specification or study it comes from.
   d. The failure mode that sets each bound.
8. INTERACTIONS for a later joint-constraint analysis: sums or ratios with Ni,
   Fe, Mn, Al or other elements; elements that Ge neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ge | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal. It designs new
pre-alloyed copper alloy powders for single-stream blown-powder laser directed
energy deposition (DED). Targets: deposits that are dense and crack-free, both
built on themselves and deposited on cast nickel-aluminum bronze (NAB, C95800)
and wrought Cu-Ni (repair), and that resist seawater AS DEPOSITED (no
post-build heat treatment) at least as well as wrought 70-30 Cu-Ni (C71500).
Lower nickel content is a secondary objective (nickel and, since 2025, copper
are US critical minerals). Powder is made in-house: about 0.5 kg charges of
oxygen-free copper plus pure metals or master alloys are induction melted in a
ceramic crucible (alumina or zirconia) under argon on an AMAZEMET rePOWDER
ultrasonic atomizer, whose induction module reaches about 1,300 C, so alloys
whose liquidus is above about 1,200-1,250 C cannot be atomized with useful
superheat. DED uses an infrared fiber laser (about 1.07 um) with argon
shielding. Corrosion screen: open-circuit potential, linear polarization,
impedance and cyclic polarization in ASTM D1141 substitute ocean water, then
30-day immersion with depth of selective attack. CALPHAD: Thermo-Calc (TCCU
copper database) and pycalphad. The composition search space (elements and
their bounds, in wt%, copper as balance) is being chosen the way an earlier
aluminum alloy project chose its 15-element palette: one literature question
per element, asking for a conservative and a non-conservative bound and the
failure modes that set them. The search covers both copper-nickel and
aluminum bronze families and anything between or beyond them that the
evidence supports.

ELEMENT UNDER REVIEW: Ge (solid solution). Cu-Ge alpha solid solution; germanium makes silver alloys tarnish resistant; critical mineral; any corrosion data in chloride.

Answer for Ge specifically, not for copper alloys in general:
1. ROLE: what Ge does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Ge ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Ge changes corrosion of
   copper alloys in natural or substitute seawater or 3.5 wt% NaCl (corrosion
   rate, Ecorr, film resistance, pitting, crevice, dealloying, erosion-
   corrosion and velocity limits). Give the range where it helps and where it
   harms.
3. DED AND WELDING: effect on solidification cracking, liquation cracking in
   reheated layers, porosity, evaporation or oxidation loss under a laser,
   and on dilution into cast NAB or wrought Cu-Ni repair substrates. Use
   welding and cladding literature (ERCuNi, ERCuAl-A2, ERCuNiAl, ERCuMnNiAl
   fillers) where AM data are missing, and say so.
4. POWDER MAKING: problems in induction melting and atomization (oxidation,
   reaction with alumina, zirconia or graphite crucibles or with a titanium-
   alloy or molybdenum sonotrode, vapor loss, effect on liquidus and surface
   tension).
5. PHASE DIAGRAM AND CALPHAD: maximum solid solubility in Cu (wt%, and the
   temperature), intermetallics and invariant reactions in Cu-Ge, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Ge, Cu-Ni-Ge and Cu-Al-Ge are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Ge in the alloy (Cu balance):
   a. DECISION: INCLUDE as a designed addition, LIMIT as an impurity only, or
      EXCLUDE, with a one-paragraph reason.
   b. If INCLUDE: a CONSERVATIVE upper bound (from established commercial or
      Navy alloys, or demonstrated AM or cladding), a NON-CONSERVATIVE upper
      bound (defensible but aggressive: experimental alloys, solubility or
      phase-boundary limits, the liquidus limit), and a FUNCTIONAL FLOOR (the
      smallest content with a measurable effect). Say which family (Cu-Ni,
      aluminum bronze, or both) each bound applies to.
   c. If LIMIT: the maximum tolerable content (wt% or ppm) in DED powder and
      deposit, and the specification or study it comes from.
   d. The failure mode that sets each bound.
8. INTERACTIONS for a later joint-constraint analysis: sums or ratios with Ni,
   Fe, Mn, Al or other elements; elements that Ge neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Ge | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Ge in copper-alloy powder for marine laser DED

**Decision — INCLUDE, but only as an exploratory Al-bronze-family variable.** [CITE] [GAP] The strongest application-relevant observation is reduced short-duration chloride-jet loss in a Ge-bearing, NAB-like powder-metallurgy alloy. A separate, second-hand report describes lower electrochemical corrosion rate in Ge-bearing Cu–Al–Ni shape-memory alloys. Neither establishes that Ge *caused* the improvement, survives atomization and DED without loss, prevents cracking, or produces an **as-deposited** coating competitive with wrought C71500. There is no comparable Ge-specific evidence for Cu–Ni repair alloy. Accordingly, Ge merits a small, controlled experimental branch, not a baseline design assumption. (aslan2020effectofalloying pages 13-16, aslan2020effectofalloying pages 4-7, dawood2020areviewof pages 5-8)

## 1. Role and existing alloys

[CITE] [NUMBERS] In Cu-rich Cu–Ge, Ge can enter the α-Cu solid solution; at greater concentrations, the assessed binary system contains the Cu-rich ξ phase and the ε, η/Cu₃Ge, and θ phases. These are **possible phase-boundary hazards**, not precipitates identified in the proposed dilute DED alloys. An experimental NAB-like material was specified as Cu–9.5 wt% Al–5 wt% Ni–4.5 wt% Fe–0.9 wt% Mn–0.2 wt% Ge; its measured Ge was 0.179 wt%. Its reported α + γ₂ microstructure does not establish a Ge-bearing precipitate: Ge was not resolved by its EDS analysis, and additional phases were not identified by XRD. The paper proposes grain refinement and a more ductile oxide layer but does not independently demonstrate either mechanism. (aslan2020effectofalloying pages 4-7, aslan2020effectofalloying pages 7-13, milosavljevic2021experimentalinvestigationof pages 1-2)

[GAP] No verified Ge-bearing *commercial or Navy seawater copper alloy*—and thus no established Ge range—was found for Cu–Ni, conventional or nickel–aluminum bronze, Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si. **[SPEC]** Do not interpret omission of Ge from an alloy's named nominal constituents as a certified *zero-Ge impurity limit*: a Ge-specific allowance in ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449, or UNS/CDA composition tables was **not verified**. The 0.2 wt% Ge NAB-like material is an *experimental recipe*, not C95800 or an AWS filler designation. A Copper Development Association review suggests Ge as a **future research addition** in brasses; it does not establish Ge inhibition of dezincification. Silver-alloy tarnish resistance is not evidence of protection of a Cu deposit in chloride seawater. (aslan2020effectofalloying pages 4-7, davies1993anoteon pages 1-3, davies1993anoteon pages 6-8, strauss2008tarnishproofsterlingsilver pages 1-5)

## 2. Quantitative seawater/chloride corrosion

The two located numerical comparisons require unusually careful interpretation:

| Study | Matrix and Ge (wt%) | Processing / chloride test | Comparator | Quantitative result | Key confound / evidence limitation | Transfer relevance |
|---|---|---|---|---|---|---|
| Aslan, Rajih & Haleem (2020), *IOP Conf. Ser.: Mater. Sci. Eng.* 987, 012018. DOI: [10.1088/1757-899X/987/1/012018](https://doi.org/10.1088/1757-899X/987/1/012018) | NAB-like Cu–Al–Ni–Fe–Mn; nominal **0.20 Ge**, measured **0.179 Ge** | Elemental powder mixing; 750 MPa compaction; Ar sintering at 550 °C/2 h then 950 °C/3 h; 850 °C/1 h solution treatment, ice-water quench, 200 °C/30 h aging; 10 h jet erosion–corrosion in **3.5 wt% NaCl** | Nominally Ge-free alloy C with the same nominal Al–Ni–Fe–Mn recipe | Total loss fell from **0.032 to 0.022 g·cm⁻²**, a **31.25% reduction** relative to C; Ge-bearing D also had the longest reported incubation period (aslan2020effectofalloying pages 13-16, aslan2020effectofalloying pages 4-7, aslan2020effectofalloying media fea7cbe2) | Not an isolated Ge comparison: measured C→D compositions also changed from **Al 9.136→9.255, Ni 5.762→6.009, Fe 4.367→4.864, and Mn 1.311→1.999 wt%**. Ge was not detected by EDS; no film chemistry or replication/statistics established causality (aslan2020effectofalloying pages 4-7, aslan2020effectofalloying pages 7-13) | Directly supports screening **≈0.20 wt% Ge in an Al-bronze/NAB-like family**, but only from sintered and post-build-heat-treated material—not wrought, cast NAB, as-deposited DED, or a commercial/Navy alloy |
| Haleem & Hashim (2018), reported second-hand in Dawood (2020), *Iraqi J. Mech. Mater. Eng.* 20, 362–375. Review DOI: [10.32852/iqjfmme.v20i4.530](https://doi.org/10.32852/iqjfmme.v20i4.530) | Cu–Al–Ni shape-memory alloy with **1, 2, or 3 Ge** | Powder metallurgy; electrochemical corrosion testing in **3.5 wt% NaCl**; detailed thermal history and polarization parameters unavailable in the retrieved review | Ge-free or lower-Ge baseline is not identified unambiguously in the review | Corrosion rate reportedly decreased from **34.99 to 4.72 mpy** at **3 wt% Ge**, an **86.5% reduction** (≈**0.889 to 0.120 mm·y⁻¹**) (dawood2020areviewof pages 5-8) | Result is second-hand; the underlying paper’s DOI, complete compositions, baseline assignment, replicate count, statistics, potentials, current densities, and film analyses were not verified. It does not establish a Ge-specific mechanism | Supports **3 wt%** only as an aggressive experimental Al-bronze-family search bound; it does not demonstrate NAB, seawater immersion, erosion–corrosion, wrought behavior, or as-deposited DED performance |


*Table: The only located quantitative chloride evidence for Ge-bearing copper–aluminum alloys is laboratory powder-metallurgy work, with important compositional or reporting limitations. Neither study demonstrates independent Ge causality or transfer to wrought, cast, or as-deposited DED material.*

[CITE] [NUMBERS] From the *Ge-free C versus Ge-bearing D* rows of Aslan and colleagues' Table 5, the measured 10-hour jet-test loss is **0.032 versus 0.022 g·cm⁻²**, a **31.25% lower loss relative to C**. The article's **308.84% “improvement”** instead compares D with a substantially different Cu–Ni alloy A and is **not** the isolated Ge effect; its prose also conflicts with the tabulated ordering of some losses. Actual C→D levels of Mn, Fe, Ni, and Al all changed, and all Al-bronze specimens were solution-treated and aged. The result therefore cannot be assigned quantitatively to Ge alone or claimed for as-deposited DED. **Figure 15 and Table 5** provide the visual record of the 3.5 wt% NaCl test. Aslan, Rajih and Haleem, *IOP Conference Series: Materials Science and Engineering* **987**, 012018 (2020), DOI **10.1088/1757-899X/987/1/012018**. (aslan2020effectofalloying pages 13-16, aslan2020effectofalloying pages 4-7, aslan2020effectofalloying media fea7cbe2, aslan2020effectofalloying media c6cf912d)

[CITE] [NUMBERS] A review attributes to Haleem and Hashim a decline from **34.99 to 4.72 mils per year** (approximately **0.889 to 0.120 mm·y⁻¹**) for powder-metallurgy Cu–Al–Ni shape-memory material tested in **3.5 wt% NaCl**, reporting a series containing **1, 2, and 3 wt% Ge** and the lowest cited value at **3 wt%**. This is an **86.5% rate reduction between the quoted endpoints**, *not* proof that a cast NAB or DED alloy has that rate: the excerpt does not unambiguously assign the 34.99-mpy endpoint, give full compositions, or document an as-deposited state. Dawood, *Iraqi Journal for Mechanical and Materials Engineering* **20**, 362–375 (2020), DOI **10.32852/iqjfmme.v20i4.530**, reviewing Haleem and Hashim, “Investigate the influence of Ge addition on the corrosion resistance and microstructure of Cu–Al–Ni shape memory prepared via powder metallurgy,” *Journal of Engineering and Applied Sciences* (2018), pp. 10882–10887; **DOI for the underlying article not verified**. (dawood2020areviewof pages 5-8)

[GAP] The defensible *reported-benefit window* is therefore **approximately 0.2–3 wt% Ge in laboratory Al-bronze-family materials only**, across *different matrices and tests*; it is **not** an established optimum or safe interval. No Ge-specific worsening threshold in copper alloys, natural-seawater immersion comparison against wrought C71500, Ecorr shift, film resistance, pitting/crevice or selective-attack depth, dezincification-inhibition measurement, or erosion–corrosion velocity limit was established. A 1993 CDA review does not list Ge among its demonstrated brass dezincification inhibitors and proposes testing it instead. Davies, *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions*, Copper Development Association Inc. (1993), technical report **without verified DOI**. (dawood2020areviewof pages 5-8, davies1993anoteon pages 6-8)

## 3. DED, welding, and repair interfaces

[GAP] **No Ge-controlled single-stream blown-powder laser-DED or ERCuNi/ERCuAl-A2/ERCuNiAl/ERCuMnNiAl welding comparison was located.** Consequently, neither crack suppression nor a Ge concentration causing solidification cracking, reheated-layer liquation, porosity, laser evaporation, or oxide-inclusion defects can be stated as a measured result. The assessed Cu–Ge multiphase diagram makes interdendritic Ge enrichment and low-melting terminal material a **hypothesis to test**, not proof of hot tearing. These risks become especially relevant to a reheated DED track and its diluted fusion boundary. Neither the listed AWS filler families nor weld success with an ordinary Ge-free filler validates Ge addition. (milosavljevic2021experimentalinvestigationof pages 1-2, milosavljevic2021experimentalinvestigationof pages 2-3)

[GAP] At the cast-NAB interface, dilution also changes **Al–Ni–Fe–Mn–Ge jointly** and may alter existing NAB phase balance; at wrought Cu–Ni, it reduces Al and changes the relevant Cu–Ni–Ge solubility and film system. No measured Ge partition coefficient, repair-interface cracking rate, or galvanic potential for either couple was found. Use paired Ge-free/Ge-bearing deposits with identical *measured* base-element chemistry, measure powder→deposit Ge retention, and separately examine first-layer dilution, remelted layers, density/cracks, and cross-interface selective-attack depth. These are proposed discriminating tests, **not literature outcomes**. (aslan2020effectofalloying pages 4-7, aslan2020effectofalloying pages 7-13)

## 4–5. Powder production, phase diagram, and CALPHAD

[CITE] [NUMBERS] A Ge-containing Cu–Bi–Ge research system was induction melted and investigated by DTA in **alumina under flowing Ar**; that is limited evidence of laboratory processing compatibility, **not** a demonstrated 0.5-kg ultrasonic-atomization yield or proof against Ge loss. Molten Cu–Ge brazing alloys containing approximately **20 wt% Ge** were tested at **1150 °C** against silicon-nitride-based ceramic: an unmodified Cu–Ge melt showed a **138°** contact angle. Neither result establishes wetting, contamination, or reaction with **alumina, zirconia, graphite, a Ti-alloy sonotrode, or Mo** under the proposed conditions. Naidich *et al.*, *Soviet Powder Metallurgy and Metal Ceramics* **27**, 888–890 (1988), DOI **10.1007/BF00796974**; Milosavljevic *et al.*, *Materials Research* **24**, e20210201 (2021), DOI **10.1590/1980-5373-MR-2021-0201**. (milosavljevic2021experimentalinvestigationof pages 1-2, naidich1988wettingofceramics pages 1-2)

[GAP] Ge's **quantitative** effects on this Cu-rich melt's surface tension, oxide skins, vaporization at a 1.07-µm laser, oxygen scavenging, and atomized-particle size/oxygen content were not established. Do not equate the volatile chloride **GeCl₄** encountered in Ge refining with the vapor pressure of **metallic Ge** in an Ar-shielded melt. Run crucible/sonotrode blank and contact checks, weigh charges, and assay Ge, O, Ti and Mo before and after atomization and DED. (milosavljevic2021experimentalinvestigationof pages 1-2, naidich1988wettingofceramics pages 1-2)

[CITE] [NUMBERS] The published Cu–Ge phase compilation reports α-(Cu) extending to **88.3 atomic% Cu**; conversion using Cu and Ge atomic masses gives **approximately 13.1 wt% Ge** at the *most Ge-rich quoted α boundary*. **The temperature of that maximum is not established by the retrieved table**, so 13.1 wt% must **not** be treated as room-temperature solubility or a DED design limit. The ξ field is quoted as 83.5–90.2 atomic% Cu; ε is approximately Cu₀.₇₆₅Ge₀.₂₃₅, η is Cu₃Ge, and θ is approximately Cu₀.₇₃₅Ge₀.₂₆₅. The binary assessment describes **two peritectic, two eutectic, one peritectoid, and three eutectoid invariant reactions**, but their individual temperature/composition coordinates were not recovered reliably. Milosavljevic *et al.* (2021), DOI **10.1590/1980-5373-MR-2021-0201**, citing the binary assessment by Wang, Jin, Leinenbach and Jacot, “Thermodynamic assessment of the Cu–Ge binary system,” *Journal of Alloys and Compounds* **504**, 159–165 (2010), DOI **10.1016/j.jallcom.2010.05.077**. (milosavljevic2021experimentalinvestigationof pages 1-2, milosavljevic2021experimentalinvestigationof pages 2-3)

[CITE] [GAP] A **published assessed Cu–Ge binary** exists, and experimental liquid **Al–Cu–Ge** mixing thermodynamics exist; the latter are *not* a validated Cu–Al–Ge solidification assessment. Kanibolotsky *et al.*, *Journal of Chemical Thermodynamics* **35**, 1763–1774 (2003), DOI **10.1016/S0021-9614(03)00157-5**. Coverage of Ge and assessed **Cu–Ni–Ge/Cu–Al–Ge** interactions in the laboratory's exact **Thermo-Calc TCCU** release, COST 531, or an accessible pycalphad-ready TDB was **not verified**; inspect `LIST_ELEMENT`/phase coverage and parameter provenance rather than silently extrapolating. Cu–Ge's Cu-rich liquidus starts at pure Cu's approximately **1084 °C**; no retrieved measurement shows that **0.2–3 wt% Ge alone** drives its liquidus above **1250 °C**, but neither does the binary guarantee adequate superheat once **Ni, Fe, and Al** are included. Require a separately checked multicomponent liquidus **≤1200–1250 °C** before melting each powder recipe. (milosavljevic2021experimentalinvestigationof pages 1-2, milosavljevic2021experimentalinvestigationof pages 2-3, kanibolotsky2003thermodynamicsofliquid pages 1-4)

## 6. Supply, cost, and safety

[CITE] [NAVY] Ge is on the **2025 final U.S. critical-minerals list**, alongside Cu and Ni; the USGS describes that list as revising its **2022 final list**. The retrieved material does **not** independently reproduce the 2022 Ge entry; confirm against the primary 2022 Federal Register listing if that historical designation must be quoted verbatim. Jones, Gallegos, KunleDare and Riggs, “USGS critical minerals review,” *Mining Engineering*, May 2026, pp. 42 ff.; and the **2025 Final List of Critical Minerals**, Federal Register document **2025-19813** (government sources; **no journal DOI**). This is a supply-risk consideration, not evidence of a Navy Ge-alloy approval. (iii2026usgscriticalminerals pages 1-2)

[NUMBERS] [GAP] A compiled Ge-metal price chart is scaled in **US$/kg** and indicates an **order of magnitude of approximately US$1,000–4,000/kg in recent years**, with substantial grade- and date-dependent volatility; those endpoints are **not verified transaction quotes** for atomization-grade Ge. For scale, **0.2 wt% Ge in a 0.5-kg charge is 1 g**, implying approximately **US$1–4** of Ge at that indicative price; **3 wt% is 15 g**, approximately **US$15–60**, before procurement losses. The price source is the compiled chart reproduced by Kumar and Kotasthane, “Lessons from China’s Weaponisation of Critical Minerals: A Case Study of Gallium and Germanium,” *Indian Public Policy Review* **7** (2026), figure 17 (**DOI not verified**). (kumar2026lessonsfromchinas pages 15-18)

[CITE] [GAP] A germanium handbook describes most Ge compounds as having comparatively low-order toxicity but distinguishes **toxic germane (GeH₄)**; this does **not** make respirable metal powder, Ge-bearing condensate, or a mixed Cu/Ni/Ge laser fume safe. No verified **Ge-specific OSHA PEL**, Ge-specific Navy alloy restriction, or Ge-specific **RoHS/REACH alloy limit** was found; none should be invented. Apply combustible/respirable-metal-powder controls, inert-gas/asphyxiation controls, local fume capture, and an industrial-hygiene assessment for the *entire* alloy, including Ni and Cu. Melcher and Buchholz, “Germanium,” *Critical Metals Handbook* (2014), pp. 177–203, DOI **10.1002/9781118755341.ch8**; Mai, “Laser generated air contaminants,” *ILSC 2023*, DOI **10.2351/7.0001450**. (melcher2014germanium pages 14-16)

## 7–9. Bounds, interactions, and evidence quality

**[NUMBERS] Proposed palette entry, all compositions in wt% Ge in the finished alloy:**

| Decision variable | Al-bronze-family proposed value | Basis and limiting failure mode |
|---|---:|---|
| **Conservative maximum** | **0.20** | Smallest **nominal experimentally tested NAB-like** dose (actual 0.179); *not* an established commercial, Navy, AM, or cladding maximum. Above this point, as-deposited interfacial corrosion, retention, and crack tolerance have **no validated conservative precedent**. (aslan2020effectofalloying pages 4-7) |
| **Non-conservative maximum** | **3.0** | Uppermost retrieved Ge dose in **Cu–Al–Ni powder-metallurgy SMA chloride** experiments, second-hand. The bounds are set by **absence of evidence beyond 3.0**, plus untested segregation/secondary phases, cracking, and cost—not a demonstrated harm threshold or a binary solubility maximum. (dawood2020areviewof pages 5-8, milosavljevic2021experimentalinvestigationof pages 1-2) |
| **Functional floor, provisional** | **0.20** | Lowest nominal Ge addition associated with a reported marine-chloride endpoint; **no Ge-isolated statistically significant threshold has been shown**. Treat 0.20 as the *lowest literature-anchored screening dose*, not a demonstrated minimum effective concentration. (aslan2020effectofalloying pages 13-16, aslan2020effectofalloying pages 4-7) |

[GAP] **Cu–Ni-family Ge bound: none justified.** A numerical Ge *impurity maximum* for the powder or deposit likewise cannot be attributed to an identified ASTM/MIL/AWS/UNS specification or study; **impurity_max_wt = NA**, not a fabricated ppm limit. If procurement or certification requires an impurity limit, obtain the actual governing material specification and establish an analytical detection/acceptance criterion independently. (aslan2020effectofalloying pages 4-7, dawood2020areviewof pages 5-8)

[CITE] [GAP] **Interactions for joint constraints:** evaluate Ge with **Al, Ni, Fe, and Mn simultaneously**, because their *measured* levels all shifted in the principal Ge comparison; do **not** fit a Ge coefficient to that C→D difference without orthogonal controls. Check α/ξ and other Ge-rich phase appearance, interdendritic enrichment, and the lowest-melting reheated constituent as composition-dependent constraints; there is no validated **Ge+Al**, **Ge/Ni**, **Ge/Fe**, or **Ge/Mn** allowable sum/ratio for the proposed deposit. Likewise, Ge has **not** been shown here to neutralize deleterious Fe/Mn effects or to inhibit Zn dealloying; the CDA report calls for Ge testing rather than asserting such effects. Literature attribution of Ge-induced oxide protection and grain refinement is mechanistic speculation until supported by cross-sectional film analysis and matched-composition controls. (aslan2020effectofalloying pages 4-7, aslan2020effectofalloying pages 7-13, milosavljevic2021experimentalinvestigationof pages 1-2, davies1993anoteon pages 6-8)

**Evidence grade: thin.** The proposed conservative bound is **experimental, not specification-derived**; one comparison is compositionally confounded and post-heat-treated, and the other is a second-hand SMA result. Neither establishes the proposal's coupled acceptance criteria of crack-free *as-deposited* repair on both substrates and ≥C71500 seawater durability. (aslan2020effectofalloying pages 4-7, dawood2020areviewof pages 5-8)

VERDICT | Ge | decision=INCLUDE | family=Al-bronze | conservative_max_wt=0.2 | nonconservative_max_wt=3.0 | floor_wt=0.2 | impurity_max_wt=NA | evidence=thin

References

1. (aslan2020effectofalloying pages 13-16): Noor Sabah Aslan, Abdalwahid K. Rajih, and Ali Hubi Haleem. Effect of alloying elements on the erosion–corrosion behaviour of cu-based alloys. IOP Conference Series: Materials Science and Engineering, 987:012018, Nov 2020. URL: https://doi.org/10.1088/1757-899x/987/1/012018, doi:10.1088/1757-899x/987/1/012018. This article has 7 citations.

2. (aslan2020effectofalloying pages 4-7): Noor Sabah Aslan, Abdalwahid K. Rajih, and Ali Hubi Haleem. Effect of alloying elements on the erosion–corrosion behaviour of cu-based alloys. IOP Conference Series: Materials Science and Engineering, 987:012018, Nov 2020. URL: https://doi.org/10.1088/1757-899x/987/1/012018, doi:10.1088/1757-899x/987/1/012018. This article has 7 citations.

3. (dawood2020areviewof pages 5-8): Nawal Mohammed Dawood. A review of microstructure and corrosion behavior of cu al ni shape memory alloy. THE IRAQI JOURNAL FOR MECHANICAL AND MATERIALS ENGINEERING, 20:362-375, Dec 2020. URL: https://doi.org/10.32852/iqjfmme.v20i4.530, doi:10.32852/iqjfmme.v20i4.530. This article has 1 citations.

4. (aslan2020effectofalloying pages 7-13): Noor Sabah Aslan, Abdalwahid K. Rajih, and Ali Hubi Haleem. Effect of alloying elements on the erosion–corrosion behaviour of cu-based alloys. IOP Conference Series: Materials Science and Engineering, 987:012018, Nov 2020. URL: https://doi.org/10.1088/1757-899x/987/1/012018, doi:10.1088/1757-899x/987/1/012018. This article has 7 citations.

5. (milosavljevic2021experimentalinvestigationof pages 1-2): Milan Milosavljevic, Milena Premovic, Dusko Minic, Vladan Cosovic, Aleksandar Djordjevic, and Milica Tomovic. Experimental investigation of phase equilibria in the bi-cu-ge system. Materials Research, Sep 2021. URL: https://doi.org/10.1590/1980-5373-mr-2021-0201, doi:10.1590/1980-5373-mr-2021-0201. This article has 2 citations.

6. (davies1993anoteon pages 1-3): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

7. (davies1993anoteon pages 6-8): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

8. (strauss2008tarnishproofsterlingsilver pages 1-5): JT Strauss. Tarnish-proof sterling silver: understanding the limitations. Unknown journal, 2008.

9. (aslan2020effectofalloying media fea7cbe2): Noor Sabah Aslan, Abdalwahid K. Rajih, and Ali Hubi Haleem. Effect of alloying elements on the erosion–corrosion behaviour of cu-based alloys. IOP Conference Series: Materials Science and Engineering, 987:012018, Nov 2020. URL: https://doi.org/10.1088/1757-899x/987/1/012018, doi:10.1088/1757-899x/987/1/012018. This article has 7 citations.

10. (aslan2020effectofalloying media c6cf912d): Noor Sabah Aslan, Abdalwahid K. Rajih, and Ali Hubi Haleem. Effect of alloying elements on the erosion–corrosion behaviour of cu-based alloys. IOP Conference Series: Materials Science and Engineering, 987:012018, Nov 2020. URL: https://doi.org/10.1088/1757-899x/987/1/012018, doi:10.1088/1757-899x/987/1/012018. This article has 7 citations.

11. (milosavljevic2021experimentalinvestigationof pages 2-3): Milan Milosavljevic, Milena Premovic, Dusko Minic, Vladan Cosovic, Aleksandar Djordjevic, and Milica Tomovic. Experimental investigation of phase equilibria in the bi-cu-ge system. Materials Research, Sep 2021. URL: https://doi.org/10.1590/1980-5373-mr-2021-0201, doi:10.1590/1980-5373-mr-2021-0201. This article has 2 citations.

12. (naidich1988wettingofceramics pages 1-2): Yu. V. Naidich, V. S. Zhuravlev, N. I. Frumina, B. D. Kostyuk, N. A. Krasovskaya, and V. G. Ostrovskii. Wetting of ceramics based on silicon nitride by metallic melts. Soviet Powder Metallurgy and Metal Ceramics, 27:888-890, Nov 1988. URL: https://doi.org/10.1007/bf00796974, doi:10.1007/bf00796974. This article has 7 citations.

13. (kanibolotsky2003thermodynamicsofliquid pages 1-4): Dmitry S. Kanibolotsky, Nataliya V. Kotova, Olena A. Bieloborodova, and Vladyslav V. Lisnyak. Thermodynamics of liquid aluminium-copper-germanium alloys. The Journal of Chemical Thermodynamics, 35:1763-1774, Nov 2003. URL: https://doi.org/10.1016/s0021-9614(03)00157-5, doi:10.1016/s0021-9614(03)00157-5. This article has 15 citations.

14. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

15. (kumar2026lessonsfromchinas pages 15-18): A Kumar and P Kotasthane. Lessons from china's weaponisation of critical minerals: a case study of gallium and germanium. Unknown journal, 2026.

16. (melcher2014germanium pages 14-16): Frank Melcher and Peter Buchholz. Germanium. Critical Metals Handbook, pages 177-203, Dec 2014. URL: https://doi.org/10.1002/9781118755341.ch8, doi:10.1002/9781118755341.ch8. This article has 97 citations.
