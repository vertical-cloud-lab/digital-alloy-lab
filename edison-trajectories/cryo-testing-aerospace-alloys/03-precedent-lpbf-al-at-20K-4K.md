<!--
Edison Scientific PRECEDENT (job-futurehouse-paperqa3-precedent)
Task ID: 3ccea3dc-454b-4b67-818a-50d167d91589
Submitted: 2026-11-12T16:41:11Z; fetched: 2026-11-12T16:59:24Z; status: success; has_successful_answer: True
Retrieved with edison-client 0.18.0 (EDISON_PLATFORM_API_KEY) from GitHub Actions for issue #254. The full trajectory is in the .trajectory.json file beside this one.
-->

**Question (PRECEDENT):** Has anyone measured tensile, fracture-toughness or fatigue properties of laser powder bed fusion (LPBF / selective laser melting) aluminum alloys, such as AlSi10Mg, Scalmalloy, A20X or other AM aluminum alloys, at liquid-hydrogen (about 20 K) or liquid-helium (about 4 K) temperature, rather than only at 77 K?

---

Question: Has anyone measured tensile, fracture-toughness or fatigue properties of laser powder bed fusion (LPBF / selective laser melting) aluminum alloys, such as AlSi10Mg, Scalmalloy, A20X or other AM aluminum alloys, at liquid-hydrogen (about 20 K) or liquid-helium (about 4 K) temperature, rather than only at 77 K?

Yes. ## Answer

**Yes—tensile properties have been measured at liquid-hydrogen temperature, not just at 77 K.** Adams, Rinauro and Leachman reported direct **20 K tensile tests in liquid hydrogen** on selective-laser-melted AlSi10Mg and A6061-RAM2 (DOI: **10.1088/1757-899X/1302/1/012006**). The underlying Washington State University thesis identifies an EOS M290 as the machine used to make both aluminum materials; it is therefore an LPBF/SLM study. Five specimens of each alloy were tested in each of two build orientations. The thesis is dated May 2022 on its title page, although its repository record is indexed as 2023; the 2024 paper reports the same results rather than a second independent campaign. (adams2023materialandscan pages 1-8, adams2023materialandscan pages 33-37, adams2024ultimatetensilestrengths pages 1-3, adams2024ultimatetensilestrengths pages 3-5)

The measured 20 K ultimate tensile strengths (UTS) and elastic moduli are summarized below; the uncertainties are **standard errors**, not standard deviations. The authors state that the specimens equilibrated overnight at 20 K before testing. (adams2024ultimatetensilestrengths pages 3-5, adams2024ultimatetensilestrengths pages 5-8, adams2024ultimatetensilestrengths media b6484a21)

| SLM/LPBF alloy | Orientation | Mean UTS (MPa) ± SE | Mean Young’s modulus (GPa) ± SE | *n* |
|---|---:|---:|---:|---:|
| AlSi10Mg | XY | 483 ± 21 | 73.5 ± 4.70 | 5 |
| AlSi10Mg | ZX | 512 ± 43 | 65.1 ± 3.30 | 5 |
| A6061-RAM2 | XY | 568 ± 16 | 76.1 ± 0.65 | 5 |
| A6061-RAM2 | ZX | 516 ± 41 | 77.8 ± 2.76 | 5 |
| **Test/source** | **Liquid hydrogen, 20 K** | **Direct tensile testing** | **Adams et al. (2024), Table 4** | **(adams2024ultimatetensilestrengths pages 3-5, adams2024ultimatetensilestrengths pages 5-8, adams2024ultimatetensilestrengths media b6484a21)** |


*Table: Direct liquid-hydrogen tensile results from Adams, Rinauro, and Leachman (2024), Table 4, DOI 10.1088/1757-899X/1302/1/012006. These are tensile-strength and elastic-modulus measurements—not fatigue or fracture-toughness tests.*

**What remains unverified at approximately 4 K:** I did not find a published, specimen-level **4–4.2 K tensile, fracture-toughness or fatigue result** for an LPBF aluminum alloy, nor a verified **20 K fracture-toughness or fatigue result**. This is a limit of the located literature, not proof that no laboratory has performed such tests. Despite its name, the *Cryogenic Accelerated Fatigue Tester* was used for **tensile** testing of the aluminum specimens in the Adams study; the paper reports UTS and modulus, not aluminum fatigue life or fracture toughness. It also reports no aluminum elongation because the strain-gauge range was exceeded. (adams2024ultimatetensilestrengths pages 3-5, adams2024ultimatetensilestrengths pages 5-8)

Several close-looking reports do not establish the requested properties at 20 or 4 K:

- **Scalmalloy:** Rehme and Weidermann describe SLM Scalmalloy specimens and say initial cryogenic tests gave unsatisfactory results, leading them to drop planned additional tensile and low-cycle-fatigue specimens. They provide neither the Scalmalloy test temperature nor quantitative mechanical results, so the report cannot establish a 20 K or 4 K property. Weiss and colleagues measured SLM Scalmalloy **thermophysical** properties down to about 4 K—including conductivity, thermal expansion and heat capacity—not the requested mechanical properties. (rehme2024additivemanufacturingof pages 1-3, rehme2024additivemanufacturingof pages 6-9, rehme2024additivemanufacturingof pages 9-9, weiss2024cryogenicthermophysicalproperties pages 6-9, weiss2024cryogenicthermophysicalproperties pages 9-11)
- **A205/A20X-family alloy:** Tumulu reports LPBF A205 tensile and instrumented Charpy-impact measurements at **−196 °C (approximately 77 K)**. Charpy absorbed energy is not a standard fracture-toughness value, and these tests are not at 20 or 4 K. (tumulu2025laserpowderbed pages 166-169, tumulu2025laserpowderbed pages 158-162)

**Bottom line:** the answer is **yes for LPBF aluminum tensile strength and modulus at 20 K**, with directly reported data for **AlSi10Mg and A6061-RAM2**. A measured LPBF-aluminum **4 K tensile property**, or **20/4 K fracture-toughness or fatigue property**, was not substantiated by the sources located. (adams2023materialandscan pages 33-37, adams2024ultimatetensilestrengths pages 3-5, adams2024ultimatetensilestrengths pages 5-8, adams2024ultimatetensilestrengths media b6484a21)

References

1. (adams2023materialandscan pages 1-8): Reece Michael Adams. Material and scan spacing variation for improved mechanical performance of additively manufactured materials at cryogenic temperatures. Text, Jan 2023. URL: https://doi.org/10.7273/000004509, doi:10.7273/000004509. This article has 2 citations and is from a peer-reviewed journal.

2. (adams2023materialandscan pages 33-37): Reece Michael Adams. Material and scan spacing variation for improved mechanical performance of additively manufactured materials at cryogenic temperatures. Text, Jan 2023. URL: https://doi.org/10.7273/000004509, doi:10.7273/000004509. This article has 2 citations and is from a peer-reviewed journal.

3. (adams2024ultimatetensilestrengths pages 1-3): R. Adams, G. Rinauro, and J. Leachman. Ultimate tensile strengths and elastic moduli at 20 k of additively manufactured pa840-gsl, a6061-ram2, and alsi10mg. IOP Conference Series: Materials Science and Engineering, 1302:012006, May 2024. URL: https://doi.org/10.1088/1757-899x/1302/1/012006, doi:10.1088/1757-899x/1302/1/012006. This article has 0 citations.

4. (adams2024ultimatetensilestrengths pages 3-5): R. Adams, G. Rinauro, and J. Leachman. Ultimate tensile strengths and elastic moduli at 20 k of additively manufactured pa840-gsl, a6061-ram2, and alsi10mg. IOP Conference Series: Materials Science and Engineering, 1302:012006, May 2024. URL: https://doi.org/10.1088/1757-899x/1302/1/012006, doi:10.1088/1757-899x/1302/1/012006. This article has 0 citations.

5. (adams2024ultimatetensilestrengths pages 5-8): R. Adams, G. Rinauro, and J. Leachman. Ultimate tensile strengths and elastic moduli at 20 k of additively manufactured pa840-gsl, a6061-ram2, and alsi10mg. IOP Conference Series: Materials Science and Engineering, 1302:012006, May 2024. URL: https://doi.org/10.1088/1757-899x/1302/1/012006, doi:10.1088/1757-899x/1302/1/012006. This article has 0 citations.

6. (adams2024ultimatetensilestrengths media b6484a21): R. Adams, G. Rinauro, and J. Leachman. Ultimate tensile strengths and elastic moduli at 20 k of additively manufactured pa840-gsl, a6061-ram2, and alsi10mg. IOP Conference Series: Materials Science and Engineering, 1302:012006, May 2024. URL: https://doi.org/10.1088/1757-899x/1302/1/012006, doi:10.1088/1757-899x/1302/1/012006. This article has 0 citations.

7. (rehme2024additivemanufacturingof pages 1-3): O. Rehme and C. Weidermann. Additive manufacturing of cryogenic materials. IOP Conference Series: Materials Science and Engineering, 1301:012047, May 2024. URL: https://doi.org/10.1088/1757-899x/1301/1/012047, doi:10.1088/1757-899x/1301/1/012047. This article has 2 citations.

8. (rehme2024additivemanufacturingof pages 6-9): O. Rehme and C. Weidermann. Additive manufacturing of cryogenic materials. IOP Conference Series: Materials Science and Engineering, 1301:012047, May 2024. URL: https://doi.org/10.1088/1757-899x/1301/1/012047, doi:10.1088/1757-899x/1301/1/012047. This article has 2 citations.

9. (rehme2024additivemanufacturingof pages 9-9): O. Rehme and C. Weidermann. Additive manufacturing of cryogenic materials. IOP Conference Series: Materials Science and Engineering, 1301:012047, May 2024. URL: https://doi.org/10.1088/1757-899x/1301/1/012047, doi:10.1088/1757-899x/1301/1/012047. This article has 2 citations.

10. (weiss2024cryogenicthermophysicalproperties pages 6-9): Klaus-Peter Weiss, Nadezda Bagrets, and Camelia Schulz. Cryogenic thermo-physical properties of additive manufactured materials. IOP Conference Series: Materials Science and Engineering, 1302:012005, May 2024. URL: https://doi.org/10.1088/1757-899x/1302/1/012005, doi:10.1088/1757-899x/1302/1/012005. This article has 4 citations.

11. (weiss2024cryogenicthermophysicalproperties pages 9-11): Klaus-Peter Weiss, Nadezda Bagrets, and Camelia Schulz. Cryogenic thermo-physical properties of additive manufactured materials. IOP Conference Series: Materials Science and Engineering, 1302:012005, May 2024. URL: https://doi.org/10.1088/1757-899x/1302/1/012005, doi:10.1088/1757-899x/1302/1/012005. This article has 4 citations.

12. (tumulu2025laserpowderbed pages 166-169): SK Tumulu. Laser powder bed fusion additive manufacturing (lpbf-am) of aluminum-copper alloys. Unknown journal, 2025.

13. (tumulu2025laserpowderbed pages 158-162): SK Tumulu. Laser powder bed fusion additive manufacturing (lpbf-am) of aluminum-copper alloys. Unknown journal, 2025.
