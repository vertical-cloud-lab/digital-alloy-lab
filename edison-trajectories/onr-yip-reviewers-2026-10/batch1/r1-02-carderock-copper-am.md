<!--
Edison Scientific LITERATURE task (batch 1)
- Task ID: b34e5c11-1cc8-4a0a-b262-f253aed4728f
- Submitted: 2026-10-24T05:25:55Z
- Fetched: 2026-10-24T05:57:56Z (status: success)
- Raw trajectory JSON: not committed here (see ../README.md); r1-02-carderock-copper-am.json.gz in the agent-staging drop
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal for the Materials &
Processes for Additive Manufacturing program (ONR Code 332). The work designs
new pre-alloyed copper alloy powders for single-stream blown-powder laser
directed energy deposition (DED). Goals: deposits that are dense and
crack-free, both built on themselves and deposited on cast nickel-aluminum
bronze (NAB) and wrought Cu-Ni (repair), and that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe, Mn, Cr; aluminum
bronzes / NAB with Ni, Fe, Mn. Lower nickel content is a secondary objective.
Powder is made in-house by ultrasonic atomization. Method: composition ->
powder -> DED deposit -> microstructure -> corrosion/hardness is a network of
linked models searched by cost-aware Bayesian optimization (cheap steps such
as CALPHAD, pre-placed powder tracks and one-hour electrochemical screens are
run more often than expensive ones such as 2 kg blown-powder builds and
30-day immersion). CALPHAD is evaluated along a heat-flow model of the DED
thermal history. Purchased DED sessions run at outside facilities.

QUESTION: Who at NSWC Carderock Division (and NSWC Philadelphia) has
published on additive manufacturing, welding, heat treatment or seawater
corrosion of copper alloys (NAB, Cu-Ni, manganese-aluminum bronze) since
2015? Include S. M. Orzolek, J. K. Semple, J. E. Norkett, J. H. Canaday and
others the literature turns up. For each, give the papers and what they
measured. What questions do these papers leave open, and which of them does
a cost-aware search for as-deposited DED copper alloys answer? Which of
their datasets or property databases could the proposal use as inputs or
benchmarks? What would this group count as convincing evidence that a new
composition deserves Navy qualification testing?

OUTPUT FORMAT: First, a short profile built only from the published record
(papers, technical reports, conference talks, program pages): positions and
affiliations with years, main research topics, methods, and recurring
co-authors. Then the publications most relevant to the proposal, each with a
full citation and DOI and one line on what it found. Then 3-6 numbered
IMPLICATIONS for the proposal: what this reader is likely to value, what they
would probe or doubt, which of their own results the proposal should cite or
build on, and wording or framing that would land well or badly with them.
Tag claims that rest on a single source or on a program web page rather than
a peer-reviewed paper. If the record is thin or a name is ambiguous (several
people share it), say so plainly instead of guessing, and do not invent
affiliations, titles or papers.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications) is
writing an ONR FY2027 Young Investigator Program proposal for the Materials &
Processes for Additive Manufacturing program (ONR Code 332). The work designs
new pre-alloyed copper alloy powders for single-stream blown-powder laser
directed energy deposition (DED). Goals: deposits that are dense and
crack-free, both built on themselves and deposited on cast nickel-aluminum
bronze (NAB) and wrought Cu-Ni (repair), and that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe, Mn, Cr; aluminum
bronzes / NAB with Ni, Fe, Mn. Lower nickel content is a secondary objective.
Powder is made in-house by ultrasonic atomization. Method: composition ->
powder -> DED deposit -> microstructure -> corrosion/hardness is a network of
linked models searched by cost-aware Bayesian optimization (cheap steps such
as CALPHAD, pre-placed powder tracks and one-hour electrochemical screens are
run more often than expensive ones such as 2 kg blown-powder builds and
30-day immersion). CALPHAD is evaluated along a heat-flow model of the DED
thermal history. Purchased DED sessions run at outside facilities.

QUESTION: Who at NSWC Carderock Division (and NSWC Philadelphia) has
published on additive manufacturing, welding, heat treatment or seawater
corrosion of copper alloys (NAB, Cu-Ni, manganese-aluminum bronze) since
2015? Include S. M. Orzolek, J. K. Semple, J. E. Norkett, J. H. Canaday and
others the literature turns up. For each, give the papers and what they
measured. What questions do these papers leave open, and which of them does
a cost-aware search for as-deposited DED copper alloys answer? Which of
their datasets or property databases could the proposal use as inputs or
benchmarks? What would this group count as convincing evidence that a new
composition deserves Navy qualification testing?

OUTPUT FORMAT: First, a short profile built only from the published record
(papers, technical reports, conference talks, program pages): positions and
affiliations with years, main research topics, methods, and recurring
co-authors. Then the publications most relevant to the proposal, each with a
full citation and DOI and one line on what it found. Then 3-6 numbered
IMPLICATIONS for the proposal: what this reader is likely to value, what they
would probe or doubt, which of their own results the proposal should cite or
build on, and wording or framing that would land well or badly with them.
Tag claims that rest on a single source or on a program web page rather than
a peer-reviewed paper. If the record is thin or a name is ambiguous (several
people share it), say so plainly instead of guessing, and do not invent
affiliations, titles or papers.


## Published-record profile

**The identifiable Carderock network is principally a materials-characterization and computational-welding network, not a documented powder-alloy-optimization team.** A 2022 article places Jennifer K. Semple, Daniel H. Bechetti, and Charles R. Fisher at the Naval Surface Warfare Center, Carderock Division (NSWCCD), West Bethesda, Maryland, and identifies its Welding, Processing, and Nondestructive Evaluation Branch; Wei Zhang was at Ohio State. Semple’s 2018 Ohio State welding-engineering thesis documents her graduate affiliation then and thanks Fisher and Bechetti of Carderock. These records do **not** establish individual Navy job titles or continuous employment dates. Their recurring work concerns pedigreed temperature-dependent properties, weld thermal cycles, phase transformations, residual stress, and distortion. (semple2022temperaturedependentmaterialproperty pages 1-2, semple2022temperaturedependentmaterialproperty pages 2-4, semple2018pedigreedmaterialproperty pages 1-8)

Sean M. Orzolek published a NAB processing/microstructure paper with Semple and Fisher in 2022, and a C63200 plate property-database paper with Justin E. Norkett and Fisher in 2023. Bibliographic records also identify Norkett and Fisher on cast 70/30 Cu–Ni (2025) and 90/10 Cu–Ni plate (2026) databases, and Norkett, Jack H. Canaday, Orzolek, and Fisher on a 2026 wire-arc NAB-component database. **[Bibliographic-record only]** The latter papers’ full texts were unavailable here: their precise measurements, data-access provisions, individual affiliations, and individual positions cannot be verified. A 2021 Carderock-attributed NAB additive-manufacturing/weldability review is cited in later literature, but its report number, DOI, and contents were not recovered. Glenn W. Hatala, Qian Wang, and Edward W. Reutzel are *Penn State collaborators*, not identified here as Navy employees; their 2021 paper includes Fisher and Semple. (camilleri2025coldsprayas pages 13-14, hatala2024aninvestigationof pages 16-17, hatala2024aninvestigationof pages 1-2)

**The directly verified Carderock corrosion author is K. L. Vasanth:** the 2017 paper gives his affiliation as NSWCCD, Code 613, West Bethesda, alongside Mariano Iannuzzi and Gerald S. Frankel at non-Navy institutions. No retrieved publication establishes a particular copper-alloy researcher at **NSWC Philadelphia Division**, or connects the named authors to that division; assigning one would be speculation. Nor does the accessible Carderock record demonstrate a manganese–aluminum-bronze corrosion paper. (iannuzzi2017unusualcorrelationbetween pages 1-2, luca2025correlationofsolidification pages 1-3)

## Publications most relevant to the proposal

**Directly inspected papers or independently corroborated citations**

- M. Iannuzzi, K. L. Vasanth, and G. S. Frankel, “Unusual Correlation between SKPFM and Corrosion of Nickel Aluminum Bronzes,” *Journal of The Electrochemical Society* **164** (2017), C488–C497. DOI: **10.1149/2.0391709jes**. On wrought/heat-treated C63200, they measured phase-resolved topography and air Volta potential alongside exposure to NaCl or ammoniacal chloride and electrochemical polarization: Cu-rich α preferentially dissolved while κ particles remained apparently unattacked; an air SKPFM potential ranking did **not** reliably predict solution corrosion. (iannuzzi2017unusualcorrelationbetween pages 1-2, iannuzzi2017unusualcorrelationbetween pages 6-8, iannuzzi2017unusualcorrelationbetween pages 9-10)
- G. W. Hatala, Q. Wang, E. W. Reutzel, C. R. Fisher, and J. K. Semple, “A Thermo-Mechanical Analysis of Laser Hot Wire Additive Manufacturing of NAB,” *Metals* **11** (2021), 1023. DOI: **10.3390/met11071023**. The published abstract reports measurements of temperature-dependent thermal and mechanical properties for NAB C95800 and simulations of laser-hot-wire deposition distortion; substituting constant room-temperature properties substantially changed predictions and could reverse predicted substrate-deflection direction. **[Abstract/reference-list verification; full article inaccessible here.]** (hatala2024aninvestigationof pages 16-17)
- S. M. Orzolek, J. K. Semple, and C. R. Fisher, “Influence of Processing on the Microstructure of Nickel Aluminum Bronze (NAB),” *Additive Manufacturing* **56** (2022), 102859. DOI: **10.1016/j.addma.2022.102859**. Its documented subject is the processing–microstructure relationship in NAB; **[citation-only]** the accessible references do not establish which process conditions, phases, hardness values, or corrosion tests it measured, so no stronger finding is attributed to it. (heniken2025influenceofmicrostructured pages 54-55, hatala2024aninvestigationof pages 16-17)
- J. K. Semple, D. H. Bechetti, W. Zhang, and C. R. Fisher, “Temperature-Dependent Material Property Databases for Marine Steels—Part 3: HSLA-80,” *Integrating Materials and Manufacturing Innovation* **11** (2022), 648–674. DOI: **10.1007/s40192-022-00288-x**. **Methodological precedent, not a copper dataset:** it measured a pedigreed plate’s composition, thermal diffusivity, heat capacity, expansion, elevated-temperature mechanical response, and heat-affected-zone transformation behavior for weld-model inputs; the authors explicitly limit extrapolation from the single plate. Raw files and micrographs are identified at Materials Commons, dataset DOI **10.13011/m3-cz82-dw37**. (semple2022temperaturedependentmaterialproperty pages 1-2, semple2022temperaturedependentmaterialproperty pages 2-4, semple2022temperaturedependentmaterialproperty pages 24-26)

**Relevant Carderock-associated publications located bibliographically, but not available for substantive full-text checking**

- S. M. Orzolek, J. E. Norkett, and C. R. Fisher, “Temperature-Dependent Material Property Database for C63200 Nickel-Aluminum Bronze (NAB) Plate,” *Integrating Materials and Manufacturing Innovation* **12** (2023), 481–492. DOI: **10.1007/s40192-023-00325-3**. **[Bibliographic-record only]** A potentially useful *plate* property benchmark; the precise measured fields and repository cannot be confirmed here. The alloy/product form must not be silently equated with cast C95800 or a DED deposit. (iannuzzi2017unusualcorrelationbetween pages 1-2, semple2022temperaturedependentmaterialproperty pages 1-2)
- J. E. Norkett and C. R. Fisher, “Temperature-Dependent Material Property Database of Cast 70/30 Cu-Ni Material,” *Integrating Materials and Manufacturing Innovation* (2025). DOI: **10.1007/s40192-025-00409-2**. **[Bibliographic-record only]** Candidate *cast* 70/30 Cu–Ni thermophysical/mechanical input, **not** an established seawater-corrosion or wrought-C71500 performance dataset; volume/pages and measured fields were not verified.
- J. E. Norkett and C. R. Fisher, “Temperature-Dependent Material Property Database for 90/10 Cu-Ni Plate,” *Integrating Materials and Manufacturing Innovation* **15** (2026), 169–180. DOI: **10.1007/s40192-026-00444-7**. **[Bibliographic-record only]** Candidate plate-property input for the lower-Ni branch; not direct evidence that 90/10 equals 70/30 in seawater.
- J. E. Norkett, J. H. Canaday, S. M. Orzolek, and C. R. Fisher, “Temperature-Dependent Material Property Database for Nickel-Aluminum Bronze (NAB) Wire-Arc Additive Components,” *Integrating Materials and Manufacturing Innovation* (2026). DOI: **10.1007/s40192-026-00454-5**. **[Bibliographic-record only]** Particularly promising *AM-component* benchmark for testing property-model transfer; its product is wire-arc, not single-stream blown-powder laser DED. Canaday’s individual position and other publications could not be substantiated.

For comparison rather than attribution to Carderock, G. W. Hatala, E. Reutzel, and Q. Wang, “An Investigation of Thermomechanical Behavior in Laser Hot Wire Directed Energy Deposition of NAB: Finite Element Analysis and Experimental Validation,” *Metals* **14** (2024), 1143, DOI **10.3390/met14101143**, measured in-situ substrate temperature histories and free-end displacement on single- and multilayer builds. Their Table 10 reports maximum thermocouple errors of **3%, 5%, 5%** and final-distortion error **12%** for single-layer, versus **3%, 6%, 2%** and **3.6%** for multilayer; a model with stress relaxation at 500 °C better reproduced the latter’s limited distortion accumulation. These are a process-model validation precedent, **not Navy-authored seawater-qualification data**. (hatala2024aninvestigationof pages 1-2, hatala2024aninvestigationof media ad20ce4b, hatala2024aninvestigationof pages 15-16)

## Implications for the proposal

1. **Frame the advance as the missing linked *composition → powder → as-deposited repair → seawater* dataset.** Carderock’s documented work supplies thermal-property, phase-history, distortion, and local-corrosion precedents, but the inspected studies do not establish an optimized pre-alloyed powder that forms dense, crack-free laser-DED deposits both on itself and on cast NAB/wrought Cu–Ni **and** matches wrought C71500 corrosion without post-build treatment. Explicitly distinguish these untested conjunctions from claims that DED NAB or Cu–Ni has never been studied. Present lower Ni as a constrained secondary objective rather than a presumed corrosion benefit. (semple2022temperaturedependentmaterialproperty pages 1-2, hatala2024aninvestigationof pages 2-4, iannuzzi2017unusualcorrelationbetween pages 9-10)

2. **Validate the thermal-to-phase link, not merely CALPHAD equilibrium.** The 2021 Navy-coauthored LHW study reports sensitivity to *temperature-dependent* properties; the independent 2024 validation demonstrates why thermocouple histories, layer dwell, transformations, and distortion matter. Use Carderock’s C95800/C63200 and candidate Cu–Ni and wire-arc NAB property papers **after obtaining and checking each dataset’s actual contents and permissions**; document feedstock chemistry, measured powder chemistry, substrate/product form, heating/cooling history, and uncertainty. Do not transfer a cast or wire-arc curve to laser-powder DED without validation. The HSLA-80 Materials Commons dataset supplies a *data-pedigree and public-release template*, not copper-alloy values. (semple2022temperaturedependentmaterialproperty pages 1-2, semple2022temperaturedependentmaterialproperty pages 2-4, semple2022temperaturedependentmaterialproperty pages 24-26, hatala2024aninvestigationof pages 16-17)

3. **Make rapid electrochemistry a screen, never the qualification endpoint.** Vasanth and coauthors demonstrate phase-selective attack and that ex-situ air SKPFM can give the *wrong* corrosion ranking in solution. Specify matched as-deposited surfaces and appropriate polished controls, cross-sections through the fusion/dilution zone, reproducible electrochemical protocols, and confirmation by longer immersion with localized-attack maps and mass-loss measurements alongside wrought C71500 and the actual substrates. Distinguish one-hour rank predictions from measured 30-day outcomes, including rank reversals; avoid saying a high open-circuit potential or a low single-scan current proves seawater equivalence. (iannuzzi2017unusualcorrelationbetween pages 6-8, iannuzzi2017unusualcorrelationbetween pages 9-10, iannuzzi2017unusualcorrelationbetween pages 2-3)

4. **Show that cost-aware optimization survives expensive, independent tests.** Pre-register a constrained acquisition policy and compare it against feasible baselines on *total dollars and DED-session hours to a confirmed candidate*, not number of cheap tracks screened. An independently made powder lot and an outside-facility blown-powder build should verify density/defects by volumetric inspection and serial sections, hardness and phase constitution across deposit/HAZ/interface, reproducibility across orientation and builds, and galvanic/local corrosion at both NAB and Cu–Ni repair interfaces. Heat-treated samples can be mechanistic controls but must not rescue an as-deposited primary claim. **This is a proposed evidentiary standard, not a published Navy qualification rule.** (semple2022temperaturedependentmaterialproperty pages 2-4, hatala2024aninvestigationof pages 15-16, iannuzzi2017unusualcorrelationbetween pages 9-10)

5. **Describe the outcome as a *candidate for Navy qualification testing*, not Navy qualification.** Persuasive evidence would combine traceable powder lots and compositions; replicated defect-free self-build and both specified dissimilar-substrate repairs; independently validated heat-flow/phase predictions; corrosion comparisons using simultaneously exposed wrought 70/30 Cu–Ni controls with uncertainty and interface-localization analysis; and an explicit plan for later tensile, fatigue, cavitation/erosion, environmental and scale-up testing as appropriate to the component. Carderock’s own steel-property paper emphasizes the limitations of one material heat, while the 2024 NAB thermal study acknowledges limited repetition. A claim of universal seawater superiority or of qualification from hardness, a short polarization scan, or a single successful coupon would overreach. **This is an inference from the published methods and limitations, not a statement by individual Navy reviewers.** (semple2022temperaturedependentmaterialproperty pages 2-4, hatala2024aninvestigationof pages 15-16, iannuzzi2017unusualcorrelationbetween pages 1-2)

**Source limitation:** Four copper-alloy database articles above were found as bibliographic metadata but could not be inspected in full. Their titles/DOIs identify acquisition priorities, not verified variable lists, numerical findings, open-data status, or personnel assignments. No program-page claim or NSWC Philadelphia affiliation was used to fill that gap.

References

1. (semple2022temperaturedependentmaterialproperty pages 1-2): Jennifer K. Semple, Daniel H. Bechetti, Wei Zhang, and Charles R. Fisher. Temperature-dependent material property databases for marine steels—part 3: hsla-80. Integrating Materials and Manufacturing Innovation, 11:648-674, Nov 2022. URL: https://doi.org/10.1007/s40192-022-00288-x, doi:10.1007/s40192-022-00288-x. This article has 10 citations and is from a peer-reviewed journal.

2. (semple2022temperaturedependentmaterialproperty pages 2-4): Jennifer K. Semple, Daniel H. Bechetti, Wei Zhang, and Charles R. Fisher. Temperature-dependent material property databases for marine steels—part 3: hsla-80. Integrating Materials and Manufacturing Innovation, 11:648-674, Nov 2022. URL: https://doi.org/10.1007/s40192-022-00288-x, doi:10.1007/s40192-022-00288-x. This article has 10 citations and is from a peer-reviewed journal.

3. (semple2018pedigreedmaterialproperty pages 1-8): JK Semple. Pedigreed material property data for residual stress and distortion modeling of naval steel weldments. Unknown journal, 2018.

4. (camilleri2025coldsprayas pages 13-14): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

5. (hatala2024aninvestigationof pages 16-17): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

6. (hatala2024aninvestigationof pages 1-2): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

7. (iannuzzi2017unusualcorrelationbetween pages 1-2): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

8. (luca2025correlationofsolidification pages 1-3): Ricardo de Luca, Paulo Henrique Tedardi do Nascimento, Vinicius Torres dos Santos, Marcio Rodrigues da Silva, Flavia Gonçalves Lobo, Rogerio Teram, Mauricio Silva Nascimento, Antonio Augusto Couto, Anibal de Andrade Mendes Filho, and Givanildo Alves dos Santos. Correlation of solidification thermal variables with microstructure and hardness in cumn11al8fe3ni3 manganese–aluminum–bronze alloy. Materials, 18:234, Jan 2025. URL: https://doi.org/10.3390/ma18020234, doi:10.3390/ma18020234. This article has 1 citations.

9. (iannuzzi2017unusualcorrelationbetween pages 6-8): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

10. (iannuzzi2017unusualcorrelationbetween pages 9-10): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

11. (heniken2025influenceofmicrostructured pages 54-55): NH Heniken. Influence of microstructure on fatigue behavior, crack initiation, and crack growth in wire-arc additively manufactured nickel aluminum-bronze. Unknown journal, 2025.

12. (semple2022temperaturedependentmaterialproperty pages 24-26): Jennifer K. Semple, Daniel H. Bechetti, Wei Zhang, and Charles R. Fisher. Temperature-dependent material property databases for marine steels—part 3: hsla-80. Integrating Materials and Manufacturing Innovation, 11:648-674, Nov 2022. URL: https://doi.org/10.1007/s40192-022-00288-x, doi:10.1007/s40192-022-00288-x. This article has 10 citations and is from a peer-reviewed journal.

13. (hatala2024aninvestigationof media ad20ce4b): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

14. (hatala2024aninvestigationof pages 15-16): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

15. (hatala2024aninvestigationof pages 2-4): Glenn W. Hatala, Edward Reutzel, and Qian Wang. An investigation of thermomechanical behavior in laser hot wire directed energy deposition of nab: finite element analysis and experimental validation. Metals, 14:1143, Oct 2024. URL: https://doi.org/10.3390/met14101143, doi:10.3390/met14101143. This article has 4 citations.

16. (iannuzzi2017unusualcorrelationbetween pages 2-3): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.
