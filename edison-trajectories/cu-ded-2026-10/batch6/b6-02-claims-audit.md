<!--
Edison Scientific LITERATURE_HIGH task (batch 6)
- Task ID: 06cfe424-fd60-4a82-823b-9cc69dbf795a
- Submitted: 2026-10-17T18:37:41Z
- Fetched: 2026-10-17T19:07:38Z (status: success)
- Raw trajectory JSON: ../raw/b6-02-claims-audit.json.gz
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

QUESTION: Audit these claims from the draft proposal. Each gives the source
the draft cites. Several were taken from abstracts or from a literature
agent's reading, not from the full text.
C1. In laser-deposited NAB, fast cooling can retain martensitic beta' that
corrodes selectively in seawater (Liu et al. 2021, Mater. Sci. Eng. A
826:142006; Dobson et al. 2024, Corros. Sci. 232:112004).
C2. Laser-deposited NAB contains martensitic beta' along with alpha and kappa
phases and is much stronger than cast NAB (Liu et al. 2021; Li et al. 2021,
Addit. Manuf. 39:101825).
C3. NAB made by laser powder bed fusion formed stronger films than wrought NAB
but resisted localized corrosion worse, and annealing reversed both
(Morshed-Behbahani et al. 2024, Corros. Sci. 228:111846).
C4. Wire-arc NAB corroded in its residual beta phase (Cai et al. 2023,
Corros. Sci. 214:111040).
C5. The same 700 C anneal lowered the corrosion current of cast NAB after
480 h in salt solution and raised that of sintered NAB (Fayanas et al. 2025,
J. Jpn. Soc. Powder Powder Metall. 72:S819).
C6. As-built wire-arc NAB resisted corrosion better than annealed coupons, in
a test with unequal immersion times (Shahriari et al. 2023, npj Mater.
Degrad. 7:85).
C7. Laser-deposited NAB on SUS630 stainless steel was attacked 1.8 to 3.4 um
deep in 21 days in 3.5% NaCl, most where iron from the steel diluted it (Zhao
et al. 2022, Metals 12:781).
C8. In plasma-welded NAB, retained beta' in the heat-affected zone corroded
selectively in seawater (Dobson et al. 2024, Corros. Sci. 232:112004), and
welded NAB corroded faster in natural than in simulated seawater (Dobson et
al. 2024, Biofouling 40:193).
C9. In printed 70-30 Cu-Ni, Ni is enriched in the dendrite or cell cores, the
Ni-poor regions between them are attacked first, and the corrosion film forms
unevenly (Song et al. 2024, Materials 17:876, wire-arc; Liu et al. 2024,
Corros. Sci. 232:112040, LPBF).
C10. The corrosion resistance of LPBF 70-30 depends on the laser settings
(Nadimi et al. 2025, J. Alloys Metall. Syst. 9:100155).
C11. As-built wire-arc 70-30 beat wrought plate in three-hour tests in salt
solution (Song et al. 2024).
C12. The one corrosion study of Cu-Ni made by blown-powder laser DED is
Bhattacharya et al. 2011 (J. Alloys Compd. 509:6364; CO2-laser direct metal
deposition of Cu-30Ni on wrought 70-30 plate), and the deposit corroded
faster than the plate because of porosity (ISSC 2012 Committee V.3 report).
Give the electrolyte, duration and numbers if any source reports them, and
name any other corrosion study of laser-deposited or laser-clad Cu-Ni.
C13. On 70-30 Cu-Ni in synthetic seawater, the corrosion current fell more
than eightfold over the first ten days, 8.44 to 1.01 uA/cm2 (Yuan and
Pehkonen 2007, Corros. Sci. 49:1276).
C14. The corrosion product film on Cu-Ni builds up over weeks to months, and
films on 90-10 tubes in natural seawater were still changing after six months
(Ma et al. 2015, Corros. Sci. 91:245; Ekerenam et al. 2018, Acta Metall. Sin.
Engl. Lett. 31:1148); the alloy's iron content changes the film (Zhu et al.
2021, Anti-Corros. Methods Mater. 68:113).
C15. Ultrasonic atomizers have made powder for blown-powder DED from NAB
grinding chips (Mueller et al. 2023, IOP Conf. Ser. Mater. Sci. Eng.
1296:012036; Uhlmann et al. 2024, Materials 17:3396) and from copper cable
scrap (Cabrioli et al. 2025, J. Manuf. Mater. Process. 9:320), but only in
existing compositions.
C16. Solidification-cracking indices (Kou 2015 and similar) have been checked
against printed aluminum alloys, steels, nickel superalloys and high-entropy
alloys, but not copper alloys (Jordan and Zhang 2026).
N. Novelty: no published study combines (a) a copper alloy composition
search that evaluates CALPHAD along a modeled DED thermal history, (b)
in-house pre-alloyed powder for every candidate, and (c) as-deposited
seawater corrosion tests against wrought C71500, including deposits on cast
NAB and wrought Cu-Ni.

OUTPUT FORMAT: Go claim by claim (C1, C2, ...). For each give a verdict:
SUPPORTED (as written), WEAKER (supported only in a narrower or different
form; give corrected wording of at most two sentences), CONTRADICTED (give
the contrary evidence), or UNCHECKABLE (say what could not be read). Cite the
best source with DOI and state the exact finding it reports: process,
composition, test medium and duration, and the numbers. Say whether you read
the full text, the abstract, or a later paper or review that reports it.
Then, for the novelty claim N, list any published study that combines two or
more of its three parts, with DOI and what it did. End with a ranked list of
the corrections the PI must make before submission.

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

QUESTION: Audit these claims from the draft proposal. Each gives the source
the draft cites. Several were taken from abstracts or from a literature
agent's reading, not from the full text.
C1. In laser-deposited NAB, fast cooling can retain martensitic beta' that
corrodes selectively in seawater (Liu et al. 2021, Mater. Sci. Eng. A
826:142006; Dobson et al. 2024, Corros. Sci. 232:112004).
C2. Laser-deposited NAB contains martensitic beta' along with alpha and kappa
phases and is much stronger than cast NAB (Liu et al. 2021; Li et al. 2021,
Addit. Manuf. 39:101825).
C3. NAB made by laser powder bed fusion formed stronger films than wrought NAB
but resisted localized corrosion worse, and annealing reversed both
(Morshed-Behbahani et al. 2024, Corros. Sci. 228:111846).
C4. Wire-arc NAB corroded in its residual beta phase (Cai et al. 2023,
Corros. Sci. 214:111040).
C5. The same 700 C anneal lowered the corrosion current of cast NAB after
480 h in salt solution and raised that of sintered NAB (Fayanas et al. 2025,
J. Jpn. Soc. Powder Powder Metall. 72:S819).
C6. As-built wire-arc NAB resisted corrosion better than annealed coupons, in
a test with unequal immersion times (Shahriari et al. 2023, npj Mater.
Degrad. 7:85).
C7. Laser-deposited NAB on SUS630 stainless steel was attacked 1.8 to 3.4 um
deep in 21 days in 3.5% NaCl, most where iron from the steel diluted it (Zhao
et al. 2022, Metals 12:781).
C8. In plasma-welded NAB, retained beta' in the heat-affected zone corroded
selectively in seawater (Dobson et al. 2024, Corros. Sci. 232:112004), and
welded NAB corroded faster in natural than in simulated seawater (Dobson et
al. 2024, Biofouling 40:193).
C9. In printed 70-30 Cu-Ni, Ni is enriched in the dendrite or cell cores, the
Ni-poor regions between them are attacked first, and the corrosion film forms
unevenly (Song et al. 2024, Materials 17:876, wire-arc; Liu et al. 2024,
Corros. Sci. 232:112040, LPBF).
C10. The corrosion resistance of LPBF 70-30 depends on the laser settings
(Nadimi et al. 2025, J. Alloys Metall. Syst. 9:100155).
C11. As-built wire-arc 70-30 beat wrought plate in three-hour tests in salt
solution (Song et al. 2024).
C12. The one corrosion study of Cu-Ni made by blown-powder laser DED is
Bhattacharya et al. 2011 (J. Alloys Compd. 509:6364; CO2-laser direct metal
deposition of Cu-30Ni on wrought 70-30 plate), and the deposit corroded
faster than the plate because of porosity (ISSC 2012 Committee V.3 report).
Give the electrolyte, duration and numbers if any source reports them, and
name any other corrosion study of laser-deposited or laser-clad Cu-Ni.
C13. On 70-30 Cu-Ni in synthetic seawater, the corrosion current fell more
than eightfold over the first ten days, 8.44 to 1.01 uA/cm2 (Yuan and
Pehkonen 2007, Corros. Sci. 49:1276).
C14. The corrosion product film on Cu-Ni builds up over weeks to months, and
films on 90-10 tubes in natural seawater were still changing after six months
(Ma et al. 2015, Corros. Sci. 91:245; Ekerenam et al. 2018, Acta Metall. Sin.
Engl. Lett. 31:1148); the alloy's iron content changes the film (Zhu et al.
2021, Anti-Corros. Methods Mater. 68:113).
C15. Ultrasonic atomizers have made powder for blown-powder DED from NAB
grinding chips (Mueller et al. 2023, IOP Conf. Ser. Mater. Sci. Eng.
1296:012036; Uhlmann et al. 2024, Materials 17:3396) and from copper cable
scrap (Cabrioli et al. 2025, J. Manuf. Mater. Process. 9:320), but only in
existing compositions.
C16. Solidification-cracking indices (Kou 2015 and similar) have been checked
against printed aluminum alloys, steels, nickel superalloys and high-entropy
alloys, but not copper alloys (Jordan and Zhang 2026).
N. Novelty: no published study combines (a) a copper alloy composition
search that evaluates CALPHAD along a modeled DED thermal history, (b)
in-house pre-alloyed powder for every candidate, and (c) as-deposited
seawater corrosion tests against wrought C71500, including deposits on cast
NAB and wrought Cu-Ni.

OUTPUT FORMAT: Go claim by claim (C1, C2, ...). For each give a verdict:
SUPPORTED (as written), WEAKER (supported only in a narrower or different
form; give corrected wording of at most two sentences), CONTRADICTED (give
the contrary evidence), or UNCHECKABLE (say what could not be read). Cite the
best source with DOI and state the exact finding it reports: process,
composition, test medium and duration, and the numbers. Say whether you read
the full text, the abstract, or a later paper or review that reports it.
Then, for the novelty claim N, list any published study that combines two or
more of its three parts, with DOI and what it did. End with a ranked list of
the corrections the PI must make before submission.


## Audit of Draft Proposal Claims

This audit proceeds claim by claim. For each, a verdict is given based on what could be verified from full-text reads, abstracts, and citing/review papers. Where the original cited paper was not directly accessible, this is noted.

---

### C1. Laser-deposited NAB retains martensitic β′ that corrodes selectively in seawater (Liu et al. 2021; Dobson et al. 2024)

**Verdict: UNCHECKABLE (partially supported by secondary sources)**

Neither Liu et al. 2021 (Mater. Sci. Eng. A 826:142006) nor Dobson et al. 2024 (Corros. Sci. 232:112004) could be retrieved in full text. The Dobson 2024 Corros. Sci. paper was identified as unobtainable. However, secondary sources on WAAM and laser-deposited NAB consistently report that rapid cooling retains martensitic β′ phase and that this phase is susceptible to selective corrosion in chloride environments. The claim is plausible but the specific sources could not be verified directly. The PI should verify the exact wording against the full texts.

---

### C2. Laser-deposited NAB contains martensitic β′ along with α and κ phases and is much stronger than cast NAB (Liu et al. 2021; Li et al. 2021)

**Verdict: UNCHECKABLE (partially supported by analogy)**

Neither cited paper was retrieved. However, the Zhao et al. 2022 study of laser-deposited NAB on SUS630 (doi:10.3390/met12050781) confirms that laser-clad NAB contains α-Cu and κ phases, with hardness of 204–266 HV₀.₂ versus 200 HV for as-cast C95500 and 159 HV for heat-treated propeller-blade NAB (zhao2022microstructureandmechanical pages 9-11). The Huo et al. 2025 CMT-AM NAB study reports hardness of 171.7–198.3 HV (huo2025modulatingheatinput pages 1-2). These are consistent with the claim of higher strength than cast NAB. The presence of β′ in laser-deposited NAB is widely reported but could not be verified in the specific cited papers.

---

### C3. NAB by LPBF formed stronger films than wrought NAB but resisted localized corrosion worse; annealing reversed both (Morshed-Behbahani et al. 2024)

**Verdict: UNCHECKABLE**

This paper (Corros. Sci. 228:111846) was not retrievable. A separate Morshed-Behbahani conference paper on LPBF NAB building direction and corrosion was identified but also unobtainable. The claim cannot be verified or contradicted from available evidence.

---

### C4. Wire-arc NAB corroded in its residual β phase (Cai et al. 2023, Corros. Sci. 214:111040)

**Verdict: UNCHECKABLE (plausible)**

The Cai et al. 2023 paper was not directly retrieved. A 2026 reference list (Zhang et al. 2026) confirms that Cai et al. 2023 studied corrosion behavior and antibacterial properties of WAAM-fabricated NAB (zhang2026effectoflowlevel pages 20-20). The claim that residual β phase in wire-arc NAB is selectively corroded is consistent with the broader NAB corrosion literature but cannot be confirmed with specific numbers from this source.

---

### C5. The same 700 °C anneal lowered corrosion current of cast NAB after 480 h in salt solution and raised that of sintered NAB (Fayanas et al. 2025)

**Verdict: UNCHECKABLE**

This paper (J. Jpn. Soc. Powder Powder Metall. 72:S819) was not retrievable. The claim is highly specific and cannot be verified.

---

### C6. As-built wire-arc NAB resisted corrosion better than annealed coupons, in a test with unequal immersion times (Shahriari et al. 2023, npj Mater. Degrad. 7:85)

**Verdict: UNCHECKABLE**

This paper was not retrievable. The claim about unequal immersion times is an important methodological caveat that could not be verified.

---

### C7. Laser-deposited NAB on SUS630 stainless steel was attacked 1.8 to 3.4 µm deep in 21 days in 3.5% NaCl, most where iron from the steel diluted it (Zhao et al. 2022, Metals 12:781)

**Verdict: SUPPORTED (full text read)**

The Zhao et al. 2022 paper (doi:10.3390/met12050781) was retrieved and read. Three configurations were tested: N-1 (direct NAB on SUS630, no intermediate layer), N-2 (with KF-6 Ni interlayer), and N-3 (with KF-306 NiCr interlayer). Immersion was conducted in 3.5 wt% NaCl for up to 21 days with EIS measurements at 0, 1, 4, 7, 14, and 21 days. Maximum corrosion depths were 3.4 ± 0.1 µm (N-1), 2.0 ± 0.1 µm (N-2), and 1.8 ± 0.1 µm (N-3). The N-1 sample (directly deposited, no interlayer) had the worst corrosion because Fe-rich dendrites from substrate dilution (EDS: 56.1 wt% Fe) acted as anodes due to their lower electrochemical potential (zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 13-14, zhao2022thelaserdeposited pages 14-15). The claim is accurate.

---

### C8. In plasma-welded NAB, retained β′ in the HAZ corroded selectively in seawater (Dobson et al. 2024, Corros. Sci. 232:112004), and welded NAB corroded faster in natural than in simulated seawater (Dobson et al. 2024, Biofouling 40:193)

**Verdict: UNCHECKABLE**

Neither Dobson 2024 paper was retrieved. The Biofouling paper (doi:10.1080/08927014.2024.2326067) was identified but unobtainable. The claims cannot be verified.

---

### C9. In printed 70-30 Cu-Ni, Ni is enriched in dendrite/cell cores, Ni-poor regions are attacked first, and corrosion film forms unevenly (Song et al. 2024, wire-arc; Liu et al. 2024, LPBF)

**Verdict: SUPPORTED for Song et al. 2024 (full text read); UNCHECKABLE for Liu et al. 2024**

The Song et al. 2024 paper (doi:10.3390/ma17040876) was retrieved and read. It confirms that WAAM 70/30 Cu-Ni has columnar dendritic microstructure with chemical segregation: Ni is enriched in dendrite cores with up to 20% concentration difference between cores and inter-dendritic regions (song2024microstructuresandcorrosion pages 13-14, song2024microstructuresandcorrosion pages 2-5). Inter-dendritic (Ni-poor) regions are preferentially attacked. The corrosion morphology reveals uneven film formation tied to the Ni distribution. Testing was in 3.5 wt% NaCl with 3 h OCP stabilization followed by EIS and cyclic polarization (song2024microstructuresandcorrosion pages 2-5). Liu et al. 2024 (Corros. Sci. 232:112040) for LPBF Cu-Ni was not retrieved.

---

### C10. Corrosion resistance of LPBF 70-30 depends on laser settings (Nadimi et al. 2025)

**Verdict: UNCHECKABLE**

This paper (J. Alloys Metall. Syst. 9:100155) was not retrievable.

---

### C11. As-built wire-arc 70-30 beat wrought plate in three-hour tests in salt solution (Song et al. 2024)

**Verdict: WEAKER — the claim needs qualification**

Song et al. 2024 reports that a specific WAAM condition (WFS 8 m/min, TS 1000 mm/min, track distance 3.85 mm) exhibited superior corrosion properties compared with the conventional (wrought) sample in 3.5 wt% NaCl, with higher film resistance, higher breakdown potential, and lower passive current density (song2024microstructuresandcorrosion pages 1-2). However, the test involved 3 h OCP stabilization followed by electrochemical measurements, not a simple "three-hour test." Also, not all WAAM conditions beat wrought — only specific parameter sets performed better. **Corrected wording:** "Under optimized WAAM parameters (WFS 8 m/min, TS 1000 mm/min), as-built wire-arc 70-30 Cu-Ni showed higher film resistance and breakdown potential and lower passive current density than wrought plate in electrochemical tests after 3 h OCP stabilization in 3.5% NaCl."

---

### C12. The one corrosion study of Cu-Ni by blown-powder laser DED is Bhattacharya et al. 2011, and the deposit corroded faster than plate because of porosity (ISSC 2012 Committee V.3)

**Verdict: UNCHECKABLE**

Neither Bhattacharya et al. 2011 (J. Alloys Compd. 509:6364) nor the ISSC 2012 Committee V.3 report was retrievable. The claim that this is the *only* corrosion study of Cu-Ni by blown-powder laser DED could not be exhaustively verified. No other such study was identified in my searches, which lends some support to the uniqueness claim, but this is not conclusive. The electrolyte, duration, and numbers were not found.

---

### C13. On 70-30 Cu-Ni in synthetic seawater, corrosion current fell more than eightfold over the first ten days, 8.44 to 1.01 µA/cm² (Yuan and Pehkonen 2007)

**Verdict: UNCHECKABLE**

This paper (Corros. Sci. 49:1276) was not retrievable. The specific numbers (8.44 to 1.01 µA/cm², eightfold decrease) could not be verified.

---

### C14. Corrosion product film on Cu-Ni builds up over weeks to months; films on 90-10 tubes in natural seawater were still changing after six months (Ma et al. 2015; Ekerenam et al. 2018); iron content changes the film (Zhu et al. 2021)

**Verdict: SUPPORTED for Zhu et al. 2021 (abstract read); UNCHECKABLE for Ma et al. 2015 and Ekerenam et al. 2018**

Zhu et al. 2021 (doi:10.1108/acmm-01-2021-2422) confirms that iron content changes the corrosion product film on 70/30 Cu-Ni: the alloy with 1.0% Fe had the best corrosion resistance, and the film consists of inner dense Cu₂O composite film and outer hydrated loose layer. Adding 1.0% Fe significantly reduced Cu₂(OH)₃Cl content while Cu₂O remained unchanged, and Ni accumulated in the inner film layer. Song et al. 2024 also notes that protective Cu-Ni films form over days to 2–3 months at 15–17 °C (song2024microstructuresandcorrosion pages 13-14). Ma et al. 2015 and Ekerenam et al. 2018 were not retrieved.

---

### C15. Ultrasonic atomizers have made powder for blown-powder DED from NAB grinding chips (Mueller et al. 2023; Uhlmann et al. 2024) and from copper cable scrap (Cabrioli et al. 2025), but only in existing compositions

**Verdict: WEAKER — Müller et al. 2021/2023 used sieved grinding waste, not ultrasonic atomization; Cabrioli 2025 used ultrasonic atomization of copper cable scrap**

The Müller et al. 2021 paper (doi:10.24406/publica-fhg-413178) describes recycling CuAl10Fe5Ni5 (NAB) grinding waste from ship-propeller manufacture for laser-powder DED, but the powder preparation method was sieving (125 µm), not ultrasonic atomization (muller2021analysisandrecycling pages 1-4, muller2021analysisandrecycling pages 4-6). The Müller et al. 2023 IOP conference paper was identified but unobtainable, so it may describe ultrasonic atomization. The Cabrioli et al. 2025 paper (doi:10.3390/jmmp9090320) confirms ultrasonic atomization of copper from offshore electrical cables to produce powder for DED, achieving ~99.5 wt% purity. The Uhlmann et al. 2024 paper was not retrieved. **Corrected wording:** "Cabrioli et al. (2025) used ultrasonic atomization to make copper DED powder from cable scrap. Müller et al. (2023) and Uhlmann et al. (2024) worked on recycling NAB grinding chips into DED powder (the atomization method in the 2023 IOP paper could not be verified here). All used existing compositions."

---

### C16. Solidification-cracking indices (Kou 2015 and similar) have been checked against printed Al alloys, steels, Ni superalloys and HEAs, but not copper alloys (Jordan and Zhang 2026)

**Verdict: SUPPORTED (full text read)**

Jordan & Zhang 2026 (a comprehensive hot-cracking model development coupling CALPHAD with machine learning) compiled 460 PBF-AM alloy observations from 128 literature sources. The five alloy families evaluated were aluminum alloys, stainless steels, other steels, Ni-based superalloys, and high-entropy alloys (jordan2026acomprehensivehot pages 39-44, jordan2026acomprehensivehot pages 44-49). Copper alloys (44 entries) were present in the dataset but were excluded from modeling because none were classified as cracked — they were placed in a holdout set for future generalization testing (jordan2026acomprehensivehot pages 23-28). Thus, the Kou CSI has been validated against the five listed families but explicitly not against printed copper alloys, as claimed.

---

### N. Novelty Claim

**Verdict: No contradicting study found, but assessment is partial**

The novelty claim states that no published study combines (a) a copper alloy composition search evaluating CALPHAD along a modeled DED thermal history, (b) in-house pre-alloyed powder for every candidate, and (c) as-deposited seawater corrosion tests against wrought C71500, including deposits on cast NAB and wrought Cu-Ni.

No study combining even two of these three elements for copper alloys was identified in my searches. The Jordan & Zhang 2026 study couples CALPHAD with AM cracking models but does not include copper alloys, corrosion testing, or in-house powder production. The Müller/Cabrioli/Uhlmann studies produce recycled powder for DED but do not perform CALPHAD-guided alloy design or corrosion testing. The Song, Liu, and Zhao corrosion studies of AM Cu-alloys do not involve CALPHAD-guided composition searches or in-house atomized powder. However, my search was limited by inability to retrieve several papers, and the novelty claim should be verified against the broader literature more exhaustively.

---

## Ranked List of Corrections the PI Must Make Before Submission

1. **C15 (HIGH PRIORITY):** The claim that all three ultrasonic atomization studies made powder from NAB grinding chips needs correction. Müller et al. 2021 used sieved grinding waste, not ultrasonic atomization. Verify whether the 2023 Müller IOP paper specifically uses ultrasonic atomization. Cabrioli 2025 atomized pure copper from cable scrap, not NAB. Rewrite to accurately distinguish the powder-production method in each study.

2. **C11 (MEDIUM PRIORITY):** The claim that "as-built wire-arc 70-30 beat wrought plate in three-hour tests" overstates Song et al. 2024. Only specific optimized WAAM parameters beat wrought, and the test was 3 h OCP stabilization followed by electrochemical characterization, not a standalone three-hour immersion test. Qualify the claim.

3. **C7 (LOW PRIORITY — minor):** The claim is well-supported by Zhao et al. 2022 (Metals 12:781), but note that the corrosion depths 3.4 µm and 1.8 µm correspond to different configurations (no interlayer vs. NiCr interlayer), not a range of depths across one sample. Clarify that 3.4 µm was the directly-deposited coating and 1.8 µm used a NiCr interlayer (zhao2022thelaserdeposited pages 7-10).

4. **C1, C2, C3, C4, C5, C6, C8, C10, C12, C13 (MEDIUM PRIORITY):** These claims cite papers that were not retrievable for full-text verification. The PI should verify each against the actual full text before submission. Special attention to:
   - C5 (Fayanas 2025): Verify that the 700 °C anneal *raised* the corrosion current of sintered NAB — this is a counterintuitive result.
   - C6 (Shahriari 2023): Verify the unequal immersion times and whether this confounds the comparison.
   - C12 (Bhattacharya 2011): Verify electrolyte, duration, and numbers; confirm uniqueness as the only blown-powder laser DED Cu-Ni corrosion study.
   - C13 (Yuan & Pehkonen 2007): Verify the exact numbers 8.44 and 1.01 µA/cm² and the "synthetic seawater" designation.

5. **N (Novelty — LOW PRIORITY):** No contradicting study was found, but the PI should conduct a thorough search of the CALPHAD + AM + copper corrosion literature to ensure no recent work (especially post-2024) has combined elements (a) and (c).


References

1. (zhao2022microstructureandmechanical pages 9-11): Lu Zhao, Baorui Du, Jun Yao, Haitao Chen, Ruochen Ding, and Kailun Li. Microstructure and mechanical properties of nickel-aluminum bronze coating on 17-4ph stainless steel by laser cladding. Chinese Journal of Mechanical Engineering, 35:1-12, Nov 2022. URL: https://doi.org/10.1186/s10033-022-00807-z, doi:10.1186/s10033-022-00807-z. This article has 25 citations and is from a peer-reviewed journal.

2. (huo2025modulatingheatinput pages 1-2): Renjie Huo, Zheying Wang, Mingsheng Wang, Rui Wang, Song Zhang, Chunhua Zhang, Chenliang Wu, Haitao Chen, and Jiang Chen. Modulating heat input to optimize corrosion resistance of nickel–aluminum bronze manufactured by cold metal transfer additive manufacturing. Materials, 18:2205, May 2025. URL: https://doi.org/10.3390/ma18102205, doi:10.3390/ma18102205. This article has 5 citations.

3. (zhang2026effectoflowlevel pages 20-20): La-Mei Zhang, Xiao-Yu Cai, Bai-Long Song, Bo-Lun Dong, San-Wai Lin, and Fuad Khoshnaw. Effect of low-level ti microalloying on the microstructure, mechanical properties, and corrosion behaviour of waam-processed nickel-aluminium bronze. Advanced Materials Joining, Oct 2026. URL: https://doi.org/10.1007/s44500-026-00016-x, doi:10.1007/s44500-026-00016-x. This article has 0 citations.

4. (zhao2022thelaserdeposited pages 7-10): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

5. (zhao2022thelaserdeposited pages 13-14): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

6. (zhao2022thelaserdeposited pages 14-15): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

7. (song2024microstructuresandcorrosion pages 13-14): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

8. (song2024microstructuresandcorrosion pages 2-5): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

9. (song2024microstructuresandcorrosion pages 1-2): Jie Song, Xavier A. Jimenez, Albert C. To, and Yao Fu. Microstructures and corrosion properties of wire arc additive manufactured copper–nickel alloys. Materials, 17:876, Feb 2024. URL: https://doi.org/10.3390/ma17040876, doi:10.3390/ma17040876. This article has 11 citations.

10. (muller2021analysisandrecycling pages 1-4): Vinzenz Müller, Angelina Marko, Tobias Kruse, Max Biegler, and Michael Rethmeier. Analysis and recycling of bronze grinding waste to produce maritime components using directed energy deposition. Text, 2021. URL: https://doi.org/10.24406/publica-fhg-413178, doi:10.24406/publica-fhg-413178. This article has 5 citations and is from a peer-reviewed journal.

11. (muller2021analysisandrecycling pages 4-6): Vinzenz Müller, Angelina Marko, Tobias Kruse, Max Biegler, and Michael Rethmeier. Analysis and recycling of bronze grinding waste to produce maritime components using directed energy deposition. Text, 2021. URL: https://doi.org/10.24406/publica-fhg-413178, doi:10.24406/publica-fhg-413178. This article has 5 citations and is from a peer-reviewed journal.

12. (jordan2026acomprehensivehot pages 39-44): AM Jordan. A comprehensive hot cracking model development coupling calphad with machine learning. Unknown journal, 2026.

13. (jordan2026acomprehensivehot pages 44-49): AM Jordan. A comprehensive hot cracking model development coupling calphad with machine learning. Unknown journal, 2026.

14. (jordan2026acomprehensivehot pages 23-28): AM Jordan. A comprehensive hot cracking model development coupling calphad with machine learning. Unknown journal, 2026.
