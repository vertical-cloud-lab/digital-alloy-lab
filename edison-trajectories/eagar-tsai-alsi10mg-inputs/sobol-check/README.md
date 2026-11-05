# eagar-tsai Sobol sweep: the `Unable to allocate 762 GiB` errors (issue #235)

A 2^20-point Sobol sweep of [eagar-tsai](https://github.com/ArroyaveLab/eagar-tsai) 0.6.0 over the AlSi10Mg
ranges in [`../README.md`](../README.md) logged one error per row:

```
Error in chunk 5, row 0: Unable to allocate 762. GiB for an array with shape (301,339693421) and data type float64
Error in chunk 6, row 0: Unable to allocate 650. GiB for an array with shape (301,289990823) and data type float64
```

## Cause: the beam diameter was in µm, and eagar-tsai reads metres

The sweep scaled `beam_diameter` to 25–250 (µm) and passed it as `beam_diameter_m`. eagar-tsai's grid
(`_core._build_grids`) starts 1.5 beam diameters ahead of the beam and ends 600 µm behind it, at the
default 1 µm spacing. It is 301 points across (300 µm half-width). Row 5 has `beam_diameter = 226.46`,
read as 226 m, so

nx = (1.5 × 226.46 m + 600 µm) / 1 µm + 1 = 339,693,421, and T_xy = 301 × 339,693,421 × 8 bytes = 762 GiB.

Row 6 (193.33) gives the 650 GiB array. Running the original script on the first 8 rows reproduces both
messages exactly. Every one of the 2^20 rows fails the same way; the smallest array is 84 GiB.
**Fix:** multiply by 1e-6, i.e. sample `beam_diameter_m` from 25e-6 to 250e-6.

## Problems that remain after the unit fix

These measurements come from a 4-vCPU GitHub runner, on the first 64 or 1,024 rows of the same Sobol design.

1. **`return_field=True` (the default) runs out of memory.** It keeps both temperature planes for every row,
   3.3 MB per row at 1 µm (4.6 MB max), so 2^20 rows hold about 3.5 TB. Pass `return_field=False`. That also
   skips the T_xz plane outside the melt pool, which cuts the time by 24% with identical W, D and L.
2. **On Linux, the PyPI wheels use the slow integrand.** All 0.6.0 manylinux wheels (cp312–cp314) link
   `__exp_finite`, which glibc ≥ 2.31 no longer exports, so `import eagar_tsai._integrand_ext` fails and
   eagar-tsai quietly falls back to its pure-Python integrand. One `quad` call takes 137 µs instead of 6 µs,
   so whole rows run 25× slower. The Windows, macOS and musllinux wheels do not have the bad reference.
   Check which integrand you have with
   `python -c "from eagar_tsai._core import _INTEGRAND; print(type(_INTEGRAND))"`. It should print
   `LowLevelCallable`. If it prints `function`, fix it with
   `pip install --force-reinstall --no-deps --no-binary eagar-tsai eagar-tsai` (needs a C compiler).
3. **2^20 rows take days even when everything is right:**

   | Grid | `return_field` | Integrand | Mean s per row per worker | 2^20 rows on 4 workers |
   |---|---|---|---|---|
   | 1 µm (default) | True (default) | compiled | 3.96 | 12 days |
   | 1 µm | False | compiled | 3.00 | 9 days |
   | **2 µm** | **False** | **compiled** | **0.73** (1,024 rows) | **2.2 days** |
   | 5 µm | False | compiled | 0.12 | 9 hours |
   | 5 µm | False | PyPI Linux wheel | 3.28 | 10 days |
   | 1 µm | True | PyPI Linux wheel | 25× the compiled time on the same 8 rows | about a year |

   Against the 1 µm grid (46 melting rows), a 2 µm grid changes W, D and L by at most 2.0, 1.0 and 2.6 µm. A 5 µm grid
   changes them by up to 8.0, 4.0 and 8.1 µm (29% on the shallowest pool). Rows vary a lot: at 2 µm the
   median is 0.66 s, but 1% of rows take over 2.7 s and the slowest takes 9 s. The slow rows are in the slow,
   hot corner, where the domain has to grow.
4. **Some corner rows fail.** For a 25 µm beam at 400 W, 0.1 m/s and A = 0.7, the pool (900 × 450 × 1032 µm) outgrows the
   600 × 300 × 200 µm start domain faster than eagar-tsai's 20 expansion steps can follow (each step is
   0.71 × beam diameter, 18 µm here), giving
   `RuntimeError: Domain expansion did not converge after 20 iterations` and a NaN row. None of the first 1,024
   rows fail, but the corner is in the box. A 1500 × 600 × 500 µm start domain solves it in 8 s.
5. **`chunk_size=1` with 2^20 rows** gives 1,048,576 chunk CSVs and 1,048,576 queued tasks. Building the one-row
   DataFrames alone costs 1.3 GB. Also, `output_dir` names chunk files `ET_0000.csv` onward on every call, so
   calling `compute_melt_pool` batch by batch into one folder overwrites the earlier batches.

## What the corrected sweep returns (first 1,024 rows, 2 µm)

- 269 rows (26%) do not melt (`melt_width_um == 0`). Low absorptivity with a wide beam puts the peak below the
  liquidus.
- 281 of the 755 melting rows (37%) peak above aluminium's boiling point (2743 K), up to 28,800 K in these rows and 40,400 K at the box corner.
  The conduction-only model does not apply there, because it has no vaporisation, recoil or keyhole physics. Filter or
  flag those rows before fitting a surrogate.

## Files

| File | What it is |
|---|---|
| [`../../../scripts/eagar_tsai_sobol_alsi10mg.py`](../../../scripts/eagar_tsai_sobol_alsi10mg.py) | Corrected sweep: SI units with a unit check, `return_field=False`, 2 µm grid, resumable batches, larger-domain retry for failed rows, slow-integrand warning |
| `first-1024-rows-2um.csv` | `python scripts/eagar_tsai_sobol_alsi10mg.py --m 10` (the first 1,024 rows of the 2^20 design, since Sobol prefixes match), compiled integrand |
