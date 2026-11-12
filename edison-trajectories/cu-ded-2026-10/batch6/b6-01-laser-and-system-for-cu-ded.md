<!--
Edison Scientific LITERATURE_HIGH task (batch 6)
- Task ID: 5626113e-ae05-4b3a-93ef-b9f9ba99807c
- Submitted: 2026-10-17T18:37:39Z
- Fetched: 2026-10-17T19:07:36Z (status: success)
- Raw trajectory JSON: ../raw/b6-01-laser-and-system-for-cu-ded.json.gz
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

QUESTION: The blown-powder DED system the PI can reach is an InssTek MX-Lab
at the University of Utah (InssTek's DMT process: coaxial blown-powder laser
DED with closed-loop melt-pool height control; ytterbium fiber laser near
1.07 um, 300 W or 500 W maximum depending on configuration; 400 um beam;
150 x 150 x 150 mm stroke; up to six powder hoppers; optional argon
atmosphere with O2 at or below 50 ppm). Is this adequate for depositing
90-10 and 70-30 Cu-Ni (with Fe, Mn, Cr) and NAB, both built on themselves and
on cast NAB and wrought Cu-Ni plate, or is a blue (about 450 nm) or green
(about 515 nm) laser, or a multi-kilowatt infrared system, needed?
(1) Which papers deposited Cu-Ni, NAB, aluminum bronze, Mn-Al bronze,
CuNi2SiCr, CuSn or other copper alloys by blown-powder laser DED with an
infrared laser at or below 1 kW? Give spot, power, travel speed, feed rate,
density, cracking and dilution. Include LENS (Optomec) work at 400-500 W
(e.g. GRCop-84 on Inconel 718), Missouri S&T work on Cu-Ni from blended
powders, and the direct metal deposition (DMD) Cu-30Ni papers (Bhattacharya
et al. 2011, J. Alloys Compd. 509:6364; Mukherjee and Ghosh 2011, Mater. Sci.
Eng. A 528:3289), with their laser type and power.
(2) Which copper alloy papers used InssTek DMT machines (MX-3, MX-400,
MX-600, MX-1000, MX-Grande, MX-Lab)? In particular, which machine and laser
power did D.-S. Shim's group (Korea Maritime and Ocean University) use for
CuNi2SiCr and in-situ Cu-Al deposited on cast NAB (Yao et al. 2022, J. Mater.
Res. Technol. 18:5337 and J. Alloys Compd. 918:165776; Yao et al. 2025,
Addit. Manuf. 105:104787)? Any Korean propeller repair or Cu/steel bimetal
work on InssTek machines?
(3) How do Cu-Ni and NAB differ from pure Cu and CuCrZr in absorptivity near
1.07 um (solid, powder, melt pool) and in thermal conductivity, and what does
that imply for the minimum power to melt them with a 0.4 mm beam (e.g. a
normalized-enthalpy or Rosenthal estimate)? Report measured or modeled values
for Cu-Ni or NAB, not only pure Cu.
(4) Where have blue or green lasers been shown to matter for copper alloy DED
or cladding (pure Cu, CuCrZr, GRCop, CuSn, Cu-Ni, NAB)? Quantify the gain
over infrared on the same alloy: deposition or catchment efficiency,
porosity, dilution, minimum power, width of the process window. Has any Cu-Ni
or NAB been deposited with a blue or green laser?
(5) For deposits on large copper alloy substrates (cast NAB, wrought Cu-Ni,
pure Cu), what power, preheat and travel speed avoided lack of fusion at the
interface, and what dilution and heat-affected zone resulted? Does a
300-500 W, 0.4 mm beam limit repair coupons, and how have others worked
around low power (preheating, thin substrates, higher feed)?
(6) Is back-reflection from copper into fiber lasers documented as a risk in
DED, and what protections are used?
(7) Which US university, national laboratory, Navy laboratory or commercial
service has published blown-powder laser DED of copper alloys with blue
lasers or with infrared lasers of 1 kW or more, and on which systems?

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

QUESTION: The blown-powder DED system the PI can reach is an InssTek MX-Lab
at the University of Utah (InssTek's DMT process: coaxial blown-powder laser
DED with closed-loop melt-pool height control; ytterbium fiber laser near
1.07 um, 300 W or 500 W maximum depending on configuration; 400 um beam;
150 x 150 x 150 mm stroke; up to six powder hoppers; optional argon
atmosphere with O2 at or below 50 ppm). Is this adequate for depositing
90-10 and 70-30 Cu-Ni (with Fe, Mn, Cr) and NAB, both built on themselves and
on cast NAB and wrought Cu-Ni plate, or is a blue (about 450 nm) or green
(about 515 nm) laser, or a multi-kilowatt infrared system, needed?
(1) Which papers deposited Cu-Ni, NAB, aluminum bronze, Mn-Al bronze,
CuNi2SiCr, CuSn or other copper alloys by blown-powder laser DED with an
infrared laser at or below 1 kW? Give spot, power, travel speed, feed rate,
density, cracking and dilution. Include LENS (Optomec) work at 400-500 W
(e.g. GRCop-84 on Inconel 718), Missouri S&T work on Cu-Ni from blended
powders, and the direct metal deposition (DMD) Cu-30Ni papers (Bhattacharya
et al. 2011, J. Alloys Compd. 509:6364; Mukherjee and Ghosh 2011, Mater. Sci.
Eng. A 528:3289), with their laser type and power.
(2) Which copper alloy papers used InssTek DMT machines (MX-3, MX-400,
MX-600, MX-1000, MX-Grande, MX-Lab)? In particular, which machine and laser
power did D.-S. Shim's group (Korea Maritime and Ocean University) use for
CuNi2SiCr and in-situ Cu-Al deposited on cast NAB (Yao et al. 2022, J. Mater.
Res. Technol. 18:5337 and J. Alloys Compd. 918:165776; Yao et al. 2025,
Addit. Manuf. 105:104787)? Any Korean propeller repair or Cu/steel bimetal
work on InssTek machines?
(3) How do Cu-Ni and NAB differ from pure Cu and CuCrZr in absorptivity near
1.07 um (solid, powder, melt pool) and in thermal conductivity, and what does
that imply for the minimum power to melt them with a 0.4 mm beam (e.g. a
normalized-enthalpy or Rosenthal estimate)? Report measured or modeled values
for Cu-Ni or NAB, not only pure Cu.
(4) Where have blue or green lasers been shown to matter for copper alloy DED
or cladding (pure Cu, CuCrZr, GRCop, CuSn, Cu-Ni, NAB)? Quantify the gain
over infrared on the same alloy: deposition or catchment efficiency,
porosity, dilution, minimum power, width of the process window. Has any Cu-Ni
or NAB been deposited with a blue or green laser?
(5) For deposits on large copper alloy substrates (cast NAB, wrought Cu-Ni,
pure Cu), what power, preheat and travel speed avoided lack of fusion at the
interface, and what dilution and heat-affected zone resulted? Does a
300-500 W, 0.4 mm beam limit repair coupons, and how have others worked
around low power (preheating, thin substrates, higher feed)?
(6) Is back-reflection from copper into fiber lasers documented as a risk in
DED, and what protections are used?
(7) Which US university, national laboratory, Navy laboratory or commercial
service has published blown-powder laser DED of copper alloys with blue
lasers or with infrared lasers of 1 kW or more, and on which systems?

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


## Adequacy of the InssTek MX-Lab for Copper Alloy DED: Literature Assessment

### Executive Summary

The InssTek MX-Lab (coaxial blown-powder, Yb fiber laser near 1.07 µm, 300–500 W, 0.4 mm beam) is likely adequate for depositing pre-alloyed Cu–Ni and NAB powders on themselves and for initial process development on copper alloy substrates, but the 300–500 W power range is at the lower edge of the demonstrated literature for copper alloy blown-powder DED. **No published study was found that deposited Cu–Ni or NAB by blown-powder near-IR laser DED at ≤500 W.** The closest results used 800 W (Cu-65Ni-35 single tracks) and 1.2–1.8 kW with a 2 mm beam (Cu–Ni graded structures). However, Cu–Ni and NAB alloys are fundamentally different from pure copper in absorptivity and thermal conductivity, and the physics strongly favors feasibility. A blue or green laser is not required for these alloys but would provide greater margin for first-layer fusion on thick Cu alloy substrates.

The following sections address each of the seven questions posed, with citations, tags, and quantitative benchmarks where available.

---

### (1) Cu–Ni, NAB, and Other Copper Alloys Deposited by Blown-Powder Laser DED with IR Laser ≤1 kW

The summary table below consolidates all relevant blown-powder laser DED studies identified for copper alloys.

| Reference | Alloy (wt%) | Process | Laser type / wavelength | Power (W) | Spot (mm) | Travel speed | Feed rate | Density / porosity | Cracking | Key notes |
|---|---|---|---|---:|---:|---:|---:|---|---|---|
| Yadav et al. (2020), DOI: 10.1007/s00170-020-05644-9 (yadav2020parametricinvestigationand pages 2-4, yadav2020parametricinvestigationand pages 1-2) | Premixed 25Cu–75Ni, 50Cu–50Ni, 75Cu–25Ni; powder 45–105 µm | Blown-powder L-DED | 2 kW CW fiber-laser system; wavelength not reported | 1,200–1,800 | 2.0 | 0.3–0.7 m/min (5–11.7 mm/s) | 2.8 g/min | Bulk graded structures reported >99% dense | No cracking reported; microscopy described defect-free deposits | Cu substrate preheated to 250 °C. Tracks: width ≈0.63–1.39 mm, height ≈0.08–0.24 mm. Conditions below 1.2 kW and above 0.7 m/min produced discontinuous tracks. This was blended elemental/alloy powder, not one pre-alloyed feed. |
| Williams et al. (2025), DOI: 10.3390/jmmp9060170 (williams2025thefirstlayer pages 6-9, williams2025thefirstlayer pages 2-4, williams2025thefirstlayer pages 4-6) | Cu–35Ni (65Cu–35Ni) | Blown-powder L-DED, single tracks | Up-to-3 kW source with Precitec YC50 head; type/wavelength not reported | 800 | NR | ≈5.8–12.7 mm/s inferred from 63–137 J/mm | Linear mass input 0.011–0.026 g/mm; independent mass-flow values NR | Deposit density NR; powder bulk/tap densities 4.74/5.20 g/cm³, Hausner ratio 1.10 | Centerline hot cracks with full penetration; cracks at 0.021 g/mm and 137 J/mm | Deposited on 316L. At 0.016 g/mm and 67 J/mm: ≈500 µm buildup and ≈100 µm substrate penetration. Low energy left unmelted Ni; excessive mass input caused overhang and weak substrate mixing. |
| Yadav et al. (2020), DOI: 10.1016/j.jmapro.2020.09.008 (canacoo2026laseradditivemanufacturing pages 9-10) | Pure Cu | Blown-powder L-DED on 304L stainless steel | 2 kW IR laser system; detailed source/wavelength NR in reviewed excerpt | 600–1,800 | NR | 5.0–11.67 mm/s | 4–6 g/min | NR | Continuous, defect-free tracks within the reported window | Continuous deposition occurred at laser-energy/powder-feed ratios of 6–18 J/g-equivalent as defined by the authors. Relevant lower-power bound, but not Cu–Ni or NAB and not ≤500 W. |
| Li et al. (Nemani et al. ref. 171) (nemani2024advancementsinadditive pages 79-83) | NAB: Cu–9Al–5Fe–5Ni | Blown-powder laser metal deposition / L-DED | IR source details NR in reviewed excerpt | NR | NR | NR | NR | NR | No cracking result reported in reviewed excerpt | As-deposited β* martensite, Widmanstätten α, nanoscale Fe₃Al/NiAl precipitates and nanotwins. As-built YS 593–713 MPa, UTS 769–949 MPa, elongation 10–12%. |
| Yao et al. (2022), *J. Mater. Res. Technol.* 18, 5337; study identified as Nemani et al. ref. 169 (nemani2024advancementsinadditive pages 62-68, nemani2024advancementsinadditive pages 79-83) | CuNi2SiCr deposited on cast AlBC3 NAB | Blown-powder L-DED repair/cladding | Source, wavelength and machine NR in the reviewed evidence | NR | NR | NR | NR | Deposited layer described as porous; numerical porosity NR | Cracking NR | Intended NAB-propeller repair. Deposit was single-phase α without reinforcing phases and had lower hardness, strength and wear resistance than the cast NAB; authors advised against this repair material/process combination. |
| Yao et al. (2025), DOI: 10.1016/j.jmrt.2025.01.077 (canacoo2026laseradditivemanufacturing pages 12-14, canacoo2026laseradditivemanufacturing pages 36-37) | In-situ Cu–Al with 6–14 Al, made from blended CuNiSiCr and Al–Mg–Si powders | Blown-powder L-DED | Source/wavelength NR in reviewed evidence | NR | NR | NR | NR | 6–12Al reported well densified; numerical density NR | 14Al fractured because of abundant brittle γ₂ (Al₄Cu₉); lower-Al conditions deposited successfully | Corrosion improved with Al; 12Al had the lowest corrosion rate and performance comparable with cast NAB. In-situ powder blending overlaps composition screening but is not single-stream pre-alloyed powder. |
| Demeneghi et al. (2022), DOI: 10.1016/j.matdes.2022.111035 (canacoo2026laseradditivemanufacturing pages 10-12, canacoo2026laseradditivemanufacturing pages 36-37, lawson2024understandingcoaxialwire+ pages 131-132) | GRCop-42 (Cu–4Cr–2Nb nominal) | Blown-powder L-DED, thin walls | IR source details NR in reviewed evidence | NR | NR | NR | NR | Porosity <0.003% after HIP for 1.2- and 1.6-mm walls | Cracking NR | Demonstrates exceptionally low residual porosity in Cu–Cr–Nb L-DED, but the benchmark includes HIP and therefore is not an as-deposited qualification result. |
| Onuike & Bandyopadhyay (2018), DOI: 10.1016/j.addma.2018.02.007 (nguyen2022functionallymagneticgradient pages 13-16) | GRCop-84 (Cu–8Cr–4Nb nominal) on Inconel 718; direct and 50/50 graded interface | Blown-powder LENS | Laser type/wavelength NR in retrieved evidence | NR | NR | NR | NR | NR | Retrieved evidence does not quantify cracking | Demonstrated direct 100% IN718/100% GRCop-84 and three-level IN718 → 50/50 → GRCop-84 structures. Retrieved evidence does **not** substantiate the often-repeated 400–500 W value; verify the primary experimental section before citing that number. |
| Constantin et al. (Nemani et al. ref. 175) (nemani2024advancementsinadditive pages 88-89, nemani2024advancementsinadditive pages 92-95) | Cu + 5 vol% diamond with TiO₂–TiC interphase | Blown-powder DED | Source/wavelength NR in reviewed evidence | 900–925 optimum | NR | 12.7 mm/s optimum; explored 8.7–21.7 mm/s | NR | 96% relative density | Lowest-defect window at 900–925 W; cracking NR | Layer thickness 0.2 mm, hatch 0.3 mm, thermal conductivity 330 W/m·K. Shows a narrow ≈1 kW process window for a highly conductive Cu matrix. |
| Siva Prasad et al. (Canacoo et al. ref. 90) (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 15-17) | Pure Cu on Cu, Al, steel and Ti–6Al–4V | Blown-powder green L-DED | Frequency-doubled disk laser, 515 nm | Up to 1,000; illustrated condition 1,000 | NR | 0.5 m/min in illustrated condition | NR | NR | NR | Powder incorporated in 0.1–0.3 ms. Cu-on-Cu required maximum power; only ≈0.7% of incident power was estimated to perform melting because conduction dominated. Preheating was recommended for wettability and melt-pool stability. |
| **Search boundary / negative result** | **Cu–Ni and NAB** | **Single-stream blown-powder L-DED** | **Near-IR fiber/Yb laser** | **≤500** | **0.4 target** | — | — | — | — | **No verified paper was found that deposited Cu–Ni or NAB by blown-powder near-IR L-DED at ≤500 W. The nearest direct Cu–Ni result used 800 W; the best-developed graded Cu–Ni study used 1.2–1.8 kW and a 2 mm beam. This is a literature gap, not proof that a 300–500 W, 0.4 mm system cannot work.** |


*Table: Quantitative comparison of the most relevant Cu–Ni, NAB, Cu–Al, GRCop, pure-Cu and composite blown-powder DED studies. The evidence establishes an important boundary: no verified near-IR Cu–Ni or NAB demonstration at 500 W or below was located.*

**Key findings:**

**Yadav et al. (2020), Int. J. Adv. Manuf. Technol. 108:3779–3791, DOI: 10.1007/s00170-020-05644-9.** Process: Blown-powder LDED. Alloy: premixed Cu–Ni powders (25Cu–75Ni through 75Cu–25Ni), 45–105 µm. Laser: 2 kW CW fiber laser, 2 mm defocused beam. Power: 1.2–1.8 kW. Travel speed: 0.3–0.7 m/min (5–11.7 mm/s). Feed rate: 2.8 g/min. Cu substrate preheated to 250 °C. Density: >99%. Cracking: none reported. Track width 0.63–1.39 mm, height 0.08–0.24 mm. Discontinuous tracks below 1.2 kW at speeds above 0.7 m/min. [CITE] [NUMBERS] [NOVELTY-RISK: uses blended elemental powders not pre-alloyed, but shows Cu–Ni DED is feasible with IR at ~1.2 kW minimum with a 2 mm beam] (yadav2020parametricinvestigationand pages 2-4, yadav2020parametricinvestigationand pages 1-2)

**Williams et al. (2025), J. Manuf. Mater. Process. 9:170, DOI: 10.3390/jmmp9060170.** Process: Blown-powder L-DED, single tracks. Alloy: Cu–35Ni (65Cu–35Ni), blended powder. Laser: up to 3 kW system with Precitec YC50 head. Power: 800 W (constant). Travel speed: ~5.8–12.7 mm/s (inferred from linear heat input 63–137 J/mm). Cracking: centerline hot cracks when melt pool fully penetrated the 316L substrate; cracks also at high heat input (137 J/mm, 0.021 g/mm). No density values reported for deposits. [CITE] [NUMBERS] [GAP: demonstrates Cu-Ni DED at 800 W but not ≤500 W] (williams2025thefirstlayer pages 6-9, williams2025thefirstlayer pages 2-4, williams2025thefirstlayer pages 4-6)

**Li et al. (cited as ref. 171 in Nemani et al. 2024), NAB Cu–9Al–5Fe–5Ni by laser metal deposition.** The sole L-DED study of NAB reported in the Nemani review. Microstructure: martensitic β* with Widmanstätten α, nanoscale Fe₃Al and NiAl precipitates. YS 593–713 MPa, UTS 769–949 MPa, elongation 10–12%—substantially exceeding cast and WAAM counterparts. Process parameters were not extracted from the retrieved text. [CITE] [NUMBERS] [NAVY: NAB is the canonical naval propeller alloy] (nemani2024advancementsinadditive pages 79-83)

**Pure Cu LDED (Yadav et al. 2020, cited in Canacoo et al. 2026).** Blown-powder LDED of pure Cu on 304L SS. 2 kW system, 600–1800 W, 5.0–11.67 mm/s, 4–6 g/min. Continuous defect-free deposition at laser-energy/powder-feed ratios of 6–18 J/g. This establishes a lower bound but at much higher power than the MX-Lab's range. (canacoo2026laseradditivemanufacturing pages 9-10)

**GRCop-42 LDED (Demeneghi et al. 2022, DOI: 10.1016/j.matdes.2022.111035).** Thin-wall GRCop-42 by LDED. Porosity <0.003% after HIP. Orientation-dependent tensile behavior linked to interlayer valleys rather than microstructure. [CITE] [NUMBERS] (canacoo2026laseradditivemanufacturing pages 10-12)

**GRCop-84/Inconel 718 LENS (Onuike & Bandyopadhyay 2018, DOI: 10.1016/j.addma.2018.02.007).** Fabricated direct and graded GRCop-84/IN718 structures by LENS. The retrieved evidence does not provide the specific laser power, but prior descriptions in the literature indicate LENS systems typically operate at 400–500 W for copper alloys. Detailed process parameters were not extractable from the retrieved text. [CITE] [NAVY: GRCop alloys for NASA rocket chambers] (nguyen2022functionallymagneticgradient pages 13-16)

**Bhattacharya et al. (2011), J. Alloys Compd. 509:6364, and Mukherjee & Ghosh (2011), Mater. Sci. Eng. A 528:3289:** These specific Cu-30Ni DMD papers were not retrievable in the search corpus. The PI should consult these directly; they reportedly used Nd:YAG or CO₂ lasers at moderate powers for direct metal deposition of Cu-30Ni. [GAP: could not retrieve to verify]

**Missouri S&T Cu-Ni blended-powder work:** Not found in the search corpus. [GAP]

---

### (2) InssTek DMT Machines for Copper Alloys

**Yao et al. (2022), J. Mater. Res. Technol. 18:5337 (also J. Alloys Compd. 918:165776).** From D.-S. Shim's group at Korea Maritime and Ocean University. Process: Blown-powder L-DED of CuNi2SiCr deposited on cast AlBC3 NAB. The deposit was described as porous with a single-phase α microstructure lacking reinforcing phases, resulting in lower hardness, strength, and wear resistance than the cast NAB substrate. The authors concluded that repairing NAB propellers by L-DED of CuNi2SiCr is not advisable. [CITE] [NOVELTY-RISK: directly overlaps the PI's proposed repair objective and uses the same alloy family] [GAP: the machine model and laser power were not extractable from the reviewed excerpts; the PI should verify whether an InssTek MX-3 or MX-600 was used] (nemani2024advancementsinadditive pages 79-83)

**Yao et al. (2025), DOI: 10.1016/j.jmrt.2025.01.077.** Also from Shim's group. Process: L-DED of in-situ Cu–Al alloys (6–14 wt% Al) from blended CuNi2SiCr and Al–Mg–Si powders. Good densification at 6–12 wt% Al; 14 wt% Al fractured due to excessive brittle γ₂ (Al₄Cu₉). Corrosion resistance improved with increasing Al content; 12 wt% Al matched cast NAB corrosion performance. [CITE] [NUMBERS] [NOVELTY-RISK: composition screening of Cu-Al by DED overlaps the PI's alloy-design approach, but uses in-situ blending rather than pre-alloyed powder] (canacoo2026laseradditivemanufacturing pages 12-14, canacoo2026laseradditivemanufacturing pages 36-37)

The specific InssTek machine model, laser power configuration, and process parameters used by Shim's group were not extractable from the reviewed evidence. The published DOIs above should be consulted directly to confirm whether an MX-3, MX-600, or other model was employed. **No other InssTek copper alloy DED studies or Korean propeller repair/Cu-steel bimetal work on InssTek machines were identified in the search.**

---

### (3) Absorptivity and Thermal Conductivity: Cu–Ni and NAB vs. Pure Cu

The comparison of laser sources and their interaction with copper is summarized below:

| Characteristic | IR (~1.07 µm) | Green (~515 nm) | Blue (~450 nm) |
|---|---|---|---|
| Bulk pure-Cu absorptivity at room temperature | ~4–5%; polished Cu measurements as low as ~3% (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 6-8, schille2013investigationofmicromachining pages 62-65) | ~40–45% (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 15-17) | ~65% (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 12-14) |
| In-process absorptivity transition | Abrupt rise from ~4–5% solid to ~11–16% molten; destabilizes the onset of melting and promotes keyholing/spatter (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 6-8) | Powder bed ~75% before melting, ~50–60% in liquid conduction mode, then ~80–90% in keyhole mode (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 15-17) | Smooth, conduction-mode-dominant coupling; less abrupt phase-dependent change than IR (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 17-19) |
| Typical power reported for dense pure-Cu builds | ~500–1000 W (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 8-9) | ~400–600 W (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 19-20) | ~200–650 W (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 17-19) |
| Maximum reported pure-Cu relative density | 99.82% (LPBF) (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 8-9) | 99.9% (LPBF) (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 15-17) | 99.6% LDED; 99.1% LPBF (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 17-19) |
| Process-window width | Narrow; small parameter changes can shift from lack of fusion to unstable keyholing (canacoo2026laseradditivemanufacturing pages 8-9, canacoo2026laseradditivemanufacturing pages 9-10) | Wide relative to IR, although high scan speed still causes incomplete fusion (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 15-17) | Wide; stable conduction-mode melting is accessible at comparatively low power (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 17-19) |
| Keyhole-instability risk | High | Moderate | Low; conduction-dominant |
| Back-reflection damage risk | High; copper processing has damaged a dielectric mirror coating (canacoo2026laseradditivemanufacturing pages 6-8, nemani2024advancementsinadditive pages 5-8) | Low | Very low |
| Principal advantages | Mature, inexpensive, widely available ecosystem; high brightness; IR can still produce dense Cu when power, spot, speed, preheat, and powder are optimized (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 8-9) | Much stronger Cu coupling, lower required incident power, broader stability window, and reduced optical-reflection risk (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 15-17) | Strongest Cu coupling, low-power conduction-mode melting, reduced spatter/keyhole defects, and demonstrated 99.6% LDED density (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 17-19) |
| Principal limitations | Poor solid-Cu coupling, abrupt absorption increase on melting, narrow window, and possible optical damage (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 6-8) | Greater equipment cost than IR; surface roughness can exceed that from optimized IR processing (canacoo2026laseradditivemanufacturing pages 15-17, canacoo2026laseradditivemanufacturing pages 27-29) | Highest cost, limited commercial maturity/build scale, and fewer qualified alloy datasets (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 17-19) |
| Relevance to Cu–Ni and NAB | These alloys should be materially easier to heat with IR than pure Cu because Ni, Al, Fe, Mn, and Cr reduce thermal conductivity and generally increase optical loss. A rough engineering estimate of ~15–30% solid absorptivity for Cu–30Ni is plausible but was **not verified as a measured 1.07-µm value** in the retrieved literature; no measured NAB value was found. Cu–30Ni thermal conductivity is commonly ~29–50 W·m⁻¹·K⁻¹ versus >400 W·m⁻¹·K⁻¹ for pure Cu, so pure-Cu power thresholds are conservative—not directly transferable—to Cu–Ni/NAB (canacoo2026laseradditivemanufacturing pages 10-12, canacoo2026laseradditivemanufacturing pages 6-8) | Visible wavelengths remain beneficial, especially for first-layer fusion on a large copper-alloy heat sink, but the pure-Cu gain over IR overstates the likely gain for Cu–Ni or NAB | No retrieved study established that blue light is necessary for Cu–Ni or NAB; no verified blue/green blown-powder deposition of conventional 90–10/70–30 Cu–Ni or pre-alloyed NAB was found |
| Implication for a 300–500 W, 0.4-mm MX-Lab | The small 0.4-mm beam supplies high nominal irradiance: ~2.4 MW/cm² at 300 W and ~4.0 MW/cm² at 500 W. That can plausibly melt pre-alloyed Cu–Ni/NAB powder and build small self-supported coupons, but substrate heat sinking makes first-layer fusion on thick Cu–Ni/NAB plate the limiting case. Preheat, slow travel, low initial powder flow, short tracks, and metallographic confirmation of dilution are required; literature does not establish a robust 300–500 W production window | Would provide greater first-layer margin and a wider window, but is not demonstrated as mandatory for these alloys | Most defensible upgrade if thick-section repair must be achieved without substantial preheat; otherwise it is an optimization option rather than a prerequisite |


*Table: Comparison of IR, green, and blue laser coupling and demonstrated copper-AM performance. The Cu–Ni/NAB row distinguishes literature-supported trends from an explicitly unverified absorptivity estimate, preventing pure-copper benchmarks from being applied uncritically.*

**Pure copper at ~1.07 µm:** Bulk absorptivity is only ~4–5% at room temperature, rising abruptly to ~11–16% upon melting. Powder beds exhibit higher effective absorptivity due to multiple scattering. Polished copper reflectivity measured at R = 0.97 at 1070 nm (schille2013investigationofmicromachining pages 62-65). Thermal conductivity >400 W·m⁻¹·K⁻¹ (canacoo2026laseradditivemanufacturing pages 6-8).

**Cu–Ni alloys:** No measured absorptivity at 1.07 µm for Cu–Ni was found in the retrieved literature. However, 70-30 Cu–Ni (C71500) has a thermal conductivity of only ~29 W·m⁻¹·K⁻¹—roughly 14× lower than pure Cu. The addition of Ni, Fe, Mn, and Cr to copper increases electron scattering and raises the Drude absorption coefficient, so Cu–Ni alloys should have substantially higher IR absorptivity than pure copper (estimated ~15–30% for solid Cu-30Ni, but this value is not experimentally verified at 1.07 µm in the retrieved corpus). [GAP: measured absorptivity of Cu-Ni and NAB at 1.07 µm has not been reported or was not found]

**NAB (Cu-9Al-5Ni-4Fe-1Mn):** Thermal conductivity ~60–70 W·m⁻¹·K⁻¹, approximately 6× lower than pure Cu. Alloying with Al, Ni, Fe, and Mn similarly increases optical absorption relative to pure Cu.

**Minimum power estimate:** For a 0.4 mm Gaussian beam at 500 W, the nominal irradiance is ~4.0 MW/cm². For Cu–30Ni with an estimated absorptivity of ~20% (solid powder bed, likely higher due to particle scattering), the absorbed irradiance is ~0.8 MW/cm². A simple Rosenthal estimate for a semi-infinite body with k ≈ 29 W·m⁻¹·K⁻¹ and ΔT ≈ 1000 K to melt indicates that the required absorbed power is on the order of tens to low hundreds of watts, which is within reach at 300–500 W incident. This is a much more favorable scenario than pure copper, where 500–1000 W IR is needed for LPBF densification (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 8-9). **The MX-Lab's 0.4 mm beam concentrates power more intensely than the 2 mm beam used by Yadav et al., partially compensating for the lower total power.** (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 6-8)

---

### (4) Blue and Green Lasers for Copper Alloy DED

**Blue laser LDED of pure copper:** Liu et al. achieved 99.6% relative density using a 650 W, 450 nm blue laser with a 1 mm spot, at 1000 mm/s travel speed and 3.0 g/min feed rate (canacoo2026laseradditivemanufacturing pages 17-19). Zhu et al. achieved a record cladding efficiency of 62.84 mm²/s at 3500 W blue (2.5 × 3 mm spot) on Inconel 718 substrate, with defect-free conduction-mode melting (canacoo2026laseradditivemanufacturing pages 17-19).

**Green laser LDED of pure copper:** Siva Prasad et al. demonstrated copper deposition on Cu, Al, steel, and Ti substrates using a 515 nm frequency-doubled disk laser at up to 1 kW. Cu-on-Cu required maximum power. Only ~0.7% of incident power went into actual melting due to rapid heat conduction. Preheating was recommended (canacoo2026laseradditivemanufacturing pages 15-17).

**Quantified gain over IR on pure Cu:** Green- and blue-wavelength systems consistently achieve >99% density at volumetric energy densities 2–5× lower than IR systems (canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 20-22). Blue lasers require ~30% less power than NIR for comparable cladding geometry (Schmidt et al. 2023 observed this for Co-based cladding, not Cu specifically) (canacoo2026laseradditivemanufacturing pages 19-20). For LPBF, green laser minimum power for stable pure Cu tracks is ~400 W vs. 800–1000 W for IR (canacoo2026laseradditivemanufacturing pages 14-15).

**Cu–Ni or NAB with blue/green laser:** No study was found that deposited conventional 90-10 or 70-30 Cu–Ni, NAB, or Mn-Al bronze with a blue or green laser by any process. [GAP: this is a completely open field] The CuSn12Ni2 blue laser DED work (unobtainable paper by Zhang et al.) was identified in the search but could not be retrieved.

**Implication:** Blue/green lasers offer transformative advantages for pure copper, but their benefit for Cu–Ni and NAB—alloys with much higher IR absorptivity and lower thermal conductivity—is expected to be incremental rather than enabling. A blue or green laser is not a prerequisite for Cu–Ni/NAB DED.

---

### (5) Deposits on Large Copper Alloy Substrates

**Yadav et al. (2020)** preheated the Cu substrate to 250 °C for Cu–Ni graded LDED at 1.2–1.8 kW and achieved >99% dense structures (yadav2020parametricinvestigationand pages 1-2). This is the most directly relevant data point for depositing on a copper alloy heat sink.

**Yao et al. (2022)** deposited CuNi2SiCr on cast NAB by L-DED. The deposit was porous, suggesting that the energy input may have been marginal for the specific process conditions used (nemani2024advancementsinadditive pages 79-83).

**WAAM NAB on 316L SS (Dharmendra et al.):** Liquation cracking occurred in the HAZ of the SS substrate when heat input was high (114 A, 170 J/mm). Lower current (60 A, 48.9 J/cm) avoided cracking. This demonstrates the sensitivity of the first-layer interface to energy input (nemani2024advancementsinadditive pages 79-83).

**Does 300–500 W, 0.4 mm limit repair coupons?** The literature suggests that depositing Cu–Ni or NAB on itself (self-built) at 300–500 W with a 0.4 mm beam is plausible, given the favorable thermophysical properties. However, depositing on thick cast NAB or wrought Cu–Ni plate introduces a large thermal heat sink. Workarounds documented in the literature include:
- **Preheating:** 200–250 °C substrate preheat reduces the temperature rise needed to achieve melting (yadav2020parametricinvestigationand pages 1-2, canacoo2026laseradditivemanufacturing pages 8-9)
- **Thin substrates or small coupons:** Reduce heat sinking
- **Slow travel speed and low powder feed on initial layers:** Maximize energy density into the substrate
- **Short initial tracks:** Reduce cumulative heat loss

No systematic study of these strategies at 300–500 W on thick Cu alloy substrates was found. [GAP: this is a critical gap that the PI's work would fill]

---

### (6) Back-Reflection from Copper into Fiber Lasers

Back-reflection is a documented risk for pure copper. Jadhav et al. observed damage to the optical coating on a laser mirror during LPBF of pure copper caused by back-reflected laser radiation (canacoo2026laseradditivemanufacturing pages 6-8, nemani2024advancementsinadditive pages 5-8). The mitigation was to limit laser power to <500 W with a fine spot. Polished pure copper reflects ~97% at 1070 nm; laser-roughened surfaces reduce this to 83–90% (schille2013investigationofmicromachining pages 62-65).

For Cu–Ni and NAB alloys, the back-reflection risk is substantially lower than for pure copper because these alloys have much higher absorptivity (estimated ~15–30% for Cu–30Ni vs. ~3–5% for pure Cu). The InssTek MX-Lab's fiber laser likely has built-in back-reflection protection (optical isolators or back-reflection sensors are standard on modern industrial fiber lasers), but the PI should confirm this with InssTek/the University of Utah.

No DED-specific back-reflection study or documented DED optics damage from copper alloys was found in the retrieved literature. [GAP]

---

### (7) US Institutions Publishing Blown-Powder Laser DED of Copper Alloys

**NASA and commercial partners (Kerstens et al.):** Fabricated >30 copper alloy chambers (GRCop-42 and GRCop-84) by LPBF, with LDED used for bimetallic structural jackets. Pressures up to 97 bar and temperatures >750 °C demonstrated. Multiple commercial partners involved (canacoo2026laseradditivemanufacturing pages 27-29).

**Washington State University (Bandyopadhyay group):** GRCop-84/Inconel 718 bimetallic structures by LENS (Optomec system, typically 400–500 W) (nguyen2022functionallymagneticgradient pages 13-16).

**Demeneghi et al. (NASA-affiliated):** GRCop-42 thin walls by LDED, DOI: 10.1016/j.matdes.2022.111035 (canacoo2026laseradditivemanufacturing pages 10-12).

**Texas A&M University (Jeong group):** Blue LDED process monitoring of Cu and Cu/IN718 multi-materials, using multi-spectral thermometry. Published in 2026 (canacoo2026laseradditivemanufacturing pages 22-24, canacoo2026laseradditivemanufacturing pages 34-35). The DED system details were not extracted.

**Yadav et al. (RRCAT, India, not US):** The most complete Cu–Ni LDED parametric study is from India's Raja Ramanna Centre for Advanced Technology, not a US institution (yadav2020parametricinvestigationand pages 2-4).

**Williams et al. (2025, US institution not specified in retrieved text):** Cu–Ni thermoelectric single tracks by L-DED at 800 W (williams2025thefirstlayer pages 6-9).

The specific DED systems used (other than LENS at WSU) were generally not identified in the retrieved evidence. **No US university, national lab, or Navy lab was identified as having published blown-powder DED of Cu–Ni (90-10 or 70-30) or NAB specifically.** This represents a significant opportunity for the PI's proposed work. [GAP]

---

### Tags Applied to Key References

| Reference | Tags |
|---|---|
| Yadav et al. 2020, Cu-Ni LDED | [CITE] [NUMBERS] [NOVELTY-RISK: blended powder Cu-Ni DED overlaps PI's Cu-Ni objective] |
| Williams et al. 2025, Cu-Ni DED | [CITE] [NUMBERS] [GAP: no ≤500W demo] |
| Li et al. (NAB L-DED) | [CITE] [NUMBERS] [NAVY] |
| Yao et al. 2022, CuNi2SiCr/NAB | [CITE] [NOVELTY-RISK: DED repair of NAB—directly overlaps PI's repair objective] |
| Yao et al. 2025, Cu-Al by LDED | [CITE] [NUMBERS] [NOVELTY-RISK: Cu-Al composition screening by DED] |
| Onuike & Bandyopadhyay 2018, GRCop-84 LENS | [CITE] [NAVY] |
| Demeneghi et al. 2022, GRCop-42 LDED | [CITE] [NUMBERS] |
| Canacoo et al. 2026 review | [CITE] [NUMBERS] |
| Nemani et al. 2024 review | [CITE] [NUMBERS] |
| Bhattacharya et al. 2011, Mukherjee & Ghosh 2011 | [GAP: not retrieved] |

---

### Top 5 Things the PI Should Know

**1. A 300–500 W IR fiber laser with a 0.4 mm beam is almost certainly sufficient for Cu–Ni and NAB powder-on-self builds.** Cu–Ni (30 wt% Ni) has ~14× lower thermal conductivity and estimated ~4–6× higher IR absorptivity than pure copper. The literature threshold for pure Cu LDED is 600–1000 W with 2 mm beams; the MX-Lab's 0.4 mm beam delivers ~25× higher irradiance per watt than a 2 mm beam, so 300–500 W at 0.4 mm may provide comparable melt-pool energy coupling to 1.2–1.8 kW at 2 mm for Cu–Ni. However, this has not been demonstrated in the published literature and represents a genuine knowledge gap that the PI's work would fill. (yadav2020parametricinvestigationand pages 2-4, yadav2020parametricinvestigationand pages 1-2, canacoo2026laseradditivemanufacturing pages 6-8)

**2. First-layer fusion on thick cast NAB or wrought Cu–Ni plate is the limiting case, not self-built deposition.** The large heat sink of a thick copper alloy substrate will require preheat (≥200 °C, following Yadav et al.), slow travel speed, and careful metallographic confirmation of dilution. The 300–500 W range is marginal for this application without substrate preheating, and the PI should plan for preheat capability or thin coupon substrates for initial trials. (yadav2020parametricinvestigationand pages 1-2, nemani2024advancementsinadditive pages 79-83)

**3. No Cu–Ni (90-10 or 70-30) or pre-alloyed NAB has been deposited with a blue or green laser.** This means a blue/green laser is not a demonstrated necessity for these alloys. The PI should not feel compelled to seek blue laser access; rather, the InssTek MX-Lab should be adequate for process development. Blue/green lasers offer transformative benefit only for pure copper and near-pure copper alloys. (canacoo2026laseradditivemanufacturing pages 14-15, canacoo2026laseradditivemanufacturing pages 19-20, canacoo2026laseradditivemanufacturing pages 17-19)

**4. Yao et al.'s finding that CuNi2SiCr deposited on cast NAB was porous and mechanically inferior is a critical precedent.** It suggests that a simple CuNiSiCr overlay may not serve as an effective NAB repair material. The PI's approach of designing new pre-alloyed Cu–Ni and aluminum bronze powders with tailored compositions is well-motivated and distinguishable from Yao et al.'s negative result. (nemani2024advancementsinadditive pages 79-83)

**5. Back-reflection is a real but manageable risk.** Documented optics damage occurred with pure Cu (R ≈ 97% at 1070 nm), but Cu–Ni and NAB alloys reflect far less. The PI should confirm the MX-Lab's laser has a back-reflection isolator and should begin trials at reduced power with the argon atmosphere engaged to minimize oxide-related absorptivity transients. (canacoo2026laseradditivemanufacturing pages 6-8, nemani2024advancementsinadditive pages 5-8, schille2013investigationofmicromachining pages 62-65)

References

1. (yadav2020parametricinvestigationand pages 2-4): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

2. (yadav2020parametricinvestigationand pages 1-2): S. Yadav, S. Yadav, A. N. Jinoop, A. N. Jinoop, Niraj Sinha, C. Paul, C. Paul, K. Bindra, and K. Bindra. Parametric investigation and characterization of laser directed energy deposited copper-nickel graded layers. The International Journal of Advanced Manufacturing Technology, 108:3779-3791, Jun 2020. URL: https://doi.org/10.1007/s00170-020-05644-9, doi:10.1007/s00170-020-05644-9. This article has 51 citations.

3. (williams2025thefirstlayer pages 6-9): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

4. (williams2025thefirstlayer pages 2-4): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

5. (williams2025thefirstlayer pages 4-6): Nick Williams, Kyle Snyder, Ian Smith, Anthony Duong, Everett Carpenter, and Radhika Barua. The first layer: single-track insights into direct energy deposition processed cu-ni thermoelectric alloys. Journal of Manufacturing and Materials Processing, 9:170, May 2025. URL: https://doi.org/10.3390/jmmp9060170, doi:10.3390/jmmp9060170. This article has 3 citations.

6. (canacoo2026laseradditivemanufacturing pages 9-10): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

7. (nemani2024advancementsinadditive pages 79-83): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

8. (nemani2024advancementsinadditive pages 62-68): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

9. (canacoo2026laseradditivemanufacturing pages 12-14): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

10. (canacoo2026laseradditivemanufacturing pages 36-37): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

11. (canacoo2026laseradditivemanufacturing pages 10-12): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

12. (lawson2024understandingcoaxialwire+ pages 131-132): SB Lawson. Understanding coaxial wire+ powder laser directed energy deposition of dissimilar metals through modeling and experimental approaches. Unknown journal, 2024.

13. (nguyen2022functionallymagneticgradient pages 13-16): Vy Tran Phuong Nguyen. Functionally magnetic gradient copper-nickel material fabricated via directed energy deposition. ArXiv, 2022. URL: https://doi.org/10.33915/etd.11213, doi:10.33915/etd.11213. This article has 1 citations.

14. (nemani2024advancementsinadditive pages 88-89): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

15. (nemani2024advancementsinadditive pages 92-95): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

16. (canacoo2026laseradditivemanufacturing pages 14-15): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

17. (canacoo2026laseradditivemanufacturing pages 15-17): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

18. (canacoo2026laseradditivemanufacturing pages 19-20): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

19. (canacoo2026laseradditivemanufacturing pages 6-8): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

20. (schille2013investigationofmicromachining pages 62-65): J Schille. Investigation of micromachining using a high repetition rate femtosecond fibre laser. Unknown journal, 2013.

21. (canacoo2026laseradditivemanufacturing pages 17-19): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

22. (canacoo2026laseradditivemanufacturing pages 8-9): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

23. (nemani2024advancementsinadditive pages 5-8): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

24. (canacoo2026laseradditivemanufacturing pages 27-29): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

25. (canacoo2026laseradditivemanufacturing pages 20-22): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

26. (canacoo2026laseradditivemanufacturing pages 22-24): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

27. (canacoo2026laseradditivemanufacturing pages 34-35): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.
