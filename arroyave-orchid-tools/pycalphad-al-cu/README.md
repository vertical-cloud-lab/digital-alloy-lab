# pycalphad with open databases vs Thermo-Calc and experiment: Al and Cu alloys (issue #235)

The Thermo-Calc column below holds numbers **published in the literature**: TCAL/TCAl, TCCU, or the AM module. Our
in-house Thermo-Calc results are the AM-module maps that Thermo-Calc ran for us (compared with eagar-tsai in
[`../eagar-tsai/`](../eagar-tsai/README.md#comparing-with-our-in-house-thermo-calc-am-module-results)). No in-house
Thermo-Calc equilibrium or Scheil numbers exist in the repo or its branches yet; the BYU desktop test plan
(`thermocalc-desktop-initial-tests.md`, branch `copilot/can-calphad-thermocalc-run-high-throughput`) has the TC-Python
scripts but no results. A blank Thermo-Calc cell means the literature search found no number for that quantity;
nothing was estimated or read off a plot. When in-house numbers exist, run the script and add them as another column.

For the two alloys in the AM-module runs, [`scripts/am_module_alloys_mc_al.py`](scripts/am_module_alloys_mc_al.py)
gives the mc_al liquidus and solidus ([csv](data/am_module_alloys_mc_al.csv)):

| Alloy (wt %) | Liquidus | Solidus | Primary phase |
|---|---|---|---|
| AlSi10Mg as sent to Thermo-Calc (Al 89.675, Si 10.0, Mg 0.325) | 868.6 K (595.4 °C) | 842.7 K (569.5 °C) | (Al) |
| BYU AA1100 + Si + AlSi10Mg blend (Al 75.56, Si 24.30, Mg 0.14) | 1019.3 K (746.2 °C) | 846.7 K (573.6 °C) | Si; (Al) joins at 850.2 K |

## Methods
- **Software:** pycalphad 0.11.2, scheil 0.3.0, Python 3.12.3, numpy 2.5.4, pandas 3.1.1, matplotlib 3.11.2. Pressure
  is 1 atm; compositions are in wt%, balance Al or Cu.
- **Rerunning everything:** `python scripts/pycalphad_al_cu_open_db.py all` regenerates every table and figure in
  about 7 minutes, single process. Single steps also run on their own: `orchid`, `al-alloys`, `alzr`, `almncrzr`,
  `binaries`, `cu-alloys`, `figures`, `literature`, `table`. The script reads the databases from a checkout of
  [orchid-calphad/orchid-project.org](https://github.com/orchid-calphad/orchid-project.org) (`data/databases/`).
- **Databases** (used in place and never copied here; SHA-256 values in `data/databases_used.csv`):
  - **MatCalc mc_al v2.032** (ODbL 1.0 / DbCL 1.0; the pycalphad/binder copy), for the Al alloys.
    - Elements: Al, Cr, Cu, Fe, Mg, Mn, Ni, Sc, Si, Ti, Zn, Zr. That covers AlSi10Mg with Fe, Al–Zr, Al–Mn–Cr–Zr
      and Scalmalloy. It has no Sn.
    - One syntax patch: the file makes the metastable GP-zone phase GP_MAT the ordered form of FCC_A1. In pycalphad
      that link drops FCC_A1, the Al matrix, so it is removed and GP_MAT excluded.
    - Also excluded: metastable precipitates and clusters (β″, β′, θ′, L1₂-Al₃Zr and others) and the helper phases
      FCCAL, FCCMG and FCCSI.
  - **MatCalc mc_ni v2.036** (ODbL 1.0), for the Cu alloys.
    - Downloaded from matcalc.at; its SHA-256 matches the ONR YIP pycalphad-cu work.
    - That approach is reused unchanged (`scripts/onr_yip_run_calphad_ref.py`, copied from branch
      `claude/onr-yip-fy27`): syntax conversion and the phase set LIQUID, FCC_A1, BCC_A2, NIAL, GAMMA_PRIME, HCP_A3.
    - It covers Al, Cu, Fe, Mn and Ni, but has no Cu–Al–Ni ternary parameters; it was built for Ni superalloys.
  - **SGTE binary collection** (Hallstedt, Calphad 89 (2025) 102833, doi:10.1016/j.calphad.2025.102833, CC BY 4.0):
    - Al–Si: 97Feu-LB, 14Lia
    - Al–Zr: eight datasets
    - Al–Cu: 21Kro, 98Sau-LB
    - Cu–Ni: 92Mey-LB, 07Tur, 87Jan, 89Sri
    - Cr–Cu: 17Liu, 95Zen-LB
    - Cu–Zr: 22Zho, 94Zen-LB
    - Cu–Sn: 24Oik, 96Shi-LB
- **Liquidus, solidus and the first appearance of each phase:** a 4–5 K temperature scan, then bisection to 0.1 K
  (0.02 K for the Al–Zr invariant).
- **Scheil:** starts 2 K above the liquidus in adaptive 1 K steps (2 K for Al–Mn–Cr–Zr).
  - Fraction eutectic is 1 − fs at the point where Si first forms.
  - Freezing range is the equilibrium liquidus minus T at fs = 0.99.
  - Phase fractions are per mole of atoms unless labelled "mass".
- **Binary invariants:** from pycalphad's binary mapper (`BinaryStrategy`, `get_invariant_data`). For all nine datasets
  checked they agree to within 0.01 K with ORCHID's own pycalphad invariants (`orchid-data/parquet/phase_diagram_invariants.parquet`).
- **Experimental values:** accepted experimental records from the ORCHID literature release of 2026-10-23 (CC BY 4.0).
  For Al–Si and the Al-rich Al–Cu eutectic only non-accepted records exist; those are flagged. Cu-alloy values are
  CDA handbook data from supplier data sheets.
- **Thermo-Calc values:** an open-literature search. `data/thermocalc_literature.csv` gives the DOI, database and
  version, and a short verbatim quote for each. Only numbers stated in text or tables are used; they are curated in
  `data/literature_values.csv`.

## Comparison

These are the key rows. All 225 are in `data/comparison.csv`, and `scripts/make_report_table.py` prints the 64 that
have a reference value. Temperatures are in °C.

| System / alloy | Quantity | pycalphad (database) | Thermo-Calc (db; DOI) | Experiment (source) | Δ vs TC | Δ vs exp |
|---|---|---|---|---|---|---|
| AlSi10Mg | liquidus / solidus | 595.4 / 568.8 (mc_al) | none found | 597 / 563 (DSC, arXiv:2507.23422) | | −1.6 / +5.8 |
| AlSi10Mg | equilibrium range; Scheil range; T at fs = 0.9 / 0.99; eutectic fraction | 26.6 K; 36.0 K; 568.0 / 559.4; 0.77 | none | DSC range 34 K | | −7.4 |
| Al–12Si–0.35Mg | liquidus / solidus; Scheil range; eutectic fraction | 580.9 / 568.6; 21.5 K; 0.95 | none | | | |
| Al–12Si (binary) | liquidus; eutectic; Scheil range | 581.8; 577.7; 4.2 K | 581; 577; 3.6 (TCAL7, Thermo-Calc 2022a; 10.1007/s11665-023-08502-3) | | +0.8; +0.7; +0.6 | |
| Al–12Si (binary) | Scheil eutectic fraction | 0.951 | ">99.95 %" (same paper) | | −0.049 | |
| Al–9.92Si–0.291Mg–0.137Fe | mass fractions at 25 °C: (Al) / Si / Mg₂Si | 0.8935 / 0.0973 / 0.0046 | 0.8933 / 0.0971 / 0.0046 (TCAL6, 2023b; 10.3390/ma16144920) | | ≤ 0.0002 | |
| same | Fe-bearing phase at 25 °C | α-Al(Fe,Mn)Si 0.0045; β 0 | β-Al₉Fe₂Si₂ 0.0051 | | phase differs | |
| Al–Si | eutectic T | 577.0 (SGTE 97Feu-LB, 14Lia) | 577 (TCAL7) | 577.0 (ORCHID, 10.1007/s11669-024-01160-5) | 0.0 | 0.0 |
| Al–Zr | Al-rich invariant T | 660.6–660.9 peritectic (98Sau-LB, 86Sau, 01Wan, 15Fis); 660.2 (18Khv, 20Lon); 656.6 eutectic (mc_al); 656.9 (10Hir); 656.5 (18Tam) | none | 660.85 (934 K; ORCHID, 10.1007/s11669-015-0398-y) | | −0.2 to +0.1; −0.7; −4.2 |
| Al–Zr | Zr in (Al) at the invariant, wt% | 0.27–0.28 (peritectic sets); 0.14 (mc_al); 0.05 (18Khv, 20Lon) | 0.25 (TCAL7, 2021a; 10.1557/s43578-022-00533-1) | | +0.02 to +0.03; −0.11 | |
| Al–0.217 / 0.5 / 1.0 Zr | liquidus | SGTE 707–770 / 795–829 / 878–894; mc_al 659.9 / 659.4 / 656.6 | none (JMatPro gives 720 at 0.217 Zr; 10.3390/ma12010022) | | | |
| Al–Mn–Cr–Zr, Mehta A / B / C | liquidus (primary phase); solidus; Scheil T at fs = 0.99 | 696.3 (Al₆Mn) / 812.2 (Al₄(Cr,Mn)) / 814.9 (Al₄(Cr,Mn)); 652.7 / 656.0 / 653.2; 652.3 / 655.1 / 652.6 | no numbers in the text (TCAL7 used) | | | |
| Al–Cu | L → (Al) + θ | 548.5 (21Kro), 547.6 (98Sau-LB) | none | 550.0 (ORCHID, not accepted) | | −1.5, −2.4 |
| Al–Cu | L + η → θ | 593.0, 595.9 | none | 590.0 (ORCHID, 10.1007/s10853-020-05423-7) | | +3.0, +5.9 |
| Cu–Al | L → (Cu) + β; β → (Cu) + γ₂ | 1042.7, 1036.1; 567.4, 564.7 | none | 1035.0; 567.0 (ORCHID) | | +7.7, +1.1; +0.4, −2.3 |
| Cu–Cr | eutectic T; liquid at% Cr | 1077.4, 1074.8; 1.21, 1.83 | none | 1075.85; 1.56 (ORCHID, 10.1007/s11106-006-0106-x) | | +1.6, −1.1 |
| Cu–Zr | L → (Cu) + Cu₅Zr | 970.0 (22Zho), 967.6 (94Zen-LB) | none | 973.85 (median of 10 records spanning 964–980; ORCHID, 10.1007/bf02647618) | | −3.8, −6.2 |
| Cu–Sn | L + (Cu) → β | 785.8 (24Oik), 796.0 (96Shi-LB) | none | 797.85 (ORCHID, 10.1016/j.intermet.2012.10.010) | | −12.1, −1.9 |
| C63000 (Cu–10Al–5Ni–3Fe) | liquidus / solidus | 1124.5 / 1044.2 (mc_ni); with 1 Mn: 1121.5 / 1037.1 | none found (TCCU) | 1054 / 1035 (CDA) | | +70.5 / +9.2 |
| C95800 | liquidus / solidus | 1111.5 / 1035.6 | none | 1060 / 1043 (CDA) | | +51.5 / −7.4 |
| C70600; C71500 | liquidus / solidus | 1131.3 / 1104.0; 1229.2 / 1171.2 | none | 1149 / 1099; 1238 / 1171 (handbook) | | −17.7 / +5.0; −8.8 / +0.2 |
| Cu–10Ni; Cu–30Ni (binary) | liquidus / solidus | SGTE 1136–1151 / 1120–1128, mc_ni 1128 / 1116; SGTE 1235–1255 / 1188–1201, mc_ni 1227 / 1178 | none | | | |

## Findings
1. **Si enrichment.** Going from 10 to 12 wt% Si roughly halves the freezing range, both at equilibrium
   (26.6 → 12.3 K) and under Scheil (36.0 → 21.5 K). The eutectic fraction rises from 0.77 to 0.95, while the
   terminal Al–Si–Mg₂Si eutectic stays near 559 °C. Adding 0.3 Fe shifts temperatures by only about 1 K: β-AlFeSi
   forms at 573.9 °C, and Scheil adds π-AlFeMgSi. This is the comparison the proposal's AM-module figure makes for
   stock vs Si-enriched AlSi10Mg ([figure](figures/alsi10mg_scheil_vs_equilibrium.png)).
2. **mc_al matches published Thermo-Calc numbers for Al–Si.** It reproduces them to within 1 K, and the
   room-temperature phase fractions of AlSi10Mg to within 0.0002 (TCAL6). Treat the identity of the Fe-bearing phase
   below about 450 °C with caution.
3. **Don't use mc_al for Al–Zr**, nor for the Zr part of Al–Mn–Cr–Zr. Its Al–Zr liquid takes far too much Zr
   (0.5 at% at the invariant), so Al₃Zr never forms first from the melt, and the invariant comes out as a 656.6 °C
   eutectic. TCAL7 and the experimental peritectic agree with the SGTE peritectic datasets (98Sau-LB/COST 507, 86Sau,
   01Wan, 15Fis), so use those for Al–Zr. The experimental literature does also contain a eutectic interpretation at
   929 K (doi:10.1007/s10973-013-3113-4).
4. **Al–Mn–Cr–Zr.** The three alloys of Mehta et al. (2022) have liquidi of 700–815 °C and almost no Scheil freezing
   range once (Al) forms. The Cr-bearing ones solidify with primary Al₄(Cr,Mn). At 400 °C alloy C is (Al) 0.744,
   Al₆Mn 0.160, Al₁₂Mn 0.088 and Al₃Zr 0.007 (mole fractions).
5. **Cu binaries.** The SGTE datasets match ORCHID's experimental invariants within ±8 K. The exception is Cu–Sn
   24Oik, at −12 K; the older -LB/COST sets are often closer.
6. **Nickel-aluminium bronze.**
   - Solid-state sequence for C63000: β on solidification, α from about 940 °C, and β gone below about 835 °C.
   - At 600 °C: 87 % α, 9 % NiAl-type κ and 4 % Fe-rich κ (mole).
   - For C95800, β is gone below about 730 °C.
   - The liquidus is **not** usable (+50 to +70 K), because the Cu–Al–Ni–Fe interactions are missing.
   - [C63000 figure](figures/nab_c63000_phase_fractions.png)

## Caveats
- **Few Thermo-Calc numbers are published, and often for slightly different compositions.**
  - The TCAL6 values come from a table, transcribed by a page reader.
  - The paper's "99.95 % eutectic" statement contradicts its own liquidus.
  - TCAL7 values exist for a 0.8 Mn AlSi10MnMg die-casting alloy (doi:10.1007/s40962-023-01018-5): (Al) start at
    about 590 °C and eutectic at about 570–574 °C. It is a different alloy, so it isn't used.
  - **No published Thermo-Calc liquidus or solidus was found for standard AlSi10Mg, for nickel-aluminium bronze or
    Cu–Ni, or for the Al–Zr liquidus.** That is exactly where our own Thermo-Calc runs would add the most.
- **Experimental and handbook values.** ORCHID's values are machine-extracted, and the Al–Si and Al-rich Al–Cu
  eutectic records are not accepted ones. Handbook values cover a specification range. A 0.28 wt% Al–Zr solubility
  quoted in the literature couldn't be traced to a source, so it isn't used.
- **Modelling simplifications.** Al–Mn–Cr–Zr was computed without Fe and Si. mc_ni's κ phases are approximations:
  NiAl takes no Cu or Fe, and Fe-rich κ is modelled as disordered bcc. Phase fractions are equilibrium or Scheil, with
  no LPBF kinetics.
- **Not done:** Scalmalloy (mc_al covers Al–Mg–Sc–Zr, but it wasn't computed), and the Cu–Ni miscibility gap wasn't
  quantified.
- **Licences:** no database file is copied here; databases are cited by name, version and SHA-256.

## Reproduce
```bash
git clone --depth 1 https://github.com/orchid-calphad/orchid-project.org   # open TDBs
git clone --depth 1 https://github.com/orchid-calphad/orchid-data          # experimental values (1.6 GB)
export OPEN_TDB_ROOT=$PWD/orchid-project.org/data/databases ORCHID_LIT=$PWD/orchid-data/literature
export CU_CALPHAD_CACHE=$PWD/tdb_cache      # mc_ni is downloaded from matcalc.at into here
uv venv --python 3.12 .venv-pycalphad
uv pip install --python .venv-pycalphad/bin/python pycalphad scheil matplotlib pandas pyarrow
.venv-pycalphad/bin/python scripts/pycalphad_al_cu_open_db.py all
.venv-pycalphad/bin/python scripts/make_report_table.py table.md
```

## Files
- `scripts/`:
  - `pycalphad_al_cu_open_db.py`: `all` regenerates everything.
  - `make_literature_values.py` and `make_report_table.py`: helpers.
  - `onr_yip_run_calphad_ref.py`: the ONR YIP script, copied unchanged and imported for the Cu alloys.
- `data/`:
  - Overall: `comparison.csv` (225 rows), `literature_values.csv`, `thermocalc_literature.csv` (44 sourced rows with
    short quotes), `databases_used.csv` (file names and SHA-256).
  - Al: `al_alloys_summary.csv`, `al_eq_fractions_*.csv`, `al_scheil_*.csv`.
  - Al–Zr and Al–Mn–Cr–Zr: `alzr_summary.csv`, `alzr_liquidus.csv`, `almncrzr_summary.csv`, `almncrzr_scheil_*.csv`.
  - Binaries: `binary_invariants_pycalphad.csv`, `orchid_invariants_*.csv`.
  - Cu: `cu_alloys_summary.csv`, `cuni_binary_liquidus_solidus.csv`, `nab_C63000_phase_fractions_mc_ni.csv`,
    `nab_C95800_phase_fractions_mc_ni.csv`.
- `figures/` (13 PNGs):
  - Solidification: `alsi10mg_scheil_vs_equilibrium.png`, `nab_c63000_phase_fractions.png`,
    `nab_c95800_phase_fractions.png`.
  - Phase diagrams: `pd_al-si_*.png`, `pd_al-zr_alrich_liquidus.png`, `pd_al-cu_*.png`, `pd_cu-ni_full.png`,
    `pd_cr-cu_full.png`, `pd_cu-zr_full.png`, `pd_cu-sn_full.png`.
- `logs/`: per-step logs, plus `run_all_from_scratch_copy.log`, a clean rerun of `all` in a fresh copy (405 s; same
  data apart from wall times and the later edits).
