<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: 267e7570-049b-4535-9dd3-a08dbe90274b
- Submitted: 2026-10-17T19:01:57Z
- Fetched: 2026-10-17T19:23:11Z (status: success)
- Raw trajectory JSON: ../raw/el-47-Nd.json.gz
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

ELEMENT UNDER REVIEW: Nd (rare earth). Neodymium additions to copper alloys, if any.

Answer for Nd specifically, not for copper alloys in general:
1. ROLE: what Nd does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Nd ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Nd changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Nd, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Nd, Cu-Ni-Nd and Cu-Al-Nd are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Nd in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Nd neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Nd | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Nd (rare earth). Neodymium additions to copper alloys, if any.

Answer for Nd specifically, not for copper alloys in general:
1. ROLE: what Nd does in copper alloys used in seawater (Cu-Ni, aluminum
   bronze and NAB, Mn-Al bronze, tin bronze and gunmetal, brasses, Cu-Ni-Sn,
   Cu-Ni-Si, others) and by what mechanism (solid solution, which precipitates
   or intermetallics, protective film chemistry, deoxidation, grain
   refinement, dealloying inhibition). List the commercial or Navy alloys and
   specifications that contain it, with their Nd ranges in wt%.
2. SEAWATER CORROSION: quantitative evidence on how Nd changes corrosion of
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
   temperature), intermetallics and invariant reactions in Cu-Nd, the effect
   on the liquidus (could it push the alloy above about 1,250 C?), and
   whether Cu-Nd, Cu-Ni-Nd and Cu-Al-Nd are assessed in a CALPHAD
   database (Thermo-Calc TCCU, COST 531, or a published TDB).
6. SUPPLY, COST, SAFETY: US critical mineral status (2022 list and 2025
   final list), approximate price per kg, toxicity and regulation (OSHA,
   RoHS/REACH, Navy restrictions), hazards for powder handling and laser fume.
7. BOUNDS, in wt% of Nd in the alloy (Cu balance):
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
   Fe, Mn, Al or other elements; elements that Nd neutralizes or worsens.
9. EVIDENCE QUALITY: where the evidence is thin, indirect, or contradictory.

End with exactly one line in this format, filled in:
VERDICT | Nd | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_max_wt=<number or NA> | nonconservative_max_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Neodymium (Nd) in marine copper-alloy DED

**Decision: LIMIT Nd as an adventitious impurity, not a designed addition.** The only located Nd-specific copper-alloy corrosion lead concerns approximately **0.05 wt% Nd in aluminum bronze tested in dilute mineral acids**, not seawater. No retrieved experiment establishes that Nd improves as-deposited Cu–Ni or nickel-aluminum bronze (NAB) in chloride, or that an Nd-bearing deposit meets the proposed wrought C71500 benchmark. Cu–Nd compounds and substantial rare-earth loss during copper-alloy melting instead create credible composition-control and inclusion risks. These are reasons for a cautious design decision, **not proof that 0.05 wt% Nd damages a DED deposit**. [CITE] [GAP] (davies1993anoteona pages 5-6, ciumag2016neodymiumelectrowinninginto pages 5-7)

## 1. Alloy role and specifications

Davies reports that Verma and colleagues observed improved *general* corrosion resistance after adding **0.05 wt% La, Ce, or Nd** to aluminum bronze in dilute sulfuric acid; a related report concerned dilute nitric acid. The retrieved account supplies neither the individually measured Nd effect nor the bronze’s composition. Deoxidation or microstructural modification is plausible, but Nd solid-solution strengthening, grain refinement, a protective Nd-containing seawater film, and inhibition of selective Al or Zn dissolution **were not demonstrated by this account**. Nd-containing Cu-rich compounds, rather than a documented strengthening precipitate in a qualified marine alloy, are the directly observed metallurgical phases. [CITE] [NUMBERS] [GAP] (davies1993anoteona pages 5-6, ciumag2016neodymiumelectrowinninginto pages 5-7)

For brass, a distinct **mischmetal** experiment charged **0.50 wt% mixed rare earths** into Cu–Zn–Pb but retained only **0.04 wt% *total* rare earths**—approximately **8% apparent recovery**. Davies attributed the loss principally to oxidation. The hot-worked and annealed brasses differed in dezincification behavior; neither the retained **Nd** concentration nor a beneficial Nd-specific effect was established. Mischmetal must not be represented as 0.04 wt% Nd. [CITE] [NUMBERS] (davies1993anoteona pages 5-6)

**[SPEC] [NAVY]** No verified intentional Nd range was found in the specified marine Cu–Ni, NAB/C95800, manganese-aluminum bronze, tin bronze/gunmetal, brass, Cu–Ni–Sn, or Cu–Ni–Si families, or in the named ASTM B111/B171/B466/B148/B369, MIL-T-16420/MIL-B-24480/MIL-C-15726, AWS A5.7, EN 12449, or UNS/CDA designations. **The verified Nd range is therefore *none established*, not a certified 0 wt% maximum:** absence of a named Nd addition cannot establish how an applicable standard treats unnamed residual elements. No Nd-bearing ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl filler specification, commercial grade, or Navy-approved repair deposit was substantiated by the retrieved evidence. [GAP] (davies1993anoteona pages 5-6)

## 2. Seawater corrosion: what can actually be quantified

**[NUMBERS] [GAP]** The sole individually identified experimental Nd addition is **0.05 wt%**, and its reported improvement is **qualitative, secondary-source evidence in mineral acid**. For *all* Nd concentrations in natural seawater, ASTM D1141 substitute ocean water, and **3.5 wt% NaCl**, the retrieved literature provides **no validated beneficial or harmful interval** for copper alloys. Nd-specific corrosion rates, *E*corr shifts, polarization currents, impedance/film resistances, maximum pit or selective-attack depths, crevice results, erosion–corrosion losses, and limiting seawater velocities are **not available**. It would be invalid to turn the mineral-acid observation or mixed-rare-earth brass dezincification result into a quantitative seawater claim. [CITE] [NUMBERS] [GAP] (davies1993anoteona pages 5-6, davies1993anoteona pages 8-9)

## 3. DED, welding, dilution, and powder preparation

**[GAP]** No Nd-controlled, pre-alloyed copper-powder laser DED, multilayer remelting, or Nd-bearing AWS marine-filler comparison was found. Consequently there is **no measured Nd effect** on deposit density, solidification or reheating-layer liquation cracking, porosity, laser evaporation, or oxidation loss, either self-built or on cast C95800 and wrought Cu–Ni. In particular, ordinary Nd-free welding or cladding performance cannot qualify Nd-bearing ERCuNi, ERCuAl-A2, ERCuNiAl, or ERCuMnNiAl analogues. A testable *risk hypothesis* is that Nd rejected into terminal liquid or Nd-rich particles could embrittle interdendritic regions and reheated interfaces; it is not a measured crack threshold. Substrate dilution would also make first-layer Nd content and any Nd–Al/Fe/Ni reaction products different from the powder nominal composition. [CITE] [GAP] (davies1993anoteona pages 5-6, ciumag2016neodymiumelectrowinninginto pages 5-7, ciumag2016neodymiumelectrowinninginto pages 7-8)

**[NUMBERS]** The **0.50→0.04 wt% total-rare-earth** brass observation is the closest retrieved copper-melt retention warning, but cannot be transferred as an Nd-specific recovery factor to argon-shielded ultrasonic atomization. Nd consumption by oxygen and associated oxide/dross or inclusion formation warrant measuring the charge, melt, powder, first-layer deposit, and upper layers independently. Reactions or pickup from **alumina versus zirconia crucibles**, graphite, a titanium-alloy versus molybdenum sonotrode, and Nd-dependent surface tension, atomization yield, powder oxygen, or fume losses have **no retrieved process-specific measurements**. A molybdenum cathode and graphite-lined vessel used in *molten-fluoride Nd extraction* are not evidence that a sonotrode or crucible is compatible with a molten copper–Nd charge. [CITE] [GAP] (davies1993anoteona pages 5-6, ciumag2016neodymiumelectrowinninginto pages 7-8, jr1972productionqualitycontrol pages 1-5)

## 4. Phase diagram and calculation readiness

**[CITE] [NUMBERS]** NdCu₄, NdCu₅, and NdCu₆ were identified in Cu–Nd droplets produced by electrochemical reduction at **900 °C**; droplets coalesced more readily at **1,040 °C**. This demonstrates Cu–Nd compound formation, **not** equilibrium phase fractions in a trace-Nd marine alloy. The cropped experimental micrograph shows the compound-bearing region. [CITE] (ciumag2016neodymiumelectrowinninginto pages 5-7, ciumag2016neodymiumelectrowinninginto pages 7-8, ciumag2016neodymiumelectrowinninginto media 42ec9898)

**[GAP]** The retrieved full texts do **not** supply a verifiable maximum Nd solubility in fcc Cu **in wt% and at a stated temperature**, Cu-rich invariant temperatures/compositions, or a Cu-rich liquidus slope. Published Cu–Nd phase-equilibrium and thermodynamic-assessment works can be identified bibliographically—Carnasciali, Costa and Franceschi, *Journal of the Less-Common Metals* **92** (1983) 97–103, DOI **10.1016/0022-5088(83)90230-8**; Zhuang *et al.*, *Journal of Phase Equilibria* **17** (1996) 508–521, DOI **10.1007/BF02665998**—but their numerical diagrams were not obtained here. Accordingly, **neither a Cu–Nd solubility-based ceiling nor a claim that trace Nd raises a candidate alloy above approximately 1,250 °C is defensible**. Calculate *each complete* Cu–Ni/Al/Fe/Mn/Nd candidate’s liquidus and solidification path before charging it; nominal Nd alone cannot decide whether the induction/atomization temperature constraint is met. An assessed Cu–Nd binary has been published, but Nd coverage and requisite interaction parameters in the **installed TCCU or COST 531 release**, and usable Cu–Ni–Nd or Cu–Al–Nd ternary descriptions, remain **unverified**. pycalphad requires an independently licensed/available TDB with the required phases and parameters; it cannot fill missing assessments by itself. [GAP] (ciumag2016neodymiumelectrowinninginto pages 5-7, ciumag2016neodymiumelectrowinninginto pages 7-8)

## 5. Supply and occupational controls

**[CITE] [NUMBERS]** Nd is an individually named mineral in the **final November 2025 USGS list of 60 critical mineral commodities**, alongside Cu and Ni; the 2025 list revised the 2022 list. Nd’s 2022 classification falls within the rare-earth listing, but the retrieved source does not establish the precise 2022 naming convention. The retrieved evidence does **not** establish a dated, like-for-like **USD/kg price for Nd *metal***: quoted Nd oxide or Nd–Pr magnet-feed prices should not be substituted for the price of certified Nd alloying metal. Likewise, no Nd-specific OSHA PEL, RoHS/REACH prohibition, or Navy compositional restriction was verified. [GAP] (iii2026usgscriticalminerals pages 1-2)

**[CITE] [NUMBERS]** Finely divided rare-earth metal oxidizes readily. An LLNL toxicity review reports weak-to-moderate lung lesions after intratracheal administration of **50 mg Nd oxide** to rats; its **1 mg/m³, 8-hour** occupational comparator is the *yttrium* PEL used as a precautionary analogy, **not an Nd-specific legal PEL**. Provide enclosed/inert powder transfer, ignition and dust controls, local extraction of laser fume, and an exposure assessment for Cu/Ni plus potentially Nd-containing particulates. The animal bolus study does not predict workplace exposure at 1 mg/m³. [GAP] (wald1990areviewof pages 12-20, wald1990areviewof pages 1-12, wald1990areviewof pages 24-30)

## 6. Search-space bounds and interactions

The following table separates observed composition values from the recommended **project-level**, unstandardized impurity-control rule.

| Evidence observation | Interpretation and limiting failure mode | Applicability to marine DED | Numerical bound or status |
|---|---|---|---|
| **0.05 wt% Nd** reportedly improved aluminum-bronze general corrosion only in dilute mineral acids. The available secondary source gives no quantitative chloride or seawater result. Davies cites N. Verma et al., *British Corrosion Journal* 25(2) (1990) 131 and R. N. Singh et al.; Davies DOI not confirmed. (davies1993anoteona pages 5-6, davies1993anoteona pages 8-9) | Possible microalloying, deoxidation, or film effects remain unresolved. Mineral-acid performance cannot establish resistance to pitting, selective attack, crevice corrosion, or erosion-corrosion in seawater. | Weak, indirect evidence from cast aluminum bronze—not Cu–Ni, NAB repair, powder, weld metal, or as-deposited DED. | **Not a validated upper bound or functional floor.** The 0.05 wt% value is an experimental acid-corrosion addition, not a marine specification. |
| **0.50 wt% mischmetal was charged, but only 0.04 wt% total rare earth was retained** in Cu–Zn–Pb brass, corresponding to approximately **8% apparent recovery**; the balance was presumed lost through oxidation. Davies cites B. A. Weldon, BNFMRA Research Report A1148 (1957); DOI not confirmed. (davies1993anoteona pages 5-6) | Strong oxygen-getter behavior predicts oxide and dross formation, composition drift, inclusions, and possible atomizer contamination. The retained amount was mixed rare earth, not Nd alone. | A relevant warning for induction melting and atomization, but not evidence of acceptable DED cracking or corrosion behavior. | **The 0.04 wt% residual is not an impurity specification.** It records mixed-RE retention after severe melt loss. |
| Cu–Nd processing produced **NdCu₄, NdCu₅, and NdCu₆** droplets; increasing temperature from **900 to 1,040 °C** promoted coalescence. Ciumag et al., *Journal of Fluorine Chemistry* 184 (2016) 1–7, DOI: **10.1016/j.jfluchem.2016.02.001**. (ciumag2016neodymiumelectrowinninginto pages 5-7, ciumag2016neodymiumelectrowinninginto pages 7-8, ciumag2016neodymiumelectrowinninginto pages 1-4, ciumag2016neodymiumelectrowinninginto media 42ec9898) | Confirms strong Cu–Nd compound formation rather than dependable Cu solid solution. Segregated intermetallics could introduce brittle particles, galvanic heterogeneity, terminal liquid, and liquation or solidification cracking. | Mechanistically relevant to rapidly solidified powder and reheated DED layers, but the experiment involved electroreduction—not welding, atomization, or corrosion testing. | **No phase-based marine limit is established.** Compound formation supports keeping unintended Nd well below the experimental 0.04–0.05 wt% levels until validated. |
| Light-rare-earth production requires strongly reducing conditions, and process materials can introduce impurities. Gschneidner, *The Production, Quality Control, and Applications of Pure RE Metals and Alloys* (1972), DOI: **10.2172/4598519**. (jr1972productionqualitycontrol pages 1-5) | Nd has high oxygen affinity; oxidation can consume the intended addition and create nonmetallic inclusions. Ceramic-crucible and sonotrode compatibility require direct testing. | Relevant to charge preparation and containment selection, but not a quantitative Cu-alloy atomization study. | **No published Nd-specific crucible or atomization maximum was found.** Control must use measured powder and deposit compositions rather than nominal charge composition. |
| **No Nd-specific tests were found** for Cu–Ni, NAB, Mn–Al bronze, Cu–Ni–Sn, Cu–Ni–Si, marine welding fillers, laser DED, natural or substitute seawater, or 3.5 wt% NaCl. | Unknown effects on cracking, porosity, evaporation, dilution, film resistance, pitting, selective attack, and velocity limits constitute the controlling evidence gap. | The absence of directly applicable evidence prevents treating Nd as a designed marine-alloy variable in the present search. | **Decision: LIMIT as an impurity only. No published Nd-specific maximum exists.** |
| Program-level control recommendation | Prevent unvalidated Nd intermetallics and oxides from confounding density, cracking, dilution, and corrosion while retaining a practical analytical-control threshold. | Applies to both Cu–Ni and aluminum-bronze families and to atomized powder and deposited metal. | **Provisional engineering screening policy—not a specification:** Nd **≤0.01 wt% (100 ppm)** in both powder and deposit. This is below the unvalidated **0.05 wt% Nd** acid experiment and approximately **0.04 wt% total-RE** brass residual. Quarantine material above 0.01 wt% pending Nd-specific DED and seawater qualification. |


*Table: Evidence does not support Nd as a designed marine-copper addition. The table distinguishes published observations from a provisional ≤0.01 wt% engineering QC policy, which is not an ASTM, AWS, Navy, or commercial-alloy specification.*

**LIMIT, both families: ≤0.01 wt% Nd (100 mass ppm) in *each* powder lot and representative deposit, pending analytical and DED validation.** This is a deliberately conservative **proposed QC ceiling, not an ASTM/AWS/MIL limit or a demonstrated tolerable corrosion threshold**. There is no defensible designed-addition conservative upper bound, aggressive upper bound, or marine functional floor. The controlling reasons are unknown chloride performance and interfacial cracking behavior, with oxygen-driven loss/oxide inclusions as a documented copper-melt warning. **0.05 wt%** is an acid-test addition, not a seawater floor or upper bound; **0.04 wt%** is residual *total* mischmetal, not a marine acceptance criterion. [CITE] [NUMBERS] [GAP] (davies1993anoteona pages 5-6, ciumag2016neodymiumelectrowinninginto pages 5-7)

**Interactions for later joint constraints.** No validated Nd:Ni, Nd:Fe, Nd:Mn, or Nd:Al ratio, nor a combined permissible Nd + other elements sum, was found. Assess Nd alongside **oxygen** first (loss, oxide inclusions, actual powder/deposit retention), then **Al, Ni, Fe, and Mn** for possible phase competition and first-layer dilution; assess S and Si as potential impurity/inclusion variables rather than claiming Nd neutralizes them in marine copper. Do **not** count any nickel reduction or seawater-film improvement from Nd until independently measured. [CITE] [GAP] (davies1993anoteona pages 5-6, ciumag2016neodymiumelectrowinninginto pages 5-7, jr1972productionqualitycontrol pages 1-5)

**Evidence quality: thin.** The crucial result is a secondary description of a mineral-acid aluminum-bronze study; the melt-loss result involves mixed rare earths; Cu–Nd compounds come from extraction, not DED; and no retrieved Nd-specific marine exposure, qualified filler, powder-atomizer trial, or repaired-interface result bridges these to as-deposited C71500-equivalent service. Principal sources: D. D. Davies, *A Note on the Dezincification of Brass and the Inhibiting Effect of Elemental Additions* (1993), references 6, 10, 38–39 (**DOI not verified**); R. N. Singh, S. K. Tiwari and W. R. Singh, “Effects of Ta, La and Nd Additions on the Corrosion Behaviour of Aluminium Bronze in Mineral Acids,” *Journal of Applied Electrochemistry* **22** (1992) 1175–1179, DOI **10.1007/BF01297420** (**primary text not obtained**); M. R. Ciumag *et al.*, “Neodymium Electrowinning into Copper-Neodymium Alloys by Mixed Oxide Reduction in Molten Fluoride Media,” *Journal of Fluorine Chemistry* **184** (2016) 1–7, DOI **10.1016/j.jfluchem.2016.02.001**; K. A. Gschneidner Jr., *The Production, Quality Control, and Applications of Pure RE Metals and Alloys* (1972), DOI **10.2172/4598519**; P. H. Wald, *A Review of the Literature on the Toxicity of Rare-Earth Metals* (LLNL, 1989/1990), DOI **10.2172/7259188**. [CITE] [GAP] (davies1993anoteona pages 5-6, davies1993anoteona pages 8-9, ciumag2016neodymiumelectrowinninginto pages 7-8, wald1990areviewof pages 1-12, jr1972productionqualitycontrol pages 1-5)

VERDICT | Nd | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.01 | evidence=thin

References

1. (davies1993anoteona pages 5-6): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

2. (ciumag2016neodymiumelectrowinninginto pages 5-7): M. R. Ciumag, M. Gibilaro, L. Massot, R. Laucournet, and P. Chamelot. Neodymium electrowinning into copper-neodymium alloys by mixed oxide reduction in molten fluoride media. Journal of Fluorine Chemistry, 184:1-7, Apr 2016. URL: https://doi.org/10.1016/j.jfluchem.2016.02.001, doi:10.1016/j.jfluchem.2016.02.001. This article has 21 citations and is from a peer-reviewed journal.

3. (davies1993anoteona pages 8-9): DD Davies. A note on the dezincification of brass and the inhibiting effect of elemental additions. Unknown journal, 1993.

4. (ciumag2016neodymiumelectrowinninginto pages 7-8): M. R. Ciumag, M. Gibilaro, L. Massot, R. Laucournet, and P. Chamelot. Neodymium electrowinning into copper-neodymium alloys by mixed oxide reduction in molten fluoride media. Journal of Fluorine Chemistry, 184:1-7, Apr 2016. URL: https://doi.org/10.1016/j.jfluchem.2016.02.001, doi:10.1016/j.jfluchem.2016.02.001. This article has 21 citations and is from a peer-reviewed journal.

5. (jr1972productionqualitycontrol pages 1-5): KA Gschneidner Jr. Production, quality control, and applications of pure re metals and alloys. Unknown journal, Jan 1972. URL: https://doi.org/10.2172/4598519, doi:10.2172/4598519.

6. (ciumag2016neodymiumelectrowinninginto media 42ec9898): M. R. Ciumag, M. Gibilaro, L. Massot, R. Laucournet, and P. Chamelot. Neodymium electrowinning into copper-neodymium alloys by mixed oxide reduction in molten fluoride media. Journal of Fluorine Chemistry, 184:1-7, Apr 2016. URL: https://doi.org/10.1016/j.jfluchem.2016.02.001, doi:10.1016/j.jfluchem.2016.02.001. This article has 21 citations and is from a peer-reviewed journal.

7. (iii2026usgscriticalminerals pages 1-2): JV Jones III, TJ Gallegos, and MA KunleDare. Usgs critical minerals review. Unknown journal, 2026.

8. (wald1990areviewof pages 12-20): PH Wald. A review of the literature on the toxicity of rare-earth metals as it pertains to the engineering demonstration system surrogate testing. Unknown journal, Jan 1990. URL: https://doi.org/10.2172/7259188, doi:10.2172/7259188.

9. (wald1990areviewof pages 1-12): PH Wald. A review of the literature on the toxicity of rare-earth metals as it pertains to the engineering demonstration system surrogate testing. Unknown journal, Jan 1990. URL: https://doi.org/10.2172/7259188, doi:10.2172/7259188.

10. (wald1990areviewof pages 24-30): PH Wald. A review of the literature on the toxicity of rare-earth metals as it pertains to the engineering demonstration system surrogate testing. Unknown journal, Jan 1990. URL: https://doi.org/10.2172/7259188, doi:10.2172/7259188.

11. (ciumag2016neodymiumelectrowinninginto pages 1-4): M. R. Ciumag, M. Gibilaro, L. Massot, R. Laucournet, and P. Chamelot. Neodymium electrowinning into copper-neodymium alloys by mixed oxide reduction in molten fluoride media. Journal of Fluorine Chemistry, 184:1-7, Apr 2016. URL: https://doi.org/10.1016/j.jfluchem.2016.02.001, doi:10.1016/j.jfluchem.2016.02.001. This article has 21 citations and is from a peer-reviewed journal.
