# Checks of the 50 per-element answers (2026-10-17)

Five Claude subagents each read the full Edison answers for a group of
elements and wrote the digests below. Each entry has the VERDICT line, the
key facts with sources, the interactions, a Crossref check of up to three
DOIs, red flags, and a recommendation. Statements marked "my judgment" or
"my recollection" are the checker's, not a checked source. The decisions in
`decisions.py` and `search_space.py` weigh these recommendations; README.md
lists where they changed Edison's verdicts. Lines saying "Repo now: ..."
compare against an intermediate draft of `search_space.md`.

Groups: 1 (Hf, Pb, Se, Te, W, Ta, Ge, Ca, Sc, Pr, Nd, Er, Gd); 2 (Ni, Al, Fe,
Cr, Sn, Zn, Si, Nb, Be, Co); 3a (Cu, Ti, Zr, Mg, Ag, V, B, Sb); 3b (C, Mo,
Ga, In, Cd, Y, Ce, Pd); 4 (Mn, As, P, Bi, S, O, H, N, Li, Sr, La).


---

# Group 1

## Edison phase-1 digests, group 1 (Hf, Pb, Se, Te, W, Ta, Ge, Ca, Sc, Pr, Nd, Er, Gd)

Notes on method. All DOIs below were checked with the Crossref API, falling back to doi.org when Crossref had no record. "TCCU7" statements come from the repo file `edison-trajectories/cu-ded-elements-2026-10/tccu7_coverage.md`. Anything marked "my judgment" or "my understanding" is my own metallurgical knowledge, not something Edison or a checked source says. All compositions are in wt%.

## Hf

**VERDICT** `VERDICT | Hf | decision=EXCLUDE | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- Hf dissolves in α-Cu up to 0.87 at about 965 °C, falling below 0.04 at 500 °C. The eutectic (Cu + Cu5Hf) is at 19.1 Hf and 988 °C, so Hf lowers the liquidus (Perry 1974, *Mater. Sci. Eng.* 13:57-62, 10.1016/0025-5416(74)90021-4).
- Strengthening needs quench, high-pressure torsion and aging. Cu-0.9Hf formed about 20 nm Cu5Hf and reached 2,400 MPa and 71% IACS after 450 °C for 1 h (Shangina 2014, *J. Mater. Sci.* 49:6674-6681, 10.1007/s10853-014-8339-4). Nothing was shown as deposited.
- The only chloride data are for Cu-Hf-Ti-Nb glass, where Nb was varied. Hf forms HfO2 at alumina interfaces (Loehman 2003, *JECS* 23:2805, 10.1016/S0955-2219(03)00292-9).
- Price is about US$4,657/kg, roughly US$42 per kg of alloy at 0.9 Hf.

**Interactions:** Cr and Hf co-precipitate in Cu-0.7Cr-0.9Hf, Zr shares Cu5(Hf,Zr), and oxygen consumes Hf. No numerical rules were found.

**DOI check:** Perry 1974 OK. Shangina 2014 OK. Turchanin & Agraval 2008, Cu-Hf assessment (*Powder Metall. Met. Ceram.* 47:223-233, 10.1007/s11106-008-9008-4), OK.

**Red flags**
- The VERDICT line gives `family=both` with EXCLUDE, while other EXCLUDE files use `none`.
- Maximum solubility is quoted at 965 °C, which is below the 988 °C eutectic. It is probably the highest temperature measured (minor).
- Hf is **not in TCCU7**.
- My understanding is that 0.5 mg/m³ is the OSHA PEL, which Edison hedged on.

**Recommendation:** Keep EXCLUDE, with `family=none`. Hf is not in TCCU7, works only after aging, is costly, and reacts with alumina.

## Pb

**VERDICT** `VERDICT | Pb | decision=LIMIT | family=both | conservative_max_wt=0.01 | nonconservative_max_wt=0.05 | floor_wt=NA | impurity_max_wt=0.01 | evidence=moderate`

**Key facts**
- C70600, C71000 and C71500 are weldable at Pb ≤0.05 (Beaver 1978, OSTI OTEC joinability survey, 10.2172/6523751).
- Pb in Cu-Ni should be below 0.01 for welding, and Pb or S cracks Cu-Ni during brazing (Van Konynenburg 1990, LLNL/OSTI, 10.2172/137782).
- Cu-Pb has no intermetallics, a 955 °C monotectic, a miscibility gap closing at about 1,000 °C, and terminal liquid down to 327 °C (Chikova 2016, *Izv. Vuz. Tsvetn. Metall.* 76-82, 10.17073/0021-3438-2016-4-76-82).
- There are no seawater data. The OSHA PEL is 50 µg/m³.

**Interactions:** Pb and S each cause damage, and one cannot offset the other in a sum. P does not neutralize Pb. Cu-Ni-Pb is assessed (Wang 2000, *Calphad* 24:149-167, and in TCCU7); Cu-Al-Pb is not. Pb diluted in from a C95800 substrate (up to 0.03) can push the fusion zone above the powder limit.

**DOI check:** Beaver DOI OK (an OSTI report, which Edison lists as "ArXiv"). Van Konynenburg OK. Chikova OK. Wang 2000 exists as 10.1016/S0364-5916(00)00020-1.

**Red flags**
- The claim that Pb "separates as droplets at 1,200-1,300 °C" contradicts the answer's own ~1,000 °C critical temperature: above it, liquid Cu-Pb is fully miscible.
- A solubility of 1.3 wt% at 950 °C looks too high to me (my judgment).
- Section 6 and the table disagree on whether Pb is on the 2025 list, and Section 6 calls Ni "unconfirmed". My understanding is that Pb was added in 2025 and Ni is on both lists.
- Because the LIMIT verdict fills the conservative fields, verdicts.md tabulates a designed range of 0.01-0.05.
- Primary specification limits are missing (my knowledge, to be verified): AWS A5.7 fillers and ASTM B111 welding grade allow Pb ≤0.02; C95800 allows ≤0.03.

**Recommendation:** Keep LIMIT at 0.01 and set the conservative and non-conservative fields to NA. Use 0.02 as the outer limit instead of 0.05.

## Se

**VERDICT** `VERDICT | Se | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.006 | evidence=thin`

**Key facts**
- For Cu-Ni hot workability, Se must be controlled "as low as 0.006", with Te at 0.003 and Bi at 0.001 (Riley & Makar 1986, *Conservation & Recycling* 9:315-323, 10.1016/0361-3658(86)90066-4). This is the only quantitative anchor, and it concerns hot working, not DED.
- Se is an insoluble free-machining phase found only in plumbing Bi-Se alloys: C89510 has 0.35-0.75, C89520 0.8-1.1, C89550 0.01-0.1, and C49300 ≤0.2. Se evaporates during melting (Zhou 2017, *Jixie Gongcheng Cailiao* 41, 10.11973/jxgccl201708002; a secondary source for ASTM B30).
- There are no seawater, DED or weld data. The OSHA PEL is 0.2 mg/m³.

**Interactions:** Keep Se separate from Bi, Te, Pb and S, since no sum rule is supported. Ni and Al do not neutralize it.

**DOI check:** Riley & Makar OK. Zhou 2017 resolves through doi.org (not Crossref) to the matching title, journal and year: OK. The CDA "High Conductivity Coppers" DOI 10.1108/acmm.1999.12846cab.036 is a **DOI MISMATCH**: it is a 1999 news item in *Anti-Corrosion Methods and Materials* 46.

**Red flags**
- The limit comes from a single 1986 secondary source.
- TCCU7 does include Se, which Edison could not confirm, but only the Cu-Se binary.
- My understanding is that Se is on neither critical-mineral list.
- My judgment: in Ni-bearing deposits, low-melting Ni-Se phases (like Ni-S) are the likely mechanism, so the Cu-Ni value is the right one to borrow.

**Recommendation:** Keep LIMIT at 0.006 (60 ppm). Oxygen-free Cu feed holds only a few ppm Se, so this is a line on the feedstock certificate, not a design variable.

## Te

**VERDICT** `VERDICT | Te | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.003 | evidence=thin`

**Key facts**
- For Cu-Ni hot workability, Te must be controlled as low as 0.003 (30 ppm), and Te is listed among impurities that cause HAZ cracking in copper alloys (Riley & Makar 1986, 10.1016/0361-3658(86)90066-4).
- Solubility follows log x = −7372/T + 2.43, about 0.0002 wt% at 600 °C, with Cu2Te forming. No Cu-Te CALPHAD assessment exists (Magnusson 2017, SKB R-17-20, no DOI). I checked the arithmetic.
- About 50% of the Te volatilized at 1,300 °C under reducing Cu-slag conditions (Klemettinen 2020, *SN Appl. Sci.* 2:337, 10.1007/s42452-020-2137-1). Elemental Te boils at about 990 °C.
- C10100 allows Te ≤0.0002. Price was US$349/kg in 2011 and about US$70/kg in 2017 (Chung 2024, *Can. Metall. Q.* 63:1626-1642, 10.1080/00084433.2024.2355031).

**Interactions:** Te belongs with S and Se as a chalcogenide embrittler, so assess their combined burden; no sum rule is supported. P does not neutralize Te.

**DOI check:** Riley & Makar OK. Klemettinen 2020 OK. Chung 2024 OK.

**Red flags**
- The limit has a single source, and Edison tags it [SPEC] although it is not a specification.
- Te is **not in TCCU7**.
- Edison left the exposure limit unverified; my understanding is that the OSHA PEL is 0.1 mg/m³.
- The critical-mineral history (removal recommended in the 2025 draft, kept on the final list) matches my understanding.

**Recommendation:** Keep LIMIT at 0.003 (30 ppm) in powder and deposit. Oxygen-free Cu feed makes this trivial to meet.

## W

**VERDICT** `VERDICT | W | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- W melts at about 3,422 °C and Cu-W is effectively immiscible, so W cannot be dissolved into a Cu melt at 1,300 °C or below for pre-alloyed powder.
- The only Cu-rich laser data come from W particles bonded onto Cu powder (6.26 W, 3 vol%). Absorptivity at 1,070 nm rose from 25.6% to 71.6%. In LPBF, density was 99.78% by optical sections but only 96.46% by Archimedes, with W agglomerates and pores at the Cu/W interfaces (Rauh 2026, *Prog. Addit. Manuf.* 11:8789-8806, 10.1007/s40964-026-01825-2).
- The chloride data cannot be transferred:
  - 95W-5Cu P/M corroded at 0.40 mm/y and 95W-4Cu-1Ni at 0.02 mm/y (Kumkumoğlu 2016 thesis, no DOI).
  - A laser-clad Ni60-WC coating corroded at 0.0158 mm/y versus 0.0183 mm/y for the Cu substrate (Liu 2022, *Coatings* 12:1537, 10.3390/coatings12101537).
- Contained W costs about US$37.8/kg (USGS OFR 2025-1032).

**Interactions:** None can be quantified.

**DOI check:** Rauh 2026 OK. Liu 2022 OK. Kustron 2023, the ultrasonic-atomizer paper (*Appl. Sci.* 13:8984, 10.3390/app13158984), OK.

**Red flags:** Nothing serious. Edison gives no number for Cu-W solubility; in my judgment it is negligible. W is not in TCCU7. The price conversion is correct (1 mtu WO3 = 7.93 kg W).

**Recommendation:** Keep EXCLUDE. No impurity cap is needed, since the feed has no plausible source of W. If repair preparation uses GTAW, watch for tungsten-electrode inclusions.

## Ta

**VERDICT** `VERDICT | Ta | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- Cu-Ta has no equilibrium solid or liquid solubility and no compounds. Only vapor-deposited condensates trap Ta, at 0.05-3 at.% (0.14-8.1 wt%). Ta forms a second phase above about 0.85 wt% and the solution decomposes above 500 °C (Riaboshtan 2025, *Functional Materials* 32:250-258, 10.15407/fm32.02.250). Ta melts at about 3,017 °C.
- Chloride benefits appear only in metallic glasses, all in 3% NaCl:
  - In Cu-Zr-Ti glass, about 0.47 Ta lowered the rate from 290 to 200 µm/y (Asami 2004, *MSEA* 375-377:235-239, 10.1016/j.msea.2003.10.034).
  - In Cu-Hf-Ti glass, about 4.2 Ta lowered it from about 0.1 to 0.001 mm/y (Qin 2003, *Mater. Trans.* 44:1042-1045, 10.2320/matertrans.44.1042).
- Ta dust has an OSHA PEL of 5 mg/m³. Ta powder has a minimum explosible concentration of 160-400 g/m³ and a minimum ignition energy below 3 mJ (Benson 2012).

**Interactions:** Ta with Ni and Ta with Al are flagged as unresolved, with no numbers.

**DOI check:** Riaboshtan OK. Asami OK. Qin OK.

**Red flags**
- Edison says TCCU coverage is "not verified". In fact Ta **is in TCCU7**, with Cu-Ni-Ta and Cu-Fe-Ta assessed. Immiscibility decides the question anyway.
- The answer missed Singh 1992 (*J. Appl. Electrochem.* 22:1175, cited in the Nd file), which studied Ta in Al-bronze. That work was in mineral acids, so the decision is unchanged.
- The at% to wt% conversions are correct.

**Recommendation:** Keep EXCLUDE. No impurity cap is needed.

## Ge

**VERDICT** `VERDICT | Ge | decision=INCLUDE | family=Al-bronze | conservative_max_wt=0.2 | nonconservative_max_wt=3.0 | floor_wt=0.2 | impurity_max_wt=NA | evidence=thin`

**Key facts**
- An NAB-like P/M alloy, Cu-9.5Al-5Ni-4.5Fe-0.9Mn-0.2Ge (0.179 Ge measured), was sintered, solution-treated and aged. Its 10 h jet erosion-corrosion loss in 3.5% NaCl was 0.022 g/cm² versus 0.032 for the Ge-free alloy (−31%). However, Mn (1.31→2.00), Fe (4.37→4.86) and Ni also changed (Aslan 2020, *IOP Conf. Ser. MSE* 987:012018, 10.1088/1757-899X/987/1/012018).
- A second-hand report: Cu-Al-Ni SMA made by P/M corroded at 4.72 mpy with 3 Ge versus 34.99 mpy (0.120 vs 0.889 mm/y) in 3.5% NaCl. The source is Haleem & Hashim 2018, reported by Dawood 2020 (*Iraqi J. Mech. Mater. Eng.* 20:362-375, 10.32852/iqjfmme.v20i4.530).
- α-Cu dissolves up to about 13.1 Ge, and Ge lowers the liquidus (Wang 2010, *J. Alloys Compd.* 504:159-165, 10.1016/j.jallcom.2010.05.077). Ge costs US$1,000-4,000/kg and is a critical mineral.

**Interactions:** Screen Ge together with Al, Ni, Fe and Mn. No sum or ratio rules exist.

**DOI check:** Aslan OK. Dawood OK. Wang 2010 OK. The primary Haleem & Hashim paper is not found in Crossref.

**Red flags**
- The INCLUDE rests on one heat-treated sample with a confounded composition, plus a second-hand SMA result. The 3.0 bound comes entirely from the second-hand result.
- The floor and the conservative maximum are both 0.2, so the conservative range has zero width.
- TCCU7 has Ge but neither Cu-Al-Ge nor Cu-Ni-Ge.
- My judgment: Ge probably widens the freezing range, as Sn and Si do, which is an untested hot-cracking risk. Its export controls also work against the critical-mineral objective.

**Recommendation:** Adjust. Treat Ge as an optional, low-priority variable for Al-bronze only, at 0 or 0.2 in the conservative space, with the aggressive bound at about 1 until the primary 3 wt% source has been read.

## Ca

**VERDICT** `VERDICT | Ca | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- No marine copper alloy contains Ca, and no corrosion study has controlled Ca content. Davies (CDA 1993, no DOI) only proposes testing Ca as a deoxidizer in brass.
- Ca found on corroded C706 Cu-Ni is a seawater deposit on cathodic areas, not alloyed Ca (Parvizi 1985 thesis).
- Ca feed reacts with moisture to form CaO, Ca(OH)2, CaCO3 and H2. Ca metal carries 0.1-0.3 O and 0.2-0.3 Cl (Talanov 2014). CaO and ZrO2 convert fully to CaZrO3 at about 1,200 °C (Jahn 2020), which is a risk for zirconia crucibles.
- Baseline only: C71500 corrodes at 0.3-0.5 mpy in quiet seawater and 0.5-0.7 mpy at 0.61 m/s (Lewis & LaQue 1981, OSTI, 10.2172/6255887).

**Interactions:** O and S consume Ca, and CaB6 would also add B. Nothing has been quantified.

**DOI check:** Lewis & LaQue 1981 OK. Risold 1995, Ca-Cu-O assessment (*J. Am. Ceram. Soc.* 78:2655-2661, 10.1111/j.1151-2916.1995.tb08036.x), OK. Olinger 2026, USGS GIP 266, OK.

**Red flags**
- Edison found no Cu-Ca phase data, but Ca **is in TCCU7** (the Cu-Ca binary is assessed, with no ternaries), so the solvus and liquidus can be calculated.
- My judgment points the same way as Edison:
  - Ca is almost insoluble in solid Cu and forms Cu5Ca through a Cu-rich eutectic near 900 °C, a low-melting phase between dendrites.
  - Ca is volatile (it boils at 1,484 °C).
  - Ca can reduce alumina and zirconia.
- Most of the sources are theses without DOIs.

**Recommendation:** Keep EXCLUDE. No impurity cap is needed.

## Sc

**VERDICT** `VERDICT | Sc | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- Cast Cu-0.16Sc and Cu-0.28Sc (graphite crucible, 1,350 °C) already showed eutectic and 5-10 µm Sc-rich particles on grain boundaries as cast. Hardening came only after aging at 450 °C: 43→62 HV after 15 h and 55→70 HV after 20 h. Maximum solubility is about 0.5 Sc at 1,130 K, with Cu4Sc, Cu2Sc and CuSc phases (Franczak 2020, *Arch. Civ. Mech. Eng.* 20:28, 10.1007/s43452-020-00035-z).
- TCCU5 does not include Sc (Jansson, Copper Alloys 2022 proceedings, no DOI). There are no seawater, DED or weld data.
- Edison cites a price of US$185,000-210,000/kg for Sc metal (Sverdrup 2024, *Biophys. Econ. Sustain.* 9, 10.1007/s41247-024-00118-y).

**Interactions:** None quantified. Oxygen consumes Sc.

**DOI check:** Franczak 2020 OK. Sverdrup 2024 OK. Nemani 2024, AM review (*JMMP* 8:54, 10.3390/jmmp8020054), OK.

**Red flags**
- The price looks like per-gram laboratory pricing multiplied up to a kilogram (my judgment). Sc bought as a master alloy would cost far less, but still a lot, and the decision does not change.
- The solubility was read from a figure that mixes at% and wt% axes; Edison flags this.
- Sc is also absent from TCCU7, which is consistent.
- The compound wt% values are correct.

**Recommendation:** Keep EXCLUDE.

## Pr

**VERDICT** `VERDICT | Pr | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- Cu-Pr forms PrCu6 (≈27.0 Pr), PrCu5, PrCu4, PrCu2 and PrCu. PrCu13 appears only after rapid quenching and may be metastable (Riani 2002, *J. Phase Equilib.* 23:7-28, 10.1361/105497102770332171).
- A binary assessment exists (Zhuang 1996, *J. Phase Equilib.* 17:508-521, 10.1007/BF02665998).
- The only rare-earth precedent in copper is for Ce: 0.1 Ce improved the hot ductility of Cu-40Zn-1Pb, while mixed rare earths caused gas blisters (Savitskii 1961, *Met. Sci. Heat Treat.* 3:391-400, 10.1007/BF00812593).
- Elemental Pr burns at about 150 °C. There are no numbers for seawater behaviour, DED or solubility.

**Interactions:** None quantified.

**DOI check:** Riani 2002 OK. Zhuang 1996 OK. Savitskii 1961 OK.

**Red flags**
- The binary facts come secondhand from Riani, which is a review of R-Cu-Ge ternaries.
- Pr is **not in TCCU7**, so the project database cannot model it.
- My judgment: Chinese literature uses about 0.01-0.1 Ce, La or mischmetal as a deoxidizer and grain refiner. If rare-earth treatment is wanted, it should be a single lumped Ce/La variable (both are in TCCU7), not Pr.

**Recommendation:** Keep EXCLUDE.

## Nd

**VERDICT** `VERDICT | Nd | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.01 | evidence=thin`

**Key facts**
- The only Nd datum is second-hand: 0.05 La, Ce or Nd improved the general corrosion of Al-bronze in dilute H2SO4 and HNO3. This comes from Davies 1993, citing Verma 1990 and Singh 1992 (*J. Appl. Electrochem.* 22:1175-1179, 10.1007/BF01297420).
- Mischmetal added to Cu-Zn-Pb at 0.50 left only 0.04 total rare earths (about 8% recovery), with the loss attributed to oxidation (Davies 1993).
- NdCu4, NdCu5 and NdCu6 form in Cu-Nd droplets at 900-1,040 °C (Ciumag 2016, *J. Fluorine Chem.* 184:1-7, 10.1016/j.jfluchem.2016.02.001).
- There are no data on seawater behaviour, DED or solubility.

**Interactions:** Oxygen matters first (loss and inclusions), then Al, Ni, Fe and Mn. Nothing is quantified.

**DOI check:** Ciumag 2016 OK. Singh 1992 OK; its title confirms "Ta, La and Nd" in Al-bronze in mineral acids. Carnasciali 1983, Nd-Cu equilibria (*J. Less-Common Met.* 92:97-103, 10.1016/0022-5088(83)90230-8), OK.

**Red flags**
- The 0.01 limit is Edison's own QC choice ("not a specification") and has no source.
- On equivalent evidence, Pr, Er and Gd were given EXCLUDE with impurity NA, so the decisions are inconsistent.
- Nd is not in TCCU7, and the acid data do not apply to seawater.

**Recommendation:** Adjust to EXCLUDE with impurity NA, to match Pr, Er and Gd. Alternatively, apply one shared non-specification QC flag of total rare earths ≤0.01 to all of them. The value hardly matters, since the feed contains essentially no Nd.

## Er

**VERDICT** `VERDICT | Er | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- In Cu-Er, ErCu5 has been observed; Er2Cu9 is assigned only by analogy (Riani 2002, 10.1361/105497102770332171).
- The only chloride data are for Al-balance alloys (1.3-1.4 Er, 2.6-3.0 Cu), with icorr of 0.68-0.98 µA/cm² in 3.5% NaCl. These cannot be transferred (Glavatskikh 2024, *Metals* 14:547, 10.3390/met14050547).
- Er2O3 stability has been shown only in iron melts (Wang 2026, IJMMM, 10.1007/s12613-026-3587-2).
- There are no figures for Cu solubility, liquidus, seawater behaviour, DED or price.

**Interactions:** None quantified. Candidates are O, Al and Fe from NAB dilution, and Ni at a Cu-Ni interface.

**DOI check:** Riani OK. Glavatskikh OK. Wang 2026: **the DOI does not resolve** (404 at both Crossref and doi.org); Edison calls it an accepted manuscript.

**Red flags:** Two of the three sources are on other matrices, and the only Cu-related source is a secondary phase review. Er is not in TCCU7.

**Recommendation:** Keep EXCLUDE.

## Gd

**VERDICT** `VERDICT | Gd | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- The answer contains no quantitative Gd data for any Cu alloy. It lists the following work by DOI only and read none of it in full:
  - Cu-Gd binary (Carnasciali 1983, *J. Less-Common Met.* 92:143-147)
  - rapid-solidification solubility (Zhou 1992, *J. Alloys Compd.* 183:168-173)
  - an Al-Cu-Gd assessment (Zhang 2009, *Calphad* 33:664-672)
  - a new study of corrosion in Cu-Al-Ni-Mn-Gd SMA (Zhang 2026, *Intermetallics* 197:109445)
- Gd is on the 2022 and 2025 lists, and China has controlled Gd exports since April 2025.

**Interactions:** None quantified.

**DOI check:** Carnasciali 1983 (10.1016/0022-5088(83)90235-7) OK. Zhang 2009 (10.1016/j.calphad.2009.08.003) OK. Zhang 2026 (10.1016/j.intermet.2026.109445) OK; the title matches.

**Red flags**
- The citations are poorly matched to the claims. They are tagged to unrelated retrieved sources: a USGS mining review and an Oishi patent on electrical Cu-Zn-Sn sheet (US 9,080,228). Beyond supply status, nothing in the answer is backed by evidence.
- Gd is not in TCCU7.

**Recommendation:** Keep EXCLUDE: there are no data, Gd is not in TCCU7, and it is a critical mineral. If rare earths in Al-bronze are revisited, read Zhang 2026.

---

# Group 2

## Group 2 digest: Ni, Al, Fe, Cr, Sn, Zn, Si, Nb, Be, Co

Source answers: `edison-trajectories/cu-ded-elements-2026-10/phase1/el-*.md`. I checked DOIs against Crossref on 2026-10-17 (the UNSW thesis DOI against DataCite). All 38 DOIs I checked resolve to the title, journal and year Edison gives. "My judgment" or "my recollection" marks reviewer knowledge that is not in Edison's answer; verify it before citing. For CALPHAD coverage, the local file `tccu7_coverage.md` answers several questions Edison left as [GAP].

## Ni

**VERDICT:** `VERDICT | Ni | decision=INCLUDE | family=both | conservative_max_wt=33 | nonconservative_max_wt=35 | floor_wt=2 | impurity_max_wt=NA | evidence=moderate`. The body splits this by family: Cu-Ni 33/35, and NAB 5.5 (conservative) and 7 (exploratory). The floor is 2 for both.

**Key facts**
- 2-h stagnant test in 3.5% NaCl at 25 °C: pure Cu corroded at 92.4 µm/y. Alloys with 9.3, 18.8, 28.4 and 48.0 wt% Ni gave 55.0, 44.2, 29.0 and 20.6 µm/y. Rp rose from 4,155 to 18,019 Ω·cm² and Ecorr moved from -304.5 to -202.8 mV SCE. Source: Yang 2019, UNSW thesis, 10.26190/unsworks/21760. This is a very short test.
- Natural seawater (Lewis & LaQue 1981, DOE report, 10.2172/6255887):
  - C70600 and C71500 corrode at 2.5-12.7 µm/y, falling below 2.5 µm/y after 14-16 y.
  - Accepted design velocities are 3.6 m/s for C70600 (about 1.4 Fe), 4.6 m/s for C71500 (about 0.5 Fe) and above 9 m/s for C72200.
  - The 90/10 and 70/30 ranges overlap, so 10→30 Ni shows no monotonic benefit in service.
- NAB, as-cast C95800 (8.79Al-4.50Ni-3.70Fe-1.00Mn) in 3.5% NaCl: 0.02 mm/y stagnant and 0.06 mm/y at 9,000 rpm. Annealing cut β from >20% to about 7% (Jafari 2021, Corros. Mater. Degrad. 2:61-77, 10.3390/cmd2010004).
- Laser DED of Cu-9Al-5Fe-5Ni gave yield strength 593-713 MPa and elongation 10-12% (Nemani 2024 review, JMMP 8:54, 10.3390/jmmp8020054).
- Cu-Ni is a complete fcc solid solution (Schmid-Fetzer 2014, 10.1007/s11669-014-0343-5). Cu-Al-Ni is assessed on the Cu-Ni side (Miettinen 2005, 10.1016/j.calphad.2005.02.002).

**Interactions**
- Ni x dissolved Fe: 90/10 needs about 1.3-2.0 Fe to match 70/30 in flowing seawater; 70/30 uses about 0.4-0.7 Fe.
- In NAB, Ni must be set jointly with Al and Fe (κIII NiAl versus Fe3Al κ). Edison gives no numbers. Two rules from my recollection:
  - ASTM B148 C95800 requires Fe ≤ Ni.
  - The NAB selective-corrosion guideline Al ≤ 8.2 + 0.5·Ni (Weill-Couly & Arnaud; quoted in Wharton et al., Corros. Sci. 2005).
- TCCU7 assesses Cu-Ni-Al, Cu-Ni-Fe, Cu-Ni-Mn and Cu-Ni-Cr.

**DOI check:** 10.2172/6255887 DOI OK. 10.26190/unsworks/21760 DOI OK (DataCite). 10.3390/cmd2010004 DOI OK. Miettinen, Schmid-Fetzer and Nemani also DOI OK.

**Red flags**
- **Liquidus.** My estimate is an ideal-solution Cu-Ni model, shifted +20 °C to match the handbook liquidus of C70600 (about 1,150 °C) and C71500 (about 1,240 °C). It gives about 1,250 °C at 33 wt% Ni and about 1,257-1,260 °C at 35 wt%. So 33 sits on the 1,200-1,250 °C atomization limit and 35 exceeds it. Edison gives no number and calls this a [GAP].
- The 2 wt% floor is arbitrary. The lowest commercial seawater Cu-Ni is C70400 (95/5, about 4.8-6.2 Ni with 1.3-1.7 Fe), from my recollection.
- Edison could not verify C71640, AWS A5.7, the MIL specs or MARINEL, and leans on one 1981 compilation and one review.

**Recommendation:** Keep INCLUDE.
- Cu-Ni: conservative 31 (33 only if CALPHAD/DSC shows liquidus ≤1,250 °C); drop 35 and use 33 as the non-conservative bound.
- NAB: 5.5/7 with Fe ≤ Ni.

## Al

**VERDICT:** `VERDICT | Al | decision=INCLUDE | family=both | conservative_max_wt=9.5 | nonconservative_max_wt=10.5 | floor_wt=1.8 | impurity_max_wt=NA | evidence=moderate`. The body gives a separate Cu-Ni-Al branch at 3.0/5.0 ("provisional"), which is not in the VERDICT line.

**Key facts**
- C95800: 8.5-9.5 Al, 4-5 Ni, 3.5-4.5 Fe, 0.8-1.5 Mn, which matches the standard (Iannuzzi 2017, JES 164:C488, 10.1149/2.0391709jes). CC333G: 8.5-10.5 Al, 4.0-5.5 Fe, 4.0-6.0 Ni. Edison calls it "DIN 1982"; it is EN 1982.
- Binary Cu-Al: eutectic L→(Cu)+β at 1,035 °C; eutectoid β→(Cu)+γ1 at 567 °C, with α at 81.5 at% Cu, about 8.8 wt% Al (Ponweiser 2011, Intermetallics 19:1737, 10.1016/j.intermet.2011.07.007). The classic diagram gives about 9.4 wt%.
- NAB with 10.4-10.9 Al and 4.4-5.5 Fe/Ni has liquidus 1,082.6 °C and solidus 1,023.3 °C (Pisarek 2013, AFE 13:72, 10.2478/afe-2013-0063). Al never threatens the atomizer ceiling.
- A close rePOWDER analogue: CuAl10Ni5Fe5 induction-melted at 1,300 °C under Ar and ultrasonically atomized at 40 kHz (Uhlmann 2024, Materials 17:3396, 10.3390/ma17143396).
  - Powder O was 0.013 wt% versus 0.073 in the chips.
  - EDX gave Al 9.83 versus 10.4; the authors say the apparent 0.57 wt% loss is not reliable.
- Wire-arc AM of Cu-9Al-4Fe-4Ni-1Mn was sound: yield 388 MPa and elongation 26% (Dharmendra 2019, Addit. Manuf. 30:100872, 10.1016/j.addma.2019.100872).

**Interactions**
- Al with Ni+Fe: κ phases take Al out of α, and Ni/Fe suppress γ2. Edison gives no numeric rule.
- Add Al ≤ 8.2 + 0.5·Ni together with Fe ≤ Ni (my recollection, see Ni). Under this rule, 10.5 Al needs Ni ≥ 4.6.
- Dilution: Al_int = (1-d)·Al_powder + d·Al_substrate.
- TCCU7 assesses Cu-Al-Ni, Cu-Al-Fe and Cu-Al-Mn, but not Cu-Al-Cr.

**DOI check:** Uhlmann, Pisarek, Dharmendra and Iannuzzi are DOI OK. Takaloo, 10.4236/msa.2011.211207: the DOI is valid and points to *Materials Sciences and Applications* 2:1542-1555 (2011), but Edison's reference list says "J. Metall. Mater. Sci. 53:67-84". This is a metadata error; the body text names the journal correctly.

**Red flags**
- The VERDICT's "family=both" applies 9.5/10.5 to both families. Those bounds hold only for Al-bronze.
- The 1.8 floor comes from Cu-22Zn-2Al brass, but Zn is LIMITed. The real NAB floor is 8.5. For Cu-Ni-Al, 1.8-2 fits MARINEL (about 1.9 Al).
- As-deposited laser NAB at 9 Al is already β′ martensite plus α (Li 2021). β′ is the phase prone to selective corrosion. The single-review claim that martensitic L-PBF NAB loses 10x less mass contradicts this, and Edison does not reconcile the two.
- 10.5 is below the C95500/C95520 (11.5) and C63000 (11.0) maxima, so it is mild rather than aggressive.

**Recommendation:** Keep NAB 9.5/10.5 with the NAB floor at 8.5. Keep the Cu-Ni-Al sub-branch at 1.8 to 3 (exploratory to 5). Add Al ≤ min(10.5, 8.2 + 0.5·Ni) and Fe ≤ Ni.

## Fe

**VERDICT:** `VERDICT | Fe | decision=INCLUDE | family=both | conservative_max_wt=5.0 | nonconservative_max_wt=6.0 | floor_wt=0.4 | impurity_max_wt=NA | evidence=moderate`. The body gives:
- Cu-Ni: floor 0.4; conservative 1.8 (90/10) or 1.0 (70/30); non-conservative 2.0.
- NAB: floor 2.0; conservative 5.0; non-conservative 6.0 ("provisional").

**Key facts**
- Fe must stay in solution (Kievits & IJsseling 1972, Werkst. Korros. 23:1084, 10.1002/maco.19720231203). After 6 months in flowing seawater:
  - 11.6Ni-1.05Fe (0.08 Fe precipitated) gave a film with 15 wt% Fe.
  - 11.3Ni-1.99Fe (1.84 Fe precipitated) gave only 4.3 wt% Fe in the film.
  - The precipitate is about Cu51-Ni31-Fe17. Dissolved Fe helps impingement resistance; precipitated Fe promotes pitting.
- Quiet seawater: 0.2-0.6 mpy for C70600 and 0.3-0.5 mpy for C71500; design velocities 3.6 and 4.6 m/s (Lewis & LaQue 1981).
- Wire-arc AM 70/30 (0.55 Fe) on C71500 plate had no pores or cracks (Song 2024, Materials 17:876, 10.3390/ma17040876).
  - After 3 h in 3.5% NaCl, film resistance was 1.40-1.66e5 Ω versus 1.08-1.18e5 Ω for wrought (reported in Ω, not Ω·cm²).
  - Ni-depleted interdendritic regions were attacked.
  - This is the best evidence that as-deposited 70/30 can match wrought.
- Laser DED of Cu-9Al-5Fe-5Ni (powder 5.48 ± 0.86 Fe) reached 99.55% density at 1,000-1,500 W; too much power caused hot cracks; as deposited it was β* + α with Fe3Al/NiAl (Li 2021, Addit. Manuf. 39:101825, 10.1016/j.addma.2020.101825).

**Interactions**
- Ni x Fe in solution; Al-Fe-Ni κ; Mn-Fe; Fe-Si silicides. Edison found no validated ratio.
- From my recollection:
  - C95800 requires Fe ≤ Ni.
  - C71640 carries 1.7-2.3 Fe with 1.5-2.5 Mn at about 30 Ni, so Cu-Ni tolerates more Fe when Ni and Mn are high.

**DOI check:** Kievits DOI OK; Li 2021 DOI OK; Song 2024 DOI OK. Cobo Ocejo (10.3390/met12030380) DOI OK.

**Red flags**
- Edison's "C71500-type 30.0-32.0 Ni, 0.5-1.5 Mn" and "C70600 0.5-1.0 Mn" are the EN grades CW354H and CW352H, not UNS (C71500 is Ni 29-33 with Mn ≤1). Its Fe ranges do match UNS.
- The VERDICT mixes a Cu-Ni floor with NAB maxima. 5-6 Fe must never reach the Cu-Ni branch.
- The Cu-Ni non-conservative 2.0 is below commercial C71640 (2.3).
- NAB at 6.0 is above every commercial NAB I know (≤5.5 in CC333G and C95520) and breaks Fe ≤ Ni unless Ni ≥ 6. In my judgment, Fe above about 5 also brings primary Fe-rich κI and a steeper liquidus.
- DED-specific risk (my judgment): fast cooling keeps Fe in solution, but reheating by later layers (about 400-700 °C) can precipitate Fe-Ni phase.

**Recommendation:** Keep INCLUDE, but set bounds by family.
- Cu-Ni: floor 0.4, conservative 1.8, non-conservative 2.3 (C71640, with Mn ≤2.5).
- NAB: floor 2.0, conservative 5.0, non-conservative 5.5, with Fe ≤ Ni.

## Cr

**VERDICT:** `VERDICT | Cr | decision=INCLUDE | family=Cu-Ni | conservative_max_wt=0.5 | nonconservative_max_wt=2.0 | floor_wt=0.5 | impurity_max_wt=NA | evidence=moderate`

**Key facts**
- C72200 (Cu-15Ni-0.8Fe-0.5Cr) against C71500 (Lewis & LaQue 1981; El Din 1993, Desalination 93:487, 10.1016/0011-9164(93)80124-6):
  - Critical velocity 12.0 versus 4.1 m/s.
  - Critical shear 2,969 versus 479 dyn/cm².
  - Design velocity >9 versus 4.6 m/s.
- The cost shows in quiet water (Lewis & LaQue):
  - Quiet seawater: C72200 corrodes at 0.4-0.9 mpy with 1 mil pits, versus 0.3-0.5 mpy and 1-2 mil for C71500.
  - Higher-Cr C71900 corrodes at 1.3/3.1/5.3 mpy versus 2.7/24.6/44.5 for C71500 at 9.5/26.3/51.5 ft/s.
  - But with no flow, C71900 had deeper crevice attack (0.003-0.009 in versus nil-0.006 in).
- Laser NAB on SUS630 picked up 1.9 Cr from a Ni-20Cr interlayer (Zhao 2022, Metals 12:781, 10.3390/met12050781). After 21 days in 3.5% NaCl, maximum attack was 1.8 µm, versus 2.0 µm with a Ni-only interlayer and 3.4 µm with none. The result is confounded.
- The Cu-Cr eutectic is at 1,076 °C and 1.27 wt% Cr, which is the liquid composition, not the solubility.
- Cu-~4.1Cr formed a persistent Cr-oxide shell on alumina, with contact angles of 128-138° at about 1,260 °C (Zygmuntowicz 2026, ASTRJ 20:263, 10.12913/22998624/225757).

**Interactions**
- Cr x Fe x Ni; Edison gives no numeric constraint.
- My judgment: the Cr cap should scale with Ni.
  - C72200: 0.3-0.7 Cr at 15-18 Ni.
  - C71900: about 2.2-3.0 Cr at about 30 Ni.
  - Cast CuNi30Cr2 (Def Stan 02-824): about 1.5-2.0 Cr.
- In Ni-poor melts, Cr above about 1.3 wt% is hypereutectic with a steep liquidus, so some Cr would stay undissolved at 1,300 °C.
- TCCU7 assesses Cu-Ni-Cr and Cu-Fe-Cr but not Cu-Al-Cr, which supports keeping Cr out of NAB.

**DOI check:** El Din DOI OK; Zhao 2022 DOI OK; Zygmuntowicz DOI OK (November 2026 issue).

**Red flags**
- Conservative max equals the floor (0.5), so the interval is degenerate. The C72200 spec is 0.3-0.7.
- Edison could not verify the Cr range of C71900 or IN-768, so its 2.0 has no anchor in its own text.
- The 30-day stagnant immersion screen is exactly where Cr alloys did worse than C71500.

**Recommendation:** INCLUDE for Cu-Ni only, with floor 0.3 and conservative 0.7. Allow non-conservative 2.0 only when Ni ≥ about 25. Treat Cr in NAB as an impurity.

## Sn

**VERDICT:** `VERDICT | Sn | decision=INCLUDE | family=both | conservative_max_wt=1.0 | nonconservative_max_wt=1.5 | floor_wt=0.5 | impurity_max_wt=NA | evidence=moderate`

**Key facts**
- The only controlled Sn series is a mechanically alloyed, microwave-sintered Cu-Al-Ni shape-memory alloy in 3.5% NaCl (Saud 2016, MMTA 47:5242, 10.1007/s11661-016-3628-y).
  - At 0, 0.5, 1.0 and 1.5 Sn: 3.19, 2.16, 0.62 and 2.56 mm/y.
  - icorr: 139.8, 94.8, 27.3 and 112.1 µA/cm².
  - The worsening at 1.5 is partly attributed to porosity.
  - Even the best rate is about 30x the 0.02 mm/y of cast NAB.
- Cast NAB with about 1.0 Sn: grains became equiaxed, hardness rose up to 69% and UTS up to 28.4%. These are mechanical results only (Poojary 2023, Sci. Rep. 13:16907, 10.1038/s41598-023-44146-y).
- Aged powder-metallurgy Cu-15Ni-8Sn in ASTM D1141 for 70 d: 0.00498 mm/y at pH 8, but with pits and intergranular attack (Cheng 2020, Mater. Corros. 71:593, 10.1002/maco.201911323).
- Critical velocities: Admiralty brass 1.83 m/s, 90-10 4.57 m/s, 70-30 5.49 m/s (LaQue 1969, Ocean Eng. 1:299, 10.1016/0029-8018(69)90031-6).
- In tin-bronze welds, Sn liquation, hot cracking and δ phase are recurring problems (Majdanchuk 2014, 10.15407/tpwj2014.01.09).
- Cu-Sn phase data (Valloton 2012, 10.1016/j.actamat.2012.03.030):
  - α solubility peaks at about 15.8 wt% near 520 °C.
  - Peritectic at about 798 °C.
  - Sn widens the freezing range.

**Interactions:** Sn x Al shows a chloride optimum near 1 Sn in the sintered SMA only. Sn x Ni forms the Cu-15Ni-8Sn spinodal, which needs aging. Edison gives no other numbers.

**DOI check:** Saud DOI OK; Poojary DOI OK; Cheng DOI OK (online 2019, volume 71 in 2020). LaQue DOI OK.

**Red flags**
- The bounds rest on a porous sintered SMA that is neither NAB nor Cu-Ni nor DED.
- The "1 wt%" anchors are Zn-bearing brasses (Admiralty brass, Nordic Gold).
- Specs conflict (my recollection), because in the target families Sn is an impurity:
  - C63000: Sn ≤0.20.
  - EN CuNi10Fe1Mn: ≤0.03; CuNi30Mn1Fe: ≤0.05.
  - CC333G: about ≤0.1.
- Sn's wide freezing range works against crack-free DED and repair.
- The Allen 2000 DOE report (10.2172/765235, cited in the Be file) tested Sn as a C95800 impurity. Pull its proposed limit.
- Tin was also on the 2022 critical-minerals list (my knowledge); Edison could not confirm this.

**Recommendation:** Downgrade to LIMIT in the core branches: NAB ≤0.2 and Cu-Ni ≤0.05. At most keep an exploratory NAB-only axis of 0.5-1.0; drop 1.5 and the Cu-Ni-Sn branch.

## Zn

**VERDICT:** `VERDICT | Zn | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.5 | evidence=thin`

**Key facts**
- L-PBF of CuZn42 with a 1,070 nm laser (Marchini 2026, Prog. Addit. Manuf. 11:7697, 10.1007/s40964-026-01764-y):
  - Zn fell from about 43 wt% in the powder to 35.46 in the deposit, a relative loss of about 17.5%.
  - 30-day dezincification in 3.5% NaCl was 790 ± 32 µm versus 247 ± 12 µm for wrought.
  - Ecorr was -643 versus -537 mV SCE.
  - Porosity confounds the comparison.
- In 1 M NaCl, C26000 brass dealloys and shows no passivity at pH 6.5. C71500 is a Zn-free reference in the same study (Alfantazi 2009, Mater. Des. 30:2425, 10.1016/j.matdes.2008.10.015).
- As inhibits dezincification in α-brass at 0.024-0.084 wt%, but 0.25 As worsens duplex brass (Davies 1993, CDA note, no DOI).
- Zn lowers the liquidus (about 930 °C at 32.5 Zn), and α extends to 38.3 at% (about 39 wt%). Zn boils at 907 °C. An Al-Cu-Zn CALPHAD assessment exists.

**Interactions:** Zn+Al and Zn+Sn matter in brasses; Fe and Mn worsen brass dezincification. In this project Zn is only a contaminant, from scrap, master alloys or substrate dilution.

**DOI check:** Marchini DOI OK; Alfantazi DOI OK. Liang & Schmid-Fetzer, 10.1016/j.calphad.2015.11.001: DOI OK (Calphad 52:21-37, 2016, Al-Cu-Zn Part III).

**Red flags:** Edison verified no specs, so "evidence=thin" understates the support for the cap. From my recollection:
- C71500 and C70600: Zn ≤1.0 (≤0.5 when for welding).
- EN Cu-Ni and CC333G: ≤0.5.
- C63000: ≤0.30.
- ERCuNiAl about ≤0.10; ERCuAl-A2 about ≤0.02.
- The Nb file independently quotes a Cu-Ni weld residual limit of Zn 0.50 (Klassert & Tikana 2007).

**Recommendation:** Keep LIMIT ≤0.5. Consider ≤0.3 for NAB-branch powder to match C63000. Charges of OFHC Cu and pure metals meet this easily.

## Si

**VERDICT:** `VERDICT | Si | decision=INCLUDE | family=both | conservative_max_wt=2.0 | nonconservative_max_wt=3.8 | floor_wt=0.5 | impurity_max_wt=NA | evidence=thin`

**Key facts**
- Precedents: C65500 at 2.8-3.8 Si and C64200 at 1.5-2.2 Si. C64200 and C95600 are about 2Si-7Al.
- Cast Cu-Al-Si-Mn with 0-2 Si, 3-9 Al and 0-2 Mn is single-phase. Swapping Al for Si/Mn raises ductility and lowers strength (Kimstach 2025, Nauk. Visn. NHU 2025(2):113, 10.33271/nvngu/2025-2/113).
- The only Si-NAB saline study is internally inconsistent (Dongo 2024, FUOYE JET 9:117, 10.4314/fuoyejet.v9i1.18):
  - The nominal 0-10 Si series measured 0-0.80 Si.
  - The "2 wt%" optimum is labelled inconsistently.
  - Some corrosion rates are negative.
  - Edison correctly rejects the study.
- Cu-Si: α solubility peaks at about 5.25 wt% near 842-852 °C, and Si lowers the liquidus. Cu-Si and Al-Cu-Si are assessed (Kroupa 2024, JPED 45:1206, 10.1007/s11669-024-01160-5).
- In brass, 0.33 Si gave a duplex structure prone to dezincification, while 0.5 Si retarded dezincification in 60/40 brass (Davies 1993).

**Interactions**
- Ni:Si is about 4.18:1 by mass for Ni2Si (arithmetic checked).
- Al-Si-Mn trade-off.
- Si-Nb weldability pairing from the Nb file: Nb ≥ 2·Si, or Nb > 1.55·Si - 0.10.
- TCCU7 assesses Cu-Ni-Si and Cu-Al-Si.

**DOI check:** Kroupa DOI OK; Dongo DOI OK; Kimstach DOI OK.

**Red flags**
- **The VERDICT contradicts the body.**
  - The body caps Cu-Ni at ≤1.0.
  - It says 2.0 applies only to low-Al Al-Si bronze ("do not apply to C95800").
  - It says 3.8 applies only to a separate silicon-bronze branch.
  - Yet the VERDICT says "both" at 2.0/3.8.
- Spec conflict (my recollection): in the target alloys Si is a tightly limited impurity.
  - C95800: Si ≤0.10 (ASTM B148).
  - CC333G, ERCuNiAl and ERCuAl-A2: about ≤0.10.
  - C63000: ≤0.25.
  - C72200: ≤0.03.
  - Cast Cu-Ni carries Si only alongside Nb (C96400 ≤0.50, C96200 ≤0.30).
- Si promotes hot cracking in Cu-Ni welds (the task text says so too). A deposit with 2-3.8 Si diluting into C95800 would leave an off-spec, crack-prone interface.

**Recommendation:** Change to LIMIT in the core branches: NAB ≤0.10; Cu-Ni ≤0.3-0.5, and only paired with Nb ≥ 2·Si. Move 2.0-3.8 Si to an optional separate silicon-bronze branch.

## Nb

**VERDICT:** `VERDICT | Nb | decision=INCLUDE | family=Cu-Ni | conservative_max_wt=0.80 | nonconservative_max_wt=1.00 | floor_wt=0.50 | impurity_max_wt=NA | evidence=thin`

**Key facts**
- Cast Cu-Ni practice (Van Konynenburg et al. 1990, DOE report, 10.2172/137782):
  - Strengthened 70-30 uses about 0.4 Si with Nb ≥ 2·Si.
  - 90-10 uses 0.10-0.15 Si with 0.50-0.70 Nb.
  - Ni-Nb-Si precipitates form even during slow casting.
- Weldability heuristic: Nb > 1.55·Si - 0.10. The same overview limits Cu-Ni weld residuals to P, S ≤0.02, Zn ≤0.50, Pb ≤0.02 and C ≤0.05 (Klassert & Tikana 2007, no DOI).
- US patent 5,164,157 (Clark & Guha 1992) is a Cu-Ni-Mn-Al-Cr-Nb fastener alloy claiming 0.50-1.00 Nb, aged.
- GRCop-84 (Minneci 2024, MMTA 55:1377, 10.1007/s11661-024-07315-w):
  - Cr2Nb dissolves only near 1,900 K (about 1,627 °C).
  - At 2,100 K, vapor pressures are Cu 1,090 Pa and Nb 9.2e-6 Pa, so Nb does not evaporate.
- Cu on Nb has contact angles of 69° at 1,090 °C and 42° at 1,200 °C (de Lima 1985, JMS 20:2464, 10.1007/BF00556075). Dissolving pure Nb at 1,300 °C is therefore uncertain.

**Interactions:** Two constraints, which are not interchangeable: Nb - 1.55·Si + 0.10 > 0, and Nb/Si ≥ 2. Also Cr:Nb (Cr2Nb). TCCU7 assesses Cu-Ni-Nb and Cu-Cr-Nb, but not Cu-Al-Nb.

**DOI check:** Van Konynenburg DOI OK; Minneci DOI OK; de Lima DOI OK.

**Red flags**
- Edison could not verify the Nb ranges of C96200 and C96400. My recollection (ASTM B369): C96200 has 0.50-1.0 Nb and C96400 has 0.50-1.5. So 0.8/1.0 sit inside the commercial ranges.
- Edison's "about 1.6 wt% Nb soluble in Cu near 1,090 °C" looks too high to me; I recall about 0.1-0.2 at%.
- Nb stays dissolved in the melt only with Ni present. Low-Ni charges risk undissolved Nb, so use a Ni-Nb master alloy.
- The patent's cavitation value of "19 mm/h" for wrought 70-30 is physically implausible (probably mg/h or mm³/h, an OCR error). Do not quote it.
- There is no seawater evidence. Nb's value is weldability, which is directly relevant to crack-free DED.

**Recommendation:** Keep INCLUDE for Cu-Ni only, with floor 0.5 and conservative 1.0 (C96200 max). Allow non-conservative 1.5 (C96400 max, if confirmed) only at Ni ≈ 28-32, with Nb ≥ 2·Si.

## Be

**VERDICT:** `VERDICT | Be | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.10 | evidence=thin`

**Key facts**
- 0.10 wt% Be was proposed as a C95800 impurity maximum (Allen 2000, Cast Metal Coalition closeout report, 10.2172/765235).
  - That program added Pb, Bi, Zn, Sn, Se, Cr, Si and Be as impurities, which reduced ductility.
  - Only Pb and Bi caused weld HAZ cracks.
- Marine atmosphere on Hainan (Cl⁻ 48.5 mg/m²/day), QBe2 (1.98 Be) over 12 months (Kong 2018, Appl. Surf. Sci. 455:543, 10.1016/j.apsusc.2018.06.029):
  - Mass loss was 15.5 versus 42.2 g/m²/y for Cu.
  - Deepest pits were 14 versus 19 µm.
  - In 3.5% NaCl the icorr difference was only about 2% (4.63 versus 4.73 µA/cm²).
- Commercial grades: C17200 has 1.8-2.0 Be; C17510 has 0.2-0.6 (0.2-0.7 in Edison's source); C17410 has 0.15-0.50 Be with 0.35-0.60 Co. All are age-hardened.
- OSHA Be limits: PEL 0.2 µg/m³ (8-h TWA) and STEL 2.0 µg/m³.
- Cu-Be and Cu-Ni-Be are assessed (Liu 2003, J. Electron. Mater. 32:1265, 10.1007/s11664-003-0021-6). TCCU7 includes Cu-Ni-Be but not Cu-Al-Be.

**Interactions:** Be forms beryllides with Ni and Co; oxygen consumes Be as BeO. For cracking, Pb and Bi matter more than Be.

**DOI check:** Allen DOI OK (OSTI 2000); Kong DOI OK; Liu DOI OK.

**Red flags**
- 0.10 is a limit proposed in one report, not a spec.
- It also coincides with the scope threshold of the OSHA beryllium standard, 29 CFR 1910.1024 (my knowledge). Materials below 0.1 wt% Be are exempt only with objective data showing exposure below the 0.1 µg/m³ action level. A lab cap at exactly 0.10 sits on that regulatory edge.
- There is no evidence that Be helps in immersed seawater.

**Recommendation:** Keep LIMIT, which is in effect EXCLUDE: no intentional Be, and impurity_max tightened to ≤0.01 wt%. That is trivially met with OFHC Cu and pure-metal charges.

## Co

**VERDICT:** `VERDICT | Co | decision=INCLUDE | family=both | conservative_max_wt=1.0 | nonconservative_max_wt=2.0 | floor_wt=0.5 | impurity_max_wt=NA | evidence=thin`

**Key facts**
- C70350 (CuNi1Co1Si) has 1.0-2.0 Co, 1.0-2.0 Ni and 0.5-1.0 Si, strengthened by δ-(Ni,Co)2Si. It is an aged connector strip (Kuhn 2007, Mat.-wiss. Werkstofftech. 38:624, 10.1002/mawe.200700152).
- Cu-2.3Ni-0.7Co-0.7Si after cold work plus 450 °C/4 h reached 258 HV. Precipitation contributed 90 HV versus 66 HV without Co. This is not as-deposited data (Pan 2021, Mater. Des. 209:109929, 10.1016/j.matdes.2021.109929).
- CuAl14Fe4Mn2Co (1.0 Co, 13.8 Al, no Ni) in 3.5% NaCl: 58.2 µA/cm² and 26.6 mpy, versus 14.3 µA/cm² and 6.5 mpy for a Co-free NAB with 5 Ni (Atapek 2017, AFE 17:7, 10.1515/afe-2017-0122). Al and Ni differ too, so the comparison is confounded.
- Cu-Co: Co solubility in Cu peaks at about 8 at% (about 7.5 wt%) at the 1,385 K peritectic. Mixing enthalpy is positive (Nikolaenko & Turchanin 1997, 10.1007/s11663-997-0068-5).
- 0.8-1.4 Co accelerated dezincification of β-brass (Davies 1993).

**Interactions:** Ni+Co totalled 3.0 in the Pan series, with (Ni+Co):Si about 2:1 atomic. Co joins κ with Al and Fe. TCCU7 assesses Cu-Ni-Co but not Cu-Al-Co.

**DOI check:** Atapek DOI OK; Kuhn DOI OK; Pan DOI OK.

**Red flags**
- Edison says no Co cap is established for C71500. But UNS counts Co with Ni: C71500 is "Ni incl. Co 29.0-33.0" and C95800 is "Ni incl. Co 4.0-5.0" (my recollection). EN Cu-Ni grades cap Co at about 0.1. So Co belongs in a Ni+Co budget, not on an independent axis.
- Co is on both the 2022 and 2025 critical-minerals lists and usually costs more than Ni, so substituting Co for Ni does not serve the low-critical-mineral objective.
- No seawater benefit is shown. The 0.5 floor and 2.0 maximum both come from connector alloys.

**Recommendation:** Low priority. Allow 0-1.0 Co only as a partial Ni substitute within the Ni+Co bound, and drop 2.0 unless a Cu-Ni-Co-Si branch is pursued. Otherwise LIMIT ≤0.1.

---

# Group 3a

## Digest group 3a: Cu, Ti, Zr, Mg, Ag, V, B, Sb

Source files: `edison-trajectories/cu-ded-elements-2026-10/phase1/el-{01-Cu,13-Ti,14-Zr,16-Mg,17-Ag,18-V,19-B,21-Sb}.md`. All compositions are in wt%. All 26 DOIs below were checked against Crossref; the Ag and Ti papers were also checked against their OpenAlex abstracts. "My judgment" or "my recollection" marks the reviewer's own knowledge, which still needs checking against the standard or source.

## Cu

`VERDICT | Cu | decision=LIMIT | family=both | conservative_min_wt=65 | nonconservative_min_wt=60 | floor_wt=NA | impurity_max_wt=NA | evidence=moderate`

**Key facts**
- Reference alloys:
  - C71500 (Ni 29–33, Fe 0.40–0.70): about 69.5 Cu and 30.5 solute. C70600: about 88.5 Cu. Source: Lewis & LaQue 1981, ANL/OTEC-BCM-019, DOI 10.2172/6255887.
  - C95800: Cu ≥79.0, Al 8.5–9.5, Ni 4–5, Fe 3.5–4.5, Mn 0.8–1.5. C95820: Cu ≥77.5. These are ASTM B148 limits copied from a thesis (Sochu 2020, no DOI).
- The C715 liquidus is about 1,240 °C, only about 60 °C below the 1,300 °C ceiling (McCright 1988, DOI 10.2172/60703).
- Corrosion-film resistance is 5.5, 23.5 and 82.5 ×10³ Ω·cm² for Cu, 90-10 and 70-30. So about 89–90 Cu is a practical ceiling for Cu-Ni.
- In cast C95800 (3.5% NaCl), annealing cut β from more than 20% to about 7% and improved corrosion (Jafari 2021, *Corros. Mater. Degrad.* 2:61, DOI 10.3390/cmd2010004). As-deposited parts keep that β risk.

**Interactions:** Two sub-spaces with different solute budgets:
- Cu-Ni: 65–89 Cu, up to 35 solute.
- NAB: 79–82 Cu (≥77.5), 18–22.5 solute, with Ni ≥ Fe.

**DOI check:** DOI OK for all four checked: 10.2172/6255887 (an OSTI report; Edison's reference list wrongly calls it "ArXiv"), 10.3390/cmd2010004, 10.3390/jmmp8020054 and 10.2172/60703.

**Red flags**
- `decision=LIMIT` does not fit a balance element. This is harmless.
- The liquidus works against the 65/60 bounds (my judgment). The Cu-Ni liquidus is about 1,260 °C at 35 Ni and 1,280 °C at 40 Ni. With Ni-dominated solute, 65 and 60 Cu cannot be atomized, and even C71500 is marginal.
- The C71500 Fe range comes from a 1981 table. My recollection is that current ASTM B111 gives Fe 0.40–1.0.
- C95700 (Cu ≥71, my recollection) was not verified.

**Recommendation:** Keep 65 as a mass-balance guard, but make the calculated and DSC-measured liquidus (≤~1,200–1,250 °C) the binding constraint. Allow 60 only for Mn/Al-rich chemistries. Set sub-space floors at NAB ≥77.5–79 and Mn-Al bronze ≥71.

## Ti

`VERDICT | Ti | decision=INCLUDE | family=both | conservative_max_wt=0.10 | nonconservative_max_wt=0.50 | floor_wt=0.012 | impurity_max_wt=NA | evidence=thin`

**Key facts**
- Specifications: AWS A5.7 ERCuNi (C71580) and MIL-E-21562E(SH) EN67/RN67 carry Ti 0.20–0.50; AWS A5.6 ECuNi weld metal allows ≤0.50. Ti is a deoxidizer that controls porosity. "Excess Ti/Fe/Si promotes cracking", with no numeric threshold (Devletian 2006, FCAW CuNi report, no DOI).
- Cast C95500 NAB with 0.012 (120 ppm) Ti had finer grains, but no significant corrosion change in 3.5% NaCl (0.021 vs 0.023 mm/y; Rivero 2021, *Mater. Res.* 24, DOI 10.1590/1980-5373-mr-2020-0335).
- WAAM NAB with Ti nanoparticles between layers (nominal 0, 0.03, 0.05, 0.10 Ti): i_corr 10.06, 10.88, 10.00 and 8.49 µA/cm². At 0.03 Ti the grains coarsened to 75 µm (Zhang 2026, *Adv. Mater. Joining* 1:17, DOI 10.1007/s44500-026-00016-x).

**Interactions:** In Cu-Ni welds, Ti, Si and Fe must be judged together. O and N consume Ti, graphite contact forms TiC, and Ni-Ti intermetallics can form. No numeric ratio was found.

**DOI check:** DOI OK for Rivero; its abstract confirms 120 ppm Ti and no significant corrosion effect. DOI OK for Zhang; its abstract confirms −15.6% i_corr, +4.34 mV and the non-monotonic grain size. DOI OK for Jin 2018 (Cu-Ni-Ti).

**Red flags**
- The VERDICT mixes the two families. Edison's own table gives Cu-Ni a floor of 0.20 and conservative and non-conservative maxima of 0.50, all backed by the spec.
- The floor of 0.012 is a cast-NAB grain-size effect with no corrosion benefit. It hides the worse result at 0.03 Ti.
- Zhang's Ti contents are nominal nanoparticle additions. It is a single study with 0 citations.
- Edison may have missed a precedent (my recollection, verify against ASTM B369): cast Cu-Ni C96700 contains Ti 0.15–0.35.
- Molten Cu would dissolve a Ti-alloy sonotrode (Cu-Ti eutectics are near 875–885 °C) and contaminate a Ti series (my judgment).

**Recommendation:** Keep INCLUDE but give each family its own bounds:
- Cu-Ni: floor 0.20, conservative 0.50, non-conservative 0.50.
- NAB: floor 0.05, conservative 0.10, non-conservative 0.50 (exploratory only).

## Zr

`VERDICT | Zr | decision=INCLUDE | family=both | conservative_max_wt=0.15 | nonconservative_max_wt=0.50 | floor_wt=0.010 | impurity_max_wt=NA | evidence=thin`

**Key facts**
- In cast brasses and silicon bronzes, grain refinement starts at about 0.010 Zr. About 50% of the Zr is lost on melting or after a 1 h hold, mainly to oxidation. Earlier work used 0.030 Zr + 0.020 B for iron-free aluminum bronze (Sadayappan 2005, CANMET/DOE report, DOI 10.2172/840819).
- Equilibrium Zr solubility in Cu is about 0.11–0.24 at 940–980 °C. The Cu-rich eutectic is at about 966–980 °C, with Cu5Zr and Zr14Cu51 phases (MSIT Landolt–Börnstein Cr-Cu-Zr, 2007).
- Cu-0.82Cr-0.48Zr printed by LPBF reached 99.8% density with remelting (Xu 2024, *Materials* 17:624, DOI 10.3390/ma17030624).
- Cu-15Ni-8Sn with 0.5 Zr reached 980 MPa after aging, with Ni5Zr and Ni4SnZr forming (Yang 2023 review, *Materials* 16:5913, DOI 10.3390/ma16175913).
- There are no Zr-controlled seawater or NaCl data.

**Interactions:** O sets how much Zr is retained, and S poisons refinement. Zr pairs with B in iron-free aluminum bronze, but is probably redundant with Fe in NAB. With Ni, Zr forms Ni-Zr phases. Zr pickup from a ZrO2 crucible was not quantified.

**DOI check:** DOI OK for 10.2172/840819 (2005 report), 10.3390/ma17030624 (CuCrZr LPBF remelting) and 10.3390/ma16175913 (Cu-15Ni-8Sn review).

**Red flags**
- The non-conservative 0.50 is 2–4× the equilibrium solubility. Without aging, excess Zr sits as Cu-Zr eutectic (about 970 °C) or Ni-Zr phases at grain boundaries. That is a liquation-crack and micro-galvanic risk in reheated DED layers (my judgment).
- All three precedents for 0.5 are non-marine, and none is multi-layer DED: an aged Cu-Ni-Sn alloy, NARloy-Z and single-alloy LPBF.
- The floor comes from brass castings.
- Edison may have missed precedents (my recollection, verify): C96700 (Zr 0.15–0.35) and possibly the Def Stan 02-824 Cu-Ni-Cr casting alloy (IN-768, about 0.1 Zr).

**Recommendation:** Keep INCLUDE with a floor of 0.01 and a conservative maximum of 0.15. Lower the non-conservative maximum to about 0.25–0.35 unless DED crack tests pass at 0.5. Always analyze retained Zr, not the charged amount.

## Mg

`VERDICT | Mg | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.01 | evidence=thin`

**Key facts**
- A DOE/CDA review says Mg is added at the end of the melt in Cu-Ni as a deoxidizer and grain refiner, leaves only a trace residual and has no service effect. The same review calls Mg "detrimental" in aluminum bronze because of ductility and hot behavior. It gives no number (Van Konynenburg 1990, DOI 10.2172/137782).
- The 0.01 limit is anchored to one value: a cast NAB substrate reported as "<0.01 Mg" in a WAAM study (Ding 2016, *Materials* 9:652, DOI 10.3390/ma9080652).
- There are no Mg-controlled seawater, NaCl, weld or DED data.
- Cu-Mg is thermodynamically assessed, with fcc, Cu2Mg (Laves) and CuMg2 phases (Bocklund 2024, *Zentropy* chapter, DOI 10.1201/9781003514466-19).

**Interactions**
- Mg with O and Al gives oxide inclusions and lowers hot ductility in NAB.
- Mg can react with the crucible.
- No ratios were found.

**DOI check:** DOI OK for 10.2172/137782 (1990 report), 10.3390/ma9080652 and 10.1201/9781003514466-19 (2024 book chapter).

**Red flags**
- The limit rests on a single substrate assay. "<0.01" is a reporting level, not a tolerance.
- Edison did not quantify the obvious process problem (my judgment). Mg boils at about 1,090 °C, below the 1,200–1,300 °C melt. It will evaporate, and it can reduce Al2O3 (forming spinel) and possibly ZrO2. Both points support LIMIT.
- Edison may have missed a specification (my recollection, verify): EN 1982 cast aluminum bronzes such as CuAl10Fe5Ni5-C (CC333G) list Mg ≤0.05.

**Recommendation:** Keep LIMIT with 0.01 as the target. Accept up to about 0.05 if Mg is used as a deoxidizer and the EN 1982 limit checks out.

## Ag

`VERDICT | Ag | decision=INCLUDE | family=Al-bronze | conservative_max_wt=0.25 | nonconservative_max_wt=1.0 | floor_wt=0.25 | impurity_max_wt=NA | evidence=thin`

**Key facts**
- The only corrosion evidence is Ag nanoparticles (0.25 Ag per the review) in a Cu-Al-Ni shape-memory alloy tested in NaCl. Primary paper: Saud et al., *Mater. Corros.* 66:527, DOI 10.1002/maco.201407658. Edison read it only through a secondary review (Dawood 2020, *Iraqi J. Mech. Mater. Eng.* 20:362, DOI 10.32852/iqjfmme.v20i4.530).
- Cu-Ag is a simple eutectic (779 °C, 72 Ag) with no intermetallic, so Ag lowers the liquidus. In Ag-Cu-Ni, Ni is excluded from the Ag-rich phase (Luo & Chen 1996, *J. Mater. Sci.* 31:5059, DOI 10.1007/BF00355906).
- In non-marine LPBF Cu with 10–30 Ag, porosity fell as Ag rose (Robinson 2021, *J. Alloys Compd.* 857:157561, DOI 10.1016/j.jallcom.2020.157561).
- Silver cost about $1,324/kg in September 2025, about $3.3 per kg of alloy at 0.25 Ag.

**Interactions:** Ag separates from Ni in the Cu-Ni branch. Ag-rich liquid is left at grain boundaries during solidification. Ag-rich phases are noble.

**DOI check:** DOI OK for Saud (Crossref dates it 2014 online; volume 66 is 2015), Dawood, Robinson and Luo.

**Red flags (major)**
- INCLUDE rests on one paper, read through one low-tier review.
- That paper studied a β-phase shape-memory alloy, not α+κ NAB, and added Ag as nanoparticles rather than alloying it.
- Edison reversed the direction of the E_corr result. The Saud abstract says the Ag-bearing alloy, at −277.1 mV_SCE, was nobler than the Ag-free alloy, and that i_corr fell from 6.93 to 5.61 µA/cm² (about −19%). Edison reports a shift from −277.1 to −307.4 mV (more negative) and says no Ag-free current was available.
- The floor equals the conservative maximum (0.25), so the conservative range is a single point.
- Ag works against the critical-mineral and cost goals.
- Specifications count Ag together with Cu ("Cu incl. Ag", my recollection), so Ag needs no impurity limit.

**Recommendation:** Downgrade to LIMIT, i.e. a residual counted with Cu and not a designed search dimension. At most, run one 0 vs 0.25 Ag pair as an Al-bronze side test, and drop the 1.0 ceiling.

## V

`VERDICT | V | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- Equilibrium V solubility in Cu is 0.17 at%, about 0.136 wt%, at 1,085 °C. Melt-spinning retained 0.40–0.80 V; the excess formed particles (Bell & Davies 1997, *MSE A* 226–228:1039, DOI 10.1016/S0921-5093(96)10854-6).
- Cu-V shows liquid immiscibility or a monotectic. The high-V liquidus is about 1,600 °C (Verhoeven & Finnemore 1989, OSTI report, DOI 10.2172/6616372). The binary is assessed by Hämäläinen 1990 (*CALPHAD* 14:125, DOI 10.1016/0364-5916(90)90014-Q).
- No Cu-Ni, NAB or AWS specification contains V.
- Grain refinement is negligible: Cu with 0.10 V had 640 µm grains vs 650 µm without (Cziegler 2015 thesis, no DOI).
- TCCU5 reportedly lacks V.
- There are no seawater data.

**Interactions:** V with O and C forms particles. None was quantified.

**DOI check:** DOI OK for Bell & Davies, Hämäläinen and Verhoeven (report).

**Red flags:** None serious; the decision is well founded.
- Check the claim that TCCU lacks V against the installed database's element list.
- With `impurity_max=NA`, contamination goes unmonitored. If the sonotrode is a Ti-6Al-4V alloy, it is a plausible V source (my judgment).

**Recommendation:** Keep EXCLUDE. Add a provisional reporting limit of about ≤0.01–0.05 V, below the 0.14 solubility, for process control.

## B

`VERDICT | B | decision=INCLUDE | family=both | conservative_max_wt=0.020 | nonconservative_max_wt=0.050 | floor_wt=0.002 | impurity_max_wt=NA | evidence=thin`

**Key facts** (all non-marine)
- In brass castings, 0.0024–0.0036 retained B (with about 0.01 Fe) refined the grains, and the effect was lost at 0.0004. Above about 0.02 B the grains coarsened, Fe-B hard spots appeared above about 0.05 Fe, and only about 50% of the B was recovered (Sadayappan 2005, DOI 10.2172/840819).
- Cu-12.5Al-5Mn with 0.05–0.19 B gave about 80% grain-size reduction, but only after thermomechanical processing (Sampath & Mallik 2009, ESOMAT, DOI 10.1051/esomat/200905028).
- In ZCuPb20Sn5 bronze, 0.10 B was optimal and formed Ni4B3; 0.2 B gave coarse borides and porosity (Ren 2021, *Materials* 14:7806, DOI 10.3390/ma14247806).
- B solubility in Cu is about 0.05–0.08 near the 1,013 °C eutectic and under 1 ppm at room temperature. Dilute B lowers the liquidus (Miettinen, *Arch. Metall. Mater.* 66:297, DOI 10.24425/amm.2021.134787).

**Interactions:** B forms Fe2B with Fe (relevant to NAB), borides with Ni, and B4C on graphite contact. It also interacts with P and has been paired with Zr.

**DOI check:** DOI OK for Sampath (2009 proceedings) and Ren. DOI OK for Miettinen; Crossref gives 2020 (online) vs Edison's 2021, which is minor.

**Red flags**
- The VERDICT says `family=both`, but its numbers are the Al-bronze values. Edison's own table limits Cu-Ni to 0.010 conservative and 0.020 non-conservative.
- The only chloride data come from an electroless Ni-6B coating in a non-peer-reviewed preprint, whose electrolyte is reported inconsistently.
- B promotes solidification and liquation cracking in Ni-rich weld metal (my judgment). The Ni-B eutectic melts near 1,090 °C, below the Cu-30Ni solidus of about 1,170 °C, so multi-pass DED of 30 Ni alloys is at risk.
- The non-conservative 0.05 equals the binary solubility, which leaves no margin for segregation.

**Recommendation:** Encode bounds by family:
- Cu-Ni: floor 0.002, conservative about 0.005–0.010, non-conservative 0.020.
- Al-bronze: floor 0.002, conservative 0.020, non-conservative 0.050.

If the palette must contain only evidence-backed dimensions, use LIMIT ≤0.01 instead.

## Sb

`VERDICT | Sb | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.02 | evidence=thin`

**Key facts**
- Sb inhibits dezincification in α-brass. Tests at 0, 0.10 and 0.20 Sb in 5% CuCl2 (not seawater) showed no extra benefit above 0.10, and Sb does not work in β brass. Source: Davies 1993, CDA report 7013-0009, summarizing Lombardi 1953–54, no DOI.
- In cast tin bronze, 0.18 Sb severely reduces ductility through Sn-rich δ phase (Riley & Makar 1986, *Conserv. Recycl.* 9:315, DOI 10.1016/0361-3658(86)90066-4).
- Sb is "detrimental" in Cu-Ni and aluminum bronze because it segregates to grain boundaries, and is "unacceptable for Cu-Ni welding". No number is given (Van Konynenburg 1990, DOI 10.2172/137782).
- Maximum Sb solubility in α-Cu is 7.8 at% (about 13.9 wt%) at 645 °C, and dilute Sb lowers the liquidus. Sources: Fürtauer & Flandorfer 2012, *Monatsh. Chem.* 143:1275, DOI 10.1007/s00706-012-0737-1; Gierlotka 2009, *J. Alloys Compd.* 484:172, DOI 10.1016/j.jallcom.2009.05.056.

**Interactions**
- Sb with Sn: δ phase in any Sn-bearing design.
- Sb with Bi, Pb, S, Te, P and O: a group of impurities that segregate to grain boundaries together. No numeric sum was found.
- Sb with Zn: the brass benefit depends on the α/β balance.

**DOI check:** DOI OK for Riley & Makar, Fürtauer, Gierlotka and Van Konynenburg.

**Red flags**
- The 0.02 limit is Edison's own precautionary choice, not from a specification or a test.
- The Cu-Ni/NAB welding warning rests on a single 1990 DOE background review.
- Edison says 0.02 "sits below" the 0.02–0.10 brass range; it actually equals the lower end.
- My recollection is that ASTM B584 gunmetals allow Sb ≤0.20–0.25. That makes 0.02 about 10× tighter than cast practice: conservative, but reasonable for crack-sensitive multi-layer DED.

**Recommendation:** Keep LIMIT at 0.02 (target ≤0.01), and constrain Sb jointly with Pb, Bi, S and P.

---

# Group 3b

## Group 3b digests: C, Mo, Ga, In, Cd, Y, Ce, Pd

Source files: edison-trajectories/cu-ded-elements-2026-10/phase1/el-*.md. All DOIs listed were checked against Crossref on 2026-10-17. "My judgment" or "my recollection" marks checker knowledge, not Edison's.

## C

`VERDICT | C | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.005 | evidence=thin`

**Key facts**
- Edison calls the 0.005 wt% cap (target 0.002) its own screening limit, "not [SPEC]". It found no C threshold for corrosion, welding or DED.
- C solubility in liquid Cu is about 0.0001 wt% at 1100 °C, a liquid value from a carbon-nanotube paper. No solid-solubility value was found (Deck & Vecchio 2006, *Carbon* 44:267-275, 10.1016/j.carbon.2005.07.023).
- Dissolved C in NAB melts precipitates as flakes beside κII. In thick castings these nucleate H-assisted microporosity, where fatigue cracks start (Wenschot 2014, *Int J Cast Met Res* 27:65-72, 10.1179/1743133613Y.0000000080). Edison lacked the full text, and the abstract (I read it) gives no threshold.
- A secondary review calls C detrimental in Cu, Cu-Ni and Al bronze (Van Konynenburg et al. 1990, LLNL, 10.2172/137782).

**Interactions:** Ni raises C uptake (no ratio given). Ti, Cr and Nb form carbides. C+O gives CO pores, and C+H gives porosity in NAB.

**DOI check:** Van Konynenburg OK. Wenschot OK (online 2013, volume 27 in 2014). Deck & Vecchio OK.

**Red flags:** Edison could not confirm C71500 C <= 0.05. My recollection is that ASTM B111/B466 do set C <= 0.05 for welding grades, and cast C96200/C96400 allow 0.10/0.15. So 0.005 is 10 times tighter than the welding grade, with no data behind it. It may also be unattainable: Ni bought to ASTM B39 (C <= 0.03, my recollection) could put Cu-30Ni at about 0.009 wt% C.

**Recommendation:** Keep LIMIT, with impurity_max = 0.02 wt% (margin under 0.05, which also covers the NAB porosity mechanism). Keep 0.005 only as a target to report against.

## Mo

`VERDICT | Mo | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.02 | evidence=thin`

**Key facts**
- Cu and Mo are nearly immiscible. The calculated eutectic is at 1084.2 °C, with 0.119 wt% Mo in the liquid and about 0.023 wt% in solid Cu (Wang et al. 2000, *J Phase Equilib* 21:54-62, 10.1361/105497100770340426). The cap is set from this value.
- Ni raises Mo solid solubility: about 1.0 wt% at 10 Ni, 1.5-2.0 at 20-30 Ni and 3.0-3.5 at 40 Ni, at 900-1100 °C (Kozlova et al. 1973, *Sov Powder Metall Met Ceram* 12:140-144, 10.1007/BF00807778).
- The only NaCl data come from Cu-Ni with about 3.1 wt% Mo plus 0.35 B. Polarization resistance in 3 wt% NaCl fell 55-57%, with the Mo and B effects confounded (Hou et al. 2021, *Met Mater Int* 27:4911-4921, 10.1007/s12540-020-00801-x).
- In cast NAB, 2-3 wt% Mo raised UTS from 434 to about 460 MPa, with no corrosion test (Anene 2019, 10.30544/423).

**Interactions:** Mo tolerance scales with Ni, and NiMo forms when both are high. Fe draws Mo into Fe-Mo phases.

**DOI check:** Wang, Kozlova, Hou (online 2020, volume 27 in 2021) and Anene are all OK.

**Red flags:** The cap uses binary Cu-Mo data, although Edison's own Kozlova numbers give 1.5-2 wt% solubility at 20-30 Ni. In my judgment that makes it very strict for Cu-Ni. The real Mo source is a Mo/TZM sonotrode eroded by a Ni-bearing melt. Minor: Edison gives C71500 Fe as 0.40-0.70; ASTM gives 0.40-1.0 (my recollection).

**Recommendation:** Keep LIMIT, but split it: <= 0.02 wt% for Al bronze and low-Ni alloys, <= 0.1 wt% for Cu-Ni with at least 10 Ni. Use Mo assays to track sonotrode wear.

## Ga

`VERDICT | Ga | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- No specification includes Ga, and there are no seawater or NaCl data for Ga-bearing Cu alloys.
- Single-phase Cu-20 wt% Ga powder exists. Liquid Ga reacts with Cu at 160-300 °C to form brittle CuGa2 and Cu9Ga4. This is microelectronics work, not DED (Liu et al. 2018, *Materials* 11:1384, 10.3390/ma11081384).
- In tests with pure liquid Ga, alumina held up to at least 1000 °C and ZrO2 to about 800 °C, while Mo was attacked at 600-800 °C (Wilkinson 1953, ANL-5027, 10.2172/4407475). These results do not cover dilute Cu-Ga.
- China produced 98% of the world's Ga in 2024 (USGS SIR 2025-5021). The price is about US$500-580/kg, from a secondary source.

**Interactions:** Ga:Ni (Ni3Ga) and Ga+Al are flagged, with no numbers.

**DOI check:** Liu OK, Wilkinson OK, and Li 2008 Cu-Ga CALPHAD (10.1016/j.calphad.2008.03.006) OK.

**Red flags:** An NA cap cannot be used downstream. Edison gives no Cu-Ga solubility. My recollection is about 20 at% (21-22 wt%) at about 620 °C, and Ga lowers the liquidus, so the liquidus is no constraint. My estimate is that the only realistic source is primary Al (about 0.01 wt% Ga), which would add at most about 0.002 wt%.

**Recommendation:** Treat Ga as excluded from the design space. Enter impurity_max = 0.01 wt% as a report-only placeholder instead of NA.

## In

`VERDICT | In | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.01 | evidence=thin`

**Key facts**
- The calculated Cu-In peritectic is at 705 °C, with fcc Cu holding 15.8 wt% In (Liu et al. 2002, *J Phase Equilib* 23:409-415, 10.1361/105497102770331352).
- The partition coefficient is about 0.48 and the liquidus slope is -6.12 °C per wt% In, so In concentrates in the last liquid (Cziegler 2015 thesis, no DOI).
- At 0.107 wt% bulk In, In covered 16-25% of the surface at 460-580 °C (Madito 2012 thesis, no DOI).
- There are no seawater data and no specification. Edison says itself that 0.01 is a procurement rule, not a tolerance.
- Workers exposed to 78.4 µg/m³ of airborne In showed lung-injury biomarkers (Liu et al. 2022, *Part Fibre Toxicol* 19:69, 10.1186/s12989-022-00510-w).

**Interactions:** None quantified. Trace In can come in with Zn or Sn feedstock.

**DOI check:** Liu 2002 OK, Dev 1996 (*Mater Des* 17:75-78) OK, Liu 2022 OK.

**Red flags:**
- The key segregation numbers come from two theses without DOIs.
- The claim that TCCU lacks In comes from proceedings without a DOI, so check the installed database.
- The ACGIH TLV of 0.0001 mg/m³ is quoted from a single paper. My recollection is that the NIOSH REL is 0.1 mg/m³ and OSHA has no PEL.

**Recommendation:** Keep LIMIT at <= 0.01 wt%. It is harmless, since In is not a normal contaminant of Cu or Ni.

## Cd

`VERDICT | Cd | decision=LIMIT | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.01 | evidence=thin`

**Key facts**
- The cap equals the RoHS homogeneous-material limit of 0.01 wt%, a regulatory value, not a metallurgical one (Miehe et al. 2015, *IJPEM-GT* 2:289-298, 10.1007/s40684-015-0035-6).
- Cd boils at about 767 °C, so it evaporates from the melt as toxic fume (CDA, *High Conductivity Coppers*). A welding review says Cd "usually causes no ill effects" only because it evaporates (Czajkowski & Butters 2001, BNL, 10.2172/791763).
- The OSHA PEL is 5 µg/m³ as an 8-h TWA, with an action level of 2.5 µg/m³.
- The only copper use is conductor alloy C16200 with 0.7-1.2 wt% Cd. Edison could not verify this range; it matches my recollection.
- A Cu-Cd assessment exists, but Edison extracted no solubility (Chen et al. 2010, *TNMSC* 20:649-654, 10.1016/S1003-6326(09)60193-X).

**Interactions:** None.

**DOI check:** Czajkowski OK and Chen OK. 10.1108/acmm.1999.12846cab.036 is a DOI MISMATCH (partial). It resolves to a short 1999 item titled "Copper Development Association" in *Anti-Corrosion Methods and Materials* vol. 46, not to the CDA publication Edison read.

**Red flags:** None affecting the decision. Fix the CDA citation by citing the CDA publication itself, without a DOI. Edison left the 2022 critical-mineral status open; my recollection is that Cd was not on the 2022 list.

**Recommendation:** Keep LIMIT at <= 0.01 wt%.

## Y

`VERDICT | Y | decision=INCLUDE | family=Cu-Ni | conservative_max_wt=0.021 | nonconservative_max_wt=0.05 | floor_wt=0.021 | impurity_max_wt=NA | evidence=thin`

**Key facts**
- The only basis is as-cast 90Cu-10Ni with 0.021 wt% Y. After 30 days in 3.5 wt% NaCl, inner-film resistance was above 1,500 kΩ (no area units given) (Zhang et al. 2020, *Int J Electrochem Sci* 15:4161-4178, 10.20964/2020.05.47).
  - Resistance rose and then fell as Y increased, while Y-rich oxysulfide inclusions grew in number and size.
  - Edison read only page 1, which is the abstract (I checked). The other Y levels and the baseline values are unknown.
- In Mg-Cu-Y at 400 °C, Cu6Y and Cu4Y form, and no Y solubility in fcc Cu was detected (Mezbahul-Islam & Medraj 2013, *Sci Rep* 3:3033, 10.1038/srep03033).
- There are no specification, DED, welding or NAB data.

**Interactions:** Y consumes O and S, so how much Y is retained depends on the O and S in the melt. No Y:Ni ratio is given.

**DOI check:** Zhang OK and Mezbahul-Islam OK. Li 2006 (*JMEP*) is OK, but it covers Ce or unspecified rare earths, not Y.

**Red flags:**
- The INCLUDE rests on one abstract: a cast alloy, tested in NaCl rather than seawater, with no comparison against C71500.
- The floor equals the conservative maximum (zero-width range), and Edison itself calls 0.05 unsupported.
- My judgment: Y binds O and S more strongly than Al does. It will be lost unevenly to oxide during melting (possibly reacting with alumina; YSZ crucibles can also add Y), atomization and laser remelting. Holding about 0.02 wt% retained Y is unrealistic.
- The decision is inconsistent with Ce, which got LIMIT despite more direct Cu-Ni evidence.

**Recommendation:** Downgrade to LIMIT at <= 0.05 wt%, not a stand-alone design dimension. Allow Y only as an option in one shared Cu-Ni rare-earth slot (see Ce), ranked below Ce and La.

## Ce

`VERDICT | Ce | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.04 | evidence=thin`

**Key facts**
- The 0.04 cap comes from brass, where a 0.5 wt% mischmetal charge left 0.04 wt% total rare earths. That is a retention figure, not a Ce tolerance (Davies 1993, CDA report, no DOI).
- In 3.5% NaCl, Cu-14Al-X with pooled trace additions corroded at 0.0264 g/m²·h, against 0.0260 for QAl9-4. The Ce effect was not isolated (Li et al. 2006, *JMEP* 15:102-110, 10.1361/105994906X83466).
- Edison could not read three direct Cu-Ni papers: Mao 2009 (*J Rare Earths* 27:1037-1041; Cu-30Ni in seawater), Lin 2009 (*J Rare Earths* 27:259-263; flowing seawater) and Du 2025 (*JMRT* 36:8062-8074). I retrieved the Du abstract from OpenAlex.
  - B10 with 0.1% Ce and B10 with 0.1% La both resisted 3.5 wt% NaCl better than Cu-10Ni, with La better than Ce.
  - The authors attribute this to rare-earth oxides helping the passive film form.

**Interactions:** Ce consumes O and S. Al-Ce-Cu phases such as Al8CeCu4 can form.

**DOI check:** Mao OK, Du OK and Lin OK. Moore 2020 Al-Ce-Cu CALPHAD (10.1007/s11669-020-00852-y) OK.

**Red flags:** The 0.04 cap sits below the 0.1 wt% Ce that Du found beneficial (probably nominal, with retention unknown). The cap is extrapolated from mischmetal in brass, and the decision is inconsistent with Y.

**Recommendation:** Change to INCLUDE for Cu-Ni as an exploratory element: floor 0.02, conservative 0.05, non-conservative 0.1 wt% retained, as one rare-earth slot shared with La and Y. At minimum, raise the cap to 0.1. Read the Mao, Lin and Du full texts first.

## Pd

`VERDICT | Pd | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- The only quantitative data come from Ni-balanced weld fillers for 304L stainless. Repassivation potentials in 0.1 M NaCl were 51.1, 64.4 and 110.1 mV vs SCE at 0, 0.24 and 1.3 wt% Pd, so about 1 wt% helped (Liang et al. 2010, *Mater Corros* 61:909-919, 10.1002/maco.200905583).
- A Cu-Sn-1Pd electrodeposit outperformed a Cu-Zn-Sn coating, but the comparison is confounded and the author could not attribute the effect to Pd (Martinuzzi 2023 thesis, no DOI).
- Cu-Pd is fully fcc at high temperature, and ordered Cu3Pd forms at about 12-32 wt% Pd (Li et al. 2008, *Calphad* 32:439-446, 10.1016/j.calphad.2008.04.004).
- Pd is a critical mineral on both the 2022 and 2025 lists.

**Interactions:** None validated.

**DOI check:** Liang OK, Li OK, and Kou 2021 (*Metals* 11:1442) OK.

**Red flags:**
- None serious.
- My judgment: Pd's cathodic-modification benefit, as in Ti Grade 7, needs a passivating metal. In Cu alloys, which are controlled by the surface film and oxygen reduction, noble Pd sites could speed attack.
- At an estimated US$30-50k/kg, 1 wt% Pd adds about US$300-500 per kg of alloy.
- Pd has no plausible contamination route, so the NA cap is fine.

**Recommendation:** Keep EXCLUDE.

---

# Group 4

## Edison phase-1 digests, group 4 (Mn, As, P, Bi, S, O, H, N, Li, Sr, La)

Notes on method. All DOIs listed under "DOI check" were looked up in the Crossref API on 2026-10-17. TCCU7 coverage statements come from the repo file `edison-trajectories/cu-ded-elements-2026-10/tccu7_coverage.md`. "Repo now" refers to the current `search_space.md`. Anything marked "my judgment" is my own metallurgical opinion, not Edison's or a checked source's. All compositions are in wt%.

## Mn

**VERDICT** `VERDICT | Mn | decision=INCLUDE | family=both | conservative_max_wt=1.5 | nonconservative_max_wt=4.4 | floor_wt=0.9 | impurity_max_wt=NA | evidence=moderate`

**Key facts**
- **Binary Cu-Mn in 3.5% NaCl.** After 2 h, with rates calculated from polarization:
  - Cu 92.4, Cu-0.9Mn 30.9, Cu-4.4Mn 25.6 (best), Cu-8.8Mn 73.1 and Cu-13.2Mn 109.9 µm/yr.
  - Low-Ni ternaries did worse: Cu-4.4Mn-4.7Ni 83.2 and Cu-13.3Mn-4.7Ni 132.4 µm/yr. A high-Ni ternary did well: Cu-9Mn-28.8Ni 10.3 µm/yr.
  - Source: Yang 2019, UNSW PhD dissertation, no DOI. **Both the floor (0.9) and the 4.4 bound come from this single test.**
- **Specifications and a wire-arc AM build.** ERCuNiAl filler is specified at 0.6-3.5 Mn and C95800 (ASTM B148) at 0.8-1.5. Wire-arc AM NAB walls built on cast NAB showed no voids or cracks by CT (Kim 2021, *Metals* 11:513, 10.3390/met11030513).
- **Wire-arc AM NAB with 1 Mn.** Cu-9Al-4Fe-4Ni-1Mn was near full density with no interlayer cracks. Yield strength was 388 MPa, tensile strength 685 MPa and elongation 26% (Dharmendra 2019, *Addit. Manuf.* 30:100872, 10.1016/j.addma.2019.100872).
- **Cast NAB with 1.23 Mn.** Mn stays in solid solution in every phase at 1.0-1.8. The corrosion film is Al2O3 plus Cu2O with no Mn oxide, and β′ and α+κIII are attacked first (Ding 2019, *Materials* 12:209, 10.3390/ma12020209).

**Interactions**
- Mn stabilizes β in NAB; the authors equate 1 Mn to about 0.15 Al. Screen Al and Mn together, with Ni above Fe.
- Mn helps keep Fe in solution in Cu-Ni.
- The low-Ni data show that Mn does not replace Ni one for one.
- Mn lowers the liquidus. The Cu-Mn minimum is 871 °C at 33.7 Mn, an average of about -6 °C per wt% by my estimate, so Mn can offset part of Ni's liquidus rise.
- TCCU7 assesses the Cu-Ni-Mn, Cu-Al-Mn and Cu-Fe-Mn ternaries. Edison wrongly says this was "not verified".

**DOI check:** Ding 2019 OK. Dharmendra 2019 OK. Kim 2021 OK.

**Red flags**
- The conservative 1.5 is labeled `family=both` but comes from C95800 alone. It sits below three established compositions:
  - ERCuNiAl at 3.5, from Edison's own Kim source.
  - C71640 at 1.5-2.5, a Cu-Ni grade that Edison says it could not verify.
  - C95700 and ERCuMnNiAl at 11-14.
- The floor and the 4.4 bound rest on one unpublished 2-hour polarization test. Its rates of 25-110 µm/yr cannot be compared with long-term Cu-Ni rates. In that test, adding 4.7 Ni raised the corrosion rate of Cu-4.4Mn from 25.6 to 83.2 µm/yr, which looks like noise (my judgment).
- A 4.4 cap shuts out Mn-Al bronze, the commercial family with only 1.5-3 Ni, which matters for the lower-Ni goal.
  - Excluding it may be right: its selective-phase corrosion is worse than NAB's, and it produces more Mn fume (respirable TLV 0.02 mg/m³) and Mn loss.
  - That choice should be stated rather than buried in a bound.
- Edison gives no measured Mn evaporation loss under the laser.

**Recommendation:** Keep INCLUDE.
- Conservative max: 2.5 for Cu-Ni (C71640) and 3.5 for aluminum bronze (ERCuNiAl).
- Non-conservative max: about 5 for Cu-Ni (MARINEL type). Either allow 14 for Mn-Al bronze or state explicitly why that family is excluded.
- Lower the floor to about 0.3-0.5 and budget for measured Mn loss.
- Repo now: 0-4, conservative 2.5, non-conservative 4.4, floor 0.3. That matches this for Cu-Ni; the Mn-Al bronze exclusion still needs to be stated.

## As

**VERDICT** `VERDICT | As | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.0005 | evidence=thin`

**Key facts**
- **Only proven role is in α-brass.** As stops dezincification there: no effect at 0.014, inhibition at 0.024, least attack at 0.05-0.084. In duplex 60-40 brass, 0.25 As made dezincification more than three times worse (Davies 1993, CDA report, no DOI).
- **Welding.** A report says As is harmless in Cu alloys "unless Ni is present", then lists As among hot-cracking residuals. It gives no threshold (Czajkowski & Butters 2001, BNL Monel 400 report, 10.2172/791763).
- **SCC in aluminum brass.** Resistance fell as As rose from 0 to 0.08 in seawater dosed with Cu2+ and ammonia, but the trend was not monotonic (Beavers 1980, report 10.2172/5047866).
- **Where the limit comes from.** The 5 ppm is the UNS C10100 (oxygen-free electronic copper) maximum, taken via Magnusson 2017 (SKB R-17-20, no DOI). As dissolves in α-Cu up to 6.83 at%, about 7.95 wt%.

**Interactions**
- As × Ni, including Ni picked up by dilution from either repair substrate.
- The benefit needs an α Cu-Zn matrix.
- P does not neutralize As, and As does not offset Pb, Bi or S.
- TCCU7 has only the Cu-As binary, with no Cu-Ni-As ternary.

**DOI check:** Uhland 2001 (*Calphad* 25:109-124, As-Cu-Ni) OK. Shishin & Jak 2018 (*Calphad* 60:134, 10.1016/j.calphad.2017.12.005) OK. Subramanian & Laughlin 1988 (*Bull. Alloy Phase Diagr.* 9:605, 10.1007/BF02881964) OK.

**Red flags**
- 5 ppm is 40 times stricter than the P and Pb reference points (0.02). It is borrowed from unalloyed copper, not from any Cu-Ni, NAB or AWS specification, and Edison concedes it is not a threshold.
- The cracking evidence is one remark with no threshold.
- My judgment: As dissolves widely in Cu and is not a low-melting boundary film like Bi or Pb. Arsenical copper C14200 (0.15-0.5 As) is weldable. Verifying 5 ppm needs ICP-MS or GDMS.
- The C44300 and C68700 ranges of 0.02-0.06 that Edison "could not verify" are the standard UNS values, to my knowledge.

**Recommendation:** Keep LIMIT with no intentional As.
- Use 0.005 (50 ppm) as the limit and 0.02 as the outer limit, matching P and Pb. Keep 5 ppm only as a feedstock aim.
- Repo now: 0.02, with an outer limit of 0.06. That 0.06 is the arsenical-brass *addition* range, not an impurity limit for Ni-bearing alloys, so drop it.

## P

**VERDICT** `VERDICT | P | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.020 | evidence=moderate`

Edison also gives a tighter target of 0.015 for aluminum-bronze compositions.

**Key facts**
- **Composition table.** Welding-grade C70600 ≤0.020, C71581/ERCuNi ≤0.020, C61400 aluminum bronze ≤0.015 (Carlone & Astarita 2019, *Metals* 9:1206, 10.3390/met9111206). Edison says the extracted table columns were "badly disordered".
- **Cu-P binary.** The eutectic is at 714 °C and 8.3-8.4 P, and α-Cu dissolves about 1.75 P at 714 °C. This is not a safe bound for welding (Schlesinger 2002, *Chem. Rev.* 102:4267, 10.1021/cr000039m).
- **Phosphides.** In Ni-bearing Cu, P forms Ni2P, Ni3P or MnNiP; these were aged alloys (Choi & Lee 2007, *MSEA* 458:295, 10.1016/j.msea.2006.12.074).
- **No seawater dose-response.** In an ammonia atmosphere, raising P from 0.014 to 0.056 lowered general corrosion from 38 to 16 mils/yr but cut time to SCC failure from 6,298 to 428 min (Van Konynenburg 1990, 10.2172/137782).

**Interactions**
- P × Ni (phosphides).
- P × Mn × Ni (MnNiP, near 1:1:1 atomic).
- P × Sn (ternary eutectic).
- P × O (deoxidation versus inclusions).
- Older brass guidance keeps P below 0.015.
- In C72700 (Cu-9Ni-6Sn) welds, 0.01 P plus 0.10 Mn helped, but there was no P-only heat (Tumuluru & Nippes 1988).
- TCCU7 assesses Cu-Ni-P but not Cu-Al-P.

**DOI check:** Carlone 2019: title, journal and year match, but Crossref shows a short special-issue editorial (abstract ending "[...]", 20 references). A multi-grade composition table is unlikely in an editorial, so **where the table really comes from is unverified**. Choi 2007 OK. Schlesinger 2002 OK.

**Red flags**
- The source is weak, but the numbers agree with the reference points: C71500 welding grade P ≤0.02, ERCuNi P ≤0.02, and C61400 P ≤0.015 (my knowledge).
- Nothing contradicts the VERDICT.

**Recommendation:** Keep LIMIT at 0.020, with 0.015 as the aluminum-bronze target. Cite AWS A5.7 and ASTM B111 directly instead of the Carlone table. Repo now: 0.02 / 0.02, consistent.

## Bi

**VERDICT** `VERDICT | Bi | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.001 | evidence=moderate`

Edison adds an extra caution of 0.0004 for Sn-rich bronzes.

**Key facts**
- **Commercial hot-rolling limits.** Bi 0.001 in Cu-Ni and nickel silver, 0.002 in 70-30 brass, 0.0004 in phosphor bronze. The same review links Bi to cracking in the heat-affected zone and lists Te 0.003 and Se 0.006 for Cu-Ni (Riley & Makar 1986, *Conserv. Recycl.* 9:315-323, 10.1016/0361-3658(86)90066-4).
- **Grain-boundary embrittlement.** One monolayer of Bi on a Cu grain boundary cuts the work of separation from 3.35 to 0.96 J/m² (Lozovoi 2006, *Phys. Rev. B* 74:155416, 10.1103/PhysRevB.74.155416).
- **Solubility.** About 0.033 at roughly 927 °C (Teppo 1990, *Thermochim. Acta* 173:137), or 0.068 at 975 °C. The Cu-Bi eutectic is near 270 °C, so the last liquid to freeze melts very low.
- **Corrosion.** In cast CAC901 with 0.4 Bi in 3.0% NaCl, Bi particles were nobler than the matrix but gave no benefit to the bulk alloy (Yasuda 2017).

**Interactions**
- Gavin's index (see S): BiE = Bi + 0.7Te + 0.4Pb + 0.2Se + 0.1S, in ppm. Bi therefore has to be limited together with Pb, Se and Te.
- Li is reported as an experimental remedy for Bi embrittlement.
- TCCU7 has the Cu-Bi binary but no Cu-X-Bi ternaries.

**DOI check:** Riley & Makar 1986 OK. Teppo 1990 (10.1016/0040-6031(90)80598-S) OK. Yasuda 2017 (10.2320/matertrans.M2017196) OK. It is *Materials Transactions* 58:1679-1686; Edison's reference list mislabels it as J. Japan Inst. Metals.

**Red flags**
- The 10 ppm figure rests on one secondary review of hot-rolling practice, not of welding or DED.
- Consistency check (my calculation): under BiE, the reference limit Pb ≤0.02 (200 ppm) alone counts as 80 ppm of Bi-equivalent, eight times the Bi limit. Either the Bi limit is conservative or Pb 0.02 is loose for DED.

**Recommendation:** Keep ≤0.001 Bi and add a joint cap on low-melting impurities (a BiE-type sum over Bi, Pb, Se, Te). This probably means holding Pb well below 0.02. Repo now: 0.001, with an outer limit of 0.005 and no source; the 70-30 brass value of 0.002 would be a better-anchored outer limit.

## S

**VERDICT** `VERDICT | S | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.010 | evidence=thin`

Edison sets a procurement aim of 0.005.

**Key facts**
- **Hot ductility of Cu-10Ni (Gavin 1978, *Metals Technol.* 5:397-401, 10.1179/mt.1978.5.1.397).** In a simulated TIG cycle:
  - S on its own was fairly harmless up to 0.075.
  - The ductility trough was 850-1100 K, and impurity effects added up as BiE = Bi + 0.7Te + 0.4Pb + 0.2Se + 0.1S (ppm).
  - A complex Cu-11Ni-8.5Mn-5.6Fe-1.35Al alloy showed stronger interactions.
  - The commercial-purity heat contained 0.0051 S.
- **Cu-S binary (Sineva 2010, *Russ. Metall.* 2010:448, 10.1134/S0036029510050162).** Solid solubility is about 0.0001 at 600 °C and 0.007 at 1000 °C. The Cu-Cu2S eutectic is at 1067 °C and 0.77 S; that is a liquid composition, not a solubility.
- **Reference values.** C10100 S ≤0.0015; Monel 400 (MIL-N-24106) S ≤0.015.
- **Sulfide in the water, not the alloy.** C71500 corroded at 0.15 mm/yr, falling to 0.09 after 168 h (Gao & Liu 2022, *Materials* 15:8513, 10.3390/ma15238513).

**Interactions**
- The BiE sum (see Bi).
- S destroys Zr grain refinement in tin bronzes, and Mg restores it (Sadayappan 2005, 10.2172/840819).
- Edison gives no Mn:S ratio. My judgment: Mn ≤1 plus Ti 0.2-0.5 in ERCuNi-type chemistry (Ti cited in Edison's Beaver 1978) ties up S.
- TCCU7 assesses Cu-Ni-S, Cu-Fe-S and Cu-Mn-S, but not Cu-Al-S.

**DOI check:** Gavin 1978 OK. Sineva 2010 OK (Crossref dates it May 2010 and Edison September; trivial). Gao & Liu 2022 OK.

**Red flags**
- None serious. 0.010 equals the ERCuNi limit and is tighter than the C71500 welding grade (0.02).
- Edison anchors the limit to impurity levels measured in one study rather than citing AWS A5.7.
- Gavin's 0.075 tolerance applies only to simple Cu-10Ni.

**Recommendation:** Keep ≤0.010 (aim ≤0.005), cite AWS A5.7 ERCuNi as the anchor, and carry the BiE sum forward. Repo now: 0.01 / 0.02, consistent.

## O

**VERDICT** `VERDICT | O | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.013 | evidence=moderate`

Edison prefers ≤0.005 where practical.

**Key facts**
- **The basis of the limit.** Ultrasonically atomized CuAl10Fe5Ni5 powder contained 0.013 O (Uhlmann 2024, *Materials* 17:3396, 10.3390/ma17143396). This single measurement is the whole basis. For comparison:
  - A gas-atomized reference of different chemistry had 0.019.
  - Ground chips had 0.073 and milled powder 0.119-0.190.
  - The study's carbon-fibre sonotrode contaminated the powder.
- **Electron-beam welds.** Oxygen-free Cu (35 ppm O) was almost pore-free, while tough-pitch Cu (179 ppm O) had 49-112 pores per specimen; H and N were below 10 ppm (Tóth 2021, *Weld. World* 65:2077-2091, 10.1007/s40194-021-01158-4).
- **Counterexample.** Surface-oxidized Cu powder at 0.20 O gave dense laser powder-bed parts, and its absorptivity rose from 32% to 58% (Jadhav 2020, *Mater. Des. Process. Commun.* 2, 10.1002/mdp2.94).
- **Binary.** The Cu-Cu2O eutectic is at 0.39 O and 1065 °C.

**Interactions**
- O × H: Cu2O + H2 forms steam pores.
- O × Al, Ti, Si, Mg, Li, P: deoxidation turns dissolved O into inclusions.
- O × Mn, B: oxide flotation.
- **Correction to Edison:** TCCU7 *does* contain O, with Cu-Al-O, Cu-Fe-O and Cu-Mn-O ternaries but no Cu-Ni-O. Edison said O was available only in TCOX.

**DOI check:** Uhlmann 2024 OK. Tóth 2021 OK. Jadhav OK (published online 2019; volume 2 is dated 2020).

**Red flags**
- 0.013 is the best value measured on one powder, not a threshold. Used as a reject limit, it leaves no margin.
- One number for both families is arbitrary, because aluminum-bronze powder carries an Al2O3 skin.
- My recollection is that commercial Cu-alloy AM powders are certified at a few hundred ppm O. The "preferred" 50 ppm is probably unrealistic for 45-150 µm powder (my judgment).

**Recommendation:** Keep LIMIT. Treat 0.013 as a target, reject above about 0.03, and tighten using measured O against porosity and corrosion. Repo now: 0.02, with an outer limit of 0.05. That is reasonable.

## H

**VERDICT** `VERDICT | H | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.0001 | evidence=thin`

Edison gives a stretch target of 0.00006.

**Key facts**
- **Where the limit comes from.** H <1 ppm (with O <5 ppm) is a materials requirement for electron-beam-welded copper in a nuclear-waste repository canister program (Robitz 1990, report 10.2172/138043). Oxygen-free phosphorus copper for canisters (SKB) is held to H <0.6 ppm.
- **Hydrogen-treated Cu powders (Ledford 2019, *Appl. Sci.* 9:3993, 10.3390/app9193993).**
  - H rose from 1.81 to 31.83 ppm as O fell from 462 to 282 ppm, and from 1.95 to 76.44 ppm as O fell from 1507 to 587 ppm.
  - Low-O powder went only from 0.87 to 1.56 ppm.
  - Steam formed from internal Cu2O fractured particles and ejected melt, yet remelting in electron-beam powder-bed fusion left negligible H.
- **Solubility.** Cu dissolves a few ppm H at 350-450 °C under 60-280 MPa of H2 (Corrigall 2020, *J. Phase Equilib. Diffus.* 41:27-34, 10.1007/s11669-019-00776-2).
- **Modeling.** A Cu-H-O-S-P CALPHAD assessment exists, but H is **not in TCCU7**.

**Interactions**
- O × H (steam) dominates.
- Ni increases gas uptake in Cu-Ni (see N).
- No H:O ratio has been validated.

**DOI check:** Ledford 2019 OK. Corrigall 2020 OK. Magnusson & Frisk 2014 (*Calphad* 47:148-160, 10.1016/j.calphad.2014.09.004) OK.

**Red flags**
- The limit comes from unalloyed canister copper, not marine alloys, and Edison concedes it is not established for C71500 or C95800.
- My judgment: on fine powder, adsorbed moisture reads as several ppm H in inert-gas fusion analysis, and Ni-bearing alloys dissolve more H. So 1 ppm is probably neither reachable nor reliably measurable on as-received powder.
- Edison's own evidence ties the defects to O and H together, not to H alone.

**Recommendation:** Keep LIMIT, but treat H as a measured and reported variable with a provisional ceiling of about 0.0005 (5 ppm) on dried powder. Use porosity, measured by density or CT, as the acceptance test rather than ppm H. Repo now: 0.0005, with an outer limit of 0.001. This matches.

## N

**VERDICT** `VERDICT | N | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.0005 | evidence=thin`

**Key facts**
- **Green-laser (515 nm) welding of oxygen-free Cu (Alter 2023 dissertation; Alter 2020, *J. Laser Appl.* 32:022020, 10.2351/7.0000063).**
  - Under Ar, no N was detected.
  - Under synthetic air, the weld held 22 ppm N and about 10% porosity by section area. Under pure N2, porosity was 0.3-0.4%.
  - In lap welds made in air, Ni foil raised porosity from 12.5% to 20-21%, while Al or Ti foil cut it below 0.3%.
- **Spray forming.** CuSn13.5 spray-formed with N2 held 0.00015-0.0002 total N, mostly as gas in pores. Adding 0.15 Ti formed TiN and cut porosity up to threefold (Müller 2004, *MSEA* 383:78-86, 10.1016/j.msea.2004.02.060).
- **Review.** N is called harmful in aluminum bronzes and Cu-Ni (Van Konynenburg 1990, 10.2172/137782). Liquid Cu dissolves only 0.00005-0.0005 N (literature summary in Alter). N is **not in TCCU7**.

**Interactions**
- N × Ni: more porosity.
- N × Al, Ti: AlN and TiN. Stoichiometry is 3.42 Ti or 1.93 Al per unit N by mass.
- N × O: pores attributed to nitrogen oxides.

**DOI check:** Alter 2020 OK (title: "Influence of hydrogen, oxygen, nitrogen, and water vapor on the formation of pores..."). Müller 2004 OK. Van Konynenburg 1990 OK (OSTI report).

**Red flags**
- 5 ppm is an engineering choice near the detection limit for N in powder. Its only benchmark is a 22 ppm porous specimen whose N included gas in the pores.
- Green-laser keyhole welding does not transfer to 1.07 µm blown-powder DED.
- My judgment: N barely dissolves in solid Cu, so the real risk is air drawn into the powder stream and melt pool. That is a shielding problem more than a powder-chemistry problem.

**Recommendation:** Keep LIMIT with an aim of ≤5 ppm and a reject level of about 0.001-0.002. Control N mainly through argon shielding and gas purity, and check porosity. Repo now: 0.005, with an outer limit of 0.02. The 0.005 limit is above the 22 ppm that went with about 10% porosity in Edison's only direct evidence, so it is loose unless porosity is the acceptance test.

## Li

**VERDICT** `VERDICT | Li | decision=LIMIT | family=both | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=0.005 | evidence=thin`

**Key facts**
- **Deoxidation by a Li charge.** Adding 0.05 Li to a Cu melt left 39 ppm O, against 1,290-2,260 ppm in untreated melts, with conductivity of 54 MS/m. This is the amount charged, not the Li retained (Rzadkosz 2014, *Arch. Foundry Eng.* 14:79-84, 10.2478/afe-2014-0041).
- **Li-Ca deoxidizer.** A dose equal to 0.0045-0.009 Li charged was used, and the authors warn that Li may lower corrosion resistance (Shatagin 2008, *Russ. Metall.* 2008:662-666, 10.1134/S0036029508080041).
- **Volatility.** Cu-17 at% Li (2.19 wt%) loses Li by evaporation above about 300 °C in vacuum, roughly 20 mg/day/cm² at 450 °C (Schorn 1989, *J. Nucl. Mater.* 162-164:924).
- **Solubility.** fcc Cu dissolves up to 18.3 at% Li, about 2.39 wt% (Okamoto 2011, *J. Phase Equilib. Diffus.* 32:172, 10.1007/s11669-010-9840-3). Li is **not in TCCU7**.

**Interactions**
- Forming Li2O takes 0.868 wt Li per 1 wt O, so 0.005 Li can bind only about 58 ppm O.
- Li also scavenges H.
- Li is cited as a remedy for Bi embrittlement (see Bi).

**DOI check:** Rzadkosz 2014 OK. Shatagin 2008 OK. Okamoto 2011 OK.

**Red flags**
- 50 ppm is arbitrary, with no specification and no threshold behind it, as Edison admits. There are no seawater data.
- My judgment: Li is volatile at the melt temperature (it boils at about 1342 °C), and Li2O is roughly as stable as Al2O3 and ZrO2. Expect losses to vapor and to the crucible.
- Normal feedstocks contain no Li, so the limit costs nothing.

**Recommendation:** Keep LIMIT, which in practice means no intentional Li, with 0.005 as a reporting limit. Do not use Li as a deoxidizer in-house without assaying the retained Li. Repo now: excluded. Consistent.

## Sr

**VERDICT** `VERDICT | Sr | decision=EXCLUDE | family=none | conservative_max_wt=NA | nonconservative_max_wt=NA | floor_wt=NA | impurity_max_wt=NA | evidence=thin`

**Key facts**
- **Theory only.** A screen of more than 1,000 compounds ranked SrO as a candidate nucleant by lattice match, but the experiments added no Sr (Cziegler 2015, MSc thesis, Leoben, no DOI).
- **Aluminum bronze.** A microalloying paper mentions Sr but reports no retained Sr and no effect (Nová 2017, *Manuf. Technol.* 17:797-804).
- **Thermodynamic data.** Sr is absent from TCCU5 (Edison) and from TCCU7 (repo file). A Cu-Sr binary assessment exists (Risold 1996, *Calphad* 20:151-160), as does a Zn-Cu-Sr assessment (Wang 2023, *Calphad* 81:102561).
- **Other.** Sr is not on the 2022 or 2025 US critical-minerals lists. Sr found on an ancient seabed bronze came from the environment (Armetta 2021).

**Interactions:** None quantified. Edison suggests tracking Sr alongside O.

**DOI check:** Chakrabarti & Laughlin 1984 (*Bull. Alloy Phase Diagr.* 5:391, 10.1007/BF02872963) OK. Risold 1996 (10.1016/S0364-5916(96)00022-3) OK. Nová 2017 (10.21062/ujep/x.2017/a/1213-2489/mt/17/5/797) OK.

**Red flags**
- None serious. Edison honestly gave no solubility or invariant-reaction numbers because it could not read the phase diagrams.
- My judgment: SrO is more stable than Al2O3 and ZrO2, and Sr boils at about 1380 °C, so Sr would not survive the melt reliably.
- Normal feedstock contains no Sr.

**Recommendation:** Keep EXCLUDE. Record it as "not added; report if detected"; no numeric limit is needed. Repo now: excluded. Consistent.

## La

**VERDICT** `VERDICT | La | decision=INCLUDE | family=both | conservative_max_wt=0.05 | nonconservative_max_wt=0.10 | floor_wt=0.05 | impurity_max_wt=NA | evidence=thin`

Edison frames this as an experimental INCLUDE.

**Key facts**
- **Cast Cu-Ni-Ce-La** with Ni 3.1-40.1 and La 0.26-3.34 (Samoilova 2019, *Mater. Sci. Forum* 946:123-128, 10.4028/www.scientific.net/MSF.946.123).
  - (Ce,La)(Ni,Cu)5 formed at grain boundaries.
  - Cu6La and Cu6Ce appeared once (Ce+La)/Ni exceeded about 0.2 by mass.
  - The alloys were melted at 1450-1500 °C.
- **Cu-15Ni-8Sn.** Raising La from 0 to 0.8 refined the secondary dendrite arm spacing from 28.4 to 10.6 µm (Qi 2023, 10.13264/j.cnki.ysjskx.2023.04.016).
- **Aluminum bronze.** 0.05 La improved corrosion in dilute H2SO4, which is acid, not seawater (Davies 1993, citing Verma 1990). Only 0.04 total rare earth was retained from 0.5 mischmetal charged.
- **Cu-24Pb.** 0.18 La formed Cu6La and La5Pb3 and reduced ductility (Alqadhi 2026 manuscript).
- **Unread paper.** A directly relevant paper was not obtained: Li, Leng & Zhu 2026, *Adv. Eng. Mater.*, on La in 90/10 Cu-Ni (10.1002/adem.202501513).

**Interactions**
- Keep (La+Ce)/Ni at or below about 0.2 by mass to avoid Cu6La.
- La ties up Ni (LaNi5-type phases) and Sn.
- La getters O and S, so track retained La against O and S.
- TCCU7 assesses Cu-Ni-La but not Cu-Al-La.

**DOI check:** Samoilova 2019 OK. Li 2026 *Adv. Eng. Mater.* OK; the paper exists (volume 28). Liu 2024 *Nat. Commun.* 15 (10.1038/s41467-024-45732-y) OK, but it used LaB6 particles in laser powder-bed Cu, not elemental La.

**Red flags**
- The floor equals the conservative max (0.05), so the conservative range is a single point.
- INCLUDE rests on acid tests, cast grain refinement and an unread paper, which sits poorly with `evidence=thin`.
- Edison could not verify La's critical-mineral status. La is individually listed on the 2022 US list (my knowledge).
- My judgment: La2O3 is clearly more stable than Al2O3 and ZrO2, so expect low and variable recovery from the crucible melt. Cu6La at grain boundaries also adds hot-cracking risk.

**Recommendation:** Demote La to one optional rare-earth variable shared with Ce: 0-0.10 retained, floor about 0.02. Drop it unless 10.1002/adem.202501513, or the Du 2025 result cited in the repo, shows a seawater benefit. Repo now: "La or Ce", 0-0.1, floor 0.02, Cu-Ni only. Consistent.
