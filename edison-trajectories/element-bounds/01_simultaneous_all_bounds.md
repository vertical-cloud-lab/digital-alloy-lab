# Phase 1 — Simultaneous all-element bounds (LITERATURE_HIGH)

*Edison task: `1d872481-5007-4e13-b937-ea9a7d130dcf`*

## Answer

Question: PROJECT CONTEXT — FLAIME (Fast Learning AI for Mineral Efficiency), DOE Genesis
Mission Phase I, Topic 3-B (AMMTO). The team is performing Bayesian Optimization
over Function Networks (BOFN/pKGFN) over a single joint search space:
(Al + 15 non-Al alloying elements) x atomization process x LPBF process.

The 15 non-Al element palette is:
  Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn.

Composition is parameterized as weight fractions that sum to 1.0; Al is the
matrix element. Down-selection is driven by CALPHAD (TCAl10 + AM Module),
Scheil solidification range, hot-cracking susceptibility, printability, and a
mineral-burden objective (USGS criticality / import reliance).

Anchor systems include Al-Mn-Cr-Zr and Al-Zr; the broader palette is intended
to enable AI-discovered sub-systems (ternary through ~9-component). All alloys
are Al-rich (Al typically >= 85 wt% for good LPBF processability and to remain
within the trustworthy region of TCAl10's binary/ternary Muggianu extrapolation).

We need element-by-element compositional BOUNDS (in weight percent, wt%) for
the BOFN / GA acquisition inner-solver search space.


TASK — JOINT BOUNDS TABLE
Provide a single consolidated table of compositional bounds (in wt%) for
the entire FLAIME 15-element palette plus Al, in one go:
    Al, Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn

For EACH of the 16 elements include:
  * conservative lower bound (wt%) — Al only; 0 for the rest unless you
    argue otherwise
  * non-conservative lower bound (wt%)
  * conservative upper bound (wt%)
  * non-conservative upper bound (wt%)
  * primary failure mode setting the upper bound
  * key citation(s)

Use a markdown table. Then below the table, in a paragraph:

  (a) Reconcile the per-element upper bounds with the simplex constraint
      sum(wt%) = 100 — i.e. flag any bounds that, if all were saturated
      simultaneously, would produce an impossible (>100 wt%) composition.
  (b) Recommend any element-pair or element-group bounds (e.g.
      Cu + Li, Mg + Si, Sc + Zr, Fe + Si impurity sum) that are tighter
      than the marginal per-element bounds because of joint-failure modes
      (hot cracking, brittle intermetallics, eutectic depression,
      printability limits).
  (c) Suggest a default Al_min for the BOFN search space.

Be quantitative, cite peer-reviewed AM Al alloy literature, and use the
TCAl10 assessed-binary/ternary coverage as a guardrail for the
"non-conservative" bounds.



# FLAIME Joint Bounds Table for BOFN Search Space: Al + 15 Non-Al Alloying Elements

## 1. Consolidated Compositional Bounds Table

The following table provides element-by-element compositional bounds (in wt%) for the FLAIME 15-element palette plus Al, informed by equilibrium solubility data, rapid-solidification (RS) extended solubility under LPBF cooling rates (~10³–10⁶ K/s), experimentally demonstrated LPBF compositions, Kou/Scheil cracking susceptibility indices, and TCAl10 CALPHAD database coverage for Muggianu extrapolation at Al ≥ 85 wt%.

| Element | Conservative Lower (wt%) | Non-Conservative Lower (wt%) | Conservative Upper (wt%) | Non-Conservative Upper (wt%) | Primary Failure Mode Setting Upper Bound | Key Citations |
|---|---:|---:|---:|---:|---|---|
| Al | 85.0 | 80.0 | 99.5 | 99.9 | Balance element; upper bound set by simplex constraint and need to leave room for alloying additions | (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, aversa2019newaluminumalloys pages 8-10) |
| Mn | 0.0 | 0.0 | 5.0 | 8.0 | Primary Al-Mn intermetallic precipitation above ~6–8 wt% even under rapid solidification; equilibrium solubility ~1.8 wt%, RS-extended ~6–8 wt% | (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, mehta2022al–mn–cr–zrbasedalloystailored pages 2-2, martucci2022theinfluenceof pages 1-2) |
| Cr | 0.0 | 0.0 | 3.0 | 6.0 | Al-Cr intermetallic formation (e.g., Al7Cr/Al13Cr2); equilibrium solubility ~0.8 wt%, RS-extended ~3–6 wt% | (mehta2022al–mn–cr–zrbasedalloystailored pages 2-2, andreyachshenko2025technologicalalloyingimpact pages 13-16) |
| Zr | 0.0 | 0.0 | 1.0 | 2.0 | Primary Al3Zr formation; equilibrium solubility ~0.25 wt%; LPBF practical supersaturation limit ~0.6–0.7 wt% | (mehta2021highperformancealuminium pages 24-27, mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, mehta2022al–mn–cr–zrbasedalloystailored pages 2-2) |
| Mg | 0.0 | 0.0 | 5.0 | 8.0 | Evaporation/spatter and composition drift above ~5 wt%; hot-cracking susceptibility also peaks in binary Al-Mg near ~2.5–5 wt% | (montanari2023additivemanufacturingof pages 17-19, mauduit2017studyofthe pages 13-19, mauduit2017studyofthe pages 19-20, kou2015asimpleindex pages 11-12) |
| Si | 0.0 | 0.0 | 12.0 | 14.0 | Primary Si precipitation beyond the Al-Si eutectic (~12.6 wt%); near-eutectic Si is beneficial for crack resistance | (hesselmann2022effectofprecipitationforming pages 1-3, babu2020laserpowderbed pages 1-2, liu2024alloydesignfor pages 14-15, hyer2021compositiondependentsolidificationcracking pages 2-3) |
| Cu | 0.0 | 0.0 | 4.0 | 7.0 | Hot-cracking peak in low-Cu range (~1–3 wt% by Kou/CSI literature), plus θ-Al2Cu segregation/intermetallics and broadened freezing range at higher Cu | (rohilla2024investigationofalcu20si10mg pages 22-25, mauduit2017studyofthe pages 13-19, kou2015asimpleindex pages 11-12, zhang2021predictionofcracking pages 5-7) |
| Ti | 0.0 | 0.0 | 0.5 | 1.5 | Primary Al3Ti/peritectic intermetallic formation; useful as grain refiner only at low additions | (andreyachshenko2025technologicalalloyingimpact pages 2-4, andreyachshenko2025technologicalalloyingimpact pages 13-16) |
| Fe | 0.0 | 0.0 | 0.5 | 2.0 | Brittle Fe-bearing intermetallics (β-Al5FeSi/Al13Fe4-type) and impurity-driven embrittlement; equilibrium solubility is very low, RS can retain more | (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, montanari2023additivemanufacturingof pages 17-19, andreyachshenko2025technologicalalloyingimpact pages 2-4) |
| Ni | 0.0 | 0.0 | 0.5 | 2.0 | Al-Ni intermetallic formation (e.g., Al3Ni/Al9Ni2); equilibrium solubility very low, eutectic/intermetallic control dominates | (andreyachshenko2025technologicalalloyingimpact pages 2-4, andreyachshenko2025technologicalalloyingimpact pages 13-16) |
| Ce | 0.0 | 0.0 | 6.0 | 12.0 | Primary Al11Ce3 above the Al-Ce eutectic (~10.6 wt% Ce); equilibrium Ce solubility in Al is negligible (~0.005 wt%) | (hesselmann2022effectofprecipitationforming pages 1-3, hesselmann2022effectofprecipitationforming pages 14-15) |
| Sc | 0.0 | 0.0 | 0.8 | 1.5 | Cost/criticality and Al3Sc precipitation/peritectic constraints; LPBF alloys typically use ~0.66–1.1 wt% Sc | (montanari2023additivemanufacturingof pages 17-19, babu2020laserpowderbed pages 1-2, dixit2022laseradditivemanufacturing pages 15-16) |
| Li | 0.0 | 0.0 | 2.0 | 3.0 | δ/δ′-AlLi formation above ~2–2.5 wt%, severe evaporation (~15% loss), and sharp density drop by 3 wt% Li | (shao2024microstructureandmechanical pages 12-14, shao2024microstructureandmechanical pages 1-2) |
| Er | 0.0 | 0.0 | 0.5 | 1.5 | Al3Er intermetallic/coarsening with very low equilibrium solubility; useful as rare-earth grain refiner only at low additions | (andreyachshenko2025technologicalalloyingimpact pages 2-4) |
| Zn | 0.0 | 0.0 | 8.0 | 20.0 | Evaporation/spatter and hot cracking in vulnerable mid-range Al-Zn-Mg compositions (e.g., ~Al-7Zn-1Mg); high-Zn Al-rich alloys up to ~20 wt% have been demonstrated in LPBF | (mauduit2017studyofthe pages 19-20, babu2020laserpowderbed pages 1-2, charpagneUnknownyearfulllistofb pages 17-19, zhang2021predictionofcracking pages 9-12) |
| Sn | 0.0 | 0.0 | 0.1 | 0.5 | Liquid Sn segregation/monotectic immiscibility and very low melting Sn-rich phase; equilibrium solubility in Al is very small (~0.06–0.1 wt% order) | (schmidfetzer2009thermodynamicaspectsof pages 2-4, drapala2017contributiontothe pages 3-5) |


*Table: This table consolidates conservative and non-conservative wt% bounds for Al and the 15 non-Al alloying elements in the FLAIME LPBF BOFN search space. The bounds are tied to LPBF-relevant failure modes such as hot cracking, volatile-element evaporation, and brittle intermetallic formation, with citations to the gathered evidence.*

### Key Notes on Individual Elements

**Al (balance):** The conservative lower bound of 85 wt% ensures the alloy remains Al-rich, within the trustworthy extrapolation region of TCAl10's binary/ternary Muggianu formalism, and maintains good LPBF processability. The non-conservative lower of 80 wt% permits higher total alloying but pushes into less well-assessed CALPHAD territory (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, mehta2022al–mn–cr–zrbasedalloystailored pages 2-2).

**Mn:** Equilibrium solubility in Al is ~1.8 wt%, but rapid solidification in LPBF extends this to 6–8 wt% (mehta2022al–mn–cr–zrbasedalloystailored pages 2-2). Mehta et al. demonstrated crack-free LPBF at ~4.7–5.0 wt% Mn with up to 7 wt% total Mn+Cr in supersaturated solid solution (mehta2021highperformancealuminium pages 24-27, mehta2022al–mn–cr–zrbasedalloystailored pages 2-3). The conservative upper of 5.0 wt% reflects well-tested territory; the non-conservative upper of 8.0 wt% reflects the RS solubility ceiling.

**Cr:** Equilibrium solubility is only ~0.8 wt%, but RS extends it to 3–6 wt% (mehta2022al–mn–cr–zrbasedalloystailored pages 2-2). Agricola et al. demonstrated an Al–2.9Cr–1.3Mo–0.3Sc–0.3Zr alloy by LPBF, and Mehta tested 0.8 wt% Cr successfully (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3). The upper bound is set by Al₇Cr-type intermetallic precipitation.

**Zr:** Equilibrium solubility is ~0.25 wt%; LPBF practical supersaturation is ~0.6–0.7 wt% due to Al₃Zr precipitation during remelting cycles (mehta2021highperformancealuminium pages 24-27, mehta2022al–mn–cr–zrbasedalloystailored pages 2-2). Cooling rates >10⁴ K/s can theoretically extend this to ~2 wt% but this has not been reliably demonstrated.

**Mg:** Scalmalloy specifies Mg max at 4.90 wt% (montanari2023additivemanufacturingof pages 17-19). Mauduit et al. showed that an alloy with 8.7 wt% Mg suffered ~4.6% evaporative loss during LPBF, and Mg evaporation causes spatter and porosity (mauduit2017studyofthe pages 13-19, mauduit2017studyofthe pages 19-20). Kou's CSI model places peak binary Al-Mg cracking susceptibility at ~2.5–5 wt% Mg (kou2015asimpleindex pages 11-12). The conservative upper of 5.0 wt% reflects Scalmalloy practice; the non-conservative 8.0 wt% accounts for higher Mg in Al-Ce-Mg systems explored by Hesselmann et al. (hesselmann2022effectofprecipitationforming pages 1-3).

**Si:** Near-eutectic Al-Si alloys (AlSi10Mg at ~10 wt% Si, AlSi12 at ~12 wt%) are the most widely processed Al LPBF alloys due to narrow freezing range and good fluidity (hesselmann2022effectofprecipitationforming pages 1-3, babu2020laserpowderbed pages 1-2). Primary Si forms above the eutectic at ~12.6 wt%. The non-conservative upper of 14 wt% allows slight hypereutectic exploration.

**Cu:** Kou's cracking susceptibility index peaks at ~1–3 wt% Cu for binary Al-Cu (kou2015asimpleindex pages 11-12, zhang2021predictionofcracking pages 5-7, kou2015asimpleindex pages 10-11). Above this peak, increasing Cu through the eutectic (~33 wt%) reduces cracking, but θ-Al₂Cu intermetallic segregation and broadened freezing range remain problematic (rohilla2024investigationofalcu20si10mg pages 25-27, rohilla2024investigationofalcu20si10mg pages 22-25). The conservative upper of 4 wt% keeps compositions near or past the cracking peak; the non-conservative 7 wt% extends into 2xxx-type territory with Si co-additions for mitigation.

**Ti:** Useful as a grain refiner (Al₃Ti) at low additions (typically 0.05–0.15 wt% in commercial alloys) (montanari2023additivemanufacturingof pages 17-19, andreyachshenko2025technologicalalloyingimpact pages 2-4). Primary Al₃Ti forms via peritectic reaction above ~1.0–1.3 wt%; the conservative upper of 0.5 wt% and non-conservative upper of 1.5 wt% reflect grain-refiner vs. intermetallic boundaries.

**Fe:** Iron is typically controlled as an impurity; equilibrium solubility is ~0.05 wt% (andreyachshenko2025technologicalalloyingimpact pages 2-4). In LPBF, Fe levels of ~0.16 wt% are commonly reported in Al-Mn-Cr-Zr powders (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3). Above ~0.5 wt%, brittle β-Al₅FeSi needles form; however, some Al-Fe alloys for LPBF intentionally use 1–2 wt% Fe for dispersoid strengthening.

**Ni:** Equilibrium solubility is very low (~0.04 wt%); Al₃Ni/Al₉Ni₂ intermetallics form readily (andreyachshenko2025technologicalalloyingimpact pages 2-4, andreyachshenko2025technologicalalloyingimpact pages 13-16). Commercial alloys use up to ~1.4 wt% Ni for high-temperature strength. The conservative upper of 0.5 wt% limits intermetallic volume fraction.

**Ce:** The Al-Ce binary eutectic occurs at ~10.6 wt% Ce, with negligible equilibrium solubility (~0.005 wt%) (hesselmann2022effectofprecipitationforming pages 1-3). Near-eutectic Al-Ce compositions (~10 wt%) produce thermally stable Al₁₁Ce₃ nano-networks beneficial for LPBF (hesselmann2022effectofprecipitationforming pages 1-3, hesselmann2022effectofprecipitationforming pages 14-15). The conservative upper of 6 wt% keeps compositions hypoeutectic; the non-conservative upper of 12 wt% allows slight hypereutectic exploration.

**Sc:** Scalmalloy uses 0.66–1.1 wt% Sc (babu2020laserpowderbed pages 1-2, dixit2022laseradditivemanufacturing pages 15-16). The Scalmalloy specification caps Sc at 0.80 wt% (montanari2023additivemanufacturingof pages 17-19). Al₃Sc is the key strengthening precipitate. Cost and USGS criticality strongly constrain Sc; the non-conservative upper of 1.5 wt% matches the highest literature LPBF demonstrations.

**Li:** Commercial Al-Li alloys contain <2.5 wt% Li; the maximum solubility in α-Al is ~4.2 wt% (shao2024microstructureandmechanical pages 12-14). Shao et al. showed that at 3 wt% Li, density dropped to 92% and δ′-AlLi phase appeared; Li loss during SLM was ~15% (shao2024microstructureandmechanical pages 12-14, shao2024microstructureandmechanical pages 1-2). The conservative upper of 2.0 wt% avoids δ-phase formation and limits evaporation.

**Er:** Analogous to Sc as a grain refiner via Al₃Er; equilibrium solubility is very low. Master alloys show eutectic structure up to ~6 wt% Er, but AM alloys typically use ≤1 wt% Er for dispersoid control (andreyachshenko2025technologicalalloyingimpact pages 2-4). The conservative upper of 0.5 wt% is appropriate for minor additions.

**Zn:** Zn is volatile (evaporation temperature concerns) and contributes to hot cracking in mid-range Al-Zn-Mg compositions—peak susceptibility near Al-7Zn-1Mg (zhang2021predictionofcracking pages 9-12). However, Babu et al. successfully processed Al-18Zn-4Mg (babu2020laserpowderbed pages 1-2), and Jin demonstrated crack-free Al-20Zn-0.1Cr (charpagneUnknownyearfulllistofb pages 17-19). The conservative upper of 8 wt% stays below the most vulnerable 7xxx cracking zone when Mg is co-present; the non-conservative upper of 20 wt% reflects demonstrated LPBF capability.

**Sn:** Sn has very low equilibrium solubility in Al (~0.06–0.1 wt% depending on database) and forms a monotectic/immiscible liquid at higher concentrations (schmidfetzer2009thermodynamicaspectsof pages 2-4, drapala2017contributiontothe pages 3-5). Low-melting Sn-rich phases segregate to grain boundaries and promote hot tearing. Sn should be treated primarily as a trace element.

---

## 2. Reconciliation and Joint Constraints

### (a) Simplex Constraint Reconciliation

The sum of all non-conservative upper bounds (excluding Al) is: 8.0 (Mn) + 6.0 (Cr) + 2.0 (Zr) + 8.0 (Mg) + 14.0 (Si) + 7.0 (Cu) + 1.5 (Ti) + 2.0 (Fe) + 2.0 (Ni) + 12.0 (Ce) + 1.5 (Sc) + 3.0 (Li) + 1.5 (Er) + 20.0 (Zn) + 0.5 (Sn) = **89.0 wt%**. This vastly exceeds the available ~15–20 wt% budget (100 − Al_min). Even the sum of conservative upper bounds is 5.0 + 3.0 + 1.0 + 5.0 + 12.0 + 4.0 + 0.5 + 0.5 + 0.5 + 6.0 + 0.8 + 2.0 + 0.5 + 8.0 + 0.1 = **48.9 wt%**, which is also impossible to saturate simultaneously. This is by design in a high-dimensional search space: the per-element marginal bounds define the box constraints for the BOFN/GA inner solver, and the simplex constraint Σwt% = 100 (with Al as balance) is enforced separately. The acquisition function's inner optimizer must project candidate compositions onto the valid simplex. In practice, FLAIME targets ternary-through-~9-component subsystems, so at most 8 non-Al elements are active simultaneously, and typical total non-Al content is 5–15 wt%.

### (b) Recommended Element-Pair and Element-Group Joint Bounds

The following joint constraints should be imposed in addition to marginal per-element bounds, because joint failure modes are tighter than the product of individual bounds:

1. **Mn + Cr ≤ 7.0 wt% (conservative) / ≤ 10.0 wt% (non-conservative):** Mehta et al. demonstrated up to ~5.8 wt% total Mn+Cr in supersaturated solid solution by LPBF (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, mehta2022al–mn–cr–zrbasedalloystailored pages 2-2). Beyond ~7 wt% combined, precipitation of Al₆(Mn,Cr) or Al₇Cr becomes unavoidable even under rapid solidification.

2. **Sc + Zr ≤ 1.5 wt% (conservative) / ≤ 2.5 wt% (non-conservative):** Both elements compete for the same L1₂ Al₃(Sc,Zr) precipitate sublattice sites. Scalmalloy uses ~0.66Sc + 0.37Zr ≈ 1.0 wt% combined (babu2020laserpowderbed pages 1-2, he2021designanddevelopment pages 40-45). Excess Zr beyond the RS solubility limit (~0.6–0.7 wt%) precipitates as primary Al₃Zr during remelting (mehta2021highperformancealuminium pages 24-27).

3. **Cu + Mg ≤ 5.0 wt% (conservative) / ≤ 8.0 wt% (non-conservative):** The Al-Cu-Mg ternary shows maximum cracking susceptibility near Al-2Cu-1.5Mg (zhang2021predictionofcracking pages 5-7). High combined Cu+Mg broadens the freezing range synergistically and promotes S-phase (Al₂CuMg) formation at grain boundaries.

4. **Cu + Li ≤ 4.0 wt% (conservative) / ≤ 6.0 wt% (non-conservative):** In Al-Cu-Li systems, T₁ (Al₂CuLi) and T₂ (Al₆CuLi₃) phases compete; at high combined content, δ′-AlLi plus T₂ co-precipitation reduces ductility and processability (shao2024microstructureandmechanical pages 12-14, shao2024microstructureandmechanical pages 1-2). Li evaporation further complicates stoichiometric control.

5. **Mg + Si ≤ 6.0 wt% (conservative) / ≤ 10.0 wt% (non-conservative), with w(Mg)/w(Si) avoiding 1.5–2.0:** The Mg₂Si stoichiometric ratio w(Mg)/w(Si) ≈ 1.73 creates a particularly cracking-vulnerable composition corridor in the Al-Mg-Si ternary (zhang2021predictionofcracking pages 7-9). Compositions near this ratio with total Mg+Si > 2 wt% should be flagged for Scheil screening.

6. **Fe + Si (as impurity sum) ≤ 0.8 wt% when Fe > 0.3 wt%:** Fe and Si jointly form β-Al₅FeSi plate-like intermetallics that are highly detrimental to ductility (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3, andreyachshenko2025technologicalalloyingimpact pages 2-4). When Fe is intentionally elevated for dispersoid strengthening, Mn should be co-added (Mn/Fe ≥ 0.5) to promote the less harmful α-Al₁₅(Fe,Mn)₃Si₂ morphology.

7. **Sc + Er ≤ 1.2 wt% (conservative):** Er substitutes for Sc in Al₃(Sc,Er) L1₂ precipitates. Combined additions beyond ~1.2 wt% risk primary intermetallic formation and exceed the cost-performance optimum for grain refinement.

8. **Total volatile elements (Mg + Zn + Li) ≤ 10 wt% (conservative) / ≤ 15 wt% (non-conservative):** Mauduit et al. demonstrated that volatile elements cause melt-pool turbulence, spatter, filter clogging, and compositional drift during LPBF (mauduit2017studyofthe pages 19-20). A combined cap limits the aggregate evaporation burden on the LPBF process.

### (c) Recommended Default Al_min for the BOFN Search Space

We recommend **Al_min = 85 wt%** as the default lower bound for aluminum in the BOFN search space. This value:

- Ensures the alloy remains firmly in the Al-rich corner where TCAl10's assessed binary and ternary descriptions are reliable under Muggianu extrapolation (mehta2022al–mn–cr–zrbasedalloystailored pages 2-2).
- Guarantees good LPBF processability (sufficient thermal conductivity, appropriate laser absorption, manageable solidification shrinkage) (montanari2023additivemanufacturingof pages 17-19, hesselmann2022effectofprecipitationforming pages 1-3).
- Provides up to 15 wt% total alloying budget, which is sufficient to explore the anchor Al-Mn-Cr-Zr system (~6–7 wt% total solute) with headroom for additional elements (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3).
- Is consistent with the Al-Mn-Cr-Zr alloys developed by Mehta et al., which contain ~93–95 wt% Al (mehta2021highperformancealuminium pages 24-27, mehta2022al–mn–cr–zrbasedalloystailored pages 2-3), and with Scalmalloy at ~93–94 wt% Al (babu2020laserpowderbed pages 1-2, he2021designanddevelopment pages 40-45).

For non-conservative exploration (e.g., high-Ce eutectic or high-Zn systems), Al_min may be relaxed to **80 wt%**, but CALPHAD predictions should be validated against Scheil simulations with particular scrutiny for ternary and higher-order interactions at these composition extremes. The BOFN acquisition function should incorporate a soft penalty below 85 wt% Al to bias toward the well-assessed composition region while still permitting occasional exploratory evaluations at lower Al content.


References

1. (mehta2022al–mn–cr–zrbasedalloystailored pages 2-3): Bharat Mehta, Lars Nyborg, Karin Frisk, and Eduard Hryha. Al–mn–cr–zr-based alloys tailored for powder bed fusion-laser beam process: alloy design, printability, resulting microstructure and alloy properties. Journal of Materials Research, 37:1256-1268, Mar 2022. URL: https://doi.org/10.1557/s43578-022-00533-1, doi:10.1557/s43578-022-00533-1. This article has 20 citations and is from a peer-reviewed journal.

2. (aversa2019newaluminumalloys pages 8-10): Alberta Aversa, Giulio Marchese, Abdollah Saboori, Emilio Bassini, Diego Manfredi, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. New aluminum alloys specifically designed for laser powder bed fusion: a review. Materials, 12:1007, Mar 2019. URL: https://doi.org/10.3390/ma12071007, doi:10.3390/ma12071007. This article has 304 citations.

3. (mehta2022al–mn–cr–zrbasedalloystailored pages 2-2): Bharat Mehta, Lars Nyborg, Karin Frisk, and Eduard Hryha. Al–mn–cr–zr-based alloys tailored for powder bed fusion-laser beam process: alloy design, printability, resulting microstructure and alloy properties. Journal of Materials Research, 37:1256-1268, Mar 2022. URL: https://doi.org/10.1557/s43578-022-00533-1, doi:10.1557/s43578-022-00533-1. This article has 20 citations and is from a peer-reviewed journal.

4. (martucci2022theinfluenceof pages 1-2): Alessandra Martucci, Bharat Mehta, Mariangela Lombardi, and Lars Nyborg. The influence of processing parameters on the al-mn enriched nano-precipitates formation in a novel al-mn-cr-zr alloy tailored for power bed fusion-laser beam process. Metals, 12:1387, Aug 2022. URL: https://doi.org/10.3390/met12081387, doi:10.3390/met12081387. This article has 5 citations.

5. (andreyachshenko2025technologicalalloyingimpact pages 13-16): Violetta Andreyachshenko and Lenka Kunčická. Technological alloying impact on formation of phase composition of al-fe-si-x alloys. Materials, 18:2096, May 2025. URL: https://doi.org/10.3390/ma18092096, doi:10.3390/ma18092096. This article has 1 citations.

6. (mehta2021highperformancealuminium pages 24-27): B Mehta. High performance aluminium alloys for laser powder bed fusion: alloy design and development. Unknown journal, 2021.

7. (montanari2023additivemanufacturingof pages 17-19): Roberto Montanari, Alessandra Palombi, Maria Richetta, and Alessandra Varone. Additive manufacturing of aluminum alloys for aeronautic applications: advantages and problems. Metals, 13:716, Apr 2023. URL: https://doi.org/10.3390/met13040716, doi:10.3390/met13040716. This article has 70 citations.

8. (mauduit2017studyofthe pages 13-19): A Mauduit, S Pillot, and H Gransac. Study of the suitability of aluminum alloys for additive manufacturing by laser powder bed fusion. Unknown journal, 2017.

9. (mauduit2017studyofthe pages 19-20): A Mauduit, S Pillot, and H Gransac. Study of the suitability of aluminum alloys for additive manufacturing by laser powder bed fusion. Unknown journal, 2017.

10. (kou2015asimpleindex pages 11-12): S Kou. A simple index for predicting the susceptibility to solidification cracking. Unknown journal, 2015.

11. (hesselmann2022effectofprecipitationforming pages 1-3): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 24 citations and is from a highest quality peer-reviewed journal.

12. (babu2020laserpowderbed pages 1-2): A.P. Babu, S.K. Kairy, A. Huang, and N. Birbilis. Laser powder bed fusion of high solute al-zn-mg alloys: processing, characterisation and properties. Materials & Design, 196:109183, Nov 2020. URL: https://doi.org/10.1016/j.matdes.2020.109183, doi:10.1016/j.matdes.2020.109183. This article has 40 citations and is from a highest quality peer-reviewed journal.

13. (liu2024alloydesignfor pages 14-15): Zhuangzhuang Liu, Qihang Zhou, Xiaokang Liang, Xiebin Wang, Guichuan Li, Kim Vanmeensel, and Jianxin Xie. Alloy design for laser powder bed fusion additive manufacturing: a critical review. International Journal of Extreme Manufacturing, 6:022002, Jan 2024. URL: https://doi.org/10.1088/2631-7990/ad1657, doi:10.1088/2631-7990/ad1657. This article has 109 citations.

14. (hyer2021compositiondependentsolidificationcracking pages 2-3): Holden Hyer, Le Zhou, Abhishek Mehta, Sharon Park, Thinh Huynh, Shutao Song, Yuanli Bai, Kyu Cho, Brandon McWilliams, and Yongho Sohn. Composition-dependent solidification cracking of aluminum-silicon alloys during laser powder bed fusion. Acta Materialia, 208:116698, Apr 2021. URL: https://doi.org/10.1016/j.actamat.2021.116698, doi:10.1016/j.actamat.2021.116698. This article has 226 citations and is from a highest quality peer-reviewed journal.

15. (rohilla2024investigationofalcu20si10mg pages 22-25): K Rohilla. Investigation of alcu20si10mg alloy fabricated by laser powder bed fusion in additive manufacturing. Unknown journal, 2024.

16. (zhang2021predictionofcracking pages 5-7): Fan Zhang, Songmao Liang, Chuan Zhang, Shuanglin Chen, Duchao Lv, Weisheng Cao, and Sindo Kou. Prediction of cracking susceptibility of commercial aluminum alloys during solidification. Metals, 11:1479, Sep 2021. URL: https://doi.org/10.3390/met11091479, doi:10.3390/met11091479. This article has 25 citations.

17. (andreyachshenko2025technologicalalloyingimpact pages 2-4): Violetta Andreyachshenko and Lenka Kunčická. Technological alloying impact on formation of phase composition of al-fe-si-x alloys. Materials, 18:2096, May 2025. URL: https://doi.org/10.3390/ma18092096, doi:10.3390/ma18092096. This article has 1 citations.

18. (hesselmann2022effectofprecipitationforming pages 14-15): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 24 citations and is from a highest quality peer-reviewed journal.

19. (dixit2022laseradditivemanufacturing pages 15-16): Som Dixit and Shunyu Liu. Laser additive manufacturing of high-strength aluminum alloys: challenges and strategies. Journal of Manufacturing and Materials Processing, 6:156, Dec 2022. URL: https://doi.org/10.3390/jmmp6060156, doi:10.3390/jmmp6060156. This article has 68 citations.

20. (shao2024microstructureandmechanical pages 12-14): Shuobing Shao, Zhuoheng Liang, Peng Yin, Xinyuan Li, and Yongzhong Zhang. Microstructure and mechanical properties of al–li alloys with different li contents prepared by selective laser melting. Materials, 17:657, Jan 2024. URL: https://doi.org/10.3390/ma17030657, doi:10.3390/ma17030657. This article has 11 citations.

21. (shao2024microstructureandmechanical pages 1-2): Shuobing Shao, Zhuoheng Liang, Peng Yin, Xinyuan Li, and Yongzhong Zhang. Microstructure and mechanical properties of al–li alloys with different li contents prepared by selective laser melting. Materials, 17:657, Jan 2024. URL: https://doi.org/10.3390/ma17030657, doi:10.3390/ma17030657. This article has 11 citations.

22. (charpagneUnknownyearfulllistofb pages 17-19): MA Charpagne. Full list of abstracts. Unknown journal, Unknown year.

23. (zhang2021predictionofcracking pages 9-12): Fan Zhang, Songmao Liang, Chuan Zhang, Shuanglin Chen, Duchao Lv, Weisheng Cao, and Sindo Kou. Prediction of cracking susceptibility of commercial aluminum alloys during solidification. Metals, 11:1479, Sep 2021. URL: https://doi.org/10.3390/met11091479, doi:10.3390/met11091479. This article has 25 citations.

24. (schmidfetzer2009thermodynamicaspectsof pages 2-4): Rainer Schmid-Fetzer. Thermodynamic aspects of tin segregation during solidification of aluminium alloys. Materials Science Forum, 618-619:183-190, Apr 2009. URL: https://doi.org/10.4028/www.scientific.net/msf.618-619.183, doi:10.4028/www.scientific.net/msf.618-619.183. This article has 4 citations and is from a peer-reviewed journal.

25. (drapala2017contributiontothe pages 3-5): J. Drápala, G. Kostiuková, and M. Losertová. Contribution to the aluminum–tin–zinc ternary system. IOP Conference Series: Materials Science and Engineering, 266:012002, Nov 2017. URL: https://doi.org/10.1088/1757-899x/266/1/012002, doi:10.1088/1757-899x/266/1/012002. This article has 12 citations.

26. (kou2015asimpleindex pages 10-11): S Kou. A simple index for predicting the susceptibility to solidification cracking. Unknown journal, 2015.

27. (rohilla2024investigationofalcu20si10mg pages 25-27): K Rohilla. Investigation of alcu20si10mg alloy fabricated by laser powder bed fusion in additive manufacturing. Unknown journal, 2024.

28. (he2021designanddevelopment pages 40-45): Peidong He. Design and development of high strength aluminium materials for laser powder-bed fusion additive manufacturing. Dissertation, Jan 2021. URL: https://doi.org/10.26190/unsworks/22600, doi:10.26190/unsworks/22600. This article has 0 citations.

29. (zhang2021predictionofcracking pages 7-9): Fan Zhang, Songmao Liang, Chuan Zhang, Shuanglin Chen, Duchao Lv, Weisheng Cao, and Sindo Kou. Prediction of cracking susceptibility of commercial aluminum alloys during solidification. Metals, 11:1479, Sep 2021. URL: https://doi.org/10.3390/met11091479, doi:10.3390/met11091479. This article has 25 citations.

---

## Prompt

```
PROJECT CONTEXT — FLAIME (Fast Learning AI for Mineral Efficiency), DOE Genesis
Mission Phase I, Topic 3-B (AMMTO). The team is performing Bayesian Optimization
over Function Networks (BOFN/pKGFN) over a single joint search space:
(Al + 15 non-Al alloying elements) x atomization process x LPBF process.

The 15 non-Al element palette is:
  Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn.

Composition is parameterized as weight fractions that sum to 1.0; Al is the
matrix element. Down-selection is driven by CALPHAD (TCAl10 + AM Module),
Scheil solidification range, hot-cracking susceptibility, printability, and a
mineral-burden objective (USGS criticality / import reliance).

Anchor systems include Al-Mn-Cr-Zr and Al-Zr; the broader palette is intended
to enable AI-discovered sub-systems (ternary through ~9-component). All alloys
are Al-rich (Al typically >= 85 wt% for good LPBF processability and to remain
within the trustworthy region of TCAl10's binary/ternary Muggianu extrapolation).

We need element-by-element compositional BOUNDS (in weight percent, wt%) for
the BOFN / GA acquisition inner-solver search space.


TASK — JOINT BOUNDS TABLE
Provide a single consolidated table of compositional bounds (in wt%) for
the entire FLAIME 15-element palette plus Al, in one go:
    Al, Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn

For EACH of the 16 elements include:
  * conservative lower bound (wt%) — Al only; 0 for the rest unless you
    argue otherwise
  * non-conservative lower bound (wt%)
  * conservative upper bound (wt%)
  * non-conservative upper bound (wt%)
  * primary failure mode setting the upper bound
  * key citation(s)

Use a markdown table. Then below the table, in a paragraph:

  (a) Reconcile the per-element upper bounds with the simplex constraint
      sum(wt%) = 100 — i.e. flag any bounds that, if all were saturated
      simultaneously, would produce an impossible (>100 wt%) composition.
  (b) Recommend any element-pair or element-group bounds (e.g.
      Cu + Li, Mg + Si, Sc + Zr, Fe + Si impurity sum) that are tighter
      than the marginal per-element bounds because of joint-failure modes
      (hot cracking, brittle intermetallics, eutectic depression,
      printability limits).
  (c) Suggest a default Al_min for the BOFN search space.

Be quantitative, cite peer-reviewed AM Al alloy literature, and use the
TCAl10 assessed-binary/ternary coverage as a guardrail for the
"non-conservative" bounds.
```
