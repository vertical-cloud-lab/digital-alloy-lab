"""Writes data/literature_values.csv: the curated Thermo-Calc and experimental numbers used in
comparison.csv. Every number was read in the cited source (see data/thermocalc_literature.csv for
the verbatim snippets) or in ORCHID's literature records (data/orchid_invariants_*.csv)."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), 'data', 'literature_values.csv')
ORCH = 'ORCHID literature record (CC BY 4.0), paper doi:'
TC_ALSI12 = ('Thermo-Calc 2022a, TCAL7 (Scheil)', '10.1007/s11665-023-08502-3')
TC_AKW = ('Thermo-Calc 2023b, TCAL6 (equilibrium, room temperature)', '10.3390/ma16144920')
DSC = 'DSC on AlSi10Mg powder (DIN EN 1706), doi:10.48550/arXiv.2507.23422'
CDA63 = 'handbook (CDA physical properties via supplier data sheet https://www.concast.com/c63000.php)'
CDA58 = 'handbook (CDA physical properties via supplier data sheet https://www.concast.com/c95800.php)'
CUNI = 'handbook (supplier data sheet, values match CDA; https://avivametals.com)'
rows = [
 # key, thermocalc_value, thermocalc_db, thermocalc_source_doi, experiment_value, experiment_source, notes
 ('AlSi10Mg|liquidus', '', '', '', 597, DSC, 'No Thermo-Calc liquidus found for standard AlSi10Mg. TCAL7 gives (Al) onset ~590 C for a 0.8Mn die-casting variant Al-10Si-0.35Mg-0.8Mn-0.3Fe (doi:10.1007/s40962-023-01018-5): different alloy, not used'),
 ('AlSi10Mg|solidus', '', '', '', 563, DSC, 'DSC powder composition not given; variation < 2 C between powder fractions'),
 ('AlSi10Mg|eq_range', '', '', '', 34, DSC + ' (597 - 563)', 'a calculated range of ~30 C is quoted for AlSi10Mg in doi:10.3390/ma12071007 (from Tang et al. 2016; software and database not verified), not used'),
 ('AlSi10Mg|eutectic', '', '', '', '', '', 'TCAL7 gives ~570 C (also ~574 C) for the 0.8Mn variant of doi:10.1007/s40962-023-01018-5: different alloy, not used'),
 ('AlSi10Mg (Al-9.92Si-0.291Mg-0.137Fe powder)|mass_FCC_A1_25', 0.8933, *TC_AKW, '', '', 'Table 4 of the source (value transcribed by the page reader)'),
 ('AlSi10Mg (Al-9.92Si-0.291Mg-0.137Fe powder)|mass_SI_DIAMOND_A4_25', 0.0971, *TC_AKW, '', '', 'Table 4'),
 ('AlSi10Mg (Al-9.92Si-0.291Mg-0.137Fe powder)|mass_MG2SI_B_25', 0.0046, *TC_AKW, '', '', 'Table 4'),
 ('AlSi10Mg (Al-9.92Si-0.291Mg-0.137Fe powder)|mass_ALFESI_T6_25', 0.0051, *TC_AKW, '', '', 'Table 4 lists Al9Fe2Si2 (beta-AlFeSi)'),
 ('AlSi10Mg (Al-9.92Si-0.291Mg-0.137Fe powder)|mass_PI_ALFEMGSI_25', 0.0, *TC_AKW, '', '', 'pi not in the TCAL6 equilibrium list (it appears only in their Scheil result)'),
 ('AlSi10Mg (Al-9.92Si-0.291Mg-0.137Fe powder)|mass_ALCRFEMNSI_A_25', 0.0, *TC_AKW, '', '', 'no alpha-AlFe(Mn)Si in the TCAL6 equilibrium list'),
 ('AlSi10Mg (Al-9.92Si-0.291Mg-0.137Fe powder)|mass_FeIMC_25', 0.0051, *TC_AKW, '', '', 'TCAL6: Al9Fe2Si2 is the only Fe phase (0.51 wt%)'),
 ('AlSi12 (binary Al-12Si)|liquidus', 581, *TC_ALSI12, '', '', '"alloy melting temperature 854 K (581 C) as per Scheil calculation"; paper alloy is nominal Al-12Si'),
 ('AlSi12 (binary Al-12Si)|eutectic', 577, *TC_ALSI12, '', '', 'Scheil eutectic temperature'),
 ('AlSi12 (binary Al-12Si)|solidus', 577, *TC_ALSI12, '', '', 'binary: solidus = eutectic temperature'),
 ('AlSi12 (binary Al-12Si)|scheil_end', 577, *TC_ALSI12, '', '', 'binary: Scheil ends at the eutectic'),
 ('AlSi12 (binary Al-12Si)|scheil_range', 3.6, *TC_ALSI12, '', '', '"solidification range ... is 3.6 C"'),
 ('AlSi12 (binary Al-12Si)|scheil_feut', 0.9995, *TC_ALSI12, '', '', 'paper: "more than 99.95% ... undergo a eutectic solidification at 577 C"; this is inconsistent with its own 581 C liquidus (lever rule gives about 0.95 eutectic), so the statement may mean something else'),
 ('AlSi|eut', 577, *TC_ALSI12, 577.0, ORCH + '10.1007/s11669-024-01160-5 (850.15 K; ORCHID extraction_accepted=false); 577 C also in doi:10.3390/ma10010076 (ASM handbook)', 'Thermo-Calc value is the Al-12Si Scheil eutectic'),
 ('AlZr|invariant_T', '', '', '', 660.85, ORCH + '10.1007/s11669-015-0398-y (934 K, Al3Zr + L -> fcc; accepted)', 'Contested: a eutectic L -> (Al) + Al3Zr at 929 K (655.85 C) with liquid at 0.72 at% Zr is reported in doi:10.1007/s11669-015-0398-y and doi:10.1007/s11669-020-00827-z (cited to doi:10.1007/s10973-013-3113-4). 661 C (934 K) also in doi:10.1051/matecconf/202032606002. No Thermo-Calc number found'),
 ('AlZr|fcc_solubility', 0.25, 'Thermo-Calc 2021a, TCAL7 (equilibrium)', '10.1557/s43578-022-00533-1', '', '', 'TC: "0.5 wt% Zr instead of 0.25 wt% Zr at equilibrium" (0.5 wt% when primary Al3Zr is suppressed). 0.28 wt% at the peritectic is quoted in Brunel-group papers (source unverified), not used'),
 ('AlZr|liquidus_0.217', '', '', '', '', '', 'No Thermo-Calc value. JMatPro (not Thermo-Calc) gives 720 C for Al-0.217Zr (doi:10.3390/ma12010022)'),
 ('AlZr|liquidus_0.5', '', '', '', '', '', 'No Thermo-Calc or experimental value found'),
 ('AlMnC|liquidus', '', '', '', '', '', 'Mehta et al. 2022 (doi:10.1557/s43578-022-00533-1, Thermo-Calc 2021a TCAL7) give no numeric liquidus or solidus in the text'),
 ('AlCu|eut_Al', '', '', '', 550.0, ORCH + '10.1007/s11669-024-01160-5 (823.15 K; extraction_accepted=false; cited to doi:10.1179/imr.1985.30.1.211)', ''),
 ('AlCu|perit_theta', '', '', '', 590.0, ORCH + '10.1007/s10853-020-05423-7 (862.15 and 864.15 K, L + eta -> theta; accepted)', 'mean of two records (589.0 and 591.0 C)'),
 ('AlCu|eut_Cu', '', '', '', 1035.0, ORCH + '10.1007/s10853-020-05423-7 (1308.15 K, liq -> beta + (Cu); accepted)', '1032.0 C (1305.15 K) in doi:10.1007/s11661-002-0173-7'),
 ('AlCu|eutectoid', '', '', '', 567.0, ORCH + '10.1007/s10853-020-05423-7 and 10.1007/s11661-002-0173-7 (840.15 K, beta -> (Cu) + gamma2; accepted)', '839.85 K also reported'),
 ('CrCu|eut', '', '', '', 1075.85, ORCH + '10.1007/s11106-006-0106-x (1349 K; accepted)', 'seven accepted records span 1343-1349 K'),
 ('CrCu|eut|xliq', '', '', '', 1.56, ORCH + '10.1007/s11106-006-0106-x (L at 0.0156; accepted)', 'another record gives 1.83 at% Cr'),
 ('CuZr|eut', '', '', '', 973.85, ORCH + '10.1007/bf02647618 (L -> (Cu) + Cu5Zr; median of 10 accepted records)', 'records span 1237-1253 K (963.85-979.85 C)'),
 ('CuSn|perit', '', '', '', 797.85, ORCH + '10.1016/j.intermet.2012.10.010 (1071 K, alpha + L -> beta; accepted)', '798.0 C (1071.15 K) in doi:10.1007/s11661-002-0173-7'),
 ('CuSn|perit|xliq', '', '', '', 15.0, ORCH + '10.1016/j.intermet.2012.10.010 (L at 0.150; accepted)', '15.5 at% in doi:10.1007/s11661-002-0173-7'),
 ('C63000|liquidus', '', '', '', 1054, CDA63, 'No Thermo-Calc (TCCU) number found in open sources. Handbook values are for the specification range, not this nominal composition'),
 ('C63000|solidus', '', '', '', 1035, CDA63, 'cooling-curve measurement on Cu-10.9Al-4.9Ni-4.0Fe-1.3Mn: start 1045.4 C (about 7 C undercooling), end 1038 C (doi:10.1038/s41598-023-44146-y)'),
 ('C63000Mn|liquidus', '', '', '', 1054, CDA63, 'C63000 allows up to 1.5 Mn'),
 ('C63000Mn|solidus', '', '', '', 1035, CDA63, ''),
 ('C95800|liquidus', '', '', '', 1060, CDA58, 'No Thermo-Calc number found'),
 ('C95800|solidus', '', '', '', 1043, CDA58, ''),
 ('C70600|liquidus', '', '', '', 1149, CUNI, 'No Thermo-Calc number found'),
 ('C70600|solidus', '', '', '', 1099, CUNI, ''),
 ('C71500|liquidus', '', '', '', 1238, CUNI, 'No Thermo-Calc number found'),
 ('C71500|solidus', '', '', '', 1171, CUNI, ''),
]
with open(OUT, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['key', 'thermocalc_value', 'thermocalc_db', 'thermocalc_source_doi', 'experiment_value', 'experiment_source', 'notes'])
    w.writerows(rows)
print(f'wrote {len(rows)} rows to {OUT}')
