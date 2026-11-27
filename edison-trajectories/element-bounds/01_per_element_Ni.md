# Phase 1 — Per-element bound: Ni

*Edison task: `da66e079-d3ef-4c71-8a63-60c46e296bf9`*

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


TASK — Element-specific bound: Ni
Ni is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Ni LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Ni) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Ni) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Ni).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.


## Ni compositional bounds for BOFN/GA search space (wt%)

| Bound class | Proposed Ni upper bound (wt%) | Evidence anchor alloys/studies with Ni wt% values | Rationale summary |
|---|---:|---|---|
| Conservative | 1.5 | EN AW-2618 standard Ni = 0.8–1.4 wt% (measured SLM powder 1.2 wt% Ni); this is a commercial/widely used Al-Cu-Mg-Ni-Fe alloy already processed by SLM, though cracking remains an issue (koutny2018influenceofscanning pages 3-5) | Setting Ni at 1.5 wt% stays just above the qualified/commercial 2618 range, giving a literature-defensible ceiling tied to established AM-relevant alloy practice rather than experimental high-Ni exploration. |
| Non-conservative | 5.7 | AlSi10Mg studied with 0–5 wt% Ni additions, with 3 wt% best properties and Al3Ni formation (wang2023influenceofni pages 1-2); Al-5.7Ni eutectic was SLM-processed crack-free over a wide processing window (deng2021ahighstrengthheatresistant pages 3-4, deng2021ahighstrengthheatresistant pages 1-2, deng2021ahighstrengthheatresistant pages 2-3); additional LPBF examples include 4.1 wt% Ni in Al-6.9Ca-4.1Ni-1.6Mn (shurkin2021remarkablethermalstability pages 1-2) and 3 wt% Ni in Al-3Ni-1Ti-0.8Zr designed around eutectic solidification (thapliyal2021designofheterogeneous pages 2-3) | 5.7 wt% Ni is an aggressive but still literature-grounded ceiling because it reaches the demonstrated Al-Ni eutectic LPBF composition that remained crack-free, while staying within clearly Al-rich compositions. |


*Table: This table summarizes conservative and non-conservative Ni upper bounds for an Al-rich LPBF alloy design space, anchored to specific reported LPBF/SLM alloy compositions. It is useful for selecting a search-space ceiling that balances commercial precedent against more aggressive eutectic-based printability evidence.*

### 1) CONSERVATIVE Ni upper bound: **1.5 wt% Ni**
A conservative ceiling is **1.5 wt% Ni**, anchored to the commercial wrought alloy EN AW-2618 (Al–Cu–Mg–Ni–Fe) that has a **standard Ni range of 0.8–1.4 wt%** and has been processed by SLM/LPBF (measured powder ~1.2 wt% Ni). (koutny2018influenceofscanning pages 3-5)

### 2) NON-CONSERVATIVE Ni upper bound: **5.7 wt% Ni**
A defensible but aggressive ceiling is **5.7 wt% Ni**, because an **Al–5.7Ni eutectic alloy** was demonstrated **successfully by SLM over a wide processing window without cracking**, and was selected specifically for its **narrow freezing range / small crack tendency** (i.e., eutectic-assisted crack mitigation). (deng2021ahighstrengthheatresistant pages 3-4)

### 3) Key failure modes setting each bound

**Conservative bound (~1.5 wt% Ni):**
- **Solidification cracking / hot tearing remains possible even at commercial Ni levels**: EN AW-2618 SLM builds showed **small cracks across the full tested parameter range**, strongly degrading tensile properties. (koutny2018influenceofscanning pages 1-3)
- **Brittle intermetallic risk** (general): Ni readily forms **Al3Ni** in LPBF conditions; while it can be beneficial as nanoscale dispersoids, coarser or continuous intermetallic networks (especially in multicomponent alloys) can reduce ductility. (wang2023influenceofni pages 7-9, shi2024solidificationmechanismof pages 1-2)
- **Mineral-burden objective sensitivity**: Ni will generally incur a nontrivial mineral-burden penalty vs many Al-alloying alternatives (project objective; not evaluated in the cited LPBF papers).

**Non-conservative bound (~5.7 wt% Ni):**
- **Intermetallic fraction/continuity and embrittlement risk at higher Ni**: LPBF Al–Ni systems strengthen via **Al3Ni**; pushing Ni beyond eutectic-like levels can increase intermetallic volume fraction and risk reduced ductility/toughness if Al3Ni becomes coarse/continuous (even if the Al–5.7Ni case showed coherent nanoscale dispersoids). (deng2021ahighstrengthheatresistant pages 2-3, deng2021ahighstrengthheatresistant pages 3-4)
- **Multicomponent segregation/network formation**: In Al–Si–Cu–Ni alloys, **Cu- and Ni-rich phases segregate to cellular boundaries** and can form multiple intermetallics (e.g., **Al7Cu4Ni**, Al3Ni, etc.), which can raise strength but has been associated with **very low ductility** in such networked microstructures. (shi2024solidificationmechanismof pages 9-11)
- **Process/property coupling via melt-pool dynamics**: In AlSi10Mg, Ni additions (0–5 wt%) altered the Si-network scale (coarsening at low Ni, refinement at higher Ni), implying that Ni changes solidification/melt-pool behavior and thus can narrow the robust process window if combined with other crack-sensitive elements. (wang2023influenceofni pages 7-9)

### 4) Ni-specific caveats/interactions for follow-up joint-constraints
- **Ni–Si interaction (AlSi10Mg baseline):** Ni reacts in situ to form ~30 nm **Al3Ni**, and Ni content modulates the **eutectic Si network size/continuity**; this will couple Ni bounds to any Si bound and to LPBF energy-density constraints. (wang2023influenceofni pages 7-9)
- **Ni–(Ti,Zr) strategy for printability:** A printability-oriented design explicitly uses Ni to access **terminal eutectic solidification** (noting Al–Al3Ni eutectic near ~6 wt% Ni) while Ti/Zr provide heterogeneous nucleation; if Ti/Zr are also active variables, a joint constraint should prevent simultaneously high Ni + low nucleant levels if crack-free printing is required. (thapliyal2021designofheterogeneous pages 2-3)
- **Ni–Cu (and Ni–Cu–Si) risk:** Ni can participate in **Cu–Ni–Al intermetallics** (e.g., Al7Cu4Ni) that segregate at cell boundaries; thus, Ni upper bounds may need to tighten as Cu increases to avoid continuous brittle boundary films and loss of elongation. (shi2024solidificationmechanismof pages 1-2, shi2024solidificationmechanismof pages 9-11)
- **Eutectic vs precipitation-strengthened regimes:** Ni at eutectic-like levels (≈5–6 wt%) can reduce freezing range and mitigate cracking (good for printability), but may move the alloy into a microstructure dominated by eutectic/intermetallic strengthening rather than conventional age hardening; this impacts downstream heat-treatment assumptions and performance models. (deng2021ahighstrengthheatresistant pages 3-4)


References

1. (koutny2018influenceofscanning pages 3-5): Daniel Koutny, David Palousek, Libor Pantelejev, Christian Hoeller, Rudolf Pichler, Lukas Tesicky, and Jozef Kaiser. Influence of scanning strategies on processing of aluminum alloy en aw 2618 using selective laser melting. Materials, 11:298, Feb 2018. URL: https://doi.org/10.3390/ma11020298, doi:10.3390/ma11020298. This article has 127 citations.

2. (wang2023influenceofni pages 1-2): Hong Wang, Like He, Qingyong Zhang, and Yiqing Yuan. Influence of ni contents on microstructure and mechanical performance of alsi10mg alloy by selective laser melting. Materials, 16:4679, Jun 2023. URL: https://doi.org/10.3390/ma16134679, doi:10.3390/ma16134679. This article has 15 citations.

3. (deng2021ahighstrengthheatresistant pages 3-4): Junwang Deng, Chao Chen, Xiaochun Liu, Yunping Li, Kechao Zhou, and Shengmin Guo. A high-strength heat-resistant al−5.7ni eutectic alloy with spherical al3ni nano-particles by selective laser melting. Scripta Materialia, 203:114034, Oct 2021. URL: https://doi.org/10.1016/j.scriptamat.2021.114034, doi:10.1016/j.scriptamat.2021.114034. This article has 154 citations and is from a highest quality peer-reviewed journal.

4. (deng2021ahighstrengthheatresistant pages 1-2): Junwang Deng, Chao Chen, Xiaochun Liu, Yunping Li, Kechao Zhou, and Shengmin Guo. A high-strength heat-resistant al−5.7ni eutectic alloy with spherical al3ni nano-particles by selective laser melting. Scripta Materialia, 203:114034, Oct 2021. URL: https://doi.org/10.1016/j.scriptamat.2021.114034, doi:10.1016/j.scriptamat.2021.114034. This article has 154 citations and is from a highest quality peer-reviewed journal.

5. (deng2021ahighstrengthheatresistant pages 2-3): Junwang Deng, Chao Chen, Xiaochun Liu, Yunping Li, Kechao Zhou, and Shengmin Guo. A high-strength heat-resistant al−5.7ni eutectic alloy with spherical al3ni nano-particles by selective laser melting. Scripta Materialia, 203:114034, Oct 2021. URL: https://doi.org/10.1016/j.scriptamat.2021.114034, doi:10.1016/j.scriptamat.2021.114034. This article has 154 citations and is from a highest quality peer-reviewed journal.

6. (shurkin2021remarkablethermalstability pages 1-2): P.K. Shurkin, N.V. Letyagin, A.I. Yakushkova, M.E. Samoshina, D. Yu. Ozherelkov, and T.K. Akopyan. Remarkable thermal stability of the al-ca-ni-mn alloy manufactured by laser-powder bed fusion. Materials Letters, 285:129074, Feb 2021. URL: https://doi.org/10.1016/j.matlet.2020.129074, doi:10.1016/j.matlet.2020.129074. This article has 45 citations and is from a peer-reviewed journal.

7. (thapliyal2021designofheterogeneous pages 2-3): Saket Thapliyal, Shivakant Shukla, Le Zhou, Holden Hyer, Priyanshi Agrawal, Priyanka Agrawal, Mageshwari Komarasamy, Yongho Sohn, and Rajiv S. Mishra. Design of heterogeneous structured al alloys with wide processing window for laser-powder bed fusion additive manufacturing. Additive Manufacturing, 42:102002, Jun 2021. URL: https://doi.org/10.1016/j.addma.2021.102002, doi:10.1016/j.addma.2021.102002. This article has 109 citations and is from a highest quality peer-reviewed journal.

8. (koutny2018influenceofscanning pages 1-3): Daniel Koutny, David Palousek, Libor Pantelejev, Christian Hoeller, Rudolf Pichler, Lukas Tesicky, and Jozef Kaiser. Influence of scanning strategies on processing of aluminum alloy en aw 2618 using selective laser melting. Materials, 11:298, Feb 2018. URL: https://doi.org/10.3390/ma11020298, doi:10.3390/ma11020298. This article has 127 citations.

9. (wang2023influenceofni pages 7-9): Hong Wang, Like He, Qingyong Zhang, and Yiqing Yuan. Influence of ni contents on microstructure and mechanical performance of alsi10mg alloy by selective laser melting. Materials, 16:4679, Jun 2023. URL: https://doi.org/10.3390/ma16134679, doi:10.3390/ma16134679. This article has 15 citations.

10. (shi2024solidificationmechanismof pages 1-2): Zhichao Shi, Pengfei Yan, and Biao Yan. Solidification mechanism of microstructure of al-si-cu-ni alloy manufactured by laser powder bed fusion and mechanical properties effect. Metals, 14:586, May 2024. URL: https://doi.org/10.3390/met14050586, doi:10.3390/met14050586. This article has 5 citations.

11. (shi2024solidificationmechanismof pages 9-11): Zhichao Shi, Pengfei Yan, and Biao Yan. Solidification mechanism of microstructure of al-si-cu-ni alloy manufactured by laser powder bed fusion and mechanical properties effect. Metals, 14:586, May 2024. URL: https://doi.org/10.3390/met14050586, doi:10.3390/met14050586. This article has 5 citations.

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


TASK — Element-specific bound: Ni
Ni is one of 15 non-Al alloying elements. Provide a CONSERVATIVE upper bound (defensible from established LPBF Al alloy literature, e.g. published commercial / qualified AM compositions) and a NON-CONSERVATIVE upper bound (defensible but more aggressive — e.g. extending to the limit of TCAl10 Al-rich validity, eutectic constraints, or known experimental high-Ni LPBF studies).

Please return:
1. CONSERVATIVE bound (wt% of Ni) with 1-2 sentence justification
   citing specific LPBF / Al-alloy literature.
2. NON-CONSERVATIVE bound (wt% of Ni) with 1-2 sentence justification.
3. Key failure modes that set each bound (e.g. hot cracking, primary phase
   formation, oxidation during atomization, intermetallic embrittlement,
   loss of TCAl10 ternary/quaternary assessment coverage, mineral-burden
   penalty for Ni).
4. Any element-specific caveats or interactions worth flagging in a follow-up
   joint-constraints analysis.

Express bounds in wt% (weight percent). Be concise but quantitative.
```
