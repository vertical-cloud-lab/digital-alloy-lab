# CALPHAD for the 316L walls: solidification, segregation, and the keyhole criterion

[`calphad_316l.py`](calphad_316l.py) runs pycalphad (0.12; Otis and Liu, J. Open Res. Softw. 5, 1 (2017),
https://doi.org/10.5334/jors.140) with MatCalc's open steel database to get what an open database can say about the 316L
in the M2 wall build before the Thermo-Calc AM Module runs: the equilibrium and Scheil solidification paths, the
segregation an etched or EDS section can see, how the 316L specification moves the solidification mode, the enthalpy
from room temperature to melting, and King et al.'s keyhole criterion for every wall set. Outputs:
[`out/calphad_316l_summary.json`](out/calphad_316l_summary.json) (every number below, with the database and the
compositions), [`out/calphad_316l_scheil.csv`](out/calphad_316l_scheil.csv) (equilibrium and Scheil paths, phase
fractions and liquid, austenite and ferrite compositions per step),
[`out/calphad_316l_keyhole.csv`](out/calphad_316l_keyhole.csv) (one row per wall set) and
[`out/m2-calphad-316l.png`](out/m2-calphad-316l.png).

`python calphad_316l.py` takes about 7 minutes on 4 cores the first time and seconds afterwards: the CALPHAD part is
cached in `.cache/`, and the keyhole table is rebuilt from `out/wall_sets.csv` on every run, so a changed sheet only
needs a rerun. The numbers here are for the sheet at commit e094d8e (33 sets: 32 Sobol settings in power, speed, spot
and trace spacing, plus the control at 370 W, 1350 mm/s, 130 µm, 0.09 mm; 42 walls).

## Database

MatCalc's open steel database mc_fe 2.062 (TU Wien, Povoden-Karadeniz and Jacob, 2024-11-08), from
https://www.matcalc.at/index.php/databases/open-databases, released under the Open Database License 1.0, with its
contents under the Database Contents License 1.0. It covers Fe, Cr, Ni, Mo, Mn, Si, C and N (and N is in the liquid,
austenite, ferrite and Cr2N), so nothing in the 316L spec except P and S is missing. It is not committed: the script
downloads it into `.cache/` from a pinned URL, checks its sha256, and fixes what pycalphad cannot read in memory (the
uncommented reference list, MatCalc-only commands, MatCalc's vacancy-enthalpy parameters, one unterminated command, two
`6000.00.00` upper limits), keeping only the parameters for the eight elements. BCC_B2 is left out because MatCalc
links its disordered part with a command pycalphad lacks; it does not form in 316L.

**The database's weak point for this job is silicon in austenite.** Two ternary terms,
L(FCC_A1,Cr,Fe,Si:Va;0) and L(FCC_A1,Fe,Mo,Si:Va;0), are both 50000 − 80 T J/mol, about −86 kJ/mol at 1700 K. With
1 wt% Si they make austenite about 0.2 kJ/mol more stable than the Fe-Cr-Ni-Mo core alone, which is enough to decide
the primary phase. Fe-18Cr-10Ni-3Mo solidifies as primary δ-ferrite in this database; add 1 wt% Si and it solidifies
as primary austenite, with the liquidus 28 K lower. Silicon is a ferrite former in every constitution diagram, so this
is the database, not the alloy. The script reruns the spec sweep without those two terms (`no_fcc_si_ternaries`) as a
sensitivity check. That variant is not better overall: it drops the solidus by up to 40 K.

## Compositions

There is no powder certificate in the repo: [`m2-single-track-schedule.md`](../m2-single-track-schedule.md) still
lists the lot and certificate as to-do. So the nominal is the middle of the 316L ranges, Fe-17Cr-12Ni-2.5Mo-1Mn-0.5Si-
0.02C-0.05N (wt%), and the two corners push every element to one end of ASTM A240 (Cr 16-18, Ni 10-14, Mo 2-3,
Mn ≤ 2, Si ≤ 0.75, C ≤ 0.03, N ≤ 0.10; F3184 for powder bed fusion allows Si ≤ 1.00):

| | Cr | Ni | Mo | Mn | Si | C | N | WRC-1992 Creq/Nieq | WRC-1992 mode |
|---|---|---|---|---|---|---|---|---|---|
| nominal | 17 | 12 | 2.5 | 1.0 | 0.5 | 0.02 | 0.05 | 1.42 | AF |
| high-ferrite corner | 18 | 10 | 3.0 | 0.1 | 1.0 | 0.005 | 0.01 | 2.02 | F |
| low-ferrite corner | 16 | 14 | 2.0 | 2.0 | 0.1 | 0.03 | 0.10 | 1.06 | A |

WRC-1992: Creq = Cr + Mo, Nieq = Ni + 35 C + 20 N (Kotecki and Siewert, Weld. J. 71, 171s (1992)), with the usual
mode boundaries A < 1.25 < AF < 1.48 < FA < 1.95 < F (Lippold and Kotecki, *Welding Metallurgy and Weldability of
Stainless Steels*, Wiley 2005). Rerun the script with the certificate's composition when the powder lot is known.

## Equilibrium solidification

| | Liquidus | Solidus | Range | Primary phase | δ-ferrite at equilibrium | At 1000 °C |
|---|---|---|---|---|---|---|
| nominal | 1426.3 °C | 1409.3 °C | 17.0 K | austenite | 1.2% from the last liquid, gone 4 K below the solidus | austenite only |
| high-ferrite corner | 1423.6 °C | 1409.3 °C | 14.3 K | austenite | 15% at the solidus, gone by 1339 °C | austenite + 1.7% σ + 0.2% χ (σ from about 1019 °C) |
| low-ferrite corner | 1427.0 °C | 1410.4 °C | 16.6 K | austenite | none | austenite only |

The liquidus sits 27-33 K below the Thermo-Calc TCFE values in the literature for 316L (liquidus about
1453-1459 °C, solidus 1400-1424 °C, ranges of 29-59 K: Wahib 2024, https://doi.org/10.34901/mul.pub.2024.074;
Sotiriou et al. 2021, https://doi.org/10.3390/iec2m-09237; collected in
[the Edison report](../../edison-trajectories/m2-walls-literature/solidification-316l-calphad-and-sem.md)). The
solidus falls inside their range, so the freezing range is about half of TCFE's. Use the AM Module's own TCFE numbers as inputs, not these.

## Scheil solidification

Classic Scheil (no diffusion in the solid), and a variant with C and N as fast diffusers (lever rule for C and N,
Scheil for the rest; an approximation to Thermo-Calc's "Scheil with fast diffusers"). Thermo-Calc's Scheil stops at 1%
liquid by default, so that is the "Scheil solidus" here.

| | 50% solid | 95% solid | 1% liquid left | δ-ferrite formed (by 1% liquid) | δ starts at |
|---|---|---|---|---|---|
| nominal, classic | 1417.6 °C | 1380.7 °C | **1321.9 °C** | **8.8%** | 67% solid, 1411 °C |
| nominal, C and N fast | 1417.7 °C | 1394.7 °C | **1378.4 °C** | **12.9%** | 66% solid |
| high-ferrite, classic / fast | 1414.3 °C | 1384-1388 °C | 1347.8 / 1363.9 °C | 16.5 / 17.3% | 44% solid |
| low-ferrite, classic / fast | 1418.9 °C | 1375-1395 °C | 1312.7 / 1383.9 °C | 1.2 / 7.9% | 91 / 84% solid |

So the "solidus" runs from 1409 °C (equilibrium) to 1378 °C (Scheil with fast C and N) to 1322 °C (classic Scheil), a
freezing range of 17, 48 or 104 K for the same alloy. In classic Scheil the last 1% of liquid holds 0.5% C and 0.6% N,
which C and N diffusing back into the solid would not allow, so the fast-diffuser number is the more realistic of the
two. The last liquid also forms traces of M23C6, M6C and Cr2N (about 0.1% in total).

**Segregation to the cell walls.** Mid-spec 316L, classic Scheil. The first austenite to form (the cell core) has
Cr 15.2, Ni 12.7, Mo 1.73 wt%. The austenite forming at 95% solid (next to the cell wall) has Cr 19.6, Ni 12.0,
Mo 3.54, and the residual liquid at 99% solid has Cr 29.6, Ni 7.4, Mo 8.0. Partition coefficients at the liquidus
(mole basis): Cr 0.89, Ni 1.06, Mo 0.67, Mn 0.88, Si 0.97, C 0.35, N 0.51. Wall-to-core ratios in the austenite
(95% solid against the first solid): Mo 2.05, Si 1.42, Mn 1.40, Cr 1.29, Ni 0.95 (fast C and N: Mo 1.86, Cr 1.25,
Ni 1.02). Mo segregates most, then Cr, while Ni is slightly depleted. The corners give the same ordering.

Measured walls are much weaker than this. Godec et al.'s STEM-EDS on as-built LPBF 316L gives Mo 4.2 vs 3.3 wt%
(1.27×) and Cr 17.4 vs 17.0 (1.02×) between cell wall and cell interior
(https://doi.org/10.1016/j.matchar.2019.110074), and Scheil overestimates LPBF segregation in general (Hasenbusch et
al., https://doi.org/10.1093/micmic/ozad065). Solute trapping at these growth rates and the probe's spatial
averaging both pull the contrast down. So Scheil gives the direction and the ordering (Mo > Cr, Ni slightly
depleted), not the size. Cells are 0.2-0.8 µm across, below the 1 µm or so that SEM-EDS at 15-20 kV samples in steel,
so EDS line scans across cells in the SEM will show little; the cells show up in etched contrast.

## Primary phase across the 316L spec

Along the straight line from the low-ferrite to the high-ferrite corner, WRC-1992 Creq/Nieq runs from 1.06 to 2.02 and
crosses every mode, A, AF, FA and F. So by WRC-1992 the spec alone allows anything from fully austenitic to fully
ferritic solidification (Grosswendt et al. make the same point for ASTM A276, https://doi.org/10.3390/ma14154074).

- **mc_fe as distributed:** primary austenite at every point on the line. A 3-phase Scheil to 1% liquid forms 1.2%
  ferrite at the low corner, rising steadily to 16.4% at the high corner: AF everywhere, never FA. This disagrees with
  WRC-1992 above 1.48, and the cause is the two Si terms above.
- **Without the two Si terms:** primary austenite up to Creq/Nieq 1.42 and primary δ-ferrite from 1.52 on (FA, 27-58%
  ferrite). The flip falls between 1.42 and 1.52, around WRC-1992's AF/FA boundary at 1.48.

The nominal (1.42) is AF in WRC-1992 and in both variants, but it sits close to the boundary, so the real powder's
composition decides AF against FA. Get the certificate.

## Enthalpy and h_s

Nominal composition, metastable austenite from 298 K (the steel is austenitic at room temperature, not at equilibrium)
and liquid at the alloy's composition; per volume with 7980 kg/m³, the room-temperature density in King et al.'s
Table 3:

| From 298 K to | Sensible only | With the latent heat |
|---|---|---|
| solidus (1682.5 K) | 0.800 MJ/kg = 6.39 GJ/m³ | 1.006 MJ/kg = 8.03 GJ/m³ |
| liquidus (1699.5 K) | 0.813 MJ/kg = 6.48 GJ/m³ | 1.019 MJ/kg = 8.13 GJ/m³ |

The latent heat is 0.206 MJ/kg, and the mean cp from 298 K to the solidus is 578 J/kg/K. The corners differ by under
1%. The latent heat is below the 0.26-0.33 MJ/kg used in 316L melt-pool models (0.33 in Sotiriou et al.), so this
database probably understates the enthalpy of melting.

**What King et al. meant by h_s:** the sensible "enthalpy at melting", h_s = ρ c T_m, with no latent heat (Sec. 2.1 and
footnote 2, which says they follow Hann et al. 2011; the threshold derivation then uses h_s = κ T_m / D, so T_m is
absolute and the heat is counted from 0 K). Their Table 3 value, 1.2 MJ/kg (×7980 = 9.58 GJ/m³, citing Rai et al.
2007, J. Phys. D 40, 5753), is c T_m with c ≈ 0.7 kJ/kg/K. That is 1.50 times the CALPHAD sensible enthalpy from 298 K
to the solidus, and 18% more than even the full enthalpy to liquid at the liquidus. None of the four CALPHAD numbers is
their h_s. The threshold of 30 was calibrated with their 9.58 GJ/m³, so a CALPHAD h_s only works with the threshold
rescaled: 30 becomes 46.6 with the CALPHAD sensible h_s and eagar_tsai_316l.py's D.

## King et al.'s keyhole criterion

Checked against the open manuscript (OSTI 1502044, LLNL-JRNL-642426; page numbers are the PDF's):

- **Formula:** ΔH/h_s = A P / (h_s √(π D v σ³)), Eq. 2.6 (p. 7). The unnumbered expression just above it puts π outside
  the root; Eq. 2.6 is the one they say they use, "following the original paper of Hann".
- **σ is the Gaussian standard deviation, not the beam radius:** I = I0 exp(−r²/2σ²) (footnote 1, p. 6; footnote 4,
  p. 10), and they report beam sizes as D4σ (footnote 3, p. 10). So σ = D4σ/4, 32.5 µm for the control's 130 µm spot.
  This checks out against their own numbers: Eq. 2.6 with σ = D4σ/4 and their Table 3 constants gives 44.3 for 334 W,
  171 mm/s, D4σ 130 µm, and 57.3 for 265 W, 1004 mm/s, D4σ 52 µm. The paper quotes 44 and 57 (p. 16, Fig. 6 on p. 28).
  The alternatives don't match: σ = D4σ/2 gives 15.7 and 20.3, the π-outside form with σ = D4σ/4 gives 25.0 and 32.3,
  and both together (as in eagar_tsai_316l.py, below) give 8.8 and 11.4.
- **Constants (Table 3, p. 36):** A 0.4, ρ 7.98 (printed "kg/m³", meaning g/cm³), h_s 1.2 × 10⁶ J/kg, D 5.38 × 10⁻⁶ m²/s.
  Powers are measured, not set-point: their M2 delivered 366 W at a 400 W set point (Table 2, p. 35).
- **Experimental threshold: 30 ± 4.** Depth is zero below about 10, the mode changes over about 26 to 34, and above about
  34 it is clearly keyhole (Sec. 5.3, p. 15). The 30 ± 4 itself is in Sec. 5.6 (p. 19) and conclusion 4 (p. 20), for
  CL 20ES 316L powder, 50 µm layers, single tracks at D4σ 52 and 130 µm on a Concept Laser M2. Their keyhole definition
  is depth greater than half the width (Sec. 5.2, p. 13).
- **Theoretical threshold:** ΔH/h_s > π T_b/T_m ≈ 6 (Eq. 2.7, p. 8), from the surface reaching boiling, with T_b ≈ 3273 K
  for steel (p. 5). With the CALPHAD liquidus or solidus and T_b 3090-3273 K it is 5.7-6.1. They call it "a crude
  estimate" against the measured 30 (p. 19).

**For the 33 sets** (King's constants, each set's own spot, σ = spot/4): ΔH/h_s runs from 6.0 to 53.5. Because the
spot now varies from 50 to 190 µm and ΔH/h_s goes as σ^−1.5, the spread is far wider than it would be at a fixed
130 µm. The control (370 W, 1350 mm/s, 130 µm) is at 17.5, which is conduction. Eleven sets reach 30 or more, all with
spots of 50-80 µm:

- **Clearly keyhole (≥ 34):** W014 (53.5), W004 (51.4), W016 (51.3), W024 (43.0), W026 (39.2), W012 (35.0).
- **At or just above the threshold (30-34):** W008 (33.9), W028 (33.2), W018 (32.9), W006 (30.7), W002 (30.3).

The other 22 sets are below 26. Nothing falls between 26 and 30.

**Against Ke:** King's ΔH/h_s and Gan et al.'s keyhole number Ke (Nat. Commun. 12, 2379 (2021),
https://doi.org/10.1038/s41467-021-22704-0) are the same dimensionless group, with different constants and a beam size
that differs by 2× (σ against r0 = spot/2). With these constants, ΔH/h_s = 3.73 Ke for every set. King's 26/30/34
therefore equals Ke 7.0/8.0/9.1, and his theoretical 6 equals Ke 1.6, close to Gan's conduction limit of 1.4. The two
criteria rank the sets identically. King's measured threshold sits about a third above Gan's Ke = 6 keyhole boundary,
so the 12 sets with Ke ≥ 6 (Ke runs 1.6-14.3, capped at 15) are King's 11 plus W020 (Ke 6.4, ΔH/h_s 23.8).

**With the CALPHAD h_s:** swapping in the CALPHAD sensible enthalpy (6.39 GJ/m³) and eagar_tsai_316l.py's D raises
every value 1.55× (to 9.3-83.0). Kept at 30, that would flag 18 sets; at the rescaled 46.6 it flags the same 11. A
CALPHAD h_s changes the units, not the verdict. It would matter when moving the criterion to another alloy, not
within 316L, where the threshold was measured directly.

**Against Eagar-Tsai:** a conduction model with a surface heat source never makes a pool deeper than its half-width,
which is King's keyhole definition, so Eagar-Tsai cannot flag keyholes itself. When `out/wall_sheet.csv` carries
Eagar-Tsai widths and depths for these sets, the script copies them in with their depth over half-width. The current
sheet has none.

**A note on the existing code:** `normalized_enthalpy` in [`eagar_tsai_316l.py`](eagar_tsai_316l.py) uses the
π-outside form with the 1/e² radius and h_s = ρ c T_liq. That gives about 0.22 times the values above, so the `dH_hs`
columns in `out/steady_state_grid.csv` and `out/finite_track_summary.csv` cannot be compared with 30 ± 4 as they
stand. This file leaves that code alone.

## What this means for the build and the AM Module comparison

- **Freezing range and solidus in the AM Module.** The AM Module takes its liquidus, solidus and mushy-zone
  enthalpy from its own TCFE calculation. Check whether that calculation is equilibrium or Scheil. Here the choice moves
  the solidus by 31-87 K, two to five times the equilibrium range. The etched melt-pool boundary is the fusion line,
  the liquidus side of a band a few µm wide, so compare measured pools with the AM Module's liquidus isotherm. Eagar-Tsai
  in this folder deepens the pool by 0.3-0.4% per K of liquidus shift (README), so a 17 K equilibrium range is about a
  6% depth question, and a Scheil range would be 15-40%.
- **What SEM should show.** Expect cellular-columnar austenite with cell walls enriched in Mo and Cr and slightly
  depleted in Ni, about 0.2-0.8 µm across, finer at the pool boundary. Every calculation here, and WRC-1992 for the
  nominal, puts 316L on the primary-austenite side or at the AF/FA boundary, and LPBF growth rates push it further
  toward primary austenite (Elmer, Allen and Eagar, Metall. Trans. A 20, 2117 (1989),
  https://doi.org/10.1007/BF02650298).
- **δ-ferrite.** Scheil forms 9-13% intercellular ferrite for the mid-spec composition, but as-built LPBF 316L is
  normally fully austenitic by XRD, with at most traces at cell boundaries in TEM (the Edison report's sources). Rapid
  solidification and reheating by later layers remove it. Do not expect δ-ferrite in SEM unless the certificate puts
  Creq/Nieq above about 1.5. Even then, it would be thin intercellular films, not something an unetched porosity
  section would show.
- **Keyhole porosity.** The 11 small-spot sets at ΔH/h_s ≥ 30 are where King et al. would expect keyhole pores. The 5
  between 30 and 34 are in the transition band, where their depth scattered most. Both criteria agree on the ranking and
  differ on one set, W020. Thin walls with a hatch run hotter than King's single tracks on a plate, so in the walls
  keyholes may start at lower ΔH/h_s.

## Caveats

- **Database.** MatCalc's mc_fe is assessed for solid-state precipitation in steels (673-2000 K). Its liquid is
  25-30 K low against TCFE, its freezing range about half TCFE's, and its latent heat (0.21 MJ/kg) low. Two FCC Si
  ternaries decide the primary phase. Use these numbers for trends and sensitivities, and the AM Module's TCFE for
  inputs. P and S, which widen real freezing ranges, are not included.
- **Composition.** These are mid-spec and spec-corner compositions, not a certificate. The WRC ratio of the actual lot
  is the single most useful number still missing.
- **Scheil.** Both variants are limits. Neither has solute trapping, which matters at LPBF growth rates, and the
  fast-C,N variant is a lever-rule approximation, not a full para-equilibrium calculation. Phase fractions are mole
  fractions of atoms.
- **Keyhole criterion.** It was calibrated on single tracks, 50 µm layers and measured (not set-point) power on an M2 in
  argon. LLNL's M2 delivered 7-14% less than its set point (King's Table 2). BYU's has not been measured, so the
  set-point powers used here may overstate ΔH/h_s by a similar amount. Each set's spot is taken as its D4σ diameter. The theoretical threshold (about 6) flags every set and is not useful.
