# Phase 1 — Per-element bound: Cu

*Edison task: `edaa4a5d-10b9-45c0-996b-2c071314ffde`*

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


TASK — Element-specific bound: Cu
Cu is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Cu LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Cu) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Cu) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Cu).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Cu compositional upper bounds for BOFN / GA search space (Al-rich LPBF)

| Bound type | Proposed Cu upper bound (wt%) | Evidence anchor alloys/studies (with short notes) | Primary failure modes limiting bound | Key compositional interactions/caveats |
|---|---:|---|---|---|
| Conservative | 4.5 | Commercial LPBF A205/A20X-family alloy explicitly reported at Al-4.5Cu-3.25Ti-1.25B-0.74Ag-0.27Mg...; LPBF AlSi10Mg+4 wt%Cu also demonstrated (~3.96 wt% measured). This keeps Cu at the level of established AM-relevant compositions rather than pushing into higher-Cu experimental territory (mair2021microstructureandmechanical pages 1-2, bosio2021strengtheningstrategiesfor pages 1-2) | Beyond this range, Cu-rich 2xxx-type alloys increasingly risk wide freezing-range hot cracking unless aided by eutectic control/grain refiners; Cu also raises Al2Cu fraction and post-build brittleness/corrosion sensitivity if not heat-treated appropriately (tumulu2025laserpowderbeda pages 45-48, bosio2021strengtheningstrategiesfor pages 1-2) | Strong interactions with Mg and Ag (precipitation hardening), with TiB2/Ti/B or Zr/Sc grain refiners for crack mitigation; Cu should be tighter when Si is low and no grain refiner is present. Mineral-burden objective will also penalize Cu, so a low conservative cap is attractive (mair2021microstructureandmechanical pages 1-2, bosio2021strengtheningstrategiesfor pages 1-2, tumulu2025laserpowderbeda pages 45-48) |
| Non-conservative | 12 | LPBF-specific study on AlCu4Mg-derived blends examined 4, 6, 8, 10, 12 wt% Cu and found >10 wt% Cu gave >99.5% relative density with no solidification cracks; rationale was increased Al-Al2Cu eutectic and reduced end-stage solidification range. Review context notes crack sensitivity drops beyond ~6 wt% Cu, with ~3 wt% as an inflection in crack-length behavior (belelli2022effectofcu pages 1-5, belelli2022effectofcu pages 5-9, tumulu2025laserpowderbed pages 45-48) | Limit is set by aggressive Cu-rich eutectic/intermetallic loading, embrittlement, corrosion/property tradeoffs, and declining transferability to broader multicomponent Al-rich TCAl10 assessments; LPBF evidence at 12 wt% exists, but this is not a broadly qualified commercial regime. Going higher also erodes Al-rich design space and likely worsens mineral-burden penalty (belelli2022effectofcu pages 1-5, belelli2022effectofcu pages 5-9) | Best treated as conditional: only allow near 10-12 wt% when paired with Mg/Ag/Si or crack-mitigating refiners and when CALPHAD/Scheil indicates acceptable freezing range. Vanzetti showed gas-atomized AlSi10Mg+Cu powders up to 20 wt% Cu are atomizable, but that is powder-feasibility only, not LPBF printability, so it should not set the BO upper bound (vanzetti2023designandcharacterization pages 1-2) |


*Table: This table summarizes conservative and non-conservative Cu upper bounds for an Al-rich LPBF Bayesian optimization search space, tying each bound to literature anchors, limiting failure modes, and key alloy-interaction caveats. It is useful for choosing a default Cu cap now and identifying where later joint-constraint logic is needed.*

### 1) CONSERVATIVE upper bound (Cu, wt%)
**Cu ≤ 4.5 wt%**. This is anchored to established LPBF-relevant Al–Cu systems including the commercial A205/A20X-family alloy with explicitly reported composition **Al–4.5Cu–3.25Ti–1.25B–0.74Ag–0.27Mg… (wt%)**, and an AlSi10Mg + Cu LPBF in-situ alloying study targeting **4 wt% Cu** (measured **3.96 ± 0.26 wt% Cu**)—both demonstrating that ~4–4.5 wt% Cu is within known printable/processable composition space. (mair2021microstructureandmechanical pages 1-2, bosio2021strengtheningstrategiesfor pages 1-2)

### 2) NON-CONSERVATIVE upper bound (Cu, wt%)
**Cu ≤ 12 wt%**. An LPBF-specific composition-sweep study produced Al–Cu–Mg alloys at **4, 6, 8, 10, and 12 wt% Cu**, and reported that specimens with **>10 wt% Cu** achieved **>99.5% relative density** and showed **no solidification cracks**, attributing the improvement to increased Al–Al\₂Cu eutectic and a reduced vulnerable end-of-solidification interval/solidification temperature range. (belelli2022effectofcu pages 1-5, belelli2022effectofcu pages 5-9)

### 3) Key failure modes setting each bound
**Conservative bound (≈4.5 wt% Cu):**
- **Solidification/hot cracking risk in Al–Cu (2xxx) alloys** due to wide solidification range, especially if the rest of the palette does not provide crack-mitigating eutectic or grain refinement; the conservative cap stays within demonstrated commercial AM compositions rather than relying on “compositionally healed” high-Cu regimes. (tumulu2025laserpowderbed pages 42-45, tumulu2025laserpowderbeda pages 45-48)
- **Excess Al\₂Cu network formation / embrittlement & ductility loss** if Cu is increased without controlled heat treatment; in AlSi10Mg+Cu work, brittle Si/Cu-rich constituents and aging response are cited as ductility risks. (bosio2021strengtheningstrategiesfor pages 1-2)
- **In-situ alloying compositional heterogeneity** (if Cu is added as elemental powder) due to mismatched melting/thermal properties, motivating a tighter Cu range when powder blending is used. (bosio2021strengtheningstrategiesfor pages 1-2)

**Non-conservative bound (≈12 wt% Cu):**
- **Eutectic/intermetallic overload tradeoffs**: the same abundant Al–Al\₂Cu eutectic that can reduce cracking at 10–12 wt% Cu can also create continuous brittle networks and worsen corrosion/property stability unless tightly controlled by thermal history and co-alloying. (belelli2022effectofcu pages 1-5, belelli2022effectofcu pages 5-9)
- **Model/assessment transferability risk in multicomponent space**: at very high Cu, phase constitution becomes more sensitive to higher-order interactions; extrapolation beyond well-assessed binary/ternary subspaces becomes riskier for joint CALPHAD down-selection (even if the binary Al–Cu itself is well studied). This is a pragmatic reason to cap exploration at the highest Cu already demonstrated crack-free in LPBF rather than pushing higher without LPBF evidence. (belelli2022effectofcu pages 1-5)
- **Mineral-burden objective penalty**: Cu is not in the “ultra-critical” class like some rare earths, but increasing Cu will generally worsen any import-reliance/criticality-weighted objective, so high-Cu solutions may be disfavored unless they deliver strong performance gains.

### 4) Cu-specific caveats / interactions for follow-up joint-constraints
- **Non-monotonic cracking vs Cu**: the LPBF Cu-sweep showed worse cracking around intermediate Cu (e.g., 6–8 wt%) but crack-free behavior at **≥10 wt% Cu**, consistent with review-level statements that crack sensitivity decreases beyond a few wt% Cu (inflection ~3 wt%; low sensitivity reported for >6 wt% Cu). This suggests a **joint constraint** should consider the full solidification path (Scheil) and not assume “more Cu = more cracking.” (belelli2022effectofcu pages 1-5, belelli2022effectofcu pages 5-9, tumulu2025laserpowderbed pages 45-48)
- **Strong dependence on co-alloying and inoculants**: Cu’s printability window depends strongly on whether the alloy contains eutectic-formers (e.g., Si) and/or grain refiners/inoculants (e.g., TiB\₂/Ti/B in A205/A20X-class alloys); thus, Cu bounds may be tightened when Si/TiB\₂/Zr/Sc are simultaneously near-zero. (mair2021microstructureandmechanical pages 1-2, tumulu2025laserpowderbeda pages 45-48)
- **Atomization ≠ LPBF**: powders with very high Cu (e.g., AlSi10Mg + 20 wt% Cu) can be gas-atomized and characterized, but that does not establish LPBF crack-free processability; do not use atomization-feasibility alone to set the BO upper bound. (vanzetti2023designandcharacterization pages 1-2)

References

1. (mair2021microstructureandmechanical pages 1-2): P. Mair, L. Kaserer, Jakob Braun, N. Weinberger, I. Letofsky-Papst, and G. Leichtfried. Microstructure and mechanical properties of a tib2-modified al–cu alloy processed by laser powder-bed fusion. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 799:140209, Jan 2021. URL: https://doi.org/10.1016/j.msea.2020.140209, doi:10.1016/j.msea.2020.140209. This article has 150 citations.

2. (bosio2021strengtheningstrategiesfor pages 1-2): Federico Bosio, Paolo Fino, Diego Manfredi, and Mariangela Lombardi. Strengthening strategies for an al alloy processed by in-situ alloying during laser powder bed fusion. Materials & Design, 212:110247, Dec 2021. URL: https://doi.org/10.1016/j.matdes.2021.110247, doi:10.1016/j.matdes.2021.110247. This article has 43 citations and is from a highest quality peer-reviewed journal.

3. (tumulu2025laserpowderbeda pages 45-48): SK Tumulu. Laser powder bed fusion additive manufacturing (lpbf-am) of aluminum-copper alloys. Unknown journal, 2025.

4. (belelli2022effectofcu pages 1-5): Filippo Belelli, Riccardo Casati, and Maurizio Vedani. Effect of cu content on hot-crack resistance of al-cu-mg alloys produced by laser powder bed fusion. Philosophical Magazine Letters, 102:111-119, Jan 2022. URL: https://doi.org/10.1080/09500839.2021.2024616, doi:10.1080/09500839.2021.2024616. This article has 7 citations and is from a peer-reviewed journal.

5. (belelli2022effectofcu pages 5-9): Filippo Belelli, Riccardo Casati, and Maurizio Vedani. Effect of cu content on hot-crack resistance of al-cu-mg alloys produced by laser powder bed fusion. Philosophical Magazine Letters, 102:111-119, Jan 2022. URL: https://doi.org/10.1080/09500839.2021.2024616, doi:10.1080/09500839.2021.2024616. This article has 7 citations and is from a peer-reviewed journal.

6. (tumulu2025laserpowderbed pages 45-48): SK Tumulu. Laser powder bed fusion additive manufacturing (lpbf-am) of aluminum-copper alloys. Unknown journal, 2025.

7. (vanzetti2023designandcharacterization pages 1-2): Matteo Vanzetti, Michael J. Pavel, C. Jacob Williamson, Elisa Padovano, Lorena I. Pérez-Andrade, Mark Weaver, Luke N. Brewer, Federica Bondioli, and Paolo Fino. Design and characterization of innovative gas-atomized al-si-cu-mg alloys for additive manufacturing. Metals, 13:1845, Nov 2023. URL: https://doi.org/10.3390/met13111845, doi:10.3390/met13111845. This article has 10 citations.

8. (tumulu2025laserpowderbed pages 42-45): SK Tumulu. Laser powder bed fusion additive manufacturing (lpbf-am) of aluminum-copper alloys. Unknown journal, 2025.

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


TASK — Element-specific bound: Cu
Cu is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Cu LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Cu) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Cu) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Cu).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
