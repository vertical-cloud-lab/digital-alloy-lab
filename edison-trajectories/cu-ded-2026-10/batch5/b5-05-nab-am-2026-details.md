<!--
Edison Scientific LITERATURE task (batch 5)
- Task ID: dba9c173-6152-4a52-95ad-a0b790903889
- Submitted: 2026-10-17T06:20:06Z
- Fetched: 2026-10-17T06:42:04Z (status: success)
- Raw trajectory JSON: ../raw/b5-05-nab-am-2026-details.json.gz
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

QUESTION: Give details (process, composition, phases, density, mechanical
and corrosion numbers) of these 2025-2026 NAB additive manufacturing
papers: Hu et al., J. Alloys Compd. 1066 (2026) 187981 (laser-powder DED vs
LPBF NAB); Saremi et al., Virtual Phys. Prototyp. 21 (2026) e2688627
(heated-platform LPBF NAB design); Roshan et al., Mater. Chem. Phys. 349
(2026) 131759 (pre-corrosion and fatigue of DED NAB); Yao et al., Addit.
Manuf. 105 (2025) 104787 (repair of NAB by in-situ Cu-Al synthesis via DED);
Yao, Shin and Shim (laser remelting for pore mitigation in DED NAB);
Mahmoudiniya et al., Mater. Sci. Eng. A 961 (2026) 150140 (NAB/martensitic
stainless steel by DED); and Wu et al., Mater. Sci. Eng. A 973 (2026) 150695
(wire flat-top laser DED NAB). Which of them report as-deposited corrosion,
and how do DED and LPBF NAB compare?

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

QUESTION: Give details (process, composition, phases, density, mechanical
and corrosion numbers) of these 2025-2026 NAB additive manufacturing
papers: Hu et al., J. Alloys Compd. 1066 (2026) 187981 (laser-powder DED vs
LPBF NAB); Saremi et al., Virtual Phys. Prototyp. 21 (2026) e2688627
(heated-platform LPBF NAB design); Roshan et al., Mater. Chem. Phys. 349
(2026) 131759 (pre-corrosion and fatigue of DED NAB); Yao et al., Addit.
Manuf. 105 (2025) 104787 (repair of NAB by in-situ Cu-Al synthesis via DED);
Yao, Shin and Shim (laser remelting for pore mitigation in DED NAB);
Mahmoudiniya et al., Mater. Sci. Eng. A 961 (2026) 150140 (NAB/martensitic
stainless steel by DED); and Wu et al., Mater. Sci. Eng. A 973 (2026) 150695
(wire flat-top laser DED NAB). Which of them report as-deposited corrosion,
and how do DED and LPBF NAB compare?

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


# NAB additive manufacturing: evidence audit

**Scope and limitation.** Bibliographic records were located for the requested studies, but their primary full texts were not retrievable in this search. Consequently, **no requested paper’s exact composition, powder size/flow/oxygen, density or porosity, hardness, tensile properties, corrosion current or rate, corrosion potential, impedance, or selective-attack depth can be verified here**. The same applies to electrolyte, exposure duration, flow, heat-treatment state, and funding acknowledgments. A title mentioning corrosion does not establish that testing was performed *as deposited*. The distinctions below are therefore useful for positioning the proposal, **not** a substitute for numerical benchmarks from the papers.

## Requested studies

1. **Hu, K., J. Gao, J. Song, Y. Liu, B. Song, B. Liu, J.-F. Wu, and Y.-S. Shi.** “Microstructure, mechanical and corrosion properties of additively manufactured nickel-aluminum bronze alloys: laser powder directed energy deposition vs. laser powder bed fusion.” *Journal of Alloys and Compounds* **1066** (2026), 187981. **DOI:** [10.1016/j.jallcom.2026.187981](https://doi.org/10.1016/j.jallcom.2026.187981). **Process:** laser powder-fed DED versus LPBF—not WAAM. **Corrosion:** explicitly within the paper’s stated scope, but whether specimens were tested as deposited, the medium and duration, and the DED–LPBF ranking cannot be verified. **Composition, phases, density, mechanical and corrosion numbers:** unavailable. **Tags:** [CITE] [NOVELTY-RISK: direct DED–LPBF NAB/corrosion overlap] [GAP: comparison against C71500 and repair-interface corrosion not established].

2. **Saremi, M., A. Shahriari, P. Moazzen, T. Maiwald-Immer, A. Lloyd, and M. Mohammadi.** “Designing nickel aluminum bronzes with enhanced properties via heated platform laser powder bed fusion.” *Virtual and Physical Prototyping* **21** (2026), e2688627. **DOI:** [10.1080/17452759.2026.2688627](https://doi.org/10.1080/17452759.2026.2688627). **Process:** heated-platform LPBF, not blown-powder DED. **Corrosion:** not established by the available record; “enhanced properties” is not a seawater-corrosion result. **Platform temperature, wt% composition, phases, density and property numbers:** unavailable. **Tags:** [CITE] [NOVELTY-RISK: NAB design and thermal-history effects] [GAP: transfer to single-stream DED and as-deposited seawater performance unestablished].

3. **Roshan, M., M. Mahtabi, W. Bednarczyk, G. Cios, and M. Haghshenas.** “Effect of Pre-Corrosion on the Fatigue Performance of Direct Energy Deposited Nickel–Aluminum Bronze.” *Materials Chemistry and Physics* **349**, 131759; **publication year requires checking** (a later paper lists 2025, whereas the supplied citation says 2026). **DOI: not verified.** The title and author list are reproduced in the later authors’ reference list. **Process:** described as DED; the accessible citation does **not** establish laser/blown powder versus arc. **Corrosion:** pre-exposure followed by fatigue is **not**, by itself, a measured as-deposited corrosion rate. **Pre-exposure medium/time, wt% composition, phases, density, fatigue and electrochemical numbers:** unavailable. Do not substitute results from the authors’ separate **WAAM** in-situ corrosion-fatigue study, which immersed specimens in synthetic seawater *during* testing and used annealed material. **Tags:** [CITE] [NAVY: marine-performance relevance, not verified Navy funding] [GAP: standalone as-deposited corrosion benchmark unverified]. (mahtabi2026insituveryhigh pages 28-32, mahtabi2026insituveryhigh pages 5-8, mahtabi2026insituveryhigh pages 1-5)

4. **Yao, C., S. He, K.-Y. Lee, G.-Y. Shin, and D.-S. Shim.** “Microstructural and interfacial characteristics in repair of nickel-aluminum bronze by in-situ synthesis of Cu-Al alloys via directed energy deposition.” *Additive Manufacturing* **105** (2025), 104787. **DOI:** [10.1016/j.addma.2025.104787](https://doi.org/10.1016/j.addma.2025.104787). **Process:** DED repair using *in-situ* Cu–Al synthesis; **not evidence for a single pre-alloyed NAB powder feed**. **Corrosion:** not established for this repair paper by the accessible material. **Substrate/deposit wt%, phases, interface integrity, density, hardness, strength and corrosion numbers:** unavailable. **Tags:** [CITE] [NAVY: NAB repair relevance, not verified Navy funding] [NOVELTY-RISK: NAB repair and composition manipulation, but a different feedstock strategy] [GAP: pre-alloyed powder and validated seawater-resistant repair interface].

5. **Yao, C., G.-Y. Shin, and D.-S. Shim.** “Study on laser remelting for pore mitigation in nickel–aluminum bronze (NAB) fabricated by directed energy deposition.” **2026 preprint; peer-reviewed publication not verified. DOI:** [10.2139/ssrn.5347164](https://doi.org/10.2139/ssrn.5347164). **Process:** DED with an additional laser-remelting operation; the feedstock form is unverified. **Corrosion:** not established. **Initial/final porosity, remelting settings, wt% composition, phases, hardness and other numbers:** unavailable. **Tags:** [CITE: process-positioning only, pending verification] [NOVELTY-RISK: pore mitigation] [GAP: achieving density without a separate remelting step and demonstrating corrosion].

6. **Mahmoudiniya, M., B. Luyten, N. Ghavanini, P. Verleysen, M. Hermans, and L. A. I. Kestens.** “Microstructure, texture and mechanical performance of a nickel–aluminium bronze / martensitic stainless steel bimetal produced by direct energy deposition.” *Materials Science and Engineering A* **961** (2026), 150140. **DOI:** [10.1016/j.msea.2026.150140](https://doi.org/10.1016/j.msea.2026.150140). **Process:** DED bimetal; laser versus arc and powder versus wire cannot be confirmed from the accessible record. **Substrate:** martensitic stainless steel, **not** cast NAB or wrought Cu–Ni. **Corrosion:** not established. **Wt% composition, phases, density, interface strength, hardness, tensile numbers:** unavailable. **Tags:** [CITE] [NOVELTY-RISK: dissimilar-metal DED/interface mechanics, but different substrate] [GAP: specified marine repair substrates and corrosion].

7. **Wu, X.-D., H.-B. Mi, S.-N. Liao, P.-C. You, L.-Y. Feng, Q.-Y. Liu, Z.-H. Liu, B.-Y. He, and W. Guo.** “Wire-based flat-top laser directed energy deposition of nickel-aluminum bronze: gradient microstructure, hierarchical precipitation, and strength-ductility synergy.” *Materials Science and Engineering A* **973** (2026), 150695. **DOI:** [10.1016/j.msea.2026.150695](https://doi.org/10.1016/j.msea.2026.150695). **Process:** **wire-fed laser DED**, neither blown-powder DED nor wire-*arc* AM. **Phases:** the title establishes hierarchical precipitation, but constituent-phase assignments cannot be verified. **Corrosion:** not established. **Wire wt% composition, porosity, hardness, strength and elongation:** unavailable. **Tags:** [CITE] [NOVELTY-RISK: NAB thermal-history/microstructure/strength design, but wire feedstock] [GAP: powder qualification and seawater behavior].

The compact process-and-evidence comparison is provided below. Its “evidence limit” column is essential: none of its missing numerical entries should be treated as zero or as a negative experimental result.

| Requested publication | Process distinction | Subject and justified corrosion evidence | Proposal relevance | Evidence limit |
|---|---|---|---|---|
| Hu et al., *J. Alloys Compd.* **1066** (2026) 187981; DOI: 10.1016/j.jallcom.2026.187981 | Blown-powder laser DED versus LPBF | Title explicitly covers microstructure, mechanical properties, and corrosion; therefore directly relevant to an as-deposited DED–LPBF comparison. Exact electrolyte, exposure, density, corrosion, hardness, and tensile values were inaccessible. | **Highest direct overlap:** conventional NAB, powder-fed laser DED, LPBF comparator, and corrosion. | Citation metadata verified; primary full text inaccessible, so no numerical result or chemistry should be inferred. |
| Saremi et al., *Virtual Phys. Prototyp.* **21** (2026) e2688627; DOI: 10.1080/17452759.2026.2688627 | Heated-platform LPBF | Alloy and process design using platform heating. Corrosion testing is not established by the accessible metadata; “enhanced properties” must not be interpreted as demonstrated seawater resistance. | Relevant comparator for thermal-history and alloy-design effects, but not blown-powder DED or repair. | Citation metadata verified; primary full text inaccessible. Composition, phases, density, mechanical results, platform temperature, and corrosion evidence remain unverified. |
| Roshan et al., *Mater. Chem. Phys.* **349** (listed as 2025/2026) 131759, “Effect of Pre-Corrosion on the Fatigue Performance of Direct Energy Deposited Nickel–Aluminum Bronze” | DED; the accessible secondary citation does not establish whether the heat source and feedstock were laser–powder or WAAM | Pre-corrosion followed by fatigue. This is an environmental-fatigue study, **not evidence of a standalone as-deposited corrosion rate**, unless the primary paper separately reports electrochemical or mass-loss measurements. The title and citation are reproduced in a later WAAM corrosion-fatigue paper (mahtabi2026insituveryhigh pages 28-32). | Relevant to durability after marine exposure, but not a demonstrated composition-to-corrosion benchmark. | DOI and publication year unresolved; primary full text inaccessible. Exposure medium and duration, fatigue conditions, chemistry, density, and corrosion metrics cannot be reported reliably. |
| Yao et al., *Addit. Manuf.* **105** (2025) 104787; DOI: 10.1016/j.addma.2025.104787 | Powder-fed DED repair using **in-situ Cu–Al synthesis or blending**, not one pre-alloyed powder stream | Repair-interface and microstructural study. Accessible metadata does not establish quantitative as-deposited corrosion testing. | **Novelty boundary:** overlaps NAB repair and composition control, but differs fundamentally from the proposed single-stream, pre-alloyed-powder approach. | Citation metadata verified; primary full text inaccessible. Do not transfer corrosion findings from the authors’ separate varied-Al Cu–Al paper, which used blended powders and found 12 wt% Al best among 6–12 wt% Al (canacoo2026laseradditivemanufacturing pages 12-14). |
| Yao, Shin, and Shim, “Study on laser remelting for pore mitigation in nickel–aluminum bronze fabricated by directed energy deposition” (2026 preprint); DOI: 10.2139/ssrn.5347164 | DED followed by laser remelting | Pore mitigation and densification. No justified corrosion evidence was found in the accessible record. | Relevant process comparator for density, but additional remelting differs from achieving dense deposits directly through alloy and powder design. | SSRN metadata verified; peer-reviewed venue and primary results inaccessible. Remelting parameters, initial and final porosity, hardness, chemistry, and corrosion values remain unverified. |
| Mahmoudiniya et al., *Mater. Sci. Eng. A* **961** (2026) 150140; DOI: 10.1016/j.msea.2026.150140 | DED of a NAB/martensitic-stainless-steel bimetal | Microstructure, texture, interface, and mechanical performance; accessible metadata does not establish corrosion testing. | Relevant to dissimilar-substrate deposition and interface integrity, but martensitic stainless steel is not cast NAB or wrought Cu–Ni. | Citation metadata verified; primary full text inaccessible. Feedstock form, compositions, phases, density, hardness, strength, elongation, and corrosion numbers cannot be verified. |
| Wu et al., *Mater. Sci. Eng. A* **973** (2026) 150695; DOI: 10.1016/j.msea.2026.150695 | **Wire-fed, flat-top-laser DED**, not blown-powder DED | Gradient microstructure, hierarchical precipitation, and strength–ductility synergy. No justified corrosion evidence was found in the accessible record. | Useful mechanical and microstructural benchmark and heat-source comparator, but its feedstock physics differ materially from pre-alloyed powder DED. | Citation metadata verified; primary full text inaccessible. Wire chemistry, phases, density, hardness, strength, elongation, and corrosion results remain unverified. |


*Table: Comparison of the seven requested NAB additive-manufacturing records, emphasizing process distinctions, defensible corrosion evidence, proposal relevance, and unavailable primary-source data. It avoids attributing quantitative results or chemistry that could not be verified.*

## Which report as-deposited corrosion? How do DED and LPBF compare?

**Hu is the one requested study whose bibliographic title explicitly promises a DED–LPBF NAB *corrosion* comparison.** Its as-deposited test state, corrosion metrics, and winning process remain **unverified** here. **Roshan** concerns *pre-corrosion fatigue*, a different endpoint. Corrosion testing in **Saremi, Yao’s repair and remelting studies, Mahmoudiniya, and Wu** cannot be confirmed from the available material. Accordingly, **there is no defensible numerical DED-versus-LPBF corrosion ranking in the retrieved evidence**, nor a substantiated claim that either equals wrought C71500 in natural or ASTM D1141 seawater. Likewise, none of the seven yields a verified **[NUMBERS]** benchmark for the requested outcomes; no Navy/DoD **funding** designation can be assigned.

**Important near-neighbor, not a result of the requested repair paper:** Yao, He, Lee, Shim, and Shin, “Microstructure and corrosion resistance manipulation of directed energy deposited Cu-Al alloys with varied Al contents,” *Journal of Materials Research and Technology* **35** (2025), 792–808, DOI [10.1016/j.jmrt.2025.01.077](https://doi.org/10.1016/j.jmrt.2025.01.077). A review reports **laser DED of *blended* CuNiSiCr and Al–Mg–Si powders**, successful deposits at **6–12 wt% Al**, fracture at **14 wt% Al** associated with a brittle phase, and the **12 wt% Al** composition as having the lowest corrosion rate in that series, described as comparable to **cast NAB**. These are **secondary-source composition and qualitative-corrosion benchmarks**, not verified numerical corrosion rates, not C71500 comparisons, and **not** outcomes of *Additive Manufacturing* 104787. **Tags:** [CITE] [NUMBERS: composition range only] [NOVELTY-RISK: alloy-content/corrosion optimization using blended feedstock] [GAP: pre-alloyed single-stream powder and C71500-standardized exposure]. (canacoo2026laseradditivemanufacturing pages 36-37, canacoo2026laseradditivemanufacturing pages 12-14, canacoo2026laseradditivemanufacturing media 642030c6)

## Top 5 things the PI should know

1. **Read Hu’s primary results before asserting an AM-process advantage:** it is the most direct prior-art challenge to a powder-DED/NAB corrosion claim, but the retrieved evidence does not support a direction or magnitude for DED versus LPBF.
2. **State the feedstock distinction precisely:** Yao’s demonstrated varied-Al corrosion trend concerns *blended powders*; in-situ repair and wire-fed laser DED do not establish outcomes for one ultrasonically atomized, pre-alloyed powder stream. (canacoo2026laseradditivemanufacturing pages 12-14)
3. **Keep endpoints separate:** Roshan’s pre-corrosion fatigue and the separate Mahtabi *WAAM* in-situ corrosion-fatigue work do not supply an as-deposited electrochemical rate for laser powder DED. (mahtabi2026insituveryhigh pages 28-32, mahtabi2026insituveryhigh pages 5-8, mahtabi2026insituveryhigh pages 1-5)
4. **Frame novelty as a coupled, validated target—not NAB AM alone:** pre-alloyed composition → measured powder quality → dense, crack-free DED on itself **and** both specified repair substrates → *as-deposited* standardized seawater performance against wrought C71500, with thermal-history-aware prediction. The seven accessible records do not verify that complete combination.
5. **Do not populate proposal benchmark tables from titles:** first obtain the primary papers and check electrolyte (3.5 wt% NaCl versus natural/ASTM D1141 seawater), immersion time and flow, as-built versus heated/annealed/remelted condition, corrosion units, substrate-side selective attack, density method, and lot-level powder oxygen/flow. No such values were verified for the requested seven studies.

References

1. (mahtabi2026insituveryhigh pages 28-32): MohammadBagher Mahtabi, Mojtaba Roshan, Wiktor Bednarczyk, Grzegorz Cios, and Meysam Haghshenas. In-situ very high cycle corrosion fatigue (vhc-cf) of wire arc additive manufactured (waam) nickel–aluminum bronze (nab). npj Materials Degradation, Jun 2026. URL: https://doi.org/10.1038/s41529-026-00831-7, doi:10.1038/s41529-026-00831-7. This article has 0 citations and is from a peer-reviewed journal.

2. (mahtabi2026insituveryhigh pages 5-8): MohammadBagher Mahtabi, Mojtaba Roshan, Wiktor Bednarczyk, Grzegorz Cios, and Meysam Haghshenas. In-situ very high cycle corrosion fatigue (vhc-cf) of wire arc additive manufactured (waam) nickel–aluminum bronze (nab). npj Materials Degradation, Jun 2026. URL: https://doi.org/10.1038/s41529-026-00831-7, doi:10.1038/s41529-026-00831-7. This article has 0 citations and is from a peer-reviewed journal.

3. (mahtabi2026insituveryhigh pages 1-5): MohammadBagher Mahtabi, Mojtaba Roshan, Wiktor Bednarczyk, Grzegorz Cios, and Meysam Haghshenas. In-situ very high cycle corrosion fatigue (vhc-cf) of wire arc additive manufactured (waam) nickel–aluminum bronze (nab). npj Materials Degradation, Jun 2026. URL: https://doi.org/10.1038/s41529-026-00831-7, doi:10.1038/s41529-026-00831-7. This article has 0 citations and is from a peer-reviewed journal.

4. (canacoo2026laseradditivemanufacturing pages 12-14): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

5. (canacoo2026laseradditivemanufacturing pages 36-37): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.

6. (canacoo2026laseradditivemanufacturing media 642030c6): Sampson Canacoo, Dong Hee Kang, Md Nazmus Sakib, and Jihoon Jeong. Laser additive manufacturing of copper and its alloys: challenges, process innovations, and future perspectives. International Journal of Precision Engineering and Manufacturing-Green Technology, Sep 2026. URL: https://doi.org/10.1007/s40684-026-00928-z, doi:10.1007/s40684-026-00928-z. This article has 0 citations.
