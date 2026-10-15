# Phase 3 — Multi-element constraints & edge cases (Edison ANALYSIS)

*Edison task: `15a4edab-7189-4438-bf42-01d554487dbb`*

## Answer

# Multi-Element Constraints & Edge Cases

Based on the provided per-element and joint-synthesis compositional bounding data, as well as standard Al-alloy and LPBF literature principles, the BOFN/pKGFN search space should enforce the following constraints, penalties, and edge-case guards to ensure physically realizable, processable, and safe alloys.

### 1. SIMPLEX & SPARSITY
* **Simplex constraint (Required):** The sum of all active weight fractions must strictly equal 1.0 (Al + Mn + Cr + Zr + Mg + Si + Cu + Ti + Fe + Ni + Ce + Sc + Li + Er + Zn + Sn = 1.0).
* **Sparsity Prior (k = 3..8):** This should be enforced as a **hard constraint** on the BOFN / GA inner-solver state space to constrain the high-dimensional volume and force the optimizer to allocate meaningful multi-element doses. Alloys with >8 non-Al elements quickly lose TCAl10 trustworthiness and risk unmanageable multi-phase complexity.
* **Dosing Floor:** Any element selected by the optimizer (non-zero state) must respect a practical activity floor of **0.05–0.10 wt%** to exceed AMAZEMET rePOWDER induction crucible dosing error margins and avoid wasting search-space volume on pseudo-active trace additions.

### 2. SUM CONSTRAINTS
These bounding inequalities capture critical joint-failure modes (e.g., synergistic hot cracking, wide freezing ranges, and coupled intermetallic precipitation) that are stricter than their constituent single-element limits.

* **Total non-Al solute (1 - Al):** `sum(all 15 non-Al elements) <= 15.0 wt%`
  * *Rationale:* Ensures Al ≥ 85 wt% to maintain reliable LPBF thermal conductivity and keep the composition within the trustworthy region of TCAl10's Muggianu extrapolation.
* **Cu + Li:** `sum(Cu, Li) <= 4.0 wt%` (conservative)
  * *Rationale:* Co-alloying these elements promotes T₁ (Al₂CuLi) and T₂ (Al₆CuLi₃) phases. High combined fractions risk δ′-AlLi plus T₂ co-precipitation, reducing ductility while increasing volatile Li losses (~15% loss) and hot-cracking susceptibility.
* **Mg + Si:** `sum(Mg, Si) <= 6.0 wt%` (conservative)
  * *Rationale:* Controls the Mg₂Si precipitation balance. Furthermore, compositions at or near the stoichiometric weight ratio w(Mg)/w(Si) ≈ 1.73 with total Mg+Si > 2 wt% represent a highly crack-vulnerable corridor and should be flagged for targeted Scheil screening.
* **Mg + Zn + Li (Volatiles cap):** `sum(Mg, Zn, Li) <= 10.0 wt%` (conservative)
  * *Rationale:* All three elements suffer high vapor pressure under LPBF laser exposure. Exceeding ~10 wt% combined drives severe keyhole destabilization, spatter, filter clogging, and unpredictable nominal-vs-retained composition drift.
* **Sc + Zr:** `sum(Sc, Zr) <= 1.5 wt%` (conservative)
  * *Rationale:* Both compete for the L1₂ Al₃(M) sublattice. Exceeding this combined limit risks wasting critical solute on coarse, embrittling primary trialuminides during remelting cycles rather than fine nano-precipitates.
* **Fe + Si:** `sum(Fe, Si) <= 0.8 wt%` when Fe > 0.3 wt%
  * *Rationale:* Controls the coupled formation of plate-like, embrittling β-Al₅FeSi phases. If Fe is used intentionally for strength, Mn should be co-added to promote more equiaxed α-Al₁₅(Fe,Mn)₃Si₂ instead.
* **Mn + Cr:** `sum(Mn, Cr) <= 7.0 wt%` (conservative)
  * *Rationale:* Exceeding this combined supersaturation limit results in the unavoidable formation of coarse Al₆(Mn,Cr) or Al₇Cr primary intermetallics, even under LPBF rapid solidification.
* **Ce + Mn (Edge Case Caution):** `sum(Ce, Mn) <= 6.0 wt%` (soft constraint)
  * *Rationale:* While established literature separately explores near-eutectic Al-Ce and Al-Mn-Sc-Zr systems, high co-additions of both Ce and Mn lack broad LPBF characterization and risk competing primary-phase network formations.

### 3. RATIO / STOICHIOMETRY CONSTRAINTS
* **Sc:Zr Weight Ratio:** Enforce or bias toward a near **1:1 to 1:1.5 Sc:Zr weight ratio** (equivalently, approximately **0.45:1 to 0.67:1 on an atomic basis**).
  * *Guidance:* Literature on optimal L1₂ precipitation (e.g., Scalmalloy uses ~0.66 wt% Sc / 0.42 wt% Zr) indicates Zr should be maintained at a sufficient level relative to Sc to form thermally stable core-shell Al₃(Sc,Zr) and prevent over-reliance on Sc.
* **Mg:Si Ratio:** Avoid **1.5 to 2.0 (w/w)** when Mg+Si > 2 wt%.
  * *Guidance:* The w(Mg)/w(Si) ≈ 1.73 ratio (matching the ~2:1 atomic stoichiometry of Mg₂Si) creates a particularly crack-vulnerable composition corridor in ternary Al-Mg-Si systems.
* **Cu:Mg Ratio:** Avoid regions near **Cu:Mg ≈ 1.33 (w/w)** (e.g., ~2 wt% Cu + 1.5 wt% Mg).
  * *Guidance:* This specific ratio corresponds to the maximum cracking susceptibility peak driven by S-phase (Al₂CuMg) formation and freezing range expansion. Ratios >4.0 favor θ′-Al₂Cu and are preferred for 2xxx-style high-strength designs.

### 4. TCAl10 COVERAGE GUARDRAILS
* **Muggianu-Extrapolation Penalties:** The TCAl10 database is built on assessed binaries and ternaries. Pushing >4 heavy-alloying elements near their individual upper bounds relies entirely on mathematical extrapolation.
* **Unassessed Ternaries:** Pairs involving **Sn, Er, Li, and high Ce** often lack fully assessed ternaries in typical CALPHAD databases when interacting with complex transitions like Mn/Cr.
  * *Guardrail:* Enforce a **multicomponent activity cap**: if `k > 5`, tighten the non-Al solute limit `sum(solutes) <= 10.0 wt%` to prevent the solver from exploiting spurious mathematical minima in unassessed 6- or 7-component thermodynamic spaces.

### 5. ATOMIZATION / OXIDATION EDGE CASES
* **Ce & Sc Oxidation:** Elemental Ce blending forms AlCeO₃ oxide films that kill melt-pool wettability, cause balling, and drive massive porosity. Sc and Er carry similar but milder oxide-skin risks.
* **Volatiles (Li, Mg, Zn):** Evaporation of Li (up to ~15% loss) and Mg causes severe process porosity ("vapor holes") and chamber fuming. Compositions relying heavily on these must be atomized and printed with strict atmospheric control (O₂, H₂O < 100 ppm).
* **Ti & Zr Losses to Primaries:** High Ti (>1.5 wt%) or Zr (>1.0 wt%) risks premature precipitation of coarse Al₃Ti / Al₃Zr peritectic phases in the induction crucible or nozzle, stripping the melt of required inoculants and causing atomization nozzle clogging.

### 6. PRINTABILITY EDGE CASES
* **Freezing Range Cutoff:** Compositions with an explicitly wide Scheil solidification range (e.g., **ΔT_f > 100–120 K**) should be heavily penalized or discarded, particularly in 7xxx-like spaces (Al-Zn-Mg) or high-Li systems where prolonged liquid-film coexistence guarantees hot tearing.
* **Mineral-Burden Penalty:** Heavy/critical elements (**Sc, Er, Ce**) must incur a sharply increasing scalar penalty in the BOFN acquisition function as they approach their upper bounds. Sourcing high-purity pre-alloyed feedstocks for these elements degrades the project's mineral-efficiency objective.

### 7. RECOMMENDATIONS
1. **Enforce Sparsity as a Hard Constraint:** Modify the GA state space generator so it only proposes candidates with `k=3` to `k=8` active non-Al elements, strictly adhering to `Al >= 85 wt%`.
2. **Apply Soft Penalties for Volatiles:** Do not hard-ban `Mg+Zn+Li > 10 wt%`, but apply a steep continuous penalty to the pKGFN acquisition function for volatile totals above 8 wt% to reflect expected composition drift and atomization difficulty.
3. **Scheil Screening Gate:** Implement a strict Scheil freezing-range constraint (ΔT_f) evaluated immediately post-CALPHAD. Any composition with a highly expanded freezing range or near a known cracking ratio (Cu:Mg ~1.33, Mg:Si ~1.73) must be discarded prior to experimental selection.
4. **Sc/Zr Ratio Bounds:** Lock the GA search bounds such that if `Sc > 0.1 wt%`, then `Zr` must be `>= 0.5 * Sc` (w/w) to ensure cost-effective L1₂ core-shell precipitation rather than wasting pure Sc.
5. **Treat Sn as an Excluded Impurity:** Set the hard upper bound for Sn to `0.1 wt%`. The risk of monotectic immiscibility, low-melting intergranular films (~232 °C), and lack of established LPBF viability make it a dead-end for a general Al-rich search space.

*Discretionary Analytical Decisions:*
- *Cu:Mg S-phase avoidance ratio was extrapolated from joint-synthesis literature highlighting the cracking peak at Al-2Cu-1.5Mg.*
- *Mg:Si ratio avoidance bounds were established strictly by weight fractions (1.5-2.0 w/w) rather than atomic percent to match BOFN inner-solver weight-percent parameterization.*
- *Multicomponent activity cap (k>5 restricting max solute to 10 wt%) was introduced as a functional heuristic to guard against TCAl10 unassessed ternary extrapolation.*
- *ΔT_f > 100–120 K was specified as a nominal heuristic cutoff for Scheil freezing range, standard for crack-susceptible Al LPBF analysis, as exact numerical cutoffs were absent in the text.*
- *Sc:Zr co-dependency (Zr >= 0.5 Sc) was formulated as a linear inequality to simplify integration into standard Bayesian Optimization acquisition constraints.*

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


TASK — SPECIAL MULTI-ELEMENT CONSTRAINTS AND EDGE CASES

Attached are: (a) the 16 per-element bound trajectories, (b) the Al
lower-bound trajectory, (c) the joint simultaneous-bounds trajectory, and
(d) the finalized bounds table you previously synthesized.

The marginal (per-element) bounds are not enough for a safe BOFN search
space. We also need MULTI-ELEMENT constraints — sums or ratios of specific
element subsets that must stay within a bound — and edge cases that the
GA / pKGFN inner solver should respect.

Please produce a markdown section titled "Multi-Element Constraints &
Edge Cases" with at least the following content, drawing only on the
attached trajectories and on standard Al-alloy / LPBF literature:

1. SIMPLEX & SPARSITY
   * Required: sum of all weight fractions = 1 (Al + 15 = 1).
   * Sparsity prior: k = 3..8 nonzero non-Al elements per composition;
     state how this should be enforced (hard or soft constraint).
   * Dosing floor for any included element (wt%).

2. SUM CONSTRAINTS — list each as
       sum(subset) <= X wt%   (or >=, or a band)
   covering at minimum:
     * Total non-Al solute (1 - Al)
     * Cu + Li (Al-Cu-Li hot-cracking + density / ductility)
     * Mg + Si (Mg2Si precipitation balance, beta-prime)
     * Mg + Zn (+ Cu) for 7xxx-style hot tearing
     * Sc + Zr (L1_2 dispersoid forming pair; near-stoichiometric ratio)
     * Fe + Si (residual / impurity sum that controls beta-AlFeSi)
     * Ce + Mn (eutectic / dispersoid co-additions reported in AM Al-Ce
       and Al-Mn-Sc-Zr literature)
     * Any other group your synthesis identifies

3. RATIO / STOICHIOMETRY CONSTRAINTS
   * Sc:Zr atomic-ratio guidance for Al3(Sc,Zr) L1_2.
   * Mg:Si atomic-ratio for Mg2Si.
   * Cu:Mg ratio for S-phase / theta'.

4. TCAl10 COVERAGE GUARDRAILS
   * Element pairs with NO assessed Al-X-Y ternary should have tighter
     marginal bounds when both are simultaneously > some threshold.
   * State explicitly which pairs from the 15-element palette are
     "Muggianu-extrapolation only" and recommend a joint-cap.

5. ATOMIZATION / OXIDATION EDGE CASES
   * Elements that are problematic for ultrasonic atomization in an Al
     induction crucible (Li, Mg high-vapor pressure; Ce/Sc/Er high cost
     and oxide-skin issues; Ti losses to Al3Ti primaries; Zr losses to
     Al3Zr primaries above the peritectic).

6. PRINTABILITY EDGE CASES
   * Compositions with predicted freezing range > some threshold should
     be discarded or flagged.
   * Compositions where the conservative upper bound on a heavy critical
     element (Sc, Er, Ce) is exceeded should incur a mineral-burden
     penalty as well as a printability one.

7. RECOMMENDATIONS
   * 3-5 specific actionable changes to the BOFN search-space definition.
   * Any constraints that should be implemented as PENALTIES in the
     pKGFN acquisition rather than as hard bounds.

Be concise, quantitative, and cite where possible.
```
