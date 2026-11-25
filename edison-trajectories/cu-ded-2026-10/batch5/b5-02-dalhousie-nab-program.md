<!--
Edison Scientific LITERATURE task (batch 5)
- Task ID: b45018d6-acf4-4651-90d6-490f52bcf3ab
- Submitted: 2026-10-17T06:20:04Z
- Fetched: 2026-10-17T06:42:01Z (status: success)
- Raw trajectory JSON: ../raw/b5-02-dalhousie-nab-program.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: Summarize the Dalhousie University program on additively
manufactured nickel-aluminum bronze (D. P. Bishop, A. Nasiri, A. J. Rayner,
K. Morshed-Behbahani, K. A. Timmons and co-workers), with numbers:
Morshed-Behbahani et al., Colloids Surf. A 708 (2025) 136069 (heat-treated
NAB by L-PBF vs L-DED, corrosion); Morshed-Behbahani et al., Corros. Sci.
228 (2024) 111846 (unusual electrochemical corrosion of LPBF NAB); Rayner et
al., COM 2024 (DED of C63020 powder) and the companion arc-DED heat
treatment paper; the 2025 CIRP J. Manuf. Sci. Technol. surface
post-treatment study; and Timmons et al. 2025 (LPBF C64200). Which process
gave better corrosion resistance and why, what were the powders (size,
source), and who funds the program (e.g. Canadian Department of National
Defence)?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Manufacturing Engineering, Brigham Young University; EXCLUDE the
PI's own publications) is writing an ONR FY2027 Young Investigator Program
proposal for the Materials & Processes for Additive Manufacturing program.
The work designs new pre-alloyed copper alloy powders for single-stream
blown-powder laser directed energy deposition (DED; one pre-alloyed powder
feed, not in-situ blending of elemental powders). Goals: deposits that are
dense and crack-free, both built on themselves and deposited on cast
nickel-aluminum bronze (NAB) and wrought Cu-Ni (repair), and that resist
seawater AS DEPOSITED (no post-build heat treatment) at least as well as
wrought 70-30 Cu-Ni (C71500). Alloy families: Cu-Ni (10-30 wt% Ni) with Fe,
Mn, Cr additions; aluminum bronzes / NAB with Ni, Fe, Mn. A secondary
objective is lower nickel content (nickel is a US critical mineral). Powder is
made in-house by ultrasonic atomization (AMAZEMET rePOWDER, induction
melting); size, Hall flow, apparent density and oxygen are measured per lot.
Method: the composition -> powder -> DED deposit -> microstructure ->
corrosion/hardness pipeline is a network of linked surrogate models searched
by cost-aware Bayesian optimization of function networks (cheap nodes such as
CALPHAD and short electrochemical tests are queried more often than expensive
ones such as 30-day immersion). ICME element: CALPHAD (Thermo-Calc) evaluated
along a heat-flow model of the DED thermal history, tested against
equilibrium-only CALPHAD and against no physics.

QUESTION: Summarize the Dalhousie University program on additively
manufactured nickel-aluminum bronze (D. P. Bishop, A. Nasiri, A. J. Rayner,
K. Morshed-Behbahani, K. A. Timmons and co-workers), with numbers:
Morshed-Behbahani et al., Colloids Surf. A 708 (2025) 136069 (heat-treated
NAB by L-PBF vs L-DED, corrosion); Morshed-Behbahani et al., Corros. Sci.
228 (2024) 111846 (unusual electrochemical corrosion of LPBF NAB); Rayner et
al., COM 2024 (DED of C63020 powder) and the companion arc-DED heat
treatment paper; the 2025 CIRP J. Manuf. Sci. Technol. surface
post-treatment study; and Timmons et al. 2025 (LPBF C64200). Which process
gave better corrosion resistance and why, what were the powders (size,
source), and who funds the program (e.g. Canadian Department of National
Defence)?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition,
wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought), the alloy
composition in wt%, the test conditions (e.g. 3.5 wt% NaCl vs natural or
substitute seawater per ASTM D1141, duration, flow), and the key numbers
(porosity/density, corrosion current density or rate, Ecorr, impedance,
selective-attack depth, hardness, strength/elongation, powder size/flow/
oxygen). Tag each item: [CITE] worth citing; [NUMBERS] gives a quantitative
benchmark; [NAVY] Navy/DoD-funded or Navy application; [NOVELTY-RISK] overlaps
the proposed work (say how); [GAP] shows something not yet done. If the
literature does not answer part of the question, say so plainly instead of
padding with loosely related work. End with a ranked "Top 5 things the PI
should know" list.


## Dalhousie additive-manufacturing program: evidence audit

**The central corrosion comparison cannot be resolved from the accessible sources.** The requested Morshed-Behbahani corrosion papers, COM proceedings chapter, arc-DED paper and CIRP study were identified bibliographically, but their experimental text was unavailable. Consequently, I cannot establish whether heat-treated LPBF or laser DED had better corrosion resistance, *why*, or their corrosion current densities, potentials, impedances, attack depths and seawater-test conditions. Neither process should be declared the winner on the basis of density or mechanical performance. The one accessible primary experimental paper, Timmons et al., studies **LPBF of C64200 aluminum–silicon bronze—not nickel–aluminum bronze—and does not test corrosion**. (timmons2025laserpowderbed pages 2-4, timmons2025laserpowderbed pages 19-23)

The following comparison separates measured results from items requiring the original papers; “not verified” does **not** mean a measurement was not made.

| Study / process | Chemistry / feedstock | Verified quantitative results | Missing information / evidence status |
|---|---|---|---|
| **Timmons, Nasiri & Bishop (2025), C64200 — LPBF** | Powder: Cu 91.89, Al 6.29, Si 1.52, Ni 0.05 wt%; GKN Hoeganaes Ar-gas-atomized Concast wrought bar; D10/mean/D90 = 18/33/54 µm; flow = 3.1 g/s (timmons2025laserpowderbed pages 2-4) | Tensile blanks: 99.5 ± 0.3% dense. As-built: YS 595 ± 28 MPa, UTS 797 ± 9 MPa, elongation 4.9 ± 1.0%, Charpy 30 ± 1 J. After 620 °C/2 h/water quench: YS 329 ± 2 MPa, UTS 567 ± 1 MPa, elongation 24.6 ± 0.3%, Charpy 63 ± 4 J (timmons2025laserpowderbed pages 19-23) | No corrosion or seawater testing; no powder-oxygen value reported. This is LPBF, not DED. |
| **Rayner et al. (2025), C63020 — LPBF** *(secondary reporting by Timmons et al.)* | Nominal Cu–10Al–5Ni–5Fe wt%; powder-bed feedstock (timmons2025laserpowderbed pages 2-4) | Near-100% density with low residual oxygen at 300 W and 800 mm/s. As-built: YS 336 MPa, elongation 2.9%. After 675 °C/6 h: YS 485 MPa, elongation 11.4% (timmons2025laserpowderbed pages 2-4) | Powder source/size, exact density, oxygen, UTS, hardness, and corrosion metrics not verified here. Distinct from the COM 2024 powder-fed laser-DED study. |
| **Morshed-Behbahani et al. (2025), heat-treated NAB — LPBF versus powder-fed laser DED** | Primary text unavailable | Bibliographic identity and process comparison only; DOI: 10.1016/j.colsurfa.2024.136069 | Corrosion ranking, explanation, chemistry, powder source/size, test solution/duration, Ecorr, icorr, impedance, attack depth, density, and hardness **not verified from available text**. |
| **Morshed-Behbahani et al. (2024), NAB — LPBF** | Primary text unavailable | Bibliographic identity only; DOI: 10.1016/j.corsci.2024.111846 | Unusual electrochemical mechanism, chemistry, powder details, exposure conditions, and all quantitative corrosion metrics **not verified from available text**. |
| **Rayner et al. (COM 2024), C63020 — blown-powder laser DED** | Primary proceedings text unavailable | Bibliographic identity only; DOI: 10.1007/978-3-031-67398-6_13 | Powder source/size/flow/oxygen, measured chemistry, density, process parameters, mechanical properties, and corrosion data **not verified**. Do not substitute the separate Rayner C63020 LPBF results above. |
| **Aliyu, Bishop & Nasiri, companion study — wire-arc DED/WAAM plus heat treatment** | Wire feedstock; primary text unavailable | Bibliographic identity only; conference DOI: 10.1007/978-3-031-67398-6_28; later full mechanical paper DOI: 10.1016/j.msea.2025.148454 | Wire chemistry, heat-treatment schedule, density, hardness, strength/elongation, and corrosion performance **not verified from available text**. |
| **Morshed-Behbahani et al. (2025), heat-treated LPBF NAB — surface post-treatments** | Primary text unavailable | Bibliographic identity only; DOI: 10.1016/j.cirpj.2025.06.010 | Surface treatments, roughness, corrosion medium/duration, Ecorr, icorr, impedance, and attack depth **not verified from available text**; no supported corrosion ranking can be assigned. |


*Table: Verified quantitative benchmarks are separated from studies whose primary text was unavailable. The table also distinguishes Rayner's 2025 C63020 LPBF study from the separate COM 2024 powder-fed laser-DED work.*

### Requested publications and proposal relevance

1. **[CITE] [NUMBERS—unavailable] [NAVY] [NOVELTY-RISK]** K. Morshed-Behbahani, A. J. Rayner, D. P. Bishop and A. Nasiri, “Impact of fabrication method on the corrosion behavior of heat-treated nickel aluminum bronze (NAB) alloy: a comparison of laser powder bed fusion (L-PBF) and laser directed energy deposition (L-DED) techniques,” *Colloids and Surfaces A: Physicochemical and Engineering Aspects* **708** (2025) 136069. DOI: **10.1016/j.colsurfa.2024.136069**. It directly overlaps the proposed *process–microstructure–corrosion* comparison, but compares **heat-treated** LPBF and laser DED, not an established as-deposited powder-alloy optimization. The available evidence does not identify the DED feedstock form, exact wt% composition, powder supplier/size, treatment schedule, electrolyte or exposure duration, corrosion ranking or its mechanism. Classifying its L-DED specifically as *blown-powder* rather than wire-fed requires the chapter itself. [GAP] No verified evidence here establishes 30-day flowing-seawater performance, C71500 equivalence or repair onto cast NAB/wrought Cu–Ni. Its defence-program connection is supported at the **program**, not demonstrably this paper’s grant, level. (timmons2025laserpowderbed pages 26-27, zakerin2025reviewoftribological pages 48-50)

2. **[CITE] [NUMBERS—unavailable] [NOVELTY-RISK]** K. Morshed-Behbahani, A. J. Rayner, D. P. Bishop and A. Nasiri, “Perspectives on the unusual electrochemical corrosion of nickel aluminum bronze (NAB) alloy fabricated through laser-powder bed fusion additive manufacturing,” *Corrosion Science* **228** (2024) 111846. DOI: **10.1016/j.corsci.2024.111846**. **Process: LPBF**; do not relabel it laser cladding or DED. Although the study is explicitly identified in the Dalhousie review’s references, the accessible excerpt supplies **no account of what makes its electrochemistry ‘unusual’**. Composition, powder specification, NaCl versus natural/substitute seawater, immersion time/flow, *E*<sub>corr</sub>, *i*<sub>corr</sub>, impedance, selective attack and hardness are therefore not reportable here. [GAP] This citation alone does not benchmark as-deposited laser-DED repair or C71500. (camilleri2025coldsprayas pages 12-13, zakerin2025reviewoftribological pages 52-54)

3. **[CITE] [NUMBERS—unavailable] [NAVY] [NOVELTY-RISK]** A. J. Rayner, K. Morshedbehbahani, C. Spence, G. Wood, D. Hamre, A. Nasiri and D. P. Bishop, “Directed Energy Deposition of UNS C63020 Nickel Aluminum Bronze Powder,” *Proceedings of the 63rd Conference of Metallurgists, COM 2024*, pp. 53–58 (2024). DOI: **10.1007/978-3-031-67398-6_13**. **Process: powder-fed DED**, according to the chapter title; the source was unavailable to establish its particular laser, cladding configuration or powder delivery arrangement. UNS C63020 is the relevant NAB grade, but the COM powder’s **measured** wt% chemistry, source, size/flow/oxygen, deposit density, cracking, hardness, strength and corrosion conditions/results could not be confirmed. [GAP] Do not represent this as prior proof of as-deposited seawater-resistant repairs. Critically, it is **not** Rayner’s separate C63020 **LPBF** publication, whose numbers appear below. (timmons2025laserpowderbed pages 2-4, timmons2025laserpowderbed pages 26-27)

4. **[CITE] [NUMBERS—unavailable] [NAVY] [GAP]** A. Aliyu, D. P. Bishop and A. Nasiri, “Tailoring Microstructure and Mechanical Properties of an Arc-Directed Energy Deposited Nickel-Aluminum Bronze Alloy via Post-Printing Heat Treatment,” *COM 2024*, pp. 135–139 (2024). DOI: **10.1007/978-3-031-67398-6_28**. **Process: arc DED/WAAM, not blown-powder laser DED.** The related expanded article is A. Aliyu, D. P. Bishop and A. Nasiri, “Impacts of post-printing heat treatment on the microstructure and mechanical properties of wire-arc additively manufactured nickel aluminum bronze alloy,” *Materials Science and Engineering A* **937** (2025) 148454, DOI: **10.1016/j.msea.2025.148454**. Neither primary text was accessible: wire composition, heat-treatment conditions, porosity, hardness, tensile/elongation results and any corrosion test cannot be transferred from LPBF or asserted for this study. Its arc and post-treatment focus leaves the proposed as-deposited, one-powder laser-DED corrosion question distinct. The Dalhousie group acknowledges Canadian defence research partners, but paper-specific funding was not verified. (zakerin2025reviewoftribological pages 48-50)

5. **[CITE] [NUMBERS—unavailable] [NOVELTY-RISK]** K. Morshed-Behbahani, N. Zakerin, A. J. Rayner, D. P. Bishop and A. Nasiri, “Impact of surface post-treatments on corrosion resistance in heat-treated laser-powder bed fused nickel aluminum bronze,” *CIRP Journal of Manufacturing Science and Technology* **61** (2025) 153–162. DOI: **10.1016/j.cirpj.2025.06.010**. **Process: LPBF plus heat and surface post-treatment**; neither an untreated laser-DED deposit nor an arc-DED experiment. Because the paper was unavailable, which surface treatment won, surface roughness, electrolyte, duration/flow, *E*<sub>corr</sub>, *i*<sub>corr</sub>, EIS, selective-attack depth and powder specifications remain **unverified**. [GAP] Its title underscores the importance of measuring the proposed alloys **as deposited**, with any surface finishing explicitly controlled, rather than borrowing post-treated benchmarks. (zakerin2025reviewoftribological pages 48-50)

6. **[CITE] [NUMBERS] [NAVY] [GAP]** K. A. Timmons, A. Nasiri and D. P. Bishop, “Laser Powder Bed Fusion Processing of UNS C64200 Aluminum–Silicon–Bronze,” *Journal of Manufacturing and Materials Processing* **9** (2025) 147. DOI: **10.3390/jmmp9050147**. **Process: LPBF on a C63000 plate, compared mechanically with wrought C64200; neither NAB nor DED.** Its **measured powder composition**, wt%, was Cu 91.89, Al 6.29, Si 1.52, Fe 0.09, Ni 0.05, Mn 0.02, Zn 0.11 and Sn 0.02. Concast wrought C64200 bar was **argon-gas-atomized by GKN Hoeganaes**, then sieved using 20- and 53-µm meshes: *D*₁₀/mean/*D*₉₀ **18/33/54 µm**, flow **3.1 g/s**, apparent/tap densities **4.45/4.55 g cm⁻³**, Hausner ratio **1.02**. These are **not** ultrasonic-atomized powder or necessarily Hall flow in seconds/50 g. Powder oxygen was not supplied in the extracted methods; **<10 ppm** denotes the **LPBF chamber atmosphere**, not powder oxygen. (timmons2025laserpowderbed pages 2-4, timmons2025laserpowderbed pages 4-7)

   At **320 W, 770 mm s⁻¹, 0.088-mm hatch and 0.030-mm layers**, the optimum cuboid was reported at **99.94% density by Archimedes** versus **99.87% by image analysis**; **tensile blanks averaged 99.5 ± 0.3% density**, a different specimen population. As-built LPBF yielded **595 ± 28 MPa yield strength, 797 ± 9 MPa UTS, 4.9 ± 1.0% elongation and 30 ± 1 J Charpy**. After **620 °C/2 h and water quench**, the corresponding results were **329 ± 2 MPa, 567 ± 1 MPa, 24.6 ± 0.3% and 63 ± 4 J**; heat-treated wrought comparators were **292 ± 1 MPa, 583 ± 3 MPa, 36.6 ± 3.7% and 108 ± 3 J**. As-built β′ martensite was eliminated by treatment. The article reports **no NaCl/seawater corrosion, *E*<sub>corr</sub>, *i*<sub>corr</sub>, impedance or selective-attack depth** and offers no corrosion ranking against C71500. Its FactSage pseudo-binary equilibrium diagram is a relevant **limited physics comparator**, not a thermal-history-coupled CALPHAD model. (timmons2025laserpowderbed pages 12-15, timmons2025laserpowderbed pages 19-23, timmons2025laserpowderbed pages 15-19)

7. **[CITE] [NUMBERS—secondary] [NOVELTY-RISK]** A. J. Rayner, J. Hierlihy, M. Trask, R. W. Cooke and D. P. Bishop, “Laser powder bed fusion processing of UNS C63020 nickel aluminum bronze powder,” *Progress in Additive Manufacturing* **10** (2025) 427–449. DOI: **10.1007/s40964-024-00633-w**. **Process: LPBF, not the COM 2024 DED process**. Timmons et al. report nominal **Cu–10Al–5Ni–5Fe wt%**, near-100% density with low residual oxygen at **300 W/800 mm s⁻¹**, and as-built yield strength/**elongation of 336 MPa/2.9%**, changing after **675 °C/6 h** to **485 MPa/11.4%** as β′ decreased and α/κ constituents evolved. These are **secondary reports**, not measurements verified against Rayner’s unavailable article; its powder source/size, numerical oxygen, precise density and seawater-corrosion metrics cannot be supplied. (timmons2025laserpowderbed pages 2-4, timmons2025laserpowderbed pages 26-27)

### Funding and the unanswered comparison

**[NAVY]** Directly verified funding for the *Timmons* study was **NSERC ALLRP 580290-22** and **Canada Foundation for Innovation 36245**. Its acknowledgments additionally identify **Research Nova Scotia; Defence Research and Development Canada (DRDC); Apollo Laser Cladding; Babcock Canada; GKN Hoeganaes; and Tronos**. The group’s 2025 review independently acknowledges NSERC, the Canada Research Chairs program and the Ocean Frontier Institute, and names **DRDC and Babcock Canada** among industry/defence partners. DRDC is an agency of **Canada’s Department of National Defence**; this establishes a Canadian defence connection, **not** that DND directly funded every cited corrosion paper or that the US Navy funded any of them. The C64200 work also tests against UK defence material specifications, which are performance standards, not a funding attribution. (timmons2025laserpowderbed pages 26-27, zakerin2025reviewoftribological pages 48-50, timmons2025laserpowderbed pages 19-23)

**[GAP]** No accessible requested experiment supplies a verified head-to-head, **as-deposited**, single-stream pre-alloyed laser-DED comparison of compositionally designed Cu–Ni or NAB on **both cast NAB and wrought Cu–Ni**, evaluated against wrought **70–30 Cu–Ni** in matched seawater exposures. The Dalhousie review itself identifies marine NAB **DED tribocorrosion** and evaluation of DED claddings in relevant service as future research areas; that is a review-level gap, not proof that no subsequent experiments exist. Accordingly, the questions **“LPBF or laser DED: which corroded less, and why?”** and **“were the corrosion tests 3.5 wt% NaCl, ASTM D1141, natural seawater, flowing or 30 days?”** remain unanswered here until the original corrosion papers are consulted. (zakerin2025reviewoftribological pages 48-50, zakerin2025reviewoftribological pages 1-2)

### Top 5 things the PI should know

1. **Do not claim a corrosion winner.** The most directly relevant LPBF-versus-laser-DED study compares **heat-treated** NAB, but its numerical results and mechanism could not be verified; a matched **as-deposited** comparator is essential. (zakerin2025reviewoftribological pages 48-50)
2. **The overlap is real, but process state matters.** Dalhousie has published a powder-fed C63020 DED proceedings study and several LPBF/NAB corrosion or post-treatment studies. Distinguish the proposed compositionally varied, one-powder **laser-DED repair** from both **LPBF** and **wire-arc DED**; do not describe the COM DED work as in-situ elemental-powder blending without evidence. (timmons2025laserpowderbed pages 2-4, zakerin2025reviewoftribological pages 48-50)
3. **Use the correct mechanical benchmark.** The accessible C64200 study is **nearly nickel-free aluminum–silicon bronze**, not NAB: its LPBF tensile specimens were **99.5 ± 0.3% dense**, but as-built elongation was only **4.9 ± 1.0%**; post-build treatment lifted it to **24.6 ± 0.3%**. This motivates testing as-deposited cracking and properties without presuming heat-treated performance. (timmons2025laserpowderbed pages 2-4, timmons2025laserpowderbed pages 19-23)
4. **Powder provenance is a differentiator, not a transferable specification.** The verified Timmons powder was **commercially argon-atomized from Concast stock at GKN**, with **18/33/54-µm** *D*₁₀/mean/*D*₉₀; its values are **not** measured properties of Dalhousie’s C63020 DED powder or of in-house ultrasonically atomized feedstock. Record oxygen **in powder separately from chamber oxygen** and characterize each lot. (timmons2025laserpowderbed pages 2-4, timmons2025laserpowderbed pages 4-7)
5. **Frame the specific advance and sponsor accurately.** Claim novelty in **as-deposited seawater qualification versus C71500, dissimilar-substrate repair, lower-Ni alloy search and thermal-history-informed CALPHAD linked to cost-aware experiments**, rather than merely ‘NAB by DED.’ Cite the demonstrated **NSERC/CFI funding and DRDC partnership** without turning a partner acknowledgment into an unverified DND grant attribution. (timmons2025laserpowderbed pages 26-27, zakerin2025reviewoftribological pages 48-50, timmons2025laserpowderbed pages 15-19)

References

1. (timmons2025laserpowderbed pages 2-4): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

2. (timmons2025laserpowderbed pages 19-23): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

3. (timmons2025laserpowderbed pages 26-27): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

4. (zakerin2025reviewoftribological pages 48-50): Nika Zakerin, Khashayar Morshed-Behbahani, Donald Paul Bishop, and Ali Nasiri. Review of tribological and wear behavior of alloys fabricated via directed energy deposition additive manufacturing. Jun 2025. URL: https://doi.org/10.3390/jmmp9060194, doi:10.3390/jmmp9060194. This article has 24 citations.

5. (camilleri2025coldsprayas pages 12-13): Steven Camilleri, Tien Tran, Andrew Duguid, and Kannoorpatti Narayanan Krishnan. Cold spray as a powder metallurgy process for production of nickel aluminium bronze. PLOS One, 20:e0319333, Mar 2025. URL: https://doi.org/10.1371/journal.pone.0319333, doi:10.1371/journal.pone.0319333. This article has 2 citations and is from a peer-reviewed journal.

6. (zakerin2025reviewoftribological pages 52-54): Nika Zakerin, Khashayar Morshed-Behbahani, Donald Paul Bishop, and Ali Nasiri. Review of tribological and wear behavior of alloys fabricated via directed energy deposition additive manufacturing. Jun 2025. URL: https://doi.org/10.3390/jmmp9060194, doi:10.3390/jmmp9060194. This article has 24 citations.

7. (timmons2025laserpowderbed pages 4-7): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

8. (timmons2025laserpowderbed pages 12-15): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

9. (timmons2025laserpowderbed pages 15-19): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

10. (zakerin2025reviewoftribological pages 1-2): Nika Zakerin, Khashayar Morshed-Behbahani, Donald Paul Bishop, and Ali Nasiri. Review of tribological and wear behavior of alloys fabricated via directed energy deposition additive manufacturing. Jun 2025. URL: https://doi.org/10.3390/jmmp9060194, doi:10.3390/jmmp9060194. This article has 24 citations.
