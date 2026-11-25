<!--
Edison Scientific LITERATURE task (phase 1)
- Task ID: bc684233-0a2d-4ae8-821a-b229696e2bea
- Submitted: 2026-10-17T18:58:27Z
- Fetched: 2026-10-17T19:27:52Z (status: success)
- Raw trajectory JSON: ../raw/el-01-Cu.json.gz
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

ELEMENT UNDER REVIEW: Cu (the matrix). Copper is the balance element. Navy seawater alloys span about 65-70 wt% Cu (70-30 Cu-Ni, C71500), 86-89 wt% (90-10, C70600), 78-82 wt% (NAB, C95800) and 71-78 wt% (Mn-Al bronze, C95700).

Answer for copper as the balance element:
1. LOWER BOUND Cu_min: give a CONSERVATIVE Cu_min (stays within established
   seawater copper alloys) and a NON-CONSERVATIVE Cu_min (defensible but more
   aggressive), in wt%, with reasons: the alpha (fcc) phase field and the
   onset of beta or other second phases, the atomizer limit (liquidus about
   1,200-1,250 C), the validity range of copper CALPHAD databases (TCCU is
   built for copper-rich alloys), and what still counts as a copper alloy
   (UNS C designations).
2. Is there a practical UPPER bound on Cu (a minimum total solute needed for
   seawater resistance or strength), e.g. compared with unalloyed copper in
   seawater?
3. How should the matrix bound interact with the two families (70-30 Cu-Ni at
   about 65-70 wt% Cu versus NAB at about 78-82 wt% Cu): one continuous space
   or two sub-spaces? What is the total solute budget for each?
4. Effects of the copper source (oxygen-free vs tough-pitch, recycled scrap)
   on the powder and deposit.
5. Failure modes that set each bound, and EVIDENCE QUALITY.

End with exactly one line in this format, filled in:
VERDICT | Cu | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_min_wt=<number or NA> | nonconservative_min_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

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

ELEMENT UNDER REVIEW: Cu (the matrix). Copper is the balance element. Navy seawater alloys span about 65-70 wt% Cu (70-30 Cu-Ni, C71500), 86-89 wt% (90-10, C70600), 78-82 wt% (NAB, C95800) and 71-78 wt% (Mn-Al bronze, C95700).

Answer for copper as the balance element:
1. LOWER BOUND Cu_min: give a CONSERVATIVE Cu_min (stays within established
   seawater copper alloys) and a NON-CONSERVATIVE Cu_min (defensible but more
   aggressive), in wt%, with reasons: the alpha (fcc) phase field and the
   onset of beta or other second phases, the atomizer limit (liquidus about
   1,200-1,250 C), the validity range of copper CALPHAD databases (TCCU is
   built for copper-rich alloys), and what still counts as a copper alloy
   (UNS C designations).
2. Is there a practical UPPER bound on Cu (a minimum total solute needed for
   seawater resistance or strength), e.g. compared with unalloyed copper in
   seawater?
3. How should the matrix bound interact with the two families (70-30 Cu-Ni at
   about 65-70 wt% Cu versus NAB at about 78-82 wt% Cu): one continuous space
   or two sub-spaces? What is the total solute budget for each?
4. Effects of the copper source (oxygen-free vs tough-pitch, recycled scrap)
   on the powder and deposit.
5. Failure modes that set each bound, and EVIDENCE QUALITY.

End with exactly one line in this format, filled in:
VERDICT | Cu | decision=<INCLUDE or LIMIT or EXCLUDE> | family=<Cu-Ni or Al-bronze or both or none> | conservative_min_wt=<number or NA> | nonconservative_min_wt=<number or NA> | floor_wt=<number or NA> | impurity_max_wt=<number or NA> | evidence=<strong or moderate or thin>

OUTPUT FORMAT: Be quantitative and specific to this element. Give full
citations with DOIs (journal papers, standards, handbooks, technical reports).
Tag items: [CITE] worth citing; [NUMBERS] gives a quantitative value; [SPEC] a
limit or range from a standard or specification (name it: ASTM B111/B171/
B466/B148/B369, MIL-T-16420, MIL-B-24480, MIL-C-15726, AWS A5.7, EN 12449,
UNS/CDA data); [NAVY] Navy or DoD use or funding; [GAP] something not yet
studied. If the literature does not answer a part, say so plainly instead of
padding with loosely related work; say when you rely on welding, casting or
wrought data instead of AM data. Express every composition in wt%.


# Copper as the balance element: composition decision

**Recommendation.** Set **Cu ≥65 wt%** for the conservative search and permit **Cu ≥60 wt%** only in a separately flagged, non-conservative **Cu–Ni-rich exploratory branch**. These are *design bounds*, not UNS or Thermo-Calc specifications. Apply the stronger, family-specific constraint **Cu ≥79 wt%** to a C95800-like nickel–aluminum-bronze (NAB) branch. Reject candidates whose **calculated liquidus is not sufficiently below the approximately 1,300 °C melt-module ceiling to provide useful atomization superheat**; meeting a Cu minimum does not establish meltability. [CITE][SPEC][NUMBERS] R. O. Lewis and F. L. LaQue, *Evaluation of Copper-Nickel Alloys for OTEC Applications*, Argonne National Laboratory report ANL/OTEC-BCM-019 (1981), DOI: **10.2172/6255887**; W. Sochu, *Stress Corrosion Cracking of Nickel Aluminium Bronze under Ammonia-Containing Artificial Seawater* (2020), ASTM B148 chemistry reproduced therein, **no verified DOI**. (lewis1981evaluationofcoppernickel pages 38-43, sochu2020stresscorrosioncracking pages 23-28, mccright1988anannotatedhistory pages 58-60)

The following comparators show why the two families require different solute budgets. “Balance” is not an independently specified numerical Cu minimum. [SPEC][NUMBERS] (lewis1981evaluationofcoppernickel pages 38-43, sochu2020stresscorrosioncracking pages 23-28, cuevas2002microstructurecharacterizationof pages 26-29)

| Comparator | Cu (wt%) | Ni (wt%) | Al (wt%) | Fe (wt%) | Mn (wt%) | Solute budget (wt%) | Basis and source |
|---|---:|---:|---:|---:|---:|---:|---|
| UNS C71500, 70–30 Cu–Ni | Balance; 69.5 nominal¹ | 29.0–33.0; 30.0 nominal | — | 0.40–0.70; 0.50 nominal | ≤1.0 | ≈30.5 nominal | DOE Lewis and LaQue, Table I, DOI: 10.2172/6255887; nominal Cu is calculated from balance, not an independently specified Cu minimum. (lewis1981evaluationofcoppernickel pages 38-43, mccright1988anannotatedhistory pages 58-60) |
| UNS C70600, 90–10 Cu–Ni | Balance; ≈88.5 nominal¹ | 9.0–11.0; 10.0 nominal | — | 1.0–1.8; 1.5 nominal | ≤1.0 | ≈11.5 nominal | DOE Lewis and LaQue, Table I, DOI: 10.2172/6255887; nominal Cu is calculated from balance, not an independently specified Cu minimum. (lewis1981evaluationofcoppernickel pages 38-43) |
| UNS C95800 NAB | ≥79.0; 81 nominal | 4.0–5.0; 5 nominal | 8.5–9.5; 9 nominal | 3.5–4.5; 4 nominal | 0.8–1.5; 1 nominal | ≈19 nominal | ASTM B148 limits reproduced by Sochu; NPS Cuevas gives the nominal chemistry. (sochu2020stresscorrosioncracking pages 23-28, cuevas2002microstructurecharacterizationof pages 26-29) |
| UNS C95820 NAB | ≥77.5 | 4.5–5.8 | 9.0–10.0 | 4.0–5.0 | ≤1.5 | ≤22.5² | ASTM B148 limits reproduced by Sochu; Zn ≤0.2 wt% and Sn ≤0.02 wt%. (sochu2020stresscorrosioncracking pages 23-28) |
| ¹ Balance calculation | — | — | — | — | — | — | Calculated nominal Cu excludes unspecified residuals and is not a statutory minimum. |
| ² Cu-minimum implication | — | — | — | — | — | — | A Cu minimum of 77.5 wt% implies no more than 22.5 wt% total non-Cu content by mass balance. |


*Table: Verified wt% comparator chemistries and derived solute budgets for the Cu–Ni and nickel–aluminum-bronze families. Calculated balance values are distinguished from explicit specification minima.*

## 1. Lower bound: phase constitution, equipment, and classification

**Conservative, 65 wt% Cu.** C71500 is established seawater-service, approximately Cu–30 wt% Ni–0.5 wt% Fe; its specified Ni interval is **29–33 wt%**, Fe **0.4–0.7 wt%**, and Cu is balance. A **65 wt% Cu** formulation therefore accommodates approximately **35 wt% total solutes** at the high-Ni edge plus a restricted minor-element allowance. It is a conservative *rounded design guardrail*, **not** an ASTM requirement or a promise that every mixture of 35 wt% solutes is seawater resistant. Cu–Ni is an extensive fcc solid-solution system, but a low Cu value obtained by adding Al, Fe, Cr, or other solutes cannot be assumed to remain single-phase merely because Cu–Ni itself does. [CITE][SPEC][NUMBERS] Lewis and LaQue (1981), DOI: **10.2172/6255887**, Table I; R. D. McCright, *An Annotated History of Container Candidate Material Selection*, technical report (1988), DOI: **10.2172/60703**. (lewis1981evaluationofcoppernickel pages 38-43, mccright1988anannotatedhistory pages 58-60, lewis1981evaluationofcoppernickel pages 43-48)

**Non-conservative, 60 wt% Cu.** This permits up to **40 wt% total non-Cu elements**, primarily to ask whether a Cu–Ni-rich, comparatively simple composition can outperform the benchmark. It is *not* an established 70–30 specification, a proved lower seawater threshold, or an invitation to combine the full Ni and Al-bronze solute allowances. The extrapolation must pass individual TCCU phase and liquidus calculations, casting/atomization trials, and as-deposited corrosion tests. In a 78-day seawater study summarized by Lewis and LaQue, a **60 wt% Cu–40 wt% Ni** specimen had a late-to-early corrosion-rate *ratio* of **0.17**, versus **0.18** for **70 wt% Cu–30 wt% Ni**; these ratios are **not absolute corrosion rates** and do not qualify the 60 wt% Cu composition for the present process. [CITE][NUMBERS][GAP] Lewis and LaQue (1981), DOI: **10.2172/6255887**, Table XVIII. (lewis1981evaluationofcoppernickel pages 55-60)

**The equipment may veto even the established benchmark.** A handbook-derived C715-type **liquidus of approximately 1,240 °C** leaves only approximately **60 °C** between liquidus and the stated 1,300 °C induction-module maximum, before crucible and transfer losses. It is thus near—or outside—the stipulated useful-superheat window of **liquidus ≤approximately 1,200–1,250 °C**. Reducing Cu by increasing Ni generally pushes the Ni-rich Cu–Ni melt toward the higher-melting constituent; consequently **60 wt% Cu is only a conditional computational bound, not a commitment to atomize it**. First demonstrate thermal margin at the actual 0.5 kg charge and measure the liquidus. [CITE][NUMBERS] McCright (1988), DOI: **10.2172/60703**, Copper Alloy No. 715 property table. (mccright1988anannotatedhistory pages 58-60)

**Alpha is a family-specific, not a Cu-only, constraint.** In binary Cu–Al, below approximately **7 wt% Al** the material solidifies and remains fcc α, whereas above approximately **9.4 wt% Al** solidification starts as bcc β; Ni and Fe alter those boundaries and create κ intermetallics. Nominal **C95800, 81 wt% Cu–9 wt% Al–5 wt% Ni–4 wt% Fe–1 wt% Mn**, itself solidifies initially as β before developing α and κ. Therefore “fcc α throughout solidification” would incorrectly exclude the established NAB benchmark; the relevant as-deposited question is *how much corrosion-susceptible retained β/β′, γ, κ, or other segregated phase remains*, particularly across DED remelt zones. In cast C95800 tested in **3.5 wt% NaCl**, annealing decreased β from **>20% to approximately 7%** and improved corrosion resistance—useful evidence of the **no-post-build-treatment risk**, not evidence that annealing is permissible for this proposal. [CITE][NUMBERS][NAVY] A. M. Cuevas, *Microstructure Characterization of Friction-Stir Processed Nickel-Aluminum Bronze Through Orientation Imaging Microscopy*, Naval Postgraduate School thesis (2002), **no verified DOI**, https://hdl.handle.net/10945/3027; H. R. Jafari, A. Davoodi and S. Hosseinpour, “Effect of Fluid Flow on the Corrosion Performance of as-Cast and Heat-Treated Nickel Aluminum Bronze Alloy (UNS C95800) in Saline Solution,” *Corrosion and Materials Degradation* **2**, 61–77 (2021), DOI: **10.3390/cmd2010004**. (cuevas2002microstructurecharacterizationof pages 21-26, cuevas2002microstructurecharacterizationof pages 26-29, jafari2021effectoffluid pages 2-4)

**CALPHAD and designation are checks, not numeric proof.** TCCU5 is developed for *Cu-based alloys* and covers **32 elements**, **148 assessed binaries** and **64 assessed ternaries**; higher-order results can depend on extrapolation. The retrieved database description supplies **no universal Cu wt% validity cutoff** and no validation of every proposed Cu–Ni–Al–Fe–Mn combination at 60 wt% Cu. Similarly, C71500/C70600 and C95800 are genuine UNS **C** copper-alloy designations, but there is **no evidence here that every novel composition above an invented 50 wt% Cu rule receives a UNS C designation**. Classify the candidate by its actual Cu-rich matrix and evaluated chemistry; seek a designation only if an applicable specification exists. [CITE][NUMBERS][GAP] Å. Jansson and colleagues, “Phase Transformations and Kinetic Simulations of Cu-based Alloys,” *Copper Alloys 2022* conference proceedings, pp. 28–31, **no verified DOI**; Y. Tang, Q. Chen and A. Engström, “Kinetic Simulations of Diffusion-Controlled Phase Transformations in Cu-Based Alloys,” *Diffusion Foundations* **15**, 1–22 (2018), DOI: **10.4028/www.scientific.net/DF.15.1**. (janssonUnknownyearphasetransformationsanda pages 28-30, lewis1981evaluationofcoppernickel pages 38-43, sochu2020stresscorrosioncracking pages 23-28)

## 2. Upper Cu limit: performance rather than a purity prohibition

There is **no established universal Cu maximum or minimum-total-solute rule** that guarantees the target “at least wrought C71500” corrosion performance. But **nearly unalloyed Cu should be a negative process/performance control, not the main candidate space**: Cu–Ni alloying produces a more resistive corrosion-product film. In the comparison tabulated by Lewis and LaQue, electronic/ionic Cu₂O-film resistances were **5.5/4.0 × 10³ Ω·cm² for Cu**, **23.5/11 × 10³ Ω·cm² for 90–10**, and **82.5/21 × 10³ Ω·cm² for 70–30**. These are film measurements, **not a direct proof that every low-solute copper fails 30-day seawater immersion**. Established C70600 provides a useful **approximately 88.5 wt% Cu, approximately 11.5 wt% solute** Cu–Ni reference; C95800 provides an **approximately 81 wt% Cu, 19 wt% solute** NAB reference. One can use **approximately 89–90 wt% Cu as a *pragmatic Cu–Ni search ceiling*** and **approximately 82 wt% as the C95800-like NAB neighborhood**, rather than claim either is a corrosion-derived universal maximum. The target remains measured *as-deposited* performance against wrought C71500. [CITE][NUMBERS][SPEC] Lewis and LaQue (1981), DOI: **10.2172/6255887**, Tables I and V; Cuevas (2002), Naval Postgraduate School thesis, **no verified DOI**. (lewis1981evaluationofcoppernickel pages 43-48, lewis1981evaluationofcoppernickel pages 38-43, cuevas2002microstructurecharacterizationof pages 26-29)

[NAVY][NUMBERS] The DOE review reports C70600/C71500 approximately **2.5–12.7 μm/year** in seawater and **<2.5 μm/year** after **14–16 years** in quiescent/low-velocity exposure; early 30-day flowing-seawater results can be much higher and are not a mature-film benchmark. This warrants retaining the proposed **30-day depth-of-attack endpoint** alongside OCP, polarization, and EIS, while acknowledging that 30 days cannot establish decades-long service equivalence. [CITE][GAP] Lewis and LaQue (1981), DOI: **10.2172/6255887**. (lewis1981evaluationofcoppernickel pages 14-17, lewis1981evaluationofcoppernickel pages 55-60)

## 3. Composition-space implementation and principal failure modes

Use **two constrained sub-spaces plus a deliberately small bridging set**, *not* one unconstrained box spanning **60–90 wt% Cu**. **Cu–Ni branch:** target **65–approximately 89 wt% Cu**, corresponding to **approximately 35–11 wt% total solutes**; anchor the high-performance end to C71500 (approximately **30.5 wt% nominal solutes**) and the lower-Ni comparison to C70600 (**approximately 11.5 wt% nominal solutes**). Extend to **60 wt% Cu/40 wt% solutes only if liquidus, fcc-dominant deposited structure, and seawater screening warrant it**. **NAB branch:** center near **79–82 wt% Cu/18–21 wt% solutes**, with the **C95800 specified ≥79 wt% Cu**; C95820 provides an established, but distinct, **≥77.5 wt% Cu/≤22.5 wt% non-Cu** benchmark. **C95700/Mn–Al bronze warrants its own chemistry and phase checks rather than assuming the C95800 budget applies.** The stated **71–78 wt% Cu** C95700 neighborhood is contextual here: I did not verify its full governing ASTM B148/B369 chemistry from an accessible specification, so I do not label that interval [SPEC]. [CITE][SPEC][NUMBERS][GAP] Lewis and LaQue (1981), DOI: **10.2172/6255887**; Sochu (2020), ASTM B148 reproduced, **no verified DOI**; Cuevas (2002), **no verified DOI**. (lewis1981evaluationofcoppernickel pages 38-43, sochu2020stresscorrosioncracking pages 23-28, cuevas2002microstructurecharacterizationof pages 26-29)

Screen **actual chemistry**, including Fe/Ni and Al together, using equilibrium plus Scheil/segregation estimates and metallography of the *actual deposited layer and diluted interface*. The Cu–Ni branch risks an unatomizable high liquidus, Ni-driven loss of the intended Cu-rich design, or loss of benchmark-like seawater films when Ni/Fe are removed. NAB and bridging compositions risk β/β′ retention, γ/dealuminification, κ-associated selective attack, and crack/porosity initiation; cast NAB evidence reports severe second-phase seawater attack when **Ni < Fe**, although this is **not a validated universal inequality for new DED alloys**. Laser powder-bed-fused NAB has shown as-printed seawater mass loss approximately **one order of magnitude below cast/wrought NAB** in a **3- and 6-month** comparison, illustrating that rapid solidification *can* help; that result is **LPBF, not single-stream blown-powder DED**, and does **not** establish parity with wrought C71500. [CITE][NUMBERS][GAP] Cuevas (2002), **no verified DOI**; Jafari et al. (2021), DOI: **10.3390/cmd2010004**; A. V. Nemani *et al.*, “Advancements in Additive Manufacturing for Copper-Based Alloys and Composites,” *Journal of Manufacturing and Materials Processing* **8**, 54 (2024), DOI: **10.3390/jmmp8020054**. (cuevas2002microstructurecharacterizationof pages 21-26, jafari2021effectoffluid pages 2-4, nemani2024advancementsinadditive pages 74-79)

## 4. Copper charge purity and powder

**Prefer documented oxygen-free Cu over tough-pitch Cu** for the 0.5 kg melt; charge purity must not be confused with final powder purity. ASTM F68 oxygen-free *electronic*-grade Cu is quoted at **≤0.0005 wt% O** (5 ppm), versus approximately **0.04 wt% O** (400 ppm) in electrolytic tough-pitch Cu. This is an **ASTM F68 grade limit**, *not* a measured limit on this laboratory’s unspecified oxygen-free copper or a justified oxygen acceptance limit for every NAB deposit. In independently measured copper powder, **approximately 0.0213–0.0219 wt% surface-bound O** occurred even without claiming a tough-pitch starting charge. Oxidized handling/reused powder, oxide inclusions, and contamination from mixed/unknown scrap can therefore erase the starting-material advantage; use certified charge records, measured powder and deposit O and chemistry, and inclusion/porosity inspection before accepting any scrap-derived melt. [CITE][SPEC][NUMBERS][GAP] C. Ledford *et al.*, “Characteristics and Processing of Hydrogen-Treated Copper Powders for EB-PBF Additive Manufacturing,” *Applied Sciences* **9**, 3993 (2019), DOI: **10.3390/app9193993**; L. Nyborg and Y. Cao, “Surface Chemical and Geometrical Properties of Pure Copper Powder Intended for Binder Jetting and Sintering,” *Surface and Interface Analysis* **54**, 944–953 (2022), DOI: **10.1002/sia.7107**. (ledford2019characteristicsandprocessing pages 1-3, nyborg2022surfacechemicaland pages 7-8)

High-oxygen copper powder exposed to hydrogen reduction produced **trapped H₂O, particle grain-boundary cracking, bubbles and spatter** in electron-beam powder-bed experiments; it is a **mechanistic warning, not a demonstrated identical failure during argon-shielded Cu-alloy laser DED**. Unalloyed Cu also combines high thermal conductivity and low absorption at the approximately **1.07 μm** fiber-laser wavelength: a review quotes **approximately 2–6% initial absorptivity** for Cu at approximately 1,064 nm, creating lack-of-fusion and reflection risks near a high-Cu search ceiling. Master-alloy additions and any scrap must be checked for unintended elements and ceramic/oxide inclusions; no defensible *single numerical maximum for all impurities* follows from the Cu-balance literature. [CITE][NUMBERS][GAP] Ledford *et al.* (2019), DOI: **10.3390/app9193993**; Nemani *et al.* (2024), DOI: **10.3390/jmmp8020054**. (ledford2019characteristicsandprocessing pages 13-16, nemani2024advancementsinadditive pages 5-8)

**Evidence quality: moderate overall.** [SPEC] UNS and ASTM B148 comparators and [CITE] longstanding Cu–Ni seawater performance strongly establish *reference compositions*. The precise **65 wt%/60 wt% design cutoffs**, approximately **90 wt% practical Cu ceiling**, rePOWDER processability of each chemistry, and **as-deposited C71500-equivalent corrosion across both repair substrates** remain [GAP] engineering hypotheses, not measured thresholds. Direct studies combining **pre-alloyed ultrasonic powder, single-stream infrared blown-powder DED, both substrates, no heat treatment, and the specified seawater/depth protocol** were not established by the retrieved sources. **Floor and impurity fields below are NA**: there is no independent Cu floor beyond the decision’s conditional Cu minima and no evidence-based universal residual-impurity maximum; element-specific limits belong in their own palette entries. (lewis1981evaluationofcoppernickel pages 38-43, sochu2020stresscorrosioncracking pages 23-28, nemani2024advancementsinadditive pages 74-79, ledford2019characteristicsandprocessing pages 1-3)

VERDICT | Cu | decision=LIMIT | family=both | conservative_min_wt=65 | nonconservative_min_wt=60 | floor_wt=NA | impurity_max_wt=NA | evidence=moderate

References

1. (lewis1981evaluationofcoppernickel pages 38-43): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

2. (sochu2020stresscorrosioncracking pages 23-28): MRW SOCHU and C Kanchanomai. Stress corrosion cracking of nickel aluminium bronze under ammonia-containing artificial seawater. Unknown journal, 2020.

3. (mccright1988anannotatedhistory pages 58-60): R. D. McCright. An annotated history of container candidate material selection. ArXiv, Jul 1988. URL: https://doi.org/10.2172/60703, doi:10.2172/60703. This article has 11 citations.

4. (cuevas2002microstructurecharacterizationof pages 26-29): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.

5. (lewis1981evaluationofcoppernickel pages 43-48): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

6. (lewis1981evaluationofcoppernickel pages 55-60): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

7. (cuevas2002microstructurecharacterizationof pages 21-26): AM Cuevas. Microstructure characterization of friction-stir processed nickel. Unknown journal, 2002.

8. (jafari2021effectoffluid pages 2-4): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

9. (janssonUnknownyearphasetransformationsanda pages 28-30): Å Jansson, Y Tang, S Jin, M Ghasemi, and CM Lancelot. Phase transformations and kinetic simulations of cu-based alloys. Unknown journal, Unknown year.

10. (lewis1981evaluationofcoppernickel pages 14-17): R. O. Lewis and F. Laque. Evaluation of copper-nickel alloys for otec applications. ArXiv, Apr 1981. URL: https://doi.org/10.2172/6255887, doi:10.2172/6255887. This article has 5 citations.

11. (nemani2024advancementsinadditive pages 74-79): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.

12. (ledford2019characteristicsandprocessing pages 1-3): Christopher Ledford, Christopher Rock, Paul Carriere, Pedro Frigola, Diana Gamzina, and Timothy Horn. Characteristics and processing of hydrogen-treated copper powders for eb-pbf additive manufacturing. Applied Sciences, 9:3993, Sep 2019. URL: https://doi.org/10.3390/app9193993, doi:10.3390/app9193993. This article has 66 citations.

13. (nyborg2022surfacechemicaland pages 7-8): Lars Nyborg and Yu Cao. Surface chemical and geometrical properties of pure copper powder intended for binder jetting and sintering. Surface and Interface Analysis, 54:944-953, May 2022. URL: https://doi.org/10.1002/sia.7107, doi:10.1002/sia.7107. This article has 11 citations and is from a peer-reviewed journal.

14. (ledford2019characteristicsandprocessing pages 13-16): Christopher Ledford, Christopher Rock, Paul Carriere, Pedro Frigola, Diana Gamzina, and Timothy Horn. Characteristics and processing of hydrogen-treated copper powders for eb-pbf additive manufacturing. Applied Sciences, 9:3993, Sep 2019. URL: https://doi.org/10.3390/app9193993, doi:10.3390/app9193993. This article has 66 citations.

15. (nemani2024advancementsinadditive pages 5-8): Alireza Vahedi Nemani, Mahya Ghaffari, Kazem Sabet Bokati, Nima Valizade, Elham Afshari, and Ali Nasiri. Advancements in additive manufacturing for copper-based alloys and composites: a comprehensive review. Journal of Manufacturing and Materials Processing, 8:54, Mar 2024. URL: https://doi.org/10.3390/jmmp8020054, doi:10.3390/jmmp8020054. This article has 100 citations.
