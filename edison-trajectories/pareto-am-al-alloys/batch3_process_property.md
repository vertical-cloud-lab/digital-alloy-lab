# Batch 3: Process-Property, Corrosion, Printability, Novel Design

*Edison Scientific LITERATURE queries for AM Al alloy Pareto front identification*

## Query 1

**Question:** What corrosion resistance data has been reported for LPBF aluminum alloys? Compare electrochemical corrosion behavior (Ecorr, icorr, pitting potential) across AlSi10Mg, Scalmalloy, 2xxx, 7xxx, and Al-Ce systems. How does LPBF processing affect corrosion compared to wrought/cast equivalents?

**Task ID:** `484388ce-6954-4e95-adf5-ed6cc862040e`

**Status:** complete

## Scope and limitations of retrieved evidence
This answer compares electrochemical corrosion metrics that were *directly retrievable from the current tool-accessible full texts* for LPBF (and closely related laser AM) aluminum alloys. Quantitative potentiodynamic parameters (Ecorr, icorr) were obtained for AlSi10Mg, an Al–Cu–Li 2xxx alloy (AA2099), and two 7xxx-type systems (a laser-AM 7075 vs forged 7075 comparison, and an LPBF high-solute Al–Zn–Mg–Cu–Si–Zr–Er alloy). In contrast, within the retrieved corpus I could not access full-text numeric polarization data (Ecorr/icorr/Epit) for LPBF Scalmalloy (Al–Mg–Sc–Zr) or for LPBF Al–Ce alloys; therefore, those two families are explicitly flagged as “not available” rather than inferred. (plotkowski2020microstructureandproperties pages 10-12, plotkowski2020microstructureandproperties pages 12-13)

## Consolidated corrosion resistance data (Ecorr, icorr, pitting potential)
The table below compiles the numerical electrochemical parameters and test conditions that were explicitly reported in the retrieved texts.

| Alloy system | Process condition | Electrolyte | Reference electrode | Scan protocol (if available) | Ecorr | icorr | Pitting / breakdown potential | Notes on microstructure / corrosion mode | Source context IDs |
|---|---|---|---|---|---|---|---|---|---|
| AlSi10Mg | LPBF as-built S0 | 3.5 wt% NaCl | Ag/AgCl | Potentiodynamic polarization + Tafel; detailed scan rate not in retrieved excerpt | −663 ± 11 mV | 7.3 ± 0.1 µA/cm² | Not reported in retrieved excerpt | Baseline LPBF condition; lower corrosion resistance than ECAP states | (snopinski2022evolutionofmicrostructure pages 9-12) |
| AlSi10Mg | LPBF heat-treated S2 (300 °C) | 3.5 wt% NaCl | Ag/AgCl | Potentiodynamic polarization + Tafel; detailed scan rate not in retrieved excerpt | −693 ± 21 mV | 18.5 ± 0.4 µA/cm² | Not reported in retrieved excerpt | Heat treatment made Ecorr more negative and increased icorr; coarser Si / melt-pool-boundary susceptibility | (snopinski2022evolutionofmicrostructure pages 9-12, snopinski2022evolutionofmicrostructure pages 14-16) |
| AlSi10Mg | LPBF heat-treated + 1 ECAP pass S2-1 | 3.5 wt% NaCl | Ag/AgCl | Potentiodynamic polarization + Tafel; detailed scan rate not in retrieved excerpt | −550 ± 17 mV | 0.3 ± 0.05 µA/cm² | Not reported in retrieved excerpt | ECAP strongly improved resistance; denser/thicker oxide, lower porosity, only small pits observed | (snopinski2022evolutionofmicrostructure pages 12-14, snopinski2022evolutionofmicrostructure pages 9-12, snopinski2022evolutionofmicrostructure pages 14-16, snopinski2022evolutionofmicrostructure media ecb11778) |
| AlSi10Mg | LPBF heat-treated + 2 ECAP passes S2-2 | 3.5 wt% NaCl | Ag/AgCl | Potentiodynamic polarization + Tafel; detailed scan rate not in retrieved excerpt | −440 ± 14 mV | 0.2 ± 0.04 µA/cm² | Not reported in retrieved excerpt | Best Ecorr/icorr among retrieved AlSi10Mg states; some localized attack still possible at overlapping melt-pool boundaries / α-Al–Si interfaces | (snopinski2022evolutionofmicrostructure pages 12-14, snopinski2022evolutionofmicrostructure pages 9-12, snopinski2022evolutionofmicrostructure pages 14-16, snopinski2022evolutionofmicrostructure media ecb11778) |
| Al–Cu–Li AA2099 | Conventional T83 | 0.1 M NaCl | Not stated in retrieved excerpt | OCP 1 h; potentiodynamic polarization; Tafel on anodic branch | −662 ± 5 mV | 0.97 ± 0.3 µA/cm² | No clear passive region or pitting potential observed | Best corrosion performance among retrieved AA2099 conditions despite slightly more negative Ecorr | (adjeikyeremeh2023preheatinginfluenceon pages 15-17, adjeikyeremeh2023preheatinginfluenceon pages 12-15) |
| Al–Cu–Li AA2099 | LPBF preheated 480 °C | 0.1 M NaCl | Not stated in retrieved excerpt | OCP 1 h; potentiodynamic polarization; Tafel on anodic branch | −643 ± 11 mV | 1.31 ± 0.6 µA/cm² | No clear passive region or pitting potential observed | AM state more noble than T83 but higher icorr; lower preheat retained better corrosion resistance than higher-preheat AM states | (adjeikyeremeh2023preheatinginfluenceon pages 15-17, adjeikyeremeh2023preheatinginfluenceon pages 12-15) |
| Al–Cu–Li AA2099 | LPBF preheated 500 °C | 0.1 M NaCl | Not stated in retrieved excerpt | OCP 1 h; potentiodynamic polarization; Tafel on anodic branch | −648 ± 8 mV | 5.11 ± 1.3 µA/cm² | No clear passive region or pitting potential observed | Corrosion worsened with increasing preheat due to more Cu-rich phases / PFZ effects | (adjeikyeremeh2023preheatinginfluenceon pages 15-17, adjeikyeremeh2023preheatinginfluenceon pages 12-15, adjeikyeremeh2023preheatinginfluenceon pages 17-19) |
| Al–Cu–Li AA2099 | LPBF preheated 520 °C | 0.1 M NaCl | Not stated in retrieved excerpt | OCP 1 h; potentiodynamic polarization; Tafel on anodic branch | −646 ± 3 mV | 10.3 ± 3 µA/cm² | No clear passive region or pitting potential observed | Worst retrieved AA2099 condition; higher preheat promoted Cu-rich grain-boundary phases and lower Rox / Rct | (adjeikyeremeh2023preheatinginfluenceon pages 15-17, adjeikyeremeh2023preheatinginfluenceon pages 12-15, adjeikyeremeh2023preheatinginfluenceon pages 17-19) |
| Al7075 | Forged | 3.5 wt% NaCl, 25 °C | Ag/AgCl | −1.2 to 0.2 V vs Ag/AgCl; 0.5 mV/s; initial potentiostatic reduction at −1.0 V for 3 min | −0.7790 V | 1.917 × 10⁻⁶ A/cm² | Not reported in retrieved excerpt | Slightly lower icorr than laser-AM sample; forging taken as conventional comparator | (zhang2021comparativestudyon pages 6-7, zhang2021comparativestudyon pages 7-9, zhang2021comparativestudyon pages 2-6) |
| Al7075 | Laser AM (LENS) | 3.5 wt% NaCl, 25 °C | Ag/AgCl | −1.2 to 0.2 V vs Ag/AgCl; 0.5 mV/s; initial potentiostatic reduction at −1.0 V for 3 min | −0.6817 V | 2.221 × 10⁻⁶ A/cm² | Not reported in retrieved excerpt | More noble Ecorr than forged, but slightly higher icorr; corrosion linked to defects / Cl⁻ enrichment at holes | (zhang2021comparativestudyon pages 6-7, zhang2021comparativestudyon pages 7-9, zhang2021comparativestudyon pages 2-6) |
| Al–Zn–Mg–Cu–Si–Zr–Er | LPBF as-printed (AP) | 3.5 wt% NaCl | SCE | OCP stabilized ~0.5 h; potentiodynamic polarization; Tafel extrapolation | −0.784 V | 1.822 µA/cm² | Not reported in retrieved excerpt | Wide / deep pits after testing; baseline for heat-treatment comparison | (zhang2023effectofpostheat pages 7-9, zhang2023effectofpostheat pages 1-3) |
| Al–Zn–Mg–Cu–Si–Zr–Er | LPBF direct aged (DA) | 3.5 wt% NaCl | SCE | OCP stabilized ~0.5 h; potentiodynamic polarization; Tafel extrapolation | −0.782 V | 1.921 µA/cm² | Not reported in retrieved excerpt | Worst retrieved corrosion ranking; strip-like Mg2Si at cellular boundaries promoted local anodic dissolution | (zhang2023effectofpostheat pages 7-9, zhang2023effectofpostheat pages 1-3, zhang2023effectofpostheat pages 9-11) |
| Al–Zn–Mg–Cu–Si–Zr–Er | LPBF T6 | 3.5 wt% NaCl | SCE | OCP stabilized ~0.5 h; potentiodynamic polarization; Tafel extrapolation | −0.801 V | 1.783 µA/cm² | Not reported in retrieved excerpt | Better than AP / DA; finer needle / rod Mg2Si and secondary Al3(Er,Zr) reduced local potential differences | (zhang2023effectofpostheat pages 7-9, zhang2023effectofpostheat pages 1-3, zhang2023effectofpostheat pages 9-11) |
| Al–Zn–Mg–Cu–Si–Zr–Er | LPBF RRA | 3.5 wt% NaCl | SCE | OCP stabilized ~0.5 h; potentiodynamic polarization; Tafel extrapolation | −0.816 V | 1.713 µA/cm² | Not reported in retrieved excerpt | Best retrieved corrosion ranking (RRA > T6 > AP > DA); narrow / shallow pits, lower HAGB fraction | (zhang2023effectofpostheat pages 7-9, zhang2023effectofpostheat pages 1-3, zhang2023effectofpostheat pages 9-11) |
| Al–Mg–Sc–Zr (Scalmalloy / related) | LPBF / Scalmalloy family | Not available in retrieved sources | Not available in retrieved sources | Not available in retrieved sources | Not available in retrieved sources | Not available in retrieved sources | Not available in retrieved sources | Relevant LPBF corrosion papers were identified by search, but accessible retrieved text did not provide extractable numeric polarization data | (plotkowski2020microstructureandproperties pages 10-12, palmer2024useofcoredc pages 9-15, bertone2025caratterizzazionedelcomportamento pages 20-24, bertone2025caratterizzazionedelcomportamento pages 27-33) |
| Al–Ce system | AM Al–Ce / Al–Ce–Mn | Not available in retrieved sources | Not available in retrieved sources | Not available in retrieved sources | Not available in retrieved sources | Not available in retrieved sources | Not available in retrieved sources | Retrieved AM Al–10Ce–8Mn source discussed microstructure / properties, not electrochemical corrosion; no numeric LPBF corrosion polarization data accessible | (plotkowski2020microstructureandproperties pages 10-12, plotkowski2020microstructureandproperties pages 12-13) |


*Table: This table compiles the electrochemical corrosion parameters that were actually retrievable from the available sources for additively manufactured aluminum alloys, alongside test conditions and microstructural interpretation. It also flags where requested Scalmalloy and Al-Ce LPBF corrosion numbers were not accessible in the retrieved corpus.*

### AlSi10Mg (LPBF)
In 3.5 wt% NaCl vs Ag/AgCl, LPBF AlSi10Mg showed Ecorr ≈ −0.66 to −0.69 V and icorr ranging from ~7.3 µA/cm² (as-built) to ~18.5 µA/cm² after a 300 °C heat treatment (worse), while subsequent ECAP (severe plastic deformation post-processing of the LPBF material) shifted Ecorr nobler and reduced icorr dramatically to ~0.2–0.3 µA/cm². (snopinski2022evolutionofmicrostructure pages 9-12, snopinski2022evolutionofmicrostructure media ecb11778)

Although the Snopiński et al. table is titled “pitting corrosion test,” the retrieved excerpt does not provide explicit pitting potential/breakdown potential values, so Epit/Eb cannot be compared from this source. (snopinski2022evolutionofmicrostructure pages 9-12)

### 2xxx (Al–Cu–Li AA2099; LPBF vs conventional T83)
In 0.1 M NaCl, conventional AA2099-T83 exhibited the lowest icorr (~0.97 µA/cm²), whereas LPBF AA2099 produced with higher in situ preheating temperatures showed progressively higher icorr (~1.31 → 5.11 → 10.3 µA/cm² for 480 → 500 → 520 °C preheat). (adjeikyeremeh2023preheatinginfluenceon pages 15-17)

The same source explicitly reports that both conventional T83 and LPBF conditions showed “no passive region or clear pitting potential” on the potentiodynamic scans under those conditions, so pitting potential comparisons are not available for AA2099 in this dataset. (adjeikyeremeh2023preheatinginfluenceon pages 12-15)

### 7xxx (Al7075; laser AM (LENS) vs forging)
In 3.5 wt% NaCl at 25 °C, using Ag/AgCl, Zhang et al. reported that the forged 7075 had Ecorr = −0.7790 V and icorr = 1.917×10−6 A/cm², while the laser additively manufactured (LENS) 7075 had a nobler Ecorr = −0.6817 V but a slightly higher icorr = 2.221×10−6 A/cm². (zhang2021comparativestudyon pages 6-7, zhang2021comparativestudyon pages 2-6)

The scan protocol was specified (−1.2 to 0.2 V vs Ag/AgCl at 0.5 mV/s, plus a short pre-reduction step), but pitting/breakdown potentials were not reported in the retrieved excerpt. (zhang2021comparativestudyon pages 2-6)

### 7xxx-like multicomponent Al–Zn–Mg–Cu–Si–Zr–Er (LPBF; post-heat treatments)
In 3.5 wt% NaCl using an SCE reference, the LPBF Al–Zn–Mg–Cu–Si–Zr–Er alloy showed icorr ~1.7–1.9 µA/cm² with modest variation across post-heat treatments, with corrosion resistance ranked RRA > T6 > as-printed (AP) > direct aged (DA) based on icorr. (zhang2023effectofpostheat pages 7-9)

No pitting/breakdown potentials were retrievable from the excerpts; the study’s discrimination among conditions was based on icorr and post-test pit morphology. (zhang2023effectofpostheat pages 7-9)

### Scalmalloy (Al–Mg–Sc–Zr) and Al–Ce systems
Within the tool-retrieved full texts in this run, I did not obtain extractable numeric potentiodynamic corrosion parameters (Ecorr, icorr, Epit/Eb) for LPBF Scalmalloy/Al–Mg–Sc–Zr or for LPBF Al–Ce systems. A retrieved Al–Ce–Mn LPBF paper focused on microstructure/mechanical property development rather than electrochemical corrosion testing. (plotkowski2020microstructureandproperties pages 10-12, plotkowski2020microstructureandproperties pages 12-13)

## Cross-alloy comparison (as supported by retrieved values)
Because corrosion metrics are highly environment-dependent, the most defensible cross-alloy comparisons are within comparable chloride environments and with stated reference electrodes.

* **AlSi10Mg (LPBF, 3.5% NaCl, Ag/AgCl):** icorr spans orders of magnitude depending on post-processing—ECAP reduced icorr to ~0.2–0.3 µA/cm² versus 7–18 µA/cm² for as-built/heat-treated conditions, indicating that post-processing can dominate corrosion performance relative to the baseline LPBF state. (snopinski2022evolutionofmicrostructure pages 9-12, snopinski2022evolutionofmicrostructure media ecb11778)
* **2xxx AA2099 (0.1 M NaCl):** conventional T83 outperformed LPBF variants in icorr, and increasing LPBF preheat temperature markedly worsened icorr (to ~10 µA/cm²), consistent with Cu-rich phase evolution compromising oxide integrity. (adjeikyeremeh2023preheatinginfluenceon pages 15-17, adjeikyeremeh2023preheatinginfluenceon pages 17-19)
* **7xxx 7075 (3.5% NaCl, Ag/AgCl):** laser AM (LENS) shifted Ecorr more noble than forged but did not lower icorr; instead, icorr was slightly higher than forged in this dataset. (zhang2021comparativestudyon pages 6-7)
* **7xxx-like multicomponent (3.5% NaCl, SCE):** among LPBF heat treatments, RRA produced the lowest icorr (~1.713 µA/cm²) and DA the highest (~1.921 µA/cm²), showing that precipitate morphology/grain-boundary character can modulate corrosion within a relatively narrow band of icorr values. (zhang2023effectofpostheat pages 7-9, zhang2023effectofpostheat pages 9-11)

## How LPBF (and laser AM) processing affects corrosion vs wrought/cast equivalents
Across the retrieved studies, the LPBF/laser-AM corrosion response reflects a competition between beneficial microstructural refinement and detrimental heterogeneities/defects:

1. **Defects and melt-pool heterogeneity promote localized corrosion and higher currents.** In the AA2099 comparison, LPBF conditions (especially higher preheat) exhibited higher icorr than conventional T83, and EIS indicated decreasing oxide/charge-transfer resistances with increasing preheat temperature, consistent with Cu-rich phase formation and compromised protective films. (adjeikyeremeh2023preheatinginfluenceon pages 15-17, adjeikyeremeh2023preheatinginfluenceon pages 17-19)

2. **Post-processing that reduces porosity/redistributes phases can strongly improve corrosion behavior.** For LPBF AlSi10Mg, ECAP processing produced substantially nobler Ecorr and reduced icorr by more than an order of magnitude versus as-built/heat-treated states, consistent with a denser oxide and fewer effective pit-initiation sites. (snopinski2022evolutionofmicrostructure pages 9-12, snopinski2022evolutionofmicrostructure pages 14-16)

3. **LPBF can shift Ecorr without necessarily improving icorr relative to conventional processing.** In the 7075 comparison, laser AM yielded a nobler Ecorr than forging, but icorr was slightly higher, suggesting that corrosion thermodynamics (potential) and kinetics (current density) do not necessarily move in the same direction when microstructural defects or galvanic couples persist. (zhang2021comparativestudyon pages 6-7)

4. **Heat-treatment design in LPBF 7xxx-like alloys changes precipitate morphology and intergranular susceptibility, affecting icorr.** In the LPBF Al–Zn–Mg–Cu–Si–Zr–Er alloy, corrosion ranking by icorr was linked to precipitate morphology (e.g., strip-like Mg2Si in DA vs finer distributions in T6/RRA) and differences in grain boundary character fraction, with RRA best in icorr and pit morphology. (zhang2023effectofpostheat pages 7-9, zhang2023effectofpostheat pages 9-11)

## Key gap relative to the user’s request
The user requested comparison across **AlSi10Mg, Scalmalloy, 2xxx, 7xxx, and Al–Ce** systems including **Ecorr, icorr, and pitting potential**. In this run, pitting potentials (Epit/Eb) were generally not available in the retrievable excerpts for the aluminum systems, and **Scalmalloy and LPBF Al–Ce polarization datasets were not accessible**; accordingly, no numerical pitting potential comparison across all requested families can be made without additional full-text retrieval of those specific works. (snopinski2022evolutionofmicrostructure pages 9-12, plotkowski2020microstructureandproperties pages 10-12)

References

1. (plotkowski2020microstructureandproperties pages 10-12): A. Plotkowski, K. Sisco, S. Bahl, A. Shyam, Ying Yang, Lawrence F. Allard, P. Nandwana, A. Rossy, and R. Dehoff. Microstructure and properties of a high temperature al–ce–mn alloy produced by additive manufacturing. Acta Materialia, 196:595-608, Sep 2020. URL: https://doi.org/10.1016/j.actamat.2020.07.014, doi:10.1016/j.actamat.2020.07.014. This article has 250 citations and is from a highest quality peer-reviewed journal.

2. (plotkowski2020microstructureandproperties pages 12-13): A. Plotkowski, K. Sisco, S. Bahl, A. Shyam, Ying Yang, Lawrence F. Allard, P. Nandwana, A. Rossy, and R. Dehoff. Microstructure and properties of a high temperature al–ce–mn alloy produced by additive manufacturing. Acta Materialia, 196:595-608, Sep 2020. URL: https://doi.org/10.1016/j.actamat.2020.07.014, doi:10.1016/j.actamat.2020.07.014. This article has 250 citations and is from a highest quality peer-reviewed journal.

3. (snopinski2022evolutionofmicrostructure pages 9-12): Przemysław Snopiński, Anna Woźniak, Dariusz Łukowiec, Krzysztof Matus, Tomasz Tański, Stanislav Rusz, and Ondřej Hilšer. Evolution of microstructure, texture and corrosion properties of additively manufactured alsi10mg alloy subjected to equal channel angular pressing (ecap). Symmetry, 14:674, Mar 2022. URL: https://doi.org/10.3390/sym14040674, doi:10.3390/sym14040674. This article has 24 citations.

4. (snopinski2022evolutionofmicrostructure pages 14-16): Przemysław Snopiński, Anna Woźniak, Dariusz Łukowiec, Krzysztof Matus, Tomasz Tański, Stanislav Rusz, and Ondřej Hilšer. Evolution of microstructure, texture and corrosion properties of additively manufactured alsi10mg alloy subjected to equal channel angular pressing (ecap). Symmetry, 14:674, Mar 2022. URL: https://doi.org/10.3390/sym14040674, doi:10.3390/sym14040674. This article has 24 citations.

5. (snopinski2022evolutionofmicrostructure pages 12-14): Przemysław Snopiński, Anna Woźniak, Dariusz Łukowiec, Krzysztof Matus, Tomasz Tański, Stanislav Rusz, and Ondřej Hilšer. Evolution of microstructure, texture and corrosion properties of additively manufactured alsi10mg alloy subjected to equal channel angular pressing (ecap). Symmetry, 14:674, Mar 2022. URL: https://doi.org/10.3390/sym14040674, doi:10.3390/sym14040674. This article has 24 citations.

6. (snopinski2022evolutionofmicrostructure media ecb11778): Przemysław Snopiński, Anna Woźniak, Dariusz Łukowiec, Krzysztof Matus, Tomasz Tański, Stanislav Rusz, and Ondřej Hilšer. Evolution of microstructure, texture and corrosion properties of additively manufactured alsi10mg alloy subjected to equal channel angular pressing (ecap). Symmetry, 14:674, Mar 2022. URL: https://doi.org/10.3390/sym14040674, doi:10.3390/sym14040674. This article has 24 citations.

7. (adjeikyeremeh2023preheatinginfluenceon pages 15-17): Frank Adjei-Kyeremeh, Yudha Pratesa, Xiao Shen, Wenwen Song, Iris Raffeis, Uwe Vroomen, Daniela Zander, and Andreas Bührig-Polaczek. Preheating influence on the precipitation microstructure, mechanical and corrosive properties of additively built al–cu–li alloy contrasted with conventional (t83) alloy. Materials, 16:4916, Jul 2023. URL: https://doi.org/10.3390/ma16144916, doi:10.3390/ma16144916. This article has 8 citations.

8. (adjeikyeremeh2023preheatinginfluenceon pages 12-15): Frank Adjei-Kyeremeh, Yudha Pratesa, Xiao Shen, Wenwen Song, Iris Raffeis, Uwe Vroomen, Daniela Zander, and Andreas Bührig-Polaczek. Preheating influence on the precipitation microstructure, mechanical and corrosive properties of additively built al–cu–li alloy contrasted with conventional (t83) alloy. Materials, 16:4916, Jul 2023. URL: https://doi.org/10.3390/ma16144916, doi:10.3390/ma16144916. This article has 8 citations.

9. (adjeikyeremeh2023preheatinginfluenceon pages 17-19): Frank Adjei-Kyeremeh, Yudha Pratesa, Xiao Shen, Wenwen Song, Iris Raffeis, Uwe Vroomen, Daniela Zander, and Andreas Bührig-Polaczek. Preheating influence on the precipitation microstructure, mechanical and corrosive properties of additively built al–cu–li alloy contrasted with conventional (t83) alloy. Materials, 16:4916, Jul 2023. URL: https://doi.org/10.3390/ma16144916, doi:10.3390/ma16144916. This article has 8 citations.

10. (zhang2021comparativestudyon pages 6-7): Jin-liang Zhang, Jie-liang Ye, Bo Song, Rui-di Li, and Yu-sheng Shi. Comparative study on microstructure and electrochemical corrosion resistance of al7075 alloy prepared by laser additive manufacturing and forging technology. Journal of Central South University, 28:1058-1067, Apr 2021. URL: https://doi.org/10.1007/s11771-021-4679-9, doi:10.1007/s11771-021-4679-9. This article has 31 citations and is from a peer-reviewed journal.

11. (zhang2021comparativestudyon pages 7-9): Jin-liang Zhang, Jie-liang Ye, Bo Song, Rui-di Li, and Yu-sheng Shi. Comparative study on microstructure and electrochemical corrosion resistance of al7075 alloy prepared by laser additive manufacturing and forging technology. Journal of Central South University, 28:1058-1067, Apr 2021. URL: https://doi.org/10.1007/s11771-021-4679-9, doi:10.1007/s11771-021-4679-9. This article has 31 citations and is from a peer-reviewed journal.

12. (zhang2021comparativestudyon pages 2-6): Jin-liang Zhang, Jie-liang Ye, Bo Song, Rui-di Li, and Yu-sheng Shi. Comparative study on microstructure and electrochemical corrosion resistance of al7075 alloy prepared by laser additive manufacturing and forging technology. Journal of Central South University, 28:1058-1067, Apr 2021. URL: https://doi.org/10.1007/s11771-021-4679-9, doi:10.1007/s11771-021-4679-9. This article has 31 citations and is from a peer-reviewed journal.

13. (zhang2023effectofpostheat pages 7-9): Zhiqian Zhang, Dehua Li, Shengci Li, Hui Tang, Yu Zhang, Tingting Dong, Weirong Li, Yanfang Li, and Olanrewaju A. Ojo. Effect of post-heat treatment on the microstructure, mechanical, and corrosion properties of laser powder bed fused al–zn–mg–cu–si–zr–er alloys. Journal of Materials Research and Technology, 27:1350-1364, Nov 2023. URL: https://doi.org/10.1016/j.jmrt.2023.10.009, doi:10.1016/j.jmrt.2023.10.009. This article has 23 citations and is from a peer-reviewed journal.

14. (zhang2023effectofpostheat pages 1-3): Zhiqian Zhang, Dehua Li, Shengci Li, Hui Tang, Yu Zhang, Tingting Dong, Weirong Li, Yanfang Li, and Olanrewaju A. Ojo. Effect of post-heat treatment on the microstructure, mechanical, and corrosion properties of laser powder bed fused al–zn–mg–cu–si–zr–er alloys. Journal of Materials Research and Technology, 27:1350-1364, Nov 2023. URL: https://doi.org/10.1016/j.jmrt.2023.10.009, doi:10.1016/j.jmrt.2023.10.009. This article has 23 citations and is from a peer-reviewed journal.

15. (zhang2023effectofpostheat pages 9-11): Zhiqian Zhang, Dehua Li, Shengci Li, Hui Tang, Yu Zhang, Tingting Dong, Weirong Li, Yanfang Li, and Olanrewaju A. Ojo. Effect of post-heat treatment on the microstructure, mechanical, and corrosion properties of laser powder bed fused al–zn–mg–cu–si–zr–er alloys. Journal of Materials Research and Technology, 27:1350-1364, Nov 2023. URL: https://doi.org/10.1016/j.jmrt.2023.10.009, doi:10.1016/j.jmrt.2023.10.009. This article has 23 citations and is from a peer-reviewed journal.

16. (palmer2024useofcoredc pages 9-15): E Palmer, S Mehraban, D Butcher, and M Ritchie. Use of cored wire in the optimisation of new alloys for laser powder bed fusion with tailored mechanical and corrosion properties. Unknown journal, 2024.

17. (bertone2025caratterizzazionedelcomportamento pages 20-24): E Bertone. Caratterizzazione del comportamento a corrosione di leghe di alluminio processate con tecnologie additive”=“characterization of the corrosion behavior of aluminum …. Unknown journal, 2025.

18. (bertone2025caratterizzazionedelcomportamento pages 27-33): E Bertone. Caratterizzazione del comportamento a corrosione di leghe di alluminio processate con tecnologie additive”=“characterization of the corrosion behavior of aluminum …. Unknown journal, 2025.


---

## Query 2

**Question:** What thermal conductivity and electrical conductivity values have been measured for LPBF aluminum alloys? Provide quantitative data across different alloy systems and conditions (as-built vs heat-treated). Which AM Al alloys achieve thermal conductivity closest to pure aluminum?

**Task ID:** `affb222e-3e57-4eee-8699-9fdaaa710d65`

**Status:** complete

## Summary of measured conductivities for LPBF aluminum alloys
Measured thermal conductivity (k) and electrical conductivity (σ, or %IACS) for LPBF aluminum alloys are concentrated in the Al–Si–Mg family (especially AlSi10Mg) with fewer quantitative datasets for other AM Al systems. Across independent studies, post-build heat treatments (stress relief/anneal/direct aging/preheating) consistently increase both k and σ by breaking up the continuous fine Si network and reducing solute supersaturation/electron scattering, while also largely eliminating build-direction anisotropy in conductivity. (sarap2024electricalandthermal pages 9-11, cauwenbergh2021unravellingthemultiscale pages 3-5, sarap2024electricalandthermal pages 6-9, selo2020onthethermal pages 1-2, selo2020onthethermal pages 3-4, ozer2020investigationofthe pages 4-7)

## Quantitative conductivity data across alloys, conditions, and orientations
| Alloy system | Condition / heat treatment | Thermal conductivity, k (W/m·K) | Electrical conductivity | Notes |
|---|---|---:|---:|---|
| AlSi10Mg | As-built | 115 ± 9 transverse; 130 ± 10 build; ASTM E1225 stack bottom 393 K / top 293 K (selo2020onthethermal pages 3-4) | — | Measured anisotropy in as-built state; build direction higher than transverse (selo2020onthethermal pages 3-4) |
| AlSi10Mg | Anneal 300 °C × 2 h, air cool | 173 ± 10, both directions (EOS-reported prior measurement) (selo2020onthethermal pages 1-2, selo2020onthethermal pages 2-3) | — | Annealing removed anisotropy; Sélo also states ~30% increase vs as-built transverse (selo2020onthethermal pages 1-2, selo2020onthethermal pages 2-3) |
| AlSi10Mg | Solution heat treatment 520 °C × 1 h + water quench | Not numerically stated in excerpt; similar to 520 °C × 2 h and below T6-like (selo2020onthethermal pages 2-3, selo2020onthethermal pages 3-4) | — | Included because this was one of the tested LPBF AlSi10Mg conditions in Sélo et al. (selo2020onthethermal pages 2-3, selo2020onthethermal pages 3-4) |
| AlSi10Mg | Solution heat treatment 520 °C × 2 h + water quench | Not numerically stated in excerpt; similar to 520 °C × 1 h and below T6-like (selo2020onthethermal pages 2-3, selo2020onthethermal pages 3-4) | — | Included because this was one of the tested LPBF AlSi10Mg conditions in Sélo et al. (selo2020onthethermal pages 2-3, selo2020onthethermal pages 3-4) |
| AlSi10Mg | T6-like: 520 °C × 1 h + water quench + 160 °C × 6 h | 166 ± 13; ASTM E1225 stack 393 K / 293 K (selo2020onthethermal pages 3-4) | ~5.94 µΩ·cm resistivity for annealed and T6-like average in related resistivity study (not same paper) (silbernagel2018electricalresistivityof pages 10-12) | Highest measured k reported in Sélo excerpt; heat treatment route explicitly defined in paper (selo2020onthethermal pages 2-3, selo2020onthethermal pages 3-4) |
| AlSi10Mg | AB | 124 ± 2 at room temperature; derived from σ via Wiedemann–Franz (cauwenbergh2021unravellingthemultiscale pages 3-5) | 17.4 ± 0.3 MS/m at room temperature (cauwenbergh2021unravellingthemultiscale pages 3-5) | No direction reported in excerpt; κ is calculated from measured σ, not directly measured (cauwenbergh2021unravellingthemultiscale pages 3-5) |
| AlSi10Mg | DA | 153 ± 5 at room temperature; derived from σ via Wiedemann–Franz (cauwenbergh2021unravellingthemultiscale pages 3-5) | 21.4 ± 0.7 MS/m at room temperature (cauwenbergh2021unravellingthemultiscale pages 3-5) | Direct-aged condition in Van Cauwenbergh et al. (cauwenbergh2021unravellingthemultiscale pages 3-5) |
| AlSi10Mg | SR | 168 ± 4 at room temperature; derived from σ via Wiedemann–Franz (cauwenbergh2021unravellingthemultiscale pages 3-5) | 23.5 ± 0.6 MS/m at room temperature (cauwenbergh2021unravellingthemultiscale pages 3-5) | Stress-relieved condition; κ increased strongly vs AB (cauwenbergh2021unravellingthemultiscale pages 3-5) |
| AlSi10Mg | PH | 183 ± 3 at room temperature; derived from σ via Wiedemann–Franz (cauwenbergh2021unravellingthemultiscale pages 3-5) | 25.6 ± 0.4 MS/m at room temperature (cauwenbergh2021unravellingthemultiscale pages 3-5) | Preheated-build condition gave highest κ among Van Cauwenbergh conditions (cauwenbergh2021unravellingthemultiscale pages 3-5) |
| AlSi10Mg | As-built, AlZ orientation | 113.3 ± 3.1 at 35 °C; 116.2 ± 1.8 at 70 °C (sarap2024electricalandthermal pages 6-9) | 14.70 ± 0.27 MS/m at 20 °C (sarap2024electricalandthermal pages 9-11) | Build/Z orientation showed highest k among as-built orientations; anisotropy present before anneal (sarap2024electricalandthermal pages 9-11, sarap2024electricalandthermal pages 6-9) |
| AlSi10Mg | As-built, Al45 orientation | 103.0 ± 3.2 at 35 °C; 106.9 ± 1.7 at 70 °C (sarap2024electricalandthermal pages 6-9) | — | Intermediate orientation between Z and X; no EC value in excerpt for Al45 (sarap2024electricalandthermal pages 6-9) |
| AlSi10Mg | As-built, AlX orientation | 106.7 ± 3.5 at 35 °C; 108.0 ± 2.0 at 70 °C (sarap2024electricalandthermal pages 6-9) | 13.08 ± 0.36 MS/m at 20 °C (sarap2024electricalandthermal pages 9-11) | Lower than AlZ in as-built state (sarap2024electricalandthermal pages 9-11, sarap2024electricalandthermal pages 6-9) |
| AlSi10Mg | Annealed, AlZ orientation | 148.2 ± 3.5 at 35 °C; 149.5 ± 2.3 at 70 °C (sarap2024electricalandthermal pages 6-9) | 23.88 ± 0.50 MS/m at 20 °C (sarap2024electricalandthermal pages 9-11) | Annealing increased k and σ and removed anisotropy (sarap2024electricalandthermal pages 9-11, sarap2024electricalandthermal pages 6-9) |
| AlSi10Mg | Annealed, Al45 orientation | 148.5 ± 3.7 at 35 °C; 149.9 ± 2.4 at 70 °C (sarap2024electricalandthermal pages 6-9) | — | k becomes essentially isotropic after anneal (sarap2024electricalandthermal pages 6-9) |
| AlSi10Mg | Annealed, AlX orientation | 148.2 ± 3.8 at 35 °C; 149.8 ± 2.3 at 70 °C (sarap2024electricalandthermal pages 6-9) | 24.72 ± 0.86 MS/m at 20 °C (sarap2024electricalandthermal pages 9-11) | Annealed X nearly identical to annealed Z in k (sarap2024electricalandthermal pages 9-11, sarap2024electricalandthermal pages 6-9) |
| AlSi10Mg | As-built (DMLS/LPBF) | — | 28.5% IACS ≈ 16.5 MS/m at ~20 °C if converted using 58 MS/m = 100% IACS (ozer2020investigationofthe pages 4-7, ozer2020investigationofthe pages 7-9) | Lowest conductivity among Özer conditions; conversion is approximate and added here for comparison only (ozer2020investigationofthe pages 4-7, ozer2020investigationofthe pages 7-9) |
| AlSi10Mg | SR (DMLS/LPBF) | — | 43.6% IACS ≈ 25.3 MS/m at ~20 °C if converted using 58 MS/m = 100% IACS (ozer2020investigationofthe pages 4-7, ozer2020investigationofthe pages 7-9) | Heat treatment raises conductivity by breaking up fine Si network (ozer2020investigationofthe pages 4-7, ozer2020investigationofthe pages 7-9) |
| AlSi10Mg | T6 (DMLS/LPBF) | — | 44.2% IACS ≈ 25.6 MS/m at ~20 °C if converted using 58 MS/m = 100% IACS (ozer2020investigationofthe pages 4-7, ozer2020investigationofthe pages 7-9) | Highest %IACS in Özer dataset; absolute MS/m shown as simple conversion note, not original reported unit (ozer2020investigationofthe pages 4-7, ozer2020investigationofthe pages 7-9) |
| Scalmalloy® (Al-Mg-Sc-Zr) | As-built | — | 11.74 ± 0.01 MS/m (ghio2025laserpowderbedfused pages 10-13, ghio2025laserpowderbedfused pages 1-2) | No thermal-conductivity values reported in the excerpted evidence (ghio2025laserpowderbedfused pages 10-13, ghio2025laserpowderbedfused pages 1-2) |
| Scalmalloy® (Al-Mg-Sc-Zr) | Aged 275 °C, long-term (up to 256 h) | — | 15.28 ± 0.01 MS/m (ghio2025laserpowderbedfused pages 10-13) | EC rises monotonically with aging/time due to solute depletion and precipitation (ghio2025laserpowderbedfused pages 10-13) |
| Scalmalloy® (Al-Mg-Sc-Zr) | Direct aging 325 °C × 2 h | — | 14.13 ± 0.01 MS/m (ghio2025laserpowderbedfused pages 13-15) | Short-time direct aging value explicitly reported (ghio2025laserpowderbedfused pages 13-15) |
| Scalmalloy® (Al-Mg-Sc-Zr) | Direct aging 325 °C × 4 h | — | 14.67 ± 0.01 MS/m (ghio2025laserpowderbedfused pages 13-15) | Reference DA condition in methods; explicitly reported (ghio2025laserpowderbedfused pages 13-15, ghio2025laserpowderbedfused pages 2-4) |
| Scalmalloy® (Al-Mg-Sc-Zr) | Aged 325 °C, long-term (up to 256 h) | — | 17.51 ± 0.01 MS/m (ghio2025laserpowderbedfused pages 10-13) | Higher than short-time 2–4 h values because EC continued increasing with time (ghio2025laserpowderbedfused pages 10-13, ghio2025laserpowderbedfused pages 13-15) |
| Scalmalloy® (Al-Mg-Sc-Zr) | Aged 400 °C, long-term (up to 256 h) | — | 18.28 ± 0.01 MS/m (ghio2025laserpowderbedfused pages 10-13) | Highest EC reported for Scalmalloy in the excerpted evidence; accompanied by overaging in hardness response (ghio2025laserpowderbedfused pages 10-13) |


*Table: This table compares measured thermal and electrical conductivity data reported for LPBF aluminum alloys across alloy systems and post-build conditions. It is useful for identifying how heat treatment and build orientation change conductivity, and which conditions approach the highest thermal conductivity values.*

Key measured thermal-conductivity dataset (with directionality and heat treatment) is shown in a cropped figure from Sélo et al. (LPBF AlSi10Mg), which includes as-built build vs transverse values and several heat-treated conditions. (selo2020onthethermal media 69418b10)

## As-built vs heat-treated: ranges observed in AlSi10Mg
**Thermal conductivity (directly measured):** As-built AlSi10Mg shows k ≈115–130 W/m·K (transverse vs build direction) under ASTM E1225 conditions, and heat treatments raise k to ~148–173 W/m·K depending on treatment and study, with anisotropy largely removed after anneal/heat treatment. (sarap2024electricalandthermal pages 6-9, selo2020onthethermal pages 1-2, selo2020onthethermal pages 3-4)

**Electrical conductivity (measured):** For AlSi10Mg, σ increases from ~13–17 MS/m in as-built states to ~23–26 MS/m after annealing/stress relief/preheating-type conditions (values and units depend on study and exact condition). In %IACS terms, one dataset reports ~28.5% IACS as-built rising to ~43.6–44.2% IACS after SR/T6. (sarap2024electricalandthermal pages 9-11, cauwenbergh2021unravellingthemultiscale pages 3-5, ozer2020investigationofthe pages 4-7, ozer2020investigationofthe pages 7-9)

## Other LPBF aluminum alloy system with quantitative electrical conductivity: Scalmalloy®
For LPBF Scalmalloy® (Al–Mg–Sc–Zr), electrical conductivity is reported as **11.74 ± 0.01 MS/m as-built**, increasing with direct aging/thermal exposure (e.g., **14.67 ± 0.01 MS/m after 325 °C × 4 h**, up to **18.28 ± 0.01 MS/m** after long-term aging at 400 °C). Thermal conductivity values were not reported in the retrieved excerpts for Scalmalloy®. (ghio2025laserpowderbedfused pages 10-13, ghio2025laserpowderbedfused pages 13-15, ghio2025laserpowderbedfused pages 1-2)

## Which LPBF Al alloys are closest to pure aluminum in thermal conductivity?
Within the retrieved LPBF aluminum-alloy measurements, the **highest reported thermal conductivity** is for LPBF **AlSi10Mg** in the **preheated/thermally post-processed (PH)** condition, **κ = 183 ± 3 W/m·K at room temperature**, reported via Wiedemann–Franz conversion from measured σ. (cauwenbergh2021unravellingthemultiscale pages 3-5)

Among *directly measured* k values in the retrieved evidence, LPBF **AlSi10Mg annealed at 300 °C × 2 h** reaches **k ≈ 173 ± 10 W/m·K** and becomes effectively isotropic, making it the closest-to-pure-Al case among the direct k measurements available here. (selo2020onthethermal pages 1-2, selo2020onthethermal pages 2-3)

No retrieved LPBF Al–Mg–Sc (Scalmalloy®) excerpt reported k, and no quantified k datasets for LPBF 6xxx/7xxx/Al–Fe/Al–Ce systems were accessible in the current tool-retrieved full texts; therefore, the “closest to pure Al” comparison is limited to the measured AlSi10Mg datasets above. (ghio2025laserpowderbedfused pages 10-13, ghio2025laserpowderbedfused pages 13-15, ghio2025laserpowderbedfused pages 1-2)

References

1. (sarap2024electricalandthermal pages 9-11): Martin Sarap, Hans Tiismus, Ants Kallaste, Mart Saarna, Märt Kolnes, Payam Shams Ghahfarokhi, and Toomas Vaimann. Electrical and thermal anisotropy in additively manufactured alsi10mg and fe-si samples. Machines, 13:1, Dec 2024. URL: https://doi.org/10.3390/machines13010001, doi:10.3390/machines13010001. This article has 3 citations.

2. (cauwenbergh2021unravellingthemultiscale pages 3-5): P. Van Cauwenbergh, V. Samaee, L. Thijs, J. Nejezchlebová, P. Sedlák, A. Iveković, D. Schryvers, B. Van Hooreweder, and K. Vanmeensel. Unravelling the multi-scale structure–property relationship of laser powder bed fusion processed and heat-treated alsi10mg. Scientific Reports, Mar 2021. URL: https://doi.org/10.1038/s41598-021-85047-2, doi:10.1038/s41598-021-85047-2. This article has 211 citations and is from a peer-reviewed journal.

3. (sarap2024electricalandthermal pages 6-9): Martin Sarap, Hans Tiismus, Ants Kallaste, Mart Saarna, Märt Kolnes, Payam Shams Ghahfarokhi, and Toomas Vaimann. Electrical and thermal anisotropy in additively manufactured alsi10mg and fe-si samples. Machines, 13:1, Dec 2024. URL: https://doi.org/10.3390/machines13010001, doi:10.3390/machines13010001. This article has 3 citations.

4. (selo2020onthethermal pages 1-2): Richard R.J. Sélo, Sam Catchpole-Smith, Ian Maskery, Ian Ashcroft, and Christopher Tuck. On the thermal conductivity of alsi10mg and lattice structures made by laser powder bed fusion. Additive Manufacturing, 34:101214, Aug 2020. URL: https://doi.org/10.1016/j.addma.2020.101214, doi:10.1016/j.addma.2020.101214. This article has 173 citations and is from a highest quality peer-reviewed journal.

5. (selo2020onthethermal pages 3-4): Richard R.J. Sélo, Sam Catchpole-Smith, Ian Maskery, Ian Ashcroft, and Christopher Tuck. On the thermal conductivity of alsi10mg and lattice structures made by laser powder bed fusion. Additive Manufacturing, 34:101214, Aug 2020. URL: https://doi.org/10.1016/j.addma.2020.101214, doi:10.1016/j.addma.2020.101214. This article has 173 citations and is from a highest quality peer-reviewed journal.

6. (ozer2020investigationofthe pages 4-7): Gökhan Özer, Gürkan Tarakçi, Mustafa S. Yilmaz, Zafer Ç. Öter, Ömer Sürmen, Yaşar Akça, Mert Coşkun, and Ebubekir Koç. Investigation of the effects of different heat treatment parameters on the corrosion and mechanical properties of the alsi10mg alloy produced with direct metal laser sintering. Materials and Corrosion, 71:365-373, Aug 2020. URL: https://doi.org/10.1002/maco.201911171, doi:10.1002/maco.201911171. This article has 45 citations.

7. (selo2020onthethermal pages 2-3): Richard R.J. Sélo, Sam Catchpole-Smith, Ian Maskery, Ian Ashcroft, and Christopher Tuck. On the thermal conductivity of alsi10mg and lattice structures made by laser powder bed fusion. Additive Manufacturing, 34:101214, Aug 2020. URL: https://doi.org/10.1016/j.addma.2020.101214, doi:10.1016/j.addma.2020.101214. This article has 173 citations and is from a highest quality peer-reviewed journal.

8. (silbernagel2018electricalresistivityof pages 10-12): Cassidy Silbernagel, Ian Ashcroft, Phill Dickens, and Michael Galea. Electrical resistivity of additively manufactured alsi10mg for use in electric motors. Additive Manufacturing, 21:395-403, May 2018. URL: https://doi.org/10.1016/j.addma.2018.03.027, doi:10.1016/j.addma.2018.03.027. This article has 154 citations and is from a highest quality peer-reviewed journal.

9. (ozer2020investigationofthe pages 7-9): Gökhan Özer, Gürkan Tarakçi, Mustafa S. Yilmaz, Zafer Ç. Öter, Ömer Sürmen, Yaşar Akça, Mert Coşkun, and Ebubekir Koç. Investigation of the effects of different heat treatment parameters on the corrosion and mechanical properties of the alsi10mg alloy produced with direct metal laser sintering. Materials and Corrosion, 71:365-373, Aug 2020. URL: https://doi.org/10.1002/maco.201911171, doi:10.1002/maco.201911171. This article has 45 citations.

10. (ghio2025laserpowderbedfused pages 10-13): Emanuele Ghio, Lorenzo Curti, Daniele Carosi, Alessandro Morri, and Emanuela Cerri. Laser powder bed-fused scalmalloy®: effect of long thermal aging on hardness and electrical conductivity. Metals, 15:1364, Dec 2025. URL: https://doi.org/10.3390/met15121364, doi:10.3390/met15121364. This article has 0 citations.

11. (ghio2025laserpowderbedfused pages 1-2): Emanuele Ghio, Lorenzo Curti, Daniele Carosi, Alessandro Morri, and Emanuela Cerri. Laser powder bed-fused scalmalloy®: effect of long thermal aging on hardness and electrical conductivity. Metals, 15:1364, Dec 2025. URL: https://doi.org/10.3390/met15121364, doi:10.3390/met15121364. This article has 0 citations.

12. (ghio2025laserpowderbedfused pages 13-15): Emanuele Ghio, Lorenzo Curti, Daniele Carosi, Alessandro Morri, and Emanuela Cerri. Laser powder bed-fused scalmalloy®: effect of long thermal aging on hardness and electrical conductivity. Metals, 15:1364, Dec 2025. URL: https://doi.org/10.3390/met15121364, doi:10.3390/met15121364. This article has 0 citations.

13. (ghio2025laserpowderbedfused pages 2-4): Emanuele Ghio, Lorenzo Curti, Daniele Carosi, Alessandro Morri, and Emanuela Cerri. Laser powder bed-fused scalmalloy®: effect of long thermal aging on hardness and electrical conductivity. Metals, 15:1364, Dec 2025. URL: https://doi.org/10.3390/met15121364, doi:10.3390/met15121364. This article has 0 citations.

14. (selo2020onthethermal media 69418b10): Richard R.J. Sélo, Sam Catchpole-Smith, Ian Maskery, Ian Ashcroft, and Christopher Tuck. On the thermal conductivity of alsi10mg and lattice structures made by laser powder bed fusion. Additive Manufacturing, 34:101214, Aug 2020. URL: https://doi.org/10.1016/j.addma.2020.101214, doi:10.1016/j.addma.2020.101214. This article has 173 citations and is from a highest quality peer-reviewed journal.


---

## Query 3

**Question:** What are the optimal LPBF process parameter windows (laser power, scan speed, hatch spacing, layer thickness) for achieving high-density (>99.5%) aluminum alloy parts? Compare process windows across AlSi10Mg, Scalmalloy, Al-Cu, and Al-Zn-Mg-Cu systems. Provide volumetric energy density ranges.

**Task ID:** `52190c63-f75e-46bd-8bd2-107efea284c6`

**Status:** complete

Volumetric energy density (VED) definition used here

Across the cited LPBF literature, the standard “volumetric energy density” is defined as

\[ \mathrm{VED} = \frac{P}{v\,h\,t} \]

with laser power \(P\) in W (= J/s), scan speed \(v\) in mm/s, hatch spacing \(h\) in mm, and layer thickness \(t\) in mm, giving VED in J/mm\(^3\). (yang2020laserpowderbed pages 1-2, zavalaarredondo2019useofpower pages 2-3)

Comparative high‑density LPBF process windows (≥99.5% relative density)

| Alloy system | Source | Density metric and achieved density | Laser power P (W) window or set | Scan speed v (mm/s) window or set | Hatch spacing h (mm) | Layer thickness t (mm) | VED (J/mm^3) | Notes on scan strategy / defocus / preheat |
|---|---|---|---:|---:|---:|---:|---:|---|
| AlSi10Mg | Hyer et al., 2020 | Relative density in Table 1 reported in the 99.5–99.7% range; highest-density region also summarized as >99% over a broad mid-range VED window (hyer2020understandingthelaser pages 2-5, hyer2020understandingthelaser pages 1-2) | 250–350 (explicit high-density sets) | 1200–1650 (explicit high-density sets) | 0.13 | 0.03 | Explicit sets: ~53–54; broader high-density Table 1 region: ~32–80 (hyer2020understandingthelaser pages 2-5, hyer2020understandingthelaser pages 1-2) | Explicit sets: 250/1200/0.13/0.03 and 350/1650/0.13/0.03; literature cited in the same paper places dense AlSi10Mg commonly around ~33–100 or ~50–60 J/mm^3 depending on machine/strategy (hyer2020understandingthelaser pages 2-5, hyer2020understandingthelaser pages 1-2) |
| Scalmalloy (Al-Mg-Sc-Zr) | Ekubaru et al., 2022 (Crystals) | OM density 99.7%, explicitly stated to exceed the industry-required >99.5% threshold (ekubaru2022effectsofscanning pages 2-4) | 360 | 1200 | 0.10 | 0.06 | 50 (reported; also equals 360/(1200×0.10×0.06)) (ekubaru2022effectsofscanning pages 2-4) | EOS M290; X- and XY-scan strategies compared at same VED; build chamber Ar, O2 <100 ppm; stage preheated to 300 K (ekubaru2022effectsofscanning pages 2-4) |
| Al-Cu-based (TiB2-modified A205-like Al-Cu-Ag-Mg-Ti-TiB2) | Mair et al., 2021 (MSEA) | 99.9 ± 0.1% by Archimedes; 99.5 ± 0.1% by optical image analysis (mair2021microstructureandmechanical pages 2-3) | 200 | 1000 | 0.10 | 0.03 | 67 (reported; also equals 200/(1000×0.10×0.03)) (mair2021microstructureandmechanical pages 2-3) | Stripe scanning (10 mm stripe), zig-zag pattern, 67° rotation between layers; AconityLAB, 60 µm spot (mair2021microstructureandmechanical pages 2-3) |
| Al-Zn-Mg-Cu (AA7075) | Stopyra et al., 2020 (Additive Manufacturing) | Highest relative density reported as about 99.5%; cracking not fully eliminated (stopyra2020laserpowderbed pages 22-27) | 200 | 200 | 0.14 | 0.05 | 143 (reported EV; also equals 200/(200×0.14×0.05)) (stopyra2020laserpowderbed pages 22-27) | Chessboard scanning strategy (2.5 mm × 2.5 mm islands); negative defocus ΔF = -3.5 mm required for best density; no base-plate preheat for this best-density case; 300 °C preheat reduced crack density but at the expense of density (stopyra2020laserpowderbed pages 22-27, stopyra2020laserpowderbed media f309be68, stopyra2020laserpowderbed media 9fd38488) |


*Table: This table compares the best-supported high-density LPBF parameter sets and windows across four aluminum alloy systems. It is useful for quickly benchmarking laser power, scan speed, hatch spacing, layer thickness, and VED needed to approach or exceed 99.5% density.*

Key cross‑alloy comparisons (parameter windows and VED ranges)

1) AlSi10Mg (Al-Si-Mg)

AlSi10Mg exhibits a relatively broad densification window in mid-range VED. Hyer et al. summarize the highest-density region as VED ≈ 32–54 J/mm\(^3\), and Table 1 in that work includes samples with 99.5–99.7% relative density across roughly ~32–80 J/mm\(^3\). (hyer2020understandingthelaser pages 1-2, hyer2020understandingthelaser pages 2-5)

Explicit high-density parameter sets reported in that paper (all at 30 µm layers and 0.13 mm hatch) include:

• 350 W, 1650 mm/s, h = 0.13 mm, t = 0.03 mm → VED ≈ 54 J/mm\(^3\). (hyer2020understandingthelaser pages 2-5)

• 250 W, 1200 mm/s, h = 0.13 mm, t = 0.03 mm → VED ≈ 53 J/mm\(^3\). (hyer2020understandingthelaser pages 2-5)

Overall, the evidence supports an “optimal” high-density AlSi10Mg window centered near ~50–60 J/mm\(^3\) with workable extension down toward ~30–40 J/mm\(^3\) and up toward ~80 J/mm\(^3\) depending on machine/strategy. (hyer2020understandingthelaser pages 1-2, hyer2020understandingthelaser pages 2-5)

2) Scalmalloy (Al-Mg-Sc-Zr)

A validated high-density parameter set on an EOS M290 is:

• P = 360 W, v = 1200 mm/s, h = 0.10 mm, t = 0.06 mm → VED = 50 J/mm\(^3\), with OM-measured density 99.7% (>99.5%). (ekubaru2022effectsofscanning pages 2-4)

This places Scalmalloy’s high-density VED requirement in the same ~50 J/mm\(^3\) band as AlSi10Mg under the cited conditions, despite Scalmalloy’s different solidification/precipitation behavior. (ekubaru2022effectsofscanning pages 2-4)

3) Al-Cu system

For a TiB\(_2\)-modified Al–Cu alloy (A205-like Al–Cu–Ag–Mg–Ti–TiB\(_2\)), Mair et al. report an optimized parameter set:

• P = 200 W, v = 1000 mm/s, h = 0.10 mm, t = 0.03 mm → VED = 67 J/mm\(^3\), achieving 99.9 ± 0.1% density (Archimedes) and 99.5 ± 0.1% (optical image analysis). (mair2021microstructureandmechanical pages 2-3)

Thus, in the retrieved evidence, Al–Cu-based high-density processing required VED modestly higher than the Scalmalloy/AlSi10Mg examples, but still in a similar order of magnitude (~50–70 J/mm\(^3\)). (mair2021microstructureandmechanical pages 2-3)

4) Al-Zn-Mg-Cu (7xxx; AA7075)

In the retrieved evidence, AA7075 required substantially higher VED to approach ~99.5% density, and densification is strongly entangled with cracking mitigation choices (scan strategy, defocus, and preheat). For volumetric specimens, Stopyra et al. report a best (highest) relative density of about 99.5% for:

• P = 200 W, v = 200 mm/s, hatch = 140 µm (0.14 mm), layer thickness = 50 µm (0.05 mm) → EV = 143 J/mm\(^3\), using a chessboard strategy and a negative defocus ΔF = −3.5 mm; however, hot cracks could not be eliminated completely. (stopyra2020laserpowderbed pages 22-27)

Figure-based evidence from the same study shows how relative density depends on scan speed and defocus at constant power with chessboard scanning (stopyra2020laserpowderbed media f309be68), and the process parameter set and EV = 143 J/mm\(^3\) are explicitly documented in the figure caption region. (stopyra2020laserpowderbed media 9fd38488)

Summary of VED ranges for ≥99.5% density in retrieved evidence

• AlSi10Mg: ~32–80 J/mm\(^3\) (with explicit high-density sets at ~53–54 J/mm\(^3\)). (hyer2020understandingthelaser pages 2-5, hyer2020understandingthelaser pages 1-2)

• Scalmalloy: ~50 J/mm\(^3\) (explicit, 99.7%). (ekubaru2022effectsofscanning pages 2-4)

• Al–Cu (TiB\(_2\)-modified): 67 J/mm\(^3\) (explicit, 99.5–99.9%). (mair2021microstructureandmechanical pages 2-3)

• AA7075 (7xxx): ~143 J/mm\(^3\) for “about 99.5%” in the cited setup, with cracking persisting. (stopyra2020laserpowderbed pages 22-27, stopyra2020laserpowderbed media 9fd38488)

Important caveats when interpreting “optimal windows”

VED collapses multiple degrees of freedom and is machine- and strategy-dependent; several sources caution that “optimal VED” can vary widely with beam size/focus, scan strategy, and density measurement method, even within AlSi10Mg. (zavalaarredondo2019useofpower pages 2-3, zavalaarredondo2019useofpower pages 10-12)

In particular for 7xxx systems, density and cracking are coupled; the Stopyra et al. evidence indicates that parameters improving density (e.g., defocus tuning) still left solidification cracks, and preheating reduced crack density but lowered relative density for the tested window. (stopyra2020laserpowderbed pages 22-27)

References

1. (yang2020laserpowderbed pages 1-2): Tao Yang, Tingting Liu, Wenhe Liao, Eric MacDonald, Huiliang Wei, Changdong Zhang, Xiangyuan Chen, and Kai Zhang. Laser powder bed fusion of alsi10mg: influence of energy intensities on spatter and porosity evolution, microstructure and mechanical properties. Journal of Alloys and Compounds, 849:156300, Dec 2020. URL: https://doi.org/10.1016/j.jallcom.2020.156300, doi:10.1016/j.jallcom.2020.156300. This article has 127 citations and is from a peer-reviewed journal.

2. (zavalaarredondo2019useofpower pages 2-3): Miguel Zavala-Arredondo, Tyler London, Madie Allen, Tomaso Maccio, Sam Ward, David Griffiths, Amanda Allison, Paul Goodwin, and Carl Hauser. Use of power factor and specific point energy as design parameters in laser powder-bed-fusion (l-pbf) of alsi10mg alloy. Materials & Design, 182:108018, Nov 2019. URL: https://doi.org/10.1016/j.matdes.2019.108018, doi:10.1016/j.matdes.2019.108018. This article has 77 citations and is from a highest quality peer-reviewed journal.

3. (hyer2020understandingthelaser pages 2-5): Holden Hyer, Le Zhou, Sharon Park, Guilherme Gottsfritz, George Benson, Bjorn Tolentino, Brandon McWilliams, Kyu Cho, and Yongho Sohn. Understanding the laser powder bed fusion of alsi10mg alloy. Metallography, Microstructure, and Analysis, 9:484-502, Jul 2020. URL: https://doi.org/10.1007/s13632-020-00659-w, doi:10.1007/s13632-020-00659-w. This article has 167 citations.

4. (hyer2020understandingthelaser pages 1-2): Holden Hyer, Le Zhou, Sharon Park, Guilherme Gottsfritz, George Benson, Bjorn Tolentino, Brandon McWilliams, Kyu Cho, and Yongho Sohn. Understanding the laser powder bed fusion of alsi10mg alloy. Metallography, Microstructure, and Analysis, 9:484-502, Jul 2020. URL: https://doi.org/10.1007/s13632-020-00659-w, doi:10.1007/s13632-020-00659-w. This article has 167 citations.

5. (ekubaru2022effectsofscanning pages 2-4): Yusufu Ekubaru, Ozkan Gokcekaya, and Takayoshi Nakano. Effects of scanning strategy on the microstructure and mechanical properties of sc-zr-modified al–mg alloy manufactured by laser powder bed fusion. Crystals, 12:1348, Sep 2022. URL: https://doi.org/10.3390/cryst12101348, doi:10.3390/cryst12101348. This article has 12 citations.

6. (mair2021microstructureandmechanical pages 2-3): P. Mair, L. Kaserer, Jakob Braun, N. Weinberger, I. Letofsky-Papst, and G. Leichtfried. Microstructure and mechanical properties of a tib2-modified al–cu alloy processed by laser powder-bed fusion. Materials Science and Engineering A-structural Materials Properties Microstructure and Processing, 799:140209, Jan 2021. URL: https://doi.org/10.1016/j.msea.2020.140209, doi:10.1016/j.msea.2020.140209. This article has 148 citations.

7. (stopyra2020laserpowderbed pages 22-27): Wojciech Stopyra, Konrad Gruber, Irina Smolina, Tomasz Kurzynowski, and Bogumiła Kuźnicka. Laser powder bed fusion of aa7075 alloy: influence of process parameters on porosity and hot cracking. Additive manufacturing, 35:101270, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101270, doi:10.1016/j.addma.2020.101270. This article has 303 citations and is from a highest quality peer-reviewed journal.

8. (stopyra2020laserpowderbed media f309be68): Wojciech Stopyra, Konrad Gruber, Irina Smolina, Tomasz Kurzynowski, and Bogumiła Kuźnicka. Laser powder bed fusion of aa7075 alloy: influence of process parameters on porosity and hot cracking. Additive manufacturing, 35:101270, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101270, doi:10.1016/j.addma.2020.101270. This article has 303 citations and is from a highest quality peer-reviewed journal.

9. (stopyra2020laserpowderbed media 9fd38488): Wojciech Stopyra, Konrad Gruber, Irina Smolina, Tomasz Kurzynowski, and Bogumiła Kuźnicka. Laser powder bed fusion of aa7075 alloy: influence of process parameters on porosity and hot cracking. Additive manufacturing, 35:101270, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101270, doi:10.1016/j.addma.2020.101270. This article has 303 citations and is from a highest quality peer-reviewed journal.

10. (zavalaarredondo2019useofpower pages 10-12): Miguel Zavala-Arredondo, Tyler London, Madie Allen, Tomaso Maccio, Sam Ward, David Griffiths, Amanda Allison, Paul Goodwin, and Carl Hauser. Use of power factor and specific point energy as design parameters in laser powder-bed-fusion (l-pbf) of alsi10mg alloy. Materials & Design, 182:108018, Nov 2019. URL: https://doi.org/10.1016/j.matdes.2019.108018, doi:10.1016/j.matdes.2019.108018. This article has 77 citations and is from a highest quality peer-reviewed journal.


---

## Query 4

**Question:** What quantitative solidification cracking susceptibility data exists for different aluminum alloy systems processed by LPBF? Which compositions show the widest crack-free process windows? What grain refiner additions (TiB2, TiC, ZrH2, ScalmAlloy-type Sc/Zr) most effectively suppress cracking?

**Task ID:** `86779cd0-a0ad-4059-9740-a7af8d2401db`

**Status:** complete

This response synthesizes quantitative LPBF solidification (hot) cracking susceptibility data that were retrievable in this run, across multiple Al alloy systems, emphasizing (i) explicit crack-free process windows and (ii) refiner/addition effectiveness.

| Alloy system / composition (wt.% unless noted) | Crack-susceptibility metric | Quantitative results | Grain refiner / addition | Notes / limitations |
|---|---|---|---|---|
| Al-6Zn-2Mg (ternary) | Crack density = total crack length per micrograph area, unit 1/µm; relative density/process window vs laser power and scan speed | At 200 W, peak density 99.2% only at 100 mm/s, but cracks increased with scan speed; at 350 W, cracks observed in all samples and crack density generally increased with scan speed. No practical crack-free LPBF window reported for the ternary alloy in the tested range. | None | Quantitative crack-density definition is explicit, but the excerpt does not report full numeric crack-density values point-by-point; low-speed dense condition was considered impractically slow because of Zn/Mg evaporation. (zhou2020processdependentcompositionmicrostructure pages 3-5) |
| Al-6Zn-2Mg-0.7Sc-0.3Zr (quinary) | Same crack-density metric as above; crack-free process window in power-scan-speed space | Crack-free, high-density LPBF window reported at 350 W with scan speed 800-1200 mm/s, and at 200 W with scan speed 400-800 mm/s. Peak density 99.7% at 350 W, 800 mm/s; 98.4% at 200 W, 800 mm/s. At 1200-1400 mm/s and 350 W, only isolated short cracks (<30 µm) occasionally observed. | Sc/Zr addition: 0.7 Sc + 0.3 Zr | Among the clearest quantitative crack-free windows in the retrieved evidence; Sc/Zr strongly suppressed cracking relative to ternary Al-6Zn-2Mg. (zhou2020processdependentcompositionmicrostructure pages 3-5) |
| AA6061 (unmodified) vs Zr-modified AA6061 | Crack density = overall crack length per unit area from >=5 optical micrographs in XY and XZ; relative density vs power/scan speed | Unmodified AA6061: extensive cracking at all tested conditions; at 200 W peak density only 97.6% at 300 mm/s. Zr-modified AA6061: remarkable disappearance of cracking for all examined LPBF parameters except minor crack-like features at 1600-1800 mm/s and 350 W; highest relative density 99.7% at 350 W and 1400 mm/s. Scan-speed range examined extended roughly from 100-800 mm/s at 200 W and 400-1800 mm/s at 350 W. | Zr modification (amount not given in excerpted pages; Zr forms Al3Zr nucleants) | Strong quantitative process-window evidence for near-crack-free behavior with Zr, but the excerpt does not reproduce absolute crack-density numbers from the figure. (mehta2021additivemanufacturingand pages 4-5) |
| EN AW 6182 / AlSi1MgZr (reported with Zr-containing powder) | lcrack = crack length per area (1/mm); VED influence; crack-free window via preheat | Example lcrack values at 400 °C preheat: 1.38, 1.13, 1.05, and 0.55 1/mm for different parameter sets. Increasing VED reduced cracking; at Ev = 54.17 J/mm^3 crack density was about 3× lower than at 36.93 J/mm^3. Crack-free specimens were achieved only at 500 °C preheat; below 500 °C no crack-free condition was found in this study. Maximum density at crack-free 500 °C condition: 99.0%; densities >99.5% were attainable within an optimal energy range. | Prealloyed Zr in 6182 (reported as Al3Zr-forming) plus high substrate preheat | Best quantitative preheat-controlled crack-suppression dataset in the evidence. Crack suppression at 500 °C also coincided with fully equiaxed grains (ECD ~19.46 µm). (riener2022processabilityofhighstrength pages 10-12, riener2022processabilityofhighstrength pages 2-4) |
| AA7075 + TiC nanoparticles | Crack density (reported in cracks/cm^2 in Table 4 / trend vs EV); crack-free VED/process window | Parameter study covered EV = 34.5-154.2 J/mm^3. Crack density generally decreased with increasing EV. Of 29 samples with EV >= 50 J/mm^3, 28 had >97.5% density. Crack-free state reported at EV = 93.3 J/mm^3 (Table 4 No. 7 / Fig. 6d). A practical crack-free example is PL = 350 W, vs = 750 mm/s, hd = 0.10 mm, yielding >99.9% density. One table line shown for comparison: unmodified AA7075 at 370 W, 900 mm/s, hd 0.08 mm, EV 102.8 J/mm^3 had crack density 154 cracks/cm^2 and 99.50% density. | TiC nanoparticles, especially 2.5 ma%; authors conclude >=1.75 ma% needed for strong crack reduction over a wide parameter range | Strongest direct quantitative evidence among refiner additions retrieved here. Exact full crack-density table for all TiC levels is not fully visible in excerpt, but crack-free EV and parameter set are explicit. (heiland2021requirementsforprocessing pages 8-10, heiland2021requirementsforprocessing pages 15-17, heiland2021requirementsforprocessing media 9ab36695) |
| AA2024 single-track LPBF / laser-track hot cracking | RDG-based hot-crack propensity via pressure drop at dendrite root (Δpmax); vulnerable-region area Avuln; G and cooling rate | Critical threshold for hot-crack initiation cited as Δp = 176 MPa. Vulnerable regions and higher Δpmax were associated with larger pulse distances (PD45 and PD60), which correlated with observed cracking. | None in this study | Mechanistic/single-track metric rather than bulk crack-free process window; useful as quantitative susceptibility threshold, not directly comparable to part-scale crack-density datasets. (guercio2024experimentalandcomputational pages 7-10) |
| Inoculated AA7075 / AA6061 with hydrogen-stabilized Zr nanoparticles leading to Al3Zr | Qualitative crack-free outcome under standard SLM conditions; no crack-density values reported in excerpt | Powder functionalization used 1 vol% hydrogen-stabilized Zr nucleants (>2 wt%) on ~45 µm prealloyed Al7075 and Al6061 powders. Processed on a 400 W Concept Laser M2 using vendor AlSi10Mg parameter set, island scan strategy (2 mm islands), 25-80 µm layers, flowing Ar, no build-plate preheat. Reported outcome: no observable cracking and fine equiaxed grains (~5 µm) versus large columnar/intercolumnar-cracked stock alloys. | 1 vol% H-stabilized Zr nanoparticles (forming Al3Zr in melt) | Very important proof-of-concept for crack elimination in 6xxx/7xxx, but excerpt lacks explicit power-speed-hatch values and numeric crack-density data; hydrogen stabilization also raises porosity/embrittlement concerns in later commentary. (heiland2021requirementsforprocessing pages 1-2, kotadiaUnknownyearkotadiahrgibbons pages 26-30, martin2018amethodologyand pages 136-141, stopyra2020laserpowderbed pages 6-9) |


*Table: This table compiles the quantitative solidification/hot-cracking metrics, crack-free processing windows, and grain-refiner effects found in the retrieved LPBF aluminum-alloy evidence. It highlights which alloy systems and additions have the clearest numeric evidence for crack suppression and practical process windows.*

## Quantitative cracking susceptibility datasets available (LPBF Al alloys)

### Al–Zn–Mg vs Al–Zn–Mg–Sc–Zr (7xxx-like model alloy)
Zhou et al. quantify cracking using crack density defined as total crack length per unit area (unit 1/µm) measured from optical micrographs, and explicitly map crack-free processing windows as a function of laser power and scan speed. For the quinary alloy Al-6Zn-2Mg-0.7Sc-0.3Zr, the reported crack-free high-density windows are: 350 W with scan speed 800–1200 mm/s, and 200 W with scan speed 400–800 mm/s. At faster speeds (1200–1400 mm/s, 350 W), only isolated short cracks (<30 µm) were occasionally observed. In contrast, the ternary Al-6Zn-2Mg showed cracks that increased with scan speed and (at 350 W) cracks in all samples, i.e., no comparable practical crack-free window in the tested range. (zhou2020processdependentcompositionmicrostructure pages 3-5)

### AA6061: unmodified vs Zr-modified (Al–Mg–Si, 6xxx)
Mehta et al. also use crack density = total crack length per unit area (from ≥5 micrographs) and examine broad scan-speed ranges at 200 and 350 W. Unmodified AA6061 exhibited extensive cracking across all tested conditions. Zr-modified AA6061 showed a “remarkable disappearance of cracking” across essentially all tested parameters, with only minor crack-like features at the highest scan speeds (~1600–1800 mm/s) at 350 W. A high-density condition highlighted by the authors is 350 W at 1400 mm/s, reaching 99.7% relative density. This constitutes one of the widest crack-suppressed (near-crack-free) parameter envelopes found in the retrievable evidence here, albeit without a fully enumerated numerical crack-density map in the excerpted text. (mehta2021additivemanufacturingand pages 4-5)

### EN AW 6182 (AlSi1MgZr, 6xxx-like) with substrate preheating
Riener et al. provide explicit numerical crack-length-per-area values (lcrack, 1/mm) and show that preheating dominates crack suppression: crack-free specimens were achieved only at 500 °C preheat (and were not achieved below 500 °C in that study). Example lcrack values at 400 °C preheat are 1.38, 1.13, 1.05, and 0.55 1/mm for different parameter sets, and increasing volumetric energy density (VED) reduces cracking (e.g., at Ev = 54.17 J/mm3 the crack density is roughly three times lower than at 36.93 J/mm3). (riener2022processabilityofhighstrength pages 10-12)

### AA7075 with TiC nanoparticles (Al–Zn–Mg–Cu, 7xxx)
Heiland et al. provide one of the clearest quantitative “process window + refiner” datasets in this run. They map crack density and relative density versus volumetric energy input (EV) for AA7075 decorated with TiC nanoparticles (notably AA7075/TiC/2.5). The parameter study spans EV = 34.5–154.2 J/mm3; crack density decreases with increasing EV, and a crack-free condition is reported at EV = 93.3 J/mm3 (Table 4 No. 7 / Fig. 6d) while maintaining 99.9% relative density. They also report a practical crack-free parameter example: PL = 350 W, vs = 750 mm/s, hd = 0.10 mm, yielding >99.9% relative density. Their conclusion states ≥1.75 ma% TiC is required for significant crack reduction/prevention over a wide parameter range, with 2.5 ma% enabling crack-free dense parts. (heiland2021requirementsforprocessing pages 8-10, heiland2021requirementsforprocessing pages 15-17)

### AA2024 single-track mechanistic hot-cracking metric (Al–Cu–Mg, 2xxx)
Del Guercio et al. report a mechanistic RDG-based criterion for hot cracking in single laser tracks of AA2024: a hot-crack propensity expressed as a pressure drop (Δpmax) at the dendrite root, referencing a literature critical threshold for crack initiation of 176 MPa. This is a quantitative susceptibility threshold but is not directly a part-scale “crack-free process window” and is not tied to grain-refiner additions in the retrieved excerpt. (guercio2024experimentalandcomputational pages 7-10)

## Which compositions show the widest crack-free process windows (within retrievable quantitative evidence)

1) **Zr-modified AA6061** shows the broadest crack-suppressed envelope in the retrieved data: cracking was nearly eliminated across a wide scan-speed range at both 200 and 350 W, with only minor crack-like features at the highest scan speeds (~1600–1800 mm/s at 350 W). (mehta2021additivemanufacturingand pages 4-5)

2) **Al-6Zn-2Mg-0.7Sc-0.3Zr** shows the clearest explicit crack-free “window” definition (two wide scan-speed intervals at two powers: 200 W and 350 W), outperforming the corresponding ternary Al-6Zn-2Mg. (zhou2020processdependentcompositionmicrostructure pages 3-5)

3) **AA7075 + 2.5 ma% TiC** has an explicitly identified crack-free VED condition (EV = 93.3 J/mm3) and a practical crack-free parameter set; the window is well-characterized in EV space, but the excerpted evidence here does not fully enumerate all crack-free points as a continuous multi-parameter window beyond the EV sweep. (heiland2021requirementsforprocessing pages 8-10, heiland2021requirementsforprocessing pages 15-17)

4) **EN AW 6182** is crack-free only under a stringent auxiliary condition (500 °C preheat), indicating a narrower operational window unless high preheat is available/acceptable. (riener2022processabilityofhighstrength pages 10-12)

## Grain refiners/additions most effective at suppressing cracking (as supported by quantitative evidence here)

### Most strongly supported (quantitative process windows/conditions)
- **TiC nanoparticles (AA7075; 7xxx):** 2.5 ma% TiC enables crack-free dense parts; crack-free at EV = 93.3 J/mm3 and >99.9% density with example PL = 350 W, vs = 750 mm/s, hd = 0.10 mm; ≥1.75 ma% needed for strong crack reduction across a wide parameter range. (heiland2021requirementsforprocessing pages 8-10, heiland2021requirementsforprocessing pages 15-17, heiland2021requirementsforprocessing media 9ab36695)
- **Sc/Zr microalloying (Al-6Zn-2Mg-0.7Sc-0.3Zr):** explicit crack-free scan-speed windows at 200 and 350 W, with only occasional short cracks at higher speeds; this is direct evidence of broad cracking suppression vs a ternary baseline. (zhou2020processdependentcompositionmicrostructure pages 3-5)
- **Zr modification forming Al3Zr nucleants (AA6061):** near-complete elimination of cracking across broad conditions at 200/350 W; this is strong window-level suppression, though the excerpted pages do not list exact Zr wt.% used. (mehta2021additivemanufacturingand pages 4-5)

### Supported but not fully quantitative in retrieved excerpts
- **Hydrogen-stabilized Zr nanoparticle inoculation (often reported as ZrH2-stabilized Zr source, forming Al3Zr):** a thesis-style source reports 1 vol% hydrogen-stabilized Zr nucleants on Al6061/Al7075 powders, processed on a Concept Laser M2 using a vendor AlSi10Mg parameter set, producing crack-free equiaxed microstructures without build-plate preheat; however, the retrieved excerpt lacks crack-density numbers and does not list the detailed laser power/scan speed/hatch parameters. (martin2018amethodologyand pages 136-141)

### Evidence gap in this run (TiB2 and ZrH2 specifically)
TiB2 is discussed in the retrieved corpus as a potent nucleant in Al alloys (including 2xxx/7xxx contexts), and ZrH2 nanoparticle coating is referenced in review-style sources, but **this run did not retrieve a primary LPBF dataset with quantitative crack density and an explicit crack-free process window for either TiB2- or ZrH2-treated alloys**. Therefore, within the quantitative evidence assembled here, TiC and Sc/Zr (and Zr/Al3Zr modification) are currently the best-supported crack suppressors. (sun2022theroleof pages 1-3, heiland2021requirementsforprocessing pages 1-2, stopyra2020laserpowderbed pages 6-9)

## Visual quantitative evidence (TiC in 7075)
The crack-density/relative-density vs EV mapping for AA7075/TiC/2.5, including the crack-free EV = 93.3 J/mm3 condition, is shown in the retrieved figure/table crops from Heiland et al. (heiland2021requirementsforprocessing media 9ab36695, heiland2021requirementsforprocessing media 41a171e2, heiland2021requirementsforprocessing media 57540699)

References

1. (zhou2020processdependentcompositionmicrostructure pages 3-5): Le Zhou, Holden Hyer, Saket Thapliyal, Rajiv S. Mishra, Brandon McWilliams, Kyu Cho, and Yongho Sohn. Process-dependent composition, microstructure, and printability of al-zn-mg and al-zn-mg-sc-zr alloys manufactured by laser powder bed fusion. Metallurgical and Materials Transactions A, 51:3215-3227, Apr 2020. URL: https://doi.org/10.1007/s11661-020-05768-3, doi:10.1007/s11661-020-05768-3. This article has 97 citations.

2. (mehta2021additivemanufacturingand pages 4-5): Abhishek Mehta, Le Zhou, Thinh Huynh, Sharon Park, Holden Hyer, Shutao Song, Yuanli Bai, D. Devin Imholte, Nicolas E. Woolstenhulme, Daniel M. Wachs, and Yongho Sohn. Additive manufacturing and mechanical properties of the dense and crack free zr-modified aluminum alloy 6061 fabricated by the laser-powder bed fusion. Additive Manufacturing, 41:101966, May 2021. URL: https://doi.org/10.1016/j.addma.2021.101966, doi:10.1016/j.addma.2021.101966. This article has 230 citations and is from a highest quality peer-reviewed journal.

3. (riener2022processabilityofhighstrength pages 10-12): Kirstin Riener, Tino Pfalz, Florian Funcke, and Gerhard Leichtfried. Processability of high-strength aluminum 6182 series alloy via laser powder bed fusion (lpbf). The International Journal of Advanced Manufacturing Technology, 119:4963-4977, Jan 2022. URL: https://doi.org/10.1007/s00170-022-08673-8, doi:10.1007/s00170-022-08673-8. This article has 46 citations.

4. (riener2022processabilityofhighstrength pages 2-4): Kirstin Riener, Tino Pfalz, Florian Funcke, and Gerhard Leichtfried. Processability of high-strength aluminum 6182 series alloy via laser powder bed fusion (lpbf). The International Journal of Advanced Manufacturing Technology, 119:4963-4977, Jan 2022. URL: https://doi.org/10.1007/s00170-022-08673-8, doi:10.1007/s00170-022-08673-8. This article has 46 citations.

5. (heiland2021requirementsforprocessing pages 8-10): Steffen Heiland, Benjamin Milkereit, Kay-Peter Hoyer, Evgeny Zhuravlev, Olaf Kessler, and Mirko Schaper. Requirements for processing high-strength alznmgcu alloys with pbf-lb/m to achieve crack-free and dense parts. Materials, 14:7190, Nov 2021. URL: https://doi.org/10.3390/ma14237190, doi:10.3390/ma14237190. This article has 21 citations.

6. (heiland2021requirementsforprocessing pages 15-17): Steffen Heiland, Benjamin Milkereit, Kay-Peter Hoyer, Evgeny Zhuravlev, Olaf Kessler, and Mirko Schaper. Requirements for processing high-strength alznmgcu alloys with pbf-lb/m to achieve crack-free and dense parts. Materials, 14:7190, Nov 2021. URL: https://doi.org/10.3390/ma14237190, doi:10.3390/ma14237190. This article has 21 citations.

7. (heiland2021requirementsforprocessing media 9ab36695): Steffen Heiland, Benjamin Milkereit, Kay-Peter Hoyer, Evgeny Zhuravlev, Olaf Kessler, and Mirko Schaper. Requirements for processing high-strength alznmgcu alloys with pbf-lb/m to achieve crack-free and dense parts. Materials, 14:7190, Nov 2021. URL: https://doi.org/10.3390/ma14237190, doi:10.3390/ma14237190. This article has 21 citations.

8. (guercio2024experimentalandcomputational pages 7-10): G. Del Guercio, S. Faron, D. G. McCartney, S. Robertson, N. T. Aboulkhair, C. Tuck, A. T. Clare, and M. Simonelli. Experimental and computational studies on hot cracking in single laser tracks of aluminium alloy aa2024 and related implications for laser powder bed fusion. Discover Materials, Nov 2024. URL: https://doi.org/10.1007/s43939-024-00154-x, doi:10.1007/s43939-024-00154-x. This article has 2 citations.

9. (heiland2021requirementsforprocessing pages 1-2): Steffen Heiland, Benjamin Milkereit, Kay-Peter Hoyer, Evgeny Zhuravlev, Olaf Kessler, and Mirko Schaper. Requirements for processing high-strength alznmgcu alloys with pbf-lb/m to achieve crack-free and dense parts. Materials, 14:7190, Nov 2021. URL: https://doi.org/10.3390/ma14237190, doi:10.3390/ma14237190. This article has 21 citations.

10. (kotadiaUnknownyearkotadiahrgibbons pages 26-30): HR Kotadia. Kotadia, hr, gibbons, g, das, a and howes, pd a review of laser powder bed fusion additive manufacturing of aluminium alloys: microstructure and …. Unknown journal, Unknown year.

11. (martin2018amethodologyand pages 136-141): JH Martin. A methodology and analysis of inoculation in additive aluminum alloys. Unknown journal, 2018.

12. (stopyra2020laserpowderbed pages 6-9): Wojciech Stopyra, Konrad Gruber, Irina Smolina, Tomasz Kurzynowski, and Bogumiła Kuźnicka. Laser powder bed fusion of aa7075 alloy: influence of process parameters on porosity and hot cracking. Additive manufacturing, 35:101270, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101270, doi:10.1016/j.addma.2020.101270. This article has 303 citations and is from a highest quality peer-reviewed journal.

13. (sun2022theroleof pages 1-3): Tengteng Sun, Hongze Wang, Zhenyang Gao, Yi Wu, Mingliang Wang, Xinyuan Jin, Chu Lun Alex Leung, P.D. Lee, Yanan Fu, and Haowei Wang. The role of in-situ nano-tib2 particles in improving the printability of noncastable 2024al alloy. Materials Research Letters, 10:656-665, May 2022. URL: https://doi.org/10.1080/21663831.2022.2080514, doi:10.1080/21663831.2022.2080514. This article has 62 citations and is from a peer-reviewed journal.

14. (heiland2021requirementsforprocessing media 41a171e2): Steffen Heiland, Benjamin Milkereit, Kay-Peter Hoyer, Evgeny Zhuravlev, Olaf Kessler, and Mirko Schaper. Requirements for processing high-strength alznmgcu alloys with pbf-lb/m to achieve crack-free and dense parts. Materials, 14:7190, Nov 2021. URL: https://doi.org/10.3390/ma14237190, doi:10.3390/ma14237190. This article has 21 citations.

15. (heiland2021requirementsforprocessing media 57540699): Steffen Heiland, Benjamin Milkereit, Kay-Peter Hoyer, Evgeny Zhuravlev, Olaf Kessler, and Mirko Schaper. Requirements for processing high-strength alznmgcu alloys with pbf-lb/m to achieve crack-free and dense parts. Materials, 14:7190, Nov 2021. URL: https://doi.org/10.3390/ma14237190, doi:10.3390/ma14237190. This article has 21 citations.


---

## Query 5

**Question:** What residual stress magnitudes have been measured in LPBF aluminum alloy parts? Compare residual stress levels across AlSi10Mg, Scalmalloy, and other AM Al alloys. How do scan strategy, preheating, and post-processing (stress relief, HIP) reduce residual stress?

**Task ID:** `3189eb79-9ad8-464e-aa83-ab72ac0dadfc`

**Status:** complete

## Scope and interpretation
Residual stress (RS) magnitudes reported in the LPBF aluminum literature depend strongly on (i) measurement technique and probe volume (e.g., XRD near-surface vs neutron diffraction bulk), and (ii) whether *phase-specific* stresses are reported (e.g., Si phase vs Al matrix in AlSi10Mg). Below, I summarize **measured** RS magnitudes (MPa) available in the retrieved full texts, compare AlSi10Mg vs Scalmalloy®, and quantify how scan strategy (where possible), baseplate preheating, and post-processing reduce RS.

## Quantitative comparison across alloys (measured magnitudes)

| Alloy | Condition | Measurement method | Stress type/location (surface vs bulk; direction) | Residual stress magnitude(s) in MPa (with sign, range, uncertainty) | Notes on scan strategy/preheating/post-processing | Source citation IDs |
|---|---|---|---|---|---|---|
| AlSi10Mg | As-built (AM_AB) | XRD + Williamson–Hall analysis | Surface / Al matrix | +56 ± 14 | LPBF; example AB case reported with 67° layer rotation and 100 °C platform in the paper; local surface tensile stress in Al reflections | (marola2021residualstressesin pages 9-10) |
| AlSi10Mg | As-built (AM_AB) | XRD + Williamson–Hall analysis | Surface / Si phase | +840 ± 560 | Very high local tensile stress in nanometric Si; much higher than matrix stress because phase-specific/local stress is being probed | (marola2021residualstressesin pages 9-10) |
| AlSi10Mg | As-built (AM_AB) | Composite transfer model using XRD Al stress | Surface / Si phase, Z direction | +56 to +79 | Modelled transferred stress in Si particles from measured Al-matrix stress | (marola2021residualstressesin pages 9-10) |
| AlSi10Mg | As-built (AM_AB) | Composite transfer model using XRD Al stress | Surface / Si phase, XY direction | +126 to +175 | Modelled in-plane Si stress higher than Z direction | (marola2021residualstressesin pages 9-10) |
| AlSi10Mg | Stress relieved (AM_SR) | XRD + Williamson–Hall analysis | Surface / Si phase | +252 ± 42 | Conventional stress relief substantially reduced Si-phase tensile residual stress from as-built value | (marola2021residualstressesin pages 9-10) |
| AlSi10Mg | Stress relieved (AM_SR) | Composite transfer model using XRD Al stress | Surface / Si phase, Z direction | +25 to +34 | Lower than as-built, indicating partial stress relaxation after SR | (marola2021residualstressesin pages 9-10) |
| AlSi10Mg | Stress relieved (AM_SR) | Composite transfer model using XRD Al stress | Surface / Si phase, XY direction | +46 to +52 | Reduced from +126 to +175 MPa in AB condition | (marola2021residualstressesin pages 9-10) |
| AlSi10Mg | As-built, 200 °C baseplate preheat | Neutron diffraction | Bulk / notch field, tensile | ~+20 | Roveda et al. studied specimens built on a 200 °C baseplate; as-built bulk stresses were already low | (roveda2022influenceofa pages 9-12, roveda2022influenceofa pages 1-3) |
| AlSi10Mg | As-built, 200 °C baseplate preheat | Neutron diffraction | Bulk / nominal field, tensile | ~+10 | Low bulk tensile residual stress due to elevated platform temperature | (roveda2022influenceofa pages 9-12, roveda2022influenceofa pages 1-3) |
| AlSi10Mg | As-built, 200 °C baseplate preheat | Energy-dispersive XRD (sin²ψ) | Near-surface / LD component | ~−50 | Stabilized compressive near-surface stress away from nearest-notch point | (roveda2022influenceofa pages 9-12) |
| AlSi10Mg | As-built, 200 °C baseplate preheat | Energy-dispersive XRD (sin²ψ) | Near-surface / BD component | ~−35 | Stabilized compressive near-surface stress | (roveda2022influenceofa pages 9-12) |
| AlSi10Mg | Literature comparison: 35 °C platform | XRD/literature cited in Roveda | Stress range (not explicitly surface/bulk) | ~90 range | Cited as representative low-preheat condition | (roveda2022influenceofa pages 1-3, roveda2022influenceofa pages 3-4) |
| AlSi10Mg | Literature comparison: 200 °C platform | XRD/literature cited in Roveda | Stress range (not explicitly surface/bulk) | <15 range | About 87% lower than the ~90 MPa range at 35 °C platform preheat | (roveda2022influenceofa pages 1-3, roveda2022influenceofa pages 3-4) |
| Scalmalloy® | As-built (AB) | Hole-drilling / strain rosette | Near-surface profile | Tensile at surface; compressive below ~0.4 mm | Numerical AB magnitudes not quoted in extracted text, but profile shape is reported | (zha2026surfaceandstructural pages 4-6) |
| Scalmalloy® | Heat treated (HT; paper cites 325 °C/4 h) | Hole-drilling / strain rosette | Near-surface profile | Near-zero, nearly uniform | HT effectively relieved residual stress compared with AB profile | (zha2026surfaceandstructural pages 2-4, zha2026surfaceandstructural pages 4-6) |
| Scalmalloy® | Shot peened | Hole-drilling | Near-surface compressive residual stress / 15 mm, 4 bar, 120 s | −267 ± 12 | Maximum CRS at ~125 ± 9 µm; influenced depth ~175 ± 9 µm | (zha2026surfaceandstructural pages 8-10) |
| Scalmalloy® | Shot peened | Hole-drilling | Near-surface compressive residual stress / 150 mm, 4 bar, 20 s | −231 ± 9 | Chosen as favorable condition balancing compressive stress and surface damage; max at ~75 ± 3 µm; influenced depth ~175 ± 5 µm | (zha2026surfaceandstructural pages 8-10) |
| Scalmalloy® | Shot peened | Hole-drilling | Near-surface compressive residual stress / 150 mm, 4 bar, 120 s | −182 ± 8 | Max at ~75 ± 6 µm; influenced depth ~325 ± 14 µm | (zha2026surfaceandstructural pages 8-10) |
| Scalmalloy® | Shot peened | Hole-drilling | Near-surface compressive residual stress / 150 mm, 6 bar, 120 s | −273 ± 11 | Strongest compressive stress reported; shallow max at ~25 ± 2 µm; influenced depth ~125 ± 6 µm | (zha2026surfaceandstructural pages 8-10) |
| Scalmalloy® | Shot-peened conditions (overall range) | Hole-drilling | Near-surface / just below surface | −60 to −273 | Reported range for treatments at 150 mm peening distance | (zha2026surfaceandstructural pages 6-8, zha2026surfaceandstructural pages 8-10) |
| Al–Mn–Sc alloy | AF, 35 °C platform (room-temperature baseplate) | XRD sin²ψ | Surface / along 3 cm build-direction profile, tensile | +154 ± 4 to +190 ± 2 | As-fabricated state without platform preheating; significant tensile RS | (bayoumy2023effectiveplatformheating pages 3-6) |
| Al–Mn–Sc alloy | AF-200, 200 °C platform preheat | XRD sin²ψ | Surface / along 3 cm build-direction profile, tensile | +59 ± 2 to +88 ± 3 | Platform heating reduced RS by ~95 to 102 MPa absolute, roughly 54–62%; AF-200 stress level is ~57% of AF per authors’ wording | (bayoumy2023effectiveplatformheating pages 3-6, bayoumy2023effectiveplatformheating pages 6-8) |


*Table: This table summarizes measured residual stress magnitudes reported for LPBF aluminum alloys in the gathered evidence, including AlSi10Mg, Scalmalloy®, and a related Al–Mn–Sc alloy. It is useful for directly comparing stress levels across alloys, measurement methods, and mitigation conditions such as platform preheating, heat treatment, and shot peening.*

### AlSi10Mg
*Surface / phase-specific residual stress (XRD)*
- Using XRD + Williamson–Hall analysis, the Al-matrix (Al reflections) stress in as-built LPBF AlSi10Mg was reported as **+56 ± 14 MPa**. In the same work, Williamson–Hall analysis on Si reflections yielded a much higher apparent Si-phase tensile stress in the as-built condition (**+840 ± 560 MPa**), which decreased after stress relief to **+252 ± 42 MPa**. (marola2021residualstressesin pages 9-10)
- Using a composite stress-transfer model (Eshelby-type) based on the measured Al stress, the inferred Si stresses were far lower than the WH(Si) result: as-built **+56 to +79 MPa (Z)** and **+126 to +175 MPa (XY)**, decreasing after stress relief to **+25 to +34 MPa (Z)** and **+46 to +52 MPa (XY)**. (marola2021residualstressesin pages 9-10)

*Bulk vs near-surface (neutron diffraction and EDXRD) in a preheated build*
- In a study where AlSi10Mg was built on a **200 °C baseplate**, neutron diffraction indicated **low tensile bulk RS**: ~**+20 MPa** in a notch field and ~**+10 MPa** in a nominal field. (roveda2022influenceofa pages 9-12, roveda2022influenceofa pages 1-3)
- In the same study, energy-dispersive XRD (sin²ψ) near-surface measurements showed stabilized compressive values around **−50 MPa** (load direction) and **−35 MPa** (build direction) at locations away from the least-compressive notch point. (roveda2022influenceofa pages 9-12)

### Scalmalloy® (Al–Mg–Sc–Zr)
- Hole-drilling measurements showed that **as-built Scalmalloy®** had a **tensile surface RS state** with **compressive RS beneath ~0.4 mm**, while a **heat-treated** condition produced an approximately **near-zero, nearly uniform RS profile** (numerical magnitudes not provided in the extracted text). (zha2026surfaceandstructural pages 4-6)
- Shot peening converted the near-surface RS state to **compressive residual stress (CRS)**, with maximum CRS values between about **−182 ± 8 MPa** and **−273 ± 11 MPa**, occurring at shallow depths (~**25–125 μm**) and with influenced depths of ~**125–325 μm**, depending on peening distance/pressure/time. (zha2026surfaceandstructural pages 8-10, zha2026surfaceandstructural pages 6-8)

### Other LPBF Al alloys (available quantified evidence in retrieved texts)
Direct numeric RS magnitudes for LPBF AA7075 and LPBF Al2024 were not available in the accessible full texts retrieved here (the available 7075 paper focused on crack/defect evolution and HIP crack healing mechanisms without RS magnitudes; the 2024 CaB6 paper focused on microstructure/mechanical properties). (mair2021laserpowderbed pages 8-9, stopyra2020laserpowderbed pages 31-35)

However, **a Sc-containing LPBF Al alloy (Al–Mn–Sc)** provides an “other alloy” benchmark with clear RS magnitudes:
- As-fabricated on an unheated (~35 °C) platform: tensile surface RS **+154 ± 4 to +190 ± 2 MPa**.
- With **200 °C platform preheating**: tensile surface RS reduced to **+59 ± 2 to +88 ± 3 MPa**. (bayoumy2023effectiveplatformheating pages 3-6)
These values are also shown graphically in the extracted figure. (bayoumy2023effectiveplatformheating media cf1c659b)

## How process choices reduce residual stress (quantified where possible)

### 1) Scan strategy
- From the retrieved evidence set, scan strategy effects were only supported **qualitatively** for AlSi10Mg: stripe scanning tends to produce higher RS than a chessboard strategy; inter-layer rotation can reduce thermal accumulation indicators, which is commonly linked to reduced RS, but robust MPa-vs-MPa scan-strategy comparisons were not available in the acquired full texts. (roveda2022influenceofa pages 3-4, yadav2022microstructuralandmechanical pages 30-33)
- In the AlSi10Mg XRD/Raman study, scan-path variants and platform temperatures (35 °C vs 100 °C) and stress relief were part of the experimental design, but the specific MPa-by-scan-strategy breakdown was not present in the extracted evidence snippet used here. (marola2021residualstressesin pages 1-2)

### 2) Baseplate/platform preheating
Preheating reduces RS primarily by lowering thermal gradients and reducing the magnitude of thermally driven contraction mismatch during solidification/cooling.
- **AlSi10Mg (literature summarized in Roveda et al.)**: a reported RS range of about **~90 MPa** at **35 °C** platform temperature dropped to **<15 MPa** when the platform was preheated to **200 °C** (≈**87% reduction** in range). (roveda2022influenceofa pages 3-4)
- **Al–Mn–Sc LPBF alloy (direct measurements)**: increasing platform temperature from **35 °C** to **200 °C** reduced tensile surface RS from **154–190 MPa** to **59–88 MPa** (absolute drop ~**95–102 MPa**, corresponding roughly to a **~54–62% reduction** in the bounds). (bayoumy2023effectiveplatformheating pages 3-6, bayoumy2023effectiveplatformheating media cf1c659b)

### 3) Post-processing: stress relief heat treatment
Stress relief reduces RS by enabling plastic relaxation/creep and recovery mechanisms at elevated temperature; in Al–Si alloys, it can also change Si morphology and redistribute stresses between phases.
- **AlSi10Mg**: in phase-specific XRD results, stress relief reduced Si-phase tensile stress from **+840 ± 560 MPa** (as-built, WH on Si) to **+252 ± 42 MPa**. (marola2021residualstressesin pages 9-10)
- In the same work, a stress-transfer model also showed consistent decreases in inferred Si stresses (e.g., **XY: +126–175 → +46–52 MPa**). (marola2021residualstressesin pages 9-10)
- **AlSi10Mg built on a 200 °C platform** already exhibited low bulk stresses, and a subsequent 265 °C/1 h treatment primarily redistributed rather than reduced the magnitude in that specific study (as described in the paper’s framing and bulk/near-surface results). (roveda2022influenceofa pages 1-3, roveda2022influenceofa pages 9-12)
- **Scalmalloy®**: heat-treated condition (the paper cites 325 °C/4 h) produced a near-zero, nearly uniform near-surface RS profile relative to the as-built condition (numerical values not in extracted text). (zha2026surfaceandstructural pages 2-4, zha2026surfaceandstructural pages 4-6)

### 4) HIP (hot isostatic pressing)
In the retrieved full texts, HIP was discussed for AA7075 primarily as a **defect/crack healing** approach (healing short cracks via liquation + compressive stresses), but **no RS magnitudes before/after HIP** were provided in the extracted content; thus RS reduction by HIP cannot be quantified from this evidence set. (stopyra2020laserpowderbed pages 31-35)

## Practical takeaways (evidence-backed)
- **Highest measured RS magnitudes** in the retrieved evidence occur when one reports **phase-specific local stresses** in AlSi10Mg (Si phase, XRD/WH), reaching hundreds of MPa (up to ~0.8 GPa), while the **Al matrix** and **bulk** stresses can be far smaller (tens of MPa), especially with platform preheating. (marola2021residualstressesin pages 9-10, roveda2022influenceofa pages 9-12, roveda2022influenceofa pages 3-4)
- **Platform preheating to ~200 °C** consistently reduces tensile RS substantially (often by ~50%+ in directly measured surface values, and can reduce stress ranges to near-negligible levels in some AlSi10Mg reports). (roveda2022influenceofa pages 3-4, bayoumy2023effectiveplatformheating pages 3-6, bayoumy2023effectiveplatformheating media cf1c659b)
- **Stress relief heat treatment** reduces phase-specific tensile RS in AlSi10Mg (particularly in the Si phase) and can bring Scalmalloy® near-surface RS close to zero. (marola2021residualstressesin pages 9-10, zha2026surfaceandstructural pages 4-6)
- **Surface mechanical treatments (shot peening)** can impose beneficial compressive RS in Scalmalloy® on the order of **−200 to −270 MPa**, albeit in a shallow surface layer (tens to hundreds of microns). (zha2026surfaceandstructural pages 8-10, zha2026surfaceandstructural pages 6-8)

## Limitations of the evidence retrieved here
The retrieved, accessible full texts did not contain numerical RS magnitudes for LPBF AA7075 or LPBF Al2024 (including modified variants) needed for a fully quantitative multi-alloy comparison beyond the AlSi10Mg/Scalmalloy/Al–Mn–Sc cases summarized above. (mair2021laserpowderbed pages 8-9, stopyra2020laserpowderbed pages 31-35)

References

1. (marola2021residualstressesin pages 9-10): Silvia Marola, Silvia Bosia, Alessandro Veltro, Gianluca Fiore, Diego Manfredi, Mariangela Lombardi, Giampiero Amato, Marcello Baricco, and Livio Battezzati. Residual stresses in additively manufactured alsi10mg: raman spectroscopy and x-ray diffraction analysis. Materials & Design, 202:109550, Apr 2021. URL: https://doi.org/10.1016/j.matdes.2021.109550, doi:10.1016/j.matdes.2021.109550. This article has 94 citations and is from a highest quality peer-reviewed journal.

2. (roveda2022influenceofa pages 9-12): Ilaria Roveda, Itziar Serrano-Munoz, Tatiana Mishurova, Mauro Madia, Thilo Pirling, Alexander Evans, Manuela Klaus, Jan Haubrich, Guillermo Requena, and Giovanni Bruno. Influence of a 265 °c heat treatment on the residual stress state of a pbf-lb/m alsi10mg alloy. Journal of Materials Science, 57:22082-22098, Dec 2022. URL: https://doi.org/10.1007/s10853-022-07997-w, doi:10.1007/s10853-022-07997-w. This article has 11 citations and is from a peer-reviewed journal.

3. (roveda2022influenceofa pages 1-3): Ilaria Roveda, Itziar Serrano-Munoz, Tatiana Mishurova, Mauro Madia, Thilo Pirling, Alexander Evans, Manuela Klaus, Jan Haubrich, Guillermo Requena, and Giovanni Bruno. Influence of a 265 °c heat treatment on the residual stress state of a pbf-lb/m alsi10mg alloy. Journal of Materials Science, 57:22082-22098, Dec 2022. URL: https://doi.org/10.1007/s10853-022-07997-w, doi:10.1007/s10853-022-07997-w. This article has 11 citations and is from a peer-reviewed journal.

4. (roveda2022influenceofa pages 3-4): Ilaria Roveda, Itziar Serrano-Munoz, Tatiana Mishurova, Mauro Madia, Thilo Pirling, Alexander Evans, Manuela Klaus, Jan Haubrich, Guillermo Requena, and Giovanni Bruno. Influence of a 265 °c heat treatment on the residual stress state of a pbf-lb/m alsi10mg alloy. Journal of Materials Science, 57:22082-22098, Dec 2022. URL: https://doi.org/10.1007/s10853-022-07997-w, doi:10.1007/s10853-022-07997-w. This article has 11 citations and is from a peer-reviewed journal.

5. (zha2026surfaceandstructural pages 4-6): Dexiang Zha, Alessandro Fortunato, Alessandro Ascari, Enrico Troiani, and Erica Liverani. Surface and structural integrity evaluation of additively manufactured scalmalloy®. Progress in Additive Manufacturing, 11:25-37, Sep 2026. URL: https://doi.org/10.1007/s40964-025-01332-w, doi:10.1007/s40964-025-01332-w. This article has 0 citations and is from a peer-reviewed journal.

6. (zha2026surfaceandstructural pages 2-4): Dexiang Zha, Alessandro Fortunato, Alessandro Ascari, Enrico Troiani, and Erica Liverani. Surface and structural integrity evaluation of additively manufactured scalmalloy®. Progress in Additive Manufacturing, 11:25-37, Sep 2026. URL: https://doi.org/10.1007/s40964-025-01332-w, doi:10.1007/s40964-025-01332-w. This article has 0 citations and is from a peer-reviewed journal.

7. (zha2026surfaceandstructural pages 8-10): Dexiang Zha, Alessandro Fortunato, Alessandro Ascari, Enrico Troiani, and Erica Liverani. Surface and structural integrity evaluation of additively manufactured scalmalloy®. Progress in Additive Manufacturing, 11:25-37, Sep 2026. URL: https://doi.org/10.1007/s40964-025-01332-w, doi:10.1007/s40964-025-01332-w. This article has 0 citations and is from a peer-reviewed journal.

8. (zha2026surfaceandstructural pages 6-8): Dexiang Zha, Alessandro Fortunato, Alessandro Ascari, Enrico Troiani, and Erica Liverani. Surface and structural integrity evaluation of additively manufactured scalmalloy®. Progress in Additive Manufacturing, 11:25-37, Sep 2026. URL: https://doi.org/10.1007/s40964-025-01332-w, doi:10.1007/s40964-025-01332-w. This article has 0 citations and is from a peer-reviewed journal.

9. (bayoumy2023effectiveplatformheating pages 3-6): Dina Bayoumy, Torben Boll, Amal Shaji Karapuzha, Xinhua Wu, Yuman Zhu, and Aijun Huang. Effective platform heating for laser powder bed fusion of an al-mn-sc-based alloy. Materials, Dec 2023. URL: https://doi.org/10.3390/ma16247586, doi:10.3390/ma16247586. This article has 8 citations.

10. (bayoumy2023effectiveplatformheating pages 6-8): Dina Bayoumy, Torben Boll, Amal Shaji Karapuzha, Xinhua Wu, Yuman Zhu, and Aijun Huang. Effective platform heating for laser powder bed fusion of an al-mn-sc-based alloy. Materials, Dec 2023. URL: https://doi.org/10.3390/ma16247586, doi:10.3390/ma16247586. This article has 8 citations.

11. (mair2021laserpowderbed pages 8-9): Philipp Mair, Valerie Sue Goettgens, Tobias Rainer, Nikolaus Weinberger, Ilse Letofsky-Papst, Stefan Mitsche, and Gerhard Leichtfried. Laser powder bed fusion of nano-cab6 decorated 2024 aluminum alloy. Journal of Alloys and Compounds, 863:158714, May 2021. URL: https://doi.org/10.1016/j.jallcom.2021.158714, doi:10.1016/j.jallcom.2021.158714. This article has 134 citations and is from a peer-reviewed journal.

12. (stopyra2020laserpowderbed pages 31-35): Wojciech Stopyra, Konrad Gruber, Irina Smolina, Tomasz Kurzynowski, and Bogumiła Kuźnicka. Laser powder bed fusion of aa7075 alloy: influence of process parameters on porosity and hot cracking. Additive manufacturing, 35:101270, Oct 2020. URL: https://doi.org/10.1016/j.addma.2020.101270, doi:10.1016/j.addma.2020.101270. This article has 303 citations and is from a highest quality peer-reviewed journal.

13. (bayoumy2023effectiveplatformheating media cf1c659b): Dina Bayoumy, Torben Boll, Amal Shaji Karapuzha, Xinhua Wu, Yuman Zhu, and Aijun Huang. Effective platform heating for laser powder bed fusion of an al-mn-sc-based alloy. Materials, Dec 2023. URL: https://doi.org/10.3390/ma16247586, doi:10.3390/ma16247586. This article has 8 citations.

14. (yadav2022microstructuralandmechanical pages 30-33): Pinku Yadav, Olivier Rigo, Corinne Arvieu, and Eric Lacoste. Microstructural and mechanical aspects of alsi7mg0.6 alloy related to scanning strategies in l-pbf. The International Journal of Advanced Manufacturing Technology, 120:6205-6223, Apr 2022. URL: https://doi.org/10.1007/s00170-022-09127-x, doi:10.1007/s00170-022-09127-x. This article has 19 citations.

15. (marola2021residualstressesin pages 1-2): Silvia Marola, Silvia Bosia, Alessandro Veltro, Gianluca Fiore, Diego Manfredi, Mariangela Lombardi, Giampiero Amato, Marcello Baricco, and Livio Battezzati. Residual stresses in additively manufactured alsi10mg: raman spectroscopy and x-ray diffraction analysis. Materials & Design, 202:109550, Apr 2021. URL: https://doi.org/10.1016/j.matdes.2021.109550, doi:10.1016/j.matdes.2021.109550. This article has 94 citations and is from a highest quality peer-reviewed journal.


---

## Query 6

**Question:** What progress has been made using CALPHAD and computational thermodynamics to design new aluminum alloys specifically for additive manufacturing? Provide examples of alloy compositions predicted and validated, including Thermo-Calc Scheil solidification modeling for printability screening.

**Task ID:** `9f10f7a4-0433-41a1-90d4-3bab214ed1d1`

**Status:** complete

## Progress in CALPHAD/computational-thermodynamics design of Al alloys for AM

Computational thermodynamics (CALPHAD) has progressed from being used primarily to rationalize why legacy high-strength Al alloys crack in laser powder bed fusion (LPBF) to being used as a front-end alloy *design* and *screening* method. Recent workflows combine (i) equilibrium and non-equilibrium (Scheil–Gulliver) solidification calculations in Thermo-Calc, (ii) derived “printability indices” from Scheil outputs (freezing range, Clyne–Davies CSC, hot-susceptibility products, and Kou-type derivatives of T–√fs), and (iii) rapid experimental validation via laser scanning and/or LPBF printing to close the loop. (uba2025enhancingtheprintability pages 4-5, sargent2021integrationofprocessing pages 4-5, taherimousavi2024additivelymanufacturablehighstrength pages 9-12)

### 1) Closed-loop ICME/CALPHAD alloy design validated in LPBF

A representative early, composition-specific demonstration is the ICME “closed-loop” design of an LPBF alloy Al–1.5Cu–0.8Sc–0.4Zr (wt%). CALPHAD was used to finalize the composition and predict solidification behavior and properties; LPBF experiments produced crack-free regions with fine equiaxed grains consistent with CALPHAD guidance, and the measured yield strength (~349 ± 8 MPa) was reported to agree with the prediction by >90%. (thapliyal2020anintegratedcomputational pages 1-2)

This line of work also framed the broader strategy—Sc/Zr-based L12 trialuminides (Al3(Sc,Zr)) used as grain refiners/heterogeneous nucleation sites to reduce hot cracking in otherwise crack-susceptible Al alloys—as a computationally guided path to expand the printable Al alloy palette beyond Al–Si cast alloys. (thapliyal2020anintegratedcomputational pages 1-2)

### 2) Thermo-Calc classic Scheil modeling for *printability screening* of modified 7xxx compositions

A more explicit Thermo-Calc Scheil *printability screening* example is the CALPHAD-guided redesign of Al 7075 (a canonical crack-prone 7xxx alloy) by adding grain refiners (V, Ti) and a eutectic-enhancing element (Mg) in small amounts (≤4 wt.% total additions). The study defined seven candidate compositions (all based on Al 7075) and used Thermo-Calc 2024a with TCAL8/MOBAL7 to run classic Scheil simulations and compute solidification indices from the T–fS curves. (uba2025enhancingtheprintability pages 4-5, uba2025enhancingtheprintability pages 5-7)

**Predicted and experimentally tested compositions (wt% additions to Al 7075):**

- Composition 1: Al 7075 (baseline)
- Composition 2: +1 V
- Composition 3: +1 V +1 Mg
- Composition 4: +1 V +2 Mg
- Composition 5: +1 V +1 Ti
- Composition 6: +1 V +1 Ti +1 Mg
- Composition 7: +1 V +1 Ti +2 Mg (uba2025enhancingtheprintability pages 5-7)

**Scheil-derived printability logic:** (i) early solidification should form dispersoids (here Al3V and/or Al3Ti) to promote heterogeneous nucleation and equiaxed grains, and (ii) terminal solidification should be dominated by a favorable eutectic (here Al2Mg3Zn3 “T phase”) to improve interdendritic feeding and reduce cracking in the final vulnerable solid-fraction range. These concepts were quantified using indices such as freezing range and cracking susceptibility metrics (CSC/HSI/TCR) derived from the Scheil T–fS curves. (uba2025enhancingtheprintability pages 7-10, uba2025enhancingtheprintability pages 10-11)

**Validation:** LPBF-processed samples showed significant cracks and pores for baseline Al 7075, while alloyed compositions (2–7) showed reduced crack density and microstructural refinement; increasing Mg further suppressed cracks, consistent with the predicted eutectic-feeding improvement at the end of solidification. (uba2025enhancingtheprintability pages 11-15)

**Scheil evidence (visual):** Table 3 and Figures 1–4 in this work explicitly show the Thermo-Calc Scheil-derived T–fS curves and summarized solidification indices used for screening. (uba2025enhancingtheprintability media b8ecfc98, uba2025enhancingtheprintability media 6eff7ff4, uba2025enhancingtheprintability media 817bc71d, uba2025enhancingtheprintability media 8269e8d0, uba2025enhancingtheprintability media 19dec755)

### 3) High-throughput Scheil-based screening coupled to ML/inverse design, then validated by rapid experiments and LPBF

A more recent direction is high-throughput exploration of multicomponent, non-traditional Al alloy spaces in which Thermo-Calc equilibrium and Scheil solidification outputs are used both for microstructure selection and *quantitative printability constraints*. In a hybrid ML/CALPHAD workflow in an Al–Ni–Zr–Er–Y–Yb design space, the authors used high-throughput Scheil simulations to compute freezing range (FR), Clyne–Davies CSC, and a combined hot-cracking susceptibility product HCS = FR × CSC, and reported that the HCS product in the constrained design region was very low (<0.05) compared with Al 7075 (reported as 1.13). (taherimousavi2024additivelymanufacturablehighstrength pages 4-7, taherimousavi2024additivelymanufacturablehighstrength pages 9-12)

**Example predicted/validated composition pathway:** The design was reduced to a Zr/Er-dominated space with additional Ni optimization to promote a metastable ternary phase during solidification (reported as Al23Ni6M4), while avoiding excessive eutectic Al3Ni. A laser-scanning workflow on nine compositions around the optimum validated “no hot cracks” (contrasted with Al 7075 showing clear hot cracking), and then a custom powder was produced for LPBF. (taherimousavi2024additivelymanufacturablehighstrength pages 9-12)

**Printed alloy composition (wt%):** Al–2.73Ni–3.19Zr–2.33Er (wt%) was selected for powder production and LPBF printing; printed cubes were verified crack-free, with equiaxed grains by EBSD. Microstructural characterization (SEM/STEM/APT) supported the predicted phase concepts (primary Al3Ni and Al3Zr plus Al3(Er,Zr) L12 nanoprecipitates and a ternary phase consistent with the predicted metastable reservoir concept). (taherimousavi2024additivelymanufacturablehighstrength pages 9-12, taherimousavi2024additivelymanufacturablehighstrength pages 12-15)

### 4) Process-coupled Thermo-Calc Scheil/DICTRA cracking metrics for screening (Al–Cu exemplar)

Beyond individual alloy discoveries, CALPHAD is increasingly embedded into *process-aware* ICME frameworks that couple LPBF thermal histories to solidification models. One approach uses Thermo-Calc (Scheil–Gulliver and DICTRA) to obtain T–√fs curves and compute Kou-style solidification cracking susceptibility as max(dT/d√fs). In Al–Cu, DICTRA was used to model how increasing cooling rate depresses solidus temperature (approaching the Scheil limit) and to compute cracking susceptibility trends that were compared against experimental cracking susceptibility data from the literature. (sargent2021integrationofprocessing pages 4-5, sargent2021integrationofprocessing pages 5-7)

## Examples and validation summary

| Study (year) | AM process | Computational tools | Printability screening metrics | Predicted/selected alloy compositions | Experimental validation outcome |
|---|---|---|---|---|---|
| Thapliyal et al. (2020) | LPBF | CALPHAD-based ICME workflow for composition finalization and prediction of solidification behavior/mechanical properties | Not reported in the retrieved excerpt as explicit Scheil cracking indices; design intent was crack reduction via Sc/Zr grain refiners and CALPHAD-guided solidification control | Al–1.5Cu–0.8Sc–0.4Zr (wt%) (thapliyal2020anintegratedcomputational pages 1-2) | Printed alloy showed crack-free regions with fine equiaxed grains consistent with CALPHAD predictions; measured yield strength ~349 ± 8 MPa, reported to be >90% agreement with prediction (thapliyal2020anintegratedcomputational pages 1-2) |
| Sargent et al. (2021) | LPBF-focused process/microstructure modeling; Al-Cu used for validation | Thermo-Calc TC-Python automation of Scheil-Gulliver, equilibrium, and DICTRA; coupled to a semi-analytical LPBF thermal model | Kou solidification cracking susceptibility metric, max(dT/d√fs); compared equilibrium vs Scheil vs DICTRA solidus/liquidus and cooling-rate effects on SCS (sargent2021integrationofprocessing pages 4-5, sargent2021integrationofprocessing pages 5-7, sargent2021integrationofprocessing pages 2-4, sargent2021integrationofprocessing pages 1-2) | Al-Cu composition space (specific wt% not given in retrieved excerpts) (sargent2021integrationofprocessing pages 2-4, sargent2021integrationofprocessing pages 1-2) | Model trends in SCS for Al-Cu were compared with experimental cracking data from literature; demonstrated that Thermo-Calc Scheil/DICTRA can rank cracking susceptibility versus cooling rate/composition, but this paper is more a validated screening framework than a report of a single new alloy composition (sargent2021integrationofprocessing pages 4-5, sargent2021integrationofprocessing pages 5-7) |
| Taheri-Mousavi et al. (2024) | Rapid laser-scanning validation followed by LPBF/3D printing of custom powder | Thermo-Calc equilibrium + high-throughput Scheil simulations; ICME + ML/NN surrogate + Bayesian optimization | Freezing range (FR), Clyne-Davies CSC, HCS = FR × CSC; Scheil used to optimize metastable ternary phase formation and constrain eutectic/printability; HCS reported <0.05 in screened design space vs 1.13 for Al 7075 (taherimousavi2024additivelymanufacturablehighstrength pages 4-7, taherimousavi2024additivelymanufacturablehighstrength pages 9-12) | Search space: Al-Ni-Zr-Er-Y-Yb with Ni 0–4 at.%, Zr/Er 0.005–2 at.%, Y/Yb 0.005–1 at.% (taherimousavi2024additivelymanufacturablehighstrength pages 4-7); validated optimum neighborhood included sample with Ni = 1.33 at.% and Zr = 1 at.% at Er = 0.4 at.% (taherimousavi2024additivelymanufacturablehighstrength pages 9-12); printed custom-powder alloy: Al-2.73Ni-3.19Zr-2.33Er (wt%) (taherimousavi2024additivelymanufacturablehighstrength pages 9-12, taherimousavi2024additivelymanufacturablehighstrength pages 12-15) | No hot cracks observed in 9 laser-scanned compositions around the optimum; LPBF samples from custom powder were verified crack-free with non-textured equiaxed grains; aged hardness exceeded Al 7075 and was ~50% above benchmark printable alloy; STEM/APT confirmed predicted Al3Ni, Al3Zr, Al23Ni6M4-like ternary reservoir, and Al3(Er,Zr) L12 nanoprecipitates (taherimousavi2024additivelymanufacturablehighstrength pages 9-12, taherimousavi2024additivelymanufacturablehighstrength pages 12-15, taherimousavi2024additivelymanufacturablehighstrength pages 25-28) |
| Uba et al. (2025) | LPBF | Thermo-Calc 2024a with TCAL8 and MOBAL7; classic Scheil solidification simulations generating T-fS and T-fS^0.5 curves | Freezing range, HSI, TCR, CSC (Clyne-Davies-based), plus T-fS/T-fS^0.5 screening for early dispersoid formation and terminal eutectic feeding; Table 3/Figs. 1–4 visualize these indices and curves (uba2025enhancingtheprintability pages 4-5, uba2025enhancingtheprintability pages 7-10, uba2025enhancingtheprintability pages 10-11, uba2025enhancingtheprintability media b8ecfc98) | Seven Al-7075-based LPBF candidate compositions (wt% additions): 1 = baseline Al 7075; 2 = +1 V; 3 = +1 V +1 Mg; 4 = +1 V +2 Mg; 5 = +1 V +1 Ti; 6 = +1 V +1 Ti +1 Mg; 7 = +1 V +1 Ti +2 Mg (uba2025enhancingtheprintability pages 5-7) | SEM showed strong crack/porosity reduction vs baseline Al 7075, especially for Mg-containing variants; compositions 2–7 exhibited finer, more equiaxed grains consistent with predicted Al3V/Al3Ti dispersoid formation and improved terminal Al2Mg3Zn3 eutectic feeding; experiments confirmed CALPHAD-guided trends despite limited laser power/process optimization (uba2025enhancingtheprintability pages 10-11, uba2025enhancingtheprintability pages 11-15, uba2025enhancingtheprintability pages 5-7) |


*Table: This table summarizes key examples where CALPHAD and Thermo-Calc-based computational thermodynamics were used to design or screen aluminum alloys for additive manufacturing. It highlights the progression from framework development to experimentally validated crack-resistant LPBF alloys, including explicit Scheil-based printability metrics and compositions.*

## Key takeaways (what “progress” looks like now)

1. **Scheil Thermo-Calc outputs are now routinely converted into AM-specific screening metrics** (freezing range, CSC/HSI/TCR, HCS products, and Kou-type derivatives), enabling down-selection before powder/printing trials. (uba2025enhancingtheprintability pages 4-5, uba2025enhancingtheprintability pages 7-10, sargent2021integrationofprocessing pages 4-5, taherimousavi2024additivelymanufacturablehighstrength pages 9-12)
2. **Validated composition design has moved beyond “just add Si”** to targeted strategies that explicitly manipulate the early/late stages of solidification: dispersoid-first (grain refiners such as V/Ti or Sc/Zr-based L12 trialuminides) plus terminal eutectic feeding enhancers (e.g., Mg effects on Al2Mg3Zn3 eutectic behavior in modified 7075). (uba2025enhancingtheprintability pages 10-11, uba2025enhancingtheprintability pages 11-15)
3. **High-throughput, multi-objective exploration (including ML + CALPHAD) is enabling non-traditional printable Al chemistries** (e.g., Al–Ni–Zr–Er) validated via rapid laser scanning and then LPBF, with microstructural confirmation of CALPHAD-predicted phase concepts. (taherimousavi2024additivelymanufacturablehighstrength pages 4-7, taherimousavi2024additivelymanufacturablehighstrength pages 9-12, taherimousavi2024additivelymanufacturablehighstrength pages 12-15)
4. **Remaining limitations** highlighted in the retrieved sources include the need to handle AM’s extreme kinetics (cooling-rate dependence, remelting/thermal cycling) and database/mobility completeness, motivating DICTRA coupling and continued experimental closure. (mehta2023developmentofhigh pages 39-43, sargent2021integrationofprocessing pages 2-4, sargent2021integrationofprocessing pages 4-5)


References

1. (uba2025enhancingtheprintability pages 4-5): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

2. (sargent2021integrationofprocessing pages 4-5): Noah Sargent, Mason Jones, Richard Otis, Andrew A. Shapiro, Jean-Pierre Delplanque, and Wei Xiong. Integration of processing and microstructure models for non-equilibrium solidification in additive manufacturing. Metals, 11:570, Apr 2021. URL: https://doi.org/10.3390/met11040570, doi:10.3390/met11040570. This article has 43 citations.

3. (taherimousavi2024additivelymanufacturablehighstrength pages 9-12): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

4. (thapliyal2020anintegratedcomputational pages 1-2): Saket Thapliyal, Mageshwari Komarasamy, Shivakant Shukla, Le Zhou, Holden Hyer, Sharon Park, Yongho Sohn, and Rajiv S. Mishra. An integrated computational materials engineering-anchored closed-loop method for design of aluminum alloys for additive manufacturing. Materialia, 9:100574, Mar 2020. URL: https://doi.org/10.1016/j.mtla.2019.100574, doi:10.1016/j.mtla.2019.100574. This article has 85 citations and is from a peer-reviewed journal.

5. (uba2025enhancingtheprintability pages 5-7): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

6. (uba2025enhancingtheprintability pages 7-10): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

7. (uba2025enhancingtheprintability pages 10-11): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

8. (uba2025enhancingtheprintability pages 11-15): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

9. (uba2025enhancingtheprintability media b8ecfc98): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

10. (uba2025enhancingtheprintability media 6eff7ff4): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

11. (uba2025enhancingtheprintability media 817bc71d): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

12. (uba2025enhancingtheprintability media 8269e8d0): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

13. (uba2025enhancingtheprintability media 19dec755): Chukwudalu Uchenna Uba, Huan Ding, Yehong Chen, Shengmin Guo, and Jonathan Richard Raush. Enhancing the printability of laser powder bed fusion-processed aluminum 7xxx series alloys using grain refinement and eutectic solidification strategies. Materials, 18:5089, Nov 2025. URL: https://doi.org/10.3390/ma18225089, doi:10.3390/ma18225089. This article has 2 citations.

14. (taherimousavi2024additivelymanufacturablehighstrength pages 4-7): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

15. (taherimousavi2024additivelymanufacturablehighstrength pages 12-15): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

16. (sargent2021integrationofprocessing pages 5-7): Noah Sargent, Mason Jones, Richard Otis, Andrew A. Shapiro, Jean-Pierre Delplanque, and Wei Xiong. Integration of processing and microstructure models for non-equilibrium solidification in additive manufacturing. Metals, 11:570, Apr 2021. URL: https://doi.org/10.3390/met11040570, doi:10.3390/met11040570. This article has 43 citations.

17. (sargent2021integrationofprocessing pages 2-4): Noah Sargent, Mason Jones, Richard Otis, Andrew A. Shapiro, Jean-Pierre Delplanque, and Wei Xiong. Integration of processing and microstructure models for non-equilibrium solidification in additive manufacturing. Metals, 11:570, Apr 2021. URL: https://doi.org/10.3390/met11040570, doi:10.3390/met11040570. This article has 43 citations.

18. (sargent2021integrationofprocessing pages 1-2): Noah Sargent, Mason Jones, Richard Otis, Andrew A. Shapiro, Jean-Pierre Delplanque, and Wei Xiong. Integration of processing and microstructure models for non-equilibrium solidification in additive manufacturing. Metals, 11:570, Apr 2021. URL: https://doi.org/10.3390/met11040570, doi:10.3390/met11040570. This article has 43 citations.

19. (taherimousavi2024additivelymanufacturablehighstrength pages 25-28): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

20. (mehta2023developmentofhigh pages 39-43): B Mehta. Development of high performance aluminium alloys tailored for powder bed fusion-laser beam. Unknown journal, 2023.


---

## Query 7

**Question:** What machine learning and high-throughput experimental approaches have been applied to discover or optimize aluminum alloys for additive manufacturing? Provide specific examples of ML-predicted compositions, Bayesian optimization campaigns, and their measured property outcomes.

**Task ID:** `6fab6174-500c-4ab0-bfaf-2e41e8e3e9d9`

**Status:** complete

## Machine-learning and high-throughput experimental approaches for Al-alloy discovery/optimization in additive manufacturing

### 1) ML-guided composition discovery and optimization (including Bayesian optimization)

**Hybrid ML/ICME inverse design + Bayesian optimization (composition → crack-free LPBF + high strength).** A hybrid workflow combining high-throughput CALPHAD/Scheil simulations with machine-learning surrogates and inverse design was applied to design precipitation-strengthened Al–(Ni,Zr,Er,…) alloys for laser powder bed fusion (LPBF). The study reports a selected alloy for powder atomization/LPBF of **Al-2.73Ni-3.19Zr-2.33Er (wt%)**, and also reports closely related “ML-optimized” and measured compositions (**Al-2.47Ni-3.25Zr-2.38Er** and XRF-measured printed **Al-2.55Ni-2.9Zr-2.37Er**). (taherimousavi2024additivelymanufacturablehighstrength pages 9-12, taherimousavi2024additivelymanufacturablehighstrength pages 22-25)

Printability outcome: the same work reports that LPBF parts were **verified crack-free** and that **no hot cracks were observed** in laser-scanned trials (reported for 9 samples). (taherimousavi2024additivelymanufacturablehighstrength pages 9-12, taherimousavi2024additivelymanufacturablehighstrength pages 12-15)

Measured property outcomes: the LPBF-built alloy had **as-built hardness ~180 HV** (comparable to wrought Al 7075) and achieved a **peak hardness after ~8–10 h aging at 400 °C** that was stated to be **~50% higher than a benchmark printable Al alloy** and higher than wrought 7075 across aging times. (taherimousavi2024additivelymanufacturablehighstrength pages 12-15)

The same paper reports room-temperature tensile testing and states that the designed alloy’s **yield strength was ~50% higher than Gong et al.’s benchmark printable alloy** (“alloy 1”, composition **Al-2.14Ni-1.15Zr-1.35Er-0.25Y-0.73Yb, wt%**), but the retrieved text did not include absolute MPa values for YS/UTS/elongation. (taherimousavi2024additivelymanufacturablehighstrength pages 12-15)

**Active-learning framework for Al–Si(-Mg-Cu) composition optimization with experimental validation.** A process-synergistic framework uses latent-space sampling and surrogate modeling, with **Bayesian optimization used to tune surrogate-model hyperparameters**, and performs iterative experimental validation of the top-ranked candidates. (cai2025aprocesssynergisticactive pages 8-9)

Specific validated compositions (wt%) and measured outcomes from Table 1 include:
- **C2: Al 89.3 / Si 6.7 / Mg 0.4 / Cu 3.2 → UTS 459.8 MPa**
- **C3: Al 88.5 / Si 7.4 / Mg 0.4 / Cu 3.4 → UTS 454.6 MPa**
- **C1: Al 90.3 / Si 6.2 / Mg 0.3 / Cu 2.9 → UTS 436.6 MPa** (cai2025aprocesssynergisticactive pages 6-7, cai2025aprocesssynergisticactive pages 4-6)

Lower-strength examples for a different processing route (GC+HE) include:
- **D1: Al 87.1 / Si 12.3 / Mg 0.6 → UTS 208.5 MPa**
- **D2: Al 87.7 / Si 11.6 / Mg 0.6 → UTS 220.5 MPa** (cai2025aprocesssynergisticactive pages 6-7)

### 2) ML-guided LPBF process-parameter optimization for Al alloys (high-throughput mapping of process windows)

**Gaussian-process-regression surrogate to map power/speed → density and properties (AlSi10Mg).** A Gaussian process regression (GPR) surrogate was trained on an LPBF dataset to identify an expanded **optimized processing window** for fully dense AlSi10Mg parts (≥99% relative density). (liu2020machinelearningassistedlaser pages 1-5)

A set of validation parameter points within the learned window included:
- **264 W / 2320 mm·s⁻¹**, **300 W / 1960 mm·s⁻¹**, **355 W / 1690 mm·s⁻¹**, **200 W / 1307 mm·s⁻¹**, **355 W / 2320 mm·s⁻¹**. (liu2020machinelearningassistedlaser pages 14-19)

Measured outcomes reported include:
- **Relative density 99.2–99.4%** (validated within <0.3% error versus GPR predictions) (liu2020machinelearningassistedlaser pages 14-19, liu2020machinelearningassistedlaser pages 9-14)
- **Hardness 118–137 HV10**, **UTS 297–389 MPa**, **elongation 6.3–10.3%**, and **fracture toughness 9.9–12.7 kJ·m⁻²**. (liu2020machinelearningassistedlaser pages 1-5)

### 3) High-throughput experimental/combinatorial approaches for Al-alloy discovery for AM

**High-throughput LPBF compositionally graded alloy (CGA) builds.** High-throughput LPBF was used to fabricate **continuous Mn–Mg composition gradients** to rapidly screen microstructure transitions; increasing Mn promoted a **columnar-to-equiaxed grain transition** and reduced the incubation time for Al nucleation. From the gradient screening, a specific composition **Al-3.8Mn-2.8Mg** was designed and reported to deliver a **strength–ductility trade-off** (no absolute tensile numbers were present in the retrieved snippet). (liu2024high‐throughputpreparationfor pages 5-5)

**High-throughput composition gradients to map crack-mitigation trade-offs (Zr in Al).** A gradient approach for Zr additions (reported range **0.6–2 wt% Zr**) is described: **2 wt% Zr** provided the **largest processing window and highest UTS** but reduced ductility due to brittle Al3Zr formation, while **0.6 wt% Zr** improved ductility but did not sufficiently refine grains. (liu2024high‐throughputpreparationfor pages 3-4)

**Combinatorial DED/LENS compositional grading (AM as a screening tool).** Directed-energy deposition (DED) / LENS-style systems have been used to produce compositionally graded libraries for rapid screening of Al-containing alloy series (primarily complex concentrated alloys). Examples include **AlxCrCuFeNi** (hardness generally increased with Al content) and **AlxCoCrFeNi** (phase stability mapped vs composition). (pegues2021exploringadditivemanufacturing pages 1-5)

**HT-READ: AM-enabled high-throughput discrete sample libraries with automated characterization.** A closed-loop platform prints a **16-sample “library ring”** (via DED) designed for rapid/automated characterization (XRD, SEM-EDS, EBSD) and hardness mapping, with ML linking composition to hardness; while demonstrated on Ni alloys, it provides a concrete AM-compatible experimental architecture for rapid alloy screening that is directly transferable to Al-alloy campaigns. (vecchio2021highthroughputrapidexperimental pages 1-4, vecchio2021highthroughputrapidexperimental pages 11-13)

### Summary table

| Study | AM process | Approach type | ML/HTE details | Specific predicted/validated composition or process parameters | Measured outcomes |
|---|---|---|---|---|---|
| Taheri-Mousavi et al. 2024 | LPBF | Hybrid ML/ICME inverse design with Bayesian optimization | High-throughput CALPHAD/Scheil screening over Al-Er-Zr-Y-Yb-Ni space; NN regressor for coarsening metric; BO with GP surrogate and EI acquisition; printability constrained by FR, CSC, HCS | Selected powder composition reported as Al-2.73Ni-3.19Zr-2.33Er (wt%); related ML-optimized composition Al-2.47Ni-3.25Zr-2.38Er; XRF of printed material Al-2.55Ni-2.9Zr-2.37Er; LPBF examples used 350 W, 1100 mm/s, 120 µm hatch, 50 µm layers, 200 °C preheat | No hot cracks observed in 9 laser-scanned samples; LPBF cubes verified crack-free; as-built hardness 180 HV; peak hardness after 8–10 h at 400 °C was ~50% higher than benchmark printable alloy and above wrought 7075; tensile tests showed ~50% higher yield strength than benchmark alloy 1, but no absolute YS/UTS/elongation values were given in the retrieved text (taherimousavi2024additivelymanufacturablehighstrength pages 9-12, taherimousavi2024additivelymanufacturablehighstrength pages 22-25, taherimousavi2024additivelymanufacturablehighstrength pages 12-15, taherimousavi2024additivelymanufacturablehighstrength pages 15-18) |
| Cai et al. 2025 | Not AM-specific in retrieved evidence; process-aware alloy-design framework for Al-Si alloys | Process-synergistic active learning with Bayesian-optimized surrogates | c-WAE latent space + GMM/MCMC sampling; NN and XGBDT surrogate ensemble; Bayesian optimization used to tune surrogate hyperparameters; iterative experimental validation across processing routes | High-strength validated candidates included C1 = Al 90.3 / Si 6.2 / Mg 0.3 / Cu 2.9 (wt%), C2 = Al 89.3 / Si 6.7 / Mg 0.4 / Cu 3.2, C3 = Al 88.5 / Si 7.4 / Mg 0.4 / Cu 3.4; GC+HE examples D1 = Al 87.1 / Si 12.3 / Mg 0.6, D2 = Al 87.7 / Si 11.6 / Mg 0.6 | UTS: C1 436.6 MPa, C2 459.8 MPa, C3 454.6 MPa; D1 208.5 MPa, D2 220.5 MPa; C-series exceeded literature maximum of 425 MPa and prior experimental result of 405 MPa; D-series exceeded literature maximum of 198 MPa and prior experimental result of 191.8 MPa (cai2025aprocesssynergisticactive pages 6-7, cai2025aprocesssynergisticactive pages 4-6, cai2025aprocesssynergisticactive pages 8-9, cai2025aprocesssynergisticactive pages 7-8) |
| Liu et al. 2020 (Acta Mater.) | LPBF of AlSi10Mg | GPR surrogate for process optimization | Gaussian process regression mapped laser power and scan speed to relative density; optimized processing window targeted fully dense parts (≥99% density); validated with five independent parameter sets | Validation sets included 264 W / 2320 mm/s, 300 W / 1960 mm/s, 355 W / 1690 mm/s, 200 W / 1307 mm/s, and 355 W / 2320 mm/s | Relative density 99.2–99.4%; hardness 118–137 HV10; UTS 297–389 MPa; elongation 6.3–10.3%; fracture toughness 9.9–12.7 kJ/m2; measured densities agreed with GPR predictions within <0.3% error (liu2020machinelearningassistedlaser pages 1-5, liu2020machinelearningassistedlaser pages 14-19, liu2020machinelearningassistedlaser pages 9-14, liu2020machinelearningassistedlaser pages 5-9) |
| Liu et al. 2024 HT review (summarizing Sun et al.) | High-throughput LPBF compositionally graded alloy screening | High-throughput experimental composition-gradient screening | Continuous Mn–Mg gradient builds used to rapidly map composition–microstructure–property relations in Al alloys | Gradient screening led to Al-3.8Mn-2.8Mg | Increasing Mn reduced Al nucleation incubation time and promoted columnar-to-equiaxed grain transition; designed Al-3.8Mn-2.8Mg achieved a reported strength–ductility trade-off, but no numeric tensile values were given in the retrieved snippet (liu2024high‐throughputpreparationfor pages 5-5) |
| Liu et al. 2024 HT review | High-throughput AM gradient study | High-throughput composition/process screening | Zr-content gradient used to probe grain refinement, processing window, and strength–ductility trade-offs in Al alloys | Zr varied from 0.6 to 2 wt% | 2 wt% Zr gave the largest processing window and highest UTS but reduced ductility because of brittle Al3Zr; 0.6 wt% improved ductility but gave insufficient grain refinement; overall HT screening identified fine equiaxed grains with favorable strength–toughness balance, but no numeric tensile values were given in the retrieved snippet (liu2024high‐throughputpreparationfor pages 3-4) |
| Pegues et al. 2021 | LB-DED / LENS-style compositional grading | Combinatorial AM high-throughput screening | Single-build compositional grading and blended-powder screening to map phase selection and hardness trends in Al-containing alloy series | AlxCrCuFeNi; AlxCoCrFeNi; AlCrFeMoVx | For AlxCrCuFeNi, hardness generally increased with Al content while microstructure, hardness, and magnetic properties were screened; for AlxCoCrFeNi, phase stability (FCC/BCC/B2) was mapped versus composition; for AlCrFeMoVx, hardness increased with V content while retaining single-phase BCC (pegues2021exploringadditivemanufacturing pages 1-5) |
| Vecchio et al. 2021 | DED-based library fabrication platform | HT-READ closed-loop high-throughput experimentation | 3D-printed 16-sample library ring designed for automated XRD, SEM-EDS, EBSD, and hardness screening; ML (Automatminer/gradient boosting) linked composition to Vickers hardness | Methodology paper demonstrated on alloyed Inconel 625, not an Al alloy in the retrieved evidence | Key outcome is the high-throughput method itself: automated analysis of all 16 samples in <1 h for SEM/EDS/EBSD, plus integrated hardness mapping and ML-guided property prediction; useful as an AM-compatible platform for rapid Al-alloy screening, but no Al-specific property data were provided in the retrieved snippets (vecchio2021highthroughputrapidexperimental pages 1-4, vecchio2021highthroughputrapidexperimental pages 11-13) |


*Table: This table summarizes the aluminum-alloy additive-manufacturing studies and AM-compatible high-throughput methods supported by the retrieved evidence. It highlights the design strategy, concrete compositions or parameter sets, and the experimentally reported outcomes most relevant to discovery or optimization.*

### Evidence limitations (important for interpretation)

1. For the ML-designed LPBF Al–Ni–Zr–Er alloy, the retrieved text contains explicit **compositions**, **crack-free printability evidence**, and **hardness outcomes**, but does **not** provide absolute tensile numbers (YS/UTS/elongation); it only reports yield strength as a relative improvement versus a benchmark printable alloy. (taherimousavi2024additivelymanufacturablehighstrength pages 12-15, taherimousavi2024additivelymanufacturablehighstrength pages 9-12)
2. Some high-throughput composition-gradient examples (e.g., Al-3.8Mn-2.8Mg; Zr gradients) are summarized in a review, and the retrieved snippets did not include the underlying numeric tensile property values. (liu2024high‐throughputpreparationfor pages 5-5, liu2024high‐throughputpreparationfor pages 3-4)

References

1. (taherimousavi2024additivelymanufacturablehighstrength pages 9-12): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

2. (taherimousavi2024additivelymanufacturablehighstrength pages 22-25): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

3. (taherimousavi2024additivelymanufacturablehighstrength pages 12-15): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

4. (cai2025aprocesssynergisticactive pages 8-9): Jianming Cai, Mengxia Han, Xirui Yan, Yan Chen, Daoxiu Li, Kai Zhao, Dongqing Zhang, Kaiqi Hu, Heng Han Sua, Hieng Kiat Jun, Kewei Xie, Guiliang Liu, Xiangfa Liu, and Sida Liu. A process-synergistic active learning framework for high-strength al-si alloys design. npj Computational Materials, Jul 2025. URL: https://doi.org/10.1038/s41524-025-01721-3, doi:10.1038/s41524-025-01721-3. This article has 5 citations and is from a peer-reviewed journal.

5. (cai2025aprocesssynergisticactive pages 6-7): Jianming Cai, Mengxia Han, Xirui Yan, Yan Chen, Daoxiu Li, Kai Zhao, Dongqing Zhang, Kaiqi Hu, Heng Han Sua, Hieng Kiat Jun, Kewei Xie, Guiliang Liu, Xiangfa Liu, and Sida Liu. A process-synergistic active learning framework for high-strength al-si alloys design. npj Computational Materials, Jul 2025. URL: https://doi.org/10.1038/s41524-025-01721-3, doi:10.1038/s41524-025-01721-3. This article has 5 citations and is from a peer-reviewed journal.

6. (cai2025aprocesssynergisticactive pages 4-6): Jianming Cai, Mengxia Han, Xirui Yan, Yan Chen, Daoxiu Li, Kai Zhao, Dongqing Zhang, Kaiqi Hu, Heng Han Sua, Hieng Kiat Jun, Kewei Xie, Guiliang Liu, Xiangfa Liu, and Sida Liu. A process-synergistic active learning framework for high-strength al-si alloys design. npj Computational Materials, Jul 2025. URL: https://doi.org/10.1038/s41524-025-01721-3, doi:10.1038/s41524-025-01721-3. This article has 5 citations and is from a peer-reviewed journal.

7. (liu2020machinelearningassistedlaser pages 1-5): Qian Liu, Hongkun Wu, Moses J. Paul, Peidong He, Zhongxiao Peng, Bernd Gludovatz, Jamie J. Kruzic, Chun H. Wang, and Xiaopeng Li. Machine-learning assisted laser powder bed fusion process optimization for alsi10mg: new microstructure description indices and fracture mechanisms. Acta Materialia, 201:316-328, Dec 2020. URL: https://doi.org/10.1016/j.actamat.2020.10.010, doi:10.1016/j.actamat.2020.10.010. This article has 305 citations and is from a highest quality peer-reviewed journal.

8. (liu2020machinelearningassistedlaser pages 14-19): Qian Liu, Hongkun Wu, Moses J. Paul, Peidong He, Zhongxiao Peng, Bernd Gludovatz, Jamie J. Kruzic, Chun H. Wang, and Xiaopeng Li. Machine-learning assisted laser powder bed fusion process optimization for alsi10mg: new microstructure description indices and fracture mechanisms. Acta Materialia, 201:316-328, Dec 2020. URL: https://doi.org/10.1016/j.actamat.2020.10.010, doi:10.1016/j.actamat.2020.10.010. This article has 305 citations and is from a highest quality peer-reviewed journal.

9. (liu2020machinelearningassistedlaser pages 9-14): Qian Liu, Hongkun Wu, Moses J. Paul, Peidong He, Zhongxiao Peng, Bernd Gludovatz, Jamie J. Kruzic, Chun H. Wang, and Xiaopeng Li. Machine-learning assisted laser powder bed fusion process optimization for alsi10mg: new microstructure description indices and fracture mechanisms. Acta Materialia, 201:316-328, Dec 2020. URL: https://doi.org/10.1016/j.actamat.2020.10.010, doi:10.1016/j.actamat.2020.10.010. This article has 305 citations and is from a highest quality peer-reviewed journal.

10. (liu2024high‐throughputpreparationfor pages 5-5): Min Liu, Chenxu Lei, Yongxiang Wang, Baicheng Zhang, and Xuan-hui Qu. High‐throughput preparation for alloy composition design in additive manufacturing: a comprehensive review. Materials Genome Engineering Advances, Jul 2024. URL: https://doi.org/10.1002/mgea.55, doi:10.1002/mgea.55. This article has 33 citations.

11. (liu2024high‐throughputpreparationfor pages 3-4): Min Liu, Chenxu Lei, Yongxiang Wang, Baicheng Zhang, and Xuan-hui Qu. High‐throughput preparation for alloy composition design in additive manufacturing: a comprehensive review. Materials Genome Engineering Advances, Jul 2024. URL: https://doi.org/10.1002/mgea.55, doi:10.1002/mgea.55. This article has 33 citations.

12. (pegues2021exploringadditivemanufacturing pages 1-5): Jonathan W. Pegues, Michael A. Melia, Raymond Puckett, Shaun R. Whetten, Nicolas Argibay, and Andrew B. Kustas. Exploring additive manufacturing as a high-throughput screening tool for multiphase high entropy alloys. Additive Manufacturing, 37:101598, Jan 2021. URL: https://doi.org/10.1016/j.addma.2020.101598, doi:10.1016/j.addma.2020.101598. This article has 106 citations and is from a highest quality peer-reviewed journal.

13. (vecchio2021highthroughputrapidexperimental pages 1-4): Kenneth S. Vecchio, Olivia F. Dippo, Kevin R. Kaufmann, and Xiao Liu. High-throughput rapid experimental alloy development (ht-read). Acta Materialia, 221:117352, Dec 2021. URL: https://doi.org/10.1016/j.actamat.2021.117352, doi:10.1016/j.actamat.2021.117352. This article has 94 citations and is from a highest quality peer-reviewed journal.

14. (vecchio2021highthroughputrapidexperimental pages 11-13): Kenneth S. Vecchio, Olivia F. Dippo, Kevin R. Kaufmann, and Xiao Liu. High-throughput rapid experimental alloy development (ht-read). Acta Materialia, 221:117352, Dec 2021. URL: https://doi.org/10.1016/j.actamat.2021.117352, doi:10.1016/j.actamat.2021.117352. This article has 94 citations and is from a highest quality peer-reviewed journal.

15. (taherimousavi2024additivelymanufacturablehighstrength pages 15-18): S. Mohadeseh Taheri-Mousavi, Michael Xu, Florian Hengsbach, Clay Houser, Zhaoxuan Ge, Benjamin Glaser, Shaolou Wei, Mikro Schaper, James M. LeBeau, Greg B. Olson, and A. John Hart. Additively manufacturable high-strength aluminum alloys with thermally stable microstructures enabled by hybrid machine learning-based design. Preprint, Jan 2024. URL: https://doi.org/10.48550/arxiv.2406.17457, doi:10.48550/arxiv.2406.17457. This article has 10 citations.

16. (cai2025aprocesssynergisticactive pages 7-8): Jianming Cai, Mengxia Han, Xirui Yan, Yan Chen, Daoxiu Li, Kai Zhao, Dongqing Zhang, Kaiqi Hu, Heng Han Sua, Hieng Kiat Jun, Kewei Xie, Guiliang Liu, Xiangfa Liu, and Sida Liu. A process-synergistic active learning framework for high-strength al-si alloys design. npj Computational Materials, Jul 2025. URL: https://doi.org/10.1038/s41524-025-01721-3, doi:10.1038/s41524-025-01721-3. This article has 5 citations and is from a peer-reviewed journal.

17. (liu2020machinelearningassistedlaser pages 5-9): Qian Liu, Hongkun Wu, Moses J. Paul, Peidong He, Zhongxiao Peng, Bernd Gludovatz, Jamie J. Kruzic, Chun H. Wang, and Xiaopeng Li. Machine-learning assisted laser powder bed fusion process optimization for alsi10mg: new microstructure description indices and fracture mechanisms. Acta Materialia, 201:316-328, Dec 2020. URL: https://doi.org/10.1016/j.actamat.2020.10.010, doi:10.1016/j.actamat.2020.10.010. This article has 305 citations and is from a highest quality peer-reviewed journal.


---

## Query 8

**Question:** What powder characteristics (particle size distribution, morphology, flowability, oxygen content) are required for LPBF aluminum alloys? How does powder recycling affect part properties? Provide quantitative data on powder degradation with reuse cycles.

**Task ID:** `e5868438-4f44-4e87-9f3c-63c747a9d61c`

**Status:** complete

## Technical summary
Laser powder bed fusion (LPBF) of aluminum alloys is unusually sensitive to powder quality because Al powders are low density (poorer gravity-driven flow), rapidly oxidize, and can adsorb moisture; these factors directly affect recoating, powder-bed packing density, and melt-pool wetting. Across the retrieved evidence, the “required” powder characteristics are best expressed as quantitative windows for (i) particle-size distribution (PSD), (ii) morphology/sphericity, (iii) flowability/spreadability, and (iv) oxygen/moisture control.

## 1) Powder characteristics required for LPBF Al alloys
### 1.1 Particle size distribution (PSD)
* **Common PSD window used for LPBF Al**: mean/typical particle sizes **15–45 µm** (often quoted for LPBF) and commercial Al LPBF powders commonly **15–50 µm**; a frequently cited target PSD for SLM/LPBF is **15–63 µm**. (trevisan2018studyandcharacterisation pages 63-66, balbaa2021roleofpowder pages 1-4, cordova2019revealingtheeffects pages 7-9)
* **Practical PSD examples (Al-alloy powders intended for LPBF-type use)**: Carrozza reported Al-alloy powder batches with **D10/D50/D90 spanning ~18.7/31.8/53.4 to 30.2/49.3/80.2 µm**, with several batches near ~20–35–56 µm and ~29–48–78 µm. (carrozza2017characterizationofpowders pages 8-12)
* **PSD trade-offs specific to Al**: Fine powders can increase laser absorptivity and reduce the energy needed to melt particles, but they also agglomerate and spread poorly; in AlSi10Mg, fine powder produced a lower powder-bed packing density and lower part density unless laser power was increased. (balbaa2021roleofpowder pages 14-18, balbaa2021roleofpowder pages 1-4)

### 1.2 Morphology / sphericity
* **Preferred morphology**: highly spherical gas- or plasma-atomized powders are typically preferred; irregular particles (e.g., water atomized) reduce packing density and flow. (trevisan2018studyandcharacterisation pages 63-66)
* **Quantitative morphology screening (general AM guidance including Al powders)**: Cordova et al. propose morphology indices fc and fs “as close as possible to 1,” and **at least 0.7** as a minimum; for Ti6Al4V they recommend higher (0.8–0.9). (cordova2019revealingtheeffects pages 7-9)
* **Reuse-related morphology defects**: powder reuse can increase satellites and produce “teardrop”/deformed particles, degrading morphology even if PSD changes are modest. (weiss2022ontheinfluence pages 1-2, cordova2019revealingtheeffects pages 7-9)

### 1.3 Flowability / spreadability
No single flow test is universally accepted for LPBF, but multiple quantitative go/no-go metrics recur:
* **Funnel flow screening**: in one LPBF powder-characterization workflow, powders that flow through a **Hall funnel (2.5 mm orifice)** are treated as having good flow; powders that only pass **Carney (5 mm)** are less certain; non-flowing powders are rejected. (carrozza2017characterizationofpowders pages 8-12)
* **Compressibility-based indices (commonly used for AM powders)**: excellent-flow threshold values are **Carr index (CI) < 10%** and **Hausner ratio (HR) < 1.11**. (cordova2019revealingtheeffects pages 7-9)
* **Example values for Al alloys**:
  * **AlSi10Mg** (virgin → used 6×): **HR 1.09 → 1.11** and **CI 8.4% → 9.9%** (remains near the “excellent-flow” window). (cordova2019revealingtheeffects pages 7-9)
  * **Scalmalloy** (virgin → used 3×): **HR 1.10 → 1.15** and **CI 8.9% → 13.5%** (flowability degrades with reuse). (cordova2019revealingtheeffects pages 7-9)
* **Typical “operational” flow metrics from Al powder batches**: Carrozza reported flow times (50 g) ranging **~11.3–70.6 s/50 g** with angles of repose **~28.26–31.88°**, and some powders that did not flow at all under the funnel tests. (carrozza2017characterizationofpowders pages 8-12)

### 1.4 Oxygen / moisture control (surface chemistry)
* **Oxygen is a key acceptance variable**, but the retrieved sources do not provide a single universal “required oxygen limit” for all LPBF Al alloys; rather, they show that oxygen pickup correlates with poorer wetting and higher lack-of-fusion porosity in AlSi10Mg when powder is aged/handled. (fedina2022influenceofalsi10mg pages 8-10, trevisan2018studyandcharacterisation pages 63-66)
* **Quantitative oxygen baseline and cycle monitoring (AlSi10Mg)**: Weiss et al. report fresh powder oxygen of **850 mg/kg** and track oxygen/hydrogen (mg/kg) versus **0–10 powder-use cycles**, alongside PSD and flow metrics. (weiss2022ontheinfluence pages 5-6, weiss2022ontheinfluence media b4882a71)
* **Moisture/hydrogen effects**: hydrogen porosity is a recognized defect mechanism in Al alloys; drying and storage in inert/dry conditions are recommended to reduce moisture-driven porosity and oxide/hydroxide formation. (martucci2023developmentandcharacterisation pages 42-45, fiegl2021effectofalsi10mg0.4 pages 1-2)

## 2) How powder recycling affects part properties (and quantitative degradation with reuse)
Powder reuse impacts part properties primarily through: (i) PSD drift (often coarsening / fewer fines), (ii) morphology degradation (satellites/spatter), and (iii) oxygen/moisture pickup and oxide/hydroxide chemistry that impairs wetting.

### 2.1 Quantitative powder degradation vs reuse cycles (cycle-resolved dataset)
**AlSi10Mg: 0–10 powder-use cycles**
* Weiss et al. provide a cycle-resolved dataset with **PSD metrics (d10/d50/d90), sphericity (SPHT), flowability metrics (avalanche angle AA, rest angle RA), and chemical analysis (oxygen and hydrogen in mg/kg)** versus powder use cycle **0–10**. (weiss2022ontheinfluence media b4882a71, weiss2022ontheinfluence media 0efdbac3)
* In that dataset, the dependence on reuse cycle was **stronger for flowability** than for PSD, with reported trend-fit coefficients **R²AA = 0.8732** and **R²RA = 0.6469** versus **R²d90 = 0.4902, R²d50 = 0.3985, R²d10 = 0.3331**. (weiss2022ontheinfluence pages 5-6)

These figures provide quantitative “powder degradation with reuse cycles” evidence (oxygen/hydrogen tracking and flow/PSD trending) even where tabulated values per cycle are not explicitly printed in the text excerpt. (weiss2022ontheinfluence media b4882a71, weiss2022ontheinfluence media 0efdbac3)

### 2.2 Quantitative links to part density/porosity and tensile properties
**AlSi10Mg: powder aging (not only reuse number) can dominate**
* Fedina et al. (AlSi10Mg) show that aging/handling leading to higher oxygen content can sharply increase porosity and reduce strength/ductility. Reported porosity increased from **3.52% to 6.5%** (and CT ROI values of **0.97% to 10.12%**) when comparing R0 vs “R0 aged 96 h” conditions, with tensile reductions, e.g. horizontal: **YS 166.0 → 140.3 MPa**, **UTS 247.3 → 179.7 MPa**, **elongation 4.9% → 1.5%**. (fedina2022influenceofalsi10mg pages 8-10)

**AlSi10Mg0.4: long-term reused powder leads to higher porosity and lower mechanical properties**
* Fiegl et al. report that long-term reused AlSi10Mg0.4 powder increased porosity from **<1% up to ~3%** (described as ~quadrupled) and decreased tensile/yield strength and elongation by **~15%**, with oxide/hydroxide formation implicated. (fiegl2021effectofalsi10mg0.4 pages 1-2)

**Al–Mg–Sc–Zr (Scalmalloy-like): reuse increased porosity and can degrade flowability**
* Cordova et al. (Al–Mg–Sc–Zr) measured µCT porosity rising from **0.06 ± 0.01% (virgin)** to **0.15 ± 0.01% (reused)**; average and maximum pore sizes were similar order (max **108.1 → 126 µm**). (cordova2020effectsofpowder pages 12-16)
* In another Scalmalloy reuse dataset, flowability degraded (virgin → used 3×): **HR 1.10 → 1.15** and **CI 8.9% → 13.5%**, consistent with satellites/irregular particles being particularly detrimental when PSD does not shift enough to compensate. (cordova2019revealingtheeffects pages 7-9)

**AlSi7Mg0.6: modest reuse can be stable if recycling excludes waste/spatter**
* Smolina et al. report stable PSD through five reuse batches (P0–P4) with x50,3 staying about **39.76–40.21 µm**, but “waste powder” was dramatically coarser (**x50,3 = 97.50 µm; x90,3 = 188.34 µm**), consistent with spatter/unmelted mixtures. (smolina2022influenceofthe pages 6-8)

### 2.3 Why recycling sometimes appears to “improve” properties
Several studies report that reused AlSi10Mg can show improved flowability because **fine particles are depleted**, shifting PSD to coarser sizes; this can improve powder-bed packing/spreadability and, in some cases, increase yield/UTS within a limited reuse window. (weiss2022ontheinfluence pages 1-2, weiss2021investigationtowardsalsi10mg pages 11-13)

## 3) Visual quantitative evidence (reuse-cycle trends)
The following figure crops from Weiss et al. show the requested quantitative, cycle-indexed degradation trends:
* PSD metrics, sphericity, and flowability (avalanche/rest angles) versus powder use cycle **0–10** (weiss2022ontheinfluence media b4882a71)
* Chemical analysis showing **oxygen and hydrogen (mg/kg)** versus powder use cycle **0–10** (weiss2022ontheinfluence media 0efdbac3)

## 4) Consolidated quantitative reference table
| Item | Quantitative data (with units) | Alloy/system | Reuse/condition | Implication for LPBF |
|---|---|---|---|---|
| Recommended PSD range for LPBF Al powders | Typical LPBF mean size/range reported as **15–45 µm**; commercial Al powders often **15–50 µm**; SLM/LPBF target PSD commonly **15–63 µm**; layer thicknesses **<30 µm** are difficult with typical 15–50 µm Al powders (trevisan2018studyandcharacterisation pages 63-66, balbaa2021roleofpowder pages 1-4, cordova2019revealingtheeffects pages 7-9) | General LPBF Al alloys / AlSi10Mg | Recommended feedstock range | PSD must balance packing and flow; too many fines improve absorptivity but worsen cohesion/spreadability, while overly coarse powder can limit thin-layer deposition and detail resolution (trevisan2018studyandcharacterisation pages 63-66, balbaa2021roleofpowder pages 1-4, balbaa2021roleofpowder pages 14-18) |
| Example PSD metrics from production powders | Carrozza Al-alloy powders: **D10/D50/D90 = 18.7/31.8/53.4 to 30.2/49.3/80.2 µm** across seven samples; examples: **20.6/34.7/56.2 µm**, **29.1/47.9/78.3 µm**, **23.4/49.9/84.7 µm** (carrozza2017characterizationofpowders pages 8-12) | Al-alloy LPBF powders | Virgin/commercial batches | Demonstrates the practical PSD window actually supplied for LPBF-type Al powders; broader/coarser tails can still be processable if flow is acceptable (carrozza2017characterizationofpowders pages 8-12) |
| Example PSD metrics with reuse | AlSi7Mg0.6 P0–P4: **x10,3 ≈ 26.1–26.54 µm, x50,3 ≈ 39.76–40.21 µm, x90,3 ≈ 58.73–59.08 µm**; waste PW: **37.78/97.50/188.34 µm** (smolina2022influenceofthe pages 6-8) | AlSi7Mg0.6 | P0–P4 reused powder vs waste/spatter-rich powder | Regularly recycled sieved powder remained stable through five cycles, but waste/spatter powder became dramatically coarser and unsuitable as-is for direct reuse (smolina2022influenceofthe pages 6-8) |
| Flowability thresholds and example values | Hall/Carney criterion: powders flowing through **Hall funnel (2.5 mm)** considered to have good flowability; powders passing only **Carney (5 mm)** are less certain; non-flowing powders are rejected (carrozza2017characterizationofpowders pages 8-12). Excellent-flow thresholds: **Hausner ratio <1.11** and **Carr index <10%** (cordova2019revealingtheeffects pages 7-9) | General LPBF Al powders | Acceptance screening | LPBF needs flowable powder for consistent recoating; Hall/Carney plus HR/CI provide practical go/no-go indicators, though cohesive Al powders may require more advanced rheometry (carrozza2017characterizationofpowders pages 8-12, cordova2019revealingtheeffects pages 7-9) |
| Flowability examples for Al powders | AlSi10Mg HR/CI: **1.09 / 8.4% (virgin)** to **1.11 / 9.9% (used 6×)**; Scalmalloy HR/CI: **1.10 / 8.9% (virgin)** to **1.15 / 13.5% (used 3×)**. Carrozza examples: flow times **11.3–70.6 s/50 g**, angle of repose **28.26–31.88°**; some powders did not flow (cordova2019revealingtheeffects pages 7-9, carrozza2017characterizationofpowders pages 8-12) | AlSi10Mg, Scalmalloy, Al-alloy batches | Virgin vs reused; multiple commercial batches | AlSi10Mg can retain acceptable flow after reuse if fines are depleted; Scalmalloy may degrade faster because satellites/irregular particles raise compressibility and reduce flow robustness (cordova2019revealingtheeffects pages 7-9) |
| Oxygen content example and cycle tracking | Fresh AlSi10Mg powder oxygen reported at **850 mg/kg**; oxygen and hydrogen were tracked versus **0–10 powder-use cycles**; cycle dependence was stronger for flowability metrics than PSD (**R²AA = 0.8732, R²RA = 0.6469, R²d90 = 0.4902, R²d50 = 0.3985, R²d10 = 0.3331**) (weiss2022ontheinfluence pages 5-6) | AlSi10Mg | 0–10 reuse cycles | Oxygen/hydrogen monitoring is essential because Al powders are oxidation-sensitive; even when PSD shifts are modest, flow behavior can change substantially with reuse (weiss2022ontheinfluence pages 5-6) |
| Morphology changes with reuse | Reuse commonly causes **fewer fines**, coarsening, **more satellites**, and more **teardrop/irregular particles**; Scalmalloy reuse showed irregular particles/satellites after **3×**, while AlSi10Mg after **6×** showed PSD right-shift and fewer fines (weiss2022ontheinfluence pages 1-2, cordova2019revealingtheeffects pages 7-9) | AlSi10Mg, Scalmalloy | Reused powder | Loss of fines can improve flow, but spatter/satellite accumulation worsens morphology and can eventually reduce spreadability and increase defects, especially in more reuse-sensitive Al systems (weiss2022ontheinfluence pages 1-2, cordova2019revealingtheeffects pages 7-9) |
| Part-property changes: aged AlSi10Mg powder | Fedina: Archimedes density dropped from about **96.42% to 93.50%** and porosity rose from **3.52% to 6.5%** with aged powder; CT in ROI showed **99.03% density / 0.97% porosity** for R0 vs **89.88% / 10.12%** for R0 aged 96 h. Tensile properties fell from **YS 166.0→140.3 MPa, UTS 247.3→179.7 MPa, elongation 4.9→1.5%** (horizontal) and **YS 171.7→150.3 MPa, UTS 269.7→229.3 MPa, elongation 7.1→3.4%** (vertical) (fedina2022influenceofalsi10mg pages 8-10, fedina2022influenceofalsi10mg pages 1-2) | AlSi10Mg | Virgin R0 vs aged 96 h powder | Aging/oxidation severely reduces density and ductility, mainly by increasing lack-of-fusion and interconnected porosity; standard virgin parameters may not transfer to aged powder (fedina2022influenceofalsi10mg pages 8-10, fedina2022influenceofalsi10mg pages 1-2) |
| Part-property changes: reused Scalmalloy | Porosity by µCT increased from **0.06 ± 0.01%** to **0.15 ± 0.01%**; average pore sphericity **0.56 ± 0.05 → 0.61 ± 0.04**; average pore size **17.8 ± 7.7 → 16.7 ± 6.5 µm**; maximum pore size **108.1 → 126 µm**; average grain size stayed similar at **2.3 vs 2.4 µm** (cordova2020effectsofpowder pages 12-16) | Al–Mg–Sc–Zr / Scalmalloy-like alloy | Virgin vs reused powder | Reuse increased pore content by ~2.5× without major grain-size change, indicating the main effect was powder/processability rather than bulk microstructure (cordova2020effectsofpowder pages 12-16) |
| Long-term reused AlSi10Mg0.4 | Reused powder caused porosity to rise from **<1% to ~3%** (described as ~quadrupled), with **~15%** decreases in tensile/yield strength and elongation; drying-related mitigation in related Al powder reduced porosity from **~3% to ~1%** (fiegl2021effectofalsi10mg0.4 pages 1-2) | AlSi10Mg0.4 | Long-term reused powder | Long-term recycling without compensating process control or drying can materially degrade part quality; moisture/oxide pickup is a key mechanism (fiegl2021effectofalsi10mg0.4 pages 1-2) |


*Table: This table compiles quantitative powder requirements and observed recycling-induced degradation for LPBF aluminum alloys. It is useful as a quick reference linking powder metrics to expected processability and part-property outcomes.*

## Limitations of the retrieved corpus
* **Fatigue-property impacts of Al powder reuse** (quantitative S–N or fatigue limit shifts vs reuse cycle) were not found in the retrieved full-text segments; the available evidence primarily quantifies porosity and monotonic tensile changes. (fiegl2021effectofalsi10mg0.4 pages 1-2, fedina2022influenceofalsi10mg pages 8-10)
* **A universal “required oxygen content limit” for LPBF Al powders** was not stated in the retrieved texts. Instead, the evidence supports that oxygen/hydrogen should be monitored (e.g., mg/kg) and that increases correlate with worse wetting and higher porosity, especially under aging/poor handling. (fedina2022influenceofalsi10mg pages 8-10, weiss2022ontheinfluence pages 5-6)

References

1. (trevisan2018studyandcharacterisation pages 63-66): FRANCESCO TREVISAN. Study and characterisation of different metal alloys processed through laser powder bed fusion. PhD thesis, Politecnico di Torino, Jun 2018. URL: https://doi.org/10.6092/polito/porto/2709711, doi:10.6092/polito/porto/2709711. This article has 7 citations.

2. (balbaa2021roleofpowder pages 1-4): M.A. Balbaa, A. Ghasemi, E. Fereiduni, M.A. Elbestawi, S.D. Jadhav, and J.-P. Kruth. Role of powder particle size on laser powder bed fusion processability of alsi10mg alloy. Additive Manufacturing, 37:101630, Jan 2021. URL: https://doi.org/10.1016/j.addma.2020.101630, doi:10.1016/j.addma.2020.101630. This article has 224 citations and is from a highest quality peer-reviewed journal.

3. (cordova2019revealingtheeffects pages 7-9): Laura Cordova, Mónica Campos, and Tiedo Tinga. Revealing the effects of powder reuse for selective laser melting by powder characterization. JOM, 71:1062-1072, Jan 2019. URL: https://doi.org/10.1007/s11837-018-3305-2, doi:10.1007/s11837-018-3305-2. This article has 318 citations and is from a peer-reviewed journal.

4. (carrozza2017characterizationofpowders pages 8-12): A Carrozza. Characterization of powders to be used in a laser powder bed machine. analysis of the critical parameters and relationship with powder flowability. Unknown journal, 2017.

5. (balbaa2021roleofpowder pages 14-18): M.A. Balbaa, A. Ghasemi, E. Fereiduni, M.A. Elbestawi, S.D. Jadhav, and J.-P. Kruth. Role of powder particle size on laser powder bed fusion processability of alsi10mg alloy. Additive Manufacturing, 37:101630, Jan 2021. URL: https://doi.org/10.1016/j.addma.2020.101630, doi:10.1016/j.addma.2020.101630. This article has 224 citations and is from a highest quality peer-reviewed journal.

6. (weiss2022ontheinfluence pages 1-2): C. Weiss, C. L. Haefner, and J. Munk. On the influence of alsi10mg powder recycling behavior in the lpbf process and consequences for mechanical properties. JOM, 74:1188-1199, Jan 2022. URL: https://doi.org/10.1007/s11837-021-05080-4, doi:10.1007/s11837-021-05080-4. This article has 34 citations and is from a peer-reviewed journal.

7. (fedina2022influenceofalsi10mg pages 8-10): Tatiana Fedina, Filippo Belelli, Giorgia Lupi, Benedikt Brandau, Riccardo Casati, Raphael Berneth, Frank Brueckner, and Alexander F.H. Kaplan. Influence of alsi10mg powder aging on the material degradation and its processing in laser powder bed fusion. Powder Technology, 412:118024, Nov 2022. URL: https://doi.org/10.1016/j.powtec.2022.118024, doi:10.1016/j.powtec.2022.118024. This article has 22 citations and is from a domain leading peer-reviewed journal.

8. (weiss2022ontheinfluence pages 5-6): C. Weiss, C. L. Haefner, and J. Munk. On the influence of alsi10mg powder recycling behavior in the lpbf process and consequences for mechanical properties. JOM, 74:1188-1199, Jan 2022. URL: https://doi.org/10.1007/s11837-021-05080-4, doi:10.1007/s11837-021-05080-4. This article has 34 citations and is from a peer-reviewed journal.

9. (weiss2022ontheinfluence media b4882a71): C. Weiss, C. L. Haefner, and J. Munk. On the influence of alsi10mg powder recycling behavior in the lpbf process and consequences for mechanical properties. JOM, 74:1188-1199, Jan 2022. URL: https://doi.org/10.1007/s11837-021-05080-4, doi:10.1007/s11837-021-05080-4. This article has 34 citations and is from a peer-reviewed journal.

10. (martucci2023developmentandcharacterisation pages 42-45): A Martucci. Development and characterisation of al-based alloys processed by pbf-lb/m. Unknown journal, 2023.

11. (fiegl2021effectofalsi10mg0.4 pages 1-2): Tobias Fiegl, Martin Franke, Ahmad Raza, Eduard Hryha, and Carolin Körner. Effect of alsi10mg0.4 long-term reused powder in pbf-lb/m on the mechanical properties. Materials &amp; Design, 212:110176, Dec 2021. URL: https://doi.org/10.1016/j.matdes.2021.110176, doi:10.1016/j.matdes.2021.110176. This article has 59 citations and is from a highest quality peer-reviewed journal.

12. (weiss2022ontheinfluence media 0efdbac3): C. Weiss, C. L. Haefner, and J. Munk. On the influence of alsi10mg powder recycling behavior in the lpbf process and consequences for mechanical properties. JOM, 74:1188-1199, Jan 2022. URL: https://doi.org/10.1007/s11837-021-05080-4, doi:10.1007/s11837-021-05080-4. This article has 34 citations and is from a peer-reviewed journal.

13. (cordova2020effectsofpowder pages 12-16): Laura Cordova, Ton Bor, Marc de Smit, Simone Carmignato, Mónica Campos, and Tiedo Tinga. Effects of powder reuse on the microstructure and mechanical behaviour of al–mg–sc–zr alloy processed by laser powder bed fusion (lpbf). Additive Manufacturing, 36:101625, Dec 2020. URL: https://doi.org/10.1016/j.addma.2020.101625, doi:10.1016/j.addma.2020.101625. This article has 140 citations and is from a highest quality peer-reviewed journal.

14. (smolina2022influenceofthe pages 6-8): Irina Smolina, Konrad Gruber, Andrzej Pawlak, Grzegorz Ziółkowski, Emilia Grochowska, Daniela Schob, Karol Kobiela, Robert Roszak, Matthias Ziegenhorn, and Tomasz Kurzynowski. Influence of the alsi7mg0.6 aluminium alloy powder reuse on the quality and mechanical properties of lpbf samples. Materials, 15:5019, Jul 2022. URL: https://doi.org/10.3390/ma15145019, doi:10.3390/ma15145019. This article has 29 citations.

15. (weiss2021investigationtowardsalsi10mg pages 11-13): C. Weiss, J. Munk, and C.L. Haefner. Investigation towards alsi10mg powder recycling behavior in the lpbf process and its influences on mechanical properties. Unknown, Jan 2021. URL: https://doi.org/10.26153/tsw/17605, doi:10.26153/tsw/17605. This article has 8 citations.

16. (fedina2022influenceofalsi10mg pages 1-2): Tatiana Fedina, Filippo Belelli, Giorgia Lupi, Benedikt Brandau, Riccardo Casati, Raphael Berneth, Frank Brueckner, and Alexander F.H. Kaplan. Influence of alsi10mg powder aging on the material degradation and its processing in laser powder bed fusion. Powder Technology, 412:118024, Nov 2022. URL: https://doi.org/10.1016/j.powtec.2022.118024, doi:10.1016/j.powtec.2022.118024. This article has 22 citations and is from a domain leading peer-reviewed journal.


---

## Query 9

**Question:** What multi-material and functionally graded structures have been demonstrated using LPBF with aluminum alloys? Provide examples of aluminum-to-aluminum and aluminum-to-other-metal gradients with measured interface properties.

**Task ID:** `daf854f0-a249-4a1a-86ab-eedc96074bcf`

**Status:** complete

This response is limited to the aluminum-alloy multi-material/FG structures for which full-text evidence with quantitative interface properties was retrievable in this run; several additional Al-to-steel and Al-to-Ti LPBF demonstrations are identified in reviews but their primary-data interface metrics were not accessible here and therefore are not tabulated as “measured interface properties.” (dzogbewu2023powderbedfusion pages 7-9, wei2021recentprogressand pages 7-9, yao2023multimetalresearchin pages 5-6)

| Material pairing | Category | Architecture | LPBF / SLM strategy | Measured interface properties | Key interfacial microstructural notes | Evidence |
|---|---|---|---|---|---|---|
| Al6061 / AlSi10Mg | Al-to-Al | Discrete bimetal interface with fusion/transition zone | First ~10 layers (~0.3 mm) at the interface processed with varied laser parameters; Taguchi L16 design to optimize porosity and shear strength | Microhardness: Al6061 ~98.20 ± 1.26 HV; interface ~99.35 ± 1.03 HV; AlSi10Mg ~109.56 ± 0.5 HV. Iosipescu interfacial shear strength up to 178.54 ± 5.49 MPa. Tensile failure occurred in Al6061 rather than at the interface; hybrid UTS ~329.7 MPa, elongation ~2.41%. Fusion zone reported as narrow (<20 μm) in low-energy builds; wider fusion zones in higher-energy conditions correlated with improved bonding. Interfacial porosity negatively correlated with shear strength. | Epitaxial growth at interface and melt-pool boundaries; transition from columnar grains in AlSi10Mg to fine equiaxed grains at interface; Marangoni-driven mixing; LOF porosity most detrimental, while small keyhole pores/microcracks (<100 μm) had less effect | (ismail2025influenceofprocess pages 7-9, ismail2025influenceofprocess pages 9-12, ismail2025influenceofprocess pages 12-14, ismail2025influenceofprocess media e08e0488) |
| AlSi10Mg / wrought AA6061 | Al-to-Al | Discrete hybrid interface | LPBF AlSi10Mg deposited onto wrought AA6061 substrate; compared as-built and heat-treated hybrid parts | No direct localized interface hardness/shear metric reported in retrieved context; qualitative interface quality only. Bulk properties: as-built hybrid UTS 192.8 ± 3.4 MPa; elongation 13.6 ± 0.5%. Interface described as defect-free with no apparent pores/cracks; galvanic corrosion at interface suppressed. | Epitaxial growth; excellent metallurgical bonding without apparent pores/cracks; fine equiaxed + coarse columnar AlSi10Mg grains retained near interface | (zhao2023feasibilityandreliability pages 1-2) |
| AlSi10Mg / C18400 Cu alloy | Al-to-other-metal | Discrete bimetal interface with intermixed transition/fusion zone | Multi-material SLM/LPBF of AlSi10Mg and UNS C18400 Cu; interface characterized by FIB/SEM/EDS/EBSD/XRD | Microhardness across interface: Cu region 71.74 ± 7.5 HV, Al region 119.06 ± 9.12 HV; gradual increase from Cu to Al with anomalously high interface readings due to IMC formation. Intermixed/fusion zone thickness ~200 μm. Composite tensile strength 176 ± 31 MPa. Flexural strength ~200 MPa with Cu at root and ~500 MPa with Al at root; individual reported fracture flexural stresses included 184 and 244 MPa in one condition. | Al2Cu intermetallic identified at interface; Cu-rich and Al-rich regions with intermixed zone from diffusion; larger equiaxed grains at interface, columnar grains in AlSi10Mg, equiaxed grains in C18400; porosity and some interface cracking on Cu side; intermetallic formation shifted fracture behavior toward brittle cleavage | (sing2015interfacialcharacterizationof pages 14-21, sing2015interfacialcharacterizationof pages 1-7, sing2015interfacialcharacterizationof pages 21-24, sing2015interfacialcharacterizationof pages 7-14) |


*Table: This table summarizes LPBF/SLM multi-material aluminum systems in the retrieved evidence, separating Al-to-Al and Al-to-other-metal examples. It highlights which studies reported quantitative interface metrics versus only qualitative bonding observations, helping answer the user's question with evidence-matched examples.*

## Aluminum-to-aluminum (Al→Al) multi-material/graded interfaces demonstrated by LPBF

### Al6061 ↔ AlSi10Mg (LPBF bimetal; parameter-tuned transition zone)
A direct Al-to-Al multi-material interface was fabricated by printing AlSi10Mg onto an Al6061 substrate with the first ~10 layers (~0.3 mm) at the interface processed using varied LPBF parameters, enabling study of fusion-zone morphology, porosity, and interfacial strength. (ismail2025influenceofprocess pages 12-14)

Measured interface properties included (i) region-wise microhardness values: AlSi10Mg 109.56 ± 0.5 HV, Al6061 98.20 ± 1.26 HV, and an intermediate interface hardness 99.35 ± 1.03 HV; and (ii) Iosipescu-measured interfacial shear strength, with a best-performing parameter set reaching 178.54 ± 5.49 MPa. (ismail2025influenceofprocess pages 7-9, ismail2025influenceofprocess pages 9-12, ismail2025influenceofprocess pages 12-14)

Microstructurally, the interface exhibited epitaxial growth at the interface/melt-pool boundaries and a transition from columnar grains in AlSi10Mg to finer equiaxed grains at the interface; a narrow fusion zone (<20 μm) was reported in low-energy builds, while wider fusion zones (higher-energy conditions) were associated with improved bonding. Interfacial lack-of-fusion (LOF) porosity was reported to correlate negatively with interfacial shear strength. (ismail2025influenceofprocess pages 9-12)

Interface-property tables supporting these values are shown in the paper’s Table 4 (microhardness) and Table 5 (shear strength and porosity). (ismail2025influenceofprocess media e08e0488, ismail2025influenceofprocess media 6f3d6ed1)

### AlSi10Mg (LPBF) ↔ wrought AA6061 (hybrid part)
Another Al-to-Al hybrid approach deposited LPBF AlSi10Mg onto a wrought AA6061 substrate, reporting “excellent metallurgical bonding” at the interface without apparent pores/cracks and epitaxial growth, but the retrieved text did not include localized interface-property metrics (e.g., hardness-vs-distance or interfacial shear/tensile strength). The paper reports bulk tensile properties for the hybrid specimen (UTS 192.8 ± 3.4 MPa; elongation 13.6 ± 0.5%). (zhao2023feasibilityandreliability pages 1-2)

## Aluminum-to-other-metal (Al→X) multi-material/graded interfaces demonstrated by LPBF

### AlSi10Mg ↔ C18400 copper alloy (SLM/LPBF Al→Cu bimetal)
A widely cited LPBF/SLM multi-material Al-to-Cu interface was demonstrated using AlSi10Mg and UNS C18400 copper alloy. The interface was characterized by FIB/SEM/EDS/EBSD and XRD, and the intermetallic Al2Cu was identified at the Al/Cu bond interface. (sing2015interfacialcharacterizationof pages 14-21, sing2015interfacialcharacterizationof pages 1-7)

Measured interface-related properties included Vickers microhardness across the interface, with representative values reported for the two sides: 71.74 ± 7.5 HV on the copper side and 119.06 ± 9.12 HV on the aluminum side, with a gradual (nearly linear) increase across the interface and anomalously high readings at the immediate interface attributed to intermetallic formation. (sing2015interfacialcharacterizationof pages 14-21, sing2015interfacialcharacterizationof pages 21-24)

A characteristic intermixed/fusion (transition) zone thickness of ~200 μm was reported, consistent with extensive element intermixing/diffusion at the interface under the applied SLM conditions. (sing2015interfacialcharacterizationof pages 7-14)

Mechanical testing reported a composite tensile strength of 176 ± 31 MPa for the Al/Cu bimetal; flexural strength depended on build orientation/loading, with ~200 MPa reported when Cu was at the root and ~500 MPa when Al was at the root. (sing2015interfacialcharacterizationof pages 14-21, sing2015interfacialcharacterizationof pages 1-7)

## Additional aluminum-including LPBF multi-material/FG demonstrations noted in reviews (no quantitative interface properties accessible here)

Reviews of multi-material LPBF report additional aluminum-including systems such as Fe/Al-12Si (often exhibiting cracking), and Al–Si bonded to Al–Cu systems, and discuss trends such as increasing Fe–Al intermetallic-layer thickness reducing bond strength. However, the quantitative interface metrics for these cases were not present in the retrieved full-text excerpts and therefore are not used as “measured interface properties” in this answer. (dzogbewu2023powderbedfusion pages 7-9, wei2021recentprogressand pages 7-9)

References

1. (dzogbewu2023powderbedfusion pages 7-9): Thywill Cephas Dzogbewu and Deon de Beer. Powder bed fusion of multimaterials. Journal of Manufacturing and Materials Processing, 7:15, Jan 2023. URL: https://doi.org/10.3390/jmmp7010015, doi:10.3390/jmmp7010015. This article has 53 citations.

2. (wei2021recentprogressand pages 7-9): Chao Wei and Lin Li. Recent progress and scientific challenges in multi-material additive manufacturing via laser-based powder bed fusion. Virtual and Physical Prototyping, 16:347-371, May 2021. URL: https://doi.org/10.1080/17452759.2021.1928520, doi:10.1080/17452759.2021.1928520. This article has 311 citations and is from a peer-reviewed journal.

3. (yao2023multimetalresearchin pages 5-6): Liming Yao, Aditya Ramesh, Zhongmin Xiao, Yang Chen, and Quihui Zhuang. Multimetal research in powder bed fusion: a review. Materials, 16:4287, Jun 2023. URL: https://doi.org/10.3390/ma16124287, doi:10.3390/ma16124287. This article has 47 citations.

4. (ismail2025influenceofprocess pages 7-9): Linda Ismail, Omer F. Mohamed, Tareq Farrah, Pradeep George, and Andreas Schiffer. Influence of process parameters on microstructure and interfacial mechanical properties of al6061/alsi10mg multi-material components fabricated via laser powder bed fusion. Materials Science and Engineering: A, 928:148061, Apr 2025. URL: https://doi.org/10.1016/j.msea.2025.148061, doi:10.1016/j.msea.2025.148061. This article has 7 citations.

5. (ismail2025influenceofprocess pages 9-12): Linda Ismail, Omer F. Mohamed, Tareq Farrah, Pradeep George, and Andreas Schiffer. Influence of process parameters on microstructure and interfacial mechanical properties of al6061/alsi10mg multi-material components fabricated via laser powder bed fusion. Materials Science and Engineering: A, 928:148061, Apr 2025. URL: https://doi.org/10.1016/j.msea.2025.148061, doi:10.1016/j.msea.2025.148061. This article has 7 citations.

6. (ismail2025influenceofprocess pages 12-14): Linda Ismail, Omer F. Mohamed, Tareq Farrah, Pradeep George, and Andreas Schiffer. Influence of process parameters on microstructure and interfacial mechanical properties of al6061/alsi10mg multi-material components fabricated via laser powder bed fusion. Materials Science and Engineering: A, 928:148061, Apr 2025. URL: https://doi.org/10.1016/j.msea.2025.148061, doi:10.1016/j.msea.2025.148061. This article has 7 citations.

7. (ismail2025influenceofprocess media e08e0488): Linda Ismail, Omer F. Mohamed, Tareq Farrah, Pradeep George, and Andreas Schiffer. Influence of process parameters on microstructure and interfacial mechanical properties of al6061/alsi10mg multi-material components fabricated via laser powder bed fusion. Materials Science and Engineering: A, 928:148061, Apr 2025. URL: https://doi.org/10.1016/j.msea.2025.148061, doi:10.1016/j.msea.2025.148061. This article has 7 citations.

8. (zhao2023feasibilityandreliability pages 1-2): Cuiling Zhao, Yuchao Bai, and Hao Wang. Feasibility and reliability of laser powder bed fused alsi10mg/wrought aa6061 hybrid aluminium alloy component. International Journal of Precision Engineering and Manufacturing-Green Technology, 10:959-977, Oct 2023. URL: https://doi.org/10.1007/s40684-022-00456-6, doi:10.1007/s40684-022-00456-6. This article has 22 citations.

9. (sing2015interfacialcharacterizationof pages 14-21): S. Sing, L. P. Lam, Dan Zhang, Zhonghong Liu, and C. Chua. Interfacial characterization of slm parts in multi-material processing: intermetallic phase formation between alsi10mg and c18400 copper alloy. Materials Characterization, 107:220-227, Sep 2015. URL: https://doi.org/10.1016/j.matchar.2015.07.007, doi:10.1016/j.matchar.2015.07.007. This article has 307 citations and is from a peer-reviewed journal.

10. (sing2015interfacialcharacterizationof pages 1-7): S. Sing, L. P. Lam, Dan Zhang, Zhonghong Liu, and C. Chua. Interfacial characterization of slm parts in multi-material processing: intermetallic phase formation between alsi10mg and c18400 copper alloy. Materials Characterization, 107:220-227, Sep 2015. URL: https://doi.org/10.1016/j.matchar.2015.07.007, doi:10.1016/j.matchar.2015.07.007. This article has 307 citations and is from a peer-reviewed journal.

11. (sing2015interfacialcharacterizationof pages 21-24): S. Sing, L. P. Lam, Dan Zhang, Zhonghong Liu, and C. Chua. Interfacial characterization of slm parts in multi-material processing: intermetallic phase formation between alsi10mg and c18400 copper alloy. Materials Characterization, 107:220-227, Sep 2015. URL: https://doi.org/10.1016/j.matchar.2015.07.007, doi:10.1016/j.matchar.2015.07.007. This article has 307 citations and is from a peer-reviewed journal.

12. (sing2015interfacialcharacterizationof pages 7-14): S. Sing, L. P. Lam, Dan Zhang, Zhonghong Liu, and C. Chua. Interfacial characterization of slm parts in multi-material processing: intermetallic phase formation between alsi10mg and c18400 copper alloy. Materials Characterization, 107:220-227, Sep 2015. URL: https://doi.org/10.1016/j.matchar.2015.07.007, doi:10.1016/j.matchar.2015.07.007. This article has 307 citations and is from a peer-reviewed journal.

13. (ismail2025influenceofprocess media 6f3d6ed1): Linda Ismail, Omer F. Mohamed, Tareq Farrah, Pradeep George, and Andreas Schiffer. Influence of process parameters on microstructure and interfacial mechanical properties of al6061/alsi10mg multi-material components fabricated via laser powder bed fusion. Materials Science and Engineering: A, 928:148061, Apr 2025. URL: https://doi.org/10.1016/j.msea.2025.148061, doi:10.1016/j.msea.2025.148061. This article has 7 citations.


---

## Query 10

**Question:** What surface treatment and post-processing methods (shot peening, laser shock peening, chemical etching, anodizing) have been applied to LPBF aluminum alloys? Provide quantitative data on surface roughness improvement and fatigue life enhancement.

**Task ID:** `60b56741-7297-41b4-ac47-c38366053f88`

**Status:** complete

Surface treatment and post-processing of LPBF aluminum alloys: quantitative roughness and fatigue outcomes

| Alloy | Treatment | Roughness before → after (% change) | Fatigue before → after (improvement) | Fatigue test condition | Citations |
|---|---|---|---|---|---|
| SLM AlSi12 | Shot peening (SP) on as-built surface | Rz/Wz decreased after SP vs as-built; absolute values not printed in extracted text (see Fig. 8) | Fatigue strength: 56 → 89 MPa at 2×10^6 cycles (+58.9%); 51 → 81 MPa at 1×10^7 cycles (+58.8%) | Plane bending, R = 0, 20 Hz, stop at 10^7 cycles | (nakamura2023effectofshot pages 4-6, nakamura2023effectofshot pages 2-4, nakamura2023effectofshot media 36949a6f) |
| SLM AlSi12 | Laser peening (LP) on as-built surface | Rz/Wz increased after LP vs as-built; absolute values not printed in extracted text (see Fig. 8) | Fatigue strength: 56 → 90 MPa at 2×10^6 cycles (+60.7%); 51 → 90 MPa at 1×10^7 cycles (+76.5%) | Plane bending, R = 0, 20 Hz, stop at 10^7 cycles | (nakamura2023effectofshot pages 4-6, nakamura2023effectofshot pages 2-4, nakamura2023effectofshot media 36949a6f) |
| LPBF AlSi10Mg (V-notched) | LSP2 | Ra 4.34 → 3.98 µm (−8.3%) | Cycles to failure at 110 MPa: 1.26×10^4 → 2.53×10^6 (199×) | Rotating bending, σ = 110 MPa | (maleki2022ontheeffects pages 10-14, maleki2022ontheeffects media 772e3fd5) |
| LPBF AlSi10Mg (V-notched) | LSP2 + electrochemical polishing (ECP) | Ra 4.34 → 3.23 µm (−25.6%) | Fatigue life reported as 375× vs as-built | Rotating bending, σ = 110 MPa | (maleki2022ontheeffects pages 10-14, maleki2022ontheeffects media 772e3fd5) |
| LPBF AlSi10Mg (V-notched) | HT + LSP2 | Ra 4.38 → 3.82 µm (−12.8%) | Cycles to failure at 110 MPa: 1.26×10^4 → 3.08×10^6 (243×) | Rotating bending, σ = 110 MPa | (maleki2022ontheeffects pages 19-21, maleki2022ontheeffects pages 10-14) |
| LPBF AlSi10Mg (V-notched) | HT + LSP2 + ECP | Ra 4.38 → 3.03 µm (−30.8%) | Cycles to failure at 110 MPa: 1.26×10^4 → 5.10×10^6 (402×) | Rotating bending, σ = 110 MPa | (maleki2022ontheeffects pages 19-21, maleki2022ontheeffects pages 10-14, maleki2022ontheeffects media 772e3fd5) |
| LPBF AlSi10Mg | LSP6 (4.5 J, 75% overlap) | Rv 25.78 → 16.33 µm (−36.7%); Ra/Rq measured but not numerically extracted | No fatigue metric reported in this corrosion-focused paper | Not reported here | (maleki2023effectsoflaser pages 1-2, maleki2023effectsoflaser media 54d71d4c, maleki2023effectsoflaser pages 4-6) |
| PBF-LS AlSi10Mg | LCP (submerged laser peening / laser cavitation peening) | Quantitative Ra not extracted in text used for fatigue summary | Fatigue strength at 10^7 cycles: 54 ± 9 → 85 ± 10 MPa (+57.4%, 1.57×); cycles at 110 MPa: 77,417 → 211,419 (2.73×) | Plane bending, R = −1; also σa = 110 MPa comparison | (soyama2024improvementoffatigue pages 19-21, soyama2024improvementoffatigue pages 17-19, soyama2024improvementoffatigue pages 1-2) |
| PBF-LS AlSi10Mg | B + LT + LCP | Quantitative Ra not extracted in text used for fatigue summary | Fatigue strength at 10^7 cycles: 54 ± 9 → 103 ± 12 MPa (+90.7%, 1.91×); cycles at 110 MPa: 77,417 → 1,865,502 (24.1×) | Plane bending, R = −1; also σa = 110 MPa comparison | (soyama2024improvementoffatigue pages 19-21, soyama2024improvementoffatigue pages 17-19) |
| LPBF Scalmalloy | Shot peening (SP) vs heat-treated (HT) reference | Ra 11.8 → 9.1 µm (−22.9%); Rz 57.3 → 45.4 µm (−20.8%); Sa reduction ~65% reported for SP parameter study | Fatigue limit of SP is 42 MPa higher than machined (M); fatigue life +45% vs M | S–N testing; exact R ratio not extracted | (zha2026surfaceandstructural pages 6-8, zha2026surfaceandstructural pages 10-12) |
| LPBF Scalmalloy | Machining (M) | Ra 11.8 → 3.9 µm (−66.9%); Rz 57.3 → 20.2 µm (−64.7%) | Lower fatigue than SP; SP gives +45% fatigue life vs M | S–N testing; exact R ratio not extracted | (zha2026surfaceandstructural pages 10-12) |
| LPBF Scalmalloy | Machining + shot peening (M+SP) | Ra 11.8 → 6.2 µm (−47.5%); Rz 57.3 → 24.1 µm (−57.9%); vs SP alone, Ra 9.1 → 6.2 µm (−31.9%) | Strength level is 10 MPa higher than SP; roughness reduction from SP to M+SP associated with ~8% fatigue improvement | S–N testing; exact R ratio not extracted | (zha2026surfaceandstructural pages 8-10, zha2026surfaceandstructural pages 10-12) |
| LPBF A357 (AlSi7Mg0.6) | ECO anodizing on as-built P surface | Substrate Ra ~9–16 µm before treatment; anodic layer P-ECO Ra = 9.7 ± 1.0 µm, Rq = 12.4 ± 1.3 µm, Sa = 9.6 ± 0.6 µm, Sq = 13.3 ± 0.1 µm; roughness increase on LPBF surfaces described as negligible (Rq ratio ~1–1.1) | No fatigue data reported | Tribology/coating study, not fatigue | (lorenzetti2023anodizingbyelectrochemical media 3661b595, lorenzetti2023anodizingbyelectrochemical pages 5-8) |
| LPBF A357 (AlSi7Mg0.6) | PEO anodizing on as-built P surface | Substrate Ra ~9–16 µm before treatment; anodic layer P-PEO Ra = 9.9 ± 1.5 µm, Rq = 13.2 ± 2.1 µm | No fatigue data reported | Tribology/coating study, not fatigue | (lorenzetti2023anodizingbyelectrochemical media 3661b595, lorenzetti2023anodizingbyelectrochemical pages 5-8) |
| LPBF A357 (AlSi7Mg0.6) | ECO anodizing on rougher M surface | Substrate Ra ~9–16 µm before treatment; anodic layer M-ECO Ra = 18.2 ± 9.0 µm, Rq = 24.5 ± 11.6 µm, Sa = 10.4 ± 1.63 µm, Sq = 13.4 ± 1.4 µm | No fatigue data reported | Tribology/coating study, not fatigue | (lorenzetti2023anodizingbyelectrochemical media 3661b595, lorenzetti2023anodizingbyelectrochemical pages 5-8) |
| LPBF A357 (AlSi7Mg0.6) | PEO anodizing on rougher M surface | Substrate Ra ~9–16 µm before treatment; anodic layer M-PEO Ra = 18.8 ± 7.8 µm, Rq = 25.7 ± 10.6 µm | No fatigue data reported | Tribology/coating study, not fatigue | (lorenzetti2023anodizingbyelectrochemical media 3661b595, lorenzetti2023anodizingbyelectrochemical pages 5-8) |
| LPBF A357 (AlSi7Mg0.6) | Pre-polished + ECO anodizing | P-ECO pre-polished Ra = 2.7 ± 0.2 µm, Rq = 3.4 ± 0.2 µm, Sa = 1.9 ± 0.2 µm, Sq = 3.1 ± 0.2 µm; M-ECO pre-polished Ra = 2.9 ± 0.2 µm, Rq = 3.8 ± 0.2 µm, Sa = 3.2 ± 0.1 µm, Sq = 5.0 ± 0.6 µm | No fatigue data reported | Tribology/coating study, not fatigue | (lorenzetti2023anodizingbyelectrochemical pages 5-8) |


*Table: This table summarizes quantitative roughness and fatigue outcomes reported for shot peening, laser shock/submerged laser peening, electrochemical polishing, and anodizing on LPBF aluminum alloys. It highlights where data are directly comparable and where studies reported roughness changes without fatigue data.*

Shot peening (SP) and laser peening / laser shock peening (LP/LSP)

For an additively manufactured Al–Si alloy with rough surfaces (reported as SLM AlSi12), Nakamura et al. quantified fatigue-strength gains at fixed life levels after SP and LP. At 1×10^7 cycles, fatigue strength increased from 51 MPa (as-built) to 81 MPa after SP (+59%) and to 90 MPa after LP (+76%); at 2×10^6 cycles it increased from 56 MPa to 89 MPa (SP) and 90 MPa (LP). In the same study, shot peening reduced surface-roughness/waviness metrics (Rz/Wz), whereas laser peening increased Rz/Wz (Fig. 8), consistent with the authors’ interpretation that deeper compressive residual stress from LP outweighed roughness effects for fatigue (nakamura2023effectofshot pages 4-6, nakamura2023effectofshot media 36949a6f).

For LPBF Scalmalloy®, Zha et al. reported that shot peening decreased areal roughness Sa by ~65% relative to a heat-treated reference surface, and Table 5 provides profile metrics for fatigue specimens (HT: Ra 11.8 µm, Rz 57.3 µm; SP: Ra 9.1 µm, Rz 45.4 µm). Fatigue comparisons indicate that SP outperformed machining (M) despite rougher surfaces: the fatigue limit of SP specimens was 42 MPa higher than machined specimens and fatigue life was 45% higher, attributed mainly to compressive residual stress (zha2026surfaceandstructural pages 6-8, zha2026surfaceandstructural pages 10-12).

Laser shock peening combined with chemical/electrochemical post-processing

On V-notched LPBF AlSi10Mg, Maleki et al. reported notch-root roughness reduction and very large fatigue-life gains from LSP and electro-chemical polishing (ECP). Roughness changes included Ra 4.34 µm (as-built) to 3.98 µm after LSP2 (−8.3%), and to 3.23 µm after LSP2+ECP (−25.6%); the best hybrid (HT+LSP2+ECP) reduced Ra to 3.03 µm (−30.8% vs the ~4.38 µm heat-treated baseline). In rotating-bending fatigue at a constant 110 MPa, cycles-to-failure increased from 1.26×10^4 (as-built) to 2.53×10^6 after LSP2 (199×), and to 5.10×10^6 after HT+LSP2+ECP (402×) (maleki2022ontheeffects pages 10-14).

A separate corrosion-focused LSP study on LPBF AlSi10Mg reported that increasing LSP energy/overlap reduced maximum profile valley depth Rv from 25.78 µm (as-built) to 16.33 µm for the most aggressive condition LSP6 (−36.7%); intermediate LSP conditions gave Rv values of 19.97–18.14 µm. This paper did not report fatigue metrics (maleki2023effectsoflaser pages 4-6).

Submerged laser peening / laser cavitation peening (LCP) and hybrid blasting + laser processing

Soyama reported plane-bending fatigue of PBF–LS (LPBF) AlSi10Mg with submerged laser peening variants. Fatigue strength at N = 10^7 increased from 54 ± 9 MPa (as-built) to 85 ± 10 MPa after laser cavitation peening (LCP) and to 103 ± 12 MPa after the combined blasting + laser treatment + LCP (B+LT+LCP), i.e., ~1.6× and ~1.9× improvement, respectively. At a stress amplitude of 110 MPa, cycles-to-failure increased from 77,417 (as-built) to 211,419 (LCP; 2.73×) and to 1,865,502 (B+LT+LCP; 24.1×) (soyama2024improvementoffatigue pages 19-21).

Anodizing (ECO/PEO) on LPBF Al–Si alloys

For LPBF A357 (AlSi7Mg0.6), Lorenzetti et al. provided quantitative roughness data for anodic layers produced by electrochemical oxidation (ECO) and plasma electrolytic oxidation (PEO). Typical as-built substrate ranges before treatment were Ra ≈ 9–16 µm and Rq ≈ 13–23 µm. After anodizing, coating roughness depended strongly on the starting surface: for the P series, P-ECO Ra = 9.7 ± 1.0 µm (Rq = 12.4 ± 1.3 µm; Sa = 9.6 ± 0.6 µm), and P-PEO Ra = 9.9 ± 1.5 µm (Rq = 13.2 ± 2.1 µm); for the rougher M series, M-ECO Ra = 18.2 ± 9.0 µm (Rq = 24.5 ± 11.6 µm; Sa = 10.4 ± 1.63 µm), and M-PEO Ra = 18.8 ± 7.8 µm (Rq = 25.7 ± 10.6 µm). The authors noted that ECO caused negligible roughness increase on already-rough LPBF substrates (Rq ratio ≈ 1–1.1), whereas on very smooth cast substrates ECO increased roughness more substantially; however, this study focused on coating structure/tribology and did not report fatigue-life effects of anodizing (lorenzetti2023anodizingbyelectrochemical pages 5-8).

Limitations of the retrieved corpus

Within the retrieved full texts, quantitative fatigue improvements for anodizing (including sulfuric acid anodizing or PEO/ECO) on LPBF aluminum alloys were not available; the anodizing study retrieved reported roughness of coatings and tribological/scratch behavior but not fatigue (lorenzetti2023anodizingbyelectrochemical pages 5-8). “Chemical etching” in the retrieved fatigue-focused LPBF AlSi10Mg work was represented quantitatively as electro-chemical polishing (ECP) used as a surface-smoothing step in hybrid post-treatments rather than as acid etching alone (maleki2022ontheeffects pages 10-14).

References

1. (nakamura2023effectofshot pages 4-6): Misato Nakamura, Koji Takahashi, and Yuta Saito. Effect of shot and laser peening on fatigue strength of additively manufactured aluminum alloy with rough surfaces. Journal of Materials Engineering and Performance, 32:1589-1600, Aug 2023. URL: https://doi.org/10.1007/s11665-022-07225-1, doi:10.1007/s11665-022-07225-1. This article has 12 citations and is from a peer-reviewed journal.

2. (nakamura2023effectofshot pages 2-4): Misato Nakamura, Koji Takahashi, and Yuta Saito. Effect of shot and laser peening on fatigue strength of additively manufactured aluminum alloy with rough surfaces. Journal of Materials Engineering and Performance, 32:1589-1600, Aug 2023. URL: https://doi.org/10.1007/s11665-022-07225-1, doi:10.1007/s11665-022-07225-1. This article has 12 citations and is from a peer-reviewed journal.

3. (nakamura2023effectofshot media 36949a6f): Misato Nakamura, Koji Takahashi, and Yuta Saito. Effect of shot and laser peening on fatigue strength of additively manufactured aluminum alloy with rough surfaces. Journal of Materials Engineering and Performance, 32:1589-1600, Aug 2023. URL: https://doi.org/10.1007/s11665-022-07225-1, doi:10.1007/s11665-022-07225-1. This article has 12 citations and is from a peer-reviewed journal.

4. (maleki2022ontheeffects pages 10-14): Erfan Maleki, Sara Bagherifard, Okan Unal, Michele Bandini, and Mario Guagliano. On the effects of laser shock peening on fatigue behavior of v-notched alsi10mg manufactured by laser powder bed fusion. International Journal of Fatigue, 163:107035, Oct 2022. URL: https://doi.org/10.1016/j.ijfatigue.2022.107035, doi:10.1016/j.ijfatigue.2022.107035. This article has 75 citations and is from a domain leading peer-reviewed journal.

5. (maleki2022ontheeffects media 772e3fd5): Erfan Maleki, Sara Bagherifard, Okan Unal, Michele Bandini, and Mario Guagliano. On the effects of laser shock peening on fatigue behavior of v-notched alsi10mg manufactured by laser powder bed fusion. International Journal of Fatigue, 163:107035, Oct 2022. URL: https://doi.org/10.1016/j.ijfatigue.2022.107035, doi:10.1016/j.ijfatigue.2022.107035. This article has 75 citations and is from a domain leading peer-reviewed journal.

6. (maleki2022ontheeffects pages 19-21): Erfan Maleki, Sara Bagherifard, Okan Unal, Michele Bandini, and Mario Guagliano. On the effects of laser shock peening on fatigue behavior of v-notched alsi10mg manufactured by laser powder bed fusion. International Journal of Fatigue, 163:107035, Oct 2022. URL: https://doi.org/10.1016/j.ijfatigue.2022.107035, doi:10.1016/j.ijfatigue.2022.107035. This article has 75 citations and is from a domain leading peer-reviewed journal.

7. (maleki2023effectsoflaser pages 1-2): Erfan Maleki, Okan Unal, Shuai Shao, and Nima Shamsaei. Effects of laser shock peening on corrosion resistance of additive manufactured alsi10mg. Coatings, 13:874, May 2023. URL: https://doi.org/10.3390/coatings13050874, doi:10.3390/coatings13050874. This article has 26 citations.

8. (maleki2023effectsoflaser media 54d71d4c): Erfan Maleki, Okan Unal, Shuai Shao, and Nima Shamsaei. Effects of laser shock peening on corrosion resistance of additive manufactured alsi10mg. Coatings, 13:874, May 2023. URL: https://doi.org/10.3390/coatings13050874, doi:10.3390/coatings13050874. This article has 26 citations.

9. (maleki2023effectsoflaser pages 4-6): Erfan Maleki, Okan Unal, Shuai Shao, and Nima Shamsaei. Effects of laser shock peening on corrosion resistance of additive manufactured alsi10mg. Coatings, 13:874, May 2023. URL: https://doi.org/10.3390/coatings13050874, doi:10.3390/coatings13050874. This article has 26 citations.

10. (soyama2024improvementoffatigue pages 19-21): Hitoshi Soyama. Improvement of fatigue strength in additively manufactured aluminum alloy alsi10mg via submerged laser peening. Coatings, 14:1174, Sep 2024. URL: https://doi.org/10.3390/coatings14091174, doi:10.3390/coatings14091174. This article has 2 citations.

11. (soyama2024improvementoffatigue pages 17-19): Hitoshi Soyama. Improvement of fatigue strength in additively manufactured aluminum alloy alsi10mg via submerged laser peening. Coatings, 14:1174, Sep 2024. URL: https://doi.org/10.3390/coatings14091174, doi:10.3390/coatings14091174. This article has 2 citations.

12. (soyama2024improvementoffatigue pages 1-2): Hitoshi Soyama. Improvement of fatigue strength in additively manufactured aluminum alloy alsi10mg via submerged laser peening. Coatings, 14:1174, Sep 2024. URL: https://doi.org/10.3390/coatings14091174, doi:10.3390/coatings14091174. This article has 2 citations.

13. (zha2026surfaceandstructural pages 6-8): Dexiang Zha, Alessandro Fortunato, Alessandro Ascari, Enrico Troiani, and Erica Liverani. Surface and structural integrity evaluation of additively manufactured scalmalloy®. Progress in Additive Manufacturing, 11:25-37, Sep 2026. URL: https://doi.org/10.1007/s40964-025-01332-w, doi:10.1007/s40964-025-01332-w. This article has 0 citations and is from a peer-reviewed journal.

14. (zha2026surfaceandstructural pages 10-12): Dexiang Zha, Alessandro Fortunato, Alessandro Ascari, Enrico Troiani, and Erica Liverani. Surface and structural integrity evaluation of additively manufactured scalmalloy®. Progress in Additive Manufacturing, 11:25-37, Sep 2026. URL: https://doi.org/10.1007/s40964-025-01332-w, doi:10.1007/s40964-025-01332-w. This article has 0 citations and is from a peer-reviewed journal.

15. (zha2026surfaceandstructural pages 8-10): Dexiang Zha, Alessandro Fortunato, Alessandro Ascari, Enrico Troiani, and Erica Liverani. Surface and structural integrity evaluation of additively manufactured scalmalloy®. Progress in Additive Manufacturing, 11:25-37, Sep 2026. URL: https://doi.org/10.1007/s40964-025-01332-w, doi:10.1007/s40964-025-01332-w. This article has 0 citations and is from a peer-reviewed journal.

16. (lorenzetti2023anodizingbyelectrochemical media 3661b595): Luca Lorenzetti, Lavinia Tonelli, Iuri Boromei, Lorella Ceschini, Pavel Shashkov, and Carla Martini. Anodizing by electrochemical oxidation (eco) of the laser powder bed fusion-processed a357 aluminium alloy: microstructural characterization and dry sliding behaviour. Progress in Additive Manufacturing, 8:629-648, Nov 2023. URL: https://doi.org/10.1007/s40964-022-00353-z, doi:10.1007/s40964-022-00353-z. This article has 4 citations and is from a peer-reviewed journal.

17. (lorenzetti2023anodizingbyelectrochemical pages 5-8): Luca Lorenzetti, Lavinia Tonelli, Iuri Boromei, Lorella Ceschini, Pavel Shashkov, and Carla Martini. Anodizing by electrochemical oxidation (eco) of the laser powder bed fusion-processed a357 aluminium alloy: microstructural characterization and dry sliding behaviour. Progress in Additive Manufacturing, 8:629-648, Nov 2023. URL: https://doi.org/10.1007/s40964-022-00353-z, doi:10.1007/s40964-022-00353-z. This article has 4 citations and is from a peer-reviewed journal.


---

