<!--
Edison Scientific LITERATURE_HIGH task (phase 1)
- Task ID: 56198956-471d-41b7-b796-170fc45cfcb9
- Submitted: 2026-10-17T19:02:08Z
- Fetched: 2026-10-17T19:35:26Z (status: success)
- Raw trajectory JSON: ../raw/joint-shortlist.json.gz
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

TASK: JOINT BOUNDS AND PALETTE. Separate per-element questions are running for
50 elements. This question looks at them together. Candidate short list
(Cu as balance): Ni, Al, Fe, Mn, Cr, Sn, Zn, Si, Nb, Ti, Zr, Co, Mg, B, P, Ce, La, Y, Be, Ag; impurities C, S, P, Pb, Bi, O, H, N.

1. Which 8-15 of the short-listed elements should form the search palette for
   the stated goal (as-deposited seawater resistance at least equal to C71500,
   crack-free blown-powder DED on itself and on cast NAB and wrought Cu-Ni,
   lower nickel), and which should be dropped or kept as impurity limits?
   Rank them and give the reason for each.
2. One consolidated markdown table for the chosen palette plus Cu: lower
   bound, conservative upper bound, non-conservative upper bound (wt%), the
   failure mode setting the upper bound, and key citations. Give Cu_min.
3. Joint constraints tighter than the per-element bounds, with numbers and
   sources, for example: the aluminum equivalent for retained beta or
   martensite in aluminum bronzes (Al + factors x Mn, Si, Sn, Zn, Ni, Fe), the
   Fe/Ni ratio and kappa phase control in NAB, Fe and Mn together in Cu-Ni
   (Fe in solid solution), Cr with Fe and Si in Cr-modified Cu-Ni, the zinc
   equivalent in brasses, total solute versus liquidus (the alloy liquidus must
   stay below about 1,250 C, which caps Ni near 30 wt% in Cu-Ni), and impurity
   sums (Pb + S + P + C) for weldability.
4. Should the space be one continuous Cu-Ni-Al-Fe-Mn-... simplex or two
   sub-spaces (Cu-Ni branch, aluminum bronze branch)? What lies between them
   (e.g. Cu-Ni-Al alloys such as MARINEL or cast Cu-7Ni-3Al), and is that
   region worth searching?
5. Which pairs and ternaries in the palette are assessed in Thermo-Calc TCCU
   (or published CALPHAD work) and which rely on extrapolation only?

Express every composition in wt%. Cite peer-reviewed work, standards and
handbooks with DOIs where available. Say plainly where evidence is thin.

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

TASK: JOINT BOUNDS AND PALETTE. Separate per-element questions are running for
50 elements. This question looks at them together. Candidate short list
(Cu as balance): Ni, Al, Fe, Mn, Cr, Sn, Zn, Si, Nb, Ti, Zr, Co, Mg, B, P, Ce, La, Y, Be, Ag; impurities C, S, P, Pb, Bi, O, H, N.

1. Which 8-15 of the short-listed elements should form the search palette for
   the stated goal (as-deposited seawater resistance at least equal to C71500,
   crack-free blown-powder DED on itself and on cast NAB and wrought Cu-Ni,
   lower nickel), and which should be dropped or kept as impurity limits?
   Rank them and give the reason for each.
2. One consolidated markdown table for the chosen palette plus Cu: lower
   bound, conservative upper bound, non-conservative upper bound (wt%), the
   failure mode setting the upper bound, and key citations. Give Cu_min.
3. Joint constraints tighter than the per-element bounds, with numbers and
   sources, for example: the aluminum equivalent for retained beta or
   martensite in aluminum bronzes (Al + factors x Mn, Si, Sn, Zn, Ni, Fe), the
   Fe/Ni ratio and kappa phase control in NAB, Fe and Mn together in Cu-Ni
   (Fe in solid solution), Cr with Fe and Si in Cr-modified Cu-Ni, the zinc
   equivalent in brasses, total solute versus liquidus (the alloy liquidus must
   stay below about 1,250 C, which caps Ni near 30 wt% in Cu-Ni), and impurity
   sums (Pb + S + P + C) for weldability.
4. Should the space be one continuous Cu-Ni-Al-Fe-Mn-... simplex or two
   sub-spaces (Cu-Ni branch, aluminum bronze branch)? What lies between them
   (e.g. Cu-Ni-Al alloys such as MARINEL or cast Cu-7Ni-3Al), and is that
   region worth searching?
5. Which pairs and ternaries in the palette are assessed in Thermo-Calc TCCU
   (or published CALPHAD work) and which rely on extrapolation only?

Express every composition in wt%. Cite peer-reviewed work, standards and
handbooks with DOIs where available. Say plainly where evidence is thin.


## Joint Bounds and Palette for Pre-Alloyed Copper Alloy Powders for Single-Stream Blown-Powder Laser DED

### 1. Recommended Element Palette (12 elements + Cu balance)

The following 12 elements are recommended for the search palette, ranked by importance. Elements are selected based on their demonstrated roles in seawater corrosion resistance, DED processability, phase stability, and compatibility with the AMAZEMET ultrasonic atomizer constraints (~1,250 °C maximum liquidus).

**Tier 1 — Primary solutes (define the alloy family):**

1. **Ni (0–30 wt%)** — The single most important element for matching C71500-class seawater resistance. Ni enriches the protective Cu₂O/hydroxychloride corrosion film, suppresses dealloying, and improves erosion-corrosion resistance (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 19-21). It also increases laser absorptivity relative to pure Cu (canacoo2026laseradditivemanufacturing pages 10-12). The liquidus constraint caps practical Ni near 30 wt% for atomization. Lower Ni is a secondary objective.

2. **Al (0–12 wt%)** — Enables the aluminum bronze branch: Al₂O₃-rich corrosion films, high strength, and demonstrated laser DED processability at 6–12 wt% Al (canacoo2026laseradditivemanufacturing pages 12-14). Above ~9.5 wt% Al (the C95800 upper limit), retained β′ martensite becomes problematic under rapid DED cooling (iorio2015determinationofrolling pages 17-23, kuprienko2025analysisofnickel pages 30-36, kuprienko2025analysisofnickela pages 30-36). At 14 wt% Al, brittle intermetallic fracture was reported in laser AM (canacoo2026laseradditivemanufacturing pages 12-14).

3. **Fe (0–6 wt%)** — Essential in both families. In Cu-Ni, 1.0–1.8 wt% Fe (C70600) improves the passive film resistivity and impingement resistance; in NAB, 3.5–4.5 wt% Fe refines grains and forms beneficial κ phases (cuevas2002microstructurecharacterizationof pages 21-26, lewis1981evaluationofcoppernickel pages 17-19, cuevas2002microstructurecharacterizationof pages 26-29). Excess or out-of-solution Fe causes crevice corrosion, pitting, blistering, and SCC (lewis1981evaluationofcoppernickel pages 17-19, tuck2005thedevelopmentof pages 5-7).

4. **Mn (0–4 wt%)** — Improves corrosion resistance in Cu-Ni alloys, deoxidizes the melt, and is a β-stabilizer in aluminum bronzes (konynenburg1990backgroundstudiesin pages 149-155, phull20172.18–marine pages 27-28). In MARINEL alloys, Mn is typically 3.8–5.3 wt% (tuck2005thedevelopmentof media 4b9488e1, tuck2005thedevelopmentof media bfa83429). Mn vapor/oxidation during atomization and DED limits practical use.

**Tier 2 — Secondary solutes (improve specific properties):**

5. **Cr (0–1.5 wt%)** — C72200 (Cu-16Ni-0.5Cr) shows exceptional erosion-corrosion resistance at velocities up to 4.6 m/s (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 14-17). CuCrZr has been successfully laser-AM processed to 99.99% density (canacoo2026laseradditivemanufacturing pages 10-12). However, Cr segregation in stagnant seawater can promote localized attack (phull20172.18–marine pages 27-28).

6. **Sn (0–2.5 wt%)** — At ~1 wt%, Sn refines NAB grain structure from columnar to equiaxed and modifies κ-phase morphology (poojary2023enhancingmicrostructureand pages 1-2, poojary2023enhancingmicrostructureand pages 6-8, poojary2023enhancingmicrostructureand pages 2-3). A 0.3 wt% Sn coating improved Cu laser absorptivity from 19% to 51% (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 9-10). Above ~1 wt%, Sn-rich grain-boundary phases form; Cu-Ni-Sn alloys are susceptible to intergranular SCC in ammonium and sulfide environments (tuck2005thedevelopmentof pages 1-3, tuck2005thedevelopmentof pages 5-7).

7. **Si (0–1.0 wt%)** — Deoxidizer and solid-solution strengthener; ~0.4% Si needed in cast 70-30 Cu-Ni to meet tensile requirements (konynenburg1990backgroundstudiesin pages 149-155). CuNiSi alloys (1.5–3% Si) have been successfully printed by LPBF (canacoo2026laseradditivemanufacturing pages 10-12). C95800 limits Si to 0.10 wt% to avoid detrimental silicides.

8. **Nb (0–1.5 wt%)** — Grain refiner and ε-phase former in MARINEL (Cu-Ni-Al-Mn-Nb, UNS C72420), where it promotes Ni₃Al precipitation effectiveness (tuck2005thedevelopmentof pages 1-3, tuck2005thedevelopmentof pages 7-11, tuck2005thedevelopmentof media 4b9488e1, tuck2005thedevelopmentof media bfa83429). Cu-Cr-Nb (GRCop-42) has been successfully DED-processed (canacoo2026laseradditivemanufacturing pages 10-12, canacoo2026laseradditivemanufacturing pages 12-14). Risk: coarse Nb intermetallics, high liquidus, and grain-boundary ε precipitates that may impair SCC resistance if Fe is also high (tuck2005thedevelopmentof pages 5-7).

**Tier 3 — Microalloying probes (small additions, exploratory):**

9. **Ti (0–0.80 wt%)** — Potential grain refiner and oxide/nitride former. Risk: oxide scavenging, crucible reactions, poor recovery. Direct seawater-DED evidence is thin; bounds are provisional.

10. **Zr (0–0.50 wt%)** — Grain refiner in CuCrZr systems with demonstrated laser-AM processability (canacoo2026laseradditivemanufacturing pages 10-12). Risk: reaction with alumina/zirconia crucibles, ZrO₂ inclusions, poor atomization recovery.

11. **B (0–0.10 wt%)** — Potential grain-boundary modifier at very low levels. Risk: low-melting grain-boundary films, hot cracking, poor compositional control at 0.5 kg scale. No direct marine Cu evidence.

12. **Ce or Y (0–0.20 wt%, single RE variable)** — Rare-earth additions at ~0.04 wt% refine brass grains and scavenge S/O (poojary2023enhancingmicrostructureand pages 1-2). Y₂O₃ dispersoids demonstrated in oxide-dispersion Cu-Cr-Nb (canacoo2026laseradditivemanufacturing pages 12-14). Risk: rapid oxygen scavenging creates inclusions, nozzle blockage, and poor recovery.

**Elements dropped from the palette:**

- **Zn** — Dropped as a design variable due to dezincification risk in seawater, volatilization/fume during melting and DED, and composition drift (phull20172.18–marine pages 28-29). Retain only as an impurity limit (≤0.50 wt% conservative).
- **Be** — Excluded entirely due to severe inhalation toxicity (chronic beryllium disease) during powder handling and atomization, incompatible with a university laboratory setting (canacoo2026laseradditivemanufacturing pages 12-14). The EU occupational exposure limit is 0.2 µg/m³.
- **Co** — Dropped due to cost, toxicity concerns in powder form, and limited demonstrated benefit over Fe+Ni in these alloy families. Co is also a US critical mineral.
- **Mg** — Dropped due to extreme oxidation, vapor pressure, poor recovery in Cu melting, and reaction with alumina crucibles. No demonstrated seawater Cu-alloy benefit.
- **Ag** — Dropped as a primary variable due to cost and limited corrosion benefit beyond what Ni provides. Cu-Ag in-situ AM has been demonstrated but targets conductivity, not marine service (canacoo2026laseradditivemanufacturing pages 12-14).
- **P** — Retained only as an impurity limit, not a design variable. Although a deoxidizer, residual P segregates to grain boundaries and promotes hot cracking.
- **La** — Merged into the single RE slot (Ce or Y preferred for better CALPHAD coverage).

### 2. Consolidated Composition Table

The table below provides bounds, failure modes, and citations for all palette elements plus Cu and impurity limits.

| Element | Lower Bound (wt%) | Conservative Upper Bound (wt%) | Non-Conservative Upper Bound (wt%) | Failure Mode Setting Upper Bound | Key Citations |
|---|---:|---:|---:|---|---|
| **Cu (balance)** | **65.0 minimum** | Balance | **60.0 minimum** | Below 65.0, the space increasingly leaves established Cu–Ni/NAB metallurgy; excessive total solute raises liquidus, freezing range, intermetallic fraction, segregation, and selective-corrosion risk. Treat 60.0–65.0 as exploratory only. | Cu ≥79.0 in C95800 (cuevas2002microstructurecharacterizationof pages 26-29, kuprienko2025analysisofnickel pages 30-36); marine copper-alloy film behavior (phull20172.18–marine pages 27-28, phull20172.18–marine pages 25-27) |
| **Ni** | 0 | 20.0 | 30.0 | Critical-mineral burden; higher liquidus and insufficient atomization superheat near 30.0; segregation and increasingly Ni-rich metallurgy. Ni is nevertheless the strongest established route to C71500-class seawater resistance and should exceed Fe in the NAB branch. | Cu–Ni seawater performance (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 19-21); Ni > Fe in NAB (cuevas2002microstructurecharacterizationof pages 21-26, cuevas2002microstructurecharacterizationof pages 26-29) |
| **Al** | 0 | 9.5 | 12.0 | Retained β/β′ martensite, selective Al attack, brittle intermetallics, and loss of ductility as Al equivalent rises; 14.0 Al caused brittle-phase fracture in laser-AM Cu–Al. | C95800: 8.5–9.5 Al (cuevas2002microstructurecharacterizationof pages 26-29, kuprienko2025analysisofnickel pages 30-36); rapid-cooling martensite (iorio2015determinationofrolling pages 17-23, kuprienko2025analysisofnickela pages 30-36); AM Cu–Al limit (canacoo2026laseradditivemanufacturing pages 12-14); selective Al attack (phull20172.18–marine pages 28-29) |
| **Fe** | 0 | 4.5 | 6.0 | Fe-rich κ phases or segregated/intergranular precipitates cause localized corrosion and SCC; in Cu–Ni, excess or out-of-solution Fe promotes crevice attack, pitting, and blistering. | C95800: 3.5–4.5 Fe (cuevas2002microstructurecharacterizationof pages 26-29, kuprienko2025analysisofnickel pages 30-36); Cu–Ni optimum and excess-Fe failures (lewis1981evaluationofcoppernickel pages 17-19, konynenburg1990backgroundstudiesin pages 149-155); NAB Fe guidance (cuevas2002microstructurecharacterizationof pages 21-26); SCC association (tuck2005thedevelopmentof pages 3-5, tuck2005thedevelopmentof pages 5-7) |
| **Mn** | 0 | 2.0 | 4.0 | Mn oxidation/fume and evaporation during induction melting, atomization, and DED; oxide inclusions, composition drift, and excessive β stabilization. Values above 2.0 have thin direct evidence for as-deposited seawater DED. | C95800: 0.8–1.5 Mn (cuevas2002microstructurecharacterizationof pages 26-29, kuprienko2025analysisofnickel pages 30-36); beneficial Cu–Ni corrosion role (konynenburg1990backgroundstudiesin pages 149-155, phull20172.18–marine pages 27-28); higher-Mn bronze precedent (iorio2015determinationofrolling pages 17-23) |
| **Cr** | 0 | 0.8 | 1.5 | Low Cu solubility causes Cr-rich segregation/particles, nozzle or crucible residue, and localized attack in stagnant seawater; excessive Cr can broaden the solidification interval. | C72200 contains about 0.5 Cr (lewis1981evaluationofcoppernickel pages 14-17); high-flow benefit but stagnant-water penalty (lewis1981evaluationofcoppernickel pages 17-19, phull20172.18–marine pages 27-28); CuCrZr laser-AM precedent (canacoo2026laseradditivemanufacturing pages 10-12) |
| **Sn** | 0 | 1.0 | 2.5 | Sn-rich grain-boundary phases, segregation, and environmentally assisted intergranular cracking; Cu–Ni–Sn SCC evidence argues against using Sn as a major solute without separate qualification. | NAB optimum near 1.0 Sn and grain-boundary phases above it (poojary2023enhancingmicrostructureand pages 1-2, poojary2023enhancingmicrostructureand pages 6-8, poojary2023enhancingmicrostructureand pages 2-3); Cu–Ni–Sn SCC concern (tuck2005thedevelopmentof pages 1-3, tuck2005thedevelopmentof pages 5-7); 0.3 Sn improves laser processing (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 10-12) |
| **Si** | 0 | 0.30 | 1.0 | Ni–Si/Fe–Si intermetallics, loss of Fe in solid solution, galvanically distinct precipitates, and hot cracking; C95800 limits Si to 0.10. Higher levels belong only in a designed Cr–Ni–Si sub-branch. | C95800 Si ≤0.10 (cuevas2002microstructurecharacterizationof pages 26-29); casting/strengthening use around 0.10–0.50 (konynenburg1990backgroundstudiesin pages 149-155); printable Cu–Ni–Si alloys (canacoo2026laseradditivemanufacturing pages 10-12) |
| **Nb** | 0 | 0.50 | 1.5 | Coarse Nb-rich intermetallics or undissolved particles, segregation, high liquidus, poor atomization recovery, and grain-boundary ε-type precipitates. Evidence for seawater corrosion in as-deposited Cu alloys is thin. | MARINEL Cu–Ni–Al–Mn–Nb precedent (tuck2005thedevelopmentof pages 1-3, tuck2005thedevelopmentof pages 7-11, tuck2005thedevelopmentof media 4b9488e1); Nb-bearing grain-boundary precipitates (tuck2005thedevelopmentof pages 3-5, tuck2005thedevelopmentof pages 5-7); Cu–Cr–Nb DED precedent (canacoo2026laseradditivemanufacturing pages 10-12, canacoo2026laseradditivemanufacturing pages 12-14) |
| **Ti** | 0 | 0.20 | 0.80 | Ti oxide/nitride formation, oxygen scavenging into inclusions, ceramic-crucible reactions, coarse Ti-rich intermetallics, and poor recovery during atomization. Direct seawater-DED evidence is thin; bound is provisional. | General copper laser-AM alloy-design constraints (canacoo2026laseradditivemanufacturing pages 12-14, canacoo2026laseradditivemanufacturing pages 32-34); evidence beyond these process precedents is thin |
| **Zr** | 0 | 0.15 | 0.50 | ZrO₂/inclusion formation, reaction with alumina/zirconia crucibles, loss during atomization, nozzle deposits, and coarse Cu–Zr intermetallics. Direct seawater evidence is thin; bound is provisional. | CuCrZr laser-AM processability precedent (canacoo2026laseradditivemanufacturing pages 10-12); general oxidation/process constraints (canacoo2026laseradditivemanufacturing pages 1-2, canacoo2026laseradditivemanufacturing pages 32-34) |
| **B** | 0 | 0.02 | 0.10 | Low-melting grain-boundary films or hard borides, hot cracking, embrittlement, and very poor compositional control at 0.5 kg melt scale. No persuasive marine Cu-alloy evidence supports higher additions; retain only as a microalloying probe. | General grain-boundary/solidification-cracking concerns in laser AM (canacoo2026laseradditivemanufacturing pages 1-2, canacoo2026laseradditivemanufacturing pages 34-35); direct Cu–Ni/NAB evidence is thin |
| **RE slot: Ce or Y** | 0 | 0.05 | 0.20 | Rapid scavenging of O/S creates oxide/oxysulfide inclusions, nozzle blockage, poor recovery, and galvanically active particles; use one RE variable, not independent Ce and Y dimensions. | Rare-earth additions near 0.04 can refine brass grains (poojary2023enhancingmicrostructureand pages 1-2); oxide-dispersion AM precedent for Y (canacoo2026laseradditivemanufacturing pages 12-14); copper-specific seawater evidence is thin |
| **Pb — impurity limit** | 0 | 0.010 | 0.030 | Insoluble, low-melting grain-boundary films cause hot shortness and solidification cracking; also unacceptable for marine release. C95800 permits no more than 0.03. | C95800 Pb ≤0.03 (cuevas2002microstructurecharacterizationof pages 26-29); low-melting impurities and hot cracking (kuprienko2025analysisofnickel pages 30-36) |
| **S — impurity limit** | 0 | 0.005 | 0.010 | Cu–S/Ni–S low-melting films, hot cracking, porosity, and severe degradation of protective-film formation in seawater. | Sulfide damage to Cu alloys (phull20172.18–marine pages 25-27); Cu–Ni–Sn/S environmental cracking evidence (tuck2005thedevelopmentof pages 1-3, tuck2005thedevelopmentof pages 5-7) |
| **P — impurity limit** | 0 | 0.010 | 0.030 | Although useful as a deoxidizer, residual P segregates to grain boundaries and promotes hot cracking; it may also segregate with κ phases in NAB. Do not treat P as a design solute in the first campaign. | Low-melting impurity/weldability concern (kuprienko2025analysisofnickel pages 30-36); general copper deoxidation context (konynenburg1990backgroundstudiesin pages 149-155) |
| **C — impurity limit** | 0 | 0.010 | 0.030 | Carbonaceous contamination, gas evolution, inclusions, poor wetting, and porosity; no demonstrated seawater benefit in these alloy families. | General copper laser-AM porosity and atmosphere sensitivity (canacoo2026laseradditivemanufacturing pages 1-2, canacoo2026laseradditivemanufacturing pages 34-35) |
| **Bi — impurity limit** | 0 | 0.001 | 0.005 | Extremely low Cu solubility and low-melting grain-boundary films produce severe hot shortness and cracking; tighter than Pb is warranted. | Low-melting impurity/weldability principle (kuprienko2025analysisofnickel pages 30-36); direct quantitative DED evidence is thin |
| **O — interstitial limit** | 0 | 0.020 | 0.050 | Oxide inclusions, hydrogen–oxygen steam porosity, reduced ductility, unstable powder surfaces, and loss of reactive Ti/Zr/RE solutes. Specify separately for melt, powder, and deposit. | Oxidation sensitivity in laser AM (canacoo2026laseradditivemanufacturing pages 1-2, canacoo2026laseradditivemanufacturing pages 34-35, canacoo2026laseradditivemanufacturing pages 32-34) |
| **H — interstitial limit** | 0 | 0.0005 | 0.0010 | Gas porosity and steam reaction with dissolved oxygen; hydrogen-assisted cracking becomes relevant in high-strength Cu–Ni–Al precipitate systems. | MARINEL hydrogen testing (tuck2005thedevelopmentof pages 1-3, tuck2005thedevelopmentof pages 3-5); general AM porosity mechanisms (canacoo2026laseradditivemanufacturing pages 34-35) |
| **N — interstitial limit** | 0 | 0.005 | 0.020 | Nitride inclusions with Ti/Zr/RE, porosity, and uncertain recovery; evidence for beneficial N alloying in marine Cu alloys is absent. | General atmosphere/oxidation control in copper AM (canacoo2026laseradditivemanufacturing pages 1-2, canacoo2026laseradditivemanufacturing pages 2-4); direct evidence is thin |
| **Zn — impurity / optional separate branch** | 0 | 0.50 | 5.0 | Volatilization during melting/DED, composition drift and fumes; increasing Zn raises dezincification and ammonia-SCC risk. Do not include Zn as a primary continuous variable unless a distinct low-Zn bronze/brass sub-study is funded. | Dezincification and preferential β-brass attack (phull20172.18–marine pages 28-29); seawater brass corrosion (phull20172.18–marine pages 27-28); inhibitor evidence (poojary2023enhancingmicrostructureand pages 1-2) |


*Table: Recommended composition bounds for the DED copper-alloy design palette, with Cu as balance and separate impurity controls. Conservative limits define the primary search, while non-conservative limits identify exploratory compositions requiring stronger process and corrosion validation.*

### 3. Joint Constraints Tighter Than Per-Element Bounds

The following multi-element constraints must be applied on top of the individual bounds:

**a) Aluminum Equivalent for β/β′ retention in aluminum bronzes.** The classical Brezina aluminum equivalent is: Al_eq = %Al + ¼(%Mn) + ⅙(%Si) + ½(%Sn) − ⅙(%Ni) − (some fraction)(%Fe). When Al_eq exceeds approximately 9.4 wt%, β is retained at room temperature and transforms to martensite β′ under rapid cooling, which is particularly problematic in DED where cooling rates are high (iorio2015determinationofrolling pages 17-23, kuprienko2025analysisofnickel pages 30-36, kuprienko2025analysisofnickela pages 30-36). The constraint for the aluminum-bronze branch should be: **Al_eq ≤ 9.0** (conservative) or **≤ 9.4** (non-conservative). Note: the exact coefficients vary among sources (Brezina 1982, doi:10.1179/imr.1982.27.1.77, was unobtainable); evidence for the precise formula in as-deposited DED conditions is thin and should be refined with Thermo-Calc Scheil calculations.

**b) Ni > Fe in the NAB branch.** For maximum seawater corrosion resistance, the nickel content should exceed the iron content; the ideal cited ratio is approximately 5 wt% Ni to 4 wt% Fe (cuevas2002microstructurecharacterizationof pages 21-26, cuevas2002microstructurecharacterizationof pages 26-29). When Ni < Fe, severe selective second-phase attack occurs in seawater.

**c) Fe in solid solution in Cu-Ni.** In 70-30 Cu-Ni (C71500), Fe must be ≤ ~2 wt% total and retained in solid solution; above 2 wt%, crevice corrosion and pitting increase (lewis1981evaluationofcoppernickel pages 17-19). In 90-10 Cu-Ni (C70600), the specified range is 1.0–1.8 wt% Fe, with an optimum near 1.5 wt% (lewis1981evaluationofcoppernickel pages 17-19, lewis1981evaluationofcoppernickel pages 14-17). In high-strength Cu-Ni-Al-Mn-Nb (MARINEL), Fe is restricted to a maximum of approximately 1.0 wt% to avoid SCC (tuck2005thedevelopmentof pages 5-7, tuck2005thedevelopmentof media 9e3cf1ab). **Constraint: Fe ≤ 1.0 wt% in the Cu-Ni-Al branch; Fe ≤ 2.0 wt% in the Cu-Ni branch; Fe 3.5–4.5 wt% only in the NAB branch where Ni > Fe.**

**d) Fe + Mn solubility in Cu-Ni.** Fe and Mn together must remain in solid solution for corrosion-film benefit. In Cu-30Ni, Fe + Mn should not exceed approximately 2.5 wt% total to avoid precipitation during DED thermal cycling. In Cu-10Ni, the combined solubility is somewhat higher but still limited.

**e) Cr with Fe and Si.** Cr-modified Cu-Ni (C72200 type) contains ~0.5 wt% Cr with ~0.5 wt% Fe and small Si. Cr requires Fe for dispersion-strengthening synergy, but Cr segregation in stagnant seawater impairs localized-corrosion resistance (lewis1981evaluationofcoppernickel pages 17-19, phull20172.18–marine pages 27-28). **Constraint: If Cr > 0.3 wt%, then Fe should be ≥ 0.5 wt% and Si ≤ 0.5 wt%.**

**f) Zinc equivalent.** Although Zn is excluded as a variable, any residual Zn should satisfy the zinc equivalent: Zn_eq = %Zn + factors for other β-stabilizers. To avoid dezincification risk entirely, keep Zn_eq < 15 wt% (phull20172.18–marine pages 28-29).

**g) Liquidus temperature constraint.** The alloy liquidus must stay below ~1,250 °C for adequate superheat in the AMAZEMET atomizer (induction module reaches ~1,300 °C). In the Cu-Ni binary, 30 wt% Ni gives a liquidus of approximately 1,240 °C (lewis1981evaluationofcoppernickel pages 14-17). This effectively caps Ni at ~30 wt%. In the NAB branch, C95800 compositions have liquidus temperatures well below 1,100 °C. **The constraint is applied via Thermo-Calc liquidus calculation for each candidate composition: T_liquidus ≤ 1,250 °C.**

**h) Impurity sums for weldability/DED cracking resistance.** Low-melting-point impurities that segregate to grain boundaries cause solidification cracking. **Constraint: Pb + Bi ≤ 0.015 wt%; S + P ≤ 0.020 wt%; total (Pb + S + P + C + Bi) ≤ 0.050 wt%.** These are conservative targets adapted from copper welding practice (kuprienko2025analysisofnickel pages 30-36, konynenburg1990backgroundstudiesin pages 149-155).

### 4. One Continuous Space vs. Two Sub-Spaces

**Recommendation: Use one continuous simplex with soft sub-region constraints, not two hard-split sub-spaces.** The rationale is as follows:

The Cu-Ni branch (C71500 type: ~30Ni, ~1Fe, ~1Mn, no Al) and the aluminum bronze branch (C95800 type: ~9Al, ~5Ni, ~4Fe, ~1Mn, no excess Ni) occupy different corners of the composition space. Between them lies the Cu-Ni-Al family, exemplified by:

- **MARINEL (UNS C72420 type):** ~15–25 Ni, ~1.6–2.3 Al, ~3.8–5.3 Mn, ~0.6–1.2 Fe, ~0.6–0.9 Nb, ~0.35–0.48 Cr, Cu balance. These alloys achieve 0.2% proof stress over 700 N/mm² and are resistant to hydrogen embrittlement, sulfide SCC, and ammonia SCC (tuck2005thedevelopmentof pages 1-3, tuck2005thedevelopmentof media 4b9488e1, tuck2005thedevelopmentof media bfa83429).
- **Cu-7Ni-3Al (cast alloys):** Intermediate compositions with ~7 Ni and ~3 Al, used in marine castings.

The MARINEL compositions demonstrate that the region between conventional Cu-Ni and NAB is not only metallurgically viable but offers exceptional properties. The Ni₃Al (γ′) precipitation hardening mechanism operates across a broad Ni-Al range, and the seawater corrosion resistance is maintained by the Cu-Ni matrix (tuck2005thedevelopmentof pages 1-3, tuck2005thedevelopmentof pages 7-11). **This intermediate region is worth searching and may be the most promising territory for low-Ni, high-performance alloys.**

However, soft constraints should guide the optimizer:
- In compositions with Al > 7 wt%, enforce Al_eq ≤ 9.0 and Ni > Fe (NAB rules).
- In compositions with Al < 2 wt%, enforce Fe in solid solution and standard Cu-Ni film constraints.
- In intermediate compositions (2 < Al < 7 wt%), both constraint sets apply in blended form.

### 5. Thermo-Calc TCCU Database Coverage

The TCCU (Thermo-Calc Copper) database is specifically designed for copper-based alloys and contains critically assessed thermodynamic descriptions for the following relevant systems. However, coverage varies:

**Binary systems likely assessed in TCCU:**
- Cu-Ni, Cu-Al, Cu-Fe, Cu-Mn, Cu-Sn, Cu-Zn, Cu-Si, Cu-Cr, Cu-Ti, Cu-Zr, Cu-Co, Cu-Ag, Cu-P, Cu-B, Cu-Pb, Cu-S — These are core copper binaries and are expected to be assessed in the current TCCU database version.
- Ni-Al, Ni-Fe, Fe-Al, Fe-Mn, Ni-Mn, Al-Mn — These important sub-binaries are typically assessed from TCNI or TCFE databases and cross-assessed in TCCU.

**Ternary systems likely assessed:**
- Cu-Ni-Al, Cu-Ni-Fe, Cu-Ni-Sn, Cu-Al-Fe, Cu-Al-Ni, Cu-Ni-Mn, Cu-Al-Mn, Cu-Zn-Sn, Cu-Ni-Si, Cu-Cr-Zr — These are commercially important ternaries for copper alloy design and are expected to be assessed.
- Cu-Al-Fe-Ni (the NAB quaternary core) — Likely assessed given the industrial importance of NAB.

**Systems relying on extrapolation (evidence is thin):**
- Cu-Nb, Cu-Ce, Cu-La, Cu-Y — Nb, Ce, La, and Y are not traditional copper alloying elements. While Cu-Nb may have a basic assessment, rare-earth binaries and ternaries (Cu-Ni-Nb, Cu-Al-Nb, Cu-Ni-Ce, Cu-Ni-Y) are likely extrapolated from limited data or absent entirely. **Recommendation: validate any TCCU predictions involving Nb, Ce, or Y against published phase-diagram data before using them for alloy screening.**
- Cu-B — Boron in copper is poorly characterized; predictions should be treated with caution.
- Cu-Ti-Zr, Cu-Ni-Ti, Cu-Ni-Zr — Some assessment may exist from precipitation-hardening alloy work, but coverage depth is uncertain.
- Cu-Fe-Cr, Cu-Ni-Cr — Chromium-modified Cu-Ni ternaries may have basic assessment but are less thoroughly validated than Cu-Ni-Fe.

**Practical recommendation:** Use `pycalphad` with TCCU to compute the liquidus surface and phase fractions for all candidate compositions. For elements outside the well-assessed core (Nb, Ti, Zr, B, Ce, Y), cross-check predictions against published experimental phase diagrams. The TCCU database documentation should be consulted for the specific version being used, as coverage expands with each release. Where TCCU coverage is insufficient, supplementary databases (TCNI for Ni-rich corners, or user-defined parameters from published CALPHAD assessments) may be needed.

**Caveat on evidence depth:** The specific systems assessed in TCCU are not publicly documented in the peer-reviewed literature in a way that could be retrieved here. The above assessment is based on general knowledge of CALPHAD database scope for copper alloys and should be verified against the actual TCCU database documentation available to the PI through their Thermo-Calc license.


References

1. (lewis1981evaluationofcoppernickel pages 17-19): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

2. (lewis1981evaluationofcoppernickel pages 14-17): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

3. (lewis1981evaluationofcoppernickel pages 19-21): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

4. (canacoo2026laseradditivemanufacturing pages 10-12): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

5. (canacoo2026laseradditivemanufacturing pages 12-14): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

6. (iorio2015determinationofrolling pages 17-23): G Iorio. Determination of rolling parameters for numerical simulation of cold rolling of nickel aluminum bronze. Unknown journal, 2015.

7. (kuprienko2025analysisofnickel pages 30-36): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

8. (kuprienko2025analysisofnickela pages 30-36): A Kuprienko. Analysis of nickel aluminum bronze weld metal microstructure and mechanical response as a function of cooling rate. Unknown journal, 2025.

9. (cuevas2002microstructurecharacterizationof pages 21-26): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.

10. (cuevas2002microstructurecharacterizationof pages 26-29): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.

11. (tuck2005thedevelopmentof pages 5-7): Clive D S Tuck. The development of very high strength copper alloys with resistance to hydrogen embrittlement and stress corrosion cracking. CORROSION 2005, pages 1-15, Apr 2005. URL: https://doi.org/10.5006/c2005-05462, doi:10.5006/c2005-05462. This article has 10 citations.

12. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

13. (phull20172.18–marine pages 27-28): B Phull and AA Abdullahi. 2.18 – marine corrosion. ArXiv, 2:1107-1148, Jan 2017. URL: https://doi.org/10.1016/b978-044452787-5.00046-9, doi:10.1016/b978-044452787-5.00046-9. This article has 61 citations.

14. (tuck2005thedevelopmentof media 4b9488e1): Clive D S Tuck. The development of very high strength copper alloys with resistance to hydrogen embrittlement and stress corrosion cracking. CORROSION 2005, pages 1-15, Apr 2005. URL: https://doi.org/10.5006/c2005-05462, doi:10.5006/c2005-05462. This article has 10 citations.

15. (tuck2005thedevelopmentof media bfa83429): Clive D S Tuck. The development of very high strength copper alloys with resistance to hydrogen embrittlement and stress corrosion cracking. CORROSION 2005, pages 1-15, Apr 2005. URL: https://doi.org/10.5006/c2005-05462, doi:10.5006/c2005-05462. This article has 10 citations.

16. (poojary2023enhancingmicrostructureand pages 1-2): Sushanth Poojary, Vikas Marakini, Rajath N. Rao, and Vijeesh Vijayan. Enhancing microstructure and mechanical properties of nickel aluminium bronze alloy through tin addition. Scientific Reports, Oct 2023. URL: https://doi.org/10.1038/s41598-023-44146-y, doi:10.1038/s41598-023-44146-y. This article has 16 citations and is from a peer-reviewed journal.

17. (poojary2023enhancingmicrostructureand pages 6-8): Sushanth Poojary, Vikas Marakini, Rajath N. Rao, and Vijeesh Vijayan. Enhancing microstructure and mechanical properties of nickel aluminium bronze alloy through tin addition. Scientific Reports, Oct 2023. URL: https://doi.org/10.1038/s41598-023-44146-y, doi:10.1038/s41598-023-44146-y. This article has 16 citations and is from a peer-reviewed journal.

18. (poojary2023enhancingmicrostructureand pages 2-3): Sushanth Poojary, Vikas Marakini, Rajath N. Rao, and Vijeesh Vijayan. Enhancing microstructure and mechanical properties of nickel aluminium bronze alloy through tin addition. Scientific Reports, Oct 2023. URL: https://doi.org/10.1038/s41598-023-44146-y, doi:10.1038/s41598-023-44146-y. This article has 16 citations and is from a peer-reviewed journal.

19. (canacoo2026laseradditivemanufacturing pages 14-15): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

20. (canacoo2026laseradditivemanufacturing pages 9-10): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

21. (tuck2005thedevelopmentof pages 1-3): Clive D S Tuck. The development of very high strength copper alloys with resistance to hydrogen embrittlement and stress corrosion cracking. CORROSION 2005, pages 1-15, Apr 2005. URL: https://doi.org/10.5006/c2005-05462, doi:10.5006/c2005-05462. This article has 10 citations.

22. (tuck2005thedevelopmentof pages 7-11): Clive D S Tuck. The development of very high strength copper alloys with resistance to hydrogen embrittlement and stress corrosion cracking. CORROSION 2005, pages 1-15, Apr 2005. URL: https://doi.org/10.5006/c2005-05462, doi:10.5006/c2005-05462. This article has 10 citations.

23. (phull20172.18–marine pages 28-29): B Phull and AA Abdullahi. 2.18 – marine corrosion. ArXiv, 2:1107-1148, Jan 2017. URL: https://doi.org/10.1016/b978-044452787-5.00046-9, doi:10.1016/b978-044452787-5.00046-9. This article has 61 citations.

24. (phull20172.18–marine pages 25-27): B Phull and AA Abdullahi. 2.18 – marine corrosion. ArXiv, 2:1107-1148, Jan 2017. URL: https://doi.org/10.1016/b978-044452787-5.00046-9, doi:10.1016/b978-044452787-5.00046-9. This article has 61 citations.

25. (tuck2005thedevelopmentof pages 3-5): Clive D S Tuck. The development of very high strength copper alloys with resistance to hydrogen embrittlement and stress corrosion cracking. CORROSION 2005, pages 1-15, Apr 2005. URL: https://doi.org/10.5006/c2005-05462, doi:10.5006/c2005-05462. This article has 10 citations.

26. (canacoo2026laseradditivemanufacturing pages 32-34): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

27. (canacoo2026laseradditivemanufacturing pages 1-2): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

28. (canacoo2026laseradditivemanufacturing pages 34-35): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

29. (canacoo2026laseradditivemanufacturing pages 2-4): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

30. (tuck2005thedevelopmentof media 9e3cf1ab): Clive D S Tuck. The development of very high strength copper alloys with resistance to hydrogen embrittlement and stress corrosion cracking. CORROSION 2005, pages 1-15, Apr 2005. URL: https://doi.org/10.5006/c2005-05462, doi:10.5006/c2005-05462. This article has 10 citations.
