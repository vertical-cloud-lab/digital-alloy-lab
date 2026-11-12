<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 322c7c4b-d2ca-43bc-b4af-f0e4292d7d0f
- Submitted: 2026-10-17T19:01:23Z
- Fetched: 2026-10-17T19:35:25Z (status: success)
- Raw trajectory JSON: ../raw/el-44-La.json.gz
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

ELEMENT UNDER REVIEW: La (rare earth). Lanthanum (often with Ce as mischmetal) added to B10/B30 Cu-Ni and bronzes, claimed to refine grains, scavenge S and O, and improve the corrosion film.

Answer for La specifically, not for copper alloys in general:
1. ROLE: what La does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their La ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how La changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-La, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-La, Cu-Ni-La and Cu-Al-La are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of La in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that La neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | La | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: La (rare earth). Lanthanum (often with Ce as mischmetal) added to B10/B30 Cu-Ni and bronzes, claimed to refine grains, scavenge S and O, and improve the corrosion film.

Answer for La specifically, not for copper alloys in general:
1. ROLE: what La does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their La ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how La changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-La, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-La, Cu-Ni-La and Cu-Al-La are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of La in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that La neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | La | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Lanthanum (La) for pre-alloyed, seawater-service copper DED powder

**Decision: INCLUDE, experimentally, in both Cu–Ni and aluminum-bronze search spaces—but do not describe La as a qualified seawater-corrosion addition.** The case for testing small La additions is credible: measured additions refine several cast Cu-alloy microstructures, and La-bearing Cu–Ni develops identifiable second phases. The case for *using* them in an as-deposited marine repair is not established. I found no accessible study demonstrating that elemental La in blown-powder DED meets wrought C71500 corrosion performance, and no verified La-bearing Navy/commercial composition range. High La also produces grain-boundary intermetallics; much of the apparent corrosion evidence concerns acid, mischmetal, another rare earth, or an inaccessible 2026 paper. The bounds below are **experimental design gates, not specification limits**. [CITE][GAP] (davies1993anoteon pages 5-6, samoilova2019effectofcerium pages 1-3, samoilova2019effectofcerium pages 3-7)

All compositions and proposed limits below are **wt% of elemental La in the alloy**, with Cu as balance unless other elements are specified. Mischmetal and LaB₆ percentages are **not** elemental-La percentages.

## 1. Role, phases, and specified alloys

- **Cu–Ni, including the B10/B30 composition families.** In nine *cast* Cu–Ni–Ce–La specimens, Ni was 3.12–40.10, measured La 0.26–3.34 and Ce 0.09–3.52. Every specimen had a Cu–Ni matrix and `(Ce,La)(Ni,Cu)₅`; six additionally had Cu₆La/Cu₆Ce. The rare-earth-rich constituents concentrated at matrix grain boundaries, while increasing rare-earth addition enlarged the eutectic constituent and refined Cu–Ni cells. This establishes neither a beneficial concentration in La-only B10/B30 nor improved seawater resistance. Notably, these specimens were melted at **1,450–1,500 °C**, not within the proposed atomizer’s operating range. [CITE][NUMBERS] Samoilova, Trofimov and Vakhitova, *Materials Science Forum* **946** (2019) 123–128, DOI **10.4028/www.scientific.net/MSF.946.123**. (samoilova2019effectofcerium pages 1-3, samoilova2019effectofcerium media b35c380c, samoilova2019effectofcerium pages 3-7)
- **Cu–Ni–Sn.** In Cu–15Ni–8Sn, nominal La additions **0, 0.1, 0.3, 0.5 and 0.8** refined *as-cast* secondary dendrite-arm spacing from **28.4 µm without La** to **21.5 µm at 0.1** and **10.6 µm at 0.8**. Identified phases shifted from **LaNiSn** toward **La₅Sn₃** as La increased; honeycomb eutectic appeared above **0.1**. The reported **324 HV at 0.8** required 450 °C aging for 30 min; the La-free alloy actually attained a higher **340 HV** peak after 15 min. These are not as-deposited corrosion results. [CITE][NUMBERS] Qi et al., *Nonferrous Metals Science and Engineering* **14** (2023) 569–579, DOI **10.13264/j.cnki.ysjskx.2023.04.016**. (zhaoming2023effectofrare pages 1-4, zhaoming2023effectofrare pages 7-9)
- **Cu–Ni–Si.** A review reports best corrosion behavior at **0.17 La** in *as-cast* C7025/C70250-type Cu–Ni–Si, citing Liu et al. (2023). The accessible review does **not** establish its electrolyte, 30-day attack depth, or suitability as a marine alloy; the primary experiment was not verified here. [CITE][NUMBERS][GAP] Yan et al., *Coatings* **15** (2025) 91, DOI **10.3390/coatings15010091**, citing Liu et al., *Chinese Journal of Rare Earth Science* **41** (2023) 930–941 (DOI not verified). (yan2025researchprogressof pages 12-15, yan2025researchprogressof pages 15-16, yan2025researchprogressof pages 21-22)
- **Aluminum bronze, including NAB and Mn–Al bronze.** A Copper Development Association review reports that *separately tested* **0.05 La**, **0.05 Ce**, or **0.05 Nd** improved aluminum-bronze general corrosion in **dilute sulfuric acid**; a related experiment used **dilute nitric acid**. Neither result establishes protection in chloride seawater, identifies a La-specific NAB κ phase, or demonstrates inhibition of selectively attacked β. In a *La-free* comparison of NAB and Mn–Al bronze in simulated seawater, β-phase amount and distribution governed selective attack; that is the substrate-specific mechanism any proposed La addition must improve, rather than merely reduce grain size. [CITE][NUMBERS][GAP] Davies, Copper Development Association, *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions* (1993), citing Verma et al., *British Corrosion Journal* **25** (1990) 131 and Singh et al., *Corrosion* **45** (1989) 222 (DOIs not verified); Cobo Ocejo, Biezma Moraleda and Linhardt, *Metals* **12** (2022) 380, DOI **10.3390/met12030380**. (davies1993anoteon pages 5-6, ocejo2022corrosionbehaviorof pages 1-3)
- **Brasses and gunmetal/tin bronzes.** The CDA review reports **0.1 mischmetal**, *not 0.1 La*, as the best tested addition to an **arsenical 60–40 brass**, whereas analogous rare-earth additions to non-arsenical duplex brass marginally **increased** dezincification. In another melt, **0.5 mischmetal charged** yielded only **0.04 total rare earth retained**, principally attributed to oxidation; behavior also changed with hot-worked versus annealed condition. It is therefore unsafe to claim La independently inhibits dezincification. I found no verified La-specific seawater improvement for tin bronze or gunmetal; the Cu–Sn–P–La work identified during searching did not yield an accessible marine-exposure result. [CITE][NUMBERS][GAP] Davies (1993), citing Sullivan, INCRA Project 178 (1971), and Weldon, BNFMRA Report A1148 (1957); these reports have **no verified DOI**. (davies1993anoteon pages 5-6, davies1993anoteon pages 6-8)
- **Other copper alloys and mechanism.** In *cast, nonmarine* Cu–24Pb, approximately **0.054 measured La** (0.06 nominal) refined α-Cu and Pb-rich constituents and improved tensile strength, whereas **0.179 measured La** produced Cu₆La and La₅Pb₃ and impaired ductility. The authors argue for an interfacial/surfactant-assisted nucleation mechanism, **not** proof that Cu₆La is an effective Cu grain-nucleation substrate. La’s oxygen/sulfur-gettering role is plausible, but retained La, oxides/oxysulfides and sulfides must be measured separately; a corrosion-protective La-bearing seawater film has **not** been demonstrated by these experiments. [CITE][NUMBERS][GAP] Alqadhi et al., “Insights into the dual role of La in microstructural refinement and mechanical improvement of hypomonotectic Cu–24Pb alloys,” available 2026 manuscript (**DOI not established**). (alqadhi2026insightsintothe pages 1-2, alqadhi2026insightsintothe pages 2-3, alqadhi2026insightsintothe pages 3-4, alqadhi2026insightsintothe pages 4-8)

**[SPEC][NAVY] Verified La-containing commercial/Navy grades: none identified.** Consequently there is **no established La wt% range** to quote from ASTM B111/B171/B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449, or UNS/CDA C71500/C95800 data in the accessible evidence. This means *not specified as an intentional addition*, **not** a demonstrated specification-mandated La maximum or a prohibition. Do not relabel the above research alloys as Navy alloys. (samoilova2019effectofcerium pages 1-3, ocejo2022corrosionbehaviorof pages 1-3)

## 2. Quantitative marine-corrosion evidence—and its limits

**[GAP] For *elemental La* in Cu–Ni or NAB, no verified numerical seawater/ASTM D1141/3.5 wt% NaCl comparison was retrievable here** for corrosion rate, *E*₍corr₎, polarization resistance, film resistance, cyclic-polarization hysteresis, pit/crevice depth, selective-attack depth, erosion–corrosion, or safe flow velocity. Accordingly there is **no defensible numerical seawater range in which La helps, or threshold at which it harms**; the proposed composition ceilings concern metallurgical risk, not proven corrosion breakpoints. The identified Li, Leng and Zhu paper, “Effect of Rare Earth Element La Addition on the Corrosion Resistance of 90/10 Copper–Nickel Alloy,” *Advanced Engineering Materials* (2026), DOI **10.1002/adem.202501513**, could be directly relevant, but its full results were **unobtainable**; assigning numbers to it would be fabrication. (davies1993anoteon pages 5-6, samoilova2019effectofcerium pages 1-3)

The **0.05 La** aluminum-bronze acid result is a positive *acid* screen, while the brass observation above shows a condition in which *mixed rare earths* worsen selective attack. A reported **0.021 Y** optimum, with inner-film resistance **>1,500 kΩ** after 30 days in 3.5 wt% NaCl, is specifically **yttrium in cast 90Cu–10Ni**, *not La*: it cannot supply a La floor or film-resistance claim. [CITE][NUMBERS][GAP] Zhang et al., *International Journal of Electrochemical Science* **15** (2020) 4161–4178, DOI **10.20964/2020.05.47**. (davies1993anoteon pages 5-6, davies1993anoteon pages 6-8)

Nor should the **2 La** pre-oxidized 56Cu–22Ni–12Fe–8Al anode in **high-temperature fluoride electrolyte** be represented as marine evidence: the reported electrolyte penetrated along La-rich regions, but that experiment involved pre-oxidation at **800 °C**, unlike an as-deposited seawater coupon. [CITE][NUMBERS] Zhuang et al., *Rare Metal Materials and Engineering* **55** (2026) 2756–2764, DOI **10.12442/j.issn.1002-185x.20250607**. (庄玉伟2026corrosionbehaviorof pages 7-8)

## 3. DED, welding, and the proposed interfaces

**[GAP] No La-specific blown-powder Cu–Ni/NAB DED solidification-crack, reheated-layer liquation-crack, pore-fraction, La-evaporation, or substrate-dilution measurement was established.** The cast Cu–Ni–Ce–La observation of grain-boundary rare-earth intermetallics and eutectic suggests a **testable** mechanism for terminal-liquid hot cracking and reheating-related liquation, not evidence that cracks occur at **0.05–0.10 La** in DED. Likewise, gettering O/S might improve melt cleanliness, or retained oxides could become pore/inclusion nucleants; neither outcome is demonstrated for this powder. [CITE][GAP] Samoilova et al. (2019), DOI **10.4028/www.scientific.net/MSF.946.123**. (samoilova2019effectofcerium pages 1-3, samoilova2019effectofcerium pages 3-7)

For repair, first-layer mixing with **C95800** introduces Al, Ni, Fe and Mn into a La-bearing Cu–Ni deposit, potentially changing both La-containing phases and the locally corrosion-sensitive β/κ balance; mixing with **wrought Cu–Ni** changes Ni and Fe/Mn levels and can dilute nominal La below its intended floor. Compare cross-section chemistry of the powder, first track and upper layers, and examine both interfaces after the 30-day immersion. This is an **inference** from cast phase and La-free NAB corrosion studies, **not a verified La welding result**. ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl experience is relevant to choosing baseline fillers and repair practice, but no La-specific allowable range or crack-suppression result in those AWS fillers was verified here. [CITE][GAP] Cobo Ocejo et al. (2022), DOI **10.3390/met12030380**; Samoilova et al. (2019), DOI **10.4028/www.scientific.net/MSF.946.123**. (samoilova2019effectofcerium pages 1-3, ocejo2022corrosionbehaviorof pages 5-8, ocejo2022corrosionbehaviorof pages 1-3, samoilova2019effectofcerium pages 3-7)

A prominent apparent AM precedent is **not an elemental-La pre-alloy**: Liu et al. used **1.0 wt% LaB₆ nanoparticles mixed with Cu powder** in **1,060 nm LPBF**, obtaining **347 ± 2 MPa yield strength**, **22.8 ± 1.2% elongation** and **98.4% IACS**. One wt% LaB₆ contains about **0.68 wt% La by stoichiometry**, alongside boron; particle-assisted absorption/dispersion and LPBF cannot establish a **0.68 La** bound, seawater resistance or crack-free single-stream DED. [CITE][NUMBERS] Liu et al., *Nature Communications* **15** (2024), DOI **10.1038/s41467-024-45732-y**. (liu2024manufacturingofhigh pages 6-7, liu2024manufacturingofhigh pages 2-4, liu2024manufacturingofhigh pages 1-2, liu2024manufacturingofhigh pages 4-5)

## 4. Melt preparation, atomization, phases, and CALPHAD

**[NUMBERS] Melt-retention warning:** the historic brass charge/retention comparison, **0.5 mischmetal charged → 0.04 total rare earth retained**, demonstrates why a nominal La charge cannot substitute for ICP-measured powder and deposit. The Cu–Ni–Ce–La cast study used an **alundum (alumina) crucible**, graphite protection and **1,450–1,500 °C**; it did **not** establish compatibility of dilute La with this project’s argon-protected, approximately **1,300 °C** ultrasonic atomizer, zirconia crucible, or a Ti-alloy/Mo sonotrode. Oxidation, crucible/sonotrode pickup, and retained oxide inclusions are credible process risks requiring before/after chemistry and particle cross-sections; **specific La–Al₂O₃, La–ZrO₂, La–graphite, La–Ti, La–Mo reaction rates and La evaporation fractions are unmeasured here**. A surfactant effect reported in a Cu–Pb melt does not provide a quantitative Cu–Ni or NAB surface-tension change. [CITE][NUMBERS][GAP] Davies (1993); Samoilova et al. (2019), DOI **10.4028/www.scientific.net/MSF.946.123**; Alqadhi et al. (2026 manuscript, DOI not established). (davies1993anoteon pages 5-6, samoilova2019effectofcerium pages 1-3, alqadhi2026insightsintothe pages 1-2, alqadhi2026insightsintothe pages 4-8)

**[CITE] Phase constitution:** a published summary names **Cu₃₇La₃, Cu₆La, Cu₅La, Cu₄La, Cu₂La and CuLa**, and identifies **Cu₆La and Cu₂La as congruently melting**. Cu₆La is the pertinent Cu-rich intermetallic; Ni can instead stabilize La-containing `(Ni,Cu)₅` phases. The available passages do **not** supply an independently verified numerical **maximum equilibrium La solubility in α-Cu *with its temperature***, or Cu-rich eutectic temperature/composition; the manuscript’s approximately **0.03–0.04 La** assertion lacks a stated temperature and should **not** be reported as the verified binary maximum. Likewise, the cited **0.2 at 870 °C and ≤0.05 at 300 °C refer to *Ce*, not La**. Cu-rich La is not shown to raise a Cu-rich alloy above **1,250 °C**, but liquidus clearance cannot be certified for any *multicomponent* proposed alloy without measured DSC and a validated assessment. [NUMBERS][GAP] Samoilova et al. (2019), DOI **10.4028/www.scientific.net/MSF.946.123**; Alqadhi et al. (2026 manuscript, DOI not established), citing Okamoto, “Cu–La,” *Journal of Phase Equilibria* **22** (2001) 594–595 (DOI not verified). (samoilova2019effectofcerium pages 1-3, alqadhi2026insightsintothe pages 9-11, samoilova2019effectofcerium pages 3-7)

**[GAP] Database status:** a *published* La–Ni–Cu assessment is identified in the cast-study bibliography: An et al., “Phase equilibria of the La–Ni–Cu ternary system at 673 K: thermodynamic modeling and experimental validation,” *CALPHAD* **36** (2012) 8–15 (**DOI not verified**). A **673 K** assessment is not automatically a validated Cu-rich **liquidus/Scheil DED** description. **TCCU La support, assessed Cu–La/Cu–Ni–La/Cu–Al–La parameters, COST 531 coverage, and an accessible reusable TDB were not verified**; check the installed TCCU element and assessed-system lists and pycalphad phase models before plotting an La-bearing contour. Do not treat a calculation extrapolating missing binaries as predictive evidence. (samoilova2019effectofcerium pages 1-3, samoilova2019effectofcerium pages 3-7)

## 5. Supply, safety, and interactions

**[GAP]** US critical-mineral classification for La should be checked under the rare-earth grouping in both the **2022** and **final 2025** US lists; the retrieved evidence does not independently verify either list entry, an elemental-La **USD/kg** transaction price, or a Navy-specific La restriction. No documented La-specific OSHA exposure limit or La-specific RoHS/REACH prohibition was established here: absence of a verified limit is **not** proof of regulatory exemption. For powder and laser operations, control combustible/reactive fine powder, oxygen/moisture ingress, metal/oxide fume and collector contamination; determine applicable site dust and fume requirements rather than borrowing a limit for a different rare earth. **No defensible approximate La price/kg can be supplied from the retrieved sources.** [GAP] (davies1993anoteon pages 5-6, samoilova2019effectofcerium pages 1-3, yan2025researchprogressof pages 15-16)

**[NUMBERS] Joint constraints to record:** track **measured retained La**, charged La, O, S and Ce separately. In cast Cu–Ni–Ce–La, the observed change from principally `(Ce,La)(Ni,Cu)₅` to that phase **plus Cu₆La/Cu₆Ce** occurred when `(Ce + La)/Ni` increased past approximately **0.2 by mass** *in the particular experimental series*—**not** a universal weldability inequality or a valid La-only upper bound. La can consume the Ni needed for LaNi₅-like phases; with Sn it instead forms **LaNiSn/La₅Sn₃** and can deplete the matrix of Ni/Sn. With Al/Fe/Mn, assess La phases jointly with NAB β/κ constitution, especially in the substrate-diluted layer. Sulfur/oxygen gettering competes with retaining metallic La and may create persistent inclusions; the relevant ratios are **effective retained La to O/S** and **La + Ce relative to Ni**, not simply charged La. [CITE][NUMBERS][GAP] Samoilova et al. (2019), DOI **10.4028/www.scientific.net/MSF.946.123**; Qi et al. (2023), DOI **10.13264/j.cnki.ysjskx.2023.04.016**; Cobo Ocejo et al. (2022), DOI **10.3390/met12030380**. (samoilova2019effectofcerium pages 1-3, zhaoming2023effectofrare pages 1-4, ocejo2022corrosionbehaviorof pages 5-8, samoilova2019effectofcerium pages 3-7)

## 6. Proposed composition gates and evidence quality

| Family | Functional floor | Conservative maximum | Non-conservative maximum | What sets the gate |
|---|---:|---:|---:|---|
| **Al-bronze/NAB** | **0.05** | **0.05** | **0.10** | **0.05** is the reported *acid*-tested elemental-La aluminum-bronze addition, not a Navy standard or verified seawater floor. **0.10** is an experimental escalation ceiling, chosen to avoid assuming that the **0.1 mischmetal** brass result transfers to elemental La or that larger La additions remain inclusion-free; validate β selective attack and reheated interfaces. |
| **Cu–Ni** | **0.05** *(provisional screening floor)* | **0.05** | **0.10** | No verified Cu–Ni seawater **La** floor or commercial La limit exists. The floor/ceiling are deliberately matched low-dose screening gates, **not** literature-derived performance thresholds. **0.10** limits exposure to uncharacterized La-bearing boundary constituents and gettering losses; research compositions with **0.26–3.34 La plus Ce** formed intermetallics and were made above this atomizer’s useful melt range. |

[CITE][NUMBERS][GAP] The proposed **0.05** Cu–Ni floor is **not** the **0.021 Y** Cu–Ni optimum, and neither family’s **0.10** is a measured solid-solubility boundary. If measurable effects require more than **0.10** in the actual atomized powder, this proposal should *reconsider inclusion* rather than silently increasing the bound. There is **no specification- or study-derived universal La impurity maximum** to report, because the decision is INCLUDE, not LIMIT. Acceptance should require actual powder/deposit La assay, crack/porosity inspection after repeated thermal cycling, and as-deposited 30-day selective-attack depth versus wrought C71500 on self-builds and both repair substrates. [CITE][SPEC][GAP] Davies (1993); Samoilova et al. (2019), DOI **10.4028/www.scientific.net/MSF.946.123**; Qi et al. (2023), DOI **10.13264/j.cnki.ysjskx.2023.04.016**. (davies1993anoteon pages 5-6, samoilova2019effectofcerium pages 1-3, zhaoming2023effectofrare pages 1-4, samoilova2019effectofcerium pages 3-7)

**Evidence grade: thin for the requested decision.** Phase identification in cast research alloys and the LPBF *LaB₆* result are considerably firmer than claims about elemental-La DED, marine films, weld cracking, feedstock retention, specifications or C71500-equivalent service. These distinctions should remain explicit in the proposal. (samoilova2019effectofcerium pages 1-3, liu2024manufacturingofhigh pages 6-7, ocejo2022corrosionbehaviorof pages 1-3)

VERDICT | La | decision=INCLUDE | family=both | conservative_max_wt=0.05 | nonconservative_max_wt=0.10 | floor_wt=0.05 | impurity_max_wt=NA | evidence=thin

References

1. (davies1993anoteon pages 5-6): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

2. (samoilova2019effectofcerium pages 1-3): O.V. Samoilova, Evgeny A. Trofimov, and E.R. Vakhitova. Effect of cerium and lanthanum additives on the phase composition of the copper-nickel alloys. Materials Science Forum, 946:123-128, Feb 2019. URL: https://doi.org/10.4028/www.scientific.net/msf.946.123, doi:10.4028/www.scientific.net/msf.946.123. This article has 3 citations and is from a peer-reviewed journal.

3. (samoilova2019effectofcerium pages 3-7): O.V. Samoilova, Evgeny A. Trofimov, and E.R. Vakhitova. Effect of cerium and lanthanum additives on the phase composition of the copper-nickel alloys. Materials Science Forum, 946:123-128, Feb 2019. URL: https://doi.org/10.4028/www.scientific.net/msf.946.123, doi:10.4028/www.scientific.net/msf.946.123. This article has 3 citations and is from a peer-reviewed journal.

4. (samoilova2019effectofcerium media b35c380c): O.V. Samoilova, Evgeny A. Trofimov, and E.R. Vakhitova. Effect of cerium and lanthanum additives on the phase composition of the copper-nickel alloys. Materials Science Forum, 946:123-128, Feb 2019. URL: https://doi.org/10.4028/www.scientific.net/msf.946.123, doi:10.4028/www.scientific.net/msf.946.123. This article has 3 citations and is from a peer-reviewed journal.

5. (zhaoming2023effectofrare pages 1-4): QI Zhaoming and XU Huaben. Effect of rare earth lanthanum on microstructure and properties of cu-15ni-8sn alloy. Unknown journal, 2023. URL: https://doi.org/10.13264/j.cnki.ysjskx.2023.04.016, doi:10.13264/j.cnki.ysjskx.2023.04.016.

6. (zhaoming2023effectofrare pages 7-9): QI Zhaoming and XU Huaben. Effect of rare earth lanthanum on microstructure and properties of cu-15ni-8sn alloy. Unknown journal, 2023. URL: https://doi.org/10.13264/j.cnki.ysjskx.2023.04.016, doi:10.13264/j.cnki.ysjskx.2023.04.016.

7. (yan2025researchprogressof pages 12-15): Huan Yan, Honglei Hu, Lei Li, Wen Huang, and Chunlei Li. Research progress of cu-ni-si series alloys for lead frames. Coatings, 15:91, Jan 2025. URL: https://doi.org/10.3390/coatings15010091, doi:10.3390/coatings15010091. This article has 16 citations.

8. (yan2025researchprogressof pages 15-16): Huan Yan, Honglei Hu, Lei Li, Wen Huang, and Chunlei Li. Research progress of cu-ni-si series alloys for lead frames. Coatings, 15:91, Jan 2025. URL: https://doi.org/10.3390/coatings15010091, doi:10.3390/coatings15010091. This article has 16 citations.

9. (yan2025researchprogressof pages 21-22): Huan Yan, Honglei Hu, Lei Li, Wen Huang, and Chunlei Li. Research progress of cu-ni-si series alloys for lead frames. Coatings, 15:91, Jan 2025. URL: https://doi.org/10.3390/coatings15010091, doi:10.3390/coatings15010091. This article has 16 citations.

10. (ocejo2022corrosionbehaviorof pages 1-3): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

11. (davies1993anoteon pages 6-8): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

12. (alqadhi2026insightsintothe pages 1-2): E Alqadhi, B Han, H Jiang, and L Zhang. Insights into the dual role of la in microstructural refinement and mechanical improvement of hypomonotectic cu–24pb alloys. Unknown journal, 2026.

13. (alqadhi2026insightsintothe pages 2-3): E Alqadhi, B Han, H Jiang, and L Zhang. Insights into the dual role of la in microstructural refinement and mechanical improvement of hypomonotectic cu–24pb alloys. Unknown journal, 2026.

14. (alqadhi2026insightsintothe pages 3-4): E Alqadhi, B Han, H Jiang, and L Zhang. Insights into the dual role of la in microstructural refinement and mechanical improvement of hypomonotectic cu–24pb alloys. Unknown journal, 2026.

15. (alqadhi2026insightsintothe pages 4-8): E Alqadhi, B Han, H Jiang, and L Zhang. Insights into the dual role of la in microstructural refinement and mechanical improvement of hypomonotectic cu–24pb alloys. Unknown journal, 2026.

16. (庄玉伟2026corrosionbehaviorof pages 7-8): 杜娟， 包生重， 杨少丹， 周延军， 庄玉伟. Corrosion behavior of pre-oxidized 56cu-22ni-12fe-8al-2la anode alloy in high-temperature molten electrolyte for aluminum electrolysis. Unknown journal, 2026. URL: https://doi.org/10.12442/j.issn.1002-185x.20250607, doi:10.12442/j.issn.1002-185x.20250607.

17. (ocejo2022corrosionbehaviorof pages 5-8): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

18. (liu2024manufacturingofhigh pages 6-7): Yingang Liu, Jingqi Zhang, Ranming Niu, Mohamad Bayat, Ying Zhou, Yu Yin, Qiyang Tan, Shiyang Liu, Jesper Henri Hattel, Miaoquan Li, Xiaoxu Huang, Julie Cairney, Yi-Sheng Chen, Mark Easton, Christopher Hutchinson, and Ming-Xing Zhang. Manufacturing of high strength and high conductivity copper with laser powder bed fusion. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45732-y, doi:10.1038/s41467-024-45732-y. This article has 165 citations and is from a highest quality peer-reviewed journal.

19. (liu2024manufacturingofhigh pages 2-4): Yingang Liu, Jingqi Zhang, Ranming Niu, Mohamad Bayat, Ying Zhou, Yu Yin, Qiyang Tan, Shiyang Liu, Jesper Henri Hattel, Miaoquan Li, Xiaoxu Huang, Julie Cairney, Yi-Sheng Chen, Mark Easton, Christopher Hutchinson, and Ming-Xing Zhang. Manufacturing of high strength and high conductivity copper with laser powder bed fusion. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45732-y, doi:10.1038/s41467-024-45732-y. This article has 165 citations and is from a highest quality peer-reviewed journal.

20. (liu2024manufacturingofhigh pages 1-2): Yingang Liu, Jingqi Zhang, Ranming Niu, Mohamad Bayat, Ying Zhou, Yu Yin, Qiyang Tan, Shiyang Liu, Jesper Henri Hattel, Miaoquan Li, Xiaoxu Huang, Julie Cairney, Yi-Sheng Chen, Mark Easton, Christopher Hutchinson, and Ming-Xing Zhang. Manufacturing of high strength and high conductivity copper with laser powder bed fusion. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45732-y, doi:10.1038/s41467-024-45732-y. This article has 165 citations and is from a highest quality peer-reviewed journal.

21. (liu2024manufacturingofhigh pages 4-5): Yingang Liu, Jingqi Zhang, Ranming Niu, Mohamad Bayat, Ying Zhou, Yu Yin, Qiyang Tan, Shiyang Liu, Jesper Henri Hattel, Miaoquan Li, Xiaoxu Huang, Julie Cairney, Yi-Sheng Chen, Mark Easton, Christopher Hutchinson, and Ming-Xing Zhang. Manufacturing of high strength and high conductivity copper with laser powder bed fusion. Nature Communications, Feb 2024. URL: https://doi.org/10.1038/s41467-024-45732-y, doi:10.1038/s41467-024-45732-y. This article has 165 citations and is from a highest quality peer-reviewed journal.

22. (alqadhi2026insightsintothe pages 9-11): E Alqadhi, B Han, H Jiang, and L Zhang. Insights into the dual role of la in microstructural refinement and mechanical improvement of hypomonotectic cu–24pb alloys. Unknown journal, 2026.
