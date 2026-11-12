<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: c89c6f74-0bbb-4eb0-a8ae-6fd86812e968
- Submitted: 2026-10-17T18:59:52Z
- Fetched: 2026-10-17T19:30:46Z (status: success)
- Raw trajectory JSON: ../raw/el-21-Sb.json.gz
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

ELEMENT UNDER REVIEW: Sb (dealloying inhibitor). Inhibited admiralty brass C44400 (0.02-0.10 Sb); impurity limit in Cu-Ni and bronzes; hot shortness.

Answer for Sb specifically, not for copper alloys in general:
1. ROLE: what Sb does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Sb ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Sb changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Sb, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Sb, Cu-Ni-Sb and Cu-Al-Sb are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Sb in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Sb neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Sb | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Sb (dealloying inhibitor). Inhibited admiralty brass C44400 (0.02-0.10 Sb); impurity limit in Cu-Ni and bronzes; hot shortness.

Answer for Sb specifically, not for copper alloys in general:
1. ROLE: what Sb does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Sb ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Sb changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Sb, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Sb, Cu-Ni-Sb and Cu-Al-Sb are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Sb in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Sb neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Sb | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Sb in pre-alloyed copper powder for marine laser DED

**Decision: LIMIT Sb as an impurity in both Cu–Ni and aluminum-bronze candidates.** Sb is an established *dezincification* inhibitor in predominantly α-phase brass, but that is not evidence that it improves an as-deposited Cu–Ni or nickel-aluminum bronze (NAB) seawater film. The available copper-alloy metallurgy instead identifies Sb as a grain-boundary embrittler and an undesirable welding impurity. For this program, specify **Sb ≤0.02 wt% (200 ppm) in both powder and deposit as a provisional internal screening limit**, not as a demonstrated safe threshold or an ASTM/AWS/MIL requirement; seek lower values where practical. Do not trade a documented cracking risk for an unmeasured corrosion benefit. [CITE] [GAP] (konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155, davies1993anoteon pages 3-4)

The evidence that drives this distinction is summarized below. **All alloy compositions and proposed bounds are in wt%; the phase-diagram source also reports solubility in at%.**

| Sb evidence context | Quantitative finding | Mechanism / failure mode | Relevance to DED alloy bounds |
|---|---|---|---|
| α 70Cu–30Zn brass; Lombardi tests summarized by D. D. Davies, *A Note on the Dezincification of Brass* (1993) | [NUMBERS] Sb = 0, 0.10, and 0.20 wt% in 5 wt% CuCl₂; Sb gave the best inhibition among Sb/As/P, with little or no added benefit above 0.10 wt% (davies1993anoteon pages 3-4) | An Sb-bearing corrosion film is proposed to suppress preferential Zn dissolution; inhibition is ineffective in β-rich brass. Grain-boundary precipitation can instead promote intercrystalline corrosion or corrosion fatigue (davies1993anoteon pages 3-4, davies1993anoteon pages 1-3) | Establishes a brass-only functional level near 0.10 wt%, not Cu–Ni or Al-bronze performance. [GAP] No Sb-controlled natural seawater, ASTM D1141, or 3.5 wt% NaCl electrochemical dataset was found. |
| Binary α-Cu–Sb; Fürtauer–Flandorfer phase diagram and Gierlotka–Jendrzejczyk-Handzlik assessment | [NUMBERS] Maximum α-Cu solubility = 7.8 at% Sb at 645 °C ≈ 13.94 wt% Sb; 6.5 at% at 484 °C and 5.7 at% at 440 °C. Reported phases include Cu₃Sb, Cu₄Sb, Cu₇₈Sb₂₀, Cu₁₀Sb₃, and Cu₂Sb; dilute Sb lowers rather than raises the Cu liquidus (modlinger2023structuresandphase pages 10-16, modlinger2023structuresandphase pages 50-53, modlinger2023structuresandphase media 63c0f99d) | High equilibrium solubility does not prevent nonequilibrium grain-boundary segregation or antimonide formation; the solubility boundary is therefore not a safe DED design bound. | Liquidus is not limiting at trace Sb and will not push Cu alloys above 1,250 °C. [GAP] No validated Cu–Ni–Sb or Cu–Al–Sb DED solidification model was found. |
| Cast tin bronze; W. D. Riley and H. V. Makar, “Impurity Effects in Secondary Copper Alloys,” *Conservation & Recycling* 9 (1986), 315–323, DOI: 10.1016/0361-3658(86)90066-4 | [NUMBERS] Sb = 0.18 wt% severely reduced tin-bronze ductility (riley1986impurityeffectsin pages 3-4) | Sb lowers Sn solubility and increases brittle Sn-rich δ phase; the failure mode is brittle interdendritic or grain-boundary material rather than useful dealloying inhibition. | Strong evidence against approaching 0.18 wt% in Sn-bearing compositions; Sn–Sb should be treated as a joint constraint. |
| Cu–Ni and aluminum/Ni–Al bronze; DOE/CDA impurity and weldability assessment | Sb is classified as detrimental in both families; it segregates to grain boundaries and impairs weldability and brazability, but no numerical threshold was reported (konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155) | Expected risks are hot shortness, solidification or reheated-layer liquation cracking, and reduced elevated-temperature ductility. [GAP] No Sb-controlled laser DED, laser cladding, atomization, dilution, porosity, evaporation, or seawater outcome was found. | Provisional engineering cap: 0.02 wt% Sb (200 ppm) in powder and deposit. This is an internal risk-control recommendation, not an ASTM, AWS, MIL, or Navy specification limit. |


*Table: The table separates quantitative Sb evidence in brass, binary Cu–Sb, and tin bronze from qualitative weldability warnings for Cu–Ni and aluminum bronze. It supports a provisional 0.02 wt% impurity cap while making clear that this value is not a formal specification.*

## 1. Function and alloy-specific precedent

**Brasses.** [CITE] Sb added to α Cu–Zn brass suppresses preferential Zn dissolution. Davies’s Copper Development Association (CDA) review describes an Sb-bearing surface film as a *proposed* explanation, analogous to the better-studied As mechanism; it does not establish an Sb oxide species, film resistance, or Sb enrichment by surface analysis. Adding Sb₂O₃ to an aggressive test solution did **not** reproduce inhibition, so an externally applied oxide and Sb incorporated into the metal must not be equated. Predominantly β or duplex brass remains susceptible despite Sb. There is no demonstrated Sb deoxidation, grain-refining, or marine-film-forming function in the proposed Cu–Ni/NAB deposits. (davies1993anoteon pages 1-3, davies1993anoteon pages 3-4)

**Commercial identification versus verified specification.** [SPEC] Inhibited admiralty brass **UNS C44400** is the pertinent intentional-Sb commercial precedent; the **0.02–0.10 wt% Sb** range supplied in the question is an identification of that grade, **not a limit independently authenticated against the text of ASTM B111/B171 in this search**. It is a *brass* design range, not permission to add 0.10 wt% Sb to C71500 or C95800. The retrieved composition table for wrought C70600 and C71500 does not identify Sb as a specified alloying addition; the DOE/CDA assessment expressly classifies Sb as detrimental in Cu–Ni and aluminum bronzes. No independently verified intentional-Sb range was obtained for C95800, Mn–Al bronze, tin bronze/gunmetal, Cu–Ni–Sn, Cu–Ni–Si, or AWS A5.7 ERCuNi, ERCuAl-A2, ERCuNiAl and ERCuMnNiAl fillers. Nor was a numeric Sb maximum authenticated for ASTM B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726 or EN 12449. **“Unspecified” must not be reported as a certified 0 wt% limit.** [GAP] (konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155, konynenburg1990backgroundstudiesin pages 136-142, lewis1981evaluationofcoppernickel pages 38-43)

**Bronze interaction.** [NUMBERS] In a literature survey of *cast tin bronzes*, **0.18 wt% Sb** was reported to severely reduce ductility: Sb decreased Sn solubility and increased brittle Sn-rich δ phase. This is evidence *against* using Sb as a generic dealloying inhibitor in Sn-bearing gunmetals, not a measured failure threshold for Sn-free NAB. Neither Cu–Ni–Sn nor Cu–Ni–Si has a retrieved Sb-specific marine benefit. [CITE] Riley and Makar, “Impurity effects in secondary copper alloys,” *Conservation & Recycling* **9** (1986), 315–323, doi:**10.1016/0361-3658(86)90066-4**. (riley1986impurityeffectsin pages 1-3, riley1986impurityeffectsin pages 3-4)

## 2. Seawater corrosion: what is—and is not—quantified

[NUMBERS] Davies summarizes Lombardi’s **0, 0.10 and 0.20 wt% Sb** additions to α **Cu–30Zn** and duplex **Cu–40Zn**, tested in **5 wt% CuCl₂ solution**. Sb gave the best inhibition of the As/Sb/P additions in the α alloy; raising inhibitor content beyond **0.10 wt%** produced little or no additional benefit. Those are concentrations and a response ranking—not extractable corrosion-rate values, and **5 wt% CuCl₂ is neither seawater nor 3.5 wt% NaCl**. Under static or cyclic stress, the same historical review reports increased intercrystalline attack/failure with inhibiting additions, attributed by the original investigator to grain-boundary precipitation; a numerical Sb-only onset was not given. [CITE] D. D. Davies, *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions*, CDA report 7013-0009 (July 1993), §2.2, summarizing P. Lombardi, *Metallurgia Italiana* **45** (1953), 449, and **46** (1954), 91, 123. No DOI was identified for the CDA report or these historical articles. (davies1993anoteon pages 1-3, davies1993anoteon pages 3-4)

[GAP] **No Sb-controlled, composition-matched Cu–Ni or NAB study was found** that establishes a beneficial or harmful concentration interval in natural seawater, ASTM D1141 substitute ocean water, or 3.5 wt% NaCl. Consequently, numerical changes in corrosion rate, *E*<sub>corr</sub>, polarization resistance, impedance/film resistance, pit or crevice depth, selective-attack depth, and erosion-corrosion or allowable velocity **cannot be assigned to Sb**. Lewis and LaQue’s seawater data provide *Sb-uncontrolled comparators*, not an Sb treatment effect: C71500 with **0.4 wt% Fe** showed approximately **0.0005–0.0011 inches/year** in the stated natural-seawater trials, while admiralty brass had **0.0015–0.0029 inches/year** in those trials; the specific Sb content of the admiralty specimens was not reported. Their review states that C70600 performed well to **3.0 m/s**, but this is **not an Sb-dependent velocity limit**. [CITE] R. O. Lewis and F. L. LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, Argonne National Laboratory report ANL/OTEC-BCM-019 (1981), doi:**10.2172/6255887**, tables I and XV. (lewis1981evaluationofcoppernickel pages 1-7, lewis1981evaluationofcoppernickel pages 55-60, lewis1981evaluationofcoppernickel pages 38-43)

## 3. DED, welding and repair interfaces

[CITE] A DOE/CDA review places Sb among detrimental impurities for **both aluminum bronzes and Cu–Ni**; it reports that Sb tends to segregate to grain boundaries and impairs copper-alloy weldability and brazability, and specifically calls Sb unacceptable for Cu–Ni welding. Its account of aluminum-bronze welds also warns of reduced ductility in the **400–600 °C** range associated with impurity segregation. These are **wrought/casting/welding judgments, not Sb-controlled laser-DED crack-frequency measurements**. [CITE] R. A. Van Konynenburg *et al.*, *Background Studies in Support of a Feasibility Assessment on the Use of Copper-Base Materials for Nuclear Waste Packages in a Repository in Tuff* (1990), doi:**10.2172/137782**. The report concerns a DOE application, **not a Navy Sb prohibition**. (konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155, konynenburg1990backgroundstudiesin pages 136-142)

[GAP] For single-stream laser DED, interdendritic Sb enrichment plausibly threatens **solidification cracking** and subsequent pass reheating plausibly threatens **grain-boundary liquation cracking**. These are risk hypotheses from the above metallurgy, **not demonstrated Sb-specific laser mechanisms or thresholds**. No Sb-controlled data were obtained for DED porosity; Sb evaporation/oxidation under a 1.07-µm laser; powder-to-deposit Sb recovery; or dilution/cracking when depositing on **cast C95800** or **wrought C71500**. In particular, neither AWS filler precedent nor clean Cu–Ni/NAB weldability validates an Sb-bearing deposit. Measure Sb and O before and after deposition, examine fusion boundaries and reheated layers for Sb segregation and cracks, and assess the corrosion of the *diluted interface* separately from the bulk deposit. (konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155, konynenburg1990backgroundstudiesin pages 136-142)

## 4. Atomization and thermodynamics

[NUMBERS] In binary Cu–Sb, the reported maximum equilibrium Sb solubility in α-Cu is **7.8 at% at 645 °C**, equivalent to approximately **13.9 wt% Sb** using Cu and Sb atomic masses; the reported values at **484 °C** and **440 °C** correspond to approximately **11.8** and **10.4 wt% Sb**, respectively. *These are equilibrium binary solubilities, not defensible alloy-addition ceilings:* segregation and the Cu–Ni/Al/Sn phase equilibria can impose much tighter processing limits. Reported binary phases include Cu₃Sb, Cu₄Sb, Cu₁₀Sb₃ and Cu₂Sb; the assessed description reports peritectoid/eutectoid reactions near **484, 467, 440, 427 and 360 °C**, and a Cu₂Sb-related peritectic near **586 °C**. [CITE] S. Fürtauer and H. Flandorfer, “A new experimental phase diagram investigation of Cu–Sb,” *Monatshefte für Chemie* **143** (2012), 1275–1287, doi:**10.1007/s00706-012-0737-1**; W. Gierlotka and D. Jendrzejczyk-Handzlik, “Thermodynamic description of the Cu–Sb binary system,” *Journal of Alloys and Compounds* **484** (2009), 172–176, doi:**10.1016/j.jallcom.2009.05.056**; phase-summary and reproduced binary diagram in M. Mödlinger, *Structures and Phase Equilibria in the Ternary Cu–As–Sb System*, University of Genoa doctoral thesis (2023). (modlinger2023structuresandphase pages 10-16, modlinger2023structuresandphase pages 50-53, modlinger2023structuresandphase media 63c0f99d)

[NUMBERS] The **dilute, Cu-rich binary liquidus decreases**, rather than increases, on adding Sb to pure Cu (melting near **1085 °C**): trace Sb alone is not a credible route to a liquidus above the atomizer’s **~1,200–1,250 °C** practical ceiling. This does **not** prove that a high-Ni or other multicomponent composition meets that ceiling. A published **binary Cu–Sb thermodynamic assessment exists**; the available evidence does *not* authenticate a complete **Cu–Ni–Sb or Cu–Al–Sb ternary assessment in TCCU**, nor coverage in COST 531 or a usable public TDB. Verify installed TCCU constituents/phases, then compare its predictions against the published binary and measured melt/solidification data; do not mistake a calculable extrapolation for an assessed ternary. (modlinger2023structuresandphase pages 10-16, modlinger2023structuresandphase pages 50-53, modlinger2023structuresandphase media 63c0f99d)

[GAP] There is no recovered Sb-specific result for **argon induction melting in alumina/zirconia**, reaction with **graphite**, transfer from a **Ti-alloy or Mo sonotrode**, oxygen pickup, surface tension, or Sb vapor-loss fraction during ultrasonic atomization. At **0.5 kg**, the proposed **0.02 wt%** cap corresponds to just **0.10 g Sb** in a charge: analytical contamination and sampling matter. Oxidation/fume loss, inclusions, and altered droplet formation should be treated as **process risks to test**, not measured effects or proof that Sb acts as a deoxidizer. The DOE review specifically notes that aluminum-bronze slag/crucible reactions and melt-refining difficulty demand tight feedstock control. (konynenburg1990backgroundstudiesin pages 136-142)

## 5. Supply, safety, bounds and coupled constraints

[SPEC] **Regulation and supply.** USGS material confirms **Sb and Cu on the final 2025 U.S. critical-minerals list**; it reports recycling as the only domestic Sb supply source in 2025. The inspected sources do not reproduce the full **2022** final list, so this search does **not independently verify the requested 2022-versus-2025 comparison**. An older industry document quotes the OSHA **29 CFR 1910.1000, Table Z-1, Sb limit as 0.5 mg/m³, 8-hour exposure**; use local exhaust/contained powder transfer and assess airborne Sb-bearing dust and laser fume against the current applicable rule. It is an *airborne exposure limit*, not a permissible alloy composition. No defensible dated **Sb-metal price in USD/kg**, current Sb-specific **REACH** entry, **RoHS** alloy prohibition, or Navy/DoD Sb ban was established from the retrieved sources; none is asserted here. Do not adopt an old solder-industry statement about absence of Sb-oxide fumes during soldering as a laser-DED safety finding. [CITE] N. T. Nassar *et al.*, USGS Open-File Report **2025-1047**, doi:**10.3133/ofr20251047**; J. V. Jones III *et al.*, USGS, “Annual Review 2025: Critical Minerals” (May 2026); D. Suraski, *A Study of Antimony in Solder*, citing OSHA Table Z-1 (publication date/DOI not established). (nassar2025methodologyandtechnical pages 4-9, suraskiUnknownyearastudyof pages 1-4, staff2022usgsminingreview pages 6-9, iii2026usgscriticalminerals pages 1-2)

**Bound and failure mode.** [NUMBERS] [GAP] Set **impurity maximum 0.02 wt% Sb (200 ppm) for each Cu–Ni or Al-bronze powder and deposit**, and aim for ≤0.01 wt% where purchasing and analytical capability permit. The **0.02 wt% value is a precautionary program specification chosen here**, **not** an ASTM B111/B171/B466/B148/B369, AWS A5.7, MIL or EN 12449 Sb limit and **not** a validated tolerable cracking threshold. It sits below the question’s **0.02–0.10 wt%** intentionally Sb-inhibited *brass* range and well below the **0.18 wt%** ductility warning in cast tin bronze; these cross-family values justify caution but cannot prove safety at 0.02 wt% in DED. The governing failure mode is Sb enrichment at solidification/reheated grain boundaries, with possible hot cracking and loss of ductility; the tin-bronze-specific additional mode is Sn-rich δ formation. Because the decision is **LIMIT**, a conservative addition maximum, aggressive addition maximum and functional floor for Cu–Ni/NAB are **not applicable**. The **0.10 wt%** brass test level is neither a functional floor nor a transferable marine-deposit target. (davies1993anoteon pages 3-4, riley1986impurityeffectsin pages 3-4, konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155)

**Interactions for joint constraints.** [CITE] [GAP] Evaluate **Sb × Sn** for δ-phase/ductility in any Sn-bearing design; **Sb × Zn and α/β fraction** for brass dealloying (benefit does not survive a β-rich microstructure); and **Sb × Al/Fe/Ni/Mn** through segregation, κ/β distributions and interface dilution in NAB/Cu–Ni. Evaluate **Sb with Bi, Pb, S, Te, O and P** as *coexisting* impurity or grain-boundary risks, **not** as a proven numerical sum or ratio. Fe and Mn changed brass dealloying in Davies’s review, but it provides **no measured Sb–Fe, Sb–Mn or Sb–Ni synergistic coefficient**; Sb has not been shown here to neutralize any of these elements in marine deposits. (davies1993anoteon pages 4-5, riley1986impurityeffectsin pages 3-4, davies1993anoteon pages 5-6, konynenburg1990backgroundstudiesin pages 142-149, davies1993anoteon pages 6-8, konynenburg1990backgroundstudiesin pages 149-155)

**Evidence assessment.** [GAP] Confidence is **moderate that intentional Sb addition should be avoided**, based on convergent brass-specific benefit and copper-family embrittlement/welding warnings; confidence in **any particular numerical marine-DED impurity ceiling is thin**. The central unresolved experiment is a controlled Sb series in *pre-alloyed* Cu–Ni and NAB/intermediate powders, assaying powder and deposit and testing crack density, diluted repairs, and **as-deposited** ASTM D1141 electrochemistry plus selective-attack depth against wrought C71500. No publication by the named PI was used. (davies1993anoteon pages 3-4, riley1986impurityeffectsin pages 3-4, konynenburg1990backgroundstudiesin pages 142-149, konynenburg1990backgroundstudiesin pages 149-155)

VERDICT | Sb | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.02 | evidence=thin

References

1. (konynenburg1990backgroundstudiesin pages 142-149): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

2. (konynenburg1990backgroundstudiesin pages 149-155): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

3. (davies1993anoteon pages 3-4): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

4. (davies1993anoteon pages 1-3): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

5. (modlinger2023structuresandphase pages 10-16): M Mödlinger. Structures and phase equilibria in the ternary cu-as-sb system. Unknown journal, 2023.

6. (modlinger2023structuresandphase pages 50-53): M Mödlinger. Structures and phase equilibria in the ternary cu-as-sb system. Unknown journal, 2023.

7. (modlinger2023structuresandphase media 63c0f99d): M Mödlinger. Structures and phase equilibria in the ternary cu-as-sb system. Unknown journal, 2023.

8. (riley1986impurityeffectsin pages 3-4): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

9. (konynenburg1990backgroundstudiesin pages 136-142): R.A. Van Konynenburg, K.J.A. Kundig, W.S. Lyman, M. Prager, J.R. Meyers, and I.S. Servi. Background studies in support of a feasibility assessment on the use of copper-base materials for nuclear waste packages in a repository in tuff. ArXiv, Jun 1990. URL: https://doi.org/10.2172/137782, doi:10.2172/137782. This article has 1 citations.

10. (lewis1981evaluationofcoppernickel pages 38-43): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

11. (riley1986impurityeffectsin pages 1-3): William D. Riley and Harry V. Makar. Impurity effects in secondary copper alloys. Conservation & Recycling, 9:315-323, Jan 1986. URL: https://doi.org/10.1016/0361-3658(86)90066-4, doi:10.1016/0361-3658(86)90066-4. This article has 12 citations.

12. (lewis1981evaluationofcoppernickel pages 1-7): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

13. (lewis1981evaluationofcoppernickel pages 55-60): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

14. (nassar2025methodologyandtechnical pages 4-9): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

15. (suraskiUnknownyearastudyof pages 1-4): D Suraski. A study of antimony in solder. Unknown journal, Unknown year.

16. (staff2022usgsminingreview pages 6-9): US Staff. Usgs mining review. Unknown journal, 2022.

17. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

18. (davies1993anoteon pages 4-5): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

19. (davies1993anoteon pages 5-6): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

20. (davies1993anoteon pages 6-8): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.
