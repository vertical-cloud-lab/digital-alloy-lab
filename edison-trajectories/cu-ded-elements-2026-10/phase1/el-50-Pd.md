<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: a3701dd9-736a-43ce-91c9-80bae66a8c9a
- Submitted: 2026-10-17T19:02:05Z
- Fetched: 2026-10-17T19:28:16Z (status: success)
- Raw trajectory JSON: ../raw/el-50-Pd.json.gz
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

ELEMENT UNDER REVIEW: Pd (platinum group). Representative of the platinum group metals: small Pd or Ru additions make titanium and stainless steels passivate (cathodic modification); is there any analogue for copper alloys in seawater, and any Cu-Pd corrosion data?

Answer for Pd specifically, not for copper alloys in general:
1. ROLE: what Pd does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Pd ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Pd changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Pd, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Pd, Cu-Ni-Pd and Cu-Al-Pd are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Pd in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Pd neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Pd | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Pd (platinum group). Representative of the platinum group metals: small Pd or Ru additions make titanium and stainless steels passivate (cathodic modification); is there any analogue for copper alloys in seawater, and any Cu-Pd corrosion data?

Answer for Pd specifically, not for copper alloys in general:
1. ROLE: what Pd does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Pd ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Pd changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Pd, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Pd, Cu-Ni-Pd and Cu-Al-Pd are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Pd in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Pd neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Pd | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Pd in pre-alloyed marine copper powders

**Decision: EXCLUDE Pd as a designed addition from the principal Cu-balanced composition search, for both Cu–Ni and aluminum-bronze families.** This is an evidence decision, not a finding that Pd necessarily damages either alloy. The most relevant positive chloride result concerns a *nickel-balanced* experimental welding filler, whereas the Cu-rich result concerns an electrodeposited coating without a composition-matched Pd-free control. Neither establishes a Pd content that improves an **as-deposited**, copper-rich DED repair to the seawater performance of wrought C71500. Pd also adds a critical, costly input without demonstrated nickel displacement. A separately funded, explicitly exploratory comparison would be reasonable; assigning it a validated composition bound in this proposal would not. (liang2010acorrosionstudy pages 10-11, martinuzzi2023analysisandstudy pages 170-179, liang2010acorrosionstudy pages 2-3)

## 1. Role, mechanisms, and specifications

[CITE] **Demonstrated outside the target family:** Liang *et al.*, “A corrosion study of nickel–copper and nickel–copper–palladium welding filler metals,” *Materials and Corrosion* **61** (2010), 909–919, doi: **10.1002/maco.200905583**, made experimental Ni-balanced fillers with approximately **0.24–1.3 wt% Pd**. The authors found better localized-corrosion behavior at approximately **1 wt% Pd** in dilute chloride; their proposed use was welding **304L stainless steel**, not repairing NAB or Cu–Ni. Their work does not establish titanium-like cathodic modification or a passive-film mechanism in a copper-balanced alloy. (liang2010acorrosionstudy pages 1-2, liang2010acorrosionstudy pages 2-3, liang2010acorrosionstudy pages 10-11)

[CITE] **Cu-rich but confounded:** Martinuzzi, *Analysis and Study of Industrially and Technologically Interesting Surfaces* (2023 thesis; **no verified DOI**), investigated an electrodeposited, Zn-free **Cu–Sn–1 wt% Pd** white-bronze coating. Compared with a *different* Zn-bearing Cu–Zn–Sn coating, it resisted chloride attack better; the author attributed much of the distinction to a continuous **SnO₂-rich** surface film, found **no Pd phase by XRD**, and expressly could not establish Pd’s contribution. These are coating results, not evidence that Pd deoxidizes, grain-refines, inhibits dealloying, or alters NAB’s protective film. (martinuzzi2023analysisandstudy pages 170-179, martinuzzi2023analysisandstudy pages 164-170)

[GAP] For copper-balanced Cu–Ni, conventional and nickel-aluminum bronze, Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, and Cu–Ni–Si, I found **no verified Pd-specific marine-alloy mechanism or useful commercial/Navy Pd range**. In particular, no evidence establishes Pd-containing κ precipitates in NAB, Pd-assisted Cu–Ni surface-film chemistry, or Pd neutralization of Fe, Mn, or Al. Pd-rich *dental* Cu–Pd alloys do exhibit selective Cu dissolution and Pd surface enrichment in artificial saliva; that observation warns against equating surface ennoblement with suppression of subsurface selective attack in seawater. Sun, *On the Corrosion Behavior and Biocompatibility of Palladium-Based Dental Alloys* (2004 thesis; **no verified DOI**). (sun2004onthecorrosion pages 23-27, sun2004onthecorrosion pages 31-36)

[SPEC][GAP] **No Pd-containing range was verified** for the named marine forms—ASTM **B111/B111M, B171/B171M, B466/B466M, B148, B369/B369M**; **MIL-T-16420, MIL-B-24480, MIL-C-15726**; **EN 12449**—or for **AWS A5.7** fillers **ERCuNi, ERCuAl-A2, ERCuNiAl, and ERCuMnNiAl**. Nor was a Pd-bearing Navy/UNS designation established. This means *no documented designed-Pd range was found*, **not** that these specifications impose a verified zero-Pd analytical limit. Liang’s experimental Ni–Cu–Pd stainless-steel consumables must not be relabeled AWS A5.7 marine fillers. (liang2010acorrosionstudy pages 1-2, liang2010acorrosionstudy pages 2-3)

## 2. Seawater corrosion: what is actually quantitative

The table separates observed chloride behavior from an attributable Pd effect. **There is no measured Pd-beneficial or Pd-harmful composition interval for the specified Cu-balanced alloys in natural seawater, ASTM D1141 water, or 3.5 wt% NaCl.** Likewise, no Pd-specific corrosion penetration rate, C71500-equivalence result, erosion–corrosion velocity limit, or 30-day selective-attack depth was established. (liang2010acorrosionstudy pages 10-11, martinuzzi2023analysisandstudy pages 170-179)

| Evidence system | Pd and comparator compositions (wt%) | Environment and quantitative result | Key limitation | Transferability to Cu-rich marine DED |
|---|---|---|---|---|
| Liang et al. (2010), **Ni-rich weld metals** | Ni–8Cu–0Pd; Ni–5Cu–0.24Pd; Ni–7.6Cu–1.3Pd | Aerated 0.1 M NaCl; 50% dilution SMA welds. Mean repassivation potential, *E*rp: **51.1, 64.4, and 110.1 mV vs SCE**, respectively. Authors concluded **0.24 wt% Pd gave no detectable improvement**, whereas approximately **1 wt% Pd improved corrosion behavior**. (liang2010acorrosionstudy pages 3-5, liang2010acorrosionstudy pages 5-6, liang2010acorrosionstudy pages 10-11) | Ni is the balance; Cu and Pd both vary, and substrate dilution introduces Fe/Cr. The electrolyte is approximately 0.58 wt% NaCl, not seawater or 3.5 wt% NaCl. | Useful only as indirect evidence for cathodic modification and a possible **approximately 1 wt%** screening level; it is **not a proven Pd threshold** for Cu-rich Cu–Ni or aluminum bronze. |
| Martinuzzi (2023), **electrodeposited white-bronze coatings** | Cu–Sn–**1Pd** compared with compositionally different Cu–Zn–Sn coating | 3.5 wt% NaCl: charge-transfer resistance, *R*ct, **6.92 × 10⁴ Ω** for Cu–Sn–1Pd versus **3.96 × 10³ Ω** for Cu–Zn–Sn; the Pd-bearing coating retained its appearance. (martinuzzi2023analysisandstudy pages 170-179, martinuzzi2023analysisandstudy pages 164-170) | No matched Pd-free Cu–Sn control; Zn, Sn, Pd, coating structure, and deposition behavior are confounded. XRD detected no Pd phase, and the study could not establish that Pd caused the improvement. | Supports testing **1 wt% Pd** as an exploratory coating/alloy level only; it does **not isolate Pd’s effect** and cannot establish a bulk-alloy functional floor. |
| Cu-rich marine alloys and DED | Cu–Ni, aluminum bronze/NAB, Mn–Al bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, Cu–Ni–Si | **No matched Pd-added versus Pd-free bulk-alloy study was located** in natural seawater, ASTM D1141 substitute seawater, or 3.5 wt% NaCl; no Pd-specific DED dataset was located. | No quantitative evidence for corrosion rate, selective attack, pitting/crevice resistance, erosion–corrosion, velocity limit, cracking, or dilution in the target Cu-rich families. | The available Ni-rich weld and electrodeposited-coating results are **not transferable as a proven Pd threshold or design bound** for marine Cu-alloy DED. |


*Table: The only quantitative chloride evidence found is indirect and compositionally confounded. Neither dataset establishes a functional Pd threshold for Cu-rich marine DED alloys.*

[NUMBERS] In Liang’s **Ni-balanced** welds, mean repassivation potentials for approximately **Ni–8Cu–0Pd**, **Ni–5Cu–0.24Pd**, and **Ni–7.6Cu–1.3Pd** were **51.1, 64.4, and 110.1 mV versus SCE**, respectively, in aerated **0.1 M NaCl** (approximately **0.58 wt% NaCl**). The Cu contents differ, and the tested stainless-steel welds were diluted; this is neither a controlled Cu-rich Pd series nor seawater. The same paper concludes that **0.24 wt% Pd gave no detectable improvement**, despite some favorable individual immersion results, while approximately **1 wt%** improved the Ni-rich weld’s corrosion properties. Its **25 wt% NaCl, pH 1.5** stress-corrosion experiment is also not neutral seawater. (liang2010acorrosionstudy pages 3-5, liang2010acorrosionstudy pages 5-6, liang2010acorrosionstudy pages 10-11, liang2010acorrosionstudy pages 2-3, liang2010acorrosionstudy pages 6-8)

[NUMBERS] For the **Cu–Sn–1Pd coating** versus Zn-bearing Cu–Zn–Sn, the reported charge-transfer resistances in **3.5 wt% NaCl** were **6.92 × 10⁴ versus 3.96 × 10³ Ω**; those are *coating-system* values, not an isolated Pd increment or bulk-film resistance normalized to area. The Pd-bearing coating still showed localized attack, and the author could not assign its better overall behavior to Pd rather than removal of Zn, altered Sn chemistry, or coating integrity. **Neither dataset identifies a range in which Pd harms a target marine alloy.** (martinuzzi2023analysisandstudy pages 170-179, martinuzzi2023analysisandstudy pages 164-170)

## 3. DED, repair dilution, and powder production

[CITE][GAP] No Pd-containing copper-balanced blown-powder DED experiment or Pd-controlled **ERCuNi/ERCuAl-A2/ERCuNiAl/ERCuMnNiAl** weld comparison was found for solidification cracking, reheated-layer liquation, porosity, laser loss, or corrosion at the **C95800** or wrought Cu–Ni fusion boundary. Liang’s Ni-balanced **SMA** welds contained substantial porosity, whereas their **GTA** welds generally performed better; this is evidence about process and consumable differences, **not evidence that Pd causes or cures porosity** in argon-shielded copper DED. Their stainless-steel dilution experiments cannot validate NAB or Cu–Ni repair. (liang2010acorrosionstudy pages 2-3, liang2010acorrosionstudy pages 6-8, liang2010acorrosionstudy pages 10-11)

[CITE] Kou, “Predicting Susceptibility to Solidification Cracking and Liquation Cracking by CALPHAD,” *Metals* **11** (2021), 1442, doi: **10.3390/met11091442**, gives an appropriate *screen*, not a Pd result: calculate temperature–fraction-solid curves for powder, substrate, reheated deposit, and diluted interface; assess late-stage mushy-zone behavior and partially melted substrate/layer behavior separately. For a proposed Pd trial, evaluate both **Cu–Ni–Pd** and **Cu–Al–Ni–Fe–Pd** at realistic dilution fractions. Do not infer freedom from cracking merely from equilibrium Cu–Pd solubility. (kou2021predictingsusceptibilityto pages 1-2)

[GAP] No quantified Pd-specific charge recovery, oxidation rate, Al₂O₃/ZrO₂ or graphite-crucible reaction, Ti-alloy/Mo-sonotrode attack, surface-tension shift, or **1.07-µm** laser evaporation loss was located for the stated **0.5-kg, argon, approximately 1,300 °C** process. Pd metal is not demonstrated to act as a deoxidizer in Cu melts. The operational tests are whether a *fully dissolved* charge attains useful superheat below the module limit and whether ICP measurements show equal Pd contents in charge, powder size fractions, and deposit; laser-fume capture remains necessary. These are proposed controls, **not published Pd recovery factors**. (almufachi2015effectsofpalladium pages 95-99, kou2021predictingsusceptibilityto pages 1-2)

## 4. Cu–Pd equilibria and database readiness

[CITE][NUMBERS] A published binary assessment exists: Li, Du, Guo and Li, “A thermodynamic modeling of the Cu–Pd system,” *CALPHAD* **32** (2008), 439–446, doi: **10.1016/j.calphad.2008.04.004**. The phase-diagram review in Al-Mufachi, *Effects of Palladium Thin Films on the Hydrogen Permeability of Pd–Cu Alloy Membranes* (2015 thesis; **no verified DOI**), describes a disordered **FCC Cu–Pd** solution across the binary’s composition range at sufficiently high temperature and lower-temperature ordering. It lists **Cu₃Pd/L1₂** at approximately **12.1–32.1 wt% Pd**, long-period ordered structures at approximately **25.5–42.9 wt% Pd**, and **CuPd/B2** at approximately **48.5–59.8 wt% Pd**. These are reported *structure/composition ranges*, **not** a maximum Pd solubility at a specified temperature and **not** justified bounds for a marine powder. Thus a unique finite “maximum solid solubility in Cu, wt% at temperature” cannot responsibly be extracted: high-temperature FCC extends through the binary, while ordering changes low-temperature phase constitution. A trial at approximately 1 wt% Pd is far below the cited Cu₃Pd range in the **binary**, but ternary segregation is unresolved. (almufachi2015effectsofpalladium pages 95-99, yang2022simulatingsegregationin pages 8-8)

[GAP] The retrieved evidence does **not** resolve Cu-rich invariant reaction coordinates, a reliable numerical liquidus-versus-Pd slope, or the Pd content at which a particular NAB/Cu–Ni composition crosses **1,200–1,250 °C**. Pd’s high elemental melting point is not a substitute for that multicomponent calculation. **Cu–Pd has a published CALPHAD assessment; whether the installed Thermo-Calc TCCU version contains assessed Pd-bearing Cu–Pd, Cu–Ni–Pd, or Cu–Al–Pd interactions is unverified.** Likewise, no suitable COST 531 Pd-bearing assessment/TDB for this marine composition space was verified. Confirm constituent lists and interaction provenance before treating any TCCU or pycalphad output as predictive; otherwise label it extrapolation. (almufachi2015effectsofpalladium pages 95-99, kou2021predictingsusceptibilityto pages 1-2)

## 5. Supply, cost, safety, and interactions

[CITE][NUMBERS] Palladium is treated as a supply-risk commodity in Nassar *et al.*, USGS *Open-File Report 2025–1047*, doi: **10.3133/ofr20251047**; its modeled probability-weighted US GDP disruption is approximately **US$85 million**, versus approximately **US$56 million** for refined copper in the cited analysis. The former is **not a Pd price**. Palladium was on the **2022 US critical-minerals list** and remained on the **2025 final list**; copper was added in 2025. The available sources did **not** substantiate a dated palladium spot/contract quotation, so a defensible **US$/kg figure is not supplied** rather than fabricating one; budgeting requires a dated supplier quotation. Supply concentration provides a further reason not to assume Pd is a low-cost way to reduce Ni. (nassar2025methodologyandtechnical pages 4-9, nassar2025methodologyandtechnical pages 27-28, cherepovitsyn2026analysisofthe pages 15-16)

[CITE][GAP] Elemental Pd and soluble **Pd²⁺ compounds are not toxicologically interchangeable**. Reports reviewed for Pd-rich dental alloys describe contact hypersensitivity and ion release after selective dissolution; this does not establish a risk threshold for marine powder. No Pd-specific **OSHA permissible exposure limit**, RoHS/REACH prohibition, or Navy restriction applicable to these powders was verified here. In particular, **do not substitute a platinum-compound exposure limit for palladium**. Use enclosed powder transfer, dust and ignition assessment, local extraction of laser plume, respiratory-exposure monitoring, and alloy-specific SDS/occupational review. Sun’s dental-alloy evidence is indirect for this workplace. (sun2004onthecorrosion pages 17-23, sun2004onthecorrosion pages 31-36, sun2004onthecorrosion pages 23-27)

[GAP] No validated **Pd:Ni, Pd:Fe, Pd:Mn, Pd:Al, or Pd:Sn ratio**, combined-solute ceiling, or element that Pd reliably neutralizes was found for the target deposits. The Ni-balanced weld experiment changes **Cu and substrate-derived Fe/Cr** as well as Pd; the Cu–Sn coating comparison changes **Zn/Sn**. Pd–Cu ordering at much higher Pd contents does not prove a useful Pd–Al or Pd–Fe precipitate in dilute NAB. Explicitly retain these covariates in any later joint-constraint experiment rather than transfer an apparent one-element effect. (liang2010acorrosionstudy pages 2-3, martinuzzi2023analysisandstudy pages 170-179, almufachi2015effectsofpalladium pages 95-99)

## 6. Bounds and evidence quality

**[GAP] EXCLUDE, family = none for a designed Pd addition.** **Conservative maximum, non-conservative maximum, and functional floor: NA**—there is neither an established Cu-balanced commercial/Navy Pd range nor a controlled Cu-balanced marine test from which to set them. **Impurity maximum: NA**—EXCLUDE is not a measured zero-tolerance impurity specification, and no cited powder/deposit standard or study supplies a defensible Pd ppm cap. Do **not** use **0.24 wt%** (a negative result in *Ni-balanced* welds), **approximately 1 wt%** (a Ni-balanced weld result and confounded Cu–Sn coating content), or **12.1 wt%** (a binary ordered-phase boundary) as a marine Cu-alloy limit. The controlling failure is presently **failure of evidence and qualification**: no demonstrated as-deposited C71500-equivalent seawater resistance, plus unresolved interface attack, liquation/solidification behavior, liquidus margin, and cost. **Evidence: thin for the actual decision context**, notwithstanding sound evidence for the distinct Ni-rich weld and Cu–Pd binary observations. (liang2010acorrosionstudy pages 10-11, martinuzzi2023analysisandstudy pages 170-179, almufachi2015effectsofpalladium pages 95-99, kou2021predictingsusceptibilityto pages 1-2)

VERDICT | Pd | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin

References

1. (liang2010acorrosionstudy pages 10-11): D. Liang, J. W. Sowards, G. S. Frankel, B. T. Alexandrov, and J. C. Lippold. A corrosion study of nickel–copper and nickel–copper–palladium welding filler metals. Materials and Corrosion, 61:909-919, Nov 2010. URL: https://doi.org/10.1002/maco.200905583, doi:10.1002/maco.200905583. This article has 5 citations.

2. (martinuzzi2023analysisandstudy pages 170-179): SM Martinuzzi. Analysis and study of industrially and technologically interesting surfaces. Unknown journal, 2023.

3. (liang2010acorrosionstudy pages 2-3): D. Liang, J. W. Sowards, G. S. Frankel, B. T. Alexandrov, and J. C. Lippold. A corrosion study of nickel–copper and nickel–copper–palladium welding filler metals. Materials and Corrosion, 61:909-919, Nov 2010. URL: https://doi.org/10.1002/maco.200905583, doi:10.1002/maco.200905583. This article has 5 citations.

4. (liang2010acorrosionstudy pages 1-2): D. Liang, J. W. Sowards, G. S. Frankel, B. T. Alexandrov, and J. C. Lippold. A corrosion study of nickel–copper and nickel–copper–palladium welding filler metals. Materials and Corrosion, 61:909-919, Nov 2010. URL: https://doi.org/10.1002/maco.200905583, doi:10.1002/maco.200905583. This article has 5 citations.

5. (martinuzzi2023analysisandstudy pages 164-170): SM Martinuzzi. Analysis and study of industrially and technologically interesting surfaces. Unknown journal, 2023.

6. (sun2004onthecorrosion pages 23-27): D Sun. On the corrosion behavior and biocompatibility of palladium-based dental alloys. Unknown journal, 2004.

7. (sun2004onthecorrosion pages 31-36): D Sun. On the corrosion behavior and biocompatibility of palladium-based dental alloys. Unknown journal, 2004.

8. (liang2010acorrosionstudy pages 3-5): D. Liang, J. W. Sowards, G. S. Frankel, B. T. Alexandrov, and J. C. Lippold. A corrosion study of nickel–copper and nickel–copper–palladium welding filler metals. Materials and Corrosion, 61:909-919, Nov 2010. URL: https://doi.org/10.1002/maco.200905583, doi:10.1002/maco.200905583. This article has 5 citations.

9. (liang2010acorrosionstudy pages 5-6): D. Liang, J. W. Sowards, G. S. Frankel, B. T. Alexandrov, and J. C. Lippold. A corrosion study of nickel–copper and nickel–copper–palladium welding filler metals. Materials and Corrosion, 61:909-919, Nov 2010. URL: https://doi.org/10.1002/maco.200905583, doi:10.1002/maco.200905583. This article has 5 citations.

10. (liang2010acorrosionstudy pages 6-8): D. Liang, J. W. Sowards, G. S. Frankel, B. T. Alexandrov, and J. C. Lippold. A corrosion study of nickel–copper and nickel–copper–palladium welding filler metals. Materials and Corrosion, 61:909-919, Nov 2010. URL: https://doi.org/10.1002/maco.200905583, doi:10.1002/maco.200905583. This article has 5 citations.

11. (kou2021predictingsusceptibilityto pages 1-2): Sindo Kou. Predicting susceptibility to solidification cracking and liquation cracking by calphad. Metals, 11:1442, Sep 2021. URL: https://doi.org/10.3390/met11091442, doi:10.3390/met11091442. This article has 56 citations.

12. (almufachi2015effectsofpalladium pages 95-99): NA Al-Mufachi. Effects of palladium thin films on the hydrogen permeability of pd-cu alloy membranes. Unknown journal, 2015.

13. (yang2022simulatingsegregationin pages 8-8): Yilin Yang, Zhitao Guo, Andrew J. Gellman, and John R. Kitchin. Simulating segregation in a ternary cu–pd–au alloy with density functional theory, machine learning, and monte carlo simulations. Jan 2022. URL: https://doi.org/10.1021/acs.jpcc.1c09647, doi:10.1021/acs.jpcc.1c09647. This article has 27 citations.

14. (nassar2025methodologyandtechnical pages 4-9): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

15. (nassar2025methodologyandtechnical pages 27-28): Nedal T. Nassar, David Pineault, Sydney M. Allen, Dalton M. McCaffrey, Abraham J. Padilla, Jamie L. Brainard, Mani Bayani, Ensieh Shojaeddini, John W. Ryter, Sara Lincoln, and Elisa Alonso. Methodology and technical input for the 2025 u.s. list of critical minerals—assessing the potential effects of mineral commodity supply chain disruptions on the u.s. economy. Open-File Report, Jan 2025. URL: https://doi.org/10.3133/ofr20251047, doi:10.3133/ofr20251047. This article has 63 citations.

16. (cherepovitsyn2026analysisofthe pages 15-16): Alexey Cherepovitsyn, Irina Mekerova, and Alexander Nevolin. Analysis of the potential of palladium market: structural transformation of global demand in the context of the energy transition. Mining, 6:50, Jul 2026. URL: https://doi.org/10.3390/mining6030050, doi:10.3390/mining6030050. This article has 1 citations.

17. (sun2004onthecorrosion pages 17-23): D Sun. On the corrosion behavior and biocompatibility of palladium-based dental alloys. Unknown journal, 2004.
