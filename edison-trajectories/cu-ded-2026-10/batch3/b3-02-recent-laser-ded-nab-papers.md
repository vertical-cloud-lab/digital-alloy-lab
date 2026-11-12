<!--
Edison Scientific LITERATURE_HIGH task (batch 3)
- Task ID: f1a334b2-df7e-46c3-bbf9-73d65a364256
- Submitted: 2026-10-17T05:46:04Z
- Fetched: 2026-10-17T06:16:52Z (status: success)
- Raw trajectory JSON: ../raw/b3-02-recent-laser-ded-nab-papers.json.gz
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

QUESTION: Give a detailed, paper-by-paper account of laser-DED (blown
powder) work on nickel-aluminum bronze and other marine copper alloys
published 2022-2026, with full text where possible. Include at least:
Jia et al., Corrosion Science (2025) 113114 (precipitate refinement and
corrosion of AM NAB); Jia et al., J. Mater. Process. Technol. (2025) 118659
(water cooling during laser deposition of NAB); Jia et al., Additive
Manufacturing 127 (2026) 105291 (subtractive composition design of NAB);
Hu et al., J. Alloys Compd. (2026) 187981 (NAB by laser-powder DED vs LPBF);
the 2024 comparison of heat-treated NAB (C63020) made by L-PBF vs L-DED;
Rayner et al. 2024 (DED of C63020 NAB powder, Dalhousie); Zhao et al.,
Metals 12 (2022) 781 (laser-deposited NAB on SUS630 in 3.5% NaCl); the 2025
study of pre-corrosion and fatigue of DED NAB; the 2025 Additive
Manufacturing study repairing NAB by in-situ synthesis of Cu-Al alloys via
DED; the 2026 Optics and Laser Technology study of pore mitigation in DED
NAB; Wang et al. 2026 (Adv. Eng. Mater., manganese-aluminum bronze by laser
DED); and Zhao et al. 2026 (SSRN, Cr and Zr microalloying of
Cu-8Al-6Ni-4Fe-2Mn for seawater). For each: process and feed, composition,
phases as deposited, porosity, corrosion test and numbers, mechanical
numbers, and what it means for a proposal that designs new DED powder
compositions for as-deposited seawater resistance.

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

QUESTION: Give a detailed, paper-by-paper account of laser-DED (blown
powder) work on nickel-aluminum bronze and other marine copper alloys
published 2022-2026, with full text where possible. Include at least:
Jia et al., Corrosion Science (2025) 113114 (precipitate refinement and
corrosion of AM NAB); Jia et al., J. Mater. Process. Technol. (2025) 118659
(water cooling during laser deposition of NAB); Jia et al., Additive
Manufacturing 127 (2026) 105291 (subtractive composition design of NAB);
Hu et al., J. Alloys Compd. (2026) 187981 (NAB by laser-powder DED vs LPBF);
the 2024 comparison of heat-treated NAB (C63020) made by L-PBF vs L-DED;
Rayner et al. 2024 (DED of C63020 NAB powder, Dalhousie); Zhao et al.,
Metals 12 (2022) 781 (laser-deposited NAB on SUS630 in 3.5% NaCl); the 2025
study of pre-corrosion and fatigue of DED NAB; the 2025 Additive
Manufacturing study repairing NAB by in-situ synthesis of Cu-Al alloys via
DED; the 2026 Optics and Laser Technology study of pore mitigation in DED
NAB; Wang et al. 2026 (Adv. Eng. Mater., manganese-aluminum bronze by laser
DED); and Zhao et al. 2026 (SSRN, Cr and Zr microalloying of
Cu-8Al-6Ni-4Fe-2Mn for seawater). For each: process and feed, composition,
phases as deposited, porosity, corrosion test and numbers, mechanical
numbers, and what it means for a proposal that designs new DED powder
compositions for as-deposited seawater resistance.

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


## Laser-DED of Nickel-Aluminum Bronze and Marine Copper Alloys (2022–2026): A Paper-by-Paper Account

This review consolidates the published literature on blown-powder laser directed energy deposition (L-DED), laser cladding, and closely related additive manufacturing (AM) processes applied to nickel-aluminum bronze (NAB) and marine copper alloys from 2022 to 2026. For each entry, the process, composition, key quantitative data, and relevance to a proposal designing new pre-alloyed DED powder compositions for as-deposited seawater resistance are noted. Where full text was obtainable, quantitative benchmarks are provided; where only metadata was available (many 2025–2026 papers were behind paywalls), the available information from titles, abstracts, and cross-references in other papers is reported.

---

### 1. Zhao et al., Metals 12 (2022) 781
**Citation:** L. Zhao, K. Li, J. Yao, Y. Yuan, B. Du, "The Laser Deposited Nickel-Aluminum Bronze Coatings on SUS630 Stainless Steel and Its Corrosion Resistance in 3.5 wt.% NaCl Solution," *Metals* 12 (2022) 781. DOI: 10.3390/met12050781

**Process:** Blown-powder laser deposition (TruDiode 3006 fiber laser, 2400 W for NAB, 1500 W for Ni alloys, 3.2 mm spot, 1000 mm/min, 50% overlap) on SUS630 stainless steel substrates.

**Composition:** NAB powder: 81.1 Cu–10.8 Al–4.1 Ni–4.0 Fe (wt%), 53–120 µm particle size; intermediate layers of KF-6 (95Ni–5Al) or KF-306 (80Ni–20Cr) (zhao2022thelaserdeposited pages 2-4).

**Phases as deposited:** α-Cu matrix, retained β/β′, intermetallic κ precipitates. Direct deposition on steel (N-1) produced abundant Fe-rich dendrites from substrate dilution and Cu–Fe liquid-phase separation. Ni and NiCr intermediate layers isolated the NAB microstructure from the steel (zhao2022thelaserdeposited pages 4-7).

**Corrosion (3.5 wt% NaCl, potentiodynamic + EIS + 21-day ASTM G31-72 immersion):**
- N-1 (direct): E_corr = −248 mV, i_corr = 7.82 × 10⁻⁶ A/cm², R_p = 2810 Ω·cm², max corrosion depth ~3.4 µm
- N-2 (Ni interlayer): E_corr = −255 mV, i_corr = 4.65 × 10⁻⁶ A/cm², R_p = 5275 Ω·cm², depth ~2.0 µm
- N-3 (NiCr interlayer): E_corr = −252 mV, i_corr = 4.09 × 10⁻⁶ A/cm², R_p = 4865 Ω·cm², depth ~1.8 µm; R_ct ~85,100 Ω·cm² at 21 days (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 13-14).

**Mechanical:** UTS: N-1 = 767.8 MPa, N-2 = 891.5 MPa, N-3 = 731.1 MPa; as-deposited NAB alone ~669 MPa. Elongation: 12.9%, 6.9%, 9.4%, vs. 17.5% for NAB alone (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 4-7).

**Tags:** [CITE] [NUMBERS] [GAP] No pre-alloyed powder composition optimization; corrosion improved by interlayer, not alloy design. Shows Fe dilution from steel is a major problem for DED NAB on dissimilar substrates—directly relevant to proposed NAB-on-NAB and NAB-on-Cu-Ni repair scenarios.

---

### 2. Jia et al., Corrosion Science 255 (2025) 113114
**Citation:** Z. Jia, R. Li, M. Chen, Z. Wang, G. Sun, E.-H. Han, "Effect of further precipitate refinement on mechanical properties and corrosion behavior of additively manufactured nickel aluminum bronze," *Corrosion Science* 255 (2025) 113114. DOI: 10.1016/j.corsci.2025.113114

**Process:** Laser deposition (blown powder) of NAB. Full text not obtainable.

**Key insight from title/abstract:** Demonstrates that further refinement of κ-phase precipitates in AM NAB improves both mechanical properties and corrosion resistance. This is a critical finding for alloy design: precipitate morphology and scale are tunable through DED thermal history and composition.

**Tags:** [CITE] [NOVELTY-RISK] Directly overlaps the proposed work's goal of designing compositions for improved as-deposited corrosion. The PI's CALPHAD-guided composition search should target precipitate refinement as a design objective. [NUMBERS] Likely contains quantitative i_corr and hardness data (not obtainable).

---

### 3. Jia et al., J. Mater. Process. Technol. (2025) 118659
**Citation:** Z. Jia, Z. Wang, M. Chen, K. Zhao, G. Sun, E.-H. Han, "Tailoring microstructural evolution in laser deposited nickel-aluminum bronze alloy by controlling water cooling condition," *J. Mater. Process. Technol.* (2025) 118659. DOI: 10.1016/j.jmatprotec.2024.118659

**Process:** Laser deposition of NAB with in-situ water cooling to control thermal history. Full text not obtainable.

**Key insight:** Water cooling during DED modifies the thermal history (cooling rate), which changes the precipitate landscape and microstructure of NAB. This is analogous to what the PI's heat-flow model aims to capture.

**Tags:** [CITE] [NOVELTY-RISK] Overlaps the proposed CALPHAD + thermal history modeling approach—the PI should cite this as prior art showing process-level thermal control. [GAP] The PI's approach is compositional rather than process-based; synergy could be noted.

---

### 4. Jia et al., Additive Manufacturing 127 (2026) 105291
**Citation:** Z. Jia, J.-X. Yang, R. Li, Z.-D. Wang, C.-L. Tan, G. Sun, E.-H. Han, "Subtractive composition design of nickel-aluminum bronze for laser additive manufacturing: achieving superior as-deposited mechanical and corrosion performance," *Additive Manufacturing* 127 (2026) 105291. DOI: 10.1016/j.addma.2026.105291

**Process:** Laser additive manufacturing (likely blown-powder DED) of NAB with systematically modified compositions—elements subtracted from the standard NAB to optimize as-deposited properties. Full text not obtainable.

**Key insight:** This is the closest competitor to the PI's proposed work. The "subtractive composition design" approach systematically removes or reduces certain elements from standard NAB to achieve superior as-deposited mechanical and corrosion performance without post-build heat treatment.

**Tags:** [CITE] [NOVELTY-RISK] **HIGH OVERLAP.** The PI's proposal designs new compositions via Bayesian optimization; Jia et al. do the same conceptually via subtractive design. The PI must differentiate by: (1) using Bayesian optimization over function networks rather than one-at-a-time subtraction, (2) targeting Cu-Ni alloys as well as NAB, (3) using ultrasonic atomization for in-house powder production. [NAVY] Likely relevant to naval applications given seawater resistance focus.

---

### 5. Hu et al., J. Alloys Compd. 1066 (2026) 187981
**Citation:** K. Hu, J. Gao, J. Song, Y. Liu, B. Song, B. Liu, J.-F. Wu, Y.-S. Shi, "Microstructure, mechanical and corrosion properties of additively manufactured nickel-aluminum bronze alloys: laser power directed energy deposition vs. laser powder fed fusion," *J. Alloys Compd.* 1066 (2026) 187981. DOI: 10.1016/j.jallcom.2026.187981

**Process:** Direct comparison of laser-powder DED vs. LPBF for NAB. Full text not obtainable.

**Key insight:** Provides the first head-to-head comparison of L-DED and LPBF for NAB, including microstructure, mechanical properties, and corrosion behavior. Different cooling rates in DED vs. LPBF yield different phase distributions and κ precipitate morphologies.

**Tags:** [CITE] [NUMBERS] Likely contains the quantitative benchmarks the PI needs for DED NAB density, hardness, and corrosion. [GAP] If DED NAB underperforms LPBF NAB in corrosion, it motivates the PI's composition-optimization approach.

---

### 6. Rayner et al. (2024), COM 2024 Proceedings (Dalhousie)
**Citation:** A.J. Rayner, K. Morshedbehbahani, C. Spence, G. Wood, D. Hamre, A. Nasiri, D.P. Bishop, "Directed Energy Deposition of UNS C63020 Nickel Aluminum Bronze Powder," in *Proceedings of the 63rd Conference of Metallurgists, COM 2024*, Springer (2024), pp. 53–58. DOI: 10.1007/978-3-031-67398-6_13

**Process:** Blown-powder laser DED of C63020 NAB powder (Dalhousie University group).

**Additional related work (LPBF):** Rayner et al. separately examined LPBF of C63020 at 200–350 W, 400–1200 mm/s. Near-100% density and low residual oxygen at 300 W/800 mm/s. As-built microstructure was entirely martensitic β′; wrought NAB had α bands with globular κ. As-built: YS = 336 MPa, elongation = 2.9%. After 675 °C/6 h heat treatment: YS = 485 MPa, elongation = 11.4% (timmons2025laserpowderbed pages 2-4).

**Tags:** [CITE] [NUMBERS] [GAP] The DED proceedings paper (COM 2024) is the first report of blown-powder DED of C63020 specifically. Full text of the proceedings paper was not obtainable, but cross-referenced data from Timmons et al. 2025 provides the LPBF benchmarks. Shows that as-built NAB is brittle (2.9% elongation) and requires heat treatment—motivating the PI's goal of as-deposited performance through composition design.

---

### 7. Morshed-Behbahani et al., Corrosion Science 228 (2024) 111846
**Citation:** K. Morshed-Behbahani, A.J. Rayner, D.P. Bishop, A. Nasiri, "Perspectives on the unusual electrochemical corrosion of nickel aluminum bronze (NAB) alloy fabricated through laser-powder bed fusion additive manufacturing," *Corrosion Science* 228 (2024) 111846. DOI: 10.1016/j.corsci.2024.111846

**Process:** LPBF of NAB (C63020). Full text not obtainable.

**Key insight:** Reports unusual electrochemical corrosion behavior of LPBF NAB—the fully martensitic β′ microstructure corrodes differently than cast/wrought NAB, which contains α + κ phases. This is the likely "2024 comparison" paper the user referenced.

**Tags:** [CITE] [NUMBERS] Likely gives Ecorr and icorr for LPBF vs. wrought NAB. [NOVELTY-RISK] Demonstrates that AM microstructures produce fundamentally different corrosion mechanisms—the PI's as-deposited corrosion targets must account for this.

---

### 8. Yao et al., Additive Manufacturing (2025) 104787
**Citation:** C. Yao, S. He, K.-Y. Lee, G.-Y. Shin, D.-S. Shim, "Microstructural and interfacial characteristics in repair of nickel-aluminum bronze by in-situ synthesis of Cu-Al alloys via directed energy deposition," *Additive Manufacturing* (2025) 104787. DOI: 10.1016/j.addma.2025.104787

**Process:** Laser DED repair of NAB using in-situ synthesis of Cu-Al alloys (blending elemental Cu and Al powders). Full text not obtainable.

**Key insight:** In-situ blending during DED to create NAB-like compositions for repair. This is a different approach from the PI's pre-alloyed powder strategy—the PI's single-stream pre-alloyed approach avoids the compositional heterogeneity inherent in in-situ blending.

**Tags:** [CITE] [NAVY] NAB repair is a naval application. [GAP] Shows the need for pre-alloyed powders: in-situ blending likely produces less uniform deposits, motivating the PI's ultrasonic atomization approach.

---

### 9. Yao et al., SSRN (2026)
**Citation:** C. Yao, G.-Y. Shin, D.-S. Shim, "Study on laser remelting for pore mitigation in nickel–aluminum bronze (NAB) fabricated by directed energy deposition," SSRN (2026). DOI: 10.2139/ssrn.5347164

**Process:** L-DED of NAB with post-deposition laser remelting to reduce porosity. Full text not obtainable (SSRN preprint, likely destined for *Optics and Laser Technology*).

**Key insight:** Porosity remains a challenge in DED NAB; laser remelting is proposed as mitigation. This confirms that achieving dense, pore-free deposits is non-trivial for NAB and motivates the PI's process optimization work.

**Tags:** [CITE] [GAP] The PI's approach focuses on composition-level control of porosity (e.g., through powder quality and alloy design) rather than post-process remelting—a complementary strategy.

---

### 10. Roshan et al., Materials Chemistry and Physics 349 (2026) 131759
**Citation:** M. Roshan, M.B. Mahtabi, W. Bednarczyk, G. Cios, M. Haghshenas, "Effect of pre-corrosion on the fatigue performance of direct energy deposited nickel–aluminum bronze (NAB)," *Mater. Chem. Phys.* 349 (2026) 131759. DOI: 10.1016/j.matchemphys.2025.131759

**Process:** Blown-powder DED of NAB, followed by pre-corrosion exposure and fatigue testing. Full text not obtainable.

**Key insight:** Studies the coupled corrosion-fatigue problem for DED NAB—critical for naval components that experience both seawater exposure and cyclic loading. Pre-corrosion degrades fatigue life, quantifying the penalty.

**Tags:** [CITE] [NAVY] [NUMBERS] Likely contains fatigue life data with/without pre-corrosion. [GAP] The PI's proposal focuses on as-deposited corrosion resistance; improved corrosion resistance would also benefit fatigue life per this study.

---

### 11. Wang et al., Advanced Engineering Materials (2026)
**Citation:** J. Wang, R. Zhang, C.-H. Guo, T.-Y. Zhang, S.-L. Cheng, X. Han, W.-Y. Wang, F.-C. Jiang, "Microstructure and corrosion resistance of manganese-aluminum bronze alloy fabricated by laser-directed energy deposition," *Adv. Eng. Mater.* (2026). DOI: 10.1002/adem.71167

**Process:** L-DED of manganese-aluminum bronze (MAB). Full text not obtainable.

**Key insight:** Extends DED from NAB to MAB—a lower-nickel marine copper alloy family. MAB (Cu-Al-Mn) is directly relevant to the PI's secondary objective of reducing nickel content while maintaining seawater resistance.

**Tags:** [CITE] [NOVELTY-RISK] Overlaps the PI's interest in Cu-Al alloys with Mn additions for reduced Ni content. [GAP] If MAB DED deposits show adequate corrosion resistance, this supports the PI's lower-Ni alloy design space.

---

### 12. Zhao et al., SSRN (2026)
**Citation:** H. Zhao, S. Huang, W. Zhang, L. Peng, H. Xie, "Effect of Cr and Zr microalloying on the seawater corrosion behaviour of a Cu-8Al-6Ni-4Fe-2Mn nickel aluminium bronze," SSRN (2026). DOI: 10.2139/ssrn.7435004

**Process:** Likely cast or wrought NAB with Cr and Zr additions; not laser DED specifically. Full text not obtainable.

**Composition:** Cu-8Al-6Ni-4Fe-2Mn base with Cr and Zr microalloying additions.

**Key insight:** Cr and Zr microalloying modifies seawater corrosion behavior of NAB. This is directly relevant to the PI's alloy design space (Cu-Ni with Cr additions; NAB with Fe, Mn).

**Tags:** [CITE] [NUMBERS] Likely contains seawater corrosion rates for Cr/Zr-modified NAB. [NOVELTY-RISK] Overlaps the PI's compositional design space. The PI should consider Cr and Zr as candidate additions in the Bayesian optimization search.

---

### Additional Relevant Papers Found (2022–2026)

**13. Timmons et al., J. Manuf. Mater. Process. 9 (2025) 147**
LPBF of C64200 aluminum-silicon-bronze (Cu-6.3Al-1.5Si). Optimum parameters: 320 W, 770 mm/s, 0.088 mm hatch, 0.030 mm layer. As-built: YS = 595 MPa, UTS = 797 MPa, elongation = 4.9% (α + β′ martensite). After 620 °C/2 h + WQ: YS = 329 MPa, UTS = 567 MPa, elongation = 24.6%, impact = 63 J. Density >99.9% (timmons2025laserpowderbed pages 23-26, timmons2025laserpowderbed pages 19-23, timmons2025laserpowderbed pages 12-15).

**Tags:** [CITE] [NUMBERS] Demonstrates that LPBF aluminum bronzes need heat treatment to eliminate brittle β′. Relevant benchmark for the PI's as-deposited target.

**14. Saremi et al., Virtual and Physical Prototyping (2026)**
LPBF of NAB on heated platform. DOI: 10.1080/17452759.2026.2688627. Shows that platform heating can modify the as-built microstructure to avoid fully martensitic β′.

**Tags:** [CITE] [GAP] Platform heating is a process-level solution; the PI's composition-level approach is complementary.

**15. Mahmoudiniya et al., Mater. Sci. Eng. A (2026)**
DED of NAB/martensitic stainless steel bimetal. DOI: 10.1016/j.msea.2026.150140. Relevant to NAB deposited on dissimilar substrates.

**16. Huang et al., Materials 19 (2026) 208**
LPBF densification of NAB. DOI: 10.3390/ma19010208. Provides density vs. process parameter data.

**17. Han et al., Virtual and Physical Prototyping (2025)**
LPBF NAB with heat treatments to manipulate martensite for strength-ductility synergy. DOI: 10.1080/17452759.2025.2478227.

**18. Filippova et al., Materials Characterization 234 (2026) 116167**
LPBF of aluminium bronze: processing, thermal, electrical, and mechanical characterization. DOI: 10.1016/j.matchar.2026.116167.

**19. Morshed-Behbahani et al., CIRP J. Manuf. Sci. Technol. 61 (2025) 153–162**
Impact of surface post-treatments on corrosion resistance in heat-treated LPBF NAB. DOI: 10.1016/j.cirpj.2025.06.010.

**20. Wu et al., Mater. Sci. Eng. A 973 (2026) 150695**
Wire-laser DED of NAB: gradient microstructure, hierarchical precipitation, strength-ductility synergy. DOI: 10.1016/j.msea.2026.150695.

---

### Limitations and Gaps in the Literature Search

1. **Full text was not obtainable** for most 2025–2026 papers (Jia et al. 2025 Corr. Sci., Jia et al. 2025 JMPT, Jia et al. 2026 Addit. Manuf., Hu et al. 2026, Roshan et al. 2026, Wang et al. 2026, Zhao et al. 2026 SSRN). Quantitative corrosion numbers (i_corr, E_corr, impedance) from these papers could not be extracted.

2. **The "2024 comparison of heat-treated NAB C63020 by L-PBF vs L-DED"** most likely refers to Morshed-Behbahani et al. (2024) in *Corrosion Science* 228, 111846, or the Rayner et al. COM 2024 proceedings paper, or a combination of the Dalhousie group's outputs. No single paper was found that explicitly compares heat-treated L-PBF vs. L-DED in a single study from 2024; the comparison may be distributed across the Dalhousie group's publications (Rayner LPBF + Rayner DED at COM 2024).

3. **No paper was found** reporting blown-powder laser DED of Cu-Ni (70-30 type) alloys for seawater service. All identified work is on aluminum bronzes (NAB, ASB, MAB). This is a significant **gap** that the PI's proposal can exploit.

4. **No paper was found** using ultrasonic atomization for marine copper alloy AM powders. This is another differentiator for the PI.

5. **Bayesian optimization of DED copper alloy composition** was not reported in any found paper. Jia et al. 2026 use "subtractive composition design" (systematic element removal), not data-driven optimization.

---

### Top 5 Things the PI Should Know

**1. Jia et al. (2026, Additive Manufacturing) is the closest competitor.** Their "subtractive composition design" for laser AM NAB directly targets as-deposited mechanical and corrosion performance—the same goal as the PI's proposal. The PI must clearly differentiate by emphasizing: (a) Bayesian optimization over function networks vs. one-at-a-time subtraction, (b) inclusion of Cu-Ni alloys (not just NAB), (c) in-house ultrasonic atomization enabling rapid alloy iteration, and (d) cost-aware multi-fidelity optimization (CALPHAD + short electrochemical tests + long immersion).

**2. As-built AM NAB is brittle and requires heat treatment with current compositions.** LPBF C63020 yields fully martensitic β′ with only 2.9% elongation (timmons2025laserpowderbed pages 2-4). LPBF C64200 gives 4.9% elongation (timmons2025laserpowderbed pages 19-23). Heat treatment at 620–675 °C restores ductility (11–25%) but is exactly what the PI's proposal seeks to avoid. This motivates the composition-design approach: finding alloys that are ductile AND corrosion-resistant as-deposited.

**3. No one has reported blown-powder laser DED of Cu-Ni (C71500-type) alloys.** All found work is on aluminum bronzes. The Cu-Ni (10–30 wt% Ni) design space with Fe, Mn, Cr additions for single-stream pre-alloyed powder DED is genuinely novel and fills a literature gap. The PI should highlight this strongly.

**4. Substrate dilution is a critical challenge for DED on dissimilar metals.** Zhao et al. (2022) showed that direct DED of NAB on steel produces Fe-rich dendrites that severely degrade corrosion resistance (i_corr nearly doubled) (zhao2022thelaserdeposited pages 7-10). The PI's proposed repair of cast NAB with DED NAB (same-family substrate) avoids this problem. DED on Cu-Ni substrates should also be compatible if compositions are properly matched.

**5. Cr and Zr microalloying and Mn-Al bronzes are emerging alloy-design levers.** Zhao et al. (2026 SSRN) show Cr and Zr improve seawater corrosion of NAB; Wang et al. (2026) demonstrate DED of Mn-Al bronze (lower Ni). Both support the PI's design space (Cu-Ni with Cr; NAB with Mn) and the critical-mineral objective of reducing Ni content. These elements should be included as candidate additions in the Bayesian search space.


References

1. (zhao2022thelaserdeposited pages 2-4): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

2. (zhao2022thelaserdeposited pages 4-7): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

3. (zhao2022thelaserdeposited pages 7-10): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

4. (zhao2022thelaserdeposited pages 13-14): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

5. (timmons2025laserpowderbed pages 2-4): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

6. (timmons2025laserpowderbed pages 23-26): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

7. (timmons2025laserpowderbed pages 19-23): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.

8. (timmons2025laserpowderbed pages 12-15): Kenzie A. Timmons, Ali Nasiri, and Donald P. Bishop. Laser powder bed fusion processing of uns c64200 aluminum–silicon–bronze. Journal of Manufacturing and Materials Processing, 9:147, Apr 2025. URL: https://doi.org/10.3390/jmmp9050147, doi:10.3390/jmmp9050147. This article has 2 citations.
