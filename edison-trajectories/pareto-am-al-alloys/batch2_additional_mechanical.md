# Batch2 Additional Mechanical

*Edison Scientific LITERATURE queries for AM Al alloy Pareto front identification*

## Query 1

**Question:** What fatigue strength and fatigue life data have been reported for LPBF aluminum alloys? Compare AlSi10Mg, Scalmalloy, and other systems. Provide S-N curve data or fatigue limits where available.

**Task ID:** `efb5d111-d958-4d98-833b-89b31a11c1a2`

**Status:** complete

## Fatigue strength / fatigue life data reported for LPBF aluminum alloys (emphasis on AlSi10Mg and Scalmalloy)

Reported fatigue properties for LPBF aluminum alloys vary widely with (i) surface condition (as-built vs machined/polished), (ii) defect population (lack-of-fusion vs gas/keyhole porosity; size/location), (iii) post-processing (stress relief, T6/solution+aging, HIP, shot peening), (iv) build orientation, and (v) load ratio R. The extracted datasets below provide (where available) either fatigue limits/strengths at 10^7 cycles (run-out) or explicit S–N points.

### Comparative summary (extracted numeric data)
| Alloy/system | Process (LPBF/SLM) & specimen | Surface condition | Post-processing/heat treatment | Load type | Stress ratio R | Fatigue metric (fatigue limit/strength at 1e7 cycles or S-N points) | Numerical values | Notes (defects/orientation) |
|---|---|---|---|---|---|---|---|---|
| AlSi10Mg | AM-SLM/LPBF; EOSINT M-280; ASTM E466 rotating-beam specimens built in Z direction | Machined and polished (SiC 1200/2500/4000 grit) | As-built baseline; study also examined stress relief and HIP at 250 °C or 500 °C, 180 MPa, 2 h | Rotating-beam fatigue | -1 | Fatigue limit at 1×10^7 cycles | **Sf = 125 MPa at Nf = 1×10^7** for as-built machined/polished condition | SR and HIP reduced fatigue resistance; HIP at 500 °C was worst; fracture controlled by defects/microstructure (uzan2017fatigueofalsi10mg pages 1-6) |
| AlSi10Mg | Laser-based PBF; axial fatigue specimens | Not stated in extracted excerpt | NHT vs HT; HT = solution 500 °C/2 h + quench + age 160 °C/24 h | Fully reversed axial fatigue; Basquin fit used | -1 | Fatigue strength at 10^7 cycles | **NHT ≈ 50 MPa; HT ≈ 80 MPa** | HT improved fatigue life region by ~90%; fractography examples at Sa = 64, 112 MPa (NHT) and 96, 128 MPa (HT); crack initiation usually from single surface defect ~100–150 μm; lack-of-fusion defects important (sajadi2021fatigueimprovementof pages 10-14, sajadi2021fatigueimprovementof pages 8-10) |
| AlSi10Mg | SLM; machined/polished specimens on resonant rig | Machined and polished | As-built vs HIP (+ anneal/aging) | Tension-compression HCF | -1 | Fatigue strength at 1×10^7 cycles, normalized by nominal UTS (Ps = 50%) | **As-built = 0.253 UTS; HIP = 0.288 UTS** (**+14%** with HIP); slope/scatter: AB **12.99**, **1:1.15**; HIP **19.37**, **1:1.06** | Run-out at 1×10^7 cycles; image/table extracted from Fig. 4/Table 2; HIP reduced porosity by ~64% and shifted failure origins from pores to microstructural features (schneller2019effectofhip media 21aae444, schneller2019effectofhip pages 1-3, schneller2019effectofhip pages 3-7, schneller2019effectofhip media 014e7aae, schneller2019effectofhip media e31ac68d) |
| Scalmalloy-class Al-4.5Mg-0.6Sc-0.3Zr | LPBF; literature S-N results summarized within FCG paper | Not specified in excerpt | Untreated vs aged | Constant-amplitude fatigue in cited prior work; present paper mainly FCG | 1 for cited S-N data; 0.1 for FCG tests | Average fatigue strength; limited S-N point range | **Untreated = 51.6 MPa; aged = 126.4 MPa** average fatigue strength; additional cited data: **120–140 MPa** gave **Nf ~10^5** at 20 Hz | Useful mainly as Scalmalloy comparison point; present paper also reports **ΔKth ≈ 1.3–1.4 MPa√m**, Paris **m ≈ 2.9–3.0**, **C ≈ (3–5)×10^-10** (chernyshova2021fatiguecrackgrowth pages 1-2) |
| Al-4.5Mn-1.5Mg-0.9Sc-0.2Zr | LPBF; HCF specimens with defect-size characterization | Not specified in excerpt | As-deposited vs direct aged at 300 °C; HIP also discussed | HCF stress-life testing | Not stated in extracted pages | S-N points; defect-size fatigue model; threshold | Example S-N points: **300 MPa → Nf = 26,909; 40,886; 44,067; 47,189; 43,469; 28,027**; **250 MPa → Nf = 99,411; 120,712; 160,181; 169,887**; **230 MPa → Nf = 460,126; 1,269,524**; **200 MPa → Nf = 1,054,146**. Model: **Δσw = 407·15.67/(√area + 15.67)**. Threshold: **ΔKth = 1.86 MPa√m** | Direct aging raised fatigue strength by **16%** while yield rose **32%**; reported fatigue strengths include **180 MPa** and **220 MPa** in context; HIP fatigue strength mentioned as **340 MPa**; defect sizes √area commonly ~25–90 μm and strongly control life (tang2024multivariaterelationshipsbetween pages 15-16, tang2024multivariaterelationshipsbetween pages 11-13, tang2024multivariaterelationshipsbetween pages 13-14) |
| Al-Ni-Cu | SLM; stress-life data from Table 5/Fig. 9 | Not specified in excerpt | As-printed vs solution 530 °C/1 h + aging 175 °C/6 h | Fatigue test (type not stated in excerpt) | Not stated | S-N points (cycles to failure) | **As-printed:** 33 kg/mm^2 → **26,090** cycles; 56.6 kg/mm^2 → **4,811**; 80.2 kg/mm^2 → **4,936**; 103.7 kg/mm^2 → **2,591**. **Heat-treated:** 33 kg/mm^2 → **6,767**; 56.6 kg/mm^2 → **3,754**; 80.2 kg/mm^2 → **2,436**; 103.7 kg/mm^2 → **1,204** | Heat treatment reduced fatigue resistance despite improving ductility relative to brittle as-printed state; no explicit run-out criterion reported in excerpt (chang2021microstructuremechanicalproperties pages 5-9) |


*Table: This table compares extracted fatigue limits, 10^7-cycle strengths, and representative S-N data for LPBF/SLM aluminum alloys, including AlSi10Mg, Scalmalloy-class alloys, and other systems. It highlights how heat treatment, surface condition, defects, and alloy chemistry affect reported fatigue behavior.*

### AlSi10Mg (LPBF/SLM): endurance limits and 10^7-cycle strengths

* **Machined/polished, Z-build, rotating-beam (R = −1): fatigue limit 125 MPa at 1×10^7 cycles.** Uzan et al. tested Z-built EOSINT M-280 AlSi10Mg specimens machined to ASTM E466 geometry and polished; the as-built (machined/polished) condition had the highest fatigue limit reported in that study (**Sf = 125 MPa at Nf = 1×10^7**). Stress relief (300 °C/2 h) and HIP (250 °C or 500 °C, 180 MPa, 2 h) reduced fatigue resistance, with HIP at 500 °C being most detrimental (uzan2017fatigueofalsi10mg pages 1-6).

* **Axial fully reversed (R = −1): 10^7-cycle fatigue strength ~50 MPa (NHT) vs ~80 MPa (HT).** Sajadi et al. fit Basquin relations and report fatigue strength at **10^7 cycles ≈ 50 MPa** for non-heat-treated (NHT) specimens and **≈ 80 MPa** after solution+aging heat treatment (500 °C/2 h + quench + 160 °C/24 h). Their fractography indicates crack initiation often from a single surface defect (~100–150 μm), with lack-of-fusion features also serving as initiators (sajadi2021fatigueimprovementof pages 8-10).

* **Axial HCF run-out 1×10^7 cycles, R = −1 (machined/polished): HIP improves normalized fatigue strength by ~14%.** Schneller et al. report statistically evaluated fatigue strength at **1×10^7 cycles** for machined/polished SLM AlSi10Mg using normalization to a nominal UTS (manufacturer value). For 50% survival probability, fatigue strength increased from **0.253·UTS (as-built)** to **0.288·UTS (HIP)** (≈+14%), with S–N curve slope and scatter also reported; Figure 4/Table 2 containing these values were extracted as images (schneller2019effectofhip pages 3-7, schneller2019effectofhip media 014e7aae, schneller2019effectofhip media e31ac68d).

Interpretation: across AlSi10Mg studies, absolute values differ substantially because “as-built” may include different surface states, defect populations, and load types; nonetheless, the extracted evidence consistently indicates that (i) removing surface roughness (machining/polishing) is critical for reaching higher endurance limits, and (ii) HIP can improve HCF strength when surface effects are minimized, primarily via porosity reduction (uzan2017fatigueofalsi10mg pages 1-6, schneller2019effectofhip pages 3-7).

### Scalmalloy / Al–Mg–Sc–Zr (LPBF): reported fatigue strengths (limited extracted S–N data)

Direct S–N curve datasets for Scalmalloy were less accessible in the retrieved full texts; however, one LPBF Scalmalloy-class (Al-4.5Mg-0.6Sc-0.3Zr) crack-growth paper reports *literature* S–N results:

* **Average fatigue strength increases markedly with aging (R = 1, cited results): 51.6 MPa → 126.4 MPa.** Chernyshova et al. summarize prior work (Schneller et al., as cited therein) indicating an average fatigue strength (stress amplitude) of **51.6 MPa** for untreated LPBF Scalmalloy and **126.4 MPa** after an aging step. The same source cites limited constant-amplitude fatigue tests at **120–140 MPa** giving failure lives near **10^5 cycles** (R = 1, 20 Hz) (chernyshova2021fatiguecrackgrowth pages 1-2).

* **Complementary fatigue crack growth (FCG) resistance:** Chernyshova et al. report thresholds and Paris-law parameters for Scalmalloy-class LPBF material (useful when S–N data are absent): **ΔKth ≈ 1.3–1.4 MPa√m**, with Paris parameters **m ≈ 2.9–3.0** and **C ≈ (3–5)×10^−10** (chernyshova2021fatiguecrackgrowth pages 1-2).

Interpretation: while not a full HCF endurance-limit dataset, the extracted evidence supports that precipitation/aging heat treatments can be decisive for Scalmalloy fatigue strength (chernyshova2021fatiguecrackgrowth pages 1-2).

### Other LPBF aluminum systems with reported S–N data or fatigue-limit models

* **LPBF Al–Mn–Sc–Zr (Al-4.5Mn-1.5Mg-0.9Sc-0.2Zr): explicit σ–Nf points and defect-based fatigue limit model.** Tang et al. provide multiple stress–life points, e.g. **300 MPa → Nf ≈ 2.7×10^4–4.7×10^4**, **250 MPa → Nf ≈ 1.0×10^5–1.7×10^5**, **230 MPa → Nf = 4.6×10^5 and 1.27×10^6**, and **200 MPa → Nf ≈ 1.05×10^6** (tang2024multivariaterelationshipsbetween pages 13-14, tang2024multivariaterelationshipsbetween pages 11-13). They also report an explicit defect-size model for fatigue limit/stress range: **Δσw = 407·15.67/(√area + 15.67)** and a long-crack threshold **ΔKth = 1.86 MPa√m**, within an El-Haddad/Murakami framework (tang2024multivariaterelationshipsbetween pages 15-16). A HIP condition is mentioned with **fatigue strength 340 MPa** (tang2024multivariaterelationshipsbetween pages 13-14).

* **SLM Al–Ni–Cu: tabulated S–N points (cycles to failure).** Chang et al. report S–N points for an SLM Al–Ni–Cu alloy in as-printed and solution+aged states. Example points: as-printed **33 kg/mm^2 → Nf 26,090** and **103.7 kg/mm^2 → Nf 2,591**, while after 530 °C/1 h + 175 °C/6 h **33 kg/mm^2 → Nf 6,767** and **103.7 kg/mm^2 → Nf 1,204**, indicating reduced fatigue resistance after this heat treatment (chang2021microstructuremechanicalproperties pages 5-9).

### Key cross-alloy comparison points and caveats

1. **AlSi10Mg has the most robust extracted HCF endurance data at 10^7 cycles**, spanning ~50–125 MPa (depending on specimen state and test type) and also providing HIP improvements expressed in normalized form when absolute UTS is not provided (uzan2017fatigueofalsi10mg pages 1-6, sajadi2021fatigueimprovementof pages 8-10, schneller2019effectofhip pages 3-7).
2. **Scalmalloy fatigue S–N values were only available indirectly** in the accessible full text (as literature values embedded in a crack-growth study). The extracted evidence still supports large improvements from aging (chernyshova2021fatiguecrackgrowth pages 1-2). A fuller Scalmalloy comparison would require direct access to primary Scalmalloy S–N papers (e.g., surface-condition studies) that were retrieved as metadata but not available with extractable S–N numbers in the current corpus.
3. **Newer microalloyed systems (e.g., Al–Mn–Sc–Zr) increasingly report defect-sensitive models and σ–N points** rather than only a single endurance limit, enabling more transferable design allowables when coupled to defect characterization (tang2024multivariaterelationshipsbetween pages 13-14, tang2024multivariaterelationshipsbetween pages 15-16).

### Visual evidence for an AlSi10Mg S–N curve

Schneller et al. present an S–N curve and Table 2 for machined/polished AlSi10Mg comparing as-built vs HIPed conditions, including the normalized fatigue strength at 1×10^7 cycles; the extracted figure/table crops are available here (schneller2019effectofhip media 014e7aae, schneller2019effectofhip media e31ac68d).


---

## Query 2

**Question:** What fracture toughness (KIC or JIC) values have been measured for LPBF aluminum alloys? Provide quantitative data across different alloy systems and conditions (as-built vs heat-treated).

**Task ID:** `71f9166e-309d-4d17-bcfd-a48098c18e5b`

**Status:** complete

## Fracture toughness measurements for LPBF aluminum alloys (KIC and JIC/JIc)

This synthesis compiles **experimentally measured** fracture-toughness values reported for **laser powder bed fusion (LPBF)/selective laser melting (SLM) aluminum alloys**, emphasizing **quantitative KIC and/or JIC (JIc)** values and explicitly distinguishing **as-built vs heat-treated** conditions where reported.

### Summary table of quantitative values

| Alloy (system) | AM process | Condition | Orientation / crack geometry | Toughness metric and value | Notes on test standard / method / caveats |
|---|---|---|---|---|---|
| AlSi10Mg | LPBF | Process-parameter study; no post-heat-treatment stated for LPBF batches | XZ (crack propagating parallel to build direction) | **K<sub>JIc</sub> = 23.8–30.9 MPa√m**; highest explicitly reported case **30.9 ± 0.3 MPa√m** with **J<sub>Ic</sub> = 11.2 ± 0.2 kJ/m²** for 30LT/190HS/67SS-XZ | ASTM E1820-based J approach; K derived from J. Table 3 also reports CTOD. Values are size-independent **K<sub>JIc</sub>**, not ASTM E399 plane-strain K<sub>IC</sub>. (paul2021fractureresistanceof pages 7-8, shah2025influenceofmicrob pages 52-55, paul2021fractureresistanceof media 81b7c6d0) |
| AlSi10Mg | LPBF | Process-parameter study; no post-heat-treatment stated for LPBF batches | ZX (crack propagating perpendicular to build direction) | **K<sub>JIc</sub> = 19.5–25.5 MPa√m**; lowest explicitly reported LPBF case **19.5 ± 1.8 MPa√m** with **J<sub>Ic</sub> = 4.5 ± 0.8 kJ/m²** for 30LT/100HS/90SS (0D)-ZX | ASTM E1820-based J approach; K derived from J. Orientation dependence is explicit, with lower toughness in ZX than XZ. (paul2021fractureresistanceof pages 7-8, shah2025influenceofmicrob pages 52-55, paul2021fractureresistanceof pages 10-12, paul2021fractureresistanceof media 81b7c6d0) |
| AlSi10Mg | LPBF | Process-parameter study; no post-heat-treatment stated for LPBF batches | 67° scan strategy, XZ vs ZX | **K<sub>JIc</sub> ≈ 30 MPa√m (XZ)** and **≈ 23–25 MPa√m (ZX)** | Reported as process/orientation-specific summary from the same Acta Mater. study; scan strategy strongly influences toughness anisotropy. (paul2021fractureresistanceof pages 12-13) |
| AlSi10Mg | LPBF | Process-parameter study; no post-heat-treatment stated for LPBF batches | 90° scan strategy, XZ vs ZX | **K<sub>JIc</sub> = 24–27 MPa√m (XZ)** and **19–25 MPa√m (ZX)** | 90SS batch showed strongest orientation effect and among the lowest toughness values. (paul2021fractureresistanceof pages 10-12) |
| AlSi10Mg | Cast reference | T6 cast reference (not AM, included only as comparator used in the LPBF study) | Not stated | **J<sub>Ic</sub> = 3.7 ± 0.4 kJ/m²**; **K<sub>JIc</sub> = 18.6 ± 1.1 MPa√m** | Comparator from the same study; not LPBF, but useful benchmark. (paul2021fractureresistanceof pages 7-8, paul2021fractureresistanceof pages 5-7) |
| AlSi10Mg | SLM / LPBF | Configuration-dependent, effectively different in-situ aging states; no named T5/T6/HIP treatment labels | Configurations a-f; f is in-build (90°) oriented | **K<sub>IC</sub> = 59.06 ± 1.430, 51.60 ± 1.794, 58.03 ± 1.321, 55.79 ± 3.614, 50.76 ± 1.917, 40.63 ± 1.247 MPa√m** for configurations a-f, respectively | Authors cite ASTM E399-08 in discussion of pre-crack/fixation geometry. Values are configuration-specific and may reflect different in-situ age-hardening states rather than conventional post-heat treatments. (hitzler2019fracturetoughnessof pages 4-6, hitzler2019fracturetoughnessof pages 6-7) |
| AlSi10Mg | SLM | Not explicitly stated (specimen series with printing plane orthogonal to crack plane) | H1-H3; printing plane orthogonal to crack plane | **J<sub>Ic</sub> = 11.2, 11.2, 11.3 N/mm**; average **11.2 N/mm**; corresponding **K<sub>IC</sub> = 29.2 MPa√m** | Trovato reports JIc and converts to KIc using **E = 70 GPa** and **ν = 0.3**. Condition (as-built vs polished) not explicit in the extracted evidence. (trovato2018validationofthe pages 47-54) |
| AlSi10Mg | SLM | Not explicitly stated (specimen series with growth/printing plane parallel to crack plane) | V1-V3; growth/printing plane parallel to crack plane | **J<sub>Ic</sub> = 7.9, 7.3, 10.9 N/mm** | Same Trovato study; excerpt gives JIc values but no converted KIc for the V series in the extracted evidence. (trovato2018validationofthe pages 47-54) |
| A357 / AlSi7Mg | LPBF | As-built (AB) | Y-X | **J<sub>Ic</sub> = 14.83 kJ/m²** | ASTM E1820-20b cited in the paper; J-R curve method used. (menezes2022effectofheat pages 8-10, menezes2022effectofheat pages 10-12) |
| A357 / AlSi7Mg | LPBF | As-built (AB) | Z-X | **J<sub>Ic</sub> = 4.10 kJ/m²** | Lowest AB orientation in this study. ASTM E1820-20b cited. (menezes2022effectofheat pages 8-10, menezes2022effectofheat pages 10-12) |
| A357 / AlSi7Mg | LPBF | As-built (AB) | Y-Z | **J<sub>Ic</sub> = 12.23 kJ/m²** | ASTM E1820-20b cited. (menezes2022effectofheat pages 8-10, menezes2022effectofheat pages 10-12) |
| A357 / AlSi7Mg | LPBF | T5 | Y-X | **J<sub>Ic</sub> = 8.88 kJ/m²** | Direct-aged condition from Table 5. (menezes2022effectofheat pages 8-10) |
| A357 / AlSi7Mg | LPBF | T5 | Z-X | **J<sub>Ic</sub> = 2.75 kJ/m²** | Lowest value in the A357 heat-treatment/orientation matrix. (menezes2022effectofheat pages 8-10) |
| A357 / AlSi7Mg | LPBF | T5 | Y-Z | **J<sub>Ic</sub> = 7.31 kJ/m²** | Table 5 value. (menezes2022effectofheat pages 8-10) |
| A357 / AlSi7Mg | LPBF | T6 | Y-X | **J<sub>Ic</sub> = 4.77 kJ/m²** | T6 reduced anisotropy but also gave the lowest average strength-toughness combination. (menezes2022effectofheat pages 8-10, menezes2022effectofheat pages 10-12) |
| A357 / AlSi7Mg | LPBF | T6 | Z-X | **J<sub>Ic</sub> = 4.38 kJ/m²** | Table 5 value. (menezes2022effectofheat pages 8-10) |
| A357 / AlSi7Mg | LPBF | T6 | Y-Z | **J<sub>Ic</sub> = 4.03 kJ/m²** | Table 5 value. (menezes2022effectofheat pages 8-10) |
| Al-Mg-Sc-Zr | SLM / LPBF | Aged **320 °C × 4 h** | 0° CT specimen | **K<sub>IC</sub> = 21.41 ± 0.19 MPa√m** | CT fracture-toughness specimens; paper reports small anisotropy after aging. Test used CT geometry; exact ASTM standard not extracted. (邹君2024激光选区熔化almgsczr合金各向组织与损伤容限性能 pages 1-4, 邹君2024激光选区熔化almgsczr合金各向组织与损伤容限性能 pages 4-7) |
| Al-Mg-Sc-Zr | SLM / LPBF | Aged **320 °C × 4 h** | 90° CT specimen | **K<sub>IC</sub> = 20.89 ± 0.31 MPa√m** | About 2.5% lower than 0° CT orientation; attributed to lower crack-propagation resistance in columnar-grain regions and defect effects. (邹君2024激光选区熔化almgsczr合金各向组织与损伤容限性能 pages 1-4, 邹君2024激光选区熔化almgsczr合金各向组织与损伤容限性能 pages 4-7) |
| AlSi10Mg | LPBF | Stress-relieved (SR) only | Z and XY orientations (not fully resolved numerically) | **K<sub>c</sub> = 31–39 MPa√m** | Dissertation evidence states LEFM validity not achieved; therefore values are reported as catastrophic-fracture-regime **Kc**, not valid ASTM E399 KIC. Single test per condition/orientation. (ngo2020effectsofbuild pages 110-115) |
| AlSi10Mg | LPBF | SR + T6 | Z and XY orientations (not fully resolved numerically) | **K<sub>c</sub> = 23–27 MPa√m** | Same caveat: not valid plane-strain KIC; LEFM conditions not met. (ngo2020effectsofbuild pages 110-115) |
| AlSi10Mg | LPBF | SR only | Z and XY orientations (not fully resolved numerically) | **Tearing modulus T = 14–18** | Included because the source reports elastic-plastic fracture behavior when LEFM validity failed; not directly KIC/JIC. (ngo2020effectsofbuild pages 110-115) |
| AlSi10Mg | LPBF | SR + T6 | Z and XY orientations (not fully resolved numerically) | **Tearing modulus T = 0–1.6** | Same caveat as above. (ngo2020effectsofbuild pages 110-115) |
| AlSi10Mg | LPBF | SR + HIP + T6 | Z and XY orientations (not fully resolved numerically) | **Tearing modulus T = 4.4–5.2** | Same caveat as above; source did not explicitly list Kc for SR+HIP+T6 in the excerpt. (ngo2020effectsofbuild pages 110-115) |
| AlSi10Mg | LPBF | Heat-treated (direct aged in Lupi 2024 study) | H / V / D | **J<sub>mat</sub> = 9.9 / 5.5 / 4.0 N/mm** | Table 4 in the paper. Useful orientation/heat-treatment comparison, but extracted evidence does **not** confirm these as ASTM E1820-compliant **JIc** values. (lupi2024fracturetoughnessof pages 6-8, lupi2024fracturetoughnessof pages 12-15) |
| AlSi10Mg | LPBF | As-built (AB) | H / V / D | **J<sub>mat</sub> = 9.1 / 4.3 / 3.5 N/mm** | Same caveat as above: reported as **Jmat**, not explicitly confirmed in the extracted evidence to be ASTM E1820 JIc. (lupi2024fracturetoughnessof pages 6-8, lupi2024fracturetoughnessof pages 12-15) |


*Table: This table summarizes explicit KIC, KJIc, JIc, and related fracture-toughness values reported for LPBF/SLM aluminum alloys across alloy systems, orientations, and conditions. It is useful for comparing as-built versus heat-treated behavior and for distinguishing valid J-based toughness values from less rigorous or non-plane-strain metrics.*

### Key quantitative findings by alloy system and condition

#### 1) AlSi10Mg (LPBF): J-based fracture toughness (ASTM E1820 approach) and converted KJIc

Paul et al. (Acta Materialia 2021) provide a size-insensitive **J-integral initiation toughness JIc** and the corresponding **KJIc** (converted via J–K equivalence) for LPBF AlSi10Mg across process-parameter sets and orientations. In their dataset, **XZ** (crack growth parallel to build direction) consistently exceeds **ZX** (perpendicular to build direction). The reported extremes include **JIc = 11.2 ± 0.2 kJ/m², KJIc = 30.9 ± 0.3 MPa√m** (high toughness case) and **JIc = 4.5 ± 0.8 kJ/m², KJIc = 19.5 ± 1.8 MPa√m** (low toughness case). (paul2021fractureresistanceof pages 7-8, paul2021fractureresistanceof media 81b7c6d0)

Orientation and scan strategy effects are explicitly quantified: for a 90° scan-strategy batch, the paper reports **KJIc ranges of 19–25 MPa√m (ZX)** versus **24–27 MPa√m (XZ)**, indicating stronger anisotropy in this scan strategy. (paul2021fractureresistanceof pages 10-12)

As a benchmark comparator in the same study (not LPBF), the authors report a **cast-T6 reference** with **JIc = 3.7 ± 0.4 kJ/m²** and **KJIc = 18.6 ± 1.1 MPa√m**. (paul2021fractureresistanceof pages 7-8)

*Note:* these are **J-derived toughness values (KJIc)** rather than ASTM E399-valid plane-strain KIC. (paul2021fractureresistanceof pages 2-3)

#### 2) AlSi10Mg (SLM/LPBF): KIC values reported under ASTM E399 framing (configuration-dependent)

Hitzler et al. report **KIC** values for SLM AlSi10Mg spanning **40.63 ± 1.247 to 59.06 ± 1.430 MPa√m** across six build/configuration cases (a–f), with one configuration (f) showing notably lower toughness (~40 MPa√m). The paper references ASTM E399-08 (fracture toughness / precrack geometry context) and interprets variation as partly arising from differing thermal histories / in-situ aging states during fabrication rather than a controlled post-build heat treatment (e.g., no explicit T5/T6 labels in the extracted text). (hitzler2019fracturetoughnessof pages 4-6, hitzler2019fracturetoughnessof pages 6-7)

*Important caveat:* these KIc values are much higher than the size-insensitive KJIc values in Paul et al.; the literature also notes that some 40–60 MPa√m reports can be inflated by specimen size effects and/or non-ideal precracking. (paul2022mechanicalanisotropyina pages 71-75)

#### 3) AlSi10Mg (SLM): JIc reported in N/mm with explicit conversion to KIc

Trovato (2018) reports **JIc** for SLM AlSi10Mg in **N/mm** (equivalently kJ/m²) and explicitly converts to **KIc** using **E = 70 GPa** and **ν = 0.3**. For specimens with **printing plane orthogonal to the crack plane (H1–H3)**, **JIc ≈ 11.2 N/mm** (11.2, 11.2, 11.3 N/mm; average 11.2 N/mm) and the corresponding **KIc = 29.2 MPa√m** is stated. For specimens with **growth/printing plane parallel to the crack plane (V1–V3)**, **JIc = 7.9, 7.3, 10.9 N/mm** is reported (no KIc conversion for V-series shown in the extracted evidence). (trovato2018validationofthe pages 47-54)

#### 4) A357 / AlSi7Mg (LPBF): JIc for as-built vs T5 vs T6, with strong orientation dependence

de Menezes et al. (International Journal of Fracture 2022) report **JIc (kJ/m²)** for LPBF A357 (AlSi7Mg) across **as-built (AB)**, **T5**, and **T6** states, and across multiple crack orientations (Y–X, Z–X, Y–Z). The full matrix from their Table 5 is:

- **As-built (AB):** Y–X **14.83**, Z–X **4.10**, Y–Z **12.23** kJ/m²  
- **T5:** Y–X **8.88**, Z–X **2.75**, Y–Z **7.31** kJ/m²  
- **T6:** Y–X **4.77**, Z–X **4.38**, Y–Z **4.03** kJ/m²  

In this dataset, the **lowest measured value** is **T5, Z–X: JIc = 2.75 kJ/m²**, and T6 reduces anisotropy (values cluster near ~4–5 kJ/m² across orientations). (menezes2022effectofheat pages 8-10)

The authors cite ASTM E1820-20b for fracture-toughness measurement. (menezes2022effectofheat pages 10-12)

#### 5) Al–Mg–Sc–Zr (SLM/LPBF): KIC after aging heat treatment

A Chinese-language study reports **compact-tension (CT) KIC** values for an SLM Al–Mg–Sc–Zr alloy after an **aging treatment of 320 °C × 4 h**. Reported values are **KIC = (21.41 ± 0.19) MPa√m** for **0° CT** specimens and **KIC = (20.89 ± 0.31) MPa√m** for **90° CT** specimens (≈2.5% lower at 90°). (邹君2024激光选区熔化almgsczr合金各向组织与损伤容限性能 pages 1-4, 邹君2024激光选区熔化almgsczr合金各向组织与损伤容限性能 pages 4-7)

### Notes on evidence coverage and limitations

- The clearest **as-built vs heat-treated** fracture-toughness datasets in the retrieved evidence are for **LPBF A357/AlSi7Mg (AB, T5, T6)** and for **SLM Al–Mg–Sc–Zr (aged)**. (menezes2022effectofheat pages 8-10, 邹君2024激光选区熔化almgsczr合金各向组织与损伤容限性能 pages 1-4)
- For **AlSi10Mg**, the highest-confidence, size-insensitive values are the **J-based JIc/KJIc** values reported under ASTM E1820 methodology (Paul et al.). (paul2021fractureresistanceof pages 7-8, paul2021fractureresistanceof media 81b7c6d0)
- Some sources report **Kc** (not valid KIC) or other fracture metrics when LEFM validity was not met; these were retained only with explicit caveats and not treated as plane-strain KIC. (ngo2020effectsofbuild pages 110-115)

Overall, published LPBF aluminum fracture-toughness measurements span roughly **JIc ≈ 2.75–14.83 kJ/m²** for LPBF A357 across AB/T5/T6 and orientations, and **K values from ~19.5 to ~30.9 MPa√m** for size-insensitive LPBF AlSi10Mg (KJIc), with additional SLM reports of KIC ranging from **~20–21 MPa√m (aged Al–Mg–Sc–Zr)** up to **~40–59 MPa√m** in some configuration-dependent AlSi10Mg datasets (with caveats about methodology/size effects). (menezes2022effectofheat pages 8-10, paul2021fractureresistanceof pages 7-8, hitzler2019fracturetoughnessof pages 4-6, 邹君2024激光选区熔化almgsczr合金各向组织与损伤容限性能 pages 1-4)

---

## Query 3

**Question:** What Vickers or Brinell hardness values have been reported for different LPBF aluminum alloys? Provide comparative data across AlSi10Mg, Scalmalloy, Al-Cu, Al-Zn-Mg-Cu, Al-Ce, and other systems.

**Task ID:** `fd482a11-0ead-406f-bf45-a5db1658a5b8`

**Status:** complete *(initially timed out; results retrieved in subsequent session)*

Reported hardness values for LPBF aluminum alloys (Vickers/Brinell)

The literature reports hardness for LPBF aluminum alloys predominantly as Vickers microhardness (HV with specified loads such as HV0.1, HV1, etc.), with fewer Brinell hardness (HB/HBW) datasets. Because hardness depends strongly on post-processing (e.g., T6 vs direct aging vs stress relief) and indentation load (indentation size effect), the most defensible comparison is to tabulate reported values without converting between HV and HB unless explicitly provided.

Comparative dataset

| Alloy/system | Composition/details (if stated) | Condition | Hardness scale & load | Reported hardness value | Notes | Citation IDs |
|---|---|---|---|---|---|---|
| AlSi10Mg / Al10SiMg | Al10SiMg, pulsed LPBF | As-built | HV0.1 (100 gf, 10 s) | 136 HV | Mean of 20 indents | (chou2017microstructureandmechanical pages 1-2) |
| AlSi10Mg | LPBF AM sample | As-produced | HB | ~125 HB | Approximate from extracted Figure 5 | (tonolini2021wearbehaviorof media 0e4d9db5) |
| AlSi10Mg | LPBF AM sample | T6 | HB | 110.1 ± 1.1 HB | Figure 5 / text excerpt | (tonolini2021wearbehaviorof pages 8-14, tonolini2021wearbehaviorof media 0e4d9db5) |
| AlSi10Mg | SLM/LPBF, Italian batches | As-built / stress-relieved | HBW | Perpendicular face ~103.30 ± 2 to 109.61 ± 1 HBW; parallel face ~81.66 ± 6 to 92.73 ± 3 HBW | Orientation-dependent; mixed batches/conditions | (marinelli2018mechanicalcharacterizationand pages 79-83) |
| AlSi10Mg | LPBF scan-strategy study | As-built | Hv (load not stated) | 144 ± 2.2 Hv | Highest value with spiral scan, 110 µm hatch spacing | (dejene2025effectsofscanning pages 8-10) |
| AlSi10Mg | LPBF heat-treatment study | As-built | HV (load not stated in excerpt) | 96.7 ± 4.01 HV | Mean of three measurements | (megahed2022effectofheat pages 7-11) |
| AlSi10Mg | LPBF heat-treatment study | HT2 | HV (load not stated in excerpt) | 61.2 HV | Other HT conditions shown in figure but not numerically quoted | (megahed2022effectofheat pages 7-11) |
| Scalmalloy | Al-Mg-Sc-Zr | As-built | HV1 | 104 ± 2 HV1 | Value listed in review table of as-built LPBF Scalmalloy | (cerri2024mainheattreatments pages 5-7) |
| Scalmalloy | Al-Mg-Sc-Zr | As-built | HV0.5 | 80 HV0.5 | Value listed in review table | (cerri2024mainheattreatments pages 5-7) |
| Scalmalloy | Al-Mg-Sc-Zr | As-built | HV0.025 | 104 ± 7 HV0.025 | Average along sample | (ghio2025laserpowderbedfused pages 10-13) |
| Scalmalloy | Al-Mg-Sc-Zr | Direct aged | HV0.025 | 170 ± 10 HV0.025 | Reference DA condition | (ghio2025laserpowderbedfused pages 10-13) |
| Scalmalloy | Al-Mg-Sc-Zr | Aging at 275 °C | HV0.5 | 106 ± 4 to 172 ± 2 HV0.5 | Peak at 128 h | (ghio2025laserpowderbedfused pages 10-13) |
| Scalmalloy | Al-Mg-Sc-Zr | Aging at 325 °C | HV0.5 | 165–171 HV0.5 | Stable post-peak plateau | (ghio2025laserpowderbedfused pages 10-13) |
| Scalmalloy | Al-Mg-Sc-Zr | Aging at 400 °C | HV0.5 | Peak 165 ± 2 HV0.5; 100 ± 2 HV0.5 after 256 h | Overaging at long times | (ghio2025laserpowderbedfused pages 10-13) |
| Scalmalloy | Al-Mg-Sc-Zr | As-built | HV (load not stated) | 105 HV | Low-power LPBF study | (martucci2022lowpowerlaserpowder pages 11-13) |
| Scalmalloy | Al-Mg-Sc-Zr | Heat treated | HV (load not stated) | 162 HV | Same low-power LPBF study | (martucci2022lowpowerlaserpowder pages 9-11) |
| Scalmalloy | Al-Mg-Sc-Zr | Heat treated | HV0.3 | 168.5 HV0.3 | Process-parameter study | (niedermeyer2026processparameterdevelopment pages 8-10) |
| AlSi10Mg + 4Cu | LPBF AlSi10Mg with 4 wt% Cu | Peak aged, 160 °C for 16 h | HV (load not stated) | >180 HV | Peak microhardness; explicit lower bound only | (martin2021effectofthe pages 1-2) |
| AlSi10Mg + 4Cu | LPBF AlSi10Mg with 4 wt% Cu | Overaged, 180 °C for 12 h | HV (load not stated) | 167 HV | Cu-modified alloy | (martin2021effectofthe pages 9-11) |
| AlSi10Mg (control) | LPBF AlSi10Mg without Cu | Aged, 160 °C for 16 h | HV (load not stated) | 140 ± 6 HV | Control in Cu-addition study | (martin2021effectofthe pages 9-11) |
| A2024 + LaB6 | PBF-LB/M A2024 with 0 wt.% LaB6 (S0) | As-built | HV0.2 | 75.6 ± 3.6 HV0.2 | Baseline alloy | (yao2024verificationofthe pages 7-9) |
| A2024 + LaB6 | PBF-LB/M A2024 with 0.25 wt.% LaB6 (S0.25) | As-built | HV0.2 | 109.1 ± 4.2 HV0.2 | LaB6-modified | (yao2024verificationofthe pages 7-9) |
| A2024 + LaB6 | PBF-LB/M A2024 with 0.5 wt.% LaB6 (S0.5) | As-built | HV0.2 | 124.2 ± 4.4 HV0.2 | LaB6-modified | (yao2024verificationofthe pages 7-9) |
| A2024 + LaB6 | PBF-LB/M A2024 with 0.75 wt.% LaB6 (S0.75) | As-built | HV0.2 | 130.6 ± 4.3 HV0.2 | LaB6-modified | (yao2024verificationofthe pages 7-9) |
| A2024 + LaB6 | PBF-LB/M A2024 with 1.0 wt.% LaB6 (S1) | As-built | HV0.2 | 135.0 ± 3.3 HV0.2 | Highest hardness in series | (yao2024verificationofthe pages 7-9) |
| TiB2-Al2618 | LPBF TiB2-reinforced Al-2618 | As-built | HV (load not stated) | 122 ± 5 HV | Thin-wall study | (lupi2025microstructureandtensile pages 8-11) |
| TiB2-Al2618 | LPBF TiB2-reinforced Al-2618 | Solution treated 530 °C, 0 h | HV (load not stated) | 105 ± 3 HV | Hardness drop after ST | (lupi2025microstructureandtensile pages 8-11) |
| TiB2-Al2618 | LPBF TiB2-reinforced Al-2618 | ST + WQ + age 160 °C, 4 h | HV (load not stated) | 133 ± 1 HV | Near peak-aged | (lupi2025microstructureandtensile pages 8-11) |
| TiB2-Al2618 | LPBF TiB2-reinforced Al-2618 | ST + WQ + age 180 °C, 1 h | HV (load not stated) | 134 ± 1 HV | Peak at 180 °C route | (lupi2025microstructureandtensile pages 8-11) |
| TiB2-Al2618 | LPBF TiB2-reinforced Al-2618 | Direct aging (T5) 180 °C, 4 h | HV (load not stated) | 134 ± 4 HV | Direct-aged condition | (lupi2025microstructureandtensile pages 8-11) |
| Al-Zn-Mg-Cu-Zr | High-strength LPBF alloy | As-built XY | HV0.1 | 140 ± 8 HV0.1 | XY plane | (chambrin2023influenceofheat pages 4-7) |
| Al-Zn-Mg-Cu-Zr | High-strength LPBF alloy | As-built XZ | HV0.1 | 143 ± 8 HV0.1 | XZ plane | (chambrin2023influenceofheat pages 4-7) |
| Al-Zn-Mg-Cu-Zr | High-strength LPBF alloy | Natural aged, 5 months | HV0.1 | 157 ± 10 HV0.1 | XZ reported explicitly | (chambrin2023influenceofheat pages 4-7) |
| Al-Zn-Mg-Cu-Zr | High-strength LPBF alloy | As-quenched | HV0.1 | 126 ± 4 HV0.1 | After solution + quench | (chambrin2023influenceofheat pages 7-11) |
| Al-Zn-Mg-Cu-Zr | High-strength LPBF alloy | T5, 120 °C | HV0.1 | 160 ± 13 HV0.1 | Peak after 30 h | (chambrin2023influenceofheat pages 7-11) |
| Al-Zn-Mg-Cu-Zr | High-strength LPBF alloy | T6 | HV0.1 | 218 ± 11 HV0.1 | Peak after 20 h | (chambrin2023influenceofheat pages 7-11) |
| Al-Si-Zn-Mg-Cu / “50% 7075” | LPBF mix of AlSi10Mg + 7075 powders | As-built | HV | 135.8 HV | Aversa Table 5 | (aversa2022laserpowderbed pages 9-11) |
| Al-Si-Zn-Mg-Cu / “50% 7075” | LPBF mix of AlSi10Mg + 7075 powders | Stress relieved, 300 °C 2 h | HV | 73.4 HV | Large drop after SR | (aversa2022laserpowderbed pages 9-11) |
| Al-Si-Zn-Mg-Cu / “50% 7075” | LPBF mix of AlSi10Mg + 7075 powders | Aged, 170 °C 3 h | HV | 148.8 HV | Aversa Table 5 | (aversa2022laserpowderbed pages 9-11) |
| Al-Si-Zn-Mg-Cu / “50% 7075” | LPBF mix of AlSi10Mg + 7075 powders | Aged, 160 °C 6 h | HV | 152.9 HV | Aversa Table 5 | (aversa2022laserpowderbed pages 9-11) |
| Si-modified 7075 | 4% Si-modified 7075 | As-built | HV | 160.0 HV | LPBF 7xxx-like alloy | (aversa2022laserpowderbed pages 9-11) |
| Si-modified 7075 | 4% Si-modified 7075 | Aged, 150 °C 6 h | HV | 171.0 HV | LPBF 7xxx-like alloy | (aversa2022laserpowderbed pages 9-11) |
| AlCe10MgSi | LPBF Al-Ce-Mg-Si | As-built, low VED | HV1 | 170 ± 5.2 HV1 | Lower VED condition | (hesselmann2022effectofprecipitationforming pages 7-9) |
| AlCe10MgSi | LPBF Al-Ce-Mg-Si | As-built, high VED | HV1 | 214 ± 11.6 HV1 | Higher VED condition | (hesselmann2022effectofprecipitationforming pages 7-9) |
| Al-15%Fe | Hypereutectic LPBF Al-Fe binary alloy | As-built | HV0.2 | ~210 HV0.2 | Scattered but mostly near 210; approximate from text summary | (wang2021processabilityandoptimization pages 12-15) |
| Al-15%Fe | Hypereutectic LPBF Al-Fe binary alloy | As-built / threshold densification condition | HV1 | ~210 HV1 | Approximate at P·v−1/2 ≈ 140 W·s1/2·m−1/2; slightly lower above threshold | (wang2021processabilityandoptimization pages 12-15) |


*Table: This table compiles reported Vickers and Brinell hardness values for major LPBF/PBF-LB aluminum alloy families across as-built and heat-treated conditions. It is useful for direct cross-alloy comparison while preserving test scale, load, and condition-specific caveats.*

Key cross-alloy comparisons (selected highlights)

1) AlSi10Mg (benchmark Al–Si–Mg)

As-built LPBF Al10SiMg (pulsed LPBF) is reported at 136 HV using a 100 gf Vickers load (HV0.1), mean of 20 indents (chou2017microstructureandmechanical pages 1-2). Brinell hardness values in one comparative study show an as-produced LPBF AlSi10Mg around ~125 HB and a decrease after T6 to 110.1 ± 1.1 HB (tonolini2021wearbehaviorof media 0e4d9db5, tonolini2021wearbehaviorof pages 8-14). This “hardness drop after conventional T6” is consistent with loss/coarsening of the fine cellular Si network often observed for LPBF AlSi10Mg.

2) Scalmalloy® (Al–Mg–Sc–Zr)

As-built Scalmalloy hardness values compiled in a review include 104 ± 2 HV1 and 80 HV0.5 (cerri2024mainheattreatments pages 5-7). A dedicated aging study reports an as-built average of 104 ± 7 HV0.025 increasing to 170 ± 10 HV0.025 after direct aging, consistent with precipitation of Al3(Sc,Zr) (ghio2025laserpowderbedfused pages 10-13). Under longer aging at 325 °C, hardness plateaus around 165–171 HV0.5, while 400 °C leads to overaging and hardness decrease to ~100 HV0.5 at long times (ghio2025laserpowderbedfused pages 10-13).

3) Al–Cu(-Mg) family (2xxx-like and Al–Si–Cu variants)

For PBF-LB/M 2024 modified with nano-LaB6, hardness increases systematically with LaB6 content from 75.6 ± 3.6 HV0.2 (S0) to a maximum of 135.0 ± 3.3 HV0.2 (S1) (yao2024verificationofthe pages 7-9), illustrating a grain-refinement/particle-strengthening route to improved LPBF processability and hardness in a crack-prone alloy.

For an LPBF AlSi10Mg + 4 wt% Cu alloy (Al–Si–Cu, not a classical 2xxx but Cu-precipitation strengthened), peak microhardness is reported as exceeding 180 HV after aging at 160 °C for 16 h; an overaged condition at 180 °C for 12 h yields 167 HV; and an AlSi10Mg control aged at 160 °C for 16 h yields 140 ± 6 HV (load not specified in excerpt) (martin2021effectofthe pages 1-2, martin2021effectofthe pages 9-11).

For a high-temperature Al-2618-based system reinforced with TiB2 and processed by LPBF, as-built hardness is 122 ± 5 HV, dropping to 105 ± 3 HV after solution treatment (530 °C), and recovering to ~133–134 HV after aging (e.g., 134 ± 1 HV after ST+WQ+180 °C/1 h; 134 ± 4 HV after direct aging 180 °C/4 h) (lupi2025microstructureandtensile pages 8-11).

4) Al–Zn–Mg–Cu (7xxx-like) and crack-mitigation variants

A “high strength Al–Si–Zn–Mg–Cu” alloy produced by LPBF from mixed AlSi10Mg and 7075 powders reported 135.8 HV (as-built) for “50% 7075”, a large decrease to 73.4 HV after stress relief (300 °C/2 h), and increases to ~149–153 HV with subsequent aging treatments (aversa2022laserpowderbed pages 9-11). The same study reports 4% Si-modified 7075 at 160 HV (as-built) and 171 HV after aging 150 °C/6 h (aversa2022laserpowderbed pages 9-11), illustrating how Si additions (eutectic modification) can improve printability while enabling moderate age hardening.

For an LPBF Al–Zn–Mg–Cu–Zr alloy (7075-like with Zr), Vickers microhardness HV0.1 is ~140–143 HV0.1 in as-built condition, increases to 157 ± 10 HV0.1 after long natural aging, and can reach a T6 peak hardness of 218 ± 11 HV0.1 (chambrin2023influenceofheat pages 4-7, chambrin2023influenceofheat pages 7-11). This is among the highest explicitly reported HV values in the retrieved LPBF Al datasets.

5) Al–Ce(-Mg/Si) systems

For an LPBF AlCe10MgSi alloy, as-built hardness depends strongly on volumetric energy density: 170 ± 5.2 HV1 (low VED) vs 214 ± 11.6 HV1 (high VED) (hesselmann2022effectofprecipitationforming pages 7-9). These values are notable because they approach or exceed many as-built AlSi10Mg microhardness values, reflecting strong intermetallic/eutectic strengthening contributions in Ce-containing alloys.

6) Other systems: Al–Fe

A hypereutectic LPBF Al–15%Fe alloy reports Vickers hardness measured at HV0.2 and HV1; HV0.2 clusters near ~210 HV and HV1 rises to ~210 HV under a densification-threshold processing condition (with slight decrease at higher energy, potentially due to cracking) (wang2021processabilityandoptimization pages 12-15). These hardness levels are high relative to many conventional LPBF Al alloys, consistent with substantial hard intermetallic content (θ-Al13Fe4) and fine-scale microstructures.

Evidence note (Brinell figure)

The extracted figure showing Brinell hardness for LPBF AlSi10Mg (as-produced and after T6) and gravity-cast comparisons provides a visually auditable HB dataset for this alloy, including an as-produced AM value around ~125 HB and AM-T6 near ~110 HB (tonolini2021wearbehaviorof media 0e4d9db5).

Limitations

1) Indentation load effects: many sources report HV without specifying load; such values are included but flagged as “load not stated” in the table, and should not be over-interpreted against HV0.1/HV1 datasets.
2) Condition dependence: for precipitation-hardenable systems (Scalmalloy, Al–Zn–Mg–Cu–Zr, AlSi10Mg+Cu), aging state dominates hardness; as-built values are not directly comparable to peak-aged values.
3) Alloy naming: some “Al–Cu” evidence in the retrieved corpus is represented by (i) A2024-based nanoparticle-modified material, and (ii) AlSi10Mg+Cu (a Si-containing Cu-strengthened alloy). Truly Si-free LPBF 2xxx Al–Cu hardness values exist in the broader literature, but were not successfully retrieved here with explicit numeric HV in accessible text chunks.


References

1. (chou2017microstructureandmechanical pages 1-2): R. Chou, A. Ghosh, S.C. Chou, M. Paliwal, and M. Brochu. Microstructure and mechanical properties of al10simg fabricated by pulsed laser powder bed fusion. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 689:53-62, Mar 2017. URL: https://doi.org/10.1016/j.msea.2017.02.023, doi:10.1016/j.msea.2017.02.023. This article has 82 citations.

2. (tonolini2021wearbehaviorof media 0e4d9db5): Pietro Tonolini, Lorenzo Montesano, Marialaura Tocci, Annalisa Pola, and Marcello Gelfi. Wear behavior of alsi10mg alloy produced by laser‐based powder bed fusion and gravity casting. Advanced Engineering Materials, Aug 2021. URL: https://doi.org/10.1002/adem.202100147, doi:10.1002/adem.202100147. This article has 43 citations and is from a peer-reviewed journal.

3. (tonolini2021wearbehaviorof pages 8-14): Pietro Tonolini, Lorenzo Montesano, Marialaura Tocci, Annalisa Pola, and Marcello Gelfi. Wear behavior of alsi10mg alloy produced by laser‐based powder bed fusion and gravity casting. Advanced Engineering Materials, Aug 2021. URL: https://doi.org/10.1002/adem.202100147, doi:10.1002/adem.202100147. This article has 43 citations and is from a peer-reviewed journal.

4. (marinelli2018mechanicalcharacterizationand pages 79-83): C Marinelli. Mechanical characterization and post-process heat treatment of selectively laser melted alsi10mg. Unknown journal, 2018.

5. (dejene2025effectsofscanning pages 8-10): Naol Dessalegn Dejene, Wakshum Mekonnen Tucho, and Hirpa G. Lemu. Effects of scanning strategies, part orientation, and hatching distance on the porosity and hardness of alsi10mg parts produced by laser powder bed fusion. Journal of Manufacturing and Materials Processing, 9:78, Feb 2025. URL: https://doi.org/10.3390/jmmp9030078, doi:10.3390/jmmp9030078. This article has 15 citations.

6. (megahed2022effectofheat pages 7-11): Sandra Megahed, Jannik Bühring, Tobias Duffe, Aleksandar Bach, Kai-Uwe Schröder, and Johannes Henrich Schleifenbaum. Effect of heat treatment on ductility and precipitation size of additively manufactured alsi10mg. Metals, 12:1311, Aug 2022. URL: https://doi.org/10.3390/met12081311, doi:10.3390/met12081311. This article has 21 citations.

7. (cerri2024mainheattreatments pages 5-7): Emanuela Cerri, Lorenzo Curti, and Emanuele Ghio. Main heat treatments currently applied on laser powder bed-fused scalmalloy®: a review. Crystals, 15:25, Dec 2024. URL: https://doi.org/10.3390/cryst15010025, doi:10.3390/cryst15010025. This article has 8 citations.

8. (ghio2025laserpowderbedfused pages 10-13): Emanuele Ghio, Lorenzo Curti, Daniele Carosi, Alessandro Morri, and Emanuela Cerri. Laser powder bed-fused scalmalloy®: effect of long thermal aging on hardness and electrical conductivity. Metals, 15:1364, Dec 2025. URL: https://doi.org/10.3390/met15121364, doi:10.3390/met15121364. This article has 0 citations.

9. (martucci2022lowpowerlaserpowder pages 11-13): Alessandra Martucci, Alberta Aversa, Diego Manfredi, Federica Bondioli, Sara Biamino, Daniele Ugues, Mariangela Lombardi, and Paolo Fino. Low-power laser powder bed fusion processing of scalmalloy®. Materials, 15:3123, Apr 2022. URL: https://doi.org/10.3390/ma15093123, doi:10.3390/ma15093123. This article has 27 citations.

10. (martucci2022lowpowerlaserpowder pages 9-11): Alessandra Martucci, Alberta Aversa, Diego Manfredi, Federica Bondioli, Sara Biamino, Daniele Ugues, Mariangela Lombardi, and Paolo Fino. Low-power laser powder bed fusion processing of scalmalloy®. Materials, 15:3123, Apr 2022. URL: https://doi.org/10.3390/ma15093123, doi:10.3390/ma15093123. This article has 27 citations.

11. (niedermeyer2026processparameterdevelopment pages 8-10): J Niedermeyer, T Witte, and F Schlenker. Process parameter development and optimization for the scalmalloy® alloy in the additive manufacturing of aircraft applications. Unknown journal, 2026.

12. (martin2021effectofthe pages 1-2): A. Martin, M. San Sebastian, E. Gil, C.Y. Wang, S. Milenkovic, M.T. Pérez-Prado, and C.M. Cepeda-Jiménez. Effect of the heat treatment on the microstructure and hardness evolution of a alsi10mgcu alloy designed for laser powder bed fusion. Materials Science and Engineering: A, 819:141487, Jul 2021. URL: https://doi.org/10.1016/j.msea.2021.141487, doi:10.1016/j.msea.2021.141487. This article has 31 citations.

13. (martin2021effectofthe pages 9-11): A. Martin, M. San Sebastian, E. Gil, C.Y. Wang, S. Milenkovic, M.T. Pérez-Prado, and C.M. Cepeda-Jiménez. Effect of the heat treatment on the microstructure and hardness evolution of a alsi10mgcu alloy designed for laser powder bed fusion. Materials Science and Engineering: A, 819:141487, Jul 2021. URL: https://doi.org/10.1016/j.msea.2021.141487, doi:10.1016/j.msea.2021.141487. This article has 31 citations.

14. (yao2024verificationofthe pages 7-9): Zeyu Yao and Ziwen Xie. Verification of the laser powder bed fusion performance of 2024 aluminum alloys modified using nano-lab6. Materials, 17:3367, Jul 2024. URL: https://doi.org/10.3390/ma17133367, doi:10.3390/ma17133367. This article has 9 citations.

15. (lupi2025microstructureandtensile pages 8-11): G. Lupi, L. Mariotti, A. Mistrini, J. Larsson, L. Patriarca, and R. Casati. Microstructure and tensile properties of tib2-reinforced al-2618 thin walls produced by laser powder bed fusion. Materials Characterization, 228:115372, Oct 2025. URL: https://doi.org/10.1016/j.matchar.2025.115372, doi:10.1016/j.matchar.2025.115372. This article has 3 citations and is from a peer-reviewed journal.

16. (chambrin2023influenceofheat pages 4-7): Nicolas Chambrin, Olivier Dalverny, Armel Descamps-Mandine, Jean-Marc Cloue, Olivier Brucelle, and Joel Alexis. Influence of heat treatments on microstructure and hardness of a high-strength al-zn-mg-cu-zr alloy processed by laser powder bed fusion. Metals, 13:1173, Jun 2023. URL: https://doi.org/10.3390/met13071173, doi:10.3390/met13071173. This article has 5 citations.

17. (chambrin2023influenceofheat pages 7-11): Nicolas Chambrin, Olivier Dalverny, Armel Descamps-Mandine, Jean-Marc Cloue, Olivier Brucelle, and Joel Alexis. Influence of heat treatments on microstructure and hardness of a high-strength al-zn-mg-cu-zr alloy processed by laser powder bed fusion. Metals, 13:1173, Jun 2023. URL: https://doi.org/10.3390/met13071173, doi:10.3390/met13071173. This article has 5 citations.

18. (aversa2022laserpowderbed pages 9-11): Alberta Aversa, Giulio Marchese, Diego Manfredi, Massimo Lorusso, Flaviana Calignano, Sara Biamino, Mariangela Lombardi, Paolo Fino, and Matteo Pavese. Laser powder bed fusion of a high strength al-si-zn-mg-cu alloy. Metals, 8(5):300, Apr 2018. URL: https://doi.org/10.3390/met8050300, doi:10.3390/met8050300. This article has 66 citations.

19. (hesselmann2022effectofprecipitationforming pages 7-9): Marcel Hesselmann, Daniel Knoop, Jérémy Epp, Volker Uhlenwinkel, Axel von Hehl, and Anastasiya Toenjes. Effect of precipitation-forming elements in a near-eutectic al-ce alloy for laser powder bed fusion. Additive Manufacturing, 57:102959, Sep 2022. URL: https://doi.org/10.1016/j.addma.2022.102959, doi:10.1016/j.addma.2022.102959. This article has 23 citations and is from a highest quality peer-reviewed journal.

20. (wang2021processabilityandoptimization pages 12-15): Wenyuan Wang, Naoki Takata, Asuka Suzuki, Makoto Kobashi, and Masaki Kato. Processability and optimization of laser parameters for densification of hypereutectic al–fe binary alloy manufactured by laser powder bed fusion. Crystals, 11(3):320, Mar 2021. URL: https://doi.org/10.3390/cryst11030320, doi:10.3390/cryst11030320. This article has 16 citations.


---



## Query 4

**Question:** What elevated temperature (150-350°C) tensile properties have been reported for AM aluminum alloys? Which alloy systems retain the most strength at high temperature? Provide quantitative data.

**Task ID:** `e4fbe1d8-9ec7-4456-96c9-50ab45ff2e39`

**Status:** complete

## Elevated-temperature tensile properties reported for AM Al alloys (150–350°C)

Quantitative tensile data in the 150–350°C window are available for several AM Al alloy families (mostly LPBF). The compiled values below include yield strength (YS), ultimate tensile strength (UTS), and elongation where reported, with some datasets only available as plotted values.

| Alloy system (composition) | AM process + condition | Test temperature (°C) | Yield strength (MPa) | UTS (MPa) | Elongation (%) | Strength retention vs RT | Notes |
|---|---|---:|---:|---:|---:|---|---|
| AlSi10Mg | LPBF; stress-relieved 2 h @ 350°C; 0° build orientation | RT | 165.94 | 280.20 | 6.37 | Baseline | Directly reported baseline for same condition/orientation (lehmhus2022hightemperaturemechanicalproperties pages 6-9, lehmhus2022hightemperaturemechanicalproperties pages 9-12) |
| AlSi10Mg | LPBF; stress-relieved 2 h @ 350°C; 0° build orientation | 250 | 132.95 | 162.82 | 15.64 | YS 0.80× RT; UTS 0.58× RT | Table A2 values; 45° and 90° were slightly higher in UTS at 250°C (174.11 and 163.56 MPa) (lehmhus2022hightemperaturemechanicalproperties media 73715003) |
| Al-Mg-Sc-Zr | LPBF; aged / heat-treated 350°C for 4 h (AA-H) | RT | — | 560.6 | 11.1 | Baseline | RT UTS and elongation explicitly reported; YS not available in extracted text here (ren2024studyonmicrostructure pages 1-2) |
| Al-Mg-Sc-Zr | LPBF; aged / heat-treated 350°C for 4 h (AA-H) | 150 | 214 | 269 | 20.1 | UTS 0.48× RT | Table 3 values (ren2024studyonmicrostructure pages 8-10, ren2024studyonmicrostructure pages 1-2) |
| Al-Mg-Sc-Zr | LPBF; aged / heat-treated 350°C for 4 h (AA-H) | 200 | 77 | 102 | 47.9 | UTS 0.18× RT | Table 3 values (ren2024studyonmicrostructure pages 8-10, ren2024studyonmicrostructure pages 1-2) |
| Al-Mg-Sc-Zr | LPBF; aged / heat-treated 350°C for 4 h (AA-H) | 250 | 52 | 54 | 72.2 | UTS 0.10× RT | Table 3 values (ren2024studyonmicrostructure pages 8-10, ren2024studyonmicrostructure pages 1-2) |
| Al-Mn-Sc | LPBF; elevated-temperature tensile; strain rate 1e-2 s^-1 | 150 | ~480 | ~485 | — | YS ~1.12× vs RT YS=427 MPa | Approx. digitized from Fig. 9; RT reference from as-fabricated alloy; elevated-temp value may reflect strain-rate sensitivity and differs from RT test protocol (yan2023microstructuresandhigh pages 6-10, yan2023microstructuresandhigh media 6f8baf6a) |
| Al-Mn-Sc | LPBF; elevated-temperature tensile; strain rate 1e-2 s^-1 | 200 | ~430 | ~435 | — | YS ~1.01× vs RT YS=427 MPa | Approx. from Fig. 9 (yan2023microstructuresandhigh pages 6-10, yan2023microstructuresandhigh media 6f8baf6a) |
| Al-Mn-Sc | LPBF; elevated-temperature tensile; strain rate 1e-2 s^-1 | 250 | ~370 | ~380 | — | YS ~0.87× vs RT YS=427 MPa | Approx. from Fig. 9 (yan2023microstructuresandhigh pages 6-10, yan2023microstructuresandhigh media 6f8baf6a) |
| Al-Mn-Sc | LPBF; elevated-temperature tensile; strain rate 1e-2 s^-1 | 300 | ~215 | ~235 | ~8 | YS ~0.50× vs RT YS=427 MPa | Approx. from Fig. 9; fracture strain at 573 K (~300°C) drops to ~8% at 1e-2 s^-1 (yan2023microstructuresandhigh pages 6-10, yan2023microstructuresandhigh media 6f8baf6a) |
| Al-Mn-Sc | LPBF; elevated-temperature tensile; strain rate 1e-3 s^-1 | 150 | ~440 | ~450 | — | YS ~1.03× vs RT YS=427 MPa | Approx. from Fig. 9 (yan2023microstructuresandhigh pages 6-10, yan2023microstructuresandhigh media 6f8baf6a) |
| Al-Mn-Sc | LPBF; elevated-temperature tensile; strain rate 1e-3 s^-1 | 200 | ~340 | ~365 | — | YS ~0.80× vs RT YS=427 MPa | Approx. from Fig. 9 (yan2023microstructuresandhigh pages 6-10, yan2023microstructuresandhigh media 6f8baf6a) |
| Al-Mn-Sc | LPBF; elevated-temperature tensile; strain rate 1e-3 s^-1 | 250 | ~235 | ~285 | — | YS ~0.55× vs RT YS=427 MPa | Approx. from Fig. 9 (yan2023microstructuresandhigh pages 6-10, yan2023microstructuresandhigh media 6f8baf6a) |
| Al-Mn-Sc | LPBF; elevated-temperature tensile; strain rate 1e-3 s^-1 | 300 | ~160 | ~180 | — | YS ~0.37× vs RT YS=427 MPa | Approx. from Fig. 9 (yan2023microstructuresandhigh pages 6-10, yan2023microstructuresandhigh media 6f8baf6a) |
| Al-10Ce-8Mn | LPBF; as-fabricated high-temperature alloy | 150 | ~250 | ~270 | ~10 | — | Approx. from Fig. 7 open-circle AlCeMn series; 350°C point not explicitly marked (plotkowski2020microstructureandproperties media f76d1508, plotkowski2020microstructureandproperties media cc410958) |
| Al-10Ce-8Mn | LPBF; as-fabricated high-temperature alloy | 200 | ~235 | ~255 | ~12 | — | Approx. from Fig. 7; graphical extraction only (plotkowski2020microstructureandproperties media f76d1508, plotkowski2020microstructureandproperties media cc410958) |
| Al-10Ce-8Mn | LPBF; as-fabricated high-temperature alloy | 250 | ~215 | ~240 | ~15 | — | Approx. from Fig. 7; graphical extraction only (plotkowski2020microstructureandproperties media f76d1508, plotkowski2020microstructureandproperties media cc410958) |
| Al-10Ce-8Mn | LPBF; as-fabricated high-temperature alloy | 300 | ~195 | ~225 | ~18 | — | Approx. from Fig. 7; graphical extraction only; no explicit 350°C marker shown (plotkowski2020microstructureandproperties media f76d1508, plotkowski2020microstructureandproperties media cc410958) |


*Table: This table compiles reported or figure-extracted tensile properties of additively manufactured aluminum alloys tested at 150–300°C, with retention versus room temperature where the same-condition RT baseline was available. It is useful for comparing which alloy systems best preserve strength at high temperature.*

### (1) Al–Si–Mg (AlSi10Mg): large strength loss by 250°C
A stress-relieved LPBF AlSi10Mg condition (2 h at 350°C) shows a substantial strength drop by 250°C: for 0° build orientation, YS decreases from 165.94 MPa at RT to 132.95 MPa at 250°C (≈0.80 retention), while UTS decreases from 280.20 MPa at RT to 162.82 MPa at 250°C (≈0.58 retention); elongation increases from 6.37% to 15.64%. (lehmhus2022hightemperaturemechanicalproperties media 73715003, lehmhus2022hightemperaturemechanicalproperties pages 9-12)

### (2) Al–Mg–Sc–Zr (Sc/Zr precipitation-strengthened): in one reported condition, rapid softening above 150°C
For an LPBF Al–Mg–Sc–Zr alloy in an “as-aged” condition (reported as heat-treated 350°C for 4 h), high-temperature tensile values show strong softening beyond 150°C: at 150°C, YS/UTS/elongation = 214 MPa / 269 MPa / 20.1%; at 200°C = 77 MPa / 102 MPa / 47.9%; and at 250°C = 52 MPa / 54 MPa / 72.2%. The same paper reports RT UTS 560.6 MPa and elongation 11.1%, so UTS retention is ≈0.48 at 150°C, ≈0.18 at 200°C, and ≈0.10 at 250°C. (ren2024studyonmicrostructure pages 8-10, ren2024studyonmicrostructure pages 1-2)

### (3) Al–Mn–Sc (Sc/Zr-containing dispersoid/precipitate-stabilized): comparatively high strength retained through 300°C
For LPBF Al–Mn–Sc, elevated-temperature tensile strengths are presented as functions of temperature and strain rate (Figure 9). Approximate values at 150–300°C show relatively high absolute strengths compared with AlSi10Mg at similar temperatures. For example at 300°C (573 K), YS is ~160 MPa (10^-3 s^-1) to ~215 MPa (10^-2 s^-1) and UTS is ~180 MPa (10^-3 s^-1) to ~235 MPa (10^-2 s^-1). (yan2023microstructuresandhigh media 6f8baf6a, yan2023microstructuresandhigh pages 6-10)

### (4) Al–Ce–Mn (intermetallic-strengthened): comparatively high strength retained through 300°C
For an AM (LPBF) Al–10Ce–8Mn alloy, tensile properties vs temperature are reported graphically (Figure 7). Approximate values for the AlCeMn series are ~250 MPa YS / ~270 MPa UTS at 150°C, ~235 MPa YS / ~255 MPa UTS at 200°C, ~215 MPa YS / ~240 MPa UTS at 250°C, and ~195 MPa YS / ~225 MPa UTS at 300°C (data points are marked at 150/200/250/300/400°C in the plot; a 350°C marker is not shown). (plotkowski2020microstructureandproperties media cc410958, plotkowski2020microstructureandproperties media f76d1508)

## Which AM Al alloy systems retain the most strength at high temperature?

Within the extracted 150–300°C datasets here, the strongest high-temperature load-carrying capability (highest absolute strengths at 250–300°C) is shown by:

1. **LPBF Al–Mn–Sc**: at ~300°C, UTS ~180–235 MPa (depending on strain rate) with YS ~160–215 MPa, indicating comparatively strong retention into the 300°C regime. (yan2023microstructuresandhigh media 6f8baf6a)
2. **LPBF Al–Ce–Mn (Al–10Ce–8Mn)**: at ~300°C, UTS ~225 MPa and YS ~195 MPa (approx. from the plotted points), comparable to Al–Mn–Sc and clearly above the typical performance of AlSi10Mg at ≥250°C. (plotkowski2020microstructureandproperties media cc410958)

By contrast:

- **LPBF AlSi10Mg** drops to ~163–174 MPa UTS at 250°C (depending on orientation), with substantial retention loss already evident by 250°C. (lehmhus2022hightemperaturemechanicalproperties media 73715003)
- **The specific LPBF Al–Mg–Sc–Zr condition reported by Ren et al.** shows very rapid loss of strength beyond 150°C, reaching UTS ~54 MPa at 250°C. (ren2024studyonmicrostructure pages 8-10)

## Evidence gaps relative to the full 150–350°C window

The retrieved primary sources here provide robust quantitative coverage up to **~300°C** (Al–Mn–Sc; Al–Ce–Mn) and to **250°C** (AlSi10Mg; Al–Mg–Sc–Zr). For **350°C**, the main gap in the present evidence is the absence of directly tabulated tensile values at 350°C for these specific AM alloys in the retrieved texts/figures (e.g., Al–Ce–Mn plot shows points at 300 and 400°C but not explicitly at 350°C). (plotkowski2020microstructureandproperties media cc410958, lehmhus2022hightemperaturemechanicalproperties media 73715003)

---

## Query 5

**Question:** What creep resistance data exists for additively manufactured aluminum alloys? Which AM Al alloys show the best creep resistance and at what temperatures? Provide quantitative creep rates or rupture times.

**Task ID:** `92493c06-50f7-4b28-9f3b-a14add560e71`

**Status:** complete

## Creep-resistance data available for AM aluminum alloys (quantitative)

The retrieved primary literature with explicit *minimum/steady-state creep rates* and/or *rupture times* is dominated by LPBF/SLM **AlSi10Mg**; within the currently retrieved corpus it is the only AM Al alloy family with a complete set of stress/temperature-resolved creep rates *and* rupture lives. (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2019compressivecreepof pages 3-4, read2015selectivelasermelting pages 5-7)

| Alloy/system | AM process & condition | Creep test mode | Temperature (°C) | Stress (MPa) | Minimum/steady-state creep rate (s^-1) | Rupture time (min or h) | Notes |
|---|---|---|---:|---:|---:|---|---|
| AlSi10Mg | SLM/LPBF; stress-relieved (300 °C, 2 h) | Tension | 225 | 147 | 1.06×10^-4 | 9 min | Uzan 2018 Table 4 (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties pages 1-5, uzan2018hightemperaturemechanicalproperties media c3b4fc4f) |
| AlSi10Mg | SLM/LPBF; stress-relieved (300 °C, 2 h) | Tension | 225 | 137 | 1.47×10^-5 | 32 min | Uzan 2018 Table 4 (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties pages 1-5, uzan2018hightemperaturemechanicalproperties media c3b4fc4f) |
| AlSi10Mg | SLM/LPBF; stress-relieved (300 °C, 2 h) | Tension | 225 | 127 | 1.78×10^-6 | 360 min | Uzan 2018 Table 4 (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties pages 1-5, uzan2018hightemperaturemechanicalproperties media c3b4fc4f) |
| AlSi10Mg | SLM/LPBF; stress-relieved (300 °C, 2 h) | Tension | 225 | 117 | 3.14×10^-7 | 3944 min | Uzan 2018 Table 4 (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties pages 11-16, uzan2018hightemperaturemechanicalproperties media c3b4fc4f) |
| AlSi10Mg | SLM/LPBF; stress-relieved (300 °C, 2 h) | Tension | 250 | 117 | 4.01×10^-6 | 282 min | Temperature series at constant 117 MPa (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties media c3b4fc4f, uzan2018hightemperaturemechanicalproperties media 263e69b6) |
| AlSi10Mg | SLM/LPBF; stress-relieved (300 °C, 2 h) | Tension | 275 | 117 | 1.21×10^-5 | 33 min | Temperature series at constant 117 MPa (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties media c3b4fc4f, uzan2018hightemperaturemechanicalproperties media 263e69b6) |
| AlSi10Mg | SLM/LPBF; stress-relieved (300 °C, 2 h) | Tension | 300 | 117 | 3.50×10^-5 | 8 min | Temperature series at constant 117 MPa (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties media c3b4fc4f, uzan2018hightemperaturemechanicalproperties media 263e69b6) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 175 | 125 | 5.60×10^-8 | NR | No current; SPS-based compressive creep (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 200 | 125 | 3.45×10^-7 | NR | No current (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 225 | 125 | 3.30×10^-6 | NR | No current (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 175 | 125 | 1.41×10^-7 | NR | With electric current; current increased creep rate vs no-current test (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 200 | 125 | 1.32×10^-6 | NR | With electric current (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 225 | 125 | 6.47×10^-6 | NR | With electric current (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 225 | 100 | 1.08×10^-7 | NR | No current; stress series at 225 °C (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 225 | 110 | 4.25×10^-7 | NR | No current; stress series at 225 °C (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 225 | 120 | 1.45×10^-6 | NR | No current; stress series at 225 °C (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM rods; stress-relieved | Compression | 225 | 130 | 6.50×10^-6 | NR | No current; stress series at 225 °C (uzan2019compressivecreepof pages 3-4) |
| AlSi10Mg | SLM horizontal sample | Tension | 180 | 200 | NR | 18.7 h | Rupture time measured; literature/Larson–Miller prediction for same condition 14.8 h (read2015selectivelasermelting pages 5-7) |
| Al-Zr and ODS-Al-Zr | LPBF elemental-blend alloys; aged 24 h at 400 °C | Compression | 300 / 400 | variable | NR | Test durations ~149–168 h at 300 °C; ~141–173 h at 400 °C | Absolute creep-rate values not transcribed; threshold stresses ~14–16 MPa at 300 °C and ~6 MPa at 400 °C (power-law fit), low-stress thresholds ~9–11 MPa at 300 °C and ~5 MPa at 400 °C; ODS and non-ODS similar overall creep resistance (anne2023laserpowderbedfusion pages 180-185, anne2023laserpowderbedfusion pages 185-191) |


*Table: This table compiles the quantitative creep rates and rupture times that were extractable from the available evidence for additively manufactured aluminum alloys. It is useful for comparing which AM Al systems have reported data and where only partial creep metrics, such as threshold stresses, are available.*

### Key quantitative datasets

**1) SLM/LPBF AlSi10Mg (stress-relieved) — tensile creep rates and rupture times (225–300 °C)**

Uzan et al. report tensile creep of SLM AlSi10Mg after stress relief at 300 °C for 2 h, including minimum creep strain rates and rupture times over 225–300 °C and 117–147 MPa. (uzan2018hightemperaturemechanicalproperties pages 1-5, uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties media c3b4fc4f)

At **225 °C**, the creep resistance improves strongly with decreasing stress: at **147 MPa** the minimum creep rate is **1.06×10^-4 s^-1** with rupture in **9 min**, while at **117 MPa** the minimum creep rate is **3.14×10^-7 s^-1** with rupture in **3944 min** (~65.7 h). (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties media c3b4fc4f)

At constant **117 MPa**, creep resistance deteriorates rapidly with temperature: **225 °C: 3.14×10^-7 s^-1 (3944 min)**; **250 °C: 4.01×10^-6 s^-1 (282 min)**; **275 °C: 1.21×10^-5 s^-1 (33 min)**; **300 °C: 3.50×10^-5 s^-1 (8 min)**. (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties media c3b4fc4f)

A creep-rate versus reciprocal-temperature plot at 117 MPa (Figure 6a) supports this strong Arrhenius-type temperature dependence. (uzan2018hightemperaturemechanicalproperties media 263e69b6)

**2) SLM/LPBF AlSi10Mg (stress-relieved rods) — compressive minimum creep rates (175–225 °C)**

Uzan et al. also report steady-state compressive creep rates for SLM AlSi10Mg at 175–225 °C and 100–130 MPa. For example, at **125 MPa** the minimum creep rate increases from **5.60×10^-8 s^-1 (175 °C)** to **3.45×10^-7 s^-1 (200 °C)** and **3.30×10^-6 s^-1 (225 °C)**. (uzan2019compressivecreepof pages 3-4)

At **225 °C**, increasing stress raises the minimum creep rate from **1.08×10^-7 s^-1 (100 MPa)** to **6.50×10^-6 s^-1 (130 MPa)**. (uzan2019compressivecreepof pages 3-4)

They further show that applying electric current can increase the creep rate by ~2.5× under otherwise similar conditions (e.g., at 125 MPa and 200 °C: 3.45×10^-7 s^-1 without current vs 1.32×10^-6 s^-1 with current). (uzan2019compressivecreepof pages 3-4)

**3) SLM AlSi10Mg — rupture time at 180 °C / 200 MPa**

Read et al. report tensile creep rupture of SLM AlSi10Mg at **180 °C and 200 MPa**, with rupture after **18.7 h** (and a comparison to a Larson–Miller-based prediction of 14.8 h from literature data). (read2015selectivelasermelting pages 5-7)

## Which AM Al alloys show the best creep resistance (from retrieved quantitative data)?

### Temperature regime: ~175–225 °C

Within the retrieved quantitative dataset, the best creep resistance (lowest reported minimum creep rate) is for **SLM/LPBF AlSi10Mg in compression at 175 °C and 125 MPa**, with a minimum creep rate of **5.60×10^-8 s^-1**. (uzan2019compressivecreepof pages 3-4)

In terms of **longest rupture life**, Uzan et al. report **3944 min (~65.7 h)** for **SLM AlSi10Mg at 225 °C and 117 MPa** (tension), with a corresponding minimum creep rate of **3.14×10^-7 s^-1**. (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties media c3b4fc4f)

### Temperature regime: ≥250 °C

For the same AlSi10Mg alloy and a fixed stress of 117 MPa, creep resistance declines sharply above 250 °C, falling to **8 min rupture life at 300 °C** with a minimum creep rate of **3.50×10^-5 s^-1**. (uzan2018hightemperaturemechanicalproperties pages 5-11, uzan2018hightemperaturemechanicalproperties media c3b4fc4f)

The present retrieved corpus contains **partial** high-temperature creep descriptors for LPBF **Al–Zr** and **ODS Al–Zr** systems at **300–400 °C** (e.g., threshold stresses ~14–16 MPa at 300 °C and ~6 MPa at 400 °C), but does **not** include absolute creep-rate points that would enable a quantitative comparison/ranking against AlSi10Mg or among high-temperature Al alloys at those temperatures. (anne2023laserpowderbedfusion pages 180-185, anne2023laserpowderbedfusion pages 185-191)

## Evidence gaps in the retrieved set (limits on ranking across AM Al alloy families)

Several AM Al families known to target higher-temperature creep (e.g., Al–Ce(-Ni/Mn/Zr) and Al–Mn–Mg–Sc–Zr/Scalmalloy-type alloys) were identified during search, but **quantitative constant-load creep rates/rupture times were not successfully retrieved in the available full texts here** (some key creep-focused papers were flagged as unobtainable by the backend). Consequently, the “best AM Al alloy” conclusion is necessarily limited to the alloys for which explicit numerical creep data were retrievable in this run, primarily AlSi10Mg. (anne2023laserpowderbedfusion pages 157-162, anne2023laserpowderbedfusion pages 77-81, anne2023laserpowderbedfusion pages 71-77)

---

## Query 6

**Question:** What are the elastic modulus values reported for different LPBF aluminum alloys? How does the modulus compare to wrought equivalents? Is there significant anisotropy?

**Task ID:** `e5cc3a82-964c-497f-8904-8220ae4fa24a`

**Status:** complete

## Summary of elastic modulus values reported for LPBF aluminum alloys

Reported Young’s modulus values for LPBF aluminum alloys in the retrieved sources cluster around ~65–78 GPa depending on alloy, heat treatment, and (sometimes) build orientation/scan strategy (garciazapata2024effectsofbuilding pages 12-13, uzan2018hightemperaturemechanicalproperties pages 5-11, mower2016mechanicalbehaviorof pages 8-10, mehta2021additivemanufacturingand pages 10-11, martucci2022lowpowerlaserpowder pages 11-13, wang2024areviewon pages 9-11). A consolidated table is provided below.

| Alloy | Process/condition | Orientation | Modulus E (GPa) | Comparator | Notes on anisotropy |
|---|---|---|---|---|---|
| AlSi10Mg | Stress-relieved SLM/LPBF | Vertical | 77.8 ± 1.5 | Horizontal: 77.1 ± 1.5 | “Virtually identical”; ΔE = 0.7 GPa (<1%), no significant elastic anisotropy after stress relief (uzan2018hightemperaturemechanicalproperties pages 5-11) |
| AlSi10Mg | Stress-relieved SLM/LPBF | Horizontal | 77.1 ± 1.5 | Vertical: 77.8 ± 1.5 | Same conclusion as above; G also nearly identical (uzan2018hightemperaturemechanicalproperties pages 5-11) |
| AlSi10Mg | LPBF, border scanning, 60 µm layer | Flat | 63 ± 3 | Vertical60: 72 ± 6 | Vertical ~14% higher than flat/edge; significant stiffness differences with build direction/process/border scanning (garciazapata2024effectsofbuilding pages 12-13) |
| AlSi10Mg | LPBF, border scanning, 60 µm layer | Edge | 63 ± 3 | Vertical60: 72 ± 6 | Edge ≈ flat; vertical higher (garciazapata2024effectsofbuilding pages 12-13) |
| AlSi10Mg | LPBF, border scanning, 60 µm layer | Vertical | 72 ± 6 | Flat60/Edge60: 63 ± 3 | Highest among bordered 60 µm set (garciazapata2024effectsofbuilding pages 12-13) |
| AlSi10Mg | LPBF, border scanning, 30 µm layer | Flat | 61 ± 5 | Vertical30: 67 ± 5 | Vertical ~10% higher than flat (garciazapata2024effectsofbuilding pages 12-13) |
| AlSi10Mg | LPBF, border scanning, 30 µm layer | Edge | 63 ± 3 | Vertical30: 67 ± 5 | Edge close to flat; vertical modestly higher (garciazapata2024effectsofbuilding pages 12-13) |
| AlSi10Mg | LPBF, border scanning, 30 µm layer | Vertical | 67 ± 5 | Flat30: 61 ± 5; Edge30: 63 ± 3 | Moderate anisotropy with border scan (garciazapata2024effectsofbuilding pages 12-13) |
| AlSi10Mg | LPBF, no border scan (WB), 60 µm layer | Flat60WB | 76 ± 4 | Vertical60WB: 54 ± 2 | Reversed trend; flat much stiffer than vertical by ~22 GPa (~29%) (garciazapata2024effectsofbuilding pages 12-13) |
| AlSi10Mg | LPBF, no border scan (WB), 60 µm layer | Edge60WB | 68 ± 6 | Vertical60WB: 54 ± 2 | Edge intermediate (garciazapata2024effectsofbuilding pages 12-13) |
| AlSi10Mg | LPBF, no border scan (WB), 60 µm layer | Vertical60WB | 54 ± 2 | Flat60WB: 76 ± 4 | Lowest modulus in set; strong process-dependent anisotropy (garciazapata2024effectsofbuilding pages 12-13) |
| AlSi10Mg | SLM/LPBF tensile modulus | Horizontal | 65.5 | Wrought Al6061: 66.5 | Horizontal LPBF AlSi10Mg ~same as wrought Al6061 in this table (mower2016mechanicalbehaviorof pages 8-10) |
| AlSi10Mg | SLM/LPBF tensile modulus | Vertical | 75.4 | Wrought Al6061: 66.5 | Vertical ~13% above wrought Al6061 and ~15% above horizontal LPBF value (mower2016mechanicalbehaviorof pages 8-10) |
| AlSi10Mg | SLM/LPBF flexural modulus | Horizontal | 71.8 | Wrought Al6061: 65.5 | Study states SLM AlSi10Mg was ~10% stiffer than conventional wrought/machined Al6061; mild orientation effect (mower2016mechanicalbehaviorof pages 7-8) |
| AlSi10Mg | SLM/LPBF flexural modulus | Vertical | 73.8 | Wrought Al6061: 65.5 | Vertical slightly higher than horizontal; still ~10% above wrought reference (mower2016mechanicalbehaviorof pages 7-8) |
| AlSi10Mg | Review summary, as-fabricated | Not orientation-resolved | 68 ± 3 | — | Bulk value only; no anisotropy information in review table (wang2024areviewon pages 9-11) |
| AlSi10Mg | Review summary, T6 | Not orientation-resolved | 66 ± 5 | As-fabricated: 68 ± 3 | Slightly lower than as-fabricated in cited review table; no orientation split (wang2024areviewon pages 9-11) |
| AlSi10Mg | Review summary, as-fabricated (another cited entry) | Not orientation-resolved | 70.2 ± 1.2 | — | Listed as another LPBF AlSi10Mg/AlSi7Mg-family entry in review table; no orientation split (wang2024areviewon pages 9-11) |
| Scalmalloy® | Low-VED LPBF | Not orientation-resolved | 74 | Datasheet / higher-power LPBF literature: agreement stated, no number quoted | Reported to align with datasheet and Spierings et al.; no direct wrought comparator in excerpt (martucci2022lowpowerlaserpowder pages 11-13) |
| Zr-modified AA6061 | LPBF, instrumented indentation, as-built | Not orientation-resolved | 73.5 ± 3.0 | As-cast / wrought / T6 AA6061: 68.9 | Indentation modulus higher than conventional reference; no orientation-specific modulus reported (mehta2021additivemanufacturingand pages 9-10, mehta2021additivemanufacturingand pages 5-9, mehta2021additivemanufacturingand pages 10-11) |
| Zr-modified AA6061 | LPBF, instrumented indentation, solution heat treated | Not orientation-resolved | 73.9 ± 2.4 | As-cast / wrought / T6 AA6061: 68.9 | Little change with heat treatment in indentation modulus (mehta2021additivemanufacturingand pages 9-10, mehta2021additivemanufacturingand pages 10-11) |
| Zr-modified AA6061 | LPBF, instrumented indentation, aged | Not orientation-resolved | 73.5 ± 3.2 | As-cast / wrought / T6 AA6061: 68.9 | Similar to as-built/SHT; no anisotropy quantification (mehta2021additivemanufacturingand pages 9-10, mehta2021additivemanufacturingand pages 10-11) |
| Zr-modified AA6061 | LPBF tensile modulus, as-built | Not orientation-resolved | 70.1 | As-cast / O-annealed wrought / T6 wrought AA6061: 68.9 | Tensile modulus essentially same as conventional AA6061 (~69–70 GPa) (mehta2021additivemanufacturingand pages 9-10, mehta2021additivemanufacturingand pages 10-11) |
| Zr-modified AA6061 | LPBF tensile modulus, T6 | Not orientation-resolved | 70.0 | As-cast / O-annealed wrought / T6 wrought AA6061: 68.9 | Essentially unchanged by T6 and very close to conventional AA6061 (mehta2021additivemanufacturingand pages 9-10, mehta2021additivemanufacturingand pages 10-11) |


*Table: This table compiles reported Young’s modulus values for LPBF aluminum alloys from the retrieved evidence, including process condition, orientation, and comparisons to conventional references where available. It is useful for seeing the typical modulus range, how close LPBF values are to wrought/as-cast materials, and whether elastic anisotropy appears significant.*

## Alloy-by-alloy modulus values

### AlSi10Mg (LPBF/SLM)
- Stress-relieved AlSi10Mg: E ≈ 77–78 GPa with essentially no measurable orientation effect in one study (vertical 77.8 ± 1.5 GPa vs horizontal 77.1 ± 1.5 GPa; authors state moduli are “virtually identical”) (uzan2018hightemperaturemechanicalproperties pages 5-11).
- In contrast, another study reported strong process- and scanning-strategy-dependent stiffness differences across build directions (Flat/Edge/Vertical) (garciazapata2024effectsofbuilding pages 12-13). With border scanning enabled, vertical was modestly higher (e.g., 72 ± 6 GPa vs 63 ± 3 GPa for flat/edge at 60 µm layer thickness), but without border scanning (WB) the ordering reversed dramatically (e.g., vertical 54 ± 2 GPa vs flat 76 ± 4 GPa) (garciazapata2024effectsofbuilding pages 12-13). The same modulus table is visible in a cropped figure capture (garciazapata2024effectsofbuilding media e07a4e55).
- Review data (orientation not reported) include as-fabricated E = 68 ± 3 GPa and after T6 E = 66 ± 5 GPa (wang2024areviewon pages 9-11).

### Scalmalloy® (Al–Mg–Sc–Zr family; LPBF)
- A low-VED LPBF condition reported E = 74 GPa; the authors note agreement with datasheet statements and higher-power LPBF literature, but no wrought-equivalent modulus was numerically provided in the excerpt (martucci2022lowpowerlaserpowder pages 11-13).

### Zr-modified AA6061 (LPBF)
- LPBF Zr-modified AA6061 modulus from tensile testing: E ≈ 70.1 GPa (as-built) and 70.0 GPa (T6) (mehta2021additivemanufacturingand pages 10-11).
- The same paper reports instrumented-indentation-derived Young’s modulus E ≈ 73.5–73.9 GPa across as-built/solution heat treated/aged conditions (mehta2021additivemanufacturingand pages 9-10).

## Comparison to wrought equivalents

- **LPBF AlSi10Mg vs wrought Al6061 (reference comparator):**
  - Mower & Long reported wrought Al6061 modulus 66.5 GPa and SLM AlSi10Mg modulus 65.5 GPa (horizontal) vs 75.4 GPa (vertical) (mower2016mechanicalbehaviorof pages 8-10). In flexural testing they similarly reported wrought Al6061 ~65.5 GPa and SLM AlSi10Mg 71.8–73.8 GPa and summarized the SLM AlSi10Mg as ~10% stiffer than conventional wrought/machined Al6061 (mower2016mechanicalbehaviorof pages 7-8).
  - Note: this is a comparison across *different alloys* (AlSi10Mg vs Al6061) chosen because AlSi10Mg was (in that study) the commercially available SLM aluminum alloy (mower2016mechanicalbehaviorof pages 8-10).

- **LPBF Zr-modified AA6061 vs conventional AA6061:**
  - Mehta et al. report LPBF Zr-modified AA6061 E ≈ 70.0–70.1 GPa and list conventional reference values of 68.9 GPa for as-cast AA6061, O-annealed wrought AA6061, and T6 wrought AA6061 (mehta2021additivemanufacturingand pages 10-11). This indicates LPBF Zr-modified AA6061 has a modulus essentially comparable to conventional AA6061 (difference ~1–2%) (mehta2021additivemanufacturingand pages 10-11).

- **Scalmalloy:** only qualitative comparison to datasheet and other LPBF literature was available in the retrieved excerpt; no numerical wrought-equivalent modulus was given (martucci2022lowpowerlaserpowder pages 11-13).

## Is there significant anisotropy in elastic modulus?

Across the extracted sources, **elastic-modulus anisotropy in LPBF AlSi10Mg is not consistently large**, and when present it appears to be **highly condition-dependent**:

- **Near-isotropic modulus reported:** Stress-relieved AlSi10Mg showed “virtually identical” moduli between vertical and horizontal builds (ΔE ≈ 0.7 GPa, within ±1.5 GPa uncertainty) (uzan2018hightemperaturemechanicalproperties pages 5-11).

- **Moderate anisotropy (~10–15%) reported:**
  - With border scanning, one AlSi10Mg dataset shows vertical ~10–14% higher than flat/edge (e.g., 72 ± 6 vs 63 ± 3 GPa) (garciazapata2024effectsofbuilding pages 12-13).
  - Mower & Long report a horizontal/vertical split for AlSi10Mg of 65.5 vs 75.4 GPa (~15% higher in vertical) in their tensile modulus table (mower2016mechanicalbehaviorof pages 8-10).

- **Large apparent anisotropy under specific scan strategy:** Without border scanning, García-Zapata et al. show vertical modulus much lower than flat (54 ± 2 vs 76 ± 4 GPa; ~29% lower) (garciazapata2024effectsofbuilding pages 12-13). This suggests that scan strategy (here, border scanning) can dominate the measured stiffness differences between build directions (garciazapata2024effectsofbuilding pages 12-13).

- **Mechanistic/interpretive context:** Tang & Pistorius note that, in most previously reported results, there is an “absence of a significant difference in elastic modulus” between XY- and Z-oriented AlSi10Mg, consistent with the expectation that texture effects on modulus are weak for this alloy and typical scan-rotation strategies disrupt a strong texture (tang2017anisotropicmechanicalbehavior pages 2-4).

## Important limitation (7xxx/2xxx alloys)

Although papers on LPBF 7075 and 2024 were retrieved, the accessible full-text chunks did not contain extractable Young’s modulus values for these alloys in the current tool state; therefore the modulus summary here is evidence-backed for AlSi10Mg, Scalmalloy, and Zr-modified AA6061 only (martucci2022lowpowerlaserpowder pages 11-13, mehta2021additivemanufacturingand pages 10-11, garciazapata2024effectsofbuilding pages 12-13, uzan2018hightemperaturemechanicalproperties pages 5-11, mower2016mechanicalbehaviorof pages 8-10, wang2024areviewon pages 9-11).

---

## Query 7

**Question:** What impact toughness or Charpy energy values have been reported for LPBF aluminum alloys? How do they compare to wrought and cast equivalents?

**Task ID:** `89172f13-b2f5-4854-9a8a-746d0f5f9deb`

**Status:** complete

## Reported impact toughness / Charpy energy values for LPBF aluminum alloys

This summary focuses on *reported* (i.e., explicitly stated in accessible text/tables) impact-related properties for LPBF/SLM aluminum alloys, and how they compare to conventional cast/wrought references when those comparators are reported in the same sources.

| Alloy | AM process | Condition (as-built/heat treatment/HIP) | Test type & metric | Value (with uncertainty if reported) | Orientation (if reported) | Temperature | Comparator (cast/wrought) and values if available | Source citation id |
|---|---|---|---|---|---|---|---|---|
| AlSi10Mg | SLM/LPBF | As-built | Charpy absorbed energy | 4 ± 1 J | Not reported in excerpt | Not reported in excerpt | None reported in excerpt | (rosenthal2018heattreatmenteffect pages 14-21) |
| AlSi10Mg | SLM/LPBF | Modified T5, 200 °C | Charpy absorbed energy | ~2 ± 1 J | Not reported in excerpt | Not reported in excerpt | None reported in excerpt | (rosenthal2018heattreatmenteffect pages 14-21) |
| AlSi10Mg | SLM/LPBF | Typical T5, 300 °C | Charpy absorbed energy | ~7 ± 1 J | Not reported in excerpt | Not reported in excerpt | None reported in excerpt | (rosenthal2018heattreatmenteffect pages 14-21) |
| AlSi10Mg | SLM/LPBF | HIP, 500 °C, 100 MPa | Charpy absorbed energy | ~20 ± 1 J | Not reported in excerpt | Not reported in excerpt | None reported in excerpt | (rosenthal2018heattreatmenteffect pages 14-21) |
| AlSi10Mg | LPBF | Multiple build conditions | Fracture toughness, JIc | ~4.5 to 11.2 kJ/m² | Various; orientation-dependent | Room temperature implied | Cast AlSi10Mg-T6: JIc = 3.7 ± 0.4 kJ/m² | (paul2021fractureresistanceof pages 7-8) |
| AlSi10Mg | LPBF | 30LT/190HS/67SS | Fracture toughness, JIc | 11.2 ± 0.2 kJ/m² | XZ | Room temperature implied | Cast AlSi10Mg-T6: JIc = 3.7 ± 0.4 kJ/m² | (paul2021fractureresistanceof pages 7-8) |
| AlSi10Mg | LPBF | 30LT/100HS/90SS (0D) | Fracture toughness, JIc | 4.5 ± 0.8 kJ/m² | ZX | Room temperature implied | Cast AlSi10Mg-T6: JIc = 3.7 ± 0.4 kJ/m² | (paul2021fractureresistanceof pages 7-8) |
| AlSi10Mg | LPBF | Multiple build conditions | Fracture toughness, KJIc | ~19.5 to 30.9 MPa·m^0.5 | Various; orientation-dependent | Room temperature implied | Cast AlSi10Mg-T6: KJIc = 18.6 ± 1.1 MPa·m^0.5 | (paul2021fractureresistanceof pages 7-8, paul2021fractureresistanceof pages 12-13, paul2021fractureresistanceof pages 5-7) |
| AlSi10Mg | LPBF | Best-performing 67SS condition | Fracture toughness, KJIc | ~30.9 ± 0.3 MPa·m^0.5 | XZ | Room temperature implied | Cast AlSi10Mg-T6: 18.6 ± 1.1 MPa·m^0.5 | (paul2021fractureresistanceof pages 7-8, paul2021fractureresistanceof pages 12-13) |
| AlSi10Mg | LPBF | 90° scan-strategy material | Fracture toughness, KJIc | ~19 to 27 MPa·m^0.5 | Not fully specified in excerpt | Room temperature implied | Lower than 67° material; cast comparator ~19 MPa·m^0.5 | (paul2021fractureresistanceof pages 12-13, paul2021fractureresistanceof pages 13-13) |
| AlSi10Mg | LPBF | 67° scan-strategy material | Fracture toughness, KJIc | ~25 to 31 MPa·m^0.5 | Not fully specified in excerpt | Room temperature implied | Higher than cast comparator ~19 MPa·m^0.5 | (paul2021fractureresistanceof pages 12-13, paul2021fractureresistanceof pages 13-13) |
| Al-12Si | SLM | AS | Fracture toughness, Kq | 46.7 | k orientation | Not reported in excerpt | Conventionally cast (CC): 11.1 | (suryawanshi2016simultaneousenhancementsof pages 5-6) |
| Al-12Si | SLM | AS | Fracture toughness, Kq | 37.9 | ⊥ orientation | Not reported in excerpt | Conventionally cast (CC): 11.1 | (suryawanshi2016simultaneousenhancementsof pages 5-6) |
| Al-12Si | SLM | HS | Fracture toughness, Kq | 21.7 | k orientation | Not reported in excerpt | Conventionally cast (CC): 11.1 | (suryawanshi2016simultaneousenhancementsof pages 5-6) |
| Al-12Si | SLM | HS | Fracture toughness, Kq | 19.3 | ⊥ orientation | Not reported in excerpt | Conventionally cast (CC): 11.1 | (suryawanshi2016simultaneousenhancementsof pages 5-6) |
| Al-12Si | SLM | CS | Fracture toughness, Kq | 47.0 | k orientation | Not reported in excerpt | Conventionally cast (CC): 11.1 | (suryawanshi2016simultaneousenhancementsof pages 5-6) |
| Al-12Si | SLM | CS | Fracture toughness, Kq | 34.5 | ⊥ orientation | Not reported in excerpt | Conventionally cast (CC): 11.1 | (suryawanshi2016simultaneousenhancementsof pages 5-6) |
| Al-12Si | Conventional cast | CC comparator | Fracture toughness, Kq | 11.1 | Not applicable | Not reported in excerpt | Baseline for SLM comparison | (suryawanshi2016simultaneousenhancementsof pages 5-6) |
| AA2219 | LPBF | As-built | Instrumented Charpy, Ei | 5.1 J | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 101-104, tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | As-built | Instrumented Charpy, Ep | 6.3 J | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 101-104, tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | As-built | Instrumented Charpy, Et | 10.7 J | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | As-built | Charpy impact toughness | 138.6 kJ/m² | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | T5 | Instrumented Charpy, Ei | 4.4 J | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 101-104, tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | T5 | Instrumented Charpy, Ep | 4.7 J | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 101-104, tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | T5 | Instrumented Charpy, Et | 9.2 J | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | T5 | Charpy impact toughness | 105.8 kJ/m² | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | T6 | Instrumented Charpy, Ei | 5.9 J | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 101-104, tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | T6 | Instrumented Charpy, Ep | 2.7 J | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 101-104, tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | T6 | Instrumented Charpy, Et | 8.6 J | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 112-116) |
| AA2219 | LPBF | T6 | Charpy impact toughness | 101 kJ/m² | Not reported in excerpt | -196 °C | No wrought/cast Charpy comparator reported in excerpt | (tumulu2025laserpowderbed pages 112-116) |


*Table: This table compiles reported Charpy impact energy and fracture-toughness values for LPBF/SLM aluminum alloys from the gathered evidence, with test conditions and available cast comparators. It is useful for directly comparing reported impact resistance across alloy systems and post-processing states.*

### 1) AlSi10Mg (LPBF/SLM)

#### Charpy absorbed energy (instrumented or non-instrumented Charpy energy)
Rosenthal et al. reported very low absorbed energies for high-strength states and much higher energies after HIP for SLM (LPBF-equivalent) AlSi10Mg: as-built **4 ± 1 J**, modified T5 at **200 °C: ~2 ± 1 J**, typical T5 at **300 °C: ~7 ± 1 J**, and **HIP at 500 °C / 100 MPa: ~20 ± 1 J**. (rosenthal2018heattreatmenteffect pages 14-21)

*Comparison to wrought/cast:* in the accessible excerpt, Rosenthal et al. do not provide a cast or wrought Charpy baseline for direct numeric comparison, so the comparison is limited to AM post-processing states. (rosenthal2018heattreatmenteffect pages 14-21)

#### Impact/fracture toughness (J-integral initiation toughness and K-equivalent)
Paul et al. quantified fracture toughness of LPBF AlSi10Mg using ASTM E1820 J-integral methods and reported **J_Ic ~4.5–11.2 kJ/m²** and **K_JIc ~19.5–30.9 MPa·m^0.5**, with strong orientation and scan-strategy effects. (paul2021fractureresistanceof pages 7-8, paul2021fractureresistanceof pages 5-7)

*Comparison to cast:* in the same table, the cast AlSi10Mg-T6 reference had **J_Ic = 3.7 ± 0.4 kJ/m²** and **K_JIc = 18.6 ± 1.1 MPa·m^0.5**, i.e., the LPBF conditions span values comparable to or substantially above the cast-T6 comparator (up to roughly ~3× in J_Ic and ~1.7× in K_JIc for the best-performing LPBF condition/orientation). (paul2021fractureresistanceof pages 7-8)

### 2) Al–12Si (SLM; directly comparable to LPBF Al–Si family behavior)
Suryawanshi et al. reported fracture-toughness parameter **Kq** for SLM Al–12Si (with build-orientation dependence) and compared it directly to a conventionally cast alloy. Their Table 1 reports, for example, **Kq = 46.7** (AS, k orientation), **37.9** (AS, ⊥), **21.7** (HS, k), **19.3** (HS, ⊥), **47.0** (CS, k), and **34.5** (CS, ⊥), while the **conventionally cast (CC) comparator is 11.1**. (suryawanshi2016simultaneousenhancementsof pages 5-6)

*Comparison to cast:* as-built and some post-processed SLM conditions (AS, CS) are ~3–4× higher in Kq than the cast comparator, while heat treatment (HS) substantially reduces Kq (but still exceeds the cast comparator in the values shown). (suryawanshi2016simultaneousenhancementsof pages 5-6)

### 3) AA2219 (LPBF Al–Cu)
Tumulu reported **instrumented Charpy V-notch** results for LPBF AA2219 at **−196 °C** (liquid-nitrogen testing), including partition into initiation and propagation energies. Total absorbed energy **Et** at −196 °C was **10.7 J (as-built), 9.2 J (T5), and 8.6 J (T6)**; initiation energies **Ei** were **5.1, 4.4, 5.9 J** and propagation energies **Ep** were **6.3, 4.7, 2.7 J** for as-built, T5, and T6, respectively. A derived “Charpy impact toughness” (Et divided by 80 mm² net area) was **138.6, 105.8, and 101 kJ/m²** (as-built, T5, T6). (tumulu2025laserpowderbed pages 101-104, tumulu2025laserpowderbed pages 112-116)

*Comparison to wrought/cast:* the accessible excerpts do not include wrought or cast AA2219 Charpy values, nor room-temperature numeric Charpy values, so a direct quantitative comparison cannot be made from the retrieved evidence. (tumulu2025laserpowderbed pages 101-104, tumulu2025laserpowderbed pages 112-116, tumulu2025laserpowderbed pages 19-21)

## Overall comparison trends (based on retrieved quantitative evidence)

1. **LPBF/SLM Al–Si alloys can exceed cast counterparts in fracture toughness** (when assessed via J-integral/K-equivalent or Kq), but results are strongly dependent on scan strategy, mesostructure, and orientation. This is shown directly for AlSi10Mg vs cast-T6 in Paul et al., and for Al–12Si vs conventional cast in Suryawanshi et al. (paul2021fractureresistanceof pages 7-8, suryawanshi2016simultaneousenhancementsof pages 5-6)

2. **Charpy absorbed energy for AlSi10Mg is highly post-processing dependent** in the available numeric dataset: HIP increased absorbed energy to ~20 J, whereas as-built and certain aging/heat-treatment states were single-digit joules. (rosenthal2018heattreatmenteffect pages 14-21)

3. **For AA2219 at cryogenic temperature (−196 °C), LPBF Charpy energies are on the order of ~9–11 J** and decrease with T5/T6 relative to as-built in the reported dataset, but **no cast/wrought Charpy baselines** were available in the retrieved excerpts for direct comparison. (tumulu2025laserpowderbed pages 101-104, tumulu2025laserpowderbed pages 112-116)

## Evidence limitations
Several AlSi10Mg Charpy-focused LPBF studies retrieved here discuss orientation/heat-treatment effects and comparisons to gravity-cast AlSi10Mg or wrought Al6061, but the *numeric* energies appear to be figure-based and were not extractable from the accessible text snippets; consequently they are not used for quantitative comparisons in this answer. (pramod2023effectofpart pages 6-8, girelli2019evaluationofthe pages 13-14, pramod2023effectofpart pages 2-3)

---

## Query 8

**Question:** What are the wear resistance and tribological properties of LPBF aluminum alloys? Which alloy systems show the best wear resistance? Provide quantitative wear rate data.

**Task ID:** `848e9e77-3257-4173-a385-56a086d6895a`

**Status:** complete

## Summary
Wear resistance of LPBF aluminum alloys spans roughly an order of magnitude in specific wear rate depending on alloy system and surface state. Across the quantitative LPBF/SLM datasets retrieved here, the **best wear resistance (lowest specific wear rate k in mm³/N·m)** is reported for **heat-treatable SLM Al–Cu–Mg–Si** and for **Scalmalloy® (Al–Mg–Sc–Zr)** (both ~10⁻⁴ mm³/N·m), while conventional **LPBF AlSi10Mg** is typically ~10⁻⁴–10⁻³ mm³/N·m and an **Al–Si–Cu** system (Al8SiCu) is ~10⁻³ mm³/N·m even after TiB₂ reinforcement. (wang2021wearbehaviorof pages 4-7, abrami2021hightemperaturewear pages 1-3, sagbas2020postprocessingeffectson pages 4-6, he2024effectsofin media bfc55b3b)

## Quantitative wear and tribological properties (representative values)
| Alloy system (LPBF/SLM) | Condition / post-processing | Test configuration & key conditions (counterface, load, motion, lubrication, distance) | Coefficient of friction (COF) | Specific wear rate k (mm^3/N·m) or other wear metric | Notes on wear mechanism or hardness | Source context ID |
|---|---|---|---|---|---|---|
| AlSi10Mg (DMLS/LPBF) | Shot-peened surface | Ball-on-disc; 6 mm Al2O3 ball; 10 N; 300 rpm; 10,600 cycles; deionized water lubrication | 0.1242 ± 0.005 | 6.34E-04 mm^3/N·m | Higher hardness than polished (182 HV vs 127 HV); higher friction but lower wear than polished | (sagbas2019investigatingthetribologicala pages 4-6, sagbas2019investigatingthetribological pages 4-6) |
| AlSi10Mg (DMLS/LPBF) | Polished surface | Ball-on-disc; 6 mm Al2O3 ball; 10 N; 300 rpm; 10,600 cycles; deionized water lubrication | 0.0862 ± 0.003 | 7.86E-04 mm^3/N·m | Lower hardness and smoother surface; lower friction but worse wear than shot-peened | (sagbas2019investigatingthetribologicala pages 4-6, sagbas2019investigatingthetribological pages 4-6) |
| AlSi10Mg (LPBF) | Shot-peened + palm oil (best case in Sagbas 2020) | Ball-on-disc; 6 mm Al2O3 ball; 10 N; 300 rpm; 10,600 cycles; palm oil | 0.0996 ± 0.005 | 3.88E-04 mm^3/N·m | Minimum wear rate among tested finishing/lubrication combinations; shot peening increased hardness/strength | (sagbas2020postprocessingeffectson pages 2-4, sagbas2020postprocessingeffectson pages 4-6) |
| AlSi10Mg (LPBF) | Polished + palm oil (lowest COF in Sagbas 2020) | Ball-on-disc; 6 mm Al2O3 ball; 10 N; 300 rpm; 10,600 cycles; palm oil | 0.0563 ± 0.005 | 6.56E-04 mm^3/N·m | Smoothest surface gave minimum friction coefficient, but not minimum wear | (sagbas2020postprocessingeffectson pages 2-4, sagbas2020postprocessingeffectson pages 4-6) |
| AlSi10Mg (LPBF) | Shot-blasted + machine oil (worst case in Sagbas 2020) | Ball-on-disc; 6 mm Al2O3 ball; 10 N; 300 rpm; 10,600 cycles; machine oil | 0.1356 ± 0.005 | 6.92E-04 mm^3/N·m | Highest COF in study; rough, hard, positively skewed surface texture increased asperity interaction | (sagbas2020postprocessingeffectson pages 2-4, sagbas2020postprocessingeffectson pages 4-6) |
| AlSi10Mg (LPBF) | Polished + machine oil (highest wear in Sagbas 2020) | Ball-on-disc; 6 mm Al2O3 ball; 10 N; 300 rpm; 10,600 cycles; machine oil | 0.1083 ± 0.003 | 7.92E-04 mm^3/N·m | Highest wear rate in study | (sagbas2020postprocessingeffectson pages 4-6) |
| Al-3.5Cu-1.5Mg-1Si (SLM) | As-built | Pin-on-disk; X210Cr12 steel disk; 15 N; 400 rpm; 60 min; sliding distance 4521 m; 313–323 K | 0.40 ± 0.01 | 1.80 ± 0.11 × 10^-4 mm^3/N·m | Hardness 124 ± 1 HV0.05; lower wear than AA2024-O | (wang2021wearbehaviorof pages 2-4, wang2021wearbehaviorof pages 4-7, wang2021wearbehaviorof pages 1-2, wang2021wearbehaviorof pages 7-9) |
| Al-3.5Cu-1.5Mg-1Si (SLM) | T6 | Pin-on-disk; X210Cr12 steel disk; 15 N; 400 rpm; 60 min; sliding distance 4521 m; 313–323 K | 0.34 ± 0.01 | 1.48 ± 0.02 × 10^-4 mm^3/N·m | Hardness 176 ± 1 HV0.05; best wear in Wang 2021 dataset; nano Al2Cu(Mg) and Mg2Si precipitates improve wear | (wang2021wearbehaviorof pages 2-4, wang2021wearbehaviorof pages 4-7, wang2021wearbehaviorof pages 1-2, wang2021wearbehaviorof pages 7-9) |
| AA2024 comparator | O temper | Same pin-on-disk setup as above; X210Cr12 steel disk; 15 N; 4521 m | 0.47 ± 0.02 | 2.23 ± 0.01 × 10^-4 mm^3/N·m | Hardness 73 ± 1 HV0.05; worst wear in Wang 2021 comparison | (wang2021wearbehaviorof pages 4-7) |
| AA2024 comparator | T6 | Same pin-on-disk setup as above; X210Cr12 steel disk; 15 N; 4521 m | 0.36 ± 0.01 | 1.74 ± 0.08 × 10^-4 mm^3/N·m | Hardness 179 ± 1 HV0.05; improved over AA2024-O but slightly above SLM-T6 wear | (wang2021wearbehaviorof pages 4-7) |
| Al8SiCu (PBF-LB) | Unreinforced alloy | Tribological test conditions not given in extracted text; figure/text report average values | 0.655 | 1.76 × 10^-3 mm^3/N·m | Baseline alloy for TiB2 addition study | (he2024effectsofin pages 1-2, he2024effectsofin pages 8-12, he2024effectsofin media bfc55b3b) |
| TiB2/Al8SiCu (PBF-LB) | In situ TiB2-reinforced composite | Tribological test conditions not given in extracted text; figure/text report average values | 0.580 | 1.38 × 10^-3 mm^3/N·m | TiB2 reduced COF and wear rate via grain refinement/hardness increase; still notably worse than best Al-Cu-Mg-Si and Scalmalloy values | (he2024effectsofin pages 1-2, he2024effectsofin pages 8-12, he2024effectsofin media bfc55b3b) |
| AlMgScZr / Scalmalloy® (LPBF) | As-built literature value cited by Abrami 2021 from Zhang et al. 2018 | Ball-on-disk style prior-literature value; Abrami test conditions for related work: ASTM G99 dry pin-on-disk, 100Cr6 steel ball 6 mm, 1 N, 0.04 m/s, 6 mm track diameter | 0.61 | 1.74 × 10^-4 mm^3/N·m | Indicates better wear performance than AlSi10Mg under similar conditions per Abrami discussion | (abrami2021hightemperaturewear pages 1-3) |
| AlMgScZr / Scalmalloy® (LPBF) | Annealed 325 °C/4 h; 25–200 °C tests | ASTM G99 dry pin-on-disk; 100Cr6 steel ball 6 mm; 1 N; 0.04 m/s; 6 mm track; room temp to 200 °C | ~0.5–0.6 at RT, rising to ~0.8–0.9 at 200 °C | Wear rate described as nearly temperature-insensitive up to 200 °C; explicit k not reported in extracted text | Wear mainly tribo-oxidative up to 100 °C; adhesive contribution at 150–200 °C | (abrami2021hightemperaturewear pages 8-9, abrami2021hightemperaturewear pages 1-3) |
| Scalmalloy® (LPBF) | SN orientation, 20 N | Dry sliding tests at 20/40/60 N; steady-state COF averaged over 600–2500 m; exact counterpart/motion type not fully stated in extracted text | COF within overall ~0.45–0.8 range; lowest at 20 N | Volumetric wear rate ≈ 4.2 mm^3/m at 20 N (not normalized by N·m) | Lowest wear among SN/BN/BP at 20 N; scanning plane harder (~95.2 HV) than building plane (~89.5 HV) | (abdi2024microstructureinducedanisotropictribological pages 15-16, abdi2024microstructureinducedanisotropictribological pages 10-13) |
| Scalmalloy® (LPBF) | BN orientation, 20 N | Same as above | COF within overall ~0.45–0.8 range; higher than SN at highest load | Volumetric wear rate ≈ 8.2 mm^3/m at 20 N (not normalized by N·m) | Highest wear at 20 N; stronger load sensitivity than SN; 20→40 N wear rate decreased 37%, then rose 25% at 60 N | (abdi2024microstructureinducedanisotropictribological pages 15-16, abdi2024microstructureinducedanisotropictribological pages 10-13) |


*Table: This table compiles quantitative tribological results for LPBF/SLM aluminum alloys and closely related Al-based LPBF composites, including wear rates, COF, and key test conditions. It supports comparison of which alloy systems and post-process states show the best wear resistance.*

### AlSi10Mg (LPBF/DMLS)
Ball-on-disc tests against an Al2O3 ball at 10 N show that surface treatments strongly affect both friction and wear. In water-lubricated tests, **shot peening** increased COF but reduced wear relative to polishing: COF **0.1242 ± 0.005** and k **6.34×10⁻⁴ mm³/N·m** (shot peened) vs COF **0.0862 ± 0.003** and k **7.86×10⁻⁴ mm³/N·m** (polished). (sagbas2019investigatingthetribologicala pages 4-6)

Under oil lubrication (palm oil/soybean oil/machine oil), the same ball-on-disc configuration (Al2O3 ball, 10 N, 300 rpm, 10,600 cycles) yields a k range from **3.88×10⁻⁴ to 7.92×10⁻⁴ mm³/N·m** depending on finishing/lubricant, with **shot-peened + palm oil** giving the lowest wear rate (k **3.88×10⁻⁴ mm³/N·m**, COF **0.0996 ± 0.005**) and **polished + machine oil** the highest wear rate (k **7.92×10⁻⁴ mm³/N·m**, COF **0.1083 ± 0.003**). (sagbas2020postprocessingeffectson pages 4-6)

### Heat-treatable Al–Cu–Mg–Si made by SLM (Al-3.5Cu-1.5Mg-1Si)
Pin-on-disk testing (15 N) against hardened steel (X210Cr12) shows substantially lower wear than the AlSi10Mg datasets above. The **as-built SLM** condition reports COF **0.40 ± 0.01** with k **(1.80 ± 0.11)×10⁻⁴ mm³/N·m**; after **T6**, COF decreases to **0.34 ± 0.01** with k **(1.48 ± 0.02)×10⁻⁴ mm³/N·m**. (wang2021wearbehaviorof pages 4-7)

In the same study (same test setup), comparator AA2024 shows k **2.23×10⁻⁴ mm³/N·m** (AA2024-O) and **1.74×10⁻⁴ mm³/N·m** (AA2024-T6), indicating the SLM alloy is competitive with or better than AA2024 for wear in this configuration. (wang2021wearbehaviorof pages 4-7)

### Scalmalloy® (Al–Mg–Sc–Zr)
Abrami et al. (LPBF Scalmalloy, ASTM G99 conditions reported as 100Cr6 steel ball, 1 N, 0.04 m/s, 6 mm track) cite prior ball-on-disk results for **as-built AlMgScZr** of COF **0.61** and k **1.74×10⁻⁴ mm³/N·m** (Zhang et al. 2018, as cited by Abrami). (abrami2021hightemperaturewear pages 1-3)

A separate Scalmalloy study reports strong microstructure/orientation and load effects, with COF broadly **~0.45–0.8** and an example of volumetric wear rate at 20 N of **~4.2 mm³/m (SN orientation, lowest)** vs **~8.2 mm³/m (BN orientation, highest)**; these values are not normalized to N·m in the extracted text, so they are not directly comparable to k without additional test-condition details. (abdi2024microstructureinducedanisotropictribological pages 15-16, abdi2024microstructureinducedanisotropictribological pages 10-13)

### Al–Si–Cu (Al8SiCu) and in-situ TiB₂ reinforcement (LPBF)
A PBF-LB study reports that adding in situ TiB₂ reduces both friction and wear rate: COF decreases from **0.655 to 0.580** and k from **1.76×10⁻³ to 1.38×10⁻³ mm³/N·m** (Al8SiCu → TiB₂/Al8SiCu). (he2024effectsofin pages 1-2, he2024effectsofin media bfc55b3b)

## Which LPBF aluminum alloy systems show best wear resistance?
Within the quantitative wear-rate evidence assembled here (noting that cross-paper comparisons remain test-condition dependent), the lowest specific wear rates are:

1. **SLM Al–Cu–Mg–Si (Al-3.5Cu-1.5Mg-1Si), especially after T6**: k ≈ **1.48×10⁻⁴ mm³/N·m** with COF ≈ **0.34** under a 15 N pin-on-disk test vs hardened steel. (wang2021wearbehaviorof pages 4-7)
2. **Scalmalloy® (Al–Mg–Sc–Zr)**: k ≈ **1.74×10⁻⁴ mm³/N·m** (as cited) with COF ≈ **0.61** in a ball-on-disk configuration. (abrami2021hightemperaturewear pages 1-3)

In contrast, the reported AlSi10Mg values are higher (worse wear) at ~**(0.4–0.8)×10⁻³ mm³/N·m**, and the Al8SiCu/TiB₂–Al8SiCu values are still higher at ~**(1.4–1.8)×10⁻³ mm³/N·m**. (sagbas2020postprocessingeffectson pages 4-6, he2024effectsofin media bfc55b3b)

## Notes on interpretation and limitations
Reported wear rates depend strongly on counterpart material, load, speed, environment/lubrication, and surface finish. As a result, the above ‘best’ ranking is most defensible **within each study’s controlled comparisons** (e.g., shot-peened vs polished AlSi10Mg; Al8SiCu vs TiB₂/Al8SiCu; as-built vs T6 Al–Cu–Mg–Si), and only suggestive across different papers that used different test configurations. (sagbas2019investigatingthetribologicala pages 4-6, wang2021wearbehaviorof pages 4-7, he2024effectsofin media bfc55b3b)

---

## Query 9

**Question:** What are the density values and specific strength (strength-to-weight ratio) for different AM aluminum alloys? Rank alloy systems by specific yield strength and specific UTS.

**Task ID:** `5349a2d9-056f-43b6-91ba-c4f5247625a8`

**Status:** complete

This synthesis compiles *explicitly reported* density and tensile strengths for additively manufactured (AM) aluminum alloys from the retrieved literature, and uses them to compute and rank specific yield strength and specific ultimate tensile strength (UTS). Only alloy conditions with both density and strength explicitly stated in the available excerpts can be included in the quantitative rankings.

## Data extracted and specific-strength calculations
| Alloy system | AM process | Condition | Density (g/cm^3) | Yield strength YS (MPa) | UTS (MPa) | Specific YS (MPa/(g/cm^3)) | Specific UTS (MPa/(g/cm^3)) | Notes |
|---|---|---|---:|---:|---:|---:|---:|---|
| AlSi10Mg | AM-SLM | Stress-relieved | 2.63 (uzan2018hightemperaturemechanicalproperties pages 5-11) | 204 (uzan2018hightemperaturemechanicalproperties pages 5-11) | 358 (uzan2018hightemperaturemechanicalproperties pages 5-11) | 77.6 | 136.1 | 25°C tensile test; average density reported as 2630 kg/m^3 = 98.5% theoretical (uzan2018hightemperaturemechanicalproperties pages 5-11) |
| Scalmalloy® (Al-Mg-Sc) | SLM | As-built | 2.7 (jakkula2021strainratesensitivity pages 1-2) | 263.2 (jakkula2021strainratesensitivity pages 2-5) | 368.4 (jakkula2021strainratesensitivity pages 2-5) | 97.5 | 136.4 | Strain rate = 0.001 s^-1 (jakkula2021strainratesensitivity pages 2-5) |
| Scalmalloy® (Al-Mg-Sc) | SLM | Heat-treated | 2.7 (jakkula2021strainratesensitivity pages 1-2) | 465.6 (jakkula2021strainratesensitivity pages 2-5) | 518.6 (jakkula2021strainratesensitivity pages 2-5) | 172.4 | 192.1 | Strain rate = 0.001 s^-1 (jakkula2021strainratesensitivity pages 2-5) |


*Table: This table compiles the AM aluminum alloy conditions for which the evidence explicitly reported both density and tensile strengths, then calculates specific yield strength and specific UTS. It is useful for directly comparing strength-to-weight performance across the available alloy systems and conditions.*

## Rankings by specific yield strength
Specific yield strength is computed as YS/ρ (MPa/(g/cm^3)).

1. **Scalmalloy® (Al–Mg–Sc), SLM, heat-treated**: 172.4 MPa/(g/cm^3) (jakkula2021strainratesensitivity pages 1-2, jakkula2021strainratesensitivity pages 2-5)
2. **Scalmalloy® (Al–Mg–Sc), SLM, as-built**: 97.5 MPa/(g/cm^3) (jakkula2021strainratesensitivity pages 1-2, jakkula2021strainratesensitivity pages 2-5)
3. **AlSi10Mg, AM-SLM, stress-relieved**: 77.6 MPa/(g/cm^3) (uzan2018hightemperaturemechanicalproperties pages 5-11)

## Rankings by specific UTS
Specific UTS is computed as UTS/ρ (MPa/(g/cm^3)).

1. **Scalmalloy® (Al–Mg–Sc), SLM, heat-treated**: 192.1 MPa/(g/cm^3) (jakkula2021strainratesensitivity pages 1-2, jakkula2021strainratesensitivity pages 2-5)
2. **Scalmalloy® (Al–Mg–Sc), SLM, as-built**: 136.4 MPa/(g/cm^3) (jakkula2021strainratesensitivity pages 1-2, jakkula2021strainratesensitivity pages 2-5)
3. **AlSi10Mg, AM-SLM, stress-relieved**: 136.1 MPa/(g/cm^3) (uzan2018hightemperaturemechanicalproperties pages 5-11)

## Notes on condition dependence and coverage limitations
- **Condition/test dependence:** The Scalmalloy values used here come from a strain-rate study; the tabulated strengths quoted are at **0.001 s−1** (quasi-static) for both as-built and heat-treated material (jakkula2021strainratesensitivity pages 2-5). The AlSi10Mg values used here are for **stress-relieved** material at **25 °C**, and the same source reports that both YS and UTS drop substantially at elevated temperature (uzan2018hightemperaturemechanicalproperties pages 5-11).
- **AlSi10Mg heat treatment:** Separate work reports substantially higher YS/UTS for AlSi10Mg in the as-built and modified T5 conditions (e.g., YS 263–298 MPa and UTS 473–479 MPa), but density was not explicitly reported in the provided excerpt and therefore those conditions could not be included in the specific-strength ranking (rosenthal2018heattreatmenteffect pages 14-21).
- **AA6061 and AA2195 (Al–Li):** LPBF AA6061 tensile strengths (as-fabricated and after a T6-style heat treatment) and LPBF AA2195 (2195 Al–Cu–Li) relative densities and strengths are reported in the retrieved sources, but at least one required component (explicit g/cm^3 density for AA6061 in the excerpt; explicit g/cm^3 density for AA2195) is missing, preventing a fully evidence-grounded specific-strength calculation and ranking for those alloy families from the currently available text snippets (uddin2018processingandcharacterization pages 17-21, qi2020ahighstrength pages 1-2, qi2020ahighstrength pages 2-4).

---

## Query 10

**Question:** What compressive mechanical properties have been reported for LPBF aluminum alloys? Include data on lattice structures and foams. How do compressive properties differ from tensile?

**Task ID:** `67fb5399-9f5f-4d99-bc11-5098bcdb0d76`

**Status:** complete

## Scope
This answer summarizes *reported* compressive mechanical properties for laser powder bed fusion (LPBF; including SLM/PBF‑LB) aluminum alloys, covering (i) dense/bulk material and (ii) architected porous materials (lattices, TPMS “foam-like” cellular structures, and graded porous metamaterials). It then contrasts compression vs tension using directly reported paired datasets.

## Reported compressive properties for LPBF aluminum alloys (dense, lattices, and foams)
| Material / structure | Condition | Key geometry / relative density | Compressive metrics reported | Tensile metrics reported | Notes |
|---|---|---|---|---|---|
| LPBF AlSi10Mg, dense/bulk | Artificially aged; build orientation 0/0 | Dense specimens; orientation 0/0 | **Compression:** E = 74.2 ± 2.2 GPa; compressive yield strength Rdp = 227 ± 14 MPa | **Tension:** E = 73.5 ± 2.7 GPa; Rp0.2 = 225 ± 6 MPa; Rm = 364 ± 5 MPa; At = 6.5 ± 0.2% | In this orientation, tensile and compressive yield strengths are very similar; compressive modulus is slightly higher. (sert2020tensileandcompressive pages 5-7, sert2020tensileandcompressive media 3c15618f) |
| LPBF AlSi10Mg, dense/bulk | Artificially aged; build orientation 90/0 | Dense specimens; orientation 90/0 | **Compression:** E = 79.1 ± 0.5 GPa; compressive yield strength Rdp = 300 ± 9 MPa | **Tension:** E = 74.8 ± 1.0 GPa; Rp0.2 = 205 ± 5 MPa; Rm = 377 ± 5 MPa; At = 3.3 ± 0.2% | Clear tension/compression asymmetry at 90/0: compressive yield exceeds tensile yield by ~95 MPa; porosity is less detrimental in compression because pores tend to close. Across all orientations, compression E ≈ 73.5–79.8 GPa and Rdp ≈ 218–300 MPa. (sert2020tensileandcompressive pages 5-7) |
| Pulsed-LPBF Al10SiMg, dense/bulk | As-built | ~99% dense | **True compression:** yield strength = 380 MPa; ultimate compressive strength = 485 MPa; compressive fracture strain = 20.0% | Not numerically reported in extracted pages; paper compares favorably with CW-LPBF/cast tensile values qualitatively | As-built P-LPBF shows high hardness (136 ± 4 HV) and high compressive strength due to refined cellular Al-Si network. (chou2017microstructureandmechanical pages 6-7) |
| Pulsed-LPBF Al10SiMg, dense/bulk | T6 | ~99% dense | **True compression:** YS and UCS can drop to ~250 MPa and ~320 MPa; compressive fracture strain rises to 49.6% | Not numerically reported in extracted pages | T6 reduces strength but strongly increases ductility; hardness drops to 112 ± 3 HV. (chou2017microstructureandmechanical pages 6-7) |
| LPBF AlSi10Mg lattice | BCC unit cell | Relative density ρ*/ρs = 0.16 | Initial densification strain = 53% experimental (59% geometric estimate) | — | BCC shows shear-band formation and crack initiation; lower plateau performance than TO. (liu2020compressivepropertiesof pages 10-14) |
| LPBF AlSi10Mg lattice | Truncated octahedron (TO) unit cell | Relative density ρ*/ρs = 0.17; best energy case reported at RD = 0.27 | Initial densification strain = 59% experimental (66% estimate); highest stiffness/plateau stress among BCC/TO/Hexa; maximum energy absorption in study = **11.4 MJ/m³** at RD 0.27 | — | TO bears high stress more uniformly and showed the best energy absorption of the three unit cells. (liu2020compressivepropertiesof pages 10-14) |
| LPBF AlSi10Mg lattice | Hexa unit cell | Relative density ρ*/ρs = 0.18 | Initial densification strain = 37% experimental (34% estimate) | — | Hexa shows flatter plateau and less shear-banding, but densifies earlier because of more struts aligned with loading direction. (liu2020compressivepropertiesof pages 10-14) |
| LPBF AlSi10Mg sheet TPMS cellular structure (IWP) | As-built vs heat-treated example | Relative density example: 19% designed, ~17.25% by CT | Peak strength at 19% RD decreases **22 → 14 MPa** after heat treatment; plateau strength **σP defined as average stress from 20–40% strain**; toughness U = area under curve to 40% strain | Base material tensile (as-built bulk): E = 55.2 GPa; UTS = 352.7 MPa; YS = 246.6 MPa; ef = 4.0% | Heat treatment smooths the compression curve and promotes collective collapse, but reduces peak strength. (alhammadi2020microstructuralcharacterizationand pages 6-9) |
| LPBF AlSi10Mg sheet TPMS cellular structure (IWP) | Heat-treated base material comparison | Bulk base material tested after heat treatment | Cellular stiffness scaling exponent at RT = 1.50, decreasing to 1.10 at 150 °C | Bulk tensile after HT-150: E = 22.5 GPa; UTS = 157.8 MPa; YS = 108.8 MPa; ef = 32.6% | Elevated temperature / heat treatment reduce bulk tensile strength strongly and make cellular response smoother and more ductile. (alhammadi2020microstructuralcharacterizationand pages 6-9) |
| LPBF AlSi10Mg gradient metamaterial | GS type | Apparent density 0.796 g/cm³ | W10% = 2.82 ± 0.03 MJ/m³; **W50% = 23.57 ± 0.02 MJ/m³**; **SW50% = 0.030 MJ/kg**; densification onset ~55–70% strain | — | GS is among the best performers; sheet-based gradient structure with high specific energy absorption. (sun2024compressivemechanicaland pages 13-15, sun2024compressivemechanicaland media e36a686d) |
| LPBF AlSi10Mg gradient metamaterial | GL type | Apparent density 1.472 g/cm³ | W10% = 5.36 ± 0.03 MJ/m³; **W50% = 34.08 ± 0.26 MJ/m³**; **SW50% = 0.023 MJ/kg**; densification onset ~55–70% strain | — | GL gives the highest volumetric energy absorption among the listed types, while GS gives higher specific energy absorption. (sun2024compressivemechanicaland pages 13-15, sun2024compressivemechanicaland media e36a686d) |


*Table: This table compiles reported compressive properties for dense LPBF AlSi10Mg and Al10SiMg, plus lattice, TPMS cellular, and gradient metamaterial structures. It is useful for comparing bulk compression with architected-porous behavior and for contrasting compressive and tensile metrics where both were reported.*

### Dense/bulk LPBF AlSi10Mg / Al10SiMg
Sert et al. measured both tensile and compressive properties for LPBF AlSi10Mg as a function of build orientation, reporting compression modulus **E ≈ 73.5–79.8 GPa** and compressive yield strength **Rdp ≈ 218–300 MPa** (room temperature). (sert2020tensileandcompressive pages 5-7)

Chou et al. (pulsed‑LPBF Al10SiMg) reported substantially higher *true* compressive strengths for as-built material: **true compressive YS = 380 MPa** and **true UCS = 485 MPa**, with a compressive fracture strain of **20.0%**. After T6, compressive strengths can drop to roughly **YS ≈ 250 MPa** and **UCS ≈ 320 MPa**, while compressive fracture strain increases to **49.6%**. (chou2017microstructureandmechanical pages 6-7)

### LPBF AlSi10Mg lattices (periodic unit cells)
For AlSi10Mg lattice structures with BCC, truncated-octahedron (TO), and Hexa unit cells, Liu et al. reported relative densities ~0.16–0.18 and *experimental* initial densification strains of **53% (BCC)**, **59% (TO)**, and **37% (Hexa)**. The maximum energy absorption reported in that study was **11.4 MJ/m³** for the **TO** lattice at relative density **0.27**. (liu2020compressivepropertiesof pages 10-14)

Yu et al. reported compression strength–relative density scaling behavior across multiple AlSi10Mg microlattice unit cells (cubic and tetrahedral families), including bend‑dominated vs buckling‑dominated scaling regimes, and reported high maximum compressive strengths (e.g., a maximum strength of **221.9 MPa** in their test matrix). (yu2019structurepropertyrelationshipin pages 7-10)

### “Foam-like” LPBF porous aluminum (TPMS sheet cellular and graded porous metamaterials)
Alhammadi et al. studied LPBF AlSi10Mg TPMS sheet cellular structures at relative densities ~10–19% and defined **plateau strength σP as the average stress from 20–40% strain** and energy absorption (toughness) as the area under the stress–strain curve up to 40% strain. For a representative **19% relative-density** cellular sample, the **peak compressive strength decreased from 22 MPa (as-built) to 14 MPa (heat-treated)**, while the compression response became smoother/more ductile after heat treatment. (alhammadi2020microstructuralcharacterizationand pages 6-9)

Sun et al. reported volumetric and specific energy absorption for LPBF AlSi10Mg *gradient* porous metamaterials and noted densification onset at approximately **55–70% strain**. For example, type **GS** (apparent density 0.796 g/cm³) achieved **W50% = 23.57 MJ/m³** and **SW50% = 0.030 MJ/kg**, while type **GL** (1.472 g/cm³) achieved **W50% = 34.08 MJ/m³** (with lower SW50% = 0.023 MJ/kg). (sun2024compressivemechanicaland pages 13-15, sun2024compressivemechanicaland media e36a686d)

## How compressive properties differ from tensile in LPBF aluminum alloys

### 1) Dense LPBF AlSi10Mg: compression can show higher yield than tension, depending on orientation
A direct paired dataset (same study, same material) shows that tension–compression yield asymmetry can be small or large depending on build orientation. In Sert et al., at 0/0 the tensile and compressive yields were essentially the same (**Rp0.2 ≈ 225 MPa** vs **Rdp ≈ 227 MPa**), whereas at 90/0 compressive yield was much higher (**Rdp ≈ 300 MPa**) than tensile yield (**Rp0.2 ≈ 205 MPa**). (sert2020tensileandcompressive pages 5-7)

### 2) Porosity is generally less damaging in compression than in tension
Sert et al. explicitly note that under compression “the nature of the load tends to close the pores,” whereas under tension pores “expand, coalesce and spread in the form of cracks that lead to failure.” This provides a mechanistic basis for why tensile ductility/strength can degrade more strongly than compressive yield/flow in porous or slightly defective LPBF Al. (sert2020tensileandcompressive pages 5-7)

### 3) Modulus: compression modulus is similar to (or slightly higher than) tensile modulus in LPBF AlSi10Mg
In the same paired dataset, Young’s modulus in compression is similar to or modestly larger than tensile modulus (e.g., at 90/0: **Ecomp ≈ 79.1 GPa** vs **Etens ≈ 74.8 GPa**). (sert2020tensileandcompressive pages 5-7)

### 4) Architected porous structures: compression is governed by collapse/plateau/densification rather than uniform plastic flow
For lattices and foam-like porous structures, compression is characterized by an initial elastic regime followed by progressive collapse and a plateau (often with stress oscillations) until densification; properties of interest shift from “UTS/elongation” to plateau stress, densification strain, and energy absorption. This is reflected in: (i) lattice densification strains (e.g., 37–59% depending on unit cell) and energy absorption values (e.g., 11.4 MJ/m³ for TO lattice) (liu2020compressivepropertiesof pages 10-14) and (ii) porous metamaterial densification onset at ~55–70% strain and high absorbed energy to 50% strain (sun2024compressivemechanicaland pages 13-15).

### 5) Heat treatment often decreases peak/plateau stress but increases ductility/smoothness in compression
For dense pulsed‑LPBF Al10SiMg, T6 decreased compressive strengths (e.g., YS/UCS dropping to ~250/320 MPa) but greatly increased compressive fracture strain (20.0% → 49.6%). (chou2017microstructureandmechanical pages 6-7)

For TPMS sheet cellular AlSi10Mg, heat treatment reduced a representative peak strength (22 → 14 MPa at ~19% relative density) and shifted deformation to more collective collapse with reduced stress fluctuations. (alhammadi2020microstructuralcharacterizationand pages 6-9)

## Evidence limitations
The retrieved full texts with explicit numerical compression properties were dominated by AlSi10Mg/Al10SiMg and AlSi10Mg-based cellular metamaterials; comparable dense compression datasets for other LPBF Al alloys (e.g., Scalmalloy®, Al‑Cu 2xxx, Al‑Zn 7xxx) were not present in the available evidence snippets, so they are not tabulated here. (sert2020tensileandcompressive pages 5-7, chou2017microstructureandmechanical pages 6-7)

---

