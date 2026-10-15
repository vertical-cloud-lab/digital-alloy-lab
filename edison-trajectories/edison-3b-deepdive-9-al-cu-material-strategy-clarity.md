# Edison Scientific LITERATURE_HIGH Output — Al vs Cu Material Strategy for Topic 3B

**Task ID:** `13fc6d7e-e22e-4b3f-89d4-e8459c2ed1f9`
**Mode:** LITERATURE_HIGH | **Date:** 2026-04-10 | **Size:** ~28K chars
**Part of:** Topic 3B Deep-Dive Series (10 queries, ~331K chars total)

> *Raw Edison Scientific output below. The query prompt appears first, followed by the model's structured response.*

---

Question: 
RESEARCH QUESTION: For a DOE Genesis Mission proposal targeting Topic 3B (Critical Minerals), what should be the relationship between Al alloys and Cu alloys in the proposal — and what does the optimal material strategy look like?

Context: There is confusion about whether the proposal should:
(a) Focus entirely on Al alloys and frame them as critical-mineral-lean
(b) Shift primarily to Cu-Cr-Zr as a Be-Cu replacement
(c) Use Al as Phase I demonstration with Cu-Cr-Zr as Phase I stretch / Phase II target
(d) Pursue both Al and Cu alloys in parallel

The platform (FLAIME) uses induction-heated ultrasonic atomization (max ~1300°C). Al alloys melt at ~570-660°C. Cu-Cr-Zr melts at ~1075°C. Both are within range.

Investigate:
1. For Topic 3B, which material demonstrates stronger "critical mineral demand reduction": Al alloys or Cu-Cr-Zr?
2. Can a single proposal credibly cover BOTH Al and Cu alloy families?
3. What is the argument for Al alloys as the "anchor" vs. Cu alloys as the "anchor"?
4. Risk assessment: is Cu-Cr-Zr atomization via ultrasonic atomization demonstrated in literature? 
5. Scoping: for a 9-month $500-750K Phase I, is it feasible to do both Al and Cu-Cr-Zr?
6. How would reviewers perceive a "two alloy family" proposal vs. a focused single-family proposal?
7. Phase I/Phase II strategy: best division of materials between phases?
8. What SPECIFIC Al alloy compositions should be targeted for maximum critical minerals story?
9. What SPECIFIC Cu-Cr-Zr compositions are most relevant for Be-Cu replacement?
10. Precedent: have successful DOE proposals covered multiple alloy families in a single autonomous platform?

Cite all sources.


## Recommended relationship between Al and Cu alloy efforts (Topic 3B)
A Topic 3B (Critical Minerals) proposal should treat **Al alloys as the Phase I anchor (primary demonstration)** and **Cu–Cr–Zr as a Phase I stretch objective / Phase II primary target**, rather than trying to run two fully parallel alloy-development programs in Phase I. This structure maximizes credibility under tight Phase I constraints while still capturing the high-value Be–Cu substitution story in a risk-managed way. The key is to frame the effort as a **single transferable autonomous manufacturing/process platform** (induction-heated ultrasonic atomization + closed-loop optimization) driven by staged “challenge problems,” where different alloy families are successive demonstrations of the same platform capability rather than separate projects. (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7, decost2022towardsautomateddesign pages 1-4, stach2021autonomousexperimentationsystems pages 6-8)

| Approach | Critical-mineral demand reduction | Technical fit to ultrasonic atomization at <=1300C | Literature maturity / risk | Phase I feasibility (9 months) | Reviewer perception | Recommended role in proposal |
|---|---|---|---|---|---|---|
| Al alloys (Mg-free Al-Zr; Al-Si) | Stronger Topic 3B story if framed as avoiding Mg and REE/Sc additions: Mg is near-critical in DOE’s assessment, and REEs are commonly critical; Al itself is noncritical short-term. Dilute Al-Zr compositions such as Al-0.25 wt% Zr are documented, and Al-Si is a low-risk Al family (bauer20232023criticalmaterials pages 16-18, bauer20232023criticalmaterials pages 133-136, hayes2018criticalmineralsa pages 1-2, czerwinski2024aluminumalloysfor pages 42-43, kahveci2019measurementandprediction pages 1-2) | Excellent fit. Induction-based ultrasonic atomization on rePowder operates up to ~1300C and has directly produced Al-10Cu powder at 1100C under argon/vacuum; Al alloy ultrasonic atomization is well represented in the literature (ukabhai2025investigationofalcu pages 1-3) | Lowest technical risk of the options; Al ultrasonic atomization is established, with known process windows and manageable issues such as minor particle fusion / cooling effects (ukabhai2025investigationofalcu pages 1-3) | High. Best suited for end-to-end Phase I demonstration of atomization + closed-loop optimization + metrology on the platform (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7) | Likely favorable as a focused, credible Phase I anchor with a clear critical-mineral-lean message (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7) | Primary Phase I anchor |
| Cu-Cr-Zr (C18150-type) | Mixed story. Strong substitution case for replacing Be-Cu with a Be-free alloy, but copper itself is not a short-term DOE critical material and rises mainly to near-critical/greater energy importance in longer-term views; thus the demand-reduction story is weaker than Mg-lean Al unless framed specifically as Be-Cu substitution and safer supply/use (bauer20232023criticalmaterials pages 133-136, reich2025criticalminerals pages 5-6, reich2025criticalminerals pages 1-2, morozova2018microstructureandproperties pages 1-2) | Plausible fit within platform temperature envelope: copper-alloy ultrasonic atomization has been shown on rePowder-type systems, and the induction module reaches ~1300C; however no direct CuCrZr ultrasonic atomization citation was found (ciftcli2025alloydevelopmentfrom pages 1-3, ukabhai2025investigationofalcu pages 1-3) | Moderate risk. Cu-containing / copper-alloy UA is feasible, but direct CuCrZr UA precedent was not located; higher-melting alloys raise concerns around oxidation, contamination, evaporation, amplitude limits, and melt accumulation (ciftcli2025alloydevelopmentfrom pages 1-3, sojoodi2025integrationofcircular pages 18-19, presz2024ultrasonicatomizationas pages 11-12, ukabhai2025investigationofalcu pages 1-3) | Medium if limited to feasibility / powder-window demonstration; low for full optimization and qualification in Phase I (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7) | Reviewers may view it as interesting and relevant for Be-Cu replacement, but riskier than Al if made the sole near-term anchor without direct UA precedent (morozova2018microstructureandproperties pages 1-2, edwards2025inertialfusionenergy pages 10-12) | Phase I stretch goal; stronger Phase II target |
| Two-family phased strategy | Best combined story: use Al to show direct critical-mineral-lean reduction now, and CuCrZr to show future Be-Cu substitution on the same autonomous platform (bauer20232023criticalmaterials pages 16-18, bauer20232023criticalmaterials pages 133-136, morozova2018microstructureandproperties pages 1-2) | Credible if presented as one platform with shared process physics / workflows and staged challenge problems rather than two equal campaigns (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 12-14, edwards2025inertialfusionenergy pages 5-7) | Balanced risk: leverages low-risk Al for platform proof while containing CuCrZr risk to a bounded stretch demonstration (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7) | Best fit for 9 months if scoped as Al end-to-end + CuCrZr feasibility only; not advisable as two parallel full alloy-development efforts (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7) | Most likely positive if framed as a phased, challenge-driven platform demonstration; negative if framed as two unfocused parallel alloy programs (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7, decost2022towardsautomateddesign pages 1-4, stach2021autonomousexperimentationsystems pages 6-8) | Recommended overall structure: Al anchor in Phase I, CuCrZr stretch in Phase I / main expansion in Phase II |


*Table: This table compares Al-alloy and Cu-Cr-Zr options for a DOE Topic 3B proposal across critical-mineral impact, technical risk, and Phase I fit. It is useful for deciding which alloy family should anchor the proposal and how to scope a credible phased strategy.*

## 1. Which material demonstrates stronger “critical mineral demand reduction”: Al alloys or Cu–Cr–Zr?
**Al alloys generally support the stronger “critical mineral demand reduction” framing**—provided you deliberately target **Mg-lean/Mg-free and REE/Sc-free** Al compositions. In DOE’s Critical Materials Assessment, **magnesium is near-critical in the short term**, while several rare earth elements are critical; aluminum itself is noncritical in the short term. (bauer20232023criticalmaterials pages 133-136)

Copper’s criticality is more mixed depending on jurisdiction and horizon: DOE’s short-term matrix lists **copper as noncritical** (though increasing in importance later), while other critical-minerals reviews describe copper as central/critical for electrification and show national lists vary. (bauer20232023criticalmaterials pages 133-136, reich2025criticalminerals pages 5-6, czerwinski2022criticalmineralsfor pages 1-2)

Therefore:
- **Al anchor story:** “reduce demand for Mg / avoid REEs while delivering performance,” using Al compositions that avoid near-critical Mg and critical REEs. (bauer20232023criticalmaterials pages 133-136, hayes2018criticalmineralsa pages 1-2)
- **Cu–Cr–Zr story:** “replace Be–Cu with a Be-free high-strength, high-conductivity copper alloy,” which is a substitution and safety/regulatory story more than a copper-demand-reduction story. (morozova2018microstructureandproperties pages 1-2)

## 2. Can a single proposal credibly cover BOTH Al and Cu alloy families?
Yes—**if** you explicitly adopt a **challenge-problem, staged maturation** structure and define crosscutting platform KPIs (powder sphericity/PSD, oxygen pickup, throughput, repeatability, closed-loop convergence), then show that two material classes are **two demonstrations of the same workflow** rather than two independent alloy programs. The challenge-problem approach, staged maturity cycles, and standardized interfaces/workflows are repeatedly emphasized as how to credibly cover heterogeneous technical domains without losing focus. (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7, oconnor2025reducedgravityand pages 48-51)

Autonomous experimentation literature also provides precedent that a single autonomous platform can present **multiple distinct case studies** to demonstrate flexibility and generality (e.g., two alloy vignettes on one platform; multiple material classes on MINERVA; broad AE campaigns across materials). (decost2022towardsautomateddesign pages 1-4, hao2025autonomousmaterialssynthesis pages 19-21, stach2021autonomousexperimentationsystems pages 6-8)

## 3. Argument for Al alloys as the “anchor” vs Cu alloys as the “anchor”
### Al as anchor
- **Critical-minerals narrative is cleaner**: avoid Mg (near-critical) and avoid REEs/Sc (often critical across studies). (bauer20232023criticalmaterials pages 133-136, hayes2018criticalmineralsa pages 1-2)
- **Lower technical risk for ultrasonic atomization**: induction-based ultrasonic atomization (rePowder) is directly demonstrated for Al-containing alloys (e.g., Al–10Cu at 1100 °C) with good sphericity and LPBF-suitable PSD, and the induction module is rated to ~1300 °C. (ukabhai2025investigationofalcu pages 1-3)

### Cu–Cr–Zr as anchor
- **Strong application pull** when framed as **Be–Cu replacement**: Cu–Cr–Zr alloys are engineered for high strength + high conductivity; Be–Cu can reach very high strength but much lower conductivity. (morozova2018microstructureandproperties pages 1-2)
- However, **riskier as Phase I anchor** because direct CuCrZr ultrasonic atomization precedent was not located in the retrieved literature, and higher-melting / copper systems increase sensitivity to oxygen pickup and process constraints. (sojoodi2025integrationofcircular pages 18-19, presz2024ultrasonicatomizationas pages 11-12)

Net: make **Al the anchor** and position Cu–Cr–Zr as the “next material-class challenge problem.” (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7)

## 4. Risk assessment: is Cu–Cr–Zr ultrasonic atomization demonstrated?
**Direct ultrasonic atomization of CuCrZr specifically was not found** in the retrieved sources; this is a real proposal risk you should acknowledge.

That said, the broader feasibility case is solid:
- The Amazemet rePowder system (induction-heated ultrasonic atomization) can melt up to ~1300 °C and has demonstrated ultrasonic atomization at 1100 °C for Al–10Cu under argon/vacuum, producing spherical powder (d50 15–75 µm). (ukabhai2025investigationofalcu pages 1-3)
- Induction-based ultrasonic atomization of a **copper alloy** on a rePowder-type system is reported (figure evidence, though without CuCrZr composition/temperature details). (ciftcli2025alloydevelopmentfrom pages 1-3)

Key technical risks for Cu alloys / higher-melting systems to manage in the proposal include: atmosphere sensitivity and oxidation pickup; the fact that ultrasonic/plasma atomization is not a decontamination method (O/C present in feedstock remains); equipment amplitude requirements; and failure modes like melt accumulation that can halt atomization. (sojoodi2025integrationofcircular pages 18-19, presz2024ultrasonicatomizationas pages 11-12)

## 5. Phase I feasibility: can you do both Al and Cu–Cr–Zr in 9 months ($500–750K)?
A **full parallel** optimization of both alloy families in Phase I is likely to read as over-scoped.

A **phased-within-Phase-I** approach is feasible:
- **Al track (primary):** end-to-end closed-loop demonstration (powder production → powder metrology → decision/optimization loop) on a Mg-lean Al composition.
- **CuCrZr track (stretch):** demonstrate melt handling + stable atomization + initial powder-quality window (e.g., oxidation/PSD/sphericity) sufficient to de-risk Phase II.

This matches common guidance for complex platforms: define challenge problems, harden workflows early, then expand validation and automated optimization in later phases. (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7)

## 6. Reviewer perception: two alloy families vs focused single-family
Reviewers typically reward focus, but the autonomy literature shows that **multiple case studies are acceptable and sometimes expected** when the platform is the product and the case studies prove generality.

A “two family” proposal is likely to be viewed positively if you:
- explicitly state “**one platform, two staged challenge problems**,”
- use shared KPIs and shared data/controls,
- keep CuCrZr Phase I scope narrowly defined as feasibility/risk-reduction. (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7, decost2022towardsautomateddesign pages 1-4, stach2021autonomousexperimentationsystems pages 6-8)

It will be viewed negatively if it reads like “two independent alloy-development programs” with two independent experimental matrices.

## 7. Phase I / Phase II strategy
**Phase I (9 months):**
1) **Platform shakedown + autonomous loop** on Al (primary proof): demonstrate repeatable induction-heated ultrasonic atomization under inert/vacuum conditions; produce spherical powder and close an optimization loop on powder quality (PSD, sphericity, oxygen). (ukabhai2025investigationofalcu pages 1-3, edwards2025inertialfusionenergy pages 10-12)
2) **CuCrZr feasibility sprint**: establish stable melting/flow/atomization regime for copper-alloy-class temperatures and document powder oxygen pickup constraints and window. (ciftcli2025alloydevelopmentfrom pages 1-3, sojoodi2025integrationofcircular pages 18-19, presz2024ultrasonicatomizationas pages 11-12)

**Phase II:**
- Expand CuCrZr to application-driven optimization (strength–%IACS trade space), post-processing (solution/aging) and component-relevant testing; optionally add an Al “second composition” once the loop is robust.

This “challenge-driven multicycle maturation” is explicitly recommended for complex ecosystems. (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7)

## 8. Specific Al alloy compositions to target (maximize critical minerals story)
The strongest “critical-mineral-lean” Al targets are **Mg-lean/Mg-free and REE/Sc-free**.

Concrete, literature-cited candidate compositions:
- **Al–0.25 wt% Zr** (dilute conductor alloy; Zr additions 0.1–0.3 wt% cited; used to maintain properties at elevated temperature). (kahveci2019measurementandprediction pages 1-2)
- Additional dilute-Zr options cited in the conductor review: **Al–0.4Zr**, **Al–0.6 wt% Zr**, and **Al–0.6%Zr–0.4%Fe–0.4%Si**. (czerwinski2024aluminumalloysfor pages 42-43)

Note: the same review also discusses Al–Ce/La/Y and Sc/Zr systems with specific compositions, but these can conflict with a “critical mineral reduction” message because REEs (and Sc) are often critical; if used at all, they should be treated as future exploratory extensions rather than the Topic-3B headline. (hayes2018criticalmineralsa pages 1-2, czerwinski2024aluminumalloysfor pages 42-43)

## 9. Specific Cu–Cr–Zr compositions relevant for Be–Cu replacement
Typical/targeted CuCrZr compositions and ranges (wt%):
- Common nominal: **Cu–0.6Cr–0.1Zr**. (morozova2018microstructureandproperties pages 13-14)
- “Optimal” contents cited: ~**0.67 wt% Cr** and **0.12 wt% Zr** (with practical upper limits depending on processing). (morozova2018microstructureandproperties pages 1-2)
- Other literature variants include **Cu–0.4Cr–0.1Zr**, **Cu–0.75Cr–0.13Zr**, **Cu–0.8Cr–0.08Zr**. (wang2020effectsofminor pages 1-2)

Property/use-case targets relevant to Be–Cu replacement:
- Conductivity targets cited for Cu–Cr–Zr applications: **>80% IACS** for high-strength wires, **>70% IACS** for welding electrodes. (morozova2018microstructureandproperties pages 11-13)
- Cu–Cr–Zr aged alloys often cited around **~80% IACS**. (morozova2018microstructureandproperties pages 1-2)
- Be–Cu comparison: Be–Cu can reach ~2000 MPa but with ~10–20% IACS, so CuCrZr is positioned as the balanced high-conductivity alternative. (morozova2018microstructureandproperties pages 1-2)

## 10. Precedent: successful DOE proposals with multiple alloy families on one autonomous platform?
Direct evidence from “successful DOE proposals” was not available in the retrieved corpus. However, **peer-reviewed precedent** strongly supports multi-case-study autonomous platforms:
- A single autonomous alloy platform publishing **two alloy design vignettes** to demonstrate flexibility and the need for integrated ML + multimodal characterization. (decost2022towardsautomateddesign pages 1-4)
- MINERVA demonstrating **five completely different classes of materials** enabled by modular robotics + software orchestration. (hao2025autonomousmaterialssynthesis pages 19-21)
- A community perspective documenting AE campaigns across multiple materials domains and framing platforms as generalizable testbeds. (stach2021autonomousexperimentationsystems pages 6-8)

These precedents support reviewer-facing language: “multiple material demonstrations are standard for proving platform generality, provided the platform is the focus and the demonstrations are scoped as challenge problems.” (decost2022towardsautomateddesign pages 1-4, stach2021autonomousexperimentationsystems pages 6-8)

## Final recommended option among (a)–(d)
**(c) Use Al as Phase I demonstration with Cu–Cr–Zr as Phase I stretch / Phase II target**.

- It best aligns with critical-minerals framing (Mg/REE avoidance), platform maturity and demonstrated induction-heated ultrasonic atomization capability up to ~1300 °C, while containing risk from the missing direct CuCrZr-UA precedent. (bauer20232023criticalmaterials pages 133-136, ukabhai2025investigationofalcu pages 1-3, sojoodi2025integrationofcircular pages 18-19, edwards2025inertialfusionenergy pages 10-12)

- Avoid (d) “parallel” unless you drastically constrain each family to minimal experiments and shared KPIs; otherwise it reads over-scoped for Phase I. (edwards2025inertialfusionenergy pages 10-12, edwards2025inertialfusionenergy pages 5-7)

References

1. (edwards2025inertialfusionenergy pages 10-12): J Edwards, E Draeger, D Flowers, and D Mariscal. Inertial fusion energy mod-sim framework a coordinated initiative for ife design and performance prediction. Unknown journal, 2025.

2. (edwards2025inertialfusionenergy pages 5-7): J Edwards, E Draeger, D Flowers, and D Mariscal. Inertial fusion energy mod-sim framework a coordinated initiative for ife design and performance prediction. Unknown journal, 2025.

3. (decost2022towardsautomateddesign pages 1-4): Brian DeCost, Howie Joress, Suchismita Sarker, Apurva Mehta, and Jason Hattrick-Simpers. Towards automated design of corrosion resistant alloy coatings with an autonomous scanning droplet cell. JOM, 74:2941-2950, Jun 2022. URL: https://doi.org/10.1007/s11837-022-05367-0, doi:10.1007/s11837-022-05367-0. This article has 25 citations and is from a peer-reviewed journal.

4. (stach2021autonomousexperimentationsystems pages 6-8): Eric Stach, Brian DeCost, A. Gilad Kusne, Jason Hattrick-Simpers, Keith A. Brown, Kristofer G. Reyes, Joshua Schrier, Simon Billinge, Tonio Buonassisi, Ian Foster, Carla P. Gomes, John M. Gregoire, Apurva Mehta, Joseph Montoya, Elsa Olivetti, Chiwoo Park, Eli Rotenberg, Semion K. Saikin, Sylvia Smullin, Valentin Stanev, and Benji Maruyama. Autonomous experimentation systems for materials development: a community perspective. Matter, 4:2702-2726, Sep 2021. URL: https://doi.org/10.1016/j.matt.2021.06.036, doi:10.1016/j.matt.2021.06.036. This article has 367 citations and is from a peer-reviewed journal.

5. (bauer20232023criticalmaterials pages 16-18): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

6. (bauer20232023criticalmaterials pages 133-136): Diana Bauer, Helena Khazdozian, Jeremy Mehta, Ruby Nguyen, Michael Severson, Bjorn Vaagensmith, Lionel Toba, Bo Zhang, Tasmin Hossain, Adam Sibal, Braeton Smith, Matthew Riddle, Diane Graziano, Tony Mathew, Patrick Cuscaden, Qiang Dai, Chukwunwike Iloeje, Lesley Edgemon, Caitlyn Sarna, and Julian Quaresima. 2023 critical materials strategy. ArXiv, Jul 2023. URL: https://doi.org/10.2172/1998242, doi:10.2172/1998242. This article has 18 citations.

7. (hayes2018criticalmineralsa pages 1-2): Sarah M. Hayes and Erin A. McCullough. Critical minerals: a review of elemental trends in comprehensive criticality studies. Resources Policy, 59:192-199, Dec 2018. URL: https://doi.org/10.1016/j.resourpol.2018.06.015, doi:10.1016/j.resourpol.2018.06.015. This article has 359 citations and is from a peer-reviewed journal.

8. (czerwinski2024aluminumalloysfor pages 42-43): Frank Czerwinski. Aluminum alloys for electrical engineering: a review. Journal of Materials Science, 59:14847-14892, Aug 2024. URL: https://doi.org/10.1007/s10853-024-09890-0, doi:10.1007/s10853-024-09890-0. This article has 103 citations and is from a peer-reviewed journal.

9. (kahveci2019measurementandprediction pages 1-2): Osman Kahveci, Emin Çadirli, Mehmet Arı, Hicran Tecer, and Mehmet Gündüz. Measurement and prediction of the thermal and electrical conductivity of al-zr overhead line conductors at elevated temperatures. Materials Research, Jan 2019. URL: https://doi.org/10.1590/1980-5373-mr-2018-0513, doi:10.1590/1980-5373-mr-2018-0513. This article has 24 citations.

10. (ukabhai2025investigationofalcu pages 1-3): Kiyaasha Dyal Ukabhai, Donald Mkhonto, and Maje Phasha. Investigation of al-cu using different preparation methods on the amazemet repowder machine. MATEC Web of Conferences, 417:03001, Jan 2025. URL: https://doi.org/10.1051/matecconf/202541703001, doi:10.1051/matecconf/202541703001. This article has 0 citations.

11. (reich2025criticalminerals pages 5-6): Martin Reich and Adam C. Simon. Critical minerals. Annual Review of Earth and Planetary Sciences, Dec 2025. URL: https://doi.org/10.1146/annurev-earth-040523-023316, doi:10.1146/annurev-earth-040523-023316. This article has 47 citations and is from a highest quality peer-reviewed journal.

12. (reich2025criticalminerals pages 1-2): Martin Reich and Adam C. Simon. Critical minerals. Annual Review of Earth and Planetary Sciences, Dec 2025. URL: https://doi.org/10.1146/annurev-earth-040523-023316, doi:10.1146/annurev-earth-040523-023316. This article has 47 citations and is from a highest quality peer-reviewed journal.

13. (morozova2018microstructureandproperties pages 1-2): A. Morozova, R. Mishnev, A. Belyakov, and R. Kaibyshev. Microstructure and properties of fine grained cu-cr-zr alloys after termo-mechanical treatments. REVIEWS ON ADVANCED MATERIALS SCIENCE, 54:56-92, Mar 2018. URL: https://doi.org/10.1515/rams-2018-0020, doi:10.1515/rams-2018-0020. This article has 95 citations and is from a peer-reviewed journal.

14. (ciftcli2025alloydevelopmentfrom pages 1-3): Jakub Ciftcli, Tomasz Choma, Bartosz Morończyk, Bartosz Kalicki, Filip Puchalski, and Łukasz Żrodowski. Alloy development from sustainable materials – close-loop of materials using ultrasonic atomization. Journal of the Japan Society of Powder and Powder Metallurgy, 72:S729-S735, Mar 2025. URL: https://doi.org/10.2497/jjspm.15e-sis13-03, doi:10.2497/jjspm.15e-sis13-03. This article has 4 citations.

15. (sojoodi2025integrationofcircular pages 18-19): Mahyar Sojoodi, Alireza Behvar, Harsh Bajaj, Shiva Mohajerani, Saeedeh Vanaei, Nasrin Taheri Andani, Anwar Algamal, Fatemeh Ghasemibojd, Mahsa Beyk Khorasani, Ahu Celebi, and Mohammad Elahinia. Integration of circular economy into metal additive manufacturing: a review of ultrasonic plasma atomization for producing virgin and recycled niti powder. Shape Memory and Superelasticity, 12:5-45, Oct 2025. URL: https://doi.org/10.1007/s40830-025-00589-y, doi:10.1007/s40830-025-00589-y. This article has 1 citations.

16. (presz2024ultrasonicatomizationas pages 11-12): Wojciech Presz, Rafał Szostak-Staropiętka, Anna Dziubińska, and Katarzyna Kołacz. Ultrasonic atomization as a method for testing material properties of liquid metals. Materials, 17:6109, Dec 2024. URL: https://doi.org/10.3390/ma17246109, doi:10.3390/ma17246109. This article has 6 citations.

17. (edwards2025inertialfusionenergy pages 12-14): J Edwards, E Draeger, D Flowers, and D Mariscal. Inertial fusion energy mod-sim framework a coordinated initiative for ife design and performance prediction. Unknown journal, 2025.

18. (czerwinski2022criticalmineralsfor pages 1-2): Frank Czerwinski. Critical minerals for zero-emission transportation. Materials, 15:5539, Aug 2022. URL: https://doi.org/10.3390/ma15165539, doi:10.3390/ma15165539. This article has 34 citations.

19. (oconnor2025reducedgravityand pages 48-51): A O'Connor, L Littles, B Richter, E Glaessgen, and A Karma. Reduced gravity and microgravity integrated computational materials engineering (icme). Unknown journal, 2025.

20. (hao2025autonomousmaterialssynthesis pages 19-21): Yuze Hao, Lan Duo, and Jinlu He. Autonomous materials synthesis laboratories: integrating artificial intelligence with advanced robotics for accelerated discovery. ChemRxiv, Aug 2025. URL: https://doi.org/10.26434/chemrxiv-2025-fk3r7, doi:10.26434/chemrxiv-2025-fk3r7. This article has 36 citations.

21. (morozova2018microstructureandproperties pages 13-14): A. Morozova, R. Mishnev, A. Belyakov, and R. Kaibyshev. Microstructure and properties of fine grained cu-cr-zr alloys after termo-mechanical treatments. REVIEWS ON ADVANCED MATERIALS SCIENCE, 54:56-92, Mar 2018. URL: https://doi.org/10.1515/rams-2018-0020, doi:10.1515/rams-2018-0020. This article has 95 citations and is from a peer-reviewed journal.

22. (wang2020effectsofminor pages 1-2): Weiyang Wang, Jialun Zhu, Nannan Qin, Yufeng Zhang, Shengyao Li, Zhu Xiao, Qian Lei, and Zhou Li. Effects of minor rare earths on the microstructure and properties of cu-cr-zr alloy. Journal of Alloys and Compounds, 847:155762, Dec 2020. URL: https://doi.org/10.1016/j.jallcom.2020.155762, doi:10.1016/j.jallcom.2020.155762. This article has 156 citations and is from a peer-reviewed journal.

23. (morozova2018microstructureandproperties pages 11-13): A. Morozova, R. Mishnev, A. Belyakov, and R. Kaibyshev. Microstructure and properties of fine grained cu-cr-zr alloys after termo-mechanical treatments. REVIEWS ON ADVANCED MATERIALS SCIENCE, 54:56-92, Mar 2018. URL: https://doi.org/10.1515/rams-2018-0020, doi:10.1515/rams-2018-0020. This article has 95 citations and is from a peer-reviewed journal.