<!--
Edison Scientific LITERATURE_HIGH task (batch 2)
- Task ID: fc6a3970-392a-45cb-b3f4-4db2b4664974
- Submitted: 2026-11-10T16:31:13Z
- Fetched: 2026-11-10T17:02:10Z (status: success)
- Raw trajectory JSON: ../raw/c2-01-beta-prime-attack-timescale.json.gz
- Synthesis: ../README.md
-->

Question:

CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications)
submitted an ONR FY2027 Young Investigator Program proposal in October 2026 to
design new pre-alloyed copper alloy powders for single-stream blown-powder
laser directed energy deposition (DED). Goals: deposits that are dense and
crack-free, built on themselves and deposited on cast nickel-aluminum bronze
(NAB, UNS C95800) and wrought Cu-Ni (repair), that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). The searched space is Cu at least 65 wt% with Ni 0-30,
Al 0-9.5 (upper bound set by retained beta-prime martensite as deposited),
Fe 0-4.5, Mn 0-4, Ti 0-0.5, plus Cr, Si, Nb in Cu-Ni only, with NAB family
rules (above 7 Al: Fe <= Ni <= 5.5). Powder is made in-house by ultrasonic
atomization (AMAZEMET rePOWDER, 40 kHz, induction melting up to 1300 C); the
first copper alloy run uses UNS C63000 bar (Cu-10Al-5Ni-3Fe). Blown-powder DED
is bought at the University of Utah (InssTek MX-Lab: InssTek DMT process,
ytterbium fiber laser of 500 W maximum, 0.4 mm beam, six powder feeders,
45-150 um powder) and at the Colorado School of Mines (FormAlloy X2).
InssTek's material database (summarized for the PI by InssTek) lists
"Al-Bronze / UNS C95300" as a qualified DED material: Cu balance, Al 9-11 wt%,
Fe 0.8-1.5 wt% (no nickel); typical powder size average about 83.8 um;
melting range 1040-1045 C; applications listed as ship propellers and marine
components; tensile strength of InssTek DMT-produced material 628 MPa (XY) and
598 MPa (Z). The database summary gives no yield strength, elongation,
hardness, heat treatment, laser power, machine model or corrosion data.

QUESTION: How quickly does selective phase corrosion (dealuminification) of
retained beta / martensitic beta-prime appear in aluminum bronzes and NAB in
seawater or 3.5 wt% NaCl, and can short electrochemical tests detect it?
The PI's hypothesis H5: corrosion rates, breakdown potentials and impedance
from a ONE-HOUR electrochemical screen, together with composition and
microstructure, predict which candidates pass a 30-day immersion test (mass
loss no greater than wrought 70-30 Cu-Ni; selective attack no deeper than
cast NAB). The proposal assumes the one-hour screen misses beta-prime attack,
which develops over weeks.
(1) Collect studies that measured BOTH a short electrochemical test (OCP,
LPR, EIS or polarization within about 24 h) AND longer immersion or
exposure (days to months; mass loss, selective-attack depth, cross sections)
on beta- or beta-prime-containing aluminum bronze or NAB: welds and heat-
affected zones, laser surface melted layers (e.g. Guo et al. 2026, Materials
19, 3995, where a beta-prime-rich layer did better in short NaCl tests),
laser clads, WAAM, LPBF, quenched castings. Did the short tests and the long
exposures rank the conditions the same way? Give times to first visible
selective attack and attack depth versus time where reported.
(2) Which test methods detect dealuminification quickly: potentiostatic
holds, cyclic polarization features, EIS signatures, acidified or heated
chloride, ammonia or sulfide additions, dezincification-style tests (ISO
6509 analogs) applied to aluminum bronze, scanning probes? With what
validation against long exposure?
(3) Does nickel-free aluminum bronze (Cu-9-11Al-1-4Fe, e.g. C95300, C95400,
CuAl10Fe) show selective attack of beta-prime faster or deeper than NAB with
5 Ni, for the same quench or deposit condition?
(4) What does this imply for using a deliberately beta-prime-rich deposit
(for example InssTek DMT C95300) as a known-risk control sample when testing
H5 on a small-volume well cell and in 30-day immersion?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition /
InssTek DMT, wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought,
weld overlay), the alloy composition in wt%, the condition (as deposited,
heat treated: temperature and time), the test conditions (e.g. 3.5 wt% NaCl
vs natural or substitute seawater per ASTM D1141, duration, flow), and the key
numbers (porosity/density, phase fractions, corrosion current density or rate,
Ecorr, selective-attack depth, hardness, UTS/yield/elongation with direction,
laser power/spot/speed/feed, powder size/flow/oxygen). Tag each item: [CITE]
worth citing; [NUMBERS] gives a quantitative benchmark; [NAVY] Navy/DoD-funded
or Navy application; [INSSTEK] made on an InssTek machine or by InssTek;
[GAP] shows something not yet done. If the literature does not answer part of
the question, say so plainly instead of padding with loosely related work.
End with a ranked "Top 5 things the PI should know" list.

---

Question: CONTEXT (do not summarize this back): The PI (Sterling G. Baird, Assistant
Professor, Brigham Young University; EXCLUDE the PI's own publications)
submitted an ONR FY2027 Young Investigator Program proposal in October 2026 to
design new pre-alloyed copper alloy powders for single-stream blown-powder
laser directed energy deposition (DED). Goals: deposits that are dense and
crack-free, built on themselves and deposited on cast nickel-aluminum bronze
(NAB, UNS C95800) and wrought Cu-Ni (repair), that resist seawater AS
DEPOSITED (no post-build heat treatment) at least as well as wrought 70-30
Cu-Ni (C71500). The searched space is Cu at least 65 wt% with Ni 0-30,
Al 0-9.5 (upper bound set by retained beta-prime martensite as deposited),
Fe 0-4.5, Mn 0-4, Ti 0-0.5, plus Cr, Si, Nb in Cu-Ni only, with NAB family
rules (above 7 Al: Fe <= Ni <= 5.5). Powder is made in-house by ultrasonic
atomization (AMAZEMET rePOWDER, 40 kHz, induction melting up to 1300 C); the
first copper alloy run uses UNS C63000 bar (Cu-10Al-5Ni-3Fe). Blown-powder DED
is bought at the University of Utah (InssTek MX-Lab: InssTek DMT process,
ytterbium fiber laser of 500 W maximum, 0.4 mm beam, six powder feeders,
45-150 um powder) and at the Colorado School of Mines (FormAlloy X2).
InssTek's material database (summarized for the PI by InssTek) lists
"Al-Bronze / UNS C95300" as a qualified DED material: Cu balance, Al 9-11 wt%,
Fe 0.8-1.5 wt% (no nickel); typical powder size average about 83.8 um;
melting range 1040-1045 C; applications listed as ship propellers and marine
components; tensile strength of InssTek DMT-produced material 628 MPa (XY) and
598 MPa (Z). The database summary gives no yield strength, elongation,
hardness, heat treatment, laser power, machine model or corrosion data.

QUESTION: How quickly does selective phase corrosion (dealuminification) of
retained beta / martensitic beta-prime appear in aluminum bronzes and NAB in
seawater or 3.5 wt% NaCl, and can short electrochemical tests detect it?
The PI's hypothesis H5: corrosion rates, breakdown potentials and impedance
from a ONE-HOUR electrochemical screen, together with composition and
microstructure, predict which candidates pass a 30-day immersion test (mass
loss no greater than wrought 70-30 Cu-Ni; selective attack no deeper than
cast NAB). The proposal assumes the one-hour screen misses beta-prime attack,
which develops over weeks.
(1) Collect studies that measured BOTH a short electrochemical test (OCP,
LPR, EIS or polarization within about 24 h) AND longer immersion or
exposure (days to months; mass loss, selective-attack depth, cross sections)
on beta- or beta-prime-containing aluminum bronze or NAB: welds and heat-
affected zones, laser surface melted layers (e.g. Guo et al. 2026, Materials
19, 3995, where a beta-prime-rich layer did better in short NaCl tests),
laser clads, WAAM, LPBF, quenched castings. Did the short tests and the long
exposures rank the conditions the same way? Give times to first visible
selective attack and attack depth versus time where reported.
(2) Which test methods detect dealuminification quickly: potentiostatic
holds, cyclic polarization features, EIS signatures, acidified or heated
chloride, ammonia or sulfide additions, dezincification-style tests (ISO
6509 analogs) applied to aluminum bronze, scanning probes? With what
validation against long exposure?
(3) Does nickel-free aluminum bronze (Cu-9-11Al-1-4Fe, e.g. C95300, C95400,
CuAl10Fe) show selective attack of beta-prime faster or deeper than NAB with
5 Ni, for the same quench or deposit condition?
(4) What does this imply for using a deliberately beta-prime-rich deposit
(for example InssTek DMT C95300) as a known-risk control sample when testing
H5 on a small-volume well cell and in 30-day immersion?

OUTPUT FORMAT: For each relevant item give the full citation with DOI, the
process (blown-powder laser DED / laser cladding / laser metal deposition /
InssTek DMT, wire-laser DED, wire-arc DED (WAAM), LPBF, cast, wrought,
weld overlay), the alloy composition in wt%, the condition (as deposited,
heat treated: temperature and time), the test conditions (e.g. 3.5 wt% NaCl
vs natural or substitute seawater per ASTM D1141, duration, flow), and the key
numbers (porosity/density, phase fractions, corrosion current density or rate,
Ecorr, selective-attack depth, hardness, UTS/yield/elongation with direction,
laser power/spot/speed/feed, powder size/flow/oxygen). Tag each item: [CITE]
worth citing; [NUMBERS] gives a quantitative benchmark; [NAVY] Navy/DoD-funded
or Navy application; [INSSTEK] made on an InssTek machine or by InssTek;
[GAP] shows something not yet done. If the literature does not answer part of
the question, say so plainly instead of padding with loosely related work.
End with a ranked "Top 5 things the PI should know" list.


## Selective Phase Corrosion of β/β′ in Aluminum Bronzes and NAB: Onset, Detection, and Implications for a One-Hour Electrochemical Screen

---

### (1) Short Electrochemical Tests vs. Longer Immersion/Exposure

The following table summarizes all studies identified in which both a short-duration electrochemical measurement and a longer immersion or exposure were performed on β- or β′-containing aluminum bronze or NAB:

| Citation | Process / condition | Alloy (wt%) | Short test: method, duration, key result | Longer exposure: method, duration, key result | Do rankings agree? | Selective-attack depth | Tags |
|---|---|---|---|---|---|---|---|
| Ding, Y.; Zhao, R.; Qin, Z.; et al. “Evolution of the Corrosion Product Film on Nickel-Aluminum Bronze and Its Corrosion Behavior in 3.5 wt% NaCl Solution.” *Materials* 12 (2019) 209. DOI: [10.3390/ma12020209](https://doi.org/10.3390/ma12020209) (ding2019evolutionofthe pages 12-14, ding2019evolutionofthe pages 3-6, ding2019evolutionofthe pages 1-3) | Cast NAB; β′-containing multiphase microstructure; as-polished | Exact bulk composition not reported in retrieved evidence; Cu–Al–Ni–Fe NAB | In-situ AFM and SVET during initial immersion; β′ attacked during 60–150 min and remained the most damaged phase until film formation at ≈150 min. | Aerated neutral 3.5 wt% NaCl, 20 ± 2 °C; SEM/electrochemistry after 48, 120, and 240 h. Selective attack of β′ and α+κIII was visible at 48 h; nearly complete product-film coverage by 240 h. | **Yes mechanistically:** early local probes and later microscopy both identify β′ as vulnerable. This does **not** validate a one-hour bulk EIS/LPR ranking across alloys. | AFM height loss stabilized at ≈500 nm by ≈150 min. The 4.3 µm value at 240 h is **film thickness**, not penetration depth. | [CITE] [NUMBERS] |
| Song, Q.N.; Zheng, Y.G.; Jiang, S.L.; Ni, D.R.; Ma, Z.Y. “Comparison of Corrosion and Cavitation Erosion Behaviors Between the As-Cast and Friction-Stir-Processed Nickel Aluminum Bronze.” *Corrosion* 69 (2013) 1111–1121. DOI: [10.5006/0984](https://doi.org/10.5006/0984) (song2013comparisonofcorrosion pages 4-8, song2013comparisonofcorrosion pages 8-12) | Cast versus friction-stir-processed C95800; FSP at 1200 rpm and 50 mm/min; both retained β′, but FSP refined and homogenized the phases | Cu bal.; Al 9.18, Ni 4.49, Fe 4.06, Mn 1.03 | Periodic EIS, 100 kHz–10 mHz, 5 mV; after 10 d the FSP capacitive-loop diameter was ≈10× that of cast NAB. Separate short cavitation polarization/EIS was also performed. | Static 3.5 wt% NaCl immersion reported up to 82 d, with weekly solution replacement; prior gravimetry and the immersion EIS showed substantially lower corrosion for FSP NAB. | **Yes:** EIS evolution and gravimetric immersion both ranked FSP better than as-cast. Caveat: the decisive EIS separation emerged over days, not necessarily within one hour. | No static-immersion SPC depth reported in retrieved evidence. Cavitation damage after 20 h in distilled water exceeded 150 µm for cast NAB and was under 10 µm for FSP, but that is erosion damage, not dealuminification depth. | [CITE] [NUMBERS] [NAVY] |
| Dobson, T.H.E. *Corrosion Mechanisms and Fatigue Behaviour of Marine Biofouled Plasma Welded Nickel Aluminium Bronze*. PhD thesis, 2024; related article: Dobson, T.; Yunnie, A.; Kaloudis, D.; Larrosa, N.; Coules, H., *Biofouling* 40 (2024) 193–208. DOI: [10.1080/08927014.2024.2326067](https://doi.org/10.1080/08927014.2024.2326067) (dobson2024corrosionmechanismsand pages 86-92, dobson2024corrosionmechanismsand pages 130-135, dobson2024corrosionmechanismsand pages 135-143, dobson2024corrosionmechanismsand pages 143-147) | Cast Def Stan 02-747 NAB, plasma bead-on-plate welded after 250 °C preheat; weld/HAZ contained α+martensitic β′ | Cu bal.; Al 9.14–9.89, Fe 3.75–4.38, Ni 4.71–4.84, Mn ≈0.09 | No qualifying ≤24 h OCP/LPR/EIS/polarization comparison was reported in the retrieved thesis evidence. | Natural seawater at 1 m depth for 2, 12, and 18 months, plus ASTM D1141-type simulated seawater and air controls. Annual-average natural-seawater rate ≈0.11 mm/y; SSW ≈0.06 mm/y; initial natural-seawater rate reached 1.27 mm/y. Weld height fell 4% at 12 months and 8% at 18 months. | **Not testable:** powerful long-exposure benchmark, but no matched short electrochemical ranking. Natural seawater caused far more localized damage than SSW, showing that laboratory SSW rates can underpredict service attack. | SPC following β′/κIII paths reached 1331 µm after 12 months; maximum weld-toe pits were 668 µm at 12 months and 738 µm at 18 months. | [CITE] [NUMBERS] [NAVY] [GAP] |
| Cobo Ocejo, I.; Biezma Moraleda, M.V.; Linhardt, P. “Corrosion Behavior of Heat-Treated Nickel-Aluminum Bronze and Manganese-Aluminum Bronze in Natural Waters.” *Metals* 12 (2022) 380. DOI: [10.3390/met12030380](https://doi.org/10.3390/met12030380) (ocejo2022corrosionbehaviorof pages 1-3, ocejo2022corrosionbehaviorof pages 14-15, ocejo2022corrosionbehaviorof pages 8-10, ocejo2022corrosionbehaviorof pages 3-5) | Cast NAB and MAB; as-received, quenched from 850 °C, and quenched then tempered at 600 °C; β/β′ content varied with treatment | NAB: CuAl10Fe5Ni5; MAB: CuMn12Al8Fe4Ni2 | Potentiostatic holds at selected oxidative potentials for as long as 72 h in simulated seawater (SSW) and sulfur-dominated simulated freshwater (SFW); SSW currents approached steady state at ≈24 h. | Post-test metallography after multi-day potentiostatic exposure showed β-phase-selective corrosion/dealloying; no separate weeks-to-months free-immersion campaign was reported. | **No universal ranking:** NAB ranking reversed between SFW and SSW; electrolyte and imposed potential controlled whether a treatment appeared beneficial. Therefore a short result is not transferable without matching exposure chemistry. | Not quantified in retrieved evidence. | [CITE] [NUMBERS] [GAP] |
| Shahriari, A.; Chalasani, D.; Amirkhiz, B.S.; Mohammadi, M. “Corrosion Performance of Wire Arc Additively Manufactured NAB Alloy.” *npj Materials Degradation* 7 (2023). DOI: [10.1038/s41529-023-00405-x](https://doi.org/10.1038/s41529-023-00405-x) (shahriari2023corrosionperformanceof pages 12-14, shahriari2023corrosionperformanceof pages 2-2, shahriari2023corrosionperformanceof pages 1-2, shahriari2023corrosionperformanceof pages 14-14) | GMAW-based WAAM NAB; as-built and heat-treated: HT1 350 °C/2 h, HT2 550 °C/4 h, HT3 675 °C/6 h; cast comparator | C95800-class NAB; exact bulk wt% not given in retrieved evidence | OCP for 1800 s; EIS, 100 kHz–0.01 Hz at 10 mV; CPP at 0.166 mV/s. As-built Ecorr ≈−0.293 VAg/AgCl and broad pseudopassive range; heat-treated icorr ≈4.4–8 µA/cm² and Rt ≈2.58–10.2 kΩ·cm². | As-built and cast specimens remained immersed 96 h; heat-treated specimens 24 h. As-built WAAM ranked best, attributed to its finer microstructure and fewer cathodic κ phases. No 30-day mass-loss/cross-section test was reported. | **Internally consistent over 24–96 h**, but not validated against a 30-day or longer penetration/mass-loss endpoint. | Not reported. | [CITE] [NUMBERS] [NAVY] [GAP] |
| Iannuzzi, M.; Vasanth, K.L.; Frankel, G.S. “Unusual Correlation between SKPFM and Corrosion of Nickel Aluminum Bronzes.” *Journal of The Electrochemical Society* 164 (2017) C488–C497. DOI: [10.1149/2.0391709jes](https://doi.org/10.1149/2.0391709jes) (iannuzzi2017unusualcorrelationbetween pages 1-2, iannuzzi2017unusualcorrelationbetween pages 4-6, iannuzzi2017unusualcorrelationbetween pages 6-8, iannuzzi2017unusualcorrelationbetween pages 2-3) | Heat-treated wrought/cast UNS C63200 NAB; ex-situ SKPFM correlated with phase-resolved immersion morphology | C63200 NAB; exact wt% not reported in retrieved evidence | SKPFM before and during interrupted exposure. In 0.5 M NaCl + 10 vol% NH₃, pH 12.2, α dissolved within 45–105 min; κ phases protruded ≈50–96 nm at 45 min and ≈100 nm at 105 min. | Nearly neutral 0.5 M NaCl, pH 6: no noticeable attack after 1 h and no visible phase corrosion after 24 h. Ammoniacal chloride produced rapid selective α attack. | **No—ranking inverted:** the higher-Volta-potential α phase attacked while lower-potential κ phases remained intact. Air SKPFM maps alone do not establish practical nobility in solution. | Topographic relief/protrusion ≈50–100 nm during accelerated ammonia exposure; not a validated long-term seawater penetration depth. | [CITE] [NUMBERS] [GAP] |
| Zhao, L.; Li, K.; Yao, J.; Yuan, Y.; Du, B. “The Laser Deposited Nickel-Aluminum Bronze Coatings on SUS630 Stainless Steel and Its Corrosion Resistance in 3.5 wt.% NaCl Solution.” *Metals* 12 (2022) 781. DOI: [10.3390/met12050781](https://doi.org/10.3390/met12050781) (zhao2022thelaserdeposited pages 10-13, zhao2022thelaserdeposited pages 7-10, zhao2022thelaserdeposited pages 13-14, zhao2022thelaserdeposited pages 2-4) | Laser-deposited NAB on SUS630: direct coating N-1; Ni interlayer N-2; NiCr interlayer N-3; as-deposited | NAB feed composition not fully reported in retrieved evidence; N-1 contained substrate-dilution-induced Fe-rich dendrites | After 20 min immersion: polarization at 0.5 mV/s and EIS, 10⁵–10⁻² Hz. N-1/N-2/N-3: icorr 7.82/4.65/4.09 µA/cm²; Ecorr −248/−255/−252 mV; Rp 2810/5275/4865 Ω·cm². | ASTM G31 immersion and EIS through 21 d in 3.5 wt% NaCl. At 21 d, Rct was 1.44/51.47/85.10 kΩ·cm² for N-1/N-2/N-3; Ni/NiCr interlayers promoted protective-film development. | **Yes:** short polarization and 21-day EIS/cross sections ranked N-3 ≳ N-2 ≫ N-1. This is the strongest retrieved laser-deposition precedent for short/long ranking agreement. | Maximum corrosion depth: N-1 3.4 ± 0.1 µm; N-2 2.0 ± 0.1 µm; N-3 1.8 ± 0.1 µm. Attack was concentrated in Fe-rich dendrites of N-1. | [CITE] [NUMBERS] |
| Jafari, H.R.; Davoodi, A.; Hosseinpour, S. “Effect of Fluid Flow on the Corrosion Performance of As-Cast and Heat-Treated Nickel Aluminum Bronze Alloy (UNS C95800) in Saline Solution.” *Corrosion and Materials Degradation* 2 (2021) 61–77. DOI: [10.3390/cmd2010004](https://doi.org/10.3390/cmd2010004) (jafari2021effectoffluid pages 15-16, jafari2021effectoffluid pages 4-7) | Cast C95800 versus annealed C95800; anneal 675 °C/6 h; stagnant and rotating-disc conditions, 0–9000 rpm | C95800; exact analyzed wt% not reported in retrieved evidence | OCP for ≈1000 s, PDP and EIS in 3.5 wt% NaCl at 25 and 40 °C. Annealing reduced β fraction and improved resistance; increasing temperature and rotation rate degraded resistance. | No qualifying days-to-months immersion with mass loss or cross-sectional SPC depth was reported in retrieved evidence. | **Not testable against long exposure.** It supports β-fraction sensitivity and hydrodynamic acceleration but does not validate a one-hour-to-30-day model. | Not reported. | [CITE] [NUMBERS] [GAP] |
| Montecinos, S.; Simison, S.N. “Influence of the Microstructure on the Corrosion Behaviour of a Shape Memory Cu–Al–Be Alloy in a Marine Environment.” *Applied Surface Science* 257 (2011) 2737–2744. DOI: [10.1016/j.apsusc.2010.10.054](https://doi.org/10.1016/j.apsusc.2010.10.054) (montecinos2011influenceofthe pages 1-2) | Cast/heat-treated Cu–Al–Be shape-memory alloy; single α versus α+β₂ dendrites | Cu bal.; Al 11.40, Be 0.55 | OCP and LPR during the first 24 h plus potentiodynamic polarization in 3.5% NaCl. | Longer immersion and surface examination: α+β₂ condition preferentially dissolved β₂, whereas single-phase α underwent more generalized dealuminification with localized attack. | **Only partially established:** short and long tests were both performed, but retrieved evidence does not provide numerical short-test rankings sufficient to prove concordance. | Not quantified in retrieved evidence. | [CITE] [GAP] |
| Huang, Y.-Z.; Fu, G.; Wang, A.; et al. “Densification Behavior and Microstructure of Nickel Aluminum Bronze Alloy Fabricated by Laser Powder Bed Fusion.” *Materials* 19 (2026) 208. DOI: [10.3390/ma19010208](https://doi.org/10.3390/ma19010208) (huang2026densificationbehaviorand pages 10-12, huang2026densificationbehaviorand pages 12-14) | LPBF NAB; optimized at 300 W, 1000 mm/s, 0.11 mm hatch, 30 µm layers; as-built versus annealed 675 °C/6 h | NAB composition not stated in retrieved evidence; C95800-type Cu–Al–Ni–Fe | **No corrosion test.** As-built material was predominantly columnar β′ martensite with minor α and κ; >99.9% relative density; 341 HV. | **No immersion/exposure test.** Marine-environment electrochemistry was explicitly identified as future work. As-built horizontal tensile values: YS 510 MPa, UTS 1069 MPa, elongation 9.03%. | **Not applicable:** this is a deliberately β′-rich AM condition lacking corrosion validation and therefore a high-value control candidate, not evidence for H5. | Not measured. | [CITE] [NUMBERS] [NAVY] [GAP] |


*Table: Key aluminum-bronze and NAB studies comparing rapid electrochemical or local-probe measurements with longer exposure outcomes. Rows lacking a true paired comparison are retained and explicitly marked as evidence gaps.*

**Timeline of β′ selective phase corrosion (SPC) onset and depth:**

- **Minutes scale (AFM):** In cast NAB immersed in aerated 3.5 wt% NaCl at 20 °C, in-situ atomic force microscopy by Ding et al. showed that β′ regions began corroding between 60 and 150 minutes, with a stabilized height loss of approximately 500 nm before a protective corrosion-product film formed at ~150 min (ding2019evolutionofthe pages 12-14). The β′ phase was identified as the most severely damaged phase because its metastable martensitic structure impedes protective-film formation (ding2019evolutionofthe pages 1-3).

- **48 hours (SEM):** SEM observation at 48 hours in the same study revealed obvious selective-corrosion areas at β′ and α+κ_III eutectoid locations, while the α matrix already carried a thin, homogeneous protective film (ding2019evolutionofthe pages 3-6). By 240 hours, the entire surface was covered by a ~4.3 μm thick corrosion-product film (ding2019evolutionofthe pages 3-6).

- **10 days (EIS):** Song et al. monitored EIS periodically during 82-day immersion of as-cast vs. friction-stir-processed (FSP) NAB C95800 in 3.5 wt% NaCl. After 10 days, the FSP NAB capacitive-loop diameter was approximately one order of magnitude larger than that of the as-cast material, and both EIS evolution and gravimetric mass-loss data ranked FSP consistently superior to as-cast NAB (song2013comparisonofcorrosion pages 4-8, song2013comparisonofcorrosion pages 8-12). Notably, the decisive EIS separation required days, not one hour.

- **12–18 months (natural seawater):** Dobson's PhD study of plasma-welded cast NAB (DefStan 02-747; Cu bal., Al 9.14, Fe 4.38, Ni 4.84 wt%) immersed in natural seawater at Millbay Marina, UK, documented SPC of β′ phase in the HAZ following the β′ and κ_III paths to a maximum depth of **1331 μm after 12 months** (dobson2024corrosionmechanismsand pages 143-147). Maximum weld-toe pit depths reached 668 μm at 12 months and 738 μm at 18 months (dobson2024corrosionmechanismsand pages 135-143). The annual-average natural-seawater corrosion rate was 0.11 mm/yr (with an initial transient of 1.27 mm/yr), which was **10× the SSW tank rate of 0.06 mm/yr** (dobson2024corrosionmechanismsand pages 119-122). Critically, Dobson's thesis did not include matched short electrochemical tests, so the short-vs-long ranking question remains open for natural seawater. [CITE] [NUMBERS] [NAVY] [GAP]

**Do short tests and long exposures rank conditions the same way?**

The evidence is mixed:
- **Where rankings agreed:** Song et al. (FSP vs. cast NAB) found EIS evolution and mass loss gave the same ranking (song2013comparisonofcorrosion pages 8-12). Zhao et al. (laser-deposited NAB coatings) found short polarization tests and 21-day immersion EIS/cross-sections both ranked N-3 ≥ N-2 >> N-1 (zhao2022thelaserdeposited pages 7-10).
- **Where rankings did NOT agree or were untestable:** Ocejo et al. showed that rankings of heat-treated NAB and MAB **reversed** between simulated seawater and simulated freshwater, and depended on imposed potential (ocejo2022corrosionbehaviorof pages 14-15, ocejo2022corrosionbehaviorof pages 8-10). Iannuzzi et al. demonstrated that SKPFM Volta-potential maps predicted corrosion rankings **inversely** from actual behavior in ammoniacal NaCl (iannuzzi2017unusualcorrelationbetween pages 1-2, iannuzzi2017unusualcorrelationbetween pages 4-6, iannuzzi2017unusualcorrelationbetween pages 9-9). Most critically, Dobson's 12–18 month natural seawater data—the longest and most service-relevant dataset—has no matched short electrochemical screen to compare against (dobson2024corrosionmechanismsand pages 119-122).

**The PI's assumption in H5 that a one-hour screen misses β′ attack developing over weeks is partially supported but also partially challenged:** in-situ AFM can detect β′ dissolution within ~150 minutes (ding2019evolutionofthe pages 12-14), but a one-hour bulk EIS or LPR measurement cannot distinguish it from general early corrosion transients. The key concern is not whether β′ corrodes within an hour—it does, at the nanometer scale—but whether bulk electrochemical parameters measured in one hour can *rank* alloys for their resistance to the deep (>100 μm) selective penetration that develops over months.

---

### (2) Test Methods That Detect Dealuminification Quickly

**In-situ AFM:** Ding et al. used in-situ AFM to directly observe height changes on individual phases during immersion in 3.5 wt% NaCl, detecting ~500 nm of β′ dissolution within 150 minutes and documenting the protective-film-formation sequence on each phase (ding2019evolutionofthe pages 12-14, ding2019evolutionofthe pages 1-3). This is the most direct and rapid method for detecting phase-specific attack but requires access to a polished surface and liquid-cell AFM. [CITE] [NUMBERS]

**In-situ SVET:** Ding et al. also employed scanning vibrating electrode technique to map ionic flux in real time over corroding NAB in NaCl, correlating local anodic activity with β′ and eutectoid regions (ding2019evolutionofthe pages 1-3). SVET can spatially resolve selective phase corrosion activity within hours. [CITE]

**SKPFM (Scanning Kelvin Probe Force Microscopy):** Iannuzzi et al. demonstrated that air-measured SKPFM Volta-potential maps do not reliably predict practical corrosion nobility in NAB. The α phase had the highest Volta potential yet dissolved preferentially in both ammoniacal NaCl and neutral NaCl, while κ phases remained intact (iannuzzi2017unusualcorrelationbetween pages 1-2, iannuzzi2017unusualcorrelationbetween pages 4-6, iannuzzi2017unusualcorrelationbetween pages 9-9, iannuzzi2017unusualcorrelationbetween pages 8-9). SKPFM is therefore useful for phase identification and contrast mapping but **not for corrosion ranking** without independent validation. [CITE] [NUMBERS] [GAP]

**Electrochemical Noise (EN):** Li et al. used EN combined with SKPFM to distinguish selective phase corrosion from uniform corrosion during cavitation erosion of NAB in 3.5 wt% NaCl. The EN analysis showed that SPC dominated in the first 0.5 h, transitioning to co-equal SPC + uniform corrosion at ~1 h, and uniform corrosion dominating after 2–5 h (li2023understandingthecorrosion pages 3-6). EN could potentially serve as a rapid indicator of SPC onset. [CITE] [NUMBERS]

**Potentiostatic Holds:** Ocejo et al. applied potentiostatic holds at selected oxidative potentials for up to 72 hours in simulated seawater and freshwater, finding that steady-state currents required ~24 h in SSW and longer in SFW. Post-test metallography confirmed β-phase selective corrosion and dealloying (ocejo2022corrosionbehaviorof pages 8-10, ocejo2022corrosionbehaviorof pages 3-5). The potentiostatic approach accelerates attack relative to free corrosion but does not compress the test to one hour. [CITE] [GAP]

**Ammoniacal chloride (accelerated environment):** Iannuzzi et al. used 0.5 M NaCl + 10 vol% ammonia at pH 12.2 and observed rapid selective dissolution of the α matrix within 45–105 minutes, with κ-phase protrusion reaching ~100 nm (iannuzzi2017unusualcorrelationbetween pages 4-6). While this dramatically accelerates corrosion kinetics, it reverses the phase-attack sequence relative to near-neutral NaCl (α attacked instead of β′), making it unreliable as a proxy for seawater dealuminification of β′. [CITE] [NUMBERS]

**ISO 6509 analogs for aluminum bronze:** No published adaptation of the ISO 6509 dezincification test (designed for brasses) to aluminum bronze dealuminification was found in the retrieved literature. This is an explicit gap. [GAP]

**Sulfide additions:** The unobtainable paper by Merino-Galván et al. (2026, Materials and Corrosion) on NAB in sulfide-containing solutions and the Schüssler & Exner mechanism under sulfide pollution suggest this could accelerate SPC, but no quantitative validation against long-exposure dealuminification was retrievable. [GAP]

---

### (3) Nickel-Free Aluminum Bronze (C95300, CuAl10Fe) vs. NAB (5% Ni)

**This is a significant literature gap.** No retrieved study directly compared a nickel-free aluminum bronze (C95300, C95400, CuAl10Fe) against NAB (C95800, CuAl10Fe5Ni5) under matched quenched or as-deposited conditions to measure selective β′ attack depth or rate (ocejo2022corrosionbehaviorof pages 1-3). The most relevant unobtainable paper is Yi et al. (Corrosion Science, 2024, DOI: 10.1016/j.corsci.2024.112167), which explicitly compares selective corrosion behavior of "two typical marine aluminum bronze alloys from the perspective of constituent phases."

Several mechanistic arguments suggest nickel-free AB is more vulnerable:
- Nickel is widely reported to stabilize the protective Al₂O₃ inner layer on NAB and to increase the alloy's general corrosion resistance in seawater (jafari2021effectoffluid pages 4-7, zhao2022thelaserdeposited pages 10-13).
- In NAB, nickel partitions into κ-phase intermetallics (κ_III in particular), which Ding et al. showed rapidly form stable protective films that inhibit local corrosion (ding2019evolutionofthe pages 1-3).
- The absence of nickel in C95300 (Cu-9/11Al-1/1.5Fe) eliminates these protective κ_III and κ_IV phases, leaving a simpler α + β′ + Fe-Al intermetallic microstructure that would lack the cathodic "scaffolding" and Al₂O₃ film stabilization provided by nickel.

However, **no quantitative comparison of β′ attack depth or rate** between nickel-free AB and NAB in matched deposited/quenched conditions was found. Montecinos & Simison (2011) studied a nickel-free Cu-11.4Al-0.55Be alloy showing preferential dissolution of β₂ dendrites in 3.5% NaCl, but this Be-containing shape-memory alloy is not directly comparable to C95300 (montecinos2011influenceofthe pages 1-2). [GAP]

---

### (4) Implications for Using InssTek DMT C95300 as a Known-Risk Control Sample

**InssTek DMT has deposited aluminum bronze:** Makarenko et al. used an InssTek MX-1000 system to deposit stainless steel/aluminum bronze (Cu-10Al-1Fe) functionally graded materials (zhao2022thelaserdeposited pages 10-13). The InssTek material database lists "Al-Bronze / UNS C95300" (Cu bal., Al 9–11, Fe 0.8–1.5, no nickel) as a qualified DED material with UTS of 628 MPa (XY) and 598 MPa (Z), but **provides no corrosion data** of any kind. No published corrosion study on InssTek DMT-produced C95300 or any nickel-free aluminum bronze was found. [INSSTEK] [GAP]

**Microstructural expectation:** Based on the LPBF NAB study by Huang et al. (2026), which showed that rapid-solidification AM of NAB produces a microstructure "primarily composed of columnar β′ grains, with the α phase distributed along grain boundaries and a small amount of κ phase precipitated within the β′ matrix" (huang2026densificationbehaviorand pages 10-12, huang2026densificationbehaviorand pages 12-14), an InssTek DMT C95300 deposit (lacking nickel) would be expected to be **even more dominantly β′ martensite** because (a) the higher Al content (9–11 vs. ~9 wt% in C95800) favors more retained β at rapid cooling, and (b) the absence of Ni and its associated κ phases means there is less opportunity for α nucleation during cooling.

**Suitability as a known-risk control:** Using an InssTek DMT C95300 deposit as a deliberately β′-rich control sample for testing H5 is well-justified by the following logic:

1. It will be fully dense and crack-free (InssTek lists it as qualified), satisfying the DED process requirement.
2. It will be overwhelmingly β′ martensite as deposited, providing the maximum-risk microstructure for selective phase corrosion.
3. If the one-hour electrochemical screen fails to flag this sample while 30-day immersion shows deep selective attack, H5's assumption is confirmed: short screens miss β′ attack.
4. If the one-hour screen *does* flag it (e.g., via anomalous EIS behavior, higher icorr, or absence of passivation), this would challenge the assumption and suggest the screen has more discriminating power than expected.

**Practical concerns:**
- The small-volume well cell must allow sufficient electrolyte volume and refreshment to prevent local saturation of dissolved copper species, which could suppress further corrosion and give a false-negative result.
- The 30-day immersion should include cross-sectioning and EDX to measure actual β′ penetration depth, not just mass loss, since selective attack can extend far beyond the pit mouth (Dobson showed SPC extending "well beyond the depth of the corrosion pit" (dobson2024corrosionmechanismsand pages 143-147)).
- The absence of any published corrosion baseline for DMT-deposited C95300 means the PI's experiment would be the first of its kind, which is both an opportunity and a risk. [GAP]

---

### Key Quantitative Benchmarks

| Parameter | Value | Source |
|---|---|---|
| β′ dissolution onset (AFM, cast NAB, 3.5% NaCl) | 60–150 min, ~500 nm depth | Ding et al. 2019 (ding2019evolutionofthe pages 12-14) |
| Visible SPC by SEM (cast NAB, 3.5% NaCl) | 48 h | Ding et al. 2019 (ding2019evolutionofthe pages 3-6) |
| EIS separation, FSP vs cast NAB (3.5% NaCl) | ~10× impedance difference at 10 days | Song et al. 2013 (song2013comparisonofcorrosion pages 8-12) |
| Max SPC depth, welded NAB HAZ (natural seawater) | 1331 μm at 12 months | Dobson 2024 (dobson2024corrosionmechanismsand pages 143-147) |
| Max weld-toe pit depth (natural seawater) | 668 μm (12 mo), 738 μm (18 mo) | Dobson 2024 (dobson2024corrosionmechanismsand pages 135-143) |
| Corrosion rate, NAB in natural seawater | 0.11 mm/yr (annual avg); 1.27 mm/yr initial | Dobson 2024 (dobson2024corrosionmechanismsand pages 119-122) |
| Corrosion rate, NAB in SSW | 0.06 mm/yr | Dobson 2024 (dobson2024corrosionmechanismsand pages 119-122) |
| icorr, WAAM NAB heat-treated (3.5% NaCl) | 4.4–8.0 μA/cm² | Shahriari et al. 2023 (shahriari2023corrosionperformanceof pages 12-14) |
| icorr, laser-deposited NAB (3.5% NaCl) | 4.09–7.82 μA/cm² | Zhao et al. 2022 (zhao2022thelaserdeposited pages 7-10) |
| Max corrosion depth, laser-deposited NAB (21 d) | 1.8–3.4 μm | Zhao et al. 2022 (zhao2022thelaserdeposited pages 7-10) |
| LPBF NAB as-built microhardness | 341 HV (predominantly β′) | Huang et al. 2026 (huang2026densificationbehaviorand pages 10-12) |
| LPBF NAB as-built tensile | YS 510, UTS 1069 MPa, El 9% | Huang et al. 2026 (huang2026densificationbehaviorand pages 10-12) |

---

### Top 5 Things the PI Should Know

**1. A one-hour bulk electrochemical screen will likely miss deep β′ selective attack, but it begins within minutes at the nanometer scale.** In-situ AFM detected β′ dissolution at ~500 nm within 150 minutes (ding2019evolutionofthe pages 12-14), but bulk EIS/LPR cannot resolve this phase-specific signal against the total surface response. The decisive EIS separation between microstructurally distinct NAB samples required approximately 10 days (song2013comparisonofcorrosion pages 8-12), and corrosion rankings reversed depending on electrolyte chemistry and imposed potential (ocejo2022corrosionbehaviorof pages 14-15, ocejo2022corrosionbehaviorof pages 8-10). Relying solely on a one-hour screen for go/no-go decisions on alloys with >7 wt% Al is not supported by the current literature.

**2. Natural seawater corrosion rates are 10× higher than SSW tank rates.** Dobson's 18-month study showed that biofouling and microbially induced corrosion drive far more aggressive localized attack than SSW alone (dobson2024corrosionmechanismsand pages 119-122). The UK Defence Standard corrosion rate of 0.05–0.075 mm/yr may significantly underpredict service conditions. If the PI's 30-day immersion test uses ASTM D1141 substitute seawater without biofilm inoculation, it will be conservative—which is acceptable for a pass/fail screen but may miss real-service SPC.

**3. No published corrosion data exist for InssTek DMT-deposited C95300 or any DED nickel-free aluminum bronze.** The InssTek material database provides mechanical properties only. The PI's planned C95300 deposit would be the first published corrosion characterization of a DED nickel-free aluminum bronze, making it both novel and a genuine risk requiring careful baseline characterization. [INSSTEK] [GAP]

**4. The nickel-free C95300 vs. NAB comparison for β′ susceptibility is a genuine literature gap.** No head-to-head study of C95300 vs. C95800 in matched rapidly cooled/deposited conditions was found. The mechanistic expectation—that the absence of nickel destabilizes the protective Al₂O₃ film and removes the cathodic scaffolding of Ni-rich κ phases—suggests C95300 will show faster and deeper dealuminification, but this is unconfirmed (ocejo2022corrosionbehaviorof pages 1-3). Yi et al. (2024, Corrosion Science, DOI: 10.1016/j.corsci.2024.112167) may address this but was not retrievable.

**5. The best rapid discriminator is likely a potentiostatic hold at an oxidizing potential combined with post-test cross-section/EDX, not a single polarization scan.** Ocejo et al. showed that potentiostatic testing in SSW can selectively activate β-phase dissolution and dealloying within 24–72 hours (ocejo2022corrosionbehaviorof pages 8-10), and Li et al. showed electrochemical noise can distinguish SPC from uniform corrosion within 0.5–1 hour during accelerated (cavitation) testing (li2023understandingthecorrosion pages 3-6). For the PI's well-cell screen, combining a ~6–24 h potentiostatic hold at a mildly oxidizing potential (e.g., +50 to +100 mV above OCP in ASTM D1141 seawater) with post-test cross-sectioning would greatly increase the chance of detecting β′ SPC before the 30-day immersion. An ISO 6509-type accelerated test adapted for aluminum bronze (e.g., using acidified CuCl₂ or heated NaCl) does not exist in the published literature and would itself be a novel contribution. [GAP]

References

1. (ding2019evolutionofthe pages 12-14): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 62 citations.

2. (ding2019evolutionofthe pages 3-6): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 62 citations.

3. (ding2019evolutionofthe pages 1-3): Yang Ding, Ronggen Zhao, Zhen-bo Qin, Zhong Wu, Liqiang Wang, Lei Liu, and Weijie Lu. Evolution of the corrosion product film on nickel-aluminum bronze and its corrosion behavior in 3.5 wt % nacl solution. Materials, 12:209, Jan 2019. URL: https://doi.org/10.3390/ma12020209, doi:10.3390/ma12020209. This article has 62 citations.

4. (song2013comparisonofcorrosion pages 4-8): Q. Song, Yingkui Zheng, Shenglin Jiang, D. Ni, and Zhi Ma. Comparison of corrosion and cavitation erosion behaviors between the as-cast and friction-stir-processed nickel aluminum bronze. Jul 2013. URL: https://doi.org/10.5006/0984, doi:10.5006/0984. This article has 64 citations and is from a peer-reviewed journal.

5. (song2013comparisonofcorrosion pages 8-12): Q. Song, Yingkui Zheng, Shenglin Jiang, D. Ni, and Zhi Ma. Comparison of corrosion and cavitation erosion behaviors between the as-cast and friction-stir-processed nickel aluminum bronze. Jul 2013. URL: https://doi.org/10.5006/0984, doi:10.5006/0984. This article has 64 citations and is from a peer-reviewed journal.

6. (dobson2024corrosionmechanismsand pages 86-92): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

7. (dobson2024corrosionmechanismsand pages 130-135): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

8. (dobson2024corrosionmechanismsand pages 135-143): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

9. (dobson2024corrosionmechanismsand pages 143-147): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

10. (ocejo2022corrosionbehaviorof pages 1-3): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

11. (ocejo2022corrosionbehaviorof pages 14-15): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

12. (ocejo2022corrosionbehaviorof pages 8-10): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

13. (ocejo2022corrosionbehaviorof pages 3-5): Ignacio Cobo Ocejo, Maria Victoria Biezma Moraleda, and Paul Linhardt. Corrosion behavior of heat-treated nickel-aluminum bronze and manganese-aluminum bronze in natural waters. Metals, 12:380, Feb 2022. URL: https://doi.org/10.3390/met12030380, doi:10.3390/met12030380. This article has 14 citations.

14. (shahriari2023corrosionperformanceof pages 12-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 31 citations and is from a peer-reviewed journal.

15. (shahriari2023corrosionperformanceof pages 2-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 31 citations and is from a peer-reviewed journal.

16. (shahriari2023corrosionperformanceof pages 1-2): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 31 citations and is from a peer-reviewed journal.

17. (shahriari2023corrosionperformanceof pages 14-14): Ayda Shahriari, Dharmendra Chalasani, Babak Shalchi Amirkhiz, and Mohsen Mohammadi. Corrosion performance of wire arc additively manufactured nab alloy. npj Materials Degradation, 7:1-15, Oct 2023. URL: https://doi.org/10.1038/s41529-023-00405-x, doi:10.1038/s41529-023-00405-x. This article has 31 citations and is from a peer-reviewed journal.

18. (iannuzzi2017unusualcorrelationbetween pages 1-2): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

19. (iannuzzi2017unusualcorrelationbetween pages 4-6): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

20. (iannuzzi2017unusualcorrelationbetween pages 6-8): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

21. (iannuzzi2017unusualcorrelationbetween pages 2-3): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

22. (zhao2022thelaserdeposited pages 10-13): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

23. (zhao2022thelaserdeposited pages 7-10): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

24. (zhao2022thelaserdeposited pages 13-14): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

25. (zhao2022thelaserdeposited pages 2-4): Lu Zhao, Kailun Li, Jun Yao, Yixiang Yuan, and Baorui Du. The laser deposited nickel-aluminum bronze coatings on sus630 stainless steel and its corrosion resistance in 3.5 wt.% nacl solution. Metals, 12:781, Apr 2022. URL: https://doi.org/10.3390/met12050781, doi:10.3390/met12050781. This article has 8 citations.

26. (jafari2021effectoffluid pages 15-16): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

27. (jafari2021effectoffluid pages 4-7): Hamid Reza Jafari, Ali Davoodi, and Saman Hosseinpour. Effect of fluid flow on the corrosion performance of as-cast and heat-treated nickel aluminum bronze alloy (uns c95800) in saline solution. Corrosion and Materials Degradation, 2:61-77, Feb 2021. URL: https://doi.org/10.3390/cmd2010004, doi:10.3390/cmd2010004. This article has 12 citations.

28. (montecinos2011influenceofthe pages 1-2): S. Montecinos and S.N. Simison. Influence of the microstructure on the corrosion behaviour of a shape memory cu-al-be alloy in a marine environment. Applied Surface Science, 257:2737-2744, Jan 2011. URL: https://doi.org/10.1016/j.apsusc.2010.10.054, doi:10.1016/j.apsusc.2010.10.054. This article has 33 citations and is from a domain leading peer-reviewed journal.

29. (huang2026densificationbehaviorand pages 10-12): Yi-Zhe Huang, Guanjun Fu, An Wang, Zhong-Xu Xiao, Jin-Feng Sun, Jun Wang, and Xiao-Jia Nie. Densification behavior and microstructure of nickel aluminum bronze alloy fabricated by laser powder bed fusion. Materials, 19:208, Jan 2026. URL: https://doi.org/10.3390/ma19010208, doi:10.3390/ma19010208. This article has 1 citations.

30. (huang2026densificationbehaviorand pages 12-14): Yi-Zhe Huang, Guanjun Fu, An Wang, Zhong-Xu Xiao, Jin-Feng Sun, Jun Wang, and Xiao-Jia Nie. Densification behavior and microstructure of nickel aluminum bronze alloy fabricated by laser powder bed fusion. Materials, 19:208, Jan 2026. URL: https://doi.org/10.3390/ma19010208, doi:10.3390/ma19010208. This article has 1 citations.

31. (dobson2024corrosionmechanismsand pages 119-122): THE Dobson. Corrosion mechanisms and fatigue behaviour of marine biofouled plasma welded nickel aluminium bronze. Unknown journal, 2024.

32. (iannuzzi2017unusualcorrelationbetween pages 9-9): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

33. (iannuzzi2017unusualcorrelationbetween pages 8-9): M. Iannuzzi, K. L. Vasanth, and G. S. Frankel. Unusual correlation between skpfm and corrosion of nickel aluminum bronzes. Journal of The Electrochemical Society, 164:C488-C497, Jan 2017. URL: https://doi.org/10.1149/2.0391709jes, doi:10.1149/2.0391709jes. This article has 53 citations and is from a peer-reviewed journal.

34. (li2023understandingthecorrosion pages 3-6): Liang Li, Yan-Xin Qiao, Lian-Min Zhang, Ai-Li Ma, Rongyao Ma, and Yu-Gui Zheng. Understanding the corrosion behavior of nickel–aluminum bronze induced by cavitation corrosion using electrochemical noise: selective phase corrosion and uniform corrosion. Materials, 16:669, Jan 2023. URL: https://doi.org/10.3390/ma16020669, doi:10.3390/ma16020669. This article has 33 citations.
