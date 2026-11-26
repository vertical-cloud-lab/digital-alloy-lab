# Standards-based EDS of AlSi10Mg: a polished Utah coupon

Source threads: [caliber#35](https://github.com/vertical-cloud-lab/caliber/issues/35) (the
spectra and the DTSA-II results) and
[caliber#12](https://github.com/vertical-cloud-lab/caliber/issues/12#issuecomment-6803490926)
(the standards). Gathered on 2026-11-26.

This is the lab's first EDS quantified against measured standards rather than with the EDAX
software's standardless routine. **It is on a printed part, not on powder.**

![Mg and Si for every run](composition-by-run.png)

*Mg and Si from all 17 runs, renormalized without O, against the AlSi10Mg specification (grey)
and the standardless result for the feedstock powder (dashed). Only the blue run has nothing
wrong with it. The table view is [`results.csv`](results.csv).*

## What was measured

- **Sample.** A polished section of one of the as-built AlSi10Mg tensile coupons printed at the
  University of Utah from the lab's commercial AlSi10Mg powder
  ([`../tensile-alsi10mg-utah/`](../tensile-alsi10mg-utah/), #138).
  - caliber calls it "our tensile sample"
    ([caliber#1](https://github.com/vertical-cloud-lab/caliber/issues/1#issuecomment-5574532841)),
    and the piece was cut on 2026-09-10
    ([photo](https://github.com/vertical-cloud-lab/caliber/issues/1#issuecomment-5622890558)).
    Which coupon it came from isn't recorded.
  - It was polished with the lab's SOP
    ([byu-vcl PR 258](https://github.com/vertical-cloud-lab/byu-vcl/pull/258), last step 0.1 µm
    diamond on the vibratory polisher) and left uncoated.
  - SE images of this surface from 2026-11-06 are in
    [byu-vcl PR 258](https://github.com/vertical-cloud-lab/byu-vcl/pull/258#issuecomment-6750386449).
- **Instrument.** BYU Apreo SEM with an EDAX Octane Plus detector, 34.8-35.4° take-off angle,
  4096 channels of 5 eV, exported from EDAX TEAM as `.msa`.
- **Standards.** Pure Al, pure Si and a cleaved MgO single crystal
  ([caliber PR 20](https://github.com/vertical-cloud-lab/caliber/pull/20)).
  - Each was measured at 5, 10, 15, 20 and 25 kV, about 1 million counts each, 3.2-4.1 nA.
  - Dates: MgO and Si on 2026-11-11, Al on 2026-11-13.
  - The student read each standard's dead time off the EDAX display: 25-32 % at 5 kV, 60-67 %
    at 10 kV and 79-99 % at 15-25 kV
    ([caliber#12](https://github.com/vertical-cloud-lab/caliber/issues/12#issuecomment-6865364302)).
- **Quantification.** The student used NIST DTSA-II ("Polaris 2026-10-07") with the XPP matrix
  correction.
  - Each unknown was fitted against standards taken at its own kV, for O, Mg, Al and Si (C was
    not included).
  - The results are in the DTSA-II reports
    [Sobol 1_6 with MgO.pdf](https://github.com/user-attachments/files/35006676/Sobol.1_6.with.MgO.pdf)
    (2026-11-17) and [Nov 20 2026.pdf](https://github.com/user-attachments/files/35182778/Nov.20.2026.pdf),
    and in [`dtsa2-results.csv`](dtsa2-results.csv).
- **Runs.** There are 17 spectra.
  - **Seed runs.** Six Sobol-design runs (`sobol_exp_1`-`6`, 2026-11-06 and 11-11) seed the
    CALIBER model.
  - **Model-chosen runs.** Trials 6 and 8-17 (11-18 and 11-20) were chosen by the model.
  - **Trial 7.** It has a current logged but no spectrum posted.

## Result

Only one run has nothing wrong with it: `sobol_exp_1_1`, at 5 kV, 6.04 nA and 332 s live time.
The standards and the unknown share the detector setting, the standards ran at low dead time,
and the analytical total is 1.033.

| | O | Mg | Al | Si | Analytical total |
|---|---|---|---|---|---|
| **`sobol_exp_1_1`, DTSA-II normalized** | 2.08 ± 0.11 | **0.35 ± 0.01** | 86.45 ± 0.16 | **11.12 ± 0.13** | 1.033 ± 0.002 |
| Same, renormalized without O | | 0.36 | 88.29 | 11.36 | |
| AlSi10Mg specification (EN AC-43000 / ASTM F3318) | | 0.20-0.45 | balance | 9.0-11.0 | |
| Standardless (TEAM eZAF), feedstock powder, normalized to metals ([`../sem-eds-feedstock/`](../sem-eds-feedstock/)) | | 1.4 | 90.8 | 7.9 | |
| Standardless (TEAM), the first polished section of a Utah coupon, 15 kV ([caliber PR 11](https://github.com/vertical-cloud-lab/caliber/pull/11#issuecomment-5374055623)) | | 1.64 | | | |

Values are wt %. The ± values are DTSA-II's 1σ, from counting statistics and the matrix
correction. They are not run-to-run scatter.

- **Mg is inside the specification.** 0.35 wt % sits in the 0.20-0.45 % range, while the
  standardless numbers read about four times higher.
- **Si is at the top of the range.** 11.1 wt % (11.4 without O) is at or just above the 11.0 %
  limit. Standards-based EDS is usually good to a few percent relative, so this reading can't
  tell 10.8 from 11.4.
- **O is a surface film.** The 2.1 wt % O comes from the native oxide and the polishing film. At
  5 kV most X-rays come from the top few hundred nanometres.
- **The MgO standard was uncoated but did not charge.** Its Duane-Hunt limit at 5 kV is
  5.107 keV, not below the beam energy.
- **One run on one area.**
  - No other run repeats these settings.
  - The coupon has had no independent analysis yet (ICP or spark OES).
  - The unknown ran at about 40,000 counts per second, roughly twice the standards' rate. Its
    analytical total of 1.03 says that did no harm here.

## Why the other 16 runs don't count yet

| Problem | Runs | Effect |
|---|---|---|
| Standards for 10-25 kV taken at 60-99 % dead time | `sobol_exp_2`-`6`, trials 15-17; also trials 6, 9, 11, 14 | Analytical totals 0.91-1.41, and Mg falls with kV, to 0 at 25 kV. Diagnosed in [caliber#35](https://github.com/vertical-cloud-lab/caliber/issues/35#issuecomment-6930731960). Fix: re-collect those standards at about 20,000 counts per second |
| Unknown acquired at a 0.96 µs amp time, while every standard used 7.68 µs | trials 6 and 8-14 (all of 2026-11-18) | Al Kα is 90-92 eV wide against 75-77 eV in the 5 kV standards and the 7.68 µs unknowns. At 5 kV, Mg reads 0.63-0.73 wt % (normalized) and the totals 0.88-0.91. Fix: take standards at 0.96 µs too, or acquire at 7.68 µs |
| MgO standard entered as "Pure magnesium", DTSA-II's default | trials 11 and 14 | Mg about 2.5-2.8 times too high, the error found in [caliber#35](https://github.com/vertical-cloud-lab/caliber/issues/35#issuecomment-6930731960) |

**Checking the amp-time effect.** [`analyze_eds.py`](analyze_eds.py) fits the 5 kV spectra
against the 5 kV standards with a top-hat filter fit. That is the method DTSA-II uses, written
in about 20 lines here; it is not DTSA-II itself.

| 5 kV spectrum | Al Kα FWHM (eV) | Fitted Mg/Al, relative to `sobol_exp_1_1` |
|---|---|---|
| `sobol_exp_1_1`, as measured (7.68 µs) | 76.5 | 1.00 |
| `sobol_exp_1_1`, broadened as a 0.96 µs amp time would | 91.3 | 1.64 |
| trials 8, 10, 12, 13 (0.96 µs) | 90.3-90.9 | 1.55-1.79 |

Broadening the 11-06 spectrum, with nothing else changed, puts its Mg where the 11-18 runs are.
So the resolution mismatch alone is enough to explain their higher Mg. There is no sign that the
Mg content itself differs.

## What this means for the feedstock numbers

**It supports the artifact reading, but doesn't test the powder.**
- **The earlier claim.** The standardless EDS of the feedstock powder gave Mg 1.4 and Si
  7.9 wt % (normalized to metals), outside the specification.
  [`../sem-eds-feedstock/`](../sem-eds-feedstock/) attributes that to the standardless method.
- **What standards add.** With standards, a part printed from the lab's commercial AlSi10Mg
  powder comes out at Mg 0.35 and Si 11.1-11.4 wt %.
- **Why it isn't a powder measurement.** Laser melting can evaporate some Mg, and no
  standards-based EDS of any powder (feedstock or atomized) exists yet.
- **What would settle it.** The supplier's certificate, or ICP of the powder.

## On GitHub but not used here

- **The 2026-04-30 fracture-surface spectrum.** This was a spectrum of a broken coupon's
  fracture surface (#138). It was re-quantified in DTSA-II on 2026-11-16
  ([caliber#35](https://github.com/vertical-cloud-lab/caliber/issues/35#issuecomment-6929087563))
  and gave Mg 0.91 wt %, but it can't be used:
  - MgO was entered as pure Mg.
  - The current was a guess (3.2 nA), and the analytical total is 0.336.
  - The surface is a rough fracture face at 24 mm working distance and a 48.8° take-off angle,
    unlike the standards.
- **The DTSA-II reports.** They are linked above, not copied. They are prints of DTSA-II's
  HTML report and carry the student's local file paths. The 2026-11-18 report
  ([Trials from Nov 18 2026.pdf](https://github.com/user-attachments/files/35052215/Trials.from.Nov.18.2026.pdf))
  is cut off at exactly 4 MiB on GitHub and doesn't open. Trials 9-14 therefore come from the
  screenshots in caliber#35 and from pages 10-16 of the 11-20 report, which repeats them.

## Files

| File | What it is |
|---|---|
| `raw/unknowns/*.msa` | The 17 spectra of the coupon, unmodified. The `sobol_exp_*` files are the "with current" versions from caliber#35, which add a `#PROBECUR` line to the originals |
| `raw/standards/*.msa` | The 15 standard spectra, unmodified but renamed; [`raw/FILES.md`](raw/FILES.md) gives the original names |
| `raw/SHA256SUMS` | Checksums of all 32 spectra |
| [`dtsa2-results.csv`](dtsa2-results.csv) | DTSA-II's results, transcribed from the reports and screenshots, with the source of each row |
| [`results.csv`](results.csv) | Written by `analyze_eds.py`: settings read from each spectrum (kV, current, live time, counts, amp time, Al Kα width), DTSA-II's numbers, the composition without O, and each run's problems |
| [`analyze_eds.py`](analyze_eds.py) | Builds `results.csv` and the figure and runs the amp-time check (numpy, matplotlib) |
| `composition-by-run.png` | The figure above |
