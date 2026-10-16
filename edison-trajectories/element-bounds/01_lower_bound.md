# Phase 1 — Lower-bound query (Al-rich constraint)

*Edison task: `d1e23d47-6ded-4f8e-a61d-50a158894d53`*

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


TASK — LOWER BOUND ANALYSIS
Aluminum is the matrix; the only element with a meaningful (nonzero) LOWER
bound is Al itself. All 15 non-Al elements technically have a lower bound of
0 wt% (they may be absent), with the simplex constraint
    Al_wt + sum_i(X_i_wt) = 1.0   for i in {Mn,Cr,Zr,Mg,Si,Cu,Ti,Fe,Ni,Ce,Sc,Li,Er,Zn,Sn}.

Please answer the following:

1. What is a defensible LOWER bound on the Al weight fraction (Al_min) for
   this BOFN search space, given that we want to remain (i) within the
   trustworthy region of TCAl10 and the AM Module, (ii) a meaningfully
   "Al alloy" by ASTM/wrought/AM convention, and (iii) reasonable for LPBF
   processability? Provide both a CONSERVATIVE Al_min (e.g. ~95 wt%) and a
   NON-CONSERVATIVE Al_min (e.g. as low as ~80–85 wt%) with justification.

2. Are there any non-Al elements that, when present, should themselves carry
   a nonzero LOWER bound — e.g. minimum Mg or Si if either is selected by
   the AI to ensure precipitation strengthening kicks in? Distinguish
   "global lower bound" (always > 0) from "conditional lower bound"
   (>0 only when the element is included).

3. How should the lower-bound Al_min interact with sparsity? FLAIME prefers
   k=3..8 active alloying elements per composition; what implications does
   this have for the per-element minimum nonzero concentration (e.g. a
   "detection / dosing floor" of ~0.05–0.1 wt% for ICP-MS / atomization
   crucible accuracy)?

Cite specific LPBF Al-alloy literature where possible. Express all numbers
in wt%.


## Objective
Define lower-bound rules for Al (matrix) and non-Al alloying elements (Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn) for a single simplex-constrained BOFN composition search space intended for CALPHAD (TCAl10 + AM Module), Scheil solidification, hot-cracking / printability screening, and LPBF processability.

## 1) Defensible lower bound on Al weight fraction (Al_min)

### Conservative Al_min (recommendation: **Al ≥ 95 wt%**)
A conservative lower bound of ~95 wt% Al (i.e., total alloying additions ≤5 wt%) is consistent with several LPBF-designed Al alloys in the literature where solute totals are single-digit wt% and Al is explicitly the balance element. Examples include Scalmalloy-like and other designed LPBF alloys reported as Al4.5Mg0.7Sc0.4Zr0.5Mn (Al ≈ 93.9 wt%) and Al-3.5Cu-1.5Mg-1Si (Al ≈ 94.0 wt%), which are already near this boundary and remain clearly Al-rich while leveraging grain-refining and precipitation-strengthening concepts (Sc/Zr, Mg, Mn, Si) used to improve LPBF performance. (aversa2019newaluminumalloys pages 8-10, aversa2019newaluminumalloys pages 12-14)

From a “meaningful Al alloy” convention standpoint, wrought Al alloys are categorized by the major alloying element system (2xxx, 3xxx, 6xxx, 7xxx, etc.) but still treat Al as the base metal; even the “commercially pure” 1xxx series is defined as ≥99.0% Al, illustrating that Al-alloy naming presumes Al as the dominant constituent. (kundig2006mechanicalengineershandbook pages 73-75)

In LPBF-specific terms, the conservative Al_min is also a pragmatic way to stay near binary/ternary-dominated regions (relevant to extrapolation-based thermodynamic assessments) while still permitting microalloying strategies (e.g., Sc/Zr) that are widely used to improve grain refinement and mitigate cracking. (aversa2019newaluminumalloys pages 8-10)

**Interpretation for BOFN:** Al_min = 95 wt% is appropriate when the program wants (i) maximal CALPHAD credibility under Muggianu extrapolation, (ii) strong “Al alloy” identity, and (iii) a bias toward microalloying / low-solute printable designs.

### Non-conservative Al_min (recommendation: **Al ≥ 85 wt%**)
A non-conservative lower bound of ~85 wt% Al (total solute up to 15 wt%) is defensible if the intent is to include the main LPBF-printable Al families and known “printability rescue” strategies that rely on larger solute contents:

* **Near-eutectic Al–Si(-Mg)**: Al–Si alloys used in LPBF commonly sit near the eutectic (≈12 wt% Si), and a commonly cited processed range is ~9–13 wt% Si. This corresponds to Al ≈ 87–91 wt% before considering Mg and other minor elements, i.e., well below 95 wt% Al but still clearly Al-balance. (brock2020laserpowderbed pages 28-32, aversa2019newaluminumalloys pages 1-3)
* **High-solute Al–Zn–Mg**: an LPBF-designed alloy Al-14Zn-3Mg has Al ≈ 83 wt% nominally; measured powder chemistry in one study was Zn 14.7 wt%, Mg 3.34 wt% with balance Al (Al ≈ 81.9 wt%), and the built part showed substantial Zn/Mg loss (Zn 10.9 wt%, Mg 2.79 wt%, balance Al). This demonstrates both that (a) Al can drop into the low-80s in credible LPBF Al-balance research alloys, and (b) volatile solute loss motivates avoiding ultra-trace “on” additions when elements are meant to matter. (babu2021onthecorrosion pages 1-2)
* **Al-balance cast alloy conventions**: in an example mass-balance formulation for cast alloy A360.0, the computed Al fraction is ~84.78 wt%, yet it is still treated as an aluminum alloy with Al as the balance element in the standard-style composition listing. (hussain2007recyclingandformulation pages 2-4)

**Interpretation for BOFN:** Al_min = 85 wt% is appropriate when the program wants to explore LPBF-printable, solute-rich composition regimes (especially Al–Si and Al–Zn–Mg families), accepting higher hot-cracking risk in some systems but enabling compositional fixes (e.g., Si additions to 7xxx) and richer strengthening strategies.

## 2) Should any non-Al elements have nonzero lower bounds?

### Global lower bound (always >0): **No**
No non-Al element should carry a strictly positive *global* lower bound in your stated discovery setting, because different printable Al alloy families rely on different principal solutes. Forcing, e.g., Mg or Si to always be present would exclude legitimate families (e.g., Mn/Cr/Zr-based designs) and undermine the AI’s ability to discover new subsystems. LPBF literature explicitly spans multiple distinct composition strategies: near-eutectic Al–Si (printable by design), Sc/Zr-modified Al–Mg systems (grain refinement/precipitation), Mn-containing systems, and high-solute Al–Zn–Mg systems. (aversa2019newaluminumalloys pages 8-10, aversa2019newaluminumalloys pages 1-3, babu2021onthecorrosion pages 1-2, zhai2022crackingbehaviormicrostructure pages 2-3)

### Conditional lower bounds (only when an element is “active”): **Yes, for functional intent**
Conditional floors are defensible when an element is selected for a specific metallurgical role and you want to prevent the optimizer from using effectively-zero “token” additions.

* **Si (crack-mitigation via eutectic / narrowing solidification range)**: A Si-modified 7075 strategy used ~3.74 wt% Si in crack-susceptibility modeling and experimentally used a 4 wt% Si + 96 wt% Al7075 powder mix to “successfully prevent” solidification cracks. This supports a conditional floor of **Si ≥ ~3–4 wt%** when Si is intended as a true solidification-range/fluidity modifier in 7xxx-like alloys (not just a trace addition). (li2021investigationofsolidification pages 1-2)
* **Sc + Zr (grain refinement and Al3(Sc,Zr)/Al3Zr nucleation + precipitation)**: Representative printable compositions in the LPBF literature include Scalmalloy-like Al4.5Mg0.7Sc0.4Zr0.5Mn and Mn/Mg/Sc/Zr alloys such as Al-5.22Mn-1.16Mg-0.81Sc-0.46Zr, supporting that Sc and Zr are typically used at ~0.4–0.8 wt% levels when they are “doing work.” A defensible conditional floor for an “active” Sc or Zr intended for nucleation/precipitation is **≥0.2 wt%** (microalloying but non-trace). (aversa2019newaluminumalloys pages 8-10, zhai2022crackingbehaviormicrostructure pages 2-3)
* **Mn / Mg (when intended as principal strengthening additions)**: Mn appears as a principal solute at multi-wt% levels in printable LPBF compositions (e.g., 5.22 wt% Mn in an Al-Mn-Mg-Sc-Zr alloy), and Mg appears from ~0.7 wt% (Scalmalloy-like) to >1 wt% (Al-5.22Mn-1.16Mg-0.81Sc-0.46Zr). Thus, if Mn or Mg is selected as an “active” principal addition (not a trace impurity), a conditional floor around **0.5–1 wt%** is defensible. (aversa2019newaluminumalloys pages 8-10, zhai2022crackingbehaviormicrostructure pages 2-3)

For other palette elements (Cr, Cu, Ti, Fe, Ni, Ce, Li, Er, Zn, Sn): the retrieved LPBF evidence set supports their use in certain systems but does not provide robust, universal “minimum effective wt%” thresholds. A general conditional activity floor (Section 3) is therefore more defensible than element-specific minima for these, unless you impose additional mechanism-specific constraints.

## 3) Interaction of Al_min with sparsity (k = 3..8 active elements) and dosing/measurement floors

### Recommended two-level lower-bound scheme
1. **Global bounds:** keep all 15 non-Al elements at **0 wt% lower bound** (true absence allowed). 
2. **Activation floor (conditional):** when an element is chosen as “active,” enforce a small nonzero lower bound (a dosing/measurement floor) such as **0.05–0.10 wt%**.

This prevents the GA/acquisition inner solver from populating many “nominally active” elements with concentrations so small they are (i) experimentally irreproducible, (ii) potentially lost to volatilization/oxidation or powder segregation, or (iii) immaterial to CALPHAD/Scheil/hot-cracking metrics. The need to avoid relying on tiny additions is reinforced by direct evidence that volatile solutes (Zn, Mg) can measurably decrease during LPBF in high-solute Al–Zn–Mg alloys (composition drift). (babu2021onthecorrosion pages 1-2)

### Feasibility implications with Al_min
* With **conservative Al_min = 95 wt%**, the solute budget is 5 wt%. At **k = 8** and a **0.10 wt% activation floor**, the minimum solute mass tied up in “being on” is only 0.8 wt%, leaving 4.2 wt% to allocate meaningfully. However, mechanism-driven conditional floors like **Si ≥ 4 wt%** (for eutectic crack mitigation in 7xxx-like alloys) can consume most of the solute budget alone, forcing the optimizer toward either (a) fewer active elements, or (b) microalloying strategies (Sc/Zr) plus one major solute. This is a feature if you want CALPHAD trust-region conservatism and sparse interpretability.
* With **non-conservative Al_min = 85 wt%**, the solute budget is 15 wt%, which readily supports k = 3..8 with both an activation floor and one or more functional floors. This is the regime needed to cover common printable Al–Si alloys (9–13 wt% Si) and high-solute Al–Zn–Mg examples, while retaining enough degrees of freedom for multi-element discovery. (brock2020laserpowderbed pages 28-32, babu2021onthecorrosion pages 1-2)

## Implementable lower-bound rules (summary)
The following artifact encodes recommended global and conditional lower-bound rules in wt%.

| Rule type | Variable / element(s) | Recommended lower bound (wt%) | When it applies | Brief justification |
|---|---|---:|---|---|
| Matrix bound | Al (conservative) | 95.0 | Conservative BOFN search | Keeps total solute ≤ 5 wt%; strongly Al-rich and close to most LPBF-designed Al alloy compositions |
| Matrix bound | Al (non-conservative) | 85.0 | Exploratory BOFN search | Allows total solute ≤ 15 wt%; still clearly Al-balance and overlaps printable Al-Si / high-solute Al-rich LPBF space |
| Global bound | Mn, Cr, Zr, Mg, Si, Cu, Ti, Fe, Ni, Ce, Sc, Li, Er, Zn, Sn | 0.0 | Always | Any non-Al element may be absent; sparsity should be handled separately from chemistry identity |
| Conditional activity floor | Any selected non-Al element | 0.05 | If merely “on” in the search space | Practical analytical / dosing floor; avoids vanishingly small pseudo-active concentrations |
| Conditional activity floor | Any selected non-Al element | 0.10 | Preferred robust floor | Better for powder blending / melt reproducibility and cleaner sparsity enforcement |
| Functional floor | Si | 3.0 | If selected specifically for eutectic-based crack mitigation / 7xxx-style printability rescue | Below this, Si may act more like a trace tweak than a true solidification-range / fluidity modifier |
| Functional floor | Si | 4.0 | Stronger crack-mitigation setting | Mirrors Si-modified 7075 studies using about 3.7–4 wt% Si to suppress cracking |
| Functional floor | Sc | 0.20 | If selected for Al3(Sc,Zr)-based nucleation / precipitation role | Below this, benefits may be inconsistent relative to cost and uncertainty |
| Functional floor | Zr | 0.20 | If selected for Al3Zr / Al3(Sc,Zr)-based grain refinement role | Ensures Zr is more than a trace residual and can contribute to nucleant formation |
| Functional floor | Sc + Zr pair | 0.20 each | If Sc and Zr are co-selected for coupled grain-refinement strategy | Reflects common LPBF Al-Mg-Sc-Zr / Al-Mn-Mg-Sc-Zr design logic |
| Functional floor | Mn | 0.50 | If using Al-Mn-Cr-Zr or Al-Mn-Mg-Sc-Zr anchor logic | Keeps Mn in a regime where it can materially affect solidification / strengthening rather than acting as a trace impurity |
| Functional floor | Mn | 1.00 | Preferred anchor-setting floor | Better aligns with Mn-bearing LPBF anchor alloys where Mn is a principal alloying addition |
| Functional floor | Mg | 0.50 | If using Mg for Al-Mg-based solid-solution / precipitation support | Below this, Mg may be too small to reliably change strengthening response |
| Functional floor | Mg | 1.00 | Preferred anchor-setting floor | More consistent with Mg as a principal strengthening addition in LPBF Al-Mg(-Sc-Zr) alloys |
| Sparsity interaction | Any active non-Al set, k = 3–8 | Sum of active-floor minima must fit within 100 − Al_min | Always | Check feasibility: e.g., with Al_min = 95 and k = 8, a 0.10 wt% floor consumes only 0.8 wt%; functional floors consume much more and should be applied selectively |
| Implementation note | Conditional floors vs global bounds | Use floors only after element selection / activation | Solver design choice | Avoids forcing every composition to contain Mg, Si, Sc, etc.; preserves discovery of ternaries through multicomponent sub-systems |


*Table: Concise lower-bound rules for the FLAIME BOFN search space, including conservative and exploratory Al minima, zero global lower bounds for all non-Al elements, and practical conditional nonzero floors when elements are active. The recommendations are grounded in LPBF Al-alloy literature on printable Al-rich composition ranges, Si-enabled crack mitigation, and Sc/Zr/Mn/Mg functional alloying roles (aversa2019newaluminumalloys pages 8-10, brock2020laserpowderbed pages 28-32, babu2021onthecorrosion pages 1-2, li2021investigationofsolidification pages 1-2, zhai2022crackingbehaviormicrostructure pages 2-3, aversa2019newaluminumalloys pages 12-14, kundig2006mechanicalengineershandbook pages 73-75, hussain2007recyclingandformulation pages 2-4, sharma2022advancementsinthe pages 31-32).*

## Visual evidence (example of LPBF Al-alloy property comparisons)
The Aversa review includes a table comparing properties across multiple modified Al alloys in LPBF, illustrating the diversity of composition strategies and the importance of alloy modification/heat treatment in achieving usable strength/ductility. (aversa2019newaluminumalloys media 1b02bf76)


References

1. (aversa2019newaluminumalloys pages 8-10): Alberta Aversa, Giulio Marchese, Abdollah Saboori, Emilio Bassini, Diego Manfredi, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. New aluminum alloys specifically designed for laser powder bed fusion: a review. Materials, 12:1007, Mar 2019. URL: https://doi.org/10.3390/ma12071007, doi:10.3390/ma12071007. This article has 304 citations.

2. (aversa2019newaluminumalloys pages 12-14): Alberta Aversa, Giulio Marchese, Abdollah Saboori, Emilio Bassini, Diego Manfredi, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. New aluminum alloys specifically designed for laser powder bed fusion: a review. Materials, 12:1007, Mar 2019. URL: https://doi.org/10.3390/ma12071007, doi:10.3390/ma12071007. This article has 304 citations.

3. (kundig2006mechanicalengineershandbook pages 73-75): JG Kaufman. Mechanical engineers' handbook: materials and mechanical design. ArXiv, Feb 2006. URL: https://doi.org/10.1002/0471777447, doi:10.1002/0471777447. This article has 33 citations.

4. (brock2020laserpowderbed pages 28-32): L Brock. Laser powder bed fusion of alsi10mg for fabrication of fluid power components. Unknown journal, 2020.

5. (aversa2019newaluminumalloys pages 1-3): Alberta Aversa, Giulio Marchese, Abdollah Saboori, Emilio Bassini, Diego Manfredi, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. New aluminum alloys specifically designed for laser powder bed fusion: a review. Materials, 12:1007, Mar 2019. URL: https://doi.org/10.3390/ma12071007, doi:10.3390/ma12071007. This article has 304 citations.

6. (babu2021onthecorrosion pages 1-2): A.P. Babu, S. Choudhary, J.C. Griffith, A. Huang, and N. Birbilis. On the corrosion of a high solute al-zn-mg alloy produced by laser powder bed fusion. Corrosion Science, 189:109626, Aug 2021. URL: https://doi.org/10.1016/j.corsci.2021.109626, doi:10.1016/j.corsci.2021.109626. This article has 69 citations and is from a highest quality peer-reviewed journal.

7. (hussain2007recyclingandformulation pages 2-4): Luay B. Hussain and Issa A. Ali Hakim. Recycling and formulation of aluminum scrap via mass balance die casting and forming. Materials and Manufacturing Processes, 22:916-921, Sep 2007. URL: https://doi.org/10.1080/10426910701451796, doi:10.1080/10426910701451796. This article has 16 citations and is from a peer-reviewed journal.

8. (zhai2022crackingbehaviormicrostructure pages 2-3): Ziyu Zhai, Wei Pan, B. Liang, Yantao Liu, and Yong-zhong Zhang. Cracking behavior, microstructure and properties of selective laser melted al-mn-mg-sc-zr alloy. Crystals, 12:565, Apr 2022. URL: https://doi.org/10.3390/cryst12040565, doi:10.3390/cryst12040565. This article has 15 citations.

9. (li2021investigationofsolidification pages 1-2): Guichuan Li, Suraj Dinkar Jadhav, Arturo Martín, Maria L. Montero-Sistiaga, Jeroen Soete, Maria San Sebastian, Carmen M. Cepeda-Jiménez, and Kim Vanmeensel. Investigation of solidification and precipitation behavior of si-modified 7075 aluminum alloy fabricated by laser-based powder bed fusion. Metallurgical and Materials Transactions A, 52:194-210, Nov 2021. URL: https://doi.org/10.1007/s11661-020-06073-9, doi:10.1007/s11661-020-06073-9. This article has 77 citations.

10. (sharma2022advancementsinthe pages 31-32): Sachin Kumar Sharma, Harpreet Singh Grewal, Kuldeep Kumar Saxena, Kahtan A. Mohammed, Chander Prakash, J. Paulo Davim, Dharam Buddhi, Ramesh Raju, Dhanesh G. Mohan, and Jacek Tomków. Advancements in the additive manufacturing of magnesium and aluminum alloys through laser-based approach. Materials, 15:8122, Nov 2022. URL: https://doi.org/10.3390/ma15228122, doi:10.3390/ma15228122. This article has 37 citations.

11. (aversa2019newaluminumalloys media 1b02bf76): Alberta Aversa, Giulio Marchese, Abdollah Saboori, Emilio Bassini, Diego Manfredi, Sara Biamino, Daniele Ugues, Paolo Fino, and Mariangela Lombardi. New aluminum alloys specifically designed for laser powder bed fusion: a review. Materials, 12:1007, Mar 2019. URL: https://doi.org/10.3390/ma12071007, doi:10.3390/ma12071007. This article has 304 citations.

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


TASK — LOWER BOUND ANALYSIS
Aluminum is the matrix; the only element with a meaningful (nonzero) LOWER
bound is Al itself. All 15 non-Al elements technically have a lower bound of
0 wt% (they may be absent), with the simplex constraint
    Al_wt + sum_i(X_i_wt) = 1.0   for i in {Mn,Cr,Zr,Mg,Si,Cu,Ti,Fe,Ni,Ce,Sc,Li,Er,Zn,Sn}.

Please answer the following:

1. What is a defensible LOWER bound on the Al weight fraction (Al_min) for
   this BOFN search space, given that we want to remain (i) within the
   trustworthy region of TCAl10 and the AM Module, (ii) a meaningfully
   "Al alloy" by ASTM/wrought/AM convention, and (iii) reasonable for LPBF
   processability? Provide both a CONSERVATIVE Al_min (e.g. ~95 wt%) and a
   NON-CONSERVATIVE Al_min (e.g. as low as ~80–85 wt%) with justification.

2. Are there any non-Al elements that, when present, should themselves carry
   a nonzero LOWER bound — e.g. minimum Mg or Si if either is selected by
   the AI to ensure precipitation strengthening kicks in? Distinguish
   "global lower bound" (always > 0) from "conditional lower bound"
   (>0 only when the element is included).

3. How should the lower-bound Al_min interact with sparsity? FLAIME prefers
   k=3..8 active alloying elements per composition; what implications does
   this have for the per-element minimum nonzero concentration (e.g. a
   "detection / dosing floor" of ~0.05–0.1 wt% for ICP-MS / atomization
   crucible accuracy)?

Cite specific LPBF Al-alloy literature where possible. Express all numbers
in wt%.
```
