# Per-element verdicts as returned by Edison (unedited)

Parsed by `tabulate_verdicts.py` from the last line of each answer in `phase1/`. These are Edison's numbers, before the cross-checks and decisions in README.md.

| Element | Decision | Family | Conservative max (wt%) | Non-conservative max (wt%) | Floor (wt%) | Impurity max (wt%) | Evidence | TCCU7 tier |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| [Cu](phase1/el-01-Cu.md) | LIMIT | both | min 65 | min 60 | NA | NA | moderate | matrix |
| [Ni](phase1/el-02-Ni.md) | INCLUDE | both | 33 | 35 | 2 | NA | moderate | 1 (>=6) |
| [Al](phase1/el-03-Al.md) | INCLUDE | both | 9.5 | 10.5 | 1.8 | NA | moderate | 1 (>=6) |
| [Fe](phase1/el-04-Fe.md) | INCLUDE | both | 5.0 | 6.0 | 0.4 | NA | moderate | 1 (>=6) |
| [Mn](phase1/el-05-Mn.md) | INCLUDE | both | 1.5 | 4.4 | 0.9 | NA | moderate | 1 (>=6) |
| [Cr](phase1/el-06-Cr.md) | INCLUDE | Cu-Ni | 0.5 | 2.0 | 0.5 | NA | moderate | 1 (>=6) |
| [Sn](phase1/el-07-Sn.md) | INCLUDE | both | 1.0 | 1.5 | 0.5 | NA | moderate | 1 (>=6) |
| [Zn](phase1/el-08-Zn.md) | LIMIT | both | NA | NA | NA | 0.5 | thin | 1 (>=6) |
| [Si](phase1/el-09-Si.md) | INCLUDE | both | 2.0 | 3.8 | 0.5 | NA | thin | 1 (>=6) |
| [Nb](phase1/el-10-Nb.md) | INCLUDE | Cu-Ni | 0.80 | 1.00 | 0.50 | NA | thin | 2 (3-5) |
| [Be](phase1/el-11-Be.md) | LIMIT | both | NA | NA | NA | 0.10 | thin | 3 (0-2) |
| [Co](phase1/el-12-Co.md) | INCLUDE | both | 1.0 | 2.0 | 0.5 | NA | thin | 1 (>=6) |
| [Ti](phase1/el-13-Ti.md) | INCLUDE | both | 0.10 | 0.50 | 0.012 | NA | thin | 2 (3-5) |
| [Zr](phase1/el-14-Zr.md) | INCLUDE | both | 0.15 | 0.50 | 0.010 | NA | thin | 2 (3-5) |
| [Hf](phase1/el-15-Hf.md) | EXCLUDE | both | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
| [Mg](phase1/el-16-Mg.md) | LIMIT | both | NA | NA | NA | 0.01 | thin | 2 (3-5) |
| [Ag](phase1/el-17-Ag.md) | INCLUDE | Al-bronze | 0.25 | 1.0 | 0.25 | NA | thin | 1 (>=6) |
| [V](phase1/el-18-V.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
| [B](phase1/el-19-B.md) | INCLUDE | both | 0.020 | 0.050 | 0.002 | NA | thin | 3 (0-2) |
| [As](phase1/el-20-As.md) | LIMIT | both | NA | NA | NA | 0.0005 | thin | 3 (0-2) |
| [Sb](phase1/el-21-Sb.md) | LIMIT | both | NA | NA | NA | 0.02 | thin | 4 (not in TCCU7) |
| [P](phase1/el-22-P.md) | LIMIT | both | NA | NA | NA | 0.020 | moderate | 2 (3-5) |
| [Pb](phase1/el-23-Pb.md) | LIMIT | both | 0.01 | 0.05 | NA | 0.01 | moderate | 2 (3-5) |
| [Bi](phase1/el-24-Bi.md) | LIMIT | both | NA | NA | NA | 0.001 | moderate | 3 (0-2) |
| [Se](phase1/el-25-Se.md) | LIMIT | both | NA | NA | NA | 0.006 | thin | 3 (0-2) |
| [Te](phase1/el-26-Te.md) | LIMIT | both | NA | NA | NA | 0.003 | thin | 4 (not in TCCU7) |
| [S](phase1/el-27-S.md) | LIMIT | both | NA | NA | NA | 0.010 | thin | 1 (>=6) |
| [Cd](phase1/el-28-Cd.md) | LIMIT | none | NA | NA | NA | 0.01 | thin | 3 (0-2) |
| [O](phase1/el-29-O.md) | LIMIT | both | NA | NA | NA | 0.013 | moderate | 2 (3-5) |
| [H](phase1/el-30-H.md) | LIMIT | both | NA | NA | NA | 0.0001 | thin | 4 (not in TCCU7) |
| [N](phase1/el-31-N.md) | LIMIT | both | NA | NA | NA | 0.0005 | thin | 4 (not in TCCU7) |
| [C](phase1/el-32-C.md) | LIMIT | both | NA | NA | NA | 0.005 | thin | 3 (0-2) |
| [Mo](phase1/el-33-Mo.md) | LIMIT | both | NA | NA | NA | 0.02 | thin | 2 (3-5) |
| [W](phase1/el-34-W.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
| [Ta](phase1/el-35-Ta.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 3 (0-2) |
| [Ga](phase1/el-36-Ga.md) | LIMIT | both | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
| [Ge](phase1/el-37-Ge.md) | INCLUDE | Al-bronze | 0.2 | 3.0 | 0.2 | NA | thin | 3 (0-2) |
| [In](phase1/el-38-In.md) | LIMIT | both | NA | NA | NA | 0.01 | thin | 4 (not in TCCU7) |
| [Li](phase1/el-39-Li.md) | LIMIT | both | NA | NA | NA | 0.005 | thin | 4 (not in TCCU7) |
| [Ca](phase1/el-40-Ca.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 3 (0-2) |
| [Sr](phase1/el-41-Sr.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
| [Sc](phase1/el-42-Sc.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
| [Y](phase1/el-43-Y.md) | INCLUDE | Cu-Ni | 0.021 | 0.05 | 0.021 | NA | thin | 4 (not in TCCU7) |
| [La](phase1/el-44-La.md) | INCLUDE | both | 0.05 | 0.10 | 0.05 | NA | thin | 2 (3-5) |
| [Ce](phase1/el-45-Ce.md) | LIMIT | both | NA | NA | NA | 0.04 | thin | 2 (3-5) |
| [Pr](phase1/el-46-Pr.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
| [Nd](phase1/el-47-Nd.md) | LIMIT | both | NA | NA | NA | 0.01 | thin | 4 (not in TCCU7) |
| [Er](phase1/el-48-Er.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
| [Gd](phase1/el-49-Gd.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
| [Pd](phase1/el-50-Pd.md) | EXCLUDE | none | NA | NA | NA | NA | thin | 4 (not in TCCU7) |
