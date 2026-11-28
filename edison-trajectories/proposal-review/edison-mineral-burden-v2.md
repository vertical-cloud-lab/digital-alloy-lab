The clean fix is: **keep the Scalmalloy comparison, but explicitly redefine CMDRI so Sc is no longer a one-element cheat code**. Right now the proposal is internally ambiguous. On p.5 it gives a linear form, `MBS = Σ w_i x_i`, but says the weights incorporate USGS net import reliance, Graedel, Helbig, and ESSENZ factors. That matters a lot. If the implemented weight includes any linear price term, the prior reviewer is right: the current `>=40% vs Scalmalloy` target is basically free for any Sc-free alloy. Using a reasonable reconstruction `CMDRI ≈ Σ (NIR_i × cost_i × wt_i)`, Scalmalloy (taken as Al-4.5Mg-0.7Sc-0.3Zr with minor Mn/Ti/Fe) has an approximate score of **$35.23/kg-alloy-risk**, of which **Sc contributes $35.00/kg, or 99.3%**. Under that formulation, **AlSi10Mg** is about **$0.14/kg** and an **Al-3Mn-1Cr-1Zr** alloy is about **$0.56/kg**, which correspond to **99.6%** and **98.4%** reductions versus Scalmalloy. So yes: under any cost-inclusive linear formulation, the **40% threshold is trivially satisfied**. By contrast, if the score were pure USGS net-import-reliance only, `Σ (NIR_i × wt_i)`, the critique would be false: Scalmalloy scores about **3.84**, while AlSi10Mg is **4.36** and Al-3Mn-1Cr-1Zr is **4.99**, meaning those alloys are actually **worse** than Scalmalloy on that metric. The proposal needs to stop sitting on that fence.

My recommendation is **option (b), but only after changing the metric definition**. Use a **log-cost-weighted import-reliance index**:

`CMDRI = Σ_{i≠Al} NIR_i × log10(1 + c_i/c_Al) × x_i`

where `NIR_i` is USGS **net import reliance** (fraction, frozen from the MCS edition current at campaign start), `c_i` is annual average elemental price, `c_Al` is the aluminum reference price, and `x_i` is weight fraction. This keeps both geopolitical exposure and price in the score, but compresses the Sc:Mn price ratio from about **2000:1** to about **6:1**, so Sc still matters without swallowing the whole objective. Under this formulation, approximate reference values are:
- **Scalmalloy:** **0.03831**
- **AlSi10Mg:** **0.01539**
- **Al-3Mn-1Cr-1Zr:** **0.02755**
- **Al-4.5Mg-0.5Zr (Sc-free Scalmalloy-like):** **0.01609**

Against Scalmalloy, those become:
- **AlSi10Mg:** **59.8% reduction**
- **Al-3Mn-1Cr-1Zr:** **28.1% reduction**
- **Al-4.5Mg-0.5Zr:** **58.0% reduction**

That’s the sweet spot. A simple Sc deletion is no longer an automatic win across all plausible high-strength families; the proposal’s own Al-Mn-Cr-Zr baseline **fails** a 40% gate at full 3-1-1 loading, so the optimizer has to genuinely reduce Mn/Cr/Zr burden while preserving YS/ductility. In other words, the metric finally starts doing work.

So the concrete replacement I’d use is:

> **Revised Gate G3 / Objective O4 mineral-burden criterion:** “For all alloys that meet the family-specific mechanical thresholds, compute the Critical Mineral Demand Reduction Index (CMDRI) as `CMDRI = Σ_{i≠Al} NIR_i × log10(1 + c_i/c_Al) × x_i`, where `NIR_i` is USGS net import reliance (fractional; frozen from the Mineral Commodity Summaries edition current at campaign start), `c_i` is the annual average elemental price, `c_Al` is the annual average aluminum price, and `x_i` is the alloy weight fraction. Gate G3 is met when at least one AI-discovered alloy achieves **CMDRI <= 0.60 × CMDRI(Scalmalloy)** (i.e., **>=40% reduction vs. Scalmalloy**) while also meeting the applicable YS/elongation thresholds on ASTM E8 sub-size specimens with n>=3 replicates. Final reporting shall also include CMDRI relative to AlSi10Mg as a secondary benchmark and a per-element CMDRI contribution breakdown.”

That’s the reviewer-ready paragraph. If you want one extra tightening sentence to stop someone from “discovering” AlSi10Mg with a haircut, add: **“Discovery yield counts only compositions outside published commercial nominal windows (e.g., ±0.5 wt% per element).”** Cheap insurance.

On your option list:
- **(a) retain >=40% vs Scalmalloy + add floor vs AlSi10Mg:** not my first choice as a gate. AlSi10Mg is already low on most reasonable criticality scores, so making it a hard floor would exclude many interesting Mn/Cr/Zr/Ce families. Better as a required reporting benchmark, not a pass/fail gate.
- **(b) raise Scalmalloy threshold:** only works if you also fix the formula. With the log-cost CMDRI above, **keeping 40% is already non-trivial**. I would **not** raise it higher than 40% for Phase I.
- **(c) Pareto/skyline criterion:** scientifically nice, but more merit-review friction than you need in a Phase I gate. Good for analysis, bad for proposal simplicity.
- **(d) composite index:** too opaque for DOE review unless you build a literature-derived calibration set. Not worth the complexity here.
- **(e) other:** the best “other” is exactly this: **fix formula + keep 40%**.

Which non-Sc elements actually move the needle? Under the recommended log-cost CMDRI, the approximate **per-wt% impact ranking** is:
1. **Sc**
2. **Er**
3. **Zr**
4. **Sn**
5. **Ti**
6. **Cr**
7. **Ni**
8. **Ce**
9. **Mn**
10. **Li**
11. **Zn**
12. **Cu**
13. **Mg**
14. **Si**
15. **Fe**

At representative alloy loadings, the main non-Sc contributors are a bit different because volume matters too. For the FLAIME palette, the biggest non-Sc movers are:
- **Zr**: high leverage even at 0.3–0.5 wt%
- **Er**: very high leverage at trace loading
- **Mg**: moderate per wt%, but big total effect because it sits at 3–5 wt%
- **Cr** and **Mn**: moderate individually, substantial when used at 1–3 wt%
- **Ce**: meaningful at 2–4 wt%
- **Fe**: basically irrelevant on import-reliance grounds

That ranking matters because it shows the revised metric isn’t just “remove Sc and party.” A second trivial substitution would try to lean on **Zr** or **Er**. The log-cost form prevents that from disappearing into rounding error.

On DOE/FOA language: I’d express the threshold using **USGS “net import reliance”** and cite the **USGS Mineral Commodity Summaries** explicitly, because that’s the cleanest federal term and it’s what the proposal already leans on. I’d also note alignment with the **DOE Critical Materials Assessment 2023** for the broader supply-risk framing. One nuance: the proposal mentions the **USGS 2024** MCS and the **USGS 2022 critical minerals list** implicitly through DOE/USGS conventions. Since USGS has since updated the statutory list again, the safest phrasing is not “USGS 2022 list” in the gate itself, but **“USGS critical minerals list and Mineral Commodity Summaries edition current at campaign start, frozen for campaign duration.”** That avoids a moving-target problem during review and execution.

Bottom line: **the critique is quantitatively correct if the implemented CMDRI includes cost, and the proposal’s citations suggest it probably will.** The strongest fix is **not** to bolt on an AlSi10Mg pass/fail floor. It’s to **define the metric explicitly with log-cost-weighted net import reliance and keep the 40% Scalmalloy threshold**. That makes the gate credible, reviewer-defensible, and hard enough to force real trade-offs.

- Used a reconstructed Scalmalloy composition of Al-4.5Mg-0.7Sc-0.3Zr with minor Mn/Ti/Fe, consistent with common published nominal ranges; exact proprietary composition variants may shift CMDRI values slightly.
- Used a reasonable reconstruction of the proposal’s mineral-burden metric because Appendix 8 gives the linear form `Σ w_i x_i` but does not specify the exact aggregation of USGS, Graedel, Helbig, and ESSENZ factors.
- Evaluated three alternative formulations for sensitivity: pure net-import-reliance weighting, linear cost-inclusive weighting, and log-cost-weighted net-import-reliance weighting.
- Recommended the log-cost formulation instead of linear cost weighting because linear weighting makes Sc contribute ~99% of Scalmalloy’s burden and destroys gate usefulness.
- Treated Al as the base metal and excluded it from the CMDRI summation in the recommended formula, because the gate is intended to discriminate alloying-element burden rather than bulk aluminum content.
- Used representative elemental prices and USGS net import reliance fractions to estimate approximate CMDRI values; these should be frozen to a single MCS edition at campaign start in the proposal text.
- Recommended keeping AlSi10Mg as a required reporting benchmark rather than a hard go/no-go floor, because a hard AlSi10Mg floor would likely screen out credible Mn/Cr/Zr/Ce alloy families.
- Did not recommend a Pareto or composite-index gate despite their validity, because they add proposal complexity and reviewer friction without clear Phase I benefit.
- Ranked non-Sc elements by approximate CMDRI leverage under the recommended log-cost formula and at representative alloy loadings to identify likely loopholes after Sc removal.
- Interpreted DOE/USGS terminology using “net import reliance” as the preferred threshold language and treated DOE 2023 Critical Materials Assessment as contextual framing rather than the gating variable itself.