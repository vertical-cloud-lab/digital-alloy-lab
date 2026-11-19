# Edison job-futurehouse-paperqa3-precedent result: precedent_collector_failures

**Task ID:** `11d5f460-eea2-48bf-8223-06d078686b63`  
**Status:** success

<details><summary>Query</summary>

```text
Find reports, manuals, application notes or papers on metal powder atomizers (ultrasonic such as the
AMAZEMET rePOWDER, gas, or centrifugal) and other inert-gas melting equipment in which hot metal,
coarse shot or molten runoff reached the powder collection container or its seals, so that elastomer
seals or gaskets overheated, smoked or burned, glass collection vessels or view ports cracked from
thermal shock, or the atmosphere's oxygen rose because a collector seal leaked. For each give the
equipment, what happened, the cause found and the fix (for example seal material, heat shields,
cooled flanges, metal collection pots, catch trays, interlocks or stop rules). Also report published
guidance on choosing seals and glass for powder collectors under melts above 1000 C, on leak testing
(rate of rise, helium) of atomizer chambers, and on how trace-oxygen sensors on such chambers should
be checked after a power failure.

```

</details>

Question: Find reports, manuals, application notes or papers on metal powder atomizers (ultrasonic such as the
AMAZEMET rePOWDER, gas, or centrifugal) and other inert-gas melting equipment in which hot metal,
coarse shot or molten runoff reached the powder collection container or its seals, so that elastomer
seals or gaskets overheated, smoked or burned, glass collection vessels or view ports cracked from
thermal shock, or the atmosphere's oxygen rose because a collector seal leaked. For each give the
equipment, what happened, the cause found and the fix (for example seal material, heat shields,
cooled flanges, metal collection pots, catch trays, interlocks or stop rules). Also report published
guidance on choosing seals and glass for powder collectors under melts above 1000 C, on leak testing
(rate of rise, helium) of atomizer chambers, and on how trace-oxygen sensors on such chambers should
be checked after a power failure.


No. # Metal-powder atomizer collectors: reported failures and applicable guidance

**Finding.** I did not locate a verifiable report of an AMAZEMET rePOWDER—or another metal-powder atomizer—in which hot shot or molten runoff **burned a powder-collector seal, cracked a glass collection vessel, or caused a measured oxygen rise through a damaged collector seal**. The sources below document related failures and preventive designs, but do not establish those particular event–cause–fix chains. They should not be cited as proof that such a collector incident occurred. (scientific2023comparisonofultrasonic pages 7-8, [name redacted]2020failureanalysisof pages 1-4, andrus1989thrustchambermaterial pages 88-91, salges2024processingandcharacterization pages 46-50)

The distinction between an observed failure and a design precaution is consequential here:

| Evidence class | Equipment/source | What happened or design provision | Cause/findings | Fix or safeguard actually reported | Relevance to requested collector event |
|---|---|---|---|---|---|
| **Documented incident** | SRNL Powder Production Facility, helium gas-spray atomizer, approximately 2.1 kg Pd-alloy charge | Faulty, diverging thermocouple readings prompted excessive RF power. Alumina thermocouple sheaths and the stopper rod failed; the broken rod remained in the nozzle throat and blocked discharge. | Melt temperature was estimated near 1,918–2,060 °C, approaching alumina’s melting point; spring load and slight misalignment probably contributed to creep rupture. | Replace contact thermocouples with non-contact infrared optical pyrometry. The source does **not** report that metal reached or damaged the collector. ([name redacted]2020failureanalysisof pages 1-4, [name redacted]2020failureanalysisof pages 4-10) | Adjacent atomizer overheating failure, **not** a collector-seal or glass-vessel incident. |
| **Documented operating problems** | Pratt & Whitney rapid-solidification-rate centrifugal atomizer | Disk-drive oil seals leaked; unstable rim atomization produced large splats that reduced yield or clogged the outlet. Fine powder and detached wall deposits could obstruct flow to the collector can. | Soft copper adhered to chamber walls; deposits could later fall, while unstable atomization and splashing generated coarse material. The oil-seal leak cause was not reported. | Shutdown was required for unstable atomization; lower-head blowdown nozzles were used to assure powder flow. **No oil-seal repair was specified**, so none should be inferred. (andrus1989thrustchambermaterial pages 88-91) | Closest documented case involving coarse splats and collector-path blockage, but no burned collector gasket, cracked glass, or oxygen rise. |
| **Reported modification, not a collector incident** | Howmet Spraycast-X vacuum-induction melting and gas-atomization system | Special seal designs were installed to avoid operational leakage after evacuation and argon backfill; low leak-up improved product cleanliness. | High chamber leak-up admitted contaminants and increased oxide and nitride inclusions; very low leak-up limited oxygen and nitrogen pickup during argon processing to generally under 15 ppm. | Improved sealing, evacuation before argon backfill, and operation under tight-vacuum and very-low-leak-up conditions. Collector seals were not identified. (prichard1992spraycastx"superalloyfor pages 4-6) | Documents atmosphere-leakage control, **not** hot metal overheating a collector seal. |
| **Preventive specification only** | 2017 LLNL/Arcast free-fall gas atomizer | Stainless-steel high-vacuum chamber; lower cone and six explosion-rated powder-removal hoppers with isolation valves and quick clamps; three redundant paramagnetic oxygen analyzers; specified leak rate below 1 × 10⁻⁶ atm·cm³/s. | Design requirements anticipated reactive, refractory, and radioactive powders and required inert transfer, vacuum integrity, and oxygen control. | Isolation valves, metal hoppers, redundant oxygen monitoring, evacuation and backfill capability, straight-groove O-rings or hygienic seals, and an acceptance leak criterion. ([name redacted]2017gasatomizationequipment pages 21-24) | Useful preventive architecture, but **not evidence that a collector seal failed or overheated**. |
| **Preventive design only** | EURECAT centrifugal atomizer | A sloped lower cone directs particles to a collector at the bottom cap; the chamber is evacuated to about 10⁻³ mbar and backfilled with inert gas. The spinning disk is water- or inert-gas-cooled. | Cooling is selected according to melt temperature; the controlled atmosphere prevents oxidation and contamination. No collector-gasket construction or failure is reported. | Disk cooling, closed metal chamber, vacuum and inert backfill, and gravity-assisted lower-cone collection. (salges2024processingandcharacterization pages 46-50) | No documented collector overheating, glass breakage, seal leak, or oxygen excursion. |
| **Search conclusion** | Published reports, papers, manuals, and specifications located in this search | **No located source confirmed hot shot or molten runoff burning or smoking a powder-collector elastomer seal, thermally shocking and cracking a glass collection vessel or viewport, or raising chamber oxygen specifically through a damaged collector seal.** | The available literature more often reports upstream overheating, outlet plugging, wall deposition, generic seal leakage, or preventive collector design. | Treat proposed heat shields, cooled collector flanges, metal pots, catch trays, and stop rules as engineering recommendations unless a source expressly reports their adoption after such an event. | This evidence gap prevents presenting the requested collector scenarios as documented incidents. |


*Table: This table separates documented atomizer failures from preventive design specifications and identifies how closely each source matches the requested collector-seal, glass-breakage, and oxygen-leak scenarios.*

The clearest nearby failure is the Savannah River Pd-alloy gas-atomization run: erroneous thermocouple readings drove excessive heating, alumina parts fractured, and a broken stopper **blocked** the nozzle. The metal therefore did **not** run into the collector; the reported change was to noncontact infrared pyrometry. The paper’s equipment schematic shows the cooling path and downstream cyclone/collector, but does not depict collector damage. ([name redacted]2020failureanalysisof pages 1-4, [name redacted]2020failureanalysisof pages 4-10, [name redacted]2020failureanalysisof media b6770702)

In Pratt & Whitney’s centrifugal atomizer, the reported disk-drive **oil-seal** leakage must not be mistaken for a leaking powder-collector gasket. Unstable disk-rim operation produced large splats and could clog the outlet; the report calls for shutdown in that condition and describes lower-head blowdown to move retained powder toward the collector. It does not identify a repair for the oil seals. Howmet’s Spraycast-X account likewise reports special seals installed *to avoid* chamber leakage and better cleanliness at low leak-up, without identifying a thermally damaged collector seal. (andrus1989thrustchambermaterial pages 88-91, prichard1992spraycastx"superalloyfor pages 4-6)

## Choosing the hot-side collector, seals and glass

**Separate melt temperature from seal temperature.** For a melt above 1,000 °C, the relevant elastomer limit is the *measured or conservatively predicted temperature at its installed sealing surface*, including credible upset conditions—not the nominal melt temperature or a material name alone. Seal guidance warns that formulation, chemistry, swelling, thermal expansion and gland design all matter; FKM grades are not interchangeable, and even FFKM must be selected by grade and service. A cited mechanical-seal review describes ordinary FKM service around 400 °F (approximately 204 °C), with some specialty *static* compounds rated to 250 °F (approximately 121 °C); these are **not** ratings for direct contact with molten metal. That review is not a collector qualification standard. (huebner2005materialselectionfor pages 5-6, huebner2005materialselectionfor pages 4-5)

**Keep the impact and runoff path metallic and away from elastomers.** The LLNL/Arcast atomizer specification calls for a stainless-steel vacuum chamber, a lower cone, isolation valves and six explosion-rated removable powder hoppers; EURECAT describes a sloped metal lower cone leading to its collector. A separate high-temperature vacuum reactor demonstrates water cooling of a flange and use of Viton seals at *cooled* quartz windows, not at the hot workpiece. Accordingly, a metal receiving pot or catch tray, a shielded or cooled collector flange, and a seal outside any direct shot/runoff path are defensible **design recommendations** to assess and validate—not fixes shown to have followed a collector fire in these publications. Verify their thermal performance and the collector’s pressure/vacuum rating for the actual installation. ([name redacted]2017gasatomizationequipment pages 21-24, jubber1994designofa pages 3-4, salges2024processingandcharacterization pages 46-50)

**Do not substitute an ordinary glass jar for a qualified hot-metal receiver.** In an optical-access high-temperature apparatus, the designers rejected soda-lime and borosilicate glass and selected quartz for its lower thermal expansion and higher continuous operating-temperature capability; they also cushioned and sealed its metal interfaces with gaskets and sized the window for the applicable pressure difference. Comparative glass data give approximate expansion coefficients of 3.4 × 10⁻⁶/°C for borosilicate and 0.55 × 10⁻⁶/°C for fused silica. These properties favor an engineered, protected observation window where optical access is necessary; **neither source certifies quartz or borosilicate as a vessel safe from direct molten-metal impact**. Window strength, mounting stress, thermal gradients and pressure loading still require specific engineering assessment. (angeloni2020designandcommissioning pages 57-63, oikonomopoulou2019materialcompositionsand pages 4-7)

A conservative operating rule is to **stop the melt/atomization sequence and retain the inert atmosphere** if visible runoff, abnormally coarse shot, collector or flange overheating, smoke, glass damage, loss of cooling, a seal leak, or unexplained oxygen rise occurs; keep the collector isolated until the equipment is safe to inspect. This is a proposed stop rule inferred from the documented blocked-outlet/shutdown experience and containment designs, **not** a manufacturer-prescribed rePOWDER procedure. ([name redacted]2017gasatomizationequipment pages 21-24, andrus1989thrustchambermaterial pages 88-91)

## Checking chamber integrity

For a *clean, dry, assembled* chamber—including its collector joints—evacuate, isolate the pump and record pressure against time. The measured gas load is **Q = V(dP/dt)** and contains both leakage and outgassing; a nearly linear sustained rise favors a real leak, whereas a rise that progressively levels off can indicate outgassing/re-adsorption. This test alone does not locate a faulty seal, and a dirty or recently heated chamber can confound it. The published pressure-rise comparison illustrates that distinction. (chung2018vacuumdiagnosisand pages 1-2, santos2005simplevacuumexperiments pages 3-4, chung2018vacuumdiagnosisand pages 2-4, chung2018vacuumdiagnosisand media b1aeea66)

Locate suspect collector flanges and other joints with an appropriately configured **helium leak detector** while applying helium locally. A published large-vessel investigation enclosed individual flange gaps and welds, introduced helium to each enclosure, corrected detector readings for gas diverted through parallel pumping, retightened leaking flanges and re-welded a defective port. Its illustrated enclosure method is useful, but its numerical joint acceptance threshold is specific to that facility. The LLNL/Arcast *atomizer design specification* instead states a whole-system leak requirement of **less than 1 × 10⁻⁶ atm·cm³/s**; the specification does not itself demonstrate that a particular machine passed testing. Set acceptance criteria and test configuration for the actual atomizer rather than transferring either example uncritically. ([name redacted]2017gasatomizationequipment pages 21-24, chung2018vacuumdiagnosisand pages 2-4, chung2018vacuumdiagnosisand pages 4-5, chung2018vacuumdiagnosisand media eee4691c)

## Trace-oxygen indication following loss of power

**No retrieved rePOWDER instruction specifies an automatic post-outage sensor check.** As a documented *analyzer-manual analogy*, the GPR-3100B oxygen analyzer performs power-on diagnostics; its manual describes allowing stabilization and calibration after installation, flushing the selected sample/calibration gas before reading, and ensuring that calibration-gas pressure and temperature are representative of the sample. Its power-failure alarm opens when power is lost. These instructions should not be represented as AMAZEMET settings or as proof that every brief outage invalidates calibration. (analyzer1992ownersmanuala pages 17-21, analyzer1992ownersmanual pages 17-21, analyzer1992ownersmanual pages 11-17)

Before relying on a restarted chamber reading to authorize a new melt, an appropriate **proposed verification** is to confirm analyzer self-test, sample flow and sampling-line integrity; check a low-oxygen reference and a suitable independent span or functional challenge under the installed analyzer manufacturer’s procedure; confirm that alarm and interlock states have returned correctly; and independently confirm chamber pressure integrity and oxygen stability after purge. Do not accept an apparently low displayed oxygen value by itself as evidence that a collector seal is sound. The available oxygen-analyzer manual supports stabilization, controlled sample presentation, zero/span calibration and attention to the power-failure alarm; the LLNL atomizer specification supports redundant oxygen monitoring, but neither supplies a universal atomizer-specific outage acceptance threshold. ([name redacted]2017gasatomizationequipment pages 21-24, analyzer1992ownersmanuala pages 17-21, analyzer1992ownersmanual pages 11-17, analyzer1992ownersmanuala pages 24-29)

References

1. (scientific2023comparisonofultrasonic pages 7-8): International Scientific, B. Bałasz, M. Bielecki, W. Gulbiński, and Ł. Słoboda. Comparison of ultrasonic and other atomization methods in metal powder production. Journal of Achievements in Materials and Manufacturing Engineering, 116:11-24, Jan 2023. URL: https://doi.org/10.5604/01.3001.0016.3393, doi:10.5604/01.3001.0016.3393. This article has 41 citations.

2. ([name redacted]2020failureanalysisof pages 1-4): A. J. [name redacted], A. J. [name redacted], L. N. [name redacted], and A. A. [name redacted]. Failure analysis of gas spray atomization crucible materials. Journal of Failure Analysis and Prevention, pages 1-6, May 2020. URL: https://doi.org/10.1007/s11668-020-00887-w, doi:10.1007/s11668-020-00887-w. This article has 0 citations.

3. (andrus1989thrustchambermaterial pages 88-91): JS Andrus and RG Bordeau. Thrust chamber material technology program. Unknown journal, 1989.

4. (salges2024processingandcharacterization pages 46-50): Sasha Alejandra Cegarra Salges. Processing and characterization of metallic glasses prepared by centrifugal atomization. ArXiv, 2024. URL: https://doi.org/10.5821/dissertation-2117-422060, doi:10.5821/dissertation-2117-422060. This article has 1 citations.

5. ([name redacted]2020failureanalysisof pages 4-10): A. J. [name redacted], A. J. [name redacted], L. N. [name redacted], and A. A. [name redacted]. Failure analysis of gas spray atomization crucible materials. Journal of Failure Analysis and Prevention, pages 1-6, May 2020. URL: https://doi.org/10.1007/s11668-020-00887-w, doi:10.1007/s11668-020-00887-w. This article has 0 citations.

6. (prichard1992spraycastx"superalloyfor pages 4-6): P.D. Prichard and R.P. Dalal. Spraycast-x'" superalloy for aerospace applications. Superalloys, pages 205-214, Jan 1992. URL: https://doi.org/10.7449/1992/superalloys\_1992\_205\_214, doi:10.7449/1992/superalloys\_1992\_205\_214. This article has 15 citations.

7. ([name redacted]2017gasatomizationequipment pages 21-24): T. [name redacted] and T. [name redacted]. Gas atomization equipment statement of work and specification for engineering design, fabrication, testing, and installation. Unknown journal, Nov 2017. URL: https://doi.org/10.2172/1411699, doi:10.2172/1411699.

8. ([name redacted]2020failureanalysisof media b6770702): A. J. [name redacted], A. J. [name redacted], L. N. [name redacted], and A. A. [name redacted]. Failure analysis of gas spray atomization crucible materials. Journal of Failure Analysis and Prevention, pages 1-6, May 2020. URL: https://doi.org/10.1007/s11668-020-00887-w, doi:10.1007/s11668-020-00887-w. This article has 0 citations.

9. (huebner2005materialselectionfor pages 5-6): Michael Huebner. Material selection for mechanical seals. ArXiv, Jan 2005. URL: https://doi.org/10.21423/r1nt1t, doi:10.21423/r1nt1t. This article has 19 citations.

10. (huebner2005materialselectionfor pages 4-5): Michael Huebner. Material selection for mechanical seals. ArXiv, Jan 2005. URL: https://doi.org/10.21423/r1nt1t, doi:10.21423/r1nt1t. This article has 19 citations.

11. (jubber1994designofa pages 3-4): M. Jubber, John I. B. Wilson, I. Drummond, P. John, and D. Milne. Design of a uhv reactor for microwave plasma deposition of diamond films. Vacuum, 45:499-506, May 1994. URL: https://doi.org/10.1016/0042-207x(94)90242-9, doi:10.1016/0042-207x(94)90242-9. This article has 37 citations and is from a peer-reviewed journal.

12. (angeloni2020designandcommissioning pages 57-63): F Angeloni. Design and commissioning of a hybrid rocket engine with optical access. Unknown journal, 2020.

13. (oikonomopoulou2019materialcompositionsand pages 4-7): Faidra Oikonomopoulou. Material compositions and production methods for solid cast glass components. Architecture and the Built Environment, Nov 2019. URL: https://doi.org/10.59490/abe.2019.9.4086, doi:10.59490/abe.2019.9.4086. This article has 2 citations.

14. (chung2018vacuumdiagnosisand pages 1-2): Taeil Chung, Jong Yeon Lim, Sangbaek Kang, Yongho Yoo, and Hyu-Soung Shin. Vacuum diagnosis and testing of a dirty thermal vacuum chamber. Applied Science and Convergence Technology, 27:120-125, Nov 2018. URL: https://doi.org/10.5757/asct.2018.27.6.120, doi:10.5757/asct.2018.27.6.120. This article has 14 citations.

15. (santos2005simplevacuumexperiments pages 3-4): J.M.F. dos Santos. Simple vacuum experiments for undergraduate student laboratories. Vacuum, 80:258-263, Oct 2005. URL: https://doi.org/10.1016/j.vacuum.2005.07.043, doi:10.1016/j.vacuum.2005.07.043. This article has 14 citations and is from a peer-reviewed journal.

16. (chung2018vacuumdiagnosisand pages 2-4): Taeil Chung, Jong Yeon Lim, Sangbaek Kang, Yongho Yoo, and Hyu-Soung Shin. Vacuum diagnosis and testing of a dirty thermal vacuum chamber. Applied Science and Convergence Technology, 27:120-125, Nov 2018. URL: https://doi.org/10.5757/asct.2018.27.6.120, doi:10.5757/asct.2018.27.6.120. This article has 14 citations.

17. (chung2018vacuumdiagnosisand media b1aeea66): Taeil Chung, Jong Yeon Lim, Sangbaek Kang, Yongho Yoo, and Hyu-Soung Shin. Vacuum diagnosis and testing of a dirty thermal vacuum chamber. Applied Science and Convergence Technology, 27:120-125, Nov 2018. URL: https://doi.org/10.5757/asct.2018.27.6.120, doi:10.5757/asct.2018.27.6.120. This article has 14 citations.

18. (chung2018vacuumdiagnosisand pages 4-5): Taeil Chung, Jong Yeon Lim, Sangbaek Kang, Yongho Yoo, and Hyu-Soung Shin. Vacuum diagnosis and testing of a dirty thermal vacuum chamber. Applied Science and Convergence Technology, 27:120-125, Nov 2018. URL: https://doi.org/10.5757/asct.2018.27.6.120, doi:10.5757/asct.2018.27.6.120. This article has 14 citations.

19. (chung2018vacuumdiagnosisand media eee4691c): Taeil Chung, Jong Yeon Lim, Sangbaek Kang, Yongho Yoo, and Hyu-Soung Shin. Vacuum diagnosis and testing of a dirty thermal vacuum chamber. Applied Science and Convergence Technology, 27:120-125, Nov 2018. URL: https://doi.org/10.5757/asct.2018.27.6.120, doi:10.5757/asct.2018.27.6.120. This article has 14 citations.

20. (analyzer1992ownersmanuala pages 17-21): HF Analyzer. Owner's manual. Unknown journal, 1992.

21. (analyzer1992ownersmanual pages 17-21): HF Analyzer. Owner's manual. Unknown journal, 1992.

22. (analyzer1992ownersmanual pages 11-17): HF Analyzer. Owner's manual. Unknown journal, 1992.

23. (analyzer1992ownersmanuala pages 24-29): HF Analyzer. Owner's manual. Unknown journal, 1992.
