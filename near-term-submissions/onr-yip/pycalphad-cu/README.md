# Preliminary pycalphad calculations: Cu-Ni and nickel-aluminum bronze (open database)

> In this repository the database file and the figure PNGs are not committed: `run_calphad.py` downloads `mc_ni_v2036.tdb` from MatCalc, checks its sha256 and regenerates the figures. The two-panel figure used in the proposal is `../figures-cu-ded/cu_calphad_prelim.pdf`.

These are equilibrium and Scheil calculations run in pycalphad with an **openly licensed** thermodynamic
database: the MatCalc open Ni database `mc_ni` v2.036 (TU Wien, ODbL 1.0). It covers Cu-Ni-Al-Fe-Mn.
**No Thermo-Calc database (TCCU or any other) was used.** Everything here is reproduced by
`python run_calphad.py` (about 1.5 min). Add `--crosscheck` to also run two other open databases.

## Files

| File | Content |
|---|---|
| `run_calphad.py` | End to end: checks the TDB's sha256, converts its syntax, runs all calculations, writes the CSVs and figures |
| `mc_ni_v2036.tdb` | The database, byte-identical to the MatCalc download (ODbL allows redistribution; see License) |
| `reference_alloys.csv` | Equilibrium and Scheil melting ranges for C71500, C70600 and C95800, with handbook values |
| `crosscheck.csv` | Equilibrium melting ranges of the same three alloys with mc_ni, mc_fe v2.062 and COST 507 |
| `nab_phase_fractions.csv` | Equilibrium phase fractions for C95800, 1150 to 600 °C in 2 °C steps |
| `composition_map.csv` | Liquidus, solidus, freezing range, primary phase and wall time on the 7 × 6 map grid |
| `cu_calphad_prelim.png/.pdf` | Two-panel figure, 6.5 × 2.6 in |
| `cu_map.png/.pdf`, `cu_panel2.png/.pdf` | The same panels as separate 3.1 × 2.4 in files, without panel letters |

## Database and provenance

- **Database:** MatCalc open thermodynamic database for Ni-base alloys, `mc_ni_v2036.tdb`, version
  2.036 (updated 2024-08-20). Editor and copyright holder: Erwin Povoden-Karadeniz, TU Wien.
  Downloaded 2026-10-24 from <https://www.matcalc.at/images/stories/Download/Database/mc_ni_v2036.tdb>,
  which is listed on <https://www.matcalc.at/index.php/databases/open-databases>.
  sha256 `84ba813156e1f7d8bde495d74420319afec03572b981f6b56103807f305313ab`.
  The database has no journal paper or DOI of its own. Cite it as: E. Povoden-Karadeniz, *MatCalc
  open thermodynamic database mc_ni*, v2.036, TU Wien (2024).
- **License:** Open Database License (ODbL) 1.0, with contents under the Database Contents License
  (DbCL) 1.0, as stated in the file header and on the download page. Both allow redistribution with
  attribution, which is why the file is copied here unmodified. The script converts its syntax at run
  time into a derived database. Any public release of that derived database must also be under ODbL.
- **Assessments behind the parameters used here** (from the file's own reference list): Cu-Ni liquid,
  A. Jansson, TRITA-MAC-0340 (KTH, 1987). Cu-Ni fcc, Al-Cu fcc/bcc and some ternaries, N. Saunders
  in *COST 507 Thermochemical database for light metal alloys* vol. 2 (1998) and J. Miettinen, TKK-MK-76
  (1999). Al-Cu liquid and Cu-Al-Fe, J. Miettinen, *Calphad* 27 (2003) 91. Al-Ni, I. Ansara et al.,
  *J. Alloys Compd.* 247 (1997) 20. Al-Fe-Ni, L. Zhang and Y. Du, *Calphad* 31 (2007) 529. Cu-Fe,
  M.A. Turchanin et al., *J. Phase Equilib.* 24 (2003) 307. Cu-Mn, C. He et al., *J. Alloys Compd.*
  457 (2008) 233. Cu-Mn-Fe, C.P. Wang et al., *J. Alloys Compd.* 438 (2007) 129. The NiAl (B2) and
  Ni3Al (L1₂) phases use MatCalc's own simplified descriptions.
- **All ten binaries** of Al-Cu-Fe-Mn-Ni have liquid, fcc and bcc parameters in this file; none is
  silently ideal. **There is no Cu-Al-Ni ternary parameter.** Cu also does not dissolve in the NiAl
  phase.
- **Phases included:** LIQUID, FCC_A1, BCC_A2, NIAL (B2), GAMMA_PRIME (Ni3Al), HCP_A3. HCP and γ′
  did not appear in any result here (the NAB scan, or the first solid on the map). Excluded phases: carbides, borides and nitrides (no C, B or N); Ni3Ti, Ni3Nb,
  Laves and R-type phases (no Ti, Nb, Mo or Cr); α-Mn and β-Mn. β-Mn came out spuriously stable in
  plain Cu-30Ni, at 1,346 °C, so those Mn phases' parameters are not usable for Cu-Ni.
- **Syntax conversion** (`clean_tdb_text`, which changes no numbers): latin-1 is converted to ASCII
  and comments are stripped. MatCalc's `ATTACH_CONTRIBUTION … ORDER_DISORDER` becomes the equivalent
  `TYPE_DEFINITION … DIS_PART`. MatCalc-only commands, phase descriptions and kinetic (HMVA)
  parameters are dropped, along with parameters for elements outside Al-Cu-Fe-Mn-Ni. One parameter
  that was missing its `!` terminator is split off. As a check, the converted mc_fe gives NiAl melting
  at about 1,650 °C, close to the accepted 1,638 °C.
- **Software:** pycalphad 0.11.2, scheil 0.3.0, Python 3.12.3, numpy 2.5.4, pandas 3.1.0 and
  matplotlib 3.11.2, on a GitHub Actions Linux runner.

### Other open databases checked

| Candidate | Result |
|---|---|
| COST 507 (frozen Round II, 1999), the copy bundled with pycalphad 0.11.2 (`pycalphad/tests/databases/COST507.tdb`, sha256 `6565f4d67695fbbf779d68b9eeeb83e86e44a1a3dde9bafd612d99daffb9c34d`). The terms are "may be used freely", so it is not copied here | Good Cu-Ni (an Mey 1992) and Al-Cu. **No Al-Ni, Fe-Ni, Cu-Mn or Mn-Ni parameters**, so NAB is computed with Ni-Al treated as ideal. Used only as a cross-check |
| COST507R.TDB in the OpenCalphad repository (<https://github.com/sundmanbo/opencalphad/blob/master/examples/macros/cost507R.TDB>, sha256 `824cf2c38cc474d4d476431f4b409cb04461eb81860df08d41f15ecc749e950f`) | Same data, but `GHSERNI` stops at 1,728 K. pycalphad sets it to zero above that, which melts Cu-30Ni backwards. Not used |
| MatCalc `mc_fe` v2.062 (steels, ODbL; <https://www.matcalc.at/images/stories/Download/Database/mc_fe_v2062.tdb>, sha256 `aa02077eac3f602dd7479cbeafb09b450e282716752b3ae2b1fc3a57d9c64865`; the script downloads it for `--crosscheck`) | Self-consistent Cu-Ni (Jansson, Servant et al. 2001) and an ordered B2 (Ansara/Dupin). For NAB, though, the (Fe,Ni)Al B2 phase is stable in the melt up to **1,245 °C**, against a handbook liquidus of 1,060 °C. Cross-check only |
| MatCalc `mc_al` v2.037 (Al alloys, ODbL; sha256 `87ec595f2caae189227ed11d5598c899b436b866ccfefea91304ca57188817c4`) | Has no B2 NiAl phase (Al3Ni2 stands in for it) and is optimized for X(Al) > 0.9. NAB liquidus 1,157 °C. Not used |
| pycalphad test databases with Al-Ni (alnipt, alcrni, Dupin 2001, …) | No Cu |
| NIST solder database, NIMS CPDDB | Cu-Ni only, or registration with no-redistribution terms. Not used |
| TDBDB index (tdbdb.org) | Did not resolve from the runner (DNS failure, 2026-10-24) |

## Computed vs handbook melting ranges (mc_ni v2.036)

Nominal compositions in wt%, balance Cu: C71500 is Cu-30Ni-0.6Fe-0.6Mn, C70600 is Cu-10Ni-1.4Fe-0.8Mn
and C95800 is Cu-9.2Al-4.5Ni-4Fe-1.2Mn. All elements were kept, since the database has all five. The
handbook ranges are the Copper Development Association values the proposal cites. Equilibrium
temperatures come from bisection to 0.1 °C. "Scheil, 99 % solid" is the temperature at which the
Scheil liquid fraction falls to 1 %.

| Alloy | Handbook solidus–liquidus (°C) | Equilibrium solidus–liquidus (°C) | Δ solidus / Δ liquidus (°C) | Equilibrium range (°C) | First solid | Scheil: first solid → 99 % solid (°C) |
|---|---|---|---|---|---|---|
| C71500 70-30 Cu-Ni | 1,171–1,238 (67) | **1,171–1,229** | 0 / −9 | 58 | α (fcc) | 1,228 → 1,061 |
| C70600 90-10 Cu-Ni | 1,099–1,149 (50) | **1,104–1,131** | +5 / −18 | 27 | α (fcc) | 1,130 → 1,018 |
| C95800 NAB | 1,043–1,060 (17) | **1,036–1,112** | −7 / +51 | 76 | Fe-rich bcc (κ-like) | 1,116 → 1,020 |

Cross-check: equilibrium solidus–liquidus in °C (`crosscheck.csv`).

| Alloy | mc_ni (used) | mc_fe v2.062 | COST 507 | Handbook |
|---|---|---|---|---|
| 70-30 | 1,171–1,229 | 1,197–1,243 | 1,201–1,250 | 1,171–1,238 |
| 90-10 | 1,104–1,131 | 1,119–1,146 | 1,131–1,154 | 1,099–1,149 |
| NAB | 1,036–1,112 | 1,031–1,245 (B2 artifact) | 1,050–1,062 (no Al-Ni data) | 1,043–1,060 |

**Reading:**

- **Cu-Ni works.** All three databases are within about 30 °C of the handbook on both liquidus and
  solidus, and mc_ni is within 18 °C. The spread between databases, about 15 to 30 °C, is a fair
  uncertainty for these open descriptions.
- **NAB only partly works.**
  - Solidus and β: mc_ni puts the solidus within 7 °C of the handbook, and β (Cu-rich bcc) forms
    there as the main solidification product.
  - Liquidus: about 4 % of an Fe-rich bcc phase precipitates from the melt starting at 1,112 °C. That
    puts the computed liquidus 51 °C above the handbook value. Primary κ_I from the melt is not the
    accepted picture for 4 wt% Fe, so treat that liquidus as an artifact. The likely cause is the
    missing Cu-Al-Fe-Ni interactions.
  - COST 507's near-perfect NAB numbers come with no NiAl phase at all, so they are partly luck.
- **Scheil ranges** are much wider than both equilibrium and the handbook (about 100 to 170 °C to
  99 % solid). That is typical of Scheil for Cu-Ni, where Mn and Cu enrich the last liquid.

## NAB phase fractions vs temperature (mc_ni, equilibrium)

Panel (b), `nab_phase_fractions.csv`.

| T (°C) | liquid | α (fcc) | β (Cu-rich bcc) | Fe-rich bcc (κ_I/II/IV-like) | NiAl B2 (κ_III-like) |
|---|---|---|---|---|---|
| 1,050 | 0.956 | 0 | 0 | 0.034 | 0.010 |
| 1,000 | 0 | 0 | 0.956 | 0.007 | 0.037 |
| 900 | 0 | 0.252 | 0.658 | 0.035 | 0.055 |
| 800 | 0 | 0.652 | 0.227 | 0.052 | 0.069 |
| 750 | 0 | 0.811 | 0.059 | 0.056 | 0.074 |
| 700 | 0 | 0.865 | 0 | 0.057 | 0.078 |
| 600 | 0 | 0.861 | 0 | 0.057 | 0.082 |

Values are mole fractions.

- **β** forms at the solidus (1,034–1,036 °C) and is nearly the whole alloy down to about 950 °C.
  It then gives way to α and **disappears at about 730 °C** (last nonzero point on the 2 °C grid).
- **α** appears below about 955 °C. NiAl (κ_III-like) is present below 1,070 °C, and Fe-rich bcc
  (κ_I/II/IV-like) below 1,110 °C. At 600 °C the alloy is 86 % α, 8 % NiAl and 6 % Fe-rich bcc.
- **How this compares with the accepted sequence:** the published sequence for C95800 is β first,
  then α out of β, Fe-rich κ, and finally β decomposing to α + κ_III. The calculation reproduces that
  order. The literature usually puts the β eutectoid near 800 °C (e.g., Hasan et al., *Metall. Trans.
  A* 13 (1982) 1337; please check before citing). The computed β-out at about 730 °C is therefore
  probably low by tens of degrees.
- **Why this matters for the proposal:** the calculation says equilibrium NAB holds no β below about
  730 °C. Any β or martensitic β′ retained at room temperature is therefore a cooling-rate effect,
  which supports the proposal's point that fast-cooled DED NAB can keep the selectively corroding β.
- **κ chemistry is approximate.** The modeled NiAl has no Cu or Fe in it, and the Fe-rich κ phases
  (D0₃-based in reality) are modeled as disordered bcc.

## Composition map (mc_ni, equilibrium)

The grid is Ni = 0, 5, …, 30 wt% by Al = 0, 1.9, 3.8, 5.7, 7.6, 9.5 wt%, with Fe fixed at 1 wt%, no Mn
and Cu as balance. 1 wt% Fe sits inside the C70600 Fe spec (1.0 to 1.8 wt%) and near the C71500
range (0.4 to 1.0 wt%). It keeps the map close to the Cu-Ni-Al ternary that the search space spans.

- **Liquidus** ranges from 1,047 °C (Cu-7.6Al-1Fe) to 1,303 °C (Cu-25Ni-9.5Al-1Fe).
- **Freezing range** runs from under 1 °C at Cu-1Fe to 227 °C at Cu-25Ni-9.5Al-1Fe.
- **Primary phase:** α (fcc) at low Al. Once Al ≳ 5.7 wt% with Ni ≥ 5 wt%, it is NiAl (B2), and
  then both the liquidus and the freezing range climb steeply. β is primary only at Cu-9.5Al-1Fe.
- **Liquidus above the proposal's 1,250 °C cap:** only where Ni ≥ 15 and Al = 9.5, or Ni ≥ 25 and
  Al ≥ 7.6. The atomizer's 1,300 °C limit is reached only at Ni 25 to 30 with Al 9.5. Both contours
  are marked in panel (a).
- **Weakest part of the map:** that high-Ni, high-Al corner rests on the NiAl description in a melt
  with no Cu-Al-Ni ternary data. NAB's own liquidus is already 51 °C too high, so treat liquidus and
  freezing range in that corner as upper bounds.
- **Reference alloys:** they are marked at their Ni and Al contents only; their actual Fe and Mn
  differ from the map's 1 wt% Fe.

## Timing

Measured on the GitHub Actions runner, single process:

| Task | Time |
|---|---|
| Load and convert the database | ≈1 s |
| One equilibrium melting range (≈100 equilibrium points: 10 °C scan, then bisection to 0.1 °C) | 0.6 to 1.9 s per composition (mean 1.1 s) |
| The 42-composition map | 46 s in total |
| One Scheil simulation (1 °C steps) | 9 to 10 s per alloy |
| NAB phase-fraction scan (276 temperatures) | a few seconds |
| Whole script | about 85 s |

Rerun on 2026-10-24 on another GitHub Actions runner (same versions, same database): the three result CSVs
were reproduced exactly; one equilibrium melting range took 0.9 to 2.9 s and the 42-composition map 70 s.

"A thermodynamic calculation takes minutes" is therefore conservative for pycalphad. It is seconds
per composition, and minutes for a few hundred compositions, or for Scheil across a whole map (about
10 s per composition).

## Caveats that limit what the proposal can claim

1. **No validated open copper database exists.** mc_ni was built and tested for Ni superalloys; its
   header gives Cu < 0.5 wt%. All Cu-rich results are extrapolations that happen to agree with the
   handbook for Cu-Ni. A Cu-specific database (TCCU, or a new assessment) is still needed for
   quantitative work. That is a fair point to make in the proposal.
2. **Cu-Ni:** usable claims are liquidus and solidus within about 10 to 20 °C of handbook values. The
   Cu-Ni liquid (Jansson) and fcc (COST 507) parameters in mc_ni come from different assessments.
   The self-consistent sets in mc_fe and COST 507 give solidus values 20 to 30 °C higher.
3. **NAB:** the qualitative phase sequence is usable (β at solidification, α + κ below about 950 °C,
   no equilibrium β below about 730 °C). Not usable: the liquidus (+51 °C, from Fe-rich bcc) and the
   κ phase compositions.
4. **Map:** the Al-free and low-Al part is trustworthy (fcc-primary Cu-Ni-Fe). The NiAl-primary,
   high-Ni and high-Al corner is not quantitative.
5. **Handbook values** are measured melting ranges for commercial material and are not strictly
   equilibrium. Scheil gives the opposite bound (no back-diffusion). Neither includes the fast
   solidification of DED.
